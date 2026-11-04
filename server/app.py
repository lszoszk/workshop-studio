"""Workshop Studio API (VM Arrakis, container studio-api, 127.0.0.1:8011; nginx /studio-api/).

Implements docs/api-contract.md. The OpenRouter key stays here. The studio front (GitHub Pages)
sends a seat code, a menu model id, a purpose and the conversation; the server checks the seat, its
budget and its rate limit, adds the system message for the purpose, pins the model to its host with
Zero Data Retention and streams the answer back as normalised SSE:

    data: {"reasoning": "…"}    the model's thinking, as it arrives (before the answer)
    data: {"delta": "…"}        the answer text, as it arrives
    event: usage                tokens, cost, host, region, zdr, seconds, budget_left
    event: done
    event: error                only if the stream breaks after it started

Logs and the usage table hold seat, model, purpose, tokens, cost, seconds and status: never message
content and never an IP address (uvicorn runs with --no-access-log).

Endpoints (under /studio-api):
  GET  /health            route status for the front's 3-second probe
  GET  /seat/{code}       country and budget of a seat
  POST /chat              {seat, model, purpose, messages} → text/event-stream
  POST /gallery           {seat, title, model, prompt_id, html} → put a participant's page on the wall
  GET  /gallery           the list for the wall;  GET /gallery/{id} → the page itself
  GET  /admin?key=        facilitator page; POST /admin does the actions (not part of the contract)

Configuration: environment variables, see Config below and RUNBOOK.md.
Run: uvicorn --factory app:create_app --port 8011 --no-access-log   (from server/)
"""
import asyncio
import datetime as dt
import hmac
import html as htmlmod
import json
import logging
import os
import re
import secrets
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

import models
from seats import Seats, normalise

VERSION = "2026-11-01"
HERE = Path(__file__).resolve().parent
OPENROUTER = "https://openrouter.ai/api/v1"
ORIGINS = "https://lszoszk.github.io,http://localhost:8766,http://127.0.0.1:8766"
GALLERY_LINK_HOSTS = ("docs.un.org", "undocs.org", "uhri.ohchr.org", "searchlibrary.ohchr.org")
GALLERY_MAX_BYTES = 300_000
GALLERY_PER_SEAT = 20
MAX_BODY_BYTES = 1_000_000
MAX_MESSAGES = 40
MAX_CHARS = 300_000          # whole conversation; earlier versions of the page travel back with it
KEEPALIVE_S = 10             # a silent upstream gets an SSE comment, so nginx and the browser stay awake
BUSY = "in_flight_budget_exhausted"   # OpenRouter 402 reason: transient, "retry after in-flight requests settle"
# purpose → (temperature, max_tokens); a question's budget holds a reasoning model's thinking (GLM-5.3 thinks
# for about 1,000 tokens before it answers) as well as the answer
PURPOSES = {"build": (0.3, 64000), "inapp": (0.2, 8000), "question": (0.8, 4000)}
INAPP_SYSTEM = ("You are called from inside a data app built in a workshop. Answer only what is asked. "
                "If JSON is requested, reply with JSON only, no prose and no code fences.")
PLACEHOLDER_BUILD = ("Return one complete HTML document in a single ```html code block. All data is in "
                     "window.WORKSHOP_DATA before your script runs; never use fetch() or load anything from the "
                     "internet. (The studio's system prompt, schema and samples were not found on the server.)")

log = logging.getLogger("studio")


def _home_env_key() -> str:
    """Locally the key lives in ~/.env, as for the other proxies on the laptop."""
    p = Path.home() / ".env"
    if not p.exists():
        return ""
    for line in p.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


