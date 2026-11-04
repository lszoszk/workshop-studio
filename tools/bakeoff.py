#!/usr/bin/env python3
"""Bake-off: every studio model on every workshop prompt, scored in headless Chromium.

Sends exactly what the studio sends (system_prompt.md + schema.md + samples.json + the
participant's prompt), extracts the HTML, runs it offline with the full data pack
injected, and checks it against site/data/prompts.json. Writes the HTML, a
screenshot and the scores to tests/bakeoff/<run>/, plus report.html for the gallery.

    python3 tools/bakeoff.py --models mistral --prompts s7-1-dashboard     # smoke test
    python3 tools/bakeoff.py                                              # everything
    python3 tools/bakeoff.py --rescore tests/bakeoff/2026-11-01T10-00       # checks only

Needs OPENROUTER_API_KEY in ~/.env, httpx and playwright (chromium).
"""
import argparse
import asyncio
import html as htmllib
import json
import re
import time
from datetime import datetime
from pathlib import Path

import httpx
from planning import compose   # tools/planning.py
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = SITE / "data"
PROMPTS = DATA / "prompts.json"
OUT = ROOT / "tests" / "bakeoff"

# id -> (OpenRouter model, pinned provider slug, label). Mirrors the studio menu.
MODELS = {
    "mistral": ("mistralai/mistral-large-4-0", "mistral/eu", "Mistral Large 4 · France · Mistral (EU)"),
    "claude": ("anthropic/claude-sonnet-5.5", "amazon-bedrock/us-east-1", "Claude Sonnet 5.5 · USA · Amazon Bedrock"),
    # the previous Mistral flagship: no thinking before the answer, so a build takes minutes less
    "mistral-l3": ("mistralai/mistral-large-2512", "mistral/eu", "Mistral Large 3 · France · Mistral (EU)"),
    "glm-cn": ("z-ai/glm-5.3", "z-ai", "GLM-5.3 · China · Z.AI"),
    "glm-eu": ("z-ai/glm-5.3", "mistral/nvfp4/eu", "GLM-5.3 · China · Mistral (EU)"),
    # candidates for the China slot (DeepSeek's own service refuses zero data retention)
    "kimi": ("moonshotai/kimi-k3.1-pro", "moonshotai", "Kimi K3.1 Pro · China · Moonshot AI"),
    "deepseek": ("deepseek/deepseek-v4-pro-0813", "nebius", "DeepSeek V4 Pro · China, open weights · Nebius"),
    # open weights small enough for a laptop; same 4-bit (MXFP4) weights, run here by CoreWeave
    "gptoss": ("openai/gpt-oss-20b", "coreweave", "gpt-oss-20b · USA, open weights · laptop-size, 4-bit · CoreWeave"),
}
DEFAULT_MODELS = ["mistral", "claude", "glm-cn"]
COUNTRY = "Kenya"
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def api_key():
    for line in (Path.home() / ".env").read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("OPENROUTER_API_KEY missing in ~/.env")


def system_prompt():
    sp = (DATA / "system_prompt.md").read_text().split("\n---\n", 1)[1].strip()
    samples = json.loads((DATA / "samples.json").read_text())
    return "\n\n".join([
        sp,
        (DATA / "schema.md").read_text().strip(),
        "## Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)\n\n```json\n"
        + json.dumps(samples, ensure_ascii=False, indent=1) + "\n```",
    ])


def request_text(p):
    """What a participant sends: the request, or for a workshop app with a planning package the plan
    composed from its default answers (tools/planning.py compose(), the same text as composePlan() in
    studio.js). Without the package the studio sends the request as written, and so does this."""
    pack = DATA / p["planning"] if p.get("planning") else None
    if not pack or not pack.exists():
        return p["prompt"].replace("{country}", COUNTRY)
    return compose(json.loads(pack.read_text()), {}, COUNTRY)


def attached(key):
    """The line the studio adds when the participant drags this file into the chat."""
    f = next(f for f in json.loads((SITE / "config.json").read_text())["files"] if f["key"] == key)
    also = "".join(f", with WORKSHOP_DATA.{k}" for k in f.get("also", []))
    return f"\n\n(Attached: {f['label'].replace('{country}', COUNTRY)} → WORKSHOP_DATA.{key}{also})"


