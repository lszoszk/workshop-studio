#!/usr/bin/env python3
"""What a room built, scored the way the bake-off scores (for the jagged-frontier slide, tools/jagged_frontier.py).

    STUDIO_ADMIN_KEY=… python3 tools/room_scores.py --label "Venice" --day 2026-11-12 --day 2026-11-13 \
        --out tests/room/venice-2026-11.json
    python3 tools/room_scores.py --label "Venice" --day 2026-11-13 --events 2026-11-13.jsonl …   # a saved activity log

Two measures, both per model and request:
  wall    every app participants sent to the wall on those days, run with the bake-off's own checks for its request
          (tools/bakeoff.py score: works, partly or broke). The wall holds what participants chose to show, often after
          their own changes, so it flatters; an app built on a participant's own file is left out (the file never left
          their computer).
  builds  every new build of a workshop request in the activity log, and how many showed an error as the app opened.
          No selection, but a weaker test: an error, not the checks.

The output holds counts and check names only: no app code, no titles (they can carry a participant's name), no seat codes.
"""
import argparse
import asyncio
import collections
import json
import os
import sys
import tempfile
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bakeoff  # noqa: E402

API = "https://150.254.115.204/studio-api"
FAMILY = {"claude": "claude", "glm-eu": "glm", "glm-cn": "glm", "mistral": "mistral"}   # the server's menu ids → the slide's models


def request_of(item: dict, prompts: dict) -> str | None:
    """The workshop request a wall app came from: its own prompt id when the studio sent one, else its files and title."""
    if item.get("prompt_id") in prompts and prompts[item["prompt_id"]].get("checks"):
        return item["prompt_id"]
    files, title = set(item.get("files") or []), (item.get("title") or "").lower()
    if "gc" in files or "verbatim" in title:
        return "s8-1-verbatim"
    if "hrc" in files or "vote" in title:
        return "s8-3-voting"
    if "pdfs" in files:
        return "v3-wiki-pdfs"   # Venice's wiki from ten PDFs: scored, but no bake-off request to compare it with
    if "uhri" in files or "recommendations" in title:
        return "s7-1-dashboard"
    return None


def outcome(checks: dict) -> str:
    """As the slide counts a bake-off build (tools/jagged_frontier.py)."""
    if not checks:
        return "broke"
    if all(checks.values()):
        return "works"
    return "broke" if checks.get("no_console_errors") is False else "partly"


def builds_from_events(events: list[dict], requests: set[str]) -> list[dict]:
    """Every new build of a workshop request (not a change to an app), and whether an error showed as that app opened,
    before the same visit's next build."""
    by_visit = collections.defaultdict(list)
    for e in events:
        by_visit[e.get("sid")].append(e)
    count = collections.Counter()
    for visit in by_visit.values():
        visit.sort(key=lambda e: e.get("ms") or 0)
        for i, e in enumerate(visit):
            if e.get("t") != "build" or e.get("kind") != "app" or e.get("parent") or e.get("prompt") not in requests:
                continue
            model = FAMILY.get(e.get("model"))
            if not model:
                continue
            after = []
            for x in visit[i + 1:]:
                if x.get("t") == "build":
                    break
                after.append(x)
            broke = any(x.get("t") == "app_error" and x.get("first") for x in after)
            count[(model, e["prompt"], "new")] += 1
            count[(model, e["prompt"], "error_on_open")] += broke
    keys = sorted({(m, p) for m, p, _ in count})
    return [{"model": m, "request": p, "new": count[(m, p, "new")], "error_on_open": count[(m, p, "error_on_open")]} for m, p in keys]


async def score_wall(items: list[dict], pages: dict, prompts: dict, index: dict) -> list[dict]:
    from playwright.async_api import async_playwright
    country_file = next(c["file"] for c in index["countries"] if c["name"] == bakeoff.COUNTRY)
    out = []
    async with async_playwright() as pw:
        browser = await bakeoff.launch(pw)
        with tempfile.TemporaryDirectory() as tmp:
            for it in items:
                req, model = request_of(it, prompts), FAMILY.get(it.get("model"))
                if not req or not model or any(str(k).startswith("own_") for k in it.get("files") or []):
                    continue
                files = set(it.get("files") or []) | {prompts[req].get("dataset") or "uhri", "uhri"}
                init = bakeoff.init_script({k: country_file if k == "uhri" else index["datasets"][k]["file"]
                                            for k in files if k == "uhri" or k in index["datasets"]})
                checks, _, _ = await bakeoff.score(browser, pages[it["id"]], prompts[req]["checks"], init, Path(tmp) / "shot.png")
                out.append({"model": model, "request": req, "outcome": outcome(checks),
                            "failed": sorted(k for k, v in checks.items() if not v)})
        await browser.close()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True, help="the room, as the slide names it (e.g. Venice)")
    ap.add_argument("--day", action="append", required=True, help="a day of the room (YYYY-MM-DD); repeat for more")
    ap.add_argument("--events", action="append", help="activity logs saved before (JSON lines); otherwise fetched with STUDIO_ADMIN_KEY")
    ap.add_argument("--api", default=API)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    raw = json.loads((ROOT / "site" / "data" / "prompts.json").read_text())
    prompts = {p["id"]: p for p in (raw["prompts"] if isinstance(raw, dict) else raw)}
    index = json.loads((ROOT / "site" / "data" / "index.json").read_text())
    with httpx.Client(timeout=60) as http:
        wall = [i for i in http.get(f"{a.api}/gallery").raise_for_status().json() if (i.get("created") or "")[:10] in a.day]
        pages = {i["id"]: http.get(f"{a.api}/gallery/{i['id']}").raise_for_status().text for i in wall}
        if a.events:
            events = [json.loads(line) for f in a.events for line in Path(f).read_text().splitlines() if line.strip()]
        else:
            key = os.environ.get("STUDIO_ADMIN_KEY") or sys.exit("STUDIO_ADMIN_KEY is needed to fetch the activity log (or pass --events)")
            events = [json.loads(line) for d in a.day
                      for line in http.get(f"{a.api}/admin/events", params={"key": key, "day": d}).raise_for_status().text.splitlines() if line.strip()]
    requests = {p for p, v in prompts.items() if v.get("checks")}
    result = {"label": a.label, "days": sorted(a.day),
              "wall": asyncio.run(score_wall(wall, pages, prompts, index)),
              "builds": builds_from_events(events, requests)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(result, indent=1) + "\n")
    tally = collections.Counter((w["model"], w["request"], w["outcome"]) for w in result["wall"])
    print(f"{a.label}: {len(result['wall'])} wall apps scored, {sum(b['new'] for b in result['builds'])} new builds in the log -> {a.out}")
    for k in sorted(tally):
        print("  wall ", *k, tally[k])
    for b in result["builds"]:
        print(f"  build {b['model']} {b['request']}: {b['error_on_open']} of {b['new']} showed an error as the app opened")


if __name__ == "__main__":
    main()
