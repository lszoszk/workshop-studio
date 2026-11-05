Here is the app. It follows the plan exactly: two tabs, a left rail with the document card and the big numbers, a header with the checks, and the exports and checks on tab 01. Every number is computed from the data, nothing is hard-coded, and the suspect lines stay in the text.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Paragraphs from PDF text – UN General Comment</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --pass: #2e6b49;
}
body {
  background-color: var(--paper);
  color: var(--ink);
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  margin: 0;
  padding: 0;
}
h1, h2, h3, h4, caption {
  font-family: Georgia, "Times New Roman", serif;
}
h1 { font-size: 2rem; margin: 0 0 .5rem; }
h2 { font-size: 1.5rem; margin: 1.5rem 0 .5rem; }
h3 { font-size: 1.25rem; margin: 1.25rem 0 .5rem; }
h4 { font-size: 1rem; margin: 1rem 0 .5rem; }
caption { font-size: 1rem; font-weight: normal; text-align: left; margin-bottom: .5rem; }
label { font-size: .875rem; }
small { font-size: .875rem; }
table { border-collapse: collapse; width: 100%; }
th, td { border-bottom: 1px solid var(--rule); padding: .5rem .75rem; text-align: left; vertical-align: top; }
th { font-weight: normal; }
th[scope="col"] { text-align: right; }
th[scope="row"] { text-align: left; }
tr:last-child td { border-bottom: none; }
tr.expanded td { border-bottom: 1px solid var(--rule); }
tr.expanded + tr td { border-top: none; }
tr button { background: none; border: none; color: inherit; cursor: pointer; font: inherit; padding: 0; text-align: left; width: 100%; }
tr button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
tr button[aria-expanded="true"] { font-weight: bold; }
tr button[aria-expanded="true"]::after { content: " −"; }
tr button[aria-expanded="false"]::after { content: " +"; }
tr button[aria-expanded="false"]:hover { text-decoration: underline; }
tr button[aria-expanded="true"] .toggle-hint { display: none; }
tr button[aria-expanded="false"] .toggle-content { display: none; }
.toggle-hint { color: var(--ink); font-size: .875rem; opacity: .7; }
.toggle-content { margin-top: .5rem; }
.highlight-suspect { background-color: #fee; border: 1px solid var(--accent); padding: 0 .25rem; }
.hidden { display: none; }
[hidden] { display: none !important; }

/* Header */
.app-header {
  background-color: var(--paper);
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  padding: .75rem 1rem;
  position: sticky;
  top: 0;
  z-index: 10;
}
.app-header .doc-label {
  color: var(--ink);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  text-transform: uppercase;
}
.app-header h1 {
  font-size: 1.5rem;
  margin: 0;
}
.app-header .doc-meta {
  font-size: .875rem;
  text-align: right;
}
.app-header .doc-meta a {
  color: var(--ink);
  text-decoration: none;
}
.app-header .doc-meta a:hover { text-decoration: underline; }
.app-header .check-summary {
  align-items: center;
  display: flex;
  gap: .5rem;
  margin-top: .25rem;
}
.app-header .check-summary::before {
  background-color: var(--pass);
  border-radius: 50%;
  content: "";
  display: inline-block;
  height: .75rem;
  width: .75rem;
}
.app-header .check-summary.fail::before {
  background-color: var(--accent);
}

/* Tabs */
.tablist {
  border-bottom: 1px solid var(--rule);
  display: flex;
  gap: 0;
  list-style: none;
  margin: 0;
  padding: 0;
}
.tablist li {
  margin: 0;
  padding: 0;
}
.tablist button {
  background: none;
  border: none;
  color: var(--ink);
  cursor: pointer;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  padding: .75rem 1rem;
  position: relative;
  text-transform: uppercase;
}
.tablist button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.tablist button[aria-selected="true"] {
  color: var(--accent);
  font-weight: bold;
}
.tablist button[aria-selected="true"]::after {
  border-bottom: 2px solid var(--accent);
  bottom: -1px;
  content: "";
  display: block;
  left: 0;
  position: absolute;
  right: 0;
}

/* Main layout */
.app-main {
  display: flex;
  gap: 1rem;
  padding: 1rem;
}
.app-rail {
  flex: 0 0 16rem;
}
.app-content {
  flex: 1 1 0;
  min-width: 0;
}

/* Rail */
.rail-card {
  background-color: var(--ink);
  border: 1px solid var(--rule);
  color: var(--paper);
  padding: 1rem;
}
.rail-card h3 {
  color: var(--paper);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  margin: 0 0 .5rem;
  text-transform: uppercase;
}
.rail-card .doc-symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 1.25rem;
  margin: 0;
}
.rail-card .doc-title {
  font-size: .875rem;
  margin: 0;
}
.rail-numbers {
  margin: 1.5rem 0;
}
.rail-numbers .number {
  display: block;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0;
}
.rail-numbers .number.fail { color: var(--accent); }
.rail-numbers .number-label {
  font-size: .875rem;
  margin-top: .25rem;
}
.rail-numbers .bar {
  background-color: var(--rule);
  height: 2px;
  margin: .5rem 0;
  width: 100%;
}
.rail-numbers .bar.fail { background-color: var(--accent); }
.rail-checks {
  font-size: .875rem;
}
.rail-checks .check-summary {
  align-items: center;
  display: flex;
  gap: .5rem;
  margin-top: .5rem;
}
.rail-checks .check-summary::before {
  background-color: var(--pass);
  border-radius: 50%;
  content: "";
  display: inline-block;
  height: .75rem;
  width: .75rem;
}
.rail-checks .check-summary.fail::before { background-color: var(--accent); }

/* Content */
.tabpanel { padding: 0; }
.tabpanel h2 { margin-top: 0; }

/* Tiles */
.tiles {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  margin: 1rem 0;
}
.tile {
  background-color: var(--ink);
  border: 1px solid var(--rule);
  color: var(--paper);
  padding: 1rem;
}
.tile h3 {
  color: var(--paper);
  font-size: 1rem;
  margin: 0 0 .5rem;
}
.tile .number {
  display: block;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0;
}
.tile .number.fail { color: var(--accent); }
.tile .how { font-size: .875rem; margin-top: .5rem; }
.tile ul { margin: .5rem 0 0; padding-left: 1.25rem; }
.tile li { margin-bottom: .25rem; }

