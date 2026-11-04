Build the full app per the plan. This is a complex single HTML file. Let me write it carefully.

Pipeline as described. I need to implement:

1. Header/footer stripping per page, displaced footnote numbers.
2. Footnote block detection with nextFootnote counter.
3. Footnote text parsing inside block, with displaced-number repair.
4. Body lines concatenated.
5. Paragraph starts (two regex forms).
6. Headings: labelled (roman/capital letter + "."), unlabelled (line before paragraph start, ≤90 chars, capital start, not ending . ; : , digit).
7. Paragraph lines joined, pages.
8. Footnote marks sequential rule.
9. First words comparison.
10. Checks: paragraph count, numbering, first words, footnotes count/sequence, marks, footnotes-out-of-paragraphs, headers/footers, headings, nothing lost (classification coverage).
11. UI: header, rail with document cards (all docs in WORKSHOP_DATA with records & reference — currently pdf_text, maybe pdf_text_2 too! "every document in WORKSHOP_DATA with `records` and a `reference` gets its own card" — pdf_text_2 has both. So the rail shows two cards and the tabs show the selected document). So the app must support multiple documents. Good — pdf_text_2 also qualifies. I'll make cards for all keys with records & reference, in order of data.

Tabs: 01 Result, 02 Paragraphs, 03 Footnotes, 04 Checks & Method.

CSV download: quoted fields, BOM, CRLF, filename from symbol with slashes → hyphens. Also footnotes.csv on tab 03.

Copy citation button.

Raw pages viewer with line classification colours and line numbers, select page.

Repair log table.

Let me design the pipeline in detail.

```js
function process(doc) {
  const sym = doc.symbol;
  const pages = doc.records.slice().sort((a,b)=>a.page-b.page);
  const ref = doc.reference || {};
  const repairs = [];
  // per page: lines = text.split('\n')
  // classify lines
```

Classification: each non-empty line gets a class: header, footer, footnote, cover, heading, paragraph. I'll build per page:

- lines = page.text.split('\n')
- trim right? Keep as-is but check trimmed. I'll work with trimmed lines for logic but keep raw for display.
- Header: first non-empty line equals symbol → class header, repair log.
- Footer: from end, walk backwards over lines while: empty, starts with "GE.", only 6-digit groups (regex /^(\d{6}\s*)+$/), or bare number 1-3 digits (/^\d{1,3}$/). Bare number == page → page number; else displaced footnote number, class footer (kept aside).
- Footnote block: after removing header and footer, find block start: first line that (a) is bare number == nextFootnote, (b) starts with nextFootnote + " ", or (c) starts with "* " on page 1. Everything from there to end is footnotes. Advance nextFootnote past highest number seen in block and past displaced number. If no opener: take first bare number greater than nextFootnote that stands before footer — but footer already removed; "before the footer" — I should detect the footnote block before removing footer? Simpler: do footer removal first, then find first bare number > nextFootnote among remaining lines... Actually plan says "If no line on a page opens nextFootnote, take the first bare number greater than it that stands before the footer and log the jump". After footer stripped, footnotes are at the end. Hmm, but a bare number in body could be mistaken. Since footnotes sit at the foot, I'll search for the first bare-number line greater than nextFootnote in the stripped page, and only accept it if it's in the latter part... Keep simple: search among lines after the body — actually let me do the footnote block detection on footer-stripped lines: scan for opener; if none, scan for first line that is a bare number > nextFootnote and is in the last... I'll just accept first bare number greater than nextFootnote anywhere in the stripped page (log jump). Given the data it's fine.

Wait, careful: footnote block start must be "the first line that is a bare number equal to nextFootnote, or starts with that number and a space, or starts with '* '". But could a body line coincidentally start with "5 something"? Body paragraphs start with "5." (number + period). A body line starting "5 " is unlikely. Fine.

Also the opener line: on page 1, "* " opener — cover asterisk note. Block starts at "* " line on first page.

- Footnote text inside block: iterate lines. Opener = line starts with number+space, or bare number alone. Lines up to next opener joined with space. Displaced repair: on a page with displaced number D: the first footnote ends at its first line ending with "."; lines after it up to next numbered line are footnote D, marked repaired, page recorded. Also non-numbered lines after a footnote that's not the first... The plan: "On a page with a displaced number D, the first footnote (its bare number, a blank line, then its text) ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D". Only applies to the first footnote on that page. Other continuation lines after other footnotes — in real data footnotes are one or two lines; with opener-based parsing, continuation lines attach to previous footnote. For the displaced case: after first footnote's period-ending line, subsequent lines until next numbered line = footnote D.

Hmm but wait: the first footnote on such pages is "a bare number on its own line, a blank line, then the text" and its text is one line ending with a full stop. Then footnote D's text follows. Then possibly more numbered footnotes. Implementation: within block, if page has displaced D: process first: find opener (bare number), skip blank, then text lines until line ending with "." — that's footnote N. Then lines until next numbered-opener line → footnote D (repaired). Then continue normal parsing from that opener.

Simpler general algorithm covering both: parse block lines; maintain current footnote; but handle displaced: when page has displaced D and we've just closed the first footnote (it ended with "."), the next non-empty lines without a number become footnote D. Let me implement:

```
let i=0; let firstDone=false;
while(i<lines.length){
  if empty: i++, continue (blank lines dropped)
  line = lines[i]
  m = opener match (bare number or number+space)
  if m: start footnote with that number, text = rest
  else if displaced && !firstDone... 
```

Actually handle displaced specially: 

```
if (displaced) {
  // first footnote: bare number, blank, text lines until line ending '.'
  // find first non-empty line, must be bare number
  ...
}
```

I'll write it directly.

The asterisk footnote on page 1: starts with "* " → footnote number "*", not counted.

- nextFootnote advancing: after processing block, nextFootnote = max(highest number seen + 1, displaced+1). "past any displaced number for that page."

- Body lines: lines before block start (after header/footer removal), tagged with page. Plus if no block, all lines.

- Cover: lines before first paragraph start in concatenated body.

- Headings: labelled: /^([IVX]+|[A-Z])\.$/ opens; skip blanks; following lines up to next label or paragraph start are heading text; a line starting lowercase or "(" continues previous heading (join, log "heading title joined from two lines"); any other line is a further heading (multiple heading lines? e.g. heading with two lines not starting lowercase — plan says "any other line is a further heading" — keep both as heading lines). Hmm, and unlabelled heading detection needs the concatenation. Order of operations: first, paragraph starts; then unlabelled heading = non-empty body line immediately followed by paragraph-start line, ≤90 chars, starts with capital, not ending with . ; : , digit. But labelled heading processing also consumes lines. Let me do:

1. Concatenate all body lines with page tags → array L.
2. Mark paragraph-start lines (regexes).
3. Mark labelled-heading label lines.
4. Mark unlabelled headings: line i where L[i] non-empty, L[i+1] is paragraph start (or label line? plan says paragraph start), meets criteria. Also not already a labelled label or paragraph start itself.
5. Everything before first paragraph start = cover.
6. Heading text lines: for labelled headings, lines between label and next label/paragraph-start. For unlabelled, just the one line. But careful: a line following a label that's long and not lowercase-starting — "further heading". I'll classify lines between a label line and the next paragraph-start/label as heading lines (joining: if a heading line starts with lowercase or "(" and there's a previous heading line, join them with space, log "heading title joined").

Wait — the labelled heading structure: "I." alone, blank line, "Introduction". The "Introduction" line would also be followed by... "Introduction" is followed by paragraph start "1." So "Introduction" would qualify as unlabelled heading too. But it's consumed by the labelled rule. Order: process labelled headings first (consume their text lines), then unlabelled detection only among remaining non-classified lines. But the text line "Introduction" is followed by a paragraph start and meets unlabelled criteria — but it belongs to the labelled heading. So: after classifying labelled heading text lines, unlabelled detection only considers lines not already classified as heading/label. Actually the plan says "An unlabelled heading is a non-empty line immediately followed by a paragraph-start line" — I'll exclude lines already classified.

Hmm, but subtle: heading text lines after label could include a wrapped second line starting lowercase → joined. Non-lowercase second line → separate heading line. Fine.

Section for paragraph = most recent heading line text (the joined title, or for roman labels the joined "IV. …"). Plan: "Each paragraph's section is the most recent heading line before it and part the most recent roman-numbered heading". For labelled roman headings, section = roman + " " + title? E.g. "IV. …". The expanded shows full path "IV. … › Right to work (art. 6)". So I'll keep a heading stack: roman parts, letter subparts, unlabelled headings. Full path = roman › (letter ›) unlabelled. Simplest: section column shows the most recent heading of any kind (lettered/unlabelled, or roman if none closer); part = most recent roman. Full path: roman title, then if current lettered subsection exists its title, then unlabelled if present. I'll track: currentRoman (title), currentLetter, currentUnlabelled. section displayed = currentUnlabelled || currentLetter || currentRoman; full path = [currentRoman, currentLetter, currentUnlabelled].filter(Boolean).join(' › ').

For the roman heading title: label "IV." + its text lines joined → "IV. Specific human rights obligations"? Store as "IV. " + text. OK.

- Footnote marks sequential rule: walk each paragraph's text (document order) with counter starting 1. Candidates: runs of 1-3 digits not touching another digit, slash, dash, or opening parenthesis "(" — i.e., char before not digit/slash/dash/(/ and char after not digit/slash/dash. "not touching another digit, a slash, a dash or an opening parenthesis" — before: not preceded by digit, slash, dash, '('? Hmm "touching" means adjacent. So candidate: digits run, preceded char (if any) not in [0-9/-] and not '('? Wait, "not touching ... an opening parenthesis" — "(17" — mark after "(" should not count? Actually in text "”. 3" mark after space. "equity, 17" — comma before, fine. Article references like "(art. 6)" — the 6 preceded by space, followed by ")". Hmm, is "(art. 6)" a footnote mark? "6" touching closing paren is fine per rule (only opening paren mentioned). But sequential counter saves us: only numbers equal to counter count. Good. I'll exclude if preceded by digit, '/', '-', '(' or followed by digit, '/', '-'. Wait why exclude after '('? Because footnote numbers in PDFs appear like "word.2" — superscript follows word, not after "(". Real marks: "waste.2", "”. 3", "equity, 17". An opening parenthesis before suggests a parenthetical number "(see para. 5)". OK.

Mark becomes [n], counter++. Only when equal to counter.

- text_raw keeps unmodified text. text = with marks bracketed. First words computed with marks removed — from text_raw with candidates removed? "first six whitespace-separated words of the joined text, footnote marks removed first" — use text (bracketed) then remove \[\d+\]? If a mark is mid-word "waste.[2]" removing gives "waste." good. Compute from joined text with marks removed: I'll strip [n] patterns from text.

- Footnotes cited by paragraph: the marks in that paragraph → footnote numbers.

Checks:
1. Paragraph count: found vs ref.paragraphs.
2. Numbering: 1..n sequential.
3. First words: count mismatches.
4. Footnotes: numbered count (excluding "*") vs ref.footnotes; sequence 1..max no gap/dup; restored listed.
5. Footnote marks: marks found run 1..ref.footnotes; list missing; list rejected candidates (candidates not equal to counter)? "the numbers it rejected as not being marks (with context)" — I'll collect candidates that were considered but not taken (i.e., runs of digits that are not marks) with a snippet. That could be many ("article 11" etc.). List a few. Maybe cap at some display, but fine.
6. Footnotes out of paragraphs: search first 40 chars of each footnote opener line (number included) in raw text of each paragraph (before marks). 0 hits expected. Also paragraphs over 300 words listed. Hmm "every paragraph over 300 words is listed" — as a caution list. I'll list them in the check line.
7. Headers/footers: pages with symbol first line (expected all), pages with page number footer (expected all but first), displaced numbers listed.
8. Headings: counts labelled/unlabelled and list unlabelled.
9. Nothing lost: every non-empty line classified once; counts per kind sum to total non-empty; unclassified listed.

For classification coverage: each line ends up in exactly one class. Cover = body lines before first paragraph start. Heading lines. Paragraph lines. Footnote lines (including blank? no—non-empty). Header, footer. But footnote block blank lines are empty, ignored. Within footnote block, all non-empty lines are footnotes. Any line before block start not classified as heading/paragraph-start/cover... Everything before first paragraph start = cover; paragraph-start lines and other lines after = paragraph lines unless heading. So classification: for each body line: if before first para start → cover; else if label line → heading; if heading text → heading; if unlabelled heading → heading; else → paragraph. All covered. Good — "nothing lost" should pass trivially, but compute anyway.

Wait — what about the "heading text lines" of labelled headings that come before the first paragraph start? E.g. page 1: cover lines, then "I." label, "Introduction", then "1." paragraph. "I." and "Introduction" are before the first paragraph start! Plan says "Lines before the first paragraph start are the cover." Hmm — but then "I. Introduction" would be cover. But headings check counts them... The plan: "Lines before the first paragraph start are the cover." Taken literally, label "I." and "Introduction" (which precede "1.") are cover. But then the headings check "number of labelled headings" — I. would be missed. Hmm.

Actually maybe treat cover as lines before first paragraph start that aren't headings. The heading detection should run regardless. Let me define: cover = body lines before the first paragraph-start line AND not part of a heading. Heading rules apply anywhere. That preserves "I. Introduction" as a heading. I think that's the right reading; the check panel will show heading counts. I'll classify: label lines and their text → heading even before first paragraph start. Cover = the rest before first paragraph start.

Hmm, but unlabelled heading detection: "non-empty line immediately followed by a paragraph-start line" — could fire on the cover (e.g., a cover line followed by... no, cover lines are followed by cover lines until first paragraph start; the line immediately before "1." on page 1 is "Introduction" which is a labelled heading text). Could a cover line be immediately before the first paragraph start? E.g. "General comment No. 27..." then... Actually on page 1 the structure: title lines, "* Adopted...", then "I.", blank, "Introduction", "1." — hmm "* Adopted" is in the footnote block? No — the asterisked note is at the foot of page 1 (cover page), it's the first footnote ("* "). The footnote block starts at "* " on page 1. So cover includes title etc. Wait — but the footnote block on page 1: block starts at the first line that "starts with '* ' on the first page". The "* Adopted by the Committee..." line is near the bottom of page 1. Everything before it on page 1 is body → cover (except header/footer, and "I." / "Introduction" headings which precede para 1 — wait, does the Introduction section start on page 1? Sample shows page 1 has "I. Introduction 1. A clean, healthy..." yes). OK.

Unlabelled detection on cover: line before "1." is "Introduction" (heading text of labelled). Excluded since classified. Good.

Edge: "6 November 2025" on cover — starts with number+space — not a footnote because counter at 1 and block opener requires bare number equal to nextFootnote or starts with "1 " — "6 November 2025" starts with "6 " not "1 ". Good. But wait — my fallback "first bare number greater than nextFootnote" — "6 November 2025" is not a bare number (has text), fine. But could "6" bare... no.

Also date stamp "051125 061125" — 6-digit groups, footer. "GE.25-15926 (E)" — starts with GE., footer. Page number alone — footer.

Header check: "first non-empty line equals symbol". Page text first line is "E/C.12/GC/27\n\nUnited Nations..." yes.

Now let me also handle multiple documents: keys of WORKSHOP_DATA with .records and .reference. In sample: pdf_text, pdf_text_2. Also uhri has records but no reference — excluded. gc? no reference. So pdf_text and pdf_text_2. Build cards in "order of the data" — I'll iterate Object.keys(WORKSHOP_DATA) and pick those with records & reference. Selected state; tabs re-render for the selected doc. Process lazily and cache.

Header line "n of m checks pass": count checks with pass status; checks that are "not run" — count as? The header says "n of m checks pass" green dot, or red dot "n checks failed". Not-run checks... I'll treat "not run" as neither pass nor fail; header shows passes of total (including not-run as not passing? that'd show red). Hmm. If reference missing, tiles say "no reference". For simplicity: green if failed==0 (and show "n of m checks pass" where m = run checks... or total). I'll show "n of m checks pass" with n = passed, m = total checks; green dot when failed == 0, red "n checks failed" when failed>0. Not-run counts as not passed but not failed — edge case unlikely here since both docs have references. Fine.

UI structure:

- header: mono label, serif title, one line (symbol link, adopted, n pages, source), sentence, right side dot + status.
- main grid: rail (left) + tabs area.
- rail: "DOCUMENT" heading, cards, big numbers paragraphs/footnotes with bars, checks link.
- tabs: 01 RESULT · 02 PARAGRAPHS · 03 FOOTNOTES · 04 CHECKS & METHOD. role=tablist, arrow keys.
- footer always visible.

Tab 01: four tiles with big numbers, "How this is computed" line each. Repairs tile links to repair log on tab 04 (switch tab + open log).

Tab 02: "Headings found: n" collapsible box, table of paragraphs: No | Section | Page | First line | Check. Rows expandable buttons showing full text, "Show the PDF's lines" toggle, reference vs found first words, pages, repairs touching, Copy citation. Note under table about [n] marks and regex.

Tab 03: footnotes table No | Page | Text | Repair; expanded shows full text (table shows truncated?). Also "the expanded paragraph also lists the footnotes it cites" (tab 02 expansions). Download footnotes.csv button.

Tab 04: check panel open; repair log (n) collapsible → table; raw pages collapsible → select + monospace panel with line classification colours, line numbers, legend; download paragraphs CSV.

CSV: BOM, CRLF, all fields double-quoted, inner quotes doubled. Columns as listed.

footnotes.csv: columns number, page, text, repaired, symbol? I'll do number,page,text,repaired.

Repair kinds: header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed. "footnote block removed" — when a page's footnote block is found, log one repair per page? The plan lists it as a kind. I'll log "footnote block removed" per page with a block (page, first footnote number). Also "paragraph joined across a page break" logged when paragraph's lines carry two page numbers.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Show "Copied" 2s.

Charts: none needed. Chart.js not required.

Design: off-white #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, pass green #1e6b3a. Serif Georgia for title/numbers; mono labels 11-12px; sans body 16px. Focus ring red. [hidden]{display:none!important}.

Category colours raw viewer: six pale tints with letter codes: C(over), H(eader), T? Let me use: cover #efe6d8, header #e3e0d0, heading #e8e0c8, paragraph #f4f0e8 (plain), footnote #e4e7ea, footer #e6dfd6... and margin letter codes: c,h,d(head? conflict). Use letters: v(cover)? Plan: "each doubled by a letter code". I'll use: cover=C, header=H, heading=D (like "division"?), paragraph=P, footnote=F, footer=B (bottom)? Better: cover K? Keep simple: C, H, S (section heading), P, N (footNote), B (footer bottom). Legend explains.

Now line count budget ~1500. Let's write compactly but completely.

Let me write the pipeline code.

```js
function processDoc(doc){
  const D = {repairs:[], warnings:[]};
  const sym = doc.symbol || '';
  const pages = (doc.records||[]).slice().sort((a,b)=>a.page-b.page).map(r=>({page:r.page, lines:String(r.text||'').split('\n')}));
  const ref = doc.reference || {};
  let nextFn = 1;
  const footnotes = []; // {number, page, text, repaired}
  const bodyLines = []; // {page, line, cls}
  const displacedAll = [];
  pages.forEach(pg=>{
    const lines = pg.lines.map(s=>s.replace(/\s+$/,'')); // rtrim keep leading?
```

Careful: I'll trim right only; blank detection via trim()===''.

Header: find first index with non-empty; if lines[i].trim()===sym → cls 'header', repair push {page, kind:'header line removed', what:'Header line removed', before: line, after:'—'}. else warning.

Footer: from end, j=lines.length-1; while j>=0: const t=lines[j].trim(); if t==='' → mark empty (just skip; these are trailing empties, but also blank lines inside footer region—only trailing). Approach: walk from end while line is empty → skip (no classification). Then while line matches footer patterns → classify footer. But blank lines between footer lines? Use: iterate from end; if empty → j--; else if matches footer pattern → classify, j--; else stop. But then blank lines before those footer lines remain unstripped (they're empty, not counted in non-empty classification anyway). OK.

Footer patterns:
- /^GE\./
- /^(\d{6}(\s+\d{6})*)$/ (date stamps, one or more 6-digit groups)
- /^\d{1,3}$/ bare number → if == pg.page, page number; else displaced.

Displaced: push to page.displaced.

Then find footnote block among lines between header and footer region. Let me construct working list: indices from headerEnd+1..footerStart-1 (where footerStart = first classified footer index; or lines.length). Actually blanks interleave. I'll find block start index: first index k in (headerIdx+1 .. footerStart-1) where line non-empty and (t===String(nextFn) || t.startsWith(nextFn+' ') || (pg.pageIsFirst && t.startsWith('* '))). Hmm "* " opener only on first page. Also nextFn could be >9, "10 " etc.

Edge: t === String(nextFn) but also bare-number-in-body? Body paragraphs are "12." not "12". Fine.

If no opener found: fallback: first non-empty line in working range that is a bare number > nextFn → block start there, log jump (repair kind... "footnote block removed" with note jump). 

If block found: blockLines = lines[k..footerStart-1] (non-empty ones are footnotes). Log repair 'footnote block removed' {page, what: `Footnote block removed from body (starts at footnote n)`, before: first line, after: '—'}.

Parse blockLines:

```
const bl = []; // {t, idx} non-empty block lines with original index
let disp = pg.displaced[0]; // at most one per page per data; handle list
```

Actually pg.displaced is an array (usually length ≤1). Handle first displaced.

Parsing with displaced repair:

```
let i=0; let firstClosed=false;
const items=[]; // {number:null|str, lines:[]}
while(i<bl.length){
  const t=bl[i];
  const m = t.match(/^(\d{1,3})\s+(.*)$/);
  const bare = t.match(/^(\d{1,3})$/);
  const star = t.match(/^\*\s+(.*)$/);
  if(star && !items.length){ items.push({number:'*', lines:[star[1]]}); i++; }
  else if(bare && (disp===null || items.length>0 || true...)) 
```

Hmm. The structure with displaced: first footnote is bare number alone, blank, then text lines. Without displaced: "first on a page is a bare number on its own line, a blank line, then the text; the others are '7 E/2003/22…'". So bare numbers open footnotes generally. 

Displaced logic: "On a page with a displaced number D, the first footnote ... ends at its first line that ends with a full stop; the lines after it, up to the next numbered line, are footnote D."

Algorithm:
```
let j=0;
// find first opener
while(j<bl.length){
  t=bl[j].t;
  if(/^\*/.test(t) && pg.isFirst){ open '*'; }
  else if(bare or num+space){ open that number; }
  else break?? 
}
```
Simpler: sequential scan:

```
let cur=null; let firstOnPage=true;
for(j...){
  t=bl[j];
  let openNum=null, rest=null;
  if(pg.isFirst && t.startsWith('* ')) {openNum='*'; rest=t.slice(2);}
  else { let m=t.match(/^(\d{1,3})\s+(.+)$/); if(m && ...){openNum=m[1];rest=m[2];}
         else if(/^\d{1,3}$/.test(t)){openNum=t;rest='';} }
  if(openNum!==null && !(openNum==='*' && cur)){ 
     // new footnote
     // but for displaced page, first footnote's text ends at line ending '.'
     ...
  }
}
```

With displaced: the first footnote (bare number, blank, text) — its text ends at first line ending with ".". Then following lines until next numbered opener are footnote D. But if I open footnotes on any number+space line, footnote D's text (no number) attaches to footnote 1. So special-case:

```
if(disp!=null){
  // parse specially
  let j=0; skip to first non-empty (should be bare number N)
  const first = {number: bl[j].t, lines:[]}; j++;
  while(j<bl.length && !endsWithPeriod(lastAddedLine...)) 
```
Plan: "ends at its first line that ends with a full stop" — accumulate lines; after adding a line that ends with '.', stop. Then lines after, until next numbered line → footnote D. Then continue normal.

```
if(disp){
  let j=0;
  const firstNum = bl[j].t; // bare
  const fl=[];
  j++;
  while(j<bl.length){
    fl.push(bl[j].t);
    if(/\.$/.test(bl[j].t)) { j++; break; }
    j++;
  }
  footnotes.push({number:firstNum,page,text:fl.join(' ')});
  // footnote D
  const dl=[];
  while(j<bl.length && !isOpener(bl[j].t)) { dl.push(bl[j].t); j++; }
  footnotes.push({number:String(disp),page,text:dl.join(' '),repaired:true});
  repair: 'footnote number restored'
  // rest normal
  parse rest from j;
} else { parse all normal; }
```

Normal parse:
```
let cur=null;
for each line:
  if opener (num+space or bare or '* ' on first page):
     cur={number,lines:[rest]}; footnotes.push(cur)
  else if cur: cur.lines.push(t)
  else: // continuation before any opener? shouldn't happen; treat as stray → classify as footnote anyway (unclassified-safe)
     cur={number:'?',lines:[t]}; footnotes.push(cur)
```

Wait: careful about "A line that starts with a number and a space opens a footnote, even when the number is not the one expected". Yes.

But hazard: footnote text continuation lines that start with a number? E.g. footnote text "2020, p. 5." on its own line — starts with "2020, " — number+space? "2020" is 4 digits; my regex limits 1-3 digits. "A/79/270" starts with 'A'. OK, 1-3 digit restriction helps. But e.g. "12 December 2024..." a continuation line starting "12 December"? Could falsely open. Plan says accept it ("never add a numbered line to the footnote before it"). Per plan, accept.

Then advance nextFn: highest numbered footnote on page +1, and past displaced.

```
const nums = footnotes on page with numeric number;
nextFn = Math.max(nextFn, max+1, disp? disp+1: 0);
```

Body: non-empty lines from headerEnd+1 to blockStart-1 (or footerStart if no block) → bodyLines with page.

Also lines within block that are blank — fine.

Then concatenate bodyLines (across pages) → array of {page, text}.

Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.

Labelled headings: line matching /^([IVX]+|[A-Z])\.$/. Then following non-blank lines up to next label/paragraph-start are heading text (with join rule).

Let me classify all body lines into: 'cover','label','headingtext','para','parastart'. Do it in one pass:

```
const L = bodyLines; // {page, text}
const cls = L.map(l=>'para'); // default
// paragraph starts
L.forEach((l,i)=>{ if(/^\d{1,3}\.$/.test(l.text)) cls[i]='pstart-num'; else {m=l.text.match(/^(\d{1,3})\. (.+)$/); if(m) cls[i]='pstart-inline';} });
// labels
L.forEach((l,i)=>{ if(/^([IVX]+|[A-Z])\.$/.test(l.text)) cls[i]='label'; });
// first paragraph start index
const firstP = L.findIndex((l,i)=>cls[i].startsWith('pstart'));
// label text lines: after a label, until next label/pstart
for(i...){ if(cls[i]==='label'){ let j=i+1; while(j<L.length && !cls[j].startsWith('pstart') && cls[j]!=='label'){ if(L[j].text.trim()!=='') cls[j]='headingtext'; j++; } i=j-1... } }
```
Careful: blank lines within (cls 'para' default but empty). Skip empties.

Hmm — "heading text up to the next label line or paragraph start" — but if a label is followed by paragraphs then later an unlabelled... whatever, fine.

Wait, issue: a label line "I." followed by blank, "Introduction" (headingtext), then "1." pstart. Good. But what if between label and its title there are other things... fine.

Unlabelled heading: line i where cls[i]==='para' (default, non-empty), L[i+1] exists and cls[i+1] startsWith 'pstart', text ≤90 chars, /^[A-Z]/, not /[.;:,0-9]$/. → cls[i]='uheading'. Also exclude if L[i+1] is... plan says followed by paragraph-start line. Also should the line before an inline pstart count? Yes ("on the line just before a paragraph number").

Hmm wait, also the unlabelled heading before "23." inline? Sure.

Cover: cls[i]='cover' for i<firstP where cls is 'para' (default) and non-empty.

Blank lines (empty text): drop entirely (not classified, not counted — "non-empty line" classification).

Heading join: for labelled heading text lines: if a headingtext line starts with lowercase or "(" and there is a previous headingtext line in same heading group → join. Log repair 'heading title joined from two lines'.

Paragraph assembly: iterate L in order; maintain current heading context:
- on 'label': if roman → currentRoman pending: collect following headingtext lines as its title; if letter (A.) → currentLetter pending.
- Actually collect heading titles: for each label, title = joined headingtext lines after it (until next label/pstart). Store heading objects {label, title, page}.
- unlabelled heading: {label:null, title:text}.

Maintain lastRoman (label roman + title, e.g. "IV. Specific obligations"), lastLetter, lastUnlabelled. On each heading: update accordingly. section for a paragraph = lastUnlabelled?.title || lastLetter || lastRoman(full) ... The table Section column shows nearest heading above: could be unlabelled ("Right to work (art. 6)"), lettered, or roman. full path = [lastRoman, lastLetter, lastUnlabelled].

Paragraphs:
```
let paras=[]; let cur=null;
for i in L:
  t=L[i].text; c=cls[i];
  if(c==='pstart-num'){ if(cur)paras.push(cur); cur={number:+m, lines:[], pages:new Set? } ; if(c inline) cur.lines.push(rest) and repair 'number and text split'; }
  else if(c==='para' && non-empty && cur){ cur.lines.push(t); cur.pages.push(L[i].page) }
  // headings/cover: if cur? headings between paragraphs shouldn't occur inside a paragraph; but if a heading appears while cur active... paragraphs end at next pstart. A heading after paragraph lines and before next pstart would be swallowed — but unlabelled heading detection prevents that. Labelled heading text after paragraph lines without a pstart following... unlikely. If heading encountered while cur, close cur? Safer: on any heading class, if cur has lines, keep cur open? Hmm. The doc structure: heading then paragraph. Between last paragraph of section X and heading of section Y there's no pstart in between... actually there is: paragraph numbering continuous. Headings come after a paragraph and before the next pstart. So when we hit a heading while cur is open, cur is complete (it will get no more lines until next pstart). Just leave cur; next pstart pushes it. But paragraph's section should be the heading AFTER it? No! Section = heading above the paragraph. Heading comes before its paragraph. A paragraph following a heading gets that section. Since we process in order, when we encounter pstart, current context already includes the preceding heading. But the PREVIOUS paragraph (before the heading) would also have been assigned... no — context updates as we walk; the previous paragraph was already pushed... wait, sections assigned when paragraph is pushed (at next pstart or end). The previous paragraph would get the new heading's section if assigned at push time after the heading. Fix: assign section at push time = context at the paragraph's LAST line, i.e., capture section when the paragraph is closed by a new pstart — but the heading appears between the last line and the pstart. Hmm.

Solution: capture section snapshot when paragraph's last line is added, or when a heading/label is encountered (close cur with current context). I'll capture section when pushing cur: but push happens at pstart which follows the heading. Instead: when we encounter a heading (label/uheading/headingtext) and cur is open, finalize cur's section from context BEFORE updating. Simpler: store on cur a `sectionCtx` updated on each line push; finalize at push. But heading lines between last para line and next pstart would update context after cur's last line — so capture context at each line push (cur.ctx = currentContext at push time... but the last line push happens before the heading, good).

Even simpler: when encountering heading while cur open → cur.done=true (no more lines will be added? not guaranteed but ok) and freeze cur.ctx. I'll do: on heading encounter, if cur && cur.lines.length, freeze. And at pstart, pushed paragraphs keep their frozen or line-time ctx. Let me just set cur.ctx = snapshot at every line push (cheap).

page_start = first line's page; page_end = last line's page. If differ → repair 'paragraph joined across a page break' for that paragraph (logged once).

Text = lines joined ' ', collapse double spaces, trim. text_raw = same (before mark bracketing). Hmm—text and text_raw: text_raw = joined text unmodified; text = with marks bracketed. First line in table = first 120 chars of text (marks bracketed? plan says marks shown in brackets in the table) — yes, use text.

text_lines: original lines for toggle/CSV ("lines separated by ' | '" for CSV column... plan lists CSV column `text_raw` and mentions "`text_lines` keeps the original lines ... and the CSV column `text_lines` (lines separated by ' | ')". But CSV column list has text_raw not text_lines. I'll include text_raw as joined raw, and also add text_lines column? The column list: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, footnotes_cited, repairs, citation, symbol, doc_url. I'll follow that exactly; the "Show PDF's lines" toggle uses stored lines. Fine—skip text_lines in CSV (the list is authoritative; the mention is contradictory). Actually I could include both; safer to follow the explicit column list.

Footnote marks: after all paragraphs built, walk in document order with counter=1, on each paragraph's raw text find candidates via regex: /(?<![\d\/\-\(])(\d{1,3})(?![\d\/\-])/g. JS supports lookbehind in modern browsers; safe? Sandboxed browser probably Chromium — fine. To be safe I'll implement without lookbehind: scan matches of /\d{1,3}/ and check neighbors manually.

```
function bracketMarks(raw, counterObj){
  let out=''; let i=0;
  while(i<raw.length){
    const m=/\d{1,3}/.exec(raw.slice(i)) — messy; do char scan:
```
Simpler: iterate with regex over full string collecting candidates with index:
```
const re=/\d{1,3}/g; let m; let res=''; let last=0;
while((m=re.exec(raw))){
  const s=m.index, e=m.index+m[0].length;
  const prev=raw[s-1]||'', next=raw[e]||'';
  if(/[\d\/\-\(]/.test(prev)||/[\d\/\-]/.test(next)) continue;
  const n=+m[0];
  if(n===counterObj.n){ res+=raw.slice(last,s)+m[0] wrapped... }
```
We want "waste.[2]" — insert brackets around: `raw.slice(last,s)+'['+m[0]+']'`. counterObj.n++. Also record mark number and rejected candidates (n!==counter with context snippet raw.slice(max(0,s-15), e+10)).

Note "not touching ... an opening parenthesis": prev==='(' excludes. Also what about next==='('? "(17" — opening paren after? Mark "word.(17"? unlikely; rule only mentions opening paren in touching—I'll exclude prev '(' only, and next not in digit/slash/dash. Hmm "not touching another digit, a slash, a dash or an opening parenthesis" — applies to both sides presumably. "(17" means the number touches '(' on left → excluded. "17(" touches '(' on right → I'll exclude too for symmetry. Fine: if prev in [\d/-(] or next in [\d/-(] → skip.

First words: from text with marks removed: text.replace(/\[\d{1,3}\]/g,'') then split whitespace, first 6, join ' '.

Normalise: curly quotes→straight, en/em dash→'-', whitespace runs→' ', trim.

Checks computation as described.

Footnotes cited by paragraph = its marks list.

Now "Footnotes stay out of the paragraphs" check: for each footnote, probe = first 40 chars of its opening line (number included; for restored, its first line). For a footnote parsed as "7 E/2003/22…", opener line is the original line "7 E/2003/22…". For restored footnote, first line of its text. Search probe in each paragraph's raw text (I'll search in raw joined text of paragraphs, before marks). Normalize both? Keep simple: search in raw text. Count hits. Also list paragraphs >300 words.

Headings check: counts of labelled (roman+letter) and unlabelled; list unlabelled titles.

Headers/footers check: pages where first non-empty line === symbol (expect all); pages with page-number footer (expect all but first); displaced numbers with page.

Nothing lost: total non-empty lines in file = sum over pages of lines with trim()!==''; classified = header+footer+footnote(block non-empty)+body classified (cover, label, headingtext, uheading, pstart, para). Compare. Unclassified: any body line whose cls is default 'para' but... all default become something. Wait — body lines classified 'para' but appearing BEFORE firstP become 'cover'; after firstP stay 'para' → belong to cur... but if cur is null (no paragraph open) and a 'para' line appears after firstP without an open paragraph — orphan! That's unclassified. E.g. stray line between heading and next pstart not caught as headingtext/uheading. Let me mark orphans: cls stays 'para' but cur==null at that point → track. I'll compute orphan lines (non-empty body line after firstP with no open paragraph and not heading/cover) and list them in check. Classify them as... they'd be "unclassified" shown red in raw viewer. For raw viewer classification, compute per-line class including 'orphan' → show red? The check lists unclassified lines with page in red. I'll classify orphans as their own and mark check fail if any.

Hmm wait: headingtext between label and pstart — my label-text loop assigns headingtext. Uheading detection catches line before pstart. What about headingtext lines that... ok.

But wait, there's an issue with the label-text loop and blank lines / multiple headings: "any other line is a further heading" — all non-empty lines after label until next label/pstart are headingtext. That could swallow a lot if a label appears with no pstart soon. Fine for this data.

Another subtlety: the unlabelled-heading rule requires "immediately followed by a paragraph-start line" — what about immediately followed by a label line? E.g. unlabelled heading then "A." subsection then paragraph. Not needed here.

Also: the line before a pstart could be a headingtext already (e.g. "Introduction" before "1.") — skip those (already heading).

Repair log entries: page, target (para/footnote/—), what, before, after. Keep before/after short (first ~60 chars).

Kinds & counts per kind displayed above the log table.

UI rendering: build with template strings, event delegation.

Tabs: buttons role=tab, aria-selected, panels hidden. Arrow-key nav.

Rail cards: for each doc key. Click selects → re-render everything (process cache).

Raw pages: select page, render lines with line numbers, class colour + margin letter, legend. Line class per page: need mapping from global line index → per-page. I'll store during processing: for each page, an array lineCls[] aligned to raw lines (before trimming? raw split lines). For header/footer/footnote lines I know indices. For body lines, map body line index → page & occurrence. Simplest: when building bodyLines, store {page, text, rawIndex} where rawIndex = index within page's lines array. Then per page build cls array.

Let me store per page: pg.lineCls = array length lines.length, values: '' (empty), 'cover','header','footer','footnote', or 'body' placeholder → later replaced by cover/heading/pstart/para via rawIndex. For footnote block region: all non-empty lines in block → 'footnote'. Blank lines in block: ''. But header detection: first non-empty index → header. Footer indices → 'footer'. Displaced number line is within footer walk → 'footer' (plan colors footer). OK.

Then after body classification, assign per rawIndex.

Check counts: non-empty total vs classified count (all non-empty should have non-empty class except orphans — orphans get 'para'? I'll give orphan class 'orphan' and count separately; check fails if orphan>0).

Actually orphan handling: to keep "nothing lost" honest, orphan lines are classified as... they're non-empty lines not part of any paragraph. I'll count them as their own category and fail the check. In raw viewer color red.

Now sizes: tab 02 table with ~90 rows, expansions. Fine.

Copy citation: use a temporary textarea + execCommand fallback.

Let me also handle `built` in footer: doc.built? WORKSHOP_DATA.pdf_text has `built`? Description: `{title, symbol, doc_url, source, count, records, reference}` — no built mentioned for pdf_text. Footer: "Source line, `built` date". Use doc.built || doc.source? I'll show source; built if present.

Header top line: "UN DOCUMENT · PDF TEXT" label; title; line: symbol → doc_url, "adopted reference.adopted", "n pages of raw converter text", source.

OK. Also tab 01 tiles: Paragraphs found n next to "The document has: reference.paragraphs" (green when equal, red with difference); Footnotes found n of ref; First words match n of ref.paragraphs; Repairs n link.

If no reference: tiles say "no reference in this file".

Let me now write the code. Aim ~1000-1200 lines. Careful with escaping in template strings (backticks inside HTML? avoid).

Charts: none. Fine, Chart.js not needed.

Let me write it.

CSS: base styles, rail, tabs, tables, tiles, checks, raw viewer tints, chips none needed. Focus visible.

HTML skeleton:

```html
<body>
<header id="appheader">...</header>
<div class="layout">
  <aside id="rail"></aside>
  <main>
    <div class="tabbar" role="tablist"></div>
    <section id="panel-result" role="tabpanel"></section>
    ... four panels
  </main>
</div>
<footer id="appfooter"></footer>
```

I'll render panels via JS functions per selected doc.

State: {docKey, results: {key: processed}}.

Render functions:
- renderHeader(doc, res)
- renderRail()
- renderTabs()
- renderResult, renderParagraphs, renderFootnotes, renderChecks.

Tab switching: show/hide panels, aria-selected, tabindex management.

Paragraph table: build rows as `<tr class="prow" data-i><td>num</td>...` and expansion row `<tr class="pexp" hidden>` containing details. Row click toggles. Make the first cell a button? Plan: "Rows are buttons with aria-expanded". I'll put a button in the first cell spanning? Simpler: the row itself gets role... I'll make the number cell contain a `<button class="rowbtn" aria-expanded>` and clicking anywhere on row toggles. Good enough for a11y.

Footnotes table similar with expansion? "The expanded paragraph also lists the footnotes it cites" refers to paragraph rows. Footnotes table: columns No | Page | Text | Repair. Text truncated with expansion for full text — plan doesn't explicitly require expansion for footnotes but full text should be available. I'll make rows expandable too (button in No cell), full text in expansion.

Headings box on tab 02: collapsible "Headings found: n" listing them.

Note under table about [n] marks + regex `\[\d+\]` — careful to render literally (escape backslashes in HTML: fine as text).

CSV builder:

```
function csv(rows, cols){ const esc=v=>'"'+String(v??'').replace(/"/g,'""')+'"'; return '\ufeff'+rows.map(r=>cols.map(c=>esc(r[c])).join(',')).join('\r\n'); }
```
Download via Blob URL, a.click().

Filename: symbol.replace(/\//g,'-') + '-paragraphs.csv'.

Now first words mismatch display: in expanded row show reference words vs found words, equal/different.

Repairs touching paragraph: repairs entries have target like 'para 12' or 'footnote 6' or page-level. For paragraph rows, filter repairs where repair.para===number. Page-level repairs (header/footer/footnote block) — "the repairs that touched this paragraph": I'll include page-level repairs of pages within [page_start, page_end]? That's noisy but per plan "the repairs that touched this paragraph". Hmm — footnote block removal on a page where paragraph spans... I'll include repairs whose page is in the paragraph's page range AND (para===number or kind is page-level). Let me tag repairs: {page, target ('para 12'/'footnote 6'/'page'), kind, what, before, after}. For paragraph row, include repairs where r.para===num OR (r.page-level && page in range). Hmm, header removed on page 3 touched every paragraph on page 3? Loosely yes. I'll include page-level ones for pages in range — could list ~3-4 per paragraph. Acceptable. Actually to reduce noise, I'll only include: number-and-text split, joined-across-break (para-targeted), and page-level header/footer/footnote-block for pages in range. That's fine.

Check "footnote marks": marks found run 1..ref.footnotes; missing listed; rejected candidates listed with context. Rejected candidates: I collect all digit runs considered and not taken, with context. In a 90-paragraph doc there will be many (article numbers, years like "2025"... wait years are 4 digits, excluded by 1-3). "article 11", "(art. 6)" — 6 preceded by space... "art. 6" — 6 preceded by space, followed by ')' — allowed as candidate; not equal to counter → rejected. Many rejections expected (e.g. "article 14", "para 5"). List them capped? Plan says list with context so reader sees "article 11" wasn't bracketed. I'll list up to... all could be dozens. I'll show count and first ~15 in the check line area (maybe a small collapsible). Keep simple: show count, and list up to 20 with context inline; if more, "+ n more". Good.

Also check pass criteria: marks must run 1..ref.footnotes without gap. Since counter only increments on match and matches are exact sequence, marks are automatically 1..k contiguous; check k === ref.footnotes.

Checks list (each {name, status: 'pass'|'fail'|'not run', detail html}):

1. Paragraph count
2. Paragraph numbering (1..n in order, no gaps/dups)
3. First words (mismatches count, each listed)
4. Footnotes count & sequence
5. Footnote marks
6. Footnotes stay out of paragraphs (+ long paragraphs list)
7. Headers and footers
8. Headings
9. Nothing lost

Header status: failed = checks.filter(fail).length; passed = checks.filter(pass).length; total m. Green: "n of m checks pass". Red: "n checks failed" + red dot on tab 04 (add class).

If a check can't run (no ref fields) → 'not run'.

Now writing everything. Let me be careful with the regex for footer date: "051125 061125" → /^(\d{6})(\s+\d{6})*$/.

Header equal check: line.trim()===sym.

Page is "first": pages[0].

Cover: also classify lines on page 1 before block... yes via body pipeline.

One more: "Paragraph starts... Lines before the first paragraph start are the cover." plus headings before it. Implemented.

Also repair "heading separated" for unlabelled: log.

Also "heading title joined": when headingtext line starts lowercase or "(" and previous line in same heading was headingtext → join. Implement in title assembly: title parts; if part starts with lowercase or '(' and parts.length>0 → join with space (single repair log).

Also roman label heading text: label "I." then "Introduction". Titles: roman → part = label + ' ' + title. Letter → letter + ' ' + title.

Now the rail big numbers: paragraphs found with "of ref" and bar (share, red when short or over). Footnotes same. "n of m checks pass" linking to tab 04.

Alright — also multiple docs: pdf_text_2 (CCPR/C/GC/32, 65 paras, 128 footnotes) will be processed by same pipeline. Its footnotes... should work similarly. Its header line is "CCPR" (symbol is CCPR/C/GC/32, first line "CCPR"? Sample shows page 1 starting "CCPR\n\nUNITED..." — header check may warn on some pages. That's fine; checks show honestly. Actually its symbol line — the header may be "CCPR/C/GC/32" on later pages; page 1 shows "CCPR". The check will report pages where first line ≠ symbol. Honest. Good.

Date stamp regex etc. applies.

Also "* " opener only first page — GC32 cover may not have asterisk note; fallback fine.

Footnote opener "starts with that number and a space": for nextFn e.g. 5, line "5" bare. Note the first footnote of a page is "a bare number on its own line, a blank line, then the text". Blank lines dropped in block parse (I use non-empty list).

Wait, in displaced parse I skip blank between number and text — I take bl (non-empty). firstNum = bl[j] bare number. Then text lines until one ends with '.'.

But careful: what if the first footnote's text has multiple lines and only later ends with '.'? "In all 12 cases the first footnote is one line ending with a full stop." The loop handles both.

Edge: displaced parse when first line isn't bare number (could be "5 A/79..." num+space)? Data says bare. I'll handle: if opener with rest non-empty... For robustness: if first line is bare number → as planned; else fall back to normal parse plus attempt displaced insertion? Keep to plan, with fallback: if bl[j] is num+space opener, treat rest as first line. I'll implement generic-ish.

Also the asterisk: only if items empty and line starts '*'. In displaced branch, skip: if first non-empty starts with '* ' → footnote '*', then continue to displaced logic. I'll handle: in block parse, pre-extract leading '* ' footnote if page is first.

Let me now also compute "Footnotes found" = numbered footnotes count (excluding '*').

Restored list: footnotes with repaired → listed with page.

Sequence check: numbers sorted === 1..n? Collect numeric numbers; check set size === max === count and equals sequence.

OK, writing the file now. I'll be economical.

Also tab 03 download footnotes.csv columns: number, page, text, repaired.

Also tab 04 raw pages: default select page 1; render on change.

Line numbers in raw viewer: index within page (1-based) — or actual raw line numbers. Yes 1-based per page.

Colours for classes:
- cover: #ece3d2, code C
- header: #e0ddca, code H
- heading: #e9e4cf, code S
- paragraph: #faf7f0, code P
- footnote: #e2e6e4, code N
- footer: #e5ded2, code B
- orphan: pale red #f3d6d6, code !

Legend lists these.

Every line shows margin letter code + line text (monospace, pre-wrap).

Now write. I'll aim for clarity and completeness. Also remember `[hidden]{display:none!important}`.

Tab keyboard: arrow left/right move focus & select.

One header detail: "One sentence under it says what the page does." Good.

Footer: "Counting, splitting and matching are done by this page's code; no model was called and nothing left the browser." plus source and built.

Let me write the JS carefully.

```js
const WD = window.WORKSHOP_DATA||{};
const DOCS = Object.keys(WD).filter(k=>WD[k]&&Array.isArray(WD[k].records)&&WD[k].reference).map(k=>({key:k,doc:WD[k]}));
```

Hmm — "every document in WORKSHOP_DATA with records and a reference" — pdf_text_2 also. uhri/gc/hrc lack reference. library has records but no reference... library records have passages; reference? no. wiki no records array? wiki has pages. OK: pdf_text, pdf_text_2.

processDoc returns res object with everything. Cache.

Let me draft processDoc fully:

```js
function processDoc(key){
  const doc = WD[key];
  const sym = doc.symbol||'';
  const ref = doc.reference||{};
  const repairs=[];
  const pages=(doc.records||[]).slice().sort((a,b)=>a.page-b.page).map(r=>({page:r.page, raw:String(r.text||'').split('\n')}));
  pages.forEach(p=>{ p.lines=p.raw.map(s=>s.replace(/\s+$/,'')); p.lineCls=p.raw.map(s=>s.trim()===''?'':'unclassified-placeholder'); });
```

Hmm simpler: p.cls = array of null; fill as we go; blank lines '' .

Header:
```js
pages.forEach(p=>{
  const fi=p.lines.findIndex(l=>l.trim()!=='');
  p.headerIdx = (p.lines[fi]&&p.lines[fi].trim()===sym)? fi : -1;
  if(p.headerIdx>=0){ p.cls[fi]='header'; repairs.push({page:p.page,target:'page',kind:'header line removed',what:'Header line (document symbol) removed',before:p.lines[fi],after:'—'}); }
});
```

Footer:
```js
pages.forEach(p=>{
  p.displaced=[];
  let j=p.lines.length-1;
  while(j>=0){
    const t=p.lines[j].trim();
    if(t===''){j--;continue;}
    if(/^GE\./.test(t)||/^(\d{6})(\s+\d{6})*$/.test(t)||/^\d{1,3}$/.test(t)){
      p.cls[j]='footer';
      if(/^\d{1,3}$/.test(t)&&+t!==p.page){ p.displaced.push(+t); }
      j--;
    } else break;
  }
  p.footerEnd=j; // last non-footer index
});
```
Wait the while with continue on empty: empty lines at very end skipped; but once we break on a non-footer, trailing empties before footer already consumed. But empty lines BETWEEN footer lines: continue skips them without classifying — but they're before (above) some footer lines... e.g. order: body, blank, "GE.25-15926", blank, pagenum? Walk from end: pagenum → footer; blank → skip; GE → footer; blank → skip; body-line → stop. The skipped blanks inside footer region remain unclassified but they're empty so not counted. OK. But wait: those blanks above GE but below body — they stay '' — fine.

Danger: bare number 1-3 digits could be a legit body line near the end? Body lines are prose. Fine.

Footnote block:

```js
let nextFn=1;
pages.forEach(p=>{
  const start=(p.headerIdx>=0?p.headerIdx+1:0);
  const end=p.footerEnd+1; // exclusive
  let blockStart=-1;
  for(let k=start;k<end;k++){
    const t=p.lines[k].trim();
    if(t==='')continue;
    if(t===String(nextFn)||t.startsWith(nextFn+' ')||(p===pages[0]&&t.startsWith('* '))){blockStart=k;break;}
  }
  if(blockStart<0){
    for(let k=start;k<end;k++){
      const t=p.lines[k].trim();
      if(t!==''&&/^\d{1,3}$/.test(t)&&+t>nextFn){blockStart=k;repairs.push({page:p.page,target:'page',kind:'footnote block removed',what:'Footnote block found after a gap in numbering (expected footnote '+nextFn+', found '+t+')',before:t,after:'—'});break;}
    }
  }
  p.blockStart=blockStart;
  if(blockStart>=0){
    for(let k=blockStart;k<end;k++) if(p.lines[k].trim()!=='') p.cls[k]='footnote';
    repairs.push({page:p.page,target:'page',kind:'footnote block removed',what:'Footnote block removed from the body text (footnotes start here)',before:first non-empty line, after:'—'});
    parseFootnotes(p, blockStart, end);
  } else {
    // all body
  }
});
```

Hmm, the "footnote block removed" repair: log once per page with block. But I also push a jump repair in fallback — double logging for fallback pages. In fallback, push only the jump-flavored entry. Reorganize: if blockStart found via opener → push plain removal entry; if via fallback → push jump entry (kind also 'footnote block removed' so kinds stay within the named set, with different what text). Good — kinds named set: header line removed, footer line removed, number and text split, paragraph joined across a page break, heading separated, heading title joined, footnote number restored, footnote block removed.

parseFootnotes:

```js
function parseFootnotes(p, s, e){
  const bl=[]; for(let k=s;k<e;k++){const t=p.lines[k].trim(); if(t!=='')bl.push(t);}
  let i=0;
  // asterisk note on first page
  if(p===pages[0]&&bl[0]&&bl[0].startsWith('* ')){ footnotes.push({number:'*',page:p.page,text:bl[0].slice(2)}); i=1; }
  const disp=p.displaced.length?p.displaced[0]:null;
  if(disp!=null){
    // first footnote: bare number, then text lines until one ends with '.'
    let num=null, rest='', fl=[];
    if(/^\d{1,3}$/.test(bl[i])){num=bl[i];i++;}
    else {const m=bl[i].match(/^(\d{1,3})\s+(.*)$/); if(m){num=m[1];rest=m[2];} i++;}
    if(rest)fl.push(rest);
    while(i<bl.length){ fl.push(bl[i]); if(/\.$/.test(bl[i])){i++;break;} i++; }
    footnotes.push({number:num,page:p.page,text:fl.join(' ')});
    const dl=[];
    while(i<bl.length&&!isFnOpener(bl[i])){ dl.push(bl[i]); i++; }
    footnotes.push({number:String(disp),page:p.page,text:dl.join(' '),repaired:true});
    repairs.push({page:p.page,target:'footnote '+disp,kind:'footnote number restored',what:'Footnote number displaced to the page foot by the converter; restored as footnote '+disp,before:'(no number)',after:'footnote '+disp});
  }
  let cur=null;
  for(;i<bl.length;i++){
    const t=bl[i];
    if(isFnOpener(t)){
      const m=t.match(/^(\d{1,3})\s+(.*)$/)||t.match(/^(\d{1,3})$/);
      cur={number:m[1],page:p.page,text:(m[2]||'')}; footnotes.push(cur);
    } else if(cur){ cur.text+=(cur.text?' ':'')+t; }
    else { cur={number:'?',page:p.page,text:t}; footnotes.push(cur); }
  }
  // advance nextFn
  const nums=footnotes.filter(f=>f.page===p.page&&/^\d+$/.test(f.number)).map(f=>+f.number);
  nextFn=Math.max(nextFn,(nums.length?Math.max(...nums):0)+1, disp!=null?disp+1:0);
}
```

isFnOpener(t): /^(\d{1,3})(\s|$)/ with rest? A bare number or number+space. Note "12 December" would match — per plan accepted.

Hmm careful: isFnOpener on "A/79/270, paras..." starts 'A' no. Good.

But wait: in the displaced branch, footnote D's text lines might include a line like "2020 study..." — 4 digits, not opener. OK.

Also stray '?' footnotes count as found? Exclude from count. Edge only.

Body:

```js
const body=[];
pages.forEach(p=>{
  const start=(p.headerIdx>=0?p.headerIdx+1:0);
  const end=p.blockStart>=0?p.blockStart:p.footerEnd+1;
  for(let k=start;k<end;k++){
    const t=p.lines[k].trim();
    if(t!=='') body.push({page:p.page,text:t,rawIdx:k});
  }
});
```

Classify:

```js
const n=body.length;
const cls=body.map(()=> 'para');
const isPStart=l=>/^\d{1,3}\.$/.test(l)||/^\d{1,3}\. \S/.test(l);
body.forEach((l,i)=>{ if(isPStart(l.text)) cls[i]='pstart'; });
body.forEach((l,i)=>{ if(/^([IVX]+|[A-Z])\.$/.test(l.text)) cls[i]='label'; });
// label text
for(let i=0;i<n;i++){
  if(cls[i]==='label'){
    let j=i+1;
    while(j<n&&cls[j]!=='label'&&!cls[j].startsWith('pstart')){ if(body[j].text.trim()!=='')cls[j]='htext'; j++; }
  }
}
```
Wait cls[j] default 'para' — loop condition cls[j]!=='label' && cls[j]!=='pstart'. But htext assigned lines then loop continues past them fine.

Hmm but careful: pstart detection with /^\d{1,3}\. \S/ — "12. The Committee..." yes. Also "1." alone.

firstP = body.findIndex((l,i)=>cls[i]==='pstart').

unlabelled:
```js
for(let i=0;i<n-1;i++){
  if(cls[i]!=='para')continue;
  const t=body[i].text;
  if(t.length<=90&&/^[A-Z]/.test(t)&&!/[.;:,\d]$/.test(t)&&cls[i+1]==='pstart'){
    cls[i]='uhead';
    repairs.push({page:body[i].page,target:'page',kind:'heading separated',what:'Unlabelled heading separated from the paragraph text below it',before:t.slice(0,60),after:'—'});
  }
}
```
Wait "not ending with ... digit" — /[.;:,\d]$/. Also heading shouldn't be before firstP? A cover line followed by pstart... cover assignment happens after; if a cover line got uhead, that's fine actually (heading). But cover lines like title "General comment No. 27 (2025) on economic..." ends with... could qualify? It must be IMMEDIATELY followed by pstart. The line immediately before first pstart is "Introduction" (htext). OK.

cover: for i<firstP && cls[i]==='para' → 'cover'. Hmm but uhead detection only for cls 'para' — cover lines before firstP are 'para' default, so a cover line right before pstart could be marked uhead. If it's genuinely a heading, fine.

Wait also: what about lines between a paragraph's end and a heading — those are htext already. And blank lines don't exist in body (non-empty only).

But: what about the last paragraph continuing to end? fine.

Paragraph assembly:

```js
const paras=[]; let cur=null;
let roman=null, letter=null, unlab=null;
const headings=[];
const snap=()=>({roman,letter,unlab});
for(let i=0;i<n;i++){
  const l=body[i], c=cls[i];
  if(c==='label'){
    if(cur&&cur.lines.length)cur.closed=true;
    // gather title
    const lab=l.text;
    let parts=[]; let j=i+1;
    while(j<n&&cls[j]!=='label'&&cls[j]!=='pstart'){
      if(cls[j]==='htext'){
        const t=body[j].text;
        if(parts.length&&(/^[a-z(]/.test(t))){ parts[parts.length-1]+=' '+t; repairs.push({page:l.page,target:'heading',kind:'heading title joined',what:'Heading title wrapped over two lines; joined',before:parts[parts.length-1].slice(0,50),after:'—'}); }
        else parts.push(t);
        cls[j]='htext'; // stays
      }
      j++;
    }
    const title=(parts.join(' ')).trim();
    const isRom=/^[IVX]+\.$/.test(lab);
    const h={label:lab,title,page:l.page,roman:isRom};
    headings.push(h);
    if(isRom){roman=lab+' '+title; letter=null; unlab=null;}
    else {letter=lab+' '+title; unlab=null;}
    i=j-1;
  } else if(c==='uhead'){
    if(cur&&cur.lines.length)cur.closed=true;
    unlab=l.text;
    headings.push({label:null,title:l.text,page:l.page,unlabelled:true});
  } else if(c==='pstart'){
    if(cur)paras.push(cur);
    const m=l.text.match(/^(\d{1,3})\.(?:\s+(.*))?$/);
    cur={number:+m[1],lines:m[2]?[m[2]]:[],pages:[l.page],ctx:snap()};
    if(m[2])repairs.push({page:l.page,target:'para '+m[1],kind:'number and text split',what:'Paragraph number and text shared one line; split',before:l.text.slice(0,60),after:'—'});
  } else if(c==='para'){
    if(!cur){ orphans.push(l); continue; }
    cur.lines.push(l.text); cur.pages.push(l.page); cur.ctx=snap();
  }
  // 'cover','htext' with cur open: htext handled in label loop; standalone htext can't occur outside label loop... actually htext only assigned within label loops which skip via i=j-1. cover: lines before firstP, cur null.
}
if(cur)paras.push(cur);
```

Wait — the label loop: `while(j<n && cls[j]!=='label' && cls[j]!=='pstart')` — inside it should consume htext lines but also 'para' lines?? Between a label and the next pstart, lines are its title (possibly multi-line). All those lines were assigned 'htext' in the earlier pass. So the while just walks htext/cover?? Cover before firstP: label "I." occurs... wait, is "I." before firstP? Page 1: cover stuff, then "I.", blank, "Introduction", "1." — firstP is "1.". So "I." and "Introduction" are before firstP. My earlier cover assignment: for i<firstP with cls 'para' → 'cover'. "I." is 'label', "Introduction" gets 'htext' from label pass (which ran before cover assignment). So order: pstart labels → label pass (htext) → firstP compute → uhead → cover. "Introduction" is htext, not cover. Good.

But in the label walk, I set i=j-1 skipping htext lines — but those skipped lines might include 'cover' lines if a label appears with no pstart until after cover?? Only page-1 scenario; handled.

Also cur.closed logic unnecessary; ctx snapshot at each push suffices. But paragraph between its last line and next pstart may pass headings — cur.ctx was set at last line push, before headings. For paragraphs with zero lines after pstart (number line then immediately heading?? no). For inline pstart with text, ctx set at creation (before subsequent lines). Fine: set cur.ctx on each line push and at creation; push uses cur.ctx at close... wait at close (next pstart), cur.ctx holds snapshot from last line — correct (before intervening heading). 

Paragraph finalize:

```js
paras.forEach(p=>{
  const raw=p.lines.join(' ').replace(/\s{2,}/g,' ').trim();
  p.text_raw=raw;
  p.page_start=p.pages[0]; p.page_end=p.pages[p.pages.length-1];
  if(p.page_end!==p.page_start)repairs.push({page:p.page_end,target:'para '+p.number,kind:'paragraph joined across a page break',what:'Paragraph continued from page '+p.page_start+' to page '+p.page_end+'; joined',before:'—',after:'—'});
  p.hyphenLines=p.lines.filter(l=>/-$/.test(l.trim())).length; // count, report
  p.section = p.ctx.unlab || p.ctx.letter || p.ctx.roman || '';
  p.part = p.ctx.roman || '';
  p.path = [p.ctx.roman,p.ctx.letter,p.ctx.unlab].filter(Boolean).join(' › ');
});
```

Hmm — ctx captured via snap() closure of roman/letter/unlab variables — but snap captures current values at call time (strings), fine.

Marks:

```js
const counter={n:1};
paras.forEach(p=>{
  const {text,marks,rejected}=bracket(p.text_raw,counter);
  p.text=text; p.marks=marks; p.rejected=rejected;
});
```

bracket:
```js
function bracket(raw,counter){
  let out='',last=0; const marks=[],rejected=[];
  const re=/\d{1,3}/g; let m;
  while((m=re.exec(raw))){
    const s=m.index,e=s+m[0].length;
    const prev=raw[s-1]||'',nx=raw[e]||'';
    if(/[\d\/\-(]/.test(prev)||/[\d\/\-(]/.test(nx))continue;
    const num=+m[0];
    if(num===counter.n){ out+=raw.slice(last,s)+'['+m[0]+']'; last=e; marks.push(num); counter.n++; }
    else rejected.push({num,ctx:raw.slice(Math.max(0,s-18),Math.min(raw.length,e+12))});
  }
  out+=raw.slice(last);
  return {text:out,marks,rejected};
}
```

Wait — rejected candidates also include runs blocked by neighbors (like "2025" inner "025"? no—\d{1,3} on "2025" matches "202" then continues from after... regex \d{1,3} greedy: on "2025" matches "202", then next match "5". prev of "202" is non-digit ok, nx is '5' digit → skip. "5": prev '2' digit → skip. Good.) Rejected only records candidates not equal to counter. Those blocked entirely aren't "rejected as not marks" per check? "the numbers it rejected as not being marks (with context)" — I'll record only unblocked candidates ≠ counter. Fine.

First words:
```js
function norm(s){return String(s||'').replace(/[\u2018\u2019\u201B\u2032]/g,"'").replace(/[\u201C\u201D\u2033]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();}
function firstWords(t){return norm(t.replace(/\[\d{1,3}\]/g,'')).split(' ').filter(Boolean).slice(0,6).join(' ');}
paras.forEach(p=>{ p.fw_found=firstWords(p.text); p.fw_ref=ref.first_words?ref.first_words[String(p.number)]:null; p.fw_match=p.fw_ref!=null&&norm(p.fw_ref)===norm(p.fw_found); });
```

Footnote contamination check:
```js
const probes=footnotes.filter(f=>/^\d+$/.test(f.number)||f.repaired).map(f=>{
  let opener;
  if(f.repaired){ opener=f.text.split('\u2014')[0]... 
```
Hmm need opener line for each footnote. Better: store f.opener (first 40 chars incl number) at parse time. In normal parse, opener = the opening line (m[0] original t). In displaced: first footnote opener = its number line (num); restored footnote D opener = its first text line. Let me store f.opener40 = first 40 chars of opening line. For first footnote in displaced branch: opening line = num (bare) + first text line? "the first 40 characters of every line that opens a footnote, its number included" — for bare-number opener the line is just the number; then text is next lines. Hmm — then probe "15" alone would hit everywhere! Wait, re-read: "The first 40 characters of every line that opens a footnote, its number included ('15 Human Rights Committee, general comm…')". The example "15 Human Rights Committee..." — that's a number+space+text opener (one line). But data says "the first on a page is a bare number on its own line, a blank line, then the text". So for a bare opener, the "line that opens" — the example suggests combining number + following text. I'll build probe as: (number + ' ' + first text line) first 40 chars for bare openers; for num+space openers the line itself; for restored, first line of its text (no number). Reasonable.

Then search probe (escaped regex? plain indexOf in raw text) across paras' text_raw. Count hits, record which paras.

Long paras: words = text_raw.split(/\s+/).length > 300.

Also "before footnote marks are touched" — use text_raw. But probe might contain regex-special chars; use indexOf. Also normalise? Keep plain.

Checks assembly. Then rendering.

Nothing lost: total nonempty = sum pages lines filter trim!==''; classified = count of p.cls entries non-empty... but orphan lines: I gave them no class. Let me set their cls to 'orphan' in p.cls via rawIdx. Body lines map to p.cls[rawIdx]: 'cover','label'→'heading','htext'→'heading','uhead'→'heading','pstart'→'paragraph','para'→'paragraph','orphan'. Header/footer/footnote already set. Then unclassified = non-empty lines with empty or placeholder cls. Count and list (page, line).

Careful: cls default — initialize p.cls with '' for blank and 'unclassified' for non-empty; then filled. At end, remaining 'unclassified' → listed. But footnote block blank lines etc fine.

Also body lines that are blank? We skip empty in body push. But their p.cls stays 'unclassified'?? No — blank lines get '' at init. Only non-empty init 'unclassified'.

Wait: lines between footerEnd and end that are empty... init '' ok. Lines in footnote block: set 'footnote' for non-empty. Block blank lines '' — but init set 'unclassified' for non-empty only; blanks '' — good. But lines after block within [blockStart,end) all set 'footnote' if non-empty; blanks skipped → remain '' good. Lines before headerIdx (should be none) — non-empty would be 'unclassified'. OK.

Hmm one bug: p.cls init: `p.raw.map(s=>s.trim()===''?'':'unclassified')`. Then header/footer/footnote fill. Then body fills via rawIdx. 

Cover lines: 'cover'.

Now the check "Headers and footers": pages with header (first non-empty === symbol) count vs total; pages with page-number footer vs total-1 (expected all but first); displaced listed.

Check "Headings": labelled count = headings.filter(!unlabelled).length; unlabelled count + list titles.

Now render. Let me write render code with helper h = (html string building).

Rendering paragraphs table rows: ~90 rows * expansions — fine.

Escape HTML: esc().

Copy citation:
```js
function copyText(t,btn){ if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,fb)}else fb(); function fb(){const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(e){}ta.remove();ok();} function ok(){const old=btn.textContent;btn.textContent='Copied';setTimeout(()=>btn.textContent=old,2000);} }
```

CSV download:
```js
function download(name,content){const b=new Blob([content],{type:'text/csv;charset=utf-8'});const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),3000);}
```

Now render functions per tab, all reading from current res (state.res). Event delegation on document for clicks: row toggles, tab switching, collapsibles, copy, downloads, select change, doc cards.

Let me structure render:

```js
function renderAll(){ renderHeader(); renderRail(); renderTabs(); renderResult(); renderParagraphs(); renderFootnotes(); renderChecks(); updateStatus(); }
```

Panels are static containers in HTML; content filled.

Tab logic: state.tab in 0..3; panels hidden attr; tab buttons aria-selected; arrow keys.

Collapsibles: repair log (open when triggered from tile 01: state.openRepair=true then switch tab 04 and set aria-expanded true and show content). I'll implement toggle via delegation on buttons with data-toggle target id.

Raw pages: state.rawPage.

OK, writing the final file now. Also must ensure "no more than ~7 things to click" per view — tabs(4) + rail cards + collapsibles... tab 04: 4 tabs + repair log + raw pages + download + select = 7ish. Fine.

Table captions: serif caption with message + mono TAB number. E.g. paragraphs table caption "90 paragraphs found, 90 expected · TAB.02". Footnotes "141 footnotes found of 141 · TAB.03".

Note: count is string "20" — pages = records length, ignore count.

Header line: `symbol` linked, "adopted X", "n pages of raw converter text", source. reference.adopted e.g. "6 November 2025"? show "adopted …" if present.

Tile computations:
- paragraphsFound = paras.length; refParas = ref.paragraphs.
- footnotesFound = numeric footnotes count; ref.footnotes.
- fwMatches = paras.filter(fw_match).length of refParas.
- repairs count.

Bar in rail: share found/ref; red when found<ref or >ref; green(ok #1e6b3a?) Actually bar accent deep red when wrong; normal ink/grey when ok? Use red when mismatch, dark green when equal? Plan: "a thin bar showing the share found (red when short or over)". Default bar colour — I'll use #9b2335 red when mismatched, #1d1b18... hmm, green when equal fits "Pass is dark green". Use green when equal, red otherwise.

Also tab 04 gets red dot when failed: add a small dot in tab label.

Check panel: each check line: name — detail — status word. Pass dark green, fail red with link to rows ("see para n" links switching to tab 02 and expanding? simpler: link text switches tab and scrolls... I'll make links that switch to tab 02 and expand the row via data-paralink). Keep simple: link switches to tab 02 and opens that paragraph's expansion.

Let me write out now. I'll try to keep code tidy. Also ensure everything is offline, no external.

Word count > 300 listing in check 6: list "para. n (m words)".

Marks check detail: marksTotal = counter.n-1; missing = numbers 1..ref.footnotes not in marks (should be none if counter reached end); rejected list count + sample.

Footnotes check: found count, sequence check: numbers array (numeric, in document order); expected 1..found; gaps/dups listed; restored listed with page.

Numbering check: para numbers in order === 1..len; list anomalies.

First words check: mismatch count with list "para. n: found … / reference …" (maybe first 10 + more count).

Nothing lost: totals + unclassified list.

Headers/footers check: headerCount/total, footerPageNumCount/(total-1), displaced list.

Also "A page with no opener at all (none here) is all body, and the check panel says so." — add to footnotes check detail: pages without block listed. Track pagesWithNoBlock.

Alright, code writing time. I'll write it in one pass, being careful.

Also `built`: pdf_text description doesn't list built. Use doc.built if present else ''.

Rail cards: each card shows symbol, short title (title first 40 chars?), adopted, pages. Selected: red left border. Also big numbers below cards — but those belong to selected doc. Plan: card then under it two big numbers — the numbers are for the selected document. OK.

Edge: first_words keyed by string number.

Now, potential issue: tab 02 Section column width; fine.

Also "First line" = first 120 chars cut at word with "…":
```js
function firstLine(t){const s=t.slice(0,120);const c=s.slice(0,s.lastIndexOf(' '));return (t.length>120?(c||s)+'…':s);}
```
Hmm if space exists. fine.

Now write the whole file.

Rough structure sizes fine. Let me write.

Also: tab panels should not be focusable when hidden: panels get hidden attr; tab buttons in hidden tab? Tabs all visible. "the tab panel of a hidden tab is not focusable" — hidden panels' content not focusable since display:none. OK.

Also [hidden]{display:none!important}.

Legend and raw viewer: build lines as divs with class by code. Select populated with pages.

Let me finalize the repair log table: Page | Paragraph or footnote | What was done | Before | After. Counts per kind above: "header line removed: n · ...".

Also "footnote block removed" entries per page with block — that's ~19-20 entries, plus header 20, footer ~ many (one per footer line!). Footer lines: each dropped line logs? Plan: "each step logs what it removed or changed" — footer line removed per line would be ~60 entries. That's fine ("a table of every change"). Hmm, that inflates repairs count (tile "Repairs made: n"). Plan kinds include "footer line removed" — per line. OK, log each footer line as a repair. Total repairs maybe ~150+. Fine.

Wait — but then "the repairs that touched this paragraph" would include footer removals for pages in range — very noisy (3 lines per page). Hmm. For paragraph repair lists, I'll include only: number and text split, paragraph joined, heading separated/joined (page-level but heading-related...). Let me reconsider: "the repairs that touched this paragraph" — I'll filter: r.target==='para '+num, plus page-level kinds 'number and text split' (targeted anyway), 'paragraph joined' (targeted), 'heading separated'/'heading title joined' for pages in range? Headings belong between paragraphs. I'll include para-targeted + heading kinds + footnote-number-restored? no. Simplest meaningful: para-targeted repairs + page-level 'heading separated'/'heading title joined'/'footnote block removed' for pages within [page_start,page_end]. I'll include those; footer/header line removals excluded (they touch the page, not the paragraph's text). Reasonable.

Actually to keep it truly simple: include kinds in a set: {'number and text split','paragraph joined across a page break'} with target match, plus {'heading separated','heading title joined','footnote number restored'} where page in range? footnote restored is in footnote block not paragraph. Just heading ones. Decide: para-targeted ∪ (heading kinds ∧ page∈range). Good.

CSV repairs column: kind list joined '; ' — use para-targeted only? Use same filter as row display. I'll use the same function.

Time to write. Also ensure the fallback `t.startsWith(nextFn+' ')` — e.g. nextFn=7, line "7 E/2003/22…". Yes.

One more: nextFn advance "past the highest number seen in the block". If page has footnotes 5,6: highest 6 → nextFn=7. And displaced branch already adds D. Since D is second footnote and highest numbered might be < D? displaced number D was in footer of same page, its text is footnote D... wait no: the displaced number D is the number OF the footnote whose text lost its number — D equals that footnote's number. The first footnote is number D-1 typically. So highest = D. Fine.

Hmm wait, subtle: is the restored footnote D placed after first footnote — but the block might continue with more numbered footnotes (7 ...). Order preserved by push order. Good.

Also the asterisk footnote counted? "kept as footnote '*' and not counted". Numeric count excludes it.

Now checks "Footnotes": "the numbers run from 1 to that count without a gap or a duplicate" — check numeric footnotes' numbers sorted equal 1..N.

Edge for GC32 (pdf_text_2): does it have displaced footnotes? Unknown; code handles both.

Also GC32 page 1 header: first line "CCPR" ≠ symbol "CCPR/C/GC/32" → header check will show "19 of 18 pages"? It reports honestly: "pages whose first line was the symbol: k of total". Fail if k<total. Fine, honest. Hmm, but maybe GC32 later pages have "CCPR/C/GC/32" as first line — sample page 1 shows "CCPR". The header line then stays in body → becomes 'cover' (before firstP) — fine, it's on page 1 before para 1. Good.

Wait, actually if header not removed on page 1, "CCPR" line is before first paragraph start → cover. And "UNITED NATIONS" etc → cover. OK.

But careful: on pages where header not removed and the symbol line appears mid-body (page 2+), it'd be a 'para' line glued into a paragraph! That would corrupt GC32 text if headers aren't the first line matching symbol. Risk: first non-empty line of GC32 pages might be "CCPR/C/GC/32" or something else. Sample page 2+ unknown. The "nothing lost" and first-words checks would flag problems. Also plan says "If a page's first non-empty line equals symbol, drop it; otherwise log a warning". I'll follow plan. But to be safer for body contamination, I could also drop any body line that exactly equals the symbol anywhere? Plan doesn't say. I'll follow plan strictly; checks will reveal.

Hmm, actually there's a real risk GC32's running header is just "CCPR" (as sample shows) which won't equal symbol, and pages 2+ may repeat "CCPR" as first line → glued into paragraphs → first-words mismatches. The plan explicitly says log warning. But maybe GC32's pages have symbol "CCPR/C/GC/32" on later pages... The sample shows page 1 with "CCPR" first. Actually typical UN docs: page 1 has "CCPR" big; later pages have the symbol. Page 2 of GC32 sample not shown. I'll additionally treat a first-non-empty line equal to symbol OR equal to a repeated first-page token... no, don't invent. Follow plan. Actually, let me add a mild robustness: if first non-empty line isn't the symbol but equals another page's first line (a repeated running header across pages), treat as header too? That's inventing beyond plan but harmless and honest ("header line removed" only when equal symbol; else warning). Plan says keep simple. I'll follow the plan exactly.

Now, GC32 has 128 footnotes over 18 pages — pipeline should work.

Also "count" is string "20" — I use records.length.

Let me also compute "n pages of raw converter text" = pages.length.

Writing final HTML now. I'll write ~900 lines.

Also careful: in template literals I need `\[\d+\]` displayed as text — fine in HTML text (escape backslash? No, backslash is literal in HTML text). In JS template building note text: use String.raw or escape. I'll write 'pattern \\[\\d+\\]' carefully or just embed literal text `\[ \d+ \]` in HTML via template string — backslashes fine in template literal but `\d` in a template literal is just 'd'? No — in JS template literals, `\d` is an unrecognized escape → in non-tagged templates it's 'd'? Actually `\d` evaluates to 'd' (backslash dropped). So I must write `\\[` etc. I'll use a constant NOTE with escaped backslashes.

CSV text fields contain quotes/curly quotes — doubled only for `"`. Fine.

Let me now also handle `first_words` check when ref missing: status 'not run'.

Write the code.

For the check line links: "with a link to the rows concerned" — for first-words check, link "para. n" that goes to tab 02 and expands that row. I'll give expansion rows ids `pexp-N` and row `prow-N`; link with data-goto="para:N". Handler: switch tab 2, expand row, scrollIntoView.

OK writing.

Also the result tile "Paragraphs found: n" next to "The document has: ref" — green when equal, red with difference. If paragraphs contain footnotes (contamination), tile says "n contain footnotes" in red even when count right.

Footer of tables: source line under table — "Source: symbol, doc_url" etc.

Let me write everything now, final.

One more detail: "Show the PDF's lines" toggle under expanded text: shows lines with page markers where each page began: render lines; before a line whose page differs from previous, show "— page N —".

Also expanded paragraph shows: full text (one block), toggle, reference first six words vs found, pages, repairs, footnotes cited, copy citation button.

Footnotes cited in expanded paragraph: list numbers, clickable? Just list; maybe link to tab 03? Keep text.

Now finally: header status: failed>0 → red dot "n checks failed"; else green "n of m checks pass" where n=passed, m=total checks (including not run? if not run exists and failed=0, green with n of m). OK.

Writing code now for real. I'll be disciplined about length.

Structure:

```html
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Paragraphs out of a PDF</title><style>...</style></head><body>
<header class="apphead">...</header>
<div class="layout"><aside class="rail" id="rail"></aside><main class="main">
<div class="tabbar" role="tablist" aria-label="Tabs" id="tabbar"></div>
<div id="panels">
 <section id="panel0" role="tabpanel" class="panel"></section>
 ... 4
</div></main></div>
<footer class="appfoot" id="appfoot"></footer>
<script>...</script></body></html>
```

CSS quickly:

```css
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--red)}
.mono{font:11.5px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
.apphead{padding:20px 28px 14px;border-bottom:1px solid var(--rule)}
...
```

I'll flesh out.

Given size, let me just write it.

For raw viewer tints:
```css
.lv-c{background:#ece3d2}.lv-h{background:#e0ddca}.lv-s{background:#e9e4cf}.lv-p{background:#faf7f0}.lv-n{background:#e2e6e4}.lv-b{background:#e5ded2}.lv-x{background:#f2d5d5}
```

Codes: C cover, H header, S heading, P paragraph, N footnote, B footer, ! unclassified/orphan.

Orphan: I set cls 'orphan' → code '!', tint red. And unclassified leftover also '!'.

Legend lists all.

Now the JS. Let me write final code mentally-complete and output.

Paragraphs table columns: No | Section | Page | First line | Check. th scope col. numbers right-aligned (No, Page). Check cell "OK" (green? plan: "OK" or "first words differ" red; OK plain). 

Footnote table: No | Page | Text | Repair. Text truncated 100 chars; expansion full text.

Headings box: collapsible above table: button "Headings found: n" aria-expanded; content: list "label title (page)".

Tab 04 layout: checks (open list), repair log collapsible, raw pages collapsible, download button.

Repair log content: counts per kind (mono line), table Page|Target|What|Before|After.

Download paragraphs CSV button on tab 04 (plan says Download under raw pages section on tab 04). Footnotes CSV on tab 03.

Now writing final answer. Intro: up to three sentences before code block.

Let me carefully write the JS now (in my head → output). I'll number panels 0-3.

Key functions:

```js
const esc=s=>String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
```

State: {docs, key, tab:0, rawPage:1, cache:{}, openRepair:false, openRaw:false}

renderTabs: four labels.

Tile HTML etc.

Event delegation:

```js
document.addEventListener('click',e=>{
  const t=e.target.closest('button,a,select'); ...
```
Handle: [data-tab], [data-doc], [data-toggle], .prow (row expand), .frow, [data-copy], [data-dl], [data-goto].

Row expand: rows have data-p index into res.paras. Toggle hidden on next sibling.

Select change for raw page: 'change' listener.

Tab key handling on tabbar keydown.

Let me write it all out now. Estimate ~950 lines. Go.

For check "Footnote marks" detail: "Marks found: k, expected 1..ref.footnotes. Missing: … Rejected as not marks (shown with context): n — 'article 11'…". I'll show rejected count + up to 12 samples.

For contamination check detail: hits count with para list; long paragraphs list.

Compose check objects: {name, status, detail (html)}.

Also need results accessible: state.res.

Let me also handle doc without reference fields gracefully in tiles: "no reference in this file".

Alright — output time. I must be careful with regex literals inside the single script and with template literals containing backticks — none.

Also note: body lines could include the "I." label check /^[IVX]+$/ conflicts? /^([IVX]+|[A-Z])\.$/ — a paragraph line "I." unlikely.

Potential clash: unlabelled heading detection requires cls[i]==='para' but htext lines already classified — e.g. "Introduction" is htext so not double-counted. But what about a labelled heading's title line that is long and followed directly by pstart? It's htext — fine.

Another clash: uhead check "immediately followed by paragraph-start line": body[i+1] — but between them there may be no blank (body excludes blanks). Good.

What about the last body line of page N and first of page N+1: concatenated adjacency — a paragraph's last line followed by next page's first body line which is a pstart → uhead detection might fire on the last line of page N if it looks like a heading! E.g. paragraph ends "...rights." ends with '.' → excluded by "not ending with full stop". A line ending without period mid-paragraph? Paragraphs' wrapped lines can end without punctuation! E.g. a wrapped line "of the present report" followed by next page's... wait, if paragraph continues across page break, next page's first line is a continuation, not pstart, so uhead check looks at body[i+1] which is continuation — not pstart → no fire. Fire only when body[i+1] is pstart, i.e., genuinely the line before a paragraph number. Mid-paragraph wrapped lines are followed by more paragraph lines. The only risk: a heading-like wrapped line that happens to be the last line of a paragraph (paragraphs end with '.' typically) — excluded. OK.

Also uhead could fire on the line immediately before an inline pstart "23. The Committee..." — fine, that's the intent.

One more risk: htext lines between label and pstart — the last htext before pstart is fine.

What about 'cover' lines before firstP followed by pstart — e.g. cover line right before "1." — that's "Introduction" (htext). But in GC32 page1, structure differs; if a cover line precedes first pstart and looks heading-like → uhead, reasonable.

Cover assignment order: I compute uhead BEFORE cover (uhead only for cls 'para'). Cover loop after: for i<firstP && cls[i]==='para' → 'cover'. If a cover line became uhead, stays heading. Good.

But wait: order matters — the label htext pass runs over all body including before firstP. Good.

Edge: inline pstart regex: /^\d{1,3}\. \S/ — must also not be like "1. " with nothing. fine.

But hazard: a body continuation line like "2. " within text? e.g. "article 1. 2"? unlikely.

Also "number and text split" repair before/after: before = full line, after = 'number + first line'. Fine.

Now — writing! Also remember: mechanism for "paragraph joined across a page break" — logged once per paragraph that spans; page of repair = page_end.

For CSV footnotes_cited: marks.join(' ').
repairs column: repair list kinds joined '; '.
first_words_match: 'TRUE'/'FALSE' or 'yes'/'no'. Use 'TRUE'/'FALSE'.

Citation: sym+', para. '+number.

OK write.

Also header always-visible right side status: `<span class="dot green/red"></span> text`.

Rail: heading "DOCUMENT" mono; cards; big numbers block; checks link.

Let me now produce the final file. I'll write ~compact but complete. Ensure under 1500 lines — yes.

Also the "Headings found" collapsible counts: headings array.

Also for tab 02 caption: `${paras.length} paragraphs found, ${ref.paragraphs} expected`.

Footnotes caption similar.

Check panel caption "n of m checks pass".

Alright, final code.

One thing: `studio.openSource` not relevant here (pdf_text). doc_url links only.

Writing now.

Also add credits? No external code used. Skip.

Now produce. Careful with `norm` for first words comparing found vs ref: also strip footnote marks from found (done via firstWords on p.text which has [n] → removed). But also the raw text may contain footnote numbers glued ("waste.2") — bracketing makes "waste.[2]", removal gives "waste." — but reference first words likely "waste." too? Reference first words are clean text; a mark mid-sentence in first six words would break match... plan says marks removed first — "[n]" removal. Since marks become [n], removal handles it. Good.

But rejected numbers (like real "article 11") stay in text — fine.

Edge: marks walk counter shared across paragraphs in document order — yes, single counter object.

Let me also compute totalWords for long-para check.

Time to write output.