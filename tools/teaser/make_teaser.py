#!/usr/bin/env python3
"""A 30-second teaser film of the apps a room sent to the Workshop Studio wall, to show full screen at the end of a class.

    python3 tools/teaser/make_teaser.py --day 2026-12-04 --course geneva --label "Geneva" --date-text "4 December 2026"
    python3 tools/teaser/make_teaser.py --day 2026-11-13 --label "Venice" --date-text "13 November 2026" --voice scratch
    python3 tools/teaser/make_teaser.py ... --voice eleven      # the real voice (ElevenLabs, costs characters; see README.md)

Steps: pick apps from the wall -> run each offline with its data and take two screenshots (as it opens, after one search)
-> narration text -> voice (macOS `say` or ElevenLabs) fitted into 30 s -> synthesized music bed ducked under the voice
-> frames of film/index.html rendered with Playwright -> H.264 + AAC at about -14 LUFS.
Needs only python3 with playwright, httpx and numpy, and ffmpeg. Seat codes are used in memory to pick one app per person
and are never printed or written.
"""
import argparse
import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import wave
from datetime import datetime
from pathlib import Path

import httpx
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bakeoff  # noqa: E402  (tools/bakeoff.py: init_script, inject, launch, COUNTRY, as room_scores.py uses it)

API = "https://150.254.115.204/studio-api"
DURATION, FPS, SR = 30.0, 30, 48000
VOICE_ID, VOICE_MODEL = "JBFqnCBsd6RMkjVDRZzb", "eleven_v4"
MAX_TEMPO = 1.15


def log(*a):
    print(*a, flush=True)


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, capture_output=True, text=True, **kw)


# ── the wall ──────────────────────────────────────────────────────────────────

def http():
    # verify=False for this host only: the studio server's certificate is a Let's Encrypt IP certificate that
    # Python's TLS store may reject. Only this one public, read-only address is ever fetched with it.
    return httpx.Client(timeout=60, verify=False)


def fetch_wall(c=None):
    own = c is None
    c = c or http()
    try:
        return c.get(f"{API}/gallery").raise_for_status().json()
    finally:
        if own:
            c.close()


def filter_wall(wall, days=(), course=None):
    """Items on the given days (by `created`) and, when the wall has a `course` field, in that course."""
    items = [i for i in wall if not days or (i.get("created") or "")[:10] in days]
    if course:
        if any("course" in i for i in wall):
            items = [i for i in items if (i.get("course") or "").lower() == course.lower()]
        else:
            log(f"note: the wall has no `course` field yet; --course {course} is ignored")
    return items


def candidates(items, max_apps):
    """Newest per person ("who") first (one app per person, and not the same title twice), then newest overall; own_* apps skipped."""
    items = sorted((i for i in items if not any(str(k).startswith("own_") for k in i.get("files") or [])),
                   key=lambda i: i.get("created") or "", reverse=True)
    seen, titles, first, rest = set(), set(), [], []
    for i in items:
        if i.get("who") not in seen and i.get("title") not in titles:
            seen.add(i.get("who")); titles.add(i.get("title")); first.append(i)
        else:
            rest.append(i)
    return first + rest


def model_labels():
    cfg = json.loads((ROOT / "site" / "config.json").read_text())["models"]
    return {k: re.sub(r"\s*\(.*?\)", "", v.get("label", k)).strip() for k, v in cfg.items()}


# ── running the apps ─────────────────────────────────────────────────────────

