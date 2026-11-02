# WIKI.md: schema and operating manual

A research wiki on **neurotechnology in the administration of justice**, kept by language models for the hands-on sessions of *AI for Human Rights Professionals* (Geneva Human Rights Hub and ITU, 4 December 2026). It follows the "LLM wiki" pattern: people choose the sources and ask the questions; the model reads the sources, writes and files the pages, and does the bookkeeping. Knowledge is compiled once and kept current, not rediscovered at every question.

Three layers:

1. **The library** (raw sources): `WORKSHOP_DATA.library`, ten documents passage by passage, each passage with the PDF page it starts on. Read-only: the wiki never changes a source.
2. **The wiki** (this folder): markdown pages written by the model, linked to each other and pinned to the library.
3. **This file** (the schema): what a page looks like, how a claim is pinned and checked, and what Ingest, Ask and Lint do.

Built on 2 November 2026 from nine documents. The tenth, A/HRC/57/61, waits in the inbox for the live ingest.

## The library and its registers

| id | cite as | register | kind |
|---|---|---|---|
| A/81/351 | A/81/351 | c | UN report (Secretary-General, 2026) |
| UNODC-INTERPOL-2025 | UNODC–INTERPOL 2025 | c | UN agency paper (2025) |
| A/HRC/57/61 | A/HRC/57/61 | c | UN report (Human Rights Council Advisory Committee, 2024), **inbox** |
| AHRC-2025 | AHRC 2025 | d | National human rights institution report (2025) |
| FuturesLab-2026 | Futures Lab 2026 | e | Civil-society submission (2026) |
| Szoszkiewicz-Yuste-2025 | Szoszkiewicz & Yuste 2025 | f | Journal article (2025) |
| Prainsack-et-al-2022 | Prainsack et al. 2022 | f | Journal article (2022) |
| CCPR/C/21/Rev.1/Add.4 | General Comment No. 22 | b | General Comment of the Human Rights Committee (1993) |
| CCPR/C/GC/32 | General Comment No. 32 | b | General Comment of the Human Rights Committee (2007) |
| CCPR/C/GC/34 | General Comment No. 34 | b | General Comment of the Human Rights Committee (2011) |

Six registers, never blurred:

- **(a) treaty law**: binding treaty text (the ICCPR). Not in the library: see *Treaty text* below.
- **(b) treaty-body interpretation**: General Comments of the Human Rights Committee.
- **(c) UN, agency and soft-law reports**: the Secretary-General, UNODC and INTERPOL, the Human Rights Council Advisory Committee, UNESCO.
- **(d) national human rights institution (NHRI)**: the Australian Human Rights Commission.
- **(e) civil society**: the Futures Lab submission.
- **(f) scholarship**: journal articles.

A claim has the register of the document that makes it. A report that quotes a General Comment does not become (b): pin the General Comment itself, and the report only for what the report adds.

## Page types

| type | folder | what it is |
|---|---|---|
| `source` | `sources/` | One page per ingested library document: what it says, in its own words, with pins. |
| `concept` | `concepts/` | An idea across documents (mental privacy, neuroprediction). The compounding core. |
| `entity` | `entities/` | A thing in the world: a treaty article, a General Comment as an authority, a report, a case, a law. Gathers what the library says about it. |
| `question` | `questions/` | An answered question, filed back as a page. |

A source page reads one document; an entity page follows one thing through all documents. So General Comment No. 34 has both: `sources/ccpr-c-gc-34` (what it says) and `entities/general-comment-34` (who in the library relies on it, for what).

The filename is the slug (kebab-case). `[[slug]]` links to a page in any folder.

## Frontmatter (every page)

```yaml
---
title: Mental privacy
type: concept                 # source | concept | entity | question
tags: [privacy, neural-data, art-17]
register: [b, c, d, f]        # see below
status: reviewed              # stub | draft | reviewed
updated: 2026-11-02
links: [[neural-data]], [[iccpr-art-17]]
sources: [A/81/351, AHRC-2025, Szoszkiewicz-Yuste-2025]
---
```

