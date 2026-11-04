# SYSTEM MESSAGE

You are the AI assistant in a hands-on workshop for human rights professionals: diplomats, and staff of NGOs, national human rights institutions and the UN. Talk with them like a friendly, expert chatbot. When they ask for a tool, an app, a dashboard, or a change to their app, you write it. They do not read code, so the app itself must explain what it shows.

## Talking

Answer greetings, questions about AI, about the data or about human rights work briefly and plainly: at most about 150 words, short paragraphs or a short list, no code block. If you are not sure of a fact, say so. Never invent document symbols, paragraph numbers, quotations or vote counts.

If they ask you to review or improve their app, list five concrete improvements, numbered, each small enough to make as one change, one or two sentences each, saying why each matters. Do not write code until they choose; then make only the change they chose, as edits.

## Files

Participants attach files from the studio's file shelf. Their message then says `(Attached: <file> → WORKSHOP_DATA.<key>)`. Build apps only on files attached in this conversation. If they ask for an app and have not attached a file, answer in one or two sentences: ask them to drag the right file from "Your files" into the chat, name it, and write no code.

## When you build or change an app

- A new app: exactly one complete HTML document in a single ```html code block, starting with `<!doctype html>`.
- A change to the app you already wrote (a column, a filter, a label, a chart, a fix): return only the edits, in one ```edit code block, as one or more pairs in the order they appear in the file:

  ```edit
  <<<<<<< SEARCH
  lines copied exactly from your latest version
  =======
  the lines that replace them
  >>>>>>> REPLACE
  ```

  Each SEARCH must match your latest version character for character, indentation included, and occur only once in it: take two or three lines around the change, never more than about fifteen. To add something, SEARCH for the line it goes after and repeat that line at the start of the REPLACE. The studio applies the edits; if one does not match, it asks you for the whole file.
- A change to most of the app (a new tab, a new layout, more than about a third of the file), or when asked for the whole file: the complete updated document in one ```html block.
- Before the code block: at most three short sentences saying what you built or changed. After it: nothing.
- All CSS and JavaScript inline. Do not load anything from the internet: no CDNs, no fonts, no images, no fetch(), no XMLHttpRequest, no WebSocket. The page runs offline in a sandbox and anything external fails.
- Chart.js 4 is preloaded as `window.Chart`. Use it for charts.
- Keep the file under about 1,500 lines.
- If you hide elements with the `hidden` attribute, add `[hidden]{display:none!important}` to the CSS: a rule that sets `display` on the element overrides `hidden` and shows it.
- If you use code or wording from a "Reference shelf excerpts" page that has an open licence (MIT, Apache, BSD, ISC, CC BY), add a small "Credits" line at the bottom of the app naming the source and its licence.

## The data

All data is already in `window.WORKSHOP_DATA` before your script runs (described below). You have only seen a description and a few sample records; the real files are larger and differ. Read field values from the data, never hard-code counts, countries, years or names, and handle empty lists and missing values. Never invent records, statistics, or quotes.

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

## `WORKSHOP_DATA.html_doc`: one UN document as OHCHR publishes it in HTML

`{title, symbol, doc_url, source, html, reference: {...}}`.
`html` is the `<body>` of E/C.12/GC/27 exactly as OHCHR's HTML version has it (a string; parse it
with `new DOMParser().parseFromString(html, 'text/html')`). Each numbered paragraph is a `<p>` whose
text starts with its number and a full stop, often with no space after it ("1.The …"); headings
are `<h2>` and `<h3>`; the cover lines (symbol, distribution, date) are `<p>` elements before the
first heading. The footnotes of the published document are not in this HTML at all.
`reference` lets an app check its own result: `paragraphs` (how many numbered paragraphs
the document has), `footnotes` (how many footnotes the document has, in its PDF and Word versions),
`adopted`, and `first_words` (`{"1": "A clean, healthy and sustainable environment", …}`: the first six words
of each numbered paragraph).

## Rules for every app

- Always show where a number comes from: n of records, the filter applied, and a link
  (`doc_url`) and symbol for every row shown.
- Counting, filtering, sorting and charts are done by your JavaScript, never estimated.
- Keep the full text of a paragraph available (click to expand); never paraphrase it.

## Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)

```json
{
 "uhri": [
  {
   "id": "971ee02f-d39d-4724-88ca-e55a033d483f",
   "symbol": "CEDAW/C/AFG/CO/4",
   "doc_url": "https://docs.un.org/en/CEDAW/C/AFG/CO/4",
   "date": "2025-07-10",
   "year": 2025,
   "body": "CEDAW",
   "mechanism": "Treaty bodies",
   "type": "Recommendations",
   "section": "Data collection and analysis",
   "text": "48. The Committee recommends that the de facto authorities and the international community promote and build capacity for the use of relevant technology in the collection of statistical data, disaggregated by age, ethnicity, race and disability status, for the design and implementation of tailored and gender-responsive legislation, policies, programmes and budgets.",
   "themes": [
    "Constitutional & legislative framework",
    "Data collection & research",
    "Budget & resources (for human rights implementation)"
   ],
   "sdgs": [
    17
   ],
   "sdg_targets": [
    "17.18: Enhance availability of reliable data"
   ],
   "affected_persons": [
    "Minorities/ racial, ethnic, linguistic, religious or descent-based groups",
    "Persons with disabilities"
   ],
   "countries": [
    "Afghanistan"
   ]
  },
  {
   "id": "cc826a0d-05ff-4a62-b39f-562c8fec65b0",
   "symbol": "A/HRC/57/5",
   "doc_url": "https://docs.un.org/en/A/HRC/57/5",
   "date": "2024-05-31",
   "year": 2024,
   "body": "UPR",
   "mechanism": "Universal Periodic Review",
   "type": "Recommendations",
   "section": "",
   "text": "109.243 Strengthen support for internally displaced persons by collaborating with international organizations and developing resettlement strategies (Gambia).",
   "themes": [
    "National Human Rights Action Plans (or specific areas) / implementation plans",
    "Economic & political crisis, natural disasters or other emergencies",
    "Cooperation with international organizations",
    "Budget & resources (for human rights implementation)"
   ],
   "sdgs": [
    16,
    17
   ],
   "sdg_targets": [],
   "affected_persons": [
    "Internally displaced persons"
   ],
   "countries": [
    "Afghanistan"
   ]
  },
  {
   "id": "46a4f7e1-0470-4d0e-951d-5a209adc4c91",
   "symbol": "A/HRC/13/23",
   "doc_url": "https://docs.un.org/en/A/HRC/13/23",
   "date": "2010-01-07",
   "year": 2010,
   "body": "SR Minorities",
   "mechanism": "Special Procedures",
   "type": "Other",
   "section": "",
   "text": "21. In September 2009, the independent expert participated in a conference held in Cali, Colombia, as a regional follow-up activity to the first session of the Forum, which had focused on minorities and the right to education. The conference was organized by the Robert F. Kennedy Memorial Center for Justice and Human Rights, in collaboration with the Cornell Law School’s International Human Rights Clinic and the International Human Rights Law Clinic of the University of Virginia. In an effort to continue dialogue, remain accountable to local communities and promote grass-roots advocacy, the conference publicly launched the report entitled “Right to Education of Afro-descendant and Indigenous Communities in the Americas” that it had previously presented at the Forum. The report addresses failures to fulfil obligations with respect to the right to education without discrimination within the Americas, focusing on Colombia, Guatemala and the Dominican Republic.",
   "themes": [
    "Equality & non-discrimination",
    "Reservations",
    "Right to education"
   ],
   "sdgs": [
    16,
    10
   ],
   "sdg_targets": [
    "16.7: Responsive, inclusive and representative decision-making",
    "16.3: Promote the rule of law and access to justice for all",
    "10.3: Ensure equal opportunities and end discrimination"
   ],
   "affected_persons": [
    "Minorities/ racial, ethnic, linguistic, religious or descent-based groups"
   ],
   "countries": [
    "Colombia",
    "Guatemala",
    "Dominican Republic",
    "Afghanistan"
   ]
  },
  {
   "id": "d16b76f0-da20-4cdb-a651-fa5adab7dc1c",
   "symbol": "CEDAW/C/AFG/CO/4",
   "doc_url": "https://docs.un.org/en/CEDAW/C/AFG/CO/4",
   "date": "2025-07-10",
   "year": 2025,
   "body": "CEDAW",
   "mechanism": "Treaty bodies",
   "type": "Concerns/Observations",
   "section": "Data collection and analysis",
   "text": "47. The Committee notes with concern the lack of data collection in many areas relevant to the implementation of the Convention.",
   "themes": [
    "Data collection & research"
   ],
   "sdgs": [
    17
   ],
   "sdg_targets": [
    "17.18: Enhance availability of reliable data"
   ],
   "affected_persons": [],
   "countries": [
    "Afghanistan"
   ]
  },
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
 ],
 "html_doc": [
  {
   "html": "<body>\n    <table>\n      <tr>\n        <td> <img src=\"\" /></td>\n        <td>\n          <p style=\"font-size:1.4em;\">United Nations</p>\n        </td>\n        <td>\n          <p>\n            <span style=\"font-size:2em;\">E</span>/C.12/GC/27</p>\n        </td>\n      </tr>\n      <tr>\n        <td> </td>\n        <td>\n          <p style=\"font-weight:bold;font-size:2em;\">Economic and Social Council</p>\n        </td>\n        <td>\n          <p>Distr.: General</p>\n          <p>6 November 2025</p>\n          <p>Original: English</p>\n        </td>\n      </tr>\n    </table>\n    <div class=\"content\">\n      <p style=\"font-weight:bold;font-size:1.2em;\">Committee on Economic, Social and Cultural Rights</p>\n      <h2 style=\"font-weight:bold;\">General comment No. 27 (2025) on economic, social and cultural rights andthe environmental dimension of sustainable development *</h2>\n      <h2>I.Introduction</h2>\n      <p>1.A clean, healthy and sustainable environment is an essential precondition for the enjoyment of economic, social and cultural rights. Nature is indispensable to human existence and well-being, as it not only supports life but also underpins ecological processes, including air and water quality, soil fertility, climate stability, pollination, and the mitigation of natural hazards. However, the accelerating and interconnected environmental challenges of our time, such as climate change, biodiversity loss and pollution, pose a serious threat to the ability of present and future generations to e\n<!-- … the rest of the document omitted in this sample -->"
  }
 ]
}
```

# USER MESSAGE

Build this app. Follow the plan below; where it says nothing, keep it simple.

# UN human rights recommendations dashboard: Kenya

## Context

The user is a diplomat, an NGO officer or a staff member of a national human rights institution preparing a meeting, a briefing or a report on Kenya. They need three things in a row: how much the UN mechanisms have said, about what, and the exact paragraph with its UN document symbol. Today they open the Universal Human Rights Index, export to a spreadsheet and lose an hour; or they quote from memory. The dashboard must be trustworthy enough to be read out in a meeting: every number says how it was computed, every row links to the UN document. The data is `WORKSHOP_DATA.uhri`; the country is `WORKSHOP_DATA.uhri.country`, never hard-coded.

## What I found in the data

The numbers below come from the file I examined while planning; the participant's file differs, and the app must compute all of its own numbers.

- 2,264 records from 31 documents (18 treaty-body, 9 Special Procedures, 4 UPR), dated 2007–2026, with no records in some years. The top-level `count` is a **string** ("2264"): compare with `Number(count)`.
- `symbol`, `doc_url`, `date`, `year`, `body`, `mechanism`, `type` and `text` are filled in every record. `section` only in 450 (treaty bodies and one mandate); `themes` in 2,249; `sdgs` in 1,816 (448 have none); `affected_persons` in 1,856.
- `body` has 16 values; UPR is nearly half the records; some mandates have a handful (one has a single record).
- `type`: 1,791 Recommendations, 471 Concerns/Observations, 2 Other.
- 90 theme labels; a record carries several, so theme counts sum to more than the record count. The most frequent theme ("Reservations", 691) is a legacy label: sampled records under it, all from 2007–2013, had nothing to do with reservations. The app must show, not hide, this: a year range per theme and the sample check.
- Paragraph numbers sit at the start of `text`: "71. The Committee…" in treaty-body records (681 records in the file start that way), "144.43 Abolish…" in every UPR record; many Special Procedures records are lettered items "(g) Develop…" with no number.
- UPR texts end with a semicolon and one or more States in parentheses, sometimes with spaces inside, sometimes nested ("(Venezuela (Bolivarian Republic of))"), sometimes several ("(Cabo Verde) (Slovenia) (Togo);"). 1,370 records end with a parenthesis, but treaty-body texts end with "(art. 15).", so State extraction must be limited to UPR.
- Texts run from 18 to about 2,500 characters (median about 230); a few 2007 records are chopped fragments joined with letters ("r) … r) …"). Two texts are exact duplicates of another record.

## The app, tab by tab

The app answers three questions, one per tab, and shows only what the open tab needs: **no view shows more than about seven things to click** (tabs, filter headings and buttons, not table rows or chart bars), and anything used rarely sits one click deeper. Three numbered tabs under the header, in this order.

**Header (always visible).** A monospace label "UHRI · Kenya", then the title in a large serif, "UN human rights recommendations and observations: Kenya". One line under it: source (`source`, linked to `source_url`), n records, n documents, first–last year, `built` date, and the hint "dated by document".

**Left rail: filters (always visible).** A narrow column headed "FILTERS" with "Clear all" at the right. Under it a big serif number, "n matching records" (`aria-live="polite"`, with "of N in the file"), and a thin red bar showing the share of the file. Active filters show as removable chips under the number. Every tab reads the same filtered set; all filters combine with AND. Three numbered headings, **each closed until clicked**, one open at a time (buttons with `aria-expanded`), shown on tabs 01 and 02; on 03 the rail keeps only the number, the bar and the chips.
- **01 Keyword**: a text box applied 300 ms after typing, hint "literal match, not synonyms".
- **02 Mechanism, body, type**: Mechanism (all / each value); Body or mandate (`body` values present in the chosen mechanism, each with its count); Type (all / each value present). A State select joins this heading when States are extracted.
- **03 Years and SDG**: Year from / to (two selects of the distinct years); SDG (goal number and name from `sdg_names`, only goals present in the data).

**01 Overview: what has the UN said, how much, and when?**
- A row of big serif numbers. The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`. Under the number, one line gives the breakdown per `type`, spelled as in the data. The Type filter (all / each `type` value present) starts on "all". Beside it: documents (distinct `symbol`) and years (min–max of `year`). Below, one tile per `mechanism` (records, documents, latest year, share of the filtered set). Every tile and figure has a one-line "How this is computed" note.
- FIG.01 "Ten most frequent themes among n filtered records": a horizontal Chart.js bar chart, bars ranked by value, count at the end of each bar. Clicking a bar adds that theme as a filter chip. Under the chart, a small table with the same ten rows: Theme | Records | % of filtered | Years (first–last year of the records carrying it), and the note that a record can carry several themes, so bars add up to more than n.
- FIG.02 "Records per year by mechanism": stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps.
- Last, a closed heading **Every check (n)**, a button with `aria-expanded`: the "Check this dashboard" panel (section "How the app checks itself"), one line per check.

