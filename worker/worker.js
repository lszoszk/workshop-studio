// Workshop Studio — Cloudflare Worker, the hot standby for the VM proxy (route 2).
//
// Implements docs/api-contract.md for the three endpoints the studio needs when the VM is down:
//   GET  /health   GET /seat/{code}   POST /chat      (a /studio-api prefix is accepted too)
// /chat streams `data: {"reasoning"}` (the model's thinking), `data: {"delta"}`, then `event: usage` and `event: done`.
// No gallery: the Worker answers 404 there, as the contract says.
//
// State lives in the KV namespace bound as STUDIO:
//   seat:<CODE>        {"country","budget","disabled"}   (python3 -m server.seats export-kv tools/out/seats.csv)
//   spent:<CODE>       what the seat has spent here, USD (kept apart, so re-seeding seats never resets it)
//   day:<YYYY-MM-DD>   total spent that day, USD
//   cfg                {"paused": bool, "default_model": id}     (the kill switch)
// The OpenRouter key is a secret (wrangler secret put OPENROUTER_API_KEY). The menu is worker/models.json,
// generated from server/models.py; a test keeps the two identical. The build system message is assembled
// from the data pack on GitHub Pages (DATA_URL), exactly as server/app.py and tools/bakeoff.py do.
//
// Differences from the VM, by design: the rate limit is kept per isolate (best effort), and KV is
// eventually consistent, so budgets can overshoot by a request or two. The hard ceiling is the credit
// limit on the Worker's own OpenRouter key (RUNBOOK.md).
//
// Logs (console.log): seat, model, purpose, tokens, cost, seconds, status. Never content, never IP.
import MODELS from "./models.json" with { type: "json" };

const VERSION = "2026-11-01";
const OPENROUTER = "https://openrouter.ai/api/v1";
const ORIGINS = "https://lszoszk.github.io,http://localhost:8766,http://127.0.0.1:8766";
const MAX_BODY_BYTES = 1_000_000;
const MAX_MESSAGES = 40;
const MAX_CHARS = 300_000;
const KEEPALIVE_MS = 10_000;
const BUSY = "in_flight_budget_exhausted";   // OpenRouter 402 reason: transient, retry after in-flight requests settle
// purpose → [temperature, max_tokens]; the same as PURPOSES in server/app.py (a test checks)
const PURPOSES = {"build": [0.3, 64000], "inapp": [0.2, 8000], "question": [0.8, 4000]};
const INAPP_SYSTEM = "You are called from inside a data app built in a workshop. Answer only what is asked. If JSON is requested, reply with JSON only, no prose and no code fences.";
const PLACEHOLDER_BUILD = "Return one complete HTML document in a single ```html code block. All data is in " +
  "window.WORKSHOP_DATA before your script runs; never use fetch() or load anything from the internet. " +
  "(The studio's system prompt, schema and samples were not found on the server.)";

const BY_KEY = Object.fromEntries(MODELS.models.map((m) => [m.key, m]));
const hits = new Map();                       // seat → request timestamps (this isolate only)
const cache = { build: null, buildAt: 0, balance: null, balanceAt: 0 };
const enc = new TextEncoder();

class Refusal extends Error {
  constructor(status, message, code, headers = {}) {
    super(message);
    Object.assign(this, { status, code, headers });
  }
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin");
  return origin && (env.ALLOWED_ORIGINS || ORIGINS).split(",").includes(origin)
    ? { "Access-Control-Allow-Origin": origin, Vary: "Origin", "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type" }
    : {};
}

const json = (obj, status, headers) =>
  new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...headers } });
const sse = (event, obj) => `${event ? `event: ${event}\n` : ""}data: ${JSON.stringify(obj)}\n\n`;
const today = () => new Date().toISOString().slice(0, 10);
const normalise = (code) => String(code || "").replace(/\s+/g, "").toUpperCase();
const num = (v, d) => (v === undefined || v === "" ? d : Number(v));
const round = (x, n) => Math.round(x * 10 ** n) / 10 ** n;
const log = (fields) => console.log(JSON.stringify(fields));

async function kvJson(env, key, fallback = null) {
  return (await env.STUDIO.get(key, "json")) ?? fallback;
}

function cleanMessages(raw) {
  if (!Array.isArray(raw) || !raw.every((m) => m && typeof m === "object"))
    throw new Refusal(400, "messages must be a list of {role, content}", "bad_messages");
  if (raw.some((m) => m.role === "system"))
    throw new Refusal(400, "System messages are added by the server; do not send one", "system_message");
  if (raw.some((m) => !["user", "assistant"].includes(m.role) || typeof m.content !== "string"))
    throw new Refusal(400, "Each message needs role user or assistant and text content", "bad_messages");
  const msgs = raw.map((m) => ({ role: m.role, content: m.content })).slice(-MAX_MESSAGES);
  const last = msgs[msgs.length - 1];
  if (!last || last.role !== "user" || !last.content.trim()) throw new Refusal(400, "Write a message first", "no_message");
  if (msgs.reduce((n, m) => n + m.content.length, 0) > MAX_CHARS)
    throw new Refusal(400, "This conversation is too long. Start a new thread with an improved prompt", "too_long");
  return msgs;
}