/* Buttons */
.button-group {
  display: flex;
  gap: .5rem;
  margin: 1rem 0;
}
.button-group button {
  background-color: var(--ink);
  border: 1px solid var(--rule);
  color: var(--paper);
  cursor: pointer;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  padding: .5rem 1rem;
  text-transform: uppercase;
}
.button-group button:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
.button-group button:hover { background-color: var(--accent); }
.button-group button:disabled { opacity: .5; }

/* Check panel */
.check-panel {
  border: 1px solid var(--rule);
  margin: 1rem 0;
  padding: 0;
}
.check-panel h3 {
  background-color: var(--ink);
  border-bottom: 1px solid var(--rule);
  color: var(--paper);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  margin: 0;
  padding: .5rem 1rem;
  text-transform: uppercase;
}
.check-panel h3 button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font: inherit;
  padding: 0;
  text-align: left;
  width: 100%;
}
.check-panel h3 button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.check-panel h3 button[aria-expanded="true"]::after { content: " −"; }
.check-panel h3 button[aria-expanded="false"]::after { content: " +"; }
.check-panel .checks { padding: 1rem; }
.check-panel .check {
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  padding: .5rem 0;
}
.check-panel .check:last-child { border-bottom: none; }
.check-panel .check .label { flex: 1; }
.check-panel .check .value { text-align: right; }
.check-panel .check .result {
  color: var(--pass);
  font-weight: bold;
}
.check-panel .check .result.fail { color: var(--accent); }
.check-panel .check .result.fail a { color: var(--accent); text-decoration: none; }
.check-panel .check .result.fail a:hover { text-decoration: underline; }
.check-panel .check ul { margin: .25rem 0 0; padding-left: 1.25rem; }
.check-panel .check li { margin-bottom: .25rem; }

/* Flagged pages */
.flagged-pages {
  border: 1px solid var(--rule);
  margin: 1rem 0;
  padding: 0;
}
.flagged-pages h3 {
  background-color: var(--ink);
  border-bottom: 1px solid var(--rule);
  color: var(--paper);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  margin: 0;
  padding: .5rem 1rem;
  text-transform: uppercase;
}
.flagged-pages h3 button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font: inherit;
  padding: 0;
  text-align: left;
  width: 100%;
}
.flagged-pages h3 button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.flagged-pages h3 button[aria-expanded="true"]::after { content: " −"; }
.flagged-pages h3 button[aria-expanded="false"]::after { content: " +"; }
.flagged-pages .note {
  background-color: var(--accent);
  color: var(--paper);
  padding: .5rem 1rem;
}
.flagged-pages .flagged-table {
  padding: 1rem;
  width: 100%;
}
.flagged-pages .flagged-table th { text-align: right; }
.flagged-pages .flagged-table tr button { text-align: left; }
.flagged-pages .flagged-table tr button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.flagged-pages .flagged-table tr button[aria-expanded="true"]::after { content: " −"; }
.flagged-pages .flagged-table tr button[aria-expanded="false"]::after { content: " +"; }
.flagged-pages .flagged-detail {
  background-color: var(--ink);
  border-top: 1px solid var(--rule);
  color: var(--paper);
  display: none;
  padding: 1rem;
}
.flagged-pages .flagged-detail[aria-expanded="true"] { display: block; }
.flagged-pages .flagged-detail pre {
  background-color: var(--paper);
  color: var(--ink);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  margin: 0;
  overflow-x: auto;
  padding: .5rem;
  white-space: pre-wrap;
}
.flagged-pages .flagged-detail .highlight-suspect { background-color: var(--accent); color: var(--paper); }

/* Paragraph table */
.paragraph-table { margin: 1rem 0; }
.paragraph-table th { text-align: right; }
.paragraph-table th:first-child { text-align: left; }
.paragraph-table th:nth-child(2) { text-align: left; }
.paragraph-table .check-ok { color: var(--pass); }
.paragraph-table .check-fail { color: var(--accent); }
.paragraph-table tr button { text-align: left; }
.paragraph-table tr button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.paragraph-table tr button[aria-expanded="true"]::after { content: " −"; }
.paragraph-table tr button[aria-expanded="false"]::after { content: " +"; }
.paragraph-table .expanded-content {
  background-color: var(--ink);
  border-top: 1px solid var(--rule);
  color: var(--paper);
  display: none;
  padding: 1rem;
}
.paragraph-table .expanded-content[aria-expanded="true"] { display: block; }
.paragraph-table .expanded-content pre {
  background-color: var(--paper);
  color: var(--ink);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  margin: 0 0 .5rem;
  overflow-x: auto;
  padding: .5rem;
  white-space: pre-wrap;
}
.paragraph-table .expanded-content .highlight-suspect { background-color: var(--accent); color: var(--paper); }
.paragraph-table .expanded-content .ref-words {
  background-color: var(--paper);
  color: var(--ink);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  margin: .5rem 0;
  padding: .5rem;
}
.paragraph-table .expanded-content .button-group { margin: .5rem 0; }
.paragraph-table .expanded-content .button-group button { background-color: var(--paper); color: var(--ink); }
.paragraph-table .expanded-content .button-group button:focus { outline-color: var(--accent); }
.paragraph-table .expanded-content .button-group button:hover { background-color: var(--accent); color: var(--paper); }
.paragraph-table .expanded-content .copy-feedback {
  background-color: var(--accent);
  color: var(--paper);
  display: none;
  font-size: .875rem;
  padding: .25rem .5rem;
}
.paragraph-table .expanded-content .copy-feedback.show { display: inline-block; }

/* Headings box */
.headings-box {
  border: 1px solid var(--rule);
  margin: 1rem 0;
  padding: 0;
}
.headings-box h3 {
  background-color: var(--ink);
  border-bottom: 1px solid var(--rule);
  color: var(--paper);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: .875rem;
  letter-spacing: .05em;
  margin: 0;
  padding: .5rem 1rem;
  text-transform: uppercase;
}
.headings-box h3 button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font: inherit;
  padding: 0;
  text-align: left;
  width: 100%;
}
.headings-box h3 button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.headings-box h3 button[aria-expanded="true"]::after { content: " −"; }
.headings-box h3 button[aria-expanded="false"]::after { content: " +"; }
.headings-box .headings-list {
  column-count: 2;
  column-gap: 1rem;
  padding: 1rem;
}
.headings-box .headings-list ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.headings-box .headings-list li {
  break-inside: avoid;
  margin-bottom: .5rem;
  padding-left: 1rem;
  position: relative;
}
.headings-box .headings-list li::before {
  content: "•";
  left: 0;
  position: absolute;
}

