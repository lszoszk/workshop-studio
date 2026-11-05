Build the full app in one HTML file. Follow the plan carefully. Let me write it.

Key pipeline: header removal, footer removal, concatenate body lines, find paragraph starts, headings, build paragraphs, suspect lines, first words, checks, exports.

Let me write the code carefully but concisely.

Plan structure:
- header, rail, tabs 01/02, footer.
- Pipeline computed once.

Let me draft the extraction algorithm per spec:

```js
const D = WORKSHOP_DATA.pdf_text;
const pages = [...D.records].sort((a,b)=>a.page-b.page);
```

Header: first non-empty line == symbol → drop; else warning.

Footer: from end, drop lines while empty, startsWith("GE."), /^\d{6}( \d{6})*$/ (date stamp), or bare number 1-3 digits. Track page number vs other bare numbers.

Body lines: {page, text, index}.

Cover: lines before first paragraph start.

Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.

Headings: labelled: /^([IVX]+|[A-Z])\.$/ — then following lines until next label or paragraph start form heading text. Unlabelled: non-empty line immediately followed by paragraph-start line, ≤90 chars, starts with capital, not ending . ; : , digit. Two-line heading: when line before passes same test and "does not end a paragraph sentence" — treat as heading continuation (combine). Simplest: when checking unlabelled heading candidates, if the previous body line also passes the test and doesn't end with sentence-ending punctuation (., ., ;, :? plan says "does not end a paragraph sentence" — I'll interpret: doesn't end with . ! ? " ' etc. — actually if it passed "not ending with full stop" it can't end a sentence... hmm. The test "not ending with a full stop, semicolon, colon, comma or digit" already excludes most sentence endings. "does not end a paragraph sentence" — maybe the previous line could end with "?" or "."? It can't end with "." per test. I'll check prev line passes the same char test; if so, both lines are heading. That covers the para-73 case.

