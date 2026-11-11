Build the full app per the detailed plan. One HTML file, two tabs, left rail, checks panel, exports, expanded rows, PDF lines toggle. Must be under ~1500 lines. Let me write carefully.

Data: WORKSHOP_DATA.pdf_text = {title, symbol, doc_url, source, count, records, reference}.

Pipeline:
- Sort records by page.
- For each page: split text into lines (split(/\n/)).
- Header: first non-empty line equals symbol → drop, else warning.
- Footer: from end, drop while empty, startsWith "GE.", only 6-digit groups (like "051125 061125" — test: /^\d{6}(\s+\d{6})*$/), or bare number 1-3 digits. If bare number equals page → page number; else count as displaced footnote number.
- Body lines concatenated with page tags.
- Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.
- Headings: labelled /^([IVX]+|[A-Z])\.$/ — but careful: "A." could also be... fine. Collect heading text lines until next label line or paragraph start; a line starting with lowercase or "(" continues. Simpler: when we hit a label line, we enter "heading" mode; subsequent non-empty lines are heading text until we hit another label line or paragraph start. Join them.
- Unlabelled heading: non-empty line immediately followed by a paragraph-start line, ≤90 chars, starts with capital, doesn't end with . ; : , or digit. Two-line heading: the line before it passes the same test and "does not end a paragraph sentence" — check previous line doesn't end with . ; : etc? "does not end a paragraph sentence" — previous text line ends with something that isn't sentence-final... The plan: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading". So if line before the heading candidate also passes the unlabelled-heading test (starts capital, ≤90, no sentence-final punctuation), merge. Actually implement: heading candidate at index i (followed by paragraph start). Check line i-1: non-empty, passes same test → and the line i-2... hmm "does not end a paragraph sentence" — since it passes the same test it doesn't end with . ; : , digit, so it qualifies. Merge i-1 and i.
- Also asterisk lines? The note "* Adopted by the Committee…" is a suspect line in text (in paragraph before para 1? It's on the cover... plan says suspect line example). Cover lines before first paragraph start are cover, not paragraph. Hmm, but the suspect example includes "* Adopted by the Committee…". It's within the cover, not a paragraph — so never in a paragraph. Fine, keep rule anyway.
- Paragraph text: join lines with single space, collapse doubles, trim.
- Suspect lines: inside a paragraph, a line that is a bare number 1-3 digits (no full stop), or starts with 1-3 digits + space + capital letter, or a UN doc symbol, or quotation mark — the plan says: "or starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". Hmm: "7 E/2003/22…" starts with digit-space-E (capital). "2 Summary for policymakers…" digit-space-capital. Quotation mark start: starts with " or “ . So rules: bare number, /^(\d{1,3})\s+[A-Z“"']/, or starts with "* ". Also UN doc symbol? "A bare number ... or starts with ... a UN document symbol" — reading: starts with digits+space+capital, a UN symbol, or a quote. UN symbol regex like /^[A-Z]{1,4}\/[A-Z]/ — a line starting with that. I'll include: /^[A-Z]{1,4}\/\S/ as suspect too. And /^\*\s/.
- Once a suspect line found in a paragraph, that line and every line after it to end of its page are suspect. So per page: find first suspect line index within paragraph; mark that line and all later lines of the same paragraph on the same page and... "every line after it to the end of its page" — lines after it belonging to that paragraph on that page (footnote text is after). But lines after could also include continuation? Actually the footnote block runs to the foot; lines after the suspect line in the same page are footnote lines belonging to that paragraph's page. But those lines are part of the paragraph (they were classified as paragraph lines since they're after paragraph start until next paragraph start). So mark all subsequent lines of the paragraph on the same page as suspect. If paragraph continues to next page, next-page lines are not suspect (new page). Hmm — but if the paragraph crosses the page, its continuation on next page should not be marked. I'll mark: from the suspect line to the last line of that paragraph whose page equals the suspect line's page.
- Word count >300 → flagged.
- First words: strip footnote marks from first tokens. Algorithm: take text, split on whitespace, take tokens; process: remove digits glued at end of word/punctuation ("waste.2"→"waste."); a digits-only token dropped only when previous token ends with . , or closing quote and not abbreviation "No." "art.". Collect first six words. Compare with reference after normalizing quotes/dashes.
- Classification of every non-empty line: cover (before first paragraph start... but headings count separately), header, heading, paragraph, footer. Count and sum. Lines in cover: non-empty lines before first paragraph start, not header/footer. Note: headings before first paragraph start? Headings like "I. Introduction" appear after paragraph... In this doc, para 1 comes after "I. Introduction" heading, and the cover includes title lines etc. Cover = lines before first heading/paragraph-start. I'll classify: lines before first paragraph start or heading label, whichever first → cover.
- Checks list: paragraph count, numbering 1..n, first words, flagged, suspect lines, headers/footers, headings, nothing lost, export round trip.

