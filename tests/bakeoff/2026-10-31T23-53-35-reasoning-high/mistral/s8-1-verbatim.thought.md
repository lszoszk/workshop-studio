Let me plan this app. A search tool over WORKSHOP_DATA.gc (General Comments paragraphs).

Requirements:
- Search box supporting AND, OR, NOT and "exact phrases"
- Filters for committee and year
- Results show matching paragraph with search words highlighted, committee, GC short title, "Copy citation" button copying e.g. "CCPR/C/GC/37, para. 12"
- Number of hits per committee as small bar chart (Chart.js)
- Paragraph text exactly as in data
- Explain what's shown: title, description with source, n, years; "How this is computed" notes
- Every row shows symbol linked to doc_url in new tab
- Handle empty lists, missing values
- No external resources; Chart.js preloaded
- Under ~700 lines
- Base font 16px, accent #1f6fb2, light background, system fonts

Search query language: tokens. Support:
- "exact phrases" in quotes
- AND, OR, NOT (uppercase keywords presumably; maybe case-insensitive but safer to treat uppercase AND/OR/NOT as operators; also support lowercase? I'll treat case-insensitive operators but that could conflict with words "and"/"or" in text... Common approach: uppercase only. I'll accept both `AND`/`and`? Hmm. Safer: operators recognized when uppercase AND/OR/NOT, or when written as `+`? Keep simple: case-insensitive operators AND, OR, NOT, but only when standalone tokens. Actually "not" as a word appears in legal text rarely as standalone... "not" appears often in legal text ("is not"). If user types lowercase "not", treating it as operator would break. So: operators only when uppercase. Also support `-` prefix as NOT? The spec says supports AND, OR, NOT and "exact phrases". I'll implement: uppercase AND/OR/NOT as operators; also allow `AND`/`OR`/`NOT` case-insensitive? No — uppercase only, and document it. Also maybe support `&&`, `||`, `!`? Keep it simple but robust: parse tokens; quoted phrases; bare words are implicit AND (typical). Operators: AND, OR, NOT (uppercase). Also support lowercase? I'll document "use uppercase AND / OR / NOT". Also support `-word` as NOT shorthand maybe. I'll add: a leading `-` before a word or phrase means NOT. That's a nice touch.

Query semantics: default operator between terms is AND. Precedence: NOT > AND > OR. Evaluate as boolean expression over terms. Implementation: tokenize into terms (word or phrase) and operators. Build expression: split by OR at top level, then AND, then NOT prefixes. Simple recursive descent or shunting-yard. Simpler: parse into AST.

Tokenizer: regex to match quoted strings `"..."` (also curly quotes “ ”), or sequences of non-space chars. Then classify: if token is AND/OR/NOT (exact uppercase) → operator. If starts with `-` and length>1 → NOT term with rest (strip quotes if quoted after -). Else term.

Parser: 
```
parseOr: parseAnd (OR parseAnd)*
parseAnd: parseNot (AND? parseNot)*   // implicit AND when next token is a term or NOT
parseNot: NOT parseNot | term
```
Implicit AND: in parseAnd loop, if next token is a term or NOT, treat as AND.

Matching: for each record, text = record.text (maybe also title? Search over paragraph text primarily; maybe also title/short_title? The user says "search tool over the General Comments" — results show matching paragraph. I'll search in text only, but maybe include title too? Highlighting in paragraph text. I'll search text only to keep highlighting meaningful; mention in "how computed". Actually searching title too could be useful but highlighting only in text. Keep text-only, note it.)

Term matching: case-insensitive. For a word term: match if the word appears as substring? Or whole word? Substring matching gives more hits (e.g., "discrimin" matches "discrimination"). I'll do substring match on lowercased text, but for highlighting we need to find occurrences. For phrase: substring match of the phrase (normalized whitespace). Highlighting: find all occurrences of each matched term (case-insensitive, escape regex) in the text and wrap in <mark>. For NOT terms, don't highlight. For OR groups, highlight all positive terms that matched... Simpler: highlight all positive terms (those not under NOT) that appear in the text. Actually highlight terms that contributed to match — for OR, only the ones present. I'll collect the set of positive terms whose regex matches the text, highlight those.

Word boundary: substring could highlight inside words. Use regex with boundaries? For legal text, substring is fine but "art" would match "article", "part". Hmm. Maybe use word-boundary matching for single words: `\bword\b` with escaped chars. That's more precise. But then "torture" matches "tortures"? \b handles prefix: "torture" won't match "tortured" with \b...\b. Could use `\bword\w*`? That matches prefix. I'll do: single word terms match with prefix allowed? Let's keep it simple and predictable: match whole word boundaries `\b(?:term)\b` for words, and for phrases, allow the phrase as-is with flexible whitespace. Hmm, but users often want stem search. I'll offer a checkbox "match word stems (prefix)"? That adds complexity. Keep: word-boundary match, case-insensitive. Document it in help. Actually, let me do substring matching but highlight with word boundaries... inconsistent. Decision: terms match as substrings (case-insensitive) — simple, documented: "matches anywhere in the text, case-insensitive; use quotes for exact phrases". Highlighting uses the same substring. That's consistent and honest. But "art" matching "heart" is ugly. Compromise: default word-boundary for unquoted single words, substring for quoted phrases? Phrases with spaces naturally boundary-ish. Hmm, phrase "article 3" substring is fine. Single word "torture" with \b won't match "tortured". I think word-boundary is better UX for a search tool. But then "discrimination" won't find "discriminatory". Add a note. Alternatively make word terms match with `\b` on left and allow trailing word chars: `term\w*` — prefix search. "torture" matches "tortured", "tortures". "art" matches "article" — bad. Ugh.

I'll go with: unquoted words match whole words (case-insensitive, Unicode-ish via regex escape, using lookarounds `(?<![\p{L}\p{N}])term(?![\p{L}\p{N}])` with 'u' flag). Quoted phrases match the exact sequence of characters (case-insensitive, whitespace-flexible: replace whitespace runs in phrase with \s+). Document both. That's clean and defensible.

Highlighting: build a combined regex from all positive matched terms, global, case-insensitive, 'u', and replace in escaped HTML text with <mark>. Careful: escape HTML first, then run regex on escaped text? Escaping changes characters (& → &amp;) which could break phrase matching across "&". Better: run regex on raw text, split into segments, escape each segment, wrap matches in <mark>. Implement: collect matches via matchAll on raw text with combined regex, then build HTML by slicing.

Combined regex: alternation of term patterns sorted by length desc to prefer longer matches (phrases first). Use `g` flag. For word terms: `(?<![\p{L}\p{N}_])` + escaped + `(?![\p{L}\p{N}_])`. For phrases: escaped with \s+ between words. Note: lookbehind support is fine in modern browsers.

Edge: overlapping matches — matchAll with alternation handles leftmost-longest? JS regex alternation is leftmost-first, so sort alternatives by length descending so phrases win over words at same position.

Filters: committee select (populated from data, sorted, with counts), year select (populated from data years sorted desc, "All years"). Also maybe a year range? Keep single select "All years" + each year. Or two selects from/to. Single select is fine; maybe better: min year and max year selects. I'll do a single "Year" dropdown with All + years — simple. Hmm, "Filters for committee and year" — a dropdown each is fine. Maybe committee multi-select? Single select with "All committees" plus each. Could do multi via checkboxes... Keep dropdowns, plus show counts.

Also maybe filter by cited article? Not requested. Skip.

Results: list of records, each showing:
- symbol link (doc_url, new tab) + "para. N" 
- committee badge, year
- short_title (GC title) — maybe full title on expand
- highlighted paragraph text (exact)
- "Copy citation" button: copies `${symbol}, para. ${paragraph}` — e.g. "CCPR/C/GC/37, para. 12". Use navigator.clipboard.writeText with fallback (execCommand). Show "Copied!" feedback.
- Expandable full text? The text is shown in full already (highlighted). "Keep the full text of a paragraph available (click to expand)" — since we show full text, fine. Maybe truncate very long paragraphs with click to expand? Rule says keep full text available via click-to-expand; showing full is also fine. I'll show full text but if longer than ~1200 chars, collapse with "Show full paragraph" toggle. Simpler: always show full. Paragraphs can be long but that's OK. I'll add collapse for >900 chars to keep list scannable, with expand button — satisfies "click to expand".

Sorting results: by committee, year desc, paragraph? Or by relevance (number of matched terms)? Sort by year desc then committee then paragraph seems natural. Maybe relevance sort option. Keep: sort by year (newest first), then committee, then paragraph. Add a select for sort: "Newest first", "Oldest first", "Most matches". Nice but optional; I'll include relevance count maybe. Keep simple: sort select with Newest / Oldest / Committee A–Z. Eh, I'll do Newest first default, plus "Most search-term matches" option. Fine.

Chart: hits per committee — small bar chart (Chart.js horizontal bar). Update on search/filter. Show counts. "How this is computed" note: "Counts paragraphs in WORKSHOP_DATA.gc whose text matches the current query and filters."

Header: title "General Comments search", description: source (WORKSHOP_DATA.gc.source), n records, years range computed from data. E.g. "Source: {source} · {count} paragraphs from {n} General Comments · years {min}–{max}". Compute from data, handle empty.

Query help: a small help text under search box: `AND`, `OR`, `NOT` (uppercase), `"exact phrase"`, `-word` excludes, multiple words = AND. Also example queries as clickable chips: e.g. `"torture" NOT "article 7"`, `children OR adolescents`, etc. But examples must not invent data — they're just queries, fine. Use generic examples like `"freedom of expression"`, `discrimination AND women`, `NOT reservations`. Clicking fills the box and runs.

Parse errors: unbalanced quotes → treat rest as phrase? Show a warning message "Unbalanced quote — treating the rest as a phrase" or just handle gracefully. I'll detect and show a gentle note, still search.

Empty query: show all (subject to filters)? Or show nothing with prompt "Type a query". I'll show all records when query empty (with note "no query — showing all paragraphs matching filters"), chart shows distribution. That's useful. Limit displayed results? Data could be large (thousands of paragraphs). Rendering thousands of rows with highlights could be slow. Add pagination / "show first 100" with a "Show more" button. I'll render in chunks of 100 with a button, and note "Showing X of Y hits". Good for performance.

Copy citation: clipboard API may fail in sandbox (permissions). Fallback: create textarea, execCommand('copy'). Show feedback "Copied" or "Copy failed — citation: ...". Also make the citation text selectable.

Chart.js: bar chart, labels = committees with hits (only those with >0? or all committees in filter scope). Show committees with hits > 0, sorted desc. Horizontal bar (indexAxis: 'y'). Small height. Colors accent #1f6fb2. Update via chart.data update + chart.update(). Handle chart creation once, update on changes. If zero hits, show "No hits" message and clear chart.

Also maybe a second small chart? Not needed.

Committee filter: dropdown listing all committees present in data with counts (of all records, or of current query hits?). Show counts of total paragraphs per committee in the option label: "CAT (123)". Year filter: dropdown of years desc with counts.

Also show "n hits" prominently: "X of Y paragraphs match".

Layout: header, controls card (search input, help, examples, filters row, sort), stats line, chart, results list. Footer note about data source.

Accessibility: labels for inputs.

Now data specifics: WORKSHOP_DATA.gc = {title, source, count, records: [...]}. Fields: id, symbol, paragraph, committee, year, title, short_title, doc_url, text, cited_articles. Handle missing: text may be missing → use "" and skip? If text missing, treat as empty string; still list? I'll treat missing text as "" (won't match queries but shows in unfiltered list with "(no text)").

