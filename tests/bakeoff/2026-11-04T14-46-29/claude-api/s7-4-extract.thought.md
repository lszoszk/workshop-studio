I'm planning a single HTML file under about 1500 lines, with a header, a left rail, two tabs, and a footer. I'm also counting clickable elements per view to keep it to roughly seven, and the first tab comes to about six or seven once I include the header link.

Still writing the code for the document parsing and the credits footer...

I'm sorting elements into the cover, which is the first table and everything inside it, and flagging any other table as unclassified. I'll collapse whitespace in the text so the parsing stays predictable.

I'm working out how to classify the parsed elements, with the paragraphs matched by their leading number and the headings split into a roman or letter label plus the rest. I'll check the title against the first h2 and handle the regex edge cases, like a heading that has no space after the label.

I'm settling the heading split: the part is the nearest roman-numbered h2, and each section is its full heading text with a label and a space after it. For glued labels like "I.Introduction", I'll insert the space while splitting so the displayed heading reads correctly.

I'm handling the rest of the section path and the paragraph and heading fallbacks, plus setting up the repair rules for sentence joins, comma spacing and quotes, with context logged for each change.

I'm adding the dash repair rule, which puts a space after an en dash when a letter follows it, and I'm running each repair with a function that records the offset and surrounding context before it returns the replacement.

I'm weighing how to mark the inserted spaces in the expanded view, since tracking indexes through sequential replacements gets messy. Searching the final text for each after-snippet is simpler, though it could match the wrong spot if the same context repeats.

I'm writing the repair step for the expanded view, tracking each inserted space by its replacement text and searching the final text for it in order. Where the same snippet appears more than once, I'll match them sequentially so each highlight lands on its own spot, and I'll skip any that can't be found.

I'm settling the footnote count next: I'll look for superscripts and in-page anchor links, and report that number rather than hardcoding zero. The reference first-words check will compare normalised text, with curly quotes straightened and dashes and non-breaking spaces standardised, and it will be skipped when there's no reference.

I'm weighing whether to count footnotes by selecting sup elements and footnote-style anchors, since reporting a hardcoded zero would be wrong if the file has any superscripts. I'll count those matches and report the real number instead.

I'm listing the checks next: paragraph count against the reference, numbering that should run 1 to n in order with any gaps or duplicates flagged, the first-words comparison, footnotes, and the repair log.

I'm settling the final checks: paragraph count, numbering in order, the first-words comparison, footnotes, heading totals, a check that nothing is lost across the classes, and an export round-trip. Footnotes are reported as a source limit, not a failure, so the header will show how many of the eight checks pass and how many fail.

I'm settling the header status line and deciding how to label the checks that didn't run, then working out what the rail card should say. Since the title isn't reliable as a short label, I'm weighing whether to derive a name from the document instead of truncating it.

I'm working out how to present the document's own title: the header will use D.title, and the Markdown and JSON output will fall back to the parsed title when D.title is missing.

Now I'm settling how the expanded view marks the inserted spaces, matching each repair to its spot in the final text. I'm also deciding how to derive the header and export titles from the document.

I'm laying out the results panel as a 2x2 grid of tiles, one each for paragraphs found against the reference count, first-words matches, footnotes, and restored spaces. Below the tiles I'll list up to ten mismatches, and the actions at the bottom will be two download buttons, one for JSON and one for Markdown.

I'm setting the Markdown layout: front matter first, headings as ## and ###, and each paragraph opening with its number in bold. I'll build one ordered list of heading and paragraph blocks so the export follows the document's order.

Next I'm setting the download step: a JSON blob named after the symbol with slashes swapped for dashes, and the button disabled when there are no paragraphs. The two collapsible headings for the checks and the restored spaces will open independently, and each check line will carry its name, a story comparing expected to found, the values, a status word, and a link.

I'm laying out the spaces table next, with a button in the Paragraph cell and the whole row clickable, showing the before and after text for each restored space.

I'm laying out the spaces table with before and after snippets for each restored space, and setting the paragraph tables to label themselves in the order their tabs appear.

I'm writing the expanded row for each paragraph as a detail line that holds the path, the full marked text, and the reference-versus-found words, with a copy-citation button.

Now I'm writing the clipboard fallback and the headings box on tab 02, which is a button with aria-expanded controlling a panel, and I'm listing each heading's level, label, and text.

I'm laying out the rail and main areas: a 240px rail on the left, with tabs and panels on the right, stacking below 800px. The header will carry status dots, and the footer will show the source and a build date if the data includes one.

