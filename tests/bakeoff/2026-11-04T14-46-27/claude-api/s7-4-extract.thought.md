I'm starting to build a complete HTML app and want to plan it carefully without overcomplicating things. I'm also checking which sources the plan drew on, since one of them is under an open licence and I may need to give it credit. No excerpts were supplied, so I'm weighing whether a short attribution line is needed or just harmless to include.

I'm laying out the app as a header, an always-visible left rail, tabs, panels, and a footer, and checking that each view stays under about seven clickable controls. Next I'm working out how to parse the document and classify the table and paragraph elements, so the cover content is handled separately.

I'm settling on how to tell the cover table and its paragraphs apart from the body: anything inside the first table counts as cover, and the first stray paragraph before the headings becomes the committee line. Other stray paragraphs go into an "unclassified" list so nothing gets silently dropped. For the body, I'm matching numbered paragraphs and Roman or letter headings with simple patterns, starting with the first h2 as the title.

I'm settling on how to pick out the body paragraphs: a paragraph counts as a numbered item when it begins with digits and a period, and a heading counts as a part when its label is a single Roman numeral in an h2. For each element I'm noting its nearest part and section, so the breadcrumb can show something like "IV. Heading › section" and fall back to just the section when the two are the same.

I'm now settling the repair step: each fix gets logged with its paragraph, the rule it came from, and about 20 characters of context on either side, and since earlier replacements shift later offsets, I'll apply the rules one after another rather than trying to track positions in one pass. I'm also deciding that heading paths stay as a stack, with the h3 cleared whenever a new h2 starts.

I'm writing the repair rules as a list of regex patterns, each with a label and a replacement function, and I'm planning to apply them one after another so offsets stay correct. For each match I'll log the paragraph, the rule, and about 20 characters of context on either side, using the string as it was before that replacement.

I'm now writing the repair rules as regex passes, with each match logged against about 20 characters of context on either side. I'm applying the rules in sequence so earlier replacements don't throw off the offsets for later ones.

I'm marking each inserted space with a private-use sentinel character during the repair passes, so I can recover the final positions afterward and swap the sentinels back to plain spaces.

I'm marking each inserted space with a sentinel character during the repair passes, then swapping those sentinels back to plain spaces at the end. The log context gets the same cleanup, and the log entries are ordered by paragraph and then by rule. For display, I'll wrap the inserted space and its two neighbours in a span with a thin red border.

I'm now comparing the first six words of each paragraph against the reference list, after normalising quotes, dashes and whitespace on both sides. If the reference has no entry for a paragraph, that check is marked as not run.

I'm running through the validation checks now: paragraph count against the reference, whether the numbering runs 1 to n in order without gaps or duplicates, and whether the first six words of each paragraph match. For footnotes, I'm comparing against the reference count, which I still need to confirm.

I'm settling on the footnote check now: counting elements that look like footnote markers (superscripts, footnote classes, and links or ids starting with "fn"), since the reference expects zero of them.

I'm adding the validation checks: the repair log should record that the raw text is preserved, meaning stripping spaces from both versions gives the same result. I'm also counting headings and checking that glued labels like "IV.Heading" were split correctly.

I'm finalising the validation checks: confirming the paragraph count and numbering against the reference, comparing the first six words of each paragraph, and checking that the raw text survives the repairs once spaces are stripped. I'm also verifying that every heading was classified and nothing was dropped, and that the JSON export round-trips to the same paragraph count.

I'm settling the summary header: a green dot showing how many checks pass out of those that ran, or a red dot with the failure count if any fail. Source limits get counted separately, and checks that couldn't run are left out of the pass count.

Next, I'm checking the first six words of each paragraph against the reference, which should flag six paragraphs where the words run together. Those mismatches are expected, so the header will show one failed check, with the wording adjusted for the count. I'm also planning the rail: a document card with each paragraph count shown as a bar against the reference, with the bar turning red when the count is short or over.

I'm now planning the tiles and the mismatch list: four tiles, each with a line on how it was computed, and up to ten mismatched paragraphs listed plainly, with the rest summarised. I'm also deciding that the link from a failed check goes to the second tab and opens the first affected paragraph, since the panel is closed by default.

I'm laying out the rest of the page: a tab for the checks and the spaces, with the checks in a closed panel and the spaces list under it. Each check gets a short story of what was expected and what was found, and the spaces tile shows how many were restored across how many paragraphs.

Now I'm settling the export format: each paragraph record carries its symbol, number, section and part headings, the text both cleaned and raw, a match flag for the first words, the citation, the document link, and any limitations.

I'm now setting up the Markdown export: front matter with the title, symbol, adoption date, source link, extraction date, and paragraph counts, with the footnote note carried over. Then I'll write the headings in document order as section lines and each paragraph with its number in bold ahead of the text, using a list of blocks to keep that order.

Next I'm settling the file names and download mechanics: the symbol's slashes become dashes, the JSON and Markdown files get their extensions, and a hidden anchor triggers the save. I'll also disable both export buttons when there are no paragraphs to export.