Checks "pass/fail" count for header dot: which checks are pass/fail? I'll define checks with pass boolean. Paragraph count, numbering, first words (0 mismatches), nothing lost (0 unclassified), headers (all pages symbol), footers page numbers... Some are informational. For the green/red dot "n of m checks pass", I'll count checks with a defined pass status; informational ones (flagged, suspect) don't count toward pass/fail? Plan says header shows "n of m checks pass" or red "n checks failed". I'll make all listed checks count, with informational ones always "pass" (they're reports). Hmm, "A flag is not a failure" — so the flagged check line reads informational. I'll give it pass=true always (it's a report). Headers check: expected all pages → pass if all. Footer page numbers: expected all but first → pass if so. Export round trip: pass if equal.

UI: header, tabs 01 RESULT, 02 PARAGRAPHS. Left rail. Tab 01: four tiles, mismatch list, export buttons, two closed headings (Every check, Flagged paragraphs). Tab 02: closed "Headings found" box, table with expandable rows, copy citation, "Show the PDF's lines" toggle.

Clicking flagged row on tab 01 opens paragraph on tab 02 with suspect lines highlighted — just switch tab and expand that row.

Keep code compact. Let me write it.

Downloads: JSON and Markdown via Blob.

Citation copy: navigator.clipboard may fail in sandbox; fallback with textarea+execCommand. I'll try clipboard then fallback.

Let me write the HTML now. Aim ~700-900 lines.

Design: CSS per spec — paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, green #1e6b3a for pass. Fonts. Tabs with role=tablist and arrow keys.

Structure:

```
header: .mono label, h1 title, meta line, right: dot + checks, flagged count
nav tabs
main: aside rail + section panels
footer
```

Render functions: renderResult(), renderParagraphs(). State: currentTab.

Let me write the pipeline code.

```js
const D = WORKSHOP_DATA.pdf_text;
const sym = D.symbol;
const pages = [...D.records].sort((a,b)=>a.page-b.page);
```

Line classification:

```js
const pageData = pages.map(p=>{
  const rawLines = p.text.split('\n');
  let lines = rawLines.map(l=>l.trim()); // hmm trimming? Keep original for PDF lines view but trimmed is fine.
```

Actually keep raw lines, trim when comparing. I'll store trimmed lines.

Header: first non-empty index; if equals sym → header. 
Footer: iterate from end over raw lines: skip empties; while line matches footer patterns → classify as footer (track page-number vs bare-number). Stop at first non-matching from the end. Note: footnote text is above footnotes... wait footnotes sit at foot before footer. Footnote text lines won't match footer patterns (they're sentences), so footer scan stops at the last footnote line. Good. But "bare number" footnote-start lines at the foot: first footnote is a bare number on its own line — the scan from the end will hit footer lines (GE code, page number) then reach the footnote text; if the last footnote line... the scan only removes footer lines from the very end; footnote text lines aren't at the very end (footer is), so ok. But wait: is the last footnote line maybe a bare number? Unlikely. However the footer scan dropping "bare number 1-3 digits" lines could eat a footnote's first bare number if it were the last line — but footer lines come after, so no.

Edge: what if GE code appears mid? Fine.

Body lines: lines between header and footer, each with page.

Then heading/paragraph scan over concatenated body lines.

Labelled heading: /^([IVX]+|[A-Z])\.$/. But paragraph-start /^(\d{1,3})\.$/ — digits, no clash. However "A." subsection vs roman "I." — both go to heading mode. Track roman vs letter: part = most recent roman heading.

In heading mode: after the label line, subsequent non-empty lines until next label or paragraph start or unlabelled heading? Heading text lines. A line starting with lowercase or "(" continues previous heading line — meaning wrapped title lines. Simplest: all non-empty lines after label until next label/paragraph-start are heading text, joined. But unlabelled headings could follow a labelled heading immediately (e.g. "A. Some title" then "Right to work (art. 6)" then paragraph)? Unlabelled heading detection: line immediately followed by paragraph-start line and passes test — this works even in heading mode. So in heading mode, check each line: if it's an unlabelled heading (followed by para start), close current heading and record it. Good.

Unlabelled heading test: 
```js
function isUnlabH(i, lines){ 
  const l=lines[i].text; if(!l) return false;
  const nxt = lines[i+1]?.text||'';
  if(!/^\d{1,3}\.\s/.test(nxt) && !/^\d{1,3}\.$/.test(nxt)) return false;
  if(l.length>90) return false;
  if(!/^[A-Z]/.test(l)) return false;
  if(/[.;:,]$/.test(l) || /\d$/.test(l)) return false;
  return true;
}
```
Two-line merge: if line i-1 is non-empty, passes same shape test (starts capital, ≤90, not ending .;:,digit, not itself followed by para start... whatever) and "does not end a paragraph sentence" — since it passes the no-final-punctuation test it qualifies. But also the previous line must not be a paragraph line ending... it passes test so fine. But careful: the previous line could be an actual heading already consumed. I'll implement: when detecting unlabelled heading at i, check i-1: if lines[i-1] exists, non-empty, not classified yet, passes test (capital start, ≤90, no sentence-final end) → merge. But that previous line would otherwise be paragraph text (a line not ending with punctuation that precedes a heading... could be paragraph text mid-sentence!). Hmm, "does not end a paragraph sentence" — a paragraph line continuing would not end with sentence punctuation either. Risk of false merge, but plan specifies this rule. Actually plan: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading". The "same test" includes being ≤90 chars, starting with capital, not ending with .;:,digit. And "does not end a paragraph sentence" is additional — I'll interpret: the line before it does not end with . ! ? ; : — i.e., not sentence-final. Since test already excludes .;:, I add ! ? too. OK.

But hold on — a paragraph's last line before a heading would typically end with "." so excluded. Good.

Headings list for the "Headings found" box: labelled (with type roman/letter) and unlabelled.

Main loop over body lines (array of {text, page, raw}):

```js
let mode='cover'; let curHead=null, curPart=null; headings=[]; paragraphs=[]; cur=null;
for(i...){
  const t = lines[i].text;
  if(!t){continue?} // blank lines dropped but classified? Blank lines not counted (non-empty only).
  if(paraStart(t)) { start new paragraph }
  else if(labelRe.test(t)) { close heading; mode='heading'; pendingLabel=t; }
  else if(mode==='heading'){ 
     if(isUnlabH(i)){ maybe merge with prev if prev was heading text just consumed... }
```

Hmm merging with previous line is tricky if previous line was already consumed as heading text of the labelled heading. E.g. "A." label, then title wraps "Long title" / "continuation", then... unlabelled heading after a labelled heading title — merge shouldn't grab the labelled heading's text. I'll only merge if the previous line was consumed as paragraph text (i.e., cur paragraph exists and prev line was pushed to it and we can pop it). Track last consumed line index and its classification. Simpler: precompute unlabelled headings before main loop: scan body lines; for each i, if isUnlabH(i): mark i as heading; if line i-1 passes merge test and is not already marked as heading/label and is non-empty → also mark i-1 as heading (and remove it from paragraph text — handle in main loop by checking mark before assigning to paragraph). Precompute a Set of heading-line indices. Also label lines set. Then main loop:

```js
for each non-empty body line i:
  if labelSet: handle heading mode
  else if unlabSet: record heading (text possibly merged: if i-1 in unlabSet, the heading started at i-1 — I'll precompute heading spans: array of {start,end,text,kind})
```

Better: precompute heading spans as objects. For unlabelled: span from start (i-1 if merged) to i. Text = join lines. kind 'unlabelled'; roman spans kind 'roman', letter kind 'letter'. Then in main loop, when line index === span.start, close current paragraph? No—headings occur between paragraphs; a heading line is "never paragraph text". When we encounter a heading span start, set curHead = span (curPart = span if roman). Skip lines in span.

Wait but labelled heading: label line then title lines — span from label to last title line. Title lines determined by: non-empty lines after label until next label/para-start/unlab-start. Precompute all "special" indices: paraStart indices, label indices, unlabStart indices. Then for a label at i: span extends while next non-empty line is not special. Good.

Cover: lines before the first special index (first paragraph start or heading span). 

Paragraph building: on paraStart, close cur, start new {num, lines:[], pages}. Other non-empty, non-heading lines: if cur is null → cover (shouldn't happen after first start). Push line.

Also note: lines between a heading and the next paragraph that aren't part of the heading? E.g. stray. They'd be classified as... my span logic takes all lines until next special, so they become heading text. Fine.

Classification counts: header lines, footer lines, heading lines (span lines), paragraph lines, cover lines. Unclassified: any non-empty body line not in any category — with my scheme everything body is either heading span, paragraph, or cover, so unclassified=0 always. That's fine; check reports it.

Hmm, but "nothing lost" check should be meaningful. Lines that are blank: skipped. Non-empty body lines all classified. OK.

Suspect detection within paragraph lines: for each paragraph, iterate its lines in order; for each line, test suspect patterns; if suspect, mark this line and all subsequent lines of the paragraph with the same page. Note bare-number test must not match paragraph start lines — paragraph start lines are stored without their number? For "/^(\d{1,3})\. (.+)$/" I store the text part as first line. For "/^(\d{1,3})\.$/" the number line itself isn't stored as text (it's just the number). Good.

Suspect patterns:
```js
function suspectLine(t){
  if(/^\d{1,3}$/.test(t)) return true;
  if(/^\d{1,3}\s+[A-Z“"']/.test(t)) return true;
  if(/^[A-Z]{1,4}\/[A-Z0-9]/.test(t)) return true; // UN symbol
  if(/^\*\s/.test(t)) return true;
  return false;
}
```

First words:
```js
function firstWords(text){
  let toks = text.split(/\s+/);
  let out=[];
  for(let k=0;k<toks.length && out.length<6;k++){
    let w=toks[k];
    let prev = out.length?out[out.length-1]:toks[k-1]... 
```
Need previous original token for the digits-alone rule. Iterate with index:
```js
const toks=text.split(/\s+/); const out=[];
for(let k=0;k<toks.length&&out.length<6;k++){
  let w=toks[k];
  w=w.replace(/\d+([.,;:]?)$/,'$1'); // cut trailing digits
  if(/^\d+$/.test(w)){
    const prev=out.length?out[out.length-1]:null;
    const prevRaw = prev ?? toks[k-1];
    if(k>0 && prevRaw && /[.,’”"]$/.test(prevRaw) && !/\b(No|art|para|Vol)\.$/.test(prevRaw)) continue; // drop
  }
  if(w) out.push(w);
}
```
Wait "digits glued to the end of a word or a punctuation mark are cut" — "waste.2"→"waste." ; also "word2"→"word". My regex \d+([.,;:]?)$ keeps punctuation. But careful: real numbers like "17" in "17 Sustainable..." — /^\d+$/ true, prev doesn't end with punctuation → keep. "article 2" — "2" digits-alone, prev "article" doesn't end with . → keep. "No. 3" — prev "No." ends with "." but is abbreviation → keep. Good.

But also first word could have glued digits: "environment1" → "environment". Handled.

Compare: normalize both: replace curly quotes ‘’“” with straight, – — with -, collapse whitespace.

```js
const norm = s=>s.replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
```

Now checks:
1. Paragraph count: found vs ref.paragraphs.
2. Numbering: nums sorted === 1..n; list gaps/dups.
3. First words: mismatch count.
4. Flagged: informational.
5. Suspect lines: informational (count lines, pages, paragraphs).
6. Headers: pages with symbol first line vs all.
7. Footers: pages with page number vs all but first; bare numbers removed listed.
8. Headings: counts, unlabelled listed.
9. Nothing lost: unclassified lines.
10. Export round trip: JSON.parse of the export string, count equals paragraphs found.

Pass/fail set: 1,2,3,6,7,9,10 → pass booleans; 4,5 informational pass=true? For dot count "n of m checks pass": m = total checks; failures = those failing. Informational count as pass. Fine.

Tiles:
- Paragraphs found n, expected ref.paragraphs.
- First words match n of ref.paragraphs.
- Paragraphs flagged n of found, on n pages.
- Footnotes: not separated, ref.footnotes.

Exports: build records:
```js
{symbol, paragraph, section, part, page_start, page_end, text, text_lines, flagged, first_words_match, citation, doc_url, limitations}
```
Plan lists fields: symbol, paragraph, section, part, page_start, page_end, text, flagged, first_words_match, citation, doc_url, limitations. Also mentions export field text_lines ("keeps the original lines for the toggle and the export field text_lines (lines separated by ' | ')"). Include text_lines too.

Markdown: front matter, headings in document order as ##/###, paragraphs. Headings in doc order: I have heading spans with start indices; paragraphs with start indices; merge and iterate.

Flagged-paragraphs table row: Paragraph | Page | Suspect lines | Why. Why: from reasons: "starts with a number and a space", "bare number", "starts with a symbol or quote", "asterisk note", "over 300 words". I'll compute reasons per suspect line type and paragraph word count.

Tab 02 table: No. | Section | Page | First line | Check. Expandable rows: full text with suspect lines marked (thin red box). Suspect lines marked: since text is joined, I'll render paragraph text as sequence of lines: render each line, suspect lines wrapped in span.suspect, joined with spaces (running text). "Show the PDF's lines" toggle shows lines with line breaks and page markers.

Copy citation button.

Clicking flagged row on tab 01: switch to tab 02, expand that paragraph, highlight (scroll into view).

Footer: source, built, disclaimer. pdf_text has no `built`? Description says {title, symbol, doc_url, source, count, records, reference}. No built. Use D.built if present else omit. Plan footer says "source, built". I'll show if present.

Reference missing handling: tiles "no reference in this file", checks "not run".

Exports disabled if no paragraphs.

Let me now write the code, carefully but compactly. Tabs arrow-key nav.

Rail: DOCUMENT card, symbol mono + short title (use D.title). Big numbers: paragraphs found of expected with bar; flagged; checks pass.

OK, writing.

Approx structure JS ~450 lines, CSS ~150, HTML ~80. Fine.

Some details:

Big number bar: width = found/expected*100, red when !=.

Tabs: two buttons, panels with hidden attribute. Arrow keys: keydown on tablist.

Closed headings: button aria-expanded toggling a div.

Row expansion in table: each row is a <tr> plus hidden <tr class="detail">. Buttons: make the first cell content a button? Simpler: row click handled on tr with tabindex=0 and role button? Plan says "Rows are buttons with aria-expanded". I'll make the number cell contain a button styled plain that toggles, and put keydown Enter on tr. Actually simplest: give each row tr a button in first cell with aria-expanded; clicking anywhere on row toggles.

Copy: async navigator.clipboard.writeText with fallback.

Downloads: blob.

Now the "first words differ" list under tiles: paragraphs where mismatch, "para. n: found … / reference …", max 10 lines then "and n more".

Check panel lines: each check: name, values, pass/fail.

Export round trip check: JSON.parse(JSON.stringify(records)) — parse the actual JSON string built for download.

Now write everything.

For the flagged table "Suspect lines" column: show first suspect line text truncated (~60 chars) maybe with count. I'll show the first suspect line's first 60 chars and "+k more" if multiple.

Why reasons mapping:
- bare number → "bare number"
- /^\d{1,3}\s+[A-Z]/ → "starts with a number and a space"
- symbol/quote → "starts with a symbol or quotation mark"
- asterisk → "asterisk note"
- word count > 300 → "paragraph over 300 words"

Let me write the file now.

Also header right: green dot + "n of m checks pass" or red "n checks failed", then "n paragraphs flagged".

Colors: green #1e6b3a.

Time to write. I'll be careful with the edit-free single file.

One more: page count = pages.length. Meta line: symbol link, adopted ref.adopted, "n pages", source.

Handle missing doc_url: link only if present.

Write:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style> ... </style>
</head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<div class="layout">
 <aside>...</aside>
 <main>
  <section id="panel-result" role="tabpanel">...</section>
  <section id="panel-paras" role="tabpanel" hidden>...</section>
 </main>
</div>
<footer>...</footer>
<script> ... </script>
</body>
</html>
```

CSS quickly.

Now the JS pipeline in detail.

```js
const D=window.WORKSHOP_DATA.pdf_text||{};
const pages=(D.records||[]).slice().sort((a,b)=>a.page-b.page);
const SYM=D.symbol||'';
const REF=D.reference||null;
const labelRe=/^([IVX]+|[A-Z])\.$/;
const pAlone=/^(\d{1,3})\.$/;
const pInline=/^(\d{1,3})\. (.+)$/;
function isPS(t){return pAlone.test(t)||pInline.test(t);}

const pageInfos=[]; // {page, lines(raw trimmed), headerIdx, footerIdxs, pageNum, bares:[], warnHeader}
```

Process each page:

```js
for(const p of pages){
  const lines=p.text.split('\n').map(s=>s.trimEnd()); // keep? trim both for compare
```
I'll trim() lines for logic; keep trimmed for display (fine).

```js
  const L=p.text.split('\n').map(s=>s.trim());
  let hi=-1; for(let i=0;i<L.length;i++){ if(L[i]){hi=i;break;} }
  let headerOk=false;
  if(hi>=0 && L[hi]===SYM){headerOk=true;}
  // footer
  const footer=[]; let pageNum=false; const bares=[];
  let i=L.length-1;
  const isDate=s=>/^\d{6}(\s+\d{6})*$/.test(s);
  const isBare=s=>/^\d{1,3}$/.test(s);
  while(i>hi){
    const s=L[i];
    if(!s){i--;continue;}
    if(s.startsWith('GE.')){footer.push(i);i--;continue;}
    if(isDate(s)){footer.push(i);i--;continue;}
    if(isBare(s)){
      if(Number(s)===p.page){pageNum=true;} else {bares.push(Number(s));}
      footer.push(i);i--;continue;
    }
    break;
  }
```
Wait: empty lines at end: `if(!s){i--;continue;}` — but loop must not go past header. Then break at first non-footer line. But the "while" with continue on empty: careful that we don't skip empties then find footer after empties — actually footer lines may be separated by blanks. Continue is right. But break on non-footer non-empty. Good. Note: while(i>hi) — also avoid classifying header line. Edge: header index.

body lines: indices hi+1 .. i (where i is index of last non-footer line... actually after loop, i points at the first line from the end that's not footer/empty; body is hi+1..i inclusive of non-footer region). Body lines = L.slice(hi+1, i+1) but that includes empties — keep empties? For concatenation, blanks are dropped in paragraph text but line indices matter. I'll build a flat body list including empties with page, and skip empties in logic but keep for nothing-lost? Non-empty only counts. Fine — include all, filter non-empty when classifying.

Concatenate bodyLines = [{text,page,li}] across pages.

Then special indices over bodyLines (only non-empty considered):

```js
const N=body.length;
const psIdx=new Array(N).fill(false), labIdx=..., unlabIdx=...;
for(i=0;i<N;i++){
  const t=body[i].text; if(!t)continue;
  if(isPS(t))psIdx[i]=true;
  else if(labelRe.test(t))labIdx[i]=true;
}
// unlabelled
function looksHeading(t){return t && t.length<=90 && /^[A-Z]/.test(t) && !/[.;:,\d]$/.test(t);}
for(i=0;i<N;i++){
  const t=body[i].text; if(!t||psIdx[i]||labIdx[i])continue;
  const nx=body[i+1]&&body[i+1].text;
  if(nx && (isPS(nx)) && looksHeading(t)) unlabIdx[i]=true;
}
// merge: unlab at i, prev non-empty passes looksHeading and not special
const unlabStart=new Array(N).fill(false);
for(i){ if(unlabIdx[i]){ let j=i-1; while(j>=0&&!body[j].text)j--; if(j>=0&&!psIdx[j]&&!labIdx[j]&&!unlabIdx[j]&&looksHeading(body[j].text)&&!/[.!?]$/.test(body[j].text)) unlabStart[j]=true; } }
```
Hmm, merge marks the previous line as heading-start, creating a heading span j..i. But then unlabIdx[j] isn't set; spans: for each unlabIdx[i], span start = unlabStart? find: if some j<i is unlabStart and between j and i only... Simpler: build heading spans directly:

```js
const spans=[];
for(let i=0;i<N;i++){
  const t=body[i].text; if(!t)continue;
  if(labIdx[i]){
    let kind=/^[IVX]+\.$/.test(t)?'roman':'letter';
    let j=i+1; let txt=[];
    while(j<N){
      const s=body[j].text;
      if(!s){j++;continue;}
      if(psIdx[j]||labIdx[j]||unlabIdx[j])break;
      txt.push(s); j++;
    }
    spans.push({start:i,end:j-1,kind,label:t,text:txt.join(' ')||t});
  } else if(unlabIdx[i]){
    let start=i; 
    let j=i-1; while(j>=0&&!body[j].text)j--;
    if(j>=0&&!psIdx[j]&&!labIdx[j]&&!unlabIdx[j]&&!unlabStartUsed[j]&&looksHeading(body[j].text)&&!/[.!?]$/.test(body[j].text)){start=j;}
    spans.push({start,end:i,kind:'unlabelled',text: body.slice(start,i+1).map(x=>x.text).filter(Boolean).join(' ')});
  }
}
```
Careful: the merged previous line j: if it's the last line of a paragraph, popping it from paragraph text. In main loop, I check "is this line index inside a heading span?" via a map. Build spanMap idx→span. Then in paragraph loop, skip lines in spanMap. But the merged line j was pushed to the current paragraph before we reach i... Since I precompute spans, in the main loop I can pop: when starting heading span at i with start<i, the paragraph's last line equals body[start].text — remove it from cur.lines if cur exists and last line matches. Since I precompute, do: before main loop fine — main loop processes sequentially; when I hit index i (unlabIdx) and span.start<i, cur paragraph's lines: pop last (if its text === body[span.start].text and page matches). Implement.

Also labelled heading while cur paragraph open: heading between paragraphs — normally previous paragraph ended. If a labelled heading appears mid-paragraph? "I." alone on a line — a paragraph line could be "I." ? Unlikely. If cur is open when heading starts, close cur (it ends there). OK.

Main loop:

```js
let cur=null, curHead=null, curPart=null;
const paragraphs=[]; const headingsFound=[]; // spans in order
let coverEnd=-1;
const inSpan={};// idx->span
spans.forEach(s=>{for(let k=s.start;k<=s.end;k++)inSpan[k]=s;});
const firstSpecial = first index with psIdx||labIdx||unlabIdx;
for(let i=0;i<N;i++){
  const t=body[i].text; if(!t)continue;
  if(inSpan[i]){ const s=inSpan[i]; if(i===s.start){ if(s.kind==='roman'){curPart=s;} curHead=s; headingsFound.push(s); if(cur&&s.start<i&&s.kind==='unlabelled'){ // pop merged line
      const pl=cur.lines[cur.lines.length-1]; if(pl&&pl.text===body[s.start].text&&pl.page===body[s.start].page){cur.lines.pop(); if(!cur.lines.length){/*empty*/} }
    } }
    continue; }
  if(psIdx[i]){ if(cur)paragraphs.push(cur); const m=t.match(pInline); cur={num:Number(t.match(/^(\d{1,3})\./)[1]), lines:[]}; if(m)cur.lines.push({text:m[2],page:body[i].page}); continue; }
  if(i<firstSpecial){coverCount++; continue;} // cover
  if(cur)cur.lines.push({text:t,page:body[i].page});
  else coverCount++;
}
if(cur)paragraphs.push(cur);
```

Hmm wait: unlabelled span start<i pop: when we reach span start index j (< i)? No — inSpan[j]=span, and i===s.start triggers at j, but we iterate i ascending so we hit j first, not i. Rework: when we encounter index j where inSpan[j] && j===s.start && s.kind==='unlabelled' && s.start<s.end — the merged previous line was body[s.start], which we already pushed into cur. Pop it there. Good: condition s.start<s.end means merged. Pop cur.lines last if matches. 

Also psIdx check order: line could be both? No overlap.

Also for labelled spans with start===i where previous paragraph may be open — that's fine, heading just follows.

But one problem: the merged line j (unlabelled start) was consumed as paragraph line before we knew. Since spans precomputed, at index j we see inSpan[j] → heading handling, pop from cur. Good, handled at j (s.start===j, s.start<s.end → pop). Fix the code above accordingly.

Then paragraph objects: num, lines[{text,page,suspect}], text, page_start/end, section (curHead at time of close — capture section when paragraph starts: cur.section=curHead?curHead.text:null; cur.part=curPart?curPart.text:null). Capture at start.

Suspect marking: after building, per paragraph:

```js
for(const p of paragraphs){
  let reasons=new Set();
  let inPage=null;
  for(const ln of p.lines){
    if(inPage!==null){ if(ln.page===inPage){ln.suspect=true;} else inPage=null; }
    if(!ln.suspect && suspectLine(ln.text)){ ln.suspect=true; ln.why=whyLine(ln.text); inPage=ln.page; }
  }
  p.wordCount=p.text.split(/\s+/).filter(Boolean).length;
  p.flagged = p.lines.some(l=>l.suspect) || p.wordCount>300;
}
```
Careful: after suspect at page X, subsequent lines same page suspect; line on next page resets. But also a later independent suspect on next page starts again. The inPage logic: once set, mark same-page lines; when page changes, clear (set null) — but then a new suspect can set again. However my code: `if(inPage!==null){ if(ln.page===inPage) mark; else inPage=null; }` then check own suspect. Order: mark continuation first, then own check — but if continuation marks it, own check `!ln.suspect` skips. Fine.

p.text = lines joined ' ', collapse double spaces, trim. Note lines already trimmed.

text_lines = lines.map(l=>l.text).join(' | ').

first words compare with REF.first_words.

Now build records for export; checks; render.

Rendering: I'll generate HTML strings.

Tab 02 table rows: tr.main + tr.detail hidden. Toggle.

"Show the PDF's lines" toggle inside detail: a button toggling a div; PDF lines view: lines with <br>, page markers "— p. N —" where line's page differs from previous.

Highlight suspect lines in running text: wrap in <span class="sl">.

Also expansion target from tab 01 flagged row: function openPara(num) → switch tab 2, expand row, scrollIntoView, flash.

Headings found box (closed) on tab 02: list headings with kind.

Number of clickable things tab 01: tabs(2) + 2 export buttons + 2 closed headings = 6. OK.

Tab 02: tabs + headings box = fine (rows don't count).

Export round trip check: build json string, parse, compare length.

Write markdown: headings and paragraphs interleaved. Need ordered items: heading spans have start index; paragraphs — record their start body index. I'll store cur.startIdx=i at creation. Then merge sort.

Markdown structure:
```
---
title: ...
symbol: ...
adopted: ...
source_url: ...
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: n
paragraphs_flagged: n
footnotes: "not separated; the document has N"
---

## I. Introduction
**1.** text

### A. ...
```
Labelled roman → ##, letter → ###, unlabelled → ###? Plan: "the headings as ## and ### lines". I'll use ## for roman, ### for others.

JSON/MD downloads: filename SYM.replace(/\//g,'-') + '.json'/'.md'.

Now write final HTML. Also `[hidden]{display:none!important}`.

Escape HTML for text display.

Let me count checks pass for header dot: checks array of {name, detail, pass (bool|null)}. m = checks where pass!==null? Plan: "n of m checks pass" or red "n checks failed". I'll do: m = all checks; failed = those with pass===false; if failed>0 red "n checks failed" else green "m of m checks pass"? Better: green "n of m checks pass" where n = passing count; red shows "n checks failed". Informational checks pass=true.

Checks needing REF: if missing → "not run", pass=null, excluded from m.

Write it all now. I'll aim for clarity over brevity but keep under limits.

Footer: D.source, D.built (may be undefined — show only if present).

Let me write.