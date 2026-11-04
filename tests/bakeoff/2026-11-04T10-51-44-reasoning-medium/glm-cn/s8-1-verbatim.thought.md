Build the full app per the plan. Need to be careful but concise. Single HTML file, four tabs, filters rail, search parser, highlighting, checks panel, draft tab with localStorage, chart, downloads. Keep under ~1500 lines.

Let me design the code carefully.

Key pieces:

- Data: WORKSHOP_DATA.gc: {title, source, count, records}.
- Load prep: for each record compute norm, marks, leading, pinpoint, citation, shared (symbol with >1 title), joint (two symbols), committees.
- committees: regex over symbol for codes: handle "CAT/OP" → CAT-OP? The plan says "CAT-OP" for CAT/OP. Codes: CAT, CCPR, CED, CEDAW, CERD, CESCR, CMW, CRC, CRPD, and CAT-OP. Regex on symbol: find "\bCAT/OP\b"? Actually symbols like "CAT/OP/12/..." — detect "CAT/OP" first → "CAT-OP". Then other codes. Plus `committee`.
- Committee full names: CAT: Committee against Torture; CAT-OP: Subcommittee on Prevention of Torture; CCPR: Human Rights Committee; CED: Committee on Enforced Disappearances; CEDAW: Committee on the Elimination of Discrimination against Women; CERD: Committee on the Elimination of Racial Discrimination; CESCR: Committee on Economic, Social and Cultural Rights; CMW: Committee on Migrant Workers; CRC: Committee on the Rights of the Child; CRPD: Committee on the Rights of Persons with Disabilities.

- Query parser: tokens. Grammar: or := and (OR and)*; and := not ((AND)? not)*; not := NOT not | primary; primary := '(' or ')' | phrase | word. Leading '-' before a word at primary position = NOT.

Echo: build English. For a phrase: the phrase “...”; word: the word child. AND → "and", OR → "or", NOT → "without"/"not". NOT-only query: top-level is NOT node → matches everything lacking. Detect: every positive term is under negation... simpler: walk tree, collect positive terms; if none, NOT-only.

- Term regex: escape word, trailing `*` → `\w*`; boundaries `(?<![\p{L}\p{N}])` `(?![\p{L}\p{N}]))` flag u. Phrase: words joined by `\s+` inside same boundaries (words themselves normalized).

- Highlight regex over shown text: word escaped but map: `'` → `['‘’']`, `"` → `["“”]`, `-` → `[-–—]`. Phrase words joined by `(?:\s|\[\[fn:\d+\]\])+`. Wrap `<mark>` after HTML escaping. To do this safely: build regex with alternation of positive term regexes, then split the shown text via matchAll on the raw text and escape around. Use a global regex on the raw shown text; since shown text may contain footnote marks (when "show as stored" toggled), include them in gaps. I'll build a single combined regex with alternation of positive terms (in highlight form), global flag, then build HTML by escaping segments between matches and wrapping matches in <mark>.

- Filters: committee checkboxes (all ticked), years from/to, document select (short_title grouped by committee via optgroup). Chips removable.

- Hits computation: recompute on any change. Render tabs.

- Tabs: 01 OVERVIEW, 02 PARAGRAPHS, 03 DRAFT (n), 04 CHECK. Tablist with arrow keys.

- Overview: Chart.js horizontal bar per committee ranked, value at end (use plugin or just formatted ticks... simpler: custom afterDatasetsDraw or use `datalabels`-style manual plugin). I'll write a small inline plugin to draw value at end of bar. Axis from zero. Click bar → tick that committee alone. aria-label with numbers, table beside.

- Paragraphs tab: summary line, order select, results 25 per page, show more. Rows: article elements with heading (badge, short_title, symbol link, pinpoint, year), text shown (footnote marks removed, marks highlighted, pre-wrap), footnote line, expand full paragraph, amber notes, click row opens detail buttons: copy citation, copy quotation, add to draft, context prev/next inline.

Copy quotation: shown text in quotes — the cleaned text (footnote marks removed), drop leading "12. " if leading==paragraph. Use typographic quotes? "copies the shown text in quotation marks" — I'll use curly double quotes “...”.

