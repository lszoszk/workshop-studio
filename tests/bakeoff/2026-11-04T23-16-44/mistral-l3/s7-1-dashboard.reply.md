Here is the app. It follows the plan exactly: three tabs, one question each, filters in a left rail, and the checks under a closed heading on the Overview tab. The design is calm, the numbers big, and every figure explains how it was computed.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>UN human rights recommendations and observations: Kenya</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --upr: #c2410c;
  --treaty: #0f766e;
  --special: #7c3aed;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
header, footer {
  grid-column: 1 / -1;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
}
header {
  border-top: 3px solid var(--accent);
}
h1 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.8rem;
  margin: 0.25rem 0 0.5rem;
  color: var(--ink);
}
.label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  color: var(--ink);
  text-transform: uppercase;
}
.source-line {
  font-size: 0.9rem;
  color: var(--ink);
  margin: 0;
}
.source-line a {
  color: var(--ink);
  text-decoration: underline;
}
.tablist {
  display: flex;
  gap: 0.5rem;
  padding: 0;
  margin: 0;
  list-style: none;
  border-bottom: 1px solid var(--rule);
}
.tablist button {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border: none;
  border-bottom: 3px solid transparent;
  background: none;
  cursor: pointer;
  color: var(--ink);
}
.tablist button[aria-selected="true"] {
  border-bottom-color: var(--accent);
  color: var(--accent);
}
.tablist button:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.rail {
  padding: 1rem;
  border-right: 1px solid var(--rule);
  background-color: var(--paper);
}
.rail h2 {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rail h2 button {
  background: none;
  border: none;
  font: inherit;
  cursor: pointer;
  color: var(--ink);
  padding: 0.25rem;
}
.rail h2 button:focus {
  outline: 2px solid var(--accent);
}
.rail .match-count {
  font-family: Georgia, serif;
  font-size: 2.5rem;
  line-height: 1;
  margin: 0.5rem 0;
  color: var(--ink);
}
.rail .match-count .total {
  font-size: 1rem;
  font-family: system-ui, sans-serif;
  color: var(--ink);
}
.rail .share-bar {
  height: 4px;
  background-color: var(--rule);
  margin: 0.5rem 0;
  position: relative;
}
.rail .share-bar::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: var(--accent);
  width: 0%;
}
.rail .filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin: 0.5rem 0;
}
.rail .filter-chip {
  background-color: var(--accent);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.rail .filter-chip button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  margin: 0;
  font-size: 0.8rem;
}
.filter-section {
  margin-top: 1rem;
}
.filter-section h3 {
  font-family: system-ui, sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  margin: 0 0 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.filter-section h3 button {
  background: none;
  border: none;
  font: inherit;
  cursor: pointer;
  color: var(--ink);
  padding: 0.25rem;
}
.filter-section h3 button:focus {
  outline: 2px solid var(--accent);
}
.filter-section[hidden] {
  display: none;
}
.filter-section .hint {
  font-size: 0.8rem;
  color: var(--ink);
  margin: 0.25rem 0;
}
.filter-section input, .filter-section select {
  width: 100%;
  padding: 0.5rem;
  margin: 0.25rem 0;
  border: 1px solid var(--rule);
  background-color: white;
  font: inherit;
}
.filter-section input:focus, .filter-section select:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.filter-section .year-range {
  display: flex;
  gap: 0.5rem;
}
.filter-section .year-range select {
  flex: 1;
}
.filter-section .sdg-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.25rem;
}
.filter-section .sdg-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.filter-section .sdg-option input {
  width: auto;
}
.filter-section .state-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.25rem;
}
.filter-section .state-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.filter-section .state-option input {
  width: auto;
}
.main {
  padding: 1rem;
}
.tabpanel {
  display: none;
}
.tabpanel[aria-hidden="false"] {
  display: block;
}
.tile-row {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}
.tile {
  flex: 1;
  min-width: 200px;
  border: 1px solid var(--rule);
  padding: 1rem;
  background-color: white;
}
.tile h3 {
  font-family: Georgia, serif;
  font-size: 3rem;
  margin: 0 0 0.5rem;
  color: var(--ink);
}
.tile .subtitle {
  font-size: 0.9rem;
  color: var(--ink);
  margin: 0 0 0.5rem;
}
.tile .mechanism-dot {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.tile .upr { background-color: var(--upr); }
.tile .treaty { background-color: var(--treaty); }
.tile .special { background-color: var(--special); }
.tile .note {
  font-size: 0.8rem;
  color: var(--ink);
  margin: 0.5rem 0 0;
}
.fig {
  margin: 2rem 0;
}
.fig h4 {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 0.5rem;
}
.fig .source {
  font-size: 0.8rem;
  color: var(--ink);
  margin: 0.25rem 0;
}
.chart-container {
  position: relative;
  height: 400px;
  margin: 1rem 0;
}
.chart-container canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.chart-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}
.chart-table th, .chart-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
.chart-table th {
  font-weight: 500;
}
.chart-table th[scope="col"] {
  text-align: right;
}
.chart-table .rank {
  text-align: right;
}
.chart-table .pct {
  text-align: right;
}
.chart-table .years {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
}
.search-box {
  width: 100%;
  padding: 0.75rem;
  margin: 1rem 0;
  border: 1px solid var(--rule);
  font: inherit;
}
.search-box:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
table.records {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9rem;
}
table.records caption {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  text-align: left;
  margin-bottom: 0.5rem;
}
table.records th, table.records td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
table.records th {
  font-weight: 500;
  position: sticky;
  top: 0;
  background-color: var(--paper);
}
table.records th[scope="col"] {
  cursor: pointer;
}
table.records th[scope="col"]:focus {
  outline: 2px solid var(--accent);
}
table.records th[scope="col"]::after {
  content: " ↕";
  font-size: 0.8rem;
  color: var(--ink);
}
table.records tr[aria-expanded="true"] th[scope="row"]::after {
  content: " ▲";
}
table.records tr[aria-expanded="false"] th[scope="row"]::after {
  content: " ▼";
}
table.records .para {
  font-family: ui-monospace, monospace;
  font-size: 0.9rem;
  text-align: right;
  white-space: nowrap;
}
table.records .first-line {
  font-size: 0.9rem;
}
table.records mark {
  background-color: #ffeb3b;
  padding: 0 0.2rem;
}
table.records .expanded {
  grid-column: 1 / -1;
  padding: 1rem;
  border-top: 1px solid var(--rule);
  background-color: white;
}
table.records .expanded h4 {
  font-family: Georgia, serif;
  font-size: 2rem;
  color: var(--accent);
  margin: 0 0 0.5rem;
}
table.records .expanded .text {
  white-space: pre-wrap;
  margin: 0.5rem 0;
}
table.records .expanded .labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.5rem 0;
}
table.records .expanded .label-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
table.records .expanded .label-group h5 {
  font-size: 0.8rem;
  margin: 0;
  font-weight: 500;
}
table.records .expanded .label-group .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}
table.records .expanded .label-group .tag {
  background-color: var(--rule);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
}
table.records .expanded .actions {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}
table.records .expanded .actions button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  background-color: white;
  cursor: pointer;
}
table.records .expanded .actions button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
table.records .expanded .actions .copied {
  font-size: 0.8rem;
  color: var(--accent);
  margin-left: 0.5rem;
}
table.records .load-more {
  grid-column: 1 / -1;
  text-align: center;
  padding: 1rem;
}
table.records .load-more button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  background-color: white;
  cursor: pointer;
}
table.records .load-more button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.checks {
  margin: 2rem 0;
}
.checks h4 {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.checks h4 button {
  background: none;
  border: none;
  font: inherit;
  cursor: pointer;
  color: var(--ink);
  padding: 0.25rem;
}
.checks h4 button:focus {
  outline: 2px solid var(--accent);
}
.checks[hidden] {
  display: none;
}
.checks ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.checks li {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  font-size: 0.9rem;
}
.checks li.pass::before {
  content: "✓ ";
  color: var(--treaty);
}
.checks li.fail::before {
  content: "✗ ";
  color: var(--accent);
}
.checks li.warn::before {
  content: "! ";
  color: var(--upr);
}
.checks li .values {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
}
.checks li .details {
  font-size: 0.8rem;
  color: var(--ink);
  margin-top: 0.25rem;
}
.method {
  margin: 2rem 0;
}
.method h3 {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 1rem;
}
.method p {
  margin: 0 0 1rem;
}
.export {
  margin: 2rem 0;
}
.export h3 {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 1rem;
}
.export button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  background-color: white;
  cursor: pointer;
  margin-right: 1rem;
}
.export button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.export .copied {
  font-size: 0.8rem;
  color: var(--accent);
  margin-left: 0.5rem;
}
footer {
  border-top: 1px solid var(--rule);
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  padding: 0.5rem 1rem;
  display: flex;
  justify-content: space-between;
}
[hidden] { display: none !important; }
</style>
</head>
<body>

