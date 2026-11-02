#!/usr/bin/env python3
"""The workshop reference shelf: offline copies of best-practice pages that a model consults
instead of the web, while planning an app (the recorded Fable sessions) and in the studio's chat (RAG).

    python3 tools/shelf.py build                       # tools/shelf_src/*.md -> site/data/shelf.json
    python3 tools/shelf.py search "accessible bar chart colours" [-k 5] [--log s7-1-dashboard]
    python3 tools/shelf.py read chartjs-accessibility [--log s7-1-dashboard]

Each page in tools/shelf_src/ is markdown with YAML frontmatter (id, title, publisher, url, licence,
retrieved, kind: excerpt|summary|code, topics; repo/path/commit for GitHub files). Search is BM25 over
passages of about 150 words, the same scoring the studio runs in the browser. With --log, every search
and read is appended to tools/out/planning/<id>.steps.jsonl, so a recorded planning session can show
the searches its planner really made.
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "shelf_src"
OUT = ROOT / "site" / "data" / "shelf.json"
LOGS = ROOT / "tools" / "out" / "planning"
STOP = set("a an and are as at be by for from has have in is it its of on or that the this to was were will with "
           "you your can should not but if into than then there these they their which when what how".split())
K1, B = 1.2, 0.75


def tokens(s):
    return [t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP and len(t) > 1]


def pages():
    out = []
    for f in sorted(SRC.glob("*.md")):
        if f.name == "SOURCES.md":
            continue
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            sys.exit(f"{f.name}: no frontmatter")
        meta = yaml.safe_load(m.group(1)) or {}
        for k in ("id", "title", "publisher", "url", "licence", "kind"):
            if not meta.get(k):
                sys.exit(f"{f.name}: missing {k}")
        meta["retrieved"] = str(meta.get("retrieved", ""))
        meta["text"] = m.group(2).strip()
        out.append(meta)
    return out


def passages(page, size=150):
    """Paragraphs joined up to about `size` words, so a hit points at a readable piece of the page."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", page["text"]) if p.strip()]
    out, cur = [], []
    for p in paras:
        cur.append(p)
        if sum(len(x.split()) for x in cur) >= size:
            out.append("\n\n".join(cur))
            cur = []
    if cur:
        out.append("\n\n".join(cur))
    return out


def build():
    recs = pages()
    ids = [p["id"] for p in recs]
    dup = [i for i, n in Counter(ids).items() if n > 1]
    if dup:
        sys.exit(f"duplicate ids: {dup}")
    shelf = {
        "dataset": "shelf",
        "title": "Workshop reference shelf: offline copies of best-practice pages",
        "source": "Openly licensed excerpts (licence per page) and summaries written for the workshop, with links to the originals",
        "built": date.today().isoformat(),
        "count": len(recs),
        "records": [{k: p.get(k) for k in ("id", "title", "publisher", "url", "licence", "licence_url", "retrieved",
                                           "kind", "topics", "repo", "path", "commit", "text") if p.get(k) is not None}
                    for p in recs],
    }
    OUT.write_text(json.dumps(shelf, ensure_ascii=False, indent=1), encoding="utf-8")
    kinds = Counter(p["kind"] for p in recs)
    print(f"shelf.json: {len(recs)} pages ({', '.join(f'{v} {k}' for k, v in kinds.items())}), "
          f"{sum(len(p['text'].split()) for p in recs):,} words")


def load():
    if not OUT.exists():
        build()
    return json.loads(OUT.read_text())["records"]


def search(query, k=5):
    docs = [(p, i, t) for p in load() for i, t in enumerate(passages(p))]
    toks = [Counter(tokens(t + " " + p["title"])) for p, _, t in docs]
    avg = sum(sum(c.values()) for c in toks) / max(1, len(toks))
    df = Counter(w for c in toks for w in c)
    n = len(docs)
    q = tokens(query)
    hits = []
    for (p, i, t), c in zip(docs, toks):
        dl = sum(c.values())
        s = sum(math.log(1 + (n - df[w] + .5) / (df[w] + .5)) * c[w] * (K1 + 1) / (c[w] + K1 * (1 - B + B * dl / avg))
                for w in q if w in c)
        if s > 0:
            hits.append((s, p, i, t))
    hits.sort(key=lambda h: -h[0])
    seen, out = set(), []
    for s, p, i, t in hits:   # one passage per page, best first
        if p["id"] in seen:
            continue
        seen.add(p["id"])
        out.append({"id": p["id"], "title": p["title"], "publisher": p["publisher"], "url": p["url"],
                    "licence": p["licence"], "kind": p["kind"], "score": round(s, 2), "passage": i, "text": t})
        if len(out) == k:
            break
    return out


def log(session, entry):
    if not session:
        return
    LOGS.mkdir(parents=True, exist_ok=True)
    entry["time"] = datetime.now().isoformat(timespec="seconds")
    with open(LOGS / f"{session}.steps.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=5)
    s.add_argument("--log")
    r = sub.add_parser("read")
    r.add_argument("id")
    r.add_argument("--log")
    a = ap.parse_args()
    if a.cmd == "build":
        return build()
    if a.cmd == "search":
        hits = search(a.query, a.k)
        log(a.log, {"kind": "search", "query": a.query, "results": [h["id"] for h in hits]})
        print(f'{len(hits)} results for "{a.query}"\n')
        for h in hits:
            snippet = re.sub(r"\s+", " ", h["text"])[:400]
            print(f"[{h['id']}] {h['title']} — {h['publisher']} ({h['kind']}, {h['licence']}) score {h['score']}\n  {h['url']}\n  {snippet}…\n")
        return
    page = next((p for p in load() if p["id"] == a.id), None)
    if not page:
        sys.exit(f"no page {a.id!r}; search first")
    log(a.log, {"kind": "read", "id": page["id"], "title": page["title"], "url": page["url"]})
    print(f"# {page['title']}\n{page['publisher']} · {page['url']} · {page['licence']} ({page['kind']}), retrieved {page['retrieved']}\n")
    print(page["text"])


if __name__ == "__main__":
    main()
