Let me build the app. Single HTML file, inline CSS/JS, Chart.js preloaded. Data from WORKSHOP_DATA.gc.

Key features:
- Title, one-line description: source, count, year range from data.
- Search box + button, Enter works, help line.
- Filters: committee select (all committees + All), year from–to inputs.
- Count line.
- Bar chart per committee of matches.
- Results sorted newest GC first (by year desc, then... maybe paragraph desc? "newest General Comment first" — sort by year desc, then maybe symbol/paragraph). Each card: committee, short_title (fallback title, else symbol), year, symbol linked to doc_url new tab; full paragraph with highlights; Copy citation button copies "symbol, para. paragraph", shows "Copied" 2s.
- Empty state message + tip.

Search parser: tokens. Support AND (implicit space), OR, NOT, quoted phrases. Case-insensitive, whole word matching. Plain word matches whole word — use regex with word boundaries. Need to escape regex special chars. Word boundary: \b works for alphanumeric; for words with apostrophes etc., use a custom boundary: (?<![A-Za-z0-9]) ... (?![A-Za-z0-9])? JS supports lookbehind in modern browsers. Safer: use `(^|[^A-Za-z0-9])word([^A-Za-z0-9]|$)` but for highlighting we need match positions. Simpler: build regex with lookarounds `(?<![\\p{L}\\p{N}])` — Unicode property escapes supported in modern JS. I'll use `(?<![A-Za-z0-9_])` and `(?![A-Za-z0-9_])`. Actually "right" should not match "rights" — with \b, "right" in "rights" — \bright\b would not match "rights" because \b requires non-word char after "t", but "s" is a word char, so no match. Good. But "rights'" — \b after "right" fails since "s" follows. Fine. Use \b but escape special chars. For words starting/ending with non-word chars (e.g., "article 3"), \b may behave oddly. Use lookarounds with letters/digits: `(?<![\\p{L}\\p{N}])` + escaped + `(?![\\p{L}\\p{N}])`. That's robust.

Parser: tokenize into terms. Grammar: expression := term (OR term)* where implicit AND between adjacent terms. NOT prefix applies to next term. Terms: quoted phrase or word.

Simplest approach: split query into tokens respecting quotes. Then parse: iterate tokens; maintain current group. Actually implement:

tokens = tokenize(query) → list of {type: 'word'|'phrase', value, negated}

Parsing with OR: I'll parse into a list of "clauses" separated by OR, each clause is a list of ANDed terms (each possibly negated). Implicit AND: consecutive terms without OR are ANDed.

Algorithm:
- clauses = [[]]
- pendingNeg = false
- for each token:
  - if token is "OR" (case-insensitive, unquoted): start new clause: clauses.push([])
  - else if token is "NOT": pendingNeg = true
  - else: clauses[last].push({value, neg: pendingNeg}); pendingNeg = false
- Match: some clause where all terms match (term matches if neg ? !match : match). Empty clause (e.g., query "OR" alone or empty) — empty query matches everything? If query empty, match all (within filters). Handle: if no terms at all, match all.

Edge: "NOT" at end with no following term — ignore.

Highlighting: for each matched card, highlight all matched words/phrases. Collect all term values (non-negated? The test says search `"best interests" AND child`: every card highlights both. For NOT terms, highlighting excluded words doesn't make sense — but test 2 only checks no card contains "detention". I'll highlight only positive terms). Build a combined regex of all positive term values (phrases and words), sorted by length desc, with the same boundary rules, global flag, case-insensitive, and wrap matches in <mark>. Must escape HTML in text first, then highlight — careful: escaping changes text (& → &amp;) which could break matching if term contains "&". Better approach: build highlighted HTML by scanning matches on the raw text and escaping segments between matches. Use regex exec on raw text, build output: escape(text.slice(lastIndex, m.index)) + '<mark>' + escape(m[0]) + '</mark>'. That preserves text character-for-character in rendering.

Combined regex: for phrases, boundary rules: phrase "best interests" — match exact sequence of words. Use lookarounds around the whole phrase with escaped inner spaces? "exact sequence of words" — I'll normalize whitespace in phrase to single spaces and match literally (escaped), with boundaries at ends. Inner words: "best interests" should match "best  interests"? Keep simple: escape phrase, replace escaped spaces... I'll just escape the phrase and allow flexible whitespace: split phrase on whitespace, join with `\\s+`. Boundaries: `(?<![\\p{L}\\p{N}])` before first and `(?![\\p{L}\\p{N}])` after last.

For single word: same boundaries.

