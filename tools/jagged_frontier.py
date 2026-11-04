#!/usr/bin/env python3
"""The jagged-frontier slide: one radar of what three models built from the same plans, from the bake-off results.

    python3 tools/jagged_frontier.py      # writes site/slides/jagged-frontier.html

Each axis is the share of a workshop app's automatic checks that a model's first build passed, with the setting the
studio uses (GLM-5.3 at medium reasoning, Mistral Large 3 without; the best build when there were several); "Footnotes" is whether the build found all 141 footnotes of CESCR GC 27 (the earlier,
footnote plan). The runs are listed in RUNS; a run that is missing is skipped.
"""
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "tests" / "bakeoff"
OUT = ROOT / "site" / "slides" / "jagged-frontier.html"

# run directory -> what it is. Sonnet was built in Claude Code (no API, no timing); the others through OpenRouter.
RUNS = {
    "2026-11-03-tabs-sonnet": "claude",
    "2026-11-04-extract-chain": "claude",
    "2026-11-04-pins-inline": "claude",
    "2026-11-04-pdf-flag": "claude",
    "2026-11-04T09-57-48-reasoning-high": "high",
    "2026-11-04T10-38-46-reasoning-low": "low",
    "2026-11-04T10-51-44-reasoning-medium": "medium",
    "2026-11-04T10-58-20": "none",
}
# the setting the studio uses for each model since 4 November 2026 (server/models.py)
STUDIO = {"claude": "claude", "glm-cn": "medium", "mistral-l3": "none"}
NEW_PDF = "2026-11-04-pdf-flag"          # paragraphs only (the plan since 4 November, 11:00)
NEW_PDF_OTHERS = []                      # filled in main(): bake-off runs of s7-4 started after the plan changed
MODELS = [("claude", "Claude Sonnet 5.5", "#1f6fb2"), ("glm-cn", "GLM-5.3", "#9b2335"), ("mistral-l3", "Mistral Large 3", "#8a6d1c")]
AXES = [
    ("s7-1-dashboard", "Dashboard on UN data"),
    ("pdf-paragraphs", "Paragraphs out of a PDF"),
    ("pdf-footnotes", "Footnotes out of a PDF"),
    ("s8-1-verbatim", "Verbatim search"),
    ("s8-5-wiki", "Wiki with checked quotes"),
    ("first-try", "Runs on the first try"),
]


def builds():
    out = []
    runs = dict(RUNS)
    for d in sorted(B.glob("2026-11-04T1[12]-*")):   # the new PDF plan (11:xx) and the dashboards (12:xx); the HTML builds (13:xx) are another exercise
        runs[d.name] = "new-pdf:" + (d.name.split("reasoning-")[-1] if "reasoning-" in d.name else "none")
    for run, kind in runs.items():
        f = B / run / "results.json"
        if not f.exists():
            continue
        for r in json.loads(f.read_text()):
            m = r["model"]
            if m not in {k for k, _, _ in MODELS}:
                continue
            new_pdf = run == NEW_PDF or kind.startswith("new-pdf")
            if r["prompt"] == "s7-4-extract" and r["total"] == 0:
                continue
            # the service failed, not the model (a 502 in the stream, an answer in a second): not a build
            if any('"code": 5' in e for e in r.get("errors", [])) or (r.get("seconds") is not None and r["seconds"] < 5):
                continue
            setting = kind.split(":")[-1]
            if STUDIO[m] != setting:
                continue
            out.append({**r, "run": run, "setting": setting, "new_pdf": new_pdf})
    return out


def main():
    bs = builds()
    data = {}
    for m, name, colour in MODELS:
        mine = [b for b in bs if b["model"] == m]
        share = lambda b: b["passed"] / b["total"] if b["total"] else 0.0
        vals, notes = {}, {}
        for key, _ in AXES:
            if key == "pdf-paragraphs":
                pool = [b for b in mine if b["prompt"] == "s7-4-extract" and b["new_pdf"]]
                score = share
            elif key == "pdf-footnotes":
                pool = [b for b in mine if b["prompt"] == "s7-4-extract" and not b["new_pdf"]]
                score = lambda b: 1.0 if b["checks"].get("text_matches") and b["lines"] else 0.0
            elif key == "first-try":
                pool = [b for b in mine if b["prompt"] in ("s7-1-dashboard", "s7-4-extract", "s8-1-verbatim", "s8-5-wiki")]
                vals[key] = round(100 * sum(1 for b in pool if b["lines"] and b["checks"].get("no_console_errors")) / len(pool)) if pool else None
                notes[key] = f"{sum(1 for b in pool if b['lines'] and b['checks'].get('no_console_errors'))} of {len(pool)} builds"
                continue
            else:
                pool = [b for b in mine if b["prompt"] == key]
                score = share
            if not pool:
                vals[key], notes[key] = None, "not built"
                continue
            best = max(pool, key=score)
            vals[key] = round(100 * score(best))
            got = sum(1 for b in pool if score(b) == 1.0)
            notes[key] = f"best {round(100 * score(best))}% ({best['setting']}); {len(pool)} build{'s' if len(pool) > 1 else ''}, {got} fully passed"
        secs = [b["seconds"] for b in mine if b.get("seconds")]
        data[m] = {"name": name, "colour": colour, "values": vals, "notes": notes,
                   "minutes": round(median(secs) / 60, 1) if secs else None, "builds": len(mine)}
    html = TEMPLATE.replace("__DATA__", json.dumps({"axes": AXES, "models": data, "findings": FINDINGS, "source": SOURCE}, ensure_ascii=False))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    for m in data.values():
        print(m["name"], m["values"], m["minutes"], "min")
    print("->", OUT)


# read against the printed values before each run of this script: they are written by hand
FINDINGS = [
    "<b>No model is best at everything.</b> Mistral Large 3 passed every check on the PDF and the wiki, but only 2 of its 6 dashboards had no error (GLM-5.3: 5 of 6).",
    "<b>GLM-5.3</b> found all 141 footnotes on the harder PDF plan, yet its build of the simpler one stopped on an error.",
    "<b>Claude Sonnet 5.5</b> passed everything, but the plans were written and tuned with it.",
    "Try a model on your own task before you rely on it.",
]
SOURCE = ("Share of each app's automatic checks passed by the first build, with the studio's settings (GLM-5.3 at medium reasoning, "
          "Mistral Large 3 without). Kenya data, 3–4 November 2026; one or two builds per app, so the chart shows a direction, not a measurement. "
          "Footnotes: all 141 of CESCR General comment No. 27, on the earlier plan. Claude was built in Claude Code, not through the studio. "
          "The term: Dell'Acqua et al., \u2018Navigating the Jagged Technological Frontier\u2019, <i>Organization Science</i> (2026), "
          "<a href=\"https://doi.org/10.1287/orsc.2025.21838\">doi:10.1287/orsc.2025.21838</a>.")

TEMPLATE = (Path(__file__).parent / "jagged_frontier.html").read_text(encoding="utf-8")

if __name__ == "__main__":
    main()
