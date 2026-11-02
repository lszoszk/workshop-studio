Let me build the app. Single HTML file, offline, Chart.js preloaded. Data: WORKSHOP_DATA.gc with records.

Plan:
- Header: title "General Comments search", one-line description: source, count, year range.
- Search box + button + help line.
- Filters: committee select (all committees + All), year from/to inputs.
- Count line.
- Bar chart: matching paragraphs per committee (Chart.js).
- Results sorted newest GC first — sort by year desc, then... "newest General Comment first" — sort by year desc, then maybe symbol. I'll sort by year desc, then committee, then paragraph desc? Keep simple: year desc, then paragraph desc within? Actually "newest General Comment first" — sort by year descending; tie-break by symbol then paragraph. I'll do year desc, then symbol asc, then paragraph desc maybe. Keep simple: year desc, then paragraph desc.

Search parser: tokens. Support AND (default), OR, NOT, quoted phrases. No grouping. Parse: split into tokens respecting quotes. Grammar: expression = term (OR term)* where term = [NOT] atom, and atoms separated by spaces are ANDed. So precedence: NOT > AND > OR. Implement: tokenize into list of {type: 'word'|'phrase', neg: bool}. Split top-level by OR (case-insensitive standalone "OR"). Each OR-group: split into AND terms; each term may start with NOT. A record matches if any OR-group matches; a group matches if all its terms match (term matches if atom present and not negated... careful: NOT term matches if atom absent).

Tokenization: scan string; quoted phrases with double quotes; words are sequences of non-space non-quote chars. "OR" as standalone word (case-insensitive) is operator. "AND" standalone — treat as separator (AND is default anyway). "NOT" prefix.

Matching: word match = whole word, case-insensitive: build regex `\b` + escaped + `\b` — but \b with words containing non-word chars could be tricky; use lookarounds: `(?<![A-Za-z0-9_])word(?![A-Za-z0-9_])` case-insensitive. For phrases: exact sequence of words — match the phrase as literal sequence of words separated by whitespace? "exact sequence of words" — I'll match phrase with flexible whitespace: split phrase into words, join with `\s+`, with word boundaries. Actually "exact phrase" — quotes find an exact phrase. I'll do: escape each word, join with `\s+`, wrap with boundaries. That handles "best interests" matching "best interests" but not "bestinterests". Good.

Highlighting: for each matched card, highlight all matched words (from all positive terms across matching OR groups? Simpler: highlight all positive atoms in the query). Build a combined regex of all positive atoms (words and phrases), wrap matches in <mark>. Must escape HTML first, then apply highlight on escaped text? Careful: escaping changes text (& → &amp;). Better: highlight on raw text using regex with capture, then escape each piece. Implement: build regex global with alternation of atoms sorted by length desc; iterate matches on raw text, escape segments, wrap matched segment in <mark>.

Empty text: never matches but counted in M. So M = total records count (all records), filters applied first then search — count line: "N paragraphs match out of M" where M is... "out of M" — M is total paragraphs in data? "empty text → never matches but still counted in M". Filters applied first, then search. Hmm, M could be total records overall or after filters. The count line says "N paragraphs match out of M, filters: …". I'll make M = total records in dataset (count field), and mention filters in the line. Actually "filters: …" part lists active filters. Let me make M = total paragraphs in the data (records.length), N = matches after filters+search. The chart bars add up to N. That's consistent.

Hmm, but maybe M should be after filters? "N paragraphs match out of M, filters: …" — ambiguous. The spec: "Filters are applied first, then the search. N, the chart bars and the cards come from the same list". M is likely the full dataset count. I'll use M = records.length (total), and the filters part shows active filters. Safe.

Year filter: from–to inputs. No year → "year unknown", included when filter open (both empty), excluded when range set. Committee filter: select with all committees + "All".

Committee list: unique committees sorted. Years: min/max from data for the description line.

Chart: bar chart of matching paragraphs per committee. Use Chart.js. Update on each search. If no matches, show empty chart or hide with message. "How this is computed" note.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Button text "Copied" for 2s. Citation: `${symbol}, para. ${paragraph}`. If paragraph missing? paragraph is int per spec; handle missing → just symbol? Spec says citation is symbol + ", para. " + paragraph. If paragraph null, maybe just symbol. I'll handle: if paragraph != null include para, else symbol only.

