#!/usr/bin/env python3
"""Look at the workshop data the way a planner should before writing a plan: what fields there are,
how full they are, what the values look like, what the raw text really looks like.

    python3 tools/look.py overview uhri [--country Kenya]
    python3 tools/look.py sample gc -n 3 [--where committee=CRC]
    python3 tools/look.py values uhri mechanism [--top 15]
    python3 tools/look.py find pdf_text "^\\d+\\.$" [-n 5]          # a regular expression, per line of text
    python3 tools/look.py raw pdf_text --page 2 [--chars 1500]      # the text exactly as stored, line breaks shown
    python3 tools/look.py raw library --doc A/81/351 [-n 3]
    python3 tools/look.py values html_doc tag                       # an HTML document: its block elements (tag, text)

Datasets are the files in site/data/ (uhri = one country's file). With --log <planning id>, each look
is appended to tools/out/planning/<id>.steps.jsonl, so a recorded planning session can replay it.
"""
import argparse
import json
import random
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"
LOGS = ROOT / "tools" / "out" / "planning"


def load(name, country):
    index = json.loads((DATA / "index.json").read_text())
    if name == "uhri":
        c = next((c for c in index["countries"] if c["name"].lower() == country.lower()), None)
        if not c:
            sys.exit(f"no country {country!r}")
        return json.loads((DATA / c["file"]).read_text())
    if name not in index["datasets"]:
        sys.exit(f"no dataset {name!r}; have uhri, {', '.join(index['datasets'])}")
    return json.loads((DATA / index["datasets"][name]["file"]).read_text())


def records(pack):
    if isinstance(pack.get("html"), str):   # a document in HTML: its block elements, in order
        return html_elements(pack["html"])
    return pack.get("records") or pack.get("pages") or []


def html_elements(markup):
    import html as H
    out = []
    for i, m in enumerate(re.finditer(r"<(h[1-6]|p|li|td)\b([^>]*)>(.*?)</\1>", markup, re.S)):
        out.append({"n": i + 1, "tag": m.group(1), "text": H.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip(),
                    "inner_tags": " ".join(sorted(set(re.findall(r"<(\w+)", m.group(3))))) or "none"})
    return out


def kind(v):
    return "list" if isinstance(v, list) else "number" if isinstance(v, (int, float)) and not isinstance(v, bool) else \
        "dict" if isinstance(v, dict) else "null" if v is None else "text" if isinstance(v, str) else type(v).__name__


def short(v, n=80):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= n else s[:n] + "…"


def overview(pack):
    recs = records(pack)
    top = {k: (short(v, 100) if not isinstance(v, list) else f"[{len(v)} items]") for k, v in pack.items() if k not in ("records", "pages", "html")}
    if isinstance(pack.get("html"), str):
        top["html"] = f"[a string of {len(pack['html']):,} characters]"
    lines = [f"Top level: {json.dumps(top, ensure_ascii=False)}", f"{len(recs):,} records"]
    fields = Counter(k for r in recs for k in r)
    for f, n in fields.most_common():
        vals = [r.get(f) for r in recs]
        filled = sum(1 for v in vals if v not in (None, "", []))
        kinds = Counter(kind(v) for v in vals if v is not None)
        ex = next((v for v in vals if v not in (None, "", [])), None)
        extra = ""
        if kinds.most_common(1)[0][0] == "number":
            nums = [v for v in vals if isinstance(v, (int, float))]
            extra = f", {min(nums)}–{max(nums)}"
        elif kinds.most_common(1)[0][0] == "text":
            extra = f", {len(set(v for v in vals if isinstance(v, str)))} distinct"
        lines.append(f"- {f} ({'/'.join(kinds)}): filled {filled:,}/{len(recs):,}{extra}; e.g. {short(ex)}")
    return "\n".join(lines), f"{len(recs):,} records, {len(fields)} fields"


