Build the full app per spec. One HTML file. Need to implement pipeline carefully.

Let me plan the code structure:

- Data: D = WORKSHOP_DATA.pdf_text; records sorted by page.
- Parse:
  - For each page: lines = text.split('\n').
  - Header: first non-empty line === symbol → drop; else warn.
  - Footer: from end, drop lines while empty, startsWith "GE.", only 6-digit groups (date stamp like "051125 061125" — consists only of 6-digit groups), or bare number 1-3 digits. Track page number vs displaced footnote numbers. Need to be careful: "051125 061125" — test /^\d{6}( \d{6})*$/. Also bare number: /^\d{1,3}$/.
  - Remaining lines: body lines with page tag.
- Concatenate body lines.
- Classify: cover (before first paragraph start), headings, paragraph lines, footer lines, header lines. Track classification for "nothing lost" check.
- Paragraph start regexes.
- Headings: labelled: /^([IVX]+|[A-Z])\.$/ — open labelled heading; skip blanks; collect lines until next label line or paragraph start. But careful: heading text lines; a line starting lowercase or "(" continues previous heading line? Spec: "a line starting with a lowercase letter or "(" continues the previous heading line". Hmm — wrapped heading titles. Actually simpler: heading lines collected, joined.
- Unlabelled heading: non-empty line immediately followed by paragraph-start line, ≤90 chars, starts with capital, not ending with . ; : , or digit. Two-line joining: when the line before it passes same test and does not end a paragraph sentence... Spec: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading." Hmm, tricky — the line before the unlabelled heading (i.e., two lines before paragraph start) passes the heading test and doesn't end with sentence punctuation → combine. I'll implement: when scanning, if line i is followed by paragraph start, check candidate; also check line i-1: if line i-1 is a heading candidate (≤90, capital start, not ending .;:,digit) AND doesn't end a sentence — hmm "does not end a paragraph sentence" — I'll interpret as not ending with "." (since heading test already excludes .;:,digit for the candidate itself... wait the candidate must not end with . etc.; the previous line test: "passes the same test" — same constraints — "and does not end a paragraph sentence"). To avoid infinite complexity, I'll implement: previous line passes the same capital/length/no-sentence-punctuation test AND current line (the one adjacent to paragraph start)... Actually simplest: when we find a heading candidate line L immediately before a paragraph start, check the previous non-blank line P before it; if P matches the candidate test and the paragraph before... risk: P is the last line of previous paragraph, which typically ends with "." so excluded. If P doesn't end with . , ; : digit — then combine. I'll just do that: P matches test → combine into two-line heading, and P is reclassified from paragraph to heading. Since paragraph lines end with "." normally, safe.

Implementation approach: process concatenated body lines with index. States: cover → then sequence of headings/paragraphs.

Algorithm:
```
i=0; state=cover
while i < lines.length:
  if isLabelledHeading(lines[i]): parse labelled heading
  elif isParaStart(lines[i]): start paragraph
  elif next non-blank line is a paraStart and current line is heading candidate: heading (possibly two-line)
  else: cover or paragraph line
```
Handle blanks skipped. Track heading object {label?, text, part}.

Suspect lines: inside a paragraph, line is suspect when:
- bare number 1-3 digits without full stop, or
- starts with 1-3 digits + space + capital letter, or a UN symbol, or quote mark... spec: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". So regex: /^\d{1,3} [A-Z"“]/ — capital, doc symbol starts with letter like E/... hmm "a UN document symbol or a quotation mark" — "7 E/2003/22" — starts with digit, space, then "E/" which is capital E. OK covered by capital letter. Quotation mark: "2 “Summary...". So /^(\d{1,3}) [\u201c"A-Z]/. Plus starts with "* ".
Then the suspect line and every line after it to end of its page → suspect. Since lines are tagged with pages, mark subsequent lines with same page as suspect. Paragraph >300 words flagged.

First words: strip footnote marks. Tokens split by whitespace. Remove digits glued to end of word or punctuation: replace /(\d+)$/ on tokens... Spec: "digits glued to the end of a word or a punctuation mark are cut ("waste.2" becomes "waste.")". So token like "waste.2" → "waste.". A token that's digits alone is dropped only when previous token ends with ., comma or closing quote and isn't abbreviation (No., art.). Take first six tokens after cleaning.

Wait — also digits glued after word "word2"? "digits glued to the end of a word or a punctuation mark" — e.g. "environment2"? Spec example only shows "waste.2". I'll cut trailing digits from any token ending with digits: "waste.2"→"waste.". But careful "article 2" — token "2" alone handled by drop rule. Tokens like "2030" alone — previous token ends with... e.g. paragraph starting "In 2030, ..." — token "2030," alone-ish; previous token "In" doesn't end with ., comma, quote → kept. OK.

Comparison normalization: curly quotes straight, en/em dashes → hyphen, whitespace runs → single, trim. Compare lower? "case is kept" — keep case.

Checks list: build array of {label, valueA, valueB, pass, detail}.

Export JSON & Markdown via Blob.

Tab 02: table with expandable rows, copy citation, "Show the PDF's lines" toggle.

Left rail with big numbers.

Header with green/red dot.

Tabs with arrow keys, role tablist.

Keep under ~1500 lines. Let me write it.

Line classification counts for "nothing lost": every non-empty line classified once: cover, header, heading, paragraph, footer. I'll track a classification per non-empty line.

Let me carefully structure parse:

```js
const D = WORKSHOP_DATA.pdf_text;
const pages = [...D.records].sort((a,b)=>a.page-b.page);
const symbol = D.symbol;
let headersDropped=0, headerWarn=[], pageNumPages=[], bareNums=[];
const bodyLines = []; // {page, text, cls}
pages.forEach(pg => {
  const lines = pg.text.split('\n').map(l=>l.replace(/\r$/,''));
  // header
  let firstIdx = lines.findIndex(l=>l.trim()!=='');
  ...
```

Non-empty lines list per page. Let me collect nonEmpty = lines with indices. Header = first nonEmpty; if === symbol drop, else warn.

Footer scan from end of the nonEmpty array: while last matches footer pattern, pop and classify. Footer patterns: empty (not in nonEmpty), /^GE\./, /^\d{6}( \d{6})*$/, /^\d{1,3}$/. Record: if bare number equal to page → page number; else bare number list.

But wait — could a footer scan eat body text? Body lines are prose; unlikely to match those patterns except... a bare number line in body (displaced footnote number at foot of page) — spec says footnotes sit at foot before footer, and those are "suspect lines" that stay in paragraphs. Hmm! Conflict: on 12 pages a bare number sits in the footer per "What I found" — "On 12 pages a third bare number sits in the footer: a footnote number the converter displaced." So the footer scan removes it. But suspect-line rule says bare numbers inside paragraphs are suspect. Those are different occurrences — some displaced numbers ended up in footer region (removed), some inside body (suspect). Fine — follow spec: footer scan removes from the end; bare numbers within body stay and are suspect.

But careful: footnote blocks sit "at the foot, before the footer". Their first line is a bare number, blank, then text. The footer scan from the end would remove footer lines but stop at footnote text (prose). Except the bare-number footnote marker line... it's before the text, so not at the very end. OK. But wait — footnote text itself is body and gets concatenated into paragraphs — that's the flagged content. Right, "footnotes not separated, they stay in text".

Hmm but footnote first is "bare number on its own line, a blank line, then the text" — that bare number inside body is a suspect line (bare number rule). Good.

Risk: footer scan could eat a bare number that is a displaced footnote number sitting after the last footnote text line — that's exactly the described behavior ("bare number removed from the footer"). Fine.

Body lines = middle. Concatenate in page order. Then classification pass.

Cover lines: before first paragraph start AND not headings — cover is everything before first para start (excluding labelled headings? Cover comes before first heading too typically). Spec: "Lines before the first paragraph start are the cover." I'll classify all body lines before the first paragraph-start line (excluding any heading parsing? There are no headings before first para in this doc presumably). Simple: cover = body lines before first paragraph start index (non-empty ones). Actually headings before first paragraph would be cover too; fine.

Main loop over bodyLines (skip blanks but keep index):

```js
let paras=[], headings=[], coverCount=0;
let current=null; // current paragraph
let i=0, first=true;
const isPS = l => /^(\d{1,3})\.$/.test(l) || /^(\d{1,3})\. /.test(l);
```
Wait, /^(\d{1,3})\. (.+)$/ — needs content.

Labelled heading: /^([IVX]+|[A-Z])\.$/.

Loop:
```
while(i<body.length){
  const line=body[i];
  if(!line.text.trim()){i++;continue;}
  if(isLabel(line)){ collect labelled heading: skip blanks; heading lines until next label/paraStart/EOF; lines starting lowercase or "(" append to previous heading line (continuation). Mark these as heading class. store heading {type:'labelled', label, text, part if roman}. continue;}
  if(isPS(line)){ start new paragraph; mark; }
  else {
    // check unlabelled heading: line followed (next non-blank) by paraStart
    if(nextNonBlankIsParaStart(i) && isHeadingCandidate(line.text)){
       // maybe two-line
       let h=[line.text];
       let start=i;
       const prev = prevNonBlank(i);
       if(prev && isHeadingCandidate(prev.text) && !/[.;:,]$/.test... hmm "does not end a paragraph sentence"
```

Hmm the two-line rule: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading." The line before the candidate. isHeadingCandidate already excludes ending with .;:,digit. "does not end a paragraph sentence" — I think for the previous line, since it passes the same test (which excludes . ; : , digit endings), "does not end a paragraph sentence" maybe means the previous-previous context... I'll interpret: prev passes candidate test AND the current candidate line — hmm. Simpler: prev passes the same test (which includes not ending with .;:,digit) → combine. Since the test itself excludes sentence-ending punctuation, "does not end a paragraph sentence" is nearly redundant. But risk: prev could be the last line of a paragraph not ending with punctuation? Paragraphs end with "." normally. I'll combine when prev is candidate and prev was classified as paragraph line of the previous paragraph and doesn't end with [.]. Keep it simple: combine if prev exists, isHeadingCandidate(prev), and prev ends with no sentence punctuation (test already ensures). Also prev must belong to the previous paragraph (already emitted lines) — I need to remove it from that paragraph. Implementation: paragraphs store line indices; when combining, pop the last line from current paragraph and reclassify as heading.

Let me restructure: process sequentially, maintain `cur` paragraph with array of line refs. When unlabelled heading found at i with possible prev at j (prev non-blank index), if combining: remove body[j] from cur's lines (if it was the last line) and mark class heading.

Heading text join: join with space.

After heading parse, continue; next para start assigns section = last heading, part = last roman labelled heading.

Suspect computation: after paragraphs built, for each paragraph, iterate lines; if line matches suspect pattern → mark it and all subsequent lines in same paragraph with same page... spec: "A suspect line and every line after it to the end of its page are suspect" — within the paragraph's lines (lines after on that page). Since paragraph lines are ordered, mark line and all following lines whose page equals that line's page? "to the end of its page" — I'll mark subsequent lines with page === suspect line's page (lines after in the paragraph on same page). Actually footnote block runs to foot of page; the paragraph's remaining lines on that page are suspect. If paragraph continues to next page, those next-page lines aren't suspect. Good: mark while line.page === s.page.

Word count >300 → flagged.

Wait — but paragraphs that span pages with footnotes: the paragraph's lines on the earlier page after the suspect line get marked. Fine.

First words: computed as spec.

Now checks:
1. Paragraph count: found vs reference.paragraphs.
2. Numbering: exactly 1..n in order; gaps/dups listed.
3. First words: count mismatches.
4. Pages flagged: n pages, n paragraphs.
5. Suspect lines: counts.
6. Headers/footers: pages with symbol first line (expected all), pages with page number (expected all but first), bare numbers removed with pages.
7. Headings: labelled count, unlabelled count with list.
8. Nothing lost: sum of classified non-empty lines === total non-empty; unclassified listed.
9. Export round trip: JSON.parse of export string; count equals table.

m = 9 checks; pass count.

Header dot: green "n of m checks pass" if all pass, else red "n checks failed". Then "n pages flagged".

Now UI. Tabs 01/02. Tab 01: 4 tiles, mismatch list, download buttons, two closed headings (Every check, Flagged pages). Tab 02: headings-found closed box + table.

Flagged pages table: rows Page | Paragraph | Suspect lines | Why; click expands raw lines of that page with suspect highlighted, showing which paragraph. Raw lines of the page: I need original page lines including header/footer? Show "the page's raw lines with the suspect ones highlighted and the paragraph they sit in". I'll show body lines of the page with page/tag info; highlight suspect ones. Show paragraph number annotation. Keep simple: list lines, suspect ones with red box and "→ para. n".

Tab 02 rows: No | Section | Page | First line | Check. Expand: full text with suspect lines marked — but text is joined running; to mark suspect lines within running text I can render the paragraph's lines, joining non-suspect into running text and suspect as marked spans? Spec: "The expanded paragraph is one block of running text" with suspect lines marked. I'll build: iterate lines, accumulate running text; when a suspect line occurs, flush and emit a marked span with that line, continue. Subsequent suspect lines too. Result reads as running text with red-boxed fragments. Good enough.

Also "Show the PDF's lines" toggle: show lines joined with " | "? Spec: "reveals the same text with the converter's line breaks and the page number where each page began". Render each line on its own line (or " | "? no, that's the export). Render lines with <br> or as block lines; prefix "[p. N]" where a new page begins. I'll render lines as divs, with "[p. N]" marker at page changes.

Copy citation button.

Exports: JSON fields: symbol, paragraph, section, part, page_start, page_end, text, flagged, first_words_match, citation, doc_url, limitations, text_lines (lines joined " | "). Spec listed text_lines in computation section ("the export field text_lines (lines separated by ' | ')").

Markdown: front matter, headings as ## / ### in document order interleaved with paragraphs. I have headings list with order and paragraphs with section/part. To interleave in document order, keep a combined ordered list during parsing: push headings and paragraphs into `docOrder`. Headings: labelled (roman → ##, lettered → ###) and unlabelled (###? spec: "the headings as ## and ### lines in document order" — labelled roman = ##, lettered subsection = ###, unlabelled = ###). I'll do: roman labelled → ##, others → ###.

Also headings box on tab 02 lists all headings found.

Edge: no reference → tiles say "no reference in this file", checks "not run". I'll implement hasRef checks.

Design: CSS per studio palette.

Let me now write the file. Aim ~700-900 lines.

Data structures:

```js
const D = WORKSHOP_DATA.pdf_text;
const ref = D.reference || null;
const pages = [...(D.records||[])].sort((a,b)=>a.page-b.page);
```

Parsing:

```js
const RE = {
  bareNum: /^\d{1,3}$/,
  dateStamp: /^\d{6}( \d{6})*$/,
  paraAlone: /^(\d{1,3})\.$/,
  paraSame: /^(\d{1,3})\. (\S.*)$/,
  label: /^([IVX]+|[A-Z])\.$/,
  suspectNum: /^\d{1,3} [A-Z\u201c"]/,
  suspectBare: /^\d{1,3}$/,
  star: /^\* /
};
```

Footer removal per page: work on array of {text, cls} for all lines including blanks? I'll process lines per page:

```js
pages.forEach(pg=>{
  const raw = pg.text.split('\n');
  const items = raw.map(t=>({page:pg.page, text:t.replace(/\s+$/,''), cls:null}));
  // header
  let fi = items.findIndex(x=>x.text.trim()!=='');
  if(fi>=0 && items[fi].text.trim()===symbol){items[fi].cls='header';headersOk.push(pg.page);} else headerWarn.push(pg.page);
  // footer
  for(let k=items.length-1;k>=0;k--){
    const t=items[k].text.trim();
    if(t==='') continue; // don't classify blanks, skip? but loop from end must stop at non-footer non-empty
    if(t.startsWith('GE.')||RE.dateStamp.test(t)||RE.bareNum.test(t)){
      items[k].cls='footer';
      if(RE.bareNum.test(t)){ if(String(pg.page)===t) pageNumbers.push(pg.page); else bareFooter.push({page:pg.page,num:t}); }
    } else break;
  }
  body.push(...items.filter(x=>x.cls===null));
});
```

Wait — blanks in footer region: loop from end skipping blanks; if line matches footer pattern classify; else break. But blanks between footer lines are fine (not classified, not counted in non-empty totals). But if a blank sits between body and footer, fine.

Hmm — careful: date stamp "051125 061125" — two 6-digit groups. Regex ok.

Then non-empty classification counts: total non-empty lines = raw lines with trim()!=='' across pages. Classified: cls in {header, footer, cover, heading, paragraph}. Anything with cls null and non-empty at end → unclassified.

Cover: body lines before first paragraph-start (non-empty ones) — but also labelled headings before? Assign in main loop: if no paragraph started yet and line isn't heading → cover.

Main loop:

```js
let cur=null, lastHeading=null, lastPart=null;
const order=[]; // {kind:'h',h} or {kind:'p',p}
let i=0;
const B = body; // includes blanks
function nextNonBlank(k){for(let j=k+1;j<B.length;j++) if(B[j].text.trim()!=='') return j; return -1;}
function isPSat(k){const t=B[k].text.trim(); return RE.paraAlone.test(t)||RE.paraSame.test(t);}
function cand(t){return t.length>0&&t.length<=90&&/^[A-Z(]/.test(t)&&!/[.;:,\d]$/.test(t);}
```
Hmm heading candidate: "starting with a capital letter" — allow "(" ? Spec says capital letter. But "Right to work (art. 6)" starts with R. Keep /^[A-Z]/. But not ending with .;,:,digit.

Loop:

```js
while(i<B.length){
  const t=B[i].text.trim();
  if(t===''){i++;continue;}
  const lm=t.match(RE.label);
  if(lm){
    // labelled heading
    let j=i+1, hlines=[];
    while(j<B.length){
      const tj=B[j].text.trim();
      if(tj===''){j++;continue;}
      if(RE.label.test(tj)||isPStext(tj)) break;
      hlines.push({idx:j,text:tj});
      j++;
    }
    // merge continuation lines starting lowercase or "(" into previous
    ...
```
Continuation: "a line starting with a lowercase letter or "(" continues the previous heading line" — append to previous heading line. I'll implement: build merged list.

Hmm wait, but this greedy collection "every line up to the next label line or paragraph start is heading text" — could swallow unlabelled headings between? Unlabelled heading sits "on the line or two lines just before a paragraph number" — so it's within this collected text, ends just before paragraph start. That's fine, it becomes heading text anyway. But the unlabelled heading should become its own heading (a ### separate from the section). Hmm. For section attribution it matters little (nearest heading). For the "Headings found" box and markdown ###, we'd want it separate. Simplify: during collection, if the last line(s) before paragraph start form an unlabelled heading candidate, treat as its own heading. Implementation: after collecting hlines, check if the last collected line passes cand() and next non-blank is para start → split it off as unlabelled heading (with two-line check). Let me implement that.

Actually simpler architecture: do a single pass where I handle:

- labelled heading start: collect its text lines until next non-blank which is label or PS. During collection, before finishing, check trailing unlabelled heading.

Alternatively, restructure: first pass marks paragraph starts; second pass: for each non-blank non-PS line, if next non-blank is PS and cand → unlabelled heading (with prev-line merge). Then labelled headings collected. Let me just do the sequential loop with careful code. It's fine.

Let me write parse code fully in final file. I'll write it now directly.

For labelled heading collection, merging: hlines array; for each, if starts with lowercase or "(" and hlines.length>0, append to last with space; else push. Also two-line unlabelled within labelled collection — skip, acceptable.

Trailing unlabelled split: after building merged hlines (indices tracked), if last merged line's next non-blank (after its idx) is a PS and cand(lastline) → pop it as unlabelled heading (and check its own prev merge? within labelled heading context — skip).

Unlabelled heading handling in main loop (when not in labelled heading): line at i, next non-blank is PS, cand(t):
```js
let h=[t], idxs=[i];
const p = prevNonBlank(i);
if(p>=0 && B[p].cls===null or paragraph... && cand(B[p].text.trim()) && !endsSentence){
```
Hmm — prev passes same test (cand already excludes .;:,digit endings, so "does not end a paragraph sentence" automatic-ish). But wait — danger: prev is last line of previous paragraph that happens to be short and capital... e.g. a paragraph ending "...under article 6" — ends with digit, excluded. Paragraphs end with "." mostly. But two-line headings wrap: "The right of everyone to the enjoyment of just" + "and favourable conditions of work" — second line starts lowercase! Hmm — "whose title can wrap over two lines" — and unlabelled heading like "Right to work (art. 6)" one line, the one before para 73 wraps two lines. If second line starts lowercase, my cand test (capital start) fails! E.g. heading line 1 "Some long heading about" line 2 "children's rights"? The spec for two-line: "when the line before it passes the same test" — the line before the candidate. So candidate = line immediately before PS starting with capital; line before that passes the same test. Hmm but wrapped headings often have lowercase second lines... The plan says this rule; the data: "the one before paragraph 73 wraps over two lines". I'll trust the plan: both lines pass the capital-start test apparently. Also labelled headings handle lowercase continuation separately. OK, follow plan.

So: if cand(t) and next is PS → candidate. Then check prev non-blank p: if p is a paragraph line (belongs to cur paragraph, or is cover?) and cand(prev) → merge: remove prev from cur's lines, classify as heading.

But careful: what if prev is itself the previous unlabelled heading... whatever.

Also need: "does not end a paragraph sentence" — since cand excludes .;:,digit endings, a paragraph last line ending "." fails cand. Good enough; I'll also require prev's next non-blank is i (adjacency) — trivially true.

Risk: false merges when a paragraph's last line is like "See also A/HRC" — ends with capital letter and no period? Unlikely; accept.

When heading found: set lastHeading={type, text}; if labelled roman → lastPart. Push to order.

Paragraph start: if paraAlone → cur={num, lines:[]}; next lines added. If paraSame → first line is the text after; cur={num, lines:[{page, text: rest}]}. Mark cls 'paragraph'.

Other non-empty lines: if cur → paragraph line (cls 'paragraph'); else cover (cls 'cover').

After parsing: for each paragraph, text = lines joined ' ', collapse double spaces, trim. flagged: suspect logic + word count>300. first words compare.

Numbering check: nums sequence.

Now rendering. I'll write render functions for tab1 and tab2, checks array.

Check items store: {name, expect, got, pass (bool|null), note}. For not-run when ref missing.

Checks:
1. Paragraph count: got=paras.length, expect=ref?.paragraphs.
2. Numbering: expect "1–n in order", got: ok or list of gaps/dups.
3. First words: got `${match} of ${paras.length} match`, expect ref.paragraphs. pass = all match.
4. Pages flagged: informational — pass=null? Spec: "A flag is not a failure". I'll mark pass=true always with note. Or treat as pass with note. Make it pass=true but note describes. Hmm "n of m checks pass" — count it as pass. I'll set pass true, note explains.
5. Suspect lines: pass=true, note counts.
6. Headers/footers: expect all pages symbol-first; got count. Also page numbers all but first; bare numbers list. Combine into one check: pass = headersOk.length===pages.length && pageNumPages.length===pages.length-1.
7. Headings: pass=true, note lists unlabelled.
8. Nothing lost: pass = unclassified.length===0 and sums match.
9. Export round trip: JSON.parse(exportString).length === paras.length.

Failed check links to rows concerned — keep simple: note text includes paragraph numbers.

Now the "Every check" panel: one line per check with values.

Flagged pages data: group flagged paragraphs' suspect info by page: for each page, list of {para, line, why}. Why: "bare number" / "starts with a number and a space" / "starts with an asterisk" / "paragraph over 300 words". For the over-300 case, no line — mark why separately; page flagged? Spec: "A page is flagged when it has a suspect line inside a paragraph". Over-300 flags the paragraph, not the page. OK.

Flagged pages table rows: page | paragraphs | suspect lines count | why (joined reasons). Click → expand: page raw lines (all lines of the page incl. header/footer? show body lines + header/footer maybe). I'll reconstruct: store per-page all lines with cls and suspect marks. Simpler: store pageLines map: page → array of {text, cls, para, suspect}. Suspect determined after paragraph parsing — lines store refs, so I can mark the same objects. Body line objects are shared; page raw lines include header/footer items too — I discarded those from body but can keep a per-page full list. Let me keep `pageAll = {}` mapping page → array of line objects (all with cls; body ones are same objects as in B). Then expansion renders pageAll[page].

Suspect marking on line objects: line.suspect=true, line.para=cur.num.

Export round trip check computed on demand at build time (generate JSON string once).

Markdown: 
```
---
title: ...
symbol: ...
adopted: ...
source_url: doc_url
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: n
pages_flagged: n
footnotes: "not separated; the document has N"
---
```
Then order: headings ## / ###, paragraphs "**n.** text (flagged: may contain footnote text)".

Tab 02: table with caption, expandable rows.

Copy citation: navigator.clipboard may fail in sandbox; fallback textarea+execCommand. Show "Copied" 2s.

Keyboard tabs: arrow keys, hidden panels with hidden attribute + [hidden]{display:none!important}.

Let me count clickable things on tab 01: 2 download buttons + 2 closed headings = 4 ✓. Tab 02: headings box = 1 ✓.

Write the code now. Also footer with source, built, and honesty line. Note: D.built exists? pdf_text has {title, symbol, doc_url, source, count, records, reference} — no built. Footer says source, built — I'll show source and count, or omit built if missing. Spec footer: "`source`, `built`". pdf_text description doesn't include built. I'll show source and pages count; guard built with fallback "—".

Let me write.

Approx CSS: studio palette.

Now writing HTML.

Key functions:

```js
function normFW(s){return s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201c\u201d]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();}
function firstWords(text){
  const toks=text.split(/\s+/);
  const out=[];
  const ABBR=/^(No|art|Arts|para|paras|vol|p|pp|No)\.$/i;
  for(let k=0;k<toks.length&&out.length<6;k++){
    let t=toks[k];
    const prev=out.length?out[out.length-1]:toks[k-1]||'';
    if(/^\d+$/.test(t)){
      const pv=out[out.length-1];
      if(pv!==undefined && /[.,"\u201d]$/.test(pv) && !ABBR.test(pv)) continue; // drop
      out.push(t); continue;
    }
    t=t.replace(/\d+$/,''); // trailing digits glued
    if(t) out.push(t);
  }
  return out.join(' ');
}
```
Hmm "digits glued to the end of a word or a punctuation mark are cut" — "waste.2"→"waste.". Also "waste2"→"waste". Use replace(/\d+$/,''). But careful with real numbers "2030:" — token ends with ":" not digits, fine. Token "2." (number with period, a real numbered list?) — /^\d+$/ doesn't match "2.". "2." would be... trailing digits cut: "2." → "2." (ends with "."). Hmm "2." stays "2." — edge; fine.

Drop rule: token of digits alone dropped only when the token before it ends with ., comma or closing quote and is not abbreviation. "before it" = the token before in the original stream. If it's the first token, no previous → keep. E.g. "article 2 and" → "2" preceded by "article" (no .,) → kept. "No. 3" → prev "No." is abbreviation → kept. Good, my code checks out[out.length-1] — but that's after cutting... prev token "waste." after cut from "waste.2" is "waste." ends with "." — would wrongly drop a following digits token. Edge; acceptable. Actually better use original previous token toks[k-1]. Let me use toks[k-1] for the drop decision (uncut original). Spec: "the token before it" — original token. Use toks[k-1].

Compare: normFW(found) === normFW(ref first_words).

Mismatch records: para.number, found FW, ref FW.

Now the main parse loop details for labelled headings. Code:

```js
while(i<B.length){
  const raw=B[i].text, t=raw.trim();
  if(t===''){i++;continue;}
  const lm=t.match(RE.label);
  const ps=t.match(RE.paraAlone), ps2=t.match(RE.paraSame);
  if(lm){
    let j=i+1, hparts=[]; // {idx, text}
    while(j<B.length){
      const tj=B[j].text.trim();
      if(tj===''){j++;continue;}
      if(RE.label.test(tj)||RE.paraAlone.test(tj)||RE.paraSame.test(tj)) break;
      hparts.push({idx:j,text:tj}); j++;
    }
    // merge lowercase continuations
    let merged=[];
    hparts.forEach(h=>{
      if(merged.length && (/^[a-z]/.test(h.text)||/^\(/.test(h.text))) merged[merged.length-1].text+=' '+h.text;
      else merged.push({...h});
    });
    // trailing unlabelled split
    let unl=null;
    if(merged.length){
      const last=merged[merged.length-1];
      const nn=nextNonBlank(last.idx);
      if(nn>=0 && isPSidx(nn) && cand(last.text)){ unl=merged.pop(); }
    }
    const label=lm[1];
    const h={type: label.length>1||/[IVX]/.test(label)&&label!=='I'? ... }
```
Roman vs single letter: label "I." is roman too; single capital A-Z. Distinguish: /^[IVX]+$/.test(label) → roman (I, V, X combos); else letter. Note "I." is roman. So roman = /^[IVX]+$/.test(label).

Set cls 'heading' on merged line idxs (and hparts original idxs — merged objects keep idx of first; continuation lines idx lost!). I need to classify all hparts lines. Keep track: mark all hparts idx as heading. Merged text for display.

If unl: create unlabelled heading after labelled one; mark its idx heading. Also two-line merge for unl inside labelled? skip.

lastHeading = unl || labelled heading (nearest = unl if exists since it comes after). Push both to order: labelled then unl.

Set i = j (index of breaking line) — but careful the unl came from within; fine.

  }
  else if(ps||ps2){
    start paragraph: cur={num:+(ps||ps2)[1], lines:[], startIdx:i};
    B[i].cls='paragraph';
    if(ps2){cur.lines.push({page:B[i].page,text:(ps2)[2]});}
    order.push(cur); paras.push(cur);
    i++;
  }
  else {
    const nn=nextNonBlank(i);
    if(nn>=0&&isPSidx(nn)&&cand(t)){
      // unlabelled heading, maybe two-line
      let hIdxs=[i], hText=t;
      const p=prevNonBlank(i);
      if(p>=0&&cand(B[p].text.trim())&&cur&&cur.lines.length&&cur.lines[cur.lines.length-1]._idx===p){
        // remove p from cur
        ... 
```
Hmm — I need cur.lines to track body indices. Let me store lines as {page, text, idx}. For the ps2 case idx=i. When adding paragraph lines: {page, text:t, idx:i}.

Two-line merge condition: p is the last line of cur (idx matches) and cand(prev) → merge. Then cur.lines.pop() (that line becomes heading). But cur.lines last element should be the line at p only if no blank between... prevNonBlank(i) returns p, and if cur's last line idx === p. If cur's last line is earlier (blank between), still could merge? Heading followed by blank then paragraph start — possible. I'll allow: if p >= cur.lastIdx (i.e., p is after cur's last line) and cand → but then the popped line isn't in cur; just classify p as heading. Simpler condition: p>=0 && cand(B[p].text.trim()) && B[p].cls!=='heading' && (cur===null || cur.lines.length===0 || cur.lines[cur.lines.length-1].idx <= p). And "does not end a paragraph sentence": cand excludes those endings anyway.

Hmm but risk of merging a cover line. Fine.

      hText = B[p].text.trim()+' '+t; hIdxs=[p,i];
      mark heading.
    }
    lastHeading={type:'unlabelled', text:hText};
    order.push heading; mark cls.
    i++;
  }
  else {
    if(cur){cur.lines.push({page:B[i].page,text:t,idx:i}); B[i].cls='paragraph'; B[i].para=cur.num;}
    else {B[i].cls='cover';}
    i++;
  }
```
Wait — the paragraph-line push also needs B[i].para set for flagged-page expansion. Set in both places. Also ps2 first line: B[i].para=cur.num.

Also note: labelled heading collection loop breaks at label or PS; lines before it classified heading. What about unlabelled heading NOT inside a labelled block (i.e., appears when previous context is a paragraph)? Handled by main loop branch. Good.

Also careful: labelled heading branch when label appears before first paragraph (cover region)? Headings exist after intro presumably; handle anyway.

Suspect pass:

```js
paras.forEach(p=>{
  let suspect=false;
  p.lines.forEach((ln,k)=>{
    const t=ln.text;
    if(RE.suspectBare.test(t)||RE.suspectNum.test(t)||RE.star.test(t)){
      suspect=true; p.suspectFrom=ln;
    }
    if(suspect&&ln.page===...)
```
Marking: once a suspect line found, mark it and all later lines in same paragraph with same page. Implementation:

```js
let susPage=null;
p.lines.forEach(ln=>{
  if(susPage===null){
    if(isSuspectLine(ln.text)){susPage=ln.page; ln.suspect=true; ln.why=whyOf(ln.text);}
  } else if(ln.page===susPage){ln.suspect=true;}
});
```
Hmm but ln.suspect should also mark when a later separate suspect starts on a later page — susPage reset when page changes? If paragraph continues to next page, lines on next page aren't suspect (footnote ended). But a new footnote could start on that next page. So:

```js
let susPage=null;
p.lines.forEach(ln=>{
  if(susPage!==null && ln.page!==susPage) susPage=null;
  if(susPage===null && isSuspect(ln.text)){susPage=ln.page;}
  if(susPage!==null){ln.suspect=true; if first mark why}
});
```

flagged = any suspect || wordCount>300 (why "paragraph over 300 words"). flagged pages: pages of suspect lines (only suspect, not wordcount). Collect set.

Suspect lines stats: count lines with suspect && isSuspect origin... count all marked lines? Spec: "n suspect lines on n pages, in n paragraphs". I'll count lines that are marked suspect (including trailing ones after origin? Those are "suspect" too as marked). Hmm, the check "Suspect lines. n suspect lines on n pages" — count marked lines. Fine.

Checks data. Let me also compute:
- hyphen-ending lines count (report in nothing-lost note or a small note). "the app counts such lines anyway and reports the number" — put in check 5 note or check 8. I'll add to suspect-lines check note.

Export JSON: build array; limitations: flagged ? `footnotes not separated; ${suspectOriginCount? } may sit inside this paragraph` — spec: "footnotes not separated; n may sit inside this paragraph" for flagged — n = number of suspect-origin lines? I'll use count of marked suspect lines in that paragraph. Or origins. I'll use number of suspect lines marked. Hmm "n may sit inside" — number of footnotes maybe. Use origin count (number of suspect starts). I'll use count of marked lines... ambiguous; use number of suspect origins in the paragraph. Keep origins per para: p.suspectOrigins.

Citation: `${symbol}, para. ${num}`.

Now build the UI HTML. I'll generate mostly via JS into containers.

Let me write the file now, carefully but compactly.

Tab arrow-key nav: standard.

Rendering tab 02 table rows: build with DOM. For ~90 rows fine.

Expanded row content: running text with suspect marked: iterate p.lines; group consecutive non-suspect into running string; suspect lines individually in <mark class="sus">. Build HTML with escaping. Then ref FW vs found FW, "Show the PDF's lines" toggle button (aria-expanded), hidden div with lines: for each line, if page changed since last, prefix "[p. N]"; line text; suspect lines red box. Copy citation button.

Escape HTML helper.

First line display: text.slice(0,120) cut at word + "…".

OK, writing final answer. Also "at most three short sentences" before code block.

For the round trip check: generate jsonString once at load; check JSON.parse length.

Date: new Date().toISOString().slice(0,10).

File names: symbol.replace(/\//g,'-').

Let me write it.

For checks panel lines: each: name, "expect: X", "got: Y", pass badge.

Let me now write everything.

One more detail: header line "n pages flagged" etc. Dot color: green if all checks pass else red. Text: pass all → "n of m checks pass"; else "k checks failed".

Rail big numbers: paragraphs found of reference (bar: width = min(found/ref,1)*100; red when != ref); pages flagged; checks pass.

Nothing-lost check: count non-empty raw lines total; classified per kind; sum; unclassified list (cls null and non-empty and not blank). Note: non-empty lines with cls null after parse → unclassified. Should be zero since main loop classifies everything. Good.

Wait: cover lines — classified 'cover'. In "sum to total" the kinds are cover, header, heading, paragraph, footer. OK.

Numbering check: expected 1..paras.length in order; compute gaps (missing numbers between 1 and ref.paragraphs?) — "Exactly 1 to n in order; gaps and duplicates listed by number and page." Check sequence strictly increasing by 1 from 1. Report deviations.

First words mismatch list on tab 01 under tiles (max 10 lines).

Alright, write it. I'll aim for clean, complete code.

For the flagged-pages expansion raw lines: pageAll[page] = all line objects of that page (I'll build during page processing: keep a reference list). Body objects shared. Header/footer objects have cls set. Render each line: text, and if body & suspect → red box + "→ para. n"; if body & paragraph cls → small "para. n" tag maybe. Show all lines including blanks? Show non-empty plus blank as empty? I'll show all lines trimmed-right; blank lines render as empty rule. Keep simple: render only lines with text or show all. I'll render all lines, blanks as subtle.

Simpler: render non-empty lines only, in order, each with left tag of nothing. Highlight suspect. That satisfies "the page's raw lines with the suspect ones highlighted and the paragraph they sit in".

Now writing final code. Estimate ~850 lines.

CSS: 
- body bg #f4f0e8, text #1d1b18, rules #d9d2c3, accent #9b2335, pass green #1e6b3a.
- header sticky? just top.
- layout: header, tabs, main grid (rail + content).

Let me write.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>...</title>
<style> ... </style>
</head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<div class="layout">
  <aside id="rail">...</aside>
  <main>
    <section id="panel1" role="tabpanel">...</section>
    <section id="panel2" role="tabpanel" hidden>...</section>
  </main>
</div>
<footer>...</footer>
<script> ... </script>
</body>
</html>
```

Rail fills via JS.

Write the JS pipeline as planned. Let me be careful with `count` being string "20" — use records length.

Time to write final.

For tiles: 4 tiles in a grid.

Buttons download: create blob, a.click().

Copy: async with fallback.

OK writing now, final output.