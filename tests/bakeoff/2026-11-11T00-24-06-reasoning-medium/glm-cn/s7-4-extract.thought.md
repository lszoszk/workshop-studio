Build the full app per plan. Need a single HTML document. Let me write it carefully but concisely, following the pipeline.

Key components: header, left rail, tabs 01/02, parsing pipeline, checks, exports, expandable rows, suspect highlighting, copy citation.

Let me plan the code structure:

- Parse: records sorted by page. For each page: split text into lines.
  - Header: first non-empty line equals symbol → drop, count; else warning.
  - Footer: from end, drop while empty, GE., date stamp (only 6-digit groups), bare number 1–3 digits (record if not page number).
  - Body lines with page tags.
- Concatenate body lines. Track page per line.
- Find paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.
- Classify lines: cover (before first para start), heading lines, paragraph lines, footer lines, header lines. For "nothing lost" check need every non-empty line classified exactly once. Note: lines before first paragraph start are "cover" — but headings only appear after? Plan says "Lines before the first paragraph start are the cover." So cover includes everything before first paragraph. Headings detection: labelled heading lines matched during scan. But headings occur after first paragraph (paragraph 1 comes before first heading maybe). Actually paragraph 1 is in Introduction after heading "I." — hmm, "I." heading comes before paragraph 1. Plan says lines before first paragraph start are cover. So "I." and "Introduction" would be cover? Wait — the heading "I. Introduction" comes before paragraph 1 in the document... Actually the sample shows page 1: title stuff, then "I." then "Introduction" then "1." So heading I appears before paragraph 1, thus classified as cover. Hmm, but then paragraph 1's part would be missing. But plan says part = most recent roman heading. If "I." is classified as cover, paragraph 1 has no part. Alternatively, process headings from body lines including before first paragraph start, and "cover" is only lines before... plan explicitly: "Lines before the first paragraph start are the cover." Follow the plan literally. Cover lines include title lines, "I.", "Introduction". Paragraph 1's section will be "" then. Fine — follow plan.

Actually wait — labelled heading detection: while scanning body lines in order, when we see /^([IVX]+|[A-Z])\.$/ we open a labelled heading. But if it's before first paragraph start it's cover. Hmm. The classification: "Every non-empty line of every page is classified exactly once as cover, header, heading, paragraph or footer". So cover takes precedence before first para start. So scan: iterate lines; before first para start → cover. After: check heading rules, para start rules, else paragraph text.

Labelled heading: line matches label regex → skip blank lines, then lines up to next label or paragraph start are heading text; lines starting with lowercase or "(" continue previous heading line... Wait, heading text lines accumulate; a line starting with lowercase or "(" continues the previous heading line — meaning part of the same heading line? "whose title can wrap over two lines" — so a heading title like "Right to work (art. 6)" — second line might start with "(art. 6)". For labelled headings: title lines joined. The "continues the previous heading line" — join with space? For unlabelled: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading" — join with space presumably.

Simplify: I'll build a heading text by joining collected lines with a space.

Unlabelled heading: a non-empty line immediately followed by a paragraph-start line, ≤90 chars, starts with capital, not ending with . ; : , or digit. Two-line: if line before also passes test and doesn't end a paragraph sentence (i.e., previous-previous line? no—) "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading". So when we find unlabelled heading candidate at index i (followed by para start at i+1), check line at i-1: if it passes the heading test and "does not end a paragraph sentence" — meaning the line before it (i-2) doesn't end with sentence-final punctuation? "does not end a paragraph sentence" — the line before it does not end a paragraph sentence, i.e., line i-2 doesn't end with . ? : etc.? Hmm ambiguous. I'll interpret: line i-1 passes heading test AND line i-2 (if exists) does not end with terminal punctuation — actually simpler: line i-1 does not end a paragraph sentence means the preceding context suggests it's not the end of a paragraph — a paragraph's last line typically ends with a period. Wait but heading test already requires not ending with period. "does not end a paragraph sentence" — the line before it [the candidate]... I think it means: the previous line is itself not the last line of a paragraph, i.e., the line before that previous line doesn't end with sentence punctuation? Hmm.

Alternative simpler reading: line i-1 passes the heading test (so it doesn't end with . ; : , digit) — and additionally the line before the pair (i-2) does not end a paragraph sentence (doesn't end with . " etc.), meaning the paragraph hadn't finished, so i-1 is a wrapped heading not paragraph text. Wait no — if i-2 doesn't end with punctuation, then i-1 is continuation of a paragraph sentence... that would make i-1 paragraph text, not heading. Hmm.

Let me think with the real case: "the one before paragraph 73 wraps over two lines." So heading line X at i-1, line Y at i, paragraph start at i+1. Y passes heading test. X passes heading test. For X to be heading not paragraph text, the paragraph before must have ended before X — i.e., line i-2 ends with terminal punctuation (ends a paragraph sentence). So "does not end a paragraph sentence" — the line before it [X]... grammar: "when the line before it passes the same test and does not end a paragraph sentence" — "it" = the unlabelled heading candidate; "the line before it" = X; X passes the test AND X does not end a paragraph sentence — X doesn't end with . ; : , (already in test) — redundant? Maybe "end a paragraph sentence" means serve as the final line of a paragraph — which would require the paragraph's previous line to... ugh.

Practical approach: X is part of the heading if X passes heading test AND (line i-2 is a paragraph-start line, heading line, blank, or ends with terminal punctuation . " ? !). I'll implement: treat X as heading continuation if X passes test and (i-2 <0 or line i-2 is blank or ends with /[.!?"]\s*$/ or is itself a heading or para start). That captures "does not end a paragraph sentence" reasonably — X isn't continuing an unfinished sentence.

