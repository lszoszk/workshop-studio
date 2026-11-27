#!/usr/bin/env python3
"""A small overview of a workshop file, for the studio's Data step (27.11.2026: on a crowded Wi-Fi the step waited for
the whole file, 1.6 MB compressed, before it showed three records and four numbers).

    python3 tools/overview.py            # writes site/data/gc-overview.json from site/data/gc.json

The overview holds what the data card and "Look inside the file" show: the counts the studio computes (paragraphs,
documents as symbol and title, committees, the first and last year) and the first three records, as they are.
tests/test_overview.py checks that it matches the file; run this after any change to gc.json.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "site" / "data"


def overview(records: list) -> dict:
    years = [r["year"] for r in records if r.get("year")]
    return {"count": len(records), "documents": len({(r["symbol"], r["title"]) for r in records}),
            "committees": len({r["committee"] for r in records}), "years": [min(years), max(years)],
            "records": records[:3]}


def main():
    src = json.loads((DATA / "gc.json").read_text(encoding="utf-8"))
    out = DATA / "gc-overview.json"
    out.write_text(json.dumps({"file": "gc.json", **overview(src["records"])}, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{out.relative_to(DATA.parent.parent)}: {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