@dataclass
class Config:
    api_key: str = field(default_factory=lambda: os.environ.get("OPENROUTER_API_KEY") or _home_env_key())
    admin_key: str = field(default_factory=lambda: os.environ.get("STUDIO_ADMIN_KEY", ""))
    state_dir: Path = field(default_factory=lambda: Path(os.environ.get("STUDIO_STATE_DIR", HERE / "state")))
    data_dir: Path = field(default_factory=lambda: Path(os.environ.get("STUDIO_DATA_DIR", HERE.parent / "site" / "data")))
    seats_csv: Path | None = field(default_factory=lambda: Path(p) if (p := os.environ.get("STUDIO_SEATS_CSV")) else None)
    seat_budget: float = field(default_factory=lambda: float(os.environ.get("STUDIO_SEAT_BUDGET", "8")))
    daily_budget: float = field(default_factory=lambda: float(os.environ.get("STUDIO_DAILY_BUDGET", "200")))
    # 60 requests per seat in 5 minutes: a page-by-page model step sends 18 at once (CCPR GC 32); the seat's
    # budget, not this limit, caps the cost
    rate_limit: int = field(default_factory=lambda: int(os.environ.get("STUDIO_RATE_LIMIT", "60")))
    rate_window: int = field(default_factory=lambda: int(os.environ.get("STUDIO_RATE_WINDOW", "300")))
    origins: list = field(default_factory=lambda: os.environ.get("STUDIO_ORIGINS", ORIGINS).split(","))
    build: str = field(default_factory=lambda: os.environ.get("STUDIO_BUILD", ""))
    busy_retry_s: float = field(default_factory=lambda: float(os.environ.get("STUDIO_BUSY_RETRY_S", "20")))


def build_system_prompt(data_dir: Path) -> str:
    """Exactly tools/bakeoff.py:system_prompt(): the text of site/data/system_prompt.md below the first
    `---` line, then schema.md, then the samples block from samples.json."""
    try:
        sp = (data_dir / "system_prompt.md").read_text(encoding="utf-8").split("\n---\n", 1)[1].strip()
        samples = json.loads((data_dir / "samples.json").read_text(encoding="utf-8"))
        schema = (data_dir / "schema.md").read_text(encoding="utf-8").strip()
    except (OSError, IndexError, ValueError):
        return PLACEHOLDER_BUILD
    return "\n\n".join([
        sp,
        schema,
        "## Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)\n\n```json\n"
        + json.dumps(samples, ensure_ascii=False, indent=1) + "\n```",
    ])


class Refusal(Exception):
    def __init__(self, status: int, message: str, code: str, headers: dict | None = None):
        self.status, self.message, self.code, self.headers = status, message, code, headers or {}


def refuse(e: Refusal) -> JSONResponse:
    return JSONResponse({"error": e.message, "code": e.code}, e.status, headers=e.headers)


def sse(event: str | None, obj: dict) -> str:
    head = f"event: {event}\n" if event else ""
    return f"{head}data: {json.dumps(obj, ensure_ascii=False)}\n\n"


def log_event(**fields) -> None:
    log.info(json.dumps(fields, ensure_ascii=False))


async def read_json(request: Request) -> dict:
    raw = await request.body()
    if len(raw) > MAX_BODY_BYTES:
        raise Refusal(413, "The request is too large", "too_large")
    try:
        d = json.loads(raw or b"{}")
    except ValueError:
        raise Refusal(400, "The request is not valid JSON", "bad_json")
    if not isinstance(d, dict):
        raise Refusal(400, "The request is not valid JSON", "bad_json")
    return d


def clean_messages(raw) -> list[dict]:
    if not isinstance(raw, list) or not all(isinstance(m, dict) for m in raw):
        raise Refusal(400, "messages must be a list of {role, content}", "bad_messages")
    if any(m.get("role") == "system" for m in raw):
        raise Refusal(400, "System messages are added by the server; do not send one", "system_message")
    if any(m.get("role") not in ("user", "assistant") or not isinstance(m.get("content"), str) for m in raw):
        raise Refusal(400, "Each message needs role user or assistant and text content", "bad_messages")
    msgs = [{"role": m["role"], "content": m["content"]} for m in raw][-MAX_MESSAGES:]
    if not msgs or msgs[-1]["role"] != "user" or not msgs[-1]["content"].strip():
        raise Refusal(400, "Write a message first", "no_message")
    if sum(len(m["content"]) for m in msgs) > MAX_CHARS:
        raise Refusal(400, "This conversation is too long. Start a new thread with an improved prompt", "too_long")
    return msgs


