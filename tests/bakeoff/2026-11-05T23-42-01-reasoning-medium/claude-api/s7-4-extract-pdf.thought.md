I'm starting on a single-file app and sketching out the data shape first: a pdf_text object with title, symbol, doc_url, source, count, records, reference, and an optional built field that the footer should handle if it's missing. Then I'm planning the pipeline, beginning by sorting pages by page number and splitting each page's text into lines to classify the non-empty ones.

I'm working through the header and footer checks for each page: a header line matching the symbol gets dropped, and I'm stripping footer lines from the bottom up (empty lines, GE. references, 6-digit groups, bare page numbers) until I hit real text. The footnote numbering and page-number cases are settled, so I'm moving on to building the body lines with their page tags.

I'm now setting up the parse loop over the body lines, keeping blank lines in the list but skipping them during matching. Before handling each paragraph start, I'm planning a pre-pass that marks heading lines by looking ahead, so a heading never ends up attached to the previous paragraph.

I'm working out how to tell a labelled heading apart from the paragraph text under it: a roman numeral or capital letter followed by a period starts a heading, and the lines after it run until the next label or paragraph start. The tricky case is an unlabelled heading that sits right after a labelled one, since it could get swallowed into the same block.

I'm weighing how to treat a labelled heading's wrapped title: lowercase or parenthesised lines continue it, while any further lines would start a separate unlabelled heading before the next paragraph.

I'm settling the heading rules: a labelled heading keeps its wrapped title lines, and any extra non-wrapping line becomes its own unlabelled heading, which I'll list separately.

I'm labelling the heading entries with their level, which is roman for level 1 and letter for level 2, and noting the page and line indices for each. I'm also checking whether a letter like "I", "V", or "X" could be a roman numeral, though letter subsections past D or E are rare enough that the simple roman match should hold.

I'm checking the paragraph-start line, looking back to the last non-empty line before it to see if it could be an unlabelled heading. It qualifies only if it's under 90 characters, starts with a capital, and doesn't end in punctuation or a digit, since a trailing footnote number would mean it's just the end of a paragraph.

I'm checking the paragraph-start case now: a line just before it could be a footnote, but footnotes begin with a digit and so fail the capital-letter test, and a stray capital-starting footnote line is an accepted risk that would show up in the headings check. I'm also considering whether the line before that candidate could be a second wrapped heading line, applying the same test to it.

I'm checking whether a line just before a paragraph start is an unlabelled heading, and if so whether the line above it is a second wrapped heading line, using the same length and capital-letter tests. Lines already marked as heading text are skipped, so the labelled-heading consumption won't cause a double match.

I'm settling how the unlabelled headings after a labelled one get split: continuation lines like lowercase or parenthesised text stay with the heading above them, and the rest are grouped together as a new heading.

I'm weighing whether the wrapped title of a labelled heading should take in every line up to the paragraph start, since the second line could be lowercase and clearly a continuation, or a capital-starting line that would be better kept as its own heading.

I'm settling how the wrapped title of a labelled heading is handled: the first line plus any lowercase or parenthesised continuations stays as one heading, and any further standalone lines become their own unlabelled headings. I also want the section tracking to walk the lines in order so each paragraph gets the right current section.

I'm settling how the section path is built: the most recent labelled heading becomes the part, a lettered subsection is tracked separately, and any unlabelled heading is the section, with the path joined by arrows from whichever of those are present.

I'm now writing out how to detect suspect lines inside a paragraph: a line that's just one to three digits, or starts with digits then a space and a capital letter, a UN document symbol, or a quotation mark, gets flagged for review.

I'm checking how a footnote block at the bottom of a page affects paragraph boundaries when the next page opens with a heading and a new paragraph. The footnote lines would sit just before the heading, so they should attach to the prior paragraph rather than the new one.