I'm settling the header and footer details: the symbol link, the adoption date and source when present, and a build date only if the data includes one. I'll handle the missing-reference case by showing "no reference in this file" on the tiles and marking the checks as not run, and I'll disable the exports when there are no paragraphs or the HTML is missing. For the nothing-lost check, I'm counting elements by class and comparing the sum against the total, with anything unclassified listed in red.

I'm checking the heading count next: h2s other than the title and h3s, with any label that runs straight into its text without a space after the dot counted separately.

I'm working out the stats next: the paragraph count, plus how many first-word checks match, measured against the reference paragraphs.

I'm working out the missing-paragraph case: if the reference has no first-words data, the tiles will say so, and any paragraph without a reference entry will count as a mismatch with the reference shown as empty. I'll also list reference paragraphs that never appeared in the found text as not found, so the mismatch list covers both directions.

Writing the JavaScript for the page now...

Writing the parser and counts for the document's elements now, with the class totals ready to check against the element count.

Now I'm working out how to tell apart the table that holds the cover and any other tables, and I'm counting each element by its class so the totals can be checked against the element count.

Writing the heading objects next: each one keeps its level, label, text, and whether it's a Roman-numeral part heading. The title is excluded from the heading list.

Now I'm working out how to handle the repair function for each paragraph, applying the rules in order and logging each change.

Now I'm writing the repair step for each paragraph: it applies the rules in order, and each replacement gets logged with the text around it, both before and after.

Writing the first-words normalizer now: curly quotes and apostrophes get straightened, en dashes and non-breaking hyphens become plain hyphens, and non-breaking spaces turn into regular ones.

I'm working out the record fields for each paragraph: the symbol, paragraph number, section and part, text, the first-words match flag, a citation, and the document link. For the limitation note, I'll say there are no footnotes in this HTML version, and give the reference footnote count if there is one.

I'm checking the first-words comparison now: any reference paragraph missing from the found text gets counted and listed alongside the mismatches.

I'm working on the HTML viewer's result tab, which compares the paragraphs and headings the app found against the document's reference counts.

I'm laying out the results page's verdict tiles and the two collapsible check sections, with each check showing its name, the expected and found values, a status word, and a link back to the paragraph.

Still writing the table markup...

Still writing the expandable row markup, with the full paragraph text marked up and a found-versus-reference comparison beneath it.

I'm working out how to find each repair in the paragraph text, so the marks land on the right spots.

I'm wiring up the tab keyboard controls and the citation copy buttons, with a function that will download the exports as files.

I'm writing the Markdown export now: YAML front matter with the title, symbol, adoption date, source link, and found-versus-expected paragraph counts, plus the footnote note. The body will hold each paragraph numbered in bold under its section heading. The filename will be the symbol with slashes swapped for hyphens.

I'm working out the status line: failed checks in red, and if everything passes, a green dot with the pass count, or grey if some checks haven't run. Source limits get their own red count.

Next I'm writing the first check, the paragraph count, which reports "no reference in this file" if there's no reference count, passes on a match, and otherwise fails and links to the results table.

I'm checking the numbering next: the paragraph numbers should run 1 to n in order, so I'm looking for gaps, duplicates, and out-of-order entries, listing the first ten problems if any turn up. Then the first-words check, which lists any mismatches against the reference. Last, the footnote count, which passes when the found count matches the reference.

I'm wrapping up the checks now: the repair count passes as a log of the spaces restored, the headings check fails if none were found, and the footnote count is a source limit rather than an app error. The last two items cover whether everything was accounted for and whether the round trip holds, and I'm noting the h2 count includes the title.

Now I'm writing the tile for the spaces restored, and the notes explaining how each count is computed.

Now I'm finishing the stylesheet: the status colours, a visible focus ring, collapsed table rules, right-aligned paragraph numbers, and a narrower side column on small screens.

Now I'm sketching the export and verification logic: the Markdown front matter, the filename derived from the symbol, and a set of checks covering paragraph count, numbering, first words, footnotes, and headings.

Writing the table row markup now, with each paragraph's number as an expandable button and its section, first line, and first-words check beside it.

Now I'm wiring the table rows so each one expands on click, with a toggle that updates the button's expanded state.

Now I'm wiring up the tab rows and the expandable details, toggling each row's detail on click and updating its aria-expanded state.

Now I'm laying out the sidebar: the document's symbol and title, a paragraph count of 90 against the reference of 90, and a footnote line showing none in this HTML version.

Now I'm finishing the header line: the symbol links to the document, followed by the adoption date and the source.

