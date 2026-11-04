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

# Paragraphs out of a PDF: the numbered paragraphs of a General Comment, checked against the reference

## Context

The user works in an office that quotes UN documents: a national human rights institution, an NGO or a mission in Geneva. To cite a General Comment they open the PDF, copy the paragraph by hand, remove the footnote numbers and page headers that come with it, and type the citation. A PDF converter copies in a second but damages the text in four ways: it reorders (a footnote number lands at the foot of the page), breaks (a paragraph across two pages), loses (the number of footnote 6) and adds noise (headers, footers, date stamps). This app turns the converter's raw text of one document, `WORKSHOP_DATA.pdf_text`, into numbered paragraphs, compares the result with the document's own reference, and shows every repair it made. Footnotes are the hard part, and this first version does not separate them: it flags every page where footnote text may have stayed inside a paragraph, so a reader knows which paragraphs to check against the PDF. Separating the footnotes is the next step. The pages are `records` (`page`, `text`); the yardstick is `reference` (`paragraphs`, `adopted`, `first_words`; `footnotes` is shown for information); `title`, `symbol` and `doc_url` describe the document. Nothing is typed in by hand.

## What I found in the data

The numbers come from the file I examined; the app computes its own from the file it is given.

- 20 pages, `text` filled on every page, 2,800 to 4,300 characters each; `count` is the string "20". `reference.paragraphs` is 90, `reference.footnotes` 141; `reference.first_words` is keyed by the paragraph number as a string.
- **Header.** The first line of every page is the document symbol.
- **Footer.** The last lines of a page are, in varying order, the page number alone on a line (pages 2 to 20) and the job code "GE.25-15926"; page 1 has "GE.25-15926 (E)" and a date stamp "051125 061125" instead. On 12 pages a third bare number sits in the footer: a footnote number the converter displaced (6, 14, 45, 51, 67, 76, 87, 96, 101, 115, 118, 131); that footnote's text on the page has no number.
- **Paragraph numbers.** 88 of 90 stand alone on their line ("1." then the text on the next line); 2 (paragraphs 23 and 87) share the line with their text. A rule for one form alone misses the other.
- **Headings.** Roman-numbered sections ("I.", a blank line, "Introduction") and lettered subsections ("A.") whose title can wrap over two lines; and 20 unlabelled headings ("Right to work (art. 6)", "Children") on the line or two lines just before a paragraph number, so a naive split glues them to the previous paragraph; the one before paragraph 73 wraps over two lines.
- **Footnotes.** Each page's footnotes sit at the foot, before the footer: the first is a bare number on its own line, a blank line, then the text; the others start with their number and a space ("7 E/2003/22…"). 129 keep their number; on 12 pages the number was displaced to the footer and the footnote text has none. These are the hardest part of the file: on 3 and 4 November, builds that tried to separate the footnotes lost the count after the first missing number, left footnote text inside 16 paragraphs, or returned no app at all. In this version footnote lines are not separated; they are flagged. Tried on this file, the suspect-line rule below flags all 20 pages (every page has footnotes), and on each page the first suspect line is that page's first footnote number, never a line of paragraph text.
- **Footnote marks in the text.** 141 marks, glued to the word before ("waste.2") or after a space ("”. 3"); they are left as found in this version, except in the first-words comparison.
- 16 paragraphs span a page break (three pages start with a heading instead); paragraphs are 43 to 254 words of plain prose, no lettered sub-paragraphs, no line ending in a hyphen; curly quotes and en dashes occur, so comparisons normalise them.

## The app, tab by tab

The same arrangement as the workshop's Verbatim finder, so participants who used one find their way in the other: a header, a rail on the left, four numbered tabs on the right.

**Header, always visible.** A monospace label "UN DOCUMENT · PDF TEXT", the serif title `title`, one line: `symbol` linked to `doc_url` (new tab), "adopted `reference.adopted`", "n pages of raw converter text", `source`. One sentence under it says what the page does: splits the text into its numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself and lists every repair. At the right a green dot and "n of m checks pass", or a red dot and "n checks failed" (and a red dot on tab 04). The footer line (last item below) is also always visible.

**Left rail, always visible.** Headed "DOCUMENT". A card for the document: its `symbol` in monospace, its short title, "adopted …", "n pages". Under it two big serif numbers: "n paragraphs" as found, with "of `reference.paragraphs`" and a thin bar showing the share found (red when short or over), and "n pages flagged" of the document's pages (red when more than 0, linking to tab 03), then "n of m checks pass", linking to tab 04. The app is written so that every document in `WORKSHOP_DATA` with `records` and a `reference` gets its own card in the rail, in the order of the data; the selected card has a red left border and the tabs show that document. Today there is one.

Under the header, numbered tabs (`role="tablist"`, arrow keys): `01 RESULT · 02 PARAGRAPHS · 03 FLAGGED PAGES · 04 CHECKS & METHOD`.

**01 RESULT. Did the app find everything the document has?** Four tiles with big serif numbers, each with a one-line "How this is computed" note: **Paragraphs found: n** next to **The document has: `reference.paragraphs`** (green when equal, red with the difference); **Pages flagged: n of the document's pages**, with "footnote text may sit inside a paragraph; see tab 03" when more than 0, and "The document has `reference.footnotes` footnotes; this version does not separate them"; **First words match: n of `reference.paragraphs`**; **Repairs made: n**, a link to the repair log on tab 04. Five things to click: four tabs and the repair-log link.