I'm checking the footnote case: a bare number line followed by text gets flagged, and footnote lines at the bottom of a page stay with the paragraph above them. The remaining concern is a footnote tail line that happens to start with a capital letter and could be mistaken for the first line of a two-line heading on the next page, which I'm accepting as a minor risk.

I'm deciding how to flag the pages: a page gets flagged when one of its paragraph lines looks like a footnote, and each flagged row lists the page, the paragraph numbers involved, the count of suspect lines, and the reason. Paragraphs over 300 words get their own flag, separate from the page flags.

I'm settling the flag rule: a page is flagged only when it has a suspect line inside its paragraph text, and the over-300-word paragraphs get noted in the paragraph listing instead of adding page rows, so the flagged-page count stays strict.

I'm deciding which pages get flagged, keeping the check strict: a page counts only when a suspect line sits inside its paragraph text, and long paragraphs get noted in the paragraph listing rather than adding page rows. Next I'm planning the flagged-page table, where each expanded row will show that page's raw lines with the suspect ones highlighted, which means keeping a per-line classification for every page.

I'm turning to the normalisation step for the first words: tokenising each line on whitespace and stripping out any standalone footnote digits that appear right after a token, so the opening words of each paragraph come out clean.

I'm settling how the first words of each paragraph are cleaned: stripping stray footnote digits from tokens, but keeping abbreviations like "No." or "art." intact, and being careful that document symbols such as "E/C.12/GC/27" don't get mangled by the digit-stripping rule.

I'm working out how to clean up the first few words of each paragraph: stripping footnote digits glued to the end of a word or punctuation mark, leaving abbreviations like "No." and document symbols alone, and only applying this to the leading tokens.

I'm checking whether the first six cleaned words match the reference, normalising curly quotes and dashes on both sides, and I'm keeping abbreviations like "No." intact while dropping stray footnote digits.

I'm checking the citation format next, which is the symbol followed by ", para." and the paragraph number. Then I'm setting up the checks list, where each entry has an id, label, expected and found values, a status, and a link to the concerned rows; a failed check will link to the first affected paragraph in tab 02. Finally I'm noting that tab 01 should be reachable in two clicks down from the top.

I'm weighing whether the pass count should include the flagged-pages check, leaning toward treating it as a warning rather than a failure, so only the deterministic checks feed the "pass" total.

I'm weighing how the header should read when the flagged-pages check isn't a true failure: it should count as neither a pass nor a fail, so the green "n of m checks pass" line stays accurate while the flag appears separately.

I'm settling the flag check's status so it doesn't count as a pass or a fail: it stays informational and is left out of the total. The header will then show red for failures and green for a clean run, and I'm starting on the checks list with the paragraph count, which needs the reference paragraph number.

I'm moving on to the checks list: paragraph numbering should run 1 through n in order, with any gap or duplicate reported against its page, and the first-words comparison will count mismatches against the reference, including paragraphs the reference doesn't cover. Headers and footers are next, where every page should carry its symbol and every page except the first should show a page number.

I'm laying out the remaining checks: the Headings check is informational and lists unlabelled headings in its detail, the nothing-lost check passes only when every paragraph is classified, and the export round-trip re-parses the JSON on load to confirm the paragraph count. Hyphenated line endings get counted as an informational check too.

I'm working out the tile counts and the mismatch list: how many found paragraphs match their reference first words, and for any reference number with no matching found paragraph, listing it as not found.

I'm settling the tile counts and the mismatch list: matches among the found paragraphs divided by the reference count, and any reference number with no matching paragraph gets listed as not found. The export will be JSON with symbol, paragraph, section, page range, text, the flag, the first-words match, citation, doc URL, limitations and the text_lines field with lines joined by " | ", leaving out text_raw since it duplicates text.

I'm setting up the markdown export: the front matter, then headings and paragraphs interleaved in document order, with roman-numbered headings as level-two and the rest as level-three. For the download, I'm building a Blob and naming the file from the symbol with slashes swapped for dashes, and I'm checking that an anchor download should work in the sandbox. Last, I'm planning the citation copy button around the clipboard API with a fallback.