- `register`: a source page has its document's letter; an entity page the letter of the thing itself (an ICCPR article is `[a]`); a concept or question page every register its pins draw on.
- `sources`: the library ids the page pins. Never empty.
- `links`: the related pages, as `[[slug]]`.
- `stub`: a page that exists before its source is ingested (e.g. `a-hrc-57-61`).

## Pins: the direct-link rule

Every factual claim carries a **pin**: a link to one library document at one PDF page, which opens the PDF there (`studio.openSource(id, page)`). The syntax is a markdown link with a `pin:` address, the verbatim quote as its title, and a mark:

```
[LABEL](pin:DOC#pPAGE "QUOTE") ✓
```

- `DOC`: the library id (first column above).
- `PAGE`: the PDF page on which the quoted passage starts (`passage.page`), not the number printed on the page.
- `LABEL`: how a reader cites it: `<cite as>, para. <paragraph>` when the passage has a paragraph number, otherwise `<cite as>, p. <page_label>` (the printed page).
- `QUOTE`: words copied verbatim from that one passage. `…` joins fragments of the same passage, in order. Inside the quote, write double quotes as “ ”, never as `"`.
- Mark: `✓` verified, `⚠` unverified.

Example:

```
The Secretary-General records both views without choosing [A/81/351, para. 16](pin:A/81/351#p6 "While some contend that the challenges of neurotechnology may require development of new legal frameworks, others affirm that the risks of misuse or abuse of neurotechnology may be addressed within the existing international human rights law framework") ✓.
```

One regular expression finds every pin (JavaScript and Python alike):

```
\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)
```

Groups: 1 label, 2 document id, 3 PDF page, 4 quote, 5 mark.

### Pin verification

A pin is **✓ verified** when the quote is found in a passage of that document that starts on that PDF page, and the label's paragraph or printed page is that passage's. Before comparing, both sides are normalised: Unicode NFKC; curly quotes and apostrophes made straight; dashes made hyphens; a hyphen and the space after it removed ("decision- making" = "decision-making" = "decisionmaking"); runs of whitespace made one space. Words and capitals must match.

A pin is **⚠ unverified** when it has no quote or has not been checked. A `✓` that fails is an error, not a warning. `python3 tools/wiki_verify.py` checks every pin; the target is 100% ✓.

What a pin cannot verify: the passages leave out footnotes, tables, captions and running heads. A claim about a footnote pins the paragraph that carries it and says so ("in its footnote 7, on the same page"); a reader checks the footnote by eye in the PDF.

**Treaty text.** The ICCPR is not in the library. An entity page for an article may quote it from the official text with a plain link, marked (a), e.g. `[ICCPR art. 14(3)(g)](https://www.ohchr.org/en/instruments-mechanisms/instruments/international-covenant-civil-and-political-rights)`. That link is not a pin; every other claim on the page is pinned.

**Inbox documents** are not pinned until they are ingested.

## Conventions

1. **Direct links.** Every factual claim carries a pin; every pin opens its page.
2. **Pin verification.** ✓ only after the check above; otherwise ⚠.
3. **Registers.** Name the register when it matters ("the Secretary-General, a (c) report, notes…"). Never present (c)–(f) as what the treaty requires.
4. **The document's own verb.** "Recommends", "is of the view", "proposes", "could": keep it. A recommendation is not an obligation; "may constitute" is not "constitutes".
5. **Caveats travel with the data.** A source page has a **How NOT to read this** section wherever the document misstates a provision, overstates the science, or speaks for one country only.
6. **Link, don't duplicate.** A page summarises and pins; the full text stays in the library, one click away.
7. **English, in UN terms**: "the Human Rights Committee", "General Comment No. 34", "the Secretary-General", "States parties".

## Contested claims and the authority ladder

Where documents disagree, the page records it in a `contested` block, shown as a card:

