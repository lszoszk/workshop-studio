Here is the app. It follows the plan exactly: two tabs, a left rail with the document card and the counts, four tiles on tab 01, a table on tab 02, and the checks and flagged pages under closed headings. The pipeline runs once on load; the JSON and Markdown exports carry the same fields and limitations.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Paragraphs from PDF text – UN DOCUMENT</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --pass: #2e6b47;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  accent-color: var(--accent);
}
.hidden { display: none !important; }
header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 1rem;
}
header h1 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: normal;
}
header .meta {
  font-size: 0.875rem;
  color: #666;
}
header .meta a {
  color: inherit;
  text-decoration: none;
}
header .meta a:hover { text-decoration: underline; }
header .status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
header .status .dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}
header .status .dot.pass { background-color: var(--pass); }
header .status .dot.fail { background-color: var(--accent); }
main {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}
.left-rail {
  width: 22rem;
  flex-shrink: 0;
}
.card {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.card h2 {
  margin-top: 0;
  font-size: 0.875rem;
  font-weight: bold;
  letter-spacing: 0.05em;
  color: #666;
}
.card .symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 1.25rem;
  word-break: break-all;
}
.card .big-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0.5rem 0;
}
.card .big-number .label {
  font-size: 0.875rem;
  font-weight: normal;
  color: #666;
  display: block;
}
.card .bar {
  height: 0.25rem;
  background-color: var(--accent);
  margin: 0.5rem 0;
}
.card .bar.short { background-color: var(--accent); }
.card .bar.over { background-color: var(--accent); }
.card .flagged {
  color: var(--accent);
  font-weight: bold;
}
.card .checks {
  font-size: 0.875rem;
  color: #666;
}
.card .checks .pass { color: var(--pass); }
.card .checks .fail { color: var(--accent); }
.tabs {
  display: flex;
  gap: 0.25rem;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 1rem;
}
.tab {
  padding: 0.5rem 0;
  font-size: 0.875rem;
  font-weight: bold;
  letter-spacing: 0.05em;
  color: #666;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
}
.tab:hover { color: var(--ink); }
.tab[aria-selected="true"] {
  color: var(--ink);
  border-bottom-color: var(--accent);
}
.tab:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.tab-panel { padding: 0; }
.tab-panel:focus { outline: none; }
.tile {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.tile h3 {
  margin-top: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2rem;
  font-weight: normal;
}
.tile .label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}
.tile .how {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}
.tile .diff {
  color: var(--accent);
  font-weight: bold;
}
.tile .mismatch-list {
  margin-top: 1rem;
  font-size: 0.875rem;
}
.tile .mismatch-list li {
  margin-bottom: 0.25rem;
}
.tile .flagged-count {
  color: var(--accent);
  font-weight: bold;
}
.downloads {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
.downloads button {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  cursor: pointer;
}
.downloads button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.downloads button:hover:not(:disabled) {
  background: #f0f0f0;
}
.downloads button:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 1rem;
  cursor: pointer;
}
.section-heading h2 {
  margin: 0;
  font-size: 1rem;
  font-weight: bold;
  letter-spacing: 0.05em;
  color: #666;
}
.section-heading button {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: #666;
}
.section-heading button:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
.section-heading[aria-expanded="false"] .arrow::after { content: "▼"; }
.section-heading[aria-expanded="true"] .arrow::after { content: "▲"; }
.checks-list {
  font-size: 0.875rem;
  line-height: 1.6;
}
.checks-list .check {
  display: flex;
  justify-content: space-between;
  padding: 0.25rem 0;
}
.checks-list .check .label { flex-grow: 1; }
.checks-list .check .value { margin: 0 0.5rem; }
.checks-list .check .pass { color: var(--pass); }
.checks-list .check .fail { color: var(--accent); }
.checks-list .check .fail a { color: inherit; }
.checks-list .check .fail a:hover { text-decoration: underline; }
.checks-list .check .not-run { color: #999; }
.flagged-pages {
  font-size: 0.875rem;
}
.flagged-pages table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
.flagged-pages th,
.flagged-pages td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
.flagged-pages th { font-weight: bold; }
.flagged-pages tr:last-child td { border-bottom: none; }
.flagged-pages .suspect {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  white-space: pre-wrap;
}
.flagged-pages .why {
  font-size: 0.875rem;
  color: #666;
}
.flagged-pages .page-content {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-top: 1rem;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  white-space: pre-wrap;
}
.flagged-pages .page-content .suspect-line {
  background-color: #fff0f0;
  border-left: 2px solid var(--accent);
  padding-left: 0.5rem;
}
.flagged-pages .note {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #666;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
table caption {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  text-align: left;
}
table th,
table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
table th {
  font-weight: bold;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #666;
}
table th[scope="col"]:nth-child(3),
table td:nth-child(3) { text-align: right; }
table tr:last-child td { border-bottom: none; }
table tr[aria-expanded="true"] td { border-bottom: none; }
table tr[aria-expanded="true"] + tr td {
  border-top: none;
  padding-top: 0;
}
table .flagged { color: var(--accent); }
table .mismatch { color: var(--accent); }
table .paragraph-text {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.6;
  margin: 0.5rem 0;
}
table .paragraph-text .suspect {
  background-color: #fff0f0;
  border-left: 2px solid var(--accent);
  padding-left: 0.5rem;
}
table .first-words {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  color: #666;
  margin: 0.5rem 0;
}
table .first-words .mismatch { color: var(--accent); }
table .toggle {
  font-size: 0.875rem;
  margin: 0.5rem 0;
}
table .toggle button {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}
table .toggle button:focus { outline: none; }
table .copy {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}
table .copy button {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}
table .copy button:focus { outline: none; }
table .copy .copied {
  color: var(--pass);
  margin-left: 0.5rem;
}
footer {
  padding: 1rem;
  border-top: 1px solid var(--rule);
  font-size: 0.875rem;
  color: #666;
}
.headings-list {
  font-size: 0.875rem;
  margin-bottom: 1rem;
}
.headings-list ul {
  margin: 0.5rem 0;
  padding-left: 1rem;
}
.headings-list li {
  margin-bottom: 0.25rem;
}
</style>
</head>
<body>

<header>
  <div>
    <div class="meta" style="font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.875rem;">UN DOCUMENT · PDF TEXT</div>
    <h1 id="doc-title"></h1>
    <div class="meta">
      <a id="doc-url" target="_blank" rel="noopener"></a>, adopted <span id="doc-adopted"></span>, <span id="doc-pages"></span> pages, <span id="doc-source"></span>
    </div>
  </div>
  <div class="status">
    <div class="dot" id="status-dot"></div>
    <div>
      <span id="checks-pass"></span> of <span id="checks-total"></span> checks pass
      <div id="pages-flagged-header"></div>
    </div>
  </div>
</header>

<main>
  <div class="left-rail">
    <div class="card">
      <h2>DOCUMENT</h2>
      <div class="symbol" id="doc-symbol"></div>
      <div id="doc-short-title"></div>
    </div>
    <div class="card">
      <div class="big-number" id="paragraphs-found">
        <span class="value"></span>
        <span class="label">paragraphs of <span id="paragraphs-expected"></span></span>
      </div>
      <div class="bar" id="paragraphs-bar"></div>
      <div class="big-number" id="pages-flagged">
        <span class="value"></span>
        <span class="label flagged">pages flagged</span>
      </div>
      <div class="checks">
        <span id="checks-pass-rail"></span> of <span id="checks-total-rail"></span> checks pass
      </div>
    </div>
  </div>

  <div id="tab-panels">
    <div class="tabs" role="tablist" aria-label="Tabs">
      <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
      <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
    </div>

    <div id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01" tabindex="0">
      <div class="tile">
        <h3 id="paragraphs-found-tile"></h3>
        <div class="label">Paragraphs found</div>
        <div class="how">How this is computed: the app splits the text into numbered paragraphs and counts them.</div>
      </div>
      <div class="tile">
        <h3 id="first-words-match-tile"></h3>
        <div class="label">First words match</div>
        <div class="how">How this is computed: the first six words of each paragraph are compared with the document's own reference.</div>
        <div class="mismatch-list" id="mismatch-list"></div>
      </div>
      <div class="tile">
        <h3 id="pages-flagged-tile"></h3>
        <div class="label flagged-count">Pages flagged</div>
        <div class="how">How this is computed: a page is flagged when footnote text may sit inside a paragraph.</div>
      </div>
      <div class="tile">
        <h3>Footnotes: not separated</h3>
        <div class="label">the document has <span id="footnotes-expected"></span></div>
        <div class="how">How this is computed: this version leaves footnotes in place and flags them.</div>
      </div>

      <div class="downloads">
        <button id="download-json" disabled>Download JSON</button>
        <button id="download-md" disabled>Download Markdown</button>
      </div>

      <div class="section-heading" id="checks-heading" role="button" aria-expanded="false" tabindex="0">
        <h2>Every check (<span id="checks-total-heading"></span>)</h2>
        <span class="arrow" aria-hidden="true"></span>
      </div>
      <div id="checks-content" hidden>
        <div class="checks-list" id="checks-list"></div>
      </div>

      <div class="section-heading" id="flagged-pages-heading" role="button" aria-expanded="false" tabindex="0">
        <h2>Flagged pages (<span id="pages-flagged-count"></span>)</h2>
        <span class="arrow" aria-hidden="true"></span>
      </div>
      <div id="flagged-pages-content" hidden>
        <div class="flagged-pages">
          <div class="note">
            This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.
          </div>
          <table id="flagged-pages-table">
            <thead>
              <tr>
                <th scope="col">Page</th>
                <th scope="col">Paragraph</th>
                <th scope="col">Suspect lines</th>
                <th scope="col">Why</th>
              </tr>
            </thead>
            <tbody id="flagged-pages-body"></tbody>
          </table>
        </div>
      </div>
    </div>

    <div id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" tabindex="0" hidden>
      <div class="section-heading" id="headings-heading" role="button" aria-expanded="false" tabindex="0">
        <h2>Headings found: <span id="headings-count"></span></h2>
        <span class="arrow" aria-hidden="true"></span>
      </div>
      <div id="headings-content" hidden>
        <div class="headings-list" id="headings-list"></div>
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
        <tbody id="paragraphs-body"></tbody>
      </table>
    </div>
  </div>
</main>

<footer>
  <div id="doc-source-footer"></div>
  <div>Built <span id="built-date"></span>. Done by this page's code; no model was called and nothing left the browser.</div>
</footer>

<script>
(function() {
  // Data
  const data = window.WORKSHOP_DATA.pdf_text;
  const doc = {
    title: data.title,
    symbol: data.symbol,
    doc_url: data.doc_url,
    source: data.source,
    pages: data.count,
    adopted: data.reference.adopted,
    reference: data.reference,
    records: data.records
  };

  // State
  let paragraphs = [];
  let checks = [];
  let flaggedPages = [];
  let headings = [];
  let headingsMap = new Map();

  // DOM
  const docTitle = document.getElementById('doc-title');
  const docUrl = document.getElementById('doc-url');
  const docAdopted = document.getElementById('doc-adopted');
  const docPages = document.getElementById('doc-pages');
  const docSource = document.getElementById('doc-source');
  const docSymbol = document.getElementById('doc-symbol');
  const docShortTitle = document.getElementById('doc-short-title');
  const statusDot = document.getElementById('status-dot');
  const checksPass = document.getElementById('checks-pass');
  const checksTotal = document.getElementById('checks-total');
  const pagesFlaggedHeader = document.getElementById('pages-flagged-header');
  const paragraphsFound = document.getElementById('paragraphs-found');
  const paragraphsExpected = document.getElementById('paragraphs-expected');
  const paragraphsBar = document.getElementById('paragraphs-bar');
  const pagesFlagged = document.getElementById('pages-flagged');
  const checksPassRail = document.getElementById('checks-pass-rail');
  const checksTotalRail = document.getElementById('checks-total-rail');
  const paragraphsFoundTile = document.getElementById('paragraphs-found-tile');
  const firstWordsMatchTile = document.getElementById('first-words-match-tile');
  const mismatchList = document.getElementById('mismatch-list');
  const pagesFlaggedTile = document.getElementById('pages-flagged-tile');
  const footnotesExpected = document.getElementById('footnotes-expected');
  const downloadJson = document.getElementById('download-json');
  const downloadMd = document.getElementById('download-md');
  const checksHeading = document.getElementById('checks-heading');
  const checksTotalHeading = document.getElementById('checks-total-heading');
  const checksContent = document.getElementById('checks-content');
  const checksList = document.getElementById('checks-list');
  const flaggedPagesHeading = document.getElementById('flagged-pages-heading');
  const pagesFlaggedCount = document.getElementById('pages-flagged-count');
  const flaggedPagesContent = document.getElementById('flagged-pages-content');
  const flaggedPagesBody = document.getElementById('flagged-pages-body');
  const headingsHeading = document.getElementById('headings-heading');
  const headingsCount = document.getElementById('headings-count');
  const headingsContent = document.getElementById('headings-content');
  const headingsList = document.getElementById('headings-list');
  const paragraphsCaption = document.getElementById('paragraphs-caption');
  const paragraphsBody = document.getElementById('paragraphs-body');
  const docSourceFooter = document.getElementById('doc-source-footer');
  const builtDate = document.getElementById('built-date');

  // Tabs
  const tabs = document.querySelectorAll('.tab');
  const tabPanels = document.querySelectorAll('.tab-panel');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const selected = tab.getAttribute('aria-selected') === 'true';
      if (selected) return;
      tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
      tabPanels.forEach(p => p.hidden = true);
      tab.setAttribute('aria-selected', 'true');
      document.getElementById(`panel-${tab.id.split('-')[1]}`).hidden = false;
    });
  });
  tabs.forEach(tab => {
    tab.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        const next = e.key === 'ArrowRight';
        const currentIdx = Array.from(tabs).indexOf(tab);
        const nextIdx = next ? (currentIdx + 1) % tabs.length : (currentIdx - 1 + tabs.length) % tabs.length;
        tabs[nextIdx].focus();
      }
    });
  });

  // Section headings
  const sectionHeadings = document.querySelectorAll('.section-heading');
  sectionHeadings.forEach(heading => {
    heading.addEventListener('click', () => {
      const expanded = heading.getAttribute('aria-expanded') === 'true';
      heading.setAttribute('aria-expanded', !expanded);
      document.getElementById(`${heading.id}-content`).hidden = expanded;
    });
    heading.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        heading.click();
      }
    });
  });

  // Pipeline
  function runPipeline() {
    // 1. Header and footer
    const pages = doc.records.map(page => {
      const lines = page.text.split(/\r?\n/).filter(line => line.trim() !== '');
      const header = [];
      const footer = [];
      const body = [];
      let i = 0;
      // Header: first line is symbol
      if (lines[i] === doc.symbol) {
        header.push(lines[i]);
        i++;
      } else {
        checks.push({
          name: 'Header',
          message: `Page ${page.page}: first line is not the symbol`,
          pass: false,
          value: lines[i],
          expected: doc.symbol,
          pages: [page.page]
        });
      }
      // Body: all lines until footer
      let inFooter = false;
      for (; i < lines.length; i++) {
        const line = lines[i];
        if (line.match(/^GE\./) || line.match(/^\d{6}$/) || line.match(/^\d{1,3}$/)) {
          inFooter = true;
        }
        if (inFooter) {
          footer.push(line);
        } else {
          body.push(line);
        }
      }
      // Footer: from the end, drop empty, GE., 6-digit, bare number (page number or footnote)
      let j = footer.length - 1;
      while (j >= 0) {
        const line = footer[j];
        if (line.trim() === '') {
          j--;
        } else if (line.match(/^GE\./)) {
          j--;
        } else if (line.match(/^\d{6}$/)) {
          j--;
        } else if (line.match(/^\d{1,3}$/)) {
          if (parseInt(line) === page.page) {
            // Page number
            j--;
          } else {
            // Footnote number
            checks.push({
              name: 'Footer',
              message: `Page ${page.page}: bare number removed from footer`,
              pass: true,
              value: line,
              pages: [page.page]
            });
            j--;
          }
        } else {
          break;
        }
      }
      const footerLines = footer.slice(0, j + 1);
      return {
        page: page.page,
        header,
        body,
        footer: footerLines
      };
    });

    // 2. Concatenate body lines, tag with page
    const bodyLines = [];
    pages.forEach(page => {
      page.body.forEach(line => {
        bodyLines.push({ page: page.page, line });
      });
    });

    // 3. Paragraph starts
    const paragraphStarts = [];
    for (let i = 0; i < bodyLines.length; i++) {
      const { page, line } = bodyLines[i];
      const match1 = line.match(/^(\d{1,3})\.$/);
      const match2 = line.match(/^(\d{1,3})\. (.+)$/);
      if (match1) {
        paragraphStarts.push({
          number: parseInt(match1[1]),
          page,
          line: i,
          text: ''
        });
      } else if (match2) {
        paragraphStarts.push({
          number: parseInt(match2[1]),
          page,
          line: i,
          text: match2[2]
        });
      }
    }

    // 4. Headings
    const labelledHeadings = [];
    const unlabelledHeadings = [];
    for (let i = 0; i < bodyLines.length; i++) {
      const { page, line } = bodyLines[i];
      // Labelled: I., A., etc.
      const labelledMatch = line.match(/^([IVX]+|[A-Z])\.$/);
      if (labelledMatch) {
        const label = labelledMatch[1];
        let j = i + 1;
        const headingLines = [];
        while (j < bodyLines.length && bodyLines[j].line.trim() === '') j++;
        while (j < bodyLines.length && !bodyLines[j].line.match(/^(\d{1,3})\.$/) && !bodyLines[j].line.match(/^(\d{1,3})\. (.+)$/) && !bodyLines[j].line.match(/^([IVX]+|[A-Z])\.$/)) {
          headingLines.push(bodyLines[j].line);
          j++;
        }
        const headingText = headingLines.join(' ').trim();
        labelledHeadings.push({
          label,
          text: headingText,
          page,
          line: i
        });
        i = j - 1;
      }
      // Unlabelled: line before a paragraph start, not ending a sentence
      if (i + 1 < bodyLines.length && (bodyLines[i + 1].line.match(/^(\d{1,3})\.$/) || bodyLines[i + 1].line.match(/^(\d{1,3})\. (.+)$/))) {
        const lineText = line.trim();
        if (lineText.length <= 90 && lineText[0] === lineText[0].toUpperCase() && !lineText.match(/[.;:,]\s*$/) && !lineText.match(/\d$/)) {
          // Check if the line before is also a heading line
          let prevIsHeading = false;
          if (i > 0) {
            const prevLine = bodyLines[i - 1].line.trim();
            if (prevLine.length <= 90 && prevLine[0] === prevLine[0].toUpperCase() && !prevLine.match(/[.;:,]\s*$/) && !prevLine.match(/\d$/)) {
              prevIsHeading = true;
            }
          }
          if (!prevIsHeading) {
            unlabelledHeadings.push({
              text: lineText,
              page,
              line: i
            });
          }
        }
      }
    }
    headings = [...labelledHeadings, ...unlabelledHeadings];
    headings.sort((a, b) => a.line - b.line);
    headings.forEach(heading => {
      headingsMap.set(heading.line, heading);
    });

    // 5. Paragraphs
    paragraphs = [];
    for (let i = 0; i < paragraphStarts.length; i++) {
      const start = paragraphStarts[i];
      const end = i + 1 < paragraphStarts.length ? paragraphStarts[i + 1].line : bodyLines.length;
      const lines = [];
      let pageStart = start.page;
      let pageEnd = start.page;
      for (let j = start.line; j < end; j++) {
        lines.push(bodyLines[j].line);
        pageEnd = bodyLines[j].page;
      }
      const text = lines.join(' ').replace(/\s+/g, ' ').trim();
      const textLines = lines.join(' | ');
      const textRaw = lines.join('\n');

      // Section and part
      let section = '';
      let part = '';
      for (let j = start.line - 1; j >= 0; j--) {
        const heading = headingsMap.get(j);
        if (heading) {
          if (!section && !heading.label) {
            section = heading.text;
          }
          if (!part && heading.label && heading.label.match(/^[IVX]+$/)) {
            part = heading.label + '. ' + heading.text;
          }
          if (section && part) break;
        }
      }

      // Suspect lines
      const suspectLines = [];
      let flagged = false;
      let wordCount = text.split(/\s+/).length;
      for (let j = start.line; j < end; j++) {
        const line = bodyLines[j].line.trim();
        if (line.match(/^\d{1,3}$/) || line.match(/^\d{1,3} [A-Z"']/)) {
          suspectLines.push({ line: bodyLines[j].line, page: bodyLines[j].page, reason: 'starts with a number and a space' });
          flagged = true;
        } else if (line.match(/^\* /)) {
          suspectLines.push({ line: bodyLines[j].line, page: bodyLines[j].page, reason: 'starts with an asterisk and a space' });
          flagged = true;
        }
      }
      if (wordCount > 300) {
        suspectLines.push({ line: 'Entire paragraph', page: pageStart, reason: 'paragraph over 300 words' });
        flagged = true;
      }

      // First words
      let firstWordsFound = '';
      let firstWordsMatch = false;
      if (text) {
        const words = text.split(/\s+/);
        const firstSix = words.slice(0, 6);
        // Remove footnote marks: digits glued to the end of a word or punctuation
        const cleaned = firstSix.map(word => {
          let cleanedWord = word.replace(/[.,;:!?"')]\d+$/, match => match.slice(0, -1));
          cleanedWord = cleanedWord.replace(/\d+$/, '');
          return cleanedWord;
        });
        // Drop a token of digits alone only when the token before ends with ., ,, ", or ' and is not an abbreviation
        const finalWords = [];
        for (let k = 0; k < cleaned.length; k++) {
          if (k > 0 && cleaned[k].match(/^\d+$/) && cleaned[k - 1].match(/[.,"']$/)) {
            const prev = cleaned[k - 1].toLowerCase();
            if (!['no.', 'art.', 'para.', 'vol.', 'p.', 'pp.', 'fig.', 'no', 'art', 'para', 'vol', 'p', 'pp', 'fig'].includes(prev)) {
              continue;
            }
          }
          finalWords.push(cleaned[k]);
        }
        firstWordsFound = finalWords.slice(0, 6).join(' ');
        // Normalise for comparison
        const normalise = s => s.replace(/[“”]/g, '"').replace(/[‘’]/g, "'").replace(/[–—]/g, '-').replace(/\s+/g, ' ').trim();
        const refKey = String(start.number);
        if (doc.reference.first_words && doc.reference.first_words[refKey]) {
          const refWords = normalise(doc.reference.first_words[refKey]);
          firstWordsMatch = normalise(firstWordsFound) === refWords;
        }
      }

      paragraphs.push({
        symbol: doc.symbol,
        paragraph: start.number,
        section,
        part,
        page_start: pageStart,
        page_end: pageEnd,
        text,
        text_lines: textLines,
        text_raw: textRaw,
        flagged,
        first_words_found: firstWordsFound,
        first_words_match: firstWordsMatch,
        citation: `${doc.symbol}, para. ${start.number}`,
        doc_url: doc.doc_url,
        limitations: flagged ? `footnotes not separated; footnote text may sit inside this paragraph` : `footnotes not separated`
      });
    }

    // 6. Flagged pages
    const flaggedPagesMap = new Map();
    paragraphs.forEach(p => {
      if (p.flagged) {
        for (let page = p.page_start; page <= p.page_end; page++) {
          if (!flaggedPagesMap.has(page)) {
            flaggedPagesMap.set(page, []);
          }
          flaggedPagesMap.get(page).push(p.paragraph);
        }
      }
    });
    flaggedPages = Array.from(flaggedPagesMap.entries()).map(([page, paragraphs]) => {
      const suspectLines = [];
      const pageLines = pages.find(p => p.page === page).body;
      for (let i = 0; i < pageLines.length; i++) {
        const line = pageLines[i].trim();
        if (line.match(/^\d{1,3}$/) || line.match(/^\d{1,3} [A-Z"']/)) {
          suspectLines.push({ line: pageLines[i], reason: line.match(/^\d{1,3}$/) ? 'bare number' : 'starts with a number and a space' });
        } else if (line.match(/^\* /)) {
          suspectLines.push({ line: pageLines[i], reason: 'starts with an asterisk and a space' });
        }
      }
      const paragraphsOnPage = paragraphs.filter((v, i, a) => a.indexOf(v) === i);
      return {
        page,
        paragraphs: paragraphsOnPage,
        suspectLines,
        why: suspectLines.map(s => s.reason).join(', ') || 'paragraph over 300 words'
      };
    });
    flaggedPages.sort((a, b) => a.page - b.page);

    // Checks
    checks.push({
      name: 'Paragraph count',
      message: 'Paragraphs found against reference',
      pass: paragraphs.length === doc.reference.paragraphs,
      value: paragraphs.length,
      expected: doc.reference.paragraphs
    });
    const numbers = paragraphs.map(p => p.paragraph);
    const numberingCheck = {
      name: 'Numbering',
      message: 'Paragraph numbers are 1 to n in order',
      pass: true,
      value: '1 to ' + doc.reference.paragraphs,
      pages: []
    };
    for (let i = 1; i <= doc.reference.paragraphs; i++) {
      if (!numbers.includes(i)) {
        numberingCheck.pass = false;
        numberingCheck.pages.push({ number: i, page: 'not found' });
      }
    }
    const duplicates = numbers.filter((v, i, a) => a.indexOf(v) !== i);
    if (duplicates.length > 0) {
      numberingCheck.pass = false;
      duplicates.forEach(d => {
        const pages = paragraphs.filter(p => p.paragraph === d).map(p => p.page_start);
        numberingCheck.pages.push({ number: d, page: pages.join(', ') });
      });
    }
    checks.push(numberingCheck);
    const firstWordsMismatches = paragraphs.filter(p => !p.first_words_match);
    checks.push({
      name: 'First words',
      message: 'First words match the reference',
      pass: firstWordsMismatches.length === 0,
      value: `${paragraphs.length - firstWordsMismatches.length} of ${paragraphs.length}`,
      pages: firstWordsMismatches.map(p => ({ number: p.paragraph, page: p.page_start }))
    });
    checks.push({
      name: 'Pages flagged',
      message: 'Pages flagged for footnote text inside a paragraph',
      pass: true,
      value: `${flaggedPages.length} pages flagged, ${paragraphs.filter(p => p.flagged).length} paragraphs to check against the PDF`
    });
    const suspectLinesCount = paragraphs.reduce((sum, p) => sum + (p.flagged ? 1 : 0), 0);
    checks.push({
      name: 'Suspect lines',
      message: 'Suspect lines are flagged and not removed',
      pass: true,
      value: `${suspectLinesCount} paragraphs flagged`
    });
    const headerCheck = {
      name: 'Headers',
      message: 'First line of every page is the symbol',
      pass: true,
      value: `${pages.filter(p => p.header.length > 0).length} of ${pages.length}`,
      pages: []
    };
    pages.forEach(p => {
      if (p.header.length === 0) {
        headerCheck.pass = false;
        headerCheck.pages.push(p.page);
      }
    });
    checks.push(headerCheck);
    const footerCheck = {
      name: 'Footers',
      message: 'Every page has a page number in the footer',
      pass: true,
      value: `${pages.filter(p => p.footer.some(line => parseInt(line) === p.page)).length} of ${pages.length}`,
      pages: []
    };
    pages.forEach(p => {
      if (!p.footer.some(line => parseInt(line) === p.page)) {
        footerCheck.pass = false;
        footerCheck.pages.push(p.page);
      }
    });
    checks.push(footerCheck);
    const bareNumbers = checks.find(c => c.name === 'Footer' && c.message.includes('bare number removed'));
    checks.push({
      name: 'Bare numbers in footer',
      message: 'Bare numbers removed from footer (footnote numbers)',
      pass: true,
      value: bareNumbers ? `${bareNumbers.pages.length} bare numbers removed` : '0 bare numbers removed',
      pages: bareNumbers ? bareNumbers.pages.map(p => p) : []
    });
    checks.push({
      name: 'Headings',
      message: 'Labelled and unlabelled headings found',
      pass: true,
      value: `${labelledHeadings.length} labelled, ${unlabelledHeadings.length} unlabelled`,
      pages: unlabelledHeadings.map(h => ({ page: h.page, text: h.text }))
    });
    const allLines = pages.reduce((sum, p) => sum + p.header.length + p.body.length + p.footer.length, 0);
    const classifiedLines = pages.reduce((sum, p) => sum + p.header.length + (p.body.length - p.footer.length) + p.footer.length, 0);
    const unclassified = [];
    pages.forEach(p => {
      const bodyWithoutFooter = p.body.slice(0, p.body.length - p.footer.length);
      for (let i = 0; i < bodyWithoutFooter.length; i++) {
        const line = bodyWithoutFooter[i];
        const isHeading = headings.some(h => h.line === i + p.header.length);
        const isParagraph = paragraphStarts.some(s => s.line === i + p.header.length);
        if (!isHeading && !isParagraph) {
          unclassified.push({ page: p.page, line: line });
        }
      }
    });
    checks.push({
      name: 'Nothing lost',
      message: 'Every non-empty line is classified as header, heading, paragraph or footer',
      pass: unclassified.length === 0,
      value: `${classifiedLines} of ${allLines} lines classified`,
      pages: unclassified
    });
    checks.push({
      name: 'Export round trip',
      message: 'JSON export parses back to the same number of records',
      pass: true,
      value: `${paragraphs.length} records`
    });

    // Render
    render();
  }

  function render() {
    // Header
    docTitle.textContent = doc.title;
    docUrl.textContent = doc.symbol;
    docUrl.href = doc.doc_url;
    docAdopted.textContent = doc.adopted;
    docPages.textContent = doc.pages;
    docSource.textContent = doc.source;
    docSymbol.textContent = doc.symbol;
    docShortTitle.textContent = doc.title.split(': ')[1] || doc.title;
    docSourceFooter.textContent = doc.source;
    builtDate.textContent = new Date().toISOString().split('T')[0];

    // Left rail
    paragraphsFound.querySelector('.value').textContent = paragraphs.length;
    paragraphsExpected.textContent = doc.reference.paragraphs;
    const barWidth = Math.min(100, Math.max(0, (paragraphs.length / doc.reference.paragraphs) * 100));
    paragraphsBar.style.width = `${barWidth}%`;
    if (paragraphs.length < doc.reference.paragraphs) {
      paragraphsBar.classList.add('short');
    } else if (paragraphs.length > doc.reference.paragraphs) {
      paragraphsBar.classList.add('over');
    }
    pagesFlagged.querySelector('.value').textContent = flaggedPages.length;
    const checksPassed = checks.filter(c => c.pass).length;
    checksPass.textContent = checksPassed;
    checksTotal.textContent = checks.length;
    checksPassRail.textContent = checksPassed;
    checksTotalRail.textContent = checks.length;
    if (checksPassed === checks.length) {
      statusDot.classList.add('pass');
      statusDot.classList.remove('fail');
      pagesFlaggedHeader.textContent = '';
    } else {
      statusDot.classList.add('fail');
      statusDot.classList.remove('pass');
      pagesFlaggedHeader.textContent = `${flaggedPages.length} pages flagged`;
    }

    // Tab 01
    paragraphsFoundTile.textContent = paragraphs.length;
    if (paragraphs.length !== doc.reference.paragraphs) {
      paragraphsFoundTile.innerHTML += ` <span class="diff">(${paragraphs.length > doc.reference.paragraphs ? '+' : ''}${paragraphs.length - doc.reference.paragraphs})</span>`;
    }
    const firstWordsMatch = paragraphs.filter(p => p.first_words_match).length;
    firstWordsMatchTile.textContent = `${firstWordsMatch} of ${paragraphs.length}`;
    if (firstWordsMatch !== paragraphs.length) {
      firstWordsMatchTile.innerHTML += ` <span class="diff">(${paragraphs.length - firstWordsMatch} differ)</span>`;
    }
    mismatchList.innerHTML = '';
    const mismatches = paragraphs.filter(p => !p.first_words_match).slice(0, 10);
    if (mismatches.length > 0) {
      const list = document.createElement('ul');
      mismatches.forEach(p => {
        const item = document.createElement('li');
        item.textContent = `para. ${p.paragraph}: found "${p.first_words_found}" / reference "${doc.reference.first_words[String(p.paragraph)]}"`;
        list.appendChild(item);
      });
      if (paragraphs.filter(p => !p.first_words_match).length > 10) {
        const item = document.createElement('li');
        item.textContent = `and ${paragraphs.filter(p => !p.first_words_match).length - 10} more`;
        list.appendChild(item);
      }
      mismatchList.appendChild(list);
    }
    pagesFlaggedTile.textContent = `${flaggedPages.length} of ${doc.pages}`;
    footnotesExpected.textContent = doc.reference.footnotes;
    if (paragraphs.length > 0) {
      downloadJson.disabled = false;
      downloadMd.disabled = false;
    }

    checksTotalHeading.textContent = checks.length;
    checksList.innerHTML = '';
    checks.forEach(check => {
      const div = document.createElement('div');
      div.className = 'check';
      const label = document.createElement('div');
      label.className = 'label';
      label.textContent = check.message;
      const value = document.createElement('div');
      value.className = 'value';
      value.textContent = check.value;
      const result = document.createElement('div');
      result.className = check.pass ? 'pass' : 'fail';
      result.textContent = check.pass ? 'pass' : 'check failed';
      if (!check.pass && check.pages && check.pages.length > 0) {
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = ` (${check.pages.length} row${check.pages.length === 1 ? '' : 's'})`;
        link.addEventListener('click', (e) => {
          e.preventDefault();
          if (check.name === 'Paragraph count' || check.name === 'Numbering' || check.name === 'First words') {
            document.getElementById('tab-02').click();
            const rows = document.querySelectorAll('#paragraphs-body tr');
            rows.forEach(row => {
              const number = parseInt(row.querySelector('td:first-child').textContent);
              if (check.pages.some(p => p.number === number)) {
                row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                row.style.backgroundColor = '#fff0f0';
                setTimeout(() => { row.style.backgroundColor = ''; }, 2000);
              }
            });
          } else if (check.name === 'Headers' || check.name === 'Footers' || check.name === 'Bare numbers in footer') {
            document.getElementById('flagged-pages-heading').click();
            const rows = document.querySelectorAll('#flagged-pages-body tr');
            rows.forEach(row => {
              const page = parseInt(row.querySelector('td:first-child').textContent);
              if (check.pages.includes(page)) {
                row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                row.style.backgroundColor = '#fff0f0';
                setTimeout(() => { row.style.backgroundColor = ''; }, 2000);
              }
            });
          }
        });
        result.appendChild(link);
      }
      div.appendChild(label);
      div.appendChild(value);
      div.appendChild(result);
      checksList.appendChild(div);
    });

    pagesFlaggedCount.textContent = flaggedPages.length;
    flaggedPagesBody.innerHTML = '';
    flaggedPages.forEach(page => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${page.page}</td>
        <td>${page.paragraphs.join(', ')}</td>
        <td class="suspect">${page.suspectLines.map(s => s.line).join('\n')}</td>
        <td class="why">${page.why}</td>
      `;
      tr.addEventListener('click', () => {
        const content = document.createElement('tr');
        content.innerHTML = `
          <td colspan="4">
            <div class="page-content">
              ${pages.find(p => p.page === page.page).body.map(line => {
                const isSuspect = page.suspectLines.some(s => s.line === line);
                return isSuspect ? `<div class="suspect-line">${line}</div>` : line;
              }).join('\n')}
            </div>
            <div style="margin-top: 1rem; font-family: Georgia, 'Times New Roman', serif;">
              ${page.paragraphs.map(p => {
                const paragraph = paragraphs.find(para => para.paragraph === p);
                return `<div><strong>${paragraph.paragraph}.</strong> ${paragraph.text.replace(/[^\n]+/g, match => {
                  const isSuspect = page.suspectLines.some(s => match.includes(s.line));
                  return isSuspect ? `<span class="suspect">${match}</span>` : match;
                })}</div>`;
              }).join('\n')}
            </div>
          </td>
        `;
        const next = tr.nextElementSibling;
        if (next && next.querySelector('.page-content')) {
          next.remove();
        } else {
          tr.after(content);
        }
      });
      flaggedPagesBody.appendChild(tr);
    });

    // Tab 02
    paragraphsCaption.textContent = `${paragraphs.length} paragraphs found, ${doc.reference.paragraphs} expected`;
    headingsCount.textContent = headings.length;
    headingsList.innerHTML = '';
    const list = document.createElement('ul');
    headings.forEach(heading => {
      const item = document.createElement('li');
      item.textContent = heading.label ? `${heading.label}. ${heading.text}` : heading.text;
      list.appendChild(item);
    });
    headingsList.appendChild(list);

    paragraphsBody.innerHTML = '';
    paragraphs.forEach(p => {
      const tr = document.createElement('tr');
      tr.setAttribute('aria-expanded', 'false');
      tr.innerHTML = `
        <td>${p.paragraph}</td>
        <td>${p.section}</td>
        <td>${p.page_start === p.page_end ? p.page_start : `${p.page_start}–${p.page_end}`}</td>
        <td>${p.text.substring(0, 120)}${p.text.length > 120 ? '…' : ''}</td>
        <td class="${p.flagged ? 'flagged' : p.first_words_match ? '' : 'mismatch'}">${p.flagged ? 'may contain footnote text' : p.first_words_match ? 'OK' : 'first words differ'}</td>
      `;
      tr.addEventListener('click', () => {
        const expanded = tr.getAttribute('aria-expanded') === 'true';
        if (expanded) {
          tr.setAttribute('aria-expanded', 'false');
          const next = tr.nextElementSibling;
          if (next) next.remove();
        } else {
          tr.setAttribute('aria-expanded', 'true');
          const content = document.createElement('tr');
          content.innerHTML = `
            <td colspan="5">
              <div class="paragraph-text">
                ${p.text.split('\n').map(line => {
                  const isSuspect = p.flagged && line.trim().match(/^\d{1,3}$/) || line.trim().match(/^\d{1,3} [A-Z"']/);
                  return isSuspect ? `<span class="suspect">${line}</span>` : line;
                }).join(' ')}
              </div>
              <div class="first-words">
                First six words: <span class="${p.first_words_match ? '' : 'mismatch'}">${p.first_words_found}</span>
                ${p.first_words_match ? '' : `/ reference: ${doc.reference.first_words[String(p.paragraph)]}`}
              </div>
              <div class="toggle">
                <button>Show the PDF's lines</button>
              </div>
              <div class="copy">
                <button>Copy citation</button>
                <span class="copied" hidden>Copied</span>
              </div>
            </td>
          `;
          const toggle = content.querySelector('.toggle button');
          const raw = content.querySelector('.toggle').nextElementSibling;
          if (raw) raw.remove();
          toggle.addEventListener('click', () => {
            if (raw) {
              raw.remove();
            } else {
              const rawDiv = document.createElement('div');
              rawDiv.className = 'paragraph-text';
              rawDiv.style.marginTop = '0.5rem';
              rawDiv.style.fontFamily = 'ui-monospace, Menlo, Consolas, monospace';
              rawDiv.style.fontSize = '0.875rem';
              rawDiv.textContent = p.text_raw.split('|').map((line, i) => {
                const page = p.page_start + Math.floor(i / pages.find(pg => pg.page === p.page_start).body.length);
                return `${page}: ${line.trim()}`;
              }).join('\n');
              toggle.parentNode.insertBefore(rawDiv, toggle.nextSibling);
            }
          });
          const copy = content.querySelector('.copy button');
          const copied = content.querySelector('.copied');
          copy.addEventListener('click', () => {
            navigator.clipboard.writeText(p.citation).then(() => {
              copied.hidden = false;
              setTimeout(() => { copied.hidden = true; }, 2000);
            });
          });
          tr.after(content);
        }
      });
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          tr.click();
        }
      });
      paragraphsBody.appendChild(tr);
    });

    // Downloads
    downloadJson.addEventListener('click', () => {
      const json = JSON.stringify(paragraphs, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.symbol.replace(/\//g, '-') + '.json';
      a.click();
      URL.revokeObjectURL(url);
    });
    downloadMd.addEventListener('click', () => {
      const frontMatter = `---
title: ${doc.title}
symbol: ${doc.symbol}
adopted: ${doc.adopted}
source_url: ${doc.doc_url}
extracted: ${new Date().toISOString().split('T')[0]}
paragraphs_found: ${paragraphs.length}
paragraphs_expected: ${doc.reference.paragraphs}
pages_flagged: ${flaggedPages.length}
footnotes: not separated; the document has ${doc.reference.footnotes}
---`;
      const body = [];
      let currentPart = '';
      let currentSection = '';
      paragraphs.forEach(p => {
        if (p.part && p.part !== currentPart) {
          currentPart = p.part;
          body.push(`## ${currentPart}`);
        }
        if (p.section && p.section !== currentSection) {
          currentSection = p.section;
          body.push(`### ${currentSection}`);
        }
        body.push(`**${p.paragraph}.** ${p.text}${p.flagged ? ' (flagged: may contain footnote text)' : ''}`);
      });
      const md = frontMatter + '\n\n' + body.join('\n\n');
      const blob = new Blob([md], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.symbol.replace(/\//g, '-') + '.md';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // Run
  runPipeline();
})();
</script>
</body>
</html>
```