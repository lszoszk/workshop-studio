Need to build a full app per spec. Two tabs, left rail, header, footer, extraction pipeline, checks, exports. Let me write carefully but compactly, aiming ~700-900 lines.

Key pipeline:

- records sorted by page. For each page: lines = text.split('\n').
- Header: if first non-empty line === symbol, drop; else warning.
- Footer: from end, drop lines while empty, starts "GE.", only 6-digit groups (/^(\d{6})( \d{6})*$/), or bare number /^\d{1,3}$/. Track page number vs bare numbers.
- Concatenate body lines (non header/footer, footnote lines included) with page tags.
- Cover: lines before first paragraph start.
- Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.
- Headings: labelled /^([IVX]+|[A-Z])\.$/ opens labelled heading; skip blanks, collect lines until next label or paragraph start; continuation lines start lowercase or "(" merge into previous heading line. Unlabelled heading: non-empty line immediately followed by paragraph start, ≤90 chars, starts capital, not ending with . ; : , or digit; possibly two-line when previous line passes same test and doesn't end paragraph sentence.
- Paragraph lines: everything else non-empty. Suspect lines: bare number 1-3 digits no full stop, or starts with 1-3 digits + space + capital / UN symbol / quote, or starts "* ". Once suspect, all lines to end of page are suspect. Paragraph >300 words flagged.
- First words: first six words after stripping footnote marks; compare with reference.

Headings detection on the concatenated body lines with lookahead. Since headings are lines before paragraph starts, I'll implement:

Iterate body lines (with page tag, and note blank lines). I'll keep blanks in the array for "immediately followed" tests (blank lines exist between heading label and title). Simpler: process sequence of lines including empties; classify each non-empty.

Algorithm:
```
i=0; state: current heading=null, part=null, current para=null.
for i over lines:
  line = lines[i]
  if empty: continue (mark unclassified? no—only non-empty classified)
  if paraStart(line): close current para? Actually paragraph ends when next paragraph starts or heading. If a paragraph is "open", close it when we hit a paragraph start or a heading. But paragraph text just continues until next structural element. Blank lines dropped.
```
Better: first find all indices of paragraph starts, labelled heading labels. Then classify.

Implementation plan:
1. lines = array of {page, text, blank}.
2. Identify paragraph starts and labelled headings and unlabelled headings by lookahead.
3. Then walk: lines before first paragraph start = cover. For each line: if paragraph start → start new para. If labelled heading marker → consume heading (label + following lines until next label line or paragraph start, blank skipping; continuation lines start lowercase or "(" join previous). If unlabelled heading marker → heading text (possibly two lines already joined). Else → paragraph line of current para (or cover).
4. page_start/end from first/last line pages.

Labelled heading consumption: label line like "I." then blank then "Introduction". Collect heading lines: skip blanks after label; take lines until next paragraph start, labelled label line, or... also stop before footer? Already removed. Continuation: line starting lowercase or "(" joins previous heading line. Heading text ends when next labelled line or paragraph start encountered. But footnote lines at foot of page before next heading — those lines would be consumed into heading! Hmm. In real docs, footnote lines sit at foot of page, then next page starts with header (removed) then maybe paragraph text continues or a heading. Footnote text lines could be eaten into a heading if a heading follows. Risk accepted; spec doesn't address. Actually spec: "every line up to the next label line or paragraph start is heading text" — yes, footnotes may get swallowed into headings. That's per spec; leave it. Hmm but that would corrupt headings. But spec says follow plan. OK.

Actually wait—footnote lines after a paragraph before a heading on next page: they'd be paragraph text of current paragraph (spec: "Every other non-empty body line belongs to the current paragraph"), and since suspect-line rule marks from a suspect line to end of page, they'd be flagged. Fine.

Unlabelled heading two-line: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading." So when we mark line i as unlabelled heading (followed by para start), check line i-1: passes heading test (≤90, capital start, not ending .;:,digit) and "does not end a paragraph sentence" — i.e., previous line doesn't end with sentence-final punctuation? If it ends with '.' etc it fails the heading test already. "does not end a paragraph sentence" — the test says not ending full stop etc. So condition is basically the same test plus not being... hmm. I'll interpret: previous line passes same test (capital, ≤90, no terminal punctuation). Then both are the heading. But careful: previous line might be a paragraph-start line? Starts with digit, not capital, fails. Good.

But wait, if line i-1 becomes part of heading, then it isn't paragraph text. And line i-2 before it? Only two lines max.

Also headings inside labelled heading region: handled by consumption.

Also note: a line followed by a paragraph-start that is *itself* a paragraph start line? No, paragraph-start lines start with digits.

Edge: "Right to work (art. 6)" starts with 'R' capital, ends ')'. Ends with ')' — the test says "not ending with a full stop, semicolon, colon, comma or digit". ')' allowed. Good.

