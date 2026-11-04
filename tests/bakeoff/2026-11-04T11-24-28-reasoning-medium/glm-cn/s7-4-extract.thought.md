Build the full app per the plan. One HTML file. Need to implement pipeline: header/footer removal, body concatenation, paragraph detection, headings, suspect lines, first words, checks, tabs, CSV download, raw page viewer with classification colours.

Keep it manageable but complete. Let me write carefully.

Data: WORKSHOP_DATA.pdf_text = {title, symbol, doc_url, source, count, records, reference, built?} — plan mentions built date in footer. I'll read `built` if present.

Multiple documents: iterate keys of WORKSHOP_DATA where value has records and reference. pdf_text and pdf_text_2 both qualify! Plan says "every document in WORKSHOP_DATA with records and a reference gets its own card in the rail, in the order of the data; the selected card has a red left border". So support pdf_text and pdf_text_2. Good — write generically.

Pipeline details:

1. For each page (sorted by page): lines = text.split('\n').
2. Header: first non-empty line === symbol → drop, log repair {page, kind:'header line removed'}. Else warning check.
3. Footer: from end, drop lines while: empty; starts with "GE."; /^(\d{1,3})$/ bare number → if == page it's page number (log 'footer line removed' with note page number? Plan kinds: "footer line removed" and "bare number removed from the footer" separate). Actually kinds listed: header line removed, footer line removed, bare number removed from the footer, number and text split, paragraph joined across a page break, heading separated, heading title joined. So page-number lines and GE./date lines log "footer line removed"; other bare numbers log "bare number removed from the footer".

Careful: footer scan from end while condition matches — but stop when a line doesn't match? "From the end of each page, drop lines while the line is empty, starts with GE., 6-digit groups only, or bare number 1–3 digits." But paragraph text could be last line before footer... a bare number at end could be paragraph text? Unlikely. But we must only drop trailing footer lines while they match; a line like "waste." stops. But wait: last real line of text could be a bare number? Paragraph text lines end with full stop typically. Accept the rule as specified. But danger: date stamp "051125 061125" — matches 6-digit groups: /^(\d{6})( \d{6})*$/. Plan says "consists only of 6-digit groups". Implement regex.

Edge: footer scan should stop once we hit a non-matching line. But empty lines: body blank lines near foot... after footnotes there's blank then footer. Dropping trailing empties fine. But if the last body line before footnotes... footnotes aren't separated; footnote text is the last body content. So footer scan starts after footnote text. Footnote lines end with "." etc. OK.

But wait: bare number in footer — "on 12 pages a third bare number sits in the footer". These get dropped from footer scan. But the plan says suspect lines flag footnote blocks; the displaced footnote number in the footer is removed, fine.

Hmm, but footer scan "while" from the end: order varies. E.g. lines: [.., "12", "GE.25-15926", "13"]? Page number might come before or after job code. The while loop handles any order as long as all match.

Risk: the while loop dropping bare numbers could eat a footnote number that sits above the footer but... it only drops from the end while matching, so once it hits footnote text (non-matching), it stops. But what if footnotes end with a line that's a bare number? Footnote text lines end with periods. OK.

4. Concatenate body lines of all pages with page tags.

