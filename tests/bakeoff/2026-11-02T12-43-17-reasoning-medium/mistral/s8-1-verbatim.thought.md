The user wants me to build an HTML app for searching General Comments. Let me carefully parse the requirements:

1. Title "General Comments search" + one line: source, number of paragraphs, year range from data.
2. Search box + Search button (Enter works) + help line about AND/OR/NOT/quotes.
3. Two filters: committee dropdown (all committees + "All"), year from–to. Changing filter re-runs search.
4. Count line: "N paragraphs match out of M, filters: …".
5. Bar chart: matching paragraphs per committee, with "How this is computed" note. Use Chart.js (window.Chart preloaded).
6. Results sorted newest GC first. Each card: committee, short title, year, symbol linked to doc_url (new tab); full paragraph with highlighted search words; "Copy citation" button copying "symbol, para. paragraph", button reads "Copied" for 2s.
7. No matches: message + tip.

Search semantics:
- Case-insensitive.
- Plain word = whole word match ("right" doesn't match "rights").
- Quoted phrase = exact sequence of words.
- Space-separated = AND; OR joins alternatives; NOT before word/phrase excludes.
- No brackets, no wildcards, no stemming.

Parsing the query: tokens. Let me design a parser:
- Tokenize into quoted phrases ("...") and words. Operators: OR, NOT (uppercase? The help says "words are combined with AND unless you write OR; NOT excludes a word". Probably case-sensitive operators OR/NOT? Safer: treat uppercase OR and NOT as operators; lowercase "or"/"not" as words? Hmm. The example uses uppercase AND, OR, NOT. I'll treat exact uppercase "OR" and "NOT" as operators, and "AND" as explicit AND (same as space). Lowercase "or"/"not" treated as literal words. That's a reasonable, documented choice. Actually to be safe, maybe treat case-insensitive operators? But then searching for the word "not" would be impossible. The spec example: `"best interests" AND child`. I'll accept operators case-insensitively? Hmm, "NOT excludes a word" — if someone searches "right not wrong", they'd expect... ambiguous. I'll go with: operators recognized when uppercase OR/NOT/AND exactly; otherwise literal words. And mention in help? The help line is specified: 'words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: `"best interests" AND child`.' I'll keep that exact help text.

Grammar: expression := term (OR term)* where implicit AND between adjacent terms; term := [NOT] (word | "phrase"). So parse: split into tokens with quotes. Then build: iterate tokens; maintain list of AND-groups; each group is a set of alternatives (OR). NOT applies to the following word/phrase.

Simple approach:
- tokens = tokenize(query) → array of {type: 'phrase'|'word', value, quoted:bool}
- Build clauses: array of {neg: bool, alts: [matcher,...]} where consecutive terms separated by OR join into same clause's alts; NOT prefixes next term.
- Matching: for each clause: if neg, require none of alts match; else require at least one alt matches. All clauses must pass (AND).

Whole-word matching: use regex with word boundaries. Need to escape regex special chars in the search word. Word chars: use `\b` — but words may contain apostrophes/hyphens? Keep simple: escape, and use boundaries `(?<![\w])` and `(?![\w])` lookarounds to be safe with unicode? JS supports lookbehind in modern browsers. Simpler: `\b` works for ASCII words. For phrase: match sequence of words with flexible whitespace? "exact sequence of words" — I'll normalize whitespace: build regex from phrase words joined by `\s+`, with word boundaries at ends. Case-insensitive flag 'gi'.

Highlighting: need to wrap matched words in the text without altering characters. Approach: compute all match ranges (start/end indices) in the original text for each positive (non-NOT) term that matched... Actually highlight all positive terms' matches (including OR alternatives that matched? The test says: search `"best interests" AND child`: every card highlights both "best interests" and "child". So highlight all positive terms. For OR alternatives, highlight whichever matched (or all alternatives that appear? Simpler: highlight all matches of all positive alternatives — but if an OR alternative doesn't appear in this card, no matches anyway). NOT terms: don't highlight.

Implementation: for each positive matcher, run regex with 'gi' over text, collect ranges. Merge overlapping ranges. Then build HTML: escape text segments, wrap ranges in `<mark>`. Must escape HTML in text to avoid injection and preserve characters. Build via DOM or string with escaping. I'll build with string concatenation using an escape function, splitting text by ranges.

Empty query: what happens? If search box empty, show all (filtered) paragraphs? Probably yes — search with empty query matches everything. The count line "N paragraphs match out of M". I'll treat empty query as match-all. That's sensible.

Filters:
- Committee dropdown: unique committees sorted, plus "All".
- Year from–to: two number inputs (or text inputs). "from–to" range. Missing year: included when filter is open (both empty), excluded when a range is set. So if from or to is set, records with no year are excluded.
- Changing filter re-runs search (on 'change'/'input' events).

Sorting: "newest General Comment first". Sort by year descending; tie-break? By committee? By paragraph descending maybe. I'll sort by year desc, then symbol, then paragraph desc. Records with no year go last. Keep deterministic.

Chart: Chart.js bar chart, matching paragraphs per committee for current search. Labels = committees present in matches (or all committees? "matching paragraphs per committee" — I'll show committees that have ≥1 match, sorted by count desc; if none, show empty chart or a message). Bars add up to N. Note: "How this is computed: counts of matching paragraphs grouped by committee; bars sum to N." Update chart on each search — destroy and recreate, or update data. I'll keep a single Chart instance and update its data, or destroy/recreate. Simpler: destroy and recreate each time (chart.destroy() then new Chart). Fine.

Count line: "N paragraphs match out of M, filters: committee = X, years = Y–Z" or "no filters". Build filter description dynamically.

Header line: source, number of paragraphs, year range. From data: `WORKSHOP_DATA.gc` has `title`, `source`, `count`, `records`. So: e.g. "Source: {source} · {count} paragraphs · years {min}–{max}". Year range computed from records with year; if none, "year unknown". Use `count` field? The spec says read from data; count is given but I can also compute records.length. I'll use records.length for M and display count from data or records.length — use records.length to be safe, but the header can use `gc.count`. I'll compute from records to be consistent: M = records.length. Header: `${gc.source} — ${records.length} paragraphs, ${minYear}–${maxYear}`. Handle missing source gracefully.

Card layout:
- Header row: committee (bold), short_title (or title, or symbol), year (or "year unknown"), symbol link (if doc_url) target _blank rel noopener.
- Paragraph text with highlight, full text, maybe in a <details>? Spec says "the full paragraph" shown; the general rules say keep full text available (click to expand) — but here spec says each card shows the full paragraph. I'll show full text directly (it's a paragraph, not huge). Maybe with a "para. N" label. The citation includes para. I'll show "para. N" in card too.
- Copy citation button: copies `${symbol}, para. ${paragraph}`. Use navigator.clipboard.writeText with fallback (execCommand). Button text changes to "Copied" for 2s then back.

No matches: "No paragraph contains these words" + tip "Try OR instead of AND, or fewer words."

Missing values handling:
- short_title empty → title → symbol.
- year missing → "year unknown"; included when year filter open; excluded by range.
- doc_url missing → symbol as plain text.
- text empty → never matches but counted in M. So in matching, if text is empty/missing, only matches if query is empty? "never matches" — even empty query? Hmm: "empty `text` → never matches but still counted in M". If query empty, does it match? Strictly "never matches" — but then with empty search, empty-text records wouldn't show. That seems odd but the rule says never matches. I'll implement: if text is empty/missing, the record never matches any search, including empty query? That would make initial view (empty search) exclude them, and N < M initially. Hmm, but is empty query a "search"? The count line says "N paragraphs match out of M". Safer interpretation: empty text never matches a search query; with an empty query... ambiguous. I'll treat empty query as match-all except empty-text records? That seems weird. Alternatively treat empty text as never matching anything, including empty query — consistent with the literal rule. But then initial page load shows N = M - (empty text count). Actually maybe better: empty query → all records match (including empty text ones, showing "(no text)"?). The rule explicitly says empty text never matches. I'll follow literally: empty/missing text → never matches, even for empty query. And display? They won't appear in results. But counted in M. Hmm, but then initial load with empty search wouldn't show them. That's fine and follows the spec. Actually wait — maybe safer: empty query matches everything including empty text (since no words to match), but any non-empty query never matches empty text. The test criteria don't cover this. The rule "empty text → never matches but still counted in M" — I think intent is: a search for words can't match an empty paragraph. With empty query there are no words... I'll go with: empty query matches all records (including empty text, card shows "No text available."), non-empty query never matches empty text. Hmm, but literal reading says never matches. Let me re-read: "Missing values: ... empty `text` → never matches but still counted in M." I think the safest is literal: never matches. But then initial view (no search yet) — should the app auto-run search on load with empty query? If it does and empty-text records never match, they're hidden. If the app doesn't run until user searches, initial results could show all. To keep N, bars, cards consistent, I'll run the search on load with empty query, and empty-text records never match (per rule). Cards for them never appear. That's consistent: "never matches but still counted in M". OK, literal it is. Actually hmm, one more consideration: with empty query, is that a "match"? The rule says never matches — I'll implement `matchesQuery` returns false when text is empty and query is non-empty; for empty query... Let me just decide: empty text → never matches any query including empty. Simple, literal. But then on load, N might be less than M even with no search. The count line will show that. Fine. Actually, you know, I worry a grader might load the app and expect N = M initially. But the rule explicitly says empty text never matches. The real data likely has no empty texts anyway. I'll go literal but... hmm. Let me think about which is more defensible. "empty `text` → never matches but still counted in M" — the point is M includes them, N doesn't. If empty query matched them, then with empty query N would include them, contradicting "never matches". So literal: never matches, period. Done.

Wait, but actually — should the app even auto-run on load? Yes, show all results initially (empty query). With empty query, all non-empty-text records match. Good.

Year filter inputs: two inputs type="number" with placeholders "from" and "to". On 'input' or 'change' re-run. I'll use 'input' for responsiveness but debounce slightly? Keep simple: 'change' and 'input' both call run(). Fine.

Committee filter: select with "All" + sorted unique committees.

Search parsing details:

```js
function tokenize(q){
  const tokens=[]; const re=/"([^"]*)"|(\S+)/g; let m;
  while((m=re.exec(q))!==null){
    if(m[1]!==undefined){ if(m[1].trim()!=='') tokens.push({type:'phrase', value:m[1]}); }
    else tokens.push({type:'word', value:m[2]});
  }
  return tokens;
}
```

Then parse into clauses:

```js
function parseQuery(q){
  const tokens=tokenize(q);
  const clauses=[]; // {neg:false, alts:[{value, quoted}]}
  let pendingNeg=false;
  let current=null; // current OR-group
  for(const t of tokens){
    const v=t.value;
    if(v==='AND'){ // explicit AND: close current group
      current=null; pendingNeg=false; continue;
    }
    if(v==='OR'){ // continue current group (create if none)
      if(!current){ current={neg:false, alts:[]}; clauses.push(current); }
      pendingNeg=false; continue;
    }
    if(v==='NOT'){ pendingNeg=true; continue; }
    // a term
    const term={value:v, quoted:t.type==='phrase'};
    if(current && clauses[clauses.length-1]===current && !pendingNeg){
      // hmm, need to know whether previous token was OR
    }
  }
}
```

Better: track `lastWasOr` flag.

```js
function parseQuery(q){
  const tokens=tokenize(q);
  const clauses=[];
  let group=null; let pendingNeg=false; let lastOr=false;
  for(const t of tokens){
    const v=t.value;
    if(v==='AND'){ group=null; lastOr=false; pendingNeg=false; continue; }
    if(v==='OR'){ if(!group){ group={neg:false,alts:[]}; clauses.push(group);} lastOr=true; pendingNeg=false; continue; }
    if(v==='NOT'){ pendingNeg=true; continue; }
    const term={value:v, quoted:t.type==='phrase'};
    if(group && lastOr){
      group.alts.push(term);
    } else {
      group={neg:pendingNeg, alts:[term]};
      clauses.push(group);
    }
    lastOr=false; pendingNeg=false;
  }
  return clauses;
}
```

Wait, NOT with OR: `a NOT b OR c` — NOT applies to b only. With my logic: a → new group. NOT → pendingNeg. b → group is current (lastOr false) → new group with neg:true. OR → group exists (the neg one), lastOr=true. c → added to the neg group's alts → meaning "not (b or c)". Hmm, `a NOT b OR c` arguably means a AND (NOT b) AND c, or a AND NOT(b OR c)? Ambiguous; no brackets allowed anyway. Edge case, fine either way. Actually maybe NOT should bind to the next term only, and OR after a NOT-term starts a new positive group? E.g. `torture NOT detention OR ill-treatment` — user probably means torture AND NOT detention AND ill-treatment? Or torture AND NOT(detention OR ill-treatment)? Ambiguous. Keep simple: NOT binds to next term; if OR follows, it extends the negated group (NOT (a OR b)). Hmm, alternatively when OR encountered and last group is negated, start a new positive group. I think `x NOT y OR z` more naturally reads as x AND NOT y AND z? Honestly ambiguous. I'll make OR after a negated term start a new positive group — no wait, that breaks `NOT a OR b` meaning "not (a or b)" which is a common intent. Ugh. Without brackets, either is defensible. I'll keep the simple rule: OR joins the immediately preceding group (whatever its negation). Document nothing; it's an edge case.

Hmm, actually let me reconsider: `torture NOT detention` test — works either way. Keep simple.

Matcher:

```js
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
function termRegex(term){
  if(term.quoted){
    const words=term.value.split(/\s+/).filter(Boolean).map(escRe);
    if(!words.length) return null;
    return new RegExp('(?<![\\w])'+(words.join('\\s+'))+'(?![\\w])','gi');
  }
  return new RegExp('(?<![\\w])'+escRe(term.value)+'(?![\\w])','gi');
}
```

Lookbehind support: modern browsers OK. Alternatively use `\b` — but `\b` fails if word starts/ends with non-word char (e.g. hyphenated). Lookarounds with `[\w]` are more precise for "whole word". Use lookarounds; fallback if not supported? Modern sandbox browser supports it. I'll use a boundary approach without lookbehind to be safe: match `(^|[^\w])(word)(?=$|[^\w])` and adjust indices. That complicates range extraction. Lookbehind is fine in any current Chrome/Firefox/Safari (Safari 16.4+). I'll use lookbehind.

Hmm, but "right" should not match "rights": with `(?<![\w])right(?![\w])`, in "rights", after "right" comes "s" which is \w → no match. Good. In "right's"? apostrophe is not \w, so "right" in "right's" matches — acceptable.

Case-insensitive: 'i' flag. Unicode: \w is ASCII-only in JS without 'u' flag; fine.

Matching a record:

```js
function recordMatches(rec, clauses){
  const text=rec.text||'';
  if(!text) return false;
  for(const cl of clauses){
    let any=false;
    for(const alt of cl.alts){
      const re=termRegex(alt);
      if(re){ re.lastIndex=0; if(re.test(text)) any=true; }
    }
    if(cl.neg){ if(any) return false; }
    else if(!any) return false;
  }
  return true;
}
```

Note: regex with 'g' flag and .test — lastIndex statefulness; create fresh regex each time or reset lastIndex. I'll create fresh per call (fine for perf at this scale; records maybe a few thousand paragraphs — creating regexes per record per term could be slow-ish but OK; better: precompile matchers once per search). I'll precompile: clauses → compiled with regexes once per run, then test each record. For highlighting, reuse compiled regexes with 'g' to collect ranges.

Highlight ranges:

```js
function highlightRanges(text, clauses){
  const ranges=[];
  for(const cl of clauses){
    if(cl.neg) continue;
    for(const alt of cl.alts){
      if(!alt.re) continue;
      alt.re.lastIndex=0;
      let m;
      while((m=alt.re.exec(text))!==null){
        ranges.push([m.index, m.index+m[0].length]);
        if(m[0].length===0) alt.re.lastIndex++; // safety
      }
    }
  }
  // merge
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
function escHtml(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function renderHighlighted(text, ranges){
  let out=''; let pos=0;
  for(const [a,b] of ranges){
    out+=escHtml(text.slice(pos,a))+'<mark>'+escHtml(text.slice(a,b))+'</mark>';
    pos=b;
  }
  out+=escHtml(text.slice(pos));
  return out;
}
```

If query empty → no ranges, plain escaped text.

Copy citation:

```js
async function copyCitation(btn, citation){
  try{
    await navigator.clipboard.writeText(citation);
  }catch(e){
    const ta=document.createElement('textarea');
    ta.value=citation; document.body.appendChild(ta); ta.select();
    try{ document.execCommand('copy'); }catch(_){}
    ta.remove();
  }
  const old=btn.textContent;
  btn.textContent='Copied'; btn.classList.add('copied');
  setTimeout(()=>{ btn.textContent=old; btn.classList.remove('copied'); },2000);
}
```

Clipboard API may fail in sandbox (non-secure context?) — fallback included. Note: in sandboxed iframe, navigator.clipboard may be undefined; guard: `if(navigator.clipboard && navigator.clipboard.writeText)`.

Chart: Chart.js bar. Data: committees of matching records, counts. Sort desc by count, then alphabetically. Colors: accent #1f6fb2 for bars. Note under chart: "How this is computed: each matching paragraph is counted once, in its committee; the bars add up to N (the count above)."

Chart config:

```js
new Chart(ctx, {type:'bar', data:{labels, datasets:[{label:'Matching paragraphs', data:counts, backgroundColor:'#1f6fb2'}]}, options:{plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true, ticks:{precision:0}, title:{display:true,text:'Paragraphs'}}, x:{ticks:{autoSkip:false}}}}});
```

Destroy previous: keep `chart` variable; `if(chart) chart.destroy();`.

If no matches: show chart with empty? I'll still render chart with zero data or hide chart and show message. Spec: "If nothing matches: 'No paragraph contains these words' and a tip". Chart with no bars is fine; I'll update chart with empty labels and show the no-match message in results area.

Sorting results: newest GC first. Sort key: year desc (missing year → -Infinity → last), then... within same year, maybe by committee then paragraph desc. I'll do: (b.year||-1)-(a.year||-1), then symbol localeCompare, then (b.paragraph||0)-(a.paragraph||0). Paragraph may be int. Fine.

Count line: `N paragraphs match out of M` + filters description: e.g. `filters: committee = CRC; years = 2003–2011` or `filters: none`. Build: parts=[]; if committee!=='All' push `committee: ${committee}`; if from or to set push `years: ${from||'…'}–${to||'…'}`; if none, "no filters". Format: `N paragraphs match out of M · filters: ...`. Spec: "N paragraphs match out of M, filters: …". I'll do exactly: `${N} paragraphs match out of ${M}, filters: ${desc}`.

Header line: `Source: ${gc.source} · ${M} paragraphs · years ${minYear}–${maxYear}` — handle no years: "years unknown". Also gc.title maybe. Spec: "one line: source, number of paragraphs, year range, all read from the data." So: `${gc.source} — ${M} paragraphs — ${min}–${max}`. I'll include title too? Keep to spec: source, count, year range. Maybe: "General Comments, paragraph by paragraph — source: X — N paragraphs — years A–B". I'll write: `${gc.title||'General Comments'} · Source: ${gc.source} · ${M} paragraphs · ${minYear}–${maxYear}`. Hmm "one line: source, number of paragraphs, year range". Keep it: `Source: ${source} · ${M} paragraphs · years ${range}`. Good.

Year filter behavior: from/to inputs; record included if (no from or year>=from) and (no to or year<=to); if record has no year: included only if both from and to empty. Implement:

```js
function passesYear(rec, from, to){
  if(from==='' && to==='') return true;
  const y=rec.year;
  if(y==null || y===undefined || isNaN(y)) return false;
  if(from!=='' && y < +from) return false;
  if(to!=='' && y > +to) return false;
  return true;
}
```

Committee filter: rec.committee === selected (committee could be missing? then only matches "All"). Fine.

Search runs on: button click, Enter in input, filter change. Also maybe live on input? Spec says button/Enter; filters re-run. I'll also run on search input 'input' event? Spec doesn't ask; keep to button/Enter to avoid surprises. Actually live search is nice but spec says Search button and Enter. Keep button + Enter only.

Layout: header, controls (search row, filters row), count line, chart, results. Max width ~900px, no horizontal scroll. Base font 16px. Accent #1f6fb2. Light background (#f5f7fa), white cards.

Card structure:

```html
<article class="card">
  <div class="card-head">
    <span class="committee">CRC</span>
    <span class="gctitle">GC14: ...</span>
    <span class="year">2000</span>
    <a class="symbol" href="..." target="_blank" rel="noopener">CRC/C/GC/14</a>
  </div>
  <p class="para"><span class="parano">para. 6</span> <span class="text">...</span></p>
  <button class="copy">Copy citation</button>
</article>
```

Citation: `${symbol}, para. ${paragraph}`. If paragraph missing? Spec says citation is symbol + ", para. " + paragraph. If paragraph null... unlikely; fallback: just symbol. I'll do `symbol + (paragraph!=null ? ', para. '+paragraph : '')`.

Symbol link: if doc_url truthy → `<a href target=_blank>`; else plain span.

Performance: records maybe ~1000-3000 paragraphs. Rendering all cards each search could be heavy but fine. Maybe cap rendering? Spec doesn't mention pagination. Keep all; it's fine.

Chart.js preloaded as window.Chart. Guard `if(window.Chart)`.

Now write the full HTML. Keep under ~700 lines. Let me draft.

Also "How this is computed" note near chart and maybe near count line. Add small note under count: "Counting is done in your browser on the paragraph texts; filters are applied before the search." And chart note: "How this is computed: matching paragraphs grouped by committee; bars sum to N."

Help line exactly: 'Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: "best interests" AND child.' — spec: 'a one-line help: words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: `"best interests" AND child`.' I'll render with the example in code style.

Edge: quoted phrase with multiple words: "best interests" — regex joins words with \s+. Good.

NOT before a phrase: `NOT "best interests"` — tokenizer handles quoted token, NOT flag applies. Good.

Empty query → clauses=[] → matches all (except empty text per rule). Highlight: none.

One more: "The search looks at the paragraph text only." Yes, only rec.text.

Let me also handle `paragraph` display: show "para. N" label in card. If paragraph null, omit.

Now the code:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments search</title>
<style>
  :root{ --accent:#1f6fb2; --bg:#f4f6f9; --card:#ffffff; --ink:#1c2733; --muted:#5b6b7b; --line:#d9e1ea; }
  *{box-sizing:border-box;}
  body{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  .wrap{ max-width:920px; margin:0 auto; padding:28px 20px 60px; }
  h1{ font-size:1.6rem; margin:0 0 6px; color:var(--accent); }
  .sub{ color:var(--muted); margin:0 0 22px; }
  .panel{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px 18px; margin-bottom:16px; }
  .searchrow{ display:flex; gap:10px; flex-wrap:wrap; }
  #q{ flex:1 1 320px; padding:10px 12px; font-size:16px; border:1px solid var(--line); border-radius:8px; }
  button{ ... }
  .btn{ background:var(--accent); color:#fff; border:none; border-radius:8px; padding:10px 18px; font-size:16px; cursor:pointer; }
  .btn:hover{ filter:brightness(1.08); }
  .help{ color:var(--muted); font-size:0.92rem; margin:8px 0 0; }
  .filters{ display:flex; gap:14px; flex-wrap:wrap; align-items:end; margin-top:12px; }
  label{ font-size:0.9rem; color:var(--muted); display:block; margin-bottom:4px; }
  select, input[type=number]{ padding:8px 10px; font-size:15px; border:1px solid var(--line); border-radius:8px; background:#fff; }
  .yearinputs input{ width:90px; }
  #countline{ font-weight:600; margin:0 0 6px; }
  .note{ color:var(--muted); font-size:0.88rem; margin:4px 0 0; }
  #chartbox{ max-width:640px; }
  .card{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 18px; margin-bottom:14px; }
  .card-head{ display:flex; flex-wrap:wrap; gap:8px 14px; align-items:baseline; margin-bottom:8px; }
  .committee{ font-weight:700; color:var(--accent); }
  .gctitle{ font-weight:600; }
  .year{ color:var(--muted); }
  .symbol{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:0.92rem; }
  .para{ margin:6px 0 10px; white-space:pre-wrap; word-wrap:break-word; }
  .parano{ color:var(--muted); font-size:0.9rem; margin-right:6px; }
  mark{ background:#ffe9a8; padding:0 1px; border-radius:2px; }
  .copy{ background:#fff; color:var(--accent); border:1px solid var(--accent); border-radius:8px; padding:6px 12px; font-size:0.92rem; cursor:pointer; }
  .copy.copied{ background:var(--accent); color:#fff; }
  #nomatch{ ... }
</style>
```

JS: as planned.

Let me now also compute header year range: years = records.map(r=>r.year).filter(y=>typeof y==='number'); min/max. If none: "years unknown".

Committees list: unique sorted via Set, localeCompare.

Write run():

```js
function run(){
  const q=input.value;
  const clauses=parseQuery(q); // compiled
  compile(clauses);
  const com=committeeSel.value;
  const from=yearFrom.value.trim(), to=yearTo.value.trim();
  const matched=[];
  for(const rec of records){
    if(com!=='All' && rec.committee!==com) continue;
    if(!passesYear(rec, from, to)) continue;
    if(!recordMatches(rec, clauses)) continue;
    matched.push(rec);
  }
  matched.sort(sortFn);
  renderCount(matched.length, com, from, to);
  renderChart(matched);
  renderResults(matched, clauses);
}
```

compile: attach re to each alt: `alt.re = termRegex(alt)`.

recordMatches uses alt.re with lastIndex reset. Since 'g' flag, .test advances lastIndex; reset before each test: `alt.re.lastIndex=0`.

renderResults: build HTML string, set innerHTML of container. For each rec: card. Use escHtml for all text fields. Highlight via ranges.

Copy buttons: attach event delegation on container: click on .copy → find data-citation attr → copy. Store citation in dataset.

Chart: 

```js
let chart=null;
function renderChart(matched){
  const counts={};
  for(const r of matched){ const c=r.committee||'(no committee)'; counts[c]=(counts[c]||0)+1; }
  const entries=Object.entries(counts).sort((a,b)=>b[1]-a[1] || a[0].localeCompare(b[0]));
  const labels=entries.map(e=>e[0]), data=entries.map(e=>e[1]);
  if(chart) chart.destroy();
  if(window.Chart){
    chart=new Chart(ctx,{type:'bar',data:{labels,datasets:[{data,backgroundColor:'#1f6fb2',borderRadius:4}]},options:{...}});
  }
}
```

If no matches, labels empty — chart shows empty axes. Fine. Maybe hide chart box when empty and show message? Keep chart with empty data; message appears in results.

Canvas needs a sized container: `<div id="chartbox"><canvas id="chart"></canvas></div>` with max-height maybe 260px; Chart.js responsive: true, maintainAspectRatio:false with container height set. I'll set `#chartbox{height:260px}` when there is data... simpler: maintainAspectRatio:true default, canvas width 100%. Set options responsive:true, maintainAspectRatio:false and give chartbox a fixed height (e.g., 240px). With empty data it still renders axes. OK.

X ticks autoSkip false might crowd with many committees (~10 committees max: CAT, CEDAW, CERD, CESCR, CMW, CRC, CRPD, CED, CCPR... ~10). Fine.

Now the "How this is computed" notes:
- Under count line: "How this is computed: filters are applied first, then the word search on the paragraph text only; counting is done in your browser, not estimated."
- Under chart: "How this is computed: each matching paragraph is counted once under its committee, so the bars add up to the N above."

No-match block: `<div class="panel" id="nomatch">No paragraph contains these words. Tip: try OR instead of AND, or use fewer words.</div>` — spec: "No paragraph contains these words" and a tip to try OR or fewer words.

Also show results even when query empty — yes.

Enter key: input keydown Enter → run. Button click → run. Filters: 'change' on select and both year inputs ('input' too). I'll add 'input' listener on year inputs and 'change' on select; also 'change' on year inputs. Just use 'input' for text/number and 'change' for select — both call run.

Initial: populate committee select, run().

Title of doc: "General Comments search".

Let me also make sure symbol link: `doc_url` may be empty string → unlinked. `<a href="${escAttr(rec.doc_url)}" target="_blank" rel="noopener noreferrer">`.

escAttr: escape & < > ".

Card head order per spec: committee, short title, year, symbol. Then paragraph, then copy button.

short title fallback: `rec.short_title || rec.title || rec.symbol || ''`.

Year display: `rec.year != null ? rec.year : 'year unknown'`.

Paragraph label: `rec.paragraph != null ? 'para. '+rec.paragraph : ''`.

Citation: `rec.symbol + (rec.paragraph!=null ? ', para. '+rec.paragraph : '')`. If symbol missing? Then citation would be "undefined" — guard: if no symbol, use short_title? Spec says citation is symbol + para, nothing invented. If symbol missing (unlikely), fallback to title? I'll do: base = rec.symbol || rec.short_title || rec.title || ''; citation = base + para part. Fine.

Now, one subtlety: highlight for OR alternatives — highlight all positive alts' matches. For `"best interests" AND child`, both highlighted. Good.

NOT terms not highlighted. Good.

Test 2: `torture NOT detention` — cards contain "torture" but not "detention". Our logic: clause1 {neg:false, alts:[torture]}, clause2 {neg:true, alts:[detention]}. Good.

Test 3: committee CRC → chart single bar height = N. Our chart groups by committee of matched → only CRC. Good.

Now write everything carefully. Also ensure no external loads. Chart.js from window.Chart.

Line count: aim ~350-450 lines. Good.

Let me write the final HTML.

Also add `lang="en"`, meta viewport. Title element.

One more detail: "Search box with a Search button (Enter also searches)". Add `type="search"`? Use text with id q. Enter handler on keydown.

Also the count line format: "N paragraphs match out of M, filters: …". I'll produce: `3 paragraphs match out of 1234, filters: committee = CRC, years 2003–2011` or `filters: none (search: "…")`? Spec says filters: … — describe active filters. If none: "no filters". Maybe include the query too? Spec: count line is "N paragraphs match out of M, filters: …". I'll append search query in the filters description? Keep to filters only; maybe add `search: "query"` when query non-empty — helpful. I'll do: `filters: committee = CRC; years = 2000–2010; search = "torture"` and if nothing active: `filters: none`. Hmm, spec literally: "N paragraphs match out of M, filters: …". Adding search is extra but harmless and informative. I'll include it.

Singular/plural: "1 paragraph matches out of M". I'll handle pluralization simply: `${N} paragraph${N===1?'':'s'} match out of ${M}`. "1 paragraphs match" would be wrong; do the plural handling.

Now write code.

```js
const gc = window.WORKSHOP_DATA.gc;
const records = gc.records || [];
const M = records.length;
```

Header sub: `Source: ${gc.source||'General Comments'} · ${M} paragraphs · years ${yearRange}` where yearRange computed.

Edge: gc.source might be long; fine.

Full JS:

```js
(function(){
  const gc = window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc ? window.WORKSHOP_DATA.gc : {records:[]};
  const records = gc.records || [];
  const M = records.length;

  // header
  const years = records.map(r=>r.year).filter(y=>typeof y==='number' && !isNaN(y));
  const yMin = years.length? Math.min.apply(null,years):null;
  const yMax = years.length? Math.max.apply(null,years):null;
  document.getElementById('sub').textContent =
    'Source: ' + (gc.source || 'General Comments') + ' · ' + M + ' paragraphs · ' +
    (yMin===null ? 'years unknown' : ('years ' + yMin + '–' + yMax));

  // committees
  const comSel = document.getElementById('committee');
  const coms = Array.from(new Set(records.map(r=>r.committee).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
  comSel.innerHTML = '<option value="All">All committees</option>' + coms.map(c=>'<option value="'+escHtml(c)+'">'+escHtml(c)+'</option>').join('');
```

Wait — option value with escHtml fine.

escHtml defined before use — order matters; define helpers first.

Search parsing:

```js
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
function tokenize(q){
  const toks=[]; const re=/"([^"]*)"|(\S+)/g; let m;
  while((m=re.exec(q))!==null){
    if(m[1]!==undefined){ const v=m[1].trim(); if(v) toks.push({value:v, quoted:true}); }
    else toks.push({value:m[2], quoted:false});
  }
  return toks;
}
function parseQuery(q){
  const toks=tokenize(q);
  const clauses=[]; let group=null; let neg=false; let lastOr=false;
  for(const t of toks){
    const v=t.value;
    if(!t.quoted && v==='AND'){ group=null; lastOr=false; neg=false; continue; }
    if(!t.quoted && v==='OR'){ if(!group){ group={neg:false,alts:[]}; clauses.push(group);} lastOr=true; neg=false; continue; }
    if(!t.quoted && v==='NOT'){ neg=true; continue; }
    const term={value:v, quoted:t.quoted, re:null};
    if(group && lastOr){ group.alts.push(term); }
    else { group={neg:neg, alts:[term]}; clauses.push(group); }
    lastOr=false; neg=false;
  }
  for(const cl of clauses) for(const a of cl.alts) a.re = termRegex(a);
  return clauses;
}
function termRegex(term){
  if(term.quoted){
    const words=term.value.split(/\s+/).filter(Boolean).map(escRe);
    if(!words.length) return null;
    return new RegExp('(?<![\\w])'+words.join('\\s+')+'(?![\\w])','gi');
  }
  return new RegExp('(?<![\\w])'+escRe(term.value)+'(?![\\w])','gi');
}
```

Hmm — quoted token value: I trimmed; but phrase "best interests" internal spaces preserved. Good. Note: quoted token could be `"AND"` — quoted so treated as phrase. Good, since I check `!t.quoted` for operators.

recordMatches:

```js
function recordMatches(rec, clauses){
  const text = rec.text || '';
  if(!text) return false;
  for(const cl of clauses){
    let any=false;
    for(const a of cl.alts){
      if(!a.re) continue;
      a.re.lastIndex=0;
      if(a.re.test(text)) any=true;
    }
    if(cl.neg ? any : !any) return false;
  }
  return true;
}
```

Wait: if cl.neg and any → return false (excluded). If !cl.neg and !any → return false. So `if(cl.neg ? any : !any) return false;` — correct.

Empty clauses → loop doesn't run → returns true (if text non-empty). Good.

Highlight ranges as planned.

renderResults:

```js
function renderResults(matched, clauses){
  const box=document.getElementById('results');
  if(!matched.length){
    box.innerHTML='<div class="panel nomatch"><strong>No paragraph contains these words.</strong><br>Tip: try OR instead of AND, or use fewer words.</div>';
    return;
  }
  const html=[];
  for(const rec of matched){
    const title = rec.short_title || rec.title || rec.symbol || '';
    const yearTxt = (rec.year===null||rec.year===undefined) ? 'year unknown' : String(rec.year);
    const sym = rec.symbol || '';
    const symHtml = (rec.doc_url ? '<a class="symbol" href="'+escAttr(rec.doc_url)+'" target="_blank" rel="noopener noreferrer">'+escHtml(sym)+'</a>' : '<span class="symbol">'+escHtml(sym)+'</span>');
    const paraLabel = (rec.paragraph===null||rec.paragraph===undefined) ? '' : 'para. '+rec.paragraph;
    const citation = (rec.symbol || rec.short_title || rec.title || '') + (rec.paragraph!=null ? ', para. '+rec.paragraph : '');
    const ranges = highlightRanges(rec.text||'', clauses);
    const body = renderHighlighted(rec.text||'', ranges);
    html.push('<article class="card">'+
      '<div class="card-head"><span class="committee">'+escHtml(rec.committee||'')+'</span>'+
      '<span class="gctitle">'+escHtml(title)+'</span>'+
      '<span class="year">'+escHtml(yearTxt)+'</span>'+ symHtml +'</div>'+
      '<p class="para">'+(paraLabel?'<span class="parano">'+escHtml(paraLabel)+'</span>':'')+'<span class="ptext">'+body+'</span></p>'+
      '<button class="copy" data-cite="'+escAttr(citation)+'">Copy citation</button>'+
      '</article>');
  }
  box.innerHTML=html.join('');
}
```

If text empty — can't happen in results (never matches). OK.

Copy delegation:

```js
document.getElementById('results').addEventListener('click', function(e){
  const btn=e.target.closest('.copy');
  if(!btn) return;
  const cite=btn.getAttribute('data-cite');
  copyText(cite).then(()=> {
    btn.textContent='Copied'; btn.classList.add('copied');
    clearTimeout(btn._t);
    btn._t=setTimeout(()=>{ btn.textContent='Copy citation'; btn.classList.remove('copied'); },2000);
  });
});
function copyText(t){
  if(navigator.clipboard && navigator.clipboard.writeText){ return navigator.clipboard.writeText(t).catch(()=>fallbackCopy(t)); }
  return Promise.resolve(fallbackCopy(t));
}
function fallbackCopy(t){
  const ta=document.createElement('textarea');
  ta.value=t; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.focus(); ta.select();
  try{ document.execCommand('copy'); }catch(e){}
  document.body.removeChild(ta);
}
```

Chart:

```js
let chart=null;
function renderChart(matched){
  const counts={};
  for(const r of matched){ const c=r.committee||'(no committee)'; counts[c]=(counts[c]||0)+1; }
  const entries=Object.keys(counts).map(k=>[k,counts[k]]).sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0]));
  const labels=entries.map(e=>e[0]), data=entries.map(e=>e[1]);
  const canvas=document.getElementById('chart');
  if(chart){ chart.destroy(); chart=null; }
  if(window.Chart){
    chart=new Chart(canvas.getContext('2d'), {
      type:'bar',
      data:{ labels:labels, datasets:[{ label:'Matching paragraphs', data:data, backgroundColor:'#1f6fb2', borderRadius:4 }]},
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false}, tooltip:{ callbacks:{ label:function(c){ return c.parsed.y + (c.parsed.y===1?' paragraph':' paragraphs'); } } } },
        scales:{ x:{ ticks:{ autoSkip:false } }, y:{ beginAtZero:true, ticks:{ precision:0 }, title:{ display:true, text:'Matching paragraphs' } } }
      }
    });
  }
}
```

Chartbox height: set CSS `#chartbox{height:240px;}` — with maintainAspectRatio:false, canvas fills. When empty data, still fine.

Count line:

```js
function renderCount(n, com, from, to, q){
  const parts=[];
  if(com!=='All') parts.push('committee = '+com);
  if(from!==''||to!=='') parts.push('years = '+(from||'…')+'–'+(to||'…'));
  if(q.trim()!=='') parts.push('search = "'+q.trim()+'"');
  const desc = parts.length? parts.join('; ') : 'none';
  document.getElementById('countline').textContent =
    n + (n===1?' paragraph matches':' paragraphs match') + ' out of ' + M + ', filters: ' + desc;
}
```

Spec: "N paragraphs match out of M, filters: …" — my singular variant is fine.

run():

```js
function run(){
  const q=document.getElementById('q').value;
  const clauses=parseQuery(q);
  const com=comSel.value;
  const from=document.getElementById('yfrom').value.trim();
  const to=document.getElementById('yto').value.trim();
  const matched=[];
  for(const rec of records){
    if(com!=='All' && rec.committee!==com) continue;
    if(!passesYear(rec, from, to)) continue;
    if(!recordMatches(rec, clauses)) continue;
    matched.push(rec);
  }
  matched.sort(function(a,b){
    const ya=(typeof a.year==='number')?a.year:-Infinity;
    const yb=(typeof b.year==='number')?b.year:-Infinity;
    if(yb!==ya) return yb-ya;
    const sa=a.symbol||'', sb=b.symbol||'';
    if(sa!==sb) return sa.localeCompare(sb);
    return (b.paragraph||0)-(a.paragraph||0);
  });
  renderCount(matched.length, com, from, to, q);
  renderChart(matched);
  renderResults(matched, clauses);
}
```

Events:

```js
document.getElementById('searchbtn').addEventListener('click', run);
document.getElementById('q').addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); run(); } });
comSel.addEventListener('change', run);
document.getElementById('yfrom').addEventListener('input', run);
document.getElementById('yto').addEventListener('input', run);
run();
```

passesYear as above.

highlightRanges + renderHighlighted + escHtml + escAttr.

escAttr: escape &, <, >, ".

Now assemble the document. Also add a small note under count: "How this is computed: the committee and year filters are applied first, then the word search runs on the paragraph text only (case-insensitive, whole words). All counting is done in your browser — nothing is estimated."

Chart note: "How this is computed: each matching paragraph is counted once, under its committee, for the current search and filters — the bars add up to the N in the count line above."

HTML skeleton:

```html
<div class="wrap">
  <h1>General Comments search</h1>
  <p class="sub" id="sub"></p>
  <div class="panel">
    <div class="searchrow">
      <input id="q" type="text" placeholder='Search paragraph text, e.g. "best interests" AND child' aria-label="Search paragraph text">
      <button class="btn" id="searchbtn">Search</button>
    </div>
    <p class="help">Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: <code>"best interests" AND child</code>.</p>
    <div class="filters">
      <div><label for="committee">Committee</label><select id="committee"></select></div>
      <div class="yearinputs"><label>Year (from–to)</label>
        <input id="yfrom" type="number" placeholder="from" aria-label="Year from">
        <span>–</span>
        <input id="yto" type="number" placeholder="to" aria-label="Year to">
      </div>
    </div>
  </div>
  <p id="countline"></p>
  <p class="note">How this is computed: ...</p>
  <div class="panel" id="chartpanel">
    <div id="chartbox"><canvas id="chart"></canvas></div>
    <p class="note">How this is computed: ...</p>
  </div>
  <div id="results"></div>
</div>
```

Number inputs: min could be set to yMin/yMax — optional; set min/max attributes dynamically? Nice touch: set yfrom.min=yMin etc. I'll set placeholder only, keep simple. Actually setting min/max helps; do it if yMin!==null.

Chart panel maybe hide when no matches? Keep visible with empty chart; the no-match message shows in results. Fine.

Check "no horizontal scrolling on laptop": max-width 920, flex-wrap. Good.

Font: system stack, base 16px. body font-size 16px.

One more consideration: `records` could be large (thousands). Rendering all cards each keystroke of year input — fine.

Potential issue: lookbehind regex `(?<![\w])` — supported in Chrome 62+, Firefox 78+, Safari 16.4+. Sandbox likely modern Chrome. Acceptable. But to be extra safe, I could avoid lookbehind using capture-group approach:

`new RegExp('(^|[^\\w])(' + pattern + ')(?=$|[^\\w])', 'gi')` and compute match start as m.index + m[1].length, length m[2].length. This works everywhere. Let me use this safer approach.

termRegex returns {re, adjust} or I store offset. Simpler: return object {re, off} where off = length of prefix group (1 if boundary group present). For phrase: pattern = words.join('\\s+'); re = `(^|[^\\w])(${pattern})(?=$|[^\\w])`. Match: start = m.index + m[1].length; end = start + m[2].length.

For single word: same with pattern=escRe(value).

Implement:

```js
function termRegex(term){
  let pat;
  if(term.quoted){
    const words=term.value.split(/\s+/).filter(Boolean).map(escRe);
    if(!words.length) return null;
    pat=words.join('\\s+');
  } else {
    pat=escRe(term.value);
  }
  return new RegExp('(^|[^\\w])('+pat+')(?=$|[^\\w])','gi');
}
```

Then in test: `re.lastIndex=0; const m=re.exec(text); any = !!m;` — test works since we just need boolean.

In highlight: 

```js
const m=re.exec(text);
const start=m.index+m[1].length;
ranges.push([start, start+m[2].length]);
```

Zero-length matches impossible since pat non-empty. Good.

Edge: word containing regex chars escaped. Word like "art." → escaped "art\." matches "art." literally with boundary after "." — `(?=$|[^\w])` after "." — "." is non-word so next char check: after "art." if next char is word char? e.g. "art.5"? boundary fails. Fine.

Now finalize. Also `code` styling for help example.

Let me also double check the "filters applied first, then search" — yes in run().

"N, the chart bars and the cards come from the same list" — yes, `matched`.

Sorting "newest General Comment first" — year desc. Good.

Write final answer: 1-3 short sentences before code block, then the html block, nothing after.

Let me count lines roughly — will be ~380 lines. Fine.

One more: title element and h1 "General Comments search". Sub line id="sub".

Also ensure `window.WORKSHOP_DATA.gc` exists — attached file guarantees it, but guard anyway.

Write it.