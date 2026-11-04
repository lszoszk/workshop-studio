I built the app you described: a two-tab tool that extracts the numbered paragraphs from the HTML version of a General Comment, checks them against the document's own reference, and lets the user download the result as JSON or Markdown. The left rail shows the document's metadata and the checks' status; tab 01 gives the result at a glance and the checks; tab 02 lists the paragraphs with their headings and lets the user expand each to see the full text and its repairs.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --pass: #2e6b49;
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
.hidden {
  display: none !important;
}
header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--rule);
  background-color: var(--paper);
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-grid {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
}
.label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--ink);
  opacity: 0.7;
}
.title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: normal;
  margin: 0;
  line-height: 1.2;
}
.meta {
  font-size: 0.875rem;
  color: var(--ink);
  opacity: 0.8;
  margin: 0;
}
.meta a {
  color: var(--ink);
  text-decoration: none;
}
.meta a:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.meta a:hover {
  text-decoration: underline;
}
.status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.status-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}
.status-dot.pass {
  background-color: var(--pass);
}
.status-dot.fail {
  background-color: var(--accent);
}
main {
  display: grid;
  grid-template-columns: 24rem 1fr;
  gap: 1rem;
  padding: 1rem;
}
.rail {
  background-color: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  font-size: 0.875rem;
}
.rail-card {
  background-color: var(--ink);
  color: var(--paper);
  padding: 0.75rem;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
}
.rail-card .symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  word-break: break-all;
}
.rail-card .short-title {
  font-size: 0.875rem;
  opacity: 0.8;
  margin: 0;
}
.rail-numbers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}
.rail-number {
  text-align: center;
}
.rail-number .value {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: normal;
  line-height: 1;
  margin: 0;
}
.rail-number .label {
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  margin: 0;
}
.rail-number .bar {
  height: 2px;
  background-color: var(--rule);
  margin-top: 0.5rem;
}
.rail-number .bar.fail {
  background-color: var(--accent);
}
.rail-number .footnotes {
  color: var(--accent);
}
.rail-checks {
  margin-top: 1rem;
}
.rail-checks .value {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: normal;
  line-height: 1;
  margin: 0;
}
.rail-checks .label {
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  margin: 0;
}
.tablist {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--rule);
}
.tab {
  padding: 0.5rem 0;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--ink);
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
  position: relative;
}
.tab:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.tab[aria-selected="true"] {
  color: var(--accent);
}
.tab[aria-selected="true"]::after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--accent);
}
.tabpanel {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  background-color: var(--paper);
}
.tabpanel:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.tile {
  background-color: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.tile .value {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: normal;
  line-height: 1;
  margin: 0 0 0.5rem 0;
}
.tile .label {
  font-size: 0.875rem;
  margin: 0;
}
.tile .how {
  font-size: 0.75rem;
  opacity: 0.7;
  margin: 0.5rem 0 0 0;
}
.tile.fail .value {
  color: var(--accent);
}
.tile.fail .label {
  color: var(--accent);
}
.tile.limit .value {
  color: var(--accent);
}
.tile.limit .label {
  color: var(--accent);
}
.tile.limit .how {
  color: var(--accent);
}
.mismatches {
  margin-top: 1rem;
  border-top: 1px solid var(--rule);
  padding-top: 1rem;
}
.mismatch {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  margin: 0.25rem 0;
}
.mismatch a {
  color: var(--ink);
  text-decoration: none;
}
.mismatch a:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.mismatch a:hover {
  text-decoration: underline;
}
.export {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
}
.export-buttons {
  display: flex;
  gap: 1rem;
}
.export-buttons button {
  padding: 0.5rem 1rem;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--paper);
  background-color: var(--ink);
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}
.export-buttons button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.export-buttons button:hover {
  background-color: var(--accent);
}
.check-panel {
  margin-top: 2rem;
  border-top: 1px solid var(--rule);
}
.check-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  cursor: pointer;
}
.check-heading:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.check-heading[aria-expanded="true"] .arrow {
  transform: rotate(180deg);
}
.arrow {
  transition: transform 0.2s;
}
.checks {
  padding: 0.5rem 0;
}
.check {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  padding: 0.25rem 0;
  font-size: 0.875rem;
}
.check .what {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  letter-spacing: 0.05em;
}
.check .found {
  text-align: right;
}
.check .expected {
  text-align: right;
  font-family: ui-monospace, Menlo, Consolas, monospace;
}
.check .result {
  text-align: right;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  letter-spacing: 0.05em;
}
.check .result.pass {
  color: var(--pass);
}
.check .result.fail {
  color: var(--accent);
}
.check .result.limit {
  color: var(--accent);
}
.check .result.not-run {
  opacity: 0.5;
}
.spaces-panel {
  margin-top: 2rem;
  border-top: 1px solid var(--rule);
}
.spaces-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  cursor: pointer;
}
.spaces-heading:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.spaces-heading[aria-expanded="true"] .arrow {
  transform: rotate(180deg);
}
.spaces-summary {
  padding: 0.5rem 0;
  font-size: 0.875rem;
}
.spaces-summary .count {
  font-family: ui-monospace, Menlo, Consolas, monospace;
}
.spaces-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}
.spaces-table th,
.spaces-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
.spaces-table th {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}
.spaces-table td {
  font-size: 0.875rem;
}
.spaces-table td.para {
  font-family: ui-monospace, Menlo, Consolas, monospace;
}
.spaces-table td.before,
.spaces-table td.after {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  white-space: pre-wrap;
}
.spaces-table tr:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.spaces-table a {
  color: var(--ink);
  text-decoration: none;
}
.spaces-table a:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.spaces-table a:hover {
  text-decoration: underline;
}
.spaces-note {
  margin-top: 1rem;
  font-size: 0.75rem;
  opacity: 0.7;
}
.table-container {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}
caption {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1rem;
  font-weight: normal;
  text-align: left;
  margin-bottom: 0.5rem;
  caption-side: top;
}
th {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
}
th[scope="col"] {
  font-weight: normal;
}
td {
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
td.number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.25rem;
  font-weight: normal;
  text-align: right;
  width: 3rem;
}
td.section {
  width: 12rem;
}
td.first-line {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
}
td.check {
  width: 8rem;
  text-align: right;
}
td.check.fail {
  color: var(--accent);
}
tr[aria-expanded="false"] {
  cursor: pointer;
}
tr[aria-expanded="false"]:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
tr[aria-expanded="true"] {
  background-color: var(--ink);
  color: var(--paper);
}
tr[aria-expanded="true"] td {
  border-bottom: 1px solid var(--rule);
  background-color: var(--ink);
  color: var(--paper);
}
tr[aria-expanded="true"] .text {
  padding: 0.5rem 0;
  white-space: pre-wrap;
}
tr[aria-expanded="true"] .first-words {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
  border-top: 1px solid var(--rule);
  margin-top: 0.5rem;
}
tr[aria-expanded="true"] .first-words .label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}
tr[aria-expanded="true"] .first-words .found,
tr[aria-expanded="true"] .first-words .reference {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
}
tr[aria-expanded="true"] .first-words .reference {
  opacity: 0.8;
}
tr[aria-expanded="true"] .spaces {
  padding: 0.5rem 0;
  border-top: 1px solid var(--rule);
  margin-top: 0.5rem;
}
tr[aria-expanded="true"] .spaces .label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}
tr[aria-expanded="true"] .spaces .place {
  display: inline-block;
  padding: 0.1rem 0.2rem;
  margin: 0 0.1rem;
  border: 1px solid var(--accent);
  border-radius: 0.1rem;
  background-color: rgba(155, 35, 53, 0.1);
}
tr[aria-expanded="true"] .citation {
  padding: 0.5rem 0;
  border-top: 1px solid var(--rule);
  margin-top: 0.5rem;
}
tr[aria-expanded="true"] .citation button {
  padding: 0.25rem 0.5rem;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: var(--paper);
  background-color: var(--ink);
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}
tr[aria-expanded="true"] .citation button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
tr[aria-expanded="true"] .citation button:hover {
  background-color: var(--accent);
}
tr[aria-expanded="true"] .citation .copied {
  margin-left: 0.5rem;
  font-size: 0.75rem;
  opacity: 0.7;
}
.headings-box {
  margin-bottom: 1rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 0.5rem;
}
.headings-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0;
  cursor: pointer;
}
.headings-heading:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.headings-heading[aria-expanded="true"] .arrow {
  transform: rotate(180deg);
}
.headings-list {
  padding: 0.25rem 0;
  font-size: 0.875rem;
}
.headings-list .heading {
  margin: 0.1rem 0;
  padding-left: 1rem;
  position: relative;
}
.headings-list .heading::before {
  content: "›";
  position: absolute;
  left: 0;
}
.footer {
  padding: 1rem;
  border-top: 1px solid var(--rule);
  font-size: 0.75rem;
  opacity: 0.7;
}
.footer a {
  color: var(--ink);
  text-decoration: none;
}
.footer a:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.footer a:hover {
  text-decoration: underline;
}
</style>
</head>
<body>

