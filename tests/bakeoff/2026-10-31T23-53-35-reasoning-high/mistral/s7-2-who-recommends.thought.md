Let me understand the task. Add a tab "Who recommends what" to the existing dashboard. For UPR recommendations only (mechanism === "Universal Periodic Review" and type === "Recommendations"), extract the recommending State from the last parentheses in the text via regex. Show top 15 States by count as a bar chart, plus a small table of the SDGs each of them raises most. Clicking a State lists its recommendations with symbols. Also report how many UPR recommendations had no State in parentheses.

I need to return the whole HTML file again, complete, with the new tab added. Keep under ~700 lines. Tabs: I'll add a tab bar with "Dashboard" and "Who recommends what". The second tab contains: note about method, count of UPR recommendations with/without state, bar chart of top 15 states, table of top SDGs per state (for top states — probably top 15 states, each with their most-raised SDGs), and a clickable list: clicking a state shows its recommendations with symbols (linked).

Design: tab buttons at top. Tab panels. Keep all existing functionality.

Extraction regex: last parentheses at end of text, e.g. "…for all children (Croatia)." The text may end with "(Croatia)." or "(Croatia)". Regex: /\(([^()]*)\)\s*\.?\s*$/ — take the last parentheses group at the end. But some texts may have trailing content. The spec says "A regex on the last parentheses extracts it." So use something like /\(([^()]+)\)\s*\.?\s*$/ and take group 1. Handle multiple states in parentheses? e.g. "(Croatia and France)" — just take the whole content as the state string? The instruction says "take the recommending State from the parentheses at the end". I'll take the content of the last parentheses; if it contains multiple, maybe split on " and "/","? Safer: keep the raw content as the state label, but maybe split on commas/"and"? Hmm. The data description says UPR recommendations end with the recommending State in parentheses, e.g. "…for all children (Croatia)." Singular. I'll take the full content of the last parentheses as the recommending state, but trim. Maybe also handle cases where parentheses contain something like "Croatia (on behalf of...)"? Keep simple: content of last parentheses group at end of text. If empty or missing → no state.

Actually, to be a bit more robust, I could split the content on " and " or ", " to attribute to multiple states? That risks inventing. The spec says the recommending State (singular). I'll keep the whole string as one state label. But maybe normalize whitespace.

Count: UPR recommendations = records where mechanism === "Universal Periodic Review" and type === "Recommendations". Hmm — should I filter type === "Recommendations"? The user says "For UPR recommendations only". The data has type mostly "Recommendations" or "Concerns/Observations". UPR records with type "Concerns/Observations" probably don't end with a state. I'll filter mechanism === "Universal Periodic Review" && type === "Recommendations". But maybe safer: mechanism UPR and type Recommendations; if type missing, include? I'll require type === "Recommendations" but if a UPR record has no type, include it? Let me just do: mechanism === 'Universal Periodic Review' && (type === 'Recommendations' || !type). Hmm, simpler: mechanism UPR and type 'Recommendations'. I'll note on screen the filter used. Actually to be safe and honest, I'll define UPR recs as mechanism === "Universal Periodic Review" and type === "Recommendations", and state that on screen. If zero, fall back? No — keep deterministic, show what's missing. Actually let me include UPR records where type is "Recommendations" OR type is missing/empty, since "UPR recommendations" primarily means mechanism UPR + type Recommendations. Hmm, I'll do: mechanism === 'Universal Periodic Review' && String(type).toLowerCase().indexOf('recommendation') === 0? Overkill. Keep: mechanism === 'Universal Periodic Review' && type === 'Recommendations'. And display "n UPR recommendations (mechanism = Universal Periodic Review, type = Recommendations)".

Wait — but maybe in the real data, UPR records all have type "Recommendations". Fine.

Extraction: 
```js
function recommendingState(text){
  var t = String(text||'').trim();
  var m = t.match(/\(([^()]*)\)\s*\.?\s*$/);
  if(!m) return null;
  var s = m[1].trim();
  return s || null;
}
```
But what if text ends with "…(Croatia) " with trailing period after? The regex handles optional period. What if there are multiple trailing parentheses like "(Croatia) (on behalf of X)"? The regex `\(([^()]*)\)\s*\.?\s*$` would match the last one "(on behalf of X)". Hmm. The description says "A regex on the last parentheses extracts it." So last parentheses is intended. OK.