Sorting: newest GC first: year desc (nulls last), then... within same year, maybe by symbol then paragraph. I'll do year desc, then committee asc, then paragraph desc? "newest General Comment first" — sort by year desc; tie: symbol asc, paragraph asc. Fine.

Card layout: header line with committee badge, short_title (or title or symbol), year (or "year unknown"), symbol link (doc_url, new tab, target _blank rel noopener). If no doc_url, plain text symbol. Then paragraph text with highlights, prefixed with "para. N"? The text field includes the paragraph number at start sometimes ("54. The Committee..."). Show full text character for character. Maybe show "Para. N" label. I'll show a small "para. N" label plus full text.

Also doc link: symbol linked to doc_url.

Design: clean, accent #1f6fb2, system fonts, base 16px, max-width container ~900px.

Chart.js: window.Chart. Bar chart with labels committees, data counts. Destroy previous chart instance on update.

Let me write the code.

Tokenizer:

```js
function tokenize(q){
  const tokens=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='"'){
      const end=q.indexOf('"', i+1);
      if(end===-1){ // unterminated quote: treat rest as phrase
        tokens.push({type:'phrase', value:q.slice(i+1)}); i=q.length;
      } else {
        tokens.push({type:'phrase', value:q.slice(i+1,end)}); i=end+1;
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

Parse into OR groups of AND terms:

```js
function parseQuery(q){
  const tokens=tokenize(q);
  const groups=[]; let cur=[]; let pendingNot=false;
  for(const t of tokens){
    const v=t.value;
    const up=v.toUpperCase();
    if(t.type==='word' && up==='OR'){ if(cur.length) groups.push(cur); cur=[]; pendingNot=false; continue; }
    if(t.type==='word' && up==='AND'){ continue; }
    if(t.type==='word' && up==='NOT'){ pendingNot=true; continue; }
    cur.push({atom:t, neg:pendingNot}); pendingNot=false;
  }
  if(cur.length) groups.push(cur);
  return groups;
}
```

Edge: empty query → groups empty → match all (after filters). Good.

Atom regex:

```js
function atomRegex(atom){
  const words=atom.value.trim().split(/\s+/).filter(Boolean).map(escapeRe);
  const body=words.join('\\s+');
  return new RegExp('(?<![A-Za-z0-9_])'+body+'(?![A-Za-z0-9_])','i');
}
```

For single word this gives whole-word matching. Good.

Match:

```js
function matches(text, groups){
  if(!text) return false;
  return groups.some(g=>g.every(t=>{
    const r=atomRegex(t.atom);
    const found=r.test(text);
    return t.neg ? !found : found;
  }));
}
```

Highlight: collect positive atoms from all groups (dedupe by value+type). Build combined regex alternation sorted by word-count/length desc:

```js
function highlightRegex(atoms){
  const parts=atoms.map(a=>a.value.trim().split(/\s+/).map(escapeRe).join('\\s+')).sort((a,b)=>b.length-a.length);
  return new RegExp('(?<![A-Za-z0-9_])('+parts.join('|')+')(?![A-Za-z0-9_])','gi');
}
```

Render: escape text, but highlight must wrap matched words without altering text. Approach: run regex on raw text with exec loop, build HTML: escape(text.slice(last, m.index)) + '<mark>'+escape(m[0])+'</mark>'.

Note lookbehind support: modern browsers fine.

Filters: committee select; year from/to number inputs. On change re-run.

Count line: `N paragraphs match out of M` + filters description: e.g. "filters: committee = CRC; year 2000–2010" or "filters: none".

Chart: counts per committee among matches. Bar chart. If N=0, show chart with empty? Show message "No paragraph contains these words" plus tip. Chart can show empty bars; I'll still render chart (all zero) or hide. I'll render chart only if N>0? Spec says small bar chart with note; if nothing matches show the no-match message. I'll keep chart area and update with zeros — simpler to always update chart; when N=0 show message in results area. Chart with all-zero is fine but maybe hide. I'll update chart always; if no committees in matches, labels empty. Fine.

Description line: source (WORKSHOP_DATA.gc.source), count, year range: `Source: ... · N paragraphs · years X–Y`. Compute min/max of year where present.

Copy: 

```js
async function copyText(t, btn){
  try{ await navigator.clipboard.writeText(t); }
  catch(e){
    const ta=document.createElement('textarea'); ta.value=t; document.body.appendChild(ta); ta.select();
    try{document.execCommand('copy');}catch(_){}
    ta.remove();
  }
  btn.textContent='Copied'; setTimeout(()=>btn.textContent='Copy citation',2000);
}
```

Clipboard may fail in sandbox without permission — fallback covers.

Sorting: 

```js
results.sort((a,b)=>{
  const ya=a.year??-Infinity, yb=b.year??-Infinity;
  if(yb!==ya) return yb-ya;
  const sa=(a.symbol||''), sb=(b.symbol||'');
  if(sa!==sb) return sa.localeCompare(sb);
  return (b.paragraph??0)-(a.paragraph??0);
});
```

Hmm paragraph desc within same symbol — newest first; paragraph order within a GC: maybe ascending is more natural, but "newest General Comment first" only specifies GC order. I'll do paragraph ascending actually... doesn't matter. I'll do paragraph asc for readability. Actually keep desc? Choose asc.

Wait — year unknown sorts last with -Infinity. Good.

Committee filter values: unique sorted committees. Year inputs: placeholder "from"/"to", type number.

Year filter logic: if from or to set (non-empty), record must have year and year>=from (if from set) and year<=to (if to set). If both empty → all included (including unknown year).

Render cards: build with DOM or innerHTML with escaping. I'll build via createElement/innerHTML carefully. Use a helper esc().

Card structure:

```
<article class="card">
  <div class="card-head">
    <span class="badge">CRC</span>
    <span class="gc-title">GC14: ...</span>
    <span class="year">2000</span>
    <a class="symbol" href=doc_url target=_blank>CRC/C/GC/14</a>
    <button>Copy citation</button>
  </div>
  <div class="para"><span class="paranum">para. 6</span> <span class="ptext">highlighted text</span></div>