Citation format: `${symbol}, para. ${paragraph}`. Example given "CCPR/C/GC/37, para. 12". Good.

Highlight in text only. Also maybe highlight in title? No.

Let me also consider searching across title too — user said "search tool over the treaty bodies' General Comments" and "Results show the matching paragraph with the search words highlighted". Searching text only is fine; but a query like "racial discrimination" would match titles too... I'll search text only and state it: "Search matches the paragraph text (case-insensitive)". Hmm, maybe include short_title in matching but highlight only text? That could confuse ("why does it match?"). Text only. State it.

Now write the code.

Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments search — ...</title>
<style>...</style>
</head>
<body>
<header>...</header>
<main>
  <section class="controls">...</section>
  <section class="stats">...</section>
  <section class="chart-card"><canvas id="committeeChart"></canvas><p class="note">...</p></section>
  <section class="results">...</section>
</main>
<script>
const DATA = window.WORKSHOP_DATA.gc;
// helpers: esc, el
// tokenizer/parser
// matching
// render filters, chart, results
</script>
</body>
</html>
```

CSS: system font stack, background #f5f7fa, cards white, accent #1f6fb2, base 16px, max-width ~1000px, mark highlight background #ffe08a or accent-tinted. Buttons accent. mark { background: #ffd766; padding: 0 1px; border-radius: 2px; }.

Tokenizer:

```js
function tokenize(q){
  const tokens = [];
  const re = /"([^"]*)"|“([^”]*)”|(\S+)/g;
  let m, unbalanced = false;
  while ((m = re.exec(q)) !== null){
    if (m[1] !== undefined) tokens.push({type:'phrase', value:m[1]});
    else if (m[2] !== undefined) tokens.push({type:'phrase', value:m[2]});
    else {
      const raw = m[3];
      if (raw === 'AND' || raw === 'OR' || raw === 'NOT') tokens.push({type:'op', value: raw});
      else if (raw.startsWith('-') && raw.length > 1){
        let v = raw.slice(1);
        // maybe -"phrase"? handle -"...": the regex would have matched the quote separately... 
        tokens.push({type:'not', value: v});
      } else tokens.push({type:'term', value: raw});
    }
  }
  // unbalanced quote: if odd number of straight quotes, the regex "([^"]*)" won't match the last one; \S+ will grab `"foo` including quote. Handle: strip leading/trailing quotes from term values.
  return tokens;
}
```

Hmm, unbalanced quote: `"torture` → \S+ matches `"torture`. I'll clean: if a term starts with `"` and no closing, treat rest as phrase and set unbalanced flag. Let me handle in tokenizer: after building, check raw count of `"` — if odd, note. Simpler: in the \S+ branch, if raw starts with `"` or `“`, strip it and mark phrase with unbalanced warning. Also trailing quote: `torture"` → strip trailing quote, phrase. I'll do a cleanup pass.

Also `-"exact phrase"`: regex alternation: `"..."` matches first if the quote comes after `-`? The string `-"torture"` — at position 0, `"([^"]*)"` doesn't match (starts with -), so \S+ matches `-"torture"` entirely. Then in branch: starts with '-', value = `"torture"` → strip quotes → phrase NOT. Handle: after slicing '-', if value starts and ends with quote, make phrase. OK.

Parser:

```js
function parse(tokens){
  let pos = 0;
  function peek(){ return tokens[pos]; }
  function parseOr(){
    let left = parseAnd();
    while (peek() && peek().type==='op' && peek().value==='OR'){
      pos++;
      const right = parseAnd();
      left = {kind:'or', children:[left, right]};
    }
    return left;
  }
  function parseAnd(){
    let left = parseNot();
    while (peek() && (peek().type==='term' || peek().type==='phrase' || peek().type==='not' || (peek().type==='op' && peek().value==='AND'))){
      if (peek().type==='op' && peek().value==='AND') pos++;
      const right = parseNot();
      left = {kind:'and', children:[left, right]};
    }
    return left;
  }
  function parseNot(){
    const t = peek();
    if (t && ((t.type==='op' && t.value==='NOT') || t.type==='not')){
      pos++;
      return {kind:'not', child: parseNot()};
    }
    if (t && (t.type==='term' || t.type==='phrase')){
      pos++;
      return {kind:'term', value: t.value, phrase: t.type==='phrase'};
    }
    return null; // unexpected operator
  }
  const ast = parseOr();
  return ast;
}
```

Edge: trailing operator like "torture AND" → parseAnd: after AND, parseNot returns null → children include null. Handle null: treat as... In parseAnd loop, if right is null, break and maybe set error flag "dangling operator". I'll guard: if parseNot returns null, stop and record warning. Also leading OR: parseOr → parseAnd → parseNot null → left null; then while sees OR... left null. Guard: if left null and next is OR, skip. I'll add checks: in loops, if child null, break. And final: if ast null → no match (or treat as match-all?). If query is only operators, show warning "query has no search terms". I'll set a warnings array.

Evaluation:

```js
function termRegex(term){
  const esc = term.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (term.phrase){
    const parts = esc.split(/\s+/).filter(Boolean);
    return parts.join('\\s+');
  }
  return `(?<![\\p{L}\\p{N}_])${esc}(?![\\p{L}\\p{N}_])`;
}
```

Wait: for phrase, escaping then splitting on \s+ — escaped string may contain `\s`? No, escape only escapes special chars; spaces remain spaces. But if phrase contains regex-special like `.` it becomes `\.` — fine, split on whitespace still works since `\.` has no space. OK.

Build regex per term with flags 'giu'. Evaluate:

```js
function evalAst(node, text){
  if (!node) return false;
  switch(node.kind){
    case 'term': return node.re.test(text); // careful with lastIndex with g flag — use fresh regex or reset
    ...
  }
}
```

