I built a dashboard for Kenya's UN recommendations and observations, answering four questions in four tabs: what the UN has said, the records themselves, a check of the app's own work, and method and export. The left rail filters the set for every tab; the header and footer stay in view.

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
  --accent: #9b2335;
  --mono: ui-monospace, Menlo, Consolas, monospace;
  --sans: system-ui, -apple-system, sans-serif;
  --serif: Georgia, "Times New Roman", serif;
}
body {
  margin: 0;
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  accent-color: var(--accent);
}
[hidden] { display: none !important; }
a { color: var(--accent); text-decoration: none; }
a:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
button, input, select, textarea {
  font: inherit;
  color: inherit;
  background: transparent;
  border: 1px solid var(--rule);
  padding: 0.5em 0.75em;
  border-radius: 3px;
}
button:focus, input:focus, select:focus, textarea:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
button { cursor: pointer; }
button:disabled { opacity: 0.5; cursor: not-allowed; }
button[aria-expanded="true"] { border-bottom-left-radius: 0; border-bottom-right-radius: 0; }
button[aria-expanded="false"] + div { display: none; }

/* Header */
.header {
  padding: 1em 1.5em;
  border-bottom: 1px solid var(--rule);
  display: flex;
  flex-wrap: wrap;
  gap: 1em;
  align-items: baseline;
}
.header-label {
  font-family: var(--mono);
  font-size: 0.875em;
  color: #666;
}
.header-title {
  font-family: var(--serif);
  font-size: 2em;
  margin: 0;
  flex-grow: 1;
}
.header-meta {
  font-size: 0.875em;
  color: #666;
  flex-basis: 100%;
}
.header-meta a { color: #666; }

/* Tabs */
.tablist {
  display: flex;
  border-bottom: 1px solid var(--rule);
  padding: 0 1.5em;
  gap: 0.5em;
  list-style: none;
  margin: 0;
  flex-wrap: wrap;
}
.tablist [role="tab"] {
  padding: 0.75em 1em;
  border: 1px solid transparent;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  background: none;
  cursor: pointer;
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.tablist [role="tab"][aria-selected="true"] {
  background: var(--paper);
  border-color: var(--rule);
  color: var(--accent);
  border-bottom-color: var(--paper);
}
.tablist [role="tab"]:focus { outline: 2px solid var(--accent); outline-offset: -2px; }

/* Main layout */
.main {
  display: flex;
  min-height: calc(100vh - 120px);
}
.rail {
  width: 280px;
  padding: 1.5em;
  border-right: 1px solid var(--rule);
  background: #f9f7f4;
  flex-shrink: 0;
}
.rail h2 {
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 1em 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rail-filter-heading {
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 1.5em 0 0.5em 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rail-filter-heading button {
  font-family: var(--mono);
  font-size: 0.875em;
  padding: 0.25em 0.5em;
  border: 1px solid var(--rule);
  border-radius: 3px;
}
.rail-filter-heading button[aria-expanded="true"]::after { content: "−"; }
.rail-filter-heading button[aria-expanded="false"]::after { content: "+"; }
.rail-filter-count {
  font-family: var(--serif);
  font-size: 2.5em;
  margin: 0 0 0.5em 0;
  line-height: 1;
}
.rail-filter-bar {
  height: 8px;
  background: var(--rule);
  margin-bottom: 1em;
  position: relative;
}
.rail-filter-bar-fill {
  height: 100%;
  background: var(--accent);
  width: 0%;
}
.rail-filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
  margin-bottom: 1em;
}
.rail-filter-chip {
  background: var(--accent);
  color: white;
  padding: 0.25em 0.5em;
  border-radius: 1em;
  font-size: 0.875em;
  display: flex;
  align-items: center;
  gap: 0.25em;
}
.rail-filter-chip button {
  background: rgba(255,255,255,0.2);
  border: none;
  border-radius: 50%;
  width: 1.2em;
  height: 1.2em;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  font-size: 0.75em;
}
.rail-filter-chip button::after { content: "×"; }

.rail-filter-section { margin-bottom: 1.5em; }
.rail-filter-section label {
  display: block;
  margin-bottom: 0.5em;
  font-size: 0.875em;
}
.rail-filter-section input[type="text"] {
  width: 100%;
  box-sizing: border-box;
}
.rail-filter-section select {
  width: 100%;
  box-sizing: border-box;
}
.rail-filter-section .radio-group {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}
.rail-filter-section .radio-option {
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.rail-filter-section .radio-option input { margin: 0; }

.content {
  flex-grow: 1;
  padding: 1.5em;
  max-width: calc(100vw - 280px);
}
.content h2 {
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 1em 0;
  color: #666;
}
.content h3 {
  font-family: var(--serif);
  font-size: 1.5em;
  margin: 1.5em 0 0.5em 0;
}
.content-fig {
  margin-bottom: 2em;
}
.content-fig-title {
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5em 0;
  color: #666;
}
.content-fig-note {
  font-size: 0.875em;
  color: #666;
  margin: 0.5em 0;
}
.content-fig-source {
  font-size: 0.875em;
  color: #666;
  margin: 0.5em 0 0 0;
}

/* Tiles */
.tiles {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5em;
  margin-bottom: 2em;
}
.tile {
  flex: 1;
  min-width: 200px;
  border: 1px solid var(--rule);
  padding: 1em;
  border-radius: 4px;
}
.tile-title {
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5em 0;
  color: #666;
}
.tile-number {
  font-family: var(--serif);
  font-size: 3em;
  margin: 0 0 0.25em 0;
  line-height: 1;
}
.tile-breakdown {
  font-size: 0.875em;
  color: #666;
  margin: 0.5em 0;
}
.tile-note {
  font-size: 0.875em;
  color: #666;
  margin: 0.5em 0 0 0;
}
.tile-dot {
  display: inline-block;
  width: 1em;
  height: 1em;
  border-radius: 50%;
  margin-right: 0.5em;
}
.tile-dot.upr { background: #c2410c; }
.tile-dot.tb { background: #0f766e; }
.tile-dot.sp { background: #7c3aed; }

/* Chart */
.chart-container {
  position: relative;
  height: 400px;
  margin-bottom: 1em;
}
.chart-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1em;
}
.chart-table th, .chart-table td {
  padding: 0.5em;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
.chart-table th { font-weight: bold; }
.chart-table td { font-family: var(--mono); }
.chart-table td:last-child { text-align: right; }

/* Table */
.table-container {
  overflow-x: auto;
}
.table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}
.table caption {
  font-family: var(--mono);
  font-size: 0.875em;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-align: left;
  margin-bottom: 0.5em;
  color: #666;
}
.table th, .table td {
  padding: 0.75em;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
.table th {
  font-weight: bold;
  background: #f9f7f4;
  position: sticky;
  top: 0;
}
.table th[scope="col"]:nth-child(4) { text-align: right; }
.table th[scope="col"]:nth-child(5) { text-align: right; }
.table tr:focus-within {
  background: #f0ebe5;
}
.table tr[aria-expanded="true"] { background: #f0ebe5; }
.table tr[aria-expanded="true"] td { border-bottom: none; }
.table-row-details {
  padding: 1em;
  border-bottom: 1px solid var(--rule);
}
.table-row-details h4 {
  margin: 0 0 0.5em 0;
  font-family: var(--serif);
  font-size: 1.5em;
  color: var(--accent);
}
.table-row-details p {
  margin: 0 0 1em 0;
  white-space: pre-wrap;
}
.table-row-details-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
  margin-bottom: 1em;
}
.table-row-details-label {
  background: #f0ebe5;
  padding: 0.25em 0.5em;
  border-radius: 3px;
  font-size: 0.875em;
}
.table-row-details-actions {
  display: flex;
  gap: 1em;
  margin-top: 1em;
}
.table-row-details-actions button {
  background: var(--accent);
  color: white;
  border: none;
  padding: 0.5em 1em;
  border-radius: 3px;
}
.table-row-details-actions button:disabled { background: #ccc; }
.table-row-details-actions .copied {
  background: #28a745;
  padding: 0.5em 1em;
  border-radius: 3px;
  animation: fadeOut 2s forwards;
}
@keyframes fadeOut {
  0% { opacity: 1; }
  100% { opacity: 0; }
}
.table-row-details-source {
  font-size: 0.875em;
  color: #666;
  margin-top: 1em;
}
.table-row-highlight mark {
  background: #ffeb3b;
  padding: 0;
}
.table-more {
  text-align: center;
  margin-top: 1em;
}
.table-more button {
  background: var(--accent);
  color: white;
  border: none;
  padding: 0.5em 1em;
  border-radius: 3px;
}

/* Check tab */
.check-panel {
  border: 1px solid var(--rule);
  padding: 1em;
  border-radius: 4px;
  margin-bottom: 2em;
}
.check-panel h3 {
  margin: 0 0 1em 0;
  font-family: var(--serif);
  font-size: 1.5em;
}
.check-panel-item {
  margin-bottom: 0.5em;
  padding-bottom: 0.5em;
  border-bottom: 1px solid var(--rule);
}
.check-panel-item:last-child { border-bottom: none; margin-bottom: 0; }
.check-panel-item.pass::before {
  content: "✓";
  color: #28a745;
  margin-right: 0.5em;
}
.check-panel-item.fail::before {
  content: "✗";
  color: var(--accent);
  margin-right: 0.5em;
}
.check-panel-item.warn::before {
  content: "!";
  color: #ffc107;
  margin-right: 0.5em;
}
.check-sample {
  margin-top: 2em;
}
.check-sample-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
}
.check-sample-header button {
  background: var(--accent);
  color: white;
  border: none;
  padding: 0.5em 1em;
  border-radius: 3px;
}
.check-sample-cards {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
.check-sample-card {
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1em;
}
.check-sample-card[aria-expanded="false"] .check-sample-card-details { display: none; }
.check-sample-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
.check-sample-card-header button {
  background: none;
  border: none;
  font-size: 1em;
  padding: 0;
}
.check-sample-card-header button[aria-expanded="true"]::after { content: "−"; }
.check-sample-card-header button[aria-expanded="false"]::after { content: "+"; }
.check-sample-card-title {
  font-weight: bold;
  margin: 0;
}
.check-sample-card-details {
  margin-top: 1em;
}
.check-sample-card-details p {
  margin: 0 0 1em 0;
  white-space: pre-wrap;
}
.check-sample-card-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
  margin: 1em 0;
}
.check-sample-card-label {
  background: #f0ebe5;
  padding: 0.25em 0.5em;
  border-radius: 3px;
  font-size: 0.875em;
}
.check-sample-card-actions {
  display: flex;
  gap: 1em;
  margin-top: 1em;
}
.check-sample-card-actions button {
  padding: 0.5em 1em;
  border-radius: 3px;
  border: 1px solid var(--rule);
}
.check-sample-card-actions button.fit { background: #28a745; color: white; }
.check-sample-card-actions button.dont { background: var(--accent); color: white; }
.check-sample-card-actions button.unsure { background: #ffc107; color: var(--ink); }
.check-sample-tally {
  margin-top: 1em;
  font-size: 0.875em;
  color: #666;
}

/* Method & export tab */
.method-section {
  margin-bottom: 2em;
}
.method-section h3 {
  font-family: var(--serif);
  font-size: 1.5em;
  margin: 0 0 0.5em 0;
}
.method-section p {
  margin: 0 0 1em 0;
  line-height: 1.6;
}
.export-actions {
  display: flex;
  gap: 1em;
  margin-bottom: 2em;
}
.export-actions button {
  background: var(--accent);
  color: white;
  border: none;
  padding: 0.75em 1.5em;
  border-radius: 3px;
  font-size: 1em;
}
.export-actions .copied {
  background: #28a745;
  padding: 0.75em 1.5em;
  border-radius: 3px;
  animation: fadeOut 2s forwards;
}

/* Footer */
.footer {
  padding: 1em 1.5em;
  border-top: 1px solid var(--rule);
  font-family: var(--mono);
  font-size: 0.875em;
  color: #666;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1em;
}
.footer a { color: #666; }

/* Mechanism colors for timeline */
.upr-bar { background-color: #c2410c; }
.tb-bar { background-color: #0f766e; }
.sp-bar { background-color: #7c3aed; }
</style>
</head>
<body>

<div class="header">
  <div class="header-label">UHRI · <span id="country-name"></span></div>
  <h1 class="header-title">UN human rights recommendations and observations: <span id="country-name-title"></span></h1>
  <div class="header-meta">
    Source: <a id="source-url" href="#" target="_blank">UHRI</a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · built <span id="built-date"></span> · dated by document
  </div>
</div>

<ul class="tablist" role="tablist" aria-label="Tabs">
  <li role="presentation"><button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 OVERVIEW</button></li>
  <li role="presentation"><button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 RECORDS</button></li>
  <li role="presentation"><button id="tab-03" role="tab" aria-selected="false" aria-controls="panel-03">03 CHECK</button></li>
  <li role="presentation"><button id="tab-04" role="tab" aria-selected="false" aria-controls="panel-04">04 METHOD & EXPORT</button></li>
</ul>

<div class="main">
  <div class="rail">
    <h2>FILTERS <button id="clear-filters">Clear all</button></h2>
    <div class="rail-filter-count" id="filtered-count" aria-live="polite">0</div>
    <div class="rail-filter-bar"><div class="rail-filter-bar-fill" id="filtered-bar"></div></div>
    <div class="rail-filter-chips" id="active-filters"></div>

    <div class="rail-filter-section">
      <div class="rail-filter-heading">
        <button id="filter-heading-01" aria-expanded="true">01 KEYWORD</button>
      </div>
      <div>
        <label for="keyword">Search records</label>
        <input type="text" id="keyword" placeholder="e.g. torture" aria-describedby="keyword-hint">
        <div id="keyword-hint" class="content-fig-note">literal match, not synonyms</div>
      </div>
    </div>

    <div class="rail-filter-section">
      <div class="rail-filter-heading">
        <button id="filter-heading-02" aria-expanded="false">02 MECHANISM, BODY, TYPE</button>
      </div>
      <div>
        <label for="mechanism">Mechanism</label>
        <select id="mechanism">
          <option value="">All mechanisms</option>
        </select>

        <div id="body-filter-group">
          <label>Body or mandate</label>
          <div class="radio-group" id="body-options"></div>
        </div>

        <div id="type-filter-group">
          <label>Type</label>
          <div class="radio-group" id="type-options"></div>
        </div>

        <div id="state-filter-group" hidden>
          <label for="state">Recommending State</label>
          <select id="state">
            <option value="">All States</option>
          </select>
        </div>
      </div>
    </div>

    <div class="rail-filter-section">
      <div class="rail-filter-heading">
        <button id="filter-heading-03" aria-expanded="false">03 YEARS AND SDG</button>
      </div>
      <div>
        <label for="year-from">Year from</label>
        <select id="year-from">
          <option value="">Earliest</option>
        </select>

        <label for="year-to">to</label>
        <select id="year-to">
          <option value="">Latest</option>
        </select>

        <label for="sdg">SDG</label>
        <select id="sdg">
          <option value="">All SDGs</option>
        </select>
      </div>
    </div>
  </div>

  <div class="content">
    <div id="panel-01" role="tabpanel" aria-labelledby="tab-01">
      <div class="tiles">
        <div class="tile">
          <div class="tile-title">All records</div>
          <div class="tile-number" id="tile-total">0</div>
          <div class="tile-breakdown" id="tile-breakdown"></div>
          <div class="tile-note">How this is computed: count of records in the file.</div>
        </div>
        <div class="tile">
          <div class="tile-title">Documents</div>
          <div class="tile-number" id="tile-documents">0</div>
          <div class="tile-note">How this is computed: distinct document symbols.</div>
        </div>
        <div class="tile">
          <div class="tile-title">Years</div>
          <div class="tile-number" id="tile-years">0</div>
          <div class="tile-note">How this is computed: first and last year of records.</div>
        </div>
      </div>

      <div class="tiles">
        <div class="tile">
          <div class="tile-title"><span class="tile-dot upr"></span> Universal Periodic Review</div>
          <div class="tile-number" id="tile-upr-records">0</div>
          <div class="tile-breakdown"><span id="tile-upr-documents">0</span> documents · latest <span id="tile-upr-latest">0</span></div>
          <div class="tile-note">How this is computed: records where mechanism = "Universal Periodic Review".</div>
          <div><a href="#" id="show-states-link">see the States</a></div>
        </div>
        <div class="tile">
          <div class="tile-title"><span class="tile-dot tb"></span> Treaty bodies</div>
          <div class="tile-number" id="tile-tb-records">0</div>
          <div class="tile-breakdown"><span id="tile-tb-documents">0</span> documents · latest <span id="tile-tb-latest">0</span></div>
          <div class="tile-note">How this is computed: records where mechanism = "Treaty bodies".</div>
        </div>
        <div class="tile">
          <div class="tile-title"><span class="tile-dot sp"></span> Special Procedures</div>
          <div class="tile-number" id="tile-sp-records">0</div>
          <div class="tile-breakdown"><span id="tile-sp-documents">0</span> documents · latest <span id="tile-sp-latest">0</span></div>
          <div class="tile-note">How this is computed: records where mechanism = "Special Procedures".</div>
        </div>
      </div>

      <div class="content-fig">
        <div class="content-fig-title">FIG.01 Ten most frequent themes among <span id="fig01-count">0</span> filtered records</div>
        <div class="chart-container">
          <canvas id="theme-chart"></canvas>
        </div>
        <table class="chart-table">
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
        <div class="content-fig-note">A record can carry several themes, so the bars add up to more than the record count.</div>
        <div class="content-fig-source">Source: UHRI, themes as labelled by OHCHR.</div>
      </div>

      <div class="content-fig">
        <div class="content-fig-title">FIG.02 Records per year by mechanism</div>
        <div class="chart-container">
          <canvas id="timeline-chart"></canvas>
        </div>
        <div class="content-fig-source">Source: UHRI, dated by document.</div>
      </div>
    </div>

    <div id="panel-02" role="tabpanel" aria-labelledby="tab-02" hidden>
      <div class="content-fig">
        <label for="search">Search <span id="search-count">0</span> records</label>
        <input type="text" id="search" placeholder="e.g. torture" aria-describedby="search-hint">
        <div id="search-hint" class="content-fig-note">literal match, not synonyms</div>
      </div>

      <div class="table-container">
        <table class="table">
          <caption id="table-caption">0 records shown of 0 matching</caption>
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
      </div>
      <div class="table-more">
        <button id="show-more">Show 50 more</button>
      </div>
    </div>

    <div id="panel-03" role="tabpanel" aria-labelledby="tab-03" hidden>
      <h2>CHECK THIS DASHBOARD</h2>

      <div class="check-panel">
        <h3>How the app checks itself</h3>
        <div id="check-panel-items"></div>
      </div>

      <div class="check-sample">
        <div class="check-sample-header">
          <h3>Check 10 at random</h3>
          <div>
            <button id="draw-sample">Draw again</button>
            <button id="draw-seed">Draw with this seed</button>
            <input type="number" id="sample-seed" value="1" min="1" max="1000000" style="width: 80px;">
          </div>
        </div>
        <div class="check-sample-tally" id="sample-tally">Themes: 0 fit, 0 don't, 0 unsure of 10 judged</div>
        <div class="check-sample-cards" id="sample-cards"></div>
      </div>
    </div>

    <div id="panel-04" role="tabpanel" aria-labelledby="tab-04" hidden>
      <h2>METHOD & EXPORT</h2>

      <div class="method-section">
        <h3>How each number is computed</h3>
        <p>Every number is computed by the app from the UHRI file, never estimated. The file holds <span id="method-total">0</span> records for <span id="country-name-method"></span>, dated <span id="method-years">0</span>.</p>
        <p>The headline total is the count of records in the file. The breakdown counts records per type, using the values exactly as spelled in the data. Documents is the number of distinct document symbols. Years is the first and last year of records.</p>
        <p>Filters combine with AND. Mechanism, body, type: exact match on the field. Year: year inclusive between the two selects. SDG: the record's SDGs include the goal number. Keyword: every word must occur as a substring of the text or symbol.</p>
        <p>Theme counts: for each record in the filtered set, each value in themes counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = first and last year of the filtered records carrying that theme.</p>
        <p>Timeline: records per year per mechanism in the filtered set, with zero for missing combinations. Paragraph number: the first match of a regular expression on the text. Recommending State: only for UPR; the trailing parenthesised groups, split and trimmed.</p>
      </div>

      <div class="method-section">
        <h3>Export the current filter</h3>
        <div class="export-actions">
          <button id="download-csv">Download CSV of the current filter</button>
          <button id="copy-summary">Copy summary</button>
          <span id="copy-summary-confirm" class="copied" hidden>Copied</span>
        </div>
      </div>

      <div class="method-section">
        <h3>Data source and licence</h3>
        <p>This dashboard is built on the Universal Human Rights Index (UHRI), maintained by the Office of the United Nations High Commissioner for Human Rights (OHCHR). The data is used under the <a href="https://www.ohchr.org/en/about-us/terms-use" target="_blank">OHCHR terms of use</a>.</p>
        <p>Built on <span id="built-date-method"></span>.</p>
      </div>
    </div>
  </div>
</div>

<div class="footer">
  <div>Built on OHCHR UHRI data · <span id="footer-count">0</span> records · <a id="footer-source" href="#" target="_blank">source</a></div>
  <div>Credits: UK Government Analysis Function (charts, tables), CC BY 4.0</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  // Data
  const data = window.WORKSHOP_DATA.uhri;
  const country = data.country;
  const records = data.records;
  const sdgNames = data.sdg_names;
  const sourceUrl = data.source_url;
  const builtDate = new Date(data.built).toLocaleDateString('en-GB', {day: 'numeric', month: 'short', year: 'numeric'});

  // DOM elements
  const countryNameEl = document.getElementById('country-name');
  const countryNameTitleEl = document.getElementById('country-name-title');
  const countryNameMethodEl = document.getElementById('country-name-method');
  const recordCountEl = document.getElementById('record-count');
  const documentCountEl = document.getElementById('document-count');
  const yearRangeEl = document.getElementById('year-range');
  const builtDateEl = document.getElementById('built-date');
  const builtDateMethodEl = document.getElementById('built-date-method');
  const sourceUrlEl = document.getElementById('source-url');
  const footerCountEl = document.getElementById('footer-count');
  const footerSourceEl = document.getElementById('footer-source');

  // Set static text
  countryNameEl.textContent = country;
  countryNameTitleEl.textContent = country;
  countryNameMethodEl.textContent = country;
  recordCountEl.textContent = new Intl.NumberFormat().format(records.length);
  documentCountEl.textContent = new Intl.NumberFormat().format(new Set(records.map(r => r.symbol)).size);
  const years = records.map(r => r.year);
  yearRangeEl.textContent = `${Math.min(...years)}–${Math.max(...years)}`;
  builtDateEl.textContent = builtDate;
  builtDateMethodEl.textContent = builtDate;
  sourceUrlEl.href = sourceUrl;
  sourceUrlEl.textContent = data.source;
  footerCountEl.textContent = new Intl.NumberFormat().format(records.length);
  footerSourceEl.href = sourceUrl;

  // State for filters
  let filters = {
    keyword: '',
    mechanism: '',
    body: '',
    type: '',
    state: '',
    yearFrom: '',
    yearTo: '',
    sdg: ''
  };
  let filteredRecords = [...records];
  let showCount = 50;
  let sampleSeed = 1;

  // Initialize UI
  initTabs();
  initFilters();
  initTiles();
  initThemeChart();
  initTimelineChart();
  initTable();
  initCheckPanel();
  initSample();
  updateAll();

  // Tabs
  function initTabs() {
    const tabs = document.querySelectorAll('[role="tab"]');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => {
          t.setAttribute('aria-selected', 'false');
          document.getElementById(t.getAttribute('aria-controls')).hidden = true;
        });
        tab.setAttribute('aria-selected', 'true');
        document.getElementById(tab.getAttribute('aria-controls')).hidden = false;
      });
    });
  }

  // Filters
  function initFilters() {
    // Keyword
    const keywordEl = document.getElementById('keyword');
    keywordEl.addEventListener('input', () => {
      filters.keyword = keywordEl.value.trim().toLowerCase();
      updateFilteredRecords();
    });

    // Mechanism
    const mechanismEl = document.getElementById('mechanism');
    const mechanisms = [...new Set(records.map(r => r.mechanism))];
    mechanisms.forEach(m => {
      const option = document.createElement('option');
      option.value = m;
      option.textContent = m;
      mechanismEl.appendChild(option);
    });
    mechanismEl.addEventListener('change', () => {
      filters.mechanism = mechanismEl.value;
      updateBodyOptions();
      updateTypeOptions();
      updateStateFilter();
      updateFilteredRecords();
    });

    // Body
    function updateBodyOptions() {
      const bodyOptionsEl = document.getElementById('body-options');
      bodyOptionsEl.innerHTML = '';
      const bodies = [...new Set(records
        .filter(r => !filters.mechanism || r.mechanism === filters.mechanism)
        .map(r => r.body))];
      bodies.sort();
      bodies.forEach(b => {
        const count = records.filter(r => r.body === b && (!filters.mechanism || r.mechanism === filters.mechanism)).length;
        const div = document.createElement('div');
        div.className = 'radio-option';
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'body';
        input.value = b;
        input.id = `body-${b}`;
        input.checked = filters.body === b;
        input.addEventListener('change', () => {
          filters.body = input.checked ? b : '';
          updateFilteredRecords();
        });
        const label = document.createElement('label');
        label.htmlFor = `body-${b}`;
        label.textContent = `${b} (${count})`;
        div.appendChild(input);
        div.appendChild(label);
        bodyOptionsEl.appendChild(div);
      });
    }

    // Type
    function updateTypeOptions() {
      const typeOptionsEl = document.getElementById('type-options');
      typeOptionsEl.innerHTML = '';
      const types = [...new Set(records
        .filter(r => !filters.mechanism || r.mechanism === filters.mechanism)
        .map(r => r.type))];
      types.sort();
      types.forEach(t => {
        const count = records.filter(r => r.type === t && (!filters.mechanism || r.mechanism === filters.mechanism)).length;
        const div = document.createElement('div');
        div.className = 'radio-option';
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'type';
        input.value = t;
        input.id = `type-${t}`;
        input.checked = filters.type === t;
        input.addEventListener('change', () => {
          filters.type = input.checked ? t : '';
          updateFilteredRecords();
        });
        const label = document.createElement('label');
        label.htmlFor = `type-${t}`;
        label.textContent = `${t} (${count})`;
        div.appendChild(input);
        div.appendChild(label);
        typeOptionsEl.appendChild(div);
      });
    }

    // State
    function updateStateFilter() {
      const stateFilterGroupEl = document.getElementById('state-filter-group');
      if (filters.mechanism === 'Universal Periodic Review') {
        stateFilterGroupEl.hidden = false;
        const stateEl = document.getElementById('state');
        stateEl.innerHTML = '<option value="">All States</option>';
        const states = new Map();
        records
          .filter(r => r.mechanism === 'Universal Periodic Review')
          .forEach(r => {
            const stateList = extractStates(r.text);
            stateList.forEach(s => {
              if (s !== 'State not found') {
                states.set(s, (states.get(s) || 0) + 1);
              }
            });
          });
        const sortedStates = Array.from(states.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
        sortedStates.forEach(([s, count]) => {
          const option = document.createElement('option');
          option.value = s;
          option.textContent = `${s} (${count})`;
          stateEl.appendChild(option);
        });
        stateEl.addEventListener('change', () => {
          filters.state = stateEl.value;
          updateFilteredRecords();
        });
      } else {
        stateFilterGroupEl.hidden = true;
        filters.state = '';
      }
    }

    // Year
    const yearFromEl = document.getElementById('year-from');
    const yearToEl = document.getElementById('year-to');
    const distinctYears = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
    distinctYears.forEach(y => {
      const optionFrom = document.createElement('option');
      optionFrom.value = y;
      optionFrom.textContent = y;
      yearFromEl.appendChild(optionFrom);
      const optionTo = document.createElement('option');
      optionTo.value = y;
      optionTo.textContent = y;
      yearToEl.appendChild(optionTo);
    });
    yearFromEl.addEventListener('change', () => {
      filters.yearFrom = yearFromEl.value;
      if (filters.yearTo && Number(filters.yearFrom) > Number(filters.yearTo)) {
        [filters.yearFrom, filters.yearTo] = [filters.yearTo, filters.yearFrom];
        yearFromEl.value = filters.yearFrom;
        yearToEl.value = filters.yearTo;
      }
      updateFilteredRecords();
    });
    yearToEl.addEventListener('change', () => {
      filters.yearTo = yearToEl.value;
      if (filters.yearFrom && Number(filters.yearFrom) > Number(filters.yearTo)) {
        [filters.yearFrom, filters.yearTo] = [filters.yearTo, filters.yearFrom];
        yearFromEl.value = filters.yearFrom;
        yearToEl.value = filters.yearTo;
      }
      updateFilteredRecords();
    });

    // SDG
    const sdgEl = document.getElementById('sdg');
    const sdgsPresent = new Set();
    records.forEach(r => {
      if (r.sdgs) {
        r.sdgs.forEach(s => sdgsPresent.add(s));
      }
    });
    const sortedSdgs = Array.from(sdgsPresent).sort((a, b) => a - b);
    sortedSdgs.forEach(s => {
      const option = document.createElement('option');
      option.value = s;
      option.textContent = `${s} ${sdgNames[s]}`;
      sdgEl.appendChild(option);
    });
    sdgEl.addEventListener('change', () => {
      filters.sdg = sdgEl.value;
      updateFilteredRecords();
    });

    // Clear filters
    document.getElementById('clear-filters').addEventListener('click', () => {
      filters = {
        keyword: '',
        mechanism: '',
        body: '',
        type: '',
        state: '',
        yearFrom: '',
        yearTo: '',
        sdg: ''
      };
      document.getElementById('keyword').value = '';
      document.getElementById('mechanism').value = '';
      document.getElementById('state').value = '';
      document.getElementById('year-from').value = '';
      document.getElementById('year-to').value = '';
      document.getElementById('sdg').value = '';
      updateBodyOptions();
      updateTypeOptions();
      updateStateFilter();
      updateFilteredRecords();
    });

    // Filter headings
    document.getElementById('filter-heading-01').addEventListener('click', () => {
      const isExpanded = document.getElementById('filter-heading-01').getAttribute('aria-expanded') === 'true';
      document.getElementById('filter-heading-01').setAttribute('aria-expanded', !isExpanded);
      document.getElementById('filter-heading-02').setAttribute('aria-expanded', false);
      document.getElementById('filter-heading-03').setAttribute('aria-expanded', false);
    });
    document.getElementById('filter-heading-02').addEventListener('click', () => {
      const isExpanded = document.getElementById('filter-heading-02').getAttribute('aria-expanded') === 'true';
      document.getElementById('filter-heading-02').setAttribute('aria-expanded', !isExpanded);
      document.getElementById('filter-heading-01').setAttribute('aria-expanded', false);
      document.getElementById('filter-heading-03').setAttribute('aria-expanded', false);
    });
    document.getElementById('filter-heading-03').addEventListener('click', () => {
      const isExpanded = document.getElementById('filter-heading-03').getAttribute('aria-expanded') === 'true';
      document.getElementById('filter-heading-03').setAttribute('aria-expanded', !isExpanded);
      document.getElementById('filter-heading-01').setAttribute('aria-expanded', false);
      document.getElementById('filter-heading-02').setAttribute('aria-expanded', false);
    });
  }

  // Update filtered records
  function updateFilteredRecords() {
    filteredRecords = records.filter(record => {
      // Keyword
      if (filters.keyword) {
        const words = filters.keyword.split(/\s+/).filter(w => w);
        if (!words.every(w => record.text.toLowerCase().includes(w) || record.symbol.toLowerCase().includes(w))) {
          return false;
        }
      }
      // Mechanism
      if (filters.mechanism && record.mechanism !== filters.mechanism) {
        return false;
      }
      // Body
      if (filters.body && record.body !== filters.body) {
        return false;
      }
      // Type
      if (filters.type && record.type !== filters.type) {
        return false;
      }
      // State
      if (filters.state && record.mechanism === 'Universal Periodic Review') {
        const states = extractStates(record.text);
        if (!states.includes(filters.state)) {
          return false;
        }
      }
      // Year
      if (filters.yearFrom && record.year < Number(filters.yearFrom)) {
        return false;
      }
      if (filters.yearTo && record.year > Number(filters.yearTo)) {
        return false;
      }
      // SDG
      if (filters.sdg && (!record.sdgs || !record.sdgs.includes(Number(filters.sdg)))) {
        return false;
      }
      return true;
    });
    updateAll();
  }

  // Update all UI
  function updateAll() {
    updateFilteredCount();
    updateActiveFilters();
    updateTiles();
    updateThemeChart();
    updateTimelineChart();
    updateTable();
    updateCheckPanel();
    updateSample();
  }

  // Update filtered count
  function updateFilteredCount() {
    const countEl = document.getElementById('filtered-count');
    const barEl = document.getElementById('filtered-bar');
    const count = filteredRecords.length;
    const total = records.length;
    countEl.textContent = `${new Intl.NumberFormat().format(count)} of ${new Intl.NumberFormat().format(total)} in the file`;
    barEl.style.width = `${(count / total) * 100}%`;
  }

  // Update active filters
  function updateActiveFilters() {
    const activeFiltersEl = document.getElementById('active-filters');
    activeFiltersEl.innerHTML = '';
    if (filters.keyword) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `Keyword: ${filters.keyword}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.keyword = '';
        document.getElementById('keyword').value = '';
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.mechanism) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `Mechanism: ${filters.mechanism}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.mechanism = '';
        document.getElementById('mechanism').value = '';
        updateBodyOptions();
        updateTypeOptions();
        updateStateFilter();
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.body) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `Body: ${filters.body}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.body = '';
        updateBodyOptions();
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.type) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `Type: ${filters.type}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.type = '';
        updateTypeOptions();
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.state) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `State: ${filters.state}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.state = '';
        document.getElementById('state').value = '';
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.yearFrom) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `Year from: ${filters.yearFrom}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.yearFrom = '';
        document.getElementById('year-from').value = '';
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.yearTo) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `Year to: ${filters.yearTo}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.yearTo = '';
        document.getElementById('year-to').value = '';
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
    if (filters.sdg) {
      const chip = document.createElement('div');
      chip.className = 'rail-filter-chip';
      chip.textContent = `SDG: ${filters.sdg} ${sdgNames[filters.sdg]}`;
      const button = document.createElement('button');
      button.addEventListener('click', () => {
        filters.sdg = '';
        document.getElementById('sdg').value = '';
        updateFilteredRecords();
      });
      chip.appendChild(button);
      activeFiltersEl.appendChild(chip);
    }
  }

  // Tiles
  function initTiles() {
    // Already initialized in updateTiles
  }

  function updateTiles() {
    const total = filteredRecords.length;
    const typeCounts = {};
    records.forEach(r => {
      typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
    });
    const typeBreakdown = Object.entries(typeCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([type, count]) => `${type}: ${new Intl.NumberFormat().format(count)}`)
      .join(' · ');
    document.getElementById('tile-total').textContent = new Intl.NumberFormat().format(total);
    document.getElementById('tile-breakdown').textContent = typeBreakdown;
    document.getElementById('tile-documents').textContent = new Intl.NumberFormat().format(new Set(filteredRecords.map(r => r.symbol)).size);
    const years = filteredRecords.map(r => r.year);
    document.getElementById('tile-years').textContent = years.length ? `${Math.min(...years)}–${Math.max(...years)}` : '–';

    // Mechanism tiles
    const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
    const tbRecords = filteredRecords.filter(r => r.mechanism === 'Treaty bodies');
    const spRecords = filteredRecords.filter(r => r.mechanism === 'Special Procedures');

    document.getElementById('tile-upr-records').textContent = new Intl.NumberFormat().format(uprRecords.length);
    document.getElementById('tile-upr-documents').textContent = new Intl.NumberFormat().format(new Set(uprRecords.map(r => r.symbol)).size);
    document.getElementById('tile-upr-latest').textContent = uprRecords.length ? Math.max(...uprRecords.map(r => r.year)) : '–';

    document.getElementById('tile-tb-records').textContent = new Intl.NumberFormat().format(tbRecords.length);
    document.getElementById('tile-tb-documents').textContent = new Intl.NumberFormat().format(new Set(tbRecords.map(r => r.symbol)).size);
    document.getElementById('tile-tb-latest').textContent = tbRecords.length ? Math.max(...tbRecords.map(r => r.year)) : '–';

    document.getElementById('tile-sp-records').textContent = new Intl.NumberFormat().format(spRecords.length);
    document.getElementById('tile-sp-documents').textContent = new Intl.NumberFormat().format(new Set(spRecords.map(r => r.symbol)).size);
    document.getElementById('tile-sp-latest').textContent = spRecords.length ? Math.max(...spRecords.map(r => r.year)) : '–';

    // States link
    const showStatesLinkEl = document.getElementById('show-states-link');
    if (filters.mechanism === 'Universal Periodic Review' || !filters.mechanism) {
      showStatesLinkEl.hidden = false;
      showStatesLinkEl.onclick = (e) => {
        e.preventDefault();
        const states = new Map();
        uprRecords.forEach(r => {
          const stateList = extractStates(r.text);
          stateList.forEach(s => {
            if (s !== 'State not found') {
              states.set(s, (states.get(s) || 0) + 1);
            }
          });
        });
        const sortedStates = Array.from(states.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 10);
        const statesText = sortedStates.map(([s, count]) => `${s}: ${count}`).join(' · ');
        alert(`Ten States that made most recommendations to ${country}:\n\n${statesText}`);
      };
    } else {
      showStatesLinkEl.hidden = true;
    }
  }

  // Theme chart
  let themeChart;
  function initThemeChart() {
    const ctx = document.getElementById('theme-chart').getContext('2d');
    themeChart = new Chart(ctx, {
      type: 'bar',
      data: { labels: [], datasets: [{ data: [], backgroundColor: '#9b2335cc' }] },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.parsed.x} records`;
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: {
              callback: (value) => new Intl.NumberFormat().format(value)
            }
          },
          y: {
            grid: { display: false }
          }
        },
        onClick: (e, activeEls) => {
          if (activeEls.length) {
            const index = activeEls[0].index;
            const theme = themeChart.data.labels[index];
            const keywordEl = document.getElementById('keyword');
            keywordEl.value = theme;
            filters.keyword = theme;
            updateFilteredRecords();
          }
        }
      }
    });
  }

  function updateThemeChart() {
    const themeCounts = {};
    filteredRecords.forEach(record => {
      if (record.themes) {
        record.themes.forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      }
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const labels = sortedThemes.map(([theme]) => theme);
    const data = sortedThemes.map(([, count]) => count);
    const percentages = sortedThemes.map(([, count]) => ((count / filteredRecords.length) * 100).toFixed(1));
    const yearRanges = sortedThemes.map(([theme]) => {
      const years = filteredRecords
        .filter(r => r.themes && r.themes.includes(theme))
        .map(r => r.year);
      return years.length ? `${Math.min(...years)}–${Math.max(...years)}` : '–';
    });

    themeChart.data.labels = labels;
    themeChart.data.datasets[0].data = data;
    themeChart.update();

    const tableBodyEl = document.getElementById('theme-table-body');
    tableBodyEl.innerHTML = '';
    sortedThemes.forEach(([theme, count], i) => {
      const tr = document.createElement('tr');
      const tdTheme = document.createElement('td');
      tdTheme.textContent = theme;
      const tdCount = document.createElement('td');
      tdCount.textContent = new Intl.NumberFormat().format(count);
      const tdPercent = document.createElement('td');
      tdPercent.textContent = `${percentages[i]}%`;
      const tdYears = document.createElement('td');
      tdYears.textContent = yearRanges[i];
      tr.appendChild(tdTheme);
      tr.appendChild(tdCount);
      tr.appendChild(tdPercent);
      tr.appendChild(tdYears);
      tableBodyEl.appendChild(tr);
    });

    document.getElementById('fig01-count').textContent = new Intl.NumberFormat().format(filteredRecords.length);
  }

  // Timeline chart
  let timelineChart;
  function initTimelineChart() {
    const ctx = document.getElementById('timeline-chart').getContext('2d');
    timelineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [
          { label: 'Universal Periodic Review', data: [], backgroundColor: '#c2410c' },
          { label: 'Treaty bodies', data: [], backgroundColor: '#0f766e' },
          { label: 'Special Procedures', data: [], backgroundColor: '#7c3aed' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${new Intl.NumberFormat().format(context.parsed.y)}`;
              }
            }
          }
        },
        scales: {
          x: { stacked: true },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: (value) => new Intl.NumberFormat().format(value)
            }
          }
        }
      }
    });
  }

  function updateTimelineChart() {
    const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
    const uprData = years.map(y => filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review' && r.year === y).length);
    const tbData = years.map(y => filteredRecords.filter(r => r.mechanism === 'Treaty bodies' && r.year === y).length);
    const spData = years.map(y => filteredRecords.filter(r => r.mechanism === 'Special Procedures' && r.year === y).length);

    timelineChart.data.labels = years.map(y => y.toString());
    timelineChart.data.datasets[0].data = uprData;
    timelineChart.data.datasets[1].data = tbData;
    timelineChart.data.datasets[2].data = spData;
    timelineChart.update();
  }

  // Table
  function initTable() {
    document.getElementById('search').addEventListener('input', () => {
      const searchEl = document.getElementById('search');
      const searchCountEl = document.getElementById('search-count');
      const searchTerm = searchEl.value.trim().toLowerCase();
      const matchingRecords = filteredRecords.filter(record => {
        return !searchTerm || record.text.toLowerCase().includes(searchTerm) || record.symbol.toLowerCase().includes(searchTerm);
      });
      searchCountEl.textContent = new Intl.NumberFormat().format(matchingRecords.length);
      renderTable(matchingRecords);
    });

    document.getElementById('show-more').addEventListener('click', () => {
      showCount += 50;
      renderTable(filteredRecords);
    });
  }

  function updateTable() {
    document.getElementById('search').value = '';
    document.getElementById('search-count').textContent = new Intl.NumberFormat().format(filteredRecords.length);
    showCount = 50;
    renderTable(filteredRecords);
  }

  function renderTable(recordsToShow) {
    const tableBodyEl = document.getElementById('table-body');
    tableBodyEl.innerHTML = '';
    const searchTerm = document.getElementById('search').value.trim().toLowerCase();
    const searchWords = searchTerm.split(/\s+/).filter(w => w);

    const captionEl = document.getElementById('table-caption');
    captionEl.textContent = `${Math.min(showCount, recordsToShow.length)} records shown of ${new Intl.NumberFormat().format(recordsToShow.length)} matching`;

    const sortedRecords = [...recordsToShow].sort((a, b) => {
      if (b.date !== a.date) return b.date.localeCompare(a.date);
      if (a.body !== b.body) return a.body.localeCompare(b.body);
      const aPara = extractParagraphNumber(a.text);
      const bPara = extractParagraphNumber(b.text);
      if (aPara && bPara) return aPara.localeCompare(bPara);
      if (aPara) return -1;
      if (bPara) return 1;
      return 0;
    });

    const shownRecords = sortedRecords.slice(0, showCount);
    shownRecords.forEach(record => {
      const tr = document.createElement('tr');
      tr.tabIndex = 0;
      tr.addEventListener('click', () => {
        const isExpanded = tr.getAttribute('aria-expanded') === 'true';
        tr.setAttribute('aria-expanded', !isExpanded);
      });
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const isExpanded = tr.getAttribute('aria-expanded') === 'true';
          tr.setAttribute('aria-expanded', !isExpanded);
        }
      });

      const tdDate = document.createElement('td');
      tdDate.textContent = record.date;

      const tdBody = document.createElement('td');
      tdBody.textContent = record.body;

      const tdSymbol = document.createElement('td');
      const aSymbol = document.createElement('a');
      aSymbol.href = record.doc_url;
      aSymbol.textContent = record.symbol;
      aSymbol.target = '_blank';
      tdSymbol.appendChild(aSymbol);

      const tdPara = document.createElement('td');
      tdPara.textContent = extractParagraphNumber(record.text) || '–';

      const tdState = document.createElement('td');
      if (record.mechanism === 'Universal Periodic Review') {
        const states = extractStates(record.text);
        tdState.textContent = states.join(', ');
      } else {
        tdState.textContent = '–';
      }

      const tdFirstLine = document.createElement('td');
      let firstLine = record.text;
      if (firstLine.length > 120) {
        firstLine = firstLine.substring(0, 120);
        const lastSpace = firstLine.lastIndexOf(' ');
        if (lastSpace > 0) {
          firstLine = firstLine.substring(0, lastSpace) + '…';
        } else {
          firstLine = firstLine + '…';
        }
      }
      if (searchTerm) {
        searchWords.forEach(word => {
          const regex = new RegExp(word, 'gi');
          firstLine = firstLine.replace(regex, match => `<mark>${match}</mark>`);
        });
      }
      tdFirstLine.innerHTML = firstLine;

      tr.appendChild(tdDate);
      tr.appendChild(tdBody);
      tr.appendChild(tdSymbol);
      tr.appendChild(tdPara);
      tr.appendChild(tdState);
      tr.appendChild(tdFirstLine);
      tableBodyEl.appendChild(tr);

      const trDetails = document.createElement('tr');
      trDetails.hidden = true;
      trDetails.setAttribute('aria-expanded', 'false');
      const tdDetails = document.createElement('td');
      tdDetails.colSpan = 6;
      const divDetails = document.createElement('div');
      divDetails.className = 'table-row-details';

      const h4Para = document.createElement('h4');
      h4Para.textContent = extractParagraphNumber(record.text) || 'No paragraph number';

      const pText = document.createElement('p');
      pText.textContent = record.text;

      const divLabels = document.createElement('div');
      divLabels.className = 'table-row-details-labels';
      if (record.themes && record.themes.length) {
        record.themes.forEach(theme => {
          const span = document.createElement('span');
          span.className = 'table-row-details-label';
          span.textContent = theme;
          divLabels.appendChild(span);
        });
      }
      if (record.sdgs && record.sdgs.length) {
        record.sdgs.forEach(sdg => {
          const span = document.createElement('span');
          span.className = 'table-row-details-label';
          span.textContent = `SDG ${sdg} ${sdgNames[sdg]}`;
          divLabels.appendChild(span);
        });
      }
      if (record.sdg_targets && record.sdg_targets.length) {
        record.sdg_targets.forEach(target => {
          const span = document.createElement('span');
          span.className = 'table-row-details-label';
          span.textContent = target;
          divLabels.appendChild(span);
        });
      }
      if (record.affected_persons && record.affected_persons.length) {
        record.affected_persons.forEach(person => {
          const span = document.createElement('span');
          span.className = 'table-row-details-label';
          span.textContent = person;
          divLabels.appendChild(span);
        });
      }
      if (record.section) {
        const span = document.createElement('span');
        span.className = 'table-row-details-label';
        span.textContent = record.section;
        divLabels.appendChild(span);
      }

      const divActions = document.createElement('div');
      divActions.className = 'table-row-details-actions';
      const buttonCopy = document.createElement('button');
      buttonCopy.textContent = extractParagraphNumber(record.text) ? 'Copy citation' : 'Copy citation (no paragraph number in this extract)';
      buttonCopy.addEventListener('click', () => {
        const citation = extractParagraphNumber(record.text)
          ? `${record.symbol}, para. ${extractParagraphNumber(record.text)}`
          : record.symbol;
        navigator.clipboard.writeText(citation).then(() => {
          const spanCopied = document.createElement('span');
          spanCopied.className = 'copied';
          spanCopied.textContent = 'Copied';
          divActions.appendChild(spanCopied);
          setTimeout(() => spanCopied.remove(), 2000);
        });
      });
      const buttonOpen = document.createElement('button');
      buttonOpen.textContent = 'Open the UN document';
      buttonOpen.addEventListener('click', () => {
        window.open(record.doc_url, '_blank');
      });
      divActions.appendChild(buttonCopy);
      divActions.appendChild(buttonOpen);

      const divSource = document.createElement('div');
      divSource.className = 'table-row-details-source';
      divSource.textContent = `Source: ${record.symbol} (${record.date})`;

      divDetails.appendChild(h4Para);
      divDetails.appendChild(pText);
      divDetails.appendChild(divLabels);
      divDetails.appendChild(divActions);
      divDetails.appendChild(divSource);
      tdDetails.appendChild(divDetails);
      trDetails.appendChild(tdDetails);
      tableBodyEl.appendChild(trDetails);

      tr.setAttribute('aria-expanded', 'false');
      tr.addEventListener('click', () => {
        const isExpanded = tr.getAttribute('aria-expanded') === 'true';
        tr.setAttribute('aria-expanded', !isExpanded);
        trDetails.hidden = isExpanded;
        trDetails.setAttribute('aria-expanded', !isExpanded);
      });
    });

    document.getElementById('show-more').hidden = showCount >= recordsToShow.length;
  }

  // Check panel
  function initCheckPanel() {
    // Already initialized in updateCheckPanel
  }

  function updateCheckPanel() {
    const checkPanelEl = document.getElementById('check-panel-items');
    checkPanelEl.innerHTML = '';

    // Record count
    const recordCountItem = document.createElement('div');
    recordCountItem.className = 'check-panel-item';
    const fileCount = Number(data.count);
    if (records.length === fileCount) {
      recordCountItem.classList.add('pass');
      recordCountItem.textContent = `Record count: ${new Intl.NumberFormat().format(records.length)} (matches the file)`;
    } else {
      recordCountItem.classList.add('fail');
      recordCountItem.textContent = `Record count: ${new Intl.NumberFormat().format(records.length)} (file says ${new Intl.NumberFormat().format(fileCount)})`;
    }
    checkPanelEl.appendChild(recordCountItem);

    // Partitions
    const mechanismCounts = {};
    const bodyCounts = {};
    const yearCounts = {};
    records.forEach(r => {
      mechanismCounts[r.mechanism] = (mechanismCounts[r.mechanism] || 0) + 1;
      bodyCounts[r.body] = (bodyCounts[r.body] || 0) + 1;
      yearCounts[r.year] = (yearCounts[r.year] || 0) + 1;
    });
    const mechanismSum = Object.values(mechanismCounts).reduce((a, b) => a + b, 0);
    const bodySum = Object.values(bodyCounts).reduce((a, b) => a + b, 0);
    const yearSum = Object.values(yearCounts).reduce((a, b) => a + b, 0);

    const mechanismItem = document.createElement('div');
    mechanismItem.className = 'check-panel-item';
    if (mechanismSum === records.length) {
      mechanismItem.classList.add('pass');
      mechanismItem.textContent = `Mechanism partition: ${new Intl.NumberFormat().format(mechanismSum)} (sums to record count)`;
    } else {
      mechanismItem.classList.add('fail');
      mechanismItem.textContent = `Mechanism partition: ${new Intl.NumberFormat().format(mechanismSum)} (should be ${new Intl.NumberFormat().format(records.length)})`;
    }
    checkPanelEl.appendChild(mechanismItem);

    const bodyItem = document.createElement('div');
    bodyItem.className = 'check-panel-item';
    if (bodySum === records.length) {
      bodyItem.classList.add('pass');
      bodyItem.textContent = `Body partition: ${new Intl.NumberFormat().format(bodySum)} (sums to record count)`;
    } else {
      bodyItem.classList.add('fail');
      bodyItem.textContent = `Body partition: ${new Intl.NumberFormat().format(bodySum)} (should be ${new Intl.NumberFormat().format(records.length)})`;
    }
    checkPanelEl.appendChild(bodyItem);

    const yearItem = document.createElement('div');
    yearItem.className = 'check-panel-item';
    if (yearSum === records.length) {
      yearItem.classList.add('pass');
      yearItem.textContent = `Year partition: ${new Intl.NumberFormat().format(yearSum)} (sums to record count)`;
    } else {
      yearItem.classList.add('fail');
      yearItem.textContent = `Year partition: ${new Intl.NumberFormat().format(yearSum)} (should be ${new Intl.NumberFormat().format(records.length)})`;
    }
    checkPanelEl.appendChild(yearItem);

    // Type partition
    const typeCounts = {};
    records.forEach(r => {
      typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
    });
    const typeSum = Object.values(typeCounts).reduce((a, b) => a + b, 0);
    const typeItem = document.createElement('div');
    typeItem.className = 'check-panel-item';
    if (typeSum === records.length) {
      typeItem.classList.add('pass');
      typeItem.textContent = `Type partition: ${new Intl.NumberFormat().format(typeSum)} (sums to record count)`;
    } else {
      typeItem.classList.add('fail');
      typeItem.textContent = `Type partition: ${new Intl.NumberFormat().format(typeSum)} (should be ${new Intl.NumberFormat().format(records.length)})`;
    }
    checkPanelEl.appendChild(typeItem);

    // Chart against table
    const themeCounts = {};
    filteredRecords.forEach(record => {
      if (record.themes) {
        record.themes.forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      }
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const chartData = sortedThemes.map(([, count]) => count);
    const tableData = sortedThemes.map(([theme]) => {
      return filteredRecords.filter(r => r.themes && r.themes.includes(theme)).length;
    });
    const chartMatch = chartData.every((v, i) => v === tableData[i]);
    const chartItem = document.createElement('div');
    chartItem.className = 'check-panel-item';
    if (chartMatch) {
      chartItem.classList.add('pass');
      chartItem.textContent = `Chart against table: top 10 themes match`;
    } else {
      chartItem.classList.add('fail');
      chartItem.textContent = `Chart against table: top 10 themes do not match`;
    }
    checkPanelEl.appendChild(chartItem);

    // Links
    const linkErrors = records.filter(r => !r.doc_url.startsWith('https://docs.un.org/') || !decodeURIComponent(r.doc_url).toLowerCase().endsWith(r.symbol.toLowerCase()));
    const linkItem = document.createElement('div');
    linkItem.className = 'check-panel-item';
    if (linkErrors.length === 0) {
      linkItem.classList.add('pass');
      linkItem.textContent = `Links: all ${new Intl.NumberFormat().format(records.length)} doc_url start with "https://docs.un.org/" and end with the symbol`;
    } else {
      linkItem.classList.add('fail');
      linkItem.textContent = `Links: ${new Intl.NumberFormat().format(linkErrors.length)} records fail (listed below)`;
      linkErrors.forEach(r => {
        const div = document.createElement('div');
        div.textContent = `${r.symbol}: ${r.doc_url}`;
        linkItem.appendChild(div);
      });
    }
    checkPanelEl.appendChild(linkItem);

    // Paragraph numbers
    const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
    const uprWithPara = uprRecords.filter(r => extractParagraphNumber(r.text));
    const uprParaItem = document.createElement('div');
    uprParaItem.className = 'check-panel-item';
    if (uprWithPara.length === uprRecords.length) {
      uprParaItem.classList.add('pass');
      uprParaItem.textContent = `Paragraph numbers: all ${new Intl.NumberFormat().format(uprRecords.length)} UPR records have a number`;
    } else {
      uprParaItem.classList.add('warn');
      uprParaItem.textContent = `Paragraph numbers: ${new Intl.NumberFormat().format(uprWithPara.length)} of ${new Intl.NumberFormat().format(uprRecords.length)} UPR records have a number (${new Intl.NumberFormat().format(uprRecords.length - uprWithPara.length)} missing)`;
    }
    checkPanelEl.appendChild(uprParaItem);

    const tbRecords = records.filter(r => r.mechanism === 'Treaty bodies');
    const tbWithPara = tbRecords.filter(r => extractParagraphNumber(r.text));
    const tbParaItem = document.createElement('div');
    tbParaItem.className = 'check-panel-item';
    tbParaItem.textContent = `Paragraph numbers: ${new Intl.NumberFormat().format(tbWithPara.length)} of ${new Intl.NumberFormat().format(tbRecords.length)} treaty-body records have a number`;
    checkPanelEl.appendChild(tbParaItem);

    const spRecords = records.filter(r => r.mechanism === 'Special Procedures');
    const spWithPara = spRecords.filter(r => extractParagraphNumber(r.text));
    const spParaItem = document.createElement('div');
    spParaItem.className = 'check-panel-item';
    spParaItem.textContent = `Paragraph numbers: ${new Intl.NumberFormat().format(spWithPara.length)} of ${new Intl.NumberFormat().format(spRecords.length)} Special Procedures records have a number`;
    checkPanelEl.appendChild(spParaItem);

    // States found
    const uprWithState = uprRecords.filter(r => {
      const states = extractStates(r.text);
      return states.some(s => s !== 'State not found');
    });
    const stateItem = document.createElement('div');
    stateItem.className = 'check-panel-item';
    if (uprWithState.length === uprRecords.length) {
      stateItem.classList.add('pass');
      stateItem.textContent = `States found: all ${new Intl.NumberFormat().format(uprRecords.length)} UPR records have at least one State`;
    } else {
      stateItem.classList.add('warn');
      stateItem.textContent = `States found: ${new Intl.NumberFormat().format(uprWithState.length)} of ${new Intl.NumberFormat().format(uprRecords.length)} UPR records have at least one State (${new Intl.NumberFormat().format(uprRecords.length - uprWithState.length)} missing)`;
      const missing = uprRecords.filter(r => {
        const states = extractStates(r.text);
        return !states.some(s => s !== 'State not found');
      });
      missing.forEach(r => {
        const div = document.createElement('div');
        div.textContent = `${r.symbol}: ${r.text.substring(r.text.length - 50)}`;
        stateItem.appendChild(div);
      });
    }
    checkPanelEl.appendChild(stateItem);

    // Duplicates and gaps
    const distinctIds = new Set(records.map(r => r.id)).size;
    const idItem = document.createElement('div');
    idItem.className = 'check-panel-item';
    if (distinctIds === records.length) {
      idItem.classList.add('pass');
      idItem.textContent = `Distinct id: ${new Intl.NumberFormat().format(distinctIds)} (no duplicates)`;
    } else {
      idItem.classList.add('fail');
      idItem.textContent = `Distinct id: ${new Intl.NumberFormat().format(distinctIds)} (should be ${new Intl.NumberFormat().format(records.length)})`;
    }
    checkPanelEl.appendChild(idItem);

    const duplicateTexts = records.reduce((acc, r) => {
      acc[r.text] = (acc[r.text] || 0) + 1;
      return acc;
    }, {});
    const duplicateCount = Object.values(duplicateTexts).filter(v => v > 1).reduce((a, b) => a + b, 0) - Object.values(duplicateTexts).filter(v => v > 1).length;
    const duplicateItem = document.createElement('div');
    duplicateItem.className = 'check-panel-item';
    duplicateItem.textContent = `Duplicate text: ${new Intl.NumberFormat().format(duplicateCount)} records`;
    checkPanelEl.appendChild(duplicateItem);

    const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
    const noThemesItem = document.createElement('div');
    noThemesItem.className = 'check-panel-item';
    noThemesItem.textContent = `Not labelled (themes): ${new Intl.NumberFormat().format(noThemes)} records`;
    checkPanelEl.appendChild(noThemesItem);

    const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    const noSdgsItem = document.createElement('div');
    noSdgsItem.className = 'check-panel-item';
    noSdgsItem.textContent = `Not labelled (SDGs): ${new Intl.NumberFormat().format(noSdgs)} records`;
    checkPanelEl.appendChild(noSdgsItem);

    const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
    const noAffectedItem = document.createElement('div');
    noAffectedItem.className = 'check-panel-item';
    noAffectedItem.textContent = `Not labelled (affected persons): ${new Intl.NumberFormat().format(noAffected)} records`;
    checkPanelEl.appendChild(noAffectedItem);
  }

  // Sample
  function initSample() {
    document.getElementById('draw-sample').addEventListener('click', () => {
      sampleSeed = Math.floor(Math.random() * 1000000) + 1;
      document.getElementById('sample-seed').value = sampleSeed;
      renderSample();
    });
    document.getElementById('draw-seed').addEventListener('click', () => {
      sampleSeed = Number(document.getElementById('sample-seed').value);
      renderSample();
    });
  }

  function updateSample() {
    renderSample();
  }

  function renderSample() {
    const sampleCardsEl = document.getElementById('sample-cards');
    sampleCardsEl.innerHTML = '';
    const tallyEl = document.getElementById('sample-tally');
    tallyEl.textContent = `Themes: 0 fit, 0 don't, 0 unsure of 10 judged (seed ${sampleSeed})`;

    const seed = sampleSeed;
    const rng = mulberry32(seed);
    const shuffled = [...filteredRecords].sort(() => rng() - 0.5);
    const sample = shuffled.slice(0, 10);

    let fit = 0, dont = 0, unsure = 0;
    sample.forEach((record, i) => {
      const cardEl = document.createElement('div');
      cardEl.className = 'check-sample-card';
      cardEl.setAttribute('aria-expanded', 'false');

      const headerEl = document.createElement('div');
      headerEl.className = 'check-sample-card-header';
      headerEl.addEventListener('click', () => {
        const isExpanded = cardEl.getAttribute('aria-expanded') === 'true';
        cardEl.setAttribute('aria-expanded', !isExpanded);
      });

      const titleEl = document.createElement('div');
      titleEl.className = 'check-sample-card-title';
      const aSymbol = document.createElement('a');
      aSymbol.href = record.doc_url;
      aSymbol.textContent = record.symbol;
      aSymbol.target = '_blank';
      titleEl.appendChild(aSymbol);
      titleEl.appendChild(document.createTextNode(`, para. ${extractParagraphNumber(record.text) || '–'}`));

      const buttonEl = document.createElement('button');
      buttonEl.setAttribute('aria-expanded', 'false');

      headerEl.appendChild(titleEl);
      headerEl.appendChild(buttonEl);
      cardEl.appendChild(headerEl);

      const detailsEl = document.createElement('div');
      detailsEl.className = 'check-sample-card-details';

      const pText = document.createElement('p');
      pText.textContent = record.text;

      const divLabels = document.createElement('div');
      divLabels.className = 'check-sample-card-labels';
      if (record.themes && record.themes.length) {
        record.themes.forEach(theme => {
          const span = document.createElement('span');
          span.className = 'check-sample-card-label';
          span.textContent = theme;
          divLabels.appendChild(span);
        });
      }

      const divActions = document.createElement('div');
      divActions.className = 'check-sample-card-actions';
      const buttonFit = document.createElement('button');
      buttonFit.className = 'fit';
      buttonFit.textContent = 'Fits';
      buttonFit.addEventListener('click', () => {
        fit++;
        updateTally();
      });
      const buttonDont = document.createElement('button');
      buttonDont.className = 'dont';
      buttonDont.textContent = "Doesn't fit";
      buttonDont.addEventListener('click', () => {
        dont++;
        updateTally();
      });
      const buttonUnsure = document.createElement('button');
      buttonUnsure.className = 'unsure';
      buttonUnsure.textContent = 'Unsure';
      buttonUnsure.addEventListener('click', () => {
        unsure++;
        updateTally();
      });
      divActions.appendChild(buttonFit);
      divActions.appendChild(buttonDont);
      divActions.appendChild(buttonUnsure);

      detailsEl.appendChild(pText);
      detailsEl.appendChild(divLabels);
      detailsEl.appendChild(divActions);
      cardEl.appendChild(detailsEl);

      sampleCardsEl.appendChild(cardEl);

      function updateTally() {
        tallyEl.textContent = `Themes: ${fit} fit, ${dont} don't, ${unsure} unsure of 10 judged (seed ${seed})`;
      }
    });
  }

  // Export
  document.getElementById('download-csv').addEventListener('click', () => {
    const headers = [
      'Date', 'Year', 'Body', 'Mechanism', 'Type', 'Symbol', 'Paragraph', 'Recommending State',
      'First line', 'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Text'
    ];
    const rows = filteredRecords.map(record => {
      const state = record.mechanism === 'Universal Periodic Review' ? extractStates(record.text).join('; ') : '';
      return [
        record.date,
        record.year,
        record.body,
        record.mechanism,
        record.type,
        record.symbol,
        extractParagraphNumber(record.text) || '',
        state,
        record.text.substring(0, 120).replace(/\n/g, ' '),
        record.themes ? record.themes.join('; ') : '',
        record.sdgs ? record.sdgs.map(s => `${s} ${sdgNames[s]}`).join('; ') : '',
        record.sdg_targets ? record.sdg_targets.join('; ') : '',
        record.affected_persons ? record.affected_persons.join('; ') : '',
        record.section || '',
        record.text.replace(/\n/g, ' ')
      ];
    });
    const csvContent = [
      `# UN human rights recommendations and observations: ${country}`,
      `# Source: ${data.source} (${sourceUrl})`,
      `# Built: ${builtDate}`,
      `# Filters: ${JSON.stringify(filters)}`,
      `# Records: ${filteredRecords.length}`,
      headers.join(','),
      ...rows.map(row => row.map(field => `"${field.replace(/"/g, '""')}"`).join(','))
    ].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `uhri-${country.toLowerCase()}-${new Date().toISOString().substring(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  });

  document.getElementById('copy-summary').addEventListener('click', () => {
    const themeCounts = {};
    filteredRecords.forEach(record => {
      if (record.themes) {
        record.themes.forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      }
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10)
      .map(([theme, count]) => `${theme} (${count})`)
      .join(', ');
    const summary = `UN human rights recommendations and observations for ${country}: ${new Intl.NumberFormat().format(filteredRecords.length)} records from ${new Set(filteredRecords.map(r => r.symbol)).size} documents, ${Math.min(...filteredRecords.map(r => r.year))}–${Math.max(...filteredRecords.map(r => r.year))}. Top themes: ${sortedThemes}.`;
    navigator.clipboard.writeText(summary).then(() => {
      const spanCopied = document.getElementById('copy-summary-confirm');
      spanCopied.hidden = false;
      setTimeout(() => spanCopied.hidden = true, 2000);
    });
  });

  // Helper functions
  function extractParagraphNumber(text) {
    const match = text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
    return match ? match[1] : null;
  }

  function extractStates(text) {
    const match = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
    if (!match) return ['State not found'];
    const groups = match[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
    return groups.map(g => {
      const state = g.substring(1, g.length - 1).trim();
      if (state.includes(',') || state.length > 60) return 'State not found';
      return state;
    }).filter(s => s !== 'State not found');
  }

  // Seeded random number generator
  function mulberry32(a) {
    return function() {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
});
</script>
</body>
</html>
```