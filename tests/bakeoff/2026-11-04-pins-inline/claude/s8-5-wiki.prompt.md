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
- If you hide elements with the `hidden` attribute, add `[hidden]{display:none!important}` to the CSS: a rule that sets `display` on the element overrides `hidden` and shows it.
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
quote") ✓` gives a label, the library id, the PDF page, the quote, and ✓ (verified) or ⚠ (unverified).
A pin is a quotation inside the sentence: the prose is written around it ("The central ask [pin] ✓, stated also
in the summary [pin] ✓"), so show the quote itself, in quotation marks, where the pin stands, followed by the
label as a small citation; a pin shown as its label alone leaves the sentence without its words.
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
- **Pins.** A pin is part of its sentence: the page's prose is written around the quotation ("The central ask [pin] ✓, stated also in the summary [pin] ✓"), so the app shows the quote itself, in quotation marks, where the pin stands, and after it a small chip: the label as a button that calls `studio.openSource(id, page, quote)` with the pin's quote, so the studio opens the PDF at that page beside the app with the quoted passage marked; the document's register letter; and the verification the code computed, "✓ verified" in green or "⚠ not found" in amber, in words as well as colour. Where that differs from the mark written in the page, the chip adds "page says ✓" or "page says ⚠". An arrow expands the chip in place: the matching passage's `paragraph` or `page_label` and its first 300 characters, and "Open the PDF page". Never show a pin as its label alone: the sentence would lose its words.
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
