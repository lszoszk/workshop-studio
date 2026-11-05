Here’s the app, built exactly to the plan. It runs the pipeline once on load, shows the result on tab 01, the paragraphs on tab 02, and the checks under a closed heading. The exports are ready to download.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF – E/C.12/GC/27</title>
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
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background: var(--paper);
}
header {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
header .label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  color: var(--ink);
  opacity: 0.7;
}
header h1 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.2rem;
  font-weight: normal;
}
header .meta {
  font-size: 0.8rem;
  opacity: 0.8;
}
header .meta a {
  color: var(--ink);
  text-decoration: none;
}
header .meta a:hover {
  text-decoration: underline;
}
header .status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}
header .status .dot {
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
}
header .status .dot.pass { background: var(--green); }
header .status .dot.fail { background: var(--red); }
main {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}
.left-rail {
  width: 20rem;
  flex-shrink: 0;
}
.left-rail h2 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5rem 0;
  color: var(--ink);
  opacity: 0.7;
}
.card {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.card h3 {
  margin: 0 0 0.5rem 0;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink);
  opacity: 0.7;
}
.card .symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  word-break: break-all;
}
.card .big-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0.5rem 0;
}
.card .big-number .unit {
  font-size: 1rem;
  opacity: 0.7;
}
.card .bar {
  height: 0.2rem;
  background: var(--rule);
  margin: 0.5rem 0;
}
.card .bar .fill {
  height: 100%;
  background: var(--red);
}
.card .flagged {
  color: var(--red);
}
.card .checks {
  font-size: 0.8rem;
  opacity: 0.8;
}
.tabs {
  flex-grow: 1;
  min-width: 0;
}
.tablist {
  display: flex;
  gap: 0.25rem;
  border-bottom: 1px solid var(--rule);
  margin: 0;
  padding: 0;
  list-style: none;
}
.tablist li {
  margin: 0;
  padding: 0;
}
.tablist button {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 0.5rem 1rem;
  border: 1px solid transparent;
  border-bottom: none;
  border-radius: 0.25rem 0.25rem 0 0;
  background: transparent;
  cursor: pointer;
  color: var(--ink);
  opacity: 0.7;
}
.tablist button[aria-selected="true"] {
  opacity: 1;
  border-color: var(--rule);
  border-bottom-color: var(--paper);
  color: var(--red);
}
.tablist button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
.tabpanel {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0 0.25rem 0.25rem 0.25rem;
  padding: 1rem;
}
.tabpanel[hidden] { display: none; }
.tabpanel h2 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 1rem 0;
  color: var(--ink);
  opacity: 0.7;
}
.tabpanel h3 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
}
.tabpanel .how {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-bottom: 1rem;
}
.tabpanel .tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.tile {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.tile h4 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5rem 0;
  color: var(--ink);
  opacity: 0.7;
}
.tile .big-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0.5rem 0;
}
.tile .big-number.fail {
  color: var(--red);
}
.tile .unit {
  font-size: 1rem;
  opacity: 0.7;
}
.tile .mismatch-list {
  font-size: 0.8rem;
  margin-top: 0.5rem;
}
.tile .mismatch-list li {
  margin-bottom: 0.25rem;
}
.tile .flagged {
  color: var(--red);
}
.downloads {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}
.downloads button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
}
.downloads button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.downloads button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
.section-heading {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  margin-bottom: 1rem;
}
.section-heading button {
  width: 100%;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.section-heading button:after {
  content: "▼";
  font-size: 0.6rem;
  opacity: 0.5;
}
.section-heading button[aria-expanded="false"]:after {
  content: "▶";
}
.section-heading button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
.section-heading .content {
  padding: 1rem;
  border-top: 1px solid var(--rule);
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
caption {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  text-align: left;
}
th, td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
th {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink);
  opacity: 0.7;
}
th[scope="col"]:nth-child(4) { text-align: right; }
tr button {
  width: 100%;
  padding: 0.5rem;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
tr button:after {
  content: "▼";
  font-size: 0.6rem;
  opacity: 0.5;
}
tr button[aria-expanded="false"]:after {
  content: "▶";
}
tr button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
tr[aria-expanded="true"] td {
  padding: 0;
}
tr[aria-expanded="true"] .expanded-content {
  padding: 0.5rem;
}
tr .first-line {
  display: inline-block;
  max-width: 30rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
tr .check {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
}
tr .check.ok { color: var(--green); }
tr .check.fail { color: var(--red); }
tr .flagged-row { background: #fff5f5; }
.suspect-line {
  background: #fff0f0;
  border-left: 2px solid var(--red);
  padding-left: 0.25rem;
}
.toggle {
  margin-top: 0.5rem;
  font-size: 0.8rem;
}
.toggle button {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
  cursor: pointer;
}
.toggle button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
.copy-button {
  margin-top: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
  cursor: pointer;
  font-size: 0.8rem;
}
.copy-button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
.copy-feedback {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 0.25rem;
}
footer {
  padding: 1rem;
  border-top: 1px solid var(--rule);
  font-size: 0.8rem;
  opacity: 0.7;
}
[hidden] { display: none !important; }
</style>
</head>
<body>

<header>
  <div>
    <div class="label">UN DOCUMENT · PDF TEXT</div>
    <h1 id="doc-title"></h1>
    <div class="meta">
      <span id="doc-symbol"></span> · adopted <span id="doc-adopted"></span> · <span id="doc-pages"></span> pages · <span id="doc-source"></span>
    </div>
  </div>
  <div class="status">
    <span class="dot" id="status-dot"></span>
    <span id="status-text"></span>
  </div>
</header>

<main>
  <aside class="left-rail">
    <h2>DOCUMENT</h2>
    <div class="card">
      <h3>Symbol</h3>
      <div class="symbol" id="rail-symbol"></div>
      <div id="rail-title"></div>
    </div>
    <div class="card">
      <h3>Paragraphs</h3>
      <div class="big-number" id="rail-paragraphs-found"><span class="unit"></span></div>
      <div class="bar"><div class="fill" id="rail-paragraphs-bar"></div></div>
      <div id="rail-paragraphs-expected"></div>
      <div class="flagged" id="rail-paragraphs-flagged"></div>
    </div>
    <div class="card">
      <h3>Checks</h3>
      <div class="checks" id="rail-checks"></div>
    </div>
  </aside>

  <div class="tabs">
    <ul class="tablist" role="tablist" aria-label="Tabs">
      <li role="presentation"><button id="tab-01-button" role="tab" aria-selected="true" aria-controls="tab-01">01 RESULT</button></li>
      <li role="presentation"><button id="tab-02-button" role="tab" aria-selected="false" aria-controls="tab-02">02 PARAGRAPHS</button></li>
    </ul>

    <div id="tab-01" role="tabpanel" tabindex="0" aria-labelledby="tab-01-button">
      <h2>01 RESULT</h2>
      <h3>Did the app find everything the document has?</h3>

      <div class="tiles">
        <div class="tile">
          <h4>Paragraphs found</h4>
          <div class="big-number" id="tile-paragraphs-found"><span class="unit"></span></div>
          <div id="tile-paragraphs-expected"></div>
        </div>
        <div class="tile">
          <h4>First words match</h4>
          <div class="big-number" id="tile-first-words-match"><span class="unit"></span></div>
          <div id="tile-first-words-expected"></div>
        </div>
        <div class="tile">
          <h4>Paragraphs flagged</h4>
          <div class="big-number flagged" id="tile-paragraphs-flagged"><span class="unit"></span></div>
          <div id="tile-paragraphs-flagged-pages"></div>
        </div>
        <div class="tile">
          <h4>Footnotes</h4>
          <div class="big-number">not separated</div>
          <div id="tile-footnotes-expected"></div>
        </div>
      </div>

      <div id="mismatch-list"></div>

      <h3>Take the paragraphs away</h3>
      <div class="downloads">
        <button id="download-json" disabled>Download JSON</button>
        <button id="download-markdown" disabled>Download Markdown</button>
      </div>

      <div class="section-heading">
        <button aria-expanded="false" aria-controls="checks-content">Every check (<span id="checks-count"></span>)</button>
        <div id="checks-content" hidden>
          <div id="checks-list"></div>
        </div>
      </div>

      <div class="section-heading">
        <button aria-expanded="false" aria-controls="flagged-content">Flagged paragraphs (<span id="flagged-count"></span>)</button>
        <div id="flagged-content" hidden>
          <p>This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.</p>
          <table>
            <caption>Paragraphs flagged: may contain footnote text</caption>
            <thead>
              <tr>
                <th scope="col">Paragraph</th>
                <th scope="col">Page</th>
                <th scope="col">Suspect lines</th>
                <th scope="col">Why</th>
              </tr>
            </thead>
            <tbody id="flagged-table"></tbody>
          </table>
        </div>
      </div>
    </div>

    <div id="tab-02" role="tabpanel" tabindex="0" aria-labelledby="tab-02-button" hidden>
      <h2>02 PARAGRAPHS</h2>
      <h3>What does each paragraph say, and how do I cite it?</h3>

      <div class="section-heading">
        <button aria-expanded="false" aria-controls="headings-content">Headings found: <span id="headings-count"></span></button>
        <div id="headings-content" hidden>
          <div id="headings-list"></div>
        </div>
      </div>

      <table>
        <caption id="paragraphs-caption"></caption>
        <thead>
          <tr>
            <th scope="col">No.</th>
            <th scope="col">Section</th>
            <th scope="col">Page</th>
            <th scope="col">First line</th>
            <th scope="col">Check</th>
          </tr>
        </thead>
        <tbody id="paragraphs-table"></tbody>
      </table>
    </div>
  </div>
</main>

<footer>
  <span id="footer-source"></span> · <span id="footer-built"></span> · Done by this page's code; no model was called and nothing left the browser.
</footer>

<script>
(function () {
  const data = window.WORKSHOP_DATA.pdf_text;
  const doc = {
    title: data.title,
    symbol: data.symbol,
    doc_url: data.doc_url,
    adopted: data.reference.adopted,
    pages: data.count,
    source: data.source,
    reference: data.reference,
    records: data.records
  };

  // Normalise text for comparison: curly quotes, dashes, whitespace
  function normalise(text) {
    return text
      .replace(/[‘’]/g, "'")
      .replace(/[“”]/g, '"')
      .replace(/[–—]/g, '-')
      .replace(/\s+/g, ' ')
      .trim();
  }

  // Pipeline
  const pipeline = {
    pages: [],
    paragraphs: [],
    headings: [],
    checks: {},
    stats: {
      paragraphsFound: 0,
      firstWordsMatch: 0,
      paragraphsFlagged: 0,
      pagesWithFlagged: 0,
      suspectLines: 0,
      pagesWithSuspectLines: 0,
      bareNumbersRemoved: 0,
      pagesWithBareNumbers: [],
      headersFound: 0,
      footersWithPageNumber: 0,
      unlabelledHeadings: [],
      unclassifiedLines: [],
      hyphenatedLines: 0
    }
  };

  // Step 1: classify each line of each page
  doc.records.forEach(record => {
    const page = record.page;
    const lines = record.text.split(/\r?\n/).filter(line => line.trim() !== '');
    const classified = {
      page,
      header: [],
      footer: [],
      body: [],
      footnotes: []
    };

    // Header: first line equals symbol
    if (lines[0] === doc.symbol) {
      classified.header.push(lines[0]);
      pipeline.stats.headersFound++;
    } else {
      pipeline.stats.unclassifiedLines.push({page, line: lines[0], reason: 'header not found'});
    }

    // Footer: from the end, drop empty, GE., date stamp, bare number
    let footerStart = lines.length;
    for (let i = lines.length - 1; i >= 0; i--) {
      const line = lines[i];
      if (line.trim() === '') continue;
      if (/^GE\.\d{2}-\d+/.test(line)) {
        classified.footer.unshift(line);
        continue;
      }
      if (/^\d{6} \d{6}$/.test(line)) {
        classified.footer.unshift(line);
        continue;
      }
      if (/^\d{1,3}$/.test(line)) {
        if (parseInt(line) === page) {
          classified.footer.unshift(line);
          pipeline.stats.footersWithPageNumber++;
        } else {
          classified.footer.unshift(line);
          pipeline.stats.bareNumbersRemoved++;
          pipeline.stats.pagesWithBareNumbers.push({page, number: line});
        }
        continue;
      }
      footerStart = i + 1;
      break;
    }

    // Body: everything between header and footer
    classified.body = lines.slice(classified.header.length, footerStart);

    // Footnotes: at the foot of the body, before the footer
    // First footnote: bare number, blank line, text
    // Others: number + space, text
    let footnoteStart = classified.body.length;
    for (let i = classified.body.length - 1; i >= 0; i--) {
      const line = classified.body[i];
      if (line.trim() === '') continue;
      if (/^\d{1,3}$/.test(line)) {
        footnoteStart = i;
        break;
      }
      if (/^\d{1,3} /.test(line)) {
        footnoteStart = i;
        break;
      }
    }
    classified.footnotes = classified.body.slice(footnoteStart);
    classified.body = classified.body.slice(0, footnoteStart);

    pipeline.pages.push(classified);
  });

  // Step 2: concatenate body lines, tag with page
  const bodyLines = [];
  pipeline.pages.forEach(page => {
    page.body.forEach(line => {
      bodyLines.push({page: page.page, line});
    });
  });

  // Step 3: find paragraph starts and headings
  let currentPart = null;
  let currentSection = null;
  let currentHeadingLines = [];
  let inHeading = false;
  let currentParagraph = null;

  bodyLines.forEach((item, index) => {
    const line = item.line;
    const page = item.page;

    // Paragraph start: number alone or number + text
    const paraMatch = line.match(/^(\d{1,3})\.$/) || line.match(/^(\d{1,3})\. (.+)$/);
    if (paraMatch) {
      const number = parseInt(paraMatch[1]);
      const text = paraMatch[2] || '';

      // Close previous paragraph
      if (currentParagraph) {
        currentParagraph.text = currentParagraph.lines.join(' ').replace(/\s+/g, ' ').trim();
        currentParagraph.text_lines = currentParagraph.lines.join(' | ');
        pipeline.paragraphs.push(currentParagraph);
      }

      // New paragraph
      currentParagraph = {
        number,
        part: currentPart,
        section: currentSection,
        lines: text ? [text] : [],
        page_start: page,
        page_end: page,
        flagged: false,
        suspectLines: []
      };
      return;
    }

    // Labelled heading: roman numeral or letter alone
    const labelMatch = line.match(/^([IVX]+|[A-Z])\.$/);
    if (labelMatch) {
      const label = labelMatch[1];
      currentHeadingLines = [line];
      inHeading = true;
      return;
    }

    // Heading text: after a label, skip blank lines, then every line until next label or paragraph
    if (inHeading) {
      if (line.trim() === '') {
        currentHeadingLines.push(line);
        return;
      }
      if (/^[a-z(]/.test(line)) {
        currentHeadingLines.push(line);
        return;
      }
      // End of heading
      const headingText = currentHeadingLines
        .filter(l => l.trim() !== '')
        .map(l => l.replace(/^[IVX]+\. /, '').replace(/^[A-Z]\. /, ''))
        .join(' ');
      const heading = {
        label: currentHeadingLines[0].match(/^([IVX]+|[A-Z])\.$/)[1],
        text: headingText,
        page,
        type: /^[IVX]+$/.test(currentHeadingLines[0].match(/^([IVX]+|[A-Z])\.$/)[1]) ? 'part' : 'section'
      };
      pipeline.headings.push(heading);
      if (heading.type === 'part') currentPart = headingText;
      if (heading.type === 'section') currentSection = headingText;
      inHeading = false;
      currentHeadingLines = [];
      return;
    }

    // Unlabelled heading: non-empty line immediately before a paragraph start
    if (index < bodyLines.length - 1) {
      const nextLine = bodyLines[index + 1].line;
      const nextParaMatch = nextLine.match(/^(\d{1,3})\.$/) || nextLine.match(/^(\d{1,3})\. (.+)$/);
      if (nextParaMatch && line.length <= 90 && /^[A-Z]/.test(line) && !/[.;:,]\d?$/.test(line)) {
        // Check if the line before is also a heading line
        if (index > 0) {
          const prevLine = bodyLines[index - 1].line;
          if (prevLine.length <= 90 && /^[A-Z]/.test(prevLine) && !/[.;:,]\d?$/.test(prevLine)) {
            const combined = prevLine + ' ' + line;
            pipeline.stats.unlabelledHeadings.push({text: combined, page});
            currentSection = combined;
            return;
          }
        }
        pipeline.stats.unlabelledHeadings.push({text: line, page});
        currentSection = line;
        return;
      }
    }

    // Paragraph line
    if (currentParagraph) {
      currentParagraph.lines.push(line);
      if (page > currentParagraph.page_end) currentParagraph.page_end = page;
    }
  });

  // Close last paragraph
  if (currentParagraph) {
    currentParagraph.text = currentParagraph.lines.join(' ').replace(/\s+/g, ' ').trim();
    currentParagraph.text_lines = currentParagraph.lines.join(' | ');
    pipeline.paragraphs.push(currentParagraph);
  }

  // Step 4: flag suspect lines and long paragraphs
  pipeline.paragraphs.forEach(para => {
    para.lines.forEach((line, lineIndex) => {
      // Suspect: bare number, or number + space + capital/UN symbol/quote
      if (/^\d{1,3}$/.test(line)) {
        para.flagged = true;
        para.suspectLines.push({line, reason: 'bare number'});
        return;
      }
      if (/^\d{1,3} [A-Z"E][A-Z/]/.test(line)) {
        para.flagged = true;
        para.suspectLines.push({line, reason: 'number + space + capital'});
        return;
      }
      if (/^\* /.test(line)) {
        para.flagged = true;
        para.suspectLines.push({line, reason: 'asterisk + space'});
        return;
      }
    });

    // Long paragraph
    const wordCount = para.text.split(/\s+/).length;
    if (wordCount > 300) {
      para.flagged = true;
      para.suspectLines.push({line: para.text, reason: 'paragraph over 300 words'});
    }

    // Hyphenated line end
    para.lines.forEach(line => {
      if (line.endsWith('-')) {
        pipeline.stats.hyphenatedLines++;
      }
    });

    if (para.flagged) {
      pipeline.stats.paragraphsFlagged++;
      pipeline.stats.pagesWithFlagged = new Set([...pipeline.stats.pagesWithFlagged, para.page_start]).size;
    }
  });

  // Step 5: first words
  pipeline.paragraphs.forEach(para => {
    // Remove footnote marks: digits glued to word or punctuation
    let cleanText = para.text.replace(/(\w)\d+(\W|$)/g, '$1$2').replace(/(\W)\d+(\W|$)/g, '$1$2');
    // Drop a token of digits alone only when the token before ends with . , or "
    cleanText = cleanText.replace(/(\w[.,"])\s+\d+\s+/, '$1 ');
    const words = cleanText.split(/\s+/).slice(0, 6).join(' ');
    para.first_words = words;

    if (doc.reference.first_words && doc.reference.first_words[para.number]) {
      const refWords = normalise(doc.reference.first_words[para.number]);
      const foundWords = normalise(words);
      para.first_words_match = foundWords === refWords;
      if (para.first_words_match) pipeline.stats.firstWordsMatch++;
    } else {
      para.first_words_match = false;
    }
  });

  // Step 6: citation
  pipeline.paragraphs.forEach(para => {
    para.citation = `${doc.symbol}, para. ${para.number}`;
  });

  // Step 7: checks
  pipeline.stats.paragraphsFound = pipeline.paragraphs.length;

  // Paragraph count
  pipeline.checks.paragraphCount = {
    label: 'Paragraph count',
    found: pipeline.stats.paragraphsFound,
    expected: doc.reference.paragraphs,
    pass: pipeline.stats.paragraphsFound === doc.reference.paragraphs,
    message: pipeline.stats.paragraphsFound === doc.reference.paragraphs ? 'pass' : 'check failed'
  };

  // Numbering
  const numbers = pipeline.paragraphs.map(p => p.number);
  const uniqueNumbers = [...new Set(numbers)];
  const missing = [];
  const duplicates = [];
  for (let i = 1; i <= doc.reference.paragraphs; i++) {
    if (!numbers.includes(i)) missing.push(i);
    if (numbers.filter(n => n === i).length > 1) duplicates.push(i);
  }
  pipeline.checks.numbering = {
    label: 'Numbering',
    found: numbers,
    expected: `1 to ${doc.reference.paragraphs}`,
    pass: missing.length === 0 && duplicates.length === 0,
    message: missing.length === 0 && duplicates.length === 0 ? 'pass' : `check failed: ${missing.length} missing (${missing.join(', ')}), ${duplicates.length} duplicates (${duplicates.join(', ')})`,
    details: {missing, duplicates}
  };

  // First words
  const mismatches = pipeline.paragraphs.filter(p => !p.first_words_match).map(p => p.number);
  pipeline.checks.firstWords = {
    label: 'First words',
    found: pipeline.stats.firstWordsMatch,
    expected: doc.reference.paragraphs,
    pass: mismatches.length === 0,
    message: mismatches.length === 0 ? 'pass' : `check failed: ${mismatches.length} mismatches (para. ${mismatches.slice(0, 10).join(', ')}${mismatches.length > 10 ? ` and ${mismatches.length - 10} more` : ''})`,
    details: {mismatches}
  };

  // Paragraphs flagged
  pipeline.checks.paragraphsFlagged = {
    label: 'Paragraphs flagged',
    found: pipeline.stats.paragraphsFlagged,
    expected: 'n/a',
    pass: true,
    message: `${pipeline.stats.paragraphsFlagged} paragraphs flagged on ${pipeline.stats.pagesWithFlagged} pages, to check against the PDF`
  };

  // Suspect lines
  pipeline.stats.suspectLines = pipeline.paragraphs.reduce((sum, p) => sum + p.suspectLines.length, 0);
  pipeline.stats.pagesWithSuspectLines = new Set(pipeline.paragraphs.filter(p => p.suspectLines.length > 0).map(p => p.page_start)).size;
  pipeline.checks.suspectLines = {
    label: 'Suspect lines',
    found: pipeline.stats.suspectLines,
    expected: 'n/a',
    pass: true,
    message: `${pipeline.stats.suspectLines} suspect lines on ${pipeline.stats.pagesWithSuspectLines} pages, in ${pipeline.stats.paragraphsFlagged} paragraphs; none removed`
  };

  // Headers and footers
  pipeline.checks.headers = {
    label: 'Headers',
    found: pipeline.stats.headersFound,
    expected: doc.records.length,
    pass: pipeline.stats.headersFound === doc.records.length,
    message: pipeline.stats.headersFound === doc.records.length ? 'pass' : `check failed: ${doc.records.length - pipeline.stats.headersFound} pages without header (${pipeline.stats.unclassifiedLines.filter(l => l.reason === 'header not found').map(l => l.page).join(', ')})`
  };
  pipeline.checks.footers = {
    label: 'Footers with page number',
    found: pipeline.stats.footersWithPageNumber,
    expected: doc.records.length - 1, // page 1 has no page number
    pass: pipeline.stats.footersWithPageNumber === doc.records.length - 1,
    message: pipeline.stats.footersWithPageNumber === doc.records.length - 1 ? 'pass' : `check failed: ${doc.records.length - 1 - pipeline.stats.footersWithPageNumber} pages without page number`
  };
  pipeline.checks.bareNumbers = {
    label: 'Bare numbers removed from footer',
    found: pipeline.stats.bareNumbersRemoved,
    expected: 'n/a',
    pass: true,
    message: pipeline.stats.bareNumbersRemoved > 0 ? `${pipeline.stats.bareNumbersRemoved} bare numbers removed (${pipeline.stats.pagesWithBareNumbers.map(n => `p. ${n.page}: ${n.number}`).join(', ')})` : 'none'
  };

  // Headings
  pipeline.checks.headings = {
    label: 'Headings',
    found: pipeline.headings.length,
    expected: 'n/a',
    pass: true,
    message: `${pipeline.headings.filter(h => h.type === 'part').length} parts, ${pipeline.headings.filter(h => h.type === 'section').length} sections, ${pipeline.stats.unlabelledHeadings.length} unlabelled (${pipeline.stats.unlabelledHeadings.map(h => h.text).join(', ')})`
  };

  // Nothing lost
  const totalLines = doc.records.reduce((sum, r) => sum + r.text.split(/\r?\n/).filter(line => line.trim() !== '').length, 0);
  const classifiedLines = pipeline.pages.reduce((sum, p) => sum + p.header.length + p.footer.length + p.body.length + p.footnotes.length, 0);
  pipeline.checks.nothingLost = {
    label: 'Nothing lost',
    found: classifiedLines,
    expected: totalLines,
    pass: classifiedLines === totalLines,
    message: classifiedLines === totalLines ? 'pass' : `check failed: ${totalLines - classifiedLines} lines unclassified (${pipeline.stats.unclassifiedLines.map(l => `p. ${l.page}: ${l.line}`).join(', ')})`
  };

  // Export round trip
  pipeline.checks.exportRoundTrip = {
    label: 'Export round trip',
    found: 'not run',
    expected: pipeline.stats.paragraphsFound,
    pass: null,
    message: 'not run'
  };

  // UI
  function render() {
    // Header
    document.getElementById('doc-title').textContent = doc.title;
    document.getElementById('doc-symbol').innerHTML = `<a href="${doc.doc_url}" target="_blank">${doc.symbol}</a>`;
    document.getElementById('doc-adopted').textContent = doc.adopted;
    document.getElementById('doc-pages').textContent = doc.pages;
    document.getElementById('doc-source').textContent = doc.source;

    // Left rail
    document.getElementById('rail-symbol').textContent = doc.symbol;
    document.getElementById('rail-title').textContent = doc.title;
    document.getElementById('rail-paragraphs-found').textContent = pipeline.stats.paragraphsFound;
    document.getElementById('rail-paragraphs-found').querySelector('.unit').textContent = ` of ${doc.reference.paragraphs}`;
    document.getElementById('rail-paragraphs-bar').style.width = `${Math.min(100, pipeline.stats.paragraphsFound / doc.reference.paragraphs * 100)}%`;
    document.getElementById('rail-paragraphs-expected').textContent = `the document has ${doc.reference.paragraphs}`;
    document.getElementById('rail-paragraphs-flagged').textContent = `${pipeline.stats.paragraphsFlagged} paragraphs flagged`;
    document.getElementById('rail-checks').textContent = `${Object.values(pipeline.checks).filter(c => c.pass !== null).filter(c => c.pass || c.message.includes('check failed')).length} checks failed`;

    // Status dot
    const checksPass = Object.values(pipeline.checks).filter(c => c.pass === true).length;
    const checksFail = Object.values(pipeline.checks).filter(c => c.pass === false).length;
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    if (checksFail === 0) {
      statusDot.className = 'dot pass';
      statusText.textContent = `${checksPass} of ${Object.values(pipeline.checks).length} checks pass`;
    } else {
      statusDot.className = 'dot fail';
      statusText.textContent = `${checksFail} checks failed`;
    }

    // Tab 01: Result
    document.getElementById('tile-paragraphs-found').textContent = pipeline.stats.paragraphsFound;
    document.getElementById('tile-paragraphs-found').className = pipeline.stats.paragraphsFound === doc.reference.paragraphs ? 'big-number' : 'big-number fail';
    document.getElementById('tile-paragraphs-found').querySelector('.unit').textContent = ` of ${doc.reference.paragraphs}`;
    document.getElementById('tile-paragraphs-expected').textContent = `the document has ${doc.reference.paragraphs}`;

    document.getElementById('tile-first-words-match').textContent = pipeline.stats.firstWordsMatch;
    document.getElementById('tile-first-words-match').className = pipeline.stats.firstWordsMatch === doc.reference.paragraphs ? 'big-number' : 'big-number fail';
    document.getElementById('tile-first-words-match').querySelector('.unit').textContent = ` of ${doc.reference.paragraphs}`;

    document.getElementById('tile-paragraphs-flagged').textContent = pipeline.stats.paragraphsFlagged;
    document.getElementById('tile-paragraphs-flagged-pages').textContent = `on ${pipeline.stats.pagesWithFlagged} pages`;

    document.getElementById('tile-footnotes-expected').textContent = `the document has ${doc.reference.footnotes}; this version leaves them in place and flags them`;

    // Mismatch list
    const mismatchList = document.getElementById('mismatch-list');
    mismatchList.innerHTML = '';
    if (pipeline.checks.firstWords.details.mismatches.length > 0) {
      const list = document.createElement('ul');
      list.className = 'mismatch-list';
      pipeline.checks.firstWords.details.mismatches.slice(0, 10).forEach(num => {
        const para = pipeline.paragraphs.find(p => p.number === num);
        const li = document.createElement('li');
        li.textContent = `para. ${num}: found "${para.first_words}" / reference "${doc.reference.first_words[num]}"`;
        list.appendChild(li);
      });
      if (pipeline.checks.firstWords.details.mismatches.length > 10) {
        const li = document.createElement('li');
        li.textContent = `and ${pipeline.checks.firstWords.details.mismatches.length - 10} more`;
        list.appendChild(li);
      }
      mismatchList.appendChild(list);
    }

    // Downloads
    const downloadJson = document.getElementById('download-json');
    const downloadMarkdown = document.getElementById('download-markdown');
    if (pipeline.stats.paragraphsFound > 0) {
      downloadJson.disabled = false;
      downloadMarkdown.disabled = false;
    }

    // Checks
    const checksList = document.getElementById('checks-list');
    checksList.innerHTML = '';
    const checksCount = document.getElementById('checks-count');
    checksCount.textContent = Object.keys(pipeline.checks).length;

    Object.values(pipeline.checks).forEach(check => {
      const div = document.createElement('div');
      div.style.marginBottom = '0.5rem';
      div.style.paddingBottom = '0.5rem';
      div.style.borderBottom = '1px solid var(--rule)';

      const label = document.createElement('div');
      label.style.fontFamily = 'ui-monospace, Menlo, Consolas, monospace';
      label.style.fontSize = '0.8rem';
      label.style.letterSpacing = '0.05em';
      label.style.textTransform = 'uppercase';
      label.style.opacity = '0.7';
      label.textContent = check.label;
      div.appendChild(label);

      const found = document.createElement('div');
      found.style.fontSize = '0.9rem';
      found.textContent = `Found: ${check.found}`;
      div.appendChild(found);

      const expected = document.createElement('div');
      expected.style.fontSize = '0.9rem';
      expected.style.marginBottom = '0.25rem';
      expected.textContent = `Expected: ${check.expected}`;
      div.appendChild(expected);

      const message = document.createElement('div');
      message.style.fontSize = '0.9rem';
      message.style.color = check.pass === true ? 'var(--green)' : check.pass === false ? 'var(--red)' : 'var(--ink)';
      if (check.pass === false && check.details && (check.details.missing || check.details.duplicates || check.details.mismatches)) {
        const link = document.createElement('button');
        link.style.background = 'none';
        link.style.border = 'none';
        link.style.padding = '0';
        link.style.color = 'var(--red)';
        link.style.textDecoration = 'underline';
        link.style.cursor = 'pointer';
        link.style.fontSize = '0.9rem';
        link.textContent = check.message;
        link.addEventListener('click', () => {
          const tabButton = document.getElementById('tab-02-button');
          tabButton.click();
          if (check.details.missing || check.details.duplicates) {
            const rows = document.querySelectorAll('#paragraphs-table tr');
            rows.forEach(row => {
              const num = parseInt(row.querySelector('th').textContent);
              if (check.details.missing.includes(num) || check.details.duplicates.includes(num)) {
                row.scrollIntoView();
                row.style.background = '#fff5f5';
              }
            });
          }
          if (check.details.mismatches) {
            const rows = document.querySelectorAll('#paragraphs-table tr');
            rows.forEach(row => {
              const num = parseInt(row.querySelector('th').textContent);
              if (check.details.mismatches.includes(num)) {
                row.scrollIntoView();
                row.style.background = '#fff5f5';
              }
            });
          }
        });
        message.appendChild(link);
      } else {
        message.textContent = check.message;
      }
      div.appendChild(message);

      checksList.appendChild(div);
    });

    // Flagged paragraphs
    const flaggedTable = document.getElementById('flagged-table');
    flaggedTable.innerHTML = '';
    const flaggedCount = document.getElementById('flagged-count');
    flaggedCount.textContent = pipeline.stats.paragraphsFlagged;

    pipeline.paragraphs.filter(p => p.flagged).forEach(para => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <th scope="row">${para.number}</th>
        <td>${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}</td>
        <td>${para.suspectLines.length}</td>
        <td>${para.suspectLines.map(s => s.reason).join(', ')}</td>
      `;
      tr.addEventListener('click', () => {
        const tabButton = document.getElementById('tab-02-button');
        tabButton.click();
        const rows = document.querySelectorAll('#paragraphs-table tr');
        rows.forEach(row => {
          if (row.querySelector('th').textContent === String(para.number)) {
            row.scrollIntoView();
            const button = row.querySelector('button');
            button.click();
          }
        });
      });
      flaggedTable.appendChild(tr);
    });

    // Tab 02: Paragraphs
    document.getElementById('paragraphs-caption').textContent = `${pipeline.stats.paragraphsFound} paragraphs found, ${doc.reference.paragraphs} expected`;

    const paragraphsTable = document.getElementById('paragraphs-table');
    paragraphsTable.innerHTML = '';

    pipeline.paragraphs.forEach(para => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <th scope="row">${para.number}</th>
        <td>${para.section || ''}</td>
        <td>${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}</td>
        <td><span class="first-line">${para.first_words}</span></td>
        <td><span class="check ${para.first_words_match ? 'ok' : 'fail'}">${para.first_words_match ? 'OK' : 'first words differ'}</span> <span class="check ${para.flagged ? 'fail' : 'ok'}">${para.flagged ? 'may contain footnote text' : ''}</span></td>
      `;
      if (para.flagged) tr.className = 'flagged-row';

      const button = document.createElement('button');
      button.setAttribute('aria-expanded', 'false');
      button.innerHTML = `
        <span>${para.number}</span>
        <span>▼</span>
      `;
      tr.querySelector('th').innerHTML = '';
      tr.querySelector('th').appendChild(button);

      const expandedContent = document.createElement('td');
      expandedContent.setAttribute('colspan', '5');
      expandedContent.innerHTML = `
        <div class="expanded-content" hidden>
          <div style="margin-bottom: 0.5rem;">
            <strong>Section:</strong> ${para.part ? `${para.part} › ${para.section}` : para.section || ''}
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Page:</strong> ${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>First words:</strong> found "${para.first_words}" / reference "${doc.reference.first_words ? doc.reference.first_words[para.number] || 'not in reference' : 'no reference'}"
          </div>
          <div style="margin-bottom: 0.5rem;">
            <strong>Text:</strong>
            <div style="white-space: pre-wrap; margin-top: 0.25rem;"></div>
          </div>
          <div class="toggle">
            <button>Show the PDF's lines</button>
          </div>
          <button class="copy-button">Copy citation</button>
          <div class="copy-feedback"></div>
        </div>
      `;
      tr.appendChild(expandedContent);

      button.addEventListener('click', () => {
        const expanded = expandedContent.querySelector('.expanded-content');
        const isExpanded = expanded.hidden;
        expanded.hidden = !isExpanded;
        button.setAttribute('aria-expanded', isExpanded);
        button.querySelector('span:last-child').textContent = isExpanded ? '▲' : '▼';

        if (isExpanded) {
          const textDiv = expanded.querySelector('div div');
          textDiv.innerHTML = para.text
            .split(/\n/)
            .map(line => {
              const suspect = para.suspectLines.find(s => s.line === line);
              return suspect ? `<span class="suspect-line">${line}</span>` : line;
            })
            .join('\n');
        }
      });

      const toggleButton = expandedContent.querySelector('.toggle button');
      toggleButton.addEventListener('click', () => {
        const textDiv = expandedContent.querySelector('div div');
        if (toggleButton.textContent === 'Show the PDF\'s lines') {
          textDiv.innerHTML = para.text_lines
            .split(' | ')
            .map((line, i) => {
              const page = para.page_start + Math.floor(i / para.lines.length * (para.page_end - para.page_start + 1));
              return `<span style="opacity: 0.7;">[p. ${page}] </span>${line}`;
            })
            .join('\n');
          toggleButton.textContent = 'Show clean text';
        } else {
          textDiv.innerHTML = para.text
            .split(/\n/)
            .map(line => {
              const suspect = para.suspectLines.find(s => s.line === line);
              return suspect ? `<span class="suspect-line">${line}</span>` : line;
            })
            .join('\n');
          toggleButton.textContent = 'Show the PDF\'s lines';
        }
      });

      const copyButton = expandedContent.querySelector('.copy-button');
      copyButton.addEventListener('click', () => {
        navigator.clipboard.writeText(para.citation).then(() => {
          const feedback = expandedContent.querySelector('.copy-feedback');
          feedback.textContent = 'Copied';
          setTimeout(() => { feedback.textContent = ''; }, 2000);
        });
      });

      paragraphsTable.appendChild(tr);
    });

    // Headings
    const headingsList = document.getElementById('headings-list');
    headingsList.innerHTML = '';
    const headingsCount = document.getElementById('headings-count');
    headingsCount.textContent = pipeline.headings.length + pipeline.stats.unlabelledHeadings.length;

    pipeline.headings.forEach(heading => {
      const div = document.createElement('div');
      div.style.marginBottom = '0.25rem';
      div.textContent = `${heading.label}. ${heading.text} (p. ${heading.page})`;
      headingsList.appendChild(div);
    });
    pipeline.stats.unlabelledHeadings.forEach(heading => {
      const div = document.createElement('div');
      div.style.marginBottom = '0.25rem';
      div.textContent = `${heading.text} (p. ${heading.page})`;
      headingsList.appendChild(div);
    });

    // Footer
    document.getElementById('footer-source').textContent = doc.source;
    document.getElementById('footer-built').textContent = new Date().toISOString().split('T')[0];

    // Tabs
    const tabButtons = document.querySelectorAll('[role="tab"]');
    tabButtons.forEach(button => {
      button.addEventListener('click', () => {
        const tabId = button.getAttribute('aria-controls');
        const tabPanel = document.getElementById(tabId);

        tabButtons.forEach(b => {
          b.setAttribute('aria-selected', 'false');
          document.getElementById(b.getAttribute('aria-controls')).hidden = true;
        });
        button.setAttribute('aria-selected', 'true');
        tabPanel.hidden = false;
        tabPanel.focus();
      });
    });

    // Downloads
    downloadJson.addEventListener('click', () => {
      const json = pipeline.paragraphs.map(para => ({
        symbol: doc.symbol,
        paragraph: para.number,
        section: para.section,
        part: para.part,
        page_start: para.page_start,
        page_end: para.page_end,
        text: para.text,
        flagged: para.flagged,
        first_words_match: para.first_words_match,
        citation: para.citation,
        doc_url: doc.doc_url,
        limitations: para.flagged ? `footnotes not separated; ${para.suspectLines.length} may sit inside this paragraph` : 'footnotes not separated',
        text_lines: para.text_lines
      }));
      const blob = new Blob([JSON.stringify(json, null, 2)], {type: 'application/json'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.symbol.replace(/\//g, '-') + '.json';
      a.click();
      URL.revokeObjectURL(url);

      // Export round trip check
      try {
        const parsed = JSON.parse(JSON.stringify(json));
        pipeline.checks.exportRoundTrip.found = parsed.length;
        pipeline.checks.exportRoundTrip.pass = parsed.length === pipeline.stats.paragraphsFound;
        pipeline.checks.exportRoundTrip.message = parsed.length === pipeline.stats.paragraphsFound ? 'pass' : 'check failed';
      } catch {
        pipeline.checks.exportRoundTrip.found = 'error';
        pipeline.checks.exportRoundTrip.pass = false;
        pipeline.checks.exportRoundTrip.message = 'check failed: invalid JSON';
      }
      render();
    });

    downloadMarkdown.addEventListener('click', () => {
      const frontMatter = `---
title: ${doc.title}
symbol: ${doc.symbol}
adopted: ${doc.adopted}
source_url: ${doc.doc_url}
extracted: ${new Date().toISOString().split('T')[0]}
paragraphs_found: ${pipeline.stats.paragraphsFound}
paragraphs_expected: ${doc.reference.paragraphs}
paragraphs_flagged: ${pipeline.stats.paragraphsFlagged}
footnotes: not separated; the document has ${doc.reference.footnotes}
---`;

      const headings = {};
      pipeline.paragraphs.forEach(para => {
        if (para.part) {
          if (!headings[para.part]) headings[para.part] = [];
          if (para.section && !headings[para.part].includes(para.section)) {
            headings[para.part].push(para.section);
          }
        }
      });

      let markdown = frontMatter + '\n\n';
      let currentPart = null;
      let currentSection = null;

      pipeline.paragraphs.forEach(para => {
        if (para.part && para.part !== currentPart) {
          markdown += `\n## ${para.part}\n`;
          currentPart = para.part;
          currentSection = null;
        }
        if (para.section && para.section !== currentSection) {
          markdown += `\n### ${para.section}\n`;
          currentSection = para.section;
        }
        markdown += `\n**${para.number}.** ${para.text}${para.flagged ? ' *(flagged: may contain footnote text)*' : ''}\n`;
      });

      const blob = new Blob([markdown], {type: 'text/markdown'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.symbol.replace(/\//g, '-') + '.md';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  render();
})();
</script>

</body>
</html>
```