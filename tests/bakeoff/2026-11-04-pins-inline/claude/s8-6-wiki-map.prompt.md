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

# ASSISTANT MESSAGE (your earlier answer)

I built the research wiki workspace with five tabs: Pages, Ask, Ingest, Check and Record. Every quotation is checked by the page's own code against the library passages, nothing is sent to a model until you press a button, and every change waits for a person to approve it. Pins are shown as the quoted words in place, followed by a small citation chip that opens the PDF.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Research wiki: neurotechnology and justice</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5a554c;--ok:#1d6a38;--amb:#8a5400;--ins:#fbf0c0;--grey:#ece7db;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
[hidden]{display:none!important}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
h1,h2,h3,h4{font-family:var(--serif);font-weight:400;line-height:1.2;margin:1.2em 0 .4em}
h1{font-size:30px;margin:.2em 0 .3em}h2{font-size:30px;margin-top:.3em}h3{font-size:22px}h4{font-size:18px}
.lab,.hint,.how,.meta,.rg,.st,.badge,th,caption,.stub,.run,.sess,footer,.stepper,.says{font-family:var(--mono)}
.lab{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);margin:0}
.hint,.how,.meta{font-size:12px;color:var(--mute);margin:.3em 0}
.big{font-family:var(--serif);font-size:48px;line-height:1;color:var(--ink)}
.top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:16px;padding:20px 24px 12px;border-bottom:1px solid var(--rule)}
.hl{flex:1 1 520px}.hr{flex:0 1 460px;text-align:right}.hr .lab{margin-bottom:6px;text-transform:none;letter-spacing:.02em}
.sub{margin:0;font-size:15px;color:var(--mute)}
#tabs{display:flex;flex-wrap:wrap;gap:4px 22px;padding:0 24px;border-bottom:1px solid var(--rule)}
#tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:12px 2px 9px;font:12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);cursor:pointer}
#tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.panel{padding:20px 24px 40px}
.two{display:grid;grid-template-columns:320px minmax(0,900px);gap:32px;align-items:start}
.rail{border-right:1px solid var(--rule);padding-right:20px}
.rail input{width:100%}
.cnt{margin:.6em 0 0;font-size:16px}.cnt .big{font-size:48px}
.grp{margin:16px 0 4px}
.plist{list-style:none;margin:0;padding:0}.plist li{padding:5px 0;border-bottom:1px solid var(--rule)}
.plist a{text-decoration:none;color:var(--ink)}.plist a[aria-current=page]{color:var(--red);font-weight:600}.plist a:hover{text-decoration:underline}
.stub{background:var(--ink);color:var(--paper);font-size:10.5px;padding:0 5px;text-transform:uppercase;border-radius:2px}
.narrow{max-width:900px}
input[type=text],input[type=search],textarea{width:100%;font:16px system-ui,sans-serif;padding:8px 10px;border:1px solid #8a8274;background:#fffdf8;color:var(--ink);border-radius:2px}
.lbl{display:block;font-family:var(--mono);font-size:12px;text-transform:uppercase;letter-spacing:.06em;margin:10px 0 4px}
.btn{font:13px var(--mono);letter-spacing:.04em;padding:8px 14px;border:1px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer;border-radius:2px}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.btn:disabled{opacity:.55;cursor:not-allowed}
.lk{background:none;border:0;padding:0;color:var(--red);text-decoration:underline;cursor:pointer;font:inherit}
.row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:10px 0}
.grey{background:var(--grey);border-left:3px solid var(--mute);padding:8px 12px;margin:10px 0;font-size:14px}
.prog{font-family:var(--mono);font-size:12.5px;color:var(--mute);min-height:1.4em;margin:6px 0}
.warn{border:1px solid var(--amb);padding:8px 12px;margin:10px 0}.warn pre{white-space:pre-wrap;max-height:220px;overflow:auto}
.pmain{min-width:0;max-width:900px}.page p,.page li{max-width:75ch}
.page h3{border-top:1px solid var(--rule);padding-top:.7em}
.page .dim{color:#6b665c}.page .ins{background:var(--ins);border-left:3px solid var(--red);padding:4px 10px}
.page ul.ins,.page ol.ins{padding-left:28px}
.dang{color:var(--red);border-bottom:1px dotted var(--red)}.dang small{font-family:var(--mono);font-size:10.5px}
.badge{display:inline-block;border:1px solid var(--mute);font-size:11px;padding:1px 7px;margin:0 6px 4px 0;text-transform:uppercase;letter-spacing:.04em}
.pq{font-family:var(--serif);font-style:italic}.pq.x{text-decoration:line-through;color:var(--mute)}
.chip{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--ok);padding:0 6px;margin:0 2px;font-size:11.5px;line-height:1.7;vertical-align:baseline;background:#fffdf8}
.chip.bad{border-color:var(--amb)}.chip.struck{border-color:var(--red)}.chip.struck .cl{text-decoration:line-through}
.cl{background:none;border:0;padding:0;font:12px var(--mono);color:var(--red);text-decoration:underline;cursor:pointer}
.rg{color:var(--mute)}.st{font-size:11px}.chip .st{color:var(--ok)}.chip.bad .st{color:var(--amb)}.chip.struck .st{color:var(--red)}
.says{font-size:10.5px;color:var(--amb)}
.tg{background:none;border:0;cursor:pointer;color:var(--ink);font-size:12px;padding:0 2px}
.pd{display:block;margin:4px 0 8px;padding:6px 10px;border-left:3px solid var(--rule);font-size:14px;max-width:70ch}
.card{border:0;border-top:2px solid var(--ink);border-bottom:1px solid var(--rule);padding:10px 0;margin:18px 0;min-width:0}
.card legend{font-family:var(--mono);font-size:12px;text-transform:uppercase;padding:0 8px 0 0}
.claim{margin:.2em 0}.verdict{font-family:var(--serif);font-size:40px;line-height:1.1;margin:.2em 0;color:var(--red)}
.bar{height:12px;background:var(--grey);border:1px solid var(--rule);max-width:420px}.bar i{display:block;height:100%;background:var(--red)}
.tw{overflow-x:auto;max-width:100%}
table{border-collapse:collapse;width:100%}
caption{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);padding:6px 0}
th{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px 6px 0}
td,th[scope=row]{border-bottom:1px solid var(--rule);padding:7px 8px 7px 0;vertical-align:top;font-size:16px}
th[scope=row]{font:inherit;text-transform:none;letter-spacing:0}
.num{text-align:right;font-variant-numeric:tabular-nums}
.pass{color:var(--ok);font-weight:600}.chk{color:var(--red);font-weight:600}.na{color:var(--mute)}
.sess{background:var(--red);color:#fff;font-size:10.5px;padding:0 6px;text-transform:uppercase}
.stepper{display:flex;flex-wrap:wrap;gap:6px 24px;list-style:none;padding:0;margin:8px 0;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.stepper [aria-current=step]{color:var(--red);border-bottom:2px solid var(--red)}.stepper .done{color:var(--ok)}
.runline{margin:10px 0}.runline .big{font-size:40px}
.sec{border-top:1px solid var(--rule);margin-top:16px;padding-top:6px}.sec summary{cursor:pointer;font-family:var(--serif);font-size:20px}
.chg{border:1px solid var(--rule);padding:10px 16px;margin:14px 0}.chg legend{font-family:var(--serif);font-size:20px;padding:0 6px}
.pick{max-height:220px;overflow:auto;border:1px solid var(--rule);margin:8px 0}.ck{display:block;padding:2px 8px}
.pgchip{display:inline-block;border:1px solid var(--red);padding:0 8px;margin:2px 4px 2px 0;text-decoration:none;font-size:14px}
.prev{white-space:pre-wrap;background:var(--grey);padding:10px;max-height:260px;overflow:auto;font:12px/1.4 var(--mono)}
.answer{border-top:2px solid var(--ink);margin-top:16px}
.kv{margin:2px 0}.kv .lab{display:inline-block;min-width:70px}
.tens{border-top:1px solid var(--rule);padding:6px 0}.tens.sel{background:var(--ins)}
.le{border-bottom:1px solid var(--rule);padding:6px 0}.le summary{cursor:pointer;font-family:var(--mono);font-size:13px}
.chkl{list-style:none;padding:0}.chkl li{padding:6px 0;border-bottom:1px solid var(--rule)}
button[role=switch]{font:12px var(--mono);padding:4px 10px;border:1px solid var(--ink);background:transparent;cursor:pointer}
button[role=switch][aria-checked=true]{background:var(--ink);color:var(--paper)}
footer{padding:14px 24px;border-top:1px solid var(--rule);font-size:11.5px;color:var(--mute)}
@media(max-width:900px){.two{grid-template-columns:1fr}.rail{border-right:0;padding-right:0}.hr{text-align:left}.panel{padding:16px}}
</style>
</head>
<body>
<header class="top">
 <div class="hl">
  <p class="lab">WIKI · neurotechnology and justice</p>
  <h1>Research wiki: neurotechnology in the administration of justice</h1>
  <p id="hsub" class="sub"></p>
 </div>
 <div class="hr">
  <p id="strip" class="lab" aria-live="polite"></p>
  <p class="lab">This page has no storage: changes live in it until you download them (tab 05)</p>
 </div>
</header>
<div id="tabs" role="tablist" aria-label="Wiki workspace, five tabs"></div>
<main>
 <section id="pan0" class="panel" role="tabpanel" aria-labelledby="tab0">
  <div class="two">
   <aside class="rail" aria-label="List of pages">
    <label for="flt" class="lab">title, tag or slug</label>
    <input id="flt" type="search" autocomplete="off">
    <p id="cnt" class="cnt"></p>
    <p class="how">How this is computed: pages whose title, slug or tags contain the text, counted by this page.</p>
    <p><a href="#index" class="lab">Show the index</a></p>
    <div id="plist"></div>
   </aside>
   <article id="pmain" class="pmain"></article>
  </div>
 </section>
 <section id="pan1" class="panel" role="tabpanel" aria-labelledby="tab1" hidden>
  <p class="lab">02 · What does the wiki answer, and is it worth filing?</p>
  <div class="narrow">
   <label for="q" class="lbl">Your question about the wiki</label>
   <textarea id="q" rows="3" placeholder="For example: does anything in the library say existing rights are enough?"></textarea>
   <p class="row"><button id="askBtn" type="button" class="btn pri">Ask the wiki</button><button id="askStop" type="button" class="btn" hidden>Stop</button><span class="hint">Enter sends · Shift+Enter makes a new line</span></p>
   <div id="askSend" class="grey" aria-live="polite"></div>
   <p id="askProg" class="prog" aria-live="polite"></p>
   <div id="askErr"></div><div id="askPages"></div><div id="askOut"></div><div id="askFile"></div>
  </div>
 </section>
 <section id="pan2" class="panel" role="tabpanel" aria-labelledby="tab2" hidden>
  <p class="lab">03 · What would the waiting document change?</p>
  <div id="ingBox" class="narrow"></div>
 </section>
 <section id="pan3" class="panel" role="tabpanel" aria-labelledby="tab3" hidden><div id="chkBox" class="narrow"></div></section>
 <section id="pan4" class="panel" role="tabpanel" aria-labelledby="tab4" hidden><div id="recBox" class="narrow"></div></section>
</main>
<footer id="foot"></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{};
const $=(s,r)=>(r||document).querySelector(s);
const $$=(s,r)=>Array.from((r||document).querySelectorAll(s));
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
if(!WD.wiki||!WD.library){document.body.innerHTML='<main style="padding:24px;max-width:640px"><p class="lab">NO WIKI ATTACHED</p><p>This workspace needs the research wiki and the library. Drag "Research wiki: neurotechnology and justice" from "Your files" into the chat, then ask again.</p></main>';return;}
const WIKI=WD.wiki,LIB=WD.library.records||[];
const FENCE=String.fromCharCode(96).repeat(3);
const INS0='<'+'!--ins-->',INS1='<'+'!--/ins-->';
const INS0_RE=new RegExp('^'+INS0+'\\s*$'),INS1_RE=new RegExp('^'+INS1+'\\s*$'),INS_ALL=new RegExp(INS0+'([\\s\\S]*?)'+INS1,'g');
const PIN_SRC='\\[([^\\]]+)\\]\\(pin:([^#\\s)]+)#p(\\d+)(?: "([^"]*)")?\\) ?(✓|⚠)';
const INL_SRC=PIN_SRC+'|\\[\\[([^\\]|#]+)(?:[|#][^\\]]*)?\\]\\]|\\[([^\\]]+)\\]\\((https?:[^)\\s]+)\\)';
const REGN={a:'treaty law',b:'General Comments',c:'UN, agency and soft-law reports',d:'national human rights institution',e:'civil society',f:'scholarship'};
const REGS={a:'treaty law',b:'General Comment',c:'UN report',d:'NHRI report',e:'civil society',f:'scholarship'};
const REGW={a:5,b:4,c:3,d:2,e:1,f:.5};
const PLU={source:'sources',concept:'concepts',entity:'entities',question:'questions'};
const SEC={source:/^#{1,4}\s*sources?\b/i,concept:/^#{1,4}\s*concepts?\b/i,entity:/^#{1,4}\s*(entity|entities)\b/i,question:/^#{1,4}\s*questions?\b/i};
const PIN_RULE='A pin has the form [label](pin:DOCUMENT_ID#pPDFPAGE "verbatim quote") ✓ and is a quotation that stands inside the sentence. Quote only words that stand in the passages given; the code will check every quote against the library and strike out what does not match. Never put a straight double quote inside a quote. Name the register where it matters and keep the document\'s own verb; never present what a (c) to (f) document says as what the treaty requires.';

const fmt=n=>Number(n||0).toLocaleString('en-US');
const today=()=>new Date().toISOString().slice(0,10);
const clone=o=>JSON.parse(JSON.stringify(o));
const uniq=a=>Array.from(new Set(a));
const slugify=s=>String(s).toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const escRe=s=>String(s).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const sameSet=(a,b)=>{a=new Set(a);b=new Set(b);return a.size===b.size&&Array.from(a).every(x=>b.has(x));};

/* ---------- data ---------- */
const DOC={};LIB.forEach(d=>{DOC[d.id]=Object.assign({},d,{passages:d.passages||[]});});
const P=[],PM=new Map(),ORIG={};
const addPage=p=>{p.fm=p.fm||{};['tags','register','links','sources'].forEach(k=>{p.fm[k]=p.fm[k]||[];});P.push(p);PM.set(p.slug,p);return p;};
(WIKI.pages||[]).forEach(p=>{addPage({slug:p.slug,type:p.type,title:p.title,fm:clone(p.frontmatter||{}),body:p.body||''});ORIG[p.slug]=p.body||'';});
const pg=s=>PM.get(s);
const S={tab:0,cur:null,flt:'',calls:0,passages:0,changes:[],callLog:[],running:null,stop:false,index:WIKI.index||'',log:WIKI.log||'',tens:WIKI.tensions||'',logBase:0,logAdded:0,op:0,order:'new',lintPressed:false,filing:null,tensNew:[],sel:null,warn0:0};

function parsePins(t){return Array.from(String(t).matchAll(new RegExp(PIN_SRC,'g')),m=>({label:m[1],id:m[2],page:+m[3],quote:m[4],mark:m[5],raw:m[0]}));}
function an(p){if(p._k!==p.body){p._k=p.body;p._links=Array.from(p.body.matchAll(/\[\[([^\]|#]+)/g),m=>m[1].trim());p._pins=parsePins(p.body);}return p;}
const backlinks=slug=>P.filter(p=>p.slug!==slug&&an(p)._links.includes(slug));
const pinKey=x=>x.id+'#p'+x.page+'|'+(x.quote||'');
const pinDocs=p=>uniq(an(p)._pins.map(x=>x.id));

/* ---------- verification ---------- */
function norm(s){return String(s==null?'':s).normalize('NFKC').replace(/[\u201C\u201D\u201E]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2014]/g,'-').replace(/\u00AD/g,'').replace(/-\s+/g,'').replace(/\s+/g,' ').trim();}
const VC=new Map();
function verify(pin,inbox){
  const k=(inbox?'i|':'n|')+pinKey(pin)+'|'+pin.label;
  if(!VC.has(k))VC.set(k,verify0(pin,inbox));
  return VC.get(k);
}
function verify0(pin,inbox){
  const d=DOC[pin.id];
  if(!d)return{ok:false,reason:'unknown document "'+pin.id+'"'};
  if(d.status==='inbox'&&!inbox)return{ok:false,reason:'the document is still in the inbox, not read into the wiki'};
  if(!pin.quote)return{ok:false,reason:'the pin has no quote'};
  const fr=String(pin.quote).split(/…|\.\.\./).map(norm).filter(Boolean);
  if(!fr.length)return{ok:false,reason:'the quote is empty'};
  const cand=d.passages.filter(x=>x.page===pin.page);
  if(!cand.length)return{ok:false,reason:'no passage of '+pin.id+' starts on PDF page '+pin.page};
  let lm=null;
  for(const x of cand){
    const t=norm(x.text);let pos=0,ok=true;
    for(const f of fr){const i=t.indexOf(f,pos);if(i<0){ok=false;break;}pos=i+f.length;}
    if(!ok)continue;
    const want=x.paragraph?'para. '+x.paragraph:'p. '+x.page_label;
    if(new RegExp(escRe(want)+'(?!\\w)').test(pin.label))return{ok:true,passage:x};
    lm={ok:false,label:true,reason:'the quote is in '+want+' but the label says "'+pin.label+'"',passage:x};
  }
  return lm||{ok:false,reason:'the quote is not in any passage that starts on PDF page '+pin.page};
}
const pinCount=p=>an(p)._pins.filter(x=>verify(x).ok).length;
function pinStats(){
  let total=0,ok=0,failMarked=0,warn=0,label=0;const fp=new Set();
  P.forEach(p=>an(p)._pins.forEach(x=>{total++;const v=verify(x);if(v.ok)ok++;else{if(x.mark==='✓'){failMarked++;fp.add(p.slug);}if(v.label)label++;}if(x.mark==='⚠')warn++;}));
  return{total,ok,failMarked,warn,label,failPages:Array.from(fp)};
}
function docReg(id){
  const s=P.find(p=>p.type==='source'&&sameSet(p.fm.sources,[id]))||pg(slugify(id))||P.find(p=>p.fm.status==='stub'&&p.fm.sources.includes(id));
  return s&&s.fm.register&&s.fm.register.length?s.fm.register:[];
}
function citeAs(id){
  const d=DOC[id],cnt={};
  P.forEach(p=>an(p)._pins.forEach(x=>{if(x.id===id){const m=x.label.match(/^(.*?),\s*(?:para\.|p\.)/);if(m)cnt[m[1]]=(cnt[m[1]]||0)+1;}}));
  const best=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a])[0];
  return best||(d&&d.symbol)||(d?d.author+' '+d.year:id);
}
const curly=q=>String(q).replace(/"([^"]*)"/g,'\u201C$1\u201D').replace(/"/g,'\u201D');
function makePin(doc,p,quote,cite){
  const label=cite+(p.paragraph?', para. '+p.paragraph:', p. '+p.page_label),q=curly(quote);
  return{label,id:doc.id,page:p.page,quote:q,mark:'✓',raw:'['+label+'](pin:'+doc.id+'#p'+p.page+' "'+q+'") ✓'};
}

/* ---------- rendering of pins, markdown, contested cards ---------- */
const PR=[];
function pinHtml(pin,ctx){
  ctx=ctx||{};
  const v=verify(pin,ctx.inbox);let ok=v.ok,why=v.reason,struck=false;
  if(ctx.sent&&!ctx.sent.has(pinKey(pin))){ok=false;struck=true;why='not on the pages sent';}
  const k=PR.push({pin,v})-1,reg=docReg(pin.id)[0]||'?';
  const says=!struck&&((ok&&pin.mark==='⚠')||(!ok&&pin.mark==='✓'));
  const x=v.passage;
  let det=x?'<b>'+(x.paragraph?'para. '+esc(x.paragraph):'p. '+esc(x.page_label))+'</b> (PDF page '+x.page+'): '+esc(x.text.slice(0,300))+(x.text.length>300?'…':''):'';
  if(!ok)det=(det?det+'<br>':'')+'<b>Not verified:</b> '+esc(why||'')+'. Footnotes, tables and captions are not in the passages, so a pin on them cannot verify.';
  det+=' <button type="button" class="lk" data-act="open" data-k="'+k+'">Open the PDF page</button>';
  const q=pin.quote?'\u201C'+esc(pin.quote)+'\u201D':'(this pin has no quote)';
  return '<span class="pq'+(struck?' x':'')+'">'+q+'</span><span class="chip '+(struck?'struck':ok?'':'bad')+'"><button type="button" class="cl" data-act="open" data-k="'+k+'" aria-label="Open '+esc(pin.label)+' at PDF page '+pin.page+'">'+esc(pin.label)+'</button><span class="rg" title="'+esc(REGN[reg]||'register unknown')+'">('+esc(reg)+')</span><span class="st">'+(struck?'not on the pages sent':ok?'✓ verified':'⚠ not found')+'</span>'+(says?'<span class="says">page says '+esc(pin.mark)+'</span>':'')+'<button type="button" class="tg" data-act="tg" data-k="'+k+'" aria-expanded="false" aria-label="Show the passage behind '+esc(pin.label)+'">▸</button></span><span class="pd" id="pd'+k+'" hidden>'+det+'</span>';
}
function wikiLink(s,ctx){const t=pg(s);if(t||(ctx.known&&ctx.known.has(s)))return '<a href="#'+encodeURIComponent(s)+'">'+esc(t?t.title:s)+'</a>';return '<span class="dang">'+esc(s)+' <small>no page</small></span>';}
function fmtText(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/(^|[^*])\*([^*\s][^*]*?)\*(?!\*)/g,'$1<em>$2</em>');}
function inline(t,ctx){
  ctx=ctx||{};const re=new RegExp(INL_SRC,'g');let out='',last=0,m;t=String(t==null?'':t);
  while((m=re.exec(t))){
    out+=fmtText(t.slice(last,m.index));
    if(m[1]!==undefined)out+=pinHtml({label:m[1],id:m[2],page:+m[3],quote:m[4],mark:m[5]},ctx);
    else if(m[6]!==undefined)out+=wikiLink(m[6].trim(),ctx);
    else out+='<a href="'+esc(m[8])+'" target="_blank" rel="noopener">'+esc(m[7])+'</a>';
    last=re.lastIndex;
  }
  return out+fmtText(t.slice(last));
}
function parseCard(txt){
  const c={claim:'',verdict:'',note:'',pos:[]};
  String(txt).split('\n').forEach(l=>{
    let m;
    if((m=l.match(/^claim:\s*(.*)$/)))c.claim=m[1];
    else if((m=l.match(/^verdict:\s*(.*)$/)))c.verdict=m[1].trim();
    else if((m=l.match(/^note:\s*(.*)$/)))c.note=m[1];
    else if((m=l.match(/^([+\-~])\s*([a-f])\s*\|\s*(.*)$/))){
      const rest=m[3],pm=new RegExp(PIN_SRC).exec(rest);let pin=null,after=rest;
      if(pm){pin={label:pm[1],id:pm[2],page:+pm[3],quote:pm[4],mark:pm[5]};after=rest.slice(pm.index+pm[0].length);}
      const parts=after.replace(/^\s*\|\s*/,'').split(/\s*\|\s*/),pgl=(parts.pop()||'').trim();
      c.pos.push({sign:m[1],reg:m[2],pin,gloss:parts.join(' | ').trim(),page:pgl});
    }
  });
  return c;
}
function tensEntries(){return S.tens.split(/^(?=### )/m).filter(s=>/^### /.test(s));}
const tensId=t=>slugify(t.split('\n')[0].replace(/^###\s*/,''));
function tensFor(slug){return tensEntries().filter(t=>{const m=t.match(/card:\s*\[\[([^\]|#]+)/);return m&&m[1].trim()===slug;}).map(tensId);}
function cardHtml(txt,ctx){
  const c=parseCard(txt);let wp=0,wt=0;
  c.pos.forEach(x=>{const w=REGW[x.reg]||0;wt+=w;wp+=x.sign==='+'?w:x.sign==='~'?w/2:0;});
  const lean=wt?Math.round(100*wp/wt):0,SG={'+':'supports','-':'contests','~':'mixed'},tl=ctx.page?tensFor(ctx.page):[];
  const rows=c.pos.map(x=>'<tr><td>'+SG[x.sign]+'</td><td>('+esc(x.reg)+') '+esc(REGS[x.reg]||'')+'</td><td>'+(x.pin?pinHtml(x.pin,ctx):'')+'</td><td>'+inline(x.gloss,ctx)+'</td><td>'+(x.page?inline(x.page,ctx):'')+'</td></tr>').join('');
  return '<section class="card'+(ctx.diff&&ctx.ins?' ins':'')+'" aria-label="Contested claim"><p class="lab">Contested claim</p><h4 class="claim">'+inline(c.claim,ctx)+'</h4><p class="verdict">'+esc(c.verdict.replace(/-/g,' ')||'no verdict')+'</p><p>'+inline(c.note,ctx)+'</p>'
   +'<p class="lab">FIG.01 · Lean bar</p><div class="bar" role="img" aria-label="Support '+lean+' percent of weighted positions"><i style="width:'+lean+'%"></i></div>'
   +'<p class="how">descriptive: support '+lean+'% of weighted positions, weights a 5 · b 4 · c 3 · d 2 · e 1 · f ½; the verdict is the answer</p>'
   +'<div class="tw"><table><caption>Positions on this claim</caption><thead><tr><th scope="col">Position</th><th scope="col">Register</th><th scope="col">Pin</th><th scope="col">Gloss</th><th scope="col">Page</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
   +(tl.length?'<p><button type="button" class="lk" data-act="tens" data-id="'+esc(tl[0])+'">in the tensions register</button></p>':'')+'</section>';
}
function md(body,ctx){
  ctx=ctx||{};const out=[];let ins=false,h1done=false;
  const parts=String(body).split(new RegExp(FENCE+'contested\\n?([\\s\\S]*?)'+FENCE));
  parts.forEach((seg,i)=>{
    if(i%2){ctx.ins=ins;out.push(cardHtml(seg,ctx));return;}
    let para=[],list=null;
    const cls=()=>ctx.diff?(ins?' class="ins"':' class="dim"'):'';
    const fP=()=>{if(para.length){out.push('<p'+cls()+'>'+inline(para.join(' '),ctx)+'</p>');para=[];}};
    const fL=()=>{if(list){out.push('<'+list.t+cls()+'>'+list.items.map(x=>'<li>'+inline(x,ctx)+'</li>').join('')+'</'+list.t+'>');list=null;}};
    seg.split('\n').forEach(line=>{
      let m;
      if(INS0_RE.test(line)){fP();fL();ins=true;return;}
      if(INS1_RE.test(line)){fP();fL();ins=false;return;}
      if(!line.trim()){fP();fL();return;}
      if((m=line.match(/^(#{1,4})\s+(.*)$/))){
        fP();fL();
        if(m[1].length===1&&!h1done&&ctx.skipH1){h1done=true;return;}
        const n=[3,3,4,5][m[1].length-1];out.push('<h'+n+cls()+'>'+inline(m[2],ctx)+'</h'+n+'>');return;
      }
      if((m=line.match(/^\s*([-*]|\d+\.)\s+(.*)$/))){fP();const t=/\d/.test(m[1])?'ol':'ul';if(list&&list.t!==t)fL();list=list||{t,items:[]};list.items.push(m[2]);return;}
      fL();para.push(line.trim());
    });
    fP();fL();
  });
  return out.join('');
}
function toMd(p){
  const f=p.fm,y=a=>'['+(a||[]).join(', ')+']';
  return '---\ntitle: "'+String(p.title).replace(/"/g,'\\"')+'"\ntype: '+p.type+'\ntags: '+y(f.tags)+'\nregister: '+y(f.register)+'\nstatus: '+(f.status||'')+'\nupdated: '+(f.updated||'')+'\nlinks: '+y(f.links)+'\nsources: '+y(f.sources)+'\n---\n\n'+p.body.replace(new RegExp(INS0+'\\n?|'+INS1+'\\n?','g'),'');
}
function firstSentence(a){
  const para=String(a).trim().split(/\n\s*\n/)[0].replace(/\n/g,' '),flat=para.replace(new RegExp(PIN_SRC,'g'),''),m=flat.match(/^.*?[.!?](?=\s|$)/);
  return(m?m[0]:flat).replace(/\s+/g,' ').trim();
}

/* ---------- lint and checks ---------- */
function lint(){
  const names=new Set(P.map(p=>p.slug)),R=[];
  const row=(label,items)=>R.push({label,items,pages:uniq(items.map(i=>i.p))});
  const il=Array.from(S.index.matchAll(/^\s*[-*]\s*\[\[([^\]|#]+)\]\]([^\n]*)/gm),m=>({s:m[1].trim(),t:m[2]})),is=new Set(il.map(x=>x.s));
  const bad=[];P.forEach(p=>an(p)._pins.forEach(x=>{if(!verify(x).ok)bad.push({p:p.slug,mark:x.mark});}));
  const tc=tensEntries().map(t=>{const m=t.match(/card:\s*\[\[([^\]|#]+)/);return m?m[1].trim():null;}).filter(Boolean);
  const cards=p=>p.body.split(FENCE+'contested').length-1;
  row('Dangling links',P.flatMap(p=>an(p)._links.filter(s=>!names.has(s)).map(s=>({p:p.slug}))));
  row('Orphan pages (nothing links to them)',P.filter(p=>!backlinks(p.slug).length).map(p=>({p:p.slug})));
  row('Pins not verified by this page',bad);
  row('Pins marked ✓ that fail',bad.filter(b=>b.mark==='✓'));
  row('Pages whose sources differ from the documents pinned',P.filter(p=>!sameSet(p.fm.sources,pinDocs(p))).map(p=>({p:p.slug})));
  row('Pages with no pins',P.filter(p=>!an(p)._pins.length).map(p=>({p:p.slug})));
  row('Links not reciprocated',P.flatMap(p=>p.fm.links.filter(s=>pg(s)&&!pg(s).fm.links.includes(p.slug)).map(()=>({p:p.slug}))));
  row('Pages missing from the index',P.filter(p=>!is.has(p.slug)).map(p=>({p:p.slug})));
  row('Index lines without a page',il.filter(x=>!names.has(x.s)).map(x=>({p:x.s})));
  row('Index ✓N that differs from the computed count',il.filter(x=>{const m=x.t.match(/✓\s*(\d+)\s*$/);return pg(x.s)&&m&&+m[1]!==pinCount(pg(x.s));}).map(x=>({p:x.s})));
  row('Contested cards without a tensions entry',P.filter(p=>cards(p)>tc.filter(s=>s===p.slug).length).map(p=>({p:p.slug})));
  row('Tensions entries without a contested card',uniq(tc).filter(s=>!pg(s)||cards(pg(s))<tc.filter(x=>x===s).length).map(s=>({p:s})));
  row('Stub pages',P.filter(p=>p.fm.status==='stub').map(p=>({p:p.slug})));
  row('Pins to a document still in the inbox',P.flatMap(p=>an(p)._pins.filter(x=>DOC[x.id]&&DOC[x.id].status==='inbox').map(()=>({p:p.slug}))));
  return R;
}
const lintNums=()=>lint().map(r=>r.items.length);
function changedSlugs(){return P.filter(p=>ORIG[p.slug]!==p.body).map(p=>p.slug);}
function checks(){
  const st=pinStats(),L=lint(),out=[],n=l=>(L.find(r=>r.label.indexOf(l)===0)||{items:[]}).items.length;
  const add=(name,ok,text,pages)=>out.push({name,ok,text,pages:pages||[]});
  const stated=(S.index.match(/(\d[\d,]*) pins/)||[])[1],sn=stated?+stated.replace(/,/g,''):null;
  add('Pins',sn===st.total&&st.ok===st.total&&!st.failMarked,'found '+fmt(st.total)+' by the regular expression, the index states '+(stated||'no number')+'; verified '+fmt(st.ok)+' of '+fmt(st.total)+'; marked ✓ but failing: '+st.failMarked,st.failPages);
  add('Labels',st.label===0,st.label+' pin(s) whose quote is found but whose label names another paragraph or page');
  const sd=[n('Dangling'),n('Orphan'),n('Pages whose sources'),n('Pages missing')+n('Index lines'),n('Contested')+n('Tensions')];
  add('Structure',sd.every(x=>x===0),'dangling links '+sd[0]+'; orphans '+sd[1]+'; sources differing from pinned documents '+sd[2]+'; index mismatches '+sd[3]+'; contested cards against tensions entries '+sd[4]);
  const ca=S.callLog;
  if(!ca.length)add('Model answers',null,'no call to the model yet');
  else{
    const bad=ca.filter(c=>!c.ok).length,unk=[].concat(...ca.map(c=>c.unknown||[])),tk=ca.filter(c=>c.tk),r=tk.reduce((a,c)=>a+c.tk.returned,0),v=tk.reduce((a,c)=>a+c.tk.ok,0),f=tk.reduce((a,c)=>a+c.tk.failed,0),d=tk.reduce((a,c)=>a+c.tk.dropped,0);
    add('Model answers',bad===0&&r===v+f+d,ca.length+' calls, '+(ca.length-bad)+' parsed as JSON; slugs that do not exist: '+(unk.length?unk.join(', '):'none')+(tk.length?'; takeaways returned '+r+' = verified '+v+' + could not verify '+f+' + dropped '+d:''));
  }
  if(!ING)add('Coverage',null,'no ingest started');
  else{const tot=ING.doc.passages.length;add('Coverage',ING.sent===tot?true:(ING.stopped?false:null),'passages sent '+ING.sent+' of '+tot+'; takeaways naming a passage that was not sent were dropped: '+ING.dropped);}
  const ch=changedSlugs(),allOk=ch.every(s=>an(pg(s))._pins.every(x=>verify(x).ok));
  add('Unverified',st.warn===S.warn0&&allOk&&st.failMarked===0,'⚠ marks in the wiki: '+st.warn+' (at load: '+S.warn0+'); every pin in a changed page verifies: '+(allOk?'yes':'no'),ch);
  const ap=uniq(S.changes.map(c=>c.slug));
  add('Approval',sameSet(ch,ap),ch.length+' page(s) differ from the loaded wiki; '+ap.length+' approved or filed here'+(ING&&ING.filed?'; the log entry names approved and rejected pages by slug':''),ch);
  if(!S.filing)add('Filing',null,'nothing filed yet');
  else{
    const f=S.filing,okp=f.slugs.every(s=>pg(s)&&an(pg(s))._pins.every(x=>verify(x).ok)),oki=f.slugs.every(s=>{const m=S.index.match(new RegExp('\\[\\['+escRe(s)+'\\]\\][^\\n]*✓\\s*(\\d+)'));return !m||+m[1]===pinCount(pg(s));});
    const le=logEntries().pop(),okl=le&&f.slugs.every(s=>(le.head+le.body).indexOf('[['+s+']]')>=0||le.head.indexOf(pg(s).title)>=0);
    add('Filing',okp&&oki&&!!okl,'changed pages re-verified: '+(okp?'yes':'no')+'; index counts equal pin counts: '+(oki?'yes':'no')+'; last log entry names them: '+(okl?'yes':'no')+'; lint checks needing a look: before '+f.before.filter(x=>x).length+', after '+f.after.filter(x=>x).length,f.slugs);
  }
  const ops=uniq(S.changes.map(c=>c.op)).length;
  add('Session',ops===S.logAdded&&exportObj().pages.length===P.length,S.changes.length+' page change(s) in '+ops+' filing(s); log entries added this session: '+S.logAdded+'; the download holds '+exportObj().pages.length+' pages, the wiki '+P.length);
  return out;
}

/* ---------- header, tabs, list, page ---------- */
const TN=['PAGES','ASK','INGEST','CHECK','RECORD'];
function renderHeader(){
  const c={};P.forEach(p=>{c[p.type]=(c[p.type]||0)+1;});const st=pinStats(),inbox=Object.keys(DOC).filter(k=>DOC[k].status==='inbox').length;
  const parts=['source','concept','entity','question'].map(t=>(c[t]||0)+' '+(c[t]===1?t:PLU[t]));
  $('#hsub').textContent=P.length+' pages ('+parts.join(', ')+') · '+fmt(st.total)+' pins, '+fmt(st.ok)+' verified by this page · '+LIB.length+' documents, '+inbox+' in the inbox · built '+(WIKI.built||'unknown');
  $('#strip').textContent='Changes this session: '+S.changes.length+' · Calls to the model: '+S.calls+' · Passages that left the browser: '+S.passages;
}
function setRun(i,on){const b=$('#tab'+i+' .run');if(b)b.textContent=on?' · running':'';}
function showTab(i,focus){
  S.tab=i;
  $$('#tabs [role=tab]').forEach((b,j)=>{b.setAttribute('aria-selected',i===j);b.tabIndex=i===j?0:-1;});
  $$('.panel').forEach((x,j)=>{x.hidden=i!==j;});
  if(i===2)renderIngest();if(i===3)renderCheck();if(i===4)renderRecord();
  if(focus)$('#tab'+i).focus();
}
function renderList(){
  const f=S.flt.trim().toLowerCase();
  const m=P.filter(p=>!f||p.title.toLowerCase().indexOf(f)>=0||p.slug.indexOf(f)>=0||p.fm.tags.join(' ').toLowerCase().indexOf(f)>=0);
  $('#cnt').innerHTML='<span class="big">'+m.length+'</span> of '+P.length+' pages';
  const types=uniq(['source','concept','entity','question'].concat(P.map(p=>p.type)));
  $('#plist').innerHTML=types.map(t=>{
    const L=m.filter(p=>p.type===t);if(!L.length)return '';
    return '<h3 class="lab grp">'+esc(t)+' · '+L.length+'</h3><ul class="plist">'+L.map(p=>'<li><a href="#'+encodeURIComponent(p.slug)+'"'+(p.slug===S.cur?' aria-current="page"':'')+'>'+esc(p.title)+'</a><br><span class="meta">'+(p.fm.register.join(' ')||'–')+' · '+an(p)._pins.length+' pins'+(p.fm.status==='stub'?' <span class="stub">stub</span>':'')+'</span></li>').join('')+'</ul>';
  }).join('')||'<p class="hint">No page matches.</p>';
}
function renderPage(){
  const el=$('#pmain');
  if(!S.cur){el.innerHTML='<p class="lab">INDEX</p><h2>Index of the wiki</h2><p class="hint">The catalog the wiki keeps, shown as written. Choose a page on the left; pins open the PDF beside this app.</p><div class="page">'+md(S.index,{skipH1:true})+'</div>';return;}
  const p=pg(S.cur);
  if(!p){el.innerHTML='<p class="lab">NO SUCH PAGE</p><h2>There is no page called "'+esc(S.cur)+'"</h2><p><a href="#index">Back to the index</a></p>';return;}
  an(p);
  const bl=backlinks(p.slug),inB=new Set(p._links),f=p.fm;
  const regs=f.register.map(r=>'<span class="badge">('+esc(r)+') '+esc(REGN[r]||'?')+'</span>').join('');
  const out=f.links.map(s=>'<li>'+(pg(s)?'<a href="#'+encodeURIComponent(s)+'">'+esc(pg(s).title)+'</a>':'<span class="dang">'+esc(s)+' <small>no page</small></span>')+(inB.has(s)?'':' <span class="hint">frontmatter only</span>')+'</li>').join('');
  const src=f.sources.map(id=>{const d=DOC[id];return d?'<li><b>'+esc(d.short_title||d.title)+'</b> · '+esc(d.kind)+' · '+esc(d.year)+' · <a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.symbol||id)+'</a>'+(d.status==='inbox'?' <span class="stub">inbox</span>':'')+'</li>':'<li>'+esc(id)+' <span class="hint">not in the library</span></li>';}).join('');
  el.innerHTML='<p class="lab">PAGE · '+esc(p.slug)+'</p><h2>'+esc(p.title)+'</h2><p><span class="badge">'+esc(p.type)+'</span>'+regs+'<span class="badge">'+esc(f.status||'no status')+'</span><span class="badge">updated '+esc(f.updated||'?')+'</span></p><p class="meta">'+f.tags.map(esc).join(' · ')+'</p>'
   +'<div class="page">'+md(p.body,{page:p.slug,skipH1:true})+'</div>'
   +'<h3>Links out</h3><ul>'+(out||'<li class="hint">none</li>')+'</ul><h3>Linked from</h3><ul>'+(bl.map(b=>'<li><a href="#'+encodeURIComponent(b.slug)+'">'+esc(b.title)+'</a></li>').join('')||'<li class="hint">no page links here</li>')+'</ul>'
   +'<h3>Sources</h3><ul>'+(src||'<li class="hint">none</li>')+'</ul><p><button type="button" class="btn" data-act="copy-md">Copy page as markdown</button> <span id="cpnote" class="hint" aria-live="polite"></span></p>';
}
function onHash(){
  const h=decodeURIComponent(location.hash.replace(/^#/,''));
  S.cur=h&&h!=='index'?h:null;showTab(0);renderList();renderPage();window.scrollTo(0,0);
}

/* ---------- calls to the model ---------- */
function parseJSON(r){
  if(r&&typeof r==='object')return r;
  const s=String(r==null?'':r).trim();
  try{return JSON.parse(s);}catch(e){}
  const m=s.match(/\x60{3}(?:json)?\s*([\s\S]*?)\x60{3}/);
  if(m){try{return JSON.parse(m[1]);}catch(e){}}
  return undefined;
}
async function callModel(prompt,label,npass,say,what){
  if(typeof studio==='undefined'||!studio.ask)throw new Error('The studio is not connected, so the model cannot be asked.');
  S.calls++;S.passages+=npass;renderHeader();
  const rec={label,chars:prompt.length,passages:npass,ok:false};S.callLog.push(rec);
  say(what+': '+fmt(prompt.length)+' characters and '+npass+' passage objects are leaving the browser. Waiting for the model…');
  const raw=await studio.ask(prompt,{json:true}),v=parseJSON(raw);
  if(v===undefined||v===null){const e=new Error('The answer was not valid JSON.');e.raw=raw;throw e;}
  rec.ok=true;return v;
}
function failHtml(err){return '<div class="warn" role="alert"><b>'+esc(err.e.message||'Error')+'</b>'+(err.e.raw!=null?'<p class="hint">Raw answer, nothing was used:</p><pre>'+esc(String(err.e.raw).slice(0,3000))+'</pre>':'')+'<button type="button" class="btn" data-act="retry">Retry</button></div>';}
let RETRY=null;
function showFail(el,e,fn){RETRY=fn;el.innerHTML=failHtml({e});}
function openSrc(pin){
  try{studio.openSource(pin.id,pin.page,pin.quote||'');}
  catch(e){const n=$('#strip');n.textContent='The studio could not open the PDF here.';}
}
function copyText(t,note){
  const done=ok=>{note.textContent=ok?'Copied.':'Could not copy; select the text and copy it by hand.';};
  const fb=()=>{const a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();let ok=false;try{ok=document.execCommand('copy');}catch(e){}a.remove();done(ok);};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(()=>done(true),fb);else fb();
}

/* ---------- index, log and tensions editing ---------- */
function idxSet(slug,line,secRe,secName){
  const L=S.index.split('\n'),i=L.findIndex(l=>new RegExp('^\\s*[-*]\\s*\\[\\['+escRe(slug)+'\\]\\]').test(l));
  if(i>=0)L[i]=line;
  else{
    const h=L.findIndex(l=>secRe.test(l));
    if(h<0)L.push('','## '+secName,line);
    else{let e=h+1;while(e<L.length&&!/^#{1,4}\s/.test(L[e]))e++;while(e>h+1&&!L[e-1].trim())e--;L.splice(e,0,line);}
  }
  S.index=L.join('\n');
}
function idxRecount(slug,N){S.index=S.index.split('\n').map(l=>new RegExp('^\\s*[-*]\\s*\\[\\['+escRe(slug)+'\\]\\]').test(l)?(/✓\s*\d+/.test(l)?l.replace(/✓\s*\d+/,'✓'+N):l):l).join('\n');}
function idxCounts(){
  const L=S.index.split('\n'),i=L.findIndex(l=>/\d[\d,]* pins/.test(l));if(i<0)return;
  const c={};P.forEach(p=>{c[p.type]=(c[p.type]||0)+1;});let l=L[i].replace(/\d[\d,]*( pins)/,fmt(pinStats().total)+'$1').replace(/\d+( pages)/,P.length+'$1');
  [['source','sources?'],['concept','concepts?'],['entity','(?:entity|entities)'],['question','questions?']].forEach(a=>{l=l.replace(new RegExp('\\d+( '+a[1]+')'),(c[a[0]]||0)+'$1');});
  L[i]=l;S.index=L.join('\n');
}
function addLog(e){S.log=S.log.replace(/\s+$/,'')+'\n\n'+e+'\n';S.logAdded++;}
function logEntries(){return S.log.split(/^(?=## )/m).filter(s=>/^## /.test(s)).map(s=>{const i=s.indexOf('\n');return{head:s.slice(3,i<0?undefined:i).trim(),body:i<0?'':s.slice(i+1).trim()};});}

/* ---------- 02 ASK ---------- */
const ASK={pages:[],manual:false,res:null,sent:null,bad:0,n:0,fileOpen:false,filed:null};
function askPlan(){
  const q=$('#q').value.trim().length;
  $('#askSend').innerHTML='<b>What will leave this browser</b> when you press <i>'+(ASK.res?'Ask again':'Ask the wiki')+'</i>. Step 1: the index ('+fmt(S.index.length)+' characters) and your question ('+q+' characters); the model returns up to five page slugs. Step 2: the full text of those pages and your question, announced here with exact numbers before it goes. 0 library passages are sent from this tab.';
}
async function doAsk(){
  if(S.running)return;
  const q=$('#q').value.trim(),say=t=>{$('#askProg').textContent=t;};
  if(!q){say('Type a question first.');$('#q').focus();return;}
  S.running='ask';S.stop=false;setRun(1,true);$('#askStop').hidden=false;$('#askBtn').disabled=true;$('#askErr').innerHTML='';
  let stage=1;
  try{
    if(!(ASK.manual&&ASK.pages.length)){
      const prompt='You are the librarian of a research wiki on neurotechnology in the administration of justice. Below are the wiki\'s index (one line per page) and a question. Return JSON {"pages":["slug", ...]}: the slugs of at most five pages most likely to answer the question. Use only slugs that appear in the index.\n\nINDEX\n'+S.index+'\n\nQUESTION\n'+q;
      const r=await callModel(prompt,'ask · pages',0,say,'Step 1, the index and your question');
      if(S.stop)throw new Error('stopped');
      const asked=(r&&Array.isArray(r.pages)?r.pages:[]).map(String);
      S.callLog[S.callLog.length-1].unknown=asked.filter(s=>!pg(s));
      ASK.pages=uniq(asked.filter(s=>pg(s))).slice(0,5);
      if(!ASK.pages.length)throw new Error('The model named no page that exists in this wiki.');
    }
    ASK.manual=false;renderAskPages();stage=2;
    const pages=ASK.pages.map(pg),chars=pages.reduce((a,p)=>a+p.body.length,0);
    $('#askSend').innerHTML='<b>Step 2 is sending:</b> '+pages.length+' pages, '+fmt(chars)+' characters; 0 library passages have left the browser. The pages: '+pages.map(p=>esc(p.title)).join('; ')+'.';
    const prompt='Answer the question using ONLY the wiki pages below. Return JSON {"title":"a short page title","answer":"markdown, at most 350 words","cannot_answer":"what these pages cannot answer, in one or two sentences"}. Build the answer around pins copied exactly from the pages; link other pages as [[slug]]. '+PIN_RULE+' Registers: (a) treaty law, (b) General Comments, (c) UN, agency and soft-law reports, (d) national human rights institution, (e) civil society, (f) scholarship.\n\nQUESTION\n'+q+'\n\nPAGES\n'+pages.map(p=>'### '+p.slug+' — '+p.title+'\n'+p.body).join('\n\n');
    const r2=await callModel(prompt,'ask · answer',0,say,'Step 2, '+pages.length+' pages and your question');
    if(S.stop)throw new Error('stopped');
    ASK.res={title:String(r2.title||q).slice(0,160),answer:String(r2.answer||''),cannot:r2.cannot_answer};
    ASK.sent=new Set();pages.forEach(p=>an(p)._pins.forEach(x=>ASK.sent.add(pinKey(x))));
    ASK.filed=null;ASK.fileOpen=false;$('#askBtn').textContent='Ask again';
    renderAskOut();say('Done. Nothing has been filed.');
  }catch(e){
    if(e.message==='stopped')say('Stopped. Nothing was filed.');
    else{if(stage===2)ASK.manual=true;showFail($('#askErr'),e,doAsk);say('The step failed. Nothing was filed.');}
  }
  S.running=null;setRun(1,false);$('#askStop').hidden=true;$('#askBtn').disabled=false;askPlan();renderHeader();
}
function renderAskPages(){
  const el=$('#askPages');
  if(!ASK.pages.length){el.innerHTML='';return;}
  if(!$('#pick')){
    el.innerHTML='<p class="lab">PAGES THE ANSWER IS BUILT ON</p><p><span id="pchips"></span> <a href="#" data-act="chg">Change pages</a></p><fieldset id="pick" class="pick" hidden><legend>Tick up to five pages, then press Ask again</legend>'+P.map(p=>'<label class="ck"><input type="checkbox" data-act="pickp" value="'+esc(p.slug)+'"> '+esc(p.title)+'</label>').join('')+'</fieldset>';
  }
  $('#pchips').innerHTML=ASK.pages.map(s=>'<a class="pgchip" href="#'+encodeURIComponent(s)+'">'+esc(pg(s).title)+'</a>').join('');
  $$('#pick input').forEach(c=>{c.checked=ASK.pages.includes(c.value);});
}
function renderAskOut(){
  const r=ASK.res,el=$('#askOut');
  if(!r){el.innerHTML='';renderAskFile();return;}
  const pins=parsePins(r.answer),by={};let bad=0;
  pins.forEach(x=>{if(verify(x).ok&&ASK.sent.has(pinKey(x))){const l=docReg(x.id)[0]||'?';by[l]=(by[l]||0)+1;}else bad++;});
  ASK.bad=bad;ASK.n=pins.length;
  const cn=Array.isArray(r.cannot)?r.cannot.map(x=>'- '+x).join('\n'):String(r.cannot||'');
  el.innerHTML='<div data-source="ai" class="answer"><p class="lab">Answer · written by a model, every pin checked by this page</p><h3>'+esc(r.title)+'</h3>'+md(r.answer,{sent:ASK.sent})+'<h4>What the library cannot answer</h4>'+(cn.trim()?md(cn,{sent:ASK.sent}):'<p>The model flagged nothing.</p>')+'</div>'
   +'<p class="hint">Verified pins by register: '+(Object.keys(by).sort().map(l=>'('+l+') '+(REGS[l]||'unknown')+' '+by[l]).join(' · ')||'none')+(bad?' · struck or not verified: '+bad:'')+'</p>'
   +'<p class="how">How this is computed: a pin counts when its quote is found in a passage of its library document on the same PDF page and it stands on the pages sent; its register is the register of its document.</p>'
   +(ASK.filed?'<p aria-live="polite">Filed as <a href="#'+encodeURIComponent(ASK.filed)+'">'+esc(ASK.filed)+'</a>.</p>':ASK.fileOpen?'':'<p><button type="button" class="btn" data-act="fileq">File as a question page</button></p>');
  renderAskFile();
}
function buildQ(){
  const r=ASK.res,qt=$('#qt'),title=((qt?qt.value:r.title).trim())||r.title,base=slugify(title)||'question';
  let slug=base,i=2;while(pg(slug))slug=base+'-'+(i++);
  const tags=($('#qtags')?$('#qtags').value:'').split(',').map(s=>s.trim()).filter(Boolean);
  const pins=parsePins(r.answer).filter(x=>verify(x).ok),sources=uniq(pins.map(x=>x.id));
  const reg=uniq([].concat(...sources.map(docReg))).sort();
  const links=uniq(Array.from(r.answer.matchAll(/\[\[([^\]|#]+)/g),m=>m[1].trim())).filter(s=>pg(s));
  const cn=Array.isArray(r.cannot)?r.cannot.map(x=>'- '+x).join('\n'):String(r.cannot||'');
  const body='# '+title+'\n\n**Short answer.** '+firstSentence(r.answer)+'\n\n## Reasoning\n\n'+r.answer.trim()+'\n\n## What the library cannot answer\n\n'+(cn.trim()||'The model flagged nothing.')+'\n\n## Related\n\n'+(links.length?links.map(s=>'- [['+s+']]').join('\n'):'- none yet')+'\n';
  return{slug,type:'question',title,fm:{title,type:'question',tags,register:reg,status:'draft',updated:today(),links,sources},body};
}
function renderAskFile(){
  const el=$('#askFile');
  if(!ASK.res||!ASK.fileOpen||ASK.filed){el.innerHTML='';return;}
  if($('#qt'))return;
  el.innerHTML='<fieldset class="card"><legend>File as a question page</legend><label for="qt" class="lbl">Title of the page</label><input id="qt" type="text" value="'+esc(ASK.res.title)+'"><label for="qtags" class="lbl">Tags (comma-separated, typed by you)</label><input id="qtags" type="text" placeholder="neurorights, existing-rights"><p class="lab">Preview of the page the code builds</p><pre id="qprev" class="prev"></pre><p id="qwhy" class="hint" aria-live="polite"></p><p class="row"><button type="button" id="qfile" class="btn pri" data-act="file-q">File this page</button><button type="button" class="btn" data-act="copy-ans">Copy answer</button><span id="qnote" class="hint" aria-live="polite"></span></p></fieldset>';
  $('#qt').addEventListener('input',updAskFile);$('#qtags').addEventListener('input',updAskFile);updAskFile();
}
function updAskFile(){
  const b=buildQ(),why=[];
  if(ASK.bad)why.push(ASK.bad+' pin(s) in the answer do not verify or are not on the pages sent');
  if(!ASK.n)why.push('the answer carries no pin');
  if(!$('#qt').value.trim())why.push('the title is empty');
  $('#qprev').textContent=toMd(b);
  $('#qwhy').textContent=why.length?'Filing is off: '+why.join('; ')+'.':'All '+ASK.n+' pins verify. Nothing is filed until you press the button.';
  $('#qfile').disabled=!!why.length;
}
function fileQ(){
  const b=buildQ(),d=today(),n0=lintNums();
  addPage(b);an(b);
  const N=pinCount(b);
  idxSet(b.slug,'- [['+b.slug+']] — '+firstSentence(ASK.res.answer).slice(0,160)+' · ('+b.fm.register.join(', ')+') · ✓'+N,SEC.question,'Questions');
  idxCounts();
  addLog('## ['+d+'] ask | '+b.title+'\nFiled [['+b.slug+']] from a question put to the wiki. '+N+' pins, all verified by this page. Pages read: '+ASK.pages.map(s=>'[['+s+']]').join(', ')+'.');
  const op=++S.op;S.changes.push({op,date:d,kind:'ask',slug:b.slug,title:b.title,page:'new'});
  S.filing={slugs:[b.slug],before:n0,after:lintNums()};
  ASK.filed=b.slug;renderAskOut();renderAll();$('#askOut').scrollIntoView();
}

/* ---------- 03 INGEST ---------- */
let ING=null;
const inboxDocs=()=>Object.keys(DOC).map(k=>DOC[k]).filter(d=>d.status==='inbox');
function startIngest(id){
  if(S.running)return;
  const doc=DOC[id],ps=doc.passages,batches=[];
  for(let i=0;i<ps.length;i+=25)batches.push({ps:ps.slice(i,i+25)});
  const stub=pg(slugify(doc.id))||P.find(p=>p.fm.status==='stub')||null;
  ING={id,doc,batches,step:1,done:0,sent:0,sentIds:new Set(),all:[],ok:[],failed:[],newSlugs:[],dropped:0,returned:0,prog:'',err:null,stopped:false,src:null,srcOne:'',srcSlug:null,touches:[],drafts:[],pi:0,changes:[],cur:0,dec:{},filed:null,chars:ps.reduce((a,x)=>a+x.text.length,0),stub,cite:citeAs(id)};
  renderIngest();const h=$('#ingH');if(h)h.focus();
}
const ingSay=t=>{if(ING)ING.prog=t;const e=$('#ingProg');if(e)e.textContent=t;};
function ingBegin(){S.running='ingest';S.stop=false;setRun(2,true);ING.err=null;renderIngest();}
function ingEnd(){S.running=null;setRun(2,false);renderIngest();renderHeader();}
function rangeOf(a){a=a.filter(x=>x!=null&&x!=='');return a.length?(a[0]===a[a.length-1]?a[0]:a[0]+'–'+a[a.length-1]):'–';}
function tkTable(I){
  if(!I.all.length)return '<p class="hint">Nothing has returned yet.</p>';
  return '<table><caption>FIG.01 · Takeaways returned by the model, each checked by this page</caption><thead><tr><th scope="col">Claim</th><th scope="col">Quote</th><th scope="col">Passage</th><th scope="col">Would touch</th><th scope="col">Check</th></tr></thead><tbody>'+I.all.map(x=>{
    const k=PR.push({pin:{id:I.id,page:x.passage.page,quote:x.quote}})-1;
    return '<tr data-source="ai"><td>'+esc(x.claim)+'</td><td><span class="pq">\u201C'+esc(x.quote)+'\u201D</span></td><td><button type="button" class="cl" data-act="open" data-k="'+k+'" aria-label="Open '+esc(x.pin.label)+' at PDF page '+x.passage.page+'">'+(x.passage.paragraph?'para. '+esc(x.passage.paragraph):'p. '+esc(x.passage.page_label))+' · PDF p. '+x.passage.page+'</button></td><td>'+(x.pages.map(s=>'<a class="pgchip" href="#'+encodeURIComponent(s)+'">'+esc(s)+(pg(s)?'':' (new)')+'</a>').join('')||'<span class="hint">none named</span>')+'</td><td class="'+(x.ok?'pass':'chk')+'">'+(x.ok?'verified':'could not verify')+'</td></tr>';
  }).join('')+'</tbody></table>';
}
function failBox(I){
  if(!I.failed.length)return '<p class="hint">Could not verify: 0</p>';
  return '<div class="warn"><b>Could not verify: '+I.failed.length+'</b><p class="hint">These claims are in no change card and in no later prompt.</p>'+I.failed.map(x=>{
    const k=PR.push({pin:{id:I.id,page:x.passage.page,quote:x.quote}})-1,n=x.near;
    return '<div data-source="ai" style="border-top:1px solid var(--rule);padding:6px 0"><p><span class="pq">\u201C'+esc(x.quote)+'\u201D</span><br><span class="hint">The model named '+esc(x.passage.id)+' (PDF p. '+x.passage.page+'). '+esc(x.v.reason||'')+'.</span></p>'+(n&&n.p?'<p class="hint">Nearest passage on that page: '+(n.p.paragraph?'para. '+esc(n.p.paragraph):'p. '+esc(n.p.page_label))+', sharing a run of '+n.run+' word(s) with the quote: '+esc(n.p.text.slice(0,200))+'…</p>':'<p class="hint">No passage on that page shares a word run with the quote.</p>')+'<button type="button" class="btn" data-act="open" data-k="'+k+'" aria-label="Open the PDF page '+x.passage.page+' for this quote">Open the PDF page</button></div>';
  }).join('')+'</div>';
}
function chgHtml(c,k,n){
  const known=new Set(ING.changes.map(x=>x.slug)),bad=c.pinsBad>0;
  return '<fieldset class="chg"><legend>Change '+k+' of '+n+': '+esc(c.title)+'</legend><p><span class="badge">'+esc(c.type)+'</span><span class="badge">'+(c.isNew?'new page':'edited')+'</span> '+c.insParas+' paragraph'+(c.insParas===1?'':'s')+' inserted · '+(c.pinsOk+c.pinsBad)+' pins added: '+c.pinsOk+' verified, '+c.pinsBad+' not verified'+(c.contested?' · adds a contested card':'')+'</p>'+(c.notes.length?'<p class="hint">'+esc(c.notes.join(' '))+'</p>':'')
   +'<div class="page" data-source="ai">'+md(c.body,{diff:true,known,inbox:true})+'</div>'
   +'<p class="row"><button type="button" class="btn pri" data-act="approve"'+(bad?' disabled':'')+' aria-label="Approve this page: change '+k+' of '+n+', '+esc(c.title)+'">Approve this page</button><button type="button" class="btn" data-act="reject" aria-label="Reject this page: change '+k+' of '+n+', '+esc(c.title)+'">Reject this page</button><span class="hint">change '+k+' of '+n+'</span></p>'
   +(bad?'<p class="hint">Approve is off: '+c.pinsBad+' pin(s) in this draft do not verify, and nothing unverified may enter the wiki. Reject this page.</p>':'')+'</fieldset>';
}
function renderIngest(){
  const el=$('#ingBox');if(!el)return;
  const I=ING;
  if(!I){
    const L=inboxDocs();
    el.innerHTML=L.length?L.map(d=>'<p><button type="button" class="btn pri" data-act="ing" data-id="'+esc(d.id)+'">Ingest '+esc(d.symbol||d.short_title)+'</button> <span class="hint">'+esc(d.short_title)+' · '+d.passages.length+' passages · reads it into the wiki, one approval per page</span></p>').join('')+'<p class="how">How this is computed: documents in the library whose status is "inbox".</p>':'<p>Nothing waits in the inbox.</p>';
    return;
  }
  const nb=I.batches.length,tot=I.doc.passages.length;
  let h='<h3 id="ingH" tabindex="-1">Ingest '+esc(I.doc.symbol||I.doc.short_title)+'</h3><ol class="stepper" aria-label="Ingest steps">'+['Scope','Takeaways','Drafts','Review and file'].map((s,i)=>'<li'+(I.step===i+1?' aria-current="step"':'')+(I.step>i+1?' class="done"':'')+'>'+(i+1)+' '+s+'</li>').join('')+'</ol>'
   +'<p class="runline" aria-live="polite"><span class="big">'+S.calls+'</span> calls so far · <span class="big">'+S.passages+'</span> passages sent</p>'
   +'<p class="row"><span id="ingProg" class="prog" aria-live="polite">'+esc(I.prog)+'</span>'+(S.running==='ingest'?'<button type="button" class="btn" data-act="stop">Stop</button>':'')+'</p>'+(I.err?failHtml(I.err).replace('data-act="retry"','data-act="ing-retry"'):'');
  if(I.step===1){
    h+='<section class="sec"><h4>Step 1 · Scope: the whole document</h4><p>All '+tot+' passages will be sent, in batches of 25 ('+nb+' calls), '+fmt(I.chars)+' characters; nothing is held back. They leave this browser for a language model; the code then checks every quote it returns.</p><div class="tw"><table><caption>Batches, in file order</caption><thead><tr><th scope="col">Batch</th><th scope="col">Paragraphs</th><th scope="col">PDF pages</th><th scope="col" class="num">Passages</th></tr></thead><tbody>'
     +I.batches.map((b,i)=>'<tr><td>'+(i+1)+' of '+nb+'</td><td>'+esc(rangeOf(b.ps.map(x=>x.paragraph)))+'</td><td>'+esc(rangeOf(b.ps.map(x=>x.page)))+'</td><td class="num">'+b.ps.length+'</td></tr>').join('')+'</tbody></table></div><p class="row"><button type="button" class="btn pri" data-act="ing-start">Start</button></p></section>';
  }
  if(I.step>=2)h+='<details class="sec"'+(I.step===2?' open':'')+'><summary>Step 2 · Takeaways: '+I.ok.length+' verified, '+I.failed.length+' could not be verified</summary><div class="tw">'+tkTable(I)+'</div>'+failBox(I)+'</details>';
  if(I.step>=3){
    h+='<section class="sec"><h4>Step 3 · Drafts</h4><p>'+I.ok.length+' verified takeaways go into the drafts; '+I.failed.length+' could not be verified and stay out of every prompt'+(I.dropped?'; '+I.dropped+' named a passage that was not sent and were dropped':'')+(I.stopped?'; the run was stopped, so the takeaways cover '+I.sent+' of '+tot+' passages':'')+'.</p>';
    if(I.step===3&&!I.src)h+='<p class="row"><button type="button" class="btn pri" data-act="draft-src"'+(I.ok.length?'':' disabled')+'>Draft the source page (1 call)</button><span class="hint">'+(I.ok.length?'sends the verified takeaways with their pins, the index and the document details':'no verified takeaway to draft from')+'</span></p>';
    if(I.src)h+='<div data-source="ai"><p><b>Source page drafted:</b> '+esc(I.src.title)+' <span class="hint">('+esc(I.srcSlug)+')</span></p><p>'+esc(I.srcOne)+'</p></div>';
    if(I.step===3&&I.src)h+='<p class="hint">Pages to draft: '+I.touches.map(t=>esc(t.slug)+(t.isNew?' (new)':'')).join(', ')+'</p><p class="row"><button type="button" class="btn pri" data-act="draft-pages">Draft the changes to '+I.touches.length+' pages ('+I.touches.length+' calls)</button></p>';
    h+='</section>';
  }
  if(I.step>=4){
    const n=I.changes.length;h+='<section class="sec"><h4>Step 4 · Review and file</h4>';
    if(I.filed){
      const f=I.filed;
      h+='<p aria-live="polite"><b>Filed.</b> '+f.ap.length+' page(s) written, '+f.rj.length+' rejected and left exactly as loaded.'+(f.statusSet?' The document now counts as ingested.':' The source page was not approved, so the document stays in the inbox.')+'</p><div class="tw"><table><caption>Lint, before and after filing</caption><thead><tr><th scope="col">Check</th><th scope="col" class="num">Before</th><th scope="col" class="num">After</th></tr></thead><tbody>'+f.labels.map((l,i)=>'<tr><th scope="row">'+esc(l)+'</th><td class="num">'+f.before[i]+'</td><td class="num">'+f.after[i]+'</td></tr>').join('')+'</tbody></table></div>';
    }else if(I.cur<n)h+=chgHtml(I.changes[I.cur],I.cur+1,n);
    else{
      const a=I.changes.filter(c=>I.dec[c.slug]==='approved').length;
      h+='<p>All '+n+' changes decided: '+a+' approved, '+(n-a)+' rejected. Nothing is written until you file.</p><p class="row"><button type="button" class="btn pri" data-act="file-ing"'+(a?'':' disabled')+'>File the approved changes</button>'+(a?'':'<span class="hint">nothing approved, nothing to file</span>')+'</p>';
    }
    h+='</section>';
  }
  el.innerHTML=h;
}
function nearest(doc,page,quote){
  const q=norm(quote).split(' ');let best={run:0,p:null};
  doc.passages.filter(x=>x.page===page).forEach(x=>{
    const t=norm(x.text).split(' ');let prev=new Array(t.length+1).fill(0),run=0;
    for(let i=1;i<=q.length;i++){const cur=new Array(t.length+1).fill(0);for(let j=1;j<=t.length;j++)if(q[i-1]===t[j-1]){cur[j]=prev[j-1]+1;if(cur[j]>run)run=cur[j];}prev=cur;}
    if(run>best.run||!best.p)best={run,p:x};
  });
  return best;
}
function takeawayPrompt(I,items){
  return 'You are reading one batch of passages from '+(I.doc.symbol||I.doc.short_title)+' for a research wiki on neurotechnology in the administration of justice. Below are the wiki\'s index (the slugs of its pages) and '+items.length+' passages as JSON {id, page, paragraph, text}.\nReturn JSON {"takeaways":[{"claim":"...","quote":"...","passage":"<id of the passage>","pages":["slug", ...]}]}: at most 10; each quote 8 to 40 words copied verbatim from that one passage; pages = slugs from the index the claim bears on. '+PIN_RULE+'\n\nINDEX\n'+S.index+'\n\nPASSAGES\n'+JSON.stringify(items);
}
function processTakeaways(I,b,r){
  const list=(r&&Array.isArray(r.takeaways)?r.takeaways:[]).slice(0,10),rec=S.callLog[S.callLog.length-1],tk={returned:list.length,ok:0,failed:0,dropped:0};
  rec.unknown=[];
  list.forEach(t=>{
    const p=I.sentIds.has(String(t.passage))?I.doc.passages.find(x=>x.id===String(t.passage)):null;
    if(!p){tk.dropped++;I.dropped++;return;}
    const quote=String(t.quote||'').trim(),pin=makePin(I.doc,p,quote,I.cite),v=verify(pin,true),pages=[];
    (Array.isArray(t.pages)?t.pages:[]).map(s=>slugify(String(s))).forEach(s=>{
      if(!s||pages.includes(s))return;
      if(pg(s)||I.newSlugs.includes(s))pages.push(s);
      else if(I.newSlugs.length<2){I.newSlugs.push(s);pages.push(s);}
      else rec.unknown.push(s);
    });
    const x={claim:String(t.claim||''),quote:pin.quote,passage:p,pin,pages,v,ok:v.ok};
    I.all.push(x);
    if(v.ok){I.ok.push(x);tk.ok++;}else{x.near=nearest(I.doc,p.page,quote);I.failed.push(x);tk.failed++;}
  });
  rec.tk=tk;
}
async function runBatches(){
  const I=ING;if(S.running)return;
  I.step=2;ingBegin();
  try{
    while(I.done<I.batches.length){
      if(S.stop){I.stopped=true;break;}
      const b=I.batches[I.done],items=b.ps.map(p=>({id:p.id,page:p.page,paragraph:p.paragraph,text:p.text})),nb=I.batches.length;
      b.ps.forEach(p=>I.sentIds.add(p.id));
      const r=await callModel(takeawayPrompt(I,items),'takeaways '+(I.done+1),items.length,ingSay,'Batch '+(I.done+1)+' of '+nb);
      processTakeaways(I,b,r);I.done++;I.sent+=items.length;
      ingSay('batch '+I.done+' of '+nb+' · '+I.sent+' of '+I.doc.passages.length+' passages have left the browser');renderIngest();
    }
    I.step=3;
  }catch(e){
    const b=I.batches[I.done];if(b)b.ps.forEach(p=>I.sentIds.delete(p.id));
    I.err={e,retry:runBatches};
  }
  ingEnd();
}
function sourcePrompt(I){
  const d=I.doc,tk=I.ok.map((x,i)=>(i+1)+'. '+x.claim+'\n   pin: '+x.pin.raw+'\n   bears on: '+(x.pages.join(', ')||'(none named)')).join('\n');
  return 'Write the source page for a research wiki on neurotechnology in the administration of justice.\nDocument: '+d.title+'. Author: '+d.author+'. Published: '+d.published+'. '+d.pages+' PDF pages. '+d.url+'\nCite-as: '+I.cite+'. Register of this document: ('+((I.stub&&I.stub.fm.register)||[]).join(', ')+').\nA source page has these sections: Full cite, Register, One-liner, Key takeaways, How NOT to read this, Where it feeds the wiki, Related.\nReturn JSON {"one_liner":"...","body":"markdown, at most 900 words, starting with a # title line","touches":[{"slug":"...","why":"..."}]}. Use only the pins given below, copied exactly; link other pages as [[slug]]. touches = pages of the index this document should be added to (at most 12; at most 2 new slugs). '+PIN_RULE+'\n\nVERIFIED TAKEAWAYS\n'+tk+'\n\nINDEX\n'+S.index;
}
function insStats(body){
  let paras=0,ok=0,bad=0;
  for(const m of body.matchAll(INS_ALL)){
    paras+=m[1].split(/\n\s*\n/).filter(s=>s.trim()).length;
    parsePins(m[1]).forEach(x=>{if(verify(x,true).ok)ok++;else bad++;});
  }
  return{paras,ok,bad};
}
async function draftSource(){
  const I=ING;if(S.running)return;
  ingBegin();
  try{
    const r=await callModel(sourcePrompt(I),'source page',0,ingSay,'Drafting the source page');
    const doc=I.doc,title=doc.short_title||doc.title;
    let body=String(r.body||'').trim();if(!/^#\s/.test(body))body='# '+title+'\n\n'+body;
    const base=slugify(doc.symbol||doc.short_title||doc.id)||'source';let slug=base,k=2;
    if(pg(base))slug=base+'-source';while(pg(slug))slug=base+'-source-'+(k++);
    const rec=S.callLog[S.callLog.length-1];rec.unknown=[];
    const cnt={};I.ok.forEach(x=>x.pages.forEach(s=>{cnt[s]=(cnt[s]||0)+1;}));
    const cand=[];
    (Array.isArray(r.touches)?r.touches:[]).forEach(t=>{const s=slugify(String(t&&t.slug||''));if(s&&!cand.some(c=>c.slug===s)&&s!==slug)cand.push({slug:s,why:String(t.why||'')});});
    Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]).forEach(s=>{if(!cand.some(c=>c.slug===s))cand.push({slug:s,why:'takeaways bear on this page'});});
    const newOk=I.newSlugs.slice(),touches=[];
    cand.forEach(c=>{
      if(touches.length>=12)return;
      if(pg(c.slug)||newOk.includes(c.slug)){touches.push(Object.assign(c,{isNew:!pg(c.slug)}));}
      else if(newOk.length<2){newOk.push(c.slug);touches.push(Object.assign(c,{isNew:true}));}
      else rec.unknown.push(c.slug);
    });
    if(I.stub&&!touches.some(t=>t.slug===I.stub.slug))touches.push({slug:I.stub.slug,why:'stub for this document',isNew:false});
    I.stubSlug=I.stub&&I.stub.slug;I.touches=touches;I.srcSlug=slug;I.srcOne=String(r.one_liner||'');
    const known=new Set(touches.map(t=>t.slug));
    const links=uniq(Array.from(body.matchAll(/\[\[([^\]|#]+)/g),m=>m[1].trim()).filter(s=>pg(s)||known.has(s)).concat(touches.map(t=>t.slug)));
    const full=INS0+'\n'+body+'\n'+INS1+'\n',st=insStats(full);
    I.src={slug,isNew:true,type:'source',title,fm:{title,type:'source',tags:touches.map(t=>t.slug),register:((I.stub&&I.stub.fm.register)||docReg(doc.id)).slice(),status:'draft',updated:today(),links,sources:[doc.id]},body:full,notes:[],insParas:st.paras,pinsOk:st.ok,pinsBad:st.bad,contested:false,added:[]};
    ingSay('Source page drafted; '+st.ok+' pins verified, '+st.bad+' not.');
  }catch(e){I.err={e,retry:draftSource};}
  ingEnd();
}
function insertAt(body,after,text,notes){
  const lines=body.replace(/\s+$/,'').split('\n'),block=['',INS0,text.trim(),INS1,''],want=String(after||'end').replace(/^#+\s*/,'').trim().toLowerCase();
  if(want&&want!=='end'){
    const hi=lines.findIndex(l=>/^#{1,4}\s/.test(l)&&l.replace(/^#+\s*/,'').trim().toLowerCase()===want);
    if(hi>=0){
      const lv=lines[hi].match(/^#+/)[0].length;let e=hi+1;
      while(e<lines.length&&!(/^#{1,4}\s/.test(lines[e])&&lines[e].match(/^#+/)[0].length<=lv))e++;
      while(e>hi+1&&!lines[e-1].trim())e--;
      lines.splice.apply(lines,[e,0].concat(block));return lines.join('\n')+'\n';
    }
    notes.push('Heading "'+after+'" was not found, so that text was added at the end of the page.');
    block.splice(2,0,'*(The model named the heading "'+String(after).replace(/"/g,"'")+'"; it was not found, so this was added at the end.)*','');
  }
  Array.prototype.push.apply(lines,block);return lines.join('\n')+'\n';
}
function pagePrompt(I,t,p,use,isStub){
  const tk=use.map((x,i)=>(i+1)+'. '+x.claim+'\n   pin: '+x.pin.raw).join('\n');
  return 'You are editing one page of a research wiki, adding what a newly read document says and nothing else.\nPAGE: '+t.slug+(p?' — '+p.title:' (does not exist yet; it will be created)')+'\nWhy it is touched: '+t.why+'\n'+(isStub?'This page is a stub for the document just read. Its body holds a checklist of what the ingest should check: address each item the takeaways can answer, and say in one line what they cannot.\n':'')
   +'Return JSON {"edits":[{"after":"an existing heading of this page, or end","markdown":"..."}],"contested":null}. At most 300 words in all. Copy pins exactly as given. "contested" is null, or a full block (opened by three backticks and the word contested; lines claim:, verdict:, note:, then one line per position: +, - or ~, the register letter, a pin, a gloss and a [[slug]], separated by " | ") only where this document disagrees with the page. '+PIN_RULE+'\n\nPAGE BODY\n'+(p?p.body:'(empty)')+'\n\nTAKEAWAYS\n'+tk;
}
function mkPageChange(I,t,p,r){
  const title=p?p.title:t.slug.replace(/-/g,' ').replace(/^./,c=>c.toUpperCase()),notes=[];
  let body=p?p.body:'# '+title+'\n',contested=false;
  (r&&Array.isArray(r.edits)?r.edits:[]).filter(e=>e&&typeof e.markdown==='string'&&e.markdown.trim()).forEach(e=>{body=insertAt(body,e.after,e.markdown,notes);});
  if(r&&typeof r.contested==='string'&&r.contested.indexOf(FENCE+'contested')>=0){body=insertAt(body,'Contested claims',r.contested.trim(),notes);contested=true;}
  const fm=clone(p?p.fm:{title,type:'concept',tags:[],register:docReg(I.doc.id).slice(),status:'draft',updated:today(),links:[],sources:[]}),added=[];
  const st=insStats(body);
  for(const m of body.matchAll(INS_ALL))parsePins(m[1]).forEach(x=>{if(fm.sources.indexOf(x.id)<0)fm.sources.push(x.id);});
  if(I.srcSlug&&fm.links.indexOf(I.srcSlug)<0){fm.links.push(I.srcSlug);added.push(I.srcSlug);}
  if(t.slug===I.stubSlug&&st.paras>0&&fm.status==='stub')fm.status='draft';
  return{slug:t.slug,isNew:!p,type:p?p.type:'concept',title,fm,body,notes,insParas:st.paras,pinsOk:st.ok,pinsBad:st.bad,contested,added};
}
async function draftPages(){
  const I=ING;if(S.running)return;
  ingBegin();
  try{
    while(I.pi<I.touches.length){
      if(S.stop){I.stopped=true;break;}
      const t=I.touches[I.pi],p=pg(t.slug),isStub=t.slug===I.stubSlug,tks=isStub?I.ok:I.ok.filter(x=>x.pages.indexOf(t.slug)>=0),use=(tks.length?tks:I.ok).slice(0,12);
      const r=await callModel(pagePrompt(I,t,p,use,isStub),'page '+t.slug,0,ingSay,'Page '+(I.pi+1)+' of '+I.touches.length+' ('+t.slug+')');
      I.drafts.push(mkPageChange(I,t,p,r));I.pi++;
      ingSay(I.pi+' of '+I.touches.length+' pages drafted');renderIngest();
    }
    const real=I.drafts.filter(c=>c.insParas>0);
    I.src.fm.links=uniq(I.src.fm.links.filter(s=>pg(s)||real.some(c=>c.slug===s)));I.src.added=real.map(c=>c.slug);
    I.changes=[I.src].concat(real);I.cur=0;I.step=4;
    ingSay(real.length+' page(s) have a proposed change'+(I.drafts.length>real.length?'; '+(I.drafts.length-real.length)+' came back with no change':'')+'. Nothing is written yet.');
  }catch(e){I.err={e,retry:draftPages};}
  ingEnd();
}
function cleanIns(b){return b.replace(new RegExp('^('+INS0+'|'+INS1+')[ \\t]*\\n?','gm'),'').replace(/\n{3,}/g,'\n\n').trim()+'\n';}
function fileIng(){
  const I=ING,d=today(),before=lintNums(),labels=lint().map(r=>r.label);
  const ap=I.changes.filter(c=>I.dec[c.slug]==='approved'),rj=I.changes.filter(c=>I.dec[c.slug]==='rejected'),op=++S.op;
  const exist=new Set(P.map(p=>p.slug)),rejected=new Set(rj.map(c=>c.slug));ap.forEach(c=>exist.add(c.slug));
  ap.forEach(c=>{
    const body=cleanIns(c.body);
    c.fm.updated=d;c.fm.links=c.fm.links.filter(s=>!(c.added.indexOf(s)>=0&&(rejected.has(s)||!exist.has(s))));
    const cur=pg(c.slug);
    if(cur){cur.body=body;cur.fm=c.fm;}else addPage({slug:c.slug,type:c.type,title:c.title,fm:c.fm,body});
    S.changes.push({op,date:d,kind:'ingest',slug:c.slug,title:c.title,page:c.isNew?'new':'edited'});
  });
  const srcOk=ap.some(c=>c.slug===I.srcSlug);
  if(srcOk){DOC[I.id].status='ingested';VC.clear();}
  ap.forEach(c=>{
    const p=pg(c.slug),N=pinCount(p),L=p.fm.register.join(', ');
    if(c.slug===I.srcSlug)idxSet(c.slug,'- [['+c.slug+']] — '+(I.srcOne||p.title)+' · ('+L+') · ✓'+N,SEC.source,'Sources');
    else if(c.isNew||c.slug===I.stubSlug)idxSet(c.slug,'- [['+c.slug+']] — '+p.title+' · ('+L+') · ✓'+N,SEC[p.type]||SEC.concept,p.type==='entity'?'Entities':p.type[0].toUpperCase()+p.type.slice(1)+'s');
    else idxRecount(c.slug,N);
  });
  idxCounts();
  ap.forEach(c=>{
    const m=c.body.match(new RegExp(FENCE+'contested\\n?([\\s\\S]*?)'+FENCE));
    if(!m||!c.contested)return;
    const cd=parseCard(m[1]),id=slugify(cd.claim).slice(0,60)||'claim-'+c.slug,v=cd.verdict;
    const stt=/^settled/.test(v)?'settled':/^leans/.test(v)?'leaning':'open';
    const pos=cd.pos.filter(x=>x.pin);
    S.tens=S.tens.replace(/\s+$/,'')+'\n\n### '+id+'\ntitle: '+cd.claim+'\nstatus: '+stt+'\ncard: [['+c.slug+']]\npoles: '+(cd.pos.filter(x=>x.sign==='+')[0]||{gloss:'none'}).gloss+' / '+(cd.pos.filter(x=>x.sign==='-')[0]||{gloss:'none'}).gloss+'\nwhere: '+pos.map(x=>x.pin.label).join('; ')+'\n';
    S.tensNew.push(id);
  });
  const doc=I.doc,edited=ap.filter(c=>c.slug!==I.srcSlug&&!c.isNew),made=ap.filter(c=>c.slug!==I.srcSlug&&c.isNew);
  const onDoc=ap.filter(c=>c.slug!==I.srcSlug&&pg(c.slug)&&an(pg(c.slug))._pins.some(x=>x.id===doc.id));
  let nDoc=0;P.forEach(p=>{nDoc+=an(p)._pins.filter(x=>x.id===doc.id).length;});
  addLog('## ['+d+'] ingest | '+(doc.symbol||doc.short_title)+': '+doc.short_title+'\nRead '+I.sent+' passages ('+I.cite+', register ('+(docReg(doc.id).join(', ')||'?')+')). '+(srcOk?'Wrote [['+I.srcSlug+']]. ':'No source page was approved. ')+(edited.length?'Edited '+edited.map(c=>'[['+c.slug+']]').join(', ')+'. ':'')+(made.length?'Created '+made.map(c=>'[['+c.slug+']]').join(', ')+'. ':'')+nDoc+' pins in all; besides its own page, pinned on '+onDoc.length+' pages'+(onDoc.length?': '+onDoc.map(c=>'[['+c.slug+']]').join(', '):'')+'. Rejected: '+(rj.length?rj.map(c=>'[['+c.slug+']]').join(', '):'none')+'.');
  const after=lintNums();
  S.filing={slugs:ap.map(c=>c.slug),before,after,labels};
  I.filed={ap,rj,before,after,labels,statusSet:srcOk};
  renderAll();
}

/* ---------- 04 CHECK ---------- */
function renderCheck(){
  const st=pinStats(),L=lint(),need=L.filter(r=>r.items.length).length,CH=checks();
  const links=pages=>pages.length?pages.map(s=>pg(s)?'<a href="#'+encodeURIComponent(s)+'">'+esc(s)+'</a>':esc(s)+' <span class="hint">no page</span>').join(', '):'<span class="hint">none</span>';
  $('#chkBox').innerHTML='<p class="lab">04 · Can I trust this?</p><p><span class="big">'+fmt(st.ok)+'</span> of '+fmt(st.total)+' pins verified by this page</p><p class="how">How this is computed: each pin\'s quote is searched, fragment by fragment in order, in the passages of its document that start on the pin\'s PDF page, and its label must name that passage. The ✓ written in a page is not trusted.</p>'
   +'<p><span class="big">'+need+'</span> of '+L.length+' lint checks need a look</p>'
   +'<p class="row"><button type="button" class="btn pri" data-act="lint">'+(S.lintPressed?'Re-run':'Lint now')+'</button><span class="hint">reads the wiki again; no model is called</span></p>'
   +'<div class="tw"><table><caption>FIG.01 · Lint checks, run by this page</caption><thead><tr><th scope="col">Check</th><th scope="col" class="num">Result</th><th scope="col">Pages concerned</th></tr></thead><tbody>'
   +L.map(r=>'<tr><th scope="row">'+esc(r.label)+'</th><td class="num '+(r.items.length?'chk':'pass')+'">'+r.items.length+' · '+(r.items.length?'check':'pass')+'</td><td>'+links(r.pages)+'</td></tr>').join('')+'</tbody></table></div>'
   +'<p class="hint">Not done by code: the schema\'s reading for contradictions between pages needs a person or a model\'s judgment. The open disagreements are in the tensions register on tab 05.</p>'
   +'<details class="sec" open><summary>Checks panel: how this page checks itself</summary><ul class="chkl">'+CH.map(c=>'<li><span class="'+(c.ok===true?'pass':c.ok===false?'chk':'na')+'">'+(c.ok===true?'pass':c.ok===false?'check':'not yet')+'</span> · <b>'+esc(c.name)+'.</b> '+esc(c.text)+(c.pages.length?' · '+links(c.pages.slice(0,12)):'')+'</li>').join('')+'</ul></details>';
}

/* ---------- 05 RECORD ---------- */
function exportObj(){
  const ls={};Object.keys(DOC).forEach(k=>{ls[k]=DOC[k].status;});
  return{title:WIKI.title,source:WIKI.source,built:WIKI.built,count:P.length,schema:WIKI.schema,pages:P.map(p=>({slug:p.slug,type:p.type,title:p.title,frontmatter:p.fm,body:p.body})),index:S.index,log:S.log,tensions:S.tens,changes:S.changes,library_status:ls};
}
function save(name,text,type){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1500);}
function tensHtml(t){
  const L=t.split('\n'),h=L.shift().replace(/^###\s*/,'').trim(),id=slugify(h);
  const body=L.filter(l=>l.trim()).map(l=>{const m=l.match(/^\s*[-*]?\s*\**([A-Za-z_ ]{2,20}?)\**:\s*(.*)$/);return m?'<div class="kv"><span class="lab">'+esc(m[1])+'</span> '+inline(m[2],{})+'</div>':'<p>'+inline(l.trim(),{})+'</p>';}).join('');
  return '<article class="tens'+(S.sel===id?' sel':'')+'" id="t-'+id+'"><h4>'+esc(h)+(S.tensNew.indexOf(id)>=0?' <span class="sess">this session</span>':'')+'</h4>'+body+'</article>';
}
function renderRecord(){
  const E=logEntries(),ord=E.map((e,i)=>i);if(S.order==='new')ord.reverse();
  const rows=ord.map(i=>'<details class="le"'+(i===ord[0]?' open':'')+'><summary>'+esc(E[i].head)+(i>=S.logBase?' <span class="sess">this session</span>':'')+'</summary><div class="page">'+md(E[i].body)+'</div></details>').join('');
  const ch=changedSlugs();
  $('#recBox').innerHTML='<p class="lab">05 · What has changed, where do the sources disagree, and how do I take it away?</p><h3>Log</h3><p class="row"><button type="button" role="switch" aria-checked="'+(S.order==='new')+'" data-act="order">Newest first</button><span class="hint">'+E.length+' entries, appended only; the switch flips the order</span></p>'+(rows||'<p class="hint">The log is empty.</p>')
   +'<h3>Tensions register</h3><p class="hint">Each entry names the page that holds its contested card.</p>'+(tensEntries().map(tensHtml).join('')||'<p class="hint">No entries.</p>')
   +'<h3>Method</h3><p class="hint">Counting, matching and verification are done by this page\'s code; each number has its "How this is computed" line. Data: '+esc(WIKI.source||'the research wiki')+', built '+esc(WIKI.built||'unknown')+', with the library of '+LIB.length+' documents. The model drafts; the code verifies every quotation; a person decides.</p>'
   +'<p class="row"><button type="button" class="btn pri" data-act="dl-json">Download the wiki</button>'+(ch.length?'<button type="button" class="btn" data-act="dl-md">Download the changed pages (markdown)</button>':'')+'<span class="hint">'+(S.changes.length?S.changes.length+' change(s) live only in this page until you download':'no changes yet')+'</span></p>';
}

/* ---------- events ---------- */
function renderAll(){renderHeader();renderList();renderPage();renderIngest();renderAskPages();if(S.tab===3)renderCheck();if(S.tab===4)renderRecord();askPlan();}
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-act]');if(!b)return;const a=b.dataset.act;
  if(a==='open'){openSrc(PR[+b.dataset.k].pin);}
  else if(a==='tg'){const d=$('#pd'+b.dataset.k),on=d.hidden;d.hidden=!on;b.setAttribute('aria-expanded',on);b.textContent=on?'▾':'▸';}
  else if(a==='retry'){const f=RETRY;RETRY=null;$('#askErr').innerHTML='';if(f)f();}
  else if(a==='ing-retry'){const f=ING.err.retry;ING.err=null;f();}
  else if(a==='ing')startIngest(b.dataset.id);
  else if(a==='ing-start')runBatches();
  else if(a==='draft-src')draftSource();
  else if(a==='draft-pages')draftPages();
  else if(a==='approve'||a==='reject'){const c=ING.changes[ING.cur];ING.dec[c.slug]=a==='approve'?'approved':'rejected';ING.cur++;renderIngest();const h=$('#ingH');if(h)h.focus();}
  else if(a==='file-ing')fileIng();
  else if(a==='stop'){S.stop=true;ingSay('Stopping after the call in flight returns; what has returned is kept.');}
  else if(a==='lint'){S.lintPressed=true;renderCheck();}
  else if(a==='order'){S.order=S.order==='new'?'old':'new';renderRecord();}
  else if(a==='dl-json')save('wiki-'+today()+'.json',JSON.stringify(exportObj(),null,1),'application/json');
  else if(a==='dl-md')save('wiki-changed-pages-'+today()+'.md',changedSlugs().map(s=>toMd(pg(s))).join('\n\n---\n\n'),'text/markdown');
  else if(a==='copy-md'){const p=pg(S.cur);if(p)copyText(toMd(p),$('#cpnote'));}
  else if(a==='copy-ans')copyText(ASK.res.answer,$('#qnote'));
  else if(a==='fileq'){ASK.fileOpen=true;renderAskOut();const t=$('#qt');if(t)t.focus();}
  else if(a==='file-q')fileQ();
  else if(a==='chg'){e.preventDefault();const f=$('#pick');f.hidden=!f.hidden;}
  else if(a==='tens'){S.sel=b.dataset.id;showTab(4);const t=$('#t-'+S.sel);if(t){t.scrollIntoView();}}
});
document.addEventListener('change',e=>{
  const c=e.target;if(!c.dataset||c.dataset.act!=='pickp')return;
  const ch=$$('#pick input:checked').map(x=>x.value);
  if(ch.length>5){c.checked=false;return;}
  ASK.pages=ch;ASK.manual=true;$('#pchips').innerHTML=ch.map(s=>'<a class="pgchip" href="#'+encodeURIComponent(s)+'">'+esc(pg(s).title)+'</a>').join('');
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&S.running){S.stop=true;const t='Stopping after the call in flight returns.';if(S.running==='ask')$('#askProg').textContent=t;else ingSay(t);}});
$('#tabs').innerHTML=TN.map((n,i)=>'<button type="button" role="tab" id="tab'+i+'" data-i="'+i+'" aria-controls="pan'+i+'" aria-selected="false" tabindex="-1">0'+(i+1)+' '+n+'<span class="run" aria-live="polite"></span></button>').join('');
$('#tabs').addEventListener('click',e=>{const b=e.target.closest('[role=tab]');if(b)showTab(+b.dataset.i);});
$('#tabs').addEventListener('keydown',e=>{
  let i=S.tab;
  if(e.key==='ArrowRight')i=(i+1)%5;else if(e.key==='ArrowLeft')i=(i+4)%5;else if(e.key==='Home')i=0;else if(e.key==='End')i=4;else return;
  e.preventDefault();showTab(i,true);
});
$('#flt').addEventListener('input',e=>{S.flt=e.target.value;renderList();});
$('#q').addEventListener('input',askPlan);
$('#q').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();doAsk();}});
$('#askBtn').addEventListener('click',doAsk);
$('#askStop').addEventListener('click',()=>{S.stop=true;$('#askProg').textContent='Stopping after the call in flight returns.';});
window.addEventListener('hashchange',onHash);

/* ---------- start ---------- */
S.logBase=logEntries().length;S.warn0=pinStats().warn;
$('#foot').textContent=(WIKI.source||'Research wiki')+' · built '+(WIKI.built||'unknown')+' · Counting, matching and verification are done by this page\'s code; the model is called only when you press Ask, Ingest or a retry button.';
renderHeader();askPlan();renderIngest();
if(location.hash.length>1)onHash();else{showTab(0);renderList();renderPage();}
$('#tab0').focus();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a tab "MAP" that draws the wiki as a graph: one node per page, coloured by its type (source, concept, entity, question), and one line for each [[link]] between two pages. Size each node by the number of pages that link to it. Draw it in plain SVG with a fixed layout computed by the code (no random start), so the map looks the same every time. Hovering a node shows its title and how many links go in and out; clicking it highlights its neighbours and offers "Open this page", which shows the page on the pages tab. Under the map, one line: how many pages and links, and the pages no other page links to (orphans), each clickable. Keep everything else as it is.

(Attached: Research wiki: neurotechnology and justice → WORKSHOP_DATA.wiki, with WORKSHOP_DATA.library)
