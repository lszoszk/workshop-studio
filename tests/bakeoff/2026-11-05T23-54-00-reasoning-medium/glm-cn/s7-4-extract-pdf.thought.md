Build the full app per spec. Single HTML file, ~700-900 lines. Let me write it carefully.

Key pipeline:
- pages sorted by page.
- per page: split text by lines (\n). Header: first non-empty line == symbol → drop, else warning.
- Footer: from end, drop lines while empty, /^GE\./, only 6-digit groups (/^(\d{6}(\s+\d{6})*)$/), or bare number 1-3 digits. Track page-number vs other bare numbers.
- Body lines concatenated with page tags.
- Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.
- Cover: lines before first paragraph start... but heading detection also applies. Cover lines classified as cover until first paragraph start.
- Headings: /^([IVX]+|[A-Z])\.$/ labelled. Unlabelled: non-empty line immediately followed by paragraph-start line, ≤90 chars, starts with capital, not ending .;:,digit; two-line heading merge when line before also passes test and doesn't end a paragraph sentence. Simplify: when checking line L followed by paragraph start, if line before L passes same test and doesn't end paragraph sentence, both are one heading (and the line before must not itself be immediately before... hmm, it is before L which is before para start, fine).
- Suspect lines: bare number 1-3 digits (no full stop), or /^\d{1,3} [A-Z"/]/... spec: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". So regex /^\d{1,3} (?:[A-Z"]|E\/|A\/|CCPR|CERD)/ roughly — "capital letter, a UN document symbol or a quotation mark". UN doc symbols start with capital letters anyway (A/, E/). So /^\d{1,3} [A-Z"“]/. Or asterisk: /^\* /.
- Suspect propagation: from a suspect line to end of its page, all lines suspect.
- Paragraph >300 words flagged.
- Page flagged when suspect line inside a paragraph on that page.
- First words: strip footnote marks: digits glued to end of word/punctuation cut; lone digit token dropped only when previous token ends with . , or closing quote and not "No."/"art.".
- Checks: paragraph count vs reference, numbering 1..n, first words mismatches, pages flagged, suspect lines stats, headers/footers stats, headings counts, nothing-lost classification counts, export round trip.

Classification count for "nothing lost": every non-empty line of every page classified exactly once as cover, header, heading, paragraph, footer. I'll track counts: header (dropped symbol lines), footer (dropped footer lines), cover (body lines before first para start, excluding headings? cover lines before first paragraph start — but the intro heading "I." appears before paragraph 1. Hmm, actually cover per spec: "Lines before the first paragraph start are the cover." But headings before para 1... I. Introduction heading is before paragraph 1. Spec says cover. But also "Each paragraph's section is the most recent heading before it" — headings can be before first para. I'll classify labelled/unlabelled heading lines as headings even before first paragraph; remaining pre-first-para lines are cover. That's fine; nothing-lost just needs each line classified once. Blank lines skipped (non-empty lines only counted).

For unlabelled heading detection, need to scan body line array; heading if next line is paragraph start. Also labelled headings consume lines until next label or paragraph start.

Implementation approach: iterate over body lines (array of {text, page, index}). Build a classification array. Then walk:

```
for i in body:
  if label line (roman/letter): start labelled heading, consume lines j: skip blanks; collect lines while not label && not paraStart && not unlabelled-heading? Spec: "every line up to the next label line or paragraph start is heading text". Blank lines within skipped. A line starting lowercase or "(" continues previous heading line (that's just about joining—heading text may wrap; also means don't treat as new... they're all heading text anyway).
```

Simplest: classify all lines first:
- isParaStart(line)
- isLabel(line)
Then walk sequentially:
- If isLabel: mark as heading-label; then following non-blank lines until next isLabel or isParaStart (or EOF) are heading text. But an unlabelled heading immediately before a para start... can an unlabelled heading follow a labelled heading text before a para start? E.g. "I." blank "Introduction" then para 1 — Introduction is heading text under label. Unlabelled headings appear elsewhere. Edge: heading text collection could swallow an unlabelled heading that sits between a labelled heading and a paragraph — unlikely; acceptable.
- Unlabelled: non-blank line where next non-blank line is paraStart, passes the char test. Also two-line: if line before passes test too and doesn't end paragraph sentence, both are heading. When walking, if line is unlabelled-heading, mark it and possibly the line before. To avoid conflicts, do labelled pass first, then unlabelled: a line is unlabelled heading if not already classified (heading/footer/paraStart line) and next non-blank line is paraStart... wait paraStart lines are paragraph lines themselves. Actually para start line belongs to the paragraph.

Hmm — is a paragraph-start line "paragraph" classification? Yes. Also the unlabelled heading test: line followed by para-start line, so check body[i+1] skipping blanks is paraStart.

Two-line unlabelled: line L is unlabelled heading; check body line before L (skipping blanks), if it passes the same test (≤90, capital start, not ending .;:,digit) and "does not end a paragraph sentence" — interpret: previous line doesn't end with '.' etc., which the test already covers partially. Test says "does not end a paragraph sentence" — a line ending without terminal punctuation likely continues. I'll take: previous line ends with no terminal punctuation (., ;, :) OR ends with a comma? The heading test excludes lines ending . ; : , digit. So previous candidate must pass the same test. If it does, mark it heading too (if unclassified). But careful: previous paragraph's last line usually ends with '.', so excluded. Good.

But what if previous line is already classified as heading text (from a labelled heading)? Skip then.

Then: paragraphs: paraStart begins a paragraph; subsequent lines (non-blank, not classified as heading, not paraStart, not label) are paragraph lines. Wait — unlabelled heading line appears immediately before para start, so during paragraph collection, when we hit a heading-classified line, the current paragraph ends? A heading between paragraphs. Spec: "A heading line is never paragraph text." So when collecting paragraph lines, stop at heading lines (they belong between paragraphs). Since headings only occur adjacent to para starts (unlabelled) or at section boundaries, just: while walking, if line is heading → close current paragraph, emit heading context.

Cover: body lines before first paraStart that aren't headings.

Now footnotes intermixed: footnote lines are body lines and belong to current paragraph (per "footnote lines included"), including "7 E/2003/22..." — these are body lines, part of paragraph text. Yes: "Body lines of all pages are concatenated (every line that is not header or footer, footnote lines included)".

Suspect detection: for each paragraph line: bare number /^\d{1,3}$/, or /^\d{1,3} [A-Z"“]/ or /^\* /. Once a suspect line found on a page (within a paragraph), all subsequent lines on that same page (within paragraphs) are suspect. Implement: suspect if any earlier-or-same line on same page is suspect-trigger, recursively. Simpler: compute per page: find first suspect-trigger line index (in body, among paragraph lines); then all paragraph lines on that page from that index onward are suspect.

Flagged paragraph: has suspect lines OR >300 words.

Page flagged: has suspect lines inside a paragraph on that page.

First words: from text, tokenize; process footnote marks. Implement per spec:
- For each of first tokens: if token has digits glued at end after word/punctuation ("waste.2") → cut digits at end: replace /\d+$/ with ''.
- Lone digit token: drop only when previous token exists and previous ends with '.', ',' or closing quote (” ’ " ') and previous is not "No." or "art." (case-insensitive? keep "No." and "art."). Collect six words after processing. Take more tokens if needed (loop until 6 words or tokens exhausted).

Compare with reference first_words[str]: normalize: curly→straight quotes (’‘→', “”→"), en/em dash (–—) → '-', whitespace runs → one space. Compare strings.

Note: also cut digits glued to closing quote like "”. 3"? Spec: "digits glued to the end of a word or a punctuation mark are cut". So token ending in digits after non-digit: strip trailing digit run. But tokens like "17" pure digits handled separately. Token "art.2"? strip → "art.". Fine.

Also the found first words should strip footnote marks before comparing. The reference first words are like "A clean, healthy and sustainable" — six words.

Edge: paragraph starting with real number "article 2" — "article" is word 1, "2" lone digit after "article" (doesn't end with ./,") so kept. "No. 3": "No." ends with '.' but is abbreviation exception → "3" kept. Good.

Header check: pages whose first non-empty line equals symbol.

Footer: loop from end while line matches drop conditions. Note bare number 1-3 digits in footer = page number or displaced footnote number.

Hyphen-ending lines count: lines (body?) ending with '-' — count and report.

text export fields: symbol, paragraph, section, part, page_start, page_end, text, flagged, first_words_match, citation, doc_url, limitations, text_lines (lines joined " | ").

Markdown: front matter, then headings in document order as ## (roman/labelled) and ### (unlabelled?) — "the headings as ## and ### lines in document order". Labelled (parts) = ##, unlabelled (sections) = ###. Paragraphs as "**n** text" with "(flagged...)" suffix.

Need ordered heading list during walk: record headings as encountered with their type.

UI: header, rail, tabs 01/02, tab01 tiles, mismatch list, download buttons, two collapsible: Every check, Flagged pages. Tab02: collapsible "Headings found: n", table with expandable rows, copy citation, "Show the PDF's lines" toggle.

Chart.js? Not needed — no chart required by plan. Plan mentions thin bar for paragraphs ratio — CSS bar, fine. No Chart needed. The system says use Chart.js for charts, but this plan has none.

Arrow-key tablist. Buttons aria-expanded. [hidden]{display:none!important}.

Copy: navigator.clipboard may fail in sandbox; fallback textarea+execCommand.

Now write the code. Aim ~900 lines.

Data structures:
```
const D = WORKSHOP_DATA.pdf_text;
const pages = [...D.records].sort((a,b)=>a.page-b.page);
```

Parsing per page lines: text.split(/\r?\n/).

Classification per page: produce bodyLines = [{text,page,raw index}], and footerDropped info.

Let me code the walk:

```
const body = []; // {text, page, cls: null}
for each page: lines; header removed; footer removal from end; remaining lines pushed (including blanks, keep them for indexing but mark blank).
```

Precompute for each body index: isBlank, isParaStart (with m), isLabel.

isParaStart: /^(\d{1,3})\.$/ → {num, text:null}; /^(\d{1,3})\. (.+)$/ → {num, text}.
isLabel: /^([IVX]+|[A-Z])\.$/.

Walk:
```
let sections = []; // ordered {level: 'part'|'section', label, text}
let curPart='', curSection='';
let paragraphs = []; let cur=null; let coverCount=0;
i=0;
while(i<body.length){
  const L=body[i];
  if(L.blank){i++;continue;}
  if(isLabel(L)){
    // labelled heading
    let label=L.text;
    i++;
    let words=[];
    while(i<body.length && !body[i].label && !body[i].paraStart){
      if(!body[i].blank) words.push(body[i].text);
      body[i].cls='heading';
      i++;
    }
    // wait: this would classify lines as heading even before... if cur paragraph open? Label shouldn't appear mid-paragraph. Close cur if open? Actually label line itself: close cur first.
```
Hmm, need to close current paragraph when hitting a heading. But labelled heading following paragraph text — the label line ends the paragraph. Since blank lines dropped from paragraph... Actually blank lines dropped; a paragraph is followed by blank, then heading. If cur open and we hit label, close cur.

Also careful: the while collecting heading text should stop at blank? No, skip blanks. But could swallow cover content? Labelled headings appear after cover typically at start. Fine.

Also stop heading-text collection at unlabelled heading? An unlabelled heading is immediately before paraStart, so collection stops at paraStart anyway. Good.

```
    curPart = label + ' ' + words.join(' ') -> actually part = roman heading text; section = same initially? Spec: section = nearest heading (could be part), part = nearest roman heading.
    sections.push({level:'part', label, text: (label+' '+words.join(' ')).trim(), lineIdx:i})
    curSection = same text.
```

Wait but for lettered subsection "A." the part stays. section = the subsection.

Unlabelled heading: detected during main walk too: line non-blank, not paraStart, not label, passes test, and next non-blank line is paraStart. And previous-line merge.

Main walk order: handle label first, then paraStart, then unlabelled-heading, then paragraph text.

For unlabelled detection at walk time, need helper nextNonBlank(i). And prevNonBlank check for two-line merge — but previous line may already be consumed as paragraph text of cur. Two-line heading: "the line before it passes the same test and does not end a paragraph sentence" — the previous line was already added to cur paragraph potentially. Hmm. Better: pre-classify unlabelled headings before the walk? But labelled heading text collection interacts. Let me precompute:

Pass 1: mark label lines and paraStart lines.
Pass 2: labelled heading text: for each label line, extend forward until next label/paraStart/EOF, marking cls='heading' (label itself cls='heading').
Pass 3: unlabelled: for i where cls==null, non-blank, passes test, nextNonBlank is paraStart → mark 'heading'; if prevNonBlank line cls==null and passes test (and doesn't end paragraph sentence — test covers: not ending .;:, digit) → mark 'heading' too.
Pass 4: walk in order building paragraphs, cover, and ordered heading list (need order & hierarchy):

```
cur=null; 
for i:
  blank -> skip
  if cls=='heading' and it's a label line (isLabel) -> close cur; curPart=..., curSection=...; push ordered heading {level:'part'}
  else if cls=='heading' (text of labelled OR unlabelled):
     For labelled heading text lines we already captured? Better capture labelled heading text during pass 2 into a map from label index to {label, text}. Then in walk, when hitting label line, emit part heading. For unlabelled heading line, emit section heading.
     close cur; curSection = line text (for unlabelled, possibly merged two lines — need the merged text).
```
For merged unlabelled heading, the heading text = prevLine + ' ' + line (or just both lines). I'll store heading group text: when marking in pass 3, record a map idx->groupText.

For labelled heading text lines in walk: they're cls='heading' but not label; when encountered after label... The label handling consumes them in walk? Let me handle in walk: when label line encountered, close cur; then read following heading lines (cls=='heading' && !isLabel) joined → partText; curPart=curSection=that; push ordered {level:'part', text}. Then skip them. Simpler in a single walk if I know which heading lines are label-starters. OK:

Walk:
```
if(isLabel(line)){
  closeCur();
  let t=[line.text];
  i++;
  while(i<len && body[i].cls=='heading'){ if(!blank) t.push(text); i++; }
  const full=t.join(' '); // "I. Introduction"
  curPart=full; curSection=full; ordered.push({level:'part',text:full});
  continue;
}
if(body[i].cls=='heading'){ // unlabelled
  closeCur();
  curSection = headingTextMap[i];
  ordered.push({level:'section', text:curSection});
  i++; continue;
}
```
But labelled heading text lines after label: in walk they're consumed by the label branch. But what if labelled heading text line has cls heading and walk hits it independently (shouldn't, label branch consumes). OK.

Wait: pass 2 marks heading text lines after label until next label or paraStart — but blank lines within? Mark non-blank ones; blanks keep cls null but skipped in walk. However pass-2 range also could include lines that pass-3 would consider unlabelled headings — impossible since unlabelled must be immediately before paraStart and pass2 stops at paraStart... a line just before paraStart within a labelled heading range would be marked heading by pass 2 — that's correct (it's heading text under the label).

Hmm but there's a subtlety: labelled heading text could include the paragraph's preceding unlabelled heading — e.g. "I." blank "Introduction" blank "Right to work (art. 6)" blank "12. ..." — pass 2 would swallow "Right to work" as part of "I. Introduction" heading text. Does that happen in this doc? Cover has I. Introduction before para 1. Other labelled headings presumably followed directly by paragraphs. Risk acceptable but could mis-assign section. To mitigate: in pass 2, stop also at a line that would itself qualify as an unlabelled heading (next non-blank is paraStart and passes test) — but "Introduction" is followed by para 1... ugh. "Introduction" is followed by blank then "1." paraStart, so Introduction itself qualifies as unlabelled heading! Then pass 2 stopping at unlabelled-heading lines would stop immediately after the label.

Hmm. That means with my rule, "I." heading text collection stops at "Introduction" (which qualifies as unlabelled since next is paraStart "1."). Then walk: label "I." → text "" → part "I."; then "Introduction" as unlabelled section heading. That actually matches spec: part="I. Introduction"? No — part would be "I." and section "Introduction". Spec says part is the roman-numbered section, presumably "I. Introduction" text. Hmm.

Re-read spec: "A line matching /^([IVX]+|[A-Z])\.$/ opens a labelled heading: skip blank lines, then every line up to the next label line or paragraph start is heading text". So "I." collects "Introduction" (up to para start "1."). Then part = "I. Introduction". And "Introduction" is heading text of the labelled heading, not an unlabelled heading — even though it precedes a para start. So pass 2 takes precedence: lines consumed as labelled heading text are not unlabelled headings. My original design (pass 2 then pass 3 skipping cls!=null) is right per spec. The swallowing concern: if a doc had "IV." then blank "Right to work (art. 6)" then paragraph — that would become part text "IV. Right to work" and no section heading. Per spec that's what the rule says. Fine — spec-faithful.

part text: label + ' ' + words.join(' ')? For "I." + "Introduction" → "I. Introduction". Yes.

Now paragraph collection in walk:
```
if(paraStart){
  closeCur();
  cur={num, lines:[], ...}
  if(m.text) cur.lines.push({text:m.text,page});
  i++; continue;
}
// plain line
if(cur) cur.lines.push(line)
else coverCount++, cls='cover'
```
closeCur: paragraphs.push(cur) with text computed, etc.

Also classify: paragraph lines cls='para'. Nothing-lost counts: header, footer, cover, heading, para, plus unclassified (should be 0; blanks excluded).

Suspect: after paragraphs built, for each paragraph line, determine suspect via page-based rule. Build map: for each page, find earliest body index on that page (in paragraph lines) that triggers suspect; simpler: iterate paragraphs' lines in global order? Paragraph lines are in document order per paragraph, paragraphs in order — yes global order. So:

```
let pageFirstSuspect = {}; // page -> global seq index of first trigger
```
Iterate all paragraph lines in document order with seq counter; if line triggers and page not in map or... once a trigger found on a page, all later lines on that page are suspect. Track per page a flag "taint started". Since lines processed in order:
```
let tainted = {}; // page -> bool
for each para, each line:
  if(tainted[line.page] || triggers(line.text)){ tainted[line.page]=true; line.suspect=true; }
```
Wait if trigger, mark suspect and taint page. But taint should not cross to next page. tainted keyed per page, set when first trigger on that page; lines on other pages unaffected. But a trigger on page 3 late shouldn't taint page 3's earlier lines (already processed) — fine, only onward. Good.

But careful: paragraph spanning pages 3–4: footnotes at foot of page 3 taint rest of page 3 (the paragraph's page-3 lines) — correct per spec ("every line after it to the end of its page").

Suspect trigger regexes:
- /^\d{1,3}$/ (bare number)
- /^\d{1,3} [A-Z"“]/ — capital letter, UN symbol (starts with capital letter too), or quotation mark.
- /^\* /

Hmm "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark" — treat as digits-space-(capital|quote). UN symbols start with capital. OK.

Paragraph >300 words: text.split(/\s+/).length > 300.

First words per earlier plan.

Numbering check: found nums sorted should be 1..n exactly, in order (they are in document order; check sequence equals 1..n). Gaps/duplicates listed.

Now the checks list (build array of {name, story, valueA, valueB, pass, detail}):
1. Paragraph count: paragraphs.length vs reference.paragraphs.
2. Numbering: expected 1..found count in order; pass if nums[i]==i+1 for all.
3. First words: mismatches count = 0 → pass (if reference exists). Actually pass when mismatches===0? "First words match: n of m". Pass if all match.
4. Pages flagged: informational — "not a failure": show as neutral. I'll render it with a neutral style (no pass/fail); or pass always? Spec: "this line reads 'n pages flagged, n paragraphs to check'". Make it neutral.
5. Suspect lines: counts, informational.
6. Headers/footers: pages with symbol header (expected all), page-number footer (expected all but first), bare numbers removed listed.
7. Headings: counts labelled (parts incl. lettered) and unlabelled, list unlabelled.
8. Nothing lost: sum of classified == total non-empty lines; list unclassified.
9. Export round trip: JSON.parse(JSON.stringify(exportRecords)).length === table rows.

Also hyphen count line? "the app counts such lines anyway and reports the number" — add to checks or a note. Put in checks as informational: "Lines ending with a hyphen: n (none expected)".

Checks pass count: count pass among the pass/fail ones (1,2,3,6,8,9 → and maybe hyphen informational). Let me define each check with status 'pass'|'fail'|'note'. Header dot green "n of m checks pass" — m = number of pass/fail checks. Red when any failed.

Export JSON: as spec'd fields.
Export Markdown: front matter + headings + paragraphs. Ordered headings: walk sections list and paragraphs merged in order. I recorded ordered headings during walk; also need their position relative to paragraphs. I'll build a single ordered stream: during walk push either {type:'h',...} or paragraph. Actually paragraphs pushed via closeCur at next event; ordering: maintain stream array; when heading encountered push heading marker; when closeCur push paragraph. But closeCur happens when next heading/paraStart encountered — order still fine since headings pushed before closing? Let me push heading first, then closeCur pushes paragraph after — but paragraph belongs before the heading! E.g. para 5 lines, then heading, then para 6. Walk hits heading → I closeCur (push para 5) then push heading marker. So: on heading: closeCur first, then push heading. On paraStart: closeCur, then... paragraph not complete until next close. So push paragraph at closeCur time. Order: heading pushed after closing para5, before para6 closes. Correct sequence: para5, heading, para6. 

For Markdown: iterate stream; heading → "## text" or "### text"; paragraph → "**n** text (flagged...)".

Limitations field: flagged → "footnotes not separated; n may sit inside this paragraph" where n = count of suspect lines? "n may sit inside" — I'll use number of suspect lines in the paragraph. Else "footnotes not separated".

Now UI. Tabs with arrow keys. Tab02 table rows expandable; each expanded shows full text with suspect lines marked (thin red box — wrap suspect lines in span). But text is joined running text; highlight suspect lines inline: build HTML from lines: suspect lines wrapped in <mark class="sus">. Running text: lines joined with space; mark each line's text.

Also show reference six words beside found six (both normalized? show found raw-processed six words and reference six). Show PDF's lines toggle: original lines with line breaks + page markers ("— page N —" where page changed).

Copy citation button: copies "symbol, para. n", "Copied" 2s.

Headings found box (closed) above tab02 table: list all headings (ordered stream headings) with level.

Tiles tab01: 4 tiles + mismatch list (max 10 lines then "and n more") + downloads + two collapsibles (Every check, Flagged pages).

Flagged pages table: one row per flagged page: Page | Paragraph | Suspect lines | Why. Why: reasons list for that page's suspect lines ("starts with a number and a space", "bare number", "paragraph over 300 words"). Clicking row shows the page's raw lines with suspects highlighted and the paragraph they sit in. Raw lines of the page: I need original page lines. Store per page the classified lines with reason. Simpler: for each flagged page, list its body lines with suspect marking; the paragraph = paragraphs that have suspect lines on that page (numbers). For "raw lines with the suspect ones highlighted" — show the body lines (post header/footer removal) or full raw lines? "the page's raw lines" — I'll show the page's lines after header/footer removal (body lines), each marked; plus note paragraph number. Keep it simple: store per page array of {text, cls, suspect, inPara}.

Actually I can store for each page: its body line indices. During walk, line knows para num. Let me give each body line: cls, para (num or null), suspect. Then flagged page detail: list lines with cls labels and highlight suspects.

Why reasons: for a page, gather reasons from its suspect lines: bare number → "bare number"; /^\d/ + space → "starts with a number and a space"; /^\*/ → "asterisk note"; also if any paragraph spanning/flagged for 300 words on that page → "paragraph over 300 words".

Downloads: Blob, a.download with symbol.replace(/\//g,'-').

Disabled exports if 0 paragraphs.

Reference missing handling: if !D.reference → tiles "no reference in this file"; checks needing it "not run".

Fonts/colors per design. Focus ring. [hidden] rule.

Let me also handle `count` being string "20" — ignore, use records length.

Write the HTML now. I'll aim for compactness but complete.

Header right: green/red dot "n of m checks pass" or "n checks failed", then "n pages flagged".

Let me write it.

CSS: standard studio look.

Now careful with copy for clipboard fallback:

```
function copyText(t){ if(navigator.clipboard&&navigator.clipboard.writeText){return navigator.clipboard.writeText(t).catch(()=>fallback(t));} fallback(t);}
function fallback(t){const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(e){}ta.remove();}
```

Tabs: role tablist, buttons role=tab aria-selected, panels role=tabpanel, arrow keys left/right. Hidden panels: hidden attribute + CSS rule.

Filters: none (left rail is a doc card, not filters). Good — "Left rail, always visible. Headed DOCUMENT".

Collapsible headings: button aria-expanded toggling next div.

Table captions serif.

Now build checks data.

Counts: totalNonEmpty = sum over pages of non-empty lines. classified: headerCount, footerCount, coverCount, headingCount (incl. labels), paraCount(lines). Sum check.

Bare numbers removed from footer: list {page, value}.

Header warnings: pages whose first non-empty line != symbol.

Now write code. Paragraph object: {num, section, part, pageStart, pageEnd, lines:[{text,page,suspect}], text, textRawLines, flagged, fwFound, fwMatch, why:[]}.

First words computation:

```
function firstWords(text){
  const toks=text.split(/\s+/);
  const out=[];
  for(let k=0;k<toks.length&&out.length<6;k++){
    let t=toks[k];
    if(/^\d+$/.test(t)){
      const prev=out[out.length-1];
      const prevTok=prev!==undefined?prev:'';
      const prevRaw=k>0?toks[k-1]:''; // check raw previous token
      const ends=/[.,\u201D\u2019"']$/.test(prevRaw);
      const abbr=/^(no|art)\.$/i.test(prevRaw);
      if(k>0&&ends&&!abbr) continue; // drop
      out.push(t); continue;
    }
    t=t.replace(/\d+$/,''); // cut glued digits
    if(t) out.push(t);
  }
  return out.join(' ');
}
```
Hmm prev should be based on the raw previous token (before processing), e.g. "No." — but if "No." was processed (no digits to cut) it's same. Use raw prev token. Edge: paragraph starts with number? Then k=0, keep. Fine.

Normalize compare:
```
function norm(s){return s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();}
```

Suspect trigger:
```
function isSuspectLine(t){
  if(/^\d{1,3}$/.test(t)) return 'bare number';
  if(/^\d{1,3} [A-Z\u201C"]/.test(t)) return 'starts with a number and a space';
  if(/^\* /.test(t)) return 'asterisk note';
  return null;
}
```
Wait "starts with a number and a space and a capital letter, a UN document symbol or a quotation mark" — [A-Z“"] covers.

Footer drop conditions:
```
function isFooterLine(t,page){
  if(/^GE\./.test(t)) return 'job code';
  if(/^(\d{6})(\s+\d{6})*$/.test(t)) return 'date stamp';
  if(/^\d{1,3}$/.test(t)) return t===String(page)?'page number':'bare number';
  return null;
}
```
Loop from end: while i>=0 and (line blank or isFooterLine) drop. But careful: dropping from end could eat body content? Only blank/footer-pattern lines; body lines rarely match these patterns... a bare number line at foot is footnote number displaced — meant to be dropped. But "12 E/2003..." has number+space, not bare. OK.

Note: footer loop: start from last line; while lines remain and (blank or footer) pop. But once we hit a non-footer non-blank line, stop. Correct.

Header: first non-empty line === D.symbol → drop; else warn.

But wait — page 1 header is "E/C.12/GC/27" per sample — matches symbol. Good.

Cover: before first paraStart. But labelled heading I. comes after cover lines; classified heading. Cover lines classified in walk when cur==null and not heading/paraStart. But walk order: I handle label/heading before plain-line cover check. Yes.

Unlabelled heading test function:
```
function headingish(t){
  return t.length<=90 && /^[A-Z]/.test(t) && !/[.;:,\d]$/.test(t) && t.trim()!=='';
}
```
Two-line merge: "when the line before it passes the same test and does not end a paragraph sentence" — headingish already excludes . ; : , digit endings; "does not end a paragraph sentence" ≈ doesn't end with '.' — covered. So: if prev non-blank line (cls==null, i.e., not yet classified) passes headingish → mark it heading too, group text = prev + ' ' + line. But prev might have been consumed as paragraph text already if pass 3 runs after... I run pass 3 before pass 4 walk, so cls==null check works: prev line cls must be null (not heading, not... para lines get cls in pass 4). But wait: prev line being genuine paragraph text that happens to pass headingish (ends without punctuation) — rare; risk accepted, matches spec's rule.

Hmm, but the prev line could also be a paragraph start line? No — paraStart line followed by heading? No, heading is before paraStart. prev of the heading line: could be a paragraph-start line with text ("23. Text...")? That ends with... could pass headingish? It starts with digit not capital — fails. OK.

Pass 2 (labelled heading text): mark from label+1 forward while not label && not paraStart: mark non-blank as 'heading'. Stop also at EOF. But also should stop at blank-then-blank? Spec: "skip blank lines, then every line up to the next label line or paragraph start is heading text". So continue across blanks. But risk: if a label is followed by lots of body without paragraph... unlikely. Also should stop at unlabelled heading? spec doesn't say. Keep as spec.

Wait, one more issue: pass 2 heading text collection starting after "A." subsection labels — "A." then blank then title. Fine.

But letter label "[A-Z]\." could match... a paragraph line "A."? paragraphs are digits. Fine. Could match an unlabelled heading that is a single capital letter + period? Rare.

Potential problem: isLabel matches "I." but also lines like "D." etc. Fine.

Now, does heading text collection stop at blank-then-paragraph? It stops at paraStart line. Good.

One more: the walk for labelled headings — I need to know in the walk that a label line is a label: isLabel(body[i].text) and cls=='heading'. And subsequent heading lines until next non-heading. Let me in walk:
```
if(L.cls==='heading' && isLabel(L.text)){
  closeCur();
  const parts=[L.text];
  let j=i+1;
  while(j<body.length && body[j].cls==='heading'){ if(!body[j].blank) parts.push(body[j].text); j++; }
  const full=parts.join(' ');
  curPart=full; curSection=full;
  stream.push({type:'h',level:'part',text:full});
  i=j; continue;
}
```
Hmm parts join: "I." + "Introduction" → "I. Introduction" (join with space). Good.

Unlabelled heading (cls heading but not after a label... wait labelled heading TEXT lines also have cls 'heading' and aren't labels — but they're consumed by label branch. However the label branch loop `while cls==='heading'` might over-consume an unlabelled heading that follows the labelled heading text before a paraStart! E.g. "A." blank "Right to work" blank... no wait that scenario: "A." then text lines, then blank, then unlabelled heading, then paraStart. Pass 2 would have already marked the unlabelled heading as heading-text-of-label (pass 2 runs to paraStart, covering it). So it's inside the label's text anyway. Consistent.

So walk: any cls==='heading' line that's not consumed by a label branch is an unlabelled heading:
```
if(L.cls==='heading'){
  closeCur();
  curSection = unlabelledMap.get(i) || L.text;
  stream.push({type:'h',level:'section',text:curSection});
  i++; continue;
}
```
unlabelledMap: idx -> merged text (for two-line). For merged, both indices map to full text; the first index encountered in walk pushes the heading, then second index also cls heading pushes again — bug. For two-line heading, mark first line as heading and store group; second line... In walk, when I hit the first heading line of the group I should skip both. Simpler: in pass 3, when merging, only record group at the FIRST line index, and in walk, after pushing, skip forward past consecutive heading lines belonging to same group? Since the second line immediately... not necessarily adjacent (blanks between). Let me store groupEnd: map idx -> endIdx. In walk: j=i+1; while j<=end skip. Or: mark second line with cls 'heading2' meaning "part of previous heading". Then walk skips cls 'heading2' silently. 

Similarly labelled text lines: consumed by label branch. But what if a labelled text line appears in walk NOT after its label (impossible). OK.

Also: pass 3 prev-merge: prev line must be cls==null. But pass 2 already ran; if prev was labelled heading text it's cls 'heading' → skip merge. Good. Mark prev cls='heading2', current cls='heading', group text at current? Walk hits prev first (heading2, skip? but then heading never pushed!). Hmm. Order: prev comes before current in walk. If prev is 'heading2' skip it — then current 'heading' pushes group text (map at current idx = prevText+' '+curText). Good: 'heading2' lines skipped, group text stored on the 'heading' line. But for labelled headings, text lines are 'heading' and consumed by label branch — label branch consumes while cls==='heading' — but 'heading2' lines wouldn't be consumed! Are there heading2 lines inside labelled regions? heading2 only created in pass 3 for cls==null lines; pass 2 already marked labelled text as 'heading', so no overlap. But label branch while-loop stops at 'heading2'? Can't happen. Fine.

Wait, another subtlety: pass 3 marks current line 'heading' — but what if the current line is the LAST line before paraStart and prev is heading-text-of-label (cls 'heading')? Then no merge (prev cls!==null) and current becomes unlabelled heading — but pass 2 should have already marked it as heading text (pass 2 extends to paraStart). Contradiction: pass 2 marks everything from label to paraStart as heading. So current would already be 'heading' from pass 2, and it IS heading text of the label, not a separate unlabelled heading. Then walk's label branch consumes it. So unlabelled headings only exist when NOT preceded (since paraStart backwards) by a label-without-intervening-paraStart. I.e., unlabelled headings occur mid-document between paragraphs. Correct.

But then: how does pass 3 know a 'heading'-cls line is unlabelled vs labelled text? Labelled text lines get consumed by label branch in the walk; the label branch's while loop runs from label forward. But what if walk encounters a labelled-text line whose label was... always before it. Walk starts at 0; label branch consumes label+text together. So any 'heading' line reached in walk outside a label branch started earlier is unlabelled. Since label branch consumes contiguously, fine. Edge: two labelled headings adjacent: "A." text "B." text — label branch stops at next label (isLabel check)? My while loop consumes while cls==='heading', and the next label line also has cls 'heading' → would be swallowed! Fix: label branch consumes while cls==='heading' && !isLabel(text). Pass 2 also marks labels as 'heading' — check isLabel to break.

OK. Also letter subsection: part stays roman, section becomes "A. Title". Good: curSection=full, curPart unchanged.

Now paragraph closeCur:
```
function closeCur(){
 if(!cur) return;
 cur.text = cur.lines.map(l=>l.text).join(' ').replace(/  +/g,' ').trim();
 ... push
 cur=null;
}
```
Suspect computation after all paragraphs: iterate paragraphs in order, lines in order, taint per page.

Then flagged, fw, citation, etc.

Now checks and rendering. Let me now write the file.

Rendering tab02 rows: build table with tbody; each row: tr with td cells; row click toggles expansion — use a following detail row (hidden). Make the main row a button? Spec: "Rows are buttons with aria-expanded". I'll make the first cell contain a button spanning? Simpler: make the whole row clickable with tabindex=0 role=button aria-expanded, keydown Enter/Space. Acceptable. Or wrap row content... I'll use tr with tabindex, role, aria-expanded, and handle click/keydown. Style hover.

Expanded detail row: colspan=5, contains full text (marked), found vs reference words, "Show the PDF's lines" toggle button, copy citation button.

OK. Markdown export builder as spec.

Let me count clicks on tab01: tiles (none clickable), 2 download buttons, 2 collapsibles = 4. Tab02: headings box + rows. Fine.

Time to write. I'll be careful with escaping backticks etc. Use template literals in JS.

Also "How this is computed" line near every chart/number — add small line under tiles and rail numbers.

Let me write the whole thing now, mindful of length.

For flagged pages detail: per flagged page store lines: I'll store pageLines: for each page, array of {text, cls, para, suspect}. Build from body after all passes: each body line gets .cls final and .para (set during walk) and .suspect (during suspect pass, only paragraph lines). Body line objects shared — paragraphs reference same line objects. Good.

Reasons for flagged page: collect from suspect lines triggers + over-300 paragraphs starting/ending on that page? "paragraph over 300 words" as a why. Include if a flagged-for-length paragraph's pages include this page? Spec's why list includes it. I'll add reason when a >300-word paragraph has a suspect... actually a page is flagged only when it has a suspect line inside a paragraph. The over-300 flag is on paragraph only. But spec's "Why" column includes "paragraph over 300 words" — maybe a page could be flagged for that? "A page is flagged when it has a suspect line inside a paragraph". So why column: reasons of suspect lines; plus if any paragraph on the page is >300 words, add that reason. I'll include both.

Paragraph column: paragraphs with suspect lines on that page, joined ", ".

Suspect lines column: count on that page.

Detail expansion: show page's body lines, suspect highlighted, with cls tag and para number. I'll show all non-blank lines with class marks.

Now write. Also arrow-key tab navigation and hidden panel focusability: panels get hidden attribute.

Reference adopted shown in header. count field ignore.

Let me write the code.

Approx structure:

```html
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport"...><title>...</title>
<style>...</style></head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<main><aside rail><section panel01><section panel02></main>
<footer>...</footer>
<script>...</script>
</body></html>
```

Rail on left always visible — layout: grid with aside + content. Tabs above content. Header above all.

Let me write CSS quickly:
- body font sans 16, bg #f4f0e8, color #1d1b18.
- .mono label style.
- header: border-bottom.
- tabs: buttons, active red underline.
- layout: .wrap{max-width:1200px;margin:auto;padding} .cols{display:grid;grid-template-columns:260px 1fr;gap:32px}
- tiles: grid 2x2 (4 tiles). big serif numbers 44px.
- bar: div with inner width%.
- tables: full width, thin rules, th mono uppercase 11px, td padding, numbers right aligned.
- mark.sus / .susline {border:1px solid #9b2335; padding:0 2px}
- .pass{color:#1e6b3a}.fail / accent color #9b2335.
- button.focus-visible outline red.
- collapsible: button with aria-expanded, plus/minus.

JS ~400 lines. Let's write final.

One more detail: "n paragraphs of reference.paragraphs" with thin bar red when short or over.

Header right dot: span.dot green/red.

Exports: JSON records per spec. text_lines field: "the export field text_lines (lines separated by ' | ')".

Markdown front matter:
```
---
title: ...
symbol: ...
adopted: ...
source_url: ...
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: m
pages_flagged: k
footnotes: "not separated; the document has N"
---
```
Then headings ## part, ### section, paragraphs "**12** text (flagged: may contain footnote text)".

Only emit heading when encountered in stream order.

Now mismatch list under tiles: for paragraphs where fwMatch===false (and reference exists): "para. n: found X / reference Y". Max 10 + "and n more".

Copy citation uses symbol from data.

OK, write it. Also handle reference missing: ref = D.reference||null; refP = ref?ref.paragraphs:null etc.

Also "if no paragraph is found, tab 01 says so and the exports are disabled."

Check "Export round trip": JSON.parse(JSON.stringify(records)).length === paragraphs.length.

Let me write final HTML. I'll keep it organized.

For paragraphs tab, table caption: "n paragraphs found, m expected".

Sort rows by num (document order already).

Also "Headings found: n" box: list ordered headings with level marker (part/section).

Arrow keys on tablist.

Write now.