#!/usr/bin/env python3
"""Verify the research wiki's pins against the library, and lint the wiki (tools/wiki/, schema in WIKI.md).

    python3 tools/wiki_verify.py                      # every page: pins, links, orphans, sources, registers, cards, index
    python3 tools/wiki_verify.py --check FILE …       # some pages only: frontmatter, pins, cards (no graph checks)
    python3 tools/wiki_verify.py --find "regex" [--doc ID]   # passages matching, each with the pin to paste
    python3 tools/wiki_verify.py --doc ID             # every passage of one document
    python3 tools/wiki_verify.py --pdf                # also look for each verified quote on the PDF page itself

A pin is `[label](pin:DOC#pPAGE "quote") ✓`. It is verified when the quote, normalised (whitespace,
quotes, dashes, hyphenation), is in a passage of DOC in site/data/library.json that starts on PDF page
PAGE, and the label is "<cite as>, para. N" or "<cite as>, p. N" for that passage. Exits with 1 when
a pin is not verified or the lint finds an error.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "tools/wiki"
LIBRARY = ROOT / "site/data/library.json"
FOLDERS = {"source": "sources", "concept": "concepts", "entity": "entities", "question": "questions"}
REQUIRED = ("title", "type", "tags", "register", "status", "updated", "links", "sources")
STATUSES = ("stub", "draft", "reviewed")
VERDICTS = ("settled-support", "leans-support", "contested", "leans-contest", "settled-contest")
PIN = re.compile(r'\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)')
LINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
CARD = re.compile(r"^```contested\n(.*?)^```", re.S | re.M)
ELLIPSIS = re.compile(r"\s*(?:…|\.\.\.)\s*")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("­", "")
    s = re.sub(r"[‘’ʼ´`]", "'", s)
    s = re.sub(r"[“”„″]", '"', s)
    s = re.sub(r"[‐‑‒–—―−]", "-", s)
    s = re.sub(r"-\s*", "", s)   # "decision- making" = "decision-making" = "decisionmaking"
    return re.sub(r"\s+", " ", s).strip()


def found(quote, text):
    """Every fragment of the quote (split at …) in the normalised passage text, in order."""
    at = 0
    for frag in ELLIPSIS.split(quote):
        frag = norm(frag)
        if not frag:
            continue
        i = text.find(frag, at)
        if i < 0:
            return False
        at = i + len(frag)
    return True


def load_library():
    lib = {d["id"]: d for d in json.loads(LIBRARY.read_text(encoding="utf-8"))["records"]}
    for d in lib.values():
        for p in d["passages"]:
            p["norm"] = norm(p["text"])
    return lib


def library_table():
    """The `| id | cite as | register | kind |` rows of WIKI.md."""
    rows = {}
    for line in (WIKI / "WIKI.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[2] in tuple("abcdef"):
            rows[cells[0]] = {"cite": cells[1], "register": cells[2]}
    return rows


def label_for(p, cite):
    return f"{cite}, para. {p['paragraph']}" if p["paragraph"] else f"{cite}, p. {p['page_label']}"


def same_label(a, b):
    return re.sub(r"\s+\(", "(", norm(a)) == re.sub(r"\s+\(", "(", norm(b))


def pin_text(d, p, cite, quote="…"):
    return f'[{label_for(p, cite)}](pin:{d["id"]}#p{p["page"]} "{quote}") ✓'


def parse(path):
    """(frontmatter dict, body) of a page; frontmatter None if missing."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if not k:
            continue
        if k == "links":
            fm[k] = LINK.findall(v)
        elif v.startswith("[") and v.endswith("]"):
            fm[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        else:
            fm[k] = v.strip('"')
    return fm, m.group(2)


def load_pages():
    pages = {}
    for kind, folder in FOLDERS.items():
        for f in sorted((WIKI / folder).glob("*.md")):
            fm, body = parse(f)
            pages.setdefault(f.stem, []).append({"slug": f.stem, "path": f, "folder": folder, "fm": fm, "body": body})
    return pages


def check_pin(pin, lib, table):
    """'ok', 'unverified' or an error message."""
    label, doc, page, quote, mark = pin
    page = int(page)
    d = lib.get(doc)
    if not d or doc not in table:
        return f"unknown document {doc!r}"
    if d.get("status") != "ingested":
        return f"{doc} is in the inbox: pin it only after it is ingested"
    if not 1 <= page <= d["pages"]:
        return f"{doc} has {d['pages']} PDF pages, not {page}"
    if mark == "⚠":
        return "unverified"
    if not quote:
        return "✓ without a quote"
    if len(norm(ELLIPSIS.sub(" ", quote)).split()) < 3:
        return "quote too short to verify (fewer than 3 words)"
    cite = table[doc]["cite"]
    hits = [p for p in d["passages"] if p["page"] == page and found(quote, p["norm"])]
    if not hits:
        elsewhere = [p for p in d["passages"] if found(quote, p["norm"])]
        if elsewhere:
            return f"quote is not in a passage starting on PDF p. {page}; it is in {pin_text(d, elsewhere[0], cite)}"
        return f"quote not found in {doc}"
    if not any(same_label(label, label_for(p, cite)) for p in hits):
        return f"label {label!r} should be {label_for(hits[0], cite)!r}"
    return "ok"


def check_page(pg, lib, table, slugs, strict=True):
    """Errors, warnings and pin results of one page (no graph checks). Not strict: a link to a page
    not written yet is a warning."""
    errs, warns, pins = [], [], []
    fm, body = pg["fm"], pg["body"]
    if fm is None:
        return ["no frontmatter"], warns, pins
    for k in REQUIRED:
        if k not in fm or fm[k] in ("", None):
            if not (k in ("links", "tags") and fm.get(k) == []):
                errs.append(f"frontmatter: `{k}` missing")
    kind = fm.get("type")
    if kind not in FOLDERS:
        errs.append(f"frontmatter: type {kind!r} is not one of {', '.join(FOLDERS)}")
    elif FOLDERS[kind] != pg["folder"]:
        errs.append(f"a {kind} page belongs in {FOLDERS[kind]}/, not {pg['folder']}/")
    if fm.get("status") not in STATUSES:
        errs.append(f"frontmatter: status {fm.get('status')!r} is not one of {', '.join(STATUSES)}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm.get("updated", ""))):
        errs.append("frontmatter: `updated` is not YYYY-MM-DD")
    reg = fm.get("register") if isinstance(fm.get("register"), list) else []
    if not reg or any(r not in tuple("abcdef") for r in reg):
        errs.append(f"frontmatter: register {fm.get('register')!r} must be a list of letters a–f")
    sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
    if not sources:
        errs.append("no sources")
    for s in sources:
        if s not in table:
            errs.append(f"sources: unknown library id {s!r}")

    found_pins = PIN.findall(body)
    spans = [m.span() for m in PIN.finditer(body)]
    for m in re.finditer(r"\]\(pin:", body):
        if not any(a <= m.start() < b for a, b in spans):
            errs.append(f"malformed pin: {body[body.rfind('[', 0, m.start()):m.start() + 50]!r}")
    pinned = []
    for pin in found_pins:
        res = check_pin(pin, lib, table)
        pins.append((pin, res))
        pinned.append(pin[1])
        if res not in ("ok", "unverified"):
            errs.append(f"pin {pin[0]!r} → {res}")
    for doc in dict.fromkeys(pinned):
        if doc in table and doc not in sources:
            errs.append(f"pins {doc} but `sources` does not list it")
    for s in sources:
        if s in table and s not in pinned and fm.get("status") != "stub":
            warns.append(f"sources lists {s} but no pin uses it")

    pinned_regs = sorted({table[d]["register"] for d in pinned if d in table})
    if kind == "source":
        if len(sources) != 1:
            errs.append("a source page has exactly one id in `sources`: its document")
        elif sources[0] in table and reg != [table[sources[0]]["register"]]:
            errs.append(f"register should be [{table[sources[0]]['register']}] (the document's)")
    elif kind in ("concept", "question") and pinned_regs and sorted(reg) != pinned_regs:
        errs.append(f"register {reg} should be {pinned_regs} (the registers its pins draw on)")

    for card in CARD.findall(body):
        keys = dict(re.findall(r"^(claim|verdict|note): *(.+)$", card, re.M))
        if not keys.get("claim") or not keys.get("note"):
            errs.append("contested card without `claim` or `note`")
        if keys.get("verdict") not in VERDICTS:
            errs.append(f"contested card: verdict {keys.get('verdict')!r} is not one of {', '.join(VERDICTS)}")
        positions = [l for l in card.splitlines() if re.match(r"[+\-−~] ", l)]
        if len(positions) < 2:
            errs.append("contested card with fewer than two positions")
        for line in positions:
            m = re.match(r"([+\-−~]) ([a-f]) \| ", line)
            pm = PIN.match(line, m.end()) if m else None
            rest = line[pm.end():] if pm else ""
            if not (m and pm and re.fullmatch(r" \| [^|]+ \|(?: \[\[[^\]]+\]\])?\s*", rest)):
                errs.append(f"contested position not `sign register | pin | gloss | [[slug]]`: {line[:80]!r}")
            elif pm.group(2) in table and m.group(2) != table[pm.group(2)]["register"]:
                errs.append(f"contested position {pm.group(1)!r}: register {m.group(2)}, but {pm.group(2)} is ({table[pm.group(2)]['register']})")

    for s in LINK.findall(body) + fm.get("links", []):
        if s not in slugs:
            (errs if strict else warns).append(f"dangling link [[{s}]]")
    return errs, warns, pins


def find(pattern, doc, lib, table):
    rx = re.compile(pattern, re.I)
    n = 0
    for d in lib.values():
        if doc and d["id"] != doc:
            continue
        for p in d["passages"]:
            if rx.search(p["text"]):
                n += 1
                inbox = "  [INBOX: do not pin]" if d.get("status") != "ingested" else ""
                print(f"{pin_text(d, p, table.get(d['id'], {}).get('cite', d['id']))}{inbox}\n  § {p['section']}\n  {p['text']}\n")
    print(f"{n} passages")


def pdf_check(results, lib):
    """Each verified quote on its PDF page, letters only (footnote marks and line breaks aside): on the
    page itself, on the next one (a passage that runs over), or split across the two."""
    import fitz   # PyMuPDF
    letters = lambda s: re.sub(r"[^a-z]", "", norm(s).lower())
    text, missing = {}, []
    for (label, doc, page, quote, _), res in results:
        if res != "ok":
            continue
        if doc not in text:
            with fitz.open(ROOT / "site" / lib[doc]["pdf"]) as f:
                text[doc] = [letters(p.get_text()) for p in f]
        pages = text[doc]
        here, nxt = pages[int(page) - 1], pages[int(page)] if int(page) < len(pages) else ""
        for frag in ELLIPSIS.split(quote):
            words = frag.split()
            if words and not any((not letters(" ".join(words[:i])) or letters(" ".join(words[:i])) in here)
                                 and (not letters(" ".join(words[i:])) or letters(" ".join(words[i:])) in (nxt if i else here + nxt))
                                 for i in range(len(words) + 1)):
                missing.append(f"{label} (pin:{doc}#p{page})")
                break
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", nargs="+", metavar="FILE")
    ap.add_argument("--find", metavar="REGEX")
    ap.add_argument("--doc", metavar="ID")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    lib, table = load_library(), library_table()
    for doc in lib:
        if doc not in table:
            print(f"WIKI.md: library document {doc} has no row in the library table")
    if a.find:
        return find(a.find, a.doc, lib, table)
    if a.doc:
        d = lib[a.doc]
        print(f"{d['id']} · {d['kind']} · ({table[d['id']]['register']}) · {d.get('status')} · {d['title']}\n")
        for p in d["passages"]:
            print(f"{pin_text(d, p, table[d['id']]['cite'])}\n  § {p['section']}\n  {p['text']}\n")
        return

    pages = load_pages()
    targets = [load_one(Path(f)) for f in a.check] if a.check else [pg for v in pages.values() for pg in v]
    results, errors, warnings = [], {}, {}
    for pg in targets:
        e, w, pins = check_page(pg, lib, table, pages, strict=not a.check)
        results += pins
        name = f"{pg['folder']}/{pg['slug']}.md"
        if e:
            errors[name] = e
        if w:
            warnings[name] = w

    graph = {}
    if not a.check:
        graph = graph_checks(pages, lib, table)
        for name, msgs in graph.items():
            errors.setdefault(name, []).extend(msgs)

    for name in sorted(set(errors) | set(warnings)):
        print(name)
        for m in errors.get(name, []):
            print(f"  ✗ {m}")
        for m in warnings.get(name, []):
            print(f"  · {m}")
    ok = sum(1 for _, r in results if r == "ok")
    unv = sum(1 for _, r in results if r == "unverified")
    bad = len(results) - ok - unv
    share = 100 * ok / len(results) if results else 0
    print(f"\npins: {len(results)} · ✓ {ok} verified ({share:.1f}%) · ⚠ {unv} unverified · ✗ {bad} failing")
    if a.pdf:
        missing = pdf_check(results, lib)
        print(f"pdf: {ok - len(missing)} of {ok} verified quotes found on the PDF page itself")
        for m in missing:
            print(f"  ? {m}")
    if not a.check:
        counts = {k: sum(1 for v in pages.values() for pg in v if pg["folder"] == f) for k, f in FOLDERS.items()}
        cards = sum(len(CARD.findall(pg["body"])) for v in pages.values() for pg in v)
        lint = {k: sum(1 for msgs in errors.values() for m in msgs if m.startswith(k)) for k in ("dangling", "orphan", "no sources")}
        other = sum(len(m) for m in errors.values()) - sum(lint.values()) - bad
        print(f"lint: {lint['dangling']} dangling links · {lint['orphan']} orphans · {lint['no sources']} pages without sources · {other} other errors")
        print(f"pages: {counts['source']} sources · {counts['concept']} concepts · {counts['entity']} entities · {counts['question']} questions · {cards} contested cards")
    sys.exit(1 if errors or unv or bad else 0)


def load_one(path):
    path = path.resolve()
    fm, body = parse(path)
    return {"slug": path.stem, "path": path, "folder": path.parent.name, "fm": fm, "body": body}


def graph_checks(pages, lib, table):
    """Dangling links from index.md and TENSIONS.md, duplicate slugs, orphans, index coverage, one source
    page per ingested document, and a TENSIONS entry for every contested card."""
    out = {}
    add = lambda name, msg: out.setdefault(name, []).append(msg)
    for slug, v in pages.items():
        if len(v) > 1:
            add(f"{v[0]['folder']}/{slug}.md", f"duplicate slug {slug!r} in {', '.join(pg['folder'] for pg in v)}")
    flat = {slug: v[0] for slug, v in pages.items()}
    inbound = {slug: set() for slug in flat}
    for slug, pg in flat.items():
        for t in LINK.findall(pg["body"]) + (pg["fm"] or {}).get("links", []):
            if t in inbound and t != slug:
                inbound[t].add(slug)
    for slug, pg in flat.items():
        if not inbound[slug]:
            add(f"{pg['folder']}/{slug}.md", "orphan: no other page links here")
    index = (WIKI / "index.md").read_text(encoding="utf-8") if (WIKI / "index.md").exists() else ""
    listed = set(LINK.findall(index))
    for s in sorted(listed - set(flat)):
        add("index.md", f"dangling link [[{s}]]")
    for slug, pg in flat.items():
        if slug not in listed:
            add("index.md", f"page [[{slug}]] is not in the index")
    for doc, d in lib.items():
        own = [s for s, pg in flat.items() if pg["fm"] and pg["fm"].get("type") == "source" and pg["fm"].get("sources") == [doc]]
        if d.get("status") == "ingested" and len(own) != 1:
            add("index.md", f"ingested document {doc} has {len(own)} source pages, not 1")
        if d.get("status") != "ingested" and own:
            add("index.md", f"{doc} is in the inbox but has a source page ({own[0]})")
    tensions = (WIKI / "TENSIONS.md").read_text(encoding="utf-8") if (WIKI / "TENSIONS.md").exists() else ""
    cards = {m for m in re.findall(r"^card: *\[\[([^\]]+)\]\]", tensions, re.M)}
    for s in sorted(set(LINK.findall(tensions)) - set(flat)):
        add("TENSIONS.md", f"dangling link [[{s}]]")
    for s in cards & set(flat):
        if not CARD.search(flat[s]["body"]):
            add("TENSIONS.md", f"card [[{s}]] has no contested block")
    for slug, pg in flat.items():
        if CARD.search(pg["body"]) and slug not in cards:
            add("TENSIONS.md", f"the contested card on [[{slug}]] has no entry")
    return out


if __name__ == "__main__":
    main()