Use non-global regex for testing (test with g flag has lastIndex issues). Create two regexes: one global for highlight, one non-global for test. Or use `text.search(re)` / `re.test` with lastIndex reset. I'll store `reTest` (no g) and `reGlobal` (g) per term.

Collect positive terms for highlighting: walk AST, collect terms not under a 'not'. Then for each, if reGlobal matches text, add its source pattern to highlight alternation. Actually simpler: highlight every positive term that appears in the text (regardless of whether it was needed for the match — e.g., in OR, both present get highlighted; that's fine and even desirable).

Highlight builder:

```js
function highlight(text, patterns){
  if (!patterns.length) return esc(text);
  const combined = new RegExp(patterns.map(p => `(?:${p})`).join('|'), 'giu');
  let out = '', last = 0, m;
  combined.lastIndex = 0;
  while ((m = combined.exec(text)) !== null){
    if (m[0].length === 0){ combined.lastIndex++; continue; }
    out += esc(text.slice(last, m.index)) + '<mark>' + esc(m[0]) + '</mark>';
    last = m.index + m[0].length;
  }
  out += esc(text.slice(last));
  return out;
}
```

Sort patterns by length desc so longer phrases match first at same position.

Matching pipeline:

```js
function runSearch(){
  const q = input.value.trim();
  const ast = q ? parse(tokenize(q)) : null;
  const committee = committeeSel.value; // '' = all
  const year = yearSel.value; // '' = all
  const results = [];
  for (const r of records){
    if (committee && r.committee !== committee) continue;
    if (year && String(r.year) !== year) continue;
    if (ast){
      const text = (r.text || '').toLowerCase(); // regex has 'i' flag anyway; use raw
      if (!evalAst(ast, r.text || '')) continue;
    }
    results.push(r);
  }
  ...
}
```

evalAst with text raw (regex 'i' handles case). For NOT terms, no highlight.

Collect positive patterns:

```js
function collectTerms(node, out, negated){
  if (!node) return;
  if (node.kind==='not'){ collectTerms(node.child, out, true); return; }
  if (node.kind==='term'){ node.negated = negated; if(!negated) out.push(node); return; }
  node.children.forEach(c => collectTerms(c, out, negated));
}
```

Then per result, patterns = positiveTerms.filter(t => t.reTest.test(text)).map(t => t.pattern).

Performance: records maybe a few thousand; per record eval is cheap. Fine.

Sort: 
- 'newest': year desc, then committee asc, paragraph asc
- 'oldest': year asc...
- 'relevance': count of distinct positive terms matched desc, then year desc. Compute matches count per result.

Rendering results: chunked. `visibleCount` starts 100, "Show more (X remaining)" button. Each result card:

```html
<article class="result">
  <div class="result-head">
    <a class="symbol" href="doc_url" target="_blank" rel="noopener">symbol</a>
    <span class="para">para. N</span>
    <span class="badge">COMMITTEE</span>
    <span class="year">2011</span>
    <button class="copy" data-cite="...">Copy citation</button>
  </div>
  <div class="gc-title">short_title — full title?</div>
  <p class="text">highlighted text</p>
  <div class="cite-line">Citation: <code>symbol, para. N</code></div>
</article>
```

Show short_title prominently and title smaller? The requirement: "the committee, the General Comment's short title". Show short_title; maybe full title as secondary line. I'll show short_title as the GC name, and full title in a smaller muted line (or title attribute). I'll include full title in small text — it's data, fine.

Copy button: copies citation string. Feedback: change text to "Copied ✓" for 1.5s. Use async clipboard with fallback.

```js
async function copyText(t, btn){
  try { await navigator.clipboard.writeText(t); ok(btn); }
  catch(e){
    const ta = document.createElement('textarea');
    ta.value = t; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.select();
    let okFlag = false;
    try { okFlag = document.execCommand('copy'); } catch(_){}
    ta.remove();
    if (okFlag) ok(btn); else { btn.textContent = 'Select & copy: ' + t; ... }
  }
}
```

Fallback message: show the citation in a prompt? Better: on failure, show inline "Could not access clipboard — citation: X" (selectable). I'll set button text to "Copy failed" and reveal a small line with the citation in a <code> that user can select. Simpler: always render the citation in a <code> element next to the button (visible), so even if copy fails the user sees it. Good — "Copy citation" button + visible citation text.

Chart: 

```js
let chart;
function renderChart(counts){
  const labels = Object.keys(counts).sort((a,b)=>counts[b]-counts[a]);
  const data = labels.map(l=>counts[l]);
  if (!chart){
    chart = new Chart(ctx, {type:'bar', data:{labels, datasets:[{data, backgroundColor:'#1f6fb2', ...}]}, options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}, tooltip:{callbacks:{label: c=>` ${c.parsed.x} paragraph(s)`}}}, scales:{x:{beginAtZero:true, ticks:{precision:0}, title:{display:true, text:'matching paragraphs'}}, y:{ticks:{autoSkip:false}}}}});
  } else {
    chart.data.labels = labels; chart.data.datasets[0].data = data; chart.update();
  }
}
```

Container height: set canvas wrapper height based on number of bars: e.g., `Math.max(120, labels.length*28+40)` px, since maintainAspectRatio false. Update wrapper height on update.

Only include committees with count>0 in chart. If none, show message.

Filters population:

```js
const committees = [...new Set(records.map(r=>r.committee).filter(Boolean))].sort();
const years = [...new Set(records.map(r=>r.year).filter(y=>y!=null))].sort((a,b)=>b-a);
```

Option labels: `${c} (${countAll})`. Year: `${y} (${n})`.

Header description: compute from data: `const yearsAll = records.map(r=>r.year).filter(...); min/max`. Text: `Source: ${DATA.source || 'WORKSHOP_DATA.gc'} · ${records.length} paragraphs · ${gcCount} General Comments · years ${min}–${max}`. gcCount = distinct symbols. Title of dataset: DATA.title. Show: `<h1>General Comments search</h1><p class="lede">${DATA.title}. Source: ...</p>`. Handle missing gracefully.

"How this is computed" notes:
- Under search controls: "How the search works: ... terms match whole words, case-insensitive; "..." exact phrase; AND/OR/NOT uppercase; -word excludes; empty query shows everything. Search runs over the paragraph text only."
- Under chart: "Hits per committee: number of paragraphs matching the current query and filters, counted by this page from WORKSHOP_DATA.gc."
- Under results: "Each row shows the paragraph exactly as in the source document; matching words are highlighted. n = X of Y paragraphs."

Also note about roll-call? Not relevant here.

Empty data handling: if !records || records.length===0 → show message "No General Comment paragraphs in the data."

Debounce input: run on 'input' with small debounce (150ms) — fine, deterministic. Or run on Enter + button. I'll do live with debounce 200ms plus a "Search" button (for accessibility). Also form submit prevent default.

Example chips: 
- `"torture"` 
- `discrimination AND women`
- `children OR adolescents`
- `"freedom of" NOT detention`
Set input value and run.

Careful: examples are queries, not data claims — fine.

Now line count: aim ~600 lines. Let me write it.

CSS details:

```css
:root{ --accent:#1f6fb2; --ink:#1c2733; --muted:#5b6b7b; --bg:#f4f6f9; --card:#fff; --line:#dde4ec; }
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--bg)}
.wrap{max-width:1040px;margin:0 auto;padding:24px 20px 64px}
header.top{...}
h1{font-size:1.6rem;margin:0 0 6px}
.lede{color:var(--muted);margin:0 0 4px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:16px 0}
.search-row{display:flex;gap:10px;flex-wrap:wrap}
#q{flex:1;min-width:260px;font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:8px}
button, .btn{font:inherit;cursor:pointer}
.btn-primary{background:var(--accent);color:#fff;border:none;border-radius:8px;padding:10px 16px}
.btn-primary:hover{background:#185a92}
select{font:inherit;padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:#fff}
.help{font-size:.9rem;color:var(--muted)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.chip{border:1px solid var(--line);background:#eef4fa;color:var(--accent);border-radius:999px;padding:4px 12px;font-size:.9rem}
.note{font-size:.85rem;color:var(--muted);margin:8px 0 0}
mark{background:#ffe9a8;border-radius:2px;padding:0 1px}
.result{border:1px solid var(--line);border-radius:10px;background:#fff;padding:14px 16px;margin:12px 0}
...
```

Result head: flex wrap, symbol link accent bold, badges.

Committee badge: small pill with accent-tinted bg.

Copy button: secondary style (outline accent).

Collapsed long text: if text length > 900, render first 900 chars + "… " + button "Show full paragraph". Implement: store full highlighted HTML; if long, show truncated version (truncate at word boundary) with toggle. Simpler: render full but add class 'clamped' with max-height and overflow hidden + "Show more" overlay button? CSS line-clamp: `-webkit-line-clamp: 6` etc. Use a details/summary? Simplest robust: if len>900, wrap in div with class collapsed (max-height: 9em; overflow:hidden) and a button toggles. Highlighted HTML computed once; store in dataset or closure. I'll build DOM via createElement to avoid innerHTML injection issues... text is data, must escape — I'm escaping in highlight(). Using innerHTML with escaped content is OK. I'll construct with innerHTML on a container since all dynamic parts are escaped (symbol, titles via esc()).

Let me write renderResult(r, patterns):

```js
function resultEl(r, patterns){
  const art = document.createElement('article');
  art.className = 'result';
  const cite = `${r.symbol || '(no symbol)'}, para. ${r.paragraph ?? '?'}`;
  const head = document.createElement('div'); head.className='rhead';
  // symbol link
  if (r.doc_url){ a.href=r.doc_url; a.target='_blank'; a.rel='noopener noreferrer'; }
  else a as span.
  ...
}
```

Copy handler: event delegation on results container for `.copy-btn` with data-cite.

Chart card includes note. Stats line: `<p id="stats">` with strong number.

Also show active filters summary in stats: "X of Y paragraphs match · query: ... · committee: All · year: All".

Now, the "How this is computed" for the search: include in help details element:

```html
<details class="howto"><summary>How the search works</summary>
<ul>
<li>Each word matches whole words in the paragraph text, ignoring case (e.g. <code>torture</code> matches “torture” but not “tortured”).</li>
<li>Use <code>"…"</code> for an exact phrase, e.g. <code>"substantial grounds"</code>.</li>
<li>Separate words with spaces = AND. Use uppercase <code>AND</code>, <code>OR</code>, <code>NOT</code> (or a leading <code>-</code>) to combine, e.g. <code>children OR adolescents</code>, <code>discrimination NOT reservations</code>.</li>
<li>Only the paragraph text is searched, not the titles. The full paragraph is shown exactly as in the source; matches are highlighted.</li>
</ul></details>
```

Wait — I said word matches whole word so "torture" doesn't match "tortured". That's a limitation; document it. Alternatively allow prefix matching... I'll keep whole-word and document. Hmm, users may find it limiting but it's predictable. Actually, let me reconsider: substring matching is what most people expect from Ctrl+F. But then "art" highlights inside "heart". Whole-word is better for precision. Keep whole-word, documented clearly. Maybe add a checkbox "Match word beginnings (stems)" — adds complexity but nice. I'll skip; keep clean. Actually... let me add it as a small checkbox "prefix match (e.g. tortur* matches tortured)"? It's easy: if checked, word pattern becomes `(?<![\p{L}\p{N}_])term` without trailing boundary... that makes "art" match "article". Hmm, that's the tradeoff. I'll skip the checkbox — whole-word only, documented. Fine.

Year filter: also maybe a text input for year? Dropdown is fine.

Now the header description: "one-line description of the data (source, n, years)". Compute:

```js
const recs = (DATA && Array.isArray(DATA.records)) ? DATA.records : [];
const years = recs.map(r=>r.year).filter(y=>typeof y==='number');
const minY = years.length? Math.min(...years): null;
const maxY = years.length? Math.max(...years): null;
const gcCount = new Set(recs.map(r=>r.symbol).filter(Boolean)).size;
lede.textContent = `${DATA.title || 'General Comments'} — source: ${DATA.source || 'WORKSHOP_DATA.gc'} · ${recs.length} paragraphs from ${gcCount} documents · years ${minY ?? '–'}–${maxY ?? '–'}`;
```

DATA.count may exist; use recs.length (actual) and mention DATA.count if differs? Just use recs.length; note "n = paragraphs loaded". Fine.

Chart note: "How this is computed: for each committee, the number of result rows above (paragraphs in WORKSHOP_DATA.gc whose text matches the current query and the committee/year filters). Counted by this page, not estimated."

Results note similar.

Now write everything carefully. Also handle `paragraph` missing → citation "para. ?" — better: if paragraph missing, omit "para." part: cite = symbol + (paragraph!=null ? `, para. ${paragraph}` : ''). 

Sort select options: newest, oldest, relevance. Relevance: number of distinct positive terms present in text (desc), tie → year desc.

Let me now also think about the tokenizer cleanup for unbalanced quotes. Approach: pre-scan: count straight double quotes; if odd, set warning "unbalanced quote". In \S+ branch: strip leading `"`/`“` and trailing `"`/`”` from raw; if after stripping it contains quote chars... keep simple: 

```js
else {
  let raw = m[3];
  let phrase = false;
  if (/^["“]/.test(raw)){ raw = raw.replace(/^["“]/, ''); phrase = true; }
  if (/["”]$/.test(raw)){ raw = raw.replace(/["”]$/, ''); phrase = true; }
  if (!raw) continue;
  if (raw==='AND'||raw==='OR'||raw==='NOT'){ tokens.push({type:'op',value:raw}); }
  else if (raw.startsWith('-') && raw.length>1){
    let v = raw.slice(1);
    if (/^["“]/.test(v) && /["”]$/.test(v) && v.length>2){ v = v.slice(1,-1); tokens.push({type:'not', value:v, phrase:true}); }
    else tokens.push({type:'not', value:v, phrase: phrase && v.includes(' ')});
  } else tokens.push({type: phrase ? 'phrase':'term', value: raw});
}
```

Hmm getting messy. Simplify: handle `-` prefix first, then quote stripping:

```js
function cleanTerm(raw){
  let neg = false;
  if (raw.startsWith('-') && raw.length>1){ neg = true; raw = raw.slice(1); }
  let phrase = false;
  if (raw.length>1 && raw.startsWith('"') && raw.endsWith('"')){ raw = raw.slice(1,-1); phrase = true; }
  else if (raw.startsWith('"')){ raw = raw.slice(1); phrase = true; } // unbalanced
  else if (raw.endsWith('"')){ raw = raw.slice(0,-1); phrase = true; }
  return {neg, phrase, value: raw};
}
```

But the tokenizer regex already captures quoted strings as phrases when balanced. The \S+ branch only sees unbalanced or plain. Also `-"foo bar"` — \S+ won't match because of space; regex alternation: at `-`, `"..."` doesn't match at that position... Actually regex scans: at index of `-`, tries `"([^"]*)"` — fails (char is -), tries `\S+` — matches `-"foo` (up to space). Then next match `"bar"` as phrase. Messy. To handle `-"phrase with spaces"`, better tokenizer: first extract quoted segments with positions, then split the rest. Alternative simpler tokenizer: manual scan:

```js
function tokenize(q){
  const tokens = []; let i = 0; const n = q.length;
  while (i < n){
    const c = q[i];
    if (/\s/.test(c)){ i++; continue; }
    if (c === '"' || c === '“'){
      const close = c === '"' ? '"' : '”';
      let j = q.indexOf(close, i+1);
      let unbal = false;
      if (j === -1){ j = n; unbal = true; }
      const val = q.slice(i+1, j);
      tokens.push({type:'phrase', value: val, unbal});
      i = j+1;
      continue;
    }
    // read a bare word up to whitespace or quote
    let j = i;
    while (j < n && !/\s/.test(q[j]) && q[j] !== '"' && q[j] !== '“') j++;
    const raw = q.slice(i, j);
    // handle -prefix
    ...
    i = j;
  }
}
```

But `-"foo bar"`: at `-`, bare word reads `-` (stops at quote). Then next iteration sees `"` → phrase. So `-` becomes its own token. Handle: if raw === '-' and next char is quote → treat as NOT marker pending. I'll handle: when raw is exactly '-', set pendingNot = true and continue; next token (phrase or word) gets negated. Also raw like `-word` → neg word. Also `NOT` op. OK:

```js
let pendingNot = false;
...
if (raw === '-'){ pendingNot = true; i = j; continue; }
let neg = pendingNot; pendingNot = false;
if (raw.startsWith('-')){ neg = true; raw = raw.slice(1); }
if (!raw) continue;
if (!neg && (raw==='AND'||raw==='OR'||raw==='NOT')){ tokens.push({type:'op', value:raw}); continue; }
if (neg && (raw==='AND'||raw==='OR'||raw==='NOT')){ // "-AND" weird; treat as term? just push as not-term
}
tokens.push(neg ? {type:'not', value:raw} : {type:'term', value:raw});
```

And phrase tokens: if pendingNot, convert to {type:'not', value, phrase:true}. Also phrase followed... fine.

Also lowercase 'and'/'or'/'not' treated as literal words — document "operators must be uppercase". Good.

Parser handles 'not' token type and 'NOT' op.

Warnings: unbalanced quotes → note. Dangling operators → note "ignored trailing operator". Empty query → ast null → match all.

Now eval with regex caching: build term objects with `pattern` (source string), `reTest` = new RegExp(pattern, 'iu'), `reG` = new RegExp(pattern, 'giu'). Note 'u' flag with lookbehind ok.

Pattern for word: `(?<![\\p{L}\\p{N}_])${esc}(?![\\p{L}\\p{N}_])`. Hmm underscore: treat `_` as word char so "art_3" doesn't match "art"? Fine include _.

Phrase pattern: escape each word, join with `\\s+`: `esc.split(/\\s+/).join('\\s+')` — but esc may contain `\\s`? No. However escaping turns nothing into whitespace. But careful: phrase "a  b" (double space) → split/filter → join single \s+ — good (flexible whitespace).

Also phrase could contain quotes? No, quotes delimit.

Highlight patterns: for each positive term present, push its pattern. Sort by pattern length desc. Combined regex `(?:p1)|(?:p2)` with 'giu'. Note: patterns contain lookarounds — alternation fine.

One catch: `matchAll`/exec with 'g' and lookbehind — fine.

Relevance count: positive terms present count.

Now the chart: committees with hits. Also maybe show all committees even 0? Only >0 keeps chart small. Note says "committees with at least one hit".

Let me now also handle the case where Chart is unavailable (window.Chart undefined) — guard: if no Chart, render a simple HTML bar list instead. Good robustness. I'll implement fallback: if (!window.Chart) render divs with widths. Keep it small.

Actually to keep code lean, I could skip fallback... but sandbox says Chart.js preloaded; still guard cheaply: `if (window.Chart) {...} else { fallback list }`. I'll include a minimal fallback.

Copy citation: citation string e.g. `CCPR/C/GC/37, para. 12`. Button label "Copy citation". On success: text "Copied ✓" revert after 1600ms.

Show citation text in <code class="cite"> next to button so it's visible/selectable.

Now results header: "Results — X of Y paragraphs" plus sort select and show-more.

Let me write the final HTML now, carefully, keeping under 700 lines.

Also title of page: "General Comments search · [source]". Set document.title maybe.

Let me draft the JS fully:

```js
(function(){
  'use strict';
  const DATA = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc) || {};
  const recs = Array.isArray(DATA.records) ? DATA.records : [];
  const $ = s => document.querySelector(s);

  const qInput = $('#q'), committeeSel = $('#committee'), yearSel = $('#year'), sortSel = $('#sort');
  const statsEl = $('#stats'), listEl = $('#results'), moreBtn = $('#more'), chartNote = $('#chartNote');
  const warnEl = $('#warn');

  // ---------- header ----------
  (function header(){
    const years = recs.map(r=>r.year).filter(y=>typeof y==='number' && !isNaN(y));
    const min = years.length ? Math.min.apply(null, years) : null;
    const max = years.length ? Math.max.apply(null, years) : null;
    const docs = new Set(recs.map(r=>r.symbol).filter(Boolean)).size;
    $('#lede').textContent = (DATA.title ? DATA.title + ' — ' : '') +
      'source: ' + (DATA.source || 'WORKSHOP_DATA.gc') +
      ' · ' + recs.length + ' paragraphs from ' + docs + ' documents' +
      (min!==null ? ' · years ' + min + '–' + max : '');
  })();
```

Hmm "one-line description of the data (source, n, years)". Good.

Filters:

```js
  function fillFilters(){
    const commCount = {}, yearCount = {};
    recs.forEach(r=>{
      if (r.committee) commCount[r.committee] = (commCount[r.committee]||0)+1;
      if (typeof r.year==='number') yearCount[r.year] = (yearCount[r.year]||0)+1;
    });
    const comms = Object.keys(commCount).sort((a,b)=> commCount[b]-commCount[a] || a.localeCompare(b));
    committeeSel.innerHTML = '<option value="">All committees (' + recs.length + ')</option>' +
      comms.map(c=>'<option value="'+esc(c)+'">'+esc(c)+' ('+commCount[c]+')</option>').join('');
    const ys = Object.keys(yearCount).map(Number).sort((a,b)=>b-a);
    yearSel.innerHTML = '<option value="">All years</option>' +
      ys.map(y=>'<option value="'+y+'">'+y+' ('+yearCount[y]+')</option>').join('');
  }
```

esc for attribute values — esc handles &<>"'.

Tokenizer/parser/eval as planned.

```js
  function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

  function tokenize(q){
    const tokens=[]; let i=0; const n=q.length; let pendingNot=false; let unbal=false;
    while(i<n){
      const c=q[i];
      if(/\s/.test(c)){ i++; continue; }
      if(c==='"'||c==='\u201C'){
        const close = c==='"' ? '"' : '\u201D';
        let j=q.indexOf(close, i+1);
        if(j===-1){ j=n; unbal=true; }
        const val=q.slice(i+1,j);
        if(val.trim()===''){ i=j+1; continue; }
        tokens.push(pendingNot?{type:'not',value:val,phrase:true}:{type:'phrase',value:val});
        pendingNot=false; i=j+1; continue;
      }
      let j=i;
      while(j<n && !/\s/.test(q[j]) && q[j]!=='"' && q[j]!=='\u201C') j++;
      let raw=q.slice(i,j); i=j;
      if(raw==='-'){ pendingNot=true; continue; }
      let neg=pendingNot; pendingNot=false;
      if(raw.charAt(0)==='-' && raw.length>1){ neg=true; raw=raw.slice(1); }
      if(!raw) continue;
      if(!neg && (raw==='AND'||raw==='OR'||raw==='NOT')){ tokens.push({type:'op',value:raw}); continue; }
      tokens.push(neg?{type:'not',value:raw}:{type:'term',value:raw});
    }
    return {tokens, unbal};
  }
```

Parser:

```js
  function parse(tokens){
    let pos=0; const warnings=[];
    function peek(){ return tokens[pos]; }
    function isTerm(t){ return t && (t.type==='term'||t.type==='phrase'||t.type==='not'); }
    function parseNot(){
      const t=peek();
      if(!t) return null;
      if(t.type==='op' && t.value==='NOT'){ pos++; const c=parseNot(); return c?{kind:'not',child:c}:null; }
      if(t.type==='not'){ pos++; const c=parseNot(); return c?{kind:'not',child:{kind:'term',value:t.value,phrase:!!t.phrase}}:null; }
      if(t.type==='term'||t.type==='phrase'){ pos++; return {kind:'term',value:t.value,phrase:t.type==='phrase'}; }
      return null;
    }
    function parseAnd(){
      let left=parseNot();
      while(true){
        const t=peek();
        if(!t) break;
        if(t.type==='op' && t.value==='OR') break;
        if(t.type==='op' && t.value==='AND'){ pos++; const r=parseNot(); if(!r){ warnings.push('trailing AND ignored'); break; } left={kind:'and',children:[left,r]}; continue; }
        if(isTerm(t)){ const r=parseNot(); if(!r) break; left={kind:'and',children:[left,r]}; continue; }
        if(t.type==='op' && t.value==='NOT'){ const r=parseNot(); if(!r) break; left={kind:'and',children:[left,r]}; continue; }
        break;
      }
      return left;
    }
    function parseOr(){
      let left=parseAnd();
      while(peek() && peek().type==='op' && peek().value==='OR'){
        pos++;
        const r=parseAnd();
        if(!r){ warnings.push('trailing OR ignored'); break; }
        left = left ? {kind:'or',children:[left,r]} : r;
      }
      return left;
    }
    const ast=parseOr();
    if(tokens.length && !ast) warnings.push('no search terms found in the query');
    return {ast, warnings};
  }
```

Hmm if left null in parseAnd (e.g., query starts with OR): parseOr: left=null; sees OR, pos++, r=parseAnd() → if r non-null, left=r. OK handled.

Compile terms:

```js
  function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
  function termPattern(t){
    const e=escRe(t.value.trim());
    if(!e) return null;
    if(t.phrase){
      const parts=e.split(/\\s+/).filter(Boolean);
      return parts.length? parts.join('\\s+') : null;
    }
    return '(?<![\\p{L}\\p{N}_])'+e+'(?![\\p{L}\\p{N}_])';
  }
  function compile(node){
    if(!node) return;
    if(node.kind==='term'){
      const p=termPattern(node);
      if(p){ node.pattern=p; node.reTest=new RegExp(p,'iu'); node.reG=new RegExp(p,'giu'); }
      else node.pattern=null;
    } else if(node.kind==='not'){ compile(node.child); }
    else node.children.forEach(compile);
  }
  function evalAst(node, text){
    if(!node) return true;
    if(node.kind==='term') return node.reTest ? node.reTest.test(text) : false;
    if(node.kind==='not') return !evalAst(node.child, text);
    if(node.kind==='and') return node.children.every(c=>evalAst(c,text));
    if(node.kind==='or') return node.children.some(c=>evalAst(c,text));
    return false;
  }
  function collectPositive(node, out, neg){
    if(!node) return;
    if(node.kind==='not'){ collectPositive(node.child,out,true); return; }
    if(node.kind==='term'){ if(!neg && node.pattern) out.push(node); return; }
    node.children.forEach(c=>collectPositive(c,out,neg));
  }
```

Search:

```js
  let current = []; // {r, patterns, relevance}
  function run(){
    const q=qInput.value.trim();
    let ast=null, warnings=[];
    if(q){
      const tk=tokenize(q);
      const p=parse(tk.tokens);
      ast=p.ast; warnings=p.warnings;
      if(tk.unbal) warnings.push('unbalanced quote — the text after the last opening quote was treated as a phrase');
      compile(ast);
    }
    const comm=committeeSel.value, yr=yearSel.value;
    const positives=[]; collectPositive(ast, positives, false);
    const out=[];
    recs.forEach(r=>{
      if(comm && r.committee!==comm) return;
      if(yr && String(r.year)!==yr) return;
      const text = r.text==null ? '' : String(r.text);
      if(ast && !evalAst(ast, text)) return;
      const pats=[]; let rel=0;
      positives.forEach(t=>{ if(t.reTest.test(text)){ pats.push(t.pattern); rel++; } });
      out.push({r, pats, rel});
    });
    // sort
    const s=sortSel.value;
    out.sort((a,b)=>{
      const ra=a.r, rb=b.r;
      if(s==='relevance'){ if(b.rel!==a.rel) return b.rel-a.rel; }
      const ya=(typeof ra.year==='number')?ra.year:-Infinity, yb=(typeof rb.year==='number')?rb.year:-Infinity;
      if(s==='oldest' ? ya!==yb : yb!==ya) return s==='oldest'? ya-yb : yb-ya;
      const ca=String(ra.committee||''), cb=String(rb.committee||'');
      if(ca!==cb) return ca.localeCompare(cb);
      return (ra.paragraph||0)-(rb.paragraph||0);
    });
    current=out;
    warnEl.textContent = warnings.join(' · ');
    warnEl.style.display = warnings.length? 'block':'none';
    renderStats(q, comm, yr);
    renderChart();
    renderList(true);
  }
```

renderStats:

```js
  function renderStats(q, comm, yr){
    const bits=[];
    bits.push(current.length + ' of ' + recs.length + ' paragraphs match');
    bits.push('query: ' + (q ? '“'+q+'”' : '(empty — showing all)'));
    bits.push('committee: ' + (comm || 'all'));
    bits.push('year: ' + (yr || 'all'));
    statsEl.innerHTML = '<strong>'+esc(bits[0])+'</strong> · ' + bits.slice(1).map(esc).join(' · ');
  }
```

renderChart:

```js
  let chart=null;
  function renderChart(){
    const counts={};
    current.forEach(({r})=>{ const c=r.committee||'(no committee)'; counts[c]=(counts[c]||0)+1; });
    const labels=Object.keys(counts).sort((a,b)=>counts[b]-counts[a]||a.localeCompare(b));
    const data=labels.map(l=>counts[l]);
    const wrap=$('#chartWrap');
    if(!labels.length){
      if(chart){ chart.destroy(); chart=null; }
      wrap.innerHTML='<p class="note">No hits — the chart is empty because no paragraph matches the current query and filters.</p>';
      return;
    }
    if(window.Chart){
      wrap.innerHTML='<canvas id="chartCanvas"></canvas>';
      wrap.style.height = Math.max(140, labels.length*30+50)+'px';
      const ctx=$('#chartCanvas').getContext('2d');
      if(chart) chart.destroy();
      chart=new Chart(ctx,{type:'bar',data:{labels,datasets:[{label:'matching paragraphs',data,backgroundColor:'#1f6fb2',borderRadius:4}]},
        options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
          plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+c.parsed.x+' matching paragraph'+(c.parsed.x===1?'':'s')}}},
          scales:{x:{beginAtZero:true,ticks:{precision:0},title:{display:true,text:'matching paragraphs'}},y:{ticks:{autoSkip:false}}}}});
    } else {
      // fallback
      const max=Math.max.apply(null,data);
      wrap.style.height='auto';
      wrap.innerHTML=labels.map((l,i)=>'<div class="fbar"><span class="flabel">'+esc(l)+'</span><span class="ftrack"><span class="ffill" style="width:'+Math.round(data[i]/max*100)+'%"></span></span><span class="fnum">'+data[i]+'</span></div>').join('');
    }
  }
```

Note: destroying and recreating chart each time is simplest and fine.

renderList with chunking:

```js
  const PAGE=100;
  let shown=0;
  function renderList(reset){
    if(reset){ listEl.innerHTML=''; shown=0; }
    const frag=document.createDocumentFragment();
    const slice=current.slice(shown, shown+PAGE);
    slice.forEach(item=>frag.appendChild(resultEl(item)));
    listEl.appendChild(frag);
    shown+=slice.length;
    if(shown<current.length){
      moreBtn.style.display='inline-block';
      moreBtn.textContent='Show more ('+(current.length-shown)+' remaining)';
    } else moreBtn.style.display='none';
    if(!current.length){
      listEl.innerHTML='<p class="note">No paragraphs match. Try removing a filter or simplifying the query (e.g. drop NOT terms).</p>';
    }
  }
```

resultEl:

```js
  function resultEl(item){
    const r=item.r;
    const art=document.createElement('article'); art.className='result';
    const cite = (r.symbol? String(r.symbol):'(no symbol)') + (r.paragraph!=null? ', para. '+r.paragraph : '');
    const head=document.createElement('div'); head.className='rhead';
    if(r.doc_url){
      const a=document.createElement('a'); a.className='symbol'; a.href=r.doc_url; a.target='_blank'; a.rel='noopener noreferrer';
      a.textContent=r.symbol||r.doc_url; head.appendChild(a);
    } else {
      const s=document.createElement('span'); s.className='symbol plain'; s.textContent=r.symbol||'(no symbol)'; head.appendChild(s);
    }
    if(r.paragraph!=null){ const p=document.createElement('span'); p.className='pill'; p.textContent='para. '+r.paragraph; head.appendChild(p); }
    if(r.committee){ const b=document.createElement('span'); b.className='pill comm'; b.textContent=r.committee; head.appendChild(b); }
    if(typeof r.year==='number'){ const y=document.createElement('span'); y.className='pill'; y.textContent=r.year; head.appendChild(y); }
    const btn=document.createElement('button'); btn.className='copy-btn'; btn.type='button'; btn.dataset.cite=cite; btn.textContent='Copy citation';
    head.appendChild(btn);
    art.appendChild(head);

    const gc=document.createElement('div'); gc.className='gc';
    gc.innerHTML = esc(r.short_title || r.title || '(untitled)') + (r.title && r.short_title ? ' <span class="fulltitle">— '+esc(r.title)+'</span>' : '');
    art.appendChild(gc);

    const citeLine=document.createElement('div'); citeLine.className='citeline';
    citeLine.innerHTML='Citation: <code>'+esc(cite)+'</code>';
    art.appendChild(citeLine);

    const text=String(r.text==null?'':r.text);
    const p=document.createElement('p'); p.className='ptext';
    p.innerHTML = item.pats.length? highlight(text,item.pats) : esc(text);
    if(text.length>900){
      p.classList.add('clamped');
      const t=document.createElement('button'); t.type='button'; t.className='linkbtn'; t.textContent='Show full paragraph ('+text.length+' chars)';
      t.addEventListener('click',()=>{ p.classList.toggle('clamped'); t.textContent = p.classList.contains('clamped')? 'Show full paragraph ('+text.length+' chars)' : 'Show less'; });
      art.appendChild(p); art.appendChild(t);
    } else art.appendChild(p);

    if(Array.isArray(r.cited_articles) && r.cited_articles.length){
      const ca=document.createElement('div'); ca.className='cited';
      ca.textContent='Cited articles: '+r.cited_articles.join(', ');
      art.appendChild(ca);
    }
    return art;
  }
```

highlight:

```js
  function highlight(text, pats){
    const sorted=pats.slice().sort((a,b)=>b.length-a.length);
    const re=new RegExp('(?:'+sorted.join(')|(?:')+')','giu');
    let out='', last=0, m; re.lastIndex=0;
    while((m=re.exec(text))!==null){
      if(m[0]===''){ re.lastIndex++; continue; }
      out+=esc(text.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
      last=m.index+m[0].length;
    }
    return out+esc(text.slice(last));
  }
```

Copy delegation:

```js
  listEl.addEventListener('click', async ev=>{
    const btn=ev.target.closest('.copy-btn'); if(!btn) return;
    const cite=btn.dataset.cite;
    let ok=false;
    try{ await navigator.clipboard.writeText(cite); ok=true; }
    catch(e){
      try{
        const ta=document.createElement('textarea'); ta.value=cite;
        ta.style.cssText='position:fixed;opacity:0'; document.body.appendChild(ta);
        ta.select(); ok=document.execCommand('copy'); ta.remove();
      }catch(e2){ ok=false; }
    }
    const old=btn.textContent;
    btn.textContent = ok? 'Copied ✓' : 'Copy failed — citation shown below';
    btn.classList.add('done');
    setTimeout(()=>{ btn.textContent=old; btn.classList.remove('done'); },1800);
  });
```

Events:

```js
  let deb=null;
  qInput.addEventListener('input',()=>{ clearTimeout(deb); deb=setTimeout(run,180); });
  $('#searchForm').addEventListener('submit',e=>{ e.preventDefault(); clearTimeout(deb); run(); });
  committeeSel.addEventListener('change',run);
  yearSel.addEventListener('change',run);
  sortSel.addEventListener('change',run);
  moreBtn.addEventListener('click',()=>renderList(false));
  document.querySelectorAll('.chip').forEach(ch=>ch.addEventListener('click',()=>{ qInput.value=ch.dataset.q; run(); qInput.focus(); }));
  fillFilters();
  run();
```

Empty data: if recs.length===0 show a banner.

HTML skeleton:

```html
<header class="top">
  <div class="wrap">
    <h1>Search the treaty bodies’ General Comments</h1>
    <p class="lede" id="lede"></p>
    <p class="note">Every result links to the UN document (<code>doc_url</code>) and shows the paragraph exactly as published — nothing is summarised. Matching words are highlighted.</p>
  </div>
</header>
<main class="wrap">
  <section class="card">
    <form id="searchForm">
      <div class="search-row">
        <label class="sr" for="q">Search the paragraph text</label>
        <input id="q" type="search" placeholder='e.g. "substantial grounds" OR torture NOT reservations' autocomplete="off">
        <button class="btn-primary" type="submit">Search</button>
      </div>
    </form>
    <p id="warn" class="warn" style="display:none"></p>
    <details class="howto">
      <summary>How the search works (AND / OR / NOT / "phrases")</summary>
      <ul>
        <li>Words match <strong>whole words</strong> in the paragraph text, ignoring case: <code>torture</code> matches “torture”, not “tortured”.</li>
        <li><code>"…"</code> = exact phrase, e.g. <code>"substantial grounds"</code>.</li>
        <li>Space between terms = AND. Uppercase <code>AND</code>, <code>OR</code>, <code>NOT</code> combine terms; a leading <code>-</code> also means NOT. Examples: <code>children OR adolescents</code>, <code>discrimination AND women NOT reservations</code>.</li>
        <li>Only the paragraph text is searched (not the titles). An empty box shows every paragraph.</li>
      </ul>
    </details>
    <div class="chips">
      <span class="chips-label">Try:</span>
      <button class="chip" data-q='"substantial grounds"'>“substantial grounds”</button>
      <button class="chip" data-q="discrimination AND women">discrimination AND women</button>
      <button class="chip" data-q="children OR adolescents">children OR adolescents</button>
      <button class="chip" data-q="torture NOT reservations">torture NOT reservations</button>
    </div>
    <div class="filters">
      <label>Committee <select id="committee"></select></label>
      <label>Year <select id="year"></select></label>
      <label>Sort <select id="sort">
        <option value="newest">Newest first</option>
        <option value="oldest">Oldest first</option>
        <option value="relevance">Most matched terms</option>
      </select></label>
    </div>
  </section>

  <p id="stats" class="stats"></p>

  <section class="card">
    <h2>Hits per committee</h2>
    <div id="chartWrap" class="chartwrap"></div>
    <p class="note">How this is computed: for each committee, the number of paragraphs in <code>WORKSHOP_DATA.gc</code> whose text matches the current query and the committee/year filters above — counted by this page from the loaded records, not estimated. Only committees with at least one hit are drawn.</p>
  </section>

  <section>
    <h2>Results</h2>
    <p class="note">How this is computed: paragraphs of <code>WORKSHOP_DATA.gc</code> passing the query + filters, sorted as chosen. Each row shows the symbol (link to the UN document, opens in a new tab), the paragraph number, committee, year, the General Comment’s short title, the citation, and the full paragraph text exactly as in the data with matches highlighted.</p>
    <div id="results"></div>
    <button id="more" class="btn-secondary" style="display:none"></button>
  </section>

  <footer class="note">Data: <code>window.WORKSHOP_DATA.gc</code> loaded in this page — no network requests. Counting, filtering, sorting and highlighting are done locally in your browser.</footer>
</main>
```

Wait — chips examples: "torture NOT reservations" etc. are queries, fine.

CSS for clamped: `.ptext.clamped{max-height:8.5em;overflow:hidden;}` plus maybe fade. Fine.

`.sr` visually hidden label.

Chart wrap: `.chartwrap{position:relative;width:100%}` canvas inside with maintainAspectRatio false needs explicit height on wrapper — I set wrap.style.height. Canvas responsive will fill. OK.

Fallback bars CSS: .fbar flex etc.

Now check the "How this is computed" near every chart or number — stats line has note? Add note under stats? The stats line itself says "X of Y paragraphs match · query · committee · year" — that's self-explanatory; add small note: I'll include in results section note. Also add note under stats: maybe combine. I'll add a `.note` right under stats: "Counted locally from the N loaded paragraphs after applying the query and filters." Good.

Edge: `r.year` may be string? Spec says int. Handle both: typeof number or numeric string. In filter compare String(r.year)===yr works for both. In sort, coerce Number(r.year). Let me use `const ynum = r.year==null? null : Number(r.year);` and check isNaN.

Let me refine sort:

```js
function ynum(r){ const y=Number(r.year); return isNaN(y)? null : y; }
out.sort((a,b)=>{
  if(s==='relevance' && b.rel!==a.rel) return b.rel-a.rel;
  const ya=ynum(a.r), yb=ynum(b.r);
  const da = ya==null? (s==='oldest'? Infinity : -Infinity) : ya;
  const db = yb==null? (s==='oldest'? Infinity : -Infinity) : yb;
  if(da!==db) return s==='oldest'? da-db : db-da;
  ...
});
```

Fine.

Also committee filter uses exact match on r.committee — if committee missing, excluded when filter set. OK.

Now header top styling: maybe accent bar. Keep simple: white header with bottom border, or accent background? "light background" overall. I'll do a white header band with accent left border on h1? Keep clean: header with bottom border, h1 accent color? h1 in ink, small accent kicker "WORKSHOP TOOL". Fine.

Let me also set `<html lang="en">`, meta viewport.

Line count check — should be around 550-650. Let me write it out now, being careful with syntax.

One more detail: the search input type="search" gives clear button; fine.

Also `label` wrapping selects: style `.filters label{display:flex;flex-direction:column;gap:4px;font-size:.9rem;color:var(--muted)}`.

Copy button style: `.copy-btn{margin-left:auto;border:1px solid var(--accent);color:var(--accent);background:#fff;border-radius:8px;padding:6px 12px;font-size:.9rem}` hover bg #eaf2fa. `.copy-btn.done{background:var(--accent);color:#fff}`.

rhead: `display:flex;align-items:center;gap:8px;flex-wrap:wrap`. symbol: `font-weight:600;color:var(--accent);text-decoration:none` hover underline. `.symbol.plain{color:var(--ink)}`.

pill: `font-size:.78rem;background:#eef2f7;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--muted)`. comm pill accent tint: `background:#e8f1fa;color:#185a92;border-color:#cfe2f2`.

gc: `margin:8px 0 2px;font-weight:600`. fulltitle: `font-weight:400;color:var(--muted);font-size:.9rem`.

citeline: `font-size:.85rem;color:var(--muted);margin:2px 0 8px` code styled.

ptext: `margin:6px 0 0;white-space:pre-wrap` — preserve line breaks as in data. Good, "exactly as in data" — pre-wrap preserves newlines. 

cited: small muted.

warn: `color:#8a5a00;background:#fff6e0;border:1px solid #f0dfae;...` small.

stats: `font-size:1.05rem;margin:18px 2px 10px`.

h2: `font-size:1.15rem;margin:0 0 10px`.

Now, "Every row that shows a document has its symbol, linked to doc_url in a new tab" — done.

Also the chart card h2 "Hits per committee" — the number of hits per committee as small bar chart — done.

Potential issue: Chart.js v4 with indexAxis 'y' — parsed.x works. OK.

Also when committee filter set to a single committee, chart shows one bar — fine.

Let me also make sure `run()` is called after fillFilters and initial. And chips exist before run — order in script: define everything, then fillFilters(); run();.

Also handle recs empty: show banner in stats/results: if(!recs.length){ statsEl.textContent='No General Comment paragraphs were loaded (WORKSHOP_DATA.gc.records is empty).'; listEl... chartWrap note; return; } I'll guard in run: if !recs.length, set messages and return.

Write final code. Also careful: in tokenize, `q.indexOf(close, i+1)` for curly open “ close ”. Also mixed quotes — fine.

In parse, note tokens of type 'not' with phrase flag: I create `{kind:'term', value:t.value, phrase:!!t.phrase}` wrapped in not. Good.

compile: for 'not' nodes compile child. evalAst 'not' → !eval(child). collectPositive marks negated.

One subtlety: `evalAst` when ast null returns true — but we only call when ast non-null. Fine.

Relevance: positives present count.

Also highlight patterns include terms under OR that matched — yes since we test each positive term against text.

Potential regex issue: pattern with lookbehind inside alternation with 'u' flag — supported in modern browsers (Chrome 62+, Safari 16.4+). Sandbox likely Chromium — fine. To be safe, could avoid lookbehind by using `(?:^|[^\p{L}\p{N}_])(term)(?![...])` but then match includes preceding char and highlight would include it. Lookbehind is fine.

Edge: term value containing only punctuation, e.g. "§" — escRe handles, lookarounds fine.

Now write the whole file. Also add `document.title` maybe static in <title>.

Count lines mentally — fine.

Let me write CSS fully:

```css
:root{--accent:#1f6fb2;--accent-dark:#185a92;--ink:#1d2733;--muted:#5c6b7a;--bg:#f4f6f9;--card:#ffffff;--line:#dce3ec;}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px}
header.top{background:var(--card);border-bottom:1px solid var(--line);padding:26px 0 20px}
.kicker{font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 6px}
h1{font-size:1.55rem;line-height:1.25;margin:0 0 8px}
.lede{margin:0 0 6px;color:var(--ink)}
.note{font-size:.86rem;color:var(--muted);margin:8px 0 0}
main.wrap{padding-bottom:70px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:18px 0}
.search-row{display:flex;gap:10px;flex-wrap:wrap}
#q{flex:1 1 320px;font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink)}
#q:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.btn-primary{font:inherit;font-weight:600;background:var(--accent);color:#fff;border:0;border-radius:8px;padding:10px 18px;cursor:pointer}
.btn-primary:hover{background:var(--accent-dark)}
.btn-secondary{font:inherit;background:#fff;border:1px solid var(--accent);color:var(--accent);border-radius:8px;padding:8px 14px;cursor:pointer;margin:6px 0 0}
.btn-secondary:hover{background:#eaf2fa}
.warn{display:none;margin:10px 0 0;font-size:.88rem;color:#7a5200;background:#fff6df;border:1px solid #ecd9a0;border-radius:8px;padding:8px 12px}
.howto{margin-top:12px;font-size:.9rem;color:var(--muted)}
.howto summary{cursor:pointer;color:var(--accent);font-weight:600}
.howto ul{margin:8px 0 0;padding-left:20px}
.howto li{margin:3px 0}
code{background:#eef2f7;border-radius:4px;padding:1px 5px;font-size:.88em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.chips{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:12px}
.chips-label{font-size:.86rem;color:var(--muted)}
.chip{font:inherit;font-size:.86rem;border:1px solid var(--line);background:#eef4fa;color:var(--accent-dark);border-radius:999px;padding:4px 12px;cursor:pointer}
.chip:hover{background:#dfeafa}
.filters{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
.filters label{display:flex;flex-direction:column;gap:4px;font-size:.86rem;color:var(--muted)}
.filters select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);max-width:320px}
.stats{font-size:1.02rem;margin:20px 2px 4px}
h2{font-size:1.12rem;margin:0 0 10px}
.chartwrap{position:relative;width:100%;min-height:60px}
.result{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:12px 0}
.rhead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.symbol{font-weight:700;color:var(--accent);text-decoration:none}
.symbol:hover{text-decoration:underline}
.symbol.plain{color:var(--ink)}
.pill{font-size:.78rem;background:#eef2f7;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--muted);white-space:nowrap}
.pill.comm{background:#e8f1fa;border-color:#cfe2f2;color:var(--accent-dark);font-weight:600}
.copy-btn{margin-left:auto;font:inherit;font-size:.86rem;border:1px solid var(--accent);color:var(--accent);background:#fff;border-radius:8px;padding:5px 12px;cursor:pointer}
.copy-btn:hover{background:#eaf2fa}
.copy-btn.done{background:var(--accent);color:#fff}
.gc{margin:9px 0 2px;font-weight:600}
.fulltitle{font-weight:400;color:var(--muted);font-size:.88rem}
.citeline{font-size:.85rem;color:var(--muted);margin:2px 0 6px}
.ptext{margin:6px 0 0;white-space:pre-wrap;word-break:break-word}
.ptext.clamped{max-height:8.6em;overflow:hidden}
.linkbtn{background:none;border:0;color:var(--accent);font:inherit;font-size:.88rem;cursor:pointer;padding:4px 0 0;text-decoration:underline}
.cited{margin-top:8px;font-size:.82rem;color:var(--muted)}
mark{background:#ffe08a;color:inherit;border-radius:2px;padding:0 1px}
.fbar{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:.9rem}
.flabel{width:90px;flex:none;text-align:right;color:var(--muted)}
.ftrack{flex:1;background:#eef2f7;border-radius:4px;height:18px;overflow:hidden}
.ffill{display:block;height:100%;background:var(--accent)}
.fnum{width:40px;flex:none}
footer.note{margin-top:26px;border-top:1px solid var(--line);padding-top:12px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
@media (max-width:640px){.copy-btn{margin-left:0}}
```

OK. Now assemble. Also note: `main.wrap` — main has class wrap; header has inner div.wrap. Fine.

Double-check the parse function handles token stream like `NOT torture` at start: parseOr→parseAnd→parseNot sees op NOT → pos++, parseNot → term torture → returns not(torture). Good. `a OR NOT b`: parseOr: left=parseAnd→ a; sees OR; pos++; parseAnd→parseNot sees NOT → not(b). left=or(a, not(b)). Good. `a AND OR b`: parseAnd: left=a; sees AND, pos++, parseNot sees OR → returns null → warning 'trailing AND ignored', break. Then parseOr: peek is OR → pos++, parseAnd → b. left=or(a,b). Hmm — "a AND OR b" becomes a OR b with warning. Acceptable.

`a b` → and(a,b). `a -b` → tokens: term a, not b → parseAnd: left=a; peek is 'not' → isTerm true → parseNot handles 'not' → not(b); and(a, not(b)). Good.

Now the year select values: I set option value = y (number → string). Compare String(r.year)===yr. If r.year is "2011" string, String works. Good.

Committee select: value esc'd — committee names may contain quotes? esc handles.

One more: stats uses innerHTML with esc — fine.

Chart destroy/recreate each run — with many runs could be heavy but fine.

Also add `aria-live="polite"` on stats maybe. Nice touch.

Now, "Before the code block: at most three short sentences saying what you built." Then code block, then nothing.

Let me write the final answer. I'll be careful with template literals inside script — fine in HTML.

Also ensure no `fetch` etc. No external loads. Chart.js from window.Chart only.

Write it.

One more consideration on highlight regex construction: patterns joined: `'(?:' + sorted.join(')|(?:') + ')'` — correct.

Also in `collectPositive`, node.negated not needed.

Potential perf: for each record, positives.forEach test — fine.

Also initial run before user types: query empty → all records shown (first 100). Chart shows distribution of all. Good.

Let me finalize the lede: also include DATA.count if present? "n" = recs.length. If DATA.count differs, whatever. Use recs.length.

Also title element: `<title>General Comments search · workshop data</title>`.

Now write out. I'll count roughly; keep it tight but complete.

Also the "How this is computed" note near the stats number: add `<p class="note" id="statsNote">Counted locally in this page from the ${recs.length} loaded paragraphs, after applying the query and filters — not estimated.</p>` — set statically after computing recs.length via JS? I'll just include in renderStats area: a static note element whose text I set in JS with recs.length. Simpler: in HTML put placeholder and fill in init: `$('#statsNote').textContent = 'Counted locally in this page from the ' + recs.length + ' loaded paragraphs, after applying the query and the committee/year filters — not estimated.'`

OK writing final.