- Draft tab: list items, remove, copy all, download txt/csv with BOM.

- Check tab: checks computed, quirks.

- Checks: 
  - Query understood: echo + term count or parse error.
  - Totals: rows listed == hits (track shown count vs hits); checkbox bracket counts sum == hits + joint hits.
  - Chart total: bars sum == hits + jointHits.
  - Highlight: every hit has at least one mark unless NOT-only; list "matched, not highlighted".
  - Normalisation: if query contains straight quote/apostrophe/hyphen, count hits that only matched via curly forms... that's hard. Simpler: count hits whose stored text contains curly forms of those characters and no straight form? The plan: "how many hits contain only those forms". I'll count hits whose norm-match would fail if we didn't normalise... approximate: hits where text contains curly quote/apostrophe/en-dash and no straight equivalent. I'll compute: for query containing `'`, count hits where text has ' or ’ but no '; similar for " and -. That's deterministic and honest.
  - Numbering: leading mismatches, shared pinpoints, subparas among hits.
  - Marks: for every hit, marks removed == count of "[[fn:" and reinsert gives stored text — verify by reconstructing: shown = text.replace(/\[\[fn:\d+\]\]/g,''), marks = count. Reconstruct by re-adding? Putting them back exactly: since removal is a simple regex, reinsertion requires storing positions. Instead verify: text.split(/\[\[fn:\d+\]\]/).join('') === shown... trivially true. I'll do: marks count equals occurrences of "[[fn:" and removing them yields the shown text (test by comparing). Fine.
  - Draft: compare stored text of record id vs item.text_as_stored.
  - Quirks at load: paragraph 0 count, shared symbols count, joint docs count, duplicated pinpoints count, leading mismatches count, each with example.

- Copy: navigator.clipboard.writeText, fallback textarea. aria-live message with exact string.

- localStorage draft with try/catch.

- Footer: source, built, credits Chart.js MIT.

- Design: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335. Serif big numbers, monospace labels, sans body.

Let me count clickable on paragraphs tab: tabs (4) + search box + 1 filter heading + order select + show more = 8. OK.

Header checks: run load-time checks (quirk checks all "pass"?). The header shows "n checks pass" — which checks? I'll compute the Check tab checks and count passes/fails at render. On load with no query, many checks trivially pass. Let me define checks list at load: marks check (all records — could be 7304 × cheap check, fine), numbering quirks are data quirks not failures. I'll define the pass/fail set as: totals, chart total, highlight, marks, draft, query understood (pass if no parse error). Header shows count of passing among these. Simpler: run computeChecks() which returns array {name, pass, detail}; header summarizes. On load (empty query), checks mostly pass.

Actually plan says header dot reflects checks; on load with no search, "n checks pass". I'll do that.

Now, size: this is big but let's write it compactly. Aim ~900-1100 lines.

Structure HTML:

```
<header> label / title / meta / checks indicator
<nav role=tablist> 4 buttons
<div id=rail> (aside) filters
<main> sections per tab
<footer>
```

Left rail always visible except Draft tab: hide rail when tab 03 active.

Let me write JS.

Normalization:
```js
function normalize(t){
  return t.replace(/\[\[fn:\d+\]\]/g,'')
    .replace(/[“”„]/g,'"').replace(/[‘’‚]/g,"'")
    .replace(/[–—]/g,'-')
    .replace(/\s+/g,' ').toLowerCase();
}
```
Soft hyphen → '-' too: /[\u00AD]/. Include.