Edge: text like "… (Croatia)." — matches. Text ending without parentheses → null → counted as "no State in parentheses".

Top 15 states bar chart: horizontal bar chart like themes. Use Chart.js. Clicking a state (bar click or a list) shows its recommendations. I'll make the chart clickable via onClick handler mapping index → state, and also render a list of the top 15 states as clickable chips/rows. Simpler: below chart, a list of top states (buttons); clicking selects state and shows its recommendations table below. Also chart onClick selects.

"Small table of the SDGs each of them raises most": a table with rows = top 15 states, columns = "Top SDGs" showing e.g. top 3 SDGs with counts (SDG number + name + count). Maybe columns: State | Recommendations | Most-raised SDGs (top 3, "SDG 16 (n=12)"). That's a small table. Clicking a row selects the state too.

Then a section "Recommendations by [State]" listing its UPR recommendations: date, symbol (linked), first line, expandable full text? The user says "Clicking a State lists its recommendations with symbols." I'll reuse expandable rows for full text — nice consistency. Keep it simpler: rows with date, symbol link, first line; click to expand full text (reuse pattern).

Also show: "X of Y UPR recommendations had no State in parentheses" — count nulls.

Tabs implementation: two buttons "Dashboard" | "Who recommends what". Panels with hidden attribute. Tab switching toggles. When switching to tab 2 first time, render (or render always at load — fine, render at load; charts in hidden canvas: Chart.js with responsive canvas in display:none container can have sizing issues. To avoid, render tab-2 content lazily on first activation, or call chart.resize() when tab shown. I'll render lazily on first show, and also re-render/resize when shown again if needed. Simplest: build tab2 content on first activation; on subsequent activations, if chart exists, call chart.resize(). Actually since filters don't affect tab 2 (it's UPR-only, independent of filters? The user says "For UPR recommendations only" — the tab is about UPR recommendations; should it respect the dashboard filters? The user didn't say to apply filters. I'll make it independent of the dashboard filters but state that clearly: "This tab uses all UPR recommendations in the dataset, regardless of the filters on the Dashboard tab." Hmm, or should it respect filters? Ambiguous. The instruction: "Add a tab 'Who recommends what'. For UPR recommendations only, take the recommending State..." I think it's a separate view over all UPR recommendations. I'll state on screen: uses all UPR recommendation records in the dataset (n=...), independent of dashboard filters. That's honest and clear.

Chart in hidden tab: I'll render tab 2 lazily when first shown. Use a flag.

Let me now write the full file. Keep the existing dashboard code intact, add tab structure.

Structure:
```html
<nav class="tabs">
  <button class="tab active" id="tabBtnDash" data-tab="dash">Dashboard</button>
  <button class="tab" id="tabBtnWho" data-tab="who">Who recommends what</button>
</nav>
<section id="panel-dash"> ...existing cards... </section>
<section id="panel-who" hidden> ... </section>
```

Tab CSS: buttons with bottom border accent when active.

Panel who contents:
- card: "Method" note: UPR recommendations = mechanism "Universal Periodic Review" + type "Recommendations" (n = X). Recommending State = text inside the last parentheses at the end of the recommendation text. Y of X had no State in parentheses (listed as "no State identified"). Exact counts.
- stats row: UPR recommendations total, with State, without State, distinct States.
- card: bar chart top 15 States (canvas + fallback + empty).
- card: table top 15 states: State | # recs | Most-raised SDGs (top 3 with counts). Row click selects state.
- card: selected state detail: heading "Recommendations by X (n)", list of records (date, symbol link, first line, expandable full text). Default select the top state.

State extraction details: also handle text ending with ")" but with trailing whitespace/newline — trim first. Also some might end with "(Croatia)." — ok. Some might have the parentheses not at very end but followed by nothing. Fine.

What about multiple states like "(Croatia, France)"? Keep as one label "Croatia, France"? That would create a weird state. Could split on /,| and /? The spec says singular state. I'll keep raw but maybe normalize: if content matches /^(.+?)(?:\s+and\s+|\s*,\s*)(.+)$/... risky. Keep raw content as the label; it's honest. Actually, hmm — real UPR recommendations sometimes end with "(Croatia)" only. Keep raw.

SDG per state: for each state, count SDGs across its records (each record's sdgs list, dedupe per record). Top 3 SDGs with counts. Display "SDG 16 Peace, justice… (12)". Use sdgNames.

Chart click: chart options onClick: (evt, elements) => if elements[0], select state at index. Also make the state list clickable: I'll render the top-15 table rows clickable, plus maybe a chip list. Table rows clickable is enough, plus chart click. Also add hint text "Click a bar or a row in the table".

Selected state panel: list of its UPR recs sorted by date desc, each row: date, symbol link, first line; click expands full text (reuse detail row pattern). Include count.

Now line count: previous file was maybe ~330 lines. Adding tab 2 adds ~150. Fine under 700.

Let me also make sure the "no State" count is displayed: "Z of X UPR recommendations had no State in parentheses (their text does not end with a parenthesised State)."

Also handle empty: if no UPR recs, show empty message.

Implementation plan in JS:

```js
var uprRecs = records.filter(function(r){
  return String(r.mechanism||'') === 'Universal Periodic Review' && String(r.type||'') === 'Recommendations';
});
```
Hmm, what if mechanism value differs in case? Data says mechanism is one of "Treaty bodies", "Universal Periodic Review", "Special Procedures". Exact match fine. But to be safe use case-insensitive compare? I'll do exact match on 'Universal Periodic Review' but also fallback: if zero results with type filter, try without type filter? That complicates. Let me do: mechanism match (case-insensitive) and type includes 'Recommendation' (case-insensitive) — covers "Recommendations". If type missing, include? I'll include records where type is missing too? "UPR recommendations" — if type missing, ambiguous. I'll require type to contain "recommendation" case-insensitively; if that yields 0 but UPR mechanism records exist, fall back to all UPR mechanism records and note it. Hmm, that's dynamic complexity. Simpler: uprRecs = records where mechanism === 'Universal Periodic Review' (case-insensitive) AND (type missing OR type contains 'recommendation' case-insensitive). And display the exact filter on screen. Actually the user said "For UPR recommendations only" — meaning among UPR records, only recommendations (not concerns/observations). I'll do mechanism UPR + type starts with 'Recommendation' (case-insensitive). And show filter description. If zero, show empty message saying no UPR recommendations found. That's honest.

Hmm, but what if real data has UPR records with type "Recommendations" — yes per description. OK.

State extraction:
```js
function recommendingState(r){
  var t = String(r.text||'').replace(/\s+$/,'');
  var m = t.match(/\(([^()]*)\)[.\s]*$/);
  if(!m) return null;
  var s = m[1].trim();
  return s.length ? s : null;
}
```
Wait `[.\s]*$` after the closing paren — allows trailing period and spaces. But if text ends with "(Croatia) something" it won't match — good, only end.

But careful: text like "... (see para. 5)." would extract "see para. 5" as a state — false positive. Hmm. The description says UPR recommendations end with the recommending State in parentheses, and "A regex on the last parentheses extracts it." So per spec, last parentheses = state. I'll follow spec. Maybe guard: if content looks like "see ..." skip? That would be inventing rules. Follow the spec: last parentheses. But I could note on screen: "State = content of the last parentheses at the end of the text, as in the UPR format." Fine.

Build map state → records:
```js
var stateMap = {}; var noState = [];
uprRecs.forEach(function(r){
  var s = recommendingState(r);
  if(s){ (stateMap[s] = stateMap[s] || []).push(r); }
  else noState.push(r);
});
var stateList = Object.keys(stateMap).map(function(k){ return [k, stateMap[k].length]; })
  .sort(function(a,b){ return b[1]-a[1] || a[0].localeCompare(b[0]); });
var top15 = stateList.slice(0,15);
```

SDG counts per state:
```js
function sdgCounts(recs){
  var m={};
  recs.forEach(function(r){
    var seen={};
    arr(r.sdgs).forEach(function(n){ var k=String(n); if(!seen[k]){seen[k]=1; m[k]=(m[k]||0)+1;} });
  });
  return Object.keys(m).map(function(k){return [k,m[k]];}).sort(function(a,b){return b[1]-a[1]|| (parseInt(a[0],10)-parseInt(b[0],10));});
}
```

Render functions for tab 2: renderWhoStats, renderWhoChart (lazy), renderWhoTable, renderWhoDetail(state).

Chart: horizontal bars, labels = state names (may be long — truncate to ~40 chars for axis, full in tooltip). Click handler selects state.

Table: columns State | Recommendations | Most-raised SDGs (top 3). Row click → selectState(name); highlight selected row.

Detail: heading + count + list. Reuse expandable rows: I'll write a generic row builder or duplicate small code. I'll write renderWhoDetail with rows similar to dashboard table but simpler: date, symbol link, first line; click expands full text. Use event delegation on the detail tbody.

Tab switching:
```js
var whoRendered = false;
function showTab(name){
  document.querySelectorAll('.tab').forEach(...);
  $('panel-dash').hidden = name!=='dash';
  $('panel-who').hidden = name!=='who';
  if(name==='who' && !whoRendered){ renderWho(); whoRendered=true; }
  if(name==='who' && whoChart){ whoChart.resize(); }
}
```
Since panel-who is hidden at load, Chart.js canvas has 0 size; rendering lazily on first show avoids the issue. On subsequent shows, resize.

Also note: dashboard chart is in visible panel at load — fine.

Now write the whole file. Also update header lede maybe mention tabs? Not needed.

CSS additions: .tabs, .tab buttons, .tab.active, selected row highlight (.sel), state list maybe. Also .who-* styles reuse.

Let me write it carefully.

Also the "small table of the SDGs each of them raises most" — "each of them" = the 15 states. Table rows = 15 states, column with top SDGs. Good.

Also mention in notes: "How this is computed" for each: chart counts, SDG counts (dedupe per record), no-state count.

Edge: state names could be long; truncate label in chart to 45 chars with ellipsis, tooltip shows full.

Let me write the code now.

Full HTML:

I'll keep prior code and add. Let me draft the new script sections.

```js
/* ---------- Tab: Who recommends what ---------- */
var uprRecs = records.filter(function(r){
  return String(r.mechanism||'').toLowerCase() === 'universal periodic review'
      && String(r.type||'').toLowerCase().indexOf('recommendation') === 0;
});
```
Hmm type could be "Recommendations" — indexOf('recommendation')===0 works case-insensitively after toLowerCase. If type missing → '' → indexOf → -1 → excluded. Should missing type be included? "UPR recommendations" — if type missing, we can't know. Exclude, and the note says filter = mechanism UPR + type Recommendations. But what if real data has UPR records with type exactly "Recommendations" — fine.

Actually, safer: include if type is missing? No. Keep strict; display filter. If uprRecs.length===0, show message "No records with mechanism 'Universal Periodic Review' and type 'Recommendations' were found in the dataset." Honest.

recommendingState as above.

renderWho():
- stats: uprRecs.length, withState = uprRecs.length - noState.length, noState.length, distinct states count.
- note text: "n = X UPR recommendations (mechanism = Universal Periodic Review, type = Recommendations). The recommending State is read from the last parentheses at the end of the recommendation text, e.g. '…(Croatia)'. Y of X had no State in parentheses."
- chart top15.
- table top15 with SDGs.
- detail default top state.

selectState(name): update table row highlight, render detail, maybe chart highlight (skip).

Detail list rows: build like dashboard rows with expandable. I'll create tbody id="whoRecBody" and delegation.

Chart click: options.onClick: function(evt, els){ if(els && els.length){ var i = els[0].index; selectState(top15[i][0]); } }.

Also add cursor pointer on chart canvas.

Now, the table "Most-raised SDGs": for each of top15 states, top 3 SDGs: "SDG 16 — Peace, justice and strong institutions (12)". If none: "—".

Write everything. Also ensure no horizontal scroll: table with long SDG names — allow wrapping.

Let me now compose the final file. I'll aim for clean, complete code.

Also keep the intro sentences before code block ≤3 sentences.

One more detail: the tab buttons should be accessible: role="tab", aria-selected. Keep simple.

Line budget fine.

Write final answer.