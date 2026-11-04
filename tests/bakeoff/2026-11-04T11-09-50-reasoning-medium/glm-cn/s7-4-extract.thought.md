Build the full app per plan. Single HTML file, four tabs, rail with document cards, pipeline, checks, CSV download. Keep under ~1500 lines. Let me write carefully but compactly.

Key pipeline details: header removal, footer removal, concatenate body lines, paragraph starts, headings (labelled and unlabelled), paragraphs, suspect lines, first words, checks, repairs log, raw page viewer, CSV.

I'll structure:

- CSS
- Header
- Rail + tabs
- Tab panels rendered by JS.

Let me code the pipeline.

Steps:

```js
const docs = Object.keys(WORKSHOP_DATA).filter(k => WORKSHOP_DATA[k] && WORKSHOP_DATA[k].records && WORKSHOP_DATA[k].reference).map(k=>({key:k, d:WORKSHOP_DATA[k]}));
```
Selected doc state.

Pipeline per doc:
```
function runPipeline(d){
  const symbol=d.symbol;
  const repairs=[];
  const pages = [...d.records].sort((a,b)=>a.page-b.page);
  const lineInfo = []; // per page: array of {text, kind}
  // classify header/footer per page
  for each page:
    lines = text.split(/\r?\n/) — raw text; keep as lines. Actually text has "\n\n". split('\n').
    first non-empty line === symbol -> header, log repair per page (maybe log once each page: "header line removed" per page — log each).
    From end: drop while empty / GE. / /^\d{6}( \d{6})*$/ / bare number 1-3 digits. bare number equal to page -> footer (page number). other bare number -> log "bare number removed from the footer".
    Everything else body.
```

Note: pages might be few with numbers in foot. Careful: the date stamp "051125 061125" matches 6-digit groups. Bare number page 1: no page number. Note: bare number equal to page — footer page number.

Also careful: footer removal from end must stop when a line doesn't match footer patterns — but footers can be interleaved? Plan says "in varying order" and drop lines while matching, from end, skipping empties. But "drop lines while the line is empty, ..." — dropping empty lines from the end is fine since blank lines dropped anyway. But careful: once we hit a non-footer line, stop — but what if footer lines are interleaved like page number then GE code then nothing? Both match patterns so fine. What about a footnote block at foot before footer — those are body (suspect). Fine.

Concatenate body lines with page tags.

Then heading/paragraph parse over body lines:
- labelled heading: /^([IVX]+|[A-Z])\.$/ — roman or single capital letter followed by period. Then skip blanks, collect heading text lines until next label line or paragraph start. A line starting with lowercase or "(" continues previous heading line (join, log "heading title joined from two lines"). Any other non-empty line is further heading text? Plan: "any other line is a further heading". Hmm, that could swallow paragraph text if a heading label is followed by text. Acceptable per plan.

Wait, but careful: heading collection runs until "next label line or paragraph start". Lines like blank skipped.

- unlabelled heading: non-empty line immediately followed by paragraph-start line, ≤90 chars, starts with capital, not ending with . ; : , or digit. Log "heading separated from paragraph text".

- paragraph start: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/ (log "number and text split").

Order of classification per line: I'll do a single pass:

```
let section=null, part=null, sectionPath=[];
let currentPara=null;
state: i over bodyLines.
if line matches labelled heading label: close current para? Actually headings appear between paragraphs; close current para (it stays with its lines). Set mode 'heading', part if roman, sectionTitle collecting.
```

Hmm but paragraphs end when next heading/paragraph start comes. Since paragraph text lines are just accumulated until a new start/heading.

Implementation: iterate; classify each line:

```
isLabel = /^([IVX]+|[A-Z])\.$/.test(l)
isParaStart = /^(\d{1,3})\.$/.test(l) || /^(\d{1,3})\. (.+)$/.test(l)
```

Cover: lines before first paragraph start AND before first heading? Plan: "Lines before the first paragraph start are the cover." Hmm — but page 1 has "I." heading before para 1? Actually cover includes title lines then "I." "Introduction". Plan says lines before the first paragraph start are cover — that would make "I." and "Introduction" cover. But heading rule also applies. Hmm. The "Nothing lost" check classifies every line as cover, header, heading, paragraph or footer. I think simpler: before the first paragraph start, everything is cover except labelled headings... risky. Let me just treat: cover = lines before the first paragraph start; but labelled heading detection starts... Actually GC27 sample: page 1 has symbol, header stuff, title, "I." "Introduction", then "1." So if cover is "lines before first paragraph start", then "I." "Introduction" are cover. But then part for para 1 would be... The plan says each paragraph's part is most recent roman heading. Simplest: process headings normally from start; cover = non-empty lines before first paragraph start that are not consumed as headings. I'll run the heading logic across the whole document; lines before first paragraph start that are not headings/labels are cover. That satisfies "Nothing lost" (cover|header|heading|paragraph|footer covers all).