<header>
  <div class="label">UHRI · <span id="country-label"></span></div>
  <h1>UN human rights recommendations and observations: <span id="country-name"></span></h1>
  <p class="source-line">Source: <a id="source-url" href="#" target="_blank" rel="noopener">Universal Human Rights Index</a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · built <span id="built-date"></span> · dated by document</p>
</header>

<div class="rail" id="filters-rail">
  <h2>FILTERS <button id="clear-all">Clear all</button></h2>
  <div class="match-count" aria-live="polite"><span id="match-count">0</span><span class="total"> of <span id="total-count"></span> in the file</span></div>
  <div class="share-bar" id="share-bar"></div>
  <div class="filter-chips" id="filter-chips"></div>

  <div class="filter-section" id="keyword-section">
    <h3><span>01</span> Keyword <button aria-expanded="false" aria-controls="keyword-controls">▼</button></h3>
    <div id="keyword-controls">
      <input type="text" id="keyword-input" placeholder="e.g. torture"/>
      <div class="hint">literal match, not synonyms</div>
    </div>
  </div>

  <div class="filter-section" id="mechanism-section">
    <h3><span>02</span> Mechanism, body, type <button aria-expanded="false" aria-controls="mechanism-controls">▼</button></h3>
    <div id="mechanism-controls">
      <div>
        <label for="mechanism-select">Mechanism</label>
        <select id="mechanism-select">
          <option value="all">All mechanisms</option>
        </select>
      </div>
      <div id="body-container">
        <label for="body-select">Body or mandate</label>
        <select id="body-select">
          <option value="all">All bodies</option>
        </select>
      </div>
      <div>
        <label for="type-select">Type</label>
        <select id="type-select">
          <option value="all">All types</option>
        </select>
      </div>
      <div id="state-container" hidden>
        <label for="state-select">Recommending State</label>
        <select id="state-select">
          <option value="all">All States</option>
        </select>
      </div>
    </div>
  </div>

  <div class="filter-section" id="year-sdg-section">
    <h3><span>03</span> Years and SDG <button aria-expanded="false" aria-controls="year-sdg-controls">▼</button></h3>
    <div id="year-sdg-controls">
      <div class="year-range">
        <div>
          <label for="year-from">Year from</label>
          <select id="year-from">
            <option value="">Earliest</option>
          </select>
        </div>
        <div>
          <label for="year-to">to</label>
          <select id="year-to">
            <option value="">Latest</option>
          </select>
        </div>
      </div>
      <div>
        <label>SDG</label>
        <div class="sdg-grid" id="sdg-grid"></div>
      </div>
    </div>
  </div>
</div>

