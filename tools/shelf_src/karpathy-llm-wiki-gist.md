---
id: karpathy-llm-wiki-gist
title: "Andrej Karpathy: \"LLM Wiki\", a pattern for LLM-maintained knowledge bases (summary)"
publisher: "Andrej Karpathy"
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
licence: summary
licence_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
retrieved: 2026-11-02
kind: summary
topics: [llm-wiki, knowledge-base, rag, markdown, search, workflow]
---
> Summary of the GitHub gist "LLM Wiki" (file llm-wiki.md, revision ac46de1ad27f92b28ac95459c782c07f6b8c964a) by Andrej Karpathy. Original: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f . Retrieved 2026-11-02.
> The gist states no licence, so no text is reproduced; this is an original summary. Only the gist's own text was used, not the comments under it. Where the gist describes its author's tools or habits, the summary says so.

## Summary written for the workshop

**What the document is.** A short idea file that describes a way of building a personal knowledge base with the help of a language model agent. Its author keeps it abstract on purpose: it describes a pattern, and the reader and their agent are expected to work out the details together.

**The contrast with ordinary retrieval.** In the familiar setup (upload files, retrieve passages when a question arrives, generate an answer) the model rebuilds its understanding from raw fragments each time, so nothing accumulates. The proposed alternative is that the agent writes and maintains a persistent wiki of interlinked markdown pages between the user and the raw sources. When a new source arrives the agent reads it and integrates it: it updates existing pages, revises summaries, links related pages and flags where the new material contradicts older claims. The synthesis is therefore done once and kept up to date, and cross-references and contradictions are already marked when a question is asked. The human selects sources, directs the analysis and asks the questions; the agent does the summarising, filing and bookkeeping.

**Three layers.**

1. *Raw sources*: the user's curated documents. They are never edited by the agent and remain the source of truth.
2. *The wiki*: markdown files written and kept consistent by the agent (summaries, pages about entities and concepts, comparisons, an overview).
3. *The schema*: a configuration document (the gist mentions the instruction files used by coding agents) that tells the agent how the wiki is organised, what conventions apply and which workflows to follow. User and agent refine it over time.

**Three operations.**

- *Ingest*: add a source; the agent discusses it, writes a summary page, updates the index and the relevant pages and adds a log entry. A single source may touch ten or fifteen pages. The author prefers to ingest one source at a time and stay involved, but notes that batch ingestion is possible.
- *Query*: ask questions against the wiki; the agent finds relevant pages and answers with citations. Good answers can be filed back as new pages so that explorations also accumulate.
- *Lint*: periodically check the wiki for contradictions, outdated claims, pages nobody links to, concepts that deserve their own page, missing cross-references and gaps that a search could fill.

**Two navigation files.** `index.md` is a catalogue of every page with a link and a one-line description, grouped by category and updated on every ingest; the agent reads it first to locate pages, which the author reports works well up to around a hundred sources and several hundred pages. `log.md` is an append-only chronological record; a consistent heading prefix for each entry (date, operation, title) makes it easy to search with simple command-line tools.

**Optional tooling.** As a wiki grows, a proper search tool helps. The gist mentions one local markdown search engine that combines keyword (BM25) and vector search with model re-ranking and offers both a command-line and an agent-tool interface, and says an agent can also help write a small search script.

**Tips from the author's own set-up.** The author works with an agent in one window and a note-taking application in another and watches the wiki change. Other tips: a web clipper to turn articles into markdown, downloading images locally so the agent can view them, a graph view to see hubs and orphan pages, slide and chart output from wiki content, and frontmatter on pages so a query plugin can build tables. The wiki is just a folder of markdown files, so version control gives history and collaboration for free.

**Why the author thinks it works.** The costly part of any knowledge base is upkeep, not reading or thinking: people abandon wikis because cross-references and summaries go stale. An agent does not tire of that bookkeeping and can edit many files in a pass. The author compares the idea to Vannevar Bush's Memex of 1945, whose unsolved problem was who would do the maintenance.

## Notes for the workshop

- For a small research wiki, start with the three layers and the two files; add search only when the index is no longer enough.
- Decide in the schema what a page must contain (for example a source link and a date), so that the agent's output can be checked. The own-work schema excerpt on this shelf is one worked example.
- Keep raw sources read-only and keep the wiki under version control so that every agent edit can be reviewed.
