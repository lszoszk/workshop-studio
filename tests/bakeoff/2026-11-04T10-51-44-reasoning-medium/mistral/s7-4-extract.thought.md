Let me understand the task. The user wants me to build an HTML app that parses raw PDF converter text of a UN General Comment (E/C.12/GC/27, 20 pages) into numbered paragraphs and footnotes, checks against a reference, and shows repairs.

The data is in `WORKSHOP_DATA.pdf_text` with shape:
- `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {paragraphs, footnotes, adopted, first_words}}`

The plan is very detailed. I need to write one complete HTML file implementing the pipeline:

1. Header removal: first non-empty line equals symbol → drop, log "header line removed".
2. Footer removal: from end, drop lines while empty, starts with "GE.", only 6-digit groups (date stamp), or bare number 1-3 digits. Bare number == page → page number; other → displaced footnote number kept aside.
3. Footnote block: counter nextFootnote starting at 1. On each page after header/footer removal, block starts at first line that is bare number == nextFootnote, or starts with that number + space, or starts with "* " on first page. From there to end is footnotes. Advance nextFootnote past highest number seen in block and past displaced number for that page. If no line opens nextFootnote, take first bare number greater than it before footer, log jump.
4. Footnote text: within footnote block, line starting with number+space or bare number alone opens a footnote; lines until next opener are its text joined with space. On a page with displaced number D, first footnote (bare number, blank, text) ends at first line ending with full stop; lines after up to next numbered line are footnote D, marked repaired. Cover asterisked note kept as footnote "*" not counted.
5. Body lines concatenated in page order, tagged with page.
6. Paragraph starts: `/^(\d{1,3})\.$/` or `/^(\d{1,3})\. (.+)$/`.
7. Headings: labelled `/^([IVX]+|[A-Z])\.$/` — skip blanks, lines up to next label or paragraph start are heading text; lowercase or "(" starting line continues previous heading line (logged "heading title joined"); unlabelled heading: non-empty line immediately followed by paragraph-start line, ≤90 chars, starts with capital, doesn't end with . ; : , or digit.
8. Paragraph lines: other non-empty body lines belong to current paragraph. page_start/page_end.
9. Paragraph text: lines joined with single space, collapse double spaces, trim. Count lines ending with hyphen.
10. Footnote marks: sequential rule — walk each paragraph's text in document order with counter starting at 1. Every run of 1-3 digits not touching another digit, slash, dash, or opening parenthesis is a candidate; candidate == counter → mark, counter++; else leave. Each mark becomes `[n]`.
11. First words: first six whitespace-separated words of joined text, marks removed first; reference from `reference.first_words[String(n)]`; match after normalising curly quotes, dashes, whitespace.
12. Citation = symbol + ", para. " + n.
13. Checks: paragraph count, numbering 1..n, first words, footnotes count + numbering, footnote marks run 1..footnotes, footnotes stay out of paragraphs (search first 40 chars of footnote opener lines in raw paragraph text before marks; also list paragraphs >300 words), headers/footers, headings counts, nothing lost (every non-empty line classified exactly once, counts sum to total).

Tabs: 01 RESULT, 02 PARAGRAPHS, 03 FOOTNOTES, 04 CHECKS & METHOD. Left rail with document card(s) — the app should handle every document in WORKSHOP_DATA with records and reference (pdf_text and pdf_text_2 both have records+reference). So rail lists both documents; selected card shows that document. Today there is one attached... but the data description says pdf_text_2 also exists with records and reference. The plan says "every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data; the selected card has a red left border and the tabs show that document. Today there is one." Hmm — "Today there is one" — but the preview data includes pdf_text_2. The instruction says build apps only on files attached in this conversation. The attached file is pdf_text only. But the plan says the app is written so every document with records+reference gets a card. I think I should iterate over WORKSHOP_DATA keys that have records and reference — that would include pdf_text and pdf_text_2 if present. But "Build apps only on files attached in this conversation" — pdf_text_2 is in WORKSHOP_DATA but not attached. Hmm. The plan explicitly says "The app is written so that every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data... Today there is one." That suggests at runtime only pdf_text is attached (the workshop data for this participant has only pdf_text). But the preview shows pdf_text_2 exists in the preview data. To be safe: iterate over keys of WORKSHOP_DATA, filter those with `records` array and `reference` object. If pdf_text_2 is present in the actual runtime data, it gets a card too. That follows the plan. But the rule says build only on attached files... The plan itself instructs to handle all documents with records+reference in WORKSHOP_DATA. I'll follow the plan: scan WORKSHOP_DATA for objects with records+reference. That's deterministic and handles both. Actually wait — the rule "Build apps only on files attached in this conversation" is about not using data the user didn't attach. The plan explicitly says to write it generically. The attached file maps to WORKSHOP_DATA.pdf_text. pdf_text_2 is described in the system prompt as available. Hmm, the system prompt says "All data is already in window.WORKSHOP_DATA" and describes pdf_text_2 as "a second UN document". The user attached only pdf_text. The plan says "Today there is one" card. I think the safest interpretation: the app scans WORKSHOP_DATA for keys with records+reference; in this participant's environment only pdf_text is attached (the message says "(Attached: ... → WORKSHOP_DATA.pdf_text)"). But the preview shows pdf_text_2... The preview is what I have; the real environment may differ. The plan says "Today there is one" — meaning in the real run, only one. But if I scan generically and pdf_text_2 exists, there'd be two cards, contradicting "today there is one"? No — "today there is one" just describes current state. Generic scanning is what the plan asks ("The app is written so that every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data"). I'll do generic scanning. That handles both cases gracefully.

Hmm, but wait — the "Files" rule says build only on attached files. If pdf_text_2 is in WORKSHOP_DATA at runtime but not attached, showing it might violate. But the plan (user instruction) explicitly overrides: "The app is written so that every document in WORKSHOP_DATA with records and a reference gets its own card in the rail". User instruction wins. I'll scan generically.

Now, the parsing pipeline. Let me think carefully about the algorithm details.

Data: records sorted by page. Each record: {page, text}. text has lines separated by \n.

Step 1: split text into lines. Keep track of non-empty lines for classification.

For each page:
- lines = text.split('\n')
- Header: first non-empty line equals symbol → remove, log repair {kind:'header line removed', page}. Else log warning (check).
- Footer: from the end, drop lines while: empty, starts with "GE.", consists only of 6-digit groups (regex like /^(\d{6} )*\d{6}$/ — "051125 061125"), or bare number 1-3 digits (/^\d{1,3}$/). For bare numbers: if == page → page number (footer); else → displaced footnote number, kept aside for the page, log repair {kind:'displaced footnote number', ...}? Actually the repair log kinds listed: "header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed". Displaced number kept aside is part of footer removal but the restoration is "footnote number restored". So when we restore it as footnote D, log "footnote number restored".

Wait, careful: the footer dropping loop — "drop lines while the line is empty, starts with 'GE.', consists only of 6-digit groups, or is a bare number of one to three digits". But we must be careful not to eat body content. The footer is at the end of the page. Footnote block is before footer. The loop from the end drops footer lines. But what if a footnote text line is a bare number? Unlikely. The plan says footnote block starts at first line that is bare number == nextFootnote etc. — we do footnote block detection after header/footer removal, scanning from... hmm, order: "On each page, after header and footer are gone, the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space, or starts with '* ' on the first page; from there to the end of the page is footnotes".

Wait — but the footer removal happens from the end. The displaced footnote number is a bare number in the footer region. So after removing footer lines, the displaced number is removed from the page and kept aside. Then footnote block detection: scan lines from start; find first line that opens nextFootnote. Everything from there to end is footnote block. Everything before is body.

But careful: body text lines could start with a number + space? E.g., "6 November 2025" on the cover — the plan notes: "'6 November 2025' on the cover starts with a number and a space; it is not a footnote because the counter is at 1 when it is met." So the opener must match nextFootnote specifically (bare number == nextFootnote, or starts with nextFootnote + space). "6 November 2025" starts with "6 " but nextFootnote is 1 at that point, so not an opener. Good.

Also "starts with '* ' on the first page" — the cover asterisk note. That opens the footnote block on page 1? Hmm — on page 1, the cover has the asterisked note "* Adopted by the Committee…". If the footnote block starts at "* " on first page, then everything from there to end of page 1 is footnotes. But the cover also has title, "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on ... sustainable development*", "I.", "Introduction", "1.", paragraph text...

Wait, from the sample: page 1 text is:
```
E/C.12/GC/27

United Nations

Economic and Social Council

Distr.: General
6 November 2025
Original: English

Committee on Economic, Social and Cultural Rights

General comment No. 27 (2025) on economic, social and
cultural rights and the environmental dimension of
sustainable development*
I.

Introduction
1.
A clean, healthy and sustainable environment is an essential precondition...
```

Hmm, where's the asterisk note? It's probably at the foot of page 1: "* Adopted by the Committee at its ... session ...". The sample says "The cover's asterisked note, '* Adopted by the Committee…', is not one of the 141." So on page 1, the footnote block starts at the "* " line near the foot. So scanning page 1 for the first opener: nextFootnote=1. Is there a line that is bare "1" or starts with "1 "? Yes! The paragraph start "1." — wait, "1." is bare number with a period: "1." — does it match "bare number equal to nextFootnote"? Bare number means /^\d+$/ presumably; "1." has a period so no. Does it start with "1 " (number and space)? "1." — no space. So "1." doesn't open the footnote block. Good. But paragraph text lines... could a body line start with "1 "? E.g., a line starting "1 something"? The plan says the block starts at the first line that is a bare number equal to nextFootnote or starts with that number and a space. On page 1, before the footnote block, is there any line starting with "1 "? Possibly not. The asterisk "* " line opens it on the first page. Hmm wait, but the rule says "or starts with '* ' on the first page" — so on page 1, the opener can be the "* " line. But scanning order: we look for the first line that matches any of the opener patterns. On page 1, the "* Adopted..." line is near the end (foot area). But also footnote "1" might be on page 1? The first footnote block on page 1 — does page 1 have numbered footnotes? The sample page 1 (truncated) shows body text; footnotes probably start on page 1 or 2. Page 2 has footnotes 5 and 6 per the plan ("page 2: '5', a blank line, 'A/79/270, paras. 84 and 85.', then 'A/42/427, p. 24.' is footnote 6"). So page 1 probably has footnotes 1-4 plus the asterisk note. The asterisk note might come before or after numbered footnotes. Typically the asterisk note is at the very foot. Hmm, but the rule says the block starts at the first line that is bare number == nextFootnote OR starts with that number+space OR (first page) starts with "* ". If the asterisk line comes before footnote 1 on page 1... unlikely. Actually in UN documents, the asterisk note is usually the first footnote on the cover page, at the bottom: "* Adopted by the Committee..." then numbered footnotes follow? Or numbered footnotes then asterisk? In E/C.12/GC/27, the cover has "sustainable development*" and at the foot "* Adopted by the Committee at its seventy-third session..." Hmm, actually typically the asterisk note appears first at the foot of the first page, then numbered footnotes. Let me think: In many UN docs, footnote 1 is on page 1 and the asterisk note is at the very bottom. E.g., CCPR/C/GC/32 page 1 sample doesn't show footnotes (truncated). 

The rule as given: block starts at first line matching: bare number == nextFootnote, or starts with nextFootnote + space, or (page 1) starts with "* ". So if the "* " line appears before any "1" opener on page 1, the block starts at "* ". Then within the block, footnote parsing: "a line that starts with a number and a space, or a bare number on its own line, opens a footnote". The "* " line — the plan says "The cover's asterisked note is kept as footnote '*' and not counted." So within the block, "* " opens footnote "*". Then "1" opens footnote 1, etc.

Hmm wait, but if the asterisk line is at the very foot (after numbered footnotes), then the block would start at footnote "1" opener, and the "* " line inside the block — how is it handled? "a line that starts with a number and a space, or a bare number on its own line, opens a footnote" — "* " doesn't match, so it would be appended to the previous footnote's text. That's wrong. So probably the asterisk line comes first on page 1. Actually in UN General Comments, the asterisk note is typically the FIRST item at the foot of page 1: "* Adopted by the Committee at its ... session (see E/2025/...)." Hmm, no — actually it's usually placed at the bottom of the cover page before the numbered footnotes? Let me recall E/C.12/GC/27... I can't verify. The plan's rule handles "* " as an opener only on the first page for block-start detection. For within-block parsing, I should also treat a line starting with "* " as opening footnote "*". Let me just handle: within footnote block, opener = bare number alone, or number+space at start, or (if line starts with "* ") footnote "*". That's safe.

Actually, let me re-read: "the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space, or starts with '* ' on the first page; from there to the end of the page is footnotes, everything before is body."

So on page 1, if "* " line appears, block starts there (if no earlier opener). But what if footnote 1 appears before the asterisk line on page 1? Then block starts at "1". Then the "* " line later in the block — I'll treat it as an opener for footnote "*" within the block. Fine.

Hmm, wait — actually there's a subtlety: on page 1, is there a "1" bare line or "1 " line in the body before the footnotes? The paragraph "1." is "1." not "1". Body text lines starting with "1 "? Unlikely. OK.