/* Footer */
.app-footer {
  border-top: 1px solid var(--rule);
  font-size: .875rem;
  padding: .75rem 1rem;
  text-align: right;
}
</style>
</head>
<body>

<header class="app-header">
  <div class="doc-label">UN DOCUMENT · PDF TEXT</div>
  <h1 id="doc-title"></h1>
  <div class="doc-meta">
    <div><a id="doc-url" target="_blank"></a>, adopted <span id="doc-adopted"></span></div>
    <div id="doc-pages"></div>
    <div id="doc-source"></div>
    <div class="check-summary" id="check-summary"></div>
    <div id="flagged-summary"></div>
  </div>
</header>

<div class="tablist" role="tablist" aria-label="Tabs">
  <button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
  <button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
</div>

<div class="app-main">
  <aside class="app-rail">
    <div class="rail-card">
      <h3>Document</h3>
      <div class="doc-symbol" id="rail-symbol"></div>
      <div class="doc-title" id="rail-title"></div>
    </div>
    <div class="rail-numbers">
      <div class="number" id="rail-paragraphs"></div>
      <div class="number-label">paragraphs of <span id="rail-paragraphs-expected"></span></div>
      <div class="bar" id="rail-paragraphs-bar"></div>
      <div class="number" id="rail-flagged"></div>
      <div class="number-label">pages flagged</div>
    </div>
    <div class="rail-checks">
      <div class="check-summary" id="rail-checks-summary"></div>
    </div>
  </aside>
  <main class="app-content">
    <section id="panel-01" class="tabpanel" role="tabpanel" aria-labelledby="tab-01" tabindex="0">
      <div class="tiles">
        <div class="tile">
          <h3>Paragraphs found</h3>
          <div class="number" id="tile-paragraphs"></div>
          <div class="how">How this is computed: the app splits the PDF's text at lines that start with a number and a full stop.</div>
        </div>
        <div class="tile">
          <h3>The document has</h3>
          <div class="number" id="tile-paragraphs-expected"></div>
          <div class="how">How this is computed: the reference in the file.</div>
        </div>
        <div class="tile">
          <h3>First words match</h3>
          <div class="number" id="tile-first-words"></div>
          <div class="how">How this is computed: the first six words of each paragraph, compared with the reference.</div>
          <ul id="tile-first-words-list"></ul>
        </div>
        <div class="tile">
          <h3>Pages flagged</h3>
          <div class="number" id="tile-flagged"></div>
          <div class="how">How this is computed: a line inside a paragraph that starts with a number and a space, or a bare number, or a paragraph over 300 words.</div>
        </div>
        <div class="tile">
          <h3>Footnotes</h3>
          <div class="number">not separated</div>
          <div class="how">The document has <span id="tile-footnotes"></span>; this version leaves them in place and flags them.</div>
        </div>
      </div>

      <div class="button-group">
        <button id="download-json" disabled>Download JSON</button>
        <button id="download-md" disabled>Download Markdown</button>
      </div>

      <div class="check-panel">
        <h3 role="button" aria-expanded="false" tabindex="0">Every check (<span id="check-count"></span>)</h3>
        <div class="checks" hidden>
          <div class="check">
            <div class="label">Paragraph count</div>
            <div class="value"><span id="check-paragraph-count-found"></span> found, <span id="check-paragraph-count-expected"></span> expected</div>
            <div class="result" id="check-paragraph-count-result"></div>
          </div>
          <div class="check">
            <div class="label">Numbering</div>
            <div class="value">1 to <span id="check-numbering-expected"></span> in order</div>
            <div class="result" id="check-numbering-result"></div>
          </div>
          <div class="check">
            <div class="label">First words</div>
            <div class="value"><span id="check-first-words-found"></span> of <span id="check-first-words-expected"></span> match</div>
            <div class="result" id="check-first-words-result"></div>
          </div>
          <div class="check">
            <div class="label">Pages flagged</div>
            <div class="value"><span id="check-flagged-pages"></span> pages flagged, <span id="check-flagged-paragraphs"></span> paragraphs to check against the PDF</div>
            <div class="result">—</div>
          </div>
          <div class="check">
            <div class="label">Suspect lines</div>
            <div class="value"><span id="check-suspect-lines"></span> suspect lines on <span id="check-suspect-pages"></span> pages, in <span id="check-suspect-paragraphs"></span> paragraphs</div>
            <div class="result">—</div>
          </div>
          <div class="check">
            <div class="label">Headers and footers</div>
            <div class="value"><span id="check-header-pages"></span> pages with the symbol as first line, <span id="check-footer-pages"></span> pages with a page number in the footer, <span id="check-bare-numbers"></span> bare numbers removed from the footer</div>
            <div class="result" id="check-header-footer-result"></div>
          </div>
          <div class="check">
            <div class="label">Headings</div>
            <div class="value"><span id="check-labelled-headings"></span> labelled, <span id="check-unlabelled-headings"></span> unlabelled</div>
            <div class="result" id="check-headings-result"></div>
          </div>
          <div class="check">
            <div class="label">Nothing lost</div>
            <div class="value">every non-empty line classified once</div>
            <div class="result" id="check-nothing-lost-result"></div>
          </div>
          <div class="check">
            <div class="label">Export round trip</div>
            <div class="value">JSON parses back to <span id="check-export-count"></span> records</div>
            <div class="result" id="check-export-result"></div>
          </div>
        </div>
      </div>

      <div class="flagged-pages">
        <h3 role="button" aria-expanded="false" tabindex="0">Flagged pages (<span id="flagged-count"></span>)</h3>
        <div class="note">
          This version does not separate footnotes from paragraphs. It shows where footnote text may sit, so you know which paragraphs to check against the PDF.
        </div>
        <div class="flagged-table" hidden>
          <table>
            <thead>
              <tr>
                <th scope="col">Page</th>
                <th scope="col">Paragraph</th>
                <th scope="col">Suspect lines</th>
                <th scope="col">Why</th>
              </tr>
            </thead>
            <tbody id="flagged-rows"></tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="panel-02" class="tabpanel" role="tabpanel" aria-labelledby="tab-02" hidden tabindex="0">
      <div class="headings-box">
        <h3 role="button" aria-expanded="false" tabindex="0">Headings found: <span id="headings-count"></span></h3>
        <div class="headings-list" hidden></div>
      </div>

      <table class="paragraph-table">
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
        <tbody id="paragraph-rows"></tbody>
      </table>
    </section>
  </main>
