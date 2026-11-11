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

import anthropic
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse

import models
from seats import Seats, normalise

VERSION = "2026-11-01"
HERE = Path(__file__).resolve().parent
OPENROUTER = "https://openrouter.ai/api/v1"
ORIGINS = "https://lszoszk.github.io,http://localhost:8766,http://127.0.0.1:8766"
GALLERY_LINK_HOSTS = ("docs.un.org", "undocs.org", "uhri.ohchr.org", "searchlibrary.ohchr.org")
GALLERY_MAX_BYTES = 300_000
GALLERY_PER_SEAT = 20
FEEDBACK_MAX_CHARS = 3000
FEEDBACK_MAX_ITEMS = 2000
MAX_BODY_BYTES = 1_000_000
MAX_CHAT_BYTES = 8_000_000   # a conversation plus up to three screenshots (nginx: client_max_body_size 8m)
# activity events (POST /studio-api/events): the names the front sends; see track() in site/studio.js
EVENT_NAMES = {"open", "session", "pick", "plan_open", "plan_build", "build", "build_fail", "app_error", "repair",
               "query", "look", "gallery_in", "own_file", "own_samples", "picture", "model", "save", "wall", "kit",
               "advanced"}
EVENT_FIELD = re.compile(r"[a-z_]{1,20}")
EVENT_VALUE = re.compile(r"[A-Za-z0-9_.:/+\-]{0,60}")   # ids and codes: no spaces, so no sentence fits
MAX_EVENTS_PER_POST = 100
EVENTS_PER_SESSION_DAY = 3000
MAX_MESSAGES = 40
MAX_CHARS = 300_000          # whole conversation; earlier versions of the page travel back with it
MAX_IMAGES = 3               # a participant's screenshots, on the last message only
MAX_IMAGE_CHARS = 2_000_000  # base64 of one image (about 1.5 MB); the studio sends them scaled down
IMAGE_TYPES = ("image/png", "image/jpeg", "image/webp", "image/gif")
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


def _home_env_key(name: str = "OPENROUTER_API_KEY") -> str:
    """Locally the keys live in ~/.env, as for the other proxies on the laptop."""
    p = Path.home() / ".env"
    if not p.exists():
        return ""
    for line in p.read_text().splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


class AnthropicLines:
    """An Anthropic message stream, read as the OpenRouter stream relay() already reads: `data:` lines with
    reasoning and content deltas, then one usage chunk with the cost, or an error chunk."""

    def __init__(self, manager, stream, model: models.Model):
        self.manager, self.stream, self.model = manager, stream, model

    async def aiter_lines(self):
        def line(d: dict) -> str:
            return "data: " + json.dumps(d)
        try:
            async for event in self.stream:
                if event.type == "content_block_delta":
                    if event.delta.type == "thinking_delta" and event.delta.thinking:
                        yield line({"choices": [{"delta": {"reasoning": event.delta.thinking}}]})
                    elif event.delta.type == "text_delta" and event.delta.text:
                        yield line({"choices": [{"delta": {"content": event.delta.text}}]})
            u = (await self.stream.get_final_message()).usage
            fresh, ct = int(u.input_tokens or 0), int(u.output_tokens or 0)
            write = int(getattr(u, "cache_creation_input_tokens", 0) or 0)
            read = int(getattr(u, "cache_read_input_tokens", 0) or 0)
            yield line({"usage": {"prompt_tokens": fresh + write + read, "completion_tokens": ct, "cached_tokens": read,
                                  "cost": models.estimate_cost(self.model, fresh, ct, write, read)}})
        except anthropic.APIError as e:   # the message is not logged: it may quote the prompt
            yield line({"error": {"code": f"anthropic_{getattr(e, 'status_code', None) or type(e).__name__}"}})

    async def aclose(self):
        await self.manager.__aexit__(None, None, None)


@dataclass
class Config:
    api_key: str = field(default_factory=lambda: os.environ.get("OPENROUTER_API_KEY") or _home_env_key())
    anthropic_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY") or _home_env_key("ANTHROPIC_API_KEY"))
    # dollars the server may spend on Anthropic's API in all; past it, Claude's requests go to its fallback
    anthropic_cap: float = field(default_factory=lambda: float(os.environ.get("STUDIO_ANTHROPIC_CAP", "15")))
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


