I built the app you described: a four-tab dashboard that splits the raw PDF converter text of E/C.12/GC/27 into numbered paragraphs and footnotes, checks itself against the document's own reference, and shows every repair it made. The left rail holds the document card; the tabs show the result, the paragraphs, the footnotes, and the checks and method.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraphs out of a PDF – UN DOCUMENT · PDF TEXT</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --pass: #2e6b2e;
  --fail: #9b2335;
  --cover: #f0e6d2;
  --header: #e6e0d2;
  --heading: #d9d2c3;
  --paragraph: #f4f0e8;
  --footnote: #e8e2d2;
  --footer: #d2c8b8;
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
h1, h2, h3, h4, h5, h6 {
  font-weight: 400;
  margin: 0;
}
h1 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 28px;
}
h2 {
  font-size: 20px;
}
h3 {
  font-size: 18px;
}
h4 {
  font-size: 16px;
}
p {
  margin: 0 0 1em 0;
}
a {
  color: var(--accent);
  text-decoration: none;
}
a:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 1.5em 0;
}
.hidden {
  display: none !important;
}
.mono {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 12px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.serif {
  font-family: Georgia, "Times New Roman", serif;
}
.small {
  font-size: 14px;
}
.big {
  font-size: 40px;
  line-height: 1;
}
.bigger {
  font-size: 56px;
  line-height: 1;
}
.red {
  color: var(--accent);
}
.green {
  color: var(--pass);
}
.pass {
  color: var(--pass);
}
.fail {
  color: var(--fail);
}
.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 0.5em;
}
.dot.pass {
  background-color: var(--pass);
}
.dot.fail {
  background-color: var(--fail);
}
.container {
  display: flex;
  min-height: 100vh;
}
.rail {
  flex: 0 0 240px;
  padding: 1em;
  border-right: 1px solid var(--rule);
  background-color: #f9f6f2;
}
.main {
  flex: 1;
  padding: 1em;
}
.header {
  padding-bottom: 1em;
  border-bottom: 1px solid var(--rule);
}
.header h1 {
  display: flex;
  align-items: baseline;
  gap: 0.5em;
}
.header .mono {
  font-size: 11px;
}
.header p {
  margin: 0.5em 0 0 0;
  font-size: 14px;
}
.header .meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5em;
}
.card {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1em;
  margin-bottom: 1em;
}
.card.selected {
  border-left: 4px solid var(--accent);
}
.card h3 {
  margin-top: 0;
}
.card .symbol {
  font-family: ui-monospace, monospace;
  font-size: 14px;
  word-break: break-all;
}
.card .meta {
  font-size: 14px;
  color: #666;
}
.card .numbers {
  display: flex;
  gap: 1.5em;
  margin: 1em 0;
}
.card .number {
  flex: 1;
}
.card .number .big {
  display: block;
}
.card .number .label {
  font-size: 14px;
  color: #666;
}
.card .number .bar {
  height: 4px;
  background-color: var(--rule);
  margin-top: 0.5em;
  border-radius: 2px;
  overflow: hidden;
}
.card .number .bar-inner {
  height: 100%;
  background-color: var(--accent);
  width: 0%;
}
.card .number .bar.fail .bar-inner {
  background-color: var(--fail);
}
.tabs {
  display: flex;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 1em;
}
.tab {
  padding: 0.5em 1em;
  cursor: pointer;
  border: 1px solid transparent;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  margin-right: 0.5em;
  font-size: 14px;
  color: #666;
}
.tab.active {
  color: var(--ink);
  border-color: var(--rule);
  border-bottom-color: white;
  background: white;
  font-weight: 500;
}
.tab:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.tabpanel {
  display: none;
}
.tabpanel.active {
  display: block;
}
.tabpanel h2 {
  margin-bottom: 1em;
}
.tabpanel h2 .mono {
  font-size: 11px;
  color: #666;
}
.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1em;
  margin-bottom: 2em;
}
.tile {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1em;
}
.tile h3 {
  font-size: 14px;
  margin-top: 0;
  color: #666;
}
.tile .big {
  display: block;
  margin: 0.5em 0;
}
.tile .big.fail {
  color: var(--fail);
}
.tile .note {
  font-size: 14px;
  color: #666;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2em;
}
caption {
  font-family: Georgia, serif;
  font-size: 18px;
  text-align: left;
  margin-bottom: 0.5em;
  padding: 0;
}
th, td {
  padding: 0.75em;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
th {
  font-weight: 500;
  background-color: #f9f6f2;
}
th[scope="col"] {
  text-align: left;
}
td {
  vertical-align: top;
}
td.number {
  text-align: right;
  font-family: Georgia, serif;
  font-size: 18px;
}
td.page {
  text-align: right;
  font-family: ui-monospace, monospace;
  font-size: 14px;
}
td.check {
  font-size: 14px;
}
td.check.fail {
  color: var(--fail);
}
tr.expanded td {
  border-bottom: none;
}
tr.detail {
  display: none;
}
tr.detail td {
  padding: 0.5em 0.75em;
  border-top: none;
}
tr.detail td[colspan] {
  padding-top: 0;
}
tr.detail pre {
  margin: 0;
  padding: 0.75em;
  background: #f9f6f2;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.5;
}
tr.detail .meta {
  display: flex;
  gap: 1em;
  margin-top: 0.5em;
  font-size: 14px;
  color: #666;
}
tr.detail .meta div {
  display: flex;
  align-items: center;
  gap: 0.5em;
}
tr.detail .meta .dot {
  width: 8px;
  height: 8px;
}
tr.detail .meta .words {
  font-family: ui-monospace, monospace;
  font-size: 12px;
}
tr.detail .repairs {
  margin-top: 0.5em;
  font-size: 14px;
}
tr.detail .repairs div {
  margin-bottom: 0.25em;
}
tr.detail button {
  margin-top: 0.5em;
}
button {
  padding: 0.5em 1em;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-family: system-ui, sans-serif;
  font-size: 14px;
}
button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
button.secondary {
  background: #f9f6f2;
}
button.copy {
  font-family: ui-monospace, monospace;
  font-size: 12px;
}
button[aria-expanded="true"]::after {
  content: "−";
}
button[aria-expanded="false"]::after {
  content: "+";
}
button[aria-expanded] {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
button[aria-expanded]::after {
  margin-left: 0.5em;
}
.footnotes {
  margin-top: 1em;
}
.footnotes h3 {
  margin-bottom: 0.5em;
}
.footnotes table {
  margin-bottom: 0;
}
.footnotes td.repair {
  font-size: 14px;
  color: #666;
}
.checks {
  margin-bottom: 2em;
}
.checks h3 {
  margin-bottom: 0.5em;
}
.checks .check {
  display: flex;
  align-items: center;
  gap: 0.5em;
  margin-bottom: 0.5em;
  font-size: 14px;
}
.checks .check .dot {
  width: 8px;
  height: 8px;
}
.checks .check .label {
  flex: 1;
}
.checks .check .value {
  font-family: ui-monospace, monospace;
  font-size: 12px;
}
.checks .check .fail {
  color: var(--fail);
}
.checks .check a {
  color: var(--fail);
  text-decoration: underline;
}
.repair-log {
  margin-bottom: 2em;
}
.repair-log h3 {
  margin-bottom: 0.5em;
}
.repair-log table {
  margin-bottom: 0;
}
.repair-log th {
  font-size: 14px;
}
.repair-log td {
  font-size: 14px;
  vertical-align: top;
}
.repair-log td.before, .repair-log td.after {
  font-family: ui-monospace, monospace;
  white-space: pre-wrap;
  word-break: break-all;
}
.repair-log .counts {
  display: flex;
  gap: 1em;
  margin-bottom: 1em;
  font-size: 14px;
}
.repair-log .counts div {
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.raw-pages {
  margin-bottom: 2em;
}
.raw-pages h3 {
  margin-bottom: 0.5em;
}
.raw-pages select {
  padding: 0.5em;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background: white;
  font-family: system-ui, sans-serif;
  font-size: 14px;
  margin-bottom: 1em;
}
.raw-pages pre {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1em;
  overflow-x: auto;
  font-family: ui-monospace, monospace;
  font-size: 12px;
  line-height: 1.4;
  white-space: pre;
}
.raw-pages .line {
  display: flex;
}
.raw-pages .line::before {
  content: attr(data-line);
  display: inline-block;
  width: 4em;
  text-align: right;
  padding-right: 1em;
  color: #999;
  font-size: 11px;
}
.raw-pages .line.cover {
  background-color: var(--cover);
}
.raw-pages .line.header {
  background-color: var(--header);
}
.raw-pages .line.heading {
  background-color: var(--heading);
}
.raw-pages .line.paragraph {
  background-color: var(--paragraph);
}
.raw-pages .line.footnote {
  background-color: var(--footnote);
}
.raw-pages .line.footer {
  background-color: var(--footer);
}
.raw-pages .line.unclassified {
  background-color: #ffebee;
}
.raw-pages .legend {
  display: flex;
  gap: 1em;
  margin-top: 1em;
  font-size: 12px;
}
.raw-pages .legend div {
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.raw-pages .legend .swatch {
  display: inline-block;
  width: 1em;
  height: 1em;
  border: 1px solid #ccc;
}
.footer {
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid var(--rule);
  font-size: 14px;
  color: #666;
}
.footer a {
  color: #666;
  text-decoration: underline;
}
</style>
</head>
<body>

<div class="container">
  <aside class="rail" role="navigation">
    <div class="card selected">
      <div class="mono">DOCUMENT</div>
      <h3 class="symbol" id="doc-symbol"></h3>
      <div class="meta" id="doc-adopted"></div>
      <div class="meta" id="doc-pages"></div>
      <div class="numbers">
        <div class="number">
          <span class="big" id="doc-paragraphs-found"></span>
          <div class="label">paragraphs</div>
          <div class="label">of <span id="doc-paragraphs-reference"></span></div>
          <div class="bar"><div class="bar-inner" id="doc-paragraphs-bar"></div></div>
        </div>
        <div class="number">
          <span class="big" id="doc-footnotes-found"></span>
          <div class="label">footnotes</div>
          <div class="label">of <span id="doc-footnotes-reference"></span></div>
          <div class="bar"><div class="bar-inner" id="doc-footnotes-bar"></div></div>
        </div>
      </div>
      <div class="meta">
        <span class="dot" id="doc-checks-dot"></span>
        <span id="doc-checks-text"></span>
      </div>
    </div>
  </aside>

  <main class="main">
    <header class="header">
      <h1>
        <span class="mono">UN DOCUMENT · PDF TEXT</span>
        <span id="doc-title"></span>
      </h1>
      <p id="doc-description"></p>
      <div class="meta">
        <div>
          <span class="dot" id="checks-dot"></span>
          <span id="checks-text"></span>
        </div>
      </div>
    </header>

    <div class="tabs" role="tablist" aria-label="Document tabs">
      <button class="tab active" id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
      <button class="tab" id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
      <button class="tab" id="tab-03" role="tab" aria-selected="false" aria-controls="panel-03">03 FOOTNOTES</button>
      <button class="tab" id="tab-04" role="tab" aria-selected="false" aria-controls="panel-04">04 CHECKS & METHOD</button>
    </div>

    <div id="panel-01" class="tabpanel active" role="tabpanel" aria-labelledby="tab-01">
      <div class="tiles">
        <div class="tile">
          <h3>Paragraphs found</h3>
          <span class="big" id="paragraphs-found"></span>
          <div class="note">How this is computed: the script split the raw text into numbered paragraphs.</div>
        </div>
        <div class="tile">
          <h3>The document has</h3>
          <span class="big" id="paragraphs-reference"></span>
          <div class="note">How this is computed: the reference in the file.</div>
        </div>
        <div class="tile">
          <h3>Footnotes found</h3>
          <span class="big" id="footnotes-found"></span>
          <div class="note">How this is computed: the script extracted the footnotes from the raw text.</div>
        </div>
        <div class="tile">
          <h3>First words match</h3>
          <span class="big" id="first-words-match"></span>
          <div class="note">How this is computed: the first six words of each paragraph against the reference.</div>
        </div>
        <div class="tile">
          <h3>Repairs made</h3>
          <span class="big"><a href="#" id="repairs-link">0</a></span>
          <div class="note">How this is computed: every change the script made to the raw text.</div>
        </div>
      </div>
    </div>

    <div id="panel-02" class="tabpanel" role="tabpanel" aria-labelledby="tab-02" hidden>
      <div class="headings-box">
        <button aria-expanded="false" aria-controls="headings-list">Headings found: <span id="headings-count">0</span></button>
        <div id="headings-list" hidden>
          <ul id="headings-list-content"></ul>
        </div>
      </div>
      <table>
        <caption>Paragraphs found in the document</caption>
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
      <p class="small">Footnote marks in the text are shown as [n]. Use find-and-replace with <code>\[\d+\]</code> to remove them.</p>
    </div>

    <div id="panel-03" class="tabpanel" role="tabpanel" aria-labelledby="tab-03" hidden>
      <div class="footnotes">
        <h2><span class="mono">TAB.03</span> Footnotes</h2>
        <p>Footnotes found: <span id="footnotes-count">0</span> of <span id="footnotes-reference-count"></span></p>
        <table>
          <thead>
            <tr>
              <th scope="col">No.</th>
              <th scope="col">Page</th>
              <th scope="col">Text</th>
              <th scope="col">Repair</th>
            </tr>
          </thead>
          <tbody id="footnotes-table"></tbody>
        </table>
        <button id="download-footnotes">Download footnotes as CSV</button>
      </div>
    </div>

    <div id="panel-04" class="tabpanel" role="tabpanel" aria-labelledby="tab-04" hidden>
      <div class="checks">
        <h2><span class="mono">TAB.04</span> Checks</h2>
        <div id="checks-list"></div>
      </div>

      <div class="repair-log">
        <h3><button aria-expanded="false" aria-controls="repair-log-content">Repair log (<span id="repair-log-count">0</span>)</button></h3>
        <div class="counts" id="repair-counts"></div>
        <div id="repair-log-content" hidden>
          <table>
            <thead>
              <tr>
                <th scope="col">Page</th>
                <th scope="col">Paragraph or footnote</th>
                <th scope="col">What was done</th>
                <th scope="col">Before</th>
                <th scope="col">After</th>
              </tr>
            </thead>
            <tbody id="repair-log-table"></tbody>
          </table>
        </div>
      </div>

      <div class="raw-pages">
        <h3><button aria-expanded="false" aria-controls="raw-pages-content">Raw pages</button></h3>
        <div id="raw-pages-content" hidden>
          <select id="raw-page-select">
            <option value="">Select a page</option>
          </select>
          <pre id="raw-page-view"></pre>
          <div class="legend">
            <div><span class="swatch" style="background-color: var(--cover);"></span> C cover</div>
            <div><span class="swatch" style="background-color: var(--header);"></span> H header</div>
            <div><span class="swatch" style="background-color: var(--heading);"></span> G heading</div>
            <div><span class="swatch" style="background-color: var(--paragraph);"></span> P paragraph</div>
            <div><span class="swatch" style="background-color: var(--footnote);"></span> F footnote</div>
            <div><span class="swatch" style="background-color: var(--footer);"></span> T footer</div>
            <div><span class="swatch" style="background-color: #ffebee;"></span> ? unclassified</div>
          </div>
        </div>
      </div>

      <div>
        <h3>Download</h3>
        <button id="download-paragraphs">Download paragraphs as CSV</button>
      </div>
    </div>

    <footer class="footer">
      <p>Source: <span id="doc-source"></span>. Built <span id="doc-built"></span>.</p>
      <p>Counting, splitting and matching are done by this page's code; no model was called and nothing left the browser.</p>
    </footer>
  </main>
</div>

<script>
(function() {
  // Data
  const data = window.WORKSHOP_DATA.pdf_text;
  const doc = {
    title: data.title,
    symbol: data.symbol,
    doc_url: data.doc_url,
    source: data.source,
    built: new Date().toISOString().split('T')[0],
    pages: data.records,
    reference: data.reference
  };

  // State
  let paragraphs = [];
  let footnotes = [];
  let headings = [];
  let repairs = [];
  let checks = [];
  let rawLines = [];

  // UI elements
  const docTitle = document.getElementById('doc-title');
  const docSymbol = document.getElementById('doc-symbol');
  const docAdopted = document.getElementById('doc-adopted');
  const docPages = document.getElementById('doc-pages');
  const docParagraphsFound = document.getElementById('doc-paragraphs-found');
  const docParagraphsReference = document.getElementById('doc-paragraphs-reference');
  const docParagraphsBar = document.getElementById('doc-paragraphs-bar');
  const docFootnotesFound = document.getElementById('doc-footnotes-found');
  const docFootnotesReference = document.getElementById('doc-footnotes-reference');
  const docFootnotesBar = document.getElementById('doc-footnotes-bar');
  const docChecksDot = document.getElementById('doc-checks-dot');
  const docChecksText = document.getElementById('doc-checks-text');
  const docDescription = document.getElementById('doc-description');
  const checksDot = document.getElementById('checks-dot');
  const checksText = document.getElementById('checks-text');
  const paragraphsFound = document.getElementById('paragraphs-found');
  const paragraphsReference = document.getElementById('paragraphs-reference');
  const footnotesFound = document.getElementById('footnotes-found');
  const footnotesReferenceCount = document.getElementById('footnotes-reference-count');
  const firstWordsMatch = document.getElementById('first-words-match');
  const repairsLink = document.getElementById('repairs-link');
  const headingsCount = document.getElementById('headings-count');
  const headingsListContent = document.getElementById('headings-list-content');
  const paragraphsTable = document.getElementById('paragraphs-table');
  const footnotesTable = document.getElementById('footnotes-table');
  const footnotesCount = document.getElementById('footnotes-count');
  const checksList = document.getElementById('checks-list');
  const repairLogCount = document.getElementById('repair-log-count');
  const repairCounts = document.getElementById('repair-counts');
  const repairLogTable = document.getElementById('repair-log-table');
  const rawPageSelect = document.getElementById('raw-page-select');
  const rawPageView = document.getElementById('raw-page-view');
  const downloadParagraphs = document.getElementById('download-paragraphs');
  const downloadFootnotes = document.getElementById('download-footnotes');

  // Tabs
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.tabpanel');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = document.getElementById(tab.getAttribute('aria-controls'));

      tabs.forEach(t => {
        t.setAttribute('aria-selected', 'false');
        t.classList.remove('active');
      });
      tab.setAttribute('aria-selected', 'true');
      tab.classList.add('active');

      panels.forEach(p => p.classList.add('hidden'));
      target.classList.remove('hidden');
    });
  });

  // Expandable headings box
  const headingsBoxButton = document.querySelector('.headings-box button');
  const headingsList = document.getElementById('headings-list');

  headingsBoxButton.addEventListener('click', () => {
    const expanded = headingsBoxButton.getAttribute('aria-expanded') === 'true';
    headingsBoxButton.setAttribute('aria-expanded', !expanded);
    headingsList.hidden = expanded;
  });

  // Expandable repair log
  const repairLogButton = document.querySelector('.repair-log button');
  const repairLogContent = document.getElementById('repair-log-content');

  repairLogButton.addEventListener('click', () => {
    const expanded = repairLogButton.getAttribute('aria-expanded') === 'true';
    repairLogButton.setAttribute('aria-expanded', !expanded);
    repairLogContent.hidden = expanded;
  });

  // Expandable raw pages
  const rawPagesButton = document.querySelector('.raw-pages button');
  const rawPagesContent = document.getElementById('raw-pages-content');

  rawPagesButton.addEventListener('click', () => {
    const expanded = rawPagesButton.getAttribute('aria-expanded') === 'true';
    rawPagesButton.setAttribute('aria-expanded', !expanded);
    rawPagesContent.hidden = expanded;
  });

  // Raw page select
  rawPageSelect.addEventListener('change', () => {
    const pageNum = parseInt(rawPageSelect.value);
    if (isNaN(pageNum)) return;

    const page = rawLines.find(p => p.page === pageNum);
    if (!page) return;

    rawPageView.innerHTML = page.lines.map(line => {
      const cls = line.type ? ` class="${line.type}"` : '';
      return `<div class="line${cls}" data-line="${line.line}">${escapeHtml(line.text)}</div>`;
    }).join('\n');
  });

  // Copy citation
  function copyCitation(symbol, number) {
    const citation = `${symbol}, para. ${number}`;
    navigator.clipboard.writeText(citation).then(() => {
      const button = event.target;
      const originalText = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => {
        button.textContent = originalText;
      }, 2000);
    });
  }

  // Escape HTML
  function escapeHtml(text) {
    return text.replace(/&/g, '&amp;')
               .replace(/</g, '&lt;')
               .replace(/>/g, '&gt;')
               .replace(/"/g, '&quot;')
               .replace(/'/g, '&#039;');
  }

  // Normalize text for comparison
  function normalize(text) {
    return text.replace(/[“”]/g, '"')
               .replace(/[‘’]/g, "'")
               .replace(/[–—]/g, '-')
               .replace(/\s+/g, ' ')
               .trim();
  }

  // Parse the document
  function parseDocument() {
    // Step 1: Tag each line of each page
    rawLines = doc.pages.map(page => {
      const lines = page.text.split('\n').map((line, i) => ({
        line: i + 1,
        text: line,
        page: page.page
      }));
      return { page: page.page, lines };
    });

    // Step 2: Remove headers and footers, tag lines
    let nextFootnote = 1;
    let displacedFootnoteNumbers = {};

    rawLines.forEach(page => {
      let lines = page.lines;
      let start = 0;
      let end = lines.length - 1;

      // Header: first non-empty line is the symbol
      while (start <= end && lines[start].text.trim() === '') start++;
      if (start <= end && lines[start].text.trim() === doc.symbol) {
        repairs.push({
          page: page.page,
          type: 'header',
          action: 'header line removed',
          before: lines[start].text,
          after: ''
        });
        lines[start].type = 'header';
        start++;
      } else if (page.page === 1) {
        checks.push({
          label: `Page ${page.page} first line is not the symbol`,
          value: `Expected "${doc.symbol}", found "${lines[start].text.trim()}"`,
          pass: false
        });
      }

      // Footer: from the end, drop empty lines, GE. lines, date stamps, bare numbers
      while (end >= start) {
        const line = lines[end].text.trim();
        if (line === '') {
          lines[end].type = 'footer';
          end--;
        } else if (line.startsWith('GE.')) {
          lines[end].type = 'footer';
          end--;
        } else if (/^\d{6}( \d{6})?$/.test(line)) {
          lines[end].type = 'footer';
          end--;
        } else if (/^\d{1,3}$/.test(line)) {
          const num = parseInt(line);
          if (num === page.page) {
            lines[end].type = 'footer';
            end--;
          } else {
            // Displaced footnote number
            displacedFootnoteNumbers[page.page] = num;
            lines[end].type = 'footer';
            end--;
          }
        } else {
          break;
        }
      }

      // Footnote block: from the first line that is a bare number or starts with nextFootnote
      let footnoteStart = -1;
      for (let i = start; i <= end; i++) {
        const line = lines[i].text.trim();
        if (line === '' || line === '*') continue;
        if (page.page === 1 && line === '* Adopted by the Committee on Economic, Social and Cultural Rights on 6 November 2025.') {
          footnoteStart = i;
          break;
        }
        if (/^\d+$/.test(line) && parseInt(line) === nextFootnote) {
          footnoteStart = i;
          break;
        }
        if (line.startsWith(`${nextFootnote} `)) {
          footnoteStart = i;
          break;
        }
      }

      if (footnoteStart === -1) {
        // No footnote opener found; check for a bare number > nextFootnote
        for (let i = start; i <= end; i++) {
          const line = lines[i].text.trim();
          if (/^\d+$/.test(line)) {
            const num = parseInt(line);
            if (num > nextFootnote) {
              checks.push({
                label: `Footnote numbering jumps from ${nextFootnote} to ${num} on page ${page.page}`,
                value: `Expected ${nextFootnote}, found ${num}`,
                pass: false
              });
              nextFootnote = num + 1;
              footnoteStart = i;
              break;
            }
          }
        }
      }

      if (footnoteStart !== -1) {
        // Tag footnotes
        let currentFootnote = null;
        for (let i = footnoteStart; i <= end; i++) {
          const line = lines[i].text.trim();
          if (line === '') {
            lines[i].type = 'footnote';
            continue;
          }
          if (/^\d+$/.test(line)) {
            const num = parseInt(line);
            if (num >= nextFootnote) {
              nextFootnote = num + 1;
            }
            currentFootnote = {
              number: num,
              lines: [],
              page: page.page,
              repaired: false
            };
            lines[i].type = 'footnote';
            footnotes.push(currentFootnote);
          } else if (line.startsWith(`${currentFootnote.number} `)) {
            currentFootnote.lines.push(line.substring(currentFootnote.number.toString().length + 1));
            lines[i].type = 'footnote';
          } else if (currentFootnote) {
            currentFootnote.lines.push(line);
            lines[i].type = 'footnote';
          }
        }

        // Handle displaced footnote number
        if (displacedFootnoteNumbers[page.page]) {
          const num = displacedFootnoteNumbers[page.page];
          if (footnotes.length > 0) {
            const lastFootnote = footnotes[footnotes.length - 1];
            if (lastFootnote.page === page.page && !lastFootnote.repaired) {
              // The second footnote on the page is the one without a number
              const text = lastFootnote.lines.join(' ');
              const firstSentenceEnd = text.indexOf('.');
              if (firstSentenceEnd !== -1) {
                const firstSentence = text.substring(0, firstSentenceEnd + 1);
                const rest = text.substring(firstSentenceEnd + 1).trim();

                // Split the footnote
                lastFootnote.lines = [firstSentence];
                lastFootnote.text = firstSentence;

                const repairedFootnote = {
                  number: num,
                  lines: [rest],
                  page: page.page,
                  repaired: true
                };
                footnotes.push(repairedFootnote);

                repairs.push({
                  page: page.page,
                  type: 'footnote',
                  action: `footnote ${num} restored from the page foot`,
                  before: `${lastFootnote.number} ${text}`,
                  after: `${lastFootnote.number} ${firstSentence}\n${num} ${rest}`
                });
              }
            }
          }
        }
      }

      // Tag the rest as body
      for (let i = start; i <= end; i++) {
        if (!lines[i].type) {
          lines[i].type = 'paragraph';
        }
      }
    });

    // Step 3: Concatenate body lines in page order
    let bodyLines = [];
    rawLines.forEach(page => {
      const body = page.lines.filter(line => line.type === 'paragraph');
      bodyLines = bodyLines.concat(body.map(line => ({
        text: line.text,
        page: line.page,
        line: line.line
      })));
    });

    // Step 4: Split into paragraphs
    let currentParagraph = null;
    let currentHeading = null;
    let currentPart = null;
    let inCover = true;

    for (let i = 0; i < bodyLines.length; i++) {
      const line = bodyLines[i];
      const text = line.text.trim();

      // Skip empty lines
      if (text === '') continue;

      // Check for paragraph start: number alone or number and text
      const paraMatch = text.match(/^(\d{1,3})\.$/);
      const paraTextMatch = text.match(/^(\d{1,3})\. (.+)$/);

      if (paraMatch || paraTextMatch) {
        inCover = false;
        const number = paraMatch ? parseInt(paraMatch[1]) : parseInt(paraTextMatch[1]);
        const firstLine = paraTextMatch ? paraTextMatch[2] : '';

        // Close previous paragraph
        if (currentParagraph) {
          currentParagraph.text = currentParagraph.lines.join(' ').replace(/\s+/g, ' ').trim();
          currentParagraph.text_raw = currentParagraph.lines.join(' ');
          currentParagraph.text_lines = currentParagraph.lines.join(' | ');
          currentParagraph.section = currentHeading;
          currentParagraph.part = currentPart;
          paragraphs.push(currentParagraph);
        }

        // Start new paragraph
        currentParagraph = {
          number,
          lines: firstLine ? [firstLine] : [],
          page_start: line.page,
          page_end: line.page,
          footnotes_cited: []
        };

        if (firstLine) {
          repairs.push({
            page: line.page,
            type: 'paragraph',
            action: 'number and text split',
            before: text,
            after: `${number}.\n${firstLine}`
          });
        }
        continue;
      }

      // Check for labelled heading: Roman numeral or letter alone
      const headingMatch = text.match(/^([IVX]+|[A-Z])\.$/);
      if (headingMatch) {
        inCover = false;
        const label = headingMatch[1];
        let headingText = [];

        // Skip blank lines
        let j = i + 1;
        while (j < bodyLines.length && bodyLines[j].text.trim() === '') j++;

        // Collect heading text until next label or paragraph
        while (j < bodyLines.length) {
          const nextLine = bodyLines[j].text.trim();
          if (nextLine === '') {
            j++;
            continue;
          }
          if (/^([IVX]+|[A-Z])\.$/.test(nextLine) || /^\d{1,3}\.$/.test(nextLine) || /^\d{1,3}\. .+$/.test(nextLine)) {
            break;
          }
          headingText.push(nextLine);
          j++;
        }

        const heading = {
          label,
          text: headingText.join(' '),
          page: line.page,
          type: /^[IVX]+$/.test(label) ? 'part' : 'section'
        };

        if (heading.type === 'part') {
          currentPart = heading.text;
        }
        currentHeading = heading.text;
        headings.push(heading);

        // Join heading lines if more than one
        if (headingText.length > 1) {
          repairs.push({
            page: line.page,
            type: 'heading',
            action: 'heading title joined from two lines',
            before: headingText.join('\n'),
            after: headingText.join(' ')
          });
        }
        i = j - 1;
        continue;
      }

      // Check for unlabelled heading: line immediately before a paragraph start
      if (i + 1 < bodyLines.length) {
        const nextLine = bodyLines[i + 1].text.trim();
        const nextParaMatch = nextLine.match(/^(\d{1,3})\.$/);
        const nextParaTextMatch = nextLine.match(/^(\d{1,3})\. (.+)$/);

        if ((nextParaMatch || nextParaTextMatch) && text.length <= 90 && /^[A-Z]/.test(text) && !/[.;:,]\d?$/.test(text)) {
          inCover = false;
          const heading = {
            text,
            page: line.page,
            type: 'unlabelled'
          };
          currentHeading = heading.text;
          headings.push(heading);

          repairs.push({
            page: line.page,
            type: 'heading',
            action: 'heading separated from paragraph text',
            before: `${text}\n${nextLine}`,
            after: `${text}\n\n${nextLine}`
          });
          continue;
        }
      }

      // Add to current paragraph
      if (currentParagraph) {
        currentParagraph.lines.push(line.text);
        currentParagraph.page_end = line.page;
      } else if (!inCover) {
        // Lines before the first paragraph are cover
        line.type = 'cover';
      }
    }

    // Close the last paragraph
    if (currentParagraph) {
      currentParagraph.text = currentParagraph.lines.join(' ').replace(/\s+/g, ' ').trim();
      currentParagraph.text_raw = currentParagraph.lines.join(' ');
      currentParagraph.text_lines = currentParagraph.lines.join(' | ');
      currentParagraph.section = currentHeading;
      currentParagraph.part = currentPart;
      paragraphs.push(currentParagraph);
    }

    // Step 5: Extract footnote marks from paragraphs
    let expectedFootnote = 1;
    paragraphs.forEach(para => {
      const text = para.text_raw;
      const marks = [];
      let i = 0;

      while (i < text.length) {
        // Find a run of digits not touching another digit, slash, dash or opening parenthesis
        const start = i;
        while (i < text.length && /\d/.test(text[i])) i++;
        if (i > start) {
          const numStr = text.substring(start, i);
          const num = parseInt(numStr);
          const before = text[start - 1];
          const after = text[i];

          if (!/[0-9\/\-\(]/.test(before) && !/[0-9\/]/.test(after)) {
            if (num === expectedFootnote) {
              marks.push({
                number: num,
                start,
                end: i
              });
              expectedFootnote++;
            } else if (num > expectedFootnote) {
              checks.push({
                label: `Footnote mark ${num} in para. ${para.number} is unexpected`,
                value: `Expected ${expectedFootnote}, found ${num}`,
                pass: false
              });
            }
          }
        }
        i++;
      }

      // Replace marks with [n]
      let newText = '';
      let last = 0;
      marks.forEach(mark => {
        newText += text.substring(last, mark.start);
        newText += `[${mark.number}]`;
        last = mark.end;
        para.footnotes_cited.push(mark.number);
      });
      newText += text.substring(last);
      para.text = newText.replace(/\s+/g, ' ').trim();
    });

    // Step 6: Extract first words
    paragraphs.forEach(para => {
      const words = para.text.replace(/\[\d+\]/g, '').split(/\s+/).filter(w => w.length > 0);
      para.first_words_found = words.slice(0, 6).join(' ');
      para.first_words_reference = doc.reference.first_words[para.number] || '';
      para.first_words_match = normalize(para.first_words_found) === normalize(para.first_words_reference);
    });

    // Step 7: Add citations
    paragraphs.forEach(para => {
      para.citation = `${doc.symbol}, para. ${para.number}`;
    });

    // Step 8: Finalize footnotes
    footnotes.forEach(f => {
      f.text = f.lines.join(' ').replace(/\s+/g, ' ').trim();
    });

    // Step 9: Checks
    runChecks();
  }

  // Run all checks
  function runChecks() {
    // Paragraph count
    const paraCount = paragraphs.length;
    const paraRefCount = doc.reference.paragraphs;
    checks.push({
      label: 'Paragraph count',
      value: `${paraCount} found, ${paraRefCount} expected`,
      pass: paraCount === paraRefCount
    });

    // Paragraph numbering
    const numbers = paragraphs.map(p => p.number);
    const uniqueNumbers = [...new Set(numbers)];
    const missing = [];
    const duplicates = [];

    for (let i = 1; i <= paraRefCount; i++) {
      if (!numbers.includes(i)) missing.push(i);
      if (numbers.filter(n => n === i).length > 1) duplicates.push(i);
    }

    if (missing.length > 0 || duplicates.length > 0) {
      let value = '';
      if (missing.length > 0) value += `Missing: ${missing.join(', ')}. `;
      if (duplicates.length > 0) value += `Duplicates: ${duplicates.join(', ')}`;
      checks.push({
        label: 'Paragraph numbering',
        value,
        pass: false
      });
    } else {
      checks.push({
        label: 'Paragraph numbering',
        value: 'Numbers 1 to n in order',
        pass: true
      });
    }

    // First words
    const firstWordsMismatches = paragraphs.filter(p => !p.first_words_match);
    if (firstWordsMismatches.length > 0) {
      checks.push({
        label: 'First words',
        value: `${firstWordsMismatches.length} mismatches`,
        pass: false,
        details: firstWordsMismatches.map(p => ({
          para: p.number,
          found: p.first_words_found,
          reference: p.first_words_reference
        }))
      });
    } else {
      checks.push({
        label: 'First words',
        value: 'All match',
        pass: true
      });
    }

    // Footnotes
    const footnoteNumbers = footnotes.map(f => f.number).filter(n => n !== '*');
    const footnoteCount = footnoteNumbers.length;
    const footnoteRefCount = doc.reference.footnotes;
    checks.push({
      label: 'Footnote count',
      value: `${footnoteCount} found, ${footnoteRefCount} expected`,
      pass: footnoteCount === footnoteRefCount
    });

    const uniqueFootnoteNumbers = [...new Set(footnoteNumbers)];
    const missingFootnotes = [];
    const duplicateFootnotes = [];

    for (let i = 1; i <= footnoteRefCount; i++) {
      if (!uniqueFootnoteNumbers.includes(i)) missingFootnotes.push(i);
      if (footnoteNumbers.filter(n => n === i).length > 1) duplicateFootnotes.push(i);
    }

    if (missingFootnotes.length > 0 || duplicateFootnotes.length > 0) {
      let value = '';
      if (missingFootnotes.length > 0) value += `Missing: ${missingFootnotes.join(', ')}. `;
      if (duplicateFootnotes.length > 0) value += `Duplicates: ${duplicateFootnotes.join(', ')}`;
      checks.push({
        label: 'Footnote numbering',
        value,
        pass: false
      });
    } else {
      checks.push({
        label: 'Footnote numbering',
        value: 'Numbers 1 to n in order',
        pass: true
      });
    }

    const restoredFootnotes = footnotes.filter(f => f.repaired).map(f => f.number);
    if (restoredFootnotes.length > 0) {
      checks.push({
        label: 'Footnote numbers restored',
        value: restoredFootnotes.join(', '),
        pass: true
      });
    }

    // Footnote marks
    const expectedMarks = Array.from({length: footnoteRefCount}, (_, i) => i + 1);
    const foundMarks = [];
    paragraphs.forEach(p => {
      foundMarks.push(...p.footnotes_cited);
    });
    const uniqueFoundMarks = [...new Set(foundMarks)].sort((a, b) => a - b);
    const missingMarks = expectedMarks.filter(m => !uniqueFoundMarks.includes(m));
    const unexpectedMarks = uniqueFoundMarks.filter(m => m > footnoteRefCount);

    if (missingMarks.length > 0 || unexpectedMarks.length > 0) {
      let value = '';
      if (missingMarks.length > 0) value += `Missing: ${missingMarks.join(', ')}. `;
      if (unexpectedMarks.length > 0) {
        const contexts = unexpectedMarks.map(m => {
          const para = paragraphs.find(p => p.footnotes_cited.includes(m));
          const text = para.text_raw;
          const start = Math.max(0, text.indexOf(m) - 10);
          const end = Math.min(text.length, text.indexOf(m) + m.toString().length + 10);
          return `${m} in para. ${para.number}: …${text.substring(start, end)}…`;
        });
        value += `Unexpected: ${contexts.join('; ')}`;
      }
      checks.push({
        label: 'Footnote marks in text',
        value,
        pass: false
      });
    } else {
      checks.push({
        label: 'Footnote marks in text',
        value: 'All expected marks found',
        pass: true
      });
    }

    // Footnotes stay out of paragraphs
    const footnoteLines = footnotes.map(f => {
      const firstLine = f.lines[0] || '';
      return `${f.number} ${firstLine.substring(0, 40)}`;
    });
    let footnoteInParagraph = false;
    const paragraphsWithFootnotes = [];

    paragraphs.forEach(para => {
      const text = para.text_raw;
      footnoteLines.forEach(line => {
        if (text.includes(line)) {
          footnoteInParagraph = true;
          paragraphsWithFootnotes.push(para.number);
        }
      });
    });

    if (footnoteInParagraph) {
      checks.push({
        label: 'Footnotes stay out of paragraphs',
        value: `${paragraphsWithFootnotes.length} paragraphs contain footnotes: ${paragraphsWithFootnotes.join(', ')}`,
        pass: false
      });
    } else {
      checks.push({
        label: 'Footnotes stay out of paragraphs',
        value: 'No footnotes in paragraphs',
        pass: true
      });
    }

    // Headers and footers
    const pagesWithHeader = rawLines.filter(page => {
      const firstLine = page.lines.find(line => line.text.trim() !== '');
      return firstLine && firstLine.text.trim() === doc.symbol;
    }).length;
    checks.push({
      label: 'Headers',
      value: `${pagesWithHeader} of ${rawLines.length} pages have the symbol as first line`,
      pass: pagesWithHeader === rawLines.length
    });

    const pagesWithPageNumber = rawLines.filter(page => {
      return page.lines.some(line => line.type === 'footer' && /^\d{1,3}$/.test(line.text.trim()) && parseInt(line.text.trim()) === page.page);
    }).length;
    checks.push({
      label: 'Page numbers in footer',
      value: `${pagesWithPageNumber} of ${rawLines.length} pages have the page number in the footer`,
      pass: pagesWithPageNumber === rawLines.length - 1  // page 1 has no page number
    });

    const displacedNumbers = Object.entries(displacedFootnoteNumbers).map(([page, num]) => `${num} on page ${page}`);
    if (displacedNumbers.length > 0) {
      checks.push({
        label: 'Displaced footnote numbers',
        value: displacedNumbers.join(', '),
        pass: true
      });
    }

    // Headings
    const labelledHeadings = headings.filter(h => h.label).length;
    const unlabelledHeadings = headings.filter(h => !h.label).length;
    checks.push({
      label: 'Headings',
      value: `${labelledHeadings} labelled, ${unlabelledHeadings} unlabelled`,
      pass: true,
      details: headings.filter(h => !h.label).map(h => h.text)
    });

    // Nothing lost
    const totalLines = rawLines.reduce((sum, page) => sum + page.lines.length, 0);
    const classifiedLines = rawLines.reduce((sum, page) => sum + page.lines.filter(line => line.type).length, 0);
    const unclassifiedLines = rawLines.reduce((sum, page) => sum + page.lines.filter(line => !line.type).length, 0);

    if (unclassifiedLines > 0) {
      const unclassified = rawLines.flatMap(page => page.lines.filter(line => !line.type).map(line => ({
        page: page.page,
        line: line.line,
        text: line.text
      })));
      checks.push({
        label: 'Nothing lost',
        value: `${unclassifiedLines} unclassified lines`,
        pass: false,
        details: unclassified
      });
    } else {
      checks.push({
        label: 'Nothing lost',
        value: `${classifiedLines} of ${totalLines} lines classified`,
        pass: true
      });
    }

    // Summary
    const passedChecks = checks.filter(c => c.pass).length;
    const totalChecks = checks.length;
    const checksPass = passedChecks === totalChecks;

    // Update UI
    updateUI();
  }

  // Update the UI
  function updateUI() {
    // Header
    docTitle.textContent = doc.title;
    docSymbol.textContent = doc.symbol;
    docSymbol.href = doc.doc_url;
    docAdopted.textContent = `adopted ${doc.reference.adopted}`;
    docPages.textContent = `${doc.pages.length} pages of raw converter text`;
    docDescription.textContent = 'Splits the raw PDF converter text into numbered paragraphs and footnotes, removes headers, footers and footnotes, checks itself against the document’s own reference, and lists every repair it made.';

    // Rail
    docParagraphsFound.textContent = paragraphs.length;
    docParagraphsReference.textContent = doc.reference.paragraphs;
    const paraBarWidth = (paragraphs.length / doc.reference.paragraphs) * 100;
    docParagraphsBar.style.width = `${paraBarWidth}%`;
    if (paragraphs.length !== doc.reference.paragraphs) {
      docParagraphsBar.parentElement.classList.add('fail');
    }

    docFootnotesFound.textContent = footnotes.filter(f => f.number !== '*').length;
    docFootnotesReference.textContent = doc.reference.footnotes;
    const footnoteBarWidth = (footnotes.filter(f => f.number !== '*').length / doc.reference.footnotes) * 100;
    docFootnotesBar.style.width = `${footnoteBarWidth}%`;
    if (footnotes.filter(f => f.number !== '*').length !== doc.reference.footnotes) {
      docFootnotesBar.parentElement.classList.add('fail');
    }

    const passedChecks = checks.filter(c => c.pass).length;
    const totalChecks = checks.length;
    docChecksDot.className = `dot ${passedChecks === totalChecks ? 'pass' : 'fail'}`;
    docChecksText.textContent = `${passedChecks} of ${totalChecks} checks pass`;

    // Tiles
    paragraphsFound.textContent = paragraphs.length;
    if (paragraphs.length !== doc.reference.paragraphs) {
      paragraphsFound.classList.add('fail');
      paragraphsFound.textContent += ` (${Math.abs(paragraphs.length - doc.reference.paragraphs)} ${paragraphs.length > doc.reference.paragraphs ? 'over' : 'short'})`;
    }

    paragraphsReference.textContent = doc.reference.paragraphs;

    const footnoteCount = footnotes.filter(f => f.number !== '*').length;
    footnotesFound.textContent = footnoteCount;
    if (footnoteCount !== doc.reference.footnotes) {
      footnotesFound.classList.add('fail');
      footnotesFound.textContent += ` (${Math.abs(footnoteCount - doc.reference.footnotes)} ${footnoteCount > doc.reference.footnotes ? 'over' : 'short'})`;
    }

    const firstWordsMatchCount = paragraphs.filter(p => p.first_words_match).length;
    firstWordsMatch.textContent = `${firstWordsMatchCount} of ${paragraphs.length}`;
    if (firstWordsMatchCount !== paragraphs.length) {
      firstWordsMatch.classList.add('fail');
    }

    repairsLink.textContent = repairs.length;
    repairsLink.addEventListener('click', (e) => {
      e.preventDefault();
      const tab = document.getElementById('tab-04');
      const panel = document.getElementById('panel-04');
      tabs.forEach(t => {
        t.setAttribute('aria-selected', 'false');
        t.classList.remove('active');
      });
      tab.setAttribute('aria-selected', 'true');
      tab.classList.add('active');
      panels.forEach(p => p.classList.add('hidden'));
      panel.classList.remove('hidden');
      repairLogButton.setAttribute('aria-expanded', 'true');
      repairLogContent.hidden = false;
    });

    // Paragraphs tab
    headingsCount.textContent = headings.length;
    headingsListContent.innerHTML = '';
    headings.forEach(h => {
      const li = document.createElement('li');
      li.textContent = h.label ? `${h.label}. ${h.text}` : h.text;
      headingsListContent.appendChild(li);
    });

    paragraphsTable.innerHTML = '';
    paragraphs.forEach(para => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="number">${para.number}</td>
        <td>${para.section || ''}</td>
        <td class="page">${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}</td>
        <td>${para.text.substring(0, 120)}${para.text.length > 120 ? '…' : ''}</td>
        <td class="check ${para.first_words_match ? 'pass' : 'fail'}">${para.first_words_match ? 'OK' : 'first words differ'}</td>
      `;
      tr.setAttribute('aria-expanded', 'false');
      tr.addEventListener('click', () => {
        const expanded = tr.getAttribute('aria-expanded') === 'true';
        tr.setAttribute('aria-expanded', !expanded);
        const detailRow = document.getElementById(`para-${para.number}-detail`);
        if (detailRow) {
          detailRow.style.display = expanded ? 'none' : 'table-row';
        } else {
          const detailTr = document.createElement('tr');
          detailTr.id = `para-${para.number}-detail`;
          detailTr.className = 'detail';
          detailTr.innerHTML = `
            <td colspan="5">
              <pre>${escapeHtml(para.text)}</pre>
              <div class="meta">
                <div>
                  <span class="dot ${para.first_words_match ? 'pass' : 'fail'}"></span>
                  <span class="words">Found: "${escapeHtml(para.first_words_found)}"</span>
                </div>
                <div>
                  <span class="words">Reference: "${escapeHtml(para.first_words_reference)}"</span>
                </div>
              </div>
              <div class="meta">
                <div>Page: ${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}</div>
              </div>
              ${para.repairs && para.repairs.length > 0 ? `
              <div class="repairs">
                <div>Repairs:</div>
                ${para.repairs.map(r => `<div>${r}</div>`).join('')}
              </div>
              ` : ''}
              <button class="copy" onclick="copyCitation('${doc.symbol}', ${para.number})">Copy citation</button>
              <button class="secondary" onclick="toggleLines(${para.number})">Show the PDF's lines</button>
              <div id="para-${para.number}-lines" hidden>
                <pre>${escapeHtml(para.text_lines)}</pre>
              </div>
            </td>
          `;
          tr.parentNode.insertBefore(detailTr, tr.nextSibling);
        }
      });
      paragraphsTable.appendChild(tr);
    });

    // Footnotes tab
    footnotesCount.textContent = footnotes.filter(f => f.number !== '*').length;
    footnotesReferenceCount.textContent = doc.reference.footnotes;
    footnotesTable.innerHTML = '';
    footnotes.filter(f => f.number !== '*').forEach(f => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="number">${f.number}</td>
        <td class="page">${f.page}</td>
        <td>${escapeHtml(f.text)}</td>
        <td class="repair">${f.repaired ? 'number restored from the page foot' : ''}</td>
      `;
      footnotesTable.appendChild(tr);
    });

    downloadFootnotes.addEventListener('click', () => {
      const headers = ['number', 'page', 'text', 'repaired'];
      const rows = footnotes.filter(f => f.number !== '*').map(f => [
        f.number,
        f.page,
        `"${f.text.replace(/"/g, '""')}"`,
        f.repaired
      ]);
      const csv = [headers.join(','), ...rows.map(row => row.join(','))].join('\r\n');
      const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${doc.symbol.replace(/\//g, '-')}-footnotes.csv`;
      a.click();
      URL.revokeObjectURL(url);
    });

    // Checks tab
    checksList.innerHTML = '';
    checks.forEach(check => {
      const div = document.createElement('div');
      div.className = `check ${check.pass ? 'pass' : 'fail'}`;
      div.innerHTML = `
        <span class="dot ${check.pass ? 'pass' : 'fail'}"></span>
        <span class="label">${check.label}</span>
        <span class="value">${check.value}</span>
      `;
      if (!check.pass && check.details) {
        if (check.label === 'First words') {
          const ul = document.createElement('ul');
          check.details.forEach(d => {
            const li = document.createElement('li');
            li.innerHTML = `para. ${d.para}: found <span class="words">${escapeHtml(d.found)}</span> / reference <span class="words">${escapeHtml(d.reference)}</span>`;
            ul.appendChild(li);
          });
          div.appendChild(ul);
        } else if (check.label === 'Headings' && check.details.length > 0) {
          const ul = document.createElement('ul');
          check.details.forEach(d => {
            const li = document.createElement('li');
            li.textContent = d;
            ul.appendChild(li);
          });
          div.appendChild(ul);
        } else if (check.label === 'Nothing lost' && check.details.length > 0) {
          const ul = document.createElement('ul');
          check.details.forEach(d => {
            const li = document.createElement('li');
            li.textContent = `Page ${d.page}, line ${d.line}: ${d.text}`;
            ul.appendChild(li);
          });
          div.appendChild(ul);
        } else if (check.label === 'Footnotes stay out of paragraphs') {
          const a = document.createElement('a');
          a.href = '#';
          a.textContent = ' (see paragraphs)';
          a.addEventListener('click', (e) => {
            e.preventDefault();
            const tab = document.getElementById('tab-02');
            const panel = document.getElementById('panel-02');
            tabs.forEach(t => {
              t.setAttribute('aria-selected', 'false');
              t.classList.remove('active');
            });
            tab.setAttribute('aria-selected', 'true');
            tab.classList.add('active');
            panels.forEach(p => p.classList.add('hidden'));
            panel.classList.remove('hidden');
          });
          div.appendChild(a);
        }
      }
      checksList.appendChild(div);
    });

    repairLogCount.textContent = repairs.length;
    repairCounts.innerHTML = '';
    const repairTypes = [...new Set(repairs.map(r => r.action))];
    repairTypes.forEach(type => {
      const count = repairs.filter(r => r.action === type).length;
      const div = document.createElement('div');
      div.innerHTML = `<span class="dot pass"></span> ${count} ${type}`;
      repairCounts.appendChild(div);
    });

    repairLogTable.innerHTML = '';
    repairs.forEach(repair => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${repair.page}</td>
        <td>${repair.type === 'paragraph' ? `para. ${paragraphs.find(p => p.page_start === repair.page && p.lines.includes(repair.before.split('\n')[0]))?.number || '?'}` : repair.type === 'footnote' ? `footnote ${footnotes.find(f => f.page === repair.page && f.lines.includes(repair.before.split('\n')[0]))?.number || '?'}` : ''}</td>
        <td>${repair.action}</td>
        <td class="before">${escapeHtml(repair.before)}</td>
        <td class="after">${escapeHtml(repair.after)}</td>
      `;
      repairLogTable.appendChild(tr);
    });

    // Raw pages
    rawPageSelect.innerHTML = '<option value="">Select a page</option>';
    rawLines.forEach(page => {
      const option = document.createElement('option');
      option.value = page.page;
      option.textContent = `Page ${page.page}`;
      rawPageSelect.appendChild(option);
    });

    // Footer
    document.getElementById('doc-source').textContent = doc.source;
    document.getElementById('doc-built').textContent = doc.built;

    // Summary
    const passedChecks = checks.filter(c => c.pass).length;
    const totalChecks = checks.length;
    checksDot.className = `dot ${passedChecks === totalChecks ? 'pass' : 'fail'}`;
    checksText.textContent = `${passedChecks} of ${totalChecks} checks ${passedChecks === totalChecks ? 'pass' : 'failed'}`;
    if (passedChecks !== totalChecks) {
      document.getElementById('tab-04').classList.add('fail-tab');
    }
  }

  // Toggle lines
  function toggleLines(number) {
    const div = document.getElementById(`para-${number}-lines`);
    const button = event.target;
    const expanded = div.hidden;
    div.hidden = !expanded;
    button.textContent = expanded ? 'Hide the PDF\'s lines' : 'Show the PDF\'s lines';
  }

  // Download paragraphs as CSV
  downloadParagraphs.addEventListener('click', () => {
    const headers = [
      'number', 'section', 'part', 'page_start', 'page_end',
      'first_words_reference', 'first_words_found', 'first_words_match',
      'text', 'text_raw', 'text_lines', 'footnotes_cited', 'repairs',
      'citation', 'symbol', 'doc_url'
    ];
    const rows = paragraphs.map(p => [
      p.number,
      `"${(p.section || '').replace(/"/g, '""')}"`,
      `"${(p.part || '').replace(/"/g, '""')}"`,
      p.page_start,
      p.page_end,
      `"${(p.first_words_reference || '').replace(/"/g, '""')}"`,
      `"${(p.first_words_found || '').replace(/"/g, '""')}"`,
      p.first_words_match,
      `"${p.text.replace(/"/g, '""')}"`,
      `"${(p.text_raw || '').replace(/"/g, '""')}"`,
      `"${(p.text_lines || '').replace(/"/g, '""')}"`,
      `"${p.footnotes_cited.join(', ')}"`,
      `"${(p.repairs || []).join('; ')}"`,
      `"${p.citation}"`,
      `"${doc.symbol}"`,
      `"${doc.doc_url}"`
    ]);
    const csv = [headers.join(','), ...rows.map(row => row.join(','))].join('\r\n');
    const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${doc.symbol.replace(/\//g, '-')}-paragraphs.csv`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Start
  parseDocument();
})();
</script>
</body>
</html>
```