Blank lines: dropped from paragraphs but body lines include them? I'll keep blank lines in the body line array for adjacency logic ("immediately followed" — does immediately mean next non-blank or literally next?). Use next non-blank line for "immediately followed by a paragraph-start line" probably safer — actually "non-empty line immediately followed by a paragraph-start line": paragraph-start lines are non-empty; if a blank sits between, then not immediately followed. Hmm but PDF text often has blank line between heading and paragraph? In the sample: "I.\n\nIntroduction\n1.\n" — heading label, blank, title, then "1." directly. Unlabelled headings: "on the line or two lines just before a paragraph number". I'll use "next non-empty line is a paragraph start" — safer against stray blanks. Actually plan says "immediately followed" — I'll use next non-empty line; blanks are dropped in paragraph text anyway. I'll classify blank lines as... they're empty, check only counts non-empty lines. Good.

Suspect line rules: bare number 1–3 digits no full stop; or starts with 1–3 digits + space + capital letter, or UN symbol, or quotation mark; or starts with "* ". UN doc symbol regex: /^[A-Z]{1,5}\/[\w./]+/ roughly — e.g. "7 E/2003/22". Rule: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". Parse: starts with digits+space+(capital letter | UN symbol | quotation mark). So /^\d{1,3} [A-Z“"']/. Also "* " lines. Also bare number /^\d{1,3}$/.

Once a suspect line found in a paragraph, every line after it to end of its page is suspect (footnote block). Mark per-line suspect; page of line.

Flagged: has suspect line or >300 words.

First words: strip footnote marks: for each token, remove trailing digits glued after word/punctuation ("waste.2"→"waste."). A token of digits alone dropped only when previous token ends with . , or closing quote and isn't "No."/"art.". Take first six words, compare normalized.

Header check: pages whose first line was symbol; footer: pages with page number; bare numbers removed.

Nothing lost: count classifications.

Export round trip: JSON.parse(JSON.stringify(records)) length check.

UI: header, rail, tabs. Tab 01: 4 tiles, mismatch list, download buttons, two closed headings (Every check, Flagged paragraphs). Tab 02: "Headings found: n" closed box, table of paragraphs, expandable rows.

Row expansion: full text with suspect lines marked (thin red box), reference six words vs found six, "Show the PDF's lines" toggle, copy citation button.

Clicking a flagged row on tab 01 opens tab 02 with that paragraph expanded and suspect highlighted.

Max 7 clickables on tab 01: 4 tiles aren't clickable... tiles, download ×2, two closed headings = 4 clickable + tabs. Fine.

Let me now write the code. Aim ~700-900 lines.

Data structures:

```js
const D = WORKSHOP_DATA.pdf_text;
const recs = [...D.records].sort((a,b)=>a.page-b.page);
```

Parse:

```js
const lines = []; // {text, page, cls}
```

Header/footer per page, then body lines list with page.

