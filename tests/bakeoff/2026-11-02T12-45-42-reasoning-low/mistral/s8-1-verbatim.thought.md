Let me build the app. Single HTML file, inline CSS/JS, Chart.js preloaded. Search parser: tokens with AND/OR/NOT, quoted phrases. Whole-word matching case-insensitive. Highlight matched words in text without altering characters — wrap matches in <mark> using index-based slicing on the original text (case-insensitive regex with escaped terms, global flag, using word boundaries for plain words).

Parser design: tokenize input into terms: quoted phrases, NOT-prefixed terms, plain words, OR keywords, AND keywords. Grammar: expression = term (OR term)* — actually spec: words separated by spaces are ANDed; OR joins alternatives; NOT excludes. Simple approach: split into clauses. Let me implement a simple parser:

- Tokenize: scan for quoted strings ("..."), then words. Keywords AND, OR, NOT (case-insensitive? probably uppercase only, but let's accept case-insensitive AND/OR/NOT as operators when standalone... risky: "not" could be a search word. Spec says NOT excludes a word. I'll treat uppercase AND/OR/NOT as operators; lowercase as words. Actually safer: treat them as operators regardless of case? The example uses uppercase. Hmm, "torture NOT detention" — NOT uppercase. I'll treat case-insensitive AND/OR/NOT as operators only when they appear as standalone tokens and... but "not" is a common word in legal text ("is not"). If user searches "not" alone they'd get operator. I'll go with: operators recognized when uppercase (AND, OR, NOT). That's a reasonable, documented choice. Actually many search UIs are case-insensitive for operators. But risk: searching "right to NOT..." unlikely. I'll accept case-insensitive operators but mention in help? The help line is fixed by spec. I'll do case-insensitive operators — simpler and matches typical expectations. Hmm, but then searching for the word "or" (e.g., "or" in text) impossible. Legal text has "or" frequently. If someone searches "cruel or degrading", with case-insensitive OR, "or" becomes operator → "cruel" OR "degrading" — wrong result. That's bad. So uppercase-only operators is safer. I'll do uppercase-only, and note in help? Help line is specified: 'words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: "best interests" AND child'. I'll keep exactly that.

Parser: tokens list of {type: 'phrase'|'word', neg: bool, text}. Operators: AND (implicit), OR, NOT prefix.

Semantics: expression = and-groups joined by OR? Standard: OR has lower precedence than AND. So parse: expr := andExpr (OR andExpr)*; andExpr := factor (AND? factor)* where implicit AND between adjacent factors; factor := NOT? atom.

Evaluate per record: for each andExpr, all factors must match (negated must not match); expr matches if any andExpr matches.

Matching: plain word → whole word, case-insensitive: regex `(?<![A-Za-z0-9])word(?![A-Za-z0-9])` with escaped word. Use \b? \b works with word chars; but words may contain apostrophes/hyphens. Use custom boundaries: not preceded/followed by letter or digit. Phrase: exact sequence of words — match the phrase as literal substring case-insensitive? "exact sequence of words" — I'll match the phrase string case-insensitively as a substring but require word boundaries at ends. E.g. "best interests" matches "best interests of the child". Should it match "best  interests" with double space? No — exact sequence. I'll build regex: boundary + escaped phrase (spaces as \s+? no — exact). Keep literal spaces. Use lookarounds `(?<![A-Za-z0-9])` and `(?![A-Za-z0-9])`.

Highlighting: collect all matched spans across all positive terms that matched in this record (for highlighting, highlight all positive atoms that appear — spec test 1: search `"best interests" AND child` highlights both). For OR, highlight whichever alternatives matched. For NOT terms, don't highlight. Implementation: for each positive atom in the expression, find all matches in text; union spans; sort; build HTML with escaping, wrapping in <mark>. Must not alter characters — slice original text between spans.

Edge: overlapping spans — merge.

Filters: committee select (all committees from data + "All"), year from/to number inputs. Year missing → "year unknown", included when filter open (i.e., when from/to empty), excluded when range set. Committee missing? Probably always present; handle missing → "unknown" group? Keep simple: if committee missing, use "Unknown". Chart: matching paragraphs per committee for current search — count by committee of matched records.

Sort: newest General Comment first — by year desc, then... within same year, maybe by paragraph? "newest General Comment first" — sort by year desc, then symbol? I'll sort year desc, then committee, then paragraph desc? Keep: year desc, then paragraph desc (later paragraphs of same GC after? or before?). Simplest: year desc, then symbol asc, then paragraph asc. Fine.

Count line: "N paragraphs match out of M, filters: committee=CRC, years 2000–2010, search: ..." Build filter description.

Chart: bar chart per committee of matches. Chart.js bar. "How this is computed" note.

Copy citation: navigator.clipboard.writeText with fallback (execCommand). Button text "Copied" for 2s.

Empty text records: never match but counted in M. So M = total records count. Search with empty query? If search box empty — what happens? Probably show all (within filters)? Spec doesn't say. I'll treat empty search as matching all (N = filtered count). Reasonable.

Year range: from–to inputs; if only from set, years >= from; only to: <= to. Missing year excluded when any range set.

Title line: source, number of paragraphs, year range from data: e.g. "Source: WORKSHOP_DATA.gc — General Comments, paragraph by paragraph · 1,234 paragraphs · 1989–2025". Read from data: gc.title, gc.source, gc.count, min/max year of records.

Let me write the code carefully, under 700 lines.

Structure:

HTML: header (h1, subtitle line), search row (input + button), help line, filters (select committee, year from, year to), count line, chart canvas + note, results container.

JS:
- const GC = WORKSHOP_DATA.gc; records = GC.records.
- committees list: unique sorted.
- years: min/max.
- state: query, committee, yearFrom, yearTo.
- tokenize(query): returns tokens.
- parse(tokens): returns AST or null if invalid (e.g., trailing operator). Handle gracefully: if parse fails, treat... show message? Keep simple: if tokens empty → match all. If parse error, fall back to AND of all atoms? I'll implement parser that's lenient: ignore dangling operators.
- matchAtom(text, atom): regex test.
- evalExpr(ast, text).
- highlight(text, atoms): spans.
- render(): filter, search, count, chart, cards.

Tokenizer:
```js
function tokenize(q){
  const tokens=[]; let i=0;
  while(i<q.length){
    const c=q[i];
    if(/\s/.test(c)){i++;continue;}
    if(c==='"'){
      const end=q.indexOf('"', i+1);
      if(end===-1){ // unterminated quote: take rest as phrase
        tokens.push({type:'phrase', text:q.slice(i+1)}); i=q.length;
      } else {
        tokens.push({type:'phrase', text:q.slice(i+1,end)}); i=end+1;
      }
      continue;
    }
    // read word until whitespace or quote
    let j=i;
    while(j<q.length && !/\s/.test(q[j]) && q[j]!=='"') j++;
    tokens.push({type:'word', text:q.slice(i,j)});
    i=j;
  }
  return tokens;
}
```

Parser: convert tokens to atoms with operators:
```js
function parse(q){
  const toks=tokenize(q);
  // build list: {op:'AND'|'OR'|'NOT'|null, atom:{type,text}}
  const items=[]; let pendingNot=false; let pendingOp='AND';
  for(const t of toks){
    const up=t.text.toUpperCase();
    if(t.type==='word' && up==='AND'){ pendingOp='AND'; pendingNot=false; continue; }
    if(t.type==='word' && up==='OR'){ pendingOp='OR'; pendingNot=false; continue; }
    if(t.type==='word' && up==='NOT'){ pendingNot=true; continue; }
    items.push({op: items.length===0?'AND':pendingOp, neg:pendingNot, atom:t});
    pendingNot=false; pendingOp='AND';
  }
  // group into OR of ANDs
  const groups=[]; let cur=[];
  for(const it of items){
    if(it.op==='OR' && cur.length){ groups.push(cur); cur=[]; }
    cur.push(it);
  }
  if(cur.length) groups.push(cur);
  if(!groups.length) return null; // match all
  return groups;
}
```
Wait: pendingOp after an atom resets to AND — good, implicit AND. But if OR appears then atom: op='OR' starts new group. If OR at start (cur empty), the atom just goes into cur with op OR but cur empty so it's first — fine.

Atom regex:
```js
function atomRegex(atom){
  const esc=atom.text.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const core = atom.type==='phrase' ? esc : esc; // phrase: literal; word: whole word
  if(atom.type==='word') return new RegExp('(?<![A-Za-z0-9])'+esc+'(?![A-Za-z0-9])','gi');
  return new RegExp('(?<![A-Za-z0-9])'+esc.replace(/\s+/g,'\\s+')+'(?![A-Za-z0-9])','gi');
}
```
Hmm phrase: "exact sequence of words" — should internal whitespace be flexible? Exact phrase: I'll allow \s+ between words (still exact sequence of words). That's reasonable. Actually "exact sequence of words" — "best interests" should match "best interests" — with \s+ it also matches "best  interests" (double space) — still same sequence of words. Fine.

Lookbehind support: modern browsers fine.

Matching per record: text lower? Use regex with 'i' flag on original text.

eval:
```js
function matches(groups, text){
  if(!groups) return true;
  if(!text) return false; // empty text never matches (but if no search query, matches all — handle: if groups null return true even for empty text)
  return groups.some(g=>g.every(it=>{
    const r=atomRegex(it.atom).test(text);
    return it.neg ? !r : r;
  }));
}
```
Careful: empty text with a query → no match. With empty query (groups null) → match all including empty text. Good.

Highlight: gather positive atoms from all groups (only those that... just all positive atoms; highlight all their occurrences). For test 1, both atoms positive and both matched. For OR where only one alternative present, highlighting the absent one finds nothing — fine.

```js
function highlightHTML(text, groups){
  const spans=[];
  if(groups){
    for(const g of groups) for(const it of g){
      if(it.neg) continue;
      const re=atomRegex(it.atom);
      let m;
      while((m=re.exec(text))){ spans.push([m.index, m.index+m[0].length]); }
    }
  }
  // merge
  spans.sort((a,b)=>a[0]-b[0]);
  const merged=[];
  for(const s of spans){
    if(merged.length && s[0]<=merged[merged.length-1][1]) merged[merged.length-1][1]=Math.max(merged[merged.length-1][1],s[1]);
    else merged.push(s);
  }
  let out='', pos=0;
  for(const s of merged){
    out+=escapeHTML(text.slice(pos,s[0]))+'<mark>'+escapeHTML(text.slice(s[0],s[1]))+'</mark>';
    pos=s[1];
  }
  out+=escapeHTML(text.slice(pos));
  return out;
}
```

Filters:
```js
function inYearFilter(r){
  const f=state.yearFrom, t=state.yearTo;
  if(f===''&&t==='') return true;
  if(r.year==null||r.year===undefined) return false;
  if(f!=='' && r.year < +f) return false;
  if(t!=='' && r.year > +t) return false;
  return true;
}
```

Render cards: for each matched record sorted: card with header line: committee badge, short_title||title||symbol, year or "year unknown", symbol link (doc_url ? <a target=_blank> : plain). Then paragraph text div with highlight. Citation button.

Citation: `${symbol}, para. ${paragraph}`. paragraph is int. If paragraph missing? Spec says always present presumably; fallback: if paragraph null, just symbol? Spec: "The citation is symbol + ', para. ' + paragraph, nothing invented." Assume present; guard: if paragraph==null use symbol only? I'll do `symbol + (paragraph!=null ? ', para. '+paragraph : '')`.

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

Chart: Chart.js bar, labels committees (of matched), data counts. Destroy previous chart instance. If N===0, show "no data" — still render chart with empty? Show message instead. I'll update chart data; if no matches, chart with empty labels fine, or hide. I'll keep chart and update.

Count line: `N paragraphs match out of M` + filters description: `filters: committee: CRC; years: 2000–2010; search: "..."` or "no search". Build: parts=[]; if committee!=='All' push 'committee = X'; if yearFrom/To push 'years ≥ f' etc.; if query push `search: query`. Join '; ' or 'no filters' when none... but search always? If query empty and no filters: "filters: none".

Sorting: newest GC first: sort by (year ?? -Infinity) desc, then symbol asc, then paragraph asc. Records with unknown year go last.

Committee select options: "All" + unique committees sorted alphabetically.

Year inputs: type number, placeholders "from" / "to", min/max from data maybe.

Header line: `${GC.source} · ${GC.count} paragraphs · ${minYear}–${maxYear}` plus title? Spec: "one line: source, number of paragraphs, year range, all read from the data." Use GC.title too maybe: `${GC.title} — ${GC.source} · N paragraphs · years X–Y`. Keep one line.

Also "How this is computed" note near chart: "Bars count the paragraphs that match the current search and filters, grouped by committee; the bar heights add up to N."

Also note near count line? Spec says count line format given. Add small note maybe not needed.

Empty results: message "No paragraph contains these words" + tip "Try OR instead of AND, or fewer words."

Escape HTML function.

Chart styling: accent #1f6fb2.

Layout: max-width 900px, padding. Base font 16px.

Let me also handle Enter key on input → search. Search button click → search. Filters change → re-run (read current query). So render() reads state from inputs directly.

Let me write the full file.

Also handle gc records where text empty: counted in M (M = records.length). Fine.

Committee missing: label "Unknown". For chart grouping use r.committee || 'Unknown'.

Year display: r.year ?? 'year unknown'.

Write code now. Keep under 700 lines — easily.

One more detail: "Changing a filter re-runs the search" — on 'change' and 'input' for year inputs? Use 'input' for year, 'change' for select. Fine.

Chart note and count line update each render.

Card structure:
```html
<article class="card">
  <div class="card-head">
    <span class="badge">CRC</span>
    <span class="gctitle">GC14: ...</span>
    <span class="year">2000</span>
    <a class="symbol" href="..." target="_blank" rel="noopener">CRC/C/GC/14</a>
  </div>
  <p class="para">...highlighted...</p>
  <button class="copy">Copy citation</button>
</article>
```

Maybe show paragraph number in card too: "para. 6" — helpful. Add `<span class="parano">para. 6</span>`.

Now write it.