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
`studio.openSource(id, page, quote)` opens that document's PDF at that PDF page next to the app and marks `quote` on it: use it
for every passage shown (with its text as `quote`), so a reader can check it against the original. Cite a passage as
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
(groups: label, id, PDF page, quote, mark). Open a pin with `studio.openSource(id, page, quote)`. A pin is verified
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
- **Pin chips.** The label is a button; clicking it calls `studio.openSource(id, page, quote)` with the pin's quote, so the studio opens the PDF at that page beside the app with the quoted passage marked; "Open the PDF page" in the expanded chip does the same. Beside it, the verification the code computed: "✓ verified" in green or "⚠ not found" in amber, in words as well as colour; where that differs from the mark written in the page, the chip adds "page says ✓" or "page says ⚠". An arrow expands the chip in place: the quote, the matching passage's `paragraph` or `page_label` and its first 300 characters, "Open the PDF page". The document's register letter is on the chip.
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

No free-text editing of pages by hand. No PDF viewer inside the app (`studio.openSource` opens the page and marks the quote). No search beyond the page filter on tab 01. No version history beyond this session's change list. No lint of contradictions by the model. No ingest of a document that is not in the inbox, and no second ingest of the same document. No export other than JSON and markdown.

## Sources consulted

- Andrej Karpathy: "LLM Wiki", a pattern for LLM-maintained knowledge bases (summary) — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Own work: a schema for an LLM-maintained research wiki (page types, frontmatter, direct links, pin verification, registers, contested claims) — unpublished, on the workshop shelf
- Quality assurance of code for analysis and research: Generative AI and "vibe coding" (UK Government Analysis Function) — https://github.com/best-practice-and-impact/qa-of-code-guidance/blob/fa39f2089905fe07c08ae4d66671736a1becd3c5/book/generative_ai.md
- The A11Y Project checklist (content, keyboard, images, tables, colour contrast, forms) — https://github.com/a11yproject/a11yproject.com/blob/090a026713ea81676a03e9b0381a10850d7c955f/src/_data/checklists.json

(Attached: Research wiki: neurotechnology and justice → WORKSHOP_DATA.wiki, with WORKSHOP_DATA.library)

# ASSISTANT MESSAGE (your earlier answer)

