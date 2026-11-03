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