5. Classify. Iterate over body lines with index:
- labelled heading: /^([IVX]+|[A-Z])\.$/ → open labelled heading; skip blank lines (blank lines already dropped? Plan says blank lines dropped for paragraphs; but heading detection says "skip blank lines". Simpler: work with a list of non-empty body lines with (page, lineNo) tags — but "skip blank lines" in heading just means go to next non-empty. Actually since blank lines are dropped from paragraphs anyway and headings skip them, I can filter out empty lines from the body list entirely? But line numbers in raw viewer and suspect line numbers reference original line numbers — keep original lineNo per line for reporting; blank lines just don't appear in body list. But "Nothing lost" check: every non-empty line classified exactly once. Empty lines aren't counted. Fine.

Hmm wait — one subtlety: "A line starting with a lowercase letter or "(" continues the previous heading line" — for wrapped heading titles. And unlabelled headings: a non-empty line immediately followed by a paragraph-start line, ≤90 chars, starts with capital, not ending with ./;/:/,/digit. And when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading.

Paragraph start: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/.

Algorithm over bodyLines (array of {page, lineNo, text}):

i=0; state: currentHeadingPath = [], currentPart = null, currentParagraph = null (accumulator).
cover: lines before first paragraph start — but headings before first paragraph? Cover is "lines before the first paragraph start". The intro heading "I." + "Introduction" comes before paragraph 1? In sample page 1: "I.\n\nIntroduction\n1.\nA clean..." So heading lines appear before paragraph 1. Are they cover or headings? Plan: "Lines before the first paragraph start are the cover." Hmm that would make "I. Introduction" cover. But headings detection: labelled heading rule applies anywhere. I think classification order: headings are detected as headings regardless; "cover" = remaining unclassified lines before first paragraph start. Let me do: process labelled headings and unlabelled headings via lookahead; paragraph starts start paragraphs; remaining lines before first paragraph start = cover; after = paragraph text.

But unlabelled heading detection requires "immediately followed by a paragraph-start line". Before para 1, the line before "1." is "Introduction" (labelled heading text). It would also pass unlabelled test... but labelled heading processing takes precedence. Process in a single pass:

for each line:
 - if labelled-heading label line (/^([IVX]+|[A-Z])\.$/): start labelled heading; consume following lines as heading text until next label line or paragraph start; within, a line starting lowercase or "(" joins previous (log 'heading title joined from two lines' — only if actually joining two lines); set currentPart if roman; section = title.
 - else if paragraph start: handle unlabelled heading check on previous line(s) — but previous line may already be consumed as paragraph text. Hmm. Need lookahead: when we encounter a paragraph start line, check the previous body line: if it hasn't been classified yet (i.e., it was added to current paragraph), test if it's an unlabelled heading. But by then it's in the paragraph. Better: before appending a line to a paragraph, we can't know if the next line is a paragraph start. So use lookahead when appending: when processing line i (candidate paragraph text), check if line i+1 is a paragraph start and line i passes unlabelled heading test → classify line i as heading (and check line i-1 similarly for two-line join). Implement: when about to append line i to current paragraph, first check unlabelled-heading conditions.

Let me restructure as index loop with explicit decisions:

```
let paras=[], headings=[], repairs=[], coverLines=[];
let cur=null; // current paragraph
let section=null, part=null, labelled=null;
for(let i=0;i<L.length;i++){
  const ln=L[i];
  if(labelRe.test(ln.text)){
    // labelled heading: gather title lines
    let j=i+1; let titleLines=[];
    while(j<L.length && !labelRe.test(L[j].text) && !paraStartRe.test(L[j].text)){
      titleLines.push(L[j]); j++;
    }
    // join: a line starting lowercase or "(" continues previous
    ... build title
    // if labelled was roman, part=title
    ...
    i=j-1; continue;
  }
  if(paraStart.test(ln.text)){
    // check previous line for unlabelled heading (only if it was appended to cur paragraph)
    maybeExtractUnlabelledHeading(i);
    // close cur, start new
    ...
    continue;
  }
  // otherwise: could be unlabelled heading if next line is paraStart
  if(isUnlabelledHeading(ln.text) && i+1<L.length && paraStart(L[i+1]) ){
     heading separated repair; 
     // two-line join: check line i-1 also passes test and doesn't end a paragraph sentence
     if(i>0 && L[i-1] is paragraph text (last appended to cur) && isUnlabelledHeading(L[i-1].text) && !endsParagraphSentence(L[i-1].text)){
        pop from cur, join, repair 'heading title joined from two lines'
     }
     section = joined title; headings.push; continue;
  }
  if(cur) cur.lines.push(ln); else coverLines.push(ln);
}
```

But wait: the two-line-join check: "when the line before it passes the same test and does not end a paragraph sentence". Line before must be part of current paragraph (otherwise it's a heading already). endsParagraphSentence: ends with "." or "?" etc? "does not end a paragraph sentence" — I'll define: ends with '.', '!', '?', ':' maybe. If previous line ends with '.', it ends a sentence → not a heading join. Good: paragraph lines typically end with '.'; heading first lines don't ("Right to work" → "(art. 6)" wraps; first line "Right to work" doesn't end with period).

Also, what about the labelled heading detection interfering: a line "A." is also... could a paragraph line be "A."? Unlikely.

Problem: labelled heading gathering: "every line up to the next label line or paragraph start is heading text" — but what if there's other content (e.g., footnote text) between? On this file, headings are clean. But what about cover lines before "I."? Fine.

Hmm, but labelled heading at end of a page followed by... e.g., "IV." at bottom of page, title on next page — gathering crosses pages, fine since concatenated.

Wait — there's a subtlety with the labelled heading while loop: if the labelled heading is followed by footnotes (suspect lines) before the next paragraph... could swallow footnote text into heading. Not on this file presumably. Accept.

Also: the labelled heading title could itself wrap: "a line starting with a lowercase letter or '(' continues the previous heading line". Join those.

Paragraph start handling: 
- if /^(\d{1,3})\.$/: number = n, first line is next line(s). 
- if /^(\d{1,3})\. (.+)$/: number = n, first line = rest; log "number and text split".

Unlabelled heading extraction must happen before starting the paragraph (looking at previous line). But careful ordering in my loop: I check unlabelled heading when processing the candidate text line (before the paraStart line). That's the lookahead approach — handled in the "otherwise" branch. Good, so at paraStart I don't need to extract. But the two-line join also handled there. 

But one issue: the unlabelled heading line immediately before paragraph start — in my "otherwise" branch I check `paraStart(L[i+1])`. But what if next line is a labelled heading label and then paragraph? No — unlabelled heading is directly before the paragraph-start line. OK.

Also heading before paragraph could be at the very start (i=0, before any paragraph): then line before doesn't exist. cur is null → it's cover... but if it passes unlabelled heading test and next is paraStart, it's a heading. My branch handles it regardless of cur (cover line case: if cur is null, the previous line might be a cover line — the two-line join check requires it was appended to cur; if cur null, skip join). Actually for the two-line join, previous line could also be unclassified... keep simple: only join if previous line was the last line of cur and passes tests.

Hmm wait, there's an issue: the unlabelled heading test requires "does not end with a full stop, semicolon, colon, comma or digit" and "starts with a capital letter", ≤90 chars. Lines of paragraph text before a new paragraph number typically end with '.', so they fail the test — good, no false positives normally. But the last line of a paragraph might not end with '.' (e.g., ends with ')' or a quote). Then it'd be mistaken for a heading — plan acknowledges this risk; the headings check lists unlabelled headings so reader can spot. Fine.

Edge: a line "A clean, healthy..." — starts with capital, doesn't end with... it's paragraph text mid-paragraph, but only lines immediately before a paragraph start get tested. The last line of para 1 ends with '.', so safe.

Suspect lines: inside a paragraph, a line is suspect when:
- bare number 1–3 digits no full stop: /^\d{1,3}$/
- starts with 1–3 digits, space, then a UN doc symbol or quotation mark or capital letter: /^\d{1,3} [A-Z"“]/? Plan: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". So /^\d{1,3} (\d|[A-Z"“])/ maybe — doc symbols start with letter or digit (E/..., A/...). Just: /^\d{1,3} [A-Z0-9"“]/. Hmm "capital letter, a UN document symbol or a quotation mark" — union. I'll use /^\d{1,3} [A-Z0-9"“„]/.
- starts with "* ".

"A suspect line and every line after it to the end of its page are suspect" — footnote block runs to foot of page. So once a suspect line found on page P (inside a paragraph), all subsequent body lines of page P are suspect. Note: the last body lines of a page are footnotes; the first footnote's number line is the first suspect. Implementation: per page, find first suspect line index among body lines (by original line order), mark all body lines from there to page end as suspect. But "A page is flagged when it has a suspect line inside a paragraph". Also suspect lines must be inside a paragraph — cover lines? Cover before para 1; "* Adopted by the Committee..." note is on page 1 before para 1? It's in cover probably. Plan: suspect line rule includes "* " lines. If it's cover, not "inside a paragraph". Flagging: page flagged when suspect line inside a paragraph. Cover suspect lines — hmm, "the note on the first page" is listed as an example of a suspect line. It's cover. I'll still record suspect lines anywhere but flag pages only when inside a paragraph... Actually simpler: compute suspect per body line (with the page-run rule), flag page if any suspect line belongs to a paragraph. The cover "* Adopted..." would be suspect but page 1 also has footnotes after para 1? Page 1 contains paras 1–3 probably plus footnotes → flagged anyway.

Wait, the page-run rule: "A suspect line and every line after it to the end of its page are suspect". Apply per page within that page's body lines. But also a heading after a suspect line? Page's remaining lines all suspect. OK.

But careful: the page-run must be based on original line numbers within the page (body lines only). Implementation: for each page, iterate body lines in order; find first that matches suspect start; mark that and all following body lines of that page as suspect.

Paragraph over 300 words → flagged too (flag the paragraph, and page? "A page is flagged when it has a suspect line inside a paragraph" — separate: paragraphs over 300 words are flagged; the "Pages flagged" check lists "the pages with suspect lines inside a paragraph and the paragraphs over 300 words, each listed with its page and paragraph". So long paragraphs add to flagged pages too? The tile says "n pages flagged" of the document's pages... I'll include long-paragraph pages in flagged pages set. Hmm, plan: "A paragraph over 300 words is flagged too". And flagged pages = pages with suspect line inside a paragraph. For the page count I'll use union: pages with suspect-in-paragraph, plus pages of over-300-word paragraphs. Simpler and matches check listing.

Actually re-read: "**Pages flagged.** The pages with suspect lines inside a paragraph and the paragraphs over 300 words, each listed with its page and paragraph." So yes, union.

First words: strip footnote marks from first six words:
- digits glued to end of word or punctuation: cut trailing digits: token.replace(/\d+$/,'') — but "waste.2" → "waste." Keep.
- token of digits alone dropped only when previous token ends with '.', ',', or closing quote and is not abbreviation "No."/"art." (and similar?). Abbreviations list: ["No.","art.","Arts.","para.","paras.","vol.","p.","pp.","No"]. I'll include a small set.

Then take first six remaining words. Compare with reference first_words (also normalised? The reference presumably clean). Normalize both: curly→straight quotes, en/em dash→hyphen, whitespace runs→single. Also should I strip footnote marks from reference too? Plan says found-side only. But to be safe, apply same normalisation to both, and also maybe strip trailing digits from reference tokens? Plan doesn't say; keep to normalisation only. Hmm, risk: reference first_words may themselves contain footnote marks? "first_words" from reference like "A clean, healthy and sustainable environment" — clean. Keep normalisation only.

Numbering check: numbers exactly 1..n in order.

Nothing lost check: total non-empty lines across all pages = sum of classified counts (cover + header + heading + paragraph + footer). Suspect lines count as paragraph. I track each original line's class in a map page→lineNo→class for the raw viewer and this check.

Repairs log entries: {page, target (paragraph number or 'footnote'/'—'), kind, before, after}. Kinds:
- header line removed: before = symbol line.
- footer line removed: before = line.
- bare number removed from the footer: before = number, page.
- number and text split: before = "23. The Committee...", after: "23." / "The Committee..." target para.
- paragraph joined across a page break: when paragraph's lines have ≥2 distinct pages → log per paragraph, before = last line of prev page + " ⏎ …" maybe; after = joined. Keep simple: before = "…end of page A", after = "start of page B joined". I'll store before: `page A last line: "..."`, after: `page B first line: "..."`.
- heading separated: before/after the line.
- heading title joined.

Repairs that touched a paragraph: filter by target para number for expanded row.

Check panel items:
1. Paragraph count: found vs reference.paragraphs.
2. Numbering: 1..n in order; list gaps/dupes.
3. First words: n mismatches, list each.
4. Suspect lines: n suspect lines on n pages, in n paragraphs; none removed.
5. Pages flagged: list page+paragraph.
6. Headers and footers: pages with symbol header (expected all), pages with page number in footer (expected all but first), bare numbers removed from footer with pages.
7. Headings: counts labelled/unlabelled + list unlabelled.
8. Nothing lost: classification sum.

Checks "pass/fail": define pass for each:
1. equal.
2. exactly 1..n.
3. zero mismatches.
4. informational? "none is removed" — always pass? I'll make it pass (it's a report). Hmm, a check should have expected output. Suspect lines check: report; pass = true (nothing removed by construction) — mark "pass" with note. Actually plan: "A flag is not a failure". So suspect lines & pages flagged checks show info; I'll display them as pass (green "report") — but "pass" must be honest. I'll label them "report" style: still show values; count them as pass in the "n of m checks pass" header. Hmm. The header says "n of m checks pass". I'll count checks 1,2,3,6,7,8 as pass/fail and 4,5 as always-pass reports (they can't fail). That's fine — m = total checks.

If reference missing: checks 1,3 "not run".

Now tab 02 table: columns No. | Section | Page | First line | Check. Rows expandable. Expanded: full text (one block, suspect lines highlighted — wrap suspect line text in <mark>? The text is joined; to highlight suspect lines in running text I can join with spans: render each line as span, suspect ones with mark styling). Then "Show the PDF's lines" toggle showing lines with page numbers where page began. Then reference first six words vs found, pages, repairs touching para, Copy citation button.

Tab 03: flagged pages rows: Page | Paragraph | Suspect lines | Why. Click expands raw lines of that page with suspect highlighted and which paragraph they sit in. Why reasons: "starts with a number and a space", "bare number", "asterisk line", "paragraph over 300 words". Reasons per suspect line — the suspect start line's reason; plus long-paragraph reason.

Tab 04: check panel, repair log (collapsible), raw pages (collapsible, select + coloured lines), CSV download.

CSV: columns as specified (includes text_lines? The column list given: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, flagged, suspect_lines, repairs, citation, symbol, doc_url. Plan earlier mentions "the CSV column text_lines (lines separated by ' | ')" but the column list doesn't include text_lines; it includes text_raw. I'll use text_raw = lines joined with " | ". Good.

CSV: BOM, CRLF, quotes doubled. Filename symbol.replace(/\//g,'-') + '-paragraphs.csv'.

Header status: green dot + "n of m checks pass" or red.

Multiple documents: cards for each key with records & reference. Selecting a card re-runs pipeline. Store state per doc key; current key.

Note: pdf_text_2 also has reference — it will be processed by the same pipeline. CCPR/C/GC/32's shape: paragraphs "1." style too presumably. The pipeline is generic; fine. Reference first_words keyed by string number.

Let me now also handle "count is the string '20'" — don't rely on count.

Line numbers: original index within page's split('\n') (1-based), for reporting and raw viewer.

Now write the code. Aim for compact but complete, under ~1500 lines. Let me draft.

Structure:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style> ... </style>
</head>
<body>
<header>...</header>
<div class="layout">
 <nav class="rail" id="rail"></nav>
 <main>
  <div class="tabs" role="tablist" id="tablist"> buttons </div>
  <section id="panel-result" role="tabpanel"></section>
  ... etc
 </main>
</div>
<footer>...</footer>
<script> ... </script>
</body>
```

CSS: paper/ink per spec, accent red, green pass #1a6b3c (contrast ok on #f4f0e8? dark green yes).

JS plan:

```js
const DOCS = Object.keys(WORKSHOP_DATA).filter(k=>{const d=WORKSHOP_DATA[k];return d&&Array.isArray(d.records)&&d.reference;});
let state={}; // per key analysis
let curKey=DOCS[0];
function analyze(d){...returns {pages, paragraphs, headings, cover, repairs, checks, classes(line classification), totals...}}
```

Detailed analyze:

```js
function analyze(D){
 const symbol=D.symbol||'';
 const pages=[...D.records].sort((a,b)=>a.page-b.page).map(r=>({page:r.page, lines:String(r.text||'').split('\n')}));
 const repairs=[];
 const lineClass={}; // page+'_'+lineNo -> class
 const notes=[]; // warnings
 const pagesInfo=[];
 for(const p of pages){
   const lines=p.lines;
   let firstNonEmpty=lines.findIndex(l=>l.trim()!=='');
   // header
   let headerOK=false;
   if(firstNonEmpty>=0 && lines[firstNonEmpty].trim()===symbol.trim()){ 
     lineClass[p.page+'_'+(firstNonEmpty+1)]='header';
     repairs.push({page:p.page,target:'—',kind:'header line removed',before:lines[firstNonEmpty],after:'(removed)'});
     headerOK=true;
   } else notes.push({page:p.page,text:'first non-empty line is not the symbol'});
   // footer scan
   let end=lines.length-1;
   let removed=[];
   while(end>firstNonEmpty){
     const t=lines[end].trim();
     if(t===''){end--;continue;}
     if(/^GE\./.test(t)){class footer; repairs footer line removed; end--; continue;}
     if(/^(\d{6})( \d{6})*$/.test(t)){footer; end--; continue;}
     if(/^\d{1,3}$/.test(t)){
       const n=parseInt(t,10);
       if(n===p.page){footer (page number); repair 'footer line removed' with note? Plan: pages with a page number in the footer expected all but first. Kind "footer line removed".}
       else {footer; repair 'bare number removed from the footer';}
       end--;continue;
     }
     break;
   }
```

Wait: page 1 has no page number footer but has "GE.25-15926 (E)" and date stamp. Fine.

But careful: what if last body line (footnote text) ends with... a bare number footnote number displaced is in footer — handled. What about a footnote whose text is just a symbol "A/75/982"? Starts with 'A' → stops loop. Good.

Danger: trailing empty lines inside footer region — the loop `if(t===''){end--;continue;}` continues past empties; but once we break at a non-footer line, we've already decremented past empties — that's fine, empties are unclassified anyway (only non-empty lines classified). But careful: after continuing past empty lines, we might then remove footer lines above the empties — correct.

But subtle bug: if the page ends with empty lines and above them real paragraph text, the loop skips empties then breaks at text — fine, nothing removed.

Also mark header page info: headerOK, hasPageNumber (bare number == page found in footer).

Body lines: indices from firstNonEmpty+1 (or 0 if no header? if header not found, keep all lines but note) to end inclusive. Actually if header found at firstNonEmpty, body starts firstNonEmpty+1; else body starts 0 (and the whole page is body; note warns). Body lines with their trimmed text? Keep original text but trimmed for joining? PDF lines have no leading spaces probably; I'll use raw line but join with trim. Classification recorded for non-empty body lines.

Build bodyList = [{page, no (1-based lineNo), text}...] for non-empty lines between bodyStart and end.

Then suspect computation per page: need per page ordered body lines. I'll group: for each page, its body lines in order; find first index matching suspectStart; from there all suspect.

suspectStart tests (on the line, trimmed):
- /^\d{1,3}$/ (bare, no stop)
- /^\d{1,3} [A-Z0-9"“]/
- /^\* /

Note: "* Adopted by the Committee…" starts with "* ". Also headings could match? "7 E/2003/22…" yes. A real paragraph line starting "17 Sustainable..." matches → suspect (accepted risk).

Mark bodyline.suspect accordingly.

Then the main classification pass over concatenated bodyList as described.

paraStartFull = /^(\d{1,3})\.$/; paraStartInline=/^(\d{1,3})\. (.+)$/;
labelRe=/^([IVX]+|[A-Z])\.$/;

Note conflict: "I." is also... paraStartFull requires 1-3 digits, so no conflict.

Cover: body lines before first paragraph start that aren't headings. Hmm: my loop classifies headings whenever encountered, even before first para. The plan says "Lines before the first paragraph start are the cover." Strictly, "I." and "Introduction" before para 1 would be cover then, and section of para 1 wouldn't be set. But the found-data says headings include "I. Introduction" presumably as a labelled heading. The heading rule doesn't exclude pre-paragraph lines. I'll treat labelled headings anywhere as headings (so para 1 gets part "Introduction"), and other pre-para lines as cover. That seems most useful and consistent with "Headings found" box.

Unlabelled heading helper:
```js
function isUnlab(t){
 t=t.trim();
 if(!t||t.length>90)return false;
 if(!/^[A-Z"“]/.test(t))return false; // starts with capital letter
 if(/[.;:,]$/.test(t)||/\d$/.test(t))return false;
 return true;
}
```
"starting with a capital letter" — /^[A-Z]/. I'll use /^[A-Z]/ strictly.

endsSentence(t): /[.?!:;]\s*$/.test(t) — used for two-line join: previous line must NOT end a paragraph sentence. "does not end a paragraph sentence": if ends with '.', it does end a sentence → no join. So join only if !/[.?!]$/.test? What about ending with ':' or ','? A heading first line wouldn't end with those either typically. I'll say endsSentence = /[.?!:,;]["”')\]]?$/. If previous line ends a sentence → not part of heading. Wait but the heading line itself must pass isUnlab which already excludes those endings. The previous-line test: "passes the same test and does not end a paragraph sentence". isUnlab already excludes .;:, digit endings. So "does not end a paragraph sentence" is an extra condition — maybe previous line ends with ')' or a quote? Hmm. E.g., heading "Right to work (art. 6)" one line. The wrapping example: "the one before paragraph 73 wraps over two lines". If isUnlab excludes lines ending with ',', and a wrapped heading's first line ends without punctuation — the extra condition probably guards lines like "…rights" ending a sentence without a period? I'll implement: prev passes isUnlab AND !/[.?!]$/.test(prev) — isUnlab already covers that. Just use isUnlab for prev, plus require prev was the last line of the current paragraph (so cover lines can't be stolen... actually could a cover line join? skip). Fine.

Loop:

```js
let paras=[],cover=[],headings=[];
let cur=null, section=null, part=null, partTitle=null;
for(let i=0;i<B.length;i++){
  const ln=B[i], t=ln.text.trim();
  const mLab=labelRe.exec(t);
  if(mLab){
    // gather title
    let j=i+1, titleParts=[];
    while(j<B.length){
      const tj=B[j].text.trim();
      if(labelRe.test(tj)||paraStartFull.test(tj)||paraStartInline.test(tj))break;
      titleParts.push({ln:B[j],text:tj}); j++;
    }
    // join continuation lines: starts lowercase or (
    let title=[];
    for(const tp of titleParts){
      if(title.length && /^[a-z(]/.test(tp.text)){
        title[title.length-1]+=' '+tp.text;
        repairs.push({page:tp.ln.page,target:'—',kind:'heading title joined from two lines',before:title[title.length-2]... 
```

Hmm, before/after: before = two lines, after = joined. Store before: prevLine+' / '+tp.text? Store strings.

Wait, "a line starting with a lowercase letter or '(' continues the previous heading line (logged as 'heading title joined from two lines')" — but also "any other line is a further heading"?? "then every line up to the next label line or paragraph start is heading text; a line starting with a lowercase letter or '(' continues the previous heading line, any other line is a further heading." So the labelled heading can have multiple heading lines (title lines). E.g. "A." then "Right to work" then "(art. 6)"? Actually "(art. 6)" starts with '(' → continues. Section = the full heading text (joined). For GC27, subsections like "A. The right to work"? and sections "I. Introduction". Title for section = roman + ' ' + title.

Hmm wait, GC27 structure per sample: "I.\n\nIntroduction". So label "I.", title "Introduction". part = "I. Introduction". section = same? For subsections "A." + title. part = most recent roman heading; section = most recent heading line (labelled or unlabelled).

Edge: footnote lines between heading label and title? The while loop would swallow footnotes into title. If a page ends with "IV." and footnotes follow... possible! In GC27, headings mid-page, footnotes at foot. If "IV." is the last body line of a page, footnotes would be gathered as title. Risk accepted? That would misclassify and inflate heading. Hmm. To reduce risk: stop gathering at a suspect line? Suspect lines are computed already (per page run). I could break the title gathering at a suspect line too. That seems wise: if B[j] is suspect, break and treat remaining... but then those lines fall through to paragraph/cover handling. Let me add: break if B[j].suspect. Then the label with no title (title empty) — heading with title ''. Possible; keep, note. Actually if heading label is immediately followed by suspect (footnotes), break, title empty, section stays previous? I'd set section to label alone. Edge case; handle gracefully.

Also the unlabelled-heading lookahead shouldn't steal a suspect line: if B[i] is suspect and next is paraStart... e.g., footnote text right before next paragraph number? Footnotes are at page foot; next paragraph number is on next page after heading maybe. A footnote line could pass isUnlab? Footnote text lines start with digits mostly or are continuations... could start with capital and not end with period (wrapped footnote). Then it'd be stolen as heading. Guard: don't treat suspect lines as unlabelled headings. Add `!ln.suspect` condition. Good.

Continue loop:

```js
  if(paraStartFull.test(t)||paraStartInline.test(t)){
    // finish cur (compute text) happens later; just push marker
    let num, firstText=null;
    let mm=paraStartFull.exec(t);
    if(mm){num=+mm[1];}
    else{mm=paraStartInline.exec(t);num=+mm[1];firstText=mm[2];
      repairs.push({page:ln.page,target:num,kind:'number and text split',before:t,after:num+'. | '+firstText});}
    cur={num,page:ln.page,lines:[],parts:[]};
    if(firstText!=null) cur.lines.push({page:ln.page,no:ln.no,text:firstText,inlineSplit:true});
    paras.push(cur);
    continue;
  }
  // unlabelled heading?
  if(!ln.suspect && isUnlab(t) && i+1<B.length && (paraStartFull.test(B[i+1].text.trim())||paraStartInline.test(B[i+1].text.trim()))){
    let title=t;
    if(cur && cur.lines.length){
      const prev=cur.lines[cur.lines.length-1];
      const pt=prev.text.trim();
      if(isUnlab(pt)){
        cur.lines.pop();
        title=pt+' '+t;
        repairs.push({page:ln.page,target:cur.num,kind:'heading title joined from two lines',before:pt+' ⏎ '+t,after:title});
      }
    }
    repairs.push({page:ln.page,target:cur?cur.num:'—',kind:'heading separated from paragraph text',before:t,after:'(heading) '+title});
```

Hmm — if two-line join happened, is "heading separated" also logged? Both repairs happened conceptually. Plan lists both kinds. I'll log "heading title joined from two lines" when joining (which includes the separation), else "heading separated". Actually cleaner: if join: log join only? The repair log counts per kind; plan's example counts unknown. I'll log both when both occur (separation of the first line happened implicitly). Simpler: when join occurs, log only 'heading title joined from two lines'; else log 'heading separated from paragraph text'. Hmm but then "heading separated" count would miss one. The plan's "What I found" doesn't give counts for repairs. I'll do: always log 'heading separated from paragraph text' for the line adjacent to paragraph; additionally log 'heading title joined from two lines' when a second line was pulled. That matches "the kinds are the ones named".

Wait — if two lines are pulled, which one is "immediately followed by paragraph start"? The second. The first is pulled via the join rule. So: log 'heading title joined' for pulling the first, and 'heading separated' for the second. OK: when join: push join repair (for prev line) AND separated repair (for current line). When no join: push separated repair only.

```js
    headings.push({page:ln.page,kind:'unlabelled',title,part});
    section=title;
    lineClass[...]='heading'; also for popped prev line: 'heading';
    continue;
  }
  // default
  if(cur){cur.lines.push(ln); lineClass='paragraph';}
  else {cover.push(ln); lineClass='cover';}
}
```

Also lineClass for heading label + title lines, header, footer, cover, paragraph (suspect lines are paragraph with flag — in viewer colour them as suspect).

After loop: compute each paragraph:
- text = lines.map(l=>l.text.trim()).join(' ').replace(/\s{2,}/g,' ').trim() — wait, joining with space then collapsing doubles. Also the inline-split first line. Lines may have trailing spaces from PDF; trim each.
- count hyphen-ending lines: lines.filter(l=>/[a-z]-$/.test(l.text.trim())).length — report total.
- page_start = lines[0].page, page_end = last.page; if distinct pages set → repair 'paragraph joined across a page break' (log once per paragraph, page = page_end? use page_start, target num, before: `…${last line of first page}`, after: `${first line of next page}…`). I'll do before: '"…'+tailOfFirstPage+'"', after: '"'+headOfNextPage+'…" joined with a space'.
- word count; over300 = words>300.
- suspectLines = lines.filter(l=>l.suspect) → {page,no,text,reason}.
- flagged = suspectLines.length>0 || over300.
- first_words_found computed with mark stripping.
- first_words_reference = ref.first_words[String(num)].
- match normalised equality (if reference exists).

First-words extraction:
```js
function stripMarksFirstWords(text,n=6){
  const raw=text.split(/\s+/).filter(Boolean);
  const out=[];let prev=null;
  for(const tok of raw){
    if(out.length>=n)break;
    let t=tok;
    // digits glued to end
    t=t.replace(/\d+$/,'');
    if(/^\d+$/.test(t)){
      // bare number token
      if(prev && /[.,”")\]]$/.test(prev) && !isAbbrev(prev)) {/*drop*/ prev=tok; continue;}
      // else keep the original token? "article 2" — keep as-is
      out.push(tok); prev=tok; continue;
    }
    if(t===''){prev=tok;continue;} // token was all digits glued? e.g. "2" handled above
    out.push(t); prev=t;
  }
  return out.join(' ');
}
```

Hmm wait: "digits glued to the end of a word or a punctuation mark are cut ("waste.2" becomes "waste.")". So replace trailing digits. But "art. 2" — token "2" is bare digits; previous token "art." ends with '.' but is an abbreviation → keep. "No. 3" similar. Paragraphs starting "Article 2 of the Covenant" — "2" bare, prev "Article" doesn't end with '.' → keep. Good.

But careful: "SDGs17"? doesn't occur. Also a token like "2030" (year) — prev likely doesn't end with period → kept. Fine.

Also the cut token might become empty ("2" alone) — but that's the bare-number case; if kept, push original? If token is pure digits and prev doesn't qualify, push the token as-is (it's a real number word). But after t=t.replace(/\d+$/,''), t='' — handle: if t==='' and bare digits: apply bare rule; if drop → skip, else push tok. Yes as written.

Edge: what about footnote mark after quotes: "”. 3" — token "3" bare, prev "”." wait "”." ends with '.'? prev token is "”." hmm the example: "”. 3" → tokens "”." and "3". prev ends with '.' and is not abbreviation → drop. Good.

isAbbrev: /^(No|Nos|art|arts|para|paras|p|pp|vol|chap|sect|e\.g|i\.e|cf)\.$/i — check with trailing period. E.g. "No.", "art.". Also "General Assembly resolution 79/172" — "79/172" not bare digits. OK.

Normalise:
```js
const norm=s=>s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();
```

Checks computation:

```js
checks=[
 {name:'Paragraph count', run: found vs ref.paragraphs, pass: equal, detail}
 {name:'Numbering', ...}
 {name:'First words', ...}
 {name:'Suspect lines', report}
 {name:'Pages flagged', report}
 {name:'Headers and footers', pass: headerOK pages == all pages && page-number pages == all but first? On this file expected all / all-but-first. If not, fail with details.}
 {name:'Headings', report, pass:true}
 {name:'Nothing lost', pass: classifiedCount==totalNonEmpty}
]
```

If no reference: checks 1,3 → 'not run'.

passCount = checks.filter(pass).length; allPass = every pass (not-run counts as not pass? Header shows "n of m checks pass" green or "n checks failed" red). If reference missing, not-run checks aren't failures. I'll count: failed = checks with pass===false. Green when failed===0.

Now UI rendering. Tabs: 4 buttons, role=tablist, arrow keys. Panels hidden attr; CSS [hidden]{display:none!important}.

Rail: document cards. Click card → select doc, re-render everything.

Rendering functions per tab, re-rendered on selection. Keep expanded row state? Simplest: re-render resets expansions; acceptable. Keep track of open paragraph numbers in a Set to preserve across re-render? Re-render happens only on doc change; fine to reset. But tab switches shouldn't re-render (panels persist). Render once per doc selection.

Tab 01: four tiles.
Tab 02: headings collapsible box + table with rows.
Tab 03: rows.
Tab 04: checks list, repair log collapsible, raw pages collapsible, download button.

Copy citation: navigator.clipboard may fail in sandbox; fallback to a temp textarea + document.execCommand('copy'), then show "Copied".

studio.openSource not relevant here (pdf_text is not library). No.

Charts: none needed.

Let me also compute "count of lines ending in hyphen" reported in method/repairs summary: show in method line.

Header line: `UN DOCUMENT · PDF TEXT` label; title; line: symbol (link), adopted ref.adopted, n pages, source. Note ref.adopted may be missing → omit.

Footer: source, built date (D.built? plan says built date; pdf_text has `built`? The dataset description for uhri has built; pdf_text description lists {title, symbol, doc_url, source, count, records, reference}. I'll use D.built if present else ''. Safer: show if present.

Now write CSS. Colors: --paper #f4f0e8, --ink #1d1b18, --rule #d9d2c3, --red #9b2335, --green #1e6b3a? Contrast: #1e6b3a on #f4f0e8 ~ ok (dark green). Pale tints for viewer: cover #ece5f5? Use pale hues with letter codes C/H/P/S/F etc. Six tints: cover (lavender), header (pale blue), heading (pale yellow), paragraph (white/none), suspect (pale red), footer (grey).

Raw viewer: monospaced, line numbers left, background tint per class, letter code in margin.

Tab 03 expanded: show page's raw lines (body + everything?) with suspect highlighted and paragraph numbers. I'll show the page's lines with class colours too (reuse renderer) — plan says "shows the page's raw lines with the suspect ones highlighted and the paragraph they sit in". I'll show non-empty lines with class + para annotation.

CSV building as specified.

Table captions with serif and "TAB.01" style monospace figure numbers.

Arrow key tabs: keydown on tablist.

Let me count clickable things per tab: tab02: 4 tabs + headings box = 5 + rows. OK. Tab04: 4 tabs + repair log + raw pages + select + download = 8... plan says "Seven things to click: four tabs, the repair log and raw pages headings, and the download (the select appears once Raw pages is open)". So 7 + select = they counted 7. Fine, follow plan.

Now, writing the whole file. Let me be careful with details and keep code organized. I'll aim ~900 lines.

Paragraph row Check cell: "OK" or "first words differ" (red) or "may contain footnote text" (red, links to tab03 page). Could be both: show both lines? Priority: if first-words differ show that; also flagged. I'll show combined: join with "; ". Link to tab03 anchor.

Section column: section (nearest heading above) truncated maybe 40 chars.

Expanded row content:
- full text: render lines as spans joined by space; suspect lines wrapped in <mark class="sus">. Since text = join of trimmed lines with space, render: lines.map(l=> l.suspect? `<mark>${esc(l.text.trim())}</mark>` : esc(l.text.trim())).join(' ').
- toggle "Show the PDF's lines": reveals list of lines each prefixed with page number when page changes: "p.3 — line". Show all lines each with page marker maybe only when page changes; plan: "the same text with the converter's line breaks and the page number where each page began". So lines; when a line's page differs from previous, prefix "[page 4]".
- first words comparison block.
- repairs list for this paragraph (repairs where target===num or kind joined with target num).
- Copy citation button.

Note text uses esc() everywhere.

Tab 01 tiles: paragraphs found vs expected; pages flagged; first words match; repairs made (link opens tab04 and expands repair log).

Let me write the "How this is computed" one-liners.

Now checks details rendering: each check line: name — values — pass/failed word. Failed with link to rows: for first words mismatch link to tab02 (just switch tab). Simple: link switches to relevant tab.

Numbering check: verify paras numbers === 1..n sequence. List gaps/dupes.

Headers/footers check: pages with header OK count (expected all → pass if all); pages with page-number footer (expected all but first → pass if exactly pages.slice(1) all have it... but what if page numbering? compute: pagesWithPageNo = pages after first that had bare number == page; pass if all pages except first have it). Also list bare numbers removed.

Nothing lost: totalNonEmpty = sum over pages of non-empty lines. classified = cover+header+heading+paragraph+footer counts (from lineClass map, counting non-empty only). unclassified list = non-empty lines not in map.

Also warnings (pages where first line wasn't symbol) shown in checks.

Line class assignment: I set lineClass during processing. For paragraph lines set 'paragraph' (suspect ones 'paragraph' but with suspect flag — in viewer show as suspect tint; store class 'paragraph', flag separately in a set). For popped heading-join prev line, change its class from paragraph to heading. For inline-split first text line: class paragraph. Cover: 'cover'. Footer lines: 'footer'. Header: 'header'. Heading label + titles: 'heading'.

Raw page viewer: for selected page, iterate original lines; empty lines shown dim? Show all lines with numbers; empty lines as blank. Colour non-empty by class; unknown → red text "unclassified".

Suspect highlight in tab 03 raw lines: suspect lines tinted red + code S.

Reasons: for each suspect start line compute reason: bare number / number+space / asterisk. Store on bodyline: reason when it's the trigger. For run-lines reason 'footnote block (after a suspect line on this page)'. Store per flagged page: paragraphs affected, suspect line list.

Tab 03 row: Page | Paragraph(s) | Suspect lines count | Why (reasons of triggers + maybe long-para). Expanded: the page's lines rendered.

Also include long-paragraph pages: why "paragraph over 300 words".

Now let's also handle the "* Adopted..." cover line: it's cover and suspect → page flagged only if inside paragraph. It's cover, so doesn't flag by itself; but page 1 likely flagged from footnotes anyway. In suspect-lines check count, count all suspect lines.

Hmm wait — the page-run rule: "A suspect line and every line after it to the end of its page are suspect". If the cover "* Adopted..." triggers on page 1, everything after on page 1 (including paras 1-2) becomes suspect! That would flag paragraphs 1–2 wrongly. Hmm. But plan says on this file "on each page the first suspect line is that page's first footnote number, never a line of paragraph text". But the cover asterisk line — where does it sit? "* Adopted by the Committee..." typically appears on page 1 after the title/cover, before "I. Introduction". If it's before the first paragraph... The plan explicitly lists "* Adopted by the Committee…" as a suspect line example ("the note on the first page"). And says the first suspect line on each page is that page's first footnote number, "never a line of paragraph text". Hmm, that suggests on page 1 the first suspect is the first footnote number, meaning the asterisk line is... also suspect but maybe after? Order on page 1: cover stuff, "* Adopted..." note, then I. Introduction, para 1..., footnotes at foot. The asterisk note is before paragraphs. If it triggers the run, all page-1 body lines after it become suspect → paragraphs 1–2 flagged, first-words might still match. The plan's claim "on each page the first suspect line is that page's first footnote number" contradicts the asterisk being earlier... unless the run rule is meant only within paragraphs? Or the asterisk is among the footnotes at the foot? Actually in real UN PDFs, "* The present general comment..." — no wait, in GCs the asterisk note usually sits on page 1 near the title ("* Adopted by the Committee..."). Hmm, but this file's footnote 1 might be that asterisk note! Footnote markers use * for the first footnote sometimes? No — "141 footnotes" numbered 1-141, but page 1's note might be "*" (the adopted note). The plan says suspect rule includes "* " lines precisely because of that note, and says "the first suspect line [on each page] is that page's first footnote number, never a line of paragraph text" — maybe on page 1 the asterisk note is at the foot with the other footnotes (it's positioned at the bottom of page 1 in the PDF). Likely yes: "GE.25-15926 (E)" and date stamp in footer, and the asterisk note... Actually the plan found: "on each page the first suspect line is that page's first footnote number". If the asterisk note were above paragraphs, that claim would be false. So presumably the asterisk note sits at the foot of page 1 (it's a footnote-like note). I'll implement as specified; run rule applies from first suspect to end of page. If the asterisk is at the foot, fine.

But wait: risk — the run rule with the asterisk on page 1: if the note is at foot after footnotes, no harm.

However there's a subtlety: if the asterisk is in the cover region (before para 1), the run would mark paras 1-2 suspect. To be safer, should the run rule only apply within paragraph content? The plan: "A suspect line and every line after it to the end of its page are suspect: a footnote block runs to the foot of the page." I'll implement as written but... hmm, that could produce false flags on page 1 if the note is early. But plan asserts tested behaviour. I'll follow the spec literally; the app shows why, and a reader checks the PDF. Actually — one mitigation: apply run only from the first suspect line that is inside a paragraph? No — spec explicit. Follow spec.

Wait, actually re-reading: "Tried on this file, the suspect-line rule below flags all 20 pages (every page has footnotes), and on each page the first suspect line is that page's first footnote number". So on page 1, the first suspect is the first footnote number — meaning the asterisk note either doesn't exist on page 1 of this file or comes after. The rule includes "* " "the note on the first page" — maybe the note IS on page 1 but positioned at the foot. Either way, spec-compliant.

OK. Another subtlety: headings between suspect run lines: e.g., page ends: paragraph lines, heading "IV." at bottom? The found data says 16 paragraphs span page breaks, three pages start with a heading. So headings at page boundaries: "IV." last line of page or title first line of next page. If a page's last body line is "IV." and footnotes... no, footnotes come after. If "IV." is last line before footnotes, the footnote run marks it suspect → it's a heading classified... my label gathering would gather footnotes as title! I added break-at-suspect in title gathering. But then "IV." with empty title, and next page starts with "Introduction" which becomes... unlabelled heading? "Introduction" followed by para start → yes! It would be caught as unlabelled heading (starts capital, short, no ending period). Actually good — section = "Introduction". And part = "IV. " with empty title? I'll set part title to label only. Edge case handled reasonably.

Hmm wait, but actually if "IV." is followed by footnotes on same page, and title on next page: my loop: labelRe matches "IV." → gather: next line is footnote text (suspect) → break immediately due to suspect check → title empty. Then continue from the suspect line: it's suspect so not unlabelled heading; cur exists (previous paragraph closed? cur is last paragraph) → suspect lines get appended to previous paragraph! That's the "footnote text stays inside paragraph" behaviour — intended (flagged). Then next page "Introduction" before para start → unlabelled heading (if next line is a paragraph start). OK.

But the found data says three pages start with a heading — meaning heading label/title at top of page, i.e., previous page ended with... whatever. Fine.

Also: my unlabelled-heading guard `!ln.suspect` prevents stealing footnote text as headings. Good. And labelled gathering breaks at suspect.

One more: paraStartInline regex /^(\d{1,3})\. (.+)$/ — but heading titles could be like "2. Something"? No.

Cover lines before first paragraph: includes "Committee on Economic, Social and Cultural Rights", "General comment No. 27 (2025) on ...", title lines, date "6 November 2025", "Original: English", "Distr.: General". Also "I." "Introduction" handled as heading if before para 1? Yes per my choice. Hmm — wait, is that right? "I." appears in the sample right before "Introduction" and "1." — it's before the first paragraph start. My loop classifies it as labelled heading. Good, para 1 gets part.

Unlabelled heading test on "Introduction": next line is para start "1." → would double-handle? No: labelled gathering consumed "I." and gathered title lines until paragraph start — "Introduction" is gathered as title. Good.

But cover line "General comment No. 27 (2025) on economic, social and cultural rights and the environmental dimension of sustainable development*" — followed eventually by "I." label line, not paragraph start, so not unlabelled heading. Good — cover.

Now "Nothing lost": also count heading label/title lines, cover, paragraph, header, footer. Empty lines excluded.

Also the first non-empty line check: if symbol is empty string (missing), header check fails gracefully.

Rendering counts: "n paragraphs" big number; bar share found/reference (clamp >100%). Red when !=.

Let me now write the HTML.

Also aria: tabs with aria-selected, panels with role=tabpanel, hidden when not active; arrow keys Left/Right.

Row buttons: I'll make each row a <tr> with a button in first cell? Better: the plan says "Rows are buttons with aria-expanded". Simplest accessible: make the visible row cells inside a <tr> that has tabindex=0 role=button aria-expanded, with keydown Enter/Space. Or wrap first cell content in a button spanning... I'll do tr with role="button" tabindex="0" aria-expanded, click + Enter/Space handlers. Acceptable.

Expanded content: an extra <tr> with a colspan cell.

Let me write everything now.

CSV columns: number, section, part, page_start, page_end, first_words_reference, first_words_found, first_words_match, text, text_raw, flagged, suspect_lines, repairs, citation, symbol, doc_url.

suspect_lines format: "p.3 line 47: 7 E/2003/22… ; ..." — join with "; ". repairs: kind list "header line removed; ..." per paragraph — target-matching repairs joined "; ".

Download: Blob with \uFEFF BOM, type 'text/csv;charset=utf-8'.

Escape function for HTML.

Charts: none.

Also the status dot in header: green/red with text.

Let me write the code now, carefully.

Also note `D.count` is string "20" — use records.length.

Render helpers: h() maybe; I'll use template strings and innerHTML with esc.

State: analysis per key cached: analyses = {}.

Selected doc: currentKey.

selectDoc(key): curKey=key; render all.

Render functions: renderRail, renderHeader (title etc), renderTabs (static), renderPanels: renderResult, renderParagraphs, renderFlagged, renderChecks.

For tab02 expanded state: keep a Set openParas; row click toggles and re-renders tab02 panel only. Similarly tab03 openPages Set. Tab04: repair log open flag, raw page open flag + selected page select.

OK writing.

For the "Show the PDF's lines" toggle inside expanded paragraph: a button toggling per-paragraph; keep set showLines.

Copy: 

```js
async function copyText(s,btn){try{await navigator.clipboard.writeText(s);}catch(e){const ta=document.createElement('textarea');ta.value=s;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(_){}ta.remove();}btn.textContent='Copied';setTimeout(()=>btn.textContent='Copy citation',2000);}
```

Analysis object shape:
```
{
 symbol, title, doc_url, source, built, ref,
 pages: [{page, lines, headerOK, hasPageNo, bareRemoved:[...]}],
 body: [bodyline],
 paragraphs: [...],
 headings: [...{page,kind,title,part}],
 cover: [lines],
 repairs: [...],
 suspectTotal, suspectPages(set), flaggedPages(set), flaggedParas,
 hyphenLines, warnings,
 lineClass: Map key `${page}:${no}` -> class,
 checks: [...], passCount, failCount
}
```

Compute flagged pages: pages where a suspect line is inside a paragraph → set; plus pages of >300-word paragraphs.

Paragraph.suspectLines: lines with suspect true (with reason: trigger reason or 'later line of the footnote block on this page').

Reason for trigger line: store trigger reason on the line when computing page suspect runs.

Now checks list construction with details HTML.

Check 1 Paragraph count: found=paragraphs.length, expected=ref.paragraphs. pass equal. detail: "found X / reference Y".
Check 2 Numbering: expected sequence 1..found in order; compute issues. pass none.
Check 3 First words: mismatches count; list "para. n: found … / reference …". pass 0. If !ref.first_words → not run.
Check 4 Suspect lines: `${suspectTotal} suspect lines on ${pages} pages, inside ${paras} paragraphs; none removed`. pass true.
Check 5 Pages flagged: list "page p, para. n". pass true (report).
Check 6 Headers and footers: headerOK pages count of total; pageNo pages count of (total-1) expected; bare numbers removed listed. pass = headerAll && pageNoAll.
Check 7 Headings: labelled n, unlabelled n + list titles. pass true.
Check 8 Nothing lost: classified vs total non-empty; unclassified listed. pass equal.

Tab01 tiles:
- Paragraphs found: big n, beside "The document has: ref.paragraphs" (green equal / red with difference). Note line.
- Pages flagged: n of pages; if >0 red + note; plus "The document has ref.footnotes footnotes; this version does not separate them."
- First words match: n of ref.paragraphs.
- Repairs made: n, link to repair log.

Method one-liners per tile.

Now write. Also keep the "How this is computed" line near numbers.

Design details: serif big numbers 44px; monospace labels 11px letter-spaced uppercase.

Time to write the final file. I'll write ~950 lines. Ensure under 1500.

Let me write CSS:

```css
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#1e6b3a;--mono:ui-monospace,Menlo,Consolas,monospace;}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
a{color:var(--red)}
a:focus-visible,button:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--red);outline-offset:2px}
.mono{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
header.site{padding:20px 28px 14px;border-bottom:1px solid var(--rule)}
... layout: .layout{display:grid;grid-template-columns:250px 1fr;}
.rail{border-right:1px solid var(--rule);padding:18px}
main{padding:18px 28px}
.tabs{display:flex;gap:0;border-bottom:1px solid var(--rule)}
.tab{background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px;cursor:pointer;font-family:var(--mono);font-size:11px;letter-spacing:.1em}
.tab[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:44px;line-height:1.05}
table{border-collapse:collapse;width:100%}
th,td{padding:7px 10px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}
th{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
caption{caption-side:top;text-align:left;font-family:Georgia,serif;font-size:20px;padding:6px 0}
.fignum{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;color:#6b6459}
.pass{color:var(--green);font-weight:600}
.fail{color:var(--red);font-weight:600}
mark.sus{background:#f3d9dc;color:var(--ink)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:0}
.tile{padding:16px 18px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.how{font-size:13px;color:#5c554b}
.rowbtn{cursor:pointer}
.rowbtn:hover{background:#ede7da}
.expand td{background:#faf7f0;padding:14px 18px}
.chip{...}
```

Raw viewer tints:
- cover: #ece4f3 (lavender), code C
- header: #e3e9f0 blue, H
- heading: #f1ead6 yellow, T? use 'd'? Use letters: C, H, G, P, S, F.
- paragraph: #fbfaf7 (near paper) P
- suspect: #f3d9dc S
- footer: #e6e2da F

Legend shows swatch + code + name.

Now the JS. Careful about size. Write it.

One more detail: tab 02 table columns: No. | Section | Page | First line | Check. And "headings found: n" collapsible above.

First line: first 120 chars cut at word + '…'.

Section: paragraph.section || '—'.

Check cell: statuses; link "see tab 03" → goTab(2) and open that page.

Tab 03: build rows from flaggedPages sorted. For each page: paragraphs affected (those with suspect lines on that page, or long para on that page), suspect count, why list (trigger reasons + 'paragraph over 300 words').

Trigger reasons text: "bare number", "starts with a number and a space", "asterisk line".

Expanded: render page lines (all, with numbers), class-tinted, suspect highlighted; annotate paragraph membership: for lines in a paragraph show "¶ n" maybe. Keep: prefix line number, then class code letter, then text.

Now writing final code. Also remember: "count is the string '20'" – ignore.

Arrow keys: on tablist keydown ArrowRight/Left move focus & select.

Also panels: `hidden` on non-active; tab panel of hidden tab not focusable — hidden handles it.

Write the repair log table: Page | Paragraph | What was done | Before | After. Counts per kind above: list each kind with count. Target display: paragraph number or '—' / 'footnote'. For header/footer: target '—'. For bare number removed: target 'footnote number'? Plan: "Paragraph or footnote". I'll use 'footnote' for bare numbers, '—' otherwise, paragraph number when known.

Joined-across-break repair: page = page_start, target num, kind 'paragraph joined across a page break'.

Now finalize first_words edge: reference missing key → first_words_reference = '' and check not counted? If ref exists but key missing for a paragraph, mark mismatch? I'll mark as "no reference entry" — count as mismatch with note. Simpler: treat as mismatch with reference '(missing)'. Fine.

Let me write it all out now.

Also `built` in footer: D.built — show "built <date>" if present.

Progress on writing... produce final answer with ≤3 sentences before code block.

Let me write carefully the analyze function.

```js
function analyze(D){
  const symbol=(D.symbol||'').trim();
  const ref=D.reference||{};
  const pages=[...D.records].sort((a,b)=>a.page-b.page).map(r=>({page:r.page,lines:String(r.text==null?'':r.text).split('\n')}));
  const repairs=[];
  const warnings=[];
  const cls=new Map(); // "p:n" -> class
  const pageInfo={};
  for(const pg of pages){
    const lines=pg.lines;
    let first=-1;
    for(let i=0;i<lines.length;i++){if(lines[i].trim()!==''){first=i;break;}}
    const info={page:pg.page,headerOK:false,hasPageNo:false,first};
    if(first>=0&&symbol&&lines[first].trim()===symbol){
      info.headerOK=true;
      cls.set(pg.page+':'+(first+1),'header');
      repairs.push({page:pg.page,target:'—',kind:'header line removed',before:lines[first],after:'(line removed)'});
    }else{
      warnings.push('page '+pg.page+': first non-empty line is not the symbol');
    }
    let end=lines.length-1;
    while(end>first){
      const t=lines[end].trim();
      if(t===''){end--;continue;}
      let isFoot=false,kind=null;
      if(/^GE\./.test(t)){isFoot=true;kind='footer line removed';}
      else if(/^(\d{6})( \d{6})*$/.test(t)){isFoot=true;kind='footer line removed';}
      else if(/^\d{1,3}$/.test(t)){
        isFoot=true;
        if(parseInt(t,10)===pg.page){info.hasPageNo=true;kind='footer line removed';}
        else kind='bare number removed from the footer';
      }
      if(!isFoot)break;
      cls.set(pg.page+':'+(end+1),'footer');
      repairs.push({page:pg.page,target:kind==='bare number removed from the footer'?'footnote':'—',kind,before:t,after:'(line removed)'});
      end--;
    }
    info.bodyStart=first>=0&&info.headerOK?first+1:0;
    info.bodyEnd=end;
    pageInfo[pg.page]=info;
  }
```

Hmm: bodyStart when headerOK false → 0 (whole page is body, warning shown). Fine.

Body lines:

```js
  const B=[];
  for(const pg of pages){
    const info=pageInfo[pg.page];
    for(let i=info.bodyStart;i<=info.bodyEnd;i++){
      const t=pg.lines[i].trim();
      if(t==='')continue;
      B.push({page:pg.page,no:i+1,text:t});
    }
  }
```

Suspect runs per page:

```js
  function triggerReason(t){
    if(/^\* /.test(t))return 'asterisk line';
    if(/^\d{1,3}$/.test(t))return 'bare number';
    if(/^\d{1,3} [A-Z0-9\u201C"]/.test(t))return 'starts with a number and a space';
    return null;
  }
  const byPage={};
  for(const b of B){(byPage[b.page]=byPage[b.page]||[]).push(b);}
  for(const p in byPage){
    const arr=byPage[p];let hit=false;
    for(const b of arr){
      if(!hit){const r=triggerReason(b.text);if(r){hit=true;b.suspect=true;b.reason=r;}}
      else{b.suspect=true;b.reason='later line of this page\u2019s footnote block';}
    }
  }
```

Classification pass:

```js
  const labelRe=/^([IVX]+|[A-Z])\.$/;
  const pFull=/^(\d{1,3})\.$/;
  const pInline=/^(\d{1,3})\. (.+)$/;
  function isPS(t){return pFull.test(t)||pInline.test(t);}
  function isUnlab(t){
    if(!t||t.length>90)return false;
    if(!/^[A-Z]/.test(t))return false;
    if(/[.;:,\u2026]$/.test(t)||/\d$/.test(t))return false;
    return true;
  }
  const paras=[];const cover=[];const headings=[];
  let cur=null,section=null,part=null;
  for(let i=0;i<B.length;i++){
    const ln=B[i],t=ln.text;
    if(labelRe.test(t)){
      let j=i+1;const raw=[];
      while(j<B.length){
        const tj=B[j].text;
        if(labelRe.test(tj)||isPS(tj)||B[j].suspect)break;
        raw.push(B[j]);j++;
      }
      let title='';const parts=[];
      for(const rl of raw){
        if(parts.length&&/^[a-z(]/.test(rl.text)){
          const before=parts[parts.length-1];
          parts[parts.length-1]=before+' '+rl.text;
          repairs.push({page:rl.page,target:'—',kind:'heading title joined from two lines',before:before+' \u21B3 '+rl.text,after:parts[parts.length-1]});
          cls.set(rl.page+':'+rl.no,'heading');
        }else{parts.push(rl.text);cls.set(rl.page+':'+rl.no,'heading');}
      }
      title=parts.join(' ');
      const isRoman=/^[IVX]+\.$/.test(t);
      const labelTitle=isRoman?(t+' '+title).trim():(t+' '+title).trim();
      headings.push({page:ln.page,kind:'labelled',title:labelTitle,rawLabel:t});
      cls.set(ln.page+':'+ln.no,'heading');
      section=labelTitle;
      if(isRoman)part=labelTitle;
      i=j-1;continue;
    }
```

Wait: raw heading text may include blank? No, B has only non-empty. Also the label heading gathering could run into cover-type lines if a label appears before para 1 with other cover lines between — e.g., "A." label then something. Fine.

Issue: heading label gathering consumes lines until next label/paraStart/suspect — but what about unlabelled headings between? E.g., "A." followed by title then paragraph. Fine.

Potential problem: what if labelRe matches a line inside paragraph text? A paragraph line exactly "A." — unlikely.

Continue:

```js
    if(isPS(t)){
      let num,firstText=null;
      let m=pFull.exec(t);
      if(m)num=+m[1];
      else{m=pInline.exec(t);num=+m[1];firstText=m[2];
        repairs.push({page:ln.page,target:num,kind:'number and text split',before:t,after:num+'. | '+firstText});}
      cls.set(ln.page+':'+ln.no,'paragraph'); // the number line itself
      cur={num,section,part,lines:[]};
      if(firstText!=null){cur.lines.push({page:ln.page,no:ln.no,text:firstText});}
      paras.push(cur);continue;
    }
```

Hmm — the number-only line: it's a paragraph start line, class paragraph. Its lineNo recorded but not in cur.lines (only text lines). For "Nothing lost" it's classified. But suspect run: could a paragraph-number line be suspect? "12." has a full stop → triggerReason bare number requires no stop. "12 The..." inline would be suspect, but inline para start has "12. " with period. Good.

```js
    if(!ln.suspect&&isUnlab(t)&&i+1<B.length&&isPS(B[i+1].text)){
      let title=t;
      if(cur&&cur.lines.length){
        const prev=cur.lines[cur.lines.length-1];
        if(isUnlab(prev.text)){
          cur.lines.pop();
          title=prev.text+' '+t;
          cls.set(prev.page+':'+prev.no,'heading');
          repairs.push({page:prev.page,target:cur.num,kind:'heading title joined from two lines',before:prev.text+' \u21B3 '+t,after:title});
        }
      }
      cls.set(ln.page+':'+ln.no,'heading');
      repairs.push({page:ln.page,target:cur?cur.num:'—',kind:'heading separated from paragraph text',before:t,after:'(set as heading) '+title});
      headings.push({page:ln.page,kind:'unlabelled',title,part});
      section=title;continue;
    }
    if(cur){cur.lines.push(ln);cls.set(ln.page+':'+ln.no,'paragraph');}
    else{cover.push(ln);cls.set(ln.page+':'+ln.no,'cover');}
  }
```

Note: prev line popped — but wait, prev might have been the last line and also might be suspect (if it's footnote text before a page-break paragraph start). isUnlab check + I should also require !prev.suspect... prev.suspect check: add `&&!prevSuspect`. The popped line is from cur.lines which store {page,no,text} — I stored bodyline objects for pushed lines except inline first text. Let me store the ln object itself plus text; suspect flag accessible. For inline first text, no suspect flag (it's after "n." — could it be suspect-trigger? "23. The..." has period so no). OK, in the join check: `if(isUnlab(prev.text)&&!prev.suspect)`.

Now paragraph finalization:

```js
  let hyphenLines=0;
  for(const p of paras){
    p.textRawLines=p.lines.map(l=>l.text);
    p.text=p.textRawLines.join(' ').replace(/\s{2,}/g,' ').trim();
    hyphenLines+=p.lines.filter(l=>/[a-z]-$/.test(l.text)).length;
    p.pageStart=p.lines.length?p.lines[0].page:p.sectionPage;
```

Hmm if lines empty (paragraph number with no text before next number?) — pInline always gives text. pFull paragraph with empty lines then immediately another number — possible degenerate; guard: pageStart = first line page or the number line's page. I recorded number line page? I didn't store it. Let me store cur.startPage=ln.page and cur.numLineNo. Do that.

```js
    p.pageStart=p.lines.length?p.lines[0].page:p.startPage;
    p.pageEnd=p.lines.length?p.lines[p.lines.length-1].page:p.startPage;
    if(new Set(p.lines.map(l=>l.page)).size>1){
      // find boundary
      let lastA=null,firstB=null;
      for(const l of p.lines){if(!firstB){if(l.page!==p.pageStart){firstB=l}else lastA=l}else break;}
      repairs.push({page:p.pageStart,target:p.num,kind:'paragraph joined across a page break',
        before:'\u2026'+lastA.text,after:firstB.text+'\u2026 (joined with a space)'});
    }
    p.words=p.text?p.text.split(/\s+/).length:0;
    p.over300=p.words>300;
    p.suspectLines=p.lines.filter(l=>l.suspect).map(l=>({page:l.page,no:l.no,text:l.text,reason:l.reason}));
    p.flagged=p.suspectLines.length>0||p.over300;
    p.firstFound=firstWords(p.text);
    p.firstRef=ref.first_words?String(ref.first_words[String(p.num)]||''):'';
    p.match=ref.first_words?norm(p.firstFound)===norm(p.firstRef):null;
  }
```

Wait — inline-split first text line has no suspect flag; a paragraph whose first inline line triggers suspect? "23. The..." no. fine.

firstWords implementation:

```js
  const ABBREV=/^(no|nos|art|arts|para|paras|p|pp|vol|chap|fig|cf|sr|cedaw|crc|cat|cerd|cescr)\.$/i;
  function firstWords(text){
    const toks=text.split(/\s+/).filter(Boolean);const out=[];let prev='';
    for(const tok of toks){
      if(out.length>=6)break;
      const cut=tok.replace(/\d+$/,'');
      if(/^\d+$/.test(cut)&&prev&&/[.,\u201D")\]]$/.test(prev)&&!ABBREV.test(prev)){prev=tok;continue;}
      if(cut===''){prev=tok;continue;}
      out.push(cut);prev=cut;
    }
    return out.slice(0,6).join(' ');
  }
```

Hmm: cut==='' happens when token is all digits (covered above) — covered. Also token like "2" real number kept via out.push(cut)? If cut is digits and prev doesn't qualify, we push cut = the digits. Good.

Edge: "waste.2" → cut "waste." pushed. Good.

norm:

```js
  const norm=s=>s.replace(/[\u2018\u2019]/g,"'").replace(/[\u201C\u201D\u201E]/g,'"').replace(/[\u2013\u2014]/g,'-').replace(/\s+/g,' ').trim();
```

Counts:

```js
  const flaggedPageSet=new Set();
  for(const p of paras){
    for(const s of p.suspectLines)flaggedPageSet.add(s.page);
    if(p.over300)flaggedPageSet.add(p.pageStart);
  }
```

Hmm also long para page — use pageStart. OK.

suspect totals: suspectLines all = B.filter(b=>b.suspect). suspectPages = pages with any suspect line. suspectParas = paras with suspect lines.

Checks:

```js
  const totalNonEmpty=pages.reduce((a,pg)=>a+pg.lines.filter(l=>l.trim()!=='').length,0);
  const classCounts={cover:0,header:0,heading:0,paragraph:0,footer:0};
  let unclassified=[];
  for(const pg of pages){
    pg.lines.forEach((l,idx)=>{
      if(l.trim()==='')return;
      const c=cls.get(pg.page+':'+(idx+1));
      if(c)classCounts[c]++;else unclassified.push({page:pg.page,no:idx+1,text:l.trim()});
    });
  }
```

Numbering check: 

```js
  const numIssues=[];
  paras.forEach((p,idx)=>{if(p.num!==idx+1)numIssues.push('para. '+p.num+' at position '+(idx+1)+' (page '+p.pageStart+')');});
  // also gaps/dupes inherently
```

First-word mismatches list.

Header checks: headerOK count; expected all pages. pageNo pages: pages.slice(1) expected all hasPageNo (pages beyond first). Actually could page numbering start at 1 with no number on page 1 — expected: all but first have page number equal to page. pass = all pages except the first have hasPageNo. Hmm what if records pages not starting at 1? Generic: expect every page except the first to carry its own number. Fine.

Checks array items: {name, status:'pass'|'fail'|'notrun', line(html)}.

Now build checks:

```js
  const checks=[];
  const hasRefParas=typeof ref.paragraphs==='number';
  checks.push({
    name:'Paragraph count',
    status:hasRefParas?(paras.length===ref.paragraphs?'pass':'fail'):'notrun',
    detail:hasRefParas?('found '+paras.length+' / reference '+ref.paragraphs):'no reference in this file'
  });
  checks.push({name:'Numbering',status:numIssues.length?'fail':'pass',detail:numIssues.length?numIssues.join('; '):'paragraph numbers run 1 to '+paras.length+' in order'});
  const hasFW=!!ref.first_words;
  const fwBad=paras.filter(p=>p.match===false);
  checks.push({name:'First words',status:hasFW?(fwBad.length?'fail':'pass'):'notrun',detail:hasFW?(fwBad.length?fwBad.length+' differ: '+fwBad.map(p=>'para. '+p.num).join(', '):'all '+paras.length+' paragraphs match the reference'):'not run'});
```

Also detailed list of mismatches in check panel: show each "para. n: found … / reference …". I'll render below the check line.

```js
  checks.push({name:'Suspect lines',status:'pass',detail:suspectTotal+' suspect lines on '+suspectPageCount+' pages, inside '+suspectParaCount+' paragraphs; none removed'});
  checks.push({name:'Pages flagged',status:'pass',detail:[...flaggedPageSet].map(pg=>{...}).join('; ')});
```

For pages flagged detail: map page→paras: "page 3 (para. 12)" etc.

```js
  const headerAll=pages.every(pg=>pageInfo[pg.page].headerOK);
  const tail=pages.slice(1);
  const pageNoAll=tail.every(pg=>pageInfo[pg.page].hasPageNo);
  checks.push({name:'Headers and footers',status:(headerAll&&pageNoAll)?'pass':'fail',detail:...});
  const bareList=repairs.filter(r=>r.kind==='bare number removed from the footer');
  checks.push({name:'Headings',status:'pass',detail:labelled count+' labelled and '+unlabelled count+' unlabelled headings'+(unlabList?' \u2014 '+list:'')});
  checks.push({name:'Nothing lost',status:unclassified.length?'fail':'pass',detail:totalNonEmpty+' non-empty lines; '+sumClassified+' classified (cover '+..+', header .., heading .., paragraph .., footer ..)'+(unclassified? ' UNCLASSIFIED: '+...)});
```

Then pass/fail counts: failed = checks with status 'fail'. notRun not failed.

Now UI.

Render header: 
```
<div class="mono">UN DOCUMENT · PDF TEXT</div>
<h1 class="serif">title</h1>
<div class="meta mono-ish">symbol link · adopted X · N pages of raw converter text · source</div>
<p>What this page does...</p>
<div class="status">dot + n of m checks pass</div>
```

Rail: "DOCUMENT" heading, cards, big numbers.

Tabs & panels. Render functions.

Let me now write the full file, being economical.

For tab02 render: build rows html string; openParas Set; after innerHTML, attach listeners via event delegation on the tbody (click on tr.rowbtn or keydown).

Event delegation on panels container.

I'll write render() that fills all four panels each time selection changes, then static listeners.

Paragraph row html:

```html
<tr class="rowbtn" data-num="12" tabindex="0" role="button" aria-expanded="false">
 <td class="num">12</td><td>Right to work (art. 6)</td><td class="num">3–4</td><td>first line…</td>
 <td><span class="ok">OK</span></td>
</tr>
```

Expanded row:

```html
<tr class="expand"><td colspan="5">
 <p class="text">full text with marks</p>
 <button class="linkbtn" data-toggle-lines="12">Show the PDF's lines</button>
 <div hidden>lines…</div>
 <p class="how">Reference first words: … / Found: … — equal|different</p>
 <p>Pages 3–4 · Repairs: …</p>
 <button data-copy="12">Copy citation</button>
</td></tr>
```

Toggle lines without full re-render? Re-render simpler: re-render panel with state. I'll re-render tab02 on each toggle (data small enough, 90 rows fine).

Citation string: `${symbol}, para. ${num}`.

Tab03 rows similar pattern with data-page.

Tab04: checks list (dl or divs), repair log collapsible, raw pages collapsible with select, download button.

Raw viewer render: for page select value, lines with class lookup:

```js
function rawPageHtml(a,page){
 const pg=a.pageMap[page];
 return pg.lines.map((l,i)=>{
   const c=a.cls.get(page+':'+(i+1));
   let clsName=c||'unknown';
   ... `<div class="rl ${clsName}"><span class="ln">${i+1}</span><span class="code">${letter}</span><span class="tx">${esc(l)||'&nbsp;'}</span></div>`
 }).join('');
});
```

Letter codes: cover C, header H, heading G, paragraph P, suspect S, footer F. Note: suspect lines are class 'paragraph' in cls but flagged — check bodyline suspect: look up in a.suspectSet keyed page:no. Build suspectSet in analyze.

CSV:

```js
function csvFor(a){
 const head=['number','section','part','page_start','page_end','first_words_reference','first_words_found','first_words_match','text','text_raw','flagged','suspect_lines','repairs','citation','symbol','doc_url'];
 const rows=a.paragraphs.map(p=>[p.num,p.section||'',p.part||'',p.pageStart,p.pageEnd,p.firstRef,p.firstFound,p.match===null?'':(p.match?'TRUE':'FALSE'),p.text,p.textRawLines.join(' | '),p.flagged?'TRUE':'FALSE',p.suspectLines.map(s=>'p.'+s.page+' line '+s.no+': '+s.text).join('; '),repairsFor(a,p).map(r=>r.kind).join('; '),a.symbol+', para. '+p.num,a.symbol,a.doc_url||'']);
 const q=v=>'"'+String(v).replace(/"/g,'""')+'"';
 return '\uFEFF'+[head,...rows].map(r=>r.map(q).join(',')).join('\r\n');
}
```

repairsFor: repairs where target===p.num (number). Note kinds 'heading separated'/'heading title joined' have target = cur.num or '—'; 'paragraph joined' target num; 'number and text split' target num. Good.

Also expanded paragraph shows "the repairs that touched this paragraph" — same repairsFor list.

Download:

```js
const blob=new Blob([csv],{type:'text/csv;charset=utf-8'});
const url=URL.createObjectURL(blob);
a.href=url;a.download=(a.symbol||'document').replace(/\//g,'-')+'-paragraphs.csv';
```

Now let me also make "Repairs made" tile link open tab04 & expand repair log.

Write the final HTML. I'll now compose it fully.

Also remember the note under tab03 table about footnotes not separated.

Also "Show raw page n" select options = pages.

Focus management: on tab switch, focus stays on tab button; fine.

Let me count clickables tab02: tabs(4) + headings box(1) + rows... rows don't count. Plus per-row expansion fine. OK.

Tab04: tabs 4 + repair log 1 + raw pages 1 + select 1 + download 1 = 8 (plan said 7 counting select appearing later). OK.

Now write. I'll be thorough but concise in code.

Also need `role="tablist"` arrow-key nav:

```js
tablist.addEventListener('keydown',e=>{
 if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft')return;
 e.preventDefault();
 const tabs=[...tablist.querySelectorAll('.tab')];
 const i=tabs.indexOf(document.activeElement);
 if(i<0)return;
 const n=(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length;
 tabs[n].focus();tabs[n].click();
});
```

Panels ids: panel-0..3.

goTab(i): set aria-selected, hidden.

Let me write the document now. Also include credits? Sources consulted are guidance pages, not code copied; no licence note needed. The plan asks to follow those guidelines but we didn't copy code. I'll add a small "Method follows…" line in tab04 method text — fine without credits line (no open-licensed code/wording copied). Actually to be safe, mention Analysis Function guidance in method text as sources. That's fine.

Write final.

Also handle multiple docs: DOCS keys — pdf_text and pdf_text_2 (has reference). Cards show symbol/short title (title truncated?), adopted, pages. Order of Object.keys.

Also careful: WORKSHOP_DATA.uhri has records but no reference → excluded. gc no reference. hrc no. library no (records yes, no reference). wiki no records array? pages. OK: pdf_text, pdf_text_2.

Header status dot: green if failCount===0.

Now compose the code. I'll write it as one block. Try to keep clean.

For tile "Paragraphs found": 

```html
<div class="tile"><div class="mono">PARAGRAPHS FOUND</div>
<div class="bignum">90</div>
<div>The document has: <span class="pass|fail">90</span></div>
<p class="how">How this is computed: lines starting “12.” or “12 The …” start a paragraph; counted by this page's code.</p></div>
```

Tab captions: e.g. `<caption>90 paragraphs found, 90 expected<span class="fignum">TAB.02</span></caption>` — put fignum right-aligned in caption via float.

OK, writing final answer now. Estimate ~800 lines.

One more: "the paragraph number line" for pFull: lineClass paragraph — but in tab02 expanded "Show the PDF's lines" we show cur.lines only (text lines), not the number line. Fine, mention.

Also for paragraphs with zero lines (degenerate), text ''. firstFound ''. Fine.

Section for paragraphs: stored at creation (section/part captured). Good — but note: section may be updated by headings after; captured at paragraph start = "most recent heading above". Correct.

Headings found box: list headings with page, kind, title.

Edge: paragraphs before any heading: section null → '—'.

Now, write.

Also `built`: D.built. Footer: "Source: {source} · built {built} · Counting, splitting, matching and flagging are done by this page's code; no model was called and nothing left the browser."

Header status also shows red dot on tab 04 when failed: add class to tab 4 button (a small red dot ●). I'll add a dot span inside tab 04 label when failed.

Compose now.