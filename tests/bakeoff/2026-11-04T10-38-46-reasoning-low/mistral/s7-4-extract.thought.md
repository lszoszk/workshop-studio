Let me understand the task. I need to build a single HTML app that parses `WORKSHOP_DATA.pdf_text` (raw PDF converter text of E/C.12/GC/27, 20 pages) into numbered paragraphs and footnotes, checks against `reference`, and shows repairs. The user gave a very detailed plan. I must follow it closely.

Key data: `WORKSHOP_DATA.pdf_text` = `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {paragraphs, footnotes, adopted, first_words}}`. Also `pdf_text_2` exists but the plan says "every document in WORKSHOP_DATA with records and a reference gets its own card in the rail" — so I should handle both pdf_text and pdf_text_2. The attached file is pdf_text, but the rail should list all documents with records+reference in order of the data. So I'll iterate over keys of WORKSHOP_DATA that have `records` and `reference`.

Let me design the parsing pipeline carefully per the spec:

1. Sort records by page.
2. For each page, split text into lines (split on \n, keep track). 
3. Header: first non-empty line equals symbol → drop, log "header line removed". Else warning.
4. Footer: from the end, drop lines while: empty, starts with "GE.", consists only of 6-digit groups (date stamp like "051125 061125"), or is a bare number 1-3 digits. Bare number equal to page → page number; other bare number → displaced footnote number kept aside.
5. Footnote block: counter nextFootnote starting at 1. On each page (after header/footer removal), find first line that is bare number == nextFootnote, or starts with nextFootnote + space, or starts with "* " on first page. From there to end of page = footnotes; before = body. Advance nextFootnote past highest number seen in block and past displaced number for that page. If no line opens nextFootnote, take first bare number greater than it before footer and log the jump. Page with no opener at all → all body, check panel says so.

Wait — careful: the footnote block detection. The body may contain lines starting with numbers? E.g., "6 November 2025" on cover — starts with "6 " but nextFootnote is 1 at that point, so it doesn't open. Good. But what about a line in body starting with "1 " when nextFootnote is 1? Hmm, the spec says the block starts at the first line that is a bare number equal to nextFootnote or starts with that number and a space. On page 1, nextFootnote=1. Is there any body line starting with "1 " before the footnote block? The cover has "1." paragraph start... "1." is bare number with a dot, not "1" alone or "1 ". The regex for "starts with that number and a space" — "1. A clean..." starts with "1." not "1 ". OK. But what about paragraph text lines starting with e.g. "1 January"? Unlikely. The spec says this rule works for this data. But also "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump". Hmm, wait — actually re-reading: "the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space, or starts with '* ' on the first page". So we search for the first line matching any of these. If none matches nextFootnote exactly, look for first bare number > nextFootnote before footer, log jump, and that's the block start.

Hmm, but there's subtlety: "starts with that number and a space" — e.g. footnote "7 E/2003/22…" starts with "7 ". But body text could have a line starting with "7 " if nextFootnote is 7? The footnote block is at the foot of the page, so the first such line in the page would be... hmm, could a body line start with "7 " while nextFootnote==7? Possibly in theory but not in this data. I'll follow the spec.

Actually wait, there's a risk: paragraph lines could start with a number+space, e.g. a line "2030 Agenda..." while nextFootnote is 20? "2030" starts with "20" but "2030" — does "2030 Agenda" start with "20" + space? No, it starts with "2030", the char after "20" is "3", not a space. So the check must be: line starts with `nextFootnote` followed by a space (i.e., `line.startsWith(n + " ")`) or line === String(n) (bare number). Also bare number equal — line is exactly the number. Also `* ` on first page.

But also "starts with that number and a space" — what about "7 E/2003/22" where nextFootnote is 7 — yes. What if a footnote line is "15 Human Rights Committee..." and nextFootnote is 15 — yes.

Edge: what if the first footnote on a page has a displaced number (the number is in the footer)? Then no line opens nextFootnote... wait no. Let me re-read the data description: "On each of those 12 pages the footnote without a number is the second on the page: it follows the first footnote's text directly, with no number and no blank line (page 2: '5', a blank line, 'A/79/270, paras. 84 and 85.', then 'A/42/427, p. 24.' is footnote 6)."

So on page 2: footnote block starts with bare "5" (nextFootnote=5 presumably), blank line, "A/79/270, paras. 84 and 85." (footnote 5 text), then "A/42/427, p. 24." — this is footnote 6 but has no number; its number 6 was displaced to the footer. So the block opener is "5" == nextFootnote. Good. Then within the block, footnote parsing: "a line that starts with a number and a space, or a bare number on its own line, opens a footnote". "A/42/427, p. 24." doesn't start with a number, so it would be glued to footnote 5. Hence the special rule: "On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D, marked repaired."

So: if page has displaced number D, then when parsing the footnote block, the first footnote (opened by bare number) ends at its first line ending with a full stop; subsequent lines up to the next numbered opener line belong to footnote D.

Hmm wait — "the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop". So footnote 5's text is "A/79/270, paras. 84 and 85." — one line ending with full stop. Then "A/42/427, p. 24." is footnote 6. But what if footnote 5's text spans multiple lines? The spec says "In all 12 cases the first footnote is one line ending with a full stop." So the rule: first footnote's text ends at first line ending with "."; lines after that until next numbered line = footnote D.

Actually more precisely: "the lines after it, up to the next numbered line, are footnote D". So after the first footnote's terminating line, collect lines until the next line that opens a footnote (number+space or bare number); those lines are footnote D's text.

But careful: what if there are more footnotes after D on the page? E.g., page has footnotes 5, 6(displaced), 7, 8. Block: "5", blank, "text5.", "text6", "7 text7", "8 text8". Parsing: opener "5" → footnote 5. Lines: blank (skip), "text5." ends with full stop → footnote 5 done. Then "text6" — not a numbered opener, and page has displaced D=6 → footnote 6 = lines until next numbered line ("7 text7"). Then "7 text7" opens footnote 7, etc. 

But the rule says "the first footnote ... ends at its first line that ends with a full stop". What if footnote 5's text is multiple lines and only the last ends with a full stop? Then lines up to and including that line are footnote 5. Fine — implement: when parsing block on a page with displaced D, for the first footnote, consume lines until one ends with "." (inclusive); then if the next lines are non-numbered, they form footnote D until next numbered opener.

Hmm, but actually a simpler general approach: parse block lines sequentially. State: current footnote. For each line:
- If line is bare number or starts with number+space → new footnote with that number (if number != expected, still opens — "never add a numbered line to the footnote before it").
- Else → append to current footnote.
- Special: if page has displaced D and current footnote is the first one and we haven't yet terminated it: if line ends with "." → mark first footnote terminated; the following non-numbered lines become footnote D.

Wait, but the displaced-number footnote is the second on the page, and the first footnote is one line ending with a full stop. So: after first footnote's line ends with ".", the next line(s) that don't open a numbered footnote belong to D. But how do we know they belong to D and not to footnote 5? Because footnote 5 already ended (line ended with full stop) AND the page has a displaced number D. So rule: on a page with displaced D, once the first footnote has a line ending with ".", subsequent non-opener lines start footnote D (until next opener).

Hmm, but what if the first footnote's text legitimately has multiple lines and the first line ends with a full stop mid-text? Spec says in all 12 cases the first footnote is one line ending with a full stop, so fine.

Also: "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page." So after processing a page, nextFootnote = max(highest number seen in block, displaced D if any) + 1.

Also the cover's asterisked note "* Adopted by the Committee…" is kept as footnote "*" and not counted. On page 1, block starts at "* " line. So footnote "*" with text "Adopted by the Committee…". Not counted in footnotes found (count only numbered ones 1..n). Actually reference.footnotes = 141, and the asterisk note is not one of them. So footnotes found = numbered footnotes only.

Wait, but on page 1, does the footnote block start with "* " or with "1"? Page 1 has the cover, then... The cover has the asterisk note at the bottom probably, then footnotes 1-4 maybe? Let me think: page 1 of E/C.12/GC/27: cover with title, "Distr.: General", "6 November 2025", "Original: English", committee name, title, then "I. Introduction", "1. A clean, healthy..." etc. Footnotes at foot of page 1: probably "* Adopted by..." then "1 ...", "2 ...", etc. The spec says block starts at first line that is bare number == nextFootnote (1), or starts with "1 ", or starts with "* " on first page. So on page 1, the first matching line — could be "* Adopted..." if it appears before footnote 1. The spec says "or starts with '* ' on the first page" — so "* " lines open the block on page 1. Then within the block, "* Adopted by the Committee..." — does "* " open a footnote? The footnote-text rule says "a line that starts with a number and a space, or a bare number on its own line, opens a footnote". "* ..." doesn't, so it would glue to... hmm, if "*" line is the block start but not a footnote opener, then it's before any footnote. I should treat "* " line on page 1 as footnote "*": keep it as footnote "*" and not counted. Let me handle: if line starts with "* ", it opens footnote "*".

Then footnote 1 on page 1: "1 ..." starts with "1 " and nextFootnote is 1. Good.

But wait — order on page 1: is "* Adopted..." before or after footnote 1? Typically the asterisk note is at the very foot, after footnotes? Actually in UN docs, the asterisk note "* Adopted by the Committee..." appears at the bottom of the first page, after the footnotes? Hmm, actually it usually appears right after the title on page 1 with the asterisk in the title, and the note at the foot of page 1, typically as the last footnote or first? In E/C.12/GC/27, the title has an asterisk: "General comment No. 27 (2025) on ... sustainable development*". The note "* Adopted by the Committee at its ... session" is at the foot of page 1. In many UN docs it's the first thing in the footnote area or the last. The spec says the block can start with "* " on the first page — implying the "*" line comes before footnote 1's opener? Or it could come after. Hmm. "the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space, or starts with '* ' on the first page". If "*" came after footnote 1, then the first matching line would be footnote 1's opener, and the block would start there, and "*" line would be inside the block — then "* Adopted..." doesn't start with a number, so it'd glue to the last footnote on page 1. That would be wrong. So presumably in this data the "*" line comes first in the footnote area (before "1 ..."). Actually in real UN documents, the asterisk note typically appears at the very end of page 1's footnotes... Hmm, no — actually in ECOSOC documents, the asterisk footnote appears first in the footnote list? Let me recall: e.g., E/C.12/GC/27 page 1: footnotes at bottom: "* Adopted by the Committee at its seventy-third session..." Hmm I actually think it appears after the numbered footnotes in some docs and before in others. The spec explicitly includes "or starts with '* ' on the first page" as a block opener, which suggests the "*" line is the first line of the footnote area on page 1. I'll handle both: block start = first line matching (bare == nextFootnote) or (starts with nextFootnote+" ") or (page 1 and starts with "* "). And within block parsing, a line starting with "* " opens footnote "*".

Hmm wait, but there's a subtlety: if the "*" line is the block opener on page 1, then nextFootnote advancement: "Advance nextFootnote past the highest number seen in the block" — the "*" footnote has no number, doesn't affect. Fine.

But actually, could the "*" line appear after some numbered footnotes on page 1? Then block starts at footnote 1's opener, and "*" line inside block would glue to the last footnote. To be safe, I'll also treat "* " lines inside the block as opening footnote "*". That handles both orders. But then the block-start detection: if "*" comes after footnote 1 on page 1, block starts at "1 ..." anyway. If "*" comes first, block starts at "*". Either way fine. But careful: what if a body line starts with "* "? Unlikely.

