#!/usr/bin/env python3
"""Assemble, check and compose the recorded planning sessions (see tools/planning/FORMAT.md).

    python3 tools/planning.py assemble s7-1-dashboard       # draft + logged steps -> site/data/planning/<id>.json
    python3 tools/planning.py check s7-1-dashboard          # every combination of answers composes cleanly
    python3 tools/planning.py compose s7-1-dashboard [q1=2 q3=1] [--country Kenya]   # print a plan (options 1-based)
"""
import argparse
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = ROOT / "tools" / "planning" / "briefs.json"
DRAFTS = ROOT / "tools" / "out" / "planning"
PACKS = ROOT / "site" / "data" / "planning"
PLAN_HEAD = "Build this app. Follow the plan below; where it says nothing, keep it simple."
MARK = "⟦step⟧"
SLOT = re.compile(r"\{\{([\w.-]+)\}\}")


def step_label(e):
    if e["kind"] == "search":
        return f'Searched the reference shelf: "{e["query"]}"', f'{len(e.get("results", []))} results'
    if e["kind"] == "read":
        return f'Read: {e["title"]}', e.get("url", "")
    what = {"overview": "the fields", "sample": "sample records", "values": f'the values of {e.get("arg")}',
            "find": f'every match of /{e.get("arg")}/', "raw": "the raw text"}.get(e["cmd"], e["cmd"])
    if e["dataset"] == "uhri" and e["cmd"] == "overview":
        return "Looked at the data: {country}, {count} records, {years}", "UN recommendations and observations"
    if e["dataset"] == "gc" and e["cmd"] == "overview":   # recounted by the studio from the file (live "gc_overview")
        return "Looked at the data: {count} paragraphs from {documents} documents of {committees} committees, {years}", \
            "General Comments and General Recommendations, paragraph by paragraph"
    if e["cmd"] == "raw" and e["dataset"] == "html_doc":
        return f"Looked at the data: the raw HTML in {e['dataset']}", e.get("summary", "")
    target = f'{e["dataset"]}' + (f' ({e["doc"]})' if e.get("doc") else f', page {e["page"]}' if e["cmd"] == "raw" else "")
    return f"Looked at the data: {what} in {target}", e.get("summary", "")


def assemble(pid):
    brief = json.loads(BRIEFS.read_text())["apps"][pid]
    draft = json.loads((DRAFTS / f"{pid}.draft.json").read_text())
    log = [json.loads(l) for l in (DRAFTS / f"{pid}.steps.jsonl").read_text().splitlines() if l.strip()]
    parts = draft["notes"].split(MARK)
    if len(parts) - 1 != len(log):
        sys.exit(f"{pid}: {len(parts) - 1} step markers in the notes, {len(log)} logged steps")
    notes, steps = parts[0], []
    for e, after in zip(log, parts[1:]):
        label, detail = step_label(e)
        s = {"at": len(notes), "kind": e["kind"], "label": label, "detail": detail}
        if e["kind"] == "look" and e["dataset"] == "uhri" and e["cmd"] == "overview":
            s["live"] = "uhri_overview"
        if e["kind"] == "look" and e["dataset"] == "gc" and e["cmd"] == "overview":
            s["live"] = "gc_overview"
        if e["kind"] == "read":
            s["shelf_id"] = e["id"]
        if e["kind"] == "search":
            s["results"] = e.get("results", [])
        steps.append(s)
        notes += after
    pack = {"id": pid, "title": brief["title"], "dataset": brief["dataset"], "problem": brief["problem"],
            "facilitator_brief": brief["facilitator_brief"], "planner": draft.get("planner", "Claude Fable 5.1"),
            "recorded": draft.get("recorded", "2026-11-02"), "notes": re.sub(r"[ \t]+\n", "\n", notes).strip(),
            "steps": steps, "questions": draft["questions"], "plan_base": draft["plan_base"].strip()}
    # a short pack (Geneva, 4.12.2026): the participant writes their own brief from labelled paragraphs, which
    # starts the recorded planning whatever its words; the plan names their topic and one of a few looks
    for k in ("brief", "looks", "free_brief", "topic_default"):
        if k in brief or k in draft:
            pack[k] = draft.get(k, brief.get(k))
    problems = check_pack(pack)
    if problems:
        sys.exit(f"{pid}:\n- " + "\n- ".join(problems))
    PACKS.mkdir(parents=True, exist_ok=True)
    (PACKS / f"{pid}.json").write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
    words = len(compose(pack, {}).split())
    print(f"{pid}: {len(steps)} steps, {len(pack['questions'])} questions, notes {len(pack['notes'].split())} words, "
          f"default plan {words} words -> site/data/planning/{pid}.json")


