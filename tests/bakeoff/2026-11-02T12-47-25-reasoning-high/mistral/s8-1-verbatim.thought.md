The user wants a single HTML app. Let me build it carefully.

Requirements:
- Title "General Comments search", one line: source, number of paragraphs, year range from data.
- Search box + button, Enter searches, help line with AND/OR/NOT/quotes syntax.
- Filters: committee dropdown (all committees + "All"), year from–to. Changing filter re-runs search.
- Count line: "N paragraphs match out of M, filters: …".
- Bar chart: matching paragraphs per committee, Chart.js, "How this is computed" note.
- Results sorted newest GC first (by year desc, then... maybe symbol). Each card: committee, short_title (fallback title, else symbol), year, symbol linked to doc_url new tab; full paragraph with highlighted search words; "Copy citation" button copying "symbol, para. paragraph", shows "Copied" 2s.
- Empty: "No paragraph contains these words" + tip.
- Search semantics: case-insensitive, whole word for plain words, exact phrase for quotes, AND by default, OR, NOT. Filters first, then search. text shown char-for-char; highlight wraps matched words only.
- Missing values handling: no short_title → title, else symbol; no year → "year unknown", included when year filter open (no range), excluded by range; no doc_url → unlinked symbol; empty text → never matches but counted in M.

Search parser: tokens. Grammar: terms separated by spaces; OR joins alternatives; NOT excludes. No brackets. So parse: split into tokens respecting quotes. Then build a boolean expression: sequence of terms, where "OR" between terms means union, "NOT x" means exclusion, default AND.

Simple approach: parse tokens into a list of clauses. A clause is {neg: bool, phrase: string}. Operators: implicit AND, explicit OR. Without brackets, precedence: NOT binds to next term; OR... typical simple approach: evaluate left to right? Better: standard precedence — NOT highest, then AND, then OR. But without brackets, "a OR b AND c" ambiguous. Keep simple: treat OR as joining alternatives at top level: split the token stream on OR tokens into groups; each group is AND of terms (each possibly NOT). That's a reasonable simple interpretation: "a OR b c" = a OR (b AND c). Actually splitting on OR: groups of ANDed terms. That matches "OR joins alternatives".

Tokenize: scan string, quoted phrases with "..." become phrase tokens; words are sequences of non-space, non-quote chars. "OR" and "NOT" as standalone words (case-insensitive? The help says write OR / NOT — I'll accept case-insensitive "or"/"not"? Safer: uppercase only? The example uses uppercase. I'll accept case-insensitive to be friendly, but a word "or" inside text search... hmm, if someone searches "or" they'd get operator. Accept case-insensitive OR/NOT as operators — simple. Actually risk: searching for the word "or" — unlikely in this context. I'll treat exact "OR"/"NOT" case-insensitive as operators.)

Matching: for a plain word w: whole-word match, case-insensitive: regex with boundaries. Word chars: use \b? "right" should not match "rights". Use regex `(?<![A-Za-z0-9_])word(?![A-Za-z0-9_])` with escaped word, case-insensitive. Unicode? Use `u` flag and lookarounds with letters... keep simple with [A-Za-z0-9] plus maybe accented letters. Use `(?<![\p{L}\p{N}])...` with u flag — supported in modern browsers. I'll use that.

Quoted phrase: exact sequence of words — match the phrase as whole words too? "quotes find an exact phrase" — exact sequence of words. I'll match phrase with word boundaries as well, case-insensitive, allowing whitespace flexibility? "exact phrase" — I'll normalize whitespace in both text and phrase (collapse multiple spaces) and match with boundaries. Simpler: build regex from phrase words joined by `\s+`, with boundaries, case-insensitive.

Highlighting: need to wrap matched words in the text without altering characters. Approach: for each result, compute match ranges by running all positive terms' regexes over the original text (using exec with global flag), collect ranges, merge overlapping, then build HTML by escaping text segments and wrapping ranges in <mark>. NOT terms only exclude, don't highlight. OR groups: positive terms across all OR groups highlight (test 1: `"best interests" AND child` highlights both). Yes — highlight all positive terms.

Careful: highlight ranges from different terms may overlap; merge. Also ensure ranges don't overlap partially causing broken tags — merge overlapping/adjacent ranges first.

Sorting: "newest General Comment first" — sort by year desc; tie-break maybe by symbol or paragraph? Sort by year desc, then committee, then paragraph desc? Keep: year desc, then symbol asc, then paragraph desc. Fine.