Suspect line rules:
- bare number 1-3 digits, no full stop: /^\d{1,3}$/
- starts with 1-3 digits, space, then capital letter, UN symbol, or quotation mark: /^\d{1,3} [A-Z"“]/ — UN symbol like "E/2003/22" starts with E capital, covered.
- starts "* " .

From suspect line to end of its page all suspect. So track per page: once a suspect found at page p, all remaining lines of page p suspect. But a page's body lines are contiguous in concat order (yes, concatenated in page order). So I can process: find suspect indices, then mark all subsequent lines with same page.

Flagged paragraph: has a suspect line or >300 words.

First words: function stripMarks(tokens):
Process tokens: for each token, remove trailing digits glued: replace(/\d+$/,'') only if token ends with digits and has non-digit before? "waste.2" → "waste." — digits at end after punctuation or word. But a token that's all digits after a token ending with '.', ',' or closing quote and previous token not abbreviation ("No.", "art.") → drop. E.g. paragraph starting "24. The Committee..." — no, paragraph number is stripped already. Paragraph 24 starts with real number per spec: "24. article 2" wait — text after removing paragraph number "24." — hmm, sample: paragraphs 24, 27, 46, 60 start with real numbers like "Article 2" — no, "start with real numbers, 'article 2' or 'No. 3'". So token "2" after token "article"? "article" ends with 'e', not punctuation, so digits token kept. "No. 3": previous token "No." ends with '.' but is abbreviation "No." — kept. OK.

Implementation:
```
function firstWords(text){
  let toks = text.trim().split(/\s+/);
  let out=[];
  for(let j=0;j<toks.length && out.length<6;j++){
    let t=toks[j];
    if(/^\d+$/.test(t)){
      let prev=out.length?out[out.length-1]:null;
      if(prev && /[.,”"’')]\.?$/.test(prev) ... 
```
Wait: drop digit-only token when the token before it (in output? or original?) ends with full stop, comma or closing quote and is not "No."/"art.". Note: after stripping glued digits, "waste.2" becomes "waste." which ends with '.', then a following digit token would be dropped. That's the intent: footnote mark "…report. 3 The" → "report." then "3" dropped. Good. Prev check: prev token ends with [. ,] or closing quote ” " ’ ') and prev.toLowerCase() not in ["no.","art."]. Hmm "No." ends with '.', abbreviations keep. Also "e.g." maybe—but spec says such as. I'll exempt a small list: no., art., para., see? Spec says "such as 'No.' or 'art.'". I'll use ["no.","art.","para.","p."]. Hmm, could break first_words for a paragraph starting "No. 3 and No. 4..." — the reference's first_words presumably includes "No. 3". Keep exemption.

Also strip glued digits: if token has non-digits and ends with digits — "waste.2" → cut trailing digits: t=t.replace(/\d+$/,''). But words ending with digits legitimately? "Goal 4"? token "4" alone handled. "COVID-19"? ends with digits! "Article 2"? "2" separate. Hmm, risky but per spec. Actually spec: 'digits glued to the end of a word or a punctuation mark are cut'. Follow it. But careful: token like "17" alone — digit-only, handled by other rule. Token "SDG" fine.

Wait, but "Paragraphs 24, 27, 46 and 60 start with real numbers, 'article 2'..." — meaning e.g. "2 The Committee..." Hmm "start with real numbers" — like paragraph text begins "2. States parties..."? If first token is "2" and prev is null (no previous token), digit-only with no prev → kept (drop only when prev exists and ends with punctuation). Good.

Then compare with reference first_words: normalize curly quotes, dashes, whitespace.

reference first_words is first six words already? "the first six words of each numbered paragraph" — yes, the value is six words. Compare joined.

Checks:
1. Paragraph count found vs reference.paragraphs.
2. Numbering 1..n in order; gaps/dups listed.
3. First words: n of m match; mismatches listed.
4. Pages flagged: info line, not failure.
5. Suspect lines: counts.
6. Headers/footers: pages with symbol first line, pages with page number in footer, bare numbers removed with page.
7. Headings: counts labelled/unlabelled, list unlabelled.
8. Nothing lost: classify every non-empty line exactly once: cover, header, heading, paragraph, footer; counts sum to total non-empty; unclassified listed red. I need to track classification counts. Header/footer dropped lines are classified header/footer. Heading lines: label lines + heading text lines. Cover lines before first para start. Paragraph lines. Blank lines not counted (non-empty only). Note footnote lines count as paragraph lines. Need total non-empty across all pages equals sum. I'll count as I classify, plus verify.

Wait: heading label lines like "I." and "A." — count as heading. Continuation lines count as heading.

9. Export round trip: JSON.parse(JSON.stringify(exportRecords)).length === table rows.

Checks pass/fail: count passes for the green/red dot. Which checks are pass/fail? Paragraph count, numbering, first words (mismatch>0 fails? spec: mismatch listed, row flagged red — I'd say it's a failure), headers/footers (expected all/eall-but-first; if not, failed? spec says "expected all" — treat as check with expectation), nothing lost (unclassified>0 fails), export round trip. Pages flagged and suspect lines are informational (not failure). Headings check informational. So m checks = let's define checks array each {name, pass:boolean|null, detail}. Count pass among those with boolean. Header/footer: two sub-checks maybe combine. I'll make each line one check; some "info". For the dot: "n of m checks pass" — m = number of checks total; pass count. Info ones... hmm. Simpler: give every check pass/fail; info checks (pages flagged, suspect lines, headings) always pass? Spec says "A flag is not a failure". I'll mark info checks as pass=true with neutral wording, counted in m. Fine.

