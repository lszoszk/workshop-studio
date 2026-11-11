#!/usr/bin/env python3
"""The jagged-frontier slide: what three models built from the same requests, as three radars side by side.

    python3 tools/jagged_frontier.py      # writes site/slides/jagged-frontier.html

Every bake-off build in tests/bakeoff (all settings tried), sorted three ways: it works (the app passed all of its
automatic checks), partly (it runs but failed a check) or it broke (an error in the app, or no app). A build where the
service failed and not the model (a 5xx in the stream, an answer in under five seconds) is left out. Each radar axis
is the share of an app's builds that worked; the bar under each radar is all of a model's builds.
"""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "tests" / "bakeoff"
OUT = ROOT / "site" / "slides" / "jagged-frontier.html"

# bake-off model key -> the model on the slide (GLM-5.3 at Z.AI or in the EU is one model; Mistral is Large 3 and 4)
FAMILY = {"claude": "claude", "claude-api": "claude", "glm-cn": "glm", "glm-eu": "glm", "mistral-l3": "mistral", "mistral": "mistral"}
MODELS = [("claude", "Claude Sonnet 5.5", "USA"), ("glm", "GLM-5.3", "China"), ("mistral", "Mistral Large 3 and 4", "France")]
AXES = [   # (the label in the table and tooltip, the short one on the radar, the requests it counts)
    ("Dashboard on UN data", "Dashboard", ["s7-1-dashboard"]),
    ("Paragraphs out of a PDF", "PDF \u2192 paragraphs", ["s7-4-extract", "s7-4-extract-pdf"]),
    ("Verbatim search", "Verbatim search", ["s8-1-verbatim"]),
    ("Wiki with checked quotes", "Wiki", ["s8-5-wiki"]),
    ("Small changes to an app", "Small changes", ["edit-1-column", "edit-2-chart", "edit-3-filter"]),
    ("Checks on recommendations", "Recommendations", ["s7-2-who-recommends", "s7-3-check-ten"]),
]


def outcome(r):
    if not r["total"]:
        return "broke"
    if r["passed"] == r["total"]:
        return "works"
    return "broke" if r["checks"].get("no_console_errors") is False else "partly"


def builds():
    out, left_out, days = [], 0, set()
    for f in sorted(B.glob("*/results.json")):
        for r in json.loads(f.read_text()):
            if r["model"] not in FAMILY:
                continue
            if any('"code": 5' in e for e in r.get("errors", [])) or (r.get("seconds") is not None and r["seconds"] < 5):
                left_out += 1
                continue
            days.add(f.parent.name[:10])
            out.append({"model": FAMILY[r["model"]], "prompt": r["prompt"], "outcome": outcome(r), "cost": r.get("cost") or 0})
    return out, left_out, sorted(days)


def main():
    bs, left_out, days = builds()
    models = []
    for key, name, origin in MODELS:
        mine = [b for b in bs if b["model"] == key]
        total = {k: sum(1 for b in mine if b["outcome"] == k) for k in ("works", "partly", "broke")}
        axes = []
        for label, _, prompts in AXES:
            pool = [b for b in mine if b["prompt"] in prompts]
            axes.append({"worked": sum(1 for b in pool if b["outcome"] == "works"), "builds": len(pool)})
        # what a build costs, on the builds with a price (Claude Code's builds of Sonnet have none), and what a working app costs
        priced = [b for b in mine if b["cost"]]
        spend = sum(b["cost"] for b in priced)
        cost = {"per_build": round(spend / len(priced), 2), "per_working": round(spend / sum(1 for b in priced if b["outcome"] == "works"), 2)}
        models.append({"id": key, "name": name, "origin": origin, "builds": len(mine), **total, "axes": axes, "cost": cost})
    span = [datetime.strptime(d, "%Y-%m-%d") for d in (days[0], days[-1])]
    stats = [(f"{len(bs)}", "builds"), (f"{len({b['prompt'] for b in bs})}", "workshop requests"), ("3", "models"),
             (f"{(span[1] - span[0]).days + 1}", "days of testing")]
    data = {"axes": [a for a, _, _ in AXES], "short": [b for _, b, _ in AXES], "models": models, "stats": stats, "findings": FINDINGS,
            "source": SOURCE.format(n=len(bs), left_out=left_out,
                                    span=f"{span[0].day} {span[0]:%B} – {span[1].day} {span[1]:%B %Y}")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    gallery = ROOT / "site" / "gallery" / "index.html"   # the gallery's link to the slide names the number of builds
    gallery.write_text(re.sub(r'(<span id="frontierBuilds">)\d+(</span>)', rf"\g<1>{len(bs)}\g<2>", gallery.read_text(encoding="utf-8")), encoding="utf-8")
    for m in models:
        print(f"{m['name']:<24} {m['builds']:>3} builds: {m['works']} works, {m['partly']} partly, {m['broke']} broke |",
              " · ".join(f"{a['worked']}/{a['builds']}" for a in m["axes"]), f"| ${m['cost']['per_build']} a build, ${m['cost']['per_working']} per working app")
    print("->", OUT)


# written by hand: read them against the printed numbers before each run
FINDINGS = [
    "<b>Claude Sonnet 5.5</b> built a working app nine times in ten, at about $0.28 per working app; GLM-5.3 six times in ten at $0.14, "
    "Mistral five times in ten at $0.10.",
    "<b>The frontier is jagged.</b> GLM-5.3 made every small change work (11 of 11) but fewer than half of the PDF tools; "
    "Mistral built every check on recommendations (9 of 9) and a third of the PDF tools.",
    "<b>Live, 11 November:</b> GLM-5.3 built the wiki from ten PDFs twice; asked to add a network, it wrote the tab but not the graph. "
    "Claude added it the first time.",
    "Try a model on your own task before you rely on it.",
]
SOURCE = ("Each axis: the share of an app's builds that passed all of its automatic checks (the app runs without an error, "
          "uses the workshop data and shows what was asked). Cost: what the model service charged for a build, averaged over the builds "
          "with a price (Sonnet's builds in Claude Code have none), and the same spend divided by the builds that worked. All {n} bake-off builds, {span}, with every setting tried "
          "({left_out} builds where the service failed, not the model, are left out). Claude: Sonnet 5.5, in Claude Code or through "
          "the API; GLM-5.3 at Z.AI or in the EU; Mistral: Large 3 and Large 4. The requests were written and tuned with Claude. "
          "The term: Dell'Acqua et al., ‘Navigating the Jagged Technological Frontier’, <i>Organization Science</i> (2026), "
          "<a href=\"https://doi.org/10.1287/orsc.2025.21838\">doi:10.1287/orsc.2025.21838</a>.")

TEMPLATE = (Path(__file__).parent / "jagged_frontier.html").read_text(encoding="utf-8")

if __name__ == "__main__":
    main()