Chart: Chart.js bar chart, labels = committees present in filtered+searched results, data = counts. Update on each search. Note "How this is computed": "Bars count the matching paragraphs per committee in the current result list; they add up to N."

Count line: "N paragraphs match out of M, filters: committee=All, years=all" etc. Describe filters: committee name or All; year range "YYYY–YYYY" or "all years".

Year filter: two number inputs from–to. "included when the year filter is open" — open means empty from and to. If from set, records with year >= from; if to set, year <= to; records with missing year excluded when any range set. Empty from/to = open.

Committee filter: unique committees sorted alphabetically.

Header line: source (WORKSHOP_DATA.gc.source), count, year range: min and max of years present (ignore missing). E.g. "Source: ... · N paragraphs · years YYYY–YYYY". Read from data: gc.title? The spec says "source, number of paragraphs, year range, all read from the data". Use gc.source for source, gc.count or records.length for number, min/max year.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Button text "Copy citation" → "Copied" for 2s.

Symbol link: if doc_url present, <a href target=_blank rel="noopener">symbol</a>, else plain text.

Card layout: header row with committee badge, short_title (fallback), year ("year unknown" if missing), symbol link. Then paragraph text with highlight. Then copy button. Also maybe show paragraph number? The citation includes para; card could show "para. N" too — spec says card shows committee, short title, year, symbol; then paragraph. I'll include "para. N" near symbol for clarity — that's fine, it's from data. Actually keep to spec but adding para label is helpful and not invented. I'll show "para. N" next to symbol.

Empty text: never matches but counted in M — since search requires matching text, empty text won't match any positive term. But what if search box is empty? Then all records match (empty query matches everything). Spec doesn't say; empty search → show all (N=M). That's natural.

If query has only NOT terms? e.g. "NOT detention" — groups: one group with only a negative term. Then positive set empty → matches everything not containing detention. Handle: if no positive terms in a group, group matches all (then apply negatives). Implement: group matches if (no positive terms OR any positive matches) AND no negative matches.

Wait — semantics with OR split: overall match = OR over groups of (AND of positives within group, minus negatives). Negatives within a group apply to that group. Hmm, "torture NOT detention": one group, positive torture, negative detention → matches texts with torture and without detention. Good.

Edge: "a NOT b OR c" → groups: [a, NOT b], [c]. Fine.