Missing reference: tiles say "no reference in this file"; checks needing it "not run" — not counted as pass. I'll set pass=null and count only non-null toward pass; m = total checks; dot shows "n of m checks pass". Slight ambiguity, fine.

Exports: JSON and Markdown downloads via Blob. Records with fields per spec plus text_lines.

Markdown: front matter, then headings in document order as ## (part/roman) and ### (section), paragraphs as "**n** text (flagged...)". Headings in document order: I'll collect a list of headings with their position (in order encountered), and emit between paragraphs. Build a combined ordered list of items: {type:'heading', level} or {type:'para', p}. When emitting, only emit heading if it changed since last emitted (paragraphs under same heading). Simple: track lastPart/lastSection; when paragraph's part/section differs from previous, emit headings. But headings with no paragraphs after them before another heading—edge, skip. Good enough: iterate paragraphs, emit heading changes. Actually to list all headings in document order including ones... spec says "the headings as ## and ### lines in document order and each paragraph as its number". I'll build ordered stream during parse: each heading pushes an item, each paragraph pushes. Then emit sequentially, skipping consecutive duplicate headings (a heading immediately followed by another heading — emit both? e.g., part then subsection, fine).

Tab 02: table of paragraphs, rows expandable showing full text with suspect lines marked (thin red box — wrap suspect line text in span), reference six words vs found six, "Show the PDF's lines" toggle revealing lines with page numbers, Copy citation button. Suspect lines within running text: since text is lines joined with spaces, I can rebuild running text with spans per line, marking suspect ones. text = lines.join(' ') — I'll render each line as a span (space-separated) so suspect lines get class.

Headings box: closed heading "Headings found: n" listing them.

Left rail always visible — layout: rail + content side by side; header above; footer below.