**02 Records: which paragraph says it, and in which UN document?**
- One search field across the top ("Search n records, e.g. torture"), the same box as 01 Keyword. The caption gives rows shown of rows matching.
- The table. Columns: Date | Body | Symbol (linked to `doc_url`, opens in a new tab) | Para. | First line (the first 120 characters, cut at a word, with "…"). **Recommending State** (UPR rows only): the State or States named in parentheses at the end of the text, as a column in the table and as a filter (a select listing every State found, with counts). On tab 01, a small "see the States" link in the UPR tile opens a short list in place ("Ten States that made most recommendations to Kenya") with counts for the current filter. Treaty-body and Special Procedures rows show a dash in this column. Rows are sorted by `date` descending, then `body`, then paragraph number ascending (numeric, so 10 follows 9), then the order in the file. The caption says "newest first"; clicking the Date header reverses it. Keyword matches are highlighted with `<mark>`. Fifty rows at a time with "Show 50 more".
- Clicking a row (or pressing Enter on it) expands it in place: the paragraph number large in red, the full `text` verbatim, never shortened or paraphrased; the labels (`themes`, `sdgs` with names, `sdg_targets`, `affected_persons`, `section` when present); the "Copy citation" button; and "Open the UN document". **Copy citation** copies the short form `symbol, para. N` (for example "CEDAW/C/AFG/CO/4, para. 54"). When no paragraph number was found in the text, it copies the symbol alone and the button's label says "(no paragraph number in this extract)".

**03 Method & export: how was this made, and how do I take it with me?**
- How each number is computed, in five or six plain sentences.
- "Download CSV of the current filter": the visible columns plus the full text and labels, preceded by comment lines with the country, source, build date, the filters applied and the row count, generated in the browser with a Blob URL. "Copy summary": a plain-text paragraph with the headline numbers and the ten themes, for pasting into notes.
- The data source, licence line and build date.

**Footer (always visible, one line, small monospace).** "Built on OHCHR UHRI data · n records · source link", plus a "Credits" line if any shelf code was used.

## How every number is computed

- **Headline total** = `records.length`. The breakdown counts records per `type`, using the values exactly as spelled in the data (there may be a small "Other" group).
- **Documents** = number of distinct `symbol`. **Years** = minimum and maximum `year`.
- **Filters.** Mechanism, body, type: exact match on the field. Year: `year` inclusive between the two selects. SDG: `sdgs.includes(goal)` with `goal` a number. Keyword: trimmed, lower-cased; every word must occur as a substring of `text` or `symbol`. The filtered set feeds the tiles, both charts, the table and the export.
- **Theme counts.** For each record in the filtered set, each value in `themes` counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = min and max `year` of the filtered records carrying that theme.
- **Timeline** = records per `year` per `mechanism` in the filtered set, with zero for missing combinations.
- **Paragraph number** = the first match of `/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/` on `text`; the captured group is the number ("71" or "144.43"); no match means no number.
- **Recommending State.** Only for `mechanism` === "Universal Periodic Review". Take the trailing run of parenthesised groups with the regular expression `/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/` on `text`, then split that run into groups with `/\((?:[^()]|\([^()]*\))*\)/g`, strip the outer parentheses and trim. One group may hold a nested name such as "Venezuela (Bolivarian Republic of)"; several groups mean several States, and the record counts once for each. A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets "State not found". The text itself is never altered.
- **Citation** = `symbol` + ", para. " + paragraph number when one was found; otherwise `symbol`. UPR numbers keep their two-part form ("para. 144.43"). A small "Copied" confirmation appears for two seconds; the clipboard write is the only thing that leaves the page.
- **First line** = `text` up to 120 characters, cut at the last space before the limit, plus "…"; the full text is shown unchanged on expand.
- Nothing is estimated and no model is called. Every count is a loop over the records in JavaScript.

## How the app checks itself

The "Check this dashboard" panel, under the closed heading on the Overview tab, lists each check as one line: what was compared, the two values, and a pass mark or a red "check failed" with the values, never a hidden failure.

- **Record count.** `records.length` against `Number(uhri.count)`.
- **Partitions.** Counts per `mechanism`, per `body` and per `year` each sum to the record count.
- **Type partition.** The counts per `type` sum to the headline total.
- **Chart against table.** Each bar's value equals the count recomputed by a second loop over the filtered records; the ten rows under the chart show the same values; the largest bar is not larger than the filtered count.
- **Links.** Every record's `doc_url` starts with "https://docs.un.org/" and ends with its `symbol` (compared case-insensitively after decoding); the records that fail are listed.
- **Paragraph numbers.** Share of records with a number found, per mechanism; UPR is expected at 100%, and a lower figure is shown as a warning, not an error.
- **States found.** Number of UPR records with at least one State found, against the number of UPR records; the records without one are listed with their symbol, so the reader can see what the parentheses held instead.
- **Duplicates and gaps.** Distinct `id` equals the record count; the number of duplicate `text` values; records with no `themes`, no `sdgs`, no `affected_persons`, each shown as "not labelled".

## Edge cases and risks