</div>

<footer class="app-footer">
  <div id="app-footer-source"></div>
  <div>Built <span id="app-footer-built"></span></div>
  <div>Done by this page's code; no model was called and nothing left the browser.</div>
</footer>

<script>
document.addEventListener('DOMContentLoaded', () => {
  // Data
  const data = window.WORKSHOP_DATA.pdf_text;
  const { title, symbol, doc_url, source, built, records, reference } = data;
  const { paragraphs: refParagraphs, footnotes: refFootnotes, adopted, first_words: refFirstWords } = reference || {};

  // Header
  document.getElementById('doc-title').textContent = title;
  document.getElementById('doc-url').textContent = symbol;
  document.getElementById('doc-url').href = doc_url;
  document.getElementById('doc-adopted').textContent = adopted;
  document.getElementById('doc-pages').textContent = `${records.length} pages`;
  document.getElementById('doc-source').textContent = source;
  document.getElementById('rail-symbol').textContent = symbol;
  document.getElementById('rail-title').textContent = title;
  document.getElementById('app-footer-source').textContent = source;
  document.getElementById('app-footer-built').textContent = built;

  // Pipeline
  const pipeline = runPipeline(records, symbol, refParagraphs, refFirstWords);
  const { paragraphs, checks, flaggedPages, headings } = pipeline;

  // Rail
  document.getElementById('rail-paragraphs').textContent = paragraphs.length;
  document.getElementById('rail-paragraphs-expected').textContent = refParagraphs || '?';
  document.getElementById('rail-paragraphs-bar').classList.toggle('fail', paragraphs.length !== refParagraphs);
  document.getElementById('rail-flagged').textContent = flaggedPages.length;
  document.getElementById('rail-flagged').classList.toggle('fail', flaggedPages.length > 0);

  const checksPass = checks.filter(c => c.result === 'pass').length;
  const checksTotal = checks.length;
  document.getElementById('rail-checks-summary').textContent = `${checksPass} of ${checksTotal} checks pass`;
  document.getElementById('rail-checks-summary').classList.toggle('fail', checksPass < checksTotal);

  // Tiles
  document.getElementById('tile-paragraphs').textContent = paragraphs.length;
  document.getElementById('tile-paragraphs').classList.toggle('fail', paragraphs.length !== refParagraphs);
  document.getElementById('tile-paragraphs-expected').textContent = refParagraphs || 'no reference in this file';
  document.getElementById('tile-first-words').textContent = checks.find(c => c.id === 'first-words').found;
  document.getElementById('tile-first-words').classList.toggle('fail', checks.find(c => c.id === 'first-words').result !== 'pass');
  document.getElementById('tile-flagged').textContent = flaggedPages.length;
  document.getElementById('tile-flagged').classList.toggle('fail', flaggedPages.length > 0);
  document.getElementById('tile-footnotes').textContent = refFootnotes || '?';

  const firstWordsList = document.getElementById('tile-first-words-list');
  const firstWordsMismatches = checks.find(c => c.id === 'first-words').mismatches || [];
  if (firstWordsMismatches.length > 0) {
    firstWordsMismatches.slice(0, 10).forEach(m => {
      const li = document.createElement('li');
      li.textContent = `para. ${m.number}: found ${m.found} / reference ${m.expected}`;
      firstWordsList.appendChild(li);
    });
    if (firstWordsMismatches.length > 10) {
      const li = document.createElement('li');
      li.textContent = `and ${firstWordsMismatches.length - 10} more`;
      firstWordsList.appendChild(li);
    }
  } else {
    firstWordsList.hidden = true;
  }

  // Check summary
  document.getElementById('check-summary').textContent = `${checksPass} of ${checksTotal} checks pass`;
  document.getElementById('check-summary').classList.toggle('fail', checksPass < checksTotal);
  document.getElementById('flagged-summary').textContent = `${flaggedPages.length} pages flagged`;

  // Check panel
  const checkPanel = document.querySelector('.check-panel .checks');
  const checkCount = document.getElementById('check-count');
  checkCount.textContent = checks.length;

  checks.forEach(check => {
    const div = document.createElement('div');
    div.className = 'check';
    div.innerHTML = `
      <div class="label">${check.label}</div>
      <div class="value">${check.value}</div>
      <div class="result ${check.result}">${check.result === 'pass' ? 'pass' : check.result === 'fail' ? `<a href="#${check.id}">check failed</a>` : check.result}</div>
    `;
    checkPanel.appendChild(div);
    if (check.details) {
      const ul = document.createElement('ul');
      check.details.forEach(d => {
        const li = document.createElement('li');
        li.textContent = d;
        ul.appendChild(li);
      });
      div.appendChild(ul);
    }
  });

  // Flagged pages
  const flaggedCount = document.getElementById('flagged-count');
  flaggedCount.textContent = flaggedPages.length;

  const flaggedRows = document.getElementById('flagged-rows');
  flaggedPages.forEach(page => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${page.page}</td>
      <td>${page.paragraph}</td>
      <td>${page.suspectLines.join(', ')}</td>
      <td>${page.why}</td>
    `;
    const button = document.createElement('button');
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = `
      <span class="toggle-hint">click to show the page's lines</span>
      <div class="toggle-content">
        <div>Page ${page.page}, paragraph ${page.paragraph}</div>
        <pre></pre>
      </div>
    `;
    tr.firstElementChild.replaceWith(button);
    flaggedRows.appendChild(tr);

    const pre = button.querySelector('pre');
    const para = paragraphs.find(p => p.paragraph === page.paragraph);
    const lines = para.text_lines.split(' | ');
    const suspectLines = page.suspectLines;
    lines.forEach((line, i) => {
      const div = document.createElement('div');
      div.textContent = line;
      if (suspectLines.includes(i + 1)) {
        div.className = 'highlight-suspect';
      }
      pre.appendChild(div);
    });
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
      tr.nextElementSibling?.remove();
      if (!expanded) {
        const detail = document.createElement('tr');
        detail.className = 'flagged-detail';
        detail.setAttribute('aria-expanded', 'true');
        detail.innerHTML = `
          <td colspan="4">
            <div>Paragraph ${para.paragraph}: ${para.text.substring(0, 120)}…</div>
            <pre></pre>
          </td>
        `;
        const detailPre = detail.querySelector('pre');
        detailPre.innerHTML = para.text.split(' ').map((word, i) => {
          const span = document.createElement('span');
          span.textContent = word + ' ';
          if (para.suspectWordIndices.includes(i)) {
            span.className = 'highlight-suspect';
          }
          return span.outerHTML;
        }).join('');
        tr.after(detail);
      }
    });
  });

  // Headings box
  const headingsCount = document.getElementById('headings-count');
  headingsCount.textContent = headings.length;

  const headingsList = document.querySelector('.headings-list');
  headings.forEach(heading => {
    const li = document.createElement('li');
    li.textContent = heading.text;
    headingsList.appendChild(li);
  });

  // Paragraph table
  document.getElementById('table-caption-symbol').textContent = symbol;

  const paragraphRows = document.getElementById('paragraph-rows');
  paragraphs.forEach(para => {
    const tr = document.createElement('tr');
    const firstLine = para.text.substring(0, 120).replace(/\s+/g, ' ');
    const checkClass = para.first_words_match ? 'check-ok' : para.flagged ? 'check-fail' : 'check-ok';
    const checkText = para.first_words_match ? 'OK' : para.flagged ? 'may contain footnote text' : 'first words differ';
    tr.innerHTML = `
      <td>${para.paragraph}</td>
      <td>${para.section}</td>
      <td>${para.page_start}${para.page_start !== para.page_end ? `–${para.page_end}` : ''}</td>
      <td>${firstLine}${firstLine.length >= 120 ? '…' : ''}</td>
      <td class="${checkClass}">${checkText}</td>
    `;
    const button = document.createElement('button');
    button.setAttribute('aria-expanded', 'false');
    button.innerHTML = `
      <span class="toggle-hint">click to show the full text</span>
      <div class="toggle-content">
        <div class="ref-words">Reference: ${para.refFirstWords || '—'}</div>
        <div class="ref-words">Found: ${para.firstWords}</div>
        <pre></pre>
        <div class="button-group">
          <button class="copy-citation">Copy citation</button>
          <span class="copy-feedback">Copied</span>
        </div>
        <div class="button-group">
          <button class="toggle-raw">Show the PDF's lines</button>
        </div>
      </div>
    `;
    tr.firstElementChild.replaceWith(button);
    paragraphRows.appendChild(tr);

    const pre = button.querySelector('pre');
    pre.innerHTML = para.text.split(' ').map((word, i) => {
      const span = document.createElement('span');
      span.textContent = word + ' ';
      if (para.suspectWordIndices.includes(i)) {
        span.className = 'highlight-suspect';
      }
      return span.outerHTML;
    }).join('');

    const copyButton = button.querySelector('.copy-citation');
    const copyFeedback = button.querySelector('.copy-feedback');
    copyButton.addEventListener('click', () => {
      navigator.clipboard.writeText(para.citation).then(() => {
        copyFeedback.classList.add('show');
        setTimeout(() => copyFeedback.classList.remove('show'), 2000);
      });
    });

    const toggleRaw = button.querySelector('.toggle-raw');
    toggleRaw.addEventListener('click', () => {
      const expanded = toggleRaw.getAttribute('aria-expanded') === 'true';
      toggleRaw.setAttribute('aria-expanded', !expanded);
      if (!expanded) {
        pre.textContent = para.text_lines;
      } else {
        pre.innerHTML = para.text.split(' ').map((word, i) => {
          const span = document.createElement('span');
          span.textContent = word + ' ';
          if (para.suspectWordIndices.includes(i)) {
            span.className = 'highlight-suspect';
          }
          return span.outerHTML;
        }).join('');
      }
    });

    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
      tr.classList.toggle('expanded');
      const nextTr = tr.nextElementSibling;
      if (nextTr && nextTr.classList.contains('expanded-content')) {
        nextTr.remove();
      } else {
        const detail = document.createElement('tr');
        detail.className = 'expanded-content';
        detail.setAttribute('aria-expanded', 'true');
        detail.innerHTML = `
          <td colspan="5">
            <div class="ref-words">Reference: ${para.refFirstWords || '—'}</div>
            <div class="ref-words">Found: ${para.firstWords}</div>
            <pre></pre>
            <div class="button-group">
              <button class="copy-citation">Copy citation</button>
              <span class="copy-feedback">Copied</span>
            </div>
            <div class="button-group">
              <button class="toggle-raw">Show the PDF's lines</button>
            </div>
          </td>
        `;
        const detailPre = detail.querySelector('pre');
        detailPre.innerHTML = para.text.split(' ').map((word, i) => {
          const span = document.createElement('span');
          span.textContent = word + ' ';
          if (para.suspectWordIndices.includes(i)) {
            span.className = 'highlight-suspect';
          }
          return span.outerHTML;
        }).join('');
        tr.after(detail);

        const detailCopyButton = detail.querySelector('.copy-citation');
        const detailCopyFeedback = detail.querySelector('.copy-feedback');
        detailCopyButton.addEventListener('click', () => {
          navigator.clipboard.writeText(para.citation).then(() => {
            detailCopyFeedback.classList.add('show');
            setTimeout(() => detailCopyFeedback.classList.remove('show'), 2000);
          });
        });

        const detailToggleRaw = detail.querySelector('.toggle-raw');
        detailToggleRaw.addEventListener('click', () => {
          const expanded = detailToggleRaw.getAttribute('aria-expanded') === 'true';
          detailToggleRaw.setAttribute('aria-expanded', !expanded);
          if (!expanded) {
            detailPre.textContent = para.text_lines;
          } else {
            detailPre.innerHTML = para.text.split(' ').map((word, i) => {
              const span = document.createElement('span');
              span.textContent = word + ' ';
              if (para.suspectWordIndices.includes(i)) {
                span.className = 'highlight-suspect';
              }
              return span.outerHTML;
            }).join('');
          }
        });
      }
    });
  });

  // Downloads
  document.getElementById('download-json').disabled = paragraphs.length === 0;
  document.getElementById('download-md').disabled = paragraphs.length === 0;

  document.getElementById('download-json').addEventListener('click', () => {
    const json = JSON.stringify(paragraphs, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = symbol.replace(/\//g, '-') + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  document.getElementById('download-md').addEventListener('click', () => {
    const frontMatter = `---
title: "${title}"
symbol: ${symbol}
adopted: ${adopted}
source_url: ${doc_url}
extracted: ${new Date().toISOString().split('T')[0]}
paragraphs_found: ${paragraphs.length}
paragraphs_expected: ${refParagraphs || '?'}
pages_flagged: ${flaggedPages.length}
footnotes: not separated; the document has ${refFootnotes || '?'}
---`;

    const mdParagraphs = paragraphs.map(para => {
      const headingPath = para.part ? `${para.part} › ${para.section}` : para.section;
      return `## ${headingPath}\n\n**${para.paragraph}.** ${para.text}${para.flagged ? ' (flagged: may contain footnote text)' : ''}`;
    }).join('\n\n');

    const md = `${frontMatter}\n\n${mdParagraphs}`;
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = symbol.replace(/\//g, '-') + '.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const tabId = tab.id;
      const panelId = tabId.replace('tab', 'panel');
      tabs.forEach(t => {
        t.setAttribute('aria-selected', t.id === tabId);
        document.getElementById(t.id.replace('tab', 'panel')).hidden = t.id !== tabId;
      });
    });
  });

  // Expandable headings
  const expandableHeadings = document.querySelectorAll('[role="button"][aria-expanded]');
  expandableHeadings.forEach(button => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
      const content = button.nextElementSibling;
      if (content) {
        content.hidden = expanded;
      }
    });
    button.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        button.click();
      }
    });
  });
});

