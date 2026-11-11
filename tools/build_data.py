#!/usr/bin/env python3
"""Build the Workshop Studio data pack (site/data/).

The studio never queries an API on the workshop day: every dataset is built once,
committed, and served from the same origin as the studio. The model only ever sees
site/data/schema.md and a few sample records; the full files go straight into the
participant's preview.

    python3 tools/build_data.py                    # default countries
    python3 tools/build_data.py --countries Kenya,Colombia
    python3 tools/build_data.py --countries all     # every country in UHRI (about 200 files, 250 MB)
    python3 tools/build_data.py --skip-uhri         # rebuild GC + HRC only
    python3 tools/build_data.py --pdf-only          # rebuild the raw PDF text, the library and the wiki only, reuse the rest

Sources
- UHRI+ (cleaned OHCHR Universal Human Rights Index): https://150.254.115.204/uhri-api/
- UN Human Rights Database, General Comments corpus: https://lszoszk.github.io/generalcomments/
- HRC voting records: ~/Desktop/HURIDOCS/OHCHR_voting/data/csv/
- Raw PDF text: CESCR General comment No. 27 (E/C.12/GC/27), the PDF from the UN Official
  Document System, converted with pdftotext (Poppler); needs `pdftotext` on the PATH
- Library: ten documents on neurotechnology in the administration of justice (tools/sources/ and
  the book wiki's UN PDFs), copied to site/files/; passages read with PyMuPDF, each with its PDF
  page and printed page; General Comment paragraphs come from the GC corpus
- Wiki: the research wiki on the library, markdown pages in tools/wiki/ (schema: tools/wiki/WIKI.md),
  every pin checked by tools/wiki_verify.py
"""
import argparse
import csv
import gzip
import json
import re
import ssl
import subprocess
import sys
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data"
UHRI = "https://150.254.115.204/uhri-api/api/data/"
UNHRDB = "https://lszoszk.github.io/generalcomments/"
VOTING = Path.home() / "Desktop/HURIDOCS/OHCHR_voting/data/csv"

# Placeholder set, one per UN region, until GHRH sends the participants' countries.
DEFAULT_COUNTRIES = ["Kenya", "Tunisia", "Colombia", "Philippines", "Georgia", "Switzerland"]
HRC_FROM_YEAR = 2021
SCHEMA_COUNTRY = "Kenya"   # its records give the examples in schema.md, so the model's instructions stay the same
# the document for the extraction exercise; its paragraphs are also in gc.json, which is the reference
PDF_DOC = {"symbol": "E/C.12/GC/27", "doc_id": "e-c-12-gc-27",
           "pdf": Path.home() / "Desktop/GC_Database/new_gcs_pdf/CESCR_GC27.pdf",
           "title": "CESCR General comment No. 27 (2025), as a PDF converter extracted it, page by page"}
# the second document a participant adds to the extraction app: another committee, an older layout
# (reference checked by hand on 4 Nov 2026: paragraphs 1-65 without a gap, last footnote 128)
PDF_DOC_2 = {"symbol": "CCPR/C/GC/32", "doc_id": "ccpr-c-gc-32", "pdf": ROOT / "site/files/CCPR_C_GC_32.pdf",
             "title": "Human Rights Committee general comment No. 32 (2007), as a PDF converter extracted it, page by page"}

# ten General Comments for "Run it on ten" (S8): the extraction app's rules, written on GC 27, run unchanged on
# documents of six committees from 2007 to 2025; PDFs from the UN Official Document System (11 Nov 2026)
TEN_DIR = ROOT / "tools/out/gc_pdfs"
PDF_TEN = [
    ("E/C.12/GC/27", Path.home() / "Desktop/GC_Database/new_gcs_pdf/CESCR_GC27.pdf"),
    ("CCPR/C/GC/32", ROOT / "site/files/CCPR_C_GC_32.pdf"),
    ("CCPR/C/GC/34", TEN_DIR / "CCPR_C_GC_34.pdf"),
    ("CCPR/C/GC/36", TEN_DIR / "CCPR_C_GC_36.pdf"),
    ("E/C.12/GC/24", TEN_DIR / "E_C_12_GC_24.pdf"),
    ("E/C.12/GC/25", TEN_DIR / "E_C_12_GC_25.pdf"),
    ("CRC/C/GC/25", TEN_DIR / "CRC_C_GC_25.pdf"),
    ("CRPD/C/GC/7", TEN_DIR / "CRPD_C_GC_7.pdf"),
    ("CAT/C/GC/4", TEN_DIR / "CAT_C_GC_4.pdf"),
    ("CEDAW/C/GC/35", TEN_DIR / "CEDAW_C_GC_35.pdf"),
]

# the same document as OHCHR publishes it in HTML (English html link on its Download.aspx page, fetched on
# 4 Nov 2026): every numbered paragraph is its own <p>, headings are <h2>/<h3>, and the footnotes are gone
HTML_DOC = {"symbol": "E/C.12/GC/27", "doc_id": "e-c-12-gc-27", "html": ROOT / "site/files/E_C.12_GC_27.html",
            "title": "CESCR General comment No. 27 (2025), as OHCHR publishes it in HTML",
            "source": "The HTML version on the OHCHR treaty body database (tbinternet.ohchr.org, Download.aspx); embedded images and styles removed, nothing else changed"}


def ssl_context():
    # python.org builds on macOS ship without a CA bundle; fall back to the system one
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        cafile = "/etc/ssl/cert.pem"
        return ssl.create_default_context(cafile=cafile if Path(cafile).exists() else None)


CTX = ssl_context()


def get_json(url):
    req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip", "User-Agent": "workshop-studio-build"})
    with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
    return json.loads(raw)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()   # Côte d'Ivoire -> cote-d-ivoire
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def strip_dash(s):
    return (s or "").removeprefix("- ").strip()


def mechanism(body):
    if body == "UPR":
        return "Universal Periodic Review"
    if re.match(r"^(SR|IE|WG) ", body):
        return "Special Procedures"
    return "Treaty bodies"


SDG_GOALS = {
    1: "No poverty", 2: "Zero hunger", 3: "Good health and well-being", 4: "Quality education",
    5: "Gender equality", 6: "Clean water and sanitation", 7: "Affordable and clean energy",
    8: "Decent work and economic growth", 9: "Industry, innovation and infrastructure",
    10: "Reduced inequalities", 11: "Sustainable cities and communities",
    12: "Responsible consumption and production", 13: "Climate action", 14: "Life below water",
    15: "Life on land", 16: "Peace, justice and strong institutions", 17: "Partnerships for the goals",
}


def sdgs(labels):
    """UHRI mixes goals ("16 - PEACE, ...") and targets ("16.3 - Promote ...").
    Returns (goals, targets); a target also counts towards its goal."""
    goals, targets = [], []
    for s in labels:
        m = re.match(r"^\s*(\d+)(?:\.(\w+))?\s*-\s*(.+)$", s)
        if not m:
            continue
        g, t, label = int(m.group(1)), m.group(2), m.group(3).strip()
        if t:
            targets.append(f"{g}.{t}: {label}")
        if g not in goals:
            goals.append(g)
    return goals, targets


