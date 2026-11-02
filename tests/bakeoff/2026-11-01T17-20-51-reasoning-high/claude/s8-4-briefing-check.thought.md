I need to plan a single-file HTML build under 700 lines, starting with a header showing the data source and sample size, then a searchable resolution picker defaulting to A/HRC/RES/51/27 that displays the selected record's symbol, title, date, session, vote counts, and sponsors.

I'm also designing an "Ask AI" feature that sends only the symbol and title to the model, with a clear disclosure about what leaves the browser, and I need to track whether the resulting text came from the AI or was user-edited so I can correctly tag elements with data-source="ai" versus user input throughout the claim-check table.

Now I'm working out regex patterns to extract vote counts from text — matching phrases like "29 in favour," "16 against," and "1 abstention" in various formats, including combined patterns like "29 votes to 16 with 1 abstention."

I'll include modest word-number support despite the added complexity risk. Now I need to decide how to reconcile official totals versus roll call counts when verifying a claim—I'll treat a claim as "matches" if it agrees with the official total, noting separately if the roll call tally disagrees, rather than requiring both to align.

For dates, I'll handle common formats like "7 July 2026", "July 7, 2026", and "2026-07-07", and also allow year-only claims like "adopted in 2022" to be checked against the record's year, though I need to be careful not to misparse numbers embedded in resolution names.

I need to parse month names properly and compare them for equality, flagging a mismatch if year and month align but the day is off. But I'm wary that unrelated dates in the text—like a report deadline—could get mistakenly flagged as wrong vote dates, so I want to only treat a date as a vote-date claim if its surrounding sentence has adoption/voting-related keywords; otherwise mark it as unable to be checked with an explanation.

For session numbers, I'm matching patterns like "51st session" or "fifty-first session," extracting the number and falling back to the symbol (like A/HRC/RES/49/18) when no explicit number appears, while treating special sessions and missing numbers as unable to be checked.

Building the regex pattern...

Still refining vote-count regex patterns...

Still writing regex patterns...

I also need to handle deduplication so overlapping claim spans don't get counted twice, keeping only the most relevant match.

I should also handle claims of "adopted without a vote" or "by consensus" — since every record here is a recorded vote by definition, such a claim is contradicted and should be flagged wrong, noting that the data only contains recorded votes. I'll build a pattern catching phrases like "by consensus," "without a vote," or "unanimously" to detect this.

Now for checking per-country voting claims, I need to map ISO3 codes to country names, then scan sentences for country mentions alongside vote-direction cues like "in favour," "against," or "abstained," matching each country to the nearest applicable cue within its sentence.

I should add a rule: if no cue appears within the same clause as a country mention, treat it as unresolved rather than guessing, since some mentions (like "sponsored by Cuba") aren't vote claims at all. I also need to handle country name matching carefully, since official names like "Democratic Republic of the Congo" may need an alias map to match correctly.

I'm building a normalization system: lowercase text, strip accents, then index official names plus common aliases keyed by ISO3 code so matching stays reliable regardless of which name variant appears (US vs United States, Russia vs Russian Federation, Czechia vs Czech Republic, etc.). I need to be careful with short aliases like "US" that could collide with common words like "us" the pronoun, so I'm considering case-sensitive matching for those ambiguous short forms.

I also want to match longest-first and prevent overlaps, since names like "Democratic Republic of the Congo" contain "Congo", and "South Korea" contains "Korea" -- word boundaries plus greedy longest-match ordering should handle these nesting issues, including similar cases like Niger/Nigeria and Sudan/South Sudan.

If a country appears in the text but isn't in this roll call's vote entries, that's a "cannot be checked" case -- it means the country wasn't a Council member at that session or there's a gap in the source data. But if a country isn't in the countries map at all, I can't detect it, so I'll just skip those entirely.

For verdicts, I'll compare the recorded vote letter against the claimed vote: if they match, it's "matches"; otherwise "wrong," and I'll display the actual recorded vote for context like "Kenya — Y (in favour)." Negations and complex phrasing like "did not vote against" are a real limitation I should flag, so I'll note that readers should check the highlighted claim in context, and I'll structure the table with the claim as written, the recorded vote, and the verdict.