function hit(code, limit, windowS) {
  const now = Date.now() / 1000;
  const h = (hits.get(code) || []).filter((t) => now - t < windowS);
  if (h.length >= limit) { hits.set(code, h); return Math.max(1, Math.floor(windowS - (now - h[0])) + 1); }
  h.push(now);
  hits.set(code, h);
  return 0;
}

// Same assembly as server/app.py build_system_prompt() and tools/bakeoff.py system_prompt().
async function buildSystem(env) {
  if (cache.build && Date.now() - cache.buildAt < 600_000) return cache.build;
  try {
    const get = async (name) => {
      const r = await fetch(env.DATA_URL + name, { signal: AbortSignal.timeout(3000) });
      if (!r.ok) throw new Error(`${name}: ${r.status}`);
      return r.text();
    };
    const [sp, schema, samples] = await Promise.all([get("system_prompt.md"), get("schema.md"), get("samples.json")]);
    const cut = sp.indexOf("\n---\n");
    if (cut < 0) throw new Error("system_prompt.md has no --- line");
    cache.build = [sp.slice(cut + 5).trim(), schema.trim(),
      "## Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)\n\n```json\n" +
      JSON.stringify(JSON.parse(samples), null, 1) + "\n```"].join("\n\n");
    cache.buildAt = Date.now();
  } catch {
    if (!cache.build) return PLACEHOLDER_BUILD;     // keep the last good copy if there is one; retry next time
  }
  return cache.build;
}

const estimate = (m, pt, ct) => (pt * m.price_in + ct * m.price_out) / 1e6;
const providerBlock = (m) => m.host
  ? { only: [m.host], allow_fallbacks: false, zdr: true, data_collection: "deny" }
  : { zdr: true, data_collection: "deny" };

async function openUpstream(env, m, system, messages, purpose) {
  const [temperature, max_tokens] = PURPOSES[purpose];
  const payload = {
    model: m.id, stream: true, usage: { include: true }, temperature, max_tokens, provider: providerBlock(m),
    messages: [...(system ? [{ role: "system", content: system }] : []), ...messages],
  };
  if (purpose === "build" && m.reasoning) payload.reasoning = { effort: m.reasoning };
  else if (purpose === "question" && m.reasoning) payload.reasoning = { effort: "low" };   // a quick question: think briefly
  try {
    const r = await fetch(`${OPENROUTER}/chat/completions`, {
      method: "POST", body: JSON.stringify(payload),
      headers: { Authorization: `Bearer ${env.OPENROUTER_API_KEY}`, "Content-Type": "application/json",
                 "HTTP-Referer": "https://lszoszk.github.io/workshop-studio/", "X-Title": "Workshop Studio" },
    });
    if (r.status === 402) {     // a credits error never quotes the prompt: read the reason, never log the body
      const reason = await r.json().then((d) => d?.error?.metadata?.reason, () => null);
      return [null, reason === BUSY ? BUSY : "http_402"];
    }
    if (r.status !== 200) { r.body?.cancel(); return [null, `http_${r.status}`]; }   // other error bodies may quote the prompt
    return [r, null];
  } catch (e) {
    return [null, e.name || "fetch_error"];
  }
}

// openUpstream, retrying OpenRouter's transient in-flight budget 402 with backoff for up to BUSY_RETRY_S.
async function openWithRetry(env, m, system, messages, purpose) {
  const deadline = Date.now() + num(env.BUSY_RETRY_S, 20) * 1000;
  for (let delay = 500; ; delay = Math.min(delay * 2, 5000)) {
    const [resp, err] = await openUpstream(env, m, system, messages, purpose);
    const remaining = deadline - Date.now();
    if (err !== BUSY || remaining <= 0) return [resp, err];
    await new Promise((ok) => setTimeout(ok, Math.min(delay, remaining)));
  }
}

