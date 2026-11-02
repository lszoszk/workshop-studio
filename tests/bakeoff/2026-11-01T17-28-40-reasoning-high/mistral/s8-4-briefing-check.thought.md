Let me understand the task. Build a briefing checker for HRC resolutions:

1. Pick a resolution from recorded votes (dropdown), default A/HRC/RES/51/27.
2. "Ask AI for a briefing" button — calls `await studio.ask(prompt, {json:true})` with only symbol + title (no data sent). Returns 250-word briefing. Put answer in a textarea where user can also paste their own text.
3. "Check" button — parses the text for checkable claims:
   - numbers in favour / against / abstaining (yes/no/abstain counts)
   - the date
   - the session
   - each State said to have voted a certain way (e.g., "Kenya voted in favour", "France voted against", "China abstained")
4. Show a table: claim as written | what recorded vote says | verdict: matches / wrong / cannot be checked.
5. Explain "cannot be checked" ≠ "wrong".

Data: window.WORKSHOP_DATA.hrc with records, countries map ISO3→name, vote_codes.

Design: clean NGO style, accent #1f6fb2, base 16px, no external loads. Chart.js available but maybe not needed — could add a small vote bar chart. Keep under 700 lines.

Key implementation details:

- Resolution picker: select with all records sorted by symbol or date. Default to A/HRC/RES/51/27 if present, else first.
- Show resolution details: symbol, title, kind, date, session, agenda item, sponsors, official totals yes/no/abstain, roll-call counts from votes map, doc_url/record_url links.
- "Ask AI for a briefing" button: builds prompt: "Write a 250-word briefing on UN Human Rights Council resolution {symbol}: {title}. Use only your own knowledge; do not invent..." Send only symbol and title. Show on screen: "Sending 1 record (symbol + title only) to the model — it left the browser." Progress indicator, and a stop button? studio.ask is a single await; can't really cancel, but we can show "waiting" state. The instructions say "let the user stop" — we can provide a stop button that sets a flag; when the promise resolves, if stopped, discard. That's the best we can do.
- Render AI answer inside element with data-source="ai" — the textarea itself should have data-source="ai"? The rule: "Render every value that came from studio.ask inside an element with the attribute data-source="ai"." So when we fill the textarea with AI text, set textarea.setAttribute('data-source','ai'); when user edits/pastes, maybe remove it or keep? If user pastes own text, it's no longer purely AI. I'll set data-source="ai" when AI fills it, and remove it (or set to "user") when the user modifies it. Actually simpler: keep a label showing source. I'll set the attribute on the textarea when AI-generated, and on input event remove it. Hmm, but the checker output table — claims come from the text which may be AI. The claims are extracted from text; the verdicts are deterministic from data. I think marking the textarea is the key requirement. I'll also mark the AI status line.
- Check button: parse text for claims.

Claim extraction — deterministic regexes:

1. Vote counts: patterns like "29 votes in favour", "29 in favour", "16 against", "1 abstention", "adopted by 29 votes in favour, 16 against and 1 abstention", "29-16-1". Need to handle words: in favour/in favor/for, against, abstain/abstention(s). Also "adopted unanimously"? That's not checkable as numbers... could check "unanimously" → no==0 && abstain==0? Maybe treat as cannot be checked or check: if text says "unanimously" and no>0 → wrong. Keep it simpler: extract numeric claims.

Approach: find sentences containing vote-count keywords. Regex for numbers near keywords:
- /(\d+)\s*(?:votes?\s*)?(?:in\s+favo[u]?r|for|supporting)/gi
- /(\d+)\s*(?:votes?\s*)?against/i
- /(\d+)\s*(?:abstentions?|abstaining|abstained)/i
- Also pattern "X–Y–Z" or "X-Y-Z" with context "in favour, against, abstain". E.g. "adopted by 29 votes in favour, 16 against and 1 abstention" — the first regex catches 29 in favour; "16 against" catches; "1 abstention" catches. Good.
- Also "with 29 yes, 16 no and 1 abstention"? Add yes/no keywords: /(\d+)\s*(?:votes?\s*)?yes/i, /(\d+)\s*(?:votes?\s*)?no\b/i — "no" is risky (matches "no" word). Require digit before: "16 no". /(\d+)\s+no\b/ ok.

For each match, record the matched claim text (the phrase), the number, the category (yes/no/abstain), and compare to official totals (yes/no/abstain fields) AND roll-call counts. The spec says "what the recorded vote says" — show both official totals and roll-call count from votes map. Verdict: matches if claim number equals official total (or roll-call count? show both; verdict matches if it matches the official total; if it matches roll-call but not official, verdict could be "matches roll call, differs from official totals" — hmm). The data description says: "Counting votes gives the roll call, which differs from the totals for a few records (gaps in the source): show both rather than silently picking one." So in the table, "what the recorded vote says" column shows e.g. "Official totals: 29 in favour; roll call from votes map: 28". Verdict: matches if number equals official total; if equals roll-call count but not official, verdict "matches the roll call but not the official total" — but allowed verdicts are matches/wrong/cannot be checked. I could make verdict "matches" if it matches either, with note. Better: verdict matches if equals official total; if equals roll-call only, verdict "matches" with note "(roll call; official total differs)". Hmm, keep three verdicts but the "recorded vote says" column shows both numbers, and verdict logic: if claim == official → "matches"; else if claim == rollcall → "matches" (note in column); else "wrong". Actually to be safe and honest: verdict "matches" only when it matches the official recorded totals; if it matches only the roll-call count, say "matches the roll call (official total is X)" — I'll use verdict "matches" with an annotation, or maybe verdict text "matches (roll call)". Let me just do: matches if claim equals official total OR roll-call count; the column explains which. Wrong otherwise. That's defensible.

2. Date: patterns like "7 July 2026", "July 7, 2026", "2026-07-07", "7/7/2026"? Parse dates: 
- ISO: /(\d{4})-(\d{2})-(\d{2})/
- "d Month yyyy": /(\d{1,2})\s+(January|...|December)\s+(\d{4})/i
- "Month d, yyyy": /(January|...)\s+(\d{1,2}),?\s+(\d{4})/i
Compare to record.date (ISO). Verdict matches if same date. If a date is found but different → wrong. If no date found → we don't list a row (only claims found). But maybe also note "no date claim found". The table lists claims found in text.

3. Session: patterns like "51st session", "at its 51st session", "during the 51st session". Extract ordinal number, compare to record.session which is like "51st session" or "Human Rights Council at its 54th session". Parse digits from record.session: /(\d+)/. Claim: /(\d+)(?:st|nd|rd|th)\s+session/i. Compare numbers. Also "session 51"? Add /session\s+(\d+)/i. Verdict matches if equal.

