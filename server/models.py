"""Server-side model menu for Workshop Studio (docs/api-contract.md).

The front sends a menu id (`mistral`, `claude`, `glm-cn`, `glm-eu`, `fast`), never an OpenRouter id.
Each id fixes the OpenRouter model and the host it is pinned to. Every request goes out with Zero
Data Retention; pinned entries also send `only: [host], allow_fallbacks: false`, so OpenRouter can
never quietly reroute a prompt to a host in another jurisdiction. `fast` (in-app calls) may run on
any ZDR host. If the pinned host fails before the stream starts, app.py retries once with the
entry's `fallback`, and the usage event says which model answered.

Hosts are OpenRouter endpoint tags (provider slug, optionally /variant/region). The EU and US entries
use region tags so the badge is true: plain `mistral` or `amazon-bedrock` may be served from
another region. Checked against https://openrouter.ai/api/v1/endpoints/zdr on 31.10.2026; re-check
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


MODELS: dict[str, Model] = {m.key: m for m in [
    Model("mistral", "mistralai/mistral-large-4-0", "mistral/eu", "Mistral Large 4", "Mistral", "EU",
          0.77, 2.31, fallback="glm-eu", reasoning="high"),
    Model("claude", "anthropic/claude-sonnet-5.5", "amazon-bedrock/us-east-1", "Claude Sonnet 5.5",
          "Amazon Bedrock", "US", 2.2, 11.0, fallback="mistral", reasoning="high"),
    Model("glm-cn", "z-ai/glm-5.3", "z-ai", "GLM-5.3 (developer's service)", "Z.AI", "CN",
          1.4, 4.4, fallback="glm-eu", reasoning="high"),
    Model("glm-eu", "z-ai/glm-5.3", "mistral/nvfp4/eu", "GLM-5.3 (run in the EU)", "Mistral", "EU",
          1.54, 4.84, fallback="mistral", reasoning="high"),
    Model("fast", "deepseek/deepseek-v4.1-flash", None, "DeepSeek V4.1 Flash", "any ZDR host", None,
          0.45, 1.8, fallback="mistral"),     # the dearest ZDR endpoint, so an estimate never undercharges
]}

DEFAULT = "mistral"


def provider_block(m: Model) -> dict:
    if m.host is None:
        return {"zdr": True, "data_collection": "deny"}
    return {"only": [m.host], "allow_fallbacks": False, "zdr": True, "data_collection": "deny"}


def estimate_cost(m: Model, prompt_tokens: int, completion_tokens: int) -> float:
    return (prompt_tokens * m.price_in + completion_tokens * m.price_out) / 1e6


def worker_export() -> dict:
    """The menu as worker/models.json, so the Cloudflare Worker cannot drift from the server."""
    return json.loads(json.dumps({"default": DEFAULT, "models": [asdict(m) for m in MODELS.values()]}))


if __name__ == "__main__":      # python3 server/models.py > worker/models.json
    print(json.dumps(worker_export(), indent=1, ensure_ascii=False))