def is_change(messages: list) -> bool:
    """A build request that follows an answer of the model's: a change to an app it already wrote (edit mode)."""
    return any(x.get("role") == "assistant" for x in messages)


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


async def read_json(request: Request, limit: int = MAX_BODY_BYTES) -> dict:
    raw = await request.body()
    if len(raw) > limit:
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
    # screenshots: on the message being sent only, never on an earlier one; their bytes are never logged
    if any(m.get("images") for m in raw[:-1]):
        raise Refusal(400, "Only the last message may carry images", "bad_images")
    images = raw[-1].get("images") or []
    if images:
        if not isinstance(images, list) or len(images) > MAX_IMAGES or not all(
                isinstance(i, dict) and i.get("media_type") in IMAGE_TYPES and isinstance(i.get("data"), str)
                and 0 < len(i["data"]) <= MAX_IMAGE_CHARS and re.fullmatch(r"[A-Za-z0-9+/=]+", i["data"]) for i in images):
            raise Refusal(400, f"Up to {MAX_IMAGES} images (PNG, JPEG, WebP or GIF, about 1.5 MB each) can go with a message", "bad_images")
        msgs[-1]["images"] = [{"media_type": i["media_type"], "data": i["data"]} for i in images]
    return msgs


def with_images(messages: list, api: str) -> list:
    """The messages as the upstream API takes them: a message with images becomes a list of content parts
    (Anthropic: the images first, then the text; OpenRouter: the text, then each image as a data URL)."""
    out = []
    for m in messages:
        imgs = m.get("images")
        if not imgs:
            out.append({"role": m["role"], "content": m["content"]})
        elif api == "anthropic":
            out.append({"role": m["role"], "content": [{"type": "image", "source": {"type": "base64", "media_type": i["media_type"],
                        "data": i["data"]}} for i in imgs] + [{"type": "text", "text": m["content"]}]})
        else:
            out.append({"role": m["role"], "content": [{"type": "text", "text": m["content"]}] + [{"type": "image_url",
                        "image_url": {"url": f"data:{i['media_type']};base64,{i['data']}"}} for i in imgs]})
    return out


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
    feedback_dir = cfg.state_dir / "feedback"
    feedback_dir.mkdir(parents=True, exist_ok=True)
    systems = {"build": build_system_prompt(cfg.data_dir), "inapp": INAPP_SYSTEM, "question": None}
    client = httpx.AsyncClient(transport=transport, timeout=httpx.Timeout(10.0, read=180.0),
                               limits=httpx.Limits(max_connections=100, max_keepalive_connections=20))
    # no retries here: a failure goes to the model's fallback at once, as on OpenRouter
    claude = anthropic.AsyncAnthropic(api_key=cfg.anthropic_key or "missing", max_retries=0,
                                      http_client=httpx.AsyncClient(transport=transport, timeout=httpx.Timeout(10.0, read=180.0)))
    balance = {"value": None, "at": 0.0, "task": None}

    @asynccontextmanager
    async def lifespan(_app):
        yield
        await client.aclose()
        await claude.close()

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

    async def open_anthropic(m: models.Model, messages: list, purpose: str):
        if not cfg.anthropic_key:
            return None, "no_anthropic_key"
        if seats.spent_on(m.key, "anthropic") >= cfg.anthropic_cap:
            return None, "anthropic_cap"
        _, max_tokens = PURPOSES[purpose]   # Sonnet 5.5 takes no temperature: only its default is accepted
        effort = "low" if purpose != "build" else (m.edit_reasoning or m.reasoning or "high") if is_change(messages) \
            else (m.reasoning or "high")
        # prompt caching: the studio's instructions, and the conversation up to the last answer (in edit mode the
        # whole app), are the same prefix on the next request; reading them back costs a tenth of the input price
        msgs = with_images(messages, "anthropic")
        last_answer = max((i for i, x in enumerate(msgs) if x["role"] == "assistant"), default=None)
        if last_answer is not None:
            msgs[last_answer]["content"] = [{"type": "text", "text": msgs[last_answer]["content"], "cache_control": {"type": "ephemeral"}}]
        params = {"model": m.id, "max_tokens": max_tokens, "messages": msgs,
                  "thinking": {"type": "adaptive", "display": "summarized"}, "output_config": {"effort": effort}}
        if systems[purpose]:
            params["system"] = [{"type": "text", "text": systems[purpose], "cache_control": {"type": "ephemeral"}}]
        manager = claude.messages.stream(**params)
        try:
            stream = await manager.__aenter__()
        except anthropic.APIStatusError as e:   # the body is not read: it may quote the prompt
            return None, f"http_{e.status_code}"
        except anthropic.APIError as e:
            return None, type(e).__name__
        return AnthropicLines(manager, stream, m), None

    async def open_upstream(m: models.Model, messages: list, purpose: str):
        if m.api == "anthropic":
            return await open_anthropic(m, messages, purpose)
        temperature, max_tokens = PURPOSES[purpose]
        system = systems[purpose]
        payload = {"model": m.id, "stream": True, "usage": {"include": True}, "temperature": temperature,
                   "max_tokens": max_tokens, "provider": models.provider_block(m),
                   "messages": ([{"role": "system", "content": system}] if system else []) + with_images(messages, "openrouter")}
        if purpose == "build" and is_change(messages) and m.edit_reasoning:
            payload["reasoning"] = {"effort": m.edit_reasoning}   # a change to an app already built
        elif purpose == "build" and m.reasoning:
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
                 "host_region": used.host_region, "zdr": used.zdr, "prompt_tokens": pt, "completion_tokens": ct,
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
            d = await read_json(request, MAX_CHAT_BYTES)
            seat = seat_or_refuse(d.get("seat"))
            purpose = d.get("purpose") or "build"
            if purpose not in PURPOSES:
                raise Refusal(400, 'purpose must be "build", "inapp" or "question"', "purpose")
            m = models.MODELS.get(d.get("model") or default_model())
            if not m:
                raise Refusal(400, "This model is not on the menu", "model")
            messages = clean_messages(d.get("messages"))
            if messages[-1].get("images") and not m.vision:
                raise Refusal(400, f"{m.label} cannot read images. Switch to a model that can, or send the message without them", "no_vision")
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
        # a busy account is busy for every model; a fallback that cannot read the images would answer without them
        if resp is None and m.fallback and err != BUSY and (models.MODELS[m.fallback].vision or not messages[-1].get("images")):
            used = models.MODELS[m.fallback]
            resp, err = await open_with_retry(used, messages, purpose)
        if resp is None:
            seconds = round(time.monotonic() - t0, 1)
            status = "busy" if err == BUSY else "credit" if err == "http_402" else "error"
            seats.record(seat["code"], model=used.key, host=used.host or "", purpose=purpose,
                         latency_ms=int(seconds * 1000), status=status, error=err)
            log_event(event="chat", seat=seat["code"], model=used.key, purpose=purpose, first_error=first_error,
                      seconds=seconds, status=status, error=err)
            if status == "busy":
                return JSONResponse({"error": "The model service is busy, try again in a minute", "code": "busy"}, 503,
                                    headers={"Retry-After": "60"})
            if status == "credit":   # both models refused for lack of credit: say so, so the facilitator can top up
                return JSONResponse({"error": "The studio's account with the model service has run out of credit. Tell the "
                                              "facilitator; your apps and the recorded answers still work.", "code": "credit"}, 503)
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

    # ── feedback from testers: text and the page's own context, never data or an app's code ──
    def feedback_items() -> list[dict]:
        items = []
        for p in feedback_dir.glob("*.json"):
            try:
                items.append(json.loads(p.read_text()))
            except (OSError, ValueError):
                continue
        return sorted(items, key=lambda i: i["created"], reverse=True)

    # ── activity, to calibrate the studio before the workshop: what was done, how long it took and what failed;
    # never a message, a file, an app or a value from the data. Names and fields are a whitelist; a string is an id
    # or a code (60 characters at most, no free text), so a stray value cannot carry a sentence. One file a day. ──
    events_dir = cfg.state_dir / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    events_today = {"day": "", "n": {}}

    def clean_event(e) -> dict | None:
        if not isinstance(e, dict) or e.get("t") not in EVENT_NAMES:
            return None
        out = {"t": e["t"], "ms": int(e["ms"]) if isinstance(e.get("ms"), (int, float)) and 0 <= e["ms"] < 1e9 else None}
        for k, v in list(e.items())[:16]:
            if k in ("t", "ms") or not EVENT_FIELD.fullmatch(str(k)):
                continue
            if v is None or isinstance(v, bool):
                out[k] = v
            elif isinstance(v, (int, float)) and abs(v) < 1e9:
                out[k] = round(v, 3)
            elif isinstance(v, str) and EVENT_VALUE.fullmatch(v):
                out[k] = v
        return out

    @app.post("/studio-api/events")
    async def events_post(request: Request):
        try:
            d = await read_json(request)
            sid = str(d.get("sid") or "")
            if not re.fullmatch(r"[0-9a-f]{8,16}", sid) or not isinstance(d.get("events"), list):
                raise Refusal(400, "events must come with a session id", "bad_events")
        except Refusal as e:
            return refuse(e)
        seat = seats.get(d.get("seat")) if d.get("seat") else None   # a recorded-mode visitor has no seat
        day = dt.date.today().isoformat()
        if events_today["day"] != day:
            events_today.update(day=day, n={})
        room = EVENTS_PER_SESSION_DAY - events_today["n"].get(sid, 0)
        kept = [x for x in (clean_event(e) for e in d["events"][:MAX_EVENTS_PER_POST]) if x][:max(0, room)]
        if kept:
            events_today["n"][sid] = events_today["n"].get(sid, 0) + len(kept)
            at = dt.datetime.now().isoformat(timespec="seconds")
            head = {"at": at, "seat": seat["code"] if seat else None, "sid": sid,
                    "v": str(d.get("v") or "")[:20] if EVENT_VALUE.fullmatch(str(d.get("v") or "")) else None}
            with (events_dir / f"{day}.jsonl").open("a", encoding="utf-8") as fh:
                for x in kept:
                    fh.write(json.dumps({**head, **x}, ensure_ascii=False) + "\n")
        return {"ok": True, "kept": len(kept)}

    @app.post("/studio-api/feedback")
    async def feedback_post(request: Request):
        try:
            d = await read_json(request)
            text = d.get("text")
            if not isinstance(text, str) or not text.strip():
                raise Refusal(400, "There is nothing to send", "no_text")
            if len(list(feedback_dir.glob("*.json"))) >= FEEDBACK_MAX_ITEMS:
                raise Refusal(429, "The feedback box is full; tell the facilitator in person", "feedback_full")
            seat = seats.get(d.get("seat")) if d.get("seat") else None   # a recorded-mode visitor has no seat
            ctx = d.get("context") if isinstance(d.get("context"), dict) else {}
            ctx = {str(k)[:40]: str(v)[:300] for k, v in list(ctx.items())[:12]}
        except Refusal as e:
            return refuse(e)
        fid = dt.datetime.now().strftime("%m%d-%H%M%S") + "-" + secrets.token_hex(3)
        item = {"id": fid, "seat": seat["code"] if seat else None, "label": seat.get("label") if seat else None,
                "text": text.strip()[:FEEDBACK_MAX_CHARS], "context": ctx,
                "created": dt.datetime.now().isoformat(timespec="seconds")}
        (feedback_dir / f"{fid}.json").write_text(json.dumps(item, ensure_ascii=False))
        log_event(event="feedback", seat=item["seat"], id=fid, chars=len(item["text"]))
        return {"ok": True, "id": fid}

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
                "gallery": gallery_items(), "feedback": feedback_items()[:200]}

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
        fb = "".join(f"<li><b>{e(f['created'])}</b> · {e(f.get('label') or f.get('seat') or 'no seat')} · "
                     f"{e(f['context'].get('app', ''))}<br>{e(f['text'])}<br><small>{e(' · '.join('%s: %s' % kv for kv in f['context'].items()))}</small></li>"
                     for f in s["feedback"]) or "<li>none yet</li>"
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
<th>Last error</th><th></th></tr>{rows}</table><h2>Feedback ({len(s["feedback"])})</h2><ul>{fb}</ul><h2>Wall</h2><ul>{wall}</ul>"""
        return HTMLResponse(body, headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    @app.get("/studio-api/admin/events")
    async def admin_events(key: str = "", day: str = ""):
        """The activity of one day (default today) as JSON lines, for tools/events_report.py."""
        if not admin_ok(key):
            return refuse(Refusal(403, "Wrong admin key", "admin"))
        day = day if re.fullmatch(r"\d{4}-\d{2}-\d{2}", day) else dt.date.today().isoformat()
        p = events_dir / f"{day}.jsonl"
        return Response(p.read_text(encoding="utf-8") if p.exists() else "", media_type="application/x-ndjson",
                        headers={"Cache-Control": "no-store"})

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