def compose(pack, answers, country="Kenya", topic=None, look=None):
    """answers: {question id: option index (0-based)}; defaults where missing. topic: the participant's topic
    from their brief ({topic}); look: the id of one of the pack's looks ({look}; the first when missing)."""
    fill = {}
    for q in pack["questions"]:
        i = answers.get(q["id"], next(k for k, o in enumerate(q["options"]) if o.get("default")))
        for f in q["options"][i]["fragments"]:
            fill.setdefault(f["section"], []).append(f["text"].strip())
    body = SLOT.sub(lambda m: "\n\n".join(fill.get(m.group(1), [])), pack["plan_base"])
    looks = pack.get("looks") or []
    chosen = next((x for x in looks if x["id"] == look), looks[0] if looks else None)
    body = body.replace("{topic}", topic or pack.get("topic_default", "my topic"))
    body = body.replace("{look}", f'{chosen["label"]}: {chosen["text"]}' if chosen else "")
    body = re.sub(r"\n{3,}", "\n\n", body.replace("{country}", country)).strip()
    return PLAN_HEAD + "\n\n" + body


def check_pack(pack):
    out = []
    qs = pack["questions"]
    want = (3, 4) if pack.get("free_brief") else (4, 5)   # a short pack asks 3–4, the long ones 4–5
    if not want[0] <= len(qs) <= want[1]:
        out.append(f"{len(qs)} questions (want {want[0]}–{want[1]})")
    ids = [q["id"] for q in qs]
    if len(set(ids)) != len(ids):
        out.append("duplicate question ids")
    base_slots = set(SLOT.findall(pack["plan_base"]))
    for q in qs:
        if len(q.get("header", "")) > 12:
            out.append(f"{q['id']}: header longer than 12 characters")
        if not 2 <= len(q["options"]) <= 3:
            out.append(f"{q['id']}: {len(q['options'])} options (want 2–3)")
        if sum(1 for o in q["options"] if o.get("default")) != 1:
            out.append(f"{q['id']}: needs exactly one default option")
        slots = [sorted(f["section"] for f in o["fragments"]) for o in q["options"]]
        if any(s != slots[0] for s in slots):
            out.append(f"{q['id']}: options fill different slots {slots}")
        for s in slots[0]:
            if s not in base_slots:
                out.append(f"{q['id']}: slot {{{{{s}}}}} is not in plan_base")
    filled = {f["section"] for q in qs for f in q["options"][0]["fragments"]}
    for s in base_slots - filled:
        out.append(f"slot {{{{{s}}}}} in plan_base is filled by no question")
    for combo in itertools.product(*[range(len(q["options"])) for q in qs]):
        text = compose(pack, dict(zip(ids, combo)))
        if SLOT.search(text):
            out.append(f"answers {combo}: slots left in the plan")
            break
    if pack.get("free_brief"):
        if not pack.get("brief") or not all({"id", "label", "text"} <= set(b) for b in pack["brief"]):
            out.append("a free-brief pack needs brief paragraphs with id, label and text")
        if "{look}" in pack["plan_base"] and len(pack.get("looks") or []) < 2:
            out.append("the plan names {look} but the pack has fewer than two looks")
        for look in pack.get("looks") or []:
            if "{" in compose(pack, {}, look=look["id"]).replace("{{", ""):
                out.append(f"look {look['id']}: a placeholder is left in the plan")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["assemble", "check", "compose"])
    ap.add_argument("id")
    ap.add_argument("answers", nargs="*")
    ap.add_argument("--country", default="Kenya")
    a = ap.parse_args()
    if a.cmd == "assemble":
        return assemble(a.id)
    pack = json.loads((PACKS / f"{a.id}.json").read_text())
    if a.cmd == "check":
        problems = check_pack(pack)
        n = 1
        for q in pack["questions"]:
            n *= len(q["options"])
        print("\n".join(problems) or f"{a.id}: all {n} combinations compose cleanly")
        return
    answers = {}
    for x in a.answers:
        k, v = x.split("=")
        answers[k] = int(v) - 1
    print(compose(pack, answers, a.country))


if __name__ == "__main__":
    main()