</article>
```

Copy button in head or after text — put in head right side.

Chart config: 

```js
chart = new Chart(ctx, {type:'bar', data:{labels, datasets:[{label:'Matching paragraphs', data, backgroundColor:'#1f6fb2'}]}, options:{...}});
```

Update: chart.data.labels=...; chart.data.datasets[0].data=...; chart.update(). Create once, destroy on rebuild? Just create once and update.

Scales: beginAtZero, ticks precision 0.

Line count: keep under 700. Fine.

Help line: `Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: "best interests" AND child`.

Also note "How this is computed" near chart: "Bars count the paragraphs that match the current search and filters, grouped by committee; the bar heights add up to N."

Also maybe a note near count line. Spec: "a short 'How this is computed' note near every chart or number." Add small note under count line: "N counts paragraphs in WORKSHOP_DATA.gc whose text matches the query after the committee and year filters; M is all paragraphs in the dataset."

Search on load? Run once on load with empty query to show all? Probably yes — show all paragraphs initially. That could be many cards (gc count maybe ~1000+). Rendering all could be heavy but fine. Maybe limit? Spec doesn't say limit. I'll render all matches; if large, it's okay. Could cap display at e.g. 200 with note? Spec says cards come from same list as N. Don't cap. Fine.

Enter key: form submit.

Let me also handle `title` fallback: short_title || title || symbol.

Write the HTML now.

Also description: `const d=WORKSHOP_DATA.gc; const years=d.records.map(r=>r.year).filter(y=>typeof y==='number');` range min–max. Source: d.source, count: d.count or records.length. Use records.length for M to be safe, but display count from d.count? Use records.length for computations; description uses d.count ?? records.length. I'll use records.length consistently and mention source.

Committee select: build options from unique committees sorted alphabetically.

Edge: committee missing → "unknown"? Group under "(unknown)". Handle: c = r.committee || 'Unknown'.

Now write code.

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
  <p class="desc" id="desc"></p>
</header>
<main>
  <form id="searchForm">
    <input id="q" type="search" ...>
    <button type="submit">Search</button>
  </form>
  <p class="help">...</p>
  <div class="filters">
    <label>Committee <select id="committee"></select></label>
    <label>Year from <input id="yearFrom" type="number"></label>
    <label>to <input id="yearTo" type="number"></label>
  </div>
  <p id="countLine"></p>
  <p class="note">How this is computed: ...</p>
  <div class="chartWrap"><canvas id="chart"></canvas></div>
  <p class="note">How this is computed: bars count ...</p>
  <section id="results"></section>
</main>
<script>...</script>
</body>
</html>
```