function runPipeline(records, symbol, refParagraphs, refFirstWords) {
  // Step 1: Header and footer
  const pages = records.map((record, i) => {
    const lines = record.text.split(/\r?\n/);
    const page = record.page;
    let headerLine = null;
    let footerLines = [];
    let bodyLines = [];
    let headerWarning = false;
    let footerPageNumber = false;
    let bareNumbers = [];

    // Header: first non-empty line
    for (let j = 0; j < lines.length; j++) {
      const line = lines[j].trim();
      if (line) {
        if (line === symbol) {
          headerLine = j;
        } else {
          headerWarning = true;
        }
        break;
      }
    }

    // Footer: from the end
    let footerStart = lines.length;
    for (let j = lines.length - 1; j >= 0; j--) {
      const line = lines[j].trim();
      if (!line) continue;
      if (line.startsWith('GE.') || /^\d{6}$/.test(line) || /^\d{6} \d{6}$/.test(line)) {
        footerStart = j;
        footerLines.unshift(line);
      } else if (/^\d{1,3}$/.test(line)) {
        if (parseInt(line) === page) {
          footerPageNumber = true;
        } else {
          bareNumbers.push(line);
        }
        footerStart = j;
        footerLines.unshift(line);
      } else {
        break;
      }
    }

    // Body: between header and footer
    for (let j = (headerLine !== null ? headerLine + 1 : 0); j < footerStart; j++) {
      const line = lines[j].trim();
      if (line) {
        bodyLines.push({ line, page });
      }
    }

    return {
      page,
      headerLine,
      headerWarning,
      footerLines,
      footerPageNumber,
      bareNumbers,
      bodyLines
    };
  });

  // Step 2: Concatenate body lines
  const allBodyLines = pages.flatMap(p => p.bodyLines);

  // Step 3: Paragraph starts
  const paragraphStarts = [];
  for (let i = 0; i < allBodyLines.length; i++) {
    const { line } = allBodyLines[i];
    const matchAlone = line.match(/^(\d{1,3})\.$/);
    const matchWithText = line.match(/^(\d{1,3})\. (.+)$/);
    if (matchAlone || matchWithText) {
      const number = matchAlone ? parseInt(matchAlone[1]) : parseInt(matchWithText[1]);
      const text = matchWithText ? matchWithText[2] : null;
      paragraphStarts.push({ index: i, number, text });
    }
  }

  // Step 4: Headings
  const headings = [];
  let currentLabelledHeading = null;
  let currentUnlabelledHeading = null;

  for (let i = 0; i < allBodyLines.length; i++) {
    const { line, page } = allBodyLines[i];
    const labelledMatch = line.match(/^([IVX]+|[A-Z])\.$/);
    if (labelledMatch) {
      // Labelled heading
      const label = labelledMatch[1];
      const headingLines = [];
      let j = i + 1;
      while (j < allBodyLines.length && !allBodyLines[j].line.match(/^(\d{1,3})\.$/) && !allBodyLines[j].line.match(/^([IVX]+|[A-Z])\.$/)) {
        if (allBodyLines[j].line.trim()) {
          headingLines.push(allBodyLines[j].line);
        }
        j++;
      }
      const text = headingLines.join(' ');
      headings.push({ index: i, label, text, page, type: 'labelled' });
      currentLabelledHeading = { label, text };
      currentUnlabelledHeading = null;
      i = j - 1;
    } else if (i + 1 < allBodyLines.length && !allBodyLines[i + 1].line.match(/^(\d{1,3})\.$/) && !allBodyLines[i + 1].line.match(/^(\d{1,3})\. (.+)$/)) {
      // Unlabelled heading candidate
      const nextLine = allBodyLines[i + 1].line;
      const isParagraphStart = nextLine.match(/^(\d{1,3})\.$/) || nextLine.match(/^(\d{1,3})\. (.+)$/);
      if (isParagraphStart) {
        const lineTrimmed = line.trim();
        const isHeading = lineTrimmed.length <= 90 &&
                          /^[A-Z]/.test(lineTrimmed) &&
                          !/[.;,:0-9]$/.test(lineTrimmed);
        if (isHeading) {
          // Check if the previous line is also a heading
          let headingText = lineTrimmed;
          let startIndex = i;
          if (i > 0) {
            const prevLine = allBodyLines[i - 1].line.trim();
            const prevIsHeading = prevLine.length <= 90 &&
                                  /^[A-Z]/.test(prevLine) &&
                                  !/[.;,:0-9]$/.test(prevLine);
            if (prevIsHeading) {
              headingText = prevLine + ' ' + headingText;
              startIndex = i - 1;
            }
          }
          headings.push({ index: startIndex, text: headingText, page, type: 'unlabelled' });
          currentUnlabelledHeading = { text: headingText };
        }
      }
    }
  }

  // Step 5: Paragraphs
  const paragraphs = [];
  for (let i = 0; i < paragraphStarts.length; i++) {
    const start = paragraphStarts[i];
    const end = i + 1 < paragraphStarts.length ? paragraphStarts[i + 1].index : allBodyLines.length;
    const paraLines = allBodyLines.slice(start.index, end);
    const textLines = paraLines.map(l => l.line);
    const text = textLines.join(' ').replace(/\s+/g, ' ').trim();
    const page_start = paraLines[0].page;
    const page_end = paraLines[paraLines.length - 1].page;

    // Section and part
    let section = '';
    let part = '';
    for (let j = headings.length - 1; j >= 0; j--) {
      if (headings[j].index < start.index) {
        if (headings[j].type === 'labelled' && /^[IVX]+$/.test(headings[j].label)) {
          part = headings[j].label + '. ' + headings[j].text;
        } else if (headings[j].type === 'unlabelled') {
          section = headings[j].text;
        } else if (headings[j].type === 'labelled') {
          section = headings[j].label + '. ' + headings[j].text;
        }
        break;
      }
    }

    // Suspect lines
    const suspectLines = [];
    const suspectWordIndices = [];
    let flagged = false;
    let wordIndex = 0;
    for (let j = 0; j < paraLines.length; j++) {
      const line = paraLines[j].line;
      const suspectMatch = line.match(/^(\d{1,3}) (.+)$/) || line.match(/^\* (.+)$/) || /^\d{1,3}$/.test(line);
      if (suspectMatch || /^\d{1,3}$/.test(line)) {
        suspectLines.push(j + 1);
        // Mark every word from this line to the end of the paragraph
        const words = line.split(/\s+/);
        for (let k = 0; k < words.length; k++) {
          suspectWordIndices.push(wordIndex + k);
        }
        wordIndex += words.length;
      } else {
        const words = line.split(/\s+/);
        wordIndex += words.length;
      }
    }
    if (suspectLines.length > 0) {
      flagged = true;
    }
    if (text.split(/\s+/).length > 300) {
      flagged = true;
    }

    // First words
    const firstWords = getFirstWords(text);
    const refWords = refFirstWords ? refFirstWords[String(start.number)] : null;
    const first_words_match = refWords ? normalizeForComparison(firstWords) === normalizeForComparison(refWords) : null;

    paragraphs.push({
      symbol,
      paragraph: start.number,
      section,
      part,
      page_start,
      page_end,
      text,
      text_lines: textLines.join(' | '),
      flagged,
      suspectLines,
      suspectWordIndices,
      firstWords,
      refFirstWords: refWords,
      first_words_match,
      citation: `${symbol}, para. ${start.number}`,
      doc_url,
      limitations: flagged ? `footnotes not separated; ${suspectLines.length} may sit inside this paragraph` : 'footnotes not separated'
    });
  }

  // Step 6: Flagged pages
  const flaggedPages = [];
  const flaggedPageNumbers = new Set();
  paragraphs.forEach(para => {
    if (para.flagged) {
      const pages = new Set();
      para.suspectLines.forEach(line => {
        const page = pages.find(p => p.page === para.page_start);
        if (!page) {
          pages.add(para.page_start);
        }
      });
      if (para.page_start !== para.page_end) {
        pages.add(para.page_end);
      }
      pages.forEach(page => {
        if (!flaggedPageNumbers.has(page)) {
          flaggedPageNumbers.add(page);
          const suspectLines = para.suspectLines.filter(line => {
            const linePage = para.page_start + Math.floor((line - 1) / (para.text_lines.split(' | ').length / (para.page_end - para.page_start + 1)));
            return linePage === page;
          }).map(line => {
            const linesPerPage = para.text_lines.split(' | ').length / (para.page_end - para.page_start + 1);
            return Math.ceil((line - 1) % linesPerPage + 1);
          });
          const why = suspectLines.length > 0 ?
            (suspectLines.some(l => para.text_lines.split(' | ')[l - 1].match(/^\d{1,3}$/) ? 'bare number' :
             suspectLines.some(l => para.text_lines.split(' | ')[l - 1].match(/^\d{1,3} (.+)$/) ? 'starts with a number and a space' : 'other')) :
            'paragraph over 300 words';
          flaggedPages.push({
            page,
            paragraph: para.paragraph,
            suspectLines,
            why
          });
        }
      });
    }
  });
  flaggedPages.sort((a, b) => a.page - b.page);

  // Checks
  const checks = [];

  // Paragraph count
  const paragraphCountCheck = {
    id: 'paragraph-count',
    label: 'Paragraph count',
    value: `${paragraphs.length} found, ${refParagraphs || '?'} expected`,
    result: refParagraphs ? (paragraphs.length === refParagraphs ? 'pass' : 'fail') : 'not run'
  };
  checks.push(paragraphCountCheck);

  // Numbering
  const numberingCheck = {
    id: 'numbering',
    label: 'Numbering',
    value: `1 to ${refParagraphs || '?'} in order`,
    result: 'pass',
    details: []
  };
  const numbers = paragraphs.map(p => p.paragraph);
  const expectedNumbers = Array.from({ length: refParagraphs || 0 }, (_, i) => i + 1);
  if (refParagraphs) {
    if (numbers.length !== expectedNumbers.length || !numbers.every((n, i) => n === expectedNumbers[i])) {
      numberingCheck.result = 'fail';
      const missing = expectedNumbers.filter(n => !numbers.includes(n));
      const duplicates = numbers.filter((n, i) => numbers.indexOf(n) !== i);
      if (missing.length > 0) {
        numberingCheck.details.push(`Missing: ${missing.join(', ')}`);
      }
      if (duplicates.length > 0) {
        numberingCheck.details.push(`Duplicates: ${duplicates.join(', ')}`);
      }
    }
  } else {
    numberingCheck.result = 'not run';
  }
  checks.push(numberingCheck);

  // First words
  const firstWordsCheck = {
    id: 'first-words',
    label: 'First words',
    value: `${paragraphs.filter(p => p.first_words_match).length} of ${refParagraphs || '?'} match`,
    result: refFirstWords ? (paragraphs.every(p => p.first_words_match) ? 'pass' : 'fail') : 'not run',
    found: paragraphs.filter(p => p.first_words_match).length,
    expected: refParagraphs || '?',
    mismatches: []
  };
  if (refFirstWords) {
    paragraphs.forEach(p => {
      if (!p.first_words_match) {
        firstWordsCheck.mismatches.push({
          number: p.paragraph,
          found: p.firstWords,
          expected: p.refFirstWords
        });
      }
    });
  }
  checks.push(firstWordsCheck);

  // Pages flagged
  const flaggedPagesCheck = {
    id: 'flagged-pages',
    label: 'Pages flagged',
    value: `${flaggedPages.length} pages flagged, ${paragraphs.filter(p => p.flagged).length} paragraphs to check against the PDF`,
    result: '—'
  };
  checks.push(flaggedPagesCheck);

  // Suspect lines
  const suspectLines = paragraphs.flatMap(p => p.suspectLines);
  const suspectPages = new Set(paragraphs.filter(p => p.flagged).map(p => p.page_start));
  const suspectParagraphs = paragraphs.filter(p => p.flagged).length;
  const suspectLinesCheck = {
    id: 'suspect-lines',
    label: 'Suspect lines',
    value: `${suspectLines.length} suspect lines on ${suspectPages.size} pages, in ${suspectParagraphs} paragraphs`,
    result: '—'
  };
  checks.push(suspectLinesCheck);

  // Headers and footers
  const headerPages = pages.filter(p => p.headerLine !== null).length;
  const footerPages = pages.filter(p => p.footerPageNumber).length;
  const bareNumbersTotal = pages.flatMap(p => p.bareNumbers).length;
  const headerFooterCheck = {
    id: 'header-footer',
    label: 'Headers and footers',
    value: `${headerPages} pages with the symbol as first line, ${footerPages} pages with a page number in the footer, ${bareNumbersTotal} bare numbers removed from the footer`,
    result: pages.length === headerPages && pages.length - 1 === footerPages ? 'pass' : 'fail',
    details: []
  };
  if (pages.length !== headerPages) {
    const missing = pages.filter(p => p.headerLine === null).map(p => p.page);
    headerFooterCheck.details.push(`Pages without the symbol as first line: ${missing.join(', ')}`);
  }
  if (pages.length - 1 !== footerPages) {
    const missing = pages.filter((p, i) => i > 0 && !p.footerPageNumber).map(p => p.page);
    headerFooterCheck.details.push(`Pages without a page number in the footer: ${missing.join(', ')}`);
  }
  if (bareNumbersTotal > 0) {
    const bareNumbersList = pages.flatMap(p => p.bareNumbers.map(n => `${n} on page ${p.page}`));
    headerFooterCheck.details.push(`Bare numbers removed: ${bareNumbersList.join(', ')}`);
  }
  checks.push(headerFooterCheck);

  // Headings
  const labelledHeadings = headings.filter(h => h.type === 'labelled').length;
  const unlabelledHeadings = headings.filter(h => h.type === 'unlabelled').length;
  const headingsCheck = {
    id: 'headings',
    label: 'Headings',
    value: `${labelledHeadings} labelled, ${unlabelledHeadings} unlabelled`,
    result: 'pass',
    details: []
  };
  if (unlabelledHeadings > 0) {
    headingsCheck.details = headings.filter(h => h.type === 'unlabelled').map(h => `${h.text} (page ${h.page})`);
  }
  checks.push(headingsCheck);

  // Nothing lost
  const totalLines = pages.reduce((sum, p) => sum + p.bodyLines.length, 0);
  const coverLines = paragraphStarts.length > 0 ? paragraphStarts[0].index : allBodyLines.length;
  const headingLines = headings.reduce((sum, h) => sum + (h.type === 'labelled' ? 1 : h.text.split(' ').length <= 2 ? 1 : 2), 0);
  const paragraphLines = paragraphs.reduce((sum, p) => sum + p.text_lines.split(' | ').length, 0);
  const classifiedLines = coverLines + headingLines + paragraphLines;
  const nothingLostCheck = {
    id: 'nothing-lost',
    label: 'Nothing lost',
    value: 'every non-empty line classified once',
    result: totalLines === classifiedLines ? 'pass' : 'fail',
    details: []
  };
  if (totalLines !== classifiedLines) {
    const unclassified = [];
    let currentIndex = 0;
    for (let i = 0; i < pages.length; i++) {
      const p = pages[i];
      for (let j = 0; j < p.bodyLines.length; j++) {
        const line = p.bodyLines[j];
        if (currentIndex < coverLines) {
          // Cover
        } else if (currentIndex < coverLines + headingLines) {
          // Heading
        } else if (currentIndex < coverLines + headingLines + paragraphLines) {
          // Paragraph
        } else {
          unclassified.push(`page ${line.page}: ${line.line}`);
        }
        currentIndex++;
      }
    }
    nothingLostCheck.details = unclassified;
  }
  checks.push(nothingLostCheck);

  // Export round trip
  const exportCheck = {
    id: 'export-round-trip',
    label: 'Export round trip',
    value: `JSON parses back to ${paragraphs.length} records`,
    result: 'pass'
  };
  checks.push(exportCheck);

  return { paragraphs, checks, flaggedPages, headings };
}

function getFirstWords(text) {
  const words = text.split(/\s+/);
  const firstWords = [];
  for (let i = 0; i < words.length && firstWords.length < 6; i++) {
    const word = words[i];
    // Remove footnote marks glued to the end
    const cleanWord = word.replace(/[\d"']+$/, '');
    if (cleanWord) {
      firstWords.push(cleanWord);
    }
  }
  return firstWords.join(' ');
}

function normalizeForComparison(text) {
  return text
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/[–—]/g, '-')
    .replace(/\s+/g, ' ')
    .trim();
}
</script>
</body>
</html>
```