def annotation_type(s):
    s = strip_dash(s)
    # a few UHRI type labels are bare UUIDs or empty
    return s if s and s != "-" and not re.fullmatch(r"[0-9a-f-]{36}", s) else "Other"


def uhri_country(country):
    records, page = [], 1
    while True:
        q = urllib.parse.urlencode({"countries": country, "page": page, "page_size": 1000})
        d = get_json(UHRI + "records?" + q)
        records += d["records"]
        if page >= d["total_pages"]:
            break
        page += 1
    out = []
    for r in records:
        body = strip_dash(r.get("Body"))
        goals, targets = sdgs(r.get("Sdgs") or [])
        day = (r.get("PublicationDate") or "")[:10]
        out.append({
            "id": r["AnnotationId"],
            "symbol": r["Symbol"],
            "doc_url": "https://docs.un.org/en/" + r["Symbol"],
            "date": day,
            "year": int(day[:4]) if day else None,
            "body": body,
            "mechanism": mechanism(body),
            "type": annotation_type(r.get("AnnotationType")),
            "section": (r.get("SectionHeadings") or [""])[0],
            "text": r.get("TextPlainCleaned") or r.get("TextPlainRaw") or "",
            "themes": r.get("Themes") or [],
            "sdgs": goals,
            "sdg_targets": targets,
            "affected_persons": r.get("AffectedPersons") or [],
            "countries": r.get("Countries") or [],
        })
    out.sort(key=lambda x: (x["date"], x["symbol"]), reverse=True)
    # the country's UN regional group, from the records addressed to it alone
    regions = Counter(g for r in records if (r.get("Countries") or []) == [country] for g in r.get("Regions") or [])
    return {
        "dataset": "uhri",
        "title": f"UN human rights recommendations and observations addressed to {country}",
        "country": country,
        "region": regions.most_common(1)[0][0] if regions else None,
        "source": "OHCHR Universal Human Rights Index (uhri.ohchr.org), cleaned as UHRI+ by Ł. Szoszkiewicz",
        "source_url": "https://uhri.ohchr.org",
        "built": date.today().isoformat(),
        "count": len(out),
        "sdg_names": {},  # filled in main() once every country has been read
        "records": out,
    }


def gc_corpus():
    paras = get_json(UNHRDB + "corpus.json")
    docs = {d["docId"]: d for d in get_json(UNHRDB + "documents.json")}
    out = []
    for p in paras:
        d = docs.get(p["docId"], {})
        out.append({
            "id": p["id"],
            "symbol": d.get("signature", ""),
            "paragraph": p.get("n"),
            "committee": p.get("committee"),
            "year": p.get("year"),
            "title": d.get("name", ""),
            "short_title": d.get("nameShort", ""),
            "doc_url": d.get("link", ""),
            "text": p.get("text", ""),
            "cited_articles": [f"{a['treaty']} art. {a['article']}" for a in p.get("citedArticles") or []],
        })
    return {
        "dataset": "gc",
        "title": "General Comments and General Recommendations of the UN treaty bodies, paragraph by paragraph",
        "source": "UN Human Rights Database (lszoszk.github.io/generalcomments), from OHCHR documents",
        "source_url": "https://lszoszk.github.io/generalcomments/",
        "built": date.today().isoformat(),
        "count": len(out),
        "records": out,
    }


def pdf_text(gc, doc_spec=PDF_DOC, key="pdf_text"):
    """One UN document exactly as a PDF converter gives it, page by page, nothing cleaned: the raw
    material for the extraction exercise. `reference` holds only what an app needs to check its
    own result against the paragraphs of the same document in the UN Human Rights Database."""
    raw = subprocess.run(["pdftotext", str(doc_spec["pdf"]), "-"], capture_output=True, text=True, check=True).stdout
    pages = raw.split("\f")
    while pages and not pages[-1].strip():
        pages.pop()
    paras = sorted((r for r in gc["records"] if r["symbol"] == doc_spec["symbol"]), key=lambda r: int(r["paragraph"]))
    first = {str(r["paragraph"]): " ".join(re.sub(r"^\d+\.\s*", "", r["text"]).split()[:6]) for r in paras}
    notes = sum(len(p.get("footnotes") or []) for p in get_json(UNHRDB + "corpus.json") if p.get("docId") == doc_spec["doc_id"])
    doc = next(d for d in get_json(UNHRDB + "documents.json") if d.get("docId") == doc_spec["doc_id"])
    return {
        "dataset": key,
        "title": doc_spec["title"],
        "symbol": doc_spec["symbol"],
        "doc_url": "https://docs.un.org/en/" + doc_spec["symbol"],
        "source": "The PDF from the UN Official Document System, converted with pdftotext (Poppler); nothing cleaned",
        "built": date.today().isoformat(),
        "count": len(pages),
        "records": [{"page": i + 1, "text": t} for i, t in enumerate(pages)],
        "reference": {"paragraphs": len(paras), "footnotes": notes, "adopted": doc.get("adoptionDate"), "first_words": first},
    }


def pdf_ten(gc):
    """Ten documents in the shape of pdf_text, one record each: its pages as the same converter gives them and
    its `reference` from the UN Human Rights Database, so the app's checks run on every one of them."""
    corpus, docs = get_json(UNHRDB + "corpus.json"), get_json(UNHRDB + "documents.json")
    out = []
    for symbol, pdf in PDF_TEN:
        raw = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
        pages = raw.split("\f")
        while pages and not pages[-1].strip():
            pages.pop()
        paras = sorted((r for r in gc["records"] if r["symbol"] == symbol), key=lambda r: int(r["paragraph"]))
        doc_id = symbol.lower().replace("/", "-").replace(".", "-")
        doc = next((d for d in docs if d.get("docId") == doc_id), {})
        out.append({
            "symbol": symbol, "committee": paras[0]["committee"], "year": paras[0]["year"],
            "title": paras[0]["short_title"].strip(), "doc_url": "https://docs.un.org/en/" + symbol, "count": len(pages),
            "pages": [{"page": i + 1, "text": t} for i, t in enumerate(pages)],
            "reference": {"paragraphs": len(paras),
                          # the database has no footnotes for some documents (CCPR/C/GC/36): null, not 0
                          "footnotes": sum(len(p.get("footnotes") or []) for p in corpus if p.get("docId") == doc_id) or None,
                          "adopted": doc.get("adoptionDate"),
                          "first_words": {str(r["paragraph"]): " ".join(re.sub(r"^\d+\.\s*", "", r["text"]).split()[:6]) for r in paras}},
        })
        print(f"  {symbol}: {len(pages)} pages, {len(paras)} paragraphs, {out[-1]['reference']['footnotes']} footnotes")
    return {"dataset": "pdf_ten", "title": "Ten General Comments, as a PDF converter extracted them, page by page",
            "source": "The PDFs from the UN Official Document System, converted with pdftotext (Poppler); nothing cleaned",
            "built": date.today().isoformat(), "count": len(out), "records": out}


