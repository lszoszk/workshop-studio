"""Edit mode: a change to an existing app comes back as SEARCH/REPLACE pairs (site/data/system_prompt.md).
The same rules as parseEdits() and applyEdits() in site/studio.js, so the bake-off scores what the studio shows.

    from edits import parse_edits, apply_edits
    new_html = apply_edits(old_html, parse_edits(reply))   # None when an edit does not fit
"""
import re

EDIT = re.compile(r"<<<<<<< SEARCH\n([\s\S]*?)\n?=======\n([\s\S]*?)\n?>>>>>>> REPLACE")


def parse_edits(text):
    return [{"search": m.group(1), "replace": m.group(2)} for m in EDIT.finditer(text) if m.group(1).strip()]


def apply_edits(code, edits):
    """Every edit or none: an exact match first, then one that ignores indentation and trailing spaces; a SEARCH
    that occurs twice is as useless as one that occurs nowhere. Returns (html, lines written) or (None, first line)."""
    out, lines = code, 0
    for e in edits:
        at = out.find(e["search"])
        if at >= 0 and out.find(e["search"], at + 1) < 0:
            out = out[:at] + e["replace"] + out[at + len(e["search"]):]
        else:
            L, want = out.split("\n"), [s.strip() for s in e["search"].split("\n")]
            hits = [i for i in range(len(L) - len(want) + 1) if all(L[i + j].strip() == w for j, w in enumerate(want))]
            if len(hits) != 1:
                return None, e["search"].split("\n")[0].strip()[:80]
            L[hits[0]:hits[0] + len(want)] = e["replace"].split("\n")
            out = "\n".join(L)
        lines += len(e["replace"].split("\n"))
    return out, lines