Approach: first classify paragraph starts. Then scan body lines sequentially, classifying:
- if line is paragraph start: current paragraph = number; heading context unchanged.
- if line is labelled heading marker: collect heading text lines (skip blanks; lines until next label line or paragraph start or... careful: unlabelled heading detection "immediately followed by paragraph-start line"). Also continuation lines starting with lowercase or "(" continue heading.
- unlabelled heading: a body line (non-empty) immediately followed (among non-empty lines? "immediately followed" — in concatenated body lines; I'll check next non-empty line... blank lines were dropped? Body lines include blanks? "Blank lines are dropped" for paragraphs. Plan says concatenate body lines "footnote lines included". For "immediately followed" I'll use next non-empty line.

Careful ordering: heading collection loop must terminate correctly. Let me do a single pass with index i over bodyLines:

```
state: currentParagraph=null, sectionHeading=null, partHeading=null
for i in lines:
  if isParaStart(line):
     close prev paragraph; start new para; record preceding heading candidate
  else if isLabelled(line):
     close prev para? No — labelled heading ends... headings come between paragraphs. Start collecting heading: skip blanks, take lines until next labelled or paraStart; lowercase/"(" starts continue heading. Set section=part or section.
```

Unlabelled heading detection: before starting a paragraph at line i (para start), check line before (previous non-empty, non-blank line in body) — if it passes the unlabelled test and isn't already classified as heading text, it's a heading. Two-line: check the one before that too.

But labelled heading collection may have already consumed those lines. When I detect a labelled heading, I collect its text; collection stops at paragraph start. But the unlabelled heading line sits before the paragraph start too and might be consumed by the labelled heading collection (which takes "every line up to the next label line or paragraph start"). Hmm — a labelled heading's text is followed possibly by an unlabelled heading? E.g. "IV." then "Right to work (art. 6)"? Per data, unlabelled headings like "Right to work (art. 6)" are standalone. To be safe: when collecting labelled heading text, if a line is immediately followed by a paragraph start and passes the unlabelled test... it would be part of labelled heading text then. But plan says collection goes up to paragraph start. Keep simple: labelled heading consumes everything to next para start/label; then unlabelled check only applies if the previous non-empty line is not already part of a heading. Actually simpler: track classification per line. Line kinds: cover, header, footer, heading, paragraph, suspect (still paragraph).

Implementation: iterate i over body lines with classification array. Then paragraphs built from consecutive paragraph-classified lines.

Algorithm:
1. Build bodyLines (after header/footer removal), keep blanks for detection? Blanks: drop empty lines from bodyLines? "Body lines of all pages are concatenated (every line that is not header or footer)". "Immediately followed by a paragraph-start line" — I'll drop blank lines when concatenating, so "immediately" = adjacency in the non-empty sequence. That matches "a blank line, then the text" footnote structure? Footnote first is bare number, blank, text — but those are inside paragraphs anyway. Fine, drop blanks.

2. Pass A: mark paraStart lines and their numbers.
3. Pass B: mark labelled heading marker lines and collect heading text.
4. Pass C: unlabelled headings: for each paraStart at index i, if lines[i-1] exists, unclassified, passes test → heading; if lines[i-2] also passes and unclassified → heading too (two-line). Wait plan says: "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading." I'll check i-1 then i-2.
5. Lines before first paraStart and not heading = cover.
6. Remaining classified = paragraph lines; group by current paragraph.

For labelled heading text collection: lines after marker until next marker or paraStart. But if among those lines the last one is followed by a paraStart and passes unlabelled test — it becomes part of labelled heading text (per plan "every line up to the next label line or paragraph start is heading text"). OK.

Also continuation "line starting with lowercase letter or "(" continues the previous heading line" — that's within labelled collection; just append all collected lines.

Section assignment: track last heading (labelled or unlabelled) and last roman labelled heading.

Suspect lines: inside paragraphs:
- bare number 1-3 digits no full stop: /^\d{1,3}$/
- starts with 1-3 digits, space, capital letter or UN symbol or quote: /^\d{1,3} [A-Z"“]/
- starts with "* "
Suspect propagates: line and all later lines on same page are suspect. Also para >300 words flagged.

Page flagged: has suspect line inside a paragraph.

First words: text split, strip footnote marks:
- digits glued to end of word/punctuation: replace /\d+$/ on token if preceded by punctuation or word... plan: 'digits glued to the end of a word or a punctuation mark are cut ("waste.2" becomes "waste.")'. So token like "waste.2" → cut trailing digits? But "waste2"? cut digits at end when token ends with digits and before that is a non-digit. Apply: token.replace(/\d+$/, "") only if the char before digits is not a digit and... but a real word could end with digit rarely; fine per plan.
- token of digits alone dropped only when previous token ends with . , or closing quote and not abbreviation like "No." "art.".

Compare with first_words[str(num)] normalising quotes/dashes/whitespace.

Checks list per plan: paragraph count, numbering 1..n, first words, pages flagged (informational), suspect lines, headers/footers, headings count + unlabelled list, nothing lost, export round trip.

Pass count: which checks pass? Paragraph count (found==reference), numbering (exactly 1..n), first words (all match), headers (all pages), footers page numbers (all but first), nothing lost (sum matches), export round trip. Pages flagged, suspect lines, headings are informational — plan says "a flag is not a failure". I'll make m = total checks listed; pass count counts pass/check-failed ones; informational ones read neutrally. Header dot: green "n of m checks pass" or red "n checks failed". I'll define checks: 7 boolean (count, numbering, first words, headers, footer page numbers, nothing lost, round trip) plus 3 informational (flagged pages, suspect lines, headings). Show m as number of boolean checks... "n of m checks pass" — let m = 7 boolean checks. But "Every check (m)" panel should list all 10. I'll use m = total lines shown, and pass count = boolean passes. Simpler: pass/fail checks count 7; panel shows all with informational ones marked "info". Header: "7 of 7 checks pass". I'll just show passCount of checkTotal where checkTotal = pass/fail checks count.

Exports: JSON array with fields; Markdown with front matter. Blob URLs.

Tab 02: table rows expandable, copy citation button, "Show the PDF's lines" toggle showing text_lines with page markers.

Flagged pages panel (tab 01): rows Page|Paragraph|Suspect lines|Why; click row → shows page's raw lines with suspect highlighted and paragraph. Note the raw lines of the page need original page lines — keep original per-page lines. Suspect lines in raw page: recompute classification per line of the original page? Easier: when rendering a flagged page's raw lines, mark lines that match suspect patterns or come after one on that page within a paragraph. I'll store for each page its raw lines, and mark: a line is suspect-display if it's a paragraph line flagged suspect in pipeline. I can store suspect flag on body line objects; for raw display, map raw lines to classified body line? Duplicates possible. Simpler: recompute per raw page line: if line matches suspect start pattern, mark it and all subsequent non-footer lines on that page. Good enough for display.

Why column reasons: "starts with a number and a space", "bare number", "paragraph over 300 words".

Line counts: nothing-lost check: total non-empty lines in file = cover+header+heading+paragraph+footer(+unclassified). Note blank lines excluded. Header count = number of dropped header lines (1 per page typically). Footer lines count including blank? Non-empty only. So compare non-empty lines total vs sum of non-empty classified. Footer dropping includes blank lines from the end — those aren't counted. Header dropped lines are non-empty. OK: total non-empty = header + footer(nonempty dropped) + body non-empty; body non-empty = cover + heading + paragraph(+unclassified). Blank lines dropped in footer strip and within body don't count.

Hyphen-ending lines count: count body lines ending with "-" (expect 0, report).

Now write the HTML. Keep it under ~1500 lines. Aim ~700-800 lines.

Design: CSS per studio spec. Tabs with arrow-key nav. [hidden] rule.

Let me write it.

Data structure para:
{n, section, part, page_start, page_end, text, text_lines:[{text,page,suspect}], flagged, first_words_match, citation, limitations, why:[reasons], suspectLines:[...]}

Numbering check: numbers sequence 1..found; gaps/dupes listed.

Copy citation: navigator.clipboard, fallback textarea. Show "Copied" 2s.

Export filenames: symbol.replace(/\//g,'-').

Markdown: front matter then headings in document order as ## (roman parts) and ### (sections) and paragraphs. Need ordered heading list: collect headings with type (roman/lettered/other) in order. For markdown: roman → ##, others → ###? Plan: "the headings as ## and ### lines in document order". I'll do: roman-labelled → ##, others → ###. And paragraphs as "**n.** text".

Section in JSON: nearest heading; part: nearest roman.

Now build headings list during pass: each heading {text, kind:'roman'|'lettered'|'unlabelled', index}. Roman: /^[IVX]+\.$/ marker.

Unlabelled headings list for check panel.

Also headings count box on tab 02, closed.

Edge: if no paragraphs found → tab 01 message, exports disabled.

Let me now write the whole file.

Line classification storage: bodyLines array of {text, page, cls: null|'cover'|'heading'|'para', para: null|idx, suspect:bool, headingRef}.

Algorithm code:

```js
const SYM = D.symbol;
const pages = D.records.slice().sort((a,b)=>a.page-b.page).filter(r=>r && typeof r.text==='string');
const stats = {headerDropped:0, headerWarn:[], footerBareNums:[], pagesWithPageNum:[], footLines:0};
const bodyLines=[]; const rawPages=[]; totalNonEmpty=0;
for (const pg of pages){
  const lines = pg.text.split('\n').map(l=>l.trim());  // trim? converter lines maybe have trailing spaces. trim right at least.
  rawPages.push({page:pg.page, lines});
  let start=0;
  // find first non-empty
  let first = lines.findIndex(l=>l!=='');
  // header: first non-empty equals symbol
  let hdrRemoved=0;
  if(first>=0 && lines[first]===SYM){ lines[first]=''; hdrRemoved=1; start=first+1; }
  else stats.headerWarn.push(pg.page);
  // footer strip from end
  const isFoot = l => l==='' || l.startsWith('GE.') || /^\d{6}( \d{6})*$/.test(l) || /^\d{1,3}$/.test(l);
  let end=lines.length;
  while(end>start && isFoot(lines[end-1])){
    const l=lines[end-1];
    if(l!==''){
      stats.footLines++;
      if(/^\d{1,3}$/.test(l)){
        if(String(pg.page)===l) stats.pagesWithPageNum.push(pg.page);
        else stats.footerBareNums.push({page:pg.page, num:l});
      }
    }
    end--;
  }
  for(let i=start;i<end;i++){
    if(lines[i]!=='') totalNonEmpty++;
    bodyLines.push({text:lines[i], page:pg.page, rawIndex:i});
  }
  // count nonempty for whole page for totals:
  // totalNonEmpty should count ALL non-empty lines in file including header/footer.
}
```

Wait, totalNonEmpty: count all non-empty across the raw page before removal. Adjust: count from rawPages at end: rawPages flat non-empty count. And classification counts: headerDropped per page (non-empty), footLines non-empty, cover+heading+para non-empty body lines. Blank body lines not counted. Good.

Header count: if hdrRemoved, that's one non-empty line. Use stats.headerDropped count.

isParaStart: 
```js
const mAlone = l => /^(\d{1,3})\.$/.exec(l);
const mWith = l => /^(\d{1,3})\. (.+)$/.exec(l);
```

Pass: iterate bodyLines skipping blanks. Build a list of nonempty indices for adjacency.

Let me structure:

```js
const NE = []; // indices of non-empty body lines
bodyLines.forEach((b,i)=>{ if(b.text!=='') NE.push(i); });
const isPS = i => mAlone(bodyLines[i].text) || mWith(bodyLines[i].text);
```

Labelled heading markers: /^([IVX]+|[A-Z])\.$/. Note single capital + "." could conflict with paragraph start? Paragraph starts are digits. Fine. But "A." marker vs... ok.

Now classify:

```js
const headings=[]; let curSection=null, curPart=null;
let k=0; // over NE
for(let a=0;a<NE.length;a++){
  const i=NE[a], t=bodyLines[i].text;
  if(bodyLines[i].cls) continue; // already heading text from labelled collection
  if(isPS(i)){ markParaStart }
  else if(/^([IVX]+|[A-Z])\.$/.test(t)){
    // collect heading
    const roman=/^[IVX]+\.$/.test(t);
    const parts=[];
    let b=a+1;
    while(b<NE.length){
      const j=NE[b], u=bodyLines[j].text;
      if(/^([IVX]+|[A-Z])\.$/.test(u) || isPS(j)) break;
      parts.push(u); bodyLines[j].cls='heading'; b++;
    }
    const h={text:parts.join(' '), roman, afterNE:a};
    headings.push(h);
    if(roman){curPart=h;curSection=h;} else curSection=h;
    bodyLines[i].cls='heading';
    continue;
  }
  // else: candidate unlabelled heading handled when we hit para start; leave unclassified for now
}
```

Hmm, unlabelled detection: when at a para start at NE index a, check NE[a-1]: if unclassified and passes test → heading; then NE[a-2] similarly. Test:

```js
const unlTest = t => t.length<=90 && /^[A-Z(]/.test(t) && !/[.;:,\d]$/.test(t) && !/^([IVX]+|[A-Z])\.$/.test(t) && !isPSline(t);
```

Plan: "starting with a capital letter" — allow "(" too? "Right to work (art. 6)" starts with capital. I'll allow capital or "(capital". Keep /^[A-Z(“"]/. Hmm keep simple: /^[A-Z(]/.

Two-line: "when the line before it passes the same test and does not end a paragraph sentence" — the line before the first heading line; since test excludes . ; : , digit endings, "does not end a paragraph sentence" mostly means it isn't mid-paragraph... ambiguous. If NE[a-2] passes the test AND is unclassified, treat as part of heading. Risk: a short line mid-paragraph? Body lines within a paragraph are long prose; a line that passes (≤90 chars, capital start, no sentence-end punctuation) mid-paragraph is possible but rare. Accept.

So in main loop, when isPS(i):
```js
if(a>0){ const p=NE[a-1];
  if(!bodyLines[p].cls && unlTest(bodyLines[p].text)){
    bodyLines[p].cls='heading'; const h={text:bodyLines[p].text, roman:false};
    if(a-1>0){ const q=NE[a-2]; if(!bodyLines[q].cls && unlTest(bodyLines[q].text)){ bodyLines[q].cls='heading'; h={text:bodyLines[q].text+' '+bodyLines[p].text, roman:false}; headings.push order... } }
    headings ordering: must be in document order. Since we push during forward scan, unlabelled heading at NE[a-1] is pushed when we reach para start at a — but a labelled heading earlier already pushed. Order fine except heading at NE[a-1] pushed before... all good since scan is forward. But if NE[a-2] case: push combined after. OK.
    curSection=h;
  }
}
```

Careful: the labelled collection loop sets cls='heading' for its text lines; those are skipped in main loop.

Cover: body lines before the first paragraph start that are unclassified and occur before first PS index → 'cover'. Simplest: after full classification, any non-empty line before firstPSIndex (index in NE of first para start) unclassified → cover. Lines after firstPS unclassified → paragraph text? No: main loop — lines that aren't para starts and aren't headings: they belong to current paragraph. If no current paragraph (before first PS) → cover.

Let me restructure main loop to handle paragraph accumulation:

```js
let paras=[]; let cur=null; let firstPSseen=false;
for(let a=0;a<NE.length;a++){
  const i=NE[a], t=bodyLines[i].text;
  if(bodyLines[i].cls){ continue; } // heading text already assigned
  if(isPS(i)){
    // unlabelled heading check on NE[a-1], NE[a-2] (must not be cls'd and must be after... also must be unclassified)
    handleUnlabelled(a);
    const m = mWith(t);
    if(cur) paras.push(cur);
    cur = {n:+(m? m[1]: t.replace('.','')), lines:[], ...};
    bodyLines[i].cls='para'; bodyLines[i].para=cur;
    if(m){ pushLine(m[2]) }
    firstPSseen=true;
  } else if(!firstPSseen){
    bodyLines[i].cls='cover';
  } else if(cur){
    bodyLines[i].cls='para'; bodyLines[i].para=cur; pushLine(t);
  } else {
    bodyLines[i].cls='cover'; // between? shouldn't happen
  }
}
```

But wait: labelled heading marker lines: I check them before para start in loop. But the labelled-collection inner loop consumes NE indices via while from a+1; those get cls='heading' and the outer loop's `continue` on cls'd lines skips them. Good. But handleUnlabelled when labelled heading text was just collected: NE[a-1] would already be cls='heading' so skipped. Good — though that means an unlabelled heading directly after a labelled heading line gets absorbed into the labelled heading's text. Acceptable per plan.

Paragraph object: {n, section (curSection at start? assign at push/close — section can't change mid-paragraph since headings only appear between paragraphs... actually heading appears after para lines; assign section at paragraph creation time, but the unlabelled heading for THIS paragraph is detected right before creation. Order: handleUnlabelled sets curSection, then create para with section=curSection. Good. But headings pushed by the labelled branch set curSection when encountered — before next para start. Good.)

Then finalize: assign para.section, part=curPartAtStart.

Text: lines joined ' ', collapse double spaces, trim. text_lines with page. suspect marking:

```js
for each para, iterate lines; if !suspectActive and line matches suspect patterns → mark, suspectActive=true; if suspectActive → mark. Reset suspectActive at page change? Plan: "A suspect line and every line after it to the end of its page are suspect". So active within page: when page changes, reset active=false. 
```

Also "* " start pattern.

Para flagged if any suspect line OR word count >300.

Pages flagged: set of pages having a suspect line inside a paragraph. Why reasons per flagged page rows: collect {page, para, suspectLines:texts, reasons}.

First words: implement per plan:

```js
function firstWords(text){
  let toks=text.split(/\s+/);
  const out=[];
  for(let k=0;k<toks.length && out.length<6;k++){
    let w=toks[k];
    // cut glued digits
    w = w.replace(/(?<=[^\s\d])\d+$/,'');  // lookbehind ok in modern browsers
    if(/^\d+$/.test(w)){
      const prev=out[out.length-1];
      if(prev && /[.,’”"]$/.test(prev) && !/(No|art|para|paras|chap|sect|vol|p)\.$/.test(prev)) continue;
    }
    out.push(w);
  }
  return out.join(' ');
}
```

Hmm lookbehind support — modern Chrome fine. Alternatively: w.replace(/\d+$/, m => /\d/.test(w.slice(0,w.length-m.length)) ? m : ...). Use: if(/\D/.test(w) && /\d+$/.test(w)) cut. Actually "waste.2": before digits is '.', non-digit → cut. "Goals17"? cut. Just: w = w.replace(/\D(\d+)$/, (mm)=>mm[0]) — replace "X<digits>" end with "X". i.e. w.replace(/([^\s\d])\d+$/, '$1').

Normalise compare: replace curly quotes, dashes, whitespace.

reference.first_words values are "first six words" strings — compare normalised equality.

Checks:

1. Paragraph count: found vs reference.paragraphs. pass if equal.
2. Numbering: numbers are exactly 1..n in order. List gaps/dupes.
3. First words: count mismatches; pass if 0 (and reference exists).
4. Pages flagged: informational: "n pages flagged, n paragraphs to check".
5. Suspect lines: n suspect lines on n pages, in n paragraphs; none removed. informational.
6. Headers/footers: pages with header (expected all) — pass if all; pages with page number in footer (expected all but first) — pass if pagesWithPageNum.length === pages.length-1 (roughly; if page 1 has no number). Bare numbers listed.
7. Headings: labelled count, unlabelled count + list. informational.
8. Nothing lost: sum equals total non-empty. pass if equal and unclassified list empty.
9. Export round trip: JSON.parse(JSON.stringify(records)).length === paras.length. pass.

Pass/fail checks: count, numbering, firstwords, headers, footer page numbers, nothing lost, round trip = 7.

Check panel lines: description + values + pass/fail.

Reference missing handling: "no reference in this file", checks "not run".

Now the exports:

JSON record fields: symbol, paragraph, section, part, page_start, page_end, text, text_lines, flagged, first_words_match, citation, doc_url, limitations.

Markdown: front matter, then iterate headings in order with their paragraphs. Build an ordered structure: I'll store paras with headingBefore reference; simpler: build sequence: iterate headings (each with a NE index), and paragraphs (each with start NE index), merge by order. For markdown: roman heading → '## ', else '### '. Then paragraphs: '**n.** text' + flagged note.

Round trip check on the JSON string built.

Downloads: Blob URL, filename SYM.replace(/\//g,'-') + '.json'/'.md'.

Tab 01 layout: 4 tiles; mismatch list; export buttons; two collapsible: Every check (m), Flagged pages (n). Flagged pages table: rows clickable → expand raw page lines with suspect highlighted and the paragraph they sit in.

Raw page lines rendering: for flagged page p, iterate rawPages[p].lines; determine header (first non-empty if ===SYM), footer region (from end per isFoot), and body lines with suspect marking: a raw body line is suspect if it matches suspect start pattern, or comes after one on that page before footer. Simpler recompute. Mark with red box.

Tab 02: headings box (closed), table rows expandable. Expanded: full text with suspect lines marked (wrap suspect lines in span with red box — but text is joined... I'll render text with suspect lines boxed: since text = lines joined by space, I can render as HTML: escape each line, wrap suspect ones). Show reference six words vs found six. "Show the PDF's lines" toggle: list text_lines with page markers. Copy citation button.

Suspect text marking: para.lines each {text,page,suspect}; render joined with ' ', suspect lines in <span class="sus">.

Now write. Keep the code tidy. Also handle empty pages / missing text.

Also footer strip: isFoot includes blank lines, but must not strip everything; the while loop stops when a non-foot line found. Note risk: a body line that is a bare number (footnote number displaced mid-page? no, those are in footer per spec). Fine.

Edge: page 1 footer has "GE.25-15926 (E)" — startsWith("GE.") ✓. Date stamp "051125 061125" matches /^\d{6}( \d{6})*$/ ✓.

Header warning when first non-empty line != symbol.

Trim lines: use trim() — but footnote pattern "digits glued" unaffected. OK.

Tab keyboard nav: standard roving. Rows as <button> with aria-expanded inside <tr>? Buttons in table rows: plan says rows are buttons with aria-expanded. I'll make the first cell a button? "Rows are buttons with aria-expanded; click or Enter expands". I'll make each row a <tr> with tabindex=0 role=button aria-expanded, keydown Enter/Space. Acceptable.

Hidden panels: use hidden attribute + CSS rule.

Let me count clicks on tab 01: export 2 buttons + 2 collapsibles = 4. OK.

Write CSS: paper #f4f0e8, ink #1d1b18, rule #d9d2c3, accent #9b2335, green #1a6b3c (dark green for pass).

Big numbers 40-56px serif.

Now produce the file. Aim compact.

Also "n pages flagged" in header. Header right: dot + "n of m checks pass" or red "n checks failed"; then "n pages flagged".

Footer: source, built, and the line. D has `built`? pdf_text description: {title, symbol, doc_url, source, count, records, reference}. built may not exist — show if present, else skip. Use D.built || ''.

Write it now.

For the "First line" column: first 120 chars cut at word with "…".

Citation copy: clipboard API with fallback.

Check panel "link to the rows concerned" — for failed checks, link to tab 02? Keep simple: failed checks mention paragraph numbers; I'll not add deep links (or link switches to tab 02). I'll add a simple link that activates tab 02 for first-words failures. Minor; include small link "→ tab 02".

Let me write final code.

One more: "How this is computed" line near every chart/number — tiles each have one.

Numbering check details: expected 1..found.length sequence; check paras[i].n === i+1. Gaps/dupes list by number and page.

Nothing lost: totalNonEmpty (all non-empty raw lines) vs headerCount + footerNonEmpty + coverNonEmpty + headingNonEmpty + paraNonEmpty. Blank lines excluded everywhere. Header lines count: for pages where header dropped, 1 each (non-empty). Also unclassified lines list (shouldn't be any by construction — every non-empty body line gets cover/heading/para... in my loop, unclassified only if cur===null after firstPS seen? No, firstPSseen true implies cur set unless... para start always sets cur. So all non-empty lines classified. Fine, check still computes.)

Compute headingNonEmpty: bodyLines.filter(cls==='heading').length. cover similarly. para count: cls==='para'. Note para-start lines are cls='para'.

Also count lines ending with '-' (hyphen report).

Let me write.

For markdown export ordering, build items list:
```js
const items=[]; // {ord, type, ...}
```
Track order via NE index. Para has startIndex (NE index of its start). Headings have NE index (marker or unlabelled line... unlabelled line index; two-line heading use first line's index). For labelled, marker index. Then sort merged by index.

For JSON `section`: heading text; `part`: roman heading text.

Write the code now, final.

Estimated length ~850 lines. Go.