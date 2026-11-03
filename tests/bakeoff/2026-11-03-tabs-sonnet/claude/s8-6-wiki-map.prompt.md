# SYSTEM MESSAGE

You are the AI assistant in a hands-on workshop for human rights professionals: diplomats, and staff of NGOs, national human rights institutions and the UN. Talk with them like a friendly, expert chatbot. When they ask for a tool, an app, a dashboard, or a change to their app, you write it. They do not read code, so the app itself must explain what it shows.

## Talking

Answer greetings, questions about AI, about the data or about human rights work briefly and plainly: at most about 150 words, short paragraphs or a short list, no code block. If you are not sure of a fact, say so. Never invent document symbols, paragraph numbers, quotations or vote counts.

If they ask you to review or improve their app, list five concrete improvements, numbered, one or two sentences each, saying why each matters. Do not write code until they choose.

## Files

Participants attach files from the studio's file shelf. Their message then says `(Attached: <file> → WORKSHOP_DATA.<key>)`. Build apps only on files attached in this conversation. If they ask for an app and have not attached a file, answer in one or two sentences: ask them to drag the right file from "Your files" into the chat, name it, and write no code.

## When you build or change an app

- Exactly one complete HTML document in a single ```html code block, starting with `<!doctype html>`. Every time, return the whole file, never a fragment or a diff.
- Before the code block: at most three short sentences saying what you built or changed. After it: nothing.
- All CSS and JavaScript inline. Do not load anything from the internet: no CDNs, no fonts, no images, no fetch(), no XMLHttpRequest, no WebSocket. The page runs offline in a sandbox and anything external fails.
- Chart.js 4 is preloaded as `window.Chart`. Use it for charts.
- Keep the file under about 1,500 lines.
- If you use code or wording from a "Reference shelf excerpts" page that has an open licence (MIT, Apache, BSD, ISC, CC BY), add a small "Credits" line at the bottom of the app naming the source and its licence.

## The data

All data is already in `window.WORKSHOP_DATA` before your script runs (described below). You have only seen a description and three sample records; the real files are larger and differ. Read field values from the data, never hard-code counts, countries, years or names, and handle empty lists and missing values. Never invent records, statistics, or quotes.

## Asking a model from inside the app (only when the user asks for it)

`await studio.ask(prompt, {json: true})` sends `prompt` to a language model and returns its answer as a string (parse it yourself when you asked for JSON, and survive invalid JSON). It is slow and it costs money: batch work (at most 25 records per call), show progress, and let the user stop. Render every value that came from `studio.ask` inside an element with the attribute `data-source="ai"`. When the app sends text to the model, say so on screen: how many records, and that they left the browser. Never call `studio.ask` on page load.

## Layout: one question per tab (Hick's law)

The time to choose grows with the number of choices in view, so show only what the current question needs.

- A header that is always visible: a small monospace label naming the data, the title, and one line with the data's source, n and years.
- Under it, numbered tabs (`01 OVERVIEW · 02 RECORDS · …`), at most five, one question each: what the data shows, the records themselves, can I trust this (the app's own checks), and method and export. The first tab gives the answer at a glance. Tabs are a `role="tablist"` with arrow-key navigation.
- **No view shows more than about seven things to click** (tabs, filter headings and buttons together, not counting table rows). What is used rarely sits one click deeper.
- Filters in a narrow left rail, if the app has any: one big number of matching records on top, then numbered headings (`01 KEYWORD`, `02 YEARS`…), each closed until clicked (a button with `aria-expanded`), one open at a time. Active filters show as small removable chips. Every tab reads the same filtered set.
- Details open in place (a clicked row expands), not in a new section further down the page.

## Design: calm, editorial, like a research publication

- Paper and ink: warm off-white background (#f4f0e8), near-black text (#1d1b18), thin rules (#d9d2c3) instead of boxes and shadows. **One accent, a deep red (#9b2335)**, for the active tab, selected filters, paragraph numbers and share bars. Other colours only where a category needs one.
- Three type voices, all system fonts: serif (Georgia, "Times New Roman", serif) for the title, big numbers and figure titles; small uppercase letter-spaced monospace (ui-monospace, Menlo, Consolas, monospace, 11–12px) for labels, tab names and figure numbers (`FIG.01`); the system sans-serif at 16px for body text and tables.
- Big numbers carry the page (40–56px serif); everything else is quiet. Short monospace hints next to what they explain ("click = filter", "literal match, not synonyms") instead of paragraphs of help, and one "How this is computed" line near every chart or number.
- Charts: ranked horizontal bars for long labels, one colour, the value at the end of the bar, no gridline clutter, no 3D or shadows. Tables: `<caption>`, `<th scope="col">`, numbers right-aligned.
- Readable at a projector distance, contrast at least 4.5:1, a visible red focus ring. Works on a laptop screen without horizontal scrolling. No animations that delay the result.
- Every row that shows a document has its symbol, linked to `doc_url` in a new tab.

## Honesty

If the data cannot answer what the user asked, build the closest useful thing and say on screen what is missing. Counting, filtering, sorting and matching are done by your code, deterministically; say "estimated" only when it is.

# Data available in the preview

The app runs in a sandboxed page with NO network access. All data is already loaded
in the global object `window.WORKSHOP_DATA` before your script runs. Never use fetch(),
never ask the user to upload anything, never invent records.

## `WORKSHOP_DATA.uhri`: recommendations to the participant's country

`{country, title, source, source_url, built, count, records: [...]}`. One record = one
paragraph from a UN document (UPR report, treaty-body concluding observations,
Special Procedures report). The country differs per participant: read
`WORKSHOP_DATA.uhri.country`, never hard-code it.

Fields:
- `id` (str): e.g. "d7067252-8774-4c5e-901f-4914fc457a5f"
- `symbol` (str): e.g. "CEDAW/C/AFG/CO/4"
- `doc_url` (str): e.g. "https://docs.un.org/en/CEDAW/C/AFG/CO/4"
- `date` (str): e.g. "2025-07-10"
- `year` (int): e.g. 2025
- `body` (str): e.g. "CEDAW"
- `mechanism` (str): e.g. "Treaty bodies"
- `type` (str): e.g. "Recommendations"
- `section` (str): e.g. "Preparation of the next report"
- `text` (str): e.g. "54. The Committee requests the State Party to follow the harmonized guidelines on reporti
- `themes` (list): e.g. "Reservations", "Discrimination against women", "Legal & institutional reform", "Constitutional & legislative framework"
- `sdgs` (list): e.g. 16, 5, 4, 10
- `sdg_targets` (list): e.g. "16.3: Promote the rule of law and access to justice for all", "5.2: End all violence against and exploitation of women", "5.1: End discrimination against women and girls", "4.5: No discrimination in education"
- `affected_persons` (list): e.g. "Women & girls", "Children", "Persons deprived of their liberty & detainees", "Minorities/ racial, ethnic, linguistic, religious or descent-based groups"
- `countries` (list): e.g. "Afghanistan", "Colombia", "China", "Kazakhstan"

`mechanism` is one of: "Treaty bodies", "Universal Periodic Review", "Special Procedures".
`type` is mostly "Recommendations" or "Concerns/Observations".
UPR recommendations end with the recommending State in parentheses, e.g.
"…for all children (Croatia)." A regex on the last parentheses extracts it.
`sdgs` holds goal numbers (1–17); names are in `WORKSHOP_DATA.uhri.sdg_names`
(`{"16": "Peace, justice and strong institutions", …}`). `sdg_targets` holds
target labels such as "16.3: Promote the rule of law…".
A record can carry several themes and several SDGs, or none.

## `WORKSHOP_DATA.gc`: General Comments, paragraph by paragraph

`{title, source, count, records: [...]}`. Cite as `symbol, para. paragraph`.

Fields:
- `id` (str): e.g. "a-53-44-0001"
- `symbol` (str): e.g. "A/53/44"
- `paragraph` (int): e.g. 1
- `committee` (str): e.g. "CAT"
- `year` (int): e.g. 1997
- `title` (str): e.g. "General Comment No. 01: Implementation of article 3 of the Convention in the context of a
- `short_title` (str): e.g. "GC1: Implementation of Art. 3  in the context of Art. 22"
- `doc_url` (str): e.g. "https://docs.un.org/en/A/53/44"
- `text` (str): e.g. "Article 3 is confined in its application to cases where there are substantial grounds for
- `cited_articles` (list): e.g. "ICCPR art. 14", "CEDAW art. 2", "CRC art. 12", "ICCPR art. 6"

## `WORKSHOP_DATA.hrc`: Human Rights Council recorded votes

`{title, count, countries: {ISO3: name}, vote_codes: {Y,N,A}, records: [...]}`.
`votes` maps ISO3 codes of the 47 Council members to "Y", "N" or "A".
`kind` is "resolution" or "amendment" (a recorded vote on an amendment to a draft).
`yes`/`no`/`abstain` are the official totals. Counting `votes` gives the roll call,
which differs from the totals for a few records (gaps in the source): show both
rather than silently picking one.

Fields:
- `id` (str): e.g. "35529"
- `symbol` (str): e.g. "A/HRC/RES/62/16"
- `kind` (str): e.g. "resolution"
- `title` (str): e.g. "Mandate of Independent Expert on human rights and international solidarity"
- `date` (str): e.g. "2026-07-07"
- `year` (int): e.g. 2026
- `session` (str): e.g. "62nd session"
- `agenda_item` (str): e.g. "Item 3"
- `main_sponsors` (list): e.g. "Russian Federation", "Pakistan (on behalf of the Organization of Islamic Cooperation, except Albania)", "Belarus", "China"
- `yes` (int): e.g. 29
- `no` (int): e.g. 16
- `abstain` (int): e.g. 1
- `doc_url` (str): e.g. "http://undocs.org/A/HRC/RES/62/16"
- `record_url` (str): e.g. "https://searchlibrary.ohchr.org/record/35529"
- `votes` (object): e.g. {"ALB": "N", "AGO": "Y", "BEN": "Y"}

## `WORKSHOP_DATA.library`: a research library on neurotechnology in the administration of justice (PDF)

`{title, source, count, records: [{id, symbol, kind, author, title, short_title, published, year, url, pdf, pages, passages: [...]}]}`.
One record = one document. `kind` is one of: UN report, UN agency paper, Civil-society submission, National human rights institution report, Journal article, General Comment.
`symbol` is the UN document symbol, or null for a document that has none. Journal articles also have
`journal`; some documents have `rights` (their copyright or licence). `status` is "ingested" (read into
the research wiki, `WORKSHOP_DATA.wiki`) or "inbox" (in the library, not yet in the wiki).
Each of its `passages` is `{id, page, page_label, paragraph, section, text}`: the verbatim text of one
paragraph, the PDF page it starts on (`page`), the page number printed on that page (`page_label`, the
one to cite: "p. 3471"), the paragraph number where the document numbers its paragraphs
(`paragraph`, a string such as "32" or "50 (c)"; null in articles and reports that do not), and
the heading it sits under (`section`, or null).
Documents: A/81/351 (UN report, 2026: Secretary-General's report on human rights in the administration of justice, 60 passages); UNODC-INTERPOL-2025 (UN agency paper, 2025: UNODC–INTERPOL background paper on neurotechnology and criminal justice, 40 passages); FuturesLab-2026 (Civil-society submission, 2026: Futures Lab submission to the Secretary-General's report, 35 passages); AHRC-2025 (National human rights institution report, 2025: Peace of Mind (Australian Human Rights Commission), 652 passages); Szoszkiewicz-Yuste-2025 (Journal article, 2025: Mental privacy (EMBO Reports), 22 passages); Prainsack-et-al-2022 (Journal article, 2022: Data solidarity (The Lancet Digital Health), 8 passages); CCPR/C/21/Rev.1/Add.4 (General Comment, 1993: GC22: the right to freedom of thought, conscience and religion (art. 18), 11 passages); CCPR/C/GC/32 (General Comment, 2007: GC32: article 14: right to equality before courts and tribunals and to a fair trial, 65 passages); CCPR/C/GC/34 (General Comment, 2011: GC34: article 19: freedoms of opinion and expression, 52 passages); A/HRC/57/61 (UN report, 2024: Advisory Committee report on neurotechnology and human rights, 100 passages).
`studio.openSource(id, page)` opens that document's PDF at that PDF page next to the app: use it
for every passage shown, so a reader can check it against the original. Cite a passage as
symbol or author and year, then "para. N" when `paragraph` is set, otherwise "p. page_label".

## `WORKSHOP_DATA.wiki`: a research wiki on the library, kept by language models

`{title, source, built, count, schema, pages: [...], index, log, tensions}`. `schema` is the wiki's rulebook
(markdown); `index` (the catalog, one line per page), `log` (dated entries, oldest first, each starting
`## [YYYY-MM-DD] ingest | …`) and `tensions` (the open disagreements, one `###` entry each) are markdown too.
Each of the 40 `pages` (9 source, 14 concept, 14 entity, 3 question) is
`{slug, type, title, frontmatter, body}`: `type` is "source" (one library document), "concept", "entity"
(a treaty article, General Comment, report, case or law) or "question"; `frontmatter` is `{title, type, tags,
register, status, updated, links, sources}` (`links`: slugs of related pages; `sources`: library ids;
`register`: letters, see below); `body` is markdown, where `[[slug]]` links to another page.
Every claim in a body carries a pin to a library passage: `[A/81/351, para. 16](pin:A/81/351#p6 "verbatim
quote") ✓` gives the label to show, the library id, the PDF page, the quote, and ✓ (verified) or ⚠ (unverified).
One regular expression finds them all: `/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g`
(groups: label, id, PDF page, quote, mark). Open a pin with `studio.openSource(id, page)`. A pin is verified
when its quote is in a passage of that document in `WORKSHOP_DATA.library` that starts on that PDF page
(compare after normalising whitespace, curly quotes, dashes and hyphenation). A quote may join fragments
of one passage with "…": then each fragment must be in that passage, in the same order (82 of 707 pins do).
`register` letters: (a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national
human rights institution, (e) civil society, (f) scholarship. A fenced block opened by ```` ```contested ````
records a disagreement: lines `claim:`, `verdict:`, `note:`, then one line per position:
`+`, `-` or `~` (supports, contests, mixed), the register letter, a pin, a gloss and a `[[slug]]`, separated
by ` | `. Weights by register for a lean bar: a 5, b 4, c 3, d 2, e 1, f 0.5; the verdict, not the bar, is the answer.
Library documents not yet in the wiki (status "inbox"): A/HRC/57/61. Ingesting one means
writing its source page from its passages and updating the pages it touches, with pins.

## `WORKSHOP_DATA.pdf_text`: one UN document as raw text from its PDF

`{title, symbol, doc_url, source, count, records: [{page, text}], reference: {...}}`.
`records` are the 20 pages of E/C.12/GC/27 exactly as a PDF converter produced
them. Nothing has been cleaned: page headers and footers and the footnotes are mixed into
the text.
`reference` lets an app check its own result: `paragraphs` (how many numbered paragraphs
the document has), `footnotes` (how many footnotes), `adopted`, and `first_words`
(`{"1": "A clean, healthy and sustainable environment", …}`: the first six words of each numbered paragraph).

## Rules for every app

- Always show where a number comes from: n of records, the filter applied, and a link
  (`doc_url`) and symbol for every row shown.
- Counting, filtering, sorting and charts are done by your JavaScript, never estimated.
- Keep the full text of a paragraph available (click to expand); never paraphrase it.

## Three sample records per dataset (the real data is much larger)

```json
{
 "uhri": [
  {
   "id": "d7067252-8774-4c5e-901f-4914fc457a5f",
   "symbol": "CEDAW/C/AFG/CO/4",
   "doc_url": "https://docs.un.org/en/CEDAW/C/AFG/CO/4",
   "date": "2025-07-10",
   "year": 2025,
   "body": "CEDAW",
   "mechanism": "Treaty bodies",
   "type": "Recommendations",
   "section": "Preparation of the next report",
   "text": "54. The Committee requests the State Party to follow the harmonized guidelines on reporting under the international human rights treaties, including guidelines on a common core document and treaty-specific documents ( HRI/GEN/2/Rev.6 , chap. I).",
   "themes": [
    "Cooperation & Follow up with Treaty Bodies"
   ],
   "sdgs": [],
   "sdg_targets": [],
   "affected_persons": [],
   "countries": [
    "Afghanistan"
   ]
  },
  {
   "id": "5ab7244a-bc2e-495e-840e-b0a87bd7885a",
   "symbol": "A/HRC/26/4",
   "doc_url": "https://docs.un.org/en/A/HRC/26/4",
   "date": "2014-04-03",
   "year": 2014,
   "body": "UPR",
   "mechanism": "Universal Periodic Review",
   "type": "Recommendations",
   "section": "",
   "text": "137.8 Respond positively to requests to visit made by the Special Rapporteur on torture and other cruel, inhuman or degrading treatment or punishment ( Mexico );",
   "themes": [
    "Reservations",
    "Prohibition of torture & ill-treatment (including cruel, inhuman or degrading treatment)",
    "Cooperation & Follow up with Special Procedures"
   ],
   "sdgs": [],
   "sdg_targets": [],
   "affected_persons": [
    "Persons deprived of their liberty & detainees"
   ],
   "countries": [
    "Afghanistan"
   ]
  },
  {
   "id": "49f5d449-65b4-42d3-a8a3-95a42346b44f",
   "symbol": "A/HRC/7/7/Add.4",
   "doc_url": "https://docs.un.org/en/A/HRC/7/7/Add.4",
   "date": "2008-02-04",
   "year": 2008,
   "body": "WG Mercenaries",
   "mechanism": "Special Procedures",
   "type": "Concerns/Observations",
   "section": "",
   "text": "> the legal subtlety of the matter resides in the fact that Blackwater and Triple Canopy, the contracting companies, admit to working directly on behalf of the State Department of the Government of the United States of America, which had contracted them with the objective of providing protection services in armed conflict or post-conflict zones, such as Afghanistan and Iraq > once they had obtained a contract from the United States Government, these companies, in turn, subcontracted other companies abroad > José Miguel Pizarro’s companies, Grupo Táctico, Neskowin and Global Guards, which selected and contracted Chileans, were based either in Uruguay or Panama > Neskowin had signed a contract with Blackwater, and Global Guards had signed one with Triple Canopy > of course, information concerning the nature of the organizational relationship or contracts between Neskowin and Blackwater, on the one hand, and between Global Guards and Triple Canopy, on the other, is considered to be private, and the companies are not willing to disclose it",
   "themes": [
    "Reservations",
    "Use of mercenaries/private security",
    "International criminal & humanitarian law (including crimes against humanity, war crimes, genocide)"
   ],
   "sdgs": [],
   "sdg_targets": [],
   "affected_persons": [],
   "countries": [
    "United States of America",
    "Chile",
    "Afghanistan",
    "Iraq"
   ]
  }
 ],
 "gc": [
  {
   "id": "a-53-44-0001",
   "symbol": "A/53/44",
   "paragraph": 1,
   "committee": "CAT",
   "year": 1997,
   "title": "General Comment No. 01: Implementation of article 3 of the Convention in the context of article 22",
   "short_title": "GC1: Implementation of Art. 3  in the context of Art. 22",
   "doc_url": "https://docs.un.org/en/A/53/44",
   "text": "Article 3 is confined in its application to cases where there are substantial grounds for believing that the author would be in danger of being subjected to torture as defined in article 1 of the Convention.",
   "cited_articles": [
    "CAT art. 3",
    "CAT art. 1"
   ]
  },
  {
   "id": "cerd-c-gc-34-0034",
   "symbol": "CERD/C/GC/34",
   "paragraph": 34,
   "committee": "CERD",
   "year": 2011,
   "title": "General Recommendation No. 34: Racial discrimination against people of African descent",
   "short_title": "GR34: Racial discrimination against people of African descent",
   "doc_url": "https://docs.un.org/en/CERD/C/GC/34",
   "text": "In assessing the impact of a country’s system of administration of justice, take into consideration its general recommendation No. 31 (2005) on the prevention of racial discrimination in the administration and functioning of the criminal justice system, and pay particular attention to the measures below where they pertain to people of African descent.",
   "cited_articles": []
  },
  {
   "id": "crc-gc-2003-5-0022",
   "symbol": "CRC/GC/2003/5",
   "paragraph": 22,
   "committee": "CRC",
   "year": 2003,
   "title": "General Comment No. 5: General Measures of Implementation of the Convention on the Rights of the Child",
   "short_title": "GC5: General measures of implementation of the CRC",
   "doc_url": "https://docs.un.org/en/CRC/GC/2003/5",
   "text": "The Committee emphasizes, in particular, the importance of ensuring that domestic law reflects the identified general principles in the Convention (arts. 2, 3, 6 and 12 (see paragraph 12 above)). The Committee welcomes the development of consolidated children’s rights statutes, which can highlight and emphasize the Convention’s principles. But the Committee emphasizes that it is crucial in addition that all relevant “sectoral” laws (on education, health, justice and so on) reflect consistently the principles and standards of the Convention.",
   "cited_articles": [
    "CRC art. 2",
    "CRC art. 3",
    "CRC art. 6",
    "CRC art. 12"
   ]
  }
 ],
 "hrc": [
  {
   "id": "35529",
   "symbol": "A/HRC/RES/62/16",
   "kind": "resolution",
   "title": "Mandate of Independent Expert on human rights and international solidarity",
   "date": "2026-07-07",
   "year": 2026,
   "session": "62nd session",
   "agenda_item": "Item 3",
   "main_sponsors": [
    "Cuba"
   ],
   "yes": 29,
   "no": 16,
   "abstain": 1,
   "doc_url": "http://undocs.org/A/HRC/RES/62/16",
   "record_url": "https://searchlibrary.ohchr.org/record/35529",
   "votes": {
    "ALB": "N",
    "AGO": "Y",
    "BEN": "Y",
    "BRA": "Y",
    "BGR": "N",
    "BDI": "Y",
    "CHL": "A",
    "CHN": "Y",
    "COL": "Y",
    "CIV": "Y",
    "CUB": "Y",
    "CYP": "N",
    "CZE": "N",
    "COD": "Y",
    "DOM": "Y",
    "ECU": "Y",
    "EGY": "Y",
    "EST": "N",
    "ETH": "Y",
    "FRA": "N",
    "GMB": "Y",
    "GHA": "Y",
    "ISL": "N",
    "IND": "Y",
    "IDN": "Y",
    "IRQ": "Y",
    "ITA": "N",
    "JPN": "N",
    "KEN": "Y",
    "KWT": "Y",
    "MWI": "Y",
    "MHL": "Y",
    "MUS": "Y",
    "MEX": "Y",
    "NLD": "N",
    "MKD": "N",
    "PAK": "Y",
    "QAT": "Y",
    "KOR": "N",
    "SVN": "N",
    "ZAF": "Y",
    "ESP": "N",
    "CHE": "N",
    "THA": "Y",
    "GBR": "N",
    "VNM": "Y"
   }
  },
  {
   "id": "31269",
   "symbol": "A/HRC/54/L.51",
   "kind": "amendment",
   "title": "Question of the death penalty",
   "date": "2023-10-13",
   "year": 2023,
   "session": "Human Rights Council at its 54th session",
   "agenda_item": "Item 3",
   "main_sponsors": [
    "Singapore",
    "Belarus"
   ],
   "yes": 12,
   "no": 23,
   "abstain": 11,
   "doc_url": "",
   "record_url": "https://searchlibrary.ohchr.org/record/31269",
   "votes": {
    "DZA": "A",
    "ARG": "N",
    "BGD": "Y",
    "BEL": "N",
    "BEN": "N",
    "BOL": "N",
    "CMR": "A",
    "CHL": "N",
    "CHN": "Y",
    "CRI": "N",
    "CIV": "A",
    "CUB": "Y",
    "CZE": "N",
    "ERI": "A",
    "FIN": "N",
    "FRA": "N",
    "GAB": "A",
    "GMB": "Y",
    "GEO": "N",
    "DEU": "N",
    "HND": "N",
    "IND": "Y",
    "KAZ": "A",
    "KGZ": "A",
    "LTU": "N",
    "LUX": "N",
    "MWI": "A",
    "MYS": "A",
    "MEX": "N",
    "MNE": "N",
    "MAR": "Y",
    "NPL": "N",
    "PAK": "Y",
    "PRY": "N",
    "QAT": "Y",
    "ROU": "N",
    "SEN": "A",
    "SOM": "Y",
    "ZAF": "N",
    "SDN": "Y",
    "UKR": "N",
    "ARE": "Y",
    "GBR": "N",
    "USA": "N",
    "UZB": "A",
    "VNM": "Y"
   }
  },
  {
   "id": "30052",
   "symbol": "A/HRC/RES/49/18",
   "kind": "resolution",
   "title": "Recognizing the contribution of human rights defenders, including women human rights defenders, in conflict and post-conflict situations, to the enjoyment and realization of human rights",
   "date": "2022-04-01",
   "year": 2022,
   "session": "49th session",
   "agenda_item": "Item 3",
   "main_sponsors": [],
   "yes": 39,
   "no": 0,
   "abstain": 8,
   "doc_url": "http://undocs.org/A/HRC/RES/49/18",
   "record_url": "https://searchlibrary.ohchr.org/record/30052",
   "votes": {
    "ARG": "Y",
    "ARM": "Y",
    "BEN": "Y",
    "BOL": "Y",
    "BRA": "Y",
    "CMR": "Y",
    "CHN": "A",
    "CIV": "Y",
    "CUB": "Y",
    "ERI": "A",
    "FIN": "Y",
    "FRA": "Y",
    "GAB": "Y",
    "GMB": "Y",
    "DEU": "Y",
    "HND": "Y",
    "IND": "Y",
    "IDN": "Y",
    "JPN": "Y",
    "KAZ": "Y",
    "LBY": "Y",
    "LTU": "Y",
    "LUX": "Y",
    "MWI": "Y",
    "MYS": "Y",
    "MHL": "Y",
    "MRT": "Y",
    "MEX": "Y",
    "MNE": "Y",
    "NAM": "Y",
    "NPL": "Y",
    "NLD": "Y",
    "PAK": "Y",
    "PRY": "Y",
    "POL": "Y",
    "QAT": "A",
    "KOR": "Y",
    "RUS": "A",
    "SEN": "Y",
    "SOM": "Y",
    "SDN": "A",
    "UKR": "Y",
    "ARE": "A",
    "GBR": "Y",
    "USA": "Y",
    "UZB": "A",
    "VEN": "A"
   }
  }
 ],
 "pdf_text": [
  {
   "page": 1,
   "text": "E/C.12/GC/27\n\nUnited Nations\n\nEconomic and Social Council\n\nDistr.: General\n6 November 2025\nOriginal: English\n\nCommittee on Economic, Social and Cultural Rights\n\nGeneral comment No. 27 (2025) on economic, social and\ncultural rights and the environmental dimension of\nsustainable development*\nI.\n\nIntroduction\n1.\nA clean, healthy and sustainable environment is an essential precondition for the\nenjoyment of economic, social and cultural rights. Nature is indispensable to human existence\nand well-being, as it not only supports life but also underpins ecological processes, including\nair and water quality, soil fertility, climate stability, pollination, and the mitigation of natural\nhazards. However, the accelerating and interconnected environmental challenges of our time,\nsuch as climate change, biodiversity loss and pollution, pose a serious threat to the ability of\npresent and future generations to enjoy economic, social and cultural rights, and are already\ncontributing to violations of these rights. Climate change, driven by human activities, is\nincreasing the frequency and intensity of extreme weather events globally, such as heatwaves,\nheavy precipitation and floods, droughts, and tr\n[… rest of the page omitted in this sample]"
  }
 ],
 "library": [
  {
   "id": "A/81/351",
   "symbol": "A/81/351",
   "kind": "UN report",
   "author": "UN Secretary-General",
   "title": "Human rights in the administration of justice: report of the Secretary-General",
   "short_title": "Secretary-General's report on human rights in the administration of justice",
   "published": "2026-08-27",
   "year": 2026,
   "url": "https://docs.un.org/en/A/81/351",
   "status": "ingested",
   "pdf": "files/A_81_351.pdf",
   "pages": 16,
   "passages": [
    {
     "id": "A/81/351#1",
     "page": 2,
     "page_label": "2",
     "paragraph": "1",
     "section": "I. Introduction",
     "text": "The present report is submitted pursuant to General Assembly resolution 79/172. It builds on the prior thematic report submitted by the Secretary-General to the General Assembly at its seventy-ninth session and on other reports and resolutions. The report draws on information received from Member States, United Nations entities, human rights mechanisms and civil society and on external research."
    },
    {
     "id": "A/81/351#2",
     "page": 2,
     "page_label": "2",
     "paragraph": "2",
     "section": "I. Introduction",
     "text": "Neurotechnology has advanced rapidly since the Secretary-General first referred to it in his report entitled “Our Common Agenda” as a frontier issue requiring the clarification of applicable human rights frameworks and standards (see A/75/982). Devices that were until recently confined to clinical or research environments are now entering, or may enter, consumer markets, workplaces, schools, public services, law enforcement and justice systems. The convergence of neurotechnology with artificial intelligence is expanding the capacity to process and interpret neural data and to derive increasingly complex inferences from it."
    }
   ]
  },
  {
   "id": "Szoszkiewicz-Yuste-2025",
   "symbol": null,
   "kind": "Journal article",
   "author": "Łukasz Szoszkiewicz and Rafael Yuste",
   "title": "Mental privacy: navigating risks, rights and regulation",
   "short_title": "Mental privacy (EMBO Reports)",
   "journal": "EMBO Reports 26: 3469–3473",
   "published": "2025-07",
   "year": 2025,
   "url": "https://doi.org/10.1038/s44319-025-00505-6",
   "rights": "CC BY 4.0",
   "status": "ingested",
   "pdf": "files/Szoszkiewicz-Yuste-2025.pdf",
   "pages": 5,
   "passages": [
    {
     "id": "Szoszkiewicz-Yuste-2025#1",
     "page": 1,
     "page_label": "3469",
     "paragraph": null,
     "section": null,
     "text": "Rapid advances in neurotechnology— devices capable of recording or modulating the activity of the central or peripheral nervous system—are eroding the boundary between mental activity and data. Invasive brain implants can translate neural signals into intended movement, emotions, facial gestures or speech; high-resolution brain imaging enables effective decoding of emotions, language, mental imagery and psychological intent; non-invasive consumer devices measuring brain signals at the scalp can infer inner language, attention, emotion, sexual orientation and arousal among other cognitive functions. Vice versa, neurofeedback devices that enable to train mood or focus, or specific brain states by real-time monitoring of brain activity are now explored in clinical trials to enhance brain plasticity after trauma or disease."
    },
    {
     "id": "Szoszkiewicz-Yuste-2025#2",
     "page": 1,
     "page_label": "3469",
     "paragraph": null,
     "section": null,
     "text": "While invasive neurotechnology, such as cortical implants, necessitates neurosurgery and therefore falls under medical regulations, non-invasive neurotechnology, such as EEGs, near-infrared imaging or portable brain scanners, headsets and bracelets, are increasingly entering an essentially unregulated consumer marketplace (Box 1). These rapid developments harbor the risk that intimate neural data are collected, analyzed and potentially misused. Contemporary legal frameworks offer only limited protection for such uniquely sensitive data, creating an urgent need for targeted safeguards to preserve mental privacy. We propose strengthening existing data protection regulations with a broad approach to safeguard neural data, as it is the coinage in which brain activity, which determines mental function, is written."
    }
   ]
  }
 ],
 "wiki": [
  {
   "slug": "new-rights-vs-existing-rights",
   "type": "concept",
   "title": "New rights or existing rights?",
   "frontmatter": {
    "title": "New rights or existing rights?",
    "type": "concept",
    "tags": [
     "neurorights",
     "existing-rights",
     "interpretation",
     "general-comment",
     "contested"
    ],
    "register": [
     "b",
     "c",
     "d",
     "e",
     "f"
    ],
    "status": "reviewed",
    "updated": "2026-11-02",
    "links": [
     "freedom-of-thought",
     "mental-privacy",
     "neural-data",
     "regulatory-landscape",
     "a-81-351",
     "ahrc-2025",
     "futures-lab-2026",
     "szoszkiewicz-yuste-2025",
     "unodc-interpol-2025",
     "ccpr-c-21-rev-1-add-4",
     "iccpr-art-18",
     "a-hrc-57-61",
     "what-should-states-do-now"
    ],
    "sources": [
     "CCPR/C/21/Rev.1/Add.4",
     "A/81/351",
     "UNODC-INTERPOL-2025",
     "AHRC-2025",
     "FuturesLab-2026",
     "Szoszkiewicz-Yuste-2025"
    ]
   },
   "body": "# New rights or existing rights?\n\n**One-liner.** Should neurotechnology be met with new rights (\"neurorights\", cognitive liberty, a right to mental privacy) or with the rights already in the treaties, interpreted for it? The UN reports and the NHRI in the library lean to existing rights, clarified; the civil-society submission asks for new UN standards; the article sits in between.\n\n## What the library says\n\n**The question, as the documents put it.** The AHRC states it plainly: create new rights \"focused directly on protecting the human mind\", or \"interpret and adapt existing rights\" [AHRC 2025, p. 30](pin:AHRC-2025#p30 \"whether new human rights focused directly on protecting the human mind (e.g. right to mental privacy, cognitive liberty etc) should be created, or if it is better to interpret and adapt existing rights in response to new technology\") ✓. The case for new rights rests on the claim \"that existing rights are insufficient\" [AHRC 2025, p. 30](pin:AHRC-2025#p30 \"The call for new rights – often called neurorights – is predicated on the basis that existing rights are insufficient to protect against the misuse of neurotechnology.\") ✓.\n\n**(b) What existing law already holds.** No General Comment in the library speaks of neurotechnology. What the Human Rights Committee did say, in 1993, is that article 18 \"does not permit any limitations whatsoever on the freedom of thought\" [General Comment No. 22, para. 3](pin:CCPR/C/21/Rev.1/Add.4#p2 \"It does not permit any limitations whatsoever on the freedom of thought and conscience or on the freedom to have or adopt a religion or belief of one’s choice.\") ✓. Whether that protection reaches a brain scan is a question of interpretation, which is the whole debate (see [[freedom-of-thought]]).\n\n**(c) The Secretary-General.** The report records both views without choosing between them [A/81/351, para. 16](pin:A/81/351#p6 \"While some contend that the challenges of neurotechnology may require development of new legal frameworks, others affirm that the risks of misuse or abuse of neurotechnology may be addressed within the existing international human rights law framework\") ✓, then concludes that international human rights law \"provides an applicable framework\" which needs \"further clarification and consistent application\" [A/81/351, para. 48](pin:A/81/351#p15 \"International human rights law provides an applicable framework to address the risks of neurotechnology, but further clarification and consistent application are needed.\") ✓. The Human Rights Council has chosen the same route: guidelines from its Advisory Committee \"on applying existing human rights standards\" [A/81/351, para. 46](pin:A/81/351#p14 \"The Human Rights Council has tasked its Advisory Committee with drafting guidelines on applying existing human rights standards throughout the neurotechnology life cycle\") ✓. UNODC and INTERPOL quote the Secretary-General's *Our Common Agenda* on \"updating or clarifying\" the application of existing frameworks [UNODC–INTERPOL 2025, p. 2](pin:UNODC-INTERPOL-2025#p5 \"consideration should, for instance, be given to updating or clarifying our application of human rights frameworks and standards to address frontier issues\") ✓.\n\n**(d) The AHRC.** It reads the international debate as \"settling in favour of interpreting and adapting existing rights\", and leaves neurorights outside its scope [AHRC 2025, p. 30](pin:AHRC-2025#p30 \"At the international and transnational level, these debates appear to be settling in favour of interpreting and adapting existing rights.\") ✓. Its own answer is a new interpretation, not a new right: a Human Rights Committee general comment on article 18 and neurotechnologies [AHRC 2025, p. 70](pin:AHRC-2025#p70 \"The United Nations Human Rights Committee provide guidance on freedom of thought and neurotechnologies through the adoption of a general comment on article 18\") ✓.\n\n**(e) Futures Lab.** The submission asks the United Nations to \"develop new human rights standards\" [Futures Lab 2026, p. 7](pin:FuturesLab-2026#p8 \"the United Nations needs to develop new human rights standards that reflect the emerging and rapidly evolving nature of neurotechnology\") ✓, while also presenting neurorights as aligned with articles 12 and 18 of the Universal Declaration [Futures Lab 2026, p. 4](pin:FuturesLab-2026#p5 \"They align with Articles 12 and 18 of the Universal Declaration of Human Rights (UDHR) which protect privacy and freedom of thought, conscience, and religion.\") ✓.\n\n**(f) Szoszkiewicz & Yuste.** They propose \"strengthening existing data protection regulations\" [Szoszkiewicz & Yuste 2025, p. 3469](pin:Szoszkiewicz-Yuste-2025#p1 \"We propose strengthening existing data protection regulations with a broad approach to safeguard neural data\") ✓, yet also see \"growing consensus that additional rules are needed\" [Szoszkiewicz & Yuste 2025, p. 3472](pin:Szoszkiewicz-Yuste-2025#p4 \"national and international regulations signal growing consensus that additional rules are needed\") ✓: existing rights, with new, specific rules on top.\n\n## Contested claims\n\n```contested\nclaim: Existing human rights law, interpreted and clarified, is enough to address neurotechnology in the administration of justice; no new rights are needed.\nverdict: leans-support\nnote: No treaty text or General Comment decides it. The UN reports and the NHRI treat existing law as applicable but in need of clarification; only civil society asks for new standards. \"Clarification\" can itself mean new instruments (guidelines, a general comment), so the two camps are closer than the labels suggest.\n~ c | [A/81/351, para. 16](pin:A/81/351#p6 \"While some contend that the challenges of neurotechnology may require development of new legal frameworks, others affirm that the risks of misuse or abuse of neurotechnology may be addressed within the existing international human rights law framework\") ✓ | records both views without choosing | [[a-81-351]]\n+ c | [A/81/351, para. 48](pin:A/81/351#p15 \"International human rights law provides an applicable framework to address the risks of neurotechnology, but further clarification and consistent application are needed.\") ✓ | the report's own conclusion: applicable, needs clarification | [[a-81-351]]\n+ c | [UNODC–INTERPOL 2025, p. 2](pin:UNODC-INTERPOL-2025#p5 \"updating or clarifying our application of human rights frameworks and standards\") ✓ | clarify existing frameworks | [[unodc-interpol-2025]]\n+ d | [AHRC 2025, p. 30](pin:AHRC-2025#p30 \"these debates appear to be settling in favour of interpreting and adapting existing rights\") ✓ | an NHRI reads the debate as settling; neurorights left out of scope | [[ahrc-2025]]\n- e | [Futures Lab 2026, p. 7](pin:FuturesLab-2026#p8 \"the United Nations needs to develop new human rights standards that reflect the emerging and rapidly evolving nature of neurotechnology\") ✓ | calls for new UN standards | [[futures-lab-2026]]\n~ f | [Szoszkiewicz & Yuste 2025, p. 3472](pin:Szoszkiewicz-Yuste-2025#p4 \"national and international regulations signal growing consensus that additional rules are needed\") ✓ | strengthen existing law, add specific rules | [[szoszkiewicz-yuste-2025]]\n```\n\n**Reading.** The weight lies with \"existing rights, clarified\", but it is the weight of (c) and (d) documents, not of a treaty body. The decisive voice would be the Human Rights Committee itself, which the AHRC asks to adopt a general comment. Until then, this is a policy choice, and an ingest of A/HRC/57/61 ([[a-hrc-57-61]]) adds the Advisory Committee's own view.\n\n## How NOT to read this\n\n- \"Appear to be settling\" is the AHRC's observation of a debate, not a holding that existing rights suffice.\n- Futures Lab's \"new standards\" need not mean new treaty rights: it frames neurorights through the Universal Declaration.\n- Chile's constitutional \"neurorights\" are domestic law ([[regulatory-landscape]]); they show one country's choice, not the state of international law.\n\n## Open questions\n\n- Is a general comment that reads article 18 to cover neural decoding \"interpretation\" or a new right in all but name?\n- What would a new right protect that article 17 privacy and the absolute forum internum do not?\n\n## Related\n\n- [[freedom-of-thought]] (the existing right most often said to suffice)\n- [[mental-privacy]] (the right most often proposed as new)\n- [[neural-data]] (the parallel card on a legal category for the data)\n- [[regulatory-landscape]] (national neurorights and data-protection laws)\n- [[iccpr-art-18]], [[ccpr-c-21-rev-1-add-4]] (the treaty text and the Committee's reading)\n- [[what-should-states-do-now]] (the recommendations that follow from each view)\n- [[a-81-351]], [[ahrc-2025]], [[futures-lab-2026]], [[szoszkiewicz-yuste-2025]], [[unodc-interpol-2025]] (the documents on the card)\n"
  },
  {
   "slug": "selvi-v-state-of-karnataka",
   "type": "entity",
   "title": "Selvi v. State of Karnataka (Supreme Court of India, 2010)",
   "frontmatter": {
    "title": "Selvi v. State of Karnataka (Supreme Court of India, 2010)",
    "type": "entity",
    "tags": [
     "case",
     "india",
     "self-incrimination",
     "brain-based-lie-detection",
     "beos",
     "domestic-law"
    ],
    "register": [
     "c"
    ],
    "status": "reviewed",
    "updated": "2026-11-02",
    "links": [
     "a-81-351",
     "brain-based-lie-detection",
     "self-incrimination",
     "iccpr-art-14-3-g",
     "general-comment-32",
     "consent-in-custody",
     "can-a-suspect-consent-to-lie-detection",
     "iccpr-art-7",
     "reliability-and-admissibility"
    ],
    "sources": [
     "A/81/351"
    ]
   },
   "body": "# Selvi v. State of Karnataka (Supreme Court of India, 2010)\n\n**What it is.** A judgment of the Supreme Court of India on brain-based lie detection, which A/81/351 cites in its footnotes as \"Supreme Court of India, Selvi v. State of Karnataka, Judgment, 5 May 2010\" (footnote 17, PDF p. 4; footnote 63, PDF p. 11, adds \"paras. 215–224\"). It is domestic law. The judgment is not in the library: the wiki knows it only through the Secretary-General's report, a (c) document, and this page carries that register. Nothing here is a reading of the judgment itself.\n\n## In the library\n\nOnly A/81/351 reports the case: twice in the text, three times in footnotes.\n\nIn its survey of brain-based deception detection, the Secretary-General reports the holding and its evidentiary consequence [A/81/351, para. 9](pin:A/81/351#p4 \"The Supreme Court of India held that the involuntary administration of brain electrical oscillation signature profiling tests violates the constitutional protection against self-incrimination and renders the resulting evidence inadmissible\") ✓ (its footnote 17, on the same PDF page, gives the date). The same paragraph adds that the ruling did not end the practice [A/81/351, para. 9](pin:A/81/351#p4 \"However, voluntary use appears to have continued in practice\") ✓.\n\nIn the fair-trial section, the case is placed next to article 14 (3) (g) of the Covenant [A/81/351, para. 32](pin:A/81/351#p10 \"The Supreme Court of India, in Selvi v. State of Karnataka, held that the involuntary administration of brain electrical oscillation signature profiling tests, a form of brain-based lie detection, violates the constitutional protection against self-incrimination\") ✓. The footnote to that sentence (footnote 63, printed on PDF p. 11) pinpoints paras. 215–224 of the judgment and cites alongside it a 2024 European Parliamentary Research Service study on mental privacy.\n\nA third mention sits in a footnote to the paragraph on torture and ill-treatment. That paragraph says brain-based lie detection applied in detention or investigative contexts [A/81/351, para. 28](pin:A/81/351#p9 \"may result in mental or physical suffering contravening the protection provided under articles 7 and 10 (1) of the International Covenant on Civil and Political Rights\") ✓; its footnote 55, on the same PDF page, offers Selvi as an instance that \"established a landmark precedent by prohibiting coercive neuro-imaging techniques as a form of degrading treatment\", adding \"See also A/HRC/57/61\".\n\n**Two framings in one report.** The text (paras. 9 and 32) presents Selvi as a self-incrimination holding; footnote 55 presents it as a degrading-treatment holding. The library contains no text of the judgment and cannot say which description is the better one, or whether both hold. A reader who needs the ground of decision must open the judgment at the paragraphs footnote 63 names.\n\n**What the library does not say.** The facts of the case; the Court's reasoning; whether the Court addressed consent given under inducement; what brain electrical oscillation signature profiling measures, beyond the report's one-line description of the technique family [A/81/351, para. 8](pin:A/81/351#p4 \"These techniques measure physiological or brain responses to determine whether a person recognizes concealed or crime-related information\") ✓. No other library document names the case.\n\n## Related\n\n- [[a-81-351]] (the only document that reports the case)\n- [[brain-based-lie-detection]] (BEOS as one technique among those the report lists)\n- [[self-incrimination]] (the right the text says the Court applied)\n- [[iccpr-art-14-3-g]] and [[general-comment-32]] (the Covenant guarantee and the Committee's reading of \"pressure\")\n- [[iccpr-art-7]] (the footnote-55 framing: degrading treatment)\n- [[consent-in-custody]] and [[can-a-suspect-consent-to-lie-detection]] (\"voluntary use appears to have continued\")\n- [[reliability-and-admissibility]] (the ruling renders the evidence inadmissible)\n"
  }
 ]
}
```

# USER MESSAGE

Build this app. Follow the plan below; where it says nothing, keep it simple.

# Research wiki workspace: neurotechnology in the administration of justice

## Context

A team of human rights professionals follows what ten documents say about neurotechnology in the justice system. The wiki in `WORKSHOP_DATA.wiki` is their compiled knowledge: 40 pages written by models, every claim pinned to a passage of `WORKSHOP_DATA.library` with a verbatim quote. What goes wrong today is upkeep and trust: a new report arrives and nobody reads it into the pages; a chatbot's answer cannot be checked; a report that quotes a General Comment gets cited as if it were one. This app is the workspace: read and navigate, ask the wiki and file good answers back, ingest the waiting document with a person approving each change, and lint. The model drafts; the code verifies every quotation; a person decides. Nothing is called on page load; every call to the model is announced with what leaves the browser.

## What I found in the data

Numbers are from the files I examined; the app computes its own at load.

- 40 pages: 9 source, 14 concept, 14 entity, 3 question; 39 `status` "reviewed", 1 "stub" (`a-hrc-57-61`, an entity page for the inbox document, 11 pins all to other documents, 16 pages linking to it, a ten-item list of what the ingest should check).
- 707 pins, all marked ✓, the number the index states. 625 quotes are whole; 82 join fragments of one passage with "…". A substring check fails those 82; the fragment rule below verifies all 707. Every label matches a passage on its page: "para. N" where the passage has `paragraph` (323 pins), "p. label" where it does not (384).
- Pins per document: A/81/351 227, AHRC-2025 146, UNODC-INTERPOL-2025 78, FuturesLab-2026 75, Szoszkiewicz-Yuste-2025 68, CCPR/C/GC/32 45, CCPR/C/21/Rev.1/Add.4 26, CCPR/C/GC/34 25, Prainsack-et-al-2022 17, A/HRC/57/61 0.
- Six `contested` blocks, one each on six concept pages; the tensions register has the same six cards and five discrepancies of fact. Verdicts: leans-contest 3, contested 2, leans-support 1.
- Links: no dangling `[[slug]]`, no orphan page, `frontmatter.sources` equals the set of pinned documents on every page; `frontmatter.links` and body links differ on 5 entries.
- Sizes: bodies 3,980 to 23,216 characters (median 8,210), 347,911 in all, about 87,000 tokens: no single call can carry the wiki. Index 6,990 characters, log 7,893, tensions 5,568, schema 12,446. Markdown used: headings to `###`, bold, italic, bullets, numbered lists, `[[slug]]`, pins, plain links, fenced `contested` blocks; no tables or images.
- Library: 10 documents; `symbol` null for 5; `paragraph` set in the five UN documents, null in the rest; `page_label` can be "3471" or "e773"; curly quotes in 120 passages, a hyphen followed by a space in 6.
- A/HRC/57/61: `status` "inbox", 100 passages on PDF pages 2–20 (the annex is left out), 61,737 characters, paragraphs 1–84, sub-paragraphs as their own passages ("78 (a)" to "80 (f)"); the passage "5 (a)" holds (b) and (c) inside its text; `section` is a broken fragment for two headings. 13 passages mention justice terms; 29 with evidence, torture and the recommendations.

## The app, tab by tab

The app answers five questions, one per tab, and shows only what the open tab needs (Hick's law): **no view shows more than about seven things to click** (tabs, filter headings and buttons, not table rows or links inside a page's text), and what is used rarely sits one click deeper. There is no filter rail: the one filter narrows the page list, so it sits with the list.

**Header (always visible).** Left: a small monospace label "WIKI · neurotechnology and justice", then the title in serif, "Research wiki: neurotechnology in the administration of justice", then one line from the data: "`pages.length` pages (n sources, n concepts, n entities, n questions) · n pins, n verified by this page · `library.records.length` documents, n in the inbox · built `wiki.built`". Right: a quiet monospace strip "Changes this session: n · Calls to the model: m · Passages that left the browser: k" and, under it, "This page has no storage: changes live in it until you download them (tab 05)". Nothing else.

**Tabs.** Under the header: "01 PAGES · 02 ASK · 03 INGEST · 04 CHECK · 05 RECORD", a `role="tablist"` with arrow keys. `location.hash = slug` opens a page on tab 01, so back and forward work. A running step goes on when you change tab; its tab then reads "03 INGEST · running".

**01 PAGES: what does the wiki say?**
- On the left (320 px), one filter box labelled "title, tag or slug" and a big serif "n of 40 pages". Under it the pages listed by type (plain monospace group labels), each with its `title`, register letters and pin count computed by the code; stubs tagged "stub". Before a page is chosen the main column shows the index, rendered like a page.
- The page: its `title`; badges for `type`, register letters with their names (a treaty law … f scholarship), `status`, `updated`; the `tags`. The `body` rendered: headings, bold, italic, lists, paragraphs; `[[slug]]` as a link to that page (a dangling one in red, "no page"); plain links in a new tab; pins as chips; `contested` blocks as cards.
- Below the body: **Links out** (`frontmatter.links`; those absent from the body marked "frontmatter only"), **Linked from** (every page whose body contains `[[this slug]]`) and **Sources** (`frontmatter.sources`, each with the document's `short_title`, `kind`, `year`, `url`, and "inbox" where it is not ingested). One button, **Copy page as markdown** (frontmatter as YAML, then the body).
- **Pin chips.** The label is a button; clicking it calls `studio.openSource(id, page)`. Beside it, the verification the code computed: "✓ verified" in green or "⚠ not found" in amber, in words as well as colour; where that differs from the mark written in the page, the chip adds "page says ✓" or "page says ⚠". An arrow expands the chip in place: the quote, the matching passage's `paragraph` or `page_label` and its first 300 characters, "Open the PDF page". The document's register letter is on the chip.
- **Contested cards.** From each fenced block: the claim as heading; the verdict in words ("leans contest") first and large, in serif; the note; the lean bar labelled "descriptive: support n% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer"; then the positions as a table with a `caption` (sign in words, register, pin chip, gloss, page link). A link "in the tensions register" (tab 05) when a `###` entry there names this page in `card:`.
- Clickables: 5 tabs, the filter box, Copy page as markdown = 7.

**02 ASK: what does the wiki answer, and is it worth filing?**
- A labelled text box and the button **Ask the wiki** (Enter sends; once there is an answer the same button reads "Ask again"). A grey box above states what each step will send before it goes. Step 1 sends the index and the question; the model returns up to five slugs, shown as chips with a **Change pages** link that lets you tick others. Step 2 sends those pages' bodies, announced as "5 pages, 41,200 characters; 0 library passages have left the browser", and the question. The answer's pins must already stand on the pages sent; one that does not is shown struck through with "not on the pages sent". The answer comes as one text. Each pin chip carries its document's register letter and name ("(c) UN report"), and the prompt says: name the register where it matters, keep the document's own verb, never present (c) to (f) as what the treaty requires. Under the answer, one line counts the verified pins by register.
- The answer is rendered like a page, inside `data-source="ai"`, every pin chip verified by the code, with "What the library cannot answer" from the model's `cannot_answer`. Under it **File as a question page**, which opens the card below in place, with **File this page** and **Copy answer**.
- **Filing a question page.** The card previews the page the code builds: slug from the title (kebab-case, unique), `type` "question", `tags` typed by the user, `register` from the pinned documents, `status` "draft", `updated` today, `links` from the `[[slugs]]` in the answer, `sources` from the pins; body = "# title", "**Short answer.**", "## Reasoning" (the answer), "## What the library cannot answer", "## Related". **File this page** adds it to `pages`, its line to the index under Questions and `## [date] ask | title` to the log. Disabled, with the reason, until every pin in the answer verifies.
- Each step has a progress line and a Stop button (shown while it runs); a parse failure shows the raw answer with "Retry".
- Clickables: 5 tabs, Ask the wiki, File as a question page = 7 (8 once the filing card is open).

**03 INGEST: what would the waiting document change?** Here sit the buttons **Ingest `symbol`** (one per library document whose `status` is "inbox"; `short_title` when `symbol` is null; none, and the line "Nothing waits in the inbox", when it is empty) and, on step 1, **Start**.
- Pressing it opens a stepper of four steps with one running line: "calls so far m · passages sent k"; the button gives way to the stepper.
- **Step 1, scope.** **Scope: the whole document.** The panel says: "All `passages.length` passages will be sent, in batches of 25 (n calls), c characters; nothing is held back." A table lists the batches with their paragraph ranges and PDF pages. **Start** runs them one after another with a progress line ("batch 2 of 4 · 50 of 100 passages have left the browser") and a Stop button that keeps what has returned.
- **Step 2, takeaways.** As each batch returns, a table grows: claim, quote, passage (paragraph and PDF page), the pages it would touch (slugs as chips), and the verification result in words. A box **Could not verify: n** lists each failed quote with the passage the model named, the nearest passage on that page and an **Open the PDF page** button; these claims are in no change card and in no later prompt.
- **Step 3, drafts.** "Draft the source page (1 call)" sends the verified takeaways; the draft appears as a change card. Then "Draft the changes to n pages (n calls)" runs one call per touched page with a progress line and Stop; the stub `a-hrc-57-61` is always among them, rewritten with its ten-item checklist sent along.
- **Step 4, review and file.** Each change is one page: a card with the page's title and type, "new page" or "edited", the number of paragraphs inserted and pins added (verified and not, in words), then the page shown with every inserted paragraph on a pale yellow background and the rest in grey, pins as chips. Two buttons, **Approve this page** and **Reject this page**, and a line "change 3 of 9". Nothing is written until Approve is pressed; a rejected page stays exactly as loaded and the rejection is noted in the log entry. After the last decision, **File the approved changes** writes them at once: pages replaced or added with `updated` today; the index updated (see "Index line" below); `## [date] ingest | symbol: short_title` appended to the log; any new contested card added to the tensions register; the document's `status` set to "ingested" in memory; Lint re-run. Until then nothing in the wiki changes.
- Clickables: 5 tabs plus the Ingest button, or Start, or one draft button, or the two decision buttons of the open change card = 6 to 7 (8 with the per-claim buttons).

**04 CHECK: can I trust this?**
- At the top one big serif number, "n of n pins verified by this page", and "n lint checks need a look".
- **Lint.** A table with a `caption` of checks, each with its count and the pages concerned as links: dangling links; orphans; pins not verified by the code; pins marked ✓ that fail; `sources` that differ from the documents pinned; pages with no pins; `links` not reciprocated; pages missing from the index or index lines without a page; index ✓N that differs from the computed count; contested cards without a tensions entry and the reverse; stub pages; pins to a document still in the inbox. Each reads "0 · pass" or "n · check". One button, **Lint now**, which reads "Re-run" after the first run. The schema's reading for contradictions is named on screen as not done by code.
- **Checks panel** (from "How the app checks itself"), open by default, under the table.
- Clickables: 5 tabs, Lint now = 6.

**05 RECORD: what has changed, where do the sources disagree, and how do I take it away?**
- The `log` rendered newest first (a switch flips it), each `## [date] op | subject` collapsible; below it the `tensions` register, each `card:` link opening its page on tab 01. Entries added in this session carry "this session".
- A short method note (counting, matching and verification are done by the page's code; each number has its "How this is computed" line) and the data source line.
- **Download the wiki**, and, once there are changes, a second button that saves the changed pages as one markdown file.
- Clickables: 5 tabs, the order switch, Download the wiki = 7 (8 with the second download).

**Footer (always visible, one line, small monospace).** `wiki.source`, `wiki.built` and "Counting, matching and verification are done by this page's code; the model is called only when you press Ask, Ingest or a retry button."

## How every number is computed

- **Load.** `P = WORKSHOP_DATA.wiki.pages`, `D = WORKSHOP_DATA.library.records`, maps slug → page and id → document. Per page: `bodyLinks` = the slugs in `/\[\[([^\]|#]+)/g`; `pins` = every match of `/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g` (label, id, page, quote, mark); `backlinks[slug]` = pages whose `bodyLinks` contain it. Header counts are `P.length`, counts by `type`, pins and verified pins summed, documents with `status` "inbox".
- **Normalise** `norm(s)`: Unicode NFKC; “ ” „ → "; ‘ ’ → '; en and em dash → "-"; soft hyphen removed; a hyphen followed by whitespace → "" ("decision- making" = "decision-making"); runs of whitespace → one space; trimmed. Capitals are kept (the schema says words and capitals must match).
- **verify(pin)** = true when a passage `x` of document `id` with `x.page === page` exists such that the quote, split on "…" or "..." into fragments, has every fragment found in `norm(x.text)` in order, each search starting where the previous fragment ended; and the label contains "para. " + `x.paragraph` when `x.paragraph` is set, otherwise "p. " + `x.page_label`. A pin with no quote, an unknown `id`, or a document whose `status` is "inbox" is not verified, with the reason kept for the chip. The 707 pins of the file I examined all verify by this rule.
- **Cite-as** for a document = the most frequent text before ", para." or ", p." in the existing pins' labels to it; with no pins, its `symbol`, or `author` + " " + `year` when `symbol` is null. **New pin** = `[cite-as, para. <paragraph>](pin:id#p<page> "quote") ✓` (", p. <page_label>" when `paragraph` is null); straight double quotes inside the quote become “ ” first, so the regular expression still matches.
- **Register of a document** = the `register` of the source page whose `sources` is exactly [that id], else of the stub page with that `sources`, else "?". A new page's `register` = the registers of its pinned documents.
- **Contested card** from a block: `claim`, `verdict`, `note` by prefix; a position line splits on " | " into sign, register, pin, gloss, page. **Lean** = (Σ weight of "+" + ½ Σ weight of "~") ÷ Σ weight of all positions, weights a 5, b 4, c 3, d 2, e 1, f 0.5, shown as a percentage with the formula.
- **Calls to the model.** One function for every call: it shows the prompt's size in characters and the passage objects in it, adds both to the session counters, calls `await studio.ask(prompt, {json: true})`, parses JSON (once more after stripping a fenced code block), and on failure shows the raw answer with Retry. Every prompt states the pin syntax and "quote only words that stand in the passages given; the code will check".
- **Ask, call 1** = the index + the question → JSON `{pages: [slug…]}`, kept to slugs that exist, at most 5. **Call 2** = the bodies of the chosen pages + the question → JSON `{title, answer, cannot_answer}`, answer at most 350 words. A pin in the answer is accepted when the same `pin:id#pPAGE` with the same quote exists in a sent page's body and `verify` is true; otherwise it is struck through. Characters sent = the lengths of the strings sent, added up; passages sent = 0.
- **Register of a pin** = the register of its document (above), shown on every chip; the count line is one number per letter over the answer's verified pins.
- **Batches** = the document's `passages` in file order, cut every 25; the number of calls = ceil(n ÷ 25). Every passage is sent exactly once.
- **Takeaway call** (one per batch): the batch's passages as `{id, page, paragraph, text}`, the index, and "return JSON {takeaways: [{claim, quote, passage, pages}]}, at most 10, quote 8 to 40 words copied verbatim from that one passage, pages = slugs from the index the claim bears on". For each takeaway the code finds the passage by `id`, builds the pin and runs `verify`; `pages` are kept to slugs that exist, plus at most two new slugs per ingest, which become "new page" cards.
- **Failed takeaway** = `verify` false. It is kept in `failed[]` with the model's quote and the nearest passage (the passage on that page sharing the longest run of consecutive normalised words with the quote, and that run's length), and excluded from every later prompt.
- **Source page call**: the verified takeaways with their ready-made pins, the cite-as, the document's `title`, `author`, `published`, `pages` and `url`, the schema's source-page anatomy (Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related) and "return JSON {one_liner, body, touches: [{slug, why}]}, body at most 900 words, only the pins given, copied exactly". The code re-verifies every pin in `body`, builds the frontmatter itself (`type` "source", `register` from the stub, `sources` [id], `links` from the body, `tags` from the touched slugs) and keeps `touches` to existing or allowed new slugs, at most 12, the stub added if missing.
- **Touched page call** (one per slug): the page's `body`, the takeaways whose `pages` include the slug, with their pins, and "return JSON {edits: [{after, markdown}], contested}, each `after` an existing heading or 'end', at most 300 words in all, pins copied exactly, `contested` a full block only where this document disagrees with the page". The code inserts each `markdown` at the end of the named heading's section (at the end of the page, with a note, when the heading is not found), re-verifies every pin, adds the link both ways in `links` and the document id to `sources`.
- **Index line** = "- [[slug]] — one-liner · (letters) · ✓N", N the verified pins counted by the code; the source page's line goes under Sources, the stub's is replaced, touched pages' N recomputed, the first line rebuilt from the counts. **Log entry**: "Read n passages (cite-as, register (x)). Wrote [[slug]]. N pins in all; besides its own page, pinned on k pages: [[…]]. Rejected: [[…]]." **Tensions entry** for a new card: `### slug-of-claim`, `title`, `status` (contested → open; leans-* → leaning; settled-* → settled), `card: [[page]]`, `poles` and `where` from the positions.
- **Download** = a Blob of JSON in the shape of `WORKSHOP_DATA.wiki` (pages, index, log, tensions, schema, count) plus `changes` (each approved change with date and kind) and `library_status`, saved as `wiki-<date>.json` through a temporary `<a download>`; a second button saves the changed pages as one markdown file with `---` separators.

## How the app checks itself

A panel of one-line checks: what was compared, the values, "pass" in green or "check" in red, with the pages concerned as links. A failing check never hides a page or a pin.

- **Pins.** Pins found by the regular expression against the number stated in the first line of the index (`/(\d[\d,]*) pins/`); verified against found; any ✓ that fails listed with its page.
- **Labels.** Every verified pin's label matches its passage's `paragraph` or `page_label`.
- **Structure.** Dangling links 0; orphans 0; `sources` equal pinned documents on every page; every page in the index and every index `[[slug]]` a page; contested cards equal tensions `card:` entries.
- **Model answers.** For every call: JSON parsed; slugs that do not exist listed; takeaways returned, verified and failed adding up.
- **Coverage.** Passages sent equal `passages.length`; every takeaway's `passage` id is among them; a takeaway naming a passage that was not sent is dropped and counted.
- **Unverified.** After an ingest the count of ⚠ pins in the wiki is unchanged (0 in the file I looked at) and every pin in a changed page verifies; the "could not verify" count plus the verified takeaways equal the takeaways returned.
- **Approval.** Pages changed in the wiki equal approved cards; the log entry lists approved and rejected pages by slug; no page differs from its loaded body without an approved card naming it.
- **Filing.** After filing: the new or changed pages re-parsed and re-verified; the index line count equals the page's verified pins; the log's last entry names the pages changed; Lint re-run and its before and after counts shown side by side.
- **Session.** Changes listed equal the log entries added this session; the download's page count equals `pages.length`.

## Edge cases and risks

- The model may change a quote while "copying" it: every pin is re-verified after every call, never trusted from the mark it wrote. A straight `"` inside a quote would break the pin syntax: the code makes it curly first.
- A sub-paragraph passage ("5 (a)") carries (b) and (c) in its text: the label is the passage's `paragraph` as stored, and the chip shows the passage so a reader sees where the words sit. `section` is broken for two headings of A/HRC/57/61: shown as stored, never used as a heading in a draft.
- Footnotes, tables and captions are not in the passages: a pin cannot verify them; the chip says so.
- A model answer may name a slug that does not exist (dropped and listed) or propose a new page with an existing slug (treated as an edit of that page).
- `studio.ask` can fail or return prose: the raw answer is shown, nothing is filed, Retry re-sends the same prompt; Stop keeps what has returned.
- Everything lives in memory: reloading loses the session, so the warning stays in the header and Download sits on tab 05. The counters show calls and passages before and after each step; a whole ingest of the inbox document is at most about 4 + 1 + 12 calls.
- The lean bar can mislead: the verdict comes first and the bar is labelled descriptive, as the schema requires. Registers are on every chip so a (c) report is never read as (b).

## Design and accessibility

- **What this app adds to the studio look.** Red accent also on the lean bar and the "this session" tag. Big serif numbers: the verified-pin count on tab 04, the running calls and passages on tab 03, the page count on tab 01; the verdict of a contested card is a large serif word. `FIG.01` titles on the lean bar, the takeaways table and the lint table. Category colours only for state, always with words: verified green, not found amber, check red, pass green; register letters stay monospace, not six colours; inserted text on pale yellow with a left border. Tab 01 has two columns (list 320 px, text up to 900 px), one below 900 px.
- From "The A11Y Project checklist": unique, descriptive button labels ("Approve change 3 of 9", "Open A/HRC/57/61 at PDF page 12"); every input has a `<label>`; change cards are a `<fieldset>` with a `<legend>`; chips and borders 3:1.
- From the quality-assurance guidance on generative AI (UK Government Analysis Function): nothing a model wrote enters the wiki before a person has read it, and the prompt box says what leaves the browser before it leaves.
- From Karpathy's "LLM Wiki" and the author's schema: the library is read-only; the index is read before pages; the log is append-only; the three operations are the three buttons (Ask, Ingest, Lint now).
- **Keyboard and screen reader.** Focus is on the first tab on load; `aria-live="polite"` on progress lines, counters and the "Filed" message, and on the "running" mark of a tab; Escape stops a running step; nothing opens in a modal. Every model output sits inside `data-source="ai"`.

## Out of scope

No free-text editing of pages by hand. No PDF viewer inside the app (`studio.openSource` does that). No search beyond the page filter on tab 01. No version history beyond this session's change list. No lint of contradictions by the model. No ingest of a document that is not in the inbox, and no second ingest of the same document. No export other than JSON and markdown.

## Sources consulted

- Andrej Karpathy: "LLM Wiki", a pattern for LLM-maintained knowledge bases (summary) — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Own work: a schema for an LLM-maintained research wiki (page types, frontmatter, direct links, pin verification, registers, contested claims) — unpublished, on the workshop shelf
- Quality assurance of code for analysis and research: Generative AI and "vibe coding" (UK Government Analysis Function) — https://github.com/best-practice-and-impact/qa-of-code-guidance/blob/fa39f2089905fe07c08ae4d66671736a1becd3c5/book/generative_ai.md
- The A11Y Project checklist (content, keyboard, images, tables, colour contrast, forms) — https://github.com/a11yproject/a11yproject.com/blob/090a026713ea81676a03e9b0381a10850d7c955f/src/_data/checklists.json

(Attached: Research wiki: neurotechnology and justice → WORKSHOP_DATA.wiki, with WORKSHOP_DATA.library)

# ASSISTANT MESSAGE (your earlier answer)

I built the wiki workspace in five tabs: Pages, Ask, Ingest, Check and Record. The page verifies every pin itself against the library, and a model is called only when you press Ask, Ingest or a retry button, with the size of what leaves the browser shown first. Ingest waits for your approval of each page before anything is written.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research wiki: neurotechnology and justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5b564c;--ok:#1f6b3a;--warn:#7d4a00;--ins:#fbf0b5;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
[hidden]{display:none!important}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.mono{font:11.5px/1.5 var(--mono);letter-spacing:.07em;text-transform:uppercase}
.mn{font:12px/1.5 var(--mono);color:var(--mute);margin:4px 0}
.mute{color:var(--mute)}
header.wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:22px;padding-bottom:14px}
header h1{font:400 30px/1.15 var(--serif);margin:4px 0 8px;max-width:30ch}
header .src{margin:0;font-size:14px;max-width:70ch}
header .hr{text-align:right;max-width:430px}
header .hr p{margin:2px 0}
#tabwrap{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
[role=tablist]{display:flex;flex-wrap:wrap}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:13px 18px;color:var(--ink);cursor:pointer}
[role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.panel{padding:24px 0 40px}
.q{margin:0 0 14px;color:var(--mute)}
.btn{font:12px var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:9px 14px;cursor:pointer;margin:2px 4px 2px 0}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.btn.sm{padding:3px 8px;font-size:11px}
.btn:disabled{opacity:.45;cursor:not-allowed}
.link{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font:inherit}
h2{font:400 26px/1.2 var(--serif);margin:6px 0 8px}
h3{font:400 20px/1.3 var(--serif);margin:22px 0 6px}
h4{font:700 16px/1.3 var(--serif);margin:16px 0 4px}
.fig{font:400 19px/1.3 var(--serif);margin:24px 0 6px}
.fig .mono{color:var(--red);margin-right:8px}
.big{font:400 52px/1.05 var(--serif);margin:8px 0}
.big small{font:12px var(--mono);letter-spacing:.07em;text-transform:uppercase;color:var(--mute)}
.pg{display:grid;grid-template-columns:320px minmax(0,900px);gap:36px}
@media(max-width:900px){.pg{grid-template-columns:1fr}header .hr{text-align:left}}
input[type=search],input[type=text],textarea{width:100%;font:16px system-ui,sans-serif;padding:8px 10px;border:1px solid var(--ink);background:#fbf9f4;color:var(--ink)}
label{display:block;font:11.5px var(--mono);letter-spacing:.07em;text-transform:uppercase;margin:10px 0 4px}
label.inl{display:inline;text-transform:none;letter-spacing:0;font:14px system-ui,sans-serif}
.grp{margin:16px 0 4px;font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);border-bottom:1px solid var(--rule)}
.li{display:block;padding:6px 8px;border-left:3px solid transparent;text-decoration:none;color:var(--ink);border-bottom:1px solid var(--rule)}
.li[aria-current=page]{border-left-color:var(--red);background:#ece6d8}
.li span{display:block;font:11.5px var(--mono);color:var(--mute)}
.tag{color:var(--red)!important;font-weight:700}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.badge{font:11.5px var(--mono);letter-spacing:.05em;border:1px solid var(--rule);padding:2px 7px}
.md p,.md li{max-width:72ch}
.md h3{border-top:1px solid var(--rule);padding-top:12px}
.md .ins{background:var(--ins);border-left:3px solid #b8960b;padding:3px 10px;margin:8px 0}
.md .ctx{color:#6a655b}
.md pre{white-space:pre-wrap;font:13px var(--mono)}
.dangling{color:var(--red);border-bottom:1px dashed var(--red)}
.pin{display:inline-block;border:1px solid #bdb5a2;background:#fbf9f4;padding:0 4px;margin:0 1px;font-size:14px;line-height:1.5;vertical-align:baseline;max-width:100%}
.pin.struck .pinlab{text-decoration:line-through}
.pinlab{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font:inherit}
.pin .reg{font:11px var(--mono);margin:0 4px}
.vf{font:11px var(--mono);margin-right:4px}
.vf.ok{color:var(--ok)}.vf.no{color:var(--warn)}.vf.diff{color:var(--mute)}
.pinx{background:none;border:0;cursor:pointer;color:var(--ink);padding:0 3px;font-size:13px}
.pinbody{display:block;white-space:normal;max-width:62ch;margin:4px 0 6px;font-size:14px}
.pinbody q{display:block;font-style:italic;margin-bottom:4px}
.pinbody .pl{display:block;margin:2px 0;color:#3b372f}
.pinbody .warn{color:var(--warn)}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:6px 0;color:var(--mute)}
th,td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;vertical-align:top}
th{font:11px var(--mono);letter-spacing:.08em;text-transform:uppercase}
.num{text-align:right;font-variant-numeric:tabular-nums}
.card{border-top:2px solid var(--ink);margin:24px 0;padding-top:10px}
.card .claim{font:700 18px/1.35 var(--serif);margin:0}
.verdict{font:400 44px/1.1 var(--serif);margin:8px 0;color:var(--red)}
.leanbar{height:14px;background:var(--rule);max-width:520px}
.leanbar i{display:block;height:100%;background:var(--red)}
.notice{background:#ebe5d6;border-left:3px solid var(--mute);padding:10px 14px;margin:0 0 14px;font-size:15px}
.chip{display:inline-block;border:1px solid var(--red);color:var(--red);padding:1px 8px;margin:2px 4px 2px 0;font:12px var(--mono)}
fieldset{border:1px solid var(--rule);padding:12px 16px;margin:14px 0}
legend{font:11.5px var(--mono);letter-spacing:.07em;text-transform:uppercase;padding:0 6px}
.steps{display:flex;flex-wrap:wrap;gap:6px 24px;list-style:none;padding:0;margin:8px 0 14px;font:12px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.steps .on{color:var(--red);border-bottom:2px solid var(--red)}
.runline{font:15px var(--serif);margin:6px 0}
.runline b{font:400 40px var(--serif);margin:0 8px 0 4px}
.pass{color:var(--ok);font-weight:700}.check{color:var(--red);font-weight:700}.na{color:var(--mute)}
details{border-bottom:1px solid var(--rule);padding:6px 0}
summary{cursor:pointer;font-weight:600}
.fail{border:1px solid var(--warn);padding:8px 14px;margin:14px 0}
.toast{position:fixed;left:16px;bottom:16px;background:var(--ink);color:#fff;font:12px var(--mono);padding:8px 12px;max-width:80vw}
.sec{border-top:1px solid var(--rule);padding-top:10px}
.ail{margin:0 0 6px}
pre.raw{white-space:pre-wrap;font:12px var(--mono);border:1px solid var(--rule);padding:8px;max-height:260px;overflow:auto}
footer.wrap{border-top:1px solid var(--rule);padding-top:12px;padding-bottom:30px}
footer p{margin:2px 0}
</style>
</head>
<body>
<header class="wrap">
 <div>
  <p class="mono mute" style="margin:0">WIKI · neurotechnology and justice</p>
  <h1>Research wiki: neurotechnology in the administration of justice</h1>
  <p class="src" id="hline"></p>
 </div>
 <div class="hr">
  <p class="mn" id="strip" aria-live="polite"></p>
  <p class="mn">This page has no storage: changes live in it until you download them (tab 05)</p>
 </div>
</header>
<div id="tabwrap"><div class="wrap"><div role="tablist" id="tabs" aria-label="Wiki workspace"></div></div></div>
<main class="wrap">
 <section class="panel" role="tabpanel" id="p0" aria-labelledby="t0">
  <p class="q mono">What does the wiki say?</p>
  <div class="pg">
   <aside>
    <label for="flt">title, tag or slug</label>
    <input type="search" id="flt" autocomplete="off">
    <p class="big" aria-live="polite"><span id="fn">0</span> <small id="ftot"></small></p>
    <p class="mn">How this is computed: pages whose title, slug or a tag contains your text, counted by this page.</p>
    <div id="plist"></div>
   </aside>
   <article id="pview"></article>
  </div>
 </section>
 <section class="panel" role="tabpanel" id="p1" aria-labelledby="t1" hidden>
  <p class="q mono">What does the wiki answer, and is it worth filing?</p>
  <div class="notice" id="notice" aria-live="polite"></div>
  <label for="q">Your question</label>
  <textarea id="q" rows="3"></textarea>
  <p><button class="btn pri" id="askBtn" data-act="askgo">Ask the wiki</button><button class="btn" id="askStop" data-act="stop" hidden>Stop</button> <span class="mn" id="askProg" aria-live="polite"></span></p>
  <div id="askOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>
  <p class="q mono">What would the waiting document change?</p>
  <div id="ingOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p3" aria-labelledby="t3" hidden>
  <p class="q mono">Can I trust this?</p>
  <div id="chkOut"></div>
 </section>
 <section class="panel" role="tabpanel" id="p4" aria-labelledby="t4" hidden>
  <p class="q mono">What has changed, where do the sources disagree, and how do I take it away?</p>
  <p><input type="checkbox" id="newest" checked> <label class="inl" for="newest">Log: newest first</label></p>
  <div id="recOut"></div>
 </section>
</main>
<footer class="wrap"><p class="mn" id="foot"></p></footer>
<div class="toast" id="toast" aria-live="polite" hidden></div>
<script>
(function(){
'use strict';
const FENCE='\x60\x60\x60',INS='<!--ins-->',INE='<!--/ins-->';
const $=(s,r)=>(r||document).querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const uniq=a=>[...new Set(a)];
const today=()=>new Date().toISOString().slice(0,10);
const fmtN=n=>Number(n).toLocaleString('en-GB');
const escRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const slugify=s=>String(s||'').normalize('NFKD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const REGN={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGS={a:'treaty law',b:'General Comment',c:'UN report',d:'NHRI',e:'civil society',f:'scholarship'};
const WGT={a:5,b:4,c:3,d:2,e:1,f:.5};
const PIN_RE=/\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/;
const INL_RE=new RegExp(PIN_RE.source+'|\\[\\[([^\\]|#]+)(?:[|#][^\\]]*)?\\]\\]|\\[([^\\]]+)\\]\\((https?:[^)\\s]+)\\)','g');
const WD=window.WORKSHOP_DATA||{};
const wiki=WD.wiki||{};
const pages=(wiki.pages||[]).map(p=>{const fm=Object.assign({links:[],sources:[],tags:[],register:[]},p.frontmatter||{});['links','sources','tags','register'].forEach(k=>{if(!Array.isArray(fm[k]))fm[k]=[];});return{slug:p.slug,type:p.type||fm.type||'',title:p.title||fm.title||p.slug,frontmatter:fm,body:String(p.body||'')};});
const docs=(WD.library&&WD.library.records)||[];
const docMap=new Map(docs.map(d=>[d.id,d]));
let indexMd=String(wiki.index||''),logMd=String(wiki.log||''),tensMd=String(wiki.tensions||'');
const orig=new Map(pages.map(p=>[p.slug,p.body]));
const S={calls:0,chars:0,passages:0},callLog=[],changes=[],sessionHeads=[],sessionTens=[];
const RUN={ask:null,ingest:null};
let P_MAP=new Map(),backl=new Map(),regCache=new Map(),vCache=new Map(),cur=null,ING=null,warn0=0;
if(!pages.length){document.body.innerHTML='<p style="padding:30px;font-family:sans-serif">No wiki data is attached. Drag the research wiki from "Your files" into the chat.</p>';return;}

/* ---------- normalising, parsing, verifying ---------- */
function normM(s,m){return String(s==null?'':s).normalize('NFKC').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/­/g,'').replace(/-\s+/g,m?'':'-').replace(/\s+/g,' ').trim();}
const norm=s=>normM(s,0);
function pn(x,m){x._n=x._n||[];if(x._n[m]==null)x._n[m]=normM(x.text,m);return x._n[m];}
function parsePins(body){const re=new RegExp(PIN_RE.source,'g');const a=[];let m;while((m=re.exec(body)))a.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5],raw:m[0]});return a;}
function verify(p,o){o=o||{};const k=[p.id,p.page,p.label,p.quote,o.inbox||''].join('\u0001');if(vCache.has(k))return vCache.get(k);const r=verify0(p,o);vCache.set(k,r);return r;}
function verify0(p,o){
 const d=docMap.get(p.id);if(!d)return{ok:false,reason:'unknown document "'+p.id+'"'};
 if(d.status==='inbox'&&o.inbox!==p.id)return{ok:false,reason:'the document is still in the inbox, not in the wiki'};
 if(!p.quote)return{ok:false,reason:'the pin has no quote'};
 const cands=(d.passages||[]).filter(x=>x.page===p.page);
 if(!cands.length)return{ok:false,reason:'no passage starts on PDF page '+p.page};
 let bad=null;
 for(const x of cands){
  let hit=false;
  for(let m=0;m<2&&!hit;m++){
   const t=pn(x,m),fr=p.quote.split(/…|\.\.\./).map(s=>normM(s,m)).filter(Boolean);let pos=0;hit=fr.length>0;
   for(const f of fr){const i=t.indexOf(f,pos);if(i<0){hit=false;break;}pos=i+f.length;}
  }
  if(!hit)continue;
  const want=x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
  if(new RegExp(escRe(want)+'(?![0-9A-Za-z])').test(p.label))return{ok:true,passage:x};
  bad={reason:'label should contain "'+want+'"',passage:x};
 }
 return bad?Object.assign({ok:false},bad):{ok:false,reason:'the quote is not in any passage that starts on PDF page '+p.page};
}
const pinKey=p=>p.id+'|'+p.page+'|'+norm(p.quote);
function reindex(){
 P_MAP=new Map(pages.map(p=>[p.slug,p]));regCache.clear();vCache.clear();backl=new Map();
 for(const p of pages){p._links=uniq([...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()));p._pins=parsePins(p.body);}
 for(const p of pages)for(const s of p._links){if(!backl.has(s))backl.set(s,new Set());backl.get(s).add(p.slug);}
 for(const p of pages)p._pins.forEach(x=>{x.v=verify(x);});
}
function regOf(id){
 if(regCache.has(id))return regCache.get(id);
 const same=(a,b)=>a.length===b.length&&a.every((x,i)=>x===b[i]);
 let sp=pages.find(p=>p.type==='source'&&same(p.frontmatter.sources,[id]))||pages.find(p=>p.frontmatter.status==='stub'&&(same(p.frontmatter.sources,[id])||p.slug===slugify(id)));
 const r=sp&&sp.frontmatter.register.length?sp.frontmatter.register.join(''):'?';regCache.set(id,r);return r;
}
const regLine=id=>{const r=regOf(id);return r==='?'?'(?) register unknown':r.split('').map(x=>'('+x+') '+(REGS[x]||'')).join(', ');};
function citeAs(d){
 const c={};for(const p of pages)for(const x of p._pins)if(x.id===d.id){const t=x.label.split(/, (?:para\.|p\.)/)[0];c[t]=(c[t]||0)+1;}
 const best=Object.entries(c).sort((a,b)=>b[1]-a[1])[0];
 return best?best[0]:(d.symbol||((d.author||'')+' '+(d.year||'')).trim());
}
const mkPin=(d,x,q)=>{const quote=String(q).replace(/"([^"]*)"/g,'“$1”').replace(/"/g,'”').trim();const label=citeAs(d)+', '+(x.paragraph?'para. '+x.paragraph:'p. '+x.page_label);return{label,id:d.id,page:x.page,quote,mark:'✓',raw:'['+label+'](pin:'+d.id+'#p'+x.page+' "'+quote+'") ✓'};};
function parseContested(t){
 const o={claim:'',verdict:'',note:'',pos:[]};
 for(const l of t.split('\n')){let m;
  if((m=l.match(/^claim:\s*(.*)$/)))o.claim=m[1];else if((m=l.match(/^verdict:\s*(.*)$/)))o.verdict=m[1].trim();else if((m=l.match(/^note:\s*(.*)$/)))o.note=m[1];
  else if((m=l.match(/^([+\-~])\s*(.*)$/))){const q=m[2].split(' | ');o.pos.push({sign:m[1],reg:(q[0]||'').trim().toLowerCase(),pin:q[1]||'',gloss:q[2]||'',page:(q[3]||'').trim()});}}
 return o;
}
function lean(pos){let t=0,s=0;for(const p of pos){const w=WGT[p.reg]||0;t+=w;s+=p.sign==='+'?w:p.sign==='~'?w/2:0;}return t?s/t:null;}
const parseTens=()=>tensMd.split(/^###\s+/m).slice(1).map((t,i)=>{const nl=t.indexOf('\n'),m=t.match(/card:\**\s*\[\[([^\]|#]+)/);return{i,head:(nl<0?t:t.slice(0,nl)).trim(),card:m?m[1].trim():null,body:nl<0?'':t.slice(nl+1)};});
const parseLog=()=>logMd.split(/^##\s+/m).slice(1).map(t=>{const nl=t.indexOf('\n');return{head:(nl<0?t:t.slice(0,nl)).trim(),body:nl<0?'':t.slice(nl+1).trim()};});
const hasCards=p=>p.body.includes(FENCE+'contested');
function plainFirst(md,n){n=n||170;let t=String(md||'').split('\n').filter(l=>l.trim()&&!/^#/.test(l)&&!l.startsWith('<!--'))[0]||'';const m=t.match(/\*\*One-liner\.\*\*\s*(.*)/);if(m)t=m[1];t=t.replace(new RegExp(PIN_RE.source,'g'),'').replace(/\[\[([^\]|#]+)\]\]/g,'$1').replace(/\[([^\]]+)\]\([^)]*\)/g,'$1').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();return t.length>n?t.slice(0,n-1).replace(/\s+\S*$/,'')+'…':t;}
const stripIns=b=>b.replace(/^<!--\/?ins-->\n?/gm,'').replace(/\n{3,}/g,'\n\n');
const insPart=b=>{const o=[];b.replace(/<!--ins-->\n([\s\S]*?)\n<!--\/ins-->/g,(m,x)=>{o.push(x);return m;});return o.join('\n\n');};
function insertAt(body,after,md){
 const L=body.replace(/\s+$/,'').split('\n'),block=['',INS,md.trim(),INE,''];let note=null;
 if(after&&after!=='end'){
  const want=norm(String(after).replace(/^#+\s*/,'')).toLowerCase(),i=L.findIndex(l=>/^#{1,6}\s/.test(l)&&norm(l.replace(/^#+\s*/,'')).toLowerCase()===want);
  if(i>=0){const lv=L[i].match(/^#+/)[0].length;let e=i+1;while(e<L.length){const m=L[e].match(/^(#{1,6})\s/);if(m&&m[1].length<=lv)break;e++;}while(e>i+1&&!L[e-1].trim())e--;L.splice(e,0,...block);return{body:L.join('\n'),note};}
  note='heading "'+after+'" not found; added at the end of the page';
 }
 L.push(...block);return{body:L.join('\n'),note};
}

/* ---------- markdown rendering ---------- */
const fmt=t=>esc(t).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/(^|[\s(])\*(?!\s)(.+?)\*(?=[\s).,;:!?]|$)/g,'$1<em>$2</em>');
function inline(s,ctx){
 ctx=ctx||{};const re=new RegExp(INL_RE.source,'g');let out='',last=0,m;
 while((m=re.exec(s))){
  out+=fmt(s.slice(last,m.index));last=re.lastIndex;
  if(m[2])out+=pinChip({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]},ctx);
  else if(m[6]){const sl=m[6].trim();out+=P_MAP.has(sl)?'<a href="#'+esc(sl)+'">'+esc(P_MAP.get(sl).title)+'</a>':'<span class="dangling">'+esc(sl)+' (no page)</span>';}
  else out+='<a href="'+esc(m[8])+'" target="_blank" rel="noopener">'+fmt(m[7])+'</a>';
 }
 return out+fmt(s.slice(last));
}
function pinChip(p,ctx){
 const r=ctx.pinCheck?ctx.pinCheck(p):verify(p),d=docMap.get(p.id),reg=regOf(p.id),x=r.passage;
 let h='<span class="pin'+(r.struck?' struck':'')+'"><button type="button" class="pinlab" data-id="'+esc(p.id)+'" data-page="'+p.page+'" aria-label="Open '+esc(p.label)+' at PDF page '+p.page+'">'+esc(p.label)+'</button>';
 h+='<span class="reg" title="'+esc(REGN[reg]||'')+'">('+esc(reg)+')</span><span class="vf '+(r.ok?'ok':'no')+'">'+(r.ok?'✓ verified':'⚠ not found')+'</span>';
 if(r.note)h+='<span class="vf no">'+esc(r.note)+'</span>';
 if(r.ok?p.mark!=='✓':p.mark==='✓')h+='<span class="vf diff">page says '+esc(p.mark)+'</span>';
 h+='<button type="button" class="pinx" aria-expanded="false" aria-label="Show the quote for '+esc(p.label)+'">▾</button><span class="pinbody" hidden>';
 h+=p.quote?'<q>'+esc(p.quote)+'</q>':'<em>no quote in this pin</em>';
 h+='<span class="pl">Document: '+(d?esc((d.symbol||d.short_title)+' · '+d.kind+' · '+d.year+(d.status==='inbox'?' · inbox':'')):'unknown')+' · register '+esc(regLine(p.id))+'</span>';
 if(x)h+='<span class="pl">Passage: '+(x.paragraph?'para. '+esc(x.paragraph):'p. '+esc(x.page_label))+' (PDF page '+x.page+'): '+esc(x.text.slice(0,300))+(x.text.length>300?'…':'')+'</span>';
 if(!r.ok)h+='<span class="pl warn">Not verified: '+esc(r.reason||r.note||'')+'. Footnotes, tables and captions are not in the passages, so a pin cannot verify them.</span>';
 return h+'<button type="button" class="openpdf btn sm" data-id="'+esc(p.id)+'" data-page="'+p.page+'" aria-label="Open '+esc(d?d.symbol||d.short_title:p.id)+' at PDF page '+p.page+'">Open the PDF page</button></span></span>';
}
function contestedCard(txt,ctx){
 const c=parseContested(txt),L=lean(c.pos),te=ctx.slug?parseTens().find(e=>e.card===ctx.slug):null,SG={'+':'supports','-':'contests','~':'mixed'};
 let h='<section class="card"><p class="claim">'+inline(c.claim,ctx)+'</p><p class="verdict">'+esc((c.verdict||'no verdict').replace(/-/g,' '))+'</p><p>'+inline(c.note,ctx)+'</p>';
 if(te)h+='<p class="mn"><button class="link" data-act="gotens" data-arg="'+te.i+'">in the tensions register</button></p>';
 h+='<h4 class="fig"><span class="mono">FIG.01</span> Lean bar</h4>';
 h+=L==null?'<p class="mn">No weighted positions.</p>':'<div class="leanbar" role="img" aria-label="support '+Math.round(L*100)+' percent"><i style="width:'+Math.round(L*100)+'%"></i></div><p class="mn">descriptive: support '+Math.round(L*100)+'% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</p>';
 h+='<table><caption>Positions on this claim</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>';
 h+=c.pos.map(p=>'<tr><td>'+(SG[p.sign]||p.sign)+'</td><td>('+esc(p.reg)+') '+esc(REGS[p.reg]||'')+'</td><td>'+inline(p.pin,ctx)+'</td><td>'+inline(p.gloss,ctx)+'</td><td>'+inline(p.page,ctx)+'</td></tr>').join('');
 return h+'</tbody></table></section>';
}
function renderMd(md,ctx){
 ctx=ctx||{};const L=String(md||'').replace(/\r/g,'').split('\n'),out=[];let i=0,ins=false;
 const cl=()=>ctx.mark?(ins?' class="ins"':' class="ctx"'):'';
 const bul=/^\s*[-*]\s+/,num=/^\s*\d+[.)]\s+/;
 while(i<L.length){
  const ln=L[i];
  if(ln.trim()===INS){ins=true;i++;continue;}
  if(ln.trim()===INE){ins=false;i++;continue;}
  const f=ln.match(/^\x60\x60\x60(\w*)\s*$/);
  if(f){const buf=[];i++;while(i<L.length&&!/^\x60\x60\x60\s*$/.test(L[i])){buf.push(L[i]);i++;}i++;
   out.push(f[1]==='contested'?(ctx.mark?'<div'+cl()+'>':'<div>')+contestedCard(buf.join('\n'),ctx)+'</div>':'<pre'+cl()+'>'+esc(buf.join('\n'))+'</pre>');continue;}
  const hm=ln.match(/^(#{1,6})\s+(.*)$/);
  if(hm){const lv=Math.min(hm[1].length+2,6);out.push('<h'+lv+cl()+'>'+inline(hm[2],ctx)+'</h'+lv+'>');i++;continue;}
  if(bul.test(ln)||num.test(ln)){
   const ord=num.test(ln),re=ord?num:bul,items=[];
   while(i<L.length&&re.test(L[i])){let t=L[i].replace(re,'');i++;while(i<L.length&&/^\s{2,}\S/.test(L[i])&&!bul.test(L[i])&&!num.test(L[i])){t+=' '+L[i].trim();i++;}items.push(t);}
   out.push('<'+(ord?'ol':'ul')+cl()+'>'+items.map(t=>'<li>'+inline(t,ctx)+'</li>').join('')+'</'+(ord?'ol':'ul')+'>');continue;}
  if(!ln.trim()){i++;continue;}
  const buf=[ln];i++;
  while(i<L.length&&L[i].trim()&&!/^(#{1,6}\s|\x60\x60\x60|<!--)/.test(L[i])&&!bul.test(L[i])&&!num.test(L[i])){buf.push(L[i]);i++;}
  out.push('<p'+cl()+'>'+inline(buf.join(' '),ctx)+'</p>');
 }
 return out.join('\n');
}

/* ---------- header, tabs, helpers ---------- */
const TABS=['PAGES','ASK','INGEST','CHECK','RECORD'];
const tabLabel=i=>'0'+(i+1)+' '+TABS[i]+(((i===1&&RUN.ask)||(i===2&&RUN.ingest))?' · running':'');
let toastT=null;
function say(m){const t=$('#toast');t.textContent=m;t.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>{t.hidden=true;},4500);}
function buildTabs(){
 $('#tabs').innerHTML=TABS.map((n,i)=>'<button role="tab" id="t'+i+'" aria-controls="p'+i+'" aria-selected="'+(i===0)+'" tabindex="'+(i===0?0:-1)+'">'+tabLabel(i)+'</button>').join('');
 $('#tabs').addEventListener('keydown',e=>{
  const i=TABS.findIndex((_,k)=>$('#t'+k)===document.activeElement);if(i<0)return;
  const k={ArrowRight:(i+1)%5,ArrowLeft:(i+4)%5,Home:0,End:4}[e.key];if(k==null)return;e.preventDefault();selectTab(k,true);
 });
 $('#tabs').addEventListener('click',e=>{const b=e.target.closest('[role=tab]');if(b)selectTab(+b.id.slice(1),false);});
}
function selectTab(i,focus){TABS.forEach((_,k)=>{const t=$('#t'+k);t.setAttribute('aria-selected',k===i);t.tabIndex=k===i?0:-1;$('#p'+k).hidden=k!==i;});if(focus)$('#t'+i).focus();}
function updTabs(){TABS.forEach((_,k)=>{const t=$('#t'+k);if(t)t.textContent=tabLabel(k);});}
const allPins=()=>pages.flatMap(p=>p._pins);
function updHeader(){
 const t={};pages.forEach(p=>{t[p.type]=(t[p.type]||0)+1;});
 const nm=[['source','source','sources'],['concept','concept','concepts'],['entity','entity','entities'],['question','question','questions']];
 const parts=nm.map(([k,s,pl])=>(t[k]||0)+' '+((t[k]||0)===1?s:pl));
 Object.keys(t).filter(k=>!nm.some(n=>n[0]===k)).forEach(k=>parts.push(t[k]+' '+(k||'other')));
 const ap=allPins(),ok=ap.filter(x=>x.v.ok).length,inbox=docs.filter(d=>d.status==='inbox').length;
 $('#hline').textContent=pages.length+' pages ('+parts.join(', ')+') · '+fmtN(ap.length)+' pins, '+fmtN(ok)+' verified by this page · '+docs.length+' documents, '+inbox+' in the inbox · built '+(wiki.built||'date unknown');
 $('#strip').textContent='Changes this session: '+changes.length+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;
 $('#foot').textContent=(wiki.source||'research wiki')+' · built '+(wiki.built||'unknown')+' · Counting, matching and verification are done by this page\'s code; the model is called only when you press Ask, Ingest or a retry button.';
}
async function copyText(t){try{await navigator.clipboard.writeText(t);return true;}catch(e){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();let ok=false;try{ok=document.execCommand('copy');}catch(_){}a.remove();return ok;}}
function openSrc(id,page){if(window.studio&&studio.openSource)studio.openSource(id,page);else say('The PDF viewer is not available in this preview.');}
function startRun(k){const r={stopped:false};r.sig=new Promise(res=>{r.halt=()=>{r.stopped=true;res('\u0000stopped');};});RUN[k]=r;updTabs();return r;}
function endRun(k){RUN[k]=null;updTabs();}
const yamlOf=fm=>Object.entries(fm).map(([k,v])=>k+': '+(Array.isArray(v)?'['+v.map(x=>JSON.stringify(x)).join(', ')+']':JSON.stringify(v))).join('\n');
const pageMd=p=>'---\n'+yamlOf(p.frontmatter)+'\n---\n\n'+p.body;
function parseJSON(raw){
 const t=String(raw||'').trim(),tries=[t,t.replace(/^\x60\x60\x60(?:json)?\s*/i,'').replace(/\s*\x60\x60\x60$/,''),t.slice(t.indexOf('{'),t.lastIndexOf('}')+1)];
 for(const s of tries){try{const v=JSON.parse(s);if(v&&typeof v==='object')return v;}catch(e){}}return null;
}
const PRE='You are helping maintain a research wiki on neurotechnology in the administration of justice. A pin is written [label](pin:DOCUMENT_ID#pPDFPAGE "verbatim quote") ✓ . Quote only words that stand in the passages given; the code will check every quote against the library and discards anything that does not match. Copy pins exactly as given. Reply with JSON only.\n\n';
async function callModel(prompt,o){
 o=o||{};const E={label:o.label,chars:prompt.length,passages:o.passages||0,parsed:false,unknown:0};callLog.push(E);
 S.calls++;S.chars+=prompt.length;S.passages+=E.passages;updHeader();
 let res;
 try{
  if(!window.studio||!studio.ask)throw new Error('studio.ask is not available here');
  const p=studio.ask(prompt,{json:true});res=await(o.run?Promise.race([p,o.run.sig]):p);
 }catch(e){return{ok:false,raw:'',error:String(e&&e.message||e),E};}
 if(res==='\u0000stopped')return{ok:false,stopped:true,E};
 const raw=typeof res==='string'?res:JSON.stringify(res),data=(res&&typeof res==='object')?res:parseJSON(raw);
 if(!data)return{ok:false,raw,error:'The answer was not valid JSON.',E};
 E.parsed=true;return{ok:true,data,raw,E};
}
const errHTML=(e,act)=>'<div class="fail"><p><strong>'+esc(e.error)+'</strong> Nothing was filed.</p>'+(e.raw?'<pre class="raw" data-source="ai">'+esc(e.raw)+'</pre>':'')+'<button class="btn" data-act="'+act+'">Retry</button></div>';
function download(name,text,type){const u=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);}

/* ---------- tab 01 pages ---------- */
function renderList(){
 const q=$('#flt').value.trim().toLowerCase();
 const hit=pages.filter(p=>!q||(p.title+' '+p.slug+' '+p.frontmatter.tags.join(' ')).toLowerCase().includes(q));
 $('#fn').textContent=hit.length;$('#ftot').textContent='of '+pages.length+' pages';
 const types=uniq(['source','concept','entity','question',...pages.map(p=>p.type)]);
 $('#plist').innerHTML=types.map(t=>{
  const g=hit.filter(p=>p.type===t);if(!g.length)return'';
  return'<p class="grp">'+esc(t||'other')+' ('+g.length+')</p>'+g.map(p=>'<a class="li" href="#'+esc(p.slug)+'"'+(cur===p.slug?' aria-current="page"':'')+'>'+esc(p.title)+'<span>'+(p.frontmatter.register.join(' ')||'-')+' · '+p._pins.length+' pins'+(p.frontmatter.status==='stub'?' · <b class="tag">stub</b>':'')+'</span></a>').join('');
 }).join('')||'<p class="mn">No page matches.</p>';
}
function pageHTML(p){
 const fm=p.frontmatter,bodyL=new Set(p._links),from=[...(backl.get(p.slug)||[])].filter(s=>s!==p.slug);
 const lk=s=>P_MAP.has(s)?'<a href="#'+esc(s)+'">'+esc(P_MAP.get(s).title)+'</a>':'<span class="dangling">'+esc(s)+' (no page)</span>';
 let h='<p class="mn"><a href="#">← index</a></p><h2>'+esc(p.title)+'</h2><p class="badges"><span class="badge">'+esc(p.type)+'</span>'+fm.register.map(r=>'<span class="badge">('+esc(r)+') '+esc(REGN[r]||'')+'</span>').join('')+'<span class="badge">'+esc(fm.status||'no status')+'</span><span class="badge">updated '+esc(fm.updated||'?')+'</span>'+(changes.some(c=>c.slug===p.slug)?'<span class="badge" style="color:var(--red)">this session</span>':'')+'</p>';
 h+='<p class="mn">tags: '+(fm.tags.map(esc).join(' · ')||'none')+'</p><div class="md">'+renderMd(p.body.replace(/^#\s+[^\n]*\n+/,''),{slug:p.slug})+'</div>';
 h+='<h3 class="sec">Links out</h3><ul>'+(fm.links.map(s=>'<li>'+lk(s)+(bodyL.has(s)?'':' <span class="mn">frontmatter only</span>')+'</li>').join('')||'<li class="mn">none</li>')+'</ul>';
 h+='<h3>Linked from</h3><ul>'+(from.map(s=>'<li>'+lk(s)+'</li>').join('')||'<li class="mn">no page links here</li>')+'</ul>';
 h+='<h3>Sources</h3><ul>'+(fm.sources.map(id=>{const d=docMap.get(id);return'<li>'+(d?esc(d.short_title||d.title)+' · '+esc(d.kind)+' · '+esc(d.year)+' · <a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.symbol||d.url)+'</a>'+(d.status==='inbox'?' · <b class="tag">inbox</b>':''):esc(id)+' (not in the library)')+'</li>';}).join('')||'<li class="mn">none</li>')+'</ul>';
 return h+'<p><button class="btn" data-act="copymd" data-arg="'+esc(p.slug)+'">Copy page as markdown</button></p>';
}
function renderView(){
 const v=$('#pview');
 if(!cur){v.innerHTML='<h2>Index</h2><p class="mn">The catalog of every page. Pick a page on the left or follow a link.</p><div class="md">'+renderMd(indexMd,{})+'</div>';return;}
 const p=P_MAP.get(cur);
 v.innerHTML=p?pageHTML(p):'<p class="mn"><a href="#">← index</a></p><h2>No page "'+esc(cur)+'"</h2><p>The wiki has no page with this slug.</p>';
}
function route(){let h='';try{h=decodeURIComponent(location.hash.slice(1));}catch(e){h=location.hash.slice(1);}cur=h||null;if(h)selectTab(0);renderList();renderView();if(h)window.scrollTo(0,0);}

/* ---------- tab 02 ask ---------- */
const ask={stage:'idle',q:'',chosen:[],sentKeys:new Set(),answer:null,err:null,filing:false,pickOpen:false,fTitle:'',fTags:'',filed:null,prog:''};
const bodiesFor=sl=>sl.map(s=>'=== PAGE '+s+' ===\n'+P_MAP.get(s).body).join('\n\n');
const q1Prompt=q=>PRE+'Choose the wiki pages needed to answer the question. Below is the wiki index. Return JSON {"pages": [slug, ...]} with at most 5 slugs that appear in the index.\n\nQUESTION: '+q+'\n\nINDEX:\n'+indexMd;
const q2Prompt=(q,sl)=>PRE+'Answer the question using only the wiki pages below. Return JSON {"title": short title, "answer": markdown of at most 350 words, "cannot_answer": one or two sentences on what the library cannot answer}. Every claim in the answer carries a pin copied exactly from the pages below, and may link to the pages you used as [[slug]]. Name the register where it matters ((a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship), keep the document\'s own verb, and never present (c) to (f) as what the treaty requires.\n\nQUESTION: '+q+'\n\n'+bodiesFor(sl);
function renderAskTop(){
 const n=$('#notice'),b=$('#askBtn'),q=($('#q').value||'').trim(),busy=!!RUN.ask;
 if(ask.stage==='pick'&&ask.chosen.length){const pr=q2Prompt(ask.q,ask.chosen);n.innerHTML='Step 2 will send '+ask.chosen.length+' page'+(ask.chosen.length===1?'':'s')+', '+fmtN(pr.length)+' characters (page bodies, instructions and the question) to a language model; 0 library passages have left the browser.';b.textContent='Send '+ask.chosen.length+' page'+(ask.chosen.length===1?'':'s')+' and the question';}
 else{n.innerHTML='Step 1 will send the wiki index ('+fmtN(indexMd.length)+' characters) and your question ('+fmtN(q.length)+' characters) to a language model. No page body and no library passage is sent in this step.';b.textContent=ask.answer?'Ask again':'Ask the wiki';}
 b.disabled=busy;$('#askStop').hidden=!busy;$('#askProg').textContent=ask.prog;
}
function renderAskOut(){
 let h='';
 if(ask.err)h+=errHTML(ask.err,'askretry');
 if(ask.stage==='pick'){
  h+='<h3 class="fig"><span class="mono">STEP 1</span> Pages chosen by the model</h3><p data-source="ai">'+(ask.chosen.map(s=>'<span class="chip">'+esc(P_MAP.get(s).title)+'</span>').join('')||'<span class="mn">none chosen</span>')+'</p><p class="mn"><button class="link" data-act="pickopen" aria-expanded="'+ask.pickOpen+'">Change pages</button></p>';
  if(ask.pickOpen)h+='<fieldset><legend>Tick the pages to send (at most 5)</legend>'+pages.map(p=>'<div><input type="checkbox" name="pick" id="pk-'+esc(p.slug)+'" value="'+esc(p.slug)+'"'+(ask.chosen.includes(p.slug)?' checked':'')+'> <label class="inl" for="pk-'+esc(p.slug)+'">'+esc(p.title)+'</label></div>').join('')+'</fieldset>';
 }
 if(ask.answer)h+=answerHTML();
 $('#askOut').innerHTML=h;
}
function askPinCheck(p){const v=verify(p);if(!ask.sentKeys.has(pinKey(p)))return Object.assign({},v,{ok:false,struck:true,note:'not on the pages sent'});return v;}
function answerHTML(){
 const a=ask.answer,ctx={pinCheck:askPinCheck},pins=parsePins(a.answer),by={};let bad=0;
 pins.forEach(p=>{const r=askPinCheck(p);if(r.ok){const g=regOf(p.id);by[g]=(by[g]||0)+1;}else bad++;});
 let h='<h3 class="fig"><span class="mono">STEP 2</span> Answer</h3><div class="md" data-source="ai"><h3 style="border:0;margin-top:0">'+esc(a.title)+'</h3>'+renderMd(a.answer,ctx)+'<h4>What the library cannot answer</h4><p>'+esc(a.cannot||'The model gave no answer to this.')+'</p></div>';
 h+='<p class="mn">How this is computed: '+pins.length+' pins in the answer; verified by register: '+(Object.entries(by).map(([k,n])=>'('+k+') '+(REGS[k]||'?')+' '+n).join(' · ')||'none')+'; not verified or not on the pages sent: '+bad+'.</p>';
 h+='<p><button class="btn pri" data-act="filecard" aria-expanded="'+ask.filing+'">File as a question page</button></p>';
 if(ask.filing)h+='<fieldset><legend>File as a question page</legend><label for="fT">Title</label><input type="text" id="fT" value="'+esc(ask.fTitle)+'"><label for="fG">Tags, separated by commas</label><input type="text" id="fG" value="'+esc(ask.fTags)+'"><div id="fPrev"></div></fieldset>';
 return h;
}
function buildQuestion(){
 const a=ask.answer,title=(ask.fTitle||a.title).trim(),pins=parsePins(a.answer),bad=pins.filter(p=>!askPinCheck(p).ok).length;
 let slug=slugify(title).slice(0,60)||'question',k=slug,n=2;while(P_MAP.has(slug)){slug=k+'-'+n++;}
 const ids=uniq(pins.map(p=>p.id)),regs=uniq(ids.flatMap(id=>regOf(id).split('')).filter(x=>'abcdef'.includes(x))).sort();
 const links=uniq([...a.answer.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>P_MAP.has(s));
 const paras=a.answer.trim().split(/\n\s*\n/),body='# '+title+'\n\n**Short answer.** '+paras[0]+'\n\n## Reasoning\n\n'+(paras.length>1?paras.slice(1).join('\n\n'):a.answer.trim())+'\n\n## What the library cannot answer\n\n'+(a.cannot||'Not stated.')+'\n\n## Related\n\n'+(links.map(s=>'- [[' + s + ']]').join('\n')||'- none')+'\n';
 const fm={title,type:'question',tags:ask.fTags.split(',').map(s=>s.trim()).filter(Boolean),register:regs,status:'draft',updated:today(),links,sources:ids};
 return{page:{slug,type:'question',title,frontmatter:fm,body},bad,pins:pins.length};
}
function updFile(){
 const el=$('#fPrev');if(!el||!ask.answer)return;const b=buildQuestion(),fm=b.page.frontmatter;
 const why=b.pins===0?'the answer has no pins':b.bad?b.bad+' pin'+(b.bad===1?'':'s')+' in the answer do not verify':'';
 el.innerHTML='<p class="mn">preview · slug '+esc(b.page.slug)+' · type question · status draft · updated '+fm.updated+' · register '+esc(fm.register.join('')||'-')+' · links '+fm.links.length+' · sources '+fm.sources.length+'</p><div class="md" style="border:1px solid var(--rule);padding:6px 14px">'+renderMd(b.page.body,{pinCheck:askPinCheck})+'</div><p><button class="btn pri" data-act="filedo"'+(why?' disabled':'')+'>File this page</button><button class="btn" data-act="copyans">Copy answer</button>'+(why?' <span class="mn">File this page is disabled: '+esc(why)+'.</span>':'')+'</p>';
}
function idxUpsert(slug,type,line){
 const L=indexMd.split('\n'),k=L.findIndex(l=>/^\s*[-*]\s/.test(l)&&l.includes('[['+slug+']]'));
 if(k>=0){L[k]=line;indexMd=L.join('\n');return;}
 const name={source:'Sources',concept:'Concepts',entity:'Entities',question:'Questions'}[type]||'Other',h=L.findIndex(l=>/^#{1,4}\s/.test(l)&&l.toLowerCase().includes(name.toLowerCase()));
 if(h<0){indexMd=indexMd.replace(/\s*$/,'')+'\n\n## '+name+'\n\n'+line+'\n';return;}
 let e=h+1,last=h;while(e<L.length&&!/^#{1,4}\s/.test(L[e])){if(/^\s*[-*]\s/.test(L[e]))last=e;e++;}
 L.splice(last+1,0,line);indexMd=L.join('\n');
}
function idxCounts(){
 const t={};pages.forEach(p=>{t[p.type]=(t[p.type]||0)+1;});const ok=allPins().filter(x=>x.v.ok).length;
 let h=indexMd.slice(0,800);const rest=indexMd.slice(800);
 h=h.replace(/(\d[\d,]*)(\s+pins)/,(m,a,b)=>(a.includes(',')?fmtN(ok):ok)+b).replace(/(\d+)(\s+pages)/,(m,a,b)=>pages.length+b);
 [['source','sources?'],['concept','concepts?'],['entity','(?:entities|entity)'],['question','questions?']].forEach(([k,re])=>{h=h.replace(new RegExp('(\\d+)(\\s+'+re+'\\b)','i'),(m,a,b)=>(t[k]||0)+b);});
 indexMd=h+rest;
}
function appendLog(head,body){logMd=logMd.replace(/\s*$/,'')+'\n\n## '+head+'\n'+body+'\n';sessionHeads.push(head);}
async function askStep1(){
 const q=$('#q').value.trim();if(!q){ask.prog='Type a question first.';renderAskTop();return;}
 Object.assign(ask,{q,answer:null,filing:false,err:null,chosen:[],stage:'idle',pickOpen:false,prog:'Step 1: sending the index and the question…'});
 const run=startRun('ask');renderAskTop();renderAskOut();
 const r=await callModel(q1Prompt(q),{label:'Ask: choose pages',run});endRun('ask');
 if(r.stopped){ask.prog='Stopped.';renderAskTop();return;}
 if(!r.ok){ask.err={error:r.error,raw:r.raw,retry:1};ask.prog='';renderAskTop();renderAskOut();return;}
 const sl=(Array.isArray(r.data.pages)?r.data.pages:[]).map(String),keep=uniq(sl.filter(s=>P_MAP.has(s))).slice(0,5);
 r.E.unknown=sl.filter(s=>!P_MAP.has(s)).length;ask.chosen=keep;ask.stage='pick';
 ask.prog=keep.length?'The model chose '+keep.length+' page'+(keep.length===1?'':'s')+(r.E.unknown?' ('+r.E.unknown+' slug'+(r.E.unknown===1?'':'s')+' that do not exist dropped)':'')+'.':'The model chose no page that exists. Tick pages yourself under "Change pages".';
 updHeader();renderAskTop();renderAskOut();
}
async function askStep2(){
 if(!ask.chosen.length){ask.prog='Choose at least one page first.';renderAskTop();return;}
 ask.err=null;ask.prog='Step 2: sending '+ask.chosen.length+' pages and the question…';ask.sentKeys=new Set(ask.chosen.flatMap(s=>parsePins(P_MAP.get(s).body).map(pinKey)));
 const run=startRun('ask');renderAskTop();
 const r=await callModel(q2Prompt(ask.q,ask.chosen),{label:'Ask: answer',run});endRun('ask');
 if(r.stopped){ask.prog='Stopped.';renderAskTop();return;}
 if(!r.ok){ask.err={error:r.error,raw:r.raw,retry:2};ask.prog='';renderAskTop();renderAskOut();return;}
 const d=r.data,cn=d.cannot_answer;
 ask.answer={title:String(d.title||ask.q.slice(0,80)).trim(),answer:String(d.answer||'').trim(),cannot:Array.isArray(cn)?cn.join(' '):String(cn||'')};
 if(!ask.answer.answer){ask.answer=null;ask.err={error:'The answer was empty.',raw:r.raw,retry:2};}
 ask.stage='done';ask.fTitle=ask.answer?ask.answer.title:'';ask.fTags='';ask.prog='Answer received. Every pin below was checked by this page.';
 renderAskTop();renderAskOut();
}
function fileQuestion(){
 const b=buildQuestion();if(b.bad||!b.pins)return;const p=b.page,date=today(),n=p.frontmatter.sources.length;
 pages.push(p);reindex();
 idxUpsert(p.slug,'question','- [[' + p.slug + ']] — ' + plainFirst(p.body.replace(/^#[^\n]*\n+/,'').replace('**Short answer.**','')) + ' · (' + p.frontmatter.register.join('') + ') · ✓' + p._pins.filter(x=>x.v.ok).length);
 idxCounts();const head='['+date+'] ask | '+p.title;
 appendLog(head,'Filed [[' + p.slug + ']] as a draft question page from the pages '+ask.chosen.map(s=>'[['+s+']]').join(', ')+'. '+p._pins.length+' pins, all verified by the code, on '+n+' document'+(n===1?'':'s')+'.');
 changes.push({date,kind:'ask',slug:p.slug,change:'new',op:head});
 ask.filed=p.slug;ask.filing=false;ask.prog='Filed: '+p.title+'. It is a draft page in memory; download it on tab 05.';
 refreshAll();say('Filed as a question page.');
}

/* ---------- lint and checks ---------- */
function lint(){
 const R=[],row=(label,count,slugs,extra)=>R.push({label,count,slugs:uniq(slugs),extra:extra||''});
 const idx=uniq([...indexMd.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())),tens=parseTens();
 let a=[];pages.forEach(p=>p._links.forEach(s=>{if(!P_MAP.has(s))a.push(p.slug);}));row('Dangling [[links]]',a.length,a);
 a=pages.filter(p=>![...(backl.get(p.slug)||[])].some(s=>s!==p.slug)).map(p=>p.slug);row('Orphan pages (no page links to them)',a.length,a);
 a=[];pages.forEach(p=>p._pins.forEach(x=>{if(!x.v.ok)a.push(p.slug);}));row('Pins the code could not verify',a.length,a);
 a=[];pages.forEach(p=>p._pins.forEach(x=>{if(!x.v.ok&&x.mark==='✓')a.push(p.slug);}));row('Pins marked ✓ that fail',a.length,a);
 a=pages.filter(p=>{const s=new Set(p.frontmatter.sources),q=new Set(p._pins.map(x=>x.id));return s.size!==q.size||[...s].some(x=>!q.has(x));}).map(p=>p.slug);row('`sources` differ from the documents pinned',a.length,a);
 a=pages.filter(p=>!p._pins.length).map(p=>p.slug);row('Pages with no pins',a.length,a);
 a=[];pages.forEach(p=>uniq([...p.frontmatter.links,...p._links]).forEach(s=>{const o=P_MAP.get(s);if(o&&o!==p&&!uniq([...o.frontmatter.links,...o._links]).includes(p.slug))a.push(p.slug);}));row('Links not reciprocated',a.length,a);
 a=pages.filter(p=>!idx.includes(p.slug)).map(p=>p.slug);row('Pages missing from the index',a.length,a);
 const nopage=idx.filter(s=>!P_MAP.has(s));row('Index lines without a page',nopage.length,[],nopage.join(', '));
 a=[];indexMd.split('\n').forEach(l=>{const m=l.match(/\[\[([^\]|#]+)\]\]/),n=l.match(/✓\s*(\d+)/);if(m&&n&&P_MAP.has(m[1].trim())&&P_MAP.get(m[1].trim())._pins.filter(x=>x.v.ok).length!==+n[1])a.push(m[1].trim());});row('Index ✓N differs from the computed count',a.length,a);
 const cards=new Set(tens.map(t=>t.card).filter(Boolean)),withC=pages.filter(hasCards).map(p=>p.slug);
 a=withC.filter(s=>!cards.has(s));row('Contested cards without a tensions entry',a.length,a);
 const rev=[...cards].filter(s=>!withC.includes(s));row('Tensions entries without a contested card',rev.length,rev.filter(s=>P_MAP.has(s)),rev.filter(s=>!P_MAP.has(s)).join(', '));
 a=pages.filter(p=>p.frontmatter.status==='stub').map(p=>p.slug);row('Stub pages',a.length,a);
 a=[];pages.forEach(p=>p._pins.forEach(x=>{const d=docMap.get(x.id);if(d&&d.status==='inbox')a.push(p.slug);}));row('Pins to a document still in the inbox',a.length,a);
 return R;
}
const slugLinks=(sl,max)=>{max=max||12;const s=sl.slice(0,max).map(x=>P_MAP.has(x)?'<a href="#'+esc(x)+'">'+esc(x)+'</a>':esc(x)).join(', ');return s+(sl.length>max?' +'+(sl.length-max)+' more':'');};
function selfChecks(){
 const L=lint(),g=l=>L.find(r=>r.label.startsWith(l)),C=[],add=(name,text,ok,slugs)=>C.push({name,text,ok,slugs:slugs||[]});
 const all=pages.flatMap(p=>p._pins.map(x=>({p,x}))),m0=(indexMd.match(/(\d[\d,]*) pins/)||[])[1],st=m0?+m0.replace(/,/g,''):null;
 const okN=all.filter(a=>a.x.v.ok).length,fc=all.filter(a=>!a.x.v.ok&&a.x.mark==='✓');
 add('Pins','found '+all.length+'; the index states '+(st==null?'no number':st)+'; verified '+okN+'; marked ✓ but failing '+fc.length,st===all.length&&!fc.length,fc.map(a=>a.p.slug));
 const lb=all.filter(a=>/^label/.test(a.x.v.reason||''));add('Labels','pins whose quote is found but whose label names the wrong paragraph or page: '+lb.length,!lb.length,lb.map(a=>a.p.slug));
 add('Structure','dangling links '+g('Dangling').count+'; orphans '+g('Orphan').count+'; `sources` differing from pinned documents '+g('`sources`').count+'; pages missing from the index '+g('Pages missing').count+'; index lines without a page '+g('Index lines').count+'; contested cards without a tensions entry '+g('Contested cards').count+', the reverse '+g('Tensions entries').count,[g('Dangling'),g('Orphan'),g('`sources`'),g('Pages missing'),g('Index lines'),g('Contested cards'),g('Tensions entries')].every(r=>!r.count),uniq(L.filter(r=>/Dangling|Orphan|sources|missing|Contested|Tensions/.test(r.label)).flatMap(r=>r.slugs)));
 const parsed=callLog.filter(c=>c.parsed).length,unk=callLog.reduce((n,c)=>n+(c.unknown||0),0);
 if(!callLog.length)add('Model answers','no call to the model yet',null);
 else add('Model answers','calls '+callLog.length+'; JSON parsed '+parsed+'; slugs that do not exist, dropped '+unk+(ING?'; takeaways returned '+ING.returned+' = verified '+ING.tk.length+' + could not verify '+ING.failed.length:''),parsed===callLog.length&&(!ING||ING.returned===ING.tk.length+ING.failed.length));
 if(!ING)add('Coverage','no ingest yet',null);
 else{const tot=ING.doc.passages.length;add('Coverage','passages sent '+ING.sent+' of '+tot+'; takeaways naming a passage that was not sent, dropped '+ING.dropped,ING.sent===tot);}
 const warn=all.filter(a=>a.x.mark==='⚠').length,chg=new Set(changes.map(c=>c.slug)),bad=all.filter(a=>chg.has(a.p.slug)&&!a.x.v.ok);
 add('Unverified','⚠ pins in the wiki: '+warn+' (at load: '+warn0+'); pins failing in changed pages: '+bad.length+(ING?'; could not verify '+ING.failed.length+' + verified '+ING.tk.length+' = returned '+ING.returned:''),warn===warn0&&!bad.length&&(!ING||ING.returned===ING.tk.length+ING.failed.length),bad.map(a=>a.p.slug));
 const diff=pages.filter(p=>orig.has(p.slug)&&orig.get(p.slug)!==p.body).map(p=>p.slug),und=diff.filter(s=>!chg.has(s));
 add('Approval','pages whose body differs from the loaded one: '+diff.length+'; of these without an approved card or filing: '+und.length,!und.length,und);
 if(ING&&ING.filed)add('Filing','pages re-parsed and re-verified: '+ING.filed.slugs.length+'; lint checks needing a look before '+ING.filed.before+', after '+ING.filed.after+'; last log entry: '+(parseLog().slice(-1)[0]||{head:'-'}).head,ING.filed.slugs.every(s=>P_MAP.has(s)&&P_MAP.get(s)._pins.every(x=>x.v.ok))&&!g('Index ✓N').count,ING.filed.slugs);
 else add('Filing','nothing filed from an ingest yet',null);
 const ops=uniq(changes.map(c=>c.op)).length;add('Session','changes listed '+changes.length+' in '+ops+' operation'+(ops===1?'':'s')+'; log entries added this session '+sessionHeads.length+'; the download holds '+exportObj().pages.length+' pages, the wiki has '+pages.length,ops===sessionHeads.length&&exportObj().pages.length===pages.length);
 return C;
}
function renderCheck(){
 const L=lint(),bad=L.filter(r=>r.count>0).length,ap=allPins(),ok=ap.filter(x=>x.v.ok).length;
 let h='<p class="big">'+fmtN(ok)+' <small>of '+fmtN(ap.length)+' pins verified by this page</small></p><p class="mono">'+bad+' lint check'+(bad===1?'':'s')+' need a look</p><p class="mn">How this is computed: each pin\'s quote is searched, after normalising quotes, dashes and spaces, in the passages of its document that start on its PDF page, and its label must name that passage.</p>';
 h+='<p><button class="btn pri" data-act="lint" id="lintBtn">'+(renderCheck.ran?'Re-run':'Lint now')+'</button> <span class="mn">Contradictions between pages are not checked by code: the schema\'s reading for contradictions is a person\'s job.</span></p>';
 h+='<table><caption><span class="mono" style="color:var(--red)">FIG.03</span> Lint: '+L.length+' checks</caption><thead><tr><th scope="col">Check</th><th scope="col" class="num">Count</th><th scope="col">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>'+L.map(r=>'<tr><td>'+esc(r.label)+'</td><td class="num">'+r.count+'</td><td class="'+(r.count?'check':'pass')+'">'+(r.count?r.count+' · check':'0 · pass')+'</td><td>'+slugLinks(r.slugs)+(r.extra?(r.slugs.length?'; ':'')+'no page: '+esc(r.extra):'')+'</td></tr>').join('')+'</tbody></table>';
 h+='<details open><summary>How the app checks itself</summary><ul>'+selfChecks().map(c=>'<li><strong>'+esc(c.name)+'.</strong> '+esc(c.text)+' · <span class="'+(c.ok==null?'na':c.ok?'pass':'check')+'">'+(c.ok==null?'not applicable yet':c.ok?'pass':'check')+'</span>'+(c.slugs.length?' · '+slugLinks(c.slugs):'')+'</li>').join('')+'</ul></details>';
 $('#chkOut').innerHTML=h;
}

/* ---------- tab 05 record ---------- */
function exportObj(){return{title:wiki.title,source:wiki.source,built:wiki.built,count:pages.length,schema:wiki.schema,pages:pages.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.frontmatter,body:p.body})),index:indexMd,log:logMd,tensions:tensMd,changes,library_status:Object.fromEntries(docs.map(d=>[d.id,d.status]))};}
function renderRecord(){
 const ent=parseLog(),list=$('#newest').checked?ent.slice().reverse():ent,tens=parseTens();
 let h='<h3 class="fig"><span class="mono">LOG</span> Operations, '+ent.length+' entries</h3>'+list.map(e=>'<details><summary>'+esc(e.head)+(sessionHeads.includes(e.head)?' <span class="chip">this session</span>':'')+'</summary><div class="md">'+renderMd(e.body,{})+'</div></details>').join('');
 h+='<h3 class="fig"><span class="mono">TENSIONS</span> Open disagreements, '+tens.length+' entries</h3>'+tens.map(e=>'<details id="tens-'+e.i+'"><summary>'+esc(e.head)+(sessionTens.includes(e.head)?' <span class="chip">this session</span>':'')+'</summary><div class="md">'+renderMd(e.body,{})+'</div>'+(e.card?'<p class="mn">card: '+(P_MAP.has(e.card)?'<a href="#'+esc(e.card)+'">'+esc(P_MAP.get(e.card).title)+'</a>':esc(e.card)+' (no page)')+'</p>':'')+'</details>').join('');
 h+='<h3>Method and source</h3><p class="mn">Counting, matching and verification are done by this page\'s code; each number has its "How this is computed" line. Data: '+esc(wiki.source||'research wiki')+', built '+esc(wiki.built||'unknown')+'.</p>';
 h+='<p><button class="btn pri" data-act="dljson">Download the wiki</button>'+(changes.length?'<button class="btn" data-act="dlmd">Download the changed pages (markdown)</button>':'')+'</p>';
 $('#recOut').innerHTML=h;
}

/* ---------- tab 03 ingest ---------- */
const chunk=(a,n)=>{const o=[];for(let i=0;i<a.length;i+=n)o.push(a.slice(i,i+n));return o;};
const paraLab=x=>x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
function newING(doc){
 const stub=pages.find(p=>p.frontmatter.status==='stub'&&(p.slug===slugify(doc.id)||p.slug===slugify(doc.symbol||'')))||pages.find(p=>p.frontmatter.status==='stub');
 return{doc,step:1,batches:chunk(doc.passages||[],25).map((ps,i)=>({i,passages:ps})),tk:[],failed:[],rows:[],dropped:0,returned:0,calls:0,sent:0,newSlugs:[],stub:stub?stub.slug:null,src:null,touched:[],drafts:{},changes:[],msg:'',err:null,filed:null,done1:false,run:null};
}
function nearest(q,page){
 const a=norm(q).split(' ');let best={run:0,passage:null};
 for(const x of ING.doc.passages.filter(x=>x.page===page)){
  const b=norm(x.text).split(' ');let run=0,prev=new Array(b.length+1).fill(0);
  for(let i=1;i<=a.length;i++){const c=new Array(b.length+1).fill(0);for(let j=1;j<=b.length;j++)if(a[i-1]===b[j-1]){c[j]=prev[j-1]+1;if(c[j]>run)run=c[j];}prev=c;}
  if(run>best.run)best={run,passage:x};
 }
 return best;
}
const vIng=p=>verify(p,{inbox:ING.doc.id});
const tkPrompt=(items,b,n)=>PRE+'DOCUMENT: '+ING.doc.title+' ('+citeAs(ING.doc)+', '+ING.doc.kind+', '+ING.doc.year+'). This is batch '+(b+1)+' of '+n+'. Return JSON {"takeaways": [{"claim": ..., "quote": ..., "passage": the passage id, "pages": [slug, ...]}]}, at most 10. Each quote is 8 to 40 words copied verbatim from that one passage. pages are slugs from the index that the claim bears on; propose a new lowercase-hyphenated slug only when no page fits (at most two in the whole ingest). Skip passages with nothing to take away.\n\nINDEX:\n'+indexMd+'\n\nPASSAGES (JSON):\n'+JSON.stringify(items);
async function ingStart(from){
 const run=startRun('ingest');ING.run=run;ING.step=2;ING.err=null;const n=ING.batches.length,tot=ING.doc.passages.length;
 for(let b=from||0;b<n;b++){
  if(run.stopped)break;const bt=ING.batches[b],items=bt.passages.map(x=>({id:x.id,page:x.page,paragraph:x.paragraph,text:x.text}));
  ING.msg='batch '+(b+1)+' of '+n+' · '+ING.sent+' of '+tot+' passages have left the browser; sending '+items.length+' more';renderIngest();
  ING.calls++;ING.sent+=items.length;
  const r=await callModel(tkPrompt(items,b,n),{label:'Ingest: batch '+(b+1),passages:items.length,run});
  if(r.stopped)break;
  if(!r.ok){ING.err={error:r.error,raw:r.raw,batch:b};ING.msg='';endRun('ingest');renderIngest();return;}
  const arr=Array.isArray(r.data.takeaways)?r.data.takeaways.slice(0,10):[];ING.returned+=arr.length;
  for(const t of arr){
   const pas=bt.passages.find(x=>x.id===String(t&&t.passage).trim());
   if(!pas){ING.dropped++;continue;}
   const quote=String(t.quote||'').trim(),pin=mkPin(ING.doc,pas,quote),v=vIng(pin);
   const pg=uniq((Array.isArray(t.pages)?t.pages:[]).map(String).filter(s=>/^[a-z0-9-]+$/.test(s))).filter(s=>{if(P_MAP.has(s)||ING.newSlugs.includes(s))return true;if(ING.newSlugs.length<2){ING.newSlugs.push(s);return true;}return false;});
   const row={claim:String(t.claim||'').trim(),quote,pas,pin,pages:pg,ok:v.ok,reason:v.reason};ING.rows.push(row);
   if(v.ok)ING.tk.push(row);else ING.failed.push(Object.assign({near:nearest(quote,pas.page)},row));
  }
  updHeader();renderIngest();
 }
 const stopped=run.stopped;endRun('ingest');ING.done1=true;
 ING.msg=(stopped?'Stopped; what has returned is kept. ':'')+ING.returned+' takeaways returned: '+ING.tk.length+' verified, '+ING.failed.length+' could not be verified'+(ING.dropped?', '+ING.dropped+' named a passage that was not sent (dropped)':'')+'.';
 renderIngest();
}
const srcPrompt=()=>PRE+'Write the source page for the document below. DOCUMENT: '+ING.doc.title+'; author '+(ING.doc.author||'unknown')+'; published '+ING.doc.published+'; '+ING.doc.pages+' pages; '+ING.doc.url+'. Cite as: '+citeAs(ING.doc)+'. Sections, in this order: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related. Return JSON {"one_liner": ..., "body": markdown of at most 900 words, "touches": [{"slug": ..., "why": ...}]}. Use only the pins given below, copied exactly, one per claim.\n\nVERIFIED TAKEAWAYS (JSON):\n'+JSON.stringify(ING.tk.map(t=>({claim:t.claim,pin:t.pin.raw,passage:paraLab(t.pas)+', PDF page '+t.pas.page,pages:t.pages})))+'\n\nREGISTER of this document: ('+regOf(ING.doc.id)+')\nINDEX (existing slugs):\n'+indexMd;
function srcSlug(){const b=slugify(ING.doc.symbol||ING.doc.id);return!P_MAP.has(b)?b:!P_MAP.has(b+'-source')?b+'-source':b+'-'+Date.now().toString(36);}
async function ingDraftSource(){
 const run=startRun('ingest');ING.run=run;ING.err=null;ING.msg='Drafting the source page (1 call)…';ING.calls++;renderIngest();
 const r=await callModel(srcPrompt(),{label:'Ingest: source page',run});endRun('ingest');
 if(r.stopped){ING.msg='Stopped.';renderIngest();return;}
 const body=r.ok?String(r.data.body||'').trim():'';
 if(!r.ok||!body){ING.err={error:r.ok?'The draft had no body.':r.error,raw:r.raw,retry:'src'};ING.msg='';renderIngest();return;}
 ING.src={slug:srcSlug(),oneLiner:String(r.data.one_liner||'').trim(),body,touches:Array.isArray(r.data.touches)?r.data.touches:[]};
 const ok=s=>typeof s==='string'&&s!==ING.src.slug&&(P_MAP.has(s)||ING.newSlugs.includes(s)),out=new Map();
 ING.src.touches.forEach(t=>{const s=String((t&&t.slug)||t);if(ok(s)&&!out.has(s))out.set(s,String((t&&t.why)||''));});
 ING.tk.forEach(t=>t.pages.forEach(s=>{if(ok(s)&&!out.has(s))out.set(s,'takeaway');}));
 let list=[...out.entries()].filter(([s])=>s!==ING.stub).map(([slug,why])=>({slug,why}));
 if(ING.stub)list.unshift({slug:ING.stub,why:'stub: rewrite it with its checklist'});
 ING.touched=list.slice(0,12).map(t=>({slug:t.slug,why:t.why,isNew:!P_MAP.has(t.slug),isStub:t.slug===ING.stub}));
 ING.msg='Source page drafted. '+ING.touched.length+' pages would be touched.';renderIngest();
}
function pagePrompt(t){
 const rel=ING.tk.filter(x=>x.pages.includes(t.slug)),use=(t.isStub?ING.tk:(rel.length?rel:ING.tk.slice(0,5))).map(x=>({claim:x.claim,pin:x.pin.raw,passage:paraLab(x.pas)}));
 const head=PRE+'DOCUMENT: '+citeAs(ING.doc)+' ('+ING.doc.title+'). Why this page is touched: '+t.why+'.\n\nTAKEAWAYS WITH READY-MADE PINS (JSON):\n'+JSON.stringify(use)+'\n\n';
 if(t.isStub)return head+'The page below is a stub for this document. Rewrite it as a real entity page, working through the checklist in its body. Return JSON {"body": the complete new markdown body starting with "# title", at most 500 words}. Keep its existing pins if you keep their claims; add only the pins given above, copied exactly.\n\nPAGE '+t.slug+':\n'+P_MAP.get(t.slug).body;
 if(t.isNew)return head+'The page "'+t.slug+'" does not exist yet. Write it as a short concept page. Return JSON {"edits": [{"after": "end", "markdown": the complete page starting with "# title"}], "contested": null}, at most 300 words, only the pins given above, copied exactly.';
 return head+'Return JSON {"edits": [{"after": an existing heading of the page or "end", "markdown": ...}], "contested": null or a full contested block (claim:, verdict:, note:, then one line per position: sign, register letter, pin, gloss, [[slug]], separated by " | ") only where this document disagrees with the page}. At most 300 words in all; pins copied exactly from above.\n\nPAGE '+t.slug+':\n'+P_MAP.get(t.slug).body;
}
async function ingDraftPages(){
 const run=startRun('ingest');ING.run=run;ING.err=null;
 for(let i=0;i<ING.touched.length;i++){
  const t=ING.touched[i];if(ING.drafts[t.slug])continue;if(run.stopped)break;
  ING.msg='page '+(i+1)+' of '+ING.touched.length+': '+t.slug;ING.calls++;renderIngest();
  const r=await callModel(pagePrompt(t),{label:'Ingest: '+t.slug,run});
  if(r.stopped)break;
  if(!r.ok){ING.err={error:r.error,raw:r.raw,retry:'pages'};ING.msg='';endRun('ingest');renderIngest();return;}
  const d=r.data,old=P_MAP.get(t.slug),notes=[];let body,kind=t.isNew?'new':'edited',title=old?old.title:t.slug,type=old?old.type:'concept';
  if(t.isStub){body=String(d.body||'').trim();if(body)body=INS+'\n'+body+'\n'+INE;}
  else{
   const ed=Array.isArray(d.edits)?d.edits:[];body=old?old.body:'';let n=0;
   for(const e of ed){const md=String((e&&e.markdown)||'').trim();if(!md)continue;if(t.isNew){body=INS+'\n'+md+'\n'+INE;n++;continue;}const x=insertAt(body,e.after,md);body=x.body;if(x.note)notes.push(x.note);n++;}
   if(typeof d.contested==='string'&&/claim:/.test(d.contested)){let blk=d.contested.trim();if(!/^\x60\x60\x60/.test(blk))blk=FENCE+'contested\n'+blk+'\n'+FENCE;if(t.isNew)body=body.replace(INE,'\n'+blk+'\n'+INE);else{body=insertAt(body,'end',blk).body;}n++;}
   if(!n)body='';
  }
  if(!body){ING.drafts[t.slug]={none:true};continue;}
  if(t.isNew){const h=insPart(body).match(/^#\s+(.*)$/m);title=h?h[1].trim():t.slug;}
  ING.drafts[t.slug]={slug:t.slug,kind,title,type,body,notes,isStub:t.isStub,decision:null};
 }
 const stopped=run.stopped;endRun('ingest');ING.msg=stopped?'Stopped; the drafts that returned are kept.':'All page drafts returned.';renderIngest();
}
function mkChanges(){
 const out=[],s=ING.src,doc=ING.doc,reg=(ING.stub&&P_MAP.get(ING.stub).frontmatter.register)||[];
 const sb=/^#\s/.test(s.body)?s.body:'# '+citeAs(doc)+' — '+(doc.short_title||doc.title)+'\n\n'+s.body;
 out.push({slug:s.slug,kind:'new',title:(sb.match(/^#\s+(.*)$/m)||[0,s.slug])[1],type:'source',body:INS+'\n'+sb+'\n'+INE,notes:[],decision:null,fm:{type:'source',tags:uniq(['source',...ING.touched.map(t=>t.slug)]),register:reg.slice(),status:'draft',links:[],sources:[doc.id]}});
 ING.touched.forEach(t=>{const d=ING.drafts[t.slug];if(d&&!d.none)out.push(d);});
 return out;
}
function cardStats(c){
 const ip=insPart(c.body),pins=parsePins(ip),ok=pins.filter(p=>vIng(p).ok).length;
 return{paras:ip.split(/\n\s*\n/).filter(x=>x.trim()).length,ok,bad:pins.length-ok};
}
function ingFile(){
 const date=today(),doc=ING.doc,bc=lint().filter(r=>r.count>0).length,ap=ING.changes.filter(c=>c.decision==='approved'),rj=ING.changes.filter(c=>c.decision==='rejected');
 const apSet=new Set(ap.map(c=>c.slug)),srcOk=apSet.has(ING.src.slug),head='['+date+'] ingest | '+(doc.symbol||doc.short_title)+': '+doc.short_title;
 const dreg=regOf(doc.id).split('').filter(x=>'abcdef'.includes(x)),newTens=[];
 for(const c of ap){
  const body=stripIns(c.body).trim()+'\n',ids=uniq(parsePins(body).map(p=>p.id)),p=P_MAP.get(c.slug),old=p?p.frontmatter:c.fm;
  const fm=Object.assign({},old,{title:c.title,type:c.type,updated:date,register:uniq([...(old.register||[]),...(c.slug===ING.src.slug?[]:dreg)]),sources:uniq([...(old.sources||[]).filter(s=>ids.includes(s)),...ids])});
  if(c.isStub||c.kind==='new')fm.status='draft';
  const bl=uniq([...body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim()));
  let links=uniq([...(old.links||[]),...bl.filter(s=>P_MAP.has(s)||apSet.has(s))]);
  if(c.slug===ING.src.slug)links=uniq([...bl.filter(s=>P_MAP.has(s)||apSet.has(s)),...ap.filter(x=>x.slug!==c.slug).map(x=>x.slug)]);else if(srcOk)links=uniq([...links,ING.src.slug]);
  fm.links=links.filter(s=>s!==c.slug);
  const oldBody=p?p.body:'';
  for(const m of body.matchAll(new RegExp(FENCE+'contested\\n([\\s\\S]*?)'+FENCE,'g'))){const k=parseContested(m[1]);if(!k.claim||oldBody.includes(k.claim))continue;
   const sm={contested:'open'},stt=/^leans/.test(k.verdict)?'leaning':/^settled/.test(k.verdict)?'settled':(sm[k.verdict]||'open');
   const ps=s=>k.pos.filter(x=>x.sign===s).map(x=>'('+x.reg+') '+((x.pin.match(/\[([^\]]+)\]/)||[0,''])[1])).join('; ')||'none';
   newTens.push('### '+(slugify(k.claim).slice(0,60)||'claim')+'\n- title: '+k.claim+'\n- status: '+stt+'\n- card: [['+c.slug+']]\n- poles: supports '+ps('+')+' · contests '+ps('-')+'\n- where: '+uniq(k.pos.map(x=>(x.pin.match(/\[([^\]]+)\]/)||[0,''])[1])).join('; '));}
  if(p){p.body=body;p.frontmatter=fm;}else pages.push({slug:c.slug,type:c.type,title:c.title,frontmatter:fm,body});
 }
 doc.status='ingested';reindex();
 for(const c of ap){
  const p=P_MAP.get(c.slug),n=p._pins.filter(x=>x.v.ok).length;
  if(c.kind==='new'||c.isStub){idxUpsert(c.slug,p.type,'- [[' + c.slug + ']] — ' + (c.slug===ING.src.slug&&ING.src.oneLiner?plainFirst(ING.src.oneLiner):plainFirst(p.body)) + ' · (' + p.frontmatter.register.join('') + ') · ✓' + n);}
  else{const L=indexMd.split('\n'),k=L.findIndex(l=>/^\s*[-*]\s/.test(l)&&l.includes('[['+c.slug+']]'));if(k>=0){L[k]=L[k].replace(/✓\s*\d+/,'✓'+n);indexMd=L.join('\n');}else idxUpsert(c.slug,p.type,'- [[' + c.slug + ']] — ' + plainFirst(p.body) + ' · (' + p.frontmatter.register.join('') + ') · ✓' + n);}
 }
 idxCounts();
 const pinned=pages.filter(p=>p.slug!==ING.src.slug&&p._pins.some(x=>x.id===doc.id)).map(p=>p.slug),tp=pages.reduce((n,p)=>n+p._pins.filter(x=>x.id===doc.id).length,0);
 appendLog(head,'Read '+ING.sent+' passages ('+citeAs(doc)+', register ('+regOf(doc.id)+')). Wrote [['+ING.src.slug+']]'+(srcOk?'':' (rejected)')+'. '+tp+' pins in all; besides its own page, pinned on '+pinned.length+' pages: '+(pinned.map(s=>'[['+s+']]').join(', ')||'none')+'. Rejected: '+(rj.map(c=>'[['+c.slug+']]').join(', ')||'none')+'.');
 if(newTens.length){tensMd=tensMd.replace(/\s*$/,'')+'\n\n'+newTens.join('\n\n')+'\n';newTens.forEach(t=>sessionTens.push(t.split('\n')[0].slice(4).trim()));}
 ap.forEach(c=>changes.push({date,kind:'ingest',slug:c.slug,change:c.kind,op:head}));
 ING.filed={date,slugs:ap.map(c=>c.slug),approved:ap.length,rejected:rj.length,before:bc,after:lint().filter(r=>r.count>0).length};
 refreshAll();say('Filed '+ap.length+' approved page'+(ap.length===1?'':'s')+'.');
}
const stepsHTML=()=>'<ol class="steps">'+['Scope','Takeaways','Drafts','Review and file'].map((n,i)=>'<li class="'+(ING.step===i+1?'on':'')+'"'+(ING.step===i+1?' aria-current="step"':'')+'>0'+(i+1)+' '+n+'</li>').join('')+'</ol>';
const runLine=()=>'<p class="runline" aria-live="polite">calls so far <b>'+ING.calls+'</b> · passages sent <b>'+ING.sent+'</b></p>'+(ING.msg?'<p class="mn" aria-live="polite">'+esc(ING.msg)+'</p>':'');
const stopBtn=()=>RUN.ingest?'<button class="btn" data-act="stop">Stop</button>':'';
function renderIngest(){
 const out=$('#ingOut'),inbox=docs.filter(d=>d.status==='inbox'),btns=inbox.map(d=>'<button class="btn pri" data-act="ingstart" data-arg="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+'</button>').join(' ');
 const intro='<p class="mn">Ingesting sends the document\'s passages to a language model in batches. Every change waits for your approval; nothing is written before.</p>';
 if(ING&&ING.filed){const f=ING.filed;out.innerHTML='<h2>Filed</h2><p class="big">'+f.approved+' <small>page'+(f.approved===1?'':'s')+' written, '+f.rejected+' rejected</small></p><p class="mn" aria-live="polite">Lint checks needing a look: '+f.before+' before, '+f.after+' after. The log, the index and the tensions register were updated; the pages are in memory until you download them on tab 05.</p>'+(inbox.length?intro+btns:'<p class="lead">Nothing waits in the inbox.</p>');return;}
 if(!ING){out.innerHTML=inbox.length?intro+'<p>'+btns+'</p>':'<p class="lead">Nothing waits in the inbox.</p>';return;}
 let h='<h2>Ingest '+esc(ING.doc.symbol||ING.doc.short_title)+'</h2>'+stepsHTML()+runLine();
 if(ING.err)h+=errHTML(ING.err,ING.err.batch!=null?'ingretry':ING.err.retry==='src'?'ingsrc':'ingpages');
 const tot=ING.doc.passages.length,n=ING.batches.length;
 if(ING.step===1){
  const chars=ING.doc.passages.reduce((a,x)=>a+x.text.length,0);
  h+='<p><strong>Scope: the whole document.</strong></p><p>All '+tot+' passages will be sent, in batches of 25 ('+n+' call'+(n===1?'':'s')+'), '+fmtN(chars)+' characters; nothing is held back. They leave the browser.</p>';
  h+='<table><caption>Batches</caption><thead><tr><th scope="col">Batch</th><th scope="col" class="num">Passages</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th></tr></thead><tbody>'+ING.batches.map(b=>{const pr=b.passages.map(x=>x.paragraph).filter(Boolean),pg=b.passages.map(x=>x.page);return'<tr><td>'+(b.i+1)+'</td><td class="num">'+b.passages.length+'</td><td>'+(pr.length?esc(pr[0]===pr[pr.length-1]?pr[0]:pr[0]+' to '+pr[pr.length-1]):'no paragraph numbers')+'</td><td>'+Math.min(...pg)+'–'+Math.max(...pg)+'</td></tr>';}).join('')+'</tbody></table><p><button class="btn pri" data-act="ingbegin">Start</button></p>';
 }else if(ING.step===2){
  h+=stopBtn();
  h+='<table><caption><span class="mono" style="color:var(--red)">FIG.02</span> Takeaways so far: '+ING.rows.length+' returned</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it would touch</th><th scope="col">Check</th></tr></thead><tbody>'+(ING.rows.map(r=>'<tr><td data-source="ai">'+esc(r.claim)+'</td><td data-source="ai">“'+esc(r.quote)+'”</td><td>'+esc(paraLab(r.pas))+' · PDF p. '+r.pas.page+'</td><td data-source="ai">'+(r.pages.map(s=>'<span class="chip">'+esc(s)+'</span>').join('')||'<span class="mn">none</span>')+'</td><td class="'+(r.ok?'pass':'check')+'">'+(r.ok?'verified':'could not verify')+'</td></tr>').join('')||'<tr><td colspan="5" class="mn">Nothing has returned yet.</td></tr>')+'</tbody></table>';
  h+='<details class="fail" open><summary>Could not verify: '+ING.failed.length+'</summary><p class="mn">These claims are in no change card and in no later prompt.</p>'+ING.failed.map(f=>'<div><p data-source="ai">“'+esc(f.quote)+'” (claim: '+esc(f.claim)+')</p><p class="mn">named passage '+esc(f.pas.id)+' ('+esc(paraLab(f.pas))+', PDF p. '+f.pas.page+'); reason: '+esc(f.reason)+'. Nearest passage on that page: '+(f.near.passage?esc(paraLab(f.near.passage))+', longest shared run '+f.near.run+' words':'none')+'.</p><button class="btn sm openpdf" data-id="'+esc(ING.doc.id)+'" data-page="'+f.pas.page+'" aria-label="Open '+esc(ING.doc.symbol||ING.doc.short_title)+' at PDF page '+f.pas.page+'">Open the PDF page</button></div>').join('')+'</details>';
  if(ING.done1&&!RUN.ingest)h+=ING.tk.length?'<p><button class="btn pri" data-act="ingto3">Continue to the drafts</button></p>':'<p class="check">No takeaway verified, so there is nothing to draft.</p>';
 }else if(ING.step===3){
  h+=stopBtn();
  if(!ING.src)h+='<p>'+ING.tk.length+' verified takeaways will be sent to draft the source page.</p><p><button class="btn pri" data-act="ingsrc"'+(RUN.ingest?' disabled':'')+'>Draft the source page (1 call)</button></p>';
  else{
   const sc=ING.touched.length,left=ING.touched.filter(t=>!ING.drafts[t.slug]).length;
   h+='<details><summary>Source page draft (one-liner: '+esc(ING.src.oneLiner||'none')+')</summary><div class="md" data-source="ai">'+renderMd(ING.src.body,{pinCheck:vIng})+'</div></details>';
   h+='<p>Pages that would be touched: '+ING.touched.map(t=>'<span class="chip">'+esc(t.slug)+(t.isNew?' (new)':t.isStub?' (stub)':'')+'</span>').join('')+'</p>';
   h+=left?'<p><button class="btn pri" data-act="ingpages"'+(RUN.ingest?' disabled':'')+'>Draft the changes to '+sc+' pages ('+left+' call'+(left===1?'':'s')+')</button></p>':'<p><button class="btn pri" data-act="ingto4">Review the changes</button></p>';
  }
 }else{
  const cs=ING.changes,k=cs.findIndex(c=>!c.decision);
  if(k>=0){
   const c=cs[k],st=cardStats(c);
   h+='<fieldset><legend>Change '+(k+1)+' of '+cs.length+' · '+esc(c.title)+' ('+esc(c.type)+') · '+(c.kind==='new'?'new page':'edited')+'</legend><p class="mn">inserted paragraphs: '+st.paras+' · pins added: '+st.ok+' verified, '+st.bad+' not verified'+(c.notes&&c.notes.length?' · note: '+esc(c.notes.join('; ')):'')+'</p><div class="md" data-source="ai">'+renderMd(c.body,{mark:true,slug:c.slug,pinCheck:vIng})+'</div><p><button class="btn pri" data-act="approve"'+(st.bad?' disabled':'')+' aria-label="Approve change '+(k+1)+' of '+cs.length+': '+esc(c.slug)+'">Approve this page</button><button class="btn" data-act="reject" aria-label="Reject change '+(k+1)+' of '+cs.length+': '+esc(c.slug)+'">Reject this page</button>'+(st.bad?' <span class="mn">Approve is disabled: '+st.bad+' inserted pin'+(st.bad===1?'':'s')+' do not verify. Reject this page.</span>':'')+'</p></fieldset>';
  }else h+='<p class="runline">All '+cs.length+' changes decided: approved <b>'+cs.filter(c=>c.decision==='approved').length+'</b> · rejected <b>'+cs.filter(c=>c.decision==='rejected').length+'</b></p><p class="mn">Nothing in the wiki has changed yet.</p><p><button class="btn pri" data-act="ingfile">File the approved changes</button></p>';
  h+='<p class="mn">Decided so far: '+cs.map(c=>esc(c.slug)+' '+(c.decision||'waiting')).join(' · ')+'</p>';
 }
 out.innerHTML=h;
}

/* ---------- actions and events ---------- */
function refreshAll(){reindex();updHeader();renderList();renderView();renderAskTop();renderAskOut();renderIngest();renderCheck();renderRecord();}
const ACT={
 askgo(){ask.stage==='pick'?askStep2():askStep1();},
 askretry(){ask.err&&ask.err.retry===2?askStep2():askStep1();},
 stop(){['ask','ingest'].forEach(k=>{if(RUN[k])RUN[k].halt();});say('Stopped. What has returned is kept.');},
 pickopen(){ask.pickOpen=!ask.pickOpen;renderAskOut();},
 filecard(){ask.filing=!ask.filing;renderAskOut();updFile();},
 filedo:fileQuestion,
 async copyans(){say(await copyText(ask.answer.answer)?'Answer copied.':'Copy failed.');},
 async copymd(s){const p=P_MAP.get(s);if(p)say(await copyText(pageMd(p))?'Page copied as markdown.':'Copy failed.');},
 gotens(i){selectTab(4);const d=$('#tens-'+i);if(d){d.open=true;d.scrollIntoView();$('summary',d).focus();}},
 lint(){renderCheck.ran=true;renderCheck();},
 dljson(){download('wiki-'+today()+'.json',JSON.stringify(exportObj(),null,1),'application/json');},
 dlmd(){const sl=uniq(changes.map(c=>c.slug)).filter(s=>P_MAP.has(s));download('wiki-changed-pages-'+today()+'.md',sl.map(s=>pageMd(P_MAP.get(s))).join('\n\n---\n\n'),'text/markdown');},
 ingstart(id){ING=newING(docMap.get(id));renderIngest();},
 ingbegin(){ingStart(0);},
 ingretry(){ingStart(ING.err.batch);},
 ingto3(){ING.step=3;ING.msg='';renderIngest();},
 ingsrc:ingDraftSource,
 ingpages:ingDraftPages,
 ingto4(){ING.changes=mkChanges();ING.step=4;ING.msg='';renderIngest();},
 approve(){const c=ING.changes.find(x=>!x.decision);if(c)c.decision='approved';renderIngest();},
 reject(){const c=ING.changes.find(x=>!x.decision);if(c)c.decision='rejected';renderIngest();},
 ingfile:ingFile
};
document.addEventListener('click',e=>{
 const t=e.target.closest('button');if(!t)return;
 if(t.classList.contains('pinlab')||t.classList.contains('openpdf')){openSrc(t.dataset.id,+t.dataset.page);return;}
 if(t.classList.contains('pinx')){const b=t.parentElement.querySelector('.pinbody'),o=b.hidden;b.hidden=!o;t.setAttribute('aria-expanded',o);t.textContent=o?'▴':'▾';return;}
 const a=t.dataset.act;if(a&&ACT[a])ACT[a](t.dataset.arg,t);
});
document.addEventListener('input',e=>{
 if(e.target.id==='flt')renderList();
 else if(e.target.id==='q')renderAskTop();
 else if(e.target.id==='fT'){ask.fTitle=e.target.value;updFile();}
 else if(e.target.id==='fG'){ask.fTags=e.target.value;updFile();}
});
document.addEventListener('change',e=>{
 if(e.target.id==='newest')renderRecord();
 else if(e.target.name==='pick'){
  const on=[...document.querySelectorAll('input[name=pick]:checked')].map(x=>x.value);
  if(on.length>5){e.target.checked=false;say('At most 5 pages.');return;}
  ask.chosen=pages.map(p=>p.slug).filter(s=>on.includes(s));renderAskTop();
 }
});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'&&(RUN.ask||RUN.ingest))ACT.stop();
 if(e.target.id==='q'&&e.key==='Enter'&&!e.shiftKey){e.preventDefault();if(!RUN.ask)askStep1();}
});
window.addEventListener('hashchange',route);

/* ---------- start ---------- */
reindex();warn0=allPins().filter(x=>x.mark==='⚠').length;
buildTabs();updHeader();renderAskTop();renderAskOut();renderIngest();renderCheck();renderRecord();route();
$('#t0').focus();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a tab "MAP" that draws the wiki as a graph: one node per page, coloured by its type (source, concept, entity, question), and one line for each [[link]] between two pages. Size each node by the number of pages that link to it. Draw it in plain SVG with a fixed layout computed by the code (no random start), so the map looks the same every time. Hovering a node shows its title and how many links go in and out; clicking it highlights its neighbours and offers "Open this page", which shows the page on the pages tab. Under the map, one line: how many pages and links, and the pages no other page links to (orphans), each clickable. Keep everything else as it is.

(Attached: Research wiki: neurotechnology and justice → WORKSHOP_DATA.wiki, with WORKSHOP_DATA.library)