Parse loop:

```
let i=0; paras=[]; headings=[]; repairs per rules; coverLines=[];
let curHeading = null; // collecting lines of labelled heading
while i < L:
  l = lines[i].text (trimmed? raw line trimmed of trailing? I'll trim each line — PDF text may have no leading spaces. Trim both ends.)
  if label line: flush current para? No — headings come after paragraph ends... paragraph doesn't "end" explicitly; it ends when a new paragraph start or heading appears. So when label appears, current para is complete (push happens when? I'll keep curPara object and finalize when a new para starts or heading appears or end).
    curHeading = {label, lines:[], page}
    flushPara()
  else if in heading mode: collect heading lines until label or para start. Lowercase/(-starting line joins to previous heading line (log "heading title joined from two lines"). Blank skip. Else if para start -> exit heading mode and handle. Else if line starts... any other non-empty line is a further heading line? Hmm "any other line is a further heading" — meaning a second line of heading text (multi-line titles that start with capital). OK, add to heading lines.
```

Wait risk: heading mode continues until next label or paragraph start — but unlabelled headings? e.g., "I." heading, then "Introduction", then blank, then "1." para start. Fine.

But what about after heading text, other content before para start? Acceptable.

Unlabelled heading detection: line at i, non-empty, next non-empty? plan: "immediately followed by a paragraph-start line". Check lines[i+1] is paragraph start (maybe skip blanks? "immediately followed" — I'll check next non-empty line? plan says immediately followed. I'll check the next line exactly, but if blank between... In PDF, heading then blank then "12." Hmm. Safer: next non-empty line. I'll do next non-empty.)

Where to check unlabelled heading: in main loop, before treating a line as paragraph text: if next non-empty line is a para start and line qualifies (≤90, starts capital, not ending . ; : , digit) and we're not in heading mode and line isn't a label → it's a heading: section = that line, log "heading separated from paragraph text". Also it should be after the first paragraph start? An unlabelled heading before para 1... cover lines. I'll only apply when we've had at least one paragraph start OR we're past cover? Actually headings can be in cover region too. Keep simple: apply anywhere; if before first paragraph, it's still a heading.

Sections: track `section` = current heading title (joined label + text? plan shows "Right to work (art. 6)" — the heading text). For labelled headings, title = text lines joined with " " (e.g., "Introduction" or "Right to work"? no, "Right to work (art. 6)" is unlabelled). Keep `section` = heading display title; for labelled, maybe "I. Introduction"? Plan: Section column shows "Right to work (art. 6)"; expanded shows full path "IV. … › Right to work (art. 6)". So part = roman heading title ("IV. …" meaning roman heading text), section = nearest heading (could be lettered or unlabelled). Full path = part + " › " + section when both.

I'll store for each heading: {label, text, type: 'roman'|'letter'|'unlabelled'}. sectionTitle = text (or label+". "+text for display of part). partDisplay = label + ". " + text for roman.

Paragraph object: {number, page_start, page_end, lines:[{text,page}], text (joined), flagged, suspectLines:[], section, part, sectionPath, firstWordsFound, firstWordsRef, match, repairs:[...]}

Suspect detection: after building paragraphs, for each paragraph, scan its lines: line is suspect if:
- bare number 1-3 digits no full stop: /^\d{1,3}$/
- starts with 1-3 digits, space, then capital letter or UN symbol or quote: /^\d{1,3} [A-Z("]/
Then that line and every subsequent line to the end of its page (within the paragraph) are suspect. Record suspect lines with page and line number? Line number — within page raw lines. I need to track original line index per page. I'll keep for each body line its original index in the page's line array.

Also paragraph > 300 words flagged.

Page flagged: pages with suspect lines inside a paragraph (or long paragraphs? Plan: "A page is flagged when it has a suspect line inside a paragraph"; long-paragraph flag also counts for pages flagged? Tab 03 row "Why" includes "paragraph over 300 words". I'll include long paragraphs in flagged pages too, listing reason.)

First words: tokenise: split whitespace, take tokens, clean each: strip digits glued at end of word: token.replace(/\d+$/,''), skip tokens that are only digits, take first 6.

Normalise compare: replace curly quotes “”‘’ → straight, – — → -, collapse whitespace.

Checks:
1. paragraph count vs reference.paragraphs.
2. numbering 1..n in order; gaps/dups listed.
3. first words: mismatch count, list up to some.
4. suspect lines: counts.
5. pages flagged list.
6. headers/footers: pages with symbol first line, pages with page number, bare numbers removed.
7. headings: counts + unlabelled list.
8. nothing lost: total non-empty lines vs classified counts; unclassified listed.

Header check expected all pages have symbol first line; footer page number expected all but first. I track these during classification.

Repairs: array of {page, target, what, before, after}. Kinds: header line removed, footer line removed, bare number removed from the footer, number and text split, paragraph joined across a page break, heading separated, heading title joined. Count per kind shown above repair log table.

"paragraph joined across a page break": when a paragraph's lines carry ≥2 distinct pages (log once per paragraph? per plan, logged when a paragraph's lines carry two page numbers — log once per paragraph).

CSV: columns as listed, plus text_lines? The plan lists columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, flagged, suspect_lines, repairs, citation, symbol, doc_url. text_raw — the original lines? It says `text_lines` earlier keeps original lines "for the toggle and the CSV column `text_lines`" but the download spec lists `text_raw`. I'll include both text_raw = lines joined with " | " (and name it text_raw per download spec; maybe include both text_raw). I'll output exactly the listed columns, with text_raw = lines joined " | ".

CSV: BOM, CRLF, quotes doubled.

Copy citation button with navigator.clipboard fallback (sandbox — clipboard may fail; use try/catch, fallback textarea execCommand). Show "Copied" 2s.

Tabs with role=tablist, arrow keys.

Tab 01: four tiles.

Tab 02: table rows expandable; headings found collapsible box; expanded shows full text, "Show the PDF's lines" toggle, first-words comparison, pages, repairs, copy citation.

Tab 03: flagged pages rows; click expands showing raw lines of the page with suspect highlighted and paragraph indicated.

Tab 04: checks panel; repair log collapsible; raw pages collapsible with select and coloured lines; download button.

Raw page viewer: classify each raw line: header (first non-empty = symbol), footer lines, cover (before first para start... need mapping), heading, paragraph, suspect. I'll compute a map from (page, lineIndex) → kind. During classification I assign kinds: header, footer, cover, heading, paragraph; then mark paragraph lines that are suspect as 'suspect' (but still paragraph). Legend with letter codes: C, H, HD, P, S, F or so: C cover, HD header? plan letter codes: cover, header, heading, paragraph, suspect line, footer — codes C, H, G, P, S, F? I'll use C=cover, H=header, T=heading(itle), P=paragraph, S=suspect, F=footer. Tints pale.

Also footer page-number line kind footer.

Check "nothing lost": count non-empty lines per page; classified kinds counts; sum. Since every line gets a kind, should pass; but compute honestly: track classifiedCount and unclassified list. Lines that are empty are skipped (not counted). I'll mark each raw line's kind during processing: build per-page array kindOf[pageIndex][lineIdx]. Cover lines: non-empty body lines before first paragraph start not heading. Assign as I go.

Implementation approach: I'll run the pipeline on raw lines and record kinds directly.

Let me structure code:

```js
function analyse(doc){
  const D = doc; const symbol=D.symbol;
  const pages=[...D.records].sort((a,b)=>a.page-b.page);
  const pageInfo = pages.map(p=>{
    const lines = p.text.split(/\r?\n/);
    return {page:p.page, lines};
  });
  // classification
  const kinds = pages.map(()=>[]); // kind per line index
  const bodyLines=[]; // {text,page,lineIdx}
  const repairs=[]; let headersFound=0, pageNoPages=[], bareFoot=[];
  pages.forEach((p,pi)=>{
    const lines=pageInfo[pi].lines;
    // header
    let fi=lines.findIndex(l=>l.trim()!=='');
    if(fi>=0 && lines[fi].trim()===symbol){kinds[pi][fi]='header';headersFound++;repairs.push({page:p.page,target:'—',what:'header line removed',before:lines[fi],after:'—'});}
    else {repairs.push({page:p.page,target:'—',what:'WARNING: first non-empty line is not the symbol',before:fi>=0?lines[fi]:'',after:'—'});}
    // footer from end
    let i=lines.length-1;
    while(i>=0){
      const t=lines[i].trim();
      if(t===''){kinds[pi][i]='empty';i--;continue;}
      if(/^GE\./.test(t)||/^\d{6}( \d{6})*$/.test(t)){kinds[pi][i]='footer';repairs.push({page:p.page,target:'—',what:'footer line removed',before:t,after:'—'});i--;continue;}
      let m=t.match(/^(\d{1,3})$/);
      if(m){ 
        if(Number(m[1])===p.page){kinds[pi][i]='footer';pageNoPages.push(p.page);repairs.push({page:p.page,target:'—',what:'footer line removed',before:t,after:'—'});}
        else{kinds[pi][i]='footer';bareFoot.push({page:p.page,number:m[1]});repairs.push({page:p.page,target:'footnote no. '+m[1],what:'bare number removed from the footer',before:t,after:'—'});}
        i--;continue;
      }
      break;
    }
    // body
    for(let j=0;j<lines.length;j++){
      if(kinds[pi][j])continue;
      const t=lines[j].trim();
      if(t===''){kinds[pi][j]='empty';continue;}
      kinds[pi][j]='pending';
      bodyLines.push({text:t,page:p.page,pi,lineIdx:j});
    }
  });
```

Hmm, wait: the footer scan from end stops at first non-footer non-empty. But header line index fi is set as footer too? The header is at start; fine.

Edge: page 1 footer may include "GE.25-15926 (E)" — starts with GE., matches. Date stamp "051125 061125" matches 6-digit groups. Good.

Then main pass over bodyLines:

```js
  const isLabel=l=>/^([IVX]+|[A-Z])\.$/.test(l);
  const paraAlone=l=>l.match(/^(\d{1,3})\.$/);
  const paraInline=l=>l.match(/^(\d{1,3})\. (.+)$/);
  const isParaStartLine=l=>paraAlone(l)||paraInline(l);
  const paras=[], headings=[], coverCount={}; 
  let cur=null, headingMode=null, section=null, part=null, sectionLabel=null;
  let seenPara=false;
  const pushPara=()=>{if(cur){finalize(cur);paras.push(cur);}cur=null;};
```

finalize: join lines, compute page_start/end, text, suspect, word count, first words, pageBreak repair if pages>1 (log once), repairs attach.

Actually suspect computed in finalize.

Main loop over bodyLines with index k:

```js
  for(let k=0;k<bodyLines.length;k++){
    const bl=bodyLines[k], l=bl.text;
    if(headingMode){
      if(isLabel(l)||isParaStartLine(l)){headingMode=null;/*fall through to handle below*/}
      else if(l===''){continue;}
      else {
        if(/^[a-z(]/.test(l)&&headingMode.lines.length){headingMode.lines[headingMode.lines.length-1]+=' '+l;repairs.push({page:bl.page,target:'heading “'+headingMode.lines.join(' ')+'”',what:'heading title joined from two lines',before:headingMode.lines[headingMode.lines.length-1],after:l});}
        else headingMode.lines.push(l);
        kinds[bl.pi][bl.lineIdx]='heading';
        continue;
      }
    }
    if(isLabel(l)){
      pushPara();
      headingMode={label:l.replace(/\.$/,''),lines:[],page:bl.page,pi:bl.pi,lineIdx:bl.lineIdx};
      kinds[bl.pi][bl.lineIdx]='heading';
      continue;
    }
    if(headingMode){ // exited above via fallthrough with current l
      // close heading: set section/part
      headings.push(headingMode); register...
    }
```

Hmm, awkward. Let me restructure: when in headingMode and encounter label/paraStart, first close the heading, then process l normally.

Let me write cleanly:

```js
  const closeHeading=()=>{ if(!headingMode)return;
    const h=headingMode; headingMode=null;
    const title=h.lines.join(' ');
    headings.push({label:h.label, title, type:/^[IVX]+$/.test(h.label)?'roman':'letter'});
    if(type roman) part = h.label+'. '+title; else section = title; 
    // also section = title for roman? plan: section = most recent heading line, part = most recent roman. So set both: section=title; if roman part=label+'. '+title.
  };
```

Wait "Each paragraph's `section` is the most recent heading line before it and `part` the most recent roman-numbered heading". So section = most recent heading (any), part = most recent roman. OK: section=title always; if roman, part = h.label + '. ' + title.

Continue loop:

```js
    if(isLabel(l)){ pushPara(); closeHeading(); headingMode={...}; kinds='heading'; continue; }
    if(isParaStartLine(l)){
      closeHeading(); pushPara();
      let firstLineText=null, num;
      let m=paraAlone(l);
      if(m){num=+m[1];}
      else {m=paraInline(l); num=+m[1]; firstLineText=m[2]; repairs.push({page:bl.page,target:'para. '+num,what:'number and text split',before:l,after:num+'. | '+firstLineText});}
      cur={number:num, lines:[], pRepairs:[], section, part};
      kinds[bl.pi][bl.lineIdx]='paragraph';
      if(firstLineText!=null)cur.lines.push({...bl,text:firstLineText});
      // mark raw line? The raw line contains number+text; kind paragraph. fine.
      seenPara=true;
      continue;
    }
    // unlabelled heading?
    const next=bodyLines[k+1]; // next non-empty? plan "immediately followed". I'll look at next body line (body lines already exclude empties!). bodyLines only has non-empty lines. So next = bodyLines[k+1], its text check isParaStartLine.
    if(next && isParaStartLine(next.text) && l.length<=90 && /^[A-Z]/.test(l) && !/[.;:,]$/.test(l) && !/\d$/.test(l)){
      closeHeading(); pushPara();
      section=l; headings.push({label:null,title:l,type:'unlabelled'});
      kinds[bl.pi][bl.lineIdx]='heading';
      repairs.push({page:bl.page,target:'para. '+(next? extract num),'what':'heading separated from paragraph text',before:l+' '+nextnum...,after:...});
```

Hmm keep simpler: before: l, after: l + ' (treated as a heading, kept out of paragraph text)'. Plan wants Before|After columns; for heading separated, before could be "…last para line? " Actually the unlabelled heading is a line that would have been glued to previous paragraph. Before: previous paragraph text end + heading; I'll do before: "previous paragraph … + " + l; simpler: before: l, after: 'heading: '+l. I'll do: before: l (would join the following paragraph), after: 'kept as heading'. Fine.

But also: unlabelled heading check requires seenPara? If before first para start and next is para start — e.g. on cover, "Introduction" is preceded by label "I." handled. A cover line directly before para 1 that looks like heading — plan says cover lines are before first paragraph start; but if a line qualifies as unlabelled heading it's a heading. Both fine; the check "Nothing lost" counts both. I'll allow it regardless of seenPara (but not in heading mode — handled since headingMode closed... actually in headingMode the fallthrough: after closeHeading, l gets here. If we're in heading mode and l is not label/paraStart, we already continue'd. Right.)

Wait order: in my loop, headingMode block: if l is label or paraStart, close heading and fall through; else handle as heading text and continue. Then label check, paraStart check, unlabelled check, else:

```js
    if(!seenPara){ kinds='cover'; continue; }
    // paragraph text
    if(!cur){ // stray line between paragraphs (after heading close?) — could happen if heading text after para... attach as paragraph? Shouldn't happen; classify cover? Let's start a new "orphan" paragraph? Plan expects none. I'll classify as 'cover' if !cur and !seenPara else... if seenPara and !cur, it's a stray line — create orphan paragraph without number? For "nothing lost" I'll classify as paragraph attached to... Simplest: treat as paragraph line of a null-number paragraph (excluded from paras list but counted). I'll create cur with number null and mark it; but numbering check expects 1..n. Orphans would break CSV. Given data, headings consume their text, so strays unlikely except… after "heading title joined" etc. I'll create orphan paragraphs and list them in nothing-lost as unclassified? No—they're paragraph lines. I'll push them as paragraphs with number null but exclude from main table? Risky. Given the plan says every non-empty line classified exactly once, and given the pipeline, strays get kind 'paragraph'. I'll allow cur=null → skip attaching but kind 'paragraph' and count in a "stray paragraph lines" count shown? Keep simple: kind 'paragraph', attach to a pseudo cur if exists else count as strayLine (listed in nothing-lost as unclassified-ish). I'll just create orphan record appended to paras with number null, and filter in display... Actually simplest and safe: if !cur, start cur with number = null; at finalize, if number===null, don't push to paras but record in strayLines list for the check. Good.
    cur.lines.push(bl); kinds='paragraph';
```

finalize(cur):
```js
function finalize(cur){
  if(!cur.lines.length)return;
  const text=cur.lines.map(x=>x.text).join(' ').replace(/ {2,}/g,' ').trim();
  cur.text=text;
  cur.page_start=cur.lines[0].page; cur.page_end=cur.lines[cur.lines.length-1].page;
  if(cur.page_start!==cur.page_end){repairs.push({page:cur.page_start+'–'+cur.page_end,target:cur.number!=null?'para. '+cur.number:'—',what:'paragraph joined across a page break',before:'paragraph split over pages '+...,after:'joined into one paragraph ('+cur.page_start+'–'+cur.page_end+')'});}
  // suspect
  cur.suspects=[]; let sus=false;
  for(const ln of cur.lines){
    if(sus && ln.page===susPage){mark} // rule: once a suspect line found, all lines to end of its page are suspect
    ...
  }
```

Suspect rule: "A suspect line and every line after it to the end of its page are suspect". Implement: iterate lines; flag=false; for each line: if(!flag && isSuspect(line.text)){flag=true;flagPage=line.page;} if(flag && line.page===flagPage){suspect} — but if line.page changes (new page), flag stays? "to the end of its page" — so only same page. Reset flag when page changes? If a later page's line is suspect on its own, it re-flags. I'll set: for each line, if line.page===flagPage&&flag → suspect; else check isSuspect(line) → if yes set flag,flagPage and suspect. When page differs from flagPage, flag effectively off unless line itself suspect. Hmm but paragraph spanning page: lines on next page not suspect unless themselves match. Good.

isSuspect(l): /^\d{1,3}$/.test(l) || /^\d{1,3} [A-Z("“]/.test(l)

Mark kinds[pi][lineIdx]='suspect' for those (overrides 'paragraph').

cur.suspectLines = list {page, lineIdx(1-based within raw page? use raw line number = lineIdx+1), text}.
cur.flagged = suspects.length>0 || wordCount>300.
cur.words = text.split(/\s+/).length.
if words>300, longPara flag with reason.

Also track hyphen-ending lines count: lines.filter(t=>/[a-z]-$/.test(t)) count overall.

firstWords: 
```js
function fw(text){const toks=text.trim().split(/\s+/);const out=[];for(const t of toks){const c=t.replace(/\d+$/,'');if(!c)continue;if(/^\d+$/.test(c))continue;out.push(c);if(out.length===6)break;}return out.join(' ');}
```
Wait "dropping tokens that are only digits and digits glued to the end of a word ('waste.2' becomes 'waste.')" — so token "17" dropped; "waste.2"→"waste.". My code: c = t.replace(/\d+$/,''); if c empty (pure digits) skip. Good.

norm(s): s.replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim().

match = norm(found)===norm(ref) when ref present.

paras list sorted by number (they're in document order already; numbering check compares sequence 1..n).

Checks array built:
- {name:'Paragraph count', pass: paras.length===ref.paragraphs, detail:`found ${paras.length} / reference ${ref.paragraphs}`}
- numbering: numbers equal 1..n sequential; list gaps/dups.
- first words: mismatches list.
- suspect lines: `${sCount} suspect lines on ${pages} pages, in ${paras} paragraphs; none removed` — pass always true (informational)? Plan: "n suspect lines on n pages, in n paragraphs; none is removed." It's a statement; pass=true.
- pages flagged: list, pass=true? It's informational ("A flag is not a failure"). Show as pass? I'd show as "flag" style—use pass styling but text "flagged". I'll render pass (green) since not failure, with text.
- headers/footers: header check: headersFound===pages.length; page numbers: pageNoPages.length===pages.length-1 (expected all but first). pass accordingly.
- headings: counts + unlabelled list, pass true.
- nothing lost: sum of classified non-empty vs total non-empty; unclassified listed; pass if equal and none unclassified.

Count classified non-empty: iterate kinds arrays: kind!=='empty' && kind set && kind!=='pending'. pending lines that never got classified (shouldn't happen since loop covers all body lines... every body line goes through loop; if in headingMode all continue as heading; else label/paraStart/unlabelled/cover/paragraph — all assigned). But 'pending' remains for lines... I set 'pending' when building bodyLines, then the main loop assigns cover/heading/paragraph/suspect. But lines inside headingMode fallthrough get assigned. OK. Any still 'pending' → unclassified.

Total non-empty lines = sum over pages lines.filter(t=>t.trim()!=='').length.

Also count kinds for raw viewer: cover, header, heading, paragraph, suspect, footer, empty.

Now checks pass count = number passing; header badge "n of m checks pass" green or red.

Now UI. I'll write render functions producing innerHTML strings mostly, plus event delegation.

Layout: header top; below: grid rail (left, ~280px) + main. Tabs across main top. Panels.

Tab 01 tiles: paragraphs found (with ref, diff), pages flagged, first words match, repairs (link to tab04 repair log — clicking activates tab 4 and opens repair log).

Tab 02: headings found box (collapsible, lists headings), table rows. Each row: button tr-like div. Expanded region below with details.

Tab 03: note + rows per flagged page; expand shows raw lines with suspect highlighted.

Tab 04: checks list; repair log collapsible (table); raw pages collapsible (select + monospace panel with legend); download button.

CSV generation as spec'd.

Doc selection: cards for each key in WORKSHOP_DATA with records && reference. pdf_text, pdf_text_2 both qualify (uhri etc. have no reference). Selected state; re-run and re-render.

Fonts/colors per design. Focus ring visible.

Write it. Aim ~900-1100 lines.

Row expansion: I'll render paragraph rows as divs with button header and hidden detail.

For tab 02 table semantics with expandable rows — use actual <table>? Expansion inside table is messy. Use div grid styled as table with caption. But design says tables with th scope. I'll use table for the main list where each row is a <tr> button-like with a following hidden <tr class=detail>. Clicking toggles. Caption present. Columns: No. | Section | Page | First line | Check. th scope col. That works: detail row spans all columns.

For headings box: a button aria-expanded toggling a list.

Tab 03 rows similar pattern.

Arrow-key tabs: keydown on tablist.

Copy: async navigator.clipboard.writeText; fallback: textarea+execCommand.

Big numbers in rail: paragraphs found (with "of ref" + bar), pages flagged, checks pass.

OK, also "051125 061125" might appear as one line "051125 061125" — regex handles. Also might be "051125" "061125" separate — each matches.

One more: page 1 header line: first non-empty line equals symbol — sample page 1 first line "E/C.12/GC/27" yes.

Bare number in footer equal to page: e.g., page 2 footer "2". Note pages might have the bare footnote number AND page number; both matched.

Danger: footer scan might strip a legitimate short paragraph line at page bottom if it's a bare number — but para numbers have "." so no.

Careful with the date line "6 November 2025" on cover — starts "6 " with capital N... isSuspect would flag it, but cover lines aren't in paragraphs, so fine.

Suspect regex `/^\d{1,3} [A-Z("“]/` — "7 E/2003/22" starts digit space E (capital) ✓. "2 Summary for policymakers" ✓. Also lines starting with quote after number per plan.

Now the "first 120 chars cut at a word": cut text at 120, then trim to last space, add "…".

Section column: cur.section; part for expanded path: if part && part!==section show part+' › '+section.

Let me also handle reference missing gracefully (ref may be undefined): tiles say "no reference in this file", checks "not run".

Rendering approach: build HTML strings, then attach listeners via delegation on containers.

Let me now write the file. I'll keep it organized.

Number formatting small details: page badge "n of m checks pass".

For suspect lines in flagged pages tab: page's raw lines with suspect highlighted: iterate page lines, mark those with kinds='suspect' or footer etc.? Show all raw lines with suspect ones highlighted (red tint), maybe footers dimmed. And note the paragraph(s) they sit in.

Flagged page record: {page, paragraphs:[numbers], suspects:[{lineNo,text}], reasons}.

Also paragraphs >300 words: flagged paragraph with reason "paragraph over 300 words"; page flagged too (its page_start).

Let me write.

CSV columns order: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, flagged, suspect_lines, repairs, citation, symbol, doc_url.

text_raw: lines joined with " | ". suspect_lines: "p3 l14: text" joined "; ". repairs: what list joined "; ".

Escape CSV: `"` → `""`, wrap in quotes, join CRLF, BOM "\uFEFF".

Filename: symbol.replace(/\//g,'-') + '-paragraphs.csv'.

Alright, writing code now. I'll be efficient.

Also tabs hidden panels: hidden attribute; CSS [hidden]{display:none!important}.

Tab arrow nav: standard.

I'll write a single render(doc) that re-renders everything.

State: currentDocKey, expanded sets (paragraph numbers expanded, flagged pages expanded, toggles). Keep simple: re-render on interactions via event delegation and toggling hidden attributes directly rather than full re-render.

Let me write HTML skeleton with static containers and JS fills rail, tabs, panels.

Time to write.

For the checks "links to rows concerned": first-words check links to tab 02 with mismatched paras; pages flagged links to tab 03. I'll add links that switch tabs.

Repair log open from tile 01: function openRepairLog() → switch tab 4, set aria-expanded true, show log.

Also numbering check gap listing.

Word count >300: "may contain footnote text" check cell shows? The Check cell in tab 02: "OK", "first words differ", "may contain footnote text" (when flagged). If both differ and flagged, show both? I'll show joined with "; ".

OK code:

I'll now write the final file mentally structured:

```html
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Paragraphs out of a PDF</title><style>...</style></head>
<body>
<header id="appHeader"></header>
<div class="layout">
  <aside id="rail"></aside>
  <main>
    <div class="tabs" role="tablist" id="tablist"></div>
    <section id="panel1" role="tabpanel"></section> ... 4 panels
  </main>
</div>
<footer id="appFooter"></footer>
<script>...</script>
```

CSS: paper colors, fonts, tiles, tables, chips, etc.

Write it. Also ensure buttons keyboard accessible (rows: I'll make the visible <tr> contain a button? A <tr> can't be a button. I'll put a button inside first cell spanning? Simpler: make the row itself focusable with role="button" tabindex=0 and keydown Enter/Space. Plan says "Rows are buttons with aria-expanded". I'll use role="button" tabindex 0 aria-expanded on the tr, handle click + keydown. Acceptable.

Actually to be safer for a11y semantics, I'll use div-based "table" with role attributes? The design asks for th scope etc. I'll keep real table; tr with tabindex=0 role="button" aria-expanded. Fine.

Now write everything concretely.

Pipeline code — one more consideration: heading mode entry when label found while cur paragraph open: pushPara first. Yes did.

Cover count kinds: 'cover'.

Also headingMode lines kinds set to 'heading' — but the label line itself too.

closeHeading also needs: when heading mode ends because of para start or label or unlabelled heading or end. At end of loop, closeHeading() + pushPara().

Also note: within headingMode, a blank body line doesn't exist (bodyLines excludes empties). Good, so "skip blank lines" moot.

Also "heading title joined": when line starts lowercase or "(" — join to previous heading line. Log repair with before/after.

Unlabelled heading repair target: the following paragraph number. I can compute from next line match.

Edge: label regex /^([IVX]+|[A-Z])\.$/ — careful: a paragraph line like "A." unlikely. OK.

One more: paraInline regex `^(\d{1,3})\. (.+)$` — could also match footnote-ish "7 E/..." no (needs period). Could match a reference line "1989. Something"? Rare, accept.

But danger: "I." also matches isLabel; and inline para numbers like "1. A clean..." — good.

However, isParaStartLine on "2. " etc. Also section labels like "A." handled before paraStart check? Order in loop: headingMode, label, paraStart, unlabelled, cover/paragraph. "A." matches isLabel → treated as label. Good.

Also what about text lines within a paragraph that are e.g. "17 Sustainable Development Goals" mid-paragraph — it's a paragraph line, becomes suspect (flagged) per plan. Good.

Now compute results object:

```js
result={pages,pageInfo,kinds,paras,headings,repairs,checks,flaggedPages,stats:{...}}
```

Rendering numbers.

Checks list construction with ref fields possibly missing.

Let me also compute mismatch list for first words (cap display at, say, all of them — likely 0).

"Nothing lost": unclassified = lines where kind==='pending' after processing (also kind undefined for lines not touched? every line got 'empty' or 'pending' or header/footer kinds in page pass; pending resolved in main loop; but bodyLines only includes non-empty → pending set for all non-empty non-header/footer). But wait: in the page pass I set kinds for header/footer/empty; body lines set 'pending' and pushed. Main loop resolves each. Good.

Line numbering in raw viewer: 1-based per page.

Legend colors: pale tints:
cover #efe6d8, header #e3e8e6? Let me pick: cover #ece3d2 (tan), header #e6e0f0? Keep muted: 
- cover: #eae0cd
- header: #e2e6e9
- heading: #e7e3d5? need distinct 6: 
cover #e9dfc8, header #dfe6ea, heading #e6e0d0, paragraph #f4f0e8 (paper), suspect #f3d9dc (pale red), footer #e4e4e4. Letter codes: C, HD, T, P, S, F. Hmm codes: "each doubled by a letter code in the margin": I'll prefix line with code.

OK, writing final answer now. Three sentences before code block.

Let me draft the JS fully in my head as I write. I'll be careful with details but pragmatic.

Also remember: "adopted" line in header: `reference.adopted` — show "adopted …".

Rail doc cards: for each qualifying dataset: symbol monospace, short title (use title), adopted, n pages. Click selects.

Note: pdf_text.built? It has source, count. Footer: "Source line, `built` date" — pdf_text may not have built; guard.

Alright — code.

Estimate line count ~1000. Go.

One subtlety in footer loop: I mark kinds and log repairs for every footer line (page number and GE code) — that's a lot of repairs (2-3 per page × 20 = ~50). Plan says log each ("footer line removed" is a named repair kind). Fine.

Repair counts per kind displayed above log.

Citation copy fallback.

For the "Show the PDF's lines" toggle in expanded paragraph: lines with page markers where page changed.

Now writing.

For tab switching with panels hidden and aria.

Also "the tab panel of a hidden tab is not focusable": panels get hidden attribute → display none, not focusable. Good.

Let me write the code now, final.

Also the header check mark dot: green #2e6b3a or red.

Checks store: {label, status:'pass'|'fail'|'info', detail, link?}

passCount = checks.filter(pass).length; total = checks.length. If any fail → red "n checks failed" (show "n of m checks pass" too?). Plan: green "n of m checks pass", or red "n checks failed". I'll show red "n of m checks failed" plus pass count maybe. Use: if fails>0: `${fails} of ${total} checks failed` red.

'info' checks (suspect lines, pages flagged, headings) count as pass? They're informational; I'll count them as pass (they verify invariants, e.g., "none removed" is true). Fine.

Numbering check: pass if numbers === 1..n exactly in order.

Write now. Also remember footer's "n of m checks pass" linking to tab 04 (it's in the rail per plan; header shows dot + text). Header right: dot + "n of m checks pass" or red. Rail also shows it linking to tab 04.

Let me write.

```js
const W = window.WORKSHOP_DATA;
const DOC_KEYS = Object.keys(W).filter(k=>W[k]&&Array.isArray(W[k].records)&&W[k].reference);
```

Wait — plan says "every document in WORKSHOP_DATA with records and a reference". pdf_text and pdf_text_2 both have reference. Good.

analyse(key) returns result; cache per key.

I'll write renderAll().

Go — write the actual file text now.