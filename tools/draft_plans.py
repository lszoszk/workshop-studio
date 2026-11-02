#!/usr/bin/env python3
"""Draft the plans for the four workshop apps with Claude Fable 5.1 (via OpenRouter).

In the studio a starter request opens as a plan on the stage: participants read it, change it,
fill in "Your decisions", and only then build. The plans are written once, before the workshop,
by a strong model, then checked by hand; this script is how they were drafted.

    python3 tools/draft_plans.py                 # draft all four into tools/out/plans/
    python3 tools/draft_plans.py s8-5-wiki       # one of them
    python3 tools/draft_plans.py --brief s8-5-wiki   # only write the brief, for Fable in the Claude app
    python3 tools/draft_plans.py --apply         # copy the drafts into site/data/prompts.json

Needs OPENROUTER_API_KEY in ~/.env and httpx. Costs about $0.25 a plan (no extended thinking).
The wiki plan was drafted by Fable 5.1 in the Claude app from the brief this script writes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"
OUT = ROOT / "tools" / "out" / "plans"
MODEL = "anthropic/claude-fable-5.1"
PLANNED = ["s7-1-dashboard", "s7-4-extract", "s8-1-verbatim", "s8-5-wiki"]

BRIEF = """You are preparing a hands-on workshop for human rights professionals in Geneva: diplomats, and
staff of NGOs, national human rights institutions and the UN. Most have never written code. In the
workshop each of them asks a language model to build a small web app on UN data. The facilitator
teaches one habit: before you build, write a plan; read it, change what you disagree with, then let the
model execute it. Your job is to write that plan for one app, so participants see what a good plan
looks like and can adapt it in two or three minutes.

Write the plan in plain English for that audience (no jargon: say "the code counts", not "the
reducer aggregates"), but precise enough that a model can build the app from it alone. Use exactly
these Markdown sections, in this order, and nothing before the first one:

## Goal
One or two sentences: what the app is for and who uses it.
## The data
Which file the app works on and which of its fields it uses (by field name, from the schema below).
## What the app shows
A numbered list, top of the screen to the bottom: every element, what it contains, what clicking it does.
## Rules for the code
Bullets: how each number is computed, what must stay verbatim, how sources are linked, what to do
with missing values. These are the rules that make the app trustworthy.
## How we will know it works
Three to five checks a participant can do by looking and clicking, each with what they should see.
## Your decisions
Three or four choices a human rights professional is better placed to make than a model, written as
bullets of the form "- **<label>**: {{<id>}}", with one short sentence after each saying what the
choice changes. Not technical choices (no colours, no libraries).
## Not in this version
Two to four bullets: what the app deliberately leaves out.

Keep the whole plan to about 350–450 words. Do not repeat the general rules every app follows
(offline, one HTML file, the design): the studio sends those itself, and they are given below only
so you know them.

Reply with JSON only, no code fence:
{"plan": "<the Markdown plan>",
 "decisions": [{"id": "<id used in {{...}}>", "label": "<as in the plan>",
                "type": "select" or "text", "options": ["<for select: 2 or 3 options, each a short phrase that reads well inside the plan>"],
                "default": "<one of the options, or the default text>"}]}
The default of every decision must give exactly the app described in the request below, so that
someone who changes nothing gets that app."""


def api_key():
    for line in (Path.home() / ".env").read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("OPENROUTER_API_KEY missing in ~/.env")


def schema_section(key):
    text = (DATA / "schema.md").read_text()
    parts = re.split(r"(?m)^## ", text)
    keep = [p for p in parts if p.startswith(f"`WORKSHOP_DATA.{key}`") or p.startswith("Rules for every app")]
    return "\n".join("## " + p for p in keep)


def brief_for(p):
    sp = (DATA / "system_prompt.md").read_text().split("\n---\n", 1)[1].strip()
    checks = json.dumps(p.get("checks", {}), ensure_ascii=False)
    return "\n\n".join([
        BRIEF,
        "# The request this plan is for\n\n" + p.get("intent", p["prompt"]),
        f"# What the facilitator will say after it is built\n\n{p.get('lesson') or ''}",
        "# Automatic checks the finished app must pass (the plan must not contradict them)\n\n" + checks,
        "# The file the app gets (the model building it sees this description and two or three sample records)\n\n"
        + schema_section(p["dataset"]),
        "# The general rules the studio already sends with every request (for your information only)\n\n" + sp,
    ])


def draft(p, client, key):
    body = {"model": MODEL, "max_tokens": 5000, "temperature": 0.4,
            "messages": [{"role": "user", "content": brief_for(p)}]}
    r = client.post("https://openrouter.ai/api/v1/chat/completions", json=body,
                    headers={"Authorization": f"Bearer {key}", "X-Title": "Workshop Studio plans"}, timeout=300)
    r.raise_for_status()
    res = r.json()
    text = res["choices"][0]["message"]["content"].strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    out = json.loads(text)
    out["model"] = MODEL
    out["usage"] = res.get("usage")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", default=PLANNED)
    ap.add_argument("--apply", action="store_true", help="copy the drafts in tools/out/plans/ into prompts.json")
    ap.add_argument("--brief", action="store_true", help="write each brief to tools/out/plans/<id>.brief.md, call no model")
    a = ap.parse_args()
    pj = json.loads((DATA / "prompts.json").read_text())
    by_id = {p["id"]: p for p in pj["prompts"]}
    OUT.mkdir(parents=True, exist_ok=True)
    if a.apply:
        for i in a.ids:
            d = json.loads((OUT / f"{i}.json").read_text())
            by_id[i]["plan"], by_id[i]["decisions"], by_id[i]["plan_by"] = d["plan"], d["decisions"], "Claude Fable 5.1"
        (DATA / "prompts.json").write_text(json.dumps(pj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("prompts.json: plans for", ", ".join(a.ids))
        return
    if a.brief:
        for i in a.ids:
            (OUT / f"{i}.brief.md").write_text(brief_for(by_id[i]), encoding="utf-8")
            print(OUT / f"{i}.brief.md")
        return
    key = api_key()
    with httpx.Client() as client:
        for i in a.ids:
            d = draft(by_id[i], client, key)
            (OUT / f"{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            u = d.get("usage") or {}
            print(f"{i}: {len(d['plan'].split())} words, {len(d['decisions'])} decisions, "
                  f"{u.get('prompt_tokens')}+{u.get('completion_tokens')} tokens, ${u.get('cost')}")


if __name__ == "__main__":
    sys.exit(main())
