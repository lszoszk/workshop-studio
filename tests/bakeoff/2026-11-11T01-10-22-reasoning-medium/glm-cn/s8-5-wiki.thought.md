Need to build a full HTML app, three tabs. Must render markdown (headings, lists, links, pins, contested blocks), lint checks, log/tensions. Keep under ~1500 lines. Let me plan carefully.

Data: WORKSHOP_DATA.wiki (pages, index, log, tensions markdown), WORKSHOP_DATA.library records with passages.

Pin verification: normalize text (whitespace, curly quotes, dashes, hyphenation). Find passage of doc id that starts on PDF page p. Quote may join fragments with "…" — each fragment in same passage, in order. Compare after normalizing.

Normalization: lowercase? Probably case-sensitive fine but normalize quotes ' ' → ', " " → ", dashes – — → -, hyphenation: "exam-\nple" → "example"? PDF text may break words. Normalise: collapse whitespace, remove soft hyphen + space? Simpler: normalize(s): s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ') and also remove '- ' (dehyphenate)? Risky but per instructions "hyphenation" is mentioned. I'll dehyphenate: replace(/-\s+/g,'-')? Actually hyphenation across lines: "con-\nscience" should become "conscience": remove hyphen followed by space? But that would break legit "word - word". I'll do: in passage text only, replace(/(\w)-\s+(\w)/g,'$1$2')? Hmm, could over-merge. Keep simple: normalize whitespace, quotes, dashes; then also try dehyphenated version as fallback. I'll normalize both passage and quote the same way, plus dehyphenate both: replace(/(\p{L})-\s+(?=\p{L})/gu,'$1'). Apply to both quote and passage consistently. Good enough.

Fragment ordering: for each fragment, search in passage starting from index after previous fragment.

Markdown rendering: minimal — handle #, ##, ###, -, **bold**, [[slug]] links, pins, ```contested blocks. Also paragraphs.

Contested block parsing: lines claim:, verdict:, note:, positions `+|-|~ | reg | pin | gloss | [[slug]]`.

Lint checks:
- Dangling links: [[slug]] not in pages.
- Orphan pages: no links in/out (excluding self)? Pages with no other page linking to them and no links out.
- Failed pins: verification false.
- Sources mismatch: frontmatter.sources vs library ids actually pinned in the page.
- Contested cards missing from tensions register: parse tensions markdown for claim lines? Tensions is markdown with ### entries. Check each contested block's claim appears in tensions text.

Header: title, source, n pages, count pins, library docs. Tabs 3.

Tab01: index list grouped by type with filter buttons (types). Click page → render page with back link. Pins rendered inline. Links out (frontmatter.links), Linked from (scan other pages' links), Sources (frontmatter.sources with library titles).

Tab02: big number verified/total, tables of each issue.

Tab03: log reversed, tensions markdown rendered, download wiki as JSON blob.

Keep clicks low. Write the code now, reasonably compact.

Contested card: verdict first, claim, note, positions with register weight lean bar? Spec says verdict first; I'll show lean bar too (weights a5,b4,c3,d2,e1,f0.5). Keep simple: show verdict, claim, note, positions list with +/- /~ mark, pin rendered as pin chip, gloss, link.

Pin HTML: `<span class="pin">"quote" <button class="pinchip" data-...>label</button> ✓/⚠</span>` clicking chip calls studio.openSource(id,page,quote).

Verification function cached.

Let me write the file.

Markdown body rendering approach: split into blocks by fenced ```contested ... ``` first via regex. For normal text: split lines, handle headings, list items (lines starting "- "), else paragraph. Inline: escape HTML, then pins regex replace, bold, [[links]].

Order of inline: escape first, then process pins (regex works on escaped text — quotes become &quot;? If I escape " to &quot; the pin quote containing " breaks). Use html-escape that doesn't escape quotes: replace & < > only. Quotes in pin quotes use curly " " mostly. Fine.

Render links: [[slug]] → button/anchor navigating to page, title lookup, styled. Slug may have section? Assume plain.

Also handle regular markdown links [label](pin:...) only in pins.

Tabs with arrow key nav per role=tablist.

Filter in tab01: buttons for All/source/concept/entity/question — that's 5 buttons + tabs 3 = 8 clicks... limit "no view shows more than ~7 things to click". Use a select dropdown instead. Good.

Download: JSON.stringify(WORKSHOP_DATA.wiki) blob.

Big number tab02: verified pins count / total.

Lint details:
- danglingLinks: per page, list [[slug]] not found.
- orphans: pages with no outgoing links and nothing links to them.
- failedPins: page, label.
- sourceMismatch: page frontmatter.sources vs pinned ids (both directions).
- contestedMissing: claims not found in tensions markdown (normalized containment).

Write it.