4. States voting a certain way: patterns like "Kenya voted in favour", "France voted against", "China abstained", "X voted yes", "X voted no", "X abstained", "X voted for", "in favour: Kenya, France" hmm. Keep to: State name followed by voted/abstained + way. Regex: /\b([A-Z][A-Za-z'’\-]+(?:\s+(?:of|the|and|de|van|von|al|bin|el))?\s+[A-Z][A-Za-z'’\-]*)\s+(?:voted|vote)\s+(in\s+favo[u]?r|for|against|yes|no|to\s+abstain|abstained)|([A-Z][\w'’\- ]+?)\s+abstained\b/gi — multi-word country names are tricky ("United States", "Russian Federation", "South Africa", "Côte d'Ivoire", "Democratic Republic of the Congo"). Better approach: build a list of country names from WORKSHOP_DATA.hrc.countries (ISO3→name) plus maybe common variants. Then for each name, search text for name followed by a vote phrase within a short window: new RegExp(escape(name) + "\\s+(?:voted|votes|cast[^.]{0,20}?)\\s+(in\\s+favo[u]?r|for|against|yes|no|abstain\\w*)", "i") and also name + " abstained". Also pattern "voted in favour: Kenya" — skip, too complex. Also "Kenya (in favour)"? Skip.

Also handle "X voted against", "X voted in favour", "X abstained", "X voted no", "X voted yes", "X voted for the resolution" → for = yes. Map: in favour/for/yes → Y; against/no → N; abstain* → A.

Then look up ISO3 by name (build reverse map, case-insensitive, also handle "United States of America" vs "United States"? The countries map keys are ISO3 with names; I'll also add aliases: for each name, also try matching without "the"? Keep simple: exact name from map, plus a few manual aliases like "United States" → USA if present, "Russia"/"Russian Federation", "South Korea"/"Republic of Korea", "North Korea"/"Democratic People's Republic of Korea", "Côte d'Ivoire"/"Ivory Coast", "Congo"/"Republic of the Congo" vs "Democratic Republic of the Congo" — careful: "Congo" alone ambiguous. I'll add alias map only when unambiguous: check if alias maps to a unique ISO3 in the countries map. E.g., "Russia" → find name containing "Russian Federation". I'll implement: for each ISO3 name, generate alias = name; plus if name includes "Republic of Korea" alias "South Korea"; "Democratic People's Republic of Korea" → "North Korea"; "United States of America" → "United States"; "Russian Federation" → "Russia"; "Côte d'Ivoire" → "Ivory Coast"; "Viet Nam" → "Vietnam"; "Türkiye" → "Turkey"; "Bolivia" ... "Bolivia (Plurinational State of)" → "Bolivia"; "Venezuela" ... "Venezuela (Bolivarian Republic of)" → "Venezuela"; "Iran" → "Iran (Islamic Republic of)"; "Syria" → "Syrian Arab Republic"; "Tanzania" → "United Republic of Tanzania"; "Moldova" → "Republic of Moldova"; "Lao" ... "Lao People's Democratic Republic" → "Laos"; "Micronesia" ...; "Cabo Verde" is the name probably. I'll generate aliases by stripping parenthetical: name.replace(/\s*\(.*\)$/,''). That handles many. Plus a small manual alias list. Good enough; unmatched state claims → verdict "cannot be checked" with reason "State not among the 47 Council members in this record" — actually if the state name isn't in votes map, it cannot be checked (not a Council member at that vote / not in data). That's a good use of "cannot be checked".

Also handle claims like "Kenya voted in favour" where Kenya is in votes map → compare to votes[ISO3]. Verdict matches/wrong. If state in countries map but not in this record's votes → cannot be checked ("not in the roll call for this vote"). If state not known at all → cannot be checked.

Also maybe pattern "in favour (Kenya)"? Skip.

Also "adopted unanimously" — could add: if text contains "unanimously" and record has no>0 or abstain>0 → wrong; if no==0&&abstain==0 → matches. Nice touch, include as a claim type "adopted unanimously". Also "without a vote" — HRC sometimes adopts without a vote, but recorded votes data... if text says "adopted without a vote" and record has votes → wrong? Eh, include: claim "without a vote" → check if yes+no+abstain totals are 0? For recorded votes they're not. I'll include unanimously only, keep scope tight. Actually the user listed specific checkable claims: numbers in favour/against/abstaining, the date, the session, each State said to have voted a certain way. Stick to those four categories. Maybe add unanimously as bonus — no, keep to spec to avoid bugs. Actually "each State said to have voted a certain way" — also patterns like "Kenya and France voted in favour" (multiple states sharing one verb). Handle: split on commas/and before the verb? Pattern: list of names followed by "voted in favour". I can handle with a regex that captures a name-list: /((?:[A-Z][\w'’.-]*(?:\s+(?:of|the|and|de)\s+|\s+)[A-Z][\w'’.-]*...)) — messy. Simpler: for each known country name, regex: name + /\s*(?:,|and)?\s*/ ... hmm.

Alternative robust approach: find all occurrences of vote-phrases with a preceding name list: regex /([A-Z][^.;:!?]{0,80}?)\s+(voted|abstained)\s+(in\s+favo[u]?r|for|against|yes|no|abstained|to\s+abstain)/gi — capture the subject phrase, then split subject by /,| and / and match each token against country names (longest match). That handles "Kenya and France voted in favour" and "Kenya voted in favour". Also "Kenya abstained" (no way word): /([A-Z][^.;:!?]{0,80}?)\s+abstained\b/gi.

Subject matching: for each subject string, find all country names contained in it (check each known name as substring with word boundaries, longest first). If none found → skip (or if subject is like "It" skip). If found states, for each, claim = full matched sentence snippet.

Edge: "France voted against the resolution" — way word "against" captured; fine. "voted in favour of the resolution" — "in favour" captured. "voted for" captured. "voted no" captured. "voted yes". "abstained" alone. "did not vote"? → cannot be checked? If text says "X did not vote" — votes map may lack the state → cannot be checked. Could add pattern "did not vote" → way = "absent/not in roll call". I'll add: if state in votes → wrong (they did vote); if not in votes → matches? Hmm "cannot be checked" is safer: the roll call only covers recorded votes; absence might be a gap. The data note says gaps exist. So "did not vote" → cannot be checked (roll call has gaps). I'll include that pattern mapping to verdict "cannot be checked" with explanation. Maybe skip to reduce complexity... I'll include it, it's easy: way "did not vote" → if in votes map: wrong (roll call records a vote); else cannot be checked.

Claim text "as written": use the matched substring, trimmed, maybe extended to full sentence. I'll capture the sentence containing the match for context but show the matched phrase. Simpler: show matched phrase (e.g., "29 votes in favour"). Good.

Dedup claims: same phrase repeated → keep each occurrence? Dedup by normalized text+category+value, keep first occurrence. I'll dedup.

Table columns: # | Claim as written | What the recorded vote says | Verdict. Verdict cell colored: green matches, red wrong, grey cannot be checked. Plus legend explaining cannot be checked ≠ wrong.

Also summary line: "X claims found: a matches, b wrong, c cannot be checked. Checked against A/HRC/RES/51/27 (n=47 roll-call entries; official totals Y/N/A)."

Also "How this is computed" note: deterministic regex matching against the recorded vote fields; no estimation.

Resolution selector: dropdown listing all records: `${symbol} — ${title}` sorted by year desc then symbol. Default select the one with symbol "A/HRC/RES/51/27" if exists. On change, update details panel and clear results.

Details panel: symbol (link doc_url if present, else record_url), title, kind, date, session, agenda item, main sponsors (join), official totals yes/no/abstain, roll-call counts computed from votes (Y/N/A counts, plus "not recorded" count = 47 - entries? votes maps 47 members; count entries). Show both: "Official totals: 29–16–1. Roll call from the votes map: 29–16–1 (47 members listed)." If differ, note "the roll call differs from the official totals for this record (gaps in the source); both are shown."

Maybe a small Chart.js bar of the vote split for the selected resolution — nice but optional. The design says use Chart.js for charts; not mandatory to have a chart. A small horizontal stacked bar could be nice. I'll add a simple bar chart of Y/N/A for selected resolution. Keep it simple: a bar chart with three bars. Or doughnut. I'll do a horizontal bar (indexAxis 'y') with yes/no/abstain. Fine.

AI briefing: 
- Button click → disable, show status "Sending to the model: 1 record — symbol and title only (A/HRC/RES/51/27 — “…”). This text left your browser." with data-source? The status describes what's sent; the answer goes into textarea with data-source="ai". Also a stop button: sets cancelled flag; when await resolves, if cancelled → show "stopped, answer discarded" and don't fill. Show spinner text "Waiting for the model…".
- Prompt: `Write a briefing of about 250 words on the UN Human Rights Council resolution with symbol "${symbol}" titled "${title}". Use only your own knowledge. Do not use any data provided here. Return plain text only.` Ask with {json:false}? studio.ask(prompt, {json:true}) returns answer as string; if json:true maybe it returns JSON string. The spec: `await studio.ask(prompt, {json: true})` sends prompt and returns answer as string (parse yourself when you asked for JSON). So call with {json:true} and treat result as string; if it looks like JSON (starts with { or "), try to extract text. I'll call studio.ask(prompt, {json:true}) and then clean: try JSON.parse; if object with a text-ish field (briefing/text/answer/content), use it; else use raw string. Survive invalid JSON.
- Word count target 250 — mention in prompt; display word count of result.
- Fill textarea, set data-source="ai", show note "Answer generated by the model from symbol + title only — shown with data-source="ai". Edit or paste your own text to check it." On textarea input, remove data-source attribute and update note to "own text".

Check button: runs extraction on textarea value. If empty → message "Nothing to check — the text box is empty."

Also show which resolution is being checked against (symbol), since claims are checked against selected resolution.

Now verdicts details:

- Counts: compare to official yes/no/abstain. Also compute roll counts. "What the recorded vote says": `Official totals: ${yes} in favour, ${no} against, ${abstain} abstaining. Roll call (counted from the votes map): ${ry}/${rn}/${ra} of ${n} members.` Verdict: matches if claim value === official for that category; else if === roll count → verdict "matches" but note? I'll implement verdict: if equals official → "matches"; else if equals roll → "matches" with the says-column clarifying "(matches the roll call; official total is X)"; else "wrong". Hmm — but if official and roll differ and claim matches roll, calling it "matches" is fine since column shows both. OK.

Actually cleaner: verdict matches if claim equals official total; if not but equals roll-call count, verdict "matches" too but I'll append in the says column. Fine.

- Date: parse claim date → ISO; compare with record.date. matches/wrong. If multiple date claims, each row. Also if text has no date, add an info row? No — table only shows found claims; add note under table: "No date claim found in the text" etc. per category maybe. I'll add a small summary of categories found/not found.

- Session: extract ordinal from claim; record session digits. matches if equal else wrong. If record.session missing digits → cannot be checked.

- State votes: as described. "What the recorded vote says": `Roll call: KEN = Y (in favour)` plus country name. Verdict matches if way maps to same code; wrong if different; cannot be checked if state not in votes map (with reason: not a recorded voter for this vote / not among Council members in this data).

Also handle "the resolution was adopted" — not checkable per spec; skip.

Now write the code. Structure:

HTML:
- header: title "Briefing checker — Human Rights Council recorded votes", description line: source, n, years computed from data: `Source: WORKSHOP_DATA.hrc — ${count} recorded votes, ${minYear}–${maxYear}. Participant country: ...` Actually hrc has no country. Description: "Recorded votes of the Human Rights Council: n resolutions/amendments, years X–Y. Source: WORKSHOP_DATA.hrc (OHCHR search library records)."
- Section 1: resolution picker + details + chart.
- Section 2: briefing: buttons Ask AI / Stop; status line; textarea; note.
- Section 3: Check button + results: summary + table + explanation of verdicts + how computed.

CSS: system font stack, background #f5f7fa, cards white, accent #1f6fb2. Base 16px. Max width ~1100px. Table styling. Verdict badges.

JS:
- const HRC = window.WORKSHOP_DATA.hrc; records = HRC.records || [].
- Build select options sorted by (year desc, symbol). Find default index of symbol 'A/HRC/RES/51/27'.
- renderDetails(rec): fill fields; compute roll counts; chart update.
- Chart: create once with data updated on change. Bar chart horizontal: labels ['In favour','Against','Abstain'], data [yes,no,abstain], backgroundColor accent shades. Also maybe second dataset roll call? Keep one dataset official totals; note roll call in text. Or grouped bars official vs roll call — nice to show both. I'll do grouped: two datasets "Official totals" and "Roll call (counted)". Colors: #1f6fb2 and #9ec7e4. Good.
- AI ask: as planned. Guard: if typeof studio === 'undefined' or !studio.ask → show message "studio.ask is not available in this environment." 
- Check: extraction functions.

Let me write extraction carefully.

```js
const MONTHS = {january:1,...};
function parseDates(text){
  const claims = [];
  // ISO
  const isoRe = /\b(\d{4})-(\d{1,2})-(\d{1,2})\b/g;
  // 7 July 2026 / 7th July 2026
  const dmyRe = /\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})\b/g;
  // July 7, 2026
  const mdyRe = /\b([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b/g;
  ...
}
```
Careful: dmyRe with month name check: month must be in MONTHS else skip (avoid matching "3 May 2020" fine; but "16 March 2020" ok). mdyRe similar. Dedup overlapping matches (e.g., "July 7, 2026" also matches dmy? "7, 2026" no—dmy needs day month year order; "July 7, 2026" mdy matches; dmy would try "7, 2026"? dmy regex: day then month-name then year — "July 7, 2026": at position of "7", next is ", 2026" not month name → no match. OK. But "7 July 2026" mdy? month first — no. Fine. Also avoid matching inside "2026-07-07" with dmy: "2026-07-07" — dmy at "07-07"? day=07 then needs month name, "-07" no. OK.

For each match, claim text = matched string; parsed ISO = `${y}-${pad(m)}-${pad(d)}`; validate month 1-12, day 1-31. Compare to rec.date (string ISO). rec.date might be "2026-07-07". Compare directly; also parse rec.date to be safe.

Session claims:
```js
const sessRe = /\b(\d{1,2})(?:st|nd|rd|th)\s+session\b/gi; // "51st session"
const sessRe2 = /\bsession\s+(\d{1,2})\b/gi;
```
Record session digits: (rec.session||'').match(/\d+/) → num. If none → cannot be checked for any session claim. Claim text e.g. "51st session". Also "at its 51st session" — the regex catches "51st session" portion; claim as written maybe include more context: I'll capture with optional prefix: /\b(?:at\s+its\s+)?(\d{1,2})(?:st|nd|rd|th)\s+session\b/gi.

Count claims:
```js
const countPatterns = [
 {re:/(\d+)\s*(?:votes?|ballots?)?\s*(?:in\s+favo[u]?r|for|supporting|yes)\b/gi, cat:'yes'},
 {re:/(\d+)\s*(?:votes?|ballots?)?\s*against\b/gi, cat:'no'},
 {re:/(\d+)\s*(?:votes?|ballots?)?\s*abstain(?:ing|ed|ions?)?\b/gi, cat:'abstain'},
 {re:/(\d+)\s*(?:votes?|ballots?)?\s*no\b/gi, cat:'no'},
];
```
Careful: "in favour" — "for" alone: "29 for" — pattern "for\b" might match "for" in "29 for the resolution"? "voted 29 for"? rare. Also "16 against" fine. "1 abstention" — abstain(?:ions?)? matches "abstention"? "abstain" + "ion"? My regex: abstain(?:ing|ed|ions?)? — "abstention" = abstain + "ion" — not covered. Use /abstain\w*/ → matches abstain, abstained, abstaining, abstention, abstentions. Good: /(\d+)\s*(?:votes?\s*)?abstain\w*/gi. But "1 abstention" has no "votes": (\d+)\s*(?:votes?\s*)?abstain\w* → "1 abstention" matches. Good.

Also "29 yes votes"? pattern yes: /(\d+)\s*(?:votes?\s*)?yes\b/gi. And "yes: 29"? skip.

Also combined "29–16–1": add pattern /(\d+)\s*[-–—]\s*(\d+)\s*[-–—]\s*(\d+)/g with claim "adopted X–Y–Z (in favour–against–abstaining)" — only if nearby words favour/against? Ambiguous; I'll include it only when the surrounding 40 chars contain "favour"/"favor"/"against"/"abstain". Implement: find match, look at context window text.slice(max(0,i-40), i+len+40), if /favo|against|abstain/i then create three claims. Good.

Also "in favour, against and abstaining" order assumed.

Dedup: key = cat+value+normalized claim text lowercase. Keep first.

State vote claims:
Build names list: from HRC.countries (ISO3→name). aliases: strip parenthetical, plus manual map:
```js
const ALIASES = {
 'united states':'USA','united states of america':'USA','russia':'RUS','russian federation':'RUS',
 'south korea':'KOR','republic of korea':'KOR','north korea':'PRK',"democratic people's republic of korea":'PRK',
 'ivory coast':'CIV',"côte d'ivoire":'CIV','vietnam':'VNM','turkey':'TUR','türkiye':'TUR',
 'bolivia':'BOL','venezuela':'VEN','iran':'IRN','syria':'SYR','tanzania':'TZA','moldova':'MDA','laos':'LAO',
 'micronesia':'FSM','cabo verde':'CPV','cape verde':'CPV','czech republic':'CZE','czechia':'CZE',
 'north macedonia':'MKD','macedonia':'MKD','eswatini':'SWZ','swaziland':'SWZ','gambia':'GMB','the gambia':'GMB',
 'democratic republic of the congo':'COD','congo-kinshasa':'COD','republic of the congo':'COG','congo-brazzaville':'COG',
 'united kingdom':'GBR','great britain':'GBR','britain':'GBR','uk':'GBR','usa':'USA','u.s.':'USA','south africa':'ZAF'
};
```
But only use alias if that ISO3 exists in HRC.countries. Build nameToIso: for each [iso,name]: add lowercase name → iso; add stripped-parenthetical → iso; then aliases if iso in countries. Also handle "the Gambia" etc.

Matching in text: for each name (sorted by length desc), regex with word boundary: new RegExp('\\b'+esc(name)+'\\b[^.;:!?\\n]{0,40}?(voted|abstained|did not vote)\\s+(in\\s+favo[u]?r|for|against|yes|no|abstain\\w*|to\\s+abstain)?','gi') — hmm "abstained" alone: name + " abstained". Let me do two passes:

Pass A: /name\s+(?:voted|votes|cast\s+(?:a|its|their)?\s*vote\s+)?.../ getting complex. Simplify to common phrasings:
- `${name} voted in favour` / `voted for` / `voted against` / `voted yes` / `voted no` / `voted to abstain`
- `${name} abstained`
- `${name} did not vote`

Regex per name: 
```js
const re = new RegExp('\\b'+esc(name)+'\\s+(voted\\s+(?:in\\s+favo[u]?r|for|against|yes|no|to\\s+abstain)|abstained|did\\s+not\\s+vote)\\b','gi');
```
Wait "voted in favour of the resolution" — "voted in favour" matches then \b after "favour" — "favour of" → \b between r and space ok. Good. Claim text = full match (name + phrase). Way mapping: contains 'favour'/'favor'/'for'/'yes' → 'Y'; 'against'/'no' → 'N'; 'abstain' → 'A'; 'did not vote' → 'absent'.

But multi-state: "Kenya and France voted in favour" — per-name regex: "Kenya and France voted in favour" — for name "Kenya", regex needs name immediately followed by voted-phrase; "Kenya and France voted..." has "and France" between → no match for Kenya; matches for France only. To handle lists, add pattern: name followed by list continuation: `\bNAME((?:\s*(?:,|and)\s*[A-Z][^.;:!?]{0,60}?)*)\s+(voted ...)` — complex. Alternative: first find all vote-phrase occurrences with preceding subject: 
```js
const subjRe = /\b([A-Z][A-Za-z'’.\-]+(?:\s+(?:of|the|and|de|del|van|von|al|bin|el|la|le|du|di)\s+[A-Za-z'’.\-]+|\s+[A-Z][A-Za-z'’.\-]+){0,3})\s+(voted\s+(?:in\s+favo[u]?r|for|against|yes|no|to\s+abstain)|abstained|did\s+not\s+vote)\b/gi;
```
Then for each match, subject = group1, phrase = group2. Split subject on /\s*(?:,|and)\s*/ → tokens; for each token, trim, lookup nameToIso (lowercase, also try stripping leading "The "). If found → claim for that state with claim text = token + ' ' + phrase (as written: maybe full match). If token not a known state → skip (could be "The Council"). This handles "Kenya and France voted in favour" → subject "Kenya and France". Also "Kenya voted in favour" → subject "Kenya". Risk: subject regex greedy across sentence: "The resolution, Kenya voted..." — subject must start uppercase letter; "The resolution, Kenya voted in favour" — subject could match "The resolution, Kenya"? The pattern allows up to 3 capitalized words with connectors; "The resolution, Kenya" — "resolution," has comma — my char class excludes comma, so "resolution" then ", " breaks; subject would be "Kenya" only if regex engine starts at "Kenya". Regex scanning: at "The", tries "The resolution" then needs voted-phrase after optional more words — "resolution, Kenya voted" — after "The resolution" comes "," which isn't in allowed continuation → fail at "The"; engine moves on; at "Kenya": "Kenya voted in favour" matches. 

But danger: "France voted against while Kenya voted in favour" — first match subject "France" phrase "voted against" good; then "while Kenya voted in favour" — at "While"? capital W: "While Kenya voted in favour" — subject "While Kenya"? "While" then space then "Kenya" (capitalized word allowed) then " voted in favour" → subject "While Kenya", tokens ["While Kenya"] → not a country → skipped, and Kenya's claim lost. Hmm. Mitigate: when token lookup fails, try splitting token into words and check each word-combination? Simpler: also run the per-name regex pass (name immediately followed by phrase) as a second pass, and merge claims (dedup by state+way+claimtext). Per-name pass catches "Kenya voted in favour" even mid-sentence. Combined passes cover most. Also for subject pass, when token not found, try each individual word and pairs? I'll do: for token, if not found, split by spaces and try consecutive n-grams (n up to 3) against nameToIso. That handles "While Kenya" → "Kenya". Good.

Also lowercase country names at sentence start? Names are capitalized anyway. Also "the United States voted..." — subject "the United States"? starts lowercase 't' — my subject regex requires [A-Z] start. Add optional "the ": /\b([Tt]he\s+)?([A-Z]...)/ — I'll allow optional leading "The/the". In per-name pass, name "United States" with \b before — "the United States voted" → \bUnited matches after "the " fine.

Way → expected code: Y/N/A. Compare with rec.votes[iso]. If iso in votes: verdict matches if equal else wrong; says: `Roll call: ${name} (${iso}) = ${code} (${label})`. If iso not in votes: cannot be checked — reason: "not in the roll call for this vote (the votes map lists N members; gaps exist in the source)". If state unknown entirely (not in countries map) — we only match known names, so unknown states never produce claims. But user might write "Germany voted in favour" — Germany not a Council member in 2026? Actually in sample, DEU appears in votes (2023 amendment). Countries map has all ISO3 names presumably including non-members? HRC.countries maps ISO3 of the 47 members... "countries: {ISO3: name}" — probably all countries or just members? Description: "countries: {ISO3: name}" ambiguous; votes maps the 47 members. I'll build names from HRC.countries (all listed), and verdict cannot-be-checked when not in this record's votes. Good.

Also handle "voted in favour of" etc. covered.

Also pattern "in favour: Kenya, France and Germany" — skip.

Now "cannot be checked" explanation: legend under table: "Cannot be checked means this data has no recorded vote for that claim (e.g., the State is not in the roll call for this resolution, or the source has gaps). It is not the same as wrong: wrong means the recorded vote contradicts the claim."

Summary: counts by verdict. Also list categories found: "Found: 3 vote-count claims, 1 date claim, 1 session claim, 5 State-vote claims. No date claim found." etc.

How computed note: "Every claim above was found by deterministic text matching (regular expressions) in your text and compared with the recorded vote fields (yes/no/abstain totals, date, session, votes map) of the selected resolution. Nothing is estimated; no AI was used for the check."

AI section note: "The model receives only the symbol and title — none of the workshop data. It is slow and costs money; you can stop waiting (the answer will be discarded)."

Now the "stop": since studio.ask is a promise we can't cancel, implement stopFlag; button "Stop" sets flag and status "Stopping… the answer will be discarded when it arrives." On resolve: if flag → discard.

Also handle errors: try/catch around await; show error message.

JSON handling: `const raw = await studio.ask(prompt, {json:true});` then:
```js
let text = raw;
try { const p = JSON.parse(raw); if (typeof p === 'string') text = p; else if (p && typeof p==='object'){ text = p.briefing || p.text || p.answer || p.content || p.message || raw; } } catch(e){ text = raw; }
```
If text not string → String(text).

Word count display: `words = text.trim().split(/\s+/).length`.

Textarea: rows=12, monospace? normal. Placeholder "Ask AI for a briefing, or paste your own text here…".

data-source="ai": set on textarea when AI fills; on 'input' event, if user typed, remove attribute and change note. But AI fill also triggers input? Programmatic value set doesn't fire input. Good.

Also the status element showing what was sent: give it data-source="ai"? The rule: render every value that came from studio.ask inside element with data-source="ai". The answer is the value; status text is ours. I'll put data-source="ai" on the textarea and also on a small "AI-generated" badge next to it. Fine.

Chart: 
```js
const ctx = document.getElementById('voteChart');
let chart = new Chart(ctx, {type:'bar', data:{labels:['In favour','Against','Abstain'], datasets:[{label:'Official totals', data:[], backgroundColor:'#1f6fb2'},{label:'Roll call (counted from votes map)', data:[], backgroundColor:'#a8cbe8'}]}, options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{beginAtZero:true, title:{display:true,text:'Votes'}}}}});
```
Update on selection: chart.data.datasets[0].data=[yes,no,abstain]; datasets[1].data=[ry,rn,ra]; chart.update().

If Chart undefined (shouldn't be), guard.

Layout: header, main container max-width 1080px, sections as cards.

Resolution details also show: kind, agenda item, session, date, sponsors, doc links: doc_url (if non-empty) "Resolution text (undocs)" and record_url "OHCHR search library record". Symbol shown.

Also note about roll call vs totals discrepancy.

Picker: label "Resolution:" select. Options text: `${symbol} — ${title}` truncated? Option text can be long; fine. Sort: by year desc, then symbol asc. Default: find symbol === 'A/HRC/RES/51/27'.

Edge: records empty → show message.

Now the check function detail — comparing date: rec.date string "2026-07-07". Claim parsed to same format. matches if equal. If rec.date missing → cannot be checked.

Session: rec.session e.g. "51st session" or "Human Rights Council at its 54th session". digits = match /\d+/ → "54". Claim "54th session" → 54. matches if equal. If rec.session has no digits → cannot be checked.

Counts: official yes/no/abstain ints. roll counts from Object.values(rec.votes||{}). reduce.

Verdict for counts: if claimVal === official[cat] → matches. else if roll exists and claimVal === roll[cat] → matches (note). else wrong. Says column: `Official totals: ${yes} in favour / ${no} against / ${abstain} abstaining. Roll call counted from the votes map (${n} members): ${ry}/${rn}/${ra}.` Maybe per-claim only show relevant: `In favour: official total ${yes}; roll call ${ry}.` I'll show relevant category line plus overall in header note. Keep says column concise: for cat yes: `Recorded: ${yes} in favour (official total); roll call count: ${ry}.`

Table rows: build array of {claim, says, verdict, reason}. Render.

Also include claim category tag maybe in claim cell: small label like "vote count", "date", "session", "State vote". Nice.

Explain verdicts legend with colored dots.

Also "cannot be checked" examples: state not in roll call; session field missing; date missing.

Now write the full HTML. Keep under 700 lines. Let me draft.

Also top description: compute n = records.length, years min/max from records' year. `Source: Human Rights Council recorded votes (WORKSHOP_DATA.hrc, OHCHR Search Library) — ${n} recorded votes, ${minY}–${maxY}.`

Title: "Briefing checker — Human Rights Council recorded votes".

Let me now write code mentally with care for regex escaping in JS strings.

esc function: `const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');`

Name list building:
```js
const countries = HRC.countries || {};
const nameToIso = {};
const names = [];
for (const [iso, name] of Object.entries(countries)) {
  const variants = [name, name.replace(/\s*\(.*?\)\s*/g,' ').replace(/\s+/g,' ').trim()];
  for (const v of variants) { const k = v.toLowerCase(); if (k && !nameToIso[k]) { nameToIso[k]=iso; names.push(v); } }
}
const ALIASES = {...};
for (const [a, iso] of Object.entries(ALIASES)) if (countries[iso] && !nameToIso[a]) { nameToIso[a]=iso; names.push(a); }
```
Wait alias should map to iso only if that iso in countries. Also names list for matching: use variants + aliases, dedupe, sort by length desc.

Matching pass 1 (subject list):
```js
const subjRe = /\b(?:[Tt]he\s+)?([A-Z][A-Za-z'’.\-]+(?:\s+(?:of|the|and|de|del|van|von|al|bin|el|la|le|du|di|das|der|dos|las|les|los|y)\s+|[A-Z][A-Za-z'’.\-]+\s*){0,3}?)(voted\s+(?:in\s+favo[u]?r|for|against|yes|no|to\s+abstain)|abstained|did\s+not\s+vote)\b/gi;
```
Hmm the continuation part is tricky. Let me simplify: subject = up to 4 capitalized tokens possibly joined by lowercase connectors or spaces:
```js
const subjRe = /\b((?:[A-Z][A-Za-z'’.\-]*|of|the|and|de|del|van|von|al|bin|el|la|le|du|di)(?:\s+(?:[A-Z][A-Za-z'’.\-]*|of|the|and|de|del|van|von|al|bin|el|la|le|du|di)){0,5})\s+(voted\s+(?:in\s+favo[u]?r|for|against|yes|no|to\s+abstain)|abstained|did\s+not\s+vote)\b/gi;
```
This could over-capture ("The Council voted in favour" → subject "The Council" → tokens: "The","Council" → n-grams: "the council" not a country → skip; but then per-name pass won't catch anything since no country name. Fine.)

But over-capture risk: "In March, Kenya voted in favour" — subject could start at "In"? "In March, Kenya voted" — "March," has comma → stops. Subject "In March"? then needs voted right after — "March, Kenya voted" no. Engine at "Kenya": subject "Kenya" + "voted in favour" ✓.

Risk: "France and Germany voted against" → subject "France and Germany" ✓ tokens France, Germany ✓.

Then for each match: subject string s, phrase p. tokens = s.split(/\s*(?:,|and)\s*/i)... careful "and" inside names? "Trinidad and Tobago" — splitting on "and" breaks it! "Trinidad and Tobago voted in favour" → tokens "Trinidad", "Tobago". n-gram lookup: try full subject first: nameToIso["trinidad and tobago"] ✓ if I check the whole subject (normalized) before splitting. Order: 1) whole subject lookup; 2) split by comma only; 3) for each comma-token, try n-grams of words (1..4 words) to find country names. "Trinidad and Tobago" whole-subject lookup works. "France and Germany" whole lookup fails; comma-split gives one token "France and Germany"; n-grams: "france" ✓, "germany" ✓, "france and", "and germany" ✗. Good. Implement n-gram search: for token, words = token.split(/\s+/); for len 1..min(4,words.length), for i, gram = words.slice(i,i+len).join(' '); if nameToIso[gram] → add. Dedup states per match.

Claim text as written: I'll use the full match (subject + phrase), trimmed. For multi-state, one row per state with claim text = `${stateName} ${phrase}`? "as written" — better show the full matched phrase "France and Germany voted against" once per state? That duplicates. I'll show claim as the full match text, and if multiple states in one match, produce one row per state each showing the full match (claim column same) — acceptable; or claim = state + phrase. I'll do: claim text = full match; add small "State: X" in says column. Actually simpler: one row per (state, way) with claim = full match text. Fine.

Pass 2 (per-name immediate): for each name in names (longest first), regex `\b${esc(name)}\s+(voted\s+(?:in\s+favo[u]?r|for|against|yes|no|to\s+abstain)|abstained|did\s+not\s+vote)\b` gi. This catches "Kenya voted in favour" even when preceded by other words. Merge with pass 1 results via dedup key: iso + '|' + way + '|' + normalized claim text? Pass1 claim "France and Germany voted against" vs pass2 for France: "France voted against"? No — pass2 regex requires name immediately followed by phrase; in "France and Germany voted against", France is followed by "and" → no match; Germany matches "Germany voted against". So pass2 gives claim "Germany voted against" — different claim text but same state+way. Dedup key: iso+way → keep first (pass1 first). But pass1 might miss a state that pass2 catches (e.g., "While Kenya voted in favour" — pass1 subject "While Kenya" → n-grams find "kenya" ✓ actually pass1 catches it via n-grams). OK dedup by iso+way, keep first occurrence (pass 1 runs first). But different ways for same state ("Kenya voted in favour... Kenya voted against" contradictory) — key includes way, so both kept. Good.

Way mapping:
```js
function wayCode(p){ const s=p.toLowerCase(); if(/did\s+not\s+vote/.test(s)) return 'absent'; if(/abstain/.test(s)) return 'A'; if(/against|\bno\b/.test(s)) return 'N'; return 'Y'; }
```
"voted no" → N; "voted for" → Y; "voted yes" → Y; "in favour" → Y.

Verdict for state: 
```js
const votes = rec.votes || {};
if (iso in votes) { const code = votes[iso]; verdict = (code===way)?'matches':'wrong'; says = `Roll call: ${name} (${iso}) recorded as ${code} — ${label(code)}.`; }
else { verdict='cannot be checked'; says = `${name} (${iso}) is not in the roll call for this vote (${Object.keys(votes).length} members recorded). The source has gaps, so absence is not proof of anything.`; }
```
For 'absent' way: if iso in votes → wrong (roll call records a vote); else cannot be checked.

label: Y 'in favour', N 'against', A 'abstaining'. HRC.vote_codes maps codes to labels? `vote_codes: {Y,N,A}` — maybe {Y:'Yes',...}. Use HRC.vote_codes?.[code] || fallback.

Date claims: also handle "on 7 July 2026" — regex catches "7 July 2026". Claim text = match. Also "July 2026" (month-year only)? Could add: /(\b(?:January|...)\s+(\d{4})\b)/ → compare year+month to rec.date; verdict matches if same month-year, wrong if different month, cannot... I'll include month-year pattern: if claim month-year != rec month-year → wrong (different month) — but maybe text refers to another event date... it's a claim about the resolution presumably. Include it; verdict wrong if differs. Hmm risk of false "wrong" if text mentions another date in same month context... acceptable. Actually to be safe, only include full dates and month-year when sentence also mentions resolution/session? Too complex. I'll include month-year claims only if the containing sentence contains "session" or "adopted" or "vote"? Let me just include full dates (day precision) and ISO; skip month-only to avoid false positives. Also "in 2026" year-only claims? The user asked for "the date" — full date. I'll also catch year-only "in 2026" when sentence mentions adopted/session? Skip. Keep: ISO, d Month yyyy, Month d, yyyy. Good.

Session claims: also "its 51st session" covered; "session 51" covered; "51st session of the Human Rights Council" covered.

Counts: also "adopted with 29 votes" etc. covered by patterns. Also "29-16-1" pattern with context check.

Now, "what the recorded vote says" for counts — include both official and roll.

Summary line: `Checked ${rows.length} claim(s) against ${rec.symbol}: ${m} match, ${w} wrong, ${c} cannot be checked.` Plus per-category found counts: `Found in your text: X vote-count claims, Y date claims, Z session claims, S State-vote claims.` If a category has zero, say "no date claim found" — I'll include in the found list only nonzero, and add sentence listing missing categories: "Not found in the text: date." Good for honesty.

Now write everything. Also ensure no horizontal scroll: table wrapper overflow-x auto.

Let me also compute years range: records.map(r=>r.year).filter(Boolean); min/max.

Write the HTML now.

Also the "Ask AI" prompt must say send only symbol and title: prompt = `Write a briefing of about 250 words about the United Nations Human Rights Council resolution with symbol "${symbol}" and title "${title}". Base it only on your own knowledge — no other data is provided or should be assumed. Return plain text only, no JSON, no headings beyond short paragraphs.` And status: `Sending to the model: 1 item — the symbol and title only ("${symbol}" — "${title}"). None of the workshop data is sent. This text left your browser.`

Note: studio may be undefined in sandbox preview — guard and show message.

Stop button: visible during waiting.

Let me write the final file. Aim ~600 lines.

CSS plan:
```css
:root{--accent:#1f6fb2;--bg:#f4f6f9;--card:#fff;--ink:#1c2733;--muted:#5b6b7b;--line:#dde4ec;}
*{box-sizing:border-box}
body{margin:0;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);}
.wrap{max-width:1080px;margin:0 auto;padding:24px 20px 60px;}
header.top{...}
h1{font-size:1.6rem;margin:0 0 6px}
.sub{color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-top:18px;}
...
table{border-collapse:collapse;width:100%;}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;font-size:15px;}
th{background:#eef3f8;}
.badge{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:600;white-space:nowrap;}
.b-match{background:#e2f3e5;color:#1c6b2f;}
.b-wrong{background:#fbe3e3;color:#a11c1c;}
.b-cant{background:#eceff3;color:#5b6b7b;}
button{...accent...}
textarea{width:100%;min-height:220px;...}
```

Chart container height 220px.

Now JS full code. Let me write it out.

```js
(function(){
"use strict";
const HRC = window.WORKSHOP_DATA && window.WORKSHOP_DATA.hrc ? window.WORKSHOP_DATA.hrc : {records:[]};
const records = Array.isArray(HRC.records)?HRC.records:[];
const countries = HRC.countries||{};
const voteCodes = HRC.vote_codes||{Y:'Yes',N:'No',A:'Abstain'};
const $ = id=>document.getElementById(id);
const esc = s=>String(s).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
...
```

Render picker:
```js
const sel = $('resSelect');
const sorted = records.slice().sort((a,b)=>( (b.year||0)-(a.year||0) ) || String(a.symbol).localeCompare(String(b.symbol)));
sorted.forEach((r,i)=>{ const o=document.createElement('option'); o.value=r.id||String(i); o.textContent = r.symbol+' — '+(r.title||''); sel.appendChild(o); });
const def = sorted.findIndex(r=>r.symbol==='A/HRC/RES/51/27');
sel.value = sorted[def>=0?def:0].id || String(def>=0?def:0);
```
Careful: value set by id; if ids missing use index. I'll set o.value = String(idx) and keep map idx→record. Simpler: sel.dataset index. Use option value = index in sorted array.

renderDetails(rec):
```js
$('dSymbol').textContent = rec.symbol||'—';
link doc: if rec.doc_url set href & show; else hide. record_url similarly.
$('dTitle').textContent = rec.title||'';
meta rows: kind, date, session, agenda item, sponsors join ', ' or '—'.
totals: yes/no/abstain.
roll: count votes.
discrepancy note if differ.
chart update.
```

Check function:

```js
function rollCounts(rec){ const v=rec.votes||{}; let y=0,n=0,a=0; for(const k in v){ const c=v[k]; if(c==='Y')y++; else if(c==='N')n++; else if(c==='A')a++; } return {y,n,a,total:Object.keys(v).length}; }
```

Extraction:

```js
const MONTHS={january:1,february:2,march:3,april:4,may:5,june:6,july:7,august:8,september:9,october:10,november:11,december:12};
function pad(n){return String(n).padStart(2,'0');}
function extractDates(text){
  const out=[]; const seen=new Set();
  const push=(claim,iso)=>{const k=claim.toLowerCase(); if(seen.has(k))return; seen.add(k); out.push({claim,iso});};
  let m;
  const isoRe=/\b(\d{4})-(\d{1,2})-(\d{1,2})\b/g;
  while((m=isoRe.exec(text))){ const y=+m[1],mo=+m[2],d=+m[3]; if(mo>=1&&mo<=12&&d>=1&&d<=31) push(m[0], y+'-'+pad(mo)+'-'+pad(d)); }
  const dmy=/\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s*,?\s+(\d{4})\b/g;
  while((m=dmy.exec(text))){ const mo=MONTHS[m[2].toLowerCase()]; if(mo){ const d=+m[1],y=+m[3]; if(d>=1&&d<=31) push(m[0], y+'-'+pad(mo)+'-'+pad(d)); } }
  const mdy=/\b([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b/g;
  while((m=mdy.exec(text))){ const mo=MONTHS[m[1].toLowerCase()]; if(mo){ const d=+m[2],y=+m[3]; if(d>=1&&d<=31) push(m[0], y+'-'+pad(mo)+'-'+pad(d)); } }
  return out;
}
```
Note dmy with optional comma: "7 July, 2026" ok.

Counts:
```js
function extractCounts(text){
  const out=[]; const seen=new Set();
  const push=(claim,cat,val)=>{const k=cat+'|'+val+'|'+claim.toLowerCase(); if(seen.has(k))return; seen.add(k); out.push({claim,cat,val});};
  const pats=[
    {re:/(\d+)\s*(?:votes?|ballots?)?\s*(?:in\s+favo[u]?r|for|yes)\b/gi,cat:'yes'},
    {re:/(\d+)\s*(?:votes?|ballots?)?\s*against\b/gi,cat:'no'},
    {re:/(\d+)\s*(?:votes?|ballots?)?\s*abstain\w*/gi,cat:'abstain'},
    {re:/(\d+)\s*(?:votes?|ballots?)?\s*no\b/gi,cat:'no'}
  ];
  for(const p of pats){ let m; p.re.lastIndex=0; while((m=p.re.exec(text))){ push(m[0].trim(), p.cat, +m[1]); } }
  // X–Y–Z pattern
  const dash=/(\d+)\s*[-–—]\s*(\d+)\s*[-–—]\s*(\d+)/g; let m;
  while((m=dash.exec(text))){ const ctx=text.slice(Math.max(0,m.index-50), m.index+m[0].length+50); if(/favo|against|abstain/i.test(ctx)){ push(m[0]+' (in favour–against–abstaining)', 'yes', +m[1]); push(m[0]+' (in favour–against–abstaining)', 'no', +m[2]); push(m[0]+' (in favour–against–abstaining)', 'abstain', +m[3]); } }
  return out;
}
```
Wait "for" pattern: "29 for" — also matches "for" in "29 for"? ok. But "in favour" also matched by "for"? "in favour" — the alternation tries "in favo[u]?r" first at position after digits+space: "29 in favour" → matches "in favour" ✓. "voted 29 for the resolution" → "29 for" ✓. But false positive: "Paragraph 29 for..." unlikely. Also "yes" pattern: "29 yes" ✓. "no" pattern: "16 no" ✓ but also "16 no" inside "16 not"? \b after no — "not" → 'no' followed by 't' → \b fails ✓ good.

Hmm "abstain\w*" with optional votes: "1 abstention" → (\d+)\s*(?:votes?\s*)?abstain\w* → "1 abstention" ✓.

Session:
```js
function extractSessions(text){
  const out=[]; const seen=new Set();
  const push=(claim,num)=>{const k=claim.toLowerCase(); if(seen.has(k))return; seen.add(k); out.push({claim,num});};
  let m;
  const r1=/\b(?:at\s+its\s+)?(\d{1,2})(?:st|nd|rd|th)\s+session\b/gi;
  while((m=r1.exec(text))) push(m[0], +m[1]);
  const r2=/\bsession\s+(?:no\.?\s*)?(\d{1,2})\b/gi;
  while((m=r2.exec(text))) push(m[0], +m[1]);
  return out;
}
```

States:
```js
function buildNames(){
  const map={}; const list=[];
  const add=(name,iso)=>{ const k=name.toLowerCase().replace(/\s+/g,' ').trim(); if(!k) return; if(!map[k]){ map[k]=iso; list.push(name); } };
  for(const iso in countries){ const nm=countries[iso]; if(!nm) continue; add(nm,iso); add(String(nm).replace(/\s*\(.*?\)\s*/g,' ').replace(/\s+/g,' ').trim(), iso); }
  const ALIASES={'united states':'USA','united states of america':'USA','usa':'USA','u.s.':'USA','russia':'RUS','russian federation':'RUS','south korea':'KOR','republic of korea':'KOR','north korea':'PRK',"democratic people's republic of korea":'PRK','ivory coast':'CIV',"côte d'ivoire":'CIV','cote divoire':'CIV','vietnam':'VNM','turkey':'TUR','türkiye':'TUR','bolivia':'BOL','venezuela':'VEN','iran':'IRN','syria':'SYR','tanzania':'TZA','moldova':'MDA','laos':'LAO','micronesia':'FSM','cape verde':'CPV','czech republic':'CZE','czechia':'CZE','north macedonia':'MKD','eswatini':'SWZ','swaziland':'SWZ','the gambia':'GMB','united kingdom':'GBR','great britain':'GBR','britain':'GBR','uk':'GBR','democratic republic of the congo':'COD','republic of the congo':'COG','congo':'COG','south africa':'ZAF','burma':'MMR','myanmar':'MMR'};
  for(const a in ALIASES){ const iso=ALIASES[a]; if(countries[iso]) add(a,iso); }
  list.sort((a,b)=>b.length-a.length);
  return {map,list};
}
```
Careful: 'congo':'COG' — if text says "Congo voted..." ambiguous but COG is reasonable; but "Democratic Republic of the Congo" contains "Congo" — per-name regex with \b... "Democratic Republic of the Congo voted in favour": longest-first list tries "Democratic Republic of the Congo" first ✓. But pass-2 iterates all names; "Congo" regex would also match inside "the Congo voted" of that sentence → claim for COG too! Dedup key iso+way — different iso (COD vs COG) → both rows. Bad. Mitigate: in pass 2, skip a name if it's a substring of a longer name that also matched at overlapping position. Simpler: remove 'congo' alias, keep only full names. Also "republic of the congo" vs "democratic republic of the congo": "Republic of the Congo voted" — the longer name "Democratic Republic of the Congo" won't match that text. OK. Drop bare 'congo'. Also 'uk','usa' fine. Also 'the gambia' vs 'gambia': name in map might be "Gambia" — alias 'the gambia' ok; but "Gambia" itself from map. Both map to GMB; dedup by iso+way handles.

Also substring issue: "South Africa" vs "Africa"? no. "United States" inside "United States of America" — both map USA, dedup by iso+way ✓. "Korea" alone not in list. "Republic of Korea" and "South Korea" both KOR ✓. "Democratic People's Republic of Korea" contains "Republic of Korea"? No — "Democratic People's Republic of Korea" — substring "Republic of Korea"? The string is "Democratic People's Republic of Korea" — does it contain "Republic of Korea"? "...People's Republic of Korea" — yes! "Republic of Korea" is a substring ("People's Republic of Korea" contains "Republic of Korea"). So text "Democratic People's Republic of Korea voted in favour": longest-first tries "Democratic People's Republic of Korea" ✓ matches at that position; then "Republic of Korea" regex also matches within same span → claim for KOR again — same iso+way → dedup ✓. Good, dedup by iso+way saves us. But "Congo"→COG vs COD differ, so drop 'congo'. Also "Ivory Coast" vs "Côte d'Ivoire" different strings, same iso CIV ✓.

Also guard: pass2 regex per name — for name with apostrophe "Côte d'Ivoire" esc handles. Word boundary \b before name: "Côte" starts with C ✓.

Pass 1 subject regex — also produce claims; dedup by iso+way with pass1 first.

Actually simpler: only do pass 2 (per-name immediate) plus pass 1 for lists. Implement both, merge with key iso+'|'+way, pass1 first.

Pass 1:
```js
const subjRe=/\b((?:[A-Z][A-Za-z'’.\-]*|of|the|and|de|del|van|von|al|bin|el|la|le|du|di)(?:\s+(?:[A-Z][A-Za-z'’.\-]*|of|the|and|de|del|van|von|al|bin|el|la|le|du|di)){0,5})\s+(voted\s+(?:in\s+favo[u]?r|for|against|yes|no|to\s+abstain)|abstained|did\s+not\s+vote)\b/gi;
```
Hmm "and" lowercase in subject list — "France and Germany" ✓. But this also matches "The Council voted in favour" → subject "The Council" → n-gram lookup fails → no claim ✓.

For each match: subject=m[1], phrase=m[2]. Resolve states:
```js
function statesIn(subject, map){
  const res=[]; const s=subject.replace(/\s+/g,' ').trim();
  const tryAdd=(str)=>{ const k=str.toLowerCase(); if(map[k]) { if(!res.includes(map[k])) res.push(map[k]); return true;} return false; };
  if(tryAdd(s)) return res;
  // comma split
  const parts=s.split(/\s*,\s*/);
  for(const part of parts){
    if(tryAdd(part)) continue;
    const words=part.split(/\s+/);
    for(let len=Math.min(4,words.length); len>=1; len--){
      for(let i=0;i+len<=words.length;i++){
        const g=words.slice(i,i+len).join(' ');
        if(tryAdd(g)) { /* continue scanning rest? */ }
      }
    }
  }
  return res;
}
```
Hmm n-gram loop adds possibly multiple; fine. But "France and Germany" — tryAdd whole fails; comma-split one part; n-grams len4..1: "france and germany" no, len3 "france and","and germany" no, len2 "france and" no... len1 "france" ✓, "and" no, "germany" ✓. Good. "Trinidad and Tobago" whole ✓.

But wait: pass1 subject regex includes lowercase words like "of","the","and" — "The United States voted in favour": subject could be "The United States" ✓ tryAdd("the united states") — map has "united states" and alias "the united states"? I added 'the gambia' only. Add generic: in tryAdd, also try stripping leading "the ". I'll normalize: k = str.toLowerCase().replace(/^the\s+/,''). And when adding names, also add with "the " prefix? Just strip in lookup. Also map keys from names don't have "the". OK: tryAdd strips leading "the ".

Pass 2 per name:
```js
for(const name of names){
  const re=new RegExp('\\b'+esc(name)+'\\s+(voted\\s+(?:in\\s+favo[u]?r|for|against|yes|no|to\\s+abstain)|abstained|did\\s+not\\s+vote)\\b','gi');
  let m; while((m=re.exec(text))){ addClaim(iso, wayCode(m[2]), m[0]); }
}
```
Wait pass2 claim text m[0] includes name+phrase. For "France and Germany voted against", pass2 for "Germany" gives "Germany voted against" — but pass1 already claimed GER|N with full text; dedup keeps pass1. For "France", pass2 no match (followed by "and"). Pass1 n-grams catch France ✓.

Order: run pass1 first, then pass2, dedup key iso|way keeps first.

Hmm but pass1 might produce wrong subject capture: "Kenya voted in favour and France voted against" — pass1 first match: subject "Kenya" phrase "voted in favour" ✓ (regex stops at phrase). Then continues after; "and France voted against" — subject regex at "and"? starts with lowercase 'and' — my subject pattern requires first char [A-Z]... "and France voted against": engine at "France": subject "France" phrase "voted against" ✓. Good.

Edge: "voted in favour: Kenya" not handled — fine.

wayCode:
```js
function wayCode(p){ const s=' '+p.toLowerCase()+' '; if(/did not vote/.test(s)) return 'absent'; if(/abstain/.test(s)) return 'A'; if(/against/.test(s)||/\bno\b/.test(s)) return 'N'; return 'Y'; }
```

Now build rows:

```js
function checkText(){
  const rec = currentRec(); const text=$('briefText').value;
  const rows=[];
  if(!text.trim()){ show empty message; return; }
  const roll=rollCounts(rec);
  const official={yes:rec.yes, no:rec.no, abstain:rec.abstain};
  // counts
  for(const c of extractCounts(text)){
    const off=official[c.cat]; const rl={yes:roll.y,no:roll.n,abstain:roll.a}[c.cat];
    let verdict, note='';
    if(off===c.val) verdict='matches';
    else if(rl===c.val){ verdict='matches'; note=' (matches the roll call counted from the votes map; the official total differs)'; }
    else verdict='wrong';
    const says=`Recorded for ${rec.symbol}: ${c.cat==='yes'?'in favour':c.cat==='no'?'against':'abstaining'} — official total ${off}, roll call counted from the votes map ${rl} (${roll.total} members listed).`;
    rows.push({cat:'Vote count', claim:c.claim, says, verdict, note});
  }
  // dates
  const recDate = rec.date ? String(rec.date) : '';
  for(const d of extractDates(text)){
    let verdict = recDate ? (d.iso===recDate?'matches':'wrong') : 'cannot be checked';
    const says = recDate ? `Recorded date of ${rec.symbol}: ${recDate}.` : `No date field in this record.`;
    rows.push({cat:'Date', claim:d.claim, says, verdict});
  }
  // session
  const sm = String(rec.session||'').match(/\d+/); const recSess = sm?+sm[0]:null;
  for(const s of extractSessions(text)){
    let verdict = recSess===null?'cannot be checked':(s.num===recSess?'matches':'wrong');
    const says = recSess===null? `No session number in this record (session field: "${rec.session||''}").` : `Recorded session of ${rec.symbol}: "${rec.session}" (session ${recSess}).`;
    rows.push({cat:'Session', claim:s.claim, says, verdict});
  }
  // states
  for(const st of extractStates(text)){
    const votes=rec.votes||{};
    const name = countries[st.iso]||st.iso;
    if(st.way==='absent'){
      if(st.iso in votes){ rows.push({cat:'State vote', claim:st.claim, says:`Roll call: ${name} (${st.iso}) is recorded as voting ${votes[st.iso]} — so "did not vote" contradicts the roll call.`, verdict:'wrong'}); }
      else rows.push({cat:'State vote', claim:st.claim, says:`${name} (${st.iso}) is not in the roll call for this vote (${Object.keys(votes).length} members recorded; the source has gaps).`, verdict:'cannot be checked'});
    } else {
      if(st.iso in votes){
        const code=votes[st.iso];
        const verdict = code===st.way?'matches':'wrong';
        const says=`Roll call: ${name} (${st.iso}) = ${code} (${voteLabel(code)}). Claim says ${st.way==='Y'?'in favour':st.way==='N'?'against':'abstaining'}.`;
        rows.push({cat:'State vote', claim:st.claim, says, verdict});
      } else {
        rows.push({cat:'State vote', claim:st.claim, says:`${name} (${st.iso}) is not in the roll call for this vote (${Object.keys(votes).length} members recorded; the source has gaps), so this cannot be verified here.`, verdict:'cannot be checked'});
      }
    }
  }
  render rows...
}
```

voteLabel: voteCodes[code] or map.

Render table with category tag, claim, says, verdict badge. Summary counts. Also "not found" categories: compute found cats; if none of a category, mention.

Also note under table: explanation of cannot be checked + how computed.

AI ask:
```js
let asking=false, stopFlag=false;
$('askBtn').onclick=async ()=>{
  if(asking) return; const rec=currentRec(); if(!rec) return;
  if(!(window.studio && typeof studio.ask==='function')){ setStatus('studio.ask is not available in this environment, so no briefing can be requested here.', true); return; }
  asking=true; stopFlag=false; $('askBtn').disabled=true; $('stopBtn').style.display='inline-block';
  setStatus(`Sending to the model: 1 item — symbol and title only (“${rec.symbol}” — “${rec.title}”). None of the workshop data is sent; this text left your browser. Waiting for the answer…`);
  const prompt=`Write a briefing of about 250 words on the United Nations Human Rights Council resolution with symbol "${rec.symbol}" titled "${rec.title}". Use only your own knowledge; no data is provided with this request and none should be assumed. Return plain text only.`;
  try{
    const raw=await studio.ask(prompt,{json:true});
    if(stopFlag){ setStatus('Stopped — the answer arrived after you pressed Stop and was discarded. Nothing was added to the text box.'); }
    else{
      let txt=String(raw==null?'':raw);
      try{ const p=JSON.parse(txt); if(typeof p==='string') txt=p; else if(p&&typeof p==='object'){ txt=String(p.briefing||p.text||p.answer||p.content||p.message||txt); } }catch(e){}
      const ta=$('briefText'); ta.value=txt; ta.setAttribute('data-source','ai');
      const wc=txt.trim()?txt.trim().split(/\s+/).length:0;
      setStatus(`Briefing received from the model (${wc} words) and placed in the text box, marked data-source="ai". It was generated from the symbol and title only. You can edit it or paste your own text — press Check to verify it against the recorded vote.`);
    }
  }catch(err){ setStatus('The model request failed: '+err, true); }
  finally{ asking=false; $('askBtn').disabled=false; $('stopBtn').style.display='none'; }
};
$('stopBtn').onclick=()=>{ if(asking){ stopFlag=true; setStatus('Stop requested — if an answer arrives it will be discarded.'); } };
$('briefText').addEventListener('input',()=>{ $('briefText').removeAttribute('data-source'); setStatus('Text box now contains your own text (no longer marked as AI-generated). Press Check to verify it.'); });
```

setStatus(msg, isErr): status element textContent, class.

Check button: $('checkBtn').onclick=checkText.

currentRec: sorted[sel.selectedIndex].

Also render details on select change; also clear results? Keep results but note which resolution checked — I'll clear results on change and set a line "Showing recorded vote for …". Simpler: on change, re-render details and clear check output with message.

Chart guard: if(window.Chart){...} else hide chart card.

Header description: compute n and years:
```js
const years=records.map(r=>r.year).filter(y=>typeof y==='number');
const yMin=years.length?Math.min(...years):null, yMax=years.length?Math.max(...years):null;
$('dataLine').textContent=`Source: Human Rights Council recorded votes (window.WORKSHOP_DATA.hrc, from the OHCHR Search Library) — ${records.length} recorded votes${yMin!==null?`, ${yMin}–${yMax}`:''}. Pick a resolution below; every number on this page is counted from these records by the page itself.`;
```

Details card content: I'll build with spans.

Also "How this is computed" notes: under details card: "Official totals are the yes/no/abstain fields of the record; the roll call is counted here from the votes map (one entry per Council member). For a few records the two differ because of gaps in the source — both are shown." Under check table: "Claims are found by deterministic text matching (regular expressions) in the text box and compared with the selected record's fields. Nothing is estimated and no AI is used for checking."

Verdict legend: three badges with explanation: "Cannot be checked ≠ wrong: 'cannot be checked' means this dataset has no recorded value to compare against (for example the State is not in the roll call for this vote, or the record has no session number). 'Wrong' means the recorded vote directly contradicts the claim."

Now write final HTML. Also ensure the select default A/HRC/RES/51/27 — find in records by symbol; if not found, first.

Table rendering: build with DOM or innerHTML with escaping — claims come from user text, must escape. Use esc() for all inserted text. I'll build rows via createElement/textContent to avoid escaping issues.

Let me count lines roughly — fine.

One more: "Every row that shows a document has its symbol, linked to doc_url in a new tab." — details card shows symbol linked to doc_url (if present) else record_url. Also in check summary mention symbol. The table rows reference rec.symbol in says text — make the symbol in the summary a link. I'll include a link in the results header: `Checked against <a href=doc_url target=_blank>symbol</a>`.

Write it.

Also textarea id briefText with data-source initially absent; placeholder.

Edge: records empty → show "No recorded votes in the data." and disable controls.

Let me write the code now, carefully.

For the chart, container: `<div style="height:230px"><canvas id="voteChart"></canvas></div>`.

Chart options: indexAxis 'y', plugins legend bottom, scales x beginAtZero, title 'Votes'. Colors: official '#1f6fb2', roll '#8fbfe6'.

Also add a note if roll differs from official: element dNote.

Now produce final answer: 2-3 sentences before code block, then the html block, nothing after.

Let me write out the whole document.

Also careful: in JS template literals inside HTML — fine. Avoid `</script>` inside strings.

Regex with '’' char fine.

One concern: pass1 subject regex could match across "…voted in favour" where subject includes previous sentence words if no punctuation, e.g., "The Council adopted it and Kenya voted in favour" — subject: "and Kenya"? starts lowercase 'and' — pattern first token must be [A-Z]... "and" is lowercase, not matched as first token; engine tries at "Kenya" ✓. But "It passed and Kenya voted in favour": at "It"? "It passed and Kenya voted" — subject tokens: "It","passed","and","Kenya" (up to 6 tokens) then "voted in favour" → subject "It passed and Kenya" → n-grams: "it","passed","and","kenya" → kenya ✓ (len1). Also "it passed" no. OK works.

But false subject: "The United States voted in favour" — subject "The United States" ✓.

Also phrase "voted for" — "for" then \b: "voted for the resolution" ✓.

Also "cast a vote in favour"? Not handled; fine.

Also "in favour of" after state without "voted": "Kenya (in favour)" not handled. Acceptable; the legend can say patterns like "X voted in favour / against / abstained".

Add hint under textarea: "Recognised patterns include: '29 votes in favour', '16 against', '1 abstention', '29-16-1', dates like '7 July 2026' or '2026-07-07', '51st session', and 'Kenya voted in favour' / 'abstained' / 'did not vote'."

Now finalize. Write code.

Also the check output area: summary div + table + legend + notes. Initially hidden with hint "Press Check…".

Let me write:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Briefing checker — Human Rights Council recorded votes</title>
<style> ... </style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Briefing checker — Human Rights Council recorded votes</h1>
  <p class="sub" id="dataLine"></p>
</header>

<section class="card">
  <h2>1 · Pick a recorded vote</h2>
  <label for="resSelect" class="lbl">Resolution / amendment (recorded vote):</label>
  <select id="resSelect"></select>
  <div class="details" id="details"> ... </div>
  <p class="note" id="rollNote"></p>
  <div class="chartBox"><canvas id="voteChart"></canvas></div>
  <p class="how">How this is computed: ...</p>
</section>

<section class="card">
  <h2>2 · Briefing text</h2>
  <p class="how">...</p>
  <div class="btnRow">
    <button id="askBtn">Ask AI for a briefing</button>
    <button id="stopBtn" class="ghost" style="display:none">Stop (discard answer)</button>
  </div>
  <p class="status" id="aiStatus"></p>
  <textarea id="briefText" placeholder="Ask AI for a briefing, or paste your own text here, then press Check."></textarea>
  <p class="hint" id="patternHint">Recognised claim patterns: …</p>
</section>

<section class="card">
  <h2>3 · Check the text against the recorded vote</h2>
  <button id="checkBtn">Check</button>
  <div id="results"></div>
  <div id="legend"> ... verdicts explanation ... </div>
  <p class="how">How this is computed: ...</p>
</section>
</div>
<script> ... </script>
</body>
</html>
```

Details markup: I'll fill via JS into a container with rows.

Write JS fully now.

Also note: `studio` may be a global object; reference via `window.studio`.

Potential pitfall: `sel.selectedIndex` after setting value — set sel.value = String(defIdx>=0?defIdx:0).

Let me now write the complete final code, being careful with syntax.

For rendering details:

```js
function renderDetails(){
  const rec=sorted[+sel.value]; if(!rec){return;}
  current=rec;
  const d=$('details');
  d.innerHTML='';
  const addRow=(k,v)=>{ const div=document.createElement('div'); div.className='drow'; const kk=document.createElement('span'); kk.className='dk'; kk.textContent=k; const vv=document.createElement('span'); vv.className='dv'; vv.appendChild(v); div.appendChild(kk); div.appendChild(vv); d.appendChild(div); };
  // symbol with link
  const sym=document.createElement('span');
  const a=document.createElement('a'); a.textContent=rec.symbol||'—';
  const url=rec.doc_url||rec.record_url||'';
  if(url){ a.href=url; a.target='_blank'; a.rel='noopener'; }
  sym.appendChild(a);
  addRow('Symbol', sym);
  addRow('Title', textNode(rec.title||'—'));
  addRow('Kind', textNode(rec.kind||'—'));
  addRow('Date', textNode(rec.date||'—'));
  addRow('Session', textNode(rec.session||'—'));
  addRow('Agenda item', textNode(rec.agenda_item||'—'));
  addRow('Main sponsors', textNode((rec.main_sponsors&&rec.main_sponsors.length)?rec.main_sponsors.join('; '):'—'));
  addRow('Official totals', textNode(`in favour ${rec.yes} · against ${rec.no} · abstaining ${rec.abstain}`));
  const roll=rollCounts(rec);
  addRow('Roll call (counted here)', textNode(`in favour ${roll.y} · against ${roll.n} · abstaining ${roll.a} · ${roll.total} members listed in the votes map`));
  // links
  const links=document.createElement('span');
  if(rec.doc_url){ links.appendChild(mkLink(rec.doc_url,'Resolution text (UN Docs)')); }
  if(rec.record_url){ links.appendChild(mkLink(rec.record_url,'OHCHR Search Library record')); }
  addRow('Links', links);
  // note
  const same = roll.y===rec.yes && roll.n===rec.no && roll.a===rec.abstain;
  $('rollNote').textContent = same
    ? 'The roll call counted from the votes map equals the official totals for this record.'
    : 'For this record the roll call counted from the votes map differs from the official totals (gaps in the source). Both are shown; the checker compares claims against the official totals and also reports a match with the roll call.';
  // chart
  if(chart){ chart.data.datasets[0].data=[rec.yes||0,rec.no||0,rec.abstain||0]; chart.data.datasets[1].data=[roll.y,roll.n,roll.a]; chart.update(); }
  // clear results
  $('results').innerHTML=''; $('results').appendChild(hintP('Press “Check” to compare the text box with this recorded vote.'));
}
```

textNode helper: document.createTextNode.

mkLink: a element.

OK. Also `current` variable.

Check render:

```js
function renderResults(rows, rec){
  const res=$('results'); res.innerHTML='';
  const m=rows.filter(r=>r.verdict==='matches').length, w=rows.filter(r=>r.verdict==='wrong').length, c=rows.filter(r=>r.verdict==='cannot be checked').length;
  const sum=document.createElement('p'); sum.className='summary';
  const link=document.createElement('a'); link.href=rec.doc_url||rec.record_url||'#'; link.target='_blank'; link.rel='noopener'; link.textContent=rec.symbol;
  sum.appendChild(document.createTextNode(`Checked ${rows.length} claim(s) in the text against the recorded vote `));
  sum.appendChild(link);
  sum.appendChild(document.createTextNode(`: ${m} match, ${w} wrong, ${c} cannot be checked.`));
  res.appendChild(sum);
  // categories found
  const cats={ 'Vote count':0, 'Date':0, 'Session':0, 'State vote':0 };
  rows.forEach(r=>cats[r.cat]++);
  const parts=Object.keys(cats).filter(k=>cats[k]>0).map(k=>`${cats[k]} ${k.toLowerCase()} claim${cats[k]>1?'s':''}`);
  const missing=Object.keys(cats).filter(k=>cats[k]===0);
  const fp=document.createElement('p'); fp.className='note';
  fp.textContent='Found in the text: '+(parts.length?parts.join(', '):'no checkable claims')+(missing.length?'. Not found: '+missing.join(', ').toLowerCase()+'.':'');
  res.appendChild(fp);
  if(!rows.length){ res.appendChild(hintP('No checkable claims were found in the text.')); return; }
  const wrap=document.createElement('div'); wrap.className='tableWrap';
  const t=document.createElement('table');
  const thead=... '<tr><th>#</th><th>Claim as written</th><th>What the recorded vote says</th><th>Verdict</th></tr>'
  build with DOM.
  rows.forEach((r,i)=>{ tr: td1 i+1; td2: catTag + claim; td3 says (+note); td4 badge });
  wrap.appendChild(t); res.appendChild(wrap);
}
```

catTag: small span.

Badge: span class 'badge b-'+verdictClass where verdictClass: matches→'match', wrong→'wrong', 'cannot be checked'→'cant'. Text: 'matches' / 'wrong' / 'cannot be checked'.

Legend static in HTML below results.

Alright, also the "how computed" for check: static text.

Now assemble everything. Also add small CSS for select, buttons, textarea, status, tableWrap overflow.

Time to write the final output. I'll be careful about quotes inside JS regex strings — use regex literals, fine.

One more detail: extractStates pass1 regex — the subject part: I'll write:

```js
const SUBJ = /\b((?:[A-Z][A-Za-z'’.\-]*|of|the|and|de|del|van|von|al|bin|el|la|le|du|di)(?:\s+(?:[A-Z][A-Za-z'’.\-]*|of|the|and|de|del|van|von|al|bin|el|la|le|du|di)){0,5})\s+(voted\s+(?:in\s+favo[u]?r|for|against|yes|no|to\s+abstain)|abstained|did\s+not\s+vote)\b/gi;
```

Note: this could match "Yes" as subject start... "Yes, Kenya voted in favour" — at "Yes": subject "Yes" then needs \s+ voted... "Yes, Kenya" — comma breaks → fail; at "Kenya" ✓.

Potential catastrophic backtracking? Bounded {0,5}, fine.

statesIn: also strip leading "The ".

Also in pass2, names list includes names with parentheses stripped etc. Also include original names. Dedup names list.

Also names like "Côte d'Ivoire" — esc handles apostrophe? esc escapes regex specials; ' is not special. ✓.

Also lowercase sentence-start names? Names capitalized; text may have "kenya voted" lowercase — regex 'gi' with name capitalized won't match lowercase 'kenya'. Add 'i' flag → matches any case ✓ (I use 'gi').

But 'i' flag on name "PRK"? names are full names. OK.

Now the dedup key for states: iso+'|'+way. But claim text differs between pass1/pass2 — keep first (pass1). Also two different sentences same state same way → dedup to one row. Fine (claim as written = first occurrence).

Also counts dedup includes claim text; "29 votes in favour" appearing twice → one row. OK.

Write final.

Also add `lang="en"`.

Let me also make sure the "Ask AI" button label exactly "Ask AI for a briefing" and "Check" button "Check". ✓.

Also mention in AI card: "The model is slow and costs money; at most this sends 1 item (symbol + title)." ✓.

Final code writing now. I'll aim for clarity and correctness.

Also: `window.WORKSHOP_DATA` may exist but hrc missing → handle.

Let me write the script section completely:

```js
(function(){
"use strict";
var W = window.WORKSHOP_DATA || {};
var HRC = W.hrc || {records:[], countries:{}, vote_codes:{}};
var records = Array.isArray(HRC.records) ? HRC.records : [];
var countries = HRC.countries || {};
var voteCodes = HRC.vote_codes || {Y:'Yes',N:'No',A:'Abstain'};
function $(id){return document.getElementById(id);}
function esc(s){return String(s).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function textNode(s){return document.createTextNode(s==null?'—':String(s));}
function pad(n){return (n<10?'0':'')+n;}

// header line
var years = records.map(function(r){return r.year;}).filter(function(y){return typeof y==='number';});
$('dataLine').textContent = 'Source: Human Rights Council recorded votes (window.WORKSHOP_DATA.hrc, from the OHCHR Search Library) — '
  + records.length + ' recorded votes'
  + (years.length ? ', ' + Math.min.apply(null,years) + '–' + Math.max.apply(null,years) : '')
  + '. Every number on this page is counted from these records by the page itself; nothing is estimated.';

// picker
var sel = $('resSelect');
var sorted = records.slice().sort(function(a,b){
  return ((b.year||0)-(a.year||0)) || String(a.symbol||'').localeCompare(String(b.symbol||''));
});
sorted.forEach(function(r,i){
  var o=document.createElement('option');
  o.value=String(i);
  o.textContent=(r.symbol||'(no symbol)')+' — '+(r.title||'');
  sel.appendChild(o);
});
var defIdx = 0;
for(var i=0;i<sorted.length;i++){ if(sorted[i].symbol==='A/HRC/RES/51/27'){ defIdx=i; break; } }
sel.value=String(defIdx);
```

rollCounts, chart init, renderDetails, etc.

Chart:
```js
var chart=null;
if(window.Chart){
  chart=new Chart($('voteChart').getContext('2d'),{
    type:'bar',
    data:{labels:['In favour','Against','Abstaining'],datasets:[
      {label:'Official totals (record fields)',data:[0,0,0],backgroundColor:'#1f6fb2'},
      {label:'Roll call (counted from the votes map)',data:[0,0,0],backgroundColor:'#9cc3e5'}
    ]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
      scales:{x:{beginAtZero:true,title:{display:true,text:'Votes'}}},
      plugins:{legend:{position:'bottom'}}}
  });
} else { $('voteChart').style.display='none'; }
```

Names builder as planned.

extract functions as planned.

checkText builds rows and renders.

AI handlers as planned.

Init: renderDetails(); sel.onchange=renderDetails.

Also initial results hint.

Edge: records empty → sel disabled, details shows message. I'll add guard in renderDetails: if(!records.length){...}.

Now write it all out. Also CSS.

Let me make sure the table header uses thead properly.

I'll now produce the final response.