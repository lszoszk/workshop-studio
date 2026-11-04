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

## `WORKSHOP_DATA.pdf_text_2`: a second UN document as raw text from its PDF

The same shape as `pdf_text`: the 18 pages of CCPR/C/GC/32 as the same converter produced them,
with its own `reference` (65 paragraphs, 128 footnotes).

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
 "pdf_text_2": [
  {
   "page": 1,
   "text": "CCPR\n\nUNITED\nNATIONS\n\nInternational covenant\non civil and\npolitical rights\n\nDistr.\nGENERAL\nCCPR/C/GC/32\n23 August 2007\nOriginal: ENGLISH\n\nHUMAN RIGHTS COMMITTEE\nNinetieth session\nGeneva, 9 to 27 July 2007\nGeneral Comment No. 32\nArticle 14: Right to equality before courts and tribunals and to a fair trial\n\nI. GENERAL REMARKS\n1.\n\nThis general comment replaces general comment No. 13 (twenty-first session).\n\n2.\nThe right to equality before the courts and tribunals and to a fair trial is a key element\nof human rights protection and serves as a procedural means to safeguard the rule of law. Article\n14 of the Covenant aims at ensuring the proper administration of justice, and to this end\nguarantees a series of specific rights.\n3.\nArticle 14 is of a particularly complex nature, combining various guarantees with\ndifferent scopes of application. The first sentence of paragraph 1 sets out a general guarantee of\nequality before courts and tribunals that applies regardless of the nature of proceedings before\nsuch bodies. The second sentence of the same paragraph entitles individuals to a fair and public\nhearing by a competent, independent and impartial tribunal established by law, if they face \n[… rest of the page omitted in this sample]"
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

# Paragraphs out of a PDF: the numbered paragraphs of a General Comment, checked against the reference

## Context

The user works in an office that quotes UN documents: a national human rights institution, an NGO or a mission in Geneva. To cite a General Comment they open the PDF, copy the paragraph by hand, remove the footnote numbers and page headers that come with it, and type the citation. A PDF converter copies in a second but damages the text in four ways: it reorders (a footnote number lands at the foot of the page), breaks (a paragraph across two pages), loses (the number of footnote 6) and adds noise (headers, footers, date stamps). This app turns the converter's raw text of one document, `WORKSHOP_DATA.pdf_text`, into numbered paragraphs, compares the result with the document's own reference, and shows every repair it made. The pages are `records` (`page`, `text`); the yardstick is `reference` (`paragraphs`, `footnotes`, `adopted`, `first_words`); `title`, `symbol` and `doc_url` describe the document. Nothing is typed in by hand.

## What I found in the data

The numbers come from the file I examined; the app computes its own from the file it is given.

- 20 pages, `text` filled on every page, 2,800 to 4,300 characters each; `count` is the string "20". `reference.paragraphs` is 90, `reference.footnotes` 141; `reference.first_words` is keyed by the paragraph number as a string.
- **Header.** The first line of every page is the document symbol.
- **Footer.** The last lines of a page are, in varying order, the page number alone on a line (pages 2 to 20) and the job code "GE.25-15926"; page 1 has "GE.25-15926 (E)" and a date stamp "051125 061125" instead. On 12 pages a third bare number sits in the footer: a footnote number the converter displaced (6, 14, 45, 51, 67, 76, 87, 96, 101, 115, 118, 131); that footnote's text on the page has no number.
- **Paragraph numbers.** 88 of 90 stand alone on their line ("1." then the text on the next line); 2 (paragraphs 23 and 87) share the line with their text. A rule for one form alone misses the other.
- **Headings.** Roman-numbered sections ("I.", a blank line, "Introduction") and lettered subsections ("A.") whose title can wrap over two lines; and 23 unlabelled headings ("Right to work (art. 6)", "Children") on the line just before a paragraph number, so a naive split glues them to the previous paragraph.
- **Footnotes.** Each page's footnotes sit at the foot, before the footer. The first on a page is a bare number on its own line, a blank line, then the text; the others are "7 E/2003/22…". 129 start with their number; 12 lost it (the displaced numbers above). On each of those 12 pages the footnote without a number is the **second** on the page: it follows the first footnote's text directly, with no number and no blank line (page 2: "5", a blank line, "A/79/270, paras. 84 and 85.", then "A/42/427, p. 24." is footnote 6). In all 12 cases the first footnote is one line ending with a full stop. A parser that only follows the numbers glues the two together, then waits for a number that never comes and loses every footnote after it: on 3 Nov a build found 5 of 141 and left the footnote blocks of 16 pages inside paragraphs. The cover's asterisked note, "* Adopted by the Committee…", is not one of the 141.
- **Footnote marks in the text.** 141 marks, glued to the word before ("waste.2"), after a space ("”. 3") or after a comma ("equity, 17 common"); real numbers such as "article 11" look the same, so only a sequential rule tells them apart.
- 19 paragraphs span a page break; paragraphs are 43 to 254 words of plain prose, no lettered sub-paragraphs, no line ending in a hyphen; curly quotes and en dashes occur, so comparisons normalise them.

## The app, tab by tab

The same arrangement as the workshop's Verbatim finder, so participants who used one find their way in the other: a header, a rail on the left, four numbered tabs on the right.

**Header, always visible.** A monospace label "UN DOCUMENT · PDF TEXT", the serif title `title`, one line: `symbol` linked to `doc_url` (new tab), "adopted `reference.adopted`", "n pages of raw converter text", `source`. One sentence under it says what the page does: splits, removes headers, footers and footnotes, checks itself, lists every repair. At the right a green dot and "n of m checks pass", or a red dot and "n checks failed" (and a red dot on tab 04). The footer line (last item below) is also always visible.

**Left rail, always visible.** Headed "DOCUMENT". A card for the document: its `symbol` in monospace, its short title, "adopted …", "n pages". Under it two big serif numbers, "n paragraphs" and "n footnotes" as found, each with "of `reference.paragraphs`" or "of `reference.footnotes`" in the reference and a thin bar showing the share found (red when short or over), then "n of m checks pass", linking to tab 04. The app is written so that every document in `WORKSHOP_DATA` with `records` and a `reference` gets its own card in the rail, in the order of the data; the selected card has a red left border and the tabs show that document. Today there is one.

Under the header, numbered tabs (`role="tablist"`, arrow keys): `01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD`.

**01 RESULT. Did the app find everything the document has?** Four tiles with big serif numbers, each with a one-line "How this is computed" note: **Paragraphs found: n** next to **The document has: `reference.paragraphs`** (green when equal, red with the difference); **Footnotes found: n of `reference.footnotes`**; **First words match: n of `reference.paragraphs`**; **Repairs made: n**, a link to the repair log on tab 04. Five things to click: four tabs and the repair-log link.

**02 PARAGRAPHS. What does each paragraph say, and how do I cite it?** One row per paragraph: No. | Page | First line | Check: the number right-aligned, the page(s) it starts and ends on ("3–4" across a page break), the first 120 characters cut at a word with "…", and a Check cell reading "OK" or "first words differ" (red; the reference's words appear in the expanded row). A **Section** column, between No. and Page, shows the nearest heading above each paragraph ("Right to work (art. 6)"); the expanded paragraph shows the full path ("IV. … › Right to work (art. 6)"). A collapsible "Headings found: n" box above the table lists them, so the reader can see that none was swallowed into a paragraph. Footnote marks inside the text are shown in square brackets, "waste.[2]", in the table, the expanded paragraph and the CSV; a note under the table says so and gives the pattern `\[\d+\]` for removing them with find-and-replace. Rows are buttons with `aria-expanded`; clicking or pressing Enter expands the row in place, under it.

Under the row, the full text, verbatim as computed, never shortened. The expanded paragraph is one block of running text; a "Show the PDF's lines" toggle under it reveals the same text with the converter's line breaks and the page number where each page began, so the join can be checked. Under the text: the reference's first six words next to the extracted first six words, marked equal or different; the page(s); the repairs that touched this paragraph; and a **Copy citation** button that copies "`symbol`, para. n" (for example "E/C.12/GC/27, para. 12") and shows "Copied" for two seconds; the same string is the CSV's `citation` column.

**03 FOOTNOTES. What do the footnotes say?** A table, "Footnotes found: n of `reference.footnotes`", with columns No. | Page | Text | Repair, where Repair reads "number restored from the page foot" for a footnote whose number the converter displaced. The expanded paragraph also lists the footnotes it cites. A download button, "footnotes.csv", on this tab.

**04 CHECKS & METHOD. Can I trust this, and can I take it away?** The check panel (see "How the app checks itself"), open, every check on one line. Under it a closed heading "Repair log (n)", a button with `aria-expanded`, which the Repairs tile on tab 01 also opens: a table of every change the script made, in document order, Page | Paragraph or footnote | What was done | Before | After, with a count per kind above it. The kinds are the ones named in the next section: header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed. Then a closed heading "Raw pages", a button with `aria-expanded`: a select "Show raw page n" and a monospaced panel with the page's `text` as stored, line numbers on the left, each line coloured by what the script decided it was (cover, header, heading, paragraph, footnote, footer), with a legend. Then **Download**: "Download paragraphs as CSV", one row per paragraph with `number`, `section`, `part`, `page_start`, `page_end`, `first_words_reference`, `first_words_found`, `first_words_match`, `text`, `text_raw`, `footnotes_cited`, `repairs`, `citation`, `symbol`, `doc_url`; UTF-8 with a byte-order mark, every field double-quoted with inner quotes doubled, CRLF line ends, a Blob URL, file name from the symbol with slashes replaced by hyphens. Seven things to click: four tabs, the repair log and raw pages headings, and the download (the select appears once "Raw pages" is open).

**Footer, always visible.** Source line, `built` date, and "Counting, splitting and matching are done by this page's code; no model was called and nothing left the browser."

## How every number is computed

The pipeline runs once on load, in this order, over `records` sorted by `page`; each step logs what it removed or changed.

- **Header.** If a page's first non-empty line equals `symbol`, drop it and log "header line removed"; otherwise log a warning for that page.
- **Footer.** From the end of each page, drop lines while the line is empty, starts with "GE." (the job code), consists only of 6-digit groups (the date stamp), or is a bare number of one to three digits. A bare number equal to `page` is the page number; any other is a **displaced footnote number**, kept aside for that page.
- **Footnote block.** Keep a counter `nextFootnote`, starting at 1. On each page, after header and footer are gone, the block starts at the first line that is a bare number equal to `nextFootnote`, or starts with that number and a space, or starts with "* " on the first page; from there to the end of the page is footnotes, everything before is body. Advance `nextFootnote` past the highest number seen in the block and past any displaced number for that page. If no line on a page opens `nextFootnote`, take the first bare number greater than it that stands before the footer and log the jump; one missed number must never stop the count on the pages that follow. A page with no opener at all (none here) is all body, and the check panel says so.
- **Footnote text.** Inside each page's footnote block, a line that starts with a number and a space, or a bare number on its own line, opens a footnote; the lines up to the next opener are its text, joined with a space. Any line that starts with a number and a space opens a footnote, even when the number is not the one expected: never add a numbered line to the footnote before it. On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D, marked `repaired`. The cover's asterisked note is kept as footnote "*" and not counted.
- **Body lines of all pages are concatenated** in page order, each line tagged with its page; this joins the paragraphs that cross a page break (logged as "paragraph joined across a page break" when a paragraph's lines carry two page numbers).
- **Paragraph starts.** A line matching `/^(\d{1,3})\.$/` (number alone) or `/^(\d{1,3})\. (.+)$/` (number and text on one line; the text after the space is the first line, logged as "number and text split"). Lines before the first paragraph start are the cover.
- **Headings.** A line matching `/^([IVX]+|[A-Z])\.$/` opens a labelled heading: skip blank lines, then every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or "(" continues the previous heading line (logged as "heading title joined from two lines"), any other line is a further heading. An **unlabelled heading** is a non-empty line immediately followed by a paragraph-start line, at most 90 characters, starting with a capital letter and not ending with a full stop, semicolon, colon, comma or digit (logged as "heading separated from paragraph text"). Each paragraph's `section` is the most recent heading line before it and `part` the most recent roman-numbered heading; a heading line is never part of a paragraph's text.
- **Paragraph lines.** Every other non-empty body line belongs to the current paragraph; blank lines are dropped. `page_start` and `page_end` are the pages of its first and last line.
- **Paragraph text** = the paragraph's lines joined with a single space, double spaces collapsed, trimmed. No line in the file ends with a hyphen, so no hyphen joining is done; the app counts such lines anyway and reports the number. `text_lines` keeps the original lines for the toggle and the CSV column `text_lines` (lines separated by " | ").
- **Footnote marks in the text.** Only a sequential rule tells a mark from a real number such as "article 11". Walk through each paragraph's text in document order with a counter that starts at 1. Every run of one to three digits not touching another digit, a slash, a dash or an opening parenthesis is a candidate; a candidate equal to the counter is a mark and the counter goes up by one; any other number is left alone. Each mark becomes `[n]`, the character before it kept ("waste.[2]", "equity,[17] common"). `text_raw` keeps the unmodified text.
- **First words.** `first_words_found` = the first six whitespace-separated words of the joined text, footnote marks removed first; `first_words_reference` = `reference.first_words[String(number)]`. They match when equal after normalising curly quotes to straight, en and em dashes to a hyphen and runs of whitespace to one space; case is kept.
- **Citation** = `symbol` + ", para. " + the paragraph number, with `symbol` read from `WORKSHOP_DATA.pdf_text`, never typed in.
- **Counts** are loops over the records in JavaScript; nothing is estimated and no model is called.

## How the app checks itself

Each check is one line: what was compared, the two values, and "pass" in green or "check failed" in red with a link to the rows concerned. A failed check never hides a result; it marks it.

- **Paragraph count.** Paragraphs found against `reference.paragraphs`.
- **Numbering.** The paragraph numbers are exactly 1 to n in order; gaps and duplicates are listed by number and page.
- **First words.** Each paragraph's first six words against `reference.first_words`; the count of mismatches, each listed as "para. n: found … / reference …", with the row flagged in the table.
- **Footnotes.** Footnotes found (numbered openers plus restored numbers) against `reference.footnotes`; the numbers run from 1 to that count without a gap or a duplicate; the restored numbers are listed with their page as repairs.
- **Footnote marks.** Marks found in the paragraphs, expected to run from 1 to `reference.footnotes` without a gap; the check lists any missing numbers and the numbers it rejected as not being marks (with context), so the reader can see that "article 11" was not bracketed.
- **Footnotes stay out of the paragraphs.** The first 40 characters of every line that opens a footnote, its number included ("15 Human Rights Committee, general comm…"; for a footnote whose number was displaced, its first line), are searched in the raw text of every paragraph, before footnote marks are touched (expected 0 hits; continuation lines are not searched, because a citation such as "United Nations Framework Convention on Climate Change" also occurs in paragraph 6), and every paragraph over 300 words is listed (the longest real one has 254). A hit means a footnote block was read as body: the check fails, the paragraph is flagged in the table, and the "Paragraphs found" tile on tab 01 says "n contain footnotes" in red, even when the count is right.
- **Headers and footers.** Pages whose first line was the symbol (expected all); pages with a page number in the footer (expected all but the first); displaced footnote numbers, listed with their page.
- **Headings.** The number of labelled and unlabelled headings and the list of unlabelled ones, so a reader can spot a paragraph's last line mistaken for a heading.
- **Nothing lost.** Every non-empty line of every page is classified exactly once as cover, header, heading, paragraph, footnote or footer, and the counts per kind sum to the total non-empty lines in the file; any unclassified line is listed with its page and shown in red in the raw page viewer.

## Edge cases and risks

- A paragraph number on the same line as its text (2 of 90 here) and alone on its line (88) must both be accepted; handling one form only loses two paragraphs or finds none.
- "6 November 2025" on the cover starts with a number and a space; it is not a footnote because the counter is at 1 when it is met.
- The reference is a yardstick, not the truth: if the counts disagree, the app shows both and the difference, and never trims or pads its result to match.
- The first-words check sees six words; a paragraph can start correctly and be damaged later. The raw page viewer and the "Nothing lost" check cover the rest.
- If `reference` or one of its fields is missing, the tiles say "no reference in this file" and the checks that need it show "not run", never "pass".

## Design and accessibility

What this app adds to the studio look:

- **Red accent** on the active tab, the paragraph numbers in the first column, and the words "first words differ" and "check failed". "Pass" is dark green. Pass and fail are always words as well as colours.
- **Big serif numbers** only on the document card in the rail and the four tiles of tab 01, with paragraphs found beside the document's own count. Every table has a serif `<caption>` that states the message ("90 paragraphs found, 90 expected") and a monospace number (`TAB.01`).
- **Category colours** only in the raw page viewer: six pale tints (cover, header, heading, paragraph, footnote, footer), each doubled by a letter code in the margin and in the legend.
- Tables follow "Data visualisation: tables" (UK Government Analysis Function): `<th scope="col">`, numbers right-aligned, the source under the table, no footnotes inside data cells.
- The check panel follows "Quality assurance of code for analysis and research: Testing code" (Analysis Function): each check tells a story, given this data, having run this code, we expect this output; every repair has a named check.
- Explanations follow "GOV.UK content guidance: Clear language": short sentences; "footnote block", "footer" and "displaced number" explained the first time they appear.
- Citations follow the Dag Hammarskjöld Library's "How should I cite a UN document?": the symbol as the key, the paragraph as the pinpoint, the parts stored separately and formatted on copy.
- Keyboard: expandable rows and the repair log heading are buttons with `aria-expanded`; the tab panel of a hidden tab is not focusable.

## Out of scope

No model calls, no summaries, no OCR, no PDF rendering: the input is the converter's text. No lettered sub-paragraphs (none here), no editing in the browser, one document only.

## Sources consulted

- UK Government Analysis Function, Quality assurance of code for analysis and research: Testing code — https://github.com/best-practice-and-impact/qa-of-code-guidance/blob/fa39f2089905fe07c08ae4d66671736a1becd3c5/book/testing_code.md
- GOV.UK content guidance: Clear language (plain English) — https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- UK Government Analysis Function, Data visualisation: tables — https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/
- Dag Hammarskjöld Library, Ask DAG: how should I cite a UN document? — https://ask.un.org/faq/401380

(Attached: CESCR General comment No. 27 (PDF) → WORKSHOP_DATA.pdf_text)

# ASSISTANT MESSAGE (your earlier answer)

I built a four-tab app on the attached PDF text: it removes headers, footers and footnotes, splits the numbered paragraphs, compares them with the document's own reference and lists every repair. Tab 01 gives the answer at a glance, and tab 04 holds nine self-checks, the repair log, the raw pages and the CSV download. Nothing is typed in by hand and no model is called.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN document: paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--ok:#1d6a38;--muted:#5a554c;--tint:#faf7f0;
--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
[hidden]{display:none!important}
*{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
a{color:var(--accent)}
button{font:inherit;color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.wrap{max-width:1320px;margin:0 auto;padding:20px 24px 28px}
.mono{font:12px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase}
.hint,.how{font:12px/1.4 var(--mono);color:var(--muted)}
.muted{color:var(--muted)}
.pass{color:var(--ok);font-weight:700}
.fail{color:var(--accent);font-weight:700}
.top{border-bottom:1px solid var(--rule);padding-bottom:16px}
.head-row{display:flex;flex-wrap:wrap;gap:12px 32px;justify-content:space-between;align-items:flex-start}
.head-main{flex:1 1 560px;min-width:0}
h1{font:400 clamp(26px,3.2vw,38px)/1.15 var(--serif);margin:6px 0 8px}
.meta{margin:0 0 4px}
.lede{margin:0;color:var(--muted)}
.status{display:flex;align-items:center;gap:8px;font:12px/1.4 var(--mono);letter-spacing:.06em;text-transform:uppercase;padding-top:10px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--muted);flex:none}
.dot.ok{background:var(--ok)}
.dot.bad{background:var(--accent)}
.layout{display:grid;grid-template-columns:272px minmax(0,1fr);gap:32px;margin-top:20px}
.rail{border-right:1px solid var(--rule);padding-right:24px;align-self:start;position:sticky;top:12px}
.rh{margin:0 0 8px;font-weight:400;color:var(--muted)}
.card{display:block;width:100%;text-align:left;background:none;border:0;border-left:4px solid transparent;border-top:1px solid var(--rule);padding:8px 8px 8px 10px;cursor:pointer}
.card[aria-current="true"]{border-left-color:var(--accent)}
.card .sym{font:12px/1.4 var(--mono);letter-spacing:.04em;display:block}
.card .tt{display:block;font-family:var(--serif)}
.card .sub{display:block;color:var(--muted);font-size:14px}
.stat{border-top:1px solid var(--rule);padding:12px 0 8px}
.big{font:400 44px/1 var(--serif)}
.of{font:12px/1.4 var(--mono);color:var(--muted);margin:2px 0 6px}
.bar{height:4px;background:var(--rule)}
.bar i{display:block;height:100%;background:var(--ok)}
.bar.bad i{background:var(--accent)}
.lnk{background:none;border:0;padding:0;color:var(--accent);text-decoration:underline;cursor:pointer;font:inherit}
.tabs{display:flex;flex-wrap:wrap;gap:0 24px;border-bottom:1px solid var(--rule);margin-bottom:18px}
.tab{background:none;border:0;border-bottom:3px solid transparent;padding:10px 0 8px;font:12px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
.q{font:400 22px/1.25 var(--serif);margin:0 0 14px}
.answer{font:400 20px/1.35 var(--serif);margin:0 0 16px}
.tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px}
.tile{border-top:1px solid var(--rule);padding:14px 0 16px}
.num{font:400 52px/1 var(--serif)}
.num.pass,.num.fail{font-weight:400}
.pair{display:flex;gap:28px;align-items:flex-end;flex-wrap:wrap}
.tile .sub{margin:6px 0 4px}
.how{margin:6px 0 0}
.terms{border-top:1px solid var(--rule);margin-top:6px;padding-top:12px;color:var(--muted)}
.terms p{margin:0 0 4px}
table{border-collapse:collapse;width:100%}
caption{text-align:left;font:400 20px/1.3 var(--serif);padding:0 0 8px}
caption .mono{display:block;color:var(--muted);font-size:11px}
th{font:12px/1.4 var(--mono);letter-spacing:.06em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:8px;vertical-align:top;overflow-wrap:anywhere}
th.r,td.r{text-align:right}
.src{font-size:14px;color:var(--muted);margin:8px 0 0}
tr.prow{cursor:pointer}
tr.prow:hover{background:#ece6d9}
.pnum{background:none;border:0;padding:0 2px;cursor:pointer;color:var(--accent);font-weight:700;text-align:right}
.pnum::before{content:"\25B8\00a0";font-weight:400}
.pnum[aria-expanded="true"]::before{content:"\25BE\00a0"}
tr.detail td{background:var(--tint);border-left:3px solid var(--accent);padding:12px 16px}
.lab{color:var(--muted);margin:10px 0 2px}
.ptext{margin:0 0 8px;max-width:70ch}
.plines{font:13px/1.45 var(--mono);white-space:pre-wrap;overflow-wrap:anywhere;border:1px solid var(--rule);background:#fff;padding:8px;margin:6px 0}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0 24px}
.cols ul{margin:0;padding-left:18px}
.btn{background:var(--ink);color:var(--paper);border:0;padding:8px 14px;cursor:pointer;font:600 15px var(--sans)}
.btn.sm{padding:4px 10px;font-size:14px}
.disc{display:block;width:100%;text-align:left;background:none;border:0;border-top:1px solid var(--rule);padding:12px 0;font:400 20px/1.3 var(--serif);cursor:pointer}
.disc::before{content:"\25B8\00a0";color:var(--accent)}
.disc[aria-expanded="true"]::before{content:"\25BE\00a0"}
.box{padding:0 0 14px}
.checks{list-style:none;margin:0 0 20px;padding:0}
.checks li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 16px;border-top:1px solid var(--rule);padding:10px 0}
.checks .nm{font-weight:700}
.checks .det{grid-column:1/-1;font-size:15px;color:var(--ink);overflow-wrap:anywhere}
.h2{font:400 22px/1.25 var(--serif);margin:22px 0 6px}
.method{margin:0 0 18px;padding-left:22px;max-width:75ch}
.kinds{margin:0 0 10px;color:var(--muted);font-size:14px}
.rawbar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;margin:0 0 8px}
.legend{display:flex;flex-wrap:wrap;gap:6px 10px;margin:0 0 8px;font:12px/1.4 var(--mono)}
.chip{padding:2px 8px;border:1px solid var(--rule)}
.chip b{margin-right:4px}
.raw{font:13px/1.45 var(--mono);border:1px solid var(--rule);max-height:520px;overflow:auto}
.ln{display:grid;grid-template-columns:3em 1.6em minmax(0,1fr);gap:0 8px;padding:0 8px;white-space:pre-wrap;overflow-wrap:anywhere}
.ln .no{color:var(--muted);text-align:right}
.ln .cd{font-weight:700}
.k-cover{background:#e8e2f1}.k-header{background:#dde9f3}.k-heading{background:#f5e6bf}
.k-paragraph{background:#e4eed8}.k-footnote{background:#f2dcd4}.k-footer{background:#e0dfdc}
.k-unclassified{background:#fff;color:var(--accent);outline:2px solid var(--accent);outline-offset:-2px}
select{font:inherit;padding:4px 8px;border:1px solid var(--ink);background:#fff;color:var(--ink)}
.foot{border-top:1px solid var(--rule);margin-top:28px;padding-top:12px;color:var(--muted);font-size:14px}
.foot p{margin:0 0 2px}
code{font:13px var(--mono);background:#ebe5d8;padding:0 4px}
@media(max-width:900px){.layout{grid-template-columns:1fr}.rail{position:static;border-right:0;padding-right:0}.tiles{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
 <div class="mono muted">UN DOCUMENT · PDF TEXT</div>
 <div class="head-row">
  <div class="head-main">
   <h1 id="title">Paragraphs out of a PDF</h1>
   <p class="meta" id="meta"></p>
   <p class="lede">This page splits the converter's raw text into numbered paragraphs, removes headers, footers and footnotes, checks itself against the document's own numbers and lists every repair it made.</p>
  </div>
  <div class="status" id="status" role="status"></div>
 </div>
</header>
<div class="layout">
 <aside class="rail" aria-label="Document">
  <h2 class="mono rh">DOCUMENT</h2>
  <div id="cards"></div>
  <div id="stats"></div>
 </aside>
 <main id="main">
  <div class="tabs" id="tabs" role="tablist" aria-label="Views of the document">
   <button type="button" class="tab" role="tab" id="t1" data-act="tab" data-tab="1" aria-controls="p1" aria-selected="true">01 RESULT</button>
   <button type="button" class="tab" role="tab" id="t2" data-act="tab" data-tab="2" aria-controls="p2" aria-selected="false" tabindex="-1">02 PARAGRAPHS</button>
   <button type="button" class="tab" role="tab" id="t3" data-act="tab" data-tab="3" aria-controls="p3" aria-selected="false" tabindex="-1">03 FOOTNOTES</button>
   <button type="button" class="tab" role="tab" id="t4" data-act="tab" data-tab="4" aria-controls="p4" aria-selected="false" tabindex="-1">04 CHECKS &amp; METHOD<span class="dot bad" id="t4dot" hidden title="A check failed"></span></button>
  </div>
  <section role="tabpanel" id="p1" data-tab="1" aria-labelledby="t1" tabindex="0"></section>
  <section role="tabpanel" id="p2" data-tab="2" aria-labelledby="t2" hidden></section>
  <section role="tabpanel" id="p3" data-tab="3" aria-labelledby="t3" hidden></section>
  <section role="tabpanel" id="p4" data-tab="4" aria-labelledby="t4" hidden></section>
 </main>
</div>
<footer class="foot" id="foot"></footer>
</div>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{};
const $=(s,r)=>(r||document).querySelector(s);
const $$=(s,r)=>Array.from((r||document).querySelectorAll(s));
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=v=>{if(v==null||v==='')return null;const n=Number(v);return isFinite(n)?n:null;};
const cut=(s,n)=>{s=String(s||'');if(s.length<=n)return s;let c=s.slice(0,n);const i=c.lastIndexOf(' ');if(i>n*0.5)c=c.slice(0,i);return c.replace(/[\s,;:]+$/,'')+'…';};
const norm=s=>String(s==null?'':s).replace(/[“”„‟]/g,'"').replace(/[‘’‚‛]/g,"'").replace(/[–—‒−]/g,'-').replace(/\s+/g,' ').trim();
const safeUrl=u=>/^https?:\/\//i.test(String(u||''))?String(u):'';
const hfull=h=>((h.label?h.label+' ':'')+(h.text||'')).trim();
const pg=p=>p.pageStart===p.pageEnd?String(p.pageStart):p.pageStart+'–'+p.pageEnd;
const lst=(arr,limit,fn)=>arr.slice(0,limit).map(fn).join('; ')+(arr.length>limit?'; and '+(arr.length-limit)+' more':'');

const PS=/^(\d{1,3})\.(?:\s+(\S.*))?$/;
const LAB=/^([IVX]+|[A-Z])\.$/;
const FORBID='/-‐‑‒–—−(';
const KINDS=['header line removed','footer line removed','number and text split','paragraph joined across a page break','heading separated from paragraph text','heading title joined from two lines','footnote number restored','footnote block removed'];
const CODE={cover:'C',header:'H',heading:'T',paragraph:'P',footnote:'N',footer:'F',unclassified:'U',blank:''};

// A number equal to the running counter is a footnote mark; every other number is left alone.
function markText(raw,start){
  const out=[],marks=[],rejected=[];let last=0,counter=start,m;
  const re=/\d+/g;
  while((m=re.exec(raw))){
    if(m[0].length>3)continue;
    const s=m.index,e=s+m[0].length,pc=s>0?raw[s-1]:'',nc=e<raw.length?raw[e]:'';
    if((pc&&FORBID.indexOf(pc)>=0)||(nc&&FORBID.indexOf(nc)>=0))continue;
    const v=+m[0];
    if(v===counter){out.push(raw.slice(last,s).replace(/\s+$/,''),'['+v+']');last=e;marks.push(v);counter++;}
    else rejected.push({a:raw.slice(Math.max(0,s-26),s),n:m[0],b:raw.slice(e,e+26)});
  }
  out.push(raw.slice(last));
  return {text:out.join(''),marks:marks,counter:counter,rejected:rejected};
}

function analyse(doc){
  const symbol=String(doc.symbol||'').trim();
  const ref=doc.reference&&typeof doc.reference==='object'?doc.reference:null;
  const refP=ref?num(ref.paragraphs):null,refF=ref?num(ref.footnotes):null;
  const refFW=ref&&ref.first_words&&typeof ref.first_words==='object'?ref.first_words:null;
  const recs=(Array.isArray(doc.records)?doc.records:[]).filter(x=>x&&typeof x==='object').slice().sort((a,b)=>(num(a.page)||0)-(num(b.page)||0));
  const repairs=[],fns=[],body=[],pageInfo=[],notes=[];
  let nextFn=1,ord=0,coverNote=null;
  const rep=(kind,page,where,what,before,after,pos,para)=>repairs.push({kind:kind,page:page,where:where,what:what,before:before,after:after,pos:pos,para:para||null,ord:ord++});

  // ---- 1. page by page: header, footer, footnote block ----
  recs.forEach((rec,ri)=>{
    const page=num(rec.page)!=null?num(rec.page):ri+1;
    const L=String(rec.text==null?'':rec.text).split(/\r?\n/).map((raw,i)=>({page:page,n:i+1,raw:raw,t:raw.trim(),kind:null,pos:page*100000+i}));
    L.forEach(l=>{if(!l.t)l.kind='blank';});
    const info={page:page,header:false,pageNo:false,displaced:[],noBlock:false,lines:L};
    pageInfo.push(info);
    const firstL=L.find(l=>l.t);
    if(firstL&&symbol&&firstL.t===symbol){
      firstL.kind='header';info.header=true;
      rep('header line removed',page,'–','Removed the symbol line at the top of the page',firstL.t,'(removed)',firstL.pos);
    }else notes.push('Page '+page+': the first line is not the document symbol.');
    let end=L.length-1;
    for(;end>=0;end--){
      const l=L[end];
      if(l.kind==='header')break;
      if(!l.t)continue;
      let what='';
      if(/^GE\./.test(l.t))what='job code';
      else if(/^\d{6}(?:\s+\d{6})*$/.test(l.t))what='date stamp';
      else if(/^\d{1,3}$/.test(l.t)){
        const v=+l.t;
        if(v===page&&!info.pageNo){info.pageNo=true;what='page number';}
        else{info.displaced.push({num:v,line:l});what='displaced footnote number '+v;}
      }
      if(!what)break;
      l.kind='footer';
      rep('footer line removed',page,'–','Removed a footer line: '+what,l.t,'(removed)',l.pos);
    }
    const Z=[];
    for(let i=0;i<=end;i++){if(L[i].kind==null)Z.push(L[i]);}
    // footnote block: starts at the line that opens footnote number nextFn
    let bs=-1;
    const want=String(nextFn);
    for(let i=0;i<Z.length;i++){
      const t=Z[i].t;
      if(t===want||t.indexOf(want+' ')===0||(ri===0&&t.indexOf('* ')===0)){bs=i;break;}
    }
    if(bs<0){
      for(let i=0;i<Z.length;i++){
        if(/^\d{1,3}$/.test(Z[i].t)&&+Z[i].t>nextFn){bs=i;notes.push('Page '+page+': no footnote '+nextFn+' was found; the count jumped to '+(+Z[i].t)+'.');break;}
      }
    }
    if(bs<0){info.noBlock=true;notes.push('Page '+page+': no line opens a footnote, so the whole page is read as body text.');}
    const bodyZ=bs<0?Z:Z.slice(0,bs),blockZ=bs<0?[]:Z.slice(bs);
    // footnotes inside the block
    const list=[];let cur=null,m;
    blockZ.forEach(l=>{
      l.kind='footnote';
      if((m=/^(\d{1,3})$/.exec(l.t))){cur={num:+m[1],parts:[],open:l,bare:true,repaired:false};list.push(cur);}
      else if((m=/^(\d{1,3})\s+(\S.*)$/.exec(l.t))){cur={num:+m[1],parts:[{t:m[2],l:l}],open:l,bare:false,repaired:false};list.push(cur);}
      else if(ri===0&&/^\*\s/.test(l.t)){cur={num:'*',parts:[{t:l.t.replace(/^\*\s*/,''),l:l}],open:l,bare:false,repaired:false};list.push(cur);}
      else if(cur)cur.parts.push({t:l.t,l:l});
    });
    // a displaced number: the footnote that lost it follows the first one's text directly
    info.displaced.slice().sort((a,b)=>a.num-b.num).forEach(d=>{
      if(list.some(f=>f.num===d.num))return;
      let idx=-1;
      list.forEach((f,k)=>{if(typeof f.num==='number'&&f.num<d.num)idx=k;});
      if(idx<0){notes.push('Page '+page+': displaced number '+d.num+' has no footnote before it to split.');return;}
      const f=list[idx];let j=-1;
      for(let k=0;k<f.parts.length;k++){if(/\.$/.test(f.parts[k].t)){j=k;break;}}
      if(j<0||j>=f.parts.length-1){notes.push('Page '+page+': could not place the displaced number '+d.num+'.');return;}
      const tail=f.parts.splice(j+1);
      const nf={num:d.num,parts:tail,open:tail[0].l,bare:false,repaired:true};
      list.splice(idx+1,0,nf);
      const tx=tail.map(x=>x.t).join(' ');
      rep('footnote number restored',page,'footnote '+d.num,'The converter had moved the number to the foot of the page; it was given back to its footnote','(no number) '+cut(tx,70),d.num+' '+cut(tx,70),tail[0].l.pos);
    });
    let mx=nextFn-1,count=0;
    list.forEach(f=>{
      if(f.num==='*'){coverNote={page:page,text:f.parts.map(x=>x.t).join(' ')};return;}
      count++;if(f.num>mx)mx=f.num;
      const text=f.parts.map(x=>x.t).join(' ').replace(/\s+/g,' ').trim();
      let key=f.repaired?(f.parts[0]?f.parts[0].t:''):f.bare?f.num+' '+(f.parts[0]?f.parts[0].t:''):f.open.t;
      key=key.replace(/\s+/g,' ').trim().slice(0,40);
      fns.push({num:f.num,page:page,text:text,repaired:f.repaired,key:key});
    });
    info.displaced.forEach(d=>{if(d.num>mx)mx=d.num;});
    nextFn=mx+1;
    if(blockZ.length)rep('footnote block removed',page,'page '+page+' foot',plural(count,'footnote','footnotes')+(coverNote&&coverNote.page===page?' and the cover note':'')+' taken out of the page text (tab 03)',cut(blockZ[0].t,60),'(kept in the footnote table)',blockZ[0].pos);
    bodyZ.forEach(l=>body.push(l));
  });

  // ---- 2. body lines of all pages in order: headings and paragraphs ----
  const n=body.length;
  const isPS=body.map(l=>PS.test(l.t)),isLab=body.map(l=>LAB.test(l.t));
  const endsSentence=t=>/[.;:,][”"’')\]]*$/.test(t)||/\d$/.test(t);
  const shape=t=>t.length<=90&&/^[A-Z]/.test(t)&&!endsSentence(t);
  const uh=body.map((l,i)=>i+1<n&&isPS[i+1]&&!isPS[i]&&!isLab[i]&&shape(l.t));
  const nextPara=i=>{for(let j=i+1;j<n;j++)if(isPS[j])return +PS.exec(body[j].t)[1];return null;};
  const paras=[],heads=[];
  let cur=null,started=false,inHead=false,lastHead=null,part=null;
  const path={r:null,l:null,u:null};
  for(let i=0;i<n;i++){
    const l=body[i],t=l.t;
    if(isPS[i]){
      const m=PS.exec(t);inHead=false;started=true;l.kind='paragraph';
      cur={number:+m[1],lines:[],numPage:l.page,sectionRef:lastHead,partRef:part,pathRefs:[path.r,path.l,path.u]};
      if(m[2]!==undefined){
        cur.lines.push({page:l.page,t:m[2],l:l});
        rep('number and text split',l.page,'para. '+cur.number,'The number and the first words stood on one line; they were separated',t,m[1]+'.  |  '+m[2],l.pos,cur.number);
      }
      paras.push(cur);continue;
    }
    if(isLab[i]){
      const roman=/^[IVX]+$/.test(t.slice(0,-1));
      const h={label:t,text:'',kind:'labelled',page:l.page,before:nextPara(i)};
      heads.push(h);lastHead=h;inHead=true;l.kind='heading';cur=null;
      if(roman){part=h;path.r=h;path.l=null;path.u=null;}else{path.l=h;path.u=null;}
      continue;
    }
    if(inHead){
      l.kind='heading';
      if(/^[a-z(]/.test(t)&&lastHead&&lastHead.text){
        const was=hfull(lastHead);lastHead.text+=' '+t;
        rep('heading title joined from two lines',l.page,'before para. '+nextPara(i),'The title of a heading was wrapped over two lines; the lines were joined',was+'  |  '+t,hfull(lastHead),l.pos);
      }else if(lastHead&&lastHead.kind==='labelled'&&!lastHead.text&&lastHead===heads[heads.length-1]){lastHead.text=t;}
      else{const h={label:'',text:t,kind:'unlabelled',page:l.page,before:nextPara(i)};heads.push(h);lastHead=h;path.u=h;}
      continue;
    }
    if(!started){l.kind='cover';continue;}
    if(uh[i]){
      const h={label:'',text:t,kind:'unlabelled',page:l.page,before:nextPara(i)};
      heads.push(h);lastHead=h;path.u=h;l.kind='heading';
      rep('heading separated from paragraph text',l.page,'before para. '+h.before,'A heading stood on the last line before a paragraph number; it was not added to the paragraph before it',cur?cut(cur.lines.length?cur.lines[cur.lines.length-1].t:'',40)+' ⏎ '+t:t,'heading: '+t,l.pos);
      continue;
    }
    if(cur){cur.lines.push({page:l.page,t:t,l:l});l.kind='paragraph';}
  }

  // ---- 3. paragraph text, page range, footnote marks, first words ----
  let counter=1;const rejectedAll=[];
  paras.forEach(p=>{
    p.textLines=p.lines.map(x=>x.t);
    p.textRaw=p.textLines.join(' ').replace(/\s+/g,' ').trim();
    p.hyphens=p.textLines.filter(x=>/[-­]$/.test(x)).length;
    p.pageStart=p.lines.length?p.lines[0].page:p.numPage;
    p.pageEnd=p.lines.length?p.lines[p.lines.length-1].page:p.numPage;
    for(let k=1;k<p.lines.length;k++){
      if(p.lines[k].page!==p.lines[k-1].page){
        rep('paragraph joined across a page break',p.lines[k].page,'para. '+p.number,'Page '+p.lines[k-1].page+' ended and page '+p.lines[k].page+' continued inside this paragraph; the two parts were joined',
          '…'+p.lines[k-1].t.slice(-45)+'  ⏎ page '+p.lines[k].page+' ⏎  '+p.lines[k].t.slice(0,45)+'…','one paragraph',p.lines[k].l.pos,p.number);
      }
    }
    const mk=markText(p.textRaw,counter);counter=mk.counter;
    p.text=mk.text;p.marks=mk.marks;
    mk.rejected.forEach(r=>rejectedAll.push({para:p.number,a:r.a,n:r.n,b:r.b}));
    p.fwFound=p.text.replace(/\[\d+\]/g,'').split(/\s+/).filter(Boolean).slice(0,6).join(' ');
    p.fwRef=refFW&&Object.prototype.hasOwnProperty.call(refFW,String(p.number))?String(refFW[String(p.number)]):null;
    p.fwMatch=refFW?(p.fwRef!==null&&norm(p.fwFound)===norm(p.fwRef)):null;
    p.words=p.textRaw?p.textRaw.split(' ').length:0;
    p.long=p.words>300;
    p.hits=[];
    fns.forEach(f=>{if(f.key&&p.textRaw.indexOf(f.key)>=0)p.hits.push(f.key);});
    p.part=p.partRef?hfull(p.partRef):'';
    p.section=p.sectionRef?hfull(p.sectionRef):'';
    p.path=p.pathRefs.filter(Boolean).map(hfull);
  });
  const marksFound=counter-1;
  repairs.sort((a,b)=>a.pos-b.pos||a.ord-b.ord);
  const fnByNum={};fns.forEach(f=>{if(!fnByNum[f.num])fnByNum[f.num]=f;});

  // ---- 4. every non-empty line classified once ----
  const kinds={cover:0,header:0,heading:0,paragraph:0,footnote:0,footer:0};
  const unclassified=[];let totalLines=0;
  pageInfo.forEach(pi=>pi.lines.forEach(l=>{
    if(l.kind==='blank')return;
    totalLines++;
    if(kinds[l.kind]!=null)kinds[l.kind]++;else{l.kind='unclassified';unclassified.push({page:l.page,n:l.n,t:l.t});}
  }));

  // ---- 5. the checks ----
  const checks=[];
  const C=(name,status,line,detail,link)=>checks.push({name:name,status:status,line:line,detail:detail||'',link:link||null});
  const nums=paras.map(p=>p.number);
  const seen={};paras.forEach(p=>{(seen[p.number]=seen[p.number]||[]).push(p.pageStart);});
  const missing=[],dups=[];
  if(nums.length){
    const top=Math.max.apply(null,nums);
    for(let k=1;k<=top;k++)if(!seen[k]){
      let prev=null;paras.forEach(p=>{if(p.number<k)prev=p;});
      missing.push({n:k,page:prev?prev.pageEnd:null});
    }
    Object.keys(seen).forEach(k=>{if(seen[k].length>1)dups.push({n:+k,pages:seen[k]});});
  }
  const firstBad=pr=>{const i=paras.findIndex(pr);return i<0?null:i;};

  C('Paragraph count',refP==null?'notrun':paras.length===refP?'pass':'fail',
    'Paragraphs found against reference.paragraphs: found '+paras.length+', reference '+(refP==null?'none':refP)+'.',
    refP!=null&&paras.length!==refP?'Difference: '+(paras.length-refP>0?'+':'')+(paras.length-refP)+'.':'',
    {tab:2,i:null});

  const ordered=nums.every((v,i)=>v===i+1);
  C('Numbering',paras.length?(ordered?'pass':'fail'):'notrun',
    'Paragraph numbers should be exactly 1 to '+paras.length+' in order: '+(ordered?'they are.':'they are not.'),
    (missing.length?'Missing: '+lst(missing,20,x=>'para. '+x.n+(x.page!=null?' (after page '+x.page+')':''))+'. ':'')+(dups.length?'Duplicates: '+lst(dups,20,x=>'para. '+x.n+' (pages '+x.pages.join(', ')+')')+'. ':'')+((!ordered&&!missing.length&&!dups.length)?'The numbers are all there but not in order. ':''),
    {tab:2,i:0});

  const badFW=paras.filter(p=>p.fwMatch===false);
  C('First words',refFW?(badFW.length?'fail':'pass'):'notrun',
    'First six words of each paragraph against reference.first_words: '+(refFW?badFW.length+' mismatches in '+paras.length+' paragraphs.':'no first_words in the reference.'),
    badFW.length?lst(badFW,30,p=>'para. '+p.number+': found “'+esc(p.fwFound)+'” / reference “'+esc(p.fwRef==null?'(none)':p.fwRef)+'”'):'',
    {tab:2,i:firstBad(p=>p.fwMatch===false)});

  const fnNums=fns.map(f=>f.num),fnSeen={},fnDup=[],fnMiss=[];
  fnNums.forEach(v=>{fnSeen[v]=(fnSeen[v]||0)+1;});
  Object.keys(fnSeen).forEach(k=>{if(fnSeen[k]>1)fnDup.push(+k);});
  if(fnNums.length){const top=Math.max.apply(null,fnNums);for(let k=1;k<=top;k++)if(!fnSeen[k])fnMiss.push(k);}
  const fnSeq=fnNums.every((v,i)=>v===i+1);
  const restored=fns.filter(f=>f.repaired);
  C('Footnotes',refF==null?'notrun':(fns.length===refF&&fnSeq)?'pass':'fail',
    'Footnotes found (numbered openers plus restored numbers) against reference.footnotes: found '+fns.length+', reference '+(refF==null?'none':refF)+'; numbers run 1 to '+(fnNums.length?Math.max.apply(null,fnNums):0)+(fnSeq?' without a gap or duplicate.':' with gaps or duplicates.'),
    (fnMiss.length?'Missing numbers: '+lst(fnMiss,30,x=>x)+'. ':'')+(fnDup.length?'Duplicate numbers: '+lst(fnDup,30,x=>x)+'. ':'')+
    (restored.length?'Numbers restored from the page foot (repairs): '+restored.map(f=>f.num+' (page '+f.page+')').join(', ')+'. ':'')+(notes.filter(x=>/count jumped|no line opens|displaced/.test(x)).map(esc).join(' ')),
    {tab:3,i:null});

  const missingMarks=[];
  if(refF!=null)for(let k=marksFound+1;k<=refF;k++)missingMarks.push(k);
  const rej=rejectedAll.slice().sort((x,y)=>(/article/i.test(y.a)?1:0)-(/article/i.test(x.a)?1:0)).slice(0,6);
  C('Footnote marks',refF==null?'notrun':(marksFound===refF?'pass':'fail'),
    'Marks found in the paragraphs, expected 1 to '+(refF==null?'?':refF)+': found '+marksFound+'.',
    (missingMarks.length?'Missing marks: '+(missingMarks.length>12?missingMarks[0]+' to '+missingMarks[missingMarks.length-1]+' ('+missingMarks.length+')':missingMarks.join(', '))+'. ':'')+
    rejectedAll.length+' other numbers were left alone'+(rej.length?', for example '+rej.map(r=>'“…'+esc(r.a)+'<b>'+esc(r.n)+'</b>'+esc(r.b)+'…” (para. '+r.para+')').join('; '):'')+'.',
    {tab:2,i:null});

  const hitParas=paras.filter(p=>p.hits.length),longParas=paras.filter(p=>p.long);
  const maxWords=paras.reduce((a,p)=>Math.max(a,p.words),0);
  C('Footnotes stay out of the paragraphs',(hitParas.length||longParas.length)?'fail':'pass',
    'The first 40 characters of every footnote opener searched in every paragraph: '+hitParas.length+' hits (expected 0). Paragraphs over 300 words: '+longParas.length+' (longest: '+maxWords+' words).',
    (hitParas.length?'Footnote text found in: '+lst(hitParas,20,p=>'para. '+p.number+' (“'+esc(p.hits[0])+'”)')+'. ':'')+(longParas.length?'Over 300 words: '+lst(longParas,20,p=>'para. '+p.number+' ('+p.words+' words)')+'.':''),
    {tab:2,i:firstBad(p=>p.hits.length||p.long)});

  const withHeader=pageInfo.filter(p=>p.header).length,withNo=pageInfo.filter((p,i)=>i>0&&p.pageNo).length;
  const allDisp=[];pageInfo.forEach(p=>p.displaced.forEach(d=>allDisp.push({num:d.num,page:p.page})));
  C('Headers and footers',(pageInfo.length&&withHeader===pageInfo.length&&withNo===pageInfo.length-1)?'pass':'fail',
    'Pages whose first line was the symbol: '+withHeader+' of '+pageInfo.length+'. Pages with a page number in the footer: '+withNo+' of '+Math.max(pageInfo.length-1,0)+' expected (all but the first).',
    allDisp.length?'Displaced footnote numbers (moved by the converter into the footer): '+allDisp.map(d=>d.num+' (page '+d.page+')').join(', ')+'.':'No displaced footnote numbers.',
    {raw:1});

  const labelled=heads.filter(h=>h.kind==='labelled'),unl=heads.filter(h=>h.kind==='unlabelled');
  C('Headings',heads.length?'pass':'notrun',
    'Headings found: '+labelled.length+' with a label (I., A.) and '+unl.length+' without.',
    unl.length?'Without a label: '+lst(unl,40,h=>'“'+esc(h.text)+'” (before para. '+h.before+')')+'. A paragraph’s last line mistaken for a heading would show up here.':'',
    {tab:2,i:null});

  const sumKinds=Object.keys(kinds).reduce((a,k)=>a+kinds[k],0);
  C('Nothing lost',(unclassified.length===0&&sumKinds===totalLines)?'pass':'fail',
    'Every non-empty line is classified once: '+Object.keys(kinds).map(k=>k+' '+kinds[k]).join(', ')+'; together '+sumKinds+' of '+totalLines+' lines.',
    (unclassified.length?'Not classified: '+lst(unclassified,20,u=>'page '+u.page+', line '+u.n+' (“'+esc(cut(u.t,40))+'”)'):'')+(paras.reduce((a,p)=>a+p.hyphens,0)?' Lines ending in a hyphen (not joined): '+paras.reduce((a,p)=>a+p.hyphens,0)+'.':' Lines ending in a hyphen: 0, so no hyphen joining was needed.'),
    {raw:unclassified.length?unclassified[0].page:1});

  return {doc:doc,symbol:symbol,ref:ref,refP:refP,refF:refF,refFW:refFW,pageInfo:pageInfo,paras:paras,fns:fns,fnByNum:fnByNum,heads:heads,repairs:repairs,checks:checks,notes:notes,coverNote:coverNote,hitCount:hitParas.length,marksFound:marksFound};
}
function plural(n,a,b){return n+' '+(n===1?a:b);}

// ---- documents in the data: any file of raw PDF pages (records with page and text) ----
const docs=Object.keys(WD).filter(k=>{
  const d=WD[k];
  return d&&typeof d==='object'&&Array.isArray(d.records)&&d.records.length&&d.records[0]&&typeof d.records[0].text==='string'&&d.records[0].page!=null;
}).map(k=>({key:k,d:WD[k]}));
if(!docs.length){
  $('#main').innerHTML='<p class="q">No PDF text found</p><p>This page needs the converter’s raw text of a document. Drag the right file from “Your files” into the chat.</p>';
  $('#tabs').hidden=true;$('#cards').innerHTML='<p class="hint">no document</p>';
  return;
}
let results;
try{results=docs.map(x=>analyse(x.d));}
catch(err){
  $('#main').innerHTML='<p class="q">The page could not read this file</p><p class="fail">'+esc(err&&err.message||err)+'</p>';
  return;
}
let R=results[0],curDoc=0,tab=1;

// ---- helpers for the checks ----
const counts=r=>{
  const c={pass:0,fail:0,notrun:0,total:r.checks.length};
  r.checks.forEach(x=>{c[x.status]++;});
  return c;
};
const linkSym=r=>{const u=safeUrl(r.doc.doc_url);return u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol);};
const fileBase=r=>(r.symbol||'document').replace(/\//g,'-').replace(/[^\w.\-]+/g,'_');

// ---- rendering ----
function renderHeader(){
  const d=R.doc,c=counts(R);
  $('#title').textContent=d.title||R.symbol||'Document';
  const bits=[];
  if(R.symbol)bits.push(linkSym(R));
  if(R.ref&&R.ref.adopted)bits.push('adopted '+esc(R.ref.adopted));
  bits.push(R.pageInfo.length+' pages of raw converter text');
  if(d.source)bits.push(esc(d.source));
  $('#meta').innerHTML=bits.join(' · ');
  $('#status').innerHTML=c.fail?'<span class="dot bad"></span><span class="fail">'+plural(c.fail,'check','checks')+' failed</span>':
    '<span class="dot '+(c.pass===c.total?'ok':'')+'"></span><span>'+c.pass+' of '+c.total+' checks pass'+(c.notrun?', '+c.notrun+' not run':'')+'</span>';
  $('#t4dot').hidden=!c.fail;
  document.title=(R.symbol?R.symbol+': ':'')+'paragraphs out of a PDF';
  const f=[];
  if(d.source)f.push('Source: '+esc(d.source)+(R.symbol?' · '+linkSym(R):'')+(d.built?' · built '+esc(d.built):''));
  f.push('Counting, splitting and matching are done by this page’s code; no model was called and nothing left the browser.');
  $('#foot').innerHTML=f.map(x=>'<p>'+x+'</p>').join('');
}

function renderRail(){
  $('#cards').innerHTML=results.map((r,i)=>{
    const d=r.doc;
    return '<button type="button" class="card" data-act="doc" data-i="'+i+'" aria-current="'+(i===curDoc)+'">'+
      '<span class="sym">'+esc(r.symbol||docs[i].key)+'</span><span class="tt">'+esc(cut(d.title||'',70))+'</span>'+
      '<span class="sub">'+(r.ref&&r.ref.adopted?'adopted '+esc(r.ref.adopted)+' · ':'')+r.pageInfo.length+' pages</span></button>';
  }).join('');
  const c=counts(R);
  const stat=(n,label,refv)=>{
    const eq=refv!=null&&n===refv;
    return '<div class="stat"><div class="big">'+n+'</div><div class="of">'+label+(refv==null?' · no reference in this file':' · of '+refv+' in the reference')+'</div>'+
      (refv!=null?'<div class="bar'+(eq?'':' bad')+'" role="img" aria-label="'+n+' of '+refv+(eq?', equal':', not equal')+'"><i style="width:'+Math.min(100,refv?n/refv*100:0)+'%"></i></div>':'')+'</div>';
  };
  $('#stats').innerHTML=stat(R.paras.length,'paragraphs',R.refP)+stat(R.fns.length,'footnotes',R.refF)+
    '<div class="stat"><button type="button" class="lnk" data-act="tab" data-tab="4">'+c.pass+' of '+c.total+' checks pass</button></div>';
}

function panel1(){
  const r=R,f=r.paras.length,fw=r.paras.filter(p=>p.fwMatch===true).length,c=counts(r);
  const noref='<span class="muted">no reference in this file</span>';
  const cmp=(a,b)=>b==null?noref:a===b?'<span class="pass">equal to the reference</span>':'<span class="fail">'+(a>b?'+':'−')+Math.abs(a-b)+' against the reference</span>';
  const cls=(a,b)=>b==null?'':a===b?'pass':'fail';
  const failed=r.checks.filter(x=>x.status==='fail').map(x=>x.name);
  let answer;
  if(failed.length)answer='Not completely. '+plural(failed.length,'check','checks')+' failed: '+esc(failed.join(', '))+'. Details are on tab 04.';
  else if(c.notrun)answer='The page found '+f+' paragraphs and '+r.fns.length+' footnotes. '+c.notrun+' checks could not run because the reference is missing something.';
  else answer='Yes. The page found all '+f+' paragraphs and all '+r.fns.length+' footnotes, and every check passes.';
  const tile=(lbl,big,sub,how)=>'<div class="tile"><div class="mono muted">'+lbl+'</div>'+big+'<div class="sub">'+sub+'</div><p class="how">How this is computed: '+how+'</p></div>';
  return '<p class="q">Did the app find everything the document has?</p><p class="answer">'+answer+'</p><div class="tiles">'+
    tile('Paragraphs found','<div class="pair"><div><span class="num '+cls(f,r.refP)+'">'+f+'</span></div><div><div class="mono muted">The document has</div><span class="num">'+(r.refP==null?'–':r.refP)+'</span></div></div>',
      cmp(f,r.refP)+(r.hitCount?' · <span class="fail">'+r.hitCount+' contain footnotes</span>':''),
      'every line that is a number and a full stop, alone or with the first words after it, starts a paragraph.')+
    tile('Footnotes found','<span class="num '+cls(r.fns.length,r.refF)+'">'+r.fns.length+'</span><span class="of"> of '+(r.refF==null?'–':r.refF)+'</span>',cmp(r.fns.length,r.refF),
      'footnotes read from the foot of each page, plus those whose number the converter moved and the page put back.')+
    tile('First words match','<span class="num '+(r.refFW?cls(fw,r.refP):'')+'">'+(r.refFW?fw:'–')+'</span><span class="of"> of '+(r.refP==null?'–':r.refP)+'</span>',r.refFW?(fw===r.refP?'<span class="pass">every paragraph starts as the reference says</span>':'<span class="fail">'+(f-fw)+' paragraphs start differently</span>'):noref,
      'the first six words of each paragraph, compared with the reference after straightening quotes and dashes.')+
    tile('Repairs made','<span class="num">'+r.repairs.length+'</span>','<button type="button" class="lnk" data-act="openlog">Open the repair log</button>',
      'one entry for every change the script made to the converter’s text.')+
    '</div><div class="terms"><p class="mono">Words used here</p>'+
    '<p><b>Footer:</b> the lines at the bottom of a page (page number, job code, date stamp).</p>'+
    '<p><b>Footnote block:</b> the footnotes at the foot of a page, above the footer.</p>'+
    '<p><b>Displaced number:</b> a footnote number the converter moved into the footer.</p></div>';
}

function detailRow(p,i){
  const rp=R.repairs.filter(x=>x.para===p.number);
  const cite=R.symbol+', para. '+p.number;
  let pl='',last=null;
  p.lines.forEach(x=>{if(x.page!==last){pl+='[page '+x.page+' begins]\n';last=x.page;}pl+=x.t+'\n';});
  const fnl=p.marks.map(m=>{const f=R.fnByNum[m];return '<li>['+m+'] '+(f?esc(f.text):'<span class="fail">footnote not found</span>')+'</li>';}).join('');
  const same=p.fwMatch;
  return '<tr class="detail" id="d-'+i+'" hidden><td colspan="5">'+
    '<div class="mono lab">Section</div><div>'+(p.path.length?esc(p.path.join(' › ')):'<span class="muted">no heading above</span>')+'</div>'+
    '<div class="mono lab">Full text <span class="hint">footnote marks in [brackets]</span></div><p class="ptext">'+esc(p.text)+'</p>'+
    '<button type="button" class="lnk" data-act="lines" aria-expanded="false" aria-controls="ln-'+i+'">Show the PDF’s lines</button>'+
    '<pre class="plines" id="ln-'+i+'" hidden>'+esc(pl.replace(/\n$/,''))+'</pre>'+
    '<div class="cols"><div><div class="mono lab">First six words</div>'+
      '<div>Reference: '+(p.fwRef==null?'<span class="muted">none</span>':'“'+esc(p.fwRef)+'”')+'</div><div>Extracted: “'+esc(p.fwFound)+'”</div>'+
      '<div>'+(same===true?'<span class="pass">equal</span>':same===false?'<span class="fail">different</span>':'<span class="muted">not checked</span>')+'</div></div>'+
    '<div><div class="mono lab">Pages</div><div>'+pg(p)+'</div><div class="mono lab">Repairs on this paragraph</div>'+
      (rp.length?'<ul>'+rp.map(x=>'<li>'+esc(x.kind)+' (page '+x.page+')</li>').join('')+'</ul>':'<div class="muted">none</div>')+'</div></div>'+
    '<div class="mono lab">Footnotes cited</div>'+(fnl?'<ul>'+fnl+'</ul>':'<div class="muted">none</div>')+
    '<p>Cite as: '+linkSym(R)+', para. '+p.number+' <button type="button" class="btn sm" data-act="copy" data-cite="'+esc(cite)+'">Copy citation</button></p>'+
    '</td></tr>';
}

function panel2(){
  const r=R,f=r.paras.length;
  const flags=p=>{
    const a=[];
    if(p.hits.length)a.push('contains footnote text');
    if(p.long)a.push('over 300 words');
    if(p.fwMatch===false)a.push('first words differ');
    return a.length?'<span class="fail">'+esc(a.join('; '))+'</span>':p.fwMatch===true?'<span class="pass">OK</span>':'<span class="muted">not checked</span>';
  };
  const rows=r.paras.map((p,i)=>'<tr class="prow" data-i="'+i+'"><td class="r"><button type="button" class="pnum" aria-expanded="false" aria-controls="d-'+i+'" title="Show the full text">'+p.number+'</button></td>'+
    '<td>'+esc(p.section||'–')+'</td><td class="r">'+pg(p)+'</td><td>'+esc(cut(p.text,120))+'</td><td>'+flags(p)+'</td></tr>'+detailRow(p,i)).join('');
  const hrows=r.heads.map(h=>'<tr><td>'+esc(h.label||'–')+'</td><td>'+esc(h.text)+'</td><td>'+(h.kind==='labelled'?'with label':'no label')+'</td><td class="r">'+h.page+'</td><td class="r">'+(h.before==null?'–':h.before)+'</td></tr>').join('');
  return '<p class="q">What does each paragraph say, and how do I cite it?</p>'+
    '<button type="button" class="disc" data-act="toggle" data-target="headsbox" aria-expanded="false" aria-controls="headsbox">Headings found: '+r.heads.length+' <span class="hint">check that none was swallowed into a paragraph</span></button>'+
    '<div class="box" id="headsbox" hidden><table><caption><span class="mono">TAB.01</span>'+r.heads.length+' headings found, taken out of the paragraph text</caption><thead><tr><th scope="col">Label</th><th scope="col">Heading</th><th scope="col">Kind</th><th scope="col" class="r">Page</th><th scope="col" class="r">Before para.</th></tr></thead><tbody>'+(hrows||'<tr><td colspan="5" class="muted">No headings found.</td></tr>')+'</tbody></table></div>'+
    '<table><caption><span class="mono">TAB.02</span>'+f+' paragraphs found, '+(r.refP==null?'no reference in this file':r.refP+' expected')+'</caption>'+
    '<thead><tr><th scope="col" class="r">No.</th><th scope="col">Section</th><th scope="col" class="r">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>'+
    (rows||'<tr><td colspan="5" class="muted">No numbered paragraphs were found.</td></tr>')+'</tbody></table>'+
    '<p class="src">Source: '+linkSym(r)+', '+esc(r.doc.source||'')+'. n = '+f+' paragraphs from '+r.pageInfo.length+' pages, no filter. <span class="hint">click a row = full text</span></p>'+
    '<p class="how">Footnote marks in the text are shown in square brackets, as in &ldquo;waste.[2]&rdquo;, in the table, the expanded paragraph and the CSV. To remove them, find <code>\\[\\d+\\]</code> and replace with nothing.</p>';
}

function panel3(){
  const r=R,f=r.fns.length;
  const rows=r.fns.map(x=>'<tr><td class="r">'+x.num+'</td><td class="r">'+x.page+'</td><td>'+esc(x.text)+'</td><td>'+(x.repaired?'number restored from the page foot':'–')+'</td></tr>').join('');
  return '<p class="q">What do the footnotes say?</p>'+
    '<p><button type="button" class="btn" data-act="csvf">footnotes.csv</button> <span class="hint">UTF-8, opens in Excel</span></p>'+
    '<table><caption><span class="mono">TAB.03</span>Footnotes found: '+f+' of '+(r.refF==null?'no reference':r.refF)+'</caption>'+
    '<thead><tr><th scope="col" class="r">No.</th><th scope="col" class="r">Page</th><th scope="col">Text</th><th scope="col">Repair</th></tr></thead><tbody>'+
    (rows||'<tr><td colspan="4" class="muted">No footnotes were found.</td></tr>')+'</tbody></table>'+
    '<p class="src">Source: '+linkSym(r)+', '+esc(r.doc.source||'')+'. n = '+f+' footnotes, no filter.'+(r.coverNote?' Cover note, not counted: “'+esc(cut(r.coverNote.text,160))+'”':'')+'</p>';
}

function panel4(){
  const r=R,c=counts(r);
  const label={pass:'<span class="pass">pass</span>',fail:'<span class="fail">check failed</span>',notrun:'<span class="muted">not run</span>'};
  const li=r.checks.map(x=>{
    let lk='';
    if(x.status==='fail'&&x.link){
      if(x.link.raw)lk=' <button type="button" class="lnk" data-act="raw" data-page="'+x.link.raw+'">see the page</button>';
      else lk=' <button type="button" class="lnk" data-act="goto" data-tab="'+x.link.tab+'"'+(x.link.i!=null?' data-i="'+x.link.i+'"':'')+'>see the rows</button>';
    }
    return '<li><div><div class="nm">'+esc(x.name)+'</div><div>'+esc(x.line)+lk+'</div></div><div>'+label[x.status]+'</div>'+(x.detail?'<div class="det">'+x.detail+'</div>':'')+'</li>';
  }).join('');
  const kc=KINDS.map(k=>k+': '+r.repairs.filter(x=>x.kind===k).length).join(' · ');
  const rrows=r.repairs.map(x=>'<tr><td class="r">'+x.page+'</td><td>'+esc(x.where)+'</td><td>'+esc(x.kind)+'. '+esc(x.what)+'</td><td>'+esc(cut(x.before,90))+'</td><td>'+esc(cut(x.after,90))+'</td></tr>').join('');
  const opts=r.pageInfo.map((p,i)=>'<option value="'+i+'">'+p.page+'</option>').join('');
  const legend=['cover','header','heading','paragraph','footnote','footer','unclassified'].map(k=>'<span class="chip k-'+k+'"><b>'+CODE[k]+'</b>'+(k==='unclassified'?'not classified':k)+'</span>').join('');
  return '<p class="q">Can I trust this, and can I take it away?</p>'+
    '<h2 class="h2" style="margin-top:0">Checks <span class="hint">'+c.pass+' of '+c.total+' pass</span></h2><ul class="checks">'+li+'</ul>'+
    (r.notes.length?'<p class="how">Notes from the run: '+esc(r.notes.join(' '))+'</p>':'')+
    '<button type="button" class="disc" id="logbtn" data-act="toggle" data-target="logbox" aria-expanded="false" aria-controls="logbox">Repair log ('+r.repairs.length+')</button>'+
    '<div class="box" id="logbox" hidden><p class="kinds">'+esc(kc)+'</p><table><caption><span class="mono">TAB.04</span>'+r.repairs.length+' repairs made by the script, in document order</caption>'+
    '<thead><tr><th scope="col" class="r">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>'+rrows+'</tbody></table>'+
    '<p class="src">Source: '+linkSym(r)+'. Every entry is made by this page’s code.</p></div>'+
    '<button type="button" class="disc" id="rawbtn" data-act="toggle" data-target="rawbox" aria-expanded="false" aria-controls="rawbox">Raw pages</button>'+
    '<div class="box" id="rawbox" hidden><div class="rawbar"><label for="rawsel" class="mono">Show raw page</label><select id="rawsel">'+opts+'</select><span class="hint">as stored, line numbers on the left, colour = what the script decided</span></div>'+
    '<div class="legend">'+legend+'</div><div class="raw" id="rawview" tabindex="0" aria-label="Raw page text"></div></div>'+
    '<h2 class="h2">Method</h2><ol class="method"><li>Each page is read line by line.</li><li>The symbol line at the top is removed (header).</li><li>The lines at the foot are removed (footer): job code, date stamp, the page number. A bare number there that is not the page number is a displaced footnote number.</li><li>The footnote block is found by counting 1, 2, 3 and cut off the page. A displaced number is given back to its footnote.</li><li>The remaining lines of all pages are joined in order, so a paragraph that crosses a page break is whole.</li><li>A line such as &ldquo;12.&rdquo; or &ldquo;12. Text&rdquo; starts a paragraph. Headings are kept apart from paragraph text.</li><li>Footnote marks are found by counting through the text: a number equal to the next expected footnote number is a mark, any other number is left alone.</li><li>The result is compared with the reference and the checks above are run.</li></ol>'+
    '<h2 class="h2">Download</h2><p><button type="button" class="btn" data-act="csvp">Download paragraphs as CSV</button> <span class="hint" id="dlmsg">one row per paragraph, UTF-8</span></p>';
}

function drawRaw(){
  const sel=$('#rawsel');if(!sel)return;
  const pi=R.pageInfo[sel.selectedIndex];if(!pi)return;
  $('#rawview').innerHTML=pi.lines.map(l=>'<div class="ln k-'+(l.kind==='blank'?'none':l.kind)+'"><span class="no">'+l.n+'</span><span class="cd">'+(CODE[l.kind]||'')+'</span><span class="tx">'+esc(l.raw)+'</span></div>').join('');
}

function renderDoc(){
  R=results[curDoc];
  renderHeader();renderRail();
  $('#p1').innerHTML=panel1();$('#p2').innerHTML=panel2();$('#p3').innerHTML=panel3();$('#p4').innerHTML=panel4();
  setTab(tab);
}

function setTab(n,focus){
  tab=n;
  $$('[role="tab"]').forEach(b=>{const on=+b.dataset.tab===n;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;});
  $$('[role="tabpanel"]').forEach(p=>{const on=+p.dataset.tab===n;p.hidden=!on;p.tabIndex=on?0:-1;});
  if(focus)$('#t'+n).focus();
}
function toggle(btn,force){
  const el=document.getElementById(btn.dataset.target);
  const open=force!==undefined?force:btn.getAttribute('aria-expanded')!=='true';
  btn.setAttribute('aria-expanded',open);el.hidden=!open;
  if(open&&btn.id==='rawbtn')drawRaw();
  return open;
}
function toggleRow(tr,force){
  const b=tr.querySelector('.pnum'),d=document.getElementById('d-'+tr.dataset.i);
  const open=force!==undefined?force:b.getAttribute('aria-expanded')!=='true';
  b.setAttribute('aria-expanded',open);d.hidden=!open;
}

// ---- export ----
const csv=rows=>'﻿'+rows.map(r=>r.map(c=>'"'+String(c==null?'':c).replace(/"/g,'""')+'"').join(',')).join('\r\n')+'\r\n';
function save(name,text){
  const url=URL.createObjectURL(new Blob([text],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),5000);
}
function csvParas(){
  const rows=[['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','footnotes_cited','repairs','citation','symbol','doc_url','text_lines']];
  R.paras.forEach(p=>rows.push([p.number,p.section,p.part,p.pageStart,p.pageEnd,p.fwRef==null?'':p.fwRef,p.fwFound,p.fwMatch==null?'':p.fwMatch?'yes':'no',p.text,p.textRaw,p.marks.join('; '),
    R.repairs.filter(x=>x.para===p.number).map(x=>x.kind).join('; '),R.symbol+', para. '+p.number,R.symbol,R.doc.doc_url||'',p.textLines.join(' | ')]));
  return csv(rows);
}
function csvFns(){
  const rows=[['number','page','text','repair','symbol','doc_url']];
  R.fns.forEach(f=>rows.push([f.num,f.page,f.text,f.repaired?'number restored from the page foot':'',R.symbol,R.doc.doc_url||'']));
  return csv(rows);
}
function copyText(s,btn){
  const label=btn.dataset.label||btn.textContent;btn.dataset.label=label;
  const done=ok=>{btn.textContent=ok?'Copied':'Copy failed: select the text';clearTimeout(btn._t);btn._t=setTimeout(()=>{btn.textContent=label;},2000);};
  const legacy=()=>{
    const ta=document.createElement('textarea');ta.value=s;ta.setAttribute('readonly','');ta.style.cssText='position:fixed;opacity:0;top:0';
    document.body.appendChild(ta);ta.select();let ok=false;
    try{ok=document.execCommand('copy');}catch(e){}
    ta.remove();done(ok);
  };
  try{
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).then(()=>done(true),legacy);return;}
  }catch(e){}
  legacy();
}

// ---- events ----
function act(a){
  const k=a.dataset.act;
  if(k==='tab')setTab(+a.dataset.tab);
  else if(k==='doc'){curDoc=+a.dataset.i;renderDoc();}
  else if(k==='toggle')toggle(a);
  else if(k==='lines'){
    const pre=document.getElementById(a.getAttribute('aria-controls')),open=a.getAttribute('aria-expanded')!=='true';
    a.setAttribute('aria-expanded',open);pre.hidden=!open;
  }
  else if(k==='copy')copyText(a.dataset.cite,a);
  else if(k==='openlog'){setTab(4);const b=$('#logbtn');toggle(b,true);b.scrollIntoView({block:'start'});b.focus();}
  else if(k==='goto'){
    setTab(+a.dataset.tab);
    if(a.dataset.i!==undefined&&+a.dataset.tab===2){
      const tr=$('#p2 tr.prow[data-i="'+a.dataset.i+'"]');
      if(tr){toggleRow(tr,true);tr.scrollIntoView({block:'center'});}
    }
  }
  else if(k==='raw'){
    setTab(4);toggle($('#rawbtn'),true);
    const i=R.pageInfo.findIndex(p=>p.page===+a.dataset.page);
    if(i>=0)$('#rawsel').selectedIndex=i;
    drawRaw();$('#rawbtn').scrollIntoView({block:'start'});
  }
  else if(k==='csvp'){save(fileBase(R)+'-paragraphs.csv',csvParas());const m=$('#dlmsg');if(m)m.textContent='Download started: '+R.paras.length+' rows.';}
  else if(k==='csvf')save(fileBase(R)+'-footnotes.csv',csvFns());
}
document.addEventListener('click',e=>{
  const a=e.target.closest('[data-act]');
  if(a){act(a);return;}
  const row=e.target.closest('tr.prow');
  if(row)toggleRow(row);
});
document.addEventListener('change',e=>{if(e.target.id==='rawsel')drawRaw();});
$('#tabs').addEventListener('keydown',e=>{
  const keys={ArrowRight:1,ArrowLeft:-1,Home:'first',End:'last'};
  if(!(e.key in keys))return;
  e.preventDefault();
  const v=keys[e.key];
  let n=v==='first'?1:v==='last'?4:tab+v;
  if(n<1)n=4;if(n>4)n=1;
  setTab(n,true);
});

renderDoc();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a second document: the Human Rights Committee's general comment No. 32, attached. Run exactly the same pipeline on it, with no rule changed, and give it its own card in the left rail so I can switch between the two documents; every tab and every check works on the selected document. Under the cards, add a small table comparing the two documents: paragraphs found, footnotes found and checks passed, each next to its reference.

(Attached: CCPR General comment No. 32 (PDF) → WORKSHOP_DATA.pdf_text_2)
