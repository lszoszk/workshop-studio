Let me understand the task. The user wants me to build an HTML app that:

1. Takes `WORKSHOP_DATA.pdf_text` (raw PDF converter text of E/C.12/GC/27, 20 pages)
2. Splits it into numbered paragraphs, removes headers/footers, flags suspect lines (footnote text inside paragraphs), checks against `reference`, logs repairs
3. Four tabs: 01 RESULT, 02 PARAGRAPHS, 03 FLAGGED PAGES, 04 CHECKS & METHOD
4. Left rail with document card
5. Header always visible with check status
6. Footer always visible
7. CSV download
8. Raw page viewer with colored lines

The data description says `WORKSHOP_DATA.pdf_text` is `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {paragraphs, footnotes, adopted, first_words}}`. Note the sample shows `pdf_text` as an array in the sample JSON, but the description says it's an object with `records`. The description says: "`WORKSHOP_DATA.pdf_text`: one UN document as raw text from its PDF — `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {...}}`". So I should read `WORKSHOP_DATA.pdf_text.records`. But the sample shows it as an array... The sample says "Sample records per dataset" — the sample shows `pdf_text` as an array of records directly. Hmm. To be safe, handle both: `const data = Array.isArray(WORKSHOP_DATA.pdf_text) ? {records: WORKSHOP_DATA.pdf_text, ...} : WORKSHOP_DATA.pdf_text`. Actually the description is authoritative: it's an object with `records`. But the sample shows an array. I'll handle both defensively: if `WORKSHOP_DATA.pdf_text.records` exists use it, else if it's an array use it as records, and get title/symbol/etc from wherever available. Also the app "is written so that every document in WORKSHOP_DATA with records and a reference gets its own card in the rail" — so I should scan all keys of WORKSHOP_DATA for objects with `records` and `reference`. That includes `pdf_text` and `pdf_text_2`. So the rail will have two cards: pdf_text (E/C.12/GC/27) and pdf_text_2 (CCPR/C/GC/32). The selected card switches the document. "Today there is one" — but the data has pdf_text_2 too. The plan says "every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data; the selected card has a red left border and the tabs show that document. Today there is one." Hmm, "today there is one" — but pdf_text_2 also has records and reference. Wait, does pdf_text_2 have a reference? "The same shape as pdf_text: the 18 pages of CCPR/C/GC/32 ... with its own reference (65 paragraphs, 128 footnotes)." So both have records and reference. So the rail would have two cards. The plan says "Today there is one" — maybe meaning in their preview only one? But the data description clearly says pdf_text_2 exists with reference. To be safe, I'll implement the generic scan: any key in WORKSHOP_DATA whose value is an object with `records` array and `reference` object gets a card. That handles both. If only one exists, one card. That's the robust approach.

Wait — but `uhri` also has `records` but no `reference`. `gc` has records but no reference. `hrc` has records, no reference. `library` has records, no reference. So scanning for `records` + `reference` picks pdf_text and pdf_text_2. Good.

Now the pipeline. Let me carefully design the parsing algorithm per the plan:

1. Sort records by page.
2. For each page, split text into lines (split on /\r?\n/).
3. Header: first non-empty line equals symbol → drop, log "header line removed". Otherwise log warning.
4. Footer: from the end, drop lines while: empty, starts with "GE.", consists only of 6-digit groups (date stamp like "051125 061125"), or is a bare number of 1-3 digits. A bare number equal to `page` is the page number; any other bare number logged as "bare number removed from the footer".
5. Body lines of all pages concatenated in page order, each tagged with page number.
6. Paragraph starts: line matching `/^(\d{1,3})\.$/` (number alone) or `/^(\d{1,3})\. (.+)$/` (number + text; log "number and text split").
7. Lines before first paragraph start = cover.
8. Headings:
   - Labelled: line matching `/^([IVX]+|[A-Z])\.$/` opens a labelled heading. Skip blank lines, then every line up to next label line or paragraph start is heading text. A line starting with lowercase letter or "(" continues previous heading line (log "heading title joined from two lines"); any other line is a further heading.
   - Unlabelled heading: non-empty line immediately followed by a paragraph-start line, at most 90 chars, starts with capital letter, doesn't end with . ; : , or digit → log "heading separated from paragraph text".
   
   Hmm, the labelled heading logic is a bit tricky. Let me think about the structure of a UN document:
   
   ```
   I.
   
   Introduction
   1.
   Text...
   ```
   
   So "I." alone on a line, blank, "Introduction", then "1." paragraph start. The rule: a line matching `/^([IVX]+|[A-Z])\.$/` opens a labelled heading. Then skip blank lines, then every line up to the next label line or paragraph start is heading text. So after "I.", we collect "Introduction" as heading text. If the title wraps: "A." blank "Something long" "continued..." — the continuation line starts with lowercase or "(" → join to previous heading line (log "heading title joined from two lines").
   
   Wait, but "any other line is a further heading" — meaning if a line after the heading title doesn't start with lowercase or "(", it's another heading line (like a second line of the heading in caps?). Hmm. Let me just implement: after a label line, skip blanks; then collect lines until we hit a label line or paragraph start. Within those, if a line starts with lowercase or "(", append it to the previous heading line (with a space), log "heading title joined from two lines". Otherwise it's its own heading line.
   
   Actually wait — there's ambiguity: what if the heading title itself is followed by more text? E.g.:
   ```
   A.
   Violence against women
   12.
   ```
   Fine. But what about:
   ```
   IV.
   ...
   ```
   Roman numerals: "IV." matches `[IVX]+`. But careful: a paragraph line could be "X." something? No, paragraph starts are digits. But what about a line like "A." appearing in text? Unlikely at line start. OK.
   
   Hmm, but there's a subtlety: what about lines like "I. Introduction" on one line? The plan says roman-numbered sections are "I.", a blank line, "Introduction" — three lines. But to be safe, maybe also handle "I. Introduction" on one line? The plan doesn't mention it. Keep it simple per plan: label alone on line. Actually, let me also handle `/^([IVX]+|[A-Z])\.\s+(.+)$/`? The plan doesn't say. Hmm, "where it says nothing, keep it simple". The plan describes the data: "Roman-numbered sections ("I.", a blank line, "Introduction")". I'll also accept label+text on one line as a heading (label + title) since it's harmless and more robust — actually wait, it could misfire. A line like "A. Something" — in the data, lettered subsections are "A." alone. I'll add the combined form as a heading too, logging appropriately, since it can only help robustness. Hmm, but risk: a paragraph text line starting with "A. "? Paragraph lines are continuation lines; a line starting with "A. " inside a paragraph... possible but unlikely. Actually the plan says keep it simple where it says nothing. I'll support both forms for labelled headings: `/^([IVX]+|[A-Z])\.$/` and `/^([IVX]+|[A-Z])\.\s+(.+)$/`. For the latter, the label is the heading label and the rest is the first title line. Hmm, but then "heading title joined" logic... Let me keep it simpler: treat `/^([IVX]+|[A-Z])\.\s*(.*)$/` — if there's text after, it's the title's first line; subsequent lines until next label/paragraph start are title continuation (lowercase/"(" joins, else new heading line). Actually that complicates. Let me just do:

   - Label line: `/^([IVX]+|[A-Z])\.$/` → opens labelled heading, label = group 1, then collect title lines.
   - Also `/^([IVX]+|[A-Z])\.\s+(.+)$/` → labelled heading with label and first title line = group 2. Then continue collecting title lines as above.
   
   For collecting: after the label (and optional first title line), skip blank lines? Hmm, the plan says "skip blank lines, then every line up to the next label line or paragraph start is heading text". So: after label line, skip blanks, then lines until next label/paragraph-start are heading text. But wait — what if there's a blank between title lines? Unlikely. OK.

   Actually, hold on. There's a subtle issue: after "I." and blank and "Introduction", the next line is "1." which is a paragraph start, so heading collection stops. Good. But what if a heading is followed by another heading? "A." ... "B." — collection stops at "B." label. Good.

   But danger: what if after a label line, the next non-blank line is NOT a title but something else? E.g., cover page has "United Nations", "Economic and Social Council", etc. But cover is before first paragraph start... wait, headings are detected in the body stream. The cover lines come before the first paragraph start. Hmm, but the heading detection happens on the concatenated body lines. Lines before the first paragraph start are the cover. But heading detection: "A line matching ... opens a labelled heading" — could a cover line match `/^([IVX]+|[A-Z])\.$/`? Cover lines: "E/C.12/GC/27", "United Nations", "Economic and Social Council", "Distr.: General", "6 November 2025", "Original: English", "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on economic, social and", "cultural rights and the environmental dimension of", "sustainable development*", "I.", "", "Introduction", "1.", ... So "I." appears on the cover area (before first paragraph "1."). Hmm! The plan says "Lines before the first paragraph start are the cover." But "I." and "Introduction" come before "1." too. So are they cover or heading?

   The plan says: "Lines before the first paragraph start are the cover." and separately headings are detected. There's tension. Let me re-read: "**Paragraph starts.** A line matching ... Lines before the first paragraph start are the cover." Then "**Headings.** A line matching `/^([IVX]+|[A-Z])\.$/` opens a labelled heading..." 

   Hmm, so if "I." and "Introduction" come before "1.", are they cover? But then section I's heading would be lost. But the plan also says the expanded paragraph shows "the full path ("IV. … › Right to work (art. 6)")" and Section column shows nearest heading. If "I. Introduction" is classified as cover, then paragraph 1's section would be... nothing? Hmm.

   Wait, maybe the order of operations matters: maybe heading detection runs on the whole stream, and "cover" is only lines before the first paragraph start that are NOT headings? Or maybe the cover is lines before the first heading/paragraph? Let me think about what makes sense: the cover is the title block (symbol already removed as header, "United Nations", "Economic and Social Council", "Distr.: General", date, "Original: English", committee name, title lines). Then "I." "Introduction" is a heading. Then "1." starts paragraph 1.

   The plan says "Lines before the first paragraph start are the cover." Taken literally, "I." and "Introduction" would be cover. But then the "Nothing lost" check classifies every line as cover, header, heading, paragraph or footer — and headings count. Hmm.

   Actually, maybe the intended reading: process the stream; when you hit the first paragraph start, everything before it that isn't a heading is cover. Or: headings can appear before the first paragraph (like "I. Introduction"), and the cover is the lines before the first heading or paragraph start, whichever comes first? 

   Let me reconsider. The plan's pipeline order: header → footer → concatenate body → paragraph starts → headings → paragraph lines. The heading rule says a label line "opens a labelled heading: skip blank lines, then every line up to the next label line or paragraph start is heading text". If we apply this to the whole stream including pre-first-paragraph lines, then "I." opens a heading, "Introduction" is its text, and collection stops at "1." (paragraph start). Then lines before "I." (the title block) are cover. That works nicely! So the cover = lines before the first heading OR paragraph start, whichever comes first. Hmm, but the plan literally says "Lines before the first paragraph start are the cover."

   Hmm wait, but actually maybe in this document, is "I. Introduction" before "1."? From the sample: page 1 text ends with "I.\n\nIntroduction\n1.\nA clean, healthy..." Yes! "I.", blank, "Introduction", "1.", text. So "I." and "Introduction" are before the first paragraph start.

   If I classify them as cover, then paragraph 1 has no section, and the "Headings found" count would miss "I. Introduction". The plan says 23 unlabelled headings and mentions roman sections. The check "Headings" counts labelled and unlabelled headings. If "I. Introduction" were cover, it wouldn't be counted as heading. Hmm.

   The plan says for the Section column: "shows the nearest heading above each paragraph". For paragraph 1, the nearest heading above is "I. Introduction" (well, "Introduction" under "I."). The full path example: "IV. … › Right to work (art. 6)". So paragraph 1's path would be "I. Introduction". That suggests "I."/"Introduction" ARE headings, not cover.

   So the sensible interpretation: cover = lines before the first heading or paragraph start. I'll implement: scan the stream; the first line that is a paragraph start OR a heading label opens the "document body"; lines before that are cover. Hmm, but what about unlabelled headings before the first paragraph? An unlabelled heading is "a non-empty line immediately followed by a paragraph-start line" — so it's by definition right before a paragraph start, fine.

   Actually, simpler: process lines sequentially with a state machine:
   - state "cover" initially. In cover state, if line is a heading label → switch to heading mode; if line is paragraph start → start paragraph 1; else → cover line.
   
   Wait but in cover state, could there be a line matching paragraph start? "6 November 2025" — no, doesn't match `/^\d{1,3}\.$/` or `/^\d{1,3}\. /`. Good. Could a cover line match heading label `/^([IVX]+|[A-Z])\.$/`? "Distr.: General" no. Single capital letter alone on a line — unlikely on cover. OK.

   Hmm, but actually there's another subtlety: what about "sustainable development*" — ends with "*", fine, cover.

   OK here's my state machine over the concatenated body lines (each tagged with page):

   ```
   state: 'cover' | 'heading-collect' | 'paragraph'
   current paragraph object, current heading stack
   ```

   Let me define line classification:
   - `isParaStart(line)`: `/^(\d{1,3})\.$/.test(line)` → {num, firstLine: null} or `/^(\d{1,3})\. (.+)$/` → {num, firstLine: text}.
   - `isLabel(line)`: `/^([IVX]+|[A-Z])\.$/` → label alone; or `/^([IVX]+|[A-Z])\.\s+(.+)$/` → label + title. Hmm wait, careful: could a paragraph continuation line start with "A. "? E.g. text wrapping where a line begins "A. "? Unlikely. But also — could a paragraph start line like "1. Text" be confused? No, digits vs letters.
   
   Hmm wait, actually there's a risk with `/^([A-Z])\.\s+(.+)$/`: a line like "E. coli something"? "E." followed by space... "E. coli" — hmm, in a human rights doc, unlikely. But to be safer, maybe require the label form only when alone on the line, per the plan, PLUS the combined form... The plan only specifies the alone form. The data says sections are "I.", blank, "Introduction". Let me check: are there any "A. Title" one-line headings in the data? The plan says lettered subsections are "A." alone. I'll support both but the combined form requires the rest to not look like... hmm. Keep it simple: support both forms; risk is minimal.

   Actually wait, one more risk: a paragraph line could be exactly "A." — e.g., an enumerated list inside a paragraph? The plan says "no lettered sub-paragraphs". OK.

   - Unlabelled heading: non-empty line immediately followed by a paragraph-start line, ≤90 chars, starts with capital, doesn't end with `. ; : ,` or digit. Note: must check the NEXT line. So I need lookahead. Implementation: iterate with index; when in paragraph state (or cover?) and current line is non-empty and next line is para start and current line matches the unlabelled-heading criteria → classify as heading (log "heading separated from paragraph text"), not paragraph text.

   Hmm wait — "a non-empty line immediately followed by a paragraph-start line". This applies when we're inside a paragraph: the paragraph's last line before the next number could be an unlabelled heading. E.g.:
   ```
   22. Some text...
   Right to work (art. 6)
   23. More text...
   ```
   So "Right to work (art. 6)" is immediately followed by "23." → unlabelled heading. Log "heading separated from paragraph text". 

   But careful: what if a paragraph's actual last line is short, starts with capital, doesn't end with punctuation, and is followed by the next paragraph number? E.g. a paragraph ending "...as follows" — ends without period? UN paragraphs usually end with a period. The criteria (≤90 chars, capital start, no terminal punctuation) make false positives unlikely. The plan acknowledges: "so a reader can spot a paragraph's last line mistaken for a heading" — the headings check lists unlabelled ones for review.

   Now the state machine in detail:

   ```
   lines = all body lines (non-header, non-footer) in page order, each {text, page, lineNo (within page)}
   results: paragraphs = [], headings = [], coverLines = [], repairs = []
   
   i = 0
   state = 'cover'
   currentHeading = null (stack of heading entries: {label, title, fullTitle, page})
   part = null (current roman part)
   section = null (current section heading)
   
   while i < lines.length:
     line = lines[i]
     if blank: i++; continue  (blank lines dropped — should I log? Plan says "blank lines are dropped". Maybe count them. The "Nothing lost" check counts non-empty lines only, so blanks don't matter. I'll just drop them, maybe count.)
     
     if state == 'cover':
       if isLabel(line): start heading (state stays 'cover'? or 'body'?) 
       ...
   ```

   Hmm, let me restructure. Rather than states, classify each line with lookahead, then group:

   Pass 1: classify each line:
   - blank → 'blank'
   - paraStart → 'parastart' (with num, inline text)
   - label → 'label'
   - else if next non-... hmm, "immediately followed by a paragraph-start line" — immediately, so next line (i+1) must be parastart. But what if there's a blank between? "on the line just before a paragraph number" — immediately followed. So check lines[i+1] is parastart. If lines[i+1] is blank, then not. OK: `isUnlabelledHeading(i)` = line non-empty, lines[i+1] exists and is parastart, len ≤ 90, /^[A-Z(]/ hmm "starting with a capital letter" — /^[A-Z]/, and not /[. ;:,]$/ and not /\d$/.
   
   Wait, "starting with a capital letter and not ending with a full stop, semicolon, colon, comma or digit". So: `/^[A-Z]/.test(t) && !/[.;:,]$/.test(t) && !/\d$/.test(t) && t.length <= 90`.
   
   Hmm, but what about headings that end with ")" like "Right to work (art. 6)" — ends with ")", allowed. Good.
   
   - else → 'text' (potential paragraph line or heading title or cover)

   Pass 2: walk through and assign:
   ```
   mode = 'cover'
   for each line:
     if blank: skip
     if parastart:
       mode = 'paragraph'
       close current paragraph (if any)
       start new paragraph {number, lines: [], pages: []}
       if inline text: add as first line, log "number and text split"
       section = current section heading; part = current part
     elif label:
       mode = 'heading'
       parse label; collect following title lines: skip blanks; while next lines are 'text' (not parastart, not label, not unlabelled-heading? hmm)...
   ```

   The heading title collection: "skip blank lines, then every line up to the next label line or paragraph start is heading text". So after a label line, skip blanks, then consume 'text' lines until we hit a parastart or label. But wait — could an unlabelled heading line appear within? E.g. label "A.", blank, "Title", then "12." parastart — fine. What if label, blank, title, then another text line that's actually... the plan says "every line up to the next label line or paragraph start is heading text". So all text lines after the label until parastart/label are heading text. Within those, "a line starting with a lowercase letter or '(' continues the previous heading line (logged 'heading title joined from two lines'), any other line is a further heading."

   Hmm wait, that's odd: "any other line is a further heading" — so if the title wraps and the continuation starts with a capital, it's treated as a separate heading line? That seems weird but OK — e.g.:
   ```
   A.
   Violence against women
   and girls
   ```
   "and girls" starts lowercase → joined. But:
   ```
   B.
   Some Title
   Another Line
   ```
   "Another Line" starts capital → "a further heading". Hmm, that would create two heading entries. Whatever — follow the plan.

   Wait, actually I wonder if it means: within the heading block, the FIRST text line is the title; subsequent lines starting with lowercase or "(" are joined to it; any other subsequent line is a further (sub)heading. OK, implement as stated.

   Also: what about unlabelled headings inside heading collection? If a text line is immediately followed by a parastart, it's an unlabelled heading — but in heading-collection mode, "every line up to the next paragraph start is heading text". Hmm, conflict: after "A." blank "Title", next line "12." parastart → collection stops. But what if "A." blank "Title" "Subtitle" "12."? Then "Subtitle" is immediately followed by parastart → unlabelled heading criteria match... but we're in heading collection. The plan's heading rule says every line up to the next paragraph start is heading text. So in heading mode, consume all text lines until parastart/label. The unlabelled-heading rule applies in paragraph mode (a paragraph's last line). Hmm, but actually the unlabelled heading rule as stated: "An unlabelled heading is a non-empty line immediately followed by a paragraph-start line" — regardless of mode? If in heading mode after "A.", the line "Title" is followed by "Subtitle" (text), not parastart, so not unlabelled. Only the last text line before parastart could be unlabelled... but in heading mode it's heading text per the labelled rule. Hmm.

   Let me simplify: I'll do classification with priority:
   1. blank
   2. parastart
   3. label
   4. unlabelled heading (next line is parastart + criteria) — but only when NOT in heading-collection mode? Actually if we're collecting a labelled heading's title and the last title line is immediately before a parastart... e.g.:
   ```
   A.
   Introduction
   1. text
   ```
   "Introduction" is immediately followed by "1." → matches unlabelled criteria (starts capital, no terminal punct, ≤90). But it's the title of heading A. So in heading mode, it should be heading text, not unlabelled heading. So: unlabelled heading detection applies only when the previous line was paragraph text (i.e., we're in a paragraph). I'll track mode.

   OK let me now write the state machine concretely:

   ```js
   function parseDocument(doc) {
     const symbol = doc.symbol;
     const records = [...doc.records].sort((a,b) => a.page - b.page);
     const repairs = []; // {page, target, kind, before, after}
     const warnings = [];
     const allLines = []; // {text, page, lineNo}
     const pageStats = records.map(rec => {
       const rawLines = rec.text.split(/\r?\n/);
       const lines = rawLines.map((t, idx) => ({text: t, page: rec.page, lineNo: idx+1}));
       // header
       let start = 0;
       // find first non-empty
       let fi = 0; while (fi < lines.length && lines[fi].text.trim() === '') fi++;
       if (fi < lines.length && lines[fi].text.trim() === symbol) {
         lines[fi].cls = 'header';
         repairs.push({page: rec.page, target: 'page header', kind: 'header line removed', before: lines[fi].text, after: ''});
         start = fi + 1;
       } else {
         warnings.push({page: rec.page, msg: 'first non-empty line is not the symbol'});
       }
       // footer: from end
       let end = lines.length;
       const footerRemoved = [];
       while (end > start) {
         const t = lines[end-1].text.trim();
         if (t === '') { end--; continue; }
         if (/^GE\./.test(t)) { footerRemoved.push({line: lines[end-1], kind:'footer'}); end--; continue; }
         if (/^(\d{6})(\s+\d{6})*$/.test(t)) { footerRemoved.push({line: lines[end-1], kind:'footer'}); end--; continue; } // date stamp
         if (/^\d{1,3}$/.test(t)) {
           const n = parseInt(t, 10);
           if (n === rec.page) { footerRemoved.push({line: lines[end-1], kind:'page number'}); }
           else {
             footerRemoved.push({line: lines[end-1], kind:'bare number'});
             repairs.push({page: rec.page, target: 'footer', kind: 'bare number removed from the footer', before: t, after: ''});
           }
           end--; continue;
         }
         break;
       }
       for (const f of footerRemoved) f.line.cls = 'footer';
       // body lines
       for (let i = start; i < end; i++) {
         allLines.push(lines[i]);
       }
       return {page: rec.page, lines, bodyCount: end - start};
     });
     ...
   }
   ```

   Wait — the footer rule: "drop lines while the line is empty, starts with 'GE.', consists only of 6-digit groups, or is a bare number of one to three digits." So the loop continues while ANY of these match. Note "consists only of 6-digit groups" — "051125 061125" matches. Also a single "051125"? "consists only of 6-digit groups" — one or more groups separated by spaces. My regex `/^(\d{6})(\s+\d{6})*$/` handles it. But careful: a bare number of 1-3 digits is also checked; a 6-digit number alone would match the 6-digit-group rule first. Order: check empty, GE., 6-digit groups, bare 1-3 digits. A 4-5 digit number wouldn't match any → stops the footer loop. Fine.

   Hmm, one concern: what if a page's last body line is a bare number that's actually paragraph text? E.g., a paragraph ending with a number on its own line? The plan says the footer rule drops trailing bare numbers — accepted risk per plan.

   Also: what if the footer loop eats into footnote text? Footnote text lines like "7 E/2003/22..." don't match footer patterns, so the loop stops there. Good — footnotes stay in body (flagged later).

   Now the main classification pass over allLines:

   ```js
   const isBlank = l => l.text.trim() === '';
   const paraStartRe1 = /^(\d{1,3})\.$/;
   const paraStartRe2 = /^(\d{1,3})\. (.+)$/;
   function paraStart(l) {
     let m = l.text.match(paraStartRe1);
     if (m) return {num: +m[1], inline: null};
     m = l.text.match(paraStartRe2);
     if (m) return {num: +m[1], inline: m[2]};
     return null;
   }
   const labelRe1 = /^([IVX]+|[A-Z])\.$/;
   const labelRe2 = /^([IVX]+|[A-Z])\.\s+(.+)$/;
   function labelOf(l) {
     let m = l.text.match(labelRe1);
     if (m) return {label: m[1], title: null};
     m = l.text.match(labelRe2);
     if (m) return {label: m[1], title: m[2]};
     return null;
   }
   ```

   Hmm wait, labelRe2 `/^([IVX]+|[A-Z])\.\s+(.+)$/` — danger: a paragraph text line like "A. clean, healthy..." would be misread as a heading. In UN docs, paragraph lines rarely start with "X. ". But what about lines like "I. Introduction" — that's the combined form, good. Risk accepted? Hmm. Actually wait — there's a real risk: paragraph continuation lines. E.g., a paragraph wrapping such that a line starts with "A. "? Very unlikely in prose. But what about roman numeral lines in text like "Article 18"? No, that doesn't match (needs to be only IVX chars before the period). "IV." alone as a line in text? Unlikely. OK, accept both forms.

   Hmm, wait, actually there's another consideration: the plan says labelled heading is "A line matching `/^([IVX]+|[A-Z])\.$/`" — only the alone form. And "where it says nothing, keep it simple". The combined form isn't mentioned... but "I. Introduction" on one line is common in UN docs. In THIS file, per the plan, sections are "I.", blank, "Introduction". I'll support both anyway for robustness — it doesn't hurt this file. Actually, hmm, it could hurt: if a paragraph's continuation line starts with e.g. "A. " — let me add a guard: only treat labelRe2 as a heading if we're NOT inside a paragraph? No wait — headings appear between paragraphs, i.e., after a paragraph's last line and before the next parastart. When we're inside a paragraph (mode='paragraph'), a line matching labelRe2... could be a heading (the paragraph ended without us knowing) or text. Hmm.

   The plan's approach: headings are detected structurally. An unlabelled heading is detected by lookahead (next line is parastart). A labelled heading "A." alone — when inside a paragraph, if we see "A." alone, is it a heading or text? Per plan, it "opens a labelled heading". So even mid-paragraph, "A." opens a heading. That means the previous paragraph ends there. OK.

   For labelRe2 (combined), mid-paragraph it's ambiguous. To be safe: treat labelRe2 as heading only when NOT currently inside a paragraph (mode != 'paragraph'), OR when... hmm. Actually, let me check: in this document, do combined label lines occur mid-paragraph? The plan says sections are the alone form. The safest: treat labelRe1 (alone) as heading always; treat labelRe2 as heading only when the previous non-blank line was a parastart's paragraph end... ugh, too complex. 

   Simpler: treat labelRe2 as a heading only when mode is 'cover' or 'heading' (i.e., not inside a paragraph). Inside a paragraph, a line starting with "X. " is treated as paragraph text. Hmm, but then a combined heading right after a paragraph would be missed... In this file, per the plan, all labelled headings are the alone form, so this doesn't matter. And unlabelled headings handle the "Title\n23." case. I'll go with: labelRe1 always a heading; labelRe2 a heading only when not inside a paragraph. Actually wait — even simpler and safer: since the plan only specifies the alone form, and the data uses the alone form, maybe I should ONLY support the alone form? But then "I. Introduction" one-liners in pdf_text_2 would break... The plan says pdf_text_2 is "the same shape". Hmm, "the same converter produced them" — likely same layout. 

   Decision: support both, with labelRe2 treated as heading when mode != 'paragraph'. If mode == 'paragraph' and line matches labelRe2, treat as paragraph text. This is robust.

   Hmm, wait, actually there's another subtlety: what about mode 'cover'? Cover lines before first parastart: "United Nations", "Economic and Social Council", etc. If a cover line matched labelRe2 (e.g., "D. Something")? "Distr.: General" — "Distr." doesn't match `[A-Z]\.` (it's "Distr." — D-i-s-t-r-period, the regex `^([IVX]+|[A-Z])\.` requires the label to be ONLY ivx chars or a single capital letter, then a period. "Distr." = "D" followed by "istr." — `^[A-Z]\.` requires period right after the single letter. "Distr." has "i" after "D", so no match. Good.) OK.

   Now unlabelled heading: line is non-empty, next line (i+1 in allLines) is a parastart, length ≤ 90, starts with capital, doesn't end with [.;:,] or digit. And mode == 'paragraph' (it's the last line of the current paragraph region). Actually also could occur in cover mode? "Introduction" before "1." — but that's consumed as labelled heading title in this file. If a doc had an unlabelled heading before the first paragraph... e.g. cover ends with "Introduction" then "1." — then "Introduction" would be unlabelled heading. Fine, allow in any mode except heading-collection.

   Wait, careful: in heading-collection mode after a label, the title lines are consumed until parastart/label. If the last title line is immediately before parastart, it's heading text (per labelled rule), not unlabelled. So unlabelled detection only when mode == 'paragraph' or 'cover'. Hmm, in cover mode, a line immediately before the first parastart that looks like a heading → unlabelled heading. OK.

   Now, the walk:

   ```js
   const paragraphs = [];
   const headings = []; // {label, title, full, page, kind: 'labelled'|'unlabelled'}
   const cover = [];
   let mode = 'cover';
   let cur = null; // current paragraph
   let curHeading = null; // current labelled heading being collected
   let section = null; // current section title (string)
   let part = null;    // current roman part (string like "IV.")
   let headingStack = []; // for full path
   
   for (let i = 0; i < allLines.length; i++) {
     const l = allLines[i];
     if (isBlank(l)) { l.cls = 'blank'; continue; }
     const ps = paraStart(l);
     if (ps) {
       // close current paragraph
       if (cur) { paragraphs.push(cur); }
       cur = { number: ps.num, lines: [], pages: new Set(), startLine: l, section: section, part: part, flagged: false, suspect: [] };
       l.cls = 'parastart';
       if (ps.inline) {
         const inlineLine = {text: ps.inline, page: l.page, lineNo: l.lineNo, cls: 'paragraph'};
         cur.lines.push(inlineLine);
         cur.pages.add(l.page);
         repairs.push({page: l.page, target: 'para. ' + ps.num, kind: 'number and text split', before: l.text, after: ps.num + '. / ' + ps.inline});
       }
       mode = 'paragraph';
       curHeading = null;
       continue;
     }
     const lab = labelOf(l);
     if (lab && (lab.title === null || mode !== 'paragraph')) {
       // labelled heading
       if (cur) { paragraphs.push(cur); cur = null; }
       l.cls = 'heading';
       const h = {label: lab.label, titleLines: lab.title ? [lab.title] : [], page: l.page, kind: 'labelled', line: l};
       headings.push(h);
       // update part/section
       if (/^[IVX]+$/.test(lab.label)) {
         part = lab.label + '.';
         section = null; // will be set by title
         headingStack = [{label: lab.label + '.', title: ''}];
       } else {
         section = lab.label + '.';
         headingStack.push({label: lab.label + '.', title: ''});
       }
       // collect title lines: skip blanks, then text lines until parastart or label
       let j = i + 1;
       // skip blanks
       while (j < allLines.length && isBlank(allLines[j])) { allLines[j].cls = 'blank'; j++; }
       let firstTitle = true;
       while (j < allLines.length) {
         const nl = allLines[j];
         if (isBlank(nl)) { nl.cls = 'blank'; j++; continue; }  // hmm, plan says skip blank lines then every line up to next label/parastart — blanks within? Let me just skip blanks throughout.
         if (paraStart(nl) || (labelOf(nl) && labelOf(nl).title === null)) break;
         // hmm, what about labelRe2 as terminator? "up to the next label line" — any label line. Let me break on any label.
         if (labelOf(nl)) break;
         // unlabelled heading check? In heading mode, per plan, every line up to next label/parastart is heading text. So no unlabelled check here.
         nl.cls = 'heading';
         const t = nl.text.trim();
         if (firstTitle) {
           h.titleLines.push(t);
           firstTitle = false;
         } else if (/^[a-z(]/.test(t)) {
           // continues previous heading line
           h.titleLines[h.titleLines.length-1] += ' ' + t;
           repairs.push({page: nl.page, target: 'heading ' + h.label + '.', kind: 'heading title joined from two lines', before: h.titleLines[h.titleLines.length-1].slice(0, ...) hmm, before/after...});
         } else {
           h.titleLines.push(t); // "a further heading"
         }
         j++;
       }
       // finalize heading title
       h.title = h.titleLines.join(' › ')? hmm...
       i = j - 1; // continue outer loop from j
       mode = 'heading';
       // update section display
       ...
       continue;
     }
     // unlabelled heading?
     if (mode !== 'heading' && i + 1 < allLines.length && paraStart(allLines[i+1]) && isUnlabelledHeading(l)) {
       if (cur) { paragraphs.push(cur); cur = null; }
       l.cls = 'heading';
       const h = {label: null, titleLines: [l.text.trim()], page: l.page, kind: 'unlabelled', line: l};
       headings.push(h);
       section = h.titleLines[0];
       repairs.push({page: l.page, target: 'heading', kind: 'heading separated from paragraph text', before: l.text, after: '(heading)'});
       mode = 'heading';
       continue;
     }
     // otherwise: cover or paragraph text
     if (mode === 'cover') {
       l.cls = 'cover';
       cover.push(l);
     } else {
       l.cls = 'paragraph';
       if (cur) {
         cur.lines.push(l);
         cur.pages.add(l.page);
       } else {
         // text after a heading but before any parastart? shouldn't happen; treat as cover? 
         l.cls = 'cover'; cover.push(l);
       }
     }
   }
   if (cur) paragraphs.push(cur);
   ```

   Hmm wait, there's a bug: when a labelled heading appears, I push `cur` (closing the paragraph). But the paragraph's lines were already collected. Good. But also — the unlabelled heading case: the line is the last line of the previous paragraph region; I close the paragraph WITHOUT including this line. Good, and log "heading separated from paragraph text".

   But wait — there's an issue with the unlabelled heading check when mode == 'paragraph' but the line is actually the paragraph's real last line (false positive). The plan accepts this risk and lists unlabelled headings in the checks so a reader can spot mistakes. OK.

   Another subtlety: the unlabelled heading check `i+1 < allLines.length && paraStart(allLines[i+1])` — but what if there are blank lines between? "immediately followed" — so no blanks. If allLines[i+1] is blank, not a heading. OK.

   Hmm, also: what if the unlabelled heading line is followed by parastart but we're in 'cover' mode and it's actually cover text? E.g., cover's last line before "1." — in this file that's "Introduction" but it's consumed by the labelled heading "I.". If a doc had no "I." label, "Introduction" before "1." would be an unlabelled heading. That's correct behavior.

   Now heading title finalization and section/part tracking. Let me maintain:
   - `partStack`: array of {label, title} for roman headings.
   - `section`: current innermost heading full title.
   
   For the Section column: "the nearest heading above each paragraph". The full path in expanded row: "IV. … › Right to work (art. 6)". So path = part label + title › section title. Let me build:
   - When a roman heading (IVX) is parsed: part = {label: "IV.", title: joined title}. section = null initially, then if it has a title, section = title? Hmm. E.g.:
   ```
   IV.
   (blank)
   Some part title
   A.
   (blank)
   Right to work (art. 6)
   23. ...
   ```
   Wait, actually in CESCR GCs, the structure is like:
   ```
   IV. 
   Conclusions and recommendations? 
   ```
   Hmm, or:
   ```
   III.
   (blank)
   Specific issues? 
   A.
   (blank)
   Right to work (art. 6)
   23.
   ```
   Hmm, actually in E/C.12/GC/27 the structure per the sample: "I.\n\nIntroduction\n1.\n..." So roman heading "I." with title "Introduction", then paragraph 1 directly (no lettered subsection). Later: "IV." title, then "A." "Right to work (art. 6)" then paragraphs.

   So: section for a paragraph = nearest heading above it, whether roman or lettered or unlabelled. Path = roman part (label + title) › ... › nearest heading. Let me maintain a stack of headings since the last roman heading:
   - `currentPart` = {label: "IV.", title: "..."} or null.
   - `currentSection` = the nearest heading (labelled lettered or unlabelled) title, or the roman title if no lettered heading since.
   
   Simplest: keep `headingPath` = array of strings. When roman heading: headingPath = [label + '. ' + title]. When lettered heading: headingPath = [partLabel + ' ' + partTitle, letter + '. ' + title]? Hmm, the example: "IV. … › Right to work (art. 6)". So path = "IV. <part title> › Right to work (art. 6)". 

   Let me store for each heading: `full` = computed path string. For roman: full = "IV. Title". For lettered: full = currentRomanFull + " › " + "A. Title". For unlabelled: full = currentRomanFull + " › " + title (or just title if no roman). And paragraph.section = the nearest heading's title (short), paragraph.path = nearest heading's full.

   Hmm, the Section column shows "the nearest heading above each paragraph ("Right to work (art. 6)")" — so just the title, e.g. "Right to work (art. 6)". And expanded shows full path "IV. … › Right to work (art. 6)". OK:
   - paragraph.section = nearest heading title (e.g., "Right to work (art. 6)"), or "" if none.
   - paragraph.path = nearest heading full path.

   For a roman heading with title "Introduction", paragraph 1's section = "Introduction", path = "I. Introduction". Good.

   Now, paragraph text computation:
   - text = lines joined with ' ', collapsing double spaces, trimmed. Each line's text trimmed first? "the paragraph's lines joined with a single space, double spaces collapsed, trimmed". So: `cur.lines.map(l => l.text.trim()).join(' ').replace(/\s+/g, ' ').trim()`? Hmm, "double spaces collapsed" — I'll do `.replace(/ {2,}/g, ' ')` after joining, or just collapse all whitespace runs. Let me do: join with ' ', then replace(/\s+/g,' '), trim. But careful: the inline text from paraStartRe2 — the line was "23. Some text" and inline = "Some text". When joining, the parastart line itself contributes only the inline part. Good.
   - text_lines: original lines (with their original text? or trimmed?) joined with " | " for CSV. Plan: "`text_lines` keeps the original lines for the toggle and the CSV column `text_lines` (lines separated by ' | ')". Hmm, the CSV columns listed don't include text_lines... wait: "one row per paragraph with `number`, `section`, `part`, `page_start`, `page_end`, `first_words_reference`, `first_words_found`, `first_words_match`, `text`, `text_raw`, `flagged`, `suspect_lines`, `repairs`, `citation`, `symbol`, `doc_url`". No text_lines in CSV. But text says "the CSV column `text_lines`" — contradiction. I'll include text_lines in the CSV anyway? The listed columns are explicit; text_raw is presumably the text with original line breaks (or the raw lines?). Hmm: `text` vs `text_raw`. Probably `text` = cleaned joined text, `text_raw` = the raw lines joined with newline (as the converter produced, including suspect lines). I'll define: text_raw = original lines' raw text joined with "\n" (preserving line breaks), text = normalized single-space join. And also include text_lines column with " | " separator — harmless to add. Actually, to follow the explicit list, I'll include exactly the listed columns plus text_lines (since the plan mentions it as a CSV column). Fine.

   - page_start / page_end: pages of first and last line. If the parastart had inline text, the parastart line's page counts as first. pages set: add parastart line's page always (even if no inline? yes — the number line is on that page). Hmm: if parastart is alone ("23.") and text starts next line possibly on next page? The number line is on page X, first text line on page X too usually. page_start = page of the parastart line. page_end = page of last line. If only the number line (empty paragraph?) — page_start = page_end = that page. I'll add l.page to pages when creating cur.

   - "paragraph joined across a page break": when a paragraph's lines carry two page numbers → log repair {kind: 'paragraph joined across a page break', page: page_end, target: 'para. n', before: 'page break between p.X and p.Y', after: 'joined'}. Log once per paragraph.

   - Suspect lines: within a paragraph's lines (including inline?), a line is suspect when:
     - bare number 1-3 digits, no full stop: `/^\d{1,3}$/` (after trim)
     - or starts with 1-3 digits, a space, then a capital letter / UN doc symbol / quotation mark: `/^\d{1,3} [A-Z"“]/` or `/^\d{1,3} [A-Z]{1,4}\//` (symbol like "E/2003/22")... The plan: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark ("7 E/2003/22…", "2 Summary for policymakers…")". So regex: `/^\d{1,3} ([A-Z"“”‘’]|[A-Z]{2,}\/)/`? Hmm, "E/2003/22" starts with capital E then "/". A capital letter covers "E" too. So `/^\d{1,3} [A-Z"“”]/` covers both examples ("7 E/2003/22" → "7 E..." matches capital; "2 Summary" matches). But wait — would a real paragraph line start with "17 Sustainable Development Goals"? Yes — the plan explicitly says that gets flagged (false positive, acceptable). So regex: `/^\d{1,3} [A-Z"“”]/`. Hmm, but also "a UN document symbol" — symbols start with capital letters anyway (E/, A/, CCPR/). So one regex suffices: `/^\d{1,3}\s+[A-Z"“”]/`. Let me also include the case with no space? "7E/..."? Plan says "a space". OK.
     
     Wait, but also the bare-number case: `/^\d{1,3}$/` — but the footer already removed trailing bare numbers; a bare number INSIDE a paragraph (footnote number displaced into the middle?) — the plan says "A suspect line and every line after it to the end of its page are suspect: a footnote block runs to the foot of the page." So once a suspect line is found in a paragraph, all subsequent lines of that paragraph on the same page are suspect. Hmm — "every line after it to the end of its page" — so within the same page, lines after the suspect line are suspect. But the paragraph may continue to the next page... The footnote block runs to the foot of the page, so lines after the suspect line until the page ends are suspect. If the paragraph continues on the next page, are those lines suspect? The footnote block ended at the page foot (footer removed). Lines on the next page belong to the next... hmm, actually if a paragraph spans a page break AND has footnotes, the footnote block is at the foot of the first page, and the paragraph continues on the next page after the header. The lines after the suspect line "to the end of its page" — so only same-page lines. Lines on subsequent pages of the same paragraph are not suspect (they're real text). I'll implement: for each paragraph, iterate its lines in order; once a suspect line is found, mark it and all following lines with the same page as suspect. Lines on later pages: not suspect (but hmm, what if the footnote block... no, footnotes end at page foot). Actually wait — what if the suspect line is on page 5 and the paragraph continues to page 6 — the footnote text is on page 5 only. Right.

     Hmm, wait, but actually there's a subtlety: the footnote block starts with the first footnote (bare number + blank + text, or "7 text"). The "suspect line" is the first footnote's number line. Everything after it on that page is footnote text (footnotes run to the foot). So marking "suspect line and every line after it to the end of its page" is right.

   - Paragraph over 300 words → flagged too. Word count of the joined text (split on whitespace). Log? The plan lists "paragraph over 300 words" as a "Why" in tab 03. And the check "Pages flagged" includes "paragraphs over 300 words". So flagged = has suspect lines OR word count > 300. A page is flagged when it has a suspect line inside a paragraph. Hmm: "A page is flagged when it has a suspect line inside a paragraph; the paragraph gets flagged true". And separately "A paragraph over 300 words is flagged too". So paragraph.flagged = suspectLines.length > 0 || words > 300. Page flagged = any paragraph with suspect lines on that page? Or any flagged paragraph touching that page? Plan: "Pages flagged: the pages with suspect lines inside a paragraph and the paragraphs over 300 words, each listed with its page and paragraph." So a page is flagged if any paragraph has suspect lines on it, or any paragraph over 300 words starts (or touches?) that page. I'll say: page flagged if any suspect line is on that page, or any over-300-word paragraph has page_start (or any page) on it. Let me use: paragraph's pages set — if flagged, all its pages are flagged? Hmm, simpler: flaggedPages = set of pages of suspect lines ∪ pages of over-300 paragraphs (all pages they span). I'll do: for each flagged paragraph, add all its pages. Hmm, but a paragraph spanning pages 3-4 with footnotes on page 3 — page 4 also flagged? The plan's tab 03: "One row per flagged page: Page | Paragraph | Suspect lines | Why". I'll compute per page: suspect lines on that page (from paragraphs), and paragraphs over 300 words that include that page. Let me keep it: page flagged if it has ≥1 suspect line, or a >300-word paragraph touches it. Rows on tab 03: one per flagged page, listing the paragraph(s) and suspect line count and why.

   - First words: first six whitespace-separated tokens of the joined text, after dropping tokens that are only digits or digits glued to end of word ("waste.2" → "waste."). So: tokens = text.split(/\s+/); filter out tokens matching /^\d+$/; map token → token.replace(/(\d+)$/, '')? "digits glued to the end of a word ('waste.2' becomes 'waste.')" — so strip trailing digits from each token. Hmm, "dropping tokens that are only digits and digits glued to the end of a word" — parse: drop tokens that are only digits; and (strip) digits glued to the end of a word. So "waste.2" → "waste.". What about "2." at the start? The paragraph number is not part of the text (we split it off), so text starts with the actual first word. But wait — for paragraphs where the number was alone on its line, the text starts with the next line. Good. But footnote marks glued: "waste.2" → strip trailing digits → "waste.". Also a token like "3" alone → dropped. Take first 6 remaining tokens. Join with ' '.
   
     Hmm wait, careful: should I strip trailing digits from ALL tokens or only when checking? The plan: "first_words_found = the first six whitespace-separated words of the joined text, after dropping tokens that are only digits and digits glued to the end of a word". So the transformation applies to the token stream before taking six. I'll apply: tokens.map(t => t.replace(/\d+$/, '')).filter(t => t !== '' && !/^\d+$/.test(t))... wait order: drop tokens that are only digits (before or after stripping? "2" is only digits → drop; "waste.2" → strip → "waste." keep). Let me do: t2 = t.replace(/\d+$/, ''); if (t2 === '') drop; else keep t2. Hmm but "2." → strip trailing digits → "2." has no trailing digit (ends with '.')... wait "2." — trailing char is '.', so /\d+$/ doesn't match. Hmm! "waste.2" ends with '2' → strip → "waste.". But a token "2." (footnote mark after a word with period? like "right.2" → "right."). And a standalone "2" → strip → "" → drop. And "2." standalone → stays "2."? Hmm. In the text, footnote marks appear as "waste.2" (glued) or "”. 3" (after space) — the latter gives token "3" → dropped. OK my approach: strip trailing digits, drop if empty. "2." → no trailing digit → kept as "2." — hmm, is that right? A token "2." would only occur if the text has "word 2." — like a list? Edge case, fine.
     
     Wait, actually also leading digits? "3 The" — token "3" dropped. OK.
     
   - Normalisation for comparison: curly quotes → straight, en/em dashes → hyphen, whitespace runs → single space. Case kept. Apply to both found and reference before comparing. `first_words_match` = normalise(found) === normalise(reference).
   
   - reference.first_words keyed by paragraph number as string. If missing → check "not run".

   - Citation = symbol + ", para. " + number.

   - Repairs log: kinds: 'header line removed', 'footer line removed', 'bare number removed from the footer', 'number and text split', 'paragraph joined across a page break', 'heading separated from paragraph text', 'heading title joined from two lines'. 
   
     Wait — "footer line removed" as a kind: the plan's repair log kinds list includes "footer line removed". So each footer line dropped (page number, GE., date stamp, blanks?) gets logged? "each step logs what it removed or changed". Hmm, the kinds list: "header line removed, footer line removed, bare number removed from the footer, number and text split, paragraph joined across a page break, heading separated, heading title joined". So footer lines (GE., date stamp, page number) → "footer line removed"; bare numbers ≠ page → "bare number removed from the footer". I'll log each footer line individually with kind 'footer line removed' (before = line text, after = ''), and bare numbers with the special kind. Blank lines dropped — log? They're not "non-empty lines"; the nothing-lost check counts non-empty. I'll not log blanks individually (too noisy), maybe count them. Actually the repair log table could get long: 20 pages × ~3 footer lines = 60 rows + headers 20 + ... That's fine, it's a log. But maybe group footer lines per page into one entry? The plan says "a table of every change the script made, in document order, Page | Paragraph or footnote | What was done | Before | After, with a count per kind above it". "every change" — I'll log each line. 20 headers + ~60 footer lines + 12 bare numbers + 2 splits + 19 joins + 23 heading separations + joins... ~140 rows. That's OK for a table. Hmm, maybe I'll log footer lines individually but that's fine.

     Actually, let me reconsider: to keep the log readable, log each removed line as its own entry. Fine.

   - "Nothing lost" check: every non-empty line classified exactly once as cover, header, heading, paragraph, or footer. I set `cls` on each line during parsing. Suspect lines are paragraph lines with a flag. Count per kind, sum = total non-empty lines. Unclassified lines listed. Since I classify every line in the walk (blank → 'blank'), every line gets a cls. Let me make sure: header lines get cls='header', footer lines cls='footer', body lines get cls in the walk: 'parastart' — hmm, parastart lines: are they 'paragraph' kind for the nothing-lost check? The kinds are cover, header, heading, paragraph, footer. A parastart line is part of the paragraph — I'll count it as 'paragraph'. Let me set cls='paragraph' for parastart lines too (but keep a flag isParaStart for rendering). Actually for the raw viewer coloring: "each line coloured by what the script decided it was (cover, header, heading, paragraph, suspect line, footer)". So parastart → paragraph colour. Suspect → suspect colour. OK: cls values: 'cover', 'header', 'heading', 'paragraph', 'suspect', 'footer', 'blank'. For nothing-lost, count non-blank lines by cls (suspect counts as paragraph? The plan: "a suspect line is a paragraph line with a flag" — so in the nothing-lost check, suspect lines count as paragraph). I'll count suspect under paragraph but also report suspect count separately.

   Now checks (tab 04), each one line:
   1. Paragraph count: found vs reference.paragraphs → pass/fail.
   2. Numbering: numbers exactly 1..n in order; gaps/duplicates listed.
   3. First words: count of mismatches vs reference.first_words; each listed "para. n: found … / reference …". If reference missing → "not run".
   4. Suspect lines: n suspect lines on n pages in n paragraphs; none removed (verify: all suspect lines still present in paragraph text — check that each suspect line's text appears in the paragraph's text_raw). 
   5. Pages flagged: list each flagged page with paragraph(s).
   6. Headers and footers: pages whose first line was symbol (expected all); pages with page number in footer (expected all but first); bare numbers removed listed with page.
   7. Headings: count labelled and unlabelled; list unlabelled ones.
   8. Nothing lost: counts per kind sum to total non-empty lines; unclassified listed.

   Header status: "n of m checks pass" green dot, or "n checks failed" red dot + red dot on tab 04. Checks that are "not run" (missing reference) — count as neither pass nor fail? I'll count pass/fail only; if reference missing, those checks show "not run". m = total checks run? Let me define m = number of checks (8), pass = those that pass, failed = those that fail, not run = shown separately. Header: "n of m checks pass" where m = 8 (or checks that ran). I'll say: if failed > 0 → red "n checks failed" (and "x of y pass" maybe). Plan: "a green dot and 'n of m checks pass', or a red dot and 'n checks failed'". So if all pass: green "8 of 8 checks pass". Else red "n checks failed". I'll show red dot + "n of m checks pass · k failed"? The plan says red dot and "n checks failed". I'll do: green: "✓ 8 of 8 checks pass"; red: "✗ 2 checks failed (6 of 8 pass)". Keep simple: red dot + "n checks failed". Hmm, I'll show "n of m checks pass" in green when all pass; when some fail, red dot + "n checks failed". Fine.

   Now the UI layout:

   - Header (always visible): monospace label "UN DOCUMENT · PDF TEXT", serif title, one line: symbol linked to doc_url (new tab), "adopted {reference.adopted}", "n pages of raw converter text", source. One sentence under: what the page does. Right side: status dot + "n of m checks pass".
   - Left rail (always visible): "DOCUMENT" heading; cards for each doc in WORKSHOP_DATA with records+reference, in order of keys. Card: symbol monospace, short title (title? maybe truncated), "adopted …", "n pages". Then two big serif numbers: "n paragraphs" with "of reference.paragraphs" and a thin bar showing share (red when short or over); "n pages flagged" of document's pages (red when > 0, link to tab 03); "n of m checks pass" link to tab 04. Selected card red left border; clicking switches document (re-run pipeline for that doc and re-render).
   - Tabs: 01 RESULT · 02 PARAGRAPHS · 03 FLAGGED PAGES · 04 CHECKS & METHOD. role="tablist", arrow-key navigation, tab panels hidden when not active; hidden panel not focusable (use hidden attribute + [hidden]{display:none!important}).
   - Footer always visible: source line, built date, "Counting, splitting, matching and flagging are done by this page's code; no model was called and nothing left the browser."

   Wait — `built` date: pdf_text has... the description lists `{title, symbol, doc_url, source, count, records, reference}` — no `built`. Hmm, the footer says "Source line, `built` date". pdf_text may not have `built`. I'll show `doc.built` if present, else omit or show source only. Let me handle: if doc.built exists show it. The sample shows pdf_text as array without built... The description of pdf_text doesn't include built. I'll conditionally show.

   Hmm wait, also `count` is "the string '20'". I'll compute n pages from records.length anyway.

   - Tab 01 RESULT: four tiles with big serif numbers + "How this is computed" notes:
     1. Paragraphs found: n — next to "The document has: reference.paragraphs" — green when equal, red with difference.
     2. Pages flagged: n of document's pages — note "footnote text may sit inside a paragraph; see tab 03" when > 0; "The document has reference.footnotes footnotes; this version does not separate them".
     3. First words match: n of reference.paragraphs.
     4. Repairs made: n — link to repair log on tab 04 (opens it and switches to tab 04).
   
   - Tab 02 PARAGRAPHS: collapsible "Headings found: n" box above table (button aria-expanded, closed by default? "A collapsible 'Headings found: n' box above the table lists them" — I'll make it a button that toggles a list). Table: caption with message + TAB.01 monospace number. Columns: No. | Section | Page | First line | Check. Rows are buttons with aria-expanded; clicking expands in place (a detail row under it). Expanded content: full text verbatim (one block), "Show the PDF's lines" toggle revealing same text with converter's line breaks + page markers, reference first six words vs extracted (equal/different), page(s), repairs touching this paragraph, Copy citation button.
   
   Wait — "Rows are buttons with aria-expanded; clicking or pressing Enter expands the row in place, under it." So each row: a <tr> with a button? Or the row itself is a button? Tables with expandable rows: I'll make the first cell (or whole row) contain a <button> that toggles a following <tr class="detail">. Simplest accessible approach: each data row is a <tr> whose cells contain a button spanning... Hmm. Common pattern: <tr><td colspan=5><button aria-expanded>...</button></td></tr><tr hidden><td colspan=5>details</td></tr>. But the plan wants columns No. | Section | Page | First line | Check visible. So the row itself should be clickable. I'll make each <tr> contain a <button> in the first cell? That breaks the table layout... Alternative: make the whole row a button-like: put a button inside the "First line" cell that covers... Hmm.

   Better approach: each paragraph = two rows: a summary row (with a button in the No. cell? no...). Let me do: summary row has cells; the entire row is wrapped: I can't put a button around a tr. Option: use a button in each row's first cell with aria-expanded and aria-controls pointing to the detail row id, and also make the whole row clickable via JS (click on tr triggers button). Keyboard: the button is focusable, Enter/Space activates. That satisfies "rows are buttons with aria-expanded" reasonably. Actually cleaner: put the button as the content of the first cell (No.), styled to fill, and add click handler on the row. Hmm, but then only the number cell looks clickable. Alternatively make the "First line" cell contain the button. 

   Let me do this: summary row: `<tr class="prow" data-id> <td class="num"><button aria-expanded="false" aria-controls="detail-N">12</button></td> <td>section</td> <td>3–4</td> <td class="firstline">…</td> <td class="check">OK</td> </tr>` and clicking anywhere on the row toggles (JS: row.addEventListener('click', ...)). The button provides keyboard access. Detail row: `<tr id="detail-N" hidden><td colspan="5">…</td></tr>`. Good.

   - Tab 03 FLAGGED PAGES: note above table; one row per flagged page: Page | Paragraph | Suspect lines | Why. Clicking a row shows the page's raw lines with suspect ones highlighted and the paragraph they sit in. So expandable rows again: detail shows raw lines of that page (monospace, suspect highlighted) + which paragraph. When no page flagged: one line saying so.

   - Tab 04 CHECKS & METHOD: check panel open (every check one line). Then closed heading "Repair log (n)" (button aria-expanded) → table Page | Paragraph or footnote | What was done | Before | After, with count per kind above it. Then closed heading "Raw pages" (button aria-expanded) → select "Show raw page n" + monospaced panel with line numbers, colored by classification, legend. Then Download button → CSV.

   CSV: columns number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, flagged, suspect_lines, repairs, citation, symbol, doc_url (+ text_lines). UTF-8 BOM, every field double-quoted, inner quotes doubled, CRLF, Blob URL, filename from symbol with slashes → hyphens (e.g. "E-C.12-GC-27-paragraphs.csv"). 

   suspect_lines in CSV: e.g. "p.3 L12: '7 E/2003/22…'; ..." — I'll format as "page:line text" joined by " ; ". repairs: kinds joined.

   Now, the "Show the PDF's lines" toggle: reveals the same text with the converter's line breaks and the page number where each page began. So render each original line, prefixed with "[p. N]" when the page changes, in monospace. Suspect lines highlighted.

   Raw page viewer (tab 04): select with pages; panel shows lines with line numbers on left, colored by cls, letter code in margin (C=cover, H=header, T=heading? hmm letters: cover C, header H, heading G? Let me pick: cover=C, header=D (doc header)? Let me use: cover "CV"? single letters: cover=C, header=H, heading=T (title)? paragraph=P, suspect=S, footer=F. Legend shows each with color + letter + name. Blank lines: show as blank (no color) — or a faint dot. I'll render blank lines as empty rows (maybe with a faint "·"). Keep simple: blank lines rendered as empty line with line number.

   Colors: six pale tints. On paper background #f4f0e8: 
   - cover: pale blue #e3e9f2? Hmm "pale tints" — let me choose: cover #e8e4f0 (pale violet), header #dfe7ee (pale blue), heading #f0e6d2 (pale amber), paragraph #e7efe4 (pale green), suspect #f6dde0 (pale red), footer #e6e2da (pale grey). Each doubled by letter code. Text stays near-black for contrast.

   Now the multi-document rail: scan Object.keys(WORKSHOP_DATA) for values that are objects with Array.isArray(v.records) && v.reference. Order: "in the order of the data" — Object.keys order. pdf_text, pdf_text_2. Each card: symbol, title (short — maybe first ~60 chars), adopted, n pages. Then big numbers: paragraphs found / of reference.paragraphs with bar; pages flagged; checks pass. Clicking a card re-runs everything for that document and re-renders all tabs. Default selected: the first (pdf_text) — or the one named pdf_text? "Today there is one" — I'll default to the first found, but prefer key 'pdf_text' if present. Actually the attached file is pdf_text, so default select 'pdf_text' if present else first.

   Since the pipeline runs per document, I'll structure: `const docs = discoverDocs(); let current = ...; let result = null; function selectDoc(key) { result = parseDocument(docs[key]); renderAll(); }`.

   Performance: pdf_text_2 has 18 pages, similar size. Fine.

   Now, header line: "A monospace label 'UN DOCUMENT · PDF TEXT'". For pdf_text_2, maybe "UN DOCUMENT · PDF TEXT" too (it's the same kind). Fine, static label.

   Title: doc.title (serif). One line: symbol linked to doc_url, "adopted {reference.adopted}", "n pages of raw converter text", source. E.g. "E/C.12/GC/27 · adopted 6 November 2025 · 20 pages of raw converter text · source: ...". What's `source`? The description says pdf_text has `source`. I don't know its value; render doc.source if present.

   The one-sentence description under header: "This page splits the converter's raw text into the document's numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's reference, and lists every repair it made."

   Now let me think about the checks in detail and how to render "one line" each:

   Check panel format: each check = one line: name, what was compared, the two values, and "pass" (green) or "check failed" (red, link to rows). E.g.:
   - "Paragraph count — found 90 vs reference 90 — pass"
   - "Numbering — numbers run 1–90 with no gaps or duplicates — pass" (or list gaps)
   - "First words — 90 of 90 paragraphs match reference.first_words — pass" (or list mismatches with links to tab 02 rows)
   - "Suspect lines — 141 suspect lines on 20 pages in 20 paragraphs; all still present in the text — pass" (the check is that none was removed)
   - "Pages flagged — 20 pages flagged (footnote text may sit inside a paragraph); a flag is not a failure — pass"? Hmm, is this a pass/fail check? The plan: "Pages flagged. The pages with suspect lines inside a paragraph and the paragraphs over 300 words, each listed with its page and paragraph. A flag is not a failure". So this check is informational — always "pass" in the sense that the flagging worked? I'll mark it "pass" when the flagging is consistent (every flagged page listed), i.e., always pass but lists pages. Hmm. Let me make it: "Pages flagged — n pages listed on tab 03 — pass (a flag is not a failure)". OK.
   - "Headers and footers — 20 of 20 pages opened with the symbol; 19 of 20 footers carried the page number (page 1 has none); 12 bare numbers removed from footers (listed) — pass" — hmm, is a missing page number on page 1 a failure? "expected all but the first" — so expected. Bare numbers removed: expected on this file (12), listed. Pass if all pages had header symbol and all but first had page number. I'll compute: headerOK = pages where first non-empty line === symbol; pageNumOK = pages (except page 1... actually "expected all but the first") with footer page number. Hmm, how do I know which page is "first"? records[0].page. I'll treat the first record's page as expected to lack a page number. Pass if headerOK == all pages and pageNumOK == all pages except the first record's page. Bare numbers listed (informational).
   - "Headings — n labelled, m unlabelled; unlabelled listed: … — pass" (informational; pass unless... always pass, it's a listing). Hmm, but a heading mistaken could be a failure? The plan says the check lets "a reader spot a paragraph's last line mistaken for a heading" — informational. I'll mark pass with the list.
   - "Nothing lost — n non-empty lines classified: cover a, header b, heading c, paragraph d (of which s suspect), footer e; a+b+c+d+e = n — pass" (fail if mismatch, listing unclassified).

   So 8 checks. m = 8. Pass count etc.

   Hmm wait — "First words" check when reference missing → "not run". Then m should maybe still be 8 with 1 not run. Header: "7 of 8 checks pass · 1 not run"? The plan says tiles say "no reference in this file" and checks that need it show "not run", never "pass". For the header dot: green if no failures. I'll compute failed = checks with status 'fail'; notRun separate. Header: if failed>0 → red "n checks failed"; else green "n of m checks pass" (counting only run checks? or all?). I'll do: green "n of m checks pass" where n = passed, m = run checks (passed+failed). If some not run, append "· k not run". Keep it simple.

   Now — the reference for pdf_text: `reference.paragraphs` = 90, `footnotes` = 141, `adopted`, `first_words` keyed by string. Note: the user's "What I found" says reference.paragraphs is 90 for pdf_text (E/C.12/GC/27) — wait, the description at top says "reference lets an app check its own result: paragraphs (how many numbered paragraphs the document has)" and mentions E/C.12/GC/27 has... the user says 90 paragraphs, 141 footnotes. But the earlier dataset description said "the 20 pages of E/C.12/GC/27" with reference — and pdf_text_2 is CCPR/C/GC/32 with 65 paragraphs, 128 footnotes. OK, whatever — read from data.

   Now, an important detail: the sample shows `WORKSHOP_DATA.pdf_text` as an ARRAY of records, not an object! The sample JSON at the bottom shows `"pdf_text": [ {page:1, text:...} ]`. But the description says it's `{title, symbol, doc_url, source, count, records, reference}`. Conflict! The sample says "Sample records per dataset: five of the recommendations, a few of the others" — so the sample shows pdf_text as just the records array (a sample of records), maybe eliding the wrapper. Hmm, risky. The description is explicit: "`WORKSHOP_DATA.pdf_text`: one UN document as raw text from its PDF — `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {...}}`". I'll trust the description but handle the array case defensively: if the value is an array, treat it as records with unknown title/symbol (fallback: symbol from... hmm). Let me write a normalizer:

   ```js
   function normalizeDoc(v) {
     if (Array.isArray(v)) return {records: v, reference: null, title: '(untitled)', symbol: '', doc_url: '', source: ''};
     if (v && Array.isArray(v.records)) return v;
     return null;
   }
   ```
   And discovery: keys where normalizeDoc(v) && v.reference (object with reference). If pdf_text were a bare array, it has no reference → wouldn't be discovered. Hmm. But per description it has reference. I'll also handle: if array, look for a sibling? No. Trust the description; the sample is just showing records. Actually, to be extra safe, I could also check `WORKSHOP_DATA.pdf_text.records` — if the top-level is an object with records, use it. That's the described shape. Go with it.

   Also `count` is the string "20" — I'll use records.length.

   Now, let me also handle `reference.first_words` possibly missing → first-words check "not run", tiles say "no reference in this file"? The plan: "If reference or one of its fields is missing, the tiles say 'no reference in this file' and the checks that need it show 'not run'". So per-field: if reference missing entirely → tiles say "no reference in this file". If reference.paragraphs missing → that tile says no reference? I'll handle per-field gracefully: paragraphs tile: if reference && reference.paragraphs != null → compare; else "no reference in this file". First words tile: if reference && reference.first_words → n of reference.paragraphs (or of found?) — "First words match: n of reference.paragraphs" — hmm, n of reference.paragraphs... if found count differs from reference, match count is over found paragraphs that have a reference entry. I'll compute matches over paragraphs that have reference.first_words[String(num)]; display "n of m" where m = number of paragraphs with a reference entry (or reference.paragraphs). Plan says "n of reference.paragraphs". I'll use m = reference.paragraphs if present else count of paragraphs with reference entries. Eh — simpler: m = number of reference entries available; but plan explicitly says "of reference.paragraphs". Use reference.paragraphs when present.

   Now the CSV download:

   ```js
   function downloadCSV() {
     const cols = ['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','text_lines','flagged','suspect_lines','repairs','citation','symbol','doc_url'];
     const esc = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
     const rows = [cols.map(esc).join(',')];
     for (const p of result.paragraphs) {
       rows.push([p.number, p.section, p.part, p.page_start, p.page_end, p.firstWordsRef ?? '', p.firstWordsFound, p.firstWordsMatch === null ? '' : (p.firstWordsMatch ? 'yes' : 'no'), p.text, p.textRaw, p.textLines, p.flagged ? 'yes':'no', p.suspectDesc, p.repairKinds, p.citation, symbol, doc_url].map(esc).join(','));
     }
     const csv = '\uFEFF' + rows.join('\r\n') + '\r\n';
     const blob = new Blob([csv], {type: 'text/csv;charset=utf-8'});
     const a = document.createElement('a');
     a.href = URL.createObjectURL(blob);
     a.download = symbol.replace(/\//g, '-') + '-paragraphs.csv';
     a.click(); URL.revokeObjectURL(a.href);
   }
   ```

   Now the tabs with arrow-key navigation:

   ```js
   tablist.addEventListener('keydown', e => {
     if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
       const tabs = [...tablist.querySelectorAll('[role=tab]')];
       let i = tabs.indexOf(document.activeElement);
       if (i < 0) return;
       const d = e.key === 'ArrowRight' ? 1 : -1;
       const j = (i + d + tabs.length) % tabs.length;
       tabs[j].focus(); tabs[j].click();
       e.preventDefault();
     }
   });
   ```
   And each tab: role="tab", aria-selected, aria-controls; panels role="tabpanel", hidden when inactive. Use `hidden` attribute + CSS `[hidden]{display:none!important}`.

   Now rendering. Since re-render on document switch, I'll build DOM via template strings + innerHTML for the tab panels, and attach event listeners after. Careful with quotes in text — escape HTML! Paragraph texts contain quotes, <, >? Possibly. I must escape: `escHtml(s)`. Important.

   Let me now also handle the "Repairs made: n" tile link → switches to tab 04 and opens the repair log heading. I'll implement `openRepairLog()` that activates tab 04 and sets the repair log button aria-expanded=true and shows the table.

   Also rail links: "n pages flagged" links to tab 03; "n of m checks pass" links to tab 04.

   Now, let me think about the parse more carefully with the actual data shape. Page 1 sample text:

   ```
   E/C.12/GC/27
   (blank)
   United Nations
   (blank)
   Economic and Social Council
   (blank)
   Distr.: General
   6 November 2025
   Original: English
   (blank)
   Committee on Economic, Social and Cultural Rights
   (blank)
   General comment No. 27 (2025) on economic, social and
   cultural rights and the environmental dimension of
   sustainable development*
   I.
   (blank)
   Introduction
   1.
   A clean, healthy and sustainable environment is an essential precondition for the
   ...
   ```

   Wait — the sample shows "sustainable development*\nI.\n\nIntroduction\n1.\n..." — is there a blank between "sustainable development*" and "I."? The sample text: "...sustainable development*\nI.\n\nIntroduction\n1.\nA clean..." — from the JSON: `"sustainable development*\nI.\n\nIntroduction\n1.\nA clean, healthy..."`. Hmm, looking at the sample: `sustainable development*\nI.\n\nIntroduction\n1.\n` — actually in the sample it's "...dimension of\nsustainable development*\nI.\n\nIntroduction\n1.\nA clean, healthy and sustainable environment..." Let me re-read the sample: 

   "General comment No. 27 (2025) on economic, social and\ncultural rights and the environmental dimension of\nsustainable development*\nI.\n\nIntroduction\n1.\nA clean, healthy and sustainable environment is an essential precondition for the\nenjoyment..."

   Yes. So "I." comes right after the title line (no blank). My state machine: mode='cover', lines: "United Nations" → cover... "I." matches labelRe1 → heading. Good, cover = lines before "I.". Then heading collection: skip blanks after "I." → "Introduction" (text line, first title) → next line "1." is parastart → stop. heading I. title = "Introduction". Then "1." parastart → paragraph 1. 

   But wait — the unlabelled heading check: "Introduction" is immediately followed by "1." (parastart) and matches unlabelled criteria — but we're in heading-collection mode, so it's consumed as heading title. In my walk, the heading collection consumes lines j from i+1; I set i = j-1 so the outer loop continues at the parastart. Good.

   Hmm, but one problem: in heading collection I break on `labelOf(nl)` — any label. But what if a title line is like "A. something" (labelRe2)? In heading mode, labelRe2... my labelOf returns {label, title} for both forms; I break on any labelOf match. But wait — in heading collection, could a title continuation line start with "A. "? Unlikely. OK.

   Also in heading collection, should I check unlabelled heading for the last title line? Per plan, no — "every line up to the next label line or paragraph start is heading text". OK.

   Now, what about the cover: lines "E/C.12/GC/27" (header, removed), then "United Nations", "", "Economic and Social Council", "", "Distr.: General", "6 November 2025", "Original: English", "", "Committee on Economic, Social and Cultural Rights", "", "General comment No. 27 (2025) on economic, social and", "cultural rights and the environmental dimension of", "sustainable development*" → all cover. Then "I." heading. 

   Wait — "6 November 2025" is in cover mode, so not suspect. Good (plan mentions this).

   Footer of page 1: "GE.25-15926 (E)" and "051125 061125" — my footer loop: from end, lines... page 1's last lines per plan: "GE.25-15926 (E)" and date stamp "051125 061125". Order varies. My loop checks: empty → drop; /^GE\./ → drop; 6-digit groups → drop; bare 1-3 digits → drop. "GE.25-15926 (E)" starts with "GE." → dropped. "051125 061125" matches 6-digit groups → dropped. Good. But careful: what if the last line is a bare number that's the page number "1"? Page 1 has no page number per plan ("pages 2 to 20" have page number alone; page 1 has GE + date stamp instead). OK.

   Hmm wait, one more: the footer loop condition — "drop lines while the line is empty, starts with 'GE.', consists only of 6-digit groups, or is a bare number of one to three digits". What if a page ends with footnote text then footer? Footnote text lines don't match → loop stops at first footnote text line from the end... wait no, the loop goes from the END backwards. The last lines are footer (GE., page number, date stamp). It drops them until it hits a non-matching line (footnote text or paragraph text). Good.

   But danger: what if a footnote text line is a bare number? Footnote first lines are "bare number on its own line" per plan! "the first is a bare number on its own line, a blank line, then the text". So a page's footnote block starts with e.g. "6" alone on a line. If the footer loop reaches that bare number (i.e., all lines after it are footer)... wait, the footnote block is BEFORE the footer. The loop from the end drops footer lines, then hits footnote text (last footnote's text) — not a bare number → stops. Unless the last footnote's text is... no, footnote text is prose. But what if the page ends with: footnote text, blank, "6" (bare number, displaced footnote number in footer), "GE.25-15926", "3" (page number)? Then the loop drops "3" (page number), "GE...", "6" (bare number ≠ page → logged as bare number removed from footer), blank, then footnote text → stops. That's exactly the described behavior: the displaced footnote number sits in the footer and gets removed + logged. 

   But wait — the plan says on 12 pages "a third bare number sits in the footer: a footnote number the converter displaced... that footnote's text on the page has no number." So the bare number in the footer is the footnote's number, displaced. And the footnote text (without number) stays in the body → becomes a suspect line inside the paragraph. Right.

   Hmm, but careful: the footer loop drops bare numbers — what if the footnote block's FIRST line (bare number "6") is at the very end of the body (i.e., after it only footer lines)? Then the loop would eat it as a "bare number removed from the footer" even though it's a footnote number in the body! Per the plan's description, the displaced number sits in the footer (after the footnote text? or before?). "On 12 pages a third bare number sits in the footer" — the footer is the last lines. The footnote block is before the footer. So order: ...footnote texts..., [bare number?], GE., page number. Hmm, actually if the bare number is IN the footer (after footnote text), the loop eats it. If the footnote block's own first bare number is the last body line before footer... then it would also be eaten. Ambiguous, but the plan says the footer rule drops trailing bare numbers and logs non-page ones as "bare number removed from the footer" — exactly what I do. The consequence: that footnote's number line is removed from body (logged), and its text remains → suspect line. That matches "that footnote's text on the page has no number" — wait, no: if the number was displaced to the footer, the text has no number, and the number in the footer is removed+logged. But if the footnote block's first line is a bare number at the end of the body... hmm, the footnote block is "bare number, blank, text" — the number comes BEFORE the text, so the text is after it, so the loop from the end hits text first. So the block's own number is safe. Only truly trailing bare numbers get eaten. Good.

   Now suspect line detection: footnote block inside a paragraph: e.g. paragraph text lines, then "6" (bare number — wait, if the footnote's number was displaced to footer, the text has no number; the first suspect line would be the footnote TEXT line, e.g. "E/2003/22 ..." hmm). Let me re-read: "Each page's footnotes sit at the foot, before the footer: the first is a bare number on its own line, a blank line, then the text; the others start with their number and a space ('7 E/2003/22…'). 129 keep their number; on 12 pages the number was displaced to the footer and the footnote text has none."

   So on most pages, the footnote block inside the paragraph region looks like:
   ```
   ...paragraph text...
   6
   (blank)
   Footnote text...
   7 E/2003/22 more text...
   8 Another footnote...
   ```
   The first suspect line = "6" (bare number, no full stop) → matches suspect rule 1. Then every line after it to end of page is suspect. Also "7 E/2003/22…" matches rule 2 anyway.

   On the 12 displaced pages, the block starts with the text without number, e.g. "E/2003/22 ..." — hmm, does that match rule 2? Rule 2: "starts with one to three digits, a space and a capital letter..." — "E/2003/22" starts with a capital but no leading digits. Hmm! Then how is it flagged? "on each page the first suspect line is that page's first footnote number, never a line of paragraph text" — wait, the user says "Tried on this file, the suspect-line rule below flags all 20 pages (every page has footnotes), and on each page the first suspect line is that page's first footnote number". So on every page, the first suspect line is a footnote NUMBER line. On the 12 displaced pages... hmm, the number was displaced to the footer — but the user says the first suspect line is the page's first footnote number. Maybe on displaced pages, the first footnote's number is in the footer but a LATER footnote keeps its number ("7 E/...")? Or maybe the displaced number... hmm. Actually wait — re-read: "on 12 pages the number was displaced to the footer and the footnote text has none" — maybe only the FIRST footnote's number is displaced (the bare-number-first pattern), and the others keep theirs. So the first suspect line on those pages would be "7 E/2003/22…" (the second footnote, which has its number). Hmm, but the user says "the first suspect line is that page's first footnote number" — loosely meaning a footnote number line. Whatever — my rules handle both: bare number lines and "N Text" lines are suspect. On displaced pages, the first footnote text (no number) might not match rule 2 if it starts with a capital non-digit... e.g. "E/2003/22, para. 3." — starts with "E" — rule 2 requires leading digits. Hmm, so that line wouldn't be suspect, but the NEXT line "7 E/..." would be, and then "every line after it to the end of its page" — but the first footnote's text is BEFORE "7 ..." — not marked suspect. Hmm. But the user says the rule flags all 20 pages with first suspect = first footnote number. So maybe on displaced pages the first footnote text still starts with digits? Or maybe the displaced number is not the first footnote's... 

   I shouldn't overthink — the user says the rule as stated flags all 20 pages correctly on this file. My implementation of the rule: bare 1-3 digit line (no full stop) OR line starting with 1-3 digits + space + [capital/quote/symbol-start]. Let me make rule 2 a bit broader to catch footnote text starting with a symbol: `/^\d{1,3} [A-Z"“”]/` plus maybe `/^\d{1,3} [A-Z]{2,4}\//`— covered by capital. What about footnote text starting with a lowercase or a symbol without digits? Not suspect per rule. Fine — follow the plan exactly. The plan's rule: "A line inside a paragraph is suspect when it is a bare number of one to three digits with no full stop after it, or starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". So: `/^\d{1,3}$/` OR `/^\d{1,3} ([A-Z"“”]|[A-Z]{2,}\/)/`. Since a UN doc symbol starts with capitals, `[A-Z]` covers it. I'll use `/^\d{1,3}\s+[A-Z"“”]/`. Hmm, also maybe the footnote text after a displaced number starts with the footnote's own reference like "See E/..." — starts with "See" (capital S) but no leading digits → not suspect. Then the next footnote "7 ..." is suspect and everything after. The first footnote's text lines before it wouldn't be flagged... but per user, on this file the first suspect line is always a footnote number, so fine.

   Hmm wait, actually — maybe on the 12 displaced pages, the displaced number is in the footer AND the footnote block's first line is the bare number of... no. Let me just also treat: once ANY suspect line is found in a paragraph, all following lines on that page are suspect. And also — should lines BEFORE the first suspect line on the page be suspect? No.

   OK. Also "A paragraph over 300 words is flagged too". Word count: text.split(/\s+/).length.

   Now — one more important detail: the suspect lines "stay in the text" — so paragraph text includes footnote text. First words are computed from the joined text — footnote marks at the start? No, footnotes are at the end of paragraphs. First words unaffected. Good.

   Now, "Repairs that touched this paragraph" in the expanded row: filter repairs by target containing 'para. n'. I'll tag repairs with paraNum when applicable.

   Let me now also design the "How this is computed" lines:
   - Tile 1: "How this is computed: lines matching 'N.' or 'N. text' start a paragraph; header and footer lines are removed first. Compared with reference.paragraphs."
   - Tile 2: "How this is computed: a line inside a paragraph that is a bare number or starts 'N Word' is suspect; every line after it on the same page is suspect too. The document has X footnotes; this version does not separate them."
   - Tile 3: "How this is computed: first six words of each paragraph, footnote marks (trailing digits) dropped, compared with reference.first_words after normalising quotes and dashes."
   - Tile 4: "How this is computed: every line the script removed, split, joined or separated, logged in document order on tab 04."

   Now the header status and tab 04 red dot: add a small red dot span on tab 04 label when failures.

   Let me now think about the overall HTML structure:

   ```html
   <!doctype html>
   <html lang="en">
   <head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <title>…</title>
   <style>…</style>
   </head>
   <body>
   <header class="top">
     <div class="kicker">UN DOCUMENT · PDF TEXT</div>
     <h1 id="docTitle"></h1>
     <p class="meta" id="docMeta"></p>
     <p class="what" id="docWhat"></p>
     <div class="status" id="statusBox"></div>
   </header>
   <div class="layout">
     <aside class="rail" id="rail"></aside>
     <main>
       <div class="tablist" role="tablist" id="tablist" aria-label="Sections">
         <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true">01 RESULT</button>
         ...
       </div>
       <section role="tabpanel" id="panel-1" aria-labelledby="tab-1">…</section>
       ...
     </main>
   </div>
   <footer class="foot" id="foot"></footer>
   <script>…</script>
   </body>
   </html>
   ```

   Layout: header full width; below, a flex row: rail (narrow, ~260px) + main. Footer full width. On narrow screens, stack.

   Design tokens:
   - --paper: #f4f0e8; --ink: #1d1b18; --rule: #d9d2c3; --red: #9b2335; --green: #1e6b3a (dark green for "pass", contrast on paper: #1e6b3a on #f4f0e8 — contrast? #1e6b3a is fairly dark, should be > 4.5:1. Let me use #1a6337 or #20643c. I'll use #1e6b3a.)
   - serif: Georgia, 'Times New Roman', serif; mono: ui-monospace, Menlo, Consolas, monospace; sans: system-ui, -apple-system, 'Segoe UI', sans-serif.

   Tabs: monospace uppercase letter-spaced 11-12px, bottom border rule; active: red text + red underline (2-3px). 

   Big numbers: 40-56px serif.

   Tables: full width, th monospace uppercase small, borders bottom rule, numbers right-aligned (class .num). caption: serif, left-aligned, with monospace "TAB.01" prefix.

   Focus ring: `:focus-visible { outline: 3px solid #9b2335; outline-offset: 2px; }`.

   Now let me write the parse function fully and carefully.

   ```js
   function parseDocument(doc) {
     const symbol = doc.symbol || '';
     const records = [...(doc.records || [])].sort((a, b) => (a.page - b.page));
     const ref = doc.reference || null;
     const repairs = [];
     const warnings = [];
     const allLines = [];
     const pageInfo = []; // per record: {page, lines: [{text, cls, lineNo}], headerOK, pageNumInFooter, bareRemoved: []}
     
     records.forEach(rec => {
       const raw = String(rec.text || '').split(/\r?\n/);
       const lines = raw.map((t, i) => ({ text: t, page: rec.page, lineNo: i + 1, cls: null }));
       const info = { page: rec.page, lines, headerOK: false, pageNum: false, bare: [] };
       // header
       let fi = 0;
       while (fi < lines.length && lines[fi].text.trim() === '') fi++;
       if (fi < lines.length && lines[fi].text.trim() === symbol && symbol !== '') {
         lines[fi].cls = 'header';
         info.headerOK = true;
         repairs.push({ page: rec.page, para: null, kind: 'header line removed', before: lines[fi].text.trim(), after: '' });
       } else if (fi < lines.length) {
         warnings.push('Page ' + rec.page + ': first non-empty line is not the symbol "' + symbol + '"');
       }
       // footer
       let end = lines.length;
       while (end > fi + 1) {  // hmm, end > fi? careful not to eat the header... use end > fi
         const t = lines[end - 1].text.trim();
         if (t === '') { lines[end-1].cls = 'blank'; end--; continue; }
         if (/^GE\./.test(t)) { lines[end-1].cls = 'footer'; repairs.push({page: rec.page, para: null, kind: 'footer line removed', before: t, after: ''}); end--; continue; }
         if (/^(\d{6})(\s+\d{6})*$/.test(t)) { lines[end-1].cls = 'footer'; repairs.push({page: rec.page, para: null, kind: 'footer line removed', before: t, after: ''}); end--; continue; }
         if (/^\d{1,3}$/.test(t)) {
           const n = parseInt(t, 10);
           lines[end-1].cls = 'footer';
           if (n === rec.page) { info.pageNum = true; repairs.push({page: rec.page, para: null, kind: 'footer line removed', before: t, after: ''}); }
           else { info.bare.push(n); repairs.push({page: rec.page, para: null, kind: 'bare number removed from the footer', before: t, after: ''}); }
           end--; continue;
         }
         break;
       }
       for (let i = fi + 1; i < end; i++) allLines.push(lines[i]);
       // hmm: lines between fi+1 and end that are blank get cls 'blank' in the walk; but lines before fi (leading blanks) — mark blank too.
       for (let i = 0; i < fi; i++) lines[i].cls = 'blank';
       // lines after end (footer) already cls 'footer'; blanks among them set above.
       pageInfo.push(info);
     });
     ...
   ```

   Wait, there's an issue: blank lines in the body (between fi+1 and end) — in the walk I set cls='blank' when encountered. But lines after `end` that were blank got cls='blank' in the footer loop. Lines before fi: set blank. OK, but the walk only iterates allLines (body lines). The raw viewer iterates each page's full lines array with cls set. Good — every line gets a cls: header/blank/footer set during page processing; body lines set during walk. But body blank lines: set in walk. Body lines all get cls in walk (cover/heading/paragraph/parastart→paragraph). Let me make sure the walk assigns cls to EVERY body line: blank → 'blank'; parastart → 'paragraph'; label → 'heading'; heading-collected → 'heading'; unlabelled → 'heading'; else cover or paragraph. Yes.

   Hmm, wait: in the walk, heading collection consumes lines j and sets their cls='heading'. But what if a line in the heading block is blank — I set 'blank' and continue. OK.

   Now the walk:

   ```js
   const paragraphs = [];
   const headings = [];
   const coverLines = [];
   let mode = 'cover';
   let cur = null;
   let partLabel = null, partTitle = null;   // current roman part
   let sectionTitle = null, sectionFull = null; // nearest heading
   
   const isBlankL = l => l.text.trim() === '';
   const psOf = l => {
     let m = l.text.match(/^(\d{1,3})\.$/);
     if (m) return { num: +m[1], inline: null };
     m = l.text.match(/^(\d{1,3})\. (.+)$/);
     if (m) return { num: +m[1], inline: m[2] };
     return null;
   };
   const labOf = l => {
     let m = l.text.match(/^([IVX]+|[A-Z])\.$/);
     if (m) return { label: m[1], title: null };
     m = l.text.match(/^([IVX]+|[A-Z])\.\s+(.+)$/);
     if (m) return { label: m[1], title: m[2] };
     return null;
   };
   const isUnlab = (l, next) => {
     if (!next) return false;
     if (!psOf(next)) return false;
     const t = l.text.trim();
     if (t.length === 0 || t.length > 90) return false;
     if (!/^[A-Z]/.test(t)) return false;
     if (/[.;:,]$/.test(t) || /\d$/.test(t)) return false;
     return true;
   };
   
   for (let i = 0; i < allLines.length; i++) {
     const l = allLines[i];
     if (isBlankL(l)) { l.cls = 'blank'; continue; }
     const ps = psOf(l);
     if (ps) {
       if (cur) paragraphs.push(cur);
       l.cls = 'paragraph';
       cur = { number: ps.num, lines: [], pages: [], pageSet: new Set(), section: sectionTitle, path: sectionFull, part: partLabel ? (partLabel + ' ' + (partTitle || '')).trim() : '', flagged: false, suspect: [], repairs: [] };
       cur.pages.push(l.page); cur.pageSet.add(l.page);
       if (ps.inline !== null) {
         const il = { text: ps.inline, page: l.page, lineNo: l.lineNo, cls: 'paragraph' };
         cur.lines.push(il);
         repairs.push({ page: l.page, para: ps.num, kind: 'number and text split', before: l.text.trim(), after: ps.num + '. ‖ ' + ps.inline });
       }
       mode = 'paragraph';
       continue;
     }
     const lab = labOf(l);
     if (lab && (lab.title === null || mode !== 'paragraph')) {
       if (cur) { paragraphs.push(cur); cur = null; }
       l.cls = 'heading';
       const h = { label: lab.label, titleLines: lab.title ? [lab.title.trim()] : [], page: l.page, kind: 'labelled' };
       headings.push(h);
       // collect title lines
       let j = i + 1;
       let first = lab.title === null; // if title came inline, first title line already set
       while (j < allLines.length) {
         const nl = allLines[j];
         if (isBlankL(nl)) { nl.cls = 'blank'; j++; continue; }
         if (psOf(nl) || labOf(nl)) break;
         nl.cls = 'heading';
         const t = nl.text.trim();
         if (h.titleLines.length === 0) { h.titleLines.push(t); }
         else if (/^[a-z(]/.test(t)) {
           const prev = h.titleLines[h.titleLines.length - 1];
           h.titleLines[h.titleLines.length - 1] = prev + ' ' + t;
           repairs.push({ page: nl.page, para: null, kind: 'heading title joined from two lines', before: prev + ' ⏎ ' + t, after: prev + ' ' + t });
         } else {
           h.titleLines.push(t);
         }
         j++;
       }
       h.title = h.titleLines.join(' › ');
       if (/^[IVX]+$/.test(h.label)) {
         partLabel = h.label + '.';
         partTitle = h.title;
         sectionTitle = h.title || (h.label + '.');
         sectionFull = h.label + '. ' + h.title;
       } else {
         sectionTitle = (h.label + '. ' + h.title).trim();
         sectionFull = (partLabel ? partLabel + ' ' + (partTitle ? partTitle + ' › ' : '') : '') + h.label + '. ' + h.title;
       }
       i = j - 1;
       mode = 'heading';
       continue;
     }
     if (mode !== 'heading' && isUnlab(l, allLines[i + 1])) {
       if (cur) { paragraphs.push(cur); cur = null; }
       l.cls = 'heading';
       const h = { label: null, titleLines: [l.text.trim()], page: l.page, kind: 'unlabelled' };
       headings.push(h);
       h.title = h.titleLines[0];
       sectionTitle = h.title;
       sectionFull = (partLabel ? partLabel + ' ' + (partTitle ? partTitle + ' › ' : '') : '') + h.title;
       repairs.push({ page: l.page, para: null, kind: 'heading separated from paragraph text', before: l.text.trim(), after: '(treated as a heading, not paragraph text)' });
       mode = 'heading';
       continue;
     }
     if (mode === 'cover' || cur === null) {
       l.cls = 'cover';
       coverLines.push(l);
     } else {
       l.cls = 'paragraph';
       cur.lines.push(l);
       if (!cur.pageSet.has(l.page)) { cur.pageSet.add(l.page); cur.pages.push(l.page); }
     }
   }
   if (cur) paragraphs.push(cur);
   ```

   Hmm wait, there's a bug: `if (mode === 'cover' || cur === null)` — after a heading, mode='heading' and cur=null; a text line then would go to cover. But per the labelled-heading collection, all text lines after a label are consumed as heading text until parastart/label, so mode='heading' with a stray text line shouldn't happen... except the unlabelled case sets mode='heading' and the next line is a parastart. OK. But what if mode==='heading' and next line is text (not parastart/label)? That would have been consumed by collection. Except after an unlabelled heading — next line is parastart by definition. OK. But to be safe, treat mode==='heading' stray text as heading too? Hmm — if it happens, it'd be misclassified as cover. Let me change: `if (mode === 'cover') cover; else if (cur) paragraph; else { l.cls='heading'; headings... }` — hmm, complicated. Actually let me make stray text after heading (cur===null, mode!=='cover') classified as 'heading' appended to the last heading's title? That could swallow real text. Given the structure, it shouldn't happen. I'll classify as 'cover' fallback but count it — the nothing-lost check will show counts; fine. Actually wait, there IS a case: mode='heading' after unlabelled heading, next line is parastart — handled. After labelled heading collection, i=j-1 and allLines[j] is parastart or label — handled. So stray text with cur===null only in cover mode. OK, `if (mode === 'cover' || cur === null)` → cover. Fine.

   Hmm, another subtle bug: when a labelled heading appears while cur is open (mid-paragraph "A." line), I push cur and set cur=null. But the paragraph's last lines were already added. Good. But what about the unlabelled heading case — the line is NOT added to cur (correct, it's a heading), and cur is pushed. Good.

   Wait, but there's an issue with the unlabelled heading check placement: it's checked when mode !== 'heading'. But what if mode === 'paragraph' and the line is a genuine last line of paragraph that happens to match? Accepted per plan.

   Also: what if a parastart line appears while mode==='cover' (first paragraph)? cur=null → create paragraph. Good.

   Now post-processing paragraphs:

   ```js
   paragraphs.forEach(p => {
     // join across page break repair
     if (p.pageSet.size > 1) {
       repairs.push({ page: p.pages[p.pages.length-1], para: p.number, kind: 'paragraph joined across a page break', before: 'page break after p. ' + p.pages[0] + ' …', after: 'joined into para. ' + p.number + ' (pp. ' + p.pages.join('–') + ')' });
     }
     p.page_start = p.pages[0];
     p.page_end = p.pages[p.pages.length - 1];
     p.textRaw = p.lines.map(l => l.text).join('\n');  // hmm: original lines including the parastart line? 
     ...
   });
   ```

   Hmm — text_raw: "the same text with the converter's line breaks" — for the toggle "Show the PDF's lines" reveals the same text with the converter's line breaks and the page number where each page began. So the raw lines should include the paragraph number line? The paragraph's lines: I stored inline text separately for the split case; for the alone case, the parastart line "23." is not in p.lines. For the raw view, I want to show "23." then the text lines. Let me store p.startLine = the parastart line object, and p.lines = text lines (including inline). Then:
   - textRaw = (startLine ? startLine.text + '\n' : '') + lines.map(text).join('\n')? Hmm, but for the split case the startLine text is "23. Some text" — raw shows that whole line. OK: textRaw = [startLine, ...lines].map(l => l.text).join('\n'). And the "PDF's lines" toggle shows these lines with page markers.
   - text = normalized join: for the split case, the first line contributes only the inline part. So: parts = []; if startLine: if inline !== null → parts.push(inline) else parts.push('') hmm — for the alone case, the number line contributes nothing to text. Let me store p.inline (null or string). text = ([p.inline ?? '', ...p.lines.map(l => l.text.trim())].join(' ')).replace(/\s+/g, ' ').trim(). Wait but lines' text may have leading/trailing spaces — trim each. And collapse. OK.

   Actually hold on — for the alone case ("23." then text on next line), p.lines[0] is the first text line. text = lines joined. For split case, p.lines[0] is the inline object I created. So text = p.lines.map(l => l.text.trim()).join(' ').replace(/\s+/g,' ').trim() — where for the split case I already pushed the inline as a line. And for the alone case the number line isn't in p.lines. 

   But wait — I need p.startLine for the raw view and for page_start. I set cur.pages from the parastart line. Let me store p.startLine = l. And textRaw includes it. For text, exclude it (or include only inline). OK.

   - textLines (CSV " | " separated): p.lines.map(l => l.text.trim()).join(' | ')? Or raw with original spacing? "keeps the original lines" — I'll use the raw line texts (untrimmed? trimmed?) joined with ' | '. I'll use trimmed to keep CSV clean. Hmm, "original lines" — I'll keep l.text as-is (not trimmed) joined with ' | '. Eh, trailing spaces are noise; trim. Fine.

   - Suspect lines: iterate p.lines in order; track suspecting = false; for each line: if !suspecting and (bare number or digit-start pattern) → suspecting = true, mark line.suspect = true, record suspect entry {page, lineNo, text}. If suspecting and line.page === suspectStartPage → mark suspect too. Wait: "A suspect line and every line after it to the end of its page are suspect". So once triggered at page X, all subsequent lines with page === X are suspect. Lines on later pages: not suspect. Implement:
   
   ```js
   let triggered = false, trigPage = null;
   for (const l of p.lines) {
     const t = l.text.trim();
     if (!triggered && (/^\d{1,3}$/.test(t) || /^\d{1,3}\s+[A-Z"“”]/.test(t))) {
       triggered = true; trigPage = l.page;
       l.suspect = true;
       p.suspect.push({ page: l.page, lineNo: l.lineNo, text: t });
     } else if (triggered && l.page === trigPage) {
       l.suspect = true;
       p.suspect.push({ page: l.page, lineNo: l.lineNo, text: t });
     }
   }
   ```
   
   Hmm wait — should the parastart inline line be checked for suspect? It starts with the number + ". " — has a full stop, so no. Skip.
   
   Hmm, also: what about suspect lines in a paragraph that continues from a previous page where triggering happened? E.g., paragraph spans pages 3-4, footnotes on page 3 trigger; page 4 lines not suspect. But what if footnotes are on page 4 (paragraph starts page 3, footnotes at foot of page 4)? Then trigger on page 4. Fine.
   
   But subtle: what if the paragraph's lines on page 3 include a suspect trigger, and the paragraph continues on page 4 — page 4 lines not suspect. But what if there are footnotes on page 4 too? They'd start with a bare number or "N Text" → trigger again (triggered already true, trigPage=3; line on page 4: `triggered && l.page === trigPage` false → not marked!). Bug. Fix: allow re-trigger: if the line matches the suspect pattern itself, mark it suspect regardless; and if triggered and same page as the most recent trigger, mark. Let me restructure:
   
   ```js
   let trigPage = null;
   for (const l of p.lines) {
     const t = l.text.trim();
     const selfSuspect = /^\d{1,3}$/.test(t) || /^\d{1,3}\s+[A-Z"“”]/.test(t);
     if (selfSuspect) { trigPage = l.page; l.suspect = true; p.suspect.push(...); }
     else if (trigPage !== null && l.page === trigPage) { l.suspect = true; p.suspect.push(...); }
   }
   ```
   
   Good.
   
   - words = p.text.split(/\s+/).length; if words > 300 → p.overWords = true.
   - p.flagged = p.suspect.length > 0 || p.overWords.
   - first words: 
   ```js
   const toks = p.text.split(/\s+/).map(t => t.replace(/\d+$/, '')).filter(t => t !== '');
   p.firstWordsFound = toks.slice(0, 6).join(' ');
   const refFW = ref && ref.first_words ? ref.first_words[String(p.number)] : null;
   p.firstWordsRef = refFW ?? null;
   p.firstWordsMatch = refFW == null ? null : norm(p.firstWordsFound) === norm(refFW);
   ```
   norm: `s.replace(/[“”]/g, '"').replace(/[‘’]/g, "'").replace(/[–—]/g, '-').replace(/\s+/g, ' ').trim()`.
   
   Hmm wait — "dropping tokens that are only digits and digits glued to the end of a word ('waste.2' becomes 'waste.')" — my map strips trailing digits from every token then filters empty. "2" → "" → dropped. "waste.2" → "waste.". But what about a token like "2025." — ends with '.', no trailing digit → kept as "2025.". Hmm, "6 November 2025" — but that's cover. In paragraph text, a year "2025" alone → dropped. OK per rule.
   
   Wait, but there's a subtlety: should the stripping apply only to the first six tokens or the whole stream before slicing? "the first six whitespace-separated words of the joined text, after dropping tokens that are only digits..." — the dropping applies to the token stream, then take six. My approach: map+filter all, then slice(0,6). Same result. OK.

   - citation = symbol + ', para. ' + p.number.
   - p.repairs = repairs.filter(r => r.para === p.number) — I'll collect after all repairs; or tag during. I'll do a post-pass: p.repairList = repairs.filter(r => r.para === p.number).

   - flaggedPages: 
   ```js
   const flaggedPages = new Map(); // page -> {page, suspects: [...], paras: Set, over: []}
   paragraphs.forEach(p => {
     p.suspect.forEach(s => { add to flaggedPages[s.page] });
     if (p.overWords) p.pages.forEach(pg => add over para);
   });
   ```
   Tab 03 rows: one per flagged page: Page | Paragraph(s) | Suspect lines (count) | Why ("starts with a number and a space", "bare number", "paragraph over 300 words"). Why per suspect line: classify each suspect line: bare number → "bare number"; else "starts with a number and a space". I'll show why as the distinct reasons joined.

   Hmm, the plan's tab 03 columns: Page | Paragraph | Suspect lines | Why. "Suspect lines" = count or list? I'll show count + short preview. Clicking row expands: page's raw lines with suspect highlighted + the paragraph they sit in. I'll render the page's lines (from pageInfo) with cls colors, suspect ones highlighted, and note which paragraph(s) contain them.

   - Checks:
   
   ```js
   const checks = [];
   // 1 paragraph count
   const refParas = ref ? ref.paragraphs : null;
   checks.push({ name: 'Paragraph count', detail: `found ${paragraphs.length} vs reference ${refParas ?? '—'}`, status: refParas == null ? 'notrun' : (paragraphs.length === refParas ? 'pass' : 'fail'), link: '#tab-2' });
   // 2 numbering
   let numOK = true; const gaps = [];
   paragraphs.forEach((p, idx) => { if (p.number !== idx + 1) { numOK = false; gaps.push(`para. ${p.number} at position ${idx+1} (p. ${p.page_start})`); } });
   // duplicates: check set size
   checks.push({ name: 'Numbering', detail: numOK ? `numbers run 1–${paragraphs.length} with no gaps or duplicates` : 'gaps/duplicates: ' + gaps.join('; '), status: numOK ? 'pass' : 'fail', link: '#tab-2' });
   ```
   
   Hmm, "The paragraph numbers are exactly 1 to n in order" — n = found count. If found 90 and they're 1..90 → pass. Duplicates: if numbers repeat, the sequence check catches it (p.number !== idx+1). OK.
   
   ```js
   // 3 first words
   const fwParas = paragraphs.filter(p => p.firstWordsRef != null);
   const fwMismatch = fwParas.filter(p => !p.firstWordsMatch);
   checks.push({ name: 'First words', detail: ref && ref.first_words ? `${fwParas.length - fwMismatch.length} of ${fwParas.length} match reference.first_words` + (fwMismatch.length ? '; mismatches: ' + fwMismatch.map(p => `para. ${p.number}: found “${p.firstWordsFound}” / reference “${p.firstWordsRef}”`).join('; ') : '') : 'no first_words in reference', status: !(ref && ref.first_words) ? 'notrun' : (fwMismatch.length === 0 ? 'pass' : 'fail'), link: '#tab-2' });
   // 4 suspect lines
   const allSuspects = []; paragraphs.forEach(p => p.suspect.forEach(s => allSuspects.push({ ...s, para: p.number })));
   const suspectPages = new Set(allSuspects.map(s => s.page));
   const suspectParas = new Set(allSuspects.map(s => s.para));
   // verify none removed: each suspect line's text appears in its paragraph's textRaw
   const stillThere = allSuspects.every(s => { const p = paragraphs.find(pp => pp.number === s.para); return p && p.textRaw.includes(s.text); });
   checks.push({ name: 'Suspect lines', detail: `${allSuspects.length} suspect lines on ${suspectPages.size} pages in ${suspectParas.size} paragraphs; ${stillThere ? 'all still present in the paragraph text (none removed)' : 'SOME REMOVED'}`, status: stillThere ? 'pass' : 'fail', link: '#tab-3' });
   // 5 pages flagged
   checks.push({ name: 'Pages flagged', detail: `${flaggedPages.size} pages flagged (${[...flaggedPages.keys()].sort((a,b)=>a-b).join(', ')}); a flag is not a failure — it marks where footnote text may sit inside a paragraph`, status: 'pass', link: '#tab-3' });
   // 6 headers/footers
   const headerOK = pageInfo.filter(p => p.headerOK).length;
   const firstPage = records.length ? records[0].page : null;
   const pageNumOK = pageInfo.filter(p => p.pageNum || p.page === firstPage).length;
   const bareAll = []; pageInfo.forEach(p => p.bare.forEach(b => bareAll.push(`p. ${p.page}: ${b}`)));
   checks.push({ name: 'Headers and footers', detail: `${headerOK} of ${pageInfo.length} pages opened with the symbol; ${pageNumOK} of ${pageInfo.length} footers carried the page number (page ${firstPage} expected to have none); bare numbers removed from footers: ${bareAll.length ? bareAll.join(', ') : 'none'}`, status: (headerOK === pageInfo.length && pageNumOK === pageInfo.length) ? 'pass' : 'fail', link: '#tab-4' });
   // 7 headings
   const lab = headings.filter(h => h.kind === 'labelled').length;
   const unlab = headings.filter(h => h.kind === 'unlabelled');
   checks.push({ name: 'Headings', detail: `${lab} labelled and ${unlab.length} unlabelled headings found; unlabelled: ${unlab.length ? unlab.map(h => `“${h.title}” (p. ${h.page})`).join('; ') : 'none'} — check these are headings, not a paragraph's last line`, status: 'pass', link: '#tab-2' });
   // 8 nothing lost
   const counts = { cover: 0, header: 0, heading: 0, paragraph: 0, footer: 0, blank: 0, suspect: 0, none: 0 };
   const unclassified = [];
   pageInfo.forEach(pi => pi.lines.forEach(l => {
     if (l.cls === 'suspect') { counts.suspect++; counts.paragraph++; }
     else if (l.cls) counts[l.cls] = (counts[l.cls] || 0) + 1;
     else { counts.none++; unclassified.push(`p. ${l.page} line ${l.lineNo}: “${l.text.trim().slice(0, 60)}”`); }
   }));
   ```
   
   Wait — I set l.suspect = true on paragraph lines but their cls stays 'paragraph'. For the raw viewer I want suspect lines colored differently. So in the viewer, check l.suspect → suspect color. For counts: paragraph includes suspect. Let me count: if l.suspect → counts.suspect++ and counts.paragraph++ (since suspect is a paragraph line). Hmm, then paragraph total includes suspect. The nothing-lost check: "Every non-empty line of every page is classified exactly once as cover, header, heading, paragraph or footer (a suspect line is a paragraph line with a flag), and the counts per kind sum to the total non-empty lines". So: nonEmpty = total lines - blank. sum(cover+header+heading+paragraph+footer) should equal nonEmpty. With suspect counted as paragraph, that works. Let me compute: counts per cls for non-blank, with suspect folded into paragraph. And separately report suspect count.
   
   ```js
   const nonEmpty = pageInfo.reduce((n, pi) => n + pi.lines.filter(l => l.text.trim() !== '').length, 0);
   const classified = counts.cover + counts.header + counts.heading + counts.paragraph + counts.footer;
   checks.push({ name: 'Nothing lost', detail: `${nonEmpty} non-empty lines: cover ${counts.cover}, header ${counts.header}, heading ${counts.heading}, paragraph ${counts.paragraph} (of which ${counts.suspect} suspect), footer ${counts.footer}; sum ${classified}${counts.none ? '; UNCLASSIFIED: ' + unclassified.join('; ') : ''}`, status: (classified === nonEmpty && counts.none === 0) ? 'pass' : 'fail', link: '#tab-4' });
   ```
   
   Wait, but blank lines have cls 'blank' — excluded from nonEmpty. But are all blank lines cls='blank'? Leading blanks before header: set. Footer blanks: set in loop. Body blanks: set in walk. But what about blank lines between fi+1 and end that... the walk covers all body lines (allLines includes blanks). Yes. And lines after `end` that are blank — set in footer loop. Lines before fi — set. OK, every line has cls. But wait: in the footer loop, when I `break` (non-matching line), lines after end are footer-classified only if they matched; the loop decrements end only for matched lines. Lines from end..lines.length are the footer ones — all got cls set when matched. But if the loop breaks at a non-matching line, that line is body (index end-1 < end). Hmm wait: loop condition `while (end > fi+1)`; inside, examine lines[end-1]; if matches, mark and end--; else break. So after the loop, lines[end..] are all marked footer/blank. Lines[fi] header. Lines[fi+1..end-1] body → pushed to allLines. But hold on — I push `for (let i = fi + 1; i < end; i++) allLines.push(lines[i])` — but if header wasn't found (fi points at first non-empty which isn't symbol), then lines[fi] is body! Let me handle: if header found, body starts at fi+1; else body starts at fi. Let me set `bodyStart = info.headerOK ? fi + 1 : fi`. And if header not found, lines[fi] gets cls in walk. OK.
   
   Edge: `while (end > fi + 1)` — should be `end > bodyStart`? If header found, bodyStart = fi+1; footer loop shouldn't go below bodyStart. Use `while (end > bodyStart)`. Hmm, if the page is all footer... edge case, fine.

   Also — the date-stamp regex: "consists only of 6-digit groups" — "051125 061125". My regex `/^(\d{6})(\s+\d{6})*$/`. But also a single 6-digit "051125"? matches. OK. But careful: a bare number of 6 digits would be eaten as date stamp — fine.

   Hmm, one more: what if a footer line is like "GE.25-15926 (E)" — starts with "GE." → matched. Good.

   Now — repairs ordering: "in document order". My repairs are pushed during page processing (headers/footers per page in page order) and during the walk (in line order). But page processing happens for all pages first, then the walk. So repairs aren't globally in document order (all header/footer repairs come before walk repairs). To fix: after parsing, sort repairs by (page, then a sequence number). I'll add a global seq counter incremented on each push, then sort by seq? No — seq order is push order, which is pages-then-walk. I want document order: page asc, and within page, line order. Let me tag each repair with page and lineNo (when applicable) and sort by page, lineNo (lineNo null → 0 for page-level). Header repair: lineNo = fi+1. Footer: lineNo = the line's lineNo. Walk repairs: lineNo = l.lineNo. Then sort by (page, lineNo). Good.

   Now rendering. Let me write render functions:

   - renderHeader(): kicker, title, meta line, what sentence, status.
   - renderRail(): document cards. Each card: button (click → selectDoc). Shows symbol, title (short), adopted, n pages, big numbers: paragraphs found (with "of X" and bar), pages flagged (red if >0, link to tab 03 — but it's inside a button... nested interactive elements are bad. Make the card a div with a click handler + a button for the card itself? Simpler: card is a <button> for selection; the "pages flagged" and "checks" links are separate small links below the card? Hmm, the plan: rail card contains the big numbers, "n pages flagged" (red when > 0, linking to tab 03), "n of m checks pass" linking to tab 04. Nested links inside a button are invalid. Solution: make the card a div with role="button" tabindex? Or: card = <article> with a select button (the symbol/title area) and the stat links as separate <a href="#..."> that switch tabs. Let me structure: 
   
   ```html
   <div class="doccard" data-key>
     <button class="docselect">symbol, title, adopted, n pages</button>
     <div class="docstats">
       <div class="bignum">90 <span>of 90 paragraphs</span><div class="bar">…</div></div>
       <div class="bignum flagged">20 <span>pages flagged</span> <a href="#" data-goto="3">see tab 03</a></div>
       <div class="checks"><a href="#" data-goto="4">8 of 8 checks pass</a></div>
     </div>
   </div>
   ```
   
   The links use buttons styled as links (to avoid href navigation) — I'll use <button class="linklike" data-goto="panel-3">. Clicking switches tab. Good, avoids nested-interactive issues.

   - renderTabs(): static tab buttons in HTML; panels rendered per current doc.
   - renderPanel1(): four tiles.
   - renderPanel2(): headings box + table.
   - renderPanel3(): note + table of flagged pages.
   - renderPanel4(): checks + repair log + raw pages + download.
   - renderFooter().

   Since panels re-render on doc switch, I'll have a single `render()` that fills all panels.

   Event delegation: after setting innerHTML, attach listeners. For paragraph rows: use event delegation on the panel (click on .prow or its button toggles detail row). For tab 03 rows similarly. For "Show the PDF's lines" toggle: delegation. Copy citation: delegation with navigator.clipboard? Clipboard API may fail in sandbox (permissions). Fallback: use a temporary textarea + document.execCommand('copy'). I'll try navigator.clipboard.writeText, catch → fallback execCommand. Show "Copied" for 2s.

   CSV download: as above.

   Raw pages viewer: select element with options "Show raw page n" for each record; on change, render lines. Default: first page. Lines rendered as divs: `<div class="rl cls-suspect"><span class="ln">12</span><span class="code">S</span><span class="lt">text</span></div>`. Blank lines: render with empty text (keep line number). Use textContent to avoid escaping issues — I'll build with createElement or use escHtml. I'll write a helper `el(html)` — simpler: build strings with escHtml for text content.

   escHtml: `s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')`.

   Legend: six items with color chip + letter + name.

   Now, tab 02 table columns: No. | Section | Page | First line | Check. First line: first 120 chars cut at a word + "…". Compute: take p.text, if length > 120: cut = p.text.slice(0, 120); cut at last space → + '…'. 

   Check cell: 
   - if p.firstWordsMatch === false → "first words differ" (red) — expanded row shows reference words.
   - if p.flagged → "may contain footnote text" (red, link to tab 03) — hmm, a paragraph could be both. Priority: show both? Cell can show "first words differ · may contain footnote text". I'll join with ' · '. If neither → "OK" (green? plan says Check cell reading "OK" — I'll make OK plain/green).
   - if firstWordsMatch === null (no reference) → "no reference" grey? I'll show "OK" only when match true; if null → "not checked". Keep simple: match===true → OK; false → differ; null → 'no reference'.

   Page cell: "3–4" if page_start !== page_end else "3".

   Expanded row content:
   - Full text (verbatim, one block): `<p class="fulltext">…</p>` with suspect lines highlighted? "the expanded paragraph on tab 02 highlights them" — yes, highlight suspect lines within the full text. Since text is joined, I can't easily highlight inline... I'll render the full text as the joined text but wrap suspect portions? Simpler: render the "PDF's lines" view by default? No — plan: "Under the row, the full text, verbatim as computed... The expanded paragraph is one block of running text; a 'Show the PDF's lines' toggle under it reveals the same text with the converter's line breaks". And "Suspect lines stay in the text... the expanded paragraph on tab 02 highlights them." Hmm — highlighting suspect lines in the running text: I can reconstruct: split text into segments by suspect lines? Since text = lines joined with ' ', I can render the running text as a sequence of spans: for each line, a span with its trimmed text + ' ', suspect spans get class. That gives running text with highlights. 
   
   So full text block: `<p class="fulltext">` + p.lines.map(l => `<span class="${l.suspect?'susp':''}">${esc(l.text.trim())}</span>`).join(' ') + `</p>`. That's verbatim (joined with single space, collapsed). Good.
   
   - Toggle "Show the PDF's lines": a button; when on, replace the fulltext block with a monospace block: each line: `[p. N]` marker when page changes (or on first line), then the line text; suspect lines highlighted. Include the startLine ("23.") as first line. 
   
   - Reference vs found first words: "reference: “…” · found: “…” — equal/different".
   - Pages: "pp. 3–4" or "p. 3".
   - Repairs touching this paragraph: list kinds (with page).
   - Copy citation button.

   Tab 02 headings box: "Headings found: n" button toggling a list: each heading: label + title + page. 

   Tab 01 tiles: 
   ```html
   <div class="tiles">
     <div class="tile"><div class="tnum">90</div><div class="tlab">paragraphs found</div><div class="tsub">The document has: 90</div><div class="how">How this is computed: …</div></div>
     ...
   </div>
   ```
   Tile 1: green when equal, red with difference: "90 found · document has 90" or "88 found · document has 90 (2 short)". 
   Tile 2: "20 of 20 pages flagged" + note. 
   Tile 3: "90 of 90 first words match". 
   Tile 4: "n repairs made" + link "see the repair log on tab 04".

   Tab 04 checks panel: each check a line: `<div class="check pass|fail|notrun"><span class="cname">Paragraph count</span> — detail — <span class="cstatus">pass</span></div>`. Fail status links to rows: I'll make the status a button/link that goes to the relevant tab. Simpler: the whole check line includes a "see rows" link when fail. Plan: "'check failed' in red with a link to the rows concerned". I'll add link in the detail when fail: e.g. first-words fail → link to tab 02. I'll add a small link at the end of failing checks: `<button class="linklike" data-goto="panel-2">see rows</button>`.

   Repair log: heading button "Repair log (n)" aria-expanded; when open, show counts per kind (chips or a line: "header line removed ×20 · footer line removed ×58 · …") then table: Page | Paragraph or footnote | What was done | Before | After. Before/After cells: monospace small, truncated? Full text could be long (footer lines short; heading joins medium). I'll show full but with `word-break` and max-height? Keep full, it's a log. Maybe truncate before/after to 200 chars with title attr. I'll show full text in a small cell; fine.

   Raw pages: heading button "Raw pages" aria-expanded; when open: select + panel + legend.

   Download: button "Download paragraphs as CSV" + a line explaining format ("UTF-8 with BOM, every field quoted, CRLF; one row per paragraph; citation column ready to paste").

   Footer: source line: `Source: {doc.source}` + built date if present + the honesty line. Also maybe "Data: WORKSHOP_DATA.pdf_text". The plan: "Source line, built date, and 'Counting, splitting, matching and flagging are done by this page's code; no model was called and nothing left the browser.'" I'll render: `Source: {source} · built {built}` (if present) and the sentence. Also name the dataset key.

   Now — the header meta line: "`symbol` linked to `doc_url` (new tab), 'adopted `reference.adopted`', 'n pages of raw converter text', `source`". So: `<a href=doc_url target=_blank rel=noopener>symbol</a> · adopted 6 November 2025 · 20 pages of raw converter text · {source}`. If doc_url empty, plain text.

   Now, one thing to double check: the plan says the app should work for "every document in WORKSHOP_DATA with records and a reference" — my discovery scans all keys. But `uhri` has records and no reference → excluded. `library` has records, no reference → excluded. Good. But wait — does `uhri` have a `reference`? No. OK.

   Also — the rail card needs a "short title". doc.title for pdf_text is probably "General comment No. 27 (2025)..." — I'll show title truncated via CSS (line-clamp) or slice. I'll show full title in the card but smaller; or slice to ~80 chars. I'll use CSS line-clamp: 2.

   Now, about `count` being string "20" — I use records.length. Fine.

   Let me also handle: reference.adopted might be missing → omit "adopted".

   Now — the tab labels: `01 RESULT · 02 PARAGRAPHS · 03 FLAGGED PAGES · 04 CHECKS & METHOD`. With the middle dot as separator in the label text? The plan writes tabs as `01 RESULT · 02 PARAGRAPHS · …` — the "·" separates tab names in the plan text, not part of labels. Labels: "01 RESULT", "02 PARAGRAPHS", "03 FLAGGED PAGES", "04 CHECKS & METHOD". I'll render with a separator via CSS (border or gap). I'll just have gap.

   Red dot on tab 04 when failures: `<span class="dot red"></span>` inside tab 04 label.

   Now let me also think: "No view shows more than about seven things to click" — tab 01: 4 tabs + repair link = 5. Tab 02: 4 tabs + headings toggle + rows (rows not counted). Tab 04: 4 tabs + repair log + raw pages + download + select = 8 — hmm, "the select appears once 'Raw pages' is open" and plan says "Seven things to click: four tabs, the repair log and raw pages headings, and the download (the select appears once 'Raw pages' is open)". So they count 7 without the select. OK fine.

   Filters rail: the left rail here is the DOCUMENT rail, not filters. The plan's rail spec: "Headed 'DOCUMENT'. A card for the document..." — no filter headings needed. Good, simpler.

   Now — writing the code. It's going to be long. Let me be careful and systematic. Target under 1500 lines. Let me draft.

   Also: "Every row that shows a document has its symbol, linked to doc_url in a new tab" — in this app, rows show paragraphs; the header shows symbol+link; CSV has symbol/doc_url columns; the rail card shows symbol (link? I'll link symbol in header; rail card symbol can also link). I'll link symbol in the header meta and in the rail card title area. Paragraph rows: maybe show symbol in expanded row? The citation includes symbol. I'll add symbol link in the expanded paragraph meta ("source: symbol ↗"). Good.

   Let me now also decide the "part" column: CSV has `part` — the roman part ("IV. Title"). p.part computed at creation. And `section` — nearest heading title. OK.

   One more detail: paragraph "Page" column shows "the page(s) it starts and ends on ('3–4' across a page break)". Good.

   Now, about performance: pdf_text 20 pages × ~3500 chars ≈ 70KB; pdf_text_2 similar. Parsing trivial. Rendering 90 rows fine. AHRC has 652 passages but that's library, not used here.

   Let me now write the whole HTML file.

   Structure of the script:

   ```js
   (function(){
     'use strict';
     const W = window.WORKSHOP_DATA || {};
     // discover docs
     const docs = [];
     Object.keys(W).forEach(k => {
       const v = W[k];
       if (v && !Array.isArray(v) && Array.isArray(v.records) && v.reference && typeof v.reference === 'object') {
         docs.push({ key: k, doc: v });
       }
     });
     // prefer pdf_text as default
     let currentKey = docs.length ? (docs.find(d => d.key === 'pdf_text') || docs[0]).key : null;
     let R = null; // current parse result
     
     ... helpers ...
     function parseDocument(doc) { ... returns R ... }
     function render() { ... }
     // tab wiring
     ...
     selectDoc(currentKey);
   })();
   ```

   Wait — if pdf_text is a bare array (sample shape), discovery fails. Add fallback: if no docs found, check W.pdf_text / W.pdf_text_2 as arrays and wrap with reference from... they wouldn't have reference. Hmm. The description clearly states the object shape with reference. I'll also add: if `W.pdf_text` is an array, wrap it as {records: W.pdf_text, reference: W.pdf_text_reference || null} — no, overengineering. Trust the description. But I'll make discovery tolerant: value could be object with records+reference. Done.

   Hmm, actually wait. Let me re-read the sample: `"pdf_text": [ { "page": 1, "text": "..." } ]` — the sample section says "Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)". So for pdf_text they show a sample of the records — as an array. This suggests WORKSHOP_DATA.pdf_text might literally be an array of records in the real environment too?? But the description says it's an object with title/symbol/records/reference. The description is the authoritative spec ("## `WORKSHOP_DATA.pdf_text`: one UN document as raw text from its PDF — `{title, symbol, doc_url, source, count, records: [{page, text}], reference: {...}}`"). The sample is just showing "records" samples. Hmm, but it shows the key "pdf_text" mapping to an array... 

   To be safe, handle both: 
   ```js
   function asDoc(v) {
     if (Array.isArray(v)) return { records: v, reference: null, title: '', symbol: '', doc_url: '', source: '' };
     if (v && typeof v === 'object' && Array.isArray(v.records)) return v;
     return null;
   }
   ```
   And discovery: keys where asDoc(v) && (v.reference || Array.isArray(v))... hmm, if pdf_text is a bare array, it has no reference — but the plan says the app checks against reference. If it's a bare array, there's no reference anywhere. I'll include bare arrays as docs with reference null (checks show "not run", tiles "no reference in this file"). That's graceful. But then symbol is unknown — citation needs symbol... fallback: symbol = '' → citation "para. 12"? Ugly. Alternatively, if bare array, try W.pdf_text_symbol? No. 

   I'll do: discovery includes objects with records (reference optional). For bare arrays, wrap with defaults and try to find symbol/title from... nothing. Given the description explicitly gives the object shape, the real data is the object. The array handling is just defensive; symbol fallback: use doc.symbol || 'document'. Fine.

   Actually, you know, let me look again at the description of pdf_text: "`{title, symbol, doc_url, source, count, records: [{page, text}], reference: {...}}`. `records` are the 20 pages of E/C.12/GC/27 exactly as a PDF converter produced them." — clear. The sample just abbreviated. Go with object shape, defensive array wrap.

   Now, let me write the CSS. Key classes:

   ```css
   :root {
     --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --red:#9b2335; --green:#1e6b3a;
     --serif: Georgia, 'Times New Roman', serif;
     --mono: ui-monospace, Menlo, Consolas, monospace;
     --sans: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
   }
   * { box-sizing: border-box; }
   body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--sans); font-size:16px; line-height:1.5; }
   [hidden]{display:none!important}
   a { color:var(--red); }
   :focus-visible { outline:3px solid var(--red); outline-offset:2px; }
   ```

   Header:
   ```css
   header.top { padding: 20px 28px 14px; border-bottom:1px solid var(--rule); }
   .kicker { font-family:var(--mono); font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--red); }
   h1 { font-family:var(--serif); font-weight:normal; font-size:30px; margin:6px 0 4px; max-width: 60ch; }
   .meta { font-size:14px; color:#4a463f; }
   .what { max-width: 75ch; margin:8px 0 0; }
   .status { position:absolute? } 
   ```
   Status at right: I'll put header as flex: left block + right status. 
   ```css
   header.top { display:flex; justify-content:space-between; gap:24px; align-items:flex-start; }
   .status { font-family:var(--mono); font-size:12px; white-space:nowrap; padding-top:6px; }
   .dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
   .dot.g { background:var(--green); } .dot.r { background:var(--red); }
   ```

   Layout:
   ```css
   .layout { display:flex; align-items:flex-start; }
   aside.rail { width:280px; flex:0 0 280px; padding:18px 20px; border-right:1px solid var(--rule); position:sticky; top:0; max-height:100vh; overflow:auto; }
   main { flex:1; min-width:0; padding:18px 28px 40px; }
   @media (max-width: 900px) { .layout{flex-direction:column} aside.rail{width:auto;flex:none;border-right:none;border-bottom:1px solid var(--rule);position:static;max-height:none} }
   ```

   Rail:
   ```css
   .rail h2 { font-family:var(--mono); font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:#6b655a; margin:0 0 10px; }
   .doccard { border-left:3px solid transparent; padding:10px 12px; margin-bottom:14px; border-bottom:1px solid var(--rule); }
   .doccard.sel { border-left-color:var(--red); background:#efe9dd; }
   .docselect { all:unset-ish; display:block; width:100%; text-align:left; cursor:pointer; }
   ```
   Buttons: I'll style `.btn` base. For docselect, use a real <button> with reset styles:
   ```css
   button { font:inherit; color:inherit; background:none; border:none; padding:0; cursor:pointer; }
   ```
   Then specific styles. Careful: table row buttons etc.

   Big numbers in rail:
   ```css
   .bignum { font-family:var(--serif); font-size:44px; line-height:1.05; }
   .bignum .of { font-family:var(--mono); font-size:11px; color:#6b655a; letter-spacing:.08em; display:block; margin-top:2px; }
   .bar { height:4px; background:var(--rule); margin-top:6px; position:relative; }
   .bar i { position:absolute; left:0; top:0; bottom:0; background:var(--green); }
   .bar i.bad { background:var(--red); }
   ```

   Tabs:
   ```css
   .tablist { display:flex; gap:4px; border-bottom:1px solid var(--rule); flex-wrap:wrap; }
   .tablist [role=tab] { font-family:var(--mono); font-size:12px; letter-spacing:.1em; padding:10px 14px; border-bottom:3px solid transparent; color:#5c564c; }
   .tablist [role=tab][aria-selected=true] { color:var(--red); border-bottom-color:var(--red); }
   ```

   Tiles:
   ```css
   .tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:0; border-top:1px solid var(--rule); }
   .tile { padding:18px 20px 18px 0; border-bottom:1px solid var(--rule); margin-right:20px; }
   .tnum { font-family:var(--serif); font-size:52px; line-height:1; }
   .tnum.bad { color:var(--red); } .tnum.good { color:var(--green); }
   .tlab { font-family:var(--mono); font-size:11px; letter-spacing:.12em; text-transform:uppercase; margin-top:6px; }
   .tsub { font-size:14px; margin-top:4px; }
   .how { font-family:var(--mono); font-size:11px; color:#6b655a; margin-top:8px; line-height:1.5; }
   ```

   Tables:
   ```css
   table { border-collapse:collapse; width:100%; margin:10px 0 6px; }
   caption { text-align:left; font-family:var(--serif); font-size:19px; padding:8px 0 4px; caption-side:top; }
   caption .tabno { font-family:var(--mono); font-size:11px; color:var(--red); letter-spacing:.12em; margin-right:8px; }
   th { font-family:var(--mono); font-size:11px; letter-spacing:.1em; text-transform:uppercase; font-weight:normal; color:#6b655a; text-align:left; padding:6px 10px 6px 0; border-bottom:1px solid var(--ink); }
   td { padding:8px 10px 8px 0; border-bottom:1px solid var(--rule); vertical-align:top; font-size:15px; }
   td.num, th.num { text-align:right; }
   tr.prow { cursor:pointer; }
   tr.prow:hover td { background:#ece6d8; }
   td.pnum { font-family:var(--serif); font-size:18px; color:var(--red); white-space:nowrap; }
   .check-ok { color:var(--green); font-family:var(--mono); font-size:11px; letter-spacing:.06em; }
   .check-bad { color:var(--red); font-family:var(--mono); font-size:11px; letter-spacing:.06em; }
   ```

   Detail rows: `tr.detail td { background:#efe9dd; }` with inner content.

   Raw lines viewer:
   ```css
   .rawline { display:flex; font-family:var(--mono); font-size:12px; line-height:1.45; white-space:pre-wrap; word-break:break-word; }
   .rawline .ln { flex:0 0 44px; text-align:right; color:#8a8375; padding-right:8px; user-select:none; }
   .rawline .code { flex:0 0 18px; }
   .rawline .lt { flex:1; }
   .cls-cover { background:#e9e4f2; } .code-c { color:#5b4a86; }
   ...
   ```
   Hmm, letter codes: cover=C, header=H, heading=T? Let me use: cover "C", header "H", heading "G"? Hmm — heading... "T" for title? I'll use: cover=C, header=H, heading=D? no. Let me pick intuitive: cover=C, header=H, heading=T (title), paragraph=P, suspect=S, footer=F. Colors:
   - cover: #e6e1f0 (pale violet), code color #5b4a86
   - header: #dde6ee (pale blue), code #33587a
   - heading: #f2e7cf (pale amber), code #8a6a1f
   - paragraph: #e4ecdf (pale green), code #3f6b34
   - suspect: #f5dcdc (pale red), code #9b2335
   - footer: #e7e3da (pale grey), code #6b655a
   - blank: no background
   Contrast: ink #1d1b18 on these pale tints — fine.

   Legend: chips with the same colors.

   Now the JS render. Let me write it all out now, carefully. I'll write the final file mentally section by section.

   Also the "How this is computed" line near every chart or number — tiles have .how; rail big numbers get small mono hints; tab 02 caption states message; tab 03 note; tab 04 checks are self-explanatory.

   Let me now also decide details for tab 03 expansion: clicking a flagged-page row expands to show: the page's raw lines (with suspect highlighted) and "the paragraph they sit in" — list paragraph numbers containing suspects on that page + over-300 paragraphs touching it. I'll render the raw lines block (reuse renderer) plus a line "Suspect lines sit in para. X, Y".

   Now, code for rendering raw lines of a page:

   ```js
   function rawLinesHtml(page) {
     const pi = R.pageInfo.find(p => p.page === page);
     if (!pi) return '';
     let out = '';
     let lastPage = null;
     pi.lines.forEach(l => {
       const t = l.text;
       const cls = l.suspect ? 'suspect' : (l.cls || 'blank');
       const code = {cover:'C',header:'H',heading:'T',paragraph:'P',suspect:'S',footer:'F',blank:''}[cls] || '?';
       const bg = cls === 'blank' ? '' : ` style="background:${CLS_BG[cls]}"`;
       out += `<div class="rawline"${bg}><span class="ln">${l.lineNo}</span><span class="code" style="color:${CLS_FG[cls]||'#8a8375'}">${code}</span><span class="lt">${escHtml(t)}</span></div>`;
     });
     return out;
   }
   ```
   Hmm, inline styles vs classes — classes cleaner. I'll define classes .c-cover etc. in CSS and map.

   For the "Show the PDF's lines" in tab 02: lines of the paragraph with page markers:
   ```js
   function paraLinesHtml(p) {
     const rows = [];
     if (p.startLine) rows.push(p.startLine);
     p.lines.forEach(l => rows.push(l));
     let out = '', lastPage = null;
     rows.forEach(l => {
       const marker = (l.page !== lastPage) ? `<span class="pg">[p. ${l.page}]</span> ` : '';
       lastPage = l.page;
       out += `<div class="rawline ${l.suspect ? 'c-suspect' : 'c-paragraph'}"><span class="ln">${l.lineNo}</span><span class="code">…</span><span class="lt">${marker}${escHtml(l.text)}</span></div>`;
     });
     return out;
   }
   ```
   Hmm, the code letter for paragraph lines: 'P', suspect 'S'. And the startLine: cls 'paragraph' → 'P'.

   Wait — p.startLine for the split case has text "23. Some text..." — showing it raw is right ("the same text with the converter's line breaks").

   Now the full text block with highlights:
   ```js
   function fullTextHtml(p) {
     return p.lines.map(l => `<span class="${l.suspect ? 'hl-suspect' : ''}">${escHtml(l.text.trim())}</span>`).join(' ');
   }
   ```
   .hl-suspect { background:#f5dcdc; } maybe with underline. OK.

   Now, event delegation. After render, attach one listener on document for clicks:
   ```js
   document.addEventListener('click', e => {
     const t = e.target.closest('[data-action]');
     if (!t) return;
     const action = t.dataset.action;
     if (action === 'tab') { activateTab(t.dataset.tab); }
     else if (action === 'toggle-row') { const tr = document.getElementById(t.dataset.target); const open = tr.hidden; tr.hidden = !open; t.setAttribute('aria-expanded', String(open)); }
     ...
   });
   ```
   Using data-action attributes simplifies delegation. Actions: tab, toggle (generic: data-target id), goto (tab + maybe open something), copy (data-citation), rawpage (select change — use 'change' listener), download, docselect (data-key), showlines (toggle within a detail), headings toggle.

   Let me define:
   - data-action="tab" data-tab="panel-1" — tab buttons and goto links.
   - data-action="toggle" data-target="id" — generic expand/collapse of element with id; also flips aria-expanded on the button.
   - data-action="copy" data-citation="..." — copy citation.
   - data-action="doc" data-key="pdf_text" — select document card.
   - data-action="goto-repairs" — activate tab 4 and open repair log.
   - data-action="download" — CSV.
   - Raw page select: id="rawselect", change listener.
   - "Show the PDF's lines" toggle: data-action="toggle" data-target="lines-N" plus swap button text? I'll have the button toggle hidden on the lines block and toggle the fulltext block hidden. Simpler: two blocks, button toggles both: data-action="showlines" data-target="N": hides #full-N, shows #lines-N, sets button text "Hide the PDF's lines"; clicking again reverses. I'll implement in the handler.

   Paragraph row click: the row itself clickable — I'll put data-action="toggle" data-target="detail-N" on the button in the No. cell, AND a click handler on the row: in delegation, also check `e.target.closest('tr.prow')` → find its button and trigger. Let me do: in the click listener, first check closest('[data-action]'); if none, check closest('tr[data-row]') → toggle its detail. I'll give each prow a data-row="detail-N" and handle: if closest tr.prow, toggle the detail row and the button's aria-expanded.

   Simpler: put the data-action="toggle" on the <tr> itself? tr isn't focusable but click works; keyboard via the inner button. I'll do both: button has data-action="toggle" data-target; row has data-rowtarget="detail-N". In handler: `const row = e.target.closest('tr[data-rowtarget]'); if (row && !e.target.closest('[data-action]')) { toggle(row.dataset.rowtarget, row.querySelector('button')); }`. Hmm, getting complex. Cleanest: handle in one place:

   ```js
   document.addEventListener('click', e => {
     const act = e.target.closest('[data-action]');
     if (act) { handleAction(act, e); return; }
     const row = e.target.closest('tr[data-detail]');
     if (row) { toggleDetail(row.dataset.detail, row); }
   });
   function toggleDetail(id, row) {
     const d = document.getElementById(id);
     if (!d) return;
     const open = d.hidden;
     d.hidden = !open;
     const btn = row ? row.querySelector('[aria-expanded]') : null;
     if (btn) btn.setAttribute('aria-expanded', String(open));
   }
   ```
   And the button inside the row also has data-action="toggle" data-target=id — but then clicking the button would hit the act branch first (closest finds the button) → handleAction toggles by id and updates aria-expanded on the button itself. And clicking elsewhere in the row hits the row branch. Both call the same core. Let me make handleAction('toggle') call toggleDetail(target, null) but also set aria-expanded on the action element itself. Fine — I'll write toggleDetail(id, btnEl) where btnEl optional.

   Keyboard: button handles Enter/Space natively (click). Good.

   Tabs: 
   ```js
   function activateTab(id) {
     document.querySelectorAll('[role=tab]').forEach(t => {
       const sel = t.getAttribute('aria-controls') === id;
       t.setAttribute('aria-selected', String(sel));
       t.tabIndex = sel ? 0 : -1;
     });
     document.querySelectorAll('[role=tabpanel]').forEach(p => { p.hidden = p.id !== id; });
   }
   ```
   Arrow keys on tablist keydown.

   Now, the repair-log tile link: data-action="goto" data-tab="panel-4" data-open="repairlog". Handler: activateTab('panel-4'); then open the repair log (set hidden false, aria-expanded true) and scroll into view.

   Rail links: data-action="tab" data-tab="panel-3" etc.

   Now let me write parseDocument fully, then render.

   One more thing — the plan says tab 02's table has a collapsible "Headings found: n" box ABOVE the table. I'll render: `<button class="coll" data-action="toggle" data-target="headingsbox" aria-expanded="false">Headings found: 25</button><div id="headingsbox" hidden>…list…</div>`.

   And tab 04: check panel open; "Repair log (n)" closed heading (button aria-expanded=false, table hidden); "Raw pages" closed heading; Download section open (always visible? plan lists Download after raw pages; I'll keep the download button always visible at the end).

   Now — CSV `part` column: p.part. `section`: p.section. `repairs`: kinds joined '; '. `suspect_lines`: "p.3 L12 “7 E/…”" joined '; '. `flagged`: yes/no. `first_words_match`: yes/no/blank.

   Let me now also compute the rail bar: share = found / reference.paragraphs; bar width = min(share,1)*100%; red when share !== 1 (short or over). If no reference → grey bar full? I'll show bar only if reference.

   Header status: compute from R.checks: pass = checks.filter(c=>c.status==='pass').length; fail = ...; notrun = ...; total = checks.length. If fail>0: red dot + `${fail} check${s} failed` (plus maybe `${pass} of ${total} pass`). Plan: red dot and "n checks failed". I'll show: red dot + `${fail} of ${total} checks failed`. Green: `${pass} of ${total} checks pass`. If notrun>0 append ` · ${notrun} not run`. Tab 04 gets red dot when fail>0.

   Now — writing everything. Also remember: no external resources; Chart.js not needed (no charts required — bars are CSS). The plan mentions thin bar in rail — CSS. OK, no Chart.js needed. That's fine ("Use it for charts" — only if charts; we have none, just CSS bars).

   Wait — should tab 01 have a chart? Plan says four tiles with big numbers. No chart needed. OK.

   Let me also add the "How this is computed" near the rail numbers: small mono hints.

   Let me now write out the complete code. I'll aim for clarity and correctness. Let me carefully write parseDocument:

   ```js
   function parseDocument(doc) {
     const symbol = doc.symbol || '';
     const records = (doc.records || []).slice().sort((a, b) => (a.page - b.page));
     const ref = (doc.reference && typeof doc.reference === 'object') ? doc.reference : null;
     const repairs = [];
     const warnings = [];
     const allLines = [];
     const pageInfo = [];
     let seq = 0;
     const pushRepair = (page, lineNo, para, kind, before, after) => {
       repairs.push({ seq: seq++, page, lineNo: lineNo == null ? 0 : lineNo, para, kind, before, after });
     };

     records.forEach(rec => {
       const page = rec.page;
       const raw = String(rec.text == null ? '' : rec.text).split(/\r?\n/);
       const lines = raw.map((t, i) => ({ text: t, page, lineNo: i + 1, cls: null, suspect: false }));
       const info = { page, lines, headerOK: false, pageNum: false, bare: [] };
       let fi = 0;
       while (fi < lines.length && lines[fi].text.trim() === '') { lines[fi].cls = 'blank'; fi++; }
       let bodyStart = fi;
       if (fi < lines.length && symbol !== '' && lines[fi].text.trim() === symbol) {
         lines[fi].cls = 'header';
         info.headerOK = true;
         pushRepair(page, fi + 1, null, 'header line removed', lines[fi].text.trim(), '');
         bodyStart = fi + 1;
       } else if (fi < lines.length) {
         warnings.push('p. ' + page + ': first non-empty line is not the symbol');
       }
       let end = lines.length;
       while (end > bodyStart) {
         const l = lines[end - 1];
         const t = l.text.trim();
         if (t === '') { l.cls = 'blank'; end--; continue; }
         if (/^GE\./.test(t)) { l.cls = 'footer'; pushRepair(page, l.lineNo, null, 'footer line removed', t, ''); end--; continue; }
         if (/^(?:\d{6})(?:\s+\d{6})*$/.test(t)) { l.cls = 'footer'; pushRepair(page, l.lineNo, null, 'footer line removed', t, ''); end--; continue; }
         if (/^\d{1,3}$/.test(t)) {
           l.cls = 'footer';
           const n = parseInt(t, 10);
           if (n === page) { info.pageNum = true; pushRepair(page, l.lineNo, null, 'footer line removed', t, ''); }
           else { info.bare.push(n); pushRepair(page, l.lineNo, null, 'bare number removed from the footer', t, ''); }
           end--; continue;
         }
         break;
       }
       for (let i = bodyStart; i < end; i++) allLines.push(lines[i]);
       pageInfo.push(info);
     });
     ```

     Wait — bug: if header not found, bodyStart = fi, and lines[fi] is body — but the footer loop condition `end > bodyStart` could eat down to bodyStart... fine. But also if header found, lines before fi are blank (set). OK. Also: lines between bodyStart and end that are blank — they're in allLines, walk sets cls='blank'. Good.

     Hmm, one more: what if the whole page is empty or fi === lines.length (all blank)? Then bodyStart = fi = lines.length, end = lines.length, loop doesn't run, no body lines. info.headerOK false → warning. Edge OK.

     Continue with the walk (as drafted above). Then post-processing. Let me also record for each paragraph its startLine and inline:

     In the walk, when ps found:
     ```js
     cur = { number: ps.num, startLine: l, inline: ps.inline, lines: [], pages: [l.page], pageSet: new Set([l.page]), section: sectionTitle, path: sectionFull, part: partLabel ? (partLabel + (partTitle ? ' ' + partTitle : '')) : '' };
     if (ps.inline != null) {
       const il = { text: ps.inline, page: l.page, lineNo: l.lineNo, cls: 'paragraph', suspect: false };
       cur.lines.push(il);
       pushRepair(l.page, l.lineNo, ps.num, 'number and text split', l.text.trim(), ps.num + '. ' + ps.inline);
     }
     ```

     Post:
     ```js
     paragraphs.forEach(p => {
       if (p.pageSet.size > 1) {
         pushRepair(p.pages[p.pages.length - 1], null, p.number, 'paragraph joined across a page break',
           'text continues from p. ' + p.pages[0] + ' to p. ' + p.pages[p.pages.length - 1],
           'joined into para. ' + p.number + ' (pp. ' + p.pages.join('–') + ')');
       }
       p.page_start = p.pages[0];
       p.page_end = p.pages[p.pages.length - 1];
       p.textRaw = [p.startLine].concat(p.lines).map(l => l.text).join('\n');
       p.text = p.lines.map(l => l.text.trim()).join(' ').replace(/\s+/g, ' ').trim();
       p.textLines = p.lines.map(l => l.text.trim()).join(' | ');
       // suspect
       p.suspect = [];
       let trigPage = null;
       p.lines.forEach(l => {
         const t = l.text.trim();
         const self = /^\d{1,3}$/.test(t) || /^\d{1,3}\s+[A-Z“"'’]/.test(t);
         if (self) { trigPage = l.page; l.suspect = true; p.suspect.push({ page: l.page, lineNo: l.lineNo, text: t, why: /^\d{1,3}$/.test(t) ? 'bare number' : 'starts with a number and a space' }); }
         else if (trigPage !== null && l.page === trigPage) { l.suspect = true; p.suspect.push({ page: l.page, lineNo: l.lineNo, text: t, why: 'after a suspect line on the same page' }); }
       });
       p.words = p.text === '' ? 0 : p.text.split(/\s+/).length;
       p.overWords = p.words > 300;
       p.flagged = p.suspect.length > 0 || p.overWords;
       // first words
       const toks = p.text.split(/\s+/).map(t => t.replace(/\d+$/, '')).filter(t => t !== '');
       p.firstWordsFound = toks.slice(0, 6).join(' ');
       const refFW = ref && ref.first_words ? ref.first_words[String(p.number)] : null;
       p.firstWordsRef = (refFW == null) ? null : String(refFW);
       p.firstWordsMatch = (p.firstWordsRef == null) ? null : (norm(p.firstWordsFound) === norm(p.firstWordsRef));
       p.citation = (symbol ? symbol + ', ' : '') + 'para. ' + p.number;
     });
     repairs.sort((a, b) => (a.page - b.page) || (a.lineNo - b.lineNo) || (a.seq - b.seq));
     paragraphs.forEach(p => { p.repairList = repairs.filter(r => r.para === p.number); });
     ```

     Hmm — the suspect regex: `/^\d{1,3}\s+[A-Z“"'’]/` — plan says "a capital letter, a UN document symbol or a quotation mark". Quotation marks: curly “ ” and straight ". I'll include `["“”‘’]`. Also a UN doc symbol starts with a capital — covered. OK: `/^\d{1,3}\s+[A-Z"“”‘’]/`.

     Wait, also: should the suspect check apply to the inline line (split case)? The inline is part of the parastart line "23. text" — has a full stop after number, so not suspect. Skip (I only iterate p.lines which includes the inline object — its text is the inline part, e.g. "Some text..." — could it start with digits? "23. 17 Sustainable..." → inline "17 Sustainable..." would match suspect pattern! Hmm. Edge case; the plan says "A line inside a paragraph is suspect when..." — the inline is part of the number line. I'll exclude the inline line from suspect scanning: mark il.inline = true and skip. Actually simpler: scan only lines after the first if the first is inline. I'll set a flag on the inline object: `il.fromStart = true`, and in the suspect loop skip lines with fromStart. Fine.

     flaggedPages:
     ```js
     const flaggedPages = new Map();
     paragraphs.forEach(p => {
       p.suspect.forEach(s => {
         if (!flaggedPages.has(s.page)) flaggedPages.set(s.page, { page: s.page, paras: new Set(), suspects: [], over: [] });
         const fp = flaggedPages.get(s.page);
         fp.paras.add(p.number); fp.suspects.push({ ...s, para: p.number });
       });
       if (p.overWords) p.pages.forEach(pg => {
         if (!flaggedPages.has(pg)) flaggedPages.set(pg, { page: pg, paras: new Set(), suspects: [], over: [] });
         flaggedPages.get(pg).paras.add(p.number); flaggedPages.get(pg).over.push(p.number);
       });
     });
     ```

     checks (as drafted). Also compute hyphenLines count: "No line in the file ends with a hyphen... the app counts such lines anyway and reports the number." Add to checks or method note: count lines ending with '-' → report in method/checks. I'll add it to the "Nothing lost" or as a note in tab 04 method line: "lines ending in a hyphen: n (none joined)". I'll add a small method paragraph on tab 04.

     Also warnings (header not symbol) — show in checks (headers/footers check detail includes warnings).

     Now render functions. Let me write them.

     ```js
     function render() {
       const doc = current.doc, R = current.result;
       // header
       document.getElementById('docTitle').textContent = doc.title || '(untitled document)';
       const meta = [];
       if (doc.symbol) {
         meta.push(doc.doc_url ? `<a href="${escAttr(doc.doc_url)}" target="_blank" rel="noopener">${escHtml(doc.symbol)}</a>` : escHtml(doc.symbol));
       }
       if (R.ref && R.ref.adopted != null) meta.push('adopted ' + escHtml(String(R.ref.adopted)));
       meta.push(R.records.length + ' pages of raw converter text');
       if (doc.source) meta.push(escHtml(String(doc.source)));
       document.getElementById('docMeta').innerHTML = meta.join(' · ');
       // status
       ...
       renderRail(); renderPanel1(); renderPanel2(); renderPanel3(); renderPanel4(); renderFooter();
     }
     ```

     I'll store current = { key, doc, result } where result includes everything (paragraphs, headings, repairs, checks, pageInfo, flaggedPages, ref, records, symbol...).

     Let me now write the panels.

     Panel 1:
     ```js
     function renderPanel1() {
       const R = current.result;
       const refParas = R.ref && R.ref.paragraphs != null ? R.ref.paragraphs : null;
       const found = R.paragraphs.length;
       const flaggedN = R.flaggedPages.size;
       const fwMatch = R.paragraphs.filter(p => p.firstWordsMatch === true).length;
       const fwTotal = R.ref && R.ref.first_words ? R.paragraphs.filter(p => p.firstWordsRef != null).length : null;
       const repairsN = R.repairs.length;
       const paraOK = refParas != null && found === refParas;
       ...
       html = `
       <div class="tiles">
         <div class="tile">
           <div class="tnum ${refParas==null?'':(paraOK?'good':'bad')}">${found}</div>
           <div class="tlab">paragraphs found</div>
           <div class="tsub">${refParas==null ? 'no reference in this file' : 'The document has: ' + refParas + (paraOK ? ' — equal' : ' — difference: ' + (found - refParas))}</div>
           <div class="how">How this is computed: lines matching “N.” or “N. text” start a paragraph; header and footer lines are removed first; the count is a loop over the result, compared with reference.paragraphs.</div>
         </div>
         <div class="tile">
           <div class="tnum ${flaggedN>0?'bad':''}">${flaggedN}<span class="of"> of ${R.records.length} pages</span></div>
           ...
       `;
     }
     ```
     Hmm, the big number with "of X" — plan: "Pages flagged: n of the document's pages". I'll put "n" big and "of 20 pages" as sub. Tile 1: "n" big, "The document has: 90" sub. OK.

     Tile 2 sub: when flaggedN>0: "footnote text may sit inside a paragraph; see tab 03" (link). Plus "The document has X footnotes; this version does not separate them" (if ref.footnotes != null).
     Tile 3: big "n of m" — hmm big number should be the match count; sub "of reference.paragraphs". If no first_words: "no reference in this file".
     Tile 4: big repairsN, sub link "see the repair log on tab 04" (button data-action="goto" data-tab="panel-4" data-open="repairlog").

     Panel 2:
     ```js
     const rows = R.paragraphs.map(p => {
       const pages = p.page_start === p.page_end ? String(p.page_start) : p.page_start + '–' + p.page_end;
       const first = p.text.length > 120 ? p.text.slice(0, 120).replace(/\s+\S*$/, '') + '…' : p.text;
       let check;
       if (p.firstWordsMatch === false && p.flagged) check = '<span class="check-bad">first words differ · may contain footnote text</span>';
       else if (p.firstWordsMatch === false) check = '<span class="check-bad">first words differ</span>';
       else if (p.flagged) check = '<span class="check-bad">may contain footnote text</span>';
       else if (p.firstWordsMatch === null) check = '<span class="check-dim">not checked</span>';
       else check = '<span class="check-ok">OK</span>';
       return `<tr class="prow" data-detail="detail-${p.number}">
         <td class="num pnum"><button data-action="toggle" data-target="detail-${p.number}" aria-expanded="false" aria-controls="detail-${p.number}">${p.number}</button></td>
         <td class="sec">${escHtml(p.section || '—')}</td>
         <td class="num">${pages}</td>
         <td class="first">${escHtml(first)}</td>
         <td>${check}</td>
       </tr>
       <tr class="detail" id="detail-${p.number}" hidden><td colspan="5">${detailHtml(p)}</td></tr>`;
     });
     ```
     
     detailHtml(p):
     ```js
     function detailHtml(p) {
       const R = current.result;
       const fw = p.firstWordsMatch === null
         ? '<span class="dim">no first_words in the reference for this paragraph</span>'
         : `reference: “${escHtml(p.firstWordsRef)}” · found: “${escHtml(p.firstWordsFound)}” — <span class="${p.firstWordsMatch?'check-ok':'check-bad'}">${p.firstWordsMatch?'equal':'different'}</span>`;
       const repairs = p.repairList.length ? p.repairList.map(r => `${escHtml(r.kind)} (p. ${r.page})`).join('; ') : 'none';
       const suspects = p.suspect.length ? p.suspect.map(s => `p. ${s.page} line ${s.lineNo}: “${escHtml(s.text.slice(0,80))}”`).join('; ') : 'none';
       return `
       <div class="detail-inner">
         <p class="fulltext" id="full-${p.number}">${fullTextHtml(p)}</p>
         <div class="lines" id="lines-${p.number}" hidden>${paraLinesHtml(p)}</div>
         <p class="rowbtns">
           <button class="btn" data-action="showlines" data-target="${p.number}">Show the PDF's lines</button>
           <button class="btn" data-action="copy" data-citation="${escAttr(p.citation)}">Copy citation</button>
           <span class="copied" id="copied-${p.number}" hidden>Copied</span>
         </p>
         <dl class="facts">
           <div><dt>First six words</dt><dd>${fw}</dd></div>
           <div><dt>Pages</dt><dd>${p.page_start === p.page_end ? 'p. ' + p.page_start : 'pp. ' + p.page_start + '–' + p.page_end}</dd></div>
           <div><dt>Section path</dt><dd>${escHtml(p.path || '—')}</dd></div>
           <div><dt>Suspect lines</dt><dd>${suspects}</dd></div>
           <div><dt>Repairs touching this paragraph</dt><dd>${repairs}</dd></div>
           <div><dt>Source</dt><dd>${R.doc.doc_url ? `<a href="${escAttr(R.doc.doc_url)}" target="_blank" rel="noopener">${escHtml(R.symbol)}</a>` : escHtml(R.symbol)} — cite as “${escHtml(p.citation)}”</dd></div>
         </dl>
       </div>`;
     }
     ```
     
     Hmm — "the reference's first six words next to the extracted first six words, marked equal or different" ✓. "the page(s)" ✓. "the repairs that touched this paragraph" ✓. "Copy citation button" ✓.

     Headings box above table:
     ```js
     const hbox = `<button class="coll" data-action="toggle" data-target="headingsbox" aria-expanded="false" aria-controls="headingsbox">Headings found: ${R.headings.length}</button>
     <div id="headingsbox" hidden><ul class="hlist">${R.headings.map(h => `<li>${h.kind==='labelled' ? escHtml(h.label + '.') : ''} ${escHtml(h.title)} <span class="dim">(p. ${h.page})</span></li>`).join('')}</ul></div>`;
     ```

     Table:
     ```html
     <table>
       <caption><span class="tabno">TAB.01</span>${R.paragraphs.length} paragraphs found${refParas!=null ? ', ' + refParas + ' expected' : ''} — click a row for the full text</caption>
       <thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>
       <tbody>…rows…</tbody>
     </table>
     <p class="src">Source: ${symbol link} · n = ${R.paragraphs.length} paragraphs computed from ${R.records.length} pages of raw converter text.</p>
     ```

     Panel 3:
     ```js
     if (R.flaggedPages.size === 0) → `<p>No page is flagged: no suspect line was found inside any paragraph.</p>`
     else note + table rows:
     flaggedPages sorted by page:
     `<tr class="prow" data-detail="fpage-${fp.page}">
        <td class="num pnum">${fp.page}</td>
        <td>${[...fp.paras].sort((a,b)=>a-b).map(n=>'para. '+n).join(', ')}</td>
        <td class="num">${fp.suspects.length}</td>
        <td>${whys}</td>
      </tr>
      <tr class="detail" id="fpage-${fp.page}" hidden><td colspan="4">
        <p class="dim">Raw lines of page ${fp.page}; suspect lines highlighted (S). The suspect lines sit in ${paras}.</p>
        <div class="rawbox">${rawLinesHtml(fp.page)}</div>
      </td></tr>`
     ```
     whys: distinct why values of suspects + 'paragraph over 300 words' if over.length.

     Note above table: "This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them."

     Panel 4:
     - checks panel: `<div class="checks">${R.checks.map(c => checkHtml(c)).join('')}</div>`
     ```js
     function checkHtml(c) {
       const cls = c.status === 'pass' ? 'pass' : c.status === 'fail' ? 'fail' : 'notrun';
       const label = c.status === 'pass' ? 'pass' : c.status === 'fail' ? 'check failed' : 'not run';
       return `<div class="check ${cls}"><span class="cname">${escHtml(c.name)}</span><span class="cdetail">${c.detail}</span><span class="cstatus">${label}</span>${c.link && c.status==='fail' ? ` <button class="linklike" data-action="tab" data-tab="${c.link}">see rows</button>` : ''}</div>`;
     }
     ```
     detail contains HTML (I'll build with escHtml inside). Careful to escape user data in details.
     
     - method paragraph: "Method: …" including hyphen-line count, pipeline order summary.
     - repair log: `<button class="coll" data-action="toggle" data-target="repairlog" aria-expanded="false">Repair log (${R.repairs.length})</button>` + counts per kind + table when open. But the table should exist in DOM (hidden) so the tile link can open it: `<div id="repairlog" hidden>…counts…<table>…</table></div>`. The tile's goto action: activate tab 4, then unhide #repairlog and set the button aria-expanded=true.
     - raw pages: `<button class="coll" data-action="toggle" data-target="rawpages" aria-expanded="false">Raw pages</button><div id="rawpages" hidden><label>Show raw page <select id="rawselect">…</select></label><div class="legend">…</div><div class="rawbox" id="rawbox"></div></div>`. On select change → render rawbox. Also render initial page when opened? I'll render on change and also when the section is first opened (render page 1). Simpler: render rawbox for the selected page whenever select changes; and when panel 4 renders, pre-render page 1 into rawbox (hidden anyway). Fine.
     - download: `<button class="btn primary" data-action="download">Download paragraphs as CSV</button> <span class="how">UTF-8 with BOM · every field double-quoted · CRLF · one row per paragraph · file name from the symbol</span>`.

     Rail:
     ```js
     function renderRail() {
       const rail = document.getElementById('rail');
       rail.innerHTML = '<h2>Document</h2>' + docs.map(d => {
         const r = results[d.key]; // precomputed parse for each doc? 
         ...
       }).join('');
     }
     ```
     Hmm — should I parse all docs upfront (for rail numbers) or lazily? Parsing both docs upfront is cheap (2 × ~70KB). I'll parse all discovered docs once at startup, store in a map, and re-render on selection. 

     Rail card:
     ```html
     <div class="doccard ${sel?'sel':''}">
       <button class="docselect" data-action="doc" data-key="${d.key}">
         <span class="dsym">${escHtml(doc.symbol || d.key)}</span>
         <span class="dtitle">${escHtml(doc.title || '')}</span>
         <span class="dmeta">${adopted} · ${records.length} pages</span>
       </button>
       <div class="dstats">
         <div class="bignum">${found}<span class="of">of ${refParas ?? '?'} paragraphs</span></div>
         <div class="bar"><i class="${ok?'':'bad'}" style="width:${pct}%"></i></div>
         <div class="bignum small ${flagged>0?'bad':''}">${flagged}<span class="of">pages flagged</span></div>
         <button class="linklike" data-action="tab" data-tab="panel-3">see tab 03</button>
         <div class="checks-line"><button class="linklike" data-action="tab" data-tab="panel-4">${pass} of ${total} checks pass</button></div>
       </div>
     </div>
     ```
     Hmm, plan: rail has "n pages flagged" of the document's pages (red when > 0, linking to tab 03), then "n of m checks pass" linking to tab 04. I'll render "20 of 20 pages flagged" as the big number with sub "pages flagged" and a link "tab 03 →". Let me structure: big number flagged, sub "of N pages flagged · see tab 03" where "see tab 03" is a button. And checks line as a button link. OK.

     Wait — the rail is "always visible" and shows the SELECTED document's numbers? Or each card shows its own numbers? "A card for the document: its symbol..., Under it two big serif numbers: 'n paragraphs' as found..." — per card. Since today there's one (or two), each card shows its own stats. I'll compute per doc. Good — parse all upfront.

     Footer:
     ```js
     foot.innerHTML = `Source: ${escHtml(doc.source || 'WORKSHOP_DATA.' + key)} · ${doc.built ? 'built ' + escHtml(String(doc.built)) + ' · ' : ''}${R.records.length} pages from WORKSHOP_DATA.${key}. Counting, splitting, matching and flagging are done by this page's code; no model was called and nothing left the browser.`;
     ```

     Now handleAction:
     ```js
     function handleAction(el, e) {
       const a = el.dataset.action;
       if (a === 'tab') { activateTab(el.dataset.tab); }
       else if (a === 'doc') { selectDoc(el.dataset.key); }
       else if (a === 'toggle') { toggleDetail(el.dataset.target, el); }
       else if (a === 'goto') { activateTab(el.dataset.tab); if (el.dataset.open) openSection(el.dataset.open); }
       else if (a === 'copy') { copyText(el.dataset.citation, el); }
       else if (a === 'showlines') { toggleLines(el); }
       else if (a === 'download') { downloadCSV(); }
     }
     function openSection(id) {
       const d = document.getElementById(id);
       if (d) { d.hidden = false; }
       const btn = document.querySelector(`[data-target="${id}"]`);
       if (btn) btn.setAttribute('aria-expanded', 'true');
       if (id === 'rawpages') renderRawPage();
     }
     ```
     Hmm, data-target used both for toggle buttons and goto open — the goto button has data-tab and data-open; the toggle button has data-target. In openSection I query `[data-target="id"]` — for repairlog the toggle button has data-target="repairlog". OK.

     toggleLines(btn): target = btn.dataset.target (paragraph number); full = #full-N, lines = #lines-N; if lines.hidden → show lines, hide full, btn text "Hide the PDF's lines"; else reverse.

     copyText: 
     ```js
     function copyText(text, btn) {
       const done = () => { const c = document.getElementById('copied-' + btn.dataset.target); ... };
     ```
     Hmm, the copied indicator: I'll put a span next to the button with id `copied-${p.number}` — but data-citation holds the citation; I need the paragraph number too. Add data-pnum. Then:
     ```js
     function copyText(text, pnum) {
       const finish = ok => {
         const c = document.getElementById('copied-' + pnum);
         if (c) { c.hidden = false; setTimeout(() => { c.hidden = true; }, 2000); }
       };
       if (navigator.clipboard && navigator.clipboard.writeText) {
         navigator.clipboard.writeText(text).then(() => finish(true), () => { fallbackCopy(text); finish(true); });
       } else { fallbackCopy(text); finish(true); }
     }
     function fallbackCopy(text) {
       const ta = document.createElement('textarea');
       ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
       document.body.appendChild(ta); ta.select();
       try { document.execCommand('copy'); } catch (e) {}
       document.body.removeChild(ta);
     }
     ```

     downloadCSV as drafted. Filename: (symbol || 'document').replace(/[^\w.-]+/g, '-')? Plan: "file name from the symbol with slashes replaced by hyphens". So symbol.replace(/\//g, '-') + '-paragraphs.csv'. If symbol empty → 'paragraphs.csv'.

     Raw page select: 
     ```js
     document.getElementById('rawselect').addEventListener('change', e => renderRawPage(e.target.value));
     function renderRawPage(pg) {
       const sel = document.getElementById('rawselect');
       const page = pg || (sel ? sel.value : null) || (R.records[0] && R.records[0].page);
       document.getElementById('rawbox').innerHTML = rawLinesHtml(Number(page));
     }
     ```
     Since panel 4 re-renders on doc switch, I need to re-attach the change listener after each render — or use delegation on 'change' at document level:
     ```js
     document.addEventListener('change', e => { if (e.target.id === 'rawselect') renderRawPage(e.target.value); });
     ```
     Good, attach once.

     Also after render(), if rawpages was open... state resets on doc switch — acceptable (re-render closes sections). But the tile "goto repairlog" opens it after render. Fine.

     Also: after render, call renderRawPage() to prefill rawbox (hidden). OK.

     Now — activateTab and initial: tab 1 active.

     Tablist HTML static:
     ```html
     <div class="tablist" role="tablist" aria-label="App sections">
       <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true" data-action="tab" data-tab="panel-1">01 RESULT</button>
       <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1" data-action="tab" data-tab="panel-2">02 PARAGRAPHS</button>
       <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1" data-action="tab" data-tab="panel-3">03 FLAGGED PAGES</button>
       <button role="tab" id="tab-4" aria-controls="panel-4" aria-selected="false" tabindex="-1" data-action="tab" data-tab="panel-4">04 CHECKS &amp; METHOD <span class="dot r" id="tab4dot" hidden></span></button>
     </div>
     <section role="tabpanel" id="panel-1" aria-labelledby="tab-1"></section>
     ...
     ```
     Arrow-key nav on the tablist.

     Note: clicking a tab button triggers both data-action handler (activateTab) — fine.

     Now, one concern: the click delegation checks `e.target.closest('[data-action]')` — tab buttons have data-action, good. But the prow click: rows have data-detail; the button inside has data-action="toggle" — clicking the button hits the action branch (toggleDetail with btn el). Clicking elsewhere in row hits row branch. In row branch, find the button to update aria-expanded: `row.querySelector('button[aria-expanded]')`.

     Let me unify: 
     ```js
     function toggleDetail(id, btn) {
       const d = document.getElementById(id);
       if (!d) return;
       const open = d.hidden;
       d.hidden = !open;
       if (btn) btn.setAttribute('aria-expanded', String(open));
       else { const b = document.querySelector(`button[data-target="${id}"]`); if (b) b.setAttribute('aria-expanded', String(open)); }
     }
     ```
     Row branch: `const row = e.target.closest('tr[data-detail]'); if (row) toggleDetail(row.dataset.detail, row.querySelector('button[aria-expanded]'));`

     But careful: clicking the "Copy citation" button inside a detail row — it has data-action, handled first. Clicking a link inside detail (source link) — no data-action, but closest tr[data-detail]? The detail row itself — is it `tr[data-detail]`? No, detail rows have id but not data-detail. The prow has data-detail. Clicking inside the detail row: closest('tr[data-detail]') → null (detail row doesn't have the attr). Good. But wait — clicking inside detail row, closest('[data-action]') might find... the showlines/copy buttons have data-action — handled. Links (source) → default navigation. Good.

     Hmm, one problem: the prow contains the toggle button with data-action="toggle" data-target="detail-N". Clicking it: action branch → toggleDetail('detail-N', btn). Good. Clicking other cells: row branch → toggleDetail(row.dataset.detail, row.querySelector('button[aria-expanded]')). Good.

     Now — the checks' "see rows" links: data-action="tab" data-tab="panel-2". Fine.

     Now let me also make sure: "the tab panel of a hidden tab is not focusable" — hidden attribute + CSS display:none handles it.

     Now, sizes: panel 2 with 90 paragraphs × 2 rows — fine.

     Let me write the checks with proper escaping. Details include paragraph texts (first words) — escape.

     Let me now also compute "hyphen lines": count lines (body) ending with '-': 
     ```js
     const hyphenLines = allLines.filter(l => /-\s*$/.test(l.text)).length;
     ```
     Report in method: "lines ending in a hyphen: n — none were joined (the plan's rule); if n > 0 they are joined as-is." Actually plan: "No line in the file ends with a hyphen, so no hyphen joining is done; the app counts such lines anyway and reports the number." So report count. I'll put it in the method text on tab 04.

     Now, method text on tab 04 (a short paragraph):
     "Method: pages are sorted by page number; a first line equal to the symbol is dropped as the header; trailing lines that are empty, start with 'GE.', are 6-digit date-stamp groups, or are bare 1–3 digit numbers are dropped as the footer (a bare number equal to the page number is the page number; any other is logged); the remaining lines of all pages are concatenated in page order; a line matching 'N.' or 'N. text' starts paragraph N; labelled headings ('I.', 'A.') and unlabelled headings (a short capitalised line just before a paragraph number) are separated from paragraph text; every other line belongs to the current paragraph. Lines ending in a hyphen: n (none joined). Suspect lines (a bare number, or 'N Word…') and every line after them on the same page stay in the text and are flagged. First words drop footnote marks (trailing digits) and are compared with reference.first_words after normalising quotes and dashes."

     Good.

     Now — one more check detail: "Suspect lines. n suspect lines on n pages, in n paragraphs; none is removed." My stillThere verification: suspect line text appears in paragraph textRaw. Since suspect lines stay in lines, textRaw includes them. ✓.

     Now, the header "what" sentence: "This page splits the converter's raw text into the document's numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's reference, and lists every repair it made."

     Now — the rail "DOCUMENT" heading and cards. Also the plan says rail headed "DOCUMENT". ✓.

     Let me also handle the case docs.length === 0: show a message "No document with records and a reference was found in WORKSHOP_DATA." in rail and panels. Defensive.

     Now — writing the final HTML. Let me also double check the CSS for `.btn`:
     ```css
     .btn { border:1px solid var(--ink); padding:6px 12px; font-family:var(--mono); font-size:12px; letter-spacing:.06em; background:transparent; }
     .btn:hover { background:#e9e2d2; }
     .btn.primary { background:var(--red); border-color:var(--red); color:#fff; }
     .btn.primary:hover { background:#7e1c2b; }
     .linklike { color:var(--red); text-decoration:underline; font-size:13px; }
     .coll { font-family:var(--mono); font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--red); border-bottom:1px solid var(--red); padding:2px 0; margin:14px 0 8px; }
     ```

     Detail row styling:
     ```css
     tr.detail > td { background:#efe9dc; padding:14px 18px; }
     .fulltext { font-size:16px; line-height:1.6; max-width:90ch; margin:0 0 10px; }
     .hl-suspect { background:#f3d9d9; box-shadow:0 0 0 1px #f3d9d9; }
     .facts { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:8px 24px; margin:10px 0 0; }
     .facts dt { font-family:var(--mono); font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:#6b655a; }
     .facts dd { margin:2px 0 0; font-size:14px; }
     ```

     Raw box:
     ```css
     .rawbox { border:1px solid var(--rule); background:#fbf8f1; padding:8px 0; max-height:520px; overflow:auto; font-family:var(--mono); }
     .rawline { display:flex; font-size:12px; line-height:1.5; }
     .rawline .ln { flex:0 0 46px; text-align:right; padding-right:8px; color:#9a927f; }
     .rawline .code { flex:0 0 20px; font-weight:bold; }
     .rawline .lt { flex:1; white-space:pre-wrap; word-break:break-word; padding-right:10px; }
     .c-cover{background:#e7e2f1}.c-header{background:#dce6ef}.c-heading{background:#f2e8cf}.c-paragraph{background:#e5edde}.c-suspect{background:#f5dbdb}.c-footer{background:#e8e4da}
     .code-c{color:#5b4a86}.code-h{color:#33587a}.code-t{color:#8a6a1f}.code-p{color:#3f6b34}.code-s{color:#9b2335}.code-f{color:#6b655a}
     ```
     I'll map cls → class suffix: cover→c-cover/code-c etc. In rawLinesHtml: `const map = {cover:['c-cover','code-c'], header:['c-header','code-h'], heading:['c-heading','code-t'], paragraph:['c-paragraph','code-p'], suspect:['c-suspect','code-s'], footer:['c-footer','code-f'], blank:['','']}`.

     Legend:
     ```html
     <div class="legend">
       <span><i class="chip c-cover"></i>C cover</span>
       <span><i class="chip c-header"></i>H header</span>
       <span><i class="chip c-heading"></i>T heading</span>
       <span><i class="chip c-paragraph"></i>P paragraph</span>
       <span><i class="chip c-suspect"></i>S suspect line</span>
       <span><i class="chip c-footer"></i>F footer</span>
     </div>
     ```
     .chip { display:inline-block; width:12px; height:12px; margin-right:5px; border:1px solid var(--rule); }

     OK. Now, let me also think about the tab 02 "Section" column width — sections can be long ("Right to work (art. 6)") — fine.

     Now assemble everything. Also add `<meta name="color-scheme" content="light">`? Not needed.

     Title of the page: "Paragraphs out of a PDF · {symbol}".

     Let me also handle: `escAttr` = escHtml basically (escape quotes). Use one esc function for both.

     Now — potential pitfall: innerHTML with paragraph text containing `</script>`? No — text is inserted into HTML, escaped via escHtml. But careful: I'm building the whole app inside a <script> tag — the script content itself must not contain the string "</script>" — my code doesn't. But template literals containing `</` sequences? escHtml output could contain `&lt;/...` — fine. But my source code contains "</tr>" etc. inside template literals — that's fine, only "</script" is problematic. OK.

     Another pitfall: `p.text.slice(0,120).replace(/\s+\S*$/, '')` — if no space in first 120 chars, replace does nothing → cut mid-word; acceptable ("cut at a word" — if no word boundary, just cut). Fine.

     Now, the checks — let me finalize the exact list and statuses:

     ```js
     const checks = [];
     // 1
     checks.push({ name: 'Paragraph count', status: refParas == null ? 'notrun' : (found === refParas ? 'pass' : 'fail'),
       detail: `found ${found} numbered paragraphs; reference.paragraphs = ${refParas == null ? 'missing' : refParas}` + (refParas != null && found !== refParas ? ` (difference ${found - refParas})` : ''), link: 'panel-2' });
     // 2 numbering
     ...
     ```

     For numbering: expected 1..found in order:
     ```js
     const bad = [];
     R.paragraphs.forEach((p, i) => { if (p.number !== i + 1) bad.push(`position ${i + 1} holds para. ${p.number} (p. ${p.page_start})`); });
     const dup = R.paragraphs.length !== new Set(R.paragraphs.map(p => p.number)).size;
     status = (bad.length === 0 && !dup) ? 'pass' : 'fail';
     detail = bad.length || dup ? 'gaps or duplicates: ' + bad.join('; ') + (dup ? ' (duplicate numbers)' : '') : `numbers run 1–${found} in order, no gaps, no duplicates`;
     ```

     // 3 first words — as drafted. link panel-2.
     // 4 suspect lines — link panel-3.
     // 5 pages flagged — informational pass. detail lists pages. link panel-3.
     // 6 headers/footers — link panel-4 (raw pages). detail includes warnings.
     // 7 headings — informational pass. link panel-2 (headings box). Hmm, link to panel-2. OK.
     // 8 nothing lost — link panel-4.

     Statuses: 5 and 7 always 'pass'? They're informational; the plan says a failed check never hides a result. For 5: "A flag is not a failure" — so status pass with the list. For 7: pass with list. OK.

     Now, one more consideration — the plan says checks panel is "open, every check on one line". ✓.

     Repair log counts per kind: 
     ```js
     const kinds = {}; R.repairs.forEach(r => { kinds[r.kind] = (kinds[r.kind] || 0) + 1; });
     const countsLine = Object.keys(kinds).sort().map(k => `${k} ×${kinds[k]}`).join(' · ');
     ```

     Repair table rows:
     ```js
     R.repairs.map(r => `<tr><td class="num">${r.page}</td><td>${r.para != null ? 'para. ' + r.para : (r.kind.includes('footnote') || r.kind.includes('bare') ? 'footnote' : '—')}</td><td>${escHtml(r.kind)}</td><td class="mono-cell">${escHtml(r.before)}</td><td class="mono-cell">${escHtml(r.after)}</td></tr>`).join('')
     ```
     Column header "Paragraph or footnote": for bare-number repairs, target is a footnote number → 'footnote'. For header/footer → '—' or 'page'. I'll show 'page' for header/footer-line removals? The column is "Paragraph or footnote" — for page-level repairs show '—'. For bare number → 'footnote'. OK.

     Truncate before/after to, say, 300 chars with ellipsis + title attr? I'll show full; cells wrap. Fine, but heading-join 'before' could be long — fine.

     Now the CSV — also include text_lines. And suspect_lines format: `p.3 L12 “…”` joined ' ; '. repairs: kinds joined '; '.

     Let me now also double-check the "first words" reference key: `reference.first_words` keyed by paragraph number as string, value = first six words string. ✓.

     norm function:
     ```js
     function norm(s) {
       return String(s).replace(/[“”]/g, '"').replace(/[‘’]/g, "'").replace(/[–—]/g, '-').replace(/\s+/g, ' ').trim();
     }
     ```

     Now — the rail bar: pct = refParas ? Math.min(100, found / refParas * 100) : 100; class bad if refParas != null && found !== refParas.

     Now let me think about whether the walk handles the actual E/C.12/GC/27 structure correctly. Page 1: after header removal, body lines: "", "United Nations", "", "Economic and Social Council", "", "Distr.: General", "6 November 2025", "Original: English", "", "Committee on Economic, Social and Cultural Rights", "", "General comment No. 27 (2025) on economic, social and", "cultural rights and the environmental dimension of", "sustainable development*", "I.", "", "Introduction", "1.", "A clean, healthy...".

     Walk: mode cover. Blanks skipped. "United Nations" — not parastart, not label (labelRe1: "United Nations" no; labelRe2: `^([IVX]+|[A-Z])\.\s+` — "United Nations" starts with "U" then "nited" — `[A-Z]\.` requires period after single letter — "Un" no. OK not label). isUnlab? next line is blank → psOf(blank) null → no. → cover. Similarly others. "6 November 2025" → cover (not suspect since cover mode — suspect check only applies to paragraph lines ✓). "I." → labelRe1 matches → heading. Collect: skip blank, "Introduction" → titleLines ['Introduction']; next "1." parastart → break. h.title = 'Introduction'. partLabel = 'I.', partTitle='Introduction', sectionTitle='Introduction', sectionFull='I. Introduction'. mode='heading', i=j-1 → next iteration processes "1." → parastart → paragraph 1 with section 'Introduction', path 'I. Introduction', part 'I. Introduction'. 

     Then paragraph 1's lines until "2." etc. Footnote block at foot of page 1: e.g. lines "2" (bare), "", "footnote text...", "3 E/..." — wait, page 1's footnotes: the sample shows page 1 ends with "tr\n[… rest omitted]" — whatever. The footnote lines are body lines (footer loop stopped at footnote text). In the walk, they're paragraph lines of the current paragraph → suspect detection: "2" bare → suspect, trigger; subsequent lines on page 1 → suspect. ✓. Then page 2's lines continue the same paragraph (if it spans) or start new. Wait — if paragraph 1 ends on page 1 and paragraph 2 starts on page 2, fine. If a paragraph spans the break, the page-2 lines are added to cur (mode paragraph) ✓ and pageSet grows → "joined across page break" repair ✓.

     Hmm — wait, one issue: the footnote block lines are added to the current paragraph (cur). If the footnote block is at the foot of page 1 and paragraph N continues on page 2, then paragraph N's lines include page-1 footnote lines AND page-2 text lines. Suspect: trigger on page 1, lines after on page 1 suspect; page 2 lines not suspect (different page) ✓.

     But — what if the paragraph ENDS at the page foot and the next paragraph starts on page 2? Then footnote lines belong to the last paragraph of page 1. ✓ flagged.

     Now headings mid-document: e.g. "IV." alone → label. But wait — could a paragraph line be exactly "IV."? No. Could a footnote line be "A."? Unlikely.

     Unlabelled headings: "Right to work (art. 6)" followed by "23." → isUnlab: length ≤ 90 ✓, starts capital ✓, ends with ")" — not in [.;:,] and not digit ✓ → heading ✓, logged 'heading separated from paragraph text' ✓.

     But careful — the unlabelled check requires mode !== 'heading'. When the previous line was paragraph text, mode === 'paragraph' ✓.

     Hmm, wait — there's an ordering bug in my walk: I check `lab` BEFORE `isUnlab`. A line like "A." followed by parastart? labelRe1 matches first → labelled heading. Fine.

     Another subtle case: what if an unlabelled heading line is followed by a parastart, but the heading line is > 90 chars or ends with a period → treated as paragraph text (last line of previous paragraph). Per plan ✓.

     Now — the "23 unlabelled headings" and "a naive split glues them to the previous paragraph" — handled ✓.

     What about lettered subsections "A." whose title wraps over two lines: "A.", "", "Violence against women", "and girls in all their diversity" — collection: skip blanks, "Violence..." → titleLines[0]; "and girls..." starts lowercase → joined, repair logged ✓.

     Now — one more: the plan says for labelled headings, "skip blank lines, then every line up to the next label line or paragraph start is heading text". My collection loop skips blanks anywhere and breaks on parastart/label. But it does NOT break on unlabelled-heading-looking lines — per plan, they're heading text. OK.

     Edge: what if after a label there are NO title lines (next is parastart)? h.title = '' — sectionTitle = label + '.'? I set sectionTitle = h.title || (h.label + '.') for roman; for lettered: (h.label + '. ' + h.title).trim() → "A." if empty. OK.

     Now — pageInfo lines cls for raw viewer: body lines get cls in walk; but note the walk sets cls on allLines entries which are the same objects as in pageInfo lines ✓ (I push references).

     Wait — in the walk, heading-collection sets nl.cls = 'heading' for consumed lines ✓. Blank body lines: cls='blank' ✓.

     Now — "Nothing lost" counts: I iterate pageInfo lines; cls values: 'blank' excluded; others counted. Suspect lines have cls 'paragraph' + suspect flag → counted as paragraph, and I separately count suspect. ✓.

     Now, let me also make sure the footer loop doesn't eat body when a page has NO footer (e.g., last page ends with paragraph text) — loop breaks immediately ✓.

     Potential issue: page 1's footer "GE.25-15926 (E)" — starts with "GE." ✓ dropped. Date stamp "051125 061125" ✓ dropped. But what if order is date stamp then GE? Loop handles any order ✓.

     What about a footer line like "20" (page number) on page 20 ✓.

     Now — the displaced bare numbers (6, 14, 45, ...) in footers: dropped + logged 'bare number removed from the footer' ✓. But wait — these are footnote numbers; the footnote text on the page has no number. The footnote text's first line — e.g. "E/2003/22, para. 5." — hmm, does it match suspect rule 2? Starts with "E" — no leading digits → NOT suspect by rule 2. Then the next footnote "7 E/..." IS suspect → trigger → lines after on that page suspect. But the first footnote's text lines (before "7 ...") are NOT marked suspect. Hmm — the user said "on each page the first suspect line is that page's first footnote number" — implying on displaced pages the first footnote still has a number line? Confusing. Whatever — my implementation follows the stated rule; the flagging will still catch the page (via the "7 ..." line or the bare number of the first footnote if present). Actually wait — on displaced pages, the first footnote's number went to the footer, so the footnote block starts with text. If that text starts with a capital non-digit... not suspect. But subsequent footnotes "7 ..." are suspect → page flagged ✓. The user's claim "first suspect line is that page's first footnote number" might refer to pages where the first footnote kept its bare-number line. Either way, pages get flagged. Good enough — and the plan explicitly says the rule flags all 20 pages on this file.

     Hmm, but wait: what if a page has only ONE footnote and its number was displaced? Then the footnote text (no number) might not match rule 2 → page not flagged. The user says all 20 pages get flagged, so this doesn't happen here. OK.

     Let me broaden rule 2 slightly to be safer? The plan is explicit about the rule; I'll follow it exactly. Actually — hmm, let me reconsider: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". A UN document symbol like "E/2003/22" — starts with capital E. So "a capital letter" already covers symbols. Quotation mark: "“...". So regex `/^\d{1,3}\s+[A-Z"“”‘’]/`. ✓.

     Now, let me write the final code. I'll be methodical. Also keep line count reasonable (~900-1100 lines).

     One more UI element: tab 01 tile 2's link "see tab 03" and tile 4's "repair log on tab 04" — buttons with data-action.

     Also the plan wants on tab 01 tile 2: "The document has `reference.footnotes` footnotes; this version does not separate them" — include when ref.footnotes != null.

     Let me write out the document now.

     Also — I should double check: "Every row that shows a document has its symbol, linked to doc_url in a new tab." In tab 02 rows show paragraphs of the document; the expanded row has the source link ✓. Tab 03 rows are pages — I'll include symbol link in the note line. Header has it ✓. Rail card: I'll make the symbol a link too (inside the docselect button? nested interactive — no. I'll put the link in the card meta line outside the button). Actually simpler: rail card symbol as plain text; header has the link. The rule says "every row that shows a document" — rows showing documents... our rows show paragraphs/pages, and the expanded paragraph shows the symbol link. I'll also add symbol link in tab 03 note and tab 04 source line. Good enough.

     Now — writing. Let me draft the complete file:

     ```html
     <!doctype html>
     <html lang="en">
     <head>
     <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <title>Paragraphs out of a PDF</title>
     <style>
     ... (as designed)
     </style>
     </head>
     <body>
     <header class="top">
       <div class="topleft">
         <div class="kicker">UN DOCUMENT · PDF TEXT</div>
         <h1 id="docTitle"></h1>
         <p class="meta" id="docMeta"></p>
         <p class="what">This page splits the converter's raw text into the document's numbered paragraphs, removes headers and footers, flags the pages where footnote text may sit inside a paragraph, checks itself against the document's reference, and lists every repair it made.</p>
       </div>
       <div class="status" id="statusBox"></div>
     </header>
     <div class="layout">
       <aside class="rail" id="rail" aria-label="Documents"></aside>
       <main>
         <div class="tablist" role="tablist" aria-label="Sections" id="tablist">
           <button role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true" data-action="tab" data-tab="panel-1">01 RESULT</button>
           <button role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" tabindex="-1" data-action="tab" data-tab="panel-2">02 PARAGRAPHS</button>
           <button role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" tabindex="-1" data-action="tab" data-tab="panel-3">03 FLAGGED PAGES</button>
           <button role="tab" id="tab-4" aria-controls="panel-4" aria-selected="false" tabindex="-1" data-action="tab" data-tab="panel-4">04 CHECKS &amp; METHOD<span class="tdot" id="tab4dot" hidden></span></button>
         </div>
         <section role="tabpanel" id="panel-1" aria-labelledby="tab-1" tabindex="0"></section>
         <section role="tabpanel" id="panel-2" aria-labelledby="tab-2" tabindex="0" hidden></section>
         <section role="tabpanel" id="panel-3" aria-labelledby="tab-3" tabindex="0" hidden></section>
         <section role="tabpanel" id="panel-4" aria-labelledby="tab-4" tabindex="0" hidden></section>
       </main>
     </div>
     <footer class="foot" id="foot"></footer>
     <script>
     ... 
     </script>
     </body>
     </html>
     ```

     Now the script. Let me write it fully:

     ```js
     (function () {
       'use strict';
       var W = window.WORKSHOP_DATA || {};

       function esc(s) {
         return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
       }
       function norm(s) {
         return String(s == null ? '' : s).replace(/[\u201C\u201D]/g, '"').replace(/[\u2018\u2019]/g, "'").replace(/[\u2013\u2014]/g, '-').replace(/\s+/g, ' ').trim();
       }

       // ---- discover documents: every value in WORKSHOP_DATA with records (and ideally a reference)
       var docs = [];
       Object.keys(W).forEach(function (k) {
         var v = W[k];
         if (Array.isArray(v)) { docs.push({ key: k, doc: { records: v, reference: null, title: k, symbol: '', doc_url: '', source: '' } }); return; }
         if (v && typeof v === 'object' && Array.isArray(v.records)) { docs.push({ key: k, doc: v }); }
       });
       ```

     Hmm wait — if I include bare arrays without reference, and pdf_text is actually the object, fine. But if some other key is a bare array of records without reference (none per spec), it'd show a card with no reference — acceptable ("no reference in this file"). But uhri is an object with records but no reference — my condition `Array.isArray(v.records)` includes uhri! uhri has records (recommendations) but no reference. The plan says "every document in WORKSHOP_DATA with records and a reference gets its own card". So require v.reference. But then a bare array (no reference) wouldn't qualify... For bare arrays I can't know. Decision: include objects with records AND reference; also include bare arrays (wrap, reference null) — but uhri/gc/hrc/library are objects with records and NO reference → excluded ✓. Bare arrays: only if some key is a bare array — per spec none are. I'll include bare arrays too (defensive for the sample shape), since if pdf_text were a bare array, we'd still want the app. But then symbol unknown... For a bare array, maybe there's a sibling key like pdf_text_reference? No. I'll just wrap with symbol '' and title = key. The app still works (citation "para. N"). OK:

     ```js
     Object.keys(W).forEach(function (k) {
       var v = W[k];
       if (Array.isArray(v)) { docs.push({ key: k, doc: { records: v, reference: null, title: 'Raw PDF text (' + k + ')', symbol: '', doc_url: '', source: '' } }); }
       else if (v && typeof v === 'object' && Array.isArray(v.records) && v.reference) { docs.push({ key: k, doc: v }); }
     });
     ```

     Hmm — but if pdf_text is the object WITH reference, and pdf_text_2 also, we get 2 docs. Good. If pdf_text were a bare array, we'd get it via the array branch (no reference). OK.

     Order: Object.keys order — pdf_text before pdf_text_2 presumably. Default select: prefer key 'pdf_text'.

     ```js
     var results = {}; // key -> parse result
     docs.forEach(function (d) { results[d.key] = parseDocument(d.doc); });
     var currentKey = docs.length ? ((docs.find(function (d) { return d.key === 'pdf_text'; }) || docs[0]).key) : null;
     ```

     parseDocument returns R = { doc, key?, symbol, records, ref, pageInfo, paragraphs, headings, repairs, warnings, flaggedPages (Map), checks, hyphenLines, allLines }.

     Then render functions and event wiring, then selectDoc(currentKey) → render().

     Let me now write parseDocument completely (final):

     ```js
     function parseDocument(doc) {
       var symbol = doc.symbol || '';
       var records = (doc.records || []).slice().sort(function (a, b) { return a.page - b.page; });
       var ref = (doc.reference && typeof doc.reference === 'object') ? doc.reference : null;
       var repairs = [], warnings = [], allLines = [], pageInfo = [];
       var seq = 0;
       function pushRepair(page, lineNo, para, kind, before, after) {
         repairs.push({ seq: seq++, page: page, lineNo: lineNo || 0, para: para, kind: kind, before: before, after: after });
       }

       records.forEach(function (rec) {
         var page = rec.page;
         var raw = String(rec.text == null ? '' : rec.text).split(/\r?\n/);
         var lines = raw.map(function (t, i) { return { text: t, page: page, lineNo: i + 1, cls: null, suspect: false }; });
         var info = { page: page, lines: lines, headerOK: false, pageNum: false, bare: [] };
         var fi = 0;
         while (fi < lines.length && lines[fi].text.trim() === '') { lines[fi].cls = 'blank'; fi++; }
         var bodyStart = fi;
         if (fi < lines.length && symbol !== '' && lines[fi].text.trim() === symbol) {
           lines[fi].cls = 'header'; info.headerOK = true; bodyStart = fi + 1;
           pushRepair(page, fi + 1, null, 'header line removed', lines[fi].text.trim(), '');
         } else if (fi < lines.length) {
           warnings.push('p. ' + page + ': the first non-empty line is not the symbol "' + symbol + '"');
         }
         var end = lines.length;
         while (end > bodyStart) {
           var l = lines[end - 1], t = l.text.trim();
           if (t === '') { l.cls = 'blank'; end--; continue; }
           if (/^GE\./.test(t)) { l.cls = 'footer'; pushRepair(page, l.lineNo, null, 'footer line removed', t, ''); end--; continue; }
           if (/^\d{6}(?:\s+\d{6})*$/.test(t)) { l.cls = 'footer'; pushRepair(page, l.lineNo, null, 'footer line removed', t, ''); end--; continue; }
           if (/^\d{1,3}$/.test(t)) {
             l.cls = 'footer';
             var n = parseInt(t, 10);
             if (n === page) { info.pageNum = true; pushRepair(page, l.lineNo, null, 'footer line removed', t, ''); }
             else { info.bare.push(n); pushRepair(page, l.lineNo, null, 'bare number removed from the footer', t, ''); }
             end--; continue;
           }
           break;
         }
         for (var i = bodyStart; i < end; i++) allLines.push(lines[i]);
         pageInfo.push(info);
       });

       // classification helpers
       function psOf(l) {
         var m = l.text.match(/^(\d{1,3})\.$/);
         if (m) return { num: +m[1], inline: null };
         m = l.text.match(/^(\d{1,3})\. (.+)$/);
         if (m) return { num: +m[1], inline: m[2] };
         return null;
       }
       function labOf(l) {
         var m = l.text.match(/^([IVX]+|[A-Z])\.$/);
         if (m) return { label: m[1], title: null };
         m = l.text.match(/^([IVX]+|[A-Z])\.\s+(.+)$/);
         if (m) return { label: m[1], title: m[2] };
         return null;
       }
       function blank(l) { return l.text.trim() === ''; }
       function isUnlab(l, next) {
         if (!next || !psOf(next)) return false;
         var t = l.text.trim();
         if (t.length === 0 || t.length > 90) return false;
         if (!/^[A-Z]/.test(t)) return false;
         if (/[.;:,]$/.test(t) || /\d$/.test(t)) return false;
         return true;
       }

       var paragraphs = [], headings = [], cover = [];
       var mode = 'cover', cur = null;
       var partLabel = null, partTitle = null, sectionTitle = null, sectionFull = null;

       for (var i = 0; i < allLines.length; i++) {
         var l = allLines[i];
         if (blank(l)) { l.cls = 'blank'; continue; }
         var ps = psOf(l);
         if (ps) {
           if (cur) paragraphs.push(cur);
           l.cls = 'paragraph';
           cur = { number: ps.num, startLine: l, inline: ps.inline, lines: [], pages: [l.page], pageSet: {}, section: sectionTitle, path: sectionFull, part: partLabel ? (partLabel + (partTitle ? ' ' + partTitle : '')) : '' };
           cur.pageSet[l.page] = true;
           if (ps.inline != null) {
             var il = { text: ps.inline, page: l.page, lineNo: l.lineNo, cls: 'paragraph', suspect: false, fromStart: true };
             cur.lines.push(il);
             pushRepair(l.page, l.lineNo, ps.num, 'number and text split', l.text.trim(), ps.num + '. ' + ps.inline);
           }
           mode = 'paragraph';
           continue;
         }
         var lab = labOf(l);
         if (lab && (lab.title === null || mode !== 'paragraph')) {
           if (cur) { paragraphs.push(cur); cur = null; }
           l.cls = 'heading';
           var h = { label: lab.label, titleLines: lab.title ? [lab.title.trim()] : [], page: l.page, kind: 'labelled' };
           headings.push(h);
           var j = i + 1;
           while (j < allLines.length) {
             var nl = allLines[j];
             if (blank(nl)) { nl.cls = 'blank'; j++; continue; }
             if (psOf(nl) || labOf(nl)) break;
             nl.cls = 'heading';
             var tt = nl.text.trim();
             if (h.titleLines.length === 0) h.titleLines.push(tt);
             else if (/^[a-z(]/.test(tt)) {
               var prev = h.titleLines[h.titleLines.length - 1];
               h.titleLines[h.titleLines.length - 1] = prev + ' ' + tt;
               pushRepair(nl.page, nl.lineNo, null, 'heading title joined from two lines', prev + ' ⏎ ' + tt, prev + ' ' + tt);
             } else h.titleLines.push(tt);
             j++;
           }
           h.title = h.titleLines.join(' › ');
           if (/^[IVX]+$/.test(h.label)) {
             partLabel = h.label + '.'; partTitle = h.title;
             sectionTitle = h.title || (h.label + '.');
             sectionFull = h.label + '. ' + h.title;
           } else {
             sectionTitle = (h.label + '. ' + h.title).trim();
             sectionFull = (partLabel ? partLabel + (partTitle ? ' ' + partTitle + ' › ' : ' ') : '') + h.label + '. ' + h.title;
           }
           i = j - 1;
           mode = 'heading';
           continue;
         }
         if (mode !== 'heading' && isUnlab(l, allLines[i + 1])) {
           if (cur) { paragraphs.push(cur); cur = null; }
           l.cls = 'heading';
           var uh = { label: null, titleLines: [l.text.trim()], page: l.page, kind: 'unlabelled' };
           uh.title = uh.titleLines[0];
           headings.push(uh);
           sectionTitle = uh.title;
           sectionFull = (partLabel ? partLabel + (partTitle ? ' ' + partTitle + ' › ' : ' ') : '') + uh.title;
           pushRepair(l.page, l.lineNo, null, 'heading separated from paragraph text', l.text.trim(), '(treated as a heading, not as paragraph text)');
           mode = 'heading';
           continue;
         }
         if (mode === 'cover' || cur === null) { l.cls = 'cover'; cover.push(l); }
         else {
           l.cls = 'paragraph';
           cur.lines.push(l);
           if (!cur.pageSet[l.page]) { cur.pageSet[l.page] = true; cur.pages.push(l.page); }
         }
       }
       if (cur) paragraphs.push(cur);
       ```

       Hmm — sectionFull for lettered: `(partLabel ? partLabel + (partTitle ? ' ' + partTitle + ' › ' : ' ') : '')` — if partTitle empty, partLabel + ' ' → "IV. " then + "A. Title" → "IV. A. Title" — missing ›. Let me clean: build path parts array. Simpler:
       ```js
       function joinPath(a, b) { return a ? (b ? a + ' › ' + b : a) : (b || ''); }
       ```
       sectionFull for lettered = joinPath(partLabel ? partLabel + (partTitle ? ' ' + partTitle : '') : '', h.label + '. ' + h.title). For roman: sectionFull = h.label + '. ' + h.title. For unlabelled: joinPath(romanFull, uh.title). Let me store romanFull = partLabel + (partTitle ? ' ' + partTitle : ''). OK I'll use joinPath.

       Post-processing:
       ```js
       var hyphenLines = allLines.filter(function (l) { return /-\s*$/.test(l.text); }).length;

       paragraphs.forEach(function (p) {
         if (p.pages.length > 1) {
           pushRepair(p.pages[p.pages.length - 1], null, p.number, 'paragraph joined across a page break',
             'text continues from p. ' + p.pages[0] + ' onto p. ' + p.pages[p.pages.length - 1],
             'joined into para. ' + p.number + ' (pp. ' + p.pages.join('–') + ')');
         }
         p.page_start = p.pages[0];
         p.page_end = p.pages[p.pages.length - 1];
         p.textRaw = [p.startLine].concat(p.lines).map(function (l) { return l.text; }).join('\n');
         p.text = p.lines.map(function (l) { return l.text.trim(); }).join(' ').replace(/\s+/g, ' ').trim();
         p.textLines = p.lines.map(function (l) { return l.text.trim(); }).join(' | ');
         p.suspect = [];
         var trigPage = null;
         p.lines.forEach(function (l) {
           if (l.fromStart) return;
           var t = l.text.trim();
           var self = /^\d{1,3}$/.test(t) || /^\d{1,3}\s+[A-Z"“”‘’]/.test(t);
           if (self) {
             trigPage = l.page; l.suspect = true;
             p.suspect.push({ page: l.page, lineNo: l.lineNo, text: t, why: /^\d{1,3}$/.test(t) ? 'bare number' : 'starts with a number and a space' });
           } else if (trigPage !== null && l.page === trigPage) {
             l.suspect = true;
             p.suspect.push({ page: l.page, lineNo: l.lineNo, text: t, why: 'follows a suspect line on the same page' });
           }
         });
         p.words = p.text === '' ? 0 : p.text.split(/\s+/).length;
         p.overWords = p.words > 300;
         p.flagged = p.suspect.length > 0 || p.overWords;
         var toks = p.text.split(/\s+/).map(function (t) { return t.replace(/\d+$/, ''); }).filter(function (t) { return t !== ''; });
         p.firstWordsFound = toks.slice(0, 6).join(' ');
         var refFW = (ref && ref.first_words) ? ref.first_words[String(p.number)] : null;
         p.firstWordsRef = (refFW == null) ? null : String(refFW);
         p.firstWordsMatch = (p.firstWordsRef == null) ? null : (norm(p.firstWordsFound) === norm(p.firstWordsRef));
         p.citation = (symbol ? symbol + ', ' : '') + 'para. ' + p.number;
       });

       repairs.sort(function (a, b) { return (a.page - b.page) || (a.lineNo - b.lineNo) || (a.seq - b.seq); });
       paragraphs.forEach(function (p) { p.repairList = repairs.filter(function (r) { return r.para === p.number; }); });

       var flaggedPages = {};
       paragraphs.forEach(function (p) {
         p.suspect.forEach(function (s) {
           var fp = flaggedPages[s.page] || (flaggedPages[s.page] = { page: s.page, paras: {}, suspects: [], over: [] });
           fp.paras[p.number] = true; fp.suspects.push({ page: s.page, lineNo: s.lineNo, text: s.text, why: s.why, para: p.number });
         });
         if (p.overWords) p.pages.forEach(function (pg) {
           var fp = flaggedPages[pg] || (flaggedPages[pg] = { page: pg, paras: {}, suspects: [], over: [] });
           fp.paras[p.number] = true; fp.over.push(p.number);
         });
       });
       ```

       Then checks:
       ```js
       var checks = [];
       var refParas = (ref && ref.paragraphs != null) ? ref.paragraphs : null;
       var found = paragraphs.length;
       checks.push({ name: 'Paragraph count', status: refParas == null ? 'notrun' : (found === refParas ? 'pass' : 'fail'), link: 'panel-2',
         detail: 'found ' + found + ' numbered paragraphs; reference.paragraphs = ' + (refParas == null ? 'missing' : refParas) + (refParas != null && found !== refParas ? ' (difference ' + (found - refParas) + ')' : '') });
       // numbering
       var bad = [], seen = {};
       paragraphs.forEach(function (p, idx) {
         if (p.number !== idx + 1) bad.push('position ' + (idx + 1) + ' holds para. ' + p.number + ' (p. ' + p.page_start + ')');
         if (seen[p.number]) bad.push('para. ' + p.number + ' appears more than once');
         seen[p.number] = true;
       });
       checks.push({ name: 'Numbering', status: bad.length ? 'fail' : 'pass', link: 'panel-2',
         detail: bad.length ? esc('gaps or duplicates: ' + bad.join('; ')) : 'numbers run 1–' + found + ' in order, no gaps, no duplicates' });
       // first words
       var fwHave = paragraphs.filter(function (p) { return p.firstWordsRef != null; });
       var fwBad = fwHave.filter(function (p) { return !p.firstWordsMatch; });
       checks.push({ name: 'First words', status: !(ref && ref.first_words) ? 'notrun' : (fwBad.length ? 'fail' : 'pass'), link: 'panel-2',
         detail: !(ref && ref.first_words) ? 'no first_words in the reference'
           : (fwHave.length - fwBad.length) + ' of ' + fwHave.length + ' paragraphs match reference.first_words'
             + (fwBad.length ? '; mismatches: ' + fwBad.map(function (p) { return 'para. ' + p.number + ': found “' + esc(p.firstWordsFound) + '” / reference “' + esc(p.firstWordsRef) + '”'; }).join('; ') : '') });
       // suspect lines
       var allSus = [];
       paragraphs.forEach(function (p) { p.suspect.forEach(function (s) { allSus.push({ para: p.number, text: s.text, raw: p.textRaw }); }); });
       var susPages = {}, susParas = {};
       allSus.forEach(function (s) { susPages[s.page] = true; susParas[s.para] = true; });
       var stillThere = allSus.every(function (s) { return s.raw.indexOf(s.text) !== -1; });
       checks.push({ name: 'Suspect lines', status: stillThere ? 'pass' : 'fail', link: 'panel-3',
         detail: allSus.length + ' suspect lines on ' + Object.keys(susPages).length + ' pages in ' + Object.keys(susParas).length + ' paragraphs; ' + (stillThere ? 'all still present in the paragraph text — none was removed' : 'SOME WERE REMOVED') });
       // pages flagged
       var fpKeys = Object.keys(flaggedPages).map(Number).sort(function (a, b) { return a - b; });
       checks.push({ name: 'Pages flagged', status: 'pass', link: 'panel-3',
         detail: fpKeys.length + ' pages flagged (' + fpKeys.join(', ') + '); a flag is not a failure — it marks where footnote text may sit inside a paragraph' });
       // headers/footers
       var hOK = pageInfo.filter(function (p) { return p.headerOK; }).length;
       var firstPage = records.length ? records[0].page : null;
       var pnOK = pageInfo.filter(function (p) { return p.pageNum || p.page === firstPage; }).length;
       var bareAll = [];
       pageInfo.forEach(function (p) { p.bare.forEach(function (b) { bareAll.push('p. ' + p.page + ': ' + b); }); });
       checks.push({ name: 'Headers and footers', status: (hOK === pageInfo.length && pnOK === pageInfo.length && warnings.length === 0) ? 'pass' : 'fail', link: 'panel-4',
         detail: hOK + ' of ' + pageInfo.length + ' pages opened with the symbol; ' + pnOK + ' of ' + pageInfo.length + ' footers carried the page number (p. ' + firstPage + ' is expected to have none); bare numbers removed from footers: ' + (bareAll.length ? bareAll.join(', ') : 'none') + (warnings.length ? '; warnings: ' + esc(warnings.join('; ')) : '') });
       // headings
       var labN = headings.filter(function (h) { return h.kind === 'labelled'; }).length;
       var unlab = headings.filter(function (h) { return h.kind === 'unlabelled'; });
       checks.push({ name: 'Headings', status: 'pass', link: 'panel-2',
         detail: labN + ' labelled and ' + unlab.length + ' unlabelled headings; unlabelled: ' + (unlab.length ? unlab.map(function (h) { return '“' + esc(h.title) + '” (p. ' + h.page + ')'; }).join('; ') : 'none') + ' — check these are headings, not a paragraph’s last line' });
       // nothing lost
       var counts = { cover: 0, header: 0, heading: 0, paragraph: 0, footer: 0, blank: 0, none: 0, suspect: 0 };
       var unclassified = [];
       pageInfo.forEach(function (pi) {
         pi.lines.forEach(function (l) {
           if (l.text.trim() === '') { counts.blank++; return; }
           if (l.suspect) counts.suspect++;
           if (l.cls) counts[l.cls] = (counts[l.cls] || 0) + 1; else { counts.none++; unclassified.push('p. ' + l.page + ' line ' + l.lineNo + ': “' + esc(l.text.trim().slice(0, 60)) + '”'); }
         });
       });
       var nonEmpty = 0;
       pageInfo.forEach(function (pi) { pi.lines.forEach(function (l) { if (l.text.trim() !== '') nonEmpty++; }); });
       var classified = counts.cover + counts.header + counts.heading + counts.paragraph + counts.footer;
       checks.push({ name: 'Nothing lost', status: (classified === nonEmpty && counts.none === 0) ? 'pass' : 'fail', link: 'panel-4',
         detail: nonEmpty + ' non-empty lines classified: cover ' + counts.cover + ', header ' + counts.header + ', heading ' + counts.heading + ', paragraph ' + counts.paragraph + ' (of which ' + counts.suspect + ' suspect), footer ' + counts.footer + '; sum ' + classified + (counts.none ? '; UNCLASSIFIED: ' + unclassified.join('; ') : '') });

       return { doc: doc, symbol: symbol, records: records, ref: ref, pageInfo: pageInfo, paragraphs: paragraphs, headings: headings, repairs: repairs, warnings: warnings, flaggedPages: flaggedPages, checks: checks, hyphenLines: hyphenLines, allLines: allLines, cover: cover };
     }
     ```

     Wait — counts[l.cls] where cls could be 'blank' for non-empty? No, blank cls only for empty lines (checked first). But a non-empty line with cls 'blank'? In the walk, blank(l) checks trim === '' — consistent. OK. Also cls could be 'paragraph' etc. counts initialized with those keys; if cls is something else (shouldn't be), counts[cls] created. Fine.

     Hmm — one bug: in the walk, when header not found, lines[fi] is body and gets cls in walk ✓. But if fi === lines.length (all blank), no body. OK.

     Another bug: the footer loop `while (end > bodyStart)` — if header found, bodyStart = fi+1; the loop could eat down to bodyStart, consuming ALL body lines if they all match footer patterns (e.g., a page that's just "3" + "GE..."). Edge, fine.

     Now render functions:

     ```js
     function R() { return results[currentKey]; }

     function render() {
       var r = R(), doc = r.doc;
       document.title = 'Paragraphs out of a PDF · ' + (r.symbol || currentKey);
       document.getElementById('docTitle').textContent = doc.title || ('Raw PDF text — WORKSHOP_DATA.' + currentKey);
       var meta = [];
       if (r.symbol) meta.push(doc.doc_url ? '<a href="' + esc(doc.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + '</a>' : esc(r.symbol));
       if (r.ref && r.ref.adopted != null) meta.push('adopted ' + esc(r.ref.adopted));
       meta.push(r.records.length + ' pages of raw converter text');
       if (doc.source) meta.push(esc(String(doc.source)));
       document.getElementById('docMeta').innerHTML = meta.join(' · ');
       // status
       var pass = r.checks.filter(function (c) { return c.status === 'pass'; }).length;
       var fail = r.checks.filter(function (c) { return c.status === 'fail'; }).length;
       var notrun = r.checks.filter(function (c) { return c.status === 'notrun'; }).length;
       var sb = document.getElementById('statusBox');
       if (fail > 0) sb.innerHTML = '<span class="dot r"></span>' + fail + ' of ' + r.checks.length + ' checks failed' + (notrun ? ' · ' + notrun + ' not run' : '');
       else sb.innerHTML = '<span class="dot g"></span>' + pass + ' of ' + r.checks.length + ' checks pass' + (notrun ? ' · ' + notrun + ' not run' : '');
       document.getElementById('tab4dot').hidden = fail === 0;
       renderRail();
       renderPanel1();
       renderPanel2();
       renderPanel3();
       renderPanel4();
       renderFoot();
       renderRawPage();
     }
     ```

     renderRail:
     ```js
     function renderRail() {
       var rail = document.getElementById('rail');
       if (!docs.length) { rail.innerHTML = '<h2>Document</h2><p>No document with records and a reference was found in WORKSHOP_DATA.</p>'; return; }
       rail.innerHTML = '<h2>Document</h2>' + docs.map(function (d) {
         var r = results[d.key];
         var refParas = (r.ref && r.ref.paragraphs != null) ? r.ref.paragraphs : null;
         var found = r.paragraphs.length;
         var pct = refParas ? Math.max(0, Math.min(100, found / refParas * 100)) : 100;
         var barBad = refParas != null && found !== refParas;
         var flagged = Object.keys(r.flaggedPages).length;
         var pass = r.checks.filter(function (c) { return c.status === 'pass'; }).length;
         var sel = d.key === currentKey ? ' sel' : '';
         var adopted = (r.ref && r.ref.adopted != null) ? 'adopted ' + esc(r.ref.adopted) + ' · ' : '';
         return '<div class="doccard' + sel + '">' +
           '<button class="docselect" data-action="doc" data-key="' + esc(d.key) + '">' +
             '<span class="dsym">' + esc(r.symbol || d.key) + '</span>' +
             '<span class="dtitle">' + esc(d.doc.title || '') + '</span>' +
             '<span class="dmeta">' + adopted + r.records.length + ' pages</span>' +
           '</button>' +
           '<div class="dstats">' +
             '<div class="bignum">' + found + '<span class="of">of ' + (refParas == null ? '?' : refParas) + ' paragraphs</span></div>' +
             '<div class="bar"><i class="' + (barBad ? 'bad' : '') + '" style="width:' + pct + '%"></i></div>' +
             '<div class="bignum small' + (flagged > 0 ? ' bad' : '') + '">' + flagged + '<span class="of">of ' + r.records.length + ' pages flagged</span></div>' +
             '<button class="linklike" data-action="tab" data-tab="panel-3">see tab 03</button>' +
             '<div class="checksline"><button class="linklike" data-action="tab" data-tab="panel-4">' + pass + ' of ' + r.checks.length + ' checks pass</button></div>' +
           '</div>' +
         '</div>';
       }).join('');
     }
     ```

     renderPanel1:
     ```js
     function renderPanel1() {
       var r = R();
       var refParas = (r.ref && r.ref.paragraphs != null) ? r.ref.paragraphs : null;
       var found = r.paragraphs.length;
       var flagged = Object.keys(r.flaggedPages).length;
       var fwMatch = r.paragraphs.filter(function (p) { return p.firstWordsMatch === true; }).length;
       var fwHave = r.paragraphs.filter(function (p) { return p.firstWordsRef != null; }).length;
       var paraOK = refParas != null && found === refParas;
       var t1sub = refParas == null ? 'no reference in this file' : 'The document has: ' + refParas + (paraOK ? ' — equal' : ' — difference: ' + (found - refParas));
       var t2sub = '';
       if (flagged > 0) t2sub += '<button class="linklike" data-action="tab" data-tab="panel-3">footnote text may sit inside a paragraph; see tab 03</button> ';
       if (r.ref && r.ref.footnotes != null) t2sub += 'The document has ' + esc(r.ref.footnotes) + ' footnotes; this version does not separate them.';
       else if (flagged === 0) t2sub += 'no page flagged';
       var t3sub = (r.ref && r.ref.first_words) ? 'of ' + (refParas != null ? refParas : fwHave) + ' paragraphs in reference.first_words' : 'no reference in this file';
       document.getElementById('panel-1').innerHTML =
         '<div class="tiles">' +
         tile(found, paraOK ? 'good' : (refParas == null ? '' : 'bad'), 'paragraphs found', t1sub, 'How this is computed: a line matching “N.” or “N. text” starts paragraph N; header and footer lines are removed first; the count is a loop over the result, compared with reference.paragraphs.') +
         tile(flagged, flagged > 0 ? 'bad' : '', 'pages flagged', t2sub, 'How this is computed: a line inside a paragraph that is a bare number or starts “N Word…” is suspect, and every line after it on the same page is suspect too; a paragraph over 300 words is flagged as well.') +
         tile(fwMatch, '', 'first words match', t3sub, 'How this is computed: the first six words of each paragraph, footnote marks (trailing digits) dropped, compared with reference.first_words after normalising quotes and dashes.') +
         tile(r.repairs.length, '', 'repairs made', '<button class="linklike" data-action="goto" data-tab="panel-4" data-open="repairlog">see the repair log on tab 04</button>', 'How this is computed: every line the script removed, split, joined or separated, logged in document order on tab 04.') +
         '</div>';
     }
     function tile(num, cls, lab, sub, how) {
       return '<div class="tile"><div class="tnum ' + cls + '">' + num + '</div><div class="tlab">' + esc(lab) + '</div><div class="tsub">' + sub + '</div><div class="how">' + esc(how) + '</div></div>';
     }
     ```
     Hmm — tile 2's big number: "n of the document's pages" — I'll make the big number flagged and sub includes "of N pages". Let me adjust: tile(flagged + ' of ' + r.records.length)? Big numbers should be just numbers... The plan: "Pages flagged: n of the document's pages". I'll put big "20" and sub "of 20 pages · footnote text may sit…". Let me restructure tile 2: num=flagged, lab='pages flagged', sub='of ' + records.length + ' pages' + (flagged>0 ? ' · <button…>footnote text may sit inside a paragraph; see tab 03</button>' : '') + footnotes note. OK.

     Also tile 3: big fwMatch, sub 'of ' + m + ' paragraphs match reference.first_words' — hmm lab 'first words match', sub 'of m paragraphs in the reference'. Fine.

     renderPanel2:
     ```js
     function renderPanel2() {
       var r = R();
       var refParas = (r.ref && r.ref.paragraphs != null) ? r.ref.paragraphs : null;
       var rows = r.paragraphs.map(function (p) {
         var pages = p.page_start === p.page_end ? String(p.page_start) : p.page_start + '–' + p.page_end;
         var first = p.text.length > 120 ? (p.text.slice(0, 120).replace(/\s+\S*$/, '') + '…') : p.text;
         var check;
         var parts = [];
         if (p.firstWordsMatch === false) parts.push('first words differ');
         if (p.flagged) parts.push('may contain footnote text');
         if (parts.length) check = '<span class="check-bad">' + parts.join(' · ') + '</span>';
         else if (p.firstWordsMatch === null) check = '<span class="check-dim">not checked</span>';
         else check = '<span class="check-ok">OK</span>';
         return '<tr class="prow" data-detail="detail-' + p.number + '">' +
           '<td class="num pnum"><button data-action="toggle" data-target="detail-' + p.number + '" aria-expanded="false" aria-controls="detail-' + p.number + '">' + p.number + '</button></td>' +
           '<td class="sec">' + esc(p.section || '—') + '</td>' +
           '<td class="num">' + pages + '</td>' +
           '<td class="first">' + esc(first) + '</td>' +
           '<td>' + check + '</td></tr>' +
           '<tr class="detail" id="detail-' + p.number + '" hidden><td colspan="5">' + detailHtml(p) + '</td></tr>';
       }).join('');
       var hbox = '<button class="coll" data-action="toggle" data-target="headingsbox" aria-expanded="false" aria-controls="headingsbox">Headings found: ' + r.headings.length + '</button>' +
         '<div id="headingsbox" hidden><ul class="hlist">' + r.headings.map(function (h) {
           return '<li>' + (h.kind === 'labelled' ? '<b>' + esc(h.label + '.') + '</b> ' : '') + esc(h.title) + ' <span class="dim">(p. ' + h.page + ')</span></li>';
         }).join('') + '</ul></div>';
       document.getElementById('panel-2').innerHTML =
         hbox +
         '<table><caption><span class="tabno">TAB.01</span>' + r.paragraphs.length + ' paragraphs found' + (refParas != null ? ', ' + refParas + ' expected' : '') + ' — click a row for the full text</caption>' +
         '<thead><tr><th scope="col" class="num">No.</th><th scope="col">Section</th><th scope="col" class="num">Page</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead>' +
         '<tbody>' + rows + '</tbody></table>' +
         '<p class="src">Source: ' + (r.doc.doc_url ? '<a href="' + esc(r.doc.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + '</a>' : esc(r.symbol)) + ' · n = ' + r.paragraphs.length + ' paragraphs computed from ' + r.records.length + ' pages of raw converter text in WORKSHOP_DATA.' + esc(currentKey) + '.</p>';
     }
     ```

     detailHtml(p) as drafted. fullTextHtml, paraLinesHtml as drafted.

     renderPanel3:
     ```js
     function renderPanel3() {
       var r = R();
       var keys = Object.keys(r.flaggedPages).map(Number).sort(function (a, b) { return a - b; });
       var note = '<p class="note">This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF. The next step can separate them.</p>';
       if (!keys.length) {
         document.getElementById('panel-3').innerHTML = note + '<p>No page is flagged: no suspect line was found inside any paragraph.</p>';
         return;
       }
       var rows = keys.map(function (pg) {
         var fp = r.flaggedPages[pg];
         var paras = Object.keys(fp.paras).map(Number).sort(function (a, b) { return a - b; }).map(function (n) { return 'para. ' + n; }).join(', ');
         var whys = {};
         fp.suspects.forEach(function (s) { whys[s.why] = true; });
         if (fp.over.length) whys['paragraph over 300 words'] = true;
         return '<tr class="prow" data-detail="fpage-' + pg + '">' +
           '<td class="num pnum">' + pg + '</td>' +
           '<td>' + paras + '</td>' +
           '<td class="num">' + fp.suspects.length + '</td>' +
           '<td>' + esc(Object.keys(whys).join('; ')) + '</td></tr>' +
           '<tr class="detail" id="fpage-' + pg + '" hidden><td colspan="4">' +
             '<p class="dim">Raw lines of page ' + pg + ' — suspect lines are marked S and highlighted. They sit in ' + paras + '.</p>' +
             '<div class="rawbox">' + rawLinesHtml(pg) + '</div>' +
           '</td></tr>';
       }).join('');
       document.getElementById('panel-3').innerHTML = note +
         '<table><caption><span class="tabno">TAB.02</span>' + keys.length + ' of ' + r.records.length + ' pages flagged — click a row to see the raw lines</caption>' +
         '<thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph</th><th scope="col" class="num">Suspect lines</th><th scope="col">Why</th></tr></thead>' +
         '<tbody>' + rows + '</tbody></table>' +
         '<p class="src">Source: ' + (r.doc.doc_url ? '<a href="' + esc(r.doc.doc_url) + '" target="_blank" rel="noopener">' + esc(r.symbol) + '</a>' : esc(r.symbol)) + ' · suspect lines stay in the paragraph text; nothing was removed.</p>';
     }
     ```

     renderPanel4:
     ```js
     function renderPanel4() {
       var r = R();
       var checksHtml = r.checks.map(function (c) {
         var cls = c.status === 'pass' ? 'pass' : c.status === 'fail' ? 'fail' : 'notrun';
         var label = c.status === 'pass' ? 'pass' : c.status === 'fail' ? 'check failed' : 'not run';
         return '<div class="check ' + cls + '"><span class="cname">' + esc(c.name) + '</span> <span class="cdetail">' + c.detail + '</span> <span class="cstatus">' + label + '</span>' +
           (c.status === 'fail' && c.link ? ' <button class="linklike" data-action="tab" data-tab="' + c.link + '">see rows</button>' : '') + '</div>';
       }).join('');
       // repair log
       var kinds = {};
       r.repairs.forEach(function (x) { kinds[x.kind] = (kinds[x.kind] || 0) + 1; });
       var countsLine = Object.keys(kinds).sort().map(function (k) { return esc(k) + ' ×' + kinds[k]; }).join(' · ');
       var rrows = r.repairs.map(function (x) {
         var target = x.para != null ? 'para. ' + x.para : (x.kind === 'bare number removed from the footer' ? 'footnote' : '—');
         return '<tr><td class="num">' + x.page + '</td><td>' + target + '</td><td>' + esc(x.kind) + '</td><td class="mono">' + esc(x.before) + '</td><td class="mono">' + esc(x.after) + '</td></tr>';
       }).join('');
       var repairLog = '<button class="coll" data-action="toggle" data-target="repairlog" aria-expanded="false" aria-controls="repairlog">Repair log (' + r.repairs.length + ')</button>' +
         '<div id="repairlog" hidden><p class="dim">' + countsLine + '</p>' +
         '<table><caption><span class="tabno">TAB.03</span>Every change the script made, in document order</caption>' +
         '<thead><tr><th scope="col" class="num">Page</th><th scope="col">Paragraph or footnote</th><th scope="col">What was done</th><th scope="col">Before</th><th scope="col">After</th></tr></thead>' +
         '<tbody>' + rrows + '</tbody></table></div>';
       // raw pages
       var opts = r.records.map(function (rec) { return '<option value="' + rec.page + '">Show raw page ' + rec.page + '</option>'; }).join('');
       var rawPages = '<button class="coll" data-action="toggle" data-target="rawpages" aria-expanded="false" aria-controls="rawpages">Raw pages</button>' +
         '<div id="rawpages" hidden>' +
           '<label class="rawlabel">Page <select id="rawselect">' + opts + '</select></label>' +
           '<div class="legend">' + legendHtml() + '</div>' +
           '<div class="rawbox" id="rawbox"></div>' +
         '</div>';
       var method = '<p class="method"><b>Method.</b> Pages are sorted by page number. A first non-empty line equal to the symbol is dropped as the header. From the end of each page, lines that are empty, start with “GE.”, are 6-digit date-stamp groups, or are bare 1–3 digit numbers are dropped as the footer; a bare number equal to the page number is the page number, any other is logged. The remaining lines of all pages are concatenated in page order. A line matching “N.” or “N. text” starts paragraph N. Labelled headings (“I.”, “A.”) and unlabelled headings (a short capitalised line just before a paragraph number) are separated from paragraph text. Every other line belongs to the current paragraph. Lines ending in a hyphen: ' + r.hyphenLines + ' (none were joined). Suspect lines stay in the text and are flagged. First words drop footnote marks (trailing digits) and are compared with reference.first_words after normalising quotes and dashes. Counting, filtering and matching are done by this page’s code.</p>';
       document.getElementById('panel-4').innerHTML =
         '<h3 class="ph">Checks — can I trust this?</h3>' + checksHtml + method + repairLog + rawPages +
         '<h3 class="ph">Take it away</h3>' +
         '<p><button class="btn primary" data-action="download">Download paragraphs as CSV</button></p>' +
         '<p class="how">UTF-8 with a byte-order mark · every field double-quoted, inner quotes doubled · CRLF line ends · one row per paragraph · columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, text_lines, flagged, suspect_lines, repairs, citation, symbol, doc_url · file name from the symbol with slashes replaced by hyphens.</p>';
     }
     ```

     legendHtml: chips.

     renderFoot:
     ```js
     function renderFoot