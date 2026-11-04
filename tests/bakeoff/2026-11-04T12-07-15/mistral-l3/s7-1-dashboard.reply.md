I built the UN human rights recommendations dashboard for Kenya, exactly as planned. Four tabs: Overview (headline numbers and charts), Records (the table with expandable rows), Check (the app's own checks and a random-sample label check), and Method & export (how it was made and how to take it with you). The left rail holds the filters, always visible; every tab reads the same filtered set.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations: Kenya</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --red: #9b2335;
  --upr: #c2410c;
  --treaty: #0f766e;
  --special: #7c3aed;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  accent-color: var(--red);
}
[hidden] { display: none !important; }
.visually-hidden {
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
a { color: inherit; text-decoration: none; }
a:focus { outline: 2px solid var(--red); outline-offset: 2px; }
button, input, select, textarea {
  font: inherit;
  color: inherit;
  background: none;
  border: 1px solid var(--rule);
  padding: 0.5em 0.75em;
  border-radius: 4px;
}
button:not(:disabled):hover, input:not(:disabled):hover, select:not(:disabled):hover, textarea:not(:disabled):hover {
  background-color: var(--ink);
  color: var(--paper);
  cursor: pointer;
}
button:disabled { opacity: 0.5; cursor: not-allowed; }
button:focus { outline: 2px solid var(--red); outline-offset: 2px; }
input[type="text"] { width: 100%; box-sizing: border-box; }
select { width: 100%; }
mark { background-color: #ffeb3b; color: var(--ink); padding: 0 0.2em; }
header, footer { padding: 1em 1.5em; border-bottom: 1px solid var(--rule); }
header { border-top: 3px solid var(--red); }
header .label { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.8em; letter-spacing: 0.05em; color: var(--ink); }
header h1 { font-family: Georgia, "Times New Roman", serif; font-size: 2em; margin: 0.25em 0 0; }
header .meta { font-size: 0.9em; color: #555; margin-top: 0.5em; }
header .meta a { text-decoration: underline; }
#app {
  display: flex;
  min-height: calc(100vh - 120px);
}
#filters {
  width: 280px;
  padding: 1em;
  border-right: 1px solid var(--rule);
  background-color: #f9f7f4;
}
#filters h2 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  margin: 0 0 1em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
#filters .count {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5em;
  margin: 0.5em 0;
  line-height: 1;
}
#filters .count-note { font-size: 0.8em; color: #555; margin-top: 0.25em; }
#filters .bar {
  height: 4px;
  background-color: var(--rule);
  margin: 0.5em 0;
  position: relative;
}
#filters .bar-fill {
  height: 100%;
  background-color: var(--red);
  width: 0%;
  transition: width 0.3s ease;
}
#filters .chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
  margin: 0.5em 0;
}
#filters .chip {
  background-color: var(--ink);
  color: var(--paper);
  padding: 0.25em 0.5em;
  border-radius: 1em;
  font-size: 0.8em;
  display: flex;
  align-items: center;
  gap: 0.25em;
}
#filters .chip button {
  padding: 0;
  margin: 0;
  width: 1em;
  height: 1em;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: none;
  color: var(--paper);
  cursor: pointer;
}
#filters .filter-section {
  margin-bottom: 1.5em;
}
#filters .filter-section h3 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  margin: 0 0 0.5em;
  display: flex;
  align-items: center;
  gap: 0.5em;
}
#filters .filter-section h3 button {
  padding: 0;
  border: none;
  background: none;
  font-size: 1em;
  cursor: pointer;
  transition: transform 0.2s;
}
#filters .filter-section h3[aria-expanded="false"] button { transform: rotate(-90deg); }
#filters .filter-section[hidden] { display: none; }
#filters .filter-section .hint {
  font-size: 0.75em;
  color: #555;
  margin-top: 0.25em;
}
#filters .filter-section .group {
  margin-bottom: 1em;
}
#filters .filter-section .group label {
  display: block;
  margin-bottom: 0.25em;
  font-size: 0.9em;
}
#filters .filter-section .group input[type="radio"], #filters .filter-section .group input[type="checkbox"] {
  width: auto;
  margin-right: 0.5em;
}
#filters .filter-section .group .radio-group, #filters .filter-section .group .checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.25em;
}
#tabs {
  display: flex;
  border-bottom: 1px solid var(--rule);
}
.tab {
  padding: 1em 1.5em;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  cursor: pointer;
  border-right: 1px solid var(--rule);
  position: relative;
  background: none;
  border: none;
  border-radius: 0;
}
.tab:focus { outline: 2px solid var(--red); outline-offset: -2px; }
.tab[aria-selected="true"] {
  background-color: var(--paper);
  border-bottom: 3px solid var(--red);
  margin-bottom: -1px;
}
.tab-panel {
  flex: 1;
  padding: 1.5em;
}
.tab-panel h2 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  margin: 0 0 1em;
}
.tab-panel h3 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5em;
  margin: 1.5em 0 0.5em;
}
.tab-panel .fig-title {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  margin: 2em 0 0.5em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.tab-panel .fig-source {
  font-size: 0.8em;
  color: #555;
  margin-top: 0.25em;
}
.tab-panel .note {
  font-size: 0.8em;
  color: #555;
  margin: 0.5em 0;
}
.tab-panel .tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5em;
  margin: 1.5em 0;
}
.tile {
  border: 1px solid var(--rule);
  padding: 1em;
  border-radius: 4px;
}
.tile h4 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5em;
  margin: 0 0 0.25em;
  line-height: 1;
}
.tile .dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 0.5em;
}
.tile .upr { background-color: var(--upr); }
.tile .treaty { background-color: var(--treaty); }
.tile .special { background-color: var(--special); }
.tile .meta {
  font-size: 0.9em;
  color: #555;
  margin-top: 0.5em;
}
.tile .meta .share {
  display: inline-block;
  width: 10px;
  height: 10px;
  background-color: var(--red);
  margin-right: 0.25em;
}
.tile .meta .share-bar {
  display: inline-block;
  height: 10px;
  background-color: var(--rule);
  width: 60px;
  position: relative;
  vertical-align: middle;
}
.tile .meta .share-fill {
  height: 100%;
  background-color: var(--red);
  width: 0%;
  display: inline-block;
}
.chart-container {
  position: relative;
  height: 400px;
  margin: 1.5em 0;
}
.chart-container canvas {
  max-width: 100%;
  height: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
}
table caption {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  text-align: left;
  margin-bottom: 0.5em;
}
table th, table td {
  padding: 0.75em;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
table th {
  font-weight: bold;
  background-color: #f9f7f4;
}
table th[scope="col"]:first-child, table td:first-child { width: 8em; }
table th[scope="col"]:nth-child(3), table td:nth-child(3) { width: 10em; }
table th[scope="col"]:nth-child(4), table td:nth-child(4) { width: 4em; }
table th[scope="col"]:nth-child(5), table td:nth-child(5) { width: 10em; }
table th[scope="col"]:nth-child(6), table td:nth-child(6) { width: 12em; }
table td { vertical-align: top; }
table td:last-child { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.9em; }
table .expand-row button {
  padding: 0;
  border: none;
  background: none;
  color: var(--ink);
  cursor: pointer;
  text-decoration: underline;
}
table .expand-row button:focus { outline: 2px solid var(--red); }
table .expanded {
  background-color: #f9f7f4;
}
table .expanded td {
  padding: 1em;
  border-bottom: 1px solid var(--rule);
}
table .expanded .para-num {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2em;
  color: var(--red);
  margin: 0.5em 0;
}
table .expanded .labels {
  margin: 0.5em 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
}
table .expanded .label {
  background-color: var(--ink);
  color: var(--paper);
  padding: 0.25em 0.5em;
  border-radius: 4px;
  font-size: 0.8em;
}
table .expanded .actions {
  margin-top: 1em;
  display: flex;
  gap: 1em;
}
table .expanded .actions button {
  padding: 0.5em 1em;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background-color: var(--ink);
  color: var(--paper);
}
table .expanded .actions button:focus { outline: 2px solid var(--red); }
table .expanded .actions .copied {
  background-color: var(--red);
  color: var(--paper);
}
.pagination {
  margin-top: 1em;
  display: flex;
  justify-content: center;
  gap: 1em;
}
.pagination button {
  padding: 0.5em 1em;
  border: 1px solid var(--rule);
  border-radius: 4px;
}
.pagination button:disabled { opacity: 0.5; }
.check-panel {
  border: 1px solid var(--rule);
  padding: 1em;
  border-radius: 4px;
  margin: 1.5em 0;
}
.check-panel h3 {
  margin: 0 0 0.5em;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
}
.check-panel .check-item {
  margin-bottom: 0.5em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.check-panel .check-item.pass::before {
  content: "✓";
  color: var(--treaty);
  margin-right: 0.5em;
}
.check-panel .check-item.fail::before {
  content: "✗";
  color: var(--red);
  margin-right: 0.5em;
}
.check-panel .check-item .values {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.9em;
}
.check-panel .check-item .details {
  font-size: 0.8em;
  color: #555;
  margin-top: 0.25em;
  white-space: pre-wrap;
}
.sample-check {
  margin: 2em 0;
}
.sample-check h3 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  margin: 0 0 1em;
}
.sample-check .controls {
  display: flex;
  gap: 1em;
  margin-bottom: 1em;
  align-items: center;
}
.sample-check .seed-box {
  display: flex;
  gap: 0.5em;
  align-items: center;
}
.sample-check .seed-box input {
  width: 6em;
  text-align: center;
}
.sample-check .tally {
  margin: 1em 0;
  font-size: 0.9em;
}
.sample-card {
  border: 1px solid var(--rule);
  border-radius: 4px;
  margin-bottom: 1em;
}
.sample-card-header {
  padding: 1em;
  background-color: #f9f7f4;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--rule);
}
.sample-card-header button {
  padding: 0;
  border: none;
  background: none;
  font-size: 1em;
  cursor: pointer;
}
.sample-card-header[aria-expanded="false"] .arrow { transform: rotate(-90deg); }
.sample-card-body {
  padding: 1em;
}
.sample-card-body[hidden] { display: none; }
.sample-card-body .text {
  white-space: pre-wrap;
  margin: 0.5em 0;
}
.sample-card-body .themes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
  margin: 0.5em 0;
}
.sample-card-body .theme {
  background-color: var(--ink);
  color: var(--paper);
  padding: 0.25em 0.5em;
  border-radius: 4px;
  font-size: 0.8em;
}
.sample-card-body .verdict {
  margin-top: 1em;
  display: flex;
  gap: 1em;
}
.sample-card-body .verdict button {
  padding: 0.5em 1em;
  border: 1px solid var(--rule);
  border-radius: 4px;
}
.sample-card-body .verdict button.active {
  background-color: var(--ink);
  color: var(--paper);
}
.export-section {
  margin: 2em 0;
}
.export-section h3 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  letter-spacing: 0.05em;
  margin: 0 0 1em;
}
.export-section .actions {
  display: flex;
  gap: 1em;
  margin-bottom: 1em;
}
.export-section .actions button {
  padding: 0.5em 1em;
  border: 1px solid var(--rule);
  border-radius: 4px;
}
.export-section .data-source {
  font-size: 0.8em;
  color: #555;
  margin-top: 1em;
}
footer {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8em;
  border-top: 1px solid var(--rule);
}
</style>
</head>
<body>