I'm settling on columns for the output table: Type, Claim as written, Recorded vote says, Verdict — skipping the extra check for mismatched resolution symbols mentioned in text since it's out of scope. I also want a summary section at top tallying matches/wrong/cannot-check counts, plus an explanation that "cannot be checked" doesn't mean false — it just means there's no dataset record to verify against, so the user should check the actual resolution text via the doc_url.

For honesty, I also want to surface sentences that contain no checkable claim at all (e.g. descriptions of what the resolution does), showing a count and a collapsible list of them, determined by checking whether any claim's span falls within each sentence's range. I'm working out a sentence-splitting approach using regex with lookbehind to handle punctuation like periods in numbers, dates, and abbreviations without over-splitting.

Still refining sentence boundaries...

Claims get extracted from the whole text with sentence lookup by index for context, while state claims work per sentence, and now I'm designing the record picker with a filter input and a select sorted by date.

Each record card should link the symbol to its doc_url (or fall back to record_url) in a new tab, and show title, date, session, agenda item, sponsors, official totals, roll-call counts, and any mismatch warnings, with an expandable breakdown of the roll call by country group.

I'm also adding an "Ask AI" button that prompts the model to write a ~250-word briefing on the resolution using only prior knowledge, instructing it to skip uncertain details rather than guess, while still nudging it to mention date, session, and vote outcome if known so there are checkable claims to verify against the real data.

For transparency, I'll show the exact prompt sent in the UI and disable the button with a "waiting for model…" state during the single call, plus a cancel option to discard the result if the user doesn't want to wait.

The textarea should track whether its content came from the AI or from the user, showing a small source label like "Source: AI answer" or "Source: pasted or edited by you" — I'll just clear the AI marker on any user edit to keep it simple.

Check button runs validation against the current text and selected record, clearing stale results if the input changes, and tags each claim with its origin for later reference. I'm rendering output safely with escaped text, showing each claim in quotes alongside a truncated, muted preview of its surrounding sentence for context, with each claim object carrying its type, text, index, sentence, and linked record data.

Setting up data access to the workshop's HRC dataset, sorting records by date, then building a lookup table mapping number words (zero through sixty, including ordinals) to their numeric values for parsing session references.

I'm separating cardinal and ordinal word sets since "second" is ambiguous depending on context, and writing a helper function that converts word phrases or digit strings into numbers by summing matched tokens...

Building number-parsing regex...

Still building the ordinal session pattern...

Still refining the regex pattern...

Still writing vote-pattern regexes...

Still refining the regex patterns...

For the "to" pattern matches like "29 votes to 16", I'll generate two claims sharing the same matched text — one labeled as the in-favour count and one as the against count. I also need to track span overlaps with a list of used ranges so overlapping matches get skipped, processing the "to" patterns in order.

I'm checking edge cases: phrases like "29 in favour, 16 against and 1 abstention" should correctly split into separate yes/no/abstain claims, and variations like "votes in favour" or "votes against" shouldn't conflict with each other. For comparing official tallies against roll-call vote counts, I'm writing a comparison function that checks the official yes/no/abstain numbers against the counted votes from the roll object.

I'm now setting up date-parsing regex patterns to catch ISO format dates, as well as day-month-year and month-day-year formats with ordinal suffixes and optional "of" phrasing.

Still writing regex patterns...

I also need to handle partial dates like "October 2022" where only month and year are given, and build out the month name alternation covering both full names and common abbreviations like "Sept," while being careful with case-insensitivity and ordering full names before abbreviations to avoid partial matches.

For determining whether a date refers to the actual vote date versus some other date in the sentence (like a reporting deadline), I need to check for contextual cues such as "adopted," "voted," "passed," or "approved" near the date, but I have to be careful not to use overly broad words like "resolution" that could cause false positives when the sentence mentions an unrelated date. I'm narrowing the cue list and restricting the search to a window of characters before and after the date match to avoid misattributing dates in sentences with multiple dates.

