Build the app per the detailed plan. Single HTML file, four tabs, left rail, checks, exports. Keep under ~1500 lines. Write carefully.

Key implementation: parse html_doc.html with DOMParser, classify elements, extract paragraphs, repairs, checks, exports.

Let me write the code compactly but complete. Include hidden CSS rule, tablist with arrow keys, expandable rows, copy citation, JSON/Markdown downloads, elements box, credits line (Turing Way / Analysis Function / DAG are guidance, not code — plan mentions them; I'll add credits lines only for open-licence code, which I don't copy, so skip credits or just cite sources in footer? The instruction: credits only for code/wording from Reference shelf excerpts. Not applicable, skip).

Design: warm off-white #f4f0e8, ink #1d1b18, rules #d9d2c3, red #9b2335, green #1e6b3a for pass.

Let me write it.

Structure:
- header: label, title, meta line, right: dot + checks pass + "1 source limit"
- tabs
- left rail + main content grid

Left rail: document card, big numbers paragraphs found/expected with bar, footnotes 0 of n, checks link.

Tabs:
01 RESULT: 4 tiles.
02 PARAGRAPHS: closed "Headings found" box, table rows expandable.
03 LOST & CHANGED: three blocks.
04 CHECKS & EXPORT: check panel, export buttons, closed elements box.

Footer.

Pipeline:

```js
const D = WORKSHOP_DATA.html_doc;
const doc = new DOMParser().parseFromString(D.html, 'text/html');
const els = [...doc.body.querySelectorAll('table, .content > *')]; 
```

Better: iterate over body's block elements in order. Use body.children? The sample shows table then div.content with children. To be safe: collect all elements in document order: cover table first, then within div.content. Simplest: `const all = [...doc.body.querySelectorAll('*')]`? That includes nested spans. Instead: take the cover table (first table), then all children of the div.content, or if no .content, body children excluding the table. I'll do:

```js
const coverTable = doc.body.querySelector('table');
const container = doc.body.querySelector('.content') || doc.body;
let elements = [];
if (coverTable && coverTable !== container) elements.push(coverTable);
[...container.children].forEach(el => { if (el !== coverTable) elements.push(el); });
```

But if container is body, children includes the table — handled by skip. Also .content children include p, h2, h3.

Classification per element:
- tag TABLE → cover
- p matching /^(\d{1,3})\.\s*(.*)$/s → paragraph
- first h2 → title
- other h2/h3 → heading
- other p → committee line

Headings: split /^([IVX]+|[A-Z])\.\s*(.+)$/ → label, heading text. Count glued labels (original without space, i.e. test raw text matched /^([IVX]+|[A-Z])\.(?!\s)/... just check if original doesn't have space after dot). I'll check `!/^[IVX]+\.\s/.test(raw)` meaning glued. Actually simpler: glued if the label match on raw text has no whitespace after the period — use regex /^([IVX]+|[A-Z])\.(?=\S)/ on raw.

Paragraph text_raw: text after number, trim, collapse whitespace. Note `\s*` after the dot.

Repairs with logging: apply rules sequentially on text_raw, logging each insertion with context ±20 chars. I'll implement a function that replaces with callback and logs position. To mark places in expanded paragraph, I'll store the positions in the repaired text or re-render by walking rules. Simpler: store repair offsets — compute by scanning text with the same regexes in order. Actually order matters. Let me apply rules one at a time, tracking a "marks" list of offsets in the final text. Approach: maintain text and list of inserted-space positions; for each rule, do a global replace with function(match, ...) computing insertion index; but offsets shift after later insertions. Since insertions only add characters, I can apply rules in a fixed order and adjust previously recorded positions... Simpler alternative: build the final text and record marks by re-running rules cumulatively? 

Easiest robust approach: apply all rules in one pass over text_raw using a combined regex? Rules:
- /([a-z])\.([A-Z])/ → "$1. $2"
- /([a-z]),([A-Za-z])/ → "$1, $2"
- /([a-z])“/ → "$1 “"
- /–([A-Za-z])/ → "– $1"

I can do a single pass with alternation and record insertion positions in the output string as I build it manually:

```js
function repair(raw){
  let out = '', marks = [], i = 0;
  const re = /([a-z])\.([A-Z])|([a-z]),([A-Za-z])|([a-z])“|–([A-Za-z])/g;
  let m;
  while ((m = re.exec(raw))) {
    out += raw.slice(i, m.index);
    let ins;
    if (m[1]!==undefined){ out += m[1] + '. ' + m[2]; ins = m.index + 2; }
    else if (m[3]!==undefined){ out += m[3] + ', ' + m[4]; ins = m.index + 2; }
    else if (m[5]!==undefined){ out += m[5] + ' “'; ins = m.index + 2; }
    else { out += '– ' + m[6]; ins = m.index + 1; }
    marks.push(ins);
    i = re.lastIndex;
  }
  out += raw.slice(i);
  return {text: out, marks};
}
```

Wait but overlapping: e.g. "a.B" — after replacement, lastIndex continues past; that's fine, non-overlapping matches. But combined regex single pass differs slightly from sequential application (e.g. dash rule on a char changed by earlier rule — but rules only insert spaces, and inserted spaces wouldn't be matched again by these patterns anyway... a space after period before capital: pattern [a-z]\.[A-Z] requires adjacency, inserted space breaks adjacency so no re-match. Good enough; single pass equals sequential in effect here). Log rule name per mark. Also log context: 20 chars each side in raw or in text. For the table on tab 03, show Before (raw context) and After (text context) — I'll compute contexts from raw around the match and from text around insertion point.