def ten_schema(p):
    first = p["records"][0]
    return [
        "## `WORKSHOP_DATA.pdf_ten`: ten UN documents as raw text from their PDFs",
        "",
        "`{title, source, built, count, records: [{symbol, committee, year, title, doc_url, count, pages: [{page, text}], reference: {...}}]}`.",
        f"`records` are {p['count']} General Comments of six treaty bodies, one record per document: `pages` holds",
        "its pages exactly as the converter of `pdf_text` produced them, nothing cleaned, and `reference` has the",
        "same fields as in `pdf_text` (`paragraphs`, `footnotes`, `adopted`, `first_words`), from the UN Human Rights",
        "Database; `footnotes` is null where the database records none. The documents differ in layout: a rule written",
        f"on one may break on another. The first is {first['symbol']}, the same document as `pdf_text`.",
        "",
    ]


def html_doc(gc, doc_spec=HTML_DOC, key="html_doc"):
    """One UN document as OHCHR's HTML: the body as published (embedded images and styles removed), and the same
    `reference` as pdf_text, from the paragraphs of the same document in the UN Human Rights Database."""
    page = doc_spec["html"].read_text(encoding="utf-8")
    body = page[page.index("<body"):page.rindex("</body>") + len("</body>")]
    body = re.sub(r'src="data:[^"]*"', 'src=""', body)
    body = re.sub(r'href="data:[^"]*"', 'href=""', body)
    paras = sorted((r for r in gc["records"] if r["symbol"] == doc_spec["symbol"]), key=lambda r: int(r["paragraph"]))
    first = {str(r["paragraph"]): " ".join(re.sub(r"^\d+\.\s*", "", r["text"]).split()[:6]) for r in paras}
    notes = sum(len(p.get("footnotes") or []) for p in get_json(UNHRDB + "corpus.json") if p.get("docId") == doc_spec["doc_id"])
    doc = next(d for d in get_json(UNHRDB + "documents.json") if d.get("docId") == doc_spec["doc_id"])
    return {
        "dataset": key,
        "title": doc_spec["title"],
        "symbol": doc_spec["symbol"],
        "doc_url": "https://docs.un.org/en/" + doc_spec["symbol"],
        "source": doc_spec["source"],
        "built": date.today().isoformat(),
        "count": 1,
        "html": body,
        "reference": {"paragraphs": len(paras), "footnotes": notes, "adopted": doc.get("adoptionDate"), "first_words": first},
    }


def html_schema(p):
    return [
        "## `WORKSHOP_DATA.html_doc`: one UN document as OHCHR publishes it in HTML",
        "",
        "`{title, symbol, doc_url, source, html, reference: {...}}`.",
        f"`html` is the `<body>` of {p['symbol']} exactly as OHCHR's HTML version has it (a string; parse it",
        "with `new DOMParser().parseFromString(html, 'text/html')`). Each numbered paragraph is a `<p>` whose",
        "text starts with its number and a full stop, often with no space after it (\"1.The …\"); headings",
        "are `<h2>` and `<h3>`; the cover lines (symbol, distribution, date) are `<p>` elements before the",
        "first heading. The footnotes of the published document are not in this HTML at all.",
        "`reference` lets an app check its own result: `paragraphs` (how many numbered paragraphs",
        "the document has), `footnotes` (how many footnotes the document has, in its PDF and Word versions),",
        f"`adopted`, and `first_words` (`{{\"1\": \"{p['reference']['first_words']['1']}\", …}}`: the first six words",
        "of each numbered paragraph).",
        "",
    ]


# the library for the wiki exercise: neurotechnology in the administration of justice, ten documents
# of six kinds. `offset` turns a PDF page into the page number printed on it (the one to cite).
SOURCES = ROOT / "tools/sources"
UN_PDFS = Path.home() / "Desktop/The Book/00_PROJECT/wiki/sources/un-pdfs"
LIBRARY = [
    {"id": "A/81/351", "symbol": "A/81/351", "kind": "UN report", "author": "UN Secretary-General",
     "title": "Human rights in the administration of justice: report of the Secretary-General",
     "short_title": "Secretary-General's report on human rights in the administration of justice",
     "published": "2026-08-27", "year": 2026, "url": "https://docs.un.org/en/A/81/351",
     "pdf_src": SOURCES / "A_81_351.pdf", "numbered": True, "skip": {1}},
    {"id": "UNODC-INTERPOL-2025", "symbol": None, "kind": "UN agency paper", "author": "UNODC and INTERPOL",
     "title": "Neurotechnology, Law Enforcement and Criminal Justice: background paper",
     "short_title": "UNODC–INTERPOL background paper on neurotechnology and criminal justice",
     "published": "2025-10", "year": 2025,
     "url": "https://www.interpol.int/How-we-work/Innovation/INTERPOL-UNODC-Neurotechnology-assessment",
     "pdf_src": SOURCES / "UNODC_INTERPOL_2025.pdf", "offset": -3, "skip": {1, 2, 3},
     "rights": "© United Nations, October 2025. All rights reserved."},
    {"id": "FuturesLab-2026", "symbol": None, "kind": "Civil-society submission",
     "author": "Futures Lab for Democracy, Tech & Human Rights, American University",
     "title": "Neurotechnology and the Administration of Justice: submission to OHCHR for the report of the Secretary-General under resolution 79/172",
     "short_title": "Futures Lab submission to the Secretary-General's report",
     "published": "2026-03-09", "year": 2026,
     "url": "https://www.ohchr.org/en/calls-for-input/2026/call-input-human-rights-administration-justice-neurotechnology-and-other",
     "pdf_src": SOURCES / "FuturesLab_2026.pdf", "offset": -1, "skip": {1}, "drop_heads": r"HUMAN RIGHTS|F ?UTURES"},
    {"id": "AHRC-2025", "symbol": None, "kind": "National human rights institution report",
     "author": "Australian Human Rights Commission",
     "title": "Peace of Mind: Navigating the Ethical Frontiers of Neurotechnology and Human Rights",
     "short_title": "Peace of Mind (Australian Human Rights Commission)",
     "published": "2025-10", "year": 2025,
     "url": "https://humanrights.gov.au/resource-hub/search-all-our-publications/reports-and-projects/reports/technology-and-human-rights/peace-of-mind-new-report-explores-neurotechnology-and-human-rights",
     "pdf_src": SOURCES / "AHRC_PeaceOfMind_2025.pdf", "compress": True, "skip": {1, 2, 3, 4, 5},
     "rights": "CC BY 4.0"},
    {"id": "Szoszkiewicz-Yuste-2025", "symbol": None, "kind": "Journal article",
     "author": "Łukasz Szoszkiewicz and Rafael Yuste",
     "title": "Mental privacy: navigating risks, rights and regulation",
     "short_title": "Mental privacy (EMBO Reports)", "journal": "EMBO Reports 26: 3469–3473",
     "published": "2025-07", "year": 2025, "url": "https://doi.org/10.1038/s44319-025-00505-6",
     "pdf_src": SOURCES / "EMBO_2025.pdf", "offset": 3468, "rights": "CC BY 4.0",
     "drop_heads": r"✉|Science & Society|^Mental privacy|^and regulation$|^Advances in neuroscience"},
    {"id": "Prainsack-et-al-2022", "symbol": None, "kind": "Journal article",
     "author": "Barbara Prainsack, Seliem El-Sayed, Nikolaus Forgó, Łukasz Szoszkiewicz and Philipp Baumer",
     "title": "Data solidarity: a blueprint for governing health futures",
     "short_title": "Data solidarity (The Lancet Digital Health)", "journal": "The Lancet Digital Health 4: e773–e774",
     "published": "2022-11", "year": 2022, "url": "https://doi.org/10.1016/S2589-7500(22)00189-3",
     "pdf_src": SOURCES / "Lancet_DH_2022.pdf", "offset": 772, "label": "e{}", "rights": "CC BY-NC-ND 4.0",
     "drop_heads": r"^Comment$|^Data solidarity: a blueprint"},
    {"id": "CCPR/C/21/Rev.1/Add.4", "symbol": "CCPR/C/21/Rev.1/Add.4", "gc_symbol": "CCPR/C/21/Rev.1/Add. 4",
     "kind": "General Comment", "pdf_src": UN_PDFS / "CCPR_C_21_Rev.1_Add.4.pdf"},
    {"id": "CCPR/C/GC/32", "symbol": "CCPR/C/GC/32", "kind": "General Comment", "pdf_src": UN_PDFS / "CCPR_C_GC_32.pdf"},
    {"id": "CCPR/C/GC/34", "symbol": "CCPR/C/GC/34", "kind": "General Comment", "pdf_src": UN_PDFS / "CCPR_C_GC_34.pdf"},
    # in the library but not yet in the wiki: the source for the live ingest. Its annex (pp. 21-23,
    # circulated as received, numbered from 1 again) is left out of the passages.
    {"id": "A/HRC/57/61", "symbol": "A/HRC/57/61", "kind": "UN report", "author": "Human Rights Council Advisory Committee",
     "title": "Impact, opportunities and challenges of neurotechnology with regard to the promotion and protection of all human rights: report of the Human Rights Council Advisory Committee",
     "short_title": "Advisory Committee report on neurotechnology and human rights",
     "published": "2024-08-08", "year": 2024, "url": "https://docs.un.org/en/A/HRC/57/61",
     "pdf_src": SOURCES / "A_HRC_57_61.pdf", "numbered": True, "skip": {1, 21, 22, 23}, "status": "inbox"},
]
PASSAGE_END = tuple('.!?:;"”’)')


