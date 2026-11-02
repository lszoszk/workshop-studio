Let me understand the task. Build a briefing checker for HRC resolutions:

1. A dropdown/picker to pick a resolution from `WORKSHOP_DATA.hrc.records` (start with A/HRC/RES/51/27 — but I must not hard-code; I should select it if present, else first record). Actually "start with A/HRC/RES/51/27" — I can pre-select that symbol if it exists in the data, otherwise default to first. That's reading from data, fine.

2. A button "Ask AI for a briefing" that calls `await studio.ask(prompt, {json:true})` with a prompt asking for a ~250-word briefing on the resolution, sending ONLY the symbol and title (none of our data). Show progress, allow stop? The instructions say batch work, show progress, let user stop — that's for batch over records; here it's a single call, but still show "sending to model" notice: how many records (1 — just symbol+title) and that it left the browser. Render answer in element with `data-source="ai"`.

3. A text box (textarea) pre-filled with the AI answer, editable, where user can paste their own text.

4. A "Check" button that parses the text for checkable claims:
   - numbers in favour / against / abstaining (yes/no/abstain totals)
   - the date
   - the session
   - each State said to have voted a certain way (e.g., "Kenya voted in favour", "France voted against", "X abstained")
   
   Show a table: claim as written | what recorded vote says | verdict: matches / wrong / cannot be checked. Explain "cannot be checked" ≠ "wrong".

Parsing approach (deterministic, in JS):
- Numbers: find patterns like "29 in favour", "29 votes in favour", "in favour: 29", "29 for", "adopted with 29 votes in favour, 16 against and 1 abstention". Need robust regex. Let me design patterns:
  - in favour: /(\d+)\s+(?:votes?\s+)?in\s+favou?r/i, also "favou?r[:\s]+(\d+)", "for[:\s]+(\d+)" maybe risky. Also "adopted by (\d+) votes to (\d+) with (\d+) abstentions" — classic UN phrasing: "adopted by 29 votes to 16, with 1 abstention". Handle that.
  - against: /(\d+)\s+(?:votes?\s+)?against/i, "to (\d+)" in the "X votes to Y" pattern, "against[:\s]+(\d+)"
  - abstain: /(\d+)\s+(?:votes?\s+)?abstain/i, "with (\d+) abstention"
  
  Also handle "unanimously" / "without a vote" — cannot be checked? Actually if text says "adopted unanimously" and record has yes=47, no=0, abstain=0, that matches? Hmm, keep it simpler: if "unanimously" appears, check no==0 && abstain==0 → matches, else wrong. Maybe include as a claim. Could be nice but adds complexity. I'll include it lightly.

- Date: find dates in text. Patterns: ISO "2023-10-13", "13 October 2023", "October 13, 2023", "13 Oct 2023". Compare to record.date. Verdict matches if equal; if a date is found but differs → wrong; if no date found → not a claim (don't list). Only list claims found in text.

- Session: text mentions session like "51st session", "at its 51st session", "during the 51st session". Record.session is like "51st session" or "Human Rights Council at its 54th session". Extract ordinal number from both and compare. If text contains "session" with a number, compare numbers. If text mentions session without number → cannot be checked? Hmm. Let's extract number from record.session via /(\d+)/. If text has "(\d+)(?:st|nd|rd|th)\s+session" compare. If text mentions "session" but no ordinal → cannot be checked (we can't verify which session from text alone... actually we could check if record.session string appears in text). Simpler: if record.session text (normalized) appears in the briefing → matches; else if an ordinal session is mentioned and differs → wrong; else cannot be checked.

