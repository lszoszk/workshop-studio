// Offline check of worker.js against docs/api-contract.md (no Cloudflare account, no network, no credits):
//   node worker/test_worker.mjs
// KV, fetch, GitHub Pages and OpenRouter's SSE are faked in memory; the data pack is read from site/data.
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

const ROOT = new URL("..", import.meta.url).pathname;
const worker = (await import("./worker.js")).default;
const kv = new Map();
const STUDIO = { async get(k, t) { const v = kv.get(k); return v === undefined ? null : t === "json" ? JSON.parse(v) : v; },
                 async put(k, v) { kv.set(k, v); } };
const env = { STUDIO, OPENROUTER_API_KEY: "sk-test", DATA_URL: "https://pages.example/data/",
              RATE_LIMIT: "3", RATE_WINDOW: "300", DAILY_BUDGET: "100", BUSY_RETRY_S: "0.3" };
kv.set("seat:ABCDEF", JSON.stringify({ country: "Kenya", budget: 8, disabled: false }));
const replies = [], sent = [];
const chunk = (o) => `data: ${JSON.stringify(o)}\n\n`;
globalThis.fetch = async (url, init = {}) => {
  url = String(url);
  if (url.endsWith("/credits")) return new Response(JSON.stringify({ data: { total_credits: 50, total_usage: 10 } }));
  if (url.startsWith(env.DATA_URL)) return new Response(readFileSync(ROOT + "site/data/" + url.slice(env.DATA_URL.length)));
  sent.push(JSON.parse(init.body));
  const [status, parts] = replies.shift() || [200, [
    chunk({ provider: "Mistral", choices: [{ delta: { reasoning: "thinking" } }] }),
    chunk({ provider: "Mistral", choices: [{ delta: { content: "hi" } }] }),
    chunk({ choices: [], usage: { prompt_tokens: 10, completion_tokens: 2, cost: 0.25 } }), "data: [DONE]\n\n"]];
  if (status !== 200) return new Response(JSON.stringify({ error: parts?.error ?? {} }), { status });
  const body = new ReadableStream({ start(c) { for (const p of parts) c.enqueue(new TextEncoder().encode(p)); c.close(); } });
  return new Response(body, { status: 200, headers: { "content-type": "text/event-stream" } });
};
const call = async (path, method = "GET", body, origin = "https://lszoszk.github.io") => {
  const waits = [];
  const r = await worker.fetch(new Request("https://w.example" + path, { method, body: body && JSON.stringify(body),
    headers: { Origin: origin, "content-type": "application/json" } }), env, { waitUntil: (p) => waits.push(p) });
  const text = await r.text(); await Promise.all(waits);
  return { status: r.status, text, headers: r.headers, json: () => JSON.parse(text) };
};
const events = (text) => text.trim().split("\n\n").filter((b) => !b.startsWith(":")).map((b) => {
  const ev = (b.match(/^event: (.*)$/m) || [, "message"])[1];
  return [ev, JSON.parse(b.match(/^data: (.*)$/m)[1])];
});
const msg = { seat: "abcdef", model: "mistral", purpose: "build", messages: [{ role: "user", content: "secret" }] };

// health and seat
let r = await call("/health");
assert.deepEqual(r.json(), { ok: true, version: "2026-11-01", route: "worker", default_model: "mistral",
  models: ["mistral", "claude", "glm-cn", "glm-eu", "fast"], accepting: true, balance_usd: 40, key_configured: true });
assert.equal(r.headers.get("access-control-allow-origin"), "https://lszoszk.github.io");
assert.equal((await call("/health", "GET", null, "http://localhost:8766")).headers.get("access-control-allow-origin"), "http://localhost:8766");
assert.equal((await call("/health", "GET", null, "https://evil.example")).headers.get("access-control-allow-origin"), null);
r = await call("/seat/ZZZZZZ"); assert.equal(r.status, 404); assert.equal(r.json().error, "Unknown seat code");
assert.deepEqual((await call("/studio-api/seat/abcdef")).json(),
  { seat: "ABCDEF", country: "Kenya", budget_total: 8, budget_left: 8, disabled: false });

// refusals
assert.equal((await call("/chat", "POST", { ...msg, seat: "ZZZZZZ" })).json().error, "Unknown or disabled seat code");
for (const model of ["mistralai/mistral-large-4-0", "constructor", "gpt"])
  assert.equal((await call("/chat", "POST", { ...msg, model })).json().error, "This model is not on the menu");
assert.equal((await call("/chat", "POST", { ...msg, messages: [{ role: "system", content: "x" }, ...msg.messages] })).status, 400);
assert.equal((await call("/chat", "POST", { ...msg, purpose: "chat" })).status, 400);
assert.equal(sent.length, 0);

// build: normalised stream, exact system message, pinning
r = await call("/chat", "POST", msg);
assert.equal(r.status, 200);
let ev = events(r.text);
assert.deepEqual(ev.slice(0, 2), [["message", { reasoning: "thinking" }], ["message", { delta: "hi" }]]);
assert.ok(!r.text.includes("[DONE]"));
assert.deepEqual(sent.at(-1).reasoning, { effort: "high" });
assert.deepEqual(ev.slice(-2).map((e) => e[0]), ["usage", "done"]);
const u = ev.at(-2)[1];
assert.deepEqual({ ...u, seconds: 0 }, { model: "mistral", model_label: "Mistral Large 4", openrouter_model: "mistralai/mistral-large-4-0",
  host: "Mistral", host_region: "EU", zdr: true, prompt_tokens: 10, completion_tokens: 2, cost: 0.25, seconds: 0, budget_left: 7.75 });
