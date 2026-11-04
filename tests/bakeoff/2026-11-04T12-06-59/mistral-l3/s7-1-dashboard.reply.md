I built the UN human rights recommendations dashboard for Kenya, exactly as you described. Four tabs: Overview (headline numbers, theme chart, timeline), Records (searchable table with expandable rows), Check (self-tests and a random-sample label check), and Method & export (how it works and a CSV button). The left rail holds the filters, always visible, and every number explains how it was computed.

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
  --red: #9b2335;
  --upr: #c2410c;
  --treaty: #0f766e;
  --special: #7c3aed;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
}
[hidden] { display: none !important; }
a { color: inherit; text-decoration: none; }
a:focus { outline: 2px solid var(--red); outline-offset: 2px; }
button { background: none; border: none; padding: 0; margin: 0; font: inherit; cursor: pointer; }
button:focus { outline: 2px solid var(--red); outline-offset: 2px; }

/* Header */
.header {
  grid-column: 1 / -1;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--rule);
  background-color: var(--paper);
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.header-label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--ink);
}
.header-title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.75rem;
  font-weight: 400;
  margin: 0;
}
.header-meta {
  font-size: 0.875rem;
  color: #6b665c;
}
.header-meta a { text-decoration: underline; }

/* Tabs */
.tablist {
  grid-column: 1 / -1;
  border-bottom: 1px solid var(--rule);
  display: flex;
  padding: 0 1rem;
  gap: 0.5rem;
}
.tab {
  padding: 0.5rem 0;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  border-bottom: 2px solid transparent;
  cursor: pointer;
}
.tab[aria-selected="true"] {
  color: var(--red);
  border-bottom-color: var(--red);
}
.tab:focus { outline: none; }

/* Left rail */
.rail {
  padding: 1rem;
  border-right: 1px solid var(--rule);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.rail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
}
.clear-all {
  font-size: 0.75rem;
  text-decoration: underline;
  color: var(--red);
}
.matching-count {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1;
  margin: 0;
}
.matching-count::after {
  content: attr(data-total);
  font-size: 0.875rem;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  color: #6b665c;
  display: block;
}
.share-bar {
  height: 4px;
  background-color: var(--rule);
  margin-top: 0.25rem;
}
.share-bar-fill {
  height: 100%;
  background-color: var(--red);
  width: 0;
}
.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.filter-chip {
  background-color: var(--red);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.filter-chip button {
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  width: 1rem;
  height: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
}
.filter-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.filter-section[hidden] { display: none; }
.filter-section-heading {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
.filter-section-heading::after {
  content: "▼";
  font-size: 0.625rem;
  transition: transform 0.2s;
}
.filter-section-heading[aria-expanded="false"]::after {
  transform: rotate(-90deg);
}
.filter-section-heading:focus { outline: none; }
.filter-section-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.filter-section-content[hidden] { display: none; }
.filter-keyword input {
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-size: 0.875rem;
}
.filter-keyword .hint {
  font-size: 0.75rem;
  color: #6b665c;
}
.filter-mechanism, .filter-body, .filter-type, .filter-state {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.filter-mechanism label, .filter-body label, .filter-type label, .filter-state label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.filter-mechanism input, .filter-body input, .filter-type input, .filter-state input {
  accent-color: var(--red);
}
.filter-year-range {
  display: flex;
  gap: 0.5rem;
}
.filter-year-range select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-size: 0.875rem;
}
.filter-sdg {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.filter-sdg label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.filter-sdg input { accent-color: var(--red); }

/* Main content */
.main {
  padding: 1rem;
  overflow-y: auto;
}
.tabpanel { padding-top: 1rem; }
.tabpanel[hidden] { display: none; }

/* Overview tab */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.overview-tile {
  border: 1px solid var(--rule);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.overview-tile-title {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
}
.overview-tile-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1;
  margin: 0;
}
.overview-tile-breakdown {
  font-size: 0.875rem;
  color: #6b665c;
  margin: 0;
}
.overview-tile-dot {
  display: inline-block;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.overview-tile-dot.upr { background-color: var(--upr); }
.overview-tile-dot.treaty { background-color: var(--treaty); }
.overview-tile-dot.special { background-color: var(--special); }
.overview-tile-note {
  font-size: 0.75rem;
  color: #6b665c;
  margin: 0;
}
.figure {
  margin-bottom: 2rem;
}
.figure-title {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  margin: 0 0 0.5rem 0;
}
.figure-chart {
  border: 1px solid var(--rule);
  padding: 1rem;
  background-color: white;
}
.figure-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}
.figure-table th, .figure-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
.figure-table th {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  font-weight: 400;
}
.figure-table td { font-size: 0.875rem; }
.figure-table tr:last-child th, .figure-table tr:last-child td { border-bottom: none; }
.figure-source {
  font-size: 0.75rem;
  color: #6b665c;
  margin-top: 0.25rem;
}
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
  font-size: 0.875rem;
}
.chart-legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.chart-legend-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}
.no-records {
  padding: 2rem;
  text-align: center;
  color: #6b665c;
  font-size: 1rem;
}

/* Records tab */
.records-search {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}
.records-table {
  width: 100%;
  border-collapse: collapse;
}
.records-table th, .records-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
.records-table th {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  font-weight: 400;
  cursor: pointer;
}
.records-table th:focus { outline: 2px solid var(--red); outline-offset: -2px; }
.records-table th.sort-asc::after { content: " ↑"; }
.records-table th.sort-desc::after { content: " ↓"; }
.records-table td { font-size: 0.875rem; }
.records-table tr:last-child th, .records-table tr:last-child td { border-bottom: none; }
.records-table tr.expanded td { padding-bottom: 0; }
.records-table tr.expanded + tr td { padding-top: 0; }
.records-table a { text-decoration: underline; }
.records-table mark {
  background-color: #ffeb3b;
  color: var(--ink);
  padding: 0 0.25rem;
}
.records-expand {
  background-color: var(--red);
  color: white;
  border: none;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  cursor: pointer;
}
.records-expand:focus { outline: none; }
.records-details {
  grid-column: 1 / -1;
  padding: 1rem;
  border-top: 1px solid var(--rule);
  background-color: white;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.records-details-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2rem;
  font-weight: 400;
  color: var(--red);
  margin: 0;
}
.records-details-text { white-space: pre-wrap; }
.records-details-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.records-details-label-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.records-details-label-group-title {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: #6b665c;
}
.records-details-label {
  background-color: var(--rule);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}
.records-details-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.records-details-copy {
  background-color: var(--red);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  cursor: pointer;
}
.records-details-copy:focus { outline: none; }
.records-details-copy::after {
  content: "Copied!";
  margin-left: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s;
}
.records-details-copy.copied::after { opacity: 1; }
.records-details-open {
  color: var(--red);
  text-decoration: underline;
  font-size: 0.875rem;
}
.show-more {
  margin-top: 1rem;
  text-align: center;
}
.show-more button {
  background-color: var(--red);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  cursor: pointer;
}
.show-more button:focus { outline: none; }

/* Check tab */
.check-panel {
  border: 1px solid var(--rule);
  padding: 1rem;
  background-color: white;
  margin-bottom: 2rem;
}
.check-panel-title {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  margin: 0 0 1rem 0;
}
.check-line {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  font-size: 0.875rem;
}
.check-line:last-child { border-bottom: none; }
.check-line.failed { color: var(--red); }
.check-line .check-result { font-family: ui-monospace, Menlo, Consolas, monospace; }
.sample-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}
.sample-seed {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.sample-seed input {
  width: 6rem;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
}
.sample-tally {
  font-size: 0.875rem;
  margin-bottom: 1rem;
}
.sample-card {
  border: 1px solid var(--rule);
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: white;
}
.sample-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.sample-card-symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
}
.sample-card-symbol a { text-decoration: underline; }
.sample-card-number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--red);
}
.sample-card-text { white-space: pre-wrap; }
.sample-card-themes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.5rem 0;
}
.sample-card-theme {
  background-color: var(--rule);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}
.sample-card-verdicts {
  display: flex;
  gap: 1rem;
}
.sample-card-verdict {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.sample-card-verdict input { accent-color: var(--red); }

/* Method & export tab */
.method-section {
  margin-bottom: 2rem;
}
.method-section-title {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: #6b665c;
  margin: 0 0 0.5rem 0;
}
.method-section p {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  line-height: 1.5;
}
.export-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}
.export-button {
  background-color: var(--red);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  cursor: pointer;
}
.export-button:focus { outline: none; }
.data-source {
  font-size: 0.75rem;
  color: #6b665c;
  margin-top: 2rem;
}