def extract_html(text):
    # the closing fence follows </html>: the app's own code may contain ``` (same rule as the studio)
    m = re.search(r"```html\s*(.*?</html>)\s*```", text, re.S | re.I) or re.search(r"```html\s*(.*?)```", text, re.S)
    if m:
        return m.group(1).strip()
    m = re.search(r"(<!doctype html.*</html>)", text, re.S | re.I)
    return m.group(1).strip() if m else ""


REASONING = None  # set from --reasoning: OpenRouter reasoning effort (low/medium/high)


async def generate(client, key, model_id, messages, tries=2):
    """Streams, like the studio does: long generations survive idle-connection cuts,
    and we get time to first token. One retry on a dropped connection."""
    mid, provider, _ = MODELS[model_id]
    body = {
        "model": mid,
        "messages": messages,
        "max_tokens": 64000,
        "temperature": 0.3,
        "stream": True,
        "provider": {"only": [provider], "allow_fallbacks": False, "zdr": True},
        "usage": {"include": True},
    }
    if REASONING:
        body["reasoning"] = {"effort": REASONING}
    for attempt in range(tries):
        t0, first, parts, usage, prov = time.monotonic(), None, [], {}, None
        think_first, thoughts = None, []
        try:
            async with client.stream("POST", "https://openrouter.ai/api/v1/chat/completions", json=body,
                                     headers={"Authorization": f"Bearer {key}", "X-Title": "Workshop Studio bake-off"},
                                     timeout=httpx.Timeout(600, read=180)) as r:
                if r.status_code != 200:
                    return {"error": f"{r.status_code} {(await r.aread())[:300]!r}", "seconds": round(time.monotonic() - t0, 1)}
                async for line in r.aiter_lines():
                    if not line.startswith("data: ") or line == "data: [DONE]":
                        continue
                    d = json.loads(line[6:])
                    if "error" in d:
                        return {"error": json.dumps(d["error"])[:300], "seconds": round(time.monotonic() - t0, 1)}
                    prov = d.get("provider") or prov
                    for c in d.get("choices") or []:
                        thought = (c.get("delta") or {}).get("reasoning")
                        if thought:
                            think_first = think_first or time.monotonic()
                            thoughts.append(thought)
                        delta = (c.get("delta") or {}).get("content")
                        if delta:
                            first = first or time.monotonic()
                            parts.append(delta)
                    usage = d.get("usage") or usage
            return {
                "text": "".join(parts),
                "seconds": round(time.monotonic() - t0, 1),
                "first_token": round(first - t0, 1) if first else None,
                "first_thought": round(think_first - t0, 1) if think_first else None,
                "reasoning_chars": sum(map(len, thoughts)),
                "thought": "".join(thoughts),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "cost": usage.get("cost"),
                "provider": prov,
            }
        except (httpx.TransportError, json.JSONDecodeError) as e:
            if attempt == tries - 1:
                return {"error": f"{type(e).__name__}: {e}", "seconds": round(time.monotonic() - t0, 1)}


async def launch(pw):
    try:
        return await pw.chromium.launch()
    except Exception:  # bundled Chromium missing: use the installed Chrome
        return await pw.chromium.launch(channel="chrome")


def init_script(dataset_files):
    chart = (SITE / "vendor" / "chart.umd.min.js").read_text()
    data = {k: json.loads((DATA / f).read_text()) for k, f in dataset_files.items()}
    return (
        chart
        + "\nwindow.WORKSHOP_DATA = " + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";\n"
        + """
window.__asks = [];
window.studio = { ask: async (prompt, opts) => {
  const ids = (prompt.match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/g) || []);
  window.__asks.push({ids: [...new Set(ids)].length, chars: prompt.length});
  await new Promise(r => setTimeout(r, 50));
  const out = [...new Set(ids)].map(id => ({id, sdgs: [16]}));
  return JSON.stringify(out);
}, openSource: (symbol, page) => { window.__opened = (window.__opened || []).concat([[symbol, page]]); }};
"""
    )


CHART_CDN = re.compile(r"""<script\b[^>]*\bsrc=["']https?://[^"']*\bchart(?:\.js|\.umd|\.min)[^"']*["'][^>]*>\s*</script>""", re.I)