<header>
  <div class="label">UHRI · <span id="country-label"></span></div>
  <h1>UN human rights recommendations and observations: <span id="country-name"></span></h1>
  <div class="meta">Source: <a id="source-link" href="#" target="_blank"></a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · built <span id="built-date"></span> · dated by document</div>
</header>

<div id="app">
  <aside id="filters" aria-labelledby="filters-heading">
    <h2 id="filters-heading">FILTERS <button id="clear-filters">Clear all</button></h2>
    <div class="count" id="matching-count" aria-live="polite">0</div>
    <div class="count-note">of <span id="total-count"></span> in the file</div>
    <div class="bar"><div class="bar-fill" id="matching-bar"></div></div>
    <div class="chips" id="active-filters"></div>

    <div class="filter-section" id="filter-keyword-section">
      <h3><button aria-expanded="true" aria-controls="filter-keyword">01 KEYWORD</button></h3>
      <div id="filter-keyword">
        <input type="text" id="keyword-input" placeholder="e.g. torture">
        <div class="hint">literal match, not synonyms</div>
      </div>
    </div>

    <div class="filter-section" id="filter-mechanism-section">
      <h3><button aria-expanded="false" aria-controls="filter-mechanism">02 MECHANISM, BODY, TYPE</button></h3>
      <div id="filter-mechanism" hidden>
        <div class="group">
          <div class="radio-group">
            <label><input type="radio" name="mechanism" value="all" checked> All mechanisms</label>
            <label><input type="radio" name="mechanism" value="Treaty bodies"> Treaty bodies</label>
            <label><input type="radio" name="mechanism" value="Universal Periodic Review"> Universal Periodic Review</label>
            <label><input type="radio" name="mechanism" value="Special Procedures"> Special Procedures</label>
          </div>
        </div>
        <div class="group" id="body-group">
          <label>Body or mandate</label>
          <div class="radio-group" id="body-options"></div>
        </div>
        <div class="group" id="type-group">
          <label>Type</label>
          <div class="radio-group" id="type-options"></div>
        </div>
        <div class="group" id="state-group" hidden>
          <label>Recommending State</label>
          <select id="state-select"><option value="all">All States</option></select>
        </div>
      </div>
    </div>

    <div class="filter-section" id="filter-year-sdg-section">
      <h3><button aria-expanded="false" aria-controls="filter-year-sdg">03 YEARS AND SDG</button></h3>
      <div id="filter-year-sdg" hidden>
        <div class="group">
          <label>Year from</label>
          <select id="year-from"><option value="">--</option></select>
          <label>to</label>
          <select id="year-to"><option value="">--</option></select>
        </div>
        <div class="group">
          <label>SDG</label>
          <select id="sdg-select"><option value="all">All SDGs</option></select>
        </div>
      </div>
    </div>
  </aside>

  <main>
    <div id="tabs" role="tablist" aria-label="Dashboard tabs">
      <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="panel-01">01 OVERVIEW</button>
      <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="panel-02">02 RECORDS</button>
      <button id="tab-03" class="tab" role="tab" aria-selected="false" aria-controls="panel-03">03 CHECK</button>
      <button id="tab-04" class="tab" role="tab" aria-selected="false" aria-controls="panel-04">04 METHOD & EXPORT</button>
    </div>

    <div id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01" tabindex="0">
      <div class="tiles">
        <div class="tile">
          <h4 id="total-records">0</h4>
          <div class="meta">
            <div><span class="share"></span> all records</div>
            <div id="type-breakdown"></div>
          </div>
          <div class="note">How this is computed: count of all records in the file, by type.</div>
        </div>
        <div class="tile">
          <h4 id="total-documents">0</h4>
          <div class="meta">documents</div>
          <div class="note">How this is computed: distinct document symbols.</div>
        </div>
        <div class="tile">
          <h4 id="total-years">0</h4>
          <div class="meta">years</div>
          <div class="note">How this is computed: first and last year in the file.</div>
        </div>
        <div class="tile">
          <h4 id="tile-upr">0</h4>
          <div class="meta"><span class="dot upr"></span> Universal Periodic Review</div>
          <div class="meta"><div class="share-bar"><div class="share-fill" id="share-upr"></div></div> of filtered</div>
          <div class="meta" id="upr-documents">0 documents · latest <span id="upr-latest-year">0</span></div>
          <div class="note">How this is computed: records with mechanism = "Universal Periodic Review".</div>
          <div class="meta"><a href="#" id="upr-states-link">see the States</a></div>
        </div>
        <div class="tile">
          <h4 id="tile-treaty">0</h4>
          <div class="meta"><span class="dot treaty"></span> Treaty bodies</div>
          <div class="meta"><div class="share-bar"><div class="share-fill" id="share-treaty"></div></div> of filtered</div>
          <div class="meta" id="treaty-documents">0 documents · latest <span id="treaty-latest-year">0</span></div>
          <div class="note">How this is computed: records with mechanism = "Treaty bodies".</div>
        </div>
        <div class="tile">
          <h4 id="tile-special">0</h4>
          <div class="meta"><span class="dot special"></span> Special Procedures</div>
          <div class="meta"><div class="share-bar"><div class="share-fill" id="share-special"></div></div> of filtered</div>
          <div class="meta" id="special-documents">0 documents · latest <span id="special-latest-year">0</span></div>
          <div class="note">How this is computed: records with mechanism = "Special Procedures".</div>
        </div>
      </div>

      <div class="fig-title">FIG.01 <span id="fig01-title">Ten most frequent themes among 0 filtered records</span></div>
      <div class="chart-container">
        <canvas id="theme-chart"></canvas>
      </div>
      <div class="fig-source">Source: computed from the filtered set of records.</div>
      <div class="note">How this is computed: count of records carrying each theme; a record can carry several themes, so the bars add up to more than the record count.</div>
      <table>
        <caption>Ten most frequent themes in the filtered set</caption>
        <thead>
          <tr>
            <th scope="col">Theme</th>
            <th scope="col">Records</th>
            <th scope="col">% of filtered</th>
            <th scope="col">Years</th>
          </tr>
        </thead>
        <tbody id="theme-table-body"></tbody>
      </table>
      <div class="fig-source">Source: computed from the filtered set of records.</div>

      <div class="fig-title">FIG.02 <span id="fig02-title">Records per year by mechanism</span></div>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <div class="fig-source">Source: computed from the filtered set of records.</div>
      <div class="note">How this is computed: count of records per year per mechanism; empty years are gaps in the data.</div>
    </div>

    <div id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" tabindex="0" hidden>
      <div class="search-box">
        <input type="text" id="search-input" placeholder="Search records, e.g. torture">
        <div class="note">literal match, not synonyms</div>
      </div>
      <div class="note" id="table-caption">Showing <span id="table-showing">0</span> of <span id="table-matching">0</span> matching records.</div>
      <table>
        <caption>UN human rights recommendations and observations: Kenya <span id="table-sort-hint">(newest first)</span></caption>
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Body</th>
            <th scope="col">Symbol</th>
            <th scope="col">Para.</th>
            <th scope="col">Recommending State</th>
            <th scope="col">First line</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
      <div class="pagination">
        <button id="show-more">Show 50 more</button>
      </div>
    </div>

    <div id="panel-03" class="tab-panel" role="tabpanel" aria-labelledby="tab-03" tabindex="0" hidden>
      <h2>03 CHECK</h2>
      <h3>Check this dashboard</h3>
      <div class="check-panel" id="check-panel"></div>

      <h3>Check the UN's labels on a random sample</h3>
      <div class="sample-check">
        <div class="controls">
          <button id="draw-sample">Check 10 at random</button>
          <button id="redraw-sample">Draw again</button>
          <div class="seed-box">
            <span>with seed</span>
            <input type="number" id="sample-seed" min="1" max="9999" value="1">
          </div>
        </div>
        <div class="tally" id="sample-tally">Themes: 0 fit, 0 don't, 0 unsure of 0 judged (seed: 1). This is your judgement; nothing is sent anywhere.</div>
        <div id="sample-cards"></div>
      </div>
    </div>

    <div id="panel-04" class="tab-panel" role="tabpanel" aria-labelledby="tab-04" tabindex="0" hidden>
      <h2>04 METHOD & EXPORT</h2>
      <h3>How each number is computed</h3>
      <p>The dashboard counts and filters the records in the file. Every number is computed by a loop over the records in JavaScript; nothing is estimated.</p>
      <ul>
        <li><strong>Headline total</strong>: count of all records in the file. The breakdown counts records per <code>type</code>.</li>
        <li><strong>Documents</strong>: number of distinct <code>symbol</code>. <strong>Years</strong>: minimum and maximum <code>year</code>.</li>
        <li><strong>Filters</strong>: exact match on the field. Year: <code>year</code> inclusive between the two selects. SDG: <code>sdgs.includes(goal)</code>. Keyword: every word must occur as a substring of <code>text</code> or <code>symbol</code>.</li>
        <li><strong>Theme counts</strong>: for each record in the filtered set, each value in <code>themes</code> counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = min and max <code>year</code> of the filtered records carrying that theme.</li>
        <li><strong>Timeline</strong>: records per <code>year</code> per <code>mechanism</code> in the filtered set, with zero for missing combinations.</li>
        <li><strong>Paragraph number</strong>: the first match of <code>/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/</code> on <code>text</code>; the captured group is the number. No match means no number.</li>
        <li><strong>Recommending State</strong>: only for UPR. Take the trailing run of parenthesised groups, split into groups, strip outer parentheses and trim. A group is accepted as a State only if it has no comma and at most 60 characters; otherwise "State not found".</li>
        <li><strong>Citation</strong>: <code>symbol</code> + ", para. " + paragraph number when one was found; otherwise <code>symbol</code>.</li>
      </ul>

      <div class="export-section">
        <h3>Take the data with you</h3>
        <div class="actions">
          <button id="download-csv">Download CSV of the current filter</button>
          <button id="copy-summary">Copy summary</button>
        </div>
        <div class="data-source">
          <p>Data source: <a id="export-source" href="#" target="_blank"></a> · Licence: <a href="https://creativecommons.org/licenses/by-nc/3.0/" target="_blank">CC BY-NC 3.0</a> · Built on <span id="export-date"></span></p>
        </div>
      </div>
    </div>
  </main>
