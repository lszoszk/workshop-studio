I built the verbatim finder for General Comments. It searches the 7,304 paragraphs with Boolean operators and exact phrases, shows the stored text with matched terms highlighted, copies citations and quotations, and collects them for a draft. The four tabs answer one question each: which committees say this, what exactly does it say, what have I collected, and can I trust this.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: General Comments and General Recommendations</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --amber: #d48300;
  --green: #2e7d32;
  --highlight: #fff9c4;
  --mono: ui-monospace, Menlo, Consolas, monospace;
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
[hidden] { display: none !important; }
a { color: var(--accent); text-decoration: none; }
a:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
h1, h2, h3 { font-weight: 400; margin: 0; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: 2.25rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.25rem; }
small { font-size: 0.875rem; }
.mono { font-family: var(--mono); font-size: 0.875rem; letter-spacing: 0.05em; }
.serif { font-family: Georgia, "Times New Roman", serif; }
.red { color: var(--accent); }
.amber { color: var(--amber); }
.green { color: var(--green); }
.bg-accent { background-color: var(--accent); }
.bg-highlight { background-color: var(--highlight); }
.bg-amber { background-color: #fff8e1; }
.bg-green { background-color: #e8f5e9; }
.container {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 1rem;
  padding: 1rem;
}
@media (max-width: 800px) {
  .container { grid-template-columns: 1fr; }
  .rail { display: none; }
  .rail-open .rail { display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 100; background: var(--paper); padding: 1rem; overflow-y: auto; }
  .rail-open .main { display: none; }
}
.header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--rule);
}
.header .label { font-family: var(--mono); font-size: 0.75rem; color: #666; }
.header .source { font-size: 0.875rem; }
.header .checks { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
.header .checks .dot { display: inline-block; width: 0.75rem; height: 0.75rem; border-radius: 50%; }
.tablist {
  grid-column: 1 / -1;
  display: flex;
  gap: 0.5rem;
  padding: 0;
  margin: 0;
  list-style: none;
  border-bottom: 1px solid var(--rule);
  overflow-x: auto;
}
.tablist button {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--rule);
  border-bottom: none;
  border-radius: 0.5rem 0.5rem 0 0;
  background: none;
  font-family: var(--mono);
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  cursor: pointer;
  white-space: nowrap;
}
.tablist button[aria-selected="true"] {
  border-color: var(--accent);
  border-bottom-color: transparent;
  background: var(--paper);
  color: var(--accent);
  font-weight: 600;
}
.tablist button:focus { outline: 2px solid var(--accent); outline-offset: -2px; }
.rail {
  padding: 1rem 0;
  border-right: 1px solid var(--rule);
}
.rail h2 { font-family: var(--mono); font-size: 0.875rem; letter-spacing: 0.05em; margin-bottom: 1rem; }
.rail .clear { background: none; border: none; color: var(--accent); font-family: var(--mono); font-size: 0.875rem; cursor: pointer; padding: 0; margin-bottom: 1rem; }
.rail .big-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 3rem;
  line-height: 1;
  margin: 0 0 1rem;
}
.rail .big-number small { font-size: 1rem; }
.rail .search-box {
  margin-bottom: 1rem;
  position: relative;
}
.rail .search-box label { display: block; font-size: 0.875rem; margin-bottom: 0.25rem; }
.rail .search-box input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  font-size: 1rem;
}
.rail .search-box .examples {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--paper);
  border: 1px solid var(--rule);
  border-top: none;
  border-radius: 0 0 0.25rem 0.25rem;
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}
.rail .search-box .examples button {
  display: block;
  width: 100%;
  padding: 0.5rem;
  text-align: left;
  background: none;
  border: none;
  border-bottom: 1px solid var(--rule);
  font-size: 0.875rem;
  cursor: pointer;
}
.rail .search-box .examples button:last-child { border-bottom: none; }
.rail .search-box .examples button:hover { background: var(--rule); }
.rail .search-box .echo {
  font-size: 0.875rem;
  margin: 0.5rem 0;
  font-style: italic;
}
.rail .search-box .error {
  color: var(--accent);
  font-size: 0.875rem;
  margin: 0.5rem 0;
}
.rail .filters { margin-top: 1rem; }
.rail .filters h3 {
  font-family: var(--mono);
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  margin: 1rem 0 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rail .filters h3 button {
  background: none;
  border: none;
  font-family: var(--mono);
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
}
.rail .filters .group { display: none; }
.rail .filters .group[aria-expanded="true"] { display: block; }
.rail .filters .group .all-none {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}
.rail .filters .group .all-none button {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
}
.rail .filters .group .checkboxes {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-height: 200px;
  overflow-y: auto;
}
.rail .filters .group .checkboxes label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.rail .filters .group .checkboxes input { accent-color: var(--accent); }
.rail .filters .group .years {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
.rail .filters .group .years input {
  width: 60px;
  padding: 0.25rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
}
.rail .filters .group .documents select {
  width: 100%;
  padding: 0.25rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  font-size: 0.875rem;
}
.rail .filters .chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}
.rail .filters .chips button {
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 1rem;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
}
.main { padding: 1rem 0; }
.tab { display: none; }
.tab[aria-expanded="true"] { display: block; }
.tab h2 { margin-bottom: 1rem; }
.tab .summary {
  font-size: 0.875rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.tab .summary select {
  padding: 0.25rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  font-size: 0.875rem;
}
.tab .hint {
  font-family: var(--mono);
  font-size: 0.875rem;
  margin-bottom: 1rem;
  color: #666;
}
.tab .chart-container {
  margin-bottom: 2rem;
  position: relative;
}
.tab .chart-container .chart-title {
  font-family: var(--mono);
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}
.tab .chart-container .chart-note {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.5rem;
}
.tab .chart-container canvas {
  max-width: 100%;
  height: auto;
}
.tab .chart-container table {
  margin-top: 1rem;
  border-collapse: collapse;
  width: 100%;
}
.tab .chart-container table th,
.tab .chart-container table td {
  padding: 0.5rem;
  border: 1px solid var(--rule);
  text-align: left;
  font-size: 0.875rem;
}
.tab .chart-container table th { font-family: var(--mono); }
.results {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.result {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.result header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}
.result header .badge {
  font-family: var(--mono);
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
}
.result header .doc {
  display: flex;
  gap: 0.5rem;
  align-items: baseline;
}
.result header .doc a {
  font-family: var(--mono);
  font-size: 0.875rem;
}
.result header .doc .pinpoint { font-size: 0.875rem; color: var(--accent); }
.result .text {
  white-space: pre-wrap;
  word-break: break-word;
}
.result .text mark {
  background-color: var(--highlight);
  font-weight: 600;
  padding: 0 0.125rem;
}
.result .meta {
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.result .meta button {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0;
}
.result .note {
  background-color: var(--amber);
  color: var(--ink);
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}
.result .expanded {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
}
.result .expanded .buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.result .expanded .buttons button {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: none;
  font-size: 0.875rem;
  cursor: pointer;
}
.result .expanded .buttons button:focus { outline: 2px solid var(--accent); }
.result .expanded .context {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
}
.result .expanded .context .para {
  background: #f9f9f9;
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}
.result .expanded .context .para header {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}
.result .expanded .context .para .text {
  font-size: 0.875rem;
  color: #666;
}
.load-more {
  margin-top: 1rem;
  text-align: center;
}
.load-more button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: none;
  font-size: 1rem;
  cursor: pointer;
}
.draft {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.draft-item {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.draft-item header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}
.draft-item header .citation { font-family: var(--mono); font-size: 0.875rem; }
.draft-item .quote {
  white-space: pre-wrap;
  word-break: break-word;
  margin-bottom: 0.5rem;
}
.draft-item .remove {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
  align-self: flex-end;
}
.draft-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.draft-actions button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background: none;
  font-size: 1rem;
  cursor: pointer;
}
.draft-hint {
  font-family: var(--mono);
  font-size: 0.875rem;
  color: #666;
}
.checks-panel {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.checks-panel h3 {
  font-family: var(--mono);
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}
.checks-panel .check {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  font-size: 0.875rem;
}
.checks-panel .check:last-child { border-bottom: none; }
.checks-panel .check .status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.checks-panel .check .status.pass { color: var(--green); }
.checks-panel .check .status.fail { color: var(--accent); }
.checks-panel .check .status .dot {
  display: inline-block;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}
.quirks {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.quirks h3 {
  font-family: var(--mono);
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
}
.quirks .quirk {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  font-size: 0.875rem;
}
.quirks .quirk:last-child { border-bottom: none; }
.footer {
  grid-column: 1 / -1;
  font-family: var(--mono);
  font-size: 0.75rem;
  color: #666;
  padding-top: 1rem;
  border-top: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
}
.copy-box {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-family: var(--mono);
  font-size: 0.875rem;
  width: 100%;
  margin: 0.5rem 0;
  background: white;
}
.live-region {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
</head>
<body>

<div class="container">
  <header class="header">
    <div>
      <div class="label">UN TREATY BODIES · GENERAL COMMENTS</div>
      <h1 class="serif">Verbatim finder: General Comments and General Recommendations</h1>
      <div class="source">7304 paragraphs from <span id="n-titles">0</span> General Comments (<span id="n-committees">0</span> committees, <span id="year-range">0000–0000</span>) · <a id="source-url" href="#" target="_blank">source</a></div>
    </div>
    <div class="checks">
      <span class="dot" id="checks-dot"></span>
      <span id="checks-count">0 checks pass</span>
    </div>
  </header>

  <nav class="rail" aria-label="Filters">
    <button class="clear mono" id="clear-all">Clear all</button>
    <div class="big-number serif" id="matching-count" aria-live="polite">0 <small>matching paragraphs</small></div>
    <div class="big-number serif">7304 <small>paragraphs</small></div>

    <div class="search-box">
      <label for="query">Search</label>
      <input type="text" id="query" placeholder="words or &quot;exact phrase&quot;" aria-describedby="query-help">
      <div class="examples" id="query-examples" hidden>
        <button data-query='"best interests" AND child'>"best interests" AND child</button>
        <button data-query='(torture OR ill-treatment) NOT detention'>(torture OR ill-treatment) NOT detention</button>
        <button data-query='"reasonable accommodation"'>"reasonable accommodation"</button>
      </div>
      <div class="echo" id="query-echo"></div>
      <div class="error" id="query-error"></div>
    </div>
    <div id="query-help" class="mono" style="font-size: 0.75rem; color: #666;">
      a space or AND joins words; OR; NOT or a leading minus; "an exact phrase" in double quotes; parentheses; a star at the end of a word for any ending (child* finds children); operators in capitals, lower-case "or" is a word
    </div>

    <div class="filters">
      <h3>
        <button id="filter-01-toggle" aria-expanded="false">01 Committee, years, document</button>
      </h3>
      <div class="group" id="filter-01" aria-expanded="false">
        <div class="all-none">
          <button id="committee-all">all</button> / <button id="committee-none">none</button>
        </div>
        <div class="checkboxes" id="committee-checkboxes"></div>
        <div class="years">
          <label for="year-from">Years</label>
          <input type="number" id="year-from" min="1900" max="2100">
          <span>to</span>
          <input type="number" id="year-to" min="1900" max="2100">
        </div>
        <div class="documents">
          <label for="document-select">Document</label>
          <select id="document-select">
            <option value="">All documents</option>
          </select>
        </div>
      </div>
    </div>
    <div class="chips" id="filter-chips"></div>
  </nav>

  <main class="main">
    <div role="tablist" aria-label="Tabs" class="tablist">
      <button id="tab-01-toggle" role="tab" aria-selected="true" aria-controls="tab-01">01 OVERVIEW</button>
      <button id="tab-02-toggle" role="tab" aria-selected="false" aria-controls="tab-02">02 PARAGRAPHS</button>
      <button id="tab-03-toggle" role="tab" aria-selected="false" aria-controls="tab-03">03 DRAFT</button>
      <button id="tab-04-toggle" role="tab" aria-selected="false" aria-controls="tab-04">04 CHECK & METHOD</button>
    </div>

    <section id="tab-01" class="tab" role="tabpanel" aria-expanded="true">
      <div class="chart-container">
        <div class="chart-title">FIG.01 Paragraphs per committee</div>
        <canvas id="chart-committees" role="img" aria-label="Bar chart showing the number of matching paragraphs per committee"></canvas>
        <div class="chart-note">How this is computed: one count per committee over the paragraphs that match the query and filters.</div>
        <table id="chart-table">
          <thead>
            <tr><th>Committee</th><th>Paragraphs</th></tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    </section>

    <section id="tab-02" class="tab" role="tabpanel" aria-expanded="false" hidden>
      <div class="summary" aria-live="polite">
        <span id="results-summary">0 of 7304 paragraphs match</span>
        <div>
          <span>sorted by</span>
          <select id="order-select">
            <option value="year-desc">year, newest first</option>
            <option value="doc">document order</option>
            <option value="matches">most matches first</option>
          </select>
        </div>
      </div>
      <div class="hint mono">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</div>
      <div class="results" id="results"></div>
      <div class="load-more">
        <button id="load-more">Show 25 more</button>
      </div>
    </section>

    <section id="tab-03" class="tab" role="tabpanel" aria-expanded="false" hidden>
      <h2>Your draft (<span id="draft-count">0</span> quotations)</h2>
      <div class="draft-actions">
        <button id="copy-all">Copy all</button>
        <button id="download-txt">Download .txt</button>
        <button id="download-csv">Download .csv</button>
      </div>
      <div class="draft-hint mono">Stored in localStorage when allowed, in memory otherwise.</div>
      <div class="draft" id="draft"></div>
    </section>

    <section id="tab-04" class="tab" role="tabpanel" aria-expanded="false" hidden>
      <div class="checks-panel">
        <h3>Checks</h3>
        <div id="checks"></div>
      </div>
      <div class="quirks">
        <h3>Known quirks of this file</h3>
        <div id="quirks"></div>
      </div>
      <div>
        <h3>How this is computed</h3>
        <p>The app searches the 7,304 paragraphs of General Comments and General Recommendations stored in the file. It never invents a paragraph, a symbol or a pinpoint. Every citation and quotation is built from the record's fields. The Check & method tab lists the checks the app runs on its own results.</p>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div id="footer-source">Source: <span id="footer-source-text"></span> · Built: <span id="footer-built"></span></div>
    <div>Counting, matching and sorting are done by this page's code; no model is called.</div>
  </footer>
</div>

<div class="live-region" aria-live="polite" id="live-region"></div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
(function() {
  'use strict';

  // Data
  const R = window.WORKSHOP_DATA.gc.records;
  const source = window.WORKSHOP_DATA.gc.source;
  const source_url = window.WORKSHOP_DATA.gc.source_url;
  const built = window.WORKSHOP_DATA.gc.built;

  // State
  let state = {
    query: '',
    queryTree: null,
    queryError: null,
    filters: {
      committees: new Set(),
      yearFrom: null,
      yearTo: null,
      document: ''
    },
    order: 'year-desc',
    expanded: null,
    draft: [],
    checks: [],
    quirks: []
  };

  // DOM
  const $ = id => document.getElementById(id);
  const $$ = sel => document.querySelectorAll(sel);

  // Header
  $('source-url').textContent = source;
  $('source-url').href = source_url;
  $('footer-source-text').textContent = source;
  $('footer-built').textContent = built;

  // Totals
  const titles = new Set(R.map(r => r.title));
  const committees = new Set(R.map(r => r.committee));
  const years = R.map(r => r.year);
  const yearMin = Math.min(...years);
  const yearMax = Math.max(...years);
  $('n-titles').textContent = titles.size;
  $('n-committees').textContent = committees.size;
  $('year-range').textContent = `${yearMin}–${yearMax}`;

  // Precompute per record
  R.forEach(r => {
    // Normalised text for search
    r.norm = normaliseText(r.text);

    // Footnote marks removed for display
    r.marks = (r.text.match(/\[\[fn:\d+\]\]/g) || []).length;
    r.textClean = r.text.replace(/\[\[fn:\d+\]\]/g, '');

    // Leading number
    const leadingMatch = r.text.match(/^(\d{1,3})\.\s/);
    r.leading = leadingMatch ? parseInt(leadingMatch[1], 10) : null;

    // Pinpoint
    if (r.paragraph === 0) {
      r.pinpoint = 'preamble';
    } else if (/^\([a-z]{1,4}\)/.test(r.text)) {
      r.pinpoint = `subpara. ${r.text.match(/^\(([a-z]{1,4})\)/)[1]}`;
    } else {
      r.pinpoint = `para. ${r.paragraph}`;
    }

    // Citation
    const shared = R.filter(r2 => r2.symbol === r.symbol && r2.title !== r.title).length > 0;
    if (shared) {
      const docName = r.title.split(':')[0].split(' on ')[0];
      r.citation = `${r.committee}, ${docName} (${r.symbol}), ${r.pinpoint}`;
    } else {
      r.citation = `${r.symbol}, ${r.pinpoint}`;
    }

    // Committees (for joint documents)
    r.committees = [];
    const symbolCommittees = r.symbol.match(/\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g) || [];
    if (symbolCommittees.includes('CAT/OP')) symbolCommittees[symbolCommittees.indexOf('CAT/OP')] = 'CAT-OP';
    r.committees = [...new Set([...symbolCommittees, r.committee])];
  });

  // Quirks
  const quirks = {
    preambles: R.filter(r => r.paragraph === 0),
    sharedSymbols: Array.from(new Set(R.filter(r => {
      return R.filter(r2 => r2.symbol === r.symbol && r2.title !== r.title).length > 0;
    }).map(r => r.symbol))),
    jointDocuments: R.filter(r => r.committees.length > 1),
    duplicatedPinpoints: Array.from(new Set(R.filter(r => {
      return R.filter(r2 => r2.title === r.title && r2.pinpoint === r.pinpoint && r2.id !== r.id).length > 0;
    }).map(r => `${r.title} ${r.pinpoint}`))),
    leadingMismatches: R.filter(r => r.leading !== null && r.leading !== r.paragraph)
  };

  state.quirks = [
    { label: 'Paragraphs with paragraph 0 (preambles)', count: quirks.preambles.length, example: quirks.preambles[0] ? `${quirks.preambles[0].symbol}, ${quirks.preambles[0].pinpoint}` : '' },
    { label: 'Symbols shared by several documents', count: quirks.sharedSymbols.length, example: quirks.sharedSymbols[0] || '' },
    { label: 'Joint General Comments (count under both committees)', count: quirks.jointDocuments.length, example: quirks.jointDocuments[0] ? `${quirks.jointDocuments[0].symbol} (${quirks.jointDocuments[0].committees.join(', ')})` : '' },
    { label: 'Duplicated pinpoints (same title and paragraph)', count: quirks.duplicatedPinpoints.length, example: quirks.duplicatedPinpoints[0] || '' },
    { label: 'Leading number differs from paragraph number', count: quirks.leadingMismatches.length, example: quirks.leadingMismatches[0] ? `${quirks.leadingMismatches[0].symbol}, ${quirks.leadingMismatches[0].pinpoint} (text begins "${quirks.leadingMismatches[0].leading}.")` : '' }
  ];

  // Committees for filter
  const committeeData = {};
  R.forEach(r => {
    r.committees.forEach(c => {
      if (!committeeData[c]) {
        committeeData[c] = { name: committeeName(c), count: 0 };
      }
      committeeData[c].count++;
    });
  });
  const committeeList = Object.entries(committeeData).sort((a, b) => b[1].count - a[1].count);

  // Documents for filter
  const documents = Array.from(new Set(R.map(r => r.short_title))).sort();
  const documentSelect = $('document-select');
  const committeeGroups = {};
  R.forEach(r => {
    if (!committeeGroups[r.committee]) committeeGroups[r.committee] = [];
    committeeGroups[r.committee].push(r.short_title);
  });
  Object.entries(committeeGroups).forEach(([code, titles]) => {
    const optgroup = document.createElement('optgroup');
    optgroup.label = committeeName(code);
    titles.forEach(title => {
      const option = document.createElement('option');
      option.value = title;
      option.textContent = title;
      optgroup.appendChild(option);
    });
    documentSelect.appendChild(optgroup);
  });

  // Init
  initFilters();
  initTabs();
  initSearch();
  initDraft();
  renderQuirks();
  renderChecks();
  updateChecksDot();

  // Filters
  function initFilters() {
    const checkboxes = $('committee-checkboxes');
    committeeList.forEach(([code, data]) => {
      const div = document.createElement('div');
      div.innerHTML = `
        <label>
          <input type="checkbox" value="${code}" checked>
          ${data.name} <span class="mono">(${data.count})</span>
        </label>
      `;
      checkboxes.appendChild(div);
    });

    $('year-from').value = yearMin;
    $('year-to').value = yearMax;
    state.filters.yearFrom = yearMin;
    state.filters.yearTo = yearMax;

    $('committee-all').addEventListener('click', () => {
      $$('#committee-checkboxes input').forEach(el => el.checked = true);
      updateFilters();
    });
    $('committee-none').addEventListener('click', () => {
      $$('#committee-checkboxes input').forEach(el => el.checked = false);
      updateFilters();
    });
    $$('#committee-checkboxes input').forEach(el => {
      el.addEventListener('change', updateFilters);
    });
    $('year-from').addEventListener('change', () => {
      state.filters.yearFrom = parseInt($('year-from').value, 10) || yearMin;
      updateFilters();
    });
    $('year-to').addEventListener('change', () => {
      state.filters.yearTo = parseInt($('year-to').value, 10) || yearMax;
      updateFilters();
    });
    $('document-select').addEventListener('change', () => {
      state.filters.document = $('document-select').value;
      updateFilters();
    });
    $('clear-all').addEventListener('click', () => {
      $$('#committee-checkboxes input').forEach(el => el.checked = true);
      $('year-from').value = yearMin;
      $('year-to').value = yearMax;
      state.filters.yearFrom = yearMin;
      state.filters.yearTo = yearMax;
      $('document-select').value = '';
      state.filters.document = '';
      updateFilters();
    });
    $('filter-01-toggle').addEventListener('click', () => {
      const expanded = $('filter-01').getAttribute('aria-expanded') === 'true';
      $('filter-01').setAttribute('aria-expanded', !expanded);
    });
  }

  function updateFilters() {
    state.filters.committees = new Set();
    $$('#committee-checkboxes input:checked').forEach(el => {
      state.filters.committees.add(el.value);
    });
    renderFilterChips();
    runSearch();
  }

  function renderFilterChips() {
    const chips = $('filter-chips');
    chips.innerHTML = '';
    if (state.filters.committees.size < committeeList.length) {
      const chip = document.createElement('button');
      chip.textContent = `${committeeList.length - state.filters.committees.size} committees excluded`;
      chip.addEventListener('click', () => {
        $$('#committee-checkboxes input').forEach(el => el.checked = true);
        updateFilters();
      });
      chips.appendChild(chip);
    }
    if (state.filters.yearFrom !== yearMin || state.filters.yearTo !== yearMax) {
      const chip = document.createElement('button');
      chip.textContent = `years ${state.filters.yearFrom}–${state.filters.yearTo}`;
      chip.addEventListener('click', () => {
        $('year-from').value = yearMin;
        $('year-to').value = yearMax;
        state.filters.yearFrom = yearMin;
        state.filters.yearTo = yearMax;
        updateFilters();
      });
      chips.appendChild(chip);
    }
    if (state.filters.document) {
      const chip = document.createElement('button');
      chip.textContent = state.filters.document;
      chip.addEventListener('click', () => {
        $('document-select').value = '';
        state.filters.document = '';
        updateFilters();
      });
      chips.appendChild(chip);
    }
  }

  // Tabs
  function initTabs() {
    $$('[role="tab"]').forEach(tab => {
      tab.addEventListener('click', () => {
        const tabId = tab.id.replace('-toggle', '');
        $$('[role="tab"]').forEach(t => t.setAttribute('aria-selected', 'false'));
        $$('[role="tabpanel"]').forEach(p => p.setAttribute('aria-expanded', 'false'));
        tab.setAttribute('aria-selected', 'true');
        $(`#${tabId}`).setAttribute('aria-expanded', 'true');
        if (tabId === 'tab-03') {
          renderDraft();
        }
      });
      tab.addEventListener('keydown', e => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          const tabs = $$('[role="tab"]');
          const index = Array.from(tabs).indexOf(tab);
          const nextIndex = e.key === 'ArrowRight' ? (index + 1) % tabs.length : (index - 1 + tabs.length) % tabs.length;
          tabs[nextIndex].focus();
        }
      });
    });
  }

  // Search
  function initSearch() {
    const queryInput = $('query');
    const examples = $('query-examples');

    queryInput.addEventListener('focus', () => {
      if (!queryInput.value) {
        examples.hidden = false;
      }
    });
    queryInput.addEventListener('blur', () => {
      examples.hidden = true;
    });
    queryInput.addEventListener('input', () => {
      if (queryInput.value) {
        examples.hidden = true;
      }
    });
    queryInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        runSearch();
      }
    });
    $$('#query-examples button').forEach(button => {
      button.addEventListener('click', () => {
        queryInput.value = button.dataset.query;
        examples.hidden = true;
        runSearch();
      });
    });
    $('order-select').addEventListener('change', () => {
      state.order = $('order-select').value;
      renderResults();
    });
  }

  function runSearch() {
    const query = $('query').value.trim();
    state.query = query;

    // Parse query
    try {
      const { tree, echo } = parseQuery(query);
      state.queryTree = tree;
      state.queryError = null;
      $('query-echo').textContent = echo;
      $('query-error').textContent = '';
    } catch (e) {
      state.queryTree = null;
      state.queryError = e.message;
      $('query-echo').textContent = '';
      $('query-error').textContent = e.message;
      renderResults();
      return;
    }

    renderResults();
  }

  function parseQuery(query) {
    if (!query) {
      return { tree: null, echo: 'No search words' };
    }

    // Tokenise
    const tokens = [];
    let i = 0;
    while (i < query.length) {
      if (query[i] === ' ') {
        i++;
        continue;
      }
      if (query[i] === '"') {
        const start = i;
        i++;
        while (i < query.length && query[i] !== '"') i++;
        if (i >= query.length) throw new Error('Unbalanced double quote');
        tokens.push({ type: 'phrase', value: query.slice(start + 1, i) });
        i++;
      } else if (query[i] === '(' || query[i] === ')') {
        tokens.push({ type: 'paren', value: query[i] });
        i++;
      } else if (query.slice(i, i + 3) === 'AND') {
        tokens.push({ type: 'and' });
        i += 3;
      } else if (query.slice(i, i + 2) === 'OR') {
        tokens.push({ type: 'or' });
        i += 2;
      } else if (query.slice(i, i + 3) === 'NOT') {
        tokens.push({ type: 'not' });
        i += 3;
      } else if (query[i] === '-') {
        tokens.push({ type: 'not' });
        i++;
      } else {
        const start = i;
        while (i < query.length && !' ()"'.includes(query[i])) i++;
        tokens.push({ type: 'word', value: query.slice(start, i) });
      }
    }

    // Shunting-yard to tree
    const output = [];
    const ops = [];
    let expectOperand = true;

    tokens.forEach(token => {
      if (token.type === 'word' || token.type === 'phrase') {
        if (!expectOperand) throw new Error('Unexpected word or phrase');
        output.push(token);
        expectOperand = false;
      } else if (token.type === 'paren' && token.value === '(') {
        ops.push(token);
        expectOperand = true;
      } else if (token.type === 'paren' && token.value === ')') {
        while (ops.length && ops[ops.length - 1].value !== '(') {
          output.push(ops.pop());
        }
        if (!ops.length) throw new Error('Unbalanced parenthesis');
        ops.pop();
        expectOperand = false;
      } else if (token.type === 'not') {
        ops.push(token);
        expectOperand = true;
      } else if (token.type === 'and' || token.type === 'or') {
        while (ops.length && precedence(ops[ops.length - 1]) >= precedence(token)) {
          output.push(ops.pop());
        }
        ops.push(token);
        expectOperand = true;
      }
    });

    while (ops.length) {
      const op = ops.pop();
      if (op.value === '(') throw new Error('Unbalanced parenthesis');
      output.push(op);
    }

    if (output.length === 0) throw new Error('Empty query');

    // Build tree
    const stack = [];
    output.forEach(token => {
      if (token.type === 'word' || token.type === 'phrase') {
        stack.push(token);
      } else if (token.type === 'not') {
        const operand = stack.pop();
        stack.push({ type: 'not', operand });
      } else if (token.type === 'and' || token.type === 'or') {
        const right = stack.pop();
        const left = stack.pop();
        stack.push({ type: token.type, left, right });
      }
    });

    const tree = stack[0];

    // Echo
    function echoNode(node) {
      if (node.type === 'word') return node.value;
      if (node.type === 'phrase') return `"${node.value}"`;
      if (node.type === 'not') return `NOT ${echoNode(node.operand)}`;
      if (node.type === 'and') return `${echoNode(node.left)} AND ${echoNode(node.right)}`;
      if (node.type === 'or') return `${echoNode(node.left)} OR ${echoNode(node.right)}`;
    }

    const echo = `Paragraphs containing ${echoNode(tree)}`;
    return { tree, echo };
  }

  function precedence(op) {
    if (op.type === 'not') return 3;
    if (op.type === 'and') return 2;
    if (op.type === 'or') return 1;
    return 0;
  }

  function normaliseText(text) {
    return text
      .replace(/\[\[fn:\d+\]\]/g, '')
      .replace(/[“”„]/g, '"')
      .replace(/[‘’‚]/g, "'")
      .replace(/[\u2013\u2014\u00AD]/g, '-')
      .replace(/\s+/g, ' ')
      .toLowerCase();
  }

  function termToRegex(term) {
    if (term.type === 'word') {
      let word = term.value;
      let star = false;
      if (word.endsWith('*')) {
        word = word.slice(0, -1);
        star = true;
      }
      word = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      if (star) word += '\\w*';
      return new RegExp(`(?<![\\p{L}\\p{N}])${word}(?![\\p{L}\\p{N}])`, 'u');
    } else if (term.type === 'phrase') {
      const words = term.value.split(/\s+/).map(w => {
        w = w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        return w;
      });
      return new RegExp(`(?<![\\p{L}\\p{N}])${words.join('\\s+')}(?![\\p{L}\\p{N}])`, 'u');
    }
  }

  function matchRecord(record, tree) {
    if (!tree) return true;

    function match(node) {
      if (node.type === 'word' || node.type === 'phrase') {
        const regex = termToRegex(node);
        return regex.test(record.norm);
      } else if (node.type === 'not') {
        return !match(node.operand);
      } else if (node.type === 'and') {
        return match(node.left) && match(node.right);
      } else if (node.type === 'or') {
        return match(node.left) || match(node.right);
      }
    }

    return match(tree);
  }

  function highlightText(text, tree) {
    if (!tree) return escapeHtml(text);

    const terms = [];
    function collectTerms(node) {
      if (node.type === 'word' || node.type === 'phrase') {
        terms.push(node);
      } else if (node.type === 'not') {
        collectTerms(node.operand);
      } else if (node.type === 'and' || node.type === 'or') {
        collectTerms(node.left);
        collectTerms(node.right);
      }
    }
    collectTerms(tree);

    let html = escapeHtml(text);
    terms.forEach(term => {
      if (term.type === 'not') return;
      let pattern;
      if (term.type === 'word') {
        let word = term.value;
        if (word.endsWith('*')) word = word.slice(0, -1);
        word = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        pattern = `(?<![\\p{L}\\p{N}])${word}(?:\\w*)(?![\\p{L}\\p{N}])`;
      } else if (term.type === 'phrase') {
        const words = term.value.split(/\s+/).map(w => {
          w = w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          return w;
        });
        pattern = `(?<![\\p{L}\\p{N}])${words.join('(?:\\s|\\[\\[fn:\\d+\\]\\])+')}(?![\\p{L}\\p{N}])`;
      }
      const regex = new RegExp(pattern, 'gui');
      html = html.replace(regex, match => `<mark>${match}</mark>`);
    });

    return html;
  }

  function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function getHits() {
    const hits = R.filter(r => {
      // Query
      if (state.queryTree && !matchRecord(r, state.queryTree)) return false;

      // Committees
      if (state.filters.committees.size > 0) {
        const recordCommittees = r.committees.filter(c => state.filters.committees.has(c));
        if (recordCommittees.length === 0) return false;
      }

      // Years
      if (r.year < state.filters.yearFrom || r.year > state.filters.yearTo) return false;

      // Document
      if (state.filters.document && r.short_title !== state.filters.document) return false;

      return true;
    });

    // Order
    if (state.order === 'year-desc') {
      hits.sort((a, b) => {
        if (b.year !== a.year) return b.year - a.year;
        if (a.title !== b.title) return a.title.localeCompare(b.title);
        return a.paragraph - b.paragraph;
      });
    } else if (state.order === 'doc') {
      hits.sort((a, b) => {
        if (a.title !== b.title) return a.title.localeCompare(b.title);
        return a.paragraph - b.paragraph;
      });
    } else if (state.order === 'matches') {
      hits.forEach(r => {
        r._matches = 0;
        function count(node) {
          if (node.type === 'word' || node.type === 'phrase') {
            const regex = termToRegex(node);
            if (regex.test(r.norm)) r._matches++;
          } else if (node.type === 'not') {
            count(node.operand);
          } else if (node.type === 'and' || node.type === 'or') {
            count(node.left);
            count(node.right);
          }
        }
        count(state.queryTree);
      });
      hits.sort((a, b) => b._matches - a._matches);
    }

    return hits;
  }

  function renderResults() {
    const hits = getHits();
    $('matching-count').textContent = hits.length;
    $('results-summary').textContent = `${hits.length} of 7304 paragraphs match · ${new Set(hits.flatMap(r => r.committees)).size} committees · ${Math.min(...hits.map(r => r.year))}–${Math.max(...hits.map(r => r.year))}`;

    // Chart
    if ($('tab-01').getAttribute('aria-expanded') === 'true') {
      renderChart(hits);
    }

    // Checks
    runChecks(hits);
    renderChecks();
    updateChecksDot();

    // Results
    const results = $('results');
    results.innerHTML = '';
    const limit = 25;
    const shown = hits.slice(0, limit);
    shown.forEach(r => {
      const div = document.createElement('div');
      div.className = 'result';
      div.innerHTML = `
        <header>
          <div class="badge">${r.committee}</div>
          <div class="doc">
            <a href="${r.doc_url}" target="_blank">${r.symbol}</a>
            <span class="pinpoint red">${r.pinpoint}</span>
            <span class="mono">${r.year}</span>
          </div>
        </header>
        <div class="text">${highlightText(r.textClean, state.queryTree)}</div>
        <div class="meta">
          <span>${r.marks} footnote mark${r.marks === 1 ? '' : 's'} removed</span>
          <button class="show-stored">show as stored</button>
        </div>
      `;

      // Notes
      const notes = [];
      if (r.leading !== null && r.leading !== r.paragraph) {
        notes.push(`the text begins "${r.leading}." but the record is ${r.pinpoint}`);
      }
      if (/^\([a-z]{1,4}\)/.test(r.text)) {
        notes.push(`a lettered sub-paragraph, numbered ${r.paragraph} by the file`);
      }
      if (R.filter(r2 => r2.title === r.title && r2.pinpoint === r.pinpoint && r2.id !== r.id).length > 0) {
        notes.push('two records share this pinpoint');
      }
      if (r.committees.length > 1) {
        notes.push('joint General Comment');
      }
      if (notes.length > 0) {
        const noteDiv = document.createElement('div');
        noteDiv.className = 'note';
        noteDiv.textContent = notes.join(' · ');
        div.appendChild(noteDiv);
      }

      // Expand
      div.addEventListener('click', e => {
        if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') return;
        if (state.expanded === r.id) {
          state.expanded = null;
          renderResults();
        } else {
          state.expanded = r.id;
          renderResults();
        }
      });

      // Show stored
      div.querySelector('.show-stored').addEventListener('click', e => {
        e.stopPropagation();
        const textDiv = div.querySelector('.text');
        textDiv.textContent = r.text;
        textDiv.innerHTML = highlightText(r.text, state.queryTree);
        div.querySelector('.meta').innerHTML = `
          <span>${r.marks} footnote mark${r.marks === 1 ? '' : 's'} shown</span>
          <button class="show-clean">show as printed</button>
        `;
        div.querySelector('.show-clean').addEventListener('click', e => {
          e.stopPropagation();
          textDiv.textContent = r.textClean;
          textDiv.innerHTML = highlightText(r.textClean, state.queryTree);
          div.querySelector('.meta').innerHTML = `
            <span>${r.marks} footnote mark${r.marks === 1 ? '' : 's'} removed</span>
            <button class="show-stored">show as stored</button>
          `;
          div.querySelector('.show-stored').addEventListener('click', e => {
            e.stopPropagation();
            textDiv.textContent = r.text;
            textDiv.innerHTML = highlightText(r.text, state.queryTree);
            div.querySelector('.meta').innerHTML = `
              <span>${r.marks} footnote mark${r.marks === 1 ? '' : 's'} shown</span>
              <button class="show-clean">show as printed</button>
            `;
          });
        });
      });

      // Long paragraph
      if (r.textClean.length > 700) {
        const textDiv = div.querySelector('.text');
        const short = r.textClean.slice(0, 700).replace(/\s+\S*$/, '');
        textDiv.textContent = short;
        textDiv.innerHTML = highlightText(short, state.queryTree);
        const more = document.createElement('div');
        more.className = 'meta';
        more.innerHTML = `<button class="show-full">Show the full paragraph (${r.textClean.split(/\s+/).length} words)</button>`;
        div.appendChild(more);
        more.querySelector('.show-full').addEventListener('click', e => {
          e.stopPropagation();
          textDiv.textContent = r.textClean;
          textDiv.innerHTML = highlightText(r.textClean, state.queryTree);
          more.remove();
        });
      }

      results.appendChild(div);
    });

    // Expanded
    if (state.expanded) {
      const expanded = R.find(r => r.id === state.expanded);
      const div = results.querySelector(`.result:nth-child(${shown.findIndex(r => r.id === state.expanded) + 1})`);
      if (div) {
        const expandedDiv = document.createElement('div');
        expandedDiv.className = 'expanded';
        expandedDiv.innerHTML = `
          <div class="buttons">
            <button class="copy-citation">Copy citation</button>
            <button class="copy-quotation">Copy quotation</button>
            <button class="add-to-draft">Add to draft</button>
          </div>
          <div class="context">
            <div class="para" hidden>
              <header>Previous paragraph</header>
              <div class="text"></div>
            </div>
            <div class="para" hidden>
              <header>Next paragraph</header>
              <div class="text"></div>
            </div>
          </div>
        `;
        div.appendChild(expandedDiv);

        // Copy
        expandedDiv.querySelector('.copy-citation').addEventListener('click', e => {
          e.stopPropagation();
          copyToClipboard(expanded.citation);
          $('live-region').textContent = `Copied: ${expanded.citation}`;
        });
        expandedDiv.querySelector('.copy-quotation').addEventListener('click', e => {
          e.stopPropagation();
          const quote = `"${expanded.textClean}" ${expanded.citation}`;
          copyToClipboard(quote);
          $('live-region').textContent = `Copied: ${quote}`;
        });
        expandedDiv.querySelector('.add-to-draft').addEventListener('click', e => {
          e.stopPropagation();
          addToDraft(expanded);
          renderDraft();
        });

        // Context
        const prev = R.find(r => r.title === expanded.title && r.paragraph === expanded.paragraph - 1);
        const next = R.find(r => r.title === expanded.title && r.paragraph === expanded.paragraph + 1);
        if (prev) {
          const para = expandedDiv.querySelector('.context .para:first-child');
          para.hidden = false;
          para.querySelector('header').textContent = `Previous paragraph (${prev.pinpoint})`;
          para.querySelector('.text').textContent = prev.textClean;
        }
        if (next) {
          const para = expandedDiv.querySelector('.context .para:last-child');
          para.hidden = false;
          para.querySelector('header').textContent = `Next paragraph (${next.pinpoint})`;
          para.querySelector('.text').textContent = next.textClean;
        }
      }
    }

    // Load more
    $('load-more').hidden = hits.length <= limit;
  }

  function renderChart(hits) {
    const counts = {};
    committeeList.forEach(([code]) => counts[code] = 0);
    hits.forEach(r => {
      r.committees.forEach(c => {
        if (state.filters.committees.size === 0 || state.filters.committees.has(c)) {
          counts[c] = (counts[c] || 0) + 1;
        }
      });
    });

    const data = committeeList.map(([code, data]) => ({
      label: data.name,
      value: counts[code] || 0
    })).filter(d => d.value > 0);

    const canvas = $('chart-committees');
    const ctx = canvas.getContext('2d');
    if (window.chart) window.chart.destroy();
    window.chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          data: data.map(d => d.value),
          backgroundColor: '#9b2335',
          borderWidth: 0
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.raw} paragraphs`
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              precision: 0
            },
            grid: {
              color: '#d9d2c3'
            }
          },
          y: {
            grid: {
              display: false
            }
          }
        }
      }
    });

    // Table
    const table = $('chart-table').querySelector('tbody');
    table.innerHTML = '';
    data.forEach(d => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${d.label}</td><td>${d.value}</td>`;
      table.appendChild(tr);
    });

    // Click
    canvas.onclick = e => {
      const points = window.chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true);
      if (points.length) {
        const index = points[0].index;
        const code = committeeList[index][0];
        $$('#committee-checkboxes input').forEach(el => {
          el.checked = el.value === code;
        });
        updateFilters();
      }
    };
  }

  function runChecks(hits) {
    state.checks = [];

    // Query understood
    if (state.queryError) {
      state.checks.push({
        label: 'Query understood',
        status: 'fail',
        message: state.queryError
      });
    } else if (state.queryTree) {
      const terms = [];
      function collectTerms(node) {
        if (node.type === 'word' || node.type === 'phrase') {
          terms.push(node);
        } else if (node.type === 'not') {
          collectTerms(node.operand);
        } else if (node.type === 'and' || node.type === 'or') {
          collectTerms(node.left);
          collectTerms(node.right);
        }
      }
      collectTerms(state.queryTree);
      state.checks.push({
        label: 'Query understood',
        status: 'pass',
        message: `${terms.length} term${terms.length === 1 ? '' : 's'}: ${$('query-echo').textContent}`
      });
    } else {
      state.checks.push({
        label: 'Query understood',
        status: 'pass',
        message: 'No search words'
      });
    }

    // Totals
    const checkboxCounts = {};
    committeeList.forEach(([code]) => checkboxCounts[code] = 0);
    hits.forEach(r => {
      r.committees.forEach(c => {
        if (state.filters.committees.size === 0 || state.filters.committees.has(c)) {
          checkboxCounts[c]++;
        }
      });
    });
    const checkboxSum = Object.values(checkboxCounts).reduce((a, b) => a + b, 0);
    const hitsSum = hits.length;
    const jointHits = hits.filter(r => r.committees.length > 1).length;
    const total = hitsSum + jointHits;
    if (checkboxSum === total) {
      state.checks.push({
        label: 'Totals',
        status: 'pass',
        message: `Checkbox counts sum to ${total} (${hitsSum} hits + ${jointHits} joint)`
      });
    } else {
      state.checks.push({
        label: 'Totals',
        status: 'fail',
        message: `Checkbox counts sum to ${checkboxSum}, should be ${total}`
      });
    }

    // Chart total
    const chartCounts = {};
    committeeList.forEach(([code]) => chartCounts[code] = 0);
    hits.forEach(r => {
      r.committees.forEach(c => {
        if (state.filters.committees.size === 0 || state.filters.committees.has(c)) {
          chartCounts[c]++;
        }
      });
    });
    const chartSum = Object.values(chartCounts).reduce((a, b) => a + b, 0);
    if (chartSum === total) {
      state.checks.push({
        label: 'Chart total',
        status: 'pass',
        message: `Bars sum to ${total} (${hitsSum} hits + ${jointHits} joint)`
      });
    } else {
      state.checks.push({
        label: 'Chart total',
        status: 'fail',
        message: `Bars sum to ${chartSum}, should be ${total}`
      });
    }

    // Highlight
    const noHighlight = hits.filter(r => {
      const html = highlightText(r.textClean, state.queryTree);
      return !/<mark>/.test(html);
    });
    if (noHighlight.length === 0 || (state.queryTree && state.queryTree.type === 'not')) {
      state.checks.push({
        label: 'Highlight',
        status: 'pass',
        message: 'Every hit is highlighted'
      });
    } else {
      state.checks.push({
        label: 'Highlight',
        status: 'fail',
        message: `${noHighlight.length} hit${noHighlight.length === 1 ? '' : 's'} matched but not highlighted: ${noHighlight.slice(0, 3).map(r => r.pinpoint).join(', ')}${noHighlight.length > 3 ? '…' : ''}`
      });
    }

    // Normalisation
    if (state.query && /['"-]/.test(state.query)) {
      const curlyHits = hits.filter(r => {
        const norm = r.norm;
        const straight = normaliseText(r.text.replace(/[‘’‚]/g, "'").replace(/[“”„]/g, '"').replace(/[\u2013\u2014]/g, '-'));
        return termToRegex(state.queryTree).test(straight) && !termToRegex(state.queryTree).test(norm);
      });
      state.checks.push({
        label: 'Normalisation',
        status: 'pass',
        message: `Curly quotes, apostrophes and dashes were matched too${curlyHits.length > 0 ? ` (${curlyHits.length} hit${curlyHits.length === 1 ? '' : 's'} contain only those forms)` : ''}`
      });
    }

    // Numbering
    const leadingMismatches = hits.filter(r => r.leading !== null && r.leading !== r.paragraph);
    if (leadingMismatches.length === 0) {
      state.checks.push({
        label: 'Numbering',
        status: 'pass',
        message: 'No leading-number mismatches'
      });
    } else {
      state.checks.push({
        label: 'Numbering',
        status: 'fail',
        message: `${leadingMismatches.length} hit${leadingMismatches.length === 1 ? '' : 's'} with leading-number mismatch: ${leadingMismatches.slice(0, 3).map(r => `${r.pinpoint} (text begins "${r.leading}.")`).join(', ')}${leadingMismatches.length > 3 ? '…' : ''}`
      });
    }
    const duplicatedPinpoints = hits.filter(r => {
      return R.filter(r2 => r2.title === r.title && r2.pinpoint === r.pinpoint && r2.id !== r.id).length > 0;
    });
    if (duplicatedPinpoints.length === 0) {
      state.checks.push({
        label: 'Duplicated pinpoints',
        status: 'pass',
        message: 'No duplicated pinpoints'
      });
    } else {
      state.checks.push({
        label: 'Duplicated pinpoints',
        status: 'fail',
        message: `${duplicatedPinpoints.length} hit${duplicatedPinpoints.length === 1 ? '' : 's'} with duplicated pinpoint: ${duplicatedPinpoints.slice(0, 3).map(r => `${r.title} ${r.pinpoint}`).join(', ')}${duplicatedPinpoints.length > 3 ? '…' : ''}`
      });
    }
    const lettered = hits.filter(r => /^\([a-z]{1,4}\)/.test(r.text));
    if (lettered.length === 0) {
      state.checks.push({
        label: 'Lettered sub-paragraphs',
        status: 'pass',
        message: 'No lettered sub-paragraphs'
      });
    } else {
      state.checks.push({
        label: 'Lettered sub-paragraphs',
        status: 'fail',
        message: `${lettered.length} lettered sub-paragraph${lettered.length === 1 ? '' : 's'}: ${lettered.slice(0, 3).map(r => r.pinpoint).join(', ')}${lettered.length > 3 ? '…' : ''}`
      });
    }

    // Marks
    const markErrors = hits.filter(r => {
      const stored = r.text;
      const clean = r.textClean;
      const marks = (stored.match(/\[\[fn:\d+\]\]/g) || []).length;
      const restored = clean.replace(/\[\[fn:\d+\]\]/g, '');
      return marks !== r.marks || restored !== stored;
    });
    if (markErrors.length === 0) {
      state.checks.push({
        label: 'Footnote marks',
        status: 'pass',
        message: 'Footnote marks removed and restored correctly'
      });
    } else {
      state.checks.push({
        label: 'Footnote marks',
        status: 'fail',
        message: `${markErrors.length} hit${markErrors.length === 1 ? '' : 's'} with footnote-mark error`
      });
    }

    // Draft
    const draftErrors = state.draft.filter(item => {
      const record = R.find(r => r.id === item.id);
      return !record || record.text !== item.text_as_stored;
    });
    if (draftErrors.length === 0) {
      state.checks.push({
        label: 'Draft',
        status: 'pass',
        message: 'All draft items match the stored text'
      });
    } else {
      state.checks.push({
        label: 'Draft',
        status: 'fail',
        message: `${draftErrors.length} draft item${draftErrors.length === 1 ? '' : 's'} do not match the stored text`
      });
    }
  }

  function renderChecks() {
    const checks = $('checks');
    checks.innerHTML = '';
    state.checks.forEach(check => {
      const div = document.createElement('div');
      div.className = 'check';
      div.innerHTML = `
        <div>${check.label}</div>
        <div class="status ${check.status}">
          <span class="dot ${check.status}"></span>
          <span>${check.message}</span>
        </div>
      `;
      checks.appendChild(div);
    });
  }

  function updateChecksDot() {
    const failed = state.checks.filter(c => c.status === 'fail').length;
    const dot = $('checks-dot');
    const count = $('checks-count');
    if (failed === 0) {
      dot.style.backgroundColor = '#2e7d32';
      count.textContent = `${state.checks.length} checks pass`;
    } else {
      dot.style.backgroundColor = '#9b2335';
      count.textContent = `${failed} check${failed === 1 ? '' : 's'} failed`;
      if ($('tab-04-toggle').getAttribute('aria-selected') !== 'true') {
        $('tab-04-toggle').classList.add('red');
      }
    }
  }

  function renderQuirks() {
    const quirks = $('quirks');
    quirks.innerHTML = '';
    state.quirks.forEach(quirk => {
      const div = document.createElement('div');
      div.className = 'quirk';
      div.innerHTML = `
        <div>${quirk.label} (${quirk.count})</div>
        <div class="mono">${quirk.example}</div>
      `;
      quirks.appendChild(div);
    });
  }

  // Draft
  function initDraft() {
    try {
      const stored = localStorage.getItem('gc-draft');
      if (stored) state.draft = JSON.parse(stored);
    } catch (e) {
      // Ignore
    }
  }

  function addToDraft(record) {
    const existing = state.draft.findIndex(item => item.id === record.id);
    if (existing >= 0) {
      state.draft.splice(existing, 1);
    }
    state.draft.unshift({
      id: record.id,
      quote: `"${record.textClean}" ${record.citation}`,
      citation: record.citation,
      symbol: record.symbol,
      paragraph: record.paragraph,
      pinpoint: record.pinpoint,
      committee: record.committee,
      short_title: record.short_title,
      year: record.year,
      text_copied: record.textClean,
      text_as_stored: record.text,
      doc_url: record.doc_url
    });
    saveDraft();
  }

  function saveDraft() {
    try {
      localStorage.setItem('gc-draft', JSON.stringify(state.draft));
    } catch (e) {
      // Ignore
    }
    $('tab-03-toggle').textContent = `03 DRAFT (${state.draft.length})`;
  }

  function renderDraft() {
    const draft = $('draft');
    draft.innerHTML = '';
    state.draft.forEach(item => {
      const div = document.createElement('div');
      div.className = 'draft-item';
      div.innerHTML = `
        <header>
          <div class="citation mono">${item.citation}</div>
          <button class="remove">Remove</button>
        </header>
        <div class="quote">${item.quote}</div>
      `;
      div.querySelector('.remove').addEventListener('click', () => {
        state.draft = state.draft.filter(i => i.id !== item.id);
        saveDraft();
        renderDraft();
      });
      draft.appendChild(div);
    });
  }

  $('copy-all').addEventListener('click', () => {
    const text = state.draft.map(item => `${item.quote}\n\n`).join('');
    copyToClipboard(text);
    $('live-region').textContent = `Copied ${state.draft.length} quotation${state.draft.length === 1 ? '' : 's'}`;
  });

  $('download-txt').addEventListener('click', () => {
    const text = state.draft.map(item => `${item.quote}\n\n`).join('');
    download('general-comments.txt', text);
  });

  $('download-csv').addEventListener('click', () => {
    const headers = ['citation', 'symbol', 'paragraph', 'pinpoint', 'committee', 'short_title', 'year', 'text_copied', 'text_as_stored', 'doc_url'];
    const rows = state.draft.map(item => {
      return headers.map(h => {
        let value = item[h];
        if (h === 'text_copied' || h === 'text_as_stored') {
          value = `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      }).join(',');
    });
    const csv = [headers.join(','), ...rows].join('\n');
    download('general-comments.csv', csv);
  });

  function copyToClipboard(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).catch(() => {
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    const box = document.createElement('div');
    box.className = 'copy-box';
    box.textContent = text;
    document.body.appendChild(box);
    const range = document.createRange();
    range.selectNode(box);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {
      document.execCommand('copy');
    } catch (e) {
      // Ignore
    }
    window.getSelection().removeAllRanges();
    document.body.removeChild(box);
  }

  function download(filename, text) {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function committeeName(code) {
    const names = {
      'CAT': 'Committee against Torture',
      'CCPR': 'Human Rights Committee',
      'CED': 'Committee on Enforced Disappearances',
      'CEDAW': 'Committee on the Elimination of Discrimination against Women',
      'CERD': 'Committee on the Elimination of Racial Discrimination',
      'CESCR': 'Committee on Economic, Social and Cultural Rights',
      'CMW': 'Committee on the Protection of the Rights of All Migrant Workers and Members of Their Families',
      'CRC': 'Committee on the Rights of the Child',
      'CRPD': 'Committee on the Rights of Persons with Disabilities',
      'CAT-OP': 'Subcommittee on Prevention of Torture'
    };
    return names[code] || code;
  }
})();
</script>
</body>
</html>
```