Combined regex for highlighting: alternation of all positive terms sorted by length descending (so longer phrases match first), flags "giu"? Use "gi" plus unicode lookarounds need "u" flag for \p. Use flags "giu".

Matching per record: test each clause: every term: termRegex.test(text). Use same regexes.

Filters: committee select built from unique committees sorted; year from/to number inputs. Year missing → "year unknown", included when filter open (both empty), excluded when range set. "open" means no from and no to? "included when the year filter is open, excluded by a from–to range" — if either from or to set, apply range; missing year excluded then.

Sorting: newest GC first — sort by year desc (missing year last), then maybe by symbol then paragraph desc? Within same GC, order by paragraph desc or asc? "newest General Comment first" — I'll sort year desc, then paragraph desc (latest paragraphs first) — or asc? Ambiguous; I'll do year desc, then paragraph desc, then symbol. Actually paragraph ascending within a GC seems natural for reading, but "newest first" only specifies GC order. I'll do year desc, then committee, then paragraph desc? Keep simple: year desc, paragraph desc. Hmm, paragraph is int. Fine.

Chart: Chart.js bar chart, labels = committees of matching records (sorted by count desc), data counts. Note "How this is computed". Destroy previous chart on re-render (Chart.getChart or keep reference and destroy).

Count line: "N paragraphs match out of M, filters: committee = X, years = A–B, search = "query"". M = total records (gc.count or records.length).

Copy citation: navigator.clipboard.writeText with fallback (textarea + execCommand) since sandbox may not have clipboard API on non-secure context. Implement fallback. Button text "Copied" for 2s.

Description line: source (gc.source), count, year range: min–max of years present. E.g., "Source: ... · N paragraphs · years YYYY–YYYY". Read from data: WORKSHOP_DATA.gc.source, .count, records. Year range computed from records with year.

Card layout: header row with committee badge, short_title (fallback), year (or "year unknown"), symbol link. Then paragraph text in a <p> with highlights. Copy button.

Also show paragraph number? Citation includes para. Maybe show "para. N" in card header too — helpful. The spec lists card contents: committee, short title, year, symbol linked; then full paragraph; copy button. I can add "para. N" small — that's fine, it's from data.

Empty results: "No paragraph contains these words" + tip.

Let me write the code, keep under 700 lines.

Committee filter: "All" plus every committee in data (unique, sorted alphabetically).

Year inputs: two number inputs with placeholder "from"/"to", change re-runs.

Search re-run on filter change; filters re-run on search.

Chart: only if N > 0? Show chart always with matches; if 0, show empty chart or hide. I'll render chart only when N>0, else show nothing (or a note). Keep chart container; if N==0 destroy chart and clear.

Let me write it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments search</title>
<style>...</style>
</head>
<body>
<header>
  <h1>General Comments search</h1>
  <p id="source-line" class="muted"></p>
</header>
<section class="controls">
  <div class="search-row">
    <input id="q" type="search" ...>
    <button id="search-btn">Search</button>
  </div>
  <p class="help">...</p>
  <div class="filters">
    <label>Committee <select id="committee"></select></label>
    <label>Year from <input id="yfrom" type="number"></label>
    <label>to <input id="yto" type="number"></label>
  </div>