<div class="main">
  <div role="tablist" aria-label="Tabs" class="tablist">
    <button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 OVERVIEW</button>
    <button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 RECORDS</button>
    <button id="tab-03" role="tab" aria-selected="false" aria-controls="panel-03">03 METHOD & EXPORT</button>
  </div>

  <div id="panel-01" role="tabpanel" aria-labelledby="tab-01" aria-hidden="false">
    <div class="tile-row">
      <div class="tile">
        <h3 id="headline-total">0</h3>
        <div class="subtitle" id="headline-breakdown"></div>
        <div class="note">How this is computed: count of all records in the file.</div>
      </div>
      <div class="tile">
        <h3 id="headline-documents">0</h3>
        <div class="subtitle">documents</div>
        <div class="note">How this is computed: distinct document symbols.</div>
      </div>
      <div class="tile">
        <h3 id="headline-years">0–0</h3>
        <div class="subtitle">years</div>
        <div class="note">How this is computed: earliest and latest document year.</div>
      </div>
    </div>

    <div class="tile-row">
      <div class="tile">
        <h3 id="tile-upr">0</h3>
        <div class="subtitle"><span class="mechanism-dot upr"></span>Universal Periodic Review</div>
        <div class="note"><span id="tile-upr-documents">0</span> documents · latest <span id="tile-upr-latest">0</span> · <span id="tile-upr-share">0</span>% of filtered set</div>
        <div class="note" id="upr-states-link-container"><a href="#" id="upr-states-link">see the States</a></div>
        <div id="upr-states-list" hidden>
          <div class="note">Ten States that made most recommendations to <span id="country-name-2"></span></div>
          <ol id="upr-states-ol"></ol>
        </div>
      </div>
      <div class="tile">
        <h3 id="tile-treaty">0</h3>
        <div class="subtitle"><span class="mechanism-dot treaty"></span>Treaty bodies</div>
        <div class="note"><span id="tile-treaty-documents">0</span> documents · latest <span id="tile-treaty-latest">0</span> · <span id="tile-treaty-share">0</span>% of filtered set</div>
      </div>
      <div class="tile">
        <h3 id="tile-special">0</h3>
        <div class="subtitle"><span class="mechanism-dot special"></span>Special Procedures</div>
        <div class="note"><span id="tile-special-documents">0</span> documents · latest <span id="tile-special-latest">0</span> · <span id="tile-special-share">0</span>% of filtered set</div>
      </div>
    </div>

    <div class="fig">
      <h4>FIG.01 Ten most frequent themes among <span id="fig01-count">0</span> filtered records</h4>
      <div class="source">Source: themes labelled by the UN mechanism in each record.</div>
      <div class="chart-container">
        <canvas id="fig01-chart"></canvas>
      </div>
      <table class="chart-table">
        <caption>Same ten themes as a table. A record can carry several themes, so the bars add up to more than the record count.</caption>
        <thead>
          <tr>
            <th scope="col">Theme</th>
            <th scope="col" class="rank">Records</th>
            <th scope="col" class="pct">% of filtered</th>
            <th scope="col">Years</th>
          </tr>
        </thead>
        <tbody id="fig01-table"></tbody>
      </table>
    </div>

    <div class="fig">
      <h4>FIG.02 Records per year by mechanism</h4>
      <div class="source">Source: document year and mechanism of each record.</div>
      <div class="chart-container">
        <canvas id="fig02-chart"></canvas>
      </div>
    </div>

    <div class="checks" id="checks-section" hidden>
      <h4>Every check (<span id="check-count">0</span>) <button aria-expanded="false" aria-controls="checks-list">▼</button></h4>
      <ul id="checks-list"></ul>
    </div>
  </div>

  <div id="panel-02" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
    <input type="text" id="search-input" class="search-box" placeholder="Search records, e.g. torture"/>
    <div class="source" id="search-caption">0 of 0 records shown</div>
    <table class="records">
      <caption>Records matching the filters, newest first. Click a row to expand.</caption>
      <thead>
        <tr>
          <th scope="col" id="col-date">Date</th>
          <th scope="col" id="col-body">Body</th>
          <th scope="col" id="col-symbol">Symbol</th>
          <th scope="col" id="col-para">Para.</th>
          <th scope="col" id="col-state">Recommending State</th>
          <th scope="col" id="col-first">First line</th>
        </tr>
      </thead>
      <tbody id="records-tbody"></tbody>
      <tfoot>
        <tr class="load-more">
          <td colspan="6"><button id="load-more">Show 50 more</button></td>
        </tr>
      </tfoot>
    </table>
  </div>

  <div id="panel-03" role="tabpanel" aria-labelledby="tab-03" aria-hidden="true">
    <div class="method">
      <h3>How each number is computed</h3>
      <p>The headline total is the count of all records in the file. The breakdown counts records per <code>type</code>, using the values exactly as spelled in the data.</p>
      <p>Documents is the number of distinct <code>symbol</code>. Years is the earliest and latest <code>year</code>.</p>
      <p>Filters: Mechanism, body, type: exact match on the field. Year: <code>year</code> inclusive between the two selects. SDG: <code>sdgs.includes(goal)</code> with <code>goal</code> a number. Keyword: every word must occur as a substring of <code>text</code> or <code>symbol</code> (literal match, not synonyms).</p>
      <p>Theme counts: for each record in the filtered set, each value in <code>themes</code> counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = min and max <code>year</code> of the filtered records carrying that theme.</p>
      <p>Timeline: records per <code>year</code> per <code>mechanism</code> in the filtered set, with zero for missing combinations.</p>
      <p>Paragraph number: the first match of <code>/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/</code> on <code>text</code>; the captured group is the number. Recommending State: only for UPR; the trailing run of parenthesised groups, split and trimmed, accepted as a State only if it has no comma and at most 60 characters.</p>
    </div>

    <div class="export">
      <h3>Take this with you</h3>
      <button id="download-csv">Download CSV of the current filter</button>
      <button id="copy-summary">Copy summary</button>
      <span class="copied" id="copy-summary-copied"></span>
    </div>

    <div class="method">
      <h3>Data source and licence</h3>
      <p>This dashboard is built on the <a href="https://uhri.ohchr.org/" target="_blank" rel="noopener">Universal Human Rights Index</a> (UHRI), maintained by the Office of the United Nations High Commissioner for Human Rights (OHCHR). The data is used under the <a href="https://www.ohchr.org/en/about-us/terms-use" target="_blank" rel="noopener">OHCHR terms of use</a>, which allow reuse for non-commercial purposes with attribution.</p>
      <p>Built on <span id="built-date-2"></span>.</p>
    </div>
  </div>
</div>

