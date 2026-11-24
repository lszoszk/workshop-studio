# Studio API contract

One contract, three implementations: the FastAPI server on the VM (`server/`), the Cloudflare Worker (`worker/`) and, for `/chat` only, the front's own direct route to OpenRouter. The front (`site/studio.js`) talks to whichever route answers first; see `site/config.json`.

Base URLs: `https://150.254.115.204/studio-api` (VM), `https://<worker>.workers.dev` (Worker).
CORS: allow `https://lszoszk.github.io`, `http://localhost:8766` and `http://127.0.0.1:8766` (local development). Methods `GET, POST, OPTIONS`; header `Content-Type`.

## `GET /health`

```json
{"ok": true, "version": "2026-11-01", "route": "vm", "default_model": "mistral", "models": ["mistral", "claude", "glm-cn", "glm-eu", "fast"], "accepting": true, "mode": "live"}
```

`accepting: false` when the kill switch is on or the mode is `recorded`. `mode` is `"live"` or `"recorded"`: the facilitator's switch (admin actions `recorded` and `live`) that sends every browser to the recorded answers. The front calls this with a 3-second timeout to pick a route; in Geneva it also polls it every 20 s while it is on this route, and reads `mode` and `accepting` to switch to recorded answers and to offer the way back.

## `GET /seat/{code}`

Codes are 6 characters, case-insensitive.

```json
{"seat": "K7Q2MA", "country": "Kenya", "budget_total": 8.0, "budget_left": 7.42, "disabled": false}
```

`country` is one of the names in `site/data/index.json`. Unknown code → `404 {"error": "Unknown seat code"}`.

## `POST /chat`

Request:

```json
{
  "seat": "K7Q2MA",
  "model": "mistral",
  "purpose": "build",
  "messages": [{"role": "user", "content": "…"}, {"role": "assistant", "content": "…"}, {"role": "user", "content": "…"}]
}
```

- `model` is a menu id from `site/config.json` (`mistral`, `claude`, `glm-cn`, `glm-eu`, `fast`), never an OpenRouter id. The server maps it to the OpenRouter model and the pinned provider, and always sends `provider: {only: [host], allow_fallbacks: false, zdr: true}` and `usage: {include: true}`.
- `purpose`:
  - `build`: the server prepends one system message assembled exactly like `tools/bakeoff.py:system_prompt()`: the text of `site/data/system_prompt.md` below the first `---` line, then `site/data/schema.md`, then the samples block from `site/data/samples.json`. Temperature 0.3, `max_tokens` 64000.
  - `inapp`: a call made by a participant's app through `studio.ask()`. System message: "You are called from inside a data app built in a workshop. Answer only what is asked. If JSON is requested, reply with JSON only, no prose and no code fences." Temperature 0.2, `max_tokens` 8000.
  - `question`: the "Ask the model directly" tool: the user's question goes to the model with no system message and no data. Temperature 0.8, `max_tokens` 1200.
- The front never sends a system message; the server rejects one with 400.
- `fallback` (optional boolean, default `true`): `true` is the usual behaviour, a failing model hands over to the fallback in its menu entry. `false` means the participant's model answers or nothing does (the Geneva course sends it, so nobody is answered by a model they did not choose). With `false`, a transient refusal (Anthropic 429 or 529, OpenRouter's in-flight 402) is retried with backoff (0.5, 1, 2, 4, 5 … s, up to 20 s in all), then:
  - `503 {"error": "The model is busy right now. Try again in a minute, or use the other model.", "code": "model_busy"}` with `Retry-After: 30`;
  - any other failure before the stream starts → `502 {"error": "The model did not answer. Try again, or use the other model.", "code": "model_failed"}`.

  With `true`, the same Anthropic 429 and 529 are retried first and only then fall back.

Response: `text/event-stream`, no buffering. Events, in order:

```
data: {"reasoning": "The user wants a dashboard of…"}
…
data: {"delta": "I built a dashboard…"}
data: {"delta": "```html\n<!doctype html>…"}
…
event: usage
data: {"model": "mistral", "model_label": "Mistral Large 3", "openrouter_model": "mistralai/mistral-large-2512", "host": "Mistral", "host_region": "EU", "zdr": true, "prompt_tokens": 6123, "completion_tokens": 6872, "cost": 0.0809, "seconds": 36.8, "budget_left": 7.34}