Tokenizer:
```js
function tokenize(q){
  const toks=[]; let i=0; const s=q;
  while(i<s.length){
    const c=s[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='"'||c==='“'||c==='”'){
      let j=i+1, out='';
      while(j<s.length && !('"“”'.includes(s[j]))){ out+=s[j]; j++; }
      if(j>=s.length) throw 'unbalanced quote';
      toks.push({t:'phrase',v:out}); i=j+1;
    } else if(c==='('){toks.push({t:'('});i++;}
    else if(c===')'){toks.push({t:')'});i++;}
    else {
      let j=i,out='';
      while(j<s.length && !/[\s()]/.test(s[j]) && !'"“”'.includes(s[j])){out+=s[j];j++;}
      // check operators
      const up=out.toUpperCase();
      if(out==='('||out===')'){...} // handled
      if(up==='AND'||up==='OR'||up==='NOT'){toks.push({t:up});}
      else if(out.startsWith('-')){toks.push({t:'NOT'});toks.push({t:'word',v:out.slice(1)});}
      else toks.push({t:'word',v:out});
      i=j;
    }
  }
  return toks;
}
```
Hmm a word could be like `(torture` — since I stop at parens, ok.

Parser: convert to tree with implicit AND.
```js
function parse(toks){
  let p=0;
  function peek(){return toks[p];}
  function parseOr(){
    let l=parseAnd();
    while(peek()&&peek().t==='OR'){p++;const r=parseAnd();if(!r)throw 'OR needs a term after it';l={op:'OR',l,r};}
    return l;
  }
  function parseAnd(){
    let l=parseNot();
    while(peek()&&peek().t!=='OR'&&peek().t!==')'){
      if(peek().t==='AND'){p++;}
      const r=parseNot(); if(!r)break/throw;
      l={op:'AND',l,r};
    }
    return l;
  }
  function parseNot(){
    if(peek()&&peek().t==='NOT'){p++;const r=parseNot();if(!r)throw 'NOT needs a term after it';return {op:'NOT',a:r};}
    return parsePrim();
  }
  function parsePrim(){
    const t=peek();
    if(!t) return null;
    if(t.t==='('){p++;const e=parseOr();const c=peek();if(!c||c.t!==')')throw 'unbalanced parenthesis';p++;return e;}
    if(t.t===')')throw 'unbalanced parenthesis';
    if(t.t==='AND'||t.t==='OR')throw 'two operators in a row';
    p++;return {op:'term',term:t};
  }
  const root=parseOr();
  if(p<toks.length) throw 'unexpected “'+ (toks[p].v||toks[p].t) +'”';
  if(!root) return null; // empty
  return root;
}
```

Echo: recursive.
```
term: phrase → the phrase “x”; word → the word x
AND: A and B
OR: A or B
NOT: not A? "paragraphs without ..." I'll echo "not (x)" or for top-level NOT-only... echo as "without x".
```
Keep simple: echo(node): term→desc; AND→ `${a} and ${b}`; OR→`${a} or ${b}`; NOT→`not ${a}`.

Positive terms: collect terms not under NOT ancestor.

Match:
```js
function termRegex(term){ // for norm
  let v=normalize(term.v);
  if(term.t==='phrase'){
    const words=v.split(/\s+/).filter(Boolean).map(esc);
    return new RegExp('(?<![\\p{L}\\p{N}])'+words.join('\\s+')+'(?![\\p{L}\\p{N}])','u');
  }
  let w=esc(v); let star=false;
  if(w.endsWith('\\*')){w=w.slice(0,-2)+'\\w*';star=true;} // esc escapes * as \*
  return new RegExp('(?<![\\p{L}\\p{N}])'+w+'(?![\\p{L}\\p{N}])','u');
}
```
esc = regex escape. Note normalize lowercases; norm is lowercase; good. Phrase words joined by \s+ (norm has single spaces).

eval(node, normTestFn): term → test; AND/OR/NOT.

Highlight regex over raw shown text: build per term:
```js
function hlPart(term){
  let v=term.v.trim();
  if(term.t==='phrase'){
    const words=v.split(/\s+/).filter(Boolean).map(w=>hlWord(w));
    return words.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
  }
  return hlWord(v);
}
function hlWord(w){
  let out=''; let star=false;
  let s=w; if(s.endsWith('*')){star=true;s=s.slice(0,-1);}
  for(const ch of s){
    if(ch==="'")out+="['‘’‘’]"; // ['‘’]
    else if(ch==='"')out+='["“”]';
    else if(ch==='-')out+='[-–—]';
    else out+=esc(ch);
  }
  if(star)out+='\\w*';
  return out;
}
```
Wrap whole with boundaries: `(?<![\p{L}\p{N}])` ... `(?![\p{L}\p{N}])`. Combine positive terms with | into one global regex 'gu'. Case-insensitive? The query normalized lowercase for matching norm, but highlight runs on shown text (original case). Use 'giu' flag — but lookahead/lookbehind with 'i' fine. Actually just add 'i'. And for the star, \w* fine.