def _norm(s):
    s = re.sub(r"\[\[fn:\d+\]\]", " ", s)
    s = re.sub(r"-\n", "", s)                 # a word broken at the end of a line
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _clean(s):
    s = unicodedata.normalize("NFKC", s).replace("­", "")
    return re.sub(r"\s+", " ", s).strip()


def _pdf_lines(path, numbered):
    """Every visual line of a PDF with its page, block, and kind: body (the document's most common
    font size), head (larger, or a short bold line) or small (footnotes, captions, references)."""
    import fitz   # PyMuPDF
    doc = fitz.open(path)
    sizes = Counter()
    for p in doc:
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    sizes[round(s["size"])] += len(s["text"].strip())
    body = sizes.most_common(1)[0][0]
    rows = []
    for n, p in enumerate(doc, 1):
        for bi, b in enumerate(p.get_text("dict")["blocks"]):
            blk = []
            for l in b.get("lines", []):
                spans = [s for s in l["spans"] if s["text"].strip()]
                if not spans:
                    continue
                size = Counter()
                for s in spans:
                    size[round(s["size"])] += len(s["text"].strip())
                sz = size.most_common(1)[0][0]
                # footnote marks raised inside a body line go
                text = _clean("".join(s["text"] for s in l["spans"] if not (
                    sz == body and (s["flags"] & 1 or s["size"] < body * 0.8) and re.fullmatch(r"\s*\d{1,3}\s*", s["text"]))))
                if not text:
                    continue
                bold = sum(len(s["text"].strip()) for s in spans if "Bold" in s["font"] or s["flags"] & 16)
                x0, y0, x1, y1 = l["bbox"]
                last = blk[-1] if blk else None
                if last and abs((y0 + y1) / 2 - last["y"]) < 2.5 and x0 > last["x1"] - 1 and sz == last["size"]:
                    last.update(text=last["text"] + " " + text, bold=last["bold"] + bold, x1=x1)   # justified text, split into words
                    continue
                blk.append({"text": text, "size": sz, "bold": bold, "x0": x0, "x1": x1, "y": (y0 + y1) / 2})
            if not blk:
                continue
            chars = sum(len(r["text"]) for r in blk)
            bold_share = sum(r["bold"] for r in blk) / max(1, chars)
            left = min(r["x0"] for r in blk)
            for r in blk:
                text, sz = r["text"], r["size"]
                is_bold = r["bold"] > len(text.replace(" ", "")) / 2
                if (re.search("[A-Za-z]{2}", text) or re.fullmatch("[A-Z]", text)) and sz > body or (
                        sz == body and is_bold and len(text) < 90 and (bold_share < 0.6 or chars < 160)
                        and re.match(r"[A-Z0-9]", text) and not (numbered and re.match(r"\(?[a-z0-9]{1,3}[.)]", text))):
                    kind = "head"
                else:
                    kind = "body" if sz == body else "small"
                rows.append((n, bi, text, kind, r["x0"] - left > 6))
    return rows, len(doc)


