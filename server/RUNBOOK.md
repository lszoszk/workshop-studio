# Runbook: Workshop Studio API

GHRH "AI for Human Rights Professionals", ITU Geneva, **4 December 2026**, Day 3, Sessions 7 (09:30–11:00) and 8 (11:15–12:45). Up to 30 participants, one seat code each.

```
front   https://lszoszk.github.io/workshop-studio/            GitHub Pages
route 1 https://150.254.115.204/studio-api                     this server: container studio-api, 127.0.0.1:8011
route 2 https://studio-api.lszoszk.workers.dev                  Cloudflare Worker (worker/), same contract, no gallery
```

The HTTP contract is [docs/api-contract.md](../docs/api-contract.md). The server, the Worker and the front all follow it.

Host `amuvmuser@150.254.115.204` (Arrakis), next to echr-api (8000), uhri-api (8001), unhrdb-api (8002), mcp-unhrdb-http (8004), aiact (8005) and mentor-api (8010). This app owns **8011**. Files live in `/home/amuvmuser/workshop-studio/`: `server/`, plus `site/data/{system_prompt.md, schema.md, samples.json}`.

## What the server guarantees

- **The key stays on the server.** `OPENROUTER_API_KEY` is read from `server/.env` on the VM. `deploy.sh` creates that file once from `~/.env` on the laptop, with mode 600. The key is never in git and never in the image.
- **Seat codes, not IPs.** The whole room shares one NAT address, so nothing is limited per IP. Each seat has a budget (default **$8**), a rate limit (**20 requests / 5 minutes**) and a disabled flag. There is also a global daily budget (default **$200**).
- **Pinned hosts with Zero Data Retention** (`models.py`). Every request sends `zdr: true`. The four pinned entries also send `only: [host], allow_fallbacks: false`:

  | menu id | model | host (OpenRouter endpoint tag) | usage `host` / `host_region` |
  |---|---|---|---|
  | `mistral` (default) | `mistralai/mistral-large-4-0` | `mistral/eu` | Mistral / EU |
  | `claude` | `anthropic/claude-sonnet-5.5` | `amazon-bedrock/us-east-1` | Amazon Bedrock / US |
  | `glm-cn` | `z-ai/glm-5.3` | `z-ai` | Z.AI / CN |
  | `glm-eu` | `z-ai/glm-5.3` | `mistral/nvfp4/eu` | Mistral / EU |
  | `fast` (in-app) | `deepseek/deepseek-v4.1-flash` | any ZDR host | the provider that served it / null |

  The region tags matter. Plain `mistral` or `amazon-bedrock` (as in `site/config.json` and `tools/bakeoff.py`) may be served from another region, and then the badge would be wrong.
  If the pinned host fails before the stream starts, the server tries the entry's fallback once (EU wherever possible). The usage event then names the model that answered and adds `fallback_from`.