I built the research wiki workspace in five tabs: Pages, Ask, Ingest, Check and Record. Every quotation is re-checked by the page's own code against the library passages. Nothing goes to the model until you press Ask or Ingest, and nothing enters the wiki until a person approves it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research wiki: neurotechnology in the administration of justice</title>
<style>
:root{--bg:#f4f0e8;--ink:#1d1b18;--mute:#5c574d;--rule:#d9d2c3;--red:#9b2335;--grn:#1f6b3a;--amb:#8a5a00;--ins:#fbf0b8;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;color:var(--ink);background:var(--bg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button,input,textarea{font:inherit;color:inherit}
.lab,.mono{font:11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.hint{font:12px/1.45 var(--mono);color:var(--mute)}
.top{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;padding:20px 28px 14px;border-bottom:1px solid var(--rule)}
h1{font:400 30px/1.15 var(--serif);margin:4px 0 6px}
.strip{text-align:right;font:11.5px/1.5 var(--mono);color:var(--mute);max-width:430px}
[role=tablist]{display:flex;flex-wrap:wrap;gap:0 4px;padding:0 28px;border-bottom:1px solid var(--rule)}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:12px 14px 9px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
.tab.on{color:var(--red);border-bottom-color:var(--red)}
main{padding:20px 28px 36px;max-width:1280px}
[role=tabpanel][hidden]{display:none}
h2.q{font:400 24px/1.25 var(--serif);margin:0 0 14px}
h2.ptitle{font:400 30px/1.2 var(--serif);margin:4px 0 8px}
.body h2{font:400 26px/1.2 var(--serif);margin:22px 0 8px}
.body h3,h3.s{font:400 21px/1.25 var(--serif);margin:22px 0 6px;border-top:1px solid var(--rule);padding-top:12px}
.body h4,.body h5{font:italic 400 18px/1.3 var(--serif);margin:16px 0 4px}
.cols{display:grid;grid-template-columns:320px minmax(0,1fr);gap:32px}
.cols>aside{position:sticky;top:8px;align-self:start;max-height:calc(100vh - 16px);overflow:auto;padding-right:8px}
.cols>div{max-width:900px}
@media(max-width:900px){.cols{grid-template-columns:1fr}.cols>aside{position:static;max-height:none}.top,main{padding-left:14px;padding-right:14px}[role=tablist]{padding:0 6px}.strip{text-align:left}}
.big{font:400 48px/1 var(--serif)}
.grp{font:11.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:16px 0 4px;border-bottom:1px solid var(--rule)}
ul.plist{list-style:none;margin:0;padding:0}
ul.plist li{padding:5px 0;border-bottom:1px solid var(--rule)}
ul.plist a{display:block}
ul.plist a[aria-current]{font-weight:700}
.stubtag{color:var(--red)}
input[type=search],input[type=text],textarea{width:100%;border:1px solid var(--ink);background:#fffdf8;padding:8px 10px;border-radius:2px}
textarea{resize:vertical}
.btn{border:1px solid var(--ink);background:transparent;padding:8px 14px;cursor:pointer;border-radius:2px}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.btn:disabled{opacity:.55;cursor:not-allowed}
.lnk{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer}
.grey{border-left:3px solid var(--rule);background:#ece7db;padding:8px 12px;margin:0 0 12px;font:12.5px/1.5 var(--mono)}
.badge{display:inline-block;border:1px solid var(--rule);padding:0 6px;margin:0 4px 4px 0;font:11.5px var(--mono)}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:15px}
caption{text-align:left;font:italic 18px var(--serif);padding:6px 0}
th{font:11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:6px 8px 6px 0;vertical-align:top}
td.n,th.n{text-align:right}
.pin{display:inline-flex;flex-wrap:wrap;align-items:baseline;gap:4px;border:1px solid var(--rule);border-radius:3px;padding:0 4px;margin:0 1px;background:#fbf8f1;font-size:14px;max-width:100%}
.pin.no{border-color:var(--amb)}
.pl{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font-size:14px;text-align:left}
.rg,.vw{font:11px var(--mono)}
.pin.ok .vw{color:var(--grn)}
.pin.no .vw{color:var(--amb)}
.px{border:0;background:none;cursor:pointer;padding:0 3px}
.pd{flex-basis:100%;display:block;font-size:13px;border-top:1px solid var(--rule);padding:4px 0}
.pd[hidden]{display:none}
.dangle{color:var(--red);font:12px var(--mono)}
.con{border:1px solid var(--rule);border-left:4px solid var(--red);padding:10px 14px;margin:14px 0;background:#faf7f0}
.con h4{font:400 19px/1.35 var(--serif);margin:4px 0}
.verdict{font:400 34px/1.1 var(--serif);margin:6px 0}
.bar{height:10px;background:var(--rule);margin:4px 0;max-width:420px}
.bar i{display:block;height:100%;background:var(--red)}
.ins{background:var(--ins);border-left:4px solid var(--amb);padding:2px 10px;margin:6px 0}
.dim{color:var(--mute)}
.dim .ins{color:var(--ink)}
.st{display:inline-block;min-width:54px;font:11.5px var(--mono);text-transform:uppercase;letter-spacing:.06em}
.st.ok{color:var(--grn)}
.st.no{color:var(--red);font-weight:700}
.st.na{color:var(--mute)}
.tag{font:11px var(--mono);color:var(--red);text-transform:uppercase;letter-spacing:.06em;margin-left:6px}
.err{border:1px solid var(--red);padding:10px 14px;margin:10px 0}
pre{white-space:pre-wrap;word-break:break-word;font:12px/1.4 var(--mono);background:#ece7db;padding:8px;max-height:220px;overflow:auto}
fieldset.chg{border:1px solid var(--ink);padding:10px 16px 14px;margin:10px 0}
legend{font:italic 19px var(--serif);padding:0 6px}
.prev{max-height:60vh;overflow:auto;border-top:1px solid var(--rule);margin:8px 0;padding-top:6px}
.steps{list-style:none;display:flex;flex-wrap:wrap;gap:6px 22px;margin:0 0 12px;padding:0;font:11.5px var(--mono);letter-spacing:.08em;color:var(--mute)}
.steps li.on{color:var(--red);border-bottom:2px solid var(--red)}
.nums{display:flex;gap:40px;margin:6px 0 10px}
.inb{display:flex;gap:16px;align-items:center;justify-content:space-between;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:10px 0}
details{margin:6px 0}
summary{cursor:pointer}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.chip{border:1px solid var(--rule);padding:1px 8px;border-radius:10px;font-size:14px;background:#fbf8f1}
.row2{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}
footer{border-top:1px solid var(--rule);padding:12px 28px 24px}
</style>
</head>
<body>
<header class="top">
 <div>
  <div class="lab">WIKI · neurotechnology and justice</div>
  <h1>Research wiki: neurotechnology in the administration of justice</h1>
  <p class="hint" id="hline"></p>
 </div>
 <div class="strip"><div id="strip" aria-live="polite"></div><div>This page has no storage: changes live in it until you download them (tab 05)</div></div>
</header>
<div id="tabs" role="tablist" aria-label="Workspace"></div>
<main>
 <section id="p1" role="tabpanel" aria-labelledby="t1">
  <div class="cols">
   <aside>
    <label for="flt" class="lab">title, tag or slug</label>
    <input id="flt" type="search" autocomplete="off">
    <div id="cnt" style="margin:12px 0 4px"></div>
    <div id="plist"></div>
   </aside>
   <div id="pview"></div>
  </div>
 </section>
 <section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
  <h2 class="q">What does the wiki answer, and is it worth filing?</h2>
  <div class="grey" id="askNote"></div>
  <label for="askQ" class="lab">Your question</label>
  <textarea id="askQ" rows="3"></textarea>
  <div class="row2"><button id="askBtn" class="btn pri" data-act="ask" type="button">Ask the wiki</button><button id="askStop" class="btn" data-act="ask-stop" type="button" hidden>Stop</button><span id="askProg" class="hint" aria-live="polite"></span></div>
  <div id="askOut"></div>
 </section>
 <section id="p3" role="tabpanel" aria-labelledby="t3" hidden>
  <h2 class="q">What would the waiting document change?</h2>
  <div id="ingOut"></div>
 </section>
 <section id="p4" role="tabpanel" aria-labelledby="t4" hidden>
  <h2 class="q">Can I trust this?</h2>
  <div id="chkOut"></div>
 </section>
 <section id="p5" role="tabpanel" aria-labelledby="t5" hidden>
  <h2 class="q">What has changed, where do the sources disagree, and how do I take it away?</h2>
  <div id="recOut"></div>
 </section>
</main>
<footer class="hint" id="foot"></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{}, WK=WD.wiki||{}, LIBR=(WD.library&&WD.library.records)||[];
const FENCE='`'.repeat(3);
const PIN_SRC='\\[([^\\]]+)\\]\\(pin:([^#\\s)]+)#p(\\d+)(?: "([^"]*)")?\\) ?(✓|⚠)';
const PIN_LOOSE=PIN_SRC.replace('(✓|⚠)','(✓|⚠)?');
const REGN={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGS={a:'treaty law',b:'General Comment',c:'UN report',d:'NHRI report',e:'civil society',f:'scholarship'};
const WT={a:5,b:4,c:3,d:2,e:1,f:.5};
const SEC={source:'Sources',concept:'Concepts',entity:'Entities',question:'Questions'};
const BASE=['01 PAGES','02 ASK','03 INGEST','04 CHECK','05 RECORD'];
const $=(s,r)=>(r||document).querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rx=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const nf=n=>Number(n).toLocaleString('en-GB');
const uniq=a=>[...new Set(a)];
const sum=(a,f)=>a.reduce((x,y)=>x+f(y),0);
const today=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');};
const slugify=s=>String(s||'').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,70);
const norm=s=>String(s==null?'':s).normalize('NFKC').replace(/­/g,'').replace(/-\s+/g,'').replace(/[“”„]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
const tryJ=s=>{try{return JSON.parse(s);}catch(e){return undefined;}};
const humanise=s=>{s=String(s).replace(/-/g,' ');return s.charAt(0).toUpperCase()+s.slice(1);};
const cleanMk=s=>String(s).replace(/^<<(?:ins|end)>>\n?/gm,'').replace(/\n{3,}/g,'\n\n');

let pages=[],bySlug={},docs={},orig={},index=WK.index||'',log=WK.log||'',tensions=WK.tensions||'';
let curPage='',curTab=0,loadedWarn=0,lintRan=false,lastFiling=null,logNewest=true,ing=null;
const S={calls:0,chars:0,passages:0,changes:[],filings:0,logAdded:new Set(),tensAdded:new Set(),callLog:[],approved:new Set()};
const running={2:false,3:false};
const pinReg=[];
const ask={q:'',stage:'idle',chosen:[],changing:false,answer:null,run:null,prog:'',err:null,file:null,filed:null,fTitle:'',fTags:''};

/* ---------- parsing and verification ---------- */
function parsePins(body){const re=new RegExp(PIN_SRC,'g'),o=[];let m;while((m=re.exec(body)))o.push({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]});return o;}
function conBlocks(body){const re=new RegExp(FENCE+'contested[ \\t]*\\n([\\s\\S]*?)\\n'+FENCE,'g'),o=[];let m;while((m=re.exec(body)))o.push(m[1]);return o;}
function frags(q){return String(q).split(/…|\.\.\./).map(norm).filter(Boolean);}
function inText(text,q){const fr=frags(q);if(!fr.length)return false;const t=norm(text);let pos=0;for(const f of fr){const k=t.indexOf(f,pos);if(k<0)return false;pos=k+f.length;}return true;}
function verify(pin,allow){
  const d=docs[pin.id];
  if(!d)return {ok:false,why:'no document '+pin.id+' in the library'};
  if(d.status==='inbox'&&allow!==pin.id)return {ok:false,why:'the document is in the inbox: not yet read into the wiki'};
  if(!pin.quote)return {ok:false,why:'the pin has no quote'};
  const fr=frags(pin.quote);if(!fr.length)return {ok:false,why:'the quote is empty'};
  const cands=(d.passages||[]).filter(x=>x.page===pin.page);
  if(!cands.length)return {ok:false,why:'no passage of '+pin.id+' starts on PDF page '+pin.page+' (footnotes, tables and captions are not in the passages)'};
  let bad=null;
  for(const x of cands){
    const t=x._n||(x._n=norm(x.text));let pos=0,ok=true;
    for(const f of fr){const k=t.indexOf(f,pos);if(k<0){ok=false;break;}pos=k+f.length;}
    if(!ok)continue;
    const want=x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
    if(new RegExp(rx(want)+'(?![\\w])').test(pin.label))return {ok:true,passage:x};
    bad={ok:false,labelBad:true,why:'quote found, but the label should say "'+want+'"',passage:x};
  }
  return bad||{ok:false,why:'quote not found in a passage that starts on PDF page '+pin.page};
}
function rebuild(){
  bySlug={};pages.forEach(p=>{bySlug[p.slug]=p;});
  pages.forEach(p=>{p._links=[...p.body.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim());p._pins=parsePins(p.body);p._v=p._pins.map(x=>verify(x));p._con=conBlocks(p.body);p._back=[];});
  pages.forEach(p=>uniq(p._links).forEach(l=>{if(bySlug[l]&&l!==p.slug)bySlug[l]._back.push(p.slug);}));
}
function vcount(p){return p._v.filter(v=>v.ok).length;}
function citeAs(d){
  const c={};pages.forEach(p=>p._pins.forEach(x=>{if(x.id===d.id){const m=x.label.match(/^(.*?), (?:para\.|p\.) /);if(m)c[m[1]]=(c[m[1]]||0)+1;}}));
  const b=Object.entries(c).sort((x,y)=>y[1]-x[1])[0];
  return b?b[0]:(d.symbol||((d.author||'')+' '+d.year));
}
function docReg(id){
  const d=docs[id];
  let p=pages.find(x=>x.type==='source'&&(x.frontmatter.sources||[]).length===1&&x.frontmatter.sources[0]===id);
  if(!p&&d)p=pages.find(x=>x.frontmatter.status==='stub'&&((x.frontmatter.sources||[]).includes(id)||x.slug===slugify(d.symbol||d.id)));
  return (p&&p.frontmatter.register)||[];
}
const regTxt=id=>{const r=docReg(id);return r.length?'('+r.join('')+')':'(?)';};
function mkPin(d,ps,quote){
  const q=quote.replace(/\s+/g,' ').replace(/"([^"]*)"/g,'“$1”').replace(/"/g,'”');
  return '['+citeAs(d)+(ps.paragraph?', para. '+ps.paragraph:', p. '+ps.page_label)+'](pin:'+d.id+'#p'+ps.page+' "'+q+'") ✓';
}
function fixPins(text,id){
  let ok=0,removed=0;const keep=[];
  let out=String(text).replace(new RegExp(PIN_LOOSE,'g'),(m,label,did,pg,quote)=>{
    const v=verify({label,id:did,page:+pg,quote:quote||''},id);
    if(v.ok){ok++;return '\u0001'+(keep.push('['+label+'](pin:'+did+'#p'+pg+' "'+quote+'") ✓')-1)+'\u0002';}
    removed++;return label+' (pin removed: not verified)';
  });
  out=out.replace(/\[([^\]]+)\]\(pin:[^)]*\)/g,(m,l)=>{removed++;return l+' (pin removed: malformed)';});
  out=out.replace(/\u0001(\d+)\u0002/g,(m,i)=>keep[+i]);
  return {text:out,ok,removed};
}

/* ---------- markdown ---------- */
function inline(s,ctx){
  const re=new RegExp(PIN_SRC+'|\\[\\[([^\\]|#]+)(?:[|#][^\\]]*)?\\]\\]|\\[([^\\]]+)\\]\\((https?:\\/\\/[^)\\s]+)\\)|\\*\\*(.+?)\\*\\*|\\*([^*\\s][^*]*?)\\*','g');
  let o='',last=0,m;
  while((m=re.exec(s))){
    o+=esc(s.slice(last,m.index));
    if(m[1]!==undefined)o+=pinChip({label:m[1],id:m[2],page:+m[3],quote:m[4]||'',mark:m[5]},ctx);
    else if(m[6]!==undefined)o+=wlink(m[6].trim());
    else if(m[7]!==undefined)o+='<a href="'+esc(m[8])+'" target="_blank" rel="noopener">'+esc(m[7])+'</a>';
    else if(m[9]!==undefined)o+='<strong>'+inline(m[9],ctx)+'</strong>';
    else o+='<em>'+esc(m[10])+'</em>';
    last=re.lastIndex;
  }
  return o+esc(s.slice(last));
}
function wlink(s){const p=bySlug[s];if(!p)return '<span class="dangle">[['+esc(s)+']] · no page</span>';return '<a href="#'+esc(s)+'" data-act="open-page" data-slug="'+esc(s)+'">'+esc(p.title)+'</a>';}
function pinChip(pin,ctx){
  const key=pin.id+'#p'+pin.page+'|'+norm(pin.quote);
  if(ctx&&ctx.allowed&&!ctx.allowed.has(key))return '<span class="pin no"><s>'+esc(pin.label)+'</s> <span class="vw">not on the pages sent</span></span>';
  const v=verify(pin,ctx&&ctx.allow),d=docs[pin.id];
  const i=pinReg.push({id:pin.id,page:pin.page,quote:pin.quote})-1;
  const diff=(pin.mark==='✓'&&!v.ok)?'page says ✓':(pin.mark==='⚠'&&v.ok)?'page says ⚠':'';
  const det=(pin.quote?'“'+esc(pin.quote)+'”':'<i>no quote</i>')+'<br>'+(v.passage?'Passage: '+(v.passage.paragraph?'para. '+esc(v.passage.paragraph):'p. '+esc(v.passage.page_label))+' · '+esc(v.passage.text.slice(0,300))+(v.passage.text.length>300?'…':''):'Not verified: '+esc(v.why))+'<br><button type="button" class="lnk" data-act="pin-open" data-pin="'+i+'" aria-label="Open '+esc(d?d.symbol||d.short_title:pin.id)+' at PDF page '+pin.page+'">Open the PDF page</button>';
  return '<span class="pin '+(v.ok?'ok':'no')+'"><button type="button" class="pl" data-act="pin-open" data-pin="'+i+'" aria-label="Open '+esc(pin.label)+' at PDF page '+pin.page+'">'+esc(pin.label)+'</button><span class="rg" title="register">'+regTxt(pin.id)+'</span><span class="vw">'+(v.ok?'✓ verified':'⚠ not found')+'</span>'+(diff?'<span class="vw">'+diff+'</span>':'')+'<button type="button" class="px" data-act="pin-toggle" aria-expanded="false" aria-label="Show the quote for '+esc(pin.label)+'">▾</button><span class="pd" hidden>'+det+'</span></span>';
}
function md(src,ctx){
  const L=String(src||'').replace(/\r/g,'').split('\n'),out=[],fenceRe=new RegExp('^'+FENCE+'(\\w*)\\s*$');
  let para=[],list=null,i=0;
  const fp=()=>{if(para.length){out.push('<p>'+inline(para.join(' '),ctx)+'</p>');para=[];}};
  const fl=()=>{if(list){out.push('<'+list.t+'>'+list.it.map(x=>'<li>'+inline(x,ctx)+'</li>').join('')+'</'+list.t+'>');list=null;}};
  while(i<L.length){
    const ln=L[i];let m;
    if((m=ln.match(fenceRe))){fp();fl();const buf=[];i++;while(i<L.length&&!fenceRe.test(L[i]))buf.push(L[i++]);i++;out.push(m[1]==='contested'?conCard(buf.join('\n'),ctx):'<pre>'+esc(buf.join('\n'))+'</pre>');continue;}
    if(ln==='<<ins>>'){fp();fl();out.push('<div class="ins" data-source="ai">');i++;continue;}
    if(ln==='<<end>>'){fp();fl();out.push('</div>');i++;continue;}
    if((m=ln.match(/^(#{1,4})\s+(.*)$/))){fp();fl();const n=m[1].length+1;out.push('<h'+n+'>'+inline(m[2],ctx)+'</h'+n+'>');i++;continue;}
    if((m=ln.match(/^\s*([-*]|\d+[.)])\s+(.*)$/))){fp();const t=/\d/.test(m[1])?'ol':'ul';if(list&&list.t!==t)fl();if(!list)list={t,it:[]};list.it.push(m[2]);i++;continue;}
    if(!ln.trim()){fp();fl();i++;continue;}
    if(list&&/^\s+\S/.test(ln)){list.it[list.it.length-1]+=' '+ln.trim();i++;continue;}
    fl();para.push(ln.trim());i++;
  }
  fp();fl();return out.join('\n');
}
function parseCon(txt){
  const o={claim:'',verdict:'',note:'',pos:[]};
  String(txt).split('\n').forEach(l=>{let m;
    if((m=l.match(/^claim:\s*(.*)$/)))o.claim=m[1];
    else if((m=l.match(/^verdict:\s*(.*)$/)))o.verdict=m[1].trim();
    else if((m=l.match(/^note:\s*(.*)$/)))o.note=m[1];
    else if((m=l.match(/^([+\-~])\s+(.*)$/))){const f=m[2].split(' | ');o.pos.push({sign:m[1],reg:(f[0]||'').trim().toLowerCase(),pin:f[1]||'',gloss:f[2]||'',page:f[3]||''});}
  });
  return o;
}
function conCard(txt,ctx){
  const c=parseCon(txt);let tot=0,sup=0;
  c.pos.forEach(x=>{const w=WT[x.reg]||0;tot+=w;sup+=x.sign==='+'?w:x.sign==='~'?w/2:0;});
  const pct=tot?Math.round(100*sup/tot):null,words={'+':'supports','-':'contests','~':'mixed'};
  const tn=ctx&&ctx.slug?tensEntries().items.find(x=>x.card===ctx.slug):null;
  return '<section class="con"><div class="lab">FIG.01 · contested claim</div><h4>'+inline(c.claim,ctx)+'</h4><div class="verdict">'+esc(c.verdict.replace(/-/g,' ')||'no verdict')+'</div><p>'+inline(c.note,ctx)+'</p>'
   +'<div class="hint">descriptive: support '+(pct==null?'n/a':pct+'%')+' of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</div>'
   +'<div class="bar" role="img" aria-label="Descriptive lean: '+(pct==null?'n/a':pct+' percent')+' support"><i style="width:'+(pct||0)+'%"></i></div>'
   +'<div class="hint">How this is computed: (weight of + positions + ½ weight of ~ positions) ÷ weight of all positions.</div>'
   +'<table><caption>Positions on this claim</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>'
   +c.pos.map(x=>'<tr><td>'+words[x.sign]+'</td><td class="mono">('+esc(x.reg)+') '+esc(REGS[x.reg]||'')+'</td><td>'+inline(x.pin,ctx)+'</td><td>'+inline(x.gloss,ctx)+'</td><td>'+inline(x.page,ctx)+'</td></tr>').join('')+'</tbody></table>'
   +(tn?'<a href="#" data-act="open-tens" data-head="'+esc(tn.head)+'">in the tensions register</a>':'')+'</section>';
}
function tensEntries(){
  const parts=tensions.split(/^### /m),intro=parts.shift();
  return {intro,items:parts.map(t=>{const nl=t.indexOf('\n'),head=(nl<0?t:t.slice(0,nl)).trim(),body=nl<0?'':t.slice(nl+1),m=body.match(/card:[^\n]*?\[\[([^\]|#]+)/);return {head,body,card:m?m[1].trim():null};})};
}
function logEntries(){
  const parts=log.split(/^## /m);parts.shift();
  return parts.map(t=>{const nl=t.indexOf('\n'),h=(nl<0?t:t.slice(0,nl)).trim();return {head:'## '+h,title:h,body:nl<0?'':t.slice(nl+1)};});
}

/* ---------- lint and self-checks ---------- */
function lintAll(){
  const idxSlugs=[...index.matchAll(/^\s*[-*]\s*\[\[([^\]|#]+)\]\]/gm)].map(m=>m[1].trim()),idxN={};
  index.split('\n').forEach(l=>{const m=l.match(/^\s*[-*]\s*\[\[([^\]|#]+)\]\][^\n]*✓\s*(\d+)/);if(m)idxN[m[1].trim()]=+m[2];});
  const te=tensEntries().items.filter(x=>x.card),C=[],add=(id,name,items)=>C.push({id,name,items});
  add('dang','Dangling links ([[slug]] with no page)',pages.flatMap(p=>uniq(p._links).filter(l=>!bySlug[l]).map(l=>({slug:p.slug,note:'[['+l+']]'}))));
  add('orph','Orphan pages (no other page links to them)',pages.filter(p=>!p._back.length).map(p=>({slug:p.slug})));
  add('unv','Pins not verified by this page',pages.flatMap(p=>p._pins.map((x,i)=>p._v[i].ok?null:{slug:p.slug,note:x.label+': '+p._v[i].why}).filter(Boolean)));
  add('lie','Pins marked ✓ that fail',pages.flatMap(p=>p._pins.map((x,i)=>(x.mark==='✓'&&!p._v[i].ok)?{slug:p.slug,note:x.label}:null).filter(Boolean)));
  add('src','Pages whose sources differ from the documents pinned',pages.filter(p=>{const a=uniq(p.frontmatter.sources||[]).sort().join('|'),b=uniq(p._pins.map(x=>x.id)).sort().join('|');return a!==b;}).map(p=>({slug:p.slug})));
  add('nop','Pages with no pins',pages.filter(p=>!p._pins.length).map(p=>({slug:p.slug})));
  add('rec','Links not reciprocated (A lists B, B does not list A)',pages.flatMap(p=>(p.frontmatter.links||[]).filter(l=>bySlug[l]&&!(bySlug[l].frontmatter.links||[]).includes(p.slug)).map(l=>({slug:p.slug,note:'→ '+l}))));
  add('idx','Pages missing from the index, and index lines without a page',[...pages.filter(p=>!idxSlugs.includes(p.slug)).map(p=>({slug:p.slug,note:'not in the index'})),...idxSlugs.filter(s=>!bySlug[s]).map(s=>({slug:s,note:'index line without a page'}))]);
  add('idn','Index ✓N that differs from the computed count',pages.filter(p=>p.slug in idxN&&idxN[p.slug]!==vcount(p)).map(p=>({slug:p.slug,note:'index '+idxN[p.slug]+', computed '+vcount(p)})));
  add('ten','Contested cards without a tensions entry, and the reverse',[...pages.filter(p=>p._con.length&&!te.some(x=>x.card===p.slug)).map(p=>({slug:p.slug,note:'no tensions entry'})),...te.filter(x=>!bySlug[x.card]||!bySlug[x.card]._con.length).map(x=>({slug:x.card,note:'tensions entry without a card'}))]);
  add('stub','Stub pages',pages.filter(p=>p.frontmatter.status==='stub').map(p=>({slug:p.slug})));
  add('inb','Pins to a document still in the inbox',pages.flatMap(p=>p._pins.filter(x=>docs[x.id]&&docs[x.id].status==='inbox').map(x=>({slug:p.slug,note:x.label}))));
  return C;
}
const needLook=()=>lintAll().filter(c=>c.items.length).length;
function slugLinks(items,max){
  const u=uniq(items.map(x=>x.slug)),sh=u.slice(0,max||12);
  return sh.map(s=>bySlug[s]?'<a href="#'+esc(s)+'" data-act="open-page" data-slug="'+esc(s)+'">'+esc(s)+'</a>':esc(s)).join(', ')+(u.length>sh.length?' … and '+(u.length-sh.length)+' more':'');
}
function selfChecks(){
  const R=[],L=Object.fromEntries(lintAll().map(c=>[c.id,c])),pins=sum(pages,p=>p._pins.length),ver=sum(pages,vcount);
  const m=index.split('\n').slice(0,8).join('\n').match(/(\d[\d,]*) pins/),stated=m?+m[1].replace(/,/g,''):null;
  const ck=(g,t,ok,items)=>R.push({g,t,ok,items:items||[]});
  ck('Pins','Pins found by the regular expression ('+nf(pins)+') against the number stated in the index ('+(stated==null?'none stated':nf(stated))+')',stated===pins);
  ck('Pins','Verified by this page ('+nf(ver)+') against found ('+nf(pins)+'); ✓ marks that fail: '+L.lie.items.length,ver===pins&&!L.lie.items.length,L.lie.items);
  const lb=sum(pages,p=>p._v.filter(v=>v.labelBad).length);
  ck('Labels','Pins whose quote is found but whose label does not match the passage’s paragraph or page label: '+lb,lb===0);
  ck('Structure','Dangling links '+L.dang.items.length+'; orphan pages '+L.orph.items.length,!L.dang.items.length&&!L.orph.items.length,[...L.dang.items,...L.orph.items]);
  ck('Structure','sources equal the pinned documents on '+(pages.length-L.src.items.length)+' of '+pages.length+' pages',!L.src.items.length,L.src.items);
  ck('Structure','Every page in the index and every index [[slug]] a page: '+L.idx.items.length+' differences',!L.idx.items.length,L.idx.items);
  ck('Structure','Contested cards ('+sum(pages,p=>p._con.length)+') against tensions card: entries ('+tensEntries().items.filter(x=>x.card).length+'): '+L.ten.items.length+' differences',!L.ten.items.length,L.ten.items);
  if(!S.callLog.length)ck('Model answers','No call to the model yet',null);
  S.callLog.forEach((c,i)=>ck('Model answers','Call '+(i+1)+' ('+c.kind+'): '+(c.parsed?'JSON parsed':'JSON not parsed')+'; slugs not in the wiki: '+((c.bad||[]).length)+(c.returned!=null?'; returned '+c.returned+' = verified '+c.ver+' + could not verify '+c.fail+' + dropped '+c.drop:''),c.parsed&&(c.returned==null||c.returned===c.ver+c.fail+c.drop)));
  if(!ing)ck('Coverage','No ingest started',null);
  else{const n=ing.doc.passages.length,done=ing.next>=ing.batches.length;ck('Coverage','Passages sent ('+ing.sent+') against passages.length ('+n+')'+(done?'':' — the run is not complete')+'; takeaways naming a passage that was not sent: dropped and counted ('+ing.dropped+')',done?ing.sent===n:null);}
  const warn=sum(pages,p=>p._pins.filter(x=>x.mark==='⚠').length);
  const changed=pages.filter(p=>!(p.slug in orig)||orig[p.slug]!==p.body),badCh=sum(changed,p=>p._v.filter(v=>!v.ok).length);
  ck('Unverified','⚠ pins in the wiki now: '+warn+' (at load: '+loadedWarn+'); pins in changed pages that do not verify: '+badCh,warn===loadedWarn&&badCh===0);
  if(ing&&ing.tk.length){const v=ing.tk.filter(t=>t.ok).length,f=ing.tk.length-v;ck('Unverified','Could not verify ('+f+') plus verified takeaways ('+v+') equal takeaways returned ('+ing.tkRet+') less those dropped ('+ing.dropped+')',f+v===ing.tkRet-ing.dropped);}
  const una=changed.filter(p=>!S.approved.has(p.slug));
  ck('Approval','Pages changed in the wiki ('+changed.length+') against approved changes ('+S.approved.size+'); changed without an approved card: '+una.length,!una.length&&changed.length===S.approved.size,una.map(p=>({slug:p.slug})));
  if(!S.filings)ck('Filing','Nothing filed yet',null);
  else{
    const lastLog=logEntries().slice(-1)[0],names=lastFiling?lastFiling.slugs:[];
    const miss=names.filter(s=>!(lastLog&&lastLog.body.includes('[['+s+']]'))&&!(lastLog&&lastLog.title.includes(s)));
    const idxBad=lintAll().find(c=>c.id==='idn').items;
    ck('Filing','Changed pages re-parsed and re-verified (pins that fail: '+badCh+'); index counts equal the pages’ verified pins ('+idxBad.length+' differences); last log entry names '+(names.length-miss.length)+' of '+names.length+' changed pages',badCh===0&&!idxBad.length&&!miss.length);
    if(lastFiling)ck('Filing','Lint checks needing a look: before '+lastFiling.before+', after '+lastFiling.after+' (side by side)',lastFiling.after<=lastFiling.before);
  }
  ck('Session','Log entries added this session ('+S.logAdded.size+') against filings made ('+S.filings+'); a download would hold '+pages.length+' pages (pages.length '+pages.length+')',S.logAdded.size===S.filings);
  return R;
}

/* ---------- rendering: header, tabs, pages ---------- */
function setRunning(k,b){running[k]=b;const s=$('#t'+k+' .run');if(s)s.textContent=b?' · running':'';}
function renderStrip(){$('#strip').textContent='Changes this session: '+S.changes.length+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;}
function renderHead(){
  const c={};pages.forEach(p=>{c[p.type]=(c[p.type]||0)+1;});
  const inbox=Object.values(docs).filter(d=>d.status==='inbox').length;
  $('#hline').textContent=pages.length+' pages ('+(c.source||0)+' sources, '+(c.concept||0)+' concepts, '+(c.entity||0)+' entities, '+(c.question||0)+' questions) · '+nf(sum(pages,p=>p._pins.length))+' pins, '+nf(sum(pages,vcount))+' verified by this page · '+LIBR.length+' documents, '+inbox+' in the inbox · built '+(WK.built||'unknown');
  renderStrip();
}
function showTab(i,focus){
  curTab=i;const tabs=document.querySelectorAll('.tab');
  tabs.forEach((b,k)=>{const on=k===i;b.setAttribute('aria-selected',String(on));b.tabIndex=on?0:-1;b.classList.toggle('on',on);$('#p'+(k+1)).hidden=!on;});
  if(focus)tabs[i].focus();
  if(i===3)renderCheck();
  if(i===4)renderRecord();
}
function openPage(slug){
  curPage=bySlug[slug]?slug:'';
  try{if(decodeURIComponent(location.hash.slice(1))!==curPage)location.hash=curPage;}catch(e){}
  showTab(0);renderList();renderPageView();window.scrollTo(0,0);
}
function openTens(head){showTab(4);const el=document.getElementById('tens-'+slugify(head));if(el){el.scrollIntoView();el.querySelector('summary').focus();el.open=true;}}
function renderList(){
  const q=($('#flt').value||'').trim().toLowerCase();
  const f=pages.filter(p=>!q||(p.title+' '+p.slug+' '+(p.frontmatter.tags||[]).join(' ')).toLowerCase().includes(q));
  $('#cnt').innerHTML='<span class="big">'+f.length+'</span> <span class="hint">of '+pages.length+' pages</span>';
  const order=['source','concept','entity','question'].concat(uniq(pages.map(p=>p.type)).filter(t=>!SEC[t]));
  let h='';
  order.forEach(t=>{const g=f.filter(p=>p.type===t);if(!g.length)return;
    h+='<div class="grp">'+esc(t)+' ('+g.length+')</div><ul class="plist">'+g.map(p=>'<li><a href="#'+esc(p.slug)+'" data-act="open-page" data-slug="'+esc(p.slug)+'"'+(p.slug===curPage?' aria-current="page"':'')+'>'+esc(p.title)+'</a><span class="hint">('+esc((p.frontmatter.register||[]).join(''))+') · '+p._pins.length+' pins'+(p.frontmatter.status==='stub'?' · <b class="stubtag">stub</b>':'')+'</span></li>').join('')+'</ul>';});
  $('#plist').innerHTML=h||'<p class="hint">No page matches.</p>';
}
function pageMarkdown(p){return '---\n'+Object.keys(p.frontmatter).map(k=>k+': '+JSON.stringify(p.frontmatter[k])).join('\n')+'\n---\n\n'+p.body;}
function renderPageView(){
  const el=$('#pview');
  if(!curPage||!bySlug[curPage]){el.innerHTML='<div class="lab">INDEX · what does the wiki say?</div><h2 class="ptitle">Index</h2><div class="body">'+md(index,{})+'</div><p class="hint">How this is computed: the index is the wiki’s own text. Pins counted here and in the header are found by this page’s code, not read from the index. Choose a page on the left.</p>';return;}
  const p=bySlug[curPage],fm=p.frontmatter,ctx={slug:p.slug},bl=p._links;
  const body=p.body.replace(/^#\s+.*\n+/,'');
  const out=uniq(fm.links||[]),src=fm.sources||[];
  el.innerHTML='<article><div class="lab"><a href="#" data-act="open-page" data-slug="">Index</a> · PAGE · '+esc(p.slug)+'</div><h2 class="ptitle">'+esc(p.title)+'</h2>'
   +'<div><span class="badge">'+esc(p.type)+'</span>'+(fm.register||[]).map(l=>'<span class="badge">('+esc(l)+') '+esc(REGN[l]||'')+'</span>').join('')+'<span class="badge">status: '+esc(fm.status||'?')+'</span><span class="badge">updated '+esc(fm.updated||'?')+'</span></div>'
   +'<div class="hint">tags: '+esc((fm.tags||[]).join(', ')||'none')+'</div>'
   +'<div class="body">'+md(body,ctx)+'</div>'
   +'<p class="hint">How this is computed: '+p._pins.length+' pins found in this body by regular expression; '+vcount(p)+' verified = the quote (fragments in order) stands in a passage of that document starting on that PDF page, and the label names its paragraph or page label.</p>'
   +'<h3 class="s">Links out</h3>'+(out.length?'<ul>'+out.map(s=>'<li>'+wlink(s)+(bl.includes(s)?'':' <span class="hint">frontmatter only</span>')+'</li>').join('')+'</ul>':'<p class="hint">none</p>')
   +'<h3 class="s">Linked from</h3>'+(p._back.length?'<ul>'+p._back.map(s=>'<li>'+wlink(s)+'</li>').join('')+'</ul>':'<p class="hint">no page links here</p>')
   +'<h3 class="s">Sources</h3>'+(src.length?'<ul>'+src.map(id=>{const d=docs[id];return d?'<li><a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.short_title||d.title)+'</a> <span class="hint">'+esc(d.kind)+' · '+esc(d.year)+(d.status==='inbox'?' · inbox':'')+'</span></li>':'<li>'+esc(id)+' <span class="hint">not in the library</span></li>';}).join('')+'</ul>':'<p class="hint">none</p>')
   +'<p><button type="button" class="btn" data-act="copy-page">Copy page as markdown</button></p></article>';
}

/* ---------- model calls ---------- */
async function callModel(prompt,nPass,kind){
  S.calls++;S.chars+=prompt.length;S.passages+=nPass;renderStrip();
  const rec={kind,parsed:false};S.callLog.push(rec);
  let raw;
  try{if(!(window.studio&&typeof studio.ask==='function'))throw new Error('studio.ask is not available in this preview');raw=await studio.ask(prompt,{json:true});}
  catch(e){return {ok:false,raw:'',error:String(e&&e.message||e),rec};}
  let d;
  if(raw&&typeof raw==='object'){d=raw;raw=JSON.stringify(raw);}
  else{raw=String(raw==null?'':raw);d=tryJ(raw);
    if(d===undefined){const m=raw.match(new RegExp(FENCE+'(?:json)?\\s*([\\s\\S]*?)'+FENCE));if(m)d=tryJ(m[1]);}
    if(d===undefined){const a=raw.indexOf('{'),b=raw.lastIndexOf('}');if(a>=0&&b>a)d=tryJ(raw.slice(a,b+1));}}
  if(d===undefined||d===null||typeof d!=='object')return {ok:false,raw,rec};
  rec.parsed=true;return {ok:true,data:d,raw,rec};
}
const PINRULE='Pin syntax: [label](pin:ID#pPAGE "verbatim quote") ✓. Quote only words that stand in the passages given; the code will check every quotation, and a pin that does not verify is removed.';
const REGRULE='Registers: (a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship. Name the register where it matters, keep the document’s own verb ("notes", "recommends", "proposes"), and never present (c) to (f) as what the treaty requires.';
function errHtml(e,act){return '<div class="err" role="alert"><p>The model’s answer could not be used'+(e.why?': '+esc(e.why):'')+'. Nothing was filed.</p><pre data-source="ai">'+esc(e.raw||'(no answer)')+'</pre><button type="button" class="btn" data-act="'+act+'">Retry</button></div>';}

/* ---------- tab 02: ask ---------- */
function pinKey(p){return p.id+'#p'+p.page+'|'+norm(p.quote);}
function askEval(){
  const a=ask.answer,pins=parsePins(a.answer);let good=0,bad=0;const reg={};
  pins.forEach(p=>{if(a.allowed.has(pinKey(p))&&verify(p).ok){good++;const r=(docReg(p.id)[0]||'?');reg[r]=(reg[r]||0)+1;}else bad++;});
  return {pins,good,bad,reg};
}
function buildQ(){
  const a=ask.answer,title=(ask.fTitle||a.title||'Untitled question').trim();
  const base=slugify(title)||'question';let slug=base,n=2;while(bySlug[slug])slug=base+'-'+n++;
  const pins=parsePins(a.answer),text=a.answer.trim(),first=text.split(/\n\s*\n/)[0];
  const links=uniq([...text.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>bySlug[s]);
  const sources=uniq(pins.map(p=>p.id)),reg=uniq(sources.flatMap(id=>docReg(id))).sort();
  const tags=(ask.fTags||'').split(',').map(s=>s.trim()).filter(Boolean);
  const body='# '+title+'\n\n**Short answer.** '+first+'\n\n## Reasoning\n\n'+text+'\n\n## What the library cannot answer\n\n'+(a.cannot||'Nothing was flagged.')+'\n\n## Related\n\n'+(links.map(s=>'- [['+s+']]').join('\n')||'- (no page linked)')+'\n';
  const ev=askEval(),reasons=[];
  if(!ev.pins.length)reasons.push('the answer has no pins');
  if(ev.bad)reasons.push(ev.bad+' pin(s) are struck through or do not verify');
  return {slug,title,first,body,links,sources,reg,tags,ev,reasons,fileable:!reasons.length,
    page:{slug,type:'question',title,body,frontmatter:{title,type:'question',tags,register:reg,status:'draft',updated:today(),links,sources}}};
}
function plain(s){return String(s).replace(new RegExp(PIN_LOOSE,'g'),'').replace(/\[\[([^\]|#]+)\]\]/g,'$1').replace(/[*_]/g,'').replace(/\s+/g,' ').trim();}
function renderAsk(){
  const a=ask,run=!!a.run;
  const k=a.chosen.length,ch=sum(a.chosen,s=>bySlug[s]?bySlug[s].body.length:0);
  $('#askNote').textContent=a.stage==='chosen'?'Step 2 will send '+k+' pages, '+nf(ch)+' characters, and your question. 0 library passages will leave the browser.'
   :a.stage==='s2'?k+' pages, '+nf(ch)+' characters; 0 library passages have left the browser.'
   :'Step 1 sends the wiki’s index ('+nf(index.length)+' characters) and your question to a language model. Step 2 then sends the bodies of up to 5 pages it names, announced here first. No library passages are sent. Nothing is sent until you press the button.';
  const b=$('#askBtn');b.textContent=a.stage==='chosen'?'Send these '+k+' pages':a.answer?'Ask again':'Ask the wiki';b.disabled=run;
  $('#askStop').hidden=!run;$('#askProg').textContent=a.prog||'';
  let h='';
  if(a.err)h+=errHtml(a.err,a.err.retry==='ask2'?'ask-retry2':'ask-retry1');
  if((a.chosen.length||a.changing)&&(a.stage==='chosen'||a.stage==='s2'||a.answer||a.changing)){
    h+='<div data-source="ai"><div class="lab">Pages chosen by the model</div><div class="chips">'+a.chosen.map(s=>'<span class="chip">'+wlink(s)+'</span>').join('')+'</div></div>';
    if(!run)h+='<button type="button" class="lnk" data-act="ask-change">Change pages</button>';
    if(a.changing)h+='<fieldset><legend>Tick up to 5 pages</legend>'+pages.map(p=>'<label style="display:block"><input type="checkbox" data-pick="'+esc(p.slug)+'"'+(a.chosen.includes(p.slug)?' checked':'')+'> '+esc(p.title)+'</label>').join('')+'</fieldset>';
  }
  if(a.answer){
    const A=a.answer,ev=askEval();
    h+='<article data-source="ai" style="border-top:1px solid var(--rule);margin-top:14px"><div class="lab">ANSWER · written by the model, every pin checked by this page</div><h3 class="s">'+esc(A.title||'Answer')+'</h3><div class="body">'+md(A.answer,{allowed:A.allowed})+'</div><h4>What the library cannot answer</h4><p>'+esc(A.cannot||'Nothing was flagged.')+'</p></article>';
    h+='<p class="hint">Verified pins by register: '+(Object.keys(ev.reg).sort().map(r=>'('+r+') '+(REGS[r]||'?')+' '+ev.reg[r]).join(' · ')||'none')+' · struck through or failing: '+ev.bad+'</p>';
    h+='<div class="row2"><button type="button" class="btn" data-act="ask-file-open" aria-expanded="'+!!a.file+'">File as a question page</button></div>';
    if(a.file)h+='<fieldset class="chg"><legend>File as a question page</legend><label for="fT" class="lab">Title</label><input id="fT" type="text" value="'+esc(a.fTitle||A.title)+'"><label for="fG" class="lab">Tags (comma-separated)</label><input id="fG" type="text" value="'+esc(a.fTags)+'"><div id="fPrev"></div></fieldset>';
  }
  if(a.filed)h+='<p aria-live="polite"><b>Filed.</b> The page is now in the wiki: '+wlink(a.filed)+'. The index and the log were updated.</p>';
  $('#askOut').innerHTML=h;
  if(a.file)updFile();
}
function updFile(){
  const q=buildQ(),el=$('#fPrev');if(!el)return;
  el.innerHTML='<p class="hint">Preview of the page the code will build. slug: '+esc(q.slug)+' · type: question · register: ('+esc(q.reg.join(''))+') · status: draft · updated '+today()+' · links: '+q.links.length+' · sources: '+esc(q.sources.join(', '))+'</p><div class="prev" data-source="ai">'+md(q.body,{allowed:ask.answer.allowed})+'</div>'
   +'<div class="row2"><button type="button" class="btn pri" data-act="ask-file"'+(q.fileable?'':' disabled')+'>File this page</button><button type="button" class="btn" data-act="ask-copy">Copy answer</button><span class="hint">'+(q.fileable?'Every pin verifies.':'Disabled: '+esc(q.reasons.join('; '))+'.')+'</span></div>';
}
async function askStep1(){
  const q=($('#askQ').value||'').trim();ask.q=q;
  if(!q){ask.prog='Type a question first.';renderAsk();return;}
  const run={stop:false};ask.run=run;ask.stage='s1';ask.answer=null;ask.file=null;ask.filed=null;ask.err=null;ask.changing=false;ask.chosen=[];
  ask.prog='Step 1 of 2 · sending the index ('+nf(index.length)+' characters) and your question…';setRunning(2,true);renderAsk();
  const prompt='You help with a research wiki on neurotechnology in the administration of justice. Below are the wiki’s index (one line per page) and a question. Choose up to 5 pages whose bodies are most likely to answer it. Return JSON {"pages": ["slug", ...]} using only slugs that appear in the index.\n\nINDEX\n'+index+'\n\nQUESTION\n'+q;
  const r=await callModel(prompt,0,'ask, step 1');
  if(run.stop)return;
  ask.run=null;setRunning(2,false);
  if(!r.ok){ask.stage='err';ask.err={raw:r.raw||r.error,retry:'ask1'};ask.prog='';return renderAsk();}
  const names=uniq((Array.isArray(r.data.pages)?r.data.pages:[]).map(s=>String(s).replace(/^\[\[|\]\]$/g,'').trim())),good=names.filter(s=>bySlug[s]).slice(0,5);
  r.rec.bad=names.filter(s=>!bySlug[s]);
  if(!good.length){ask.stage='err';ask.err={raw:r.raw,retry:'ask1',why:'it named no page that exists in the index'};ask.prog='';return renderAsk();}
  ask.chosen=good;ask.stage='chosen';ask.prog='Step 1 done · '+good.length+' pages chosen'+(r.rec.bad.length?' · '+r.rec.bad.length+' unknown slug(s) dropped':'')+'.';renderAsk();
}
async function askStep2(){
  const sent=ask.chosen.map(s=>bySlug[s]).filter(Boolean),ch=sum(sent,p=>p.body.length);
  const run={stop:false};ask.run=run;ask.stage='s2';ask.err=null;ask.changing=false;
  ask.prog='Step 2 of 2 · sending '+sent.length+' pages, '+nf(ch)+' characters; 0 library passages have left the browser.';setRunning(2,true);renderAsk();
  const prompt='You answer one question from a research wiki on neurotechnology in the administration of justice, using ONLY the wiki pages below.\n'+PINRULE+' Copy pins exactly as they stand on the pages; do not write a pin that is not on them.\n'+REGRULE+'\nAnswer in at most 350 words of markdown; you may link pages as [[slug]]. If the pages cannot answer part of the question, say so in cannot_answer instead of guessing.\nReturn JSON {"title": "a short title for the question", "answer": "...", "cannot_answer": "..."}.\n\nQUESTION\n'+ask.q+'\n\n'+sent.map(p=>'=== PAGE '+p.slug+' ('+(p.frontmatter.register||[]).join('')+') ===\n'+p.body).join('\n\n');
  const r=await callModel(prompt,0,'ask, step 2');
  if(run.stop)return;
  ask.run=null;setRunning(2,false);
  if(!r.ok||typeof r.data.answer!=='string'||!r.data.answer.trim()){ask.stage='chosen';ask.err={raw:r.raw||r.error,retry:'ask2',why:r.ok?'it returned no answer text':''};ask.prog='';return renderAsk();}
  const allowed=new Set();sent.forEach(p=>parsePins(p.body).forEach(x=>allowed.add(pinKey(x))));
  ask.answer={title:String(r.data.title||'').trim(),answer:r.data.answer,cannot:String(r.data.cannot_answer||'').trim(),allowed};
  r.rec.bad=uniq([...r.data.answer.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>!bySlug[s]);
  ask.stage='done';ask.fTitle='';ask.fTags='';ask.prog='Done. '+parsePins(r.data.answer).length+' pins in the answer, each checked by this page.';renderAsk();
}
function addIndexLine(section,line){
  const L=index.split('\n'),re=new RegExp(rx(section),'i');
  const h=L.findIndex(l=>/^#{1,4}\s/.test(l)&&re.test(l));
  if(h<0){L.push('','## '+section,line);}
  else{let j=h+1,last=h;while(j<L.length&&!/^#{1,4}\s/.test(L[j])){if(L[j].trim())last=j;j++;}L.splice(last+1,0,line);}
  index=L.join('\n');
}
function setIndexLine(slug,line){const re=new RegExp('^\\s*[-*]\\s*\\[\\['+rx(slug)+'\\]\\]');index=index.split('\n').map(l=>re.test(l)?line:l).join('\n');}
function setIndexN(slug,n){const re=new RegExp('^\\s*[-*]\\s*\\[\\['+rx(slug)+'\\]\\]');index=index.split('\n').map(l=>re.test(l)?l.replace(/✓\s*\d+/,'✓'+n):l).join('\n');}
function fixIndexHead(){
  const L=index.split('\n'),n=sum(pages,p=>p._pins.length);
  for(let i=0;i<Math.min(L.length,8);i++)if(/(\d[\d,]*) pins/.test(L[i])){L[i]=L[i].replace(/(\d[\d,]*) pins/,nf(n)+' pins').replace(/(\d+) pages/,pages.length+' pages');break;}
  index=L.join('\n');
}
function fileQuestion(){
  const q=buildQ();if(!q.fileable)return;
  const t=today(),before=needLook();
  pages.push(q.page);rebuild();
  const p=bySlug[q.slug],n=vcount(p);
  addIndexLine('Questions','- [['+q.slug+']] — '+(plain(q.first).slice(0,140)||q.title)+' · ('+q.reg.join('')+') · ✓'+n);fixIndexHead();
  const head='## ['+t+'] ask | '+q.title;
  log=log.replace(/\s+$/,'')+'\n\n'+head+'\n\nQuestion: "'+ask.q.replace(/"/g,'”')+'". Filed as [['+q.slug+']] from '+ask.chosen.length+' pages ('+ask.chosen.map(s=>'[['+s+']]').join(', ')+'). '+n+' pins, all verified.\n';
  S.logAdded.add(head);S.changes.push({date:t,kind:'ask',slug:q.slug,how:'new page'});S.approved.add(q.slug);S.filings++;
  lintRan=true;lastFiling={before,after:needLook(),slugs:[q.slug]};
  ask.filed=q.slug;ask.file=null;renderAll();
}

/* ---------- tab 03: ingest ---------- */
const inboxDocs=()=>Object.values(docs).filter(d=>d.status==='inbox');
function openIngest(id){
  const d=docs[id],ps=d.passages||[],B=[];
  for(let i=0;i<ps.length;i+=25){const ch=ps.slice(i,i+25),nums=ch.map(p=>p.paragraph).filter(Boolean),pg=ch.map(p=>p.page),lo=Math.min(...pg),hi=Math.max(...pg);
    B.push({n:B.length+1,passages:ch,para:nums.length?nums[0]+(nums.length>1?' – '+nums[nums.length-1]:''):'none numbered',pp:lo+(hi>lo?' – '+hi:''),chars:sum(ch,p=>p.text.length),state:'todo'});}
  ing={doc:d,stage:1,batches:B,next:0,sent:0,tk:[],tkRet:0,dropped:0,run:null,prog:'',err:null,src:null,srcSlug:'',touchesRaw:[],touched:null,drafted:0,cards:[],i:0,dec:{},newOK:new Set(),filed:null,c0:S.calls,p0:S.passages,skipped:[]};
  renderIngest();
}
function takePrompt(g,b){
  const d=g.doc;
  return 'You are reading a document that is waiting to be added to a research wiki on neurotechnology in the administration of justice.\nDOCUMENT: '+d.title+' ('+citeAs(d)+', '+d.year+'), register '+regTxt(d.id)+'.\nBelow are (1) the wiki’s index and (2) a batch of passages from the document as JSON {id, page, paragraph, text}.\nReturn JSON {"takeaways":[{"claim":"...","quote":"...","passage":"<passage id>","pages":["slug"]}]}.\n- At most 10 takeaways; keep only claims that bear on the administration of justice (evidence, torture and ill-treatment, fair trial, self-incrimination, recommendations); skip the rest.\n- claim: one sentence saying what the document says, with its own verb; do not turn a report’s statement into law.\n- quote: 8 to 40 words copied verbatim from that one passage. Quote only words that stand in the passages given; the code will check every quotation.\n- passage: the id of the passage the quote comes from.\n- pages: slugs from the index that the claim bears on.\n\nINDEX\n'+index+'\n\nPASSAGES\n'+JSON.stringify(b.passages.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,text:p.text})));
}
function lcsRun(a,b){let best=0;const prev=new Array(b.length+1).fill(0);for(let i=1;i<=a.length;i++){let diag=0;for(let j=1;j<=b.length;j++){const t=prev[j];prev[j]=a[i-1]===b[j-1]?diag+1:0;if(prev[j]>best)best=prev[j];diag=t;}}return best;}
function nearest(doc,ps,quote){
  const qw=norm(quote).toLowerCase().split(' ');let best=null;
  doc.passages.filter(x=>x.page===ps.page).forEach(x=>{const r=lcsRun(qw,norm(x.text).toLowerCase().split(' '));if(!best||r>best.run)best={p:x,run:r};});
  return best||{p:ps,run:0};
}
function procBatch(g,b,data){
  const arr=Array.isArray(data.takeaways)?data.takeaways:[],rows=arr.slice(0,10);let ver=0,fail=0,drop=arr.length-rows.length;const bad=[];
  g.tkRet+=arr.length;
  rows.forEach(t=>{
    const claim=String(t&&t.claim||'').trim(),quote=String(t&&t.quote||'').replace(/\s+/g,' ').trim(),pid=String(t&&t.passage||'').trim(),tail=pid.replace(/^.*#/,'');
    const ps=b.passages.find(p=>p.id===pid)||(/^\d+$/.test(tail)?b.passages.find(p=>p.id===g.doc.id+'#'+tail):null);
    if(!ps||!claim||!quote){drop++;return;}
    const slugs=[];
    (Array.isArray(t.pages)?t.pages:[]).forEach(s=>{s=String(s).replace(/^\[\[|\]\]$/g,'').trim();
      if(bySlug[s])slugs.push(s);
      else if(/^[a-z0-9][a-z0-9-]*$/.test(s)&&(g.newOK.has(s)||g.newOK.size<2)){g.newOK.add(s);slugs.push(s);}
      else bad.push(s);});
    const e={claim,quote,ps,slugs:uniq(slugs),ok:inText(ps.text,quote),batch:b.n};
    if(e.ok){e.pin=mkPin(g.doc,ps,quote);if(!verify(parsePins(e.pin)[0],g.doc.id).ok)e.ok=false;}
    if(e.ok)ver++;else{e.near=nearest(g.doc,ps,quote);fail++;}
    g.tk.push(e);
  });
  g.dropped+=drop;
  return {returned:arr.length,ver,fail,drop,bad};
}
async function runBatches(){
  const g=ing;g.stage=2;g.err=null;const run={stop:false};g.run=run;setRunning(3,true);renderIngest();
  while(g.next<g.batches.length&&!run.stop){
    const b=g.batches[g.next];b.state='running';
    g.prog='batch '+b.n+' of '+g.batches.length+' · '+(g.sent+b.passages.length)+' of '+g.doc.passages.length+' passages have left the browser';
    g.sent+=b.passages.length;renderIngest();
    const r=await callModel(takePrompt(g,b),b.passages.length,'takeaways, batch '+b.n+' of '+g.batches.length);
    if(run.stop)return;
    if(!r.ok){g.sent-=b.passages.length;b.state='failed';g.err={raw:r.raw||r.error,retry:'batch'};break;}
    Object.assign(r.rec,procBatch(g,b,r.data));b.state='done';g.next++;
  }
  g.run=null;setRunning(3,false);
  g.prog=g.err?'':(g.next>=g.batches.length?'All '+g.batches.length+' batches have returned.':'');
  renderIngest();
}
function stopIngest(){
  const g=ing;if(!g||!g.run)return;g.run.stop=true;g.run=null;setRunning(3,false);
  if(g.stage===2){const b=g.batches[g.next];if(b&&b.state==='running'){b.state='todo';g.sent-=b.passages.length;}}
  g.prog='Stopped. What has returned is kept.';renderIngest();
}
function stopAsk(){
  if(!ask.run)return;ask.run.stop=true;ask.run=null;setRunning(2,false);
  ask.stage=ask.chosen.length&&ask.stage==='s2'?'chosen':ask.stage==='s1'?'idle':ask.stage;ask.prog='Stopped.';renderAsk();
}
function blocks(t){return String(t).split(/\n\s*\n/).filter(s=>s.trim()).length;}
function insertAfter(body,after,text){
  const blk=['','<<ins>>',text,'<<end>>',''],want=String(after).replace(/^#+\s*/,'').trim().toLowerCase();
  const atEnd=note=>({body:body.replace(/\s+$/,'')+'\n'+blk.join('\n'),note});
  if(!want||want==='end')return atEnd('');
  const L=body.split('\n');let h=-1,lvl=0;
  for(let pass=0;pass<2&&h<0;pass++)for(let i=0;i<L.length;i++){const m=L[i].match(/^(#{1,4})\s+(.*)$/);if(m&&(pass?m[2].toLowerCase().includes(want):m[2].trim().toLowerCase()===want)){h=i;lvl=m[1].length;break;}}
  if(h<0)return atEnd('Heading "'+after+'" was not found: the text is placed at the end of the page.');
  let j=h+1;while(j<L.length){const m=L[j].match(/^(#{1,4})\s/);if(m&&m[1].length<=lvl)break;j++;}
  L.splice(j,0,...blk);return {body:L.join('\n'),note:''};
}
function cleanCon(raw,id){
  if(!raw||typeof raw!=='string')return null;
  let s=raw.trim();const m=s.match(new RegExp(FENCE+'(?:contested)?[ \\t]*\\n([\\s\\S]*?)\\n?'+FENCE));if(m)s=m[1];s=s.trim();
  if(!/^claim:/m.test(s)||!/^verdict:/m.test(s)||!/^[+\-~]\s/m.test(s))return null;
  return fixPins(s,id);
}
function srcPrompt(g,vt){
  const d=g.doc;
  return 'You write the source page for a document being added to a research wiki on neurotechnology in the administration of justice.\nDOCUMENT: '+d.title+'; author: '+d.author+'; published: '+d.published+'; '+d.pages+' PDF pages; url: '+d.url+'; cite as: '+citeAs(d)+'; register '+regTxt(d.id)+'.\n'+PINRULE+' Use only the pins listed below, copied exactly.\n'+REGRULE+'\nPage anatomy, as ## headings in this order: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related. Link wiki pages as [[slug]].\nReturn JSON {"one_liner":"...","body":"markdown, at most 900 words","touches":[{"slug":"...","why":"..."}]}.\n\nVERIFIED TAKEAWAYS\n'+vt.map((t,i)=>(i+1)+'. '+t.claim+'\n   pin: '+t.pin+'\n   pages: '+t.slugs.join(', ')).join('\n')+'\n\nINDEX\n'+index;
}
async function draftSource(){
  const g=ing,vt=g.tk.filter(t=>t.ok),d=g.doc;g.err=null;const run={stop:false};g.run=run;g.prog='Drafting the source page (1 call)…';setRunning(3,true);renderIngest();
  const r=await callModel(srcPrompt(g,vt),0,'source page');
  if(run.stop)return;
  g.run=null;setRunning(3,false);
  if(!r.ok||typeof r.data.body!=='string'){g.err={raw:r.raw||r.error,retry:'src',why:r.ok?'it returned no page body':''};g.prog='';return renderIngest();}
  const f=fixPins(r.data.body,d.id),base=slugify(d.symbol||d.short_title||d.id)||'source';let slug=base;if(bySlug[slug])slug=base+'-source';let n=2;while(bySlug[slug])slug=base+'-source-'+n++;
  g.srcSlug=slug;g.touchesRaw=Array.isArray(r.data.touches)?r.data.touches.slice(0,12):[];
  const links=uniq([...f.text.matchAll(/\[\[([^\]|#]+)/g)].map(m=>m[1].trim())).filter(s=>bySlug[s]);
  const title=(d.short_title||d.title)+' ('+citeAs(d)+')',one=String(r.data.one_liner||'').trim();
  const fm={title,type:'source',tags:uniq(g.touchesRaw.map(x=>String(x&&x.slug||'')).filter(s=>bySlug[s])).slice(0,8),register:docReg(d.id).slice(),status:'draft',updated:today(),links,sources:[d.id]};
  const bodyTxt=/^#\s/.test(f.text.trim())?f.text.trim():'# '+title+'\n\n'+f.text.trim();
  g.src={slug,title,type:'source',kind:'new',role:'source',stub:false,after:'<<ins>>\n'+bodyTxt+'\n<<end>>\n',paras:blocks(bodyTxt),ok:f.ok,removed:f.removed,notes:[],oneLiner:one,con:null,fm};
  g.cards=[g.src];g.touched=planTouched(g);g.drafted=0;g.prog='';renderIngest();
}
function planTouched(g){
  const vt=g.tk.filter(t=>t.ok),map={};
  vt.forEach(t=>t.slugs.forEach(s=>{(map[s]=map[s]||[]).push(t);}));
  g.touchesRaw.forEach(x=>{const s=String(x&&x.slug||'').trim();if(!s||s===g.srcSlug)return;
    if(bySlug[s]||g.newOK.has(s)){map[s]=map[s]||[];}
    else if(/^[a-z0-9][a-z0-9-]*$/.test(s)&&g.newOK.size<2){g.newOK.add(s);map[s]=[];}});
  const stub=pages.find(p=>p.frontmatter.status==='stub'&&(p.slug===slugify(g.doc.symbol||g.doc.id)||(p.frontmatter.sources||[]).includes(g.doc.id)))||pages.find(p=>p.frontmatter.status==='stub');
  const sl=stub?stub.slug:null;
  const rest=Object.keys(map).filter(s=>s!==sl).sort((a,b)=>map[b].length-map[a].length).slice(0,sl?11:12);
  return (sl?[sl]:[]).concat(rest).map(s=>({slug:s,isNew:!bySlug[s],stub:s===sl,mode:(!bySlug[s]||s===sl)?'body':'edits',tks:s===sl?vt:map[s]}));
}
function touchPrompt(g,t){
  const d=g.doc,p=bySlug[t.slug],tl=t.tks.map((x,i)=>(i+1)+'. '+x.claim+'\n   pin: '+x.pin).join('\n')||'(none: use the document’s title and register only)';
  let h='You are updating a research wiki on neurotechnology in the administration of justice after reading a new document: '+d.title+' ('+citeAs(d)+', '+d.year+', register '+regTxt(d.id)+').\n'+PINRULE+' Use only the pins listed below, copied exactly.\n'+REGRULE+'\n\n';
  if(t.mode==='edits')h+='PAGE '+t.slug+' (current body)\n'+p.body+'\n\nNEW TAKEAWAYS BEARING ON THIS PAGE\n'+tl+'\n\nReturn JSON {"edits":[{"after":"<an existing heading of this page, or end>","markdown":"..."}],"contested":null}. At most 300 words in all. "contested" is a full block (lines claim:, verdict:, note:, then one line per position: + or - or ~, a register letter, a pin, a gloss and a [[slug]], separated by " | ") only where this document disagrees with the page; otherwise null.';
  else if(t.stub)h+='STUB PAGE '+t.slug+' (current body, with the checklist of what the ingest should check)\n'+p.body+'\n\nTAKEAWAYS FROM THE DOCUMENT\n'+tl+'\n\nRewrite this page as a proper entity page for the document: answer each checklist item the document addresses, say plainly which items it does not address, keep every existing pin that still applies (copied exactly) and use the pins above. Return JSON {"one_liner":"...","body":"markdown starting with # title, at most 600 words"}.';
  else h+='NEW PAGE '+t.slug+'\n\nTAKEAWAYS\n'+tl+'\n\nWrite a new wiki page with this slug. Return JSON {"title":"...","type":"concept or entity","one_liner":"...","body":"markdown starting with # title, at most 400 words"}.';
  return h;
}
function buildCard(g,t,data){
  const p=bySlug[t.slug],id=g.doc.id,notes=[];let ok=0,removed=0,paras=0,after,con=null;
  const one=String(data.one_liner||'').trim();
  if(t.mode==='edits'){
    after=p.body;let words=0;
    (Array.isArray(data.edits)?data.edits:[]).forEach(e=>{
      const m0=String(e&&e.markdown||'').trim();if(!m0)return;
      words+=m0.split(/\s+/).length;if(words>400){notes.push('An edit beyond the word limit was dropped.');return;}
      const f=fixPins(m0,id);ok+=f.ok;removed+=f.removed;paras+=blocks(f.text);
      const r=insertAfter(after,String(e.after||'end'),f.text);after=r.body;if(r.note)notes.push(r.note);});
    const c=cleanCon(data.contested,id);
    if(c){ok+=c.ok;removed+=c.removed;con=c.text;paras+=1;
      const blockTxt=FENCE+'contested\n'+c.text+'\n'+FENCE;
      after=after.replace(/\s+$/,'')+'\n\n<<ins>>\n'+(/^#{1,4}\s.*contested/im.test(after)?'':'## Contested claims\n\n')+blockTxt+'\n<<end>>\n';}
    if(!paras)return null;
    return {slug:t.slug,title:p.title,type:p.type,kind:'edited',stub:false,after,paras,ok,removed,notes,oneLiner:one,con};
  }
  const f=fixPins(String(data.body||''),id);ok=f.ok;removed=f.removed;
  if(!f.text.trim())return null;
  const title=p?p.title:String(data.title||'').trim()||humanise(t.slug),type=p?p.type:(data.type==='entity'?'entity':'concept');
  const bt=/^#\s/.test(f.text.trim())?f.text.trim():'# '+title+'\n\n'+f.text.trim();
  const fm=p?null:{title,type,tags:[],register:docReg(id).slice(),status:'draft',updated:today(),links:[],sources:[id]};
  return {slug:t.slug,title,type,kind:p?'edited':'new',stub:!!t.stub,after:'<<ins>>\n'+bt+'\n<<end>>\n',paras:blocks(bt),ok,removed,notes,oneLiner:one,con:null,fm};
}
async function draftPages(){
  const g=ing;g.err=null;const run={stop:false};g.run=run;setRunning(3,true);
  for(let k=g.drafted;k<g.touched.length&&!run.stop;k++){
    const t=g.touched[k];g.prog='page '+(k+1)+' of '+g.touched.length+': '+t.slug;renderIngest();
    const r=await callModel(touchPrompt(g,t),0,'page '+(k+1)+' of '+g.touched.length+' ('+t.slug+')');
    if(run.stop)return;
    if(!r.ok){g.err={raw:r.raw||r.error,retry:'pages'};break;}
    const c=buildCard(g,t,r.data);if(c)g.cards.push(c);else g.skipped.push(t.slug);
    g.drafted=k+1;
  }
  g.run=null;setRunning(3,false);g.prog=g.err?'':(g.drafted>=g.touched.length?'All page drafts have returned.':'');renderIngest();
}
function decide(v){const g=ing,c=g.cards[g.i];if(!c)return;g.dec[c.slug]=v;g.i++;renderIngest();}
function secOf(t){return SEC[t]||'Other';}
function fileIngest(){
  const g=ing,d=g.doc,t=today(),before=needLook();
  const ap=g.cards.filter(c=>g.dec[c.slug]==='approve'),rj=g.cards.filter(c=>g.dec[c.slug]==='reject');
  if(!ap.length)return;
  const cite=citeAs(d),srcCard=ap.find(c=>c.role==='source');
  d.status='ingested';
  ap.forEach(c=>{
    const cl=cleanMk(c.after);let p=bySlug[c.slug];
    if(p){p.body=cl;if(c.stub)p.frontmatter.status='draft';}
    else{p={slug:c.slug,type:c.type,title:c.title,frontmatter:c.fm,body:cl};pages.push(p);bySlug[p.slug]=p;}
  });
  rebuild();
  ap.forEach(c=>{
    const p=bySlug[c.slug],fm=p.frontmatter,ids=uniq(p._pins.map(x=>x.id));
    fm.updated=t;fm.sources=uniq((fm.sources||[]).filter(s=>ids.includes(s)).concat(ids));
    fm.links=uniq((fm.links||[]).concat(p._links.filter(s=>bySlug[s]&&s!==p.slug)));
    if(srcCard)fm.links=uniq(fm.links.concat(c.role==='source'?ap.filter(x=>x!==c).map(x=>x.slug):[srcCard.slug]));
  });
  rebuild();
  ap.forEach(c=>{
    const p=bySlug[c.slug],n=vcount(p),line='- [['+p.slug+']] — '+(c.oneLiner||p.title)+' · ('+(p.frontmatter.register||[]).join('')+') · ✓'+n;
    if(c.kind==='new')addIndexLine(secOf(p.type),line);else if(c.stub)setIndexLine(p.slug,line);else setIndexN(p.slug,n);
  });
  fixIndexHead();
  const pinsAll=sum(pages,p=>p._pins.filter(x=>x.id===d.id).length),srcSlug=srcCard?srcCard.slug:'';
  const others=pages.filter(p=>p.slug!==srcSlug&&p._pins.some(x=>x.id===d.id)).map(p=>'[['+p.slug+']]');
  const head='## ['+t+'] ingest | '+(d.symbol?d.symbol+': ':'')+d.short_title;
  const bodyTxt='Read '+g.sent+' passages ('+cite+', register '+regTxt(d.id)+'). Wrote '+(srcCard?'[['+srcCard.slug+']]':'no source page')+'. '+pinsAll+' pins in all; besides its own page, pinned on '+others.length+' pages: '+(others.join(', ')||'none')+'. Rejected: '+(rj.map(c=>'[['+c.slug+']]').join(', ')||'none')+'.';
  log=log.replace(/\s+$/,'')+'\n\n'+head+'\n\n'+bodyTxt+'\n';S.logAdded.add(head);
  ap.forEach(c=>{
    if(!c.con)return;
    const cc=parseCon(c.con),slug=slugify(cc.claim).slice(0,60)||c.slug+'-claim',st=/^leans-/.test(cc.verdict)?'leaning':/^settled-/.test(cc.verdict)?'settled':'open';
    const gl=sg=>cc.pos.filter(x=>x.sign===sg).map(x=>x.gloss.trim()).join('; ')||'none';
    tensions=tensions.replace(/\s+$/,'')+'\n\n### '+slug+'\n\n- title: '+cc.claim+'\n- status: '+st+'\n- card: [['+c.slug+']]\n- poles: '+gl('+')+' — against: '+gl('-')+'\n- where: '+cc.pos.map(x=>(x.pin.match(/^\[([^\]]+)\]/)||[])[1]||'').filter(Boolean).join('; ')+'\n';
    S.tensAdded.add('### '+slug);
  });
  ap.forEach(c=>{S.changes.push({date:t,kind:'ingest',slug:c.slug,how:c.kind==='new'?'new page':'edited'});S.approved.add(c.slug);});
  S.filings++;lintRan=true;
  const after=needLook();lastFiling={before,after,slugs:ap.map(c=>c.slug)};
  g.filed={ap:ap.length,rj:rj.length,before,after,head,bodyTxt};
  renderAll();
}
function renderIngest(){
  const el=$('#ingOut'),g=ing;let h='';
  const inboxList=()=>{const ds=inboxDocs();return ds.length?ds.map(d=>'<div class="inb"><div><b>'+esc(d.short_title||d.title)+'</b><div class="hint">'+esc(d.symbol||d.author||'')+' · '+esc(d.kind)+' · '+esc(d.year)+' · '+(d.passages||[]).length+' passages · '+esc(d.pages)+' PDF pages · status: inbox</div></div><button type="button" class="btn pri" data-act="ing-open" data-id="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+'</button></div>').join(''):'<p>Nothing waits in the inbox.</p>';};
  if(!g){el.innerHTML='<div class="grey">Pressing the button opens a four-step plan. Nothing leaves the browser until you press Start, and every step says what it sends.</div>'+inboxList();return;}
  const steps=['01 SCOPE','02 TAKEAWAYS','03 DRAFTS','04 REVIEW AND FILE'];
  h+='<ol class="steps" aria-label="Steps">'+steps.map((s,i)=>'<li'+(g.stage===i+1?' class="on" aria-current="step"':'')+'>'+s+'</li>').join('')+'</ol>';
  h+='<div class="nums"><div><span class="big">'+(S.calls-g.c0)+'</span><div class="hint">calls so far</div></div><div><span class="big">'+(S.passages-g.p0)+'</span><div class="hint">passages sent</div></div></div><div class="hint" aria-live="polite">calls so far '+(S.calls-g.c0)+' · passages sent '+(S.passages-g.p0)+(g.prog?' · '+esc(g.prog):'')+'</div>';
  if(g.run)h+='<div class="row2"><button type="button" class="btn" data-act="ing-stop">Stop</button><span class="hint">Escape also stops. What has returned is kept.</span></div>';
  if(g.err)h+=errHtml(g.err,'ing-retry');
  const vt=g.tk.filter(t=>t.ok),n=g.doc.passages.length;
  if(g.stage===1){
    h+='<h3 class="s">Scope: the whole document</h3><p>All '+n+' passages will be sent, in batches of 25 ('+g.batches.length+' calls), '+nf(sum(g.batches,b=>b.chars))+' characters; nothing is held back.</p>'
     +'<table><caption>Batches</caption><thead><tr><th scope="col">Batch</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th><th scope="col" class="n">Passages</th><th scope="col" class="n">Characters</th></tr></thead><tbody>'+g.batches.map(b=>'<tr><td>'+b.n+'</td><td>'+esc(b.para)+'</td><td>'+esc(b.pp)+'</td><td class="n">'+b.passages.length+'</td><td class="n">'+nf(b.chars)+'</td></tr>').join('')+'</tbody></table>'
     +'<p><button type="button" class="btn pri" data-act="ing-start">Start</button> <span class="hint">sends '+g.batches.length+' calls, one after another, with the wiki’s index in each</span></p>';
  }else if(g.stage===2){
    h+='<h3 class="s">Takeaways</h3><table><caption>FIG.02 Takeaways from '+esc(g.doc.symbol||g.doc.short_title)+': '+vt.length+' verified of '+g.tk.length+'</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Pages it would touch</th><th scope="col">Verification</th></tr></thead><tbody>'
     +(g.tk.length?g.tk.map(t=>'<tr><td data-source="ai">'+esc(t.claim)+'</td><td data-source="ai">“'+esc(t.quote)+'”</td><td>'+(t.ps.paragraph?'para. '+esc(t.ps.paragraph)+' · ':'')+'PDF p. '+t.ps.page+'</td><td data-source="ai">'+(t.slugs.map(s=>'<span class="chip">'+esc(s)+(bySlug[s]?'':' (new)')+'</span>').join(' ')||'—')+'</td><td>'+(t.ok?'<span class="st ok">verified</span>':'<span class="st no">not verified</span>')+'</td></tr>').join(''):'<tr><td colspan="5" class="hint">No takeaway yet.</td></tr>')+'</tbody></table>'
     +'<p class="hint">How this is computed: each quote must stand in the passage the model named; the code builds the pin and runs the same check as everywhere else. '+g.dropped+' takeaways were dropped (no passage sent, or over 10 in a batch).</p>';
    const fl=g.tk.map((t,i)=>({t,i})).filter(x=>!x.t.ok);
    h+='<details'+(fl.length?' open':'')+'><summary><b>Could not verify: '+fl.length+'</b></summary>'+(fl.length?fl.map(({t,i})=>'<div class="err"><p data-source="ai"><b>'+esc(t.claim)+'</b><br>Model’s quote: “'+esc(t.quote)+'”</p><p class="hint">Passage named: '+(t.ps.paragraph?'para. '+esc(t.ps.paragraph)+', ':'')+'PDF p. '+t.ps.page+' · nearest passage on that page: '+(t.near.p.paragraph?'para. '+esc(t.near.p.paragraph):'p. '+esc(t.near.p.page_label))+', sharing a run of '+t.near.run+' words</p><button type="button" class="btn" data-act="ing-open-tk" data-i="'+i+'" aria-label="Open '+esc(g.doc.symbol||g.doc.short_title)+' at PDF page '+t.ps.page+'">Open the PDF page</button></div>').join(''):'<p class="hint">None so far. These claims would be in no change card and in no later prompt.</p>')+'</details>';
    if(!g.run){
      const left=g.batches.length-g.next;
      h+='<div class="row2">'+(left?'<button type="button" class="btn'+(vt.length?'':' pri')+'" data-act="ing-start">Run the remaining '+left+' batches</button>':'')+(vt.length?'<button type="button" class="btn pri" data-act="ing-go3">Go to the drafts</button>':'<span class="hint">No verified takeaway yet, so there is nothing to draft.</span>')+'</div>';
    }
  }else if(g.stage===3){
    h+='<h3 class="s">Drafts</h3>';
    if(!g.src){
      const ch=sum(vt,t=>t.claim.length+t.pin.length)+index.length;
      h+='<div class="grey">Sends '+vt.length+' verified takeaways (claims and pins, no passages) and the index: about '+nf(ch)+' characters, 1 call.</div>'+(g.run?'':'<button type="button" class="btn pri" data-act="ing-src">Draft the source page (1 call)</button>');
    }else{
      const c=g.src;
      h+='<p>Source page drafted: <b data-source="ai">'+esc(c.title)+'</b> <span class="hint">('+esc(c.slug)+') · '+c.paras+' paragraphs · pins: '+c.ok+' verified, '+c.removed+' removed because they did not verify</span></p><p data-source="ai">'+esc(c.oneLiner)+'</p>';
      if(g.drafted<g.touched.length&&!g.run){
        const left=g.touched.length-g.drafted;
        h+='<div class="grey">Pages to touch ('+g.touched.length+'): '+g.touched.map(t=>esc(t.slug)+(t.isNew?' (new)':'')+(t.stub?' (stub, rewritten)':'')).join(', ')+'. Each call sends the page’s body and the takeaways that bear on it; no passages.</div><button type="button" class="btn pri" data-act="ing-pages">'+(g.drafted?'Draft the remaining '+left+' pages':'Draft the changes to '+g.touched.length+' pages ('+g.touched.length+' calls)')+'</button>';
      }
      if(g.drafted>0&&!g.run)h+=' <button type="button" class="btn'+(g.drafted>=g.touched.length?' pri':'')+'" data-act="ing-review">Review the changes ('+g.cards.length+' pages)</button>';
      if(g.skipped.length)h+='<p class="hint">No change proposed for: '+esc(g.skipped.join(', '))+'.</p>';
    }
  }else{
    const c=g.cards[g.i],tot=g.cards.length;
    h+='<h3 class="s">Review and file</h3>';
    if(g.filed){
      h+='<div role="status"><p><b>Filed.</b> '+g.filed.ap+' pages written, '+g.filed.rj+' rejected. The index, the log and the tensions register were updated.</p><div class="nums"><div><span class="big">'+g.filed.before+'</span><div class="hint">lint checks needing a look, before</div></div><div><span class="big">'+g.filed.after+'</span><div class="hint">after (tab 04 shows which)</div></div></div><p class="hint">Log entry: '+esc(g.filed.head)+'</p></div>';
    }else if(c){
      h+='<fieldset class="chg"><legend>Change '+(g.i+1)+' of '+tot+' · '+esc(c.title)+' · '+esc(c.type)+'</legend><p class="mono">'+(c.kind==='new'?'new page':'edited')+' · '+c.paras+' paragraphs inserted · pins added: '+c.ok+' verified, '+c.removed+' removed because they did not verify</p>'
       +(c.notes.length?'<p class="hint">'+c.notes.map(esc).join(' ')+'</p>':'')+'<div class="prev dim">'+md(c.after,{allow:g.doc.id,slug:c.slug})+'</div>'
       +'<div class="row2"><button type="button" class="btn pri" data-act="ing-approve" aria-label="Approve change '+(g.i+1)+' of '+tot+': '+esc(c.title)+'">Approve this page</button><button type="button" class="btn" data-act="ing-reject" aria-label="Reject change '+(g.i+1)+' of '+tot+': '+esc(c.title)+'">Reject this page</button><span class="hint">change '+(g.i+1)+' of '+tot+' · nothing is written until you file</span></div></fieldset>';
    }else{
      const ap=g.cards.filter(x=>g.dec[x.slug]==='approve').length;
      h+='<p>'+tot+' decisions made: '+ap+' approved, '+(tot-ap)+' rejected. A rejected page stays exactly as loaded.</p><button type="button" class="btn pri" data-act="ing-file"'+(ap?'':' disabled')+'>File the approved changes</button>'+(ap?'':' <span class="hint">Disabled: no page was approved.</span>');
    }
  }
  if(g.filed)h+=inboxList();
  el.innerHTML=h;
}

/* ---------- tabs 04 and 05 ---------- */
function renderCheck(){
  const C=lintAll(),pins=sum(pages,p=>p._pins.length),ver=sum(pages,vcount),need=C.filter(c=>c.items.length).length;
  let h='<div><span class="big" aria-live="polite">'+nf(ver)+'</span> <span>of '+nf(pins)+' pins verified by this page</span></div><p><b>'+need+' lint checks need a look.</b> <span class="hint">How this is computed: a pin verifies when its quote stands in a passage of that document starting on that PDF page and the label names the paragraph or page label.</span></p>';
  h+='<table><caption>FIG.03 Lint checks on the wiki</caption><thead><tr><th scope="col">Check</th><th scope="col" class="n">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>'
   +C.map(c=>'<tr><td>'+esc(c.name)+'</td><td class="n"><span class="st '+(c.items.length?'no':'ok')+'">'+c.items.length+' · '+(c.items.length?'check':'pass')+'</span></td><td>'+(c.items.length?slugLinks(c.items):'—')+'</td></tr>').join('')+'</tbody></table>';
  h+='<p><button type="button" class="btn pri" data-act="lint">'+(lintRan?'Re-run':'Lint now')+'</button> <span class="hint">Contradictions between pages (the schema’s reading lint) are not checked by this page’s code.</span></p>';
  const R=selfChecks(),groups=uniq(R.map(r=>r.g));
  h+='<details open><summary><b>How the app checks itself</b></summary>'+groups.map(g=>'<h4 class="lab" style="margin:12px 0 2px">'+esc(g)+'</h4><ul style="list-style:none;padding:0;margin:0">'+R.filter(r=>r.g===g).map(r=>'<li style="padding:3px 0;border-bottom:1px solid var(--rule)"><span class="st '+(r.ok===null?'na':r.ok?'ok':'no')+'">'+(r.ok===null?'n/a':r.ok?'pass':'check')+'</span> '+esc(r.t)+(r.items.length?' · '+slugLinks(r.items,8):'')+'</li>').join('')+'</ul>').join('')+'</details>';
  $('#chkOut').innerHTML=h;
}
function renderRecord(){
  const ents=logEntries();if(logNewest)ents.reverse();
  const te=tensEntries();
  let h='<div class="row2"><span class="lab">LOG</span><button type="button" class="btn" data-act="log-order" aria-pressed="'+logNewest+'">'+(logNewest?'Newest first':'Oldest first')+'</button><span class="hint">click = switch order</span></div>';
  h+=ents.map(e=>'<details><summary>'+esc(e.title)+(S.logAdded.has(e.head)?'<span class="tag">this session</span>':'')+'</summary><div class="body">'+md(e.body,{})+'</div></details>').join('')||'<p class="hint">The log is empty.</p>';
  h+='<h3 class="s">Where the sources disagree: the tensions register</h3>'+(te.intro.trim()?'<div class="body">'+md(te.intro,{})+'</div>':'')
   +te.items.map(x=>'<details id="tens-'+slugify(x.head)+'"><summary>'+esc(x.head)+(S.tensAdded.has('### '+x.head)?'<span class="tag">this session</span>':'')+'</summary><div class="body">'+md(x.body,{})+'</div></details>').join('');
  h+='<h3 class="s">Method</h3><p class="hint">Counting, matching and verification are done by this page’s code; each number has its “How this is computed” line. Source: '+esc(WK.source||'the attached wiki')+' · built '+esc(WK.built||'unknown')+' · library: '+esc((WD.library&&WD.library.source)||'the attached library')+'.</p>';
  h+='<div class="row2"><button type="button" class="btn pri" data-act="download">Download the wiki</button>'+(S.changes.length?'<button type="button" class="btn" data-act="download-md">Download the changed pages (markdown)</button>':'')+'<span id="dlMsg" class="hint" aria-live="polite"></span></div>';
  $('#recOut').innerHTML=h;
}
function download(name,text,type){
  try{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},500);}
  catch(e){const m=$('#dlMsg');if(m)m.textContent='Download is not available here: '+e.message;}
}
function copyBtn(b,text){
  const old=b.textContent,done=ok=>{b.textContent=ok?'Copied':'Copy is not available here';setTimeout(()=>{b.textContent=old;},1600);};
  const fb=()=>{try{const a=document.createElement('textarea');a.value=text;a.style.cssText='position:fixed;opacity:0';document.body.appendChild(a);a.select();const ok=document.execCommand('copy');a.remove();return ok;}catch(e){return false;}};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(()=>done(true),()=>done(fb()));else done(fb());
}
function renderAll(){renderHead();renderList();renderPageView();renderAsk();renderIngest();renderCheck();renderRecord();}

/* ---------- events ---------- */
function openPin(i){const p=pinReg[i];if(!p)return;try{if(window.studio&&typeof studio.openSource==='function')studio.openSource(p.id,p.page,p.quote);}catch(e){}}
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-act]');if(!b)return;const a=b.dataset.act;
  const F={
   'open-page':()=>{e.preventDefault();openPage(b.dataset.slug);},
   'open-tens':()=>{e.preventDefault();openTens(b.dataset.head);},
   'pin-open':()=>openPin(+b.dataset.pin),
   'pin-toggle':()=>{const d=b.parentElement.querySelector('.pd');d.hidden=!d.hidden;b.setAttribute('aria-expanded',String(!d.hidden));b.textContent=d.hidden?'▾':'▴';},
   'copy-page':()=>copyBtn(b,pageMarkdown(bySlug[curPage])),
   'ask':()=>ask.stage==='chosen'?askStep2():askStep1(),
   'ask-stop':stopAsk,
   'ask-retry1':askStep1,'ask-retry2':askStep2,
   'ask-change':()=>{ask.changing=!ask.changing;renderAsk();},
   'ask-file-open':()=>{ask.file=!ask.file;renderAsk();},
   'ask-file':fileQuestion,
   'ask-copy':()=>copyBtn(b,ask.answer.answer),
   'ing-open':()=>openIngest(b.dataset.id),
   'ing-start':runBatches,'ing-stop':stopIngest,
   'ing-go3':()=>{ing.stage=3;renderIngest();},
   'ing-src':draftSource,'ing-pages':draftPages,
   'ing-review':()=>{ing.stage=4;ing.i=0;renderIngest();},
   'ing-approve':()=>decide('approve'),'ing-reject':()=>decide('reject'),
   'ing-file':fileIngest,
   'ing-retry':()=>{const r=ing.err&&ing.err.retry;if(r==='batch')runBatches();else if(r==='src')draftSource();else draftPages();},
   'ing-open-tk':()=>{const t=ing.tk[+b.dataset.i];try{if(window.studio&&studio.openSource)studio.openSource(ing.doc.id,t.ps.page,t.near.p.text.split(' ').slice(0,12).join(' '));}catch(err){}},
   'lint':()=>{lintRan=true;renderCheck();},
   'log-order':()=>{logNewest=!logNewest;renderRecord();},
   'download':()=>download('wiki-'+today()+'.json',JSON.stringify({title:WK.title,source:WK.source,built:WK.built,count:pages.length,schema:WK.schema,pages:pages.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.frontmatter,body:p.body})),index,log,tensions,changes:S.changes,library_status:Object.fromEntries(Object.values(docs).map(d=>[d.id,d.status]))},null,1),'application/json'),
   'download-md':()=>download('changed-pages-'+today()+'.md',pages.filter(p=>S.approved.has(p.slug)).map(pageMarkdown).join('\n\n'),'text/markdown')
  };
  if(F[a])F[a]();
});
document.addEventListener('input',e=>{
  if(e.target.id==='flt')renderList();
  else if(e.target.id==='fT'||e.target.id==='fG'){ask.fTitle=$('#fT').value;ask.fTags=$('#fG').value;updFile();}
});
document.addEventListener('change',e=>{
  const s=e.target.dataset&&e.target.dataset.pick;if(!s)return;
  let c=ask.chosen.filter(x=>x!==s);if(e.target.checked)c.push(s);
  if(c.length>5){e.target.checked=false;return;}
  ask.chosen=c;ask.answer=null;ask.file=null;ask.err=null;ask.stage=c.length?'chosen':'idle';ask.prog=c.length?'Pages changed by you. Press the button to send them.':'';renderAsk();
});
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){if(ask.run)stopAsk();if(ing&&ing.run)stopIngest();}
  if(e.target.id==='askQ'&&e.key==='Enter'&&!e.shiftKey){e.preventDefault();if(!ask.run)(ask.stage==='chosen'?askStep2:askStep1)();}
});
window.addEventListener('hashchange',()=>{let s='';try{s=decodeURIComponent(location.hash.slice(1));}catch(e){}if(s!==curPage){curPage=bySlug[s]?s:'';showTab(0);renderList();renderPageView();}});

/* ---------- start ---------- */
(function init(){
  pages=(WK.pages||[]).map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:JSON.parse(JSON.stringify(p.frontmatter||{})),body:p.body||''}));
  pages.forEach(p=>{orig[p.slug]=p.body;});
  LIBR.forEach(d=>{docs[d.id]=Object.assign({},d);});
  rebuild();loadedWarn=sum(pages,p=>p._pins.filter(x=>x.mark==='⚠').length);
  const tl=$('#tabs');
  tl.innerHTML=BASE.map((t,i)=>'<button type="button" class="tab" role="tab" id="t'+(i+1)+'" aria-controls="p'+(i+1)+'" data-tab="'+i+'">'+t+'<span class="run" aria-live="polite"></span></button>').join('');
  tl.querySelectorAll('.tab').forEach((b,i)=>{
    b.addEventListener('click',()=>showTab(i));
    b.addEventListener('keydown',e=>{const n=BASE.length;let k=null;if(e.key==='ArrowRight')k=(i+1)%n;else if(e.key==='ArrowLeft')k=(i+n-1)%n;else if(e.key==='Home')k=0;else if(e.key==='End')k=n-1;if(k!==null){e.preventDefault();showTab(k,true);}});
  });
  $('#foot').textContent=(WK.source||'')+' · built '+(WK.built||'unknown')+' · Counting, matching and verification are done by this page’s code; the model is called only when you press Ask, Ingest or a retry button.';
  if(!pages.length){$('#pview').innerHTML='<p>No wiki is attached to this conversation. Drag the wiki file from “Your files” into the chat.</p>';}
  try{const s=decodeURIComponent(location.hash.slice(1));if(bySlug[s])curPage=s;}catch(e){}
  renderAll();showTab(0,true);
})();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a tab "MAP" that draws the wiki as a graph: one node per page, coloured by its type (source, concept, entity, question), and one line for each [[link]] between two pages. Size each node by the number of pages that link to it. Draw it in plain SVG with a fixed layout computed by the code (no random start), so the map looks the same every time. Hovering a node shows its title and how many links go in and out; clicking it highlights its neighbours and offers "Open this page", which shows the page on the pages tab. Under the map, one line: how many pages and links, and the pages no other page links to (orphans), each clickable. Keep everything else as it is.

(Attached: Research wiki: neurotechnology and justice → WORKSHOP_DATA.wiki, with WORKSHOP_DATA.library)