def pdf_passages(path, numbered=False, skip=(), drop_heads=None):
    """The body text of a PDF as passages, each with the page it starts on and the heading above it.
    Dropped: smaller print (footnotes, captions, references), lines repeated on many pages (running
    heads), page numbers, contents lines and pull quotes. In a numbered document a passage is a
    numbered paragraph or one of its lettered sub-paragraphs; elsewhere it is a printed paragraph."""
    rows, pages = _pdf_lines(path, numbered)
    seen = Counter(re.sub(r"\d+", "#", r[2]) for r in rows)
    running = {k for k, v in seen.items() if v >= max(3, pages // 3) and len(k) < 120 and re.search("[A-Za-z]", k)}
    out, cur, section, last_head, para, dropcap, quote_block = [], None, None, None, 0, "", None
    for n, bi, text, kind, indent in rows:
        if (n in skip or kind == "small" or re.sub(r"\d+", "#", text) in running
                or re.fullmatch(r"[\d/ e\-–]+", text) or re.search(r"\.{5,}|…{3,}", text)):
            continue
        if kind == "head":
            if re.fullmatch(r"[A-Z]", text):   # a drop cap: the first letter of the next paragraph
                dropcap = text
            elif re.match(r"[“\"]", text) or quote_block == (n, bi):   # a pull quote: the whole block goes
                quote_block = (n, bi)
            elif not (drop_heads and re.search(drop_heads, text)) and len(text) < 140:
                section = section + " " + text if last_head == (n, bi) else text
                last_head = (n, bi)
            continue
        label = None
        if numbered:   # a paragraph number (only the next one in sequence counts), or a lettered sub-paragraph
            m = re.match(r"(\d{1,3})\.(?:\s+(.*))?$", text)
            if m and int(m.group(1)) == para + 1:
                para, label, text = para + 1, str(para + 1), m.group(2) or ""
            else:
                m = re.match(r"\(([a-z]{1,2})\)(?:\s+(.*))?$", text)
                if m and para and cur and (cur["text"].endswith(":") or cur["paragraph"] != str(para)):
                    label, text = f"{para} ({m.group(1)})", m.group(2) or ""
        if label or cur is None:
            starts = True
        elif numbered:
            starts = cur["paragraph"] is None and (n, bi) != cur["_block"] and cur["text"].endswith(PASSAGE_END)
        else:
            starts = (((n, bi) != cur["_block"] or indent)
                      and (not re.match(r"[a-z]", text) or re.match(r"(?:[ivx]+|[a-z])[.)] ", text))   # a break mid-sentence, unless a list item
                      and not re.search(r"[a-z,-]$", cur["text"]))
        if starts:
            if cur:
                out.append(cur)
            cur = {"page": n, "paragraph": label, "section": section, "text": "", "_block": (n, bi)}
        cur["_block"] = (n, bi)
        if dropcap and re.match(r"[a-z]", text):
            text, dropcap = dropcap + text, ""
        if text:
            if not cur["text"]:
                cur["text"] = text
            elif re.search(r"[a-z]-$", cur["text"]) and re.match(r"[a-z]", text):   # a word broken at the end of a line
                cur["text"] = cur["text"][:-1] + text
            else:
                cur["text"] += " " + text
    if cur:
        out.append(cur)
    for c in out:
        del c["_block"]
    if out and re.match(r"[a-z]", out[0]["text"]):   # the end of a sentence from a skipped page
        out.pop(0)
    return [c for c in out if len(c["text"].split()) >= 12 or (c["paragraph"] and c["text"])]


def gc_passages(path, recs):
    """The paragraphs of a General Comment from the GC corpus, each placed on the PDF page where its
    first words are found (looking from the page of the paragraph before)."""
    raw = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True).stdout
    pages = [_norm(t) for t in raw.split("\f")]
    out, at, missed = [], 0, 0
    for r in sorted(recs, key=lambda r: r.get("paragraph") or 0):
        words = _norm(re.sub(r"^\s*\d+\.\s*", "", r["text"])).split()
        page = None
        for k in (8, 5):
            key = " ".join(words[:k])
            if not key:
                break
            page = next((i for i in range(at, len(pages)) if key in pages[i]), None)
            if page is not None:
                break
        if page is None:
            missed += 1
            page = at       # not found as typed (a table, a broken line): the page of the paragraph before
        at = page
        out.append({"page": page + 1, "paragraph": str(r["paragraph"]), "section": None,
                    "text": re.sub(r"^\s*\d+\.\s*", "", r["text"]).strip()})
    return out, missed


def library(gc):
    """Ten documents on neurotechnology in the administration of justice, as PDFs plus their text
    passage by passage, each passage with the PDF page it starts on (to open) and the page number
    printed there (to cite). The PDFs are copied to site/files/."""
    files = ROOT / "site/files"
    files.mkdir(exist_ok=True)
    keep = {PDF_DOC["symbol"].replace("/", "_") + ".pdf"}
    docs = []
    for d in LIBRARY:
        meta = {k: v for k, v in d.items() if k not in ("pdf_src", "numbered", "skip", "drop_heads", "offset", "label", "compress", "gc_symbol")}
        meta.setdefault("status", "ingested")   # "inbox": in the library, not yet in the wiki
        name = d["id"].replace("/", "_") + ".pdf"
        keep.add(name)
        if d.get("compress"):   # an 8 MB report: images down to screen quality, text untouched
            subprocess.run(["gs", "-q", "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dBATCH",
                            f"-sOutputFile={files / name}", str(d["pdf_src"])], check=True, capture_output=True)
        else:
            (files / name).write_bytes(d["pdf_src"].read_bytes())
        if d["kind"] == "General Comment":
            recs = [r for r in gc["records"] if r["symbol"] == d.get("gc_symbol", d["symbol"])]
            first = recs[0]
            meta.update(author="Human Rights Committee", title=first["title"], short_title=first["short_title"],
                        published=str(first["year"]), year=first["year"], url="https://docs.un.org/en/" + d["symbol"])
            ps, missed = gc_passages(d["pdf_src"], recs)
            if missed:
                print(f"  {d['id']}: {missed} paragraphs placed by the page before")
        else:
            ps = pdf_passages(d["pdf_src"], d.get("numbered", False), d.get("skip", ()), d.get("drop_heads"))
        for i, p in enumerate(ps, 1):
            printed = p["page"] + d.get("offset", 0)
            p["page_label"] = d.get("label", "{}").format(printed)
            p["id"] = f"{d['id']}#{i}"
        meta.update(pdf="files/" + name, pages=_page_count(d["pdf_src"]),
                    passages=[{k: p[k] for k in ("id", "page", "page_label", "paragraph", "section", "text")} for p in ps])
        docs.append(meta)
        print(f"  {d['id']}: {len(ps)} passages")
    for f in files.glob("*.pdf"):   # the library of an earlier build
        if f.name not in keep:
            f.unlink()
    return {
        "dataset": "library",
        "title": "A research library on neurotechnology in the administration of justice: ten documents, passage by passage, with pages",
        "source": "The documents' own PDFs (UN, UNODC and INTERPOL, a civil-society submission, a national human rights institution, "
                  "two journal articles, three General Comments); General Comment paragraphs from the UN Human Rights Database",
        "built": date.today().isoformat(),
        "count": len(docs),
        "records": docs,
    }


def _page_count(path):
    import fitz
    with fitz.open(path) as doc:
        return len(doc)


# the research wiki on the library: markdown pages written by language models before the workshop
# (schema in tools/wiki/WIKI.md, every pin checked by tools/wiki_verify.py)
WIKI_SRC = ROOT / "tools/wiki"
WIKI_SAMPLES = ("moratorium", "selvi-v-state-of-karnataka")   # a concept with a contested card, and an entity


def wiki():
    from wiki_verify import FOLDERS, parse
    pages = []
    for folder in FOLDERS.values():
        for f in sorted((WIKI_SRC / folder).glob("*.md")):
            fm, body = parse(f)
            pages.append({"slug": f.stem, "type": fm["type"], "title": fm["title"], "frontmatter": fm, "body": body.strip() + "\n"})
    read = lambda name: (WIKI_SRC / name).read_text(encoding="utf-8")
    return {
        "dataset": "wiki",
        "title": "A research wiki on neurotechnology in the administration of justice, kept by language models on the library",
        "source": "Pages written by Claude Fable 5.1 agents from nine of the library's documents, each claim pinned to a passage "
                  "and checked against it by tools/wiki_verify.py",
        "built": date.today().isoformat(),
        "count": len(pages),
        "schema": read("WIKI.md"),
        "pages": pages,
        "index": read("index.md"),
        "log": read("log.md"),
        "tensions": read("TENSIONS.md"),
    }


def agenda(s):
    s = (s or "").strip().rstrip(".")
    return f"Item {s}" if s.isdigit() else s.title()


def split_outside_parens(s):
    parts, depth, cur = [], 0, ""
    for ch in s or "":
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return [p for p in parts if p]


def hrc_votes():
    res = [r for r in csv.DictReader(open(VOTING / "resolutions.csv", encoding="utf-8"))
           if r["body"] == "Human Rights Council" and r["vote_type"] == "RECORDED" and int(r["year"]) >= HRC_FROM_YEAR]
    keep = {r["record_id"] for r in res}  # amendments share the resolution's symbol
    votes, names = {}, {}
    for v in csv.DictReader(open(VOTING / "votes_long.csv", encoding="utf-8")):
        if v["record_id"] in keep and v["vote"] in ("Y", "N", "A"):
            votes.setdefault(v["record_id"], {})[v["iso3"]] = v["vote"]
            names[v["iso3"]] = v["country"].title()
    out = []
    for r in res:
        out.append({
            "id": r["record_id"],
            "symbol": r["symbol"],
            "kind": "amendment" if re.search(r":\s*amendment\s*/?\s*$", r["title"]) else "resolution",
            "title": re.sub(r"\s*:\s*(resolution|amendment)\s*/?\s*$", "", r["title"]).strip(" :/"),
            "date": r["date"],
            "year": int(r["year"]),
            "session": r["statement"].replace("adopted by the Human Rights Council at its ", ""),
            "agenda_item": agenda(r["agenda_item_no"]),
            "main_sponsors": split_outside_parens(r["main_sponsors"]),
            "yes": int(r["yes"] or 0), "no": int(r["no"] or 0), "abstain": int(r["abstain"] or 0),
            "doc_url": r["url_resolution"],
            "record_url": r["record_url"],
            "votes": votes.get(r["record_id"], {}),
        })
    out.sort(key=lambda x: x["date"], reverse=True)
    return {
        "dataset": "hrc",
        "title": f"Human Rights Council resolutions adopted by recorded vote, {HRC_FROM_YEAR} onwards",
        "source": "OHCHR voting records (searchlibrary.ohchr.org), compiled by Ł. Szoszkiewicz",
        "source_url": "https://lszoszk.github.io/hrc-voting/",
        "built": date.today().isoformat(),
        "count": len(out),
        "countries": dict(sorted(names.items())),
        "vote_codes": {"Y": "yes", "N": "no", "A": "abstain"},
        "records": out,
    }


def write(name, obj):
    path = OUT / name
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"  {name:28} {obj['count']:>6} records  {path.stat().st_size / 1e6:5.1f} MB")
    return path