Flagged pages panel on tab 01: table Page|Paragraph|Suspect lines|Why, click row expands raw page lines with suspects highlighted and paragraph info. Need to keep raw page lines (after header/footer removal? "the page's raw lines" — I'll show body lines with page tag, suspects highlighted). Suspect lines stored per paragraph; for page view, compute suspect lines of that page: lines belonging to paragraphs flagged on that page that are suspect, plus "why" reasons. Why reasons: "starts with a number and a space", "bare number", "asterisk note", "paragraph over 300 words". I'll store reason per suspect line.

Let me store for each paragraph: lines: [{page, text, suspect, reason}]. Page flagged when any paragraph line on that page (in a paragraph) is suspect.

For flagged pages table: for page p, list paragraphs with suspect lines on p; suspect lines = the actual line texts; why = reasons.

Copy citation: navigator.clipboard may fail in sandbox; fallback with textarea + execCommand. Use try/catch.

Styling: studio look. Let me write the code now. Aim for clean, complete.

Structure:

```html
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>...</title>
<style>...</style></head>
<body>
<header>...</header>
<div class="tabs" role="tablist">...</div>
<main class="layout">
  <aside id="rail">...</aside>
  <section id="panel01" role="tabpanel">...</section>
  <section id="panel02" role="tabpanel" hidden>...</section>
</main>
<footer>...</footer>
<script>...</script>
</body></html>
```

Wait tabs under header, rail always visible spanning both tabs — put tabs above layout, rail inside layout left, panels right.

Arrow key tab navigation per WAI-ARIA.

Now the parse code.

```js
const D = WORKSHOP_DATA.pdf_text;
const recs = [...D.records].sort((a,b)=>a.page-b.page);
const symbol = D.symbol, ref = D.reference||{};
```

Per page processing:
```js
const stats = {headerPages:0, pageNumberPages:0, bareFooterNums:[], headerWarn:[]};
const pageBodies = []; // array of {page, lines:[{text, cls}]}
for(const r of recs){
  const raw = (r.text||'').split('\n').map(s=>s.replace(/\r$/,''));
  // find first non-empty
  let first = raw.findIndex(l=>l.trim()!=='');
  let lines = raw.map(l=>l.trim()); // trim? Spec says "first non-empty line equals symbol" — use trimmed comparisons. I'll trim all lines.
```
Trimming lines: fine for prose since joined with spaces.

```js
  let start=0;
  if(lines[first]===symbol){start=first+1; stats.headerPages++;}
  else stats.headerWarn.push(r.page);
  // footer from end
  let end=lines.length;
  const bareFooter=[];
  while(end>start){
    const l=lines[end-1];
    if(l===''){end--;continue;}
    if(/^GE\./.test(l)){end--;continue;}
    if(/^(\d{6})( \d{6})*$/.test(l)){end--;continue;}
    if(/^\d{1,3}$/.test(l)){
      if(l===String(r.page)) stats.pageNumberPages++;
      else {stats.bareFooterNums.push({page:r.page, num:l});}
      end--;continue;
    }
    break;
  }
  pageBodies.push({page:r.page, lines:lines.slice(start,end)});
}
```
Wait: page 1 has "GE.25-15926 (E)" — starts with "GE." ✓. Date stamp "051125 061125" — 6-digit groups ✓. Page number bare equal to page ✓. Note: page 1 has no page number; expected all but first ✓.

Also careful: trimming could turn "   " into "" — blank. Fine.

Concatenate body lines:
```js
const body=[]; // {page,text}
for(const pb of pageBodies) for(const t of pb.lines) if(t!=='') body.push({page:pb.page,text:t});
```
Hmm but I need blanks for "immediately followed by paragraph-start" — blanks removed; "immediately followed" among non-empty lines is fine (a blank between heading and paragraph start still means next non-empty is para start). Labelled heading "skip blank lines" — handled.

But "A line starting with a lowercase letter or '(' continues the previous heading line" — within heading collection.

Blank line counting for "nothing lost": only non-empty lines classified. Cover: non-empty lines before first paragraph start... but headings also occur there? Cover is everything before first para start including headings? "Lines before the first paragraph start are the cover." I'll classify pre-first-para lines as cover, except... first para is "1." near start; headings come after. Cover = lines before paragraph 1. OK.

Paragraph start regex:
```js
const reAlone=/^(\d{1,3})\.$/;
const reWith=/^(\d{1,3})\. (.+)$/;
```

Labelled heading label: /^([IVX]+|[A-Z])\.$/

Unlabelled heading test for line at index i in body (non-empty): next non-empty? Since I removed empties, body[i+1] is next non-empty. Test: body[i+1] is paragraph start; body[i].text.length<=90; /^[A-Z]/; !/[.;:,\d]$/.test(text). Note also body[i] must not itself be a paragraph start or label line (para start starts with digit; label is like "A." — "A." ends with '.', fails test since ends with '.'? "A." ends with full stop → fails unlabelled test ✓).

Two-line: if i>0 and body[i-1] passes heading text test (capital, ≤90, not ending .;:,digit) and body[i-1] not classified as something else... "does not end a paragraph sentence" — same as the punctuation test. But body[i-1] might be a paragraph-start's text line? Paragraph-start-with-text line: "23. The Committee..." starts with digit — fails capital test. Good. But body[i-1] could be a normal paragraph line mid-sentence ("of the Covenant") — lowercase, fails. A paragraph line starting with capital and not ending punctuation... could be wrongly joined. Risk accepted per spec. But guard: body[i-1] must not be a paragraph start line, label line, or already a heading. I'll do classification in one pass with lookahead computed first.

Let me precompute flags array:
```js
const isParaStart = body.map(l=> reAlone.test(l.text)||reWith.test(l.text));
const isLabel = body.map(l=>/^([IVX]+|[A-Z])\.$/.test(l.text));
function headingTextOK(t){return t.length<=90 && /^[A-Z]/.test(t) && !/[.;:,\d]$/.test(t);}
const isUnlabelled = body.map((l,i)=> !isParaStart[i] && !isLabel[i] && i+1<body.length && isParaStart[i+1] && headingTextOK(l.text));
```
Two-line: when emitting unlabelled heading at i, check i-1: !isParaStart[i-1] && !isLabel[i-1] && !isUnlabelled[i-1] && headingTextOK(body[i-1].text) — and also i-1 must be before first paragraph start (cover region?) Hmm if body[i-1] is a paragraph line that happens to pass, we'd steal it. "does not end a paragraph sentence" — the punctuation test covers that mostly. Also require body[i-1] not already consumed. I'll track consumption in main walk and decide there.

Main walk:
```js
const paras=[], headingsSeq=[]; // headingsSeq: {level:1|2, text}
let cur=null, section=null, part=null;
let clsCount={cover:0,heading:0,paragraph:0};
let firstParaIdx = body.findIndex((l,i)=>isParaStart[i]);
const unclassified=[];
let i=0;
const hyphenEnd = body.filter(l=>/-$/.test(l.text.replace(/\s+$/,''))).length; // count lines ending with hyphen
for(i=0;i<body.length;i++){
  const l=body[i];
  if(i<firstParaIdx){clsCount.cover++;continue;}
  if(isParaStart[i]){
    const m=reAlone.exec(l.text)||reWith.exec(l.text);
    cur={paragraph:+m[1], lines:[], section, part, pageStart:l.page,pageEnd:l.page, flagged:false, suspectCount:0};
    paras.push(cur);
    if(m[2]) cur.lines.push({page:l.page,text:m[2]});
    clsCount.paragraph++;
    continue;
  }
  if(isLabel[i]){
    const roman=/^[IVX]+$/.test(l.text);
    clsCount.heading++;
    let title=[];
    let j=i+1;
    while(j<body.length && !isParaStart[j] && !isLabel[j]){
      const t=body[j].text;
      if(title.length && (/^[a-z(]/.test(t))){ title[title.length-1]+=' '+t; }
      else title.push(t);
      clsCount.heading++;
      j++;
    }
    const text=title.join(' ');
    headingsSeq.push({level:roman?1:2,text});
    if(roman){part=text;section=null;} else section=text;
    cur=null; // heading ends current paragraph? Actually paragraph already ended... spec: paragraphs end at next paragraph start presumably; but a heading after paragraph text — remaining lines are heading. Set cur=null so stray lines don't append. But footnote lines before a heading on the next page would come *before* the label line, so they belong to cur. Fine.
    i=j-1;
    continue;
  }
  if(isUnlabelled[i]){
    let text=l.text;
    clsCount.heading++;
    if(i-1>=firstParaIdx && !isParaStart[i-1] && !isLabel[i-1] && headingTextOK(body[i-1].text) && bodyLineIsParagraphText... 
```
Hmm, for the two-line case, body[i-1] was already classified as paragraph line in a previous iteration (since we walk forward). I need to handle: if it qualifies, pop it from cur.lines and decrement paragraph count, increment heading. But only if it "does not end a paragraph sentence" — headingTextOK covers. Also must not be the first line of a paragraph-with-text (that line starts with digit — excluded). Also only if body[i-1] was classified as paragraph (i.e., i-1 > firstParaIdx and it went into cur). If i-1 < firstParaIdx it's cover — a cover line before para 1... e.g. cover lines like "Committee on Economic, Social and Cultural Rights" — but first paragraph comes right after intro heading, so cover ends before. Edge case: what if the unlabelled heading's second line is in cover? Then it stays cover. I'll only merge if it was added to cur (cur && cur.lines.length && last line matches body[i-1]).

```js
    if(cur && body[i-1] && !isParaStart[i-1] && !isLabel[i-1] && headingTextOK(body[i-1].text)){
      const prev=cur.lines[cur.lines.length-1];
      if(prev && prev.page===body[i-1].page && prev.text===body[i-1].text){
        cur.lines.pop(); clsCount.paragraph--; clsCount.heading++;
        text=body[i-1].text+' '+text;
      }
    }
    headingsSeq.push({level:2,text});
    section=text;
    cur=null;
    continue;
  }
  // paragraph line
  if(cur){cur.lines.push({page:l.page,text:l.text}); clsCount.paragraph++;}
  else unclassified.push({page:l.page,text:l.text});
}
```

Wait, issue: unlabelled heading where the two lines are both before it — my isUnlabelled marks line i; the pair line i-1 merge handled above. But what about when line i-1 is itself flagged isUnlabelled? Can't be: isUnlabelled[i-1] requires isParaStart[i], and isParaStart[i] is true here (since isUnlabelled[i] requires it) — wait isUnlabelled[i-1] requires body[i] to be para start; body[i] is the heading line, not para start (starts with capital). So no.

Also note: paragraphs spanning page breaks — handled since body concatenated.

Suspect detection on paragraph lines:
```js
function suspectReason(t){
  if(/^\d{1,3}$/.test(t)) return 'bare number';
  const m=/^(\d{1,3}) (.+)$/.exec(t);
  if(m && /^[A-Z"“]/.test(m[2])) return 'starts with a number and a space';
  if(/^\* /.test(t)) return 'asterisk note';
  return null;
}
```
"starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark" — UN symbol E/2003/22 starts with 'E' — capital covers. OK.

Mark to end of page: per paragraph, iterate lines; once suspect found with page p, all subsequent lines with page===p are suspect too (reason 'same page as a footnote line' — I'll use 'after a suspect line on this page'). Note lines across the paragraph could span pages; suspect spread only within same page.

Also paragraphs' first injected text line (from reWith) — could be suspect? It's the paragraph's own text; number has full stop so not suspect by rules (rule requires no full stop / digit-space-capital — "23. The..." starts "23." then... my regex ^\d{1,3} (.+) requires digits then space, "23. The" has "23." — no match ✓).

Hmm but a paragraph line like "17 Sustainable Development Goals are..." mid-paragraph → suspect (documented risk). Fine.

Word count >300: text.split(/\s+/).length>300 → flagged with reason 'paragraph over 300 words'. But that doesn't make lines suspect; for flagged-pages table "why" only line-level reasons. Paragraph-level flag shows on tab 02 and in paragraph's flagged status. For flagged pages table, only pages with suspect lines are flagged (spec: "A page is flagged when it has a suspect line inside a paragraph"). OK so >300 words flags paragraph but not page.

Paragraph text: lines joined ' ', collapse double spaces, trim.
pageStart = lines[0].page (or label line page if no lines), pageEnd = last line page.

First words:
```js
function stripFootnoteMarks(text){
  const toks=text.split(/\s+/); const out=[];
  for(const t0 of toks){
    let t=t0;
    if(/^\d+$/.test(t)){
      const prev=out.length?out[out.length-1]:null;
      if(prev && /[.,”"’',)]$/.test(prev) && !/^(no|art|para|p)\.$/i.test(prev)) continue; // dropped
      out.push(t); continue;
    }
    t=t.replace(/\d+$/,''); // cut glued digits
    if(t) out.push(t);
  }
  return out;
}
```
Wait "cut glued digits" — "waste.2"→"waste.". But what about a legit word ending in digits mid-six-words? e.g. "COVID-19"? replace gives "COVID-" hmm. Rare; spec says do it. But careful: only cut when there's something before digits: /\d+$/ on "COVID-19" → "COVID-". Accept per spec.

Hmm, but "closing quote" in the drop condition — prev ends with '”' etc. Included.

first six: out.slice(0,6).join(' ').

Normalization for compare: replace curly quotes ’‘“” → straight, –— → '-', collapse whitespace:
```js
const norm=s=>s.replace(/[’‘]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
```

Compare: ref.first_words[String(n)].

Checks list:
```js
const checks=[];
checks.push({name:'Paragraph count', ...});
```
Each check: {label, detail(html), pass (true/false/null)}.

1. Paragraph count: found vs ref.paragraphs. pass if equal. If no ref: 'not run'.
2. Numbering: expected 1..found.length sequence; check paras numbers equal index+1; gaps/dups: build multiset. pass if exactly 1..n.
3. First words: n of ref count match; pass if mismatches===0. If no ref: not run. If found count != ref... still run per found.
4. Pages flagged: info, pass true.
5. Suspect lines: info counts, pass true.
6. Headers and footers: pages with symbol first line (expected all = recs.length), pages with page number (expected recs.length-1... or all but first — use recs.length - (recs.some page1? ) I'll compute expected = recs.length - 1 assuming page 1 has none; but safer: expected all but the first page. detail shows values; pass if matches. Bare numbers removed listed. Combine into one check line? Spec: "Headers and footers. Pages whose first line was the symbol (expected all); pages with a page number in the footer (expected all but the first); bare numbers removed from the footer, listed with their page." One check line with all three; pass if both expectations hold.
7. Headings: counts labelled/unlabelled, unlabelled listed. Info, pass true.
8. Nothing lost: total non-empty lines across pages (raw, after trim, non-empty) = header + footer + cover + heading + paragraph. footer count: count dropped footer lines (non-empty). header count: headerPages (1 per page where dropped; headerWarn pages 0). unclassified list. pass if unclassified empty and sum matches.

Careful: total non-empty lines = sum over pages of non-empty raw lines. Classified: header (pages where first line == symbol), footer (dropped non-empty lines), cover, heading (clsCount.heading includes label lines and heading text lines and merged second lines), paragraph. Verify sum.

9. Export round trip: parse JSON string of records, length === paras.length.

Dot in header: passCount + " of " + checks.length + " checks pass" green if all non-null pass and no failures; red if any fail. If some null... show pass count anyway.

Rail:
- card: symbol + short title (title — maybe first heading-ish; use D.title).
- big number: paras found "of reference.paragraphs", thin bar red when mismatch.
- pages flagged big number red when >0.
- checks pass line.

Tab 01 tiles: 4 tiles as described. Mismatch list under tiles (first words differ), max 10 lines + "and n more".

Buttons Download JSON / Markdown; disabled if no paragraphs.

Export records:
```js
function exportRecords(){
  return paras.map(p=>({
    symbol, paragraph:p.paragraph, section:p.section, part:p.part,
    page_start:p.pageStart, page_end:p.pageEnd, text:p.text,
    flagged:p.flagged, first_words_match:p.fwMatch,
    citation: symbol+', para. '+p.paragraph, doc_url:D.doc_url,
    limitations: p.flagged? 'footnotes not separated; '+(p.suspectCount||'footnote text')+' may sit inside this paragraph'...
```
Spec: limitations: "footnotes not separated; n may sit inside this paragraph" for flagged (n = ? probably n suspect lines? or footnote count?). "n may sit inside this paragraph" — I'll use number of suspect lines: "footnotes not separated; 3 footnote lines may sit inside this paragraph". Hmm spec literal: "footnotes not separated; n may sit inside this paragraph". n ambiguous; use suspect line count. Else "footnotes not separated".

Markdown: front matter keys: title, symbol, adopted, source_url, extracted (today ISO), paragraphs_found, paragraphs_expected, pages_flagged, footnotes: "not separated; the document has n". Then stream: I'll build ordered items from headingsSeq and paras. But headingsSeq order vs paras order: headings encountered in walk are in order. Combine: during walk push to `stream` both. Simpler: build stream after: iterate i over body in walk order... I recorded headingsSeq separately without positions. Let me push headings into a stream during walk: stream.push({type:'h',level,text}) and for each para stream.push({type:'p',para}). Then markdown: for h emit '#'.repeat(level+1) (level1 roman → ##, level2 → ###). For p: `**${n}** ${text}` + flagged note. Skip consecutive headings where nothing between? Keep all; fine.

Actually part headings (roman) are level 1, lettered subsections level 2, unlabelled also level 2 — but an unlabelled under a part without lettered subsection: fine.

Edge: heading immediately followed by heading (part then subsection) — both emitted. OK.

Download: Blob + a.download, URL.createObjectURL.

Tab 02: 
- closed "Headings found: n" box: list headings with type.
- table: caption, th: No | Section | Page | First line | Check. Rows: button aria-expanded; expanded row (extra tr) shows full text with suspect spans, reference vs found six words, toggle "Show the PDF's lines", copy citation button.

Rendering paragraphs table: could be 90 rows — fine.

Expanded: 
```
<div class="para-full">spans per line joined with space</div>
found six vs ref six
<button toggle lines>
<div class="lines" hidden>each line: [p3] text (suspect highlighted)</div>
<button copy>
```

Tab 01 flagged pages panel: closed heading, note, table rows expandable showing raw page body lines with suspects highlighted + which paragraph. For raw page lines I need page body lines and their suspect status. Suspect status computed per paragraph lines; page body lines not in any paragraph (cover/headings) not suspect. I'll build per page: for each line in pageBodies, find if it's a suspect paragraph line — map by reference. Simpler: build suspectLinesByPage from paras: for each flagged para, its suspect lines with page. For the page view, show all body lines of the page, highlighting those whose text matches a suspect line entry (match by text+page; store suspect set as Set of `${page}|${text}`). Careful: identical texts unlikely; fine.

Suspect lines count per page and why: for flagged page row: Paragraph(s) (paras with suspects on that page), Suspect lines (texts, first few), Why (reasons).

Now the header dot & flagged pages count in header: "n pages flagged".

Tabs keyboard: arrow keys move focus & select.

Copy to clipboard with fallback.

Let me also compute: pagesFlagged = set of pages with any suspect paragraph line.

Also "n of the document's pages" tiles: total pages = recs.length.

Now write it. Keep design: off-white bg, Georgia serif, monospace labels, red accent, green for pass (#2e6b3a maybe, contrast ok).

CSS quickly:
- body layout, header, tabs buttons, rail, tiles grid, tables, buttons, chips? no filters needed.
- [hidden]{display:none!important}

Focus ring: :focus-visible outline 2px solid #9b2335.

Let me now write the full HTML. I'll be careful with edit-uniqueness not needed (new file).

Rail bar: thin bar width = found/expected*100%, red when mismatch else neutral dark.

Write code:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF — General comment No. 27</title>
<style>
:root{--ink:#1d1b18;--paper:#f4f0e8;--rule:#d9d2c3;--red:#9b2335;--green:#2e6b3a;}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
a{color:var(--red)}
.mono{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}
header.site{padding:18px 24px 12px;border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
h1{font:600 28px/1.2 Georgia,"Times New Roman",serif;margin:4px 0 2px}
.meta{font-size:13px;color:#555}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;vertical-align:-1px}
.dot.ok{background:var(--green)} .dot.bad{background:var(--red)}
.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);padding:0 24px}
.tab{appearance:none;background:none;border:none;border-bottom:3px solid transparent;padding:10px 16px 8px;cursor:pointer;font:12px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;color:#555}
.tab[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tab:focus-visible,button:focus-visible{outline:2px solid var(--red);outline-offset:2px}
.layout{display:flex;gap:0;align-items:flex-start}
aside{width:250px;flex:none;border-right:1px solid var(--rule);padding:18px 20px}
main{flex:1;padding:18px 28px;min-width:0}
.bignum{font:600 46px/1 Georgia,serif;margin:2px 0}
...
```

Fine, I'll write it out fully now.

Footer: source, built, honesty line.

Note D.built may exist. `built` in pdf_text? Description says title, symbol, doc_url, source, count, records, reference. No built. Spec footer says source, built... I'll show built if present else skip. I'll include `D.built` if exists.

Count checks for header dot: passCount/checks.

Edge: ref missing — handle refHas = !!(D.reference && D.reference.paragraphs).

For "First words match: n of reference.paragraphs" tile: if no ref: "no reference in this file".

Write the JS pipeline carefully.

Also note the paragraph-start line for reWith case: line text includes the number; the injected text line m[2] — but classification count: that line counts once as paragraph (I count clsCount.paragraph++ once for the start line). ✓. But the injected text — is it "paragraph line"? Yes, one line total.

Also suspect check should apply to the injected first line too? E.g., "23. 7 E/2003..."? Unlikely; but run suspect check over all lines including injected (its text has no leading number now). I'll include it — but careful: the injected line could start with digits+space+capital legitimately? That'd be paragraph content starting "23. 17 Sustainable..." — suspect flagged, costing a look; acceptable. Actually wait — a paragraph-start-with-text line whose text starts with a number, like "60. Article 2..."? Not suspect (capital A... "Article" capital → "starts with number and space"? the injected text "Article 2" doesn't start with digits). OK.

Hmm one more: paragraph 24 etc "start with real numbers": e.g. "24. 2 The Committee..."? Then injected text "2 The Committee" → bare-number rule? Not bare; "2 The" = digits space capital → suspect → flagged + first words: "2" is first token, digit-only, prev null → kept; "The" capital... token "2" kept, "The"... first six: "2 The Committee..." vs reference "2 The Committee..." — wait reference's first words would be "2 The Committee also..." Hmm but stripFootnoteMarks: token "2": /^\d+$/ yes, prev null → push. Good. But suspect flag on it — false positive, acceptable per spec ("a line of real paragraph text may start with a number and a space... it is flagged").

Hmm wait, but "24. 2 The" — is that how it appears? Spec says paragraphs 24, 27, 46, 60 start with real numbers, "article 2" or "No. 3". Maybe like "24. Article 2 of the Covenant..." Fine either way.

Suspect spread to end of page: implement per paragraph:
```js
for(const p of paras){
  let pageSuspect=false, lastSuspectPage=null;
  for(const ln of p.lines){
    if(ln.suspect) ... 
```
Process sequentially:
```js
let spread=false;
for(const ln of p.lines){
  if(!spread){const r=suspectReason(ln.text); if(r){ln.suspect=true;ln.reason=r;spread=true;ln.spreadPage=ln.page;}}
  else if(ln.page===prevSuspectPage){ln.suspect=true;ln.reason='continues a footnote block on this page';}
  else spread=false... 
```
Careful: spread only until page changes. Implement: 
```js
for(let k=0;k<p.lines.length;k++){
  const ln=p.lines[k];
  const r=suspectReason(ln.text);
  if(r){ln.suspect=true;ln.reason=r;
    let m=k+1;
    while(m<p.lines.length && p.lines[m].page===ln.page){p.lines[m].suspect=true;p.lines[m].reason='same page, after a suspect line';m++;}
    k=m-1;
  }
}
```
Good.

p.suspectCount = lines.filter(suspect).length. flagged = suspectCount>0 || wordCount>300. For over-300, store p.longFlag=true.

Suspect lines total & pages & paragraphs stats.

Now headings list for check: labelled count = headingsSeq where from labels... I need to distinguish. Track during walk: labelledHeadings list, unlabelledHeadings list. 

Now "Nothing lost": count lines per classification. Header count: number of pages where first non-empty line == symbol (each = 1 line). What about headerWarn pages — their first line not symbol, that line goes into body as cover/paragraph — fine, counted there. Footer: count non-empty lines dropped in footer loop. Cover/heading/paragraph from clsCount. Total non-empty = sum over raw pages. unclassified lines: those with cur==null after headings etc (e.g., paragraph text after a heading before any paragraph start — post-first-para). Wait: after a heading, cur=null; if next lines are paragraph text (not para start, not heading) they'd be unclassified — but in reality paragraph lines only follow a paragraph start. Except footnote lines? Footnotes follow paragraph text, cur still open. After a heading, next should be paragraph start or another heading. OK. But also: lines between paragraph N's end and next paragraph start that aren't headings → they'd be appended to paragraph N (cur stays open). That's the design (footnotes into paragraph N). ✓.

But one subtlety: cur stays open across headings? I set cur=null at headings. After paragraph N, if a *labelled* heading comes, cur=null; any stray lines then are unclassified. Fine, they're listed.

Also note: paragraph continues across page break: on the new page, body lines (footnote lines of previous page already appended) then continuing paragraph text appended. ✓.

Check the unclassified counting: in walk, the "paragraph line" branch when cur==null → unclassified.push. But cover branch handles i<firstParaIdx. Note firstParaIdx could be -1 (no paragraphs) → everything cover. Handle: if firstParaIdx===-1 set to body.length.

Export round trip check: JSON.parse(jsonString).length===paras.length.

First words mismatch list for tiles.

Now rendering. I'll build with template strings and innerHTML mostly, with event delegation.

Tabs: two buttons + panels; arrow keys.

Rail content: computed.

Tiles: 4 divs.

Buttons: download handlers.

Closed headings (details-like): custom buttons with aria-expanded toggling a div.

Flagged pages table: rows as buttons expanding a raw-lines view row.

Tab 02 rows: build all rows; expand toggles.

Copy citation:
```js
function copyText(s,btn){ 
 const done=()=>{btn.textContent='Copied';setTimeout(()=>btn.textContent='Copy citation',2000);};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s).then(done).catch(()=>fallback());}else fallback();
 function fallback(){const ta=document.createElement('textarea');ta.value=s;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);done();}
}
```

Markdown escape: fine.

Let me count "things to click" — fine.

Now write everything. I'll aim for clarity over micro-detail. Begin.

Also table caption serif with monospace number.

Let me write the final file now, then 2-3 sentence intro.

One more detail: header line "n pages flagged" at right after dot.

Rail "n paragraphs of reference.paragraphs" — bar: width % = min(100, found/expected*100); red if found!==expected.

Tile 1 side-by-side "the document has reference.paragraphs".

Write:

For tiles grid: grid-template-columns repeat(auto-fit,minmax(220px,1fr)).

Flagged pages table "Why": join unique reasons.

Page raw lines display: iterate pageBodies find page; lines each `<div>` with [pN] prefix? "the page's raw lines with the suspect ones highlighted and the paragraph they sit in" — show paragraph number for suspect lines. I'll show each line; suspect ones highlighted with the paragraph number appended.

Suspect set: build map key `${page}::${text}` → para number.

OK writing now. Also, remember tab 02 "Headings found: n" closed box above the table listing headings (type: part/subsection/heading).

Section full path in expanded row: `${p.part} › ${p.section}` (part may equal section? no, part is roman).

Check row "Section": nearest heading = section (or part if no section).

Alright. Also ensure I never hardcode counts.

Let me draft the JS fully in my head as I write. Time to produce output.

Length: probably ~850 lines. Acceptable.

One more: "First words match" check line links to rows concerned — link "rows concerned" for failed checks: I'll add a link that switches to tab 02 and highlights? Simpler: a link that opens tab 02. I'll make links with data-goto="tab2" that activate tab 02. Good enough ("a link to the rows concerned" — activate tab 02 and maybe filter? I'll just switch tab).

Also paragraphs table when many rows: all shown, fine.

Now, `ref.adopted` shown in header.

Write the code.