Careful: lookbehind support — modern browsers OK.

Records prep:
```js
const R = D.gc.records;
const titleSet=new Set(R.map(r=>r.title));
const symTitles={}; R.forEach(r=>{(symTitles[r.symbol]??=new Set()).add(r.title)});
R.forEach(r=>{
  r.norm=normalize(r.text);
  r.marks=(r.text.match(/\[\[fn:\d+\]\]/g)||[]).length;
  const m=r.text.match(/^(\d{1,3})\.\s/); r.leading=m?+m[1]:null;
  r.shownText=r.text.replace(/\[\[fn:\d+\d?\]\]/g,''); // \d+ ok
  r.shared=symTitles[r.symbol].size>1;
  r.joint=/[–,]/.test(r.symbol)&&countCodes>1... 
```
Joint: symbol contains two symbols — detect by counting committee codes in symbol >1, or symbol contains '–' or ', '. Plan: "a joint General Comment (two symbols in one symbol)". I'll detect: /(–|, )/ in symbol AND matches more than one code pattern. Simpler: count codes found via regex global.

Committees of record:
```js
function symCodes(sym){
  const codes=[];
  if(/\bCAT\/OP\b/.test(sym)) codes.push('CAT-OP');
  const re=/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g;
  let m; while(m=re.exec(sym)) if(!codes.includes(m[1]))codes.push(m[1]);
  return codes;
}
r.committees=unique([...symCodes(r.symbol), r.committee]);
```
Careful: "CED" also matches inside "CEDAW"? \b...: CEDAW — 'CED' followed by 'A' — \bCED\b: boundary between D and A? Both word chars so no boundary; good. But "CEDAW/C/GC/..." — CED matches with boundary before '/'? CED inside CEDAW: the regex would try CED at position in CEDAW, followed by A → \b fails. Good.

Pinpoint:
```js
function pinpoint(r){
  if(r.paragraph===0) return 'preamble';
  const sm=r.text.match(/^\(([a-z]{1,4})\)/);
  if(sm) return 'subpara. ('+sm[1]+')';
  return 'para. '+r.paragraph;
}
```
Citation:
```js
function docName(title){ return title.split(/:| on /)[0].trim(); }
function citation(r){
  const p=pinpoint(r);
  if(r.shared) return r.committee+', '+docName(r.title)+' ('+r.symbol+'), '+p;
  return r.symbol+', '+p;
}
```
Hmm "title up to the first colon or ' on '" — order: split at first ':' else ' on '. `title.split(':')[0]` then if same, split ' on '. Do: let t=title.split(':')[0]; if(t===title) t=title.split(' on ')[0]. Good.

Search flow: search button / Enter sets query string, parses, stores tree, echo, error. Changing filters recomputes hits. Hits:
```js
function computeHits(){
  hits = R.filter(r=>{
    if(tree && !evalNode(tree, t=>termRegexCache[t].test(r.norm))) return false;
    if(!ticked intersect r.committees) return false;
    if(r.year<from||r.year>to) return false;
    if(docSel && r.title!==docSel) return false;
    return true;
  });
}
```
Cache term regexes at parse time.

Note: NOT-only query — tree exists but all terms negative: matches records lacking terms — evalNode handles naturally (NOT true when absent). Good; echo note "matches everything without …" — just echo.

Hits per committee: count each hit into each of its committees' counts; jointHits = sum over hits of (committees.length-1) — but committee field may duplicate a sym code; committees is unique set, and the "committee" may equal a sym code. For joint definition: record counts as joint if committees.size>1. jointHits = hits where committees.length>1.