PICK_BUTTON = """() => {
  const bad = /^(search|go|clear|reset|apply|close|menu|download|export|copy|share|next|prev|previous|back|sort|filter|filters|more|show|hide|help|about|submit|print|save|ask|cancel|ok|settings|language|toggle|expand|collapse|load)\\b/i;
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 20 && r.height > 10 && s.visibility !== 'hidden' && s.display !== 'none' && r.top < 900 && r.bottom > 0; };
  let best = null, top = 0;
  for (const b of document.querySelectorAll('button, [role=button]')) {
    if (!vis(b) || b.disabled || b.getAttribute('role') === 'tab') continue;
    const tx = (b.innerText || '').trim();
    if (tx.length < 3 || tx.length > 60 || bad.test(tx) || /^[^a-z0-9]*$/i.test(tx)) continue;
    const ctx = [b.className, b.id, b.parentElement && b.parentElement.className, b.parentElement && b.parentElement.id].join(' ');
    let s = 1;
    if (/example|suggest|chip|sample|try|quick|preset|pill|topic|tag/i.test(ctx)) s += 3;
    if (/\\s/.test(tx)) s += 1;
    if (s > top) { top = s; best = b; }
  }
  if (best && top >= 4) { best.setAttribute('data-teaser-pick', '1'); return best.innerText.trim(); }
  return null;
}"""
TEXT_INPUT = "input[type=search]:visible, input[type=text]:visible, input:not([type]):visible"
ERROR_TEXT = re.compile(r"\b(ReferenceError|TypeError|SyntaxError|Uncaught|is not defined|Something went wrong)\b")


async def capture_app(browser, item, page_html, init, shots: Path, k: int):
    """Two screenshots of an app: as it opens, and after one search. Returns the shot names, or None if the app breaks."""
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))

    async def block(route):   # the apps run offline, as in the studio's sandbox
        if route.request.url.startswith(("about:", "data:", "blob:")):
            await route.continue_()
        else:
            await route.abort()

    await page.route("**/*", block)
    try:
        await page.set_content(bakeoff.inject(page_html, init), wait_until="load", timeout=30000)
        await page.wait_for_timeout(1500)
        body = await page.inner_text("body")
        if errors or len(body.strip()) < 40 or ERROR_TEXT.search(body):
            log(f"  skip {item['id']}: error on open ({(errors or ['empty or error screen'])[0][:90]})")
            return None
        a = shots / f"{k:02d}_a.png"
        await page.screenshot(path=a)
        how = None
        picked = await page.evaluate(PICK_BUTTON)
        try:
            if picked:
                await page.locator("[data-teaser-pick]").first.click(timeout=3000)
                how = f"button “{picked}”"
            else:
                box = page.locator(TEXT_INPUT).first
                if await box.count():
                    await box.fill("children", timeout=3000)
                    await box.press("Enter")
                    how = "typed a word"
                else:
                    sel = page.locator("select:visible").first
                    if await sel.count() and await sel.locator("option").count() > 1:
                        await sel.select_option(index=1, timeout=3000)
                        how = "changed a menu"
        except Exception as e:   # a failed click must not lose the first shot
            log(f"  {item['id']}: no search ({type(e).__name__})")
            how = None
        b = None
        if how:
            await page.wait_for_timeout(1200)
            b = shots / f"{k:02d}_b.png"
            await page.screenshot(path=b)
            if a.read_bytes() == b.read_bytes():
                b.unlink(); b = None
        log(f"  ok   {item['id']} {item.get('title', '')[:50]!r} ({how or 'no search'}{'' if b else ', one shot'})")
        return {"img1": f"shots/{a.name}", "img2": f"shots/{b.name}" if b else None}
    except Exception as e:
        log(f"  skip {item['id']}: {type(e).__name__}: {str(e)[:90]}")
        return None
    finally:
        await ctx.close()


async def capture_all(cands, pages, shots: Path, max_apps, prompts, index, labels):
    from playwright.async_api import async_playwright
    country_file = next(c["file"] for c in index["countries"] if c["name"] == bakeoff.COUNTRY)
    out = []
    async with async_playwright() as pw:
        browser = await bakeoff.launch(pw)
        for it in cands:
            if len(out) >= max_apps:
                break
            keys = set(it.get("files") or []) | {"uhri"}
            if it.get("prompt_id") in prompts and prompts[it["prompt_id"]].get("dataset"):
                keys.add(prompts[it["prompt_id"]]["dataset"])
            init = bakeoff.init_script({k: country_file if k == "uhri" else index["datasets"][k]["file"]
                                        for k in keys if k == "uhri" or k in index["datasets"]})
            got = await capture_app(browser, it, pages[it["id"]], init, shots, len(out) + 1)
            if got:
                name = (it.get("name") or "").strip()
                out.append({**got, "created": it.get("created") or "", "title": (it.get("title") or "Untitled").strip(),
                            "model": labels.get(it.get("model"), it.get("model") or "an AI model"), "name": name[:40] or None})
        await browser.close()
    return sorted(out, key=lambda a: a["created"])


