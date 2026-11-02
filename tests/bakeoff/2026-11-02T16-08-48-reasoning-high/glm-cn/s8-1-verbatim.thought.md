Let me build this app carefully. It's a search tool for General Comments.

Requirements:
1. Title "General Comments search", one line: source, number of paragraphs, year range from data.
2. Search box + Search button, Enter searches, help line about syntax with example.
3. Filters: committee (all committees in data + "All"), year from–to. Changing filter re-runs search.
4. Count line: "N paragraphs match out of M, filters: …".
5. Bar chart: matching paragraphs per committee, with "How this is computed" note. Chart.js.
6. Results sorted newest year first (newest General Comment first — sort by year descending; maybe tie-break). Each card: committee, short title, year, symbol linked to doc_url in new tab; full paragraph text with highlighted search words; "Copy citation" button copying "symbol, para. N"; button says "Copied" for 2 seconds.
7. Empty state message.

Search parsing rules:
- Case-insensitive.
- Plain word: whole word match ("right" doesn't match "rights").
- Quoted phrase: exact sequence of words.
- Spaces = AND; OR joins alternatives; NOT before word/phrase excludes.
- No brackets.

I need a small query parser. Grammar:

Query → OR of AND groups? Let me think. "Words separated by spaces are ANDed; OR joins alternatives; NOT before a word or phrase excludes it."

Simplest approach: split top-level by OR (as a token word "OR"), each alternative is a list of terms ANDed. Within a group, terms can be prefixed by NOT. Example: `torture NOT detention` → one group: torture AND NOT detention. `cat OR dog` → two groups.

Tokenizer: handle quoted phrases "best interests", words, and keywords OR / NOT (case-sensitive? Probably treat OR and NOT as operators regardless of case? The help says write OR, NOT uppercase. Hmm. But a paragraph could contain the word "or" or "not". To be safe, treat operators as uppercase-only: "OR" and "NOT" as standalone tokens. Actually if user types "or" lowercase it would be searched as a word. The spec example uses uppercase. I'll treat only exact uppercase "OR" and "NOT" as operators. Hmm, but that could confuse. Actually the plan says: 'words are combined with AND unless you write OR; NOT excludes a word'. I'll make operators case-sensitive uppercase to avoid matching the common English words "or"/"not" as operators. That's the safer choice for searching legal text. Wait — but if someone searches "not" as a word... unlikely. I'll go with uppercase-only operators. Hmm, let me reconsider: many search systems accept any case. But searching text of General Comments, "or" and "not" are common words. If user types ` torture or detention` expecting OR, and it treats "or" as a word to match, they'd get zero results possibly. The help text says "unless you write OR" — implying writing OR specifically. I'll accept "OR"/"NOT" in uppercase only... Actually, let me be a bit lenient: I'll accept case-insensitive "or" and "not"? No — risk: search for phrase containing "not"? Quoted phrases are fine. A bare word "not" is unusual. I think uppercase-only is fine and matches the help text. Let me keep uppercase-only.

Parsing algorithm:
- Tokenize: scan the string; quoted phrases become {type:'phrase', value}; whitespace-separated words become {type:'word', value}. Keep the raw tokens including "OR"/"NOT".
- Split token list on OR tokens → groups.
- Each group: sequence of terms; a term optionally preceded by NOT. Note: consecutive NOTs? Just handle NOT immediately before a word/phrase.
- Empty query → match all (no search filter). If query is only NOT terms, that's fine — e.g., "NOT detention" matches everything without detention. That's reasonable.

Matching a record:
- For each group (alternative), all terms must match; a NOT term must not match. Record matches if any group matches.
- Word match: whole word, case-insensitive. Regex: escape word, use word boundaries. But careful with words containing non-alphanumeric... "child" fine. Word boundary \b works for typical words. What about words with apostrophes like "children's"? \b at the end after 's' works (' is non-word char so boundary between s and... hmm "children's" — searching "children" with \bchildren\b would not match "children's" because after "children" comes "'", which is a non-word char, so \b matches. Actually \bchildren\b: "children's" — position after "children" is between "n" and "'", both... \b exists between word char and non-word char. So "children" would match inside "children's". Is that whole-word? Debatable but acceptable. Keep simple \b approach. Actually better: define word characters as letters/digits and use custom boundaries: (^|[^\p{L}\p{N}])word(?=[^\p{L}\p{N}]|$). Unicode property escapes require the u flag, supported in modern browsers. That handles apostrophes: "children" vs "children's" — "'" is not a letter/number, so "children" would still match "children's" prefix... hmm, with custom boundaries, "children" followed by "'" — lookahead [^\p{L}\p{N}] matches ', so yes it matches. Same as \b. Whatever; "right" vs "rights": "rights" after "right" comes "s", a letter, so no match. Good.

Use Unicode-aware regex with 'u' flag for robustness with accented characters. Build a RegExp per term for matching, cache.

Phrase match: exact sequence of words, case-insensitive. "an exact sequence of words" — so normalize whitespace? "best interests" matching "best    interests" across line breaks? The text may contain newlines. I'll treat phrase as: the phrase words in order, separated by flexible whitespace (and maybe hyphenation?). Keep it as: escape each word, join with \s+ — case-insensitive. Hmm, "exact sequence of words" — I'll use \s+ between words. That handles line breaks.

Highlighting: need to highlight matched words. For each positive term (word or phrase) in the query, wrap matches in the text with <mark>. Must not alter text. Approach: build a combined regex from all positive terms (alternation), then escape HTML of the text, and... careful: HTML-escaping then applying regex could match across entities (e.g., "&amp;"). Safer: split the raw text by the combined regex with capture groups, escape each piece, wrap matches.

Implementation: build one regex: (term1|term2|...) with 'giu' flag where each term is its own pattern (word boundaries or phrase pattern). Order matters: longer phrases first so "best interests" highlights as a phrase rather than "best" and "interests" separately. Sort terms by pattern source length descending? Better: sort by number of words descending, then length. Since alternation picks the first match at a position, put phrases first.

But careful: word boundary around alternation. Each alternative carries its own boundaries: \bword\b or phrase-words joined with \s+. Combined: new RegExp(alts.join('|'), 'giu')... wait 'u' flag with \b is fine; but my custom boundaries use \p{L} which requires u flag. \b works with u flag too.

Edge: overlapping matches — with global regex and exec loop, matches don't overlap; fine.

For NOT terms, don't highlight.

Also, highlight should only apply terms that actually appear? Highlighting all positive terms is fine — if a term matches, it gets highlighted; if not (e.g., in an OR where only one side matched), the regex simply finds nothing.

Word matching detail — case-insensitivity: use 'i' flag; for Unicode, maybe also normalize? Keep simple: 'iu' flags. Accented characters: 'i' flag without full case folding may miss e.g. "É" vs "é"? The i flag does simple case folding; 'iu' does... For most searches fine.

Whole-word boundary: use lookbehind/lookahead: (?<![\p{L}\p{N}]) and (?![\p{L}\p{N}]). Lookbehind supported in modern browsers (sandbox presumably Chromium). Should be fine. Alternatively \b works but treats underscore as word char and fails on apostrophes adjacent. I'll use the \p approach.

Hmm wait — what about a search word that starts with a non-letter, like "non-refoulement"? Hyphen inside: \b behavior — pattern "non-refoulement" with boundaries: lookbehind before 'n' and lookahead after final 't'. Inside the hyphen is literal. Fine.

Escape regex special chars in terms.

Now filters:
- Committee filter: select with "All" + every committee in data (sorted? alphabetical). Sorted alphabetically.
- Year from–to: two number inputs. Empty = open. Records with no year: included when filter open (both empty), excluded when a from–to range set (either from or to set? "excluded by a from–to range" — I'll say if either from or to is specified, it's a range and excludes unknown years). Hmm: what if only "from" set? Still a range constraint → exclude unknown. I'll implement: if from or to set → year must exist and satisfy constraints.

Filters applied first, then search. Count line: "N paragraphs match out of M, filters: …". What's M? Total paragraphs in dataset? Or after filters? The spec: "N paragraphs match out of M". And "empty text → never matches but still counted in M". Hmm — that suggests M is the total after filters? Let's think: "Filters are applied first, then the search." If M were post-filter count, then "counted in M" for empty text... empty text records are still in the filtered set (they're paragraphs). Actually I think M = number of paragraphs after filters (the pool the search runs on). But then the line "out of M" with filters listed... Alternatively M = total in dataset. Hmm.

Test criteria don't clarify. Let me decide: M = paragraphs after filters (the search pool). And show filters applied in the line. E.g., "12 paragraphs match out of 3,460 (filters: committee = CRC, years 2000–2020; search: "best interests" AND child)". Hmm the spec says 'A count line: "N paragraphs match out of M, filters: …"'. I'll render: `N paragraphs match out of M` then `Filters: committee: All · year: 1900–2030 (all years) · search: ...`. Actually "filters: …" describes the filters. I'll include the search query too for clarity.

Hmm, wait: "empty text → never matches but still counted in M". If M is post-filter pool, an empty-text record is in the pool and counted in M, but never matches. That's consistent. Good, M = filtered pool size.

Sorting: "newest General Comment first" — sort by year descending. Tie-break? Maybe by symbol/paragraph. I'll sort year desc, then symbol, then paragraph. Records without year go last? "newest first" — unknown year at the end. Fine.

Card layout:
- Header line: committee, short_title (or title, or symbol), year (or "year unknown"), symbol linked.
- Paragraph text (full, character for character). Should it be in a <pre>-like element to preserve characters? "shown character for character" — newlines? Using white-space: pre-wrap preserves line breaks without inventing structure. I'll use pre-wrap on the text container. That shows characters exactly.
- Copy citation button: copies `symbol + ", para. " + paragraph`. Use navigator.clipboard.writeText with fallback (execCommand textarea) since sandboxed pages may restrict clipboard. Provide fallback.

Citation: only symbol and paragraph, "nothing invented". If paragraph missing? Paragraph is int per schema; assume present. If missing... skip button? Just handle: if paragraph == null, citation is symbol only? Spec says citation is symbol + ", para. " + paragraph. I'll guard: if paragraph is null/undefined, copy just symbol. Keep minimal.

Chart: bar chart of matching paragraphs per committee for current search. Include committees with >0 matches only? "the bars add up to N" — if we include zero-count committees, bars add to N anyway (zeros add nothing). But cleaner to show all committees in filtered pool? Hmm. Test 3: "Choose CRC in the committee filter: the chart shows a single bar whose height equals N." If committee filter is CRC, the pool only has CRC, so a single bar. If I show all committees from the full dataset with zero bars, filtering CRC would show many zero bars + one bar. The test says "a single bar". So chart should show committees present in the filtered pool (count > 0 among matches? or among pool?). If pool = CRC only, committees in pool = {CRC} → single bar. 

Should the chart show committees with matches>0, or all committees in the filtered pool (some may have 0 matches)? If search yields matches only in CRC but pool is all, bars: committees with matches>0 → only CRC bar. Committees in pool with zero matches would add zero-height bars. "the bars add up to N" holds either way. I'll show committees from the filtered pool, sorted by count descending, but only include those with at least one match? Hmm — showing zero bars is noise. Let me include only committees with count > 0 among matches. Then bars sum to N always. And with CRC filter, single bar. 

Wait, but should chart reflect pool or matches? "A small bar chart: matching paragraphs per committee for the current search". So counts = matches per committee. Show only committees with ≥1 match. If N=0, show empty chart area with a note or hide chart. I'll show a message "No matches to chart" or just render empty. I'll conditionally render chart, else show text.

Chart.js 4 preloaded as window.Chart. Use it. Destroy chart before re-creating on updates.

"How this is computed" note near the chart: e.g., "How this is computed: each bar counts the paragraphs in the current filtered, matching results grouped by the committee field. The bars together equal the number of matching paragraphs shown above."

Also a "How this is computed" note near... the rules say "a short 'How this is computed' note near every chart or number." So near the count line too? Add small note under count line: how N and M computed. I'll add one note covering the count and one for the chart.

Header line: "source, number of paragraphs, year range, all read from the data". Source: WORKSHOP_DATA.gc.source or title. Data description: `{title, source, count, records}`. Use source for "source", count for number... but count should match records.length; read from data — use records.length maybe, or count. "number of paragraphs" — I'll compute from records.length (that's read from data). Year range: min/max year over records, handling missing years.

One-line description: e.g., "Source: {source} · {n} paragraphs · {minYear}–{maxYear}". If no years at all: "years unknown".

Search behavior: Search button re-runs; Enter in input re-runs. Filters changing re-runs. Should typing re-run live? No — only on Search/Enter, and filter changes. I'll keep a current query state applied on search action.

Initial state: no query → all filtered paragraphs shown? Showing all thousands of cards would be heavy. Hmm. Initially, with no search, results = entire pool. That could be thousands of cards (real data is larger). Rendering e.g. 3000 cards is heavy but doable? Could be slow. Better: cap displayed cards with a "show more" or show first 100 with a note. But rule: "N, the chart bars and the cards come from the same list". Capping display doesn't change the list; I can show first 200 and a note "Showing first 200 of N". Hmm, the spec doesn't mention pagination. To be safe and honest, I'll render up to 300 cards and note if truncated: "Showing the first 300 matching paragraphs; refine your search to see fewer." The chart and N still reflect the full list. I think that's acceptable and pragmatic. Actually let me reconsider — is it "keeping it simple"? A truncate-with-note is simple. Yes, cap at 300.

Highlight function details:

```js
function buildTermRegex(term, isPhrase){
  if(isPhrase){
    const words = term.split(/\s+/).filter(Boolean).map(escapeRe);
    return '(?:' + words.join('\\s+') + ')';
  }
  return '(?<![\\p{L}\\p{N}])' + escapeRe(term) + '(?![\\p{L}\\p{N}])';
}
```

For phrase, "exact sequence of words" — should phrase be bounded too? "a quoted phrase matches that exact sequence of words" — "best interests" shouldn't match "best interested"? Sequence of words — I'd bound the phrase on both sides as well: (?<![\p{L}\p{N}]) before and (?![\p{L}\p{N}]) after. Yes, add boundaries to phrase: `(?<![\p{L}\p{N}])(?:w1\s+w2)(?![\p{L}\p{N}])`. Wait, but then "best interests" wouldn't match "best interests of" — it would, since after "interests" comes space. Fine. But what about punctuation adjacency: "child," matches "child". Good.

Hmm, one concern: \s+ in phrase with 'u' flag fine.

Matching a record for a term: use regex with 'iu' flags, test against text. But careful: regexes with global flag have lastIndex state; use non-global for testing, global for highlighting. Create per-term test regex without 'g'.

Combined highlight regex: alternation of positive term patterns, flags 'giu'. Sort alternatives: phrases (multi-word) first, then longer words first. Since alternation is ordered, first matching alternative at a position wins. Put all patterns sorted by (word count desc, length desc).

Highlight rendering:
```js
function renderHighlighted(text, regex){
  if(!regex){ return escapeHtml(text); }
  let out = '', last = 0, m;
  regex.lastIndex = 0;
  while((m = regex.exec(text)) !== null){
    out += escapeHtml(text.slice(last, m.index)) + '<mark>' + escapeHtml(m[0]) + '</mark>';
    last = m.index + m[0].length;
    if(m[0].length === 0) regex.lastIndex++; // safety
  }
  out += escapeHtml(text.slice(last));
  return out;
}
```

Edge: zero-length matches impossible since terms non-empty.

Parser:

```js
function tokenize(query){
  const tokens = [];
  let i = 0;
  while(i < query.length){
    const ch = query[i];
    if(ch === '"'){
      const end = query.indexOf('"', i+1);
      if(end === -1){
        // unterminated: take rest as phrase
        const val = query.slice(i+1).trim();
        if(val) tokens.push({t:'phrase', v:val});
        i = query.length;
      } else {
        const val = query.slice(i+1, end).trim();
        if(val) tokens.push({t:'phrase', v:val});
        i = end+1;
      }
    } else if(/\s/.test(ch)){
      i++;
    } else {
      let j = i;
      while(j < query.length && !/\s/.test(query[j]) && query[j] !== '"') j++;
      tokens.push({t:'word', v: query.slice(i,j)});
      i = j;
    }
  }
  return tokens;
}
```

Then interpret: OR (word token exactly "OR") splits groups; NOT (word token exactly "NOT") negates next token.

```js
function parseQuery(query){
  const tokens = tokenize(query);
  const groups = [];
  let current = [];
  for(let k=0;k<tokens.length;k++){
    const tok = tokens[k];
    if(tok.t==='word' && tok.v==='OR'){
      groups.push(current); current = [];
    } else if(tok.t==='word' && tok.v==='NOT'){
      const next = tokens[k+1];
      if(next){ current.push({neg:true, phrase: next.t==='phrase', v: next.v}); k++; }
      // NOT at end: ignore
    } else {
      current.push({neg:false, phrase: tok.t==='phrase', v: tok.v});
    }
  }
  groups.push(current);
  return groups.filter(g => g.length > 0);
}
```

If groups empty → no constraints → match all.

matchRecord: for each group, every term: test = regexTest(term, text); if neg ? test : !test → group fails. Any group passes → match.

Note: empty text ("" or null) never matches — if there are positive terms, regex won't match empty text; if query only has NOT terms, "NOT detention" on empty text... text without "detention" — empty text would match NOT-only query. But rule says empty text never matches. So special-case: if !text or text.trim()==='' → never matches (when a query exists). What about no query at all — show empty-text records? They're in pool and counted in M; with no query they'd be "matches"... Rule: "empty text → never matches but still counted in M". Hmm, "never matches" — even with empty query? If no query, all pool records shown, including empty text ones? Displaying an empty card is weird. I'll interpret: with an active query, empty text never matches. With no query, everything in pool shows. Hmm, but "never matches" is strong. If no search, "matches" concept doesn't apply — the count line would say "M paragraphs match out of M". I'll make no-query show all pool records including empty text (they're counted in M, consistent). Actually wait — to be safe with the letter of the rule, maybe exclude empty-text records from results always, but count them in M? Then with no query, N = pool minus empty-text count, but M = pool → "N match out of M" where N≠M with no filters/search, which looks odd but is honest: "empty text never matches". Hmm.

The rule is under "Missing values" and pairs with "no year → show 'year unknown', included when the year filter is open". I think the intent: when searching, empty text can't match. With no query, there's no matching happening. I'll go: if query is non-empty, empty text never matches; if query empty, all pool records display. And a card with empty text would show "(no text)"... Actually simpler: I'll treat empty query as matching everything in pool, including empty-text records, but render empty text as an em-dash note "(this paragraph has no text in the data)". Hmm, that adds complexity. Realistically, GC paragraphs all have text. Keep the guard simple: empty/null text → treated as "" and simply won't match any positive term. If no query, it displays with empty body. Fine — minimal handling, edge case unlikely.

Actually let me just add: `if(!rec.text || rec.text.trim()===''){ if(hasQuery) return false; }` — with no query it shows. Fine.

Filters:

```js
function inYearFilter(rec, from, to){
  const y = rec.year;
  if(from === '' && to === '') return true; // open
  if(y == null) return false;
  if(from !== '' && y < from) return false;
  if(to !== '' && y > to) return false;
  return true;
}
```

from/to as numbers.

Count line format: `"best interests" AND child` example. Count line: `N paragraphs match out of M` + filters description. Let me write: 

`<strong>{N}</strong> paragraphs match out of {M}` then below: `Filters: committee: {committee} · year: {desc} · search: {query or 'none'}`. Where year desc: "all years" or "from X" or "to Y" or "X–Y".

Where M = filtered pool size. Also note: "How this is computed: filters are applied first (committee and year), then the search runs on the remaining paragraphs; M is the number of paragraphs after filtering."

Hmm wait, re-reading: 'A count line: "N paragraphs match out of M, filters: …"'. Maybe M is total dataset and "filters: …" lists the filters. If M were total, then "empty text counted in M" trivially true. Ambiguous. Which is more useful? "12 match out of 3,460" with filters listed — user sees filters applied. I think M = after filters is more informative (denominator of the search). But hmm, "filters: …" following suggests the sentence continues "out of M, filters: committee=CRC, years…". Either reading works. I'll use M = pool after filters, and explicitly label: "out of M paragraphs after filtering". Let me phrase count line: `{N} of {M} paragraphs match (after filters) · filters: committee: …, year: …, search: …`. Hmm, keep close to spec: "N paragraphs match out of M, filters: committee: All, year: all years, search: …". I'll write exactly that pattern.

Chart note: "How this is computed: bars count the matching paragraphs (after filters and search) grouped by their committee field. Bars sum to N above."

Copy citation fallback:
```js
function copyText(str, btn){
  const done = () => { const old = btn.textContent; btn.textContent='Copied'; btn.disabled... setTimeout restore 2000ms; };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(str).then(done).catch(()=>fallback());
  } else fallback();
  function fallback(){ const ta=document.createElement('textarea'); ta.value=str; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(ta); done(); }
}
```

Citation string: `${symbol}, para. ${paragraph}`. If paragraph null → just symbol. (Guard.)

Sorting: newest first: year desc; nulls last; tie: symbol asc (localeCompare), paragraph asc.

Card structure:
```html
<div class="card">
  <div class="card-head">
    <span class="chip">{committee}</span>
    <span class="ctitle">{short_title||title||symbol}</span>
    <span class="cyear">{year ?? 'year unknown'}</span>
    <a class="csymbol" href="{doc_url}" target="_blank" rel="noopener">{symbol}</a>
  </div>
  <p class="ctext">{highlighted}</p>
  <button class="copy-btn" data-citation="...">Copy citation</button>
</div>
```

Use event delegation for copy buttons, storing citation in data attribute (escape quotes). Or closure per button. Since we rebuild the list each render, attach listeners directly — but 300 cards × listener fine. Use delegation on container, reading data-citation. Citation contains quotes? Symbols like "CCPR/C/GC/37" — no quotes. Use data attribute with escapeHtml for attribute value. Or store index and look up in a retained array. I'll keep a `lastResults` array and data-index. Clean.

Committee filter options: unique committees sorted. Some records may lack committee? Guard: treat missing as "—"? Keep simple: filter(Boolean) unique; if a record has no committee and filter != All, it's excluded unless... hmm. If record.committee is undefined and a specific committee chosen, excluded. If "All", included. Chart groups by committee; missing committee → group "(unknown)". Minor edge; handle gracefully with `(rec.committee || 'Unknown')`.

Year inputs: `<input type="number" placeholder="from">` — also allow just typing. Add min/max hints from data? Placeholder with data min/max.

Design: base font 16px, accent #1f6fb2, light background (#f6f8fa), system font stack, cards white with border, generous spacing. Title, description line. Sticky-ish? No need.

Chart: small, maybe max-width 100%, height ~220px. Bar color accent. X axis labels rotated? With many committees (CRC, CAT, CERD, CESCR, CCPR, CMW, CEDAW, CRPD, etc. — maybe ~10), auto-skip. Chart.js handles it.

Empty state: "No paragraph contains these words" + tip "Try OR between words, or remove some words to broaden the search."

Also validation messages for query? Keep simple.

Re-run on filter change: 'change' and 'input'? 'change' event for select and number inputs (change fires on blur/enter for number). Use 'input' for select (fires immediately) and 'change' for number inputs. Actually 'input' fires on number fields per keystroke too — that re-runs search each keystroke, could be fine (search is fast) but Enter conflicts... The spec: "Changing a filter re-runs the search." I'll use 'change' on both select and number inputs — fires when value committed. Good.

Now search execution: query state. The input holds the text; pressing Search or Enter sets currentQuery = input.value, then render. Filters read live.

Let me also handle: the search input's Enter key → preventDefault, run search.

Line count: keep under ~700 lines. Should be fine (~450).

Header description: "Source: {source} — {count} paragraphs of General Comments, {minYear}–{maxYear}." Use records.length for count. Also maybe mention title? Data has title like "General Comments, paragraph by paragraph". Use source field. If source missing use title.

Chart "How this is computed" note and count note.

Let me also double check the highlight with regex special chars: escapeRe = s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'). With 'u' flag, escaping is fine.

Lookbehind in 'u' regex: (?<![\p{L}\p{N}]) — supported in Chromium 62+. Sandbox presumably modern. OK.

Case-insensitive with 'iu': for phrase with accented chars fine.

One more: term regex for testing — build once per unique term, cache in a Map.

Also the combined highlight regex must include both phrase and word terms; if no positive terms (pure NOT query), no highlighting — regex null → plain escaped text. Good: `torture NOT detention` highlights "torture" only. Wait — should "torture" be highlighted? Yes, positive term. NOT terms not highlighted. Good.

Test 1: `"best interests" AND child` — "AND" is a word token "AND"! My parser treats "AND" as a search word. The example query includes "AND". Hmm! The help says: 'words are combined with AND unless you write OR'. So "AND" as a typed token — should it be treated as operator or as a word? The example `"best interests" AND child` — if AND is treated as a literal word, the search would require the word "and" in the text. General Comment text contains "and" everywhere, so it would still match... but it would also try to highlight "and" everywhere! That would be bad.

So I must treat "AND" (uppercase) as an operator token (no-op, since adjacency already means AND). Yes — accept AND, OR, NOT as uppercase operators. AND = ignored. OR = group separator. NOT = negation. And bare "and"/"or"/"not" lowercase remain searchable words. Good catch.

Highlight: don't highlight "AND" — operators excluded from terms. Good.

Now tokenizer produces word tokens; parser skips 'AND', splits on 'OR', negates after 'NOT'.

Edge: `NOT "best interests"` — NOT before phrase: negate phrase. Handled: next token can be phrase.

Edge: `NOT NOT word`? First NOT consumes next token which is "NOT" (a word token)... my parser: NOT takes tokens[k+1] regardless of it being NOT keyword. Then k++ skips it. So "NOT NOT word" → negated term "NOT"?? Hmm: tokens: [NOT, NOT, word]. k=0: NOT → next is word "NOT" → push neg term "NOT", k=1→ k becomes 2. Then k=2: word → positive. Weird but harmless. Keep simple; not in spec.

Now, the year range in header: compute min/max over records with year. If none, "year range unknown".

Committee chart: also show even when no query? Yes, chart of matches (pool) per committee. With CRC filter → single CRC bar = N. Good.

Sorting committees in chart: descending count, then alphabetical.

Truncation: display limit 300. Note under results if truncated: "Showing the first 300 of N matching paragraphs — refine the search to shorten the list." Count line N still full.

Now the count-line "filters" text. Let me produce:
- committee: value or "All"
- year: "all years" / "from {from}" / "up to {to}" / "{from}–{to}"
- search: `"{query}"` or "none"

E.g.: `142 paragraphs match out of 3,460 · filters: committee: All · year: all years · search: "best interests" AND child`.

Spec: "N paragraphs match out of M, filters: …" — good match.

Now write the HTML.

Structure:

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
<header class="top">
  <h1>General Comments search</h1>
  <p id="dataLine"></p>
</header>
<section class="controls">
  <div class="searchrow">
    <input id="q" type="text" placeholder='e.g. "best interests" AND child'>
    <button id="searchBtn">Search</button>
  </div>
  <p class="help">Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: <code>"best interests" AND child</code>. Plain words match whole words only ("right" does not match "rights").</p>
  <div class="filters">
    <label>Committee <select id="committee"></select></label>
    <label>Year from <input id="from" type="number"></label>
    <label>to <input id="to" type="number"></label>
  </div>
</section>
<p id="countLine"></p>
<p class="note" id="countNote">How this is computed: ...</p>
<section class="chartbox">
  <h2>Matching paragraphs by committee</h2>
  <div class="chartwrap"><canvas id="chart"></canvas></div>
  <p class="note">How this is computed: ...</p>
</section>
<section id="results"></section>
<script>...</script>
</body>
</html>
```

CSS: clean, light. Accent #1f6fb2. mark styling: background #ffe9a8 or accent-tinted.

Chart container fixed height (e.g., 240px) with position relative for Chart.js responsive.

When N=0: hide chart section, show empty message in results.

Let me write JS:

```js
const GC = window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc;
const recs = (GC && Array.isArray(GC.records)) ? GC.records : [];
```

If no data: show message. Edge guard.

Header line:
```js
const years = recs.map(r=>r.year).filter(y=>typeof y==='number');
const minY = years.length? Math.min(...years) : null;
...
const source = GC.source || GC.title || 'unknown source';
dataLine.textContent = `Source: ${source} · ${recs.length} paragraphs` + (years.length? ` · ${minY}–${maxY}` : ' · year range unknown');
```

Wait — Math.min(...years) with thousands of entries: spread of maybe 5k numbers is OK. Or reduce. Use reduce to be safe.

Committees: unique sorted:
```js
const committees = [...new Set(recs.map(r=>r.committee).filter(Boolean))].sort();
```

Populate select: All + committees.

State: currentQuery = ''.

parse + match as designed.

```js
const termCache = new Map();
function termTestRegex(term){
  const key = (term.phrase?'P':'W') + '\u0000' + term.v.toLowerCase();
  ...
}
```

Actually just build pattern string:

```js
function termPattern(term){
  if(term.phrase){
    const ws = term.v.split(/\s+/).filter(Boolean).map(escapeRe);
    if(!ws.length) return null;
    return '(?<![\\p{L}\\p{N}])(?:' + ws.join('\\s+') + ')(?![\\p{L}\\p{N}])';
  }
  return '(?<![\\p{L}\\p{N}])' + escapeRe(term.v) + '(?![\\p{L}\\p{N}])';
}
```

Test regex: new RegExp(pattern, 'iu'). Phrase test: also 'iu'.

matchRecord(text, groups):
```js
function matchesQuery(rec, groups){
  if(groups.length === 0) return true;
  const text = rec.text || '';
  if(!text.trim()) return false; // empty text never matches when a query exists
  return groups.some(g => g.every(term => {
    const re = getTestRe(term);
    const hit = re.test(text);
    return term.neg ? !hit : hit;
  }));
}
```

Wait — groups.length===0 when query is empty string or only operators. If query non-empty but parses to no groups (e.g., "AND" alone)? Then groups empty → matches everything. Acceptable: "AND" alone → no constraints. Hmm, "NOT" alone with nothing after → no groups → match all. Fine.

But careful: if query is "NOT detention", groups = [[{neg:true,...detention}]] → matches all texts without detention. Good.

Highlight regex: from positive terms of all groups:
```js
function buildHighlightRegex(groups){
  const pos = [];
  groups.forEach(g=>g.forEach(t=>{ if(!t.neg) pos.push(t); }));
  if(!pos.length) return null;
  const pats = pos.map(termPattern).filter(Boolean);
  // longer first
  pats.sort((a,b)=>b.length-a.length);
  try{ return new RegExp('(?:' + pats.join('|') + ')', 'giu'); }catch(e){ return null; }
}
```

Hmm — sorting by pattern string length is a rough proxy for specificity; phrases have boundaries making them longer. Good enough.

Edge: term with empty value filtered in tokenizer (val truthy check). Phrase of only spaces → skipped.

escapeHtml:
```js
function escapeHtml(s){ return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
```

render():

```js
function runSearch(){
  const q = document.getElementById('q').value;
  currentQuery = q;
  render();
}
```

Actually store query in variable; filters read directly in render.

```js
function render(){
  const committeeSel = ..., from = ..., to = ...;
  const fromV = from.value === '' ? null : parseInt(from.value,10);
  ...
  const pool = recs.filter(r => (committeeSel.value==='All' || r.committee===committeeSel.value) && yearOk(r, fromV, toV));
  const groups = parseQuery(currentQuery);
  const hasQuery = currentQuery.trim() !== '' && groups.length>0;
```

Hmm — hasQuery: if query text non-empty. If groups.length===0 but query text non-empty (e.g., "AND"), no constraints — treat as no query. Let me define hasQuery = groups.length > 0. Then empty-text records match when no groups. OK consistent with earlier decision.

Wait, subtle: query "NOT detention" → groups.length=1 → hasQuery true → empty text excluded. Good.

```js
  const results = pool.filter(r => matchesQuery(r, groups));
  results.sort(cmp); // year desc, nulls last, then symbol, then paragraph
```

Count line & chart & cards.

Chart: counts per committee among results:
```js
const byComm = {};
results.forEach(r=>{ const c = r.committee || 'Unknown'; byComm[c]=(byComm[c]||0)+1; });
const labels = Object.keys(byComm).sort((a,b)=> byComm[b]-byComm[a] || a.localeCompare(b));
```

If labels.length: draw; else show "No matches to chart." in chartbox (replace canvas with message? Keep canvas but draw empty and add note). I'll toggle: if no labels, hide canvas, show a p element "Nothing to chart — no paragraphs match."

Chart.js instance management:
```js
let chart=null;
function drawChart(labels, data){
  if(chart){ chart.destroy(); chart=null; }
  if(!labels.length){ canvas hidden; msg shown; return; }
  show canvas, hide msg;
  chart = new Chart(ctx, {type:'bar', data:{labels, datasets:[{label:'Matching paragraphs', data, backgroundColor:'#1f6fb2'}]}, options:{...}});
}
```

Options: responsive true, maintainAspectRatio false; plugins.legend.display false; scales.y beginAtZero, ticks stepSize 1 (precision 0). x ticks autoSkip false? With ~10 committees fine; maybe maxRotation 45. Keep defaults with some tuning.

Cards render (cap 300):

```js
const CAP = 300;
const shown = results.slice(0, CAP);
let html = '';
shown.forEach((r, i) => {
  const title = r.short_title || r.title || r.symbol || '';
  const yearTxt = (typeof r.year === 'number') ? r.year : 'year unknown';
  const symTxt = r.symbol || '(no symbol)';
  const symHtml = r.doc_url ? `<a href="${escapeHtml(r.doc_url)}" target="_blank" rel="noopener">${escapeHtml(symTxt)}</a>` : escapeHtml(symTxt);
  const bodyHtml = r.text ? renderHighlighted(r.text, hlRe) : '<span class="notext">(no text in the data)</span>';
  const citation = makeCitation(r);
  html += `<article class="card"> ... </article>`;
});
```

For citation button: data-i index; store shown array in `shownRecs`.

makeCitation: 
```js
function makeCitation(r){
  if(r.paragraph == null) return r.symbol || '';
  return (r.symbol||'') + ', para. ' + r.paragraph;
}
```

Copy handler (delegated):
```js
resultsEl.addEventListener('click', e=>{
  const btn = e.target.closest('button.copy-btn');
  if(!btn) return;
  const r = shownRecs[+btn.dataset.i];
  copyText(makeCitation(r), btn);
});
```

copyText with "Copied" for 2s:
```js
function copyText(str, btn){
  const restore = ()=>{ btn.textContent='Copy citation'; btn.classList.remove('copied'); };
  const done = ()=>{ btn.textContent='Copied'; btn.classList.add('copied'); clearTimeout(btn._t); btn._t=setTimeout(restore, 2000); };
  const fallback = ()=>{ ...execCommand...; done(); };
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(str).then(done, fallback); } else fallback();
}
```

Truncation note: if results.length > CAP, append note paragraph.

Empty results: `<p class="empty">No paragraph contains these words.</p><p class="tip">Tip: try OR between alternatives, or remove some words to broaden the search.</p>`

Count note ("How this is computed" near numbers): "How this is computed: the committee and year filters are applied first; M counts the paragraphs left after filtering; N counts those whose text matches the search. The chart and the cards below use the same list, so the bars add up to N."

Chart note: "How this is computed: each bar counts the matching paragraphs (after filters and search) whose committee field equals that committee. Committees with no matching paragraphs are omitted."

Count line building:
```js
const filtersDesc = `committee: ${committeeSel.value === 'All' ? 'All' : committeeSel.value}, year: ${yearDesc(fromV,toV)}, search: ${currentQuery.trim()? '“'+currentQuery.trim()+'”' : 'none'}`;
countLine.innerHTML = `<strong>${results.length}</strong> paragraph${...} match out of ${pool.length} (after filters) — filters: ${escapeHtml(filtersDesc)}`;
```

Careful with quotes inside innerHTML — escape. I'll build with textContent where possible but want bold N. Use innerHTML with escaped pieces.

yearDesc: 
```js
function yearDesc(f,t){
  if(f==null && t==null) return 'all years';
  if(f!=null && t!=null) return f+'–'+t;
  if(f!=null) return 'from '+f;
  return 'up to '+t;
}
```

yearOk:
```js
function yearOk(r, f, t){
  if(f==null && t==null) return true;
  if(typeof r.year !== 'number') return false;
  if(f!=null && r.year < f) return false;
  if(t!=null && r.year > t) return false;
  return true;
}
```

Sorting comparator:
```js
function cmp(a,b){
  const ya = typeof a.year==='number'? a.year : -Infinity;
  const yb = typeof b.year==='number'? b.year : -Infinity;
  if(yb!==ya) return yb-ya;
  const sa = a.symbol||''; const sb = b.symbol||'';
  if(sa!==sb) return sa.localeCompare(sb);
  return (a.paragraph||0)-(b.paragraph||0);
}
```

Wait, unknown year last: using -Infinity puts them last in desc order. But spec doesn't say; fine.

Number inputs: set min/max attributes from data year range, placeholder.

Initial render on load: currentQuery='' → all pool shown (capped at 300). Fine.

Prevent number input from triggering on Enter causing form submit — no form element, fine. But Enter in number input: no search button association; ok. Also add Enter handler on search input.

Also help text placement. Good.

Accessibility: labels for inputs, aria-live on count? Add aria-live="polite" to countLine. Nice.

CSS details:

```css
:root { --accent:#1f6fb2; --bg:#f5f7fa; --ink:#1c2733; --muted:#5a6b7b; --line:#d9e1e8; }
* { box-sizing:border-box; }
body { margin:0; padding:32px 40px 64px; font:16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color:var(--ink); background:var(--bg); }
.wrap { max-width:1080px; margin:0 auto; }
h1 { font-size:26px; margin:0 0 6px; color:var(--accent); } 
```

Hmm h1 in ink with accent underline? Keep h1 dark, accent used for buttons/links/bars.

Search row: input flex 1, padding 10px 12px, border 1px solid line, radius 6px, font 16px. Button accent bg white text, radius 6px, cursor pointer.

Filters row: flex, gap 20px, margin-top 14px. Labels with small text.

Cards: white bg, border, radius 8px, padding 16px 18px, margin-bottom 14px. Card head: flex wrap, gap 10px, align baseline; committee as chip (accent-tinted bg #e7f0f8, accent text, small bold); title normal weight italic? keep plain; year muted; symbol link accent, margin-left auto, font-family monospace-ish? Symbols look good in monospace but system fonts only — use monospace stack (allowed, it's a system font). `font-family: ui-monospace, "SF Mono", Consolas, monospace;` fine, not loading external font.

Text: white-space: pre-wrap; word-break: break-word? Long URLs... use overflow-wrap:anywhere. Font size 15.5px. Keep character-for-character with pre-wrap.

mark { background:#ffe58f; padding:0 1px; border-radius:2px; } — use a yellow highlight; accent-tinted could conflict. Yellow is readable.

Copy button: small, border 1px solid accent, accent text, transparent bg; .copied state: accent bg white text.

Chart box: white card, padding, height 240px canvas wrap.

Empty state styling.

Note class: font-size 13px, color muted, margin small.

Let me also think about performance: pool filtering + regex tests over possibly thousands of records per keystroke? Searches only on button/Enter/filter change, fine.

renderHighlighted per card — fine for 300.

Now, edge: query with only phrases quoted with nothing — handled.

One more check on test 1: `"best interests" AND child` — tokens: phrase "best interests", word "AND", word "child". Parser: phrase positive, AND skipped, child positive. Group matches texts containing both. Highlight regex: patterns: phrase-pattern "best interests" (longer) then "child". Both highlighted. ✓.

Test 2: `torture NOT detention` → group: torture positive, detention negated. ✓ no card contains detention.

Test 3: CRC filter → pool = CRC records; chart single CRC bar = N ✓.

Test 4: copy citation → `CRC/C/GC/14, para. 6` format ✓.

Test 5: symbol links target _blank ✓.

Also ensure the count line "out of M" — with CRC filter M = CRC pool size. And "filters: …" lists them.

Now, one subtlety: the phrase pattern `ws.join('\\s+')` — with 'u' flag \s fine. Also case-insensitive 'i'.

Another subtlety: lookbehind at string start works fine.

Unicode 'u' flag and escapeRe: escaped characters like \\$ — fine. But 'u' flag disallows unescaped identity escapes of letters? In annex B... In u mode, escapes like \- or \' are syntax errors! escapeRe escapes: . * + ? ^ $ { } ( ) | [ ] \ — escaping these with backslash is valid in u mode (they're not letters). OK.

But wait: what if a search word contains a character like "/" — no escaping needed, fine in RegExp.

Now write count of lines — aim ~500.

Also the "How this is computed" note near count — I'll put one note under countLine covering N/M, and one under chart.

Additionally: description line must include source, n, years — done.

Let me now also handle Chart availability: if window.Chart undefined (shouldn't be), show note instead. Minor guard.

Write final HTML.

Also: number inputs width ~100px. Committee select styling minimal.

Let me write out the code fully and carefully.

Regarding shownRecs and data-i: also need truncation note.

Also highlight regex rebuilt each render (cache by query string maybe — fine to rebuild).

One more detail: `matchesQuery` when groups empty returns true, but empty-text rule — with no query, empty text records appear in results. Their card shows "(no text in the data)". OK.

Also, when query has groups but consists of... fine.

Let me write it.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments search</title>
<style>
  :root{ --accent:#1f6fb2; --accent-soft:#e7f0f8; --bg:#f5f7fa; --ink:#1d2a36; --muted:#5b6b7a; --line:#d8e0e8; }
  *{ box-sizing:border-box; }
  body{ margin:0; padding:28px 36px 70px; background:var(--bg); color:var(--ink);
        font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif; }
  .wrap{ max-width:1060px; margin:0 auto; }
  h1{ font-size:27px; margin:0 0 4px; }
  #dataLine{ margin:0 0 22px; color:var(--muted); font-size:15px; }
  .panel{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px 20px; margin-bottom:18px; }
  .searchrow{ display:flex; gap:10px; }
  #q{ flex:1; padding:10px 12px; font:inherit; border:1px solid var(--line); border-radius:6px; }
  #q:focus{ outline:2px solid var(--accent-soft); border-color:var(--accent); }
  #searchBtn{ padding:10px 22px; font:inherit; font-weight:600; color:#fff; background:var(--accent); border:none; border-radius:6px; cursor:pointer; }
  #searchBtn:hover{ background:#185a92; }
  .help{ margin:10px 0 0; font-size:14px; color:var(--muted); }
  .help code{ background:var(--accent-soft); padding:1px 5px; border-radius:4px; }
  .filters{ display:flex; flex-wrap:wrap; gap:16px 26px; margin-top:16px; align-items:end; }
  .filters label{ font-size:14px; color:var(--muted); display:flex; flex-direction:column; gap:4px; }
  .filters select,.filters input{ font:inherit; padding:7px 9px; border:1px solid var(--line); border-radius:6px; background:#fff; }
  .filters input{ width:110px; }
  #countLine{ font-size:16px; margin:0 0 4px; }
  .note{ font-size:13px; color:var(--muted); margin:4px 0 16px; }
  .chartbox h2{ font-size:17px; margin:0 0 12px; }
  .chartwrap{ position:relative; height:230px; }
  .card{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:14px 18px 12px; margin-bottom:13px; }
  .cardhead{ display:flex; flex-wrap:wrap; gap:8px 12px; align-items:baseline; margin-bottom:8px; }
  .chip{ background:var(--accent-soft); color:var(--accent); font-size:13px; font-weight:700; padding:2px 9px; border-radius:11px; }
  .ctitle{ font-size:15px; }
  .cyear{ color:var(--muted); font-size:14px; }
  .csym{ margin-left:auto; font-size:14px; font-family:ui-monospace,"SF Mono",Consolas,"Liberation Mono",monospace; }
  .csym a{ color:var(--accent); text-decoration:none; }
  .csym a:hover{ text-decoration:underline; }
  .ctext{ white-space:pre-wrap; overflow-wrap:anywhere; margin:0 0 10px; font-size:15.5px; }
  mark{ background:#ffe58f; color:inherit; padding:0 1px; border-radius:2px; }
  .copy-btn{ font:inherit; font-size:14px; color:var(--accent); background:#fff; border:1px solid var(--accent); border-radius:6px; padding:5px 14px; cursor:pointer; }
  .copy-btn.copied{ background:var(--accent); color:#fff; }
  .empty{ font-size:18px; font-weight:600; }
  .tip{ color:var(--muted); }
  .trunc{ color:var(--muted); font-size:14px; margin-top:6px; }
  .notext{ color:var(--muted); font-style:italic; }
</style>
</head>
<body>
<div class="wrap">
  <h1>General Comments search</h1>
  <p id="dataLine"></p>

  <div class="panel">
    <div class="searchrow">
      <input id="q" type="text" spellcheck="false" placeholder='Search the text of the paragraphs, e.g. "best interests" AND child' aria-label="Search words">
      <button id="searchBtn" type="button">Search</button>
    </div>
    <p class="help">Words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Plain words match whole words only ("right" does not match "rights"). Example: <code>"best interests" AND child</code>.</p>
    <div class="filters">
      <label>Committee <select id="committee"></select></label>
      <label>Year from <input id="fromY" type="number"></label>
      <label>Year to <input id="toY" type="number"></label>
    </div>
  </div>

  <p id="countLine" aria-live="polite"></p>
  <p class="note" id="countNote">How this is computed: the committee and year filters are applied first; the second number counts the paragraphs left after filtering, and the first counts those whose text matches the search. The chart and the cards use this same list, so the bars add up to the first number.</p>

  <div class="panel chartbox">
    <h2>Matching paragraphs by committee</h2>
    <div class="chartwrap"><canvas id="chart"></canvas></div>
    <p id="noChart" style="display:none;">Nothing to chart: no paragraphs match the current filters and search.</p>
    <p class="note">How this is computed: each bar counts the matching paragraphs (after filters and search) grouped by their committee field. Committees with no matching paragraph are omitted, so the bars always add up to the number of matching paragraphs.</p>
  </div>

  <div id="results"></div>
</div>
<script>
(function(){
"use strict";
var GC = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc) || {};
var recs = Array.isArray(GC.records) ? GC.records : [];

/* ---------- header line ---------- */
(function(){
  var el = document.getElementById('dataLine');
  if(!recs.length){ el.textContent = 'No General Comment data is loaded.'; return; }
  var min = null, max = null;
  recs.forEach(function(r){
    if(typeof r.year === 'number'){ if(min===null||r.year<min)min=r.year; if(max===null||r.year>max)max=r.year; }
  });
  var src = GC.source || GC.title || 'unknown source';
  el.textContent = 'Source: ' + src + ' \u00b7 ' + recs.length + ' paragraphs' +
    (min!==null ? ' \u00b7 ' + min + '\u2013' + max : ' \u00b7 year range unknown');
  var f = document.getElementById('fromY'), t = document.getElementById('toY');
  if(min!==null){ f.min = t.min = min; f.max = t.max = max; f.placeholder = String(min); t.placeholder = String(max); }
})();
```

Hmm, "one line: source, number of paragraphs, year range". Good.

Committee select population:

```js
var committees = [];
recs.forEach(function(r){ if(r.committee && committees.indexOf(r.committee)===-1) committees.push(r.committee); });
committees.sort();
var commSel = document.getElementById('committee');
['All'].concat(committees).forEach(function(c){
  var o = document.createElement('option'); o.value = c; o.textContent = c; commSel.appendChild(o);
});
```

Query parsing (ES5-ish or modern? Use modern JS; browsers fine).

I'll write with const/let and arrow functions, template literals — fine.

Full script continues:

```js
/* ---------- query parsing ---------- */
function tokenize(q){
  const tokens = [];
  let i = 0;
  while(i < q.length){
    const ch = q[i];
    if(ch === '"'){
      let end = q.indexOf('"', i+1);
      let val, next;
      if(end === -1){ val = q.slice(i+1).trim(); next = q.length; }
      else { val = q.slice(i+1, end).trim(); next = end+1; }
      if(val) tokens.push({kind:'phrase', v:val});
      i = next;
    } else if(/\s/.test(ch)){
      i++;
    } else {
      let j = i;
      while(j < q.length && !/\s/.test(q[j]) && q[j] !== '"') j++;
      tokens.push({kind:'word', v:q.slice(i,j)});
      i = j;
    }
  }
  return tokens;
}

function parseQuery(q){
  const tokens = tokenize(q);
  const groups = [];
  let cur = [];
  for(let k=0;k<tokens.length;k++){
    const t = tokens[k];
    if(t.kind==='word' && t.v==='OR'){
      if(cur.length) groups.push(cur);
      cur = [];
    } else if(t.kind==='word' && t.v==='NOT'){
      const nxt = tokens[k+1];
      if(nxt && !(nxt.kind==='word' && (nxt.v==='OR'||nxt.v==='NOT'||nxt.v==='AND'))){
        cur.push({neg:true, phrase:nxt.kind==='phrase', v:nxt.v});
        k++;
      }
    } else if(t.kind==='word' && t.v==='AND'){
      /* AND is the default: ignore */
    } else {
      cur.push({neg:false, phrase:t.kind==='phrase', v:t.v});
    }
  }
  if(cur.length) groups.push(cur);
  return groups;
}
```

Hmm — I added guard so NOT doesn't swallow operator words. If "NOT OR" appears — weird, ignore NOT. Fine.

escapeRe and patterns:

```js
function escapeRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
const B0 = '(?<![\\p{L}\\p{N}])', B1 = '(?![\\p{L}\\p{N}])';
function termPattern(t){
  if(t.phrase){
    const ws = t.v.split(/\s+/).filter(Boolean).map(escapeRe);
    if(!ws.length) return null;
    return B0 + '(?:' + ws.join('\\s+') + ')' + B1;
  }
  return B0 + escapeRe(t.v) + B1;
}
const testCache = new Map();
function testRegex(t){
  const key = (t.neg?'-':'+') + (t.phrase?'p':'w') + '\u0001' + t.v;
  if(!testCache.has(key)){
    const p = termPattern(t);
    testCache.set(key, p ? new RegExp(p, 'iu') : null);
  }
  return testCache.get(key);
}
function matchesQuery(r, groups){
  if(!groups.length) return true;
  const text = r.text || '';
  if(!text.trim()) return false;
  return groups.some(g => g.every(t => {
    const re = testRegex(t);
    const hit = re ? re.test(text) : false;
    return t.neg ? !hit : hit;
  }));
}
function highlightRegex(groups){
  const pats = [];
  groups.forEach(g => g.forEach(t => { if(!t.neg){ const p = termPattern(t); if(p) pats.push(p); } }));
  if(!pats.length) return null;
  pats.sort((a,b) => b.length - a.length);
  try { return new RegExp('(?:' + pats.join('|') + ')', 'giu'); }
  catch(e){ return null; }
}
```

Note: if a term pattern is null (empty phrase) but term exists — matches: re null → hit false → positive term fails → no match. Edge, fine.

escapeHtml + renderHighlighted:

```js
function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function renderHighlighted(text, re){
  if(!re) return escapeHtml(text);
  let out = '', last = 0, m;
  re.lastIndex = 0;
  while((m = re.exec(text)) !== null){
    out += escapeHtml(text.slice(last, m.index)) + '<mark>' + escapeHtml(m[0]) + '</mark>';
    last = m.index + m[0].length;
    if(m[0].length === 0) re.lastIndex++;
  }
  return out + escapeHtml(text.slice(last));
}
```

Filters helpers, sorting, citation, state, render, chart, copy — then wire events, initial render.

```js
const fromY = document.getElementById('fromY'), toY = document.getElementById('toY');
const resultsEl = document.getElementById('results');
const countLine = document.getElementById('countLine');
let currentQuery = '';
let shownRecs = [];
const CAP = 300;

function numOrNull(el){ const v = el.value.trim(); if(v==='') return null; const n = parseInt(v,10); return isNaN(n)?null:n; }
function yearOk(r, f, t){
  if(f===null && t===null) return true;
  if(typeof r.year !== 'number') return false;
  if(f!==null && r.year < f) return false;
  if(t!==null && r.year > t) return false;
  return true;
}
function yearDesc(f,t){
  if(f===null && t===null) return 'all years';
  if(f!==null && t!==null) return f + '\u2013' + t;
  if(f!==null) return 'from ' + f;
  return 'up to ' + t;
}
function cmp(a,b){
  const ya = typeof a.year==='number' ? a.year : -Infinity;
  const yb = typeof b.year==='number' ? b.year : -Infinity;
  if(ya!==yb) return yb-ya;
  const sa = a.symbol||'', sb = b.symbol||'';
  if(sa!==sb) return sa.localeCompare(sb);
  return (a.paragraph||0)-(b.paragraph||0);
}
function makeCitation(r){
  if(r.paragraph == null) return r.symbol || '';
  return (r.symbol||'') + ', para. ' + r.paragraph;
}
```

Chart:

```js
let chart = null;
function drawChart(labels, data){
  const canvas = document.getElementById('chart');
  const noChart = document.getElementById('noChart');
  if(chart){ chart.destroy(); chart = null; }
  if(!labels.length || typeof window.Chart === 'undefined'){
    canvas.style.display = 'none';
    noChart.style.display = 'block';
    if(typeof window.Chart === 'undefined' && labels.length) noChart.textContent = 'Chart library not available in this sandbox; the counts per committee cannot be drawn.';
    return;
  }
  canvas.style.display = 'block';
  noChart.style.display = 'none';
  chart = new window.Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: { labels: labels, datasets: [{ label: 'Matching paragraphs', data: data, backgroundColor: '#1f6fb2', maxBarThickness: 70 }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { callbacks: {} } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: 'Matching paragraphs' } },
        x: { ticks: { maxRotation: 45, minRotation: 0 } }
      }
    }
  });
}
```

Render:

```js
function render(){
  const comm = commSel.value;
  const f = numOrNull(fromY), t = numOrNull(toY);
  const pool = recs.filter(r => (comm==='All' || r.committee===comm) && yearOk(r, f, t));
  const groups = parseQuery(currentQuery);
  const results = pool.filter(r => matchesQuery(r, groups)).sort(cmp);
  const hl = highlightRegex(groups);

  // count line
  const qTxt = currentQuery.trim();
  const filtersTxt = 'committee: ' + comm + ' \u00b7 year: ' + yearDesc(f,t) +
    ' \u00b7 search: ' + (qTxt ? '\u201c' + qTxt + '\u201d' : 'none');
  countLine.innerHTML = '<strong>' + results.length + '</strong> paragraph' + (results.length===1?'':'s') +
    ' match out of ' + pool.length + ' (after filters) \u2014 filters: ' + escapeHtml(filtersTxt);

  // chart
  const byComm = {};
  results.forEach(r => { const c = r.committee || 'Unknown'; byComm[c] = (byComm[c]||0)+1; });
  const labels = Object.keys(byComm).sort((a,b) => (byComm[b]-byComm[a]) || a.localeCompare(b));
  drawChart(labels, labels.map(c => byComm[c]));

  // results
  shownRecs = results.slice(0, CAP);
  if(!results.length){
    resultsEl.innerHTML = '<p class="empty">No paragraph contains these words.</p>' +
      '<p class="tip">Tip: try OR between alternatives, or use fewer words to broaden the search.</p>';
    return;
  }
  let html = '';
  shownRecs.forEach((r, i) => {
    const title = r.short_title || r.title || r.symbol || '(untitled)';
    const yearTxt = typeof r.year === 'number' ? String(r.year) : 'year unknown';
    const sym = r.symbol || '(no symbol)';
    const symHtml = r.doc_url
      ? '<a href="' + escapeHtml(r.doc_url) + '" target="_blank" rel="noopener">' + escapeHtml(sym) + '</a>'
      : escapeHtml(sym);
    const bodyHtml = (r.text && r.text.trim()) ? renderHighlighted(r.text, hl)
      : '<span class="notext">(this paragraph has no text in the data)</span>';
    html += '<article class="card">' +
      '<div class="cardhead">' +
        '<span class="chip">' + escapeHtml(r.committee || 'Unknown') + '</span>' +
        '<span class="ctitle">' + escapeHtml(title) + '</span>' +
        '<span class="cyear">' + escapeHtml(yearTxt) + '</span>' +
        '<span class="csym">' + symHtml + '</span>' +
      '</div>' +
      '<p class="ctext">' + bodyHtml + '</p>' +
      '<button type="button" class="copy-btn" data-i="' + i + '">Copy citation</button>' +
    '</article>';
  });
  if(results.length > CAP){
    html += '<p class="trunc">Showing the first ' + CAP + ' of ' + results.length +
      ' matching paragraphs. Refine the search or the filters to shorten the list \u2014 the count and the chart above already cover all matches.</p>';
  }
  resultsEl.innerHTML = html;
}
```

Wait — renderHighlighted on r.text: r.text could be undefined; guarded.

Copy handling:

```js
resultsEl.addEventListener('click', function(e){
  const btn = e.target.closest ? e.target.closest('.copy-btn') : null;
  if(!btn) return;
  const r = shownRecs[parseInt(btn.getAttribute('data-i'),10)];
  if(!r) return;
  copyText(makeCitation(r), btn);
});
function copyText(str, btn){
  const done = function(){
    btn.textContent = 'Copied';
    btn.classList.add('copied');
    clearTimeout(btn._t);
    btn._t = setTimeout(function(){ btn.textContent = 'Copy citation'; btn.classList.remove('copied'); }, 2000);
  };
  const fallback = function(){
    const ta = document.createElement('textarea');
    ta.value = str;
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch(err){}
    document.body.removeChild(ta);
    done();
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(str).then(done, fallback);
  } else { fallback(); }
}
```

Note: resultsEl.innerHTML replaced but btn._t timer references old button — after re-render, old button gone; fine.

Events:

```js
document.getElementById('searchBtn').addEventListener('click', function(){
  currentQuery = document.getElementById('q').value;
  render();
});
document.getElementById('q').addEventListener('keydown', function(e){
  if(e.key === 'Enter'){ e.preventDefault(); currentQuery = this.value; render(); }
});
commSel.addEventListener('change', render);
fromY.addEventListener('change', render);
toY.addEventListener('change', render);
render();
```

If no data: render handles empty — countLine "0 paragraphs match out of 0", chart noChart shown, empty message. Slightly odd but data exists per attachment. Add early guard maybe: if !recs.length, skip events? render works fine anyway. Keep.

One thing: number input 'change' fires on blur even if unchanged — render anyway, harmless.

Chart y-axis title 'Matching paragraphs' good.

Also, spec: "A small bar chart: matching paragraphs per committee for the current search" — with no query, chart shows pool by committee. Fine.

Check countLine: "N paragraphs match out of M (after filters) — filters: …". Matches spec pattern.

Check "How this is computed" notes present near count and chart. ✓.

Now check the whole under 700 lines — yes, ~430.

One more consideration: highlight regex global flag + 'iu'. termPattern uses lookbehind — combined regex also uses lookbehind inside alternatives: `(?:(?<!...)\w+(?!...)|...)` — lookbehind inside alternation is fine.

Potential problem: regex alternation with lookbehind at same start position: e.g., text "child" and patterns for "child" and phrase "child rights": at position of "child", phrase pattern requires "child\s+rights" — matches "child rights" wholly, marking both words as one mark. And "child" alone pattern would match at same position but phrase alternative is first (longer pattern sorted first) → phrase wins. Then next exec continues after "rights". Good — test 1 highlights "best interests" as a phrase mark and "child" separately.

Edge: overlapping like "rights" and "right" — "right" pattern shorter sorted later; at "rights", "right" pattern's lookahead (?![\p{L}\p{N}]) fails after "right" (next is 's'), so no match anyway. Good.

What about phrase "best interests" where text has "best  interests" (double space) — \s+ handles.

What about text with "best-interests" hyphen? \s+ won't match hyphen — phrase not found. "Exact sequence of words" — acceptable.

Now the help line mentions example. Spec item 2 exact-ish text: 'words are combined with AND unless you write OR; NOT excludes a word; "quotes" find an exact phrase. Example: "best interests" AND child'. I included plus whole-word note. Good.

Double-check spec item 1: "Title 'General Comments search' and one line: source, number of paragraphs, year range, all read from the data." ✓.

Item 3: "Two filters: committee (every committee in the data, plus 'All') and year (from–to). Changing a filter re-runs the search." ✓.

Item 6: "sorted newest General Comment first" ✓ (year desc).

Citation example "CCPR/C/GC/37, para. 12" ✓ format.

I think the app is complete. Let me also make sure no external resources. Chart.js from window.Chart ✓. Fonts system ✓.

Also: base font 16px ✓; accent #1f6fb2 ✓.

Write final answer: ≤3 sentences before code block, nothing after.

Let me count lines roughly to stay under 700 — fine.

One more check on `tokenize` regex `/\s/.test(q[j])` — q[j] single char, fine.

In parseQuery, guard for NOT: `if(nxt && !(nxt.kind==='word' && (nxt.v==='OR'||nxt.v==='AND'||nxt.v==='NOT')))`. If NOT is last token, nxt undefined → ignore. Good.

Hmm, one subtle thing about `hasQuery` and the "search: none" display: if user typed "AND" only, groups empty, matches all, but filters say search: "AND". Slightly inconsistent but harmless; count line shows search text as typed. Fine.

Also initial page: countLine "3,460 paragraphs match out of 3,460 (after filters) — filters: committee: All · year: all years · search: none". Wait — no number formatting; plain numbers fine. Maybe toLocaleString for readability. I'll use toLocaleString() for N and M in count line. But test says "the number of cards equals N" — cards capped at 300 might break test 1 if N > 300 for `"best interests" AND child`! Hmm. How many GC paragraphs contain "best interests" AND child? CRC GCs on children... "best interests" appears in many CRC GCs. Could plausibly exceed 300? CRC alone has ~27 GCs; "best interests" mentions per GC maybe a handful. Total maybe 100–300. Risky. The acceptance test: "the number of cards equals N". If I cap at 300 and N=400, test fails.

Options: raise cap to a high number (e.g., 2000) or no cap. Rendering 2000 cards with innerHTML is OK performance-wise (innerHTML parse of ~2000 articles, a few MB — acceptable, maybe 100–300ms). Data size unknown; "the real files are larger" — gc maybe several thousand paragraphs total. Matches for a specific query rarely exceed a few hundred. I'll set CAP = 1000 and keep truncation note. Or... make CAP = 500? Test risk: N up to 500 covered. Hmm.

Alternatively no cap at all — simplest and always passes the test. Downside: empty query shows every paragraph (could be 5k cards, heavy but one-time; innerHTML with 5k articles might take a second and lots of DOM, but browsers handle it; memory fine).

The plan says nothing about capping; "keep it simple". I'll set CAP high (2000) with note — balances. Hmm, but if N=2500? For query "the"... users won't. Empty query shows all though! Initial load with no query shows ALL records. If dataset is 5k, initial render = 5k cards. With CAP 2000 + note. That's fine.

Actually, wait: does initial no-query show all? Yes per my design. That's per spec ambiguity ("search tool" — initially showing everything is typical). OK: CAP = 2000.

Let me finalize. Also add `type="button"` on Search button (no form anyway).

Also `resultsEl.addEventListener('click', ...)` — e.target.closest exists on elements; if click on text node? e.target is element. Fine.

Also one detail: `.csym` uses margin-left:auto to push right.

Regarding `data-i` and rerender timing with "Copied" — fine.

Final code assembly. Also make sure the script is wrapped and runs after DOM (script at end of body) ✓.

Line count estimate: CSS ~60 lines, HTML ~50, JS ~250. Total ~380. Good.