For comparing the recorded vote date against the extracted one, I need logic to flag exact matches versus partial matches (like matching month and year but not day), and for year-only mentions I need to compute where exactly in the string the year appears relative to the cue phrase. For session numbers, I'm figuring out how to extract them either from structured symbols like "A/HRC/RES/49/18" or from ordinal text like "49th session," falling back to unknown if neither pattern is found.

I'm also refining how to distinguish ordinal word forms like "fifty-first" from compound tens, requiring suffixes on bare digits to avoid false matches, and flagging special sessions separately since their numbering doesn't align with regular sessions. I need to watch out for cases where "session" refers to a different body entirely, like a UN committee rather than the Human Rights Council.

I'm settling on only flagging a session number as incorrect when the sentence contains cue words like "adopt," "vote," "pass," "approve," "Council," or "HRC" -- otherwise marking it as not applicable. I'm writing a normalization function that strips diacritical marks and lowercases text for comparison purposes.

Since stripping accents can occasionally shift character positions relative to the original string, I'm adding a safeguard: fall back to using the normalized string for extracting clause text whenever its length doesn't match the original exactly.

I'm building a name-to-ISO lookup from country names and aliases, normalizing apostrophe variants, and compiling a single regex with alternatives sorted longest-first so multi-word names match before shorter substrings.

For the vote classification, I'm drafting cue-phrase regexes for each clause to detect "in favour," "voted for," "supported," and similar expressions, while being careful that words like "approved" don't create ambiguous matches.

Then I set up similar negative and abstention patterns, and work out a distance-based matching scheme so each country mention gets paired with its nearest cue word, using sentence and clause boundaries (splitting on semicolons, "while," "whereas," "but," "however") to keep the matches contextually correct.

I should flag negation if detected within about 15 characters before the chosen cue (like "did not vote in favour"), marking it as NA with a note explaining the ambiguity, since that's the more honest approach.

For the written claim text, I'll format it as the span covering both the mention and cue, taking the minimal substring from whichever starts first to whichever ends last so the snippet reads naturally — though for list-style claims like "Brazil, India and Kenya voted in favour," the span will cover the whole list even though only one country is being labeled, which is a bit ambiguous but acceptable.

For the recorded vote outcome, I check the ISO code against the vote data: if there's a letter code, I phrase it as voting in favor/against/abstaining; if the country isn't in the roll call or the votes object is empty, I mark it as not applicable with an explanatory note. Repeated mentions of the same state get treated as separate claims rather than deduplicated, and unchecked sentences are those where no claim's mention index falls within the sentence span.

I'm sorting all claims by their absolute position, then rendering the results table with color-coded verdicts (green check for matches, red X for wrong, grey question mark for unverifiable) alongside text labels so it's not color-only. I also want a summary line tallying matches/wrong/unverifiable, a note clarifying that "cannot be checked" doesn't mean "wrong," a limitations box explaining what the checker does and doesn't cover, and a fallback message listing what kinds of claims it looks for if none are found.

Now I'm laying out the page as a single-column, card-based structure capped at 1000px wide, keeping the whole thing under 700 lines by aiming closer to 400: a header and data line, a card for choosing a resolution with a filter input and dropdown, a card for the briefing text with buttons to request an AI briefing or stop waiting, a notice explaining what gets sent plus a collapsible exact prompt, a textarea and check button, and a hidden results card for section three.

I'm deciding to use a sized listbox select (around 7 rows) so people can browse resolutions easily rather than a tiny dropdown, especially useful on a projector. I'm also adding logic so that changing the selected resolution clears prior results and warns the user if there's leftover briefing text that was written for a different resolution, plus disabling the ask button when nothing is selected. I'm writing a small roll-call tally function that counts Yes/No/Abstain votes from a record's vote map, and now I'm starting to render the record card itself.

For the AI ask flow, I'm writing an async function that increments a token to handle cancellation, calls the studio helper, and fills the textarea with the result while marking its origin as AI-generated; if the studio helper isn't available I show a fallback message suggesting the user paste text manually. I'm also drafting the actual prompt text asking for a ~250 word briefing on the resolution, including adoption details and voting breakdown, with an instruction to admit uncertainty rather than guess—which feels like good practice for honesty.