I'm setting up tab 02 as a table with a caption and a button in each row's number cell that toggles a hidden detail row, which will carry the aria-expanded state. I'm also making the whole row clickable for mouse users and using a hidden attribute on the detail row, so it stays out of view until opened.

I'm rendering the paragraph detail for each row, marking suspect lines in their own spans and joining the rest so the text matches what's in the file. I'll also show the reference and found first words side by side, plus a toggle that reveals the raw PDF lines with page markers. Rendering the details lazily on expand should keep all 90 rows manageable.

I'm laying out the flagged-pages view next: a row per flagged page that expands to show its raw lines with the suspect ones highlighted, along with the paragraph each sits in. I'm also planning the header status and the document rail with its headline numbers and pass count.

I'm working out how the expanded paragraph detail should link back to the checks: a failed check will get a "see rows" button that jumps to tab 02 and opens the affected paragraphs. I'm also setting up the tabs with proper tablist roles, roving tabindex, and arrow-key navigation.

I'm working out the remaining details: tab panels get the hidden attribute so they're not focusable when closed, the footer falls back to "built: not stated" if the build date is missing, and I'm guarding against a missing records list. Page ranges will read as "3–4", and the first line in each row gets trimmed to about 120 characters, cutting at a word boundary when one is available.

Writing the record pipeline now: sorting pages, splitting text into lines, and classifying the non-empty ones...

Writing the footer and page-number detection next, scanning each page from the bottom for a GE number or a bare number to check against the page.

Now I'm checking each page from the bottom for a GE number or a bare page number, and setting aside any footnote numbers that don't match the page.

Next I'm handling the footer and body split: lines that are header or footer get marked and set aside, and the rest go into the body list, keeping blank lines in place. I'm also counting body lines that end in a hyphen as an informational check.

I'm defining the heading check so it only treats a line as a paragraph start when it's the next non-empty line after the heading, with blank lines ignored. I'm writing the regex patterns for paragraph numbers and a helper that pulls out the number and any text that follows it.

I'm working out how to tell the paragraph-start lines apart: a regex matches a number followed by a period, with or without text after it, and a separate pattern picks up roman-numeral or single-letter labels for headings. I'll mark each line's role in an array, then look at what comes before the first real paragraph start, since the labelled headings sit there too.

I'm working out how to tell the cover from the body: the cover runs up to the first heading label or paragraph start, whichever comes first. I'm also noting that the page-1 footnote with the asterisk likely sits after the first paragraph, so it gets flagged under the rules, and I'm checking how the wrapped title line on the cover should be read.

I'm finishing the cover detection: the cover runs up to the first heading label or paragraph start, and I'm marking those lines before it. Then I'm stepping through the remaining body lines to pick out headings and paragraphs.

Continuing the paragraph loop, I'm stepping through the remaining body lines: when a line opens a numbered paragraph, I start a new record with its number and any text that follows on the same line, and I'm tagging the page each line came from.

I'm handling the heading lines before each numbered paragraph, marking a label line as a heading and gathering the lines that follow it until the next label or paragraph start, while planning to cap how many of those lines count as heading text so no body text gets swallowed.

I'm grouping the heading lines into entries, where a line starting with a lowercase letter or parenthesis continues the previous entry, and the first entry takes the label while later ones are unlabelled. Then I'm marking those lines as headings and setting the heading level by whether the label is a roman numeral.

I'm settling how to spot unlabelled headings: a line counts as a candidate if it starts with a capital, is short, and doesn't end in punctuation or a digit. Then I'm checking the line just after it to see whether it opens a numbered paragraph, and I'll look two lines ahead for the case where the heading runs over two lines.

I'm now checking the candidate-heading rule in a fixed order: first whether a pair of short capitalized lines is followed by a paragraph start, then whether a single one is, so the two-line case is caught before the one-line case.

