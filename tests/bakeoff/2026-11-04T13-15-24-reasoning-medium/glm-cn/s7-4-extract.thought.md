Build the app following the plan. One HTML file, four tabs, left rail, header, footer. Follow the spec carefully.

Let me write the code compactly but complete. Key logic:

Parse html with DOMParser, iterate body elements. Cover table = elements inside first `<table>`. After it: p matching /^(\d{1,3})\.\s*(.*)$/s = paragraph. First h2 = title. Other h2/h3 = heading, split label. Other p = committee line.

Repairs with regexes, log insertions. Characters counted. First words check with normalization. Checks panel. Exports JSON/Markdown.

Marks in expanded paragraph: rebuild text showing repaired places with thin red box — I can apply the same regexes but wrap in span. Simpler: for each paragraph, regenerate marked HTML by replacing with `<mark>` spans using same regexes. For raw text display, use escapeHtml first then apply regexes... careful: regexes on escaped text still work since escaping doesn't change those characters. I'll produce marked text from text_raw: escape, then apply replacements wrapping inserted space in a span.

Table captions, tablist with arrow keys, aria-expanded rows, export round trip check, elements found collapsible.

Let me write it. Aim ~700 lines.

Structure:

- header: label, title, meta line, right status dot + "1 source limit"
- tabs nav
- main grid: left rail + content panels
- footer

JS:
```
const D = WORKSHOP_DATA.html_doc;
const doc = new DOMParser().parseFromString(D.html,'text/html');
```
Iterate body children; for each element, if inside table (first table contains cover) — check `el.closest('table')`. Elements: I'll walk body's descendant block elements? The plan says "over the parsed document's body elements in order". Cover table's inner elements are cover. I'll iterate body.querySelectorAll('table, p, h2, h3, div, ...')? Simpler: collect all elements that are `p, h2, h3, table` in document order via body.querySelectorAll('p, h2, h3, table'), and mark elements whose closest table ancestor exists (and that table is the cover one) as cover. Actually the div.content wrapper too — for "Elements found" listing I'll list p, h2, h3, table, div.

Let me just do: all elements matching 'p,h2,h3,div,table' in order. For each: if closest('table') → cover (classified as "cover"). Else classify.

Committee line: p not matching paragraph pattern and after cover. Title: first h2 after cover. Other h2/h3: headings; split /^([IVX]+|[A-Z])\.\s*(.+)$/.

Paragraph regex: /^(\d{1,3})\.\s*(.*)$/s — note [\s\S] via s flag; use match.

Current heading tracking: when heading encountered, set currentHeading = {label, text, full}; roman h2 sets currentPart.

Repairs on text_raw:
- r1: /([a-z])\.([A-Z])/g → "$1. $2" (sentence)
- r2: /([a-z]),([A-Za-z])/g → comma
- r3: /([a-z])“/g → quote
- r4: /–([A-Za-z])/g → dash

Log each with before/after context (20 chars each side). I'll do via replace with callback capturing index.

First words: first six words of text vs reference.first_words[str(n)], normalize: replace curly quotes straight, en dash & U+2011 → '-', nbsp → ' '.

Characters: count over all text (or text_raw) of: – (2013), “ ” (201C/201D combined count), ’ (2019), ‑ (2011), nbsp (00A0). Example word containing it.

Checks array: each {name, detail, status: 'pass'|'fail'|'limit'|'notrun'}.

Checks:
1. Paragraph count: found vs ref.paragraphs.
2. Numbering: 1..n in order; gaps/dups.
3. First words: mismatches count.
4. Footnotes: 0 vs ref.footnotes → limit.
5. Repairs: count, per rule.
6. Headings: h2+h3 count, glued labels separated count.
7. Nothing lost: every block element classified once; unclassified listed.
8. Export round trip: JSON.parse(JSON.stringify(records)).length === table count → trivially pass but compute after building records.

Status dot: passCount vs total, excluding 'limit'? Header: green "n of m checks pass" or red "n checks failed". I'll count pass/total of non-limit checks; limits shown separately ("1 source limit").

Tabs: 4 buttons, panels with hidden, arrow-key nav, role=tablist/tab/tabpanel.

Tab 02: "Headings found: n" closed box, table rows as buttons with aria-expanded. Each row: number, section (nearest heading), first line 120 chars, check OK/differ. Expanded: full text with marked repairs, ref six words vs found six, repairs list for that para, copy citation button.

Tab 03: three blocks.

Tab 04: check panel, export buttons, elements found closed box.

Copy: navigator.clipboard may fail in sandbox; fallback textarea+execCommand. Show "Copied".

Edge cases: reference missing fields → "not run", no paragraphs → tab01 message, disable exports.

File names: symbol.replace(/\//g,'-').

Write CSS: paper palette, tabs, rail, tables, mark style.

Let me write the final code now, carefully but concisely.