event: done
data: {}
```

Errors before the stream starts are plain JSON with a status code: `400` bad request or model not on the menu, `403 {"error": "Unknown or disabled seat code"}`, `429 {"error": "This seat has used its budget"}` or `{"error": "Too many requests from this seat, wait a minute"}`, `503 {"error": "The studio is paused by the facilitator", "code": "paused"}`, `503 {"error": "The facilitator has switched the studio to recorded answers.", "code": "recorded_mode"}` (`/chat` only; the seat is checked first, and the wall still takes pages). Errors after the stream started are sent as

```
event: error
data: {"status": 502, "error": "The model provider stopped responding"}
```

`reasoning` events carry the model's thinking (OpenRouter's `choices[0].delta.reasoning`), streamed as it arrives; they come before the first `delta` and the studio shows them in a "Thinking" box, so a participant sees the model working instead of a blank wait. Pass them through for every model that sends them. For `build`, the server also sends OpenRouter `reasoning: {"effort": …}` from the model's menu entry (see `reasoning` in `site/config.json`; omitted = the model's default).

The front fails over to the next route only when the request fails before the first `reasoning` or `delta` event.

## `POST /gallery` and `GET /gallery`

`POST {"seat", "title", "model", "prompt_id", "html"}` (HTML ≤ 300 kB, no `<script src>` and no external URLs in `src`/`href` except links to `docs.un.org`, `undocs.org`, `uhri.ohchr.org`, `searchlibrary.ohchr.org`) → `{"ok": true, "id": "…"}`.

Two optional fields: `name`, the display name the participant chose (spaces collapse, 40 characters at most; letters of any script, digits, spaces and `. , ' ’ - ( ) &`; empty is stored as `null`; anything else → `400 {"code": "bad_name", "error": "Use letters, numbers and spaces in the name"}`), and `course`, a slug `[a-z0-9-]{1,20}` (anything else is stored as `null`). Logs record only whether a name was given.

`GET /gallery` → `[{"id", "who", "country", "title", "model", "prompt_id", "files", "name", "course", "created"}]`, newest first. `who` is the same short key for every page of one seat (never the seat code, which spends the seat's budget; it changes when the server restarts). `GET /gallery?course=geneva` keeps only that course's pages. `GET /gallery/{id}` → the stored HTML (`text/html`). The Worker does not implement the gallery.

## `GET /room` and `POST /room`: the room chat

`GET /room?course=venice` → `{"items": [{"id", "at", "text"}]}`: the facilitator's messages to everyone in the course (the newest 50, oldest first; `at` in UTC). No seat needed, so recorded mode gets them too. The studio asks every 15 s while the page is visible.

`POST {"course", "text", "seat", "sid"}` (text ≤ 1,000 characters; a seat or the page's session id; 8 messages in 5 minutes per sender) → `{"ok": true, "id"}`: a participant's message to the facilitator. It is never shown to the other participants.

The facilitator reads and writes on `GET /admin/room?key=…&course=…` (a live page; JSON at `/admin/room.json`, actions `post`, `remove` and `clear` on `POST /admin/room`). Messages are kept in `state/room/<course>.json` until the facilitator clears them; logs hold who and how long, never the text. The Worker does not implement the room.

The facilitator's room page also shows progress. The front sends `progress` events (`{"t": "progress", "step": 1–7, "secs", "course"}`) through `POST /events`; `GET /admin/room.json?key=…&course=…` then carries `"progress": {"visits": 24, "steps": {"1": 22, "2": 20, "3": 18, "4": 15, "5": 12, "6": 6, "7": 3}}`: of today's page sessions with an event for that course, how many reached each step.

## `GET /teaser` and `HEAD /teaser`

The teaser video, `state/teaser/latest.mp4` on the server, as `video/mp4` with `ETag`, `Last-Modified`, `Cache-Control: no-cache` and byte ranges (`Range: bytes=…` → `206` with `Content-Range`; Safari will not play a video without them). `404 {"error": "There is no teaser yet", "code": "no_teaser"}` when the file is missing. CORS exposes `ETag` and `Last-Modified`. The Worker does not implement it.

## Logging

Seat, model, purpose, tokens, cost, seconds, status. Never message content, never IP addresses.
