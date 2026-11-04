"""Server-side model menu for Workshop Studio (docs/api-contract.md).

The front sends a menu id (`mistral`, `claude`, `glm-cn`, `glm-eu`, `fast`), never an OpenRouter id.
Each id fixes the OpenRouter model and the host it is pinned to. Every request goes out with Zero
Data Retention; pinned entries also send `only: [host], allow_fallbacks: false`, so OpenRouter can
never quietly reroute a prompt to a host in another jurisdiction. `fast` (in-app calls) may run on
any ZDR host. If the pinned host fails before the stream starts, app.py retries once with the
entry's `fallback`, and the usage event says which model answered.

Hosts are OpenRouter endpoint tags (provider slug, optionally /variant/region). The EU and US entries
use region tags so the badge is true: plain `mistral` or `amazon-bedrock` may be served from
another region. Checked against https://openrouter.ai/api/v1/endpoints/zdr on 31.10.2026 (Mistral Large 3
on mistral/eu on 4.11.2026); re-check
before the workshop (RUNBOOK.md, "Before the day").

Prices are USD per million tokens (OpenRouter list prices for the pinned endpoint). They are used
only to estimate the cost of a stream that ended without OpenRouter's usage figures; normal
accounting uses OpenRouter's own cost.
"""
import json
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Model:
    key: str            # menu id, as in site/config.json
    id: str             # OpenRouter model id
    host: str | None    # OpenRouter endpoint tag the request is pinned to (None: any ZDR host)
    label: str
    host_label: str     # "host" in the usage event
    host_region: str | None   # where the prompt is processed: "EU", "US", "CN" (None: varies)
    price_in: float
    price_out: float
    fallback: str | None
    reasoning: str | None = None   # OpenRouter reasoning effort for build requests (None: the model's default);
                                   # mirrors "reasoning" in site/config.json
    api: str = "openrouter"        # "anthropic": straight to Anthropic's API with ANTHROPIC_API_KEY (app.py)
    zdr: bool = True               # requests go out with zero data retention; Anthropic's own API has none by default
    worker_id: str | None = None   # for api="anthropic": the OpenRouter model and host the Cloudflare Worker uses instead
    worker_host: str | None = None
    edit_reasoning: str | None = None   # effort for a change to an app already built (edit mode): less than a new build


MODELS: dict[str, Model] = {m.key: m for m in [
    # Large 3, not Large 4: Large 4 thinks for 8-10 minutes on a workshop plan whatever the effort, and on the
    # PDF plan its thinking used up the whole answer budget (bake-off, 4.11.2026); Large 3 answers in 2-5
    Model("mistral", "mistralai/mistral-large-2512", "mistral/eu", "Mistral Large 3", "Mistral", "EU",
          0.55, 1.65, fallback="glm-eu"),
    # straight to Anthropic since 4.11.2026 (Łukasz's Console credit); its spend on the server stops at
    # STUDIO_ANTHROPIC_CAP, after which requests go to the fallback. No zero data retention on this route.
    # Medium effort: dashboards in 2.4-2.8 min instead of 4.7-5.3 at high, all checks passed (bake-off, 4.11.2026)
    Model("claude", "claude-sonnet-5-5", "anthropic", "Claude Sonnet 5.5", "Anthropic", "US",
          2.0, 10.0, fallback="mistral", reasoning="medium", api="anthropic", zdr=False, edit_reasoning="low",
          worker_id="anthropic/claude-sonnet-5.5", worker_host="amazon-bedrock/us-east-1"),
    Model("glm-cn", "z-ai/glm-5.3", "z-ai", "GLM-5.3 (developer's service)", "Z.AI", "CN",
          1.4, 4.4, fallback="glm-eu", reasoning="medium", edit_reasoning="low"),
    Model("glm-eu", "z-ai/glm-5.3", "mistral/nvfp4/eu", "GLM-5.3 (run in the EU)", "Mistral", "EU",
          1.54, 4.84, fallback="mistral", reasoning="medium", edit_reasoning="low"),
    Model("fast", "deepseek/deepseek-v4.1-flash", None, "DeepSeek V4.1 Flash", "any ZDR host", None,
          0.45, 1.8, fallback="mistral"),     # the dearest ZDR endpoint, so an estimate never undercharges
]}

DEFAULT = "mistral"


def provider_block(m: Model) -> dict:   # OpenRouter's routing block; an api="anthropic" entry has none
    if m.host is None:
        return {"zdr": True, "data_collection": "deny"}
    return {"only": [m.host], "allow_fallbacks": False, "zdr": True, "data_collection": "deny"}


def estimate_cost(m: Model, prompt_tokens: int, completion_tokens: int, cache_write: int = 0, cache_read: int = 0) -> float:
    """prompt_tokens are the uncached input; a cache write costs 1.25 times the input price, a cache read 0.1 times
    (Anthropic's prompt caching)."""
    return (prompt_tokens * m.price_in + cache_write * m.price_in * 1.25 + cache_read * m.price_in * 0.1
            + completion_tokens * m.price_out) / 1e6


def worker_export() -> dict:
    """The menu as worker/models.json, so the Cloudflare Worker cannot drift from the server. The Worker has only
    an OpenRouter key: an entry that the server sends to Anthropic goes out there through its OpenRouter twin."""
    out = []
    for m in MODELS.values():
        d = asdict(m)
        if m.api == "anthropic":
            d.update(id=m.worker_id, host=m.worker_host, host_label="Amazon Bedrock", api="openrouter", zdr=True,
                     price_in=2.2, price_out=11.0)
        for k in ("api", "zdr", "worker_id", "worker_host", "edit_reasoning"):
            d.pop(k, None)
        out.append(d)
    return json.loads(json.dumps({"default": DEFAULT, "models": out}))


if __name__ == "__main__":      # python3 server/models.py > worker/models.json
    print(json.dumps(worker_export(), indent=1, ensure_ascii=False))
