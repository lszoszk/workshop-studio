Build a full HTML app per the plan. Two tabs, left rail, header, footer. Need to implement the pipeline carefully. Keep under ~1500 lines.

Let me write the code.

Key data: WORKSHOP_DATA.pdf_text with records, reference, title, symbol, doc_url, source, built, count.

Pipeline:
1. Sort records by page.
2. For each page: split text into lines. Header: first non-empty line === symbol → drop. Footer: from end, drop while empty / GE. / 6-digit groups / bare number 1-3 digits (page number if equal page, else count as displaced footnote number).
3. Concatenate body lines with page tags.
4. Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.
5. Headings: labelled /^([IVX]+|[A-Z])\.$/ — skip blanks, collect heading lines until next label or paragraph start; lowercase or "(" starts continue. Unlabelled: non-empty line immediately followed by a paragraph-start line, ≤90 chars, starts capital, not ending . ; : , digit. Two-line merge when previous line passes the same test and doesn't end paragraph sentence.
6. Paragraph lines otherwise; suspect lines: bare number no full stop; starts digits+space+capital or quote; starts "* ". Suspect propagates to end of page. Paragraph >300 words flagged.
7. First words: strip footnote marks, take six words, compare normalised.
8. Checks: counts, numbering 1..n, first words, pages flagged, suspect lines, headers/footers, headings, nothing lost, export round trip.