Rule names: "sentence join", "comma join", "quote join", "dash join".

Characters count: over all paragraph texts (I'll count over text concatenated, or text_raw — same counts since rules only insert spaces).

First words: normalize function: curly quotes straight (‘’“” → ' '), en dash and U+2011 → '-', nbsp → ' '. Compare first six whitespace words of text vs reference.first_words[String(n)].

Sections: nearest heading above (h2 or h3 heading, use its display: label + '. ' + heading or just heading if no label... display = raw trimmed heading text is fine — but glued labels like "I.Introduction"; I should show separated: label + '. ' + rest). part = nearest roman h2 label + heading.

Checks:
1. paragraph count: found vs reference.paragraphs
2. numbering: 1..n in order, gaps/dupes
3. first words: n match of total; list mismatches
4. footnotes: 0 vs reference.footnotes → "source limit"
5. repairs: counts per rule
6. headings: h2/h3 counts + glued labels separated count
7. nothing lost: elements all classified; counts sum; list unclassified
8. export round trip: parse JSON.stringify back, record count equals table count.

Pass/fail logic; failed checks link to tab 02 rows (mismatches) — I'll add links that switch tab and could scroll; keep simple: link switches to tab 02 and expands that row. I'll implement a function openPara(n).

Exports: build JSON array; Markdown with front matter; Blob downloads; filename symbol.replace(/\//g,'-').

Elements box: every block element in order with Tag | Classified as | Text first 80 chars.

Edge cases: missing reference fields → "not run"; no paragraphs → tab 01 message, disable exports.

Tab 03 spaces table: each repair row: Paragraph | Before | After | Rule; click opens paragraph on tab 02.

Mark repaired places in expanded paragraph: thin red box around inserted char (the space). I'll render text with marks: build HTML escaping, then wrap char at mark positions with span.mark.

Also flagged (first words differ) paragraphs — plan says "places repaired or flagged in this paragraph" in expanded row; the flag is the first-words mismatch, shown with found six vs reference six. OK.

Tab 02 row: No | Section | First line (120 chars at word + "…") | Check (OK / "first words differ" red). Expanded: full text with marks, found vs reference six words, repairs list count, Copy citation button.

Headings box: closed by default, lists headings in order.

Header right: dot green/red + "n of m checks pass" or "n checks failed", then "1 source limit". Check counting: total checks = 8; pass = those passing; source limit counted apart. So display: green dot if failures==0: "n of m checks pass"; else red "n checks failed". m = checks run? I'll say "{pass} of {pass+fail} checks pass" plus "+1 source limit". Keep simple.

Rail: symbol card, big numbers, checks link.

Tabs with arrow keys, role=tablist; panels hidden with hidden attribute + CSS rule.

Let me now write the whole file. Aim ~800 lines. Use plain JS, Chart.js not needed (no charts — plan has bar for paragraphs found; thin bar, can do with div). Fine.

Copy citation: navigator.clipboard fallback textarea.

Today's date for extracted: new Date().toISOString().slice(0,10).

Write it.