def describe(obj, keep=3):
    """A compact, model-facing description: field list with example values, never the data itself."""
    rec = obj["records"]
    fields = []
    for k, v in rec[0].items():
        if isinstance(v, list):
            vals = Counter(x for r in rec for x in (r.get(k) or []))
            ex = ", ".join(json.dumps(x, ensure_ascii=False) for x, _ in vals.most_common(4)) if vals else "…"
            fields.append(f"- `{k}` (list): e.g. {ex}")
        elif isinstance(v, dict):
            fields.append(f"- `{k}` (object): e.g. {json.dumps(dict(list(v.items())[:3]))}")
        else:
            fields.append(f"- `{k}` ({type(v).__name__}): e.g. {json.dumps(v, ensure_ascii=False)[:90]}")
    return fields


def schema(packs):
    u = packs.get("uhri")
    lines = [
        "# Data available in the preview",
        "",
        "The app runs in a sandboxed page with NO network access. All data is already loaded",
        "in the global object `window.WORKSHOP_DATA` before your script runs. Never use fetch(),",
        "never ask the user to upload anything, never invent records.",
        "",
    ]
    if u:
        bodies = Counter(r["mechanism"] for r in u["records"])
        lines += [
            "## `WORKSHOP_DATA.uhri`: recommendations to the participant's country",
            "",
            "`{country, title, source, source_url, built, count, records: [...]}`. One record = one",
            "paragraph from a UN document (UPR report, treaty-body concluding observations,",
            "Special Procedures report). The country differs per participant: read",
            "`WORKSHOP_DATA.uhri.country`, never hard-code it.",
            "",
            "Fields:",
            *describe(u),
            "",
            f"`mechanism` is one of: {', '.join(f'\"{k}\"' for k in bodies)}.",
            "`type` is mostly \"Recommendations\" or \"Concerns/Observations\".",
            "UPR recommendations end with the recommending State in parentheses, e.g.",
            "\"…for all children (Croatia).\" A regex on the last parentheses extracts it.",
            "`sdgs` holds goal numbers (1–17); names are in `WORKSHOP_DATA.uhri.sdg_names`",
            "(`{\"16\": \"Peace, justice and strong institutions\", …}`). `sdg_targets` holds",
            "target labels such as \"16.3: Promote the rule of law…\".",
            "A record can carry several themes and several SDGs, or none.",
            "",
        ]
    if "gc" in packs:
        lines += [
            "## `WORKSHOP_DATA.gc`: General Comments, paragraph by paragraph",
            "",
            "`{title, source, count, records: [...]}`. Cite as `symbol, para. paragraph`.",
            "",
            "Fields:",
            *describe(packs["gc"]),
            "",
        ]
    if "hrc" in packs:
        lines += [
            "## `WORKSHOP_DATA.hrc`: Human Rights Council recorded votes",
            "",
            "`{title, count, countries: {ISO3: name}, vote_codes: {Y,N,A}, records: [...]}`.",
            "`votes` maps ISO3 codes of the 47 Council members to \"Y\", \"N\" or \"A\".",
            "`kind` is \"resolution\" or \"amendment\" (a recorded vote on an amendment to a draft).",
            "`yes`/`no`/`abstain` are the official totals. Counting `votes` gives the roll call,",
            "which differs from the totals for a few records (gaps in the source): show both",
            "rather than silently picking one.",
            "",
            "Fields:",
            *describe(packs["hrc"]),
            "",
        ]
    if "library" in packs:
        lib = packs["library"]["records"]
        lines += [
            "## `WORKSHOP_DATA.library`: a research library on neurotechnology in the administration of justice (PDF)",
            "",
            "`{title, source, count, records: [{id, symbol, kind, author, title, short_title, published, year, url, pdf, pages, passages: [...]}]}`.",
            "One record = one document. `kind` is one of: " + ", ".join(dict.fromkeys(d["kind"] for d in lib)) + ".",
            "`symbol` is the UN document symbol, or null for a document that has none. Journal articles also have",
            "`journal`; some documents have `rights` (their copyright or licence). `status` is \"ingested\" (read into",
            "the research wiki, `WORKSHOP_DATA.wiki`) or \"inbox\" (in the library, not yet in the wiki).",
            "Each of its `passages` is `{id, page, page_label, paragraph, section, text}`: the verbatim text of one",
            "paragraph, the PDF page it starts on (`page`), the page number printed on that page (`page_label`, the",
            "one to cite: \"p. 3471\"), the paragraph number where the document numbers its paragraphs",
            "(`paragraph`, a string such as \"32\" or \"50 (c)\"; null in articles and reports that do not), and",
            "the heading it sits under (`section`, or null).",
            "Documents: " + "; ".join(f"{d['id']} ({d['kind']}, {d['year']}: {d['short_title']}, {len(d['passages'])} passages)" for d in lib) + ".",
            "`studio.openSource(id, page, quote)` opens that document's PDF at that PDF page next to the app and marks `quote` on it: use it",
            "for every passage shown (with its text as `quote`), so a reader can check it against the original. Cite a passage as",
            "symbol or author and year, then \"para. N\" when `paragraph` is set, otherwise \"p. page_label\".",
            "",
        ]
    if "wiki" in packs:
        w = packs["wiki"]
        kinds = Counter(pg["type"] for pg in w["pages"])
        inbox = [d["id"] for d in packs.get("library", {}).get("records", []) if d.get("status") == "inbox"]
        lines += [
            "## `WORKSHOP_DATA.wiki`: a research wiki on the library, kept by language models",
            "",
            "`{title, source, built, count, schema, pages: [...], index, log, tensions}`. `schema` is the wiki's rulebook",
            "(markdown); `index` (the catalog, one line per page), `log` (dated entries, oldest first, each starting",
            "`## [YYYY-MM-DD] ingest | …`) and `tensions` (the open disagreements, one `###` entry each) are markdown too.",
            f"Each of the {w['count']} `pages` (" + ", ".join(f"{n} {k}" for k, n in kinds.items()) + ") is",
            "`{slug, type, title, frontmatter, body}`: `type` is \"source\" (one library document), \"concept\", \"entity\"",
            "(a treaty article, General Comment, report, case or law) or \"question\"; `frontmatter` is `{title, type, tags,",
            "register, status, updated, links, sources}` (`links`: slugs of related pages; `sources`: library ids;",
            "`register`: letters, see below); `body` is markdown, where `[[slug]]` links to another page.",
            "Every claim in a body carries a pin to a library passage: `[A/81/351, para. 16](pin:A/81/351#p6 \"verbatim",
            "quote\") ✓` gives a label, the library id, the PDF page, the quote, and ✓ (verified) or ⚠ (unverified).",
            "A pin is a quotation inside the sentence: the prose is written around it (\"The central ask [pin] ✓, stated also",
            "in the summary [pin] ✓\"), so show the quote itself, in quotation marks, where the pin stands, followed by the",
            "label as a small citation; a pin shown as its label alone leaves the sentence without its words.",
            r'One regular expression finds them all: `/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g`',
            "(groups: label, id, PDF page, quote, mark). Open a pin with `studio.openSource(id, page, quote)`. A pin is verified",
            "when its quote is in a passage of that document in `WORKSHOP_DATA.library` that starts on that PDF page",
            "(compare after normalising whitespace, curly quotes, dashes and hyphenation). A quote may join fragments",
            "of one passage with \"…\": then each fragment must be in that passage, in the same order (82 of 707 pins do).",
            "`register` letters: (a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national",
            "human rights institution, (e) civil society, (f) scholarship. A fenced block opened by ```` ```contested ````",
            "records a disagreement: lines `claim:`, `verdict:`, `note:`, then one line per position:",
            "`+`, `-` or `~` (supports, contests, mixed), the register letter, a pin, a gloss and a `[[slug]]`, separated",
            "by ` | `. Weights by register for a lean bar: a 5, b 4, c 3, d 2, e 1, f 0.5; the verdict, not the bar, is the answer.",
            f"Library documents not yet in the wiki (status \"inbox\"): {', '.join(inbox) or 'none'}. Ingesting one means",
            "writing its source page from its passages and updating the pages it touches, with pins.",
            "",
        ]
    if "pdf_text" in packs:
        p = packs["pdf_text"]
        lines += [
            "## `WORKSHOP_DATA.pdf_text`: one UN document as raw text from its PDF",
            "",
            "`{title, symbol, doc_url, source, count, records: [{page, text}], reference: {...}}`.",
            f"`records` are the {p['count']} pages of {p['symbol']} exactly as a PDF converter produced",
            "them. Nothing has been cleaned: page headers and footers and the footnotes are mixed into",
            "the text.",
            "`reference` lets an app check its own result: `paragraphs` (how many numbered paragraphs",
            "the document has), `footnotes` (how many footnotes), `adopted`, and `first_words`",
            f"(`{{\"1\": \"{p['reference']['first_words']['1']}\", …}}`: the first six words of each numbered paragraph).",
            "",
        ]
    if "pdf_text_2" in packs:
        p = packs["pdf_text_2"]
        lines += [
            "## `WORKSHOP_DATA.pdf_text_2`: a second UN document as raw text from its PDF",
            "",
            f"The same shape as `pdf_text`: the {p['count']} pages of {p['symbol']} as the same converter produced them,",
            f"with its own `reference` ({p['reference']['paragraphs']} paragraphs, {p['reference']['footnotes']} footnotes).",
            "",
        ]
    lines += [
        "## Rules for every app",
        "",
        "- Always show where a number comes from: n of records, the filter applied, and a link",
        "  (`doc_url`) and symbol for every row shown.",
        "- Counting, filtering, sorting and charts are done by your JavaScript, never estimated.",
        "- Keep the full text of a paragraph available (click to expand); never paraphrase it.",
    ]
    (OUT / "schema.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  schema.md")


