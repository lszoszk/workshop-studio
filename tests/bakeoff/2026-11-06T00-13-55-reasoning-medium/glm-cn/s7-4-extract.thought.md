Build the full app per plan. Need to implement the pipeline carefully. Let me write one HTML file, ~700-900 lines.

Key pipeline:

1. records sorted by page.
2. Per page: split text into lines (split /\r?\n/). Header: first non-empty line equals symbol → drop. Otherwise warning.
3. Footer: from end, drop lines while empty, starts with "GE.", only 6-digit groups (e.g. "051125 061125" — matches /^(\d{6}(\s+\d{6})*)$/), or bare number /^\d{1,3}$/. Track page-number presence: bare number equal to page. Other bare numbers counted as "bare number removed from the footer" with page.
   Careful: loop from end skipping empty lines, but "drop lines while the line is empty, starts with GE..." — the condition includes empty. But we shouldn't keep dropping footnotes? Footnote text lines wouldn't match those patterns, so fine.
   But bare number dropped could include footnote numbers — yes intended.
4. Body lines: remaining non-header/footer lines, tagged with page. But header detection: only first non-empty line. So drop first non-empty line if equals symbol; note warning otherwise.
5. Paragraph starts: /^(\d{1,3})\.$/ or /^(\d{1,3})\. (.+)$/ on a body line.
6. Headings: labelled: /^([IVX]+|[A-Z])\.$/ — line like "I." or "A.". Then skip blank lines, collect heading lines until next label or paragraph start. A line starting lowercase or "(" continues previous heading (when collecting multi-line headings? Actually that rule: "a line starting with a lowercase letter or "(" continues the previous heading line" — for wrapped headings). Collect lines until next label or paragraph start; these are heading text lines.
7. Unlabelled heading: non-empty line immediately followed by a paragraph-start line, ≤90 chars, starts with capital, not ending with . ; : , or digit. When line before passes same test and doesn't end a paragraph sentence → two lines one heading. "does not end a paragraph sentence" — I'll check it doesn't end with "." etc already enforced... Actually the previous line passes the same test (capital start, not ending with .;:,digit, ≤90) — but "doesn't end a paragraph sentence": hmm, if it passed the same test it doesn't end with full stop. But it also must be non-empty and followed by... the test's "immediately followed by a paragraph-start" applies to the second line. So: line L is heading candidate if next line is paragraph start etc. If the line before L is also a heading candidate-ish (capital start, not ending punctuation, ≤90) and doesn't end a paragraph sentence, then both lines form the heading. I'll implement: for line i candidate (next line is para start, tests pass), check line i-1: non-empty, ≤90, starts capital, not ending .;:,digit, and doesn't end a paragraph sentence — since not ending . ; : it can't end a sentence except with "?" "!" or quote. I'll say not ending with [.?!;:,] or a closing quote. Then heading = two lines joined.

Processing approach: classify each body line once. Walk through body lines:
- if paragraph start → close heading collection, start paragraph.
- if label line → close paragraph? Start labelled heading, collect following lines as heading until next label/para start.
- else if unlabelled heading candidate → heading.
- else if we're in a paragraph and not in heading-collection → paragraph line. Lines before first paragraph start = cover. Lines after headings start etc: every non-empty body line belongs to current paragraph; blank dropped. But heading lines are excluded. So classification: cover (before first paragraph start, not heading), header/footer already removed, heading lines, paragraph lines.

Edge: after a paragraph ends (next paragraph start), a heading may come. Lines between last paragraph line and heading — shouldn't happen. Any non-empty body line that is not paragraph start, label, heading candidate, and no current paragraph → cover. Also unclassified: lines while in heading collection (labelled heading's content) are heading lines.

Implement classifier over array of lines (page-tagged):

state: current para index or null, heading mode.

```
let cover=[], headings=[], paras=[], currentHeading=null;
i loop:
 line:
 if paraStart: finish; new para {number, firstLineText}
 else if labelLine: heading collecting = true; currentLabel = match
 ...
```

Let me simplify: iterate with index i:

```
function isParaStart(l){ m=l.match(/^(\d{1,3})\. ?(.*)$/); return m && (m[2]==="" || l.match(/^\d{1,3}\. /)); }
```
Careful: /^(\d{1,3})\. (.+)$/ requires space+text; /^(\d{1,3})\.$/ alone. Note "1." alone vs "1. text". Also a body line "6 November 2025" — no full stop after number, fine.

Label: /^([IVX]+|[A-Z])\.$/.

Algorithm:

```
const cls = []; // per line: 'cover'|'heading'|'paragraph'|'label'
let para = null; let headingCollect = false; let headingLines = [];
for i in lines:
  l = lines[i].text;
  if isParaStart(l):
     headingCollect=false;
     para = {num, lines:[], pageStart:line.page,...}
     if m[2] (text on same line) push that text line into para lines? Actually text after space is first line: record it as a para line (page same).
     paras.push(para)
     cls[i]='paragraph'
     continue
  if isLabel(l):
     headingCollect=true; cls[i]='heading'; headings.push({label:l})  // start new
     continue
  if headingCollect:
     // until next label or paragraph start (handled above)
     cls[i]='heading'; append line to current labelled heading text
     continue
  if isUnlabelledHeading(i):
     // mark i (and maybe i-1) as heading
     ...
     continue
  if para: cls[i]='paragraph'; push line
  else: cls[i]='cover'
```

Unlabelled heading check: next non-empty? Plan says "immediately followed by a paragraph-start line". Take literally lines[i+1] is para start (blank lines between? probably not; keep literal but maybe check next non-empty line — plan says immediately, use next line; but safer: next non-empty line is a para start AND no blank between? I'll use next non-empty line is para start and all lines between are empty). Conditions on l: trimmed, ≤90, /^[A-Z]/, not /[.;:,0-9]$/. If lines[i-1] non-empty and passes same test and doesn't end sentence → both are heading. But careful: i-1 might already be classified as paragraph; we reclassify. Also need to avoid i-1 being a paragraph line ending mid-sentence... "does not end a paragraph sentence": if previous line doesn't end with .;: and it's a paragraph line, it's mid-sentence, so it continues the paragraph, not heading? Hmm "when the line before it passes the same test and does not end a paragraph sentence, the two lines are one heading." If the line before is part of a paragraph mid-sentence it doesn't end a sentence — then it'd be treated as heading?! That's wrong. But it "passes the same test": starts with a capital letter — mid-paragraph continuation lines rarely start with capital. And ends without punctuation — rare for paragraph line. So fine.

But heading line before it must itself not already be... e.g. i-1 could be an unlabelled heading already? Ok.

Also headings after paragraphs and before para starts. Also headings must come after previous paragraph closed: when a heading is found, the current paragraph ends (last line is the line before heading). Fine — we just stop appending.

Also heading candidates while in cover (before first para)? Possible; allow.

For each para: section = most recent heading text, part = most recent roman heading. Labelled headings with roman label → part; heading text = label? Plan: `section` nearest heading, `part` nearest roman-numbered section. Labelled heading "I." followed by line "Introduction" → heading display "I. Introduction". For lettered "A." + "Right to work..." Actually "Right to work (art. 6)" is listed as unlabelled. Whatever — store heading as string.

When is a heading "done"? At next para start / label / next heading. Unlabelled headings: text is the line(s). Labelled: label + following text lines joined.

Wait, potential problem: after labelled heading collect, blank lines skipped, lines up to next label or paragraph start are heading text — but what if there's a paragraph number... covered. But unlabelled heading within labelled heading collection? The collection stops at para start. If there's a lettered "A." then its title then paragraphs — fine.

Headings count check: number of labelled and unlabelled. Count labelled as those with roman or letter label; unlabelled as the detected ones.

Suspect lines: within paragraph lines (including the "text after number" line? Probably not, it's para start). A para line is suspect when:
- bare number /^\d{1,3}$/
- starts with one to three digits, a space and a capital letter: /^\d{1,3} [A-Z]/
- starts with UN symbol: /^[A-Z]{1,5}\/\S/ e.g. "7 E/2003/22" — that's covered by digits+space+capital... "E/2003/22" starts with capital E — yes. But also a symbol alone at line start? plan: "starts with ... a UN document symbol or a quotation mark" — patterns: "7 E/2003/22…" (digits space capital), "2 Summary for policymakers…" (digits space capital). So regex: /^\d{1,3} ([A-Z“"])/ maybe. Plus bare number. Plus /^\* /. I'll use: /^\d{1,3}$/ || /^\d{1,3} [A-Z“"]\S/ || /^\* /. Plan: "starts with one to three digits, a space and a capital letter, a UN document symbol or a quotation mark". So digits space then (capital letter | symbol | quote). Implement: /^\d{1,3} ([A-Z“'"]|[A-Z]{1,5}\/)/ — capital letter covers it. Fine.

Suspect propagation: a suspect line and every line after it to the end of its page (same page) is suspect. Note lines are page-tagged; propagation applies to subsequent lines of same paragraph with same page. But careful: the last paragraph line on a page followed by footnotes... wait — footnotes are included in body lines! Plan: footnote lines are in body (not removed). So paragraph at foot of page absorbs footnote text lines. Those lines: first footnote is bare number then blank then text; others start "7 E/2003/22…". The blank line after bare number dropped. So paragraph gets bare number line (suspect) and text lines (suspect by propagation).

But wait: after the paragraph's page ends, the next page starts with header (dropped) and body continues — possibly a continuation of the same paragraph or a new para start. Propagation stops at page end. Good.

Word count > 300 → flagged.

First words: strip footnote marks. Implement cleanWord: remove trailing digits from token when preceded by punctuation? Plan: "digits glued to the end of a word or a punctuation mark are cut ('waste.2' → 'waste.')", and a digits-only token dropped when previous token ends with . , or closing quote and isn't abbreviation like "No." "art.". So:

```
function tokens(text){ return text.split(/\s+/); }
clean: for each token:
  t = token;
  if (/^[0-9]+$/.test(t)) { if prev exists && /[.,’”")]/.test(prev) && !/(No|art|para|vol)\.$/.test(prev) → drop } else keep (real number)
  else t = t.replace(/(\p{P})\d+$/u,'$1') // "waste.2" → "waste."
```
Also digits glued after word without punctuation? "word2"? Plan says "digits glued to the end of a word or a punctuation mark" — cut trailing digits, keeping punctuation if any: t.replace(/\d+$/,'') but careful not to eat real numbers in words? "17 Sustainable" — "17" is digits-only, handled. Fine: if token has trailing digits and not all digits: t = t.replace(/\d+$/,'').

Then first six words joined with space; normalize: curly→straight, en/em dash→hyphen, whitespace collapse. Compare with reference first_words (also normalized).

Paragraph 24, 27, 46, 60 start with real numbers like "article 2" — "article" not digits. "No. 3" — token "3" digits-only, prev "No." ends with "." but is abbreviation → keep. Good.

Checks list:
1. Paragraph count found vs reference.paragraphs.
2. Numbering 1..n in order; gaps/duplicates listed.
3. First words mismatches count.
4. Paragraphs flagged: n flagged on n pages (informational).
5. Suspect lines: n on n pages in n paragraphs.
6. Headers/footers: pages with symbol header; pages with page number in footer; bare numbers removed listed.
7. Headings: counts labelled/unlabelled, list unlabelled.
8. Nothing lost: every non-empty line classified once; unclassified listed. I'll count: total non-empty original lines = header lines + footer lines + classified body (cover+heading+paragraph+label). Lines dropped as header: first non-empty line per page (if equals symbol). Footer dropped lines. Body non-empty lines all classified. Since blank lines get cls undefined, ensure each non-empty body line gets a class. In unlabelled heading two-line case, mark i-1 too. Every non-empty body line goes through one branch — the branches: paraStart, label, headingCollect, unlabelledHeading (i and i-1), para, else cover. Cover includes everything before first para. So all covered. But "unclassified" check: verify no non-empty line without class — compute counts and report pass/fail.
9. Export round trip: JSON.parse(JSON.stringify(exportRecords)).length === paras.length. Trivially true; do it anyway.

Header check green/red: n of m checks pass. Checks that "fail": paragraph count, numbering, first words, nothing lost, (round trip). Informational: flagged, suspect, headers/footers, headings — do they count as pass/fail? Plan: header line shows "n of m checks pass" green or red "n checks failed". Let me make pass/fail checks: count, numbering, first-words, nothing-lost, roundtrip (5), plus headers check pass if all pages had symbol header (and page numbers on all but first). Headings check: pass always (informational). Suspect/flagged: informational pass. I'll count total checks m and passes.

Also missing reference handling: tiles "no reference in this file", checks "not run".

Exports: JSON records with fields: symbol, paragraph, section, part, page_start, page_end, text, flagged, first_words_match, citation, doc_url, limitations, text_raw (plan mentions text_lines field for export? It says export field `text_lines` (lines separated by " | ") — the plan earlier lists JSON fields without text_lines but pipeline says "the export field `text_lines`". I'll include both `text` and `text_lines`.)

Markdown: front matter, headings as ## / ### in document order, paragraphs "**n.** text". Headings: roman → ##, lettered → ###, unlabelled → ###? Plan: "the headings as ## and ### lines in document order". I'll use roman → ##, others (lettered + unlabelled) → ###. Wait unlabelled headings like "Right to work (art. 6)" sit under lettered subsections? Hmm, in this doc "Right to work (art. 6)" might be an unlabelled heading under section. I'll do roman ##, lettered ###, unlabelled ###.

File name: symbol.replace(/\//g,'-') + '.json'/'.md'.

Tab 02: table rows as buttons with aria-expanded; expanded shows full text with suspect lines marked (thin red box — I'll wrap each original line? Text is running; for highlight, render lines: since text = lines joined with space, I can render paragraph as sequence of line spans, joined visually with space. Suspect line spans get class "suspect". Show citation copy button, reference six words vs found six. "Show the PDF's lines" toggle: shows lines with " | " or line breaks and page markers. Plan: "the same text with the converter's line breaks and the page number where each page began" — render each original line, and when page changes insert "— p. N —" marker. text_raw export: lines joined " | ".

Flagged paragraphs table on tab 01: rows: Paragraph | Page | Suspect lines | Why. Clicking opens tab 02 and expands that paragraph, highlighting suspect lines (they're already highlighted).

Tabs: role=tablist, arrow key nav, panels hidden.

Left rail: card symbol, short title, big numbers. Big numbers: paragraphs found of expected with thin bar (red when ≠); flagged count; checks pass. Short title: derive from title? Title is "General comment No. 27..." long. Use maybe title's first part? Plan says "the short title" — pdf_text has no short_title. Use title truncated? I'll show title (maybe cut at ~80 chars... just show full title, it's fine in the rail, styled smaller). Use `title` in serif small.

Header line: symbol linked, adopted reference.adopted, n pages, source. Green/red dot: pass/fail. Plus "n paragraphs flagged".

Layout: header top, then tabs row, then content: left rail + main. Rail always visible both tabs. OK.

Result tab: 4 tiles; first-words mismatch list under tiles; Take away buttons; two closed headings (Every check, Flagged paragraphs).

Seven-click limit tab 01: 2 download buttons + 2 closed headings + 4 tiles? Tiles not clickable. OK.

Citation copy: "`symbol`, para. n" — actually format "E/C.12/GC/27, para. 12". navigator.clipboard may not work in sandbox; fallback textarea+execCommand. Show "Copied".

Also hyphen-ending line count report: count lines ending with "-" and show somewhere (in checks maybe: "0 lines end with a hyphen"). Add to headings check area or its own line in Every check. I'll add as part of suspect/informational check "Line endings".

Now write code. Data access: const D = WORKSHOP_DATA.pdf_text; const R = D.reference || {}.

Counts: D.records.length pages. `built` for footer — D.built? pdf_text shape says {title, symbol, doc_url, source, count, records, reference}. Footer shows `source`, `built`. built may not exist; show if present.

CSS per studio style: paper #f4f0e8, ink #1d1b18, rules #d9d2c3, accent #9b2335, green #1e6b3a for pass.

Let me write it.

Some details:

Paragraph start regex on trimmed line. Lines from PDF have trailing spaces maybe; trim each line.

Cover: also "6 November 2025" etc.

Labelled heading collection: after label line, collect non-empty lines until next label or para start; skip blank lines. A line "starting with a lowercase letter or (" continues previous heading — meaning wrapped heading title, e.g. title wraps "General comment No. 27 (2025) on economic, social and" / "cultural rights..." — lowercase start. That's within collection anyway; the rule just means such lines belong to heading. In collection, all lines until stop are heading lines anyway. OK, so the lowercase rule is redundant; fine.

But caution: heading collection runs until next label/para start — could swallow a lot if a label appears without following paragraphs... acceptable.

Unlabelled heading detection: need "immediately followed by a paragraph-start line". Check lines[i+1] (skip empties? "immediately" — but there may be blank line between heading and paragraph number in PDF? e.g. heading then blank then "23." Let me allow skipping blank lines: next non-empty line is a para start and only blanks between). Safer.

Also ensure candidate line isn't itself... e.g. last line of a paragraph that doesn't end with punctuation and starts with capital followed by para start — plan accepts risk; heading check lists unlabelled headings so reader can spot.

Also mark i-1 as heading when it passes: previous line non-empty, ≤90, /^[A-Z]/, not ending [.];:,digit, and doesn't end a paragraph sentence (not /[.?!…]$/ plus quotes). Note i-1 might be blank → skip. But also i-1 must be adjacent (no blank between)? "the line before it" — I'll require immediate (non-blank). Also only if i-1 not already classified as heading/label... it'd be paragraph. Reclassify: remove it from paragraph lines. Implement paragraph lines as list of {page, text, suspect} refs; easier: do classification pass first, then build paragraphs from cls. Yes: first pass assigns cls per line index; second pass builds.

Structure lines array: {page, text (raw), trimmed, kind (later), empty}.

Pass 1: header removal → mark kind 'header' or warn. Footer → 'footer' (+ info). Rest body.

Pass 2 classification as described (only over body lines, all lines in one array; header/footer skipped).

Then build paragraphs: for each line cls==='paragraph', attach to current para; para start lines create para and push first text line if inline form. But inline text: text after the number is "the first line" — push as line.

Blank lines: dropped (not part of para).

page_start/page_end from first/last line pages.

Suspect: compute per line; propagation: once a suspect line found at page P, mark subsequent lines of same para with page===P as suspect. Word count.

Headings list: each with {label?, type: 'roman'|'letter'|'unlabelled', text, lineIndex, page}. Build in order; paragraphs get section/part from headings with lineIndex < para start index.

Numbering check: paras numbers should be 1..n sequential.

Now, "Nothing lost": count non-empty lines total; kinds: header, footer, cover, heading (label + heading text), paragraph. Sum equals total non-empty lines. Unclassified: body non-empty lines without kind → list. In my pass every body non-empty line gets kind; but two-line unlabelled heading marks i-1 — i-1 was possibly already kind 'paragraph'; reassign to 'heading' and it will be removed from paragraph build (build checks kind==='paragraph' at time of build, after classification completes). Good.

Wait: label line "I." — kind 'heading'. Its collected lines kind 'heading'.

Cover lines: kind 'cover'.

Total non-empty = header+footer+cover+heading+paragraph counts. Should equal. Report pass/fail.

One subtlety: heading collection started but then a paragraph start appears — fine. What about labelled heading appearing while para open — para just stops getting lines. Good.

Another: unlabelled heading detection during cover region — allowed, kind 'heading'.

Now tiles + rail numbers.

First-words comparison: ref FW = reference.first_words || {}.

Export JSON: build records. limitations: flagged? `footnotes not separated; ${suspectCount? } may sit inside this paragraph` — plan: "footnotes not separated; n may sit inside this paragraph" for flagged (n = suspect lines count in it). Else "footnotes not separated".

Markdown: iterate events in document order (headings and paragraphs interleaved by line index). Track roman headings for ## level? Actually part: roman → ##, lettered → ###, unlabelled → ###? Hmm if unlabelled under lettered, then deeper. I'll do roman ##, lettered ###, unlabelled ###. Fine.

Markdown front matter fields per plan.

Downloads: Blob + a.download, URL.createObjectURL. Filename: symbol with "/"→"-".

Tab 02 table: rows as tr with button? "Rows are buttons with aria-expanded". Make each row's first cell contain a button, or make row itself a button-like (role). Simplest: each row is a <tr> with tabindex 0 role button aria-expanded, click/Enter toggles. Expanded content in a following tr with colspan. Or expand in place within the row's second cell? Plan says expand in place. I'll do: clicking row toggles a detail row after it. But "a hidden tab panel is not focusable" — fine.

Suspect lines highlighted in expanded text: render each line as span, joined by space; suspect spans get class with thin red border.

Show PDF's lines toggle: button under expanded text; shows <pre>-ish with page markers "— page N —".

Copy citation button.

Flagged table on tab 01: rows clickable → switch to tab 02, expand paragraph, scroll to it.

Every check panel: list lines: description, values, pass/fail or info.

Arrow-key tab navigation.

Header status: green dot if all pass-checks pass, red otherwise: "n of m checks pass" or "n checks failed".

Let me now count checks:
1. Paragraph count (pass/fail)
2. Numbering (pass/fail)
3. First words (pass/fail, info listing)
4. Paragraphs flagged (info: "n paragraphs flagged on n pages, to check against the PDF") — counts as pass? I'll mark info as pass (green "pass"? Plan: "A flag is not a failure"). I'll show "pass" for these too since expected behaviour. Hmm "each check ... 'pass' in green or 'check failed'". For flagged/suspect I'll display "noted" in neutral? Plan says one line per check with pass or check failed. I'll use pass for informational ones (they ran as expected).
5. Suspect lines (info)
6. Headers and footers: pass if all pages had symbol header and page-number on all but first; else check failed with page list. Also list bare numbers removed.
7. Headings (info, list unlabelled)
8. Line endings (hyphen count, info)
9. Nothing lost (pass/fail)
10. Export round trip (pass/fail)

If no reference: checks 1,3 "not run".

Now write. Aim ~900 lines. Let me write the HTML carefully.

Data details: symbol "E/C.12/GC/27". Adopted: reference.adopted like "6 November 2025" presumably (a date string). Show "adopted X".

Let me write code now.

Suspect regexes:
```
function isSuspectLine(t){
  if(/^\d{1,3}$/.test(t)) return true;
  if(/^\d{1,3} [A-Z“'"]/.test(t)) return true;  // capital, symbol (E/...), or quote
  if(/^\* /.test(t)) return true;
  return false;
}
```
Hmm "starts with ... a UN document symbol or a quotation mark" — the symbol follows digits+space ("7 E/2003/22"). Capital letter covers "E". Quote mark "“" also. Good.

Also could a footnote start like "3See A/..." (no space)? Not per plan. Skip.

First-words cleaning:

```
function firstWords(text, n=6){
  let toks = text.split(/\s+/);
  const out = [];
  for(let i=0;i<toks.length && out.length<n;i++){
    let t = toks[i];
    if(/^\d+$/.test(t)){
      const prev = out.length? out[out.length-1] : toks[i-1];
      if(prev && /[.,;’”"')]/.test(prev.slice(-1)) && !/\b(No|art|para|vol|chap|p)\.$/i.test(prev)) continue; // drop footnote number
      out.push(t); continue;
    }
    t = t.replace(/\d+$/,''); // digits glued at end
    if(!t) continue;
    out.push(t);
  }
  return out.join(' ');
}
```
Wait prev for i=0: no prev, keep. Also prev should be the *cleaned previous token* — use out last. But footnote numbers typically appear after punctuation mid-text; first words rarely have them. Fine.

Edge: "waste.2" → replace trailing digits → "waste." good. Token "2" after "No." kept.

Normalize compare:
```
function norm(s){return s.replace(/[’‘]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/\s+/g,' ').trim();}
```

Now build.

Rail numbers: paragraphs found big, "of reference.paragraphs"; thin bar width = found/expected. Red when found!==expected or no ref.

Flagged big number red if >0.

Checks big-ish number "n of m".

Header right: dot + "n of m checks pass" green if all pass else red "n checks failed"; then "· n paragraphs flagged".

Tiles:
- Paragraphs found: n, beside "the document has X". green when equal.
- First words match: n of X.
- Paragraphs flagged: n of found, on n pages.
- Footnotes: "not separated" text; document has X.

Mismatch list under tiles when differing: "para. n: found "…" / reference "…"".

Now writing the full file. Keep under limits. Also `[hidden]{display:none!important}`.

Tab 02 "Headings found: n" closed box lists headings.

Write JS functions: parse(), render functions.

For table caption messages with counts.

Let me write it all.

Keyboard tab nav:
```
tabs.forEach((t,i)=>{t.addEventListener('keydown',e=>{ if(e.key==='ArrowRight'||e.key==='ArrowLeft'){...focus+activate}})})
```

Copy:
```
function copyText(s,btn){ if(navigator.clipboard){navigator.clipboard.writeText(s).then(...).catch(fallback)} else fallback(); }
fallback: textarea execCommand.
```

Flagged row click: activate tab 02, expand para, scrollIntoView.

Suspect lines list per flagged para for table: count and first example? Table columns: Paragraph | Page | Suspect lines (count) | Why (reasons joined). Reasons: for first suspect line: classify ("bare number", "starts with a number and a space", "asterisk note"). Plus "paragraph over 300 words".

OK, writing now. I'll be careful with the paragraph-start inline case: /^(\d{1,3})\. (.+)$/ — must ensure it's not e.g. "5. The" yes. But also "1." alone matches first regex. Also avoid matching things like "art. 2"? Line "art. 2" doesn't start with digits. Good. Avoid "2025. Something"? \d{1,3} limits to ≤3 digits. Good.

Label: /^([IVX]+|[A-Z])\.$/ — but "I." also could be... fine. Note: paragraph numbers use digits, labels use letters — no conflict. But wait: uppercase letter label "A." — a line "A." alone. OK.

Careful: inline paragraph start "23. The Committee..." — also label regex? No, digits.

Potential conflict: line "I." vs roman label fine.

Heading text collection: after label, skip blank lines, collect until next label or para start. But what if there's an unlabelled heading between label and paragraph? E.g. "A." then blank then "Right to work (art. 6)" then "23. ..." — the unlabelled heading line gets absorbed as label's heading text. Hmm. In this doc, lettered subsections have their titles as text after label; the unlabelled ones are separate. Per plan, the collection rule stands. Fine.

Order of checks in classification loop matters: para start first, then label, then headingCollect, then unlabelled, then para/cover.

For unlabelled two-line: when detecting at i, also check i-1 line (must be directly before, non-empty, classified as paragraph or cover/heading? require kind not set to heading already? If i-1 is already 'heading' (part of another heading) leave). Require kind of i-1 is undefined so far? In a single forward pass, i-1 kind assigned already (paragraph or cover). Condition: passes test and not ending sentence. Then set kind[i-1]='heading', and if it was paragraph line, it's removed at build. Good.

Also must not treat the label's own text line... whatever.

Also: unlabelled heading candidate itself might currently be inside headingCollect — no, headingCollect checked first.

Edge: "at most 90 characters" — use trimmed length.

Now paragraph text: join line texts with ' ', collapse double spaces, trim.

text_raw: lines joined " | ".

Let me write the whole thing.

For the bar in rail: div with inner width %.

Also status of header/footer check: pagesWithHeader (first non-empty === symbol), pagesWithPageNumber (bare number === page found in footer). Expected: header all pages; page number pages 2..N.

Bare numbers removed list: {page, value}.

Count suspect lines overall, pages, paragraphs.

Now write. Also handle empty records / no paragraphs: tab01 says so, exports disabled.

Markdown heading levels: track whether a roman heading open... simpler: type roman → '##', lettered → '###', unlabelled → '###'.

Export "extracted": today's date new Date().toISOString().slice(0,10).

JSON pretty-print 2 spaces.

Filename: (symbol||'document').replace(/\//g,'-').

Let me also include section/part in tab 02 rows: nearest heading; expanded shows full path part › section.

Write CSS: rail width 260px, grid layout main.

Let me draft the file.

Also "How this is computed" line near every chart/number: tiles each have one; rail numbers small hint.

Alright, code:

I'll write compactly but complete. Estimate ~800 lines. Go.

One more: header label "UN DOCUMENT · PDF TEXT". Footer: source, built, disclaimer.

Tabs: `01 RESULT · 02 PARAGRAPHS`.

Flagged paragraphs panel table columns: Paragraph | Page | Suspect lines | Why. Note above.

Every check panel: lines like:
"Paragraph count — found 90, reference 90 — pass".

Let me write JS carefully.

```js
const D = window.WORKSHOP_DATA.pdf_text || {};
const R = D.reference || {};
const SYM = D.symbol || '';
const records = (D.records||[]).slice().sort((a,b)=>a.page-b.page);
```

Parse:

```js
const lines = []; // {page, raw, t, empty}
const pageInfo = []; // per page {headerDropped, pageNumberFound, bareNumbers:[]}
for(const rec of records){
  const rawLines = String(rec.text||'').split(/\r?\n/);
  // header: first non-empty
  let firstNonEmpty = rawLines.findIndex(l=>l.trim()!=='');
  let headerOk = firstNonEmpty>=0 && rawLines[firstNonEmpty].trim()===SYM;
  // footer
  let end = rawLines.length-1;
  let pageNumberFound=false; let bare=[];
  while(end>=0){
    const t = rawLines[end].trim();
    if(t===''){end--; continue;}
    if(t.startsWith('GE.')){end--; continue;}
    if(/^\d{6}(\s+\d{6})*$/.test(t)){end--; continue;}
    if(/^\d{1,3}$/.test(t)){
      if(Number(t)===rec.page) pageNumberFound=true; else bare.push(Number(t));
      end--; continue;
    }
    break;
  }
  // body lines: indices (firstNonEmpty+1 .. end) if headerOk else (firstNonEmpty..end)
  ...
}
```

If header not ok (first non-empty != symbol): warning; body starts from firstNonEmpty (don't drop). Note header kind none.

Bare numbers: they're footnote numbers removed. But careful: what if page number appears as footer AND also another bare number... covered.

Wait: also date stamp "051125 061125" = two 6-digit groups — regex handles.

Hmm: is the page-number check right? On page 1 footer has "GE.25-15926 (E)" and date stamp. On other pages "GE.25-15926" and page number. Good.

Body lines with global index for classification.

Classification:

```js
const body = []; // {gi, page, t, kind}
```

Then loop j over body:

```js
let headingCollect=false;
let curLabel=null;
let cls = new Array(body.length).fill(null);
for(let j=0;j<body.length;j++){
  const L = body[j];
  const t = L.t;
  if(!t){continue;} // blank: unclassified, not counted (non-empty only)
  let m;
  if(m = t.match(/^(\d{1,3})\.$/) || null){ ... }
```

Actually handle: 
```js
let psNum=null, psText=null;
let m1 = t.match(/^(\d{1,3})\.$/);
let m2 = t.match(/^(\d{1,3})\. (\S.*)$/);
```
m2 requires space then text starting non-space. Note m1 case text empty.

Label: /^([IVX]+|[A-Z])\.$/.

Unlabelled candidate for line j: next non-empty body line (k>j, blanks between) is para start; t length<=90; /^[A-Z]/; !/[.;:,\d]$/. Wait "not ending with a full stop, semicolon, colon, comma or digit" — so not /[.;:,\d]$/.

prev line j-1: if exists, t non-empty, same tests (≤90, capital, not ending punct), and not ending sentence !/[.?!;:,…’”"']$/ (doesn't end a paragraph sentence — but the same test already excludes .;:,digit; exclude also ? ! and closing quotes). Hmm if it passes "same test" it already doesn't end .;:,digit. Additional "does not end a paragraph sentence": exclude ? ! and quotes. So condition: !/[.?!;:,…’”"')\d]$/ roughly. Fine.

Then heading record.

Build headings array during pass: each heading {index:j, type, text}. For labelled: label line j is start; text lines are subsequent collected ones; text = label + ' ' + collected.join(' ')? Display "I. Introduction". For roman type. For lettered "A." + title.

But heading completion: for labelled, text collected over following lines until stop; but the heading object is created at label; subsequent lines appended. If another label comes, new heading.

For unlabelled: heading {type:'unlabelled', text: one or two lines joined}.

Paragraph build after pass:

```js
const paras=[];
let cur=null;
for(let j=0;j<body.length;j++){
  const L=body[j]; if(!L.t||L.kind!=='paragraph') continue;
  // para start stored as body[j].paraStart = number, and .firstText
  if(L.paraStart!=null){ cur={num:L.paraStart, lines:[], startIdx:j}; if(L.firstText) cur.lines.push({page:L.page, t:L.firstText}); paras.push(cur);}
  else if(cur){ cur.lines.push({page:L.page,t:L.t}); }
}
```

Then for each para: text, pageStart/End, section/part from headings with index < para.startIdx (use last heading). Suspect: iterate lines; propagation per page.

Suspect computed at line level: body[j].suspect boolean, then in para lines use. But para start inline text line: firstText — could be suspect? Unlikely; skip.

Compute:
```js
for(const p of paras){
  let flag=false; let reasons=[]; let nSus=0;
  let susPage=null;
  for(const ln of p.lines){
    let s = isSuspect(ln.t);
    if(susPage===ln.page) s=true;
    if(s){ if(susPage===null){susPage=ln.page; reasons.push(reasonFor(ln.t));} nSus++; }
    else if(susPage!==null && ln.page!==susPage){ susPage=null; }
    ln.suspect=s;
  }
```
Hmm propagation: "A suspect line and every line after it to the end of its page are suspect". So once suspect at page P, all following lines with page===P suspect. Lines on later pages reset (not suspect unless new suspect). My logic: keep susPage until page changes; when page changes reset susPage=null. Correct.

Word count >300: words = text.split(/\s+/).length. If >300 flag + reason.

p.flagged = nSus>0 || words>300.

Headings found count includes labelled & unlabelled.

Nothing lost: total non-empty lines across all pages; kinds count: header (only when dropped), footer (dropped lines count, including empties? no, non-empty only), cover, heading, paragraph. Blank lines unclassified, fine. Sum should equal. Unclassified = non-empty body lines with kind null — should be zero; but wait: body lines after classification: every non-empty body line gets kind in pass? In the pass loop, if !t continue (blank). Else branches assign kind to j... but the two-line unlabelled assigns to j-1 which was assigned. All non-empty get kind: paraStart→'paragraph', label→'heading', headingCollect→'heading', unlabelled→'heading' (and j-1), else para?→'paragraph', else 'cover'. Yes all assigned. Also blank lines inside heading collection skipped — they remain null but empty. OK. Nothing-lost check passes trivially but computed honestly.

Hmm but header when headerOk false: the first non-empty line isn't dropped and becomes body line (kind cover/heading/paragraph). Then "non-empty lines" counts still balance. Fine.

First words: compute per para; match = norm(fw)===norm(ref). first_words_match boolean; if no ref → null ("not run").

Mismatch list.

Now render. I'll write render functions producing HTML strings + event wiring.

Time to write the file. Also need aria: tablist etc.

Let me write final HTML.

Also detail: rail "n paragraphs of reference.paragraphs" — if no ref: "no reference in this file".

For flagged paragraphs tab01 table "Suspect lines" column: count; "Why": reasons list.

Check panel lines construction with pass/fail and links: "check failed" red with link to rows concerned — for paragraph count mismatch link to tab 02; for first words link to tab02. Simple: link switches tab.

Alright — writing.

For downloads of markdown headings order: build events array merging headings and paras by index (heading.index vs para.startIdx).

I'll now write the code block. Keep organized.

Also "short title" in rail card: use title but style small; maybe take part before "on " ? Just show full title small serif.

Let me write.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--green:#1e6b3a;--mono:ui-monospace,Menlo,Consolas,monospace;}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",system-ui,sans-serif}
a{color:var(--accent)}
a:focus,button:focus,[tabindex]:focus{outline:2px solid var(--accent);outline-offset:2px}
.mono{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
header.top{border-bottom:1px solid var(--rule);padding:14px 24px 12px}
...
```

I'll write it fully now in the answer. Keep ~; fine.

Details for tab 02 table: columns No. | Section | Page | First line | Check. Row click expands detail row. Use <tbody> rows.

Implement expandable: each paragraph gets `<tr class="prow" data-i tabindex="0" role="button" aria-expanded="false">` and detail `<tr class="pdetail" hidden>`.

Flagged row click on tab01: goto tab 02, expand, scroll.

Time to just write it.

For "Show the PDF's lines" toggle in detail: button toggling a div showing lines with page markers.

Copy citation button.

OK writing final answer now. Also three sentences before code block, nothing after.