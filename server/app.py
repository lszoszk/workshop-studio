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
  GET  /gallery           the list for the wall (?course= keeps one course's);  GET /gallery/{id} → the page itself
  GET  /room?course=      the facilitator's messages to the room;  POST /room {course, text, seat, sid} → a
                          participant's message to the facilitator (kept in state/room/ until cleared)
  GET  /teaser            the teaser video (state/teaser/latest.mp4), with byte ranges
  GET  /admin?key=        facilitator page; POST /admin does the actions (not part of the contract)
  GET  /admin/room?key=&course=   the facilitator's live room chat (JSON: /admin/room.json; POST /admin/room)

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
import unicodedata
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import anthropic
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response, StreamingResponse

import models
from seats import Seats, normalise

VERSION = "2026-11-01"
HERE = Path(__file__).resolve().parent
ROOM_PAGE = (HERE / "room_page.html").read_text(encoding="utf-8")   # the facilitator's live room chat
OPENROUTER = "https://openrouter.ai/api/v1"
ANTHROPIC_MODELS = "https://api.anthropic.com/v1/models"   # the free call that checks a pasted Claude key
KEY_KINDS = {"openrouter": ("sk-or-", "OpenRouter"), "anthropic": ("sk-ant-", "Claude (Anthropic)")}   # prefix, name
ORIGINS = "https://lszoszk.github.io,http://localhost:8766,http://127.0.0.1:8766"
GALLERY_LINK_HOSTS = ("docs.un.org", "undocs.org", "uhri.ohchr.org", "searchlibrary.ohchr.org",
                      "www.gov.pl", "gov.pl")   # gov.pl: the GAAR Council PDFs (Poznan, 19.11.2026)
GALLERY_MAX_BYTES = 300_000
GALLERY_PER_SEAT = 20
FEEDBACK_MAX_CHARS = 3000
# the room chat: the facilitator writes to everyone in a course, a participant writes to the facilitator
ROOM_COURSE = re.compile(r"[a-z0-9-]{1,20}")
ROOM_MAX_CHARS = 1000
ROOM_MAX_ITEMS = 3000          # per course; past it, participants are told to speak to the facilitator
ROOM_SHOWN = 50                # the newest messages from the facilitator that a participant's page gets
ROOM_RATE = (8, 300)           # a participant (session or seat): 8 messages in 5 minutes
FEEDBACK_MAX_ITEMS = 2000
MAX_BODY_BYTES = 1_000_000
MAX_CHAT_BYTES = 8_000_000   # a conversation plus up to three screenshots (nginx: client_max_body_size 8m)
# activity events (POST /studio-api/events): the names the front sends; see track() in site/studio.js
EVENT_NAMES = {"open", "session", "pick", "plan_open", "plan_build", "build", "build_fail", "app_error", "repair",
               "query", "look", "gallery_in", "own_file", "own_samples", "picture", "model", "save", "wall", "kit",
               "advanced", "reset", "rescue", "ask_cached", "json_view", "route", "seat_ok", "seat_wrong", "seat_skip",
               "room_msg", "room_open", "room_sent", "progress", "progress_skip", "plan_edit", "plan_revise", "plan_look",
               "backup", "wall_dlg", "model_retry", "test_done", "ideas_shown", "idea_built", "phones",
               "studio_error", "wall_fail", "step_back"}
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
ANTHROPIC_BUSY = ("http_429", "http_529")   # Anthropic rate limit and "overloaded": gone within seconds, so worth a retry
WALL_NAME_PUNCT = " .,'’-()&"   # besides letters of any script and digits; see wall_name()
COURSE_SLUG = re.compile(r"[a-z0-9-]{1,20}")
PROGRESS_STEPS = 7
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
    # the whole site, served at /studio-api/site/ as the second home of the studio (27.11.2026: a backup for GitHub Pages,
    # and a host the page falls back to for its files); None: not served
    site_dir: Path | None = field(default_factory=lambda: Path(p) if (p := os.environ.get("STUDIO_SITE_DIR")) else None)
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


def build_system_prompt(data_dir: Path, keep: tuple | None = None) -> str:
    """Exactly tools/bakeoff.py:system_prompt(): the text of site/data/system_prompt.md below the first
    `---` line, then schema.md, then the samples block from samples.json.
    keep (27.11.2026): a course that reads only some files (Geneva: gc) gets only their sections of schema.md and their
    samples; every dataset's description and samples made each message some 30,000 tokens."""
    try:
        sp = (data_dir / "system_prompt.md").read_text(encoding="utf-8").split("\n---\n", 1)[1].strip()
        samples = json.loads((data_dir / "samples.json").read_text(encoding="utf-8"))
        schema = (data_dir / "schema.md").read_text(encoding="utf-8").strip()
    except (OSError, IndexError, ValueError):
        return PLACEHOLDER_BUILD
    if keep:
        schema = schema_for(schema, keep)
        return "\n\n".join([sp, schema, "## Sample records of the data in this workshop (the real data is much larger)\n\n```json\n"
                             + json.dumps({k: v for k, v in samples.items() if k in keep}, ensure_ascii=False, indent=1) + "\n```"])
    return "\n\n".join([
        sp,
        schema,
        "## Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)\n\n```json\n"
        + json.dumps(samples, ensure_ascii=False, indent=1) + "\n```",
    ])


def schema_for(schema: str, keep: tuple) -> str:
    """schema.md without the sections of the datasets a course does not read (each begins "## `WORKSHOP_DATA.<key>`");
    its opening and the rules for every app stay."""
    parts = re.split(r"(?m)^(?=## )", schema)
    out = [x for x in parts if not ((m := re.match(r"## `WORKSHOP_DATA\.(\w+)`", x)) and m.group(1) not in keep)]
    return "".join(out).strip()


class Refusal(Exception):
    def __init__(self, status: int, message: str, code: str, headers: dict | None = None):
        self.status, self.message, self.code, self.headers = status, message, code, headers or {}


def wall_name(value) -> str | None:
    """The display name a participant chose for the wall: letters of any script, digits, spaces and . , ' ’ - ( ) &.
    Spaces collapse and 40 characters are kept; empty is None. Anything else is refused, so no link, tag or sentence
    of markup fits in a name."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise Refusal(400, "Use letters, numbers and spaces in the name", "bad_name")
    name = re.sub(" +", " ", value.strip())
    # combining marks (an accent typed as a separate character) belong to the letter before them
    if not all(c.isalnum() or c in WALL_NAME_PUNCT or unicodedata.category(c).startswith("M") for c in name):
        raise Refusal(400, "Use letters, numbers and spaces in the name", "bad_name")
    return name[:40].strip() or None


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
    room_dir = cfg.state_dir / "room"
    room_dir.mkdir(parents=True, exist_ok=True)
    systems = {"build": build_system_prompt(cfg.data_dir), "inapp": INAPP_SYSTEM, "question": None}
    try:   # the datasets a request may name (samples.json's keys); an unknown name is ignored
        known_datasets = set(json.loads((cfg.data_dir / "samples.json").read_text(encoding="utf-8")))
    except (OSError, ValueError):
        known_datasets = set()
    built_for: dict = {}

    def system_for(purpose: str, datasets) -> str | None:
        """The instructions for a request: a build that names its course's datasets gets only theirs (made once each)."""
        if purpose != "build" or not isinstance(datasets, list):
            return systems[purpose]
        keep = tuple(sorted({k for k in datasets if isinstance(k, str) and k in known_datasets}))
        if not keep:
            return systems[purpose]
        if keep not in built_for:
            built_for[keep] = build_system_prompt(cfg.data_dir, keep)
        return built_for[keep]
    # ── model keys pasted on the admin page. Each is checked with one free call before it is kept; it then wins over the
    # key in the server's .env. They live in state/keys.json (mode 600, never in git or the image) and are never sent
    # back: the page shows their last four characters. A pasted Claude key also sends Claude straight to Anthropic. ──
    keys_file = cfg.state_dir / "keys.json"
    try:
        pasted = json.loads(keys_file.read_text())
        pasted = {k: v for k, v in pasted.items() if k in KEY_KINDS and isinstance(v, dict) and isinstance(v.get("key"), str)}
    except (OSError, ValueError, AttributeError):
        pasted = {}

    def keys_write() -> None:
        tmp = keys_file.with_suffix(".tmp")
        with os.fdopen(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as fh:
            json.dump(pasted, fh)
        os.replace(tmp, keys_file)

    def or_key() -> str:
        return pasted["openrouter"]["key"] if "openrouter" in pasted else cfg.api_key

    def an_key() -> str:
        return pasted["anthropic"]["key"] if "anthropic" in pasted else cfg.anthropic_key

    def routed(m: models.Model) -> models.Model:
        return models.CLAUDE_DIRECT if m.key == "claude" and "anthropic" in pasted else m
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
    app.add_middleware(CORSMiddleware, allow_origins=cfg.origins, allow_methods=["GET", "HEAD", "POST", "OPTIONS"],
                       allow_headers=["Content-Type", "Range", "If-None-Match", "If-Modified-Since"],
                       # a page on GitHub Pages reads the teaser's version (ETag, Last-Modified) to know when it changed
                       expose_headers=["ETag", "Last-Modified", "Content-Length", "Content-Range", "Accept-Ranges"], max_age=600)
    app.state.cfg, app.state.seats, app.state.systems = cfg, seats, systems
    if cfg.site_dir and cfg.site_dir.is_dir():
        # compressed (the General Comments are 7.9 MB as JSON, 1.6 MB gzipped); only here, never the chat's event stream
        app.mount("/studio-api/site", GZipMiddleware(StaticFiles(directory=cfg.site_dir, html=True), minimum_size=1024, compresslevel=6), name="site")

    def paused() -> bool:
        return seats.setting("paused", "0") == "1"

    def recorded() -> bool:   # the facilitator has switched every browser to the recordings
        return seats.setting("mode", "live") == "recorded"

    def default_model() -> str:
        k = seats.setting("default_model", models.DEFAULT)
        return k if k in models.MODELS else models.DEFAULT

    def seat_or_refuse(code, model: bool = True) -> dict:
        s = seats.get(code)
        if not s or s["disabled"]:
            raise Refusal(403, "Unknown or disabled seat code", "seat")
        if paused():
            raise Refusal(503, "The studio is paused by the facilitator", "paused")
        if model and recorded():   # recorded answers stop the models, not the wall
            raise Refusal(503, "The facilitator has switched the studio to recorded answers.", "recorded_mode")
        return s

    def headers() -> dict:
        return {"Authorization": f"Bearer {or_key()}", "HTTP-Referer": "https://lszoszk.github.io/workshop-studio/",
                "X-Title": "Workshop Studio"}

    async def open_anthropic(m: models.Model, messages: list, purpose: str, system: str | None):
        if not an_key():
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
        if system:
            params["system"] = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        manager = claude.with_options(api_key=an_key()).messages.stream(**params)
        try:
            stream = await manager.__aenter__()
        except anthropic.APIStatusError as e:   # the body is not read: it may quote the prompt
            return None, f"http_{e.status_code}"
        except anthropic.APIError as e:
            return None, type(e).__name__
        return AnthropicLines(manager, stream, m), None

    async def open_upstream(m: models.Model, messages: list, purpose: str, system: str | None):
        if m.api == "anthropic":
            return await open_anthropic(m, messages, purpose, system)
        temperature, max_tokens = PURPOSES[purpose]
        payload = {"model": m.id, "stream": True, "usage": {"include": True}, "temperature": temperature,
                   "max_tokens": max_tokens, "provider": models.provider_block(m),
                   "messages": ([{"role": "system", "content": system}] if system else []) + with_images(messages, "openrouter")}
        if purpose == "build" and is_change(messages) and m.edit_reasoning:
            payload["reasoning"] = {"effort": m.edit_reasoning}   # a change to an app already built
        elif purpose == "build" and m.reasoning:
            payload["reasoning"] = {"effort": m.reasoning}
        elif purpose in ("question", "inapp") and m.reasoning:   # a quick question, or an app's own request (a whole document
            payload["reasoning"] = {"effort": "low"}                # to read): think briefly, or GLM-5.3 thinks past its budget
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

    def is_transient(m: models.Model, err: str | None) -> bool:
        return err == BUSY or (m.api == "anthropic" and err in ANTHROPIC_BUSY)

    async def open_with_retry(m: models.Model, messages: list, purpose: str, system: str | None):
        """open_upstream, retrying a transient refusal with backoff for up to cfg.busy_retry_s: OpenRouter's in-flight
        budget 402 (30 people pressing Build at once on a low balance) and Anthropic's 429 and 529."""
        deadline, delay = time.monotonic() + cfg.busy_retry_s, 0.5
        while True:
            resp, err = await open_upstream(m, messages, purpose, system)
            remaining = deadline - time.monotonic()
            if not is_transient(m, err) or remaining <= 0:
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
        d = {}
        try:
            d = await read_json(request, MAX_CHAT_BYTES)
            seat = seat_or_refuse(d.get("seat"))
            purpose = d.get("purpose") or "build"
            if purpose not in PURPOSES:
                raise Refusal(400, 'purpose must be "build", "inapp" or "question"', "purpose")
            m = models.MODELS.get(d.get("model") or default_model())
            m = m and routed(m)
            if not m:
                raise Refusal(400, "This model is not on the menu", "model")
            messages = clean_messages(d.get("messages"))
            system = system_for(purpose, d.get("datasets"))
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
            code = d.get("seat") if isinstance(d, dict) and isinstance(d.get("seat"), str) else None
            log_event(event="chat", seat=code, status="refused", error=e.code)
            if e.code in ("seat_budget", "daily_budget", "rate_limit", "paused") and code:
                seats.record(code, model=str(d.get("model") or ""), host="", purpose=str(d.get("purpose") or ""),
                             status="refused", error=e.code)
            return refuse(e)

        t0 = time.monotonic()
        used, (resp, err) = m, await open_with_retry(m, messages, purpose, system)
        first_error = err
        # fallback false (the Geneva course): the participant chose this model and gets it or an honest refusal, never
        # another model's answer under its name
        swap = d.get("fallback") is not False
        # a busy account is busy for every model; a fallback that cannot read the images would answer without them
        if resp is None and swap and m.fallback and err != BUSY and (models.MODELS[m.fallback].vision or not messages[-1].get("images")):
            used = routed(models.MODELS[m.fallback])
            resp, err = await open_with_retry(used, messages, purpose, system)
        if resp is None:
            seconds = round(time.monotonic() - t0, 1)
            status = "busy" if is_transient(used, err) else "failed" if not swap else "credit" if err == "http_402" else "error"
            seats.record(seat["code"], model=used.key, host=used.host or "", purpose=purpose,
                         latency_ms=int(seconds * 1000), status=status, error=err)
            log_event(event="chat", seat=seat["code"], model=used.key, purpose=purpose, first_error=first_error,
                      seconds=seconds, status=status, error=err)
            if not swap:
                if status == "busy":
                    return JSONResponse({"error": "The model is busy right now. Try again in a minute, or use the other model.",
                                         "code": "model_busy"}, 503, headers={"Retry-After": "30"})
                return JSONResponse({"error": "The model did not answer. Try again, or use the other model.",
                                     "code": "model_failed"}, 502)
            if status == "busy":
                return JSONResponse({"error": "The model service is busy, try again in a minute", "code": "busy"}, 503,
                                    headers={"Retry-After": "60"})
            if status == "credit":   # both models refused for lack of credit: say so, so the facilitator can top up
                return JSONResponse({"error": "The studio's account with the model service has run out of credit. Tell the "
                                              "facilitator; your apps and the recorded answers still work.", "code": "credit"}, 503)
            return JSONResponse({"error": "The model provider did not respond", "code": "upstream"}, 502)
        prompt_chars = len(system or "") + sum(len(x["content"]) for x in messages)
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
            seat = seat_or_refuse(d.get("seat"), model=False)
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
            name = wall_name(d.get("name"))
        except Refusal as e:
            return refuse(e)
        course = d.get("course") if isinstance(d.get("course"), str) and COURSE_SLUG.fullmatch(d["course"]) else None
        gid = dt.datetime.now().strftime("%H%M%S") + "-" + secrets.token_hex(4)
        # the country the app ran on (a participant may pick another than the seat's) and the files it was
        # given in the chat, so the wall can run it on the same data
        country = d.get("country")
        country = country.strip() if isinstance(country, str) and re.fullmatch(r"[^\W\d_][\w .,'()\-]{0,59}", country.strip()) else seat["country"]
        files = [f for f in (d.get("files") or []) if isinstance(f, str) and re.fullmatch(r"[a-z0-9_]{1,30}", f)][:10] \
            if isinstance(d.get("files"), list) else []
        meta = {"id": gid, "seat": seat["code"], "country": country, "files": files, "name": name, "course": course,
                "title": str(d.get("title") or "Untitled").strip()[:120],
                "model": d.get("model") if d.get("model") in models.MODELS else None,
                "prompt_id": str(d.get("prompt_id") or "")[:60] or None,
                "created": dt.datetime.now().isoformat(timespec="seconds")}
        (gallery_dir / f"{gid}.html").write_text(page, encoding="utf-8")
        (gallery_dir / f"{gid}.json").write_text(json.dumps(meta, ensure_ascii=False))
        log_event(event="gallery", seat=seat["code"], id=gid, bytes=len(page.encode("utf-8")), named=name is not None)
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
                    fh.write(json.dumps({**x, **head}, ensure_ascii=False) + "\n")
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

    # ── the room chat: one file per course (state/room/<course>.json); messages stay until the facilitator clears
    # them. Logs hold who and how long, never the text. ──
    room_cache: dict[str, list] = {}
    room_hits: dict[str, deque] = defaultdict(deque)

    def room(course: str) -> list[dict]:
        if course not in room_cache:
            p = room_dir / f"{course}.json"
            try:
                room_cache[course] = json.loads(p.read_text()) if p.exists() else []
            except (OSError, ValueError):
                room_cache[course] = []
        return room_cache[course]

    def room_save(course: str):
        p = room_dir / f"{course}.json"
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(room(course), ensure_ascii=False))
        tmp.replace(p)

    def room_add(course: str, item: dict) -> dict:
        items = room(course)
        item = {"id": (items[-1]["id"] + 1) if items else 1,
                "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), **item}
        items.append(item)
        room_save(course)
        return item

    def room_course(value) -> str:
        c = str(value or "")
        if not ROOM_COURSE.fullmatch(c):
            raise Refusal(400, "Unknown course", "bad_course")
        return c

    def room_text(value) -> str:
        if not isinstance(value, str) or not value.strip():
            raise Refusal(400, "There is nothing to send", "no_text")
        return value.strip()[:ROOM_MAX_CHARS]

    @app.get("/studio-api/room")
    async def room_get(course: str = ""):
        """What the facilitator sent to the room: everyone in the course may read it, with or without a seat."""
        try:
            c = room_course(course)
        except Refusal as e:
            return refuse(e)
        host = [{"id": i["id"], "at": i["at"], "text": i["text"]} for i in room(c) if i["from"] == "host"]
        return JSONResponse({"items": host[-ROOM_SHOWN:]}, headers={"Cache-Control": "no-store"})

    @app.post("/studio-api/room")
    async def room_post(request: Request):
        """A participant's message to the facilitator; it reaches only the facilitator's room page."""
        try:
            d = await read_json(request)
            c, text = room_course(d.get("course")), room_text(d.get("text"))
            seat = seats.get(d.get("seat")) if d.get("seat") else None   # a recorded-mode visitor has no seat
            sid = str(d.get("sid") or "")
            sid = sid if re.fullmatch(r"[0-9a-f]{8,16}", sid) else None
            who = seat["code"] if seat else sid
            if not who:
                raise Refusal(400, "A message needs a seat or a session", "no_sender")
            if sum(1 for i in room(c) if i["from"] == "guest") >= ROOM_MAX_ITEMS:
                raise Refusal(429, "The room chat is full; tell the facilitator in person", "room_full")
            hits, now = room_hits[f"{c}:{who}"], time.monotonic()
            while hits and now - hits[0] >= ROOM_RATE[1]:
                hits.popleft()
            if len(hits) >= ROOM_RATE[0]:
                raise Refusal(429, "Too many messages, wait a minute", "room_rate")
            hits.append(now)
        except Refusal as e:
            return refuse(e)
        item = room_add(c, {"from": "guest", "text": text, "seat": seat["code"] if seat else None,
                            "label": seat.get("label") if seat else None, "country": seat.get("country") if seat else None,
                            "sid": sid})
        log_event(event="room", course=c, seat=item["seat"], chars=len(text))
        return {"ok": True, "id": item["id"]}

    # "who": one short key for every page of a seat, so the wall can keep each person's newest app. Never the seat code,
    # which spends that seat's budget; the key changes when the server restarts.
    who_salt = secrets.token_bytes(16)

    def who_key(seat):
        return hmac.new(who_salt, seat.encode(), "sha256").hexdigest()[:10] if isinstance(seat, str) else None

    @app.get("/studio-api/gallery")
    async def gallery_list(course: str = ""):
        keep = ("id", "country", "title", "model", "prompt_id", "files", "name", "course", "created")
        return [{**{k: i.get(k) for k in keep}, "who": who_key(i.get("seat"))}
                for i in gallery_items() if not course or i.get("course") == course]

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
                "models": list(models.MODELS), "accepting": not paused() and not recorded(),
                "mode": "recorded" if recorded() else "live",
                # beyond the contract, for the facilitator:
                "build": cfg.build, "balance_usd": balance["value"], "key_configured": bool(or_key()),
                "seats": {"total": len(all_seats), "enabled": sum(1 for s in all_seats if not s["disabled"]),
                          "active_10min": seats.active_count(10)}}

    # ── admin ──
    def admin_ok(key: str | None) -> bool:
        return bool(cfg.admin_key) and hmac.compare_digest((key or "").encode(), cfg.admin_key.encode())

    def admin_state() -> dict:
        return {"paused": paused(), "mode": "recorded" if recorded() else "live", "default_model": default_model(), "spent_today": round(seats.spent_today(), 4),
                "daily_budget": cfg.daily_budget, "balance_usd": balance["value"], "seats": seats.all(),
                "gallery": gallery_items(), "feedback": feedback_items()[:200], "keys": keys_state()}

    def keys_state() -> dict:   # where each key comes from and its last four characters; never the key
        out = {}
        for kind in KEY_KINDS:
            if kind in pasted:
                out[kind] = {"source": "admin", "ends": pasted[kind]["key"][-4:], "at": pasted[kind].get("at")}
            else:
                k = cfg.api_key if kind == "openrouter" else cfg.anthropic_key
                out[kind] = {"source": "server" if k else None, "ends": k[-4:] if k else None, "at": None}
        return out

    async def check_key(kind: str, key: str) -> str | None:
        """None when the service accepts the key (one free call: OpenRouter's key info, Anthropic's model list)."""
        name = KEY_KINDS[kind][1]
        try:
            if kind == "openrouter":
                r = await client.get(f"{OPENROUTER}/key", headers={"Authorization": f"Bearer {key}"}, timeout=10.0)
            else:
                r = await client.get(ANTHROPIC_MODELS, headers={"x-api-key": key, "anthropic-version": "2023-06-01"}, timeout=10.0)
        except httpx.HTTPError as e:
            return f"{name} could not be reached ({type(e).__name__}); the key was not saved"
        return None if r.status_code == 200 else f"{name} refused the key (HTTP {r.status_code}); it was not saved"

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
        wall = "".join(f"<li>{e(g['created'])} · {e(g['country'])} · {e(g['title'])} · {e(g.get('name') or 'no name')} · {e(g.get('course') or 'no course')} "
                       + form("remove_gallery", "Remove", f'<input type="hidden" name="value" value="{e(g["id"])}">')
                       + "</li>" for g in s["gallery"]) or "<li>empty</li>"
        fb = "".join(f"<li><b>{e(f['created'])}</b> · {e(f.get('label') or f.get('seat') or 'no seat')} · "
                     f"{e(f['context'].get('app', ''))}<br>{e(f['text'])}<br><small>{e(' · '.join('%s: %s' % kv for kv in f['context'].items()))}</small></li>"
                     for f in s["feedback"]) or "<li>none yet</li>"
        bal = "unknown" if s["balance_usd"] is None else f"${s['balance_usd']:.2f}"

        def key_row(kind: str, what: str) -> str:
            st = s["keys"][kind]
            now = (f"pasted here{' on ' + e(st['at']) + ' UTC' if st['at'] else ''} · ends …{e(st['ends'])}" if st["source"] == "admin"
                   else f"the server's file · ends …{e(st['ends'])}" if st["source"] == "server" else "none")
            remove = form("clear_key", "Remove", f'<input type="hidden" name="kind" value="{kind}">') if st["source"] == "admin" else ""
            return (f"<tr><td><b>{e(KEY_KINDS[kind][1])}</b><br><small>{e(what)}</small></td><td>{now}</td><td>"
                    + form("set_key", "Save and check", f'<input type="hidden" name="kind" value="{kind}">',
                           f'<input type="password" name="value" size="28" autocomplete="off" spellcheck="false" placeholder="{KEY_KINDS[kind][0]}…">')
                    + f" {remove}</td></tr>")
        keys = (key_row("openrouter", "GLM-5.3, Mistral, and Claude when no Claude key is pasted (through Amazon Bedrock)")
                + key_row("anthropic", "Claude Sonnet straight to Anthropic"))
        body = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Studio admin</title><style>body{{font:14px system-ui;margin:16px}}table{{border-collapse:collapse}}
td,th{{border-bottom:1px solid #ddd;padding:4px 8px;text-align:left}}form{{display:inline}}tr.off{{opacity:.5}}
.bar{{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin:12px 0}}.paused{{color:#b00;font-weight:600}}</style>
<h1>Workshop Studio · admin</h1>{f"<p><b>{e(note)}</b></p>" if note else ""}
<p>Room chat: <a href="/studio-api/admin/room?key={k}&amp;course=venice">Venice</a> · <a href="/studio-api/admin/room?key={k}&amp;course=geneva">Geneva</a></p>
<div class="bar"><span class="{'paused' if s['paused'] else ''}">{'PAUSED: every seat is refused' if s['paused'] else 'Running'}</span>
{form('resume' if s['paused'] else 'pause', 'Resume all seats' if s['paused'] else 'Kill switch: pause all seats')}
<span class="{'paused' if s['mode'] == 'recorded' else ''}">{'RECORDED ANSWERS for everyone: no model is called' if s['mode'] == 'recorded' else 'Live models'}</span>
{form('live' if s['mode'] == 'recorded' else 'recorded', 'Back to live models' if s['mode'] == 'recorded' else 'Recorded answers for everyone')}
<span>Spent today ${s['spent_today']:.2f} / ${s['daily_budget']:.0f} · OpenRouter balance {bal} · times in UTC</span>
{form('default_model', 'Set default model', fields=f'<select name="value">{opts}</select>')}</div>
<h2>Model keys</h2><p>A key pasted here is checked with one free call, then used instead of the key in the server's file.
It stays on the server and is never shown again, only its last four characters. Remove goes back to the server's file.</p>
<table><tr><th>Service</th><th>In use</th><th></th></tr>{keys}</table>
<h2>Seats</h2><table><tr><th>Seat</th><th>Label</th><th>Country</th><th>Spent / budget</th><th>Req</th><th>Err</th><th>Last request</th>
<th>Last error</th><th></th></tr>{rows}</table><h2>Feedback ({len(s["feedback"])})</h2><ul>{fb}</ul><h2>Wall</h2><ul>{wall}</ul>"""
        return HTMLResponse(body, headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    # ── room progress: of the page sessions that sent events for the course today, how many reached each step. The
    # day's file is read again only when it has grown (a participant's page sends every few seconds, the facilitator's
    # page asks every 4). ──
    progress_cache = {"key": None, "by_course": {}}

    def room_progress(course: str) -> dict:
        p = events_dir / f"{dt.date.today().isoformat()}.jsonl"
        try:
            st = p.stat()
        except OSError:
            st = None
        key = (str(p), st.st_size, st.st_mtime_ns) if st else (str(p), 0, 0)
        if progress_cache["key"] != key:
            seen: dict[str, dict] = {}   # course → {"visits": set of sid, step → set of sid}
            if st:
                with p.open(encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            e = json.loads(line)
                        except ValueError:
                            continue   # a line cut short by a write in progress
                        c, sid = e.get("course"), e.get("sid")
                        if not c or not sid:
                            continue
                        got = seen.setdefault(c, {"visits": set(), "steps": defaultdict(set)})
                        got["visits"].add(sid)
                        step = e.get("step")
                        if e.get("t") == "progress" and isinstance(step, (int, float)) and step == int(step) \
                                and 1 <= step <= PROGRESS_STEPS:
                            got["steps"][int(step)].add(sid)
            progress_cache.update(key=key, by_course=seen)
        got = progress_cache["by_course"].get(course)
        return {"visits": len(got["visits"]) if got else 0,
                "steps": {str(n): len(got["steps"][n]) if got else 0 for n in range(1, PROGRESS_STEPS + 1)}}

    # ── the teaser video: one file, put there by tools/teaser/teaser_watch.py --upload. FileResponse answers byte
    # ranges (206 with Content-Range), which Safari needs before it plays a video, and sets ETag and Last-Modified. ──
    @app.api_route("/studio-api/teaser", methods=["GET", "HEAD"])
    async def teaser():
        p = cfg.state_dir / "teaser" / "latest.mp4"
        if not p.is_file():
            return JSONResponse({"error": "There is no teaser yet", "code": "no_teaser"}, 404, headers={"Cache-Control": "no-cache"})
        return FileResponse(p, media_type="video/mp4", headers={"Cache-Control": "no-cache"})

    @app.get("/studio-api/admin/room.json")
    async def admin_room_json(key: str = "", course: str = ""):
        if not admin_ok(key):
            return refuse(Refusal(403, "Wrong admin key", "admin"))
        try:
            c = room_course(course)
        except Refusal as e:
            return refuse(e)
        return JSONResponse({"course": c, "items": room(c), "progress": room_progress(c)}, headers={"Cache-Control": "no-store"})

    @app.post("/studio-api/admin/room")
    async def admin_room_post(request: Request):
        """{key, course, action: post | remove | clear, text, id}: post to the room, take one of your messages back,
        or clear the course's chat after the class."""
        try:
            d = await read_json(request)
            if not admin_ok(str(d.get("key", ""))):
                raise Refusal(403, "Wrong admin key", "admin")
            c, action = room_course(d.get("course")), d.get("action")
            if action == "post":
                item = room_add(c, {"from": "host", "text": room_text(d.get("text"))})
                log_event(event="room", course=c, seat="host", chars=len(item["text"]))
            elif action == "remove":
                items = room(c)
                keep = [i for i in items if not (i["from"] == "host" and i["id"] == d.get("id"))]
                if len(keep) == len(items):
                    raise Refusal(404, "No such message", "not_found")
                items[:] = keep
                room_save(c)
            elif action == "clear":
                room(c).clear()
                room_save(c)
                log_event(event="room_clear", course=c)
            else:
                raise Refusal(400, "Unknown action", "bad_action")
        except Refusal as e:
            return refuse(e)
        return JSONResponse({"ok": True, "course": c, "items": room(c)}, headers={"Cache-Control": "no-store"})

    @app.get("/studio-api/admin/room")
    async def admin_room_page(key: str = "", course: str = "venice"):
        if not admin_ok(key):
            return refuse(Refusal(403, "Wrong admin key", "admin"))
        try:
            c = room_course(course)
        except Refusal as e:
            return refuse(e)
        page = ROOM_PAGE.replace("__COURSE__", htmlmod.escape(c))
        return HTMLResponse(page, headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

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
        ok, note, kind = True, None, f.get("kind")
        if action in ("disable", "enable"):
            ok = seats.set_disabled(seat, action == "disable")
        elif action == "budget":
            try:
                ok = seats.set_budget(seat, float(value))
            except ValueError:
                ok = False
        elif action in ("pause", "resume"):
            seats.set_setting("paused", "1" if action == "pause" else "0")
        elif action in ("recorded", "live"):
            seats.set_setting("mode", action)
        elif action == "default_model":
            ok = value in models.MODELS
            if ok:
                seats.set_setting("default_model", value)
        elif action == "remove_gallery":
            ok = bool(re.fullmatch(r"[0-9]{6}-[0-9a-f]{8}", value)) and (gallery_dir / f"{value}.json").exists()
            if ok:
                for ext in ("json", "html"):
                    (gallery_dir / f"{value}.{ext}").unlink(missing_ok=True)
        elif action == "set_key" and kind in KEY_KINDS:
            value = value.strip()
            note = (None if value.startswith(KEY_KINDS[kind][0]) and 20 <= len(value) <= 300 and value.isprintable() and " " not in value
                    else f"That does not look like a {KEY_KINDS[kind][1]} key (it starts with {KEY_KINDS[kind][0]}); nothing was saved")
            note = note or await check_key(kind, value)
            ok = note is None
            if ok:
                pasted[kind] = {"key": value, "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")}
                keys_write()
                balance["at"] = 0.0   # the balance is read again with the new key
                note = f"{KEY_KINDS[kind][1]} key saved and checked (ends …{value[-4:]})"
        elif action == "clear_key" and kind in KEY_KINDS:
            ok = pasted.pop(kind, None) is not None
            if ok:
                keys_write()
                balance["at"] = 0.0
                note = f"{KEY_KINDS[kind][1]} key removed; the server's file is used again"
        else:
            ok = False
        log_event(event="admin", action=action, seat=seat or None, kind=kind if action in ("set_key", "clear_key") else None, ok=ok)
        if wants_json:
            return JSONResponse({"ok": ok} | ({"note": note} if note else {}) | admin_state(), 200 if ok else 400)
        return admin_page(key, note or f"{action}: {'done' if ok else 'nothing changed'}")

    return app