Body processing:
- allBody = array of {text, page} (non-blank? keep blanks for adjacency? I'll keep all lines including blanks, skip blanks in logic).
- Find paragraph start indices: line matches paraStart regex. Note cover = lines before first para start (non-empty ones → cover class).
- Walk index i from first para start:
  - if paraStart → close current para, start new.
  - else if labelled heading label line (roman or single capital + "."): collect heading: skip blanks; then take lines until next label line or para start; lines starting lowercase or "(" continue previous heading line — join all with space? For wrapped titles I'll join lines: accumulate parts; if a part starts lowercase or "(", append to previous part without... with space? "Right to work (art. 6)" wrap: line1 "Right to work" line2 "(art. 6)" → join " " → "Right to work (art. 6)". Lowercase continuation: e.g. "andthe environmental dimension"? that's the doc title h2, but titles are cover. I'll join with space, collapsing. Keep simple: join with " ".
  - unlabelled heading: at line i (non-empty, before a para start at next non-empty), test.
  - else if blank → skip.
  - else paragraph text line.

Careful: unlabelled heading check must happen when the NEXT non-empty line is a para start. When iterating, when we hit a para start at index j, check the previous non-empty line j-1 (and possibly j-2) for unlabelled heading. Easier: precompute. Let me instead do single pass with lookahead: for each non-blank body line at position i (after cover), determine next non-blank index n(i). If body[i] is unlabelled-heading candidate and body[n(i)] is para start → heading (possibly with previous line). But previous line may already have been consumed as paragraph text in the pass. So do a pre-pass: compute classifications before assembling paragraphs. Plan:

1. Build body array with pages.
2. firstParaIdx = first index matching paraStart.
3. Classify each non-blank line: idx < firstParaIdx → cover.
4. For idx >= firstParaIdx: iterate:
   - labelled label lines: detect via regex; when found, mark label line and following title lines as heading until next label/paraStart/blank? "every line up to the next label line or paragraph start is heading text". Blank lines skipped within.
   - unlabelled: if next non-blank line is para start and line passes test → heading (check previous non-blank for two-line).
   
Order matters: a line could be both? A labelled label is like "IV." — ends with "."? no, "IV." ends with period — the unlabelled test requires not ending with full stop, so no clash. Do a single pass classifying each non-blank line as 'heading' or 'paragraph' or 'paraStart' (para start is paragraph).

Pass algorithm:
```js
let cls = new Array(n).fill(null); // for non-blank indices
let i = firstParaIdx;
// classify cover before
for k < firstParaIdx non-blank: cover
while i < n:
  if blank: i++; continue
  if isLabel(line[i]): // roman or [A-Z].
     consume heading: mark i heading; i++; skip blanks; while i<n && !isLabel && !isParaStart: if non-blank mark heading; i++
     continue
  if isParaStart(line[i]): mark 'start'; i++; continue
  // check unlabelled: next non-blank is para start or label? plan says paragraph-start line
  let nn = nextNonBlank(i)
  if nn!=-1 && isParaStart(line[nn]) && isUnlabelledHeading(line[i]):
     // maybe two-line: check prev non-blank pn
     let pn = prevNonBlank(i)
     if pn!=-1 && !isStart? && isUnlabelledHeading(line[pn]) && !endsParagraphSentence(pn):
        mark pn heading too
     mark i heading; i++; continue
  mark paragraph line; i++
```

Wait "does not end a paragraph sentence": for the two-line heading, the line before the pair — if line pn is paragraph text continuing, the line before pn wouldn't end with terminal punctuation. I'll define: pn can be heading if isUnlabelledHeading(pn) and (prevNonBlank(pn) is -1, or classified as heading/start/cover, or line ends with /[.!?;:"]$/... hmm "end a paragraph sentence" — a paragraph's last line usually ends with "." — if prev-prev ends with ".", then pn is likely a new heading line (paragraph finished). If prev-prev doesn't end with sentence punctuation, pn is mid-sentence continuation → paragraph text. So: pn is heading if prev-prev ends with /[.!?]/ or is a heading/start/blank/none. Blank lines: paragraphs separated by blank? In PDF text para lines are consecutive mostly. OK implement that.

But careful: when we mark pn as heading retroactively, it was already marked paragraph in the pass. Since we look ahead: at position i (candidate second line), pn = i-1 non-blank already classified 'paragraph'. If test passes, reclassify pn as heading. Fine.

Edge: isUnlabelledHeading test: non-empty, ≤90 chars, starts with capital letter, not ending with . ; : , or digit. Also should not itself be a para start... para start lines match /^(\d{1,3})\.( ...)?$/ — "1." ends with "." so fails test anyway; "1. text" ends with whatever. Also exclude label lines (end with "."). Good.

Also cover lines before firstParaIdx: they're cover, never headings — the doc title and "I." "Introduction" become cover. Paragraph 1 gets section "" — acceptable per plan.

Hmm wait, actually is that right? Look at sample page 1: "General comment No. 27 (2025) ... development*\nI.\n\nIntroduction\n1.\nA clean..." So yes "I." and "Introduction" precede paragraph 1 → cover. Plan acknowledges. OK.

Paragraphs assembly: for each 'start' line, para number; following 'paragraph' lines until next start or heading? Heading lines between paragraphs are not paragraph text. So paragraph = start line + subsequent 'paragraph'-classified lines until next start (headings skipped, but they end... a heading between para N and para N+1 — para N's lines stop at the heading; page_end = page of last paragraph line).

text = lines joined " ", collapse double spaces, trim. text_lines for toggle & export joined " | ".

Suspect: per paragraph line, suspect if matches rules, or follows a suspect line on the same page (within the paragraph, "every line after it to the end of its page" — but lines after belong to same paragraph until page ends; if a paragraph continues on next page those lines aren't suspect). Implement per line: suspect if rule matches OR (previous line in same paragraph, same page, was suspect).

Flag: any suspect line or word count > 300.

First words: compute from text tokens with footnote-mark removal.

Checks list:
1. Paragraph count: found vs reference.paragraphs.
2. Numbering: 1..n in order, gaps/dups listed.
3. First words: mismatches count.
4. Flagged: n flagged on n pages.
5. Suspect lines: counts.
6. Headers/footers: pages with symbol header (expected all = count pages), pages with page number (expected count-1), bare numbers removed (list with page).
7. Headings: labelled count, unlabelled count, list unlabelled.
8. Nothing lost: sum of classified non-empty lines vs total non-empty lines; unclassified listed.
9. Export round trip.

pass = green/red. "n of m checks pass" in header.

Tiles: paragraphs found vs expected; first words match n of expected; flagged n of found on n pages; footnotes "not separated" tile.

Mismatch list under tiles: "para. n: found … / reference …" max 10.

Downloads: JSON & Markdown per spec.

Tab 02: headings box (closed), table rows expandable. Row: No. | Section | Page | First line | Check. Expanded: full text with suspect lines in red box, found six vs reference six, "Show the PDF's lines" toggle, copy citation button. Full path in expanded: part › section.

Cross-link: flagged row click on tab 01 → switch to tab 02, expand that paragraph, scroll to it.

Design: warm off-white, serif numbers, monospace labels, red accent, thin rules.

Let me write it. I'll be careful with escaping (the regexes, template literals). Keep under 1500 lines.

Copy citation: navigator.clipboard with fallback (execCommand). Show "Copied" 2s.

Line joining: "double spaces collapsed" — text.replace(/ {2,}/g,' ').

First-words token cleanup:
```js
function cleanTokens(text){
  const toks = text.split(/\s+/);
  const out=[];
  for(let k=0;k<toks.length;k++){
    let t=toks[k];
    t = t.replace(/[.,;:]\d+$/, m=>m[0]); // "waste.2" -> "waste."  also "word2"? "digits glued to the end of a word or a punctuation mark are cut"
```
"digits glued to the end of a word or a punctuation mark are cut" — so trailing digits removed from any token ("waste.2"→"waste.", maybe "waste2"→"waste"). I'll strip trailing digit runs: t.replace(/\d+$/,''). But keep tokens that are all digits conditionally: if token is all digits and previous out token ends with . , or closing quote and not "No."/"art." → drop. Otherwise keep (real numbers like "17", "article 2" — "2" is all digits, previous token "article" doesn't end with punctuation → kept; "No. 3" previous "No." ends with "." but is abbreviation → kept).

Normalization for compare: curly→straight quotes, en/em dash→hyphen, whitespace runs→space.

Now footer stripping: from end, while line empty OR /^GE\./ OR /^(\d{6}( \d{6})*)$/ (6-digit groups) OR /^\d{1,3}$/. Bare number: if === page → page number; else record as removed bare number. But careful: stop stripping at first line that doesn't match? "From the end of each page, drop lines while the line is empty, starts with GE., ..." — yes while loop from end.

But wait: could a paragraph's last line be a bare number? Unlikely. Also footnotes text lines at foot aren't stripped (they stay, flagged). Fine.

Also header: first non-empty line === symbol → drop; else warning for that page (check "pages whose first line was the symbol").

Date stamp: "051125 061125" — /^(\d{6})( \d{6})*$/.

"GE.25-15926 (E)" starts with "GE." ✓.

Now headings path: section = most recent heading (labelled or unlabelled) before paragraph; part = most recent roman labelled heading. Store headings list with text & type.

Labelled heading text: label line "IV." then title lines. Combined heading text: I'll store as title only, or "IV. Title"? For part display "IV. …". Store heading {label:'IV', text:'Introduction'}. section display: for labelled, "Introduction"? Plan: section = nearest heading ("Right to work (art. 6)") — unlabelled ones have no label. For labelled, use label + ". " + title? I'll store section text as (label? label+'. '+title : title). part = label+'. '+title for roman.

Now write HTML. Tabs with role=tablist, arrow keys.

Check panel rows: description, values, pass/fail.

Flagged paragraphs table (tab 01, closed): Paragraph | Page | Suspect lines | Why. Why reasons: collect reasons per suspect line: "starts with a number and a space", "bare number", "asterisk note", "over 300 words". Show joined.

Let me write the file now.

Suspect rules detail:
```js
function suspectReason(line){
  const t=line.trim();
  if(/^\d{1,3}$/.test(t)) return 'bare number';
  if(/^\d{1,3} [A-Z“"'A-Z]/.test(t)) ... 
```
"starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark": /^\d{1,3} ([A-Z“"])/ — capital letter covers E of E/2003/22 too. So just /^\d{1,3} [A-Z“"‘'']/.
Asterisk: /^\*\s/ → 'asterisk note' (the "* Adopted by..." note — but that's on page 1 in cover area before para 1? It's after title, before "I."? In sample, "*" footnote is at end of title in HTML; in PDF probably near foot of page 1 with other footnotes... it says starts with "* " — include rule.)

Propagation: line.suspect true if reason or (prev line in same paragraph same page suspect).

Why column: reasons of first suspect line + maybe "footnote block to end of page"? Plan's why examples: "starts with a number and a space", "bare number", "paragraph over 300 words". I'll list distinct reasons.

Now the expanded row "suspect lines marked": render each line; suspect lines wrapped in span.suspect with thin red box. But text is joined running text; to mark lines, render lines joined with space but wrap suspect lines in spans: paragraphs lines array → html with suspect spans, joined " ".

"Show the PDF's lines" toggle: show lines with original line breaks and page markers where a new page began.

Export JSON fields: symbol, paragraph, section, part, page_start, page_end, text, flagged, first_words_match, citation, doc_url, limitations, text_lines.

Markdown: front matter, then headings in document order as ## (labelled/roman → ##, lettered/unlabelled → ###?) plan: "the headings as ## and ### lines in document order and each paragraph as its number in bold, then its text". I'll do labelled (roman) → ##, others → ###.

Headings in document order: I need headings interleaved with paragraphs. During the pass, record events in order. I'll build a docOrder array.

Filename: symbol.replace(/\//g,'-').

Disable exports if no paragraphs.

Rail: big numbers.

Edge: reference missing → tiles "no reference in this file", checks "not run".

OK, writing now. I'll aim for clarity.

Also arrow-key tab navigation, hidden panels not focusable (use hidden attribute + CSS rule).

Check "Nothing lost": classifications: cover, header, heading, paragraph (includes para-start lines), footer. Count non-empty lines total across pages; each non-empty line gets exactly one class. My lines array: I'll create per-page processing producing bodyLines (with class null initially), and header/footer counted. Cover etc. assigned in pass. Then count.

Blank lines: not counted (non-empty only). Note: line "" trimmed? Lines may have trailing spaces — trim for tests; count non-empty after trim.

Let me write:

```js
const D = WORKSHOP_DATA.pdf_text || {};
const SYM = D.symbol || '';
const REF = D.reference || null;
const recs = (D.records||[]).slice().sort((a,b)=>a.page-b.page).filter(r=>typeof r.text==='string');
```

Parse pages:

```js
const bodyLines = []; // {text, page}
const pageInfo = [];
let headerPages=0, headerWarnings=[], pageNumPages=0, bareFooter=[];
for(const r of recs){
  const raw = r.text.split(/\r?\n/);
  const lines = raw.map(s=>s.replace(/\s+$/,''));
  // header
  let fi=0; while(fi<lines.length && lines[fi].trim()==='') fi++;
  if(fi<lines.length && lines[fi].trim()===SYM){ headerPages++; }
  else headerWarnings.push(r.page);
  // footer
  let ei=lines.length-1;
  const footerSet=[];
  while(ei>=0){
    const t=lines[ei].trim();
    if(t===''){ ei--; continue; }
    if(/^GE\./.test(t)){ footerSet.push({t,kind:'job'}); ei--; continue; }
    if(/^\d{6}( \d{6})*$/.test(t)){ footerSet.push({t,kind:'date'}); ei--; continue; }
    if(/^\d{1,3}$/.test(t)){
      if(Number(t)===r.page){ footerSet.push({t,kind:'page'}); }
      else { footerSet.push({t,kind:'bare'}); bareFooter.push({page:r.page, num:t}); }
      ei--; continue;
    }
    break;
  }
  ...
```

Careful: header removal — body starts after first non-empty line if it's the symbol; if not... plan says drop if equals symbol, otherwise note warning — and the line stays in body? "If a page's first non-empty line equals symbol, drop it; otherwise note a warning for that page." So if not symbol, line remains as body. OK: start = (fi<lines.length && lines[fi].trim()===SYM) ? fi+1 : fi. End: last index kept = ei (line that broke loop) — body lines from start..ei inclusive. But header check uses fi before footer processing — fine, footer processing from end independent. But if a page's only content... fine.

Count footer lines: non-empty footer lines classified 'footer'. Also count 'header' classified lines: 1 per page where dropped.

Body: for i in start..ei: if trim!=='' push {text: lines[i].trim(), page: r.page, cls:null}. Actually keep trimmed.

Wait "immediately followed" logic uses next non-blank within body lines (blanks dropped from array). But two-line heading check uses prev non-blank in bodyLines. But cover/body split: bodyLines includes pre-first-para lines (cover). OK.

Para start regexes:
```js
const reAlone=/^(\d{1,3})\.$/;
const reWith=/^(\d{1,3})\. (.+)$/;
```

Label: /^([IVX]+|[A-Z])\.$/.

Pass:

```js
const firstIdx = bodyLines.findIndex(l=>isStart(l.text));
for(let i=0;i<bodyLines.length;i++){
  if(i<firstIdx){ bodyLines[i].cls='cover'; }
}
let i=firstIdx;
const headings=[]; // {label, text, idx}
const docOrder=[];
while(i<bodyLines.length){
  const l=bodyLines[i];
  if(isLabel(l.text)){
    let label=l.text.slice(0,-1);
    i++;
    while(i<bodyLines.length && bodyLines[i].text==='') i++; // no blanks in array anyway
    const parts=[];
    while(i<bodyLines.length && !isLabel(bodyLines[i].text) && !isStart(bodyLines[i].text)){
      parts.push(bodyLines[i].text); bodyLines[i].cls='heading'; i++;
    }
    const h={label, text: parts.join(' '), roman:/^[IVX]+$/.test(label)};
    headings.push(h); docOrder.push({type:'h',h});
    continue;
  }
  if(isStart(l.text)){
    l.cls='para'; l.startNum=Number(RegExp.$1||...) 
```

Hmm need number extraction; write helper startNum(text) returns number or null, plus first text part.

Continue:
```js
  if(isStart(l.text)){ l.cls='para'; l.start=true; i++; continue; }
  // unlabelled heading?
  const nn = i+1; // bodyLines has no blanks
  if(nn<bodyLines.length && isStart(bodyLines[nn].text) && isUnlabelled(l.text)){
    // two-line
    const pn = i-1;
    if(pn>=0 && isUnlabelled(bodyLines[pn].text) && bodyLines[pn].cls!=='heading' && !continuesSentence(pn)){
      bodyLines[pn].cls='heading';
      headings.push({label:null, text: bodyLines[pn].text+' '+l.text, roman:false});
      docOrder.push({type:'h',h:last});
    } else {
      headings.push({label:null,text:l.text,roman:false}); docOrder.push(...)
    }
    l.cls='heading'; i++; continue;
  }
  l.cls='para'; i++;
```

continuesSentence(pn): the line before pn — if it's a para line not ending with /[.!?;:"”]/ → pn continues a sentence → not heading. Define: const before = bodyLines[pn-1]; return before && before.cls==='para' && !/[.!?;:]”"]$/.test(before.text). If continuesSentence true → pn is paragraph text.

But wait: bodyLines[pn].cls might be 'para' already; the check "does not end a paragraph sentence": I'll require NOT continuesSentence. Also if pn is a start line (para start with text on same line) — could a heading directly follow a "N. text" start line? The start line's text is paragraph text, paragraph continues. Unlikely. Keep simple.

Also note: when we retroactively mark pn heading, it might already have been pushed... no, headings pushed when encountered; pn was classified 'para' earlier in the loop but not into any heading. But it may have been added to a paragraph's lines? I assemble paragraphs after classification, so fine.

But subtle: pn's cls was 'para' — reassign to 'heading'. Also docOrder: heading pushed now, but paragraphs come later — docOrder for headings vs paragraphs: I'll build docOrder from final assembly instead: iterate bodyLines; when hitting a heading-line that is the first line of a heading... simpler: build paragraphs from para lines; for markdown order, I can reconstruct: walk bodyLines in order; group heading lines into heading blocks (consecutive heading cls lines = one heading? two-line unlabelled heading lines are adjacent; labelled label+title adjacent). Actually consecutive 'heading' lines = one heading block. I'll do that for docOrder: iterate, when cls==='heading' and (prev not heading) → new heading block collecting until cls!=='heading'. When start line → new paragraph. Good, avoids docOrder during pass. Drop docOrder pushes.

Paragraph assembly:

```js
const paras=[]; let cur=null; let curHeadingText=''; let curPart='';
for(let idx=firstIdx; idx<bodyLines.length; idx++){
  const l=bodyLines[idx];
  if(l.cls==='heading'){
    // heading boundary: ends current paragraph
    if(cur) { cur=null; }  // paragraph ends at heading
    // update current heading refs: need heading object
```

Hmm — need to know heading text when crossing it. Consecutive heading lines belong to one heading; the heading's full text known after collecting. Approach: precompute heading blocks: list of {startIdx,endIdx,heading}. Then in assembly walk: maintain headingIndex. Simpler: iterate idx; if line is heading and it's the first line of a block → finalize block → set curSection/curPart; end current paragraph. If para start line → close cur, open new with number. If para line → append (if no cur... can't happen after firstIdx since starts at a start line; but paragraph lines before any start? no, firstIdx is first start).

Wait: could there be 'para' lines between firstIdx... firstIdx is a start line, fine. Could 'para' lines appear with cur===null (after a heading, before next start)? Paragraph text lines always follow their start. After a heading, next is a start (or another heading). Should be fine; guard: if cur null and para line → attach to... create orphan? Classify-wise it's 'para'. Guard: append to previous paragraph? I'll guard by creating the paragraph anyway with number null — but numbering check expects 1..n. Just guard: if(!cur) continue-ish but keep line classified. Actually if it happens, attach to last paragraph if exists. Keep code robust: if(!cur && paras.length) append to paras[paras.length-1]. Else skip.

Each paragraph:
```js
{num, lines:[{text,page,suspect,reason}], section, part, page_start, page_end}
```
page_start = first line page; page_end = last line page.

Note paragraph ends also at heading or next start or end.

Suspect per line with propagation within paragraph same page:
```js
let prevSuspectPage=null;
for(const ln of p.lines){
  let r = suspectReason(ln.text);
  if(!r && prevSuspect===true && prevPage===ln.page){ r='footnote block'; }
```
Reasons: only first line gets its reason; subsequent get 'footnote block'. flagged reasons set.

Word count: text.split(/\s+/).length.

First words function:

```js
function firstWords(text){
  const toks=text.split(/\s+/);
  const out=[];
  for(const t0 of toks){
    let t=t0.replace(/\d+$/,''); // cut glued digits
    if(/^\d+$/.test(t)){
      const prev=out[out.length-1];
      const p=prev||'';
      if(p && /[.,;”"’']$/.test(p) && !/\b(No|No\.|art|arts|para|paras|page|pages|vol)\.$/... 
```
Simplify: abbreviation check: prev matches /(No|art|para|page|vol)\.$/i → keep number. Else if prev ends with [.,;”"'] → drop. Else keep.
Then push t (if t!=='' ). Take first 6 of out.

Wait "a token of digits alone is dropped only when the token before it ends with a full stop, comma or closing quote and is not an abbreviation such as No. or art.". Also what about the very first token being digits (para starts with number, "17 Sustainable...")? prev undefined → keep. Good.

Also cutting glued digits from every token: "waste.2"→"waste."; but "2" alone handled above; "2025" alone → prev "in" doesn't end punctuation → kept. Good. But careful: cutting digits from tokens like "16.3"? Only first six words matter; acceptable.

Normalize compare:
```js
const norm=s=>s.replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
```

Compare out.slice(0,6).join(' ') with REF.first_words[String(num)].

Checks array: each {name, detail, pass, extra}. Build list; count passes.

Now render. I'll write render functions building innerHTML strings mostly, with event delegation.

Tabs: two buttons; panels divs with hidden.

Tab 01 content:
- tiles (4)
- mismatch list
- Take away: two buttons
- closed: Every check (button aria-expanded + div hidden)
- closed: Flagged paragraphs (n) + note + table

Tab 02:
- closed: Headings found: n
- table with rows (details/summary-like custom: tr button? Rows as buttons with aria-expanded — use <tr> with click, and aria-expanded on the row? Better: each paragraph is a <div class="row">? Plan says table with caption, th scope. I'll use a real table where the main row is clickable (role="button", tabindex=0, aria-expanded) and expansion inserts a following row with colspan=5. Keep accessible.

Copy citation button inside expanded row.

"Show the PDF's lines" toggle under expanded text.

Cross-link from tab 01 flagged table: switch tab, expand para, highlight suspect (already marked red boxes).

Check panel lines: name, values, pass/fail.

Let me count checks (m=9).

Header right: green dot "n of m checks pass" or red "n checks failed"; then "n paragraphs flagged".

Footer: source, built (D.built? pdf_text has no built field in spec — it has title, symbol, doc_url, source, count, records, reference. Use D.built if present else omit), and the no-model line.

Now write the whole file. Let me write it directly, carefully.

For the expanded paragraph full text with suspect marks: join lines; suspect lines wrapped `<span class="sus">line</span>`; escape HTML.

Escape helper.

First line column: text.slice(0,120) cut at word + "…".

Let me now also handle: "paragraph over 300 words" flagged reason.

JSON export: build records, download via Blob.

Round-trip check: JSON.parse(JSON.stringify(exportRecords)).length === paras.length → pass.

Numbering check: expected sequence 1..paras.length? "Exactly 1 to n in order" — compare nums to 1..N; gaps/dups listed. pass if nums[i]===i+1 for all.

First words check: count mismatches among paras with reference available; pass if 0.

Headers check: headerPages === recs.length → pass; detail lists warnings.
Page-number check: pageNumPages === recs.length-1 (expected all but first). Note: page 1 might have no page number; but page numbers might be "2".."20" matching. Count pages where a footer line === page.

Nothing-lost check: total non-empty lines = header+footer+cover+heading+para(+unclassified). I track counts: headerCount (dropped symbol lines), footerCount (non-empty footer lines), then body classes. Any cls===null → unclassified, list with page.

Suspect check: count suspect lines, pages, paragraphs — informational, pass true always? "none is removed" — I'll make it pass always (informational).

Flagged check: informational, pass true.

Paragraph count check: pass if equal (when reference exists).

So m = 9 checks; pass count varies.

Tiles: 
1. Paragraphs found: n — beside "the document has R.paragraphs"; green equal, red with difference.
2. First words match: n of R.paragraphs.
3. Paragraphs flagged: n of found, on n pages, red if >0.
4. Footnotes: "not separated" (text tile, big serif "141" maybe? plan: **Footnotes: not separated**, "the document has reference.footnotes". I'll show big number = reference.footnotes with label "footnotes in the document — not separated".)

If no reference: tiles say "no reference in this file".

If no paragraphs found: tab 01 says so, exports disabled.

Now writing. Also CSS: [hidden]{display:none!important}.

Let me draft the full HTML now, mindful of length.

For arrow-key tabs:
```js
tablist.addEventListener('keydown', e=>{ if(e.key==='ArrowRight'||e.key==='ArrowLeft'){...}});
```

Row expansion on tab 02: function togglePara(num).

Copy: async navigator.clipboard.writeText fallback textarea.

Markdown export:
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
footnotes: "not separated; the document has n"
---

## I. Introduction

**1.** text...

**2.** text (flagged: may contain footnote text)
```

Heading lines: for labelled: `## IV. Title`; others `### Title`. In document order interleaved with paragraphs. Build via bodyLines walk: heading blocks and paragraphs in index order. I have paras with their first line index? Track para.startIdx. Let me store firstIdx per para during assembly. Then merge sorted by first line index.

OK. Write it.

Also "Headings found: n" box lists them (closed). Include type.

Time to write final code. I'll write ~800 lines.

One more detail: row Check column values: "OK", "first words differ" (red), "may contain footnote text" (red). If both? Show "may contain footnote text" priority? Plan lists three; I'll show flagged first, else first-words, else OK. Actually if both, show both compactly: "flagged · first words differ"? I'll show "may contain footnote text" and if also mismatch add "· first words differ".

Expanded row: full path "IV. … › Right to work (art. 6)", found six words vs reference six words, full text with suspect marks, PDF lines toggle, copy citation.

Also tab01 flagged table "Why" reasons; "Suspect lines" = count of suspect lines in paragraph.

Alright, code:

I'll now write carefully. Note template literal usage with ${} inside strings — fine.

Potential pitfall: regex `/^(\d{1,3})\. (.+)$/` — paragraph 23 shares line. Good.

isStart returns {num, text} or null.

Let me write it all out.

For the "found six words beside reference six words": show both even when equal? Plan: "the reference's six words beside the found six". Show always in expanded.

Write the code now. I'll produce the final answer with a short intro and the html block.

Regarding rail: "DOCUMENT" card with symbol monospace and short title — pdf_text has only title; use title (maybe shortened?). Use D.title. Two big serif numbers: paragraphs found of expected with thin bar (bar width = found/expected, red when ≠); flagged count red when >0; then "n of m checks pass".

Also header line: symbol linked, adopted, n pages, source.

Checks panel content lines: each check: name — values — pass/fail. With link to rows concerned for failures (numbering → tab02, first words → tab02). I'll add a link "view paragraphs" that switches to tab 02.

Flagged table on tab 01: clicking row → open tab 02, expand, scroll.

Implement expandPara(num): ensure row exists, set expanded, insert expansion row after.

I'll render tab02 table once; expansion rows created/removed dynamically.

Suspect highlight: expansion shows text with suspect spans.

"Show the PDF's lines": button toggling a <pre>-like block with lines and "[page N]" markers.

OK writing final.

Estimated char budget fine. Let me write.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b34;}
*{box-sizing:border-box;}
[hidden]{display:none!important;}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
a{color:var(--red);}
.mono{font:11px/1.5 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;}
...
```

Focus ring: :focus-visible{outline:2px solid var(--red); outline-offset:2px}.

Layout: header, main grid: rail 260px + content.

Write JS.

Also handle count: D.count is string "20" — use recs.length.

Now, final code writing. I'll be thorough but compact.

Careful about the two-line unlabelled heading when pn was classified 'para' — also the paragraph before must be closed at pn... In assembly, heading cls lines end paragraphs; since pn now 'heading', assembly handles it.

But wait: order of pass: we process lines left to right; when at i (candidate), pn=i-1 already processed as 'para'. Retroactively set to 'heading'. But what if pn is a start line ("23. something")? isUnlabelled requires ≤90 chars, capital start, not ending .;:,digit — "23. Something..." starts with digit not capital → fails. Good.

Also unlabelled heading immediately followed by a labelled label line? Plan says followed by paragraph-start. Only para start.

Also: what if an unlabelled heading candidate is followed by another heading line then para start? E.g., "Right to work (art. 6)" then "A." then title then para. "Right to work..." followed by "A." (label), not para start → not detected as heading → becomes paragraph text of previous para. Hmm. In real doc, unlabelled headings sit directly before paragraph numbers ("on the line or two lines just before a paragraph number"). Follow plan.

Hmm, but wait: are unlabelled headings like "Right to work (art. 6)" actually under lettered subsections "A."? "Right to work (art. 6)" — in GC27 these are the subsection titles themselves? The plan says lettered subsections "A." whose title wraps, and unlabelled headings like "Right to work (art. 6)". So "Right to work (art. 6)" is likely the title under "A."? Then "A." then "Right to work (art. 6)" then paragraph. Then "Right to work..." is followed by para start directly — fine, it's the heading text of the labelled heading? No — labelled heading collection: "A." then lines until next label or para start → "Right to work (art. 6)" would be collected as the labelled heading's title. Then it's a labelled heading, not unlabelled. The 20 unlabelled ones are others like "Children". OK either way the pass handles: labelled collection consumes lines until para start, so those become heading text of "A." — good.

But wait, then when is "Right to work (art. 6)" an unlabelled heading? When there's no "A." before it. Doesn't matter — plan's example. Code handles both.

One more: the labelled heading collection "every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or '(' continues the previous heading line" — I join all parts with space regardless. Fine.

Edge: what if labelled label line appears but no title (next line is para start)? heading text ''. Fine.

Now first words compare — REF.first_words keys strings.

Mismatch list: for paras where ref exists and mismatch: "para. n: found X / reference Y" (found six words). Max 10 + "and n more".

Let me also compute pagesWithFlagged.

Write export JSON:

```js
function exportRecords(){
  return paras.map(p=>({
    symbol:SYM, paragraph:p.num, section:p.section, part:p.part,
    page_start:p.page_start, page_end:p.page_end, text:p.text,
    flagged:p.flagged, first_words_match:p.fwMatch, citation:cite(p.num),
    doc_url:D.doc_url||'',
    limitations: p.flagged? `footnotes not separated; ${p.suspectCount} may sit inside this paragraph` : 'footnotes not separated',
    text_lines: p.lines.map(l=>l.text).join(' | ')
  }));
}
```

Hmm "n may sit inside" — n = suspect lines count. OK.

Downloads:
```js
function download(name, mime, content){ const b=new Blob([content],{type:mime+';charset=utf-8'}); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(u),5000);}
```

Now render everything. Let me write the final document.

Also tabs arrow keys and role=tabpanel.

Let me write out the code in full now, being careful.

Also the check "Export round trip": run at build time (parse JSON string). pass if length equal.

Also nothing-lost: count classified:
- headerLines: number of dropped symbol lines (per page 0 or 1)
- footer non-empty lines count
- body cls counts: cover/heading/para; null → unclassified list.

Total non-empty lines = sum over pages of lines with trim!=='' . Compute during page parse: totalNonEmpty += count. And header/footer counts track only non-empty. Body lines only non-empty. So sum should match unless bug. 

Now flagged paragraphs closed heading on tab 01 — table with rows clickable.

Reason strings: from suspect reasons set + 'paragraph over 300 words'.

suspectReason:
```js
function suspectReason(t){
  if(/^\d{1,3}$/.test(t)) return 'bare number';
  if(/^\d{1,3} [A-Z“"‘']/.test(t)) return 'starts with a number and a space';
  if(/^\*\s/.test(t)) return 'asterisk note';
  return null;
}
```
Hmm "bare number" suspect inside paragraph — but paragraph numbers alone lines are start lines (with period). Bare number without period inside para = suspect. But careful: the propagation mark "footnote block" lines — reason 'footnote block'.

Also, the plan's Why examples include "bare number". Good.

Note: capital letter check includes symbols like "E/2003/22" (E is capital). ✓.

One risk: line "17 Sustainable Development Goals..." mid-paragraph → flagged (plan accepts).

Now big writing. Also include "How this is computed" lines near tiles.

Let me write the answer.