I'm settling the two-line heading case: when two short capitalized lines are followed by a paragraph start, they count as one heading, checked before the single-line case. I'm also noting that a wrapped line starting with a lowercase letter or parenthesis would not be picked up as an unlabelled heading under this rule.

Continuing the two-line heading check: the second line can also begin with a lowercase letter or parenthesis, so a wrapped heading still counts as one heading. Then the line-advance logic and the paragraph fallback follow.

I'm settling the heading entries: the first entry takes the label and later ones stay unlabelled, with the level set by whether the label is roman. Then I'm updating the section path so each paragraph picks up its current heading chain.

I'm marking the suspect lines on each paragraph: for each page I track whether a flag has started, and flag a line when it looks like a footnote, such as a bare number or a numbered note starting with a capital.

I'm checking which lines count as suspect footnote text on each page, flagging bare numbers, numbers followed by a capital or quote, and lines starting with an asterisk. Then I'm joining each paragraph's lines into one text and noting whether any line was flagged or the paragraph runs past 300 words.

I'm checking each paragraph's opening words against the reference first-words list, counting matches, and treating entries missing from the reference as unknown. Paragraph numbers can repeat, so each paragraph keeps its position in the array as its row id. For flagged pages, I'm collecting the paragraphs, a count, and the distinct reasons from the lines that triggered a flag.

I'm working through the final checks now: confirming that every paragraph number lines up in sequence, and that the classification counts add up to the total number of non-empty lines.

I'm checking the paragraph numbering: each number should follow the previous one, and a jump or a repeat gets flagged as a gap or an out-of-order entry. Then I'm laying out the page itself, a grid with a left rail and a main column that stacks on narrow screens, with a header showing a mono label, a serif title and a status on the right.

I'm working on the rendering for the first tab, with a found count tile showing how many paragraphs were detected against the reference total, colored by whether they match. The other tiles cover the first-word match count, the number of flagged pages, and whether footnotes were separated.

I'm now defining the accordion helper and wiring the check panel, where each check states what the data should show and what was found. Then I'm handling the interactions through a single document-level click handler that toggles the expandable sections.

I'm adding the paragraph detail view: a path line, the reference first words beside the found ones, the paragraph's spans, and a link to show the source PDF lines.

Checking how the paragraph detail view should show each paragraph's lines, with page markers and the suspect lines highlighted, and how the check column should flag mismatches.

I'm now writing the markdown export, starting with a YAML front-matter block that records the title, symbol, source URL, and paragraph counts, with footnote status noted alongside.

I'm wrapping up the markdown export and the page layout: each heading gets a level-two or level-three marker, each paragraph starts with its number in bold, and blank lines separate them. Then I'm moving on to the header line, the title, the metadata and the status on the right, plus a guard for when the file has no pages, and tab keyboard navigation.

I'm writing the word-cleaning helper now, which trims each token and drops stray numbers that trail a sentence-ending punctuation mark, with an exception for abbreviations like "No." or "para.".

I'm writing the helper that cleans each token, stripping stray footnote numbers stuck to the end of words while keeping abbreviations like "No." and "para." intact. I'm also checking whether a bare number following a sentence-ending mark should be dropped.

I'm adjusting the abbreviation check so it matches the whole previous token, including an optional opening parenthesis, and leaves words like "article" alone. A stray number after a closing quote and full stop gets dropped. I'm also normalizing curly quotes and dashes, collapsing whitespace, and trimming, and then capping the first words at six.

Writing the table...

I'm working out the tab 01 first-words list: for each reference entry in ascending order I check whether a paragraph with that number exists, marking it "not found" if not and listing mismatches, capped at ten. The match tile then counts reference entries whose paragraph's opening words agree, measured against the reference paragraph total or the number of keys if that total is missing.

Still rounding out the markdown export and the table layout...

