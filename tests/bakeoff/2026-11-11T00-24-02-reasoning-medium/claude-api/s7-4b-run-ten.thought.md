I'm restructuring the pipeline around a per-document analyze(doc) function, which means rewriting most of the file, so I'll output the complete HTML rather than a partial patch. The data design is taking shape: each record carries its symbol, committee, year, title, doc URL, count, page texts, and reference, with the source and built fields coming from the document level and the adopted value taken from the reference.

Next I'm defining analyze(D) to take over the per-document work, pulling symbol, pages, and reference from each record and handling the case where footnotes are null. The three tabs and the keyboard navigation need to extend to cover all three, and the rail will list the ten documents as buttons with the selected one marked.

I'm now writing the analysis as a single analyze(D) function that returns all the per-document results: paragraphs, headings, events, checks, warnings, and the record and markdown outputs. The markdown will get a shared front matter, with each document's body built separately under its own heading.

Now I'm setting the rail to select documents by index, with the header and footer tied to the chosen one. The table cells will go red only where a check actually fails, and the table will be built from the current analysis.

Now I'm wrapping each document's analysis into a single pass, with everything computed up front for all ten. The JSON export will combine every record, and I'll keep the per-document round-trip check.