def uhri_samples(rec):
    """Five records chosen to show the variety the model's code must handle: each mechanism, both
    main types, SDGs filled in, several countries, and empty lists. The first match in file order."""
    wants = [
        lambda r: r["mechanism"] == "Treaty bodies" and r["type"] == "Recommendations" and r.get("sdgs") and r.get("affected_persons"),
        lambda r: r["mechanism"] == "Universal Periodic Review" and r.get("sdgs"),
        lambda r: r["mechanism"] == "Special Procedures" and len(r.get("countries") or []) > 1,
        lambda r: r["type"] == "Concerns/Observations",
        lambda r: not r.get("themes") or not r.get("affected_persons") or not r.get("sdgs"),
    ]
    pick = []
    for want in wants:
        r = next((r for r in rec if want(r) and r not in pick), None)
        if r:
            pick.append(r)
    return pick


def samples(packs):
    """A few records per dataset (five of the recommendations): the only rows the model is ever shown."""
    out = {}
    for k, p in packs.items():
        if k == "wiki":   # two whole pages
            out[k] = [pg for pg in p["pages"] if pg["slug"] in WIKI_SAMPLES]
            continue
        rec = p["records"]
        pick = [rec[0], rec[len(rec) // 2], rec[-1]]
        if k == "uhri":
            pick = uhri_samples(rec)
        if k == "gc" or k == "hrc":
            pick = [rec[0], rec[len(rec) // 3], rec[2 * len(rec) // 3]]
        if k == "library":   # a numbered UN report and a journal article, two passages each
            pick = []
            for d in (rec[0], next(r for r in rec if r["kind"] == "Journal article")):
                d = dict(d); d["passages"] = d["passages"][:2]
                pick.append(d)
        if k in ("pdf_text", "pdf_text_2"):   # one page is enough to see the format; the whole document would go with every request
            pick = [{"page": 1, "text": rec[0]["text"][:1200] + "\n[… rest of the page omitted in this sample]"}]
        out[k] = pick
    (OUT / "samples.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  samples.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--countries", default=",".join(DEFAULT_COUNTRIES))
    ap.add_argument("--skip-uhri", action="store_true")
    ap.add_argument("--pdf-only", action="store_true", help="rebuild pdf_text.json, library.json and wiki.json only; reuse the other files")
    ap.add_argument("--html-only", action="store_true", help="build html_doc.json and add it to index.json, schema.md and samples.json")
    ap.add_argument("--ten-only", action="store_true", help="build pdf_ten.json and add it to index.json, schema.md and samples.json")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.ten_only:
        index = json.loads((OUT / "index.json").read_text())
        p = pdf_ten(json.loads((OUT / "gc.json").read_text()))
        write("pdf_ten.json", p)
        index["datasets"]["pdf_ten"] = {"file": "pdf_ten.json", "count": p["count"]}
        (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
        schema = (OUT / "schema.md").read_text()
        if "WORKSHOP_DATA.pdf_ten" not in schema:
            schema = schema.replace("## Rules for every app", "\n".join(ten_schema(p)) + "\n## Rules for every app", 1)
            (OUT / "schema.md").write_text(schema, encoding="utf-8")
        samples = json.loads((OUT / "samples.json").read_text())
        one = dict(p["records"][1]); one["pages"] = [{"page": 1, "text": one["pages"][0]["text"][:800] + "\n[… rest of the page and the other pages omitted]"}]
        one["reference"] = dict(one["reference"], first_words={k: v for k, v in list(one["reference"]["first_words"].items())[:2]})
        samples["pdf_ten"] = [one]
        (OUT / "samples.json").write_text(json.dumps(samples, ensure_ascii=False, indent=1), encoding="utf-8")
        print("  pdf_ten.json, index.json, schema.md, samples.json")
        return
    if a.html_only:
        index = json.loads((OUT / "index.json").read_text())
        h = html_doc(json.loads((OUT / "gc.json").read_text()))
        write("html_doc.json", h)
        index["datasets"]["html_doc"] = {"file": "html_doc.json", "count": 1}
        (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
        schema = (OUT / "schema.md").read_text()
        if "WORKSHOP_DATA.html_doc" not in schema:
            schema = schema.replace("## Rules for every app", "\n".join(html_schema(h)) + "\n## Rules for every app", 1)
            (OUT / "schema.md").write_text(schema, encoding="utf-8")
        samples = json.loads((OUT / "samples.json").read_text())
        samples["html_doc"] = [{"html": h["html"][:1500] + "\n<!-- … the rest of the document omitted in this sample -->"}]
        (OUT / "samples.json").write_text(json.dumps(samples, ensure_ascii=False, indent=1), encoding="utf-8")
        print("  html_doc.json, index.json, schema.md, samples.json")
        return
    if a.pdf_only:
        index = json.loads((OUT / "index.json").read_text())
        packs = {"uhri": json.loads((OUT / index["countries"][0]["file"]).read_text()),
                 "gc": json.loads((OUT / "gc.json").read_text()), "hrc": json.loads((OUT / "hrc.json").read_text())}
        print("Raw PDF text …")
        packs["pdf_text"] = pdf_text(packs["gc"])
        write("pdf_text.json", packs["pdf_text"])
        index["datasets"]["pdf_text"] = {"file": "pdf_text.json", "count": packs["pdf_text"]["count"]}
        packs["pdf_text_2"] = pdf_text(packs["gc"], PDF_DOC_2, "pdf_text_2")
        write("pdf_text_2.json", packs["pdf_text_2"])
        index["datasets"]["pdf_text_2"] = {"file": "pdf_text_2.json", "count": packs["pdf_text_2"]["count"]}
        print("Library …")
        packs["library"] = library(packs["gc"])
        write("library.json", packs["library"])
        index["datasets"].pop("un_library", None)
        index["datasets"]["library"] = {"file": "library.json", "count": packs["library"]["count"]}
        print("Wiki …")
        packs["wiki"] = wiki()
        write("wiki.json", packs["wiki"])
        index["datasets"]["wiki"] = {"file": "wiki.json", "count": packs["wiki"]["count"]}
        (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
        print("  index.json")
        schema(packs)
        samples(packs)
        return

    index = {"built": date.today().isoformat(), "countries": [], "datasets": {}}
    packs, built = {}, []
    if not a.skip_uhri:
        wanted = (get_json(UHRI + "facets")["countries"] if a.countries == "all"
                  else [x.strip() for x in a.countries.split(",") if x.strip()])
        names = {str(k): v for k, v in sorted(SDG_GOALS.items())}

        def one(c):   # written as soon as it is read: 200 countries would not fit in memory together
            p = uhri_country(c)
            if not p["count"]:
                sys.exit(f"no UHRI records for {c!r}: check the spelling against /facets")
            p["sdg_names"] = names
            f = f"uhri_{slug(c)}.json"
            write(f, p)
            return c, {"name": c, "file": f, "count": p["count"], "region": p["region"]}, (p if c == SCHEMA_COUNTRY else None)

        with ThreadPoolExecutor(4) as ex:   # four at a time: gentle on the UHRI server
            for c, entry, p in ex.map(one, wanted):
                index["countries"].append(entry)
                if p:
                    packs["uhri"] = p
        if "uhri" not in packs:   # the schema's examples come from one country; any will do
            first = index["countries"][0]
            packs["uhri"] = json.loads((OUT / first["file"]).read_text())
        index["countries"].sort(key=lambda e: e["name"])
    print("General Comments …")
    packs["gc"] = gc_corpus()
    write("gc.json", packs["gc"])
    index["datasets"]["gc"] = {"file": "gc.json", "count": packs["gc"]["count"]}
    print("HRC votes …")
    packs["hrc"] = hrc_votes()
    write("hrc.json", packs["hrc"])
    index["datasets"]["hrc"] = {"file": "hrc.json", "count": packs["hrc"]["count"]}
    print("Raw PDF text …")
    packs["pdf_text"] = pdf_text(packs["gc"])
    write("pdf_text.json", packs["pdf_text"])
    index["datasets"]["pdf_text"] = {"file": "pdf_text.json", "count": packs["pdf_text"]["count"]}
    packs["pdf_text_2"] = pdf_text(packs["gc"], PDF_DOC_2, "pdf_text_2")
    write("pdf_text_2.json", packs["pdf_text_2"])
    index["datasets"]["pdf_text_2"] = {"file": "pdf_text_2.json", "count": packs["pdf_text_2"]["count"]}
    print("Library …")
    packs["library"] = library(packs["gc"])
    write("library.json", packs["library"])
    index["datasets"]["library"] = {"file": "library.json", "count": packs["library"]["count"]}
    print("Wiki …")
    packs["wiki"] = wiki()
    write("wiki.json", packs["wiki"])
    index["datasets"]["wiki"] = {"file": "wiki.json", "count": packs["wiki"]["count"]}

    if "uhri" not in packs:
        old = json.loads((OUT / "index.json").read_text())
        index["countries"] = old["countries"]
        packs["uhri"] = json.loads((OUT / old["countries"][0]["file"]).read_text())
    (OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print("  index.json")
    schema(packs)
    samples(packs)


if __name__ == "__main__":
    main()