CSS: body font stack, background #f5f7fa, container max-width 960px, cards white with border, accent #1f6fb2, mark background #ffe08a maybe. Base font 16px.

JS details:

```js
const D = window.WORKSHOP_DATA.gc;
const records = D.records || [];
const M = records.length;
```

desc: `${D.source} · ${M} paragraphs · years ${min}–${max}` (if years exist; else "years unknown").

run():

```js
function currentFilters(){
  return {committee: sel.value, from: yearFrom.value, to: yearTo.value};
}
function applyFilters(){
  const {committee, from, to} = ...;
  const f = from===''?null:parseInt(from), t = to===''?null:parseInt(to);
  return records.filter(r=>{
    if(committee!=='All' && (r.committee||'Unknown')!==committee) return false;
    if(f!==null || t!==null){
      if(typeof r.year!=='number') return false;
      if(f!==null && r.year<f) return false;
      if(t!==null && r.year>t) return false;
    }
    return true;
  });
}
```

Then groups=parseQuery(q); matches = filtered.filter(r=>matches(r.text, groups)); sort; render.

Count line: `${N} paragraph${s} match out of ${M}` + filters text: build parts: committee!=='All' → `committee: ${committee}`; from/to → `year ${from||'…'}–${to||'…'}`; if none → 'no filters'. Format: `N paragraphs match out of M · filters: committee = CRC, year 2000–2010` or `filters: none (search only)`.

Chart data: count per committee of matches, sorted desc by count then alpha. Labels committees, data counts.

Render results: if N===0 → message div: "No paragraph contains these words." + tip "Try OR instead of AND, or fewer words — e.g. \"best interests\" OR child." Spec tip: "try OR or fewer words".

Highlight atoms: positive atoms from groups: groups.flat().filter(t=>!t.neg).map(t=>t.atom). Dedupe by type+value lowercase. If groups empty (empty query) → no highlight.

Card HTML building with escaping:

```js
function esc(s){return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function highlight(text, atoms){
  if(!atoms.length || !text) return esc(text);
  const parts = atoms.map(a=>a.value.trim().split(/\s+/).map(escapeRe).join('\\s+')).sort((a,b)=>b.length-a.length);
  const re = new RegExp('(?<![A-Za-z0-9_])('+parts.join('|')+')(?![A-Za-z0-9_])','gi');
  let out='', last=0, m;
  while((m=re.exec(text))){
    out += esc(text.slice(last,m.index)) + '<mark>'+esc(m[0])+'</mark>';
    last = m.index + m[0].length;
    if(m[0].length===0) re.lastIndex++;
  }
  out += esc(text.slice(last));
  return out;
}
```

escapeRe: `s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')`.

Card:

```js
const title = r.short_title || r.title || r.symbol || 'Untitled';
const yearTxt = (typeof r.year==='number') ? r.year : 'year unknown';
const sym = r.symbol || '(no symbol)';
const link = r.doc_url ? `<a href="${esc(r.doc_url)}" target="_blank" rel="noopener noreferrer">${esc(sym)}</a>` : esc(sym);
const cite = r.symbol ? (r.paragraph!=null ? `${r.symbol}, para. ${r.paragraph}` : r.symbol) : '';
```

Copy button disabled if no cite? If no symbol, citation can't be formed; hide button. Fine.

Para label: `para. ${r.paragraph}` if present.

Chart creation:

```js
let chart=null;
function updateChart(counts){
  const labels=counts.map(c=>c.k), data=counts.map(c=>c.n);
  if(!chart){
    chart=new Chart(document.getElementById('chart'),{type:'bar',data:{labels,datasets:[{label:'Matching paragraphs',data,backgroundColor:'#1f6fb2',borderRadius:3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{precision:0,stepSize:1},title:{display:true,text:'Paragraphs'}},x:{ticks:{autoSkip:false}}}}});
  } else {
    chart.data.labels=labels; chart.data.datasets[0].data=data; chart.update();
  }
}
```

Chart wrap height ~260px.

Events: form submit → run; select change → run; year inputs 'input' → run.

Initial run on load with empty query.

Also note near count line: "How this is computed: filters are applied first, then the search; N, the bars and the cards below all come from the same list of matching paragraphs. M is every paragraph in the dataset (empty texts are counted in M but never match)."

Now write full file. Keep it tidy.

One more: search input width, layout responsive. Filters row flex wrap.

Let me write it.