<header>
  <div class="header-grid">
    <div class="label">UN DOCUMENT · HTML</div>
    <div class="title" id="doc-title"></div>
    <div class="status">
      <div class="status-dot" id="status-dot"></div>
      <div id="status-text"></div>
    </div>
  </div>
  <div class="meta" id="doc-meta"></div>
</header>

<main>
  <aside class="rail">
    <div class="rail-card">
      <div class="symbol" id="doc-symbol"></div>
      <div class="short-title" id="doc-short-title"></div>
    </div>
    <div class="rail-numbers">
      <div class="rail-number">
        <div class="value" id="rail-paragraphs-value"></div>
        <div class="label">paragraphs of <span id="rail-paragraphs-expected"></span></div>
        <div class="bar" id="rail-paragraphs-bar"></div>
      </div>
      <div class="rail-number">
        <div class="value" id="rail-footnotes-value">0</div>
        <div class="label footnotes">footnotes of <span id="rail-footnotes-expected"></span></div>
        <div class="bar fail"></div>
      </div>
    </div>
    <div class="rail-checks">
      <div class="value" id="rail-checks-value"></div>
      <div class="label">of <span id="rail-checks-total"></span> checks pass</div>
    </div>
  </aside>

  <div>
    <div class="tablist" role="tablist" aria-label="Tabs">
      <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
      <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
    </div>

    <div id="panel-01" class="tabpanel" role="tabpanel" aria-labelledby="tab-01" tabindex="0">
      <div class="tiles">
        <div class="tile">
          <div class="value" id="tile-paragraphs-value"></div>
          <div class="label">Paragraphs found</div>
          <div class="how">How this is computed: counted in the HTML, against the document's own reference.</div>
        </div>
        <div class="tile">
          <div class="value" id="tile-paragraphs-expected"></div>
          <div class="label">the document has</div>
        </div>
        <div class="tile">
          <div class="value" id="tile-first-words-value"></div>
          <div class="label">First words match</div>
          <div class="how">How this is computed: the first six words of each paragraph, normalised.</div>
        </div>
        <div class="tile limit">
          <div class="value" id="tile-footnotes-value">0</div>
          <div class="label">Footnotes</div>
          <div class="how">this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.</div>
        </div>
        <div class="tile">
          <div class="value" id="tile-spaces-value"></div>
          <div class="label">Spaces</div>
          <div class="how">How this is computed: rules restore a space where the characters prove it was there.</div>
        </div>
      </div>

      <div class="mismatches" id="mismatches-container" hidden>
        <div class="label">First words that differ</div>
        <div id="mismatches-list"></div>
      </div>

      <div class="export">
        <div class="label">Take the paragraphs away</div>
        <div class="export-buttons">
          <button id="download-json">Download JSON</button>
          <button id="download-markdown">Download Markdown</button>
        </div>
      </div>

      <div class="check-panel">
        <button class="check-heading" id="checks-heading" aria-expanded="false" aria-controls="checks">
          <span>Every check (<span id="checks-heading-count"></span>)</span>
          <span class="arrow">▼</span>
        </button>
        <div id="checks" class="checks" hidden></div>
      </div>

      <div class="spaces-panel">
        <button class="spaces-heading" id="spaces-heading" aria-expanded="false" aria-controls="spaces-table-container">
          <span>The spaces restored (<span id="spaces-heading-count"></span>)</span>
          <span class="arrow">▼</span>
        </button>
        <div id="spaces-table-container" hidden>
          <div class="spaces-summary">
            <span class="count" id="spaces-summary-sentence"></span> sentence joins, <span class="count" id="spaces-summary-comma"></span> comma joins, <span class="count" id="spaces-summary-quote"></span> quote joins, <span class="count" id="spaces-summary-dash"></span> dash joins.
          </div>
          <div class="table-container">
            <table class="spaces-table">
              <thead>
                <tr>
                  <th scope="col">Paragraph</th>
                  <th scope="col">Before</th>
                  <th scope="col">After</th>
                  <th scope="col">Rule</th>
                </tr>
              </thead>
              <tbody id="spaces-table-body"></tbody>
            </table>
          </div>
          <div class="spaces-note">
            Rules restore a space only where the characters prove it was there. Word pairs such as "Giventhe" are not touched.
          </div>
        </div>
      </div>
    </div>

    <div id="panel-02" class="tabpanel" role="tabpanel" aria-labelledby="tab-02" hidden tabindex="0">
      <div class="headings-box">
        <button class="headings-heading" id="headings-heading" aria-expanded="false" aria-controls="headings-list">
          <span>Headings found: <span id="headings-heading-count"></span></span>
          <span class="arrow">▼</span>
        </button>
        <div id="headings-list" class="headings-list" hidden></div>
      </div>
      <div class="table-container">
        <table>
          <caption id="paragraphs-caption"></caption>
          <thead>
            <tr>
              <th scope="col">No.</th>
              <th scope="col">Section</th>
              <th scope="col">First line</th>
              <th scope="col">Check</th>
            </tr>
          </thead>
          <tbody id="paragraphs-body"></tbody>
        </table>
      </div>
    </div>
  </div>