def sample(pack, n, where, seed):
    recs = records(pack)
    if where:
        f, v = where.split("=", 1)
        recs = [r for r in recs if str(r.get(f)) == v or (isinstance(r.get(f), list) and v in map(str, r.get(f)))]
    random.Random(seed).shuffle(recs := list(recs))
    return "\n\n".join(json.dumps(r, ensure_ascii=False, indent=1)[:3000] for r in recs[:n]), f"{min(n, len(recs))} sample records" + (f" where {where}" if where else "")


def values(pack, field, top):
    c = Counter()
    for r in records(pack):
        v = r.get(field)
        for x in (v if isinstance(v, list) else [v]):
            c[x if not isinstance(x, (dict, list)) else json.dumps(x)] += 1
    lines = [f"{len(c):,} distinct values of {field}"] + [f"{n:6,}  {short(v, 100)}" for v, n in c.most_common(top)]
    return "\n".join(lines), f"{len(c):,} distinct values of {field}"


def find(pack, pattern, n):
    rx = re.compile(pattern, re.M)
    hits, total = [], 0
    for r in records(pack):
        for f, v in r.items():
            if isinstance(v, str):
                ms = list(rx.finditer(v))
                total += len(ms)
                for m in ms[: max(0, n - len(hits))]:
                    a, b = max(0, m.start() - 60), min(len(v), m.end() + 60)
                    hits.append(f"[{r.get('id') or r.get('page') or r.get('symbol') or (r.get('tag', '') + ' ' + str(r.get('n', '')))}·{f}] …{v[a:b]!r}…")
    return "\n".join([f"{total:,} matches of /{pattern}/"] + hits), f"{total:,} matches of /{pattern}/"


def raw(pack, page, doc, n, chars):
    if doc:
        d = next((d for d in records(pack) if d.get("id") == doc or d.get("symbol") == doc), None)
        if not d:
            sys.exit(f"no document {doc!r}")
        ps = d.get("passages") or []
        meta = {k: v for k, v in d.items() if k != "passages"}
        body = "\n\n".join(json.dumps(p, ensure_ascii=False) for p in ps[:n])
        return f"{json.dumps(meta, ensure_ascii=False)}\n{len(ps)} passages; the first {min(n, len(ps))}:\n\n{body}", f"{doc}: {len(ps)} passages"
    if isinstance(pack.get("html"), str):   # the markup exactly as stored, from the start of the body
        h = pack["html"]
        return f"the HTML, {len(h):,} characters; the first {min(chars, len(h)):,}:\n{h[:chars]}", "the raw HTML"
    recs = records(pack)
    r = next((r for r in recs if r.get("page") == page), recs[page - 1] if 0 < page <= len(recs) else None)
    if not r:
        sys.exit(f"no page {page}")
    text = r.get("text", "")
    shown = text[:chars].replace("\n", "⏎\n")
    return f"page {page}, {len(text):,} characters (⏎ marks a line break):\n{shown}", f"raw text of page {page}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["overview", "sample", "values", "find", "raw"])
    ap.add_argument("dataset")
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--country", default="Kenya")
    ap.add_argument("-n", type=int, default=3)
    ap.add_argument("--where")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--doc")
    ap.add_argument("--chars", type=int, default=1500)
    ap.add_argument("--log")
    a = ap.parse_args()
    pack = load(a.dataset, a.country)
    if a.cmd == "overview":
        text, summary = overview(pack)
    elif a.cmd == "sample":
        text, summary = sample(pack, a.n, a.where, a.seed)
    elif a.cmd == "values":
        text, summary = values(pack, a.arg, a.top)
    elif a.cmd == "find":
        text, summary = find(pack, a.arg, a.n)
    else:
        text, summary = raw(pack, a.page, a.doc, a.n, a.chars)
    print(text)
    if a.log:
        LOGS.mkdir(parents=True, exist_ok=True)
        entry = {"kind": "look", "dataset": a.dataset, "cmd": a.cmd, "arg": a.arg, "where": a.where, "page": a.page if a.cmd == "raw" else None,
                 "doc": a.doc, "country": a.country if a.dataset == "uhri" else None, "summary": summary,
                 "time": datetime.now().isoformat(timespec="seconds")}
        with open(LOGS / f"{a.log}.steps.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
