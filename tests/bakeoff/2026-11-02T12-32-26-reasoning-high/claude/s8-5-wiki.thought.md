I need to keep the app under roughly 700 lines, so I'm mapping out the key concepts and their matching search terms, like mental privacy, freedom of thought, and self-incrimination, keeping the term lists simple by mostly using the concept name itself.

I also need to handle text normalization carefully — whitespace, hyphen breaks, and special hyphen characters — so matches like "self-incrimination" work across line breaks, and so substring matches like "consent" catching "consented" still work fine for concepts like neural data, data solidarity, proportionality, and lie detection (which needs synonyms like deception detection and brain fingerprinting). I'm also planning how added concepts get tracked with their own terms, how the sidebar counts occurrences, how related concepts get linked by co-occurring passages, and how the kind-based table should be ordered.

I'm working through how documents group passages in library order, how citation links should call into the studio viewer safely with an existence check, and how to format citations differently depending on whether a document has a symbol and paragraph number versus just an author, year, and page. I'm also figuring out author name parsing rules — splitting multiple authors on "and" or commas, abbreviating three or more authors as "et al.", and keeping non-journal document authors exactly as written.

For passage text display, I'm planning a line-clamped preview with a "Show more" toggle that only appears when the content actually overflows, detected by comparing scroll height to client height.

I'm leaning toward skipping highlighting of matched terms to avoid regex complexity with line breaks and word variants, but recognizing it would help users see why a passage matched — like distinguishing "deception detection" from "lie detection."

Still building the regex pattern...

I'm planning to precompute matches per concept against the flattened passage list, then handle the "add concept" flow where typing a term and pressing Enter either selects an existing concept or creates a new one with that term, displayed under a "Terms that find it" heading, alongside a "Draft a summary" button.

Clicking that button sends the first 12 passages to the model, with a clear disclosure beforehand ("text leaves browser") and an after-the-fact label confirming how many passages were sent. I'm adding a waiting state with a stop control that just ignores the result, clearing the summary whenever the concept changes, and marking the answer text with a data-source="ai" attribute so its origin stays visible.

As a lightweight verification layer, I'm thinking of splitting the answer into sentences and checking whether each one's trailing citation actually comes from the passages that were sent—then surfacing a simple count like "x of y sentences cite a sent passage" rather than building anything more elaborate.

For the UI, I'm sketching a sidebar-plus-main layout that collapses on narrow screens, with a header summarizing the source, document count, passage count, and years. I also want a "Passages by kind" table with totals, an explanatory note on how the numbers are computed, and a "related concepts" list ranked by how many passages they share with the current concept, falling back to a message when nothing overlaps.

Each citation entry needs a short title, kind, year, and either a symbol link or author fallback, plus a clickable citation link that opens the source PDF at the right page, guarded with error handling in case that data is missing. For long passages I'm adding text-clamping with a toggle to expand or fold, checking overflow after the DOM renders, and being mindful that concepts like "consent" could have hundreds of matching passages, so I want to batch the overflow measurements to avoid excessive forced layouts.

I'm setting up the concept state structure with cached regex matches computed lazily, building the sidebar from the library data, and writing helper functions for regex escaping and case-insensitive matching across both highlighted and tested text. Writing concept match logic...

I'm also writing a surname extraction function that splits author strings by commas, semicolons, and "and", grabbing the last word of each name, and formatting the result as "Last & Last" or "Last et al." depending on how many authors there are, though I notice edge cases like single-letter initials could break the last-word heuristic.

For citation formatting, I'm building a helper that checks if a paragraph number exists and uses the document's symbol or author label plus "para. X", otherwise falling back to author plus year plus page label. Then I'm setting up a table that groups hits by document kind in the order they first appear, counting hits and unique docs per kind, with zero-count rows shown as muted.

Now I'm drafting the summarization prompt itself: it instructs the model to write exactly three sentences about the shared concept across the numbered passages, grounding each sentence strictly in the provided text and ending it with the exact citation copied from brackets, without adding outside knowledge. I need to decide whether to truncate long passage texts before sending them in the prompt, since some documents could be quite lengthy and might need a length cap to keep things manageable.

I'm planning the HTML structure now: a heading for the concept, a sidebar of related search terms with sensible defaults per concept (lie detection synonyms, self-incrimination, etc.), an input to add custom concepts with a note that they won't persist on reload, and a render function that resets summary state and wires up click handlers for the term buttons styled as links. I'm sketching a small DOM helper to keep the markup generation tidy as I write this out.

Writing highlight logic...

