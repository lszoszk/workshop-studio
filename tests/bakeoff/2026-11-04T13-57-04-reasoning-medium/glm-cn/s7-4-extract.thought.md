Build the app per the plan. Single HTML file, two tabs, left rail, checks, exports. Keep under ~1500 lines.

Let me design the pipeline:

- Parse html, walk `table, p, h2, h3` in order.
- First table = cover. Everything after that classified.
- Paragraph regex: /^(\d{1,3})\.\s*(.*)$/s
- Heading split: /^([IVX]+|[A-Z])\.\s*(.+)$/
- Repairs with logged insertions (20 chars context).
- First words compare with normalization.
- Checks: count, numbering, first words, footnotes (source limit), repairs, headings, nothing lost, export round trip.
- Tabs with role=tablist, arrow keys.
- Export JSON/Markdown via Blob.
- Tab 02: table rows expandable, copy citation button.
- Rail numbers, header.

Write code carefully but compactly. Use window.Charts? No charts needed. Fine.

Data note: reference may be missing — handle. If no paragraphs found, disable exports, message on tab 01.

Let me write the code.

Key functions:
- norm(s): curly quotes → straight, en dash & U+2011 → hyphen, nbsp → space.
- firstWords(text, n=6).
- repairs: apply 4 rules on text_raw, record insertions with rule name, before/after context (20 chars each side), paragraph number.

Rules:
1. sentence: /([a-z])\.([A-Z])/g → "$1. $2"
2. comma: /([a-z]),([A-Za-z])/g → "$1, $2"
3. quote: /([a-z])“/g → "$1 “"
4. dash: /–([A-Za-z])/g → "– $1"

Careful: sentence rule must not fire after abbreviation? Plan says just apply; fine. But sentence rule applied before comma; note ordering: apply each regex to current text, log insertions with index. Log before/after with 20 chars each side.

To mark repaired places in expanded paragraph, I can record positions. Simpler: after building final text, re-run regexes to find match indices with their rule. Approach: for each rule, use replace with callback capturing index from the current string; but subsequent rules change string. Do sequentially: for each rule, find matches via regex.exec loop on current string, record positions (adjusted), then apply replacement. Since insertions only add one space, I can track positions: easier—rebuild text manually: for each rule, iterate matches, then build new string inserting space at pos+1 (after matched char). Record absolute positions in the new string. Positions from later rules are on already-modified string, fine. Store per-paragraph array of {index (in final text), rule, before, after}.

Implementation:
```js
function applyRepairs(raw){
  let text = raw; const marks = [];
  const rules = [
    {name:'sentence join', re:/([a-z])\.([A-Z])/g, at: m=>m.index+1},
    {name:'comma join', re:/([a-z]),([A-Za-z])/g, at:m=>m.index+1},
    {name:'quote join', re:/([a-z])“/g, at:m=>m.index+1},
    {name:'dash join', re:/–([A-Za-z])/g, at:m=>m.index+1},
  ];
  for(const r of rules){
    let m, out='', last=0;
    while((m=r.re.exec(text))!==null){
      const pos = m.index+1; // insert space after first char
      out += text.slice(last,pos)+' ';
      marks.push({rule:r.name, index: out.length-1, before: text.slice(Math.max(0,pos-20),pos), after: text.slice(pos,pos+21)});
      last = pos;
    }
    out += text.slice(last);
    text = out;
    r.re.lastIndex=0;
  }
  return {text, marks};
}
```
Wait: index stored as position of inserted space in final text — but later rules shift positions. Since later rules append after this point? No — later rules insert spaces anywhere, including before earlier marks. To keep it simple: after computing final text, recompute mark positions by tracking offsets. Alternative: store marks as (rule, before, after) with the matched char, and when rendering expanded paragraph, re-apply: build HTML from text_raw by applying the same replacements with replacement callbacks that wrap inserted space in a span. That's clean:

```js
function renderRepaired(raw){
  // returns html with <span class=fix> </span> inserted
}
```
Use sequential replaces with callback where I know context. E.g. for sentence rule: text.replace(/([a-z])\.([A-Z])/g, (mm,a,b)=>a+'.'+SP+b) where SP = '<span class="fix"> </span>'. But commas etc similar. Since these are plain string ops, use placeholder token like '\u0001' then replace with span in escaped HTML. Do escaping first: escape raw, then apply rules (regex on escaped text — quotes: curly quote not escaped, fine; but &amp; would break [a-z] contexts... risk. Use token approach on raw text, then escape: replace token after? Order: build markedText = raw with '\u0001' tokens inserted (plain text), then escape whole thing, then replace '\u0001' with span HTML. Tokens survive escaping since escaped chars become &...; and token is \u0001 char. Good.

For marks list (before/after contexts): collect during same pass.

Headings: count h2/h3, glued labels count = headings matching /^([IVX]+|[A-Z])\.\s*(.+)$/ where label glued... plan says "how many glued labels were separated" — headings where original text matches /^([IVX]+|[A-Z])\.(?!\s)/ i.e. no space after dot. Count those.

Nothing-lost check: total elements walked = tables + p + h2 + h3; classified: cover table(s), title h2, headings, paragraphs, committee p. Sum equals total; list unclassified.

Committee line: `<p>` after cover that doesn't match paragraph regex. But cover table is first table; committee p is before first h2? Plan: "any other `<p>` is the committee line". So any p not matching paragraph = committee line (there are 97 p, 90 numbered, so 7 committee lines? Plan said 24 h3, 90 numbered p, 97 p in all — 7 other p... maybe committee line + others). I'll classify any non-paragraph p as "other <p> (committee / cover lines)". Just count them as class "other paragraph". Fine for nothing-lost check.

Numbering check: numbers must be exactly 1..n in order; list gaps/duplicates.

First words: reference.first_words keyed by string number; found first 6 words of text (repaired text? plan says of `text` — yes, `text`). Normalize both.

Export JSON: array of records with fields as listed. Export round-trip: JSON.parse(JSON.stringify(records)) length equals table count — trivially same but do JSON.parse of the generated string.

Markdown: front matter, then headings in document order as ## / ###, paragraphs as "**n.** text"? Plan: "each paragraph as its number in bold, then its text". So `**12.** text`.

Headings in document order: I need to keep ordered list of blocks. Keep `order` array of {type:'h2'|'h3', label, heading, num} and paragraphs.

Section: nearest heading above; part: nearest roman h2. Store heading path for expanded display: part label+heading › section label+heading.

Rail: symbol, short title (title? plan says short title — use title maybe trimmed; html_doc has `title`). I'll show title.

Header status: green dot "n of m checks pass" or red if failures. Checks: count, numbering, first words, footnotes (source limit — counted apart), repairs, headings, nothing lost, round trip. m = total checks; pass = passing; footnotes shown as source limit. If any fail → red dot "n checks failed"? Plan: "green dot 'n of m checks pass' or a red dot 'n checks failed'". Compute: failures = failed checks; if failures>0 red dot with "n checks failed"; else green "n of m checks pass" where m excludes... I'll say passes of m where m counts all run checks. Keep simple: m = number of run checks (excluding source-limit?), pass count. Show both.

"1 source limit" note at right of header.

Tabs: 01 RESULT, 02 PARAGRAPHS. Arrow key nav, hidden panels `hidden` attr with CSS override.

Tab 01 tiles: 4 tiles with big numbers. Under tiles mismatch list (max 10 lines). Then "Take the paragraphs away": two buttons. Then two closed headings: "Every check (m)" and "The spaces restored (n)" — panel with table Paragraph|Before|After|Rule plus counts per rule; clicking a row opens paragraph on tab 02 (switch tab and expand row). Then a note line.

Click count on tab 01: 4 tiles? tiles aren't clickable. Buttons: 2 download + 2 closed headings = 4. Fine.

Tab 02: "Headings found: n" closed box listing them; table rows expandable; copy citation button.

Copy: navigator.clipboard may not exist in sandbox; fallback textarea execCommand. Show "Copied" for 2s.

Let me now write the whole HTML. Aim ~700 lines.

Structure:

```html
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>...</title><style>...</style></head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<main>
 <aside id="rail">...</aside>
 <section id="panel1" role="tabpanel">...</section>
 <section id="panel2" role="tabpanel" hidden>...</section>
</main>
<footer>...</footer>
<script>...</script>
</body></html>
```

Rail always visible — place it in a grid with main content, both under tabs? Plan says left rail always visible, header always visible, tabs under header. I'll do: header full width; then a grid: rail left column spanning both tabs, tab content right. Tabs nav above content but rail left... Simplest: grid with rail as first column full height, right column contains tablist + panels.

CSS per studio: colors, fonts, focus ring.

Now details of check panel lines: each check: name, what compared, two values, status word pass/failed/source limit; failed links to rows (switch to tab 02 and scroll to paragraph? For first-words failures link to rows). For simplicity, link only for first words check → goes to tab 02 and expands first mismatched paragraph.

Numbering check values: expected "1–n in order", found sequence.

Repairs check: pass if repairs logged correctly (they're deterministic — check that text differs from raw only by inserted single spaces: verify text.length - raw.length === number of insertions and that removing one space... do simple check: text.length - text_raw.length === marks count).

Headings check: counts found.

Nothing lost: sum of class counts === total elements; else fail listing unclassified.

Round trip: parse exported JSON string, record count equals paragraphs length.

Footnotes check: "source limit".

Reference missing handling: if no reference or fields missing, tiles say "no reference in this file", relevant checks "not run".

If no paragraphs: tab 01 message, exports disabled.

Write it.

First words found: `text.split(/\s+/).slice(0,6).join(' ')`, normalized.

Normalization function:
```js
const norm = s => s.replace(/[\u201C\u201D]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2011]/g,'-').replace(/\u00A0/g,' ');
```

Markdown export: headings in doc order. Build from ordered blocks list.

JSON download:
```js
function download(name, content, type){ const b=new Blob([content],{type}); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(u),1000); }
```

Filename: symbol.replace(/\//g,'-').

Now expanded row content: full text verbatim (with marked repairs in red box), reference six words vs found six, missing-space places (the marks list), Copy citation button.

Section column: nearest heading text (heading without label? plan: "Right to work (art. 6)" — the heading text after label). Show `heading` text; expanded shows full path "IV. … › Right to work (art. 6)".

Copy citation: "E/C.12/GC/27, para. 12".

Go write.

Tab arrows: keydown on tablist, ArrowLeft/Right.

"Open paragraph on tab 02" from spaces table: function openPara(n): switch tab, expand row, scrollIntoView.

Also heading glued count: headings where /^([IVX]+|[A-Z])\.(?!\s)/ matched original.

Let me write final code now. I'll be careful with quotes in strings (curly quote “ in regex — fine in UTF-8 file).

Committee line: classify p non-matching as 'other'. For nothing-lost, classes: cover table, title, headings, paragraphs, other p, other tables. All elements must be classified: every table → cover (first) or "other table"; every h2 → title (first h2 after cover) or heading; h3 → heading; p → paragraph or other. So everything classified by definition; still compute and display. To make the check real: count each class and sum vs total elements — always passes by construction, but that's the "nothing lost" audit. OK.

Edge: paragraph regex /s flag for multiline — use /^(\d{1,2,3}).../ careful: (\d{1,3}). text of p: use el.textContent.

Heading label regex: /^([IVX]+|[A-Z])\.\s*(.+)$/ — plan's split regex; glued check separately: original matches /^([IVX]+|[A-Z])\.(?!\s)/.

Time to write. Estimate ~650 lines. Go.