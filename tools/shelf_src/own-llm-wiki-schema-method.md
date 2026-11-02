---
id: own-llm-wiki-schema-method
title: "Own work: a schema for an LLM-maintained research wiki (page types, frontmatter, direct links, pin verification, registers, contested claims)"
publisher: "Łukasz Szoszkiewicz (own work)"
url: n/a
licence: own-work
licence_url: n/a
retrieved: 2026-11-02
kind: excerpt
topics: [llm-wiki, knowledge-base, schema, verification, citations, research-workflow]
---
> Excerpt, general method only, from the author's own schema document for a private LLM-maintained research wiki (the schema layer of the pattern described in the Karpathy LLM-wiki page also on this shelf). Own work of Łukasz Szoszkiewicz, shared for the workshop; unpublished, so there is no public URL. Retrieved 2026-11-02.
> Subject-matter examples, source locations, tool names, scripts and local paths of the original are left out; "[…]" marks every cut. The original headings were reduced to the ones kept here.

# Wiki schema: page types, frontmatter, direct links, pin verification, registers, contested claims, operations

## Page types

| Type | Folder | What it is |
|---|---|---|
| `concept` | `concepts/` | A cross-lens idea ([…]). **The compounding core.** |
| `source` | `sources/` | One page per ingested source — paper, case, […] video, URL. |
| `entity` | `entities/` | An instrument, provision, case, GC, study, delegation, or person. |
| `question` | `questions/` | An answered query, filed back as a page. |

`index.md` is the catalog (one line per page). `log.md` is the append-only record of ingests / queries / lints. `inbox/` holds raw fetched externals + stubs awaiting ingest.

## Frontmatter (required on every page)

```yaml
---
title: […]
type: concept              # concept | source | entity | question
tags: […]
lenses: […]   # which lenses have content
status: draft              # draft | reviewed | stable | option(=decision-pending)
updated: 2026-07-21
links: […]   # [[slug]] of related pages
[…]
sources: […]
---
```

Page filename = the slug (kebab-case). `[[slug]]` links resolve to `concepts|sources|entities|questions/<slug>.md`. A `[[slug]]` that doesn't exist yet is a valid *stub target* (Lint reports it).

## Conventions

1. **Direct-link rule (Wikipedia-style).** Every factual claim carries an inline link straight to its source: a URL, a **local file** `[label](file:///abs/path.pdf#page=12)` […]
2. **Pin-verification.** Every UN/treaty pin is stamped `✓ verified {YYYY-MM-DD}` (and stores the retrieved verbatim + `para_id`/`annotation_id`) or `⚠ unverified`. […] Lint re-checks.
3. **Link, don't duplicate.** Point to canonical files […]; never copy […] text into the wiki.

[…]

5. **Distinguish the four legal registers:** (a) binding law, (b) treaty-body interpretation/GCs, (c) soft law, (d) authorial proposal. Never blur them.

[…]

7. **Open ≠ adopted.** A page for a decision-pending idea […] is `status: option` and must say plainly it is not the […] committed position.

[…]

9. **Contested claims (consensus, authority-weighted).** Where sources disagree on a claim, record it in a `` ```contested `` block (rendered as a consensus card: authored verdict + authority-weighted lean bar + tier ladder of traceable for/against positions). Grade every position by the **interpretive-authority hierarchy** for treaty-body material — **T1** treaty text · **T2** General Comments · **T3** jurisprudence & travaux préparatoires · **T4** Concluding Observations / official TB statements · **T5** mandate holders (Special Procedures) · **Sch** commentary & regional courts (persuasive, non-TB). The lean bar is *descriptive* (weighted 5·4·3·2·1·½); the **authored `verdict:` and `note:` lead** — a higher tier can be dispositive, so never read the raw percentage as the answer. Every position carries a verbatim + `para_id`/link […]. Block format:
   ````
   ```contested
   claim: <the disputed statement>
   verdict: settled-support | leans-support | contested | leans-contest | settled-contest
   note: <one-line authored reading — where the real weight lies>
   + T2 | GC34 ¶9 | <short verbatim> | <wiki-slug or blank> | <para_id> | <source URL>
   […]
   ```
   ````
   `+` supports · `−`/`-` contests · `~` mixed. Fields are `|`-separated: tier · source · verbatim · wiki-ref · para_id · link.

[…]

## Operations

- **Ingest(source).** […] Agent reads → **discusses takeaways with the author** → writes the `sources/` page → creates/updates `concepts/`+`entities/` […] → verifies pins live […] → updates `index.md` → appends `log.md` → […].
- **Query(question).** Search […] → cited synthesis → optionally file back as a `questions/` page.
- **Lint.** […]: contradictions, stale claims, orphan pages, dangling `[[links]]`, coverage gaps, `⚠ unverified` pins.
