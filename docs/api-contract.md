# Studio API contract

One contract, three implementations: the FastAPI server on the VM (`server/`), the Cloudflare Worker (`worker/`) and, for `/chat` only, the front's own direct route to OpenRouter. The front (`site/studio.js`) talks to whichever route answers first; see `site/config.json`.

Base URLs: `https://150.254.115.204/studio-api` (VM), `https://<worker>.workers.dev` (Worker).
CORS: allow `https://lszoszk.github.io`, `http://localhost:8766` and `http://127.0.0.1:8766` (local development). Methods `GET, POST, OPTIONS`; header `Content-Type`.

## `GET /health`

```json
{"ok": true, "version": "2026-11-01", "route": "vm", "default_model": "mistral", "models": ["mistral", "claude", "glm-cn", "glm-eu", "fast"], "accepting": true}
```

`accepting: false` when the kill switch is on. The front calls this with a 3-second timeout to pick a route.

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

Errors before the stream starts are plain JSON with a status code: `400` bad request or model not on the menu, `403 {"error": "Unknown or disabled seat code"}`, `429 {"error": "This seat has used its budget"}` or `{"error": "Too many requests from this seat, wait a minute"}`, `503 {"error": "The studio is paused by the facilitator"}`. Errors after the stream started are sent as

```
event: error
data: {"status": 502, "error": "The model provider stopped responding"}
```

`reasoning` events carry the model's thinking (OpenRouter's `choices[0].delta.reasoning`), streamed as it arrives; they come before the first `delta` and the studio shows them in a "Thinking" box, so a participant sees the model working instead of a blank wait. Pass them through for every model that sends them. For `build`, the server also sends OpenRouter `reasoning: {"effort": …}` from the model's menu entry (see `reasoning` in `site/config.json`; omitted = the model's default).

The front fails over to the next route only when the request fails before the first `reasoning` or `delta` event.

## `POST /gallery` and `GET /gallery`

`POST {"seat", "title", "model", "prompt_id", "html"}` (HTML ≤ 300 kB, no `<script src>` and no external URLs in `src`/`href` except links to `docs.un.org`, `undocs.org`, `uhri.ohchr.org`, `searchlibrary.ohchr.org`) → `{"ok": true, "id": "…"}`.

`GET /gallery` → `[{"id", "seat", "country", "title", "model", "created"}]`, newest first. `GET /gallery/{id}` → the stored HTML (`text/html`). The Worker does not implement the gallery.

## Logging

Seat, model, purpose, tokens, cost, seconds, status. Never message content, never IP addresses.
