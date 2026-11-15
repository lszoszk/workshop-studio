#!/usr/bin/env python3
"""Two prototype tasks for the bake-off (not yet in the studio's menus): their data files, and the facts the checks
look for, written into site/data/prompts.json.

    python3 tools/lab_data.py

pdf_meta.json   the ten General Comments of pdf_ten.json as bare files (doc-01.pdf …, in another order), pages only:
                the metadata (symbol, date, type, number, what it replaces) has to come out of the text.
drafts.json     three ICCPR articles (21, 19, 22) stage by stage, 1947–1966, from the Travaux database
                (~/Desktop/AI/travaux/data/travaux.sqlite3): each draft as its OCR gives it, the adopted text, and the
                votes taken on the article with their meeting dates.
"""
import hashlib
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "site" / "data"
TRAVAUX = Path.home() / "Desktop" / "AI" / "travaux" / "data" / "travaux.sqlite3"

# the Travaux API's stages (api/server.py COVENANT_STAGES): (stage, symbol, what it is, date)
STAGES = [("uk_draft_1947", "E/CN.4/21", "United Kingdom's draft international bill (E/CN.4/21, annex B)", "June 1947"),
          ("e_cn4_21_g", "E/CN.4/21", "Drafting Committee: articles for a convention (E/CN.4/21, annex G)", "June 1947"),
          ("e_cn4_56", "E/CN.4/56", "Commission's working group on the Convention (Geneva)", "December 1947"),
          ("e600", "E/600", "Commission, 2nd session: draft Covenant (Geneva draft)", "December 1947"),
          ("chr5", "E/800", "Commission, 3rd session: draft Covenant (E/800, annex B)", "June 1948"),
          ("chr6", "E/CN.4/350", "Commission, 5th session: draft Covenant (E/1371, annex I)", "June 1949"),
          ("e1681", "E/1681", "Commission, 6th session: draft Covenant (E/1681, annex I)", "May 1950"),
          ("e1992", "E/CN.4/640", "Commission, 7th session: draft Covenant (E/1992, annex I)", "May 1951"),
          ("e2256", "E/CN.4/669", "Commission, 8th session: draft Covenants (E/2256)", "June 1952"),
          ("e2447", "E/CN.4/689", "Commission, 9th session: draft Covenants (E/2447)", "May 1953"),
          ("e2573", "A/2929", "Commission on Human Rights, 10th session (E/2573, reprinted in A/2929)", "April 1954"),
          ("a4625", "A/4625", "Third Committee, 15th session: articles 15-18 as adopted (A/4625, annex)", "December 1960"),
          ("a5000", "A/5000", "Third Committee, 16th session: articles 19-25 as adopted (A/5000, annex)", "December 1961")]
ARTICLES = {   # the adopted texts (A/RES/2200 A (XXI), 16 December 1966), as the Travaux database gives them
    21: ("Peaceful assembly",
         "The right of peaceful assembly shall be recognized. No restrictions may be placed on the exercise of this right other than "
         "those imposed in conformity with the law and which are necessary in a democratic society in the interests of national security "
         "or public safety, public order (ordre public), the protection of public health or morals or the protection of the rights and "
         "freedoms of others."),
    19: ("Freedom of opinion and expression",
         "1. Everyone shall have the right to hold opinions without interference. 2. Everyone shall have the right to freedom of expression; "
         "this right shall include freedom to seek, receive and impart information and ideas of all kinds, regardless of frontiers, either "
         "orally, in writing or in print, in the form of art, or through any other media of his choice. 3. The exercise of the rights "
         "provided for in paragraph 2 of this article carries with it special duties and responsibilities. It may therefore be subject to "
         "certain restrictions, but these shall only be such as are provided by law and are necessary: (a) For respect of the rights or "
         "reputations of others; (b) For the protection of national security or of public order (ordre public), or of public health or morals."),
    22: ("Freedom of association",
         "1. Everyone shall have the right to freedom of association with others, including the right to form and join trade unions for the "
         "protection of his interests. 2. No restrictions may be placed on the exercise of this right other than those which are prescribed "
         "by law and which are necessary in a democratic society in the interests of national security or public safety, public order "
         "(ordre public), the protection of public health or morals or the protection of the rights and freedoms of others. This article "
         "shall not prevent the imposition of lawful restrictions on members of the armed forces and of the police in their exercise of this "
         "right. 3. Nothing in this article shall authorize States Parties to the International Labour Organisation Convention of 1948 "
         "concerning Freedom of Association and Protection of the Right to Organize to take legislative measures which would prejudice, or to "
         "apply the law in such a manner as to prejudice, the guarantees provided for in that Convention."),
}
MONTHS = "January February March April May June July August September October November December".split()


def pdf_meta():
    src = json.loads((DATA / "pdf_ten.json").read_text())["records"]
    order = sorted(src, key=lambda r: hashlib.sha1(r["symbol"].encode()).hexdigest())   # not the order of pdf_ten
    records, truth = [], []
    for i, r in enumerate(order, 1):
        first = r["pages"][0]["text"]
        date = re.search(r"(\d{1,2} (?:%s) \d{4})" % "|".join(MONTHS), first).group(1)
        kind = re.search(r"General (comment|recommendation) No\. ?(\d+)", first, re.I)
        replaces = re.findall(r"(?:replaces|updating) general (?:comments?|recommendation) No(?:s)?\. ?(\d+)(?:,[^.]*?No\. (\d+))?", " ".join(p["text"] for p in r["pages"][:2]), re.I)
        nums = sorted({n for pair in replaces for n in pair if n})
        records.append({"file": f"doc-{i:02d}.pdf", "pages": r["pages"]})
        truth.append({"file": f"doc-{i:02d}.pdf", "symbol": r["symbol"], "date": date, "type": kind.group(1).lower(),
                      "number": kind.group(2), "replaces": nums})
    out = {"dataset": "pdf_meta", "title": "Ten UN documents as bare PDF files, the text of each page as a converter extracted it",
           "source": "The PDFs from the UN Official Document System, converted with pdftotext (Poppler); nothing cleaned",
           "built": "2026-11-15", "count": len(records), "records": records}
    (DATA / "pdf_meta.json").write_text(json.dumps(out, ensure_ascii=False))
    return truth