SCRIPT_SRC = re.compile(r"<script\b[^>]*?\ssrc\s*=", re.I)
URL_ATTR = re.compile(r"""[\s"'](?:src|href)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)


def page_violations(page: str) -> list[str]:
    """`<script src>` of any kind, and src/href pointing outside the UN document hosts."""
    bad = ["<script src>"] if SCRIPT_SRC.search(page) else []
    for a in URL_ATTR.finditer(page):
        url = next(g for g in a.groups() if g is not None).strip()
        low = url.lower()
        if low.startswith("//") or re.match(r"[a-z][a-z0-9+.-]*://", low):
            host = urlparse("https:" + url if low.startswith("//") else url).hostname or ""
            if host not in GALLERY_LINK_HOSTS:
                bad.append(url[:120])
    return bad


def create_app(cfg: Config | None = None, transport: httpx.AsyncBaseTransport | None = None) -> FastAPI:
    cfg = cfg or Config()
    if not log.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(message)s"))
        log.addHandler(h)
        log.setLevel(logging.INFO)
    seats = Seats(cfg.state_dir / "studio.sqlite3", cfg.seat_budget, cfg.daily_budget, cfg.rate_limit, cfg.rate_window)
    if cfg.seats_csv and cfg.seats_csv.exists():
        seats.import_csv(cfg.seats_csv, keep_existing=True)   # a restart never resets a top-up
    gallery_dir = cfg.state_dir / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)
    systems = {"build": build_system_prompt(cfg.data_dir), "inapp": INAPP_SYSTEM, "question": None}
    client = httpx.AsyncClient(transport=transport, timeout=httpx.Timeout(10.0, read=180.0),
                               limits=httpx.Limits(max_connections=100, max_keepalive_connections=20))
    balance = {"value": None, "at": 0.0, "task": None}

    @asynccontextmanager
    async def lifespan(_app):
        yield
        await client.aclose()

    app = FastAPI(title="Workshop Studio API", version=VERSION, lifespan=lifespan,
                  docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(CORSMiddleware, allow_origins=cfg.origins, allow_methods=["GET", "POST", "OPTIONS"],
                       allow_headers=["Content-Type"], max_age=600)
    app.state.cfg, app.state.seats, app.state.systems = cfg, seats, systems

    def paused() -> bool:
        return seats.setting("paused", "0") == "1"

    def default_model() -> str:
        k = seats.setting("default_model", models.DEFAULT)
        return k if k in models.MODELS else models.DEFAULT

    def seat_or_refuse(code) -> dict:
        s = seats.get(code)
        if not s or s["disabled"]:
            raise Refusal(403, "Unknown or disabled seat code", "seat")
        if paused():
            raise Refusal(503, "The studio is paused by the facilitator", "paused")
        return s

    def headers() -> dict:
        return {"Authorization": f"Bearer {cfg.api_key}", "HTTP-Referer": "https://lszoszk.github.io/workshop-studio/",
                "X-Title": "Workshop Studio"}

    async def open_upstream(m: models.Model, messages: list, purpose: str):
        temperature, max_tokens = PURPOSES[purpose]
        system = systems[purpose]
        payload = {"model": m.id, "stream": True, "usage": {"include": True}, "temperature": temperature,
                   "max_tokens": max_tokens, "provider": models.provider_block(m),
                   "messages": ([{"role": "system", "content": system}] if system else []) + messages}
        if purpose == "build" and m.reasoning:
            payload["reasoning"] = {"effort": m.reasoning}
        elif purpose == "question" and m.reasoning:   # a quick question: think briefly (GLM-5.3 otherwise thinks past its budget)
            payload["reasoning"] = {"effort": "low"}
        req = client.build_request("POST", f"{OPENROUTER}/chat/completions", json=payload, headers=headers())
        try:
            r = await client.send(req, stream=True)
        except httpx.HTTPError as e:
            return None, type(e).__name__
        if r.status_code == 402:      # a credits error never quotes the prompt: read the reason, never log the body
            try:
                reason = ((json.loads(await r.aread())["error"].get("metadata") or {}).get("reason"))
            except (ValueError, KeyError, TypeError, AttributeError, httpx.HTTPError):
                reason = None
            await r.aclose()
            return None, BUSY if reason == BUSY else "http_402"
        if r.status_code != 200:
            await r.aclose()          # other error bodies are not read: they may quote the prompt
            return None, f"http_{r.status_code}"
        return r, None

    async def open_with_retry(m: models.Model, messages: list, purpose: str):
        """open_upstream, retrying OpenRouter's transient in-flight budget 402 with backoff for up to
        cfg.busy_retry_s (30 people pressing Build at once on a low balance)."""
        deadline, delay = time.monotonic() + cfg.busy_retry_s, 0.5
        while True:
            resp, err = await open_upstream(m, messages, purpose)
            remaining = deadline - time.monotonic()
            if err != BUSY or remaining <= 0:
                return resp, err
            await asyncio.sleep(min(delay, remaining))
            delay = min(delay * 2, 5.0)

    async def relay(resp, used: models.Model, asked: models.Model, seat: dict, purpose: str, t0: float,
                    prompt_chars: int, first_error: str | None):
        usage, provider, out_chars, status, error = {}, None, 0, "ok", None
        last_write = time.monotonic()
        try:
            async for line in resp.aiter_lines():
                data = line[5:].strip() if line.startswith("data:") else None
                chunk = None
                if data and data != "[DONE]":
                    try:
                        chunk = json.loads(data)
                    except ValueError:
                        pass
                text = ""
                if isinstance(chunk, dict):
                    if chunk.get("error"):
                        status, error = "error", str((chunk["error"] or {}).get("code") or "stream_error")
                        yield sse("error", {"status": 502, "error": "The model provider stopped responding"})
                        last_write = time.monotonic()
                        break
                    if chunk.get("usage"):
                        usage = chunk["usage"]
                    provider = chunk.get("provider") or provider
                    deltas = [ch.get("delta") or {} for ch in chunk.get("choices") or []]
                    thought = "".join(d.get("reasoning") or "" for d in deltas)
                    text = "".join(d.get("content") or "" for d in deltas)
                    if thought:       # billed as completion tokens too, so it counts towards an estimate
                        out_chars += len(thought)
                        yield sse(None, {"reasoning": thought})
                        last_write = time.monotonic()
                if text:
                    out_chars += len(text)
                    yield sse(None, {"delta": text})
                    last_write = time.monotonic()
                elif time.monotonic() - last_write > KEEPALIVE_S:
                    yield ": keep-alive\n\n"
                    last_write = time.monotonic()
        except httpx.HTTPError as e:
            status, error = "error", type(e).__name__
            yield sse("error", {"status": 502, "error": "The model provider stopped responding"})
        except asyncio.CancelledError:
            status, error = "aborted", "client_closed"
            raise
        finally:
            await resp.aclose()
            pt, ct = int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)
            estimated = "cost" not in usage
            if estimated:     # the stream ended before the usage chunk: charge an estimate, never zero
                pt, ct = pt or prompt_chars // 4, ct or out_chars // 4
                cost = models.estimate_cost(used, pt, ct)
            else:
                cost = float(usage["cost"] or 0)
            seconds = round(time.monotonic() - t0, 1)
            seats.record(seat["code"], model=used.key, host=used.host or provider or "", purpose=purpose,
                         prompt_tokens=pt, completion_tokens=ct, cost=cost, estimated=estimated,
                         latency_ms=int(seconds * 1000), status=status, error=error)
            log_event(event="chat", seat=seat["code"], model=used.key, purpose=purpose,
                      fallback_from=asked.key if used is not asked else None, first_error=first_error,
                      prompt_tokens=pt, completion_tokens=ct, cost=round(cost, 6), estimated=estimated,
                      seconds=seconds, status=status, error=error)
        if status != "aborted":
            u = {"model": used.key, "model_label": used.label, "openrouter_model": used.id,
                 "host": used.host_label if used.host else (provider or used.host_label),
                 "host_region": used.host_region, "zdr": True, "prompt_tokens": pt, "completion_tokens": ct,
                 "cost": round(cost, 6), "seconds": seconds,
                 "budget_left": round(max(0.0, seat["budget"] - seat["spent"] - cost), 4)}
            if estimated:
                u["estimated"] = True
            if used is not asked:
                u["fallback_from"] = asked.key
            yield sse("usage", u)
            yield sse("done", {})

    @app.post("/studio-api/chat")
    async def chat(request: Request):
        try:
            d = await read_json(request)
            seat = seat_or_refuse(d.get("seat"))
            purpose = d.get("purpose") or "build"
            if purpose not in PURPOSES:
                raise Refusal(400, 'purpose must be "build", "inapp" or "question"', "purpose")
            m = models.MODELS.get(d.get("model") or default_model())
            if not m:
                raise Refusal(400, "This model is not on the menu", "model")
            messages = clean_messages(d.get("messages"))
            if seat["spent"] >= seat["budget"]:
                raise Refusal(429, "This seat has used its budget", "seat_budget")
            if seats.spent_today() >= cfg.daily_budget:
                raise Refusal(429, "The studio has reached today's spending limit", "daily_budget")
            wait = seats.hit(seat["code"])
            if wait:
                raise Refusal(429, "Too many requests from this seat, wait a minute", "rate_limit",
                              {"Retry-After": str(wait)})
        except Refusal as e:
            return refuse(e)

        t0 = time.monotonic()
        used, (resp, err) = m, await open_with_retry(m, messages, purpose)
        first_error = err
        if resp is None and m.fallback and err != BUSY:    # a busy account is busy for every model: no fallback
            used = models.MODELS[m.fallback]
            resp, err = await open_with_retry(used, messages, purpose)
        if resp is None:
            seconds = round(time.monotonic() - t0, 1)
            status = "busy" if err == BUSY else "error"
            seats.record(seat["code"], model=used.key, host=used.host or "", purpose=purpose,
                         latency_ms=int(seconds * 1000), status=status, error=err)
            log_event(event="chat", seat=seat["code"], model=used.key, purpose=purpose, first_error=first_error,
                      seconds=seconds, status=status, error=err)
            if status == "busy":
                return JSONResponse({"error": "The model service is busy, try again in a minute", "code": "busy"}, 503,
                                    headers={"Retry-After": "60"})
            return JSONResponse({"error": "The model provider did not respond", "code": "upstream"}, 502)
        prompt_chars = len(systems[purpose] or "") + sum(len(x["content"]) for x in messages)
        return StreamingResponse(relay(resp, used, m, seat, purpose, t0, prompt_chars, first_error),
                                 media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    @app.get("/studio-api/seat/{code}")
    async def seat_info(code: str):
        s = seats.get(code)
        if not s:
            return refuse(Refusal(404, "Unknown seat code", "seat"))
        return {"seat": s["code"], "country": s["country"], "budget_total": s["budget"],
                "budget_left": round(max(0.0, s["budget"] - s["spent"]), 4), "disabled": bool(s["disabled"])}

    # ── gallery (the wall) ──
    def gallery_items() -> list[dict]:
        items = []
        for p in gallery_dir.glob("*.json"):
            try:
                items.append(json.loads(p.read_text()))
            except (OSError, ValueError):
                continue
        return sorted(items, key=lambda i: i["created"], reverse=True)

    @app.post("/studio-api/gallery")
    async def gallery_post(request: Request):
        try:
            d = await read_json(request)
            seat = seat_or_refuse(d.get("seat"))
            page = d.get("html")
            if not isinstance(page, str) or not page.strip():
                raise Refusal(400, "There is no page to send", "no_html")
            if len(page.encode("utf-8")) > GALLERY_MAX_BYTES:
                raise Refusal(413, f"The page is larger than {GALLERY_MAX_BYTES // 1000} kB", "too_large")
            bad = page_violations(page)
            if bad:
                raise Refusal(400, "The page loads something from outside: " + ", ".join(bad[:5])
                              + ". Only links to " + ", ".join(GALLERY_LINK_HOSTS) + " are allowed", "external")
            if sum(1 for i in gallery_items() if i.get("seat") == seat["code"]) >= GALLERY_PER_SEAT:
                raise Refusal(429, f"This seat has already sent {GALLERY_PER_SEAT} pages to the wall", "gallery_full")
        except Refusal as e:
            return refuse(e)
        gid = dt.datetime.now().strftime("%H%M%S") + "-" + secrets.token_hex(4)
        # the country the app ran on (a participant may pick another than the seat's) and the files it was
        # given in the chat, so the wall can run it on the same data
        country = d.get("country")
        country = country.strip() if isinstance(country, str) and re.fullmatch(r"[^\W\d_][\w .,'()\-]{0,59}", country.strip()) else seat["country"]
        files = [f for f in (d.get("files") or []) if isinstance(f, str) and re.fullmatch(r"[a-z0-9_]{1,30}", f)][:10] \
            if isinstance(d.get("files"), list) else []
        meta = {"id": gid, "seat": seat["code"], "country": country, "files": files,
                "title": str(d.get("title") or "Untitled").strip()[:120],
                "model": d.get("model") if d.get("model") in models.MODELS else None,
                "prompt_id": str(d.get("prompt_id") or "")[:60] or None,
                "created": dt.datetime.now().isoformat(timespec="seconds")}
        (gallery_dir / f"{gid}.html").write_text(page, encoding="utf-8")
        (gallery_dir / f"{gid}.json").write_text(json.dumps(meta, ensure_ascii=False))
        log_event(event="gallery", seat=seat["code"], id=gid, bytes=len(page.encode("utf-8")))
        return {"ok": True, "id": gid}

    @app.get("/studio-api/gallery")
    async def gallery_list():
        keep = ("id", "seat", "country", "title", "model", "prompt_id", "files", "created")
        return [{k: i.get(k) for k in keep} for i in gallery_items()]

    @app.get("/studio-api/gallery/{gid}")
    async def gallery_page(gid: str):
        p = gallery_dir / f"{gid}.html"
        if not re.fullmatch(r"[0-9]{6}-[0-9a-f]{8}", gid) or not p.exists():
            return refuse(Refusal(404, "No such page on the wall", "not_found"))
        # sandbox = an opaque origin, so a participant's page opened here can never act as this API's origin
        return HTMLResponse(p.read_text(encoding="utf-8"), headers={
            "Content-Security-Policy": "sandbox allow-scripts", "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-store"})

    # ── health ──
    async def refresh_balance():
        try:
            r = await client.get(f"{OPENROUTER}/credits", headers=headers(), timeout=5.0)
            c = r.json()["data"]
            balance["value"] = round(float(c["total_credits"]) - float(c["total_usage"]), 2)
        except Exception:      # noqa: BLE001 — health must answer even when OpenRouter does not
            balance["value"] = None
        balance["at"] = time.monotonic()

    @app.get("/studio-api/health")
    async def health():
        # The front probes with a 3 s timeout: a slow OpenRouter costs at most 1.5 s once a minute,
        # and the refresh then finishes in the background.
        if time.monotonic() - balance["at"] > 60 and (balance["task"] is None or balance["task"].done()):
            balance["task"] = asyncio.create_task(refresh_balance())
        if balance["task"] is not None and not balance["task"].done():
            try:
                await asyncio.wait_for(asyncio.shield(balance["task"]), 1.5)
            except asyncio.TimeoutError:
                pass
        all_seats = seats.all()
        return {"ok": True, "version": VERSION, "route": "vm", "default_model": default_model(),
                "models": list(models.MODELS), "accepting": not paused(),
                # beyond the contract, for the facilitator:
                "build": cfg.build, "balance_usd": balance["value"], "key_configured": bool(cfg.api_key),
                "seats": {"total": len(all_seats), "enabled": sum(1 for s in all_seats if not s["disabled"]),
                          "active_10min": seats.active_count(10)}}

    # ── admin ──
    def admin_ok(key: str | None) -> bool:
        return bool(cfg.admin_key) and hmac.compare_digest((key or "").encode(), cfg.admin_key.encode())

    def admin_state() -> dict:
        return {"paused": paused(), "default_model": default_model(), "spent_today": round(seats.spent_today(), 4),
                "daily_budget": cfg.daily_budget, "balance_usd": balance["value"], "seats": seats.all(),
                "gallery": gallery_items()}

    def admin_page(key: str, note: str = "") -> HTMLResponse:
        s, e = admin_state(), htmlmod.escape
        k = e(key)

        def form(action: str, label: str, extra: str = "", fields: str = "") -> str:
            return (f'<form method="post" action="/studio-api/admin"><input type="hidden" name="key" value="{k}">'
                    f'<input type="hidden" name="action" value="{action}">{extra}{fields}<button>{label}</button></form>')

        rows = "".join(
            f"<tr class='{'off' if r['disabled'] else ''}'><td><code>{e(r['code'])}</code></td><td>{e(r['label'])}</td><td>{e(r['country'])}</td>"
            f"<td>${r['spent']:.2f} / ${r['budget']:.2f}</td><td>{r['requests']}</td><td>{r['errors']}</td>"
            f"<td>{e(r['last_request'] or '')}</td><td>{e(r['last_error'] or '')}</td><td>"
            + form("enable" if r["disabled"] else "disable", "Enable" if r["disabled"] else "Disable",
                   f'<input type="hidden" name="seat" value="{e(r["code"])}">')
            + form("budget", "Set budget", f'<input type="hidden" name="seat" value="{e(r["code"])}">',
                   f'<input name="value" size="4" value="{r["budget"]:g}">')
            + "</td></tr>" for r in s["seats"])
        opts = "".join(f'<option value="{m.key}"{" selected" if m.key == s["default_model"] else ""}>{e(m.label)}</option>'
                       for m in models.MODELS.values())
        wall = "".join(f"<li>{e(g['created'])} · {e(g['country'])} · {e(g['title'])} "
                       + form("remove_gallery", "Remove", f'<input type="hidden" name="value" value="{e(g["id"])}">')
                       + "</li>" for g in s["gallery"]) or "<li>empty</li>"
        bal = "unknown" if s["balance_usd"] is None else f"${s['balance_usd']:.2f}"
        body = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Studio admin</title><style>body{{font:14px system-ui;margin:16px}}table{{border-collapse:collapse}}
td,th{{border-bottom:1px solid #ddd;padding:4px 8px;text-align:left}}form{{display:inline}}tr.off{{opacity:.5}}
.bar{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin:12px 0}}.paused{{color:#b00;font-weight:600}}</style>
<h1>Workshop Studio · admin</h1>{f"<p><b>{e(note)}</b></p>" if note else ""}
<div class="bar"><span class="{'paused' if s['paused'] else ''}">{'PAUSED: every seat is refused' if s['paused'] else 'Running'}</span>
{form('resume' if s['paused'] else 'pause', 'Resume all seats' if s['paused'] else 'Kill switch: pause all seats')}
<span>Spent today ${s['spent_today']:.2f} / ${s['daily_budget']:.0f} · OpenRouter balance {bal} · times in UTC</span>
{form('default_model', 'Set default model', fields=f'<select name="value">{opts}</select>')}</div>
<table><tr><th>Seat</th><th>Label</th><th>Country</th><th>Spent / budget</th><th>Req</th><th>Err</th><th>Last request</th>
<th>Last error</th><th></th></tr>{rows}</table><h2>Wall</h2><ul>{wall}</ul>"""
        return HTMLResponse(body, headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    @app.get("/studio-api/admin")
    async def admin_get(key: str = "", format: str = "html"):
        if not admin_ok(key):
            return refuse(Refusal(403, "Wrong admin key", "admin"))
        return admin_state() if format == "json" else admin_page(key)

    @app.post("/studio-api/admin")
    async def admin_post(request: Request):
        raw = await request.body()
        wants_json = request.headers.get("content-type", "").startswith("application/json")
        if wants_json:
            try:
                f = json.loads(raw or b"{}")
            except ValueError:
                f = {}
        else:
            f = {k: v[0] for k, v in parse_qs(raw.decode("utf-8", "replace")).items()}
        key = str(f.get("key", ""))
        if not admin_ok(key):
            return refuse(Refusal(403, "Wrong admin key", "admin"))
        action, seat, value = f.get("action"), normalise(f.get("seat", "")), str(f.get("value", ""))
        ok = True
        if action in ("disable", "enable"):
            ok = seats.set_disabled(seat, action == "disable")
        elif action == "budget":
            try:
                ok = seats.set_budget(seat, float(value))
            except ValueError:
                ok = False
        elif action in ("pause", "resume"):
            seats.set_setting("paused", "1" if action == "pause" else "0")
        elif action == "default_model":
            ok = value in models.MODELS
            if ok:
                seats.set_setting("default_model", value)
        elif action == "remove_gallery":
            ok = bool(re.fullmatch(r"[0-9]{6}-[0-9a-f]{8}", value)) and (gallery_dir / f"{value}.json").exists()
            if ok:
                for ext in ("json", "html"):
                    (gallery_dir / f"{value}.{ext}").unlink(missing_ok=True)
        else:
            ok = False
        log_event(event="admin", action=action, seat=seat or None, ok=ok)
        if wants_json:
            return JSONResponse({"ok": ok} | admin_state(), 200 if ok else 400)
        return admin_page(key, f"{action}: {'done' if ok else 'nothing changed'}")

    return app