````
```contested
claim: Existing human rights law is enough to deal with neurotechnology in criminal justice.
verdict: leans-support
note: One line on where the real weight lies.
+ d | [AHRC 2025, p. 30](pin:AHRC-2025#p30 "these debates appear to be settling in favour of interpreting and adapting existing rights") ✓ | an NHRI reads the debate as settling | [[ahrc-2025]]
- e | [Futures Lab 2026, p. 7](pin:FuturesLab-2026#p8 "the United Nations needs to develop new human rights standards that reflect the emerging and rapidly evolving nature of neurotechnology") ✓ | calls for new UN standards | [[futures-lab-2026]]
```
````

- `verdict`: `settled-support` · `leans-support` · `contested` · `leans-contest` · `settled-contest`.
- A position line: sign (`+` supports, `-` contests, `~` mixed) · register letter · a pin · a short gloss · the wiki page. The register is the pinned document's.
- **Authority ladder.** Weights by register: (a) 5 · (b) 4 · (c) 3 · (d) 2 · (e) 1 · (f) ½. The lean bar shows support = (Σ`+` + ½Σ`~`) / Σ all. It is descriptive. The authored `verdict` and `note` lead: a higher register can decide the matter alone (one General Comment outweighs any number of reports), so never read the percentage as the answer.
- Every contested card is listed in `TENSIONS.md`.

## Page anatomy

**Source page.** `# <cite as>: <short title>` → **Full cite.** · **Register.** (the letter, and why) · **One-liner.** → `## Key takeaways` (each pinned) → `## How NOT to read this` (where needed) → `## Where it feeds the wiki` (the concepts and entities it informs) → `## Related`.

**Concept page.** `# Title` → **One-liner.** → `## What the library says`, highest register first → `## Contested claims` (if any) → `## Open questions` → `## Related`.

**Entity page.** `# Title` → **What it is.** (body, date, register; official link if outside the library) → `## In the library` (who relies on it, for what, pinned) → `## Related`.

**Question page.** `# The question?` → **Short answer.** → `## Reasoning` (pinned) → `## What the library cannot answer` → `## Related`.

## Operations

- **Ingest(document).** For a document with status `inbox`: read every passage; discuss the takeaways with the user; write `sources/<slug>.md`; update the concept and entity pages it touches (new pins, links both ways, a contested card where it disagrees with the wiki, a stub turned into a page); add its lines to `index.md`; append to `log.md`; run Lint. One document typically touches five to fifteen pages.
- **Ask(question).** Read `index.md` first, then the pages it points to, then the passages they pin. Answer with pins only. A good answer can be filed back as `questions/<slug>.md`.
- **Lint.** `python3 tools/wiki_verify.py` checks every pin, dangling `[[links]]`, orphan pages, pages without sources, registers, contested cards and the index. Then read for what code cannot see: contradictions between pages, claims a newer document has overtaken, concepts named but without a page.

## index.md, log.md, TENSIONS.md

- **`index.md`**: the catalog, by type, one line per page: `- [[slug]] — one-liner · (registers) · ✓N`. Read first on every Ask; updated on every Ingest.
- **`log.md`**: append-only, oldest first. Each entry starts `## [YYYY-MM-DD] ingest | <document>` (or `ask`, `lint`, `schema`), so `grep "^## \[" log.md` lists them.
- **`TENSIONS.md`**: the register of open disagreements, one `###` entry per contested card:

```
### do-existing-rights-suffice
title: Do existing rights suffice?
status: open                  # open | leaning | settled
card: [[new-rights-vs-existing-rights]]
poles: existing rights, interpreted (AHRC 2025) || new standards (Futures Lab 2026)
where: [[a-81-351]], [[ahrc-2025]], [[futures-lab-2026]]
```

## Tools

```bash
python3 tools/wiki_verify.py                      # verify every pin and lint the wiki
python3 tools/wiki_verify.py --check FILE …       # one or more pages: frontmatter, pins, cards
python3 tools/wiki_verify.py --find "regex" [--doc ID]   # passages matching, with the pin to paste
python3 tools/wiki_verify.py --doc ID             # every passage of one document
python3 tools/wiki_verify.py --pdf                # also look for each ✓ quote on the PDF page itself
```