# ── narration ────────────────────────────────────────────────────────────────

def join_names(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def narration(n, people, label, date_text, names):
    """Six short lines, plain English. Every line is true of any workshop app: real UN documents, a source for each passage."""
    who = f"{people} people" if people != 1 else "one person"
    tools = f"{n} tools" if n != 1 else "a tool"
    where = ", ".join(x for x in (f"Garage Research {label}".strip(), date_text) if x)
    lines = [
        f"Today, {who} in this room built {tools} of their own.",
        "Each started from a brief, read a plan, and changed it before anything was built.",
        "Every tool works from real UN documents and shows where each passage comes from.",
        "Each one is different: its own question, its own look." + (f" Among the builders: {join_names(names[:3])}." if names else ""),
        "None of them summarises. Every quotation can be checked against its source.",
        f"Built in {where}." if where else "Built in Garage Research.",
    ]
    words = sum(len(l.split()) for l in lines)
    if words > 72 and names:   # too long with names: drop the sentence rather than speed the voice up
        lines[3] = "Each one is different: its own question, its own look."
        words = sum(len(l.split()) for l in lines)
    if not 55 <= words <= 72:
        log(f"warning: narration has {words} words (aim 55-70)")
    return lines


# ── voice ────────────────────────────────────────────────────────────────────

def read_wav(p):
    with wave.open(str(p)) as w:
        assert w.getsampwidth() == 2
        ch = w.getnchannels()
        y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return y.reshape(-1, ch).mean(1) if ch > 1 else y


def write_wav(p, y):
    y = np.clip(y, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1 if y.ndim == 1 else y.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())


def to_wav(src, dst, tempo=1.0):
    af = f"atempo={tempo:.4f}" if tempo != 1.0 else "anull"
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", SR, "-af", af, "-c:a", "pcm_s16le", dst])


def trim(y):
    idx = np.where(np.abs(y) > 0.012)[0]
    return y[max(0, idx[0] - 480): idx[-1] + 2400] if len(idx) else y


def eleven_key():
    for line in (Path.home() / ".env").read_text().splitlines():
        m = re.match(r"\s*(?:export\s+)?ELEVENLABS_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
        if m:
            return m.group(1)
    sys.exit("ELEVENLABS_API_KEY is not in ~/.env")


def take(line, voice, tmp: Path, i: int):
    """One narration line as a raw audio file. ElevenLabs takes are cached by (voice, model, text), so a rerun with the same lines is free."""
    if voice == "scratch":
        out = tmp / f"line{i}.aiff"
        run(["say", "-v", "Daniel", "-o", out, "--", line])
        return out, 0
    cache = HERE / "cache"
    cache.mkdir(exist_ok=True)
    f = cache / (hashlib.sha256(json.dumps([VOICE_ID, VOICE_MODEL, line]).encode()).hexdigest()[:24] + ".mp3")
    if f.exists():
        return f, 0
    r = httpx.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128",
                   headers={"xi-api-key": eleven_key()},
                   json={"text": line, "model_id": VOICE_MODEL, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
                   timeout=120)
    if r.status_code != 200:
        sys.exit(f"ElevenLabs answered {r.status_code}: {r.text[:200]}")
    f.write_bytes(r.content)
    return f, len(line)


def make_voice(lines, voice, tmp: Path):
    """Returns (voice track at 30 s, [{text,start,end}]). Silences trimmed; tempo up to 1.15 if the lines do not fit."""
    raws, sent = [], 0
    for i, l in enumerate(lines):
        f, c = take(l, voice, tmp, i)
        raws.append(f); sent += c
    if voice == "eleven":
        log(f"ElevenLabs: {sent} characters sent this run (cached takes cost nothing)")
    clips = []
    for i, f in enumerate(raws):
        w = tmp / f"line{i}.wav"
        to_wav(f, w)
        write_wav(w, trim(read_wav(w)))
        clips.append(w)
    start, end_by, gap_min = 0.4, 29.4, 0.15
    total = sum(len(read_wav(w)) for w in clips) / SR
    tempo = 1.0
    need = total / (end_by - start - gap_min * (len(lines) - 1))
    if need > 1.0:
        tempo = min(MAX_TEMPO, need)
        for i, w in enumerate(clips):
            w2 = tmp / f"line{i}_t.wav"
            to_wav(w, w2, tempo)
            clips[i] = w2
        if need > MAX_TEMPO:
            log(f"warning: the voice is {total:.1f} s; even at {MAX_TEMPO}x it does not fit 30 s. Shorten the lines.")
    ys = [read_wav(w) for w in clips]
    dur = sum(len(y) for y in ys) / SR
    gap = float(np.clip((end_by - start - dur) / (len(ys) - 1), gap_min, 0.9))
    track = np.zeros(int(DURATION * SR), np.float32)
    timing, t = [], start
    for l, y in zip(lines, ys):
        a = int(t * SR)
        seg = y[: max(0, len(track) - a)]
        track[a:a + len(seg)] += seg
        timing.append({"text": l, "start": round(t, 3), "end": round(min(t + len(y) / SR + 0.1, DURATION), 3)})
        t += len(y) / SR + gap
    log(f"voice: {dur:.1f} s of speech, tempo {tempo:.2f}x, last line ends at {timing[-1]['end']:.1f} s")
    return track, timing


# ── music: a calm 120 BPM bed in A minor (after the film studio's score), ducked under the voice ──

def music():
    BEAT = 0.5
    N = int(DURATION * SR)
    mix = np.zeros((N, 2), np.float32)
    rng = np.random.default_rng(76)
    noise = (rng.random(SR) * 2 - 1).astype(np.float32)

    def midi(n):
        return 440.0 * 2 ** ((n - 69) / 12)

    def place(buf, t, gain=1.0, pan=0.0):
        i = int(round(t * SR)); j = min(N, i + len(buf))
        if j <= i:
            return
        mix[i:j, 0] += buf[: j - i] * np.cos((pan + 1) * np.pi / 4) * gain
        mix[i:j, 1] += buf[: j - i] * np.sin((pan + 1) * np.pi / 4) * gain

    def felt(freq, dur=1.4):
        t = np.arange(int(dur * SR)) / SR
        out = np.zeros_like(t, dtype=np.float32)
        for k in range(1, 8):
            f = freq * k * (1 + 0.0004 * k * k)
            if f > 9000:
                break
            out += (1.0 / k ** 1.6) * np.sin(2 * np.pi * f * t) * np.exp(-t * (2.2 + 1.4 * k))
        return (out * np.minimum(1, t / 0.006)).astype(np.float32)

    def pad(freqs, dur, att=0.9, rel=1.2):
        t = np.arange(int(dur * SR)) / SR
        out = np.zeros_like(t, dtype=np.float32)
        for f0 in freqs:
            for det in (-0.12, 0.0, 0.11):
                for k in range(1, 7):
                    out += (1.0 / k ** 2.1) * np.sin(2 * np.pi * f0 * 2 ** (det / 12) * k * t + k * 0.7)
        env = np.minimum(1, t / att) * np.minimum(1, np.maximum(0, dur - t) / rel)
        return (out * env / (3 * len(freqs))).astype(np.float32)

    def kick():
        t = np.arange(int(0.35 * SR)) / SR
        ph = 2 * np.pi * np.cumsum(46 + 70 * np.exp(-t * 32)) / SR
        return (np.sin(ph) * np.exp(-t * 9) + noise[: len(t)] * np.exp(-t * 400) * 0.25).astype(np.float32)

    def hat():
        t = np.arange(int(0.05 * SR)) / SR
        return (np.diff(np.concatenate([[0], noise[1000:1000 + len(t)]])) * np.exp(-t * 90) * 0.5).astype(np.float32)

    def bass(freq, dur):
        t = np.arange(int(dur * SR)) / SR
        s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
        return (s * np.minimum(1, t / 0.02) * np.exp(-t * 1.1) * np.minimum(1, (dur - t) / 0.08)).astype(np.float32)

    chords = [([57, 60, 64, 71], 45), ([53, 57, 60, 64], 41), ([48, 52, 55, 62], 48), ([55, 59, 62, 69], 43)]
    arp = [0, 2, 1, 3, 2, 1, 3, 2]
    bar = 4 * BEAT
    for b in range(int(np.ceil(DURATION / bar))):
        t0 = b * bar
        notes, root = chords[b % 4]
        place(pad([midi(n) for n in notes], bar + 1.2), t0, gain=0.10 if t0 < 4 else 0.075)
        if t0 >= 4:
            for i, idx in enumerate(arp):
                place(felt(midi(notes[idx] + 12)), t0 + i * BEAT / 2, gain=0.12 if i % 2 == 0 else 0.08, pan=-0.35 if i % 2 else 0.35)
            place(bass(midi(root), bar * 0.95), t0, gain=0.22)
            for q in range(4):
                if q in (0, 2):
                    place(kick(), t0 + q * BEAT, gain=0.30)
                if t0 + q * BEAT >= 10:
                    place(hat(), t0 + q * BEAT + BEAT / 2, gain=0.09, pan=0.25)
        else:
            place(felt(midi(notes[0] + 12)), t0, gain=0.11)
    fade = SR
    mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return mix / max(1e-9, np.abs(mix).max()) * 0.7


def duck_curve(voice):
    """1 where the voice is silent, ~0.3 under speech; quick attack, slow release."""
    env = np.convolve(np.abs(voice), np.ones(int(0.12 * SR)) / int(0.12 * SR), mode="same")
    want = 1 - 0.7 * np.clip(env / 0.03, 0, 1)
    out = np.empty_like(want); g = 1.0
    step = 1 / SR
    a_down, a_up = 1 - np.exp(-step / 0.08), 1 - np.exp(-step / 0.5)
    # a one-pole follower, computed in blocks of 48 samples (1 ms) to stay fast in numpy
    B = 48
    for s in range(0, len(want), B):
        w = want[s:s + B].min()
        g += (w - g) * ((a_down if w < g else a_up) * B)
        out[s:s + B] = g
    return out


def mix_audio(voice, tmp: Path):
    bed = music() * 0.55
    d = duck_curve(voice)
    stereo = bed * d[:, None] + np.stack([voice, voice], 1) * 1.0
    raw = tmp / "mix.wav"
    write_wav(raw, stereo)
    out = tmp / "master.wav"
    # two-pass loudnorm to -14 LUFS
    p = subprocess.run(["ffmpeg", "-hide_banner", "-y", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, check=True)
    m = json.loads(re.findall(r"\{[^{}]*\}", p.stderr)[-1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample={SR},apad,atrim=0:{DURATION}")
    run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", SR, "-c:a", "pcm_s16le", out])
    return out


# ── the film ─────────────────────────────────────────────────────────────────

async def render_frames(work: Path, workers=3):
    from playwright.async_api import async_playwright
    frames = work / "frames"
    frames.mkdir(exist_ok=True)
    n = int(DURATION * FPS)
    async with async_playwright() as pw:
        browser = await bakeoff.launch(pw)

        async def worker(w):
            ctx = await browser.new_context(viewport={"width": 1920, "height": 1080})
            page = await ctx.new_page()
            await page.goto((work / "film" / "index.html").as_uri())
            await page.evaluate("window.READY")
            for f in range(w, n, workers):
                await page.evaluate(f"seek({f / FPS})")
                await page.screenshot(path=frames / f"{f:05d}.jpg", type="jpeg", quality=93)
            await ctx.close()

        await asyncio.gather(*(worker(w) for w in range(workers)))
        await browser.close()
    return frames


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--course", help="only apps whose `course` field matches (ignored while the wall has no such field)")
    ap.add_argument("--day", action="append", default=[], help="only apps created on this day (YYYY-MM-DD); repeat for more")
    ap.add_argument("--max-apps", type=int, default=5)
    ap.add_argument("--label", default="", help="the room, e.g. Geneva")
    ap.add_argument("--date-text", default=None, help="the date as shown, e.g. '4 December 2026' (default: from a single --day)")
    ap.add_argument("--voice", choices=["scratch", "eleven"], default="scratch")
    ap.add_argument("--out", default=str(HERE / "out"))
    ap.add_argument("--keep", action="store_true", help="keep the working folder (screenshots, frames)")
    return ap.parse_args()


def make(a) -> Path:
    t0 = time.time()
    out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    work = out / f"work-{stamp}"
    shutil.copytree(HERE / "film", work / "film")
    shots = work / "film" / "shots"; shots.mkdir()

    wall = filter_wall(fetch_wall(), a.day, a.course)
    if not wall:
        sys.exit("no apps on the wall for these filters")
    people = len({i.get("who") for i in wall})   # "who": one key per seat, never the seat code
    log(f"wall: {len(wall)} apps from {people} people match")
    cands = candidates(wall, a.max_apps)
    with http() as c:
        pages = {}
        for i in cands[: a.max_apps * 4]:   # a few spare in case some apps break on open
            pages[i["id"]] = c.get(f"{API}/gallery/{i['id']}").raise_for_status().text
    cands = [i for i in cands if i["id"] in pages]
    raw = json.loads((ROOT / "site" / "data" / "prompts.json").read_text())
    prompts = {p["id"]: p for p in (raw["prompts"] if isinstance(raw, dict) else raw)}
    index = json.loads((ROOT / "site" / "data" / "index.json").read_text())
    log("capturing apps")
    apps = asyncio.run(capture_all(cands, pages, shots, a.max_apps, prompts, index, model_labels()))
    if not apps:
        sys.exit("no app could be captured")
    t_cap = time.time() - t0

    date_text = a.date_text if a.date_text is not None else (datetime.strptime(a.day[0], "%Y-%m-%d").strftime("%-d %B %Y") if len(a.day) == 1 else "")
    names = [x["name"] for x in apps if x["name"]]
    lines = narration(len(wall), people, a.label, date_text, names)
    for l in lines:
        log("  ·", l)
    voice, timing = make_voice(lines, a.voice, work)
    master = mix_audio(voice, work)

    data = {"label": a.label, "dateText": date_text, "n": len(wall), "duration": DURATION, "lines": timing,
            "apps": [{k: x[k] for k in ("img1", "img2", "title", "model", "name")} for x in apps]}
    (work / "film" / "data.js").write_text("window.TEASER = " + json.dumps(data, ensure_ascii=False) + ";\n")
    log("rendering frames")
    frames = asyncio.run(render_frames(work))
    mp4 = out / f"teaser-{stamp}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-framerate", FPS, "-i", frames / "%05d.jpg", "-i", master,
         "-c:v", "libx264", "-preset", "medium", "-crf", 18, "-vf", "scale=in_range=pc:out_range=tv,format=yuv420p", "-r", FPS,
         "-c:a", "aac", "-b:a", "192k", "-t", DURATION, "-movflags", "+faststart", mp4])
    shutil.copy(mp4, out / "latest.mp4")
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]).stdout)
    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    log(f"{mp4}  ({dur:.2f} s, {len(apps)} apps, total {time.time() - t0:.0f} s of which capture {t_cap:.0f} s)")
    return mp4


if __name__ == "__main__":
    make(parse_args())
