Build the full app per plan. One HTML file. Need to implement the pipeline carefully. Let me write it compactly but complete.

Key structures:
- parse records sorted by page
- header/footer removal with diagnostics
- body lines with page tags
- paragraph starts, headings
- paragraphs with lines, suspect detection
- checks
- tabs 01/02, rail, exports, expanded rows.

Let me write the code.

Plan for parsing:

```
const D = WORKSHOP_DATA.pdf_text;
const pages = [...D.records].sort((a,b)=>a.page-b.page);
```

Footer removal per page: iterate lines, from end skip empties; drop while empty || /^GE\./ || /^\d{6}( \d{6})*$/ || bare number 1-3 digits. Record page number line if equals page; other bare numbers counted.

Header: first non-empty line === symbol → drop, count; else warning.

Body lines: remaining lines (keep empties? blank lines dropped later, but heading detection needs blank lines skipped—work with full line list and indexes). I'll build body as array of {text, page}, keeping all lines including blanks for heading logic simplicity. Actually simpler: keep all lines with page tags; process sequentially.

Detection:
- labelledHeading: /^([IVX]+|[A-Z])\.$/ — open heading: skip blanks, collect lines until next label line or paragraph start; a line starting with lowercase or "(" continues heading... Hmm within labelled heading collection: lines are heading text until paragraph-start line or another label. Also unlabelled headings shouldn't interrupt a labelled heading's title? E.g. "I." blank "Introduction" then next is paragraph or "A."? Plan says collect up to next label line or paragraph start. But unlabelled heading test requires line immediately followed by paragraph start — inside a labelled heading the line followed by paragraph start is the heading text itself. I'll process line-by-line with a state machine:

State: currentRoman, currentSection.
For each body line index i:
- if labelled regex → set pendingLabel = m; currentRoman if roman; skip; continue collecting subsequent non-blank, non-label, non-paraStart lines as heading text (joined). Set currentSection = heading text; if roman set currentRoman.
- else if paragraphStart regex → close pending heading; start new paragraph.
- else if pending heading collecting: if line non-blank, append to heading text.
- else (no pending heading): if line non-blank:
   - check unlabelled heading: next non-... plan says "immediately followed by a paragraph-start line". Check next line (skip? "immediately followed"). I'll check the next line is paragraph-start (maybe allow skipping nothing). Also two-line heading: line before it passes same test... Let me implement: line L at i; paraStart at i+1 → candidate heading (≤90 chars, starts capital, not ending . ; : , digit). Also if paraStart at i+2 and line i+1 also passes candidate test and doesn't end paragraph sentence → two-line heading using both. Keep simple: check i+1 paraStart → heading; else check line at i is candidate and line i+1 is candidate and line i+2 is paraStart → two-line heading.

