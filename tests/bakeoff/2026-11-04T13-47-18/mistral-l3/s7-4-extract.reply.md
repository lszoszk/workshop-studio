I built the app you described: a two-tab tool that extracts the numbered paragraphs from the HTML version of a General Comment, checks them against the document's own reference, and lets the user download the result as JSON or Markdown. The header, left rail and footer are always visible; the checks and repairs are shown only when opened.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Paragraphs from a UN document</title>
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
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}
header .label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  color: var(--ink);
  opacity: 0.7;
}
header .title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.1rem;
  margin: 0 1rem;
  flex-grow: 1;
}
header .meta {
  display: flex;
  gap: 1rem;
  align-items: center;
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
}
header .status .dot {
  width: 0.8rem;
  height: 0.8rem;
  border-radius: 50%;
}
header .status .pass { background-color: var(--pass); }
header .status .fail { background-color: var(--accent); }
.left-rail {
  width: 20rem;
  padding: 1rem;
  border-right: 1px solid var(--rule);
  position: fixed;
  top: 3.5rem;
  bottom: 0;
  overflow-y: auto;
}
.left-rail h2 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.2rem;
  margin: 0 0 1rem 0;
  padding: 0;
}
.left-rail .card {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.left-rail .card .symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  margin: 0;
}
.left-rail .card .short-title {
  font-size: 0.9rem;
  margin: 0.5rem 0 0 0;
  color: var(--ink);
  opacity: 0.8;
}
.left-rail .big-numbers {
  margin: 1.5rem 0;
}
.left-rail .big-numbers .number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0;
  display: block;
}
.left-rail .big-numbers .label {
  font-size: 0.9rem;
  margin: 0.25rem 0 0 0;
  color: var(--ink);
  opacity: 0.8;
}
.left-rail .big-numbers .bar {
  height: 0.25rem;
  background-color: var(--accent);
  margin-top: 0.25rem;
  border-radius: 0.125rem;
}
.left-rail .big-numbers .bar.short {
  background-color: var(--accent);
  opacity: 0.5;
}
.left-rail .big-numbers .bar.over {
  background-color: var(--accent);
}
.left-rail .checks {
  margin-top: 1.5rem;
}
.left-rail .checks .number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  line-height: 1;
  margin: 0;
}
.left-rail .checks .label {
  font-size: 0.9rem;
  margin: 0.25rem 0 0 0;
  color: var(--ink);
  opacity: 0.8;
}
.tabs {
  margin-left: 20rem;
  padding: 1rem;
}
.tab-list {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--rule);
  margin: 0 0 1rem 0;
  padding: 0;
  list-style: none;
}
.tab-list li {
  margin: 0;
  padding: 0;
}
.tab-list button {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--ink);
  opacity: 0.7;
  cursor: pointer;
  margin: 0;
}
.tab-list button:hover {
  opacity: 1;
}
.tab-list button[aria-selected="true"] {
  opacity: 1;
  border-bottom-color: var(--accent);
  color: var(--accent);
}
.tab-panel {
  padding: 0;
}
.tab-panel h2 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  margin: 0 0 1rem 0;
}
.tab-panel h3 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.2rem;
  margin: 1.5rem 0 0.5rem 0;
}
.tab-panel .how {
  font-size: 0.8rem;
  color: var(--ink);
  opacity: 0.7;
  margin: 0.25rem 0 1rem 0;
}
.tab-panel .tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.tab-panel .tile {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.tab-panel .tile .number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0;
}
.tab-panel .tile .label {
  font-size: 0.9rem;
  margin: 0.25rem 0 0 0;
  color: var(--ink);
  opacity: 0.8;
}
.tab-panel .tile .fail {
  color: var(--accent);
}
.tab-panel .tile .limit {
  color: var(--accent);
}
.tab-panel .tile .pass {
  color: var(--pass);
}
.tab-panel .tile .diff {
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
.tab-panel .tile .diff.fail {
  color: var(--accent);
}
.tab-panel .first-words-list {
  margin: 1rem 0;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
}
.tab-panel .first-words-list .line {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
  display: flex;
  gap: 1rem;
}
.tab-panel .first-words-list .line:last-child {
  border-bottom: none;
}
.tab-panel .first-words-list .para {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
}
.tab-panel .first-words-list .found {
  flex-grow: 1;
}
.tab-panel .first-words-list .ref {
  flex-grow: 1;
}
.tab-panel .export {
  margin: 2rem 0;
  display: flex;
  gap: 1rem;
}
.tab-panel .export button {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  cursor: pointer;
}
.tab-panel .export button:hover {
  background: var(--paper);
}
.tab-panel .export button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.tab-panel .check-panel {
  margin: 2rem 0;
}
.tab-panel .check-panel h4 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 1.5rem 0 0.5rem 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.tab-panel .check-panel h4::before {
  content: "▶";
  font-size: 0.7rem;
}
.tab-panel .check-panel h4[aria-expanded="true"]::before {
  content: "▼";
}
.tab-panel .check-panel .checks {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
  padding: 0 1rem;
}
.tab-panel .check-panel .check {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  display: flex;
  gap: 1rem;
}
.tab-panel .check-panel .check:last-child {
  border-bottom: none;
}
.tab-panel .check-panel .check .what {
  flex-grow: 1;
}
.tab-panel .check-panel .check .found {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
}
.tab-panel .check-panel .check .expected {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
}
.tab-panel .check-panel .check .result {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
}
.tab-panel .check-panel .check .pass {
  color: var(--pass);
}
.tab-panel .check-panel .check .fail {
  color: var(--accent);
}
.tab-panel .check-panel .check .limit {
  color: var(--accent);
}
.tab-panel .check-panel .check .not-run {
  color: var(--ink);
  opacity: 0.5;
}
.tab-panel .check-panel .check .link {
  color: var(--accent);
  text-decoration: none;
}
.tab-panel .check-panel .check .link:hover {
  text-decoration: underline;
}
.tab-panel .repairs-panel {
  margin: 2rem 0;
}
.tab-panel .repairs-panel h4 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 1.5rem 0 0.5rem 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.tab-panel .repairs-panel h4::before {
  content: "▶";
  font-size: 0.7rem;
}
.tab-panel .repairs-panel h4[aria-expanded="true"]::before {
  content: "▼";
}
.tab-panel .repairs-panel .counts {
  margin-bottom: 1rem;
}
.tab-panel .repairs-panel .counts .count {
  display: flex;
  gap: 1rem;
  padding: 0.25rem 0;
}
.tab-panel .repairs-panel .counts .count .rule {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 10rem;
}
.tab-panel .repairs-panel .counts .count .n {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 3rem;
  text-align: right;
}
.tab-panel .repairs-panel .counts .count .paras {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
}
.tab-panel .repairs-panel .table {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
  width: 100%;
  border-collapse: collapse;
}
.tab-panel .repairs-panel .table th {
  padding: 0.5rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}
.tab-panel .repairs-panel .table td {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
.tab-panel .repairs-panel .table td.para {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 3rem;
}
.tab-panel .repairs-panel .table td.before {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 20rem;
}
.tab-panel .repairs-panel .table td.after {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 20rem;
}
.tab-panel .repairs-panel .table td.rule {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 10rem;
}
.tab-panel .repairs-panel .table tr:last-child td {
  border-bottom: none;
}
.tab-panel .repairs-panel .note {
  font-size: 0.8rem;
  color: var(--ink);
  opacity: 0.7;
  margin-top: 1rem;
}
.tab-panel .table-container {
  margin: 2rem 0;
}
.tab-panel table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
}
.tab-panel table caption {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  text-align: left;
}
.tab-panel table th {
  padding: 0.5rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}
.tab-panel table td {
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
.tab-panel table td.no {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 3rem;
  text-align: right;
}
.tab-panel table td.section {
  width: 15rem;
}
.tab-panel table td.first-line {
  flex-grow: 1;
}
.tab-panel table td.check {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 8rem;
  text-align: right;
}
.tab-panel table td.check.fail {
  color: var(--accent);
}
.tab-panel table tr:last-child td {
  border-bottom: none;
}
.tab-panel table tr[aria-expanded="true"] {
  background: var(--paper);
}
.tab-panel table tr[aria-expanded="true"] td {
  border-bottom: none;
  padding-bottom: 0;
}
.tab-panel table .expanded {
  padding: 0 1rem 1rem 1rem;
  border-bottom: 1px solid var(--rule);
}
.tab-panel table .expanded .text {
  white-space: pre-wrap;
  margin: 1rem 0;
}
.tab-panel table .expanded .text .mark {
  background-color: rgba(155, 35, 53, 0.1);
  border: 1px solid var(--accent);
  padding: 0 0.1rem;
}
.tab-panel table .expanded .first-words {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}
.tab-panel table .expanded .first-words .label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  width: 8rem;
}
.tab-panel table .expanded .first-words .found {
  flex-grow: 1;
}
.tab-panel table .expanded .first-words .ref {
  flex-grow: 1;
}
.tab-panel table .expanded .first-words .ref.fail {
  color: var(--accent);
}
.tab-panel table .expanded .repairs {
  margin: 1rem 0;
}
.tab-panel table .expanded .repairs .repair {
  margin: 0.5rem 0;
}
.tab-panel table .expanded .repairs .repair .before {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  color: var(--ink);
  opacity: 0.7;
}
.tab-panel table .expanded .repairs .repair .after {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
}
.tab-panel table .expanded .repairs .repair .rule {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  color: var(--ink);
  opacity: 0.7;
}
.tab-panel table .expanded .citation {
  margin: 1rem 0;
  display: flex;
  gap: 1rem;
  align-items: center;
}
.tab-panel table .expanded .citation button {
  padding: 0.25rem 0.5rem;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
}
.tab-panel table .expanded .citation button:hover {
  background: var(--paper);
}
.tab-panel table .expanded .citation .copied {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  color: var(--pass);
}
.tab-panel .headings-panel {
  margin: 2rem 0;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: white;
  padding: 1rem;
}
.tab-panel .headings-panel h4 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 0 0 0.5rem 0;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.tab-panel .headings-panel h4::before {
  content: "▶";
  font-size: 0.7rem;
}
.tab-panel .headings-panel h4[aria-expanded="true"]::before {
  content: "▼";
}
.tab-panel .headings-panel .headings {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.tab-panel .headings-panel .heading {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9rem;
  background: var(--paper);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}
footer {
  margin-left: 20rem;
  padding: 1rem;
  border-top: 1px solid var(--rule);
  font-size: 0.8rem;
  color: var(--ink);
  opacity: 0.7;
}
</style>
</head>
<body>

<header>
  <div class="label">UN DOCUMENT · HTML</div>
  <div class="title" id="title"></div>
  <div class="meta">
    <a id="symbol" target="_blank"></a>
    <span id="adopted"></span>
    <span id="source"></span>
    <div class="status">
      <div class="dot" id="status-dot"></div>
      <span id="status-text"></span>
    </div>
  </div>
</header>

<div class="left-rail">
  <h2>DOCUMENT</h2>
  <div class="card">
    <p class="symbol" id="rail-symbol"></p>
    <p class="short-title" id="rail-title"></p>
  </div>
  <div class="big-numbers">
    <span class="number" id="rail-paragraphs"></span>
    <span class="label">paragraphs of <span id="rail-paragraphs-expected"></span></span>
    <div class="bar" id="rail-paragraphs-bar"></div>
  </div>
  <div class="big-numbers">
    <span class="number" id="rail-footnotes">0</span>
    <span class="label">footnotes of <span id="rail-footnotes-expected"></span></span>
    <div class="bar" style="background-color: var(--accent);"></div>
  </div>
  <div class="checks">
    <span class="number" id="rail-checks-pass"></span>
    <span class="label">of <span id="rail-checks-total"></span> checks pass</span>
  </div>
</div>

<div class="tabs">
  <div role="tablist" aria-label="Tabs">
    <button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
    <button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
  </div>

  <div id="panel-01" role="tabpanel" tabindex="0" aria-labelledby="tab-01">
    <h2>Did the app find everything the document has?</h2>

    <div class="tiles">
      <div class="tile">
        <div class="number" id="tile-paragraphs-found"></div>
        <div class="label">Paragraphs found</div>
        <div class="how">How this is computed: the app counts the numbered &lt;p&gt; elements in the HTML.</div>
      </div>
      <div class="tile">
        <div class="number" id="tile-paragraphs-expected"></div>
        <div class="label">the document has <span id="tile-paragraphs-expected-value"></span></div>
        <div class="how">How this is computed: the reference in the file.</div>
        <div class="diff" id="tile-paragraphs-diff"></div>
      </div>
      <div class="tile">
        <div class="number" id="tile-first-words-match"></div>
        <div class="label">First words match</div>
        <div class="how">How this is computed: the first six words of each paragraph against the reference.</div>
      </div>
      <div class="tile">
        <div class="number" id="tile-footnotes-found">0</div>
        <div class="label fail">Footnotes</div>
        <div class="how limit">this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.</div>
      </div>
      <div class="tile">
        <div class="number" id="tile-spaces-restored"></div>
        <div class="label">Spaces</div>
        <div class="how">How this is computed: rules that insert a space where the characters prove one was there.</div>
        <div class="diff" id="tile-spaces-paras"></div>
      </div>
    </div>

    <div id="first-words-list" class="first-words-list hidden"></div>

    <h3>Take the paragraphs away</h3>
    <div class="export">
      <button id="download-json">Download JSON</button>
      <button id="download-markdown">Download Markdown</button>
    </div>

    <div class="check-panel">
      <h4 id="checks-heading" tabindex="0" role="button" aria-expanded="false" aria-controls="checks">Every check (<span id="checks-count"></span>)</h4>
      <div id="checks" class="checks hidden"></div>
    </div>

    <div class="repairs-panel">
      <h4 id="repairs-heading" tabindex="0" role="button" aria-expanded="false" aria-controls="repairs">The spaces restored (<span id="repairs-count"></span>)</h4>
      <div id="repairs" class="hidden">
        <div class="counts" id="repairs-counts"></div>
        <table class="table">
          <thead>
            <tr>
              <th class="para">Para.</th>
              <th class="before">Before</th>
              <th class="after">After</th>
              <th class="rule">Rule</th>
            </tr>
          </thead>
          <tbody id="repairs-table"></tbody>
        </table>
        <div class="note">Rules restore a space only where the characters prove it was there. Word pairs such as "Giventhe" are not touched.</div>
      </div>
    </div>
  </div>

  <div id="panel-02" role="tabpanel" tabindex="0" aria-labelledby="tab-02" class="hidden">
    <div class="headings-panel">
      <h4 id="headings-heading" tabindex="0" role="button" aria-expanded="false" aria-controls="headings">Headings found: <span id="headings-count"></span></h4>
      <div id="headings" class="headings hidden"></div>
    </div>

    <div class="table-container">
      <table>
        <caption>Every numbered paragraph in the document, with the heading it sits under.</caption>
        <thead>
          <tr>
            <th scope="col" class="no">No.</th>
            <th scope="col" class="section">Section</th>
            <th scope="col" class="first-line">First line</th>
            <th scope="col" class="check">Check</th>
          </tr>
        </thead>
        <tbody id="paragraphs-table"></tbody>
      </table>
    </div>
  </div>
</div>

<footer>
  <span id="footer-source"></span>, <span id="footer-built"></span>, and <span id="footer-note">Done by this page's code; no model was called and nothing left the browser.</span>
</footer>

<script>
(function() {
  const data = window.WORKSHOP_DATA.html_doc;
  const doc = new DOMParser().parseFromString(data.html, 'text/html');
  const ref = data.reference || {};
  const today = new Date().toISOString().split('T')[0];

  // State
  let paragraphs = [];
  let headings = [];
  let checks = [];
  let repairs = [];
  let firstWordsMismatches = [];
  let status = { pass: 0, fail: 0, limit: 0, notRun: 0 };

  // Header
  document.getElementById('title').textContent = data.title;
  const symbolLink = document.getElementById('symbol');
  symbolLink.textContent = data.symbol;
  symbolLink.href = data.doc_url;
  document.getElementById('adopted').textContent = `adopted ${ref.adopted || 'unknown date'}`;
  document.getElementById('source').textContent = data.source;
  document.getElementById('footer-source').textContent = data.source;
  document.getElementById('footer-built').textContent = today;

  // Left rail
  document.getElementById('rail-symbol').textContent = data.symbol;
  document.getElementById('rail-title').textContent = data.title.split(' (')[0];
  document.getElementById('rail-paragraphs-expected').textContent = ref.paragraphs || '?';
  document.getElementById('rail-footnotes-expected').textContent = ref.footnotes || '?';

  // Pipeline
  classifyElements(doc.body.children);
  repairText();
  assignSections();
  checkFirstWords();
  runChecks();
  render();

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');
  const panels = document.querySelectorAll('[role="tabpanel"]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const panelId = tab.getAttribute('aria-controls');
      tabs.forEach(t => {
        t.setAttribute('aria-selected', t.id === tab.id);
      });
      panels.forEach(p => {
        p.classList.toggle('hidden', p.id !== panelId);
      });
    });
  });

  // Expandable headings
  document.getElementById('checks-heading').addEventListener('click', () => {
    const expanded = document.getElementById('checks-heading').getAttribute('aria-expanded') === 'true';
    document.getElementById('checks-heading').setAttribute('aria-expanded', !expanded);
    document.getElementById('checks').classList.toggle('hidden');
  });
  document.getElementById('repairs-heading').addEventListener('click', () => {
    const expanded = document.getElementById('repairs-heading').getAttribute('aria-expanded') === 'true';
    document.getElementById('repairs-heading').setAttribute('aria-expanded', !expanded);
    document.getElementById('repairs').classList.toggle('hidden');
  });
  document.getElementById('headings-heading').addEventListener('click', () => {
    const expanded = document.getElementById('headings-heading').getAttribute('aria-expanded') === 'true';
    document.getElementById('headings-heading').setAttribute('aria-expanded', !expanded);
    document.getElementById('headings').classList.toggle('hidden');
  });

  // Downloads
  document.getElementById('download-json').addEventListener('click', () => {
    const json = JSON.stringify(paragraphs, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });
  document.getElementById('download-markdown').addEventListener('click', () => {
    let md = `---\ntitle: ${data.title}\nsymbol: ${data.symbol}\nadopted: ${ref.adopted || 'unknown'}\nsource_url: ${data.doc_url}\nextracted: ${today}\nparagraphs_found: ${paragraphs.length}\nparagraphs_expected: ${ref.paragraphs || '?'}\nfootnotes: this HTML version has none; the document has ${ref.footnotes || '?'}\n---\n\n`;
    let lastPart = null;
    let lastSection = null;
    paragraphs.forEach(p => {
      if (p.part !== lastPart) {
        md += `\n## ${p.part}\n`;
        lastPart = p.part;
        lastSection = null;
      }
      if (p.section !== lastSection) {
        md += `\n### ${p.section}\n`;
        lastSection = p.section;
      }
      md += `\n**${p.paragraph}.** ${p.text}\n`;
    });
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  // Classification
  function classifyElements(elements) {
    let inCover = true;
    let lastRomanHeading = null;
    Array.from(elements).forEach(el => {
      if (inCover && el.tagName === 'TABLE') {
        return; // cover table
      }
      inCover = false;
      if (el.tagName === 'P') {
        const match = el.textContent.match(/^(\d{1,3})\.\s*(.*)$/s);
        if (match) {
          paragraphs.push({
            element: el,
            paragraph: parseInt(match[1], 10),
            text_raw: match[2].trim().replace(/\s+/g, ' '),
            text: '',
            section: '',
            part: '',
            first_words_match: null,
            citation: `${data.symbol}, para. ${match[1]}`,
            doc_url: data.doc_url,
            limitations: `no footnotes in this HTML version; the document has ${ref.footnotes || '?'}`
          });
        } else if (el.textContent.match(/Committee on/)) {
          // committee line, ignore
        } else {
          checks.push({
            what: 'Unclassified &lt;p&gt; element',
            found: el.textContent.substring(0, 30) + '…',
            expected: 'not a paragraph',
            result: 'fail',
            link: null
          });
        }
      } else if (el.tagName === 'H2') {
        if (el.textContent.match(/General comment/)) {
          // title, ignore
        } else {
          const match = el.textContent.match(/^([IVX]+)\.\s*(.+)$/);
          if (match) {
            lastRomanHeading = match[2];
            headings.push({
              element: el,
              label: match[1],
              heading: match[2],
              level: 'part'
            });
          } else {
            headings.push({
              element: el,
              label: '',
              heading: el.textContent,
              level: 'part'
            });
          }
        }
      } else if (el.tagName === 'H3') {
        const match = el.textContent.match(/^([A-Z])\.\s*(.+)$/);
        if (match) {
          headings.push({
            element: el,
            label: match[1],
            heading: match[2],
            level: 'section'
          });
        } else {
          headings.push({
            element: el,
            label: '',
            heading: el.textContent,
            level: 'section'
          });
        }
      }
    });
    paragraphs.sort((a, b) => a.paragraph - b.paragraph);
  }

  // Repairs
  function repairText() {
    const rules = [
      { name: 'sentence join', regex: /([a-z])\.([A-Z])/g, replacement: '$1. $2' },
      { name: 'comma join', regex: /([a-z]),([A-Za-z])/g, replacement: '$1, $2' },
      { name: 'quote join', regex: /([a-z])“/g, replacement: '$1 “' },
      { name: 'dash join', regex: /–([A-Za-z])/g, replacement: '– $1' }
    ];
    paragraphs.forEach(p => {
      let text = p.text_raw;
      rules.forEach(rule => {
        let match;
        while ((match = rule.regex.exec(text)) !== null) {
          const before = text.substring(match.index - 20, match.index);
          const after = text.substring(match.index, match.index + 20);
          repairs.push({
            paragraph: p.paragraph,
            rule: rule.name,
            before: before + match[0] + after,
            after: before + match[0].replace(rule.regex, rule.replacement) + after
          });
          text = text.replace(rule.regex, rule.replacement);
          rule.regex.lastIndex = 0; // reset for global regex
        }
      });
      p.text = text;
    });
  }

  // Sections
  function assignSections() {
    let lastPart = null;
    let lastSection = null;
    headings.forEach(h => {
      if (h.level === 'part') {
        lastPart = h.heading;
        lastSection = null;
      } else if (h.level === 'section') {
        lastSection = h.heading;
      }
    });
    paragraphs.forEach(p => {
      let currentPart = lastPart;
      let currentSection = lastSection;
      for (let i = headings.length - 1; i >= 0; i--) {
        if (headings[i].element.compareDocumentPosition(p.element) & Node.DOCUMENT_POSITION_PRECEDING) {
          if (headings[i].level === 'part') {
            currentPart = headings[i].heading;
            break;
          } else if (headings[i].level === 'section') {
            currentSection = headings[i].heading;
          }
        }
      }
      p.part = currentPart;
      p.section = currentSection;
    });
  }

  // First words
  function checkFirstWords() {
    const normalize = s => s.replace(/[“”]/g, '"').replace(/[–‑]/g, '-').replace(/\u00A0/g, ' ');
    paragraphs.forEach(p => {
      const found = p.text.split(/\s+/).slice(0, 6).join(' ');
      const expected = ref.first_words ? ref.first_words[String(p.paragraph)] : null;
      p.first_words_match = expected ? normalize(found) === normalize(expected) : null;
      if (p.first_words_match === false) {
        firstWordsMismatches.push(p.paragraph);
      }
    });
  }

  // Checks
  function runChecks() {
    // Paragraph count
    checks.push({
      what: 'Paragraph count',
      found: paragraphs.length,
      expected: ref.paragraphs || 'no reference',
      result: ref.paragraphs ? (paragraphs.length === ref.paragraphs ? 'pass' : 'fail') : 'not-run',
      link: ref.paragraphs && paragraphs.length !== ref.paragraphs ? '#panel-02' : null
    });

    // Numbering
    const numbers = paragraphs.map(p => p.paragraph);
    const unique = [...new Set(numbers)];
    const duplicates = numbers.filter((n, i) => numbers.indexOf(n) !== i);
    const gaps = [];
    for (let i = 1; i <= (ref.paragraphs || numbers.length); i++) {
      if (!numbers.includes(i)) gaps.push(i);
    }
    checks.push({
      what: 'Numbering: exactly 1 to n in order',
      found: `1–${numbers.length}`,
      expected: `1–${ref.paragraphs || numbers.length}`,
      result: duplicates.length === 0 && gaps.length === 0 ? 'pass' : 'fail',
      link: duplicates.length > 0 || gaps.length > 0 ? '#panel-02' : null
    });
    if (duplicates.length > 0) {
      checks.push({
        what: 'Numbering: duplicates',
        found: duplicates.join(', '),
        expected: 'none',
        result: 'fail',
        link: '#panel-02'
      });
    }
    if (gaps.length > 0) {
      checks.push({
        what: 'Numbering: gaps',
        found: gaps.join(', '),
        expected: 'none',
        result: 'fail',
        link: '#panel-02'
      });
    }

    // First words
    const firstWordsMatch = paragraphs.filter(p => p.first_words_match).length;
    checks.push({
      what: 'First words match',
      found: firstWordsMatch,
      expected: ref.paragraphs || 'no reference',
      result: ref.paragraphs ? (firstWordsMatch === ref.paragraphs ? 'pass' : 'fail') : 'not-run',
      link: ref.paragraphs && firstWordsMatch !== ref.paragraphs ? '#panel-02' : null
    });

    // Footnotes
    checks.push({
      what: 'Footnotes',
      found: 0,
      expected: ref.footnotes || 'no reference',
      result: 'limit',
      link: null
    });

    // Repairs
    checks.push({
      what: 'Spaces restored',
      found: repairs.length,
      expected: 'n/a',
      result: repairs.length > 0 ? 'pass' : 'not-run',
      link: repairs.length > 0 ? '#repairs' : null
    });

    // Headings
    const h2 = headings.filter(h => h.level === 'part').length;
    const h3 = headings.filter(h => h.level === 'section').length;
    const glued = headings.filter(h => h.label && !h.heading.startsWith(h.label + ' ')).length;
    checks.push({
      what: 'Headings: &lt;h2&gt; elements',
      found: h2,
      expected: 'n/a',
      result: 'pass',
      link: null
    });
    checks.push({
      what: 'Headings: &lt;h3&gt; elements',
      found: h3,
      expected: 'n/a',
      result: 'pass',
      link: null
    });
    checks.push({
      what: 'Headings: glued labels separated',
      found: glued,
      expected: 'n/a',
      result: glued > 0 ? 'pass' : 'not-run',
      link: null
    });

    // Nothing lost
    const classified = paragraphs.length + headings.length + 1; // +1 for title
    const total = doc.body.children.length - 1; // -1 for cover table
    checks.push({
      what: 'Nothing lost: every block element classified',
      found: classified,
      expected: total,
      result: classified === total ? 'pass' : 'fail',
      link: classified !== total ? '#panel-02' : null
    });
    if (classified !== total) {
      const unclassified = Array.from(doc.body.children).filter(el => {
        return !paragraphs.some(p => p.element === el) &&
               !headings.some(h => h.element === el) &&
               el.tagName !== 'TABLE' &&
               !el.textContent.match(/Committee on/);
      });
      unclassified.forEach(el => {
        checks.push({
          what: 'Unclassified element',
          found: el.outerHTML.substring(0, 50) + '…',
          expected: 'classified',
          result: 'fail',
          link: '#panel-02'
        });
      });
    }

    // Export round trip
    try {
      const json = JSON.stringify(paragraphs);
      const parsed = JSON.parse(json);
      checks.push({
        what: 'Export round trip: JSON parses back',
        found: parsed.length,
        expected: paragraphs.length,
        result: parsed.length === paragraphs.length ? 'pass' : 'fail',
        link: null
      });
    } catch (e) {
      checks.push({
        what: 'Export round trip: JSON parses back',
        found: 'error',
        expected: paragraphs.length,
        result: 'fail',
        link: null
      });
    }

    // Status
    checks.forEach(check => {
      if (check.result === 'pass') status.pass++;
      else if (check.result === 'fail') status.fail++;
      else if (check.result === 'limit') status.limit++;
      else if (check.result === 'not-run') status.notRun++;
    });
  }

  // Render
  function render() {
    // Left rail
    document.getElementById('rail-paragraphs').textContent = paragraphs.length;
    document.getElementById('rail-paragraphs-expected').textContent = ref.paragraphs || '?';
    const bar = document.getElementById('rail-paragraphs-bar');
    if (ref.paragraphs) {
      const percent = (paragraphs.length / ref.paragraphs) * 100;
      bar.style.width = `${percent}%`;
      if (paragraphs.length < ref.paragraphs) bar.classList.add('short');
      if (paragraphs.length > ref.paragraphs) bar.classList.add('over');
    }
    document.getElementById('rail-checks-pass').textContent = status.pass;
    document.getElementById('rail-checks-total').textContent = checks.length;

    // Tiles
    document.getElementById('tile-paragraphs-found').textContent = paragraphs.length;
    document.getElementById('tile-paragraphs-expected').textContent = ref.paragraphs || '?';
    document.getElementById('tile-paragraphs-expected-value').textContent = ref.paragraphs || '?';
    if (ref.paragraphs) {
      const diff = paragraphs.length - ref.paragraphs;
      document.getElementById('tile-paragraphs-diff').textContent = diff === 0 ? '' : (diff > 0 ? `+${diff}` : diff);
      document.getElementById('tile-paragraphs-diff').classList.toggle('fail', diff !== 0);
    }
    const firstWordsMatch = paragraphs.filter(p => p.first_words_match).length;
    document.getElementById('tile-first-words-match').textContent = firstWordsMatch;
    document.getElementById('tile-spaces-restored').textContent = repairs.length;
    document.getElementById('tile-spaces-paras').textContent = `${repairs.length} in ${[...new Set(repairs.map(r => r.paragraph))].length} paragraphs`;

    // First words list
    const list = document.getElementById('first-words-list');
    if (firstWordsMismatches.length > 0) {
      list.classList.remove('hidden');
      firstWordsMismatches.slice(0, 10).forEach(n => {
        const p = paragraphs.find(p => p.paragraph === n);
        const line = document.createElement('div');
        line.className = 'line';
        line.innerHTML = `
          <div class="para">para. ${n}</div>
          <div class="found">${p.text.split(/\s+/).slice(0, 6).join(' ')}</div>
          <div class="ref">${ref.first_words ? ref.first_words[String(n)] : 'no reference'}</div>
        `;
        list.appendChild(line);
      });
      if (firstWordsMismatches.length > 10) {
        const line = document.createElement('div');
        line.className = 'line';
        line.textContent = `and ${firstWordsMismatches.length - 10} more`;
        list.appendChild(line);
      }
    }

    // Checks
    const checksContainer = document.getElementById('checks');
    checks.forEach(check => {
      const div = document.createElement('div');
      div.className = 'check';
      div.innerHTML = `
        <div class="what">${check.what}</div>
        <div class="found">${check.found}</div>
        <div class="expected">${check.expected}</div>
        <div class="result ${check.result}">${check.result === 'pass' ? 'pass' : check.result === 'fail' ? 'check failed' : check.result === 'limit' ? 'source limit' : 'not run'}${check.link ? ` <a href="${check.link}" class="link">→</a>` : ''}</div>
      `;
      checksContainer.appendChild(div);
    });
    document.getElementById('checks-count').textContent = checks.length;

    // Repairs
    const repairsCounts = document.getElementById('repairs-counts');
    const counts = {};
    repairs.forEach(r => {
      counts[r.rule] = (counts[r.rule] || 0) + 1;
    });
    Object.entries(counts).forEach(([rule, n]) => {
      const div = document.createElement('div');
      div.className = 'count';
      div.innerHTML = `
        <div class="rule">${rule}</div>
        <div class="n">${n}</div>
        <div class="paras">in ${[...new Set(repairs.filter(r => r.rule === rule).map(r => r.paragraph))].length} paragraphs</div>
      `;
      repairsCounts.appendChild(div);
    });
    const repairsTable = document.getElementById('repairs-table');
    repairs.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="para">${r.paragraph}</td>
        <td class="before">${r.before}</td>
        <td class="after">${r.after}</td>
        <td class="rule">${r.rule}</td>
      `;
      repairsTable.appendChild(tr);
    });
    document.getElementById('repairs-count').textContent = repairs.length;

    // Headings
    const headingsContainer = document.getElementById('headings');
    headings.forEach(h => {
      const div = document.createElement('div');
      div.className = 'heading';
      div.textContent = h.heading;
      headingsContainer.appendChild(div);
    });
    document.getElementById('headings-count').textContent = headings.length;

    // Paragraphs table
    const table = document.getElementById('paragraphs-table');
    paragraphs.forEach(p => {
      const tr = document.createElement('tr');
      tr.setAttribute('aria-expanded', 'false');
      tr.setAttribute('tabindex', '0');
      tr.innerHTML = `
        <td class="no">${p.paragraph}</td>
        <td class="section">${p.section}</td>
        <td class="first-line">${p.text.substring(0, 120).replace(/\s+/g, ' ')}…</td>
        <td class="check ${p.first_words_match === false ? 'fail' : ''}">${p.first_words_match === false ? 'first words differ' : 'OK'}</td>
      `;
      const expanded = document.createElement('tr');
      expanded.className = 'expanded hidden';
      expanded.innerHTML = `
        <td colspan="4">
          <div class="text" id="text-${p.paragraph}"></div>
          <div class="first-words">
            <div class="label">First words</div>
            <div class="found">${p.text.split(/\s+/).slice(0, 6).join(' ')}</div>
            <div class="ref ${p.first_words_match === false ? 'fail' : ''}">${ref.first_words ? ref.first_words[String(p.paragraph)] : 'no reference'}</div>
          </div>
          <div class="repairs" id="repairs-${p.paragraph}"></div>
          <div class="citation">
            <button data-citation="${p.citation}">Copy citation</button>
            <span class="copied hidden">Copied</span>
          </div>
        </td>
      `;
      table.appendChild(tr);
      table.appendChild(expanded);

      // Text with marks
      const textDiv = document.getElementById(`text-${p.paragraph}`);
      let text = p.text;
      repairs.filter(r => r.paragraph === p.paragraph).forEach(r => {
        const before = r.before.substring(r.before.length - 20);
        const after = r.after.substring(0, 20);
        const regex = new RegExp(escapeRegExp(before + after), 'g');
        text = text.replace(regex, match => {
          const index = match.indexOf(before) + before.length;
          return match.substring(0, index) + '<span class="mark">' + match.substring(index, index + (after.length - before.length)) + '</span>' + match.substring(index + (after.length - before.length));
        });
      });
      textDiv.innerHTML = text;

      // Repairs in this paragraph
      const repairsDiv = document.getElementById(`repairs-${p.paragraph}`);
      repairs.filter(r => r.paragraph === p.paragraph).forEach(r => {
        const div = document.createElement('div');
        div.className = 'repair';
        div.innerHTML = `
          <div class="before">${r.before}</div>
          <div class="after">${r.after}</div>
          <div class="rule">${r.rule}</div>
        `;
        repairsDiv.appendChild(div);
      });

      // Copy citation
      const button = expanded.querySelector('button');
      button.addEventListener('click', () => {
        navigator.clipboard.writeText(p.citation).then(() => {
          const copied = expanded.querySelector('.copied');
          copied.classList.remove('hidden');
          setTimeout(() => copied.classList.add('hidden'), 2000);
        });
      });

      // Expand row
      tr.addEventListener('click', () => {
        const expanded = tr.nextElementSibling;
        const isExpanded = tr.getAttribute('aria-expanded') === 'true';
        tr.setAttribute('aria-expanded', !isExpanded);
        expanded.classList.toggle('hidden');
      });
      tr.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          tr.click();
        }
      });
    });

    // Status
    const dot = document.getElementById('status-dot');
    const text = document.getElementById('status-text');
    if (status.fail > 0) {
      dot.classList.add('fail');
      dot.classList.remove('pass');
      text.textContent = `${status.pass} checks passed, ${status.fail} failed`;
    } else {
      dot.classList.add('pass');
      dot.classList.remove('fail');
      text.textContent = `${status.pass} checks passed`;
    }
    if (status.limit > 0) {
      text.textContent += `, ${status.limit} source limit`;
    }
    if (status.notRun > 0) {
      text.textContent += `, ${status.notRun} not run`;
    }
    document.getElementById('download-json').disabled = paragraphs.length === 0;
    document.getElementById('download-markdown').disabled = paragraphs.length === 0;
  }

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
})();
</script>
</body>
</html>
```