</div>

<footer>
  Built on OHCHR UHRI data · <span id="footer-count"></span> records · <a id="footer-source" href="#" target="_blank">source</a>
</footer>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const data = window.WORKSHOP_DATA.uhri;
  const country = data.country;
  const sdgNames = data.sdg_names;
  const records = data.records;
  const source = data.source;
  const sourceUrl = data.source_url;
  const built = data.built;
  const count = Number(data.count);

  // Header
  document.getElementById('country-label').textContent = country;
  document.getElementById('country-name').textContent = country;
  document.getElementById('source-link').textContent = source;
  document.getElementById('source-link').href = sourceUrl;
  document.getElementById('record-count').textContent = count.toLocaleString();
  document.getElementById('built-date').textContent = new Date(built).toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'});
  document.getElementById('export-source').textContent = source;
  document.getElementById('export-source').href = sourceUrl;
  document.getElementById('export-date').textContent = new Date(built).toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'});
  document.getElementById('footer-count').textContent = count.toLocaleString();
  document.getElementById('footer-source').textContent = source;
  document.getElementById('footer-source').href = sourceUrl;

  // Distinct years
  const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
  const yearFromSelect = document.getElementById('year-from');
  const yearToSelect = document.getElementById('year-to');
  years.forEach(year => {
    const optionFrom = document.createElement('option');
    optionFrom.value = year;
    optionFrom.textContent = year;
    yearFromSelect.appendChild(optionFrom);

    const optionTo = document.createElement('option');
    optionTo.value = year;
    optionTo.textContent = year;
    yearToSelect.appendChild(optionTo);
  });

  // Distinct mechanisms, bodies, types
  const mechanisms = [...new Set(records.map(r => r.mechanism))];
  const bodies = [...new Set(records.map(r => r.body))].sort();
  const types = [...new Set(records.map(r => r.type))].sort();

  // Body options per mechanism
  const bodyOptions = document.getElementById('body-options');
  const updateBodyOptions = (mechanism) => {
    bodyOptions.innerHTML = '';
    const label = document.createElement('label');
    label.innerHTML = '<input type="radio" name="body" value="all" checked> All bodies';
    bodyOptions.appendChild(label);
    const filteredBodies = mechanism === 'all' ? bodies : [...new Set(records.filter(r => r.mechanism === mechanism).map(r => r.body))].sort();
    filteredBodies.forEach(body => {
      const count = records.filter(r => r.body === body && (mechanism === 'all' || r.mechanism === mechanism)).length;
      const label = document.createElement('label');
      label.innerHTML = `<input type="radio" name="body" value="${body}"> ${body} (${count})`;
      bodyOptions.appendChild(label);
    });
  };
  updateBodyOptions('all');

  // Type options
  const typeOptions = document.getElementById('type-options');
  types.forEach(type => {
    const count = records.filter(r => r.type === type).length;
    const label = document.createElement('label');
    label.innerHTML = `<input type="radio" name="type" value="${type}"> ${type} (${count})`;
    typeOptions.appendChild(label);
  });

  // SDG options
  const sdgSelect = document.getElementById('sdg-select');
  const sdgsPresent = [...new Set(records.flatMap(r => r.sdgs || []))].sort((a, b) => a - b);
  sdgsPresent.forEach(goal => {
    const option = document.createElement('option');
    option.value = goal;
    option.textContent = `${goal} ${sdgNames[goal]}`;
    sdgSelect.appendChild(option);
  });

  // State extraction for UPR
  const stateGroup = document.getElementById('state-group');
  const stateSelect = document.getElementById('state-select');
  const uprStatesLink = document.getElementById('upr-states-link');
  let stateCounts = {};
  const extractStates = (text) => {
    const stateRegex = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
    const groupRegex = /\((?:[^()]|\([^()]*\))*\)/g;
    const match = text.match(stateRegex);
    if (!match) return [];
    const groups = match[0].match(groupRegex) || [];
    return groups.map(group => {
      const state = group.slice(1, -1).trim();
      if (state.includes(',') || state.length > 60) return null;
      return state;
    }).filter(Boolean);
  };
  const updateStateOptions = (filteredRecords) => {
    stateCounts = {};
    filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review').forEach(r => {
      const states = extractStates(r.text);
      states.forEach(state => {
        stateCounts[state] = (stateCounts[state] || 0) + 1;
      });
    });
    stateSelect.innerHTML = '<option value="all">All States</option>';
    Object.entries(stateCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).forEach(([state, count]) => {
      const option = document.createElement('option');
      option.value = state;
      option.textContent = `${state} (${count})`;
      stateSelect.appendChild(option);
    });
    const topStates = Object.entries(stateCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
    uprStatesLink.onclick = (e) => {
      e.preventDefault();
      const list = topStates.map(([state, count]) => `${state}: ${count}`).join(', ');
      alert(`Ten States that made most recommendations to ${country}:\n\n${list}`);
    };
  };

  // Filter state
  let filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    yearFrom: '',
    yearTo: '',
    sdg: 'all',
    state: 'all'
  };

  const applyFilters = () => {
    let filtered = records;

    // Keyword
    if (filters.keyword) {
      const terms = filters.keyword.toLowerCase().split(/\s+/).filter(term => term);
      filtered = filtered.filter(r => {
        const text = r.text.toLowerCase();
        const symbol = r.symbol.toLowerCase();
        return terms.every(term => text.includes(term) || symbol.includes(term));
      });
    }

    // Mechanism
    if (filters.mechanism !== 'all') {
      filtered = filtered.filter(r => r.mechanism === filters.mechanism);
    }

    // Body
    if (filters.body !== 'all') {
      filtered = filtered.filter(r => r.body === filters.body);
    }

    // Type
    if (filters.type !== 'all') {
      filtered = filtered.filter(r => r.type === filters.type);
    }

    // Year
    if (filters.yearFrom) {
      const year = Number(filters.yearFrom);
      filtered = filtered.filter(r => r.year >= year);
    }
    if (filters.yearTo) {
      const year = Number(filters.yearTo);
      filtered = filtered.filter(r => r.year <= year);
    }

    // SDG
    if (filters.sdg !== 'all') {
      const goal = Number(filters.sdg);
      filtered = filtered.filter(r => (r.sdgs || []).includes(goal));
    }

    // State (only for UPR)
    if (filters.state !== 'all' && filters.mechanism === 'Universal Periodic Review') {
      filtered = filtered.filter(r => {
        const states = extractStates(r.text);
        return states.includes(filters.state);
      });
    }

    return filtered;
  };

  const updateUI = () => {
    const filtered = applyFilters();
    const matchingCount = filtered.length;
    const totalCount = records.length;

    // Matching count and bar
    document.getElementById('matching-count').textContent = matchingCount.toLocaleString();
    document.getElementById('total-count').textContent = totalCount.toLocaleString();
    const barFill = document.getElementById('matching-bar');
    barFill.style.width = `${(matchingCount / totalCount) * 100}%`;

    // Active filters
    const activeFiltersContainer = document.getElementById('active-filters');
    activeFiltersContainer.innerHTML = '';
    if (filters.keyword) {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Keyword: ${filters.keyword}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.keyword = '';
        document.getElementById('keyword-input').value = '';
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.mechanism !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Mechanism: ${filters.mechanism}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.mechanism = 'all';
        document.querySelector('input[name="mechanism"][value="all"]').checked = true;
        updateBodyOptions('all');
        stateGroup.hidden = true;
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.body !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Body: ${filters.body}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.body = 'all';
        document.querySelector('input[name="body"][value="all"]').checked = true;
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.type !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Type: ${filters.type}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.type = 'all';
        document.querySelector('input[name="type"][value="all"]').checked = true;
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.yearFrom) {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Year from: ${filters.yearFrom}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.yearFrom = '';
        yearFromSelect.value = '';
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.yearTo) {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Year to: ${filters.yearTo}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.yearTo = '';
        yearToSelect.value = '';
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.sdg !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `SDG: ${filters.sdg} ${sdgNames[filters.sdg]}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.sdg = 'all';
        sdgSelect.value = 'all';
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }
    if (filters.state !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `State: ${filters.state}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.onclick = () => {
        filters.state = 'all';
        stateSelect.value = 'all';
        updateUI();
      };
      chip.appendChild(removeBtn);
      activeFiltersContainer.appendChild(chip);
    }

    // Tiles
    const totalRecords = records.length;
    const totalDocuments = new Set(records.map(r => r.symbol)).size;
    const totalYears = `${years[0]}–${years[years.length - 1]}`;
    document.getElementById('total-records').textContent = totalRecords.toLocaleString();
    document.getElementById('total-documents').textContent = totalDocuments.toLocaleString();
    document.getElementById('total-years').textContent = totalYears;

    const typeBreakdown = types.map(type => {
      const count = records.filter(r => r.type === type).length;
      return `${type}: ${count}`;
    }).join(', ');
    document.getElementById('type-breakdown').textContent = typeBreakdown;

    const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
    const uprDocuments = new Set(uprRecords.map(r => r.symbol)).size;
    const uprLatestYear = Math.max(...uprRecords.map(r => r.year));
    document.getElementById('tile-upr').textContent = uprRecords.length.toLocaleString();
    document.getElementById('upr-documents').textContent = `${uprDocuments} documents · latest ${uprLatestYear}`;
    document.getElementById('share-upr').style.width = `${(uprRecords.length / totalRecords) * 100}%`;

    const treatyRecords = records.filter(r => r.mechanism === 'Treaty bodies');
    const treatyDocuments = new Set(treatyRecords.map(r => r.symbol)).size;
    const treatyLatestYear = Math.max(...treatyRecords.map(r => r.year));
    document.getElementById('tile-treaty').textContent = treatyRecords.length.toLocaleString();
    document.getElementById('treaty-documents').textContent = `${treatyDocuments} documents · latest ${treatyLatestYear}`;
    document.getElementById('share-treaty').style.width = `${(treatyRecords.length / totalRecords) * 100}%`;

    const specialRecords = records.filter(r => r.mechanism === 'Special Procedures');
    const specialDocuments = new Set(specialRecords.map(r => r.symbol)).size;
    const specialLatestYear = Math.max(...specialRecords.map(r => r.year));
    document.getElementById('tile-special').textContent = specialRecords.length.toLocaleString();
    document.getElementById('special-documents').textContent = `${specialDocuments} documents · latest ${specialLatestYear}`;
    document.getElementById('share-special').style.width = `${(specialRecords.length / totalRecords) * 100}%`;

    // Share of filtered
    const uprFiltered = filtered.filter(r => r.mechanism === 'Universal Periodic Review').length;
    const treatyFiltered = filtered.filter(r => r.mechanism === 'Treaty bodies').length;
    const specialFiltered = filtered.filter(r => r.mechanism === 'Special Procedures').length;
    document.getElementById('share-upr').style.width = `${(uprFiltered / matchingCount) * 100}%`;
    document.getElementById('share-treaty').style.width = `${(treatyFiltered / matchingCount) * 100}%`;
    document.getElementById('share-special').style.width = `${(specialFiltered / matchingCount) * 100}%`;

    // Theme chart and table
    const themeCounts = {};
    filtered.forEach(r => {
      (r.themes || []).forEach(theme => {
        themeCounts[theme] = (themeCounts[theme] || 0) + 1;
      });
    });
    const topThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);

    document.getElementById('fig01-title').textContent = `Ten most frequent themes among ${matchingCount.toLocaleString()} filtered records`;
    const themeChartCtx = document.getElementById('theme-chart').getContext('2d');
    if (window.themeChart) window.themeChart.destroy();
    window.themeChart = new Chart(themeChartCtx, {
      type: 'bar',
      data: {
        labels: topThemes.map(([theme]) => theme),
        datasets: [{
          label: 'Records',
          data: topThemes.map(([, count]) => count),
          backgroundColor: '#9b2335',
          borderWidth: 0
        }]
      },
      options: {
        indexAxis: 'y',
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 } },
          y: { grid: { display: false } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => {
                const theme = context.label;
                const count = context.raw;
                const pct = ((count / matchingCount) * 100).toFixed(1);
                return `${count} (${pct}%)`;
              }
            }
          }
        },
        onClick: (e, activeEls) => {
          if (activeEls.length) {
            const idx = activeEls[0].index;
            const theme = topThemes[idx][0];
            filters.keyword = theme;
            document.getElementById('keyword-input').value = theme;
            updateUI();
          }
        }
      }
    });

    const themeTableBody = document.getElementById('theme-table-body');
    themeTableBody.innerHTML = '';
    topThemes.forEach(([theme, count]) => {
      const pct = ((count / matchingCount) * 100).toFixed(1);
      const themeRecords = filtered.filter(r => (r.themes || []).includes(theme));
      const years = [...new Set(themeRecords.map(r => r.year))].sort((a, b) => a - b);
      const yearRange = `${years[0]}–${years[years.length - 1]}`;

      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${theme}</td>
        <td>${count.toLocaleString()}</td>
        <td>${pct}%</td>
        <td>${yearRange}</td>
      `;
      themeTableBody.appendChild(row);
    });

    // Timeline chart
    const timelineData = {};
    years.forEach(year => {
      timelineData[year] = {
        'Universal Periodic Review': 0,
        'Treaty bodies': 0,
        'Special Procedures': 0
      };
    });
    filtered.forEach(r => {
      timelineData[r.year][r.mechanism]++;
    });
    const timelineChartCtx = document.getElementById('timeline-chart').getContext('2d');
    if (window.timelineChart) window.timelineChart.destroy();
    window.timelineChart = new Chart(timelineChartCtx, {
      type: 'bar',
      data: {
        labels: years,
        datasets: [
          {
            label: 'Universal Periodic Review',
            data: years.map(year => timelineData[year]['Universal Periodic Review']),
            backgroundColor: '#c2410c'
          },
          {
            label: 'Treaty bodies',
            data: years.map(year => timelineData[year]['Treaty bodies']),
            backgroundColor: '#0f766e'
          },
          {
            label: 'Special Procedures',
            data: years.map(year => timelineData[year]['Special Procedures']),
            backgroundColor: '#7c3aed'
          }
        ]
      },
      options: {
        scales: {
          x: { stacked: true },
          y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } }
        },
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${context.raw}`;
              }
            }
          }
        }
      }
    });
    document.getElementById('fig02-title').textContent = `Records per year by mechanism (${matchingCount.toLocaleString()} filtered)`;

    // Table
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';
    const searchInput = document.getElementById('search-input');
    const searchTerms = searchInput.value.toLowerCase().split(/\s+/).filter(term => term);
    let tableRecords = filtered;
    if (searchTerms.length) {
      tableRecords = tableRecords.filter(r => {
        const text = r.text.toLowerCase();
        const symbol = r.symbol.toLowerCase();
        return searchTerms.every(term => text.includes(term) || symbol.includes(term));
      });
    }
    document.getElementById('table-showing').textContent = '0';
    document.getElementById('table-matching').textContent = tableRecords.length.toLocaleString();

    let sortDirection = -1; // -1 = newest first, 1 = oldest first
    const sortRecords = () => {
      tableRecords.sort((a, b) => {
        if (a.date !== b.date) return sortDirection * (new Date(a.date) - new Date(b.date));
        if (a.body !== b.body) return a.body.localeCompare(b.body);
        const aPara = a.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)?.[1] || '';
        const bPara = b.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)?.[1] || '';
        return aPara.localeCompare(bPara, undefined, {numeric: true});
      });
    };
    sortRecords();

    const dateHeader = tableBody.parentNode.querySelector('th:first-child');
    dateHeader.onclick = () => {
      sortDirection *= -1;
      sortRecords();
      renderTable();
      document.getElementById('table-sort-hint').textContent = sortDirection === -1 ? '(newest first)' : '(oldest first)';
    };

    let tableOffset = 0;
    const renderTable = () => {
      const rows = tableRecords.slice(tableOffset, tableOffset + 50);
      tableBody.innerHTML = '';
      rows.forEach(r => {
        const paraMatch = r.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
        const paraNum = paraMatch ? paraMatch[1] : '';
        const firstLine = r.text.substring(0, 120).replace(/\s+$/, '');
        const firstLineCut = firstLine.length < r.text.length ? firstLine + '…' : firstLine;

        let states = [];
        if (r.mechanism === 'Universal Periodic Review') {
          states = extractStates(r.text);
        }

        const row = document.createElement('tr');
        row.className = 'expand-row';
        row.innerHTML = `
          <td>${new Date(r.date).toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'})}</td>
          <td>${r.body}</td>
          <td><a href="${r.doc_url}" target="_blank">${r.symbol}</a></td>
          <td>${paraNum}</td>
          <td>${states.length ? states.join(', ') : '—'}</td>
          <td><button>${searchTerms.reduce((text, term) => text.replace(new RegExp(term, 'gi'), match => `<mark>${match}</mark>`), firstLineCut)}</button></td>
        `;
        row.onclick = () => {
          const expanded = row.classList.contains('expanded');
          document.querySelectorAll('.expanded').forEach(el => el.classList.remove('expanded'));
          if (!expanded) {
            row.classList.add('expanded');
            const expandedTd = document.createElement('td');
            expandedTd.colSpan = 6;
            expandedTd.innerHTML = `
              <div class="para-num">${paraNum}</div>
              <div class="text">${searchTerms.reduce((text, term) => text.replace(new RegExp(term, 'gi'), match => `<mark>${match}</mark>`), r.text)}</div>
              <div class="labels">
                ${(r.themes || []).map(theme => `<span class="label">${theme}</span>`).join('')}
                ${(r.sdgs || []).map(goal => `<span class="label">SDG ${goal} ${sdgNames[goal]}</span>`).join('')}
                ${(r.sdg_targets || []).map(target => `<span class="label">${target}</span>`).join('')}
                ${(r.affected_persons || []).map(person => `<span class="label">${person}</span>`).join('')}
                ${r.section ? `<span class="label">${r.section}</span>` : ''}
              </div>
              <div class="actions">
                <button class="copy-citation">Copy citation</button>
                <button onclick="window.open('${r.doc_url}', '_blank')">Open the UN document</button>
              </div>
            `;
            row.appendChild(expandedTd);
            const copyBtn = expandedTd.querySelector('.copy-citation');
            copyBtn.onclick = () => {
              const citation = paraNum ? `${r.symbol}, para. ${paraNum}` : r.symbol;
              navigator.clipboard.writeText(citation).then(() => {
                copyBtn.textContent = 'Copied!';
                copyBtn.classList.add('copied');
                setTimeout(() => {
                  copyBtn.textContent = paraNum ? 'Copy citation' : '(no paragraph number in this extract)';
                  copyBtn.classList.remove('copied');
                }, 2000);
              });
            };
          }
        };
        tableBody.appendChild(row);
      });
      document.getElementById('table-showing').textContent = Math.min(tableOffset + 50, tableRecords.length).toLocaleString();
      document.getElementById('show-more').disabled = tableOffset + 50 >= tableRecords.length;
    };
    renderTable();

    document.getElementById('show-more').onclick = () => {
      tableOffset += 50;
      renderTable();
    };

    // State filter visibility
    stateGroup.hidden = filters.mechanism !== 'Universal Periodic Review';
    if (filters.mechanism === 'Universal Periodic Review') {
      updateStateOptions(filtered);
    }

    // Checks
    const checkPanel = document.getElementById('check-panel');
    checkPanel.innerHTML = '';

    const addCheck = (label, actual, expected, pass, details = '') => {
      const item = document.createElement('div');
      item.className = `check-item ${pass ? 'pass' : 'fail'}`;
      item.innerHTML = `
        <span>${label}</span>
        <span class="values">${actual} / ${expected}</span>
      `;
      if (details) {
        const detailsEl = document.createElement('div');
        detailsEl.className = 'details';
        detailsEl.textContent = details;
        item.appendChild(detailsEl);
      }
      checkPanel.appendChild(item);
    };

    // Record count
    addCheck('Record count', records.length, count, records.length === count);

    // Partitions
    const mechanismCounts = mechanisms.map(m => records.filter(r => r.mechanism === m).length);
    const mechanismSum = mechanismCounts.reduce((a, b) => a + b, 0);
    addCheck('Mechanism partition', mechanismSum, records.length, mechanismSum === records.length);

    const bodyCounts = bodies.map(b => records.filter(r => r.body === b).length);
    const bodySum = bodyCounts.reduce((a, b) => a + b, 0);
    addCheck('Body partition', bodySum, records.length, bodySum === records.length);

    const yearCounts = years.map(y => records.filter(r => r.year === y).length);
    const yearSum = yearCounts.reduce((a, b) => a + b, 0);
    addCheck('Year partition', yearSum, records.length, yearSum === records.length);

    // Type partition
    const typeCounts = types.map(t => records.filter(r => r.type === t).length);
    const typeSum = typeCounts.reduce((a, b) => a + b, 0);
    addCheck('Type partition', typeSum, records.length, typeSum === records.length);

    // Chart against table
    const chartSum = topThemes.reduce((a, [, count]) => a + count, 0);
    addCheck('Theme chart sum', chartSum, matchingCount, chartSum >= matchingCount, 'A record can carry several themes, so the sum can be larger than the record count.');

    // Links
    const linkErrors = records.filter(r => !r.doc_url.startsWith('https://docs.un.org/') || !r.doc_url.toLowerCase().includes(encodeURIComponent(r.symbol).toLowerCase()));
    addCheck('Document links', linkErrors.length, 0, linkErrors.length === 0, linkErrors.map(r => `${r.symbol}: ${r.doc_url}`).join('\n'));

    // Paragraph numbers
    const paraStats = {};
    mechanisms.forEach(m => {
      const mechRecords = records.filter(r => r.mechanism === m);
      const withPara = mechRecords.filter(r => r.text.match(/^\d{1,3}(?:\.\d{1,3})?\.?\s/)).length;
      paraStats[m] = { total: mechRecords.length, withPara };
    });
    const uprParaPct = (paraStats['Universal Periodic Review'].withPara / paraStats['Universal Periodic Review'].total) * 100;
    addCheck('Paragraph numbers (UPR)', `${uprParaPct.toFixed(1)}%`, '100%', uprParaPct === 100, `Expected 100% for UPR; ${paraStats['Universal Periodic Review'].total - paraStats['Universal Periodic Review'].withPara} records without a number.`);

    // States found
    const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
    const uprWithState = uprRecords.filter(r => extractStates(r.text).length > 0).length;
    const uprWithoutState = uprRecords.filter(r => extractStates(r.text).length === 0);
    addCheck('States found (UPR)', uprWithState, uprRecords.length, uprWithState === uprRecords.length, uprWithoutState.map(r => `${r.symbol}: "${r.text}"`).join('\n'));

    // Duplicates and gaps
    const distinctIds = new Set(records.map(r => r.id)).size;
    addCheck('Distinct IDs', distinctIds, records.length, distinctIds === records.length);

    const textCounts = {};
    records.forEach(r => {
      textCounts[r.text] = (textCounts[r.text] || 0) + 1;
    });
    const duplicateTexts = Object.values(textCounts).filter(v => v > 1).length;
    addCheck('Duplicate texts', duplicateTexts, 0, duplicateTexts === 0);

    const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
    addCheck('Records without themes', noThemes, 0, noThemes === 0);

    const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    addCheck('Records without SDGs', noSdgs, 0, noSdgs === 0);

    const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
    addCheck('Records without affected persons', noAffected, 0, noAffected === 0);

    // Sample check
    const sampleCards = document.getElementById('sample-cards');
    sampleCards.innerHTML = '';
    const sampleTally = document.getElementById('sample-tally');
    let sampleJudgements = {};

    const mulberry32 = (a) => {
      return function() {
        a |= 0; a = a + 0x6D2B79F5 | 0;
        let t = Math.imul(a ^ a >>> 15, 1 | a);
        t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
        return ((t ^ t >>> 14) >>> 0) / 4294967296;
      };
    };

    const drawSample = () => {
      const seed = Number(document.getElementById('sample-seed').value);
      const rng = mulberry32(seed);
      const sample = [...filtered].sort(() => rng() - 0.5).slice(0, 10);
      sampleCards.innerHTML = '';
      sampleJudgements = {};
      sample.forEach((r, i) => {
        const paraMatch = r.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
        const paraNum = paraMatch ? paraMatch[1] : '';

        const card = document.createElement('div');
        card.className = 'sample-card';
        card.innerHTML = `
          <div class="sample-card-header" aria-expanded="false">
            <div>
              <a href="${r.doc_url}" target="_blank">${r.symbol}</a>, para. ${paraNum}
            </div>
            <button class="arrow">▼</button>
          </div>
          <div class="sample-card-body" hidden>
            <div class="text">${r.text}</div>
            <div class="themes">
              ${(r.themes || []).map(theme => `<span class="theme">${theme}</span>`).join('')}
            </div>
            <div class="verdict">
              <button data-verdict="fit">Fits</button>
              <button data-verdict="dont">Doesn't fit</button>
              <button data-verdict="unsure">Unsure</button>
            </div>
          </div>
        `;
        sampleCards.appendChild(card);

        const header = card.querySelector('.sample-card-header');
        const body = card.querySelector('.sample-card-body');
        const arrow = card.querySelector('.arrow');
        header.onclick = () => {
          const expanded = header.getAttribute('aria-expanded') === 'true';
          header.setAttribute('aria-expanded', !expanded);
          body.hidden = expanded;
          arrow.style.transform = expanded ? 'rotate(-90deg)' : 'rotate(0deg)';
        };

        const verdictBtns = card.querySelectorAll('[data-verdict]');
        verdictBtns.forEach(btn => {
          btn.onclick = () => {
            verdictBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            sampleJudgements[i] = btn.dataset.verdict;
            updateSampleTally();
          };
        });
      });
      updateSampleTally();
    };

    const updateSampleTally = () => {
      const fit = Object.values(sampleJudgements).filter(v => v === 'fit').length;
      const dont = Object.values(sampleJudgements).filter(v => v === 'dont').length;
      const unsure = Object.values(sampleJudgements).filter(v => v === 'unsure').length;
      const seed = document.getElementById('sample-seed').value;
      sampleTally.textContent = `Themes: ${fit} fit, ${dont} don't, ${unsure} unsure of ${Object.keys(sampleJudgements).length} judged (seed: ${seed}). This is your judgement; nothing is sent anywhere.`;
    };

    document.getElementById('draw-sample').onclick = drawSample;
    document.getElementById('redraw-sample').onclick = drawSample;

    // Export
    document.getElementById('download-csv').onclick = () => {
      const headers = [
        'Date', 'Year', 'Body', 'Mechanism', 'Type', 'Symbol', 'Document URL',
        'Paragraph number', 'Recommending State', 'Section', 'Text',
        'Themes', 'SDGs', 'SDG targets', 'Affected persons'
      ];
      const rows = filtered.map(r => {
        const paraMatch = r.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
        const paraNum = paraMatch ? paraMatch[1] : '';
        const states = r.mechanism === 'Universal Periodic Review' ? extractStates(r.text).join('; ') : '';
        return [
          r.date,
          r.year,
          r.body,
          r.mechanism,
          r.type,
          r.symbol,
          r.doc_url,
          paraNum,
          states,
          r.section || '',
          `"${r.text.replace(/"/g, '""')}"`,
          `"${(r.themes || []).join('; ')}"`,
          `"${(r.sdgs || []).map(g => `${g} ${sdgNames[g]}`).join('; ')}"`,
          `"${(r.sdg_targets || []).join('; ')}"`,
          `"${(r.affected_persons || []).join('; ')}"`
        ];
      });
      const csv = [
        `# UN human rights recommendations and observations: ${country}`,
        `# Source: ${source} (${sourceUrl})`,
        `# Built: ${built}`,
        `# Filters: ${JSON.stringify(filters)}`,
        `# Records: ${filtered.length}`,
        headers.join(','),
        ...rows.map(row => row.join(','))
      ].join('\n');
      const blob = new Blob([csv], {type: 'text/csv'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `uhri-${country.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    };

    document.getElementById('copy-summary').onclick = () => {
      const summary = `UN human rights recommendations and observations: ${country}
Source: ${source}
Records: ${matchingCount.toLocaleString()} (of ${totalCount.toLocaleString()} in the file)
Documents: ${new Set(filtered.map(r => r.symbol)).size}
Years: ${Math.min(...filtered.map(r => r.year))}–${Math.max(...filtered.map(r => r.year))}

Top themes:
${topThemes.map(([theme, count]) => `- ${theme}: ${count} (${((count / matchingCount) * 100).toFixed(1)}%)`).join('\n')}`;
      navigator.clipboard.writeText(summary).then(() => {
        const btn = document.getElementById('copy-summary');
        btn.textContent = 'Copied!';
        setTimeout(() => {
          btn.textContent = 'Copy summary';
        }, 2000);
      });
    };
  };

  // Event listeners
  document.getElementById('keyword-input').addEventListener('input', (e) => {
    filters.keyword = e.target.value.trim();
    updateUI();
  });

  document.querySelectorAll('input[name="mechanism"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      filters.mechanism = e.target.value;
      updateBodyOptions(e.target.value);
      stateGroup.hidden = e.target.value !== 'Universal Periodic Review';
      updateUI();
    });
  });

  document.querySelectorAll('input[name="body"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      filters.body = e.target.value;
      updateUI();
    });
  });

  document.querySelectorAll('input[name="type"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      filters.type = e.target.value;
      updateUI();
    });
  });

  yearFromSelect.addEventListener('change', (e) => {
    filters.yearFrom = e.target.value;
    if (filters.yearFrom && filters.yearTo && Number(filters.yearFrom) > Number(filters.yearTo)) {
      [filters.yearFrom, filters.yearTo] = [filters.yearTo, filters.yearFrom];
      yearFromSelect.value = filters.yearFrom;
      yearToSelect.value = filters.yearTo;
    }
    updateUI();
  });

  yearToSelect.addEventListener('change', (e) => {
    filters.yearTo = e.target.value;
    if (filters.yearFrom && filters.yearTo && Number(filters.yearFrom) > Number(filters.yearTo)) {
      [filters.yearFrom, filters.yearTo] = [filters.yearTo, filters.yearFrom];
      yearFromSelect.value = filters.yearFrom;
      yearToSelect.value = filters.yearTo;
    }
    updateUI();
  });

  sdgSelect.addEventListener('change', (e) => {
    filters.sdg = e.target.value;
    updateUI();
  });

  stateSelect.addEventListener('change', (e) => {
    filters.state = e.target.value;
    updateUI();
  });

  document.getElementById('clear-filters').onclick = () => {
    filters = {
      keyword: '',
      mechanism: 'all',
      body: 'all',
      type: 'all',
      yearFrom: '',
      yearTo: '',
      sdg: 'all',
      state: 'all'
    };
    document.getElementById('keyword-input').value = '';
    document.querySelector('input[name="mechanism"][value="all"]').checked = true;
    updateBodyOptions('all');
    document.querySelector('input[name="body"][value="all"]').checked = true;
    document.querySelector('input[name="type"][value="all"]').checked = true;
    yearFromSelect.value = '';
    yearToSelect.value = '';
    sdgSelect.value = 'all';
    stateSelect.value = 'all';
    stateGroup.hidden = true;
    updateUI();
  };

  document.getElementById('search-input').addEventListener('input', (e) => {
    renderTable();
  });

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabPanels = document.querySelectorAll('[role="tabpanel"]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const selected = tab.getAttribute('aria-selected') === 'true';
      if (selected) return;

      tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
      tab.setAttribute('aria-selected', 'true');

      tabPanels.forEach(panel => panel.hidden = true);
      const panelId = tab.getAttribute('aria-controls');
      document.getElementById(panelId).hidden = false;

      // Filter sections visibility
      const filterSections = document.querySelectorAll('#filters .filter-section');
      if (panelId === 'panel-01' || panelId === 'panel-02') {
        filterSections.forEach(section => {
          const heading = section.querySelector('h3 button');
          const content = section.querySelector('div');
          if (section.id === 'filter-keyword-section') {
            heading.setAttribute('aria-expanded', 'true');
            content.hidden = false;
          } else if (section.id === 'filter-mechanism-section') {
            heading.setAttribute('aria-expanded', panelId === 'panel-01' ? 'false' : 'true');
            content.hidden = panelId === 'panel-01';
          } else {
            heading.setAttribute('aria-expanded', 'false');
            content.hidden = true;
          }
        });
      } else {
        filterSections.forEach(section => {
          section.hidden = true;
        });
      }
    });
  });

  // Filter section toggles
  document.querySelectorAll('#filters .filter-section h3 button').forEach(button => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
      const contentId = button.getAttribute('aria-controls');
      document.getElementById(contentId).hidden = expanded;
    });
  });

  // Initial render
  document.getElementById('year-range').textContent = `${years[0]}–${years[years.length - 1]}`;
  document.getElementById('document-count').textContent = new Set(records.map(r => r.symbol)).size.toLocaleString();
  updateUI();
});
</script>
</body>
</html>
```