Chart: bars per committee (all committees present in data, or only ticked ones?). Plan: one bar per committee, ranked. I'll show all committees that appear in the full dataset? Or in hits? "Paragraphs per committee" over the paragraphs that match. Show all committees (with zero bars if no hits — maybe filter zeros out? Keep all with values including 0; chart still fine). I'll include all committees in data, sorted desc. Value at end via plugin.

Click bar → tick that committee alone: onClick in chart options, get index, set checkbox states, recompute.

Aria-label: "Paragraphs per committee: CRC 2091, ..." (using current hit counts).

Tabs & rail: rail hidden on Draft tab. Arrow key nav on tablist.

Rows: state per record for expanded/full/stored toggles — keep in a Set of ids.

Pagination: shown count variable, "Show 25 more".

Order comparator: default year desc, then title, then paragraph asc. Select: 'doc' = document order (title then paragraph), 'match' = most matches first (count of positive-term matches in norm? count matches via combined regex count on norm) — precompute per hit when order selected. Simplest: count matches using highlight regex on shown text (global match count). Fine.

Context: prev/next: find records with same title and paragraph ±1; render inline grey with pinpoint.

Amber notes:
- leading mismatch: leading != null && leading !== paragraph → "the text begins 'X.' but the record is para. Y: check the document". Also leading null but paragraph>0? Plan says the 5 where number differs. Just when leading!==null && !==paragraph.
- subpara: text starts with lettered label and paragraph>0 → "a lettered sub-paragraph, numbered N by the file".
- duplicate pinpoint: another record with same title & paragraph → "two records share this pinpoint". Precompute map at load: key title+'|'+paragraph count.
- joint → "joint General Comment".

Copy citation / quotation / add to draft. Copy uses clipboard; fallback: show a box with textarea.

Draft items: {id, citation, symbol, paragraph, pinpoint, committee, short_title, year, text_copied, text_as_stored, doc_url}. text_copied = shownText (marks removed), with leading "N. " dropped if leading===paragraph. Dedup: if id already in draft, don't add again (or move?). I'll skip if present.

Downloads: txt & csv with BOM via Blob and a temp anchor.

localStorage key 'vf_draft'; try/catch.

Checks computation (function computeChecks returns list):
1. Query understood: pass if no parse error; detail echo + term count.
2. Totals: rowsRendered total vs hits.length; checkbox bracket sum vs hits + jointHits.
3. Chart total: bars sum vs hits+jointHits.
4. Highlight: count hits with no mark (not NOT-only) — list up to few.
5. Normalisation: only when query has straight ' " -; count hits containing only curly forms.
6. Numbering: among hits, mismatches/shared pinpoints/subparas — pass if none? These are data quirks; plan says "A failed check marks rows; it never drops them." I'll make it pass=false when count>0 with pinpoints listed, else pass.
7. Marks: verify per hit — pass if all good.
8. Draft: compare items; pass if all match.

Header: count pass/fail across these. Recompute on each render.

Quirks at load (tab 04, before search): 
- paragraph 0 count + example
- shared symbols count (symbols with >1 title) + example
- joint docs count + example
- duplicated pinpoints (title+paragraph pairs with >1 record) count + example
- leading-number mismatches count + example
- lettered subparas count
Show counts & examples.

Highlight check needs rendered marks — but I compute highlight in JS: a hit "has highlight" if the highlight regex matches its shown text. Deterministic; same as rendered.

OK also "bracketed counts" after search: each committee checkbox shows hits count in brackets: count of hits whose committees include that code. Sum = hits + jointHits (each joint counted twice). Good.

Chips: active filters: committees narrowed (not all ticked), years narrowed, document selected. Removable chips.

Now write the whole file. Keep CSS compact. Let's write.

For the value-at-end plugin:
```js
const endLabels={id:'endLabels',afterDatasetsDraw(c){const{ctx}=c;c.data.datasets[0].data.forEach((v,i)=>{const m=c.getDatasetMeta(0).data[i];if(!m)return;ctx.save();ctx.fillStyle='#1d1b18';ctx.font='12px Georgia';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(String(v),m.x+6,m.y);ctx.restore();});}};
```
Chart config: indexAxis:'y', bars color '#9b2335', x grid light, ticks precision 0, no legend.