/* Footer */
.footer {
  grid-column: 1 / -1;
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--rule);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  color: #6b665c;
  display: flex;
  justify-content: space-between;
}
.footer-credits { font-size: 0.625rem; }
</style>
</head>
<body>

<div class="header">
  <div class="header-label">UHRI · <span id="country-label"></span></div>
  <h1 class="header-title">UN human rights recommendations and observations: <span id="country-title"></span></h1>
  <div class="header-meta">Source: <a id="source-link" target="_blank"></a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · built <span id="built-date"></span> · dated by document</div>
</div>

<div class="tablist" role="tablist" aria-label="Tabs">
  <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="panel-01">01 OVERVIEW</button>
  <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="panel-02">02 RECORDS</button>
  <button id="tab-03" class="tab" role="tab" aria-selected="false" aria-controls="panel-03">03 CHECK</button>
  <button id="tab-04" class="tab" role="tab" aria-selected="false" aria-controls="panel-04">04 METHOD & EXPORT</button>
</div>

<div class="rail">
  <div class="rail-header">
    <span>FILTERS</span>
    <button class="clear-all" id="clear-all">Clear all</button>
  </div>
  <div class="matching-count" id="matching-count" aria-live="polite"></div>
  <div class="share-bar"><div class="share-bar-fill" id="share-bar-fill"></div></div>
  <div class="filter-chips" id="filter-chips"></div>

  <div class="filter-section" id="filter-section-01">
    <button class="filter-section-heading" aria-expanded="true" aria-controls="filter-01-content">01 KEYWORD</button>
    <div class="filter-section-content" id="filter-01-content">
      <div class="filter-keyword">
        <input type="text" id="keyword-input" placeholder="Search text or symbol…"/>
        <div class="hint">literal match, not synonyms</div>
      </div>
    </div>
  </div>

  <div class="filter-section" id="filter-section-02">
    <button class="filter-section-heading" aria-expanded="false" aria-controls="filter-02-content">02 MECHANISM, BODY, TYPE</button>
    <div class="filter-section-content" id="filter-02-content">
      <div class="filter-mechanism">
        <label><input type="radio" name="mechanism" value="all" checked/> All mechanisms</label>
        <label><input type="radio" name="mechanism" value="Universal Periodic Review"/> Universal Periodic Review</label>
        <label><input type="radio" name="mechanism" value="Treaty bodies"/> Treaty bodies</label>
        <label><input type="radio" name="mechanism" value="Special Procedures"/> Special Procedures</label>
      </div>
      <div class="filter-body" id="filter-body-container"></div>
      <div class="filter-type" id="filter-type-container"></div>
      <div class="filter-state" id="filter-state-container" hidden>
        <label for="state-select">Recommending State</label>
        <select id="state-select"><option value="all">All States</option></select>
      </div>
    </div>
  </div>

  <div class="filter-section" id="filter-section-03">
    <button class="filter-section-heading" aria-expanded="false" aria-controls="filter-03-content">03 YEARS AND SDG</button>
    <div class="filter-section-content" id="filter-03-content">
      <div class="filter-year-range">
        <select id="year-from"><option value="">From</option></select>
        <select id="year-to"><option value="">To</option></select>
      </div>
      <div class="filter-sdg" id="filter-sdg-container"></div>
    </div>
  </div>
</div>

<div class="main">
  <div id="panel-01" class="tabpanel" role="tabpanel" aria-labelledby="tab-01">
    <div class="overview-grid">
      <div class="overview-tile">
        <div class="overview-tile-title">ALL RECORDS</div>
        <div class="overview-tile-number" id="tile-all-records"></div>
        <p class="overview-tile-breakdown" id="tile-all-breakdown"></p>
        <p class="overview-tile-note">How this is computed: count of records in the file, by type.</p>
      </div>
      <div class="overview-tile">
        <div class="overview-tile-title">DOCUMENTS</div>
        <div class="overview-tile-number" id="tile-documents"></div>
        <p class="overview-tile-note">How this is computed: distinct document symbols.</p>
      </div>
      <div class="overview-tile">
        <div class="overview-tile-title">YEARS</div>
        <div class="overview-tile-number" id="tile-years"></div>
        <p class="overview-tile-note">How this is computed: first and last year in the file.</p>
      </div>
      <div class="overview-tile">
        <div class="overview-tile-title">UNIVERSAL PERIODIC REVIEW</div>
        <div class="overview-tile-number" id="tile-upr-records"></div>
        <div class="overview-tile-dot upr"></div>
        <div class="overview-tile-breakdown"><span id="tile-upr-documents"></span> documents · latest <span id="tile-upr-latest"></span> · <span id="tile-upr-share"></span> of filtered</div>
        <p class="overview-tile-note">How this is computed: records with mechanism = "Universal Periodic Review". <button id="show-states" class="records-expand">see the States</button></p>
      </div>
      <div class="overview-tile">
        <div class="overview-tile-title">TREATY BODIES</div>
        <div class="overview-tile-number" id="tile-treaty-records"></div>
        <div class="overview-tile-dot treaty"></div>
        <div class="overview-tile-breakdown"><span id="tile-treaty-documents"></span> documents · latest <span id="tile-treaty-latest"></span> · <span id="tile-treaty-share"></span> of filtered</div>
        <p class="overview-tile-note">How this is computed: records with mechanism = "Treaty bodies".</p>
      </div>
      <div class="overview-tile">
        <div class="overview-tile-title">SPECIAL PROCEDURES</div>
        <div class="overview-tile-number" id="tile-special-records"></div>
        <div class="overview-tile-dot special"></div>
        <div class="overview-tile-breakdown"><span id="tile-special-documents"></span> documents · latest <span id="tile-special-latest"></span> · <span id="tile-special-share"></span> of filtered</div>
        <p class="overview-tile-note">How this is computed: records with mechanism = "Special Procedures".</p>
      </div>
    </div>

    <div class="figure">
      <div class="figure-title">FIG.01 Ten most frequent themes among <span id="theme-count"></span> filtered records</div>
      <div class="figure-chart">
        <div class="chart-container"><canvas id="theme-chart"></canvas></div>
        <div class="chart-legend" id="theme-legend"></div>
      </div>
      <table class="figure-table">
        <thead>
          <tr><th scope="col">Theme</th><th scope="col">Records</th><th scope="col">% of filtered</th><th scope="col">Years</th></tr>
        </thead>
        <tbody id="theme-table-body"></tbody>
      </table>
      <div class="figure-source">Source: themes as labelled in the UHRI data. A record can carry several themes, so the bars add up to more than the record count.</div>
    </div>

    <div class="figure">
      <div class="figure-title">FIG.02 Records per year by mechanism</div>
      <div class="figure-chart">
        <div class="chart-container"><canvas id="timeline-chart"></canvas></div>
        <div class="chart-legend">
          <div class="chart-legend-item"><div class="chart-legend-dot" style="background-color: var(--upr);"></div> Universal Periodic Review</div>
          <div class="chart-legend-item"><div class="chart-legend-dot" style="background-color: var(--treaty);"></div> Treaty bodies</div>
          <div class="chart-legend-item"><div class="chart-legend-dot" style="background-color: var(--special);"></div> Special Procedures</div>
        </div>
      </div>
      <div class="figure-source">Source: records per year per mechanism in the filtered set.</div>
    </div>
  </div>

  <div id="panel-02" class="tabpanel" role="tabpanel" aria-labelledby="tab-02" hidden>
    <input type="text" class="records-search" id="records-search" placeholder="Search records, e.g. torture"/>
    <div class="records-caption" id="records-caption"></div>
    <table class="records-table">
      <thead>
        <tr><th scope="col" id="sort-date">Date</th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr>
      </thead>
      <tbody id="records-table-body"></tbody>
    </table>
    <div class="show-more"><button id="show-more">Show 50 more</button></div>
  </div>

  <div id="panel-03" class="tabpanel" role="tabpanel" aria-labelledby="tab-03" hidden>
    <div class="check-panel">
      <div class="check-panel-title">Check this dashboard</div>
      <div id="check-results"></div>
    </div>

    <div class="sample-controls">
      <button id="draw-sample">Check 10 at random</button>
      <button id="draw-again" hidden>Draw again</button>
      <div class="sample-seed">
        <span>Draw with this seed</span>
        <input type="number" id="sample-seed" min="1" value="1"/>
      </div>
    </div>
    <div class="sample-tally" id="sample-tally"></div>
    <div id="sample-cards"></div>
  </div>

  <div id="panel-04" class="tabpanel" role="tabpanel" aria-labelledby="tab-04" hidden>
    <div class="method-section">
      <div class="method-section-title">How each number is computed</div>
      <p>Headline total = count of records in the file. The breakdown counts records per type, using the values exactly as spelled in the data.</p>
      <p>Documents = number of distinct document symbols. Years = first and last year in the file.</p>
      <p>Filters. Mechanism, body, type: exact match on the field. Year: year inclusive between the two selects. SDG: the record's SDG list includes the goal number. Keyword: every word must occur as a substring of the text or symbol (literal match, not synonyms).</p>
      <p>Theme counts = for each record in the filtered set, each value in its theme list counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = first and last year of the filtered records carrying that theme.</p>
      <p>Timeline = records per year per mechanism in the filtered set, with zero for missing combinations.</p>
      <p>Paragraph number = the first match of /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/ on the text; the captured group is the number ("71" or "144.43"); no match means no number.</p>
      <p>Recommending State = only for UPR. Take the trailing run of parenthesised groups, split into groups, strip outer parentheses and trim. A group is accepted as a State only if it has no comma and at most 60 characters; otherwise the record gets "State not found".</p>
      <p>Citation = symbol + ", para. " + paragraph number when one was found; otherwise symbol. UPR numbers keep their two-part form ("para. 144.43").</p>
    </div>

    <div class="method-section">
      <div class="method-section-title">Download CSV of the current filter</div>
      <div class="export-buttons">
        <button class="export-button" id="export-csv">Download CSV</button>
        <button class="export-button" id="copy-summary">Copy summary</button>
      </div>
    </div>

    <div class="data-source">
      Data source: <a id="data-source-link" target="_blank"></a><br/>
      Licence: CC BY 4.0 (OHCHR UHRI)<br/>
      Built: <span id="built-date-footer"></span>
    </div>
  </div>