def inject(page_html, init):
    """Put the bootstrap in front of the app's own scripts, as the studio's srcdoc does (which also drops
    a Chart.js loaded from a CDN: the studio has its own, site/preview-doc.js)."""
    page_html = CHART_CDN.sub("<!-- Chart.js: the studio's own copy, not the internet -->", page_html)
    tag = "<script>" + init + "</script>"
    m = re.search(r"<head[^>]*>", page_html, re.I) or re.search(r"<html[^>]*>", page_html, re.I)
    if m:
        return page_html[:m.end()] + tag + page_html[m.end():]
    return tag + page_html


SETTINGS = {"ask_button", "ask_steps"}   # in a prompt's `checks` but not a check: the label of the button that calls studio.ask


async def score(browser, page_html, checks, init, shot_path):
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
    page = await ctx.new_page()
    errors, network = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))

    async def block(route):
        if not route.request.url.startswith(("about:", "data:", "blob:")):
            network.append(route.request.url)
        await route.abort()

    await page.route("**/*", block)
    res = {}
    try:
        await page.set_content(inject(page_html, init), wait_until="load", timeout=30000)
        await page.wait_for_timeout(1500)
        tabs = page.locator("[role=tab]:visible")
        n_tabs = await tabs.count()

        async def anywhere(probe):
            """True if probe() holds on the first view or after clicking one of the app's tabs (Hick's-law layout)."""
            if await probe():
                return True
            for i in range(n_tabs):
                await tabs.nth(i).click()
                await page.wait_for_timeout(400)
                if await probe():
                    return True
            return False

        texts = [await page.inner_text("body")]
        for i in range(n_tabs):
            await tabs.nth(i).click()
            await page.wait_for_timeout(400)
            texts.append(await page.inner_text("body"))
        if n_tabs:
            await tabs.nth(0).click()
            await page.wait_for_timeout(400)
        text = "\n".join(texts)
        country = COUNTRY
        # a button may sit in a row that opens on click, so look for it after the search has filled the list
        for name, want in sorted(checks.items(), key=lambda kv: kv[0] == "button_matches"):
            if name in SETTINGS:
                continue
            if name == "no_console_errors":
                res[name] = not errors
            elif name == "no_network":
                res[name] = not network
            elif name == "uses_workshop_data":
                res[name] = "WORKSHOP_DATA" in page_html
            elif name == "chart":
                res[name] = await anywhere(lambda: page.evaluate(
                    "() => (window.Chart && Object.keys(Chart.instances||{}).length > 0) || "
                    "[...document.querySelectorAll('svg,canvas')].some(e => { const r = e.getBoundingClientRect(); return r.width > 120 && r.height > 80; })"))
            elif name == "table_min_rows":
                res[name] = await anywhere(lambda: page.evaluate(
                    f"() => document.querySelectorAll('tbody tr, [role=row]').length >= {int(want)}"))
            elif name == "text_contains":
                res[name] = all(w.replace("{country}", country).lower() in text.lower() for w in want)
            elif name == "text_matches":
                res[name] = bool(re.search(want, text))
            elif name == "controls_min":
                n = await page.evaluate("() => document.querySelectorAll('select, input, [role=combobox]').length")
                res[name] = n >= want
            elif name == "links_to":
                res[name] = await anywhere(lambda: page.evaluate(f"() => !!document.querySelector('a[href*=\"{want}\"]')"))
            elif name == "source_matches":
                res[name] = bool(re.search(want, page_html))
            elif name == "button_matches":
                async def has_button():
                    labels = await page.evaluate("() => [...document.querySelectorAll('button, [role=button], input[type=button]')].map(b => b.innerText || b.value || '')")
                    return any(re.search(want, l) for l in labels)
                async def has_button_deeper():   # one click deeper: open the first collapsed items in this view
                    if await has_button():
                        return True
                    closed = page.locator("button[aria-expanded=false]:visible, tbody tr:visible")
                    for _ in range(min(4, await closed.count())):
                        await closed.nth(0).click()
                        await page.wait_for_timeout(400)
                        if await has_button():
                            return True
                    return False
                res[name] = await anywhere(has_button_deeper)
            elif name == "download":
                res[name] = bool(re.search(r"Blob|download\s*=|\.download\b", page_html))
            elif name == "search_box":
                res[name] = await page.evaluate("() => !!document.querySelector('input[type=search], input[type=text], input:not([type])')")
            elif name == "text_contains_after_search":
                box = page.locator("input[type=search]:visible, input[type=text]:visible, input:not([type]):visible").first
                await anywhere(lambda: box.count())
                await box.fill(want["query"])
                await box.press("Enter")
                await page.wait_for_timeout(1200)
                res[name] = want["expect"].lower() in (await page.inner_text("body")).lower()
            elif name in ("calls_studio_ask", "batches_max"):
                if "calls_studio_ask" not in res:
                    # ask_steps: buttons to press in order (a tab, then the button that sends); else one ask_button
                    for step in checks.get("ask_steps") or [checks.get("ask_button", "suggest|ai")]:
                        btn = page.locator("button:visible", has_text=re.compile(step, re.I)).first
                        if await anywhere(lambda: btn.count()):
                            await btn.click()
                            await page.wait_for_timeout(800)
                    await page.wait_for_timeout(3200)
                    asks = await page.evaluate("() => window.__asks")
                    res["calls_studio_ask"] = bool(asks)
                    res["batches_max"] = bool(asks) and max(a["ids"] for a in asks) <= checks.get("batches_max", 25)
        await page.screenshot(path=str(shot_path), full_page=False)
    except Exception as e:  # a broken page fails every check it did not reach
        errors.append(f"harness: {e}")
        for name in checks:
            if name not in SETTINGS:
                res.setdefault(name, False)
    finally:
        await ctx.close()
    return res, errors[:5], network[:5]