M = total records count (all records, regardless of filters? "N paragraphs match out of M" — M is total paragraphs in data, I think: "empty text → never matches but still counted in M". M = records.length. Filters described separately in the count line. Yes M = total.

Chart with zero results: show empty chart or hide with message. Chart.js with empty data fine; maybe show "no data" — just render empty chart.

Design: clean, accent #1f6fb2, light background, system fonts, base 16px, max-width container ~900px, no horizontal scroll.

Highlight mark styling: background light yellow or accent tint. Use <mark> with custom style.

Escape HTML properly when building highlighted text.

Let me write the tokenizer:

```js
function tokenize(q){
  const tokens=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='"'){
      const end=q.indexOf('"',i+1);
      if(end===-1){ // unterminated quote: treat rest as phrase
        const phrase=q.slice(i+1).trim();
        if(phrase) tokens.push({type:'phrase',value:phrase});
        break;
      }
      const phrase=q.slice(i+1,end).trim();
      if(phrase) tokens.push({type:'phrase',value:phrase});
      i=end+1;
    } else {
      let j=i;
      while(j<q.length && !/\s/.test(q[j]) && q[j]!=='"') j++;
      tokens.push({type:'word',value:q.slice(i,j)});
      i=j;
    }
  }
  return tokens;
}
```

Parse into groups:

```js
function parseQuery(q){
  const tokens=tokenize(q);
  const groups=[[]]; // each group: {pos:[], neg:[]}
  let neg=false;
  for(const t of tokens){
    const v=t.value;
    const up=v.toUpperCase();
    if(t.type==='word' && up==='OR'){ groups.push([]); neg=false; continue; }
    if(t.type==='word' && up==='NOT'){ neg=true; continue; }
    groups[groups.length-1].push({neg, value:v, phrase:t.type==='phrase'});
    neg=false;
  }
  return groups.map(g=>({pos:g.filter(x=>!x.neg), neg:g.filter(x=>x.neg)}));
}
```

Regex builder:

```js
function termRegex(term){
  const words = term.phrase ? term.value.split(/\s+/) : [term.value];
  const esc = words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('\\s+');
  return new RegExp('(?<![\\p{L}\\p{N}_])'+esc+'(?![\\p{L}\\p{N}_])','giu');
}
```

Hmm, for a single word, joining gives just the word. Good. Whole word: "right" doesn't match "rights" — with lookahead (?![\p{L}\p{N}_]) after "right", "rights" has 's' → no match. Good. Hyphenated? "human-rights": "rights" preceded by "-" which is not letter → matches. Fine.

Match test:

```js
function matches(text, groups){
  if(!text) return false;
  return groups.some(g=>{
    const posOk = g.pos.length===0 || g.pos.some(t=>termRegex(t).test(text));
    if(!posOk) return false;
    return !g.neg.some(t=>termRegex(t).test(text));
  });
}
```

Note: regex with 'g' flag and .test — lastIndex statefulness! Using a fresh regex each call avoids the issue since termRegex creates new each time. But in highlight I'll create regexes once per query and use exec loops — need to reset lastIndex or create per use. I'll create fresh regex per test call (fine for perf at this scale) or manage lastIndex. For highlight, collect ranges:

```js
function highlightRanges(text, posTerms){
  const ranges=[];
  for(const t of posTerms){
    const re=termRegex(t);
    let m;
    while((m=re.exec(text))!==null){
      ranges.push([m.index, m.index+m[0].length]);
      if(m[0].length===0) re.lastIndex++;
    }
  }
  ranges.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const merged=[];
  for(const r of ranges){
    const last=merged[merged.length-1];
    if(last && r[0]<=last[1]) last[1]=Math.max(last[1],r[1]);
    else merged.push([r[0],r[1]]);
  }
  return merged;
}
```

Build HTML:

```js
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function renderHighlighted(text, ranges){
  let out='', pos=0;
  for(const [a,b] of ranges){
    out+=esc(text.slice(pos,a))+'<mark>'+esc(text.slice(a,b))+'</mark>';
    pos=b;
  }
  out+=esc(text.slice(pos));
  return out;
}
```

Empty query: groups = [[]] → pos empty → matches all (text non-empty). Empty text never matches because matches() returns false for empty text — but with empty query, should empty-text records match? "empty text → never matches but still counted in M". So even with empty query, empty text never matches. My matches() returns false for falsy text — good, but careful: text could be "" → false. Good.

Wait: with empty query and non-empty text, groups=[{pos:[],neg:[]}] → posOk true, neg none → true. Good.

Filters:

```js
function applyFilters(){
  const comm = commSel.value;
  const yFrom = yearFrom.value.trim(), yTo = yearTo.value.trim();
  return DATA.records.filter(r=>{
    if(comm!=='All' && r.committee!==comm) return false;
    if(yFrom!=='' || yTo!==''){
      const y = r.year;
      if(typeof y!=='number') return false;
      if(yFrom!=='' && y < +yFrom) return false;
      if(yTo!=='' && y > +yTo) return false;
    }
    return true;
  });
}
```

Then search over filtered list.

Count line: `N paragraphs match out of M, filters: committee: All · years: all` or `committee: CRC · years: 2003–2011`. If from only: "from 2003"; to only: "to 2011".

Chart: aggregate counts by committee over results. Sort bars descending count, then committee. Chart.js:

```js
chart = new Chart(ctx, {type:'bar', data:{labels, datasets:[{label:'Matching paragraphs', data, backgroundColor:'#1f6fb2'}]}, options:{...}});
```

Update via chart.data... chart.update(). Destroy/recreate simpler: keep reference, update data and call update.

Sorting results: year desc (missing year → treat as -Infinity, goes last), then symbol.localeCompare, then paragraph desc (paragraph is int). 

Card HTML:

```
<article class="card">
  <div class="card-head">
    <span class="badge">CRC</span>
    <span class="gc-title">GC14: ...</span>
    <span class="year">2000</span>
    <a class="symbol" href=... target="_blank" rel="noopener">CRC/C/GC/14</a>
    <span class="para">para. 6</span>
  </div>
  <p class="text">...highlighted...</p>
  <button class="copy">Copy citation</button>
</article>
```

Copy: `symbol + ', para. ' + paragraph`. paragraph is int per spec. If paragraph missing? Spec says fields used include paragraph; assume present. But guard: if paragraph == null, citation just symbol? Spec: "The citation is symbol + ', para. ' + paragraph, nothing invented." I'll do: if paragraph is null/undefined → just symbol. Fine.

Clipboard: navigator.clipboard may fail in sandbox (non-secure context). Fallback with textarea + execCommand('copy'). Implement both.

Button "Copied" for 2 seconds: setTimeout revert.

Header line: `Source: ${gc.source} · ${records.length} paragraphs · ${minYear}–${maxYear}` — read from data. gc.source exists per description ("{title, source, count, records}"). Year range: compute min/max over records with numeric year; if none, "years unknown".

Help line: `Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: "best interests" AND child`.

Committee options: unique sorted committees + All. Build from data.

Year inputs: type="number", placeholders "from" / "to". Changing re-runs search: 'input' event on both, 'change' on select.

Search triggers: button click, Enter in search input (form submit — wrap in form with onsubmit preventDefault).

Chart note: "How this is computed: each bar counts the paragraphs in the current result list (after filters and search) for that committee; the bars add up to N."

Also maybe a note near count line? The count line itself shows filters. Add "How this is computed" near chart only, per spec. Maybe also small note under results? Spec says count line includes filters. OK.

Layout: header, controls card (search + help, filters row), count line, chart section, results. Keep under 700 lines. No external resources. Chart.js preloaded.

Empty results: show message div "No paragraph contains these words" + tip "Try OR instead of AND, or fewer words." Also chart shows empty.

Let me also handle: search input value read at search time; filters re-run search using current query.

Structure code:

```js
const DATA = window.WORKSHOP_DATA.gc;
const records = DATA.records || [];
```

Render functions: runSearch() reads query, filters, computes results, updates count, chart, results list.

Highlight terms: positive terms from all groups (flattened pos). If query empty → no highlight.

Let me write the full HTML now.

Also title element: "General Comments search".

CSS: body background #f5f7fa, container max-width 960px, cards white with border, accent #1f6fb2. mark background #ffe9a8 or rgba accent. Use #fff3c4? I'll use background:#ffe08a; padding 0 1px; border-radius 2px.

Chart container height ~260px, maintainAspectRatio false.

Buttons: accent background, white text.

Copy fallback:

```js
function copyText(t){
  if(navigator.clipboard && navigator.clipboard.writeText){
    return navigator.clipboard.writeText(t).catch(()=>legacyCopy(t));
  }
  return Promise.resolve(legacyCopy(t));
}
function legacyCopy(t){
  const ta=document.createElement('textarea');
  ta.value=t; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try{document.execCommand('copy');}catch(e){}
  document.body.removeChild(ta);
}
```

Copy button handler: event delegation on results container.

Now write everything. Also ensure no horizontal scroll: chart canvas width 100%.

Committee badge list: `const committees=[...new Set(records.map(r=>r.committee).filter(Boolean))].sort();` If committee missing? Show "committee unknown"? Spec doesn't mention missing committee; guard: display r.committee || 'unknown'. For filter, include only truthy; records with falsy committee only match "All". Fine.

Year display: `r.year != null ? r.year : 'year unknown'`.

short_title fallback: `r.short_title || r.title || r.symbol`.

Symbol link: `r.doc_url ? <a ...> : <span>`.

Count line format: `${n} paragraph${n===1?'':'s'} match out of ${m}, filters: committee ${comm==='All'?'All':comm}, years ${yearDesc}` where yearDesc = both empty ? 'all' : (from&&to? `${from}–${to}` : from? `from ${from}` : `to ${to}`).

Header info line: `Source: ${DATA.source} · ${records.length} paragraphs · years ${min}–${max}` (or "years unknown").

Chart: create once on load with empty data, then update. If Chart undefined (shouldn't be), guard.

Sort: 

```js
results.sort((a,b)=>{
  const ya = typeof a.year==='number'?a.year:-Infinity;
  const yb = typeof b.year==='number'?b.year:-Infinity;
  if(yb!==ya) return yb-ya;
  const sa=a.symbol||'', sb=b.symbol||'';
  if(sa!==sb) return sa.localeCompare(sb);
  return (b.paragraph||0)-(a.paragraph||0);
});
```

Now write the file. Keep it tidy, ~350 lines.

One more detail: "Changing a filter re-runs the search" — call runSearch on input events.

Enter also searches: form submit.

Search button type submit inside form.

Let me write it.