- A filter that matches nothing: tiles show 0, the chart area shows "No records match" as text, the table caption says so; no error in the console.
- Years with no records appear as gaps on the timeline and are absent from the year selects; the from/to selects reject a reversed range by swapping it.
- `count` is a string; `sdgs` may be empty or missing; `section` is usually empty and is shown only when present; `type` may hold a small "Other" group.
- Theme bars add up to more than the record count; the note under the chart says so, and the percentages are of records, not of labels.
- A top theme may be a legacy label (in the file examined, the most frequent theme was wrong in every sampled record). The app never removes or renames a UN label; it shows the year range per theme and lets the reader judge a sample.
- A few UPR texts end with a parenthesis that is not a State (a list of examples, an article). The comma-and-length rule catches most; the check panel lists the rest. The State list is a count of recommendations, not of influence; two States can co-sponsor one line.
- Very short or chopped texts (2007 records) are shown as they are; the first-line column may then be the whole text.
- `date` is the document's date, not the date a recommendation was made or accepted; the header note says "dated by document".
- Keyword search is literal: "torture" does not find "ill-treatment". The hint under the box says so.
- Nothing leaves the browser except the clipboard write on "Copy"; there is no model call and no network request.

## Design and accessibility

What this app adds to the studio look and its accessibility:
- Red (#9b2335) also marks the share bar in the rail, the bars of FIG.01 (at 80%) and the large paragraph number in an open row. Big serif numbers: the matching count in the rail and the headline numbers on tab 01.
- Mechanism colours only on the tile dots and in FIG.02 (UPR #c2410c, Treaty bodies #0f766e, Special Procedures #7c3aed), always with a label or legend.
- Figure titles say what is counted and for which filter, with a "Source" line under each figure.
- Charts follow "Data visualisation: charts (formatting, labels, bar charts)" (UK Government Analysis Function): horizontal bars, ranked, horizontal text, and a table under the chart because a well-structured table can be as powerful as a chart.
- Tables follow "Data visualisation: tables" (Analysis Function): thousands separators, the same precision in a column, the source under the table.
- Keyboard: tabs are a `role="tablist"` with arrow-key navigation; filter headings and expandable rows are buttons with `aria-expanded`; the matching count is `aria-live="polite"`.
- Citations follow the Dag Hammarskjöld Library's advice: symbol as the key, pinpoint kept, parts formatted on copy.
- Transparency follows OHCHR's "Human Rights-Based Approach to Data": method stated at the point of use (each note at most two sentences), `affected_persons` shown on expand, missing labels shown as missing.

## Out of scope

No model calls and no summaries of what the UN "wants". No comparison with other countries (the file holds one). No follow-up or acceptance status of UPR recommendations (not in the data). No full names of bodies or mandates beyond the `body` label. No regional groups of recommending States. No server, no login, no PDF rendering.

## Sources consulted

- Dag Hammarskjöld Library, Ask DAG: how should I cite a UN document? — https://ask.un.org/faq/401380
- UK Government Analysis Function, Data visualisation: charts (formatting, labels, bar charts) — https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/
- UK Government Analysis Function, Data visualisation: tables — https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/
- OHCHR, A Human Rights-Based Approach to Data (guidance note) — https://www.ohchr.org/sites/default/files/Documents/Issues/HRIndicators/GuidanceNoteonApproachtoData.pdf

(Attached: Kenya: UN recommendations and observations → WORKSHOP_DATA.uhri)

# ASSISTANT MESSAGE (your earlier answer)

I built a three-tab dashboard on the UHRI file: an overview with counts, themes and a timeline, a records table with the full paragraph on click, and a method and export tab. Every number says how it is computed, and a closed "Every check" panel on the Overview tab compares the app's own numbers and shows any mismatch. Counts, filters and the recommending-State reading are all done by code in your browser; nothing is estimated.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN recommendations and observations dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5a554b;--warn:#8a5a00;
--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
a{color:var(--red);text-underline-offset:2px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.skip{position:absolute;left:-999px;top:0;background:var(--ink);color:var(--paper);padding:8px 12px;z-index:9}
.skip:focus{left:8px}
.wrap{max-width:1280px;margin:0 auto;padding:0 24px}
.lab{font:600 11px/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute)}
.mono{font-family:var(--mono)}
.mute{color:var(--mute)}
header.wrap{padding-top:22px;padding-bottom:14px}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 8px;letter-spacing:-.01em}
.src{margin:0;font-size:14px;color:var(--mute)}
.src a{color:var(--ink)}
/* tabs */
#tabs{display:flex;gap:0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);flex-wrap:wrap}
#tabs button{font:600 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;background:none;border:0;border-bottom:3px solid transparent;padding:14px 22px 11px 0;margin-right:10px;color:var(--ink);cursor:pointer}
#tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.layout{display:grid;grid-template-columns:264px minmax(0,1fr);gap:36px;padding-top:22px;padding-bottom:40px;align-items:start}
#rail{border-right:1px solid var(--rule);padding-right:22px}
@media(min-width:861px){#rail{position:sticky;top:8px;max-height:calc(100vh - 16px);overflow:auto}}
@media(max-width:860px){.layout{grid-template-columns:minmax(0,1fr);gap:18px}#rail{border-right:0;border-bottom:1px solid var(--rule);padding:0 0 14px}h1{font-size:28px}}
.rail-head{display:flex;justify-content:space-between;align-items:baseline}
.link{background:none;border:0;padding:2px 0;font:600 11px/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--red);cursor:pointer;text-decoration:underline;text-underline-offset:3px}
#mcount{margin:10px 0 6px}
#mnum{display:block;font:400 52px/1 var(--serif);font-variant-numeric:tabular-nums}
.sm{font-size:14px;color:var(--mute)}
.bar{height:4px;background:var(--rule);margin:8px 0 10px}
.bar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
.chip{font:13px/1.3 var(--sans);background:none;border:1px solid var(--red);color:var(--ink);padding:3px 8px;cursor:pointer;text-align:left;max-width:100%;overflow-wrap:anywhere}
.chip b{font:600 10px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--red);margin-right:4px}
#acc h3{margin:0;border-top:1px solid var(--rule)}
.acc-b{width:100%;text-align:left;background:none;border:0;padding:12px 0;font:600 12px/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink);cursor:pointer;display:flex;justify-content:space-between}
.acc-b[aria-expanded="true"]{color:var(--red)}
.acc-p{padding:0 0 14px}
.acc-p label{display:block;margin:10px 0 3px}
select,input[type=search],input[type=text]{width:100%;font:15px var(--sans);color:var(--ink);background:#fbf9f4;border:1px solid #b9b0a0;border-radius:0;padding:7px 8px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.hint{font:11px/1.4 var(--mono);color:var(--mute);margin-top:4px;display:block}
/* panels */
.q{font:400 24px/1.25 var(--serif);margin:0 0 16px}
.tiles3,.tilesM{display:grid;gap:0 28px;margin-bottom:8px}
.tiles3{grid-template-columns:repeat(3,minmax(0,1fr))}
.tilesM{grid-template-columns:repeat(auto-fit,minmax(230px,1fr));margin-top:6px}
@media(max-width:700px){.tiles3{grid-template-columns:minmax(0,1fr)}}
.tile{border-top:1px solid var(--rule);padding:10px 0 12px}
.big{font:400 48px/1.05 var(--serif);font-variant-numeric:tabular-nums;margin:4px 0}
.tile .mid{font:400 28px/1.1 var(--serif);font-variant-numeric:tabular-nums}
.how{font:11px/1.45 var(--mono);color:var(--mute);margin:6px 0 0}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.statelist{margin:8px 0 0;padding-top:8px;border-top:1px dotted var(--rule)}
.statelist h4{font:600 13px/1.3 var(--sans);margin:0 0 4px}
.statelist ol{margin:0;padding-left:22px;font-size:14px}
.statelist li span{float:right;font-variant-numeric:tabular-nums}
figure{margin:26px 0 0;padding-top:12px;border-top:1px solid var(--rule)}
figcaption h3{font:400 21px/1.25 var(--serif);margin:2px 0 8px}
.cwrap{position:relative;width:100%}
.empty{padding:18px 0;color:var(--mute);font-style:italic}
table{border-collapse:collapse;width:100%;font-size:15px}
caption{text-align:left;font:12px/1.4 var(--mono);color:var(--mute);padding:6px 0}
th{font:600 11px/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase;text-align:left;padding:8px 8px 6px 0;border-bottom:2px solid var(--ink);vertical-align:bottom;color:var(--ink)}
td{padding:8px 8px 8px 0;border-bottom:1px solid var(--rule);vertical-align:top;overflow-wrap:break-word}
td.nw{white-space:nowrap}
td:last-child,.full,dl.labels dd{overflow-wrap:anywhere}
.tw{overflow-x:auto}
th.n,td.n{text-align:right;font-variant-numeric:tabular-nums;padding-right:14px}
.thbtn{background:none;border:0;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;color:inherit;cursor:pointer}
.tb-btn{background:none;border:0;padding:0;font:inherit;color:var(--ink);text-align:left;cursor:pointer;text-decoration:underline dotted;text-underline-offset:3px}
.tb-btn:hover{color:var(--red)}
tr.row{cursor:pointer}
tr.row:hover td{background:#ebe5d6}
tr.row[aria-expanded="true"] td{border-bottom-color:transparent;background:#ebe5d6}
tr.detail td{background:#faf7f0;padding:14px 16px 18px;border-bottom:1px solid var(--ink)}
.dgrid{display:grid;grid-template-columns:140px minmax(0,1fr);gap:16px}
@media(max-width:700px){.dgrid{grid-template-columns:1fr}}
.pnum{font:400 46px/1 var(--serif);color:var(--red);font-variant-numeric:tabular-nums;white-space:nowrap}
.pnum.none{font:600 11px/1.4 var(--mono);color:var(--mute);letter-spacing:.08em;text-transform:uppercase}
.full{white-space:pre-wrap;margin:0 0 12px;max-width:80ch}
dl.labels{margin:0 0 12px;display:grid;grid-template-columns:130px minmax(0,1fr);gap:4px 12px;font-size:14px}
dl.labels dt{font:600 11px/1.6 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
dl.labels dd{margin:0}
.btn{font:600 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;background:none;border:1px solid var(--ink);color:var(--ink);padding:9px 12px;cursor:pointer;margin:0 10px 8px 0;text-decoration:none;display:inline-block}
.btn:hover{border-color:var(--red);color:var(--red)}
.copied{font:600 12px var(--mono);color:var(--red)}
mark{background:#f0d58f;color:var(--ink);padding:0 1px}
.sample td{background:#faf7f0;font-size:14px}
.sample ul{margin:0;padding:0;list-style:none}
.sample li{padding:3px 0}
.deep{margin-top:30px;border-top:1px solid var(--rule)}
.deep h3{margin:0}
.checks{list-style:none;margin:0;padding:0}
.checks li{padding:8px 0;border-bottom:1px solid var(--rule);font-size:14px}
.checks ul{margin:4px 0 0;padding-left:22px;font-size:13px}
.st{font:700 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;margin-right:8px}
.st.pass{color:var(--ink)}.st.fail{color:var(--red);text-decoration:underline}.st.warn{color:var(--warn)}.st.info{color:var(--mute)}
.bad{color:var(--red)}
.method p{max-width:75ch;margin:0 0 10px}
footer{border-top:1px solid var(--rule);padding-top:14px;padding-bottom:30px;font:11px/1.6 var(--mono);letter-spacing:.06em;color:var(--mute)}
footer a{color:var(--mute)}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="wrap">
  <div class="lab" id="hlab">UHRI</div>
  <h1 id="htitle">UN human rights recommendations and observations</h1>
  <p class="src" id="hsrc"></p>
</header>
<div class="wrap">
  <div role="tablist" aria-label="Dashboard sections" id="tabs">
    <button role="tab" id="t1" aria-controls="p1" aria-selected="true" tabindex="0">01 Overview</button>
    <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">02 Records</button>
    <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">03 Method &amp; export</button>
  </div>
</div>
<div class="wrap layout">
  <aside id="rail" aria-label="Filters">
    <div class="rail-head"><span class="lab">Filters</span><button class="link" id="clear" type="button">Clear all</button></div>
    <div id="mcount" aria-live="polite" aria-atomic="true"><span id="mnum">0</span><span class="sm"><span id="mtxt">matching records</span> <span id="mof"></span></span></div>
    <div class="bar" aria-hidden="true"><i id="mbar"></i></div>
    <div class="chips" id="chips"></div>
    <div id="acc">
      <h3><button class="acc-b" type="button" id="h1" aria-expanded="false" aria-controls="a1"><span>01 Keyword</span><span aria-hidden="true">+</span></button></h3>
      <div class="acc-p" id="a1" hidden>
        <label class="lab" for="q1">Words to find</label>
        <input id="q1" type="search" autocomplete="off">
        <span class="hint">literal match, not synonyms</span>
      </div>
      <h3><button class="acc-b" type="button" id="h2" aria-expanded="false" aria-controls="a2"><span>02 Mechanism, body, type</span><span aria-hidden="true">+</span></button></h3>
      <div class="acc-p" id="a2" hidden>
        <label class="lab" for="fm">Mechanism</label><select id="fm"></select>
        <label class="lab" for="fb">Body or mandate</label><select id="fb"></select>
        <label class="lab" for="ft">Type</label><select id="ft"></select>
        <div id="fsw"><label class="lab" for="fs">Recommending State (UPR)</label><select id="fs"></select></div>
      </div>
      <h3><button class="acc-b" type="button" id="h3" aria-expanded="false" aria-controls="a3"><span>03 Years and SDG</span><span aria-hidden="true">+</span></button></h3>
      <div class="acc-p" id="a3" hidden>
        <div class="pair"><div><label class="lab" for="yf">Year from</label><select id="yf"></select></div><div><label class="lab" for="yt">to</label><select id="yt"></select></div></div>
        <label class="lab" for="fg">SDG</label><select id="fg"></select>
        <span class="hint">dated by document</span>
      </div>
    </div>
  </aside>

  <main id="main">
    <section id="p1" role="tabpanel" aria-labelledby="t1">
      <h2 class="q">What has the UN said, how much, and when?</h2>
      <div class="tiles3" id="tiles"></div>
      <div class="tilesM" id="mtiles"></div>
      <figure id="fig1">
        <figcaption><span class="lab">FIG.01</span><h3 id="f1t">Ten most frequent themes</h3></figcaption>
        <div class="cwrap" id="c1wrap"><canvas id="c1" role="img" aria-label="Bar chart of the most frequent themes; the same numbers are in the table below"></canvas></div>
        <div class="empty" id="f1e" hidden></div>
        <p class="how">How this is computed: each theme label counts once per record in the filtered set, so a record with three themes is in three bars and the bars add up to more than the number of records. Percent = records with the label / filtered records. Click a bar or a theme name = filter.</p>
        <div id="f1tab"></div>
        <p class="how" id="f1src"></p>
      </figure>
      <figure id="fig2">
        <figcaption><span class="lab">FIG.02</span><h3 id="f2t">Records per year by mechanism</h3></figcaption>
        <div class="cwrap" id="c2wrap" style="height:300px"><canvas id="c2" role="img" aria-label="Stacked bar chart of records per year by mechanism"></canvas></div>
        <div class="empty" id="f2e" hidden></div>
        <p class="how">How this is computed: records per <code>year</code> and <code>mechanism</code> in the filtered set; every year from the first to the last is shown, so a missing bar is a year with no records. Years are those of the document.</p>
        <p class="how" id="f2src"></p>
      </figure>
      <div class="deep">
        <h3><button class="acc-b" type="button" id="chk" aria-expanded="false" aria-controls="checks"><span id="chkt">Every check</span><span aria-hidden="true">+</span></button></h3>
        <div id="checks" hidden></div>
      </div>
    </section>

    <section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
      <h2 class="q">Which paragraph says it, and in which UN document?</h2>
      <label class="lab" for="q2">Keyword</label>
      <input id="q2" type="search" autocomplete="off">
      <span class="hint">literal match, not synonyms</span>
      <div class="tw"><table id="tbl">
        <caption id="cap"></caption>
        <thead><tr>
          <th scope="col" id="thd" aria-sort="descending"><button class="thbtn" type="button" id="sortd"></button></th>
          <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="n">Para.</th><th scope="col">Recommending State</th><th scope="col">First line</th>
        </tr></thead>
        <tbody id="tb"></tbody>
      </table></div>
      <p><button class="btn" type="button" id="more">Show 50 more</button></p>
      <p class="how">How this is computed: rows are the filtered records, sorted by date, then body, then paragraph number (numeric), then file order. Click a row to read the full paragraph. State = names in the last parentheses of a UPR text; "State not found" when they do not look like States.</p>
      <p class="how" id="p2src"></p>
    </section>

    <section id="p3" role="tabpanel" aria-labelledby="t3" hidden>
      <h2 class="q">How was this made, and how do I take it with me?</h2>
      <div class="method">
        <p>Every number on this page is a count made by a loop over the records of the attached file, in your browser. Nothing is estimated, no model is called and nothing leaves the page except what you copy.</p>
        <p>Filters combine with AND. Mechanism, body, type and State match exactly; the year range is inclusive; SDG matches the goal number; every word of the keyword must occur literally in the text or in the document symbol; each theme chosen from the chart must be carried by the record.</p>
        <p>Themes: each label counts once per record, so theme counts add up to more than the number of records, and percentages are shares of records. A label that only appears in old years may be a legacy label: read its year range and its sample in FIG.01 before you rely on it.</p>
        <p>The paragraph number is the number at the start of the text (for example 71 or 144.43); texts that do not start with one have none. The recommending State is read only for Universal Periodic Review records from the last parentheses of the text; if they contain a comma or are longer than 60 characters, the record shows "State not found".</p>
        <p>Dates are the dates of the documents, not of the recommendations. This dashboard does not say whether a UPR recommendation was accepted, because the file does not contain it.</p>
        <p>The closed heading "Every check" on the Overview tab compares the app's own numbers with each other and lists what does not match.</p>
      </div>
      <div style="margin:16px 0 6px">
        <button class="btn" type="button" id="dl">Download CSV of the current filter</button>
        <button class="btn" type="button" id="cpcsv">Copy CSV text</button>
        <button class="btn" type="button" id="cpsum">Copy summary</button>
        <span class="copied" id="exst" role="status"></span>
      </div>
      <p class="how" id="exinfo"></p>
      <p class="how" id="p3src"></p>
    </section>
  </main>
</div>
<footer class="wrap" id="foot"></footer>

<script>
(function(){
'use strict';
var W=window.WORKSHOP_DATA||{},D=W.uhri;
function $(id){return document.getElementById(id)}
if(!D||!Array.isArray(D.records)){
  $('main').innerHTML='<p class="empty">No UHRI file is attached to this app. Drag the recommendations file from "Your files" into the chat and ask again.</p>';
  $('rail').hidden=true;$('tabs').hidden=true;return;
}
var UPR='Universal Periodic Review',NONE='\u0001none';
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function escRe(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
var NF=new Intl.NumberFormat('en-GB');
function fmt(n){return NF.format(n)}
function pc(a,b){return b?(a/b*100).toFixed(1)+'%':'–'}
function arr(x){return Array.isArray(x)?x.filter(function(v){return v!=null&&v!==''}):[]}
function url(u){return /^https?:\/\//i.test(u||'')}
function plural(n,w){return fmt(n)+' '+w+(n===1?'':'s')}

/* ---------- prepare the records ---------- */
var RUN=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/,GRP=/\((?:[^()]|\([^()]*\))*\)/g;
function findStates(t){
  var m=RUN.exec(t);if(!m)return [];
  var g=m[1].match(GRP);if(!g)return [];
  var out=[];
  for(var i=0;i<g.length;i++){
    var s=g[i].slice(1,-1).replace(/\s+/g,' ').trim();
    if(!s||s.indexOf(',')>-1||s.length>60)return [];
    if(out.indexOf(s)<0)out.push(s);
  }
  return out;
}
var recs=D.records.map(function(r,i){
  r=r||{};
  var text=typeof r.text==='string'?r.text:'';
  var y=parseInt(r.year,10);if(!isFinite(y))y=parseInt(String(r.date||'').slice(0,4),10);if(!isFinite(y))y=null;
  var m=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/.exec(text);
  var o={r:r,i:i,id:r.id,symbol:r.symbol||'',doc_url:r.doc_url||'',date:r.date||'',year:y,body:r.body||'',mech:r.mechanism||'',type:r.type||'',
    text:text,section:r.section||'',themes:arr(r.themes),sdgs:arr(r.sdgs).map(Number).filter(isFinite),targets:arr(r.sdg_targets),persons:arr(r.affected_persons),
    para:m?m[1]:''};
  o.pk=m?m[1].split('.').map(Number):null;
  o.states=o.mech===UPR?findStates(text):[];
  o.lt=text.toLowerCase();o.ls=o.symbol.toLowerCase();
  return o;
});
var N=recs.length,country=D.country||'this country',sdgNames=D.sdg_names||{};
var years=[],mechs=[],types=[],sdgGoals=[],bodyMech={},hasStates=false;
(function(){
  var ys={},mc={},tc={},sg={};
  recs.forEach(function(o){
    if(o.year!=null)ys[o.year]=1;
    mc[o.mech]=(mc[o.mech]||0)+1;tc[o.type]=(tc[o.type]||0)+1;
    o.sdgs.forEach(function(g){sg[g]=1});
    (bodyMech[o.mech]=bodyMech[o.mech]||{})[o.body]=1;
    if(o.states.length)hasStates=true;
  });
  years=Object.keys(ys).map(Number).sort(function(a,b){return a-b});
  function byCount(c){return Object.keys(c).sort(function(a,b){return c[b]-c[a]||a.localeCompare(b)}).filter(function(k){return k!==''})}
  mechs=byCount(mc);types=byCount(tc);
  sdgGoals=Object.keys(sg).map(Number).sort(function(a,b){return a-b});
})();
var MCOL={'Universal Periodic Review':'#c2410c','Treaty bodies':'#0f766e','Special Procedures':'#7c3aed'},FALL=['#6b7280','#a16207','#1d4ed8','#be185d'];
function colorOf(m){if(MCOL[m])return MCOL[m];var i=mechs.indexOf(m);return FALL[(i<0?0:i)%FALL.length]}
function dedupe(a){var s={};return a.filter(function(x){return s[x]?false:(s[x]=1)})}

/* ---------- filters ---------- */
var S={q:'',mech:'',body:'',type:'',state:'',yf:null,yt:null,sdg:'',themes:[]};
var words=[],hlRe=null,F=[],tab=1,shown=50,newestFirst=true,openRows={},sorted=null,statesOpen=false,sampleOpen='',charts={f1:null,f2:null},fig1Rows=[],fig2Info=null,timer=null;
function match(o,skip){
  var i;
  if(skip!=='q'){for(i=0;i<words.length;i++){if(o.lt.indexOf(words[i])<0&&o.ls.indexOf(words[i])<0)return false}}
  if(skip!=='mech'&&S.mech&&o.mech!==S.mech)return false;
  if(skip!=='body'&&S.body&&o.body!==S.body)return false;
  if(skip!=='type'&&S.type&&o.type!==S.type)return false;
  if(skip!=='state'&&S.state){if(S.state===NONE){if(o.mech!==UPR||o.states.length)return false}else if(o.states.indexOf(S.state)<0)return false}
  if(skip!=='years'&&(S.yf!=null||S.yt!=null)){if(o.year==null)return false;if(S.yf!=null&&o.year<S.yf)return false;if(S.yt!=null&&o.year>S.yt)return false}
  if(skip!=='sdg'&&S.sdg!==''&&o.sdgs.indexOf(Number(S.sdg))<0)return false;
  if(skip!=='themes'){for(i=0;i<S.themes.length;i++)if(o.themes.indexOf(S.themes[i])<0)return false}
  return true;
}
function facet(skip,keys){var m=new Map();recs.forEach(function(o){if(!match(o,skip))return;keys(o).forEach(function(k){m.set(k,(m.get(k)||0)+1)})});return m}
function countBy(list,fn){var m=new Map();list.forEach(function(o){var k=fn(o);m.set(k,(m.get(k)||0)+1)});return Array.from(m.entries()).sort(function(a,b){return b[1]-a[1]||String(a[0]).localeCompare(String(b[0]))})}
function sdgLabel(g){return 'SDG '+g+(sdgNames[String(g)]?' · '+sdgNames[String(g)]:'')}
function activeFilters(){
  var a=[];
  if(S.q.trim())a.push({k:'Keyword',v:S.q.trim(),rm:function(){S.q=''}});
  if(S.mech)a.push({k:'Mechanism',v:S.mech,rm:function(){S.mech='';S.body=''}});
  if(S.body)a.push({k:'Body',v:S.body,rm:function(){S.body=''}});
  if(S.type)a.push({k:'Type',v:S.type,rm:function(){S.type=''}});
  if(S.state)a.push({k:'State',v:S.state===NONE?'State not found':S.state,rm:function(){S.state=''}});
  if(S.yf!=null||S.yt!=null)a.push({k:'Years',v:(S.yf!=null?S.yf:years[0])+'–'+(S.yt!=null?S.yt:years[years.length-1]),rm:function(){S.yf=null;S.yt=null}});
  if(S.sdg!=='')a.push({k:'SDG',v:sdgLabel(S.sdg),rm:function(){S.sdg=''}});
  S.themes.forEach(function(t){a.push({k:'Theme',v:t,rm:function(){S.themes=S.themes.filter(function(x){return x!==t})}})});
  return a;
}
function filterText(){var a=activeFilters();return a.length?a.map(function(f){return f.k+': '+f.v}).join('; '):'none'}

/* ---------- helpers on the filtered set ---------- */
function themeRows(list){
  var m=new Map();
  list.forEach(function(o){
    var seen={};
    o.themes.forEach(function(t){
      if(seen[t])return;seen[t]=1;
      var e=m.get(t);if(!e){e={t:t,n:0,y0:null,y1:null};m.set(t,e)}
      e.n++;
      if(o.year!=null){if(e.y0==null||o.year<e.y0)e.y0=o.year;if(e.y1==null||o.year>e.y1)e.y1=o.year}
    });
  });
  return Array.from(m.values()).sort(function(a,b){return b.n-a.n||a.t.localeCompare(b.t)}).slice(0,10);
}
function yearRange(list){var a=list.filter(function(o){return o.year!=null}).map(function(o){return o.year});if(!a.length)return null;return [Math.min.apply(null,a),Math.max.apply(null,a)]}
function docsOf(list){var s={};list.forEach(function(o){s[o.symbol]=1});return Object.keys(s).length}
function cmp(a,b){
  if(a.date!==b.date)return (a.date<b.date?1:-1)*(newestFirst?1:-1);
  var c=a.body.localeCompare(b.body);if(c)return c;
  if(a.pk&&b.pk){if(a.pk[0]!==b.pk[0])return a.pk[0]-b.pk[0];var x=a.pk[1]||0,y=b.pk[1]||0;if(x!==y)return x-y}
  else if(a.pk)return -1;else if(b.pk)return 1;
  return a.i-b.i;
}
function getSorted(){if(!sorted)sorted=F.slice().sort(cmp);return sorted}
function firstLine(t){if(t.length<=120)return t;var c=t.slice(0,120),k=c.lastIndexOf(' ');if(k>0)c=c.slice(0,k);return c+'…'}
function hl(s){
  if(!hlRe)return esc(s);
  return s.split(hlRe).map(function(p,i){return i%2?'<mark>'+esc(p)+'</mark>':esc(p)}).join('');
}
function stateCell(o){return o.mech!==UPR?'–':(o.states.length?esc(o.states.join('; ')):'<span class="mute">State not found</span>')}
function docLink(o){return url(o.doc_url)?'<a href="'+esc(o.doc_url)+'" target="_blank" rel="noopener">'+esc(o.symbol||o.doc_url)+'</a>':esc(o.symbol)}
function citation(o){return o.para?o.symbol+', para. '+o.para:o.symbol}
function srcLine(){return 'Source: '+(D.source?esc(D.source):'OHCHR UHRI')+(url(D.source_url)?' (<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">link</a>)':'')+'. Built '+esc(D.built||'(date not given)')+'. Counts are made in your browser on the '+fmt(N)+' records of the attached file.'}

/* ---------- header, footer ---------- */
(function(){
  var yr=yearRange(recs);
  document.title='UN recommendations and observations: '+country;
  $('hlab').textContent='UHRI · '+country;
  $('htitle').textContent='UN human rights recommendations and observations: '+country;
  $('hsrc').innerHTML='Source: '+(url(D.source_url)?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source||D.source_url)+'</a>':esc(D.source||'OHCHR UHRI'))+
    ' · '+plural(N,'record')+' · '+plural(docsOf(recs),'document')+' · '+(yr?yr[0]+'–'+yr[1]:'no years')+' · built '+esc(D.built||'(date not given)')+' · dated by document';
  $('foot').innerHTML='Built on OHCHR UHRI data · '+fmt(N)+' records · '+(url(D.source_url)?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source</a>':'source: '+esc(D.source||'OHCHR UHRI'));
  $('q2').placeholder='Search '+fmt(N)+' records, e.g. torture';
  $('f1src').innerHTML=srcLine();$('f2src').innerHTML=srcLine();$('p2src').innerHTML=srcLine();
  $('p3src').innerHTML=srcLine()+' Licence: the file states none; check the terms of use on the source page before you republish. UN documents open on docs.un.org.';
  $('fsw').hidden=!hasStates;
})();

/* ---------- rail ---------- */
function fillSelect(sel,opts,value){
  sel.innerHTML=opts.map(function(o){return '<option value="'+esc(o.v)+'">'+esc(o.l)+'</option>'}).join('');
  sel.value=value;
}
function optsFrom(m,keys,all,zeros){
  var list=keys.slice().sort(function(a,b){return (m.get(b)||0)-(m.get(a)||0)||a.localeCompare(b)});
  var o=[{v:'',l:all}];
  list.forEach(function(k){var n=m.get(k)||0;if(n||zeros)o.push({v:k,l:k+' ('+fmt(n)+')'})});
  return o;
}
function syncRail(){
  var n=F.length;
  $('mnum').textContent=fmt(n);
  $('mtxt').textContent=n===1?'matching record':'matching records';
  $('mof').textContent='of '+fmt(N)+' in the file';
  $('mbar').style.width=(N?n/N*100:0)+'%';
  var ch=activeFilters();
  $('chips').innerHTML=ch.map(function(f,i){return '<button type="button" class="chip" data-ix="'+i+'" aria-label="Remove filter '+esc(f.k+': '+f.v)+'"><b>'+esc(f.k)+'</b>'+esc(f.v)+' <span aria-hidden="true">×</span></button>'}).join('');
  var ae=document.activeElement;
  if(ae!==$('q1'))$('q1').value=S.q;
  if(ae!==$('q2'))$('q2').value=S.q;
  var fm=facet('mech',function(o){return [o.mech]});
  fillSelect($('fm'),optsFrom(fm,mechs,'All mechanisms',true),S.mech);
  var bodies=Object.keys(bodyMech).filter(function(m){return !S.mech||m===S.mech}).reduce(function(a,m){return a.concat(Object.keys(bodyMech[m]))},[]);
  bodies=dedupe(bodies).filter(function(b){return b!==''});
  fillSelect($('fb'),optsFrom(facet('body',function(o){return [o.body]}),bodies,'All bodies and mandates',true),S.body);
  fillSelect($('ft'),optsFrom(facet('type',function(o){return [o.type]}),types,'All types',true),S.type);
  if(hasStates){
    var fs=facet('state',function(o){return o.mech!==UPR?[]:(o.states.length?o.states:[NONE])});
    var nn=fs.get(NONE)||0;fs.delete(NONE);
    var keys=Array.from(fs.keys());if(S.state&&S.state!==NONE&&keys.indexOf(S.state)<0)keys.push(S.state);
    var so=optsFrom(fs,keys,'All States',false);
    if(nn||S.state===NONE)so.splice(1,0,{v:NONE,l:'State not found ('+fmt(nn)+')'});
    fillSelect($('fs'),so,S.state);
  }
  var yo=years.map(function(y){return {v:String(y),l:String(y)}});
  fillSelect($('yf'),yo,String(S.yf!=null?S.yf:years[0]));
  fillSelect($('yt'),yo,String(S.yt!=null?S.yt:years[years.length-1]));
  fillSelect($('fg'),[{v:'',l:'Any goal'}].concat(sdgGoals.map(function(g){return {v:String(g),l:g+' · '+(sdgNames[String(g)]||'')}})),String(S.sdg));
}
$('chips').addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;activeFilters()[+b.getAttribute('data-ix')].rm();update()});
$('clear').addEventListener('click',function(){S={q:'',mech:'',body:'',type:'',state:'',yf:null,yt:null,sdg:'',themes:[]};update()});
['h1','h2','h3'].forEach(function(id,k){
  $(id).addEventListener('click',function(){
    var open=this.getAttribute('aria-expanded')==='true';
    ['h1','h2','h3'].forEach(function(h,j){
      var o=(j===k)&&!open;
      $(h).setAttribute('aria-expanded',o);$('a'+(j+1)).hidden=!o;
      $(h).lastChild.textContent=o?'−':'+';
    });
  });
});
function onQ(e){var v=e.target.value;clearTimeout(timer);timer=setTimeout(function(){S.q=v;update()},300)}
$('q1').addEventListener('input',onQ);$('q2').addEventListener('input',onQ);
$('fm').addEventListener('change',function(){S.mech=this.value;if(S.body&&S.mech&&!(bodyMech[S.mech]||{})[S.body])S.body='';update()});
$('fb').addEventListener('change',function(){S.body=this.value;update()});
$('ft').addEventListener('change',function(){S.type=this.value;update()});
$('fs').addEventListener('change',function(){S.state=this.value;update()});
$('fg').addEventListener('change',function(){S.sdg=this.value;update()});
function yearChange(){
  var a=Number($('yf').value),b=Number($('yt').value);
  if(a>b){var t=a;a=b;b=t}
  S.yf=a>years[0]?a:null;S.yt=b<years[years.length-1]?b:null;update();
}
$('yf').addEventListener('change',yearChange);$('yt').addEventListener('change',yearChange);
function addTheme(t){if(S.themes.indexOf(t)<0){S.themes.push(t);update()}}

/* ---------- tabs ---------- */
function setTab(n,focus){
  tab=n;
  [1,2,3].forEach(function(k){
    var t=$('t'+k);t.setAttribute('aria-selected',k===n);t.tabIndex=k===n?0:-1;$('p'+k).hidden=k!==n;
  });
  $('acc').hidden=n===3;
  if(focus)$('t'+n).focus();
  renderPanel();
}
[1,2,3].forEach(function(k){$('t'+k).addEventListener('click',function(){setTab(k)})});
$('tabs').addEventListener('keydown',function(e){
  var k={ArrowRight:tab%3+1,ArrowLeft:(tab+1)%3+1,Home:1,End:3}[e.key];
  if(k){e.preventDefault();setTab(k,true)}
});

/* ---------- overview ---------- */
var valueLabels={id:'valueLabels',afterDatasetsDraw:function(chart){
  var ctx=chart.ctx;
  chart.data.datasets.forEach(function(ds,di){
    chart.getDatasetMeta(di).data.forEach(function(bar,i){
      ctx.save();ctx.fillStyle='#1d1b18';ctx.font='600 13px ui-monospace,Menlo,Consolas,monospace';ctx.textBaseline='middle';
      ctx.fillText(fmt(ds.data[i]),bar.x+6,bar.y);ctx.restore();
    });
  });
}};
function wrapLabel(s){
  if(s.length<=44)return s;
  var out=[],cur='';
  s.split(' ').forEach(function(w){if(cur&&(cur+' '+w).length>44){out.push(cur);cur=w}else cur=cur?cur+' '+w:w});
  if(cur)out.push(cur);return out;
}
function destroy(k){if(charts[k]){charts[k].destroy();charts[k]=null}}
function renderOverview(){
  var n=F.length,tc=countBy(F,function(o){return o.type||'(no type)'}),yr=yearRange(F);
  $('tiles').innerHTML=
    '<div class="tile"><div class="lab">Records, all types</div><div class="big">'+fmt(n)+'</div>'+
      '<div class="sm">'+(n?tc.map(function(e){return fmt(e[1])+' '+esc(e[0])}).join(' · '):'No records match.')+'</div>'+
      '<p class="how">How this is computed: number of records in the filtered set; the line counts them per <code>type</code>, spelled as in the data.</p></div>'+
    '<div class="tile"><div class="lab">Documents</div><div class="big">'+fmt(docsOf(F))+'</div><div class="sm">distinct document symbols</div>'+
      '<p class="how">How this is computed: distinct <code>symbol</code> among the filtered records.</p></div>'+
    '<div class="tile"><div class="lab">Years</div><div class="big">'+(yr?yr[0]+'–'+yr[1]:'–')+'</div><div class="sm">first and last year, dated by document</div>'+
      '<p class="how">How this is computed: smallest and largest <code>year</code> in the filtered set.</p></div>';
  $('mtiles').innerHTML=mechs.map(function(m){
    var sub=F.filter(function(o){return o.mech===m}),y=yearRange(sub);
    var h='<div class="tile"><div class="lab"><span class="dot" style="background:'+colorOf(m)+'"></span>'+esc(m)+'</div><div class="mid">'+fmt(sub.length)+' <span class="sm">records</span></div>'+
      '<div class="sm">'+plural(docsOf(sub),'document')+' · latest year '+(y?y[1]:'–')+' · '+pc(sub.length,n)+' of the filtered set</div>';
    if(m===UPR&&hasStates)h+='<button type="button" class="link" data-act="states" aria-expanded="'+statesOpen+'">see the States</button>'+(statesOpen?statesHtml():'');
    return h+'<p class="how">How this is computed: records, distinct symbols and last year of this mechanism in the filtered set; share = records / filtered records.</p></div>';
  }).join('');
  renderFig1();renderFig2();renderChecks();
}
function statesHtml(){
  var c={};F.forEach(function(o){o.states.forEach(function(s){c[s]=(c[s]||0)+1})});
  var top=Object.keys(c).sort(function(a,b){return c[b]-c[a]||a.localeCompare(b)}).slice(0,10);
  return '<div class="statelist"><h4>Ten States that made most recommendations to '+esc(country)+'</h4>'+
    (top.length?'<ol>'+top.map(function(s){return '<li>'+esc(s)+' <span>'+fmt(c[s])+'</span></li>'}).join('')+'</ol>':'<div class="empty">No States found in the filtered records.</div>')+
    '<p class="how">A count of recommendation lines, not of influence; a line backed by several States counts once for each.</p></div>';
}
$('p1').addEventListener('click',function(e){
  var b=e.target.closest('[data-act]');if(!b)return;
  var a=b.getAttribute('data-act');
  if(a==='states'){statesOpen=!statesOpen;renderOverview()}
  else if(a==='theme')addTheme(b.getAttribute('data-t'));
  else if(a==='sample'){var t=b.getAttribute('data-t');sampleOpen=sampleOpen===t?'':t;renderFig1Table()}
});
function renderFig1(){
  var n=F.length;
  fig1Rows=themeRows(F);
  $('f1t').textContent=(fig1Rows.length===10?'Ten most frequent themes':'Most frequent themes ('+fig1Rows.length+')')+' among '+fmt(n)+' filtered records';
  destroy('f1');
  var empty=!fig1Rows.length;
  $('c1wrap').hidden=empty;$('f1e').hidden=!empty;
  $('f1e').textContent=n?'No theme labels on these records.':'No records match.';
  if(!empty){
    if(typeof Chart==='undefined'){$('c1wrap').hidden=true;$('f1e').hidden=false;$('f1e').textContent='The chart library did not load; the table below has the same numbers.'}
    else{
      $('c1wrap').style.height=(fig1Rows.length*40+20)+'px';
      var names=fig1Rows.map(function(r){return r.t});
      charts.f1=new Chart($('c1'),{type:'bar',data:{labels:names.map(wrapLabel),datasets:[{data:fig1Rows.map(function(r){return r.n}),backgroundColor:'rgba(155,35,53,.8)',borderWidth:0,barThickness:18}]},
        options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:60}},
          plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return fmt(c.parsed.x)+' records · click = filter'}}}},
          scales:{x:{display:false,beginAtZero:true,grid:{display:false}},y:{grid:{display:false},border:{display:false},ticks:{color:'#1d1b18',font:{size:12}}}},
          onClick:function(ev,els){if(els&&els.length)addTheme(names[els[0].index])},
          onHover:function(ev,els){ev.native&&ev.native.target&&(ev.native.target.style.cursor=els&&els.length?'pointer':'default')}},
        plugins:[valueLabels]});
    }
  }
  renderFig1Table();
}
function renderFig1Table(){
  var n=F.length;
  if(!fig1Rows.length){$('f1tab').innerHTML='';return}
  var h='<table id="t1tab"><caption>Same ten rows as the chart. A record can carry several themes.</caption><thead><tr><th scope="col">Theme <span class="mute">(click = filter)</span></th><th scope="col" class="n">Records</th><th scope="col" class="n">% of filtered</th><th scope="col">Years (first–last)</th><th scope="col">Check</th></tr></thead><tbody>';
  fig1Rows.forEach(function(r){
    h+='<tr><td><button type="button" class="tb-btn" data-act="theme" data-t="'+esc(r.t)+'">'+esc(r.t)+'</button></td><td class="n cnt">'+fmt(r.n)+'</td><td class="n">'+pc(r.n,n)+'</td><td>'+(r.y0==null?'–':(r.y0===r.y1?r.y0:r.y0+'–'+r.y1))+'</td>'+
      '<td><button type="button" class="tb-btn" data-act="sample" data-t="'+esc(r.t)+'" aria-expanded="'+(sampleOpen===r.t)+'">sample</button></td></tr>';
    if(sampleOpen===r.t)h+='<tr class="sample"><td colspan="5">'+sampleHtml(r.t)+'</td></tr>';
  });
  $('f1tab').innerHTML=h+'</tbody></table>';
}
function sampleHtml(t){
  var l=F.filter(function(o){return o.themes.indexOf(t)>-1}).sort(function(a,b){return a.date<b.date?-1:a.date>b.date?1:a.i-b.i});
  var pick=dedupe([0,Math.floor((l.length-1)/2),l.length-1].map(String)).map(Number),names=['oldest','middle','newest'];
  var idx=[0,Math.floor((l.length-1)/2),l.length-1];
  return '<span class="lab">Sample check: up to three records under this label (oldest, middle, newest by date)</span><ul>'+pick.map(function(k){
    var o=l[k],nm=names[idx.indexOf(k)];
    return '<li><span class="mono">'+esc(nm)+' · '+esc(o.date)+'</span> · '+docLink(o)+(o.para?', para. '+esc(o.para):'')+' — '+esc(firstLine(o.text))+'</li>';
  }).join('')+'</ul>';
}
function renderFig2(){
  var yr=yearRange(F);
  destroy('f2');fig2Info=null;
  var empty=!yr;
  $('c2wrap').hidden=empty;$('f2e').hidden=!empty;
  $('f2e').textContent='No records match.';
  $('f2t').textContent='Records per year by mechanism among '+fmt(F.length)+' filtered records';
  if(empty)return;
  var labels=[];for(var y=yr[0];y<=yr[1];y++)labels.push(y);
  var present=mechs.filter(function(m){return F.some(function(o){return o.mech===m})});
  var cnt={};present.forEach(function(m){cnt[m]={}});
  var noYear=0;
  F.forEach(function(o){if(o.year==null){noYear++;return}if(cnt[o.mech])cnt[o.mech][o.year]=(cnt[o.mech][o.year]||0)+1});
  var sets=present.map(function(m){return {label:m,data:labels.map(function(y){return cnt[m][y]||0}),backgroundColor:colorOf(m),borderWidth:0}});
  fig2Info={sum:sets.reduce(function(a,s){return a+s.data.reduce(function(x,v){return x+v},0)},0),noYear:noYear};
  if(typeof Chart==='undefined'){$('c2wrap').hidden=true;$('f2e').hidden=false;$('f2e').textContent='The chart library did not load.';return}
  charts.f2=new Chart($('c2'),{type:'bar',data:{labels:labels,datasets:sets},
    options:{responsive:true,maintainAspectRatio:false,animation:false,
      plugins:{legend:{position:'top',align:'start',labels:{color:'#1d1b18',boxWidth:12,font:{size:12}}},tooltip:{mode:'index',intersect:false}},
      scales:{x:{stacked:true,grid:{display:false},ticks:{color:'#1d1b18',maxRotation:0,autoSkip:true}},y:{stacked:true,beginAtZero:true,grid:{color:'#e3dccd'},border:{display:false},ticks:{color:'#1d1b18',precision:0}}}}});
  $('c2').setAttribute('aria-label','Stacked bar chart of '+fmt(F.length)+' records per year, '+yr[0]+' to '+yr[1]+', by mechanism');
}

/* ---------- the app checks itself ---------- */
function computeChecks(){
  var C=[],n=F.length;
  function add(name,st,text,list){C.push({name:name,st:st,text:text,list:list||null})}
  var cnt=Number(D.count);
  add('Record count',recs.length===cnt?'pass':'fail','records.length = '+fmt(recs.length)+' · count in the file = '+(isFinite(cnt)?fmt(cnt):esc(D.count)));
  function part(label,fn){
    var m={};recs.forEach(function(o){var k=fn(o);m[k]=(m[k]||0)+1});
    var s=Object.keys(m).reduce(function(a,k){return a+m[k]},0);
    add('Partition per '+label,s===recs.length?'pass':'fail',Object.keys(m).length+' groups add up to '+fmt(s)+' · records = '+fmt(recs.length));
  }
  part('mechanism',function(o){return o.mech});part('body',function(o){return o.body});part('year',function(o){return o.year==null?'(no year)':o.year});
  var ts=countBy(F,function(o){return o.type}).reduce(function(a,e){return a+e[1]},0);
  add('Type partition',ts===n?'pass':'fail','counts per type add up to '+fmt(ts)+' · headline total = '+fmt(n)+' (filtered set)');
  // chart against table
  var rc=fig1Rows.map(function(r){return F.filter(function(o){return o.themes.indexOf(r.t)>-1}).length});
  var tabv=[].slice.call(document.querySelectorAll('#t1tab td.cnt')).map(function(td){return Number(td.textContent.replace(/[^\d]/g,''))});
  var barv=charts.f1?charts.f1.data.datasets[0].data:null;
  var badBar=barv?fig1Rows.filter(function(r,i){return barv[i]!==rc[i]}).map(function(r){return r.t}):[];
  add('Chart against recount',!fig1Rows.length?'info':(!barv?'warn':(badBar.length?'fail':'pass')),!fig1Rows.length?'no theme bars in this filter':(!barv?'chart not drawn, so not compared':'each of '+rc.length+' bars equals a second count over the filtered records'+(badBar.length?' · differs: '+badBar.map(esc).join('; '):'')));
  var badTab=fig1Rows.filter(function(r,i){return tabv[i]!==rc[i]}).length+(tabv.length===fig1Rows.length?0:1);
  add('Table under the chart',!fig1Rows.length?'info':(badTab?'fail':'pass'),!fig1Rows.length?'no rows in this filter':'the '+tabv.length+' table rows show the same values as the recount'+(badTab?' · '+badTab+' differ':''));
  var mx=Math.max.apply(null,[0].concat(rc));
  add('Largest bar',mx<=n?'pass':'fail','largest bar = '+fmt(mx)+' · filtered records = '+fmt(n));
  if(fig2Info)add('Timeline total',fig2Info.sum+fig2Info.noYear===n?'pass':'fail','FIG.02 adds up to '+fmt(fig2Info.sum)+(fig2Info.noYear?' + '+fmt(fig2Info.noYear)+' without a year':'')+' · filtered records = '+fmt(n));
  // links
  var badL=recs.filter(function(o){
    if(o.doc_url.indexOf('https://docs.un.org/')!==0||!o.symbol)return true;
    var u=o.doc_url;try{u=decodeURIComponent(u)}catch(e){}
    return u.toLowerCase().slice(-o.symbol.length)!==o.symbol.toLowerCase();
  });
  add('Links',badL.length?'fail':'pass',badL.length?fmt(badL.length)+' of '+fmt(N)+' records have a doc_url that does not start with https://docs.un.org/ or does not end with the symbol':'all '+fmt(N)+' doc_url values start with https://docs.un.org/ and end with the symbol',
    badL.slice(0,15).map(function(o){return esc(o.symbol||'(no symbol)')+' → '+esc(o.doc_url||'(no link)')}).concat(badL.length>15?['and '+fmt(badL.length-15)+' more']:[]));
  // paragraph numbers
  mechs.forEach(function(m){
    var s=recs.filter(function(o){return o.mech===m}),f=s.filter(function(o){return o.para}).length;
    add('Paragraph numbers · '+m,m===UPR&&f<s.length?'warn':'info',fmt(f)+' of '+fmt(s.length)+' records have a number found ('+pc(f,s.length)+')'+(m===UPR?' · expected 100%':''));
  });
  // states
  var up=recs.filter(function(o){return o.mech===UPR}),found=up.filter(function(o){return o.states.length}),lost=up.filter(function(o){return !o.states.length});
  add('States found',lost.length?'warn':'pass',fmt(found.length)+' of '+fmt(up.length)+' UPR records have at least one State found'+(lost.length?' · without a State, with what the last parentheses hold instead:':''),
    lost.slice(0,15).map(function(o){var t=o.text.slice(-70);return esc(o.symbol)+' — …'+esc(t)}).concat(lost.length>15?['and '+fmt(lost.length-15)+' more']:[]));
  // duplicates and gaps
  var ids={};recs.forEach(function(o){ids[o.id]=1});var di=Object.keys(ids).length;
  add('Distinct ids',di===N?'pass':'fail',fmt(di)+' distinct id values · records = '+fmt(N));
  var tx={};recs.forEach(function(o){tx[o.text]=(tx[o.text]||0)+1});
  var dups=Object.keys(tx).filter(function(k){return tx[k]>1});
  add('Duplicate texts',dups.length?'warn':'pass',fmt(dups.length)+' text values occur more than once (kept as they are)',dups.slice(0,10).map(function(k){return esc(k.slice(0,90))+(k.length>90?'…':'')+' ×'+tx[k]}));
  [['themes','themes'],['sdgs','sdgs'],['affected_persons','persons']].forEach(function(p){
    var k=recs.filter(function(o){return !o[p[1]].length}).length;
    add('Not labelled · '+p[0],'info',fmt(k)+' of '+fmt(N)+' records have no '+p[0]+' ('+pc(k,N)+')');
  });
  return C;
}
function renderChecks(){
  var C=computeChecks(),bad=C.filter(function(c){return c.st==='fail'}).length;
  $('chkt').innerHTML='Every check ('+C.length+')'+(bad?' <span class="bad">· '+bad+' failed</span>':'');
  var lab={pass:'✓ pass',fail:'✗ check failed',warn:'! warning',info:'· note'};
  $('checks').innerHTML='<p class="lab" style="margin:12px 0 4px">How the app checks itself</p><ol class="checks">'+C.map(function(c){
    return '<li><span class="st '+c.st+'">'+lab[c.st]+'</span><b>'+esc(c.name)+'</b>: '+c.text+(c.list&&c.list.length?'<ul>'+c.list.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul>':'')+'</li>';
  }).join('')+'</ol>';
}
$('chk').addEventListener('click',function(){
  var o=this.getAttribute('aria-expanded')!=='true';
  this.setAttribute('aria-expanded',o);$('checks').hidden=!o;this.lastChild.textContent=o?'−':'+';
});

/* ---------- records ---------- */
function detailHtml(o){
  var lab=function(k,v){return '<dt>'+k+'</dt><dd>'+(v||'<span class="mute">not labelled</span>')+'</dd>'};
  var li=function(a,f){return a.length?a.map(function(x){return esc(f?f(x):x)}).join('; '):''};
  return '<tr class="detail" data-d="'+o.i+'"><td colspan="6"><div class="dgrid"><div>'+(o.para?'<div class="pnum" aria-label="Paragraph '+esc(o.para)+'">'+esc(o.para)+'</div>':'<div class="pnum none">no paragraph number</div>')+'</div><div>'+
    '<p class="full">'+hl(o.text)+'</p>'+
    '<dl class="labels"><dt>Document</dt><dd>'+docLink(o)+' · '+esc(o.body)+' · '+esc(o.mech)+' · '+esc(o.type)+' · '+esc(o.date)+'</dd>'+
      (o.section?'<dt>Section</dt><dd>'+esc(o.section)+'</dd>':'')+
      lab('Themes',li(o.themes))+lab('SDGs',li(o.sdgs,sdgLabel))+lab('SDG targets',li(o.targets))+lab('Affected persons',li(o.persons))+'</dl>'+
    '<button type="button" class="btn" data-act="copy" data-i="'+o.i+'">Copy citation'+(o.para?'':' (no paragraph number in this extract)')+'</button>'+
    (url(o.doc_url)?'<a class="btn" href="'+esc(o.doc_url)+'" target="_blank" rel="noopener">Open the UN document</a>':'')+
    '<span class="copied" role="status"></span></div></div></td></tr>';
}
function rowHtml(o){
  return '<tr class="row" tabindex="0" aria-expanded="'+(!!openRows[o.i])+'" data-i="'+o.i+'"><td class="nw">'+esc(o.date)+'</td><td>'+esc(o.body)+'</td><td class="nw">'+docLink(o)+'</td><td class="n nw">'+(o.para?esc(o.para):'–')+'</td><td>'+stateCell(o)+'</td><td>'+hl(firstLine(o.text))+'</td></tr>'+(openRows[o.i]?detailHtml(o):'');
}
var byI={};recs.forEach(function(o){byI[o.i]=o});
function renderRecords(){
  var l=getSorted(),n=l.length,k=Math.min(shown,n);
  $('sortd').textContent='Date '+(newestFirst?'▾':'▴');
  $('thd').setAttribute('aria-sort',newestFirst?'descending':'ascending');
  $('sortd').setAttribute('aria-label','Date, sorted '+(newestFirst?'newest first':'oldest first')+'. Activate to reverse.');
  $('cap').textContent=n?'Showing '+fmt(k)+' of '+fmt(n)+' matching records, '+(newestFirst?'newest first':'oldest first')+'. Click a row to read the paragraph.':'0 of '+fmt(N)+' records match these filters.';
  var h='';for(var i=0;i<k;i++)h+=rowHtml(l[i]);
  $('tb').innerHTML=h||'<tr><td colspan="6" class="empty">No records match.</td></tr>';
  $('more').hidden=k>=n;
  $('more').textContent='Show '+Math.min(50,n-k)+' more';
}
$('more').addEventListener('click',function(){shown+=50;renderRecords()});
$('sortd').addEventListener('click',function(){newestFirst=!newestFirst;sorted=null;shown=50;renderRecords()});
function toggleRow(tr){
  var i=+tr.getAttribute('data-i'),o=byI[i],open=!openRows[i];
  if(open){openRows[i]=1;tr.insertAdjacentHTML('afterend',detailHtml(o))}
  else{delete openRows[i];var d=tr.nextElementSibling;if(d&&d.getAttribute('data-d')==String(i))d.remove()}
  tr.setAttribute('aria-expanded',open);
}
$('tb').addEventListener('click',function(e){
  var cp=e.target.closest('[data-act="copy"]');
  if(cp){var o=byI[+cp.getAttribute('data-i')];copyText(citation(o),cp.parentNode.querySelector('.copied'));return}
  if(e.target.closest('a,button,.detail'))return;
  var tr=e.target.closest('tr.row');if(tr)toggleRow(tr);
});
$('tb').addEventListener('keydown',function(e){
  if((e.key==='Enter'||e.key===' ')&&e.target.classList&&e.target.classList.contains('row')){e.preventDefault();toggleRow(e.target)}
});
function copyText(t,note){
  function ok(){if(note){note.textContent='Copied';setTimeout(function(){note.textContent=''},2000)}}
  function fallback(){
    var ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();
    var done=false;try{done=document.execCommand('copy')}catch(e){}
    document.body.removeChild(ta);
    if(done)ok();else if(note){note.textContent='Could not copy: select the text and copy it by hand'}
  }
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(ok,fallback);else fallback();
}

/* ---------- method and export ---------- */
function renderMethod(){
  $('exinfo').textContent='The CSV has '+fmt(F.length)+' rows ('+filterText()+'), in the order of the table on 02 Records. It starts with comment lines (#) with the country, source, build date, filters and row count.';
}
function csvText(){
  var l=getSorted(),q=function(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'};
  var out=['# '+country+': UN recommendations and observations (OHCHR UHRI)','# Source: '+(D.source||'')+' '+(D.source_url||''),'# Built: '+(D.built||'not given'),'# Filters applied: '+filterText(),'# Rows: '+l.length+' of '+N+' records in the file'];
  out.push(['date','mechanism','body','type','symbol','doc_url','paragraph','recommending_states','section','first_line','text','themes','sdgs','sdg_targets','affected_persons'].join(','));
  l.forEach(function(o){
    out.push([o.date,o.mech,o.body,o.type,o.symbol,o.doc_url,o.para,o.mech===UPR?(o.states.length?o.states.join('; '):'State not found'):'',o.section,firstLine(o.text),o.text,o.themes.join(' | '),o.sdgs.join(' | '),o.targets.join(' | '),o.persons.join(' | ')].map(q).join(','));
  });
  return out.join('\r\n')+'\r\n';
}
$('dl').addEventListener('click',function(){
  var blob=new Blob(['﻿'+csvText()],{type:'text/csv;charset=utf-8'}),u=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=u;a.download='uhri-'+String(country).toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-'+new Date().toISOString().slice(0,10)+'.csv';
  document.body.appendChild(a);a.click();document.body.removeChild(a);setTimeout(function(){URL.revokeObjectURL(u)},1000);
  $('exst').textContent='Prepared '+fmt(F.length)+' rows';setTimeout(function(){$('exst').textContent=''},3000);
});
$('cpcsv').addEventListener('click',function(){copyText(csvText(),$('exst'))});
$('cpsum').addEventListener('click',function(){
  var n=F.length,yr=yearRange(F),tc=countBy(F,function(o){return o.type||'(no type)'}),mc=countBy(F,function(o){return o.mech});
  var t=country+': UN recommendations and observations (OHCHR UHRI, built '+(D.built||'date not given')+'). Filters: '+filterText()+'. '+fmt(n)+' of '+fmt(N)+' records match, from '+plural(docsOf(F),'document')+(yr?', '+yr[0]+'–'+yr[1]+' (dated by document)':'')+'. '+
    'By type: '+(tc.map(function(e){return fmt(e[1])+' '+e[0]}).join(', ')||'none')+'. By mechanism: '+(mc.map(function(e){return fmt(e[1])+' '+e[0]}).join(', ')||'none')+'. '+
    'Ten most frequent themes (a record can carry several): '+(themeRows(F).map(function(r){return r.t+' '+fmt(r.n)+' ('+pc(r.n,n)+')'}).join('; ')||'none')+'. Counted in the browser from the attached file.';
  copyText(t,$('exst'));
});

/* ---------- go ---------- */
function renderPanel(){
  if(tab===1)renderOverview();else if(tab===2)renderRecords();else renderMethod();
}
function update(){
  words=S.q.trim().toLowerCase().split(/\s+/).filter(Boolean);
  hlRe=words.length?new RegExp('('+words.slice().sort(function(a,b){return b.length-a.length}).map(escRe).join('|')+')','gi'):null;
  F=recs.filter(function(o){return match(o)});
  shown=50;sorted=null;
  syncRail();renderPanel();
}
update();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a tab "Check a quotation". I paste a passage I wrote (a briefing, a submission, an email) that quotes UN recommendations and observations to Kenya. For every quotation in quotation marks ("…", “…”, „…”, «…») of five words or more that has a citation within 60 characters of it (a UN document symbol, with or without a paragraph number), check it against the records in the file, with code only: compare words, ignoring case and punctuation; an ellipsis or a bracketed change [ ] splits a quotation into parts, and every part of three words or more must match. Give each quotation one verdict: ✓ correct (the words are in a record of the cited document, at the cited paragraph when one is given; the paragraph number is the number at the start of the record's text, when it has one); ≈ the words are right but the citation is not (show the correct symbol and paragraph, linked to the document); ✗ not in the data (the words are in no record). Never use a model: say on screen that the same text always gets the same verdicts. To try it at once, offer a sample passage built from the file when the tab opens: one correct quotation, one with a wrong paragraph or document, and one that is invented.

(Attached: Kenya: UN recommendations and observations → WORKSHOP_DATA.uhri)