I'm laying out the paragraph table: each row's number cell holds a button with aria-expanded and aria-controls pointing at a hidden detail row, and the row click toggles the same thing. Pressing Enter on the button fires the click, which then bubbles up to the row, so I need to make sure the handler doesn't toggle twice.

I'm planning the paragraph table next: each row's number cell holds a button wired to a hidden detail row, and clicking the row toggles it too, with one handler on the row so Enter and Space don't toggle twice. The expanded view will show the heading path, the repaired text, and the first six words of the reference and the found text side by side, plus a copy button for the citation.

I'm writing the paragraph table's rows, where a long paragraph gets cut at a word boundary near 120 characters with an ellipsis, and opening a paragraph from the first tab will switch to the second tab and expand that row.

I'm handling the missing-data cases now: if the document data isn't there I'll show a message, and if the HTML yields no paragraphs the first tab says so and both exports stay disabled. I'm also setting up the tab keyboard support with arrow keys, Home and End, and building the page with a small element helper so inserted text is never parsed as HTML.

I'm laying out the page's structure now: a narrow left rail that stays visible, the main content to its right, and stacking below about 820px. The header carries the symbol, adoption date and source, and each check gets a short expected-versus-found story with a status.

I'm settling the repairs table: each row gets a paragraph number, the text before and after the fix, and the rule that applied, with per-rule counts shown above it. Clicking a row will open that paragraph in the second tab.

Now I'm building the paragraph table with a button in each number cell, and I'm making sure the row's click handler only toggles once so Enter and Space don't double-fire. Each expanded row will show the heading path, the repaired text, and the first six words of the reference and the found text side by side, plus a copy button for the citation.

Next I'm building the paragraph classification pass: walking the body's block elements in order so each one lands in exactly one bucket.

I'm writing the classification loop over the body's elements, skipping the cover table and sorting paragraphs by their leading numbers.

I'm now classifying each block in the body: skipping the cover table, sorting paragraphs by their leading numbers, and treating empty elements as their own bucket so the counts still add up to the total.

Now I'm settling the paragraph records and how headings get tracked: each paragraph carries its section and part, and a heading only counts as a part when its label is a Roman numeral.

I'm working out how the repair function applies each rule: it runs the replacements in order and logs what changed, with the paragraph's number and offsets kept for the before-and-after table.

I'm writing the repair pass: each replacement records what changed, and then I'm mapping the text so the spaces that were restored can be marked in the output.

I'm checking the footnote count and how the dash and comma rules interact with the sentence rule, then sketching the render functions and a status-badge styling scheme.

I'm laying out the styling now: a fixed-width left rail with the document details, and the main content taking the remaining space. The status colours will be green for pass, red for failures and source limits, and a muted grey for checks that weren't run.

I'm sketching the sidebar: a document card with a shortened title taken from the full one, and the paragraph count shown as a large number with a progress bar. I'm also setting up the tab panels in the markup and letting the script fill them in.

Still writing the helper functions for building the page elements...

I'm settling how each paragraph's first-word check is scored: if the reference has an entry for that number, I'll compare the opening words, and if it doesn't, the result stays unmatched. A paragraph the source has but the reference lacks should count as a mismatch rather than being skipped.

I'm working out the paragraph check now: any paragraph whose opening words differ from the reference goes on a mismatch list, and so does any reference entry with no matching paragraph in the document. That list gets sorted by paragraph number, and rows that were never found can't be opened, so the link for them will point to the first paragraph that was.

Now I'm wiring up the summary header counts and the first tab's rendering, including how each check's rows get computed.

I'm laying out the first tab's checks: the paragraph count, the first-words comparison, the footnote count, and the spacing rules, each with a short description and a status. Then the tab's heading asks whether the app found everything in the document, and the "Every check" and "The spaces restored" sections will start open.

Still writing the download helper and the export round trip. Once the JSON is built, I'll check that parsing it back gives the same number of records.

I'm sketching the markdown export next: front matter first, then each heading as a level-two or level-three line and each paragraph with its number in bold, leaving out the title heading. The headings tab will show the caption with the paragraph count against the expected total, and a closed panel listing the headings in order, indented by level.

Still writing the paragraph table: each row gets a button on its number, and the row's section, first line and check status sit beside it. The detail row for each one starts hidden and toggles open on click, showing the heading path, the text with its marks, and the reference against the found text.

Still writing the row toggling, the marked-text builder, and the tab switching; the open-paragraph link and the citation copy come next.

Still writing the clipboard helper: it tries the modern API first and falls back to a hidden textarea with execCommand if that fails. Then I'm adding the button's "Copied" feedback and the focus ring styling.

I'm wrapping up the footer and the no-reference case, where the tiles will say there's no reference in the file. Next I'm writing the HTML skeleton with fixed element ids, then filling it in with the script.

I'm now setting up the header tile and the first tab's paragraph comparison, colouring the share bar green when the counts match and red when they don't. I'm also finishing the final assembly, including the viewport meta tag.

I'm writing the mismatch list for the first tab, with each line showing the found text against the reference. Then I'll finish the final answer, keeping the text before the code to a few sentences.

