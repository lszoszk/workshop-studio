Build a single HTML file. Features: resolution selector (default A/HRC/RES/51/27 if present, else first), AI briefing button with progress, textarea, Check button parsing claims, table of verdicts.

Claim extraction: for the selected resolution's known symbol, parse text for:
- "in favour" numbers, "against", "abstain": patterns like "29 in favour, 16 against and 1 abstention" or "adopted by a recorded vote of 29 to 16, with 1 abstention".
- date: parse dates in text, compare to record date.
- session: e.g. "51st session" or "HRC's 51st session" — match against record.session.
- States voted a way: for each country name in WORKSHOP_DATA.hrc.countries (ISO3 -> name), if name appears in text with nearby vote word ("voted in favour", "voted against", "abstained", or "supported"/"opposed"? keep to vote words). Check votes[iso].

Verdicts: matches / wrong / cannot be checked in this data. Show both official totals and roll-call counts.

Parsing numbers: regex like /(\d+)\s*(?:votes?\s*)?in favour/i, /(\d+)\s*(?:votes?\s*)?against/i, /(\d+)\s*abstention/i. Also "by a vote of 29 to 16 with 1 abstention". I'll do a reasonable multi-pattern parser.

States: for each country name, find occurrences with context ±60 chars, look for vote phrases: "voted in favour", "in favour", "voted against", "against", "abstained", "abstention". Order matters — search "abstained" first, then "voted against|opposed|against", then "voted in favour|in favour|supported". Avoid double counting "against" inside "in favour... against". I'll use a context window regex per occurrence.

Cannot be checked: e.g., dates not matching anything? A date found in text is checkable against the record's date (only the vote date is known). If a date claim references a different date — is it "wrong" or "cannot be checked"? The resolution has one date; any date claim can be checked against it: matches or wrong. But dates for other events (adoption of mandate earlier) can't be checked — hard to distinguish. I'll say: date claims are checked against the vote date; if mismatch, verdict "wrong" but with caveat? Simpler: any explicit date in text is checked against record date; mismatches marked wrong with note that data only holds the vote date. That's honest.

Session: extract /(\d+)(st|nd|rd|th) session/ occurrences, compare to record.session number if record session contains one; else cannot be checked.

Numbers: check against roll-call counts AND official totals; if they disagree with both → wrong; if match roll-call but not official → "matches (roll-call count)".

Countries: check votes[iso]; if country not in votes map (not a member in that record) → cannot be checked (this data has no vote for them) — actually roll call should cover all members; a non-member name might appear in sponsors. If ISO3 not in votes → cannot be checked in this data.

Note about "cannot be checked ≠ wrong".

UI: selector of resolutions (sorted by symbol? maybe by year desc), default A/HRC/RES/51/27 if exists else first. Show resolution details panel: title, symbol link, date, session, sponsors, official totals and roll-call totals, votes summary (Y/N/A counts from votes object).

AI: send only symbol + title, show "1 record leaves the browser" note, data-source="ai" on output. Show progress state.

Keep under ~700 lines. Write it.