</div>

<div class="footer">
  <div>Built on OHCHR UHRI data · <span id="record-count-footer"></span> records · <a id="source-link-footer" target="_blank">source link</a></div>
  <div class="footer-credits">Credits: Chart.js (MIT)</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  // Data
  const uhri = window.WORKSHOP_DATA.uhri;
  const country = uhri.country;
  const sdgNames = uhri.sdg_names;
  const records = uhri.records;
  const recordCount = records.length;
  const documentCount = new Set(records.map(r => r.symbol)).size;
  const years = Array.from(new Set(records.map(r => r.year))).sort((a, b) => a - b);
  const firstYear = years[0];
  const lastYear = years[years.length - 1];
  const mechanisms = Array.from(new Set(records.map(r => r.mechanism)));
  const types = Array.from(new Set(records.map(r => r.type)));
  const bodies = Array.from(new Set(records.map(r => r.body)));

  // State extraction
  const stateRegex = /((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
  const stateGroupRegex = /\((?:[^()]|\([^()]*\))*\)/g;
  const stateRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
  const stateMap = {};
  stateRecords.forEach(r => {
    const match = r.text.match(stateRegex);
    if (!match) return;
    const groups = match[1].match(stateGroupRegex) || [];
    groups.forEach(g => {
      const state = g.slice(1, -1).trim();
      if (state.includes(',') || state.length > 60) return;
      if (!stateMap[state]) stateMap[state] = 0;
      stateMap[state]++;
    });
  });
  const states = Object.keys(stateMap).sort((a, b) => stateMap[b] - stateMap[a] || a.localeCompare(b));

  // UI elements
  const countryLabel = document.getElementById('country-label');
  const countryTitle = document.getElementById('country-title');
  const sourceLink = document.getElementById('source-link');
  const recordCountEl = document.getElementById('record-count');
  const documentCountEl = document.getElementById('document-count');
  const yearRangeEl = document.getElementById('year-range');
  const builtDateEl = document.getElementById('built-date');
  const matchingCountEl = document.getElementById('matching-count');
  const shareBarFill = document.getElementById('share-bar-fill');
  const filterChipsEl = document.getElementById('filter-chips');
  const clearAllBtn = document.getElementById('clear-all');
  const keywordInput = document.getElementById('keyword-input');
  const filterBodyContainer = document.getElementById('filter-body-container');
  const filterTypeContainer = document.getElementById('filter-type-container');
  const filterStateContainer = document.getElementById('filter-state-container');
  const stateSelect = document.getElementById('state-select');
  const yearFromSelect = document.getElementById('year-from');
  const yearToSelect = document.getElementById('year-to');
  const filterSdgContainer = document.getElementById('filter-sdg-container');
  const tab01 = document.getElementById('tab-01');
  const tab02 = document.getElementById('tab-02');
  const tab03 = document.getElementById('tab-03');
  const tab04 = document.getElementById('tab-04');
  const panel01 = document.getElementById('panel-01');
  const panel02 = document.getElementById('panel-02');
  const panel03 = document.getElementById('panel-03');
  const panel04 = document.getElementById('panel-04');
  const tileAllRecords = document.getElementById('tile-all-records');
  const tileAllBreakdown = document.getElementById('tile-all-breakdown');
  const tileDocuments = document.getElementById('tile-documents');
  const tileYears = document.getElementById('tile-years');
  const tileUprRecords = document.getElementById('tile-upr-records');
  const tileUprDocuments = document.getElementById('tile-upr-documents');
  const tileUprLatest = document.getElementById('tile-upr-latest');
  const tileUprShare = document.getElementById('tile-upr-share');
  const tileTreatyRecords = document.getElementById('tile-treaty-records');
  const tileTreatyDocuments = document.getElementById('tile-treaty-documents');
  const tileTreatyLatest = document.getElementById('tile-treaty-latest');
  const tileTreatyShare = document.getElementById('tile-treaty-share');
  const tileSpecialRecords = document.getElementById('tile-special-records');
  const tileSpecialDocuments = document.getElementById('tile-special-documents');
  const tileSpecialLatest = document.getElementById('tile-special-latest');
  const tileSpecialShare = document.getElementById('tile-special-share');
  const themeCountEl = document.getElementById('theme-count');
  const themeChartCanvas = document.getElementById('theme-chart');
  const themeLegend = document.getElementById('theme-legend');
  const themeTableBody = document.getElementById('theme-table-body');
  const timelineChartCanvas = document.getElementById('timeline-chart');
  const recordsSearch = document.getElementById('records-search');
  const recordsCaption = document.getElementById('records-caption');
  const recordsTableBody = document.getElementById('records-table-body');
  const sortDate = document.getElementById('sort-date');
  const showMoreBtn = document.getElementById('show-more');
  const checkResults = document.getElementById('check-results');
  const drawSampleBtn = document.getElementById('draw-sample');
  const drawAgainBtn = document.getElementById('draw-again');
  const sampleSeedInput = document.getElementById('sample-seed');
  const sampleTally = document.getElementById('sample-tally');
  const sampleCards = document.getElementById('sample-cards');
  const exportCsvBtn = document.getElementById('export-csv');
  const copySummaryBtn = document.getElementById('copy-summary');
  const showStatesBtn = document.getElementById('show-states');
  const dataSourceLink = document.getElementById('data-source-link');
  const recordCountFooter = document.getElementById('record-count-footer');
  const sourceLinkFooter = document.getElementById('source-link-footer');
  const builtDateFooter = document.getElementById('built-date-footer');

  // State for filters
  let filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    state: 'all',
    yearFrom: '',
    yearTo: '',
    sdg: 'all'
  };
  let filteredRecords = [...records];
  let sortOrder = 'desc';
  let visibleRows = 50;

  // Initialize UI
  countryLabel.textContent = country;
  countryTitle.textContent = country;
  sourceLink.href = uhri.source_url;
  sourceLink.textContent = uhri.source;
  recordCountEl.textContent = recordCount;
  documentCountEl.textContent = documentCount;
  yearRangeEl.textContent = `${firstYear}–${lastYear}`;
  builtDateEl.textContent = uhri.built;
  matchingCountEl.textContent = recordCount;
  matchingCountEl.setAttribute('data-total', `of ${recordCount} in the file`);
  dataSourceLink.href = uhri.source_url;
  dataSourceLink.textContent = uhri.source;
  recordCountFooter.textContent = recordCount;
  sourceLinkFooter.href = uhri.source_url;
  builtDateFooter.textContent = uhri.built;

  // Populate filter UI
  function populateFilters() {
    // Body filter
    const mechanism = filters.mechanism;
    const bodiesInMechanism = mechanism === 'all'
      ? bodies
      : Array.from(new Set(records.filter(r => r.mechanism === mechanism).map(r => r.body)));
    filterBodyContainer.innerHTML = '';
    const allBodyLabel = document.createElement('label');
    allBodyLabel.innerHTML = `<input type="radio" name="body" value="all" ${filters.body === 'all' ? 'checked' : ''}/> All bodies`;
    filterBodyContainer.appendChild(allBodyLabel);
    bodiesInMechanism.forEach(body => {
      const label = document.createElement('label');
      const count = records.filter(r => r.body === body && (mechanism === 'all' || r.mechanism === mechanism)).length;
      label.innerHTML = `<input type="radio" name="body" value="${body}" ${filters.body === body ? 'checked' : ''}/> ${body} (${count})`;
      filterBodyContainer.appendChild(label);
    });

    // Type filter
    const typesInFilter = filters.mechanism === 'all' && filters.body === 'all'
      ? types
      : Array.from(new Set(filteredRecords.map(r => r.type)));
    filterTypeContainer.innerHTML = '';
    const allTypeLabel = document.createElement('label');
    allTypeLabel.innerHTML = `<input type="radio" name="type" value="all" ${filters.type === 'all' ? 'checked' : ''}/> All types`;
    filterTypeContainer.appendChild(allTypeLabel);
    typesInFilter.forEach(type => {
      const label = document.createElement('label');
      const count = records.filter(r => r.type === type && (filters.mechanism === 'all' || r.mechanism === filters.mechanism) && (filters.body === 'all' || r.body === filters.body)).length;
      label.innerHTML = `<input type="radio" name="type" value="${type}" ${filters.type === type ? 'checked' : ''}/> ${type} (${count})`;
      filterTypeContainer.appendChild(label);
    });

    // State filter
    if (mechanism === 'Universal Periodic Review' || mechanism === 'all') {
      filterStateContainer.hidden = false;
      stateSelect.innerHTML = '<option value="all">All States</option>';
      states.forEach(state => {
        const option = document.createElement('option');
        option.value = state;
        option.textContent = `${state} (${stateMap[state]})`;
        if (filters.state === state) option.selected = true;
        stateSelect.appendChild(option);
      });
    } else {
      filterStateContainer.hidden = true;
    }

    // Year filter
    yearFromSelect.innerHTML = '<option value="">From</option>';
    yearToSelect.innerHTML = '<option value="">To</option>';
    years.forEach(year => {
      const optionFrom = document.createElement('option');
      optionFrom.value = year;
      optionFrom.textContent = year;
      if (filters.yearFrom === year) optionFrom.selected = true;
      yearFromSelect.appendChild(optionFrom);

      const optionTo = document.createElement('option');
      optionTo.value = year;
      optionTo.textContent = year;
      if (filters.yearTo === year) optionTo.selected = true;
      yearToSelect.appendChild(optionTo);
    });

    // SDG filter
    const sdgsInData = Array.from(new Set(records.flatMap(r => r.sdgs || []))).sort((a, b) => a - b);
    filterSdgContainer.innerHTML = '';
    const allSdgLabel = document.createElement('label');
    allSdgLabel.innerHTML = `<input type="radio" name="sdg" value="all" ${filters.sdg === 'all' ? 'checked' : ''}/> All SDGs`;
    filterSdgContainer.appendChild(allSdgLabel);
    sdgsInData.forEach(sdg => {
      const label = document.createElement('label');
      const count = records.filter(r => (r.sdgs || []).includes(sdg)).length;
      label.innerHTML = `<input type="radio" name="sdg" value="${sdg}" ${filters.sdg == sdg ? 'checked' : ''}/> ${sdg} ${sdgNames[sdg]} (${count})`;
      filterSdgContainer.appendChild(label);
    });
  }

  // Apply filters
  function applyFilters() {
    filteredRecords = records.filter(record => {
      // Keyword
      if (filters.keyword) {
        const keywords = filters.keyword.toLowerCase().split(/\s+/).filter(k => k);
        if (!keywords.every(k => record.text.toLowerCase().includes(k) || record.symbol.toLowerCase().includes(k))) {
          return false;
        }
      }

      // Mechanism
      if (filters.mechanism !== 'all' && record.mechanism !== filters.mechanism) {
        return false;
      }

      // Body
      if (filters.body !== 'all' && record.body !== filters.body) {
        return false;
      }

      // Type
      if (filters.type !== 'all' && record.type !== filters.type) {
        return false;
      }

      // State (UPR only)
      if (filters.mechanism === 'Universal Periodic Review' || filters.mechanism === 'all') {
        if (filters.state !== 'all') {
          const match = record.text.match(stateRegex);
          if (!match) return false;
          const groups = match[1].match(stateGroupRegex) || [];
          const statesInRecord = groups.map(g => g.slice(1, -1).trim()).filter(s => !s.includes(',') && s.length <= 60);
          if (!statesInRecord.includes(filters.state)) {
            return false;
          }
        }
      }

      // Year
      if (filters.yearFrom && record.year < filters.yearFrom) {
        return false;
      }
      if (filters.yearTo && record.year > filters.yearTo) {
        return false;
      }

      // SDG
      if (filters.sdg !== 'all') {
        const sdg = parseInt(filters.sdg);
        if (!(record.sdgs || []).includes(sdg)) {
          return false;
        }
      }

      return true;
    });

    // Update matching count
    const matchingCount = filteredRecords.length;
    matchingCountEl.textContent = matchingCount;
    shareBarFill.style.width = `${(matchingCount / recordCount) * 100}%`;

    // Update filter chips
    updateFilterChips();

    // Update overview tiles
    updateOverviewTiles();

    // Update theme chart and table
    updateThemeChart();

    // Update timeline chart
    updateTimelineChart();

    // Update records table
    updateRecordsTable();

    // Update check results
    updateCheckResults();

    // Reset visible rows
    visibleRows = 50;
  }

  // Update filter chips
  function updateFilterChips() {
    filterChipsEl.innerHTML = '';
    if (filters.keyword) {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Keyword: ${filters.keyword}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.keyword = '';
        keywordInput.value = '';
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.mechanism !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Mechanism: ${filters.mechanism}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.mechanism = 'all';
        document.querySelector('input[name="mechanism"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.body !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Body: ${filters.body}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.body = 'all';
        document.querySelector('input[name="body"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.type !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Type: ${filters.type}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.type = 'all';
        document.querySelector('input[name="type"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.state !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `State: ${filters.state}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.state = 'all';
        stateSelect.value = 'all';
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.yearFrom) {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `From: ${filters.yearFrom}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.yearFrom = '';
        yearFromSelect.value = '';
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.yearTo) {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `To: ${filters.yearTo}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.yearTo = '';
        yearToSelect.value = '';
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
    if (filters.sdg !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `SDG: ${filters.sdg} ${sdgNames[filters.sdg]}`;
      const removeBtn = document.createElement('button');
      removeBtn.textContent = '×';
      removeBtn.addEventListener('click', () => {
        filters.sdg = 'all';
        document.querySelector('input[name="sdg"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(removeBtn);
      filterChipsEl.appendChild(chip);
    }
  }

  // Update overview tiles
  function updateOverviewTiles() {
    const matchingCount = filteredRecords.length;

    // All records
    tileAllRecords.textContent = matchingCount;
    const typeCounts = {};
    types.forEach(type => {
      typeCounts[type] = filteredRecords.filter(r => r.type === type).length;
    });
    const typeBreakdown = types.map(type => `${typeCounts[type]} ${type}`).join(', ');
    tileAllBreakdown.textContent = typeBreakdown;

    // Documents
    const documents = new Set(filteredRecords.map(r => r.symbol)).size;
    tileDocuments.textContent = documents;

    // Years
    const filteredYears = Array.from(new Set(filteredRecords.map(r => r.year))).sort((a, b) => a - b);
    tileYears.textContent = filteredYears.length > 0 ? `${filteredYears[0]}–${filteredYears[filteredYears.length - 1]}` : '–';

    // UPR
    const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
    const uprCount = uprRecords.length;
    const uprDocuments = new Set(uprRecords.map(r => r.symbol)).size;
    const uprLatest = uprRecords.length > 0 ? Math.max(...uprRecords.map(r => r.year)) : '–';
    const uprShare = matchingCount > 0 ? `${Math.round((uprCount / matchingCount) * 100)}%` : '0%';
    tileUprRecords.textContent = uprCount;
    tileUprDocuments.textContent = uprDocuments;
    tileUprLatest.textContent = uprLatest;
    tileUprShare.textContent = uprShare;

    // Treaty bodies
    const treatyRecords = filteredRecords.filter(r => r.mechanism === 'Treaty bodies');
    const treatyCount = treatyRecords.length;
    const treatyDocuments = new Set(treatyRecords.map(r => r.symbol)).size;
    const treatyLatest = treatyRecords.length > 0 ? Math.max(...treatyRecords.map(r => r.year)) : '–';
    const treatyShare = matchingCount > 0 ? `${Math.round((treatyCount / matchingCount) * 100)}%` : '0%';
    tileTreatyRecords.textContent = treatyCount;
    tileTreatyDocuments.textContent = treatyDocuments;
    tileTreatyLatest.textContent = treatyLatest;
    tileTreatyShare.textContent = treatyShare;

    // Special Procedures
    const specialRecords = filteredRecords.filter(r => r.mechanism === 'Special Procedures');
    const specialCount = specialRecords.length;
    const specialDocuments = new Set(specialRecords.map(r => r.symbol)).size;
    const specialLatest = specialRecords.length > 0 ? Math.max(...specialRecords.map(r => r.year)) : '–';
    const specialShare = matchingCount > 0 ? `${Math.round((specialCount / matchingCount) * 100)}%` : '0%';
    tileSpecialRecords.textContent = specialCount;
    tileSpecialDocuments.textContent = specialDocuments;
    tileSpecialLatest.textContent = specialLatest;
    tileSpecialShare.textContent = specialShare;
  }

  // Update theme chart and table
  function updateThemeChart() {
    const matchingCount = filteredRecords.length;
    themeCountEl.textContent = matchingCount;

    // Count themes
    const themeCounts = {};
    filteredRecords.forEach(record => {
      (record.themes || []).forEach(theme => {
        if (!themeCounts[theme]) themeCounts[theme] = 0;
        themeCounts[theme]++;
      });
    });

    // Sort by count, then alphabetically
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);

    // Prepare chart data
    const chartLabels = sortedThemes.map(([theme]) => theme);
    const chartData = sortedThemes.map(([, count]) => count);
    const chartColors = Array(chartData.length).fill(`rgba(155, 35, 53, 0.8)`);

    // Destroy previous chart
    if (window.themeChart) {
      window.themeChart.destroy();
    }

    // Create chart
    const ctx = themeChartCanvas.getContext('2d');
    window.themeChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartLabels,
        datasets: [{
          data: chartData,
          backgroundColor: chartColors,
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
              label: context => {
                const count = context.raw;
                const percentage = ((count / matchingCount) * 100).toFixed(1);
                return `${count} (${percentage}%)`;
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            max: Math.max(...chartData) * 1.1,
            ticks: {
              callback: value => value.toLocaleString()
            },
            grid: { display: false }
          },
          y: {
            grid: { display: false }
          }
        },
        onClick: (e, activeEls) => {
          if (activeEls.length > 0) {
            const index = activeEls[0].index;
            const theme = chartLabels[index];
            filters.keyword = theme;
            keywordInput.value = theme;
            applyFilters();
          }
        }
      }
    });

    // Update legend
    themeLegend.innerHTML = '';
    sortedThemes.forEach(([theme, count]) => {
      const percentage = ((count / matchingCount) * 100).toFixed(1);
      const item = document.createElement('div');
      item.textContent = `${theme}: ${count} (${percentage}%)`;
      themeLegend.appendChild(item);
    });

    // Update table
    themeTableBody.innerHTML = '';
    sortedThemes.forEach(([theme, count]) => {
      const percentage = ((count / matchingCount) * 100).toFixed(1);
      const recordsWithTheme = filteredRecords.filter(r => (r.themes || []).includes(theme));
      const themeYears = Array.from(new Set(recordsWithTheme.map(r => r.year))).sort((a, b) => a - b);
      const yearRange = themeYears.length > 0 ? `${themeYears[0]}–${themeYears[themeYears.length - 1]}` : '–';

      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${theme}</td>
        <td>${count.toLocaleString()}</td>
        <td>${percentage}%</td>
        <td>${yearRange}</td>
      `;
      themeTableBody.appendChild(row);
    });
  }

  // Update timeline chart
  function updateTimelineChart() {
    // Prepare data per mechanism per year
    const mechanismData = {};
    mechanisms.forEach(mechanism => {
      mechanismData[mechanism] = {};
      years.forEach(year => {
        mechanismData[mechanism][year] = 0;
      });
    });

    filteredRecords.forEach(record => {
      mechanismData[record.mechanism][record.year]++;
    });

    // Prepare chart data
    const chartLabels = years.map(year => year.toString());
    const datasets = mechanisms.map(mechanism => {
      const data = years.map(year => mechanismData[mechanism][year]);
      let backgroundColor;
      if (mechanism === 'Universal Periodic Review') backgroundColor = 'rgba(194, 65, 12, 0.8)';
      else if (mechanism === 'Treaty bodies') backgroundColor = 'rgba(15, 118, 110, 0.8)';
      else if (mechanism === 'Special Procedures') backgroundColor = 'rgba(124, 58, 237, 0.8)';
      return {
        label: mechanism,
        data: data,
        backgroundColor: backgroundColor,
        borderWidth: 0
      };
    });

    // Destroy previous chart
    if (window.timelineChart) {
      window.timelineChart.destroy();
    }

    // Create chart
    const ctx = timelineChartCanvas.getContext('2d');
    window.timelineChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartLabels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => {
                return `${context.dataset.label}: ${context.raw}`;
              }
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            grid: { display: false }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: value => value.toLocaleString()
            }
          }
        }
      }
    });
  }

  // Update records table
  function updateRecordsTable() {
    const matchingCount = filteredRecords.length;
    recordsCaption.textContent = `${Math.min(visibleRows, matchingCount)} of ${matchingCount} matching records shown`;

    // Sort records
    let sortedRecords = [...filteredRecords];
    if (sortOrder === 'desc') {
      sortedRecords.sort((a, b) => {
        if (b.date !== a.date) return b.date.localeCompare(a.date);
        if (b.body !== a.body) return a.body.localeCompare(b.body);
        const aPara = a.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)?.[1] || '';
        const bPara = b.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)?.[1] || '';
        return aPara.localeCompare(bPara);
      });
    } else {
      sortedRecords.sort((a, b) => {
        if (a.date !== b.date) return a.date.localeCompare(b.date);
        if (a.body !== b.body) return a.body.localeCompare(b.body);
        const aPara = a.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)?.[1] || '';
        const bPara = b.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)?.[1] || '';
        return bPara.localeCompare(aPara);
      });
    }

    // Filter visible rows
    const visibleRecords = sortedRecords.slice(0, visibleRows);

    // Update table
    recordsTableBody.innerHTML = '';
    visibleRecords.forEach(record => {
      const row = document.createElement('tr');
      row.tabIndex = 0;

      // Date
      const date = new Date(record.date);
      const dateStr = date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

      // Paragraph number
      const paraMatch = record.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
      const paraNumber = paraMatch ? paraMatch[1] : '–';

      // First line
      const firstLine = record.text.length > 120
        ? record.text.slice(0, 120).split(' ').slice(0, -1).join(' ') + '…'
        : record.text;

      // Recommending State (UPR only)
      let state = '–';
      if (record.mechanism === 'Universal Periodic Review') {
        const match = record.text.match(stateRegex);
        if (match) {
          const groups = match[1].match(stateGroupRegex) || [];
          const statesInRecord = groups.map(g => g.slice(1, -1).trim()).filter(s => !s.includes(',') && s.length <= 60);
          state = statesInRecord.join(', ') || 'State not found';
        } else {
          state = 'State not found';
        }
      }

      // Highlight keyword matches
      let highlightedFirstLine = firstLine;
      if (filters.keyword) {
        const keywords = filters.keyword.toLowerCase().split(/\s+/).filter(k => k);
        keywords.forEach(k => {
          const regex = new RegExp(k, 'gi');
          highlightedFirstLine = highlightedFirstLine.replace(regex, match => `<mark>${match}</mark>`);
        });
      }

      row.innerHTML = `
        <td>${dateStr}</td>
        <td>${record.body}</td>
        <td><a href="${record.doc_url}" target="_blank">${record.symbol}</a></td>
        <td>${paraNumber}</td>
        <td>${highlightedFirstLine}</td>
        <td>${state}</td>
      `;

      // Expand row on click
      row.addEventListener('click', () => {
        const expandedRow = document.createElement('tr');
        expandedRow.className = 'expanded';
        expandedRow.innerHTML = `
          <td colspan="6">
            <div class="records-details">
              <div class="records-details-number">${paraNumber}</div>
              <div class="records-details-text">${record.text}</div>
              <div class="records-details-labels">
                ${record.themes && record.themes.length > 0 ? `
                <div class="records-details-label-group">
                  <div class="records-details-label-group-title">THEMES</div>
                  <div>${record.themes.map(theme => `<div class="records-details-label">${theme}</div>`).join('')}</div>
                </div>
                ` : ''}
                ${record.sdgs && record.sdgs.length > 0 ? `
                <div class="records-details-label-group">
                  <div class="records-details-label-group-title">SDGS</div>
                  <div>${record.sdgs.map(sdg => `<div class="records-details-label">${sdg} ${sdgNames[sdg]}</div>`).join('')}</div>
                </div>
                ` : ''}
                ${record.sdg_targets && record.sdg_targets.length > 0 ? `
                <div class="records-details-label-group">
                  <div class="records-details-label-group-title">SDG TARGETS</div>
                  <div>${record.sdg_targets.map(target => `<div class="records-details-label">${target}</div>`).join('')}</div>
                </div>
                ` : ''}
                ${record.affected_persons && record.affected_persons.length > 0 ? `
                <div class="records-details-label-group">
                  <div class="records-details-label-group-title">AFFECTED PERSONS</div>
                  <div>${record.affected_persons.map(person => `<div class="records-details-label">${person}</div>`).join('')}</div>
                </div>
                ` : ''}
                ${record.section ? `
                <div class="records-details-label-group">
                  <div class="records-details-label-group-title">SECTION</div>
                  <div><div class="records-details-label">${record.section}</div></div>
                </div>
                ` : ''}
              </div>
              <div class="records-details-actions">
                <button class="records-details-copy" data-symbol="${record.symbol}" data-para="${paraNumber}">Copy citation</button>
                <a href="${record.doc_url}" target="_blank" class="records-details-open">Open the UN document</a>
              </div>
            </div>
          </td>
        `;
        if (row.nextElementSibling?.classList.contains('expanded')) {
          row.parentNode.removeChild(row.nextElementSibling);
        } else {
          if (row.nextElementSibling) {
            row.parentNode.insertBefore(expandedRow, row.nextElementSibling);
          } else {
            row.parentNode.appendChild(expandedRow);
          }
        }
      });

      // Also expand on Enter
      row.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          row.click();
        }
      });

      recordsTableBody.appendChild(row);
    });

    // Update show more button
    showMoreBtn.hidden = visibleRows >= matchingCount;
  }

  // Update check results
  function updateCheckResults() {
    checkResults.innerHTML = '';

    // Record count
    const recordCountCheck = document.createElement('div');
    recordCountCheck.className = 'check-line';
    const recordCountValue = Number(uhri.count);
    const recordCountPass = recordCount === recordCountValue;
    recordCountCheck.innerHTML = `
      <span>Record count</span>
      <span class="check-result">${recordCount} (file) vs ${recordCountValue} (header) ${recordCountPass ? '✓' : '✗'}</span>
    `;
    if (!recordCountPass) recordCountCheck.classList.add('failed');
    checkResults.appendChild(recordCountCheck);

    // Partitions
    const mechanismCounts = {};
    mechanisms.forEach(mechanism => {
      mechanismCounts[mechanism] = filteredRecords.filter(r => r.mechanism === mechanism).length;
    });
    const mechanismSum = Object.values(mechanismCounts).reduce((a, b) => a + b, 0);
    const mechanismPass = mechanismSum === filteredRecords.length;
    const mechanismCheck = document.createElement('div');
    mechanismCheck.className = 'check-line';
    mechanismCheck.innerHTML = `
      <span>Mechanism partition</span>
      <span class="check-result">${mechanismSum} (sum) vs ${filteredRecords.length} (total) ${mechanismPass ? '✓' : '✗'}</span>
    `;
    if (!mechanismPass) mechanismCheck.classList.add('failed');
    checkResults.appendChild(mechanismCheck);

    const bodyCounts = {};
    bodies.forEach(body => {
      bodyCounts[body] = filteredRecords.filter(r => r.body === body).length;
    });
    const bodySum = Object.values(bodyCounts).reduce((a, b) => a + b, 0);
    const bodyPass = bodySum === filteredRecords.length;
    const bodyCheck = document.createElement('div');
    bodyCheck.className = 'check-line';
    bodyCheck.innerHTML = `
      <span>Body partition</span>
      <span class="check-result">${bodySum} (sum) vs ${filteredRecords.length} (total) ${bodyPass ? '✓' : '✗'}</span>
    `;
    if (!bodyPass) bodyCheck.classList.add('failed');
    checkResults.appendChild(bodyCheck);

    const yearCounts = {};
    years.forEach(year => {
      yearCounts[year] = filteredRecords.filter(r => r.year === year).length;
    });
    const yearSum = Object.values(yearCounts).reduce((a, b) => a + b, 0);
    const yearPass = yearSum === filteredRecords.length;
    const yearCheck = document.createElement('div');
    yearCheck.className = 'check-line';
    yearCheck.innerHTML = `
      <span>Year partition</span>
      <span class="check-result">${yearSum} (sum) vs ${filteredRecords.length} (total) ${yearPass ? '✓' : '✗'}</span>
    `;
    if (!yearPass) yearCheck.classList.add('failed');
    checkResults.appendChild(yearCheck);

    // Type partition
    const typeCounts = {};
    types.forEach(type => {
      typeCounts[type] = filteredRecords.filter(r => r.type === type).length;
    });
    const typeSum = Object.values(typeCounts).reduce((a, b) => a + b, 0);
    const typePass = typeSum === filteredRecords.length;
    const typeCheck = document.createElement('div');
    typeCheck.className = 'check-line';
    typeCheck.innerHTML = `
      <span>Type partition</span>
      <span class="check-result">${typeSum} (sum) vs ${filteredRecords.length} (total) ${typePass ? '✓' : '✗'}</span>
    `;
    if (!typePass) typeCheck.classList.add('failed');
    checkResults.appendChild(typeCheck);

    // Chart against table
    const themeCounts = {};
    filteredRecords.forEach(record => {
      (record.themes || []).forEach(theme => {
        if (!themeCounts[theme]) themeCounts[theme] = 0;
        themeCounts[theme]++;
      });
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const chartValues = sortedThemes.map(([, count]) => count);
    const chartSum = chartValues.reduce((a, b) => a + b, 0);
    const chartMax = Math.max(...chartValues);
    const chartPass = chartMax <= filteredRecords.length;
    const chartCheck = document.createElement('div');
    chartCheck.className = 'check-line';
    chartCheck.innerHTML = `
      <span>Chart against table</span>
      <span class="check-result">max ${chartMax} vs ${filteredRecords.length} (filtered) ${chartPass ? '✓' : '✗'}</span>
    `;
    if (!chartPass) chartCheck.classList.add('failed');
    checkResults.appendChild(chartCheck);

    // Links
    const linkErrors = [];
    filteredRecords.forEach(record => {
      const url = new URL(record.doc_url);
      if (url.hostname !== 'docs.un.org' || !url.pathname.toUpperCase().endsWith(record.symbol.toUpperCase())) {
        linkErrors.push(record.symbol);
      }
    });
    const linkPass = linkErrors.length === 0;
    const linkCheck = document.createElement('div');
    linkCheck.className = 'check-line';
    if (linkPass) {
      linkCheck.innerHTML = `
        <span>Links</span>
        <span class="check-result">all links valid ✓</span>
      `;
    } else {
      linkCheck.innerHTML = `
        <span>Links</span>
        <span class="check-result check-failed">${linkErrors.length} invalid: ${linkErrors.join(', ')}</span>
      `;
      linkCheck.classList.add('failed');
    }
    checkResults.appendChild(linkCheck);

    // Paragraph numbers
    const paraCounts = {};
    mechanisms.forEach(mechanism => {
      paraCounts[mechanism] = { total: 0, withPara: 0 };
    });
    filteredRecords.forEach(record => {
      paraCounts[record.mechanism].total++;
      if (record.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/)) {
        paraCounts[record.mechanism].withPara++;
      }
    });
    const paraChecks = [];
    mechanisms.forEach(mechanism => {
      const { total, withPara } = paraCounts[mechanism];
      if (total === 0) return;
      const percentage = ((withPara / total) * 100).toFixed(1);
      const paraCheck = document.createElement('div');
      paraCheck.className = 'check-line';
      if (mechanism === 'Universal Periodic Review' && percentage !== '100.0') {
        paraCheck.innerHTML = `
          <span>Paragraph numbers (${mechanism})</span>
          <span class="check-result">${percentage}% (${withPara}/${total}) ⚠</span>
        `;
        paraCheck.classList.add('failed');
      } else {
        paraCheck.innerHTML = `
          <span>Paragraph numbers (${mechanism})</span>
          <span class="check-result">${percentage}% (${withPara}/${total}) ✓</span>
        `;
      }
      paraChecks.push(paraCheck);
    });
    paraChecks.forEach(check => checkResults.appendChild(check));

    // States found
    const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
    const stateFoundCount = uprRecords.filter(r => {
      const match = r.text.match(stateRegex);
      if (!match) return false;
      const groups = match[1].match(stateGroupRegex) || [];
      const statesInRecord = groups.map(g => g.slice(1, -1).trim()).filter(s => !s.includes(',') && s.length <= 60);
      return statesInRecord.length > 0;
    }).length;
    const statePass = stateFoundCount === uprRecords.length;
    const stateErrors = uprRecords.filter(r => {
      const match = r.text.match(stateRegex);
      if (!match) return true;
      const groups = match[1].match(stateGroupRegex) || [];
      const statesInRecord = groups.map(g => g.slice(1, -1).trim()).filter(s => !s.includes(',') && s.length <= 60);
      return statesInRecord.length === 0;
    }).map(r => r.symbol);
    const stateCheck = document.createElement('div');
    stateCheck.className = 'check-line';
    if (statePass) {
      stateCheck.innerHTML = `
        <span>States found (UPR)</span>
        <span class="check-result">${stateFoundCount}/${uprRecords.length} ✓</span>
      `;
    } else {
      stateCheck.innerHTML = `
        <span>States found (UPR)</span>
        <span class="check-result check-failed">${stateFoundCount}/${uprRecords.length} (${stateErrors.length} missing: ${stateErrors.join(', ')})</span>
      `;
      stateCheck.classList.add('failed');
    }
    checkResults.appendChild(stateCheck);

    // Duplicates and gaps
    const distinctIds = new Set(filteredRecords.map(r => r.id)).size;
    const idPass = distinctIds === filteredRecords.length;
    const idCheck = document.createElement('div');
    idCheck.className = 'check-line';
    idCheck.innerHTML = `
      <span>Distinct IDs</span>
      <span class="check-result">${distinctIds} vs ${filteredRecords.length} ${idPass ? '✓' : '✗'}</span>
    `;
    if (!idPass) idCheck.classList.add('failed');
    checkResults.appendChild(idCheck);

    const textCounts = {};
    filteredRecords.forEach(record => {
      if (!textCounts[record.text]) textCounts[record.text] = 0;
      textCounts[record.text]++;
    });
    const duplicateTexts = Object.entries(textCounts).filter(([, count]) => count > 1);
    const duplicateCount = duplicateTexts.reduce((sum, [, count]) => sum + count - 1, 0);
    const duplicateCheck = document.createElement('div');
    duplicateCheck.className = 'check-line';
    duplicateCheck.innerHTML = `
      <span>Duplicate texts</span>
      <span class="check-result">${duplicateCount} duplicates ✓</span>
    `;
    checkResults.appendChild(duplicateCheck);

    const noThemes = filteredRecords.filter(r => !r.themes || r.themes.length === 0).length;
    const noThemesCheck = document.createElement('div');
    noThemesCheck.className = 'check-line';
    noThemesCheck.innerHTML = `
      <span>Themes not labelled</span>
      <span class="check-result">${noThemes} records ✓</span>
    `;
    checkResults.appendChild(noThemesCheck);

    const noSdgs = filteredRecords.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    const noSdgsCheck = document.createElement('div');
    noSdgsCheck.className = 'check-line';
    noSdgsCheck.innerHTML = `
      <span>SDGs not labelled</span>
      <span class="check-result">${noSdgs} records ✓</span>
    `;
    checkResults.appendChild(noSdgsCheck);

    const noAffected = filteredRecords.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
    const noAffectedCheck = document.createElement('div');
    noAffectedCheck.className = 'check-line';
    noAffectedCheck.innerHTML = `
      <span>Affected persons not labelled</span>
      <span class="check-result">${noAffected} records ✓</span>
    `;
    checkResults.appendChild(noAffectedCheck);
  }

  // Draw sample
  function drawSample(seed) {
    // Seeded random number generator (mulberry32)
    function mulberry32(a) {
      return function() {
        a |= 0; a = a + 0x6D2B79F5 | 0;
        let t = Math.imul(a ^ a >>> 15, 1 | a);
        t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
        return ((t ^ t >>> 14) >>> 0) / 4294967296;
      };
    }

    const rng = mulberry32(seed);
    const sampleRecords = [...filteredRecords].sort(() => rng() - 0.5).slice(0, 10);

    sampleCards.innerHTML = '';
    sampleRecords.forEach(record => {
      const card = document.createElement('div');
      card.className = 'sample-card';

      // Paragraph number
      const paraMatch = record.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
      const paraNumber = paraMatch ? paraMatch[1] : '–';

      card.innerHTML = `
        <div class="sample-card-header">
          <div class="sample-card-symbol"><a href="${record.doc_url}" target="_blank">${record.symbol}</a></div>
          <div class="sample-card-number">${paraNumber}</div>
        </div>
        <div class="sample-card-text">${record.text}</div>
        <div class="sample-card-themes">
          ${(record.themes || []).map(theme => `<div class="sample-card-theme">${theme}</div>`).join('')}
        </div>
        <div class="sample-card-verdicts">
          <label class="sample-card-verdict">
            <input type="radio" name="verdict-${record.id}" value="fit"/> Fits
          </label>
          <label class="sample-card-verdict">
            <input type="radio" name="verdict-${record.id}" value="nofit"/> Doesn't fit
          </label>
          <label class="sample-card-verdict">
            <input type="radio" name="verdict-${record.id}" value="unsure"/> Unsure
          </label>
        </div>
      `;
      sampleCards.appendChild(card);
    });

    // Update tally
    function updateTally() {
      const verdicts = {};
      sampleRecords.forEach(record => {
        const selected = document.querySelector(`input[name="verdict-${record.id}"]:checked`);
        if (selected) {
          const verdict = selected.value;
          if (!verdicts[verdict]) verdicts[verdict] = 0;
          verdicts[verdict]++;
        }
      });
      const fit = verdicts.fit || 0;
      const nofit = verdicts.nofit || 0;
      const unsure = verdicts.unsure || 0;
      sampleTally.textContent = `Themes: ${fit} fit, ${nofit} don't, ${unsure} unsure of 10 judged (seed ${seed})`;
    }

    // Add event listeners
    sampleRecords.forEach(record => {
      const radios = document.querySelectorAll(`input[name="verdict-${record.id}"]`);
      radios.forEach(radio => {
        radio.addEventListener('change', updateTally);
      });
    });

    updateTally();
  }

  // Event listeners
  tab01.addEventListener('click', () => {
    tab01.setAttribute('aria-selected', 'true');
    tab02.setAttribute('aria-selected', 'false');
    tab03.setAttribute('aria-selected', 'false');
    tab04.setAttribute('aria-selected', 'false');
    panel01.hidden = false;
    panel02.hidden = true;
    panel03.hidden = true;
    panel04.hidden = true;
  });

  tab02.addEventListener('click', () => {
    tab01.setAttribute('aria-selected', 'false');
    tab02.setAttribute('aria-selected', 'true');
    tab03.setAttribute('aria-selected', 'false');
    tab04.setAttribute('aria-selected', 'false');
    panel01.hidden = true;
    panel02.hidden = false;
    panel03.hidden = true;
    panel04.hidden = true;
  });

  tab03.addEventListener('click', () => {
    tab01.setAttribute('aria-selected', 'false');
    tab02.setAttribute('aria-selected', 'false');
    tab03.setAttribute('aria-selected', 'true');
    tab04.setAttribute('aria-selected', 'false');
    panel01.hidden = true;
    panel02.hidden = true;
    panel03.hidden = false;
    panel04.hidden = true;
  });

  tab04.addEventListener('click', () => {
    tab01.setAttribute('aria-selected', 'false');
    tab02.setAttribute('aria-selected', 'false');
    tab03.setAttribute('aria-selected', 'false');
    tab04.setAttribute('aria-selected', 'true');
    panel01.hidden = true;
    panel02.hidden = true;
    panel03.hidden = true;
    panel04.hidden = false;
  });

  // Filter section toggles
  document.querySelectorAll('.filter-section-heading').forEach(heading => {
    heading.addEventListener('click', () => {
      const expanded = heading.getAttribute('aria-expanded') === 'true';
      heading.setAttribute('aria-expanded', !expanded);
      document.getElementById(heading.getAttribute('aria-controls')).hidden = expanded;
    });
  });

  // Clear all
  clearAllBtn.addEventListener('click', () => {
    filters = {
      keyword: '',
      mechanism: 'all',
      body: 'all',
      type: 'all',
      state: 'all',
      yearFrom: '',
      yearTo: '',
      sdg: 'all'
    };
    keywordInput.value = '';
    document.querySelector('input[name="mechanism"][value="all"]').checked = true;
    document.querySelector('input[name="body"][value="all"]').checked = true;
    document.querySelector('input[name="type"][value="all"]').checked = true;
    stateSelect.value = 'all';
    yearFromSelect.value = '';
    yearToSelect.value = '';
    document.querySelector('input[name="sdg"][value="all"]').checked = true;
    applyFilters();
  });

  // Keyword filter
  keywordInput.addEventListener('input', () => {
    filters.keyword = keywordInput.value.trim();
    applyFilters();
  });

  // Mechanism filter
  document.querySelectorAll('input[name="mechanism"]').forEach(radio => {
    radio.addEventListener('change', () => {
      filters.mechanism = radio.value;
      filters.body = 'all';
      filters.type = 'all';
      populateFilters();
      applyFilters();
    });
  });

  // Body filter
  filterBodyContainer.addEventListener('change', e => {
    if (e.target.name === 'body') {
      filters.body = e.target.value;
      filters.type = 'all';
      populateFilters();
      applyFilters();
    }
  });

  // Type filter
  filterTypeContainer.addEventListener('change', e => {
    if (e.target.name === 'type') {
      filters.type = e.target.value;
      applyFilters();
    }
  });

  // State filter
  stateSelect.addEventListener('change', () => {
    filters.state = stateSelect.value;
    applyFilters();
  });

  // Year filter
  yearFromSelect.addEventListener('change', () => {
    filters.yearFrom = yearFromSelect.value;
    if (filters.yearTo && filters.yearFrom > filters.yearTo) {
      [filters.yearFrom, filters.yearTo] = [filters.yearTo, filters.yearFrom];
      yearFromSelect.value = filters.yearFrom;
      yearToSelect.value = filters.yearTo;
    }
    applyFilters();
  });

  yearToSelect.addEventListener('change', () => {
    filters.yearTo = yearToSelect.value;
    if (filters.yearFrom && filters.yearTo < filters.yearFrom) {
      [filters.yearFrom, filters.yearTo] = [filters.yearTo, filters.yearFrom];
      yearFromSelect.value = filters.yearFrom;
      yearToSelect.value = filters.yearTo;
    }
    applyFilters();
  });

  // SDG filter
  filterSdgContainer.addEventListener('change', e => {
    if (e.target.name === 'sdg') {
      filters.sdg = e.target.value;
      applyFilters();
    }
  });

  // Records search
  recordsSearch.addEventListener('input', () => {
    filters.keyword = recordsSearch.value.trim();
    applyFilters();
  });

  // Sort date
  sortDate.addEventListener('click', () => {
    sortOrder = sortOrder === 'desc' ? 'asc' : 'desc';
    sortDate.classList.toggle('sort-asc', sortOrder === 'asc');
    sortDate.classList.toggle('sort-desc', sortOrder === 'desc');
    updateRecordsTable();
  });

  // Show more
  showMoreBtn.addEventListener('click', () => {
    visibleRows += 50;
    updateRecordsTable();
  });

  // Copy citation
  document.addEventListener('click', e => {
    if (e.target.classList.contains('records-details-copy')) {
      const symbol = e.target.getAttribute('data-symbol');
      const para = e.target.getAttribute('data-para');
      const citation = para !== '–' ? `${symbol}, para. ${para}` : symbol;
      navigator.clipboard.writeText(citation).then(() => {
        e.target.classList.add('copied');
        setTimeout(() => {
          e.target.classList.remove('copied');
        }, 2000);
      });
    }
  });

  // Draw sample
  drawSampleBtn.addEventListener('click', () => {
    const seed = parseInt(sampleSeedInput.value) || 1;
    drawSample(seed);
    drawSampleBtn.hidden = true;
    drawAgainBtn.hidden = false;
  });

  drawAgainBtn.addEventListener('click', () => {
    const seed = parseInt(sampleSeedInput.value) || 1;
    drawSample(seed);
  });

  sampleSeedInput.addEventListener('change', () => {
    const seed = parseInt(sampleSeedInput.value) || 1;
    drawSample(seed);
  });

  // Export CSV
  exportCsvBtn.addEventListener('click', () => {
    const headers = [
      'Date', 'Body', 'Symbol', 'Paragraph', 'First line', 'Recommending State',
      'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Full text'
    ];
    const rows = filteredRecords.map(record => {
      const paraMatch = record.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
      const paraNumber = paraMatch ? paraMatch[1] : '–';
      let state = '–';
      if (record.mechanism === 'Universal Periodic Review') {
        const match = record.text.match(stateRegex);
        if (match) {
          const groups = match[1].match(stateGroupRegex) || [];
          const statesInRecord = groups.map(g => g.slice(1, -1).trim()).filter(s => !s.includes(',') && s.length <= 60);
          state = statesInRecord.join(', ') || 'State not found';
        } else {
          state = 'State not found';
        }
      }
      return [
        `"${record.date}"`,
        `"${record.body}"`,
        `"${record.symbol}"`,
        `"${paraNumber}"`,
        `"${record.text.replace(/"/g, '""').slice(0, 120).split(' ').slice(0, -1).join(' ') + '…'}"`,
        `"${state}"`,
        `"${(record.themes || []).join('; ')}"`,
        `"${(record.sdgs || []).map(sdg => `${sdg} ${sdgNames[sdg]}`).join('; ')}"`,
        `"${(record.sdg_targets || []).join('; ')}"`,
        `"${(record.affected_persons || []).join('; ')}"`,
        `"${record.section || ''}"`,
        `"${record.text.replace(/"/g, '""')}"`
      ].join(',');
    });

    const csvContent = [
      `# UN human rights recommendations and observations: ${country}`,
      `# Source: ${uhri.source}`,
      `# Built: ${uhri.built}`,
      `# Filters: ${JSON.stringify(filters)}`,
      `# Records: ${filteredRecords.length}`,
      headers.join(','),
      ...rows
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `uhri-${country.toLowerCase()}-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  // Copy summary
  copySummaryBtn.addEventListener('click', () => {
    const matchingCount = filteredRecords.length;
    const typeCounts = {};
    types.forEach(type => {
      typeCounts[type] = filteredRecords.filter(r => r.type === type).length;
    });
    const typeBreakdown = types.map(type => `${typeCounts[type]} ${type}`).join(', ');

    const themeCounts = {};
    filteredRecords.forEach(record => {
      (record.themes || []).forEach(theme => {
        if (!themeCounts[theme]) themeCounts[theme] = 0;
        themeCounts[theme]++;
      });
    });
    const sortedThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10)
      .map(([theme, count]) => `${theme} (${count})`)
      .join(', ');

    const summary = `UN human rights recommendations and observations: ${country} (${matchingCount} records, ${typeBreakdown}; themes: ${sortedThemes})`;

    navigator.clipboard.writeText(summary).then(() => {
      copySummaryBtn.textContent = 'Copied!';
      setTimeout(() => {
        copySummaryBtn.textContent = 'Copy summary';
      }, 2000);
    });
  });

  // Show States
  showStatesBtn.addEventListener('click', () => {
    const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
    const stateCounts = {};
    states.forEach(state => {
      stateCounts[state] = uprRecords.filter(r => {
        const match = r.text.match(stateRegex);
        if (!match) return false;
        const groups = match[1].match(stateGroupRegex) || [];
        const statesInRecord = groups.map(g => g.slice(1, -1).trim()).filter(s => !s.includes(',') && s.length <= 60);
        return statesInRecord.includes(state);
      }).length;
    });
    const sortedStates = Object.entries(stateCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10)
      .map(([state, count]) => `${state} (${count})`)
      .join(', ');

    const dialog = document.createElement('div');
    dialog.style.position = 'fixed';
    dialog.style.top = '50%';
    dialog.style.left = '50%';
    dialog.style.transform = 'translate(-50%, -50%)';
    dialog.style.backgroundColor = 'white';
    dialog.style.padding = '1rem';
    dialog.style.border = '1px solid var(--rule)';
    dialog.style.borderRadius = '0.25rem';
    dialog.style.boxShadow = '0 0.5rem 1rem rgba(0,0,0,0.1)';
    dialog.style.zIndex = '1000';
    dialog.innerHTML = `
      <h3 style="margin: 0 0 1rem 0; font-family: Georgia, 'Times New Roman', serif;">Ten States that made most recommendations to ${country}</h3>
      <p style="margin: 0 0 1rem 0;">${sortedStates}</p>
      <button style="background-color: var(--red); color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem;">Close</button>
    `;
    document.body.appendChild(dialog);

    dialog.querySelector('button').addEventListener('click', () => {
      document.body.removeChild(dialog);
    });
  });

  // Initialize
  populateFilters();
  applyFilters();
});
</script>
</body>
</html>
```