Nothing lost classification: I need to classify every non-empty line of every page exactly once. I'll classify during processing: header lines, footer lines, cover lines (before first paragraph start and not heading), heading lines, paragraph lines. Count total non-empty lines from raw pages and compare sum. Since I drop blank lines only when concatenating, classification should cover all non-empty lines. Header line dropped; footer lines dropped. Cover: lines before first paragraph start that aren't headings. But unlabelled heading detection: line followed by paragraph start... cover lines before first paragraph start — the first paragraph start is paragraph 1; lines before that which aren't headings are cover. Wait, unlabelled heading before para 1? There might be. Handle: for lines before first paragraph start, treat as cover unless it's a labelled heading (or an unlabelled heading immediately followed by a paragraph start — e.g., "I. Introduction"? that's labelled). Simplify: cover = non-heading lines before first paragraph start.

Actually the plan: "Lines before the first paragraph start are the cover." So cover regardless of heading-ness? But labelled headings before first paragraph... e.g. "I." + "Introduction" before para 1 — those lines would be classified as cover lines. That's fine for "nothing lost" (classified once). I'll classify: before first paragraph start → cover (and drop them from heading detection too? The plan says lines before first paragraph start are cover). But then part/section for para 1... Section "Introduction" would be cover. Hmm. Simpler: still run heading detection over the whole body, but classify lines before first paragraph start as cover. Actually let heading detection run; a labelled heading before para 1 still sets current heading. Classify line kinds: I'll track each body line's kind (heading/paragraph/cover) and count. Total = header + footer + cover + heading + paragraph.

Careful with two-line unlabelled heading merge: when line L is followed by paragraph-start line and passes test, and line L-1 also passes test and doesn't end a sentence, both are heading lines. But L-1 might already be classified as paragraph text. I'll do a two-pass: first identify heading line indices, then assign paragraph lines.

Implementation plan:

```
pages = records sorted by page.
For each page: lines = text.split('\n').
  // header
  find first non-empty index; if === symbol → header line, remove.
  // footer: iterate from end
  i = lines.length-1
  while i>=0:
    l = lines[i].trim()
    if empty → mark footer-blank? No — blank lines are just skipped in classification ("every non-empty line classified"). I'll remove footer lines (including empties at end) but only count non-empty ones as footer.
    if l==='' → footerDrop, i--
    else if /^GE\./ → footer, i--
    else if /^(\d{6})( \d{6})*$/ → footer (date stamp)
    else if /^\d{1,3}$/ → footer; if === page → page number else displaced footnote number
    else break
  body = lines.slice(0, i+1) with empties kept.
```

Concatenate body lines across pages, tagged with page. Keep an array `bodyLines` of {text, page, raw}. 

Then paragraph starts detection over bodyLines (using trimmed text? Use raw trimmed). Build flags.

Heading detection: iterate bodyLines with index.
- labelled: trimmed matches /^([IVX]+|[A-Z])\.$/. Then collect following lines (skipping blanks) until next label or paragraph start; those are heading text lines. Also a heading text line that starts lowercase or "(" continues — that's automatic since I collect all lines up to boundary. Plan says "a line starting with a lowercase letter or '(' continues the previous heading line" — but my collection takes all lines until boundary anyway. OK.
- unlabelled: non-empty line at index i, trimmed, where bodyLines[i+1] (skipping blanks? plan says "immediately followed") — take next non-empty? Plan says "immediately followed by a paragraph-start line". Use next non-empty line being a paragraph start (skip blanks to be safe? keep immediate non-blank check: find next non-empty; if it's a paragraph start). Tests: length ≤90, /^[A-Z(]/, not ending in /[.;:,0-9]$. Hmm "starting with a capital letter" — I'll allow "(". Also previous line same test + not ending sentence (not ending . ? "does not end a paragraph sentence" — I'll interpret: doesn't end with '.', ';', ':' or the next line... keep simple: previous line passes heading tests and doesn't end with '.').

But careful: a labelled heading's last line could be immediately followed by a paragraph start and pass the unlabelled test — then it would be counted as unlabelled too. E.g., "I." "Introduction" then "1." — "Introduction" is already a labelled heading line; must not double-classify. So skip unlabelled detection for lines already marked as heading (labelled) lines. Also cover lines: heading detection runs from start; lines before first paragraph start — plan says they're cover. But there could be a real heading before para 1 (e.g. "I. Introduction"). Hmm. The doc: page 1 has cover stuff, then "I." "Introduction" then "1.". If those are "cover", then para 1's section is unknown. I'd rather let labelled headings count as headings even before para 1, and mark remaining pre-para-1 lines as cover. The "nothing lost" check just needs classification; plan says "Lines before the first paragraph start are the cover" — but also headings found before... I'll do: labelled and unlabelled headings are headings wherever they appear; other pre-para1 lines are cover. That keeps classification complete and better sections. The check panel will list counts.

Wait — but cover lines like "United Nations", "Committee on Economic..." — the title line "General comment No. 27..." might pass unlabelled heading test (≤90 chars? it's long, ~110 chars, so no). "Introduction" before para 1: it's part of labelled heading. OK.

Actually risk: cover lines like "6 November 2025" end with digits → not heading. "Original: English" ends with letter but starts "O" — followed by "Committee..." not a paragraph start. Fine.

Paragraphs: from each paragraph start, collect subsequent lines (excluding heading lines and the next paragraph start) until next paragraph start or heading. Blank lines dropped. text = join single space, collapse doubles, trim. Hyphen-ending lines counted. page_start/page_end.

Suspect lines: for each line inside a paragraph: trimmed matches /^\d{1,3}$/ (bare number no dot), or /^(\d{1,3}) [A-Z“"]/ (digits space capital or quote) — plan says "one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". UN doc symbols start with letter+slash, e.g. "E/2003/22" — that's "digits, space, capital" covers "7 E/2003/22" (7 space E...). So regex /^\d{1,3} [A-Z“"'E]/ — capital letter or quote. Or /^\* /. When a line is suspect, all lines after it on the same page (within that paragraph or continuing pages? "every line after it to the end of its page") are suspect. So compute per-line suspect status globally: mark suspect line, then subsequent bodyLines with same page also suspect.

Flag paragraph if any of its lines suspect, or >300 words.

Page flagged if any suspect line in a paragraph on that page.

First words: text tokens; process tokens: remove digits glued to end of a word or punctuation: replace /\d+$/ at token end... "waste.2" → "waste." — token "waste.2": strip trailing digits if preceded by non-digit? Careful with "17" real numbers. Rule: if token ends with digits and the part before is non-empty and non-digit → cut digits. A token of digits alone: drop only when previous kept token ends with '.', ',', or closing quote and isn't "No." or "art.". Take first six tokens after processing.

Compare with reference.first_words[String(n)]: normalise both (curly→straight quotes, en/em dashes→hyphen, whitespace runs→single).

Citation: `${symbol}, para. ${n}`.

Exports: JSON array with fields listed. Markdown with front matter, headings as ##/### in document order (labelled roman = ##, lettered = ###, unlabelled = ###? plan says "the headings as ## and ### lines in document order"). I'll do roman → ##, others → ###. Paragraphs: "**n.** text" plus flagged note.

File names: symbol replace / with -. Blob URLs.

Checks list (m checks):
1. Paragraph count: found vs reference.paragraphs.
2. Numbering: exactly 1..n in order.
3. First words: mismatches count.
4. Pages flagged: n pages, n paragraphs (not pass/fail — show as info).
5. Suspect lines: counts.
6. Headers/footers: pages with symbol first line, pages with page number, bare numbers removed.
7. Headings: labelled/unlabelled counts, unlabelled listed.
8. Nothing lost: classification sums.
9. Export round trip: JSON.parse round trip count.

If reference missing: tiles show "no reference in this file", checks "not run".

Tab 02: table rows expandable. Columns: No | Section | Page | First line | Check. Closed "Headings found: n" box listing them. Expanded: full text with suspect lines marked (thin red box around those line segments — since text is joined, I'll render paragraph as running text but wrap suspect lines' content in <span class="suspect">). Reference six words vs found six. "Show the PDF's lines" toggle: shows text_lines with page markers where page changes. Copy citation button.

Header right: green dot "n of m checks pass" or red "n checks failed", "n pages flagged".

Design: #f4f0e8 background, #1d1b18 text, #d9d2c3 rules, #9b2335 accent, green #1e6b34 for pass.

Tablist with arrow keys. role=tab, aria-selected, panels hidden attribute with [hidden]{display:none!important}.

Max 7 clickable things per view: tab01 has: 2 tabs + 2 download buttons + 2 collapsible headings = ~6. Tab02: 2 tabs + headings box + rows. Fine.

Let me now write the code. I'll be careful with size.

Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>...</title>
<style>...</style>
</head>
<body>
<header>...</header>
<nav role="tablist">...</nav>
<main>
  <aside>rail</aside>
  <section panels>
</main>
<footer>...</footer>
<script>...</script>
</body>
</html>
```

Layout: rail on left of content area, always visible both tabs.

Let me draft the JS pipeline.

```js
const D = WORKSHOP_DATA.pdf_text;
const pages = [...D.records].sort((a,b)=>a.page-b.page);
const ref = D.reference || null;
const symbol = D.symbol, title=D.title, doc_url=D.doc_url||'', source=D.source||'';

let headerPages=0, pageNoPages=0, bareRemoved=[], warnings=[];
let allLines=[]; // {text, page, kind}
let classifiedNonEmpty = {header:0, footer:0, cover:0, heading:0, paragraph:0};

pages.forEach(p=>{
  const raw = (p.text||'').split('\n');
  // header
  let start=0;
  // find first non-empty
  let fi = raw.findIndex(l=>l.trim()!=='');
  if(fi>=0 && raw[fi].trim()===symbol){ headerPages++; start=fi+1; }
  else warnings.push('Page '+p.page+': first non-empty line is not the symbol');
  // footer
  let end = raw.length-1;
  let footerNonEmpty=0;
  while(end>=start){
    const t=raw[end].trim();
    if(t===''){ end--; continue; }
    if(/^GE\./.test(t)){ footerNonEmpty++; end--; continue; }
    if(/^\d{6}( \d{6})*$/.test(t)){ footerNonEmpty++; end--; continue; }
    if(/^\d{1,3}$/.test(t)){ footerNonEmpty++; if(+t===p.page) pageNoPages++; else bareRemoved.push({page:p.page,line:t}); end--; continue; }
    break;
  }
  classifiedNonEmpty.header += (fi>=0 && raw[fi].trim()===symbol)?1:0;
  classifiedNonEmpty.footer += footerNonEmpty;
  for(let i=start;i<=end;i++){
    const t=raw[i].trim();
    if(t==='') continue;
    allLines.push({text:t, page:p.page});
  }
});
```

Wait — "nothing lost" counts non-empty lines total. Total non-empty = header + footer + body non-empty. Body lines go through classification: heading/cover/paragraph. I'll compute totalNonEmpty from raw pages.

Paragraph starts:
```js
const paraStartRe1=/^(\d{1,3})\.$/;
const paraStartRe2=/^(\d{1,3})\. (.+)$/;
function paraStart(line){ let m=line.match(paraStartRe1); if(m) return {n:+m[1], first:null}; m=line.match(paraStartRe2); if(m) return {n:+m[1], first:m[2]}; return null; }
```

Hmm, paraStartRe2 could match things like "1. Introduction"? No headings like that. But footer lines already removed. Also year lines "2025." unlikely. Fine. But careful: a footnote line like "1 See A/..." — starts "1 " no dot. Not matched. A line "12. See..." inside footnotes could be a paragraph start false positive? Footnote text lines: first footnote is "bare number on its own line, a blank line, then the text". So footnote body doesn't start with number. Others start "7 E/2003/22…" — no dot after number. Good.

But wait — the reference has 90 paragraphs and the doc found 90 per the plan's exploration, so the regexes are fine.

Heading detection. Build array of body line indices. I'll iterate and mark:

```js
const N=allLines.length;
const isParaStart = new Array(N).fill(false);
const psInfo = new Array(N).fill(null);
allLines.forEach((l,i)=>{ const m=paraStart(l.text); if(m){isParaStart[i]=true; psInfo[i]=m;} });
const firstPS = isParaStart.indexOf(true);

const isHeading = new Array(N).fill(false);
let headings=[]; // {text, page, kind:'roman'|'letter'|'unlabelled'}
const labelRe=/^([IVX]+|[A-Z])\.$/;
// labelled headings
for(let i=0;i<N;i++){
  if(labelRe.test(allLines[i].text)){
    const label=allLines[i].text;
    // gather following lines until next label line or paragraph start
    let j=i+1, parts=[label];
    while(j<N && !isParaStart[j] && !labelRe.test(allLines[j].text)){
      if(allLines[j].text!=='') parts.push(allLines[j].text);
      j++;
    }
    const kind=/^[IVX]+\.$/.test(label)?'roman':'letter';
    headings.push({text:parts.join(' '), page:allLines[i].page, kind});
    for(let k=i;k<j;k++) if(allLines[k].text!=='') isHeading[k]=true;
    i=j-1;
  }
}
```

Wait: labelled heading gathering skips until next label or paragraph start — but an unlabelled heading before a paragraph start within the section would be swallowed into the labelled heading text. E.g., "A." then subsection lines, then unlabelled "Children" then "43." — "Children" would join the labelled heading. Hmm. Actually plan: "then every line up to the next label line or paragraph start is heading text" — so yes, that's per plan. But then the unlabelled "Children" is heading text of the lettered heading? That would make section "A. ... Children" for para after. Plan says section = nearest heading. The unlabelled detection: "a non-empty line immediately followed by a paragraph-start line" — if it's already inside a labelled heading block, it's heading anyway. Its text merges into the labelled heading. Hmm, that could produce combined headings like "A. ... Children". The plan's exploration says 20 unlabelled headings found, so presumably they occur and aren't all inside labelled blocks... Actually maybe they are standalone (not after a label without intervening paragraph). Like after paragraph text, a heading, then next paragraph. In that case label gathering doesn't reach them because there's paragraph start between? No — label gathering runs from the label line to the next label or paragraph start. If a section is "A. Heading" then para 20..23, then unlabelled "Children", then para 24 — the labelled gathering from "A." stops at para 20's start. "Children" comes after paragraphs, followed by para start → unlabelled. Good.

Edge: unlabelled heading immediately after labelled heading with no paragraph between (label gathering swallows it). Per plan, fine.

Unlabelled detection (only lines not already heading, and index >= firstPS? cover lines... let me allow anywhere but they need to be followed by paragraph start):

```js
function headingTest(t){ return t && t.length<=90 && /^[A-Z(]/.test(t) && !/[.;:,0-9]$/.test(t); }
for(let i=0;i<N;i++){
  if(isHeading[i]||isParaStart[i]||allLines[i].text==='') continue;
  // find next non-empty
  let j=i+1; while(j<N&&allLines[j].text==='')j++;
  if(j<N && isParaStart[j]){
    // check not part of labelled heading block — isHeading[j] false, ok
    let texts=[allLines[i].text], idx=[i];
    // previous line merge
    let k=i-1; while(k>=0&&allLines[k].text==='')k--;
    if(k>=0 && !isHeading[k] && !isParaStart[k] && headingTest(allLines[k].text) && !/[.;:!?]$/.test(allLines[k].text)){
      texts.unshift(allLines[k].text); idx.unshift(k);
    }
    headings.push({text:texts.join(' '), page:allLines[idx[0]].page, kind:'unlabelled'});
    idx.forEach(x=>isHeading[x]=true);
  }
}
```

But previous line merge: previous line already used as part of a previous unlabelled heading? No, headings are followed by paragraph starts so each heading immediately precedes a paragraph start; distinct. But previous line might be the last line of the previous paragraph's text that happens to pass — that's why "does not end a paragraph sentence" check (not ending '.', ';'...). Plan says "does not end a paragraph sentence" — I use not ending [.;:!?]. Hmm but a heading line itself doesn't end with those. OK.

Wait — order matters: labelled headings collected first, marking isHeading. Then unlabelled. But headings order in document: I should sort headings by their first line index for "document order" in exports and section assignment. I'll store index.

Also: cover. Lines before firstPS not heading → cover. Also lines before firstPS that match labelRe — they're labelled headings (e.g. "I." "Introduction" before para 1). Per plan "Lines before the first paragraph start are the cover" but classifying them as headings is more useful; check panel just reports counts. Hmm, risk: cover contains "I." line? Page 1: "Committee on Economic, Social and Cultural Rights", title, "I." , "Introduction", "1." — yes, "I." appears before para 1. If I treat it as heading, para 1's part = "I. Introduction". Good. I'll classify as heading. The check "Nothing lost" counts all non-empty lines as one of cover/header/heading/paragraph/footer. Fine.

But also: could cover lines pass unlabelled heading test and be followed by paragraph start? E.g., "Introduction" line (if "I." weren't matched)... "I." matches labelRe so labelled path. The title line before "I." is long >90. OK.

Paragraphs:
```js
let paragraphs=[]; let current=null; let headingOrder = headings sorted by index;
```
Actually I need headings with index. Let me store {idx, text, page, kind} and sort by idx.

Iterate lines 0..N-1:
- if isParaStart[i]: close current; start new para {n, lines:[first? ]}; push first line if psInfo.first.
- else if isHeading[i]: close current? A heading between paragraphs — paragraph already closed at next start... but a heading could come while current is open only if... a paragraph ends and heading then next para start. When we hit a heading line, close current (set current=null). Headings are never paragraph text.
- else: if before firstPS → cover; else if current → append; else orphan (shouldn't happen; classify as cover? count separately). Blank lines skipped earlier — wait I skipped empty lines when building allLines. Good, allLines has only non-empty lines.

Hmm but "every line after suspect to end of page is suspect" — with blank lines removed that's fine, I check page field.

Paragraph text: lines joined ' ', collapse /\s{2,}/, trim. Actually joining with ' ' and lines already trimmed → just join(' ').

Hyphen-ending count: lines ending with '-'.

Suspect: 
```js
function suspectTest(t){
  if(/^\d{1,3}$/.test(t)) return 'bare number';
  if(/^\d{1,3} [A-Z“"]/.test(t)) return 'starts with a number and a space';
  if(/^\* /.test(t)) return 'starts with an asterisk';
  return null;
}
```
Wait "* Adopted by the Committee…" — is that in a paragraph or cover? Page 1 cover has "* Adopted..." note? The plan says the note on the first page. It's a suspect line type; if it's in cover it won't be in a paragraph. Actually in this PDF, the asterisk note "* Adopted by the Committee at its..." might be on page 1 near end of document? GC27's adoption note is typically on first page. If it's before para 1, it's cover and not in any paragraph — then no paragraph flags from it. Hmm, but the plan lists it as suspect line type, so presumably it appears inside a paragraph region (end of page 1, footnotes area, within paragraph 1's page range but before... no). Actually footnote lines at foot of page 1 include the asterisk note. Paragraph 1 spans pages... lines after paragraph content on page 1 are footnotes of page 1 — they'd be inside "current paragraph" (para 1 or 2). So the asterisk line would be in paragraph text. OK, my global approach handles it: suspect computed on all lines with page propagation, then flagged per paragraph.

Suspect propagation: compute suspect flags per line:
```js
const suspect=new Array(N).fill(false); const suspectWhy={};
for(let i=0;i<N;i++){
  const w=suspectTest(allLines[i].text);
  if(w){ suspect[i]=true; suspectWhy[i]=w;
    for(let j=i+1;j<N&&allLines[j].page===allLines[i].page;j++) suspect[j]=true;
  }
}
```

Paragraph flagged: any of its lines suspect, or word count >300. Suspect reason for flagged pages table: I need "Suspect lines" — list the line texts and why. I'll collect per paragraph: suspect entries {line, why, page}. For propagated lines why = 'after a suspect line on this page'? The flagged pages table wants "Suspect lines | Why ('starts with a number and a space', 'bare number', 'paragraph over 300 words')". So per flagged page, show triggering lines with reasons. I'll record trigger lines (those with explicit why) and also the >300 reason.

Pages flagged: page has a suspect line inside a paragraph. I'll compute: for each paragraph, for each line flagged suspect that belongs to the paragraph, mark page. Note propagated lines in paragraphs count.

First words:
```js
function firstWords(text){
  let toks=text.split(/\s+/);
  let out=[];
  for(let t of toks){
    // glued digits
    let m=t.match(/^(.*?[^\d\s])\d+$/); // ends with digits, prefix non-digit... 
```
Hmm "waste.2": strip trailing digits when preceded by non-digit: t=t.replace(/(?<=\D)\d+$/,'') — lookbehind ok in modern browsers. Safer: match /^(.+?\D)(\d+)$/ → t = m[1]. E.g. "waste.2" → "waste.". "2" alone → no match (prefix must be non-digit and non-empty). 
    if(/^\d+$/.test(t)){
      const prev=out[out.length-1];
      if(prev && /[.,’”"]$/.test(prev) && !/\bNo\.$|art\.$/.test(prev)) continue; // drop
      // keep
    }
    out.push(t); if(out.length===6) break;
  }
  return out.join(' ');
}
```
Wait the plan: "a token of digits alone is dropped only when the token before it ends with a full stop, comma or closing quote and is not an abbreviation such as 'No.' or 'art.'". Good.

Also glued digits: "digits glued to the end of a word or a punctuation mark are cut". Applies to first six words anyway.

normalise: s.replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').

Checks and m count: I'll define checks array with {name, expected, found, pass|info|notrun, detail}. m = total checks (say 9). Passes counted.

Tiles:
- Paragraphs found n vs ref.paragraphs.
- First words match n of ref.paragraphs.
- Pages flagged n of pages, red when >0.
- Footnotes: "not separated", ref.footnotes count.

Mismatches listed: "para. n: found … / reference …" max 10 then "and n more".

Flagged pages panel rows: Page | Paragraph | Suspect lines | Why. Click row → show page's raw lines with suspect highlighted and the paragraph. I'll render below the row (expandable). Raw lines of the page: I need to keep raw page lines for display. Store per page rawLines (post header/footer removal? "the page's raw lines" — I'll show body lines with page context; simplest: store original split lines per page, and highlight those that are suspect in paragraphs... but mapping raw→body lines: header/footer dropped. I'll show body lines (the ones kept) — that's the page's raw lines minus header/footer; plus mention header/footer dropped. Simpler: keep per-page array of {text, suspect:boolean|null, kind}. I'll build a display structure: for each page, list of lines with class if suspect. Let me store during classification: for each line index i, kind. Then pageLines = allLines.filter(l=>l.page===p) with suspect flags and paragraph association.

Clicking a flagged-page row: expand to show lines with suspect highlighted, and "sits in: para. n".

Tab 02: table with rows. Expand: full text (running, suspect segments marked), reference vs found first words, toggle "Show the PDF's lines", copy citation button.

Copy: navigator.clipboard may fail in sandbox; fallback textarea+execCommand. Show "Copied".

Exports disabled if no paragraphs.

Round-trip check: JSON.parse(JSON.stringify(exportRecords)) length equals paragraphs.length.

Now UI counts of clicks: Tab01: 2 tabs, 2 download buttons, 2 disclosure buttons = 6. Tab02: 2 tabs, 1 headings disclosure, rows (rows don't count). OK.

Tabs arrow-key navigation.

Rail: "DOCUMENT" card with symbol + short title (use title, maybe truncated — "short title": D.title; I'll use title). Big numbers: paragraphs n of ref with thin bar; pages flagged n; checks n of m.

Header right: dot + text, then "n pages flagged".

Footer: source, built, honesty line.

Let me also handle ref missing fields: paragraphs, footnotes, adopted, first_words. If missing: tile shows "no reference in this file".

Note "count is the string '20'": use pages.length.

Now write the whole file. Aim ~900-1100 lines.

Also "How this is computed" line near every chart or number — tiles have them; rail numbers maybe one line.

Design details: tabs numbered monospace "01 RESULT · 02 PARAGRAPHS". Accent red for active tab underline/text.

Let me write it.

CSS: 
```css
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
header.site{padding:20px 28px 14px;border-bottom:1px solid #d9d2c3;display:flex;justify-content:space-between;gap:16px;align-items:flex-start}
...
```

Layout main: display:flex; aside rail width 230px; content flex:1.

Tabs bar: buttons role=tab.

I'll write JS to render everything.

Big numbers: .big{font-family:Georgia;font-size:44px}

Flagged pages table: use a div-based list of expandable rows (buttons) rather than table-in-table. Plan says "One row per flagged page: Page | Paragraph | Suspect lines | Why" then clicking shows lines. I'll make each a <button class="fp-row"> grid with columns, then a hidden div after it.

Tab 02 table: real <table> with caption, and rows expandable — a tr with a hidden following tr for details. Rows as buttons: plan says "Rows are buttons with aria-expanded". Inside a table, use <tr> with tabindex=0 role=button? Simpler: put a <button> in the first cell? Plan: rows are buttons with aria-expanded; click or Enter expands. I'll make the main row a <tr tabindex="0" role="button" aria-expanded> with keydown Enter/Space. That's acceptable.

Copy citation: button in expanded detail.

Downloads: 
```js
function download(name, content, type){ const b=new Blob([content],{type}); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(u),5000); }
```

JSON records fields: symbol, paragraph, section, part, page_start, page_end, text, text_lines (plan mentions export field text_lines lines separated " | "), flagged, first_words_match, citation, doc_url, limitations.

Markdown: front matter:
```
---
title: ...
symbol: ...
adopted: ...
source_url: ...
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: n
pages_flagged: n
footnotes: "not separated; the document has 141"
---
```
Then headings in document order: roman "## ", others "### ". Paragraphs: "**1.** text" and "(flagged: may contain footnote text)".

Headings document order with paragraph interleaving: iterate through body lines again in order, emitting headings and paragraphs by index. I'll sort headings by idx and paragraphs by startIdx, merge.

Check panel: list of checks with details, pass green / fail red / info.

"Headers and footers" check line includes bare numbers list.

"Headings" check lists unlabelled headings.

"Nothing lost": total non-empty lines vs sum; list unclassified (none expected — but if a body line isn't heading/paragraph/cover, list in red; I classify orphans as 'other' and list).

Let me now count non-empty total from raw page text: sum over pages of lines with trim !== ''.

Classification per body line: kind = 'heading' | 'paragraph' | 'cover' | 'other'. Header lines counted when dropped; footer lines counted. Sum check.

Now build the code.

For first words comparison display: found six vs reference six — reference.first_words values are already six words presumably.

Numbering check: expected sequence 1..found.length? Check paragraphs[i].n === i+1; gaps/duplicates listed.

Suspect line stats: count trigger lines and affected lines. I'll count lines with explicit why (triggers) and total suspect lines in paragraphs.

Flagged pages data: map page → {paras:set, triggers:[{line,why,para}]}.

Let me carefully produce flagged-pages table: "Suspect lines" column shows the suspect line text (truncated), "Why" shows reason. Trigger lines only, plus "paragraph over 300 words" reason when applicable.

Expansion shows page's body lines with suspect ones highlighted and which paragraph each sits in ("sits in para. n" or "not in a paragraph"). I'll precompute per line its paragraph number.

OK. Also expanded paragraph on tab 02: render running text; mark suspect lines: since text joins lines with spaces, I'll render as sequence of spans per line: each line a span; suspect lines get class .sus (thin red box). Joined visually with spaces. That preserves running text appearance while marking. Good — same for flagged page detail.

"Show the PDF's lines" toggle: show text_lines with line breaks, and mark where a new page begins: when line.page changes from previous, prefix "— p. X —" marker.

Also first line of para with psInfo.first: the "first" text is line 1 of paragraph.

Now, cover lines: cover before first paragraph start. But headings before first paragraph start (like "I." "Introduction") are headings. Cover lines classified cover.

Also lines after last paragraph but headings? Fine.

Now the header right dot: checksPass / checksTotal; if failures>0 red "n checks failed" else green "n of m checks pass". Checks that are "info" (pages flagged, suspect lines) — are they pass/fail? Plan: "A flag is not a failure: ... this line reads 'n pages flagged...'". I'll treat checks as pass/fail/not-run/info. m = number of checks; pass count excludes info? "n of m checks pass" — I'll count pass among all m; info counts as pass (nothing failed)? Hmm. Let me define: each check has status pass/fail/info/notrun. Header shows passCount + infoCount? Simpler: header shows "n of m checks pass" where n = pass + info (i.e., not failed, not notrun)? That inflates. Let me make: m checks total; failures = count fail; if failures>0 → red "n checks failed"; else green "n of m checks pass" where n = m - notrun count. Info checks count as passing (they ran and nothing failed). That reads fine.

Edge: "Export round trip" — runs always (if paragraphs exist).

If no paragraphs: tab 01 says so, exports disabled.

Let me write the final HTML now. I'll keep it organized and reasonably compact.

Section/part for paragraphs: current nearest heading (any kind) = section; nearest roman = part. Track during iteration.

Let me write.

Also `built` for footer: D.built.

Write code:

```js
(function(){
const D=window.WORKSHOP_DATA.pdf_text||{};
const symbol=D.symbol||''; const title=D.title||''; const doc_url=D.doc_url||'';
const source=D.source||''; const ref=D.reference||null;
const pages=(D.records||[]).slice().sort((a,b)=>a.page-b.page).map(r=>({page:r.page,lines:(r.text||'').split('\n')}));

// --- pipeline
const labelRe=//^([IVX]+|[A-Z])\.$/;
...
```

Classification loop detail:

```js
let totalNonEmpty=0;
pages.forEach(p=>p.lines.forEach(l=>{if(l.trim()!=='')totalNonEmpty++;}));

let cntHeader=0,cntFooter=0;
const bareRemoved=[]; const headerMiss=[];
const body=[]; // {text,page}
pages.forEach(p=>{
  let s=0;
  let fi=p.lines.findIndex(l=>l.trim()!=='');
  if(fi>=0&&p.lines[fi].trim()===symbol){cntHeader++;s=fi+1;}
  else headerMiss.push(p.page);
  let e=p.lines.length-1;
  while(e>=s){
    const t=p.lines[e].trim();
    if(t===''){e--;continue;}
    if(/^GE\./.test(t)||/^\d{6}( \d{6})*$/.test(t)||/^\d{1,3}$/.test(t)){
      cntFooter++;
      if(/^\d{1,3}$/.test(t)){ if(+t!==p.page) bareRemoved.push({page:p.page,line:t}); }
      e--;continue;
    }
    break;
  }
  for(let i=s;i<=e;i++){const t=p.lines[i].trim(); if(t!=='') body.push({text:t,page:p.page});}
});
```

Note: header line removed also when fi is 0 and equals symbol. But what if the first non-empty line equals symbol but there are blank lines before? fine.

Edge: if header missing, the symbol line stays in body → could be misclassified; headerMiss records it.

Then:
```js
const N=body.length;
const psOf=body.map(l=>{const m1=l.text.match(/^(\d{1,3})\.$/); if(m1)return{n:+m1[1],first:null}; const m2=l.text.match(/^(\d{1,3})\. (.+)$/); if(m2)return{n:+m2[1],first:m2[2]}; return null;});
const firstPS=psOf.findIndex(x=>x);
```

Headings:
```js
const isHead=new Array(N).fill(false);
const headings=[]; // {idx,text,page,kind}
for(let i=0;i<N;i++){
  if(labelRe.test(body[i].text)){
    const j0=i; let j=i+1; const parts=[body[i].text];
    while(j<N&&!psOf[j]&&!labelRe.test(body[j].text)){parts.push(body[j].text);j++;}
    const kind=/^[IVX]+\.$/.test(body[i].text)?'roman':'letter';
    headings.push({idx:j0,text:parts.join(' '),page:body[i].page,kind});
    for(let k=j0;k<j;k++)isHead[k]=true;
    i=j-1;
  }
}
function headTest(t){return t.length<=90&&/^[A-Z(]/.test(t)&&!/[.;:,0-9]$/.test(t);}
for(let i=0;i<N;i++){
  if(isHead[i]||psOf[i])continue;
  let j=i+1;while(j<N&&false){} // next non-empty always exists since body has no empties
  if(i+1<N&&psOf[i+1]){
    let texts=[body[i].text],idxs=[i];
    let k=i-1;
    if(k>=0&&!isHead[k]&&!psOf[k]&&headTest(body[k].text)&&!/[.;:!?]$/.test(body[k].text)){
      texts.unshift(body[k].text);idxs.unshift(k);
    }
    headings.push({idx:idxs[0],text:texts.join(' '),page:body[idxs[0]].page,kind:'unlabelled'});
    idxs.forEach(x=>isHead[x]=true);
  }
}
```
Body has no blank lines (filtered), so "immediately followed" = i+1. And previous line = i-1. 

Wait, issue: labelled-heading gathering loop consumes lines until next label or paragraph start — but those consumed lines include unlabelled headings and everything. But blank lines were removed, so a "labelled heading" block from "A." runs until next paragraph start — meaning any text between "A." and the next paragraph is heading text, including stray lines. Per plan. OK.

But careful: unlabelled merge previous line check "does not end a paragraph sentence": I check !/[.;:!?]$/ — but heading lines don't end with those anyway (headTest excludes . ; : , digit). So previous line also passes headTest, meaning it doesn't end with . ; : , — the additional sentence check excludes ! and ?. Also could end with '?' — rare. Fine.

But possible double-processing: after an unlabelled heading at i with merge from k=i-1, the loop continues; k was already marked isHead. Fine.

Paragraph building:
```js
const paras=[];
let cur=null, curSection='', curPart='', headIdx=0;
const headSorted=headings.slice().sort((a,b)=>a.idx-b.idx);
let hPtr=0;
for(let i=0;i<N;i++){
  while(hPtr<headSorted.length&&headSorted[hPtr].idx<=i){
    const h=headSorted[hPtr]; curSection=h.text; if(h.kind==='roman')curPart=h.text; hPtr++;
  }
  // hmm heading idx might equal i when line i is heading
  if(psOf[i]){ if(cur)paras.push(cur); cur={n:psOf[i].n,lines:[],startIdx:i,section:curSection,part:curPart}; if(psOf[i].first)cur.lines.push({text:psOf[i].first,page:body[i].page,bodyIdx:null}); continue; }
  if(isHead[i]){ if(cur)paras.push(cur),cur=null; continue; }
  if(i<firstPS){ /* cover */ coverCount++; continue; }
  if(cur){ cur.lines.push({text:body[i].text,page:body[i].page,bodyIdx:i}); }
  else otherCount++, otherLines.push(i);
}
if(cur)paras.push(cur);
```

Hmm "cur=null; continue;" — syntax: `if(isHead[i]){ if(cur){paras.push(cur);cur=null;} continue; }`.

Wait but paragraph closed at heading — then next paragraph start reopens. But cur.section was updated by the heading before paragraph start: heading processed first in loop (hPtr while) since heading idx < para idx. But I close cur when hitting heading line AFTER updating headings? The while loop runs before the isHead check at same i: heading at idx i gets processed (sets curSection) and then line i closes cur. Good.

Cover lines: also count lines before firstPS that are headings — isHead check comes before cover check? Order in loop: psOf → isHead → cover. isHead before cover so headings before firstPS are headings not cover. Good.

Suspect:
```js
function whySuspect(t){
  if(/^\d{1,3}$/.test(t))return 'bare number';
  if(/^\d{1,3} [A-Z“"]/.test(t))return 'starts with a number and a space';
  if(/^\* /.test(t))return 'asterisk note';
  return null;
}
const susFlag=new Array(N).fill(false), susWhy=new Array(N).fill(null);
for(let i=0;i<N;i++){
  const w=whySuspect(body[i].text);
  if(w){susFlag[i]=true;susWhy[i]=w;
    for(let j=i+1;j<N&&body[j].page===body[i].page;j++)susFlag[j]=true;
  }
}
```

Paragraph finalise:
```js
paras.forEach(p=>{
  p.page_start=p.lines[0].page; p.page_end=p.lines[p.lines.length-1].page;
  p.text=p.lines.map(l=>l.text).join(' ').replace(/\s{2,}/g,' ').trim();
  p.words=p.text.split(/\s+/).length;
  p.text_lines=p.lines.map(l=>l.text).join(' | ');
  p.suspectLines=p.lines.filter(l=>l.bodyIdx!=null&&susFlag[l.bodyIdx]);
  p.flagged=p.suspectLines.length>0||p.words>300;
  p.over300=p.words>300;
  p.fw=firstWords(p.text);
  const rw=ref&&ref.first_words?ref.first_words[String(p.n)]:null;
  p.first_words_match=rw!=null?norm(p.fw)===norm(rw):null;
  p.citation=symbol+', para. '+p.n;
});
```

Note the "first" line from psOf has bodyIdx null — it's not a body line so can't be suspect (its number form has full stop anyway; but the text after could theoretically be suspect — it's real text, skip).

Hyphen count: `const hyphenEnd=body.filter(l=>/-$/.test(l.text)).length;`

Line paragraph association: map bodyIdx → para n: build `linePara` array.

```js
const linePara=new Array(N).fill(null);
paras.forEach(p=>p.lines.forEach(l=>{if(l.bodyIdx!=null)linePara[l.bodyIdx]=p.n;}));
```

Also heading lines and cover lines have linePara null.

Counts:
- foundCount=paras.length; expected=ref?ref.paragraphs:null.
- numbering check: for i, paras[i].n===i+1? collect issues.
- fwMatchCount=paras.filter(p=>p.first_words_match===true).length; fwChecked = paras where rw exists (or expected). Mismatches list.
- flagged pages: 
```js
const flaggedPages={};
paras.forEach(p=>{ if(p.flagged){
  const pagesSet=new Set();
  p.suspectLines.forEach(l=>{ const i=l.bodyIdx; let pg=body[i].page; pagesSet.add(pg); });
  pagesSet.forEach(pg=>{ (flaggedPages[pg]=flaggedPages[pg]||{paras:new Set(),triggers:[]}); flaggedPages[pg].paras.add(p.n); });
  // triggers: lines with explicit why inside this para
  p.suspectLines.forEach(l=>{ if(susWhy[l.bodyIdx]) flaggedPages[l.page].triggers.push({line:l.text,why:susWhy[l.bodyIdx],para:p.n}); });
  if(p.over300){ const pg=p.page_end; ... push {why:'paragraph over 300 words',para:p.n, line:p.words+' words'} }
}});
```
Wait page flagged when it has a suspect line inside a paragraph — suspect lines are all in paragraphs (cover lines can't be suspect? cover lines could match "6 November 2025"? no that's digits then month. "GE.25..." removed. Cover lines before para1 aren't in paragraphs so don't flag. But suspect propagation from a cover line to end of page 1 would flag page 1's paragraph lines! E.g., a cover line matching suspect — "051125 061125" removed as footer. Cover lines like "6 November 2025"? regex /^\d{1,3} [A-Z“"]/ — "6 November" matches! "6 November 2025" starts with "6 " then capital "N" → suspect trigger! Then propagation marks rest of page 1 lines suspect... but cover is before first paragraph; propagation goes to end of page — including paragraph 1's lines on page 1! That would wrongly flag. The plan says: "'6 November 2025' on the cover starts with a number and a space; it is never suspect because the cover comes before the first paragraph." So the suspect rule shouldn't apply to cover lines, and propagation from cover shouldn't happen. So restrict suspect detection to lines at/after firstPS. Propagation also only from triggers at/after firstPS. And also footnote triggers: fine.

But also heading lines could be suspect? Headings don't start with digits. Restrict triggers to lines where linePara!=null? No wait — triggers happen at footnote lines at foot of page, which ARE inside paragraphs (current paragraph continues across pages). Actually a footnote line at foot of page X belongs to the paragraph "current" at that point — which is the paragraph whose text started earlier on that page or a previous page. Since paragraphs close only at next paragraph start or heading, footnote lines at the foot of a page belong to the last paragraph before the footnotes. Yes — that's exactly the design: footnote text glues into the paragraph. So triggers are lines with linePara!=null (or within paragraph region). I'll compute suspect only for i>=firstPS, and effectively triggers only matter if they end up in a paragraph. Simplest: compute susFlag for all i>=firstPS; propagation within page. Then flagged per paragraph. Cover lines (i<firstPS) never suspect, and page-1 propagation from cover impossible. 

But wait: could a trigger line be a heading line? Headings don't start with digits/asterisk. Fine.

Also careful: propagation marks lines after trigger on same page — those may include heading lines etc., harmless.

Now checks:

```js
const checks=[];
function addCheck(name, detail, status, link){checks.push({name,detail,status});}
```
Status: 'pass','fail','info','notrun'.

1. Paragraph count: expected vs found. status pass/fail; notrun if no ref.paragraphs.
2. Numbering: detail "1–n in order" or issues list. pass/fail.
3. First words: n of expected match; mismatches listed on tab01; status pass if 0 mismatches else fail. notrun if no first_words.
4. Pages flagged (info): "n pages flagged, n paragraphs to check".
5. Suspect lines (info): counts.
6. Headers/footers: pass if all pages had symbol header and page number except first... expected: headerPages === pages.length; pageNoPages === pages.length-1 (page 1 has date stamp instead). Status pass if headerPages===pages.length (else fail listing). Detail includes bareRemoved list.
7. Headings: labelled count, unlabelled count, unlabelled listed. pass (info-ish) — I'll make pass with detail.
8. Nothing lost: sum === totalNonEmpty; unclassified listed. pass/fail.
9. Export round trip: parse JSON, count equals. pass/fail (notrun if no paras).

m=9.

Header text: failures>0 → red "n checks failed"; else green "n of m checks pass" with n = pass+info (not notrun). Fine.

Now render. I'll write render functions with template strings.

Tab 01 content:
- tiles grid (4 tiles).
- mismatch list (if any).
- Take the paragraphs away: buttons.
- Every check (m) disclosure.
- Flagged pages (n) disclosure with note + rows.

Flagged page row expansion: show body lines of that page: for each line (text, page) → div, class sus if susFlag[i], prefix mono "L" not needed; mark "→ para. n" if linePara[i]. Also show header/footer dropped note. Clicking row toggles detail div.

Tab 02:
- "Headings found: n" disclosure box listing headings (kind + text).
- table with caption "n paragraphs found, n expected" — caption uses found and expected.
- rows: No | Section | Page | First line | Check. tr tabindex=0 role button aria-expanded; click/Enter toggles detail tr (colspan=5) with full text (spans per line, sus marked), reference vs found words, toggle PDF lines, copy citation button.

First line: first 120 chars cut at word + "…".

Check cell: OK / first words differ (red) / may contain footnote text (red).

Section column: nearest heading (curSection) — maybe truncated with title attr.

Expanded: full path "part › section" if part and section differ.

Copy button: clipboard.

Downloads:
```js
function fname(ext){return symbol.replace(/\//g,'-')+'.'+ext;}
```
JSON content: JSON.stringify(records,null,2). Markdown build.

Markdown headings in document order interleaved with paragraphs: iterate merged list by idx: headings have idx; paragraphs have startIdx. Sort events. Roman → '## ', others → '### '.

Paragraph markdown: `**${n}.** ${text}` + (flagged? ' *(flagged: may contain footnote text)*' : '').

Front matter lines:
```
---
title: "..."
symbol: ...
adopted: ...
source_url: ...
extracted: 2026-.. (today's date new Date().toISOString().slice(0,10))
paragraphs_found: n
paragraphs_expected: n (or "unknown")
pages_flagged: n
footnotes: "not separated; the document has N"
---
```

Now write final HTML. Let me also remember: `count` is string; use pages.length.

Also tab arrow keys: keydown on tablist: ArrowRight/Left move focus & select.

Accessibility: hidden panels not focusable — [hidden] display none handles.

Let me count clickables on tab01: tabs(2)+buttons(2)+disclosures(2)=6 ✓. Plus flagged page rows when opened (inside disclosure, one click deeper) fine.

Write CSS carefully.

Now writing full file. Also note the studio.look: thin rules, no boxes/shadows. Tables with thin borders bottom.

Time to write it out. I'll aim for clarity.

For the rail bar: thin bar under "n paragraphs of m": width percent = found/expected, red if !=.

One more detail: the tiles' "How this is computed" lines.

Mismatch lines format: "para. n: found … / reference …".

Flagged pages table columns: Page | Paragraph | Suspect lines | Why. Paragraph cell: paragraph numbers joined. Suspect lines: trigger line texts (truncated ~60 chars, joined with "; "). Why: reasons.

Expansion: page's body lines with suspect highlighted + which paragraph.

Also "Show the PDF's lines" toggle in expanded para: button toggling a pre-like div showing lines each on own line, with "— p. X —" markers when page changes from previous line.

Also expanded paragraph: reference's six words beside found six: "First words — found: X | reference: Y".

Copy citation: `symbol, para. n`.

Now write.

Also add data-source? No AI used — footer says none.

Alright, writing the code now. I'll be careful with escaping quotes in template literals.

For norm function: 
```js
const norm=s=>s.replace(/[\u201c\u201d]/g,'"').replace(/[\u2018\u2019]/g,"'").replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();
```

firstWords:
```js
function firstWords(text){
  const toks=text.split(/\s+/); const out=[];
  for(const t0 of toks){
    let t=t0;
    const m=t.match(/^(.+?\D)(\d+)$/);
    if(m)t=m[1];
    if(/^\d+$/.test(t)){
      const prev=out[out.length-1];
      if(prev&&/[.,\u201d"]$/.test(prev)&&!/(No|art|para|vol)\.$/.test(prev))continue;
    }
    out.push(t);
    if(out.length===6)break;
  }
  return out.join(' ');
}
```
Note "waste.2" → m[1]="waste." good. Token "17" → no match (needs non-digit prefix), stays. But what about "Goals17"? → "Goals". fine.

But careful: "article 2" — "article" then "2": prev="article" doesn't end with ./, → keep "2". Good. "No. 3": prev "No." — excluded abbreviation → keep "3". Good.

Suspect regex for quote: /^\d{1,3} [A-Z\u201c"]/.

Now — one concern: paragraph start regex /^(\d{1,3})\. (.+)$/ might match a suspect footnote line like "1. See..." — footnotes here don't use that form per plan. Fine.

Also labelRe /^([IVX]+|[A-Z])\.$/ could match a paragraph number like "I."? Paragraph numbers are digits. Could match a body line "A." inside text? Unlikely.

One more: heading gathering for labelled heading consumes lines until next para start — including suspect footnote lines at page foot before the next paragraph. E.g. "IV." heading at top of page after previous page's footnotes? Headings come after footnotes of the previous page in the concatenated stream: previous page's footnote lines are consumed into the previous paragraph (since paragraph closes only at heading/para start). Then heading "IV." on next page: fine, previous paragraph closed at heading line. Good — footnote lines stay in previous paragraph. 

Now the "First line" column: first 120 chars at word boundary.

Let me write the document.

Regarding sizes: fine.

Also add focus ring: :focus-visible{outline:2px solid #9b2335; outline-offset:2px}.

Let me write everything now, final.