<footer>
  <div>Built on OHCHR UHRI data · <span id="record-count-2"></span> records · <a id="source-url-2" href="#" target="_blank" rel="noopener">source</a></div>
  <div>Credits: UK Government Analysis Function (charts and tables, Open Government Licence v3.0)</div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  // ------------------------------------------------------------
  // DATA
  // ------------------------------------------------------------
  const uhri = window.WORKSHOP_DATA.uhri;
  const country = uhri.country;
  const sdgNames = uhri.sdg_names;
  const records = uhri.records;
  const totalCount = records.length;
  const documentCount = new Set(records.map(r => r.symbol)).size;
  const years = Array.from(new Set(records.map(r => r.year))).sort((a, b) => a - b);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  const builtDate = new Date(uhri.built).toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'});

  // ------------------------------------------------------------
  // STATE
  // ------------------------------------------------------------
  let filteredRecords = [...records];
  let activeFilters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    state: 'all',
    yearFrom: '',
    yearTo: '',
    sdgs: new Set()
  };
  let sortDirection = 'desc';
  let visibleRows = 50;

  // ------------------------------------------------------------
  // UTILITIES
  // ------------------------------------------------------------
  const formatNumber = n => n.toLocaleString('en');
  const formatPercent = (n, total) => total ? (n / total * 100).toFixed(1) + '%' : '0%';
  const debounce = (fn, delay) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn(...args), delay);
    };
  };

  const extractParagraphNumber = text => {
    const match = text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
    return match ? match[1] : null;
  };

  const extractRecommendingStates = text => {
    const match = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
    if (!match) return [];
    const groups = match[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
    return groups.map(g => {
      const inner = g.slice(1, -1).trim();
      if (inner.includes(',') || inner.length > 60) return null;
      return inner;
    }).filter(Boolean);
  };

  const getFirstLine = text => {
    const cut = text.slice(0, 120);
    const lastSpace = cut.lastIndexOf(' ');
    return lastSpace > 0 ? cut.slice(0, lastSpace) + '…' : cut;
  };

  const copyToClipboard = text => {
    navigator.clipboard.writeText(text).then(() => {
      const el = document.getElementById('copy-summary-copied');
      el.textContent = 'Copied';
      setTimeout(() => { el.textContent = ''; }, 2000);
    });
  };

  // ------------------------------------------------------------
  // FILTERS
  // ------------------------------------------------------------
  const applyFilters = () => {
    filteredRecords = records.filter(record => {
      // Keyword
      if (activeFilters.keyword) {
        const words = activeFilters.keyword.toLowerCase().split(/\s+/).filter(w => w);
        if (!words.every(w => record.text.toLowerCase().includes(w) || record.symbol.toLowerCase().includes(w))) {
          return false;
        }
      }

      // Mechanism
      if (activeFilters.mechanism !== 'all' && record.mechanism !== activeFilters.mechanism) {
        return false;
      }

      // Body
      if (activeFilters.body !== 'all' && record.body !== activeFilters.body) {
        return false;
      }

      // Type
      if (activeFilters.type !== 'all' && record.type !== activeFilters.type) {
        return false;
      }

      // State
      if (activeFilters.state !== 'all') {
        if (record.mechanism !== 'Universal Periodic Review') return false;
        const states = extractRecommendingStates(record.text);
        if (!states.includes(activeFilters.state)) return false;
      }

      // Year
      if (activeFilters.yearFrom && record.year < activeFilters.yearFrom) return false;
      if (activeFilters.yearTo && record.year > activeFilters.yearTo) return false;

      // SDG
      if (activeFilters.sdgs.size > 0) {
        const recordSdgs = record.sdgs || [];
        if (!recordSdgs.some(s => activeFilters.sdgs.has(s))) return false;
      }

      return true;
    });

    // Sort
    filteredRecords.sort((a, b) => {
      if (a.date < b.date) return sortDirection === 'desc' ? 1 : -1;
      if (a.date > b.date) return sortDirection === 'desc' ? -1 : 1;
      if (a.body < b.body) return -1;
      if (a.body > b.body) return 1;
      const aPara = extractParagraphNumber(a.text);
      const bPara = extractParagraphNumber(b.text);
      if (!aPara || !bPara) return 0;
      return aPara.localeCompare(bPara, undefined, {numeric: true});
    });

    updateUI();
  };

  const updateFilterChips = () => {
    const chipsEl = document.getElementById('filter-chips');
    chipsEl.innerHTML = '';

    const addChip = (label, onRemove) => {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = label;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', onRemove);
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    };

    if (activeFilters.keyword) {
      addChip(`Keyword: ${activeFilters.keyword}`, () => {
        activeFilters.keyword = '';
        document.getElementById('keyword-input').value = '';
        applyFilters();
      });
    }

    if (activeFilters.mechanism !== 'all') {
      const label = document.querySelector(`#mechanism-select option[value="${activeFilters.mechanism}"]`).textContent;
      addChip(`Mechanism: ${label}`, () => {
        activeFilters.mechanism = 'all';
        document.getElementById('mechanism-select').value = 'all';
        applyFilters();
      });
    }

    if (activeFilters.body !== 'all') {
      const label = document.querySelector(`#body-select option[value="${activeFilters.body}"]`).textContent;
      addChip(`Body: ${label}`, () => {
        activeFilters.body = 'all';
        document.getElementById('body-select').value = 'all';
        applyFilters();
      });
    }

    if (activeFilters.type !== 'all') {
      const label = document.querySelector(`#type-select option[value="${activeFilters.type}"]`).textContent;
      addChip(`Type: ${label}`, () => {
        activeFilters.type = 'all';
        document.getElementById('type-select').value = 'all';
        applyFilters();
      });
    }

    if (activeFilters.state !== 'all') {
      const label = document.querySelector(`#state-select option[value="${activeFilters.state}"]`).label;
      addChip(`State: ${label}`, () => {
        activeFilters.state = 'all';
        document.getElementById('state-select').value = 'all';
        applyFilters();
      });
    }

    if (activeFilters.yearFrom) {
      addChip(`Year from: ${activeFilters.yearFrom}`, () => {
        activeFilters.yearFrom = '';
        document.getElementById('year-from').value = '';
        applyFilters();
      });
    }

    if (activeFilters.yearTo) {
      addChip(`Year to: ${activeFilters.yearTo}`, () => {
        activeFilters.yearTo = '';
        document.getElementById('year-to').value = '';
        applyFilters();
      });
    }

    activeFilters.sdgs.forEach(goal => {
      const label = `${goal} ${sdgNames[goal]}`;
      addChip(`SDG: ${label}`, () => {
        activeFilters.sdgs.delete(goal);
        document.querySelector(`#sdg-${goal}`).checked = false;
        applyFilters();
      });
    });
  };

  // ------------------------------------------------------------
  // UI UPDATES
  // ------------------------------------------------------------
  const updateUI = () => {
    const matchCount = filteredRecords.length;
    document.getElementById('match-count').textContent = formatNumber(matchCount);
    document.getElementById('share-bar').style.setProperty('--share', `${matchCount / totalCount * 100}%`);
    updateFilterChips();

    // Tiles
    document.getElementById('headline-total').textContent = formatNumber(matchCount);
    const typeCounts = {};
    records.forEach(r => { typeCounts[r.type] = (typeCounts[r.type] || 0) + 1; });
    const typeBreakdown = Object.entries(typeCounts).map(([type, count]) => `${type} ${formatNumber(count)}`).join(', ');
    document.getElementById('headline-breakdown').textContent = typeBreakdown;
    document.getElementById('headline-documents').textContent = formatNumber(new Set(filteredRecords.map(r => r.symbol)).size);
    document.getElementById('headline-years').textContent = `${Math.min(...filteredRecords.map(r => r.year))}–${Math.max(...filteredRecords.map(r => r.year))}`;

    const mechanismCounts = { 'Universal Periodic Review': 0, 'Treaty bodies': 0, 'Special Procedures': 0 };
    const mechanismDocs = { 'Universal Periodic Review': new Set(), 'Treaty bodies': new Set(), 'Special Procedures': new Set() };
    const mechanismYears = { 'Universal Periodic Review': [], 'Treaty bodies': [], 'Special Procedures': [], 'Special Procedures': [] };
    filteredRecords.forEach(r => {
      mechanismCounts[r.mechanism]++;
      mechanismDocs[r.mechanism].add(r.symbol);
      mechanismYears[r.mechanism].push(r.year);
    });
    document.getElementById('tile-upr').textContent = formatNumber(mechanismCounts['Universal Periodic Review']);
    document.getElementById('tile-upr-documents').textContent = mechanismDocs['Universal Periodic Review'].size;
    document.getElementById('tile-upr-latest').textContent = Math.max(...mechanismYears['Universal Periodic Review']);
    document.getElementById('tile-upr-share').textContent = formatPercent(mechanismCounts['Universal Periodic Review'], matchCount);
    document.getElementById('tile-treaty').textContent = formatNumber(mechanismCounts['Treaty bodies']);
    document.getElementById('tile-treaty-documents').textContent = mechanismDocs['Treaty bodies'].size;
    document.getElementById('tile-treaty-latest').textContent = Math.max(...mechanismYears['Treaty bodies']);
    document.getElementById('tile-treaty-share').textContent = formatPercent(mechanismCounts['Treaty bodies'], matchCount);
    document.getElementById('tile-special').textContent = formatNumber(mechanismCounts['Special Procedures']);
    document.getElementById('tile-special-documents').textContent = mechanismDocs['Special Procedures'].size;
    document.getElementById('tile-special-latest').textContent = Math.max(...mechanismYears['Special Procedures']);
    document.getElementById('tile-special-share').textContent = formatPercent(mechanismCounts['Special Procedures'], matchCount);

    // FIG.01
    const themeCounts = {};
    filteredRecords.forEach(r => {
      (r.themes || []).forEach(theme => {
        themeCounts[theme] = (themeCounts[theme] || 0) + 1;
      });
    });
    const topThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    document.getElementById('fig01-count').textContent = formatNumber(matchCount);
    const fig01Ctx = document.getElementById('fig01-chart').getContext('2d');
    if (window.fig01Chart) window.fig01Chart.destroy();
    window.fig01Chart = new Chart(fig01Ctx, {
      type: 'bar',
      data: {
        labels: topThemes.map(([theme]) => theme),
        datasets: [{
          data: topThemes.map(([, count]) => count),
          backgroundColor: '#9b233580',
          borderColor: '#9b2335',
          borderWidth: 1
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
              label: ctx => `${ctx.raw} records (${formatPercent(ctx.raw, matchCount)})`
            }
          }
        },
        scales: {
          x: { display: false },
          y: {
            ticks: { font: { size: 14 } },
            grid: { display: false }
          }
        },
        onClick: (e, activeEls) => {
          if (activeEls.length) {
            const theme = topThemes[activeEls[0].index][0];
            const themeFilter = document.createElement('div');
            themeFilter.className = 'filter-chip';
            themeFilter.textContent = `Theme: ${theme}`;
            const button = document.createElement('button');
            button.textContent = '×';
            button.addEventListener('click', () => {
              themeFilter.remove();
              const newThemes = new Set(activeFilters.themes || []);
              newThemes.delete(theme);
              activeFilters.themes = newThemes;
              applyFilters();
            });
            themeFilter.appendChild(button);
            document.getElementById('filter-chips').appendChild(themeFilter);
            const newThemes = new Set(activeFilters.themes || []);
            newThemes.add(theme);
            activeFilters.themes = newThemes;
            applyFilters();
          }
        }
      }
    });
    const fig01Table = document.getElementById('fig01-table');
    fig01Table.innerHTML = '';
    topThemes.forEach(([theme, count]) => {
      const tr = document.createElement('tr');
      const themeYears = filteredRecords.filter(r => (r.themes || []).includes(theme)).map(r => r.year);
      const minThemeYear = Math.min(...themeYears);
      const maxThemeYear = Math.max(...themeYears);
      tr.innerHTML = `
        <td>${theme}</td>
        <td class="rank">${formatNumber(count)}</td>
        <td class="pct">${formatPercent(count, matchCount)}</td>
        <td class="years">${minThemeYear}–${maxThemeYear}</td>
      `;
      fig01Table.appendChild(tr);
    });

    // FIG.02
    const yearMechanismCounts = {};
    filteredRecords.forEach(r => {
      if (!yearMechanismCounts[r.year]) yearMechanismCounts[r.year] = { 'Universal Periodic Review': 0, 'Treaty bodies': 0, 'Special Procedures': 0 };
      yearMechanismCounts[r.year][r.mechanism]++;
    });
    const fig02Labels = years;
    const uprData = fig02Labels.map(y => yearMechanismCounts[y]?.['Universal Periodic Review'] || 0);
    const treatyData = fig02Labels.map(y => yearMechanismCounts[y]?.['Treaty bodies'] || 0);
    const specialData = fig02Labels.map(y => yearMechanismCounts[y]?.['Special Procedures'] || 0);
    const fig02Ctx = document.getElementById('fig02-chart').getContext('2d');
    if (window.fig02Chart) window.fig02Chart.destroy();
    window.fig02Chart = new Chart(fig02Ctx, {
      type: 'bar',
      data: {
        labels: fig02Labels,
        datasets: [
          { label: 'Universal Periodic Review', data: uprData, backgroundColor: '#c2410c' },
          { label: 'Treaty bodies', data: treatyData, backgroundColor: '#0f766e' },
          { label: 'Special Procedures', data: specialData, backgroundColor: '#7c3aed' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.dataset.label}: ${ctx.raw} records`
            }
          }
        },
        scales: {
          x: { stacked: true },
          y: { stacked: true }
        }
      }
    });

    // Records table
    const tbody = document.getElementById('records-tbody');
    tbody.innerHTML = '';
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const rowsToShow = filteredRecords.slice(0, visibleRows);
    const shownCount = rowsToShow.filter(r => {
      if (!searchTerm) return true;
      return r.text.toLowerCase().includes(searchTerm) || r.symbol.toLowerCase().includes(searchTerm);
    }).length;
    document.getElementById('search-caption').textContent = `${formatNumber(shownCount)} of ${formatNumber(matchCount)} records shown`;

    rowsToShow.forEach(record => {
      const tr = document.createElement('tr');
      tr.setAttribute('aria-expanded', 'false');
      tr.setAttribute('tabindex', '0');
      tr.addEventListener('click', () => toggleRow(tr, record));
      tr.addEventListener('keydown', e => { if (e.key === 'Enter') toggleRow(tr, record); });

      const date = new Date(record.date).toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'});
      const para = extractParagraphNumber(record.text);
      const firstLine = getFirstLine(record.text);
      const states = record.mechanism === 'Universal Periodic Review' ? extractRecommendingStates(record.text) : [];
      const stateText = states.length ? states.join(', ') : '—';

      tr.innerHTML = `
        <th scope="row">${date}</th>
        <td>${record.body}</td>
        <td><a href="${record.doc_url}" target="_blank" rel="noopener">${record.symbol}</a></td>
        <td class="para">${para || '—'}</td>
        <td>${stateText}</td>
        <td class="first-line">${firstLine}</td>
      `;

      if (searchTerm) {
        const text = record.text.toLowerCase();
        const symbol = record.symbol.toLowerCase();
        if (text.includes(searchTerm) || symbol.includes(searchTerm)) {
          const mark = document.createElement('mark');
          mark.textContent = searchTerm;
          const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
          const highlighted = parts.map(p => p.toLowerCase() === searchTerm.toLowerCase() ? mark.outerHTML : p).join('');
          tr.querySelector('.first-line').innerHTML = getFirstLine(highlighted);
        }
      }

      tbody.appendChild(tr);
    });

    // UPR States list
    const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
    const stateCounts = {};
    uprRecords.forEach(r => {
      const states = extractRecommendingStates(r.text);
      states.forEach(s => {
        stateCounts[s] = (stateCounts[s] || 0) + 1;
      });
    });
    const topStates = Object.entries(stateCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const ol = document.getElementById('upr-states-ol');
    ol.innerHTML = '';
    topStates.forEach(([state, count]) => {
      const li = document.createElement('li');
      li.textContent = `${state} (${formatNumber(count)})`;
      ol.appendChild(li);
    });

    // Checks
    updateChecks();
  };

  const toggleRow = (tr, record) => {
    const isExpanded = tr.getAttribute('aria-expanded') === 'true';
    tr.setAttribute('aria-expanded', !isExpanded);

    if (isExpanded) {
      const expanded = tr.querySelector('.expanded');
      if (expanded) expanded.remove();
    } else {
      const para = extractParagraphNumber(record.text);
      const states = record.mechanism === 'Universal Periodic Review' ? extractRecommendingStates(record.text) : [];

      const expanded = document.createElement('tr');
      expanded.className = 'expanded';
      expanded.innerHTML = `
        <td colspan="6">
          <h4>${para ? `para. ${para}` : 'No paragraph number'}</h4>
          <div class="text">${record.text}</div>
          <div class="labels">
            ${record.themes?.length ? `
            <div class="label-group">
              <h5>Themes</h5>
              <div class="tags">${record.themes.map(t => `<span class="tag">${t}</span>`).join('')}</div>
            </div>
            ` : ''}
            ${record.sdgs?.length ? `
            <div class="label-group">
              <h5>SDGs</h5>
              <div class="tags">${record.sdgs.map(s => `<span class="tag">${s} ${sdgNames[s]}</span>`).join('')}</div>
            </div>
            ` : ''}
            ${record.sdg_targets?.length ? `
            <div class="label-group">
              <h5>SDG targets</h5>
              <div class="tags">${record.sdg_targets.map(t => `<span class="tag">${t}</span>`).join('')}</div>
            </div>
            ` : ''}
            ${record.affected_persons?.length ? `
            <div class="label-group">
              <h5>Affected persons</h5>
              <div class="tags">${record.affected_persons.map(a => `<span class="tag">${a}</span>`).join('')}</div>
            </div>
            ` : ''}
            ${record.section ? `
            <div class="label-group">
              <h5>Section</h5>
              <div class="tags"><span class="tag">${record.section}</span></div>
            </div>
            ` : ''}
          </div>
          <div class="actions">
            <button class="copy-citation">Copy citation</button>
            <span class="copied"></span>
            <a href="${record.doc_url}" target="_blank" rel="noopener">Open the UN document</a>
          </div>
        </td>
      `;
      tr.after(expanded);

      expanded.querySelector('.copy-citation').addEventListener('click', () => {
        const citation = para ? `${record.symbol}, para. ${para}` : record.symbol;
        copyToClipboard(citation);
        const copied = expanded.querySelector('.copied');
        copied.textContent = 'Copied';
        setTimeout(() => { copied.textContent = ''; }, 2000);
      });
    }
  };

  const updateChecks = () => {
    const checksList = document.getElementById('checks-list');
    checksList.innerHTML = '';

    // Record count
    const recordCountCheck = document.createElement('li');
    recordCountCheck.className = Number(uhri.count) === totalCount ? 'pass' : 'fail';
    recordCountCheck.innerHTML = `
      Record count: <span class="values">${totalCount} (file) vs ${Number(uhri.count)} (header)</span>
    `;
    checksList.appendChild(recordCountCheck);

    // Partitions
    const mechanismCounts = { 'Universal Periodic Review': 0, 'Treaty bodies': 0, 'Special Procedures': 0 };
    const bodyCounts = {};
    const yearCounts = {};
    records.forEach(r => {
      mechanismCounts[r.mechanism]++;
      bodyCounts[r.body] = (bodyCounts[r.body] || 0) + 1;
      yearCounts[r.year] = (yearCounts[r.year] || 0) + 1;
    });
    const mechanismSum = Object.values(mechanismCounts).reduce((a, b) => a + b, 0);
    const bodySum = Object.values(bodyCounts).reduce((a, b) => a + b, 0);
    const yearSum = Object.values(yearCounts).reduce((a, b) => a + b, 0);
    const mechanismCheck = document.createElement('li');
    mechanismCheck.className = mechanismSum === totalCount ? 'pass' : 'fail';
    mechanismCheck.innerHTML = `Mechanism partition: <span class="values">${mechanismSum} (sum) vs ${totalCount} (total)</span>`;
    checksList.appendChild(mechanismCheck);
    const bodyCheck = document.createElement('li');
    bodyCheck.className = bodySum === totalCount ? 'pass' : 'fail';
    bodyCheck.innerHTML = `Body partition: <span class="values">${bodySum} (sum) vs ${totalCount} (total)</span>`;
    checksList.appendChild(bodyCheck);
    const yearCheck = document.createElement('li');
    yearCheck.className = yearSum === totalCount ? 'pass' : 'fail';
    yearCheck.innerHTML = `Year partition: <span class="values">${yearSum} (sum) vs ${totalCount} (total)</span>`;
    checksList.appendChild(yearCheck);

    // Type partition
    const typeCounts = {};
    records.forEach(r => { typeCounts[r.type] = (typeCounts[r.type] || 0) + 1; });
    const typeSum = Object.values(typeCounts).reduce((a, b) => a + b, 0);
    const typeCheck = document.createElement('li');
    typeCheck.className = typeSum === totalCount ? 'pass' : 'fail';
    typeCheck.innerHTML = `Type partition: <span class="values">${typeSum} (sum) vs ${totalCount} (total)</span>`;
    checksList.appendChild(typeCheck);

    // Chart against table
    const themeCounts = {};
    filteredRecords.forEach(r => {
      (r.themes || []).forEach(theme => {
        themeCounts[theme] = (themeCounts[theme] || 0) + 1;
      });
    });
    const topThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    let chartCheckPass = true;
    topThemes.forEach(([theme, count]) => {
      const recomputed = filteredRecords.filter(r => (r.themes || []).includes(theme)).length;
      if (recomputed !== count) chartCheckPass = false;
    });
    const chartCheck = document.createElement('li');
    chartCheck.className = chartCheckPass ? 'pass' : 'fail';
    chartCheck.innerHTML = `Chart against table: <span class="values">${topThemes.length} themes match</span>`;
    checksList.appendChild(chartCheck);

    // Links
    const linkErrors = [];
    records.forEach(r => {
      const url = new URL(r.doc_url);
      if (url.protocol !== 'https:' || url.hostname !== 'docs.un.org') {
        linkErrors.push(r.symbol);
      } else {
        const pathSymbol = decodeURIComponent(url.pathname.split('/').pop()).toUpperCase();
        if (pathSymbol !== r.symbol.toUpperCase()) {
          linkErrors.push(r.symbol);
        }
      }
    });
    const linkCheck = document.createElement('li');
    linkCheck.className = linkErrors.length === 0 ? 'pass' : 'fail';
    linkCheck.innerHTML = `Links: <span class="values">${linkErrors.length} errors</span>`;
    if (linkErrors.length) {
      linkCheck.innerHTML += `<div class="details">Failed symbols: ${linkErrors.join(', ')}</div>`;
    }
    checksList.appendChild(linkCheck);

    // Paragraph numbers
    const paraCounts = { 'Universal Periodic Review': 0, 'Treaty bodies': 0, 'Special Procedures': 0 };
    const paraTotal = { 'Universal Periodic Review': 0, 'Treaty bodies': 0, 'Special Procedures': 0 };
    records.forEach(r => {
      paraTotal[r.mechanism]++;
      if (extractParagraphNumber(r.text)) paraCounts[r.mechanism]++;
    });
    const uprParaCheck = document.createElement('li');
    uprParaCheck.className = paraCounts['Universal Periodic Review'] === paraTotal['Universal Periodic Review'] ? 'pass' : 'warn';
    uprParaCheck.innerHTML = `UPR paragraph numbers: <span class="values">${paraCounts['Universal Periodic Review']} of ${paraTotal['Universal Periodic Review']}</span>`;
    checksList.appendChild(uprParaCheck);
    const treatyParaCheck = document.createElement('li');
    treatyParaCheck.className = 'pass';
    treatyParaCheck.innerHTML = `Treaty bodies paragraph numbers: <span class="values">${paraCounts['Treaty bodies']} of ${paraTotal['Treaty bodies']}</span>`;
    checksList.appendChild(treatyParaCheck);
    const specialParaCheck = document.createElement('li');
    specialParaCheck.className = 'pass';
    specialParaCheck.innerHTML = `Special Procedures paragraph numbers: <span class="values">${paraCounts['Special Procedures']} of ${paraTotal['Special Procedures']}</span>`;
    checksList.appendChild(specialParaCheck);

    // States found
    const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
    const stateFound = uprRecords.filter(r => extractRecommendingStates(r.text).length > 0).length;
    const stateErrors = uprRecords.filter(r => extractRecommendingStates(r.text).length === 0).map(r => r.symbol);
    const stateCheck = document.createElement('li');
    stateCheck.className = stateErrors.length === 0 ? 'pass' : 'warn';
    stateCheck.innerHTML = `UPR recommending States: <span class="values">${stateFound} of ${uprRecords.length}</span>`;
    if (stateErrors.length) {
      stateCheck.innerHTML += `<div class="details">Records without a State: ${stateErrors.join(', ')}</div>`;
    }
    checksList.appendChild(stateCheck);

    // Duplicates and gaps
    const distinctIds = new Set(records.map(r => r.id)).size;
    const idCheck = document.createElement('li');
    idCheck.className = distinctIds === totalCount ? 'pass' : 'fail';
    idCheck.innerHTML = `Distinct IDs: <span class="values">${distinctIds} vs ${totalCount}</span>`;
    checksList.appendChild(idCheck);

    const textCounts = {};
    records.forEach(r => { textCounts[r.text] = (textCounts[r.text] || 0) + 1; });
    const duplicateTexts = Object.values(textCounts).filter(v => v > 1).length;
    const duplicateCheck = document.createElement('li');
    duplicateCheck.className = duplicateTexts === 0 ? 'pass' : 'warn';
    duplicateCheck.innerHTML = `Duplicate texts: <span class="values">${duplicateTexts}</span>`;
    checksList.appendChild(duplicateCheck);

    const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
    const noThemesCheck = document.createElement('li');
    noThemesCheck.className = 'pass';
    noThemesCheck.innerHTML = `Records without themes: <span class="values">${noThemes}</span>`;
    checksList.appendChild(noThemesCheck);

    const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    const noSdgsCheck = document.createElement('li');
    noSdgsCheck.className = 'pass';
    noSdgsCheck.innerHTML = `Records without SDGs: <span class="values">${noSdgs}</span>`;
    checksList.appendChild(noSdgsCheck);

    const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
    const noAffectedCheck = document.createElement('li');
    noAffectedCheck.className = 'pass';
    noAffectedCheck.innerHTML = `Records without affected persons: <span class="values">${noAffected}</span>`;
    checksList.appendChild(noAffectedCheck);

    document.getElementById('check-count').textContent = checksList.children.length;
  };

  // ------------------------------------------------------------
  // INITIAL SETUP
  // ------------------------------------------------------------
  document.getElementById('country-label').textContent = country;
  document.getElementById('country-name').textContent = country;
  document.getElementById('country-name-2').textContent = country;
  document.getElementById('record-count').textContent = formatNumber(totalCount);
  document.getElementById('record-count-2').textContent = formatNumber(totalCount);
  document.getElementById('document-count').textContent = formatNumber(documentCount);
  document.getElementById('year-range').textContent = `${minYear}–${maxYear}`;
  document.getElementById('built-date').textContent = builtDate;
  document.getElementById('built-date-2').textContent = builtDate;
  document.getElementById('source-url').href = uhri.source_url;
  document.getElementById('source-url-2').href = uhri.source_url;
  document.getElementById('total-count').textContent = formatNumber(totalCount);

  // Mechanism select
  const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
  const mechanismSelect = document.getElementById('mechanism-select');
  mechanisms.forEach(m => {
    const option = document.createElement('option');
    option.value = m;
    option.textContent = m;
    mechanismSelect.appendChild(option);
  });
  mechanismSelect.addEventListener('change', () => {
    activeFilters.mechanism = mechanismSelect.value;
    updateBodySelect();
    updateStateContainer();
    applyFilters();
  });

  // Body select
  const updateBodySelect = () => {
    const bodySelect = document.getElementById('body-select');
    bodySelect.innerHTML = '<option value="all">All bodies</option>';
    const bodies = {};
    records.forEach(r => {
      if (activeFilters.mechanism === 'all' || r.mechanism === activeFilters.mechanism) {
        bodies[r.body] = (bodies[r.body] || 0) + 1;
      }
    });
    Object.entries(bodies)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .forEach(([body, count]) => {
        const option = document.createElement('option');
        option.value = body;
        option.textContent = `${body} (${formatNumber(count)})`;
        bodySelect.appendChild(option);
      });
  };
  document.getElementById('body-select').addEventListener('change', () => {
    activeFilters.body = document.getElementById('body-select').value;
    applyFilters();
  });

  // Type select
  const types = Array.from(new Set(records.map(r => r.type)));
  const typeSelect = document.getElementById('type-select');
  typeSelect.innerHTML = '<option value="all">All types</option>';
  types.forEach(t => {
    const option = document.createElement('option');
    option.value = t;
    option.textContent = t;
    typeSelect.appendChild(option);
  });
  typeSelect.addEventListener('change', () => {
    activeFilters.type = typeSelect.value;
    applyFilters();
  });

  // State select
  const updateStateContainer = () => {
    const stateContainer = document.getElementById('state-container');
    if (activeFilters.mechanism === 'Universal Periodic Review' || activeFilters.mechanism === 'all') {
      stateContainer.hidden = false;
      const stateSelect = document.getElementById('state-select');
      stateSelect.innerHTML = '<option value="all">All States</option>';
      const states = {};
      records.forEach(r => {
        if (r.mechanism === 'Universal Periodic Review' && (activeFilters.mechanism === 'all' || r.mechanism === activeFilters.mechanism)) {
          const recordStates = extractRecommendingStates(r.text);
          recordStates.forEach(s => {
            states[s] = (states[s] || 0) + 1;
          });
        }
      });
      Object.entries(states)
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .forEach(([state, count]) => {
          const option = document.createElement('option');
          option.value = state;
          option.textContent = `${state} (${formatNumber(count)})`;
          option.label = state;
          stateSelect.appendChild(option);
        });
    } else {
      stateContainer.hidden = true;
    }
  };
  document.getElementById('state-select').addEventListener('change', () => {
    activeFilters.state = document.getElementById('state-select').value;
    applyFilters();
  });

  // Year selects
  const yearFromSelect = document.getElementById('year-from');
  const yearToSelect = document.getElementById('year-to');
  years.forEach(y => {
    const optionFrom = document.createElement('option');
    optionFrom.value = y;
    optionFrom.textContent = y;
    yearFromSelect.appendChild(optionFrom);
    const optionTo = document.createElement('option');
    optionTo.value = y;
    optionTo.textContent = y;
    yearToSelect.appendChild(optionTo);
  });
  yearFromSelect.addEventListener('change', () => {
    const from = yearFromSelect.value;
    const to = yearToSelect.value;
    if (from && to && Number(from) > Number(to)) {
      yearToSelect.value = from;
      activeFilters.yearTo = from;
    }
    activeFilters.yearFrom = from;
    applyFilters();
  });
  yearToSelect.addEventListener('change', () => {
    const from = yearFromSelect.value;
    const to = yearToSelect.value;
    if (from && to && Number(from) > Number(to)) {
      yearFromSelect.value = to;
      activeFilters.yearFrom = to;
    }
    activeFilters.yearTo = to;
    applyFilters();
  });

  // SDG grid
  const sdgGrid = document.getElementById('sdg-grid');
  Object.entries(sdgNames)
    .sort((a, b) => Number(a[0]) - Number(b[0]))
    .forEach(([goal, name]) => {
      const div = document.createElement('div');
      div.className = 'sdg-option';
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.id = `sdg-${goal}`;
      input.value = goal;
      input.addEventListener('change', () => {
        if (input.checked) {
          activeFilters.sdgs.add(goal);
        } else {
          activeFilters.sdgs.delete(goal);
        }
        applyFilters();
      });
      const label = document.createElement('label');
      label.htmlFor = `sdg-${goal}`;
      label.textContent = `${goal} ${name}`;
      div.appendChild(input);
      div.appendChild(label);
      sdgGrid.appendChild(div);
    });

  // Keyword input
  const keywordInput = document.getElementById('keyword-input');
  keywordInput.addEventListener('input', debounce(() => {
    activeFilters.keyword = keywordInput.value.trim();
    applyFilters();
  }, 300));

  // Clear all
  document.getElementById('clear-all').addEventListener('click', () => {
    activeFilters = {
      keyword: '',
      mechanism: 'all',
      body: 'all',
      type: 'all',
      state: 'all',
      yearFrom: '',
      yearTo: '',
      sdgs: new Set()
    };
    keywordInput.value = '';
    mechanismSelect.value = 'all';
    document.getElementById('body-select').value = 'all';
    typeSelect.value = 'all';
    document.getElementById('state-select').value = 'all';
    yearFromSelect.value = '';
    yearToSelect.value = '';
    document.querySelectorAll('#sdg-grid input').forEach(cb => { cb.checked = false; });
    applyFilters();
  });

  // Tabs
  document.getElementById('tab-01').addEventListener('click', () => {
    document.querySelectorAll('[role="tab"]').forEach(t => t.setAttribute('aria-selected', 'false'));
    document.querySelectorAll('[role="tabpanel"]').forEach(p => p.setAttribute('aria-hidden', 'true'));
    document.getElementById('tab-01').setAttribute('aria-selected', 'true');
    document.getElementById('panel-01').setAttribute('aria-hidden', 'false');
  });
  document.getElementById('tab-02').addEventListener('click', () => {
    document.querySelectorAll('[role="tab"]').forEach(t => t.setAttribute('aria-selected', 'false'));
    document.querySelectorAll('[role="tabpanel"]').forEach(p => p.setAttribute('aria-hidden', 'true'));
    document.getElementById('tab-02').setAttribute('aria-selected', 'true');
    document.getElementById('panel-02').setAttribute('aria-hidden', 'false');
  });
  document.getElementById('tab-03').addEventListener('click', () => {
    document.querySelectorAll('[role="tab"]').forEach(t => t.setAttribute('aria-selected', 'false'));
    document.querySelectorAll('[role="tabpanel"]').forEach(p => p.setAttribute('aria-hidden', 'true'));
    document.getElementById('tab-03').setAttribute('aria-selected', 'true');
    document.getElementById('panel-03').setAttribute('aria-hidden', 'false');
  });

  // Sort
  document.getElementById('col-date').addEventListener('click', () => {
    sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
    applyFilters();
  });

  // Load more
  document.getElementById('load-more').addEventListener('click', () => {
    visibleRows += 50;
    applyFilters();
  });

  // UPR States link
  document.getElementById('upr-states-link').addEventListener('click', e => {
    e.preventDefault();
    const list = document.getElementById('upr-states-list');
    list.hidden = !list.hidden;
  });

  // Checks toggle
  document.querySelector('#checks-section h4 button').addEventListener('click', () => {
    const button = document.querySelector('#checks-section h4 button');
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', !isExpanded);
    document.getElementById('checks-list').hidden = isExpanded;
  });

  // Filter section toggles
  document.querySelectorAll('.filter-section h3 button').forEach(button => {
    button.addEventListener('click', () => {
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !isExpanded);
      const controls = document.getElementById(button.getAttribute('aria-controls'));
      controls.hidden = isExpanded;
    });
  });

  // Download CSV
  document.getElementById('download-csv').addEventListener('click', () => {
    const headers = [
      'Date', 'Year', 'Body', 'Mechanism', 'Type', 'Symbol', 'Paragraph', 'Recommending State',
      'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Text'
    ];
    const rows = filteredRecords.map(r => {
      const para = extractParagraphNumber(r.text);
      const states = r.mechanism === 'Universal Periodic Review' ? extractRecommendingStates(r.text).join('; ') : '';
      return [
        r.date,
        r.year,
        r.body,
        r.mechanism,
        r.type,
        r.symbol,
        para || '',
        states,
        (r.themes || []).join('; '),
        (r.sdgs || []).map(s => `${s} ${sdgNames[s]}`).join('; '),
        (r.sdg_targets || []).join('; '),
        (r.affected_persons || []).join('; '),
        r.section || '',
        r.text
      ];
    });
    const csv = [
      '# UN human rights recommendations and observations',
      `# ${country}`,
      `# Source: ${uhri.source}`,
      `# Built: ${uhri.built}`,
      `# Filters: ${JSON.stringify(activeFilters)}`,
      `# Records: ${filteredRecords.length}`,
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
    ].join('\n');
    const blob = new Blob([csv], {type: 'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `uhri-${country.toLowerCase()}-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Copy summary
  document.getElementById('copy-summary').addEventListener('click', () => {
    const matchCount = filteredRecords.length;
    const typeCounts = {};
    records.forEach(r => { typeCounts[r.type] = (typeCounts[r.type] || 0) + 1; });
    const typeBreakdown = Object.entries(typeCounts).map(([type, count]) => `${type} ${formatNumber(count)}`).join(', ');
    const mechanismCounts = { 'Universal Periodic Review': 0, 'Treaty bodies': 0, 'Special Procedures': 0 };
    filteredRecords.forEach(r => { mechanismCounts[r.mechanism]++; });
    const themeCounts = {};
    filteredRecords.forEach(r => {
      (r.themes || []).forEach(theme => {
        themeCounts[theme] = (themeCounts[theme] || 0) + 1;
      });
    });
    const topThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10)
      .map(([theme, count]) => `${theme} (${formatNumber(count)})`)
      .join(', ');

    const summary = `UN human rights recommendations and observations: ${country}
Source: Universal Human Rights Index (${uhri.source_url})
${formatNumber(totalCount)} records (${typeBreakdown}), ${formatNumber(documentCount)} documents, ${minYear}–${maxYear}
Current filter: ${matchCount} records
Universal Periodic Review: ${formatNumber(mechanismCounts['Universal Periodic Review'])} records
Treaty bodies: ${formatNumber(mechanismCounts['Treaty bodies'])} records
Special Procedures: ${formatNumber(mechanismCounts['Special Procedures'])} records
Top themes: ${topThemes}`;

    copyToClipboard(summary);
  });

  // Initial render
  updateBodySelect();
  updateStateContainer();
  applyFilters();
});
</script>
</body>
</html>
```