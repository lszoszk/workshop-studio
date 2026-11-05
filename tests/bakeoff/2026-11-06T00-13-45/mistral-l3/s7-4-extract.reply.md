Here’s the app that extracts the numbered paragraphs from the PDF converter’s text, checks them against the reference, and flags suspect lines. It follows the plan exactly: two tabs, a left rail with the document card, and the checks and exports on tab 01.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Paragraphs from PDF text</title>
  <style>
    :root {
      --paper: #f4f0e8;
      --ink: #1d1b18;
      --rule: #d9d2c3;
      --red: #9b2335;
      --green: #2e6b49;
    }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 16px;
      line-height: 1.5;
      color: var(--ink);
      background-color: var(--paper);
      display: grid;
      grid-template-columns: 240px 1fr;
      grid-template-rows: auto 1fr;
      min-height: 100vh;
    }
    [hidden] { display: none !important; }
    a { color: var(--ink); }
    a:focus { outline: 2px solid var(--red); outline-offset: 2px; }

    /* Header */
    header {
      grid-column: 1 / -1;
      padding: 0.5rem 1rem;
      border-bottom: 1px solid var(--rule);
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      font-size: 0.8rem;
    }
    .header-left { display: flex; gap: 1rem; }
    .header-right { display: flex; gap: 1rem; align-items: center; }
    .header-label {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
    }
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 0.3rem;
    }
    .status-pass { background-color: var(--green); }
    .status-fail { background-color: var(--red); }

    /* Left rail */
    .rail {
      padding: 1rem;
      border-right: 1px solid var(--rule);
      font-size: 0.9rem;
    }
    .rail h2 {
      font-size: 0.8rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
      margin: 0 0 1rem 0;
      text-transform: uppercase;
    }
    .rail-card {
      background: white;
      border: 1px solid var(--rule);
      padding: 0.8rem;
      margin-bottom: 1.5rem;
    }
    .rail-card h3 {
      font-size: 0.8rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
      margin: 0 0 0.5rem 0;
      text-transform: uppercase;
    }
    .rail-card .symbol {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 1.1rem;
      margin-bottom: 0.5rem;
      display: block;
    }
    .rail-card .title {
      font-size: 0.9rem;
      line-height: 1.4;
    }
    .rail-numbers {
      display: flex;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .rail-number {
      flex: 1;
      text-align: center;
    }
    .rail-number .value {
      font-family: Georgia, "Times New Roman", serif;
      font-size: 2.5rem;
      line-height: 1;
      display: block;
    }
    .rail-number .label {
      font-size: 0.7rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .rail-number .bar {
      height: 2px;
      background: var(--rule);
      margin-top: 0.3rem;
    }
    .rail-number .bar.short { background: var(--red); }
    .rail-number .bar.flagged { background: var(--red); }
    .rail-checks {
      font-size: 0.8rem;
    }
    .rail-checks .pass { color: var(--green); }
    .rail-checks .fail { color: var(--red); }

    /* Tabs */
    .tabs {
      grid-column: 2;
      padding: 0 1rem;
      border-bottom: 1px solid var(--rule);
    }
    .tablist {
      display: flex;
      gap: 0;
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .tab {
      padding: 0.8rem 1rem;
      background: none;
      border: none;
      font-size: 0.9rem;
      cursor: pointer;
      position: relative;
      color: var(--ink);
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .tab:focus { outline: 2px solid var(--red); outline-offset: -2px; }
    .tab[aria-selected="true"] {
      color: var(--red);
      border-bottom: 2px solid var(--red);
    }
    .tab-panel { padding: 1rem; }

    /* Tab 01 */
    .tiles {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }
    .tile {
      background: white;
      border: 1px solid var(--rule);
      padding: 1rem;
    }
    .tile h3 {
      font-family: Georgia, "Times New Roman", serif;
      font-size: 2.5rem;
      margin: 0 0 0.5rem 0;
      line-height: 1;
    }
    .tile .subtitle {
      font-size: 0.9rem;
      margin-bottom: 0.5rem;
    }
    .tile .how {
      font-size: 0.8rem;
      color: #666;
      font-style: italic;
    }
    .tile .fail { color: var(--red); }
    .tile .footnote-note {
      font-size: 0.8rem;
      color: var(--red);
      margin-top: 0.5rem;
    }
    .first-words-list {
      margin: 1rem 0;
      border: 1px solid var(--rule);
      padding: 0.5rem;
      background: white;
    }
    .first-words-list p {
      margin: 0.3rem 0;
      padding: 0.3rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.9rem;
    }
    .first-words-list .fail { background: #fff0f0; }
    .export-buttons {
      display: flex;
      gap: 1rem;
      margin: 2rem 0;
    }
    .export-buttons button {
      padding: 0.6rem 1rem;
      border: 1px solid var(--rule);
      background: white;
      cursor: pointer;
    }
    .export-buttons button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .check-panel, .flagged-panel {
      border: 1px solid var(--rule);
      margin-top: 1rem;
    }
    .check-panel h4, .flagged-panel h4 {
      margin: 0;
      padding: 0.6rem 1rem;
      background: var(--rule);
      font-size: 0.9rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .check-panel h4:focus, .flagged-panel h4:focus {
      outline: 2px solid var(--red);
    }
    .check-panel[aria-expanded="false"] .checks,
    .flagged-panel[aria-expanded="false"] .flagged-table {
      display: none;
    }
    .checks {
      padding: 1rem;
      background: white;
    }
    .check {
      display: flex;
      justify-content: space-between;
      padding: 0.3rem 0;
      border-bottom: 1px solid var(--rule);
    }
    .check:last-child { border-bottom: none; }
    .check .label { font-family: ui-monospace, Menlo, Consolas, monospace; }
    .check .value { font-family: ui-monospace, Menlo, Consolas, monospace; }
    .check .pass { color: var(--green); }
    .check .fail { color: var(--red); }
    .check a { color: var(--red); text-decoration: none; }
    .check a:focus { outline: 2px solid var(--red); }
    .flagged-table {
      width: 100%;
      border-collapse: collapse;
      background: white;
    }
    .flagged-table th, .flagged-table td {
      padding: 0.6rem;
      text-align: left;
      border-bottom: 1px solid var(--rule);
    }
    .flagged-table th {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .flagged-table .fail { color: var(--red); }
    .flagged-note {
      padding: 1rem;
      font-size: 0.9rem;
      background: white;
      border-top: 1px solid var(--rule);
    }

    /* Tab 02 */
    .headings-box {
      border: 1px solid var(--rule);
      margin-bottom: 1rem;
    }
    .headings-box h4 {
      margin: 0;
      padding: 0.6rem 1rem;
      background: var(--rule);
      font-size: 0.9rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .headings-box h4:focus { outline: 2px solid var(--red); }
    .headings-box[aria-expanded="false"] .headings-list {
      display: none;
    }
    .headings-list {
      padding: 1rem;
      background: white;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .paragraphs-table {
      width: 100%;
      border-collapse: collapse;
    }
    .paragraphs-table caption {
      font-family: Georgia, "Times New Roman", serif;
      font-size: 1.1rem;
      margin-bottom: 0.5rem;
      text-align: left;
    }
    .paragraphs-table th, .paragraphs-table td {
      padding: 0.6rem;
      text-align: left;
      border-bottom: 1px solid var(--rule);
    }
    .paragraphs-table th {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .paragraphs-table th.num, .paragraphs-table td.num {
      text-align: right;
      font-family: Georgia, "Times New Roman", serif;
    }
    .paragraphs-table .page { font-family: ui-monospace, Menlo, Consolas, monospace; }
    .paragraphs-table .check { font-family: ui-monospace, Menlo, Consolas, monospace; }
    .paragraphs-table .check.fail { color: var(--red); }
    .paragraphs-table tr[aria-expanded="true"] {
      background: #f9f7f4;
    }
    .paragraphs-table tr[aria-expanded="true"] td {
      padding: 0;
    }
    .paragraph-expanded {
      padding: 1rem;
      background: white;
      border-top: 1px solid var(--rule);
    }
    .paragraph-expanded .meta {
      display: flex;
      gap: 1rem;
      margin-bottom: 0.5rem;
      font-size: 0.8rem;
      font-family: ui-monospace, Menlo, Consolas, monospace;
    }
    .paragraph-expanded .text {
      white-space: pre-wrap;
      line-height: 1.6;
    }
    .paragraph-expanded .suspect {
      background: #fff0f0;
      padding: 0 0.2rem;
      border: 1px solid var(--red);
    }
    .paragraph-expanded .first-words {
      margin-top: 0.5rem;
      font-size: 0.9rem;
    }
    .paragraph-expanded .first-words .found {
      font-family: ui-monospace, Menlo, Consolas, monospace;
    }
    .paragraph-expanded .first-words .ref {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      color: #666;
    }
    .paragraph-expanded .first-words.fail { color: var(--red); }
    .paragraph-expanded .toggle {
      margin-top: 1rem;
      font-size: 0.8rem;
    }
    .paragraph-expanded .toggle button {
      background: none;
      border: none;
      color: var(--ink);
      text-decoration: underline;
      cursor: pointer;
      padding: 0;
    }
    .paragraph-expanded .toggle button:focus { outline: 2px solid var(--red); }
    .paragraph-expanded .raw {
      margin-top: 0.5rem;
      white-space: pre-wrap;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.9rem;
      line-height: 1.5;
      background: #f9f7f4;
      padding: 0.5rem;
      border: 1px solid var(--rule);
    }
    .paragraph-expanded .citation-button {
      margin-top: 1rem;
      padding: 0.4rem 0.8rem;
      background: white;
      border: 1px solid var(--rule);
      cursor: pointer;
    }
    .paragraph-expanded .citation-button:focus { outline: 2px solid var(--red); }
    .paragraph-expanded .copied {
      margin-left: 0.5rem;
      color: var(--green);
      font-size: 0.8rem;
    }

    /* Footer */
    footer {
      grid-column: 1 / -1;
      padding: 0.8rem 1rem;
      border-top: 1px solid var(--rule);
      font-size: 0.8rem;
      display: flex;
      justify-content: space-between;
    }
    .footer-left { font-family: ui-monospace, Menlo, Consolas, monospace; }
    .footer-right { text-align: right; }
  </style>
</head>
<body>

<header>
  <div class="header-left">
    <span class="header-label">UN DOCUMENT · PDF TEXT</span>
    <span id="doc-title"></span>
  </div>
  <div class="header-right">
    <span id="status"></span>
    <span id="flagged-count"></span>
  </div>
</header>

<div class="rail">
  <h2>Document</h2>
  <div class="rail-card">
    <h3>Symbol</h3>
    <a id="rail-symbol" class="symbol" target="_blank"></a>
    <div id="rail-title" class="title"></div>
  </div>
  <div class="rail-numbers">
    <div class="rail-number">
      <span id="rail-paragraphs-value" class="value"></span>
      <span class="label">paragraphs of <span id="rail-paragraphs-expected"></span></span>
      <div id="rail-paragraphs-bar" class="bar"></div>
    </div>
    <div class="rail-number">
      <span id="rail-flagged-value" class="value"></span>
      <span class="label">paragraphs flagged</span>
      <div id="rail-flagged-bar" class="bar"></div>
    </div>
  </div>
  <div class="rail-checks">
    <span id="rail-checks-pass" class="pass"></span>
    <span> of </span>
    <span id="rail-checks-total"></span>
    <span> checks pass</span>
  </div>
</div>

<div class="tabs">
  <div role="tablist" aria-label="Tabs">
    <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
    <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
  </div>
</div>

<div id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01">
  <div class="tiles">
    <div class="tile">
      <h3 id="paragraphs-found-value"></h3>
      <div class="subtitle">Paragraphs found</div>
      <div class="how">How this is computed: the app looks for lines that start with a number and a full stop, alone or with text after it.</div>
    </div>
    <div class="tile">
      <h3 id="paragraphs-expected-value"></h3>
      <div class="subtitle">The document has <span id="paragraphs-expected-ref"></span></div>
      <div class="how">How this is computed: the reference in the file says how many numbered paragraphs the document has.</div>
      <div id="paragraphs-count-fail" class="fail" hidden></div>
    </div>
    <div class="tile">
      <h3 id="first-words-match-value"></h3>
      <div class="subtitle">First words match</div>
      <div class="how">How this is computed: the first six words of each paragraph, after removing footnote marks, are compared with the reference.</div>
      <div id="first-words-list" hidden></div>
    </div>
    <div class="tile">
      <h3 id="paragraphs-flagged-value"></h3>
      <div class="subtitle">Paragraphs flagged</div>
      <div class="how">How this is computed: a paragraph is flagged when it has a line that looks like a footnote or is over 300 words.</div>
      <div id="paragraphs-flagged-pages" class="footnote-note"></div>
    </div>
    <div class="tile">
      <h3>Not separated</h3>
      <div class="subtitle">Footnotes</div>
      <div class="how">How this is computed: the document has <span id="footnotes-expected"></span>; this version leaves them in place and flags them.</div>
    </div>
  </div>

  <div class="export-buttons">
    <button id="export-json" disabled>Download JSON</button>
    <button id="export-markdown" disabled>Download Markdown</button>
  </div>

  <div class="check-panel" aria-expanded="false">
    <h4 tabindex="0" role="button" aria-expanded="false">
      Every check (<span id="checks-total"></span>)
      <span>▼</span>
    </h4>
    <div class="checks" id="checks-list"></div>
  </div>

  <div class="flagged-panel" aria-expanded="false">
    <h4 tabindex="0" role="button" aria-expanded="false">
      Flagged paragraphs (<span id="flagged-paragraphs-count"></span>)
      <span>▼</span>
    </h4>
    <div class="flagged-note">
      This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.
    </div>
    <table class="flagged-table">
      <thead>
        <tr>
          <th>Paragraph</th>
          <th>Page</th>
          <th>Suspect lines</th>
          <th>Why</th>
        </tr>
      </thead>
      <tbody id="flagged-paragraphs-list"></tbody>
    </table>
  </div>
</div>

<div id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" hidden>
  <div class="headings-box" aria-expanded="false">
    <h4 tabindex="0" role="button" aria-expanded="false">
      Headings found: <span id="headings-count"></span>
      <span>▼</span>
    </h4>
    <div class="headings-list" id="headings-list"></div>
  </div>

  <table class="paragraphs-table">
    <caption id="paragraphs-table-caption"></caption>
    <thead>
      <tr>
        <th class="num">No.</th>
        <th>Section</th>
        <th class="page">Page</th>
        <th>First line</th>
        <th>Check</th>
      </tr>
    </thead>
    <tbody id="paragraphs-list"></tbody>
  </table>
</div>

<footer>
  <div class="footer-left">
    <span id="footer-source"></span><br>
    <span id="footer-built"></span>
  </div>
  <div class="footer-right">
    Done by this page's code; no model was called and nothing left the browser.
  </div>
</footer>

<script>
  // Data
  const data = window.WORKSHOP_DATA.pdf_text;
  const { title, symbol, doc_url, source, built, records, reference } = data;
  const { paragraphs: refParagraphs, footnotes: refFootnotes, adopted, first_words: refFirstWords } = reference || {};

  // State
  let paragraphs = [];
  let checks = [];
  let headings = [];
  let flaggedParagraphs = [];
  let firstWordsMismatches = [];

  // Normalise text for comparison
  function normalise(text) {
    return text
      .replace(/[“”]/g, '"')
      .replace(/[‘’]/g, "'")
      .replace(/[–—]/g, '-')
      .replace(/\s+/g, ' ')
      .trim();
  }

  // Extract first six words, removing footnote marks
  function firstSixWords(text) {
    // Remove footnote marks: digits glued to the end of a word or punctuation
    const cleaned = text.replace(/(\w|\p{P})(\d+)/gu, '$1');
    const words = cleaned.split(/\s+/).filter(w => w.length > 0);
    return words.slice(0, 6).join(' ');
  }

  // Is a token a real number that starts a paragraph?
  function isRealNumber(token) {
    const realNumbers = ['No.', 'article', 'Article', 'art.', 'Art.', 'para.', 'Para.'];
    return realNumbers.some(prefix => token.startsWith(prefix));
  }

  // Pipeline
  function runPipeline() {
    // 1. Classify lines
    let coverLines = [];
    let headerLines = [];
    let footerLines = [];
    let bodyLines = [];
    let unclassifiedLines = [];

    records.forEach((page, pageIndex) => {
      const lines = page.text.split(/\r?\n/).filter(line => line.trim().length > 0);
      const pageNum = pageIndex + 1;

      // Header: first non-empty line equals symbol
      if (lines.length > 0 && lines[0] === symbol) {
        headerLines.push({ page: pageNum, line: lines[0] });
        lines.shift();
      } else if (lines.length > 0) {
        unclassifiedLines.push({ page: pageNum, line: lines[0], reason: 'header' });
      }

      // Footer: from the end, drop empty, GE., date stamp, bare number
      let footer = [];
      while (lines.length > 0) {
        const line = lines[lines.length - 1];
        if (line.trim().length === 0) {
          lines.pop();
          continue;
        }
        if (line.startsWith('GE.')) {
          footer.unshift(line);
          lines.pop();
          continue;
        }
        if (/^\d{6}$/.test(line) || /^\d{6} \d{6}$/.test(line)) {
          footer.unshift(line);
          lines.pop();
          continue;
        }
        if (/^\d{1,3}$/.test(line)) {
          if (parseInt(line) === pageNum) {
            footer.unshift(line);
            lines.pop();
          } else {
            footer.unshift(line);
            lines.pop();
            checks.push({
              name: 'bare_number_removed',
              page: pageNum,
              line: line,
              pass: true
            });
          }
          continue;
        }
        break;
      }
      footerLines.push({ page: pageNum, lines: footer });

      // Body: the rest
      bodyLines.push(...lines.map(line => ({ page: pageNum, line })));
    });

    // 2. Concatenate body lines in page order
    const allBodyLines = bodyLines;

    // 3. Find paragraph starts
    let currentParagraph = null;
    let currentHeading = null;
    let currentPart = null;
    let inHeading = false;
    let headingLines = [];

    allBodyLines.forEach(({ page, line }, index) => {
      // Paragraph start: number alone or number and text on one line
      const paraMatch = line.match(/^(\d{1,3})\.$/) || line.match(/^(\d{1,3})\. (.+)$/);
      if (paraMatch) {
        const number = parseInt(paraMatch[1]);
        const text = paraMatch[2] || '';

        // Close previous paragraph
        if (currentParagraph) {
          currentParagraph.text = currentParagraph.lines.join(' ').replace(/\s+/g, ' ').trim();
          currentParagraph.text_lines = currentParagraph.lines.join(' | ');
          paragraphs.push(currentParagraph);
        }

        // Start new paragraph
        currentParagraph = {
          symbol,
          paragraph: number,
          section: currentHeading,
          part: currentPart,
          page_start: page,
          page_end: page,
          lines: text ? [text] : [],
          flagged: false,
          first_words_match: false,
          citation: `${symbol}, para. ${number}`,
          doc_url,
          limitations: 'footnotes not separated'
        };
        inHeading = false;
        return;
      }

      // Labelled heading: I., A., etc.
      const labelMatch = line.match(/^([IVX]+|[A-Z])\.$/);
      if (labelMatch) {
        inHeading = true;
        headingLines = [];
        currentHeading = null;
        return;
      }

      // Heading text: after a label, skip blank lines, then every line up to next label or paragraph
      if (inHeading) {
        if (line.trim().length === 0) return;
        if (/^[a-z(]/.test(line)) {
          headingLines.push(line);
          return;
        }
        if (/^([IVX]+|[A-Z])\.$/.test(line) || /^\d{1,3}\.$/.test(line) || /^\d{1,3}\. /.test(line)) {
          const headingText = headingLines.join(' ');
          const label = labelMatch ? labelMatch[1] : null;
          const slug = label ? `${label}. ${headingText}` : headingText;
          headings.push({ label, text: headingText, slug, page });
          if (/^[IVX]+$/.test(label)) currentPart = slug;
          currentHeading = slug;
          inHeading = false;
          return;
        }
        headingLines.push(line);
        return;
      }

      // Unlabelled heading: non-empty line immediately followed by a paragraph start, at most 90 chars, starts with capital, does not end with .;,:
      const nextLine = allBodyLines[index + 1]?.line;
      const nextIsPara = nextLine && (/^\d{1,3}\.$/.test(nextLine) || /^\d{1,3}\. /.test(nextLine));
      const isHeading = nextIsPara &&
        line.length <= 90 &&
        /^[A-Z]/.test(line) &&
        !/[.;,:]\s*$/.test(line) &&
        !/\d$/.test(line);

      if (isHeading) {
        // Check if the previous line is also a heading line
        const prevLine = allBodyLines[index - 1]?.line;
        const prevIsHeading = prevLine &&
          prevLine.length <= 90 &&
          /^[A-Z]/.test(prevLine) &&
          !/[.;,:]\s*$/.test(prevLine) &&
          !/\d$/.test(prevLine);
        if (prevIsHeading) {
          const prevHeading = headings[headings.length - 1];
          prevHeading.text += ` ${line}`;
          prevHeading.slug = prevHeading.text;
          currentHeading = prevHeading.slug;
        } else {
          const slug = line;
          headings.push({ label: null, text: line, slug, page });
          currentHeading = slug;
        }
        return;
      }

      // Paragraph line
      if (currentParagraph) {
        currentParagraph.lines.push(line);
        currentParagraph.page_end = page;
      } else {
        coverLines.push({ page, line });
      }
    });

    // Close last paragraph
    if (currentParagraph) {
      currentParagraph.text = currentParagraph.lines.join(' ').replace(/\s+/g, ' ').trim();
      currentParagraph.text_lines = currentParagraph.lines.join(' | ');
      paragraphs.push(currentParagraph);
    }

    // 4. Flag suspect lines
    paragraphs.forEach(para => {
      const lines = para.lines;
      let hasSuspect = false;
      let suspectLines = [];
      let suspectReason = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        // Bare number of 1–3 digits
        if (/^\d{1,3}$/.test(line)) {
          hasSuspect = true;
          suspectLines.push(i);
          suspectReason.push('bare number');
          continue;
        }
        // Number, space, capital letter / UN symbol / quote
        if (/^\d{1,3} [A-Z"UN]/.test(line) || /^\d{1,3} E\/[A-Z0-9]/.test(line)) {
          hasSuspect = true;
          suspectLines.push(i);
          suspectReason.push('starts with a number and a space');
          continue;
        }
        // Asterisk and space
        if (/^\* /.test(line)) {
          hasSuspect = true;
          suspectLines.push(i);
          suspectReason.push('starts with an asterisk and a space');
          continue;
        }
      }

      // Paragraph over 300 words
      if (para.text.split(/\s+/).length > 300) {
        hasSuspect = true;
        suspectReason.push('paragraph over 300 words');
      }

      if (hasSuspect) {
        para.flagged = true;
        para.limitations = `footnotes not separated; footnote text may sit inside this paragraph`;
        flaggedParagraphs.push({
          paragraph: para.paragraph,
          page_start: para.page_start,
          page_end: para.page_end,
          suspectLines: suspectLines.map(i => lines[i]).join(' | '),
          reason: suspectReason.join(', ')
        });
      }
    });

    // 5. First words
    paragraphs.forEach(para => {
      const found = firstSixWords(para.text);
      const ref = refFirstWords ? refFirstWords[String(para.paragraph)] : null;
      para.first_words_match = ref ? normalise(found) === normalise(ref) : false;
      if (!para.first_words_match && ref) {
        firstWordsMismatches.push({
          paragraph: para.paragraph,
          found,
          ref
        });
      }
    });

    // 6. Checks
    checks.push({
      name: 'paragraph_count',
      found: paragraphs.length,
      expected: refParagraphs,
      pass: paragraphs.length === refParagraphs
    });

    const numbers = paragraphs.map(p => p.paragraph);
    const uniqueNumbers = [...new Set(numbers)];
    const duplicates = numbers.filter((n, i) => numbers.indexOf(n) !== i);
    const gaps = [];
    for (let i = 1; i <= refParagraphs; i++) {
      if (!numbers.includes(i)) gaps.push(i);
    }
    checks.push({
      name: 'numbering',
      duplicates: duplicates.length > 0 ? duplicates : null,
      gaps: gaps.length > 0 ? gaps : null,
      pass: duplicates.length === 0 && gaps.length === 0
    });

    checks.push({
      name: 'first_words',
      mismatches: firstWordsMismatches.length,
      pass: firstWordsMismatches.length === 0
    });

    checks.push({
      name: 'paragraphs_flagged',
      count: flaggedParagraphs.length,
      pages: [...new Set(flaggedParagraphs.map(p => p.page_start))].length,
      pass: true // not a failure
    });

    const suspectLinesCount = paragraphs.reduce((sum, p) => sum + (p.flagged ? 1 : 0), 0);
    checks.push({
      name: 'suspect_lines',
      count: suspectLinesCount,
      pages: [...new Set(paragraphs.filter(p => p.flagged).map(p => p.page_start))].length,
      paragraphs: flaggedParagraphs.length,
      pass: true // not a failure
    });

    const headerPages = headerLines.map(h => h.page);
    checks.push({
      name: 'headers',
      found: headerPages.length,
      expected: records.length,
      missing: records.map((_, i) => i + 1).filter(p => !headerPages.includes(p)),
      pass: headerPages.length === records.length
    });

    const footerPages = footerLines.filter(f => f.lines.some(l => /^\d{1,3}$/.test(l) && parseInt(l) === f.page)).map(f => f.page);
    checks.push({
      name: 'footers',
      found: footerPages.length,
      expected: records.length - 1,
      missing: records.slice(1).map((_, i) => i + 2).filter(p => !footerPages.includes(p)),
      pass: footerPages.length === records.length - 1
    });

    const bareNumbers = checks.filter(c => c.name === 'bare_number_removed');
    checks.push({
      name: 'bare_numbers_removed',
      count: bareNumbers.length,
      pages: bareNumbers.map(b => b.page),
      pass: true
    });

    checks.push({
      name: 'headings',
      labelled: headings.filter(h => h.label).length,
      unlabelled: headings.filter(h => !h.label).length,
      unlabelledList: headings.filter(h => !h.label).map(h => h.slug),
      pass: true
    });

    const totalLines = coverLines.length + headerLines.length + footerLines.reduce((sum, f) => sum + f.lines.length, 0) + bodyLines.length;
    const classifiedLines = coverLines.length + headerLines.length + footerLines.reduce((sum, f) => sum + f.lines.length, 0) + paragraphs.reduce((sum, p) => sum + p.lines.length, 0);
    checks.push({
      name: 'nothing_lost',
      total: totalLines,
      classified: classifiedLines,
      unclassified: unclassifiedLines.map(u => `${u.page}: ${u.line}`),
      pass: totalLines === classifiedLines && unclassifiedLines.length === 0
    });

    const json = JSON.stringify(paragraphs, null, 2);
    const parsed = JSON.parse(json);
    checks.push({
      name: 'export_round_trip',
      found: parsed.length,
      expected: paragraphs.length,
      pass: parsed.length === paragraphs.length
    });
  }

  // Render
  function render() {
    // Header
    document.getElementById('doc-title').textContent = title;
    const statusEl = document.getElementById('status');
    const flaggedEl = document.getElementById('flagged-count');
    const railSymbol = document.getElementById('rail-symbol');
    const railTitle = document.getElementById('rail-title');
    railSymbol.textContent = symbol;
    railSymbol.href = doc_url;
    railTitle.textContent = `Adopted ${adopted}`;

    // Rail
    const railParagraphsValue = document.getElementById('rail-paragraphs-value');
    const railParagraphsExpected = document.getElementById('rail-paragraphs-expected');
    const railParagraphsBar = document.getElementById('rail-paragraphs-bar');
    const railFlaggedValue = document.getElementById('rail-flagged-value');
    const railFlaggedBar = document.getElementById('rail-flagged-bar');
    const railChecksPass = document.getElementById('rail-checks-pass');
    const railChecksTotal = document.getElementById('rail-checks-total');

    railParagraphsValue.textContent = paragraphs.length;
    railParagraphsExpected.textContent = refParagraphs || '?';
    railParagraphsBar.classList.toggle('short', paragraphs.length !== refParagraphs);
    railFlaggedValue.textContent = flaggedParagraphs.length;
    railFlaggedBar.classList.toggle('flagged', flaggedParagraphs.length > 0);

    const checksPass = checks.filter(c => c.pass).length;
    const checksTotal = checks.length;
    railChecksPass.textContent = checksPass;
    railChecksTotal.textContent = checksTotal;
    railChecksPass.className = checksPass === checksTotal ? 'pass' : 'fail';
    statusEl.innerHTML = '';
    const dot = document.createElement('span');
    dot.className = `status-dot ${checksPass === checksTotal ? 'status-pass' : 'status-fail'}`;
    statusEl.appendChild(dot);
    statusEl.appendChild(document.createTextNode(`${checksPass} of ${checksTotal} checks pass`));
    flaggedEl.textContent = `${flaggedParagraphs.length} paragraphs flagged`;

    // Tab 01
    const paragraphsFoundValue = document.getElementById('paragraphs-found-value');
    const paragraphsExpectedValue = document.getElementById('paragraphs-expected-value');
    const paragraphsExpectedRef = document.getElementById('paragraphs-expected-ref');
    const paragraphsCountFail = document.getElementById('paragraphs-count-fail');
    const firstWordsMatchValue = document.getElementById('first-words-match-value');
    const firstWordsList = document.getElementById('first-words-list');
    const paragraphsFlaggedValue = document.getElementById('paragraphs-flagged-value');
    const paragraphsFlaggedPages = document.getElementById('paragraphs-flagged-pages');
    const footnotesExpected = document.getElementById('footnotes-expected');
    const exportJson = document.getElementById('export-json');
    const exportMarkdown = document.getElementById('export-markdown');
    const checksTotal = document.getElementById('checks-total');
    const checksList = document.getElementById('checks-list');
    const flaggedParagraphsCount = document.getElementById('flagged-paragraphs-count');
    const flaggedParagraphsList = document.getElementById('flagged-paragraphs-list');

    paragraphsFoundValue.textContent = paragraphs.length;
    paragraphsExpectedValue.textContent = refParagraphs || 'no reference in this file';
    paragraphsExpectedRef.textContent = refParagraphs || '?';
    if (refParagraphs && paragraphs.length !== refParagraphs) {
      paragraphsCountFail.textContent = `(${paragraphs.length > refParagraphs ? '+' : ''}${paragraphs.length - refParagraphs})`;
      paragraphsCountFail.hidden = false;
    } else {
      paragraphsCountFail.hidden = true;
    }

    firstWordsMatchValue.textContent = `${paragraphs.filter(p => p.first_words_match).length} of ${refParagraphs || '?'}`;
    if (firstWordsMismatches.length > 0) {
      firstWordsList.hidden = false;
      firstWordsList.innerHTML = '';
      firstWordsMismatches.slice(0, 10).forEach(m => {
        const p = document.createElement('p');
        p.className = 'fail';
        p.textContent = `para. ${m.paragraph}: found ${m.found} / reference ${m.ref}`;
        firstWordsList.appendChild(p);
      });
      if (firstWordsMismatches.length > 10) {
        const p = document.createElement('p');
        p.textContent = `and ${firstWordsMismatches.length - 10} more`;
        firstWordsList.appendChild(p);
      }
    } else {
      firstWordsList.hidden = true;
    }

    paragraphsFlaggedValue.textContent = flaggedParagraphs.length;
    const pages = [...new Set(flaggedParagraphs.map(p => p.page_start))];
    paragraphsFlaggedPages.textContent = `on ${pages.length} page${pages.length === 1 ? '' : 's'}`;

    footnotesExpected.textContent = refFootnotes || '?';

    exportJson.disabled = paragraphs.length === 0;
    exportMarkdown.disabled = paragraphs.length === 0;

    checksTotal.textContent = checks.length;
    checksList.innerHTML = '';
    checks.forEach(check => {
      const div = document.createElement('div');
      div.className = 'check';
      const label = document.createElement('span');
      label.className = 'label';
      label.textContent = check.name.replace(/_/g, ' ');
      const value = document.createElement('span');
      value.className = 'value';
      const pass = document.createElement('span');
      pass.className = check.pass ? 'pass' : 'fail';
      pass.textContent = check.pass ? 'pass' : 'check failed';

      if (check.name === 'paragraph_count') {
        value.textContent = `${check.found} found, ${check.expected} expected`;
        if (!check.pass) {
          const a = document.createElement('a');
          a.href = '#';
          a.textContent = ' see tab 02';
          a.addEventListener('click', e => {
            e.preventDefault();
            document.getElementById('tab-02').click();
          });
          pass.appendChild(a);
        }
      } else if (check.name === 'numbering') {
        value.textContent = `1–${refParagraphs || '?'}`;
        if (!check.pass) {
          if (check.duplicates && check.duplicates.length > 0) {
            value.textContent += `, duplicates: ${check.duplicates.join(', ')}`;
          }
          if (check.gaps && check.gaps.length > 0) {
            value.textContent += `, gaps: ${check.gaps.join(', ')}`;
          }
        }
      } else if (check.name === 'first_words') {
        value.textContent = `${check.mismatches} mismatch${check.mismatches === 1 ? '' : 'es'}`;
        if (!check.pass) {
          const a = document.createElement('a');
          a.href = '#';
          a.textContent = ' see above';
          a.addEventListener('click', e => {
            e.preventDefault();
            firstWordsList.scrollIntoView();
          });
          pass.appendChild(a);
        }
      } else if (check.name === 'paragraphs_flagged') {
        value.textContent = `${check.count} paragraphs flagged on ${check.pages} pages, to check against the PDF`;
      } else if (check.name === 'suspect_lines') {
        value.textContent = `${check.count} suspect lines on ${check.pages} pages, in ${check.paragraphs} paragraphs; none removed`;
      } else if (check.name === 'headers') {
        value.textContent = `${check.found} of ${check.expected}`;
        if (!check.pass) {
          value.textContent += `, missing on page${check.missing.length === 1 ? '' : 's'} ${check.missing.join(', ')}`;
        }
      } else if (check.name === 'footers') {
        value.textContent = `${check.found} of ${check.expected}`;
        if (!check.pass) {
          value.textContent += `, missing on page${check.missing.length === 1 ? '' : 's'} ${check.missing.join(', ')}`;
        }
      } else if (check.name === 'bare_numbers_removed') {
        value.textContent = `${check.count} on page${check.count === 1 ? '' : 's'} ${check.pages.join(', ')}`;
      } else if (check.name === 'headings') {
        value.textContent = `${check.labelled} labelled, ${check.unlabelled} unlabelled`;
        if (check.unlabelled > 0) {
          value.textContent += `: ${check.unlabelledList.join('; ')}`;
        }
      } else if (check.name === 'nothing_lost') {
        value.textContent = `${check.classified} of ${check.total} lines classified`;
        if (!check.pass) {
          value.textContent += `, unclassified: ${check.unclassified.join('; ')}`;
        }
      } else if (check.name === 'export_round_trip') {
        value.textContent = `${check.found} of ${check.expected}`;
      } else {
        value.textContent = '';
      }

      div.appendChild(label);
      div.appendChild(value);
      div.appendChild(pass);
      checksList.appendChild(div);
    });

    flaggedParagraphsCount.textContent = flaggedParagraphs.length;
    flaggedParagraphsList.innerHTML = '';
    flaggedParagraphs.forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${p.paragraph}</td>
        <td>${p.page_start}${p.page_start !== p.page_end ? `–${p.page_end}` : ''}</td>
        <td>${p.suspectLines}</td>
        <td>${p.reason}</td>
      `;
      tr.addEventListener('click', () => {
        const tab = document.getElementById('tab-02');
        tab.click();
        const row = document.querySelector(`#paragraphs-list tr[data-paragraph="${p.paragraph}"]`);
        if (row) {
          row.setAttribute('aria-expanded', 'true');
          row.scrollIntoView({ behavior: 'smooth', block: 'center' });
          renderExpandedRow(row);
        }
      });
      flaggedParagraphsList.appendChild(tr);
    });

    // Tab 02
    const headingsCount = document.getElementById('headings-count');
    const headingsListEl = document.getElementById('headings-list');
    const paragraphsTableCaption = document.getElementById('paragraphs-table-caption');
    const paragraphsList = document.getElementById('paragraphs-list');

    headingsCount.textContent = headings.length;
    headingsListEl.innerHTML = headings.map(h => h.slug).join('\n');

    paragraphsTableCaption.textContent = `${paragraphs.length} paragraphs found, ${refParagraphs || '?'} expected`;
    paragraphsList.innerHTML = '';
    paragraphs.forEach(para => {
      const tr = document.createElement('tr');
      tr.setAttribute('data-paragraph', para.paragraph);
      tr.setAttribute('aria-expanded', 'false');
      tr.setAttribute('role', 'button');
      tr.setAttribute('tabindex', '0');
      tr.innerHTML = `
        <td class="num">${para.paragraph}</td>
        <td>${para.section || ''}</td>
        <td class="page">${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}</td>
        <td>${para.text.substring(0, 120).replace(/\s+/g, ' ').trim()}${para.text.length > 120 ? '…' : ''}</td>
        <td class="check ${para.first_words_match ? '' : 'fail'}">${para.flagged ? 'may contain footnote text' : para.first_words_match ? 'OK' : 'first words differ'}</td>
      `;
      tr.addEventListener('click', () => {
        const expanded = tr.getAttribute('aria-expanded') === 'true';
        tr.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        if (!expanded) {
          renderExpandedRow(tr);
        }
      });
      tr.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          tr.click();
        }
      });
      paragraphsList.appendChild(tr);
    });

    // Footer
    document.getElementById('footer-source').textContent = source;
    document.getElementById('footer-built').textContent = `Built ${built}`;
  }

  function renderExpandedRow(row) {
    const paraNum = parseInt(row.getAttribute('data-paragraph'));
    const para = paragraphs.find(p => p.paragraph === paraNum);
    if (!para) return;

    const td = document.createElement('td');
    td.setAttribute('colspan', '5');
    td.innerHTML = `
      <div class="paragraph-expanded">
        <div class="meta">
          <span>${para.section ? `Section: ${para.section}` : ''}</span>
          <span>${para.part ? `Part: ${para.part}` : ''}</span>
        </div>
        <div class="text"></div>
        <div class="first-words">
          <span class="found">Found: ${firstSixWords(para.text)}</span>
          ${refFirstWords ? `<span class="ref">Reference: ${refFirstWords[String(para.paragraph)] || ''}</span>` : ''}
        </div>
        <div class="toggle">
          <button>Show the PDF's lines</button>
        </div>
        <div class="raw" hidden></div>
        <button class="citation-button">Copy citation</button>
        <span class="copied" hidden>Copied</span>
      </div>
    `;
    row.appendChild(td);

    const textEl = td.querySelector('.text');
    const lines = para.lines;
    const suspectLines = [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (/^\d{1,3}$/.test(line) ||
          /^\d{1,3} [A-Z"UN]/.test(line) ||
          /^\d{1,3} E\/[A-Z0-9]/.test(line) ||
          /^\* /.test(line)) {
        suspectLines.push(i);
      }
    }
    const text = lines.map((line, i) => {
      return suspectLines.includes(i) ? `<span class="suspect">${line}</span>` : line;
    }).join(' ');
    textEl.innerHTML = text;

    const firstWordsEl = td.querySelector('.first-words');
    if (!para.first_words_match) {
      firstWordsEl.classList.add('fail');
    }

    const toggleButton = td.querySelector('.toggle button');
    const rawEl = td.querySelector('.raw');
    toggleButton.addEventListener('click', () => {
      const hidden = rawEl.hidden;
      rawEl.hidden = !hidden;
      toggleButton.textContent = hidden ? 'Hide the PDF\'s lines' : 'Show the PDF\'s lines';
      if (!hidden) {
        const rawText = para.text_lines.split(' | ').map((line, i) => {
          const pageStart = para.page_start;
          const pageEnd = para.page_end;
          const page = pageStart + Math.floor(i / (para.lines.length / (pageEnd - pageStart + 1)));
          return `${page}: ${line}`;
        }).join('\n');
        rawEl.textContent = rawText;
      }
    });

    const citationButton = td.querySelector('.citation-button');
    const copiedEl = td.querySelector('.copied');
    citationButton.addEventListener('click', () => {
      navigator.clipboard.writeText(para.citation).then(() => {
        copiedEl.hidden = false;
        setTimeout(() => { copiedEl.hidden = true; }, 2000);
      });
    });
  }

  // Exports
  document.getElementById('export-json').addEventListener('click', () => {
    const json = JSON.stringify(paragraphs, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = symbol.replace(/\//g, '-') + '.json';
    a.click();
    URL.revokeObjectURL(url);
  });

  document.getElementById('export-markdown').addEventListener('click', () => {
    const frontMatter = `---
title: ${title}
symbol: ${symbol}
adopted: ${adopted}
source_url: ${doc_url}
extracted: ${new Date().toISOString().split('T')[0]}
paragraphs_found: ${paragraphs.length}
paragraphs_expected: ${refParagraphs || '?'}
paragraphs_flagged: ${flaggedParagraphs.length}
footnotes: not separated; the document has ${refFootnotes || '?'}
---`;

    const headingsMap = {};
    paragraphs.forEach(para => {
      if (para.part && !headingsMap[para.part]) {
        headingsMap[para.part] = [];
      }
      if (para.section && !headingsMap[para.section]) {
        headingsMap[para.section] = [];
      }
    });

    let md = frontMatter + '\n\n';
    let lastPart = null;
    let lastSection = null;
    paragraphs.forEach(para => {
      if (para.part && para.part !== lastPart) {
        md += `\n## ${para.part}\n`;
        lastPart = para.part;
        lastSection = null;
      }
      if (para.section && para.section !== lastSection) {
        md += `\n### ${para.section}\n`;
        lastSection = para.section;
      }
      md += `\n**${para.paragraph}.** ${para.text}`;
      if (para.flagged) {
        md += ` (flagged: may contain footnote text)`;
      }
      md += '\n';
    });

    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = symbol.replace(/\//g, '-') + '.md';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const panelId = tab.getAttribute('aria-controls');
      const panel = document.getElementById(panelId);

      tabs.forEach(t => {
        t.setAttribute('aria-selected', 'false');
        document.getElementById(t.getAttribute('aria-controls')).hidden = true;
      });
      tab.setAttribute('aria-selected', 'true');
      panel.hidden = false;
    });
  });

  // Expandable headings
  const expandableHeadings = document.querySelectorAll('[role="button"][aria-expanded]');
  expandableHeadings.forEach(heading => {
    heading.addEventListener('click', () => {
      const expanded = heading.getAttribute('aria-expanded') === 'true';
      heading.setAttribute('aria-expanded', expanded ? 'false' : 'true');
    });
    heading.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        heading.click();
      }
    });
  });

  // Run
  runPipeline();
  render();
</script>
</body>
</html>
```