x max: auto; leave room for label: suggest ticks callback fine.

Chart click: options.onClick(e, elements) → if elements[0], committee = labels[i], tick only that.

Search syntax help: shown when input empty & focused; examples as options (buttons) that fill and run. Close on typing/input event.

Also chips need ids. Let's manage filter state object: {committeeAll bool + set, from, to, doc}.

Simplify committee state: `tick = Set(allCodes)`; "all/none" buttons.

Render functions: renderRail(), renderOverview(), renderRows(), renderDraft(), renderChecks(). renderAll() calls based on active tab.

The header meta: "N paragraphs from M General Comments (distinct title) of K committees, YMIN–YMAX", source linked.

Committee full names map.

Let me now write the code. I'll aim for clarity with moderate compactness.

Edge: paragraph could be 0 and text starts "1." etc. pinpoint preamble fine.

CSV escaping: wrap fields in double quotes, double internal quotes.

Download: 
```js
function download(name, content, type){const blob=new Blob([content],{type});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
```
BOM: '\ufeff'+content.

Copy fallback: keep a hidden div with textarea shown when needed, plus a "Select and copy" — I'll create a section that appears with textarea value and select().

Context prev/next: same title, paragraph-1 / +1. If paragraph 0, prev none.

Row rendering: text truncation at 700 chars at word boundary; full stored line breaks preserved with pre-wrap.

Marks line: "N footnote marks removed · show as stored" toggles per row (state.stored set). When showing as stored, still highlight? Highlight regex includes fn marks in gaps, so yes still works (escape handles). I'll highlight both versions.

Truncation: state.full set → full text. "Show the full paragraph (N words)".

When row clicked (on the article, but not on links/buttons), toggle open state (state.open set). Buttons only in open row. Also context links in open row.

Highlighting function:
```js
function highlightText(raw){
  if(!posTerms.length) return esc(raw);
  const re=new RegExp('(?<![\\p{L}\\p{N}])(?:'+posTerms.map(hlWrap).join('|')+')(?![\\p{L}\\p{N}])','giu');
  let out='',last=0,m;
  while(m=re.exec(raw)){
    out+=esc(raw.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
    last=m.index+m[0].length;
    if(m.index===re.lastIndex)re.lastIndex++;
  }
  return out+esc(raw.slice(last));
}
```
posTerms = positive term nodes.

For NOT-only queries posTerms empty → no marks, fine.

Words count for full paragraph: text.split(/\s+/).length.

Order 'match': count = (shownText.match(hlRegexGlobal)||[]).length — need a global regex; reuse combined. If no posTerms, 0.

Summary line: "279 of 7,304 paragraphs match · 8 committees · 1990–2023" — committees count = distinct committees among hits; years min–max of hits. If no query: "no search words". 

Order select label: options: "year, newest first" (default), "document order", "most matches first".

Now the "aria-live" count in rail: big number.

Rail structure:
```
FILTERS  [Clear all]
BIG NUMBER (aria-live)
of 7,304
search label + input + button
syntax help (hidden, shows on focus when empty)
echo line / error
chips
01 COMMITTEE, YEARS, DOCUMENT (button aria-expanded) → panel
```

Tabs: 01 OVERVIEW · 02 PARAGRAPHS · 03 DRAFT (n) · 04 CHECK.

Tab 04 title: "04 CHECK & METHOD".

OK, writing now. Also focus search on load.

One more: "Rows listed across pages equal the hits" — track totalShown; check compares min(shown, hits)... I'll compare Math.min(shownCount, hits.length) === hits.length ? Actually rows rendered = min(hits.length, shown). Check: renderedCount === hits.length when shown>=hits.length else it's incomplete by design (paged) — check should pass since paging is intentional. I'll check that rendered rows (accumulated) equals min(shown, hits). Trivially true. Better: check that the DOM row count + "not yet shown" equals hits. I'll compute rowsInDom vs Math.min(shown,hits.length). Pass if equal.