async function pump(resp, writable, ctx) {
  const { env, used, asked, seat, code, purpose, t0, promptChars, firstError } = ctx;
  const writer = writable.getWriter();
  const reader = resp.body.pipeThrough(new TextDecoderStream()).getReader();
  let usage = {}, provider = null, outChars = 0, status = "ok", error = null, buf = "", lastWrite = Date.now();
  const send = async (s) => { await writer.write(enc.encode(s)); lastWrite = Date.now(); };
  const streamError = () => sse("error", { status: 502, error: "The model provider stopped responding" });
  try {
    read: for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += value;
      const lines = buf.split("\n");
      buf = lines.pop();
      for (const raw of lines) {
        const line = raw.replace(/\r$/, "");
        const data = line.startsWith("data:") ? line.slice(5).trim() : null;
        let chunk = null;
        if (data && data !== "[DONE]") { try { chunk = JSON.parse(data); } catch { /* skip */ } }
        let text = "";
        if (chunk && typeof chunk === "object") {
          if (chunk.error) {
            status = "error"; error = String(chunk.error.code || "stream_error");
            await send(streamError());
            reader.cancel().catch(() => {});
            break read;
          }
          if (chunk.usage) usage = chunk.usage;
          provider = chunk.provider || provider;
          const deltas = (chunk.choices || []).map((c) => c.delta || {});
          const thought = deltas.map((x) => x.reasoning || "").join("");
          text = deltas.map((x) => x.content || "").join("");
          if (thought) { outChars += thought.length; await send(sse(null, { reasoning: thought })); }
        }
        if (text) { outChars += text.length; await send(sse(null, { delta: text })); }
        else if (Date.now() - lastWrite > KEEPALIVE_MS) await send(": keep-alive\n\n");
      }
    }
  } catch (e) {
    // a failed write means the participant closed the tab; a failed read means the upstream broke off
    status = writer.desiredSize === null ? "aborted" : "error";
    error = status === "aborted" ? "client_closed" : e.name || "read_error";
    reader.cancel().catch(() => {});
    if (status === "error") await send(streamError()).catch(() => {});
  }
  const estimated = usage.cost === undefined;
  const pt = Number(usage.prompt_tokens) || (estimated ? Math.floor(promptChars / 4) : 0);
  const ct = Number(usage.completion_tokens) || (estimated ? Math.floor(outChars / 4) : 0);
  const cost = estimated ? estimate(used, pt, ct) : Number(usage.cost) || 0;
  const seconds = round((Date.now() - t0) / 1000, 1);
  if (status !== "aborted") {
    const u = { model: used.key, model_label: used.label, openrouter_model: used.id,
                host: used.host ? used.host_label : provider || used.host_label, host_region: used.host_region,
                zdr: true, prompt_tokens: pt, completion_tokens: ct, cost: round(cost, 6), seconds,
                budget_left: round(Math.max(0, seat.budget - seat.spent - cost), 4) };
    if (estimated) u.estimated = true;
    if (used !== asked) u.fallback_from = asked.key;
    await send(sse("usage", u) + sse("done", {})).catch(() => {});
    await writer.close().catch(() => {});
  }
  // read-modify-write on a fresh copy (the seat's other streams may have finished meanwhile)
  await env.STUDIO.put(`spent:${code}`, String((Number(await env.STUDIO.get(`spent:${code}`)) || 0) + cost));
  const dayKey = `day:${today()}`;
  await env.STUDIO.put(dayKey, String((Number(await env.STUDIO.get(dayKey)) || 0) + cost), { expirationTtl: 7 * 86400 });
  log({ event: "chat", route: "worker", seat: code, model: used.key, purpose, fallback_from: used !== asked ? asked.key : null,
        first_error: firstError, prompt_tokens: pt, completion_tokens: ct, cost: round(cost, 6), estimated, seconds,
        status, error });
}

const defaultModel = (cfg) => (Object.hasOwn(BY_KEY, cfg?.default_model ?? "") ? cfg.default_model : MODELS.default);

