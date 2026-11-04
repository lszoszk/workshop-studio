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
 ]
}
```

# USER MESSAGE

Build this app. Follow the plan below; where it says nothing, keep it simple.

# UN human rights recommendations dashboard: Kenya

## Context

The user is a diplomat, an NGO officer or a staff member of a national human rights institution preparing a meeting, a briefing or a report on Kenya. They need three things in a row: how much the UN mechanisms have said, about what, and the exact paragraph with its UN document symbol. Today they open the Universal Human Rights Index, export to a spreadsheet and lose an hour; or they quote from memory. The dashboard must be trustworthy enough to be read out in a meeting: every number says how it was computed, every row links to the UN document, and the UN's own labels can be checked on a random sample, because the labels are the weakest part of the data. The data is `WORKSHOP_DATA.uhri`; the country is `WORKSHOP_DATA.uhri.country`, never hard-coded.

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

The app answers four questions, one per tab, and shows only what the open tab needs: **no view shows more than about seven things to click** (tabs, filter headings and buttons, not table rows or chart bars), and anything used rarely sits one click deeper. Four numbered tabs under the header, in this order.

**Header (always visible).** A monospace label "UHRI · Kenya", then the title in a large serif, "UN human rights recommendations and observations: Kenya". One line under it: source (`source`, linked to `source_url`), n records, n documents, first–last year, `built` date, and the hint "dated by document".

**Left rail: filters (always visible).** A narrow column headed "FILTERS" with "Clear all" at the right. Under it a big serif number, "n matching records" (`aria-live="polite"`, with "of N in the file"), and a thin red bar showing the share of the file. Active filters show as removable chips under the number. Every tab reads the same filtered set; all filters combine with AND. Three numbered headings, **each closed until clicked**, one open at a time (buttons with `aria-expanded`), shown on tabs 01 and 02; on 03 and 04 the rail keeps only the number, the bar and the chips.
- **01 Keyword**: a text box applied 300 ms after typing, hint "literal match, not synonyms".
- **02 Mechanism, body, type**: Mechanism (all / each value); Body or mandate (`body` values present in the chosen mechanism, each with its count); Type (all / each value present). A State select joins this heading when States are extracted.
- **03 Years and SDG**: Year from / to (two selects of the distinct years); SDG (goal number and name from `sdg_names`, only goals present in the data).

**01 Overview: what has the UN said, how much, and when?**
- A row of big serif numbers. The first tile counts **all records** in the file: recommendations, concerns/observations and any other `type`. Under the number, one line gives the breakdown per `type`, spelled as in the data. The Type filter (all / each `type` value present) starts on "all". Beside it: documents (distinct `symbol`) and years (min–max of `year`). Below, one tile per `mechanism` (records, documents, latest year, share of the filtered set). Every tile and figure has a one-line "How this is computed" note.
- FIG.01 "Ten most frequent themes among n filtered records": a horizontal Chart.js bar chart, bars ranked by value, count at the end of each bar. Clicking a bar adds that theme as a filter chip. Under the chart, a small table with the same ten rows: Theme | Records | % of filtered | Years (first–last year of the records carrying it), and the note that a record can carry several themes, so bars add up to more than n.
- FIG.02 "Records per year by mechanism": stacked bars for the current filter; every year from the first to the last appears, so empty years are visible gaps.
- Nothing else on this tab.

**02 Records: which paragraph says it, and in which UN document?**
- One search field across the top ("Search n records, e.g. torture"), the same box as 01 Keyword. The caption gives rows shown of rows matching.
- The table. Columns: Date | Body | Symbol (linked to `doc_url`, opens in a new tab) | Para. | First line (the first 120 characters, cut at a word, with "…"). **Recommending State** (UPR rows only): the State or States named in parentheses at the end of the text, as a column in the table and as a filter (a select listing every State found, with counts). On tab 01, a small "see the States" link in the UPR tile opens a short list in place ("Ten States that made most recommendations to Kenya") with counts for the current filter. Treaty-body and Special Procedures rows show a dash in this column. Rows are sorted by `date` descending, then `body`, then paragraph number ascending (numeric, so 10 follows 9), then the order in the file. The caption says "newest first"; clicking the Date header reverses it. Keyword matches are highlighted with `<mark>`. Fifty rows at a time with "Show 50 more".
- Clicking a row (or pressing Enter on it) expands it in place: the paragraph number large in red, the full `text` verbatim, never shortened or paraphrased; the labels (`themes`, `sdgs` with names, `sdg_targets`, `affected_persons`, `section` when present); the "Copy citation" button; and "Open the UN document". **Copy citation** copies the short form `symbol, para. N` (for example "CEDAW/C/AFG/CO/4, para. 54"). When no paragraph number was found in the text, it copies the symbol alone and the button's label says "(no paragraph number in this extract)".

**03 Check: can I trust these numbers?**
- The "Check this dashboard" panel (section "How the app checks itself"), one line per check.
- Below it the random-sample label check: "Check 10 at random" draws the cards (then "Draw again" and "Draw with this seed", the seed box and the tally). The ten cards are listed as one line each, one open at a time.

**04 Method & export: how was this made, and how do I take it with me?**
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

The "Check this dashboard" panel lists each check as one line: what was compared, the two values, and a pass mark or a red "check failed" with the values, never a hidden failure.

- **Record count.** `records.length` against `Number(uhri.count)`.
- **Partitions.** Counts per `mechanism`, per `body` and per `year` each sum to the record count.
- **Type partition.** The counts per `type` sum to the headline total.
- **Chart against table.** Each bar's value equals the count recomputed by a second loop over the filtered records; the ten rows under the chart show the same values; the largest bar is not larger than the filtered count.
- **Links.** Every record's `doc_url` starts with "https://docs.un.org/" and ends with its `symbol` (compared case-insensitively after decoding); the records that fail are listed.
- **Paragraph numbers.** Share of records with a number found, per mechanism; UPR is expected at 100%, and a lower figure is shown as a warning, not an error.
- **States found.** Number of UPR records with at least one State found, against the number of UPR records; the records without one are listed with their symbol, so the reader can see what the parentheses held instead.
- **Duplicates and gaps.** Distinct `id` equals the record count; the number of duplicate `text` values; records with no `themes`, no `sdgs`, no `affected_persons`, each shown as "not labelled".
- **Random-sample label check.** Ten records drawn from the current filter with a seeded generator (mulberry32; the seed is shown in a box, default 1, with "Draw again" and "Draw with this seed"), each as a card: symbol linked to `doc_url`, paragraph number, the full verbatim text. Each card shows the paragraph's `themes` as chips under the verbatim text and three buttons: **Fits**, **Doesn't fit**, **Unsure**. One verdict per card is about the themes as a set. A line above the cards says: "This is your judgement of the UN's labels; nothing is sent anywhere."
- **Sample tally.** "Themes: x fit, y don't, z unsure of 10 judged", updated as the reader clicks, with the seed used, so a colleague can draw the same ten. The tally is the reader's judgement, labelled as such; the app never changes a UN label.

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

I built a four-tab dashboard on your file: Overview (counts, top themes, records per year), Records (every paragraph with its UN symbol and a copyable citation), Check (the app's own checks plus a random sample of the UN's theme labels) and Method & export. Filters sit in the left rail and every tab reads the same filtered set. Everything is counted in your browser; nothing is sent anywhere.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5b564c;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 var(--sans)}
a{color:var(--ink);text-decoration-color:var(--red);text-underline-offset:2px}
a:hover{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
[hidden]{display:none!important}
.wrap{max-width:1320px;margin:0 auto;padding:22px 28px 14px}
.lab{font:600 11.5px/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:0}
.mute{color:var(--mute)}
header h1{font:400 clamp(26px,3.6vw,42px)/1.12 var(--serif);margin:6px 0 8px;max-width:980px}
.meta{margin:0;color:var(--mute);font-size:15px}
.tabs{display:flex;flex-wrap:wrap;gap:2px;margin-top:18px;border-bottom:1px solid var(--rule)}
.tabs button{font:600 12px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;background:none;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:13px 16px;color:var(--mute);cursor:pointer}
.tabs button b{font-weight:700}
.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tabs button:hover{color:var(--ink)}
.layout{display:grid;grid-template-columns:268px minmax(0,1fr);gap:30px;margin-top:22px;align-items:start}
.rail{border-right:1px solid var(--rule);padding-right:22px}
.railhead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}
.linkbtn{background:none;border:0;padding:0;font:600 11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--red);text-decoration:underline;text-underline-offset:3px;cursor:pointer;text-align:left}
.big{font:400 56px/1 var(--serif);font-variant-numeric:tabular-nums}
.matchlab{font-size:15px;margin-top:4px}
.sharebar{height:4px;background:var(--rule);margin:10px 0 12px}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip{font:12px/1.3 var(--mono);color:var(--red);background:none;border:1px solid var(--red);border-radius:999px;padding:3px 10px;cursor:pointer;text-align:left}
.chip:hover{background:var(--red);color:var(--paper)}
.acch{margin:0;border-top:1px solid var(--rule)}
.acch button{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:0;padding:12px 0;font:600 12px/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink);cursor:pointer;text-align:left}
.acch b{color:var(--red);margin-right:6px}
.acch .cnt{color:var(--red);margin-left:6px}
.accp{padding:0 0 14px}
.accp .lab{display:block;margin:10px 0 4px}
input,select{font:16px/1.3 var(--sans);width:100%;padding:8px 9px;border:1px solid #8c8577;background:#fffdf8;color:var(--ink);border-radius:2px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hint{font:12px/1.4 var(--mono);color:var(--mute);margin:6px 0 0}
.panel{min-width:0}
.panel>.lab{margin-bottom:2px}
h2{font:400 clamp(22px,2.4vw,30px)/1.2 var(--serif);margin:0 0 18px}
h3{font:400 22px/1.25 var(--serif);margin:0 0 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:22px 30px;margin-bottom:26px}
.tile{border-top:1px solid var(--ink);padding-top:8px;min-width:0}
.tile .n{font:400 48px/1.05 var(--serif);margin:4px 0 2px;font-variant-numeric:tabular-nums}
.tile .sub{margin:0;font-size:15px}
.how{font:12px/1.5 var(--mono);color:var(--mute);margin:6px 0 0;max-width:80ch}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:7px;vertical-align:-1px}
.statesbox{margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.statesbox h4{font:400 17px/1.3 var(--serif);margin:0 0 6px}
.statesbox ol{margin:0 0 6px;padding-left:24px;font-size:15px}
figure.fig{margin:34px 0 0;border-top:1px solid var(--ink);padding-top:10px}
.chartbox{position:relative;margin:10px 0 8px}
.empty{margin:0;padding:24px 0;color:var(--mute)}
.scroll{overflow-x:auto}
table.data{border-collapse:collapse;width:100%;margin-top:10px}
table.data caption{caption-side:top;text-align:left;font:600 11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);padding-bottom:6px}
table.data th{font:600 11.5px/1.3 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);text-align:left;padding:8px 10px;border-bottom:1px solid var(--ink);vertical-align:bottom}
table.data td{padding:9px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
table.data .num,table.data th.num{text-align:right;font-variant-numeric:tabular-nums}
.nw{white-space:nowrap}
.sorter{background:none;border:0;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;color:var(--ink);cursor:pointer;text-decoration:underline;text-decoration-color:var(--red);text-underline-offset:3px}
.rowx{cursor:pointer}
.rowx:hover td{background:rgba(29,27,24,.04)}
.rowbtn{background:none;border:0;padding:0;font:inherit;color:inherit;text-align:left;cursor:pointer;width:100%}
.rowbtn::before{content:"+";color:var(--red);font-family:var(--mono);margin-right:8px}
.rowbtn[aria-expanded="true"]::before{content:"\2013"}
mark{background:rgba(155,35,53,.16);color:inherit;padding:0 1px}
.det td{background:#faf7f0}
.detail{display:grid;grid-template-columns:minmax(70px,130px) 1fr;gap:18px;padding:10px 4px}
.pn{font:400 52px/1 var(--serif);color:var(--red)}
.full{margin:0 0 12px;white-space:pre-wrap;max-width:78ch}
.dl{display:grid;grid-template-columns:150px 1fr;gap:6px;margin:6px 0}
.dl dt{padding-top:4px}
.dl dd{margin:0}
.tag{display:inline-block;border:1px solid var(--rule);padding:1px 8px;margin:0 6px 6px 0;font-size:14px;background:var(--paper)}
.btn{font:600 12px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:10px 14px;border:1px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{border-color:var(--red);color:var(--red)}
.btn[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.btn.primary{background:var(--ink);color:var(--paper)}
.btn.primary:hover{background:var(--red);border-color:var(--red);color:var(--paper)}
.ok{font:12px var(--mono);color:var(--red);margin:0 10px 0 8px}
.actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:14px 0 6px}
.more{margin:14px 0 4px}
.searchrow{max-width:640px;margin-bottom:6px}
.searchrow .lab{display:block;margin-bottom:4px}
ol.checks{list-style:none;margin:10px 0 30px;padding:0;border-top:1px solid var(--ink)}
.chk{display:grid;grid-template-columns:118px 1fr;gap:12px;padding:11px 0;border-bottom:1px solid var(--rule)}
.chk .mark{font:600 12px/1.5 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.chk.fail{border-left:3px solid var(--red);padding-left:9px}
.chk.fail .mark{color:var(--red)}
.chk.warn .mark{font-style:italic}
.vals{color:var(--ink)}
details{margin-top:6px;font-size:15px}
summary{cursor:pointer;font:600 12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--red)}
ul.lst{margin:6px 0 0;padding-left:20px;max-height:260px;overflow:auto;font-size:14px}
ol.cards{list-style:none;margin:10px 0 0;padding:0;border-top:1px solid var(--ink)}
.card{border-bottom:1px solid var(--rule)}
.cardline{display:flex;gap:12px;align-items:baseline;padding:9px 0;flex-wrap:wrap}
.cn{font:600 12px var(--mono);color:var(--red);min-width:22px}
.cardbtn{flex:1 1 260px;background:none;border:0;padding:0;font:inherit;color:inherit;text-align:left;cursor:pointer}
.cardbtn::before{content:"+";color:var(--red);font-family:var(--mono);margin-right:8px}
.cardbtn[aria-expanded="true"]::before{content:"\2013"}
.vd{font:12px var(--mono);color:var(--mute)}
.carddet{padding:4px 0 16px 34px}
.sample-ctl{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;margin:12px 0 8px}
.sample-ctl .seed{width:110px}
.tally{font:600 13px/1.5 var(--mono);margin:8px 0 0}
.method li{margin-bottom:8px;max-width:80ch}
dl.src{display:grid;grid-template-columns:150px 1fr;gap:6px 14px;margin:8px 0 0}
dl.src dt{padding-top:3px}
dl.src dd{margin:0}
footer{margin-top:40px;border-top:1px solid var(--rule);padding:12px 0 6px;font:12px/1.5 var(--mono);color:var(--mute)}
@media(max-width:860px){.layout{grid-template-columns:1fr}.rail{border-right:0;padding-right:0;border-bottom:1px solid var(--rule);padding-bottom:12px}.wrap{padding:16px}.chk{grid-template-columns:1fr}.dl,dl.src{grid-template-columns:1fr}.detail{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="lab" id="hLab">UHRI</div>
  <h1 id="hTitle">UN human rights recommendations and observations</h1>
  <p class="meta" id="hMeta"></p>
</header>
<div class="tabs" role="tablist" aria-label="Dashboard sections" id="tabs"></div>

<div class="layout">
<aside class="rail" aria-label="Filters">
  <div class="railhead"><span class="lab">Filters</span><button type="button" class="linkbtn" data-act="clear">Clear all</button></div>
  <div id="matchLive" aria-live="polite" aria-atomic="true">
    <div class="big" id="matchN">0</div>
    <div class="matchlab">matching records <span class="mute" id="matchOf"></span></div>
  </div>
  <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
  <div class="chips" id="chips"></div>
  <div id="accs">
    <h3 class="acch"><button type="button" id="ah-kw" aria-expanded="false" aria-controls="ac-kw" data-act="acc" data-k="kw"><span><b>01</b>Keyword<span class="cnt" id="an-kw"></span></span><span aria-hidden="true">+</span></button></h3>
    <div class="accp" id="ac-kw" role="region" aria-labelledby="ah-kw" hidden>
      <label class="lab" for="kwRail">Words (all must match)</label>
      <input id="kwRail" type="search" autocomplete="off" placeholder="e.g. torture">
      <p class="hint">literal match, not synonyms</p>
    </div>
    <h3 class="acch"><button type="button" id="ah-mbt" aria-expanded="false" aria-controls="ac-mbt" data-act="acc" data-k="mbt"><span><b>02</b>Mechanism, body, type<span class="cnt" id="an-mbt"></span></span><span aria-hidden="true">+</span></button></h3>
    <div class="accp" id="ac-mbt" role="region" aria-labelledby="ah-mbt" hidden>
      <label class="lab" for="mechSel">Mechanism</label><select id="mechSel"></select>
      <label class="lab" for="bodySel">Body or mandate</label><select id="bodySel"></select>
      <label class="lab" for="typeSel">Type</label><select id="typeSel"></select>
      <div id="stateWrap"><label class="lab" for="stateSel">Recommending State (UPR only)</label><select id="stateSel"></select></div>
    </div>
    <h3 class="acch"><button type="button" id="ah-ys" aria-expanded="false" aria-controls="ac-ys" data-act="acc" data-k="ys"><span><b>03</b>Years and SDG<span class="cnt" id="an-ys"></span></span><span aria-hidden="true">+</span></button></h3>
    <div class="accp" id="ac-ys" role="region" aria-labelledby="ah-ys" hidden>
      <div class="two">
        <div><label class="lab" for="fromSel">Year from</label><select id="fromSel"></select></div>
        <div><label class="lab" for="toSel">Year to</label><select id="toSel"></select></div>
      </div>
      <label class="lab" for="sdgSel">SDG</label><select id="sdgSel"></select>
    </div>
  </div>
</aside>

<main>
<section class="panel" id="p-ov" role="tabpanel" aria-labelledby="t-ov">
  <p class="lab">01 · Overview</p>
  <h2>What has the UN said, how much, and when?</h2>
  <div class="tiles" id="tiles1"></div>
  <div class="tiles" id="tiles2"></div>
  <figure class="fig">
    <p class="lab">FIG.01</p>
    <h3 id="fig1t"></h3>
    <div class="chartbox" id="box1"><canvas id="c1" role="img" aria-label="Ranked horizontal bars of the ten most frequent themes"></canvas><p class="empty" id="c1e" hidden></p></div>
    <div class="scroll">
    <table class="data" id="themeTable">
      <caption>The same ten themes as a table</caption>
      <thead><tr><th scope="col">Theme <span style="text-transform:none;letter-spacing:0">(click = filter)</span></th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col" class="num">Years (first–last)</th></tr></thead>
      <tbody id="themeRows"></tbody>
    </table>
    </div>
    <p class="how" id="fig1n"></p>
    <p class="how">A theme confined to early years may be a legacy label that no longer describes its text. <button type="button" class="linkbtn" data-act="goto" data-t="chk">Judge a sample of the labels on 03 Check</button></p>
    <p class="how" id="fig1s"></p>
  </figure>
  <figure class="fig">
    <p class="lab">FIG.02</p>
    <h3 id="fig2t"></h3>
    <div class="chartbox" style="height:310px"><canvas id="c2" role="img" aria-label="Stacked bars of records per year by mechanism"></canvas><p class="empty" id="c2e" hidden></p></div>
    <p class="how" id="fig2n"></p>
    <p class="how" id="fig2s"></p>
  </figure>
</section>

<section class="panel" id="p-rec" role="tabpanel" aria-labelledby="t-rec" hidden>
  <p class="lab">02 · Records</p>
  <h2>Which paragraph says it, and in which UN document?</h2>
  <div class="searchrow"><label class="lab" for="kwMain">Search</label><input id="kwMain" type="search" autocomplete="off" placeholder="Search records, e.g. torture"><p class="hint">literal match, not synonyms · same box as 01 Keyword</p></div>
  <div class="scroll">
  <table class="data" id="recTable">
    <caption id="recCap"></caption>
    <thead><tr>
      <th scope="col"><button type="button" class="sorter" data-act="sortdate" id="dateSort" aria-label="Date: click to reverse the order">Date ▼</button></th>
      <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line <span style="text-transform:none;letter-spacing:0">(click a row to open it)</span></th><th scope="col">Recommending State</th>
    </tr></thead>
    <tbody id="recBody"></tbody>
  </table>
  </div>
  <div class="more"><button type="button" class="btn" id="moreBtn" data-act="more">Show 50 more</button></div>
  <p class="how" id="recSrc"></p>
</section>

<section class="panel" id="p-chk" role="tabpanel" aria-labelledby="t-chk" hidden>
  <p class="lab">03 · Check</p>
  <h2>Can I trust these numbers?</h2>
  <p class="lab">How the app checks itself</p>
  <h3>Check this dashboard</h3>
  <p class="how" id="checkSum"></p>
  <ol class="checks" id="checks"></ol>
  <p class="lab">Random-sample label check</p>
  <h3>Do the UN's theme labels fit the paragraphs?</h3>
  <p>This is your judgement of the UN's labels; nothing is sent anywhere.</p>
  <div class="sample-ctl">
    <div class="seed"><label class="lab" for="seed">Seed</label><input id="seed" type="number" min="0" step="1" value="1"></div>
    <button type="button" class="btn primary" id="drawBtn" data-act="draw">Check 10 at random</button>
    <button type="button" class="btn" data-act="seeddraw">Draw with this seed</button>
  </div>
  <p class="hint" id="sampleHint"></p>
  <p class="tally" id="tally" aria-live="polite"></p>
  <ol class="cards" id="cards"></ol>
</section>

<section class="panel" id="p-met" role="tabpanel" aria-labelledby="t-met" hidden>
  <p class="lab">04 · Method &amp; export</p>
  <h2>How was this made, and how do I take it with me?</h2>
  <h3>How each number is computed</h3>
  <ol class="method">
    <li>Every number is a loop over the records of the file you attached; nothing is estimated, no model is called, and nothing leaves the page except the text you choose to copy.</li>
    <li>A record is one paragraph of a UN document. Documents are counted as distinct symbols, and years come from the date of the document, not from the moment a recommendation was made.</li>
    <li>Filters combine with AND. Mechanism, body and type match exactly, the year range is inclusive, an SDG matches when the goal is among the record's SDGs, and a keyword matches when every word occurs in the text or the symbol (literal, not synonyms).</li>
    <li>Themes, SDGs and affected persons are the UN's own labels. A record can carry several themes, so theme counts add up to more than the number of records; the app never removes or renames a label.</li>
    <li>The paragraph number is the number at the start of the text. The recommending State is read only from UPR records, from the parentheses that end the text; where nothing fits, the row says State not found.</li>
    <li>A citation is the symbol plus ", para." and the number; where no number was found it is the symbol alone.</li>
  </ol>
  <h3 style="margin-top:26px">Take it with you</h3>
  <p class="hint" id="expInfo"></p>
  <div class="actions">
    <button type="button" class="btn primary" data-act="csv">Download CSV of the current filter</button>
    <button type="button" class="btn" data-act="copysum">Copy summary</button><span class="ok" id="expStatus" role="status"></span>
  </div>
  <h3 style="margin-top:26px">The data</h3>
  <dl class="src" id="srcList"></dl>
</section>
</main>
</div>

<footer id="foot"></footer>
</div>

<script>
(function(){
'use strict';
var D=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.uhri)||{};
var RAW=Array.isArray(D.records)?D.records:[];
var COUNTRY=D.country?String(D.country):'this country';
var SDG_NAMES=D.sdg_names||{};
var UPR='Universal Periodic Review';
var COLORS={};COLORS[UPR]='#c2410c';COLORS['Treaty bodies']='#0f766e';COLORS['Special Procedures']='#7c3aed';
var OTHERC='#6b6558';
var PAGE=50;
var PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
var TAIL_RE=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
var GROUP_RE=/\((?:[^()]|\([^()]*\))*\)/g;

function $(id){return document.getElementById(id);}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function fmt(n){return Number(n).toLocaleString('en-US');}
function pct(a,b){return (b?100*a/b:0).toFixed(1)+'%';}
function arr(v){return Array.isArray(v)?v:[];}
function str(v){return v==null?'':String(v);}
function cnt(){return Object.create(null);}
function uniq(a){return a.filter(function(x,i){return a.indexOf(x)===i;});}
function safeUrl(u){return /^https?:\/\//i.test(u)?u:'';}
function colorOf(m){return COLORS[m]||OTHERC;}
function mlabel(m){return m||'(mechanism not stated)';}
function rx(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function ci(a,b){a=a.toLowerCase();b=b.toLowerCase();return a<b?-1:a>b?1:0;}
function short(s,n){return s.length>n?s.slice(0,n-1)+'…':s;}
function yr(a,b){return a===null?'–':(a===b?String(a):a+'–'+b);}

function extractStates(text){
  var m=TAIL_RE.exec(text);
  if(!m)return [];
  var groups=m[1].match(GROUP_RE)||[];
  var out=[];
  groups.forEach(function(g){
    var s=g.slice(1,-1).trim();
    if(s&&s.indexOf(',')<0&&s.length<=60&&out.indexOf(s)<0)out.push(s);
  });
  return out;
}

/* ---------- prepare records ---------- */
var recs=RAW.map(function(r,i){
  r=r||{};
  var text=str(r.text),m=PARA_RE.exec(text),para=m?m[1]:'';
  var y=(r.year===null||r.year===undefined||r.year==='')?NaN:Number(r.year);
  var mech=str(r.mechanism),parts=para?para.split('.').map(Number):[];
  return {i:i,id:str(r.id),symbol:str(r.symbol),url:str(r.doc_url),date:str(r.date),year:isFinite(y)?y:null,
    body:str(r.body),mech:mech,type:str(r.type),section:str(r.section),text:text,
    themes:uniq(arr(r.themes).map(str).filter(Boolean)),
    sdgs:uniq(arr(r.sdgs).map(Number).filter(function(x){return isFinite(x);})),
    targets:arr(r.sdg_targets).map(str),persons:arr(r.affected_persons).map(str),
    para:para,p1:parts.length?parts[0]:Infinity,p2:parts.length>1?parts[1]:-1,
    states:mech===UPR?extractStates(text):[],
    lc:(text+' '+str(r.symbol)).toLowerCase()};
});
var N=recs.length;

var mc=cnt();recs.forEach(function(o){mc[o.mech]=(mc[o.mech]||0)+1;});
var KNOWN=[UPR,'Treaty bodies','Special Procedures'];
var MECHS=KNOWN.filter(function(k){return k in mc;}).concat(Object.keys(mc).filter(function(k){return KNOWN.indexOf(k)<0;}).sort());
var ym=cnt();recs.forEach(function(o){if(o.year!==null)ym[o.year]=1;});
var YEARS=Object.keys(ym).map(Number).sort(function(a,b){return a-b;});
var tcAll=cnt();recs.forEach(function(o){if(o.type)tcAll[o.type]=(tcAll[o.type]||0)+1;});
var TYPES=Object.keys(tcAll).sort(function(a,b){return tcAll[b]-tcAll[a]||ci(a,b);});
var stAll=cnt();recs.forEach(function(o){o.states.forEach(function(s){stAll[s]=(stAll[s]||0)+1;});});
var STATE_LIST=Object.keys(stAll).sort(ci);
var sdAll=cnt();recs.forEach(function(o){o.sdgs.forEach(function(g){sdAll[g]=1;});});
var SDG_LIST=Object.keys(sdAll).map(Number).sort(function(a,b){return a-b;});
var DOCS=new Set(recs.map(function(o){return o.symbol;})).size;

function minmax(L){
  var a=null,b=null;
  for(var k=0;k<L.length;k++){var y=L[k].year;if(y===null)continue;if(a===null||y<a)a=y;if(b===null||y>b)b=y;}
  return {a:a,b:b};
}
var FILEYEARS=minmax(recs);

/* ---------- state ---------- */
var S={kw:'',mech:'',body:'',type:'',state:'',from:'',to:'',sdg:'',themes:[]};
var WORDS=[],HLRE=null,FILTERED=[],SORTED=[],dateAsc=false,shown=PAGE,OPEN={},THEME_TOP=[],LAST_BARS=[],CHIPFN=[];
var active='ov',openAcc='',statesOpen=false,charts={t:null,m:null},FILECHK=null;
var SAMPLE=[],VERD={},SEED=1,kwT=null;
var TABS=[
  {id:'ov',num:'01',name:'Overview'},
  {id:'rec',num:'02',name:'Records'},
  {id:'chk',num:'03',name:'Check'},
  {id:'met',num:'04',name:'Method &amp; export'}
];

function setWords(){
  WORDS=S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  HLRE=WORDS.length?new RegExp('('+WORDS.map(rx).join('|')+')','gi'):null;
}
function hl(s){
  s=str(s);
  if(!HLRE)return esc(s);
  return s.split(HLRE).map(function(p,i){return i%2?'<mark>'+esc(p)+'</mark>':esc(p);}).join('');
}
function matches(o,skip){
  var k;
  if(skip!=='kw'){for(k=0;k<WORDS.length;k++){if(o.lc.indexOf(WORDS[k])<0)return false;}}
  if(skip!=='mech'&&S.mech&&o.mech!==S.mech)return false;
  if(skip!=='body'&&S.body&&o.body!==S.body)return false;
  if(skip!=='type'&&S.type&&o.type!==S.type)return false;
  if(skip!=='state'&&S.state&&o.states.indexOf(S.state)<0)return false;
  if(skip!=='years'){
    if(S.from!==''&&(o.year===null||o.year<Number(S.from)))return false;
    if(S.to!==''&&(o.year===null||o.year>Number(S.to)))return false;
  }
  if(skip!=='sdg'&&S.sdg!==''&&o.sdgs.indexOf(Number(S.sdg))<0)return false;
  if(skip!=='themes'){for(k=0;k<S.themes.length;k++){if(o.themes.indexOf(S.themes[k])<0)return false;}}
  return true;
}
function facet(getter,skip){
  var m=cnt();
  recs.forEach(function(o){
    if(!matches(o,skip))return;
    var v=getter(o);
    (Array.isArray(v)?v:[v]).forEach(function(x){if(x===''||x===null||x===undefined)return;m[x]=(m[x]||0)+1;});
  });
  return m;
}
function sortRecs(list){
  return list.slice().sort(function(a,b){
    if(a.date!==b.date){var s=a.date<b.date?-1:1;return dateAsc?s:-s;}
    if(a.body!==b.body)return a.body<b.body?-1:1;
    if(a.p1!==b.p1)return a.p1<b.p1?-1:1;
    if(a.p2!==b.p2)return a.p2<b.p2?-1:1;
    return a.i-b.i;
  });
}
function citation(o){return o.symbol+(o.para?', para. '+o.para:'');}
function firstLine(t){
  t=t.replace(/\s+/g,' ').trim();
  if(t.length<=120)return t;
  var cut=t.slice(0,120),sp=cut.lastIndexOf(' ');
  if(sp>0)cut=cut.slice(0,sp);
  return cut+'…';
}
function filterText(){
  var p=[];
  if(WORDS.length)p.push('keyword "'+S.kw.trim()+'"');
  if(S.mech)p.push('mechanism = '+S.mech);
  if(S.body)p.push('body = '+S.body);
  if(S.type)p.push('type = '+S.type);
  if(S.state)p.push('recommending State = '+S.state);
  if(S.from!==''||S.to!=='')p.push('years '+(S.from!==''?S.from:'first')+' to '+(S.to!==''?S.to:'last'));
  if(S.sdg!=='')p.push('SDG '+S.sdg);
  S.themes.forEach(function(t){p.push('theme = '+t);});
  return p.length?p.join('; '):'none';
}

/* ---------- header, footer, static fills ---------- */
function initStatic(){
  var src=D.source?(safeUrl(str(D.source_url))?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a>':esc(D.source)):'source not stated';
  document.title='UN human rights recommendations: '+COUNTRY;
  $('hLab').textContent='UHRI · '+COUNTRY;
  $('hTitle').textContent='UN human rights recommendations and observations: '+COUNTRY;
  $('hMeta').innerHTML=src+' · '+fmt(N)+' records · '+fmt(DOCS)+' documents · '+yr(FILEYEARS.a,FILEYEARS.b)+' · built '+esc(D.built||'date not stated')+' · dated by document';
  $('foot').innerHTML='Built on OHCHR UHRI data · '+fmt(N)+' records · '+(safeUrl(str(D.source_url))?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source</a>':'source link not given');
  $('srcList').innerHTML='<dt class="lab">Source</dt><dd>'+src+'</dd><dt class="lab">Records</dt><dd>'+fmt(N)+' records, '+fmt(DOCS)+' documents</dd><dt class="lab">Built</dt><dd>'+esc(D.built||'date not stated')+'</dd><dt class="lab">Licence</dt><dd>Not stated in the file you attached; check the OHCHR terms of use before republishing text. Every row links to the UN document it comes from.</dd>';
  $('fromSel').innerHTML=$('toSel').innerHTML='';
  var yo=YEARS.map(function(y){return '<option value="'+y+'">'+y+'</option>';}).join('');
  $('fromSel').innerHTML='<option value="">First</option>'+yo;
  $('toSel').innerHTML='<option value="">Last</option>'+yo;
  $('kwMain').placeholder='Search '+fmt(N)+' records, e.g. torture';
  $('stateWrap').hidden=!STATE_LIST.length;
}

/* ---------- tabs ---------- */
function buildTabs(){
  $('tabs').innerHTML=TABS.map(function(t,i){
    return '<button type="button" role="tab" id="t-'+t.id+'" aria-selected="'+(i===0)+'" aria-controls="p-'+t.id+'" tabindex="'+(i===0?0:-1)+'" data-tab="'+t.id+'"><b>'+t.num+'</b> '+t.name+'</button>';
  }).join('');
}
function selectTab(id,focus){
  active=id;
  TABS.forEach(function(t){
    var on=t.id===id,b=$('t-'+t.id);
    b.setAttribute('aria-selected',on?'true':'false');
    b.tabIndex=on?0:-1;
    $('p-'+t.id).hidden=!on;
  });
  $('accs').hidden=!(id==='ov'||id==='rec');
  if(focus)$('t-'+id).focus();
  if(id==='ov')drawCharts();
}
$('tabs').addEventListener('click',function(e){
  var b=e.target.closest('[data-tab]');
  if(b)selectTab(b.getAttribute('data-tab'),false);
});
$('tabs').addEventListener('keydown',function(e){
  var keys=['ArrowRight','ArrowLeft','Home','End'];
  if(keys.indexOf(e.key)<0)return;
  var ids=TABS.map(function(t){return t.id;}),i=ids.indexOf(active);
  if(e.key==='ArrowRight')i=(i+1)%ids.length;
  else if(e.key==='ArrowLeft')i=(i-1+ids.length)%ids.length;
  else if(e.key==='Home')i=0;
  else i=ids.length-1;
  e.preventDefault();
  selectTab(ids[i],true);
});

/* ---------- accordion ---------- */
function syncAcc(){
  ['kw','mbt','ys'].forEach(function(k){
    var open=openAcc===k,b=$('ah-'+k);
    b.setAttribute('aria-expanded',open?'true':'false');
    b.lastElementChild.textContent=open?'–':'+';
    $('ac-'+k).hidden=!open;
  });
}

/* ---------- rail ---------- */
function chipList(){
  var c=[];
  if(WORDS.length)c.push({l:'Keyword: '+S.kw.trim(),f:function(){S.kw='';syncKw();}});
  if(S.mech)c.push({l:'Mechanism: '+S.mech,f:function(){S.mech='';}});
  if(S.body)c.push({l:'Body: '+S.body,f:function(){S.body='';}});
  if(S.type)c.push({l:'Type: '+S.type,f:function(){S.type='';}});
  if(S.state)c.push({l:'State: '+S.state,f:function(){S.state='';}});
  if(S.from!==''||S.to!=='')c.push({l:'Years: '+(S.from!==''?S.from:'first')+'–'+(S.to!==''?S.to:'last'),f:function(){S.from='';S.to='';}});
  if(S.sdg!=='')c.push({l:'SDG '+S.sdg,f:function(){S.sdg='';}});
  S.themes.forEach(function(t){c.push({l:'Theme: '+t,f:function(){S.themes=S.themes.filter(function(x){return x!==t;});}});});
  return c;
}
function fillSelect(sel,allLabel,items,cur){
  sel.innerHTML='<option value="">'+esc(allLabel)+'</option>'+items.map(function(i){return '<option value="'+esc(i.v)+'">'+esc(i.l)+'</option>';}).join('');
  sel.value=cur;
}
function renderRail(){
  var n=FILTERED.length;
  $('matchN').textContent=fmt(n);
  $('matchOf').textContent='of '+fmt(N)+' in the file';
  $('shareFill').style.width=(N?100*n/N:0)+'%';
  CHIPFN=chipList();
  $('chips').innerHTML=CHIPFN.map(function(c,k){
    return '<button type="button" class="chip" data-act="chip" data-k="'+k+'" title="'+esc(c.l)+'" aria-label="Remove filter: '+esc(c.l)+'">'+esc(short(c.l,46))+' <span aria-hidden="true">×</span></button>';
  }).join('');
  var fm=facet(function(o){return o.mech;},'mech');
  fillSelect($('mechSel'),'All mechanisms',MECHS.filter(Boolean).map(function(m){return {v:m,l:m+' ('+fmt(fm[m]||0)+')'};}),S.mech);
  var fb=facet(function(o){return o.body;},'body'),bl=cnt();
  recs.forEach(function(o){if(o.body&&(!S.mech||o.mech===S.mech))bl[o.body]=1;});
  fillSelect($('bodySel'),'All bodies and mandates',Object.keys(bl).sort(ci).map(function(b){return {v:b,l:b+' ('+fmt(fb[b]||0)+')'};}),S.body);
  var ft=facet(function(o){return o.type;},'type');
  fillSelect($('typeSel'),'All types',TYPES.map(function(t){return {v:t,l:t+' ('+fmt(ft[t]||0)+')'};}),S.type);
  var fs=facet(function(o){return o.states;},'state');
  fillSelect($('stateSel'),'All States',STATE_LIST.map(function(s){return {v:s,l:s+' ('+fmt(fs[s]||0)+')'};}),S.state);
  var fg=facet(function(o){return o.sdgs;},'sdg');
  fillSelect($('sdgSel'),'All SDGs',SDG_LIST.map(function(g){return {v:String(g),l:'SDG '+g+(SDG_NAMES[String(g)]?' · '+SDG_NAMES[String(g)]:'')+' ('+fmt(fg[g]||0)+')'};}),S.sdg);
  $('fromSel').value=S.from;$('toSel').value=S.to;
  var a1=WORDS.length?1:0,a2=(S.mech?1:0)+(S.body?1:0)+(S.type?1:0)+(S.state?1:0),a3=((S.from!==''||S.to!=='')?1:0)+(S.sdg!==''?1:0);
  $('an-kw').textContent=a1?'· '+a1:'';$('an-mbt').textContent=a2?'· '+a2:'';$('an-ys').textContent=a3?'· '+a3:'';
}
function syncKw(){$('kwRail').value=S.kw;$('kwMain').value=S.kw;}
function onKw(e){
  var v=e.target.value,other=e.target===$('kwRail')?$('kwMain'):$('kwRail');
  other.value=v;
  clearTimeout(kwT);
  kwT=setTimeout(function(){S.kw=v;update();},300);
}
$('kwRail').addEventListener('input',onKw);
$('kwMain').addEventListener('input',onKw);
$('accs').addEventListener('change',function(e){
  var id=e.target.id,v=e.target.value;
  if(id==='mechSel'){
    S.mech=v;
    if(S.mech&&S.body&&!recs.some(function(o){return o.mech===S.mech&&o.body===S.body;}))S.body='';
  }
  else if(id==='bodySel')S.body=v;
  else if(id==='typeSel')S.type=v;
  else if(id==='stateSel')S.state=v;
  else if(id==='fromSel')S.from=v;
  else if(id==='toSel')S.to=v;
  else if(id==='sdgSel')S.sdg=v;
  else return;
  if(S.from!==''&&S.to!==''&&Number(S.from)>Number(S.to)){var t=S.from;S.from=S.to;S.to=t;}
  update();
});

/* ---------- overview ---------- */
function themeStats(list){
  var m=cnt();
  list.forEach(function(o){
    o.themes.forEach(function(t){
      var e=m[t]||(m[t]={name:t,count:0,y0:null,y1:null});
      e.count++;
      if(o.year!==null){if(e.y0===null||o.year<e.y0)e.y0=o.year;if(e.y1===null||o.year>e.y1)e.y1=o.year;}
    });
  });
  return Object.keys(m).map(function(k){return m[k];}).sort(function(a,b){return b.count-a.count||ci(a.name,b.name);});
}
function stateTop(L){
  var m=cnt(),upr=0,found=0;
  L.forEach(function(o){
    if(o.mech!==UPR)return;
    upr++;if(o.states.length)found++;
    o.states.forEach(function(s){m[s]=(m[s]||0)+1;});
  });
  var a=Object.keys(m).map(function(k){return {name:k,count:m[k]};}).sort(function(x,y){return y.count-x.count||ci(x.name,y.name);});
  return {top:a.slice(0,10),upr:upr,found:found};
}
function tile(label,big,sub,how,extra,color){
  return '<div class="tile"><p class="lab">'+(color?'<span class="dot" style="background:'+color+'"></span>':'')+label+'</p><p class="n">'+big+'</p><p class="sub">'+sub+'</p><p class="how">How this is computed: '+how+'</p>'+(extra||'')+'</div>';
}
function renderOverview(){
  var L=FILTERED,n=L.length,mm=minmax(L);
  var docs=new Set(L.map(function(o){return o.symbol;})).size;
  var tc=cnt();
  L.forEach(function(o){var k=o.type||'(type not stated)';tc[k]=(tc[k]||0)+1;});
  var tl=Object.keys(tc).sort(function(a,b){return tc[b]-tc[a]||ci(a,b);}).map(function(k){return fmt(tc[k])+' '+esc(k);}).join(' · ');
  $('tiles1').innerHTML=
    tile('Records',fmt(n),(n!==N?'of '+fmt(N)+' in the file<br>':'')+(tl||'No records match'),'every record in the filtered set; types are counted as spelled in the data.')+
    tile('Documents',fmt(docs),'distinct UN symbols','distinct symbol values in the filtered set.')+
    tile('Years',mm.a===null?'–':yr(mm.a,mm.b),'first–last year, dated by document','smallest and largest year in the filtered set.');
  $('tiles2').innerHTML=MECHS.map(function(m){
    var Lm=L.filter(function(o){return o.mech===m;}),mx=minmax(Lm);
    var d=new Set(Lm.map(function(o){return o.symbol;})).size;
    var extra='';
    if(m===UPR){
      extra='<p class="how"><button type="button" class="linkbtn" data-act="states" aria-expanded="'+statesOpen+'">see the States</button></p>';
      if(statesOpen){
        var st=stateTop(L);
        extra+='<div class="statesbox"><h4>Ten States that made most recommendations to '+esc(COUNTRY)+'</h4>'+
          (st.top.length?'<ol>'+st.top.map(function(s){return '<li>'+esc(s.name)+' · '+fmt(s.count)+'</li>';}).join('')+'</ol>':'<p>No State found in the current selection.</p>')+
          '<p class="how">How this is computed: States named in the parentheses that end each UPR text; a line made by several States counts once for each. '+fmt(st.found)+' of '+fmt(st.upr)+' UPR records name a State.</p></div>';
      }
    }
    return tile(esc(mlabel(m)),fmt(Lm.length),fmt(d)+' documents · latest '+(mx.b===null?'–':mx.b)+' · '+pct(Lm.length,n)+' of filtered','records with this mechanism in the filtered set; share = records / filtered records.',extra,colorOf(m));
  }).join('');

  var TS=themeStats(L);
  THEME_TOP=TS.slice(0,10);
  LAST_BARS=THEME_TOP.map(function(t){return t.count;});
  $('fig1t').textContent=(TS.length<10?'Most frequent themes (only '+TS.length+' present)':'Ten most frequent themes')+' among '+fmt(n)+' filtered records';
  $('themeRows').innerHTML=THEME_TOP.length?THEME_TOP.map(function(t,k){
    return '<tr data-count="'+t.count+'" data-name="'+esc(t.name)+'"><td><button type="button" class="sorter" data-act="theme" data-k="'+k+'">'+esc(t.name)+'</button></td><td class="num">'+fmt(t.count)+'</td><td class="num">'+pct(t.count,n)+'</td><td class="num">'+yr(t.y0,t.y1)+'</td></tr>';
  }).join(''):'<tr><td colspan="4">'+(n?'No themes are labelled in this selection.':'No records match the current filters.')+'</td></tr>';
  $('fig1n').textContent='How this is computed: each record counts once for every theme it carries, so bars add up to more than the '+fmt(n)+' records; percentages are of records, not of labels. Click a bar = add the theme as a filter.';
  var srcTxt='Source: '+(D.source||'UHRI file')+(D.built?', built '+D.built:'')+'; '+fmt(n)+' of '+fmt(N)+' records.';
  $('fig1s').textContent=srcTxt;
  $('fig2s').textContent=srcTxt;
  var undated=L.filter(function(o){return o.year===null;}).length;
  $('fig2t').textContent='Records per year by mechanism, '+fmt(n)+' filtered records';
  $('fig2n').textContent='How this is computed: records per year and mechanism in the filtered set, zero for missing combinations; empty years show as gaps.'+(undated?' '+fmt(undated)+' records without a year are not drawn.':'');
}

var endLabels={id:'endLabels',afterDatasetsDraw:function(chart){
  var ctx=chart.ctx,meta=chart.getDatasetMeta(0),data=chart.data.datasets[0].data;
  ctx.save();ctx.font='600 13px ui-monospace, Menlo, Consolas, monospace';ctx.fillStyle='#1d1b18';ctx.textBaseline='middle';
  meta.data.forEach(function(bar,i){ctx.fillText(fmt(data[i]),bar.x+6,bar.y);});
  ctx.restore();
}};
function wrap(s,w,maxLines){
  var words=s.split(' '),lines=[],cur='';
  words.forEach(function(x){
    if(cur&&(cur+' '+x).length>w){lines.push(cur);cur=x;}else cur=cur?cur+' '+x:x;
  });
  if(cur)lines.push(cur);
  if(lines.length>maxLines){lines=lines.slice(0,maxLines);lines[maxLines-1]+='…';}
  return lines;
}
function addTheme(name){
  if(S.themes.indexOf(name)<0)S.themes.push(name);
  update();
}
function drawCharts(){
  ['t','m'].forEach(function(k){if(charts[k]){charts[k].destroy();charts[k]=null;}});
  var n=FILTERED.length,hasChart=!!window.Chart;
  var msg=!hasChart?'Chart.js did not load; the table has the same numbers.':'No records match the current filters.';
  var show1=hasChart&&THEME_TOP.length>0;
  $('c1').hidden=!show1;$('c1e').hidden=show1;
  $('c1e').textContent=hasChart&&n?'No themes are labelled in this selection.':msg;
  var mm=minmax(FILTERED),show2=hasChart&&mm.a!==null;
  $('c2').hidden=!show2;$('c2e').hidden=show2;
  $('c2e').textContent=hasChart&&n?'No record in this selection has a year.':msg;
  if(!hasChart)return;
  try{
    Chart.defaults.font.family='system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
    Chart.defaults.color='#1d1b18';
    if(show1){
      var top=THEME_TOP;
      $('box1').style.height=Math.max(160,top.length*46+20)+'px';
      charts.t=new Chart($('c1'),{type:'bar',
        data:{labels:top.map(function(t){return wrap(t.name,34,3);}),datasets:[{data:LAST_BARS,backgroundColor:'rgba(155,35,53,0.8)',hoverBackgroundColor:'#9b2335',barPercentage:0.75,categoryPercentage:0.9}]},
        options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:64}},
          interaction:{mode:'nearest',axis:'y',intersect:false},
          plugins:{legend:{display:false},tooltip:{callbacks:{
            title:function(items){return top[items[0].dataIndex].name;},
            label:function(c){return fmt(c.parsed.x)+' records ('+pct(c.parsed.x,n)+' of filtered)';}}}},
          scales:{x:{display:false,beginAtZero:true},y:{grid:{display:false},border:{display:false},ticks:{autoSkip:false,font:{size:13}}}},
          onClick:function(evt,els){if(els&&els.length)addTheme(top[els[0].index].name);},
          onHover:function(evt,els){if(evt.native&&evt.native.target)evt.native.target.style.cursor=els&&els.length?'pointer':'default';}},
        plugins:[endLabels]});
      $('c1').setAttribute('aria-label','Ranked horizontal bars. Largest: '+top[0].name+', '+fmt(top[0].count)+' records. The table below lists all ten.');
    }
    if(show2){
      var years=[];for(var y=mm.a;y<=mm.b;y++)years.push(y);
      var per={};MECHS.forEach(function(m){per[m]=years.map(function(){return 0;});});
      var tot=years.map(function(){return 0;});
      FILTERED.forEach(function(o){if(o.year===null)return;var k=o.year-mm.a;per[o.mech][k]++;tot[k]++;});
      var peak=0;tot.forEach(function(v,k){if(v>tot[peak])peak=k;});
      charts.m=new Chart($('c2'),{type:'bar',
        data:{labels:years,datasets:MECHS.map(function(m){return {label:mlabel(m),data:per[m],backgroundColor:colorOf(m),stack:'s'};})},
        options:{responsive:true,maintainAspectRatio:false,animation:false,
          plugins:{legend:{position:'top',labels:{boxWidth:12,font:{size:13}}},tooltip:{mode:'index',intersect:false}},
          scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:true,maxRotation:0}},y:{stacked:true,beginAtZero:true,ticks:{precision:0},grid:{color:'#e7e1d3'}}}}});
      $('c2').setAttribute('aria-label','Stacked bars of records per year by mechanism, '+mm.a+' to '+mm.b+'. Busiest year: '+years[peak]+' with '+fmt(tot[peak])+' records.');
    }
  }catch(err){
    $('c1e').hidden=false;$('c1e').textContent='The charts could not be drawn ('+err.message+'); the table has the same numbers.';
  }
}

/* ---------- records ---------- */
function detailHtml(o){
  function tags(items,f){return items.length?items.map(function(x){return '<span class="tag">'+esc(f?f(x):x)+'</span>';}).join(''):'<span class="mute">not labelled</span>';}
  var cite=!o.para;
  return '<tr class="det"><td colspan="6"><div class="detail"><div class="pn" aria-label="Paragraph number">'+esc(o.para||'–')+'</div><div>'+
    '<p class="full">'+hl(o.text)+'</p>'+
    '<dl style="margin:0"><div class="dl"><dt class="lab">Themes</dt><dd>'+tags(o.themes)+'</dd></div>'+
    '<div class="dl"><dt class="lab">SDGs</dt><dd>'+tags(o.sdgs,function(g){return 'SDG '+g+(SDG_NAMES[String(g)]?' · '+SDG_NAMES[String(g)]:'');})+'</dd></div>'+
    (o.targets.length?'<div class="dl"><dt class="lab">SDG targets</dt><dd>'+tags(o.targets)+'</dd></div>':'')+
    '<div class="dl"><dt class="lab">Affected persons</dt><dd>'+tags(o.persons)+'</dd></div>'+
    (o.section?'<div class="dl"><dt class="lab">Section</dt><dd>'+esc(o.section)+'</dd></div>':'')+'</dl>'+
    '<div class="actions"><button type="button" class="btn" data-act="copycite" data-i="'+o.i+'">Copy citation'+(cite?' (no paragraph number in this extract)':'')+'</button><span class="ok" role="status"></span>'+
    (safeUrl(o.url)?'<a class="btn" href="'+esc(o.url)+'" target="_blank" rel="noopener">Open the UN document</a>':'<span class="mute">no link in the file</span>')+'</div>'+
    '</div></div></td></tr>';
}
function rowHtml(o){
  var open=!!OPEN[o.i];
  var st=o.mech===UPR?(o.states.length?o.states.map(esc).join('; '):'<span class="mute">State not found</span>'):'<span class="mute">–</span>';
  var h='<tr class="rowx" data-i="'+o.i+'"><td class="nw">'+esc(o.date)+'</td><td>'+hl(o.body)+'</td><td>'+
    (safeUrl(o.url)?'<a href="'+esc(o.url)+'" target="_blank" rel="noopener">'+hl(o.symbol)+'</a>':hl(o.symbol))+'</td><td class="num">'+esc(o.para||'–')+
    '</td><td><button type="button" class="rowbtn" aria-expanded="'+open+'">'+hl(firstLine(o.text))+'</button></td><td>'+st+'</td></tr>';
  return open?h+detailHtml(o):h;
}
function renderRecords(){
  var total=SORTED.length;
  $('recCap').textContent=total?'Showing '+fmt(Math.min(shown,total))+' of '+fmt(total)+' matching records, '+(dateAsc?'oldest':'newest')+' first':'No records match the current filters';
  $('recBody').innerHTML=total?SORTED.slice(0,shown).map(rowHtml).join(''):'<tr><td colspan="6">No records match the current filters. Remove a chip or use Clear all.</td></tr>';
  $('moreBtn').hidden=shown>=total;
  $('dateSort').textContent='Date '+(dateAsc?'▲':'▼');
  $('recSrc').textContent='Source: '+(D.source||'UHRI file')+(D.built?', built '+D.built:'')+'. Dates are the date of the document. Para. is the number at the start of the text; Special Procedures items without one show a dash.';
}
function toggleRow(tr){
  var i=Number(tr.getAttribute('data-i')),open=!OPEN[i];
  OPEN[i]=open;
  tr.querySelector('.rowbtn').setAttribute('aria-expanded',open?'true':'false');
  var nx=tr.nextElementSibling;
  if(open){tr.insertAdjacentHTML('afterend',detailHtml(recs[i]));}
  else if(nx&&nx.classList.contains('det')){nx.remove();}
}

/* ---------- checks ---------- */
function listBox(label,items){
  if(!items.length)return '';
  var cap=300;
  return '<details><summary>'+esc(label)+' ('+fmt(items.length)+')</summary><ul class="lst">'+items.slice(0,cap).map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>'+(items.length>cap?'<p class="hint">'+fmt(items.length-cap)+' more are not listed here.</p>':'')+'</details>';
}
function sumPresent(getter){
  var m=cnt(),s=0,g=0;
  recs.forEach(function(o){var v=getter(o);if(v!==''&&v!==null)m[v]=(m[v]||0)+1;});
  for(var k in m){s+=m[k];g++;}
  return {sum:s,groups:g};
}
function snippet(o,tail){var t=o.text.replace(/\s+/g,' ');return esc(tail?'…'+t.slice(-90):t.slice(0,90)+(t.length>90?'…':''));}
function recLink(o){return (safeUrl(o.url)?'<a href="'+esc(o.url)+'" target="_blank" rel="noopener">'+esc(o.symbol||'(no symbol)')+'</a>':esc(o.symbol||'(no symbol)'))+(o.para?', para. '+esc(o.para):'');}
function buildFileChecks(){
  var f={},declared=Number(D.count);
  f.count={s:isFinite(declared)&&declared===N?'pass':'fail',name:'Record count',d:'records.length = '+fmt(N)+' · Number(count) = '+(D.count!==undefined&&isFinite(declared)?fmt(declared):'missing')};
  var pm=sumPresent(function(o){return o.mech;}),pb=sumPresent(function(o){return o.body;}),py=sumPresent(function(o){return o.year;});
  f.parts={s:(pm.sum===N&&pb.sum===N&&py.sum===N)?'pass':'fail',name:'Partitions',d:'mechanism: '+pm.groups+' groups sum to '+fmt(pm.sum)+' · body: '+pb.groups+' groups sum to '+fmt(pb.sum)+' · year: '+py.groups+' groups sum to '+fmt(py.sum)+' · each should equal '+fmt(N)};
  var pt=sumPresent(function(o){return o.type;});
  f.types={s:pt.sum===N?'pass':'fail',name:'Type partition',d:'counts per type ('+pt.groups+' values) sum to '+fmt(pt.sum)+' · headline total '+fmt(N)};
  var badLinks=recs.filter(function(o){
    var u=o.url;try{u=decodeURIComponent(u);}catch(e){}
    u=u.toLowerCase();var s=o.symbol.toLowerCase();
    return !(s&&u.indexOf('https://docs.un.org/')===0&&u.length>=s.length&&u.lastIndexOf(s)===u.length-s.length);
  });
  f.links={s:badLinks.length?'fail':'pass',name:'Links',d:fmt(N-badLinks.length)+' of '+fmt(N)+' doc_url values start with https://docs.un.org/ and end with their symbol · '+fmt(badLinks.length)+' fail',
    x:listBox('Records whose link fails',badLinks.map(function(o){return esc(o.symbol||'(no symbol)')+' → '+esc(o.url||'(no doc_url)');}))};
  var pp=MECHS.map(function(m){
    var Lm=recs.filter(function(o){return o.mech===m;}),k=Lm.filter(function(o){return o.para;}).length;
    return {m:m,k:k,n:Lm.length};
  });
  var uprRow=pp.filter(function(p){return p.m===UPR;})[0];
  var uprMiss=recs.filter(function(o){return o.mech===UPR&&!o.para;});
  f.para={s:uprMiss.length?'warn':'pass',name:'Paragraph numbers',d:pp.map(function(p){return esc(mlabel(p.m))+': '+pct(p.k,p.n)+' ('+fmt(p.k)+' of '+fmt(p.n)+')';}).join(' · ')+(uprRow?' · UPR is expected at 100%'+(uprMiss.length?', so this is a warning, not an error':''):''),
    x:listBox('UPR records without a number',uprMiss.map(function(o){return recLink(o)+' · '+snippet(o,false);}))};
  var upr=recs.filter(function(o){return o.mech===UPR;}),noState=upr.filter(function(o){return !o.states.length;});
  var odd=STATE_LIST.filter(function(s){return /\d/.test(s);});
  f.states={s:noState.length?'warn':'pass',name:'States found',d:fmt(upr.length-noState.length)+' of '+fmt(upr.length)+' UPR records have at least one State found'+(odd.length?' · '+odd.length+' extracted names contain a digit and may not be States':''),
    x:listBox('UPR records without a State (the end of the text shows what the parentheses held)',noState.map(function(o){return recLink(o)+' · '+snippet(o,true);}))+listBox('Extracted names containing a digit',odd.map(esc))};
  var ids=new Set(recs.map(function(o){return o.id;})).size,tm=cnt(),dg=0,dx=0;
  recs.forEach(function(o){tm[o.text]=(tm[o.text]||0)+1;});
  for(var k in tm){if(tm[k]>1){dg++;dx+=tm[k]-1;}}
  var nt=recs.filter(function(o){return !o.themes.length;}).length,ns=recs.filter(function(o){return !o.sdgs.length;}).length,np=recs.filter(function(o){return !o.persons.length;}).length;
  f.dups={s:ids!==N?'fail':(dg?'warn':'pass'),name:'Duplicates and gaps',d:'distinct id = '+fmt(ids)+' of '+fmt(N)+' · '+fmt(dg)+' texts occur more than once ('+fmt(dx)+' extra records) · not labelled: '+fmt(nt)+' without themes, '+fmt(ns)+' without SDGs, '+fmt(np)+' without affected persons',
    x:listBox('Records whose text occurs more than once',recs.filter(function(o){return tm[o.text]>1;}).map(function(o){return recLink(o)+' · '+snippet(o,false);}))};
  return f;
}
function chartCheck(){
  var n=FILTERED.length,bad=[],rows=document.querySelectorAll('#themeRows tr[data-count]');
  THEME_TOP.forEach(function(t,k){
    var c=0;
    for(var j=0;j<FILTERED.length;j++){if(FILTERED[j].themes.indexOf(t.name)>=0)c++;}
    var cell=rows[k]?Number(rows[k].getAttribute('data-count')):NaN;
    if(c!==LAST_BARS[k]||c!==cell)bad.push(t.name+': bar '+LAST_BARS[k]+', table '+cell+', recount '+c);
  });
  if(rows.length!==THEME_TOP.length)bad.push('table has '+rows.length+' rows, chart has '+THEME_TOP.length+' bars');
  var mx=THEME_TOP.length?THEME_TOP[0].count:0,okMax=mx<=n;
  return {s:bad.length||!okMax?'fail':'pass',name:'Chart against table',
    d:fmt(THEME_TOP.length)+' bars recounted by a second loop over '+fmt(n)+' filtered records · '+(bad.length?'disagreements below':'bars, table rows and recount agree')+' · largest bar '+fmt(mx)+(okMax?' ≤ ':' > ')+fmt(n)+' filtered records',
    x:bad.length?listBox('Disagreements',bad.map(esc)):''};
}
function renderChecks(){
  if(!FILECHK)FILECHK=buildFileChecks();
  var f=FILECHK,list=[f.count,f.parts,f.types,chartCheck(),f.links,f.para,f.states,f.dups];
  var p=list.filter(function(c){return c.s==='pass';}).length,w=list.filter(function(c){return c.s==='warn';}).length,x=list.filter(function(c){return c.s==='fail';}).length;
  $('checkSum').textContent=p+' of '+list.length+' checks pass'+(w?' · '+w+' warning'+(w>1?'s':''):'')+(x?' · '+x+' failed':'')+'. File checks cover all '+fmt(N)+' records; the chart check follows the current filter.';
  $('checks').innerHTML=list.map(function(c){
    var mark=c.s==='pass'?'✓ pass':c.s==='warn'?'warning':'check failed';
    return '<li class="chk '+c.s+'"><span class="mark">'+mark+'</span><div><strong>'+esc(c.name)+'</strong> · <span class="vals">'+c.d+'</span>'+(c.x||'')+'</div></li>';
  }).join('');
}

/* ---------- random sample ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};}
function resetSample(){
  SAMPLE=[];VERD={};
  $('cards').innerHTML='';$('tally').textContent='';
  $('drawBtn').textContent='Check 10 at random';
  $('sampleHint').textContent='Ten paragraphs are drawn from the '+fmt(FILTERED.length)+' records matching the current filter, with a seeded generator (mulberry32): the same seed and filter give the same ten.';
}
function draw(seed){
  var pool=FILTERED.slice(),rnd=mulberry32(seed>>>0),k=Math.min(10,pool.length);
  for(var i=0;i<k;i++){var j=i+Math.floor(rnd()*(pool.length-i)),t=pool[i];pool[i]=pool[j];pool[j]=t;}
  SAMPLE=pool.slice(0,k);VERD={};SEED=seed;
  $('seed').value=seed;
  $('drawBtn').textContent='Draw again';
  $('cards').innerHTML=SAMPLE.map(function(o,c){
    return '<li class="card"><div class="cardline"><span class="cn">'+(c<9?'0':'')+(c+1)+'</span><span>'+recLink(o)+'</span>'+
      '<button type="button" class="cardbtn" data-act="card" data-k="'+c+'" aria-expanded="false">'+esc(short(firstLine(o.text),90))+'</button><span class="vd" id="vd'+c+'">not judged</span></div>'+
      '<div class="carddet" hidden><p class="full">'+esc(o.text)+'</p><p class="lab" style="margin-bottom:4px">Themes the UN gave this paragraph</p><div>'+
      (o.themes.length?o.themes.map(function(t){return '<span class="tag">'+esc(t)+'</span>';}).join(''):'<span class="mute">not labelled</span>')+'</div>'+
      '<div class="actions" role="group" aria-label="Do the themes fit as a set?">'+
      '<button type="button" class="btn" aria-pressed="false" data-act="verdict" data-k="'+c+'" data-v="fit">Fits</button>'+
      '<button type="button" class="btn" aria-pressed="false" data-act="verdict" data-k="'+c+'" data-v="no">Doesn\'t fit</button>'+
      '<button type="button" class="btn" aria-pressed="false" data-act="verdict" data-k="'+c+'" data-v="unsure">Unsure</button></div></div></li>';
  }).join('');
  if(!SAMPLE.length)$('cards').innerHTML='<li class="card"><p class="empty">No records match the current filters, so nothing can be drawn.</p></li>';
  tally();
}
function tally(){
  var f=0,d=0,u=0;
  Object.keys(VERD).forEach(function(k){if(VERD[k]==='fit')f++;else if(VERD[k]==='no')d++;else u++;});
  $('tally').textContent=SAMPLE.length?'Themes: '+f+' fit, '+d+' don\'t, '+u+' unsure · '+(f+d+u)+' of '+SAMPLE.length+' judged · seed '+SEED+'. This is your judgement; the UN labels are never changed.':'';
}
function openCard(k){
  var btns=document.querySelectorAll('#cards .cardbtn');
  Array.prototype.forEach.call(btns,function(b,i){
    var on=i===k&&b.getAttribute('aria-expanded')!=='true';
    b.setAttribute('aria-expanded',on?'true':'false');
    b.parentNode.nextElementSibling.hidden=!on;
  });
}
function setVerdict(k,v,btn){
  VERD[k]=v;
  Array.prototype.forEach.call(btn.parentNode.children,function(b){b.setAttribute('aria-pressed',b===btn?'true':'false');});
  $('vd'+k).textContent={fit:'themes fit',no:'themes don\'t fit',unsure:'unsure'}[v];
  tally();
}

/* ---------- method & export ---------- */
function typeCounts(L){
  var tc=cnt();
  L.forEach(function(o){var k=o.type||'(type not stated)';tc[k]=(tc[k]||0)+1;});
  return Object.keys(tc).sort(function(a,b){return tc[b]-tc[a]||ci(a,b);}).map(function(k){return fmt(tc[k])+' '+k;});
}
function summaryText(){
  var L=FILTERED,n=L.length,mm=minmax(L),docs=new Set(L.map(function(o){return o.symbol;})).size;
  var mech=MECHS.map(function(m){return mlabel(m)+' '+fmt(L.filter(function(o){return o.mech===m;}).length);}).join(', ');
  var themes=THEME_TOP.map(function(t,k){return (k+1)+'. '+t.name+' ('+fmt(t.count)+(t.y0!==null?', '+yr(t.y0,t.y1):'')+')';}).join('; ');
  return ['UN human rights recommendations and observations: '+COUNTRY+'.',
    'Source: '+(D.source||'UHRI file')+(D.built?', built '+D.built:'')+'; dates are the date of the document.',
    'Filters: '+filterText()+'.',
    fmt(n)+' of '+fmt(N)+' records from '+fmt(docs)+' documents, years '+yr(mm.a,mm.b)+' ('+typeCounts(L).join(', ')+').',
    'By mechanism: '+(mech||'none')+'.',
    'Ten most frequent themes among these records (a record can carry several): '+(themes||'none')+'.',
    'Counted in the browser from the file; the UN labels are used as given.'].join(' ');
}
function csvCell(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function downloadCsv(){
  var head=['date','body','mechanism','type','symbol','paragraph','recommending_states','doc_url','text','themes','sdgs','sdg_targets','affected_persons','section'];
  var lines=['# Country: '+COUNTRY,'# Source: '+(D.source||'')+(D.source_url?' '+D.source_url:''),'# Built: '+(D.built||''),'# Filters: '+filterText(),'# Rows: '+SORTED.length,head.join(',')];
  SORTED.forEach(function(o){
    lines.push([o.date,o.body,o.mech,o.type,o.symbol,o.para,o.states.join(' | '),o.url,o.text,o.themes.join(' | '),o.sdgs.join(' | '),o.targets.join(' | '),o.persons.join(' | '),o.section].map(csvCell).join(','));
  });
  var blob=new Blob(['﻿'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});
  var url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download='uhri-'+COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-filtered.csv';
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);},4000);
  $('expStatus').textContent='CSV created: '+fmt(SORTED.length)+' rows.';
}
function copyText(text,statusEl){
  function done(ok){
    statusEl.textContent=ok?'Copied':'Copy failed: select the text by hand';
    setTimeout(function(){statusEl.textContent='';},2000);
  }
  function fallback(){
    var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';
    document.body.appendChild(ta);ta.select();
    var ok=false;try{ok=document.execCommand('copy');}catch(e){}
    ta.remove();done(ok);
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(function(){done(true);},fallback);}
  else fallback();
}
function renderMethod(){
  $('expInfo').textContent='The export holds '+fmt(FILTERED.length)+' rows. Filters applied: '+filterText()+'.';
}

/* ---------- update everything ---------- */
function update(){
  setWords();
  FILTERED=recs.filter(function(o){return matches(o);});
  SORTED=sortRecs(FILTERED);
  shown=PAGE;
  renderRail();renderOverview();renderRecords();renderChecks();renderMethod();resetSample();
  if(active==='ov')drawCharts();
}

/* ---------- clicks ---------- */
document.addEventListener('click',function(e){
  var t=e.target;
  var tr=t.closest('tr.rowx');
  if(tr&&!t.closest('a')){toggleRow(tr);return;}
  var a=t.closest('[data-act]');
  if(!a)return;
  var act=a.getAttribute('data-act'),k=Number(a.getAttribute('data-k'));
  if(act==='acc'){openAcc=openAcc===a.getAttribute('data-k')?'':a.getAttribute('data-k');syncAcc();}
  else if(act==='clear'){S={kw:'',mech:'',body:'',type:'',state:'',from:'',to:'',sdg:'',themes:[]};syncKw();update();}
  else if(act==='chip'){if(CHIPFN[k]){CHIPFN[k].f();update();}}
  else if(act==='states'){statesOpen=!statesOpen;renderOverview();}
  else if(act==='theme'){if(THEME_TOP[k])addTheme(THEME_TOP[k].name);}
  else if(act==='goto'){selectTab(a.getAttribute('data-t'),true);}
  else if(act==='sortdate'){dateAsc=!dateAsc;SORTED=sortRecs(FILTERED);renderRecords();}
  else if(act==='more'){shown+=PAGE;renderRecords();}
  else if(act==='copycite'){var o=recs[Number(a.getAttribute('data-i'))];copyText(citation(o),a.nextElementSibling);}
  else if(act==='copysum'){copyText(summaryText(),$('expStatus'));}
  else if(act==='csv'){downloadCsv();}
  else if(act==='draw'){draw(Math.floor(Math.random()*999999)+1);}
  else if(act==='seeddraw'){var s=parseInt($('seed').value,10);draw(isFinite(s)&&s>=0?s:1);}
  else if(act==='card'){openCard(k);}
  else if(act==='verdict'){setVerdict(k,a.getAttribute('data-v'),a);}
});

/* ---------- start ---------- */
initStatic();
buildTabs();
syncAcc();
if(window.Chart){try{Chart.defaults.animation=false;}catch(e){}}
update();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a tab "Who recommends what". For UPR recommendations only, take the recommending State from the parentheses at the end of each recommendation. Show the 15 States that made the most recommendations to Kenya, as a bar chart, and a small table of the SDGs each of them raises most. Clicking a State lists its recommendations with symbols. Say how many UPR recommendations had no State in parentheses.

(Attached: Kenya: UN recommendations and observations → WORKSHOP_DATA.uhri)