Now I'm sketching the claim-finder: it splits the text into sentences, tracks which spans are already claimed, and adds detected claims to a list, along with a sentence splitter that handles abbreviations and punctuation edge cases so it doesn't split on things like "Mr." or "No.".

Still refining the abbreviation regex...

Still refining the regex patterns...

Refining the regex patterns...

Still writing detection patterns...

I'm now sketching a helper function that validates count claims against the recorded roll-call data, comparing extracted yes/no/abstain numbers against the official record for each match found.

For displaying dates, I'm building a month-lookup table matching abbreviated and full month names so I can parse date claims in various formats like ISO, day-month-year, or month-day-year ordering.

Still writing date pattern matchers...

I'm also double-checking that month abbreviations like "Mar" don't accidentally match inside longer words, making sure the boundary conditions behave correctly across both date orderings.

Still writing verdict logic...

Now I'm structuring the output rows, tagging claims with their source attribute and context sentence, sorting by position, and identifying any unchecked sentences that don't overlap with a claim's position range.

I also need a "checked against" reference line linking to the official record or roll call, then I'll finalize the HTML/JS—escaping special characters safely and building a helper to link document symbols to their URLs.

Now I'm writing a function that builds a list of country names and aliases mapped to ISO codes, then compiles them into a single regex with word boundaries to detect state claims in text, sorting names by length so longer matches take priority.

For each sentence I'm working out offsets by slicing the original text at the sentence's start and end positions, then splitting the sentence into clauses using punctuation and connector words like "while," "whereas," "but," and "however" as cut points.

Within each clause I'm scanning for voting cue words (support/favor terms for yes, against/opposed/rejected for no, abstain-related terms for abstention) and then matching nearby country mentions to whichever cue is closest.

I realize there's a risk: a phrase like "resolution adopted with 29 votes in favour" could falsely attach "in favour" to a nearby country mention even though that's just a vote-count statement, not an individual country's position. I should exclude cues that overlap with count-claim spans by checking their position against the spans I already tracked for numeric vote counts.

For linking a country mention to its nearest cue, I'll compute distance based on whichever comes first, break ties by preferring the cue that comes after, and cap the max allowed distance (maybe 200 chars) so distant cues in long country lists don't get wrongly matched to the wrong clause.

I also need to handle negation — checking a short window of characters before the cue word for terms like "not," "never," or contractions, so phrases like "did not vote against" get excluded. Then the actual claim text gets extracted by slicing from the earlier of the mention/cue start to the later of their ends.

Now I'm working out how to display results: labeling the claim type with the country name, showing the claimed vote next to the recorded vote text, and laying out the verdict columns with a note underneath, followed by a summary and an explanation of how the computation works. I'm estimating the total output length and planning the CSS variables and table styling needed.

I'm setting color-coded classes for matched, wrong, and not-applicable vote states, along with grouped lists for roll call details. I'm also building the header dataline showing the title, vote counts, year range, and source, handling cases where recs or source data is missing, and setting up the filter dropdown logic to preserve or default the selection.

For the selection change handler, I'm updating the current record and re-rendering, with option labels formatted to show symbol, year, amendment status, and truncated title. I'm noting a potential bug with regex objects needing fresh flags per call, and now writing the claim-counting logic with key mappings for yes/no/abstain votes.

Still writing claim-counting logic...

Then I'm handling the roll-call mismatch edge case where official counts could be zero but no roll call exists, pushing claim objects with type, position, sentiment, and verdict data, and finalizing verdict labels as "Matches," "Wrong," or "Cannot be checked."

Writing vote-pattern regex...

I'm adding a scan for consensus/unanimous vote phrases, then handling dates, year-only mentions, and sessions before states since those need span matching last. I'm writing a helper to convert number words or digits into numeric values, and separate regexes for session numbers written as digits versus spelled-out ordinals.

Still writing session logic...

I'm defining the judgment logic for session matches: it checks if the session is special (marks as not applicable), verifies the sentence context mentions voting or council action, extracts the recorded session number, and compares it against the expected number to decide match, mismatch, or no-session-found cases.

Alright, time to just write out the full solution now.