- States voting a certain way: patterns like "Kenya voted in favour", "France voted against", "Germany abstained", "X voted yes", "X voted no", "X abstained from voting", "voted with ...". Need to map country names to ISO3 via `WORKSHOP_DATA.hrc.countries` (ISO3 → name). Build reverse map name → ISO3 (case-insensitive, also handle lowercase). Patterns:
  - /([A-Z][a-zA-Z'’\-]+(?:\s+[A-Z][a-zA-Z'’\-]+)*)\s+voted\s+(in\s+favou?r|for|yes|against|no|abstain(?:ed)?)/gi — tricky with multi-word names like "Russian Federation", "United States", "South Africa", "Côte d'Ivoire". Better approach: for each country name in the map, search text for name followed by a vote phrase within a short window: new RegExp(escape(name) + "\\s+(?:voted|votes)\\s+(.{0,30})", "i") then parse the trailing phrase. Also patterns "X abstained", "X did not vote"? votes map only has Y/N/A for members; non-members can't be checked → "cannot be checked" (country not a Council member in this vote / not in roll call). That's a good use of "cannot be checked": e.g., a State mentioned that isn't in the votes map (not a member at that time) → cannot be checked in this data. Also if the vote phrase can't be parsed → cannot be checked.

  Vote phrase mapping: "in favour", "for", "yes", "voted yes" → Y; "against", "no", "voted no" → N; "abstain", "abstained", "abstention" → A. Also "voted in favour of", "voted against". Also "X voted with the majority"? skip.

  Also handle "X and Y voted in favour" — the regex per country name handles each name individually if followed by "voted..."; "X and Y voted in favour" — Y is followed by "voted in favour" but X is followed by "and Y voted..." — my per-name regex requires name immediately followed by voted. Could extend: name followed by optional "(,| and) <other names>" then voted. Simpler: also match pattern where name appears in a list before "voted": find all matches of /((?:[A-Z][\w'’\-]+(?:\s+(?:and|,)\s+|\s+))+)\s+voted\s+(...)/ — getting complicated. Alternative: for each country name, regex: name + "\\s*(?:,|\\s+and\\s+)?\\s*(?:[A-Z][\\w'’\\-]+\\s+){0,3}?\\s*voted\\s+..." too loose.

  Pragmatic approach: two patterns:
  1. name + "\\s+voted\\s+(phrase)" (direct)
  2. name + "\\s+(?:,|and)\\s+" + otherName + "\\s+voted\\s+(phrase)" — handle by scanning: find all occurrences of /voted\s+(in\s+favou?r|against|abstain\w*|yes|no|for)/gi, then look backwards up to ~60 chars for country names: take the text segment before the match (say 80 chars), find all country names present in that segment that are "close" (within the segment and after the last sentence boundary). Hmm, could over-capture: "Kenya and France voted in favour" — segment before "voted in favour" is "Kenya and France " → both names found → both claimed in favour. Good. But "France voted against while Kenya voted in favour" — for the "in favour" match, segment before is "...while Kenya " → contains France too if within 80 chars → wrongly claims France in favour. Mitigate: split segment at sentence/clause boundaries (".", ";", " while ", " whereas ", " but ", " although ", ","). Take the last clause. In "France voted against while Kenya voted in favour", the clause before "voted in favour" after splitting on "while" is "Kenya " → only Kenya. 

  Let me implement: for each match of vote-phrase regex, take preceding 100 chars, split on /[.;:!?]\s*|\s+(?:while|whereas|although|but|however|and\s+then)\s+/i, take last piece, find country names in it (longest match first to handle "South Africa" vs "Africa"? names are full country names; check each name with word boundaries, sort by length desc). For each found name, record claim: name + vote phrase → expected code. Also handle "abstained" without "voted": pattern /(name)\s+abstained/ — covered if phrase regex includes "abstained" as a vote phrase: /(?:voted\s+)?(in\s+favou?r|against|abstain\w*|yes|no)\b/ — but "no" as a word is dangerous ("no votes against"?). Hmm "voted no" fine; bare "no" risky. Restrict: phrase must follow "voted" OR be "abstained"/"abstention". So regex: /voted\s+(in\s+favou?r|favou?r|for|against|yes|no|abstain\w*)|abstain(?:ed|s)?\b/gi. For the abstained case, the preceding-clause approach also works.

  Also "in favour of the resolution" — "in favour" captured, trailing "of the resolution" ignored. Good.

  Edge: "The resolution was adopted with 29 votes in favour, 16 against and 1 abstention." — the numbers patterns catch these; the state-claim scan: "votes in favour" — phrase regex requires "voted" not "votes". "votes in favour" — my regex `voted\s+` won't match "votes". Good, but "abstain\w*" bare could match "1 abstention" → preceding clause "16 against and 1 " → no country names → no claim. Fine.

  Also "X voted in favour of..." fine.

- Also check "adopted by X votes to Y with Z abstentions" pattern for numbers.

Verdicts:
- matches: claim value === record value.
- wrong: claim value !== record value (both present).
- cannot be checked: e.g., state not in votes map (not a member / no recorded vote), or claim type not present in data (e.g., session mentioned without number and record.session doesn't literally appear), or date format unrecognized? If a date-like string found but unparseable → cannot be checked. Also amendment records may have empty doc_url — fine.

Also the roll call vs official totals discrepancy: the spec says counting votes gives roll call which differs from totals for a few records — show both. So in the resolution header, show official totals (yes/no/abstain) AND roll-call counts computed from votes map, noting they may differ. For claim checking, which to compare against? The claim "29 in favour" — compare against official `yes` primarily; but maybe show both in "what the recorded vote says" column: "Official totals: 29 Y / 16 N / 1 A; roll call count: 28/16/1". Verdict: matches if claim equals official total; if it equals roll-call count but not official → hmm. I'd say: verdict matches if it matches the official total; if it matches the roll-call count instead, verdict "matches" but note? Simpler and honest: compare against official totals, and in the "recorded vote" column show both numbers. If claim matches roll-call but not official, verdict could be "matches (roll call)" — let me do: if claim == official → "matches"; else if claim == rollcall → "matches (roll-call count, differs from official total)"; else "wrong". Actually keep verdicts to the three required values, with the explanation column carrying nuance. I'll implement: matches if equals official; else if equals roll-call count, verdict "matches" but the "what the data says" cell notes "roll-call count is X (official total Y)". Hmm, that could confuse. Alternative: verdict "cannot be checked"? No — it can be checked. I'll do: primary comparison official; if mismatch but equals roll call, verdict "matches" with note. Let me just include note text. Actually simplest honest approach: the "what the recorded vote says" column shows "yes: 29 (official) / 29 (roll call)". Verdict matches if claim equals either, with a footnote if they differ and claim matched only one. I'll implement verdict logic: if claim===official → matches; else if claim===rollcall → matches (note in column); else wrong.

For state votes: compare claim code to votes[iso3]. If country not in votes map → cannot be checked (with reason: not among the 47 recorded votes for this vote — either not a Council member then or no vote recorded). If votes[iso3] missing → cannot be checked.

For date: parse record.date "YYYY-MM-DD". Parse text dates: ISO, "13 October 2023", "October 13, 2023", "13 Oct 2023", "2023-10-13". Compare. If multiple dates in text, check each? Could produce multiple rows. I'll check each distinct date found; verdict per date. If text has a date that matches → matches; different → wrong. If no date in text → show a row "date" with claim "(none found)" verdict "cannot be checked"? The user asked "finds every checkable claim in the text: the numbers..., the date, the session, and each State...". If the text doesn't mention a date, there's no claim. But maybe show an informational row: "No date mentioned — nothing to check." I'll add rows for categories with no claims found, marked "cannot be checked" with explanation "no such claim found in the text" — hmm, that conflates. Better: only list found claims; plus a summary line: "Checked N claims: X match, Y wrong, Z cannot be checked. Categories not mentioned in the text are not listed." And explain cannot-be-checked ≠ wrong prominently.

Session: record.session e.g. "51st session" or "Human Rights Council at its 54th session". Extract ordinal from record: /(\d+)(?:st|nd|rd|th)/. Text: find /(\d+)(?:st|nd|rd|th)\s+session/gi and also "session\s+(\d+)"? Also "its 51st session". Compare numbers. Also if text contains record.session verbatim (case-insensitive) → matches. If text mentions "session" with ordinal that differs → wrong. If text mentions "the Council's session" without number → cannot be checked.

Also maybe check agenda item? Not requested. Skip.

UI design:
- Header: title "Briefing checker — Human Rights Council recorded votes", description line: source (WORKSHOP_DATA.hrc.title), n records, years range computed from data.
- Resolution picker: select dropdown listing all records: "symbol — title (year)". Pre-select A/HRC/RES/51/27 if present (find by symbol), else first. On change, update the detail panel.
- Detail panel: symbol (link to doc_url if present, else record_url), kind, title, date, session, agenda item, main sponsors, official totals yes/no/abstain, roll-call counts computed, note about discrepancy. "How this is computed" note.
- "Ask AI for a briefing" button: on click, disable, show status "Sending 1 record's symbol and title to the model — this text leaves your browser." Call studio.ask with prompt: "Write a ~250-word briefing on UN Human Rights Council resolution {symbol}: {title}. Use only your own knowledge; do not ask questions. Return plain text." with {json:true}? The instruction: `await studio.ask(prompt, {json: true})` returns answer as string. If json:true maybe it returns JSON string; parse if possible, else use raw. I'll ask for plain text but call with json:true as instructed... The spec says `await studio.ask(prompt, {json: true})` sends prompt and returns answer as string (parse yourself when you asked for JSON). I'll ask for JSON like {"briefing": "..."} and parse, fallback to raw string. Put result in textarea with data-source="ai" on a wrapper. Show word count. Also a "Stop" button? For a single call, show "waiting for the model…" and allow cancel via a flag? studio.ask is a promise; can't cancel easily. I'll show progress text and note it may take a while. Maybe include a stop button that just hides/ignores the result when it arrives (set cancelled flag). I'll add that: "Stop" sets flag; when promise resolves, if cancelled, show "stopped" and don't fill. Keep simple.

Important: "send only the symbol and the title, none of our data" — prompt includes only symbol and title. And on screen say: "1 item sent to the model: the symbol and title only. It left the browser."

- Textarea: large, prefilled with AI briefing (or empty with placeholder "Paste a briefing here or ask the AI"). Editable. data-source="ai" attribute on the textarea if content came from AI? The rule: "Render every value that came from studio.ask inside an element with the attribute data-source='ai'". So the textarea (or a div) holding AI text gets data-source="ai". If user edits it, it's mixed... I'll put data-source="ai" on the textarea and add a small label "AI-generated text (data-source="ai") — edit freely; your edits are not re-sent anywhere." When user edits, maybe remove attribute? Keep it simple: keep attribute, note that edits are local. Actually to be safe: when user modifies the textarea, remove the data-source attribute and change label to "your text". Hmm, but then the AI provenance is lost. The rule is about rendering values from studio.ask — once edited it's user text. I'll keep the attribute but label clearly; simpler: on input, set a flag and update label "edited by you". I'll keep data-source="ai" only while unedited; on first input remove it and label "Your text (edited)". That's clean and honest.

- "Check" button: runs the checker, renders table. Columns: # | Claim as written (quote the matched text) | What the recorded vote says | Verdict. Verdict cell colored: matches (green), wrong (red), cannot be checked (grey/amber). Below table: explanation box: "Cannot be checked means this data has no recorded vote for that claim (e.g., the State was not among the 47 recorded votes, or the text doesn't give a number we can compare). It is not the same as wrong: wrong means the data contradicts the claim."

- Also a "How this is computed" note near the table: claims are extracted by deterministic patterns (list them briefly), compared to the record's official totals, roll call, date, session.

- Every row that shows a document has symbol linked to doc_url in new tab — the resolution detail does that; also maybe list of all resolutions? The picker covers it. Maybe also show a small "all recorded votes" table? Not required. Keep focused. But "Every row that shows a document has its symbol, linked to doc_url" — the detail panel shows symbol link. Fine. Maybe also in the claims table, the header row references the resolution symbol linked. I'll include a line above the table: "Checking against {symbol} (link)".

Data handling: read WORKSHOP_DATA.hrc; handle missing/empty records gracefully (show message). Years range: min/max of record.year. Countries map for names. vote_codes description.

Let me now write the parsing functions carefully.

```js
const HRC = window.WORKSHOP_DATA.hrc || {};
const records = Array.isArray(HRC.records) ? HRC.records : [];
const countries = HRC.countries || {}; // ISO3 -> name
const nameToIso = {};
Object.entries(countries).forEach(([iso, name]) => {
  nameToIso[name.toLowerCase()] = iso;
  // also without diacritics? normalize
});
```

Normalize function: lowercase, remove diacritics via normalize("NFD").replace(/\p{Diacritic}/gu,""), collapse spaces. Build map from normalized name → iso. Also add common short forms? e.g., "United States" vs "USA"? The data uses names like "Russian Federation", "United States"? In votes keys are ISO3; countries map gives names. Text may say "the United States" — normalized "united states" matches if map has "United States". Also "US" / "U.S." — add alias: if name is "United States of America" add "united states", "us", "u.s.". I'll add a few generic aliases: strip "the " prefix; for names containing "of America" add short. Keep it modest: also match name without leading "The ". And add alias for "Russian Federation" → "russia". I'll add: if normalized name includes "russian federation" add "russia"; "united states" variants; "côte d'ivoire" normalized "cote d'ivoire" — text may write "Côte d'Ivoire" → normalized matches. Also "Ivory Coast"? skip. Add "democratic republic of the congo" → "drc"? skip. Keep a small alias map applied generically: for each name, also register name with "the " removed, and if name matches /united states( of america)?/ register "us","u.s.","usa"; /russian federation/ → "russia"; /bolivia.*/ skip. Fine.

Finding country names in a text segment: sort names by length desc; for each, regex with boundaries: new RegExp("(?<![a-z])" + escaped + "(?![a-z])", "i") — lookbehind supported in modern browsers; sandbox likely modern. To be safe, use "(^|[^a-z])" + name + "([^a-z]|$)" with capture. I'll use a helper that scans with index checks manually to avoid lookbehind issues. Simpler: use matchAll with "g" flag and boundary groups.

Vote phrase detection:

```js
const VOTE_PATTERNS = [
  {re: /voted\s+in\s+favou?r(?:\s+of)?/gi, code: "Y"},
  {re: /voted\s+favou?r(?:\s+of)?/gi, code: "Y"},
  {re: /voted\s+for\b/gi, code: "Y"},
  {re: /voted\s+yes\b/gi, code: "Y"},
  {re: /in\s+favou?r(?:\s+of)?\b/gi, code: "Y"}, // risky? "in favour" without voted — e.g., "29 votes in favour" would trigger state scan; preceding clause "29 votes " has no country names, ok. But "countries in favour included Kenya"? then "in favour" match, preceding clause "countries " no names... the names come after. Hmm. Maybe skip bare "in favour" to avoid noise, or include but only names in preceding clause. "Kenya was in favour" — name before "in favour" within clause → claim. Include bare "in favour" but require a country name in the preceding clause (which is our design anyway — no name, no claim). Risk: "France voted against, while Kenya was in favour" — clause before "in favour" after splitting on "while" is "Kenya was " → Kenya Y. Good. Risk: "16 against and 1 abstention; Kenya in favour" fine.
  {re: /voted\s+against\b/gi, code: "N"},
  {re: /voted\s+no\b/gi, code: "N"},
  {re: /against\b/gi, code: "N"}, // bare "against" — "voted against" covered; "16 against" no names before... "France against"? Include bare "against"? "against the resolution" — "France voted against the resolution" — "voted against" matches first. Bare "against" could catch "France, against" weird. I'll include bare "against" too since no-name → no claim. But danger: "against" appears in "voted against" already matched; duplicates — dedupe claims by (country, code, span). Also "the 16 against" no names. OK include.
  {re: /abstain(?:ed|s|ing|ention)?\b/gi, code: "A"},
];
```

Hmm, bare "against"/"in favour" increase false positives in weird sentences but only produce claims when a country name is in the preceding clause. E.g., "Unlike France, Kenya voted in favour" — clause before "in favour": split on "," → last piece " Kenya voted " → Kenya Y. France not claimed. Good. "France and Kenya voted in favour" — clause "France and Kenya voted " → both Y. Good.

But: "Kenya voted in favour of the resolution, while France voted against" — for "against" match, preceding text "...while France voted " → split on "while" → "France voted " → France N. Good.

Dedupe: key = iso + code + matched phrase start? If same country claimed twice with same code, keep first (or list both?). List each distinct claim occurrence but dedupe identical (country, code) pairs — if a country is claimed both Y and N in text (contradiction), show both rows, verdicts computed independently. Fine.

Preceding clause extraction: take text.slice(max(0, m.index - 120), m.index), split on /[.;:!?]\s+|\s+—\s+|\s+(?:while|whereas|although|though|but|however|whereas)\s+/i, take last non-empty piece. Then find country names in it. Also handle "along with X"? skip.

Also pattern "X and Y abstained" — "abstained" bare pattern catches; clause "X and Y " → both A. Good.

Also "X did not vote" → cannot be checked? votes map has only Y/N/A; "did not vote" → claim "no vote recorded" — if country in votes map with a code, then "did not vote" contradicts → wrong? Hmm, "did not vote" isn't Y/N/A. I'd map "did not vote"/"not voting" to code "NV" and verdict: if votes[iso] exists → wrong (the roll call records a vote); if not in map → cannot be checked. That's a nice touch. Add pattern /did\s+not\s+vote|not\s+voting/ code "NV". Maybe skip to reduce complexity... I'll include it, it's easy.

Numbers extraction:

```js
function findNumberClaims(text) {
  const claims = [];
  // pattern A: "N in favour / N votes in favour / N for"
  const fav = [
    /(\d{1,3})\s+(?:votes?\s+)?in\s+favou?r/gi,
    /(\d{1,3})\s+(?:votes?\s+)?for\b/gi,
    /favou?r\s*[:\-]?\s*(\d{1,3})/gi,
    /in\s+favou?r\s*[:\-]?\s*(\d{1,3})/gi,
  ];
  ...
}
```

Careful: "29 votes in favour, 16 against and 1 abstention" — pattern /(\d+)\s+(?:votes?\s+)?in\s+favou?r/ matches "29 votes in favour". Against: /(\d{1,3})\s+(?:votes?\s+)?against\b/gi matches "16 against". Abstain: /(\d{1,3})\s+(?:votes?\s+)?abstain/gi matches "1 abstention". Also "with 1 abstention" — matches "1 abstention" via abstain pattern. Also "adopted by 29 votes to 16, with 1 abstention": add pattern /by\s+(\d{1,3})\s+votes?\s+to\s+(\d{1,3})(?:,?\s*with\s+(\d{1,3})\s+abstain\w*)?/gi → fav=29, against=16, abstain=1. Also "adopted ... 29-16-1"? pattern /(\d{1,3})\s*[-–]\s*(\d{1,3})\s*[-–]\s*(\d{1,3})/ — risky (dates like 2023-10-13 could match "2023-10-13"? \d{1,3} limits to 3 digits; "2023-10-13" — "023-10-13"? The regex would try to match within: "023-10-13" — \d{1,3} can match "023"? The string "2023-10-13": positions... "2023" is 4 digits; regex \d{1,3} could match "023" starting at index 1, then "-10-13" → matches "023-10-13" → fav=23? That's bad. Guard: require not preceded/followed by digit or hyphen-date context: use (?<![\d-]) and (?![\d-])? Lookbehind again. Alternative: require the triple pattern to be surrounded by non-digit non-hyphen: /(^|[^\d\-])(\d{1,3})\s*[-–]\s*(\d{1,3})\s*[-–]\s*(\d{1,3})(?!\d)/gm. "2023-10-13": try match starting... "2023-10-13" — the char before "023" is "2" (digit) so [^\d\-] fails at that position; could match starting at "2023"? \d{1,3} matches "202"? then next char "3" not "-" → backtrack... "202" then need \s*[-–] but next is "3" → fail; "20" then "2" fail; "2" then "0" fail. Then start at index1 "023-10-13": preceding char "2" is digit → [^\d\-] fails. index2 "23-10-13": preceding "0" digit → fail. index3 "3-10-13": preceding "2" digit → fail. So no match inside dates. Good. But "29-16-1" preceded by space → matches. OK include with guards. Also label it "adopted 29-16-1" style.

Also "yes: 29, no: 16, abstain: 1" — patterns /yes\s*[:\-]?\s*(\d{1,3})/gi etc. But "yes" appears in "voted yes" — "Kenya voted yes" → "yes" not followed by number, fine. "no" pattern dangerous: "no 16"? /no\s*[:\-]?\s*(\d{1,3})/ would match "no 16" but also "no 5" in "there were no 5..." rare. Also "No. 27" (resolution numbers!) — "A/HRC/RES/51/27" contains "RES/51/27" not "no". But "No. 27" text → "no" followed by ". 27"? pattern /no\s*[:\-]?\s*(\d{1,3})/ — "No. 27": "no" then "." — my pattern allows [:\-]? optional then \s* then digits; "." is not in [:\-] and not \s → no match. Good, but "no: 16" matches. Hmm "no" also in "not"? \b needed: /\bno\b\s*[:\-]?\s*(\d{1,3})/gi. "voted no" — "no" followed by "." or end → no digits → no match. OK.

To limit false positives, maybe restrict the "label: number" patterns to when label is one of yes/no/abstain/in favour/against/for with colon or "of". I'll include: /(?:yes|in\s+favou?r|favou?r|for)\s*[:\-–]?\s*(\d{1,3})\b/gi for Y... but "for 29"? "for" is common word: "for 29 years"? unlikely in briefing but possible. Require colon or "of": /(?:in\s+favou?r|favou?r)\s*(?:of|:|\-)\s*(\d{1,3})/gi and /\byes\s*[:\-]\s*(\d{1,3})/gi, /\bno\s*[:\-]\s*(\d{1,3})/gi, /\babstain\w*\s*[:\-]\s*(\d{1,3})/gi. And the "N votes in favour" style. And "X to Y with Z". And "X-Y-Z". That's decent coverage.

Dedupe number claims by (kind, value, index) — if same number found by two patterns at same spot, dedupe by kind+start index proximity. I'll collect with start index and dedupe per kind keeping first occurrence (or all occurrences? If briefing says "29 in favour" twice, one row is enough; but "every checkable claim" — I'll list each occurrence but dedupe identical kind+value+same index). Simpler: dedupe by kind + value + matched text. Eh — I'll dedupe by kind and start index (rounded). Let me just dedupe by kind+value+quote.

Date extraction:

```js
const MONTHS = {january:1,...};
function findDates(text) {
  const out = [];
  // ISO
  let m; const reISO = /\b(\d{4})-(\d{2})-(\d{2})\b/g;
  // "13 October 2023" / "13 Oct 2023"
  const reDmy = /\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s*,?\s+(\d{4})\b/g;
  // "October 13, 2023" / "Oct. 13 2023"
  const reMdy = /\b([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s*,\s*(\d{4})\b/g;
  ...
}
```

Month name → number via lookup with first 3 letters. Validate month 1-12, day 1-31. Compare with record.date parts. Verdict: matches if same date; wrong if different. If a date found that's unparseable (e.g., "October 2023" only) → cannot be checked? "October 2023" gives month+year; record date has day. Could compare year+month → if match, "matches (month/year)"? Keep: if only year found (e.g., "in 2023") — that's a year claim, not date. The user asked for "the date". I'll treat full dates; also handle "in October 2023" as partial → cannot be checked (no full date to compare)? Hmm, or compare month/year if record matches → matches. I'll implement: full date claims compared fully; month-year claims compared on year+month, verdict matches/wrong accordingly, and note "compared year and month only". Keep it but simple. Actually to reduce complexity, I'll only extract full dates (with day) plus ISO. If text has "October 2023" without day, skip (no claim). Hmm, briefings often say "adopted on 13 October 2023" — full date likely. Also "on 7 October 2025". OK full dates only, plus ISO. Also "2023" alone → year claim? The user listed "the date" — I'll also check bare 4-digit years? That might conflict with resolution numbers (51/27 no). "in 2023" → year claim compared to record.year. I'll add year claims: /\b(19|20)\d{2}\b/g but exclude those that are part of a full date already matched (track spans). Verdict vs record.year. That's useful. But careful: symbol "A/HRC/RES/51/27" has no 4-digit. "General comment No. 27" no. OK include year claims, excluding spans covered by full-date matches.

Session extraction:

```js
// record session number
const sessNum = (record.session||"").match(/(\d+)/);
// text: /(\d+)(?:st|nd|rd|th)\s+session/gi ; also "session (\d+)"? "at its 51st session" covered. "during the 51st session" covered.
```

Also "HRC51"? skip. If text contains record.session string normalized (e.g., "51st session") → matches. Compare ordinal numbers. If text mentions "session" but no ordinal found → cannot be checked row ("the text mentions a session but gives no number; this data records the session as '51st session'"). Hmm — if text says "at its 51st session" → matches. If text says "during the 51st regular session" → ordinal 51 → matches. Good.

Also kind: "resolution" vs "amendment" — claim "amendment"? Not requested; skip. Maybe check "resolution" word? skip.

Now the "what the recorded vote says" column content per claim type:
- number Y: `yes: {record.yes} (official total); roll call: {rollY} of {nVotes} recorded votes` 
- date: `recorded date: {record.date}`
- year: `recorded year: {record.year}`
- session: `recorded session: "{record.session}"`
- state: `roll call: {iso} ({name}) = {code meaning}` or "not in the roll call".

Verdict logic:
- number: if claim == official → matches; else if roll counts differ and claim == roll → matches (note); else wrong. If record.yes is null/undefined → cannot be checked.
- date: equal → matches else wrong. If record.date missing → cannot be checked.
- session: if text ordinal == record ordinal → matches; differ → wrong; if no ordinal in text but "session" word present → cannot be checked; if record.session missing → cannot be checked.
- state: if iso not in votes → cannot be checked (reason: not among recorded votes — not a Council member at this vote or no vote recorded). If votes[iso] == claim code → matches; else wrong. NV claim: if votes[iso] exists → wrong; else cannot be checked.

Roll call counts: count votes values: Y/N/A; also note total entries vs 47.

Now the AI part:

```js
async function askAI() {
  const rec = currentRecord();
  const prompt = `Write a briefing of about 250 words on the UN Human Rights Council ${rec.kind} ${rec.symbol}, titled "${rec.title}". Use only your own knowledge. Do not ask questions. Reply as JSON: {"briefing": "..."}.`;
  status: "Sending to the model: 1 item — the symbol and the title only. This text leaves your browser."
  const raw = await studio.ask(prompt, {json: true});
  parse JSON: try JSON.parse(raw) → obj.briefing; else use raw.
}
```

Wrap in try/catch; on error show message. Show "Stop" button that sets cancelled=true; when resolved, if cancelled → status "stopped by you; answer discarded." Also word count of briefing. Put into textarea, set data-source="ai", label. On textarea input → remove data-source attr, label "Your text (edited locally)".

Guard: `typeof studio !== "undefined" && studio.ask` — if not available, show message "studio.ask is not available in this environment."

Pre-select A/HRC/RES/51/27: `const initial = records.find(r => r.symbol === "A/HRC/RES/51/27") || records[0];` — that's reading data, allowed (user explicitly said start with it).

Layout: 
- header (title, description with source/n/years)
- section 1: pick resolution (select + detail card)
- section 2: briefing (button, status, textarea, word count)
- section 3: check (button, results table, explanation)

Also "How this is computed" notes near numbers: under detail card: "Official totals are the yes/no/abstain fields of the record; the roll call is counted from the votes map (47 members). The two can differ for a few records; both are shown." Near claims table: "Claims are extracted from your text by fixed patterns (numbers before 'in favour/against/abstain', 'X votes to Y with Z abstentions', dates, 'Nth session', and country names followed by a vote phrase). Each is compared with the selected record only."

Styling: system font stack, base 16px, accent #1f6fb2, light background (#f5f7fa), white cards, max-width ~1000px, no horizontal scroll. Verdict colors: matches #1a7f37 (green), wrong #b3261e (red), cannot #6b6b6b grey with amber? Use grey #666 with background #f0f0f0. Table with borders, readable at projector distance.

Chart? Not required. Could add a small bar of votes? Not necessary; keep focused. Maybe a tiny stacked bar showing Y/N/A — nice but optional. The instructions say use Chart.js for charts; charts optional. I'll add a simple horizontal stacked bar using plain divs (not a chart) or skip. I'll add a simple CSS bar showing yes/no/abstain proportions — it's a "number" so needs a "how computed" note. Keep it: a proportional bar with counts labeled. Simple divs, no Chart.js needed (it's not a chart per se). Fine.

Empty data handling: if records empty → show "No recorded votes in the data."

Also handle records with missing fields (votes undefined, doc_url empty → link to record_url or no link; show symbol text without link if no URL).

Let me also show in detail: main_sponsors joined, agenda_item, kind, session, date, year.

Now write the code. Aim under 700 lines. Let me draft.

HTML structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Briefing checker — HRC recorded votes</title>
<style>...</style>
</head>
<body>
<header>
  <h1>Briefing checker — Human Rights Council recorded votes</h1>
  <p class="desc" id="dataset-desc"></p>
</header>
<main>
  <section class="card" id="pick">
    <h2>1. Pick a recorded vote</h2>
    <label for="res-select">Resolution / amendment:</label>
    <select id="res-select"></select>
    <div id="res-detail"></div>
    <p class="note" id="res-note"></p>
  </section>
  <section class="card" id="brief">
    <h2>2. Briefing text</h2>
    <p>...</p>
    <button id="ask-btn">Ask AI for a briefing</button>
    <button id="stop-btn" hidden>Stop</button>
    <p id="ai-status" class="status"></p>
    <label for="briefing-text">Briefing text (AI answer appears here; you can edit or paste your own):</label>
    <textarea id="briefing-text" rows="10" placeholder="..."></textarea>
    <p class="note" id="briefing-meta"></p>
  </section>
  <section class="card" id="check">
    <h2>3. Check the claims</h2>
    <button id="check-btn">Check</button>
    <div id="results"></div>
    <div id="verdict-legend">...</div>
    <p class="note">How this is computed...</p>
  </section>
</main>
<script>...</script>
</body>
</html>
```

JS details:

```js
const DATA = window.WORKSHOP_DATA || {};
const HRC = DATA.hrc || {};
const records = Array.isArray(HRC.records) ? HRC.records : [];
const countries = HRC.countries || {};
```

Build name→iso with normalization:

```js
const norm = s => (s||"").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ").trim();
const nameToIso = new Map();
for (const [iso, name] of Object.entries(countries)) {
  const n = norm(name);
  if (n) nameToIso.set(n, iso);
  // aliases
  const aliases = [];
  if (/united states/.test(n)) aliases.push("united states","us","usa","u s");
  if (/russian federation/.test(n)) aliases.push("russia");
  if (/^the /.test(n)) aliases.push(n.slice(4));
  for (const a of aliases) if (!nameToIso.has(a)) nameToIso.set(a, iso);
}
// sorted names longest first for scanning
const names = Object.values(countries).map(norm).filter(Boolean).sort((a,b)=>b.length-a.length);
```

Wait — nameToIso maps normalized name → iso; names list for scanning should be the normalized names. But scanning text: I need to find occurrences of country names in raw text. Approach: normalize the whole text once? That would break index mapping for quotes. Alternative: for each name, build regex from escaped original name? Names may have diacritics in text differently. Pragmatic: scan the raw segment with a regex built from the normalized name converted to a pattern allowing optional non-letter chars between letters? Overkill.

Simpler robust approach: create a normalized version of the text where each character position maps back to original index. Build arrays: normChars (normalized text) and indexMap (original index of each norm char). Then for each name (normalized), find all occurrences in normText with boundary check (prev/next char not a-z), get original span via indexMap, and extract the original substring for the quote. 

Implementation:

```js
function normalizeWithMap(text) {
  let out = ""; const map = [];
  for (let i=0;i<text.length;i++){
    const ch = text[i];
    const n = ch.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
    for (const c of n) {
      if (/[a-z0-9]/.test(c)) { out += c; map.push(i); }
      else if (c === " " || /[^\w\s]/.test(ch)) { /* punctuation becomes space */ }
    }
    // ensure separator: if char produced nothing (e.g., punctuation), push a space
    if (n === "" || !/[a-z0-9 ]/.test(n)) { out += " "; map.push(i); }
    else if (n === " ") { out += " "; map.push(i); }
  }
  return {norm: out, map};
}
```

Hmm, getting fiddly. Let me simplify: iterate chars; for each char compute normalized expansion; if expansion contains letters/digits, append them with map entries; else append single space with map to this char. Also lowercase letters map to themselves. Also collapse? Don't collapse spaces (keeps indices simpler). Multiple spaces fine.

```js
function normMap(text){
  let norm=""; const map=[];
  for(let i=0;i<text.length;i++){
    const ch=text[i];
    let e=ch.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
    if(/[a-z0-9]/.test(e)){
      for(const c of e){ if(/[a-z0-9]/.test(c)){ norm+=c; map.push(i);} }
    } else {
      norm+=" "; map.push(i);
    }
  }
  return {norm,map};
}
```

Note: "é".toLowerCase().normalize("NFD") → "e" + combining accent; strip → "e". Good. Apostrophes → space: "Côte d'Ivoire" → "cote d ivoire" (apostrophe → space) → normalized name "cote d ivoire" matches. Good.

Then find names:

```js
function findCountriesInRange(normText, map, start, end, nameToIso, names){
  const found = [];
  const seg = normText.slice(start, end);
  for (const name of names) {
    let idx = seg.indexOf(name);
    while (idx !== -1) {
      const s = start + idx, e = s + name.length;
      const before = s>0 ? normText[s-1] : " ";
      const after = e<normText.length ? normText[e] : " ";
      if (!/[a-z0-9]/.test(before) && !/[a-z0-9]/.test(after)) {
        const iso = nameToIso.get(name);
        found.push({iso, name, origStart: map[s], origEnd: map[Math.min(e-1, map.length-1)] + 1});
      }
      idx = seg.indexOf(name, idx + 1);
    }
  }
  // remove overlaps: keep longest / first
  found.sort((a,b)=> (b.origEnd-b.origStart) - (a.origEnd-a.origStart) || a.origStart-b.origStart);
  const chosen = [];
  for (const f of found) {
    if (!chosen.some(c => !(f.origEnd <= c.origStart || f.origStart >= c.origEnd))) chosen.push(f);
  }
  return chosen;
}
```

Names sorted longest-first globally so "south africa" found before "africa"? "africa" isn't a country name in map probably. But "united states" vs "states"? fine. Overlap removal keeps longest.

Vote phrase scanning on normalized text too (so "in favour" matches "in favour" regardless of case; "favour" British). Patterns on norm text:

```js
const PHRASES = [
  {re:/\bvoted in favour\b/g, code:"Y"},
  {re:/\bvoted for\b/g, code:"Y"},
  {re:/\bvoted yes\b/g, code:"Y"},
  {re:/\bin favour\b/g, code:"Y"},
  {re:/\bvoted against\b/g, code:"N"},
  {re:/\bvoted no\b/g, code:"N"},
  {re:/\bagainst\b/g, code:"N"},
  {re:/\babstained\b/g, code:"A"},
  {re:/\babstention\b/g, code:"A"},
  {re:/\babstain\b/g, code:"A"},
  {re:/\bdid not vote\b/g, code:"NV"},
];
```

Wait "in favour" bare: "29 votes in favour" → match at "in favour"; preceding clause "29 votes " → no country → no claim. OK. "against" bare: "16 against" → no country. "the resolution was adopted ... against"? fine.

But danger: "against" in "voted against" already matched by earlier pattern; both matches produce claims only if country in preceding clause — "France voted against" → "voted against" match: clause "france voted " → France N. "against" match: clause "france voted " → France N duplicate. Dedupe by (iso, code) — keep first occurrence, but quote maybe from first. Dedupe key iso+code; if same iso claimed with different codes, keep both (contradiction in text — both rows shown, each judged). Good.

Preceding clause: from norm text, take normText.slice(max(0, m.index-140), m.index), split on /[.;:!?—–-]\s+|\s+(?:while|whereas|although|though|but|however|yet)\s+/ — careful: hyphen split could break "cote d'ivoire"? apostrophe already space in norm. Hyphen in "well-known" → splits; acceptable. Actually splitting on "-" might split "twenty-one"? fine.

Hmm wait: splitting on "-" would split "A/HRC/RES/51/27"? "/" not in split set. OK. But "non-binding" splits — fine.

Take last piece, then find countries in that range (need global indices: compute split with indices). Implementation: 

```js
function precedingClause(normText, pos){
  const from = Math.max(0, pos-140);
  const seg = normText.slice(from, pos);
  const parts = seg.split(/(\s+(?:while|whereas|although|though|but|however|yet)\s+|[.;:!?]\s*)/i);
  // split with capture keeps separators; take last non-separator chunk
  let last = "";
  for (let i=parts.length-1;i>=0;i--){ if(parts[i] && !/^\s*(?:while|whereas|although|though|but|however|yet)\s*$/i.test(parts[i]) && !/^[.;:!?\s]+$/.test(parts[i])) { last = parts[i]; break; } }
  const start = from + seg.lastIndexOf(last);
  return {start: Math.max(from, start), end: pos};
}
```

Hmm lastIndexOf(last) could find earlier duplicate; acceptable. Edge: last empty → return whole seg.

Then findCountriesInRange(normText, map, clauseStart, clauseEnd).

Quote for claim: original text slice from country origStart to phrase end: map[m.index + phrase.length - 1] + 1. Claim as written: text.slice(countryOrigStart, phraseEndOrig). E.g., "Kenya voted in favour". 

Number claims on original text (numbers unaffected by normalization; but easier on norm text too — digits preserved). Use norm text for matching, map back for quotes. Patterns:

```js
const NUM_PATTERNS = [
  {kind:"Y", re:/(\d{1,3})\s+(?:votes?\s+)?in favour/g},
  {kind:"Y", re:/(\d{1,3})\s+(?:votes?\s+)?for\b/g},
  {kind:"Y", re:/\b(?:in )?favour\s*(?:of|:|-)\s*(\d{1,3})/g},
  {kind:"Y", re:/\byes\s*[:\-]\s*(\d{1,3})/g},
  {kind:"N", re:/(\d{1,3})\s+(?:votes?\s+)?against\b/g},
  {kind:"N", re:/\bno\s*[:\-]\s*(\d{1,3})/g},
  {kind:"N", re:/\bagainst\s*(?:of|:|-)\s*(\d{1,3})/g},
  {kind:"A", re:/(\d{1,3})\s+(?:votes?\s+)?abstain\w*/g},
  {kind:"A", re:/\babstain\w*\s*[:\-]\s*(\d{1,3})/g},
  {kind:"Y", re:/\bby\s+(\d{1,3})\s+votes?\s+to\s+(\d{1,3})/g, pair:true}, // special
];
```

The "by X votes to Y" pattern needs custom handling: capture both. I'll handle separately:

```js
const reTo = /\b(\d{1,3})\s+votes?\s+to\s+(\d{1,3})(?:\s*,?\s*with\s+(\d{1,3})\s+abstain\w*)?/g;
```
→ Y=g1, N=g2, A=g3 (if present).

And triple: /(^|[^\d\-–])(\d{1,3})\s*[–—-]\s*(\d{1,3})\s*[–—-]\s*(\d{1,3})(?!\d)/gm on norm text — norm text has spaces instead of punctuation, so "29-16-1" becomes "29 16 1" in norm! Because "-" → space. Hmm. That breaks the dash pattern on norm text. Do number patterns on original text instead, and map indices via... I have map from norm→orig, not orig→norm. Alternative: build reverse: for quoting, I can just use the original match index directly since I match on original text. But then case/diacritics don't matter for numbers — numbers and "in favour" are ASCII mostly; "favour" vs "favor" — handle both spellings in regex on original text with /gi. Diacritics irrelevant for these phrases. So: run number/date/session/phrase patterns on ORIGINAL text with /gi, and run country-name finding on the normalized text using map. But phrase matches need to align with norm indices for country lookup...

Simpler unified approach: do everything on the normalized text, but preserve hyphens in normalization? If I keep "-" as "-" in norm (instead of space), then "29-16-1" stays, and "cote d'ivoire" → "cote d-ivoire"? Then normalized country names must also keep hyphens: normalize names the same way (keep "-"). Let me change normMap: letters/digits kept; everything else → " " EXCEPT "-" and "–" kept as "-". Then "A/HRC/RES/51/27" → "a hrc res 51 27" (slashes → spaces) — fine. "29-16-1" → "29-16-1". Country "Côte d'Ivoire" → "cote d-ivoire"; name normalized same way → match. Good.

Then all patterns run on normText (lowercased already, so no /i needed but harmless), quotes via map. 

Date patterns on normText: ISO "2023-10-13" preserved (hyphens kept). "13 october 2023" fine. Month lookup on normalized month names.

Year claims: /\b(19|20)\d{2}\b/g on normText, excluding spans inside date matches. Note "51/27" → "51 27" no. Resolution "res 51 27" fine. But "a hrc res 51 27" — no 4-digit. Good. However briefing might mention other years (e.g., "since 2006") → would create year claims compared to record.year → "wrong" verdicts for unrelated years! Hmm. That's a problem: "adopted in 2023" is the claim; but "the mandate was created in 2011" would be flagged wrong. The user asked to check "the date" — I should only check dates/years in proximity to adoption context? Hard. Compromise: only treat a year as a date claim if it appears within ~40 chars of words like "adopted", "vote", "on", "date", "resolution", "session"? Or: only check full dates (with day) and ISO dates, plus years that appear adjacent to "adopted|adopted on|passed|vote took place|on". Let me restrict: year claim only if the 4-digit year is within 30 chars before/after a keyword (adopted, adoption, voted, vote, resolution, passed, adopted on). Actually simpler: only extract full dates (day+month+year or ISO). If the text only says "in 2023", no full date → no date claim; but then a briefing saying just "adopted in 2023" has no checkable date claim... The user said "the date" — full date expected. I'll extract full dates; additionally, if no full date found but a year appears near "adopt"/"vote"/"resolution", add a year-level claim compared on year only, labeled "year only". Hmm, complexity. Decision: extract full dates always; extract bare years ONLY when within 40 chars of /adopt|vote|resolution|passed|session/ — compare to record.year. This limits false positives like "since 2011" (unless near those words... "mandate created in 2011" — "mandate" not keyword; ok). "the 2023 resolution" → year claim, matches. Acceptable.

Actually also "on 13 October 2023" full date covers most. Keep both mechanisms.

Session patterns on normText: /(\d{1,3})(?:st|nd|rd|th)\s+session/g; also /session\s+(\d{1,3})/g; also "hrc\s*(\d{1,3})"? e.g., "HRC51"? skip. Also record.session may be "Human Rights Council at its 54th session" → ordinal 54. Also "51st session" in record. Compare numbers. Also if normText includes norm(record.session) → matches directly.

Also check "agenda item"? not requested, skip.

Now verdicts & table rendering. Build claims array:

```js
{type: "number"|"date"|"year"|"session"|"state", quote, claimDesc, dataDesc, verdict, reason}
```

Render table rows. Verdict classes.

Summary line: "N claims found: X match, Y wrong, Z cannot be checked." Plus legend explaining cannot ≠ wrong.

Also handle: text empty → message "The text box is empty — nothing to check."

Roll call computation:

```js
function rollCall(rec){
  const v = rec.votes || {};
  let y=0,n=0,a=0,other=0;
  for (const k in v){ const c=(v[k]||"").toUpperCase(); if(c==="Y")y++; else if(c==="N")n++; else if(c==="A")a++; else other++; }
  return {y,n,a,total:Object.keys(v).length,other};
}
```

Detail panel shows: official yes/no/abstain; roll call y/n/a (total); note if differ: "The roll call count differs from the official totals for this record (gaps in the source); both are shown."

State claim data desc: if votes has iso: `roll call: ${name} (${iso}) voted ${codeLabel}` where codeLabel: Y="in favour (Y)", N="against (N)", A="abstained (A)". Verdict: claim code === actual → matches else wrong. NV: if votes[iso] exists → wrong ("the roll call records a vote for X"); else cannot be checked.

If country not in votes: cannot be checked, reason: "not among the ${total} recorded votes — this State was not a Council member at this vote or no vote is recorded for it."

Also if country name found but not in countries map at all (e.g., "Wakanda") — we only detect names from the map, so unknown states aren't detected. Should I detect unknown capitalized words followed by "voted"? That could catch "Atlantis voted in favour" → cannot be checked (not in data). Nice-to-have; adds complexity. The countries map has all UN member names presumably, so any real state is covered. Skip unknown detection.

Number claim verdict: 
```js
const official = {Y: rec.yes, N: rec.no, A: rec.abstain};
const roll = rollCall(rec);
if (official[kind] == null) verdict = cannot;
else if (claim == official[kind]) matches;
else if (roll differs && claim == roll[kind]) matches with note "matches the roll-call count (X), not the official total (Y)";
else wrong.
```

dataDesc: `official total: ${official[kind]}; roll call: ${roll[kind]} of ${roll.total} recorded votes`.

Date claim: parse to {y,m,d}; record date parse from rec.date "YYYY-MM-DD" (split "-"). If rec.date missing → cannot. Compare → matches/wrong. dataDesc: `recorded date: ${rec.date}`.

Year claim: compare to rec.year.

Session: record ordinal from rec.session; text ordinals list; each → claim. If none but /session/ in text → one cannot-be-checked row: quote the word "session" context. dataDesc: `recorded session: "${rec.session}"`.

Now the AI prompt: "send only the symbol and the title". Prompt:

```
You are writing a briefing for a human rights professional. Write about 250 words on the UN Human Rights Council document identified below, using only your own knowledge (you will not receive any additional data). Identify it by symbol and title only.

Symbol: ${rec.symbol}
Title: ${rec.title}

Write a neutral briefing of about 250 words: what the resolution is about, context, and the recorded vote if you know it. Do not ask questions. Reply strictly as JSON: {"briefing": "<the briefing text>"}.
```

Status message before call: `Sending 1 item to the model — the symbol and the title only (no data from this page). The request leaves your browser.` After: `Answer received from the model (${words} words) and placed in the text box. It is marked data-source="ai".` Render answer inside textarea with data-source="ai" attribute set on the textarea. Also maybe show it in a read-only div? The requirement: "Put the answer in a text box, where I can also paste a text of my own." So textarea. Set textarea.setAttribute("data-source","ai") when filled from AI; on user input, remove attribute and update meta label.

studio.ask may not exist → guard.

Stop button: sets cancelled flag; status "Stopped — the answer will be discarded when it arrives." When promise resolves and cancelled → status "Stopped by you; answer discarded." else fill.

Also disable ask button while waiting.

Check button: reads textarea value, runs extractClaims(text, rec), renders.

Now the select options: `${symbol} — ${title} (${year})` maybe truncated. Use textContent with symbol + short title. Option value = index.

On change: render detail, clear results? Keep briefing text (user may want to check same text against another resolution — actually that's useful; keep text, clear results and note "results cleared — press Check again"). I'll clear results.

Detail rendering with links: symbol linked to doc_url if non-empty else record_url; target _blank rel noopener. Also record_url link "search library record". Show kind, session, agenda item, date, sponsors, totals, roll call, proportional bar.

Proportional bar: div with three spans widths % of total (official). Label "in favour / against / abstaining (official totals)". Note how computed.

Header desc: `Source: ${HRC.title || "Human Rights Council recorded votes"} · ${records.length} recorded votes · years ${minYear}–${maxYear} · roll call of 47 Council members per vote.` Compute from data; handle empty.

Also mention vote_codes meaning: Y/N/A from HRC.vote_codes if present: `HRC.vote_codes` = {Y:..., N:..., A:...}? Description says vote_codes: {Y,N,A} — probably labels like "Yes"/"No"/"Abstain". I'll display if present: "Vote codes: Y = Yes, N = No, A = Abstain" built from the object values if strings.

Now CSS: 

```css
:root{--accent:#1f6fb2;}
*{box-sizing:border-box;}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:16px;line-height:1.5;background:#f4f6f9;color:#1c2733;}
header{background:#fff;border-bottom:1px solid #dde3ea;padding:20px 24px;}
h1{font-size:1.5rem;margin:0 0 6px;color:#123;}
...
main{max-width:1020px;margin:0 auto;padding:20px 24px 60px;}
.card{background:#fff;border:1px solid #dde3ea;border-radius:8px;padding:20px 24px;margin:20px 0;}
button{background:var(--accent);color:#fff;border:0;border-radius:6px;padding:10px 16px;font-size:16px;cursor:pointer;}
button.secondary{background:#fff;color:var(--accent);border:1px solid var(--accent);}
button:disabled{opacity:.6;cursor:default;}
select,textarea{width:100%;font:inherit;padding:8px;border:1px solid #c6cfd9;border-radius:6px;}
textarea{font-family:ui-monospace,...? } keep system but maybe slightly mono? Keep normal.
table{border-collapse:collapse;width:100%;margin-top:12px;}
th,td{border:1px solid #d7dee6;padding:8px 10px;text-align:left;vertical-align:top;}
th{background:#eef3f8;}
.verdict{font-weight:600;padding:2px 8px;border-radius:4px;white-space:nowrap;}
.v-match{background:#e3f3e8;color:#1a7f37;}
.v-wrong{background:#fbe7e5;color:#b3261e;}
.v-cannot{background:#eeeeee;color:#555;}
.note{background:#eef3f8;border-left:4px solid var(--accent);padding:8px 12px;border-radius:0 6px 6px 0;font-size:.95rem;}
.status{...}
.bar{display:flex;height:22px;border-radius:4px;overflow:hidden;margin:6px 0 2px;}
.bar span{display:block;height:100%;}
```

Bar colors: Y #1a7f37, N #b3261e, A #9aa4ae.

Now write extractClaims fully.

```js
function normMap(text){ ... as above, keep "-" and "–" as "-" ... }
```

Wait: keeping "-" means "cote d'ivoire" → apostrophe → space → "cote d ivoire" while hyphen kept. Country name "Côte d'Ivoire" normalized → "cote d ivoire". Text "Côte d'Ivoire" → same. Text "Cote d'Ivoire" → same. Good. But if text writes "Côte-d'Ivoire" → "cote-d-ivoire" ≠ "cote d ivoire". Edge case, ignore.

Also digits: keep. Everything else → " ". Also collapse multiple spaces? For indexOf-based name finding, multiple spaces fine as long as names normalized the same way (names normalized with same function → single spaces since names have single spaces). Text "cote  divoire" (double space) wouldn't match "cote d ivoire". Collapse spaces in norm but then map... collapsing breaks map alignment. Alternative: when searching names, use regex with \s+ between words: build pattern from name: name.split(" ").map(escapeRe).join("\\s+") — but name may contain "-" which we keep; escape it. And boundary: (?<![a-z0-9]) ... (?![a-z0-9]) — lookbehind; modern browsers OK (Chrome 62+, Safari 16.4+). Sandbox likely Chromium. I'll use lookbehind but with fallback? I'll just use lookarounds via manual check to be safe: match with /(^|[^a-z0-9])PATTERN([^a-z0-9]|$)/g and compute inner start = match.index + m[1].length. That avoids lookbehind. 

So findCountriesInRange: for each name, pattern = name.split(/\s+/).map(esc).join("[\\s\\-]+")? Hmm "-" kept in norm; name "cote d ivoire" has spaces. Join with "\\s+" fine. If name contains "-" (e.g., "Guinea-Bissau" → "guinea-bissau"), escape → "guinea\-bissau" matches literal "-". Text "Guinea Bissau" → "guinea bissau" wouldn't match "guinea-bissau". Add join flexibility: replace "-" in name with "[\\s\\-]+" too. So pattern = name.split(/[\s\-]+/).map(esc).join("[\\s\\-]+"). Good.

Then for each match, origStart = map[innerStart], origEnd = map[innerEnd-1]+1.

OK. Now phrase patterns on normText (lowercase). Since normText is lowercase, patterns lowercase without /i but I'll add /g only. Note \b works with [a-z0-9] boundaries.

One more: "in favour of" — pattern /\bin favour\b/ matches. "voted in favour" also matches "in favour" → duplicate claims for same country? "France voted in favour": patterns "voted in favour" (Y) and "in favour" (Y) both match; preceding clause for both contains "france" → two claims same iso+code → dedupe by iso+code keeps first. Good.

"against" bare pattern: "voted against" → "voted against" and "against" both → dedupe. But bare "against" also matches in "against the backdrop of..." with a country in preceding clause: "Unlike France, the resolution passed against..." — clause before "against" = "the resolution passed " no country. OK. Risk: "France, against expectations, voted in favour" — "against" match: clause before = "france, " → split on ","? My split set includes [.;:!?] and keywords, not comma. Add comma to split set? "France, against expectations, voted in favour" — for "in favour" match, clause = "france, against expectations, voted " → contains france → France Y correct. For "against" match, clause = "france, " → France N — WRONG claim extracted! Hmm. Add "," to clause split: then clause before "against" = " " (after comma) → no country → no claim. But "France and Kenya voted in favour" — clause before "in favour" = "france and kenya voted " — no comma, fine. "France, Kenya and Germany voted in favour" — clause = "kenya and germany voted " → France missed! Trade-off. Comma-splitting loses list-first items. Alternative: don't split on comma, but require the phrase to be "voted X" form for claims, and treat bare "in favour/against/abstained" only when directly preceded by country name within a few words? Hmm.

Let me reconsider: require patterns to include a verb-ish anchor: "voted in favour", "voted for", "voted yes", "voted against", "voted no", "abstained", "was in favour", "were in favour", "in favour of" preceded by name... The risky bare ones: "in favour", "against". Let me drop bare "in favour"/"against" and instead add patterns: /(?:was|were)\s+in\s+favour/, /(?:is|are)\s+in\s+favour/, and "in favour of" only when preceded by name? "countries in favour of the resolution included France" — names after. Ugh.

Pragmatic: keep patterns: voted in favour / voted favour / voted for / voted yes / in favour (bare) / voted against / voted no / against (bare) / abstained / abstention / did not vote. Accept the "France, against expectations" false positive risk — it's an edge case; and the checker would show "France voted against — wrong" which is actually a mis-extraction. To mitigate, split clause on commas too BUT also include the segment before the last comma if it contains a country name AND the phrase is a "voted" phrase? Getting complicated.

Alternative mitigation: for bare "against"/"in favour" (no "voted"), require the country name to be within 25 chars before the phrase and no comma between. For "voted X" phrases, allow up to 140 chars with comma splitting. Implement: for each phrase match, determine if pattern includes "voted"/"abstained"/"did not vote" (anchored) → clause = last segment after splitting on [.;:!?…] and keywords and commas? Hmm "France and Kenya voted in favour" — no comma, fine. "France, Kenya voted in favour" — comma split → "kenya voted " → France missed. Acceptable? Briefings usually write "France and Kenya voted in favour" or "France voted in favour, as did Kenya". "as did Kenya" — "did" not matched... "as did Kenya vote in favour"? rare.

I'll accept: split clause on /[.;:!?]/ and keywords (while/whereas/although/but/however/yet) and commas; take last piece; find countries. For anchored patterns ("voted ..."), also if last piece has no country, try the piece before the last comma? No — keep simple. Most natural sentences work.

Actually, one more common form: "It was adopted with 29 votes in favour, 16 against and 1 abstention, with France and Kenya voting in favour." — "voting in favour" — add pattern /\bvoting in favour\b/ and /\bvoting against\b/ and /\babstaining\b/. Add those.

Also "support"/"oppose": "France supported the resolution" → Y; "opposed" → N. Add: /\b(?:supported|supporting)\b/ → Y? "supported" could be "supported by France" (names after). Preceding clause approach: "France supported the resolution" → clause "france " → France Y. "The resolution, supported by France, passed" → clause before "supported" = "the resolution, " → comma split → "" → no claim. OK add supported→Y, opposed→N, /opposing/? skip. Add "voted with"? skip.

Fine. Dedupe by iso+code.

Now, also the numbers: "in favour" bare pattern for numbers: /(\d{1,3})\s+(?:votes?\s+)?in favour/ — on normText. "29 votes in favour" → "29 votes in favour" matches. "in favour: 29" → pattern /\bin favour\s*[:\-]?\s*(\d{1,3})/ — norm keeps ":" ? No! ":" → space in norm. Hmm, I said keep only "-" and letters/digits; ":" becomes space. So "in favour: 29" → "in favour 29" → pattern /\bin favour\s+(\d{1,3})/ matches. OK adjust patterns to norm conventions: punctuation (except -) is space. So write patterns accordingly: /\bin favour\s+(\d{1,3})\b/, /\byes\s+(\d{1,3})\b/ — but "yes 29"? "yes: 29" → "yes 29" matches. But "voted yes" → "yes" followed by... "france voted yes" → "yes" at end, no digits after → no match. Good. "no 16" — "no" bare dangerous: "no 16"? "there was no 16..." rare. But "no" appears in "no votes against"? "no votes against" → "no votes against" — pattern /\bno\s+(\d{1,3})/ needs digit right after "no" (with spaces) — "no votes" → "votes" not digit → no match. OK. But "No. 27" → "no 27" → matches as N=27! "General comment No. 27" in a briefing about... the briefing is about an HRC resolution; might mention "No. 27"? unlikely but "resolution 51/27" → "51 27" no "no". Hmm "No." → "no " + digits. Risk exists. Mitigate: require the number pattern for no/yes to be preceded by start or non-letter... "no 27" from "No. 27" — indistinguishable from "no: 27". Accept small risk; or drop the "yes/no colon" patterns and keep only "N votes in favour/against/abstain", "X votes to Y with Z", "X-Y-Z", "in favour N", "against N", "abstain N". I'll keep yes/no patterns but require the word to be preceded by a non-letter and the whole thing looks like a tally: /\b(?:yes|no|abstain\w*|in favour|against|for)\s+(\d{1,3})\b/ — "for 29"? "for" common: "for 29 years" → false. Drop "for N". Keep: yes, no, abstain*, in favour, against + N. And "N votes in favour" etc. And "by N votes to M". And "N-M-M". Good enough; document the patterns in the "how computed" note.

Also "unanimously": if /\bunanimously\b/ or /without a vote/ → claim: adopted without a vote → check official no==0 && abstain==0 && yes==total? "unanimously" → all Y: check roll.y == roll.total && roll.n==0 && roll.a==0 → matches else wrong. Add as number-type claim kind "unan". dataDesc: official totals + roll call. I'll include: if text has "unanimously" → claim "adopted unanimously"; verdict: matches if (rec.no==0 && rec.abstain==0) else wrong. "without a vote" → cannot be checked? If record has votes recorded, "without a vote" contradicts → wrong if any votes recorded... Actually "adopted without a vote" means no recorded vote; our data has a recorded vote → wrong. I'll treat "without a vote" as claim: matches if roll.total==0 else wrong. Minor; include.

Date patterns on normText: 
- ISO: /\b(\d{4})-(\d{1,2})-(\d{1,2})\b/g (hyphens kept).
- DMY: /\b(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]+)\s+(\d{4})\b/g with month lookup (first 3 letters).
- MDY: /\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})\b/g — but this could match "october 2023"? needs day digits: "october 13 2023" ok. Also "may 2025"? no day → no match (needs \d{1,2} then \d{4}; "may 2025" → month "may", then "2025" as day? \d{1,2} can't match "2025" (4 digits) — \b after? "2025" — \d{1,2} matches "20" then needs \s+(\d{4}) but next is "25" → fail; backtrack... "may 2025": after "may ", try day="20", then \s+ required but next char "2" → fail; day="2", next "0" not space → fail. Good, no match.
- Also "13th of October 2023": /\b(\d{1,2})(?:st|nd|rd|th)?\s+of\s+([a-z]+)\s+(\d{4})\b/ — add "of" optional in DMY: /\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)\s+(\d{4})\b/.

Month map: jan..dec → 1..12, also full names. Validate.

Year claims: /\b((?:19|20)\d{2})\b/g, skip if inside a date match span; only keep if within 40 chars of keyword /adopt|vote|resolution|passed|session|council/ ... hmm "council" too broad? "Human Rights Council in 2023" → year claim fine. Let me use keywords: adopt, vote, vot, resolution, passed, session, decision. Check window ±40 chars around the year in normText. If matched → year claim.

Session: /(\d{1,3})(?:st|nd|rd|th)\s+session/g and /session\s+(\d{1,3})\b/g. Also "its 51st session" covered by first. Also "the 51st session of the human rights council" covered. Collect ordinals; dedupe. If none and /\bsession\b/ present → cannot row. Record ordinal: from rec.session match /(\d+)/. If record.session missing → cannot.

Also compare: if text ordinal == record ordinal → matches; else wrong. dataDesc: `recorded session: "${rec.session}"`.

Now claims table columns: "Claim as written" (quote from original text, maybe with ellipsis), "What the recorded vote says", "Verdict". Also a "Type" maybe merged into claim. I'll add type label small.

Quote extraction: for each match on normText with index range [s,e), original span = map[s] .. map[e-1]+1. Quote = text.slice(origS, origE). For number patterns with capture group, quote whole match. Good.

Now assemble code. Also render "checking against" line with symbol link.

Let me also handle multiple records with same symbol? Use index as value.

Edge: records empty → show message in select area.

Let me now also compute header desc: years min/max from records' year field (filter numbers). n = records.length. Source: HRC.title. Also mention kinds count? Keep simple.

Write the final HTML now, carefully, aiming ~600 lines.

Also remember: before code block, ≤3 short sentences; after, nothing.

Let me write JS functions in order:

```js
(function(){
"use strict";
const DATA = window.WORKSHOP_DATA || {};
const HRC = DATA.hrc || {};
const records = Array.isArray(HRC.records) ? HRC.records : [];
const countries = (HRC.countries && typeof HRC.countries==="object") ? HRC.countries : {};
const voteCodes = HRC.vote_codes || {};

// normalization
function escRe(s){return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");}
function normChar(ch){ ... }
function normMap(text){
  let norm=""; const map=[];
  for(let i=0;i<text.length;i++){
    const ch=text[i];
    let e=ch.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
    if(/[a-z0-9]/.test(e)){
      for(const c of e){ if(/[a-z0-9]/.test(c)){norm+=c;map.push(i);} else if(c==="-"||c==="–"){norm+="-";map.push(i);} }
    } else if(ch==="-"||ch==="–"){ norm+="-"; map.push(i); }
    else { norm+=" "; map.push(i); }
  }
  return {norm,map};
}
```

Hmm "–" (en dash) → "-". Also if e contains other chars (like "’" → after NFD stays "’") → falls to else → space. But my loop: if e has letters, I iterate chars of e; non-alnum non-dash chars inside e (rare) → skipped, meaning no space inserted — could join words: "l’été" → "l" + "’"(skipped) + "été" → "lété". Minor. Let me handle: in the letter branch, for chars not alnum and not dash, push " ". Rewrite:

```js
for(const c of e){
  if(/[a-z0-9]/.test(c)){norm+=c;map.push(i);}
  else if(c==="-"||c==="–"){norm+="-";map.push(i);}
  else {norm+=" ";map.push(i);}
}
```
And if e === "" (char vanished, e.g., combining mark alone) → push space. Handle: if(e===""){norm+=" ";map.push(i);} else { loop }.

Country name patterns:

```js
const nameToIso = new Map();
const namePatterns = []; // {iso, name, re}
for(const [iso,name] of Object.entries(countries)){
  const n = normMap(String(name)).norm;
  if(!n) continue;
  if(!nameToIso.has(n)) nameToIso.set(n, iso);
  const pat = n.split(/[\s\-]+/).filter(Boolean).map(escRe).join("[\\s\\-]+");
  namePatterns.push({iso, name:String(name), re:new RegExp("(^|[^a-z0-9])("+pat+")([^a-z0-9]|$)","g")});
  // aliases
  const al = [];
  if(/united states/.test(n)) al.push("united states","us","usa");
  if(/russian federation/.test(n)) al.push("russia");
  if(/^the /.test(n)) al.push(n.replace(/^the ",""));
  for(const a of al){ if(!nameToIso.has(a)) nameToIso.set(a, iso); }
}
namePatterns.sort((a,b)=> b.name.length - a.name.length);
```

Wait: nameToIso keyed by normalized name; but findCountries uses regex per name pattern and then iso directly from pattern — I don't even need nameToIso except aliases. For alias "us": pattern for "us" would match "us" inside... boundary [^a-z0-9] prevents mid-word. "the US voted" → norm "the us voted" → "us" bounded by spaces → match. But "us" also in "let us vote"? "let us vote in favour" → "us" matched → iso USA claimed Y! False positive. Hmm. "us" alias risky. Drop "us"/"usa"? "the USA voted" → "usa" bounded → ok, keep "usa" but drop "us". Also "russia" alias fine. Also add "america"? "the America"? skip. Also "britain"/"uk" for United Kingdom? Add if /united kingdom/ → "uk","great britain","britain". And /bolivia/ skip. Also "south korea" vs "korea": if name "Republic of Korea" → norm "republic of korea" → alias "korea","south korea". Add: if(/korea/.test(n)) al.push("korea","south korea") — but "Democratic People's Republic of Korea" also contains korea → both map to different isos; alias "korea" ambiguous — skip korea aliases. Keep minimal: united states→"usa","united states"; russian federation→"russia"; united kingdom→"uk","britain"; ^the strip. Also "czech republic"/"czechia"? skip.

Also note: namePatterns regex with capture groups: m[2] is the name. innerStart = m.index + m[1].length; innerEnd = innerStart + m[2].length.

findCountries(norm, map, from, to): iterate patterns, use re.lastIndex=0, exec over slice? Easier: run on full norm but restrict matches with index+len within [from,to). Since patterns are global regexes, reset lastIndex each call.

```js
function findCountries(norm, map, from, to){
  const found=[];
  for(const p of namePatterns){
    p.re.lastIndex=0;
    let m;
    while((m=p.re.exec(norm))!==null){
      const s=m.index+m[1].length, e=s+m[2].length;
      if(s>=from && e<=to){
        found.push({iso:p.iso, name:p.name, s, e});
      }
      if(m[0].length===0) p.re.lastIndex++;
    }
  }
  // dedupe overlaps: sort by length desc, keep non-overlapping
  found.sort((a,b)=> (b.e-b.s)-(a.e-a.s) || a.s-b.s);
  const out=[];
  for(const f of found){
    if(!out.some(o=> !(f.e<=o.s || f.s>=o.e))) out.push(f);
  }
  return out;
}
```

Phrase patterns (on norm, lowercase):

```js
const PHRASES=[
 {re:/\bvoted in favour\b/g, code:"Y"},
 {re:/\bvoting in favour\b/g, code:"Y"},
 {re:/\bvoted for\b/g, code:"Y"},
 {re:/\bvoted yes\b/g, code:"Y"},
 {re:/\bin favour\b/g, code:"Y"},
 {re:/\bwas in favour\b/g, code:"Y"},
 {re:/\bwere in favour\b/g, code:"Y"},
 {re:/\bsupported\b/g, code:"Y"},
 {re:/\bvoted against\b/g, code:"N"},
 {re:/\bvoting against\b/g, code:"N"},
 {re:/\bvoted no\b/g, code:"N"},
 {re:/\bagainst\b/g, code:"N"},
 {re:/\bopposed\b/g, code:"N"},
 {re:/\babstained\b/g, code:"A"},
 {re:/\babstaining\b/g, code:"A"},
 {re:/\babstention\b/g, code:"A"},
 {re:/\bdid not vote\b/g, code:"NV"},
];
```

Hmm "supported" bare: "supported by France" — clause before "supported" is "the resolution " → no country. "France supported" → clause "france " → Y. OK. "against" bare risk as discussed; accept.

Wait, issue: "in favour" bare will also match inside "voted in favour" — dedupe by iso+code handles. But also "29 votes in favour" → clause "29 votes " no country. OK.

Another: "against" bare matches "voted against" too — dedupe.

But subtle: "France voted in favour, Germany against" — "against" match clause: split on comma → " germany " → Germany N. 

Clause splitting:

```js
function clauseBefore(norm, pos){
  const from=Math.max(0,pos-160);
  const seg=norm.slice(from,pos);
  const parts=seg.split(/(\s+(?:while|whereas|although|though|but|however|yet)\s+|[.;:!?]\s*|,)/);
  let last="";
  for(let i=parts.length-1;i>=0;i--){
    const p=parts[i];
    if(!p) continue;
    if(/^\s*(?:while|whereas|although|though|but|however|yet)\s*$/i.test(p)) continue;
    if(/^[.;:!?,]\s*$/.test(p)) continue;
    last=p; break;
  }
  if(!last) return {s:from,e:pos};
  const idx=seg.lastIndexOf(last);
  return {s:from+idx, e:pos};
}
```

Note split with capture group keeps separators as parts. Comma included → "France, against expectations" → parts: ["france", ",", " against expectations", ...] wait the split regex: comma alone matches "," → parts ["france", ",", " against expectations voted in favour"]. For "in favour" match, last non-sep part = " against expectations voted " → contains no country → no claim. For "against" match at "against expectations", clause = parts before: last non-sep = "france" → France N — false positive remains! Because "against" here is a preposition. Hmm. "against expectations" — pattern /\bagainst\b/ matches. To reduce: require for bare "against"/"in favour" (non-anchored) that the immediately preceding word(s) be a country name or "and"-list — i.e., clause length small? In "France voted against", anchored pattern "voted against" catches it; bare "against" also matches but dedupe. For "France, against expectations, voted in favour": anchored "voted in favour" gives France Y (clause "against expectations voted " — wait clause before "voted in favour" = "france, against expectations, " → split on comma → last part " against expectations " → no country → France missed!). Ugh.

OK let me think differently. Better approach for state claims: find country names first, then look AFTER each name for a vote phrase within a short window (e.g., 40 chars), skipping over list connectors ("and", ",", "along with", "as well as"). That's more natural: "France voted in favour" → name then phrase. "France and Kenya voted in favour" → for France, window after = " and kenya voted in favour" → contains "voted in favour" → France Y; for Kenya, window = " voted in favour" → Y. "France, against expectations, voted in favour" → window after France = ", against expectations, voted in favour" → first phrase found scanning left-to-right: "against" at offset ~2 → would assign N! Bad. But if I prioritize anchored patterns ("voted ...") over bare ones: scan window for anchored patterns first; if found, use it; else bare patterns. In the window ", against expectations, voted in favour": anchored "voted in favour" found → Y. Good. "France voted against" → anchored "voted against" → N. "France abstained" → anchored "abstained" → A. "France was in favour" → anchored? "was in favour" is in my list as anchored-ish; bare "in favour" also. Prioritize: anchored list = voted/voting/abstained/abstaining/did not vote/was in favour/were in favour/supported/opposed. Bare = in favour, against, abstention. In window after name, find earliest anchored match; if none, earliest bare match. Also stop window at sentence end (.;:!?) or clause keyword (while/whereas/but...) to avoid crossing into next clause: "France voted in favour. Germany voted against." — for France, window after name: " voted in favour. germany voted against." — must stop at "." → only "voted in favour". Implement: cut window at first occurrence of /[.;:!?]/ or /\s+(?:while|whereas|although|but|however|yet)\s+/.

Also handle "France and Germany voted in favour": France's window " and germany voted in favour" (cut at sentence end) → anchored "voted in favour" → Y. Germany's window " voted in favour" → Y. 

"France did not vote" → anchored "did not vote" → NV.

"France, along with Germany, abstained" → France window ", along with germany, abstained" → anchored "abstained" → A; Germany window ", abstained" → A. 

"16 countries voted in favour, including France" — France's window after name: "" (nothing after) → no claim for France. Missed claim, but acceptable (direction reversed). Could also look BEFORE name: "including France" — pattern "including X" → claim. Add: also scan window BEFORE name (up to 40 chars) for phrases like "including", "such as", "namely"? Skip — keep after-name only, plus maybe "X voted" is the dominant form. Fine.

So algorithm: for each country occurrence (from findCountries over whole text), take window = norm.slice(e, min(e+45, len)) cut at sentence/clause boundary; find anchored phrase match (earliest); else bare phrase; if found → claim {iso, code, quoteSpan: from name start to phrase end}. Dedupe by iso+code (keep first). Also if a country appears multiple times with different codes, both kept.

Also "voted in favour of the resolution" — window " voted in favour of the resolution" → anchored "voted in favour" → Y. Good.

Edge: "France voted in favour of the amendment, while Germany voted against" — France window cut at "while" → " voted in favour of the amendment, " → Y. Good.

Now numbers patterns on norm:

```js
function extractNumbers(norm, map, text){
  const claims=[]; // {kind, value, s, e}
  function add(kind, value, s, e){ claims.push({kind, value:parseInt(value,10), s, e}); }
  let m;
  const res=[
    {kind:"Y", re:/(\d{1,3})\s+(?:votes?\s+)?in favour\b/g},
    {kind:"Y", re:/(\d{1,3})\s+(?:votes?\s+)?for\b/g},
    {kind:"Y", re:/\bin favour\s+(\d{1,3})\b/g},
    {kind:"Y", re:/\byes\s+(\d{1,3})\b/g},
    {kind:"N", re:/(\d{1,3})\s+(?:votes?\s+)?against\b/g},
    {kind:"N", re:/\bagainst\s+(\d{1,3})\b/g},
    {kind:"N", re:/\bno\s+(\d{1,3})\b/g},
    {kind:"A", re:/(\d{1,3})\s+(?:votes?\s+)?abstain\w*/g},
    {kind:"A", re:/\babstain\w*\s+(\d{1,3})\b/g},
  ];
  for(const r of res){
    r.re.lastIndex=0;
    while((m=r.re.exec(norm))!==null){
      add(r.kind, m[1], m.index, m.index+m[0].length);
      if(m[0].length===0) r.re.lastIndex++;
    }
  }
  // "by X votes to Y, with Z abstentions"
  const reTo=/\b(\d{1,3})\s+votes?\s+to\s+(\d{1,3})(?:\s*,?\s*with\s+(\d{1,3})\s+abstain\w*)?/g;
  while((m=reTo.exec(norm))!==null){
    add("Y", m[1], m.index, m.index+m[0].length);
    add("N", m[2], m.index, m.index+m[0].length);
    if(m[3]) add("A", m[3], m.index, m.index+m[0].length);
  }
  // "29-16-1" style
  const reTri=/(^|[^\d\-])(\d{1,3})\s*\-\s*(\d{1,3})\s*\-\s*(\d{1,3})(?!\d)/g;
  while((m=reTri.exec(norm))!==null){
    const base=m.index+m[1].length;
    add("Y", m[2], base, base+m[0].length-m[1].length);
    add("N", m[3], base, base+m[0].length-m[1].length);
    add("A", m[4], base, base+m[0].length-m[1].length);
  }
  // dedupe by kind+value+approx position
  ...
}
```

Wait "for" pattern: "(\d+) for" — "for" as in "29 for"? "votes for"? "29 for, 16 against" — plausible tally style. But "for 29"? pattern is number-then-for: "29 for" ok. False positive: "room for 29"? "for 29" is number-after-for — not matched by this pattern (needs digit before "for"). "29 for" rare in prose except tallies. Keep.

"no (\d+)": "no 16" — from "no: 16" → norm "no 16". Also "No. 16" → "no 16" false positive. Accept, note in how-computed? Eh. Actually I can reduce: require "no" not preceded by... can't distinguish. Keep; risk low in briefings.

Dedupe numbers: key = kind+"|"+value+"|"+Math.round(s/5). Keep first.

Also "unanimously": if /\bunanimously\b/ test → claim kind "U". "without a vote": /\bwithout a vote\b/ → kind "W".

Dates:

```js
const MONTHS={jan:1,feb:2,mar:3,apr:4,may:5,jun:6,jul:7,aug:8,sep:9,oct:10,nov:11,dec:12};
function monthOf(w){ w=w.toLowerCase().slice(0,3); return MONTHS[w]||0; }
function extractDates(norm){
  const out=[]; let m;
  const reISO=/\b(\d{4})-(\d{1,2})-(\d{1,2})\b/g;
  while((m=reISO.exec(norm))!==null){ out.push({y:+m[1],mo:+m[2],d:+m[3],s:m.index,e:m.index+m[0].length}); }
  const reDMY=/\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)\s+(\d{4})\b/g;
  while((m=reDMY.exec(norm))!==null){ const mo=monthOf(m[2]); if(mo) out.push({y:+m[3],mo,d:+m[1],s:m.index,e:m.index+m[0].length}); }
  const reMDY=/\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})\b/g;
  while((m=reMDY.exec(norm))!==null){ const mo=monthOf(m[1]); if(mo && m[2]<=31) out.push({y:+m[3],mo,d:+m[2],s:m.index,e:m.index+m[0].length}); }
  return out;
}
```

Careful: reDMY could match inside ISO? "2023-10-13": reDMY needs digit then month letters — "2023-10-13" has no letters → no. reMDY on "october 13 2023" fine. Overlap between DMY and MDY? "13 october 2023" — MDY: month first — "13 october" no. OK. Also validate d 1..31, mo 1..12, y reasonable.

Year claims: after collecting date spans, scan /\b((?:19|20)\d{2})\b/g; skip if within any date span; keep if keyword within ±40 chars: /(adopt|vot|resolution|passed|session|decision|council)/. Hmm "council" — "Human Rights Council" appears often; "in 2023 the Council..." fine, it's about the resolution year anyway. But "since 2011 the Council has..." → year claim 2011 vs record.year → wrong verdict — misleading! The user asked to check "the date" of the resolution. A briefing mentioning other years would generate wrong verdicts. Restrict keyword window to ±30 chars and keywords: adopt, vot, pass, resolution, decision, session. "adopted in 2023" → "adopted in 2023": year within 30 chars after "adopt" → claim. "the Council has addressed this since 2011" → "council" not in keyword list now → no claim. Good. Also "on 13 October 2023" full date already covers. Also "2023 session"? "the 2023 session" → "session" keyword → claim. OK.

Session claims:

```js
function extractSessions(norm){
  const out=[]; let m;
  const re1=/(\d{1,3})(?:st|nd|rd|th)\s+session/g;
  while((m=re1.exec(norm))!==null) out.push({num:+m[1], s:m.index, e:m.index+m[0].length});
  const re2=/\bsession\s+(\d{1,3})\b/g;
  while((m=re2.exec(norm))!==null) out.push({num:+m[1], s:m.index, e:m.index+m[0].length});
  return out;
}
```

Dedupe by num.

Record session ordinal: (rec.session||"").match(/(\d+)/).

Now build claims list with verdicts:

```js
function checkText(text, rec){
  const {norm, map} = normMap(text);
  const claims=[];
  const roll = rollCall(rec);
  const official = {Y: rec.yes, N: rec.no, A: rec.abstain};
  const codeLabel = {Y:"in favour (Y)", N:"against (N)", A:"abstained (A)", NV:"did not vote"};
  const quote = (s,e)=> text.slice(map[s], map[Math.min(e-1, map.length-1)]+1);

  // numbers
  for(const c of extractNumbers(norm)){
    const k=c.kind;
    let verdict, data;
    if(k==="U"){ ... }
    ...
  }
  ...
}
```

Let me define per-claim object: {type, quote, claimText (human description like "29 in favour"), dataText, verdict, note}.

Number claim:
- claimText: `${value} ${label}` where label: Y→"in favour", N→"against", A→"abstaining".
- dataText: `Official totals: ${official.Y} in favour, ${official.N} against, ${official.A} abstaining. Roll call counted from the votes map: ${roll.y}/${roll.n}/${roll.a} of ${roll.total} recorded votes.`
- verdict: if official[k]==null → cannot ("this record has no official total for ..."). else if value===official[k] → matches. else if value===roll[k] && roll[k]!==official[k] → matches with note "matches the roll-call count, which differs from the official total for this record". else wrong.

U claim (unanimously): claimText "adopted unanimously"; dataText totals+roll; verdict: matches if official.N===0 && official.A===0 (and official.Y>0) else wrong. If official missing → cannot.
W claim (without a vote): matches if roll.total===0 else wrong; if no votes map → cannot.

Date claim: parse rec.date: const dm = /^(\d{4})-(\d{2})-(\d{2})/.exec(rec.date||""). If no → cannot. Compare y/mo/d. verdict matches/wrong. dataText: `Recorded date: ${rec.date}`. claimText: formatted date from text e.g. "13 October 2023" — reconstruct from quote or from parsed: `${d} ${monthName} ${y}`. Use quote as claim as written; claimText maybe same. I'll set claimText = quote.

Year claim: compare to rec.year. dataText `Recorded year: ${rec.year} (date ${rec.date})`.

Session claim: recOrd from rec.session. If !recOrd → cannot. If text num === recOrd → matches else wrong. dataText: `Recorded session: "${rec.session}"`. If no session numbers in text but /\bsession\b/ → one cannot claim: quote "session" word context (slice around). claimText: "mentions a session (no number given)". dataText: recorded session. verdict cannot, note "the text does not say which session, so there is nothing to compare".

State claim: iso, code. actual = (rec.votes||{})[iso]. dataText: if actual → `Roll call: ${name} (${iso}) = ${actual} (${codeLabel[actual]})` else `Not in the roll call: this vote records ${roll.total} votes; ${name} (${iso}) is not among them (not a Council member at this vote, or no vote recorded).` verdict: if actual==null → cannot; else if code==="NV" → actual? wrong : cannot... wait NV claim "did not vote": if actual exists → wrong ("the roll call records a vote"); if actual null → cannot (consistent with not-in-rollcall). else code===actual → matches else wrong.

claimText: `${name} ${phrase}` — use quote (original text span from name start to phrase end).

Now rendering results:

```js
function renderResults(claims, rec){
  if(!claims.length){ results.innerHTML = "<p>No checkable claims found...</p>"; return; }
  build table...
  summary counts.
}
```

Also always include the "cannot ≠ wrong" explanation box below table (static in HTML).

Also the "checking against" line: `Checking against <a href=...>symbol</a> — title`.

Now the detail panel render:

```js
function renderDetail(rec){
  const roll = rollCall(rec);
  const url = rec.doc_url || rec.record_url || "";
  ...
  html: symbol (link), kind, title, date, year, session, agenda item, sponsors, official totals, roll call, bar, note if differ.
}
```

Use DOM building or template strings with escaping. Text from data could contain HTML chars — escape! Write esc() function and use it for all data-derived strings. Important.

Bar: widths based on official totals (if total>0): y%, n%, a%. Colors. Label under: "in favour X · against Y · abstaining Z (official totals; bar widths proportional)".

Note: "How this is computed: official totals are the record's yes/no/abstain fields; the roll call is counted from the votes map (one entry per Council member). For a few records the two differ (gaps in the source); both are shown, and the checker compares claims mainly with the official totals."

Select options: for each record i: label = `${rec.symbol||"(no symbol)"} — ${rec.title||""} (${rec.year||"?"})`. Might be long; fine.

Initial selection: find index where symbol === "A/HRC/RES/51/27"; else 0.

AI ask:

```js
let cancelled=false;
askBtn.onclick = async ()=>{
  const rec = current();
  if(!rec) return;
  if(typeof studio==="undefined" || !studio.ask){ status("studio.ask is not available..."); return; }
  cancelled=false; askBtn.disabled=true; stopBtn.hidden=false;
  aiStatus.textContent = `Sending 1 item to the model: the symbol and the title only — no data from this page. This request leaves your browser. Waiting for the answer…`;
  const prompt = `Write a neutral briefing of about 250 words for a human rights professional about the UN Human Rights Council ${rec.kind||"document"} identified below, using only your own knowledge. You will receive no other data. Symbol: ${rec.symbol}. Title: ${rec.title}. Cover what it is about and, if you know it, the recorded vote. Do not ask questions. Reply strictly as JSON: {"briefing": "..."}`;
  try{
    const raw = await studio.ask(prompt, {json:true});
    if(cancelled){ aiStatus.textContent="Stopped by you — the model's answer was discarded."; return; }
    let briefing = raw;
    try{ const p=JSON.parse(raw); if(p && typeof p.briefing==="string") briefing=p.briefing; }catch(e){}
    briefing = String(briefing||"").trim();
    if(!briefing){ aiStatus.textContent="The model returned an empty answer."; return; }
    ta.value=briefing; ta.setAttribute("data-source","ai");
    briefingMeta.textContent = `AI answer from studio.ask (${wordCount(briefing)} words), marked data-source="ai". Edit it freely or paste your own text — editing removes the AI marker; nothing is sent anywhere unless you press the button again.`;
    aiStatus.textContent = `Answer received from the model (1 item was sent: symbol and title only).`;
  }catch(err){
    aiStatus.textContent = "The request to the model failed: "+err;
  } finally { askBtn.disabled=false; stopBtn.hidden=true; }
};
ta.addEventListener("input", ()=>{ ta.removeAttribute("data-source"); briefingMeta.textContent="Your own text (edited locally). Press Check to verify its claims."; });
stopBtn.onclick = ()=>{ cancelled=true; aiStatus.textContent="Stopping… the answer will be discarded when it arrives."; };
```

wordCount: split on whitespace.

Check button:

```js
checkBtn.onclick = ()=>{
  const rec=current(); const text=ta.value;
  results.innerHTML="";
  if(!rec){...}
  if(!text.trim()){ results.innerHTML="<p class='note'>The text box is empty — nothing to check. Ask the AI for a briefing or paste a text first.</p>"; return; }
  const claims = checkText(text, rec);
  renderResults(claims, rec);
};
```

renderResults: header line "Checking the text against {symbol link} — {title} ({kind}, {date})." Then table. Then summary. Then static explanation (already in HTML below).

Table row: 
```
<tr>
 <td><span class="ctype">in favour</span> “quote”</td>
 <td>dataText (+note)</td>
 <td><span class="verdict v-match">matches</span></td>
</tr>
```

Type labels: "Votes in favour", "Votes against", "Abstentions", "Unanimous", "Without a vote", "Date", "Year", "Session", "State vote".

Summary: `Found N checkable claims: X match · Y wrong · Z cannot be checked.`

Static legend (always visible under results area):
```
"Cannot be checked" means this dataset has no recorded value to compare the claim with — for example a State that is not among the recorded votes for this resolution, or a session mentioned without a number. It is not the same as "wrong": "wrong" means the recorded vote directly contradicts the claim.
```

How-computed note near table:
```
How this is computed: your text is scanned with fixed patterns — numbers before "in favour / against / abstain(…)", "X votes to Y with Z abstentions", "X-Y-Z" tallies, "unanimously"; dates (ISO, "13 October 2023", "October 13, 2023"); years near words like "adopted"/"resolution"; "Nth session"; and country names followed by a vote phrase ("voted in favour", "abstained", …). Each claim is compared only with the selected record: official totals (yes/no/abstain), the roll call counted from the votes map, the recorded date and session. All counting is done by this page, deterministically.
```

Now, also the top description: `Source: ${HRC.title} — ${records.length} recorded votes (resolutions and amendments), years ${min}–${max}. Vote codes: Y/N/A as defined in the data (${...}).` Build vote code text: Object.entries(voteCodes).map(([k,v])=>`${k} = ${v}`).join(", ") if present.

Handle empty records: if records.length===0 → show note "No recorded votes found in WORKSHOP_DATA.hrc." and disable controls.

Now write everything. Also ensure no horizontal scroll: table width 100%, word-wrap. textarea width 100%.

Let me write the final file mentally and count lines ~ fine.

One more detail: "Every row that shows a document has its symbol, linked to doc_url in a new tab." In results header line, include symbol link. In detail panel, symbol link. Good.

Also the select: when changed, re-render detail and clear results with a note.

Let me write code now.

Also careful: `studio` may be undefined — reference via `typeof studio!=="undefined"`.

Potential pitfall: template literals inside the HTML script containing `</script>`? No.

Escaping: esc = s => String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

Now, the checkText function full:

```js
function rollCall(rec){
  const v = (rec && rec.votes && typeof rec.votes==="object") ? rec.votes : {};
  let y=0,n=0,a=0,t=0;
  for(const k in v){ t++; const c=String(v[k]).toUpperCase(); if(c==="Y")y++; else if(c==="N")n++; else if(c==="A")a++; }
  return {y,n,a,total:t};
}

function checkText(text, rec){
  const {norm, map} = normMap(text);
  const quote=(s,e)=> text.slice(map[s], map[Math.min(e-1,map.length-1)]+1).trim();
  const claims=[];
  const roll=rollCall(rec);
  const off={Y:rec.yes,N:rec.no,A:rec.abstain};
  const codeLabel={Y:"in favour (Y)",N:"against (N)",A:"abstained (A)"};
  const kindLabel={Y:"votes in favour",N:"votes against",A:"abstentions"};

  // --- numbers ---
  const nums=extractNumbers(norm);
  const seen=new Set();
  for(const c of nums){
    const key=c.kind+"|"+c.value+"|"+Math.round(c.s/6);
    if(seen.has(key)) continue; seen.add(key);
    const q=quote(c.s,c.e);
    let verdict, note="";
    if(off[c.kind]==null || off[c.kind]===undefined){
      verdict="cannot";
      note="This record has no official total for this.";
    } else if(c.value===off[c.kind]){
      verdict="matches";
    } else if(c.value===roll[c.kind.toLowerCase()] && roll[c.kind.toLowerCase()]!==off[c.kind]){
      verdict="matches";
      note=`Matches the roll-call count (${roll[c.kind.toLowerCase()]}), which differs from the official total (${off[c.kind]}) for this record.`;
    } else {
      verdict="wrong";
    }
    claims.push({
      type:kindLabel[c.kind]||c.kind,
      quote:q,
      claim:`${c.value} ${c.kind==="Y"?"in favour":c.kind==="N"?"against":"abstaining"}`,
      data:`Official totals — in favour: ${off.Y}, against: ${off.N}, abstaining: ${off.A}. Roll call counted from the votes map: ${roll.y} in favour, ${roll.n} against, ${roll.a} abstaining (${roll.total} recorded votes).`,
      verdict, note
    });
  }
  // unanimous / without a vote
  ...
```

roll.y etc — rollCall returns {y,n,a,total}; map kind Y→y: use roll[c.kind==="Y"?"y":c.kind==="N"?"n":"a"].

Unanimous:

```js
  let mu = /\bunanimously\b/.exec(norm);
  if(mu){
    const q=quote(mu.index, mu.index+mu[0].length);
    let verdict;
    if(off.Y==null) verdict="cannot";
    else verdict = (off.N===0 && off.A===0) ? "matches" : "wrong";
    claims.push({type:"adoption", quote:q, claim:"adopted unanimously",
      data:`Official totals — in favour: ${off.Y}, against: ${off.N}, abstaining: ${off.A}; roll call: ${roll.y}/${roll.n}/${roll.a} of ${roll.total}.`,
      verdict, note: verdict==="matches" ? "No votes against and no abstentions are recorded." : "The record shows votes against and/or abstentions."});
  }
  let mw = /\bwithout a vote\b/.exec(norm);
  if(mw){ ... verdict: roll.total===0 ? "matches":"wrong"; if no votes map (roll.total===0 && !rec.votes) → cannot }
```

Hmm if rec.votes missing entirely, roll.total=0 → would say matches wrongly. Check: if(!rec.votes) verdict="cannot". OK.

Dates:

```js
  const dates=extractDates(norm);
  const dms=/^(\d{4})-(\d{1,2})-(\d{1,2})/.exec(String(rec.date||""));
  const seenD=new Set();
  for(const d of dates){
    const key=d.y+"-"+d.mo+"-"+d.d;
    if(seenD.has(key)) continue; seenD.add(key);
    const q=quote(d.s,d.e);
    let verdict;
    if(!dms) verdict="cannot";
    else verdict = (+dms[1]===d.y && +dms[2]===d.mo && +dms[3]===d.d) ? "matches" : "wrong";
    claims.push({type:"date", quote:q, claim:`date ${d.d}/${d.mo}/${d.y}`,
      data:`Recorded date: ${rec.date||"(none in this record)"}`,
      verdict, note: dms? "" : "This record has no date field."});
  }
```

Years:

```js
  const dateSpans=dates.map(d=>[d.s,d.e]);
  const reY=/\b((?:19|20)\d{2})\b/g; let my;
  const seenY=new Set();
  while((my=reY.exec(norm))!==null){
    const s=my.index, e=s+my[0].length;
    if(dateSpans.some(sp=> s>=sp[0]-1 && e<=sp[1]+1)) continue;
    const ctx=norm.slice(Math.max(0,s-40), Math.min(norm.length,e+40));
    if(!/(adopt|vot|resolution|passed|decision|session)/.test(ctx)) continue;
    const y=+my[1];
    if(seenY.has(y)) continue; seenY.add(y);
    const q=quote(s,e);
    let verdict;
    if(rec.year==null) verdict="cannot";
    else verdict = (y===rec.year)?"matches":"wrong";
    claims.push({type:"year", quote:q, claim:`year ${y}`,
      data:`Recorded year: ${rec.year!=null?rec.year:"(none)"} (date ${rec.date||"n/a"})`,
      verdict, note:""});
  }
```

Hmm ctx includes the year itself; "vot" matches "vote". "adopted in 2023" → ctx contains "adopt" → claim. Good. But also "resolution 51/27 was adopted in 2023" — the "2023" near "adopt" → claim. Also "in 2023" near "resolution" → claim. OK.

Wait: dateSpans check — ISO date "2023-10-13" in norm; reY would match "2023" inside it; span check excludes. But my span check: s>=sp[0]-1 && e<=sp[1]+1 — "2023" at start of "2023-10-13": s=sp[0], e=sp[0]+4, sp[1]=sp[0]+10 → e<=sp[1]+1 true, s>=sp[0]-1 true → excluded. Good. Also "13 october 2023": "2023" at end → excluded. Good.

Sessions:

```js
  const sess=extractSessions(norm);
  const recOrd=(String(rec.session||"").match(/(\d+)/)||[])[1];
  const seenS=new Set();
  for(const s of sess){
    if(seenS.has(s.num)) continue; seenS.add(s.num);
    const q=quote(s.s,s.e);
    let verdict;
    if(!recOrd) verdict="cannot";
    else verdict = (+recOrd===s.num)?"matches":"wrong";
    claims.push({type:"session", quote:q, claim:`session ${s.num}${ordinalSuffix(s.num)}`,
      data:`Recorded session: "${rec.session||"(none)"}"`,
      verdict, note: recOrd? "" : "This record has no session field."});
  }
  if(!sess.length && /\bsession\b/.test(norm)){
    const i=norm.indexOf("session");
    claims.push({type:"session", quote:quote(Math.max(0,i-20), i+8), claim:"mentions a session without a number",
      data:`Recorded session: "${rec.session||"(none)"}"`,
      verdict:"cannot", note:"The text does not say which session, so there is nothing to compare."});
  }
```

States:

```js
  const all=findCountries(norm, map, 0, norm.length);
  const seenC=new Set();
  for(const f of all){
    // window after name
    let wEnd=Math.min(norm.length, f.e+50);
    const wRaw=norm.slice(f.e, wEnd);
    const cut=wRaw.search(/[.;:!?]/);
    const cut2=wRaw.search(/\s+(?:while|whereas|although|though|but|however|yet)\s+/);
    let cutAt=wRaw.length;
    if(cut>=0) cutAt=Math.min(cutAt,cut);
    if(cut2>=0) cutAt=Math.min(cutAt,cut2);
    const win=norm.slice(f.e, f.e+cutAt);
    // anchored phrases first
    let code=null, phEnd=null;
    const anchored=[
      {re:/\bvoted in favour\b|\bvoting in favour\b|\bvoted for\b|\bvoted yes\b|\bwas in favour\b|\bwere in favour\b|\bsupported\b/g, code:"Y"},
      {re:/\bvoted against\b|\bvoting against\b|\bvoted no\b|\bopposed\b/g, code:"N"},
      {re:/\babstained\b|\babstaining\b/g, code:"A"},
      {re:/\bdid not vote\b/g, code:"NV"},
    ];
    const bare=[
      {re:/\bin favour\b/g, code:"Y"},
      {re:/\bagainst\b/g, code:"N"},
      {re:/\babstention\b/g, code:"A"},
    ];
    for(const grp of [anchored, bare]){
      let found=null;
      for(const p of grp){
        p.re.lastIndex=0;
        const mm=p.re.exec(win);
        if(mm && (!found || mm.index<found.index)) found={index:mm.index, end:mm.index+mm[0].length};
      }
      if(found){ 
        // determine code: need which pattern matched earliest
        ...
      }
    }
  }
```

Hmm, need code of earliest match. Restructure: collect all matches from all patterns in group with their code, pick min index:

```js
    function earliest(patterns, win){
      let best=null;
      for(const p of patterns){
        p.re.lastIndex=0;
        let mm;
        while((mm=p.re.exec(win))!==null){
          if(!best || mm.index<best.index) best={index:mm.index, end:mm.index+mm[0].length, code:p.code};
          if(mm[0].length===0) p.re.lastIndex++;
        }
      }
      return best;
    }
    let hit = earliest(anchored, win) || earliest(bare, win);
    if(hit){
      const key=f.iso+"|"+hit.code;
      if(!seenC.has(key)){
        seenC.add(key);
        const q=quote(f.s, f.e+hit.end);
        const votes=rec.votes||{};
        const actual=votes[f.iso];
        const name=countries[f.iso]||f.iso;
        let verdict, data, note="";
        if(actual==null){
          verdict="cannot";
          data=`Not in the roll call: this vote records ${roll.total} member votes; ${name} (${f.iso}) is not among them (not a Council member at this vote, or no vote recorded).`;
          note="Cannot be checked here — not the same as wrong.";
        } else {
          data=`Roll call: ${name} (${f.iso}) = ${actual} — ${codeLabel[actual]||actual}.`;
          if(hit.code==="NV"){ verdict = "wrong"; note="The roll call records an actual vote for this State."; }
          else verdict = (hit.code===String(actual).toUpperCase()) ? "matches" : "wrong";
        }
        claims.push({type:"State vote", quote:q, claim:`${name} ${hit.code==="Y"?"voted in favour":hit.code==="N"?"voted against":hit.code==="A"?"abstained":"said to have not voted"}`,
          data, verdict, note});
      }
    }
```

Wait — anchored "supported" in window: "France supported the resolution" → win " supported the resolution" → anchored Y. Good. But "France, which supported..." fine.

Issue: bare "against" in window: "France voted against" — anchored group has "voted against" → hit at index 6? win=" voted against" → anchored match "voted against" index 1 → code N. Good, bare not needed. "France was against" → anchored none ("was against" not in list) → bare "against" → N. OK.

Issue: "France voted in favour of X, Germany against" — France win cut at "," ? My cut regex includes [.;:!?] not comma. win = " voted in favour of x germany against" (50 chars) → anchored earliest = "voted in favour" → Y. Good. Germany win = " against" → bare → N. Good.

But "France and Germany voted in favour": France win = " and germany voted in favour" → anchored "voted in favour" → Y. Germany win = " voted in favour" → Y. Good.

Potential false: "France voted in favour; Germany abstained" — France win cut at ";" → " voted in favour" → Y. Good.

"France did not vote" → anchored NV. Good.

One more: the window is 50 chars — "France, along with Germany and Kenya, voted in favour" → France win: " along with germany and kenya voted in favour" (46 chars) → anchored "voted in favour" → Y. Good.

Now dedupe: seenC by iso+code — if text says "France voted in favour" twice, one row. If says France voted in favour AND against (contradiction), two rows. OK.

Also findCountries over whole text may find country names in unrelated sentences (e.g., "France proposed...") with no phrase after → no claim. Good.

Order claims: maybe sort by position in text. I'll collect with s position and sort by s at the end. Add s to each claim. Let me add `pos` field = start index in norm, sort ascending.

extractNumbers returns {kind,value,s,e}. Dates have s. etc. I'll add pos to each claim and sort.

renderResults:

```js
function renderResults(claims, rec){
  const url=rec.doc_url||rec.record_url||"";
  const sym=rec.symbol||"(no symbol)";
  const link=url?`<a href="${esc(url)}" target="_blank" rel="noopener">${esc(sym)}</a>`:esc(sym);
  let html=`<p>Checking the text against ${link} — ${esc(rec.title||"")} (${esc(rec.kind||"")}, ${esc(rec.date||"")}). ${claims.length} claim${claims.length===1?"":"s"} found.</p>`;
  if(claims.length){
    html+="<table><thead><tr><th>Claim as written</th><th>What the recorded vote says</th><th>Verdict</th></tr></thead><tbody>";
    for(const c of claims){
      const vClass = c.verdict==="matches"?"v-match":c.verdict==="wrong"?"v-wrong":"v-cannot";
      html+=`<tr><td><span class="ctype">${esc(c.type)}</span><br>“${esc(c.quote)}”<br><strong>${esc(c.claim)}</strong></td><td>${esc(c.data)}${c.note?`<br><em>${esc(c.note)}</em>`:""}</td><td><span class="verdict ${vClass}">${c.verdict}</span></td></tr>`;
    }
    html+="</tbody></table>";
    const m=claims.filter(c=>c.verdict==="matches").length;
    const w=claims.filter(c=>c.verdict==="wrong").length;
    const u=claims.filter(c=>c.verdict==="cannot").length;
    html+=`<p class="summary"><strong>${claims.length} claims checked:</strong> ${m} match · ${w} wrong · ${u} cannot be checked.</p>`;
  }
  results.innerHTML=html;
}
```

ctype style: small uppercase grey.

Now detail panel:

```js
function renderDetail(rec){
  const roll=rollCall(rec);
  const url=rec.doc_url||"";
  const recUrl=rec.record_url||"";
  const sym=rec.symbol||"(no symbol)";
  const symLink=url?`<a href="${esc(url)}" target="_blank" rel="noopener">${esc(sym)}</a>`:(recUrl?`<a href="${esc(recUrl)}" target="_blank" rel="noopener">${esc(sym)}</a>`:esc(sym));
  const sponsors=(Array.isArray(rec.main_sponsors)?rec.main_sponsors:[]).filter(Boolean);
  const tot=(off.Y||0)+(off.N||0)+(off.A||0);
  let bar="";
  if(tot>0){
    bar=`<div class="bar" title="official totals"><span style="width:${off.Y/tot*100}%;background:#1a7f37"></span><span style="width:${off.N/tot*100}%;background:#b3261e"></span><span style="width:${off.A/tot*100}%;background:#9aa4ae"></span></div>
    <p class="barlabel">in favour ${off.Y} · against ${off.N} · abstaining ${off.A} (official totals; bar widths proportional)</p>`;
  }
  const differ = (roll.y!==off.Y)||(roll.n!==off.N)||(roll.a!==off.A);
  detail.innerHTML=`
    <h3>${symLink} <span class="kindtag">${esc(rec.kind||"")}</span></h3>
    <p class="rtitle">${esc(rec.title||"")}</p>
    <dl class="facts">
      <div><dt>Date</dt><dd>${esc(rec.date||"")}</dd></div>
      <div><dt>Session</dt><dd>${esc(rec.session||"")}</dd></div>
      <div><dt>Agenda item</dt><dd>${esc(rec.agenda_item||"")}</dd></div>
      <div><dt>Main sponsors</dt><dd>${sponsors.length?esc(sponsors.join("; ")):"(none listed)"}</dd></div>
      <div><dt>Official totals</dt><dd>in favour ${off.Y} · against ${off.N} · abstaining ${off.A}</dd></div>
      <div><dt>Roll call (counted from the votes map)</dt><dd>${roll.y} in favour · ${roll.n} against · ${roll.a} abstaining — ${roll.total} recorded member votes</dd></div>
      <div><dt>Links</dt><dd>${url?`<a href="${esc(url)}" target="_blank" rel="noopener">UN document (${esc(sym)})</a>`:""}${url&&recUrl?" · ":""}${recUrl?`<a href="${esc(recUrl)}" target="_blank" rel="noopener">search library record</a>`:""}</dd></div>
    </dl>
    ${bar}
    ${differ?`<p class="warn">The roll-call count differs from the official totals for this record (gaps in the source). Both are shown; the checker compares claims with the official totals first and notes when a claim matches the roll call instead.</p>`:""}
    <p class="note">How this is computed: official totals are the record's yes/no/abstain fields; the roll call is counted by this page from the votes map (one entry per Council member, codes ${voteCodeText}).</p>`;
}
```

voteCodeText from HRC.vote_codes: e.g. "Y = Yes, N = No, A = Abstain" — build: Object.entries(voteCodes).map(([k,v])=>`${k} = ${v}`).join(", ") or fallback "Y/N/A".

Header desc:

```js
const years=records.map(r=>r.year).filter(y=>typeof y==="number");
const minY=years.length?Math.min(...years):null, maxY=years.length?Math.max(...years):null;
desc.textContent = `Source: ${HRC.title||"Human Rights Council recorded votes"} · ${records.length} recorded votes (resolutions and amendments) · years ${minY!=null?minY+"–"+maxY:"n/a"} · each vote records the roll call of the Council's members (codes ${voteCodeText}).`;
```

Select population:

```js
records.forEach((r,i)=>{
  const o=document.createElement("option");
  o.value=i;
  o.textContent=`${r.symbol||"(no symbol)"} — ${r.title||"(untitled)"} (${r.year||"?"})`;
  sel.appendChild(o);
});
const startIdx=records.findIndex(r=>r.symbol==="A/HRC/RES/51/27");
sel.value = startIdx>=0?startIdx:0;
```

On change: renderDetail(records[+sel.value]); results.innerHTML=""; maybe keep briefing.

Now CSS details for facts dl: grid two columns.

Also add "How this is computed" near the check section (static note) and near AI section explaining what's sent.

Also the AI section note: "Only the symbol and the title of the selected resolution are sent to the model — none of the data on this page. The request leaves your browser; the answer is shown in the text box marked data-source="ai"."

Let me now also double check normMap handles uppercase: ch.toLowerCase() first — yes.

escRe for name patterns: names normalized contain only [a-z0-9 -]; esc fine.

One concern: findCountries patterns use "(^|[^a-z0-9])(pat)([^a-z0-9]|$)" with /g — overlapping matches: since pattern consumes boundary chars, consecutive names "france and kenya" — "france" match consumes trailing space; next exec starts after, "and kenya" — "kenya" preceded by space which was consumed? The match for "france" is " france " (with boundaries) ending after the space; next search starts at "and kenya..." — "kenya" needs preceding [^a-z0-9] — the space before "kenya" is at position within "and kenya", available since "and" wasn't consumed. Actually match " france " spans indices [i, i+7) where i is the space before f... hmm m.index is start of m[0] which includes m[1] (the boundary char). So m[0]=" france " consumes the space before AND after. Next exec from index after that — "and kenya voted" — "kenya" preceded by space (between "and" and "kenya") which is still available → matches. Good. But "france,kenya"? norm "france kenya" (comma→space) → "france " consumed incl trailing space, then "kenya" at start: needs (^|[^a-z0-9]) — ^ won't match mid-string; preceding char is the consumed space... exec continues from lastIndex = end of previous match = position after the space, i.e., at "k". Then m[1] must match [^a-z0-9] at "k" — fails; regex engine advances: tries at "e"... no match for "kenya" because boundary char before it was consumed. Classic overlapping issue. Fix: use lookahead for the trailing boundary instead: "(^|[^a-z0-9])(pat)(?![a-z09])" — but lookbehind for leading... leading boundary consumed is fine only if it's the leading one; the problem is trailing space consumed blocks next match's leading boundary. Use lookahead for trailing: pattern "(^|[^a-z0-9])("+pat+")(?![a-z0-9])" — trailing char not consumed → next match can use it as leading boundary. And leading boundary consumed is OK because previous match's trailing lookahead didn't consume it... wait if previous match ended with lookahead at position of space, lastIndex = position of space (end of m[0] = end of name, since lookahead is zero-width). Then next match attempt at space: m[1] matches space, then name. 

So: new RegExp("(^|[^a-z0-9])("+pat+")(?![a-z0-9])","g"). m[2] is name, innerStart = m.index + m[1].length. Good. Avoid lookbehind entirely. 

Similarly for phrase patterns using \b — fine.

Also in findCountries I restrict s>=from && e<=to — with the new regex, s = m.index+m[1].length, e = s+m[2].length.

Now extractNumbers dedupe: key kind|value|round(s/6) — two different patterns matching same spot produce same s roughly. OK.

Also note: pattern /(\d{1,3})\s+(?:votes?\s+)?for\b/ — "29 for" — but also "for" in "29 for the resolution"? fine. False: "back for 29"? number before for required. "2029 for"? \d{1,3} with \b? "2029" — (\d{1,3}) could match "202" then "9" not \s → backtrack to "20"? then "2" ... hmm "2029 for": regex tries at "2": \d{1,3} greedy "202", then \s+ needs whitespace but next is "9" → fail; backtrack "20", next "2" fail; "2", next "0" fail. Move to index1: "029 for" → "029" then " " then "for" → match! value 29 from year 2029. Guard: add (?<!\d) — lookbehind... or use /(^|[^\d])(\d{1,3})\s+.../ with capture offset. Let me add boundary via capture: replace patterns with /(^|[^\d])(\d{1,3})\s+(?:votes?\s+)?in favour\b/g and value=m[2], s=m.index+m[1].length. Similarly for others. And trailing: "29 in favour" fine; "291 in favour"? \d{1,3} greedy "291" → value 291 — official max 47, verdict wrong; but "291" unlikely. Add (?!\d) trailing lookahead — safe (lookahead fine). So patterns: /(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?in favour\b/g etc.

For "in favour 29": /\bin favour\s+(\d{1,3})(?!\d)/g — "in favour 2029"? (?!\d) after \d{1,3} greedy "202" then next "9" is digit → fail; backtrack "20" next "2" digit fail; "2" next "0" fail → no match at that position... then engine tries other positions — no other "in favour". Good, "in favour 2029" won't match — acceptable.

reTo: /\b(\d{1,3})(?!\d)\s+votes?\s+to\s+(\d{1,3})(?!\d)/g — "by 29 votes to 16" — also matches "29 votes to 16" without "by". fine.

reTri: /(^|[^\d\-])(\d{1,3})(?!\d)\s*\-\s*(\d{1,3})(?!\d)\s*\-\s*(\d{1,3})(?!\d)/g — "2023-10-13": at index0: m[1]="" (^), \d{1,3} greedy "202", (?!\d) next "3" digit → fail; backtrack "20" next "2" fail; "2" next "0" fail. index1: m[1] must be [^\d\-] — "0" is digit → fail... all inner positions fail since preceded by digit. index of "-"? m[1]="-" not allowed ([^\d\-] excludes -). So no match in dates. "29-16-1": index0 ^, "29", (?!\d) next "-" ok, \s*\-\s* matches "-", "16", "-", "1", (?!\d) end → match. 

But wait: "res 51 27" no. "a hrc res 51 27" fine. What about "51/27" → "51 27" no dash. OK.

Also hyphen in norm: I map both "-" and "–" to "-". Good.

Now extractDates reISO: /\b(\d{4})-(\d{1,2})-(\d{1,2})\b/g — \b before (\d{4}): in "x2023-10-13"? \b between x and 2? "x2023" — x is word char, 2 is word char → no boundary → won't match mid-word. Good.

reDMY: /\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)\s+(\d{4})\b/g — "13 october 2023" ✓. Could falsely match "16 against 2023"? "against" is [a-z]+ but monthOf("against")=0 → skipped. Good. "1 abstention 2023"? monthOf("abstention")=0 skip. Good.

reMDY: /\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})\b/g — "october 13 2023" ✓. False: "session 51 2023"? monthOf("session")=0 skip. Good.

Validate d<=31, mo 1..12.

Also "on 13 October 2023," trailing comma → norm space, fine.

Now session re1: /(\d{1,3})(?:st|nd|rd|th)\s+session/g — "51st session" ✓. Also "the 51st regular session" ✓ (matches "51st ... session"? "51st regular session" — pattern requires ordinal immediately followed by \s+session — "51st regular session" has "regular" between → no match! Add optional words: /(\d{1,3})(?:st|nd|rd|th)\s+(?:\w+\s+){0,2}?session/g — hmm greedy issues. Use /(\d{1,3})(?:st|nd|rd|th)\s+(?:[a-z]+\s+){0,3}?session/g. "51st session" → zero words ✓. "51st regular session" → one word ✓. OK.

Also record.session "Human Rights Council at its 54th session" → ordinal 54 via /(\d+)/ first match — "54th" → 54 ✓. But "Human Rights Council at its 54th session" — first \d+ is 54 ✓.

Now the "How this is computed" static note under check section — include pattern list.

Also initial state: results area shows a hint "Press Check after writing/pasting a briefing."

Also add small print: "All counting, filtering and matching on this page is done deterministically in your browser; nothing is estimated."

Now assemble final HTML. Also ensure the textarea has aria-label. Buttons type="button".

Let me also handle `current()` = records[+sel.value].

Edge: records empty → sel disabled, detail shows message, buttons disabled.

Write it.

Also: the AI answer element must have data-source="ai" — textarea gets it. Also maybe wrap status. Fine.

Line count: let's write compactly but readable. Probably ~550 lines. OK.

One more consideration: `studio.ask` prompt — "send only the symbol and the title, none of our data". My prompt includes kind ("resolution") — kind is data... The user said send only symbol and title. I'll phrase prompt using only symbol and title; I can say "UN Human Rights Council document" without kind. Keep strictly symbol+title. Prompt:

`You are helping a human rights professional. Using only your own knowledge, write a neutral briefing of about 250 words about the following UN Human Rights Council document. You will be given only its symbol and title — no other data. Do not ask questions and do not request more information.

Symbol: ${rec.symbol}
Title: ${rec.title}

The briefing should say what the document is about and, if you know it, how the Council voted on it. Reply strictly as JSON: {"briefing": "<briefing text>"} — no other keys.`

Good — only symbol and title embedded.

Status text: "Sending 1 item to the model — the symbol and the title only; no data from this page is included. The request leaves your browser."

Now write the whole document.

CSS: keep clean. Let me write:

```css
:root{--accent:#1f6fb2;--ink:#1c2733;--line:#d9e1ea;--bg:#f4f6f9;}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:16px;line-height:1.55;color:var(--ink);background:var(--bg)}
header{background:#fff;border-bottom:1px solid var(--line);padding:22px 28px}
header h1{margin:0 0 6px;font-size:1.45rem;color:#10314f}
header p{margin:0;max-width:60rem;color:#3d4c5c}
main{max-width:1040px;margin:0 auto;padding:8px 28px 64px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px 24px;margin:22px 0}
.card h2{margin:0 0 10px;font-size:1.15rem;color:#10314f}
label{display:block;font-weight:600;margin:12px 0 6px}
select,textarea{width:100%;font:inherit;color:var(--ink);padding:9px 10px;border:1px solid #c3cedb;border-radius:6px;background:#fff}
textarea{min-height:180px;line-height:1.5}
button{font:inherit;font-weight:600;background:var(--accent);color:#fff;border:0;border-radius:6px;padding:10px 18px;cursor:pointer;margin-right:8px}
button.ghost{background:#fff;color:var(--accent);border:1px solid var(--accent)}
button:disabled{opacity:.55;cursor:default}
.note{background:#eaf2fa;border-left:4px solid var(--accent);padding:9px 12px;border-radius:0 6px 6px 0;margin:12px 0;font-size:.95rem}
.warn{background:#fdf3e7;border-left:4px solid #c77700;padding:9px 12px;border-radius:0 6px 6px 0;margin:12px 0;font-size:.95rem}
.status{min-height:1.4em;font-weight:600;color:#10314f;margin:10px 0}
.meta{font-size:.92rem;color:#4a5a6a;margin:6px 0}
table{border-collapse:collapse;width:100%;margin-top:14px;font-size:.95rem}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:#eef3f9}
td{overflow-wrap:anywhere}
.ctype{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#5a6b7c;background:#eef1f5;border-radius:4px;padding:1px 6px;margin-bottom:4px}
.verdict{display:inline-block;font-weight:700;padding:3px 10px;border-radius:5px;white-space:nowrap}
.v-match{background:#e2f3e7;color:#177a3d}
.v-wrong{background:#fbe6e4;color:#b3261e}
.v-cannot{background:#eceff2;color:#5b6770}
.summary{font-size:1.02rem;margin-top:14px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px 22px;margin:12px 0}
.facts dt{font-weight:700;font-size:.85rem;color:#5a6b7c;text-transform:uppercase;letter-spacing:.03em}
.facts dd{margin:2px 0 0}
.rtitle{font-size:1.05rem;font-weight:600;margin:4px 0 10px}
h3{margin:0 0 4px;font-size:1.1rem}
.kindtag{font-size:.8rem;font-weight:600;background:#eef1f5;border-radius:4px;padding:2px 8px;color:#41505f;vertical-align:middle}
.bar{display:flex;height:20px;border-radius:5px;overflow:hidden;margin:10px 0 4px;max-width:520px}
.bar span{display:block;height:100%}
.barlabel{font-size:.9rem;color:#4a5a6a;margin:0 0 8px}
a{color:var(--accent)}
```

OK. Now write the full document. Also add `<meta name="viewport">`.

Double-check: no external resources. Chart.js not needed (no charts) — that's fine ("Use it for charts" — only if charts).

Write final answer: 2-3 sentences before code block, then the html block, nothing after.

Let me write out the JS completely and carefully to avoid bugs.

Full script:

```js
(function(){
"use strict";
var DATA = window.WORKSHOP_DATA || {};
var HRC = DATA.hrc || {};
var records = Array.isArray(HRC.records) ? HRC.records : [];
var countries = (HRC.countries && typeof HRC.countries === "object") ? HRC.countries : {};
var voteCodes = (HRC.vote_codes && typeof HRC.vote_codes === "object") ? HRC.vote_codes : {};

function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }
function escRe(s){ return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

var voteCodeText = Object.keys(voteCodes).length
  ? Object.keys(voteCodes).map(function(k){ return k + " = " + voteCodes[k]; }).join(", ")
  : "Y / N / A";

// ---------- text normalization (keeps a map back to original indices) ----------
function normMap(text){
  var norm="", map=[], i, ch, e, j, c;
  for(i=0;i<text.length;i++){
    ch=text[i];
    e=ch.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"");
    if(e===""){ norm+=" "; map.push(i); continue; }
    for(j=0;j<e.length;j++){
      c=e[j];
      if(/[a-z0-9]/.test(c)){ norm+=c; map.push(i); }
      else if(c==="-"||c==="\u2013"||c==="\u2014"){ norm+="-"; map.push(i); }
      else { norm+=" "; map.push(i); }
    }
  }
  return {norm:norm, map:map};
}
```

Wait: ch.toLowerCase() of "–" is "–"; NFD keeps it; my check c==="–" handles. But I lowercase first then NFD — fine.

Country patterns:

```js
var namePatterns=[];
(function(){
  var seen={};
  Object.keys(countries).forEach(function(iso){
    var name=String(countries[iso]||"");
    var n=normMap(name).norm;
    if(!n) return;
    var pat=n.split(/[\s\-]+/).filter(Boolean).map(escRe).join("[\\s\\-]+");
    namePatterns.push({iso:iso, name:name, re:new RegExp("(^|[^a-z0-9])("+pat+")(?![a-z0-9])","g")});
    var aliases=[];
    if(/united states/.test(n)) aliases.push("usa","united states");
    if(/russian federation/.test(n)) aliases.push("russia");
    if(/united kingdom/.test(n)) aliases.push("uk","britain");
    if(/^the /.test(n)) aliases.push(n.replace(/^the ",""));
    aliases.forEach(function(a){
      if(!seen[a]){ seen[a]=1; var ap=a.split(/[\s\-]+/).filter(Boolean).map(escRe).join("[\\s\\-]+");
        namePatterns.push({iso:iso, name:"alias:"+a, re:new RegExp("(^|[^a-z0-9])("+ap+")(?![a-z0-9])","g")}); }
    });
  });
  namePatterns.sort(function(a,b){ return b.name.length-a.name.length; });
})();
```

Hmm alias "usa" — "the USA voted" → "usa" bounded ✓. "us" dropped. OK.

findCountries:

```js
function findCountries(norm, from, to){
  var found=[], i, p, m, s, e;
  for(i=0;i<namePatterns.length;i++){
    p=namePatterns[i]; p.re.lastIndex=0;
    while((m=p.re.exec(norm))!==null){
      s=m.index+m[1].length; e=s+m[2].length;
      if(s>=from && e<=to) found.push({iso:p.iso, name:p.name, s:s, e:e});
      if(m[0].length===0) p.re.lastIndex++;
    }
  }
  found.sort(function(a,b){ return (b.e-b.s)-(a.e-a.s) || a.s-b.s; });
  var out=[];
  for(i=0;i<found.length;i++){
    var f=found[i], overlap=false, j;
    for(j=0;j<out.length;j++){ if(!(f.e<=out[j].s || f.s>=out[j].e)){ overlap=true; break; } }
    if(!overlap) out.push(f);
  }
  return out;
}
```

rollCall, extractNumbers, extractDates, extractSessions as planned.

checkText: assemble with pos for sorting.

Let me write extractNumbers concretely:

```js
function extractNumbers(norm){
  var out=[], m;
  var pats=[
    {kind:"Y", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?in favour\b/g},
    {kind:"Y", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?for\b/g},
    {kind:"Y", re:/\bin favour\s+(\d{1,3})(?!\d)/g},
    {kind:"Y", re:/\byes\s+(\d{1,3})(?!\d)/g},
    {kind:"N", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?against\b/g},
    {kind:"N", re:/\bagainst\s+(\d{1,3})(?!\d)/g},
    {kind:"N", re:/\bno\s+(\d{1,3})(?!\d)/g},
    {kind:"A", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?abstain\w*/g},
    {kind:"A", re:/\babstain\w*\s+(\d{1,3})(?!\d)/g}
  ];
  pats.forEach(function(p){
    p.re.lastIndex=0;
    while((m=p.re.exec(norm))!==null){
      var s = m.index + (m[1]?m[1].length:0);
      var val = m[1] && /^\d/.test(m[1]) ? m[2] : m[1]; // hmm
      ...
    }
  });
}
```

Careful with capture groups: for patterns with leading boundary group, m[1] is boundary, m[2] is number. For patterns without, m[1] is number. Unify: make ALL patterns have leading boundary group: e.g. /\bin favour\s+(\d{1,3})(?!\d)/ → change to /(^|[^\w])in favour.../ messy. Simpler: give every pattern exactly two groups where group 2 is the number: prefix each with "(^|[^\\d])"? For "in favour 29": /(^|[^\d])in favour\s+(\d{1,3})(?!\d)/g — boundary before "in" — preceded by digit? unlikely; fine, harmless. So all patterns: /(^|[^\d])...(\d{1,3})(?!\d).../ with number in m[2], start s=m.index+m[1].length.

Rewrite:

```js
var pats=[
  {kind:"Y", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?in favour\b/g},
  {kind:"Y", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?for\b/g},
  {kind:"Y", re:/(^|[^\d])in favour\s+(\d{1,3})(?!\d)/g},
  {kind:"Y", re:/(^|[^\d])yes\s+(\d{1,3})(?!\d)/g},
  {kind:"N", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?against\b/g},
  {kind:"N", re:/(^|[^\d])against\s+(\d{1,3})(?!\d)/g},
  {kind:"N", re:/(^|[^\d])no\s+(\d{1,3})(?!\d)/g},
  {kind:"A", re:/(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?abstain\w*/g},
  {kind:"A", re:/(^|[^\d])abstain\w*\s+(\d{1,3})(?!\d)/g}
];
```

Wait "in favour 29": boundary (^|[^\d]) before "in" — if preceded by digit? "29 in favour 29"? weird. fine.

Hmm but "no 16": boundary before "no" — "no" preceded by space ✓. "No. 16" → norm "no 16" → matches (false positive risk accepted).

Also "for" pattern: "29 for" — boundary ok.

Then:

```js
pats.forEach(function(p){
  p.re.lastIndex=0;
  while((m=p.re.exec(norm))!==null){
    out.push({kind:p.kind, value:parseInt(m[2],10), s:m.index+m[1].length, e:m.index+m[0].length});
    if(m[0].length===0) p.re.lastIndex++;
  }
});
// "X votes to Y, with Z abstentions"
var reTo=/(^|[^\d])(\d{1,3})(?!\d)\s+votes?\s+to\s+(\d{1,3})(?!\d)(?:\s*,?\s*with\s+(\d{1,3})(?!\d)\s+abstain\w*)?/g;
while((m=reTo.exec(norm))!==null){
  var base=m.index+m[1].length;
  out.push({kind:"Y", value:+m[2], s:base, e:m.index+m[0].length});
  out.push({kind:"N", value:+m[3], s:base, e:m.index+m[0].length});
  if(m[4]) out.push({kind:"A", value:+m[4], s:base, e:m.index+m[0].length});
}
// "29-16-1"
var reTri=/(^|[^\d\-])(\d{1,3})(?!\d)\s*\-\s*(\d{1,3})(?!\d)\s*\-\s*(\d{1,3})(?!\d)/g;
while((m=reTri.exec(norm))!==null){
  var b2=m.index+m[1].length;
  out.push({kind:"Y", value:+m[2], s:b2, e:m.index+m[0].length});
  out.push({kind:"N", value:+m[3], s:b2, e:m.index+m[0].length});
  out.push({kind:"A", value:+m[4], s:b2, e:m.index+m[0].length});
}
return out;
```

Note: reTo also matches inside reTri? "29-16-1" — reTo needs "votes to" — no. OK. But "29 votes to 16" also matched by...? "29 votes" — pattern "(\d+) (votes )?in favour" no. fine. Dedupe later.

Also note "with 1 abstention" after "16 against": pattern A "(\d+) abstain" matches "1 abstention" ✓.

extractDates:

```js
var MONTHS={jan:1,feb:2,mar:3,apr:4,may:5,jun:6,jul:7,aug:8,sep:9,oct:10,nov:11,dec:12};
function monthOf(w){ return MONTHS[String(w).toLowerCase().slice(0,3)]||0; }
function extractDates(norm){
  var out=[], m;
  var reISO=/\b(\d{4})-(\d{1,2})-(\d{1,2})\b/g;
  while((m=reISO.exec(norm))!==null){ out.push({y:+m[1],mo:+m[2],d:+m[3],s:m.index,e:m.index+m[0].length}); }
  var reDMY=/\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)\s+(\d{4})\b/g;
  while((m=reDMY.exec(norm))!==null){ var mo=monthOf(m[2]); if(mo&&+m[1]>=1&&+m[1]<=31) out.push({y:+m[3],mo:mo,d:+m[1],s:m.index,e:m.index+m[0].length}); }
  var reMDY=/\b([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})\b/g;
  while((m=reMDY.exec(norm))!==null){ var mo2=monthOf(m[1]); if(mo2&&+m[2]>=1&&+m[2]<=31) out.push({y:+m[3],mo:mo2,d:+m[2],s:m.index,e:m.index+m[0].length}); }
  return out;
}
```

extractSessions:

```js
function extractSessions(norm){
  var out=[], m;
  var re1=/(\d{1,3})(?:st|nd|rd|th)\s+(?:[a-z]+\s+){0,3}?session\b/g;
  while((m=re1.exec(norm))!==null){ out.push({num:+m[1], s:m.index, e:m.index+m[0].length}); }
  var re2=/\bsession\s+(\d{1,3})(?!\d)/g;
  while((m=re2.exec(norm))!==null){ out.push({num:+m[1], s:m.index, e:m.index+m[0].length}); }
  return out;
}
```

checkText full:

```js
function checkText(text, rec){
  var nm=normMap(text), norm=nm.norm, map=nm.map;
  function quote(s,e){ if(s>=e) return ""; return text.slice(map[s], map[Math.min(e-1,map.length-1)]+1).trim(); }
  var claims=[];
  var roll=rollCall(rec);
  var off={Y:rec.yes, N:rec.no, A:rec.abstain};
  var rollBy={Y:roll.y, N:roll.n, A:roll.a};
  var codeLabel={Y:"in favour (Y)", N:"against (N)", A:"abstained (A)"};
  var kindLabel={Y:"votes in favour", N:"votes against", A:"abstentions"};

  // numbers
  var nums=extractNumbers(norm), seen={}, i, c, key;
  for(i=0;i<nums.length;i++){
    c=nums[i];
    key=c.kind+"|"+c.value+"|"+Math.round(c.s/6);
    if(seen[key]) continue; seen[key]=1;
    var verdict, note="";
    if(off[c.kind]==null){ verdict="cannot"; note="This record has no official total for this figure."; }
    else if(c.value===off[c.kind]){ verdict="matches"; }
    else if(c.value===rollBy[c.kind] && rollBy[c.kind]!==off[c.kind]){ verdict="matches"; note="Matches the roll-call count ("+rollBy[c.kind]+"), which differs from the official total ("+off[c.kind]+") for this record."; }
    else { verdict="wrong"; }
    claims.push({pos:c.s, type:kindLabel[c.kind], quote:quote(c.s,c.e),
      claim:c.value+" "+(c.kind==="Y"?"in favour":c.kind==="N"?"against":"abstaining"),
      data:"Official totals — in favour: "+off.Y+", against: "+off.N+", abstaining: "+off.A+". Roll call counted from the votes map: "+roll.y+" in favour, "+roll.n+" against, "+roll.a+" abstaining ("+roll.total+" recorded votes).",
      verdict:verdict, note:note});
  }
  // unanimous / without a vote
  var mu=/\bunanimously\b/.exec(norm);
  if(mu){
    var v2 = (off.Y==null) ? "cannot" : ((off.N===0&&off.A===0)?"matches":"wrong");
    claims.push({pos:mu.index, type:"adoption", quote:quote(mu.index,mu.index+mu[0].length),
      claim:"adopted unanimously",
      data:"Official totals — in favour: "+off.Y+", against: "+off.N+", abstaining: "+off.A+"; roll call: "+roll.y+"/"+roll.n+"/"+roll.a+" of "+roll.total+".",
      verdict:v2, note: v2==="matches" ? "No votes against and no abstentions are recorded." : (v2==="wrong" ? "The record shows votes against and/or abstentions." : "No official totals in this record.")});
  }
  var mw=/\bwithout a vote\b/.exec(norm);
  if(mw){
    var v3 = (!rec.votes) ? "cannot" : (roll.total===0 ? "matches" : "wrong");
    claims.push({pos:mw.index, type:"adoption", quote:quote(mw.index,mw.index+mw[0].length),
      claim:"adopted without a vote",
      data: rec.votes ? ("Roll call: "+roll.total+" recorded votes.") : "This record has no votes map.",
      verdict:v3, note: v3==="wrong" ? "A recorded vote exists for this document." : ""});
  }
  // dates
  var dates=extractDates(norm), dms=/^(\d{4})-(\d{1,2})-(\d{1,2})/.exec(String(rec.date||"")), seenD={};
  for(i=0;i<dates.length;i++){
    var d=dates[i], dk=d.y+"-"+d.mo+"-"+d.d;
    if(seenD[dk]) continue; seenD[dk]=1;
    var vd = !dms ? "cannot" : ((+dms[1]===d.y&&+dms[2]===d.mo&&+dms[3]===d.d) ? "matches" : "wrong");
    claims.push({pos:d.s, type:"date", quote:quote(d.s,d.e),
      claim:"date "+d.d+"/"+d.mo+"/"+d.y,
      data:"Recorded date: "+(rec.date||"(none in this record)"),
      verdict:vd, note: dms ? "" : "This record has no date field."});
  }
  // years (only near adoption/vote words, and not inside a full date)
  var reY=/\b((?:19|20)\d{2})\b/g, my, seenY={};
  while((my=reY.exec(norm))!==null){
    var s=my.index, e2=s+my[0].length, inside=false, j;
    for(j=0;j<dates.length;j++){ if(s>=dates[j].s-1 && e2<=dates[j].e+1){ inside=true; break; } }
    if(inside) continue;
    var ctx=norm.slice(Math.max(0,s-40), Math.min(norm.length,e2+40));
    if(!/(adopt|vot|resolution|passed|decision|session)/.test(ctx)) continue;
    var y=+my[1];
    if(seenY[y]) continue; seenY[y]=1;
    var vy = (rec.year==null) ? "cannot" : (y===rec.year ? "matches" : "wrong");
    claims.push({pos:s, type:"year", quote:quote(s,e2), claim:"year "+y,
      data:"Recorded year: "+(rec.year!=null?rec.year:"(none)")+" (date "+(rec.date||"n/a")+")",
      verdict:vy, note:""});
  }
  // sessions
  var sess=extractSessions(norm), recOrd=(String(rec.session||"").match(/(\d+)/)||[])[1], seenS={};
  for(i=0;i<sess.length;i++){
    var sv=sess[i];
    if(seenS[sv.num]) continue; seenS[sv.num]=1;
    var vs = !recOrd ? "cannot" : (+recOrd===sv.num ? "matches" : "wrong");
    claims.push({pos:sv.s, type:"session", quote:quote(sv.s,sv.e),
      claim:"session "+sv.num+(sv.num%10===1&&sv.num!==11?"st":sv.num%10===2&&sv.num!==12?"nd":sv.num%10===3&&sv.num!==13?"rd":"th"),
      data:'Recorded session: "'+(rec.session||"(none)")+'"',
      verdict:vs, note: recOrd ? "" : "This record has no session field."});
  }
  if(!sess.length && /\bsession\b/.test(norm)){
    var si=norm.indexOf("session");
    claims.push({pos:si, type:"session", quote:quote(Math.max(0,si-25), si+7),
      claim:"mentions a session without a number",
      data:'Recorded session: "'+(rec.session||"(none)")+'"',
      verdict:"cannot", note:"The text does not say which session, so there is nothing to compare."});
  }
  // state votes
  var all=findCountries(norm, 0, norm.length);
  var anchored=[
    {re:/\bvoted in favour\b|\bvoting in favour\b|\bvoted for\b|\bvoted yes\b|\bwas in favour\b|\bwere in favour\b|\bsupported\b/g, code:"Y"},
    {re:/\bvoted against\b|\bvoting against\b|\bvoted no\b|\bopposed\b/g, code:"N"},
    {re:/\babstained\b|\babstaining\b/g, code:"A"},
    {re:/\bdid not vote\b/g, code:"NV"}
  ];
  var bare=[
    {re:/\bin favour\b/g, code:"Y"},
    {re:/\bagainst\b/g, code:"N"},
    {re:/\babstention\b/g, code:"A"}
  ];
  function earliest(pats, win){
    var best=null, i2, p, mm;
    for(i2=0;i2<pats.length;i2++){
      p=pats[i2]; p.re.lastIndex=0;
      while((mm=p.re.exec(win))!==null){
        if(!best || mm.index<best.index) best={index:mm.index, end:mm.index+mm[0].length, code:p.code};
        if(mm[0].length===0) p.re.lastIndex++;
      }
    }
    return best;
  }
  var seenC={};
  for(i=0;i<all.length;i++){
    var f=all[i];
    var wRaw=norm.slice(f.e, Math.min(norm.length, f.e+50));
    var cut=wRaw.search(/[.;:!?]/);
    var cut2=wRaw.search(/\s+(?:while|whereas|although|though|but|however|yet)\s+/);
    var cutAt=wRaw.length;
    if(cut>=0) cutAt=Math.min(cutAt,cut);
    if(cut2>=0) cutAt=Math.min(cutAt,cut2);
    var win=norm.slice(f.e, f.e+cutAt);
    var hit=earliest(anchored,win)||earliest(bare,win);
    if(!hit) continue;
    var ck=f.iso+"|"+hit.code;
    if(seenC[ck]) continue; seenC[ck]=1;
    var votes=rec.votes||{};
    var actual=votes[f.iso];
    var name=countries[f.iso]||f.iso;
    var verdict2, data2, note2="";
    if(actual==null){
      verdict2="cannot";
      data2="Not in the roll call: this vote records "+roll.total+" member votes; "+name+" ("+f.iso+") is not among them (not a Council member at this vote, or no vote recorded).";
      note2="Cannot be checked in this data — not the same as wrong.";
    } else {
      data2="Roll call: "+name+" ("+f.iso+") = "+actual+" — "+(codeLabel[actual]||actual)+".";
      if(hit.code==="NV"){ verdict2="wrong"; note2="The roll call records an actual vote for this State."; }
      else verdict2 = (hit.code===String(actual).toUpperCase()) ? "matches" : "wrong";
    }
    var claimTxt = name+" "+(hit.code==="Y"?"voted in favour":hit.code==="N"?"voted against":hit.code==="A"?"abstained":"did not vote");
    claims.push({pos:f.s, type:"State vote", quote:quote(f.s, f.e+hit.end), claim:claimTxt, data:data2, verdict:verdict2, note:note2});
  }
  claims.sort(function(a,b){ return a.pos-b.pos; });
  return claims;
}
```

Wait: quote(f.s, f.e+hit.end) — f.e+hit.end is index in norm of phrase end; map lookup ok.

One issue: `earliest` with anchored "supported" — "France supported the resolution" win=" supported the resolution" → Y ✓. But "France, which Germany supported, voted in favour" — France win cut at ","? cut regex [.;:!?] doesn't include comma → win=" which germany supported, voted in favour" (50 chars) → anchored earliest: "supported" at index 18 vs "voted in favour" at 30 → picks "supported" → France Y. Correct anyway (France voted in favour). Germany: win after "germany" = " supported, voted in favour" → anchored "supported" → Germany Y — but actually Germany supported... ambiguous sentence, fine.

Another: "France voted in favour of the resolution" — win " voted in favour of the resolution" → anchored "voted in favour" ✓.

"abstained" anchored ✓.

Now renderResults and detail and wiring. Also wordCount.

Also note: `quote` uses map[s] — s must be < map.length; guard.

Potential issue: normMap map length equals norm length ✓ (each pushed char appends one norm char... wait in the letter branch, for multi-char expansion e (e.g., "ﬁ" ligature → "fi"), I push two norm chars both mapping to i — map length = norm length ✓ since each iteration pushes exactly one map entry per norm char appended. In the e==="" case push one. In else branch loop pushes per char. Yes map.length===norm.length ✓.

Now HTML body:

```html
<header>
  <h1>Briefing checker — Human Rights Council recorded votes</h1>
  <p id="dataset-desc"></p>
</header>
<main>
  <section class="card">
    <h2>1 · Pick a recorded vote</h2>
    <label for="res-select">Resolution or amendment (recorded vote):</label>
    <select id="res-select"></select>
    <div id="res-detail"></div>
  </section>

  <section class="card">
    <h2>2 · Briefing text</h2>
    <p class="meta">Press the button to ask the model for a ~250-word briefing. <strong>Only the symbol and the title of the selected document are sent</strong> — none of the data on this page; the request leaves your browser. The answer appears in the text box below, marked <code>data-source="ai"</code>. You can edit it or paste your own briefing; editing removes the AI marker and nothing is sent anywhere.</p>
    <button type="button" id="ask-btn">Ask AI for a briefing</button>
    <button type="button" id="stop-btn" class="ghost" hidden>Stop</button>
    <p class="status" id="ai-status"></p>
    <label for="briefing-text">Briefing text (AI answer or your own):</label>
    <textarea id="briefing-text" placeholder="Ask the AI for a briefing, or paste a text here…"></textarea>
    <p class="meta" id="briefing-meta"></p>
  </section>

  <section class="card">
    <h2>3 · Check the claims</h2>
    <p class="meta">The checker finds every checkable claim in the text — the numbers in favour, against and abstaining, the date, the session, and each State said to have voted a certain way — and compares each with the selected recorded vote.</p>
    <button type="button" id="check-btn">Check</button>
    <div id="results"></div>
    <div class="note" id="legend">
      <strong>How to read the verdicts.</strong> <span class="verdict v-match">matches</span> = the recorded vote agrees with the claim.
      <span class="verdict v-wrong">wrong</span> = the recorded vote directly contradicts the claim.
      <span class="verdict v-cannot">cannot be checked</span> = this data has no recorded value to compare the claim with (for example a State that is not among the recorded votes for this document, or a session mentioned without a number).
      <strong>“Cannot be checked” is not the same as “wrong”:</strong> wrong means the data contradicts the claim; cannot be checked means the data simply does not cover it.
    </div>
    <p class="note"><strong>How this is computed:</strong> your text is scanned with fixed patterns — numbers before “in favour / against / abstain…”, “X votes to Y with Z abstentions”, “X-Y-Z” tallies, “unanimously”; dates (ISO, “13 October 2023”, “October 13, 2023”); years near words like “adopted” or “resolution”; “Nth session”; and country names followed by a vote phrase (“voted in favour”, “abstained”, …). Each claim is compared only with the selected record: its official totals (yes/no/abstain), the roll call counted from its votes map, its recorded date and session. All counting and matching is done by this page, deterministically — nothing is estimated.</p>
  </section>
</main>
```

Legend verdict spans inside note — fine.

Wiring:

```js
var sel=document.getElementById("res-select");
var detail=document.getElementById("res-detail");
var results=document.getElementById("results");
var ta=document.getElementById("briefing-text");
var briefingMeta=document.getElementById("briefing-meta");
var aiStatus=document.getElementById("ai-status");
var askBtn=document.getElementById("ask-btn");
var stopBtn=document.getElementById("stop-btn");
var checkBtn=document.getElementById("check-btn");

function current(){ return records[+sel.value]; }

// header desc
(function(){
  var years=records.map(function(r){return r.year;}).filter(function(y){return typeof y==="number";});
  var range = years.length ? (Math.min.apply(null,years)+"–"+Math.max.apply(null,years)) : "n/a";
  document.getElementById("dataset-desc").textContent =
    "Source: "+(HRC.title||"Human Rights Council recorded votes")+" · "+records.length+" recorded votes (resolutions and amendments) · years "+range+
    " · each record carries the roll call of the Council members (vote codes "+voteCodeText+"). All figures on this page are counted from these records in your browser.";
})();

if(!records.length){
  sel.disabled=true; askBtn.disabled=true; checkBtn.disabled=true;
  detail.innerHTML="<p class='note'>No recorded votes were found in WORKSHOP_DATA.hrc.</p>";
} else {
  records.forEach(function(r,i){
    var o=document.createElement("option");
    o.value=String(i);
    o.textContent=(r.symbol||"(no symbol)")+" — "+(r.title||"(untitled)")+" ("+(r.year||"?")+")";
    sel.appendChild(o);
  });
  var start=records.findIndex(function(r){ return r.symbol==="A/HRC/RES/51/27"; });
  sel.value=String(start>=0?start:0);
  renderDetail(current());
  sel.addEventListener("change", function(){
    renderDetail(current());
    results.innerHTML="";
  });
}
```

renderDetail as planned. Note off values may be undefined → display "n/a": use fmt(v){return v==null?"n/a":v}.

Ask AI:

```js
var cancelled=false;
askBtn.addEventListener("click", function(){
  var rec=current(); if(!rec) return;
  if(typeof studio==="undefined" || !studio || typeof studio.ask!=="function"){
    aiStatus.textContent="studio.ask is not available in this environment, so no briefing can be requested.";
    return;
  }
  cancelled=false; askBtn.disabled=true; stopBtn.hidden=false;
  aiStatus.textContent="Sending 1 item to the model — the symbol and the title only; no data from this page is included. The request leaves your browser. Waiting for the answer…";
  var prompt='You are helping a human rights professional. Using only your own knowledge, write a neutral briefing of about 250 words about the following UN Human Rights Council document. You are given only its symbol and title — no other data — so do not ask for more. Do not ask questions.\n\nSymbol: '+rec.symbol+'\nTitle: '+rec.title+'\n\nCover what the document is about and, if you know it, how the Council voted on it. Reply strictly as JSON with one key: {"briefing": "<the briefing text>"}';
  studio.ask(prompt, {json:true}).then(function(raw){
    if(cancelled){ aiStatus.textContent="Stopped by you — the model's answer was discarded."; return; }
    var briefing=String(raw==null?"":raw);
    try{ var p=JSON.parse(briefing); if(p && typeof p.briefing==="string") briefing=p.briefing; }catch(e){}
    briefing=briefing.trim();
    if(!briefing){ aiStatus.textContent="The model returned an empty answer."; return; }
    ta.value=briefing;
    ta.setAttribute("data-source","ai");
    briefingMeta.textContent="AI answer from studio.ask ("+wordCount(briefing)+" words), rendered with data-source=\"ai\". Edit it or paste your own text — editing removes the marker; nothing is sent anywhere unless you press the button again.";
    aiStatus.textContent="Answer received from the model (1 item was sent: the symbol and the title only).";
  }).catch(function(err){
    aiStatus.textContent="The request to the model failed: "+err;
  }).finally? ... 
```

Use .then/.catch and reset buttons in both: simpler:

```js
  function done(){ askBtn.disabled=false; stopBtn.hidden=true; }
  studio.ask(...).then(function(raw){ ...; done(); }).catch(function(err){ aiStatus...; done(); });
```

But if cancelled we return early — still call done(). Put done() in both paths.

stopBtn: cancelled=true; aiStatus.textContent="Stopping… the answer will be discarded when it arrives.";

ta input listener:

```js
ta.addEventListener("input", function(){
  ta.removeAttribute("data-source");
  briefingMeta.textContent="Your own text (edited locally). Press “Check” to verify its claims against the selected recorded vote.";
});
```

wordCount: `function wordCount(s){ return (s.trim().match(/\S+/g)||[]).length; }`

checkBtn:

```js
checkBtn.addEventListener("click", function(){
  var rec=current();
  if(!rec){ results.innerHTML="<p class='note'>No recorded vote is selected.</p>"; return; }
  var text=ta.value;
  if(!text.trim()){ results.innerHTML="<p class='note'>The text box is empty — ask the AI for a briefing or paste a text first.</p>"; return; }
  var claims=checkText(text, rec);
  renderResults(claims, rec);
});
```

renderResults as planned with symbol link.

renderDetail:

```js
function fmt(v){ return (v==null||v==="") ? "n/a" : v; }
function rollCall(rec){
  var v=(rec && rec.votes && typeof rec.votes==="object")?rec.votes:{};
  var y=0,n=0,a=0,t=0,k;
  for(k in v){ t++; var c=String(v[k]).toUpperCase(); if(c==="Y")y++; else if(c==="N")n++; else if(c==="A")a++; }
  return {y:y,n:n,a:a,total:t};
}
function renderDetail(rec){
  var roll=rollCall(rec);
  var off={Y:rec.yes,N:rec.no,A:rec.abstain};
  var url=rec.doc_url||"", recUrl=rec.record_url||"";
  var sym=rec.symbol||"(no symbol)";
  var symLink = url ? '<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(sym)+'</a>'
              : (recUrl ? '<a href="'+esc(recUrl)+'" target="_blank" rel="noopener">'+esc(sym)+'</a>' : esc(sym));
  var sponsors=(Array.isArray(rec.main_sponsors)?rec.main_sponsors:[]).filter(Boolean);
  var tot=(off.Y||0)+(off.N||0)+(off.A||0);
  var bar="";
  if(tot>0){
    bar='<div class="bar"><span style="width:'+(off.Y/tot*100)+'%;background:#1a7f37"></span>'+
        '<span style="width:'+(off.N/tot*100)+'%;background:#b3261e"></span>'+
        '<span style="width:'+(off.A/tot*100)+'%;background:#9aa4ae"></span></div>'+
        '<p class="barlabel">in favour '+off.Y+' · against '+off.N+' · abstaining '+off.A+' (official totals; bar widths proportional)</p>';
  }
  var differ=(roll.y!==off.Y)||(roll.n!==off.N)||(roll.a!==off.A);
  var links="";
  if(url) links+='<a href="'+esc(url)+'" target="_blank" rel="noopener">UN document '+esc(sym)+'</a>';
  if(url&&recUrl) links+=" · ";
  if(recUrl) links+='<a href="'+esc(recUrl)+'" target="_blank" rel="noopener">OHCHR search-library record</a>';
  detail.innerHTML=
    '<h3>'+symLink+' <span class="kindtag">'+esc(rec.kind||"")+'</span></h3>'+
    '<p class="rtitle">'+esc(rec.title||"")+'</p>'+
    '<dl class="facts">'+
    '<div><dt>Date</dt><dd>'+esc(fmt(rec.date))+'</dd></div>'+
    '<div><dt>Session</dt><dd>'+esc(fmt(rec.session))+'</dd></div>'+
    '<div><dt>Agenda item</dt><dd>'+esc(fmt(rec.agenda_item))+'</dd></div>'+
    '<div><dt>Main sponsors</dt><dd>'+(sponsors.length?esc(sponsors.join("; ")):"(none listed)")+'</dd></div>'+
    '<div><dt>Official totals</dt><dd>in favour '+fmt(off.Y)+' · against '+fmt(off.N)+' · abstaining '+fmt(off.A)+'</dd></div>'+
    '<div><dt>Roll call (counted from the votes map)</dt><dd>'+roll.y+' in favour · '+roll.n+' against · '+roll.a+' abstaining — '+roll.total+' recorded member votes</dd></div>'+
    '<div><dt>Links</dt><dd>'+(links||"(none)")+'</dd></div>'+
    '</dl>'+bar+
    (differ?'<p class="warn">The roll-call count differs from the official totals for this record (gaps in the source). Both are shown; the checker compares claims with the official totals first and notes when a claim matches the roll call instead.</p>':'')+
    '<p class="note"><strong>How this is computed:</strong> the official totals are the record’s yes / no / abstain fields; the roll call is counted by this page from the votes map (one entry per Council member; codes '+esc(voteCodeText)+').</p>';
}
```

renderResults:

```js
function renderResults(claims, rec){
  var url=rec.doc_url||rec.record_url||"";
  var sym=rec.symbol||"(no symbol)";
  var link=url?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(sym)+'</a>':esc(sym);
  var html='<p>Checking the text against '+link+' — '+esc(rec.title||"")+' ('+esc(rec.kind||"")+', '+esc(rec.date||"")+').</p>';
  if(!claims.length){
    html+='<p class="note">No checkable claim was found in the text (no vote numbers, date, session or State vote). Nothing to compare.</p>';
    results.innerHTML=html; return;
  }
  html+='<table><thead><tr><th style="width:34%">Claim as written</th><th>What the recorded vote says</th><th style="width:12%">Verdict</th></tr></thead><tbody>';
  claims.forEach(function(c){
    var vc=c.verdict==="matches"?"v-match":c.verdict==="wrong"?"v-wrong":"v-cannot";
    html+='<tr><td><span class="ctype">'+esc(c.type)+'</span><br>“'+esc(c.quote)+'”<br><strong>'+esc(c.claim)+'</strong></td>'+
          '<td>'+esc(c.data)+(c.note?'<br><em>'+esc(c.note)+'</em>':'')+'</td>'+
          '<td><span class="verdict '+vc+'">'+c.verdict+'</span></td></tr>';
  });
  html+='</tbody></table>';
  var m=0,w=0,u=0;
  claims.forEach(function(c){ if(c.verdict==="matches")m++; else if(c.verdict==="wrong")w++; else u++; });
  html+='<p class="summary"><strong>'+claims.length+' claim'+(claims.length===1?"":"s")+' checked:</strong> '+m+' match · '+w+' wrong · '+u+' cannot be checked.</p>';
  results.innerHTML=html;
}
```

Note: verdict text "cannot" — display "cannot be checked"? The verdict value is "cannot"; display label: map to "cannot be checked". In table: label = c.verdict==="cannot"?"cannot be checked":c.verdict. Adjust.

Also in summary "cannot be checked".

Now check: does anything call studio.ask on load? No ✓.

Check "Every row that shows a document has its symbol, linked to doc_url in a new tab" — results header line has symbol link ✓, detail has it ✓.

Potential issue: `records.findIndex` — fine.

Also initial results hint: set results.innerHTML initially to a hint paragraph. Add after wiring: results.innerHTML='<p class="meta">Press “Check”…</p>' — but if records empty skip. Fine, set in else branch.

Also `sel.value=String(...)` before options? Options added first ✓.

Edge: `+sel.value` when no records → NaN; current() returns undefined; guarded.

Now double-check normMap with uppercase: "Kenya".toLowerCase() → "kenya" ✓. Digits ✓. "A/HRC/RES/51/27" → "a hrc res 51 27" ✓.

Country "Côte d'Ivoire" → normMap: "côte d'ivoire" → lowercase "côte d'ivoire", NFD: "cote d'ivoire" (ô→o+combining, stripped) → chars: c,o,t,e, space, d, ' → space, i,v,o,i,r,e → "cote d ivoire" ✓. Pattern from name: split on [\s\-]+ → ["cote","d","ivoire"] → "cote[\\s\\-]+d[\\s\\-]+ivoire" ✓ matches text "Côte d'Ivoire" → norm "cote d ivoire" ✓.

Text "Ivory Coast" won't match — acceptable.

Now, one more check on `earliest` anchored regex with alternation and /g: /\bvoted in favour\b|\bvoting in favour\b|.../g — exec finds first occurrence of any alternative ✓.

Window cut: wRaw.search(/[.;:!?]/) — norm has these as spaces! Wait — normMap converts punctuation to spaces! So "France voted in favour. Germany voted against." → norm "france voted in favour  germany voted against " — the "." became space! So cut on [.;:!?] never fires in norm. Oops. I need sentence boundaries preserved in norm. Options: keep "." as "." in norm? But then country patterns with [a-z0-9] boundaries — "." is non-alnum so boundary ok. Let me keep "." ";" ":" "!" "?" as themselves in normMap (they're useful boundaries), and convert other punctuation to space. Then date ISO "2023-10-13" keeps hyphens ✓, "13 October 2023," → comma → space ✓. reISO \b works with "." present ✓. Clause cut regex works ✓. Country boundary [^a-z0-9] — "." qualifies ✓. Phrase \b works ✓.

But careful: keeping "." means "No. 27" → "no. 27" — my "no (\d+)" pattern requires \s+ between — "no. 27" has "." between → /\bno\s+(\d{1,3})/ won't match "no. 27" ✓ actually good, removes that false positive! And "no: 16" → "no: 16" — pattern needs \s+ after "no" — ":" not \s → won't match "no: 16"! Hmm. Tally "yes: 29, no: 16" → norm "yes: 29 no: 16" — patterns fail. Add optional punctuation: /(^|[^\d])no[\s:]+(\d{1,3})(?!\d)/g etc. Let me update label patterns to allow [:\s]+ after keyword: yes/no/abstain/in favour/against followed by [\s:]+ then digits. And number-first patterns: "29 votes in favour" fine; "in favour: 29" → "in favour: 29" → pattern /(^|[^\d])in favour[\s:]+(\d{1,3})(?!\d)/ ✓.

Also reTri with "-" kept ✓. reTo "29 votes to 16, with 1 abstention" → comma → space ✓.

Also the year regex \b((?:19|20)\d{2})\b — with "." kept, "in 2023." → \b after "2023" before "." ✓.

Also cut regex for window: /[.;:!?]/ ✓ now works.

Also clause keywords search /\s+(?:while|...)\s+/ ✓.

Also "supported" etc fine.

Update normMap: keep chars in ".;:!?" as-is; also keep "-"; everything else → space. Also maybe keep "," ? No — comma → space is fine (we don't need comma boundaries since window cut doesn't use comma... earlier I decided not to split on comma; window approach handles lists). OK.

But wait: with "." kept, "U.S." → "u.s." — country alias "usa" unaffected. "U.S. voted in favour" → norm "u.s. voted in favour" — alias "us" would need boundary: "u.s." — pattern for "us": (^|[^a-z0-9])us(?![a-z0-9]) — in "u.s.", "us" isn't present as contiguous ("u.s." has dots). So "U.S." not matched. Add alias pattern "u\.s\."? Add alias "u.s." → pattern escRe("u.s.") = "u\.s\." with boundaries — but boundary check [^a-z0-9] before "u" ✓ after "." ✓... the trailing (?![a-z0-9]) after final "." ✓. Add aliases: "u.s.", "usa", "united states", "u.k.", "uk". I'll add "u.s." and "u.k.".

Also month names with "." — "Oct. 13, 2023" → "oct. 13 2023" — reMDY: ([a-z]+)\s+(\d{1,2})... "oct." has "." → [a-z]+ matches "oct" then \s+ required but next is "." → fail. Add optional dot: ([a-z]+)\.? — update reMDY/reDMY month part to ([a-z]+)\.?\s+... Let me adjust: reDMY: /\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)\.?\s+(\d{4})\b/g; reMDY: /\b([a-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})\b/g. monthOf("oct") ✓.

OK. Also ISO with "." no.

Now also the "for" number pattern: "29 for" — with "." kept, "for." at sentence end: "29 for." → pattern ...for\b ✓ matches "29 for" ✓.

Also "against" bare in numbers: "16 against." ✓.

Now the window cut also should cut at newline? "\n" → space in norm. Sentence cut via "." covers most. Also cut at "—" → space. fine.

One more: anchored phrase "supported" — "France supported the resolution" ✓. But "unsupported"? \b prevents? "unsupported" contains "supported" but \b before "supported" — "un" + "supported": boundary between "n" and "s"? both word chars → no boundary → no match ✓.

Now the AI prompt includes rec.symbol and rec.title — if title contains quotes, fine in JS string.

Also ensure `studio.ask` called with {json:true} ✓.

Also "show progress" — status text ✓; "let the user stop" — stop button ✓.

Now, the initial selected record: A/HRC/RES/51/27 — findIndex on symbol ✓ (user asked to start with it; reading from data).

Also note: the description says hrc has `countries` map and `vote_codes`. ✓.

Let me also double check `extractNumbers` pattern "for": /(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?for\b/g — "29 for" ✓; false positive "2019 for"? (?!\d) after "201"? "2019": \d{1,3} greedy "201", next "9" digit → fail; "20" next "1" fail; "2" next "0" fail → no match at that start; next start "019 for"? boundary (^|[^\d]) — preceded by "2" digit → fail. Good.

"no" pattern: /(^|[^\d])no[\s:]+(\d{1,3})(?!\d)/g — "no 16" ✓; "no. 16" → "no. 16": after "no" comes "." — [\s:] doesn't include "." → no match. Hmm "No. 16" false positive avoided ✓ but "no: 16" ✓ matches. Good.

"yes[\s:]+(\d{1,3})" ✓.

"in favour[\s:]+(\d{1,3})" ✓.

"against[\s:]+(\d{1,3})" — "against: 16" ✓.

"abstain\w*[\s:]+(\d{1,3})" ✓.

Number-first: "(\d{1,3})(?!\d)\s+(?:votes?\s+)?in favour\b" ✓; "...against\b" ✓; "...abstain\w*" ✓; "...for\b" ✓.

Now dedupe key uses Math.round(c.s/6) — patterns matching same phrase at same s dedupe ✓; "29 votes in favour" also matched by...? Only one pattern. "in favour: 29" matched by label pattern only. OK.

Potential duplicate: "adopted by 29 votes to 16, with 1 abstention" — reTo gives Y=29,N=16,A=1; also "1 abstention" matches A-pattern "(\d+) abstain" → A=1 at different s → key differs → duplicate A claim (same value 1, different position) → two rows both verdict matches. Minor; acceptable, or dedupe by kind+value globally when verdict same? Keep position-based dedupe; duplicates rare. Actually "with 1 abstention" — A-pattern: /(^|[^\d])(\d{1,3})(?!\d)\s+(?:votes?\s+)?abstain\w*/ matches "1 abstention" ✓ and reTo also adds A=1 at base s (start of "29 votes to...") — different s → two rows. To reduce noise, dedupe by kind+value globally? But then "29 in favour" appearing twice in text → one row — fine, actually cleaner. But if text says "29 in favour" and later "30 in favour" (contradiction), both kept (different values) ✓. I'll dedupe numbers by kind+value (keep first occurrence). Simpler and cleaner. Do that: key=kind+"|"+value.

Similarly dates dedupe by full date ✓ already. Sessions by num ✓. Years by year ✓. States by iso+code ✓.

Now, verdict for number when off missing: records should have yes/no/abstain; if missing → cannot ✓.

I think the design is solid. Now also handle `rec.votes` values maybe lowercase — String(actual).toUpperCase() compare ✓.

Write final HTML. Also include `<meta charset>`. Title.

Also add small footer? Not needed.

Let me also make sure the check works when user pastes text with "A/HRC/RES/51/27" — contains "51 27" — number patterns need "in favour" etc after digits — no. Year regex: "51" not 4-digit ✓. Session: "res 51 27" — re2 "session (\d+)" no. OK.

But wait: symbol in text "A/HRC/RES/51/27" — reTri? "51 27" no dash ✓.

What about "HRC-51"? → "hrc-51" — reTri needs three numbers ✓ no.

One more: the year keyword ctx includes "vot" — "vote" ✓; but also matches "voted" ✓ good; "devoted"? contains "vot" → "devoted to human rights in 2011" → year claim 2011 → wrong verdict. Hmm. Use \bvot|adopt|resolution|passed|decision|session\b-ish: /(adopt|\bvot|resolution|passed|decision|session)/ — "devoted" — \bvot requires boundary before v — "devoted" has "e" before "vot" → no boundary → no match ✓. "voted" → \bvot ✓. Good: use /(adopt|\bvot|resolution|passed|decision|session)/.

Also "adopt" matches "adopted"/"adoption" ✓.

Now finalize. Also add `lang="en"`.

Counting lines — will be ~600. Fine.

One more requirement check: "A button 'Ask AI for a briefing' asks the model ... for a 250-word briefing on that resolution from what it already knows: send only the symbol and the title, none of our data." ✓ prompt contains only symbol+title (plus instructions). "Put the answer in a text box, where I can also paste a text of my own." ✓ textarea. "A 'Check' button then finds every checkable claim..." ✓. "Show a table with the claim as written, what the recorded vote says, and a verdict: matches, wrong, or cannot be checked in this data." ✓. "Explain that 'cannot be checked' is not the same as 'wrong'." ✓ legend.

"start with A/HRC/RES/51/27" ✓ preselect.

Also "When the app sends text to the model, say so on screen: how many records, and that they left the browser." ✓ status: "Sending 1 item ... leaves your browser."

"Render every value that came from studio.ask inside an element with data-source='ai'" ✓ textarea.

Also never call studio.ask on load ✓.

Now write it all out. Also careful: in JS strings inside HTML, avoid "</script>" sequences — none.

Also the em-dash / quotes in strings fine (UTF-8).

Let me write the final code block now, being careful with syntax.

Also: `sel.addEventListener` inside else branch; define renderDetail before use — function declarations hoisted ✓ (I'll use function declarations).

Also `results` initial hint: after wiring, if records.length: results.innerHTML='<p class="meta">Press “Check” to compare the text above with the selected recorded vote.</p>';

Edge: `ta` input event also fires when we set ta.value programmatically? No, only user input ✓.

Write it.

Also small thing: in renderResults the verdict label: `var label = c.verdict==="cannot" ? "cannot be checked" : c.verdict;`

And summary counts use u for cannot.

Final check of normMap keeping ".;:!?": implement:

```js
else if(c==="-"||c==="\u2013"||c==="\u2014"){ norm+="-"; map.push(i); }
else if(".;:!?".indexOf(c)>=0){ norm+=c; map.push(i); }
else { norm+=" "; map.push(i); }
```

But this is inside the per-char loop over e (NFD expansion). For ch="." → e="." → loop: c="." → kept ✓. For ch="é" → e="e\u0301" → chars "e" (alnum) and combining mark (not alnum, not in keep sets → space!). Hmm — combining mark would append a space after "e": "é" → "e " — that breaks words: "Côte" → "cote " with trailing space?? Wait NFD of "ô" is "o" + U+0302; my regex strips combining marks: e = ch.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"") — I strip them in e already ✓. So e="o" ✓. Good, the replace handles it.

But careful: the strip regex range \u0300-\u036f covers combining diacriticals ✓.

Also ch.toLowerCase() before NFD: "İ" → "i̇" etc — edge, fine.

Now the boundary regex for names uses [^a-z0-9] — "." qualifies as boundary ✓, "-" is NOT in [a-z0-9] so "guinea-bissau": pattern "guinea[\s\-]+bissau" — in text "guinea-bissau" norm keeps "-" ✓ matches ✓. But boundary before "guinea" if preceded by "-"? e.g., "x-guinea"? [^a-z0-9] includes "-" → would match "guinea" in "x-guinea" — minor.

OK writing final now.

Also one more: `findCountries(norm, 0, norm.length)` — patterns global regex reused; reset lastIndex each call ✓ (I set p.re.lastIndex=0 at loop start ✓).

In `earliest`, patterns' regexes are shared objects with /g — reset lastIndex=0 before exec loop ✓.

Let me now also think: window after name is 50 chars — "France, together with Germany and Kenya, voted in favour" — France win: " together with germany and kenya voted in favour" = 48 chars ✓ contains "voted in favour" ✓.

"France voted in favour of the resolution and Germany abstained" — France win cut at... no "." — win = " voted in favour of the resolution and germany abstained" (56>50 → 50 chars: " voted in favour of the resolution and germany abst") → anchored earliest "voted in favour" ✓ Y. Germany win = " abstained" → A ✓. Good.

Now finalize the answer text before code: 2–3 sentences.

Write everything.

Actually one more detail — `checkText` uses `rec.votes` for state claims; if votes missing → all state claims "cannot" ✓ handled by actual==null.

Also `rollCall` when votes missing → total 0; detail shows "0 recorded member votes" — fine, and differ check: roll.y(0)!==off.Y → warn shows — maybe suppress warn if no votes map: if(!rec.votes) skip warn. Add condition: differ && rec.votes.

OK write final.

Let me write the complete file:

(Constructing carefully...)

Also I realize: in extractNumbers, patterns with leading (^|[^\d]) — for "in favour 29" I wrote /(^|[^\d])in favour[\s:]+(\d{1,3})(?!\d)/g — boundary before "in" — if text "29 in favour 29"? weird. fine.

Also add pattern for "in favour of the resolution: 29"? covered by in favour[\s:]+? "in favour of the resolution 29" — "in favour" followed by " of..." not digits → no match. fine.

Also "votes in favour: 29" → "in favour: 29" ✓.

Double-check reTo doesn't need "by": "adopted 29 votes to 16" ✓ matches.

Now the final code. I'll write it in one go.

Also ensure the `legend` note is inside check card ✓.

Also the top-of-page description must include source, n, years ✓.

Potential HTML-injection via esc everywhere for data ✓; claims quote/data escaped ✓.

Let me write out now. I'll aim for clarity.

One more consideration on `studio` — reference `window.studio`. Use `var studioObj = window.studio;` then check.

Final code below.