Wait: order matters — the two-line case: line i+1 immediately precedes paraStart; line i is heading first line. Test: line i candidate, line i+1 candidate, i+2 paraStart, and line i "does not end a paragraph sentence" (doesn't end with . ? etc.) — candidate test already excludes those endings. Fine.

Lines before first paragraph start = cover.

Suspect lines inside paragraphs:
- bare number 1-3 digits no full stop: /^\d{1,3}$/
- starts with 1-3 digits, space, capital letter OR UN symbol or quotation mark: /^\d{1,3} [A-Z“"]/ — plan: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". So regex /^\d{1,3} ([A-Z“"A-Z])/ basically /^\d{1,3} [A-Z“"]/. E/ symbols start with letter... "7 E/2003/22" — capital E covers it.
- starts with "* " : /^\* /
A suspect line and every line after it to end of its page are suspect (same page). Flagged paragraph; page flagged.
Paragraph over 300 words flagged.

First words: first six whitespace tokens of text after removing footnote marks. Rules:
- digits glued to end of word or punctuation mark are cut: replace /\d+$/ at token end? "waste.2" → "waste.": token = token.replace(/[0-9]+$/,'') — but only when digits glued... a token like "2025" alone? Then drop only if previous token ends with . , or closing quote and not abbreviation (No., art.). Tokens of digits alone: if prev ends with [.,’”"] and prev lowercased not in ['no.','art.'] → drop. Hmm careful: "No. 3" — prev "No." ends with "." but is abbreviation → keep "3". "article 2" — prev "article" doesn't end with punctuation → keep. Paragraph starting "24." etc — number is part of para start line "24.The..."? Para starts with number-and-text form: text = "24. The Committee..."? Wait paragraph start regex /^(\d{1,3})\. (.+)$/ captures number 24 and text "The...". So text doesn't include the number. But plan says paragraphs 24, 27, 46, 60 "start with real numbers, 'article 2' or 'No. 3'". So text may start with e.g. "24." alone-on-line form: number line "24." then next line "The Committee"? Then text starts with "The". Hmm "start with real numbers" — maybe text like "Article 2..." whatever. My implementation follows rules.

Actually wait — what about paragraph like "1." alone, then next line begins text. The number isn't in text. But some paragraphs' text may begin "24 States..." per edge case "17 Sustainable Development Goals" line starts with number+space — that's a text line, kept.

First-words comparison: take first six tokens after mark removal, join, normalize quotes/dashes/whitespace; compare with reference first_words.

Numbering check: paragraphs numbers == 1..n in order; gaps/duplicates listed.

Nothing lost: classify each non-empty original line: cover, header, heading, paragraph, footer. Sum == total non-empty lines. I need to count: header lines dropped, footer lines dropped (all dropped footer lines count as footer), cover lines, heading lines, paragraph lines. Since every non-empty line falls in one of these buckets by construction, count and compare. Track counts during processing.

Export: JSON and Markdown as specified. text_lines joined " | ".

UI: header, rail, two tabs. Tab 01: tiles, mismatch list, export buttons, two closed headings (Every check, Flagged pages). Tab 02: closed "Headings found: n" box, table of paragraphs with expandable rows.

Tab 02 rows: use buttons aria-expanded; expanded content: full text with suspect lines marked. But text is joined lines — mark suspect lines: render text as joined but highlight suspect line content? Simpler: render paragraph text with suspect line texts wrapped in span. Since lines joined with space, I can build HTML by joining lines, wrapping suspect ones in <span class="sl">. Also show reference six words vs found six words, "Show the PDF's lines" toggle, Copy citation button.

Row count could be 90 — table rows fine. Keep DOM reasonable.

Let me write it. Aim ~600 lines.

Header status: green dot "n of m checks pass" or red "n checks failed". Which checks count? Define checks array with pass booleans. Checks: paragraph count, numbering, first words, pages flagged (informational — count as pass always? It says "a flag is not a failure"), suspect lines (informational), headers/footers (two checks: header all pages, page number all but first), headings (informational), nothing lost, export round trip. Let me define pass/fail: paragraph count (pass if equal), numbering (pass if 1..n), first words (pass if 0 mismatches), header (pass if all pages), footer page numbers (pass if all but first), nothing lost (pass if all classified & sum matches), export round trip (pass). Informational ones: pages flagged, suspect lines, bare numbers, headings — displayed without pass/fail? Plan says one line per check with "pass" or "check failed". I'll give informational ones "noted" style. Simpler: checks list with status pass/fail/info. Header dot: count of pass vs failed among pass/fail checks.

Handle missing reference gracefully.

Edge: if no paragraphs found, tab01 message, disable exports.

Markdown export: front matter, headings in document order with ## and ###. Need heading positions relative to paragraphs. During parsing, record headings in order with level (roman → ##, lettered → ###, unlabelled → ###?). Plan: "the headings as ## and ### lines in document order". Roman → ##, others → ###. I'll keep an ordered list of {level, text, afterParagraphIndex} and interleave.

Download: Blob URL.

Copy citation: navigator.clipboard maybe unavailable in sandbox; fallback textarea+execCommand. Show "Copied" 2s.

Let me now write the HTML.

Structure:

```html
<!doctype html><html lang="en"><head>...styles...</head>
<body>
<header>...</header>
<nav tabs>
<main: rail + section panels>
<footer>
<script>
```

Rail visible always; tabs switch panels. Both panels show paragraphs table? Tab01 doesn't show table; tab02 does.

Filters: none. Fine.

Write JS:

```js
const D = window.WORKSHOP_DATA.pdf_text;
const R = D.reference || {};
const pages = [...(D.records||[])].sort((a,b)=>a.page-b.page);
const lines = []; // {text,page,kind:null}
```

Process per page: split text by /\r?\n/. header: find first non-empty index; if equals symbol, mark kind 'header'. Footer: from end, walk while empty or footer pattern; mark 'footer'; record info.

Footer pattern fn:
```js
function isFoot(l){
  if(!l.trim()) return true;
  if(/^GE\./.test(l)) return true;
  if(/^\d{6}( \d{6})*$/.test(l.trim())) return true;
  if(/^\d{1,3}$/.test(l.trim())) return true;
  return false;
}
```
While walking from end: skip empties (kind 'blank' — but they're empty, not counted in non-empty classification). Non-empty footer lines get kind 'footer'. Track: if bare number equals page → pageNumber; else bareNums list {page, n}. Stop when line not footer-pattern.

Body lines: lines between header and footer start, each {text, page}. Keep blanks in body array for heading logic? I'll keep all body lines (with blanks) tagged, then in the state machine skip blanks but use indices.

Classification counts: non-empty lines total = sum of kinds. Blanks excluded. Kinds: header, footer, cover, heading, para. Every non-empty body line must get cover/heading/para. By construction yes. unclassified = 0 always but compute anyway.

State machine over bodyLines (array of {t,page,kind?}):

```js
const paras=[], headings=[], coverCount=0;
let curRoman='', curSection='', pendLabel=null, pendText=[], cur=null, coverDone=false;
const reNumAlone=/^(\d{1,3})\.$/;
const reNumText=/^(\d{1,3})\. (.+)$/;
const reLabel=/^([IVX]+|[A-Z])\.$/;
```

I'll iterate i over bodyLines; blanks skipped except within labelled heading collection (skip them).

Algorithm:
```
for i:
 l = body[i]; if l.t==='' continue... but pending heading must not consume across blanks? "skip blank lines, then every line up to the next label line or paragraph start is heading text"
```

Implementation:

```
if(pendLabel){
  if blank: continue (but if next meaningful is paraStart, heading ends — handled since we check before appending)
  if reLabel.test(l) or paraStart(l): close heading (headings.push, set curSection; if roman curRoman), pendLabel=null; fall through to process this line normally
  else append l to pendText (mark heading)
  continue-ish
}
```
Careful ordering. Let me write with a helper closeHeading().

Actually simpler: handle at each non-blank line:

```
function paraStart(l){ return reNumAlone.test(l)||reNumText.test(l); }
```

Pseudocode:

```
for i in 0..n-1:
  l=body[i]; if(!l.t) continue;
  if(pending){ // collecting labelled heading text
     if(reLabel.test(l.t)||paraStart(l.t)){ closePending(); /* then process l below */ }
     else { pending.text.push(l.t); l.kind='heading'; continue; }
  }
  m=reLabel.exec(l.t);
  if(m){ pending={roman:/^[IVX]+$/.test(m[1]), text:[]}; l.kind='heading'; continue; }
  if(paraStart(l.t)){
     if(!coverDone) coverDone=true;
     closePending();
     // unlabelled heading detection happens before this line, handled when we processed previous line... 
```

Problem: unlabelled heading detection needs lookahead. So before classifying a non-blank line as paragraph text, when processing line i we should have already looked ahead when processing line i-1... Easier: do lookahead at line i itself: check if line i is an unlabelled heading (next non-? line i+1 or i+2 paraStart). But a paragraph's text line could also be followed by a paraStart line (end of paragraph). Test: candidate heading = starts capital, ≤90 chars, not ending [. ; : , digit]. A paragraph's last line often ends with "." → excluded. Risk of false positive if last line ends without punctuation. Acceptable per plan.

So at line i (non-blank, not label, not paraStart, not pending):
```
if(coverDone && isUnlabHeading(i)){
   l.kind='heading'; curSection = heading text; headings.push; continue;
}
if(!coverDone){ l.kind='cover'; coverCount++; continue; }
l.kind='para'; cur.lines.push(l);
```

isUnlabHeading(i): cand(t): t.length<=90 && /^[A-Z“"]/... starts with capital letter: /^[A-Z]/. not ending [.;:,0-9] and not ending digit. 
- if body[i+1] non-blank? plan says immediately followed. Use raw next line (i+1). If paraStart(body[i+1].t) → heading single.
- two-line: cand(body[i].t) && cand(body[i+1].t) && paraStart(body[i+2]?.t) && body[i+1] not blank && body[i+2] exists. Also "when the line before it passes the same test and does not end a paragraph sentence" — cand already excludes sentence-ending punctuation. OK.
Return heading text joined.

But wait: what about the last line of a paragraph followed by blank then paraStart? next line is blank → not immediately followed → not heading. Good. But real headings followed by blank line then paragraph number? Plan says unlabelled headings are "on the line or two lines just before a paragraph number" — immediately. Fine.

Blank line check: body[i+1].t === '' fails paraStart → single-line check fails; two-line check body[i+1] blank fails cand. OK.

Also labelled heading with pending: pending closes when hitting paraStart or label. But what if pending heading is followed by blank lines then paragraph? We skip blanks while pending; then hit paraStart → closePending. But careful: my loop `if(!l.t) continue;` inside pending skips blanks — good, matches "skip blank lines".

closePending: text = pending.text.join(' '); curSection=text; if pending.roman curRoman=text; headings.push({level: pending.roman?2:3, text, paraIndex: paras.length}); reset pending=null.

Wait roman push level 2; lettered level 3; unlabelled level 3.

Also when closing because of new label while pending — fine.

For unlabelled close: headings.push({level:3,text,paraIndex:paras.length}); curSection=text.

Paragraph creation at paraStart:
```
m = reNumText.exec or reNumAlone
num = +m[1]; firstText = reNumText? m[2] : null
cur = {num, lines:[], pageStart:l.page, section:curSection, part:curRoman}
paras.push(cur)
if(firstText){ cur.lines.push({t:firstText,page:l.page,kind:'para'}) }
l.kind='para'
```
Mark the number line kind 'para' too.

After loop, closePending if still pending (heading at end — weird).

Then compute per paragraph: text = lines.map(t=>t.replace(/\s+/g,' ').trim()).join(' ') with double space collapse. pageEnd = last line page.

Suspect: for each paragraph, iterate lines; if line.suspect or pageAlreadySuspectFromEarlier? Rule: "A suspect line and every line after it to the end of its page are suspect". So once a suspect line found on page P, all subsequent lines of that paragraph on page P are suspect. Implement per paragraph: suspectActive=false, lastSuspectPage=null; for each line: if line.page===lastSuspectPage → suspect. else if isSuspect(line.t) → suspect, lastSuspectPage=line.page. Mark.

isSuspect(t): 
```
t=t.trim();
return /^\d{1,3}$/.test(t) || /^\d{1,3} [A-Z“"]/.test(t) || /^\* /.test(t);
```

Word count > 300 → flagged.

Hyphen-ending lines count: lines ending with '-'.

Footnote mark removal for first words:
```
function firstWords(text){
  let toks=text.split(/\s+/);
  let out=[];
  for(let j=0;j<toks.length && out.length<6;j++){
    let t=toks[j];
    // cut digits glued to end
    t=t.replace(/[0-9]+$/,'');
    if(/^\d+$/.test(t)){
      const prev=out[out.length-1];
      const pl=prev?prev.toLowerCase():'';
      if(prev && /[.,;’”"]$/.test(prev) && !['no.','art.','para.','paras.','p.','pp.'].includes(pl)){
        continue; // drop
      }
    }
    if(t) out.push(t);
  }
  return out.join(' ');
}
```
Hmm but digits-alone token with prev ending punctuation: only drop when prev ends . , or closing quote. Semicolon? plan says "full stop, comma or closing quote". Use /[.,”’]/. Abbreviations "No." "art.". Also need lookahead? Dropping changes prev for next? Minor.

Wait, also glued digits: "waste.2"→"waste." good; but a real token "article2"? unlikely. Also token like "2025," ends with comma not digits — fine.

Compare: normalize both: replace curly quotes straight, en/em dashes hyphen, collapse whitespace:
```
norm=s=>s.replace(/[“”]/g,'"').replace(/[‘’]/g,"'").replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();
```

Checks:
- paragraphs found vs R.paragraphs
- numbering: nums equal 1..n sequence
- first words mismatches
- pages flagged (info)
- suspect lines count (info)
- header pages count vs pages.length
- page-number pages vs pages.length-1
- bare numbers removed (info list)
- headings count (info, list unlabelled)
- nothing lost: classification counts sum vs non-empty total
- export round trip: JSON.parse(JSON.stringify(exportRecs)).length === paras.length

Header dot: failed = checks with fail. passCount.

Now UI rendering. Build with template strings, then attach event listeners.

Tab 02: headings box (closed, button aria-expanded, shows list when open). Table with 90 rows; each row: a button row (tr with td containing button? For aria-expanded rows, make each row's first cell a button that toggles a detail row). Simpler: each paragraph rendered as a div: header line (button, aria-expanded) with columns via CSS grid, then detail div hidden. But plan says table with caption, th scope. I'll do a real table where each paragraph = two <tr>: main row (button in first cell spanning? ) Hmm. I'll use table: main row cells: No (button with aria-expanded), Section, Page, First line, Check. Detail row (hidden) colspan=5 with full text etc. Button toggles.

But "Rows are buttons with aria-expanded" — I'll make the number cell a button. Good enough, focusable.

Expanded: full text with suspect lines marked (span.sl thin red box), found six vs reference six words, "Show the PDF's lines" toggle button, copy citation button, section full path.

Suspect marking in joined text: build html from lines: lines.map(l=> suspect? `<span class="sl">${esc(l)}</span>` : esc(l)).join(' ').

Tab 01 flagged pages table inside closed heading: rows Page|Paragraph|Suspect lines|Why. Why reasons: for each suspect line, classify: bare number / number+space+capital / asterisk / "paragraph over 300 words" for the para flag. Clicking row expands raw lines of that page with suspects highlighted and paragraph they sit in. Raw lines: I need original page lines with their classification/suspect status. Store during parsing: for each page, array of {t, cls, suspect, paraNum}. I dropped header/footer lines from body but kept them marked — I'll keep a per-page allLines list with computed info. During footer/header processing mark kind. Body lines get kind later; after paragraph assignment, annotate each body line with para num and suspect. Then flagged-pages row expansion renders page's lines.

Let me maintain: pageLines[pageIndex] = array of {t, kind, suspect:false, para:null}. Header/footer lines kind set, para null. Body lines reference same objects as body array entries so annotation propagates. I'll make body entries the same objects.

Suspect "why": I'll compute reason per flagged page: list reasons of its suspect lines: bare number → "bare number"; /^\d+ [A-Z]/ → "starts with a number and a space"; /^\*/ → "asterisk note"; plus "paragraph over 300 words" if any flagged paragraph on that page by word count.

Suspect lines count on page: number of directly-suspect lines? "Suspect lines" column: count of suspect lines in paragraphs on that page (including trailing-to-page-end ones). I'll count all lines marked suspect on that page.

Now exports.

JSON records:
```
{symbol, paragraph, section, part, page_start, page_end, text, text_lines: lines.join(' | '), flagged, first_words_match, citation, doc_url, limitations}
```

Markdown:
```
---
title: ...
symbol: ...
adopted: ...
source_url: doc_url
extracted: YYYY-MM-DD
paragraphs_found: n
paragraphs_expected: m
pages_flagged: k
footnotes: "not separated; the document has N"
---
```
then iterate headings interleaved with paragraphs: maintain pointer over headings (they have paraIndex). For each para index: while headings with paraIndex===idx, print heading line. Then para: **n.** text (+flag note).

File names: symbol.replace(/\//g,'-') + '.json'/'.md'.

Download via Blob.

Copy citation: try navigator.clipboard.writeText; fallback.

Tabs: role tablist, arrow keys. Panels hidden attr; CSS [hidden]{display:none!important}.

Check panel: list of lines.

First-words mismatch list on tab 01 under tiles (max 10 + "and n more").

Counts line in header: source, n pages, built? Header line: symbol link, adopted, n pages, source. Footer: source, built, no-model note. D.built exists? pdf_text shape doesn't list built... it lists {title, symbol, doc_url, source, count, records, reference}. Plan footer says source, built. Use D.built || '' guard.

Write the code now, carefully but concisely.

Also "n paragraphs of reference.paragraphs" bar on rail: thin bar width = found/expected, red when short or over.

Handle missing reference: tiles "no reference in this file".

Let me draft final HTML.

Regarding no paragraphs: guard exports disabled.

CSS: paper theme per studio.

Let me write it all out.

Edge: paragraph number with text line: "23.Text..."? The PDF sample shows "1.\nA clean..." — number alone. Fine.

Cover: lines before first paragraph start. Cover lines counted kind 'cover'.

Now compute non-empty totals: totalNonEmpty = sum over pageLines of t.trim()!=='' . But footer walk skipped empties at end (fine). Header: first non-empty line. Cover etc. classified. Sum of kinds (header+footer+cover+heading+para) should equal totalNonEmpty. Compute classifiedCount and unclassified list (lines with kind null and non-empty). By construction none, but compute anyway.

Careful: pending heading lines marked 'heading'. Unlabelled heading lines: mark the 1-2 lines 'heading'.

One catch: in isUnlabHeading two-line case, mark both lines heading.

Also "coverDone" — lines before first paragraph start are cover even if they'd match heading tests. My check `if(coverDone && isUnlabHeading(i))` — but also labelled headings before first paragraph? Cover includes them? Plan: "Lines before the first paragraph start are the cover." So yes, cover. But reLabel check comes before coverDone check in my flow — a roman label on cover page would start pending heading. Hmm cover pages: "I." appears after paragraph 1 typically. Page 1 has cover lines then "I." label. First paragraph start is para 1 which comes after "I. Introduction". So cover = lines before... wait "1." paragraph start comes AFTER the heading "I. Introduction". So coverDone stays false through the heading! Then "I." would be classified cover, not heading, and para 1's section would be empty.

Hmm. Plan says lines before the first paragraph start are the cover. So headings before para 1 count as cover?? That would lose "Introduction" as section for para 1. But the plan's pipeline order: paragraph starts; "Lines before the first paragraph start are the cover." Then headings rules apply... ambiguous. But cover is typically: "United Nations", "Economic and Social Council", distr lines, title, date. Then "I." label, "Introduction", then "1." So if cover = everything before "1.", the Introduction heading is cover and para 1 has no section. That seems wrong for citations ("section" would be empty for para 1). 

I think better: cover = lines before the first paragraph start OR first heading, whichever comes first. I'll implement: once we hit a labelled heading or an unlabelled heading candidate, coverDone becomes true (headings begin). That is: cover is lines before the first structural element. This keeps "Introduction" as para 1's section. I'll set coverDone=true when pending opens or unlabelled heading found. Document has title on cover as h2-like lines — could an unlabelled heading test trigger on the cover title? Title line "General comment No. 27 (2025) on economic, social and cultural rights andthe environmental dimension of sustainable development *" — >90 chars, excluded. Other cover lines: "Committee on Economic, Social and Cultural Rights" — 49 chars, starts capital, ends 's' (not excluded)... immediately followed by? Next line maybe the h2 title (long, not paraStart) → not heading. Good. "Introduction" comes after "I." label anyway. So safe-ish. Also "6 November 2025" starts with digit → not capital start. Fine.

Set coverDone when: reLabel matched, or isUnlabHeading true. I'll restructure: 

```
if(m=reLabel){ pending=...; coverDone=true; ...}
if(paraStart){ coverDone=true; ...}
if(coverDone && isUnlab(i)){ ... coverDone=true }
```

OK.

Another catch: unlabelled heading check must not fire for a line that is the last line of previous paragraph followed immediately (no blank) by next paragraph number. Paragraph text lines wrap; last line ends with "." typically → excluded by candidate test. Accept risk.

Also lines inside pending heading collection shouldn't be checked for unlabelled. Handled.

Now the "part" (roman section) and "section": for para 1 under "I. Introduction", section="Introduction", part="Introduction"? part = most recent roman heading text. Fine.

Let me also record headings order with paraIndex = paras.length at time of heading creation (number of paragraphs before it). Unlabelled heading set curSection.

Now write everything.

For rendering 90 paragraphs + details lazily: build detail HTML on first expand to save size. Fine, build on demand.

Charts: none needed (no chart required). OK.

Write final file. Estimate ~700 lines. Let's go.

Number formatting: big serif numbers.

Header right: dot green "n of m checks pass" / red "n checks failed" plus "n pages flagged".

Let me write the code.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
 :root{--ink:#1d1b18;--paper:#f4f0e8;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b34;}
 *{box-sizing:border-box}
 body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
 [hidden]{display:none!important}
 .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
 header.site{padding:18px 28px 14px;border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}
 h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;margin:6px 0 4px;font-weight:600}
 ...
</style>
```

I'll write it fully in the answer. Keep CSS moderate.

Tabs nav: buttons role=tab, arrow keys handler.

Let me now write the JS in full mentally then output.

Key data vars after parse:
- P = paras array: {num, section, part, lines:[{t,page,suspect}], text, pageStart, pageEnd, flagged, wordCount, firstWordsFound, firstWordsMatch}
- headingsList: {level,text,paraIndex, type:'labelled-roman'|'labelled-letter'|'unlabelled'}
- flaggedPages: map page→{suspectLines:[{t,para}], reasons:Set, paras:Set}
- checks array
- counts.

Rendering tab 01 tiles etc.

Export JSON records built from P.

Round trip check: JSON.parse(JSON.stringify(recs)).length === P.length.

Copy citation per paragraph.

OK, writing output now. Also flagged-pages expandable rows within tab 01 (closed heading "Flagged pages (n)"), each row click → show raw lines.

"Every check (m)" closed heading with check lines; failed checks link to rows concerned — I'll just describe; for numbering failure list gaps; keep simple: link text jumps to tab 02? I'll render plain text listing, plus a link for first-words to tab02. Keep simple: text.

Time to write. I'll be careful with escaping (quotes in template strings with esc()).

esc function:
```js
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
```

Detail row includes text with suspect spans — build via esc per line.

Write everything now.