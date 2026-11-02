I need to plan a single HTML file around 700 lines that works with the UN library records data, where each record has paragraphs with cited articles. I'm thinking through how to deterministically match concept terms like "proportionality" against the text in a case-insensitive way.

For simplicity, I'll define a set of known concepts with their variant spellings, and for user-typed search terms, match the exact phrase case-insensitively with flexible whitespace and hyphen handling, plus basic plural support. I want the UI to be honest that this is literal text matching, not semantic understanding, and I'm working out how to normalize different hyphen characters into a flexible regex pattern.

For related concepts, I'll show other sidebar concepts that co-occur in the same paragraphs with counts and links, plus small chips showing cited articles per paragraph. The sidebar will let users add and remove their own concepts (kept in memory rather than persisted), and the page will show paragraph and document counts.

For each paragraph I'll group by document with a header linking to the source, then show individual paragraph entries with a button to jump to that location in studio, and the verbatim text with matches highlighted using safe DOM construction rather than string manipulation. For long paragraphs I'm weighing clamping with a "show more" toggle against always showing full text, since clamping risks hiding highlighted matches.

For the summary feature, I'm designing a "Draft a summary" button disabled when there are no paragraphs, which deterministically selects up to 12 paragraphs round-robin across documents, with on-screen text disclosing how many of the total were sent and that the data leaves the browser. The prompt instructs the model to write three sentences, each citing (SYMBOL, para. N), using only the supplied text, without JSON output.

I'm labeling the rendered output as AI-generated and advising the reader to check it against the source paragraphs, showing how many paragraphs were used out of those found. Rather than allowing cancellation mid-request, I'll add a cancel button that simply ignores the eventual result, and I'll cache summaries per concept so switching pages shows the cached version without re-calling the model on load. For rendering, I plan to escape the summary text safely and then make the embedded citations clickable, linking each one back to its source paragraph.

I'm parsing citation patterns like "(SYMBOL, para. N)" using a regex, turning matches into links when the referenced paragraph actually exists among the sent set, and flagging citations that don't match as suspicious with a "bad" class — a small honesty check. For related concepts, I'll show them as chips with shared-paragraph counts, placed below the paragraph list per the spec, with the page ordered as: title, methodology note, summary box, paragraphs grouped by document, then related concepts.

I'm skipping hash navigation and sidebar search for now. I'm designing the concept data structure with name, variants, and a builtin flag, computing matches lazily with a flat array of all paragraphs tagged by symbol and index, and deriving related concepts from shared paragraph-id sets. For highlighting, I need to use matchAll instead of exec to avoid regex global-state bugs. The header will show the title, source, document count, year range, and total paragraph count.

For user input, commas separate multiple variant wordings, and I'll note that matching is literal wording when a concept has no matches. The layout uses a sticky 280px sidebar next to the main content, stacking on narrow screens. Building the data structures and escape-safe regex helper now...

Adding more variant patterns...

I'll settle on "non-State actor" and "non-State entities" as the final variants. For the remaining concepts, I'm defining variant lists for proportionality, deprivation of liberty, surveillance, legal capacity, reasonable accommodation, and access to information, then writing a function to build regex patterns from these variants and scan the flattened text for matches.

For each concept I'm computing related concepts by finding shared document hits, sorting by overlap count, and wiring up chip clicks to select related concepts. I also need to handle concept ID slugs, reject duplicate names, render the sidebar with counts and active highlighting plus removable chips for custom concepts, and group the matched hits by document in their original order for the main display.

For each paragraph I'm rendering a button to jump to the source PDF page, article citation chips, and clamped text with highlighted matches that can expand if too long, falling back to an alert if the PDF viewer integration isn't available. For the summary feature I'm tracking per-concept state (text, sentence counts, status) and showing a notice before the user clicks that explains the text will be sent to a language model, with a running "Asking…" state and cancel option.

I'm designing the paragraph selection logic to round-robin across document groups up to 12 items, then ordering them for the prompt, which instructs the model to write exactly three sentences about how the paragraphs treat the concept, citing each sentence with the paragraph's symbol and number, using only the given text without outside knowledge, and truncating each paragraph to a fixed character limit.

I'm writing a regex to parse citations like "(SYMBOL, para. N)" from the AI's output, cross-checking each against the set of paragraphs actually sent, flagging any citation that doesn't match a sent paragraph as suspicious, and adding a verification line summarizing how many citations checked out. I also need to wrap the whole thing in error handling to display a message if something fails, and then style the result.