async def run(models, prompt_ids, outdir):
    key = api_key()
    sp = system_prompt()
    spec = [p for p in json.loads(PROMPTS.read_text())["prompts"] if p.get("bakeoff", True)]
    spec = [p for p in spec if not prompt_ids or p["id"] in prompt_ids or any(
        q["id"] in prompt_ids and q.get("builds_on") == p["id"] for q in spec)]
    index = json.loads((DATA / "index.json").read_text())
    country_file = next(c["file"] for c in index["countries"] if c["name"] == COUNTRY)
    files = {"uhri": country_file, **{k: v["file"] for k, v in index["datasets"].items()}}
    init = init_script(files)
    results = []
    async with httpx.AsyncClient() as client, async_playwright() as pw:
        browser = await launch(pw)

        async def one_model(m):
            convo = {}  # prompt id -> messages after that prompt's answer
            for p in spec:
                user = request_text(p) + attached(p["dataset"])
                base = convo.get(p["builds_on"]) if p.get("builds_on") else None
                messages = (base or [{"role": "system", "content": sp}]) + [{"role": "user", "content": user}]
                g = await generate(client, key, m, messages)
                page_html = extract_html(g.get("text", ""))
                d = outdir / m
                d.mkdir(parents=True, exist_ok=True)
                (d / f"{p['id']}.html").write_text(page_html or "<!-- no html -->", encoding="utf-8")
                (d / f"{p['id']}.reply.md").write_text(g.get("text") or g.get("error", ""), encoding="utf-8")
                if g.get("thought"):   # the studio replays it before the answer in recorded mode
                    (d / f"{p['id']}.thought.md").write_text(g["thought"], encoding="utf-8")
                if page_html:
                    convo[p["id"]] = messages + [{"role": "assistant", "content": g["text"]}]
                    checks, errs, net = await score(browser, page_html, p["checks"], init, d / f"{p['id']}.png")
                else:
                    checks, errs, net = {k: False for k in p["checks"]}, [g.get("error", "no html in reply")], []
                r = {"model": m, "label": MODELS[m][2], "prompt": p["id"], "checks": checks,
                     "passed": sum(checks.values()), "total": len(checks), "errors": errs, "network": net,
                     "lines": page_html.count("\n") + 1 if page_html else 0,
                     **{k: g.get(k) for k in ("seconds", "first_token", "first_thought", "reasoning_chars", "prompt_tokens", "completion_tokens", "cost", "provider")}}
                results.append(r)
                print(f"{m:8} {p['id']:22} {r['passed']}/{r['total']}  thought@{r['first_thought']}s code@{r['first_token']}s  {r['seconds']}s  ${r['cost'] or 0:.3f}  {errs[:1]}")

        for m, err in zip(models, await asyncio.gather(*(one_model(m) for m in models), return_exceptions=True)):
            if isinstance(err, Exception):
                print(f"{m}: stopped early: {type(err).__name__}: {err}")
        await browser.close()
    (outdir / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    report(outdir, results)


async def rescore(outdir):
    spec = {p["id"]: p for p in json.loads(PROMPTS.read_text())["prompts"]}
    index = json.loads((DATA / "index.json").read_text())
    country_file = next(c["file"] for c in index["countries"] if c["name"] == COUNTRY)
    init = init_script({"uhri": country_file, **{k: v["file"] for k, v in index["datasets"].items()}})
    results = json.loads((outdir / "results.json").read_text())
    async with async_playwright() as pw:
        browser = await launch(pw)
        for r in results:
            f = outdir / r["model"] / f"{r['prompt']}.html"
            reply = f.with_suffix(".reply.md")
            if reply.exists():   # extract again, so a fix to extract_html reaches old runs
                f.write_text(extract_html(reply.read_text()) or "<!-- no html -->", encoding="utf-8")
            page_html = f.read_text()
            if page_html.startswith("<!-- no html"):
                continue
            r["lines"] = page_html.count("\n") + 1
            checks, errs, net = await score(browser, page_html, spec[r["prompt"]]["checks"], init,
                                            outdir / r["model"] / f"{r['prompt']}.png")
            r.update(checks=checks, passed=sum(checks.values()), total=len(checks), errors=errs, network=net)
            print(f"{r['model']:8} {r['prompt']:22} {r['passed']}/{r['total']}")
        await browser.close()
    (outdir / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
    report(outdir, results)


def report(outdir, results):
    prompts = list(dict.fromkeys(r["prompt"] for r in results))
    models = list(dict.fromkeys(r["model"] for r in results))
    by = {(r["model"], r["prompt"]): r for r in results}
    rows = []
    for p in prompts:
        cells = []
        for m in models:
            r = by.get((m, p))
            if not r:
                cells.append("<td></td>")
                continue
            fails = ", ".join(k for k, v in r["checks"].items() if not v) or "all checks passed"
            cells.append(
                f"<td><a href='{m}/{p}.html' target='_blank'><img src='{m}/{p}.png' loading='lazy'></a>"
                f"<div class='s'>{r['passed']}/{r['total']} · {r['seconds']} s · ${r['cost'] or 0:.3f} · {r['lines']} lines</div>"
                f"<div class='f'>{htmllib.escape(fails)}</div></td>")
        rows.append(f"<tr><th>{p}</th>{''.join(cells)}</tr>")
    head = "".join(f"<th>{htmllib.escape(MODELS[m][2])}</th>" for m in models)
    (outdir / "report.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Bake-off {outdir.name}</title>
<style>body{{font:14px system-ui;margin:24px}}table{{border-collapse:collapse}}td,th{{border:1px solid #ddd;padding:8px;vertical-align:top}}
img{{width:420px;display:block}}.s{{font-weight:600;margin-top:6px}}.f{{color:#a33;font-size:12px;max-width:420px}}</style>
<h1>Same prompt, different models</h1><p>Run {outdir.name}. Country: {COUNTRY}. Click a screenshot to open the app.</p>
<table><tr><th></th>{head}</tr>{''.join(rows)}</table>""", encoding="utf-8")
    print("report:", outdir / "report.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(DEFAULT_MODELS))
    ap.add_argument("--prompts", default="")
    ap.add_argument("--rescore", type=Path)
    ap.add_argument("--reasoning", choices=["minimal", "low", "medium", "high"])
    a = ap.parse_args()
    global REASONING
    REASONING = a.reasoning
    if a.rescore:
        asyncio.run(rescore(a.rescore))
        return
    outdir = OUT / (datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + (f"-reasoning-{a.reasoning}" if a.reasoning else ""))
    outdir.mkdir(parents=True, exist_ok=True)
    asyncio.run(run([m.strip() for m in a.models.split(",")], set(filter(None, a.prompts.split(","))), outdir))


if __name__ == "__main__":
    main()