</section>
<p id="count-line"></p>
<div class="chart-wrap"><canvas id="chart"></canvas></div>
<p class="note" id="chart-note">How this is computed: ...</p>
<div id="results"></div>
<script>...</script>
</body>
</html>
```

JS details:

```js
const GC = window.WORKSHOP_DATA.gc;
const records = GC.records || [];
const M = records.length;
```

Tokenizer:

```js
function tokenize(q){
  const tokens=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='"'){
      let j=q.indexOf('"', i+1);
      if(j===-1){ // unterminated quote: treat rest as phrase
        tokens.push({type:'phrase', value:q.slice(i+1)}); i=q.length;
      } else {
        tokens.push({type:'phrase', value:q.slice(i+1,j)}); i=j+1;
      }
    } else {
      let j=i;
      while(j<q.length && !/\s/.test(q[j]) && q[j]!=='"') j++;
      tokens.push({type:'word', value:q.slice(i,j)});
      i=j;
    }
  }
  return tokens;
}
```

Hmm, a word followed directly by quote like `child"phrase"` — edge case, ignore.

Parse:

```js
function parseQuery(q){
  const tokens = tokenize(q);
  const clauses=[[]];
  let neg=false;
  for(const t of tokens){
    const v=t.value;
    const upper=v.toUpperCase();
    if(t.type==='word' && upper==='OR' && clauses[clauses.length-1].length>0){
      clauses.push([]); continue;
    }
    if(t.type==='word' && upper==='NOT'){ neg=true; continue; }
    clauses[clauses.length-1].push({value:v, neg, phrase:t.type==='phrase'});
    neg=false;
  }
  // remove empty clauses? If query is "a OR" trailing OR creates empty clause which matches everything — bad. Filter: keep clause if it has terms; if all clauses empty → match all.
  const nonEmpty = clauses.filter(c=>c.length>0);
  return nonEmpty.length? nonEmpty : null; // null = match all
}
```

Wait: "a OR" — trailing OR: clauses = [[a],[]]. nonEmpty=[[a]] → matches only a. Reasonable.

Term regex:

```js
function esc(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function termRegex(term){
  const parts = term.value.trim().split(/\s+/).filter(Boolean).map(esc);
  if(!parts.length) return null;
  const body = parts.join('\\s+');
  return new RegExp('(?<![\\p{L}\\p{N}])'+body+'(?![\\p{L}\\p{N}])','iu');
}
```

For single word, split gives one part — same. Good, phrases handled uniformly. But phrase "best interests" — inner boundary between words: joined with \s+, fine.

Match:

```js
function matches(rec, clauses){
  if(clauses===null) return true;
  const text = rec.text || '';
  if(!text) return false; // empty text never matches
  return clauses.some(clause => clause.every(t => {
    const r = t.regex || (t.regex=termRegex(t));
    if(!r) return !t.neg; // empty term: ignore
    const m = r.test(text);
    return t.neg ? !m : m;
  }));
}
```

Hmm empty text never matches even with empty query? Spec: "empty `text` → never matches but still counted in M." So even with no query, empty text doesn't match? "never matches" — yes, return false if !text. But then with empty query, N < M possibly. That's per spec. OK.

Wait — but with clauses===null (empty query) and empty text: spec says empty text never matches. So check text first:

```js
if(!rec.text) return false;
if(clauses===null) return true;
```

Highlight regex: combine positive terms:

```js
function highlightRegex(clauses){
  if(!clauses) return null;
  const terms=[];
  for(const cl of clauses) for(const t of cl) if(!t.neg && t.value.trim()) terms.push(t);
  if(!terms.length) return null;
  // sort by value length desc
  terms.sort((a,b)=>b.value.length-a.value.length);
  const alts = terms.map(t=>t.value.trim().split(/\s+/).map(esc).join('\\s+'));
  return new RegExp('(?<![\\p{L}\\p{N}])('+alts.join('|')+')(?![\\p{L}\\p{N}])','giu');
}
```

Careful: alternation with boundaries — the lookbehind applies before group, lookahead after group; with alternation inside group, fine.

Escape HTML:

```js
function escHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function renderHighlighted(text, rx){
  if(!rx) return escHtml(text);
  let out='', last=0, m;
  rx.lastIndex=0;
  while((m=rx.exec(text))){
    out += escHtml(text.slice(last,m.index)) + '<mark>'+escHtml(m[0])+'</mark>';
    last = m.index + m[0].length;
    if(m[0].length===0) rx.lastIndex++; // safety
  }
  out += escHtml(text.slice(last));
  return out;
}
```

Filters:

```js
function applyFilters(){
  const comm = committeeSel.value;
  const yf = yfrom.value.trim(), yt = yto.value.trim();
  const from = yf===''? null : parseInt(yf,10);
  const to = yt===''? null : parseInt(yt,10);
  return records.filter(r=>{
    if(comm!=='All' && r.committee!==comm) return false;
    if(from!==null || to!==null){
      if(typeof r.year!=='number') return false;
      if(from!==null && r.year<from) return false;
      if(to!==null && r.year>to) return false;
    }
    return true;
  });
}
```

Then search on filtered list.

Sort:

```js
results.sort((a,b)=>{
  const ya = typeof a.year==='number'?a.year:-Infinity;
  const yb = ...;
  if(yb!==ya) return yb-ya;
  const pa = a.paragraph||0, pb=b.paragraph||0;
  if(pb!==pa) return pb-pa;
  return String(a.symbol||'').localeCompare(String(b.symbol||''));
});
```

Chart: aggregate counts by committee over results.

```js
let chart=null;
function renderChart(counts){
  const ctx=document.getElementById('chart');
  if(chart){chart.destroy(); chart=null;}
  if(!counts.length){ /* clear canvas */ const c=ctx.getContext('2d'); c.clearRect(0,0,ctx.width,ctx.height); return; }
  chart = new Chart(ctx, {type:'bar', data:{labels:counts.map(c=>c.name), datasets:[{label:'Matching paragraphs', data:counts.map(c=>c.n), backgroundColor:'#1f6fb2'}]}, options:{...}});
}
```

Chart options: responsive, maintainAspectRatio false with fixed height container, scales y beginAtZero, ticks precision 0.

Count line: `N paragraphs match out of M · filters: committee: All · years: all · search: "…"`. Build string.

Card:

```js
function card(r, rx){
  const title = r.short_title || r.title || r.symbol || 'Untitled';
  const yearTxt = typeof r.year==='number' ? r.year : 'year unknown';
  const sym = r.symbol ? (r.doc_url ? `<a href="${escAttr(r.doc_url)}" target="_blank" rel="noopener">${escHtml(r.symbol)}</a>` : escHtml(r.symbol)) : '';
  const para = r.paragraph!=null ? `para. ${r.paragraph}` : '';
  ...
}
```

escAttr: escape quotes in URL: replace " with %22 or &quot;. Use escHtml for attribute too (escapes & < > but not quotes) — add quote escaping.

Copy citation: `r.symbol + ', para. ' + r.paragraph`. If symbol missing? Spec says citation is symbol + para; assume present. If paragraph missing, still "symbol, para. undefined"? Guard: if paragraph==null just symbol. Keep simple: build parts.

Clipboard:

```js
async function copyText(t){
  try{ await navigator.clipboard.writeText(t); return true; }
  catch(e){
    const ta=document.createElement('textarea'); ta.value=t; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    let ok=false; try{ ok=document.execCommand('copy'); }catch(_){}
    ta.remove(); return ok;
  }
}
```

Button handler: copy, set text "Copied", disabled? just text, setTimeout revert 2000.

Source line: `${GC.source} · ${M} paragraphs · years ${min}–${max}` — compute min/max over records with numeric year; if none, "years unknown". GC.title maybe: "General Comments, paragraph by paragraph". Use GC.title as source? Spec: "source, number of paragraphs, year range, all read from the data." Use GC.source (a string) — sample shows gc has `title, source, count`. I'll show: `${GC.source||GC.title} — ${M} paragraphs (of ${GC.count} in source) — years X–Y`. Keep simple: `Source: ${GC.source} · ${M} paragraphs · years ${min}–${max}`.

Committee select options: unique committees sorted; "All" default.

Events: search button click, Enter on input (form submit or keydown), select change, year inputs 'input' change → run().

run(): read query, parse, filter, match, sort, render count line, chart, cards.

Initial run on load with empty query (shows all). That's fine — no studio.ask.

Design: light background #f7f9fb, white cards, accent #1f6fb2, base font 16px, system stack, max-width 900px container.

Help line: `Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: "best interests" AND child`.

Empty state: div with "No paragraph contains these words." + tip "Try OR between words, or fewer words."

Chart note: "How this is computed: each matching paragraph is counted once, in its committee; the bars add up to the N shown above."

Count line format: `N paragraphs match out of M · filters: committee = All, years = all, search = "torture NOT detention"`. If search empty: search = (none).

Let me also handle paragraph display: show "para. N" chip in card header.

Now write the full file. Keep under 700 lines — easy.

One more detail: "Changing a filter re-runs the search" — yes.

Year filter "open" = both empty → include year-unknown records. Done.

Chart when N==0: show message instead? I'll hide chart area and show nothing; count line says 0. Maybe show "No bars — no matches." Keep simple: if no counts, destroy chart and show a small note. I'll just clear canvas and set a placeholder text in note? Simpler: if counts empty, set chart-note text to "No matches, so no bars." Fine.

Write code now.

Also Enter in year inputs triggers search — they're inputs; 'change' event fires on blur/Enter. Use 'input' event for immediacy? 'change' is fine; add keydown Enter → run. I'll listen to 'input' on year fields (fires per keystroke) — fine.

Let me write final HTML.

Card HTML structure:

```html
<article class="card">
  <div class="card-head">
    <span class="badge">CRC</span>
    <span class="gc-title">GC14: ...</span>
    <span class="year">2003</span>
    <span class="para">para. 6</span>
    <span class="sym"><a ...>CRC/C/GC/14</a></span>
    <button class="copy">Copy citation</button>
  </div>
  <p class="text">...highlighted...</p>
</article>
```

Copy button in head right-aligned. Use flex wrap.

Citation string: `${symbol}, para. ${paragraph}` — if paragraph null, just symbol.

OK, write it.