Hmm, wait — actually there's another subtlety: the block-start rule searches for the FIRST line matching the opener conditions. On page 1, body includes "1." paragraph start — "1." is not bare "1" and doesn't start with "1 " (it's "1."), so no match. Good. But what about a body line like "6 November 2025"? starts with "6 " — if nextFootnote were 6 at that point... on page 1 nextFootnote is 1, so no. But on later pages, could a body line start with "N " where N == nextFootnote? E.g., page 5, nextFootnote might be 30, and a body line "30 days..."? Possible in theory. The spec's rule would misfire, but the spec says this works for this data ("If no line on a page opens nextFootnote..." implies usually one does). Hmm, but actually the risk: the block starts at the FIRST line matching, which could be a body line before the real footnote block. The spec acknowledges this rule as given; I'll follow it but maybe add a guard: prefer the LAST... no, follow the spec. Actually wait — let me reconsider. The spec says "the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space". Hmm, for safety I could search from the end? No — footnotes are at the foot, so the first matching line from the top could be a false positive in body. But given the data description says this works, and the "6 November 2025" example is explicitly called out as not being a footnote "because the counter is at 1 when it is met" — implying the rule is first-match-from-top and the counter saves us. I'll implement first-match-from-top as specified.

Hmm, actually wait. Let me reconsider: maybe safer to find the last occurrence? No — spec is explicit: "the block starts at the first line that...". Follow it.

But one more guard: "or starts with '* ' on the first page" — only page 1.

Also: "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump; one missed number must never stop the count on the pages that follow." So if no exact opener, find first bare number > nextFootnote (before footer — but we already removed footer, so within remaining lines) and start block there, log "footnote number jump" (a repair? The kinds list doesn't include it... the repair kinds are: header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed. Hmm, "footnote block removed" — that's when the footnote block is separated from body, logged per page? "each step logs what it removed or changed". So removing the footnote block from the body is logged as "footnote block removed" per page. And the jump is logged... maybe as part of checks or as a repair of kind... The spec lists 8 kinds. The jump could be logged as a warning in the check panel rather than a repair. I'll log it as a repair with kind "footnote number jump" — hmm, but spec says "The kinds are the ones named in the next section" — the 8 kinds. Let me re-read: "a table of every change the script made, in document order, Page | Paragraph or footnote | What was done | Before | After, with a count per kind above it. The kinds are the ones named in the next section: header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed."

So exactly these 8 kinds. The jump log — I'll put it in the check panel as a note, or as a repair with kind... hmm. Maybe log the jump as a repair of kind "footnote number restored"? No. I'll add it to the check panel as an informational line, and maybe also as a repair row with kind "footnote block removed" (since the block start moved)? Actually the jump means the block starts at a bare number > nextFootnote; the lines between... hmm. Let me just log the jump in the check panel ("Footnote numbering: page n starts at footnote k, expected m — jump logged") and not as a repair row. Or include it as a repair with kind "footnote block removed" and description "block starts at footnote k (expected m)". Hmm, the "What was done" column is free text, so I can describe the jump there while kind stays "footnote block removed". That works.

Wait, also "footnote block removed" — per page where a footnote block was found and removed from body. Log one repair per page: Page | — | footnote block removed | before: first line of block | after: (removed). Hmm, "Before | After" columns. For removals, Before = the removed content (truncated), After = "removed" or empty. I'll design: Before = snippet of removed line(s), After = what it became (e.g., "" or "—"). Let me make Before/After meaningful per kind:

- header line removed: Before = symbol line, After = "removed".
- footer line removed: Before = the footer line, After = "removed". Maybe one row per footer line, or one per page summarizing? "a table of every change the script made, in document order" — every change. Footer has multiple lines per page (page number, GE code, maybe displaced number). That could be ~40+ rows. That's fine, but maybe group per page: one row per page listing footer lines removed. Hmm, "every change" — I'll do one row per removed line for header/footer? That's a lot but honest. Actually, let me do one row per page for footer with Before = joined footer lines, After = "removed". Hmm, but displaced footnote number is kept aside, not removed — it's "footer line removed" but the number is restored later as "footnote number restored". OK.

Let me decide: repairs logged:
1. Per page: header line removed (Before: the line, After: "removed").
2. Per page: footer lines removed (one row per page; Before: the footer lines joined with " / ", After: "removed" — and if displaced number, note "number D kept aside"). Actually maybe one row per footer line is cleaner for "every change". 20 pages × ~2-3 lines = ~50 rows. Plus 12 displaced. Plus 90-ish paragraph splits (2), joins (19), headings (23 unlabelled + labelled joins), footnote blocks (20), footnote restorations (12). Total maybe ~120 rows. That's fine for a table.

Hmm, but "footer line removed" per line: page number line, "GE.25-15926", date stamp, displaced number. I'll log each line as its own repair row. Actually that inflates the log with boring rows. Alternative: one row per page: "footer removed (3 lines: '2', 'GE.25-15926', '6')". The spec says "a table of every change the script made" — a page-level footer removal is one change arguably. I'll do one row per page for the footer, with Before listing the lines. And one row per page for header. That keeps the log readable. Hmm, but "every change"... I think per-page grouping for header/footer is reasonable and I'll say "n lines" in the What column. Actually, let me do per-line for header (1 line) and per-page for footer. Fine.

3. "number and text split": for paragraphs 23 and 87 where number and text share a line. Before: "23. The Committee..." After: "23." + "The Committee..." (split into number line + text line).
4. "paragraph joined across a page break": when a paragraph's lines span two pages. Before: "...end of page n" / After: "...start of page n+1 joined". Log once per paragraph.
5. "heading separated": unlabelled heading line separated from the following paragraph. Before: heading glued? Actually Before = the line as it appeared (it was its own line already, but would have been glued to previous paragraph by naive split). Hmm — the heading is on its own line before the paragraph number. A naive split on paragraph numbers would glue it to the previous paragraph. So the repair: Before: "Right to work (art. 6)" (would join previous paragraph), After: "kept as heading". 
6. "heading title joined": lettered subsection title wrapping over two lines — joined into one heading line. Before: two lines, After: joined line.
7. "footnote number restored": displaced number D from footer restored to footnote. Before: footnote text without number (first line), After: "D " + text.
8. "footnote block removed": per page, the footnote block removed from body. Before: first line of block, After: "moved to footnotes".

Also "paragraph joined across a page break" — logged when paragraph's lines carry two page numbers.

Now the body parsing:

After removing header, footer, footnote block from each page, concatenate body lines in page order, each tagged with page. Lines before the first paragraph start are the cover.

Paragraph starts: line matching `/^(\d{1,3})\.$/` (number alone) or `/^(\d{1,3})\. (.+)$/` (number + text). For the second form, split: number line + text line (log "number and text split").

Headings:
- Labelled: line matching `/^([IVX]+|[A-Z])\.$/`. Then skip blank lines, then every line up to the next label line or paragraph start is heading text. A line starting with lowercase or "(" continues the previous heading line (join, log "heading title joined from two lines"); any other line is a further heading line.

Hmm, let me parse this: after a label line like "A.", skip blanks, then collect lines until next label line (`/^([IVX]+|[A-Z])\.$/`) or paragraph start (`/^(\d{1,3})\./`). Among those lines: if a line starts with lowercase letter or "(", it continues the previous heading line (join with space, log). Otherwise it's a heading line on its own. So "A." + "Right to work (art. 6)" — wait, that's an unlabelled heading example. Labelled example: "A." then "Non-discrimination" then maybe "(art. 2)" on next line starting with "(" → joined: "Non-discrimination (art. 2)".

Hmm wait, but the unlabelled heading rule: "a non-empty line immediately followed by a paragraph-start line, at most 90 characters, starting with a capital letter and not ending with a full stop, semicolon, colon, comma or digit". So "Right to work (art. 6)" is immediately followed by "12." → unlabelled heading.

But careful: a labelled heading's title lines are followed by... the next label or paragraph start. E.g. "IV." blank "Labour rights" then "A." ... hmm. Or "I." blank "Introduction" then "1." — "Introduction" is immediately followed by paragraph start "1."! Would the unlabelled rule also catch "Introduction"? It's part of labelled heading "I." though. Order of rules: labelled heading parsing consumes lines up to next label/paragraph start, so "Introduction" is consumed as heading text of "I.". Then the unlabelled rule applies to remaining lines. So I need to process sequentially: walk lines; when I hit a label line, consume the heading block; when I hit a paragraph start, check if the previous non-empty line qualifies as unlabelled heading.

Let me structure the body walk:

```
lines = body lines (non-empty? keep blanks for structure but drop them for paragraphs)
```

Actually spec: "Every other non-empty body line belongs to the current paragraph; blank lines are dropped." And headings: "skip blank lines" after label. Let me write a state machine over all body lines (including blanks, tagged with page):

State: current context = cover | heading-collect | paragraph.

Algorithm:
- i = 0; cover lines = lines before first paragraph start.
- Actually simpler: iterate lines; maintain `currentParagraph` (null until first start), `currentHeading` (last heading line), `part` (last roman heading).

For each line index i:
- If line matches paragraph start (either form): 
  - Before treating it as paragraph start, check if previous non-empty body line (i-1 skipping blanks) is an unlabelled heading candidate: non-empty, length ≤ 90, starts with capital, doesn't end with . ; : , or digit, and is not itself a label line or already consumed as heading. If so, mark it as heading (log "heading separated"), set section = that line.
  - Start new paragraph with number.
- Else if line matches label `/^([IVX]+|[A-Z])\.$/`: enter heading mode: the label line itself is a heading line; then consume following lines: skip blanks; while next lines are not label and not paragraph start: if line starts with lowercase or "(" → append to previous heading line (log join); else → new heading line. Set section = last heading line; if label is roman (IVX), set part = label + " " + title? Hmm.

Wait — "Each paragraph's section is the most recent heading line before it and part the most recent roman-numbered heading". So `part` = most recent roman-numbered heading (e.g., "IV. Labour rights" or just "IV."?). The expanded paragraph shows "the full path ('IV. … › Right to work (art. 6)')". So part could be "IV. <title>" and section "Right to work (art. 6)". Full path = part + " › " + section. I'll store part as the roman label + its title (e.g., "IV. Labour rights"), section as the most recent heading line (labelled subsection title or unlabelled heading). Hmm, "section is the most recent heading line" — a heading line could be "A." itself? Or the title after "A."? I think heading lines include both the label and its title lines. The "most recent heading line" — for display, probably the title. Let me store headings as a list of {label, title, line} where line = full text like "A. Non-discrimination" or just "Right to work (art. 6)". Then section = the full line of the most recent heading; part = full line of most recent roman heading. Full path: part › section (if different).

Hmm, let me simplify: maintain `headingStack` — actually just `lastHeading` (string) and `lastRoman` (string). When a labelled heading is parsed: label line "IV." → heading entry; title lines appended. The heading's display line = label + " " + joined title (e.g., "IV. Introduction")? But spec says "Roman-numbered sections ('I.', a blank line, 'Introduction')" — so "I." on one line, blank, "Introduction" on next. The heading line for section purposes: "the most recent heading line". Hmm. For the full path "IV. … › Right to work (art. 6)", part = "IV. …" (roman heading with its title), section = "Right to work (art. 6)".

I'll build heading entries: when label line found, create heading {label: "IV.", title: collected title lines joined}. Display = label + " " + title (if title) else label. lastHeading = display of the most recent heading (including unlabelled ones). lastRoman = display of most recent heading whose label is roman.

For unlabelled heading: display = the line itself.

- Else (non-empty, not paragraph start, not label): if we're inside a heading collection (i.e., the previous line was a label or heading line and no paragraph has started since), treat per heading rules. Otherwise, it belongs to the current paragraph (or cover if no paragraph yet).

Hmm, the tricky part: distinguishing "heading title lines" from paragraph lines. The labelled-heading rule: after a label line, "every line up to the next label line or paragraph start is heading text". So once a label line is seen, all subsequent lines until next label/paragraph-start are heading text (with the lowercase/"(" continuation rule). So the state machine:

```
mode = 'cover'
for each line:
  if paragraphStart(line): 
     (check unlabelled heading on previous line)
     mode = 'paragraph'; start new paragraph
  elif labelLine(line):
     mode = 'heading'; start new heading entry
  else:
     if mode == 'heading':
        if line starts with lowercase or '(': append to last heading title (log join if it was a separate line)
        else: add as new title line of current heading
        (blank lines skipped)
     elif mode == 'paragraph':
        append to current paragraph
     else: # cover
        append to cover
```

Wait but there's an issue: after a heading's title lines, the next thing is a paragraph start. But what if after heading title there are more lines that are actually... no, per spec, everything up to next label/paragraph start is heading text. OK.

But the unlabelled heading: "a non-empty line immediately followed by a paragraph-start line". In my state machine, when I hit a paragraph start, I look back at the previous non-empty line: if mode == 'paragraph' and that line is the last line of the current paragraph and it qualifies (≤90 chars, capital start, not ending with . ; : , or digit) → it's actually an unlabelled heading, remove it from the paragraph, log "heading separated", set as lastHeading. That matches "a naive split glues them to the previous paragraph".

Hmm wait, but also: what if the previous line is the last line of a heading title? E.g., labelled heading "A." + "Non-discrimination" then paragraph "5." — "Non-discrimination" is immediately followed by "5." and would qualify as unlabelled heading, but it's already consumed as heading title (mode == 'heading' at that point). So the look-back should only apply when mode == 'paragraph'. Good.

Also the cover: lines before first paragraph start. Cover includes title lines, "Distr.: General", "6 November 2025", etc. The "6 November 2025" line — in body (before footnote block removal? wait, is "6 November 2025" before the footnote block on page 1? Yes, it's on the cover, above the footnotes). And the footnote block detection: first line matching bare==1 or starts with "1 " or (page 1) "* ". "6 November 2025" starts with "6 " — nextFootnote is 1, so no match. Good. But wait — what about "1." paragraph start on page 1? "1." — bare number equal to 1? The line is "1." not "1". My bare-number check: line matches `/^\d{1,3}$/`. "1." doesn't match. starts with "1 "? "1. A clean..." — starts with "1." not "1 ". Good.

Hmm, but wait: what about paragraph lines like "10. The Committee..." — starts with "10 " ? No — "10." — char after "10" is ".". Good. But a paragraph line (continuation) could start with a number+space, e.g., "2030 was..." — if nextFootnote == 20... "2030 was" starts with "20" followed by "3", not space. OK. But "20 days later..." as a continuation line while nextFootnote==20 would falsely open the block. Risk accepted per spec.

Hmm, actually wait — there's a subtle issue with the block-start rule and pages where the first footnote's number was displaced. E.g., page 2: footnotes 5 and 6, where 6 is displaced. Block opener: bare "5" == nextFootnote (5). Good. But what if a page's FIRST footnote is the displaced one? Spec says in all 12 cases the displaced one is the second on the page. OK.

Another subtlety: "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page." So nextFootnote = max(all numbers seen in block openers, displaced D) + 1. But what if the block contains numbers not in sequence (e.g., page has footnotes 5,6,7 — openers 5, 7, and 6 displaced)? Highest = 7, displaced 6 → next = 8. Good.

But hmm — what if a page's footnote block contains a number LOWER than nextFootnote? E.g., weird. "Any line that starts with a number and a space opens a footnote, even when the number is not the one expected". So we accept it. For nextFootnote advancement, take max.

Also the jump rule: "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump". So: search lines (after header/footer removal) for first line that is bare number == nextFootnote, or starts with nextFootnote+" ", or (page 1) starts with "* ". If none, search for first bare number > nextFootnote; if found, block starts there, log jump; nextFootnote advances past highest seen. If none at all, page is all body, check panel notes it.

Wait, careful: "starts with that number and a space" — should I also accept "starts with that number and a non-digit"? E.g., footnote "7 E/2003/22" — "7" + space. What about "7.E/..."? Unlikely. Keep space.

Hmm, one more: the block-start search — should it search only in the latter part of the page? The spec says first line in the page (after header/footer removal). But consider page 1: cover lines include "6 November 2025" — starts with "6 ", nextFootnote=1, no match. But what if cover had "1 something"? Not here. OK.

But actually, hmm, wait: there's a real risk on page 1: the title lines... "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development*" — starts with "General", fine. OK.

Now, footnote block parsing within a page:

```
blockLines = lines from blockStart to end (footer already removed)
displaced = page's displaced number D (or null)
footnotes on page = []
current = null
firstFootnoteDone = false  (for displaced handling)
for each line in blockLines:
  if line starts with "* " → open footnote "*" (text = rest), current = *
  elif line matches /^(\d{1,3})$/ → open footnote with number = int(line), text = ""
  elif line matches /^(\d{1,3}) (.+)$/ → open footnote number, text = rest
  else:
    if current == null: skip (or treat as part of nothing)
    else: append line to current.text
    special displaced handling: if displaced != null and current is the first footnote on the page and not yet terminated and line ends with "." → mark first footnote terminated; then subsequent non-opener lines go to footnote D.
```

Hmm, let me restructure the displaced handling: "On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D, marked repaired."

So: when page has displaced D:
- Parse first footnote normally (opener bare number N, then lines). The first footnote ends at its first line ending with "." (inclusive). 
- After that, lines that don't open a numbered footnote belong to footnote D (until next numbered opener).

Implementation: track `firstFnClosed = false`. When processing a non-opener line: if displaced && current is first footnote && !firstFnClosed: append to current; if line ends with "." → firstFnClosed = true. Else if displaced && firstFnClosed && current is first footnote (i.e., we're right after closure and haven't opened D yet): open footnote D with this line, mark repaired. Hmm, but what if there are blank lines between? Blank lines in block — skip blanks? The block may have blank lines between footnotes. Let me skip blank lines within the block (or keep them as separators but not text). Actually footnote text joined with space; blank lines dropped.

Wait, but the first footnote on page 2: "5", blank, "A/79/270, paras. 84 and 85." — the blank line after "5". If I skip blanks, then "A/79/270..." appends to footnote 5, ends with "." → closed. Then "A/42/427, p. 24." — non-opener, firstFnClosed, displaced=6 → open footnote 6, text = "A/42/427, p. 24.", repaired. Then next line "7 ..." opens footnote 7. 

But hold on — what if the first footnote's text is multiple lines and an intermediate line ends with "."? Spec says in all 12 cases it's one line. But to be safer: "ends at its first line that ends with a full stop" — that's the spec, implement as stated.

Hmm, wait — actually there's a subtlety: what if displaced D exists but the first footnote's text does NOT end with a full stop on any line before the next opener? Then... the rule says it ends at its first line ending with a full stop; if none, then it ends at the next opener, and then D would have no lines? Edge case; handle gracefully: if we hit an opener while current is first footnote and !firstFnClosed, then... the displaced footnote D has no text? Then maybe D's text is empty — mark repaired with empty text? Or the lines after the next opener...? Per spec this doesn't happen. I'll handle: if opener encountered and displaced && !firstFnClosed && current is first → close first footnote at previous line, and... hmm, then D gets nothing. I'll just log it. Actually, alternative interpretation: maybe D's lines come after the LAST footnote? No — spec is explicit: second on the page, right after the first. Fine.

Also: what if displaced D exists but the block's first footnote is not bare-numbered but "N text"? Spec says first is bare number + blank + text. I'll apply the rule regardless: first footnote in block ends at first line ending with ".".

Hmm, wait, actually one more consideration: what if a page has displaced D but the first footnote in the block is opened by "N text" (number+space on same line)? Then the "first line ending with full stop" would be that same line if it ends with ".". Then subsequent lines → D. OK, my implementation handles since I check line ends with "." after appending.

Let me now also handle: "Any line that starts with a number and a space opens a footnote, even when the number is not the one expected: never add a numbered line to the footnote before it." So in block parsing, any `/^(\d{1,3}) /` line opens a new footnote. But careful: footnote text continuation lines could start with a number+space? E.g., "2024 report..." as continuation of footnote 15? The rule says never — a numbered line always opens. Per spec, follow it. Hmm, but that could break footnotes whose text wraps and the next line starts with a year like "2025". Risk accepted per spec ("Any line that starts with a number and a space opens a footnote, even when the number is not the one expected").

Hmm wait, actually, that seems risky. Let me re-read: "Inside each page's footnote block, a line that starts with a number and a space, or a bare number on its own line, opens a footnote; the lines up to the next opener are its text, joined with a space. Any line that starts with a number and a space opens a footnote, even when the number is not the one expected: never add a numbered line to the footnote before it."

OK so yes, any "N ..." line opens. But then "the numbers run from 1 to that count without a gap or a duplicate" check — if a continuation line "2025 ..." opened a footnote, we'd get a duplicate/out-of-range number and the check would fail. The spec says the check verifies this. So presumably in this data, continuation lines don't start with number+space. Follow the spec.

Hmm, but wait — what about the displaced case: "A/42/427, p. 24." starts with "A", not a number. Good.

Now footnote marks in paragraph text: "Walk through each paragraph's text in document order with a counter that starts at 1. Every run of one to three digits not touching another digit, a slash, a dash or an opening parenthesis is a candidate; a candidate equal to the counter is a mark and the counter goes up by one; any other number is left alone. Each mark becomes [n], the character before it kept."

So regex over the joined text: find runs of 1-3 digits `/\d{1,3}/g` with boundaries: not preceded/followed by digit, slash, dash, or opening parenthesis. "not touching another digit, a slash, a dash or an opening parenthesis" — so the char before the run must not be [0-9/-(] and char after must not be [0-9/-(]. Hmm, "an opening parenthesis" — only before? "not touching another digit, a slash, a dash or an opening parenthesis" — I'll check both sides for digit, slash, dash; and opening parenthesis... Let me think: "article 11" — the "11" is preceded by space, followed by end/space. It's a candidate but not equal to counter (unless counter is 11 at that point — the sequential rule handles it: if counter happens to be 11 when we hit "article 11", it would be wrongly bracketed! But the spec says "only a sequential rule tells them apart" and the check lists rejected numbers so the reader can see "article 11" was not bracketed. So presumably the data works out — the counter passes 11 at a real mark before any "article 11" appears, or "article 11" appears when counter ≠ 11.)

Wait, hmm, that's fragile but it's the spec. Let me implement exactly: walk matches of `/\d{1,3}/g` in order; for each, check boundaries (prev char and next char not in [0-9], '/', '-', '(' — hmm, should ')' also be excluded? Spec says "another digit, a slash, a dash or an opening parenthesis". So excluded chars: digit, '/', '-', '('. I'll check prev and next chars against /[\d\/\-(\)]/? No — spec says opening parenthesis only. Let me use: prev not matching /[\d\/\-(\)]/... hmm. Let me just do: the run must not be adjacent to a digit, '/', '-', or '('. I'll check both prev and next char: if either is a digit, '/', '-', or '(' → not a candidate. Hmm, but what about ')' after? E.g., "(see para 5)" — "5" preceded by space, followed by ")". Is that a mark? In UN text, footnote marks often appear as "text (see para. 5)6"? Hmm. The spec says only opening parenthesis blocks. So "5)" would be a candidate. If counter == 5 there, it'd be bracketed. Follow spec exactly: blocked chars = digit, slash, dash, opening paren. Check on both sides? "not touching another digit, a slash, a dash or an opening parenthesis" — touching = adjacent on either side. I'll check both sides for all four char types. Hmm, but a closing paren after a mark... e.g., "waste.2)" — weird. Follow spec: only '(' blocks.

Wait, actually, hmm: "an opening parenthesis" — why would '(' block? Because footnote marks in UN PDFs sometimes appear as superscript after a parenthesis? Or because "(art. 11)" — the "11" is preceded by space... hmm, "art. 11)" — "11" followed by ")". Not blocked by my rule. But "(11)" — "11" preceded by "(" → blocked. OK that's the point: parenthetical numbers like "(2025)" or "(art. 11)" — wait "(art. 11)" has "11" preceded by space. Hmm. Whatever — implement as spec: candidate = run of 1-3 digits where prev char and next char are not in {digit, '/', '-', '('}.

Hmm, wait: should I also block when prev is a letter? "waste.2" — "2" preceded by "." — that's a mark (glued to word before). So letters/dots before are fine (marks glue to words). OK.

Then: candidate equal to counter → mark, counter++. Else → leave alone (log as rejected with context for the check panel).

Each mark becomes "[n]" replacing the digits, keeping surrounding chars: "waste.[2]", "equity,[17] common", "”. [3]"? Spec: "after a space ('”. 3')" → "”. [3]"? Hmm — "Each mark becomes [n], the character before it kept ('waste.[2]', 'equity,[17] common')". So "”. 3" → "”. [3]"? The space before is kept: "”. [3]". Yes, just replace the digit run with "[n]".

Wait, but careful: the counter walks "each paragraph's text in document order" — one counter across all paragraphs (starts at 1, continues). Yes: "Walk through each paragraph's text in document order with a counter that starts at 1."

But note: the marks are found in the joined paragraph text. But the check "Footnote marks: marks found in the paragraphs, expected to run from 1 to reference.footnotes without a gap" — so marks found should be 1..141. And footnotes found should also be 1..141. 

Hmm wait, but there's an ordering issue: footnote marks in text are sequential 1..141 in document order, and footnotes at page feet are also 1..141 in order. Good.

But wait — the cover's asterisk note: does the title have an asterisk mark? "sustainable development*" — the "*" is not a digit, so not a mark. Good.

First words: `first_words_found` = first six whitespace-separated words of joined text, footnote marks removed first. So remove `[n]` patterns (the bracketed marks) from text before extracting words? "footnote marks removed first" — remove the marks (the digits) — i.e., from text_raw, remove mark digits? Or from the bracketed text remove "[n]"? I think: take the joined text, remove the footnote marks (the digit runs that were identified as marks), then take first six words. Equivalent: take text with marks as [n], remove /\[\d+\]/, then split. Hmm, but "waste.[2]" → removing "[2]" gives "waste." — good. "equity,[17] common" → "equity, common" — hmm, that leaves double space? "equity, common" — the space after the mark remains: "equity, common" — words: "equity," "common". Whereas original "equity,17 common" → removing "17" gives "equity, common". Same. OK: first_words_found = first 6 words of text_with_marks.replace(/\[\d{1,3}\]/g, '') — wait, but that would also remove real bracketed numbers if any... there are none presumably. Alternatively remove the raw digit runs. I'll compute from the marked text by removing the bracketed marks, then normalize whitespace, split, take 6, join with space.

Hmm, actually simpler: during mark detection, I know which digit runs were marks. I can build `text_clean` = text with mark runs removed (replaced with ''), then first words from that. But the spec says marks become [n] in `text`, and `text_raw` keeps unmodified. For first words: "the first six whitespace-separated words of the joined text, footnote marks removed first". I'll remove the [n] from the marked text: `text.replace(/\[\d+\]/g,'')` then collapse spaces. Equivalent enough.

Normalisation for comparison: curly quotes → straight, en/em dashes → hyphen, whitespace runs → single space. Case kept.

reference.first_words keyed by paragraph number as string: `reference.first_words[String(n)]`.

Now checks (tab 04), each one line:
1. Paragraph count: found vs reference.paragraphs.
2. Numbering: numbers exactly 1..n in order; gaps/duplicates listed by number and page.
3. First words: count of mismatches, each listed "para. n: found … / reference …".
4. Footnotes: found vs reference.footnotes; numbers run 1..count without gap/duplicate; restored numbers listed with page.
5. Footnote marks: marks found 1..reference.footnotes without gap; missing numbers listed; rejected numbers listed with context.
6. Footnotes stay out of paragraphs: first 40 chars of every footnote-opener line (including number) searched in raw paragraph text (before marks) — expected 0 hits; paragraphs over 300 words listed (longest real 254).
7. Headers and footers: pages whose first line was symbol (expected all); pages with page number in footer (expected all but first); displaced numbers listed with page.
8. Headings: count of labelled and unlabelled; list of unlabelled ones.
9. Nothing lost: every non-empty line classified exactly once; counts per kind sum to total non-empty lines; unclassified lines listed with page, shown red in raw viewer.

Check status: pass (green) / fail (red) / "not run" if reference missing.

Header shows "n of m checks pass" with green/red dot; red dot on tab 04 when failures.

Now the raw page viewer (tab 04, closed heading "Raw pages"): select "Show raw page n" + monospaced panel with line numbers, each line coloured by classification (cover, header, heading, paragraph, footnote, footer), with legend. Six pale tints + letter codes (C, H, D?, ...). Let me assign: cover=C, header=H, heading=D (or "T" for title?), paragraph=P, footnote=F, footer=X? Let me use: COVER=C, HEADER=H, HEADING=T, PARAGRAPH=P, FOOTNOTE=F, FOOTER=R? Hmm, letters: C, H, T, P, F, R. Or simpler: cover "c", header "h", heading "t", paragraph "p", footnote "f", footer "x". I'll use uppercase single letters: C, H, T, P, F, X. Legend explains.

So I need per-line classification for every line of every page (including header/footer/footnote block lines). I'll classify during parsing: each original line gets a kind. Lines in the footnote block → footnote (except the block-start line? no, all footnote). Lines removed as header → header. Footer lines → footer. Body lines → cover/heading/paragraph. Blank lines → blank (unclassified but empty — "every non-empty line classified exactly once"). The "Nothing lost" check counts non-empty lines.

CSV export: columns `number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, footnotes_cited, repairs, citation, symbol, doc_url`. Wait, the plan earlier says `text_lines` is kept for the toggle and "the CSV column text_lines (lines separated by ' | ')" — but the column list doesn't include text_lines... Let me re-read: "**Paragraph text** = ... `text_lines` keeps the original lines for the toggle and the CSV column `text_lines` (lines separated by " | ")." And the download column list: "`number`, `section`, `part`, `page_start`, `page_end`, `first_words_reference`, `first_words_found`, `first_words_match`, `text`, `text_raw`, `footnotes_cited`, `repairs`, `citation`, `symbol`, `doc_url`". Hmm, text_lines mentioned but not in the list. I'll include text_lines too (it says it's a CSV column). Actually the list says "one row per paragraph with [columns]" — I'll include text_lines after text_raw to satisfy both mentions. Order: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, text_lines, footnotes_cited, repairs, citation, symbol, doc_url. Hmm, the explicit list doesn't have text_lines; but the earlier paragraph says it's a CSV column. Including it is safe.

CSV format: UTF-8 BOM, every field double-quoted, inner quotes doubled, CRLF line ends, Blob URL, filename from symbol with slashes → hyphens (e.g., "E-C.12-GC-27-paragraphs.csv"). I'll name it `${symbol.replace(/\//g,'-')}-paragraphs.csv`.

footnotes_cited: the footnote numbers cited in this paragraph (the marks found in it), e.g., "2; 3" or "2, 3". I'll join with "; ".

repairs: repairs that touched this paragraph — e.g., "number and text split; paragraph joined across a page break; heading separated". Join with "; ".

footnotes.csv on tab 03: columns? Spec just says "A download button, 'footnotes.csv', on this tab." I'll do number, page, text, repair, symbol, doc_url. Reasonable.

Copy citation button: copies "symbol, para. n" via navigator.clipboard (with fallback textarea+execCommand since sandbox may not have clipboard API? navigator.clipboard requires secure context; file:// might work? I'll try clipboard API, fallback to execCommand). Show "Copied" for 2 seconds.

Tabs: role="tablist", arrow-key navigation, buttons with role="tab", aria-selected, panels role="tabpanel". Hidden panels: use hidden attribute + CSS `[hidden]{display:none!important}`. "the tab panel of a hidden tab is not focusable" — hidden attribute handles that.

Left rail: "DOCUMENT" heading, card per document in WORKSHOP_DATA with records+reference. Today one (pdf_text) — but pdf_text_2 also has records and reference! Wait: "The app is written so that every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data; the selected card has a red left border and the tabs show that document. Today there is one." Hmm — but pdf_text_2 also has records and reference (18 pages of CCPR/C/GC/32 with reference 65 paragraphs, 128 footnotes). The preview says both exist. "Today there is one" — maybe in the participant's actual data only pdf_text is attached? The attached file message says "(Attached: CESCR General comment No. 27 (PDF) → WORKSHOP_DATA.pdf_text)". But WORKSHOP_DATA may still contain pdf_text_2... The instruction says "Build apps only on files attached in this conversation." The attached file is pdf_text. Hmm, but the plan says "every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data". If pdf_text_2 is present in WORKSHOP_DATA, it would get a card. But the rules say build only on attached files. The attachment maps to WORKSHOP_DATA.pdf_text. pdf_text_2 is described in the system prompt as available... but the user only attached pdf_text. To be safe: iterate over WORKSHOP_DATA keys, include those with records && reference — but should I include pdf_text_2 if present? The plan explicitly says "every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data; ... Today there is one." This suggests in the actual runtime, only pdf_text has records+reference... but the system prompt describes pdf_text_2 with reference too. Hmm. The safest: include all keys in WORKSHOP_DATA that have both `records` and `reference` — that follows the plan literally. If pdf_text_2 is there, it gets a card and works (the pipeline is generic). That's actually a nice demonstration. But "Build apps only on files attached in this conversation" — pdf_text_2 wasn't attached... but it's in WORKSHOP_DATA which is preloaded. The plan (from the user, who knows their data) says "Today there is one" — meaning in their data only one document has records+reference. But the system prompt says pdf_text_2 exists with reference. Contradiction? The system prompt describes "Data available in the preview" — the preview includes pdf_text_2. The user's plan says today there is one card. Maybe in the real workshop data, pdf_text_2 is present too and the plan statement is just about the preview... Ambiguous. 

Decision: write generic code that scans WORKSHOP_DATA for objects with `records` (array) and `reference` (object), in key order, and builds a card for each. If only pdf_text qualifies at runtime, one card. If pdf_text_2 also qualifies, two cards — and the app still works. This follows the plan's "written so that every document ... gets its own card". I think that's the intended behavior. But wait — "Build apps only on files attached in this conversation. If they ask for an app and have not attached a file..." — they attached pdf_text. pdf_text_2 is in the preloaded data though. Hmm. The plan says "every document in WORKSHOP_DATA with records and a reference" — I'll follow the plan; it's explicit about the rail behavior. Actually hold on, let me reconsider: maybe safer to only use attached... but I can't detect "attached" — the attachment note says pdf_text. The plan says scan WORKSHOP_DATA. I'll scan WORKSHOP_DATA for records+reference. If pdf_text_2 shows up, fine — it's real data in the sandbox, not invented. Actually hmm, but the rule "Build apps only on files attached in this conversation" is about not hallucinating data; pdf_text_2 is genuinely in WORKSHOP_DATA. The user's plan explicitly says to scan WORKSHOP_DATA. Go with scanning.

Wait, but actually — re-reading: "The app is written so that every document in `WORKSHOP_DATA` with `records` and a `reference` gets its own card in the rail, in the order of the data; the selected card has a red left border and the tabs show that document. Today there is one." — "Today there is one" strongly implies at runtime only one such key exists. But the preview shows two... The preview is "the data available in the preview" — maybe in the actual workshop, WORKSHOP_DATA has only pdf_text. Either way, generic scanning handles both. 

Hmm, one concern: pdf_text_2's reference — does it have first_words? The system prompt says pdf_text_2 has "its own reference (65 paragraphs, 128 footnotes)" — presumably same shape. My code handles missing fields gracefully ("no reference in this file" / "not run").

Now, the header: monospace label "UN DOCUMENT · PDF TEXT", serif title, one line: symbol linked to doc_url (new tab), "adopted reference.adopted", "n pages of raw converter text", source. One sentence under: what the page does. Right side: green/red dot + "n of m checks pass".

Wait — "n pages of raw converter text" — count is the string "20"; I'll compute records.length. And `source` — WORKSHOP_DATA.pdf_text.source. And `built`? The footer needs "built date" — pdf_text may not have `built`... The footer spec: "Source line, `built` date, and ...". pdf_text has title, symbol, doc_url, source, count, records, reference — no `built` mentioned. I'll show built if present, else omit or show "—". I'll handle: `doc.built ? ... : ''`. Hmm, footer always visible: "Source line, built date, and 'Counting, splitting...'". I'll include built only if present.

Rail card: symbol in monospace, short title (title is long — "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development" — I'll show full title in small text, or truncate? Show it, it's fine, maybe clamp). "adopted …", "n pages". Two big serif numbers: "n paragraphs" / "of reference.paragraphs" with thin bar showing share (red when short or over), "n footnotes" / "of reference.footnotes" with bar. Then "n of m checks pass" linking to tab 04.

Tab 01 RESULT: four tiles: Paragraphs found (n) vs document has (reference.paragraphs) — green when equal, red with difference; Footnotes found n of reference.footnotes; First words match n of reference.paragraphs; Repairs made n (link to repair log on tab 04 — clicking switches to tab 04 and opens the repair log). Each tile has "How this is computed" one-liner.

Tab 02 PARAGRAPHS: collapsible "Headings found: n" box above table. Table columns: No. | Section | Page | First line | Check. Rows are buttons with aria-expanded; clicking expands in place showing full text, "Show the PDF's lines" toggle, reference first words vs found, pages, repairs, Copy citation button. Footnote marks shown as [n] in table first-line, expanded text, and CSV. Note under table about `\[\d+\]` removal pattern.

Wait — the table has a "First line" column with first 120 chars cut at a word with "…". And Check column "OK" or "first words differ" (red). Section column between No. and Page.

Expanded row content: full text (verbatim, with [n] marks), toggle "Show the PDF's lines" revealing text with original line breaks and page markers, then comparison of first words, page(s), repairs touching this paragraph, Copy citation button.

Implementation of expandable rows: I'll render each paragraph as a `<tbody>`-less structure... Tables with expandable rows: use one `<table>` with rows, and after each row a hidden `<tr class="detail"><td colspan=5>...`. The row itself is a `<tr>` with a button? "Rows are buttons with aria-expanded" — I'll make the first cell contain a button, or make the whole row clickable via a button in the row. Simplest accessible approach: each paragraph row's first cell has a `<button aria-expanded>` spanning... Actually make the entire row a button is invalid HTML inside table? A `<tr>` can't be a button. I'll put a button in the No. cell (or make the row contain a button that covers the row via CSS). Common pattern: `<tr class="prow"><td colspan="5"><button aria-expanded="false" aria-controls="detail-n">…whole row content…</button></td></tr><tr class="detail" hidden>…</tr>`. But then the table columns wouldn't align. Alternative: row with cells, and the No. cell contains the button; clicking anywhere on row triggers via JS (row click handler) but the button provides keyboard access. I'll do: `<tr data-i>` with cells; first cell contains `<button class="rowbtn" aria-expanded aria-controls>`. Also add click handler on the row for convenience. The detail row follows, hidden.

Hmm, "Rows are buttons with aria-expanded" — I'll make the button wrap the number and maybe the first-line text? To keep table alignment, I'll keep cells but put the button in the first cell and also make the whole row clickable. Actually cleaner: make the entire row content inside a single button? That breaks the table layout (No. | Section | Page | First line | Check columns). Let me do: each `<tr>` has 5 `<td>`s; the first `<td>` contains the button with the number; the row has a click listener; the button has aria-expanded and aria-controls pointing to the detail row. Keyboard: Tab focuses the button, Enter/Space toggles. Good enough and accessible.

Tab 03 FOOTNOTES: table "Footnotes found: n of reference.footnotes" with caption; columns No. | Page | Text | Repair. Repair reads "number restored from the page foot" for restored ones. Expanded paragraph also lists footnotes it cites — that's in tab 02's expanded row ("footnotes_cited"). Also maybe footnote rows expandable to show full text? Spec: "The expanded paragraph also lists the footnotes it cites." So footnote table rows could be simple (text may be long — truncate? "Text" column — I'll show full text but it's a table cell; maybe clamp with expandable too. Keep simple: show text, allow wrap; maybe make rows expandable too? Spec doesn't ask. I'll show the text in the cell, possibly long — fine, or clamp to ~200 chars with title attr. Hmm, "Keep the full text of a paragraph available (click to expand)" — that's for paragraphs. For footnotes, I'll make rows expandable too for consistency? The spec for tab 03 doesn't mention expansion. Keep simple: full text in cell (footnotes are short-ish). Actually some footnotes could be long. I'll make them expandable rows as well — no wait, "where it says nothing, keep it simple". I'll show full text in the cell with wrapping. Fine.

Download "footnotes.csv" button on tab 03.

Tab 04 CHECKS & METHOD: check panel open (every check one line). Then closed heading "Repair log (n)" (button aria-expanded) — table Page | Paragraph or footnote | What was done | Before | After, with count per kind above it. Then closed heading "Raw pages" — select "Show raw page n" + monospaced panel with line numbers, coloured lines, legend. Then Download: "Download paragraphs as CSV" button.

Clicking "Repairs made: n" tile on tab 01 → switch to tab 04 and open repair log (and scroll to it).

Footer always visible.

Now — the "How this is computed" line near every chart/number. Tiles get one-liners.

Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Serif Georgia for title/big numbers/figure titles; monospace uppercase letter-spaced 11-12px for labels/tabs/figure numbers; sans 16px body. Green for pass: dark green like #1e6b3a (contrast on #f4f0e8: #1e6b3a vs #f4f0e8 — luminance... #1e6b3a is fairly dark, should be ≥4.5:1. Let me pick #1a6b3c or #17663a. I'll use #1e6b3a. Red #9b2335 for fail (contrast vs #f4f0e8: #9b2335 is dark red, fine).

Focus ring: visible red outline: `:focus-visible{outline:3px solid #9b2335; outline-offset:2px}`.

No horizontal scrolling on laptop: max-width container ~1100px, table font maybe 14-15px for tables? Body 16px. Tables can be 14px to fit. Hmm "the system sans-serif at 16px for body text and tables" — tables at 16px might overflow with 5 columns; I'll allow table wrapper overflow-x:auto as safety, but design to fit ~1000px. First line column can wrap. OK.

Charts: no charts needed here really (bars in rail are thin divs, not Chart.js). The plan mentions thin bars in rail — simple divs. No Chart.js needed. That's fine ("Use it for charts" — only if charts; we have none, just bars which are CSS).

Now let me think about the parsing implementation in detail.

```js
const DATA = window.WORKSHOP_DATA;
// find documents
const docs = [];
for (const key of Object.keys(DATA)) {
  const d = DATA[key];
  if (d && Array.isArray(d.records) && d.reference && typeof d.reference === 'object') docs.push({key, data: d});
}
```

Wait — uhri has records but no reference; gc has records no reference; hrc records no reference; library records no reference; wiki pages no records. pdf_text and pdf_text_2 have records+reference. Good filter: `Array.isArray(d.records) && d.records.length && d.reference && typeof d.reference==='object' && d.reference.paragraphs != null`? The plan: "every document in WORKSHOP_DATA with records and a reference". I'll check `d.records && d.reference`. But uhri etc. don't have reference. OK.

Hmm wait, but should I restrict to attached? The attachment is pdf_text. If pdf_text_2 is in WORKSHOP_DATA at runtime, it gets a card. The plan says "Today there is one" — trusting that. Generic scan it is.

Parse function:

```js
function parseDocument(doc) {
  const symbol = doc.symbol || '';
  const records = [...doc.records].sort((a,b)=>a.page-b.page);
  const ref = doc.reference || null;
  const repairs = [];   // {page, target, kind, before, after}
  const checks = [];    // filled later
  const pages = [];     // per-page info: {page, lines:[{raw, kind, page}], headerRemoved, footerLines:[], displaced, pageNumberFound, blockStart}
  let nextFootnote = 1;
  const footnotes = []; // {number (int or '*'), page, text, repaired, openerLine}
  const bodyLines = []; // {text, page, kind}
  
  for (const rec of records) {
    const page = rec.page;
    const rawLines = String(rec.text||'').split('\n');
    // classify each line
    const lines = rawLines.map(t => ({raw: t, page, kind: null}));
    // header: first non-empty line equals symbol
    let i = 0;
    while (i < lines.length && lines[i].raw.trim()==='') i++;
    if (i < lines.length && lines[i].raw.trim() === symbol) {
      lines[i].kind = 'header';
      repairs.push({page, target:'—', kind:'header line removed', before: lines[i].raw.trim(), after:'removed'});
      i++;
    } else {
      // warning
      pageWarnings.push(...)
    }
    // footer: from end
    let j = lines.length - 1;
    const footerLines = [];
    let displaced = null, pageNumFound = false;
    while (j >= i) {
      const t = lines[j].raw.trim();
      if (t === '') { lines[j].kind = 'blank'; j--; continue; }
      if (t.startsWith('GE.')) { footerLines.push(lines[j]); j--; continue; }
      if (/^(\d{6})(\s+\d{6})*$/.test(t)) { footerLines.push(lines[j]); j--; continue; } // date stamp 6-digit groups
      if (/^\d{1,3}$/.test(t)) {
        const n = parseInt(t,10);
        if (n === page) { pageNumFound = true; footerLines.push(lines[j]); j--; continue; }
        else { displaced = n; footerLines.push(lines[j]); j--; continue; }
      }
      break;
    }
    // mark footer lines kind='footer', log repair per page
    ...
    // remaining lines i..j are content
    // footnote block detection
    ...
  }
}
```

Wait, careful with the footer loop: "drop lines while the line is empty, starts with 'GE.', consists only of 6-digit groups, or is a bare number of one to three digits." So the loop continues while any of these match. A bare number equal to page → page number; any other bare number → displaced footnote number. Note: the loop drops ALL trailing bare numbers — e.g., footer "2\nGE.25-15926" — from end: "GE.25-15926" dropped, "2" dropped (page number). On 12 pages there's a third bare number (displaced). Order varies. Also page 1: "GE.25-15926 (E)" — starts with "GE." → dropped. Date stamp "051125 061125" → 6-digit groups → dropped. Page 1 has no bare page number (page number absent on page 1? "pages 2 to 20" have the page number alone; page 1 has GE code and date stamp instead). So page 1: pageNumFound = false — expected ("pages with a page number in the footer (expected all but the first)").

Hmm wait, careful: the date stamp regex — "consists only of 6-digit groups". "051125 061125" → two groups of 6 digits separated by space. Regex: `/^\d{6}(\s+\d{6})*$/`. Good.

But careful: a bare number of 1-3 digits — could a footnote block's last line be a bare number? The footnote block is before the footer; the footer loop stops at the first non-matching line from the end. Footnote text lines end with "." typically, so loop stops there. But what if the last footnote's text is a bare number? Unlikely. OK.

Also careful: the displaced number is "kept aside for that page" — and it's also removed from the page (it's in the footer). Log as footer line removed, and later "footnote number restored".

Edge: what if a bare number in the footer is neither page nor... it's displaced. But what if page number appears AND displaced? Both handled.

Hmm, one more: what if the footer loop encounters a bare number that equals page but there's also another bare number? E.g., footer "6\n2\nGE.25-15926" on page 2: from end: GE dropped, "2" → page number, "6" → displaced. Good.

Now footnote block detection on content lines (indices i..j after header/footer removal):

```js
const content = lines.slice(i, j+1); // each has raw, page
// find block start
let blockStart = -1;
for (let k = 0; k < content.length; k++) {
  const t = content[k].raw.trim();
  if (/^\d{1,3}$/.test(t) && parseInt(t,10) === nextFootnote) { blockStart = k; break; }
  if (t.startsWith(nextFootnote + ' ')) { blockStart = k; break; }
  if (page === firstPage && t.startsWith('* ')) { blockStart = k; break; }
}
if (blockStart === -1) {
  // jump: first bare number > nextFootnote
  for (let k = 0; k < content.length; k++) {
    const t = content[k].raw.trim();
    if (/^\d{1,3}$/.test(t) && parseInt(t,10) > nextFootnote) { blockStart = k; jump = parseInt(t,10); break; }
  }
}
```

Hmm wait — "starts with that number and a space": `t.startsWith(nextFootnote + ' ')`. But careful: if nextFootnote is 1 and a line is "1. A clean..." — starts with "1." not "1 ". Good. But what about "10 ..." when nextFootnote is 1? starts with "1"? "10 ..." starts with "1" followed by "0" — `startsWith("1 ")` is false since second char is "0" not space. Good.

But hmm — what about a line "1 " exactly? Edge. Fine.

Also the "* " check: only on the first page (page === records[0].page, i.e., first page of doc). Spec: "or starts with '* ' on the first page". I'll use `page === firstPageNumber`.

Wait, but there's a problem: on page 1, the block-start search checks conditions in order per line: for each line k, check all three conditions. The first line matching ANY condition wins. On page 1, if "* Adopted..." appears before footnote "1 ...", block starts at "*". If after, block starts at "1 ...". Either way OK since I handle "* " openers inside the block too.

Hmm, but actually — wait. What if on page 1, a cover line starts with "1 "? Like "1 November..."? Not in this doc. OK.

If blockStart found: body = content[0..blockStart-1], block = content[blockStart..end]. Log repair "footnote block removed" per page: Before = first line of block (trimmed, truncated), After = "moved to footnotes (n lines)". Mark block lines kind='footnote'.

If no blockStart: whole content is body; note "no footnote block on this page" for check panel.

Then parse block into footnotes:

```js
let cur = null;
let firstFn = null; // first footnote object on this page
let firstClosed = false;
const pageFns = [];
for (const ln of block) {
  const t = ln.raw.trim(); // hmm — should I trim? footnote text lines... keep raw but trim for matching
  if (t === '') continue; // skip blanks inside block? 
  ...
}
```

Hmm wait — blank lines inside the block: the first footnote on a page is "a bare number on its own line, a blank line, then the text". If I skip blanks, fine. But the displaced rule relies on "the first footnote ends at its first line that ends with a full stop" — blanks skipped don't matter.

But careful: should blank lines within footnote text be preserved as paragraph breaks? Spec says "the lines up to the next opener are its text, joined with a space" — blanks dropped (joining with space). OK skip blanks.

Opener detection:
```js
let m;
if (t.startsWith('* ')) { open footnote {number:'*', text: t.slice(2)} }
else if ((m = t.match(/^(\d{1,3})$/))) { open {number:+m[1], text:''} }
else if ((m = t.match(/^(\d{1,3}) (.+)$/))) { open {number:+m[1], text:m[2]} }
else {
  // continuation line
  if (displaced != null && firstFn && !firstClosed && cur === firstFn) {
    // shouldn't happen: continuation of first fn
    cur.text += ' ' + t;
    if (t.endsWith('.')) firstClosed = true;
  } else if (displaced != null && firstFn && firstClosed && cur === firstFn) {
    // open footnote D
    cur = {number: displaced, page, text: t, repaired: true, openerLine: ln};
    pageFns.push(cur); footnotes.push(cur);
    // log repair 'footnote number restored'
  } else if (cur) {
    cur.text += ' ' + t;
    if (cur === firstFn && displaced != null && t.endsWith('.')) firstClosed = true;
  }
}
```

Hmm, this is getting tangled. Let me restructure: handle the first-footnote-termination uniformly: when appending a continuation line to the first footnote on a page with displaced D, check if it ends with '.' → firstClosed = true. Then, on the NEXT continuation line (cur still === firstFn, firstClosed true, displaced != null) → open footnote D instead.

Wait but what if the first footnote's opener was "N text..." (number+space same line) and that line ends with '.'? Then firstClosed should be set at open time. Let me set: when opening the first footnote, if its initial text ends with '.', firstClosed = true. Then continuation lines: if displaced && firstFn && firstClosed && cur===firstFn → open D. Else append to cur (and if cur===firstFn && !firstClosed && line ends with '.' → firstClosed=true).

Hmm, but there's another subtlety: what if displaced != null but the first footnote is NOT the one before D? Spec says it always is. OK.

Also: what if displaced != null and firstClosed never becomes true (first fn text never ends with '.')? Then D never opens and its lines glue to first fn. The check "footnotes found vs reference" would then show a shortfall. Acceptable — but per data it won't happen.

Also the "*" footnote: number '*', not counted in numbered footnotes. When advancing nextFootnote, ignore '*'.

Advance: after processing page's block, `nextFootnote = max(nextFootnote, ...all numbers opened in block, displaced||0) + 1`. Wait — "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page." So nextFootnote = max(highestSeen, displaced) + 1. But careful: if the block had a jump (started at number > nextFootnote), highestSeen covers it.

Hmm, wait — but what if a page's block contains numbers but the page's first footnote is displaced... covered.

Also: what if blockStart found via exact opener but the block also contains lower numbers? Whatever, max handles.

Edge: page with no block at all → nextFootnote unchanged.

Now body lines: all content lines before blockStart, across pages, concatenated in page order, each tagged {text: raw (untrimmed? keep raw for display; for parsing use trimmed?), page, kind}. Hmm — for paragraph text joining, spec says "the paragraph's lines joined with a single space, double spaces collapsed, trimmed". So I can trim each line when joining. For the raw-lines toggle, keep original lines. I'll store both: `raw` (original) and use trimmed for logic.

Wait, but "Show the PDF's lines" reveals "the same text with the converter's line breaks and the page number where each page began". So the toggle shows the paragraph's original lines (with page markers). I'll store paragraph.lines = [{text: rawLine, page}].

Now walk body lines for cover/headings/paragraphs:

```js
const bodyAll = []; // {raw, page}
pages.forEach(p => p.bodyLines.forEach(l => bodyAll.push(l)));
```

Each body line gets kind assigned during the walk: 'cover' | 'heading' | 'paragraph'.

Walk:
```js
let mode = 'cover';
let cur = null; // current paragraph {number, lines:[], pageStart, pageEnd}
let curHeading = null; // {label, titleLines:[], display}
let lastHeading = '';   // display string of most recent heading
let lastRoman = '';     // display of most recent roman heading
const paragraphs = [];
const headings = []; // {display, labelled, page, line}
const coverLines = [];

for (let idx = 0; idx < bodyAll.length; idx++) {
  const ln = bodyAll[idx];
  const t = ln.raw.trim();
  if (t === '') continue; // blank dropped
  let m;
  if ((m = t.match(/^(\d{1,3})\.$/)) || (m = t.match(/^(\d{1,3})\. (.+)$/))) {
    // paragraph start
    const num = +m[1];
    let firstText = m[2] || '';
    if (m[2]) {
      // number and text on one line → split
      repairs.push({page: ln.page, target: 'para. '+num, kind:'number and text split', before: t, after: num+'.  →  '+firstText.slice(0,60)+'…'});
      // the text becomes a separate line
    }
    // check previous non-empty line for unlabelled heading
    const prev = previousNonEmpty(bodyAll, idx);
    if (mode === 'paragraph' && cur && prev && prev.lineObj && cur.lines[cur.lines.length-1] === prev.lineObj) {
      const pt = prev.text;
      if (pt.length <= 90 && /^[A-ZÀ-Þ]/.test(pt) && !/[.;:,0-9]$/.test(pt)) {
        // unlabelled heading: remove from paragraph
        cur.lines.pop();
        prev.lineObj.kind = 'heading';
        headings.push({display: pt, labelled:false, page: prev.lineObj.page});
        lastHeading = pt;
        repairs.push({page: prev.lineObj.page, target:'para. '+num, kind:'heading separated', before: pt + '  (would join para. ' + cur.number + ')', after: 'kept as heading'});
        // recompute pageEnd of cur
      }
    }
    cur = {number: num, lines: [], pageStart: ln.page, pageEnd: ln.page, section: lastHeading, part: lastRoman, firstLineSplit: !!m[2]};
    if (m[2]) cur.lines.push({text: firstText, page: ln.page, splitFromNumber: true});
    ln.kind = 'paragraph';
    paragraphs.push(cur);
    mode = 'paragraph';
  } else if ((m = t.match(/^([IVX]+|[A-Z])\.$/))) {
    // labelled heading
    mode = 'heading';
    curHeading = {label: m[1], titleLines: [], page: ln.page, lineObj: ln};
    ln.kind = 'heading';
    headings.push(curHeading);
    // display set after collecting title
  } else {
    // other line
    if (mode === 'heading') {
      if (/^[a-z(]/.test(t)) {
        // continuation of previous heading title line
        const prevH = curHeading.titleLines[curHeading.titleLines.length-1];
        ... join
        repairs.push({kind:'heading title joined from two lines', ...});
        curHeading.titleLines[last] = prevH + ' ' + t;
      } else {
        curHeading.titleLines.push(t);
      }
      ln.kind = 'heading';
    } else if (mode === 'paragraph' && cur) {
      cur.lines.push({text: t, page: ln.page});
      cur.pageEnd = ln.page;
      ln.kind = 'paragraph';
    } else {
      // cover
      ln.kind = 'cover';
      coverLines.push(ln);
    }
  }
}
```

Hmm wait, there's a problem with the labelled heading: after "IV." the title lines come, but the heading display should be "IV. Introduction". And `lastHeading`/`lastRoman` should update when? "Each paragraph's section is the most recent heading line before it and part the most recent roman-numbered heading". So when a paragraph starts, section = most recent heading line. The "heading line" for a labelled heading — is it "IV." or "IV. Introduction"? For the full path "IV. … › Right to work (art. 6)", part = "IV. …" (roman + title), section = "Right to work (art. 6)". So I'll compute heading display = label + (title ? ' ' + title.join(' ') : ''). Update lastHeading = display whenever a heading completes... but titles are collected as we go. Simplest: when a paragraph starts (or at end), set section from the current heading state. Let me maintain `lastHeadingDisplay` updated whenever a heading line is added: for labelled headings, display = label + ' ' + titleLines.join(' ') (recompute as titles are added). For unlabelled, display = the line.

But careful: the unlabelled heading look-back — the previous line might be a heading title line (mode==='heading'), in which case we don't treat it as unlabelled (mode check handles: only when mode==='paragraph').

Hmm, wait — there's an issue: after a labelled heading's title, the next paragraph start triggers the look-back at the previous non-empty line, which is the heading title (mode==='heading'), so no unlabelled detection. Good.

But another issue: the unlabelled heading look-back when mode==='paragraph': the previous non-empty line is the last line of the current paragraph. But what if the paragraph has only the split first line? E.g., "23. Text..." split into number + text; then next line is "24." — previous non-empty line is the split text line, which is part of para 23. If it qualifies as unlabelled heading (≤90 chars, capital, no terminal punctuation)... e.g., para 23's text is one line "The Committee considers..." ending with "." → doesn't qualify (ends with '.'). OK.

But hmm — what if the previous line is the paragraph's ONLY line and it's short without terminal punctuation? Could be misdetected. Per data, the 23 unlabelled headings are exactly the lines before paragraph starts. The rule as spec'd. But wait — there's a subtle bug: the look-back must only consider the line immediately before the paragraph-start line (skipping blanks). And it must be the last line of the current paragraph (i.e., cur.lines last element). If mode==='paragraph' and prev non-empty line is cur's last line — yes by construction. But what if mode==='paragraph' and the previous non-empty line belongs to... it must be cur's last line since all non-empty lines in paragraph mode go to cur. Unless the previous line was a heading? No — if it were, mode would be 'heading'. OK.

Hmm, but one more: what about the FIRST paragraph (para 1) — mode==='cover' before it, so no look-back; cover lines stay cover. But what if a cover line qualifies as unlabelled heading before para 1? E.g., "Introduction" after "I." — that's labelled heading mode. OK.

Wait, actually there's a subtle issue with mode==='heading' and paragraph starts: after heading "I. Introduction", next line "1." → paragraph start, mode was 'heading', look-back skipped (mode!=='paragraph'). Good. But `lastHeading` must be "I. Introduction" at that point — yes, updated when heading lines were added.

Hmm, but when do I update lastHeading for labelled headings? The label line "I." comes first, then blank, then "Introduction". When "I." is processed, display = "I." (no title yet). Then "Introduction" added → display = "I. Introduction". I'll recompute display after each heading line addition and set lastHeading = display; if label is roman (matches /^[IVX]+$/), lastRoman = display.

Wait — roman detection: `/^([IVX]+|[A-Z])\.$/` — [IVX]+ matches I, V, X, IV, IX, etc. But also matches... "X."? yes. Single [A-Z] matches any capital letter A-Z. So "A." is a lettered subsection. Roman = /^[IVX]+$/.

Hmm, but careful: could a paragraph-start-like line "X." be confused? "X." matches label regex. In this doc, sections are I., II., III., IV., V., VI. and subsections A., B., C. Fine.

Now, the heading title continuation rule: "a line starting with a lowercase letter or '(' continues the previous heading line (logged as 'heading title joined from two lines'), any other line is a further heading". So within heading mode, non-label non-paragraph lines: if starts with lowercase or '(' → join to previous title line; else → new title line. But what if it's the FIRST title line (no previous)? Then just push. Also — what if a heading has multiple separate title lines (not continuations)? "any other line is a further heading" — so titleLines can have multiple entries; display joins them with space? Hmm, "further heading" — maybe each is its own heading line. For display, join with ' '. I'll join all titleLines with ' ' for display. And the continuation join logs the repair.

Hmm wait, actually re-reading: "skip blank lines, then every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or '(' continues the previous heading line (logged as 'heading title joined from two lines'), any other line is a further heading." So heading text = possibly multiple lines; lowercase/"(" lines merge into the previous line. Display = label + ' ' + merged lines joined with ' '. OK as I planned.

Now — potential problem: heading mode consumes ALL lines until next label/paragraph start. What if a heading is followed by body text without a paragraph number? Per spec, doesn't happen (every body line after headings belongs to a paragraph). OK.

Another subtlety: the unlabelled heading check happens at paragraph start, looking at previous non-empty line. But what if that line was already classified as heading (mode==='heading')? Skipped. What if mode==='cover'? Skipped (cover). Good.

But wait — there's an ordering issue with the unlabelled heading and `section`: when para starts, section = lastHeading. If the previous line was just reclassified as unlabelled heading, lastHeading = that line, and section = it. Good — set lastHeading before assigning section. In my code above, I do the look-back before creating cur, and set lastHeading = pt. Then cur.section = lastHeading. 

Also `part` = lastRoman. Full path in expanded row: part + ' › ' + section (if both and different).

Now paragraph text: lines joined with ' ', double spaces collapsed, trimmed. page_start = first line's page, page_end = last line's page. If pageStart !== pageEnd → log repair "paragraph joined across a page break": Before = last line of previous page (truncated), After = first line of next page (truncated) — or "joined pages n–n+1". I'll do Before: `…${lastLineOfPrevPage.slice(-40)}`, After: `${firstLineOfNextPage.slice(0,40)}…`. Simpler: Before: 'page '+pageStart+' ends: …', After: 'page '+pageEnd+' begins: …'. Let me make Before/After concise snippets.

Footnote marks: walk paragraphs in order, one counter:

```js
let markCounter = 1;
const marksFound = []; // {n, para, context}
const rejected = [];   // {num, para, context}
for (const p of paragraphs) {
  p.text_raw = joinLines(p); // unmodified
  let text = p.text_raw;
  // find candidates
  const re = /\d{1,3}/g;
  let result = '';
  let last = 0;
  let m;
  const localMarks = [];
  while ((m = re.exec(text))) {
    const start = m.index, end = start + m[0].length;
    const prevCh = start > 0 ? text[start-1] : '';
    const nextCh = end < text.length ? text[end] : '';
    const blocked = ch => /[\d\/\-(\)]/.test(ch); // hmm
    ...
  }
}
```

Wait, blocked chars: digit, slash, dash, opening parenthesis. Let me define `isBlocked = ch => ch !== '' && /[\d\/\-(\)]/.test(ch)`. Hmm — should ')' block? Spec lists "another digit, a slash, a dash or an opening parenthesis". I'll block on both sides for: digit, '/', '-', '('. Not ')'. Hmm, but wait: "not touching another digit, a slash, a dash or an opening parenthesis" — touching means adjacent. So if prev or next char is any of those, the run is not a candidate. I'll check both sides against /[\d\/\-(\)]/? No — ')' is a closing paren, not listed. Use /[\d\/\-(\)]/... ugh, let me just write: `const bad = /[\d\/\-(\)]/;` no. OK: `function touchingBad(text, start, end){ const p = start>0?text[start-1]:''; const n = end<text.length?text[end]:''; return /[\d\/\-(\)]/.test(p) || ... }` — I keep confusing myself. The set is {digit, '/', '-', '('}. Regex: `/[\d\/\-(\)]/` includes ')' — wrong. Use `/[\d\/\-(\)]/`... no! Character class `[\d/\-(\)]` = digit, slash, hyphen, '(', ')'. I want to EXCLUDE ')' from the class: `[\d/\-(]` — that's digit, slash, hyphen, '('. In a regex char class, `(` doesn't need escaping: `/[\d/\-(]/`. Yes.

So: `const bad = ch => ch && /[\d\/\-(]/.test(ch);` candidate if !bad(prev) && !bad(next).

Hmm wait, but also: what about a digit run preceded by a letter, like "art.11"? "11" preceded by "." — not blocked → candidate. If counter==11 → wrongly bracketed. But spec says sequential rule works for this data. Also "article 11" — "11" preceded by space, followed by space/end → candidate; bracketed only if counter==11 at that moment. The check panel lists rejected numbers with context so reader sees "article 11" wasn't bracketed — meaning at that point counter ≠ 11. OK.

Hmm, wait — actually there's a subtlety: "Every run of one to three digits not touching another digit..." — a run of 4+ digits like "2025" — the regex `\d{1,3}` with /g would match "202" then "5"? No — `\d{1,3}` is greedy, matches "202" (3 digits) then next match starts at "5" → "5". Hmm, that's wrong: "2025" would produce candidates "202" and "5". But "not touching another digit" — the run "202" touches "5" (next char is digit) → blocked. Then "5": prev char is "2" (digit) → blocked. Good, the boundary check handles it. But careful with regex: after matching "202" at index i, lastIndex = i+3; next match "5" at i+3, prev char text[i+2]='2' digit → blocked. Good.

But wait, what about "12,345"? "12" followed by "," → candidate; "345" preceded by "," → candidate. Hmm, "not touching another digit, a slash, a dash or an opening parenthesis" — comma not blocked. So "12,345" gives two candidates. If counter matches one... edge case, ignore.

Also: marks like "waste.2" — "2" preceded by "." → candidate. Good. "equity, 17 common" — "17" preceded by space, followed by space → candidate. "”. 3" → candidate.

Replacement: build marked text by replacing candidate runs equal to counter with `[n]`, counter++. Others left as-is (record rejected with context: surrounding ~30 chars).

Context for rejected: `text.slice(max(0,start-25), start) + '[' + m[0] + ']' + text.slice(end, end+25)`.

Marks per paragraph: p.marks = [n,...]; p.footnotes_cited = marks joined '; '. p.text = marked text. p.text_raw = unmarked joined text.

Wait — order of operations: "Footnote marks inside the text are shown in square brackets... in the table, the expanded paragraph and the CSV". And first_words from text with marks removed. So: text_raw = joined; text = marked; first_words_found from text_raw? "the first six whitespace-separated words of the joined text, footnote marks removed first" — joined text = text_raw (marks are digits in raw). Removing marks from raw = removing the digit runs. Equivalent to removing [n] from marked. I'll compute from marked text: `p.text.replace(/\[\d{1,3}\]/g,' ')` then normalize whitespace, split, slice 6, join ' '. Hmm — replacing with '' vs ' ': "waste.[2] The" → "waste. The" either way. "equity,[17] common" → "equity, common" (replace with '') — good. Replace with '' then collapse whitespace.

Normalisation function:
```js
function norm(s){
  return String(s||'')
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[\u201C\u201D]/g, '"')
    .replace(/[\u2013\u2014]/g, '-')
    .replace(/\s+/g, ' ')
    .trim();
}
```
First words match: norm(found) === norm(reference) — case kept. Hmm, "case is kept" — so compare exact case after normalising quotes/dashes/whitespace. But reference first_words — e.g., "1": "A clean, healthy and sustainable environment". Found: "A clean, healthy and sustainable environment" — wait, para 1's text starts "A clean, healthy and sustainable environment is an essential precondition..." — first six words: "A clean, healthy and sustainable environment". Match. But careful: the paragraph number line "1." is separate; text starts with "A clean...". Good.

Hmm — but what about paragraphs where the number+text were on one line (23, 87)? Split handled: first line = text after "23. ". Good.

first_words_match = norm(found) === norm(ref). If ref missing → 'not run'.

Now checks list. Let me define checks as objects {name, detail, status: 'pass'|'fail'|'notrun', html}. Each check one line in the panel: "what was compared, the two values, and 'pass' in green or 'check failed' in red with a link to the rows concerned."

Checks:
1. Paragraph count: found vs ref.paragraphs. pass if equal. Link to tab 02.
2. Numbering: numbers exactly 1..n in order. List gaps/duplicates with page.
3. First words: mismatches count; list each "para. n: found … / reference …". Link to rows (I'll give each paragraph row an id `p-<n>` and link `#` + switch to tab 02? Links inside tab 04 to rows on tab 02 — clicking should switch tab. I'll make such links buttons that activate tab 02 and expand the row. Simpler: link with data attributes; JS handles click → show tab 02, expand row, scroll. I'll implement a helper.)
4. Footnotes: found vs ref.footnotes; numbering 1..count no gaps/dups; restored listed with page.
5. Footnote marks: marks 1..ref.footnotes no gaps; missing listed; rejected listed with context.
6. Footnotes stay out of paragraphs: search first 40 chars of each footnote opener line (with number) in each paragraph's text_raw — expected 0 hits; paragraphs >300 words listed. Hmm — "the first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…'; for a footnote whose number was displaced, its first line)". So for each footnote, take its opener line's first 40 chars (e.g., "15 Human Rights Committee, general comm") — for restored ones, the first line of its text (since number was displaced, the opener line in the PDF had no number; "its first line" — the first line of the footnote text). Search in raw paragraph text (before marks). Count hits. Also list paragraphs over 300 words. Pass if 0 hits (and maybe note long paragraphs). Hmm — "every paragraph over 300 words is listed (the longest real one has 254)" — so if any paragraph >300 words, that's suspicious (footnote block read as body) — the check fails? "A hit means a footnote block was read as body: the check fails". The >300 words listing is informational — I'll fail the check if hits>0; list long paragraphs as part of detail (if any >300, mention; maybe also fail? The spec: "and every paragraph over 300 words is listed" — just listed. I'll list them; fail only on hits. Hmm, but a >300-word paragraph likely indicates footnote leakage even without exact 40-char hit... I'll fail if hits>0 OR any paragraph >300 words? The spec says "A hit means... the check fails". For >300 words it just says listed. I'll fail on hits>0, and list >300-word paragraphs in the detail (and if any exist, mark check failed too? Let me fail on hits only, but list long ones; actually to be safe, treat >300 words as failure too since it indicates leakage — hmm, but "the longest real one has 254" so none should exceed; if one does, something's wrong. I'll fail if hits>0 or longParagraphs.length>0, with clear detail.) Hmm, wait — careful: footnote text could legitimately be inside... no. OK: fail if hits>0; also list >300-word paragraphs and fail if any (since expected max 254). Actually let me just fail on hits>0 and separately list >300 word paragraphs as part of the same check line, failing if either. Fine.

   For the search: footnote opener line first 40 chars — I need to store the opener line raw for each footnote. For normal footnotes: the line that opened it, e.g., "15 Human Rights Committee, general comment..." → first 40 chars "15 Human Rights Committee, general comm". For restored: its first text line, e.g., "A/42/427, p. 24." → first 40 chars. Search in each paragraph's text_raw (normalized? "searched in the raw text of every paragraph" — I'll search in norm(text_raw) with norm(opener40)? Whitespace differences... The paragraph text_raw is joined with single spaces; the opener line is a raw line. If the footnote text got glued into a paragraph, the paragraph's joined text would contain the opener line's content possibly with different spacing. I'll normalize both (collapse whitespace) and search. Also the mark digits: "before footnote marks are touched" — text_raw is before marks. Good.)

   Hmm, also: "continuation lines are not searched, because a citation such as 'United Nations Framework Convention on Climate Change' also occurs in paragraph 6" — right, only opener lines.

7. Headers and footers: pages whose first line was symbol (expected all — count); pages with page number in footer (expected all but first); displaced numbers listed with page.
8. Headings: number of labelled and unlabelled; list unlabelled ones.
9. Nothing lost: every non-empty line classified exactly once; counts per kind sum to total non-empty lines; unclassified listed with page (shown red in raw viewer).

For "nothing lost": I classify every line in every page: header, footer, blank, footnote, cover, heading, paragraph. Non-empty lines must have kind in {header, footer, footnote, cover, heading, paragraph}. Sum of those counts === total non-empty lines. Blank lines are empty (after trim) — not counted. But wait: lines that are whitespace-only — "non-empty" means trim() !== ''. OK.

Hmm — but the footnote block lines: all marked 'footnote'. Body lines before block: classified in walk. Header/footer: marked. So every line gets a kind. Unclassified = lines with kind null and trim non-empty — should be 0.

Wait — one problem: in the walk, I skip blank lines (`if (t==='') continue`) without setting kind — they stay null but they're empty, fine. But I should mark them 'blank' for the raw viewer coloring? The raw viewer colors each line by classification; blank lines can be uncolored. I'll set kind='blank' for them in the walk (or pre-set). Let me set kind='blank' when t===''.

Also the raw viewer needs per-line kinds for ALL lines including header/footer/footnote — I have that from page parsing. I'll store per page: `lines: [{raw, kind}]` where kind ∈ cover/header/heading/paragraph/footnote/footer/blank/unclassified.

Now the "Repairs made" count = repairs.length. Repair log table with count per kind above it: I'll render a small summary line: "header line removed ×20 · footer line removed ×20 · ..." as monospace chips or a line. "with a count per kind above it" — a line above the table listing each kind with count.

Repair log columns: Page | Paragraph or footnote | What was done | Before | After. "What was done" = kind (human-readable). Before/After = snippets (truncate to ~80 chars, with title attr for full).

Now tab 01 tiles:
- Tile 1: "Paragraphs found: n" big; beside it "The document has: reference.paragraphs"; green when equal, red with difference ("+2" / "−3"). How computed: "Count of lines matching a paragraph number (1–3 digits + '.') in the body after headers, footers and footnote blocks were removed."
- Tile 2: "Footnotes found: n of reference.footnotes". How: "Numbered footnote openers in the page-foot blocks, plus numbers restored from page footers."
- Tile 3: "First words match: n of reference.paragraphs". How: "First six words of each paragraph vs the reference, after normalising quotes, dashes and spaces."
- Tile 4: "Repairs made: n" link to repair log. How: "Every line or join the script changed, listed on tab 04."

If reference missing: tiles say "no reference in this file".

Also tile 1 note: "n contain footnotes" in red if check 6 hits>0.

Rail card: symbol, short title — I'll derive short title? The doc has `title` (long). "its short title" — pdf_text has only `title`. I'll show title (maybe clamped with CSS line-clamp 3). "adopted …", "n pages". Big numbers: paragraphs found + "of X" + bar; footnotes found + "of Y" + bar. Bar: thin div, width = min(100, found/expected*100)%, red when short or over (over → 100% red? "red when short or over" — if found>expected, bar full and red; if equal, green? The accent is red... hmm. "a thin bar showing the share found (red when short or over)". So bar color: red when short or over; otherwise (equal) — some neutral/ink color? I'll use ink (#1d1b18) when equal, red otherwise. Then "n of m checks pass" link to tab 04.

Header right: dot + "n of m checks pass" (green dot) or red dot + "n checks failed" + red dot on tab 04 label. "a red dot on tab 04" — add a small red dot next to "04 CHECKS & METHOD" tab label when failures.

Tabs: 01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD.

Tab 02 details:
- Collapsible "Headings found: n" box above the table: a button with aria-expanded toggling a list of headings (display strings, labelled/unlabelled marked). 
- Table caption: serif, states message: "90 paragraphs found, 90 expected" + monospace "TAB.01"? The figure numbers: "FIG.01" style for figures; tables get "TAB.01"? Spec: "Every table has a serif <caption> that states the message ('90 paragraphs found, 90 expected') and a monospace number (TAB.01)." So captions like `<caption><span class="fig">TAB.01</span> 90 paragraphs found, 90 expected</caption>`. I'll number TAB.01 (paragraphs), TAB.02 (footnotes), TAB.03 (repair log).
- Columns: No. | Section | Page | First line | Check. No. right-aligned, red accent color for paragraph numbers ("Red accent on ... the paragraph numbers in the first column").
- First line: first 120 chars cut at a word + "…". Compute: take text (marked), if length>120, cut at last space before 120, add "…".
- Check cell: "OK" (green) or "first words differ" (red).
- Page cell: "3–4" if spans pages, else "3".
- Section cell: section display (may be long — clamp).
- Expanded row: full text (marked, verbatim), toggle "Show the PDF's lines" → shows lines with page markers like "[p. 3] line text..." — "the page number where each page began" — I'll render each line prefixed with its page when it changes: e.g. `— page 3 —` marker before the first line of each page. Then comparison block: "Reference first words: … / Found: …" with equal/different mark; pages; repairs touching this paragraph (list of kind strings); footnotes cited; Copy citation button.

Wait — "the reference's first six words next to the extracted first six words, marked equal or different; the page(s); the repairs that touched this paragraph; and a Copy citation button". Also "The expanded paragraph also lists the footnotes it cites" (from tab 03 spec). Include footnotes cited in expanded row.

- Note under table: "Footnote marks are shown in square brackets, e.g. waste.[2]. Remove them with find-and-replace using the pattern \[\d+\]." — in monospace hint.

Tab 03: caption "Footnotes found: n of m" + TAB.02. Columns No. | Page | Text | Repair. Repair: "number restored from the page foot" for repaired, else "—". Download footnotes.csv button. Maybe also note about the asterisk footnote if present: "The cover's asterisked note is kept as footnote * and not counted." I'll add if a '*' footnote exists.

Tab 04: 
- Check panel open: heading "Checks" + each check one line. Format: monospace label? Each check: name (sans, medium), detail (small), status word "pass" green / "check failed" red / "not run". With links to rows where relevant.
- "Repair log (n)" closed heading (button aria-expanded) → count per kind line + table TAB.03: Page | Paragraph or footnote | What was done | Before | After.
- "Raw pages" closed heading → select "Show raw page n" (options per page) + monospace panel with line numbers left, each line colored by kind, legend with six tints + letter codes.
- Download: "Download paragraphs as CSV" button.

Footer: source line, built date (if present), and the honesty line.

Now — CSV generation:

```js
function csvEscape(v){ return '"' + String(v==null?'':v).replace(/"/g,'""') + '"'; }
function toCSV(rows){ return '\ufeff' + rows.map(r => r.map(csvEscape).join(',')).join('\r\n') + '\r\n'; }
```
Blob with type 'text/csv;charset=utf-8'. Filename: symbol.replace(/\//g,'-') + '-paragraphs.csv'.

Paragraph CSV columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, text_lines, footnotes_cited, repairs, citation, symbol, doc_url. text_lines joined with " | ".

Footnotes CSV: number, page, text, repair, symbol, doc_url.

Download via Blob + a.click().

Copy citation: navigator.clipboard.writeText with fallback.

Now, multi-document support: rail cards for each doc; clicking a card re-renders the tabs area for that doc. I'll structure: parse all docs up front (or lazily on select — parse on load for all, it's cheap; but rail needs counts → parse all at load). State: selectedDoc index. renderAll() builds header info? Header shows selected doc's title/symbol. Rail shows all cards. Tabs content re-rendered on selection.

Actually simpler: parse each doc once at load, store result. On card click, set selected, re-render header line + tabs. I'll write render functions that rebuild the tab panels' innerHTML from the parsed result. Since content is large (90 paragraphs), rebuilding is fine.

Let me now also handle: "the selected card has a red left border".

Arrow-key tab navigation: keydown on tablist: ArrowRight/ArrowLeft move focus+activate (I'll activate on arrow, standard pattern: focus follows selection or use roving tabindex; simplest: arrows move selection and focus).

Now let me think about sizes: 90 paragraphs × expanded detail — render all rows collapsed initially. Fine.

Raw page viewer: 20 pages, each up to ~4300 chars → ~60-80 lines. Rendering one page at a time via select. Each line: `<div class="rl"><span class="ln">12</span><span class="lt k-paragraph">text</span></div>`. Colors: pale tints:
- cover: #efe6d8? Let me pick six pale tints on paper background:
  - cover: #ece4d4 (pale tan)
  - header: #e8e0f0? hmm keep warm palette... "six pale tints" — any pale colors OK ("Other colours only where a category needs one" — the raw viewer is the exception). I'll use:
  - cover C: #efe7d7
  - header H: #e6e9f2 (pale blue-grey)
  - heading T: #f3dede (pale red tint)
  - paragraph P: #e9f0e4 (pale green)
  - footnote F: #f7ecd9 (pale amber)
  - footer X: #e4e4e4 (pale grey)
  Letter codes in margin: C/H/T/P/F/X. Legend below with same tints.

Text color stays ink for readability.

Now, checks details — let me enumerate what I compute:

```js
checks = [
 {id:'count', name:'Paragraph count', detail: `Found ${paras.length} numbered paragraphs; the reference says ${ref.paragraphs}.`, status: paras.length===ref.paragraphs?'pass':'fail', link: tab02},
 {id:'numbering', name:'Numbering', detail: numbers 1..n in order? gaps/dups listed, status},
 {id:'firstwords', name:'First words', detail: `${matches}/${ref.paragraphs} match; mismatches: ...`, status: mismatches===0},
 {id:'footnotes', name:'Footnotes', detail: `Found ${fns.length} of ${ref.footnotes}; numbers 1..${fns.length} without gap or duplicate; restored: ${list}`, status},
 {id:'marks', name:'Footnote marks', detail: `Marks found run 1..${maxMark} ... missing: [...]; rejected numbers: [...]`, status},
 {id:'leak', name:'Footnotes stay out of the paragraphs', detail: `0 of ${fns.length} footnote openers found in paragraph text; paragraphs over 300 words: ${list}`, status},
 {id:'hf', name:'Headers and footers', detail: `${headerOk}/${pages} pages start with the symbol; ${pageNumCount} pages carry their page number in the footer (all but the first expected); displaced numbers: ${list}`, status},
 {id:'headings', name:'Headings', detail: `${labelled} labelled, ${unlabelled} unlabelled: list`, status: 'pass' (informational — always pass? It's a check that headings were found and none swallowed; status pass if unlabelled list matches... hmm. I'll make it informational pass: "n headings found (x labelled, y unlabelled); unlabelled: …" status pass unless... I'll mark pass always but list. Actually a check should be able to fail: if an unlabelled heading looks like a paragraph's last line mistaken... can't verify automatically. I'll keep it as informational with status 'pass' when headings found > 0. Hmm, or 'not run'? No. I'll say pass with the list.)
 {id:'lost', name:'Nothing lost', detail: `Every non-empty line classified exactly once: cover ${c}, header ${h}, heading ${d}, paragraph ${p}, footnote ${f}, footer ${x} = ${sum} of ${total} non-empty lines; unclassified: ${list}`, status: sum===total && unclassified.length===0}
]
```

Marks check: marks found should run 1..ref.footnotes without gap. marksFound list of numbers in order; check sequence equals 1..max; missing = numbers in 1..ref.footnotes not in marks; also marks beyond ref.footnotes? List. Rejected numbers with context — could be many (every "article 11" etc.). Listing all rejected could be long — I'll list them in a collapsible detail or cap at, say, all of them in a scrollable box. The spec says "the check lists any missing numbers and the numbers it rejected as not being marks (with context)". I'll render them in a small scrollable list within the check line's detail (max-height with overflow). OK.

Status logic for marks: pass if marks sequence is exactly 1..ref.footnotes (no gaps, no extras). 

Now, "n of m checks pass" — m = checks.length (9). If reference missing, some checks 'not run' — then pass count excludes them? "the checks that need it show 'not run', never 'pass'". So m = number of checks run? I'll compute: runChecks = checks.filter(c=>c.status!=='notrun'); pass = those with 'pass'. Display "n of m checks pass" where m = runChecks.length. If reference missing entirely, tiles say "no reference in this file" and checks needing it are 'not run'; header shows "n of m checks pass" over run checks (headers/footers/lost/headings don't need reference). Fine.

Now let me also double check the footnote-block-start edge on page 1 more carefully, because getting this wrong breaks everything. Page 1 content (after header "E/C.12/GC/27" removed and footer removed): cover lines, "I.", blank, "Introduction", "1.", "A clean, healthy...", ... paragraphs ..., then footnote block: "* Adopted by the Committee..." (maybe), "1 ...", "2 ...", etc.

Block-start search with nextFootnote=1: scan lines top-down; first line that is bare "1", or starts with "1 ", or (page 1) starts with "* ". Cover lines: "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on ...", "I.", "Introduction", "1.", "A clean...". 

- "6 November 2025": starts with "6 " — nextFootnote is 1, so `startsWith("1 ")`? "6 November..." starts with "6", not "1". No.
- "1.": bare "1"? No (has dot). starts with "1 "? "1." — second char is ".", not space. No.
- Any line starting with "1 "? Hmm — could a wrapped title line start with "1 "? Unlikely.
- "* Adopted..." if present before footnote 1 → block starts there. If the asterisk note is at the very end of page 1 (after footnotes), then block starts at footnote 1's opener, and the "*" line is inside the block → my block parser opens footnote '*' on "* " lines. Good, handled.

But wait — what if the asterisk note is AFTER the numbered footnotes on page 1 and the block started at "1 ..."? Then within block parsing, when we hit "* Adopted...", we open footnote '*'. But the rule "Any line that starts with a number and a space opens a footnote" — "*" doesn't. And my special displaced logic: displaced is null on page 1, so continuation lines append to current footnote — but "* " line opens '*' footnote before that. Order of checks in block parser: check "* " first, then bare number, then number+space, else continuation. Good.

Hmm, but one more: what if the "*" note appears between footnotes? Handled — opens '*'.

Now, nextFootnote advancement on page 1: block contains '*' and footnotes 1..k. nextFootnote = max(k, displaced||0)+1 = k+1. Good.

Another edge: what if a page's footnote block's first opener is "N text" (number+space) rather than bare? Handled.

What about pages where the footnote block contains a number LOWER than nextFootnote (out of order)? "even when the number is not the one expected" — accept. nextFootnote = max+1 anyway.

Now the jump case: "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump". Note: "bare number greater than it" — only bare numbers (not "N text" lines)? Spec says "the first bare number greater than it". OK, search `/^\d{1,3}$/` with value > nextFootnote. If found, blockStart there, log jump (I'll log as repair kind 'footnote block removed' with note "starts at footnote k, expected m — jump logged", or as a separate note in checks). Hmm — the repair kinds are fixed at 8; the jump isn't one of them. I'll record the jump in the page info and surface it in the footnotes check detail ("page n starts at footnote k, expected m"). And the block removal repair still logged. Good.

Now — the displaced number and nextFootnote: "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page." So if page 2 has block with footnotes 5,7 (6 displaced): highest seen = 7, displaced 6 → next = 8. But wait — in my block parser, footnote 6 is opened via the displaced rule, so "numbers seen in block" includes 6 anyway. Fine either way.

Hmm, wait — actually there's a subtle issue: on page 2, the block opener search: nextFootnote should be 5 when we reach page 2 (page 1 had footnotes 1-4). Block starts at bare "5". Good. But what if page 1 had footnotes 1-4 and page 2's first footnote is 5 — yes.

But here's a trickier scenario: what if the displaced number D is the FIRST footnote on a page? Spec says it's always the second. OK.

Now — the footer displaced number: on page 2, footer contains "6" (displaced), "2" (page number), "GE.25-15926". My footer loop from end: "GE.25-15926" → footer; "2" → bare number === page → page number; "6" → bare number ≠ page → displaced=6. Loop continues while lines match — next line up is footnote text (ends with '.') → stop. 

But wait — order varies: "the last lines of a page are, in varying order, the page number alone on a line (pages 2 to 20) and the job code 'GE.25-15926'; ... On 12 pages a third bare number sits in the footer". So footer = {page number, GE code, maybe displaced}. My loop handles any order. But careful: what if the displaced number equals the page number? E.g., page 6 with displaced 6? Then ambiguous — the loop would treat "6" as page number. Hmm — on page 6, if displaced is 6... the displaced numbers are 6, 14, 45, 51, 67, 76, 87, 96, 101, 115, 118, 131 — page 6 could have displaced 6? The displaced numbers listed: 6 is displaced on some page — if that page is page 2 (per example: page 2 has displaced 6). Page 6's displaced would be a different number. But could page 14 have displaced 14? The displaced list includes 14 — if it's on page 14, ambiguity! My loop: from end, first bare number encountered... if footer is "14\nGE.25-15926" on page 14 — "14" === page → treated as page number, displaced lost. Hmm. But the spec says "A bare number equal to page is the page number; any other is a displaced footnote number" — so if both appear, the one equal to page is the page number and the other is displaced. If only one bare number and it equals page... then no displaced on that page. The data presumably has displaced numbers on pages where they differ from the page number, or both lines present. I'll follow the spec rule exactly: equal to page → page number; else displaced. If two bare numbers and one equals page: the other is displaced. My loop handles since it processes each line independently. But if only ONE bare number and it equals page, it's the page number (correct per spec). OK.

Hmm, wait — but actually, what if the displaced number appears and the page number also appears, order varying — handled. What if displaced number appears but page number doesn't (page 1)? Page 1 has no bare numbers in footer per spec (GE code + date stamp). OK.

Now, the "footnote number restored" repair: when I open footnote D in the block parser, log repair: {page, target: 'footnote '+D, kind:'footnote number restored', before: first line of D's text (the unnumbered line), after: D + ' ' + first line}. 

Now — an important detail: the footnote block detection uses `nextFootnote` which advances per page. But the displaced number D on a page: the block opener is the first footnote (bare number == nextFootnote). E.g., page 2: nextFootnote=5, block starts at "5". Good. But what if a page's first footnote number was displaced (block opener would be the second footnote)? Spec says displaced is always second. OK.

Now, body lines concatenation and paragraph joining across pages: since I concatenate all body lines in page order, a paragraph spanning pages is naturally joined; I detect pageStart !== pageEnd and log the repair. But careful: the page break might fall between paragraphs — then no join. Also the page break might fall mid-heading? Headings are within a page presumably. Fine.

Also — the cover: lines before first paragraph start on page 1. But what if body lines exist on page 1 after... no, cover is only before para 1.

Wait — one more thing: the header removal — "If a page's first non-empty line equals symbol". Compare trimmed line to symbol exactly. Page 1's first line is "E/C.12/GC/27" — matches symbol. Good.

Now — "Paragraphs found" tile: count = paragraphs.length. Reference 90. 

Let me now also handle `count` field: "count is the string '20'" — I'll use records.length for pages, and maybe show `count` too? Header: "n pages of raw converter text" — n = records.length. Fine.

Now the header line: `symbol` linked to doc_url (new tab, target=_blank rel=noopener), "adopted reference.adopted", "n pages of raw converter text", source. E.g.: "E/C.12/GC/27 · adopted 6 November 2025? ..." — reference.adopted — I don't know its exact value; read from data. Format: `<a>symbol</a> — adopted ${ref.adopted} — ${n} pages of raw converter text — ${source}`. Hmm "one line with the data's source, n and years" from the general layout rules; here the plan specifies the content. I'll do: symbol link, "adopted …", "n pages of raw converter text", source. If ref missing, omit adopted.

One sentence under header: "This page splits the converter's raw text into numbered paragraphs, removes headers, footers and footnotes, checks itself against the document's reference, and lists every repair it made."

Right side: dot + "n of m checks pass" or red "k checks failed".

Now — implementation size: this is a big app. Let me keep it organized and under ~1500 lines. Let me write carefully.

Let me draft the HTML structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF — …</title>
<style> ... </style>
</head>
<body>
<header class="top">
  <div class="kicker">UN DOCUMENT · PDF TEXT</div>
  <div class="headrow">
    <div>
      <h1 id="docTitle"></h1>
      <p class="meta" id="docMeta"></p>
      <p class="what" id="docWhat"></p>
    </div>
    <div class="checkpill" id="checkPill"></div>
  </div>
</header>
<div class="layout">
  <aside class="rail">
    <div class="railhead">DOCUMENT</div>
    <div id="docCards"></div>
  </aside>
  <main>
    <div class="tabs" role="tablist" id="tablist" aria-label="Sections">
      <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 RESULT</button>
      ... 02 PARAGRAPHS, 03 FOOTNOTES, 04 CHECKS & METHOD (with dot span)
    </div>
    <section id="panel-0" role="tabpanel" aria-labelledby="tab-0">…tiles…</section>
    <section id="panel-1" role="tabpanel" aria-labelledby="tab-1" hidden>…</section>
    <section id="panel-2" ... hidden>…</section>
    <section id="panel-3" ... hidden>…</section>
  </main>
</div>
<footer id="foot"></footer>
<script> ... </script>
</body>
</html>
```

Tabs labels: "01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD" — the plan writes them with "·" separators in the description but they're separate tabs: `01 RESULT`, `02 PARAGRAPHS`, `03 FOOTNOTES`, `04 CHECKS & METHOD`. I'll render as separate buttons with monospace uppercase labels.

CSS plan:

```css
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1e6b3a;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:30px;line-height:1.2;margin:6px 0 4px}
...
```

Layout: header full width with padding; layout = grid: rail 260px + main 1fr; max-width 1180px margin auto.

Rail cards: border-left 3px solid transparent; selected → var(--red). Card content: symbol mono, title small serif? "its short title" — I'll show title in 13px sans, clamped. "adopted …", "n pages" small. Big numbers: serif 40px. Bars: 4px height background rule color, fill ink or red.

Tiles: grid 2×2 (or 4 across on wide). Each tile: top rule, mono label, big serif number, side note, how-computed line in small mono/sans.

Tables: width 100%, border-collapse; th mono uppercase 11px letter-spaced, border-bottom 1px rule; td padding 8px 10px, border-bottom 1px solid rule; numbers right-aligned (class .num). caption: serif 20px, text-align left, padding-bottom, with mono fig number.

Buttons: plain, underline on hover, red focus ring.

Check lines: each `.check` with border-top rule, padding; status word colored.

Raw viewer: `.rawline{display:flex} .ln{width:3ch; text-align:right; color:#8a8375; user-select:none} .lt{flex:1; white-space:pre-wrap; font-family:monospace; font-size:12.5px}` with background tint per kind. Letter code: `.lt::before{content:attr(data-k); ...}` — hmm, letter in margin: I'll add a small code span. Let me do: `<span class="code k-p">P</span>` before text. Legend: swatches.

Colors for kinds:
```css
.k-cover{background:#efe6d3}.k-header{background:#e3e7f0}.k-heading{background:#f2dcdc}.k-paragraph{background:#e7efe2}.k-footnote{background:#f6ecd6}.k-footer{background:#e6e2da}.k-blank{background:transparent}.k-unclassified{background:#f2c4c4}
```

Now the JS. Let me write it fully.

```js
(function(){
'use strict';
var DATA = window.WORKSHOP_DATA || {};

function norm(s){
  return String(s==null?'':s)
    .replace(/[\u2018\u2019]/g,"'")
    .replace(/[\u201C\u201D]/g,'"')
    .replace(/[\u2013\u2014\u2212]/g,'-')
    .replace(/\s+/g,' ')
    .trim();
}
function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function trunc(s,n){ s=String(s==null?'':s); return s.length>n? s.slice(0,n-1)+'…' : s; }
function cutWord(s,n){ s=String(s); if(s.length<=n) return s; var cut=s.slice(0,n); var sp=cut.lastIndexOf(' '); return (sp>0?cut.slice(0,sp):cut)+'…'; }
```

Documents discovery:

```js
var docs=[];
Object.keys(DATA).forEach(function(k){
  var d=DATA[k];
  if(d && Array.isArray(d.records) && d.records.length && d.reference && typeof d.reference==='object') docs.push({key:k,doc:d});
});
```

Hmm — should I require reference.paragraphs? "with records and a reference" — just reference object. OK.

Parse:

```js
function parseDoc(doc){
  var symbol = doc.symbol || '';
  var ref = doc.reference || null;
  var records = doc.records.slice().sort(function(a,b){return a.page-b.page;});
  var firstPage = records.length? records[0].page : null;
  var repairs=[];   // {page,target,kind,before,after}
  var pages=[];     // {page, lines:[{raw,kind}], headerOk, pageNum, displaced, blockStart, jump, hasBlock}
  var footnotes=[]; // {number, page, text, repaired, opener}
  var bodyAll=[];   // {raw,page,kind}
  var nextFootnote=1;
  var pageNotes=[];

  records.forEach(function(rec){
    var page=rec.page;
    var rawLines=String(rec.text==null?'':rec.text).split('\n');
    var lines=rawLines.map(function(r){return {raw:r,kind:null,page:page};});
    var pg={page:page,lines:lines,headerOk:false,pageNum:false,displaced:null,hasBlock:false,jump:null};
    pages.push(pg);
    // header
    var i=0;
    while(i<lines.length && lines[i].raw.trim()==='') i++;
    if(i<lines.length && lines[i].raw.trim()===symbol){
      lines[i].kind='header'; pg.headerOk=true;
      repairs.push({page:page,target:'—',kind:'header line removed',before:lines[i].raw.trim(),after:'removed'});
      i++;
    } else {
      pageNotes.push('page '+page+': first non-empty line is not the symbol');
    }
    // footer
    var j=lines.length-1;
    var foot=[];
    while(j>=i){
      var t=lines[j].raw.trim();
      if(t===''){ lines[j].kind='blank'; j--; continue; }
      if(t.indexOf('GE.')===0){ foot.push(lines[j]); j--; continue; }
      if(/^\d{6}(\s+\d{6})*$/.test(t)){ foot.push(lines[j]); j--; continue; }
      if(/^\d{1,3}$/.test(t)){
        var n=parseInt(t,10);
        if(n===page){ pg.pageNum=true; }
        else { pg.displaced=n; }
        foot.push(lines[j]); j--; continue;
      }
      break;
    }
    if(foot.length){
      foot.forEach(function(l){ l.kind='footer'; });
      repairs.push({page:page,target:'—',kind:'footer line removed',
        before: foot.map(function(l){return l.raw.trim();}).join(' / '),
        after:'removed'+(pg.displaced!=null?' (number '+pg.displaced+' kept aside as a displaced footnote number)':'')});
    }
    // content lines i..j
    var content=lines.slice(i,j+1);
    // footnote block start
    var blockStart=-1, jump=null;
    for(var k=0;k<content.length;k++){
      var ct=content[k].raw.trim();
      if(/^\d{1,3}$/.test(ct) && parseInt(ct,10)===nextFootnote){ blockStart=k; break; }
      if(ct.indexOf(nextFootnote+' ')===0){ blockStart=k; break; }
      if(page===firstPage && ct.indexOf('* ' )===0){ blockStart=k; break; }
    }
    if(blockStart===-1){
      for(var k2=0;k2<content.length;k2++){
        var ct2=content[k2].raw.trim();
        if(/^\d{1,3}$/.test(ct2) && parseInt(ct2,10)>nextFootnote){ blockStart=k2; jump=parseInt(ct2,10); break; }
      }
    }
    var body, block;
    if(blockStart===-1){ body=content; block=[]; pageNotes.push('page '+page+': no footnote block found; all lines are body'); }
    else { body=content.slice(0,blockStart); block=content.slice(blockStart); pg.hasBlock=true; pg.jump=jump; }
    if(block.length){
      repairs.push({page:page,target:'—',kind:'footnote block removed',
        before: trunc(block[0].raw.trim(),60), after:'moved to the footnotes ('+block.length+' lines)'+(jump!=null?'; block starts at footnote '+jump+', expected '+nextFootnote+' — jump logged':'')});
    }
    // parse block into footnotes
    var cur=null, firstFn=null, firstClosed=false, highest=0;
    block.forEach(function(ln){
      var t=ln.raw.trim();
      ln.kind='footnote';
      if(t==='') return;
      var m;
      if(t.indexOf('* ' )===0){
        cur={number:'*',page:page,text:t.slice(2),repaired:false,opener:t};
        footnotes.push(cur); if(!firstFn) firstFn=cur; highest=Math.max(highest,0);
        return;
      }
      if((m=t.match(/^(\d{1,3})$/))){
        cur={number:parseInt(m[1],10),page:page,text:'',repaired:false,opener:t};
        footnotes.push(cur); if(!firstFn) firstFn=cur; highest=Math.max(highest,cur.number);
        if(cur===firstFn && pg.displaced!=null && t.endsWith('.')) firstClosed=true; // bare number never ends with '.', skip
        return;
      }
      if((m=t.match(/^(\d{1,3}) (.+)$/))){
        cur={number:parseInt(m[1],10),page:page,text:m[2],repaired:false,opener:t};
        footnotes.push(cur); if(!firstFn) firstFn=cur; highest=Math.max(highest,cur.number);
        if(cur===firstFn && pg.displaced!=null && m[2].endsWith('.')) firstClosed=true;
        return;
      }
      // continuation
      if(pg.displaced!=null && firstFn && cur===firstFn && firstClosed){
        // open the displaced footnote
        cur={number:pg.displaced,page:page,text:t,repaired:true,opener:t};
        footnotes.push(cur); highest=Math.max(highest,cur.number);
        repairs.push({page:page,target:'footnote '+pg.displaced,kind:'footnote number restored',
          before: trunc(t,60), after: pg.displaced+' '+trunc(t,60)});
        return;
      }
      if(cur){
        cur.text=(cur.text?cur.text+' ':'')+t;
        if(cur===firstFn && pg.displaced!=null && !firstClosed && t.charAt(t.length-1)==='.') firstClosed=true;
      }
    });
    if(pg.displaced!=null) highest=Math.max(highest,pg.displaced);
    nextFootnote=Math.max(nextFootnote,highest)+1;
    // body lines
    body.forEach(function(ln){ bodyAll.push(ln); });
  });
```

Hmm wait — there's a bug in the displaced logic: the first footnote on the page is opened by a bare number (e.g., "5"), then blank, then text "A/79/270, paras. 84 and 85." — the continuation branch: cur===firstFn, displaced=6, firstClosed=false → append text; ends with '.' → firstClosed=true. Then next line "A/42/427, p. 24." — continuation: cur===firstFn && firstClosed && displaced → open footnote 6. 

But what if the first footnote's text is multiple lines and the first line ends with '.'? Then firstClosed=true after first line, and the second line would wrongly open footnote D. Per spec, in all 12 cases the first footnote is ONE line ending with a full stop. So OK.

But hmm — what if displaced != null but the first footnote in the block is NOT followed by D's lines (e.g., D's lines come elsewhere)? Spec guarantees. OK.

Another subtle bug: what if displaced != null and the block's first footnote opener is "N text" (number+space) where text ends with '.'? Then firstClosed set at open. Next continuation line → opens D. OK.

Also: what if displaced != null but firstClosed never set (first fn text never ends with '.')? Then D's lines glue to first fn. The footnote count check will show shortfall. Acceptable.

Wait, also — the bare-number opener case: `if(cur===firstFn && pg.displaced!=null && t.endsWith('.'))` — t is the bare number, never ends with '.', so that line is dead code; remove.

Hmm, also: what about the case where displaced != null and the block's first line is the bare number, then blank, then text — but ALSO what if the displaced footnote is the first on the page? Spec says second. Skip.

Now — one more issue with the block-start search: `ct.indexOf(nextFootnote+' ')===0` — if nextFootnote is 1 and a cover line is "1 something"... on page 1 cover: "6 November 2025" — starts with "6 ". nextFootnote=1 → no. OK. But what about paragraph continuation lines on later pages starting with e.g. "20 " when nextFootnote=20? Possible in theory; the spec's rule accepts this risk. Hmm, actually wait — this could be a real problem: body text lines like "2030 Agenda" — starts with "20" but next char "3" — `indexOf("20 ")` requires space after "20" — "2030" has "3" → no match. A line starting "20 days" would match if nextFootnote=20. In this document, footnote numbers go up to 141 across 20 pages, ~7 per page. A body line starting with exactly the next footnote number + space is unlikely. Proceed.

Now the body walk:

```js
  // walk body lines
  var paragraphs=[]; var headings=[]; var coverCount=0;
  var mode='cover'; var cur=null;
  var lastHeading=''; var lastRoman='';
  var curHead=null; // {label, titles:[], page, display}
  var hyphenLines=0;

  function prevNonEmpty(idx){
    for(var x=idx-1;x>=0;x--){ if(bodyAll[x].raw.trim()!=='') return bodyAll[x]; }
    return null;
  }

  bodyAll.forEach(function(ln,idx){
    var t=ln.raw.trim();
    if(t===''){ ln.kind='blank'; return; }
    if(ln.raw.length && ln.raw.charAt(ln.raw.length-1)==='-') hyphenLines++;
    var m;
    if((m=t.match(/^(\d{1,3})\.$/)) || (m=t.match(/^(\d{1,3})\. (.+)$/))){
      var num=parseInt(m[1],10);
      var firstText=m[2]||'';
      // unlabelled heading look-back
      if(mode==='paragraph' && cur && cur.lines.length){
        var prev=prevNonEmpty(idx);
        if(prev && cur.lines[cur.lines.length-1]===prev){
          var pt=prev.raw.trim();
          if(pt.length<=90 && /^[A-Z\u00C0-\u00DE]/.test(pt) && !/[.;:,\d]$/.test(pt)){
            cur.lines.pop();
            prev.kind='heading';
            headings.push({display:pt,labelled:false,page:prev.page});
            lastHeading=pt;
            repairs.push({page:prev.page,target:'para. '+num,kind:'heading separated',
              before:pt+' (would have joined para. '+cur.number+')',after:'kept as a heading'});
            // fix pageEnd
            if(cur.lines.length) cur.pageEnd=cur.lines[cur.lines.length-1].page;
          }
        }
      }
      if(firstText){
        repairs.push({page:ln.page,target:'para. '+num,kind:'number and text split',
          before:trunc(t,70),after:num+'.  →  '+trunc(firstText,60)});
      }
      cur={number:num,lines:[],pageStart:ln.page,pageEnd:ln.page,section:lastHeading,part:lastRoman,marks:[],repairs:[]};
      if(firstText) cur.lines.push({text:firstText,page:ln.page});
      ln.kind='paragraph';
      paragraphs.push(cur);
      mode='paragraph';
    } else if((m=t.match(/^([IVX]+|[A-Z])\.$/))){
      mode='heading';
      curHead={label:m[1],titles:[],page:ln.page,labelled:true};
      ln.kind='heading';
      headings.push(curHead);
      updateHeadingDisplay();
    } else {
      if(mode==='heading' && curHead){
        if(/^[a-z(]/.test(t) && curHead.titles.length){
          var lastT=curHead.titles[curHead.titles.length-1];
          curHead.titles[curHead.titles.length-1]=lastT+' '+t;
          repairs.push({page:ln.page,target:curHead.label,kind:'heading title joined from two lines',
            before:lastT+'  |  '+t, after:lastT+' '+t});
        } else {
          curHead.titles.push(t);
        }
        ln.kind='heading';
        updateHeadingDisplay();
      } else if(mode==='paragraph' && cur){
        cur.lines.push({text:t,page:ln.page});
        cur.pageEnd=ln.page;
        ln.kind='paragraph';
      } else {
        ln.kind='cover'; coverCount++;
      }
    }
  });

  function updateHeadingDisplay(){
    if(!curHead) return;
    curHead.display=curHead.label+(curHead.titles.length?' '+curHead.titles.join(' '):'');
    lastHeading=curHead.display;
    if(/^[IVX]+$/.test(curHead.label)) lastRoman=curHead.display;
  }
```

Hmm — wait, there's an issue: `updateHeadingDisplay` sets lastHeading to the labelled heading display. But when an unlabelled heading is found later, lastHeading = that. And when a paragraph starts, section=lastHeading. But what about a labelled heading with no title yet ("IV." alone, then paragraph)? display="IV." — fine.

But there's a subtle problem: the unlabelled heading look-back uses `cur.lines[cur.lines.length-1]===prev` — comparing object identity. prevNonEmpty returns the line object; cur.lines stores the same objects? In the paragraph branch I push `{text:t,page:ln.page}` — a NEW object, not ln itself! So identity fails. Fix: push ln itself and use ln.raw.trim() as text. Let me store lines as the ln objects: `cur.lines.push(ln)` and text = ln.raw.trim() when joining. But for the split case (number+text on one line), I create a synthetic line: `{raw:firstText, page:ln.page, kind:'paragraph', synthetic:true}`. Then identity works if I push the synthetic object. Let me restructure: cur.lines = array of line objects (either real ln or synthetic). Join: lines.map(l=>l.raw.trim()).join(' '). For synthetic, raw=firstText. OK.

Also pageEnd update after popping the heading line: recompute from remaining lines.

Also — the look-back condition `mode==='paragraph'`: but what if the previous non-empty line is the synthetic split line of the current paragraph? E.g., "23. Text" then "24." — prev is the synthetic line "Text..." — if it qualifies (≤90, capital, no terminal punct) it'd be misdetected as heading. Para 23's text is long (>90 chars) so no. OK.

Hmm, also: what if mode==='paragraph' but the previous non-empty line is NOT in cur.lines (e.g., it was a heading)? Can't happen — in paragraph mode all non-empty lines go to cur.lines... except the paragraph-start line itself (ln.kind='paragraph' but not pushed to lines). Wait — the paragraph-start line with number alone ("12.") is not added to cur.lines (only its number). The next paragraph-start's look-back: prev non-empty line is the last line of the previous paragraph — in cur.lines. But what if a paragraph consists ONLY of its number line (no text lines)? Then cur.lines is empty → look-back skipped (cur.lines.length check). But then prev non-empty would be... the previous paragraph's last line, which belongs to the previous cur, not current. My check `cur.lines[cur.lines.length-1]===prev` guards this. Good.

Wait, but there's another case: mode==='paragraph', cur.lines non-empty, prev is cur's last line — always true actually. Fine.

Now — hmm, one more: the unlabelled heading rule says "a non-empty line immediately followed by a paragraph-start line". My look-back skips blanks — "immediately followed" modulo blanks. OK.

Now paragraph text and marks:

```js
  var markCounter=1;
  var marksAll=[]; // {n, para}
  var rejected=[];
  paragraphs.forEach(function(p){
    var raw = p.lines.map(function(l){return l.raw.trim();}).join(' ').replace(/\s+/g,' ').trim();
    p.text_raw=raw;
    p.text_lines=p.lines.map(function(l){return l.raw;}); // original lines (raw, untrimmed?) 
```

Hmm — text_lines for CSV "lines separated by ' | '" — original lines. I'll use l.raw (original, maybe with trailing \r? split('\n') leaves \r if CRLF. I'll strip \r when splitting: split(/\r?\n/). Good — do that at the start.)

```js
    // marks
    var text=raw, out='', last=0, m;
    var re=/\d{1,3}/g;
    while((m=re.exec(raw))){
      var s=m.index, e=s+m[0].length;
      var pc=s>0?raw.charAt(s-1):'', nc=e<raw.length?raw.charAt(e):'';
      var bad=/[\d\/\-(]/.test(pc)||/[\d\/\-(]/.test(nc);
      if(bad) continue;
      var val=parseInt(m[0],10);
      if(val===markCounter){
        out+=raw.slice(last,s)+'['+val+']';
        last=e;
        markCounter++;
        p.marks.push(val); marksAll.push({n:val,para:p.number});
      } else {
        rejected.push({num:val,para:p.number,context:raw.slice(Math.max(0,s-25),s)+'⟨'+m[0]+'⟩'+raw.slice(e,e+25)});
      }
    }
    out+=raw.slice(last);
    p.text=out;
    // first words
    var clean=p.text.replace(/\[\d{1,3}\]/g,'');
    p.first_words_found=norm(clean).split(' ').slice(0,6).join(' ');
    var refFW = ref && ref.first_words ? ref.first_words[String(p.number)] : null;
    p.first_words_reference = refFW!=null? String(refFW): null;
    p.first_words_match = (p.first_words_reference==null)? null : (norm(p.first_words_found)===norm(p.first_words_reference));
    // pages
    if(p.pageStart!==p.pageEnd){
      repairs.push({page:p.pageStart+'–'+p.pageEnd,target:'para. '+p.number,kind:'paragraph joined across a page break',
        before:'page '+p.pageStart+' ends: …'+trunc(p.lines[p.lines.length-1].raw.trim(),40),
        after:'page '+p.pageEnd+' begins: '+trunc(p.lines[0].raw.trim(),40)+'…'});
    }
    p.citation=symbol+', para. '+p.number;
  });
```

Wait — the join repair should be logged once per paragraph spanning pages; but I'm logging inside the paragraphs.forEach — fine, but repairs order: "in document order" — the join repair for para spanning pages 3-4 would be logged during the marks loop, after heading repairs etc. Document order roughly OK. Hmm, but repairs are pushed in phases (page-level repairs during page loop, then body-walk repairs, then mark-phase repairs). "in document order" — I should sort repairs by page at the end? Pages are numeric; I'll sort repairs by page (numeric if possible) with a stable sort, keeping insertion order within a page. Let me give each repair a seq number and sort by (pageNum, seq). Page values like "3–4" for join repairs — parse first number. I'll store pageNum separately. Let me add `pg` numeric field to each repair and sort by pg then seq.

Hmm, actually simpler: log the join repair during the body walk (when the paragraph's pageEnd changes to a new page) — that's more "document order". Let me do it in the walk: when pushing a line to cur, if ln.page !== cur.pageEnd → log join repair (once per paragraph per page transition). Actually a paragraph could span 3 pages? Unlikely (43-254 words). I'll log when page changes: if cur.pageEnd !== ln.page and cur.lines.length>0 → log. But careful: the first line sets pageEnd. Let me handle: when pushing line, if cur.lines.length>0 && ln.page!==cur.pageEnd → log join. And pageStart = first line's page. Also the synthetic split line: page = ln.page. OK, move join logging into the walk.

Also paragraph repairs list: p.repairs — collect kinds of repairs with target 'para. n'. I'll filter repairs by target===('para. '+p.number) when rendering. Simpler: after all repairs, for each p, p.repairs = repairs.filter(r=>r.target==='para. '+p.number).map(r=>r.kind). 

Now footnotes cited: p.marks (numbers). footnotes_cited = p.marks.join('; ').

Now checks computation:

```js
  var numberedFns = footnotes.filter(f=>f.number!=='*');
  var fnNumbers = numberedFns.map(f=>f.number);
  // gaps/dups
  ...
```

Check details:

1. count: paragraphs.length vs ref.paragraphs.
2. numbering: expected 1..paragraphs.length; actual sequence; gaps = numbers in 1..n missing; dups = numbers appearing more than once. List "number x (page y)".
3. firstwords: matches count; mismatches list "para. n: found '…' / reference '…'".
4. footnotes: numberedFns.length vs ref.footnotes; sequence 1..len gaps/dups; restored list "footnote D (page p)".
5. marks: marksAll numbers; expected 1..ref.footnotes; missing = in 1..ref.footnotes not present; extra = present > ref.footnotes; rejected list with context.
6. leak: for each footnote, opener40 = norm((f.number==='*'? f.opener : (typeof f.number==='number'? f.number+' '+firstLineOfText : ...))). Hmm — "the first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…'; for a footnote whose number was displaced, its first line)". So for normal footnotes: the opener line (which includes the number) first 40 chars. For restored: its first line (the unnumbered line) first 40 chars. I stored f.opener = the raw opener line (trimmed). For restored, opener = the first text line (no number). So opener40 = norm(f.opener).slice(0,40). For normal footnotes, opener includes "15 Human Rights Committee..." — good. Search in each paragraph's norm(text_raw): `norm(p.text_raw).indexOf(opener40) !== -1` → hit. Count hits, list (footnote, para). Also paragraphs with word count > 300: `p.text_raw.split(/\s+/).length > 300`.
7. hf: headerOk count / pages; pageNum count (expected pages-1... "expected all but the first"); displaced list "number D on page p".
8. headings: labelled count, unlabelled count, list unlabelled displays.
9. lost: classify counts: iterate all pages' lines: kind counts for non-empty lines: cover/header/heading/paragraph/footnote/footer; total non-empty; unclassified = non-empty with kind null or 'blank'? blank lines have trim '' so they're empty. unclassified = lines with raw.trim()!=='' && (!kind || kind==='blank'). Sum check.

Wait — in the walk, blank lines get kind='blank' but they're empty (trim===''), so excluded from non-empty count. But in the page loop, footer blank lines also 'blank'. Header blank lines before header: kind stays null but they're empty. OK. So unclassified = non-empty lines with kind not in the six kinds. Should be 0.

Hmm — one problem: lines in the body that were skipped... in the walk every non-empty body line gets a kind (cover/heading/paragraph). Block lines get 'footnote'. Header/footer set. So all good.

Status per check: 'pass'/'fail'/'notrun' (notrun when ref missing for checks 1,3,4,5 partially). Check 5 needs ref.footnotes. Check 4 needs ref.footnotes. Check 1,3 need ref. Checks 2,6,7,8,9 don't need ref (check 6's expectation "0 hits" doesn't need ref; the >300 words listing doesn't need ref).

Now rendering. Let me write render functions.

State: `var selected=0;` docs parsed: `docs.forEach(d=> d.parsed = parseDoc(d.doc));`

renderHeader(): title, meta line, what sentence, check pill.
renderRail(): cards.
renderTabs(): panels content for selected doc.

I'll re-render panels on doc switch. Tabs themselves static (4 tabs), with red dot on tab 04 when failures.

Tab activation function `activateTab(i)`: update aria-selected, hidden on panels, focus.

Arrow keys: on tablist keydown: ArrowRight → activate (i+1)%4, focus; ArrowLeft → (i+3)%4; Home/End.

Panel 0 (RESULT) render:

```js
function renderResult(P){ // P = parsed
  var ref=P.ref;
  var tiles=[];
  var paraN=P.paragraphs.length, fnN=P.numberedFns.length;
  ...
}
```

Tile 1: label "PARAGRAPHS FOUND", big number paraN, side: ref? "The document has: "+ref.paragraphs : "no reference in this file". Status: equal → green "match"; else red "difference +x/−x". Plus if leak hits: red "n contain footnotes".
How: "Count of body lines that start a numbered paragraph (1–3 digits + '.') after headers, footers and footnote blocks were removed."

Tile 2: "FOOTNOTES FOUND", big "n of ref.footnotes" — big number fnN, side "of "+ref.footnotes. How: "Numbered openers in the page-foot blocks, plus numbers restored from page footers."

Tile 3: "FIRST WORDS MATCH", big matches+" of "+ref.paragraphs. How: "First six words of each paragraph against the reference, after normalising quotes, dashes and spaces."

Tile 4: "REPAIRS MADE", big repairs.length, link "open the repair log" → activate tab 3 + open repair log + scroll. How: "Every line, split, join or restoration the script made — listed with before and after on tab 04."

If ref missing: tiles 1-3 show "no reference in this file" instead of comparison.

Panel 1 (PARAGRAPHS):

```html
<button class="coll" aria-expanded="false" id="headingsBtn">Headings found: n</button>
<div id="headingsBox" hidden> list </div>
<table>
 <caption><span class="fig">TAB.01</span> 90 paragraphs found, 90 expected</caption>
 <thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>
 <tbody> rows... </tbody>
</table>
<p class="hint">Footnote marks are shown in square brackets, e.g. waste.[2]. Remove them with find-and-replace, pattern <code>\[\d+\]</code>.</p>
```

Row:
```html
<tr class="prow" data-i="0">
  <td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="det-0">12</button></td>
  <td class="sec">Right to work (art. 6)</td>
  <td class="num">3–4</td>
  <td class="firstline">…</td>
  <td class="chk ok">OK</td>
</tr>
<tr class="detail" id="det-0" hidden><td colspan="5"> ... </td></tr>
```

Row click: clicking anywhere on .prow toggles. Button handles keyboard.

Detail content:
```html
<div class="fulltext">…marked text…</div>
<button class="linesToggle" aria-expanded="false">Show the PDF's lines</button>
<div class="rawlines" hidden> per line: <div>[p. 3] line</div> ... </div>
<div class="fwcmp">Reference first words: "…" · Found: "…" — <span class="ok">equal</span></div>
<div class="meta2">Pages 3–4 · cites footnotes 2, 3 · repairs: paragraph joined across a page break</div>
<button class="copyBtn" data-cite="E/C.12/GC/27, para. 12">Copy citation</button>
```

Full path: if part && section && part!==section → "part › section" shown at top of detail as mono line.

Panel 2 (FOOTNOTES):

```html
<p class="lead">Footnotes found: n of m.</p> — actually caption in table.
<button download footnotes.csv>
<table><caption><span class="fig">TAB.02</span> n footnotes found, m expected</caption>
<thead>No. | Page | Text | Repair</thead>
rows: number (or *), page, text, repair ("number restored from the page foot" or "—")
</table>
```

Also note if '*' footnote exists: "The cover's asterisked note is kept as footnote * and is not counted."

Panel 3 (CHECKS & METHOD):

```html
<h2 class="sec-h">Checks</h2>
<div class="checks"> each check:
  <div class="check"><div class="cname">Paragraph count</div><div class="cdetail">Found 90; the reference says 90.</div><div class="cstatus pass">pass</div></div>
</div>
<button class="coll" aria-expanded="false" id="repairsBtn">Repair log (n)</button>
<div id="repairsBox" hidden>
  <p class="kinds">header line removed × 20 · footer line removed × 20 · …</p>
  <table><caption><span class="fig">TAB.03</span> n repairs, in document order</caption>
  <thead>Page | Paragraph or footnote | What was done | Before | After</thead> rows</table>
</div>
<button class="coll" aria-expanded="false" id="rawBtn">Raw pages</button>
<div id="rawBox" hidden>
  <label>Show raw page <select id="rawSel">…</select></label>
  <div class="legend"> swatches </div>
  <div class="rawpanel" id="rawPanel"></div>
</div>
<h2>Download</h2>
<button id="csvBtn">Download paragraphs as CSV</button>
<p class="hint">UTF-8 with BOM, every field quoted, CRLF line ends. File name: E-C.12-GC-27-paragraphs.csv</p>
```

Check line with links: e.g., first-words check links "para. 12" → button that activates tab 1, expands row, scrolls. I'll implement `goToPara(n)`.

Also "check failed" links to rows concerned — for leak check, link to flagged paragraphs.

Footer: `Source: ${doc.source} · built ${doc.built||'—'} · Counting, splitting and matching are done by this page's code; no model was called and nothing left the browser.` Hmm — "Source line, built date, and '...'". pdf_text may not have built; I'll show if present. Actually the general header rule says "one line with the data's source, n and years" — the plan's header covers that. Footer: source + built + honesty line. If no built, show "built —" or omit. I'll include `doc.built` only if present: `Source: …` + (built? ` · built ${built}` : '') + ` · Counting…`.

Hmm wait, the header meta already includes source. Footer repeats source line — fine per plan.

Now — the rail card:

```html
<button class="doccard selected" data-i="0">
  <div class="mono sym">E/C.12/GC/27</div>
  <div class="dtitle">General comment No. 27 (2025) …</div>
  <div class="dmeta">adopted … · 20 pages</div>
  <div class="bignum"><span class="big">90</span> <span class="of">of 90 paragraphs</span></div>
  <div class="bar"><div class="fill ok" style="width:100%"></div></div>
  <div class="bignum"><span class="big">141</span> <span class="of">of 141 footnotes</span></div>
  <div class="bar"><div class="fill" style="width:100%"></div></div>
  <div class="mono checks">9 of 9 checks pass →</div>
</button>
```

Bar fill: width = min(100, found/expected*100)%; class 'bad' (red) if found!==expected else 'ok' (ink). If no ref: show found only, bar full ink? I'll handle: if ref missing, "of —" and bar neutral.

Card click → select doc, re-render.

Now — sizes: paragraphs table with 90 rows + detail rows: fine.

Raw page viewer: select with 20 options; on change render lines. Each line: `<div class="rl"><span class="ln">n</span><span class="kc k-paragraph">P</span><span class="lt">text</span></div>`. Use textContent to avoid HTML issues — I'll build with DOM or escape. I'll use esc().

Legend: six items: swatch + letter + name: C cover, H header, T heading, P paragraph, F footnote, X footer. Plus red = unclassified.

Now CSV:

```js
function downloadCSV(filename, header, rows){
  var out='\ufeff';
  out+=header.map(csvQ).join(',')+'\r\n';
  rows.forEach(r=>{ out+=r.map(csvQ).join(',')+'\r\n'; });
  var blob=new Blob([out],{type:'text/csv;charset=utf-8'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob); a.download=filename;
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },500);
}
function csvQ(v){ return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'; }
```

Paragraph CSV rows: [number, section, part, page_start, page_end, first_words_reference||'', first_words_found, first_words_match===null?'not run':(first_words_match?'yes':'no'), text, text_raw, text_lines.join(' | '), footnotes_cited, repairs.join('; '), citation, symbol, doc_url].

Filename: symbol.replace(/\//g,'-')+'-paragraphs.csv'.

Footnotes CSV: header [number, page, text, repair, symbol, doc_url]; repair = repaired? 'number restored from the page foot' : ''.

Copy citation:

```js
function copyText(t, btn){
  function done(){ btn.textContent='Copied'; setTimeout(()=>btn.textContent='Copy citation',2000); }
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done, function(){fallback();}); }
  else fallback();
  function fallback(){ var ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy'); done();}catch(e){} ta.remove(); }
}
```

Now — event delegation: since panels re-render, I'll attach listeners after each render, or use delegation on document for clicks with data attributes. Delegation is cleaner:

```js
document.addEventListener('click', function(e){
  var t=e.target.closest('[data-action]');
  ...
});
```

Actions: tab (data-tab), doccard (data-doc), prow toggle (data-prow), headings toggle, repairs toggle (data-open-repairs), raw toggle, raw select change, csv download, footnotes csv, copy citation (data-cite), goToPara (data-goto), checkpill link (data-tab="3").

Let me use data-action attributes: `data-act="tab" data-i="0"`, `data-act="doc" data-i="0"`, `data-act="toggle-row" data-i="n"`, `data-act="toggle" data-target="id"`, `data-act="goto-para" data-n="12"`, `data-act="csv"`, `data-act="csv-fn"`, `data-act="copy" data-cite="…"`, `data-act="open-repairs"`.

For toggle buttons with aria-expanded: generic handler flips hidden on target and aria-expanded.

Now, one important detail: "the Repairs tile on tab 01 also opens" the repair log — so clicking the repairs tile: activate tab 3, set repairsBtn aria-expanded=true, show box, scroll into view.

Let me now also compute the "checks pass" pill: runChecks = checks.filter(status!=='notrun'); passCount. Pill: green dot + "n of m checks pass" or red dot + "k of m checks failed". And tab 04 gets a red dot span when failCount>0.

Now let me think about the "How this is computed" lines and hints — include per plan.

Also the header "what" sentence: "This page splits the converter's raw text into numbered paragraphs, removes headers, footers and footnotes, checks itself against the document's reference, and lists every repair it made."

Now — potential issue: `reference.first_words` keys — paragraph numbers as strings. If a paragraph number has no reference entry → first_words_reference null → match null → Check cell shows "no reference" (neutral). Check 3 counts matches of those with reference.

Now, let me also double-check the paragraph-start regex against heading labels: "A." matches label regex `/^([IVX]+|[A-Z])\.$/` — but ALSO... does "A." match paragraph-start `/^(\d{1,3})\.$/`? No (not digits). Good. But order: I check paragraph-start first, then label. "12." → paragraph. "A." → label. Good.

But wait — what about a line like "V." vs a paragraph "5."? Fine.

Hmm — one more: the label regex `[IVX]+` would match "I", "V", "X", "IV", "VI", "IX", "XI"... but also "XX", "XXX". And single [A-Z] matches any capital. But what about "B."? matches [A-Z]. OK.

Potential conflict: a paragraph line "X." — no, paragraphs are digits.

Now — the cover: lines before first paragraph start. On page 1, cover includes "I." and "Introduction"? Wait — "I." is a label line → mode='heading', so "I." and "Introduction" are headings, not cover. Cover = lines before "I.": "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) ... sustainable development*". Good — 7 cover lines.

Hmm wait — but the footnote block detection on page 1: scanning content lines for opener... "6 November 2025" starts with "6 " — nextFootnote=1 → no match. But what about... the title line "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development*" — starts with "General" — no. OK. And "* Adopted by..." — if it's in the footnote area, block starts there (page===firstPage && starts with "* "). But if the asterisk note is at the very end of page 1 after footnotes... then block starts at footnote 1's opener "1 ..." — wait, is there a line starting with "1 "? Footnote 1 on page 1: probably "1 See ..." or bare "1" then text. Either matches. Good.

Hmm — but WAIT. A critical issue: on page 1, is there any body line starting with "1 " BEFORE the footnote block? Like a wrapped line "1 something"? The cover title wraps: "General comment No. 27 (2025) on economic, social and\ncultural rights and the environmental dimension of\nsustainable development*" — continuation lines start with "cultural", "sustainable". OK. Paragraph text lines could start with "1 "? E.g., a line "1.5 million"? starts with "1." — no. "1 000"? Hmm, UN documents write "1 million"... A wrapped line starting with "1 " is possible in theory. The spec's rule accepts this. Proceed.

Another critical check — the block-start search happens per page with the running nextFootnote. On page 2, nextFootnote=5 (if page 1 had 1-4). Page 2 body: paragraphs continue; footnote block at foot: "5", blank, "A/79/270...", "A/42/427...", "7 ..."? wait — page 2's footnotes: 5, 6(displaced), maybe 7, 8. Block starts at bare "5" == nextFootnote. 

But hmm — what if page 2's body contains a line starting with "5 " before the footnote block? E.g., paragraph text "5.2 billion"? starts with "5." no. "5 countries"? possible... risk accepted.

Now — the jump rule: "If no line on a page opens nextFootnote, take the first bare number greater than it". When would this happen? If a page's first footnote number was skipped... e.g., if the displaced number is the page's first footnote — then no line opens nextFootnote (the first footnote has no number), and the jump rule finds the next bare number > nextFootnote (the second footnote's number, if bare) — but spec says displaced is always second. The jump rule is a safety net. OK.

Now — an important question: after the block is removed, body lines from ALL pages concatenated — but I do the walk after all pages processed. bodyAll is in page order. Good.

Now — the "Nothing lost" check: count kinds across all pages' lines. Note: lines in the block are 'footnote'; body lines got kinds in walk; header/footer set; blanks 'blank' or null (empty). Non-empty = raw.trim()!==''. Sum of six kinds should equal total non-empty. 

Wait — one problem: in the page loop, blank lines BEFORE the header (i=0 while loop) — kind stays null, but they're empty → not counted. Blank lines in footer loop get 'blank'. Blank lines in content: in the walk, `if(t===''){ln.kind='blank';return;}` — but block lines: I set ln.kind='footnote' BEFORE checking blank — so blank lines inside the block get 'footnote' but they're empty → not counted in non-empty. Fine.

Hmm wait, in the block parser I do `ln.kind='footnote'; if(t==='') return;` — blank block lines marked footnote but empty. OK.

Now — the raw viewer: show ALL lines of the selected page with kinds. Blank lines: kind 'blank' or null → render with no tint. Unclassified (non-empty, no kind): red tint + '?' code. Should be none.

Now let me also compute per-paragraph "repairs" for the detail row: filter repairs where target === 'para. '+number. Also footnote repairs target 'footnote n'. Header/footer target '—'.

Repair log "Paragraph or footnote" column: target.

Now — counts per kind above repair table: group repairs by kind, order of first appearance: "header line removed ×20 · footer line removed ×20 · footnote block removed ×20 · number and text split ×2 · heading separated ×23 · heading title joined ×n · paragraph joined across a page break ×19 · footnote number restored ×12". Render as mono line with wrapping.

Now — the checks panel content. Let me write each check's detail HTML:

1. Paragraph count: `Found <b>90</b> numbered paragraphs; the reference says <b>90</b>.` status pass. Link: "see the paragraphs" → tab 1.
2. Numbering: `Numbers run 1–90 in order, no gaps, no duplicates.` or list issues: `Gaps: 12 (page 4); duplicates: 7 (page 3).` status fail if issues.
3. First words: `90 of 90 match.` or `88 of 90 match. Mismatches: para. 23: found "…" / reference "…"; …` each mismatch a link data-act="goto-para". status fail if any mismatch (among those with reference).
4. Footnotes: `Found 141 numbered footnotes; the reference says 141. Numbers run 1–141 without a gap or duplicate. Restored from page footers: 6 (page 2), 14 (page 5), …` status.
5. Footnote marks: `Marks in the paragraph text run 1–141 without a gap. Rejected as not marks (with context): article ⟨11⟩ (para. 6): "…article 11…"; …` status pass if sequence complete. Missing listed.
6. Footnotes stay out of the paragraphs: `0 of 141 footnote openers appear in any paragraph text (expected 0). Paragraphs over 300 words: none (longest 254).` status pass. If hits: list "footnote 15 opener found in para. 6" with goto link; tile 1 shows "n contain footnotes".
7. Headers and footers: `20 of 20 pages begin with the symbol. 19 of 20 pages carry their page number in the footer (all but the first expected). Displaced footnote numbers kept aside: 6 (page 2), …` status pass if headerOk===pages && pageNum===pages-1 (first page exempt) — hmm, "expected all but the first": pageNum count should be pages-1. But what if firstPage !== 1? Use records[0].page as first. status pass if headerOk===pages.length && pageNumCount===pages.length-1 && displaced handled (displaced are fine, they're restored). Also pageNotes (no block) listed.
8. Headings: `23 labelled headings (I., A., …) and 23 unlabelled headings found: "Right to work (art. 6)", "Children", …` status pass (informational). Hmm — make it fail if zero headings? I'll pass if headings.length>0.
9. Nothing lost: `Every non-empty line is classified exactly once: cover 7, header 20, heading 46, paragraph 312, footnote 289, footer 41 = 715 of 715 non-empty lines. Unclassified: none.` status pass if equal.

Wait — heading count: labelled headings count = headings.filter(labelled).length; unlabelled = rest. But note: each labelled heading is one entry (with titles). Unlabelled entries pushed individually. OK.

Now — the marks check "expected to run from 1 to reference.footnotes" — if ref missing, compare to max mark? I'll say notrun if no ref.footnotes.

Now, tile 3 "First words match: n of reference.paragraphs" — n = matches among paragraphs with reference. If ref missing → "no reference in this file".

Now — let me also handle the "n contain footnotes" on tile 1: leakHits paragraphs count.

Now, rendering performance: fine.

Let me now also think about the tab labels with the red dot: `<button role="tab" ...>04 CHECKS & METHOD<span class="dot" hidden></span></button>`.

Now — writing all of this compactly but completely. Let me estimate lines: CSS ~200, HTML skeleton ~60, JS ~600-700. Under 1500. Good.

Let me write the final code now, carefully.

One more design consideration: the layout — header, then a flex row: rail (fixed 250px) + main. Tabs sticky? Not needed. Footer at bottom.

Also "Works on a laptop screen without horizontal scrolling": set max-width 1200px, rail 240px, main flexible; tables with `table-layout:fixed`? First line column flexible. I'll give th widths: No. 6%, Section 18%, Page 8%, First line 56%, Check 12%. Section cell can wrap. Add `overflow-wrap:anywhere` for long text? Use `word-break:break-word` on cells.

Font sizes: body 16px; table 14px maybe — spec says 16px for tables... "the system sans-serif at 16px for body text and tables". OK keep 15-16px; with the widths above it should fit in ~900px main. First line 120 chars at 16px ≈ 900px — too wide; it wraps (it's a cell, wraps fine). OK.

Detail row: colspan 5, background slightly different? Keep paper, with left red border? "Details open in place". I'll style detail td with border-left 3px red? Hmm, accent usage: red for active tab, selected filters, paragraph numbers, share bars, "first words differ", "check failed". Detail rows: keep neutral with a thin left rule. Fine.

Now — the "Show the PDF's lines" toggle: reveals lines with page markers. Render: for each line in p.lines: if line.page !== previousLine.page → insert marker `<div class="pagemark">— page 3 —</div>`. Then `<div class="pline">text</div>` in monospace.

Wait — p.lines includes the synthetic split line (raw=firstText). Its page = ln.page. Fine.

Also — the expanded row shows "the page(s)": "Pages 3–4" or "Page 3".

Copy citation button: data-cite = p.citation.

Now — goto-para: activate tab 1 (index 1), expand row for para n, scroll to it. Need row element id: `prow-<n>`? Rows indexed by paragraph number — I'll set id on the tr: `id="prow-"+p.number`. Detail id `det-"+p.number`.

Toggle row function: find tr.prow[data-n], button inside, detail row; flip.

Now — the headings collapsible box: list all headings: labelled (display) and unlabelled. Render as a simple list with mono markers "L"/"U"? I'll show: `I. Introduction` etc., with unlabelled ones marked. Simple `<ul>`.

Now — the raw pages select: options "page 1".."page 20" with value=page. On change render. Default first page.

Raw panel line rendering: build HTML string with esc(). Line numbers: index+1.

Legend: 
```
<span class="sw k-cover"></span>C cover · <span class="sw k-header"></span>H header · <span class="sw k-heading"></span>T heading · <span class="sw k-paragraph"></span>P paragraph · <span class="sw k-footnote"></span>F footnote · <span class="sw k-footer"></span>X footer · red = unclassified
```

Now — the checks panel: each check as a row: name (sans 15px, weight 600), detail (14px), status pill (mono, green/red). One line each — "every check on one line" — I'll keep detail concise on one line where possible, with links inline. For long lists (rejected numbers), put in a scrollable sub-box (max-height 120px, overflow auto) — still "one line" for the check header. Acceptable.

Now — writing the checks with links: for goto-para links: `<button class="link" data-act="goto-para" data-n="23">para. 23</button>`.

OK — also the header pill: `<button class="pill" data-act="tab" data-i="3"><span class="dot green"></span> 9 of 9 checks pass</button>` or red: "2 checks failed".

Now — one more thing: the plan says tab 01 has "Five things to click: four tabs and the repair-log link." — so tiles shouldn't have other clickable things. OK — tile 4's number is the link.

Tab 04: "Seven things to click: four tabs, the repair log and raw pages headings, and the download (the select appears once 'Raw pages' is open)." — so tab 04 has: repair log heading, raw pages heading, download button = 3 + 4 tabs = 7. The check panel links (goto-para) would add clicks... hmm, "No view shows more than about seven things to click" — the check links are inline links within check lines; the plan itself says checks have "a link to the rows concerned". The count is approximate ("about seven"). I'll keep check links but they're small inline links; acceptable given the plan explicitly asks for them.

Now — let me also make sure: "the tab panel of a hidden tab is not focusable" — hidden attribute handles.

Let me now write out the whole file. I'll be careful with regexes in JS string literals inside HTML — no `</script>` sequences. The pattern `\[\d+\]` in hint text — fine.

Also careful: in the hint, showing `\[\d+\]` — in HTML: `<code>\[\d+\]</code>` — backslash fine.

Let me write the JS parse function completely and correctly now, mentally compiling.

Also: `records` may have `count` as string "20" — ignore, use records.length.

Edge: `doc.doc_url` may be missing → link omitted.

Let me define parseDoc returning P with: symbol, doc, ref, pages, footnotes (all incl '*'), numberedFns, paragraphs, headings, repairs, checks, counts, pageNotes, hyphenLines, coverCount, kindCounts, totalNonEmpty, unclassified.

Let me write it:

```js
function parseDoc(doc){
  var symbol=doc.symbol||'';
  var ref=(doc.reference && typeof doc.reference==='object')?doc.reference:null;
  var records=(doc.records||[]).slice().sort(function(a,b){return (a.page||0)-(b.page||0);});
  var firstPage=records.length?records[0].page:null;
  var P={doc:doc,symbol:symbol,ref:ref,pages:[],footnotes:[],paragraphs:[],headings:[],repairs:[],pageNotes:[],hyphenLines:0};
  var nextFootnote=1;
  var bodyAll=[];
  var seq=0;

  function addRepair(page,target,kind,before,after){
    P.repairs.push({seq:seq++,pg:typeof page==='number'?page:(parseInt(page,10)||0),page:page,target:target,kind:kind,before:before,after:after});
  }

  records.forEach(function(rec){
    var page=rec.page;
    var rawLines=String(rec.text==null?'':rec.text).split(/\r?\n/);
    var lines=rawLines.map(function(r){return {raw:r,kind:null,page:page};});
    var pg={page:page,lines:lines,headerOk:false,pageNum:false,displaced:null,hasBlock:false,jump:null};
    P.pages.push(pg);
    var i=0;
    while(i<lines.length && lines[i].raw.trim()==='') i++;
    if(i<lines.length && lines[i].raw.trim()===symbol){
      lines[i].kind='header'; pg.headerOk=true;
      addRepair(page,'—','header line removed',lines[i].raw.trim(),'removed');
      i++;
    } else if(i<lines.length){
      P.pageNotes.push('page '+page+': the first non-empty line is not the symbol');
    }
    var j=lines.length-1, foot=[];
    while(j>=i){
      var t=lines[j].raw.trim();
      if(t===''){ lines[j].kind='blank'; j--; continue; }
      if(t.indexOf('GE.')===0){ foot.push(lines[j]); j--; continue; }
      if(/^\d{6}(\s+\d{6})*$/.test(t)){ foot.push(lines[j]); j--; continue; }
      if(/^\d{1,3}$/.test(t)){
        var n=parseInt(t,10);
        if(n===page) pg.pageNum=true; else pg.displaced=n;
        foot.push(lines[j]); j--; continue;
      }
      break;
    }
    if(foot.length){
      foot.forEach(function(l){ l.kind='footer'; });
      addRepair(page,'—','footer line removed',
        foot.map(function(l){return l.raw.trim();}).join('  /  '),
        'removed'+(pg.displaced!=null?' — the number '+pg.displaced+' was kept aside as a displaced footnote number':''));
    }
    var content=lines.slice(i,j+1);
    var blockStart=-1, jump=null, k, ct;
    for(k=0;k<content.length;k++){
      ct=content[k].raw.trim();
      if(/^\d{1,3}$/.test(ct) && parseInt(ct,10)===nextFootnote){ blockStart=k; break; }
      if(ct.indexOf(nextFootnote+' ')===0){ blockStart=k; break; }
      if(page===firstPage && ct.indexOf('* ' )===0){ blockStart=k; break; }
    }
    if(blockStart===-1){
      for(k=0;k<content.length;k++){
        ct=content[k].raw.trim();
        if(/^\d{1,3}$/.test(ct) && parseInt(ct,10)>nextFootnote){ blockStart=k; jump=parseInt(ct,10); break; }
      }
    }
    var body, block;
    if(blockStart===-1){ body=content; block=[]; P.pageNotes.push('page '+page+': no footnote block found — the whole page is body'); }
    else { body=content.slice(0,blockStart); block=content.slice(blockStart); pg.hasBlock=true; pg.jump=jump; }
    if(block.length){
      addRepair(page,'—','footnote block removed', trunc(block[0].raw.trim(),60),
        'moved to the footnotes ('+block.length+' lines)'+(jump!=null?' — the block starts at footnote '+jump+' where '+nextFootnote+' was expected; jump logged':''));
    }
    var cur=null, firstFn=null, firstClosed=false, highest=0;
    block.forEach(function(ln){
      var t=ln.raw.trim();
      ln.kind='footnote';
      if(t==='') return;
      var m;
      if(t.indexOf('* ' )===0){
        cur={number:'*',page:page,text:t.slice(2),repaired:false,opener:t};
        P.footnotes.push(cur); if(!firstFn) firstFn=cur;
        return;
      }
      if((m=t.match(/^(\d{1,3})$/))){
        cur={number:parseInt(m[1],10),page:page,text:'',repaired:false,opener:t};
        P.footnotes.push(cur); if(!firstFn) firstFn=cur; if(cur.number>highest)highest=cur.number;
        return;
      }
      if((m=t.match(/^(\d{1,3}) (.+)$/))){
        cur={number:parseInt(m[1],10),page:page,text:m[2],repaired:false,opener:t};
        P.footnotes.push(cur); if(!firstFn) firstFn=cur; if(cur.number>highest)highest=cur.number;
        if(cur===firstFn && pg.displaced!=null && m[2].charAt(m[2].length-1)==='.') firstClosed=true;
        return;
      }
      if(pg.displaced!=null && firstFn && cur===firstFn && firstClosed){
        cur={number:pg.displaced,page:page,text:t,repaired:true,opener:t};
        P.footnotes.push(cur); if(cur.number>highest)highest=cur.number;
        addRepair(page,'footnote '+pg.displaced,'footnote number restored',trunc(t,60),pg.displaced+' '+trunc(t,60));
        return;
      }
      if(cur){
        cur.text=(cur.text?cur.text+' ':'')+t;
        if(cur===firstFn && pg.displaced!=null && !firstClosed && t.charAt(t.length-1)==='.') firstClosed=true;
      }
    });
    if(pg.displaced!=null && pg.displaced>highest) highest=pg.displaced;
    if(highest>=nextFootnote) nextFootnote=highest+1;
    body.forEach(function(ln){ bodyAll.push(ln); });
  });
```

Hmm wait — `if(highest>=nextFootnote) nextFootnote=highest+1;` — spec: "Advance nextFootnote past the highest number seen in the block and past any displaced number". If highest < nextFootnote (no block or low numbers), keep nextFootnote. OK.

Hmm — but there's an issue: what if the block contains a number LOWER than nextFootnote (out of order)? highest might be < nextFootnote → nextFootnote unchanged. Fine.

Now the body walk:

```js
  var mode='cover', cur=null, curHead=null, lastHeading='', lastRoman='';
  function prevNonEmpty(idx){ for(var x=idx-1;x>=0;x--){ if(bodyAll[x].raw.trim()!=='') return bodyAll[x]; } return null; }
  function headDisplay(){
    if(!curHead) return;
    curHead.display=curHead.label+(curHead.titles.length?' '+curHead.titles.join(' '):'');
    lastHeading=curHead.display;
    if(/^[IVX]+$/.test(curHead.label)) lastRoman=curHead.display;
  }
  bodyAll.forEach(function(ln,idx){
    var t=ln.raw.trim();
    if(t===''){ ln.kind='blank'; return; }
    if(/\-$/.test(ln.raw)) P.hyphenLines++;
    var m;
    if((m=t.match(/^(\d{1,3})\.$/)) || (m=t.match(/^(\d{1,3})\. (.+)$/))){
      var num=parseInt(m[1],10), firstText=m[2]||'';
      if(mode==='paragraph' && cur && cur.lines.length){
        var prev=prevNonEmpty(idx);
        if(prev && cur.lines[cur.lines.length-1]===prev){
          var pt=prev.raw.trim();
          if(pt.length<=90 && /^[A-Z\u00C0-\u00DE]/.test(pt) && !/[.;:,\d]$/.test(pt)){
            cur.lines.pop();
            prev.kind='heading';
            P.headings.push({display:pt,labelled:false,page:prev.page});
            lastHeading=pt;
            addRepair(prev.page,'para. '+num,'heading separated',pt+' — would have joined para. '+cur.number+' above','kept as a heading');
            if(cur.lines.length) cur.pageEnd=cur.lines[cur.lines.length-1].page; else cur.pageEnd=cur.pageStart;
          }
        }
      }
      if(firstText){
        addRepair(ln.page,'para. '+num,'number and text split',trunc(t,70),num+'.  →  '+trunc(firstText,60));
        cur={number:num,lines:[{raw:firstText,page:ln.page,kind:'paragraph',synthetic:true}],pageStart:ln.page,pageEnd:ln.page,section:lastHeading,part:lastRoman,marks:[]};
      } else {
        cur={number:num,lines:[],pageStart:ln.page,pageEnd:ln.page,section:lastHeading,part:lastRoman,marks:[]};
      }
      ln.kind='paragraph';
      P.paragraphs.push(cur);
      mode='paragraph';
    } else if((m=t.match(/^([IVX]+|[A-Z])\.$/))){
      mode='heading';
      curHead={label:m[1],titles:[],page:ln.page,labelled:true};
      ln.kind='heading';
      P.headings.push(curHead);
      headDisplay();
    } else if(mode==='heading' && curHead){
      if(/^[a-z(]/.test(t) && curHead.titles.length){
        var lastT=curHead.titles[curHead.titles.length-1];
        curHead.titles[curHead.titles.length-1]=lastT+' '+t;
        addRepair(ln.page,curHead.label,'heading title joined from two lines',lastT+'  |  '+t,lastT+' '+t);
      } else {
        curHead.titles.push(t);
      }
      ln.kind='heading';
      headDisplay();
    } else if(mode==='paragraph' && cur){
      if(cur.lines.length && ln.page!==cur.pageEnd){
        addRepair(ln.page,'para. '+cur.number,'paragraph joined across a page break',
          'page '+cur.pageEnd+' ends: …'+trunc(cur.lines[cur.lines.length-1].raw.trim(),40),
          'page '+ln.page+' begins: '+trunc(t,40)+'…');
      }
      cur.lines.push(ln);
      cur.pageEnd=ln.page;
      ln.kind='paragraph';
    } else {
      ln.kind='cover';
    }
  });
```

Wait — bug: in the paragraph-start branch, when firstText exists I create cur with the synthetic line, but I don't push ln itself... ln.kind='paragraph' set. Good. But the synthetic line's raw = firstText — for text_lines CSV, the synthetic line represents the text after the number. OK.

Hmm — also the join repair: when a paragraph's line is on a new page. But the FIRST line of a paragraph sets pageStart; if the paragraph-start line itself is on a new page relative to previous paragraph — that's not a join (different paragraph). My condition `cur.lines.length && ln.page!==cur.pageEnd` — only when adding continuation lines. But the synthetic first line: pageStart=pageEnd=ln.page. Then continuation on next page → join logged. Good. But what if the paragraph-start line (number alone) is on page 3 and its first text line on page 4? The number line isn't in cur.lines; the first continuation line: cur.lines.length===0 → no join logged, pageEnd updated to 4, pageStart stays 3 → pageStart!==pageEnd → but no repair logged. Hmm — I should log the join whenever pageStart!==pageEnd at the end. Let me instead, after the walk, for each paragraph with pageStart!==pageEnd, ensure a join repair exists. Simpler: after walk, for each p, if p.pageStart!==p.pageEnd and no join repair logged for it, add one. Or: log join in the walk when `ln.page!==cur.pageEnd` regardless of lines.length, but only if cur.lines.length>0 OR... hmm. Let me just do post-walk: for each p with pageStart!==pageEnd, addRepair once (if not already). To avoid duplicates, track p.joined flag. Actually simplest: remove the in-walk join logging and do it post-walk:

```js
  P.paragraphs.forEach(function(p){
    if(p.pageStart!==p.pageEnd){
      addRepair(p.pageEnd,'para. '+p.number,'paragraph joined across a page break',
        'page '+p.pageStart+' ends: …'+trunc(lastLineOfPage(p,p.pageStart).raw.trim(),40),
        'page '+p.pageEnd+' begins: '+trunc(p.lines[0].raw.trim(),40)+'…');
    }
  });
```

Hmm, before/after: better: before = last line on pageStart, after = first line on pageEnd. Let me compute: lines on pageStart = p.lines.filter(l=>l.page===p.pageStart); last of those. lines on pageEnd: first. OK. But repairs order — post-walk repairs come after walk repairs; sorting by pg at the end fixes order. I'll sort P.repairs by (pg, seq) when rendering. Good — then I can log joins post-walk.

Actually wait — the in-walk join logging I wrote logs when page changes mid-paragraph, which is the same event. But the case where the number line is on page 3 and text starts page 4 — pageStart=3 (number line page), first line page 4. Post-walk check catches it. Let me drop the in-walk join and do post-walk only. But careful: pageStart is set from the paragraph-start line's page (ln.page), even if no lines yet. If paragraph has number on page 3 and all text on page 4 → pageStart=3, pageEnd=4 → join logged. Good.

Hmm, but also: what if the paragraph-start line is on page 3, text on page 3, more text on page 4 → pageStart=3, pageEnd=4 → logged once. Good.

Now marks & first words (post-walk):

```js
  var markCounter=1;
  P.marksAll=[]; P.rejected=[];
  P.paragraphs.forEach(function(p){
    var raw=p.lines.map(function(l){return l.raw.trim();}).join(' ').replace(/\s+/g,' ').trim();
    p.text_raw=raw;
    p.text_lines=p.lines.map(function(l){return l.raw.replace(/\s+/g,' ').trim();});
    var out='', last=0, m, re=/\d{1,3}/g;
    while((m=re.exec(raw))){
      var s=m.index, e=s+m[0].length;
      var pc=s>0?raw.charAt(s-1):'', nc=e<raw.length?raw.charAt(e):'';
      if(/[\d\/\-(]/.test(pc) || /[\d\/\-(]/.test(nc)) continue;
      var val=parseInt(m[0],10);
      if(val===markCounter){
        out+=raw.slice(last,s)+'['+val+']'; last=e; markCounter++;
        p.marks.push(val); P.marksAll.push(val);
      } else {
        P.rejected.push({num:val,para:p.number,context:raw.slice(Math.max(0,s-28),s)+'⟨'+m[0]+'⟩'+raw.slice(e,e+28)});
      }
    }
    out+=raw.slice(last);
    p.text=out;
    var clean=out.replace(/\[\d{1,3}\]/g,' ');
    p.first_words_found=norm(clean).split(' ').filter(Boolean).slice(0,6).join(' ');
    var rfw=(ref&&ref.first_words)?ref.first_words[String(p.number)]:null;
    p.first_words_reference=(rfw==null)?null:String(rfw);
    p.first_words_match=(p.first_words_reference==null)?null:(norm(p.first_words_found)===norm(p.first_words_reference));
    p.citation=symbol+', para. '+p.number;
    p.repairs=P.repairs.filter(function(r){return r.target==='para. '+p.number;}).map(function(r){return r.kind;});
  });
```

Wait — the bad-char regex `/[\d\/\-(]/` — inside a character class, `\-` is a literal hyphen, `(` literal. So class = digit, '/', '-', '('. Good. But careful: `pc` could be '' (start) — `/.../.test('')` is false → not blocked. Good.

Hmm — one issue: `norm(clean).split(' ')` — norm collapses whitespace; if clean starts with space (mark at start?) — norm trims. filter(Boolean) guards empty. OK.

Wait, another subtlety: first_words_found should be "the first six whitespace-separated words of the joined text, footnote marks removed first". If a mark is among the first six words, removing it changes the words. E.g., "waste.2 The Committee" → removing mark → "waste. The Committee" → first six words include "waste." — matches reference presumably. Good.

Now checks:

```js
  P.numberedFns=P.footnotes.filter(function(f){return f.number!=='*';});
  // sort footnotes by document order? They're pushed in page order already. But within a page, order of opening. Fine.
```

Hmm — footnotes order: pushed per page in block order. The displaced one is pushed when encountered (second). So order is document order. Good.

```js
  var refP = ref? ref.paragraphs : null;
  var refF = ref? ref.footnotes : null;
  var checks=[];
  // 1 count
  checks.push({name:'Paragraph count', status: refP==null?'notrun':(P.paragraphs.length===refP?'pass':'fail'),
    detail: 'Found '+P.paragraphs.length+' numbered paragraphs'+(refP==null?' — no reference in this file.':'')+'; the reference says '+refP+'.',
    link:{act:'tab',i:1,label:'see the paragraphs'}});
```

Hmm, let me structure detail as HTML string built with helpers. I'll write them inline.

Check 2 numbering:
```js
  var nums=P.paragraphs.map(function(p){return p.number;});
  var gaps=[],dups=[];
  var seen={};
  nums.forEach(function(n){ if(seen[n]) dups.push(n); seen[n]=true; });
  for(var n=1;n<=nums.length;n++) if(!seen[n]) gaps.push(n);
  // also numbers beyond length? if max>length they're dups/gaps handled
```
Hmm — numbering check: "The paragraph numbers are exactly 1 to n in order; gaps and duplicates are listed by number and page." So expected sequence 1..n where n=found count. gaps = missing in 1..n; dups = repeated. Also if numbers not in order (e.g., 1,2,4,3)? "exactly 1 to n in order" — check sorted equality: nums.join() === [1..n].join(). I'll compute inOrder = nums.every((v,i)=>v===i+1). If not, list issues. Detail: 'Numbers run 1–'+n+' in order, no gaps or duplicates.' or 'Not in order: …; gaps: …; duplicates: … (page …)'.

Check 3 first words:
```js
  var withRef=P.paragraphs.filter(p=>p.first_words_reference!=null);
  var mism=withRef.filter(p=>!p.first_words_match);
  detail: withRef.length+' of '+ (refP!=null?refP:P.paragraphs.length) +' match.' + mismatches list with goto links.
```
Hmm — "First words match: n of reference.paragraphs" on tile. n = withRef.length - mism.length. If ref missing → notrun.

Check 4 footnotes:
```js
  var fnNums=P.numberedFns.map(f=>f.number);
  var fnGaps=[],fnDups=[]; seen={};
  fnNums.forEach(...); for n=1..fnNums.length if !seen gaps.
  var restored=P.numberedFns.filter(f=>f.repaired);
  detail: 'Found X numbered footnotes; the reference says Y. Numbers run 1–X without gap or duplicate. Restored from page footers: 6 (page 2), …'
  status: refF==null?'notrun':(X===refF && no gaps/dups ? 'pass':'fail')
```

Check 5 marks:
```js
  var marks=P.marksAll;
  var maxMark=marks.length?marks[marks.length-1]:0; // marks are sequential by construction (counter), so marks = [1..k]. Actually since counter increments only on match, marksAll is exactly 1..k. So no gaps possible! Hmm.
```
Wait — marksAll is [1,2,...,k] by construction (counter). So "marks found run 1 to k without a gap" is trivially true; the real check is k === ref.footnotes. And missing = numbers in 1..refF not in marks → if k<refF, missing = k+1..refF. And rejected list. So check: status pass iff refF!=null && k===refF. Detail: 'Marks in the paragraph text run 1–'+k+' (the counter only advances on a match). Expected 1–'+refF+'. Missing: … Rejected as not marks: ⟨11⟩ in para. 6 "…article 11…", …' — list rejected (maybe cap display at 30 with "and n more" in a scroll box).

Check 6 leak:
```js
  var hits=[];
  P.numberedFns.forEach(function(f){
    var op=norm(f.opener).slice(0,40);
    if(!op) return;
    P.paragraphs.forEach(function(p){
      if(norm(p.text_raw).indexOf(op)!==-1) hits.push({fn:f.number,para:p.number});
    });
  });
  var longP=P.paragraphs.filter(p=>p.text_raw.split(/\s+/).length>300);
  status: hits.length===0 && longP.length===0 ? 'pass':'fail';
  detail: hits.length+' of '+P.numberedFns.length+' footnote openers appear inside paragraph text (expected 0). Paragraphs over 300 words: '+ (longP.length? list with links : 'none (longest '+maxWords+')') +'.'
```
Hmm — the '*' footnote opener: skip (number '*'). Also for restored footnotes, opener = first text line (no number) — per spec "for a footnote whose number was displaced, its first line". Good — f.opener for restored is the unnumbered line. 

Wait — for normal footnotes opened by bare number, opener = "5" — first 40 chars = "5" — searching "5" in paragraph text would hit constantly! Hmm. "the first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…'...)" — the example shows a "N text" opener. For bare-number openers, the opener line is just "5" — searching "5" would false-positive. Hmm. But wait — in this document, are footnote openers bare numbers or "N text"? Spec: "The first on a page is a bare number on its own line, a blank line, then the text; the others are '7 E/2003/22…'". So the first footnote on each page has a bare-number opener — its "opener line" is just the number. Searching "5" in paragraphs → hits. That would make the check fail wrongly.

Hmm. Let me re-read: "the first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…'; for a footnote whose number was displaced, its first line), are searched in the raw text of every paragraph". Maybe for bare-number openers, the "line that opens the footnote" should be understood as the number + following text line? Or maybe I should use the opener line PLUS the first text line? The example "15 Human Rights Committee, general comm…" is a "N text" opener. For a bare-number opener, the meaningful searchable string is the number + first text line, e.g., "5 A/79/270, paras. 84 and 85." Hmm.

To be safe and useful: build the search string as: if opener is bare number, use `number + ' ' + first 40 chars of text`? Or just use the first 40 chars of (opener + ' ' + text)? Let me define: searchStr = norm(f.opener + (f.text? ' '+f.text : '')).slice(0,40). For "15 Human Rights Committee, general comment…" → "15 Human Rights Committee, general comm" (matches example). For bare "5" with text "A/79/270, paras. 84 and 85." → "5 A/79/270, paras. 84 and 85." — 40 chars. For restored (displaced) footnote: opener is the unnumbered first line, text = same line → searchStr = norm(opener+' '+text).slice(0,40) would duplicate. Hmm — for restored, f.opener === first line and f.text === same → opener+' '+text duplicates. Let me instead store f.search = the line(s): for normal: opener line if it has text beyond the number, else number + ' ' + first text line... 

Simpler: store `f.searchLine` at parse time: for "N text" openers → the whole line; for bare-number openers → the number + ' ' + the first following non-empty line (i.e., when the first text line is appended, if opener was bare, set f.searchLine = number + ' ' + that line); for restored → the unnumbered line; for '*' → skip. Then searchStr = norm(f.searchLine).slice(0,40).

Let me implement: when opening a footnote with bare number, set `cur.searchLine = m[1]` initially; when the first text line is appended to a footnote whose searchLine is just the number, update searchLine = number + ' ' + t. Hmm — but the displaced case: first footnote bare "5", text "A/79/270..." — searchLine becomes "5 A/79/270, paras. 84 and 85.". Good. For "N text" openers, searchLine = t (whole line). For restored, searchLine = t. For '*', searchLine = null (skip).

Actually simpler: after parsing each footnote, compute searchLine = (opener is bare number) ? (number + ' ' + text) : opener. Since text for bare-number footnotes is the following lines. But if text empty → just number → skip (too short). Let me do post-processing:

```js
  P.footnotes.forEach(function(f){
    if(f.number==='*'){ f.search=null; return; }
    var op=f.opener;
    if(/^\d{1,3}$/.test(op)) f.search=(f.number+' '+f.text).trim();
    else f.search=op;
  });
```
Then searchStr = norm(f.search).slice(0,40); skip if length < 10 (avoid trivial). Hmm — spec says first 40 chars; if the line is shorter, the whole line. A bare "5" alone with empty text → search "5" → skip via length check? The spec doesn't mention skipping... but a 1-char search would false-positive. In practice every footnote has text. I'll require searchStr.length>=8 to search. Reasonable.

Hmm wait, actually — for the bare-number first footnote on a page, is the "line that opens the footnote" the bare number line, or...? The spec's parenthetical example only shows the "N text" form. I think using number+first-text-line is the sensible reading ("its number included"). OK.

Check 7 headers/footers:
```js
  var hdrOk=P.pages.filter(p=>p.headerOk).length;
  var pgNum=P.pages.filter(p=>p.pageNum).length;
  var disp=P.pages.filter(p=>p.displaced!=null).map(p=>p.displaced+' (page '+p.page+')');
  status: hdrOk===P.pages.length && pgNum===P.pages.length-1 ? 'pass':'fail'
  detail: hdrOk+' of '+P.pages.length+' pages begin with the symbol. '+pgNum+' of '+P.pages.length+' pages carry their own page number in the footer (all but the first expected). Displaced footnote numbers kept aside from footers: '+disp.join(', ')+'.' + pageNotes
```
Hmm — "expected all but the first": pgNum should equal pages.length-1 assuming first page lacks number. But what if firstPage isn't 1... whatever, use pages.length-1. Actually safer: expected = pages.length - (first page has no number ? 1 : 0). I'll compute expectedPg = P.pages.length - (P.pages[0] && !P.pages[0].pageNum ? 1 : 0). status pass if pgNum===expectedPg && hdrOk===pages.length.

Check 8 headings:
```js
  var lab=P.headings.filter(h=>h.labelled).length, unlab=P.headings.filter(h=>!h.labelled).length;
  detail: lab+' labelled and '+unlab+' unlabelled headings found. Unlabelled: '+list (truncated, maybe in scroll box).
  status: P.headings.length>0?'pass':'fail'
```

Check 9 nothing lost:
```js
  var kinds={cover:0,header:0,heading:0,paragraph:0,footnote:0,footer:0};
  var total=0, unclass=[];
  P.pages.forEach(function(pg){
    pg.lines.forEach(function(l){
      if(l.raw.trim()==='') return;
      total++;
      if(l.kind && kinds[l.kind]!==undefined) kinds[l.kind]++;
      else unclass.push('page '+pg.page+' line "'+trunc(l.raw.trim(),40)+'"');
    });
  });
  var sum=kinds.cover+kinds.header+kinds.heading+kinds.paragraph+kinds.footnote+kinds.footer;
  status: sum===total && unclass.length===0 ? 'pass':'fail'
  detail: 'Every non-empty line classified exactly once: cover '+kinds.cover+', header '+kinds.header+', heading '+kinds.heading+', paragraph '+kinds.paragraph+', footnote '+kinds.footnote+', footer '+kinds.footer+' = '+sum+' of '+total+' non-empty lines. Unclassified: '+(unclass.length? unclass.join('; ') : 'none')+'.'
```

Also hyphen lines note: "No line ends with a hyphen, so no hyphen joining is done; the app counts such lines anyway and reports the number." — I'll add to method text: "Lines ending in a hyphen: n (none here, so no hyphen joining was needed)." Put in tab 04 method area or check 9 detail. I'll add a small "Method" note under checks: pipeline description. Actually the plan says tab 04 is "CHECKS & METHOD" — include a short method paragraph. I'll add a "Method" block: the pipeline in 4-5 short lines. Good for honesty.

Now — P.checks = checks; P.passCount etc computed at render.

Now render functions. Let me write them.

```js
var selected=0;
docs.forEach(function(d,i){ d.parsed=parseDoc(d.doc); });

function activateTab(i, focus){
  var tabs=document.querySelectorAll('#tablist [role="tab"]');
  tabs.forEach(function(t,k){
    t.setAttribute('aria-selected', k===i?'true':'false');
    t.tabIndex = k===i?0:-1;
    document.getElementById('panel-'+k).hidden = k!==i;
  });
  if(focus) tabs[i].focus();
}
```

Roving tabindex: set tabIndex on render. I'll set in activateTab and initial.

renderAll(): renderHeader, renderRail, renderPanels.

renderHeader():
```js
function renderHeader(){
  var d=docs[selected], P=d.parsed, doc=d.doc;
  document.getElementById('docTitle').textContent=doc.title||'Untitled document';
  var meta=[];
  if(doc.symbol){ meta.push(doc.doc_url? '<a href="'+esc(doc.doc_url)+'" target="_blank" rel="noopener">'+esc(doc.symbol)+'</a>' : esc(doc.symbol)); }
  if(P.ref && P.ref.adopted!=null) meta.push('adopted '+esc(P.ref.adopted));
  meta.push(P.pages.length+' pages of raw converter text');
  if(doc.source) meta.push(esc(doc.source));
  document.getElementById('docMeta').innerHTML=meta.join(' · ');
  // pill
  var run=P.checks.filter(c=>c.status!=='notrun');
  var pass=run.filter(c=>c.status==='pass').length;
  var fail=run.length-pass;
  var pill=document.getElementById('checkPill');
  if(fail>0){ pill.innerHTML='<span class="dot red"></span>'+fail+' of '+run.length+' checks failed'; pill.className='pill bad'; }
  else { pill.innerHTML='<span class="dot green"></span>'+pass+' of '+run.length+' checks pass'; pill.className='pill ok'; }
  // tab 04 dot
  var t4=document.getElementById('tab-3').querySelector('.dot');
  t4.hidden = fail===0;
}
```

Hmm — pill as button linking to tab 3: make it `<button class="pill" data-act="tab" data-i="3">`. OK.

renderRail():
```js
function renderRail(){
  var box=document.getElementById('docCards');
  box.innerHTML=docs.map(function(d,i){
    var P=d.parsed, doc=d.doc, ref=P.ref;
    var paraN=P.paragraphs.length, fnN=P.numberedFns.length;
    var refP=ref?ref.paragraphs:null, refF=ref?ref.footnotes:null;
    function bar(found,exp){
      if(exp==null) return '<div class="bar"><div class="fill neutral" style="width:100%"></div></div>';
      var pct=Math.max(0,Math.min(100, found/exp*100));
      var cls= found===exp?'fill ok':'fill bad';
      return '<div class="bar"><div class="'+cls+'" style="width:'+pct+'%"></div></div>';
    }
    var run=P.checks.filter(c=>c.status!=='notrun');
    var pass=run.filter(c=>c.status==='pass').length;
    var chk = run.length? (pass===run.length? pass+' of '+run.length+' checks pass' : (run.length-pass)+' of '+run.length+' checks failed') : 'no checks run';
    return '<button class="doccard'+(i===selected?' selected':'')+'" data-act="doc" data-i="'+i+'">'
      +'<span class="mono sym">'+esc(doc.symbol||d.key)+'</span>'
      +'<span class="dtitle">'+esc(doc.title||'')+'</span>'
      +'<span class="dmeta">'+(ref&&ref.adopted!=null?'adopted '+esc(ref.adopted)+' · ':'')+P.pages.length+' pages</span>'
      +'<span class="bigrow"><span class="big">'+paraN+'</span><span class="of">of '+(refP!=null?refP:'—')+' paragraphs</span></span>'
      +bar(paraN,refP)
      +'<span class="bigrow"><span class="big">'+fnN+'</span><span class="of">of '+(refF!=null?refF:'—')+' footnotes</span></span>'
      +bar(fnN,refF)
      +'<span class="mono checks">'+(i===selected?chk:chk)+' → tab 04</span>'
      +'</button>';
  }).join('');
}
```

Hmm — "each with 'of reference.paragraphs' or 'of reference.footnotes' in the reference and a thin bar showing the share found (red when short or over), then 'n of m checks pass', linking to tab 04." — the checks line should be a link to tab 04... but the whole card is a button (can't nest buttons). I'll make the checks line visually indicate; clicking card selects doc. To honor "linking to tab 04", I could make the card a div with two buttons... simpler: card is a button; the checks line says "n of m checks pass — see tab 04". Acceptable. Or: after selecting, the pill in header links to tab 04. Fine.

renderPanels(): builds each panel's innerHTML for selected doc.

Panel 0:
```js
function renderResult(P){
  var ref=P.ref, refP=ref?ref.paragraphs:null, refF=ref?ref.footnotes:null;
  var paraN=P.paragraphs.length, fnN=P.numberedFns.length;
  var withRef=P.paragraphs.filter(p=>p.first_words_reference!=null);
  var matchN=withRef.filter(p=>p.first_words_match).length;
  var leakHits = P.leakHits.length; // computed in checks
  ...
  tiles html
}
```

Let me compute leakHits in parseDoc and store on P (check 6). I'll store P.leak = {hits:[...], longP:[...]}.

Tile HTML:
```html
<div class="tiles">
  <div class="tile">
    <div class="mono tlabel">PARAGRAPHS FOUND</div>
    <div class="trow"><span class="big">90</span><span class="tside">The document has: <b>90</b> <span class="ok">match</span></span></div>
    <div class="how">How this is computed: count of body lines that open a numbered paragraph (1–3 digits + “.”), after headers, footers and footnote blocks were removed.</div>
  </div>
  ...
</div>
```

Tile 1 side: if refP==null → "no reference in this file". Else if equal → green "match"; else red "difference +2"/"−3". Plus if leakHits>0: red line "n paragraphs contain footnote text".

Tile 2: big fnN, side "of refF footnotes" (or "no reference"). status color if mismatch.
Tile 3: big matchN, side "of refP paragraphs" — hmm "First words match: n of reference.paragraphs". side: "of "+refP+" paragraphs in the reference". 
Tile 4: big repairs.length, side: link `<button class="link" data-act="open-repairs">open the repair log on tab 04</button>`.

Panel 1 (paragraphs): as designed. Let me write:

```js
function renderParagraphs(P){
  var ref=P.ref;
  var cap = P.paragraphs.length+' paragraphs found'+(ref&&ref.paragraphs!=null?', '+ref.paragraphs+' expected':'');
  var rows=P.paragraphs.map(function(p){
    var pages = p.pageStart===p.pageEnd? String(p.pageStart) : p.pageStart+'–'+p.pageEnd;
    var chk = p.first_words_match===null? '<span class="mut">no reference</span>' : (p.first_words_match? '<span class="ok">OK</span>' : '<span class="bad">first words differ</span>');
    var first = cutWord(p.text,120);
    return '<tr class="prow" id="prow-'+p.number+'" data-n="'+p.number+'">'
      +'<td class="num"><button class="rowbtn" data-act="toggle-row" data-n="'+p.number+'" aria-expanded="false" aria-controls="det-'+p.number+'">'+p.number+'</button></td>'
      +'<td class="sec">'+esc(p.section||'—')+'</td>'
      +'<td class="num">'+pages+'</td>'
      +'<td class="fl">'+esc(first)+'</td>'
      +'<td class="chk">'+chk+'</td></tr>'
      +'<tr class="detail" id="det-'+p.number+'" hidden><td colspan="5">'+detailHtml(P,p)+'</td></tr>';
  }).join('');
  ...
}
```

detailHtml(P,p):
```js
function detailHtml(P,p){
  var h='';
  var path = (p.part && p.section && p.part!==p.section) ? p.part+' › '+p.section : (p.section||p.part||'');
  if(path) h+='<div class="mono path">'+esc(path)+'</div>';
  h+='<div class="fulltext">'+esc(p.text)+'</div>';
  h+='<button class="link linesToggle" data-act="toggle-lines" data-n="'+p.number+'" aria-expanded="false" aria-controls="lines-'+p.number+'">Show the PDF’s lines</button>';
  h+='<div class="rawlines" id="lines-'+p.number+'" hidden>'+linesHtml(p)+'</div>';
  var fw;
  if(p.first_words_reference==null) fw='<span class="mut">no reference for this paragraph</span>';
  else fw='reference: “'+esc(p.first_words_reference)+'” · found: “'+esc(p.first_words_found)+'” — '+(p.first_words_match?'<span class="ok">equal</span>':'<span class="bad">different</span>');
  h+='<div class="fw">First six words: '+fw+'</div>';
  var meta=[];
  meta.push('pages '+ (p.pageStart===p.pageEnd? p.pageStart : p.pageStart+'–'+p.pageEnd));
  if(p.marks.length) meta.push('cites footnotes '+p.marks.join(', '));
  if(p.repairs.length) meta.push('repairs: '+p.repairs.join('; '));
  h+='<div class="pmeta">'+esc(meta.join(' · '))+'</div>';
  h+='<button class="copybtn" data-act="copy" data-cite="'+esc(p.citation)+'">Copy citation</button>';
  return h;
}
function linesHtml(p){
  var out='', lastPage=null;
  p.lines.forEach(function(l){
    if(l.page!==lastPage){ out+='<div class="pagemark">— page '+l.page+' —</div>'; lastPage=l.page; }
    out+='<div class="pline">'+esc(l.raw)+'</div>';
  });
  return out;
}
```

Headings box:
```js
var hbox = '<button class="coll" data-act="toggle" data-target="headingsBox" aria-expanded="false" aria-controls="headingsBox">Headings found: '+P.headings.length+'</button>'
 +'<div id="headingsBox" hidden><ul class="hlist">'
 + P.headings.map(h=>'<li>'+(h.labelled?'<span class="mono">labelled</span> ':'<span class="mono">unlabelled</span> ')+esc(h.display||h.label)+'</li>').join('')
 +'</ul></div>';
```

Hmm — "A collapsible 'Headings found: n' box above the table lists them". Good.

Panel 2 (footnotes):
```js
function renderFootnotes(P){
  var ref=P.ref, refF=ref?ref.footnotes:null;
  var cap=P.numberedFns.length+' footnotes found'+(refF!=null?', '+refF+' expected':'');
  rows = P.footnotes.map(f=> ... ) // include '*' row? "Footnotes found: n of reference.footnotes" — numbered only in count; I'll list numbered footnotes, and if a '*' exists add a note line. Actually include the '*' row at its position with No. "*" and repair "—"? The count says numbered. I'll list all footnotes including '*' (marked), but caption counts numbered. Simpler: list numberedFns only, plus note about '*'. Hmm — the asterisk note is a footnote of the cover; listing it is informative. I'll list all P.footnotes, with '*' shown as "*" and a note. Count in caption = numberedFns.length.
  row: '<tr><td class="num">'+f.number+'</td><td class="num">'+f.page+'</td><td class="ftext">'+esc(f.text)+'</td><td>'+(f.repaired?'<span class="bad">number restored from the page foot</span>':'—')+'</td></tr>'
  download button: '<button class="dl" data-act="csv-fn">footnotes.csv</button>'
}
```

Wait — repair column text: "number restored from the page foot" — spec exact words: "number restored from the page foot". Use that (maybe red? It's a repair, not a failure — keep ink or red? The plan says Repair reads "number restored from the page foot". I'll keep plain ink with maybe red accent? Red is for failures; restoration is a fix. Keep ink.)

Panel 3 (checks & method):
```js
function renderChecks(P){
  var checksHtml = P.checks.map(function(c,i){
    var st = c.status==='pass'? '<span class="ok">pass</span>' : c.status==='fail'? '<span class="bad">check failed</span>' : '<span class="mut">not run</span>';
    return '<div class="check"><div class="chead"><span class="cname">'+esc(c.name)+'</span>'+st+'</div><div class="cdetail">'+c.detail+'</div></div>';
  }).join('');
  // method block
  var method = '<div class="method"><div class="mono mlabel">METHOD</div>'
   +'<p>Each page is split into lines. The header (the symbol on the first line) and the footer (job code, date stamp, page number, displaced numbers) are removed. The footnote block is found at the foot of the page and moved out of the body. Body lines of all pages are joined in page order, so paragraphs that cross a page break are re-joined. Paragraphs start at a line that is a number alone or a number followed by text; headings are labelled (“IV.”, “A.”) or sit on the line just before a paragraph number. Footnote marks in the text are found by a sequential counter, not by pattern alone, so “article 11” is not bracketed. Lines ending in a hyphen: '+P.hyphenLines+' (none, so no hyphen joining was needed).</p></div>';
  // repair log
  var kinds={}; P.repairs.forEach(r=>{kinds[r.kind]=(kinds[r.kind]||0)+1;});
  var kindsLine=Object.keys(kinds).map(k=>esc(k)+' ×'+kinds[k]).join('  ·  ');
  var sorted=P.repairs.slice().sort((a,b)=> a.pg-b.pg || a.seq-b.seq);
  var rrows=sorted.map(r=>'<tr><td class="num">'+esc(String(r.page))+'</td><td>'+esc(r.target)+'</td><td>'+esc(r.kind)+'</td><td class="bf">'+esc(trunc(r.before,90))+'</td><td class="bf">'+esc(trunc(r.after,90))+'</td></tr>').join('');
  ...
}
```

Hmm — repairs sorted by pg: pg for join repairs I set to p.pageEnd (number). For heading separated: prev.page. OK numeric.

Repair log HTML:
```html
<button class="coll" data-act="toggle" data-target="repairsBox" id="repairsBtn" aria-expanded="false" aria-controls="repairsBox">Repair log (n)</button>
<div id="repairsBox" hidden>
  <p class="kinds mono">kinds…</p>
  <table><caption><span class="fig">TAB.03</span> n repairs, in document order</caption>
  <thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead>
  <tbody>rows</tbody></table>
</div>
```

Raw pages:
```html
<button class="coll" data-act="toggle" data-target="rawBox" aria-expanded="false" aria-controls="rawBox">Raw pages</button>
<div id="rawBox" hidden>
  <label class="rawlabel">Show raw page <select id="rawSel">options</select></label>
  <div class="legend mono">…</div>
  <div class="rawpanel" id="rawPanel"></div>
</div>
```

Raw panel render on select change (delegate 'change' event on document for #rawSel).

Download:
```html
<div class="dlblock">
  <div class="mono mlabel">DOWNLOAD</div>
  <button class="dl" data-act="csv">Download paragraphs as CSV</button>
  <p class="hint">UTF-8 with a byte-order mark, every field double-quoted, CRLF line ends. File name: <span class="mono">E-C.12-GC-27-paragraphs.csv</span>. Columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, text_lines, footnotes_cited, repairs, citation, symbol, doc_url.</p>
</div>
```

Footer:
```js
function renderFooter(){
  var d=docs[selected], doc=d.doc;
  document.getElementById('foot').innerHTML = 'Source: '+esc(doc.source||'WORKSHOP_DATA')+(doc.built?' · built '+esc(doc.built):'')+' · Counting, splitting and matching are done by this page’s code; no model was called and nothing left the browser.';
}
```

Hmm — footer should maybe show for the selected doc; on doc switch re-render. OK.

Event delegation:

```js
document.addEventListener('click', function(e){
  var el=e.target.closest('[data-act]');
  if(!el) return;
  var act=el.getAttribute('data-act');
  if(act==='tab'){ activateTab(+el.getAttribute('data-i'), false); }
  else if(act==='doc'){ selected=+el.getAttribute('data-i'); renderAll(); }
  else if(act==='toggle-row'){ toggleRow(+el.getAttribute('data-n')); }
  else if(act==='toggle'){ var t=document.getElementById(el.getAttribute('data-target')); var open=t.hidden; t.hidden=!open; el.setAttribute('aria-expanded', open?'true':'false'); if(el.getAttribute('data-target')==='rawBox' && open) renderRawPage(); }
  else if(act==='toggle-lines'){ same generic — actually toggle-lines uses data-target too? I gave aria-controls="lines-n" but data-act toggle-lines with data-n. Let me unify: use data-act="toggle" data-target="lines-N" for the lines toggle too. Simplify: all collapsibles use data-act="toggle" data-target="id". The lines toggle button: data-target="lines-12". Good — drop toggle-lines.
  else if(act==='open-repairs'){ activateTab(3,false); var b=document.getElementById('repairsBtn'); var box=document.getElementById('repairsBox'); box.hidden=false; b.setAttribute('aria-expanded','true'); b.scrollIntoView({block:'start'}); }
  else if(act==='goto-para'){ var n=+el.getAttribute('data-n'); activateTab(1,false); expandRow(n); var row=document.getElementById('prow-'+n); if(row) row.scrollIntoView({block:'center'}); }
  else if(act==='copy'){ copyText(el.getAttribute('data-cite'), el); }
  else if(act==='csv'){ downloadParagraphsCSV(); }
  else if(act==='csv-fn'){ downloadFootnotesCSV(); }
});
document.addEventListener('change', function(e){
  if(e.target.id==='rawSel') renderRawPage();
});
document.addEventListener('keydown', function(e){
  if(e.target.getAttribute && e.target.getAttribute('role')==='tab'){
    var tabs=[...document.querySelectorAll('#tablist [role="tab"]')];
    var i=tabs.indexOf(e.target);
    if(e.key==='ArrowRight'){ activateTab((i+1)%tabs.length,true); e.preventDefault(); }
    else if(e.key==='ArrowLeft'){ activateTab((i-1+tabs.length)%tabs.length,true); e.preventDefault(); }
    else if(e.key==='Home'){ activateTab(0,true); e.preventDefault(); }
    else if(e.key==='End'){ activateTab(tabs.length-1,true); e.preventDefault(); }
  }
});
```

toggleRow(n): 
```js
function toggleRow(n){
  var btn=document.querySelector('.rowbtn[data-n="'+n+'"]');
  var det=document.getElementById('det-'+n);
  if(!btn||!det) return;
  var open=det.hidden;
  det.hidden=!open;
  btn.setAttribute('aria-expanded', open?'true':'false');
}
function expandRow(n){ var det=document.getElementById('det-'+n); var btn=document.querySelector('.rowbtn[data-n="'+n+'"]'); if(det&&det.hidden){det.hidden=false; btn.setAttribute('aria-expanded','true');} }
```

Also clicking the prow (not just button): add data-act="toggle-row" on the tr? tr with data-act — clicking anywhere in row triggers. But then clicking the button inside also triggers (closest finds button first — same action, fine, but double-toggle? e.target.closest('[data-act]') returns the button (nearest ancestor with data-act) — the tr also has data-act but closest returns the button. One handler call. Good. So put data-act="toggle-row" data-n on the tr, and the button inside has no data-act (or same — closest picks button, same act/n). I'll put data-act only on tr; button inside is focusable and click bubbles to tr handler. But keyboard Enter on button fires click → bubbles → handler. Good. So button: `<button class="rowbtn" aria-expanded="false" aria-controls="det-N">N</button>` without data-act; tr has data-act="toggle-row" data-n="N". 

renderRawPage():
```js
function renderRawPage(){
  var P=docs[selected].parsed;
  var sel=document.getElementById('rawSel');
  var page=+sel.value;
  var pg=P.pages.filter(p=>p.page===page)[0];
  if(!pg) return;
  var html=pg.lines.map(function(l,i){
    var k=l.kind||'unclassified';
    var cls = k==='blank'?'k-blank':'k-'+k;
    var code = k==='blank'?'·':(k==='unclassified'?'!':k.charAt(0).toUpperCase());
    return '<div class="rl"><span class="ln">'+(i+1)+'</span><span class="kc '+cls+'">'+code+'</span><span class="lt '+cls+'">'+esc(l.raw)+'</span></div>';
  }).join('');
  document.getElementById('rawPanel').innerHTML=html;
}
```

Hmm — kind 'blank' lines: raw may be '' — render empty. kind null & non-empty → 'unclassified' red. kind null & empty → blank. Let me handle: `var k = l.kind || (l.raw.trim()==='' ? 'blank' : 'unclassified');`

Legend codes: cover C, header H, heading T, paragraph P, footnote F, footer X. k.charAt(0).toUpperCase(): cover→C, header→H, heading→T? 'heading'.charAt(0)='h' → 'H' — collides with header! Use explicit map: {cover:'C',header:'H',heading:'T',paragraph:'P',footnote:'F',footer:'X',blank:'·',unclassified:'!'}. 

CSV downloads:

```js
function downloadParagraphsCSV(){
  var P=docs[selected].parsed, doc=docs[selected].doc;
  var header=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','text_lines','footnotes_cited','repairs','citation','symbol','doc_url'];
  var rows=P.paragraphs.map(function(p){
    return [p.number, p.section||'', p.part||'', p.pageStart, p.pageEnd,
      p.first_words_reference||'', p.first_words_found, p.first_words_match===null?'not run':(p.first_words_match?'yes':'no'),
      p.text, p.text_raw, p.text_lines.join(' | '), p.marks.join('; '), p.repairs.join('; '), p.citation, P.symbol, doc.doc_url||''];
  });
  downloadCSV(P.symbol.replace(/\//g,'-')+'-paragraphs.csv', header, rows);
}
function downloadFootnotesCSV(){
  var P=docs[selected].parsed, doc=docs[selected].doc;
  var header=['number','page','text','repair','symbol','doc_url'];
  var rows=P.footnotes.map(function(f){
    return [String(f.number), f.page, f.text, f.repaired?'number restored from the page foot':'', P.symbol, doc.doc_url||''];
  });
  downloadCSV(P.symbol.replace(/\//g,'-')+'-footnotes.csv', header, rows);
}
```

Now — checks detail HTML with links. Let me write them concretely in parseDoc:

```js
  // check 3 detail with links
  function paraLink(n){ return '<button class="link" data-act="goto-para" data-n="'+n+'">para. '+n+'</button>'; }
```

Check 3 detail: `matchN+' of '+withRef.length+' paragraphs with a reference match'+(refP!=null?' (reference: '+refP+')':'')+'.' + (mism.length? ' Mismatches: '+mism.map(p=>paraLink(p.number)+': found “'+esc(trunc(p.first_words_found,40))+'” / reference “'+esc(trunc(p.first_words_reference,40))+'”').join('; ') : ' No mismatches.')`

Check 5 detail: `'Marks in the paragraph text run 1–'+k+'; the reference expects 1–'+refF+'.'+(missing.length?' Missing: '+missing.join(', '):'')+' Rejected as not marks (context shown): '+rejectedList` — rejectedList in a scrollable div: `<div class="scrollbox">` + items `⟨11⟩ para. 6: “…article ⟨11⟩…”` — hmm context already has ⟨⟩. Format: `para. 6: “…article ⟨11⟩ and…”`. I'll render each rejected as `<div>para. N — “context”</div>`.

Check 6 detail: hits list with paraLink; longP list with paraLink; plus maxWords.

Check 4 detail: restored list: `footnote 6 (page 2)` etc.

Check 7 detail: as above + pageNotes.

Check 8 detail: unlabelled list in scrollbox.

OK. Now — one more thing: tile 1 "n contain footnotes" — from check 6 hits: count distinct paragraphs with hits. P.leakParas = unique para numbers in hits.

Now — initial render: parse all docs, renderAll, activateTab(0).

Also — the tab buttons need ids tab-0..tab-3 and panels panel-0..panel-3, with aria-labelledby.

Let me also handle: when switching docs, re-render panels and rail and header and footer; also reset raw select etc. Since panels are rebuilt via innerHTML, listeners are delegated — fine. The rawSel change listener is on document — fine.

One catch: after re-render, the repairsBox/rawBox are hidden again (fresh HTML with hidden). Fine.

Now — CSS details. Let me write the full CSS:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;--mut:#6f6a5e}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-text-size-adjust:100%}
a{color:var(--red)}
button{font:inherit;color:inherit;background:none;border:none;padding:0;cursor:pointer;text-align:left}
button.link{color:var(--red);text-decoration:underline;text-underline-offset:2px}
:focus-visible{outline:3px solid var(--red);outline-offset:2px;border-radius:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,"Liberation Mono",monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase}
header.top{max-width:1240px;margin:0 auto;padding:22px 28px 10px}
.kicker{color:var(--red)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(24px,3.4vw,34px);line-height:1.18;margin:8px 0 6px;max-width:60ch}
.meta{font-size:14px;color:var(--ink);margin:0 0 4px}
.meta a{color:var(--red)}
.what{font-size:15px;max-width:75ch;margin:6px 0 0;color:var(--ink)}
.headrow{display:flex;justify-content:space-between;gap:24px;align-items:flex-start;flex-wrap:wrap}
.pill{...}
```

Pill: mono, border 1px rule, padding 6px 10px, border-radius 999px, white-space nowrap. dot: 9px circle inline-block.

Layout:
```css
.layout{max-width:1240px;margin:0 auto;padding:0 28px 30px;display:grid;grid-template-columns:250px 1fr;gap:28px;align-items:start}
@media (max-width:900px){.layout{grid-template-columns:1fr}}
.rail{border-right:1px solid var(--rule);padding-right:18px;position:sticky;top:0}
```
Hmm sticky rail — fine without. Keep simple: no sticky.

Rail:
```css
.railhead{color:var(--mut);border-bottom:1px solid var(--rule);padding-bottom:6px;margin-bottom:12px}
.doccard{display:block;width:100%;border-left:3px solid transparent;padding:10px 12px;margin-bottom:10px;border-radius:0 6px 6px 0}
.doccard:hover{background:#ece7db}
.doccard.selected{border-left-color:var(--red);background:#efe9dc}
.doccard .sym{color:var(--red);display:block}
.dtitle{display:block;font-size:13px;line-height:1.35;margin:4px 0 2px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.dmeta{display:block;font-size:12px;color:var(--mut);margin-bottom:8px}
.bigrow{display:flex;align-items:baseline;gap:8px;margin-top:6px}
.big{font-family:Georgia,serif;font-size:40px;line-height:1}
.of{font-size:12.5px;color:var(--mut)}
.bar{height:4px;background:var(--rule);margin:6px 0 2px;border-radius:2px;overflow:hidden}
.fill{height:100%;background:var(--ink)}
.fill.bad{background:var(--red)}
.fill.neutral{background:var(--rule)}
.doccard .checks{display:block;margin-top:8px;color:var(--mut)}
```

Tabs:
```css
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin-bottom:18px;flex-wrap:wrap}
.tabs [role="tab"]{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;padding:10px 14px;border-bottom:2px solid transparent;color:var(--mut)}
.tabs [role="tab"][aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tabs [role="tab"]:hover{color:var(--ink)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-left:6px;vertical-align:1px}
.dot.green{background:var(--green)}.dot.red{background:var(--red)}
```

Panels:
```css
.panel{min-width:0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0 26px}
.tile{border-top:1px solid var(--ink);padding:10px 0 16px}
.tlabel{color:var(--mut)}
.trow{display:flex;align-items:baseline;gap:12px;margin:6px 0 4px;flex-wrap:wrap}
.trow .big{font-size:52px}
.tside{font-size:14px}
.how{font-size:12.5px;color:var(--mut);border-top:1px solid var(--rule);padding-top:6px;margin-top:6px}
.ok{color:var(--green);font-weight:600}
.bad{color:var(--red);font-weight:600}
.mut{color:var(--mut)}
```

Tables:
```css
table{width:100%;border-collapse:collapse;margin:10px 0 6px;font-size:15px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:20px;padding:0 0 8px}
caption .fig{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;color:var(--red);margin-right:10px;vertical-align:2px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:400;color:var(--mut);text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule);padding:8px 10px 8px 0;vertical-align:top;overflow-wrap:break-word}
th.num,td.num{text-align:right}
.prow{cursor:pointer}
.prow:hover td{background:#ece7db}
.rowbtn{font-family:Georgia,serif;font-size:17px;color:var(--red);min-width:2.2ch;text-align:right;padding:0 4px}
tr.detail td{background:#efe9dc;border-bottom:1px solid var(--ink);padding:14px 16px}
.sec{font-size:13.5px;color:var(--mut)}
.fl{font-size:14.5px}
```

Hmm — rowbtn inside td.num right-aligned. OK.

Detail content:
```css
.path{color:var(--red);margin-bottom:8px}
.fulltext{font-size:15.5px;line-height:1.6;max-width:85ch}
.rawlines{margin-top:8px;border-top:1px solid var(--rule);padding-top:8px}
.pline{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;overflow-wrap:break-word}
.pagemark{font-family:ui-monospace,monospace;font-size:10.5px;letter-spacing:.12em;color:var(--red);margin:6px 0 2px;text-transform:uppercase}
.fw{margin-top:10px;font-size:14px}
.pmeta{margin-top:6px;font-size:13px;color:var(--mut)}
.copybtn{margin-top:10px;border:1px solid var(--ink);padding:6px 12px;border-radius:999px;font-size:13.5px}
.copybtn:hover{background:var(--ink);color:var(--paper)}
```

Collapsibles:
```css
.coll{display:block;font-family:ui-monospace,monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);border-top:1px solid var(--rule);width:100%;padding:10px 0;margin-top:14px}
.coll:hover{color:var(--ink)}
```

Checks:
```css
.check{border-top:1px solid var(--rule);padding:10px 0}
.chead{display:flex;justify-content:space-between;gap:14px;align-items:baseline}
.cname{font-weight:600;font-size:15px}
.cdetail{font-size:13.5px;color:var(--ink);margin-top:3px}
.scrollbox{max-height:150px;overflow:auto;border:1px solid var(--rule);padding:6px 10px;margin-top:6px;font-size:12.5px;background:#efe9dc}
```

Raw viewer:
```css
.rawpanel{border:1px solid var(--rule);background:#fbf8f2;margin-top:10px;max-height:520px;overflow:auto;padding:8px 0}
.rl{display:flex;gap:8px;padding:0 10px 0 0}
.ln{width:4ch;text-align:right;color:var(--mut);font-family:ui-monospace,monospace;font-size:10.5px;user-select:none;padding-top:1px}
.kc{width:2ch;text-align:center;font-family:ui-monospace,monospace;font-size:10px;padding-top:2px;border-radius:2px;flex:none}
.lt{flex:1;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;overflow-wrap:break-word;padding:1px 6px 1px 0}
.k-cover{background:#efe6d0}.k-header{background:#e2e7f2}.k-heading{background:#f3dede}.k-paragraph{background:#e6efe0}.k-footnote{background:#f7ecd4}.k-footer{background:#e7e3da}.k-blank{background:transparent}.k-unclassified{background:#f0b9b9}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:10px;color:var(--mut)}
.sw{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:5px;vertical-align:-1px}
```

Hint:
```css
.hint{font-size:13px;color:var(--mut);max-width:90ch}
.hint code{font-family:ui-monospace,monospace;font-size:12px;background:#e9e3d6;padding:1px 5px;border-radius:3px}
```

Footer:
```css
footer{border-top:1px solid var(--ink);max-width:1240px;margin:0 auto;padding:12px 28px 30px;font-size:13px;color:var(--mut)}
```

Buttons .dl:
```css
.dl{border:1px solid var(--ink);border-radius:999px;padding:8px 16px;font-size:14px;margin:6px 0}
.dl:hover{background:var(--ink);color:var(--paper)}
```

OK. Now — assemble everything. Also the "what" sentence and header.

One more requirement: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — the header meta has symbol link. Paragraph rows: the citation includes symbol; the CSV has symbol+doc_url. Maybe add symbol link in paragraph detail? The detail has Copy citation; I'll add a small mono line with symbol link in the detail: `<a href=doc_url target=_blank>symbol</a>`. Good — add to detailHtml: path line + symbol link. Actually the header covers it; but "every row that shows a document" — rows show paragraphs of the document; I'll include the symbol link in each detail row's meta line. Cheap: add to pmeta: `<a ...>E/C.12/GC/27</a>`. OK.

Also footnote rows: symbol? They're footnotes of the doc; the tab has the doc context. I'll skip per-row symbol there but the CSV includes it. Hmm, "Every row that shows a document has its symbol, linked to doc_url" — rows showing documents... paragraphs/footnotes are parts of the document. To be safe, add symbol link in footnote table caption area? I'll add a line under footnotes caption: symbol link. Fine.

Now — let me also double check the tab count constraint: tab 02 has: 4 tabs + headings collapsible + per-row buttons (rows not counted). OK. Tab 04: 4 tabs + repairs heading + raw heading + download + raw select (when open) + check links... "about seven" — close enough; check links are inline text links. Hmm, to reduce, I could make check links only on failed checks. I'll include links only where meaningful (mismatches, hits, long paragraphs). Fine.

Now — one more important thing: the plan says tab 01 tiles: "Paragraphs found: n next to The document has: reference.paragraphs (green when equal, red with the difference)". OK.

Let me also handle `ref.first_words` possibly keyed differently — use String(p.number).

Now — writing the final HTML. Also include `<title>`. And a "Credits" line? The sources consulted (UK Gov etc.) are guidance, not code — no licence requirement for code. The wiki/library stuff isn't used. No credits needed (no open-licence code copied). Skip.

Let me also double-check: "Before the code block: at most three short sentences saying what you built or changed. After it: nothing." — I'll write 2-3 sentences before the code block, then the html block, nothing after.

Now, let me carefully write the complete file. I need to be meticulous with the JS. Let me write it out.

Also — potential pitfall: `e.target.closest` — e.target may be a text node? No, in click events target is an element. But if e.target is not an Element (e.g., document)? Guard: `e.target.closest && ...`.

Another pitfall: buttons inside .prow tr — the tr has data-act; clicking the rowbtn: closest('[data-act]') → rowbtn has no data-act → tr. Good. But the detail row's copy button has data-act="copy" — inside det tr which has no data-act. Good.

Wait — the prow tr contains the rowbtn; but I also want clicking anywhere on the row to toggle. tr data-act="toggle-row" data-n. But the detail row (det) is a separate tr without data-act. Good.

But careful: the headings collapsible button uses data-act="toggle" data-target="headingsBox" — inside panel 1. And repairs/raw in panel 3. The generic toggle handler: find target by id, flip hidden, set aria-expanded on the button (el). Good.

For "open-repairs" from tile 4: activateTab(3), then open repairsBox: set hidden=false, repairsBtn aria-expanded=true, scrollIntoView.

Now — renderAll:

```js
function renderAll(){
  renderHeader(); renderRail(); renderFooter();
  document.getElementById('panel-0').innerHTML=renderResult(docs[selected].parsed);
  document.getElementById('panel-1').innerHTML=renderParagraphs(docs[selected].parsed);
  document.getElementById('panel-2').innerHTML=renderFootnotes(docs[selected].parsed);
  document.getElementById('panel-3').innerHTML=renderChecksPanel(docs[selected].parsed);
  // reset raw select default
}
```

activateTab(0) initially; panels 1-3 hidden via attribute in HTML.

Tab keydown: also Enter/Space on tab buttons natively click → data-act="tab" handles.

Now — renderResult details. Let me write:

```js
function renderResult(P){
  var ref=P.ref, refP=ref&&ref.paragraphs!=null?ref.paragraphs:null, refF=ref&&ref.footnotes!=null?ref.footnotes:null;
  var paraN=P.paragraphs.length, fnN=P.numberedFns.length;
  var withRef=P.paragraphs.filter(function(p){return p.first_words_reference!=null;});
  var matchN=withRef.filter(function(p){return p.first_words_match;}).length;
  var leakN=P.leakParas.length;
  function side(found,exp,unit){
    if(exp==null) return '<span class="mut">no reference in this file</span>';
    if(found===exp) return 'The document has: <b>'+exp+'</b> <span class="ok">match</span>';
    var d=found-exp; return 'The document has: <b>'+exp+'</b> <span class="bad">difference '+(d>0?'+':'−')+Math.abs(d)+'</span>';
  }
  var t1='<div class="tile"><div class="mono tlabel">Paragraphs found</div>'
    +'<div class="trow"><span class="big">'+paraN+'</span><span class="tside">'+side(paraN,refP)+'</span></div>'
    +(leakN? '<div class="bad" style="font-size:13.5px;margin-top:2px">'+leakN+' contain footnote text</div>':'')
    +'<div class="how">How this is computed: the count of body lines that open a numbered paragraph (1–3 digits followed by “.”), after headers, footers and footnote blocks were removed from every page.</div></div>';
  var t2='<div class="tile"><div class="mono tlabel">Footnotes found</div>'
    +'<div class="trow"><span class="big">'+fnN+'</span><span class="tside">'+(refF!=null?('of <b>'+refF+'</b> footnotes in the reference '+(fnN===refF?'<span class="ok">match</span>':'<span class="bad">difference '+(fnN-refF>0?'+':'−')+Math.abs(fnN-refF)+'</span>')):'<span class="mut">no reference in this file</span>')+'</span></div>'
    +'<div class="how">How this is computed: numbered footnote openers in the page-foot blocks, plus numbers the converter displaced into the page footer and the script restored.</div></div>';
  var t3='<div class="tile"><div class="mono tlabel">First words match</div>'
    +'<div class="trow"><span class="big">'+matchN+'</span><span class="tside">'+(refP!=null?('of <b>'+refP+'</b> paragraphs in the reference'):'<span class="mut">no reference in this file</span>')+'</span></div>'
    +'<div class="how">How this is computed: the first six words of each paragraph, footnote marks removed, against the reference’s first six words, after normalising curly quotes, dashes and spaces. Case is kept.</div></div>';
  var t4='<div class="tile"><div class="mono tlabel">Repairs made</div>'
    +'<div class="trow"><span class="big">'+P.repairs.length+'</span><span class="tside"><button class="link" data-act="open-repairs">open the repair log on tab 04</button></span></div>'
    +'<div class="how">How this is computed: every line removed, split, joined or restored by this page’s code, listed with before and after on tab 04.</div></div>';
  return '<div class="tiles">'+t1+t2+t3+t4+'</div>';
}
```

Note: "−" minus sign — fine.

renderParagraphs:

```js
function renderParagraphs(P){
  var ref=P.ref;
  var capText=P.paragraphs.length+' paragraphs found'+(ref&&ref.paragraphs!=null?', '+ref.paragraphs+' expected':'');
  var hbtn='<button class="coll" data-act="toggle" data-target="headingsBox" aria-expanded="false" aria-controls="headingsBox" style="margin-top:0">Headings found: '+P.headings.length+'</button>';
  var hbox='<div id="headingsBox" hidden><ul class="hlist">'+P.headings.map(function(h){
    return '<li><span class="mono tag">'+(h.labelled?'labelled':'unlabelled')+'</span> '+esc(h.display||h.label)+'</li>';
  }).join('')+'</ul></div>';
  var rows=P.paragraphs.map(function(p){
    var pages=p.pageStart===p.pageEnd?String(p.pageStart):p.pageStart+'–'+p.pageEnd;
    var chk=p.first_words_match===null?'<span class="mut">no reference</span>':(p.first_words_match?'<span class="ok">OK</span>':'<span class="bad">first words differ</span>');
    return '<tr class="prow" id="prow-'+p.number+'" data-act="toggle-row" data-n="'+p.number+'">'
      +'<td class="num"><button class="rowbtn" aria-expanded="false" aria-controls="det-'+p.number+'">'+p.number+'</button></td>'
      +'<td class="sec">'+esc(p.section||'—')+'</td>'
      +'<td class="num">'+pages+'</td>'
      +'<td class="fl">'+esc(cutWord(p.text,120))+'</td>'
      +'<td class="chk">'+chk+'</td></tr>'
      +'<tr class="detail" id="det-'+p.number+'" hidden><td colspan="5">'+detailHtml(P,p)+'</td></tr>';
  }).join('');
  return hbtn+hbox
    +'<table><caption><span class="fig">TAB.01</span>'+esc(capText)+'</caption>'
    +'<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'
    +'<tbody>'+rows+'</tbody></table>'
    +'<p class="hint">Footnote marks are shown in square brackets, e.g. <code>waste.[2]</code>. Remove them with find-and-replace using the pattern <code>\\[\\d+\\]</code>. Click a row to expand the full text.</p>';
}
```

Wait — in JS string, to output `\[\d+\]` in HTML I write '\\[\d+\\]'? In a JS single-quoted string, `'\\['` produces `\[`. So `'<code>\\[\\d+\\]</code>'` → `<code>\[\d+\]</code>`. Good.

detailHtml as sketched, plus symbol link:

```js
function detailHtml(P,p){
  var doc=docs[selected].doc;
  var h='';
  var path=(p.part&&p.section&&p.part!==p.section)?(p.part+' › '+p.section):(p.section||p.part||'');
  if(path) h+='<div class="mono path">'+esc(path)+'</div>';
  h+='<div class="fulltext">'+esc(p.text)+'</div>';
  h+='<button class="link" data-act="toggle" data-target="lines-'+p.number+'" aria-expanded="false" aria-controls="lines-'+p.number+'" style="margin-top:8px">Show the PDF’s lines</button>';
  h+='<div class="rawlines" id="lines-'+p.number+'" hidden>'+linesHtml(p)+'</div>';
  var fw;
  if(p.first_words_reference==null) fw='<span class="mut">no reference for this paragraph</span>';
  else fw='reference “'+esc(p.first_words_reference)+'” · found “'+esc(p.first_words_found)+'” — '+(p.first_words_match?'<span class="ok">equal</span>':'<span class="bad">different</span>');
  h+='<div class="fw"><b>First six words.</b> '+fw+'</div>';
  var meta=['pages '+(p.pageStart===p.pageEnd?p.pageStart:p.pageStart+'–'+p.pageEnd)];
  if(p.marks.length) meta.push('cites footnotes '+p.marks.join(', '));
  if(p.repairs.length) meta.push('repairs: '+p.repairs.join('; '));
  if(doc.doc_url) meta.push('<a href="'+esc(doc.doc_url)+'" target="_blank" rel="noopener">'+esc(P.symbol)+'</a>');
  else meta.push(esc(P.symbol));
  h+='<div class="pmeta">'+meta.join(' · ')+'</div>';
  h+='<button class="copybtn" data-act="copy" data-cite="'+esc(p.citation)+'">Copy citation</button>';
  return h;
}
```

renderFootnotes:

```js
function renderFootnotes(P){
  var ref=P.ref, refF=ref&&ref.footnotes!=null?ref.footnotes:null;
  var capText=P.numberedFns.length+' footnotes found'+(refF!=null?', '+refF+' expected':'');
  var star=P.footnotes.filter(function(f){return f.number==='*';});
  var rows=P.footnotes.map(function(f){
    return '<tr><td class="num">'+esc(String(f.number))+'</td><td class="num">'+f.page+'</td><td class="ftext">'+esc(f.text)+'</td><td>'+(f.repaired?'number restored from the page foot':'—')+'</td></tr>';
  }).join('');
  return '<p class="lead">Each footnote as the converter produced it, after the script moved the footnote block out of the body.</p>'
    +'<button class="dl" data-act="csv-fn">footnotes.csv</button>'
    +'<table><caption><span class="fig">TAB.02</span>'+esc(capText)+'</caption>'
    +'<thead><tr><th scope="col" class="num">No.</th><th scope="col" class="num">Page</th><th scope="col">Text</th><th scope="col">Repair</th></tr></thead>'
    +'<tbody>'+rows+'</tbody></table>'
    +(star.length?'<p class="hint">The cover’s asterisked note is kept as footnote * and is not counted among the numbered footnotes.</p>':'')
    +'<p class="hint">Source: '+esc(P.doc.source||'')+' — every footnote belongs to <a href="'+esc(P.doc.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(P.symbol)+'</a>.</p>';
}
```

Hmm — P.doc — I