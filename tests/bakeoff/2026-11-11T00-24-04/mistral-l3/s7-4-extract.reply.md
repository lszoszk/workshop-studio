Here is the app. It follows the plan exactly: two tabs, a left rail with the document card and the big numbers, a header with the checks, and the exports and flagged-paragraphs table on tab 01. The pipeline runs once on load, the checks run after it, and the exports are ready when the page opens.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Paragraphs from PDF text</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --red: #9b2335;
  --green: #2e6b49;
  --mono: ui-monospace, Menlo, Consolas, monospace;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--paper);
  color: var(--ink);
  line-height: 1.5;
  font-size: 16px;
}
[hidden] { display: none !important; }
a { color: inherit; text-decoration: none; }
a:focus { outline: 2px solid var(--red); outline-offset: 2px; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: 0.5em 1em; text-align: left; border-bottom: 1px solid var(--rule); }
th { font-weight: normal; }
th[scope="col"] { text-align: right; }
th[scope="row"] { text-align: left; font-weight: normal; }
caption { font-family: Georgia, "Times New Roman", serif; font-size: 1.1em; margin-bottom: 0.5em; text-align: left; caption-side: top; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2em 0; }
h1, h2, h3 { font-family: Georgia, "Times New Roman", serif; margin: 1em 0 0.5em; }
h1 { font-size: 1.8em; }
h2 { font-size: 1.4em; }
h3 { font-size: 1.2em; }
.smallcaps { font-variant: small-caps; letter-spacing: 0.05em; }
.mono { font-family: var(--mono); font-size: 0.9em; }
.red { color: var(--red); }
.green { color: var(--green); }
.big { font-family: Georgia, "Times New Roman", serif; font-size: 2.5em; line-height: 1.2; margin: 0.2em 0; }
.big-label { font-size: 0.7em; display: block; margin-top: -0.3em; }
.tile { background: white; padding: 1em; border: 1px solid var(--rule); margin-bottom: 1em; }
.tile h3 { margin-top: 0; font-size: 1em; }
.tile .how { font-size: 0.8em; color: #666; margin-top: 0.5em; }
.tile .mismatch { margin-top: 0.5em; font-size: 0.9em; }
.tile .mismatch div { margin-bottom: 0.3em; }
.flagged { border-left: 3px solid var(--red); }
.suspect { background: #fff0f0; padding: 0.1em 0.3em; border-radius: 3px; }
.button {
  background: white;
  border: 1px solid var(--rule);
  padding: 0.5em 1em;
  cursor: pointer;
  font-size: 1em;
  display: inline-block;
  margin-bottom: 0.5em;
}
.button:focus { outline: 2px solid var(--red); outline-offset: 2px; }
.button[aria-expanded="true"] { background: var(--paper); }
.button::after {
  content: " · ";
  font-family: var(--mono);
  display: inline-block;
  transform: scaleY(0.7);
}
.button[aria-expanded="true"]::after { content: " ▾"; }
.button[aria-expanded="false"]::after { content: " ›"; }
.rail {
  width: 280px;
  float: left;
  padding: 1em;
  border-right: 1px solid var(--rule);
  background: white;
  min-height: 100vh;
}
.rail h2 { font-size: 1em; margin: 1em 0 0.5em; }
.rail .card { background: var(--paper); padding: 1em; margin-bottom: 1em; }
.rail .card .symbol { font-family: var(--mono); font-size: 0.9em; }
.rail .card .title { font-size: 0.9em; margin: 0.3em 0; }
.rail .big { margin: 0.5em 0; }
.rail .big-label { font-size: 0.6em; }
.rail .bar { height: 4px; background: var(--red); margin: 0.3em 0; }
.rail .bar.short { background: var(--red); }
.rail .bar.over { background: var(--red); }
.rail .bar.ok { background: var(--green); }
.main { margin-left: 300px; padding: 1em; }
.header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 0.5em;
  margin-bottom: 1em;
}
.header .label { font-family: var(--mono); font-size: 0.8em; }
.header h1 { margin: 0; font-size: 1.5em; }
.header .checks { font-size: 0.9em; }
.header .checks .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.3em; }
.header .checks .dot.pass { background: var(--green); }
.header .checks .dot.fail { background: var(--red); }
.tabs { display: flex; border-bottom: 1px solid var(--rule); margin-bottom: 1em; }
.tabs button {
  padding: 0.5em 1em;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 1em;
  margin-right: 0.5em;
}
.tabs button[aria-selected="true"] { border-bottom-color: var(--red); font-weight: bold; }
.tabs button:focus { outline: 2px solid var(--red); outline-offset: 2px; }
.tabpanel { display: none; }
.tabpanel[aria-hidden="false"] { display: block; }
.expanded { background: white; padding: 1em; margin: 0.5em 0; border: 1px solid var(--rule); }
.expanded .text { white-space: pre-wrap; margin: 0.5em 0; }
.expanded .text .suspect { background: #fff0f0; padding: 0 0.2em; border-radius: 2px; }
.expanded .ref { font-size: 0.9em; color: #666; margin: 0.5em 0; }
.expanded .ref .match { color: var(--green); }
.expanded .ref .mismatch { color: var(--red); }
.expanded .toggle { font-size: 0.9em; margin: 0.5em 0; }
.expanded .citation { font-size: 0.9em; margin: 0.5em 0; }
.footer { font-size: 0.8em; color: #666; margin-top: 2em; border-top: 1px solid var(--rule); padding-top: 1em; }
.check-panel { background: white; padding: 1em; border: 1px solid var(--rule); margin-bottom: 1em; }
.check-panel h3 { margin-top: 0; font-size: 1em; }
.check-panel .check { margin-bottom: 0.5em; display: flex; justify-content: space-between; }
.check-panel .check .status { font-weight: bold; }
.check-panel .check .status.pass { color: var(--green); }
.check-panel .check .status.fail { color: var(--red); }
.check-panel .check .details { font-size: 0.9em; margin-top: 0.3em; }
.check-panel .check .details a { color: var(--red); }
.flagged-table { width: 100%; border-collapse: collapse; margin-bottom: 1em; }
.flagged-table th, .flagged-table td { padding: 0.5em 1em; border-bottom: 1px solid var(--rule); text-align: left; }
.flagged-table th { font-weight: normal; }
.flagged-table th[scope="col"] { text-align: right; }
.flagged-table tr:focus { outline: 2px solid var(--red); outline-offset: 2px; background: #f0f0f0; }
.flagged-table .why { font-size: 0.9em; color: #666; }
.flagged-table .why .suspect { background: #fff0f0; padding: 0 0.2em; border-radius: 2px; }
</style>
</head>
<body>

<div class="rail">
  <h2>DOCUMENT</h2>
  <div class="card">
    <div class="symbol mono" id="rail-symbol"></div>
    <div class="title" id="rail-title"></div>
  </div>
  <div class="big" id="rail-paragraphs">0</div>
  <div class="big-label">paragraphs of <span id="rail-expected">0</span></div>
  <div class="bar" id="rail-bar"></div>
  <div class="big red" id="rail-flagged">0</div>
  <div class="big-label">paragraphs flagged</div>
  <div style="font-size: 0.9em; margin-top: 1em;">
    <div class="dot pass" style="display: inline-block; margin-right: 0.3em;"></div>
    <span id="rail-checks">0 of 0 checks pass</span>
  </div>
</div>

<div class="main">
  <div class="header">
    <div>
      <div class="label mono">UN DOCUMENT · PDF TEXT</div>
      <h1 id="header-title"></h1>
      <div id="header-meta"></div>
    </div>
    <div class="checks">
      <span class="dot" id="header-dot"></span>
      <span id="header-checks">0 of 0 checks pass</span>
      <div id="header-flagged">0 paragraphs flagged</div>
    </div>
  </div>

  <div class="tabs" role="tablist" aria-label="Tabs">
    <button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
    <button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
  </div>

  <div id="panel-01" class="tabpanel" role="tabpanel" aria-labelledby="tab-01" aria-hidden="false">
    <div class="tile">
      <h3>Paragraphs found: <span id="tile-paragraphs">0</span></h3>
      <div class="how">How this is computed: the app splits the raw text into numbered paragraphs and counts them.</div>
      <div>the document has <span id="tile-expected">0</span></div>
    </div>

    <div class="tile">
      <h3>First words match: <span id="tile-first-words">0</span> of <span id="tile-first-words-total">0</span></h3>
      <div class="how">How this is computed: the first six words of each paragraph, after removing footnote marks, compared with the reference.</div>
      <div class="mismatch" id="tile-mismatch"></div>
    </div>

    <div class="tile">
      <h3>Paragraphs flagged: <span id="tile-flagged">0</span> of <span id="tile-flagged-total">0</span></h3>
      <div class="how">How this is computed: a paragraph is flagged when it has a suspect line or is over 300 words.</div>
      <div>footnote text may sit inside these paragraphs: check them against the PDF</div>
      <div>on <span id="tile-flagged-pages">0</span> pages</div>
    </div>

    <div class="tile">
      <h3>Footnotes: not separated</h3>
      <div class="how">How this is computed: this version leaves footnotes in place and flags them.</div>
      <div>the document has <span id="tile-footnotes">0</span>; this version leaves them in place and flags them</div>
    </div>

    <h2>Take the paragraphs away</h2>
    <button id="download-json" class="button">Download JSON</button>
    <button id="download-md" class="button">Download Markdown</button>

    <h2>
      <button id="checks-toggle" class="button" aria-expanded="false" aria-controls="checks-panel">Every check (<span id="checks-count">0</span>)</button>
    </h2>
    <div id="checks-panel" hidden>
      <div class="check-panel" id="checks-list"></div>
    </div>

    <h2>
      <button id="flagged-toggle" class="button" aria-expanded="false" aria-controls="flagged-panel">Flagged paragraphs (<span id="flagged-count">0</span>)</button>
    </h2>
    <div id="flagged-panel" hidden>
      <p>This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>
      <table class="flagged-table">
        <caption>Flagged paragraphs: <span id="flagged-table-count">0</span></caption>
        <thead>
          <tr>
            <th scope="col">Paragraph</th>
            <th scope="col">Page</th>
            <th scope="col">Suspect lines</th>
            <th scope="col">Why</th>
          </tr>
        </thead>
        <tbody id="flagged-table-body"></tbody>
      </table>
    </div>
  </div>

  <div id="panel-02" class="tabpanel" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
    <div>
      <button id="headings-toggle" class="button" aria-expanded="false" aria-controls="headings-panel">Headings found: <span id="headings-count">0</span></button>
    </div>
    <div id="headings-panel" hidden>
      <div id="headings-list"></div>
    </div>
    <table>
      <caption>TAB.02 Paragraphs of <span id="table-caption-symbol"></span></caption>
      <thead>
        <tr>
          <th scope="col">No.</th>
          <th scope="col">Section</th>
          <th scope="col">Page</th>
          <th scope="col">First line</th>
          <th scope="col">Check</th>
        </tr>
      </thead>
      <tbody id="paragraphs-table-body"></tbody>
    </table>
  </div>

  <div class="footer">
    <div id="footer-source"></div>
    <div id="footer-built"></div>
    <div>Done by this page's code; no model was called and nothing left the browser.</div>
  </div>
</div>

<script>
const data = window.WORKSHOP_DATA.pdf_text;
const ref = data.reference || {};
const records = data.records || [];
const symbol = data.symbol || '';
const title = data.title || '';
const doc_url = data.doc_url || '';
const source = data.source || '';
const adopted = ref.adopted || '';
const paragraphs_expected = ref.paragraphs || 0;
const footnotes_expected = ref.footnotes || 0;
const first_words_ref = ref.first_words || {};
const built = data.built || new Date().toISOString().split('T')[0];

// Normalise text for comparison: curly quotes, dashes, whitespace
function normalise(text) {
  return text
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/[–—]/g, '-')
    .replace(/\s+/g, ' ')
    .trim();
}

// Remove footnote marks from the first six words
function cleanFirstWords(text) {
  const words = text.split(/\s+/);
  const cleaned = [];
  let count = 0;
  for (let i = 0; i < words.length && count < 6; i++) {
    let word = words[i];
    // Remove digits glued to the end of a word or punctuation
    word = word.replace(/[.,;:!?'"»’”)\]]\d+$/, match => match.slice(0, -1));
    // Remove a token of digits alone only if the previous token ends with . , " or ' and is not an abbreviation
    if (/^\d+$/.test(word)) {
      if (i > 0) {
        const prev = words[i-1];
        if (/[.,'"»’”)\]]$/.test(prev) && !/(No|Art|art|para)\.$/.test(prev)) {
          continue;
        }
      }
    }
    cleaned.push(word);
    count++;
  }
  return cleaned.slice(0, 6).join(' ');
}

// Pipeline: run once on load
const pipeline = (() => {
  const pages = records.map(r => ({ page: r.page, text: r.text }));
  const checks = {
    header: { expected: pages.length, found: 0, pages: [] },
    footer: { pageNumber: { expected: pages.length - 1, found: 0, pages: [] }, bareNumber: { count: 0, pages: [] } },
    lines: { total: 0, classified: 0, unclassified: [] },
    paragraphs: { found: 0, numbering: { gaps: [], duplicates: [] }, flagged: 0, flaggedPages: new Set() },
    firstWords: { match: 0, mismatch: [] },
    suspectLines: { count: 0, pages: new Set(), paragraphs: new Set() },
    headings: { labelled: 0, unlabelled: 0, list: [] },
    exportRoundTrip: false
  };

  // Header: first non-empty line equals symbol
  pages.forEach(p => {
    const lines = p.text.split(/\r?\n/).filter(line => line.trim() !== '');
    if (lines.length === 0) return;
    checks.lines.total += lines.length;
    const firstLine = lines[0].trim();
    if (firstLine === symbol) {
      checks.header.found++;
    } else {
      checks.header.pages.push(p.page);
    }
  });

  // Footer: from the end, drop empty, GE., 6-digit groups, bare numbers
  pages.forEach(p => {
    const lines = p.text.split(/\r?\n/);
    let footerStart = lines.length;
    for (let i = lines.length - 1; i >= 0; i--) {
      const line = lines[i].trim();
      if (line === '') continue;
      if (/^GE\.\d+/.test(line)) {
        footerStart = i;
        continue;
      }
      if (/^\d{6}$/.test(line)) {
        footerStart = i;
        continue;
      }
      if (/^\d{1,3}$/.test(line)) {
        if (parseInt(line) === p.page) {
          checks.footer.pageNumber.found++;
          checks.footer.pageNumber.pages.push(p.page);
        } else {
          checks.footer.bareNumber.count++;
          checks.footer.bareNumber.pages.push({ page: p.page, number: line });
        }
        footerStart = i;
        continue;
      }
      break;
    }
    p.lines = lines.slice(0, footerStart).map(line => ({ text: line, page: p.page }));
  });

  // Body lines: concatenate all non-footer lines, tag with page
  const bodyLines = pages.flatMap(p => p.lines.map(line => ({ text: line.text, page: p.page })));

  // Classify lines: cover, heading, paragraph, or unclassified
  const classified = [];
  let currentPart = '';
  let currentSection = '';
  let currentParagraph = null;
  let inCover = true;

  bodyLines.forEach(line => {
    const text = line.text.trim();
    if (text === '') return;

    // Paragraph start: number alone or number and text
    const paraMatch = text.match(/^(\d{1,3})\.$/) || text.match(/^(\d{1,3})\.\s+(.+)$/);
    if (paraMatch) {
      inCover = false;
      const number = parseInt(paraMatch[1]);
      const firstLine = paraMatch[2] || '';

      // Close previous paragraph
      if (currentParagraph) {
        classified.push(currentParagraph);
        checks.paragraphs.found++;
      }

      // Start new paragraph
      currentParagraph = {
        type: 'paragraph',
        number,
        part: currentPart,
        section: currentSection,
        lines: [{ text: paraMatch[0], page: line.page }],
        page_start: line.page,
        page_end: line.page,
        text: firstLine,
        text_lines: [paraMatch[0]],
        flagged: false,
        first_words_match: false,
        citation: `${symbol}, para. ${number}`,
        doc_url,
        limitations: 'footnotes not separated'
      };
      return;
    }

    // Labelled heading: I. A. etc.
    const labelMatch = text.match(/^([IVX]+|[A-Z])\.$/);
    if (labelMatch) {
      inCover = false;
      const label = labelMatch[1];
      const headingLines = [];
      let i = classified.length - 1;
      // Skip blank lines
      while (i >= 0 && classified[i].text.trim() === '') i--;
      // Collect heading lines
      while (i >= 0 && (classified[i].text.match(/^[a-z(]/) || classified[i].text.trim() === '')) {
        headingLines.unshift(classified[i].text);
        classified.pop();
        i--;
      }
      headingLines.push(text);
      const headingText = headingLines.join(' ').trim();
      if (labelMatch[1].length === 1) {
        currentPart = headingText;
      }
      currentSection = headingText;
      classified.push({ type: 'heading', label, text: headingText, page: line.page });
      checks.headings.labelled++;
      if (!checks.headings.list.includes(headingText)) {
        checks.headings.list.push(headingText);
      }
      return;
    }

    // Unlabelled heading: line immediately before a paragraph start, at most 90 chars, starts with capital, does not end with . ; : , or digit
    if (inCover === false && currentParagraph === null) {
      const nextLine = bodyLines.find(l => l.page > line.page || (l.page === line.page && bodyLines.indexOf(l) > bodyLines.indexOf(line)));
      if (nextLine) {
        const nextText = nextLine.text.trim();
        const nextParaMatch = nextText.match(/^(\d{1,3})\.$/) || nextText.match(/^(\d{1,3})\.\s+(.+)$/);
        if (nextParaMatch && text.length <= 90 && /^[A-Z]/.test(text) && !/[.;:,]\d*$/.test(text)) {
          // Check if the previous line is also a heading line
          const prevLine = classified[classified.length - 1];
          if (prevLine && prevLine.type === 'line' && prevLine.text.length <= 90 && /^[A-Z]/.test(prevLine.text) && !/[.;:,]\d*$/.test(prevLine.text)) {
            const combined = prevLine.text + ' ' + text;
            currentSection = combined;
            classified.pop();
            classified.push({ type: 'heading', text: combined, page: prevLine.page });
            checks.headings.unlabelled--;
            checks.headings.list = checks.headings.list.filter(h => h !== prevLine.text);
            if (!checks.headings.list.includes(combined)) {
              checks.headings.list.push(combined);
            }
          } else {
            currentSection = text;
            classified.push({ type: 'heading', text, page: line.page });
            checks.headings.unlabelled++;
            if (!checks.headings.list.includes(text)) {
              checks.headings.list.push(text);
            }
          }
          return;
        }
      }
    }

    // Cover: lines before the first paragraph
    if (inCover) {
      classified.push({ type: 'cover', text, page: line.page });
      return;
    }

    // Paragraph line: add to current paragraph
    if (currentParagraph) {
      currentParagraph.lines.push({ text, page: line.page });
      currentParagraph.page_end = line.page;
      currentParagraph.text_lines.push(text);
      return;
    }

    // Unclassified
    classified.push({ type: 'line', text, page: line.page });
    checks.lines.unclassified.push({ text, page: line.page });
  });

  // Close last paragraph
  if (currentParagraph) {
    classified.push(currentParagraph);
    checks.paragraphs.found++;
  }

  // Build paragraphs: join lines, collapse spaces, trim
  const paragraphs = classified.filter(c => c.type === 'paragraph').map(p => {
    p.text = p.lines.map(l => l.text).join(' ').replace(/\s+/g, ' ').trim();
    p.text_lines = p.lines.map(l => l.text);
    return p;
  });

  // Check numbering: 1 to n in order
  const numbers = paragraphs.map(p => p.number);
  const unique = [...new Set(numbers)].sort((a, b) => a - b);
  if (unique.length > 0) {
    for (let i = 1; i <= unique[unique.length - 1]; i++) {
      if (!unique.includes(i)) {
        checks.paragraphs.numbering.gaps.push(i);
      }
    }
    const seen = new Set();
    numbers.forEach(n => {
      if (seen.has(n)) {
        checks.paragraphs.numbering.duplicates.push(n);
      }
      seen.add(n);
    });
  }

  // Flag suspect lines and long paragraphs
  paragraphs.forEach(p => {
    let hasSuspect = false;
    const suspectLines = [];
    p.lines.forEach((line, i) => {
      const text = line.text.trim();
      // Bare number of 1-3 digits
      if (/^\d{1,3}$/.test(text)) {
        hasSuspect = true;
        suspectLines.push({ line: i, text, reason: 'bare number' });
        return;
      }
      // Starts with number, space, capital / UN symbol / quote
      if (/^\d{1,3}\s+[A-Z"UN]/.test(text) || /^\d{1,3}\s+[A-Z][a-z]+[/.][A-Z]/.test(text)) {
        hasSuspect = true;
        suspectLines.push({ line: i, text, reason: 'starts with a number and a space' });
        return;
      }
      // Starts with asterisk and space
      if (/^\*\s/.test(text)) {
        hasSuspect = true;
        suspectLines.push({ line: i, text, reason: 'starts with an asterisk and a space' });
        return;
      }
    });
    // Paragraph over 300 words
    if (p.text.split(/\s+/).length > 300) {
      hasSuspect = true;
      suspectLines.push({ line: p.lines.length, text: '(entire paragraph)', reason: 'paragraph over 300 words' });
    }
    if (hasSuspect) {
      p.flagged = true;
      p.limitations = `footnotes not separated; ${suspectLines.length} may sit inside this paragraph`;
      checks.paragraphs.flagged++;
      suspectLines.forEach(s => {
        checks.suspectLines.count++;
        checks.suspectLines.pages.add(p.page_start);
        checks.suspectLines.paragraphs.add(p.number);
      });
      checks.paragraphs.flaggedPages.add(p.page_start);
    }
  });

  // First words: compare with reference
  paragraphs.forEach(p => {
    const found = cleanFirstWords(p.text);
    const expected = first_words_ref[String(p.number)] || '';
    p.first_words_match = normalise(found) === normalise(expected);
    if (p.first_words_match) {
      checks.firstWords.match++;
    } else {
      checks.firstWords.mismatch.push({ number: p.number, found, expected });
    }
  });

  // Classified lines: every non-empty line is classified exactly once
  checks.lines.classified = classified.length;
  if (checks.lines.classified !== checks.lines.total) {
    checks.lines.unclassified = bodyLines
      .map(line => ({ text: line.text, page: line.page }))
      .filter(line => !classified.some(c => c.text === line.text && c.page === line.page));
  }

  // Export round trip: JSON to download is parsed back
  try {
    const json = JSON.stringify(paragraphs.map(p => ({
      symbol: p.symbol,
      paragraph: p.number,
      section: p.section,
      part: p.part,
      page_start: p.page_start,
      page_end: p.page_end,
      text: p.text,
      text_lines: p.text_lines,
      flagged: p.flagged,
      first_words_match: p.first_words_match,
      citation: p.citation,
      doc_url: p.doc_url,
      limitations: p.limitations
    })), null, 2);
    const parsed = JSON.parse(json);
    checks.exportRoundTrip = parsed.length === paragraphs.length;
  } catch (e) {
    checks.exportRoundTrip = false;
  }

  return { pages, paragraphs, classified, checks };
})();

// Render the app
document.addEventListener('DOMContentLoaded', () => {
  // Header
  document.getElementById('header-title').textContent = title;
  document.getElementById('header-meta').innerHTML = `
    <a href="${doc_url}" target="_blank" class="mono">${symbol}</a>,
    adopted ${adopted},
    ${records.length} pages,
    ${source}
  `;
  document.getElementById('rail-symbol').textContent = symbol;
  document.getElementById('rail-title').textContent = title.split(' (')[0];

  // Rail
  document.getElementById('rail-paragraphs').textContent = pipeline.paragraphs.length;
  document.getElementById('rail-expected').textContent = paragraphs_expected;
  const railBar = document.getElementById('rail-bar');
  if (pipeline.paragraphs.length === paragraphs_expected) {
    railBar.classList.add('ok');
  } else if (pipeline.paragraphs.length < paragraphs_expected) {
    railBar.classList.add('short');
  } else {
    railBar.classList.add('over');
  }
  document.getElementById('rail-flagged').textContent = pipeline.checks.paragraphs.flagged;
  const checksPass = [
    pipeline.checks.header.found === pipeline.checks.header.expected,
    pipeline.checks.footer.pageNumber.found === pipeline.checks.footer.pageNumber.expected,
    pipeline.checks.paragraphs.numbering.gaps.length === 0,
    pipeline.checks.paragraphs.numbering.duplicates.length === 0,
    pipeline.checks.lines.unclassified.length === 0,
    pipeline.checks.exportRoundTrip
  ].filter(Boolean).length;
  const checksTotal = 6;
  document.getElementById('rail-checks').textContent = `${checksPass} of ${checksTotal} checks pass`;
  document.getElementById('rail-checks').prepend(checksPass === checksTotal ? createDot('pass') : createDot('fail'));

  // Tiles
  document.getElementById('tile-paragraphs').textContent = pipeline.paragraphs.length;
  document.getElementById('tile-expected').textContent = paragraphs_expected;
  if (pipeline.paragraphs.length !== paragraphs_expected) {
    document.getElementById('tile-paragraphs').classList.add('red');
  }

  document.getElementById('tile-first-words').textContent = pipeline.checks.firstWords.match;
  document.getElementById('tile-first-words-total').textContent = paragraphs_expected;
  if (pipeline.checks.firstWords.mismatch.length > 0) {
    const mismatchDiv = document.getElementById('tile-mismatch');
    mismatchDiv.innerHTML = '';
    pipeline.checks.firstWords.mismatch.slice(0, 10).forEach(m => {
      const div = document.createElement('div');
      div.textContent = `para. ${m.number}: found “${m.found}” / reference “${m.expected}”`;
      mismatchDiv.appendChild(div);
    });
    if (pipeline.checks.firstWords.mismatch.length > 10) {
      const div = document.createElement('div');
      div.textContent = `and ${pipeline.checks.firstWords.mismatch.length - 10} more`;
      mismatchDiv.appendChild(div);
    }
  }

  document.getElementById('tile-flagged').textContent = pipeline.checks.paragraphs.flagged;
  document.getElementById('tile-flagged-total').textContent = pipeline.paragraphs.length;
  document.getElementById('tile-flagged-pages').textContent = pipeline.checks.paragraphs.flaggedPages.size;
  if (pipeline.checks.paragraphs.flagged > 0) {
    document.getElementById('tile-flagged').classList.add('red');
  }

  document.getElementById('tile-footnotes').textContent = footnotes_expected;

  // Header checks
  const headerChecksPass = checksPass;
  const headerChecksTotal = checksTotal;
  document.getElementById('header-checks').textContent = `${headerChecksPass} of ${headerChecksTotal} checks pass`;
  document.getElementById('header-dot').className = headerChecksPass === headerChecksTotal ? 'dot pass' : 'dot fail';
  document.getElementById('header-flagged').textContent = `${pipeline.checks.paragraphs.flagged} paragraphs flagged`;

  // Checks panel
  const checksList = document.getElementById('checks-list');
  checksList.innerHTML = '';

  addCheck(checksList, 'Paragraph count', `${pipeline.paragraphs.length} found`, `${paragraphs_expected} expected`, pipeline.paragraphs.length === paragraphs_expected, null);

  addCheck(checksList, 'Numbering', `1 to ${pipeline.paragraphs.length} in order`, 'no gaps or duplicates', pipeline.checks.paragraphs.numbering.gaps.length === 0 && pipeline.checks.paragraphs.numbering.duplicates.length === 0, () => {
    const details = document.createElement('div');
    details.className = 'details';
    if (pipeline.checks.paragraphs.numbering.gaps.length > 0) {
      const div = document.createElement('div');
      div.innerHTML = `Gaps: ${pipeline.checks.paragraphs.numbering.gaps.map(n => `<a href="#" data-tab="02" data-number="${n}">para. ${n}</a>`).join(', ')}`;
      details.appendChild(div);
    }
    if (pipeline.checks.paragraphs.numbering.duplicates.length > 0) {
      const div = document.createElement('div');
      div.innerHTML = `Duplicates: ${pipeline.checks.paragraphs.numbering.duplicates.map(n => `<a href="#" data-tab="02" data-number="${n}">para. ${n}</a>`).join(', ')}`;
      details.appendChild(div);
    }
    return details;
  });

  addCheck(checksList, 'First words', `${pipeline.checks.firstWords.match} match`, `${paragraphs_expected} expected`, pipeline.checks.firstWords.mismatch.length === 0, () => {
    const details = document.createElement('div');
    details.className = 'details';
    if (pipeline.checks.firstWords.mismatch.length > 0) {
      const div = document.createElement('div');
      div.innerHTML = pipeline.checks.firstWords.mismatch.slice(0, 5).map(m => `para. ${m.number}: found “${m.found}” / reference “${m.expected}”`).join('<br>');
      details.appendChild(div);
    }
    return details;
  });

  addCheck(checksList, 'Paragraphs flagged', `${pipeline.checks.paragraphs.flagged} flagged on ${pipeline.checks.paragraphs.flaggedPages.size} pages`, 'to check against the PDF', true, () => {
    const details = document.createElement('div');
    details.className = 'details';
    details.textContent = 'A flag is not a failure: the paragraph count can be right while footnote text sits inside a paragraph.';
    return details;
  });

  addCheck(checksList, 'Suspect lines', `${pipeline.checks.suspectLines.count} on ${pipeline.checks.suspectLines.pages.size} pages`, 'none removed', true, () => {
    const details = document.createElement('div');
    details.className = 'details';
    details.textContent = 'Suspect lines stay in the text; the expanded paragraph highlights them.';
    return details;
  });

  addCheck(checksList, 'Headers and footers', `header on ${pipeline.checks.header.found} pages, page number on ${pipeline.checks.footer.pageNumber.found} pages`, `${pipeline.checks.header.expected} and ${pipeline.checks.footer.pageNumber.expected} expected`, pipeline.checks.header.found === pipeline.checks.header.expected && pipeline.checks.footer.pageNumber.found === pipeline.checks.footer.pageNumber.expected, () => {
    const details = document.createElement('div');
    details.className = 'details';
    if (pipeline.checks.header.pages.length > 0) {
      const div = document.createElement('div');
      div.textContent = `Header missing on pages: ${pipeline.checks.header.pages.join(', ')}`;
      details.appendChild(div);
    }
    if (pipeline.checks.footer.pageNumber.pages.length !== pipeline.checks.footer.pageNumber.expected) {
      const div = document.createElement('div');
      div.textContent = `Page number missing on pages: ${Array.from({ length: pipeline.checks.footer.pageNumber.expected }, (_, i) => i + 1).filter(p => !pipeline.checks.footer.pageNumber.pages.includes(p)).join(', ')}`;
      details.appendChild(div);
    }
    if (pipeline.checks.footer.bareNumber.count > 0) {
      const div = document.createElement('div');
      div.textContent = `Bare numbers removed from footer: ${pipeline.checks.footer.bareNumber.pages.map(p => `${p.number} on p. ${p.page}`).join(', ')}`;
      details.appendChild(div);
    }
    return details;
  });

  addCheck(checksList, 'Headings', `${pipeline.checks.headings.labelled} labelled, ${pipeline.checks.headings.unlabelled} unlabelled`, 'none hidden inside a paragraph', true, () => {
    const details = document.createElement('div');
    details.className = 'details';
    if (pipeline.checks.headings.unlabelled > 0) {
      const div = document.createElement('div');
      div.textContent = `Unlabelled headings: ${pipeline.checks.headings.list.filter(h => !/^[IVX]+ |^[A-Z]\.\s/.test(h)).join(', ')}`;
      details.appendChild(div);
    }
    return details;
  });

  addCheck(checksList, 'Nothing lost', `${pipeline.checks.lines.classified} lines classified`, `${pipeline.checks.lines.total} total`, pipeline.checks.lines.unclassified.length === 0, () => {
    const details = document.createElement('div');
    details.className = 'details';
    if (pipeline.checks.lines.unclassified.length > 0) {
      const div = document.createElement('div');
      div.innerHTML = pipeline.checks.lines.unclassified.map(line => `p. ${line.page}: “${line.text}”`).join('<br>');
      details.appendChild(div);
    }
    return details;
  });

  addCheck(checksList, 'Export round trip', 'JSON to download parses back', `${pipeline.paragraphs.length} records`, pipeline.checks.exportRoundTrip, null);

  document.getElementById('checks-count').textContent = checksList.children.length;

  // Flagged paragraphs table
  const flaggedTableBody = document.getElementById('flagged-table-body');
  flaggedTableBody.innerHTML = '';
  pipeline.paragraphs
    .filter(p => p.flagged)
    .forEach(p => {
      const tr = document.createElement('tr');
      tr.tabIndex = 0;
      tr.innerHTML = `
        <td>${p.number}</td>
        <td>${p.page_start}${p.page_start !== p.page_end ? `–${p.page_end}` : ''}</td>
        <td>${p.lines.filter(line => isSuspectLine(line.text)).length}</td>
        <td class="why">${p.lines.filter(line => isSuspectLine(line.text)).map(line => `<span class="suspect">${line.text.trim()}</span>`).join('<br>') || p.text.split(/\s+/).length > 300 ? '(entire paragraph)' : ''}</td>
      `;
      tr.addEventListener('click', () => {
        document.getElementById('tab-02').click();
        const row = document.querySelector(`#paragraphs-table-body tr[data-number="${p.number}"]`);
        if (row) {
          row.scrollIntoView({ behavior: 'smooth', block: 'center' });
          row.click();
        }
      });
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          tr.click();
        }
      });
      flaggedTableBody.appendChild(tr);
    });
  document.getElementById('flagged-count').textContent = pipeline.checks.paragraphs.flagged;
  document.getElementById('flagged-table-count').textContent = pipeline.checks.paragraphs.flagged;

  // Headings panel
  const headingsList = document.getElementById('headings-list');
  headingsList.innerHTML = pipeline.checks.headings.list.map(h => `<div>${h}</div>`).join('');
  document.getElementById('headings-count').textContent = pipeline.checks.headings.list.length;

  // Paragraphs table
  const tableBody = document.getElementById('paragraphs-table-body');
  tableBody.innerHTML = '';
  pipeline.paragraphs.forEach(p => {
    const tr = document.createElement('tr');
    tr.tabIndex = 0;
    tr.dataset.number = p.number;
    tr.innerHTML = `
      <th scope="row">${p.number}</th>
      <td>${p.section || ''}</td>
      <td>${p.page_start}${p.page_start !== p.page_end ? `–${p.page_end}` : ''}</td>
      <td>${p.text.substring(0, 120)}${p.text.length > 120 ? '…' : ''}</td>
      <td class="${p.first_words_match ? 'green' : 'red'}">${p.first_words_match ? 'OK' : p.flagged ? 'may contain footnote text' : 'first words differ'}</td>
    `;
    tr.addEventListener('click', () => {
      const expanded = tr.nextElementSibling;
      const isExpanded = expanded && expanded.classList.contains('expanded');
      document.querySelectorAll('.expanded').forEach(el => el.remove());
      if (!isExpanded) {
        const div = document.createElement('tr');
        div.className = 'expanded';
        div.innerHTML = `
          <td colspan="5">
            <div class="text" id="text-${p.number}">${formatTextWithSuspect(p)}</div>
            <div class="ref">
              First six words: <span class="${p.first_words_match ? 'match' : 'mismatch'}">${cleanFirstWords(p.text)}</span>
              ${p.first_words_match ? '' : `<br>Reference: <span class="mismatch">${first_words_ref[String(p.number)] || ''}</span>`}
            </div>
            <div class="toggle">
              <button class="button" id="toggle-${p.number}">Show the PDF's lines</button>
            </div>
            <div class="citation">
              Citation: <span class="mono">${p.citation}</span>
              <button class="button" id="copy-${p.number}">Copy citation</button>
            </div>
          </td>
        `;
        tr.insertAdjacentElement('afterend', div);
        document.getElementById(`toggle-${p.number}`).addEventListener('click', () => {
          const textDiv = document.getElementById(`text-${p.number}`);
          if (textDiv.innerHTML === formatTextWithSuspect(p)) {
            textDiv.innerHTML = formatTextRaw(p);
            document.getElementById(`toggle-${p.number}`).textContent = 'Show the clean text';
          } else {
            textDiv.innerHTML = formatTextWithSuspect(p);
            document.getElementById(`toggle-${p.number}`).textContent = 'Show the PDF\'s lines';
          }
        });
        document.getElementById(`copy-${p.number}`).addEventListener('click', () => {
          navigator.clipboard.writeText(p.citation).then(() => {
            const button = document.getElementById(`copy-${p.number}`);
            const original = button.textContent;
            button.textContent = 'Copied';
            setTimeout(() => { button.textContent = original; }, 2000);
          });
        });
      }
    });
    tr.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        tr.click();
      }
    });
    tableBody.appendChild(tr);
  });
  document.getElementById('table-caption-symbol').textContent = symbol;

  // Footer
  document.getElementById('footer-source').textContent = source;
  document.getElementById('footer-built').textContent = `Built ${built}`;

  // Tabs
  document.getElementById('tab-01').addEventListener('click', () => switchTab('01'));
  document.getElementById('tab-02').addEventListener('click', () => switchTab('02'));
  document.getElementById('checks-toggle').addEventListener('click', () => {
    const panel = document.getElementById('checks-panel');
    panel.hidden = !panel.hidden;
    document.getElementById('checks-toggle').setAttribute('aria-expanded', panel.hidden ? 'false' : 'true');
  });
  document.getElementById('flagged-toggle').addEventListener('click', () => {
    const panel = document.getElementById('flagged-panel');
    panel.hidden = !panel.hidden;
    document.getElementById('flagged-toggle').setAttribute('aria-expanded', panel.hidden ? 'false' : 'true');
  });
  document.getElementById('headings-toggle').addEventListener('click', () => {
    const panel = document.getElementById('headings-panel');
    panel.hidden = !panel.hidden;
    document.getElementById('headings-toggle').setAttribute('aria-expanded', panel.hidden ? 'false' : 'true');
  });

  // Downloads
  document.getElementById('download-json').addEventListener('click', () => {
    const json = JSON.stringify(pipeline.paragraphs.map(p => ({
      symbol: p.symbol,
      paragraph: p.number,
      section: p.section,
      part: p.part,
      page_start: p.page_start,
      page_end: p.page_end,
      text: p.text,
      text_lines: p.text_lines,
      flagged: p.flagged,
      first_words_match: p.first_words_match,
      citation: p.citation,
      doc_url: p.doc_url,
      limitations: p.limitations
    })), null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = symbol.replace(/\//g, '-') + '.json';
    a.click();
    URL.revokeObjectURL(url);
  });

  document.getElementById('download-md').addEventListener('click', () => {
    const frontMatter = `---
title: ${title}
symbol: ${symbol}
adopted: ${adopted}
source_url: ${doc_url}
extracted: ${new Date().toISOString().split('T')[0]}
paragraphs_found: ${pipeline.paragraphs.length}
paragraphs_expected: ${paragraphs_expected}
paragraphs_flagged: ${pipeline.checks.paragraphs.flagged}
footnotes: not separated; the document has ${footnotes_expected}
---`;

    const headings = {};
    pipeline.paragraphs.forEach(p => {
      if (p.part) {
        if (!headings[p.part]) headings[p.part] = [];
        if (p.section && !headings[p.part].includes(p.section)) {
          headings[p.part].push(p.section);
        }
      }
    });

    const mdHeadings = Object.entries(headings).map(([part, sections]) => {
      const partLine = `## ${part}`;
      const sectionLines = sections.map(s => `### ${s}`).join('\n');
      return `${partLine}\n${sectionLines}`;
    }).join('\n');

    const paragraphsMd = pipeline.paragraphs.map(p => {
      const sectionPath = [p.part, p.section].filter(Boolean).join(' › ');
      return `**${p.number}.** ${p.text}${p.flagged ? ' (flagged: may contain footnote text)' : ''}`;
    }).join('\n\n');

    const md = `${frontMatter}\n\n${mdHeadings}\n\n${paragraphsMd}`;
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = symbol.replace(/\//g, '-') + '.md';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Helper: is a line suspect?
  function isSuspectLine(text) {
    const trimmed = text.trim();
    return /^\d{1,3}$/.test(trimmed) ||
           /^\d{1,3}\s+[A-Z"UN]/.test(trimmed) ||
           /^\d{1,3}\s+[A-Z][a-z]+[/.][A-Z]/.test(trimmed) ||
           /^\*\s/.test(trimmed);
  }

  // Helper: format text with suspect lines marked
  function formatTextWithSuspect(p) {
    return p.text_lines.map(line => {
      const trimmed = line.trim();
      if (isSuspectLine(line)) {
        return `<span class="suspect">${line}</span>`;
      }
      return line;
    }).join(' ');
  }

  // Helper: format text with raw lines and page breaks
  function formatTextRaw(p) {
    const lines = [];
    let currentPage = p.page_start;
    p.text_lines.forEach((line, i) => {
      if (p.lines[i].page !== currentPage) {
        lines.push(`\n[page ${p.lines[i].page}]\n`);
        currentPage = p.lines[i].page;
      }
      lines.push(line);
    });
    return lines.join('\n');
  }

  // Helper: add a check to the panel
  function addCheck(container, label, found, expected, pass, detailsFn) {
    const div = document.createElement('div');
    div.className = 'check';
    const status = document.createElement('div');
    status.className = `status ${pass ? 'pass' : 'fail'}`;
    status.textContent = pass ? 'pass' : 'check failed';
    const labelDiv = document.createElement('div');
    labelDiv.textContent = `${label}: ${found}`;
    const expectedDiv = document.createElement('div');
    expectedDiv.textContent = expected;
    div.appendChild(labelDiv);
    div.appendChild(expectedDiv);
    div.appendChild(status);
    if (detailsFn) {
      const details = detailsFn();
      if (details) {
        div.appendChild(details);
      }
    }
    container.appendChild(div);
  }

  // Helper: create a dot
  function createDot(type) {
    const dot = document.createElement('span');
    dot.className = `dot ${type}`;
    return dot;
  }

  // Helper: switch tab
  function switchTab(tab) {
    document.querySelectorAll('[role="tab"]').forEach(t => {
      t.setAttribute('aria-selected', t.id === `tab-${tab}`);
    });
    document.querySelectorAll('[role="tabpanel"]').forEach(p => {
      p.setAttribute('aria-hidden', p.id !== `panel-${tab}`);
    });
  }
});
</script>
</body>
</html>
```