Bracketed counts sum: sum over committee checkboxes of count(code) == hits + jointHits where jointHits counted as extra committee memberships: sum over hits of (committees.size - 1)? But committees includes `committee` field which might be an extra code not in symbol (e.g., joint GR "CMW/C/GC/7–CERD/C/GC/38" has one `committee`). For such, committees = {CMW, CERD, committee}. If committee is 'CMW' already, size 2. Sum of checkbox counts = Σ hits |codes∩tick|... if all ticked, Σ|committees|. So sum == hits + Σ(|committees|-1). Define jointExtra = Σ(max(0,|committees|-1)). Chart bars sum likewise. Good, consistent.

Let me define committeeCodes list = all codes appearing (from committees sets), sorted for display maybe by code.

Chart note: "Joint General Comments count under both committees, so the bars can add up to more than the hits" when jointExtra>0.

Alright, write it.

For optgroup document select: group by committee (r.committee), options short_title (distinct), value = title. Distinct short_title→title map (assume 1:1-ish; use first title per short_title... but 188 distinct titles vs short_titles maybe fewer collisions. Use value=title, label=short_title; dedupe by title).

Now writing final HTML. Estimate ~950 lines. Go.

CSS essentials:
- body layout: header, tab nav, then flex: rail (260px) + main.
- [hidden]{display:none!important}
- .mono label style
- mark {background:#f5e6a8; font-weight:bold; color:#1d1b18}
- amber note .note-amber {color:#8a6d1a}
- pass green #1e7a34, fail red accent.
- badge: outlined monospace.
- chips.
- rows article with border-top thin rule.
- focus ring: outline 2px solid #9b2335.

Write JS in one script.

Careful with template literals containing quotes and the HTML escaping.

esc for HTML: replace &<>"'.

Let me write.

Also the syntax help list opens with arrow keys — I'll add keydown ArrowDown/Up on input to focus example buttons; simpler: when help open, examples are buttons; ArrowDown moves focus to first. Implement minimal.

Clear all: reset filters (all ticked, years min/max, doc blank) but keep query? "Clear all" — clear filters and query. I'll clear everything.

Time to write the code.

Draft storage load at init.

Checks: compute in renderChecks and also for header — call computeChecks() storing result; header dot updated.

Header check pass count: count of pass===true among checks; if any fail → red dot + "n checks failed" (show fails count) and red dot on tab 04. Plan: green "n checks pass" or red "n checks failed". I'll show red with number failed.

Quirk computation at load (counts + examples).

Now produce code.

For evalNode with term test function keyed by term object — use Map from term node to regex (precompiled for norm; separate for highlight). Terms are objects {t:'word'|'phrase', v}. Build at search: walk tree, collect all term nodes; for each, normRegex and hlPart. Use Map keyed by node.

Positive terms: walk with negation flag.

Echo: as planned.

Write out.

Row HTML generation function rowHTML(r). Include data-id. State stored in sets: openSet, fullSet, storedSet, ctxSet (context shown). Rerender rows on any toggle (simplest, preserves state via sets). Rerendering on click re-renders whole list — fine.

Text shown base: storedSet.has(id) ? r.text : r.shownText; truncation if !fullSet && length>700: cut at word: slice(0,700), then lastIndexOf(' ').

Truncated text + highlight: highlight applied to the truncated string. Careful: a mark spanning cut — acceptable.

Notes list amber.

Context: find prev = R.find(x=>x.title===r.title&&x.paragraph===r.paragraph-1) — better precompute map by title sorted by paragraph; lookup ±1. For paragraph 0 prev none. Show inline grey text with pinpoint; highlight not applied (grey). Use esc only. Fine.

Buttons: Copy citation, Copy quotation, Add to draft. Copy quotation text: '“' + textCopied + '” ' + citation. textCopied = shownText minus leading number when leading===paragraph: shownText.replace(/^\d{1,3}\.\s/,'') when leading===paragraph.

Copied message aria-live shows exact string (maybe truncated visually? show full, fine).

Add to draft → push, persist, update tab label, message.

Draft tab render: items list, remove buttons, copy all, download txt/csv.

CSV columns order per plan.

localStorage persist on change.

OK. Also "the tab name carries the count: 03 DRAFT (4)".

Now, writing the final file. I'll be careful about length; let's go.