- **Purposes** (contract): `build` gets the system message from `site/data` (assembled exactly like `tools/bakeoff.py:system_prompt()`, read at start-up), temperature 0.3, 64,000 tokens (Mistral's thinking alone can take 28,000). `inapp` gets the fixed in-app message, 0.2, 8,000 tokens. `question` gets no system message, 0.8, 1,200 tokens. A system message from the front is refused with 400.
- **Thinking is shown.** OpenRouter's `delta.reasoning` is streamed as `data: {"reasoning": …}` before the answer's `delta` events. For `build`, `mistral` and `claude` are sent `reasoning: {effort: "high"}` and the GLM entries `"low"` (as `"reasoning"` in `site/config.json`). Bake-off of 31.10: at high, Claude thinks out loud from about 3 s and an app takes 54–130 s ($0.10–0.25); at low it skipped thinking in 4 of 6 builds. Mistral thinks within 1–6 s at any effort and takes 58–175 s. GLM at low returned 6/6 apps in 34–52 s; at its default it ran out of tokens on half of them.
- **A busy account degrades gracefully.** OpenRouter answers 402 with `metadata.reason: "in_flight_budget_exhausted"` when too many requests are in flight for the balance. That is transient, so the server retries it with backoff (0.5, 1, 2, 4, 5 s… for up to 20 s, `STUDIO_BUSY_RETRY_S`). If it does not clear, the server answers `503 {"error": "The model service is busy, try again in a minute"}` with `Retry-After: 60`. It does not fall back (a busy account is busy for every model) and logs status `busy`. On the admin page this shows as `last_error in_flight_budget_exhausted`: the fix is a top-up. Any other 402 (no credits) is not retried; it goes to the fallback and then 502.
- **Content-free logs.** `docker logs studio-api` shows one JSON line per call: seat, model, purpose, tokens, cost, seconds, status, error code. The usage table in `state/studio.sqlite3` holds the same fields. There is no message text and no IP: uvicorn runs with `--no-access-log`, and nginx has `access_log off` for `/studio-api/`.

Beyond the contract, `/health` also returns `balance_usd` (OpenRouter balance, cached for 60 s), `key_configured` and seat counts. A usage event may carry `estimated: true` (the stream ended before OpenRouter's figures, so the seat is charged an estimate) and `fallback_from`. While the model reasons, the stream carries `: keep-alive` comments every 10 s.

## First install (once)

1. **Seats.** `python3 tools/make_seats.py` writes `tools/out/seats.csv` (`code,country,label,budget`) and the badges to print. Codes are 6 characters from `ABCDEFGHJKMNPQRSTUVWXYZ23456789`; `country` is a name from `site/data/index.json`. The file is a set of credentials, and `tools/out/` is git-ignored: never commit it. The label (who holds the seat) appears only on the admin page and in `seats.py list`. It never goes into logs, public endpoints or the Worker.
2. **Deploy:** `bash server/deploy.sh` (or `SEATS_CSV=path bash server/deploy.sh`). It runs the unit tests, syncs `server/`, the three prompt files and `tools/out/seats.csv` when it exists. It creates `server/.env` on the VM if it is missing (the key plus a new `STUDIO_ADMIN_KEY`), checks for 2 GB of free disk, builds and starts the container, and waits for health. `--dry-run` prints every step and touches nothing. After the restart it imports the seat list. New seats are added; known seats get the file's country, label and budget; spending is never reset. (The automatic import at container start-up only adds new seats, so a plain restart cannot undo a top-up made on the admin page.) By hand: `docker exec studio-api python seats.py import /state/seats.csv`, or locally `python3 -m server.seats import tools/out/seats.csv`.
3. **nginx** (root, once): `ssh -t amuvmuser@150.254.115.204 'sudo bash /home/amuvmuser/workshop-studio/server/install-nginx.sh'`. Run `--dry-run` first to see the diff.
   - It writes `/etc/nginx/conf.d/studio-upstream.conf` and inserts `location /studio-api/` into the 443 server block, between markers.
   - It backs the config up outside `sites-enabled/` and runs `nginx -t`. If the test fails, it restores the backup without reloading.
   - Settings: `proxy_buffering off`, `proxy_read_timeout 300s`, no per-IP `limit_req`, body limit 1 MB.
   - CORS comes from the app: `https://lszoszk.github.io`, `http://localhost:8766` and `http://127.0.0.1:8766`. nginx adds no CORS headers.
4. **Check:** `curl -s https://150.254.115.204/studio-api/health` and `…/studio-api/seat/<a code>`.

Update after a change to the code or to the prompt files: run `bash server/deploy.sh` again. The prompt files are read at start-up. The container is recreated and `state/` (sqlite, gallery) survives.

## Before the day

- [ ] **OpenRouter balance and key limit.** On 2.11.2026 the account balance was **$8.27**, and the key in `~/.env` had a **$25 limit** ($8.98 left). At $3.46 (31.10), 3 parallel requests already hit the in-flight budget 402. Raise both the balance and the server key's limit (Keys page in OpenRouter); a key's own limit stops it even when the account has credits. The plan needs at least $300 (30 seats × $8, plus headroom). `/health` shows `balance_usd`.
- [ ] ZDR is enforced for the whole account in the OpenRouter settings. The request-level `zdr: true` already refuses non-ZDR endpoints.
- [ ] Re-check the pinned hosts: `curl -s https://openrouter.ai/api/v1/endpoints/zdr` must still list each `model_id` + `tag` from the table. Endpoints change. A missing pin fails, and the fallback takes over.
- [ ] Verify the jurisdiction claim for `z-ai` (where Z.AI's API servers are).
- [ ] Load test (`tools/loadtest.py`): 40 streams from one IP through routes 1 and 2. Watch `docker stats studio-api` against the 384 MB cap.
- [ ] On 2.12: open `/health` and the studio from the ITU network.

## On the day

Admin page: `https://150.254.115.204/studio-api/admin?key=<STUDIO_ADMIN_KEY>`. Read the key with `ssh amuvmuser@150.254.115.204 'grep ADMIN /home/amuvmuser/workshop-studio/server/.env'`. Times are UTC. The page has:

- the seat table: spent / budget, requests, errors, last request, last error, with **Disable / Enable** and **Set budget** (a top-up)
- the **kill switch**: every chat and gallery post gets 503 until you press **Resume**, and `/health` says `accepting: false`
- **Set default model**: what a request with an empty `model` uses
- the **Wall**: remove a page from the projector

The same actions as JSON: `POST /studio-api/admin` with `{"key", "action": disable|enable|budget|pause|resume|default_model|remove_gallery, "seat", "value"}`.

CLI inside the container: `docker exec studio-api python seats.py list`, `… create 5 --country Kenya` (spare seats), `… import /state/seats.csv`. After a re-import, the admin page's top-ups are replaced by the file's budget: raise the budget in the file, or top up again.

**Two routes, two sets of books.** Seat spending and the kill switch are kept separately on the VM and in the Worker's KV. If the front falls back to the Worker after a 503 (paused) or a 429 (budget), the seat starts fresh there. When you pause, pause both: use the admin page, then `npx wrangler kv key put --binding STUDIO cfg '{"paused":true}'`.

## Failure drills (do them at the rehearsal, ~20.11)

| Drill | Expected |
|---|---|
| `docker stop studio-api` | nginx answers 502 at once (`max_fails`) and the front moves to the Worker; `docker start studio-api` brings route 1 back |
| pin a model to a host that does not exist (edit `models.py`, deploy) | the fallback answers; the usage event has `fallback_from` |
| kill switch on the admin page | chat and gallery → 503 "The studio is paused by the facilitator"; `/health` → `accepting: false` |
| a seat at its budget | 429 "This seat has used its budget"; **Set budget** reopens it |
| after the workshop: kill switch, or disable every seat | every request is refused |

## Cloudflare Worker (route 2)

Nothing has been created yet. One-time setup, from `worker/`:

```bash
npx wrangler kv namespace create STUDIO        # put the id into wrangler.toml
npx wrangler secret put OPENROUTER_API_KEY      # a SEPARATE key, with a credit limit (e.g. $60) set in OpenRouter
(cd .. && python3 -m server.seats export-kv tools/out/seats.csv) > /tmp/seats-kv.json && npx wrangler kv bulk put --binding STUDIO /tmp/seats-kv.json && rm /tmp/seats-kv.json
npx wrangler deploy                             # name studio-api → https://studio-api.lszoszk.workers.dev (site/config.json)
```

- Seats in KV are `seat:<CODE>` = `{country, budget, disabled}`, with no labels. Spending is kept apart under `spent:<CODE>`, so re-seeding after a new `make_seats.py` run keeps it. Re-seed whenever the seat list changes.
- The menu is `worker/models.json`, generated with `python3 server/models.py > worker/models.json`. `tests/test_server.py` fails if it drifts from the server, or if the purposes or the in-app system message differ.
- The build system message is assembled from `DATA_URL` (the data pack on GitHub Pages) and cached for 10 minutes. `worker/test_worker.mjs` checks that it is byte-for-byte the server's.
- Kill switch: `npx wrangler kv key put --binding STUDIO cfg '{"paused":true}'`. Default model: `'{"default_model":"glm-eu"}'`.
- Limits of the standby:
  - The rate limit is kept per isolate (best effort).
  - KV is eventually consistent, so budgets can overshoot by a request or two.
  - The hard ceiling is the credit limit on the Worker's own key.
  - The free plan allows 1,000 KV writes a day, which is about 500 chats (2 writes each). That is enough for a short outage; for a whole session on route 2, use Workers Paid ($5 a month).
- Offline check, with no account needed: `node worker/test_worker.mjs`.

## Local development

```bash
cd server && STUDIO_ADMIN_KEY=dev uvicorn --factory app:create_app --port 8011 --no-access-log
cd .. && python3 -m server.seats import tools/out/seats.csv   # local seats in server/state/
python3 -m pytest tests/test_server.py -q           # from the repo root; OpenRouter is mocked
node worker/test_worker.mjs
```

Locally the key is read from `~/.env` when `OPENROUTER_API_KEY` is not set, and the prompt files come from `site/data/`.

## Removal after the workshop

```bash
ssh -t amuvmuser@150.254.115.204 'sudo bash /home/amuvmuser/workshop-studio/server/install-nginx.sh --remove'
ssh amuvmuser@150.254.115.204 'cd /home/amuvmuser/workshop-studio && docker compose -f server/docker-compose.yml down && docker image rm studio-api:latest'
```

Then revoke both OpenRouter keys. `state/` holds the usage table and the wall: archive it or delete it.