But another subtlety: the block-start scan looks for the FIRST line matching the opener patterns. On pages 2-20, nextFootnote is whatever. E.g., page 2: nextFootnote=5 (after page 1's footnotes 1-4). Page 2's footnote block starts at bare "5". But wait — could a body line on page 2 start with "5 "? E.g., text "...5 ..." at line start? Possible but the plan says this rule works on the data. Also "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump". Hmm — "before the footer" — but we already removed the footer. So among remaining lines, find first bare number > nextFootnote. Log the jump (a missed number). 

Wait, there's an issue: the displaced footnote number D was removed from the footer and kept aside. The footnote block on that page: first footnote is bare number == nextFootnote (say 5), then blank, then text ending with full stop, then the unnumbered footnote (which is D=6), then footnote 7 etc. The rule: "On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D, marked repaired."

Hmm, so within the footnote block on a displaced page: parse openers normally (bare number or number+space). The first footnote's text: lines until next opener — but the next "opener" would be footnote 7's line, and the unnumbered footnote D's lines sit between footnote 5's text and footnote 7's opener. Without special handling, D's lines get glued to footnote 5's text. The special rule: if the page has a displaced number D, then the first footnote in the block ends at its first line ending with a full stop; lines after that (up to next numbered opener) are footnote D.

Wait — "the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop". So footnote 5's text is "A/79/270, paras. 84 and 85." — one line ending with full stop. Then "A/42/427, p. 24." is footnote 6 (D=6). Then footnote 7's opener line "7 ..." etc.

But hold on — what if the first footnote's text is multiple lines and the first line ends with a full stop but the footnote continues? The plan says "In all 12 cases the first footnote is one line ending with a full stop." So the rule works: end first footnote at first line ending with ".".

Hmm, but actually more precisely: the displaced footnote is the SECOND on the page. The first footnote is numbered (== nextFootnote). So: parse the block; when we encounter the first footnote on a displaced page, cut its text at the first line ending with a full stop; the remaining lines until the next numbered opener become footnote D.

Also: "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page." So after page 2: block has footnotes 5, 6(restored), 7, ... up to say 12. nextFootnote = max(highest seen, D) + 1.

Wait, also the jump rule: "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump; one missed number must never stop the count on the pages that follow." When would this happen? If a page's first footnote number is greater than nextFootnote (a gap — maybe a footnote number was lost entirely). Then we jump. Log it as a repair? The repair kinds don't include "jump"... The kinds are: header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed. Hmm, "footnote block removed" — that's when the block is separated from body? Maybe log "footnote block removed" once per page when the block is identified (the block lines removed from body). Actually "footnote block removed" likely means: the footnote block was removed from the body text — logged per page where a block exists. Let me log one repair per page: "footnote block removed (n lines)" when a block is found. And the jump logged as... maybe part of checks rather than repairs. The plan says "log the jump" — I'll log it as a repair of kind "footnote number restored"? No. Hmm. Let me add it to the repair log with kind "footnote block removed"? No. I could log the jump as a warning in checks. The plan: "take the first bare number greater than it that stands before the footer and log the jump". I'll log it in the repair log as kind... The listed kinds are "the ones named in the next section" — the kinds are fixed. Maybe the jump doesn't occur in this data (all 141 footnotes found). I'll log jumps as repairs with kind "footnote number restored"? That's wrong semantically. Alternatively I can add a kind "footnote count jumped" — but the plan says the kinds are those named. Since the jump presumably doesn't happen with this data (141 found of 141), I'll implement it and log it as a repair with kind "footnote number restored" only if it's a displaced restoration... Hmm. Let me just log jumps into the checks panel as a warning line, and also as a repair with kind "footnote block removed"? No.

Simplest: implement the jump; if it happens, log a repair {kind: 'footnote number restored', detail: 'count jumped from X to Y on page p (number X not seen)'}? That conflates. Actually, I'll create the repair entry with kind "footnote number restored" only for displaced numbers, and for jumps log kind "footnote block removed" with note? No — I'll just add the jump to the checks/warnings list and also as a repair with a distinct kind string "footnote count jumped" — the plan says the kinds are the ones named, but adding one more kind for an edge case that likely doesn't occur is harmless. Actually, to strictly follow, I'll log the jump as a repair with kind "footnote number restored" and detail explaining the jump... no. Let me re-read: "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page. If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump; one missed number must never stop the count on the pages that follow."

I'll log the jump in the repair log with kind "footnote number restored" — hmm no. OK decision: repairs have a `kind` field; I'll use the named kinds for the named events, and for a jump I'll use kind "footnote number restored" with what="footnote count jumped from a to b on page p (number a not found on any page)". Eh. Actually simpler: I'll allow kind "footnote count jumped" — the plan's list says "The kinds are the ones named in the next section" describing what appears; if a jump never occurs, the kind never appears. If it does occur, showing it is more honest. I'll include it as its own kind. Fine.

Now "footnote block removed" — when is it logged? I think: for each page where a footnote block is identified and removed from the body, log one repair "footnote block removed" with page and count of lines. That gives 20-ish entries (pages with footnotes). Hmm, or maybe it's logged once per footnote? "footnote block removed" singular per page seems right. Actually maybe per page: "footnote block removed (page 3, 5 footnotes)". I'll do per page.

Wait, but actually maybe "footnote block removed" means each footnote's block of lines removed from body — same thing per page. OK per page.

Now body parsing:

Body lines of all pages concatenated in page order, each tagged with page. Then:
- Lines before first paragraph start = cover. (Classified as "cover".)
- Paragraph starts: `/^(\d{1,3})\.$/` (number alone) → paragraph number, no first line; next lines are text. `/^(\d{1,3})\. (.+)$/` → number and text on one line; text after space is first line; log "number and text split".
- Headings: labelled `/^([IVX]+|[A-Z])\.$/` — e.g., "I.", "A.", "IV.". After a label line: skip blank lines, then every line up to the next label line or paragraph start is heading text. A line starting with lowercase or "(" continues the previous heading line (join with space, log "heading title joined from two lines"); any other line is a further heading (separate heading line). Hmm: "skip blank lines, then every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or '(' continues the previous heading line (logged as 'heading title joined from two lines'), any other line is a further heading."

So after "A." label, lines like "Right to work" then "(art. 6)" — "(art. 6)" starts with "(" → continues previous heading line → heading title becomes "Right to work (art. 6)", logged "heading title joined". A line starting with lowercase continues too. Other lines (starting with capital etc.) are further heading lines (each its own heading? or appended?). "any other line is a further heading" — I'll treat each as its own heading entry (a heading line). For section purposes, "the most recent heading line before it" — so multiple heading lines: the most recent one is the section. And `part` = most recent roman-numbered heading (I., II., ... — match /^[IVX]+\.$/).

Hmm wait, roman numeral regex: `/^([IVX]+|[A-Z])\.$/` — "I." matches [IVX]+; "A." matches [A-Z]. But "A." could also be... fine. Note: single letters A-Z as labels. But careful: a body line like "B." alone? That's a labelled heading per the rule. OK.

- Unlabelled heading: "a non-empty line immediately followed by a paragraph-start line, at most 90 characters, starting with a capital letter and not ending with a full stop, semicolon, colon, comma or digit (logged as 'heading separated from paragraph text')". So when scanning body lines, if line i is non-empty, line i+1 matches paragraph-start regex, and line i meets the criteria → it's a heading, not part of previous paragraph. Log "heading separated".

Wait — but what about the line before a paragraph start that does NOT meet the criteria (e.g., ends with a period)? Then it belongs to the previous paragraph. E.g., previous paragraph's last line followed by "23." — the last line ends with "." so it stays in the paragraph. Good.

But careful with ordering: the unlabelled-heading check needs lookahead. Implementation: iterate body lines with index; classify each line. For line i: if it matches paragraph-start → new paragraph. Else if it matches labelled heading → heading mode. Else if next line is paragraph-start and line meets unlabelled criteria → heading. Else → paragraph text of current paragraph (or cover if no paragraph yet).

Hmm, but also: what about lines between a heading and the paragraph? E.g.:
```
Right to work (art. 6)
12.
The Committee...
```
Line "Right to work (art. 6)" is followed by "12." → unlabelled heading. Good.

And labelled:
```
IV.

Environmental dimension...
A.
Right to work
(art. 6)
12.
```
Hmm wait — "IV." then blank then "Introduction" then "1." — "Introduction" is followed by "1." (paragraph start) — is "Introduction" an unlabelled heading? It's ≤90 chars, starts with capital, doesn't end with . ; : , or digit → yes, unlabelled heading. But it's also heading text after the "I." label. Conflict! The labelled-heading rule says: after label "I.", skip blanks, every line up to next label or paragraph start is heading text. So "Introduction" is consumed as heading text of "I." — the unlabelled rule shouldn't apply because we're in heading mode. So the classification must be stateful: when we hit a labelled heading, we consume subsequent lines as heading text until next label/paragraph start. So "Introduction" is part of heading "I. Introduction". Then "1." starts paragraph 1. Section of para 1 = "Introduction"? or "I. Introduction"? The plan: "Each paragraph's section is the most recent heading line before it and part the most recent roman-numbered heading". Hmm — "the most recent heading line". If heading "I." has title lines "Introduction", what's the "heading line"? I think the heading's full title: "I. Introduction"? Or just the last line? The plan for tab 02: "A Section column... shows the nearest heading above each paragraph ('Right to work (art. 6)'); the expanded paragraph shows the full path ('IV. … › Right to work (art. 6)')". So section = nearest heading (e.g., "Right to work (art. 6)"), part = roman heading ("IV."), and full path = "IV. … › Right to work (art. 6)" — hmm "IV. …" with ellipsis? The example shows "IV. … › Right to work (art. 6)". Maybe the roman heading's title too: "IV. Environmental dimension of sustainable development › Right to work (art. 6)"? The example literally shows "IV. … › Right to work (art. 6)". Hmm, maybe the roman heading title is long so it's shown as "IV. …"? I think the full path should be like "IV. <title> › <section>". But the example shows "IV. …". Maybe in the actual document, the roman heading is "IV." followed by a long title, and the path shows "IV. …" truncated? I'll build the path as: part label + title (if any) + " › " + section. E.g., "IV. Environmental dimension… › Right to work (art. 6)". Hmm, but to match the example exactly... The example "IV. … › Right to work (art. 6)" — maybe the roman heading in the doc is just "IV." with the title on the next line being long, and they show "IV. …". I'll construct path as `${partLabel}. ${partTitle} › ${section}` and if partTitle is long it's fine. Actually wait — maybe simpler: path = part (roman heading with its title) + " › " + section. I'll do that. The "…" in the example might just be eliding the title in the plan text. I'll include the title.

Hmm, actually let me reconsider: maybe headings structure: "IV." on its own line, then title lines. The heading entry = {label: "IV.", title: "Environmental dimension of sustainable development", level: 'roman'} or {label: "A.", title: "Right to work (art. 6)", level: 'letter'}. Unlabelled heading = {label: null, title: "Children", level: 'unlabelled'}. Section = most recent heading's title (full, with label if labelled?). The example section shows "Right to work (art. 6)" — that's the lettered heading's title without "A.". Hmm, or with? "Right to work (art. 6)" — the doc probably has "A." then "Right to work" then "(art. 6)". So section shows title only: "Right to work (art. 6)". And path: "IV. … › Right to work (art. 6)" — part shown as "IV." + maybe title elided. I'll show path as `IV. <part title> › <section title>` — but if the example shows "IV. …", maybe they truncate. I'll just include the part title; it's more informative. Actually, to be safe and match: path = partLabel + ". " + partTitle + " › " + sectionTitle. If partTitle empty, just partLabel + ".". Fine.

Wait, but what about unlabelled headings like "Children" — section = "Children", part = most recent roman. Path = "IV. … › Children". OK.

Now, heading consumption details: after a labelled heading line "A.", "skip blank lines, then every line up to the next label line or paragraph start is heading text". So:
```
A.
Right to work
(art. 6)
12.
```
Lines after "A.": skip blanks; "Right to work" — starts with capital, not lowercase/"(" → "a further heading" (its own heading line? or the first title line?). Hmm. "every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or '(' continues the previous heading line..., any other line is a further heading."

So the first line "Right to work" is heading text (a heading line). "(art. 6)" starts with "(" → continues previous heading line → joined: "Right to work (art. 6)". If there were another capital line "Something else", it'd be "a further heading" — a separate heading line. So a labelled heading can have multiple heading lines; the last one before the paragraph... hmm, "Each paragraph's section is the most recent heading line before it". So if heading "A." has lines "Right to work" and "(art. 6)" joined into one, section = "Right to work (art. 6)". If there were two separate lines, section = the most recent one. Hmm, that seems odd but OK — actually maybe "continues the previous heading line" applies to lowercase/"(" lines, and other lines are "further headings" meaning additional heading entries. For section, most recent heading line. But when "(art. 6)" joins "Right to work", the heading line becomes "Right to work (art. 6)" — one line. Good.

Wait, but what about roman headings: "IV." then blank then "Environmental dimension of sustainable development" — that line starts with capital → a heading line (the title). So heading = {label:"IV.", lines:["Environmental dimension of sustainable development"]}. If the title wraps: "General comment No. 27 (2025) on economic, social and" / "cultural rights and the environmental dimension of" / "sustainable development*" — wait that's the cover, before any paragraph. Cover lines are classified as cover (before first paragraph start). Hmm — but the cover contains "I." and "Introduction" and "1."! From the sample page 1: after the title, "I." then blank then "Introduction" then "1." then paragraph text. So "I." IS a labelled heading on page 1, and "Introduction" its title, and "1." starts paragraph 1. Lines before "I." (the cover proper: "United Nations", "Economic and Social Council", etc.) are cover. So "lines before the first paragraph start are the cover" — but "I." and "Introduction" come before "1." too! Hmm. The plan says "Lines before the first paragraph start are the cover." But then "I." and "Introduction" would be cover, not headings. But the heading rule would classify "I." as a labelled heading... Conflict.

Let me re-read: "**Paragraph starts.** A line matching ... Lines before the first paragraph start are the cover." and "**Headings.** A line matching `/^([IVX]+|[A-Z])\.$/` opens a labelled heading..."

Order of rules: paragraph starts first, then headings. Hmm, but the classification is one pass. I think the intended logic: process body lines sequentially; maintain state. A labelled heading line opens heading mode regardless. Lines before the first paragraph start that aren't headings are cover. So "I." on page 1 → heading; "Introduction" → heading title; "1." → paragraph start. Cover = lines before "I." (or before first paragraph start if no heading). Actually "Lines before the first paragraph start are the cover" — but "I." and "Introduction" are before "1."... 

Hmm. Maybe the intended reading: the cover is the lines before the first heading-or-paragraph-start? Or: when scanning, if we're in "cover" state (no paragraph yet, no heading yet), lines are cover; once a labelled heading appears, we're in heading mode. The plan's sentence is a simplification. But it matters for the "Nothing lost" check: every non-empty line classified exactly once as cover, header, heading, paragraph, footnote or footer. So "I." and "Introduction" must be classified as heading, not cover, presumably. Or as cover? If classified as cover, then paragraph 1's section would be... nothing. Hmm.

The plan says headings include roman-numbered sections ("I.", a blank line, "Introduction"). So "I." + "Introduction" is a heading. So classification: labelled heading lines and their titles are "heading". Cover = body lines before the first heading or paragraph start, whichever comes first. I'll implement: state machine over body lines:
- state = 'cover' initially.
- If line matches paragraph-start → start paragraph (state='body').
- Else if line matches labelled heading → heading mode: consume following lines per heading rules (they're 'heading').
- Else if in cover state → 'cover'.
- Else if next line is paragraph-start and line meets unlabelled criteria → 'heading' (unlabelled).
- Else → 'paragraph' (current paragraph's text) — but if no current paragraph (cover state), it's cover.

Wait but unlabelled heading check: "a non-empty line immediately followed by a paragraph-start line". In cover state, e.g., "Introduction" followed by "1." — but "Introduction" was already consumed as heading title of "I.". If there were a cover line followed by "1." without a preceding label... e.g., the title "sustainable development*" followed by "I." — "I." is a label line, not paragraph start. OK.

Hmm, what about page 1 sample: "General comment No. 27 (2025) on economic, social and\ncultural rights and the environmental dimension of\nsustainable development*\nI.\n\nIntroduction\n1.\nA clean, healthy..." — lines: "sustainable development*" then "I." — "I." matches labelled heading → heading mode. Then blank skipped, "Introduction" → heading title. Then "1." → paragraph start. So cover = everything before "I.". 

But wait — the unlabelled heading rule: "Introduction" is immediately followed by "1." (paragraph start), ≤90 chars, capital, no ending punctuation → it would qualify as unlabelled heading too, but it's consumed by the labelled heading rule first. Order matters: check labelled heading consumption first. In my state machine, after "I." we're in heading mode and consume until next label/paragraph-start. Good.

Now, what about a labelled heading line appearing mid-paragraph? E.g., paragraph text then "A." — the rule says a label line opens a heading. But could a paragraph line be "A."? Unlikely. OK.

Also careful: the unlabelled heading check must not fire for lines inside heading mode. State machine handles that.

Another subtlety: "a non-empty line immediately followed by a paragraph-start line" — what if the paragraph-start is "23. Some text" (number+text on one line)? Still a paragraph-start line. OK.

What about the LAST line of a page being a heading and the paragraph starting on the next page? Body lines are concatenated across pages, so lookahead works across pages. Good — that's why we concatenate first.

Now footnote marks in paragraph text. Sequential rule: "Walk through each paragraph's text in document order with a counter that starts at 1. Every run of one to three digits not touching another digit, a slash, a dash or an opening parenthesis is a candidate; a candidate equal to the counter is a mark and the counter goes up by one; any other number is left alone."

Implementation: process paragraphs in order; for each paragraph's joined text (raw, before marking), scan with regex for digit runs: /(?<!\d)(\d{1,3})(?!\d)/g — but also must not touch slash, dash, opening parenthesis: i.e., the char before the run must not be a digit (handled), and the char after must not be a digit, '/', '-', '('. Also char before must not be... "not touching another digit, a slash, a dash or an opening parenthesis" — touching on either side? "waste.2" — mark glued to word before: char before is '.', fine. "”. 3" — after a space. "equity, 17 common" — after comma+space. So the mark can be preceded by punctuation/space. The exclusion: if the run is preceded or followed by a digit (longer number), slash, dash, or '(' — e.g., "article 11" — hmm, "article 11": the run "11" is preceded by a space, followed by end/space. Why is "article 11" not a mark? Because of the sequential rule: candidate must equal the counter. If counter is at 5 and we see "11", it's not equal → left alone. But what if counter is at 11 and text says "article 11"? Then it would wrongly bracket. The plan says "real numbers such as 'article 11' look the same, so only a sequential rule tells them apart" — meaning the sequential rule is the only way, and it works because marks appear in order 1,2,3,... and real numbers rarely equal the current counter at the right position. Hmm, risky but that's the spec. Also "not touching ... an opening parenthesis" — e.g., "(11)" — the run followed by ')' preceded by '(' → not a candidate. And "11/2023" — followed by '/' → not candidate. "2025-07" — dash. OK.

So candidate regex: a run of 1-3 digits where: char before is not [0-9/-(] and char after is not [0-9/-(]. Wait "not touching another digit, a slash, a dash or an opening parenthesis" — touching means adjacent on either side. So before-run char ∉ {digit, '/', '-', '('} and after-run char ∉ {digit, '/', '-', '('}. Hmm, what about closing paren after? "(see para 5)" — "5" followed by ")" — that's allowed as candidate? The spec only excludes opening parenthesis. Hmm, "para 5)" — the 5 is followed by ')'. Per spec, ')' is not excluded, so it's a candidate. If counter==5, it'd be marked. Risky but spec. Actually wait — maybe the exclusion of '(' is because footnote references like "(see footnote 12)"? Eh, follow spec.

Also: should the char before exclude letters? "waste.2" — before is '.', OK. What about "art.11"? before is '.', fine. What about a word like "COVID19"? run "19" preceded by 'D' (letter) — letters not excluded, so "19" is a candidate if not touching digits... "COVID19": the run is "19"? Actually "COVID19" — digits "19" preceded by 'D'. Per regex, candidate. If counter==19 it'd be marked. Spec says only digit/slash/dash/open-paren excluded. Follow spec.

Implementation: for each paragraph in document order, take raw joined text, use regex with lookbehind/lookahead: /(?<![\d\/\-(\d])(\d{1,3})(?![\d\/\-(\d])/g — hmm lookbehind must be fixed-width in JS? JS supports variable-length lookbehind actually (ES2018 allows variable-length lookbehind in JS!). Yes, JavaScript supports variable-length lookbehind. But to be safe, I'll do manual scanning: iterate matches of /\d{1,3}/g hmm that would match within longer numbers. Better: /\d+/g and check length ≤3 and neighbors. Let me do: text.replace(/(\d+)/g, cb) — for each digit run, if run.length ≤ 3 and char before (m.index-1) not in excluded set and char after not in excluded set → candidate. Then if candidate == counter → mark, counter++. Else leave as-is (and record as "rejected number" for the check with context).

Wait, but the counter walks "through each paragraph's text in document order" — so counter persists across paragraphs. Marks found should run 1..141. The check: "Marks found in the paragraphs, expected to run from 1 to reference.footnotes without a gap; the check lists any missing numbers and the numbers it rejected as not being marks (with context)".

Marking: replace the candidate digits with `[n]` in the text. "Each mark becomes [n], the character before it kept ('waste.[2]', 'equity,[17] common')". So "waste.2" → "waste.[2]". Just insert brackets around the digits.

Note: marks are applied to the paragraph text for display/CSV `text`; `text_raw` keeps unmodified.

First words: from the marked text? "first_words_found = the first six whitespace-separated words of the joined text, footnote marks removed first". So take text (with marks), remove `\[\d+\]`, then split on whitespace, take 6, join with space. Compare with reference.first_words[String(n)] after normalisation (curly quotes→straight, en/em dash→hyphen, whitespace runs→single space). Case kept.

Hmm wait — "footnote marks removed first" — remove the bracketed marks. But what if the mark was glued: "waste.[2]" → removing "[2]" gives "waste." — good.

Now checks:

1. Paragraph count: found vs reference.paragraphs.
2. Numbering: numbers exactly 1..n in order; list gaps/duplicates by number and page.
3. First words: count mismatches, list "para. n: found … / reference …".
4. Footnotes: found vs reference.footnotes; numbers run 1..count without gap/duplicate; restored numbers listed with page.
5. Footnote marks: marks found run 1..reference.footnotes without gap; list missing numbers and rejected numbers with context.
6. Footnotes stay out of paragraphs: for every footnote opener line (first 40 chars including its number), search in raw text of every paragraph (before marks touched) — expected 0 hits. Also list paragraphs over 300 words. A hit → check fails, paragraph flagged, tile says "n contain footnotes".
7. Headers and footers: pages whose first line was the symbol (expected all); pages with page number in footer (expected all but first); displaced footnote numbers listed with page.
8. Headings: count of labelled and unlabelled headings; list of unlabelled ones.
9. Nothing lost: every non-empty line classified exactly once; counts per kind sum to total non-empty lines; unclassified lines listed with page, shown red in raw viewer.

Header check: "Pages whose first line was the symbol (expected all)" — page 1's first line is the symbol "E/C.12/GC/27" per sample. So all 20 pages have header. Footer page number: pages 2-20 have bare page number; page 1 has date stamp instead. So "pages with a page number in the footer (expected all but the first)".

Now the "n of m checks pass" — m = number of checks (9). Each check passes or fails. If reference missing → "not run".

Now the UI. Let me design:

- Header: monospace label "UN DOCUMENT · PDF TEXT", serif title, line with symbol link, adopted, "n pages of raw converter text", source. One sentence what the page does. Right side: green/red dot + "n of m checks pass".
- Left rail: "DOCUMENT" heading; card(s). Card: symbol monospace, short title (title? "its short title" — pdf_text has `title`; use title, maybe truncated), "adopted …", "n pages". Two big serif numbers: paragraphs found (with "of reference.paragraphs" and thin bar showing share, red when short or over), footnotes found similarly, then "n of m checks pass" link to tab 04. Selected card red left border.
- Tabs: 01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD. role=tablist, arrow keys.
- Footer always visible: source line, built date, honesty line.

Wait — does pdf_text have `built`? The description: `{title, symbol, doc_url, source, count, records, reference}`. No `built`. The footer says "Source line, `built` date". Hmm — pdf_text has `source` but maybe not `built`. I'll show built if present, else omit or show source only. Handle missing gracefully: `data.built ? ... : ''`. Actually the header line says "one line with the data's source, n and years" — for this app: symbol linked, adopted, n pages, source. Footer: source line, built date (if present), honesty line. I'll conditionally include built.

Tab 01 RESULT: four tiles: Paragraphs found n (next to "The document has: reference.paragraphs", green when equal, red with difference); Footnotes found n of reference.footnotes; First words match n of reference.paragraphs; Repairs made n (link to repair log on tab 04). Each tile with "How this is computed" note.

Tab 02 PARAGRAPHS: collapsible "Headings found: n" box above table. Table columns: No. | Section | Page | First line | Check. Rows are buttons with aria-expanded; click expands in place showing full text, "Show the PDF's lines" toggle, reference first words vs found, pages, repairs touching this paragraph, Copy citation button. Footnote marks shown as [n] in table/expanded/CSV; note under table with pattern \[\d+\].

Wait, column order per plan: "No. | Page | First line | Check" and "A Section column, between No. and Page". So: No. | Section | Page | First line | Check.

Page cell: "the page(s) it starts and ends on ('3–4' across a page break)" — so "3" or "3–4".

Expanded row: full text verbatim; toggle "Show the PDF's lines" reveals text with converter's line breaks and page number where each page began; under the text: reference's first six words next to extracted first six words, equal/different; the page(s); repairs that touched this paragraph; Copy citation button copying "symbol, para. n", shows "Copied" 2s.

Tab 03 FOOTNOTES: table "Footnotes found: n of reference.footnotes", columns No. | Page | Text | Repair. Repair reads "number restored from the page foot" for restored. Expanded paragraph also lists footnotes it cites — hmm, "The expanded paragraph also lists the footnotes it cites" — that's on tab 02's expanded row: list footnote numbers cited (the marks). Download button "footnotes.csv" on this tab. Footnotes CSV columns? Not specified — I'll do number, page, text, repair, citation? Let me do: number, page, text, repaired, symbol, doc_url. Reasonable.

Tab 04 CHECKS & METHOD: check panel open, every check one line. Then closed heading "Repair log (n)" button aria-expanded — table Page | Paragraph or footnote | What was done | Before | After, with count per kind above. Then closed heading "Raw pages" — select "Show raw page n" + monospaced panel with line numbers, each line coloured by classification, legend. Then Download: "Download paragraphs as CSV" with specified columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, footnotes_cited, repairs, citation, symbol, doc_url. UTF-8 BOM, all fields double-quoted, inner quotes doubled, CRLF, Blob URL, filename from symbol with slashes→hyphens. Note: the plan mentions CSV column `text_lines` in the pipeline section ("text_lines keeps the original lines for the toggle and the CSV column text_lines") but the download column list doesn't include text_lines... The column list: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, footnotes_cited, repairs, citation, symbol, doc_url. Hmm, text_lines mentioned earlier but not in the list. I'll include text_lines too? The list is explicit; but earlier says "the CSV column text_lines". Conflict. I'll include text_lines after text_raw — it says "keeps the original lines for the toggle and the CSV column text_lines (lines separated by ' | ')". So the CSV should have text_lines. The later list omits it, but the earlier explicitly names it as a CSV column. I'll include it (harmless, more complete). Actually, to strictly follow the explicit column list... The explicit list is what "Download paragraphs as CSV" produces. The earlier sentence says text_lines is a CSV column. I'll include text_lines between text_raw and footnotes_cited. Both instructions can be satisfied.

CSV escaping: every field double-quoted, inner quotes doubled, CRLF line ends, BOM \uFEFF.

Now the raw page viewer: select "Show raw page n", monospaced panel with the page's text as stored, line numbers left, each line coloured by classification (cover, header, heading, paragraph, footnote, footer), legend with six pale tints + letter codes (C, H, D?, ...). Letter codes: cover=C? header=H, heading=D? Let me pick: cover "CV"? single letters: cover=C, header=H, heading=G? Hmm. Let me use: cover "C", header "H", heading "T" (title)? The plan says "each doubled by a letter code in the margin and in the legend". I'll use: C=cover, H=header, G=heading (G for "graf"? eh) — maybe: cover "c", header "h", heading "t" (title), paragraph "p", footnote "f", footer "r"? Let me choose clear ones: COVER=C, HEADER=H, HEADING=T, PARAGRAPH=P, FOOTNOTE=F, FOOTER=R? Hmm "R" for footer... maybe "E" (end)? I'll use: C cover, H header, T heading, P paragraph, N footnote (note), F footer. Eh. Let me just do: cover=C, header=H, heading=D (de-head?)... Simpler: cover=C, header=H, heading=T, paragraph=P, footnote=N, footer=F. Fine.

Classification per line: I need to track, for each original line of each page (by page + line index), its classification. During parsing I'll record for each line: {page, idx, text, cls}. Header lines → 'header'; footer lines → 'footer'; footnote block lines → 'footnote'; body lines → 'cover'/'heading'/'paragraph'. Every non-empty line classified exactly once. Empty lines: not counted (the "nothing lost" check counts non-empty lines). In the raw viewer, show all lines including empty ones (as stored), with empty lines uncoloured.

Now repairs log entries: {page, target (e.g., "para. 12" or "footnote 6"), kind, before, after}. Kinds:
- "header line removed": before = the symbol line, after = "" (removed). Page.
- "footer line removed": per footer line? Or per page? "footer line removed" — I'll log each footer line removed? That'd be ~3 per page × 20 = 60 entries. Hmm, maybe log one per page summarizing. The table has Before | After columns — for footer, before could be the removed lines joined, after "(removed)". I'll log one entry per page listing the removed footer lines: before = lines joined with " / ", after = "removed". Kind "footer line removed". Similarly header one per page. That keeps the log manageable. Actually per-line might be more precise but noisy. The plan: "a table of every change the script made, in document order, Page | Paragraph or footnote | What was done | Before | After, with a count per kind above it". "every change" — per line then? Header: 20 changes. Footer: ~60. That's fine actually, table can be long. But "footer line removed" per line: before = line, after = "". Hmm, I'll do per-line for header and footer — it's "every change". Actually, let me reconsider: 20 header + ~60 footer + 2 splits + 19 joins + ~23 heading separations + ~few joins + 12 restorations + ~20 block removals ≈ 160 rows. That's OK for a table. But maybe group footer per page to keep it readable... The plan says "every change the script made". I'll log per-line for header/footer. Hmm, but then Before/After columns: before = the line text, after = "(removed)". OK.

Actually wait — for "footnote block removed", per page: before = "n lines at foot of page p", after = "moved to footnotes". I'll do per page.

- "number and text split": before = "23. The Committee...", after = "23." + "The Committee..." (number separated from first text line). Target para 23.
- "paragraph joined across a page break": target para n, before = "…end of page p / start of page p+1…", after = joined text. Page = p–p+1? Page column: the pages involved. I'll put "p–p+1".
- "heading separated": before = heading line glued context, after = "heading: 'Right to work (art. 6)'". Target = the paragraph it precedes? "Paragraph or footnote" column — for heading separated, target = "para. 12" (the paragraph it now precedes) or the heading itself. I'll put target = heading text or "before para. n". I'll use "para. n" where n is the following paragraph.
- "heading title joined from two lines": before = "Right to work" + "(art. 6)", after = "Right to work (art. 6)".
- "footnote number restored": target footnote D, page p, before = "A/42/427, p. 24. (no number; '6' displaced to page foot)", after = "6 A/42/427, p. 24.".
- "footnote block removed": page p, before = "footnote block, n lines", after = "removed from body".

Count per kind above the table: e.g., "header line removed ×20 · footer line removed ×58 · …".

Now, the pipeline must also handle the second document (pdf_text_2) generically — same code, run per document. The app runs the pipeline for each document in WORKSHOP_DATA with records+reference, stores results, and the rail switches between them. "Today there is one" — but code handles many. I'll run pipeline for all found docs on load (cheap), render selected.

Hmm wait — should I include pdf_text_2? The user attached only pdf_text. The system prompt says build only on attached files. But the plan says scan WORKSHOP_DATA. In the actual runtime, WORKSHOP_DATA presumably contains only what's attached (pdf_text). The preview shows pdf_text_2 but that's the preview. The plan says "every document in WORKSHOP_DATA with records and a reference gets its own card... Today there is one." This strongly implies at runtime only pdf_text has records+reference... but the preview data includes pdf_text_2 with records and reference. Hmm, "Today there is one" — maybe meaning in this workshop instance. If I scan generically and pdf_text_2 is present, two cards appear — which actually matches "the app is written so that every document... gets its own card". I think generic scanning is intended and safe: if only pdf_text is attached at runtime, one card; if both, two cards. The plan explicitly describes this behavior. Go generic.

Wait, but the "Files" rule: "Build apps only on files attached in this conversation." If pdf_text_2 is in WORKSHOP_DATA but not attached... The user's plan overrides with explicit instruction. Also the system prompt lists pdf_text_2 as available data. I'll scan generically — it satisfies the plan either way.

Hmm, actually, let me reconsider once more. The rule exists so I don't hallucinate data. Scanning WORKSHOP_DATA keys is not hallucinating. The plan says to do it. OK.

Now let me think about parsing details more concretely, then write the code.

```js
function parseDocument(data) {
  const symbol = data.symbol;
  const records = [...data.records].sort((a,b)=>a.page-b.page);
  const repairs = [];   // {page, target, kind, before, after}
  const warnings = [];
  const lineClass = []; // per page: array of {idx, text, cls}
  // classification counts
  const classCounts = {cover:0, header:0, heading:0, paragraph:0, footnote:0, footer:0, unclassified:0};
  
  let nextFootnote = 1;
  const footnotes = []; // {number (str, or '*'), page, text, repaired, openerLine (first 40 chars incl number), lines:[...]}
  const bodyLines = []; // {page, text}
  
  records.forEach(rec => {
    const page = rec.page;
    const rawLines = rec.text.split('\n');
    // classify each line index
    const cls = rawLines.map(()=>null);
    // header
    let i = 0;
    while (i < rawLines.length && rawLines[i].trim()==='') i++;
    if (i < rawLines.length && rawLines[i].trim() === symbol) {
      cls[i] = 'header';
      repairs.push({page, target:'page header', kind:'header line removed', before: rawLines[i], after:'(removed)'});
      i++;
    } else {
      warnings.push(`page ${page}: first non-empty line is not the symbol`);
    }
    // footer: from end
    let j = rawLines.length - 1;
    const displaced = [];
    const footerRemoved = [];
    while (j >= i) {
      const t = rawLines[j].trim();
      if (t === '') { j--; continue; }
      if (/^GE\./.test(t)) { cls[j]='footer'; footerRemoved.push(rawLines[j]); j--; continue; }
      if (/^(\d{6} )*\d{6}$/.test(t)) { cls[j]='footer'; footerRemoved.push(rawLines[j]); j--; continue; }
      if (/^\d{1,3}$/.test(t)) {
        cls[j]='footer';
        const n = parseInt(t,10);
        if (n === page) { /* page number */ }
        else displaced.push(n);
        footerRemoved.push(rawLines[j]);
        j--; continue;
      }
      break;
    }
    // log footer removals
    footerRemoved.forEach(line => repairs.push({page, target:'page footer', kind:'footer line removed', before: line, after:'(removed)'}));
    // hmm: order — repairs should be in document order; footer at end of page. Since we process pages in order and within a page we push header then footer... but body repairs come later. Document order within a page: header (top), body, footnotes, footer (bottom). My push order: header, footer, then footnote block, then body. Not document order. I should sort repairs at the end by page and a sequence number. Let me add a seq counter per line position: I'll record repairs with an order key (page, lineIndex) and sort at the end. For body-level repairs (joins, splits, headings), the line index is known. For footer, line index j. Let me store {page, line: idx, ...} and sort by (page, line). For paragraph joins across pages, line = first line index of the paragraph's continuation... eh, approximate. I'll sort by page then line index; for synthetic entries use the relevant line index.
```

Hmm, this is getting complex. Let me simplify: each repair gets `page` and `ord` (line index within page, or Infinity for page-level). Sort by page, then ord. Good enough for "document order".

Continue per page:

```js
    // remaining lines: i..j (inclusive) after header/footer removal
    const lines = [];
    for (let k = i; k <= j; k++) lines.push({idx:k, text: rawLines[k]});
    // find footnote block start
    let blockStart = -1;
    for (const L of lines) {
      const t = L.text.trim();
      if (t === '') continue;
      if (/^\d{1,3}$/.test(t) && parseInt(t,10) === nextFootnote) { blockStart = L.idx; break; }
      if (new RegExp('^'+nextFootnote+' ').test(t)) { blockStart = L.idx; break; }
      if (page === records[0].page && t.startsWith('* ')) { blockStart = L.idx; break; }
    }
```

Wait — "starts with that number and a space": `^nextFootnote ` — but careful with regex special chars; nextFootnote is a number, fine. But also "starts with that number and a space" — e.g., nextFootnote=5, line "5 A/79/270..." starts with "5 " → opener. But a body line "5 something"? The rule accepts it. Also bare number equal to nextFootnote. Hmm, also what about a line starting with nextFootnote but followed by "."? "5." — that's a paragraph start, not "5 " (no space). OK.

But wait — there's a subtle issue: on page 1, nextFootnote=1. Body contains "1." (paragraph start) — not "1" bare, not "1 ". Good. But what about the cover line "6 November 2025"? starts with "6 " — nextFootnote is 1, so no match. Good. What if a body line starts with "1 " on page 1 before the footnote block? E.g., a wrapped line starting with "1 "? Possible in theory; the plan says the rule works on this data. But hmm — page 1: does the footnote block start on page 1? Footnotes 1-4 presumably on page 1. The first opener: bare "1"? or "1 ..."? In UN docs, first footnote on a page is often bare number on its own line then blank then text (per plan: "The first on a page is a bare number on its own line, a blank line, then the text"). So page 1 block starts at bare "1". But wait — the cover has "1." paragraph start BEFORE the footnote block. "1." is not bare "1" (has period). OK good.

But danger: what if a body line is exactly "1" (bare)? No.

Also the jump rule: if no opener found, find first bare number > nextFootnote among lines (before footer — already removed): 

```js
    if (blockStart === -1) {
      for (const L of lines) {
        const t = L.text.trim();
        if (/^\d{1,3}$/.test(t) && parseInt(t,10) > nextFootnote) { blockStart = L.idx; log jump; break; }
      }
    }
    if (blockStart === -1) {
      // all body; check panel notes page has no footnote block
      warnings.push(`page ${page}: no footnote block found; all lines are body`);
    }
```

Then: body = lines with idx < blockStart; footnote block = lines idx >= blockStart.

Classify: footnote block lines → cls 'footnote'; body lines → pushed to bodyLines with page; their cls set later during body parsing (cover/heading/paragraph).

Footnote block parsing:

```js
    if (blockStart !== -1) {
      const block = lines.filter(L => L.idx >= blockStart);
      // mark cls
      block.forEach(L => cls[L.idx] = 'footnote');
      repairs.push({page, target:'footnote block', kind:'footnote block removed', before: block.length + ' lines at the foot of page ' + page, after: 'moved out of the body text'});
      // parse footnotes within block
      let cur = null; // {number, lines:[], page}
      const pageDisplaced = displaced; // array of numbers
      let firstFootnoteDone = false;
      for (const L of block) {
        const t = L.text; const tt = t.trim();
        if (tt === '') continue; // blank lines dropped inside footnotes? Hmm — "The first on a page is a bare number on its own line, a blank line, then the text" — blank line after bare number is skipped. Blank lines within footnote text? Probably none. I'll skip blanks.
        const bare = /^(\d{1,3})$/.exec(tt);
        const numSpace = /^(\d{1,3}) (.+)$/.exec(tt);
        if (bare || numSpace) {
          // close current
          if (cur) footnotes.push(finish(cur));
          const num = bare ? bare[1] : numSpace[1];
          cur = {number: num, page, lines: [numSpace ? numSpace[2] : ''], opener: tt.slice(0,40), repaired:false};
          ...
        } else if (tt.startsWith('* ') && page === firstPage) {
          if (cur) push; cur = {number:'*', ...};
        } else {
          // continuation line
          if (cur) {
            // displaced-page special: first footnote ends at first line ending with full stop
            if (pageDisplaced.length && cur === firstFootnoteOfPage && !cur.closed) {
              if (cur.lines.some(l => l.trim().endsWith('.'))) {
                // split: lines up to and including first line ending with '.' stay; rest go to footnote D
                ...
              }
            }
            cur.lines.push(tt);
          }
        }
      }
    }
```

Hmm, the displaced handling: "On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D, marked repaired."

So specifically: the FIRST footnote in the block on a displaced page. Its text lines: accumulate; when a line ends with '.', that's the end of the first footnote; subsequent non-opener lines until the next numbered opener belong to footnote D.

Implementation: track `firstFn` = the first footnote object created on this page (if pageDisplaced.length > 0). While accumulating lines into firstFn, check after adding each line whether it ends with '.'; if yes and pageDisplaced.length, then set a flag `splitNext` — the NEXT continuation lines (until next opener) go to a new footnote D instead. Actually simpler: when adding a continuation line to firstFn, if pageDisplaced.length && firstFn is the first footnote && firstFn.lines already contain a line ending with '.' (i.e., this is after the terminating line), then this line starts footnote D: close firstFn, create cur = {number: String(D), repaired: true, ...} and add the line.

Wait, order: lines of first footnote: ["A/79/270, paras. 84 and 85."] — ends with '.'. Next line "A/42/427, p. 24." — when we encounter it as continuation: check if firstFn (current cur) is the page's first footnote and pageDisplaced.length>0 and cur already has a line ending with '.' → then this line belongs to footnote D. So: close cur (footnote 5), create footnote D with this line, mark repaired, log repair "footnote number restored". Then subsequent lines until next opener go to D. Then "7 ..." opener closes D.

But careful: what if the first footnote's text is multiple lines and only the last ends with '.'? "ends at its first line that ends with a full stop" — so the first line ending with '.' terminates it. If footnote 5's text were "A/79/270, paras. 84 and\n85." — first line doesn't end with '.', second does → footnote 5 = both lines; next line goes to D. OK, my logic: when a continuation line arrives and cur is firstFn and pageDisplaced and cur.lines.some(ends with '.') → move to D. That means the line AFTER the first '.'-ending line goes to D. Correct.

Edge: what if D's lines themselves contain a line ending with '.'? Doesn't matter — once we switch to D, all continuation lines go to D until next opener.

Also: what if displaced page's first footnote is NOT the bare-number one? Plan says in all 12 cases the first footnote is the bare number + blank + one-line text. Fine.

Also the asterisk footnote: number '*', not counted in footnotes count. Keep in list with number '*'.

Advance nextFootnote: after parsing block, nextFootnote = max(highest number seen in block (numeric), displaced numbers, nextFootnote) + 1. "Advance nextFootnote past the highest number seen in the block and past any displaced number for that page." So nextFootnote = max(all numbers in block, displaced, nextFootnote) + 1.

Hmm wait — but what about the jump case: block starts at bare number > nextFootnote (jump). Then numbers seen include that. Fine.

Also: what if a page has NO footnote block (blockStart === -1)? Then nextFootnote unchanged. Warning logged.

Hmm, one more: the block-start scan looks for opener matching nextFootnote. But what if the page's first footnote is a displaced one? I.e., the page's first footnote number was displaced to the footer, so the block starts with... the plan says on displaced pages, the first footnote IS numbered (bare number == nextFootnote) and the SECOND is displaced. So block start found normally. Good.

But wait — what if nextFootnote's opener is missing because that footnote was displaced AND it's the first on the page? Plan says the displaced one is always the second. OK.

Now body parsing:

```js
  // bodyLines: [{page, text, idx}] in page order
  const paragraphs = [];
  const headings = []; // {label, title, lines, page, kind:'roman'|'letter'|'unlabelled', lineIdx}
  let cur = null; // current paragraph {number, lines:[{page,text}], ...}
  let state = 'cover'; // 'cover' | 'body'
  let headingMode = null; // {label, lines:[], page}
  
  for (let i = 0; i < bodyLines.length; i++) {
    const L = bodyLines[i];
    const t = L.text; const tt = t.trim();
    if (tt === '') continue; // blank lines dropped (but classified? blank lines are not non-empty; skip)
    const paraAlone = /^(\d{1,3})\.$/.exec(tt);
    const paraText = /^(\d{1,3})\. (.+)$/.exec(tt);
    const label = /^([IVX]+|[A-Z])\.$/.exec(tt);
    
    if (paraAlone || paraText) {
      // close heading mode if any
      if (headingMode) { headings.push(finishHeading(headingMode)); headingMode = null; }
      if (cur) paragraphs.push(finishPara(cur));
      const num = (paraAlone||paraText)[1];
      cur = {number: num, lines: [], startLine: L};
      if (paraText) {
        cur.lines.push({page: L.page, text: paraText[2]});
        repairs.push({page: L.page, target: 'para. '+num, kind:'number and text split', before: tt, after: num+'. | '+paraText[2], ord: L.idx});
      }
      state = 'body';
      L.cls = 'paragraph';
      continue;
    }
    if (label) {
      if (headingMode) headings.push(finishHeading(headingMode));
      if (cur) { paragraphs.push(finishPara(cur)); cur = null; }
      headingMode = {label: label[1], labelLine: L, titleLines: [], page: L.page, kind: /^[IVX]+$/.test(label[1]) ? 'roman' : 'letter'};
      L.cls = 'heading';
      continue;
    }
    if (headingMode) {
      // heading text lines until next label or paragraph start
      const next = bodyLines[i+1];
      const nextIsLabel = next && /^([IVX]+|[A-Z])\.$/.test(next.text.trim());
      const nextIsPara = next && (/^(\d{1,3})\.$/.test(next.text.trim()) || /^(\d{1,3})\. /.test(next.text.trim()));
      if (nextIsLabel || nextIsPara) {
        headings.push(finishHeading(headingMode)); headingMode = null;
        // reprocess current line? No — current line is heading text; but if next is label/para, current line is the last heading line. Handle: treat current as heading text, then next iteration handles label/para.
        headingMode = null;
        // fall through to classify current line as heading
        classifyHeadingLine(headingModeJustClosed, L);
        continue;
      }
      // heading text
      ...
    }
    ...
  }
```

Hmm, this is getting tangled. Let me restructure with a cleaner state machine:

States: 'cover', 'heading' (with current heading object), 'para' (with current paragraph object).

For each non-empty body line L (with lookahead to next non-empty body line? or next line including blanks? "a non-empty line immediately followed by a paragraph-start line" — immediately followed in the raw line sequence, but blanks between? "immediately followed" — I'll use next non-empty body line, since blank lines are dropped. Hmm, "immediately followed by a paragraph-start line" — in the concatenated body lines, blanks are dropped, so "immediately" = next non-empty line. I'll use next non-empty.)

Wait, but for heading mode: "skip blank lines, then every line up to the next label line or paragraph start is heading text". So within heading mode, blanks skipped, lines until next label/para are heading text. So lookahead should be next non-empty line.

Let me define nb[i] = index of next non-empty body line after i.

Algorithm:

```js
for i in bodyLines:
  L = bodyLines[i]; tt = trim(L.text); if (!tt) continue;
  next = nextNonEmpty(i); ntt = next ? trim(bodyLines[next].text) : '';
  
  if (isParaStart(tt)) {
    closeHeading(); closePara();
    start new para; if paraText form, add first line + repair;
    L.cls='paragraph'; continue;
  }
  if (isLabel(tt)) {
    closeHeading(); closePara();
    headingMode = new heading; L.cls='heading'; continue;
  }
  if (headingMode) {
    // current line is heading text (since next isn't label/para? not necessarily — if next IS label/para, current is still heading text, the last one)
    // Actually: "every line up to the next label line or paragraph start is heading text" — so current line is heading text regardless; heading ends when we ENCOUNTER a label/para line.
    addHeadingLine(L); L.cls='heading'; continue;
  }
  // not in heading mode
  if (state==='cover') {
    // could be unlabelled heading if next is para start and criteria met
    if (isParaStart(ntt) && isUnlabelledHeading(tt)) {
      headings.push({label:null, title:tt, kind:'unlabelled', page:L.page});
      repairs.push({... kind:'heading separated', target:'before para. '+ntt-num ...});
      L.cls='heading'; continue;
    }
    L.cls='cover'; continue;
  }
  // in para
  if (isParaStart(ntt) && isUnlabelledHeading(tt)) {
    // this line is a heading, not paragraph text
    closePara();
    headings.push({label:null, title:tt, kind:'unlabelled', page:L.page});
    repairs.push({kind:'heading separated', target:'para. '+(num of ntt), before: tt, after:'heading: '+tt});
    L.cls='heading'; continue;
  }
  // paragraph text
  L.cls='paragraph';
  cur.lines.push({page:L.page, text: tt});
```

Wait — issue: in heading mode, when do we close the heading? When we encounter a label or para-start line — handled at top of loop (closeHeading before starting new). But also: heading mode should end at... only label or para start. What if body ends? Close at end. OK. But there's a subtlety: after heading mode, the next line could be another heading text line? No — heading text continues until label/para. So all lines in heading mode are heading text. But what if a heading is followed by another heading without paragraph between? E.g., "IV." title, then "A." — "A." is a label → closeHeading, start new heading. Good.

Hmm wait, but there's a problem: in heading mode, EVERY line is heading text — including lines that would be unlabelled headings? E.g.:
```
A.
Right to work
(art. 6)
12.
```
"Right to work" — heading text (starts with capital → "a further heading" — its own heading line within the heading). "(art. 6)" starts with "(" → continues previous heading line → joined. So heading object has lines: ["Right to work (art. 6)"] after joining. Implementation of addHeadingLine: if tt starts with lowercase or '(' and heading.titleLines.length>0 → append to last title line with space, log "heading title joined from two lines". Else → push as new title line.

Hmm — "a line starting with a lowercase letter or '(' continues the previous heading line (logged as 'heading title joined from two lines'), any other line is a further heading". So each capital-starting line is a separate heading line. For section purposes "the most recent heading line" — so if heading "A." has lines ["Right to work", "Something"], section = "Something"? That seems odd but per spec. In practice probably one title line per heading (plus joined continuations). For the roman heading "IV." + title — one line. OK.

But wait — what about the heading title for roman: "I." then "Introduction" — heading {label:'I.', titleLines:['Introduction']}. Section for para 1 = most recent heading line = "Introduction"? And part = "I."? The plan example: section shows "Right to work (art. 6)" (no label), path shows "IV. … › Right to work (art. 6)". So section = title line (without label), part = roman label. For para 1, section = "Introduction", part = "I.". Path = "I. Introduction"? Hmm, path format "IV. … › Right to work (art. 6)" — the "…" suggests the roman heading's title is elided or long. I'll build path as: part ? (partLabel + '. ' + partTitle + ' › ') : '' + section. Where partTitle is the roman heading's (last) title line. If partTitle empty → "IV. › ...". Hmm the example "IV. …" — maybe they show "IV." + ellipsis because title long. I'll just include the title; if it's long, fine. Actually, let me match the example more closely: maybe path = partLabel + '.' + (partTitle ? ' ' + truncate(partTitle, 40) + '…' : '') ... overengineering. I'll do: path = [partLabel + '. ' + partTitle (if any), section].join(' › '). E.g., "IV. Environmental dimension of sustainable development › Right to work (art. 6)". Good enough and informative.

Hmm wait, actually — what is `part` in the CSV? "part" column = the most recent roman-numbered heading. I'll store part = "IV." or "IV. Title"? CSV `part` — I'll store the roman label + title, e.g., "IV. Environmental dimension...". And `section` = most recent heading line title (e.g., "Right to work (art. 6)"). For para 1: section="Introduction", part="I. Introduction"? Hmm, part should probably be just the roman heading. I'll make part = label + (title ? ' ' + title : '') e.g. "IV. Environmental dimension of sustainable development". And section = last heading line (title only, no label) e.g. "Right to work (art. 6)" or "Introduction". Path = part + ' › ' + section.

Unlabelled heading criteria: non-empty, immediately followed by paragraph-start line, ≤90 chars, starts with capital letter, not ending with . ; : , or digit. Note: "starting with a capital letter" — /^[A-ZÀ-Þ]/? Use /^[A-Z]/ plus maybe accented; I'll use /^[A-ZÀ-ÖØ-Þ]/u... simpler: /^[A-Z]/ on the first char, plus allow unicode uppercase via /\p{Lu}/u. I'll use /^\p{Lu}/u. Not ending with [.;:,] or digit: /[.;:,\d]$/ → excluded.

Wait — but there's an issue: the unlabelled heading check in 'cover' state: on page 1, "Introduction" is consumed by heading mode (after "I."), so fine. But what about cover lines followed by para start? E.g., if "I." weren't there. Fine.

Another subtlety: what if a paragraph's last line is followed by a paragraph-start line and meets unlabelled criteria? E.g., paragraph ends "...the following:" — ends with ':' → excluded. "...in 2025." ends with '.' → excluded. A line like "Children" followed by "12." → heading. But what if a paragraph's last line is like "The Committee recommends the following" (no ending punctuation, ≤90, capital) followed by "13."? Then it'd be misclassified as heading. The plan says 23 unlabelled headings exist and the rule works. Trust it.

Hmm wait, actually there's a risk: paragraph text lines are wrapped; a paragraph's LAST line before the next paragraph number could be short and not end with punctuation? E.g., "...as follows" then "24." — would be misclassified. But plan says the rule works on this data (23 unlabelled headings found correctly). The check panel lists unlabelled headings so reader can spot mistakes. OK.

Now — important: the unlabelled heading check uses lookahead to next non-empty line being a para start. But what about the LAST body line of the document? No next → not heading → paragraph text. Fine.

Also: what about lines in 'cover' state that are followed by para start but DON'T meet criteria → cover. E.g., "sustainable development*" followed by "I." — "I." is a label, not para start. So "sustainable development*" → cover. Good.

Now finishPara: 
```js
function finishPara(p) {
  const text_raw = p.lines.map(l=>l.text).join(' ').replace(/  +/g,' ').trim();
  // hmm: "joined with a single space, double spaces collapsed, trimmed"
  const pages = p.lines.map(l=>l.page);
  const page_start = pages[0], page_end = pages[pages.length-1];
  if (pages.length>1 && page_end!==page_start) → repair 'paragraph joined across a page break'
  ...
}
```

Wait — "paragraph joined across a page break (logged when a paragraph's lines carry two page numbers)". So if a paragraph's lines span multiple pages → log repair. Page cell shows "3–4". page_start = first line's page, page_end = last line's page. If spans 3 pages? "3–5". I'll show start–end if different.

Hmm, careful: lines within a page — the paragraph might have lines on pages 3 and 4 → joined. Log repair with before = last line of page 3 + ' / ' + first line of page 4? Before/After columns: before = "…[end of p.3] ‖ [start of p.4]…", after = joined. I'll do before: `page ${a} ends "…${lastLine.slice(-30)}" ‖ page ${b} begins "${firstLine.slice(0,30)}…"`, after: 'joined into one paragraph'. Keep it simple.

Hyphen check: count lines ending with '-' across all body lines; report number (expected 0).

Footnote marks: applied per paragraph in document order with global counter:

```js
let markCounter = 1;
const marksFound = []; // numbers
const rejected = []; // {number, context, para}
paragraphs.forEach(p => {
  const raw = p.text_raw;
  let marked = '';
  let last = 0;
  const re = /\d+/g; let m;
  while ((m = re.exec(raw))) {
    const run = m[0];
    const before = m.index > 0 ? raw[m.index-1] : '';
    const after = m.index + run.length < raw.length ? raw[m.index+run.length] : '';
    const excluded = ch => /[\d\/\-(\d]/.test(ch); // digit, slash, dash, open paren
    let candidate = run.length <= 3 && !excluded(before) && !excluded(after);
    if (candidate && parseInt(run,10) === markCounter) {
      marksFound.push(markCounter);
      marked += raw.slice(last, m.index) + '[' + run + ']';
      last = m.index + run.length;
      markCounter++;
    } else if (candidate) {
      rejected.push({number: run, context: raw.slice(Math.max(0,m.index-25), m.index+run.length+25), para: p.number});
    }
  }
  marked += raw.slice(last);
  p.text = marked;
});
```

Wait — excluded chars: "not touching another digit, a slash, a dash or an opening parenthesis". So before/after must not be digit, '/', '-', '('. My regex char class: /[\d\/\-(\d]/ — the \d twice is redundant; /[\d\/\-(\d]/ = digits, slash, hyphen, open paren. OK: `const excluded = ch => ch !== '' && /[\d\/\-(\d]/.test(ch);` — hmm if before is '' (start of text), not touching → allowed. Let me write: `const bad = ch => ch && /[\d\/\-(\d]/.test(ch);` candidate = run.length<=3 && !bad(before) && !bad(after).

Hmm wait — should the mark also not be preceded by a letter? "waste.2" — preceded by '.', fine. What about "art.2"? preceded by '.', fine, candidate. OK per spec.

But hold on — there's a subtlety with the sequential rule and rejected numbers: "the check lists ... the numbers it rejected as not being marks (with context), so the reader can see that 'article 11' was not bracketed". So rejected = candidates that didn't equal the counter. But note: a candidate equal to counter is consumed as mark; a candidate NOT equal is rejected (left alone). But what if a real number equals the counter at that point? Then it'd be wrongly marked — the spec accepts this risk ("only a sequential rule tells them apart"). The check "marks run 1..footnotes without gap" would catch anomalies.

Hmm, wait — actually there's a subtle issue: what if a mark number appears but counter has advanced past it (out of order)? Then it's rejected and the mark is missing → check lists missing numbers. OK.

Also — the marks should be found in paragraph text; but footnote marks could also appear in headings? Plan says "Footnote marks in the text" walking paragraphs. Headings probably don't have marks. OK.

first_words_found: from p.text (marked), remove /\[\d+\]/g, split /\s+/, take 6, join ' '. Normalise both sides: replace curly quotes [‘’“”] → straight, en dash – and em dash — → '-', collapse whitespace. Compare.

Wait — normalisation: "curly quotes to straight, en and em dashes to a hyphen and runs of whitespace to one space; case is kept". So normalise(s) = s.replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim(). Compare normalise(found) === normalise(ref).

Hmm — but first_words_found should probably be stored normalised or raw? Store the found six words (from marked text, marks removed) — I'll store the raw found string (un-normalised) for display, and match on normalised. CSV column first_words_found — store as found (maybe normalised? I'll store the found words as extracted, marks removed, joined with single space). Fine.

footnotes_cited: the marks in this paragraph: list of numbers, e.g., "2; 3" or "2, 3". I'll join with ', '.

repairs per paragraph: filter repairs where target starts with 'para. n'. I'll tag repairs with para number when applicable.

Now checks list (each: {name, detail, pass, failInfo, links}):

1. Paragraph count: found vs ref.paragraphs. pass if equal (or if no ref → 'not run').
2. Numbering: numbers are exactly 1..n in order. List gaps/dupes: "para. numbers found: 1..90; gaps: none; duplicates: none".
3. First words: mismatches count; list each "para. n: found '…' / reference '…'".
4. Footnotes: found (excluding '*') vs ref.footnotes; numbering 1..count no gaps/dupes; restored listed with page.
5. Footnote marks: marksFound should be 1..ref.footnotes; list missing; list rejected with context (maybe cap list at, say, 20 with "and n more").
6. Footnotes stay out of paragraphs: for each footnote, take opener line (first 40 chars incl number) — search in each paragraph's text_raw. Count hits. Also paragraphs >300 words listed. pass if 0 hits.
   - Note: "for a footnote whose number was displaced, its first line" — the opener for restored footnote D is its first text line (no number). I stored opener as tt.slice(0,40) for numbered ones; for restored, the first line of its text. I'll store `searchLine` = first 40 chars of the footnote's first content line (including number if present).
   - Hmm: "The first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…'; for a footnote whose number was displaced, its first line)". So for normal footnotes, the opener line includes the number: "15 Human Rights Committee, general comm…". For displaced, the first line of its text (no number). Search these in raw paragraph texts. Expected 0.
7. Headers and footers: pages whose first line was symbol (count/total); pages with page number in footer (expected all but first); displaced numbers listed with page.
8. Headings: counts labelled (roman/letter) and unlabelled; list unlabelled ones (cap display).
9. Nothing lost: sum of classCounts (non-empty lines) === total non-empty lines in file; unclassified listed.

Also hyphen count reported somewhere — "the app counts such lines anyway and reports the number" — I'll add it to the method/checks area (maybe as part of check 9 or a note on tab 04 method). I'll put it in the method text on tab 04: "lines ending in a hyphen: n (no hyphen joining done)".

Check pass counting: checks with ref missing → 'not run' (not counted in m? "the checks that need it show 'not run', never 'pass'"). So m = number of checks run (those with reference available)? I'll count m = checks that ran (pass or fail); not-run excluded from m. Header shows "n of m checks pass" or "n checks failed". If any fail → red dot + "n checks failed" + red dot on tab 04.

Now the "n of m checks pass" in header and rail card.

Now rendering. Let me plan the HTML structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>...</title>
<style>...</style>
</head>
<body>
<header>
  <div class="kicker">UN DOCUMENT · PDF TEXT</div>
  <h1 id="docTitle"></h1>
  <p class="meta" id="docMeta"></p>
  <p class="what">This page splits the converter's raw text into numbered paragraphs, removes headers, footers and footnotes, checks itself against the document's reference, and lists every repair it made.</p>
  <div class="checkpill" id="checkPill"></div>
</header>
<div class="layout">
  <aside class="rail">
    <h2 class="railhead">DOCUMENT</h2>
    <div id="docCards"></div>
  </aside>
  <main>
    <div class="tabs" role="tablist" aria-label="Sections">
      <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true">01 RESULT</button>
      ... 02 PARAGRAPHS, 03 FOOTNOTES, 04 CHECKS & METHOD
    </div>
    <section role="tabpanel" id="panel-0" aria-labelledby="tab-0">...</section>
    ...
  </main>
</div>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

Tab labels: `01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD` — the plan writes them with "·" separators in one string but they're separate tabs. I'll render four buttons: "01 RESULT", "02 PARAGRAPHS", "03 FOOTNOTES", "04 CHECKS & METHOD". Hmm, the plan: "numbered tabs (role="tablist", arrow keys): `01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD`". The "·" is just listing. Four tabs.

Arrow-key navigation: left/right (and up/down) move between tabs, Home/End. Standard roving tabindex.

Panels: hidden attribute for inactive; `[hidden]{display:none!important}` in CSS.

Tab 01 RESULT: four tiles in a grid:
- Tile 1: big number = paragraphs found; side text "The document has: 90" (reference.paragraphs); green when equal, red with difference ("+2" / "−3"). How-this-is-computed note: "Counted by this page's code: lines matching a paragraph number, joined across pages."
- Tile 2: footnotes found "n of 141". Note.
- Tile 3: first words match "n of 90". Note.
- Tile 4: repairs made n, link "see the repair log" → opens tab 04 and expands repair log. Note.

If reference missing: tiles say "no reference in this file".

Tab 02 PARAGRAPHS:
- Collapsible "Headings found: n" box (button aria-expanded) listing headings (label + title). Closed by default? "A collapsible 'Headings found: n' box above the table lists them" — I'll make it a button that toggles a list. Default closed.
- Table with caption "90 paragraphs found, 90 expected" + "TAB.01" monospace. Columns: No. | Section | Page | First line | Check.
- Rows: `<tr>` with a button in first cell? "Rows are buttons with aria-expanded; clicking or pressing Enter expands the row in place, under it." Implementation: each row is a `<tr class="prow">` containing a `<button>` that spans... Simplest accessible approach: make the whole row clickable via a button in the No. cell that has aria-expanded and aria-controls pointing to the detail row id. But "Rows are buttons" — I'll make the first cell contain a button covering the row? Alternative: use `<tr tabindex="0" role="button" aria-expanded>` — but role=button on tr breaks table semantics. Common pattern: a button inside the row (e.g., in the first cell, styled to fill) with aria-expanded; clicking toggles a following `<tr class="detail">` with the expanded content. I'll put a button in the No. cell labeled with the number, full-width, plus make the whole row clickable via JS (click on tr triggers button) — but keyboard users use the button. To keep it simple and accessible: each row's first cell has `<button class="rowbtn" aria-expanded="false" aria-controls="detail-N">n</button>`, and clicking anywhere on the row toggles (add click handler on tr that calls toggle, but avoid double-toggle when clicking the button — check event target). Simpler: only the button toggles; style the button to look like the row's number cell, and add cursor:pointer on the row with click handler that forwards to button if target isn't the button. I'll do: tr click → if (e.target closest button) return; else btn.click(). And btn click toggles. That works.

Detail row: `<tr class="detail" id="detail-N" hidden><td colspan="5">...full text, toggle, checks, repairs, copy button...</td></tr>`.

- First line cell: first 120 chars cut at a word + "…". Compute: take text (marked, with [n]), if length > 120, cut at last space before 120, add "…".
- Check cell: "OK" (green) or "first words differ" (red) — plus if paragraph contains footnote-block hit, flag too ("contains footnotes" red). The plan: check cell reads "OK" or "first words differ". The footnote-hit flag: "the paragraph is flagged in the table" — I'll add to Check cell: "OK" / "first words differ" / "contains footnotes" / both.
- Note under table: "Footnote marks are shown in square brackets, e.g. waste.[2]. Remove them with find-and-replace using the pattern \[\d+\]."
- Expanded content: full text (marked) as one block; "Show the PDF's lines" toggle (button aria-expanded) revealing text_lines with page markers: lines joined by newline, with "— page p —" marker where page changes. I'll render each line as a div, and when page changes insert a marker line "── page p ──". Under: reference first words vs found (marked equal/different); pages; repairs touching this paragraph (list); Copy citation button.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" for 2s. Clipboard may fail in sandbox — fallback: create temp textarea, execCommand('copy'). I'll try clipboard API, catch → fallback. Show "Copied" or "Copy failed".

Tab 03 FOOTNOTES:
- Heading "Footnotes found: n of 141" (caption). Table: No. | Page | Text | Repair. Rows expandable? "The expanded paragraph also lists the footnotes it cites" — that's tab 02. Footnote rows: maybe also expandable to show full text? Text column can show full text (footnotes are short). I'll show full text in the cell (maybe truncated with expand? keep simple: full text, it's one-two lines). Repair column: "number restored from the page foot" for repaired ones, else "—".
- Also list footnote "*" (asterisk note) separately? It's kept as footnote "*" not counted. I'll show it in the table with No. "*" and a note, or below the table as a note. I'll include it as a row with No. "*" and note "(cover note, not counted)". Hmm — "Footnotes found: n of reference.footnotes" counts numbered only. I'll add the asterisk row at the end with a muted style and a note. Or simpler: mention under the table. I'll include as row with number "*".
- Download button "footnotes.csv" — columns: number, page, text, repair, symbol, doc_url. I'll define: number,page,text,repaired,repair_note,symbol,doc_url. Keep simple: number, page, text, repair, symbol, doc_url.

Tab 04 CHECKS & METHOD:
- Check panel open: each check one line: name, what was compared, values, "pass" green / "check failed" red with link to rows (link → go to tab 02 and expand the row? "a link to the rows concerned" — I'll make links that switch to tab 02 and expand relevant rows, or for footnote checks → tab 03). Implement: `<a href="#" data-goto="para" data-n="12">para. 12</a>` — on click, switch to tab 02, expand row 12, scroll to it. For simplicity, links like "para. 12" in check details.
- Repair log: closed heading button "Repair log (n)" aria-expanded; when opened (also via tile link on tab 01), shows count per kind + table Page | Paragraph or footnote | What was done | Before | After.
- Raw pages: closed heading button "Raw pages"; inside: select "Show raw page n" (options 1..20) + monospaced panel with line numbers, each line coloured by class + letter code in margin; legend with six tints.
- Download: "Download paragraphs as CSV" button.
- Method text: brief description of pipeline + hyphen count + "How this is computed" lines.

Footer: source line (`data.source`), built date if present, honesty line: "Counting, splitting and matching are done by this page's code; no model was called and nothing left the browser."

Now — the header meta line: "`symbol` linked to `doc_url` (new tab), 'adopted `reference.adopted`', 'n pages of raw converter text', `source`". So: `<a href=doc_url target=_blank>symbol</a> · adopted 6 November 2025? · 20 pages of raw converter text · source`. reference.adopted — value like "6 November 2025"? The reference has `adopted`. I'll display "adopted " + reference.adopted.

Rail card: symbol monospace, short title — pdf_text has `title` (long). "its short title" — I'll use title but maybe truncated via CSS (line-clamp). I'll show title with CSS clamp 3 lines. "adopted …", "n pages". Two big serif numbers: paragraphs found with "of 90" and thin bar (share = found/ref, red when short or over — i.e., if found !== ref → red bar; else neutral/green? "a thin bar showing the share found (red when short or over)" — bar fill = min(found/ref,1)*100%, red if found≠ref else default ink? I'll make bar fill red when found<ref or found>ref, else a calm ink/green. Hmm "red when short or over" — so when equal, not red. I'll use green? The design says one accent red; pass is dark green. I'll make the bar fill dark green when equal, red otherwise. Actually simpler: fill color red if found!==ref else #2e6b4f (dark green). OK.

Then "n of m checks pass" link → tab 04.

Now, multiple documents: rail cards for each; clicking a card re-renders tabs for that document. I'll structure: parse all docs upfront into `docs` array; `state.selected = 0`; render function renders header/rail/tabs for selected doc. Since header shows selected doc's title etc.

Wait — header shows the document title — with multiple docs, header changes with selection. Fine.

Now, sizes: 90 paragraphs, 141 footnotes, ~160 repairs, 20 raw pages. Rendering all rows is fine.

CSV generation:

```js
function toCSV(rows, cols) {
  const esc = v => '"' + String(v==null?'':v).replace(/"/g,'""') + '"';
  const lines = [cols.map(c=>esc(c.label)).join(',')];
  rows.forEach(r => lines.push(cols.map(c=>esc(r[c.key])).join(',')));
  return '\uFEFF' + lines.join('\r\n') + '\r\n';
}
```

Blob: `new Blob([csv], {type:'text/csv;charset=utf-8'})`, URL.createObjectURL, a.download = symbol.replace(/\//g,'-') + '-paragraphs.csv'. Click.

Paragraph CSV columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, text_lines, footnotes_cited, repairs, citation, symbol, doc_url.

- first_words_match: "yes"/"no" (or true/false). I'll use "yes"/"no".
- repairs: join repair kinds with '; '.
- text_lines: lines joined with ' | '.

Footnotes CSV: number, page, text, repair, symbol, doc_url. Filename: symbol-hyphens + '-footnotes.csv'.

Now the raw page viewer classification: I need per-line classification for every line of every page, including header/footer/footnote lines. I built `cls` arrays during parsing. For body lines, cls assigned during body parse ('cover'/'heading'/'paragraph'). Blank lines: cls = null (shown uncoloured). Unclassified non-empty lines: the "nothing lost" check — with my state machine every non-empty body line gets a class, header/footer/footnote too. So unclassified should be 0. But I'll still compute and list any.

Wait — one problem: lines between header and footer that are in the footnote block get 'footnote'. Body lines get classes in body parse. But what about lines after blockStart... all block lines are 'footnote'. And lines before blockStart are body. Good. But blank lines within the footnote block: cls stays null — they're empty, not counted. In the raw viewer they show uncoloured. Fine.

Hmm — but wait: the footer removal loop starts from the end and drops while matching footer patterns. What if a footnote text line at the end matches "bare number"? E.g., last footnote line is "131" alone? The displaced numbers ARE bare numbers in the footer region — that's exactly how we detect them. But could a footnote's text line be a bare number and get eaten as footer? The plan says the displaced numbers sit in the footer (after the footnote block). The loop drops from the end: page number, GE code, date stamp, displaced number — all footer. Then stops at the last footnote text line. OK per plan.

But careful: the loop condition "drop lines while the line is empty, starts with 'GE.', consists only of 6-digit groups, or is a bare number of one to three digits" — it drops ALL trailing bare numbers, e.g., if footer is "GE.25-15926" / "12" / "6" — wait page 2's footer: page number "2" and displaced "6"? Order varies. The loop collects all trailing bare numbers; those equal to page → page number; others → displaced. But what if there are multiple non-page bare numbers? Plan says on 12 pages a third bare number sits in the footer (one displaced). So at most one displaced per page. If multiple, I'll treat all non-page ones as displaced (restore each? The rule mentions "a displaced number D" singular). I'll handle array: restore each in order? The footnote-block rule handles "a page with a displaced number D" — I'll generalise: if displaced.length > 0, apply the split rule for the first footnote, creating footnotes for each displaced number in order as continuation lines arrive. Simpler: handle first displaced D1; if more, subsequent continuation lines after D1's lines... complicated. Given data has exactly one per page, I'll implement for the general case loosely: after the first footnote's terminating line, each subsequent "run" of continuation lines before the next numbered opener becomes the next displaced footnote. Actually simplest: when in displaced mode and current footnote is a restored one and we hit... hmm. Let me implement: on a displaced page, after the first footnote closes (at first '.'-ending line), all continuation lines until the next numbered opener are collected; if displaced.length === 1, they all form footnote D. If more, split them... I'll just assign all to the first displaced number and log extra displaced numbers as warnings. Given the data, one each. Fine.

Now — the block-start detection issue: on a displaced page, the block starts at bare number == nextFootnote (the first footnote). Good. But what if nextFootnote's number was itself displaced (i.e., the page's first footnote is the displaced one)? Plan says displaced is always the second. OK.

Another subtlety: "or starts with that number and a space" — e.g., nextFootnote=15, line "15 Human Rights Committee, general comment..." → opener. But also a body line could start with "15 " — e.g., wrapped text starting with a number? The plan's rule accepts the risk. But wait — there's a real risk: body text lines like "2025 was a year..." — starts with "2025 " — 4 digits, and nextFootnote would need to be 2025 — no, nextFootnote ≤ 141. A body line starting with e.g. "6 November 2025" — nextFootnote=6 at some point? If a page's body has a line starting "6 ..." and nextFootnote==6 and the footnote block hasn't started yet on that page... then block would wrongly start there. The plan says the rule works on this data (the "6 November 2025" note is about page 1 where counter is 1). Trust the plan.

Hmm, wait — actually one more: the block-start scan takes the FIRST line matching opener patterns. On page 1, could a cover line match before the real footnote block? Cover lines: "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", ... "6 November 2025" starts with "6 " — nextFootnote=1 → no. OK. And "* " on first page — the asterisk line. If the asterisk line comes before footnote "1" on page 1, block starts at "*". Then within block, "1" opener etc. Fine either way.

But hmm — what if on page 1 the asterisk note is at the very foot AFTER numbered footnotes? Then block starts at "1" (bare) and the "* " line inside the block — my within-block parser treats "* " as opener for footnote "*". Good, I'll add that.

Now, within-block parsing details: "a line that starts with a number and a space, or a bare number on its own line, opens a footnote; the lines up to the next opener are its text, joined with a space. Any line that starts with a number and a space opens a footnote, even when the number is not the one expected: never add a numbered line to the footnote before it."

So opener regex: /^(\d{1,3}) / or /^(\d{1,3})$/. Note "starts with a number and a space" — number 1-3 digits followed by space. What about "15." at start? Not an opener (period). OK.

Footnote text: lines joined with a space — trim each line? "joined with a space" — I'll trim each line and join with ' '. Blank lines skipped.

The first footnote on a page: "a bare number on its own line, a blank line, then the text" — bare number opens footnote, blank skipped, text lines joined. Good.

Displaced rule: first footnote of the page (the one opened by the bare number == nextFootnote... or just the first footnote object on the page) ends at its first line ending with '.'. Implementation as described.

Hmm wait — actually re-read: "On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D, marked repaired."

So: first footnote = the one with the bare number. Its text ends at first line ending with '.'. Lines after → footnote D. My implementation: when cur is the first footnote of the page AND page has displaced AND cur already has a line ending with '.' AND a new continuation line arrives → close cur, open footnote D (repaired), add line to D. Subsequent continuation lines go to D (cur is now D, not first). Next numbered opener closes D. 

But careful: what if the first footnote's text has multiple lines and the first line ends with '.' but more lines follow that belong to it? Plan says in all 12 cases it's one line. OK.

Also: what if displaced page's first footnote is opened by "N text" (number+space) instead of bare? Plan says bare. My rule: apply split logic to the first footnote object on the page regardless of opener form. Fine.

Now nextFootnote advancement: after processing page's block: numbers seen = all footnote numbers on the page (numeric). nextFootnote = max(nextFootnote, ...numbers, ...displaced) + 1.

Hmm — wait, what if a page's block contains numbers but the page had NO block (blockStart -1)? Then no advancement. And the jump rule handles missing opener.

Edge: what if blockStart found via jump (bare number > nextFootnote)? Log jump repair: kind — I'll use "footnote number restored"? No... I'll log kind "footnote block removed" already covers the block; the jump I'll log as a separate repair kind "footnote count jumped" with before/after. Since it likely doesn't occur, fine. Actually — hmm, let me reconsider: maybe log the jump as a warning in checks (check 4 detail: "number X not seen on any page; count jumped on page p"). I'll do both: repair entry kind "footnote count jumped" (only if occurs) and check detail. OK.

Now — the "Footnote block" detection when nextFootnote opener exists but ALSO earlier body lines start with numbers... covered.

One more: pages where the footnote block opener is "starts with nextFootnote + space" — e.g., page starts mid-footnote? No, blocks are at foot.

Now, body lines include the cover. Cover lines: "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on economic, social and", "cultural rights and the environmental dimension of", "sustainable development*". Then "I." heading. So cover = 9 lines. classCounts.cover = 9.

Wait — "Distr.: General" — hmm, in the sample it's "Distr.: General\n6 November 2025\nOriginal: English". OK.

Now — the "Nothing lost" check: total non-empty lines across all pages = sum of classCounts + unclassified. My classification covers every non-empty line: header (first line if symbol), footer (trailing), footnote (block), body (cover/heading/paragraph). Every non-empty line in i..j range is either body or block. Body lines all get cover/heading/paragraph. So sum should equal total. I'll compute total non-empty lines independently and compare.

Now let me also handle: what if first non-empty line is NOT the symbol → warning; then that line stays in body (cls assigned in body parse). Fine.

Now — rendering performance: 90 paragraph rows + details, 141 footnote rows, repairs table ~160 rows, raw pages 20 × ~40 lines. Fine.

Let me now think about the "How this is computed" notes:
- Tile 1: "Counted by this page's code: every body line that starts a numbered paragraph, joined across page breaks. Compared with the document's own reference."
- Tile 2: "Counted by this page's code: footnote openers in each page's footnote block, plus numbers restored from page feet."
- Tile 3: "First six words of each extracted paragraph (footnote marks removed) compared with reference.first_words after normalising quotes, dashes and spaces."
- Tile 4: "Every change the script logged while parsing, listed on tab 04."

Tab captions: "TAB.01" etc. — "Every table has a serif <caption> that states the message ('90 paragraphs found, 90 expected') and a monospace number (TAB.01)". So caption contains message + monospace "TAB.01". I'll put `<caption><span class="tabno">TAB.01</span> 90 paragraphs found, 90 expected</caption>`.

Figure numbers FIG.01 for tiles? "monospace ... for labels, tab names and figure numbers (FIG.01)". Tiles could have FIG.01–FIG.04. I'll add small monospace "FIG.01" labels on tiles. Nice.

Now design CSS:

```css
:root{
  --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#2e6b4f;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
header{padding:28px 32px 18px;border-bottom:1px solid var(--rule)}
...
```

Layout: `.layout{display:flex;gap:0}` rail width 260px, border-right rule; main flex 1, padding.

Tabs: `.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);position:sticky? no}` tab buttons: mono, padding, border-bottom 2px transparent; active: color red + border-bottom red. Focus ring: `:focus-visible{outline:2px solid var(--red);outline-offset:2px}`.

Tiles: grid 4 columns (2 on narrow). `.tile{border-top:1px solid var(--rule);padding:14px 16px}` big number `.bignum{font-family:Georgia;font-size:48px;line-height:1}`.

Tables: `table{width:100%;border-collapse:collapse} caption{text-align:left;font-family:Georgia;font-size:18px;padding:8px 0} th{...mono small, border-bottom} td{border-bottom:1px solid var(--rule);padding:6px 8px;vertical-align:top} .num{text-align:right;font-variant-numeric:tabular-nums}`.

Paragraph number in first column: red, serif? "Red accent on ... the paragraph numbers in the first column". I'll make the No. cell red serif bold.

Raw viewer: `.rawpage{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;white-space:pre-wrap;background:#efe9dd?}` each line: `<div class="rl"><span class="ln">12</span><span class="code">P</span><span class="lt">text</span></div>` with background tint per class. Tints: cover #efe6d8? Let me pick six pale tints on paper:
- cover: #ece4d4
- header: #f3d9d3 (pale red)
- heading: #e3d9c2? hmm heading should differ. Let me choose:
  - cover C: #eae2d0
  - header H: #f0dcd6
  - heading T: #e6ddc4
  - paragraph P: #f4f0e8 (paper) — hmm paragraph should be visible; use #f7f4ec with left border? Let me give paragraph #f2eee2.
  - footnote N: #e2e6da (pale green-grey)
  - footer F: #e8e0ee? pale purple — but "other colours only where a category needs one" — the raw viewer is the exception ("Category colours only in the raw page viewer: six pale tints"). OK.
  - unclassified: red tint #f5d5d5.

Letter codes: C, H, T, P, N, F.

Legend: swatches with code + name.

Now the JS structure. Let me write it carefully.

```js
const DATA = window.WORKSHOP_DATA || {};
const docKeys = Object.keys(DATA).filter(k => {
  const d = DATA[k];
  return d && Array.isArray(d.records) && d.records.length && d.reference && typeof d.reference === 'object';
});
// preserve order of keys
```

Hmm — Object.keys order: insertion order. pdf_text, pdf_text_2. OK.

parseDocument(data) returns result object:

```js
{
  data, symbol, title, docUrl, source, built, ref, records,
  paragraphs: [{number, section, part, path, page_start, page_end, text, text_raw, text_lines, first_words_found, first_words_reference, first_words_match, footnotes_cited:[], repairs:[], citation, containsFootnotes:bool}],
  footnotes: [{number, page, text, repaired, opener}],
  headings: [{label, title, kind, page}],
  repairs: [{page, ord, target, kind, before, after}],
  checks: [{id, name, detail, status: 'pass'|'fail'|'notrun', links:[{label, tab, para}]}],
  classCounts, totalNonEmpty, unclassified: [{page, line, text}],
  hyphenLines: n,
  warnings: [],
  lineClasses: Map page -> array of cls per line index,
  rawPages: [{page, lines:[...]}]
}
```

Let me now write the parse function in full detail.

```js
function norm(s){
  return String(s==null?'':s)
    .replace(/[\u201C\u201D]/g,'"')
    .replace(/[\u2018\u2019]/g,"'")
    .replace(/[\u2013\u2014]/g,'-')
    .replace(/\s+/g,' ')
    .trim();
}

function parseDocument(data){
  const symbol = data.symbol || '';
  const ref = data.reference || null;
  const records = [...(data.records||[])].sort((a,b)=>(a.page-b.page));
  const firstPage = records.length ? records[0].page : 1;
  const repairs = [];
  const warnings = [];
  const footnotes = [];
  const bodyLines = []; // {page, idx, text}
  const lineCls = new Map(); // page -> array
  const classCounts = {cover:0, header:0, heading:0, paragraph:0, footnote:0, footer:0};
  let totalNonEmpty = 0;
  let nextFootnote = 1;
  const pageInfo = []; // {page, hadHeader, hadPageNumber, displaced:[], blockFound, blockLines}

  records.forEach(rec => {
    const page = rec.page;
    const raw = String(rec.text||'').split('\n');
    const cls = raw.map(()=>null);
    lineCls.set(page, cls);
    raw.forEach(l => { if (l.trim()!=='') totalNonEmpty++; });
    let i = 0;
    while (i < raw.length && raw[i].trim()==='') i++;
    let hadHeader = false;
    if (i < raw.length && raw[i].trim() === symbol) {
      cls[i] = 'header'; classCounts.header++; hadHeader = true;
      repairs.push({page, ord:i, target:'page header', kind:'header line removed', before: raw[i], after:'(removed from the body)'});
      i++;
    } else if (i < raw.length) {
      warnings.push('page '+page+': the first non-empty line is not the symbol "'+symbol+'"');
    }
    // footer
    let j = raw.length - 1;
    const displaced = [];
    let hadPageNumber = false;
    const footerLines = [];
    while (j >= i) {
      const t = raw[j].trim();
      if (t === '') { j--; continue; }
      if (/^GE\./.test(t) || /^(\d{6} )*\d{6}$/.test(t) || /^\d{1,3}$/.test(t)) {
        cls[j] = 'footer'; classCounts.footer++;
        footerLines.push({idx:j, text: raw[j]});
        if (/^\d{1,3}$/.test(t)) {
          const n = parseInt(t,10);
          if (n === page) hadPageNumber = true; else displaced.push(n);
        }
        j--; continue;
      }
      break;
    }
    footerLines.forEach(f => repairs.push({page, ord:f.idx, target:'page footer', kind:'footer line removed', before: f.text, after:'(removed from the body)'}));
    // footnote block
    const lines = [];
    for (let k=i;k<=j;k++) lines.push({idx:k, text: raw[k]});
    let blockStart = -1;
    for (const L of lines) {
      const t = L.text.trim();
      if (t==='') continue;
      if (/^\d{1,3}$/.test(t) && parseInt(t,10)===nextFootnote) { blockStart = L.idx; break; }
      if (t.startsWith(nextFootnote+' ')) { blockStart = L.idx; break; }
      if (page===firstPage && t.startsWith('* ')) { blockStart = L.idx; break; }
    }
    let jumped = false;
    if (blockStart === -1) {
      for (const L of lines) {
        const t = L.text.trim();
        if (/^\d{1,3}$/.test(t) && parseInt(t,10) > nextFootnote) {
          blockStart = L.idx; jumped = true;
          repairs.push({page, ord:L.idx, target:'footnote block', kind:'footnote count jumped', before:'expected footnote '+nextFootnote, after:'block starts at footnote '+t+' on page '+page});
          warnings.push('page '+page+': no line opens footnote '+nextFootnote+'; the block starts at '+t);
          break;
        }
      }
    }
    if (blockStart === -1) {
      warnings.push('page '+page+': no footnote block found; every line is body');
      pageInfo.push({page, hadHeader, hadPageNumber, displaced, blockFound:false});
    } else {
      const block = lines.filter(L => L.idx >= blockStart);
      block.forEach(L => { cls[L.idx]='footnote'; classCounts.footnote++; });
      repairs.push({page, ord:blockStart, target:'footnote block', kind:'footnote block removed', before: block.length+' lines at the foot of page '+page, after:'moved out of the body text into footnotes'});
      // parse footnotes in block
      let cur = null;
      let firstFn = null;
      const pushCur = () => { if (cur) { cur.text = cur.lines.join(' ').replace(/  +/g,' ').trim(); footnotes.push(cur); } };
      const seen = [];
      for (const L of block) {
        const tt = L.text.trim();
        if (tt==='') continue;
        const bare = /^(\d{1,3})$/.exec(tt);
        const numSpace = /^(\d{1,3}) (.+)$/.exec(tt);
        if (bare || numSpace) {
          pushCur();
          const num = bare ? bare[1] : numSpace[1];
          cur = {number: num, page, lines: numSpace ? [numSpace[2]] : [], opener: tt.slice(0,40), repaired:false, search: tt.slice(0,40)};
          if (!firstFn) firstFn = cur;
          seen.push(parseInt(num,10));
          continue;
        }
        if (page===firstPage && tt.startsWith('* ')) {
          pushCur();
          cur = {number:'*', page, lines:[tt], opener: tt.slice(0,40), repaired:false, asterisk:true, search: tt.slice(0,40)};
          continue;
        }
        // continuation
        if (cur) {
          if (displaced.length && cur === firstFn && cur.lines.some(l=>l.trim().endsWith('.'))) {
            // this line belongs to the displaced footnote
            pushCur();
            const D = displaced[0];
            cur = {number: String(D), page, lines:[tt], opener: tt.slice(0,40), repaired:true, search: tt.slice(0,40)};
            seen.push(D);
            repairs.push({page, ord:L.idx, target:'footnote '+D, kind:'footnote number restored', before:'"'+tt.slice(0,60)+'" — no number; '+D+' sat alone in the page foot', after:'footnote '+D+' '+tt.slice(0,60)});
            continue;
          }
          cur.lines.push(tt);
        }
      }
      pushCur();
      const maxSeen = seen.length ? Math.max(...seen) : 0;
      const maxDisp = displaced.length ? Math.max(...displaced) : 0;
      nextFootnote = Math.max(nextFootnote, maxSeen, maxDisp) + 1;
      pageInfo.push({page, hadHeader, hadPageNumber, displaced, blockFound:true});
    }
    // body lines
    for (const L of lines) {
      if (L.idx < blockStart || blockStart===-1) {
        if (L.text.trim()!=='') bodyLines.push({page, idx:L.idx, text:L.text});
      }
    }
  });
```

Hmm wait — bug: when blockStart === -1, all lines are body: condition `L.idx < blockStart || blockStart===-1` — if blockStart===-1, `L.idx < -1` false, so need the `|| blockStart===-1`. I wrote that. OK. But cleaner: `if (blockStart===-1 || L.idx < blockStart)`.

Also — the displaced restore: `cur === firstFn && cur.lines.some(ends with '.')` — but this check happens when a continuation line arrives. The first footnote's lines: first line "A/79/270, paras. 84 and 85." ends with '.' → after adding it, cur.lines has a '.'-ending line. Next continuation "A/42/427, p. 24." → condition true → becomes footnote D. 

But wait — what if the first footnote's text is added via numSpace opener ("5 A/79/270...")? Then cur.lines = ["A/79/270..."] — ends with '.' → next continuation goes to D. OK.

Edge: what if displaced.length && the first continuation line arrives BEFORE any '.'-ending line in firstFn? Then it's added to firstFn normally. Per plan, first footnote is one line ending with '.', so fine.

Now body parsing:

```js
  const paragraphs = [];
  const headings = [];
  let cur = null;
  let heading = null;
  const isParaStart = t => /^(\d{1,3})\.$/.test(t) || /^(\d{1,3})\. .+$/.test(t);
  const paraNum = t => { const m = /^(\d{1,3})\./.exec(t); return m ? m[1] : null; };
  const isLabel = t => /^([IVX]+|[A-Z])\.$/.test(t);
  const isUnlabelled = (t, nextT) => {
    if (!isParaStart(nextT)) return false;
    if (t.length > 90) return false;
    if (!/^\p{Lu}/u.test(t)) return false;
    if (/[.;:,\d]$/.test(t)) return false;
    return true;
  };
  // next non-empty body line text
  const nb = bodyLines.map((L,i)=>{ // index of next non-empty
    ...
  });
```

Simpler: precompute array of indices of non-empty body lines; iterate with pointer. Let me build `ne = bodyLines.filter(L=>L.text.trim()!=='')` — but I need original idx for repairs ord. bodyLines already only includes non-empty? In my collection loop I only pushed non-empty lines (`if (L.text.trim()!=='')`). Wait no — I wrote `if (L.text.trim()!=='') bodyLines.push(...)` — yes only non-empty. But blank lines within body are dropped (per plan: "blank lines are dropped"). Good — so bodyLines = non-empty body lines only. Then next non-empty = next element in bodyLines.

```js
  const closeHeading = () => {
    if (heading) {
      heading.title = heading.lines.join(' | '); // hmm
      headings.push(heading); heading = null;
    }
  };
```

Wait — heading lines: multiple title lines; joined continuations. Let me store heading.lines as array of title lines (after joining continuations). heading.title = lines.join(' ') maybe; but for section we need "the most recent heading line". Hmm — if a labelled heading has multiple title lines (e.g., "Right to work" and "(art. 6)" joined into one), lines = ["Right to work (art. 6)"]. If two separate capital lines, lines = ["A", "B"] — most recent = "B". For section I'll use the LAST line. For display in headings box, show label + all lines joined.

Hmm, wait — actually for roman headings like "IV." + "Environmental dimension of sustainable development" — one line. For lettered "A." + "Right to work" + "(art. 6)" → joined → one line "Right to work (art. 6)". Good.

But hold on — the join rule: "a line starting with a lowercase letter or '(' continues the previous heading line". What about a title wrapping to a second line starting with a capital? E.g., "General comment No. 27 (2025) on economic, social and" / "cultural rights..." — second line starts lowercase 'c' → joins. Good. But some titles wrap with capital? Then it'd be "a further heading" — separate line. For section, most recent line. OK.

```js
  const closePara = () => {
    if (!cur) return;
    const p = cur; cur = null;
    const raw = p.lines.map(l=>l.text.trim()).join(' ').replace(/  +/g,' ').trim();
    const pages = p.lines.map(l=>l.page);
    const pstart = pages[0], pend = pages[pages.length-1];
    if (pages.some(pg=>pg!==pstart)) {
      repairs.push({page:pstart, ord:p.lines[p.lines.length-1].idx, target:'para. '+p.number, kind:'paragraph joined across a page break',
        before:'page '+pstart+' ends "…'+p.lines.filter(l=>l.page===pstart).slice(-1)[0].text.trim().slice(-40)+'" ‖ page '+pend+' begins "'+p.lines.filter(l=>l.page===pend)[0].text.trim().slice(0,40)+'…"',
        after:'joined into one paragraph'});
    }
    p.text_raw = raw;
    p.page_start = pstart; p.page_end = pend;
    p.text_lines = p.lines.map(l=>l.text.trim()).join(' | ');
    paragraphs.push(p);
  };
```

Hmm — ord for the join repair: use the idx of the first line on the later page. Fine, approximate.

Wait — also the "number and text split" repair: pushed when paraText form encountered.

Main loop:

```js
  let state = 'cover';
  for (let i=0;i<bodyLines.length;i++){
    const L = bodyLines[i];
    const t = L.text.trim();
    const nextT = i+1<bodyLines.length ? bodyLines[i+1].text.trim() : '';
    if (isParaStart(t)) {
      closeHeading(); closePara();
      const m = /^(\d{1,3})\./.exec(t);
      const num = m[1];
      cur = {number:num, lines:[], startIdx:L.idx, page:L.page};
      const inline = /^(\d{1,3})\. (.+)$/.exec(t);
      if (inline) {
        cur.lines.push({page:L.page, idx:L.idx, text: inline[2]});
        repairs.push({page:L.page, ord:L.idx, target:'para. '+num, kind:'number and text split', before:t, after:num+'. ‖ '+inline[2]});
      }
      L.cls='paragraph'; state='body';
      continue;
    }
    if (isLabel(t)) {
      closeHeading(); closePara();
      const m = /^([IVX]+|[A-Z])\.$/.exec(t);
      heading = {label:m[1], lines:[], page:L.page, kind:/^[IVX]+$/.test(m[1])?'roman':'letter', lineIdx:L.idx};
      L.cls='heading';
      continue;
    }
    if (heading) {
      // heading text line
      if ((/^[a-z(]/u.test(t)) && heading.lines.length) {
        const prev = heading.lines[heading.lines.length-1];
        heading.lines[heading.lines.length-1] = prev + ' ' + t;
        repairs.push({page:L.page, ord:L.idx, target:'heading "'+heading.label+'"', kind:'heading title joined from two lines', before: prev+' ‖ '+t, after: prev+' '+t});
      } else {
        heading.lines.push(t);
      }
      L.cls='heading';
      continue;
    }
    if (isUnlabelled(t, nextT)) {
      closePara();
      headings.push({label:null, title:t, lines:[t], page:L.page, kind:'unlabelled', lineIdx:L.idx});
      const nn = paraNum(nextT);
      repairs.push({page:L.page, ord:L.idx, target:'before para. '+nn, kind:'heading separated from paragraph text', before:'"'+t+'" sat directly above para. '+nn, after:'kept as a heading: "'+t+'"'});
      L.cls='heading';
      state='body';
      continue;
    }
    if (state==='cover') { L.cls='cover'; continue; }
    // paragraph text
    L.cls='paragraph';
    if (cur) cur.lines.push({page:L.page, idx:L.idx, text:t});
    else { L.cls='cover'; } // safety
  }
  closeHeading(); closePara();
```

Hmm — wait, there's an issue with heading mode and unlabelled headings: after a labelled heading's title lines, the next line is a para start — handled at top. But what if after heading title lines comes another non-para, non-label line? It stays heading text (per rule "every line up to the next label line or paragraph start is heading text"). OK.

But there's a subtle problem: heading mode never ends except at label/para/body-end. What if a heading is followed by cover-like lines? Not in this data.

Another subtlety: unlabelled heading in 'cover' state — e.g., is there any? Page 1: "I." label comes before "1.". So cover lines then "I." → heading mode. Fine. But what if a document had no roman heading before para 1? Then cover lines followed by "1." — the line before "1." if it meets unlabelled criteria becomes a heading. E.g., "Introduction" without "I." — would become unlabelled heading. Fine.

Wait — one more: in 'cover' state, isUnlabelled check: `state==='cover'` and next is para start and criteria → heading. But I placed the isUnlabelled check BEFORE the cover check, and it applies in both cover and body states. In cover state, if line meets criteria and next is para → heading (good). Otherwise cover. In body state (cur exists), if line meets criteria and next is para → close para, heading. Otherwise paragraph text. That's what I have. But note: in body state, `closePara()` then heading — but state stays 'body'. Good.

Hmm — but there's a bug: in body state, a paragraph text line followed by a para-start line that meets unlabelled criteria → treated as heading. But what if it's genuinely the paragraph's last line? That's the ambiguity the plan accepts (23 unlabelled headings). The check panel lists them. OK.

Now — wait, another important subtlety: the unlabelled heading rule says "a non-empty line immediately followed by a paragraph-start line". In my bodyLines, blanks are dropped, so "immediately followed" = next element. But in the raw page, there might be a blank line between heading and paragraph number? E.g., "Right to work (art. 6)\n\n12."? Hmm — in UN docs, usually no blank between heading and paragraph. But after a labelled heading there ARE blanks ("I.\n\nIntroduction"). For unlabelled, plan says "on the line just before a paragraph number". So no blank. My next-element approach handles both (blank dropped). Slight risk: a paragraph's last line, blank, then next para number — with blanks dropped, the last line appears "immediately followed" by para start. If that last line meets criteria (≤90, capital, no ending punct) it'd be misclassified. Plan accepts. OK.

Now compute per-paragraph derived data:

```js
  // section/part per paragraph
  let lastHeading = null, lastRoman = null;
  // walk body lines in order again? Better: assign during parse. Let me track during the loop: when a heading is pushed, set lastHeading/lastRoman; when a para starts, record cur.section = lastHeading ? lastHeadingTitle : '', cur.part = lastRoman ? ... : ''.
```

I'll do it inline: maintain `curHeading` (last heading object) and `curRoman` (last roman heading). When starting a paragraph: `cur.section = curHeading ? (curHeading.label ? '' : '') ...` hmm. Section = most recent heading line (title). For labelled heading, the "heading line" — I'll use the last title line of the heading, or if label with no title, the label. Let me define heading.display = label ? (label + '. ' + lines.join(' ')) : lines.join(' '). And section = lines.length ? lines[lines.length-1] : label+'.'. Part = roman heading display (label + title). Path = (part ? part + ' › ' : '') + section.

Hmm wait — for para 1 under "I. Introduction": section = "Introduction", part = "I. Introduction"? That makes path "I. Introduction › Introduction" — redundant. Hmm. Maybe for roman headings, section should be the roman heading itself when no closer heading? Let me reconsider: "Each paragraph's section is the most recent heading line before it and part the most recent roman-numbered heading". So section = most recent heading LINE. For "I." + "Introduction": heading lines = ["Introduction"] (the title). So section = "Introduction". part = "I." (roman). Path = "I. › Introduction"? The example "IV. … › Right to work (art. 6)" — so path = part + ' › ' + section where part shows "IV. …" (label + elided title?). I'll make part = roman label + '.' + (title ? ' ' + title : '') — e.g., "IV. Environmental dimension of sustainable development". Path = part + ' › ' + section. For para 1: "I. Introduction › Introduction" — redundant but harmless. Hmm, alternatively when section comes from the roman heading's own title, path could be just part. I'll special-case: if the most recent heading IS the roman heading, path = part, section = its title. Eh — simpler: path = [part, section].filter(Boolean).join(' › '); if section === part's title, it'll show twice. Let me just do: if lastHeading is the roman heading itself, path = partDisplay, section = title. I'll compute: when paragraph starts, section = lastHeading ? lastHeadingTitle : ''; part = lastRoman ? lastRomanDisplay : ''; path = (part && section && !lastHeadingIsRoman) ? part+' › '+section : (part || section). Where lastHeadingIsRoman = (lastHeading === lastRoman). OK fine.

Actually simpler and matches example: path = part ? (section && section !== partTitle ? part + ' › ' + section : part) : section. I'll implement with a flag.

CSV `part` column: part display e.g. "IV. Environmental dimension of sustainable development" or "I." if no title. `section`: e.g. "Right to work (art. 6)".

Now footnote marks (sequential) — as designed above. Also collect `footnotes_cited` per paragraph = marks found in that paragraph.

Then first words:

```js
  paragraphs.forEach(p => {
    const noMarks = p.text.replace(/\[\d+\]/g,'');
    const words = noMarks.split(/\s+/).filter(Boolean).slice(0,6).join(' ');
    p.first_words_found = words;
    p.first_words_reference = ref && ref.first_words ? (ref.first_words[String(p.number)] ?? '') : '';
    p.first_words_match = ref ? norm(words) === norm(p.first_words_reference) : null;
  });
```

Hmm — first_words_reference might be missing for a number → ''. match false. OK.

Wait — the mark replacement: p.text has marks as [n]. Removing `\[\d+\]` — but what if original text had brackets? Unlikely. OK.

Also — should first_words be computed from text_raw with marks removed instead? "the first six whitespace-separated words of the joined text, footnote marks removed first" — joined text = text_raw; remove marks (the digit runs) then take words. Removing "[2]" from "waste.[2]" gives "waste." — same as removing the digits from raw. Equivalent. OK.

Checks:

```js
  const checks = [];
  const hasRef = !!(ref && ref.paragraphs != null);
  // 1 paragraph count
  ...
```

Let me define each check with status and detail HTML (built with DOM, not innerHTML with data? I can use innerHTML with escaped text — I'll write an esc() helper and build strings carefully).

Check 1 — Paragraph count: `paragraphs.length` vs `ref.paragraphs`. pass if equal. detail: "Found 90 numbered paragraphs; the document's reference says 90." fail: difference.

Check 2 — Numbering: expected 1..n. Compute gaps/dupes: iterate paragraphs, expected counter 1..paragraphs.length; if p.number != expected → record. Also duplicates. detail lists them with page.

Check 3 — First words: mismatches list (cap 10 shown + count). Each entry link to para row.

Check 4 — Footnotes: numbered footnotes count (exclude '*') vs ref.footnotes; numbering 1..count gaps/dupes; restored listed "footnote 6 restored on page 2".

Check 5 — Footnote marks: marksFound vs ref.footnotes: missing numbers (1..ref.footnotes not in marksFound), rejected candidates list (cap). pass if marksFound covers 1..ref.footnotes exactly in order? "expected to run from 1 to reference.footnotes without a gap" — marksFound should be [1..141]. Check: marksFound.length === ref.footnotes && marksFound[i]===i+1. List missing.

Check 6 — Footnotes stay out of paragraphs: for each footnote, search footnote.search (first 40 chars of opener line) in each paragraph's text_raw. Count hits. Also paragraphs with word count > 300 listed. pass if hits===0. If hits, flag those paragraphs (p.containsFootnotes = true) and tile note.

Hmm — searching 141 footnotes × 90 paragraphs × indexOf — fine.

Wait — the search string: "The first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…')". So opener line trimmed, first 40 chars. For bare-number openers, the opener line is just the number — first 40 chars = "15" — searching "15" in paragraph text would hit any "15"! Hmm. That's a problem. Wait — re-read: "every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…'; for a footnote whose number was displaced, its first line)". The example "15 Human Rights Committee..." is a number+space opener. For bare-number openers (first footnote on a page), the opener line is just "5" — searching "5" would false-positive. Hmm. But the plan says "expected 0 hits". Maybe for bare-number openers, the "line that opens a footnote" should be the number PLUS the following text? Or maybe they mean the first line of the footnote's text including the number when present. For a bare opener, the footnote's first content line is the next non-blank line. I think the intent: the searchable string = the footnote's first line including its number if the number is on the same line; for bare-number openers, use the first text line; for displaced, its first line. To avoid the "5" false positive, I'll use: if opener is bare number, search = number + ' ' + first text line's first 40 chars? Hmm. Let me define search string = (opener line if it has text beyond the number, else number + ' ' + firstLine).slice(0,40)... Actually simpler and safer: search = first 40 chars of (number + ' ' + text) for numbered footnotes — i.e., "15 Human Rights Committee, general comm…" — for bare opener "5" with text "A/79/270, paras. 84 and 85." → "5 A/79/270, paras. 84 and 85." — searching that in paragraphs → 0 hits expected. For displaced footnote D: its first line without number: "A/42/427, p. 24." — search that. Good, I'll build search accordingly: for normal footnotes: (number + ' ' + lines.join(' ')).slice(0,40) — wait but the plan example shows "15 Human Rights Committee, general comm…" which is exactly number + space + text start. For bare opener, number + ' ' + text. Same thing. For displaced: text only. For '*': skip (not counted, but could still search? skip). 

Hmm, but careful: a footnote like "5 A/79/270, paras. 84 and 85." — could "5 A/79/270..." appear in a paragraph? No. OK.

But also: what if a footnote's text is short, e.g. "6 See A/42/427." — search "6 See A/42/427." — fine.

Edge: footnote text could be empty? Then search = number alone → false positives. I'll require search length ≥ 8 chars, else skip (note it). Eh, I'll just use it; data likely fine. Actually to be safe: if search.trim().length < 6, skip and count as skipped. Fine.

Check 7 — Headers and footers: pages with header (hadHeader count / total), pages with page number (hadPageNumber; expected all but first page), displaced numbers listed "6 on page 2, 14 on page 5, ...". pass if all pages had header and all but first had page number. Hmm — "expected all" for header; "expected all but the first" for page number. pass = (headerCount === totalPages) && (pageNumberCount === totalPages - 1 || ...). Actually page 1 has no page number (has date stamp). So expected pageNumberCount = totalPages - 1. But what if first page had a page number? Then expected all. I'll compute expected = records[0] had page number ? total : total-1. Simpler: pass if every page except possibly the first has a page number, and all have headers. I'll define: headerPass = all hadHeader; footerPass = all pages except the first have hadPageNumber. Combined check pass = headerPass && footerPass. Detail lists displaced.

Check 8 — Headings: counts: labelled roman, labelled letter, unlabelled; list unlabelled (cap 30). pass always (informational)? Checks need pass/fail — heading check: pass if no unlabelled heading looks like paragraph text? Hard to auto-judge. I'll make it informational-pass: "pass" if headings found > 0 and none of the unlabelled headings ends with sentence punctuation (by construction they don't). Hmm. Let me define pass = (headings.length > 0). Detail: "23 unlabelled headings listed below so a reader can spot a paragraph's last line mistaken for a heading". I'll mark pass with the counts. It's a check that "tells a story". OK.

Check 9 — Nothing lost: sum(classCounts) + unclassified === totalNonEmpty. pass if equal and unclassified empty. List unclassified with page.

Also hyphen count: report in method section: "lines ending in a hyphen: 0 (no hyphen joining was needed)".

Now — "n of m checks pass": m = checks with status pass/fail (not 'notrun'). If ref missing, checks 1-5 'notrun'; 6 needs ref.footnotes — notrun; 7,8,9 run. Header pill: if any fail → red "n checks failed" else green "n of m checks pass". If some notrun, mention? Keep simple: pill shows pass/fail of run checks; if notrun exist, add "(k not run — no reference)". Hmm, plan: "If reference or one of its fields is missing, the tiles say 'no reference in this file' and the checks that need it show 'not run', never 'pass'." I'll show pill "n of m checks pass" where m excludes notrun; if notrun>0 append "· k not run". Fine.

Tab 04 red dot when failures: add a red dot span in tab 04 label.

Now rendering functions. Let me write the render:

```js
function render(){
  const d = docs[state.sel];
  // header
  // rail cards
  // tabs panels
}
```

Since tabs panels content is large, I'll render all four panels each time selection changes (rebuild innerHTML). Use event delegation or rebind after render. I'll use inline onclick attributes? Better: addEventListener after building, or event delegation on document with data attributes. I'll use delegation: document.addEventListener('click', handler) checking closest('[data-action]'). Actions: tab switch, row toggle, detail toggle, copy citation, headings box toggle, repair log toggle, raw pages toggle, raw page select change, download csv, doc card select, check link goto, tile repair link.

Let me now also handle the "Show the PDF's lines" toggle: each detail row has a button; toggling shows a `<pre>`-like div with lines and page markers. I'll pre-render the lines HTML in the detail row (hidden), toggle hidden.

Detail row content:
```html
<tr class="detail" id="d-12" hidden><td colspan="5">
  <div class="fulltext">…marked text…</div>
  <button class="tog" data-action="rawlines" aria-expanded="false" aria-controls="rl-12">Show the PDF's lines</button>
  <div class="rawlines" id="rl-12" hidden>…lines with page markers…</div>
  <div class="fw">Reference first words: "…" · Found: "…" — <span class="ok">equal</span></div>
  <div class="meta2">Pages 3–4 · cites footnotes 2, 3 · repairs: …</div>
  <button class="copy" data-action="copy" data-cite="E/C.12/GC/27, para. 12">Copy citation</button>
</td></tr>
```

Page markers in rawlines: for each line of the paragraph, if line.page !== prevPage, insert marker div "── page p ──". Lines joined with '\n' in a pre-wrap div.

Copy: navigator.clipboard?.writeText(cite).then(ok).catch(fallback); fallback textarea+execCommand. Then button text "Copied" for 2s.

Now tab 01 tiles:

```html
<div class="tiles">
  <div class="tile"><div class="mono fig">FIG.01</div><div class="bignum serif">90</div><div class="tilelabel">paragraphs found</div><div class="tilecmp">The document has: <b>90</b> <span class="ok">— equal</span></div><div class="how">How this is computed: …</div></div>
  ...
</div>
```

Tile 1 compare: green when equal, red with difference: e.g., "The document has: 90 — found 88 (−2)" red.

Tile 4: repairs count + link `<a href="#" data-action="openRepairs">repair log on tab 04</a>`.

If no ref: tiles show "no reference in this file".

Tab 03: caption "141 footnotes found, 141 expected". Table No.|Page|Text|Repair. Download button.

Tab 04: 
```html
<h3 class="serif">Checks</h3>
<div class="checks"> each: <div class="check pass|fail"><span class="mono">CHK.01</span> <b>Paragraph count.</b> Found 90, reference says 90. <span class="ok">pass</span></div> ...</div>
<button class="sect" data-action="repairs" aria-expanded="false">Repair log (163)</button>
<div id="repairlog" hidden> counts per kind + table </div>
<button class="sect" data-action="rawpages" aria-expanded="false">Raw pages</button>
<div id="rawpages" hidden> select + panel + legend </div>
<h3>Download</h3>
<button data-action="dlcsv">Download paragraphs as CSV</button>
<p class="how">method text…</p>
```

Check lines with links: for first-words mismatches, "para. 12" links → data-action="goto" data-para="12" → switch to tab 02, expand row, scrollIntoView.

Now — the tab keyboard nav:

```js
tablist.addEventListener('keydown', e => {
  const tabs = [...tablist.querySelectorAll('[role=tab]')];
  let idx = tabs.indexOf(document.activeElement);
  if (idx<0) return;
  if (e.key==='ArrowRight'||e.key==='ArrowDown') { idx=(idx+1)%tabs.length; }
  else if (e.key==='ArrowLeft'||e.key==='ArrowUp') { idx=(idx-1+tabs.length)%tabs.length; }
  else if (e.key==='Home') idx=0; else if (e.key==='End') idx=tabs.length-1; else return;
  e.preventDefault(); tabs[idx].focus(); activateTab(idx);
});
```

activateTab: set aria-selected, tabindex, hidden panels.

Panels: hidden attribute on inactive panels. "the tab panel of a hidden tab is not focusable" — hidden handles that.

Now — the rail card click: data-action="doc" data-i="0".

Now let me also compute the rail card bars: share = found/ref; bar width = min(share,1)*100%; color red if found!==ref else green.

Header pill: dot + text.

Footer: source, built, honesty.

Now — one more requirement: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — the header has symbol link. Paragraph rows: citation includes symbol; the CSV has symbol+doc_url. In the paragraphs table, maybe add symbol link in... the plan's table columns don't include symbol. The header covers it. Footnote rows: no symbol column either. Hmm — "Every row that shows a document has its symbol, linked to doc_url" — the document rows (rail cards) should have symbol linked. I'll make the rail card symbol a link to doc_url. And header symbol link. Good.

Now — writing all this code. It's going to be long (~900-1100 lines). Let me be careful and systematic.

Let me also double check the footer regex for date stamp: "051125 061125" — /^(\d{6} )*\d{6}$/ matches "051125 061125" ✓. Also single "051125" ✓.

Job code: "GE.25-15926" and "GE.25-15926 (E)" — /^GE\./ ✓.

Bare number 1-3 digits: /^\d{1,3}$/ ✓.

Now — potential issue: the footer loop could eat into footnote block if the last footnote's text ends with a bare number line? E.g., footnote text "…see 12." — not bare. OK.

Another: page 1 footer: "GE.25-15926 (E)" and "051125 061125" — both dropped. Page 1 has no page number → hadPageNumber false. Expected.

Now — the block-start scan on page 1: lines include cover + "I." + "Introduction" + "1." + paragraph text + footnote block. nextFootnote=1. Scan: first line matching bare "1" or "1 " or "* ". Cover lines: "6 November 2025" starts with "6 " — nextFootnote is 1, no. "1." — bare? "1." has period → /^\d{1,3}$/ fails; startsWith("1 ")? "1." no. Good. Paragraph text lines starting with "1 "? Possibly! E.g., a wrapped line starting with "1 " — hmm. If any body line on page 1 starts with "1 " before the footnote block, blockStart would be wrong. The plan says the rule works. But wait — actually there's a real concern: paragraph text lines are wrapped at ~90 chars; a line could start with "1 " if the text has "... 1 something" wrapping. Risk exists but plan asserts it works on this data. Also the asterisk "* " line: if it appears before footnote 1... The scan takes the FIRST match among all patterns. If "* Adopted..." is at the foot after numbered footnotes, then "1" (bare) comes first. If asterisk is before footnote 1, block starts at "*". Either way fine.

Hmm — wait, actually one more concern: on page 1, is there a bare "1" line in the body? The paragraph start is "1." not "1". OK.

But here's a trickier one: pages 2-20 — body text lines starting with e.g. "5 " when nextFootnote==5? The footnote block is at the foot; body lines come before. If a body line starts with "5 " and nextFootnote==5, blockStart would be set there — wrong! But plan says the rule works on this data ("the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space"). Presumably in this document no body line starts with the current nextFootnote + space before the footnote block. Trust it. Hmm, but wait — actually, is that plausible? Body lines are wrapped prose; a line starting with a number followed by space... e.g., "2025" is 4 digits — startsWith("2025 ")? nextFootnote max 141, so "2025 " doesn't match unless nextFootnote... no, startsWith(nextFootnote+' ') with nextFootnote ≤ 141 — "2025 " starts with "2"? nextFootnote+' ' = "2 " — "2025 " starts with "2" then "0" — "2 " requires space after 2. "2025 " → "2" then "0" ≠ " ". So no. A line starting "12 May 2025"? starts with "12 " — if nextFootnote==12 at that point → false positive. Possible in theory. The plan says it works; also the check panel would reveal problems (footnote count wrong). I'll trust the plan — it explicitly describes this rule as what works on the examined file.

Hmm, wait — actually let me re-read: "On each page, after header and footer are gone, the block starts at the first line that is a bare number equal to nextFootnote, or starts with that number and a space, or starts with '* ' on the first page". Yes. Trust.

Now — one more: within-block opener "starts with a number and a space" — ANY number, even not expected ("Any line that starts with a number and a space opens a footnote, even when the number is not the one expected"). So within block, opener regex /^(\d{1,3}) / or bare. But careful: a footnote text continuation line could start with a number+space? E.g., footnote text wrapping: "…resolution 79/172 of 12\nDecember 2024" — continuation line "December 2024" starts with letter. But a wrapped line could start with "12 December 2024"? Then it'd wrongly open footnote 12. Plan says "never add a numbered line to the footnote before it" — accept. Trust data.

Now, the sequential footnote-mark rule — one more check: "Every run of one to three digits not touching another digit, a slash, a dash or an opening parenthesis is a candidate". My excluded set for before/after chars: digit, '/', '-', '('. What about the run being part of "art. 11"? before char is space → candidate; if counter==11 → marked. The plan says the check lists rejected numbers so reader sees "article 11" not bracketed — implying in this data, when "article 11" appears, counter ≠ 11. OK.

Hmm — wait, actually there's a subtlety: "not touching ... an opening parenthesis" — e.g., "(11)" — before is '(' → excluded. But what about "para. 11)" — after is ')' → allowed candidate. If counter==11 → marked "[11])" — wrong but per spec. Trust.

Now — marks in text: "waste.2" → "waste.[2]". My replace inserts brackets around digits: raw.slice(last, m.index) + '[' + run + ']'. ✓.

Now — the check "Footnote marks ... expected to run from 1 to reference.footnotes without a gap" — marksFound should be exactly 1..141. With sequential counter, marksFound is increasing by 1 each time — so it's 1..k where k = number of marks found. Missing = ref.footnotes - k if k < ref.footnotes. Also if a mark number was skipped (candidate ≠ counter), counter doesn't advance → subsequent marks all mismatch → cascade. The check lists missing numbers. OK.

Now — CSV download filename: symbol.replace(/\//g,'-') → "E-C.12-GC-27-paragraphs.csv". ✓.

Now let me think about the "How this is computed" line near every chart/number — tiles have them; rail card numbers have small notes; tables have captions. OK.

Now, writing the actual code. Let me draft the full HTML.

Also — title of app: use data.title. Header kicker: "UN DOCUMENT · PDF TEXT". 

Let me write CSS carefully for the design:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b4f;--soft:#6b655a}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
[hidden]{display:none!important}
a{color:var(--red)}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
header.top{padding:26px 34px 16px;border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:8px 28px;align-items:flex-end;justify-content:space-between}
...
```

Layout: 
```css
.layout{display:flex;align-items:flex-start}
.rail{width:264px;flex:0 0 264px;border-right:1px solid var(--rule);padding:18px 18px 28px;position:sticky;top:0;max-height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:18px 30px 60px}
```

Hmm sticky rail — fine.

Tabs:
```css
.tabs{display:flex;gap:4px;border-bottom:1px solid var(--rule);margin-bottom:18px;flex-wrap:wrap}
.tabs [role=tab]{appearance:none;background:none;border:none;border-bottom:2px solid transparent;padding:10px 12px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.14em;color:var(--soft)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
```

Tiles:
```css
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:0 26px;margin:6px 0 22px}
.tile{border-top:1px solid var(--rule);padding:12px 2px 16px}
.bignum{font-family:Georgia,serif;font-size:52px;line-height:1.05;font-weight:400}
```

Tables:
```css
table{width:100%;border-collapse:collapse;margin:6px 0 18px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:19px;padding:10px 0 6px}
caption .mono{color:var(--soft);margin-right:10px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--soft);text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px;font-weight:400}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
tr.prow{cursor:pointer}
tr.prow:hover td{background:#efe9dc}
.rowbtn{appearance:none;background:none;border:none;font:inherit;color:var(--red);font-family:Georgia,serif;font-weight:700;cursor:pointer;padding:0 4px}
```

Hmm — the No. cell: red serif number as button. Section cell: small text. First line: 120 chars. Check cell: OK green / differ red.

Detail row: `tr.detail td{background:#efe9dc;padding:14px 18px}`.

Raw viewer:
```css
.rawpanel{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;line-height:1.5;border:1px solid var(--rule);background:#f8f5ee;max-height:520px;overflow:auto;padding:8px 0}
.rl{display:flex;gap:10px;padding:0 10px;white-space:pre-wrap;word-break:break-word}
.rl .ln{flex:0 0 3ch;text-align:right;color:var(--soft)}
.rl .code{flex:0 0 1.5ch;text-align:center;font-weight:700}
.rl.c-cover{background:#eae1cd}.rl.c-header{background:#f2dcd4}.rl.c-heading{background:#e7ddc0}.rl.c-paragraph{background:transparent}.rl.c-footnote{background:#e0e6d6}.rl.c-footer{background:#e6dfee}.rl.c-unclassified{background:#f3d2d2}
```

Legend swatches similar.

Check panel:
```css
.check{border-bottom:1px solid var(--rule);padding:9px 2px;display:flex;gap:12px;align-items:baseline}
.check .st{font-family:ui-monospace...; }
.ok{color:var(--green)} .bad{color:var(--red)}
```

Pill:
```css
.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--rule);padding:6px 12px;border-radius:999px;font-family:mono...}
.dot{width:9px;height:9px;border-radius:50%;background:var(--green)} .dot.red{background:var(--red)}
```

Rail card:
```css
.doccard{border:1px solid var(--rule);border-left:3px solid transparent;padding:12px 14px;margin-bottom:14px;cursor:pointer;background:#f8f5ee}
.doccard.sel{border-left-color:var(--red)}
.doccard .bignum{font-size:40px}
.bar{height:4px;background:var(--rule);margin:4px 0 2px}
.bar i{display:block;height:100%;background:var(--green)} .bar i.red{background:var(--red)}
```

OK. Now the JS. Let me write it fully now, being careful.

```js
(function(){
'use strict';
var DATA = window.WORKSHOP_DATA || {};
function esc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function norm(s){ return String(s==null?'':s).replace(/[\u201C\u201D]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim(); }

var docKeys = Object.keys(DATA).filter(function(k){
  var d = DATA[k];
  return d && Array.isArray(d.records) && d.records.length>0 && d.reference && typeof d.reference==='object';
});

function parseDocument(data){ ... }
```

Let me write parseDocument completely (as designed above), then checks, then render.

One thing: repairs need `para` reference for per-paragraph repair listing. I'll tag repairs with `paraNum` when target is a paragraph. For "heading separated" target 'before para. N' → paraNum = N. For joins/splits → paraNum = number. I'll add field `para` (number string) where applicable.

Per-paragraph repairs: filter repairs by para === p.number.

Now checks construction. Let me write:

```js
function buildChecks(R){
  var ref = R.ref;
  var checks = [];
  function add(id, name, status, detailHtml, links){ checks.push({id:id,name:name,status:status,detail:detailHtml,links:links||[]}); }
  var hasRef = !!(ref && ref.paragraphs!=null);
  // CHK.01 paragraph count
  if (hasRef) {
    var ok = R.paragraphs.length === ref.paragraphs;
    add('CHK.01','Paragraph count', ok?'pass':'fail',
      'Found <b>'+R.paragraphs.length+'</b> numbered paragraphs; the document\u2019s reference says <b>'+esc(ref.paragraphs)+'</b>.');
  } else add('CHK.01','Paragraph count','notrun','No reference in this file.');
  ...
}
```

Hmm — detail uses HTML with esc for data values. Fine.

CHK.02 numbering: 
```js
var nums = R.paragraphs.map(p=>parseInt(p.number,10));
var gaps=[], dupes=[];
var seen={};
nums.forEach(function(n){ if(seen[n]) dupes.push(n); seen[n]=1; });
for (var e=1;e<=nums.length;e++) if(!seen[e]) gaps.push(e);
// also numbers beyond length
```
Actually "The paragraph numbers are exactly 1 to n in order; gaps and duplicates are listed by number and page." So check nums[i]===i+1. If not, list. I'll compute mismatches: for i, if nums[i]!==i+1 → record "position i holds para. nums[i] (page x)". Plus dupes/gaps lists. pass if all in order.

CHK.03 first words: mismatches array {n, found, ref}. pass if 0. links to paras.

CHK.04 footnotes: numbered = footnotes.filter(f=>f.number!=='*'); count vs ref.footnotes; numbering 1..count; restored list. pass if count===ref.footnotes && numbering ok.

CHK.05 marks: marksFound vs ref.footnotes: missing = numbers 1..ref.footnotes not in marksFound; rejected list (cap 15). pass if no missing && marksFound.length===ref.footnotes. Hmm — marksFound is 1..k by construction; missing = k+1..ref.footnotes. Also if marksFound.length > ref.footnotes → extra. pass = marksFound.length===ref.footnotes (and sequence ok by construction). detail lists missing and rejected with context.

CHK.06 footnotes out of paragraphs: hits. For each footnote (numbered + '*'? just numbered + asterisk? I'll include all with search), for each paragraph, if p.text_raw.indexOf(f.search) !== -1 → hit {footnote, para}. Also long paragraphs >300 words. pass if hits===0. Flag paragraphs: p.containsFootnotes = true. Detail: "Searched the first 40 characters of each of the 141 footnote opener lines in the raw text of all 90 paragraphs: 0 hits. Longest paragraph: 254 words (limit 300)." fail lists hits.

Wait — the search should be in "the raw text of every paragraph, before footnote marks are touched" — text_raw ✓.

CHK.07 headers/footers: headerPages = pageInfo.filter(hadHeader).length; pageNumPages = filter(hadPageNumber); displaced list. pass = headerPages===total && pageNumPages >= total-1. detail.

CHK.08 headings: roman count, letter count, unlabelled count + list (cap 30, each with page). pass = headings.length>0. Hmm — should it ever fail? If zero headings found → fail ("no headings found — paragraph text may be swallowing headings"). OK.

CHK.09 nothing lost: sum classCounts + unclassified.length === totalNonEmpty && unclassified.length===0. pass accordingly. detail: "Every non-empty line classified exactly once: cover 9, header 20, heading 45, paragraph 700, footnote 350, footer 60 — total N of N non-empty lines."

Also hyphenLines count → put in method text on tab 04 and maybe CHK.09 detail. I'll add to method.

Now — "n of m checks pass": m = checks.filter(status!=='notrun').length; n = pass count. fails = m-n.

Now render. Let me write renderDoc(R) building HTML strings for panels, then wire events via delegation.

Given size, I'll build HTML with template strings and esc().

Panel 02 rows: for each paragraph:
```js
var firstLine = p.text.length>120 ? p.text.slice(0,120).replace(/\s+\S*$/,'') + '…' : p.text;
```
Hmm "first 120 characters cut at a word with '…'": take slice(0,120), cut back to last space, add '…'. If text ≤120, show whole (no ellipsis? maybe still fine). I'll do: if len>120 → cut at last space within 120 + '…'.

Check cell: 
```js
var chk = [];
if (p.first_words_match === false) chk.push('<span class="bad">first words differ</span>');
if (p.containsFootnotes) chk.push('<span class="bad">contains footnotes</span>');
if (!chk.length) chk.push('<span class="ok">OK</span>');
```

Row:
```html
<tr class="prow" data-para="12">
 <td class="num"><button class="rowbtn" data-action="toggle" aria-expanded="false" aria-controls="d-12">12</button></td>
 <td class="sec">Right to work (art. 6)</td>
 <td class="num">3–4</td>
 <td class="fl">…first line…</td>
 <td class="ck">OK</td>
</tr>
<tr class="detail" id="d-12" hidden><td colspan="5">…</td></tr>
```

Detail content:
```html
<div class="path mono">IV. … › Right to work (art. 6)</div>
<p class="fulltext">marked text</p>
<button class="tog mono" data-action="rawlines" aria-expanded="false" aria-controls="rl-12">Show the PDF's lines</button>
<div class="rawlines" id="rl-12" hidden>…</div>
<p class="fwcmp">Reference first six words: <i>“…”</i> · found: <i>“…”</i> — <span class="ok">equal</span></p>
<p class="pmeta">Pages 3–4 · cites footnotes 2, 3 · repairs: number and text split; paragraph joined across a page break</p>
<button class="copybtn" data-action="copy" data-cite="...">Copy citation</button>
```

rawlines content: lines with page markers:
```js
var rl = p.lines.map(function(l,idx){
  var s = '';
  if (idx===0 || l.page !== p.lines[idx-1].page) s += '<div class="pgmark">── page '+l.page+' ──</div>';
  return s + '<div>'+esc(l.text.trim())+'</div>';
}).join('');
```
in a pre-wrap container.

Hmm — p.lines stores {page, idx, text}. ✓.

Copy citation: data-cite = symbol + ', para. ' + number.

Panel 03 footnotes rows:
```html
<tr><td class="num">6</td><td class="num">2</td><td>A/42/427, p. 24.</td><td class="bad">number restored from the page foot</td></tr>
```
Asterisk row: number '*', note "cover note, not counted".

Caption: "141 footnotes found, 141 expected" + TAB.03? Table numbering: TAB.01 paragraphs, TAB.02 footnotes, TAB.03 repairs, TAB.04 raw? I'll number tables sequentially per tab: paragraphs table TAB.01, footnotes TAB.02, repair log TAB.03. Fine.

Panel 04: checks list, repair log, raw pages, download, method.

Repair log: counts per kind:
```js
var kinds = {}; R.repairs.forEach(r=>{kinds[r.kind]=(kinds[r.kind]||0)+1;});
```
Line: "header line removed ×20 · footer line removed ×58 · …" Then table Page | Paragraph or footnote | What was done | Before | After. Cap rows? ~160 rows fine. Maybe cap at 400 for safety.

Raw pages: select with options "Show raw page n" — label "Show raw page" + select of pages. Panel: lines with numbers and class colours. Build per selected page; on change re-render panel. I'll render all pages? 20 pages × ~45 lines = 900 divs — fine, but select shows one at a time. I'll render only selected page's lines into the panel; on change, re-render. Store lineCls per page.

Legend: six items with code letters and names + unclassified.

Download CSV: build and trigger.

Method text on tab 04: short paragraph describing pipeline + hyphen count + "How this is computed" for checks: "Each check compares two values this page computed itself…".

Now — event delegation:

```js
document.addEventListener('click', function(e){
  var el = e.target.closest('[data-action]');
  if (!el) {
    // row click forwarding
    var tr = e.target.closest('tr.prow');
    if (tr) { var b = tr.querySelector('.rowbtn'); if (b && e.target!==b && !e.target.closest('button')) b.click(); }
    return;
  }
  var a = el.getAttribute('data-action');
  if (a==='tab'){ activateTab(+el.getAttribute('data-i')); }
  else if (a==='doc'){ state.sel = +el.getAttribute('data-i'); renderAll(); }
  else if (a==='toggle'){ var tr = el.closest('tr'); var d = document.getElementById(el.getAttribute('aria-controls')); var open = d.hasAttribute('hidden'); if(open){d.removeAttribute('hidden'); el.setAttribute('aria-expanded','true');} else {d.setAttribute('hidden',''); el.setAttribute('aria-expanded','false');} }
  ...
});
```

Careful: `e.target.closest('button')` — if the click was on the rowbtn itself, the data-action branch handles it. The row-forward branch only when no data-action element matched — but rowbtn has data-action, so clicking it goes to branch. Clicking elsewhere in row → forward. But my code: `var el = e.target.closest('[data-action]')` — if click on row text, el is null → row forward. But if click on detail row content (no data-action), tr.prow closest? detail row is separate tr, not prow. OK. But careful: clicking the copy button inside detail — has data-action → handled. Clicking rawlines toggle — data-action. Good.

Wait — issue: `e.target.closest('[data-action]')` — the tab buttons have data-action="tab". The doc cards data-action="doc". OK.

Actions list:
- tab: activateTab(i)
- doc: select doc, renderAll
- toggle: expand/collapse row detail (aria-controls)
- rawlines: toggle the rawlines div
- copy: copy citation, feedback
- headings: toggle headings box
- repairs: toggle repair log (and if opened via tile link, also switch to tab 04 first)
- rawpages: toggle raw pages section
- dlcsv: download paragraphs CSV
- dlfn: download footnotes CSV
- goto: switch to tab 02 (or 03), expand row, scroll
- openrepairs: activateTab(3) then open repair log + scroll

Select change: document.addEventListener('change', ...) for raw page select → render raw panel.

Keyboard: tablist keydown.

Copy fallback:
```js
function copyText(t, btn){
  function done(ok){ btn.textContent = ok?'Copied':'Press Ctrl+C'; setTimeout(function(){btn.textContent='Copy citation';},2000); }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(t).then(function(){done(true);}, function(){fallback();});
  } else fallback();
  function fallback(){
    var ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    var ok=false; try{ ok=document.execCommand('copy'); }catch(err){}
    document.body.removeChild(ta); done(ok);
  }
}
```

CSV:
```js
function csvEscape(v){ return '"'+String(v==null?'':v).replace(/"/g,'""')+'"'; }
function downloadCSV(filename, header, rows){
  var lines=[header.map(csvEscape).join(',')];
  rows.forEach(function(r){ lines.push(r.map(csvEscape).join(',')); });
  var csv='\uFEFF'+lines.join('\r\n')+'\r\n';
  var blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a'); a.href=url; a.download=filename; document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); },500);
}
```

Paragraph CSV rows:
```js
var header=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','text_lines','footnotes_cited','repairs','citation','symbol','doc_url'];
rows = R.paragraphs.map(p=>[p.number, p.section, p.part, p.page_start, p.page_end, p.first_words_reference, p.first_words_found, p.first_words_match===null?'':(p.first_words_match?'yes':'no'), p.text, p.text_raw, p.text_lines, p.footnotes_cited.join(' '), p.repairs.map(r=>r.kind).join('; '), p.citation, R.symbol, R.docUrl]);
filename = R.symbol.replace(/\//g,'-')+'-paragraphs.csv';
```

Footnotes CSV: header ['number','page','text','repair','symbol','doc_url']; repair = repaired ? 'number restored from the page foot' : ''.

Now — renderAll: builds header, rail, panels; called on doc change. Tab state per render: keep state.tab.

Let me now also handle "Repairs made: n, a link to the repair log on tab 04" — tile 4 link: `<a href="#repairs" data-action="openrepairs">repair log on tab 04</a>`.

Check links: `<a href="#" data-action="goto" data-tab="1" data-para="12">para. 12</a>`.

goto handler: activateTab(tab); then find row [data-para] → expand detail; scrollIntoView.

Now — the header pill and tab 04 dot: computed from checks.

Let me now also make sure: "At the right a green dot and 'n of m checks pass', or a red dot and 'n checks failed' (and a red dot on tab 04)."

Rail card: "n of m checks pass" linking to tab 04: `<a data-action="tab" data-i="3">`.

Now — writing everything. Also the intro sentence under header meta: "This page splits the converter's raw text into numbered paragraphs, removes headers, footers and footnotes, checks itself against the document's reference, and lists every repair it made."

Footer: `<footer>` with source line: `Source: {data.source}` + built + honesty line. Always visible — place after layout, border-top.

Let me now also decide the "what the page does" line and "How this is computed" notes text.

Now — potential pitfall: `records` count is string "20" per plan ("count is the string '20'"). I use records.length for pages — fine, and display "n pages" from records.length. Header: "20 pages of raw converter text".

reference.adopted — display "adopted " + adopted.

Now — one more detail: the plan says rail card shows "its short title". pdf_text.title is the full title "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development". I'll show it clamped.

Let me now write the final code. I'll aim for clarity and correctness. Let me write it in one pass, mentally testing.

Also — important: the app must handle `WORKSHOP_DATA.pdf_text` possibly having `built`? Not in spec; guard.

Edge: doc_url may be empty string — link only if present.

Let me write the parse function now, final version, with all pieces:

```js
function parseDocument(data){
  var symbol = data.symbol || '';
  var ref = (data.reference && typeof data.reference==='object') ? data.reference : null;
  var records = (data.records||[]).slice().sort(function(a,b){return a.page-b.page;});
  var firstPage = records.length ? records[0].page : 1;
  var repairs = [], warnings = [], footnotes = [], bodyLines = [];
  var lineCls = {}; // page -> array
  var classCounts = {cover:0,header:0,heading:0,paragraph:0,footnote:0,footer:0};
  var totalNonEmpty = 0, hyphenLines = 0;
  var nextFootnote = 1;
  var pageInfo = [];

  records.forEach(function(rec){
    var page = rec.page;
    var raw = String(rec.text==null?'':rec.text).split('\n');
    var cls = raw.map(function(){return null;});
    lineCls[page] = cls;
    raw.forEach(function(l){ if(l.trim()!=='') totalNonEmpty++; if(/-\s*$/.test(l)) hyphenLines++; });
    var i=0; while(i<raw.length && raw[i].trim()==='') i++;
    var hadHeader=false;
    if(i<raw.length && raw[i].trim()===symbol){
      cls[i]='header'; classCounts.header++; hadHeader=true;
      repairs.push({page:page, ord:i, para:null, target:'page header', kind:'header line removed', before:raw[i], after:'(removed from the body)'});
      i++;
    } else if(i<raw.length){
      warnings.push('Page '+page+': the first non-empty line is not the symbol "'+symbol+'".');
    }
    var j=raw.length-1, displaced=[], hadPageNumber=false, footerLines=[];
    while(j>=i){
      var t=raw[j].trim();
      if(t===''){ j--; continue; }
      if(/^GE\./.test(t) || /^(\d{6} )*\d{6}$/.test(t) || /^\d{1,3}$/.test(t)){
        cls[j]='footer'; classCounts.footer++;
        footerLines.push({idx:j, text:raw[j]});
        if(/^\d{1,3}$/.test(t)){ var n=parseInt(t,10); if(n===page) hadPageNumber=true; else displaced.push(n); }
        j--; continue;
      }
      break;
    }
    footerLines.forEach(function(f){
      repairs.push({page:page, ord:f.idx, para:null, target:'page footer', kind:'footer line removed', before:f.text, after:'(removed from the body)'});
    });
    var lines=[]; for(var k=i;k<=j;k++) lines.push({idx:k, text:raw[k]});
    var blockStart=-1;
    for(var q=0;q<lines.length;q++){
      var tt=lines[q].text.trim(); if(tt==='') continue;
      if(/^\d{1,3}$/.test(tt) && parseInt(tt,10)===nextFootnote){ blockStart=lines[q].idx; break; }
      if(tt.indexOf(nextFootnote+' ')===0){ blockStart=lines[q].idx; break; }
      if(page===firstPage && tt.indexOf('* ' )===0){ blockStart=lines[q].idx; break; }
    }
    if(blockStart===-1){
      for(var q2=0;q2<lines.length;q2++){
        var t2=lines[q2].text.trim();
        if(/^\d{1,3}$/.test(t2) && parseInt(t2,10)>nextFootnote){
          blockStart=lines[q2].idx;
          repairs.push({page:page, ord:lines[q2].idx, para:null, target:'footnote block', kind:'footnote count jumped', before:'expected footnote '+nextFootnote, after:'block starts at footnote '+t2+' on page '+page});
          warnings.push('Page '+page+': no line opens footnote '+nextFootnote+'; the block starts at '+t2+'.');
          break;
        }
      }
    }
    if(blockStart===-1){
      warnings.push('Page '+page+': no footnote block found; every line is body.');
      pageInfo.push({page:page, hadHeader:hadHeader, hadPageNumber:hadPageNumber, displaced:displaced, blockFound:false});
    } else {
      var block=lines.filter(function(L){return L.idx>=blockStart;});
      block.forEach(function(L){ cls[L.idx]='footnote'; classCounts.footnote++; });
      repairs.push({page:page, ord:blockStart, para:null, target:'footnote block', kind:'footnote block removed', before:block.length+' lines at the foot of page '+page, after:'moved out of the body text into footnotes'});
      var cur=null, firstFn=null, seen=[];
      function pushCur(){ if(cur){ cur.text=cur.lines.join(' ').replace(/  +/g,' ').trim(); footnotes.push(cur); cur=null; } }
      block.forEach(function(L){
        var tt=L.text.trim(); if(tt==='') return;
        var bare=/^(\d{1,3})$/.exec(tt), numSpace=/^(\d{1,3}) (.+)$/.exec(tt);
        if(bare || numSpace){
          pushCur();
          var num = bare?bare[1]:numSpace[1];
          cur={number:num, page:page, lines:numSpace?[numSpace[2]]:[], repaired:false, asterisk:false};
          cur.search=(num+' '+(numSpace?numSpace[2]:cur.lines.join(' '))).slice(0,40);
          if(!firstFn) firstFn=cur;
          seen.push(parseInt(num,10));
          return;
        }
        if(page===firstPage && tt.indexOf('* ' )===0){
          pushCur();
          cur={number:'*', page:page, lines:[tt], repaired:false, asterisk:true};
          cur.search=tt.slice(0,40);
          return;
        }
        if(cur){
          if(displaced.length && cur===firstFn && cur.lines.some(function(l){return /\.$/.test(l.trim());})){
            pushCur();
            var D=displaced[0];
            cur={number:String(D), page:page, lines:[tt], repaired:true, asterisk:false};
            cur.search=tt.slice(0,40);
            seen.push(D);
            repairs.push({page:page, ord:L.idx, para:null, target:'footnote '+D, kind:'footnote number restored', before:'"'+tt.slice(0,60)+'" had no number; '+D+' sat alone in the page foot', after:'restored as footnote '+D});
            return;
          }
          cur.lines.push(tt);
        }
      });
      pushCur();
      var maxSeen = seen.length?Math.max.apply(null,seen):0;
      var maxDisp = displaced.length?Math.max.apply(null,displaced):0;
      nextFootnote = Math.max(nextFootnote, maxSeen, maxDisp)+1;
      pageInfo.push({page:page, hadHeader:hadHeader, hadPageNumber:hadPageNumber, displaced:displaced, blockFound:true});
    }
    for(var q3=0;q3<lines.length;q3++){
      var L=lines[q3];
      if(blockStart===-1 || L.idx<blockStart){ if(L.text.trim()!=='') bodyLines.push({page:page, idx:L.idx, text:L.text, cls:null}); }
    }
  });
```

Wait — bug: `cur.search` for bare opener: `(num+' '+(numSpace?numSpace[2]:cur.lines.join(' ')))` — at that point cur.lines is [] for bare, so search = num+' ' — too short. I need the first text line, which arrives later. Fix: set search after pushCur, or compute search at pushCur time: `cur.search = (cur.number==='*' ? '' : cur.number+' ') + cur.lines.join(' ')` sliced 40 — but for displaced footnote, search should be its first line WITHOUT number. Let me compute search in pushCur:

```js
function pushCur(){
  if(!cur) return;
  cur.text = cur.lines.join(' ').replace(/  +/g,' ').trim();
  var prefix = (cur.repaired || cur.asterisk) ? '' : cur.number+' ';
  cur.search = (prefix + cur.text).slice(0,40);
  footnotes.push(cur); cur=null;
}
```

Hmm — for normal footnotes, search = "15 Human Rights Committee, general comm…" ✓ (number + space + text). For displaced (repaired), search = text only ✓. For '*', text only. Good. But wait — for a bare-number opener, the number is on its own line and text follows; search = "5 A/79/270, paras. 84 and 85." — includes number ✓ matches plan ("its number included").

Hmm, but plan says "The first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…')". For bare opener "5", the line that opens is "5" — first 40 chars = "5". But that would false-positive. The example shows number+text, so they mean the opener line when it has text. My approach (number + first text) is the sensible reading. But hmm — for bare opener, maybe they intend just the following text line? "for a footnote whose number was displaced, its first line" — for displaced, first line (no number). For normal, the opener line including number. For bare opener, the opener line is just the number... I'll go with number+text — safer against false positives and matches the example. Actually wait — could "5 A/79/270..." appear in a paragraph? No. Could "A/79/270, paras. 84 and 85." appear in a paragraph? Possibly (citations repeat)! That's why they include the number. OK, number+text it is.

Now body parse:

```js
  var paragraphs=[], headings=[];
  var cur=null, heading=null, state='cover';
  var lastHeading=null, lastRoman=null;
  function isParaStart(t){ return /^(\d{1,3})\.$/.test(t) || /^(\d{1,3})\. .+$/.test(t); }
  function paraNumOf(t){ var m=/^(\d{1,3})\./.exec(t); return m?m[1]:null; }
  function isLabel(t){ return /^([IVX]+|[A-Z])\.$/.test(t); }
  function isUnlabelled(t,nextT){
    if(!isParaStart(nextT)) return false;
    if(t.length>90) return false;
    if(!/^\p{Lu}/u.test(t)) return false;
    if(/[.;:,\d]$/.test(t)) return false;
    return true;
  }
  function closeHeading(){
    if(heading){
      heading.title = heading.lines.join(' ');
      headings.push(heading);
      lastHeading = heading;
      if(heading.kind==='roman') lastRoman = heading;
      heading=null;
    }
  }
  function closePara(){
    if(!cur) return;
    var p=cur; cur=null;
    var raw=p.lines.map(function(l){return l.text.trim();}).join(' ').replace(/  +/g,' ').trim();
    var pages=p.lines.map(function(l){return l.page;});
    p.text_raw=raw;
    p.page_start=pages[0]; p.page_end=pages[pages.length-1];
    p.text_lines=p.lines.map(function(l){return l.text.trim();}).join(' | ');
    if(pages.some(function(pg){return pg!==p.page_start;})){
      var lastOfStart = null, firstOfEnd=null;
      p.lines.forEach(function(l){ if(l.page===p.page_start) lastOfStart=l; if(firstOfEnd===null && l.page!==p.page_start) firstOfEnd=l; });
      repairs.push({page:p.page_start, ord:p.lines[p.lines.length-1].idx, para:p.number, target:'para. '+p.number, kind:'paragraph joined across a page break',
        before:'page '+p.page_start+' ends \u201c\u2026'+String(lastOfStart.text.trim()).slice(-40)+'\u201d \u2016 page '+p.page_end+' begins \u201c'+String(firstOfEnd.text.trim()).slice(0,40)+'\u2026\u201d',
        after:'joined into one paragraph'});
    }
    paragraphs.push(p);
  }
  for(var i=0;i<bodyLines.length;i++){
    var L=bodyLines[i];
    var t=L.text.trim();
    var nextT = i+1<bodyLines.length ? bodyLines[i+1].text.trim() : '';
    if(isParaStart(t)){
      closeHeading(); closePara();
      var num=paraNumOf(t);
      cur={number:num, lines:[], page:L.page};
      cur.section = lastHeading ? (lastHeading.lines.length? lastHeading.lines[lastHeading.lines.length-1] : lastHeading.label+'.') : '';
      cur.part = lastRoman ? (lastRoman.label+'.'+(lastRoman.lines.length?' '+lastRoman.lines.join(' '):'')) : '';
      cur.headingIsRoman = (lastHeading===lastRoman);
      var inline=/^(\d{1,3})\. (.+)$/.exec(t);
      if(inline){
        cur.lines.push({page:L.page, idx:L.idx, text:inline[2]});
        repairs.push({page:L.page, ord:L.idx, para:num, target:'para. '+num, kind:'number and text split', before:t, after:num+'. \u2016 '+inline[2]});
      }
      L.cls='paragraph'; state='body';
      continue;
    }
    if(isLabel(t)){
      closeHeading(); closePara();
      var m=/^([IVX]+|[A-Z])\.$/.exec(t);
      heading={label:m[1], lines:[], page:L.page, kind:/^[IVX]+$/.test(m[1])?'roman':'letter'};
      L.cls='heading';
      continue;
    }
    if(heading){
      if((/^[a-z(]/u.test(t)) && heading.lines.length){
        var prev=heading.lines[heading.lines.length-1];
        heading.lines[heading.lines.length-1]=prev+' '+t;
        repairs.push({page:L.page, ord:L.idx, para:null, target:'heading '+heading.label+'.', kind:'heading title joined from two lines', before:prev+' \u2016 '+t, after:prev+' '+t});
      } else {
        heading.lines.push(t);
      }
      L.cls='heading';
      continue;
    }
    if(isUnlabelled(t,nextT)){
      closePara();
      var h={label:null, lines:[t], title:t, page:L.page, kind:'unlabelled'};
      headings.push(h); lastHeading=h;
      var nn=paraNumOf(nextT);
      repairs.push({page:L.page, ord:L.idx, para:nn, target:'before para. '+nn, kind:'heading separated from paragraph text', before:'\u201c'+t+'\u201d sat directly above para. '+nn, after:'kept as a heading: \u201c'+t+'\u201d'});
      L.cls='heading'; state='body';
      continue;
    }
    if(state==='cover' || !cur){ L.cls='cover'; classCounts.cover++; continue; }
    L.cls='paragraph';
    cur.lines.push({page:L.page, idx:L.idx, text:t});
  }
  closeHeading(); closePara();
  // class counts for body lines
  bodyLines.forEach(function(L){ if(L.cls==='paragraph') classCounts.paragraph++; else if(L.cls==='heading') classCounts.heading++; else if(L.cls==='cover') classCounts.cover++; });
```

Hmm wait — I increment classCounts.cover in the loop AND in the forEach — double count. Let me only count in the forEach. Remove the increment in the loop. Also unclassified: bodyLines with cls null → but all get cls. Let me compute unclassified = bodyLines.filter(L=>!L.cls). And classCounts from the forEach only. Also header/footer/footnote counted during page processing. Good — remove `classCounts.cover++` from loop.

Wait, also there's a subtle issue with `state==='cover' || !cur` — after closePara due to unlabelled heading, cur is null and state='body'; next line is the para start → handled. OK. But if state==='body' and cur===null (shouldn't happen except right after heading), lines would be cover — edge, fine.

Hmm — another subtle issue: `closePara()` inside isUnlabelled branch — but what if state==='cover' and cur===null? closePara no-op. Fine.

Now — section/part assignment: I set cur.section at para start from lastHeading/lastRoman. But lastHeading updates only when a heading CLOSES (closeHeading). An unlabelled heading pushes directly and sets lastHeading ✓. A labelled heading sets lastHeading when closed — which happens when the next para start or label arrives — BEFORE the para start creates cur? Order in loop: isParaStart branch calls closeHeading() first, then creates cur and reads lastHeading ✓. isLabel branch calls closeHeading() then creates new heading ✓. Good.

But wait — in the isParaStart branch I call closeHeading() then closePara() — closePara uses cur (previous para) ✓, then create new cur with section from lastHeading (just closed) ✓.

Path: cur.path = cur.headingIsRoman ? cur.part : (cur.part ? cur.part+' › '+cur.section : cur.section). Hmm — if headingIsRoman, section is the roman title; path = part (which includes title). E.g., para 1: part="I. Introduction", section="Introduction", path="I. Introduction". Else path = "IV. … › Right to work (art. 6)". ✓ matches example format.

Now footnote marks:

```js
  var markCounter=1, marksFound=[], rejected=[];
  paragraphs.forEach(function(p){
    var raw=p.text_raw, out='', last=0, m, re=/\d+/g;
    p.footnotes_cited=[];
    while((m=re.exec(raw))){
      var run=m[0], bi=m.index, ai=bi+run.length;
      var before = bi>0?raw.charAt(bi-1):'', after = ai<raw.length?raw.charAt(ai):'';
      var bad = function(ch){ return ch!=='' && /[\d\/\-(\d]/.test(ch); };
      var candidate = run.length<=3 && !bad(before) && !bad(after);
      if(candidate && parseInt(run,10)===markCounter){
        out += raw.slice(last,bi)+'['+run+']';
        last=ai;
        marksFound.push(markCounter);
        p.footnotes_cited.push(markCounter);
        markCounter++;
      } else if(candidate){
        rejected.push({number:run, para:p.number, context: raw.slice(Math.max(0,bi-30), Math.min(raw.length, ai+30))});
      }
    }
    out += raw.slice(last);
    p.text = out;
  });
```

Wait — the bad char class: /[\d\/\-(\d]/ — includes digit twice, fine: chars excluded: digit, '/', '-', '('. ✓.

Hmm — one issue: `bad('')` returns false (empty string → ch!=='' false → returns false) ✓.

First words:

```js
  paragraphs.forEach(function(p){
    var noMarks = p.text.replace(/\[\d+\]/g,'');
    var words = noMarks.split(/\s+/).filter(Boolean).slice(0,6).join(' ');
    p.first_words_found = words;
    p.first_words_reference = (ref && ref.first_words) ? (ref.first_words[String(p.number)] != null ? String(ref.first_words[String(p.number)]) : '') : '';
    p.first_words_match = ref ? (norm(words)===norm(p.first_words_reference)) : null;
    p.citation = symbol + ', para. ' + p.number;
    p.repairs = repairs.filter(function(r){ return String(r.para)===String(p.number); });
  });
```

Hmm — p.repairs: repairs with para===p.number. But repairs pushed during body parse have para set for splits/joins/heading-separated. ✓.

Wait — order: p.repairs computed after all repairs pushed ✓ (marks loop after body parse; repairs all pushed by then). But footnote repairs have para=null ✓.

Footnote containment check:

```js
  var fnHits=[];
  footnotes.forEach(function(f){
    if(!f.search || f.search.trim().length<6) return;
    paragraphs.forEach(function(p){
      if(p.text_raw.indexOf(f.search)!==-1) fnHits.push({fn:f.number, para:p.number});
    });
  });
  paragraphs.forEach(function(p){ p.containsFootnotes = fnHits.some(function(h){return h.para===p.number;}); });
  var longParas = paragraphs.filter(function(p){ return p.text_raw.split(/\s+/).length>300; }).map(function(p){return {n:p.number, w:p.text_raw.split(/\s+/).length}; });
```

Now checks:

```js
  var checks=[];
  function add(id,name,status,detail,links){ checks.push({id:id,name:name,status:status,detail:detail,links:links||[]}); }
  var hasRef = !!(ref && ref.paragraphs!=null);
  var numbered = footnotes.filter(function(f){return f.number!=='*';});
  // CHK.01
  if(hasRef){
    add('CHK.01','Paragraph count', paragraphs.length===ref.paragraphs?'pass':'fail',
      'Found <b>'+paragraphs.length+'</b> numbered paragraphs; the reference says <b>'+esc(ref.paragraphs)+'</b>.');
  } else add('CHK.01','Paragraph count','notrun','No reference in this file, so this check was not run.');
  // CHK.02 numbering
  var numIssues=[];
  paragraphs.forEach(function(p,idx){ if(parseInt(p.number,10)!==idx+1) numIssues.push('position '+(idx+1)+' holds para. '+esc(p.number)+' (page '+p.page_start+')'); });
  var seen={}, dupes=[];
  paragraphs.forEach(function(p){ var n=parseInt(p.number,10); if(seen[n]) dupes.push(n); seen[n]=1; });
  if(hasRef){
    add('CHK.02','Numbering', numIssues.length===0 && dupes.length===0 ?'pass':'fail',
      'Paragraph numbers run 1 to '+paragraphs.length+(numIssues.length||dupes.length?' — problems: '+esc(numIssues.concat(dupes.map(function(d){return 'duplicate para. '+d;})).join('; ')):' in order, no gaps, no duplicates.'));
  } else add('CHK.02','Numbering','notrun','No reference in this file.');
```

Hmm — CHK.02 doesn't strictly need ref (checks 1..n internally). But plan groups it under checks needing reference? "the checks that need it show 'not run'" — numbering check compares to 1..n which is internal; but expected count comes from ref. I'll run it regardless (it doesn't need ref): status pass/fail based on internal order. Actually "The paragraph numbers are exactly 1 to n in order" — n = found count. Internal. I'll run always. Fine.

  // CHK.03 first words
```js
  var fwMis=[];
  paragraphs.forEach(function(p){ if(p.first_words_match===false) fwMis.push(p); });
  if(hasRef && ref.first_words){
    add('CHK.03','First words', fwMis.length===0?'pass':'fail',
      fwMis.length===0 ? 'All '+paragraphs.length+' paragraphs start with the six words the reference expects.'
      : fwMis.length+' of '+paragraphs.length+' differ: '+ fwMis.slice(0,10).map(function(p){return 'para. '+p.number+' found \u201c'+esc(p.first_words_found)+'\u201d / reference \u201c'+esc(p.first_words_reference)+'\u201d';}).join('; ')+(fwMis.length>10?' …':''),
      fwMis.slice(0,20).map(function(p){return {label:'para. '+p.number, tab:1, para:p.number};}));
  } else add('CHK.03','First words','notrun','No reference first_words in this file.');
```

  // CHK.04 footnotes
```js
  var fnNums = numbered.map(function(f){return parseInt(f.number,10);});
  var fnDupes=[], fnSeen={};
  fnNums.forEach(function(n){ if(fnSeen[n]) fnDupes.push(n); fnSeen[n]=1; });
  var fnGaps=[]; for(var e=1;e<=fnNums.length;e++) if(!fnSeen[e]) fnGaps.push(e);
  var restored = footnotes.filter(function(f){return f.repaired;});
  if(hasRef && ref.footnotes!=null){
    var ok4 = numbered.length===ref.footnotes && fnGaps.length===0 && fnDupes.length===0;
    add('CHK.04','Footnotes', ok4?'pass':'fail',
      'Found <b>'+numbered.length+'</b> numbered footnotes; the reference says <b>'+esc(ref.footnotes)+'</b>. Numbers run 1 to '+numbered.length+(fnGaps.length||fnDupes.length?' — gaps: '+fnGaps.join(', ')+' duplicates: '+fnDupes.join(', '):' with no gaps or duplicates.')+
      (restored.length?' Restored from page feet: '+restored.map(function(f){return 'footnote '+f.number+' (page '+f.page+')';}).join(', ')+'.':''));
  } else add('CHK.04','Footnotes','notrun','No reference in this file.');
```

  // CHK.05 marks
```js
  var missing=[];
  if(hasRef && ref.footnotes!=null){ for(var e2=1;e2<=ref.footnotes;e2++) if(marksFound.indexOf(e2)===-1) missing.push(e2); }
  var ok5 = hasRef && ref.footnotes!=null ? (marksFound.length===ref.footnotes && missing.length===0) : true;
  if(hasRef && ref.footnotes!=null){
    add('CHK.05','Footnote marks', ok5?'pass':'fail',
      'Found '+marksFound.length+' footnote marks in the paragraphs; the reference expects '+esc(ref.footnotes)+'.'+
      (missing.length?' Missing: '+missing.join(', ')+'.':'')+
      ' Rejected as real numbers, not marks: '+ (rejected.length? rejected.slice(0,8).map(function(r){return r.number+' in para. '+r.para+' (\u201c'+esc(r.context)+'\u201d)';}).join('; ')+(rejected.length>8?' …':'') : 'none.'));
  } else add('CHK.05','Footnote marks','notrun','No reference in this file.');
```

Hmm — CHK.05 without ref: could still check marks run 1..k without gap (by construction they do). notrun fine.

  // CHK.06
```js
  add('CHK.06','Footnotes stay out of the paragraphs', fnHits.length===0?'pass':'fail',
    'Searched the first 40 characters of each of the '+footnotes.length+' footnote opener lines in the raw text of all '+paragraphs.length+' paragraphs: <b>'+fnHits.length+'</b> hits (expected 0).'+
    (longParas.length?' Paragraphs over 300 words: '+longParas.map(function(p){return 'para. '+p.n+' ('+p.w+' words)';}).join(', ')+'.':' Longest paragraph: '+maxWords+' words (limit 300).')+
    (fnHits.length?' Hits: '+fnHits.slice(0,10).map(function(h){return 'footnote '+h.fn+' text found in para. '+h.para;}).join('; '):''),
    fnHits.slice(0,20).map(function(h){return {label:'para. '+h.para, tab:1, para:h.para};}));
```

maxWords = max word count. Compute.

  // CHK.07
```js
  var hdrOk = pageInfo.filter(function(p){return p.hadHeader;}).length;
  var pgOk = pageInfo.filter(function(p){return p.hadPageNumber;}).length;
  var allDisp = [];
  pageInfo.forEach(function(p){ p.displaced.forEach(function(d){ allDisp.push(d+' on page '+p.page); }); });
  var ok7 = hdrOk===records.length && pgOk>=records.length-1;
  add('CHK.07','Headers and footers', ok7?'pass':'fail',
    'Pages whose first line was the symbol: <b>'+hdrOk+' of '+records.length+'</b>. Pages with their own number in the footer: <b>'+pgOk+' of '+records.length+'</b> (the first page carries a date stamp instead).'+
    (allDisp.length?' Displaced footnote numbers found in page feet: '+esc(allDisp.join(', '))+'.':' No displaced numbers.'));
```

  // CHK.08
```js
  var romanH = headings.filter(function(h){return h.kind==='roman';}).length;
  var letterH = headings.filter(function(h){return h.kind==='letter';}).length;
  var unlab = headings.filter(function(h){return h.kind==='unlabelled';});
  add('CHK.08','Headings', headings.length>0?'pass':'fail',
    'Labelled headings: '+romanH+' roman-numbered, '+letterH+' lettered. Unlabelled headings (a line directly above a paragraph number): <b>'+unlab.length+'</b>'+(unlab.length?' — '+unlab.slice(0,30).map(function(h){return '\u201c'+esc(h.title)+'\u201d (page '+h.page+')';}).join(', ')+(unlab.length>30?' …':''):'')+'.');
```

  // CHK.09
```js
  var sum=0; for(var k in classCounts) sum+=classCounts[k];
  var unclassified = [];
  // recompute: every non-empty line should have a class
  records.forEach(function(rec){
    var cls = lineCls[rec.page];
    var raw = String(rec.text||'').split('\n');
    raw.forEach(function(l,idx){ if(l.trim()!=='' && !cls[idx]) unclassified.push({page:rec.page, line:idx+1, text:l}); });
  });
  var ok9 = unclassified.length===0 && sum===totalNonEmpty;
  add('CHK.09','Nothing lost', ok9?'pass':'fail',
    'Every non-empty line classified exactly once: cover '+classCounts.cover+', header '+classCounts.header+', heading '+classCounts.heading+', paragraph '+classCounts.paragraph+', footnote '+classCounts.footnote+', footer '+classCounts.footer+' — total <b>'+sum+'</b> of <b>'+totalNonEmpty+'</b> non-empty lines.'+(unclassified.length?' Unclassified: '+unclassified.slice(0,10).map(function(u){return 'page '+u.page+' line '+u.line+' \u201c'+esc(u.text.slice(0,50))+'\u201d';}).join('; '):''));
```

Wait — sum counts classified non-empty lines; totalNonEmpty counts all non-empty. If some line unclassified, sum < total. ok9 requires both. ✓.

Hmm — but blank lines inside body: they're not in bodyLines (skipped) and cls stays null — but they're empty so not counted in totalNonEmpty ✓. In raw viewer they show uncoloured ✓.

Return object R with everything.

Now — one thing I missed: `p.lines` for the raw-lines toggle — I keep p.lines (array of {page, idx, text}) ✓.

Also `R.lineCls`, `R.rawPages = records.map(r=>({page:r.page, lines:String(r.text||'').split('\n')}))`.

Now render. Let me write renderAll():

```js
var state={sel:0, tab:0};
var docs = docKeys.map(function(k){ return parseDocument(DATA[k]); });

function activateTab(i){
  state.tab=i;
  var tabs=document.querySelectorAll('.tabs [role=tab]');
  tabs.forEach(function(t,idx){
    t.setAttribute('aria-selected', idx===i?'true':'false');
    t.tabIndex = idx===i?0:-1;
    var p=document.getElementById('panel-'+idx);
    if(idx===i) p.removeAttribute('hidden'); else p.setAttribute('hidden','');
  });
}
```

renderAll builds:
- header content
- rail
- panels 0..3

Let me write the HTML builders.

Header:
```js
function headerHtml(R){
  var ref=R.ref;
  var meta = [];
  if(R.docUrl) meta.push('<a href="'+esc(R.docUrl)+'" target="_blank" rel="noopener">'+esc(R.symbol)+'</a>');
  else meta.push(esc(R.symbol));
  if(ref && ref.adopted!=null) meta.push('adopted '+esc(ref.adopted));
  meta.push(R.records.length+' pages of raw converter text');
  if(R.source) meta.push(esc(R.source));
  var pill;
  var run = R.checks.filter(function(c){return c.status!=='notrun';});
  var pass = run.filter(function(c){return c.status==='pass';}).length;
  var fail = run.length-pass;
  if(fail>0) pill='<span class="pill"><span class="dot red"></span>'+fail+' check'+(fail>1?'s':'')+' failed of '+run.length+' run</span>';
  else pill='<span class="pill"><span class="dot"></span>'+pass+' of '+run.length+' checks pass'+(run.length<R.checks.length?' · '+(R.checks.length-run.length)+' not run':'')+'</span>';
  return '<div class="kicker mono">UN DOCUMENT · PDF TEXT</div>'+
    '<h1 class="serif">'+esc(R.title)+'</h1>'+
    '<p class="meta">'+meta.join(' · ')+'</p>'+
    '<p class="what">This page splits the converter\u2019s raw text into numbered paragraphs, removes headers, footers and footnotes, checks itself against the document\u2019s reference, and lists every repair it made.</p>'+
    '<div class="pillwrap">'+pill+'</div>';
}
```

Hmm — header layout: I'll structure header as flex with left block and pill right.

Rail:
```js
function railHtml(){
  return '<h2 class="mono railhead">DOCUMENT</h2>' + docs.map(function(R,i){
    var ref=R.ref;
    var pFound=R.paragraphs.length, fFound=R.footnotes.filter(function(f){return f.number!=='*';}).length;
    var pRef = ref&&ref.paragraphs!=null?ref.paragraphs:null;
    var fRef = ref&&ref.footnotes!=null?ref.footnotes:null;
    function bar(found, rf){
      if(rf==null) return '';
      var share = rf>0 ? Math.min(found/rf,1)*100 : 100;
      var cls = found===rf?'':' red';
      return '<div class="bar"><i class="'+cls+'" style="width:'+share+'%"></i></div>';
    }
    var run=R.checks.filter(function(c){return c.status!=='notrun';});
    var pass=run.filter(function(c){return c.status==='pass';}).length;
    var chk = (run.length-pass)>0 ? (run.length-pass)+' checks failed' : pass+' of '+run.length+' checks pass';
    return '<div class="doccard'+(i===state.sel?' sel':'')+'" data-action="doc" data-i="'+i+'" role="button" tabindex="0" aria-label="Show '+esc(R.symbol)+'">'+
      '<div class="mono sym">'+(R.docUrl?'<a href="'+esc(R.docUrl)+'" target="_blank" rel="noopener" onclick="event.stopPropagation()">'+esc(R.symbol)+'</a>':esc(R.symbol))+'</div>'+
      '<div class="ctitle">'+esc(R.title)+'</div>'+
      '<div class="cmeta">'+(ref&&ref.adopted!=null?'adopted '+esc(ref.adopted)+' · ':'')+R.records.length+' pages</div>'+
      '<div class="bignum serif">'+pFound+'</div><div class="blabel">paragraphs found'+(pRef!=null?' of '+pRef:'')+'</div>'+bar(pFound,pRef)+
      '<div class="bignum serif">'+fFound+'</div><div class="blabel">footnotes found'+(fRef!=null?' of '+fRef:'')+'</div>'+bar(fFound,fRef)+
      '<div class="clink"><a data-action="tab" data-i="3">'+esc(chk)+' → tab 04</a></div>'+
    '</div>';
  }).join('');
}
```

Hmm — nested data-action (card vs inner links): clicking the symbol link should open doc, not switch doc — stopPropagation on the anchor click... but my delegation uses closest('[data-action]') — the anchor has no data-action, but the card does; closest from anchor finds card → would trigger doc switch. I added onclick="event.stopPropagation()" — but delegation is on document; stopPropagation in inline onclick prevents reaching document ✓. But the tab link inside card has data-action="tab" — closest finds the anchor first ✓ (closest returns nearest ancestor including self). Good.

Also keyboard: doccard role=button tabindex=0 — need Enter/Space handler. I'll add keydown delegation: if e.target matches '.doccard' and key Enter/Space → click. Add in the keydown listener.

Panels:

Panel 0 (RESULT):
```js
function panel0(R){
  var ref=R.ref;
  var hasRef = ref && ref.paragraphs!=null;
  var pFound=R.paragraphs.length;
  var fFound=R.footnotes.filter(function(f){return f.number!=='*';}).length;
  var fwOk = R.paragraphs.filter(function(p){return p.first_words_match===true;}).length;
  var fwN = R.paragraphs.filter(function(p){return p.first_words_match!=null;}).length;
  var fnBad = R.paragraphs.filter(function(p){return p.containsFootnotes;}).length;
  function cmp(found, rf){
    if(rf==null) return '<span class="noref">no reference in this file</span>';
    if(found===rf) return '<span class="ok">The document has: <b>'+rf+'</b> — equal</span>';
    var d=found-rf;
    return '<span class="bad">The document has: <b>'+rf+'</b> — found '+found+' ('+(d>0?'+':'')+d+')</span>';
  }
  ...
}
```

Tiles:
```html
<div class="tiles">
 <div class="tile"><div class="mono fig">FIG.01</div><div class="bignum serif">90</div><div class="tlabel">paragraphs found</div><div class="tcmp">…</div><div class="how">How this is computed: every body line that starts a numbered paragraph, joined across page breaks, counted by this page's code.</div></div>
 <div class="tile">FIG.02 footnotes found n of 141 … how: footnote openers in each page's footnote block, plus numbers restored from page feet.</div>
 <div class="tile">FIG.03 first words match n of 90 … how: first six words of each extracted paragraph (marks removed) compared with the reference after normalising quotes, dashes and spaces.</div>
 <div class="tile">FIG.04 repairs made n … <a data-action="openrepairs">repair log on tab 04</a> … how: every change the script logged while parsing.</div>
</div>
```

Tile 1 extra: if fnBad>0 add red note "n paragraphs contain footnote text". 

Panel 1 (PARAGRAPHS):
```js
function panel1(R){
  var ref=R.ref;
  var headBox = '<button class="sect mono" data-action="headings" aria-expanded="false" aria-controls="headbox">Headings found: '+R.headings.length+'</button>'+
    '<div id="headbox" hidden><ul class="hlist">'+R.headings.map(function(h){
      return '<li>'+(h.label?esc(h.label)+'. ':'')+esc(h.title||h.lines.join(' '))+' <span class="mono">p. '+h.page+'</span></li>';
    }).join('')+'</ul></div>';
  var rows = R.paragraphs.map(function(p){
    var fl = p.text.length>120 ? p.text.slice(0,120).replace(/\s+\S*$/,'')+'…' : p.text;
    var ck=[];
    if(p.first_words_match===false) ck.push('<span class="bad">first words differ</span>');
    if(p.containsFootnotes) ck.push('<span class="bad">contains footnotes</span>');
    if(!ck.length) ck.push('<span class="ok">OK</span>');
    var pages = p.page_start===p.page_end ? String(p.page_start) : p.page_start+'–'+p.page_end;
    var detail = detailHtml(R,p);
    return '<tr class="prow" data-para="'+esc(p.number)+'">'+
      '<td class="num"><button class="rowbtn" data-action="toggle" aria-expanded="false" aria-controls="d-'+esc(p.number)+'">'+esc(p.number)+'</button></td>'+
      '<td class="sec">'+esc(p.section||'—')+'</td>'+
      '<td class="num">'+esc(pages)+'</td>'+
      '<td class="fl">'+esc(fl)+'</td>'+
      '<td class="ck">'+ck.join(' ')+'</td></tr>'+
      '<tr class="detail" id="d-'+esc(p.number)+'" hidden><td colspan="5">'+detail+'</td></tr>';
  }).join('');
  var cap = (R.paragraphs.length) + ' paragraphs found, ' + (ref&&ref.paragraphs!=null?ref.paragraphs:'?') + ' expected';
  return headBox+
   '<table><caption><span class="mono">TAB.01</span>'+esc(cap)+'</caption>'+
   '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>'+
   '<tbody>'+rows+'</tbody></table>'+
   '<p class="note">Footnote marks inside a paragraph are shown in square brackets, e.g. <code>waste.[2]</code>. Remove them with find-and-replace using the pattern <code>\\[\\d+\\]</code>. Click a row for the full text, the PDF\u2019s own lines, and a citation to copy.</p>';
}
```

detailHtml:
```js
function detailHtml(R,p){
  var rl = p.lines.map(function(l,idx){
    var s='';
    if(idx===0 || l.page!==p.lines[idx-1].page) s+='<div class="pgmark mono">── page '+l.page+' ──</div>';
    return s+'<div class="rline">'+esc(l.text.trim())+'</div>';
  }).join('');
  var fw = p.first_words_match===null ? 'no reference' :
    (p.first_words_match ? '<span class="ok">equal</span>' : '<span class="bad">different</span>');
  var reps = p.repairs.length ? p.repairs.map(function(r){return esc(r.kind);}).join('; ') : 'none';
  var fn = p.footnotes_cited.length ? 'cites footnotes '+p.footnotes_cited.join(', ') : 'cites no footnotes';
  var pages = p.page_start===p.page_end ? 'page '+p.page_start : 'pages '+p.page_start+'–'+p.page_end;
  return '<div class="path mono">'+esc(p.path||p.section||'')+'</div>'+
    '<p class="fulltext">'+esc(p.text)+'</p>'+
    '<button class="tog mono" data-action="rawlines" aria-expanded="false" aria-controls="rl-'+esc(p.number)+'">Show the PDF\u2019s lines</button>'+
    '<div class="rawlines" id="rl-'+esc(p.number)+'" hidden>'+rl+'</div>'+
    '<p class="fwcmp">Reference first six words: <i>\u201c'+esc(p.first_words_reference)+'\u201d</i> · found: <i>\u201c'+esc(p.first_words_found)+'\u201d</i> — '+fw+'</p>'+
    '<p class="pmeta">'+esc(pages)+' · '+esc(fn)+' · repairs: '+reps+'</p>'+
    '<button class="copybtn" data-action="copy" data-cite="'+esc(p.citation)+'">Copy citation</button>';
}
```

Panel 2 (FOOTNOTES):
```js
function panel2(R){
  var ref=R.ref;
  var numbered=R.footnotes; // includes '*'
  var rows=R.footnotes.map(function(f){
    var rep = f.repaired ? '<span class="bad">number restored from the page foot</span>' : (f.asterisk?'cover note, not counted':'—');
    return '<tr><td class="num">'+esc(f.number)+'</td><td class="num">'+esc(f.page)+'</td><td class="ftext">'+esc(f.text)+'</td><td>'+rep+'</td></tr>';
  }).join('');
  var n = R.footnotes.filter(function(f){return f.number!=='*';}).length;
  var cap = n+' footnotes found, '+(ref&&ref.footnotes!=null?ref.footnotes:'?')+' expected';
  return '<table><caption><span class="mono">TAB.02</span>'+esc(cap)+'</caption>'+
   '<thead><tr><th scope="col" class="num">No.</th><th scope="col" class="num">Page</th><th scope="col">Text</th><th scope="col">Repair</th></tr></thead>'+
   '<tbody>'+rows+'</tbody></table>'+
   '<p class="note">Each paragraph on tab 02 lists the footnotes it cites. The cover\u2019s asterisked note is kept as footnote \u201c*\u201d and is not counted.</p>'+
   '<button class="dl" data-action="dlfn">Download footnotes.csv</button>';
}
```

Panel 3 (CHECKS & METHOD):
```js
function panel3(R){
  var checksHtml = R.checks.map(function(c){
    var st = c.status==='pass' ? '<span class="ok mono">pass</span>' : c.status==='fail' ? '<span class="bad mono">check failed</span>' : '<span class="mono noref">not run</span>';
    var links = c.links.length ? ' <span class="clinks">'+c.links.map(function(l){return '<a data-action="goto" data-tab="'+l.tab+'" data-para="'+esc(l.para)+'">'+esc(l.label)+'</a>';}).join(' ')+'</span>' : '';
    return '<div class="check"><span class="mono cid">'+c.id+'</span><span class="cbody"><b>'+esc(c.name)+'.</b> '+c.detail+links+'</span>'+st+'</div>';
  }).join('');
  // repair log
  var kinds={}; R.repairs.forEach(function(r){kinds[r.kind]=(kinds[r.kind]||0)+1;});
  var kindLine = Object.keys(kinds).map(function(k){return esc(k)+' ×'+kinds[k];}).join(' · ');
  var rrows = R.repairs.slice().sort(function(a,b){ return a.page-b.page || (a.ord-b.ord); }).map(function(r){
    return '<tr><td class="num">'+esc(r.page)+'</td><td>'+esc(r.target)+'</td><td>'+esc(r.kind)+'</td><td class="bf">'+esc(r.before)+'</td><td class="bf">'+esc(r.after)+'</td></tr>';
  }).join('');
  // raw pages
  var opts = R.records.map(function(rec){return '<option value="'+rec.page+'">page '+rec.page+'</option>';}).join('');
  ...
}
```

Raw pages panel: select + div#rawpanel. On change, render lines of selected page. I'll render initial page (first) at render time and handle change via delegation.

```js
function rawPageHtml(R, page){
  var rec = R.records.find(function(r){return r.page===page;});
  var cls = R.lineCls[page]||[];
  var lines = String(rec.text||'').split('\n');
  var html = lines.map(function(l,idx){
    var c = cls[idx]||'';
    var code = {cover:'C',header:'H',heading:'T',paragraph:'P',footnote:'N',footer:'F'}[c]||'?';
    var cl = c?('c-'+c):(l.trim()!==''?'c-unclassified':'');
    return '<div class="rl '+cl+'"><span class="ln">'+(idx+1)+'</span><span class="code">'+code+'</span><span class="lt">'+esc(l)+'</span></div>';
  }).join('');
  return html;
}
```

Legend:
```html
<div class="legend mono">
 <span><i class="sw c-cover"></i>C cover</span>
 <span><i class="sw c-header"></i>H header</span>
 <span><i class="sw c-heading"></i>T heading</span>
 <span><i class="sw c-paragraph"></i>P paragraph</span>
 <span><i class="sw c-footnote"></i>N footnote</span>
 <span><i class="sw c-footer"></i>F footer</span>
 <span><i class="sw c-unclassified"></i>? unclassified</span>
</div>
```

Panel 3 full:
```js
return '<h3 class="serif">Checks — can I trust this?</h3>'+
 '<p class="how">Each check compares two values this page computed itself, given this data and this code. A failed check never hides a result; it marks it.</p>'+
 '<div class="checks">'+checksHtml+'</div>'+
 '<button class="sect" data-action="repairs" aria-expanded="false" aria-controls="repairlog">Repair log ('+R.repairs.length+')</button>'+
 '<div id="repairlog" hidden><p class="kindline mono">'+kindLine+'</p>'+
 '<table><caption><span class="mono">TAB.03</span>Every change the script made, in document order</caption>'+
 '<thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead>'+
 '<tbody>'+rrows+'</tbody></table></div>'+
 '<button class="sect" data-action="rawpages" aria-expanded="false" aria-controls="rawsec">Raw pages</button>'+
 '<div id="rawsec" hidden><label class="mono" for="rawsel">Show raw page</label> <select id="rawsel" data-action="rawpage">'+opts+'</select>'+
 '<div class="legend mono">…</div><div class="rawpanel" id="rawpanel"></div></div>'+
 '<h3 class="serif">Download</h3>'+
 '<button class="dl" data-action="dlcsv">Download paragraphs as CSV</button>'+
 '<p class="note">UTF-8 with a byte-order mark, every field double-quoted, CRLF line ends. Columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, text_lines, footnotes_cited, repairs, citation, symbol, doc_url.</p>'+
 '<h3 class="serif">Method</h3>'+
 '<p class="how">The pipeline runs once on load over the pages in order: header line removed, footer lines removed (a bare number that is not the page number is kept aside as a displaced footnote number), the footnote block at the foot of each page separated from the body, footnotes parsed line by line (a number restored where the converter displaced it), body lines of all pages concatenated, paragraph numbers found in both forms (alone on a line, or with their text), headings separated, footnote marks bracketed by a sequential rule, first six words compared with the reference. Lines ending in a hyphen: '+R.hyphenLines+' (no hyphen joining was needed). Counting, splitting and matching are done by this page\u2019s code; no model was called and nothing left the browser.</p>';
```

Hmm — the honesty line is also in footer; fine to repeat briefly in method? The footer has it always visible. I'll keep method shorter and let footer carry the line. Actually plan's footer: "Source line, built date, and 'Counting, splitting and matching are done by this page's code; no model was called and nothing left the browser.'" — put in footer only.

Footer:
```js
'<footer><p class="mono">'+esc(R.source||'')+(R.built?' · built '+esc(R.built):'')+'</p><p>Counting, splitting and matching are done by this page\u2019s code; no model was called and nothing left the browser.</p></footer>'
```

Footer shows selected doc's source. OK.

Now the main render:

```js
function renderAll(){
  var R=docs[state.sel];
  document.getElementById('hd').innerHTML = headerHtml(R);
  document.getElementById('rail').innerHTML = railHtml();
  document.getElementById('panel-0').innerHTML = panel0(R);
  document.getElementById('panel-1').innerHTML = panel1(R);
  document.getElementById('panel-2').innerHTML = panel2(R);
  document.getElementById('panel-3').innerHTML = panel3(R);
  // raw panel initial
  var sel=document.getElementById('rawsel');
  if(sel){ document.getElementById('rawpanel').innerHTML = rawPageHtml(R, +sel.value); }
  activateTab(state.tab);
  // tab 04 red dot if failures
  var run=R.checks.filter(function(c){return c.status!=='notrun';});
  var fail=run.filter(function(c){return c.status==='fail';}).length;
  var t4=document.getElementById('tab-3');
  var dot = fail>0 ? ' <span class="dot red inline"></span>' : '';
  t4.innerHTML = '04 CHECKS & METHOD'+dot;
}
```

Hmm — tab labels: I'll set them statically in HTML and append dot via a span. Simpler: tab buttons static HTML with `<span id="tabdot"></span>`. I'll handle: `document.getElementById('tabdot').className = fail>0?'dot red inline':'dot inline hidden'`... Let me just include `<span class="dot red inline" id="tabdot" hidden></span>` in tab 4 label and toggle hidden.

Wait — but renderAll re-renders panels; tabs are static in HTML (not re-rendered) except the dot. Good — tabs static:

```html
<div class="tabs" role="tablist" aria-label="Sections">
  <button role="tab" id="tab-0" aria-controls="panel-0" aria-selected="true" data-action="tab" data-i="0">01 RESULT</button>
  <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="false" tabindex="-1" data-action="tab" data-i="1">02 PARAGRAPHS</button>
  <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1" data-action="tab" data-i="2">03 FOOTNOTES</button>
  <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1" data-action="tab" data-i="3">04 CHECKS &amp; METHOD<span class="dot red inline" id="tabdot" hidden></span></button>
</div>
```

Panels:
```html
<section role="tabpanel" id="panel-0" aria-labelledby="tab-0"></section>
...
```

Event delegation — click:

```js
document.addEventListener('click', function(e){
  var el = e.target.closest ? e.target.closest('[data-action]') : null;
  if(!el){
    var tr = e.target.closest ? e.target.closest('tr.prow') : null;
    if(tr){ var b=tr.querySelector('.rowbtn'); if(b && !e.target.closest('button')) b.click(); }
    return;
  }
  var a=el.getAttribute('data-action');
  if(a==='tab'){ activateTab(+el.getAttribute('data-i')); }
  else if(a==='doc'){ state.sel=+el.getAttribute('data-i'); state.tab=0; renderAll(); }
  else if(a==='toggle'){
    var ctl=document.getElementById(el.getAttribute('aria-controls'));
    if(ctl){ if(ctl.hasAttribute('hidden')){ctl.removeAttribute('hidden'); el.setAttribute('aria-expanded','true');} else {ctl.setAttribute('hidden',''); el.setAttribute('aria-expanded','false');} }
  }
  else if(a==='rawlines'){ same as toggle using aria-controls }
  else if(a==='headings' || a==='repairs' || a==='rawpages'){ toggle section by aria-controls }
  else if(a==='openrepairs'){ activateTab(3); var rl=document.getElementById('repairlog'); var btn=document.querySelector('[data-action="repairs"]'); if(rl && rl.hasAttribute('hidden')){ rl.removeAttribute('hidden'); btn.setAttribute('aria-expanded','true'); } rl.scrollIntoView? ... }
  else if(a==='copy'){ copyText(el.getAttribute('data-cite'), el); }
  else if(a==='goto'){ var tab=+el.getAttribute('data-tab'); activateTab(tab); var para=el.getAttribute('data-para'); var row=document.querySelector('tr.prow[data-para="'+para+'"]'); if(row){ var b=row.querySelector('.rowbtn'); if(b && b.getAttribute('aria-expanded')==='false') b.click(); row.scrollIntoView({block:'center'}); } }
  else if(a==='dlcsv'){ downloadParagraphsCSV(R_current()); }
  else if(a==='dlfn'){ downloadFootnotesCSV(R_current()); }
});
```

Hmm — toggle for rawlines/headings/repairs/rawpages all use aria-controls pattern — I can merge: if the element has aria-controls and action in (toggle, rawlines, headings, repairs, rawpages) → generic toggle. Let me just make all these use data-action="toggle" with aria-controls! Simpler: one action "toggle" for all expand/collapse buttons. The row buttons, rawlines, headings box, repair log, raw pages all use data-action="toggle" + aria-controls. 

But "openrepairs" needs tab switch + open + scroll. Keep separate.

Change event for rawsel:
```js
document.addEventListener('change', function(e){
  if(e.target.id==='rawsel'){ var R=docs[state.sel]; document.getElementById('rawpanel').innerHTML=rawPageHtml(R, +e.target.value); }
});
```

Keydown for tablist:
```js
document.querySelector('.tabs').addEventListener('keydown', function(e){
  var tabs=Array.prototype.slice.call(this.querySelectorAll('[role=tab]'));
  var idx=tabs.indexOf(document.activeElement);
  if(idx<0) return;
  var n=null;
  if(e.key==='ArrowRight'||e.key==='ArrowDown') n=(idx+1)%tabs.length;
  else if(e.key==='ArrowLeft'||e.key==='ArrowUp') n=(idx-1+tabs.length)%tabs.length;
  else if(e.key==='Home') n=0;
  else if(e.key==='End') n=tabs.length-1;
  if(n!==null){ e.preventDefault(); tabs[n].focus(); activateTab(n); }
});
```

Doccard keyboard:
```js
document.addEventListener('keydown', function(e){
  if((e.key==='Enter'||e.key===' ') && e.target.classList && e.target.classList.contains('doccard')){ e.preventDefault(); e.target.click(); }
});
```

Now — R_current() = docs[state.sel].

downloadParagraphsCSV:
```js
function downloadParagraphsCSV(R){
  var header=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','text_lines','footnotes_cited','repairs','citation','symbol','doc_url'];
  var rows=R.paragraphs.map(function(p){
    return [p.number, p.section, p.part, p.page_start, p.page_end, p.first_words_reference, p.first_words_found, p.first_words_match===null?'':(p.first_words_match?'yes':'no'), p.text, p.text_raw, p.text_lines, p.footnotes_cited.join(' '), p.repairs.map(function(r){return r.kind;}).join('; '), p.citation, R.symbol, R.docUrl];
  });
  downloadCSV(R.symbol.replace(/\//g,'-')+'-paragraphs.csv', header, rows);
}
```

downloadFootnotesCSV similar with header ['number','page','text','repair','symbol','doc_url'].

Now — panel0 details. Let me write:

```js
function panel0(R){
  var ref=R.ref, hasRef=ref&&ref.paragraphs!=null;
  var pFound=R.paragraphs.length;
  var fFound=R.footnotes.filter(function(f){return f.number!=='*';}).length;
  var fwMatch=R.paragraphs.filter(function(p){return p.first_words_match===true;}).length;
  var fwTotal=R.paragraphs.filter(function(p){return p.first_words_match!=null;}).length;
  var fnBad=R.paragraphs.filter(function(p){return p.containsFootnotes;}).length;
  function cmp(found, rf, label){
    if(rf==null) return '<div class="tcmp noref">no reference in this file</div>';
    if(found===rf) return '<div class="tcmp"><span class="ok">The document has: <b>'+rf+'</b> — equal</span></div>';
    var d=found-rf;
    return '<div class="tcmp"><span class="bad">The document has: <b>'+rf+'</b> — found '+found+' ('+(d>0?'+':'−')+Math.abs(d)+')</span></div>';
  }
  var tiles=
   '<div class="tile"><div class="mono fig">FIG.01</div><div class="bignum serif">'+pFound+'</div><div class="tlabel">paragraphs found</div>'+cmp(pFound, hasRef?ref.paragraphs:null)+
   (fnBad?'<div class="tcmp"><span class="bad">'+fnBad+' contain footnote text</span></div>':'')+
   '<div class="how">How this is computed: every body line that starts a numbered paragraph, in both forms, joined across page breaks — counted by this page\u2019s code.</div></div>'+
   '<div class="tile"><div class="mono fig">FIG.02</div><div class="bignum serif">'+fFound+'</div><div class="tlabel">footnotes found'+(hasRef&&ref.footnotes!=null?' of '+ref.footnotes:'')+'</div>'+
   (hasRef&&ref.footnotes!=null?cmp(fFound, ref.footnotes):'<div class="tcmp noref">no reference in this file</div>')+
   '<div class="how">How this is computed: footnote openers in each page\u2019s footnote block, plus numbers restored from page feet.</div></div>'+
   '<div class="tile"><div class="mono fig">FIG.03</div><div class="bignum serif">'+fwMatch+'</div><div class="tlabel">first words match, of '+fwTotal+' checked'+(hasRef?' (document has '+ref.paragraphs+')':'')+'</div>'+
   '<div class="how">How this is computed: the first six words of each extracted paragraph, footnote marks removed, compared with the reference after normalising quotes, dashes and spaces.</div></div>'+
   '<div class="tile"><div class="mono fig">FIG.04</div><div class="bignum serif">'+R.repairs.length+'</div><div class="tlabel">repairs made</div>'+
   '<div class="tcmp"><a data-action="openrepairs">see the repair log on tab 04</a></div>'+
   '<div class="how">How this is computed: every change the script logged while parsing — headers, footers, splits, joins, restored numbers.</div></div>';
  return '<div class="tiles">'+tiles+'</div>'+
   '<p class="note">The reference is a yardstick, not the truth: where the counts disagree, both numbers are shown and the difference is marked, and the result is never trimmed or padded to match.</p>';
}
```

Hmm — tile 3 label: "First words match: n of reference.paragraphs" per plan. fwTotal = paragraphs with match!=null = all (if ref). I'll show "n of ref.paragraphs". Let me use ref.paragraphs when hasRef.

Now — one more requirement: "Five things to click: four tabs and the repair-log link." ✓ (tiles have one link).

Tab 04 "Seven things to click: four tabs, the repair log and raw pages headings, and the download (the select appears once 'Raw pages' is open)." ✓.

Now — the headings box on tab 02: "A collapsible 'Headings found: n' box above the table" ✓.

Now — potential issue: `p.text.slice(0,120).replace(/\s+\S*$/,'')` — if the 120-char cut lands mid-word, cut back to last whitespace. If no whitespace in first 120 chars (unlikely), replace does nothing → slice stays 120 chars mid-word + '…'. Fine.

Now — the `esc` for text with quotes — fine.

Now — sizes: panel1 with 90 rows × 2 trs, each detail with full text — total maybe 200KB HTML. Fine.

Now — one more check on the pipeline: the "cover" classification — lines before first heading/para. On page 1: "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on economic, social and", "cultural rights and the environmental dimension of", "sustainable development*" → 9 cover lines. Then "I." label → heading. ✓.

Wait — hmm, "Distr.: General" — is it on its own line? Sample shows "Distr.: General\n6 November 2025\nOriginal: English". ✓.

But — careful: isUnlabelled check in cover state: "sustainable development*" — next line is "I." — isParaStart("I.")? No (not digits). So not unlabelled → cover ✓.

Another: "Introduction" — consumed by heading mode after "I." ✓ (heading mode branch comes before isUnlabelled).

Wait — order in my loop: isParaStart → isLabel → heading-mode → isUnlabelled → cover/para. "Introduction": not para start, not label, heading mode active → heading text ✓.

Now — what about page breaks mid-heading? E.g., "A." at end of page 3, title on page 4. Body lines concatenated → heading mode continues across pages ✓.

Now — the unlabelled heading at a page boundary: last line of page 3 is "Children", first line of page 4 is "12." → concatenated → nextT = "12." ✓ heading detected ✓.

Now — paragraph joined across page break: paragraph lines span pages → repair ✓. But note: the heading detection uses nextT across pages — a paragraph's last line on page 3 followed by "13." on page 4: if the last line meets unlabelled criteria → heading. That's per spec.

Now — one concern: `isUnlabelled` requires next line is para start. But what about the LAST body line of the whole document? nextT='' → not para start → paragraph text ✓.

Now — the footnote block detection on pages where nextFootnote opener is "N text" form (not bare). E.g., page with footnotes continuing: "15 Human Rights Committee..." — starts with "15 " and nextFootnote=15 → blockStart ✓.

Now — within-block: the first footnote on such a page is "15 Human Rights..." (numSpace opener) ✓.

Now — displaced page: block starts at bare "5" (== nextFootnote) ✓. firstFn = footnote 5. Its lines: after bare opener, blank skipped, "A/79/270, paras. 84 and 85." → continuation → cur.lines=["A/79/270, paras. 84 and 85."] — ends with '.' ✓. Next line "A/42/427, p. 24." → continuation, cur===firstFn, displaced.length=1, cur.lines has '.'-ending → becomes footnote 6 repaired ✓. Then "7 ..." opener → pushCur (footnote 6) ✓.

Wait — but there's an ordering bug: in my block loop, the check `cur.lines.some(l=>/\.$/.test(l.trim()))` — when processing "A/42/427, p. 24.", cur.lines = ["A/79/270, paras. 84 and 85."] which ends with '.' → condition true → footnote 6 created with line "A/42/427, p. 24." ✓. 

But hmm — what if the first footnote's text is added via numSpace opener: "5 A/79/270, paras. 84 and 85." → cur.lines=["A/79/270, paras. 84 and 85."] ends with '.' → next continuation → footnote D ✓.

Edge: what if displaced page's first footnote text does NOT end with '.' on its first line but the plan says it does. OK.

Now — nextFootnote advancement on displaced page: seen includes 5, 6(D), 7... maxSeen covers. ✓.

Now — what about pages where the block's first opener is via jump (bare > nextFootnote)? seen includes it; nextFootnote advances past. ✓.

Now — CHK.06 search strings: for footnote 5 (bare opener), search = "5 A/79/270, paras. 84 and 85." (40 chars) — searched in paragraph text_raw — 0 hits expected ✓.

Hmm wait — one potential false positive: footnote search strings like "1 A/..." — could a paragraph contain "1 A/..."? Unlikely. OK.

Now — the marks: 141 marks expected. The sequential rule: counter starts at 1, walks paragraphs in order. Paragraph 1 text: "A clean, healthy and sustainable environment is an essential precondition for the enjoyment of economic, social and cultural rights. Nature is indispensable..." — any digit runs? "article 11"? Not in para 1. The first mark might be in para 2 or wherever. If a paragraph contains "2025" — 4 digits → run length 4 > 3 → not candidate ✓. "art. 6" — run "6", before char '.', after maybe space → candidate; if counter==6 at that point → wrongly marked! Hmm. E.g., heading "Right to work (art. 6)" — headings aren't scanned (only paragraphs). But paragraph text mentioning "article 6" when counter==6 → false mark. The plan says the sequential rule works on this data (141 marks found, check passes). Trust.

Hmm — wait, actually there's a subtlety: "not touching ... an opening parenthesis" — "(art. 6)" — the "6" is followed by ")" — allowed. Preceded by space. So candidate. If counter==6 → marked. The plan's check lists rejected numbers so reader sees "article 11" not bracketed — implying in this data real numbers never coincide with the counter. OK.

Now — one more: the mark regex /\d+/g on text_raw — but text_raw includes things like "E/2003/22" — runs "2003" (4 digits, skip), "22" — before char '/', excluded ✓. "paras. 84 and 85" in footnotes — not scanned. "HRI/GEN/2/Rev.6" — "2" before '/', excluded; "6" after '.', before... "Rev.6" — run "6", before '.', after end/space → candidate! If counter==6 → marked. Hmm — "Rev.6" appears in paragraph 54's text ("HRI/GEN/2/Rev.6 , chap. I"). If the counter is at 6 when paragraph 54 is processed... The plan says the rule works (141 marks, no gaps). The check will reveal. Trust the plan — it explicitly says only the sequential rule is used and the check lists rejected numbers.

Hmm, wait — actually, let me reconsider: maybe "not touching ... a dash" also covers "Rev.6"? No, '.' isn't excluded. OK trust.

Now — one more design point: "the app counts such lines anyway and reports the number" (hyphen-ending lines) — I count hyphenLines and report in method ✓.

Now — the header "n pages of raw converter text" — records.length ✓. And `count` field is string "20" — I use records.length.

Now — title: data.title. For pdf_text: "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development" presumably. ✓.

Now — let me also double-check the "Section" column shows "—" when empty. ✓.

Now — writing the final file. Also need `<meta name="viewport">`. Title tag: "Paragraphs out of a PDF — {symbol}".

Let me also handle: if docKeys is empty (no data) — show a message. Guard: if(!docs.length){ document.body.innerHTML = '<p>No document with records and a reference found in WORKSHOP_DATA.</p>'; return; }

Also — the plan says "Today there is one" — with generic scan, if pdf_text_2 present, two cards. Fine.

One more: the rail heading "DOCUMENT" — mono. ✓.

Let me also add "How this is computed" near rail numbers? The rail card has bars; add small note "found by this page's code; bar shows the share of the reference count". I'll add a tiny hint.

Now — CSS for `.sect` buttons (collapsible headings): 
```css
.sect{appearance:none;background:none;border:none;border-top:1px solid var(--rule);width:100%;text-align:left;padding:12px 2px;cursor:pointer;font-family:ui-monospace,...;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);display:flex;justify-content:space-between}
.sect::after{content:'+'}
.sect[aria-expanded="true"]::after{content:'–'}
```

Check panel styling, tiles, etc.

Also `.note` small text; `code` styling mono.

Let me now also think about the tab panels' top: maybe a one-line question per tab? The plan: "one question each". Tab 01: "Did the app find everything the document has?" — I'll add as a serif subtitle in each panel:
- 01: "Did the app find everything the document has?"
- 02: "What does each paragraph say, and how do I cite it?"
- 03: "What do the footnotes say?"
- 04: "Can I trust this, and can I take it away?"

Add `<h2 class="serif q">…</h2>` at top of each panel.

Now — assemble everything. Also ensure no external resources. Chart.js not needed (no charts required — bars are CSS). That's fine ("Use it for charts" — only if charts; we have none, just bars).

Let me write the complete file now. I'll be careful with quotes inside template strings — I'll use string concatenation with single quotes and escape properly. Using template literals would be easier but I must be careful with backticks inside — none. I'll use template literals for readability. Actually mixing — I'll use template literals throughout the JS. Careful: `${}` inside strings intended literally — avoid.

Also `esc()` for all data-derived text inserted into HTML.

One more detail — the plan says tab 02 note: "a note under the table says so and gives the pattern \[\d+\] for removing them with find-and-replace" ✓ included.

Also "Rows are buttons with aria-expanded; clicking or pressing Enter expands the row in place, under it." ✓.

Also — "the expanded paragraph shows the full path ('IV. … › Right to work (art. 6)')" ✓ path div.

Also — "Under the text: the reference's first six words next to the extracted first six words, marked equal or different; the page(s); the repairs that touched this paragraph; and a Copy citation button" ✓.

Now — the CSV `text` column: marked text (with [n]) ✓; `text_raw` unmodified ✓.

Let me also double check downloadCSV filename for footnotes: symbol.replace(/\//g,'-')+'-footnotes.csv' ✓.

Now — write it. Also remember: before the code block, at most three short sentences saying what I built. After the code block: nothing.

Let me now write out the entire HTML file carefully.

Also — one more consideration on `activateTab` and panels: panels are `<section role="tabpanel" tabindex="0"?>` — add tabindex="0" so panel is focusable? Not required. Keep simple.

Potential pitfall: `e.target.closest` — e.target may be a text node? In click events target is an element. OK. But if e.target is document? Guard with `e.target.closest ? ... : null` — I'll guard.

Let me also handle the case where `aria-controls` id contains characters — ids like "d-12", "rl-12" fine.

Now — writing rawPageHtml: `R.records.find` — records sorted ✓.

Also — lineCls keyed by page number (could be number type) — object keys become strings; access with page (number) → JS converts ✓.

Now — the `classCounts` for paragraph lines: I count in a forEach over bodyLines after parse. But header/footer/footnote counted during page loop. Cover/heading counted in forEach. Let me make sure I don't double count: in the body loop I set L.cls but don't increment; after loop, forEach increments by cls. ✓. But note: lines with cls null (shouldn't happen) → unclassified.

Wait — there's one case: body lines when state==='cover' get cls='cover' ✓; when cur exists → 'paragraph' ✓; heading mode → 'heading' ✓; unlabelled → 'heading' ✓. All body lines get cls. ✓.

Now — CHK.09 sum: classCounts sums = header+footer+footnote+cover+heading+paragraph = all non-empty lines ✓ if no unclassified.

Now — let me also compute maxWords for CHK.06.

Also — the plan wants CHK.06 to also list paragraphs over 300 words — included.

Now — writing everything out. Let me also think about initial tab: 01 RESULT ✓.

Let me write the code now in final form.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF · UN document</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b4f;--soft:#6f6759}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.13em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:var(--red)}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;background:#ece6d8;padding:1px 4px}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}
header.top{padding:26px 34px 14px;border-bottom:1px solid var(--rule)}
.kicker{color:var(--soft);margin-bottom:6px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px;font-weight:400;max-width:60ch}
.meta{margin:0 0 6px;color:var(--soft);font-size:14px}
.what{margin:0;max-width:75ch}
.pillwrap{position:absolute?}
```

Hmm — header layout: I want the pill at the right. Use flex: header.top{display:flex;...} with a left div and pill. Let me structure:

```html
<header class="top">
  <div class="hleft" id="hd"></div>
  <div class="hright" id="pill"></div>
</header>
```

header.top{display:flex;justify-content:space-between;gap:24px;align-items:flex-start;flex-wrap:wrap}

Pill:
```css
.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--rule);border-radius:999px;padding:7px 14px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;margin-top:6px}
.dot{width:9px;height:9px;border-radius:50%;background:var(--green);display:inline-block}
.dot.red{background:var(--red)}
.dot.inline{margin-left:6px;vertical-align:middle}
```

Layout:
```css
.layout{display:flex;align-items:flex-start}
.rail{flex:0 0 270px;width:270px;border-right:1px solid var(--rule);padding:18px 18px 40px;position:sticky;top:0;max-height:100vh;overflow:auto}
main{flex:1;min-width:0;padding:16px 32px 70px}
.railhead{color:var(--soft);border-bottom:1px solid var(--rule);padding-bottom:8px;margin:0 0 14px}
.doccard{border:1px solid var(--rule);border-left:3px solid transparent;background:#f8f4ea;padding:12px 14px;margin-bottom:14px;cursor:pointer}
.doccard.sel{border-left-color:var(--red)}
.doccard .sym{margin-bottom:4px}
.doccard .sym a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}
.ctitle{font-family:Georgia,serif;font-size:15px;line-height:1.35;margin-bottom:4px}
.cmeta{color:var(--soft);font-size:13px;margin-bottom:10px}
.bignum{font-family:Georgia,serif;font-size:42px;line-height:1;margin-top:8px}
.blabel{font-size:13px;color:var(--soft);margin-bottom:2px}
.bar{height:4px;background:var(--rule);margin:3px 0 6px}
.bar i{display:block;height:100%;background:var(--green)}
.bar i.red{background:var(--red)}
.clink{margin-top:8px;font-size:13px}
```

Tabs:
```css
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);margin-bottom:16px;flex-wrap:wrap}
.tabs [role=tab]{appearance:none;background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:10px 12px 8px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;letter-spacing:.13em;color:var(--soft)}
.tabs [role=tab]:hover{color:var(--ink)}
.tabs [role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
```

Panels:
```css
.q{font-size:22px;font-weight:400;margin:4px 0 14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:0 28px;margin:0 0 20px}
.tile{border-top:1px solid var(--ink);padding:12px 2px 18px}
.fig{color:var(--soft);margin-bottom:8px}
.bignum{font-family:Georgia,serif;font-size:54px;line-height:1}
.tlabel{font-size:14px;margin:2px 0 6px}
.tcmp{font-size:14px;margin-bottom:6px}
.how{font-size:12.5px;color:var(--soft);border-top:1px solid var(--rule);padding-top:6px;margin-top:8px}
.ok{color:var(--green)} .bad{color:var(--red)} .noref{color:var(--soft)}
.note{font-size:13.5px;color:var(--soft);max-width:90ch}
```

Tables:
```css
table{width:100%;border-collapse:collapse;margin:8px 0 20px}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:19px;padding:8px 0 8px}
caption .mono{color:var(--soft);margin-right:12px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:400;color:var(--soft);text-align:left;border-bottom:1px solid var(--ink);padding:6px 8px}
td{border-bottom:1px solid var(--rule);padding:7px 8px;vertical-align:top;font-size:14.5px}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.prow{cursor:pointer}
tr.prow:hover td{background:#ede7d8}
.rowbtn{appearance:none;background:none;border:none;padding:0 2px;cursor:pointer;color:var(--red);font-family:Georgia,serif;font-size:16px;font-weight:700}
td.sec{max-width:180px;color