def proposers(raw):
    try:
        return [str(x) for x in json.loads(raw or "[]")]
    except ValueError:
        return [x for x in (raw or "").split("; ") if x]


def date_rx(date):
    """A date as an app may print it: 23 August 2007, 2007-08-23, 23/08/2007, 23.08.2007, August 23, 2007, 23 Aug 2007."""
    d, m, y = date.split()
    mm = f"{MONTHS.index(m) + 1:02d}"
    return "|".join([re.escape(date), f"{y}-{mm}-{int(d):02d}", f"0?{int(d)}/{mm}/{y}", rf"0?{int(d)}\.{mm}\.{y}",
                     rf"{m} 0?{int(d)},? {y}", rf"0?{int(d)} {m[:3]}\.? {y}"])


def checks(truth):
    """The facts each prototype's checks look for (tools/bakeoff.py: row_facts_*, diff_*)."""
    symbols = [t["symbol"] for t in truth]
    num = lambda n: rf"(?:no\.?|gc|gr|comments?|recommendations?)\s*(?:no\.?\s*)?{n}\b"
    meta = {"no_console_errors": True, "no_network": True, "uses_workshop_data": True, "table_min_rows": 10,
            "text_contains": symbols, "download": True,
            "row_facts_dates": {"rows": symbols, "facts": [{"row": t["symbol"], "has": [date_rx(t["date"])]} for t in truth]},
            "row_facts_types": {"rows": symbols, "facts": [{"row": t["symbol"], "has": ["recommendation" if t["type"] == "recommendation" else "comment"]}
                                                           for t in truth]},
            "row_facts_replaces": {"rows": symbols, "facts": [{"row": t["symbol"], "has": [num(n) for n in t["replaces"]]} for t in truth if t["replaces"]]}}
    versions = {"no_console_errors": True, "no_network": True, "uses_workshop_data": True, "controls_min": 1,
                "text_contains": ["E/CN.4/669", "A/RES/2200", "E/CN.4/L.201"],
                # "or public safety, public order": a word diff may keep either "public" as unchanged, so the check
                # looks for the word that was only ever added
                "diff_added": ["democratic society", "safety", "ordre public"],
                "diff_removed": ["to ensure"],
                "diff_not": ["restric"]}
    return meta, versions


def drafts():
    db = sqlite3.connect(TRAVAUX)
    order = {st: i for i, (st, *_) in enumerate(STAGES)}
    meta = {st: (sym, label, date) for st, sym, label, date in STAGES}
    articles = []
    for art, (title, final) in ARTICLES.items():
        rows = db.execute("select stage, stage_symbol, draft_article, page, text from draft_texts where instrument='ICCPR' and final_article=?",
                          (art,)).fetchall()
        stages = [{"stage": meta[st][1], "symbol": sym, "date": meta[st][2], "draft_article": da, "page": pg, "text": tx}
                  for st, sym, da, pg, tx in sorted(rows, key=lambda r: order[r[0]])]
        stages.append({"stage": "General Assembly: the Covenant as adopted", "symbol": "A/RES/2200 A (XXI)", "date": "16 December 1966",
                       "draft_article": art, "page": None, "text": final})
        votes = [{"meeting": sym, "date": dt, "outcome": out, "yes": y, "no": n, "abstentions": a, "proposers": proposers(pr),
                  "subject": " ".join((subj or "").split())[:400]}
                 for sym, dt, out, y, n, a, pr, subj in db.execute(
                     "select d.symbol, doc.meeting_date, d.outcome, d.yes, d.no, d.abstentions, d.proposers, d.subject from decisions d "
                     "left join documents doc on doc.symbol = d.symbol where d.article_instrument='ICCPR' and d.final_article=? "
                     "order by doc.meeting_date, d.seq", (art,))]
        articles.append({"instrument": "ICCPR", "article": art, "title": title, "stages": stages, "votes": votes})
    out = {"dataset": "drafts", "title": "How three articles of the ICCPR were drafted, 1947–1966: the text at every stage, and the votes",
           "source": "UN travaux préparatoires: the Covenant drafts and meeting records, OCR (Travaux préparatoires database, Ł. Szoszkiewicz)",
           "built": "2026-11-15", "count": len(articles), "records": articles}
    (DATA / "drafts.json").write_text(json.dumps(out, ensure_ascii=False))
    return articles


if __name__ == "__main__":
    t = pdf_meta()
    for x in t:
        print(x)
    a = drafts()
    for x in a:
        print(x["article"], x["title"], len(x["stages"]), "stages,", len(x["votes"]), "votes")
    meta, versions = checks(t)
    path = DATA / "prompts.json"
    spec = json.loads(path.read_text())
    for p in spec["prompts"]:
        if p["id"] == "x-meta-pdfs":
            p["checks"] = meta
        if p["id"] == "x-versions":
            p["checks"] = versions
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    print("checks written to", path)