const py = execFileSync("python3", ["-c", "import sys,json,pathlib; sys.path.insert(0,'server'); import app; " +
  "print(json.dumps(app.build_system_prompt(pathlib.Path('site/data'))))"], { cwd: ROOT }).toString();
assert.equal(sent.at(-1).messages[0].content, JSON.parse(py), "build system message differs from server/app.py");
assert.deepEqual([sent.at(-1).temperature, sent.at(-1).max_tokens], [0.3, 64000]);
assert.deepEqual(sent.at(-1).provider, { only: ["mistral/eu"], allow_fallbacks: false, zdr: true, data_collection: "deny" });
assert.equal(Number(kv.get("spent:ABCDEF")), 0.25);
// re-seeding the seat (new budget) keeps its spending
kv.set("seat:ABCDEF", JSON.stringify({ country: "Kenya", budget: 9, disabled: false }));
assert.equal((await call("/seat/ABCDEF")).json().budget_left, 8.75);

// inapp and question
await call("/chat", "POST", { ...msg, model: "fast", purpose: "inapp" });
assert.equal(sent.at(-1).messages[0].role, "system"); assert.equal(sent.at(-1).max_tokens, 8000);
assert.deepEqual(sent.at(-1).provider, { zdr: true, data_collection: "deny" });
assert.equal(sent.at(-1).reasoning, undefined);                 // effort only for build
await call("/chat", "POST", { ...msg, purpose: "question" });
assert.deepEqual(sent.at(-1).messages.map((m) => m.role), ["user"]); assert.equal(sent.at(-1).temperature, 0.8);

// rate limit (3 in this env; 3 chats so far for ABCDEF)
r = await call("/chat", "POST", msg);
assert.equal(r.status, 429); assert.equal(r.json().error, "Too many requests from this seat, wait a minute");
assert.ok(Number(r.headers.get("retry-after")) > 0);

// fallback, on a fresh seat
kv.set("seat:PQRSTU", JSON.stringify({ country: "Tunisia", budget: 8 }));
replies.push([503, []]);
r = await call("/chat", "POST", { ...msg, seat: "PQRSTU", model: "claude" });
assert.equal(sent.at(-1).model, "mistralai/mistral-large-4-0");
assert.equal(events(r.text).at(-2)[1].fallback_from, "claude");
replies.push([503, []], [500, []]);
r = await call("/chat", "POST", { ...msg, seat: "PQRSTU" });
assert.equal(r.status, 502); assert.ok(r.headers.get("content-type").startsWith("application/json"));

// mid-stream error
replies.push([200, [chunk({ choices: [{ delta: { content: "part" } }] }), chunk({ error: { code: 502, message: "overloaded" } })]]);
ev = events((await call("/chat", "POST", { ...msg, seat: "PQRSTU" })).text);
assert.deepEqual(ev[1], ["error", { status: 502, error: "The model provider stopped responding" }]);

// budgets and the kill switch
kv.set("seat:GHJKMN", JSON.stringify({ country: "Kenya", budget: 1 })); kv.set("spent:GHJKMN", "1");
r = await call("/chat", "POST", { ...msg, seat: "GHJKMN" });
assert.equal(r.status, 429); assert.equal(r.json().error, "This seat has used its budget");
kv.set("cfg", JSON.stringify({ paused: true }));
r = await call("/chat", "POST", msg); assert.equal(r.status, 503); assert.equal(r.json().error, "The studio is paused by the facilitator");
assert.equal((await call("/health")).json().accepting, false);
assert.equal((await call("/gallery")).status, 404);
assert.ok(Number(kv.get(`day:${new Date().toISOString().slice(0, 10)}`)) >= 1.0);
// reasoning effort: high for GLM too (2 Nov 2026: all four workshop apps pass, at 2.5–8 min each)
kv.set("cfg", JSON.stringify({}));
kv.set("seat:VWXYZ2", JSON.stringify({ country: "Georgia", budget: 8 }));
await call("/chat", "POST", { ...msg, seat: "VWXYZ2", model: "glm-eu" });
assert.deepEqual(sent.at(-1).reasoning, { effort: "high" });

// OpenRouter's transient in-flight budget 402: retried, then 503 without fallback; other 402s fall back
const IN_FLIGHT = { error: { code: 402, message: "Insufficient credits", metadata: { reason: "in_flight_budget_exhausted" } } };
let before = sent.length;
replies.push([402, IN_FLIGHT]);
r = await call("/chat", "POST", { ...msg, seat: "VWXYZ2" });
assert.equal(r.status, 200);
assert.deepEqual(sent.slice(before).map((q) => q.model), ["mistralai/mistral-large-4-0", "mistralai/mistral-large-4-0"]);
kv.set("seat:VWXYZ3", JSON.stringify({ country: "Georgia", budget: 8 }));
before = sent.length;
for (let i = 0; i < 10; i++) replies.push([402, IN_FLIGHT]);
r = await call("/chat", "POST", { ...msg, seat: "VWXYZ3", model: "claude" });
assert.equal(r.status, 503); assert.equal(r.json().error, "The model service is busy, try again in a minute");
assert.equal(r.headers.get("retry-after"), "60");
const tries = sent.slice(before).map((q) => q.model);
assert.ok(tries.length >= 2 && tries.length <= 4 && tries.every((x) => x === "anthropic/claude-sonnet-5.5"), String(tries));
replies.length = 0;
before = sent.length;
replies.push([402, { error: { code: 402, message: "Insufficient credits" } }]);
r = await call("/chat", "POST", { ...msg, seat: "VWXYZ3", model: "claude" });
assert.equal(r.status, 200);
assert.deepEqual(sent.slice(before).map((q) => q.model), ["anthropic/claude-sonnet-5.5", "mistralai/mistral-large-4-0"]);
console.log("worker: all checks passed");
