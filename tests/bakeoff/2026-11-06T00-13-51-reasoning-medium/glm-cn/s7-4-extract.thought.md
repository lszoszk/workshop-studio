Build the full app per plan. Single HTML file, ~keep manageable. Let me write it carefully.

Key pipeline: parse records, classify lines, build paragraphs, headings, checks, tabs, exports, etc.

Let me write the code.

Plan structure:
- Header
- Tabs: 01 RESULT, 02 PARAGRAPHS
- Left rail
- Tab panels
- Footer

Extraction algorithm details:
- For each page (sorted by page): lines = text.split('\n')
- Header: first non-empty line equals symbol → drop, else warning.
- Footer: from end, drop lines while empty, starts "GE.", only 6-digit groups (/^(\d{6})( \d{6})*$/), or bare number 1-3 digits. If bare number == page → page number; else count as displaced footnote number.
- Remaining body lines tagged with page. Blank lines: drop (but keep for concatenation? blank lines dropped; headings detection uses "non-empty line immediately followed by paragraph start" — so skip blanks when finding that adjacency).

Then concatenate body lines (with page tags) across pages. Now classify:
- labelled heading: /^[IVX]+\.$/ or /^[A-Z]\.$/. Then skip blank lines (already dropped), collect heading text lines until next label or paragraph start. "a line starting with a lowercase letter or "(" continues the previous heading line" — hmm, heading can wrap; all lines up to next label/paragraph start are heading text anyway. So heading text = lines until next label or paragraph-start line. That includes continuation.
- paragraph start: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.
- unlabelled heading: non-empty line immediately followed by paragraph-start line (in concatenated non-blank sequence), ≤90 chars, starts with capital letter, not ending with . ; : , digit. Two-line heading: when the line before it passes the same test and does not end a paragraph sentence... Let's implement: when we find an unlabelled heading candidate at index i (followed by paragraph start at i+1), check line i-1: if it passes the unlabelled-heading test (capital start, ≤90, not ending with .;:,digit) and doesn't end a paragraph sentence (i.e., doesn't end with . ! ? " etc.) then it's part of the heading. But careful: only when line i-1 is also a candidate. I'll implement: look back one line; if it matches the heading-line test (capital, ≤90 chars, not ending in .;:,digit) and previous paragraph's last line — well "does not end a paragraph sentence" means the line before doesn't end with a sentence-ending punctuation. That's the same test basically. So: if previous line passes heading-line test, join it as heading start (two-line heading). But that could grab a real paragraph line... the test says "does not end a paragraph sentence" — ending without full stop. Since paragraph lines mid-paragraph are fragments that could pass. Risk accepted per plan. Actually plan: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading." Same test includes not ending with full stop etc. So just: if prev line passes the test → two-line heading. But also the prev line must not itself be followed by... it's fine.

Edge: prev line might be another paragraph's text — but paragraph lines within a paragraph are fragments not ending with punctuation; if followed by an unlabelled heading candidate which is followed by a paragraph start, the heading candidate is between paragraph text and a new paragraph start. Hmm, the prev line is the last line of the previous paragraph — which typically ends with a full stop, so it fails the test. Good.

- Everything else non-empty → current paragraph lines (or cover if before first paragraph start).

Wait: but heading detection needs to happen during a single pass. Order: iterate lines; if line is label → start labelled heading collection; if paragraph start → close heading, start paragraph; else if in heading → heading text; else → could be unlabelled heading if next line is paragraph start; else paragraph text (or cover).

Careful: unlabelled heading check applies to any non-empty line not in a labelled heading. But heading candidate line itself must not be paragraph start (it isn't, since we checked). Also cover lines before first paragraph: "6 November 2025" — next line isn't paragraph start probably, so it goes to cover. Good. But unlabelled heading detection requires next line is paragraph start — cover lines before first paragraph start: the line before the first paragraph start could be a cover line like "Original: English"? It ends with... "English" no full stop, starts with capital, ≤90 → would be treated as unlabelled heading before paragraph 1. Hmm. That's a heading of the document title actually — acceptable? The plan says lines before the first paragraph start are the cover. So I should only apply unlabelled-heading detection after the first paragraph start has been seen. I'll do that: if no paragraph started yet, line is cover.

Suspect lines: within paragraph lines: bare number 1-3 digits no full stop, or starts with 1-3 digits + space + capital letter or UN symbol or quote mark... plan: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". Regex: /^\d{1,3} [A-Z“"]/ — capital letter, or starts with a quote. Or /^(\d{1,3}) (E\/|A\/|CCPR|CEDAW|...)/ — simpler: /^\d{1,3} (“|"|E\/|A\/|S\/)/. Or /^\* /. Also line before it. Implement:
- /^\d{1,3}$/ (no full stop)
- /^\d{1,3} [A-Z“"]/
- /^\* /
When a suspect line found, that line and every line after it to end of its page (same page) are suspect. Since lines have page tags, mark all subsequent lines with same page as suspect.

Flag paragraph if any suspect line or >300 words.

First words: strip footnote marks from first six words. Algorithm: take words = text.split(/\s+/). Process tokens: remove digits glued at end of word/punctuation: token.replace(/\d+([.,;:]*)$/... actually "waste.2" → "waste."; "word2" → "word". Then a token of digits alone dropped only when previous token ends with . , or closing quote and not abbreviation like "No." "art.". Simpler per plan. Then take first six, compare.

Normalisation for compare: curly quotes → straight, en/em dash → hyphen, whitespace runs → single space, case kept.

Hmm reference first_words values like "A clean, healthy and sustainable environment" — six words. Compare found six words joined by space vs reference string, after normalisation.

Wait, "No. 3" — token "No." ends with full stop but is an abbreviation; "3" must stay. Implement: drop digit-only token if prev ends with . or , or ”/"/’/' and prev is not in abbreviation set and doesn't match /^(No|art|para|vol|p)\.$/i etc. Keep simple list.

Actually footnote marks appear glued ("waste.2") — when do bare digit tokens appear? After space "”. 3". OK.

Checks list (m checks): paragraph count, numbering, first words, flagged paragraphs (informational), suspect lines, headers/footers, headings, nothing lost, export round trip. That's ~9 checks. Pass/fail: paragraph count pass if equal; numbering pass if 1..n in order; first words pass if 0 mismatches; flagged: not a failure — mark as "pass" style? Plan says the line reads "n paragraphs flagged on n pages, to check against the PDF" — count as pass? Header count "n of m checks pass": treat informational checks as pass when they ran. Suspect lines similar. Headers/footers: pass if all pages had symbol header? Expected all; page number all but first. Pass if matches expectation? Could fail on real data... say pass if all pages had symbol first line and pages 2..n had page number; else fail listing. Hmm risky but per data it holds. Actually the plan says "expected all" — I'll make it fail if not matching. Nothing lost: pass if unclassified = 0. Export round trip: pass if counts equal.

Classification counts: header, footer, cover, heading (label + text lines + unlabelled), paragraph. Every non-empty line classified exactly once. In my pipeline I drop header/footer first, then cover/heading/paragraph. Track counts. Note blank lines aren't counted (non-empty only). Footer stripping: I drop empty lines from end — those are blank, not counted. Good.

Tab 01: tiles, mismatch list, download buttons, closed headings: Every check, Flagged paragraphs table.

Tab 02: table of paragraphs, headings box closed, expandable rows, copy citation, PDF lines toggle.

Rail: big numbers.

Let me now write the HTML. Aim ~900 lines. Keep CSS minimal.

Data details: count is string "20" per plan; use records.length.

Exports: JSON array of records with fields. Markdown with front matter and headings in document order.

For markdown: headings as ## and ### in document order, paragraphs under them. Structure: iterate events in order (heading events with level, paragraph events). Labelled roman → "## ", lettered → "### ", unlabelled → "### "? Plan: "the headings as ## and ### lines in document order". I'll do roman = ##, lettered/unlabelled = ###.

Need heading events list with level. During parse, record headings in order: {level: 2 for roman, 3 for letter, 3 for unlabelled, text, index}. And paragraphs get section (nearest heading text) and part (nearest roman heading text).

Suspect lines in text_lines toggle: show lines with page markers where page changed.

Copy citation: navigator.clipboard with fallback textarea.

Arrow key tabs.

Let me write.

First words mismatch display: "para. n: found … / reference …" max 10.

Flagged paragraphs closed heading on tab 01: table Paragraph | Page | Suspect lines | Why. Why: reasons collected: "starts with a number and a space", "bare number", "asterisk line"?? Plan lists three why reasons: "starts with a number and a space", "bare number", "paragraph over 300 words". Suspect kinds: bare → "bare number"; number+space → "starts with a number and a space"; asterisk → hmm. I'll add "starts with an asterisk" for that. Also count suspect lines.

Clicking flagged row → open tab 02, expand that paragraph, highlight suspect lines (they are highlighted anyway).

Now the "first line" column: first 120 chars cut at word + "…".

Check panel: one line per check.

Let me write the code now.

Structure:

```html
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>...</title>
<style>...</style></head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<div class="layout">
  <aside>rail</aside>
  <main>
    <section id="panel-result" role="tabpanel">...</section>
    <section id="panel-paragraphs" role="tabpanel" hidden>...</section>
  </main>
</div>
<footer>...</footer>
<script>...</script>
</body></html>
```

CSS: paper/ink per studio rules.

JS: compute everything on load, render.

Parsing details for footer: 
```
let lines = rec.text.split('\n');
// header
let i0 = lines.findIndex(l=>l.trim()!=='');
if (lines[i0].trim()===symbol) {headerCount++; lines.splice(i0,1);} // remove header line only? blanks stay
```
Wait header is first non-empty line. Remove that line (mark as header). If not equal, warning.

Footer from end:
```
let end = lines.length;
while (end>0) {
  let l = lines[end-1].trim();
  if (l==='') {end--; continue;}
  if (/^GE\./.test(l)) {footerLines.push(...); end--; continue;}
  if (/^(\d{6})( \d{6})*$/.test(l)) {end--; continue;}
  if (/^\d{1,3}$/.test(l)) {
    if (Number(l)===rec.page) pageNumCount++; else bareFootnoteNums.push({page, num:l});
    end--; continue;
  }
  break;
}
bodyLines = lines.slice(0,end)
```
But careful: header removal — if I splice then footer scan on remaining. But blank line removal from end and "GE." lines etc are footer. What about paragraph text near foot? Footnotes are in body (suspect lines). Fine.

Edge: header removal — after removing the symbol line, count it classified once.

Then build body line array: for each page, bodyLines (non-blank? keep blanks? just push non-blank with page tag — blank dropped). But concatenation across page: previous page's last line and next page's first body line join into same paragraph. Since we join with space, fine.

But wait — heading detection "line immediately followed by paragraph-start line" — with blanks dropped, adjacency in the concatenated array. Good.

Also two-line unlabelled heading: heading candidate at index i, check i-1.

Classification counts: total non-empty lines across all pages = sum. headerCount + footerCount + body non-empty lines... body non-empty lines each classified as cover, heading, or paragraph line. Note: blank lines within body are dropped, not counted. Footer scan drops blank lines at the very end — they're blank, not counted. But what about blank lines in the middle? Fine.

Also count lines ending with hyphen (report number).

Parse pass over bodyLines (array of {text, page}):

```
let paras=[], headings=[], cover=[], state...
let currentHeading=null; // {text, level, part}
let curPara=null;
let romanText=null;
for (i=0..n-1):
  line = bodyLines[i]
  t = line.text
  if (/^([IVX]+|[A-Z])\.$/.test(t)) {
    // labelled heading: collect following lines until next label or para start
    let level = /^[IVX]+\.$/.test(t)?2:3;
    let textParts=[];
    let j=i+1;
    while (j<n && !isLabel(bodyLines[j].text) && !isParaStart(bodyLines[j].text)) { textParts.push(bodyLines[j].text); markHeading(j); j++; }
    heading = {level, text: textParts.join(' '), roman: level==2}
    headings.push(heading)
    if (level==2) romanText = heading.text
    currentHeading = heading
    i = j-1; continue;
  }
  if (isParaStart(t)) {
    m = t.match(/^(\d{1,3})\. ?(.*)$/)
    curPara = {num: +m[1], lines: [], pages:[]}
    if (m[2]) curPara.lines.push({text:m[2], page:line.page})
    paras.push(curPara); continue;
  }
  // unlabelled heading?
  if (curParaSeen && i+1<n && isParaStart(bodyLines[i+1].text) && headingTest(t)) {
    let start=i;
    if (i>0 && headingTest(bodyLines[i-1].text) && !isLabel(bodyLines[i-1].text) && bodyLines[i-1] classified as paragraph?? )
```
Hmm, two-line heading: line i-1 passes headingTest. But i-1 might be a labelled heading text line (e.g., heading text itself). If i-1 was already classified as heading, don't re-grab. Track classified array: cls[i] = 'heading'|'para'|'cover'. For two-line: only grab i-1 if cls[i-1]==='para' (part of previous paragraph, not ending a sentence) — wait if previous paragraph's last line doesn't end with a full stop... usually it does. If cls[i-1]==='heading' then it's a wrapped labelled heading already handled? No — labelled heading collection consumes lines until paragraph start, so a line right before a paragraph start that's part of labelled heading text already consumed. So for unlabelled two-line case, i-1 is paragraph line or cover. Only grab when cls[i-1]==='para' and passes test. Actually plan: "when the line before it passes the same test and does not end a paragraph sentence". headingTest includes "not ending with full stop..." so "does not end a paragraph sentence" is covered. So: if i>0 && cls[i-1]==='para' && headingTest(prev) → heading spans both; unclassify prev line from its paragraph (remove from paragraph's lines). Need to remove it from the previous paragraph's lines array — since lines are pushed as objects, I can filter at end or track. Simpler: paragraphs store line indices? Store lines with index; when converting to heading, remove from prev para.

Hmm but a paragraph's last line not ending with a full stop is rare. Fine.

Then heading = {level:3, text: prevText + ' ' + t}, cls[i-1]='heading'.

  else if (!curPara) { cover; cls='cover' }
  else { curPara.lines.push(line); cls='para' }

headingTest(t): t.length<=90 && /^[A-Z“"(]/.test(t)? plan: "starting with a capital letter". Use /^[A-Z]/. && !/[.;:,,\d]$/.test(t). Not ending with full stop, semicolon, colon, comma or digit. Also non-empty. Also should not itself be a bare number etc. OK.

Also unlabelled heading only when a paragraph has started (curParaSeen). But what about heading between paragraphs where curPara exists — fine.

Wait also: unlabelled heading line itself gets cls='heading'.

Paragraph finalisation: for each para: page_start = lines[0].page, page_end = last.page; text = lines.map(text).join(' ') collapse double spaces, trim. text_lines field: lines joined " | ".

Suspect marking: for each para line index within para: if matches suspect patterns → suspect; and all following lines with same page → suspect. Compute reasons.

Word count > 300 → flag reason "paragraph over 300 words".

First words: compute per algorithm.

Now build export records, checks, render.

Check "Nothing lost": count non-empty lines total; sum classifications (header+footer+cover+heading+para); unclassified = lines where cls undefined among body lines. Should be 0.

Header/footer check: pagesWithSymbolHeader === totalPages? and pages 2+ with page number. Compute.

Numbering check: paras nums equal 1..n sequence. gaps/dups listed.

Export round trip: JSON.parse(JSON.stringify(exportRecs)).length === paras.length.

Rendering. Tabs with arrow keys. Rail numbers. Tiles. Buttons aria-expanded for collapsibles. Table tab 02: rows as buttons? "Rows are buttons with aria-expanded" — make first cell a button, or whole row clickable with role. I'll make an expand button in the first cell plus row click. Simpler: a <button> spanning the row content styled as row. I'll use <tr> with a button in first cell controlling expansion, and row click too. Actually simplest robust: each paragraph rendered as a div row (button) that toggles a detail div. Use div-based "table" with grid. But plan wants table semantics with caption, th scope. I'll use a real table; the first cell contains a button with aria-expanded; clicking row toggles; detail row (extra <tr>) contains full text. aria-expanded on button. That works.

Flagged row click on tab 01 → switch to tab 02, expand paragraph, scroll.

Copy citation: clipboard.

Show PDF lines toggle in expanded row.

Headings found box: closed details with list of headings.

Download JSON/Markdown: Blob URL.

Empty paragraph case: disable exports, message.

Missing reference: tiles show "no reference in this file", checks "not run".

Write it. Try to be complete but compact.

Header right: green dot "n of m checks pass" or red if failures.

Let me count checks m: 1 paragraph count, 2 numbering, 3 first words, 4 flagged (informational, counts as pass when ran), 5 suspect lines (informational), 6 headers/footers, 7 headings (informational, pass), 8 nothing lost, 9 export round trip. m=9.

Pass computation: 
1: found===expected (if no ref: not run)
2: sequence ok
3: mismatches===0 (not run without ref)
4: pass (informational)
5: pass
6: headers all + page numbers pages2+ → pass else fail
7: pass
8: unclassified===0
9: roundtrip ok

Checks that are "not run" don't count in m? "n of m checks pass" — if not run, exclude from m and show "not run". I'll count only run checks in m.

Now write the file.

For "suspect lines" numbers: total suspect lines, pages, paragraphs.

Flagged table "Suspect lines" column: the suspect line texts (maybe first, truncated).

Citation copy fallback.

OK, writing.

Also footer: source, built (WORKSHOP_DATA.pdf_text.built? plan mentions `built` in footer — dataset has {title, symbol, doc_url, source, count, records, reference}. built not listed... The description of pdf_text: `{title, symbol, doc_url, source, count, records, reference: {...}}`. No built. Footer shows source and built — I'll show source, and built if present else omit. Use `D.built || ''`.

Header line: symbol linked, "adopted reference.adopted", "n pages", source.

Now code. Estimate ~850 lines. Go.

For markdown export:
```
---
title: ...
symbol: ...
adopted: ...
source_url: doc_url
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: n
paragraphs_flagged: n
footnotes: "not separated; the document has n"
---

# title? then headings and paragraphs in order.
```
Build ordered events: keep array `order` of {type:'heading',h} / {type:'para',p} pushed during parse. Then generate: `## I. Introduction` (roman heading text with its numeral? heading text is "Introduction", numeral dropped. Plan says "the headings as ## and ### lines" — text only. I'll do "## Introduction"). Paragraph: `**12.** text (flagged: may contain footnote text)`.

JSON fields per plan.

Escaping markdown minimal.

Now write final answer: 2-3 sentences, then code block.

Let me write carefully.

First-words footnote-mark removal:
```
function cleanToken(tok){
  return tok.replace(/[’']?\d+([.,;:!?])?$/,'$1') // hmm
```
"waste.2" → "waste." : replace /\d+$/ after? Pattern: glued digits at end: tok.replace(/(\d+)([.,;:]*)$/,...) careful. Cases: "waste.2" (digits after punctuation), "word2". Rule: "digits glued to the end of a word or a punctuation mark are cut". So: if /\D\d+$/ or /[.,;:]\d+$/. Replace trailing digits: tok = tok.replace(/\d+$/, '') — but "waste.2" → "waste." good; "word2"→"word". But a token that is digits alone handled separately. But careful "1990" alone (real number in text, e.g. "General comment No. 27 (2025)") — digits alone dropped only when prev ends with . , or closing quote and prev not abbreviation. "(2025)" has parens so fine. Tokens like "27" after "No." — prev "No." ends with '.' but is abbreviation → keep. Also "art." etc.

Then take first six tokens after cleaning; drop digit-only tokens per rule while collecting? The rule affects ordering. I'll process sequentially: cleaned = []; for tok of words: t = stripGlued(tok); if /^\d+$/.test(t): if prev (last kept, or original prev?) ends with . , ” " and prev not abbreviation → skip; else keep t. else keep t (or maybe stripped). Push. Stop at 6 kept. prev = last kept token.

Abbreviations: /^(no|art|para|vol|p|sec)\.$/i.

Compare: norm(s) = s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim().

Found six words vs reference first_words — reference strings may have exactly six words; join found with space.

Edge: reference value may be fewer than six words? take as-is.

OK. Also paragraphs 24 etc start with real numbers "article 2" — token "2" prev "article" doesn't end with . → kept. Good.

Now write.

Also "How this is computed" line near each tile/chart.

Table captions serif with TAB.01 numbering.

Let me draft the whole file mentally then write out.

I'll write it now in the answer. Keep code tight.

Tab 02 table columns: No. | Section | Page | First line | Check. Expanded row: full text with suspect lines marked (thin red box around the suspect line's contribution — since text is joined, I'll render per-line: render paragraph as lines joined with space but wrap suspect lines in <mark>-ish span). Detail shows: full path section, text with suspect marks, reference vs found first words, "Show the PDF's lines" toggle (button aria-expanded) revealing lines with "· p. N" markers, Copy citation button.

Render expanded: para detail row colspan=5.

Suspect rendering: build text by mapping lines: suspect lines wrapped in <span class="suspect">line</span>, joined with space.

Copy citation feedback.

Now the flagged table on tab 01 with click → open tab 02 row.

Alright, writing final code. I'll be careful with edit-free single delivery.

Approx sizes fine. Write.