**02 PARAGRAPHS. What does each paragraph say, and how do I cite it?** One row per paragraph: No. | Page | First line | Check: the number right-aligned, the page(s) it starts and ends on ("3–4" across a page break), the first 120 characters cut at a word with "…", and a Check cell reading "OK", "first words differ" (red; the reference's words appear in the expanded row) or "may contain footnote text" (red, linking to the page on tab 03). A **Section** column, between No. and Page, shows the nearest heading above each paragraph ("Right to work (art. 6)"); the expanded paragraph shows the full path ("IV. … › Right to work (art. 6)"). A collapsible "Headings found: n" box above the table lists them, so the reader can see that none was swallowed into a paragraph. Rows are buttons with `aria-expanded`; clicking or pressing Enter expands the row in place, under it.

Under the row, the full text, verbatim as computed, never shortened. The expanded paragraph is one block of running text; a "Show the PDF's lines" toggle under it reveals the same text with the converter's line breaks and the page number where each page began, so the join can be checked. Under the text: the reference's first six words next to the extracted first six words, marked equal or different; the page(s); the repairs that touched this paragraph; and a **Copy citation** button that copies "`symbol`, para. n" (for example "E/C.12/GC/27, para. 12") and shows "Copied" for two seconds; the same string is the CSV's `citation` column.

**03 FLAGGED PAGES. Which paragraphs should I check against the PDF?** One row per flagged page: Page | Paragraph | Suspect lines | Why ("starts with a number and a space", "bare number", "paragraph over 300 words"). Clicking a row shows the page's raw lines with the suspect ones highlighted and the paragraph they sit in. A note above the table: "This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them." When no page is flagged, the tab says so in one line.

**04 CHECKS & METHOD. Can I trust this, and can I take it away?** The check panel (see "How the app checks itself"), open, every check on one line. Under it a closed heading "Repair log (n)", a button with `aria-expanded`, which the Repairs tile on tab 01 also opens: a table of every change the script made, in document order, Page | Paragraph or footnote | What was done | Before | After, with a count per kind above it. The kinds are the ones named in the next section: header line removed, footer line removed, bare number removed from the footer, number and text split, paragraph joined across a page break, heading separated, heading title joined. Then a closed heading "Raw pages", a button with `aria-expanded`: a select "Show raw page n" and a monospaced panel with the page's `text` as stored, line numbers on the left, each line coloured by what the script decided it was (cover, header, heading, paragraph, suspect line, footer), with a legend. Then **Download**: "Download paragraphs as CSV", one row per paragraph with `number`, `section`, `part`, `page_start`, `page_end`, `first_words_reference`, `first_words_found`, `first_words_match`, `text`, `text_raw`, `flagged`, `suspect_lines`, `repairs`, `citation`, `symbol`, `doc_url`; UTF-8 with a byte-order mark, every field double-quoted with inner quotes doubled, CRLF line ends, a Blob URL, file name from the symbol with slashes replaced by hyphens. Seven things to click: four tabs, the repair log and raw pages headings, and the download (the select appears once "Raw pages" is open).

**Footer, always visible.** Source line, `built` date, and "Counting, splitting, matching and flagging are done by this page's code; no model was called and nothing left the browser."

## How every number is computed

The pipeline runs once on load, in this order, over `records` sorted by `page`; each step logs what it removed or changed.

- **Header.** If a page's first non-empty line equals `symbol`, drop it and log "header line removed"; otherwise log a warning for that page.
- **Footer.** From the end of each page, drop lines while the line is empty, starts with "GE." (the job code), consists only of 6-digit groups (the date stamp), or is a bare number of one to three digits. A bare number equal to `page` is the page number; any other is logged as "bare number removed from the footer" (on this file, a footnote number the converter displaced; the app does not try to put it back).
- **Body lines of all pages are concatenated** (every line that is not header or footer, footnote lines included) in page order, each line tagged with its page; this joins the paragraphs that cross a page break (logged as "paragraph joined across a page break" when a paragraph's lines carry two page numbers).
- **Paragraph starts.** A line matching `/^(\d{1,3})\.$/` (number alone) or `/^(\d{1,3})\. (.+)$/` (number and text on one line; the text after the space is the first line, logged as "number and text split"). Lines before the first paragraph start are the cover.
- **Headings.** A line matching `/^([IVX]+|[A-Z])\.$/` opens a labelled heading: skip blank lines, then every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or "(" continues the previous heading line (logged as "heading title joined from two lines"), any other line is a further heading. An **unlabelled heading** is a non-empty line immediately followed by a paragraph-start line, at most 90 characters, starting with a capital letter and not ending with a full stop, semicolon, colon, comma or digit (logged as "heading separated from paragraph text"); when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading ("heading title joined from two lines"). Each paragraph's `section` is the most recent heading line before it and `part` the most recent roman-numbered heading; a heading line is never part of a paragraph's text.
- **Paragraph lines.** Every other non-empty body line belongs to the current paragraph; blank lines are dropped. `page_start` and `page_end` are the pages of its first and last line.
- **Paragraph text** = the paragraph's lines joined with a single space, double spaces collapsed, trimmed. No line in the file ends with a hyphen, so no hyphen joining is done; the app counts such lines anyway and reports the number. `text_lines` keeps the original lines for the toggle and the CSV column `text_lines` (lines separated by " | ").
- **Suspect lines.** A line inside a paragraph is suspect when it is a bare number of one to three digits with no full stop after it, or starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark ("7 E/2003/22…", "2 Summary for policymakers…"), or starts with an asterisk and a space ("* Adopted by the Committee…", the note on the first page). A paragraph start always has a full stop after its number, so the two never mix. A suspect line and every line after it to the end of its page are suspect: a footnote block runs to the foot of the page. A paragraph over 300 words is flagged too (the longest real one here has 254). A page is **flagged** when it has a suspect line inside a paragraph; the paragraph gets `flagged` true and its `suspect_lines` (page, line number, text).
- **Suspect lines stay in the text.** They remain part of their paragraph's `text` and `text_raw`; the expanded paragraph on tab 02 highlights them.
- **First words.** `first_words_found` = the first six whitespace-separated words of the joined text, after removing footnote marks: digits glued to the end of a word or a punctuation mark are cut ("waste.2" becomes "waste."), and a token of digits alone is dropped only when the token before it ends with a full stop, comma or closing quote and is not an abbreviation such as "No." or "art." (paragraphs 24, 27, 46 and 60 start with real numbers, "article 2" or "No. 3", which must stay); `first_words_reference` = `reference.first_words[String(number)]`. They match when equal after normalising curly quotes to straight, en and em dashes to a hyphen and runs of whitespace to one space; case is kept.
- **Citation** = `symbol` + ", para. " + the paragraph number, with `symbol` read from `WORKSHOP_DATA.pdf_text`, never typed in.
- **Counts** are loops over the records in JavaScript; nothing is estimated and no model is called.

## How the app checks itself

Each check is one line: what was compared, the two values, and "pass" in green or "check failed" in red with a link to the rows concerned. A failed check never hides a result; it marks it.

- **Paragraph count.** Paragraphs found against `reference.paragraphs`.
- **Numbering.** The paragraph numbers are exactly 1 to n in order; gaps and duplicates are listed by number and page.
- **First words.** Each paragraph's first six words against `reference.first_words`; the count of mismatches, each listed as "para. n: found … / reference …", with the row flagged in the table.
- **Suspect lines.** n suspect lines on n pages, in n paragraphs; none is removed.
- **Pages flagged.** The pages with suspect lines inside a paragraph and the paragraphs over 300 words, each listed with its page and paragraph. A flag is not a failure: the paragraph count can be right while footnote text sits inside a paragraph, so the "Paragraphs found" tile on tab 01 says "n may contain footnote text" in red whenever a page is flagged.
- **Headers and footers.** Pages whose first line was the symbol (expected all); pages with a page number in the footer (expected all but the first); bare numbers removed from the footer, listed with their page.
- **Headings.** The number of labelled and unlabelled headings and the list of unlabelled ones, so a reader can spot a paragraph's last line mistaken for a heading.
- **Nothing lost.** Every non-empty line of every page is classified exactly once as cover, header, heading, paragraph or footer (a suspect line is a paragraph line with a flag), and the counts per kind sum to the total non-empty lines in the file; any unclassified line is listed with its page and shown in red in the raw page viewer.

## Edge cases and risks

- A paragraph number on the same line as its text (2 of 90 here) and alone on its line (88) must both be accepted; handling one form only loses two paragraphs or finds none.
- "6 November 2025" on the cover starts with a number and a space; it is never suspect because the cover comes before the first paragraph.
- A line of real paragraph text may start with a number and a space ("17 Sustainable Development Goals"); it is flagged, which costs a reader one look at the PDF, never a lost line.
- Footnotes are not separated in this version: a reader who quotes a flagged paragraph checks it against the PDF, or runs the next step, in which a model reads only the flagged pages and the code checks its answer.
- The reference is a yardstick, not the truth: if the counts disagree, the app shows both and the difference, and never trims or pads its result to match.
- The first-words check sees six words; a paragraph can start correctly and be damaged later. The raw page viewer and the "Nothing lost" check cover the rest.
- If `reference` or one of its fields is missing, the tiles say "no reference in this file" and the checks that need it show "not run", never "pass".

## Design and accessibility

What this app adds to the studio look:

- **Red accent** on the active tab, the paragraph numbers in the first column, and the words "first words differ" and "check failed". "Pass" is dark green. Pass and fail are always words as well as colours.
- **Big serif numbers** only on the document card in the rail and the four tiles of tab 01, with paragraphs found beside the document's own count. Every table has a serif `<caption>` that states the message ("90 paragraphs found, 90 expected") and a monospace number (`TAB.01`).
- **Category colours** only in the raw page viewer: six pale tints (cover, header, heading, paragraph, suspect line, footer), each doubled by a letter code in the margin and in the legend.
- Tables follow "Data visualisation: tables" (UK Government Analysis Function): `<th scope="col">`, numbers right-aligned, the source under the table, no footnotes inside data cells.
- The check panel follows "Quality assurance of code for analysis and research: Testing code" (Analysis Function): each check tells a story, given this data, having run this code, we expect this output; every repair has a named check.
- Explanations follow "GOV.UK content guidance: Clear language": short sentences; "footer", "suspect line" and "flagged page" explained the first time they appear.
- Citations follow the Dag Hammarskjöld Library's "How should I cite a UN document?": the symbol as the key, the paragraph as the pinpoint, the parts stored separately and formatted on copy.
- Keyboard: expandable rows and the repair log heading are buttons with `aria-expanded`; the tab panel of a hidden tab is not focusable.

## Out of scope

No model calls, no summaries, no OCR, no PDF rendering: the input is the converter's text. No footnote extraction: that is the next step. No lettered sub-paragraphs (none here), no editing in the browser, one document only.

## Sources consulted

- UK Government Analysis Function, Quality assurance of code for analysis and research: Testing code — https://github.com/best-practice-and-impact/qa-of-code-guidance/blob/fa39f2089905fe07c08ae4d66671736a1becd3c5/book/testing_code.md
- GOV.UK content guidance: Clear language (plain English) — https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- UK Government Analysis Function, Data visualisation: tables — https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/
- Dag Hammarskjöld Library, Ask DAG: how should I cite a UN document? — https://ask.un.org/faq/401380

(Attached: CESCR General comment No. 27 (PDF) → WORKSHOP_DATA.pdf_text)

# ASSISTANT MESSAGE (your earlier answer)

I built the paragraph extractor on the attached General comment: it splits the converter text into numbered paragraphs, removes headers and footers, and flags every page where footnote text may sit inside a paragraph. It checks itself against the document's own reference (count, numbering, first words) and logs every repair. Four tabs: result, paragraphs with a copy-citation button, flagged pages, and checks with the repair log and the CSV download.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6a3b;--mut:#5c574e;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
a{color:var(--ink)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;color:inherit}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.sm{font-size:12px;color:var(--mut)}
.ser{font-family:var(--serif)}
.bad{color:var(--red)}.ok{color:var(--green)}.mut{color:var(--mut)}
.sr{position:absolute;left:-9999px}
header.top{border-bottom:1px solid var(--rule);padding:22px 0 16px}
header.top .hrow{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 8px;max-width:800px}
.meta{margin:0 0 6px;color:var(--mut)}
.what{margin:0;max-width:780px}
.status{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;padding-top:8px}
.dot{display:inline-block;width:.75em;height:.75em;border-radius:50%;margin-right:.45em;background:var(--mut);vertical-align:baseline}
.dot.ok{background:var(--green)}.dot.bad{background:var(--red)}
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:36px;padding-top:24px;padding-bottom:30px}
aside h2{margin:0 0 10px;font-weight:400}
.card{border:0;border-left:3px solid transparent;border-bottom:1px solid var(--rule);padding:8px 0 10px 12px;margin:0 0 6px;display:block;width:100%;text-align:left;background:none}
.card.sel{border-left-color:var(--red)}
button.card{cursor:pointer}
.card .sym{font-family:var(--mono);font-size:13px;display:block}
.card .st2{display:block}
.card .sub{display:block;color:var(--mut);font-size:14px}
.rn{margin:18px 0 0;padding-left:12px}
.big{font:400 48px/1.05 var(--serif)}
.cap{color:var(--mut);font-size:14px}
.bar{height:5px;background:var(--rule);margin:6px 0 4px}.bar i{display:block;height:100%;background:var(--green)}.bar.bad i{background:var(--red)}
.rn a{display:block;margin-bottom:16px;text-decoration:none}
.rn a:hover .big{text-decoration:underline}
#tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-bottom:22px}
#tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px 9px 0;margin-right:18px;cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
#tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
h2.q{font:400 24px/1.25 var(--serif);margin:0 0 16px}
h3.mono{font-weight:400;margin:26px 0 8px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0 36px}
.tile{border-top:1px solid var(--rule);padding:14px 0 18px}
.tile .pair{display:flex;gap:30px;flex-wrap:wrap;align-items:flex-end}
.how{font-family:var(--mono);font-size:12px;color:var(--mut);margin:8px 0 0;line-height:1.5}
.tile p{margin:6px 0 0}
table.data{width:100%;border-collapse:collapse;margin:8px 0 0}
table.data caption{text-align:left;padding:0 0 8px;font:400 19px/1.3 var(--serif)}
table.data caption .mono{margin-right:10px;color:var(--mut)}
table.data th{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;font-weight:400}
table.data td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
table.data .r{text-align:right}
table.data td.num{font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}tr.prow:hover{background:#ece6d8}
.rowbtn{background:none;border:0;padding:0 2px;cursor:pointer;color:var(--red);font:inherit;font-weight:600;font-variant-numeric:tabular-nums}
.src{font-family:var(--mono);font-size:12px;color:var(--mut);margin:8px 0 0}
.pd{padding:6px 4px 14px;max-width:880px}
.ptext{font-size:17px;line-height:1.6;margin:8px 0 12px}
mark.sus{background:#f3d3d3;color:var(--ink);padding:0 2px}
.path{margin:2px 0 0;color:var(--mut)}
pre.lines,.raw{font:12.5px/1.5 var(--mono);white-space:pre-wrap;margin:8px 0;background:#fffdf8;border:1px solid var(--rule);padding:8px 10px;overflow:auto;max-height:420px}
.pg{color:var(--red)}
dl.kv{display:grid;grid-template-columns:150px 1fr;gap:4px 12px;margin:12px 0}
dl.kv dt{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);padding-top:3px}
dl.kv dd{margin:0}
.tgl,.btn,button.head{background:none;border:1px solid var(--ink);padding:5px 12px;cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.btn.pri{background:var(--ink);color:var(--paper)}
button.head{border:0;border-bottom:1px solid var(--ink);padding:6px 0;width:100%;text-align:left;font-size:13px}
button.head::before{content:"+ "}button.head[aria-expanded=true]::before{content:"\2212  "}
.tgl:hover,.btn:hover{background:#ece6d8}.btn.pri:hover{background:#000}
.copied{margin-left:10px;font-family:var(--mono);font-size:12px}
.box{border:1px solid var(--rule);padding:4px 12px 10px;margin:0 0 14px;background:#faf7f0}
.box ol{margin:6px 0 0;padding-left:22px}
.checks{list-style:none;padding:0;margin:0}
.checks>li{border-top:1px solid var(--rule);padding:9px 0}
.ch{display:grid;grid-template-columns:130px 170px 1fr;gap:4px 14px}
.st{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;padding-top:3px}
.st.pass{color:var(--green)}.st.fail{color:var(--red)}.st.info,.st.notrun{color:var(--ink)}
.items{margin:6px 0 0 144px;padding-left:18px;font-size:14px}
.items button,.lnk{background:none;border:0;padding:0;text-decoration:underline;cursor:pointer;font:inherit}
.steps{font-size:14px;color:var(--mut);margin:10px 0 0;padding-left:20px}
.kinds{display:flex;flex-wrap:wrap;gap:4px 22px;margin:8px 0 12px;font-family:var(--mono);font-size:12px}
td.mn,.mn{font-family:var(--mono);font-size:12px;word-break:break-word}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-family:var(--mono);font-size:12px;margin:8px 0}
.legend span{padding:1px 8px}
.rl{display:grid;grid-template-columns:3em 1.6em 1fr;gap:0 6px;padding:0 4px}
.rl .ln{color:var(--mut);text-align:right}
.c-cover{background:#e7e2f0}.c-header{background:#dce9f2}.c-heading{background:#f1e3c3}.c-paragraph{background:#fffdf8}.c-suspect{background:#f3d3d3}.c-footer{background:#dbe8d9}.c-blank{background:#f4f0e8;color:var(--mut)}.c-unk{background:#fff;outline:2px solid var(--red)}
footer.foot{border-top:1px solid var(--rule);padding:14px 0 28px;color:var(--mut);font-size:14px}
footer.foot p{margin:2px 0}
@media (max-width:860px){.layout{grid-template-columns:1fr;gap:18px}.tiles{grid-template-columns:1fr}.ch{grid-template-columns:1fr}.items{margin-left:18px}h1{font-size:27px}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="mono sm">UN DOCUMENT · PDF TEXT</div>
  <div class="hrow">
    <div>
      <h1 id="title">Paragraphs out of a PDF</h1>
      <p class="meta" id="meta"></p>
      <p class="what">This page splits the converter's text into its numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's own reference and lists every repair.</p>
    </div>
    <div class="status" id="status" role="status"></div>
  </div>
</div></header>
<div class="wrap layout">
  <aside id="rail" aria-label="Document"></aside>
  <main>
    <div id="tabs" role="tablist" aria-label="Views"></div>
    <section id="p1" role="tabpanel" aria-labelledby="t1" hidden></section>
    <section id="p2" role="tabpanel" aria-labelledby="t2" hidden></section>
    <section id="p3" role="tabpanel" aria-labelledby="t3" hidden></section>
    <section id="p4" role="tabpanel" aria-labelledby="t4" hidden></section>
  </main>
</div>
<footer class="foot"><div class="wrap" id="foot"></div></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{};
const KIND={header:'header line removed',footer:'footer line removed',bare:'bare number removed from the footer',split:'number and text split',join:'paragraph joined across a page break',hsep:'heading separated from paragraph text',hjoin:'heading title joined from two lines'};
const REASON={num:'starts with a number and a space',bare:'bare number',star:'starts with an asterisk and a space',long:'paragraph over 300 words'};
const CODE={cover:'C',header:'H',heading:'T',paragraph:'P',suspect:'S',footer:'F'};
const START=/^(\d{1,3})\.(?: (.+))?$/, LABEL=/^([IVX]+|[A-Z])\.$/;
const ABBR=new Set(['no.','nos.','art.','arts.','para.','paras.','p.','pp.','vol.','ch.','chap.','sec.','sect.','res.','cf.','fig.','e.g.','i.e.','rev.','add.','s.','ss.']);
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cut=(s,n)=>{s=String(s);if(s.length<=n)return s;let c=s.slice(0,n);const k=c.lastIndexOf(' ');if(k>n*.5)c=c.slice(0,k);return c.replace(/[\s,;:]+$/,'')+'…';};
const safeUrl=u=>/^https?:\/\//i.test(u||'')?u:'';
const pl=(n,w)=>n+' '+w+(n===1?'':/(ch|s|x)$/.test(w)?'es':'s');
const num=v=>(v===null||v===undefined||v===''||!isFinite(Number(v)))?null:Number(v);
const normW=s=>String(s).replace(/[“”„‟]/g,'"').replace(/[‘’‚‛]/g,"'").replace(/[–—‑‐−]/g,'-').replace(/\s+/g,' ').trim();
const endsSentence=t=>/[.;:,\d]$/.test(t.replace(/[”’"']+$/,''));
const headLike=t=>t.length<=90&&/^[A-Z]/.test(t)&&!endsSentence(t);
const susReason=t=>/^\d{1,3}$/.test(t)?'bare':/^\d{1,3} (?:[A-Z]|["“”‘’'])/.test(t)?'num':/^\* /.test(t)?'star':null;

/* Footnote marks removed from the first six words only */
function firstWords(text,n){
  const toks=text.split(/\s+/).filter(Boolean),out=[];let prev='';
  for(let i=0;i<toks.length&&out.length<n;i++){
    let w=toks[i];const raw=w;let m;
    if(/^\d{1,3}$/.test(w)){
      const pa=prev.toLowerCase().replace(/^[("“‘']+/,'');
      if(prev&&/[.,”’"']$/.test(prev)&&!ABBR.has(pa)&&!/^\d+,$/.test(prev)){prev=raw;continue;}
    }else if(w.indexOf('/')<0){
      if((m=/^(.*[.,;:?!”’"')])(\d{1,3})$/.exec(w))&&!/\d[.,]$/.test(m[1])&&!ABBR.has(m[1].toLowerCase().replace(/^[("“‘']+/,'')))w=m[1];
      else if((m=/^([A-Za-zÀ-ɏ][a-zß-ɏ]{2,})\d{1,3}$/.exec(w)))w=m[1];
    }
    out.push(w);prev=raw;
  }
  return out;
}

function analyse(D){
  const symbol=String(D.symbol||'');
  const recs=(D.records||[]).filter(r=>r&&typeof r.text==='string').map((r,i)=>({page:num(r.page)==null?i+1:num(r.page),text:r.text})).sort((a,b)=>a.page-b.page);
  const ref=D.reference&&typeof D.reference==='object'?D.reference:null;
  const R={paragraphs:ref?num(ref.paragraphs):null,footnotes:ref?num(ref.footnotes):null,fw:ref&&ref.first_words&&typeof ref.first_words==='object'?ref.first_words:null,adopted:ref&&ref.adopted?String(ref.adopted):''};
  const repairs=[],warnings=[],rawPages=[],body=[],pageStat=[],paras=[],heads=[],pending=[];
  let total=0;
  const rep=(o,p)=>{o.para=p?p.number:null;repairs.push(o);if(p)p.repairs.push(o);};
  recs.forEach(r=>{
    const pl_=r.text.split(/\r?\n/).map((s,i)=>({page:r.page,ln:i+1,t:s.trim(),cls:s.trim()===''?'blank':null,sus:null,pt:null}));
    rawPages.push({page:r.page,lines:pl_});
    total+=pl_.filter(l=>l.t!=='').length;
    const st={page:r.page,header:false,pageNo:false,bare:[]};pageStat.push(st);
    const first=pl_.findIndex(l=>l.t!=='');
    if(first>=0&&symbol&&pl_[first].t===symbol){
      pl_[first].cls='header';st.header=true;
      rep({page:r.page,ln:pl_[first].ln,kind:KIND.header,before:pl_[first].t,after:'(removed)'});
    }else warnings.push('Page '+r.page+': the first line is not the symbol, so no header was removed.');
    const lo=st.header?first:-1;
    for(let k=pl_.length-1;k>lo;k--){
      const l=pl_[k],t=l.t;if(t==='')continue;
      let note;
      if(/^GE\./.test(t))note='job code';
      else if(/^\d{6}(?:\s+\d{6})*$/.test(t))note='date stamp';
      else if(/^\d{1,3}$/.test(t)){if(!st.pageNo&&+t===r.page){st.pageNo=true;note='page number';}else note='bare';}
      else break;
      l.cls='footer';
      if(note==='bare'){st.bare.push(t);rep({page:r.page,ln:l.ln,kind:KIND.bare,before:t,after:'(removed; the footnote is not put back)'});}
      else rep({page:r.page,ln:l.ln,kind:KIND.footer,before:t,after:'(removed: '+note+')'});
    }
    pl_.forEach(l=>{if(l.cls===null)body.push(l);});
  });

  /* split into paragraphs and headings */
  let cur=null,hR=null,hL=null,hP=null,started=false,foot=false,lastPage=null;
  const mkHead=(kind,text,page,ln)=>{const h={kind,text,page,ln,next:null};heads.push(h);pending.push(h);};
  for(let i=0;i<body.length;i++){
    const L=body[i],t=L.t;let m;
    if(lastPage!==L.page){foot=false;lastPage=L.page;}
    if((m=LABEL.exec(t))){
      const roman=/^[IVX]+$/.test(m[1]);
      L.cls='heading';started=true;foot=false;
      const parts=[];let j=i+1;
      while(j<body.length){
        const B=body[j];
        if(LABEL.test(B.t)||START.test(B.t)||B.t.length>120||parts.length>=6)break;
        B.cls='heading';
        if(parts.length&&/^[a-z(]/.test(B.t)){const q=parts[parts.length-1];rep({page:B.page,ln:B.ln,kind:KIND.hjoin,before:q.text+' | '+B.t,after:q.text+' '+B.t});q.text+=' '+B.t;}
        else parts.push({text:B.t,page:B.page,ln:B.ln});
        j++;
      }
      i=j-1;cur=null;
      const first=parts.shift(),label=m[1]+'.',text=first?label+' '+first.text:label;
      mkHead(roman?'roman':'letter',text,L.page,L.ln);
      if(roman){hR=text;hL=null;hP=null;}else{hL=text;hP=null;}
      parts.forEach(q=>{mkHead('plain',q.text,q.page,q.ln);hP=q.text;});
      continue;
    }
    if((m=START.exec(t))){
      L.cls='paragraph';started=true;foot=false;
      cur={number:+m[1],lines:[],repairs:[],part:hR||'',sect:[hR,hL,hP].filter(Boolean),startPage:L.page};
      paras.push(cur);pending.forEach(h=>{h.next=cur.number;});pending.length=0;
      if(m[2]){L.pt=m[2].trim();cur.lines.push(L);rep({page:L.page,ln:L.ln,kind:KIND.split,before:t,after:m[1]+'. | '+L.pt},cur);}
      continue;
    }
    if(!started||!cur){L.cls='cover';continue;}
    if(foot)L.sus='follows';
    else{const r=susReason(t);if(r){foot=true;L.sus=r;}}
    if(!L.sus&&i+1<body.length&&START.test(body[i+1].t)){
      const prev=cur.lines.length?cur.lines[cur.lines.length-1]:null;
      const prevOk=!!prev&&!prev.sus&&headLike(prev.pt);
      const own=headLike(t),tail=/^[a-z(]/.test(t)&&t.length<=90&&!endsSentence(t);
      if(own||(tail&&prevOk)){
        const two=prevOk,tailText=cur.lines.length>(two?1:0)?cur.lines[cur.lines.length-(two?2:1)].pt:'';
        const text=two?prev.pt+' '+t:t;
        if(two){cur.lines.pop();prev.cls='heading';}
        L.cls='heading';
        rep({page:L.page,ln:L.ln,kind:KIND.hsep,before:'… '+tailText.slice(-30)+' '+text,after:'heading: '+text},cur);
        if(two)rep({page:L.page,ln:L.ln,kind:KIND.hjoin,before:prev.pt+' | '+t,after:text},cur);
        mkHead('plain',text,two?prev.page:L.page,two?prev.ln:L.ln);hP=text;
        continue;
      }
    }
    L.cls='paragraph';L.pt=t;cur.lines.push(L);
  }

  let hyphen=0;
  paras.forEach(p=>{
    const ls=p.lines;
    p.text=ls.map(l=>l.pt).join(' ').replace(/ {2,}/g,' ').trim();
    p.textRaw=ls.map(l=>l.t).join(' | ');
    p.pageStart=ls.length?ls[0].page:p.startPage;
    p.pageEnd=ls.length?ls[ls.length-1].page:p.startPage;
    p.words=p.text?p.text.split(/\s+/).length:0;
    p.sus=ls.filter(l=>l.sus).map(l=>({page:l.page,ln:l.ln,text:l.t,reason:l.sus}));
    p.long=p.words>300;p.flagged=p.sus.length>0||p.long;
    p.flagPage=p.sus.length?p.sus[0].page:p.pageStart;
    p.section=p.sect.length?p.sect[p.sect.length-1]:'';
    ls.forEach((l,k)=>{
      if(/-$/.test(l.pt))hyphen++;
      if(k&&l.page!==ls[k-1].page)rep({page:l.page,ln:l.ln,kind:KIND.join,before:'…'+ls[k-1].pt.slice(-30)+' [p. '+ls[k-1].page+' | p. '+l.page+'] '+l.pt.slice(0,30)+'…',after:'one paragraph, pages '+ls[k-1].page+'–'+l.page},p);
    });
    p.fwFound=firstWords(p.text,6).join(' ');
    p.fwRef=R.fw&&R.fw[String(p.number)]!=null?String(R.fw[String(p.number)]):null;
    p.fwMatch=p.fwRef==null?null:normW(p.fwFound)===normW(p.fwRef);
    p.citation=symbol+', para. '+p.number;
  });
  repairs.sort((a,b)=>a.page-b.page||a.ln-b.ln);

  const fpm=new Map();
  const fp=pg=>{if(!fpm.has(pg))fpm.set(pg,{page:pg,paras:[],sus:[],reasons:new Set()});return fpm.get(pg);};
  paras.forEach(p=>{
    p.sus.forEach(s=>{const e=fp(s.page);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.sus.push(s);if(s.reason!=='follows')e.reasons.add(s.reason);});
    if(p.long){const e=fp(p.pageStart);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.reasons.add('long');}
  });
  const A={D,symbol,R,rawPages,pageStat,paras,heads,repairs,warnings,hyphen,total,flagPages:[...fpm.values()].sort((a,b)=>a.page-b.page)};
  A.pages=rawPages.length;
  A.fwMatches=paras.filter(p=>p.fwMatch===true).length;
  A.flaggedParas=paras.filter(p=>p.flagged).length;
  A.checks=buildChecks(A);
  const cc=A.checks.filter(c=>c.status!=='info');
  A.m=cc.length;A.nPass=cc.filter(c=>c.status==='pass').length;A.nFail=cc.filter(c=>c.status==='fail').length;A.nNot=cc.filter(c=>c.status==='notrun').length;
  return A;
}

function buildChecks(A){
  const P=A.paras,R=A.R,C=[],n=P.length;
  const add=(id,name,status,line,items)=>C.push({id,name,status,line,items:items||[]});
  /* paragraph count */
  if(R.paragraphs==null)add('count','Paragraph count','notrun','found '+n+'; the file has no reference count');
  else{const d=n-R.paragraphs;add('count','Paragraph count',d===0?'pass':'fail','found '+n+' / reference '+R.paragraphs+(d?' (difference '+(d>0?'+':'')+d+')':''));}
  /* numbering */
  const seen={},dup=[],bad=[],gaps=[];
  P.forEach((p,i)=>{if(seen[p.number])dup.push(p);seen[p.number]=1;if(p.number!==i+1&&bad.length<8)bad.push({p,i});});
  const max=P.reduce((a,p)=>Math.max(a,p.number),0);
  for(let v=1;v<=max;v++)if(!seen[v])gaps.push(v);
  const it=[];
  gaps.forEach(v=>{const b=P.filter(p=>p.number<v).pop();it.push({t:'gap: no paragraph '+v+(b?' (after para. '+b.number+', page '+b.pageEnd+')':''),go:b?'para:'+b.number:null});});
  dup.forEach(p=>it.push({t:'duplicate: para. '+p.number+', page '+p.pageStart,go:'para:'+p.number}));
  if(!gaps.length&&!dup.length)bad.forEach(o=>it.push({t:'out of order: position '+(o.i+1)+' holds para. '+o.p.number+', page '+o.p.pageStart,go:'para:'+o.p.number}));
  const okNum=n>0&&P.every((p,i)=>p.number===i+1);
  add('num','Numbering',okNum?'pass':'fail',(n?'expected 1 to '+n+' in order; found '+P[0].number+' to '+P[n-1].number:'no paragraph found')+'; '+pl(gaps.length,'gap')+', '+pl(dup.length,'duplicate'),it);
  /* first words */
  if(!R.fw)add('fw','First words','notrun','the file has no first_words reference');
  else{
    const mis=P.filter(p=>p.fwMatch===false),nor=P.filter(p=>p.fwMatch===null);
    const miss=Object.keys(R.fw).filter(k=>!P.some(p=>String(p.number)===k));
    const it3=mis.map(p=>({t:'para. '+p.number+': found “'+p.fwFound+'” / reference “'+p.fwRef+'”',go:'para:'+p.number}));
    nor.forEach(p=>it3.push({t:'para. '+p.number+': no reference entry',go:'para:'+p.number}));
    miss.forEach(k=>it3.push({t:'reference has para. '+k+'; the app found no such paragraph',go:null}));
    add('fw','First words',it3.length?'fail':'pass',A.fwMatches+' of '+n+' paragraphs found start with the reference’s six words; '+pl(mis.length,'mismatch'),it3);
  }
  /* suspect lines */
  const sl=[].concat(...P.map(p=>p.sus)),slPages=new Set(sl.map(s=>s.page)),slParas=P.filter(p=>p.sus.length);
  const kept=P.every(p=>p.sus.every(s=>p.text.indexOf(s.text.trim())>=0));
  add('sus','Suspect lines',kept?'pass':'fail',pl(sl.length,'suspect line')+' on '+pl(slPages.size,'page')+', in '+pl(slParas.length,'paragraph')+'; '+(kept?'none was removed':'some are missing from the text'));
  /* flagged pages */
  add('flag','Pages flagged',A.flagPages.length?'info':'pass',pl(A.flagPages.length,'page')+' of '+A.pages+' flagged; a flag is not a failure, it says “check this against the PDF”',A.flagPages.map(e=>({t:'page '+e.page+', para. '+e.paras.join(', ')+(e.reasons.has('long')?' (over 300 words)':''),go:'page:'+e.page})));
  /* headers and footers */
  const hdr=A.pageStat.filter(s=>s.header).length,pn=A.pageStat.filter(s=>s.pageNo).length;
  const it6=A.warnings.map(w=>({t:w,go:null}));
  A.pageStat.forEach(s=>s.bare.forEach(b=>it6.push({t:'page '+s.page+': bare number '+b+' removed from the footer (not put back)',go:'raw:'+s.page})));
  add('hf','Headers and footers',hdr===A.pages&&pn>=A.pages-1&&A.pages>0?'pass':'fail',hdr+' of '+A.pages+' pages start with the symbol; '+pn+' page numbers found, '+Math.max(A.pages-1,0)+' expected; '+pl(A.pageStat.reduce((a,s)=>a+s.bare.length,0),'bare number')+' removed',it6);
  /* headings */
  const lab=A.heads.filter(h=>h.kind!=='plain').length,unl=A.heads.filter(h=>h.kind==='plain');
  add('head','Headings','info',lab+' labelled and '+unl.length+' unlabelled; check that no heading is a paragraph’s last line',unl.map(h=>({t:'page '+h.page+': “'+h.text+'”',go:h.next!=null?'para:'+h.next:null})));
  /* nothing lost */
  const cnt={cover:0,header:0,heading:0,paragraph:0,footer:0},unk=[];let s2=0;
  A.rawPages.forEach(pg=>pg.lines.forEach(l=>{if(l.t==='')return;if(cnt[l.cls]!==undefined){cnt[l.cls]++;s2++;}else unk.push(l);}));
  add('lost','Nothing lost',!unk.length&&s2===A.total?'pass':'fail',s2+' of '+A.total+' non-empty lines classified: cover '+cnt.cover+', header '+cnt.header+', heading '+cnt.heading+', paragraph '+cnt.paragraph+' (suspect '+sl.length+'), footer '+cnt.footer,unk.map(l=>({t:'page '+l.page+', line '+l.ln+': “'+cut(l.t,60)+'”',go:'raw:'+l.page})));
  return C;
}

/* ---------- state and views ---------- */
const keys=Object.keys(WD).filter(k=>{const d=WD[k];return d&&typeof d==='object'&&Array.isArray(d.records)&&d.records.length&&d.records.every(r=>r&&typeof r.text==='string'&&r.page!=null);});
const cache={};let sel=0,tab=1;
const cur=()=>{const k=keys[sel];if(!cache[k])cache[k]=analyse(WD[k]);return cache[k];};
const rng=p=>p.pageStart===p.pageEnd?String(p.pageStart):p.pageStart+'–'+p.pageEnd;
const link=(go,txt,cls)=>'<a href="#" data-go="'+esc(go)+'"'+(cls?' class="'+cls+'"':'')+'>'+txt+'</a>';

function rail(A){
  const D=A.D,R=A.R;
  const cards=keys.map((k,i)=>{
    const d=WD[k],inner='<span class="sym">'+esc(d.symbol||k)+'</span><span class="st2 ser">'+esc(d.short_title||cut(d.title||'',60))+'</span><span class="sub">'+(i===sel&&R.adopted?'adopted '+esc(R.adopted)+' · ':'')+pl((d.records||[]).length,'page')+'</span>';
    return keys.length>1?'<button class="card'+(i===sel?' sel':'')+'" data-doc="'+i+'"'+(i===sel?' aria-pressed="true"':' aria-pressed="false"')+'>'+inner+'</button>':'<div class="card sel">'+inner+'</div>';
  }).join('');
  const n=A.paras.length,hasR=R.paragraphs!=null,eq=hasR&&n===R.paragraphs;
  const share=hasR&&R.paragraphs>0?Math.min(100,Math.round(n/R.paragraphs*100)):0;
  return '<h2 class="mono">DOCUMENT</h2>'+cards+'<div class="rn"><div><div class="big">'+n+'</div><div class="cap">paragraphs'+(hasR?' of '+R.paragraphs:' · no reference in this file')+'</div>'+(hasR?'<div class="bar'+(eq?'':' bad')+'" role="img" aria-label="'+share+' percent of the reference count found"><i style="width:'+share+'%"></i></div>':'')+'</div>'
   +'<a href="#" data-go="tab:3" style="margin-top:16px"><div class="big'+(A.flagPages.length?' bad':'')+'">'+A.flagPages.length+'</div><div class="cap">pages flagged of '+A.pages+'</div></a>'
   +'<a href="#" data-go="tab:4"><div class="big" style="font-size:34px">'+A.nPass+' of '+A.m+'</div><div class="cap">checks pass'+(A.nNot?' · '+A.nNot+' not run':'')+'</div></a></div>';
}

function tile(lab,big,extra,how){return '<article class="tile"><div class="mono sm">'+lab+'</div>'+big+extra+'<p class="how">How this is computed: '+how+'</p></article>';}
function tab1(A){
  const R=A.R,n=A.paras.length,hasR=R.paragraphs!=null,d=hasR?n-R.paragraphs:0;
  const t1=tile('PARAGRAPHS FOUND','<div class="pair"><div><div class="big">'+n+'</div><div class="cap">found</div></div><div><div class="big '+(!hasR?'':d===0?'ok':'bad')+'">'+(hasR?R.paragraphs:'–')+'</div><div class="cap">the document has</div></div></div>',
    (hasR?(d===0?'<p class="ok">Same count.</p>':'<p class="bad">'+Math.abs(d)+' '+(d<0?'fewer':'more')+' than the document has.</p>'):'<p>No reference in this file.</p>')+(A.flaggedParas?'<p class="bad">'+A.flaggedParas+' may contain footnote text.</p>':''),
    'every line that is a number and a full stop (“12.” alone, or “12. Text”) starts a paragraph; the reference is the document’s own count.');
  const t2=tile('PAGES FLAGGED','<div class="big'+(A.flagPages.length?' bad':'')+'">'+A.flagPages.length+'<span class="cap"> of '+A.pages+' pages</span></div>',
    (A.flagPages.length?'<p>Footnote text may sit inside a paragraph; '+link('tab:3','see tab 03')+'.</p>':'<p class="ok">No page has suspect lines.</p>')+'<p>'+(R.footnotes!=null?'The document has '+R.footnotes+' footnotes; this version does not separate them.':'This version does not separate footnotes.')+'</p>',
    'a page is flagged when a line inside a paragraph is a bare number or starts with a number, a space and a capital letter; the rest of that page is then suspect.');
  const t3=tile('FIRST WORDS MATCH','<div class="big">'+(R.fw?A.fwMatches:'–')+'<span class="cap"> of '+(R.paragraphs!=null?R.paragraphs:'?')+'</span></div>',R.fw?(A.fwMatches===R.paragraphs?'<p class="ok">Every paragraph starts as the reference says.</p>':'<p class="bad">'+(A.paras.length-A.fwMatches)+' found paragraphs differ or have no reference entry.</p>'):'<p>No reference in this file.</p>',
    'the first six words of each paragraph, footnote marks removed, against the reference’s words; quotes and dashes are normalised, case is kept.');
  const t4=tile('REPAIRS MADE','<div class="big">'+A.repairs.length+'</div>','<p>'+link('repairs','Open the repair log')+'</p>','every line the script removed, split or joined, one entry each; nothing is changed silently.');
  const note=hasR&&d===0&&A.flagPages.length?'<p>The count is right, but footnote text may still sit inside some paragraphs. Check the flagged ones against the PDF before you quote them.</p>':'';
  return '<h2 class="q">Did the app find everything the document has?</h2><div class="tiles">'+t1+t2+t3+t4+'</div>'+note;
}

function tab2(A){
  const R=A.R,P=A.paras,hasR=R.paragraphs!=null;
  const rows=P.map(p=>{
    const c=[];
    if(p.fwMatch===false)c.push('<span class="bad">first words differ</span>');
    if(p.flagged)c.push(link('page:'+p.flagPage,'may contain footnote text','bad'));
    if(!c.length)c.push(p.fwMatch===null?'<span class="mut">no reference</span>':'OK');
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="d'+p.number+'">'+p.number+'</button></td><td>'+esc(p.section||'–')+'</td><td class="r num">'+rng(p)+'</td><td>'+esc(cut(p.text,120)||'(empty)')+'</td><td>'+c.join('<br>')+'</td></tr><tr id="d'+p.number+'" data-n="'+p.number+'" hidden><td colspan="5"></td></tr>';
  }).join('');
  const hd=A.heads.map(h=>'<li>'+esc(h.text)+' <span class="sm">· page '+h.page+(h.kind==='plain'?' · unlabelled':'')+(h.next!=null?' · '+link('para:'+h.next,'before para. '+h.next):'')+'</span></li>').join('');
  return '<h2 class="q">What does each paragraph say, and how do I cite it?</h2>'
   +'<div class="box"><h3 style="margin:0"><button class="head" data-toggle="hbox" aria-expanded="false" aria-controls="hbox">Headings found: '+A.heads.length+'</button></h3><div id="hbox" hidden><p class="how">Headings are kept out of the paragraph text. Unlabelled ones were found by their position just before a paragraph number.</p>'+(hd?'<ol>'+hd+'</ol>':'<p>No headings found.</p>')+'</div></div>'
   +(P.length?'<table class="data"><caption><span class="mono">TAB.01</span>'+P.length+' paragraphs found, '+(hasR?R.paragraphs+' expected':'no reference in this file')+'</caption><thead><tr><th scope="col" class="r">No.</th><th scope="col">Section</th><th scope="col" class="r">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text of '+pl(A.pages,'page')+'. Click a row to read the paragraph and copy its citation.</p>':'<p>No numbered paragraph was found in this text.</p>');
}

function rawLines(pg){
  return pg.lines.map(l=>{
    const k=l.t===''?'blank':l.sus?'suspect':(l.cls&&CODE[l.cls]?l.cls:'unk');
    return '<div class="rl c-'+k+'"><span class="ln">'+l.ln+'</span><span class="code" aria-label="'+k+'">'+(k==='blank'?'':k==='unk'?'?':CODE[k])+'</span><span>'+esc(l.t)+'</span></div>';
  }).join('');
}
const legend='<div class="legend" aria-label="Legend"><span class="c-cover">C cover</span><span class="c-header">H header</span><span class="c-heading">T heading</span><span class="c-paragraph">P paragraph</span><span class="c-suspect">S suspect line</span><span class="c-footer">F footer</span></div>';

function tab3(A){
  const F=A.flagPages;
  if(!F.length)return '<h2 class="q">Which paragraphs should I check against the PDF?</h2><p>No page is flagged: no line inside a paragraph looks like footnote text.</p>';
  const rows=F.map(e=>{
    const why=[...e.reasons].map(r=>REASON[r]).join('; ');
    const first=e.sus.length?'<span class="mn">'+esc(cut(e.sus[0].text,36))+'</span>':'–';
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="f'+e.page+'">'+e.page+'</button></td><td class="r num">'+e.paras.join(', ')+'</td><td>'+e.sus.length+(e.sus.length?' · first: '+first:'')+'</td><td>'+esc(why||'follows a suspect line')+'</td></tr><tr id="f'+e.page+'" data-page="'+e.page+'" hidden><td colspan="4"></td></tr>';
  }).join('');
  return '<h2 class="q">Which paragraphs should I check against the PDF?</h2>'
   +'<p>This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them.</p>'
   +'<p class="how">A <b>suspect line</b> is a line inside a paragraph that looks like a footnote: a bare number, a number and a capital letter, or an asterisk. The rest of that page is suspect too. A <b>flagged page</b> has at least one.</p>'
   +'<table class="data"><caption><span class="mono">TAB.02</span>'+F.length+' of '+A.pages+' pages flagged</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col" class="r">Paragraph</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text. Suspect lines stay in the paragraph text; none is removed.</p>';
}

function tab4(A){
  const st={pass:'PASS',fail:'CHECK FAILED',info:'FLAGGED',notrun:'NOT RUN'};
  const chk=A.checks.map(c=>{
    const lim=c.items.slice(0,14);
    const li=lim.map(i=>'<li>'+(i.go?'<button data-go="'+esc(i.go)+'">'+esc(i.t)+'</button>':esc(i.t))+'</li>').join('')+(c.items.length>14?'<li>and '+(c.items.length-14)+' more</li>':'');
    return '<li><div class="ch"><span class="st '+c.status+'">'+(c.status==='info'&&c.id==='head'?'FOR INFORMATION':st[c.status])+'</span><strong>'+c.name+'</strong><span>'+esc(c.line)+'</span></div>'+(li?'<ul class="items">'+li+'</ul>':'')+'</li>';
  }).join('');
  const kinds=Object.keys(KIND).map(k=>'<span>'+KIND[k]+': <b>'+A.repairs.filter(r=>r.kind===KIND[k]).length+'</b></span>').join('');
  const rl=A.repairs.map(r=>'<tr><td class="r num">'+r.page+'</td><td>'+(r.para!=null?'para. '+r.para:'page')+'</td><td>'+esc(r.kind)+'</td><td class="mn" title="'+esc(r.before)+'">'+esc(cut(r.before,110))+'</td><td class="mn" title="'+esc(r.after)+'">'+esc(cut(r.after,110))+'</td></tr>').join('');
  const opts=A.rawPages.map((p,i)=>'<option value="'+i+'">'+p.page+'</option>').join('');
  return '<h2 class="q">Can I trust this, and can I take it away?</h2>'
   +'<h3 class="mono">CHECKS · TAB.04</h3><ul class="checks">'+chk+'</ul>'
   +'<ol class="steps"><li>Header and footer lines are removed page by page; every page’s remaining lines are joined in page order.</li><li>A line like “12.” or “12. Text” starts a paragraph; roman and lettered lines open headings.</li><li>Unlabelled headings are lines just before a paragraph number that look like titles.</li><li>Lines are joined with one space; '+pl(A.hyphen,'line')+' ended with a hyphen, none was joined.</li><li>Footnote text is not separated; it is flagged.</li></ol>'
   +'<h3 style="margin:24px 0 0"><button class="head" data-toggle="replog" aria-expanded="false" aria-controls="replog" id="replogbtn">Repair log ('+A.repairs.length+')</button></h3><div id="replog" hidden><div class="kinds">'+kinds+'</div><table class="data"><caption><span class="mono">TAB.03</span>'+A.repairs.length+' repairs, in document order</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>'+rl+'</tbody></table></div>'
   +'<h3 style="margin:18px 0 0"><button class="head" data-toggle="rawbox" aria-expanded="false" aria-controls="rawbox" id="rawbtn">Raw pages</button></h3><div id="rawbox" hidden><p><label>Show raw page <select id="rawsel">'+opts+'</select></label></p>'+legend+'<div class="raw" id="rawview" tabindex="0"></div><p class="how">Each line is coloured by what the script decided it was, and carries a letter code. A red outline marks a line that no rule classified.</p></div>'
   +'<h3 class="mono">DOWNLOAD</h3><button class="btn pri" id="csv">Download paragraphs as CSV</button><span class="copied" id="csvmsg" role="status"></span>';
}

function paraDetail(A,p){
  const th=p.lines.map(l=>{const s=esc(l.pt).replace(/ {2,}/g,' ');return l.sus?'<mark class="sus">'+s+'</mark>':s;}).join(' ');
  let lp=null,pre='';
  p.lines.forEach(l=>{if(l.page!==lp){pre+='<span class="pg">── page '+l.page+(lp==null?'':' begins')+' ──</span>\n';lp=l.page;}pre+=(l.sus?'<mark class="sus">'+esc(l.t)+'</mark>':esc(l.t))+'\n';});
  const reps=p.repairs.length?'<ul style="margin:0;padding-left:18px">'+p.repairs.map(r=>'<li>'+esc(r.kind)+' <span class="sm">(page '+r.page+')</span></li>').join('')+'</ul>':'none';
  const fw=p.fwRef==null?'no reference entry':'reference “'+esc(p.fwRef)+'”<br>found “'+esc(p.fwFound)+'” · '+(p.fwMatch?'<b class="ok">equal</b>':'<b class="bad">different</b>');
  return '<div class="pd"><div class="path mono">'+esc(p.sect.join(' › ')||'no heading above')+'</div><p class="ptext">'+(th||'(no text)')+'</p>'
   +(p.sus.length?'<p class="how bad">Highlighted: '+pl(p.sus.length,'suspect line')+' that may be footnote text. Check this paragraph against the PDF.</p>':'')+(p.long?'<p class="how bad">'+p.words+' words: longer than 300, check it against the PDF.</p>':'')
   +'<button class="tgl" data-lines="1" aria-expanded="false">Show the PDF’s lines</button><pre class="lines" hidden>'+pre+'</pre>'
   +'<dl class="kv"><dt>First words</dt><dd>'+fw+'</dd><dt>Page(s)</dt><dd>'+rng(p)+'</dd><dt>Repairs</dt><dd>'+reps+'</dd></dl>'
   +'<button class="btn" data-copy="'+esc(p.citation)+'">Copy citation</button> <code>'+esc(p.citation)+'</code><span class="copied" role="status"></span></div>';
}
function pageDetail(A,e){
  const pg=A.rawPages.find(x=>x.page===e.page);
  return '<div class="pd" style="max-width:none"><p>Paragraph'+(e.paras.length>1?'s':'')+' the suspect lines sit in: '+e.paras.map(n=>link('para:'+n,'para. '+n)).join(', ')+'. Highlighted lines are suspect.</p>'+legend+'<div class="raw">'+(pg?rawLines(pg):'')+'</div></div>';
}

/* ---------- interaction ---------- */
function setTab(n,focus){
  tab=n;
  document.querySelectorAll('#tabs button').forEach(b=>{const on=+b.dataset.tab===n;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;if(on&&focus)b.focus();});
  [1,2,3,4].forEach(i=>{const p=$('#p'+i);p.hidden=i!==n;if(i===n)p.tabIndex=0;else p.removeAttribute('tabindex');});
}
function toggle(btn,force){
  const open=force===undefined?btn.getAttribute('aria-expanded')!=='true':force;
  btn.setAttribute('aria-expanded',open);
  const t=document.getElementById(btn.getAttribute('aria-controls'));
  if(t)t.hidden=!open;
  if(open&&t&&t.id==='rawbox')showRaw(+$('#rawsel').value);
  return t;
}
function toggleRow(tr,force){
  const btn=tr.querySelector('button[aria-expanded]');if(!btn)return;
  const det=toggle(btn,force);
  if(det&&!det.hidden&&!det.dataset.built){
    const A=cur();
    det.firstElementChild.innerHTML=det.dataset.n?paraDetail(A,A.paras.find(p=>String(p.number)===det.dataset.n)):pageDetail(A,A.flagPages.find(e=>String(e.page)===det.dataset.page));
    det.dataset.built='1';
  }
}
function showRaw(i){const A=cur(),pg=A.rawPages[i];if(pg)$('#rawview').innerHTML=rawLines(pg);}
function go(spec){
  const [k,v]=spec.split(':');let el=null;
  if(k==='tab'){setTab(+v);return;}
  if(k==='para'){setTab(2);const b=document.querySelector('button[aria-controls="d'+v+'"]');if(b){const tr=b.closest('tr');if(b.getAttribute('aria-expanded')!=='true')toggleRow(tr,true);el=b;}}
  if(k==='page'){setTab(3);const b=document.querySelector('button[aria-controls="f'+v+'"]');if(b){const tr=b.closest('tr');if(b.getAttribute('aria-expanded')!=='true')toggleRow(tr,true);el=b;}}
  if(k==='repairs'){setTab(4);el=$('#replogbtn');toggle(el,true);}
  if(k==='raw'){setTab(4);const b=$('#rawbtn');toggle(b,true);const A=cur();const i=A.rawPages.findIndex(p=>String(p.page)===v);if(i>=0){$('#rawsel').value=i;showRaw(i);}el=$('#rawview');}
  if(el){el.scrollIntoView({block:'center'});el.focus();}
}
function copyText(txt,done){
  const fb=()=>{try{const ta=document.createElement('textarea');ta.value=txt;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();const ok=document.execCommand('copy');ta.remove();return ok;}catch(e){return false;}};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(()=>done(true),()=>done(fb()));else done(fb());
}
function downloadCsv(){
  const A=cur(),cols=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','flagged','suspect_lines','repairs','citation','symbol','doc_url'];
  const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
  const rows=A.paras.map(p=>[p.number,p.section,p.part,p.pageStart,p.pageEnd,p.fwRef==null?'':p.fwRef,p.fwFound,p.fwMatch==null?'':p.fwMatch,p.text,p.textRaw,p.flagged,p.sus.map(s=>'p.'+s.page+' l.'+s.ln+': '+s.text).join(' | '),p.repairs.map(r=>r.kind+' (p.'+r.page+')').join('; '),p.citation,A.symbol,A.D.doc_url||'']);
  const csv='﻿'+[cols].concat(rows).map(r=>r.map(q).join(',')).join('\r\n')+'\r\n';
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=(A.symbol||'paragraphs').replace(/[\/\\]+/g,'-')+'.csv';document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),4000);
  $('#csvmsg').textContent=A.paras.length+' rows prepared. If nothing was saved, your browser blocked the download.';
}

document.addEventListener('click',e=>{
  const t=e.target;let x;
  if((x=t.closest('[data-go]'))){e.preventDefault();go(x.dataset.go);return;}
  if((x=t.closest('#tabs [data-tab]'))){setTab(+x.dataset.tab,true);return;}
  if((x=t.closest('[data-doc]'))){sel=+x.dataset.doc;render();return;}
  if((x=t.closest('[data-copy]'))){const m=x.parentNode.querySelector('.copied');copyText(x.dataset.copy,ok=>{m.textContent=ok?'Copied':'Not copied: select the text and press Ctrl+C';setTimeout(()=>{m.textContent='';},2000);});return;}
  if((x=t.closest('[data-lines]'))){const pre=x.nextElementSibling;const o=x.getAttribute('aria-expanded')!=='true';x.setAttribute('aria-expanded',o);pre.hidden=!o;x.textContent=o?'Hide the PDF’s lines':'Show the PDF’s lines';return;}
  if((x=t.closest('button[data-toggle]'))){toggle(x);return;}
  if(t.closest('#csv')){downloadCsv();return;}
  if((x=t.closest('tr.prow'))){toggleRow(x);}
});
document.addEventListener('change',e=>{if(e.target.id==='rawsel')showRaw(+e.target.value);});
document.addEventListener('keydown',e=>{
  if(!e.target.closest||!e.target.closest('#tabs'))return;
  const k=e.key,i=tab-1;let n=null;
  if(k==='ArrowRight'||k==='ArrowDown')n=(i+1)%4;else if(k==='ArrowLeft'||k==='ArrowUp')n=(i+3)%4;else if(k==='Home')n=0;else if(k==='End')n=3;
  if(n!==null){e.preventDefault();setTab(n+1,true);}
});

function render(){
  if(!keys.length){
    $('#title').textContent='No PDF text in this data';
    $('#meta').textContent='';
    $('#status').textContent='';
    $('main').innerHTML='<p>The workshop data has no document with pages of raw text (records with a page number and a text). Attach a PDF text file from “Your files” and build again.</p>';
    $('#foot').innerHTML='<p>Nothing was computed; no model was called and nothing left the browser.</p>';
    return;
  }
  const A=cur(),D=A.D,u=safeUrl(D.doc_url);
  $('#title').textContent=D.title||A.symbol;
  $('#meta').innerHTML=(u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(A.symbol)+'</a>':esc(A.symbol))+(A.R.adopted?' · adopted '+esc(A.R.adopted):'')+' · '+pl(A.pages,'page')+' of raw converter text'+(D.source?' · '+esc(D.source):'');
  $('#status').innerHTML=A.nFail?'<span class="dot bad"></span>'+pl(A.nFail,'check')+' failed':'<span class="dot '+(A.nNot?'':'ok')+'"></span>'+A.nPass+' of '+A.m+' checks pass';
  $('#rail').innerHTML=rail(A);
  const names=['01 RESULT','02 PARAGRAPHS','03 FLAGGED PAGES','04 CHECKS &amp; METHOD'];
  $('#tabs').innerHTML=names.map((nm,i)=>'<button role="tab" id="t'+(i+1)+'" data-tab="'+(i+1)+'" aria-controls="p'+(i+1)+'" aria-selected="false" tabindex="-1">'+nm+(i===3&&A.nFail?' <span class="dot bad"></span><span class="sr">checks failed</span>':'')+'</button>').join('');
  $('#p1').innerHTML=tab1(A);$('#p2').innerHTML=tab2(A);$('#p3').innerHTML=tab3(A);$('#p4').innerHTML=tab4(A);
  $('#foot').innerHTML='<p>Source: '+esc(D.source||D.title||A.symbol)+(D.built?' · built '+esc(D.built):'')+'</p><p>Counting, splitting, matching and flagging are done by this page’s code; no model was called and nothing left the browser.</p>';
  setTab(tab,false);
}
render();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a second document: the Human Rights Committee's general comment No. 32, attached. Run exactly the same pipeline on it, with no rule changed, and give it its own card in the left rail so I can switch between the two documents; every tab and every check works on the selected document. Under the cards, add a small table comparing the two documents: paragraphs found next to the reference, pages flagged and checks passed.

(Attached: CCPR General comment No. 32 (PDF) → WORKSHOP_DATA.pdf_text_2)

# ASSISTANT MESSAGE (your earlier answer)

I added General Comment No. 32 as a second card in the left rail; the tabs, checks, repair log and CSV all follow the card you select, and the pipeline is the same, with no rule changed. Under the cards there is a small table with, for each document, the paragraphs found next to the reference, the pages flagged and the checks passed. Because no rule changed, a heading written on one line as "I. GENERAL REMARKS" is not recognised by the heading rule, so look at the Headings check on tab 04 before you trust the sections of this document.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6a3b;--mut:#5c574e;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 var(--sans)}
a{color:var(--ink)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;color:inherit}
.wrap{max-width:1200px;margin:0 auto;padding:0 20px}
.mono{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.sm{font-size:12px;color:var(--mut)}
.ser{font-family:var(--serif)}
.bad{color:var(--red)}.ok{color:var(--green)}.mut{color:var(--mut)}
.sr{position:absolute;left:-9999px}
header.top{border-bottom:1px solid var(--rule);padding:22px 0 16px}
header.top .hrow{display:flex;gap:24px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}
h1{font:400 34px/1.15 var(--serif);margin:6px 0 8px;max-width:800px}
.meta{margin:0 0 6px;color:var(--mut)}
.what{margin:0;max-width:780px}
.status{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;padding-top:8px}
.dot{display:inline-block;width:.75em;height:.75em;border-radius:50%;margin-right:.45em;background:var(--mut);vertical-align:baseline}
.dot.ok{background:var(--green)}.dot.bad{background:var(--red)}
.layout{display:grid;grid-template-columns:320px minmax(0,1fr);gap:36px;padding-top:24px;padding-bottom:30px}
aside h2{margin:0 0 10px;font-weight:400}
.card{border:0;border-left:3px solid transparent;border-bottom:1px solid var(--rule);padding:8px 0 10px 12px;margin:0 0 6px;display:block;width:100%;text-align:left;background:none}
.card.sel{border-left-color:var(--red)}
button.card{cursor:pointer}
.card .sym{font-family:var(--mono);font-size:13px;display:block}
.card .st2{display:block}
.card .sub{display:block;color:var(--mut);font-size:14px}
.cmpw{overflow-x:auto;margin:14px 0 0}
.cmp{width:100%;border-collapse:collapse;font-size:14px}
.cmp caption{text-align:left;padding:0 0 6px 12px;font:400 16px/1.3 var(--serif)}
.cmp caption .mono{margin-right:8px;color:var(--mut)}
.cmp th,.cmp td{padding:5px 4px;border-bottom:1px solid var(--rule);vertical-align:top;font-weight:400;text-align:left}
.cmp thead th{border-bottom:2px solid var(--ink);vertical-align:bottom}
.cmp thead th.c{font-family:var(--mono);font-size:12px;word-break:break-all;text-align:right}
.cmp thead th.c.sel{color:var(--red);box-shadow:inset 0 -3px 0 var(--red)}
.cmp tbody th{padding-left:12px;color:var(--mut)}
.cmp td{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.cmp td.sel{background:#ece6d8}
.cmpnote{margin:6px 0 0 12px}
.rn{margin:18px 0 0;padding-left:12px}
.big{font:400 48px/1.05 var(--serif)}
.cap{color:var(--mut);font-size:14px}
.bar{height:5px;background:var(--rule);margin:6px 0 4px}.bar i{display:block;height:100%;background:var(--green)}.bar.bad i{background:var(--red)}
.rn a{display:block;margin-bottom:16px;text-decoration:none}
.rn a:hover .big{text-decoration:underline}
#tabs{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--rule);margin-bottom:22px}
#tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:10px 16px 9px 0;margin-right:18px;cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
#tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
h2.q{font:400 24px/1.25 var(--serif);margin:0 0 16px}
h3.mono{font-weight:400;margin:26px 0 8px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:0 36px}
.tile{border-top:1px solid var(--rule);padding:14px 0 18px}
.tile .pair{display:flex;gap:30px;flex-wrap:wrap;align-items:flex-end}
.how{font-family:var(--mono);font-size:12px;color:var(--mut);margin:8px 0 0;line-height:1.5}
.tile p{margin:6px 0 0}
table.data{width:100%;border-collapse:collapse;margin:8px 0 0}
table.data caption{text-align:left;padding:0 0 8px;font:400 19px/1.3 var(--serif)}
table.data caption .mono{margin-right:10px;color:var(--mut)}
table.data th{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px;font-weight:400}
table.data td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
table.data .r{text-align:right}
table.data td.num{font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}tr.prow:hover{background:#ece6d8}
.rowbtn{background:none;border:0;padding:0 2px;cursor:pointer;color:var(--red);font:inherit;font-weight:600;font-variant-numeric:tabular-nums}
.src{font-family:var(--mono);font-size:12px;color:var(--mut);margin:8px 0 0}
.pd{padding:6px 4px 14px;max-width:880px}
.ptext{font-size:17px;line-height:1.6;margin:8px 0 12px}
mark.sus{background:#f3d3d3;color:var(--ink);padding:0 2px}
.path{margin:2px 0 0;color:var(--mut)}
pre.lines,.raw{font:12.5px/1.5 var(--mono);white-space:pre-wrap;margin:8px 0;background:#fffdf8;border:1px solid var(--rule);padding:8px 10px;overflow:auto;max-height:420px}
.pg{color:var(--red)}
dl.kv{display:grid;grid-template-columns:150px 1fr;gap:4px 12px;margin:12px 0}
dl.kv dt{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);padding-top:3px}
dl.kv dd{margin:0}
.tgl,.btn,button.head{background:none;border:1px solid var(--ink);padding:5px 12px;cursor:pointer;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.btn.pri{background:var(--ink);color:var(--paper)}
button.head{border:0;border-bottom:1px solid var(--ink);padding:6px 0;width:100%;text-align:left;font-size:13px}
button.head::before{content:"+ "}button.head[aria-expanded=true]::before{content:"\2212  "}
.tgl:hover,.btn:hover{background:#ece6d8}.btn.pri:hover{background:#000}
.copied{margin-left:10px;font-family:var(--mono);font-size:12px}
.box{border:1px solid var(--rule);padding:4px 12px 10px;margin:0 0 14px;background:#faf7f0}
.box ol{margin:6px 0 0;padding-left:22px}
.checks{list-style:none;padding:0;margin:0}
.checks>li{border-top:1px solid var(--rule);padding:9px 0}
.ch{display:grid;grid-template-columns:130px 170px 1fr;gap:4px 14px}
.st{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:700;padding-top:3px}
.st.pass{color:var(--green)}.st.fail{color:var(--red)}.st.info,.st.notrun{color:var(--ink)}
.items{margin:6px 0 0 144px;padding-left:18px;font-size:14px}
.items button,.lnk{background:none;border:0;padding:0;text-decoration:underline;cursor:pointer;font:inherit}
.steps{font-size:14px;color:var(--mut);margin:10px 0 0;padding-left:20px}
.kinds{display:flex;flex-wrap:wrap;gap:4px 22px;margin:8px 0 12px;font-family:var(--mono);font-size:12px}
td.mn,.mn{font-family:var(--mono);font-size:12px;word-break:break-word}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-family:var(--mono);font-size:12px;margin:8px 0}
.legend span{padding:1px 8px}
.rl{display:grid;grid-template-columns:3em 1.6em 1fr;gap:0 6px;padding:0 4px}
.rl .ln{color:var(--mut);text-align:right}
.c-cover{background:#e7e2f0}.c-header{background:#dce9f2}.c-heading{background:#f1e3c3}.c-paragraph{background:#fffdf8}.c-suspect{background:#f3d3d3}.c-footer{background:#dbe8d9}.c-blank{background:#f4f0e8;color:var(--mut)}.c-unk{background:#fff;outline:2px solid var(--red)}
footer.foot{border-top:1px solid var(--rule);padding:14px 0 28px;color:var(--mut);font-size:14px}
footer.foot p{margin:2px 0}
@media (max-width:860px){.layout{grid-template-columns:1fr;gap:18px}.tiles{grid-template-columns:1fr}.ch{grid-template-columns:1fr}.items{margin-left:18px}h1{font-size:27px}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <div class="mono sm">UN DOCUMENT · PDF TEXT</div>
  <div class="hrow">
    <div>
      <h1 id="title">Paragraphs out of a PDF</h1>
      <p class="meta" id="meta"></p>
      <p class="what">This page splits the converter's text into its numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's own reference and lists every repair.</p>
    </div>
    <div class="status" id="status" role="status"></div>
  </div>
</div></header>
<div class="wrap layout">
  <aside id="rail" aria-label="Document"></aside>
  <main>
    <div id="tabs" role="tablist" aria-label="Views"></div>
    <section id="p1" role="tabpanel" aria-labelledby="t1" hidden></section>
    <section id="p2" role="tabpanel" aria-labelledby="t2" hidden></section>
    <section id="p3" role="tabpanel" aria-labelledby="t3" hidden></section>
    <section id="p4" role="tabpanel" aria-labelledby="t4" hidden></section>
  </main>
</div>
<footer class="foot"><div class="wrap" id="foot"></div></footer>
<script>
(function(){
'use strict';
const WD=window.WORKSHOP_DATA||{};
const KIND={header:'header line removed',footer:'footer line removed',bare:'bare number removed from the footer',split:'number and text split',join:'paragraph joined across a page break',hsep:'heading separated from paragraph text',hjoin:'heading title joined from two lines'};
const REASON={num:'starts with a number and a space',bare:'bare number',star:'starts with an asterisk and a space',long:'paragraph over 300 words'};
const CODE={cover:'C',header:'H',heading:'T',paragraph:'P',suspect:'S',footer:'F'};
const START=/^(\d{1,3})\.(?: (.+))?$/, LABEL=/^([IVX]+|[A-Z])\.$/;
const ABBR=new Set(['no.','nos.','art.','arts.','para.','paras.','p.','pp.','vol.','ch.','chap.','sec.','sect.','res.','cf.','fig.','e.g.','i.e.','rev.','add.','s.','ss.']);
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cut=(s,n)=>{s=String(s);if(s.length<=n)return s;let c=s.slice(0,n);const k=c.lastIndexOf(' ');if(k>n*.5)c=c.slice(0,k);return c.replace(/[\s,;:]+$/,'')+'…';};
const safeUrl=u=>/^https?:\/\//i.test(u||'')?u:'';
const pl=(n,w)=>n+' '+w+(n===1?'':/(ch|s|x)$/.test(w)?'es':'s');
const num=v=>(v===null||v===undefined||v===''||!isFinite(Number(v)))?null:Number(v);
const normW=s=>String(s).replace(/[“”„‟]/g,'"').replace(/[‘’‚‛]/g,"'").replace(/[–—‑‐−]/g,'-').replace(/\s+/g,' ').trim();
const endsSentence=t=>/[.;:,\d]$/.test(t.replace(/[”’"']+$/,''));
const headLike=t=>t.length<=90&&/^[A-Z]/.test(t)&&!endsSentence(t);
const susReason=t=>/^\d{1,3}$/.test(t)?'bare':/^\d{1,3} (?:[A-Z]|["“”‘’'])/.test(t)?'num':/^\* /.test(t)?'star':null;

/* Footnote marks removed from the first six words only */
function firstWords(text,n){
  const toks=text.split(/\s+/).filter(Boolean),out=[];let prev='';
  for(let i=0;i<toks.length&&out.length<n;i++){
    let w=toks[i];const raw=w;let m;
    if(/^\d{1,3}$/.test(w)){
      const pa=prev.toLowerCase().replace(/^[("“‘']+/,'');
      if(prev&&/[.,”’"']$/.test(prev)&&!ABBR.has(pa)&&!/^\d+,$/.test(prev)){prev=raw;continue;}
    }else if(w.indexOf('/')<0){
      if((m=/^(.*[.,;:?!”’"')])(\d{1,3})$/.exec(w))&&!/\d[.,]$/.test(m[1])&&!ABBR.has(m[1].toLowerCase().replace(/^[("“‘']+/,'')))w=m[1];
      else if((m=/^([A-Za-zÀ-ɏ][a-zß-ɏ]{2,})\d{1,3}$/.exec(w)))w=m[1];
    }
    out.push(w);prev=raw;
  }
  return out;
}

function analyse(D){
  const symbol=String(D.symbol||'');
  const recs=(D.records||[]).filter(r=>r&&typeof r.text==='string').map((r,i)=>({page:num(r.page)==null?i+1:num(r.page),text:r.text})).sort((a,b)=>a.page-b.page);
  const ref=D.reference&&typeof D.reference==='object'?D.reference:null;
  const R={paragraphs:ref?num(ref.paragraphs):null,footnotes:ref?num(ref.footnotes):null,fw:ref&&ref.first_words&&typeof ref.first_words==='object'?ref.first_words:null,adopted:ref&&ref.adopted?String(ref.adopted):''};
  const repairs=[],warnings=[],rawPages=[],body=[],pageStat=[],paras=[],heads=[],pending=[];
  let total=0;
  const rep=(o,p)=>{o.para=p?p.number:null;repairs.push(o);if(p)p.repairs.push(o);};
  recs.forEach(r=>{
    const pl_=r.text.split(/\r?\n/).map((s,i)=>({page:r.page,ln:i+1,t:s.trim(),cls:s.trim()===''?'blank':null,sus:null,pt:null}));
    rawPages.push({page:r.page,lines:pl_});
    total+=pl_.filter(l=>l.t!=='').length;
    const st={page:r.page,header:false,pageNo:false,bare:[]};pageStat.push(st);
    const first=pl_.findIndex(l=>l.t!=='');
    if(first>=0&&symbol&&pl_[first].t===symbol){
      pl_[first].cls='header';st.header=true;
      rep({page:r.page,ln:pl_[first].ln,kind:KIND.header,before:pl_[first].t,after:'(removed)'});
    }else warnings.push('Page '+r.page+': the first line is not the symbol, so no header was removed.');
    const lo=st.header?first:-1;
    for(let k=pl_.length-1;k>lo;k--){
      const l=pl_[k],t=l.t;if(t==='')continue;
      let note;
      if(/^GE\./.test(t))note='job code';
      else if(/^\d{6}(?:\s+\d{6})*$/.test(t))note='date stamp';
      else if(/^\d{1,3}$/.test(t)){if(!st.pageNo&&+t===r.page){st.pageNo=true;note='page number';}else note='bare';}
      else break;
      l.cls='footer';
      if(note==='bare'){st.bare.push(t);rep({page:r.page,ln:l.ln,kind:KIND.bare,before:t,after:'(removed; the footnote is not put back)'});}
      else rep({page:r.page,ln:l.ln,kind:KIND.footer,before:t,after:'(removed: '+note+')'});
    }
    pl_.forEach(l=>{if(l.cls===null)body.push(l);});
  });

  /* split into paragraphs and headings */
  let cur=null,hR=null,hL=null,hP=null,started=false,foot=false,lastPage=null;
  const mkHead=(kind,text,page,ln)=>{const h={kind,text,page,ln,next:null};heads.push(h);pending.push(h);};
  for(let i=0;i<body.length;i++){
    const L=body[i],t=L.t;let m;
    if(lastPage!==L.page){foot=false;lastPage=L.page;}
    if((m=LABEL.exec(t))){
      const roman=/^[IVX]+$/.test(m[1]);
      L.cls='heading';started=true;foot=false;
      const parts=[];let j=i+1;
      while(j<body.length){
        const B=body[j];
        if(LABEL.test(B.t)||START.test(B.t)||B.t.length>120||parts.length>=6)break;
        B.cls='heading';
        if(parts.length&&/^[a-z(]/.test(B.t)){const q=parts[parts.length-1];rep({page:B.page,ln:B.ln,kind:KIND.hjoin,before:q.text+' | '+B.t,after:q.text+' '+B.t});q.text+=' '+B.t;}
        else parts.push({text:B.t,page:B.page,ln:B.ln});
        j++;
      }
      i=j-1;cur=null;
      const first=parts.shift(),label=m[1]+'.',text=first?label+' '+first.text:label;
      mkHead(roman?'roman':'letter',text,L.page,L.ln);
      if(roman){hR=text;hL=null;hP=null;}else{hL=text;hP=null;}
      parts.forEach(q=>{mkHead('plain',q.text,q.page,q.ln);hP=q.text;});
      continue;
    }
    if((m=START.exec(t))){
      L.cls='paragraph';started=true;foot=false;
      cur={number:+m[1],lines:[],repairs:[],part:hR||'',sect:[hR,hL,hP].filter(Boolean),startPage:L.page};
      paras.push(cur);pending.forEach(h=>{h.next=cur.number;});pending.length=0;
      if(m[2]){L.pt=m[2].trim();cur.lines.push(L);rep({page:L.page,ln:L.ln,kind:KIND.split,before:t,after:m[1]+'. | '+L.pt},cur);}
      continue;
    }
    if(!started||!cur){L.cls='cover';continue;}
    if(foot)L.sus='follows';
    else{const r=susReason(t);if(r){foot=true;L.sus=r;}}
    if(!L.sus&&i+1<body.length&&START.test(body[i+1].t)){
      const prev=cur.lines.length?cur.lines[cur.lines.length-1]:null;
      const prevOk=!!prev&&!prev.sus&&headLike(prev.pt);
      const own=headLike(t),tail=/^[a-z(]/.test(t)&&t.length<=90&&!endsSentence(t);
      if(own||(tail&&prevOk)){
        const two=prevOk,tailText=cur.lines.length>(two?1:0)?cur.lines[cur.lines.length-(two?2:1)].pt:'';
        const text=two?prev.pt+' '+t:t;
        if(two){cur.lines.pop();prev.cls='heading';}
        L.cls='heading';
        rep({page:L.page,ln:L.ln,kind:KIND.hsep,before:'… '+tailText.slice(-30)+' '+text,after:'heading: '+text},cur);
        if(two)rep({page:L.page,ln:L.ln,kind:KIND.hjoin,before:prev.pt+' | '+t,after:text},cur);
        mkHead('plain',text,two?prev.page:L.page,two?prev.ln:L.ln);hP=text;
        continue;
      }
    }
    L.cls='paragraph';L.pt=t;cur.lines.push(L);
  }

  let hyphen=0;
  paras.forEach(p=>{
    const ls=p.lines;
    p.text=ls.map(l=>l.pt).join(' ').replace(/ {2,}/g,' ').trim();
    p.textRaw=ls.map(l=>l.t).join(' | ');
    p.pageStart=ls.length?ls[0].page:p.startPage;
    p.pageEnd=ls.length?ls[ls.length-1].page:p.startPage;
    p.words=p.text?p.text.split(/\s+/).length:0;
    p.sus=ls.filter(l=>l.sus).map(l=>({page:l.page,ln:l.ln,text:l.t,reason:l.sus}));
    p.long=p.words>300;p.flagged=p.sus.length>0||p.long;
    p.flagPage=p.sus.length?p.sus[0].page:p.pageStart;
    p.section=p.sect.length?p.sect[p.sect.length-1]:'';
    ls.forEach((l,k)=>{
      if(/-$/.test(l.pt))hyphen++;
      if(k&&l.page!==ls[k-1].page)rep({page:l.page,ln:l.ln,kind:KIND.join,before:'…'+ls[k-1].pt.slice(-30)+' [p. '+ls[k-1].page+' | p. '+l.page+'] '+l.pt.slice(0,30)+'…',after:'one paragraph, pages '+ls[k-1].page+'–'+l.page},p);
    });
    p.fwFound=firstWords(p.text,6).join(' ');
    p.fwRef=R.fw&&R.fw[String(p.number)]!=null?String(R.fw[String(p.number)]):null;
    p.fwMatch=p.fwRef==null?null:normW(p.fwFound)===normW(p.fwRef);
    p.citation=symbol+', para. '+p.number;
  });
  repairs.sort((a,b)=>a.page-b.page||a.ln-b.ln);

  const fpm=new Map();
  const fp=pg=>{if(!fpm.has(pg))fpm.set(pg,{page:pg,paras:[],sus:[],reasons:new Set()});return fpm.get(pg);};
  paras.forEach(p=>{
    p.sus.forEach(s=>{const e=fp(s.page);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.sus.push(s);if(s.reason!=='follows')e.reasons.add(s.reason);});
    if(p.long){const e=fp(p.pageStart);if(e.paras.indexOf(p.number)<0)e.paras.push(p.number);e.reasons.add('long');}
  });
  const A={D,symbol,R,rawPages,pageStat,paras,heads,repairs,warnings,hyphen,total,flagPages:[...fpm.values()].sort((a,b)=>a.page-b.page)};
  A.pages=rawPages.length;
  A.fwMatches=paras.filter(p=>p.fwMatch===true).length;
  A.flaggedParas=paras.filter(p=>p.flagged).length;
  A.checks=buildChecks(A);
  const cc=A.checks.filter(c=>c.status!=='info');
  A.m=cc.length;A.nPass=cc.filter(c=>c.status==='pass').length;A.nFail=cc.filter(c=>c.status==='fail').length;A.nNot=cc.filter(c=>c.status==='notrun').length;
  return A;
}

function buildChecks(A){
  const P=A.paras,R=A.R,C=[],n=P.length;
  const add=(id,name,status,line,items)=>C.push({id,name,status,line,items:items||[]});
  /* paragraph count */
  if(R.paragraphs==null)add('count','Paragraph count','notrun','found '+n+'; the file has no reference count');
  else{const d=n-R.paragraphs;add('count','Paragraph count',d===0?'pass':'fail','found '+n+' / reference '+R.paragraphs+(d?' (difference '+(d>0?'+':'')+d+')':''));}
  /* numbering */
  const seen={},dup=[],bad=[],gaps=[];
  P.forEach((p,i)=>{if(seen[p.number])dup.push(p);seen[p.number]=1;if(p.number!==i+1&&bad.length<8)bad.push({p,i});});
  const max=P.reduce((a,p)=>Math.max(a,p.number),0);
  for(let v=1;v<=max;v++)if(!seen[v])gaps.push(v);
  const it=[];
  gaps.forEach(v=>{const b=P.filter(p=>p.number<v).pop();it.push({t:'gap: no paragraph '+v+(b?' (after para. '+b.number+', page '+b.pageEnd+')':''),go:b?'para:'+b.number:null});});
  dup.forEach(p=>it.push({t:'duplicate: para. '+p.number+', page '+p.pageStart,go:'para:'+p.number}));
  if(!gaps.length&&!dup.length)bad.forEach(o=>it.push({t:'out of order: position '+(o.i+1)+' holds para. '+o.p.number+', page '+o.p.pageStart,go:'para:'+o.p.number}));
  const okNum=n>0&&P.every((p,i)=>p.number===i+1);
  add('num','Numbering',okNum?'pass':'fail',(n?'expected 1 to '+n+' in order; found '+P[0].number+' to '+P[n-1].number:'no paragraph found')+'; '+pl(gaps.length,'gap')+', '+pl(dup.length,'duplicate'),it);
  /* first words */
  if(!R.fw)add('fw','First words','notrun','the file has no first_words reference');
  else{
    const mis=P.filter(p=>p.fwMatch===false),nor=P.filter(p=>p.fwMatch===null);
    const miss=Object.keys(R.fw).filter(k=>!P.some(p=>String(p.number)===k));
    const it3=mis.map(p=>({t:'para. '+p.number+': found “'+p.fwFound+'” / reference “'+p.fwRef+'”',go:'para:'+p.number}));
    nor.forEach(p=>it3.push({t:'para. '+p.number+': no reference entry',go:'para:'+p.number}));
    miss.forEach(k=>it3.push({t:'reference has para. '+k+'; the app found no such paragraph',go:null}));
    add('fw','First words',it3.length?'fail':'pass',A.fwMatches+' of '+n+' paragraphs found start with the reference’s six words; '+pl(mis.length,'mismatch'),it3);
  }
  /* suspect lines */
  const sl=[].concat(...P.map(p=>p.sus)),slPages=new Set(sl.map(s=>s.page)),slParas=P.filter(p=>p.sus.length);
  const kept=P.every(p=>p.sus.every(s=>p.text.indexOf(s.text.trim())>=0));
  add('sus','Suspect lines',kept?'pass':'fail',pl(sl.length,'suspect line')+' on '+pl(slPages.size,'page')+', in '+pl(slParas.length,'paragraph')+'; '+(kept?'none was removed':'some are missing from the text'));
  /* flagged pages */
  add('flag','Pages flagged',A.flagPages.length?'info':'pass',pl(A.flagPages.length,'page')+' of '+A.pages+' flagged; a flag is not a failure, it says “check this against the PDF”',A.flagPages.map(e=>({t:'page '+e.page+', para. '+e.paras.join(', ')+(e.reasons.has('long')?' (over 300 words)':''),go:'page:'+e.page})));
  /* headers and footers */
  const hdr=A.pageStat.filter(s=>s.header).length,pn=A.pageStat.filter(s=>s.pageNo).length;
  const it6=A.warnings.map(w=>({t:w,go:null}));
  A.pageStat.forEach(s=>s.bare.forEach(b=>it6.push({t:'page '+s.page+': bare number '+b+' removed from the footer (not put back)',go:'raw:'+s.page})));
  add('hf','Headers and footers',hdr===A.pages&&pn>=A.pages-1&&A.pages>0?'pass':'fail',hdr+' of '+A.pages+' pages start with the symbol; '+pn+' page numbers found, '+Math.max(A.pages-1,0)+' expected; '+pl(A.pageStat.reduce((a,s)=>a+s.bare.length,0),'bare number')+' removed',it6);
  /* headings */
  const lab=A.heads.filter(h=>h.kind!=='plain').length,unl=A.heads.filter(h=>h.kind==='plain');
  add('head','Headings','info',lab+' labelled and '+unl.length+' unlabelled; check that no heading is a paragraph’s last line',unl.map(h=>({t:'page '+h.page+': “'+h.text+'”',go:h.next!=null?'para:'+h.next:null})));
  /* nothing lost */
  const cnt={cover:0,header:0,heading:0,paragraph:0,footer:0},unk=[];let s2=0;
  A.rawPages.forEach(pg=>pg.lines.forEach(l=>{if(l.t==='')return;if(cnt[l.cls]!==undefined){cnt[l.cls]++;s2++;}else unk.push(l);}));
  add('lost','Nothing lost',!unk.length&&s2===A.total?'pass':'fail',s2+' of '+A.total+' non-empty lines classified: cover '+cnt.cover+', header '+cnt.header+', heading '+cnt.heading+', paragraph '+cnt.paragraph+' (suspect '+sl.length+'), footer '+cnt.footer,unk.map(l=>({t:'page '+l.page+', line '+l.ln+': “'+cut(l.t,60)+'”',go:'raw:'+l.page})));
  return C;
}

/* ---------- state and views ---------- */
const keys=Object.keys(WD).filter(k=>{const d=WD[k];return d&&typeof d==='object'&&Array.isArray(d.records)&&d.records.length&&d.records.every(r=>r&&typeof r.text==='string'&&r.page!=null);});
const cache={};let sel=0,tab=1;
const an=i=>{const k=keys[i];if(!cache[k]){try{cache[k]=analyse(WD[k]);}catch(e){cache[k]={err:String(e&&e.message||e),D:WD[k]};}}return cache[k];};
const cur=()=>an(sel);
const rng=p=>p.pageStart===p.pageEnd?String(p.pageStart):p.pageStart+'–'+p.pageEnd;
const link=(go,txt,cls)=>'<a href="#" data-go="'+esc(go)+'"'+(cls?' class="'+cls+'"':'')+'>'+txt+'</a>';

function compare(){
  if(keys.length<2)return '';
  const B=keys.map((k,i)=>an(i));
  const cell=(i,txt,bad)=>'<td class="'+(i===sel?'sel':'')+(bad?' bad':'')+'">'+txt+'</td>';
  const row=(lab,f)=>'<tr><th scope="row">'+lab+'</th>'+B.map((b,i)=>b.err?cell(i,'–',false):f(b,i)).join('')+'</tr>';
  const head=keys.map((k,i)=>'<th scope="col" class="c'+(i===sel?' sel':'')+'">'+esc(WD[k].symbol||k)+(i===sel?'<span class="sr"> (selected)</span>':'')+'</th>').join('');
  const body=row('Paragraphs found',(b,i)=>cell(i,b.paras.length,b.R.paragraphs!=null&&b.paras.length!==b.R.paragraphs))
    +row('Paragraphs in the reference',(b,i)=>cell(i,b.R.paragraphs!=null?b.R.paragraphs:'none',false))
    +row('Pages flagged',(b,i)=>cell(i,b.flagPages.length+' of '+b.pages,b.flagPages.length>0))
    +row('Checks passed',(b,i)=>cell(i,b.nPass+' of '+b.m,b.nFail>0));
  const bad=B.some(b=>b.err)?'<p class="how bad cmpnote">A document marked “–” could not be read.</p>':'';
  return '<div class="cmpw"><table class="cmp"><caption><span class="mono">TAB.05</span>The documents side by side</caption><thead><tr><th scope="col"><span class="sr">Measure</span></th>'+head+'</tr></thead><tbody>'+body+'</tbody></table></div>'
    +'<p class="how cmpnote">Same pipeline for every document, no rule changed. Red: count differs from the reference, pages flagged, or a check failed.</p>'+bad;
}
function rail(A){
  const D=A.D,R=A.R||{};
  const cards=keys.map((k,i)=>{
    const d=WD[k],inner='<span class="sym">'+esc(d.symbol||k)+'</span><span class="st2 ser">'+esc(d.short_title||cut(d.title||'',60))+'</span><span class="sub">'+(i===sel&&R.adopted?'adopted '+esc(R.adopted)+' · ':'')+pl((d.records||[]).length,'page')+'</span>';
    return keys.length>1?'<button class="card'+(i===sel?' sel':'')+'" data-doc="'+i+'"'+(i===sel?' aria-pressed="true"':' aria-pressed="false"')+'>'+inner+'</button>':'<div class="card sel">'+inner+'</div>';
  }).join('');
  if(A.err)return '<h2 class="mono">DOCUMENT</h2>'+cards+compare();
  const n=A.paras.length,hasR=R.paragraphs!=null,eq=hasR&&n===R.paragraphs;
  const share=hasR&&R.paragraphs>0?Math.min(100,Math.round(n/R.paragraphs*100)):0;
  return '<h2 class="mono">DOCUMENT</h2>'+cards+compare()+'<div class="rn"><div><div class="big">'+n+'</div><div class="cap">paragraphs'+(hasR?' of '+R.paragraphs:' · no reference in this file')+'</div>'+(hasR?'<div class="bar'+(eq?'':' bad')+'" role="img" aria-label="'+share+' percent of the reference count found"><i style="width:'+share+'%"></i></div>':'')+'</div>'
   +'<a href="#" data-go="tab:3" style="margin-top:16px"><div class="big'+(A.flagPages.length?' bad':'')+'">'+A.flagPages.length+'</div><div class="cap">pages flagged of '+A.pages+'</div></a>'
   +'<a href="#" data-go="tab:4"><div class="big" style="font-size:34px">'+A.nPass+' of '+A.m+'</div><div class="cap">checks pass'+(A.nNot?' · '+A.nNot+' not run':'')+'</div></a></div>';
}

function tile(lab,big,extra,how){return '<article class="tile"><div class="mono sm">'+lab+'</div>'+big+extra+'<p class="how">How this is computed: '+how+'</p></article>';}
function tab1(A){
  const R=A.R,n=A.paras.length,hasR=R.paragraphs!=null,d=hasR?n-R.paragraphs:0;
  const t1=tile('PARAGRAPHS FOUND','<div class="pair"><div><div class="big">'+n+'</div><div class="cap">found</div></div><div><div class="big '+(!hasR?'':d===0?'ok':'bad')+'">'+(hasR?R.paragraphs:'–')+'</div><div class="cap">the document has</div></div></div>',
    (hasR?(d===0?'<p class="ok">Same count.</p>':'<p class="bad">'+Math.abs(d)+' '+(d<0?'fewer':'more')+' than the document has.</p>'):'<p>No reference in this file.</p>')+(A.flaggedParas?'<p class="bad">'+A.flaggedParas+' may contain footnote text.</p>':''),
    'every line that is a number and a full stop (“12.” alone, or “12. Text”) starts a paragraph; the reference is the document’s own count.');
  const t2=tile('PAGES FLAGGED','<div class="big'+(A.flagPages.length?' bad':'')+'">'+A.flagPages.length+'<span class="cap"> of '+A.pages+' pages</span></div>',
    (A.flagPages.length?'<p>Footnote text may sit inside a paragraph; '+link('tab:3','see tab 03')+'.</p>':'<p class="ok">No page has suspect lines.</p>')+'<p>'+(R.footnotes!=null?'The document has '+R.footnotes+' footnotes; this version does not separate them.':'This version does not separate footnotes.')+'</p>',
    'a page is flagged when a line inside a paragraph is a bare number or starts with a number, a space and a capital letter; the rest of that page is then suspect.');
  const t3=tile('FIRST WORDS MATCH','<div class="big">'+(R.fw?A.fwMatches:'–')+'<span class="cap"> of '+(R.paragraphs!=null?R.paragraphs:'?')+'</span></div>',R.fw?(A.fwMatches===R.paragraphs?'<p class="ok">Every paragraph starts as the reference says.</p>':'<p class="bad">'+(A.paras.length-A.fwMatches)+' found paragraphs differ or have no reference entry.</p>'):'<p>No reference in this file.</p>',
    'the first six words of each paragraph, footnote marks removed, against the reference’s words; quotes and dashes are normalised, case is kept.');
  const t4=tile('REPAIRS MADE','<div class="big">'+A.repairs.length+'</div>','<p>'+link('repairs','Open the repair log')+'</p>','every line the script removed, split or joined, one entry each; nothing is changed silently.');
  const note=hasR&&d===0&&A.flagPages.length?'<p>The count is right, but footnote text may still sit inside some paragraphs. Check the flagged ones against the PDF before you quote them.</p>':'';
  return '<h2 class="q">Did the app find everything the document has?</h2><div class="tiles">'+t1+t2+t3+t4+'</div>'+note;
}

function tab2(A){
  const R=A.R,P=A.paras,hasR=R.paragraphs!=null;
  const rows=P.map(p=>{
    const c=[];
    if(p.fwMatch===false)c.push('<span class="bad">first words differ</span>');
    if(p.flagged)c.push(link('page:'+p.flagPage,'may contain footnote text','bad'));
    if(!c.length)c.push(p.fwMatch===null?'<span class="mut">no reference</span>':'OK');
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="d'+p.number+'">'+p.number+'</button></td><td>'+esc(p.section||'–')+'</td><td class="r num">'+rng(p)+'</td><td>'+esc(cut(p.text,120)||'(empty)')+'</td><td>'+c.join('<br>')+'</td></tr><tr id="d'+p.number+'" data-n="'+p.number+'" hidden><td colspan="5"></td></tr>';
  }).join('');
  const hd=A.heads.map(h=>'<li>'+esc(h.text)+' <span class="sm">· page '+h.page+(h.kind==='plain'?' · unlabelled':'')+(h.next!=null?' · '+link('para:'+h.next,'before para. '+h.next):'')+'</span></li>').join('');
  return '<h2 class="q">What does each paragraph say, and how do I cite it?</h2>'
   +'<div class="box"><h3 style="margin:0"><button class="head" data-toggle="hbox" aria-expanded="false" aria-controls="hbox">Headings found: '+A.heads.length+'</button></h3><div id="hbox" hidden><p class="how">Headings are kept out of the paragraph text. Unlabelled ones were found by their position just before a paragraph number.</p>'+(hd?'<ol>'+hd+'</ol>':'<p>No headings found.</p>')+'</div></div>'
   +(P.length?'<table class="data"><caption><span class="mono">TAB.01</span>'+P.length+' paragraphs found, '+(hasR?R.paragraphs+' expected':'no reference in this file')+'</caption><thead><tr><th scope="col" class="r">No.</th><th scope="col">Section</th><th scope="col" class="r">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text of '+pl(A.pages,'page')+'. Click a row to read the paragraph and copy its citation.</p>':'<p>No numbered paragraph was found in this text.</p>');
}

function rawLines(pg){
  return pg.lines.map(l=>{
    const k=l.t===''?'blank':l.sus?'suspect':(l.cls&&CODE[l.cls]?l.cls:'unk');
    return '<div class="rl c-'+k+'"><span class="ln">'+l.ln+'</span><span class="code" aria-label="'+k+'">'+(k==='blank'?'':k==='unk'?'?':CODE[k])+'</span><span>'+esc(l.t)+'</span></div>';
  }).join('');
}
const legend='<div class="legend" aria-label="Legend"><span class="c-cover">C cover</span><span class="c-header">H header</span><span class="c-heading">T heading</span><span class="c-paragraph">P paragraph</span><span class="c-suspect">S suspect line</span><span class="c-footer">F footer</span></div>';

function tab3(A){
  const F=A.flagPages;
  if(!F.length)return '<h2 class="q">Which paragraphs should I check against the PDF?</h2><p>No page is flagged: no line inside a paragraph looks like footnote text.</p>';
  const rows=F.map(e=>{
    const why=[...e.reasons].map(r=>REASON[r]).join('; ');
    const first=e.sus.length?'<span class="mn">'+esc(cut(e.sus[0].text,36))+'</span>':'–';
    return '<tr class="prow"><td class="r num"><button class="rowbtn" aria-expanded="false" aria-controls="f'+e.page+'">'+e.page+'</button></td><td class="r num">'+e.paras.join(', ')+'</td><td>'+e.sus.length+(e.sus.length?' · first: '+first:'')+'</td><td>'+esc(why||'follows a suspect line')+'</td></tr><tr id="f'+e.page+'" data-page="'+e.page+'" hidden><td colspan="4"></td></tr>';
  }).join('');
  return '<h2 class="q">Which paragraphs should I check against the PDF?</h2>'
   +'<p>This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them.</p>'
   +'<p class="how">A <b>suspect line</b> is a line inside a paragraph that looks like a footnote: a bare number, a number and a capital letter, or an asterisk. The rest of that page is suspect too. A <b>flagged page</b> has at least one.</p>'
   +'<table class="data"><caption><span class="mono">TAB.02</span>'+F.length+' of '+A.pages+' pages flagged</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col" class="r">Paragraph</th><th scope="col">Suspect lines</th><th scope="col">Why</th></tr></thead><tbody>'+rows+'</tbody></table><p class="src">Source: '+esc(A.symbol)+', raw text. Suspect lines stay in the paragraph text; none is removed.</p>';
}

function tab4(A){
  const st={pass:'PASS',fail:'CHECK FAILED',info:'FLAGGED',notrun:'NOT RUN'};
  const chk=A.checks.map(c=>{
    const lim=c.items.slice(0,14);
    const li=lim.map(i=>'<li>'+(i.go?'<button data-go="'+esc(i.go)+'">'+esc(i.t)+'</button>':esc(i.t))+'</li>').join('')+(c.items.length>14?'<li>and '+(c.items.length-14)+' more</li>':'');
    return '<li><div class="ch"><span class="st '+c.status+'">'+(c.status==='info'&&c.id==='head'?'FOR INFORMATION':st[c.status])+'</span><strong>'+c.name+'</strong><span>'+esc(c.line)+'</span></div>'+(li?'<ul class="items">'+li+'</ul>':'')+'</li>';
  }).join('');
  const kinds=Object.keys(KIND).map(k=>'<span>'+KIND[k]+': <b>'+A.repairs.filter(r=>r.kind===KIND[k]).length+'</b></span>').join('');
  const rl=A.repairs.map(r=>'<tr><td class="r num">'+r.page+'</td><td>'+(r.para!=null?'para. '+r.para:'page')+'</td><td>'+esc(r.kind)+'</td><td class="mn" title="'+esc(r.before)+'">'+esc(cut(r.before,110))+'</td><td class="mn" title="'+esc(r.after)+'">'+esc(cut(r.after,110))+'</td></tr>').join('');
  const opts=A.rawPages.map((p,i)=>'<option value="'+i+'">'+p.page+'</option>').join('');
  return '<h2 class="q">Can I trust this, and can I take it away?</h2>'
   +'<h3 class="mono">CHECKS · TAB.04</h3><ul class="checks">'+chk+'</ul>'
   +'<ol class="steps"><li>Header and footer lines are removed page by page; every page’s remaining lines are joined in page order.</li><li>A line like “12.” or “12. Text” starts a paragraph; roman and lettered lines open headings.</li><li>Unlabelled headings are lines just before a paragraph number that look like titles.</li><li>Lines are joined with one space; '+pl(A.hyphen,'line')+' ended with a hyphen, none was joined.</li><li>Footnote text is not separated; it is flagged.</li></ol>'
   +'<h3 style="margin:24px 0 0"><button class="head" data-toggle="replog" aria-expanded="false" aria-controls="replog" id="replogbtn">Repair log ('+A.repairs.length+')</button></h3><div id="replog" hidden><div class="kinds">'+kinds+'</div><table class="data"><caption><span class="mono">TAB.03</span>'+A.repairs.length+' repairs, in document order</caption><thead><tr><th scope="col" class="r">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead><tbody>'+rl+'</tbody></table></div>'
   +'<h3 style="margin:18px 0 0"><button class="head" data-toggle="rawbox" aria-expanded="false" aria-controls="rawbox" id="rawbtn">Raw pages</button></h3><div id="rawbox" hidden><p><label>Show raw page <select id="rawsel">'+opts+'</select></label></p>'+legend+'<div class="raw" id="rawview" tabindex="0"></div><p class="how">Each line is coloured by what the script decided it was, and carries a letter code. A red outline marks a line that no rule classified.</p></div>'
   +'<h3 class="mono">DOWNLOAD</h3><button class="btn pri" id="csv">Download paragraphs as CSV</button><span class="copied" id="csvmsg" role="status"></span>';
}

function paraDetail(A,p){
  const th=p.lines.map(l=>{const s=esc(l.pt).replace(/ {2,}/g,' ');return l.sus?'<mark class="sus">'+s+'</mark>':s;}).join(' ');
  let lp=null,pre='';
  p.lines.forEach(l=>{if(l.page!==lp){pre+='<span class="pg">── page '+l.page+(lp==null?'':' begins')+' ──</span>\n';lp=l.page;}pre+=(l.sus?'<mark class="sus">'+esc(l.t)+'</mark>':esc(l.t))+'\n';});
  const reps=p.repairs.length?'<ul style="margin:0;padding-left:18px">'+p.repairs.map(r=>'<li>'+esc(r.kind)+' <span class="sm">(page '+r.page+')</span></li>').join('')+'</ul>':'none';
  const fw=p.fwRef==null?'no reference entry':'reference “'+esc(p.fwRef)+'”<br>found “'+esc(p.fwFound)+'” · '+(p.fwMatch?'<b class="ok">equal</b>':'<b class="bad">different</b>');
  return '<div class="pd"><div class="path mono">'+esc(p.sect.join(' › ')||'no heading above')+'</div><p class="ptext">'+(th||'(no text)')+'</p>'
   +(p.sus.length?'<p class="how bad">Highlighted: '+pl(p.sus.length,'suspect line')+' that may be footnote text. Check this paragraph against the PDF.</p>':'')+(p.long?'<p class="how bad">'+p.words+' words: longer than 300, check it against the PDF.</p>':'')
   +'<button class="tgl" data-lines="1" aria-expanded="false">Show the PDF’s lines</button><pre class="lines" hidden>'+pre+'</pre>'
   +'<dl class="kv"><dt>First words</dt><dd>'+fw+'</dd><dt>Page(s)</dt><dd>'+rng(p)+'</dd><dt>Repairs</dt><dd>'+reps+'</dd></dl>'
   +'<button class="btn" data-copy="'+esc(p.citation)+'">Copy citation</button> <code>'+esc(p.citation)+'</code><span class="copied" role="status"></span></div>';
}
function pageDetail(A,e){
  const pg=A.rawPages.find(x=>x.page===e.page);
  return '<div class="pd" style="max-width:none"><p>Paragraph'+(e.paras.length>1?'s':'')+' the suspect lines sit in: '+e.paras.map(n=>link('para:'+n,'para. '+n)).join(', ')+'. Highlighted lines are suspect.</p>'+legend+'<div class="raw">'+(pg?rawLines(pg):'')+'</div></div>';
}

/* ---------- interaction ---------- */
function setTab(n,focus){
  tab=n;
  document.querySelectorAll('#tabs button').forEach(b=>{const on=+b.dataset.tab===n;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;if(on&&focus)b.focus();});
  [1,2,3,4].forEach(i=>{const p=$('#p'+i);p.hidden=i!==n;if(i===n)p.tabIndex=0;else p.removeAttribute('tabindex');});
}
function toggle(btn,force){
  const open=force===undefined?btn.getAttribute('aria-expanded')!=='true':force;
  btn.setAttribute('aria-expanded',open);
  const t=document.getElementById(btn.getAttribute('aria-controls'));
  if(t)t.hidden=!open;
  if(open&&t&&t.id==='rawbox')showRaw(+$('#rawsel').value);
  return t;
}
function toggleRow(tr,force){
  const btn=tr.querySelector('button[aria-expanded]');if(!btn)return;
  const det=toggle(btn,force);
  if(det&&!det.hidden&&!det.dataset.built){
    const A=cur();
    det.firstElementChild.innerHTML=det.dataset.n?paraDetail(A,A.paras.find(p=>String(p.number)===det.dataset.n)):pageDetail(A,A.flagPages.find(e=>String(e.page)===det.dataset.page));
    det.dataset.built='1';
  }
}
function showRaw(i){const A=cur(),pg=A.rawPages[i];if(pg)$('#rawview').innerHTML=rawLines(pg);}
function go(spec){
  const [k,v]=spec.split(':');let el=null;
  if(k==='tab'){setTab(+v);return;}
  if(k==='para'){setTab(2);const b=document.querySelector('button[aria-controls="d'+v+'"]');if(b){const tr=b.closest('tr');if(b.getAttribute('aria-expanded')!=='true')toggleRow(tr,true);el=b;}}
  if(k==='page'){setTab(3);const b=document.querySelector('button[aria-controls="f'+v+'"]');if(b){const tr=b.closest('tr');if(b.getAttribute('aria-expanded')!=='true')toggleRow(tr,true);el=b;}}
  if(k==='repairs'){setTab(4);el=$('#replogbtn');toggle(el,true);}
  if(k==='raw'){setTab(4);const b=$('#rawbtn');toggle(b,true);const A=cur();const i=A.rawPages.findIndex(p=>String(p.page)===v);if(i>=0){$('#rawsel').value=i;showRaw(i);}el=$('#rawview');}
  if(el){el.scrollIntoView({block:'center'});el.focus();}
}
function copyText(txt,done){
  const fb=()=>{try{const ta=document.createElement('textarea');ta.value=txt;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();const ok=document.execCommand('copy');ta.remove();return ok;}catch(e){return false;}};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(()=>done(true),()=>done(fb()));else done(fb());
}
function downloadCsv(){
  const A=cur(),cols=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','flagged','suspect_lines','repairs','citation','symbol','doc_url'];
  const q=v=>'"'+String(v==null?'':v).replace(/"/g,'""')+'"';
  const rows=A.paras.map(p=>[p.number,p.section,p.part,p.pageStart,p.pageEnd,p.fwRef==null?'':p.fwRef,p.fwFound,p.fwMatch==null?'':p.fwMatch,p.text,p.textRaw,p.flagged,p.sus.map(s=>'p.'+s.page+' l.'+s.ln+': '+s.text).join(' | '),p.repairs.map(r=>r.kind+' (p.'+r.page+')').join('; '),p.citation,A.symbol,A.D.doc_url||'']);
  const csv='﻿'+[cols].concat(rows).map(r=>r.map(q).join(',')).join('\r\n')+'\r\n';
  const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download=(A.symbol||'paragraphs').replace(/[\/\\]+/g,'-')+'.csv';document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),4000);
  $('#csvmsg').textContent=A.paras.length+' rows prepared. If nothing was saved, your browser blocked the download.';
}

document.addEventListener('click',e=>{
  const t=e.target;let x;
  if((x=t.closest('[data-go]'))){e.preventDefault();go(x.dataset.go);return;}
  if((x=t.closest('#tabs [data-tab]'))){setTab(+x.dataset.tab,true);return;}
  if((x=t.closest('[data-doc]'))){sel=+x.dataset.doc;render();const c=document.querySelector('[data-doc="'+sel+'"]');if(c)c.focus();return;}
  if((x=t.closest('[data-copy]'))){const m=x.parentNode.querySelector('.copied');copyText(x.dataset.copy,ok=>{m.textContent=ok?'Copied':'Not copied: select the text and press Ctrl+C';setTimeout(()=>{m.textContent='';},2000);});return;}
  if((x=t.closest('[data-lines]'))){const pre=x.nextElementSibling;const o=x.getAttribute('aria-expanded')!=='true';x.setAttribute('aria-expanded',o);pre.hidden=!o;x.textContent=o?'Hide the PDF’s lines':'Show the PDF’s lines';return;}
  if((x=t.closest('button[data-toggle]'))){toggle(x);return;}
  if(t.closest('#csv')){downloadCsv();return;}
  if((x=t.closest('tr.prow'))){toggleRow(x);}
});
document.addEventListener('change',e=>{if(e.target.id==='rawsel')showRaw(+e.target.value);});
document.addEventListener('keydown',e=>{
  if(!e.target.closest||!e.target.closest('#tabs'))return;
  const k=e.key,i=tab-1;let n=null;
  if(k==='ArrowRight'||k==='ArrowDown')n=(i+1)%4;else if(k==='ArrowLeft'||k==='ArrowUp')n=(i+3)%4;else if(k==='Home')n=0;else if(k==='End')n=3;
  if(n!==null){e.preventDefault();setTab(n+1,true);}
});

function render(){
  if(!keys.length){
    $('#title').textContent='No PDF text in this data';
    $('#meta').textContent='';
    $('#status').textContent='';
    $('main').innerHTML='<p>The workshop data has no document with pages of raw text (records with a page number and a text). Attach a PDF text file from “Your files” and build again.</p>';
    $('#foot').innerHTML='<p>Nothing was computed; no model was called and nothing left the browser.</p>';
    return;
  }
  const A=cur(),D=A.D,u=safeUrl(D.doc_url);
  if(A.err){
    $('#title').textContent=D.title||D.symbol||keys[sel];
    $('#meta').textContent=D.symbol||'';
    $('#status').innerHTML='<span class="dot bad"></span>could not be read';
    $('#rail').innerHTML=rail(A);
    $('#tabs').innerHTML='';
    [1,2,3,4].forEach(i=>{$('#p'+i).innerHTML='';});
    $('#p1').innerHTML='<p class="bad">This document could not be analysed: '+esc(A.err)+'. The other document is not affected; choose it in the rail.</p>';
    $('#foot').innerHTML='<p>Nothing was computed for this document; no model was called and nothing left the browser.</p>';
    setTab(1,false);
    return;
  }
  $('#title').textContent=D.title||A.symbol;
  $('#meta').innerHTML=(u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(A.symbol)+'</a>':esc(A.symbol))+(A.R.adopted?' · adopted '+esc(A.R.adopted):'')+' · '+pl(A.pages,'page')+' of raw converter text'+(D.source?' · '+esc(D.source):'');
  $('#status').innerHTML=A.nFail?'<span class="dot bad"></span>'+pl(A.nFail,'check')+' failed':'<span class="dot '+(A.nNot?'':'ok')+'"></span>'+A.nPass+' of '+A.m+' checks pass';
  $('#rail').innerHTML=rail(A);
  const names=['01 RESULT','02 PARAGRAPHS','03 FLAGGED PAGES','04 CHECKS &amp; METHOD'];
  $('#tabs').innerHTML=names.map((nm,i)=>'<button role="tab" id="t'+(i+1)+'" data-tab="'+(i+1)+'" aria-controls="p'+(i+1)+'" aria-selected="false" tabindex="-1">'+nm+(i===3&&A.nFail?' <span class="dot bad"></span><span class="sr">checks failed</span>':'')+'</button>').join('');
  $('#p1').innerHTML=tab1(A);$('#p2').innerHTML=tab2(A);$('#p3').innerHTML=tab3(A);$('#p4').innerHTML=tab4(A);
  $('#foot').innerHTML='<p>Source: '+esc(D.source||D.title||A.symbol)+(D.built?' · built '+esc(D.built):'')+'</p><p>Counting, splitting, matching and flagging are done by this page’s code; no model was called and nothing left the browser.</p>';
  setTab(tab,false);
}
render();
})();
</script>
</body>
</html>
```


# USER MESSAGE

Add a button "Check the flagged pages with the model". For every flagged page, where footnote text may sit inside a paragraph, it sends that page's numbered lines to the model with `studio.ask`, one page per call, and asks only which lines are paragraph text (with the paragraph number), which are footnotes (with their numbers) and which are headers, footers or blank; the model must never retype text. The code cuts the text from those line numbers, takes the footnotes out of the paragraphs and runs the checks again, now also counting the footnotes against the reference. Accept the model's answer for a page only if every line is used exactly once, the footnote numbers continue from the page before, and every footnote mark in the page's paragraphs has its footnote. Also send one page that was not flagged, if there is one, as a control, and distrust the model if it disagrees with the script there. Before it runs, say how many pages will leave the browser; show progress and a Stop button. Then show, for each document, what the script found, what the model changed, and the pages that still need a person.

(Attached: CCPR General comment No. 32 (PDF) → WORKSHOP_DATA.pdf_text_2)