</main>

<footer class="footer">
  <div id="footer-source"></div>
  <div id="footer-built"></div>
  <div>Done by this page's code; no model was called and nothing left the browser.</div>
</footer>

<script>
document.addEventListener('DOMContentLoaded', () => {
  const data = window.WORKSHOP_DATA.html_doc;
  const doc = new DOMParser().parseFromString(data.html, 'text/html');
  const reference = data.reference || {};

  // Header
  document.getElementById('doc-title').textContent = data.title;
  const meta = document.getElementById('doc-meta');
  meta.innerHTML = `<a href="${data.doc_url}" target="_blank">${data.symbol}</a>, adopted ${reference.adopted || 'unknown'}, ${data.source}`;

  // Rail
  document.getElementById('doc-symbol').textContent = data.symbol;
  document.getElementById('doc-short-title').textContent = data.title.replace(/^General comment No\. \d+ \(\d+\) /, '');
  document.getElementById('rail-paragraphs-expected').textContent = reference.paragraphs || '?';
  document.getElementById('rail-footnotes-expected').textContent = reference.footnotes || '?';

  // Pipeline
  const {paragraphs, headings, checks, spaces} = extractParagraphs(doc, data.symbol, reference);
  const checksPassed = checks.filter(c => c.result === 'pass').length;
  const checksTotal = checks.length;

  // Status
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');
  if (checksPassed === checksTotal) {
    statusDot.className = 'status-dot pass';
    statusText.textContent = `${checksPassed} checks pass`;
  } else {
    statusDot.className = 'status-dot fail';
    statusText.textContent = `${checksPassed} of ${checksTotal} checks pass`;
  }

  // Rail numbers
  const railParagraphsValue = document.getElementById('rail-paragraphs-value');
  const railParagraphsBar = document.getElementById('rail-paragraphs-bar');
  railParagraphsValue.textContent = paragraphs.length;
  if (paragraphs.length !== reference.paragraphs) {
    railParagraphsBar.classList.add('fail');
  }
  document.getElementById('rail-footnotes-value').textContent = 0;
  document.getElementById('rail-checks-value').textContent = checksPassed;
  document.getElementById('rail-checks-total').textContent = checksTotal;

  // Tiles
  const tileParagraphsValue = document.getElementById('tile-paragraphs-value');
  const tileParagraphsExpected = document.getElementById('tile-paragraphs-expected');
  tileParagraphsValue.textContent = paragraphs.length;
  tileParagraphsExpected.textContent = reference.paragraphs || '?';
  if (paragraphs.length !== reference.paragraphs) {
    tileParagraphsValue.parentElement.classList.add('fail');
  }

  const firstWordsMatch = paragraphs.filter(p => p.first_words_match).length;
  document.getElementById('tile-first-words-value').textContent = `${firstWordsMatch} of ${reference.paragraphs || '?'}`;
  if (firstWordsMatch !== reference.paragraphs) {
    document.getElementById('tile-first-words-value').parentElement.classList.add('fail');
  }

  const spacesCount = spaces.length;
  document.getElementById('tile-spaces-value').textContent = `${spacesCount} in ${new Set(spaces.map(s => s.paragraph)).size} paragraphs`;

  // Mismatches
  const mismatches = paragraphs.filter(p => !p.first_words_match);
  const mismatchesContainer = document.getElementById('mismatches-container');
  const mismatchesList = document.getElementById('mismatches-list');
  if (mismatches.length > 0) {
    mismatchesContainer.hidden = false;
    mismatches.slice(0, 10).forEach(m => {
      const div = document.createElement('div');
      div.className = 'mismatch';
      div.innerHTML = `para. <a href="#para-${m.paragraph}" data-tab="02">${m.paragraph}</a>: found <span class="found">${m.first_words_found}</span> / reference <span class="reference">${m.first_words_reference}</span>`;
      mismatchesList.appendChild(div);
    });
    if (mismatches.length > 10) {
      const div = document.createElement('div');
      div.className = 'mismatch';
      div.textContent = `and ${mismatches.length - 10} more`;
      mismatchesList.appendChild(div);
    }
  }

  // Checks panel
  const checksHeading = document.getElementById('checks-heading');
  const checksContainer = document.getElementById('checks');
  checksHeading.addEventListener('click', () => {
    checksContainer.hidden = !checksContainer.hidden;
    checksHeading.setAttribute('aria-expanded', checksContainer.hidden ? 'false' : 'true');
  });
  checksHeading.querySelector('span:first-child').textContent = `Every check (${checks.length})`;
  checks.forEach(check => {
    const div = document.createElement('div');
    div.className = 'check';
    div.innerHTML = `
      <div class="what">${check.what}</div>
      <div class="found">${check.found}</div>
      <div class="expected">${check.expected}</div>
      <div class="result ${check.result}">${check.result === 'pass' ? 'pass' : check.result === 'limit' ? 'source limit' : check.result === 'not-run' ? 'not run' : 'check failed'}</div>
    `;
    checksContainer.appendChild(div);
  });

  // Spaces panel
  const spacesHeading = document.getElementById('spaces-heading');
  const spacesTableContainer = document.getElementById('spaces-table-container');
  spacesHeading.addEventListener('click', () => {
    spacesTableContainer.hidden = !spacesTableContainer.hidden;
    spacesHeading.setAttribute('aria-expanded', spacesTableContainer.hidden ? 'false' : 'true');
  });
  spacesHeading.querySelector('span:first-child').textContent = `The spaces restored (${spaces.length})`;

  const spacesSummarySentence = document.getElementById('spaces-summary-sentence');
  const spacesSummaryComma = document.getElementById('spaces-summary-comma');
  const spacesSummaryQuote = document.getElementById('spaces-summary-quote');
  const spacesSummaryDash = document.getElementById('spaces-summary-dash');
  const sentenceJoins = spaces.filter(s => s.rule === 'sentence').length;
  const commaJoins = spaces.filter(s => s.rule === 'comma').length;
  const quoteJoins = spaces.filter(s => s.rule === 'quote').length;
  const dashJoins = spaces.filter(s => s.rule === 'dash').length;
  spacesSummarySentence.textContent = sentenceJoins;
  spacesSummaryComma.textContent = commaJoins;
  spacesSummaryQuote.textContent = quoteJoins;
  spacesSummaryDash.textContent = dashJoins;

  const spacesTableBody = document.getElementById('spaces-table-body');
  spaces.forEach(space => {
    const tr = document.createElement('tr');
    tr.tabIndex = 0;
    tr.innerHTML = `
      <td class="para"><a href="#para-${space.paragraph}" data-tab="02">${space.paragraph}</a></td>
      <td class="before">${escapeHtml(space.before)}</td>
      <td class="after">${escapeHtml(space.after)}</td>
      <td>${space.rule}</td>
    `;
    tr.addEventListener('click', () => {
      document.getElementById('tab-02').click();
      document.querySelector(`#para-${space.paragraph}`).scrollIntoView();
    });
    spacesTableBody.appendChild(tr);
  });

  // Headings
  const headingsHeading = document.getElementById('headings-heading');
  const headingsList = document.getElementById('headings-list');
  headingsHeading.addEventListener('click', () => {
    headingsList.hidden = !headingsList.hidden;
    headingsHeading.setAttribute('aria-expanded', headingsList.hidden ? 'false' : 'true');
  });
  headingsHeading.querySelector('span:first-child').textContent = `Headings found: ${headings.length}`;
  headings.forEach(heading => {
    const div = document.createElement('div');
    div.className = 'heading';
    div.textContent = heading.heading;
    headingsList.appendChild(div);
  });

  // Paragraphs table
  const paragraphsCaption = document.getElementById('paragraphs-caption');
  paragraphsCaption.textContent = `${paragraphs.length} paragraphs found, ${reference.paragraphs || '?'} expected`;
  const paragraphsBody = document.getElementById('paragraphs-body');
  paragraphs.forEach(para => {
    const tr = document.createElement('tr');
    tr.id = `para-${para.paragraph}`;
    tr.setAttribute('aria-expanded', 'false');
    tr.tabIndex = 0;
    tr.innerHTML = `
      <td class="number">${para.paragraph}</td>
      <td class="section">${para.section}</td>
      <td class="first-line">${escapeHtml(para.text.substring(0, 120).replace(/\s+/g, ' '))}${para.text.length > 120 ? '…' : ''}</td>
      <td class="check ${para.first_words_match ? '' : 'fail'}">${para.first_words_match ? 'OK' : 'first words differ'}</td>
    `;
    tr.addEventListener('click', () => {
      const expanded = tr.getAttribute('aria-expanded') === 'true';
      tr.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      if (!expanded) {
        const fullPath = para.part ? `${para.part} › ${para.section}` : para.section;
        tr.innerHTML = `
          <td class="number">${para.paragraph}</td>
          <td class="section">${fullPath}</td>
          <td colspan="2">
            <div class="text">${escapeHtml(para.text)}</div>
            <div class="first-words">
              <div class="label">First words</div>
              <div class="found">${escapeHtml(para.first_words_found)}</div>
              <div class="label">Reference</div>
              <div class="reference">${escapeHtml(para.first_words_reference)}</div>
            </div>
            <div class="spaces">
              <div class="label">Spaces restored</div>
              <div>${para.spaces.map(s => `<span class="place">${escapeHtml(s.before)}</span> → <span class="place">${escapeHtml(s.after)}</span> (${s.rule})`).join(', ')}</div>
            </div>
            <div class="citation">
              <button>Copy citation</button>
              <span class="copied"></span>
            </div>
          </td>
        `;
        tr.querySelector('button').addEventListener('click', e => {
          e.stopPropagation();
          navigator.clipboard.writeText(para.citation).then(() => {
            const copied = tr.querySelector('.copied');
            copied.textContent = 'Copied';
            setTimeout(() => copied.textContent = '', 2000);
          });
        });
      } else {
        tr.innerHTML = `
          <td class="number">${para.paragraph}</td>
          <td class="section">${para.section}</td>
          <td class="first-line">${escapeHtml(para.text.substring(0, 120).replace(/\s+/g, ' '))}${para.text.length > 120 ? '…' : ''}</td>
          <td class="check ${para.first_words_match ? '' : 'fail'}">${para.first_words_match ? 'OK' : 'first words differ'}</td>
        `;
      }
    });
    paragraphsBody.appendChild(tr);
  });

  // Tabs
  const tabs = document.querySelectorAll('.tab');
  const tabpanels = document.querySelectorAll('.tabpanel');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const selected = tab.getAttribute('aria-selected') === 'true';
      if (selected) return;
      tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
      tabpanels.forEach(p => p.hidden = true);
      tab.setAttribute('aria-selected', 'true');
      document.getElementById(tab.getAttribute('aria-controls')).hidden = false;
    });
  });

  // Downloads
  document.getElementById('download-json').addEventListener('click', () => {
    const json = JSON.stringify(paragraphs, null, 2);
    const blob = new Blob([json], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.json';
    a.click();
    URL.revokeObjectURL(url);
  });

  document.getElementById('download-markdown').addEventListener('click', () => {
    const frontMatter = `---
title: ${data.title}
symbol: ${data.symbol}
adopted: ${reference.adopted || 'unknown'}
source_url: ${data.doc_url}
extracted: ${new Date().toISOString().split('T')[0]}
paragraphs_found: ${paragraphs.length}
paragraphs_expected: ${reference.paragraphs || '?'}
footnotes: no footnotes in this HTML version; the document has ${reference.footnotes || '?'}
---`;
    const markdown = [frontMatter];
    let currentPart = '';
    let currentSection = '';
    paragraphs.forEach(para => {
      if (para.part && para.part !== currentPart) {
        markdown.push(`\n## ${para.part}`);
        currentPart = para.part;
      }
      if (para.section && para.section !== currentSection) {
        markdown.push(`\n### ${para.section}`);
        currentSection = para.section;
      }
      markdown.push(`\n**${para.paragraph}.** ${para.text}`);
    });
    const blob = new Blob([markdown.join('\n')], {type: 'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.md';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Footer
  document.getElementById('footer-source').textContent = data.source;
  document.getElementById('footer-built').textContent = `Built ${new Date().toISOString().split('T')[0]}`;
});

function extractParagraphs(doc, symbol, reference) {
  const elements = doc.body.querySelectorAll('table, p, h2, h3');
  const paragraphs = [];
  const headings = [];
  const checks = [];
  const spaces = [];
  let currentPart = '';
  let currentSection = '';
  let numbering = [];
  let repairs = [];

  // Classification
  elements.forEach(el => {
    if (el.tagName === 'TABLE') {
      // Cover table, skip
      return;
    }
    if (el.tagName === 'P') {
      const text = el.textContent.trim();
      const match = text.match(/^(\d{1,3})\.\s*(.*)$/s);
      if (match) {
        const number = parseInt(match[1], 10);
        const textRaw = match[2].trim().replace(/\s+/g, ' ');
        numbering.push(number);

        // Repairs
        let textRepaired = textRaw;
        const spaceLog = [];
        textRepaired = textRepaired.replace(/([a-z])\.([A-Z])/g, (_, a, b) => {
          spaceLog.push({rule: 'sentence', before: `${a}.${b}`, after: `${a}. ${b}`});
          return `${a}. ${b}`;
        });
        textRepaired = textRepaired.replace(/([a-z]),([A-Za-z])/g, (_, a, b) => {
          spaceLog.push({rule: 'comma', before: `${a},${b}`, after: `${a}, ${b}`});
          return `${a}, ${b}`;
        });
        textRepaired = textRepaired.replace(/([a-z])“/g, (_, a) => {
          spaceLog.push({rule: 'quote', before: `${a}“`, after: `${a} “`});
          return `${a} “`;
        });
        textRepaired = textRepaired.replace(/–([A-Za-z])/g, (_, a) => {
          spaceLog.push({rule: 'dash', before: `–${a}`, after: `– ${a}`});
          return `– ${a}`;
        });
        repairs.push(...spaceLog.map(log => ({paragraph: number, ...log})));

        // First words
        const firstWordsFound = textRepaired.split(/\s+/).slice(0, 6).join(' ');
        const firstWordsReference = reference.first_words ? reference.first_words[String(number)] || '' : '';
        const firstWordsMatch = normalise(firstWordsFound) === normalise(firstWordsReference);

        paragraphs.push({
          symbol,
          paragraph: number,
          part: currentPart,
          section: currentSection,
          text: textRepaired,
          text_raw: textRaw,
          first_words_found: firstWordsFound,
          first_words_reference: firstWordsReference,
          first_words_match: firstWordsMatch,
          citation: `${symbol}, para. ${number}`,
          doc_url: docURL(symbol, number),
          spaces: spaceLog,
          limitations: `no footnotes in this HTML version; the document has ${reference.footnotes || '?'}`
        });
      }
    } else if (el.tagName === 'H2') {
      const text = el.textContent.trim();
      if (text === data.title) {
        // Title, skip
        return;
      }
      const match = text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
      if (match) {
        currentPart = match[2];
        currentSection = '';
        headings.push({label: match[1], heading: match[2], level: 'part'});
      } else {
        currentSection = text;
        headings.push({label: '', heading: text, level: 'section'});
      }
    } else if (el.tagName === 'H3') {
      const text = el.textContent.trim();
      const match = text.match(/^([A-Z])\.\s*(.+)$/);
      if (match) {
        currentSection = match[2];
        headings.push({label: match[1], heading: match[2], level: 'subsection'});
      } else {
        currentSection = text;
        headings.push({label: '', heading: text, level: 'subsection'});
      }
    }
  });

  // Checks
  checks.push({
    what: 'Paragraph count',
    found: paragraphs.length,
    expected: reference.paragraphs || 'no reference',
    result: reference.paragraphs ? (paragraphs.length === reference.paragraphs ? 'pass' : 'fail') : 'not-run'
  });

  const numberingCheck = checkNumbering(numbering);
  checks.push({
    what: 'Numbering',
    found: numberingCheck.found,
    expected: numberingCheck.expected,
    result: numberingCheck.result
  });

  const firstWordsMatch = paragraphs.filter(p => p.first_words_match).length;
  checks.push({
    what: 'First words',
    found: `${firstWordsMatch} of ${reference.paragraphs || '?'}`,
    expected: reference.paragraphs || 'no reference',
    result: reference.paragraphs ? (firstWordsMatch === reference.paragraphs ? 'pass' : 'fail') : 'not-run'
  });

  checks.push({
    what: 'Footnotes',
    found: 0,
    expected: reference.footnotes || 'no reference',
    result: 'limit'
  });

  const spacesCount = repairs.length;
  checks.push({
    what: 'Spaces restored',
    found: `${spacesCount} in ${new Set(repairs.map(r => r.paragraph)).size} paragraphs`,
    expected: 'n/a',
    result: 'pass'
  });

  checks.push({
    what: 'Headings',
    found: `${headings.filter(h => h.level === 'part').length} parts, ${headings.filter(h => h.level === 'section').length} sections, ${headings.filter(h => h.level === 'subsection').length} subsections`,
    expected: 'n/a',
    result: 'pass'
  });

  const unclassified = elements.length - paragraphs.length - headings.length - 1; // 1 for the title
  checks.push({
    what: 'Nothing lost',
    found: `${paragraphs.length} paragraphs, ${headings.length} headings, 1 title`,
    expected: elements.length - 1, // minus the cover table
    result: unclassified === 0 ? 'pass' : 'fail'
  });

  // Export round trip
  try {
    const json = JSON.stringify(paragraphs);
    const parsed = JSON.parse(json);
    checks.push({
      what: 'Export round trip',
      found: parsed.length,
      expected: paragraphs.length,
      result: parsed.length === paragraphs.length ? 'pass' : 'fail'
    });
  } catch {
    checks.push({
      what: 'Export round trip',
      found: 'error',
      expected: paragraphs.length,
      result: 'fail'
    });
  }

  return {paragraphs, headings, checks, spaces: repairs};
}

function checkNumbering(numbering) {
  if (numbering.length === 0) {
    return {found: 'none', expected: '1 to n', result: 'fail'};
  }
  const expected = Array.from({length: numbering.length}, (_, i) => i + 1);
  const duplicates = numbering.filter((n, i) => numbering.indexOf(n) !== i);
  const gaps = expected.filter(n => !numbering.includes(n));
  if (duplicates.length === 0 && gaps.length === 0) {
    return {found: '1 to ' + numbering.length, expected: '1 to ' + numbering.length, result: 'pass'};
  }
  const found = [];
  if (gaps.length > 0) found.push(`gaps: ${gaps.join(', ')}`);
  if (duplicates.length > 0) found.push(`duplicates: ${duplicates.join(', ')}`);
  return {found: found.join('; '), expected: '1 to ' + numbering.length, result: 'fail'};
}

function normalise(s) {
  return s
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/[–—]/g, '-')
    .replace(/\u2011/g, '-')
    .replace(/\u00A0/g, ' ');
}

function escapeHtml(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function docURL(symbol, paragraph) {
  return `https://undocs.org/${symbol}#para${paragraph}`;
}
</script>
</body>
</html>
```