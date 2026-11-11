#!/usr/bin/env python3
"""Summarise the studio's activity records (server state/events/<day>.jsonl, or GET /studio-api/admin/events) for
calibrating the workshop: builds per request and model with their times, failures, fallbacks, repairs, app errors,
queries, and which tools and files people used.

    python3 tools/events_report.py events-2026-11-20.jsonl [more.jsonl …]
"""
import json
import statistics
import sys
from collections import Counter, defaultdict


def load(paths):
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    yield json.loads(line)


def secs(xs):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    if not xs:
        return "-"
    return f"median {statistics.median(xs):.0f} s, {xs[0]:.0f}-{xs[-1]:.0f} s"


def main(paths):
    ev = list(load(paths))
    visits = {e["sid"] for e in ev}
    seats = {e["seat"] for e in ev if e.get("seat")}
    print(f"{len(ev)} events, {len(visits)} page visits, {len(seats)} seats\n")

    print("Builds by request and model (kind: app / talk / query):")
    builds = defaultdict(list)
    for e in ev:
        if e["t"] == "build":
            builds[(e.get("prompt") or "(own words)", e.get("model"), e.get("kind"))].append(e)
    for (prompt, model, kind), xs in sorted(builds.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        live = [x for x in xs if not x.get("rec")]
        cost = sum(x.get("cost") or 0 for x in live)
        print(f"  {prompt:28} {model or '-':10} {kind:5} {len(xs):3} ({len(live)} live)  {secs(x.get('s') for x in live)}  ${cost:.2f}")

    fails = Counter((e.get("prompt") or "(own words)", e.get("model"), e.get("code")) for e in ev if e["t"] == "build_fail")
    print("\nFailed builds (request, model, code):")
    for k, n in fails.most_common():
        print(f"  {n:3}  {k}")
    fell = Counter((e.get("asked"), e.get("model")) for e in ev if e["t"] == "build" and e.get("fell"))
    if fell:
        print("\nAnswered by the fallback (asked → answered):", dict(fell))

    errs = Counter(e.get("kind") for e in ev if e["t"] == "app_error")
    first = sum(1 for e in ev if e["t"] == "app_error" and e.get("first"))
    print(f"\nApp errors: {sum(errs.values())} ({first} as the app opened), by kind: {dict(errs)}")
    print(f"Automatic repairs sent: {sum(1 for e in ev if e['t'] == 'repair')}")
    q = [e for e in ev if e["t"] == "query"]
    if q:
        print(f"Queries run: {len(q)}, failed: {sum(1 for e in q if not e.get('ok'))} {dict(Counter(e.get('kind') for e in q if not e.get('ok')))}")

    print("\nPicked:", dict(Counter(e.get("prompt") for e in ev if e["t"] == "pick").most_common()))
    print("Plans built with changed answers:", sum(1 for e in ev if e["t"] == "plan_build" and e.get("changed")),
          "of", sum(1 for e in ev if e["t"] == "plan_build"))
    print("Look inside:", dict(Counter(e.get("item") for e in ev if e["t"] == "look").most_common()))
    print("Model switches:", dict(Counter((e.get("by"), e.get("to")) for e in ev if e["t"] == "model")))
    print("Own files:", dict(Counter(e.get("kind") for e in ev if e["t"] == "own_file")),
          "· samples ticked:", sum(1 for e in ev if e["t"] == "own_samples" and e.get("on")),
          "· pictures:", sum(1 for e in ev if e["t"] == "picture"))
    print("Saved as file:", sum(1 for e in ev if e["t"] == "save"), "· sent to the wall:", sum(1 for e in ev if e["t"] == "wall"),
          "· from the gallery:", sum(1 for e in ev if e["t"] == "gallery_in"))
    print("Browsers:", dict(Counter(e.get("ua") for e in ev if e["t"] == "open")),
          "· routes:", dict(Counter(e.get("route") for e in ev if e["t"] == "open")))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
