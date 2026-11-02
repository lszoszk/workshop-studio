#!/usr/bin/env python3
"""Publish bake-off results as the studio's "Same prompt, different models" gallery.

    python3 tools/build_gallery.py tests/bakeoff/2026-10-31T23-09-05-reasoning-high tests/bakeoff/2026-10-31T23-02-58-reasoning-low

A model run several times on the same prompt is shown by its best app, with how many
attempts returned an app and how many passed every check. Copies each app and its screenshot to
site/gallery/apps/<model>/ and writes site/gallery/gallery.json for gallery/index.html.
"""
import json
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bakeoff import request_text   # noqa: E402  what a participant sends, plan or request

ROOT = Path(__file__).resolve().parent.parent
GALLERY = ROOT / "site" / "gallery"

# what the card says about where the model comes from and who ran it
MODELS = {
    "mistral": {"name": "Mistral Large 4", "origin": "France", "host": "Mistral, in the EU", "weights": "closed"},
    "claude": {"name": "Claude Sonnet 5.5", "origin": "USA", "host": "Amazon Bedrock", "weights": "closed"},
    "glm-cn": {"name": "GLM-5.3", "origin": "China", "host": "Z.AI, the developer's service", "weights": "open"},
    "glm-eu": {"name": "GLM-5.3", "origin": "China", "host": "Mistral, in the EU", "weights": "open"},
    "gptoss": {"name": "gpt-oss-20b", "origin": "USA", "host": "CoreWeave", "weights": "open",
               "note": "Small enough to run on a laptop with 16 GB of memory, offline, so nothing leaves the machine. "
                       "Here the same 4-bit weights ran on a cloud server, so the quality is what a laptop would give; "
                       "on a laptop it would take longer."},
}


# the four workshop apps became plans on 2 November 2026: earlier runs of them answered another request
PLANS_SINCE = "2026-11-02T12"


def main(runs):
    prompts = {p["id"]: p for p in json.loads((ROOT / "site/data/prompts.json").read_text())["prompts"]}
    tries = {}
    for run in map(Path, runs):
        for r in json.loads((run / "results.json").read_text()):
            if r["model"] not in MODELS:   # tried in a bake-off, not offered in the studio
                continue
            if prompts.get(r["prompt"], {}).get("plan") and run.name < PLANS_SINCE:
                continue
            r["_run"] = run
            tries.setdefault((r["model"], r["prompt"]), []).append(r)
    best = {k: max(v, key=lambda r: r["passed"] / r["total"]) for k, v in tries.items()}
    apps = GALLERY / "apps"
    if apps.exists():
        shutil.rmtree(apps)
    out = []
    for (m, p), r in sorted(best.items()):
        src = r["_run"] / m
        dst = apps / m
        dst.mkdir(parents=True, exist_ok=True)
        has_app = (src / f"{p}.html").exists() and not (src / f"{p}.html").read_text().startswith("<!-- no html")
        if has_app:
            shutil.copy(src / f"{p}.html", dst / f"{p}.html")
        if (src / f"{p}.png").exists():
            shutil.copy(src / f"{p}.png", dst / f"{p}.png")
        out.append({
            "model": m, "prompt": p, "app": has_app,
            "passed": r["passed"], "total": r["total"],
            "failed": [k for k, v in r["checks"].items() if not v],
            "seconds": r.get("seconds"), "first_token": r.get("first_token"),
            "cost": r.get("cost"), "completion_tokens": r.get("completion_tokens"), "lines": r.get("lines"),
            "attempts": len(tries[(m, p)]),
            "returned": sum(1 for t in tries[(m, p)] if t.get("lines")),
            "full": sum(1 for t in tries[(m, p)] if t["passed"] == t["total"]),
        })
    used = sorted({m for m, _ in best}, key=lambda m: list(MODELS).index(m) if m in MODELS else 99)
    (GALLERY / "gallery.json").write_text(json.dumps({
        "country": "Kenya",
        "built": date.today().isoformat(),
        "models": {m: MODELS.get(m, {"name": m}) for m in used},
        "prompts": [{"id": i, "title": prompts[i]["title"], "prompt": request_text(prompts[i]),
                     "session": prompts[i]["session"]} for i in prompts if any(p == i for _, p in best)],
        "results": out,
    }, indent=1, ensure_ascii=False))
    print(f"{len(out)} apps from {len(runs)} run(s) -> {GALLERY}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
