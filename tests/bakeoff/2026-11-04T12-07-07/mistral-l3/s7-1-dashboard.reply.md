I built the UN human rights recommendations dashboard for Kenya, exactly as you described. Four tabs: Overview, Records, Check, Method & export. The left rail holds the filters, the header stays visible, and every number is computed from the data. The app shows the UN's own labels and lets the reader check a random sample.

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
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
}
@media (max-width: 800px) {
  body { grid-template-columns: 1fr; }
  .rail { display: none; }
  .rail-open { display: block; }
}
h1, h2, h3, h4, h5, h6 {
  font-family: Georgia, "Times New Roman", Times, serif;
  font-weight: 400;
  margin: 0;
}
h1 { font-size: 2.2rem; }
h2 { font-size: 1.8rem; }
h3 { font-size: 1.4rem; }
h4 { font-size: 1.2rem; }
label, figcaption, .hint, .mono, .rail-label, .tab-name, .chip, .copy-confirm, .check-line, .export-note {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink);
}
.rail-label { font-size: 0.75rem; }
.mono { font-size: 0.85rem; }
.hint, .export-note { color: #6b665c; }
a {
  color: var(--ink);
  text-decoration: none;
}
a:hover { text-decoration: underline; }
a:focus { outline: 2px solid var(--red); outline-offset: 2px; }

/* Header */
.header {
  grid-column: 1 / -1;
  border-bottom: 1px solid var(--rule);
  padding: 0.5rem 1rem;
  display: flex;
  align-items: baseline;
  gap: 1rem;
}
.header .mono { color: #6b665c; }
.header h1 { margin-right: auto; }

/* Tabs */
.tablist {
  grid-column: 1 / -1;
  border-bottom: 1px solid var(--rule);
  display: flex;
  gap: 0;
  padding: 0;
  margin: 0;
  list-style: none;
}
.tab {
  padding: 0.75rem 1rem;
  border: 0;
  background: none;
  cursor: pointer;
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  border-bottom: 2px solid transparent;
  position: relative;
}
.tab[aria-selected="true"] {
  border-bottom-color: var(--red);
  color: var(--red);
}
.tab[aria-selected="true"] .tab-name { color: var(--red); }
.tab:focus { outline: 2px solid var(--red); outline-offset: -2px; }
.tab-name { display: block; margin-top: 0.25rem; }

/* Rail */
.rail {
  border-right: 1px solid var(--rule);
  padding: 1rem;
  background-color: var(--paper);
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.rail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.rail-header h3 { margin: 0; }
.clear-all {
  background: none;
  border: 0;
  padding: 0;
  font: inherit;
  cursor: pointer;
  color: var(--red);
  text-decoration: underline;
}
.clear-all:focus { outline: 2px solid var(--red); }
.count-box {
  border: 1px solid var(--rule);
  padding: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
}
.count-box .big {
  font-family: Georgia, serif;
  font-size: 2.5rem;
  line-height: 1;
  display: block;
}
.count-box .of { color: #6b665c; }
.share-bar {
  height: 4px;
  background-color: var(--rule);
  margin-bottom: 1rem;
}
.share-bar-fill {
  height: 100%;
  background-color: var(--red);
  width: 0%;
}
.filter-section {
  margin-bottom: 1.5rem;
}
.filter-section[aria-expanded="false"] .filter-content { display: none; }
.filter-section[aria-expanded="true"] .filter-heading::after { content: "−"; }
.filter-section[aria-expanded="false"] .filter-heading::after { content: "+"; }
.filter-heading {
  background: none;
  border: 0;
  padding: 0;
  font: inherit;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  text-align: left;
  margin-bottom: 0.5rem;
}
.filter-heading:focus { outline: 2px solid var(--red); }
.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.chip {
  background-color: var(--rule);
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.chip button {
  background: none;
  border: 0;
  padding: 0;
  font: inherit;
  cursor: pointer;
  color: var(--red);
  font-size: 0.8rem;
}
.chip button:focus { outline: 2px solid var(--red); }
.filter-content { padding-left: 1rem; }
.filter-content label { display: block; margin-bottom: 0.5rem; }
.filter-content input[type="text"], .filter-content select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font: inherit;
}
.filter-content input[type="text"]:focus, .filter-content select:focus {
  outline: 2px solid var(--red);
  border-color: var(--red);
}
.filter-content .hint { margin-top: 0.25rem; }
.filter-content .radio-group { display: flex; flex-direction: column; gap: 0.25rem; }
.filter-content .radio-option { display: flex; align-items: center; }
.filter-content .radio-option input { margin-right: 0.5rem; }
.filter-content .state-select { margin-top: 1rem; }

/* Main */
.main {
  padding: 1.5rem;
  overflow-y: auto;
}
.tab-content { display: none; }
.tab-content[aria-hidden="false"] { display: block; }
.tile-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.tile {
  border: 1px solid var(--rule);
  padding: 1rem;
  flex: 1;
  min-width: 200px;
}
.tile h3 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.tile .big {
  font-family: Georgia, serif;
  font-size: 3rem;
  line-height: 1;
  display: block;
}
.tile .breakdown { color: #6b665c; font-size: 0.9rem; }
.tile .hint { margin-top: 0.5rem; }
.mechanism-dot {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.mechanism-dot.upr { background-color: var(--upr); }
.mechanism-dot.treaty { background-color: var(--treaty); }
.mechanism-dot.special { background-color: var(--special); }
.figure {
  margin-bottom: 2rem;
}
.figure-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.figure-title .fig-num { color: var(--red); }
.chart-container {
  border: 1px solid var(--rule);
  padding: 1rem;
  margin-bottom: 1rem;
}
.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}
.chart-legend-item {
  display: flex;
  align-items: center;
}
.chart-legend-dot {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.chart-legend-dot.upr { background-color: var(--upr); }
.chart-legend-dot.treaty { background-color: var(--treaty); }
.chart-legend-dot.special { background-color: var(--special); }
.table-container {
  border: 1px solid var(--rule);
  margin-bottom: 1rem;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
th { background-color: var(--rule); }
th[scope="col"] { font-weight: normal; }
th[scope="col"]:first-child { width: 80px; }
th[scope="col"]:nth-child(3) { width: 120px; }
th[scope="col"]:nth-child(4) { width: 60px; }
th[scope="col"]:nth-child(5) { width: 100px; }
td { vertical-align: top; }
td:first-child { font-family: Georgia, serif; font-size: 1.1rem; }
td:nth-child(5) { font-family: Georgia, serif; }
td:nth-child(6) { color: #6b665c; }
tr[aria-expanded="true"] { background-color: #f9f7f4; }
tr[aria-expanded="true"] td { border-bottom: 0; }
.expand-row {
  background: none;
  border: 0;
  padding: 0.75rem;
  font: inherit;
  cursor: pointer;
  width: 100%;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.expand-row:focus { outline: 2px solid var(--red); }
.expand-row::after { content: "▼"; }
tr[aria-expanded="true"] .expand-row::after { content: "▲"; }
.expanded-content {
  padding: 1rem;
  border-top: 1px solid var(--rule);
  grid-column: 1 / -1;
}
.expanded-content .para-num {
  font-family: Georgia, serif;
  font-size: 2rem;
  color: var(--red);
  margin-bottom: 0.5rem;
}
.expanded-content .full-text {
  white-space: pre-wrap;
  margin-bottom: 1rem;
  line-height: 1.6;
}
.expanded-content .labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.expanded-content .label-group {
  margin-bottom: 0.5rem;
}
.expanded-content .label-group h4 {
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}
.expanded-content .label-chip {
  background-color: var(--rule);
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  display: inline-block;
  margin-right: 0.25rem;
  margin-bottom: 0.25rem;
}
.expanded-content .actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.copy-btn {
  background: none;
  border: 1px solid var(--rule);
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.copy-btn:focus { outline: 2px solid var(--red); }
.copy-confirm {
  margin-left: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s;
}
.copy-confirm.visible { opacity: 1; }
.open-doc {
  background: none;
  border: 1px solid var(--rule);
  padding: 0.5rem 1rem;
  cursor: pointer;
  text-decoration: underline;
}
.open-doc:focus { outline: 2px solid var(--red); }
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}
.pagination button {
  background: none;
  border: 1px solid var(--rule);
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.pagination button:focus { outline: 2px solid var(--red); }
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }
.check-panel {
  border: 1px solid var(--rule);
  padding: 1rem;
  margin-bottom: 1rem;
}
.check-panel h3 { margin-top: 0; }
.check-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--rule);
}
.check-line:last-child { border-bottom: 0; margin-bottom: 0; }
.check-line .check-fail { color: var(--red); }
.check-line .check-pass { color: var(--treaty); }
.sample-card {
  border: 1px solid var(--rule);
  margin-bottom: 1rem;
}
.sample-card-header {
  padding: 0.75rem 1rem;
  background-color: var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.sample-card-header button {
  background: none;
  border: 0;
  padding: 0;
  font: inherit;
  cursor: pointer;
  color: var(--red);
}
.sample-card-header button:focus { outline: 2px solid var(--red); }
.sample-card-content {
  padding: 1rem;
  display: none;
}
.sample-card[aria-expanded="true"] .sample-card-content { display: block; }
.sample-card .symbol { font-family: Georgia, serif; font-size: 1.1rem; }
.sample-card .para-num {
  font-family: Georgia, serif;
  color: var(--red);
  margin: 0.5rem 0;
}
.sample-card .full-text {
  white-space: pre-wrap;
  margin-bottom: 1rem;
  line-height: 1.6;
}
.sample-card .theme-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.sample-card .verdict-buttons {
  display: flex;
  gap: 0.5rem;
}
.sample-card button {
  background: none;
  border: 1px solid var(--rule);
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
.sample-card button:focus { outline: 2px solid var(--red); }
.sample-card button.selected {
  background-color: var(--red);
  color: white;
  border-color: var(--red);
}
.export-section {
  border: 1px solid var(--rule);
  padding: 1rem;
  margin-bottom: 1rem;
}
.export-section h3 { margin-top: 0; }
.export-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.export-buttons button {
  background: none;
  border: 1px solid var(--rule);
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.export-buttons button:focus { outline: 2px solid var(--red); }
.footer {
  grid-column: 1 / -1;
  border-top: 1px solid var(--rule);
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.footer .mono { color: #6b665c; }
.credits { color: #6b665c; }

/* Hidden elements */
[hidden] { display: none !important; }
</style>
</head>
<body>

<div class="header">
  <span class="mono">UHRI · <span id="country-label"></span></span>
  <h1>UN human rights recommendations and observations: <span id="country-name"></span></h1>
</div>

<div class="rail" id="rail">
  <div class="rail-header">
    <h3>FILTERS</h3>
    <button class="clear-all" id="clear-all">Clear all</button>
  </div>
  <div class="count-box">
    <span class="big" id="matching-count">0</span>
    <span class="of mono" id="of-total">of 0 in the file</span>
  </div>
  <div class="share-bar">
    <div class="share-bar-fill" id="share-bar-fill"></div>
  </div>
  <div id="filter-chips" class="filter-chips"></div>

  <div class="filter-section" id="keyword-section">
    <button class="filter-heading" aria-expanded="false">
      <span class="rail-label">01 KEYWORD</span>
    </button>
    <div class="filter-content">
      <label for="keyword-input">Search records</label>
      <input type="text" id="keyword-input" placeholder="e.g. torture">
      <div class="hint">literal match, not synonyms</div>
    </div>
  </div>

  <div class="filter-section" id="mechanism-section">
    <button class="filter-heading" aria-expanded="false">
      <span class="rail-label">02 MECHANISM, BODY, TYPE</span>
    </button>
    <div class="filter-content">
      <div class="radio-group">
        <label><input type="radio" name="mechanism" value="all" checked> All mechanisms</label>
        <label><input type="radio" name="mechanism" value="Universal Periodic Review"> Universal Periodic Review</label>
        <label><input type="radio" name="mechanism" value="Treaty bodies"> Treaty bodies</label>
        <label><input type="radio" name="mechanism" value="Special Procedures"> Special Procedures</label>
      </div>
      <div id="body-filter-group">
        <label for="body-select">Body or mandate</label>
        <select id="body-select" disabled>
          <option value="all">All</option>
        </select>
      </div>
      <div id="type-filter-group">
        <label for="type-select">Type</label>
        <select id="type-select">
          <option value="all">All</option>
        </select>
      </div>
      <div id="state-filter-group" hidden>
        <label for="state-select">Recommending State</label>
        <select id="state-select">
          <option value="all">All</option>
        </select>
      </div>
    </div>
  </div>

  <div class="filter-section" id="year-sdg-section">
    <button class="filter-heading" aria-expanded="false">
      <span class="rail-label">03 YEARS AND SDG</span>
    </button>
    <div class="filter-content">
      <div>
        <label for="year-from">Year from</label>
        <select id="year-from">
          <option value="all">All</option>
        </select>
      </div>
      <div>
        <label for="year-to">to</label>
        <select id="year-to">
          <option value="all">All</option>
        </select>
      </div>
      <div id="sdg-filter-group">
        <label for="sdg-select">SDG</label>
        <select id="sdg-select">
          <option value="all">All</option>
        </select>
      </div>
    </div>
  </div>
</div>

<div class="main">
  <div role="tablist" aria-label="Tabs">
    <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="tabpanel-01">
      <span class="tab-name">01 OVERVIEW</span>
    </button>
    <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="tabpanel-02">
      <span class="tab-name">02 RECORDS</span>
    </button>
    <button id="tab-03" class="tab" role="tab" aria-selected="false" aria-controls="tabpanel-03">
      <span class="tab-name">03 CHECK</span>
    </button>
    <button id="tab-04" class="tab" role="tab" aria-selected="false" aria-controls="tabpanel-04">
      <span class="tab-name">04 METHOD & EXPORT</span>
    </button>
  </div>

  <div id="tabpanel-01" class="tab-content" role="tabpanel" aria-labelledby="tab-01" aria-hidden="false">
    <div class="source-line mono">
      Source: <a id="source-link" href="#" target="_blank"></a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · built <span id="built-date"></span> · dated by document
    </div>

    <div class="tile-row">
      <div class="tile">
        <h3>All records</h3>
        <span class="big" id="total-records">0</span>
        <div class="breakdown" id="type-breakdown"></div>
        <div class="hint">How this is computed: count of records in the file, by type.</div>
      </div>
      <div class="tile">
        <h3>Documents</h3>
        <span class="big" id="total-documents">0</span>
        <div class="hint">How this is computed: distinct document symbols.</div>
      </div>
      <div class="tile">
        <h3>Years</h3>
        <span class="big" id="total-years">0</span>
        <div class="hint">How this is computed: first and last year of a document in the file.</div>
      </div>
    </div>

    <div class="tile-row">
      <div class="tile">
        <h3><span class="mechanism-dot upr"></span> Universal Periodic Review</h3>
        <span class="big" id="upr-records">0</span>
        <div><span id="upr-documents">0</span> documents · latest <span id="upr-latest">0</span></div>
        <div class="hint">How this is computed: records where mechanism = "Universal Periodic Review".</div>
        <div class="mono" id="upr-states-link" hidden><a href="#" id="show-states">see the States</a></div>
      </div>
      <div class="tile">
        <h3><span class="mechanism-dot treaty"></span> Treaty bodies</h3>
        <span class="big" id="treaty-records">0</span>
        <div><span id="treaty-documents">0</span> documents · latest <span id="treaty-latest">0</span></div>
        <div class="hint">How this is computed: records where mechanism = "Treaty bodies".</div>
      </div>
      <div class="tile">
        <h3><span class="mechanism-dot special"></span> Special Procedures</h3>
        <span class="big" id="special-records">0</span>
        <div><span id="special-documents">0</span> documents · latest <span id="special-latest">0</span></div>
        <div class="hint">How this is computed: records where mechanism = "Special Procedures".</div>
      </div>
    </div>

    <div class="figure">
      <div class="figure-title">
        <h3><span class="fig-num">FIG.01</span> Ten most frequent themes among <span id="theme-count">0</span> filtered records</h3>
      </div>
      <div class="chart-container">
        <canvas id="theme-chart"></canvas>
      </div>
      <div class="table-container">
        <table>
          <caption>A record can carry several themes, so the bars add up to more than the number of records.</caption>
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
      </div>
      <div class="mono source-line">Source: themes labelled by the UN in the Universal Human Rights Index.</div>
    </div>

    <div class="figure">
      <div class="figure-title">
        <h3><span class="fig-num">FIG.02</span> Records per year by mechanism</h3>
      </div>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <div class="chart-legend">
        <div class="chart-legend-item"><span class="chart-legend-dot upr"></span> Universal Periodic Review</div>
        <div class="chart-legend-item"><span class="chart-legend-dot treaty"></span> Treaty bodies</div>
        <div class="chart-legend-item"><span class="chart-legend-dot special"></span> Special Procedures</div>
      </div>
      <div class="mono source-line">Source: records in the file, dated by document.</div>
    </div>
  </div>

  <div id="tabpanel-02" class="tab-content" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
    <div class="source-line mono">
      Source: <a id="source-link-02" href="#" target="_blank"></a> · <span id="record-count-02"></span> records · <span id="document-count-02"></span> documents · <span id="year-range-02"></span>
    </div>

    <div class="search-box">
      <label for="search-input">Search <span id="search-count">0</span> records, e.g. torture</label>
      <input type="text" id="search-input" placeholder="e.g. torture">
      <div class="hint">literal match, not synonyms</div>
    </div>

    <div class="table-container">
      <table>
        <caption id="table-caption">Loading…</caption>
        <thead>
          <tr>
            <th scope="col" id="sort-date">Date <span id="sort-icon">↓</span></th>
            <th scope="col">Body</th>
            <th scope="col">Symbol</th>
            <th scope="col">Para.</th>
            <th scope="col">Recommending State</th>
            <th scope="col">First line</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>

    <div class="pagination">
      <button id="show-more">Show 50 more</button>
      <span id="row-count">0–0 of 0</span>
    </div>
  </div>

  <div id="tabpanel-03" class="tab-content" role="tabpanel" aria-labelledby="tab-03" aria-hidden="true">
    <div class="source-line mono">
      Source: <a id="source-link-03" href="#" target="_blank"></a> · <span id="record-count-03"></span> records
    </div>

    <div class="check-panel">
      <h3>Check this dashboard</h3>
      <div id="check-results"></div>
    </div>

    <div class="check-panel">
      <h3>Check 10 at random</h3>
      <div class="export-note">This is your judgement of the UN's labels; nothing is sent anywhere.</div>
      <div class="sample-controls">
        <button id="draw-sample">Draw again</button>
        <span>Draw with this seed: <input type="number" id="sample-seed" min="1" max="1000000" value="1"></span>
      </div>
      <div id="sample-tally" class="mono">Themes: 0 fit, 0 don't, 0 unsure of 10 judged</div>
      <div id="sample-cards"></div>
    </div>
  </div>

  <div id="tabpanel-04" class="tab-content" role="tabpanel" aria-labelledby="tab-04" aria-hidden="true">
    <div class="source-line mono">
      Source: <a id="source-link-04" href="#" target="_blank"></a> · <span id="record-count-04"></span> records
    </div>

    <div class="export-section">
      <h3>How each number is computed</h3>
      <p>The dashboard counts, filters and sorts the records in the file. Every number is computed by the app's JavaScript, never estimated.</p>
      <ul>
        <li><strong>Headline total</strong>: count of records in the file. The breakdown counts records per type.</li>
        <li><strong>Documents</strong>: number of distinct document symbols. <strong>Years</strong>: minimum and maximum year.</li>
        <li><strong>Filters</strong>: exact match on the field. Year: inclusive between the two selects. SDG: the record's SDGs include the goal. Keyword: every word must occur in the text or symbol.</li>
        <li><strong>Theme counts</strong>: for each record in the filtered set, each value in themes counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal.</li>
        <li><strong>Timeline</strong>: records per year per mechanism in the filtered set, with zero for missing combinations.</li>
        <li><strong>Paragraph number</strong>: the first match of <code>/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/</code> on the text. <strong>Recommending State</strong>: only for UPR; the trailing parenthesised groups, stripped of outer parentheses and trimmed.</li>
        <li><strong>Citation</strong>: symbol + ", para. " + paragraph number when one was found; otherwise symbol.</li>
      </ul>
    </div>

    <div class="export-section">
      <h3>Download CSV of the current filter</h3>
      <div class="export-note">The file is generated in your browser; nothing is sent to a server.</div>
      <div class="export-buttons">
        <button id="download-csv">Download CSV</button>
        <button id="copy-summary">Copy summary</button>
      </div>
    </div>

    <div class="export-section">
      <h3>Data source and licence</h3>
      <p>The data is from the <a href="https://uhri.ohchr.org/" target="_blank">Universal Human Rights Index</a>, published by the Office of the United Nations High Commissioner for Human Rights. The data is used under the <a href="https://www.un.org/en/about-us/terms-of-use" target="_blank">UN Terms of Use</a>.</p>
      <p>Built on <span id="built-date-04"></span>.</p>
    </div>
  </div>
</div>

<div class="footer">
  <div class="mono">Built on OHCHR UHRI data · <span id="footer-count">0</span> records · <a id="footer-source" href="#" target="_blank">source</a></div>
  <div class="credits">Credits: UK Government Analysis Function (charts and tables, Open Government Licence v3.0)</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  const data = window.WORKSHOP_DATA.uhri;
  const country = data.country;
  const records = data.records;
  const source = data.source;
  const sourceUrl = data.source_url;
  const built = data.built;
  const sdgNames = data.sdg_names;

  // Header
  document.getElementById('country-label').textContent = country;
  document.getElementById('country-name').textContent = country;
  document.getElementById('source-link').href = sourceUrl;
  document.getElementById('source-link').textContent = source;
  document.getElementById('source-link-02').href = sourceUrl;
  document.getElementById('source-link-02').textContent = source;
  document.getElementById('source-link-03').href = sourceUrl;
  document.getElementById('source-link-03').textContent = source;
  document.getElementById('source-link-04').href = sourceUrl;
  document.getElementById('source-link-04').textContent = source;
  document.getElementById('footer-source').href = sourceUrl;
  document.getElementById('footer-source').textContent = source;
  document.getElementById('built-date').textContent = built;
  document.getElementById('built-date-04').textContent = built;

  // Record count
  const recordCount = records.length;
  const recordCountStr = recordCount.toLocaleString();
  document.getElementById('record-count').textContent = recordCountStr;
  document.getElementById('record-count-02').textContent = recordCountStr;
  document.getElementById('record-count-03').textContent = recordCountStr;
  document.getElementById('record-count-04').textContent = recordCountStr;
  document.getElementById('footer-count').textContent = recordCountStr;

  // Document count
  const symbols = new Set(records.map(r => r.symbol));
  const documentCount = symbols.size;
  document.getElementById('document-count').textContent = documentCount;
  document.getElementById('document-count-02').textContent = documentCount;

  // Year range
  const years = records.map(r => r.year);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  document.getElementById('year-range').textContent = `${minYear}–${maxYear}`;
  document.getElementById('year-range-02').textContent = `${minYear}–${maxYear}`;

  // Type breakdown
  const typeCounts = {};
  records.forEach(r => {
    typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
  });
  const typeBreakdown = Object.entries(typeCounts)
    .map(([type, count]) => `${count.toLocaleString()} ${type}`)
    .join(', ');
  document.getElementById('type-breakdown').textContent = typeBreakdown;

  // Mechanism tiles
  const mechanismCounts = {};
  const mechanismDocs = {};
  const mechanismYears = {};
  records.forEach(r => {
    mechanismCounts[r.mechanism] = (mechanismCounts[r.mechanism] || 0) + 1;
    if (!mechanismDocs[r.mechanism]) mechanismDocs[r.mechanism] = new Set();
    mechanismDocs[r.mechanism].add(r.symbol);
    if (!mechanismYears[r.mechanism]) mechanismYears[r.mechanism] = [];
    mechanismYears[r.mechanism].push(r.year);
  });
  const mechanismLatest = {};
  Object.keys(mechanismYears).forEach(m => {
    mechanismLatest[m] = Math.max(...mechanismYears[m]);
  });
  document.getElementById('upr-records').textContent = mechanismCounts['Universal Periodic Review']?.toLocaleString() || '0';
  document.getElementById('upr-documents').textContent = mechanismDocs['Universal Periodic Review']?.size || '0';
  document.getElementById('upr-latest').textContent = mechanismLatest['Universal Periodic Review'] || '–';
  document.getElementById('treaty-records').textContent = mechanismCounts['Treaty bodies']?.toLocaleString() || '0';
  document.getElementById('treaty-documents').textContent = mechanismDocs['Treaty bodies']?.size || '0';
  document.getElementById('treaty-latest').textContent = mechanismLatest['Treaty bodies'] || '–';
  document.getElementById('special-records').textContent = mechanismCounts['Special Procedures']?.toLocaleString() || '0';
  document.getElementById('special-documents').textContent = mechanismDocs['Special Procedures']?.size || '0';
  document.getElementById('special-latest').textContent = mechanismLatest['Special Procedures'] || '–';

  // States in UPR
  const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
  const stateCounts = {};
  const stateRegex = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
  const stateGroupRegex = /\((?:[^()]|\([^()]*\))*\)/g;
  uprRecords.forEach(r => {
    const match = r.text.match(stateRegex);
    if (match) {
      const groups = match[1].match(stateGroupRegex) || [];
      groups.forEach(g => {
        const state = g.slice(1, -1).trim();
        if (state.length <= 60 && !state.includes(',')) {
          stateCounts[state] = (stateCounts[state] || 0) + 1;
        }
      });
    }
  });
  const stateList = Object.entries(stateCounts)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([state, count]) => ({ state, count }));
  const topStates = stateList.slice(0, 10);
  const stateSelect = document.getElementById('state-select');
  stateList.forEach(({ state, count }) => {
    const option = document.createElement('option');
    option.value = state;
    option.textContent = `${state} (${count})`;
    stateSelect.appendChild(option);
  });
  document.getElementById('upr-states-link').hidden = false;
  document.getElementById('show-states').addEventListener('click', e => {
    e.preventDefault();
    const statesDiv = document.createElement('div');
    statesDiv.className = 'states-list';
    statesDiv.innerHTML = '<h4>Ten States that made most recommendations to Kenya</h4>';
    const ul = document.createElement('ul');
    topStates.forEach(({ state, count }) => {
      const li = document.createElement('li');
      li.textContent = `${state}: ${count}`;
      ul.appendChild(li);
    });
    statesDiv.appendChild(ul);
    const tile = document.querySelector('.tile:nth-child(1)');
    tile.appendChild(statesDiv);
    e.target.hidden = true;
  });

  // Filters
  let filteredRecords = records;
  let activeFilters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    state: 'all',
    yearFrom: 'all',
    yearTo: 'all',
    sdg: 'all'
  };

  function updateFilters() {
    filteredRecords = records.filter(r => {
      if (activeFilters.keyword) {
        const words = activeFilters.keyword.toLowerCase().split(/\s+/).filter(w => w);
        if (!words.every(w => r.text.toLowerCase().includes(w) || r.symbol.toLowerCase().includes(w))) {
          return false;
        }
      }
      if (activeFilters.mechanism !== 'all' && r.mechanism !== activeFilters.mechanism) {
        return false;
      }
      if (activeFilters.body !== 'all' && r.body !== activeFilters.body) {
        return false;
      }
      if (activeFilters.type !== 'all' && r.type !== activeFilters.type) {
        return false;
      }
      if (activeFilters.state !== 'all' && r.mechanism === 'Universal Periodic Review') {
        const match = r.text.match(stateRegex);
        if (match) {
          const groups = match[1].match(stateGroupRegex) || [];
          const states = groups.map(g => g.slice(1, -1).trim()).filter(s => s.length <= 60 && !s.includes(','));
          if (!states.includes(activeFilters.state)) {
            return false;
          }
        } else {
          return false;
        }
      }
      if (activeFilters.yearFrom !== 'all' && r.year < parseInt(activeFilters.yearFrom)) {
        return false;
      }
      if (activeFilters.yearTo !== 'all' && r.year > parseInt(activeFilters.yearTo)) {
        return false;
      }
      if (activeFilters.sdg !== 'all' && (!r.sdgs || !r.sdgs.includes(parseInt(activeFilters.sdg)))) {
        return false;
      }
      return true;
    });

    updateMatchingCount();
    updateShareBar();
    updateFilterChips();
    updateTab01();
    updateTab02();
    updateTab03();
    updateTab04();
  }

  function updateMatchingCount() {
    const count = filteredRecords.length;
    document.getElementById('matching-count').textContent = count.toLocaleString();
    document.getElementById('of-total').textContent = `of ${recordCountStr} in the file`;
  }

  function updateShareBar() {
    const share = filteredRecords.length / recordCount;
    document.getElementById('share-bar-fill').style.width = `${share * 100}%`;
  }

  function updateFilterChips() {
    const chipsContainer = document.getElementById('filter-chips');
    chipsContainer.innerHTML = '';
    if (activeFilters.keyword) {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.innerHTML = `Keyword: ${activeFilters.keyword} <button aria-label="Remove keyword filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.keyword = '';
        document.getElementById('keyword-input').value = '';
        document.getElementById('search-input').value = '';
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
    if (activeFilters.mechanism !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.innerHTML = `Mechanism: ${activeFilters.mechanism} <button aria-label="Remove mechanism filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.mechanism = 'all';
        document.querySelector('input[name="mechanism"][value="all"]').checked = true;
        updateBodySelect();
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
    if (activeFilters.body !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.innerHTML = `Body: ${activeFilters.body} <button aria-label="Remove body filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.body = 'all';
        document.getElementById('body-select').value = 'all';
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
    if (activeFilters.type !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.innerHTML = `Type: ${activeFilters.type} <button aria-label="Remove type filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.type = 'all';
        document.getElementById('type-select').value = 'all';
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
    if (activeFilters.state !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.innerHTML = `State: ${activeFilters.state} <button aria-label="Remove state filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.state = 'all';
        document.getElementById('state-select').value = 'all';
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
    if (activeFilters.yearFrom !== 'all' || activeFilters.yearTo !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      const from = activeFilters.yearFrom === 'all' ? minYear : activeFilters.yearFrom;
      const to = activeFilters.yearTo === 'all' ? maxYear : activeFilters.yearTo;
      chip.innerHTML = `Year: ${from}–${to} <button aria-label="Remove year filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.yearFrom = 'all';
        activeFilters.yearTo = 'all';
        document.getElementById('year-from').value = 'all';
        document.getElementById('year-to').value = 'all';
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
    if (activeFilters.sdg !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      const goal = activeFilters.sdg;
      const name = sdgNames[goal] || `SDG ${goal}`;
      chip.innerHTML = `SDG: ${name} <button aria-label="Remove SDG filter">×</button>`;
      chip.querySelector('button').addEventListener('click', () => {
        activeFilters.sdg = 'all';
        document.getElementById('sdg-select').value = 'all';
        updateFilters();
      });
      chipsContainer.appendChild(chip);
    }
  }

  // Keyword filter
  const keywordInput = document.getElementById('keyword-input');
  const searchInput = document.getElementById('search-input');
  let keywordTimeout;
  keywordInput.addEventListener('input', () => {
    clearTimeout(keywordTimeout);
    keywordTimeout = setTimeout(() => {
      activeFilters.keyword = keywordInput.value.trim();
      updateFilters();
    }, 300);
  });
  searchInput.addEventListener('input', () => {
    clearTimeout(keywordTimeout);
    keywordTimeout = setTimeout(() => {
      activeFilters.keyword = searchInput.value.trim();
      keywordInput.value = activeFilters.keyword;
      updateFilters();
    }, 300);
  });

  // Mechanism filter
  document.querySelectorAll('input[name="mechanism"]').forEach(radio => {
    radio.addEventListener('change', () => {
      activeFilters.mechanism = radio.value;
      updateBodySelect();
      updateStateSelect();
      updateFilters();
    });
  });

  function updateBodySelect() {
    const bodySelect = document.getElementById('body-select');
    bodySelect.innerHTML = '<option value="all">All</option>';
    bodySelect.disabled = activeFilters.mechanism === 'all';
    if (activeFilters.mechanism !== 'all') {
      const bodies = new Set();
      records.forEach(r => {
        if (r.mechanism === activeFilters.mechanism) {
          bodies.add(r.body);
        }
      });
      const sortedBodies = Array.from(bodies).sort();
      sortedBodies.forEach(body => {
        const count = records.filter(r => r.mechanism === activeFilters.mechanism && r.body === body).length;
        const option = document.createElement('option');
        option.value = body;
        option.textContent = `${body} (${count})`;
        bodySelect.appendChild(option);
      });
    }
  }

  function updateStateSelect() {
    const stateSelect = document.getElementById('state-select');
    const stateFilterGroup = document.getElementById('state-filter-group');
    stateFilterGroup.hidden = activeFilters.mechanism !== 'Universal Periodic Review';
  }

  // Body filter
  document.getElementById('body-select').addEventListener('change', () => {
    activeFilters.body = document.getElementById('body-select').value;
    updateFilters();
  });

  // Type filter
  const typeSelect = document.getElementById('type-select');
  const types = new Set(records.map(r => r.type));
  Array.from(types).sort().forEach(type => {
    const option = document.createElement('option');
    option.value = type;
    option.textContent = type;
    typeSelect.appendChild(option);
  });
  typeSelect.addEventListener('change', () => {
    activeFilters.type = typeSelect.value;
    updateFilters();
  });

  // State filter
  document.getElementById('state-select').addEventListener('change', () => {
    activeFilters.state = document.getElementById('state-select').value;
    updateFilters();
  });

  // Year filter
  const yearFromSelect = document.getElementById('year-from');
  const yearToSelect = document.getElementById('year-to');
  const distinctYears = Array.from(new Set(records.map(r => r.year))).sort((a, b) => a - b);
  distinctYears.forEach(year => {
    const optionFrom = document.createElement('option');
    optionFrom.value = year;
    optionFrom.textContent = year;
    yearFromSelect.appendChild(optionFrom);
    const optionTo = document.createElement('option');
    optionTo.value = year;
    optionTo.textContent = year;
    yearToSelect.appendChild(optionTo);
  });
  yearFromSelect.addEventListener('change', () => {
    const from = yearFromSelect.value;
    const to = yearToSelect.value;
    if (from !== 'all' && to !== 'all' && parseInt(from) > parseInt(to)) {
      yearToSelect.value = from;
    }
    activeFilters.yearFrom = yearFromSelect.value;
    activeFilters.yearTo = yearToSelect.value;
    updateFilters();
  });
  yearToSelect.addEventListener('change', () => {
    const from = yearFromSelect.value;
    const to = yearToSelect.value;
    if (from !== 'all' && to !== 'all' && parseInt(from) > parseInt(to)) {
      yearFromSelect.value = to;
    }
    activeFilters.yearFrom = yearFromSelect.value;
    activeFilters.yearTo = yearToSelect.value;
    updateFilters();
  });

  // SDG filter
  const sdgSelect = document.getElementById('sdg-select');
  const sdgsPresent = new Set();
  records.forEach(r => {
    if (r.sdgs) {
      r.sdgs.forEach(sdg => sdgsPresent.add(sdg));
    }
  });
  const sortedSdgs = Array.from(sdgsPresent).sort((a, b) => a - b);
  sortedSdgs.forEach(sdg => {
    const option = document.createElement('option');
    option.value = sdg;
    option.textContent = `${sdg}: ${sdgNames[sdg]}`;
    sdgSelect.appendChild(option);
  });
  sdgSelect.addEventListener('change', () => {
    activeFilters.sdg = sdgSelect.value;
    updateFilters();
  });

  // Clear all
  document.getElementById('clear-all').addEventListener('click', () => {
    activeFilters = {
      keyword: '',
      mechanism: 'all',
      body: 'all',
      type: 'all',
      state: 'all',
      yearFrom: 'all',
      yearTo: 'all',
      sdg: 'all'
    };
    document.getElementById('keyword-input').value = '';
    document.getElementById('search-input').value = '';
    document.querySelector('input[name="mechanism"][value="all"]').checked = true;
    document.getElementById('body-select').value = 'all';
    document.getElementById('type-select').value = 'all';
    document.getElementById('state-select').value = 'all';
    document.getElementById('year-from').value = 'all';
    document.getElementById('year-to').value = 'all';
    document.getElementById('sdg-select').value = 'all';
    updateBodySelect();
    updateStateSelect();
    updateFilters();
  });

  // Filter sections
  document.querySelectorAll('.filter-section .filter-heading').forEach(button => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
    });
  });

  // Tab 01: Overview
  function updateTab01() {
    const totalRecords = filteredRecords.length;
    document.getElementById('total-records').textContent = totalRecords.toLocaleString();
    document.getElementById('theme-count').textContent = totalRecords;

    // Mechanism tiles
    const mechanismCounts = {};
    const mechanismDocs = {};
    const mechanismYears = {};
    filteredRecords.forEach(r => {
      mechanismCounts[r.mechanism] = (mechanismCounts[r.mechanism] || 0) + 1;
      if (!mechanismDocs[r.mechanism]) mechanismDocs[r.mechanism] = new Set();
      mechanismDocs[r.mechanism].add(r.symbol);
      if (!mechanismYears[r.mechanism]) mechanismYears[r.mechanism] = [];
      mechanismYears[r.mechanism].push(r.year);
    });
    const mechanismLatest = {};
    Object.keys(mechanismYears).forEach(m => {
      mechanismLatest[m] = Math.max(...mechanismYears[m]);
    });
    document.getElementById('upr-records').textContent = mechanismCounts['Universal Periodic Review']?.toLocaleString() || '0';
    document.getElementById('upr-documents').textContent = mechanismDocs['Universal Periodic Review']?.size || '0';
    document.getElementById('upr-latest').textContent = mechanismLatest['Universal Periodic Review'] || '–';
    document.getElementById('treaty-records').textContent = mechanismCounts['Treaty bodies']?.toLocaleString() || '0';
    document.getElementById('treaty-documents').textContent = mechanismDocs['Treaty bodies']?.size || '0';
    document.getElementById('treaty-latest').textContent = mechanismLatest['Treaty bodies'] || '–';
    document.getElementById('special-records').textContent = mechanismCounts['Special Procedures']?.toLocaleString() || '0';
    document.getElementById('special-documents').textContent = mechanismDocs['Special Procedures']?.size || '0';
    document.getElementById('special-latest').textContent = mechanismLatest['Special Procedures'] || '–';

    // Theme chart
    const themeCounts = {};
    filteredRecords.forEach(r => {
      if (r.themes) {
        r.themes.forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      }
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const themeLabels = sortedThemes.map(([theme]) => theme);
    const themeData = sortedThemes.map(([, count]) => count);
    const themePercent = sortedThemes.map(([, count]) => ((count / totalRecords) * 100).toFixed(1));
    const themeYears = {};
    filteredRecords.forEach(r => {
      if (r.themes) {
        r.themes.forEach(theme => {
          if (!themeYears[theme]) themeYears[theme] = [];
          themeYears[theme].push(r.year);
        });
      }
    });
    const themeYearRanges = {};
    Object.keys(themeYears).forEach(theme => {
      themeYearRanges[theme] = `${Math.min(...themeYears[theme])}–${Math.max(...themeYears[theme])}`;
    });

    const themeChartCtx = document.getElementById('theme-chart').getContext('2d');
    if (window.themeChart) window.themeChart.destroy();
    window.themeChart = new Chart(themeChartCtx, {
      type: 'bar',
      data: {
        labels: themeLabels,
        datasets: [{
          data: themeData,
          backgroundColor: 'rgba(155, 35, 53, 0.8)',
          borderColor: 'rgba(155, 35, 53, 1)',
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
              label: context => {
                const count = context.raw;
                const percent = ((count / totalRecords) * 100).toFixed(1);
                return `${count} (${percent}%)`;
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              callback: value => value.toLocaleString()
            }
          },
          y: {
            ticks: {
              font: {
                family: 'Georgia, serif'
              }
            }
          }
        },
        onClick: (e, elements) => {
          if (elements.length > 0) {
            const theme = themeLabels[elements[0].index];
            activeFilters.keyword = theme;
            keywordInput.value = theme;
            searchInput.value = theme;
            updateFilters();
          }
        }
      }
    });

    // Theme table
    const themeTableBody = document.getElementById('theme-table-body');
    themeTableBody.innerHTML = '';
    sortedThemes.forEach(([theme, count]) => {
      const row = document.createElement('tr');
      const percent = ((count / totalRecords) * 100).toFixed(1);
      row.innerHTML = `
        <td>${theme}</td>
        <td>${count.toLocaleString()}</td>
        <td>${percent}%</td>
        <td>${themeYearRanges[theme]}</td>
      `;
      themeTableBody.appendChild(row);
    });

    // Timeline chart
    const timelineData = {};
    filteredRecords.forEach(r => {
      if (!timelineData[r.year]) timelineData[r.year] = {};
      timelineData[r.year][r.mechanism] = (timelineData[r.year][r.mechanism] || 0) + 1;
    });
    const timelineYears = Array.from({ length: maxYear - minYear + 1 }, (_, i) => minYear + i);
    const uprData = timelineYears.map(year => timelineData[year]?.['Universal Periodic Review'] || 0);
    const treatyData = timelineYears.map(year => timelineData[year]?.['Treaty bodies'] || 0);
    const specialData = timelineYears.map(year => timelineData[year]?.['Special Procedures'] || 0);

    const timelineChartCtx = document.getElementById('timeline-chart').getContext('2d');
    if (window.timelineChart) window.timelineChart.destroy();
    window.timelineChart = new Chart(timelineChartCtx, {
      type: 'bar',
      data: {
        labels: timelineYears.map(y => y.toString()),
        datasets: [
          {
            label: 'Universal Periodic Review',
            data: uprData,
            backgroundColor: 'rgba(194, 65, 12, 0.8)',
            borderColor: 'rgba(194, 65, 12, 1)',
            borderWidth: 1
          },
          {
            label: 'Treaty bodies',
            data: treatyData,
            backgroundColor: 'rgba(15, 118, 110, 0.8)',
            borderColor: 'rgba(15, 118, 110, 1)',
            borderWidth: 1
          },
          {
            label: 'Special Procedures',
            data: specialData,
            backgroundColor: 'rgba(124, 58, 237, 0.8)',
            borderColor: 'rgba(124, 58, 237, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => {
                const label = context.dataset.label;
                const value = context.raw;
                return `${label}: ${value}`;
              }
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            title: {
              display: true,
              text: 'Year'
            }
          },
          y: {
            stacked: true,
            title: {
              display: true,
              text: 'Records'
            },
            ticks: {
              callback: value => value.toLocaleString()
            }
          }
        }
      }
    });
  }

  // Tab 02: Records
  let tableRecords = [];
  let tableOffset = 0;
  const tableLimit = 50;

  function updateTab02() {
    tableRecords = filteredRecords.map(r => {
      const paraMatch = r.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
      const paraNumber = paraMatch ? paraMatch[1] : null;
      let recommendingState = '–';
      if (r.mechanism === 'Universal Periodic Review') {
        const match = r.text.match(stateRegex);
        if (match) {
          const groups = match[1].match(stateGroupRegex) || [];
          const states = groups.map(g => g.slice(1, -1).trim()).filter(s => s.length <= 60 && !s.includes(','));
          if (states.length > 0) {
            recommendingState = states.join(', ');
          } else {
            recommendingState = 'State not found';
          }
        } else {
          recommendingState = 'State not found';
        }
      }
      const firstLine = r.text.length > 120 ? r.text.slice(0, 120).split(' ').slice(0, -1).join(' ') + '…' : r.text;
      return {
        ...r,
        paraNumber,
        recommendingState,
        firstLine
      };
    });

    // Sort by date descending, then body, then paraNumber ascending
    tableRecords.sort((a, b) => {
      if (a.date !== b.date) return b.date.localeCompare(a.date);
      if (a.body !== b.body) return a.body.localeCompare(b.body);
      if (a.paraNumber && b.paraNumber) {
        const aNum = a.paraNumber.includes('.') ? parseFloat(a.paraNumber) : parseInt(a.paraNumber);
        const bNum = b.paraNumber.includes('.') ? parseFloat(b.paraNumber) : parseInt(b.paraNumber);
        return aNum - bNum;
      }
      return 0;
    });

    renderTable();
    updateSearchCount();
  }

  function updateSearchCount() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    if (!searchTerm) {
      document.getElementById('search-count').textContent = filteredRecords.length;
      return;
    }
    const words = searchTerm.split(/\s+/).filter(w => w);
    const count = tableRecords.filter(r => {
      return words.every(w => r.text.toLowerCase().includes(w) || r.symbol.toLowerCase().includes(w));
    }).length;
    document.getElementById('search-count').textContent = count;
  }

  searchInput.addEventListener('input', updateSearchCount);

  function renderTable() {
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';
    const filteredTableRecords = tableRecords.filter(r => {
      const searchTerm = searchInput.value.trim().toLowerCase();
      if (!searchTerm) return true;
      const words = searchTerm.split(/\s+/).filter(w => w);
      return words.every(w => r.text.toLowerCase().includes(w) || r.symbol.toLowerCase().includes(w));
    });
    const paginatedRecords = filteredTableRecords.slice(tableOffset, tableOffset + tableLimit);
    if (paginatedRecords.length === 0) {
      document.getElementById('table-caption').textContent = 'No records match the current filter.';
      document.getElementById('row-count').textContent = '0–0 of 0';
      document.getElementById('show-more').disabled = true;
      return;
    }
    document.getElementById('table-caption').textContent = `Showing ${Math.min(tableOffset + tableLimit, filteredTableRecords.length)} of ${filteredTableRecords.length} records (newest first)`;
    document.getElementById('row-count').textContent = `${tableOffset + 1}–${Math.min(tableOffset + tableLimit, filteredTableRecords.length)} of ${filteredTableRecords.length}`;
    document.getElementById('show-more').disabled = tableOffset + tableLimit >= filteredTableRecords.length;

    paginatedRecords.forEach(r => {
      const row = document.createElement('tr');
      row.setAttribute('tabindex', '0');
      row.innerHTML = `
        <td>${r.date}</td>
        <td>${r.body}</td>
        <td><a href="${r.doc_url}" target="_blank">${r.symbol}</a></td>
        <td>${r.paraNumber || '–'}</td>
        <td>${r.recommendingState}</td>
        <td>${highlightText(r.firstLine, searchInput.value)}</td>
      `;
      row.addEventListener('click', () => {
        const expanded = row.getAttribute('aria-expanded') === 'true';
        row.setAttribute('aria-expanded', !expanded);
      });
      row.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          const expanded = row.getAttribute('aria-expanded') === 'true';
          row.setAttribute('aria-expanded', !expanded);
        }
      });
      const expandedRow = document.createElement('tr');
      expandedRow.setAttribute('aria-expanded', 'false');
      expandedRow.innerHTML = `
        <td colspan="6">
          <button class="expand-row">Expand</button>
          <div class="expanded-content">
            <div class="para-num">${r.paraNumber ? `para. ${r.paraNumber}` : 'No paragraph number'}</div>
            <div class="full-text">${r.text}</div>
            <div class="labels">
              ${r.themes && r.themes.length > 0 ? `
              <div class="label-group">
                <h4>Themes</h4>
                ${r.themes.map(theme => `<span class="label-chip">${theme}</span>`).join('')}
              </div>
              ` : ''}
              ${r.sdgs && r.sdgs.length > 0 ? `
              <div class="label-group">
                <h4>SDGs</h4>
                ${r.sdgs.map(sdg => `<span class="label-chip">${sdg}: ${sdgNames[sdg]}</span>`).join('')}
              </div>
              ` : ''}
              ${r.sdg_targets && r.sdg_targets.length > 0 ? `
              <div class="label-group">
                <h4>SDG targets</h4>
                ${r.sdg_targets.map(target => `<span class="label-chip">${target}</span>`).join('')}
              </div>
              ` : ''}
              ${r.affected_persons && r.affected_persons.length > 0 ? `
              <div class="label-group">
                <h4>Affected persons</h4>
                ${r.affected_persons.map(person => `<span class="label-chip">${person}</span>`).join('')}
              </div>
              ` : ''}
              ${r.section ? `
              <div class="label-group">
                <h4>Section</h4>
                <span class="label-chip">${r.section}</span>
              </div>
              ` : ''}
            </div>
            <div class="actions">
              <button class="copy-btn">Copy citation${r.paraNumber ? '' : ' (no paragraph number in this extract)'}</button>
              <span class="copy-confirm">Copied</span>
              <a href="${r.doc_url}" target="_blank" class="open-doc">Open the UN document</a>
            </div>
          </div>
        </td>
      `;
      expandedRow.querySelector('.expand-row').addEventListener('click', () => {
        const expanded = expandedRow.getAttribute('aria-expanded') === 'true';
        expandedRow.setAttribute('aria-expanded', !expanded);
      });
      expandedRow.querySelector('.copy-btn').addEventListener('click', () => {
        const citation = r.paraNumber ? `${r.symbol}, para. ${r.paraNumber}` : r.symbol;
        navigator.clipboard.writeText(citation).then(() => {
          const confirm = expandedRow.querySelector('.copy-confirm');
          confirm.classList.add('visible');
          setTimeout(() => confirm.classList.remove('visible'), 2000);
        });
      });
      tableBody.appendChild(row);
      tableBody.appendChild(expandedRow);
    });
  }

  function highlightText(text, searchTerm) {
    if (!searchTerm) return text;
    const words = searchTerm.toLowerCase().split(/\s+/).filter(w => w);
    let highlighted = text;
    words.forEach(word => {
      const regex = new RegExp(word, 'gi');
      highlighted = highlighted.replace(regex, match => `<mark>${match}</mark>`);
    });
    return highlighted;
  }

  document.getElementById('show-more').addEventListener('click', () => {
    tableOffset += tableLimit;
    renderTable();
  });

  document.getElementById('sort-date').addEventListener('click', () => {
    const icon = document.getElementById('sort-icon');
    const isDescending = icon.textContent === '↓';
    icon.textContent = isDescending ? '↑' : '↓';
    tableRecords.sort((a, b) => {
      if (a.date !== b.date) return isDescending ? a.date.localeCompare(b.date) : b.date.localeCompare(a.date);
      if (a.body !== b.body) return a.body.localeCompare(b.body);
      if (a.paraNumber && b.paraNumber) {
        const aNum = a.paraNumber.includes('.') ? parseFloat(a.paraNumber) : parseInt(a.paraNumber);
        const bNum = b.paraNumber.includes('.') ? parseFloat(b.paraNumber) : parseInt(b.paraNumber);
        return aNum - bNum;
      }
      return 0;
    });
    tableOffset = 0;
    renderTable();
  });

  // Tab 03: Check
  function updateTab03() {
    const checkResults = document.getElementById('check-results');
    checkResults.innerHTML = '';

    // Record count
    const recordCountCheck = document.createElement('div');
    recordCountCheck.className = 'check-line';
    const expectedCount = Number(data.count);
    const recordCountPass = recordCount === expectedCount;
    recordCountCheck.innerHTML = `
      <span>Record count</span>
      <span>${recordCount.toLocaleString()} (file) vs ${expectedCount.toLocaleString()} (header) <span class="${recordCountPass ? 'check-pass' : 'check-fail'}">${recordCountPass ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(recordCountCheck);

    // Partitions
    const mechanismPartition = Object.values(mechanismCounts).reduce((a, b) => a + b, 0) === recordCount;
    const mechanismPartitionLine = document.createElement('div');
    mechanismPartitionLine.className = 'check-line';
    mechanismPartitionLine.innerHTML = `
      <span>Mechanism partition</span>
      <span>sums to ${recordCount.toLocaleString()} <span class="${mechanismPartition ? 'check-pass' : 'check-fail'}">${mechanismPartition ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(mechanismPartitionLine);

    const bodyPartition = records.reduce((sum, r) => {
      const bodies = new Set(records.map(r => r.body));
      return sum + (bodies.has(r.body) ? 1 : 0);
    }, 0) === recordCount;
    const bodyPartitionLine = document.createElement('div');
    bodyPartitionLine.className = 'check-line';
    bodyPartitionLine.innerHTML = `
      <span>Body partition</span>
      <span>sums to ${recordCount.toLocaleString()} <span class="${bodyPartition ? 'check-pass' : 'check-fail'}">${bodyPartition ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(bodyPartitionLine);

    const yearPartition = years.reduce((sum, y) => sum + records.filter(r => r.year === y).length, 0) === recordCount;
    const yearPartitionLine = document.createElement('div');
    yearPartitionLine.className = 'check-line';
    yearPartitionLine.innerHTML = `
      <span>Year partition</span>
      <span>sums to ${recordCount.toLocaleString()} <span class="${yearPartition ? 'check-pass' : 'check-fail'}">${yearPartition ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(yearPartitionLine);

    // Type partition
    const typePartition = Object.values(typeCounts).reduce((a, b) => a + b, 0) === recordCount;
    const typePartitionLine = document.createElement('div');
    typePartitionLine.className = 'check-line';
    typePartitionLine.innerHTML = `
      <span>Type partition</span>
      <span>sums to ${recordCount.toLocaleString()} <span class="${typePartition ? 'check-pass' : 'check-fail'}">${typePartition ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(typePartitionLine);

    // Chart against table
    const themeCounts = {};
    filteredRecords.forEach(r => {
      if (r.themes) {
        r.themes.forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      }
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const chartValues = sortedThemes.map(([, count]) => count);
    const tableValues = sortedThemes.map(([theme]) => {
      return filteredRecords.filter(r => r.themes && r.themes.includes(theme)).length;
    });
    const chartTableMatch = chartValues.every((v, i) => v === tableValues[i]);
    const chartTableLine = document.createElement('div');
    chartTableLine.className = 'check-line';
    chartTableLine.innerHTML = `
      <span>Chart against table</span>
      <span>values match <span class="${chartTableMatch ? 'check-pass' : 'check-fail'}">${chartTableMatch ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(chartTableLine);

    // Links
    const linkErrors = [];
    records.forEach(r => {
      const url = new URL(r.doc_url);
      if (url.protocol !== 'https:' || url.hostname !== 'docs.un.org' || !url.pathname.endsWith(r.symbol)) {
        linkErrors.push(r.symbol);
      }
    });
    const linkLine = document.createElement('div');
    linkLine.className = 'check-line';
    if (linkErrors.length === 0) {
      linkLine.innerHTML = `
        <span>Links</span>
        <span>all start with https://docs.un.org/ and end with symbol <span class="check-pass">✓</span></span>
      `;
    } else {
      linkLine.innerHTML = `
        <span>Links</span>
        <span>${linkErrors.length} records fail: ${linkErrors.slice(0, 5).join(', ')}${linkErrors.length > 5 ? '…' : ''} <span class="check-fail">✗ check failed</span></span>
      `;
    }
    checkResults.appendChild(linkLine);

    // Paragraph numbers
    const paraStats = {};
    ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'].forEach(m => {
      const records = filteredRecords.filter(r => r.mechanism === m);
      const withPara = records.filter(r => r.text.match(/^\d{1,3}(?:\.\d{1,3})?\.?\s/)).length;
      paraStats[m] = { withPara, total: records.length };
    });
    const paraLine = document.createElement('div');
    paraLine.className = 'check-line';
    paraLine.innerHTML = `
      <span>Paragraph numbers</span>
      <span>
        UPR: ${paraStats['Universal Periodic Review'].withPara}/${paraStats['Universal Periodic Review'].total} (${Math.round((paraStats['Universal Periodic Review'].withPara / paraStats['Universal Periodic Review'].total) * 100)}%),
        Treaty: ${paraStats['Treaty bodies'].withPara}/${paraStats['Treaty bodies'].total} (${Math.round((paraStats['Treaty bodies'].withPara / paraStats['Treaty bodies'].total) * 100)}%),
        Special: ${paraStats['Special Procedures'].withPara}/${paraStats['Special Procedures'].total} (${Math.round((paraStats['Special Procedures'].withPara / paraStats['Special Procedures'].total) * 100)}%)
      </span>
    `;
    checkResults.appendChild(paraLine);

    // States found
    const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
    const uprWithState = uprRecords.filter(r => {
      const match = r.text.match(stateRegex);
      if (match) {
        const groups = match[1].match(stateGroupRegex) || [];
        const states = groups.map(g => g.slice(1, -1).trim()).filter(s => s.length <= 60 && !s.includes(','));
        return states.length > 0;
      }
      return false;
    }).length;
    const stateErrors = uprRecords.filter(r => {
      const match = r.text.match(stateRegex);
      if (match) {
        const groups = match[1].match(stateGroupRegex) || [];
        const states = groups.map(g => g.slice(1, -1).trim()).filter(s => s.length <= 60 && !s.includes(','));
        return states.length === 0;
      }
      return true;
    }).map(r => r.symbol);
    const stateLine = document.createElement('div');
    stateLine.className = 'check-line';
    if (stateErrors.length === 0) {
      stateLine.innerHTML = `
        <span>States found</span>
        <span>all UPR records have at least one State <span class="check-pass">✓</span></span>
      `;
    } else {
      stateLine.innerHTML = `
        <span>States found</span>
        <span>${uprRecords.length - uprWithState} records without a State: ${stateErrors.slice(0, 5).join(', ')}${stateErrors.length > 5 ? '…' : ''} <span class="check-fail">✗ check failed</span></span>
      `;
    }
    checkResults.appendChild(stateLine);

    // Duplicates and gaps
    const distinctIds = new Set(records.map(r => r.id)).size;
    const idLine = document.createElement('div');
    idLine.className = 'check-line';
    idLine.innerHTML = `
      <span>Distinct IDs</span>
      <span>${distinctIds} of ${recordCount} <span class="${distinctIds === recordCount ? 'check-pass' : 'check-fail'}">${distinctIds === recordCount ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(idLine);

    const duplicateTexts = records.reduce((acc, r) => {
      acc[r.text] = (acc[r.text] || 0) + 1;
      return acc;
    }, {});
    const duplicateCount = Object.values(duplicateTexts).filter(v => v > 1).reduce((a, b) => a + b, 0) - Object.values(duplicateTexts).filter(v => v > 1).length;
    const duplicateLine = document.createElement('div');
    duplicateLine.className = 'check-line';
    duplicateLine.innerHTML = `
      <span>Duplicate texts</span>
      <span>${duplicateCount} records <span class="${duplicateCount === 0 ? 'check-pass' : 'check-fail'}">${duplicateCount === 0 ? '✓' : '✗ check failed'}</span></span>
    `;
    checkResults.appendChild(duplicateLine);

    const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
    const noThemesLine = document.createElement('div');
    noThemesLine.className = 'check-line';
    noThemesLine.innerHTML = `
      <span>Records without themes</span>
      <span>${noThemes} not labelled</span>
    `;
    checkResults.appendChild(noThemesLine);

    const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    const noSdgsLine = document.createElement('div');
    noSdgsLine.className = 'check-line';
    noSdgsLine.innerHTML = `
      <span>Records without SDGs</span>
      <span>${noSdgs} not labelled</span>
    `;
    checkResults.appendChild(noSdgsLine);

    const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
    const noAffectedLine = document.createElement('div');
    noAffectedLine.className = 'check-line';
    noAffectedLine.innerHTML = `
      <span>Records without affected persons</span>
      <span>${noAffected} not labelled</span>
    `;
    checkResults.appendChild(noAffectedLine);

    // Sample check
    let sampleSeed = 1;
    let sampleRecords = [];
    let sampleJudgements = Array(10).fill(null);

    function drawSample() {
      sampleSeed = parseInt(document.getElementById('sample-seed').value) || 1;
      const rng = mulberry32(sampleSeed);
      sampleRecords = [];
      const shuffled = [...filteredRecords].sort(() => rng() - 0.5);
      for (let i = 0; i < 10 && i < shuffled.length; i++) {
        sampleRecords.push(shuffled[i]);
      }
      renderSample();
      updateSampleTally();
    }

    document.getElementById('draw-sample').addEventListener('click', drawSample);
    document.getElementById('sample-seed').addEventListener('change', drawSample);

    function renderSample() {
      const sampleCards = document.getElementById('sample-cards');
      sampleCards.innerHTML = '';
      sampleRecords.forEach((r, i) => {
        const card = document.createElement('div');
        card.className = 'sample-card';
        card.setAttribute('aria-expanded', 'false');
        card.innerHTML = `
          <div class="sample-card-header">
            <span><a href="${r.doc_url}" target="_blank">${r.symbol}</a>, para. ${r.paraNumber || '–'}</span>
            <button aria-label="Expand card">▼</button>
          </div>
          <div class="sample-card-content">
            <div class="para-num">${r.paraNumber ? `para. ${r.paraNumber}` : 'No paragraph number'}</div>
            <div class="full-text">${r.text}</div>
            <div class="theme-chips">
              ${r.themes && r.themes.length > 0 ? r.themes.map(theme => `<span class="label-chip">${theme}</span>`).join('') : 'No themes'}
            </div>
            <div class="verdict-buttons">
              <button data-index="${i}" data-verdict="fit">Fits</button>
              <button data-index="${i}" data-verdict="dont">Doesn't fit</button>
              <button data-index="${i}" data-verdict="unsure">Unsure</button>
            </div>
          </div>
        `;
        card.querySelector('.sample-card-header button').addEventListener('click', () => {
          const expanded = card.getAttribute('aria-expanded') === 'true';
          card.setAttribute('aria-expanded', !expanded);
        });
        card.querySelectorAll('.verdict-buttons button').forEach(button => {
          button.addEventListener('click', () => {
            const index = parseInt(button.getAttribute('data-index'));
            const verdict = button.getAttribute('data-verdict');
            sampleJudgements[index] = verdict;
            updateSampleButtons(index);
            updateSampleTally();
          });
        });
        sampleCards.appendChild(card);
      });
    }

    function updateSampleButtons(index) {
      const card = document.querySelector(`.sample-card:nth-child(${index + 1})`);
      card.querySelectorAll('.verdict-buttons button').forEach(button => {
        button.classList.remove('selected');
      });
      const verdict = sampleJudgements[index];
      if (verdict) {
        card.querySelector(`.verdict-buttons button[data-verdict="${verdict}"]`).classList.add('selected');
      }
    }

    function updateSampleTally() {
      const fit = sampleJudgements.filter(v => v === 'fit').length;
      const dont = sampleJudgements.filter(v => v === 'dont').length;
      const unsure = sampleJudgements.filter(v => v === 'unsure').length;
      document.getElementById('sample-tally').textContent = `Themes: ${fit} fit, ${dont} don't, ${unsure} unsure of ${sampleJudgements.length} judged (seed ${sampleSeed})`;
    }

    drawSample();
  }

  // Tab 04: Method & export
  function updateTab04() {
    // Download CSV
    document.getElementById('download-csv').addEventListener('click', () => {
      const headers = [
        'Date', 'Body', 'Symbol', 'Paragraph', 'Recommending State', 'First line',
        'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Full text'
      ];
      const rows = filteredRecords.map(r => {
        const paraMatch = r.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
        const paraNumber = paraMatch ? paraMatch[1] : '';
        let recommendingState = '';
        if (r.mechanism === 'Universal Periodic Review') {
          const match = r.text.match(stateRegex);
          if (match) {
            const groups = match[1].match(stateGroupRegex) || [];
            const states = groups.map(g => g.slice(1, -1).trim()).filter(s => s.length <= 60 && !s.includes(','));
            recommendingState = states.join(', ');
          }
        }
        const firstLine = r.text.length > 120 ? r.text.slice(0, 120).split(' ').slice(0, -1).join(' ') + '…' : r.text;
        return [
          r.date,
          r.body,
          r.symbol,
          paraNumber,
          recommendingState,
          firstLine,
          r.themes ? r.themes.join('; ') : '',
          r.sdgs ? r.sdgs.map(sdg => `${sdg}: ${sdgNames[sdg]}`).join('; ') : '',
          r.sdg_targets ? r.sdg_targets.join('; ') : '',
          r.affected_persons ? r.affected_persons.join('; ') : '',
          r.section || '',
          r.text
        ];
      });
      const csvContent = [
        `# UN human rights recommendations and observations: ${country}`,
        `# Source: ${source}`,
        `# Built: ${built}`,
        `# Filters: ${JSON.stringify(activeFilters)}`,
        `# Records: ${filteredRecords.length}`,
        headers.join(','),
        ...rows.map(row => row.map(field => `"${String(field).replace(/"/g, '""')}"`).join(','))
      ].join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `uhri-kenya-${new Date().toISOString().slice(0, 10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });

    // Copy summary
    document.getElementById('copy-summary').addEventListener('click', () => {
      const totalRecords = filteredRecords.length;
      const typeCounts = {};
      filteredRecords.forEach(r => {
        typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
      });
      const typeBreakdown = Object.entries(typeCounts)
        .map(([type, count]) => `${count} ${type}`)
        .join(', ');
      const mechanismCounts = {};
      filteredRecords.forEach(r => {
        mechanismCounts[r.mechanism] = (mechanismCounts[r.mechanism] || 0) + 1;
      });
      const themeCounts = {};
      filteredRecords.forEach(r => {
        if (r.themes) {
          r.themes.forEach(theme => {
            themeCounts[theme] = (themeCounts[theme] || 0) + 1;
          });
        }
      });
      const sortedThemes = Object.entries(themeCounts)
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 10)
        .map(([theme, count]) => `${theme} (${count})`)
        .join(', ');
      const summary = `UN human rights recommendations and observations: ${country}
Source: ${source}
Records: ${totalRecords.toLocaleString()} (${typeBreakdown})
Mechanisms: UPR ${mechanismCounts['Universal Periodic Review'] || 0}, Treaty bodies ${mechanismCounts['Treaty bodies'] || 0}, Special Procedures ${mechanismCounts['Special Procedures'] || 0}
Top themes: ${sortedThemes}`;
      navigator.clipboard.writeText(summary).then(() => {
        const button = document.getElementById('copy-summary');
        const originalText = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => button.textContent = originalText, 2000);
      });
    });
  }

  // Tabs
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => {
        t.setAttribute('aria-selected', 'false');
      });
      tab.setAttribute('aria-selected', 'true');
      document.querySelectorAll('.tab-content').forEach(panel => {
        panel.setAttribute('aria-hidden', 'true');
      });
      const panelId = tab.getAttribute('aria-controls');
      document.getElementById(panelId).setAttribute('aria-hidden', 'false');
    });
  });
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        const tabs = Array.from(document.querySelectorAll('.tab'));
        const currentIndex = tabs.indexOf(document.activeElement);
        let nextIndex;
        if (e.key === 'ArrowRight') {
          nextIndex = (currentIndex + 1) % tabs.length;
        } else {
          nextIndex = (currentIndex - 1 + tabs.length) % tabs.length;
        }
        tabs[nextIndex].focus();
      }
    });
  });

  // Initial render
  updateFilters();
});

// Seeded random number generator (mulberry32)
function mulberry32(a) {
  return function() {
    var t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
}
</script>
</body>
</html>
```