async function chat(request, env, waitUntil, cors) {
  const text = await request.text();
  if (text.length > MAX_BODY_BYTES) throw new Refusal(413, "The request is too large", "too_large");
  let d;
  try { d = JSON.parse(text || "{}"); } catch { throw new Refusal(400, "The request is not valid JSON", "bad_json"); }
  if (!d || typeof d !== "object" || Array.isArray(d)) throw new Refusal(400, "The request is not valid JSON", "bad_json");
  const code = normalise(d.seat);
  const stored = code ? await kvJson(env, `seat:${code}`) : null;
  if (!stored || stored.disabled) throw new Refusal(403, "Unknown or disabled seat code", "seat");
  const cfg = await kvJson(env, "cfg", {});
  if (cfg.paused) throw new Refusal(503, "The studio is paused by the facilitator", "paused");
  const seat = { budget: num(stored.budget, num(env.SEAT_BUDGET, 8)), spent: Number(await env.STUDIO.get(`spent:${code}`)) || 0 };
  const purpose = d.purpose || "build";
  if (!PURPOSES[purpose]) throw new Refusal(400, 'purpose must be "build", "inapp" or "question"', "purpose");
  const key = d.model || defaultModel(cfg);
  const m = Object.hasOwn(BY_KEY, key) ? BY_KEY[key] : null;      // hasOwn: "constructor" is not a model
  if (!m) throw new Refusal(400, "This model is not on the menu", "model");
  const messages = cleanMessages(d.messages);
  if (seat.spent >= seat.budget) throw new Refusal(429, "This seat has used its budget", "seat_budget");
  if ((Number(await env.STUDIO.get(`day:${today()}`)) || 0) >= num(env.DAILY_BUDGET, 200))
    throw new Refusal(429, "The studio has reached today's spending limit", "daily_budget");
  const wait = hit(code, num(env.RATE_LIMIT, 20), num(env.RATE_WINDOW, 300));
  if (wait) throw new Refusal(429, "Too many requests from this seat, wait a minute", "rate_limit", { "Retry-After": String(wait) });

  const t0 = Date.now();
  const system = purpose === "build" ? await buildSystem(env) : purpose === "inapp" ? INAPP_SYSTEM : null;
  let used = m;
  let [resp, err] = await openWithRetry(env, m, system, messages, purpose);
  const firstError = err;
  if (!resp && m.fallback && err !== BUSY) {     // a busy account is busy for every model: no fallback
    used = BY_KEY[m.fallback];
    [resp, err] = await openWithRetry(env, used, system, messages, purpose);
  }
  if (!resp) {
    const status = err === BUSY ? "busy" : "error";
    log({ event: "chat", route: "worker", seat: code, model: used.key, purpose, first_error: firstError,
          seconds: round((Date.now() - t0) / 1000, 1), status, error: err });
    if (status === "busy")
      return json({ error: "The model service is busy, try again in a minute", code: "busy" }, 503, { ...cors, "Retry-After": "60" });
    return json({ error: "The model provider did not respond", code: "upstream" }, 502, cors);
  }
  const promptChars = (system || "").length + messages.reduce((n, x) => n + x.content.length, 0);
  const { readable, writable } = new TransformStream();
  waitUntil(pump(resp, writable, { env, used, asked: m, seat, code, purpose, t0, promptChars, firstError }));
  return new Response(readable, { headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", ...cors } });
}

async function balance(env) {
  if (Date.now() - cache.balanceAt > 60_000) {
    cache.balanceAt = Date.now();
    try {
      const r = await fetch(`${OPENROUTER}/credits`, { headers: { Authorization: `Bearer ${env.OPENROUTER_API_KEY}` },
                                                      signal: AbortSignal.timeout(1500) });
      const c = (await r.json()).data;
      cache.balance = round(c.total_credits - c.total_usage, 2);
    } catch { cache.balance = null; }
  }
  return cache.balance;
}

async function health(env) {
  const cfg = await kvJson(env, "cfg", {});
  return { ok: true, version: VERSION, route: "worker", default_model: defaultModel(cfg),
           models: MODELS.models.map((m) => m.key), accepting: !cfg.paused,
           // beyond the contract, for the facilitator (seats are not counted: listing KV costs quota)
           balance_usd: await balance(env), key_configured: !!env.OPENROUTER_API_KEY };
}

async function seatInfo(env, codeRaw) {
  const code = normalise(codeRaw);
  const s = await kvJson(env, `seat:${code}`);
  if (!s) throw new Refusal(404, "Unknown seat code", "seat");
  const budget = num(s.budget, num(env.SEAT_BUDGET, 8)), spent = Number(await env.STUDIO.get(`spent:${code}`)) || 0;
  return { seat: code, country: s.country || "", budget_total: budget, budget_left: round(Math.max(0, budget - spent), 4),
           disabled: !!s.disabled };
}

export default {
  async fetch(request, env, ctx) {
    const cors = corsHeaders(request, env);
    if (request.method === "OPTIONS")
      return new Response(null, { status: 204, headers: { ...cors, "Access-Control-Max-Age": "600" } });
    const path = new URL(request.url).pathname.replace(/^\/studio-api/, "").replace(/\/+$/, "") || "/";
    try {
      if (path === "/health" && request.method === "GET") return json(await health(env), 200, cors);
      if (path.startsWith("/seat/") && request.method === "GET")
        return json(await seatInfo(env, decodeURIComponent(path.slice(6))), 200, cors);
      if (path === "/chat" && request.method === "POST") return await chat(request, env, (p) => ctx.waitUntil(p), cors);
      return json({ error: "Not found", code: "not_found" }, 404, cors);     // includes /gallery: VM only
    } catch (e) {
      if (e instanceof Refusal) return json({ error: e.message, code: e.code }, e.status, { ...cors, ...e.headers });
      log({ event: "error", route: "worker", error: e.name });
      return json({ error: "Internal error", code: "internal" }, 500, cors);
    }
  },
};
