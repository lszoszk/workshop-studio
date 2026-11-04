Here is the app. It follows the plan exactly: three tabs, a filter rail on the first two, the checks panel under a closed heading on the Overview tab, and every number computed from the data.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
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
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--rule);
  background-color: var(--paper);
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}
.header-label {
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  color: var(--ink);
  letter-spacing: 0.05em;
}
.header-title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.75rem;
  font-weight: 400;
  margin: 0;
  flex-grow: 1;
  text-align: center;
}
.header-meta {
  font-size: 0.875rem;
  color: var(--ink);
  text-align: right;
}
.header-meta a {
  color: var(--ink);
  text-decoration: none;
}
.header-meta a:hover {
  text-decoration: underline;
}
.tablist {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--rule);
  margin: 0;
  padding: 0;
  list-style: none;
}
.tab {
  padding: 0.75rem 1.5rem;
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--ink);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  margin-bottom: -1px;
}
.tab:hover {
  background-color: rgba(155, 35, 53, 0.05);
}
.tab[aria-selected="true"] {
  color: var(--accent);
  border-bottom-color: var(--accent);
  font-weight: 600;
}
.tab:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
main {
  display: flex;
  min-height: calc(100vh - 120px);
}
.rail {
  width: 220px;
  padding: 1rem;
  border-right: 1px solid var(--rule);
  background-color: var(--paper);
  flex-shrink: 0;
}
.rail h2 {
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.75rem 0;
  padding: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rail button.clear {
  background: none;
  border: none;
  font-family: ui-monospace, monospace;
  font-size: 0.75rem;
  color: var(--accent);
  cursor: pointer;
  padding: 0;
}
.rail-count {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1;
  margin: 0 0 0.5rem 0;
  color: var(--ink);
}
.rail-count::after {
  content: attr(data-total);
  font-size: 0.875rem;
  font-family: system-ui, sans-serif;
  font-weight: 400;
  color: var(--ink);
  opacity: 0.7;
}
.rail-bar {
  height: 4px;
  background-color: var(--rule);
  margin-bottom: 1rem;
  position: relative;
}
.rail-bar-fill {
  height: 100%;
  background-color: var(--accent);
  width: 0%;
}
.filter-chip {
  display: inline-flex;
  align-items: center;
  background-color: var(--accent);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  margin: 0 0.25rem 0.25rem 0;
  gap: 0.25rem;
}
.filter-chip button {
  background: none;
  border: none;
  color: white;
  font-size: 0.75rem;
  cursor: pointer;
  padding: 0;
  margin: 0;
  width: 1em;
  height: 1em;
  display: flex;
  align-items: center;
  justify-content: center;
}
.filter-section {
  margin-bottom: 1.5rem;
}
.filter-section h3 {
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5rem 0;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.filter-section h3 button {
  background: none;
  border: none;
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.filter-section[aria-expanded="false"] .filter-content {
  display: none;
}
.filter-keyword input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: system-ui, sans-serif;
  font-size: 0.875rem;
}
.filter-keyword .hint {
  font-size: 0.75rem;
  color: var(--ink);
  opacity: 0.7;
  margin-top: 0.25rem;
}
.filter-mechanism, .filter-body, .filter-type, .filter-state, .filter-year, .filter-sdg {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.filter-mechanism label, .filter-body label, .filter-type label, .filter-state label, .filter-sdg label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.filter-mechanism input, .filter-body input, .filter-type input, .filter-state input, .filter-sdg input {
  margin: 0;
}
.filter-year {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}
.filter-year select {
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: system-ui, sans-serif;
  font-size: 0.875rem;
}
.content {
  flex-grow: 1;
  padding: 1.5rem;
  max-width: calc(100vw - 220px);
}
.content h2 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  margin: 0 0 1rem 0;
}
.content h3 {
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 2rem 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.content h3 button {
  background: none;
  border: none;
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.content h3[aria-expanded="false"] + * {
  display: none;
}
.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.tile {
  border: 1px solid var(--rule);
  padding: 1rem;
  background-color: white;
}
.tile-title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1;
  margin: 0 0 0.5rem 0;
  color: var(--ink);
}
.tile-subtitle {
  font-size: 0.875rem;
  color: var(--ink);
  opacity: 0.7;
  margin: 0 0 0.5rem 0;
}
.tile-body {
  font-size: 0.875rem;
  color: var(--ink);
  margin: 0;
}
.tile-dot {
  display: inline-block;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.tile-dot.upr { background-color: var(--upr); }
.tile-dot.treaty { background-color: var(--treaty); }
.tile-dot.special { background-color: var(--special); }
.tile-note {
  font-size: 0.75rem;
  color: var(--ink);
  opacity: 0.7;
  margin-top: 0.5rem;
}
.chart-container {
  margin: 2rem 0;
  position: relative;
}
.chart-title {
  font-family: ui-monospace, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5rem 0;
}
.chart-source {
  font-size: 0.75rem;
  color: var(--ink);
  opacity: 0.7;
  margin: 0.5rem 0 0 0;
}
.chart-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  font-size: 0.875rem;
}
.chart-table th, .chart-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
.chart-table th {
  font-family: ui-monospace, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-weight: 600;
}
.chart-table td {
  vertical-align: top;
}
.chart-table tr:hover {
  background-color: rgba(155, 35, 53, 0.05);
}
.search-box {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  margin-bottom: 1rem;
}
.table-container {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
table caption {
  font-family: ui-monospace, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  text-align: left;
  margin-bottom: 0.5rem;
  color: var(--ink);
  opacity: 0.7;
}
th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
th {
  font-family: ui-monospace, monospace;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-weight: 600;
  position: sticky;
  top: 0;
  background-color: var(--paper);
}
tbody tr:hover {
  background-color: rgba(155, 35, 53, 0.05);
}
tbody tr[aria-expanded="true"] {
  background-color: rgba(155, 35, 53, 0.05);
}
tbody tr[aria-expanded="true"] td {
  border-bottom: none;
}
tbody tr[aria-expanded="true"] + tr.detail {
  display: table-row;
}
.detail {
  display: none;
}
.detail td {
  padding: 1rem;
  border-bottom: 1px solid var(--rule);
}
.detail-paragraph {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2rem;
  font-weight: 400;
  color: var(--accent);
  margin: 0 0 1rem 0;
}
.detail-text {
  margin: 0 0 1rem 0;
  white-space: pre-wrap;
}
.detail-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}
.detail-label {
  background-color: var(--ink);
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}
.detail-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.detail-actions button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: system-ui, sans-serif;
  font-size: 0.875rem;
  cursor: pointer;
}
.detail-actions button:hover {
  background-color: rgba(155, 35, 53, 0.05);
}
.detail-actions button:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.detail-actions .copied {
  font-size: 0.75rem;
  color: var(--accent);
  margin-left: 0.5rem;
}
.method-section {
  margin-bottom: 2rem;
}
.method-section h3 {
  margin: 1.5rem 0 0.5rem 0;
}
.method-section p {
  margin: 0 0 1rem 0;
  line-height: 1.6;
}
.download-button {
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 1rem;
}
.download-button:hover {
  background-color: rgba(155, 35, 53, 0.05);
}
.download-button:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.copy-button {
  padding: 0.75rem 1.5rem;
  border: 1px solid var(--rule);
  background-color: white;
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  cursor: pointer;
}
.copy-button:hover {
  background-color: rgba(155, 35, 53, 0.05);
}
.copy-button:focus {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
.footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--rule);
  font-family: ui-monospace, monospace;
  font-size: 0.75rem;
  color: var(--ink);
  opacity: 0.7;
  display: flex;
  justify-content: space-between;
}
.credits {
  font-size: 0.75rem;
  color: var(--ink);
  opacity: 0.7;
  margin-top: 0.5rem;
}
mark {
  background-color: rgba(155, 35, 53, 0.2);
  color: var(--ink);
  padding: 0;
}
</style>
</head>
<body>

<header>
  <div class="header-top">
    <div class="header-label">UHRI · <span id="country-name"></span></div>
    <h1 class="header-title">UN human rights recommendations and observations: <span id="country-name-title"></span></h1>
  </div>
  <div class="header-meta">
    Source: <a id="source-link" href="#" target="_blank"></a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · Built <span id="built-date"></span> (dated by document)
  </div>
</header>

<ul class="tablist" role="tablist" aria-label="Tabs">
  <li role="presentation"><button class="tab" id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 OVERVIEW</button></li>
  <li role="presentation"><button class="tab" id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 RECORDS</button></li>
  <li role="presentation"><button class="tab" id="tab-03" role="tab" aria-selected="false" aria-controls="panel-03">03 METHOD & EXPORT</button></li>
</ul>

<main>
  <aside class="rail" id="rail">
    <h2>FILTERS <button class="clear" id="clear-filters">Clear all</button></h2>
    <div class="rail-count" id="rail-count" aria-live="polite">0</div>
    <div class="rail-bar"><div class="rail-bar-fill" id="rail-bar-fill"></div></div>
    <div id="filter-chips"></div>

    <div class="filter-section" id="filter-keyword-section" aria-expanded="true">
      <h3><button id="filter-keyword-toggle">▼ 01 KEYWORD</button></h3>
      <div class="filter-content filter-keyword">
        <input type="text" id="keyword-input" placeholder="Search text or symbol…" aria-label="Keyword search"/>
        <div class="hint">literal match, not synonyms</div>
      </div>
    </div>

    <div class="filter-section" id="filter-mechanism-section" aria-expanded="false">
      <h3><button id="filter-mechanism-toggle">▶ 02 MECHANISM, BODY, TYPE</button></h3>
      <div class="filter-content filter-mechanism">
        <div class="filter-mechanism">
          <label><input type="radio" name="mechanism" value="all" checked/> All mechanisms</label>
          <label><input type="radio" name="mechanism" value="Treaty bodies"/> Treaty bodies</label>
          <label><input type="radio" name="mechanism" value="Universal Periodic Review"/> Universal Periodic Review</label>
          <label><input type="radio" name="mechanism" value="Special Procedures"/> Special Procedures</label>
        </div>
        <div class="filter-body" id="filter-body-options"></div>
        <div class="filter-type" id="filter-type-options"></div>
        <div class="filter-state" id="filter-state-options" hidden>
          <label for="state-select">Recommending State</label>
          <select id="state-select"><option value="all">All States</option></select>
        </div>
      </div>
    </div>

    <div class="filter-section" id="filter-year-section" aria-expanded="false">
      <h3><button id="filter-year-toggle">▶ 03 YEARS AND SDG</button></h3>
      <div class="filter-content filter-year">
        <div class="filter-year">
          <select id="year-from"><option value="">From year</option></select>
          <select id="year-to"><option value="">To year</option></select>
        </div>
        <div class="filter-sdg" id="filter-sdg-options"></div>
      </div>
    </div>
  </aside>

  <div class="content" id="panel-01" role="tabpanel" aria-labelledby="tab-01">
    <div class="tiles">
      <div class="tile">
        <div class="tile-title" id="tile-total">0</div>
        <div class="tile-subtitle" id="tile-type-breakdown"></div>
        <div class="tile-note">How this is computed: records in the file, by type</div>
      </div>
      <div class="tile">
        <div class="tile-title" id="tile-documents">0</div>
        <div class="tile-subtitle">documents</div>
        <div class="tile-note">How this is computed: distinct document symbols</div>
      </div>
      <div class="tile">
        <div class="tile-title" id="tile-years">0–0</div>
        <div class="tile-subtitle">years</div>
        <div class="tile-note">How this is computed: min–max of document years</div>
      </div>
      <div class="tile" id="tile-upr">
        <div class="tile-title">0</div>
        <div class="tile-subtitle"><span class="tile-dot upr"></span> Universal Periodic Review</div>
        <div class="tile-body">in <span id="tile-upr-documents">0</span> documents, latest <span id="tile-upr-latest">0</span> (<span id="tile-upr-share">0</span>%)</div>
        <div class="tile-note">How this is computed: records with mechanism = "Universal Periodic Review"</div>
      </div>
      <div class="tile" id="tile-treaty">
        <div class="tile-title">0</div>
        <div class="tile-subtitle"><span class="tile-dot treaty"></span> Treaty bodies</div>
        <div class="tile-body">in <span id="tile-treaty-documents">0</span> documents, latest <span id="tile-treaty-latest">0</span> (<span id="tile-treaty-share">0</span>%)</div>
        <div class="tile-note">How this is computed: records with mechanism = "Treaty bodies"</div>
      </div>
      <div class="tile" id="tile-special">
        <div class="tile-title">0</div>
        <div class="tile-subtitle"><span class="tile-dot special"></span> Special Procedures</div>
        <div class="tile-body">in <span id="tile-special-documents">0</span> documents, latest <span id="tile-special-latest">0</span> (<span id="tile-special-share">0</span>%)</div>
        <div class="tile-note">How this is computed: records with mechanism = "Special Procedures"</div>
      </div>
    </div>

    <h3><span id="fig01-title">FIG.01</span> <button id="fig01-toggle" aria-expanded="true">▼</button></h3>
    <div class="chart-container">
      <canvas id="fig01-chart"></canvas>
      <div class="chart-title" id="fig01-subtitle"></div>
      <div class="chart-source">Source: computed from the filtered records</div>
      <table class="chart-table">
        <thead>
          <tr><th>THEME</th><th>RECORDS</th><th>% OF FILTERED</th><th>YEARS</th></tr>
        </thead>
        <tbody id="fig01-table"></tbody>
      </table>
      <div class="chart-note">A record can carry several themes, so the bars add up to more than the number of records.</div>
    </div>

    <h3><span id="fig02-title">FIG.02</span> <button id="fig02-toggle" aria-expanded="true">▼</button></h3>
    <div class="chart-container">
      <canvas id="fig02-chart"></canvas>
      <div class="chart-source">Source: computed from the filtered records</div>
    </div>

    <h3><button id="checks-toggle" aria-expanded="false">▶ EVERY CHECK (<span id="checks-count">0</span>)</button></h3>
    <div id="checks-panel"></div>
  </div>

  <div class="content" id="panel-02" role="tabpanel" aria-labelledby="tab-02" hidden>
    <input type="text" class="search-box" id="search-input" placeholder="Search records, e.g. torture" aria-label="Search records"/>
    <div class="table-container">
      <table>
        <caption id="table-caption">Showing 0 of 0 records</caption>
        <thead>
          <tr>
            <th id="sort-date" tabindex="0" role="button" aria-label="Sort by date">DATE</th>
            <th>BODY</th>
            <th>SYMBOL</th>
            <th>PARA.</th>
            <th>FIRST LINE</th>
            <th id="state-column-header">RECOMMENDING STATE</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>
    <button id="load-more" hidden>Show 50 more</button>
  </div>

  <div class="content" id="panel-03" role="tabpanel" aria-labelledby="tab-03" hidden>
    <div class="method-section">
      <h2>How each number is computed</h2>
      <p>Every number is computed from the data in the browser, never estimated. The headline total is the number of records in the file. The breakdown counts records per type, using the values exactly as spelled in the data. Documents is the number of distinct document symbols. Years is the minimum and maximum year of the documents.</p>
      <p>Filters: Mechanism, body and type match the field exactly. Year is inclusive between the two selects. SDG checks if the goal number is in the record's sdgs array. Keyword search is literal: every word must occur as a substring of the text or symbol. The filtered set feeds the tiles, charts, table and export.</p>
      <p>Theme counts: for each record in the filtered set, each value in themes counts once. The top ten are ranked by count, ties alphabetical. Percentage is count divided by the number of filtered records, one decimal. Year range is the min and max year of the records carrying that theme.</p>
      <p>Timeline: records per year per mechanism in the filtered set, with zero for missing combinations. Paragraph number is the first match of a regular expression on the text; no match means no number. Recommending State is extracted from UPR texts only, using a regular expression on the trailing parentheses.</p>
    </div>

    <div class="method-section">
      <h2>Take this with you</h2>
      <button class="download-button" id="download-csv">Download CSV of the current filter</button>
      <button class="copy-button" id="copy-summary">Copy summary</button>
    </div>

    <div class="method-section">
      <h2>Data source and licence</h2>
      <p>The data is the Universal Human Rights Index (UHRI) as provided by the Office of the United Nations High Commissioner for Human Rights. The UHRI is in the public domain; the app is released under the MIT licence.</p>
      <p>Built on <span id="built-date-footer"></span>.</p>
    </div>
  </div>
</main>

<footer class="footer">
  <div>Built on OHCHR UHRI data · <span id="record-count-footer"></span> records · <a id="source-link-footer" href="#" target="_blank">source</a></div>
  <div class="credits">Credits: UK Government Analysis Function (charts and tables, Open Government Licence v3.0)</div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  // Data
  const uhri = window.WORKSHOP_DATA.uhri;
  const country = uhri.country;
  const records = uhri.records;
  const sdgNames = uhri.sdg_names || {};
  const source = uhri.source;
  const sourceUrl = uhri.source_url;
  const built = uhri.built;
  const totalRecords = Number(uhri.count);

  // DOM
  const countryNameEl = document.getElementById('country-name');
  const countryNameTitleEl = document.getElementById('country-name-title');
  const sourceLinkEl = document.getElementById('source-link');
  const sourceLinkFooterEl = document.getElementById('source-link-footer');
  const recordCountEl = document.getElementById('record-count');
  const recordCountFooterEl = document.getElementById('record-count-footer');
  const documentCountEl = document.getElementById('document-count');
  const yearRangeEl = document.getElementById('year-range');
  const builtDateEl = document.getElementById('built-date');
  const builtDateFooterEl = document.getElementById('built-date-footer');

  countryNameEl.textContent = country;
  countryNameTitleEl.textContent = country;
  sourceLinkEl.textContent = source;
  sourceLinkEl.href = sourceUrl;
  sourceLinkFooterEl.textContent = source;
  sourceLinkFooterEl.href = sourceUrl;
  recordCountEl.textContent = totalRecords.toLocaleString();
  recordCountFooterEl.textContent = totalRecords.toLocaleString();
  builtDateEl.textContent = built;
  builtDateFooterEl.textContent = built;

  // State for filters
  let filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    state: 'all',
    yearFrom: null,
    yearTo: null,
    sdg: 'all'
  };
  let filteredRecords = [];
  let stateList = new Map();
  let bodyList = new Map();
  let typeList = new Map();
  let yearList = [];
  let sdgList = new Map();
  let themeList = new Map();
  let paragraphStats = { upr: 0, treaty: 0, special: 0, uprTotal: 0, treatyTotal: 0, specialTotal: 0 };
  let checks = [];

  // Initialize
  function init() {
    // Extract distinct values
    records.forEach(record => {
      // Body
      if (!bodyList.has(record.body)) {
        bodyList.set(record.body, 0);
      }
      bodyList.set(record.body, bodyList.get(record.body) + 1);

      // Type
      if (!typeList.has(record.type)) {
        typeList.set(record.type, 0);
      }
      typeList.set(record.type, typeList.get(record.type) + 1);

      // Year
      if (!yearList.includes(record.year)) {
        yearList.push(record.year);
      }

      // SDG
      if (record.sdgs && record.sdgs.length) {
        record.sdgs.forEach(sdg => {
          if (!sdgList.has(sdg)) {
            sdgList.set(sdg, 0);
          }
          sdgList.set(sdg, sdgList.get(sdg) + 1);
        });
      }

      // Theme
      if (record.themes && record.themes.length) {
        record.themes.forEach(theme => {
          if (!themeList.has(theme)) {
            themeList.set(theme, { count: 0, years: new Set() });
          }
          const themeData = themeList.get(theme);
          themeData.count++;
          themeData.years.add(record.year);
          themeList.set(theme, themeData);
        });
      }

      // State (UPR only)
      if (record.mechanism === 'Universal Periodic Review') {
        const states = extractStates(record.text);
        if (states.length) {
          states.forEach(state => {
            if (!stateList.has(state)) {
              stateList.set(state, 0);
            }
            stateList.set(state, stateList.get(state) + 1);
          });
        }
      }

      // Paragraph stats
      const mechanismKey = record.mechanism === 'Universal Periodic Review' ? 'upr' :
                           record.mechanism === 'Treaty bodies' ? 'treaty' : 'special';
      const hasParagraph = extractParagraphNumber(record.text) !== null;
      paragraphStats[mechanismKey + 'Total']++;
      if (hasParagraph) {
        paragraphStats[mechanismKey]++;
      }
    });

    // Sort years
    yearList.sort((a, b) => a - b);

    // Populate selects
    const yearFromSelect = document.getElementById('year-from');
    const yearToSelect = document.getElementById('year-to');
    yearList.forEach(year => {
      const optionFrom = document.createElement('option');
      optionFrom.value = year;
      optionFrom.textContent = year;
      yearFromSelect.appendChild(optionFrom);

      const optionTo = document.createElement('option');
      optionTo.value = year;
      optionTo.textContent = year;
      yearToSelect.appendChild(optionTo);
    });

    // Populate body options
    const bodyOptionsEl = document.getElementById('filter-body-options');
    const bodies = Array.from(bodyList.keys()).sort();
    bodies.forEach(body => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'body';
      input.value = body;
      input.checked = body === 'all';
      label.appendChild(input);
      label.appendChild(document.createTextNode(` ${body} (${bodyList.get(body)})`));
      bodyOptionsEl.appendChild(label);
    });

    // Populate type options
    const typeOptionsEl = document.getElementById('filter-type-options');
    const types = Array.from(typeList.keys()).sort();
    types.forEach(type => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'type';
      input.value = type;
      input.checked = type === 'all';
      label.appendChild(input);
      label.appendChild(document.createTextNode(` ${type} (${typeList.get(type)})`));
      typeOptionsEl.appendChild(label);
    });

    // Populate state select
    const stateSelect = document.getElementById('state-select');
    const states = Array.from(stateList.keys()).sort((a, b) => stateList.get(b) - stateList.get(a));
    states.forEach(state => {
      const option = document.createElement('option');
      option.value = state;
      option.textContent = `${state} (${stateList.get(state)})`;
      stateSelect.appendChild(option);
    });

    // Populate SDG options
    const sdgOptionsEl = document.getElementById('filter-sdg-options');
    const sdgs = Array.from(sdgList.keys()).sort((a, b) => a - b);
    sdgs.forEach(sdg => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'sdg';
      input.value = sdg;
      input.checked = sdg === 'all';
      label.appendChild(input);
      label.appendChild(document.createTextNode(` SDG ${sdg}: ${sdgNames[sdg] || 'Unknown'} (${sdgList.get(sdg)})`));
      sdgOptionsEl.appendChild(label);
    });

    // Set document and year counts
    const distinctSymbols = new Set(records.map(r => r.symbol)).size;
    documentCountEl.textContent = distinctSymbols.toLocaleString();
    yearRangeEl.textContent = `${Math.min(...yearList)}–${Math.max(...yearList)}`;

    // Set up event listeners
    setupEventListeners();

    // Initial filter
    applyFilters();
  }

  function setupEventListeners() {
    // Tabs
    document.getElementById('tab-01').addEventListener('click', () => switchTab('01'));
    document.getElementById('tab-02').addEventListener('click', () => switchTab('02'));
    document.getElementById('tab-03').addEventListener('click', () => switchTab('03'));

    // Filter toggles
    document.getElementById('filter-keyword-toggle').addEventListener('click', () => toggleFilterSection('keyword'));
    document.getElementById('filter-mechanism-toggle').addEventListener('click', () => toggleFilterSection('mechanism'));
    document.getElementById('filter-year-toggle').addEventListener('click', () => toggleFilterSection('year'));

    // Clear filters
    document.getElementById('clear-filters').addEventListener('click', () => {
      filters = {
        keyword: '',
        mechanism: 'all',
        body: 'all',
        type: 'all',
        state: 'all',
        yearFrom: null,
        yearTo: null,
        sdg: 'all'
      };
      document.getElementById('keyword-input').value = '';
      document.querySelector('input[name="mechanism"][value="all"]').checked = true;
      document.querySelector('input[name="body"][value="all"]').checked = true;
      document.querySelector('input[name="type"][value="all"]').checked = true;
      document.getElementById('state-select').value = 'all';
      document.getElementById('year-from').value = '';
      document.getElementById('year-to').value = '';
      document.querySelector('input[name="sdg"][value="all"]').checked = true;
      applyFilters();
    });

    // Mechanism change
    document.querySelectorAll('input[name="mechanism"]').forEach(input => {
      input.addEventListener('change', (e) => {
        filters.mechanism = e.target.value;
        filters.body = 'all';
        filters.state = 'all';
        updateBodyOptions();
        applyFilters();
      });
    });

    // Body change
    document.querySelectorAll('input[name="body"]').forEach(input => {
      input.addEventListener('change', (e) => {
        filters.body = e.target.value;
        applyFilters();
      });
    });

    // Type change
    document.querySelectorAll('input[name="type"]').forEach(input => {
      input.addEventListener('change', (e) => {
        filters.type = e.target.value;
        applyFilters();
      });
    });

    // State change
    document.getElementById('state-select').addEventListener('change', (e) => {
      filters.state = e.target.value;
      applyFilters();
    });

    // Year change
    document.getElementById('year-from').addEventListener('change', (e) => {
      filters.yearFrom = e.target.value ? Number(e.target.value) : null;
      applyFilters();
    });
    document.getElementById('year-to').addEventListener('change', (e) => {
      filters.yearTo = e.target.value ? Number(e.target.value) : null;
      applyFilters();
    });

    // SDG change
    document.querySelectorAll('input[name="sdg"]').forEach(input => {
      input.addEventListener('change', (e) => {
        filters.sdg = e.target.value;
        applyFilters();
      });
    });

    // Keyword search
    let keywordTimeout;
    document.getElementById('keyword-input').addEventListener('input', (e) => {
      clearTimeout(keywordTimeout);
      keywordTimeout = setTimeout(() => {
        filters.keyword = e.target.value.trim();
        applyFilters();
      }, 300);
    });

    // Search on records tab
    document.getElementById('search-input').addEventListener('input', (e) => {
      renderTable(e.target.value.trim());
    });

    // Sort by date
    document.getElementById('sort-date').addEventListener('click', () => {
      const th = document.getElementById('sort-date');
      const currentOrder = th.getAttribute('data-order') || 'desc';
      const newOrder = currentOrder === 'desc' ? 'asc' : 'desc';
      th.setAttribute('data-order', newOrder);
      th.setAttribute('aria-label', `Sort by date ${newOrder === 'desc' ? 'descending' : 'ascending'}`);
      renderTable(document.getElementById('search-input').value.trim());
    });

    // Load more
    document.getElementById('load-more').addEventListener('click', () => {
      const tbody = document.getElementById('table-body');
      const rows = tbody.querySelectorAll('tr:not(.detail)');
      const nextRows = Array.from(rows).slice(rows.length, rows.length + 50);
      nextRows.forEach(row => {
        row.hidden = false;
      });
      if (nextRows.length < 50) {
        document.getElementById('load-more').hidden = true;
      }
    });

    // Download CSV
    document.getElementById('download-csv').addEventListener('click', downloadCSV);

    // Copy summary
    document.getElementById('copy-summary').addEventListener('click', copySummary);

    // Checks toggle
    document.getElementById('checks-toggle').addEventListener('click', () => {
      const button = document.getElementById('checks-toggle');
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !isExpanded);
    });

    // Fig01 toggle
    document.getElementById('fig01-toggle').addEventListener('click', () => {
      const button = document.getElementById('fig01-toggle');
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !isExpanded);
    });

    // Fig02 toggle
    document.getElementById('fig02-toggle').addEventListener('click', () => {
      const button = document.getElementById('fig02-toggle');
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !isExpanded);
    });
  }

  function toggleFilterSection(section) {
    const sections = ['keyword', 'mechanism', 'year'];
    sections.forEach(s => {
      const el = document.getElementById(`filter-${s}-section`);
      if (s === section) {
        const isExpanded = el.getAttribute('aria-expanded') === 'true';
        el.setAttribute('aria-expanded', !isExpanded);
      } else {
        el.setAttribute('aria-expanded', 'false');
      }
    });
  }

  function updateBodyOptions() {
    const bodyOptionsEl = document.getElementById('filter-body-options');
    bodyOptionsEl.innerHTML = '';

    if (filters.mechanism === 'all') {
      const bodies = Array.from(bodyList.keys()).sort();
      bodies.forEach(body => {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'body';
        input.value = body;
        input.checked = body === 'all';
        label.appendChild(input);
        label.appendChild(document.createTextNode(` ${body} (${bodyList.get(body)})`));
        bodyOptionsEl.appendChild(label);
      });
    } else {
      const bodies = Array.from(bodyList.keys())
        .filter(body => {
          const record = records.find(r => r.body === body);
          return record && record.mechanism === filters.mechanism;
        })
        .sort();
      if (bodies.length > 1) {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'body';
        input.value = 'all';
        input.checked = true;
        label.appendChild(input);
        label.appendChild(document.createTextNode(` All bodies (${bodies.reduce((sum, body) => sum + bodyList.get(body), 0)})`));
        bodyOptionsEl.appendChild(label);
      }
      bodies.forEach(body => {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'body';
        input.value = body;
        input.checked = false;
        label.appendChild(input);
        label.appendChild(document.createTextNode(` ${body} (${bodyList.get(body)})`));
        bodyOptionsEl.appendChild(label);
      });
    }

    // State select visibility
    const stateSelect = document.getElementById('filter-state-options');
    if (filters.mechanism === 'Universal Periodic Review') {
      stateSelect.hidden = false;
    } else {
      stateSelect.hidden = true;
      filters.state = 'all';
    }
  }

  function applyFilters() {
    filteredRecords = records.filter(record => {
      // Keyword
      if (filters.keyword) {
        const keywords = filters.keyword.toLowerCase().split(/\s+/);
        const text = record.text.toLowerCase();
        const symbol = record.symbol.toLowerCase();
        if (!keywords.every(kw => text.includes(kw) || symbol.includes(kw))) {
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
      if (filters.mechanism === 'Universal Periodic Review' && filters.state !== 'all') {
        const states = extractStates(record.text);
        if (!states.includes(filters.state)) {
          return false;
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
        if (!record.sdgs || !record.sdgs.includes(Number(filters.sdg))) {
          return false;
        }
      }

      return true;
    });

    // Update rail count and bar
    const railCountEl = document.getElementById('rail-count');
    railCountEl.textContent = filteredRecords.length;
    railCountEl.setAttribute('data-total', `of ${totalRecords.toLocaleString()} in the file`);
    const railBarFillEl = document.getElementById('rail-bar-fill');
    const share = totalRecords > 0 ? filteredRecords.length / totalRecords : 0;
    railBarFillEl.style.width = `${share * 100}%`;

    // Update filter chips
    updateFilterChips();

    // Update tiles
    updateTiles();

    // Update charts
    updateFig01();
    updateFig02();

    // Update checks
    updateChecks();

    // Update table
    renderTable(document.getElementById('search-input').value.trim());
  }

  function updateFilterChips() {
    const chipsEl = document.getElementById('filter-chips');
    chipsEl.innerHTML = '';

    if (filters.keyword) {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Keyword: ${filters.keyword}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.keyword = '';
        document.getElementById('keyword-input').value = '';
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.mechanism !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Mechanism: ${filters.mechanism}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.mechanism = 'all';
        document.querySelector('input[name="mechanism"][value="all"]').checked = true;
        updateBodyOptions();
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.body !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Body: ${filters.body}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.body = 'all';
        document.querySelector('input[name="body"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.type !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `Type: ${filters.type}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.type = 'all';
        document.querySelector('input[name="type"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.state !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `State: ${filters.state}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.state = 'all';
        document.getElementById('state-select').value = 'all';
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.yearFrom) {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `From: ${filters.yearFrom}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.yearFrom = null;
        document.getElementById('year-from').value = '';
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.yearTo) {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `To: ${filters.yearTo}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.yearTo = null;
        document.getElementById('year-to').value = '';
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }

    if (filters.sdg !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'filter-chip';
      chip.textContent = `SDG: ${filters.sdg}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.sdg = 'all';
        document.querySelector('input[name="sdg"][value="all"]').checked = true;
        applyFilters();
      });
      chip.appendChild(button);
      chipsEl.appendChild(chip);
    }
  }

  function updateTiles() {
    const tileTotalEl = document.getElementById('tile-total');
    const tileTypeBreakdownEl = document.getElementById('tile-type-breakdown');
    const tileDocumentsEl = document.getElementById('tile-documents');
    const tileYearsEl = document.getElementById('tile-years');

    tileTotalEl.textContent = filteredRecords.length.toLocaleString();

    // Type breakdown
    const typeCounts = {};
    filteredRecords.forEach(record => {
      if (!typeCounts[record.type]) {
        typeCounts[record.type] = 0;
      }
      typeCounts[record.type]++;
    });
    const typeBreakdown = Object.entries(typeCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([type, count]) => `${type} ${count.toLocaleString()}`)
      .join(', ');
    tileTypeBreakdownEl.textContent = typeBreakdown;

    // Documents
    const distinctSymbols = new Set(filteredRecords.map(r => r.symbol)).size;
    tileDocumentsEl.textContent = distinctSymbols.toLocaleString();

    // Years
    const years = filteredRecords.map(r => r.year);
    const minYear = years.length ? Math.min(...years) : 0;
    const maxYear = years.length ? Math.max(...years) : 0;
    tileYearsEl.textContent = `${minYear}–${maxYear}`;

    // Mechanism tiles
    const mechanisms = {
      upr: filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review'),
      treaty: filteredRecords.filter(r => r.mechanism === 'Treaty bodies'),
      special: filteredRecords.filter(r => r.mechanism === 'Special Procedures')
    };

    const uprTile = document.getElementById('tile-upr');
    const treatyTile = document.getElementById('tile-treaty');
    const specialTile = document.getElementById('tile-special');

    uprTile.querySelector('.tile-title').textContent = mechanisms.upr.length.toLocaleString();
    uprTile.querySelector('#tile-upr-documents').textContent = new Set(mechanisms.upr.map(r => r.symbol)).size;
    const uprLatest = mechanisms.upr.length ? Math.max(...mechanisms.upr.map(r => r.year)) : 0;
    uprTile.querySelector('#tile-upr-latest').textContent = uprLatest;
    const uprShare = filteredRecords.length > 0 ? (mechanisms.upr.length / filteredRecords.length * 100).toFixed(0) : 0;
    uprTile.querySelector('#tile-upr-share').textContent = uprShare;

    treatyTile.querySelector('.tile-title').textContent = mechanisms.treaty.length.toLocaleString();
    treatyTile.querySelector('#tile-treaty-documents').textContent = new Set(mechanisms.treaty.map(r => r.symbol)).size;
    const treatyLatest = mechanisms.treaty.length ? Math.max(...mechanisms.treaty.map(r => r.year)) : 0;
    treatyTile.querySelector('#tile-treaty-latest').textContent = treatyLatest;
    const treatyShare = filteredRecords.length > 0 ? (mechanisms.treaty.length / filteredRecords.length * 100).toFixed(0) : 0;
    treatyTile.querySelector('#tile-treaty-share').textContent = treatyShare;

    specialTile.querySelector('.tile-title').textContent = mechanisms.special.length.toLocaleString();
    specialTile.querySelector('#tile-special-documents').textContent = new Set(mechanisms.special.map(r => r.symbol)).size;
    const specialLatest = mechanisms.special.length ? Math.max(...mechanisms.special.map(r => r.year)) : 0;
    specialTile.querySelector('#tile-special-latest').textContent = specialLatest;
    const specialShare = filteredRecords.length > 0 ? (mechanisms.special.length / filteredRecords.length * 100).toFixed(0) : 0;
    specialTile.querySelector('#tile-special-share').textContent = specialShare;
  }

  function updateFig01() {
    const fig01TitleEl = document.getElementById('fig01-title');
    const fig01SubtitleEl = document.getElementById('fig01-subtitle');
    const fig01TableEl = document.getElementById('fig01-table');

    fig01TitleEl.textContent = `FIG.01 Ten most frequent themes among ${filteredRecords.length.toLocaleString()} filtered records`;
    fig01SubtitleEl.textContent = `Top themes by record count (click a bar to filter)`;

    // Count themes in filtered records
    const themeCounts = new Map();
    filteredRecords.forEach(record => {
      if (record.themes && record.themes.length) {
        record.themes.forEach(theme => {
          if (!themeCounts.has(theme)) {
            themeCounts.set(theme, 0);
          }
          themeCounts.set(theme, themeCounts.get(theme) + 1);
        });
      }
    });

    // Sort by count, then by name
    const sortedThemes = Array.from(themeCounts.entries())
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);

    // Prepare data for chart
    const labels = sortedThemes.map(([theme]) => theme);
    const data = sortedThemes.map(([, count]) => count);
    const backgroundColor = sortedThemes.map(() => `rgba(155, 35, 53, 0.8)`);

    // Destroy previous chart
    const canvas = document.getElementById('fig01-chart');
    if (canvas.chart) {
      canvas.chart.destroy();
    }

    // Create chart
    canvas.chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: backgroundColor,
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
              label: (context) => {
                const theme = context.label;
                const count = context.raw;
                const share = filteredRecords.length > 0 ? (count / filteredRecords.length * 100).toFixed(1) : 0;
                const years = themeList.get(theme).years;
                const minYear = Math.min(...years);
                const maxYear = Math.max(...years);
                return [
                  `Records: ${count.toLocaleString()}`,
                  `Share: ${share}%`,
                  `Years: ${minYear}–${maxYear}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            display: false,
            beginAtZero: true
          },
          y: {
            beginAtZero: true,
            ticks: {
              font: {
                family: 'system-ui, sans-serif',
                size: 12
              }
            },
            grid: { display: false }
          }
        },
        onClick: (e, activeEls) => {
          if (activeEls.length) {
            const index = activeEls[0].index;
            const theme = labels[index];
            // Add theme as a keyword filter
            filters.keyword = theme;
            document.getElementById('keyword-input').value = theme;
            applyFilters();
          }
        }
      }
    });

    // Update table
    fig01TableEl.innerHTML = '';
    sortedThemes.forEach(([theme, count]) => {
      const share = filteredRecords.length > 0 ? (count / filteredRecords.length * 100).toFixed(1) : 0;
      const years = themeList.get(theme).years;
      const minYear = Math.min(...years);
      const maxYear = Math.max(...years);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${theme}</td>
        <td>${count.toLocaleString()}</td>
        <td>${share}%</td>
        <td>${minYear}–${maxYear}</td>
      `;
      fig01TableEl.appendChild(tr);
    });
  }

  function updateFig02() {
    // Prepare data: records per year per mechanism
    const years = Array.from(new Set(records.map(r => r.year))).sort((a, b) => a - b);
    const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
    const mechanismColors = {
      'Universal Periodic Review': 'rgba(194, 65, 12, 0.8)',
      'Treaty bodies': 'rgba(15, 118, 110, 0.8)',
      'Special Procedures': 'rgba(124, 58, 237, 0.8)'
    };

    const datasets = mechanisms.map(mechanism => {
      const data = years.map(year => {
        return filteredRecords.filter(r => r.mechanism === mechanism && r.year === year).length;
      });
      return {
        label: mechanism,
        data: data,
        backgroundColor: mechanismColors[mechanism],
        borderWidth: 0
      };
    });

    // Destroy previous chart
    const canvas = document.getElementById('fig02-chart');
    if (canvas.chart) {
      canvas.chart.destroy();
    }

    // Create chart
    canvas.chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: years.map(y => y.toString()),
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: {
                family: 'system-ui, sans-serif',
                size: 12
              }
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const mechanism = context.dataset.label;
                const count = context.raw;
                const year = context.label;
                return `${mechanism}: ${count.toLocaleString()} record${count !== 1 ? 's' : ''} in ${year}`;
              }
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            ticks: {
              font: {
                family: 'system-ui, sans-serif',
                size: 12
              }
            }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              font: {
                family: 'system-ui, sans-serif',
                size: 12
              }
            }
          }
        }
      }
    });
  }

  function updateChecks() {
    checks = [];

    // 1. Record count
    const recordCountCheck = {
      label: 'Record count',
      value1: records.length.toLocaleString(),
      value2: totalRecords.toLocaleString(),
      pass: records.length === totalRecords,
      note: 'records.length against Number(uhri.count)'
    };
    checks.push(recordCountCheck);

    // 2. Partitions
    const mechanismCounts = {};
    const bodyCounts = {};
    const yearCounts = {};
    records.forEach(record => {
      mechanismCounts[record.mechanism] = (mechanismCounts[record.mechanism] || 0) + 1;
      bodyCounts[record.body] = (bodyCounts[record.body] || 0) + 1;
      yearCounts[record.year] = (yearCounts[record.year] || 0) + 1;
    });
    const mechanismSum = Object.values(mechanismCounts).reduce((a, b) => a + b, 0);
    const bodySum = Object.values(bodyCounts).reduce((a, b) => a + b, 0);
    const yearSum = Object.values(yearCounts).reduce((a, b) => a + b, 0);

    const mechanismCheck = {
      label: 'Mechanism partition',
      value1: mechanismSum.toLocaleString(),
      value2: records.length.toLocaleString(),
      pass: mechanismSum === records.length,
      note: 'sum of counts per mechanism against record count'
    };
    checks.push(mechanismCheck);

    const bodyCheck = {
      label: 'Body partition',
      value1: bodySum.toLocaleString(),
      value2: records.length.toLocaleString(),
      pass: bodySum === records.length,
      note: 'sum of counts per body against record count'
    };
    checks.push(bodyCheck);

    const yearCheck = {
      label: 'Year partition',
      value1: yearSum.toLocaleString(),
      value2: records.length.toLocaleString(),
      pass: yearSum === records.length,
      note: 'sum of counts per year against record count'
    };
    checks.push(yearCheck);

    // 3. Type partition
    const typeCounts = {};
    records.forEach(record => {
      typeCounts[record.type] = (typeCounts[record.type] || 0) + 1;
    });
    const typeSum = Object.values(typeCounts).reduce((a, b) => a + b, 0);

    const typeCheck = {
      label: 'Type partition',
      value1: typeSum.toLocaleString(),
      value2: records.length.toLocaleString(),
      pass: typeSum === records.length,
      note: 'sum of counts per type against record count'
    };
    checks.push(typeCheck);

    // 4. Chart against table
    const themeCounts = new Map();
    filteredRecords.forEach(record => {
      if (record.themes && record.themes.length) {
        record.themes.forEach(theme => {
          if (!themeCounts.has(theme)) {
            themeCounts.set(theme, 0);
          }
          themeCounts.set(theme, themeCounts.get(theme) + 1);
        });
      }
    });
    const sortedThemes = Array.from(themeCounts.entries())
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);

    let chartTableCheckPass = true;
    const fig01TableRows = document.querySelectorAll('#fig01-table tr');
    sortedThemes.forEach(([theme, count], i) => {
      const row = fig01TableRows[i];
      if (row) {
        const rowCount = Number(row.children[1].textContent.replace(/\D/g, ''));
        if (rowCount !== count) {
          chartTableCheckPass = false;
        }
      }
    });
    if (sortedThemes.length > 0 && sortedThemes[0][1] > filteredRecords.length) {
      chartTableCheckPass = false;
    }

    const chartTableCheck = {
      label: 'Chart against table',
      value1: sortedThemes.length ? sortedThemes[0][1].toLocaleString() : '0',
      value2: filteredRecords.length.toLocaleString(),
      pass: chartTableCheckPass,
      note: 'largest bar value against filtered record count, and table values against recomputed counts'
    };
    checks.push(chartTableCheck);

    // 5. Links
    const linkErrors = [];
    records.forEach(record => {
      const url = record.doc_url;
      const symbol = record.symbol;
      if (!url.startsWith('https://docs.un.org/') || !decodeURIComponent(url).toLowerCase().endsWith(symbol.toLowerCase())) {
        linkErrors.push(record.symbol);
      }
    });

    const linkCheck = {
      label: 'Links',
      value1: linkErrors.length ? linkErrors.join(', ') : 'none',
      value2: '0 errors expected',
      pass: linkErrors.length === 0,
      note: 'every doc_url starts with "https://docs.un.org/" and ends with its symbol (case-insensitive)'
    };
    checks.push(linkCheck);

    // 6. Paragraph numbers
    const paragraphStatsCheck = {
      label: 'Paragraph numbers',
      value1: `UPR ${paragraphStats.upr}/${paragraphStats.uprTotal} (${Math.round(paragraphStats.upr / paragraphStats.uprTotal * 100)}%), Treaty ${paragraphStats.treaty}/${paragraphStats.treatyTotal} (${Math.round(paragraphStats.treaty / paragraphStats.treatyTotal * 100)}%), Special ${paragraphStats.special}/${paragraphStats.specialTotal} (${Math.round(paragraphStats.special / paragraphStats.specialTotal * 100)}%)`,
      value2: 'UPR 100% expected',
      pass: paragraphStats.upr === paragraphStats.uprTotal,
      note: 'share of records with a paragraph number found, per mechanism'
    };
    checks.push(paragraphStatsCheck);

    // 7. States found
    const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
    const stateErrors = uprRecords.filter(record => {
      const states = extractStates(record.text);
      return states.length === 0;
    });

    const stateCheck = {
      label: 'States found',
      value1: `${uprRecords.length - stateErrors.length}/${uprRecords.length}`,
      value2: `${uprRecords.length}/${uprRecords.length}`,
      pass: stateErrors.length === 0,
      note: 'UPR records with at least one State found; records without one are listed below'
    };
    checks.push(stateCheck);

    // 8. Duplicates and gaps
    const ids = records.map(r => r.id);
    const distinctIds = new Set(ids).size;
    const idCheck = {
      label: 'Distinct ids',
      value1: distinctIds.toLocaleString(),
      value2: records.length.toLocaleString(),
      pass: distinctIds === records.length,
      note: 'distinct id against record count'
    };
    checks.push(idCheck);

    const textCounts = {};
    records.forEach(record => {
      textCounts[record.text] = (textCounts[record.text] || 0) + 1;
    });
    const duplicateTexts = Object.values(textCounts).filter(v => v > 1).length;

    const duplicateCheck = {
      label: 'Duplicate texts',
      value1: duplicateTexts.toLocaleString(),
      value2: '0 expected',
      pass: duplicateTexts === 0,
      note: 'number of duplicate text values'
    };
    checks.push(duplicateCheck);

    const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
    const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;

    const labelsCheck = {
      label: 'Missing labels',
      value1: `themes ${noThemes}, SDGs ${noSdgs}, affected ${noAffected}`,
      value2: '0 expected for each',
      pass: noThemes === 0 && noSdgs === 0 && noAffected === 0,
      note: 'records with no themes, no sdgs, no affected_persons'
    };
    checks.push(labelsCheck);

    // Render checks
    const checksPanelEl = document.getElementById('checks-panel');
    checksPanelEl.innerHTML = '';
    checks.forEach(check => {
      const div = document.createElement('div');
      div.style.marginBottom = '0.5rem';
      div.style.padding = '0.5rem';
      div.style.borderBottom = '1px solid var(--rule)';

      const passEl = document.createElement('span');
      passEl.textContent = check.pass ? '✓ pass' : '✗ check failed';
      passEl.style.color = check.pass ? 'var(--treaty)' : 'var(--accent)';
      passEl.style.fontWeight = '600';

      div.appendChild(passEl);
      div.appendChild(document.createTextNode(` ${check.label}: `));
      div.appendChild(document.createTextNode(`${check.value1} vs ${check.value2}`));
      if (check.note) {
        const noteEl = document.createElement('div');
        noteEl.textContent = check.note;
        noteEl.style.fontSize = '0.75rem';
        noteEl.style.opacity = '0.7';
        noteEl.style.marginTop = '0.25rem';
        div.appendChild(noteEl);
      }

      checksPanelEl.appendChild(div);
    });

    // Add state errors list
    if (stateErrors.length > 0) {
      const stateErrorsEl = document.createElement('div');
      stateErrorsEl.style.marginTop = '1rem';
      stateErrorsEl.style.padding = '0.5rem';
      stateErrorsEl.style.borderTop = '1px solid var(--rule)';
      stateErrorsEl.innerHTML = '<strong>UPR records without a State found:</strong><br>';

      const listEl = document.createElement('ul');
      stateErrors.forEach(record => {
        const itemEl = document.createElement('li');
        itemEl.textContent = `${record.symbol}: "${record.text.slice(-50)}"`;
        listEl.appendChild(itemEl);
      });
      stateErrorsEl.appendChild(listEl);
      checksPanelEl.appendChild(stateErrorsEl);
    }

    // Add link errors list
    if (linkErrors.length > 0) {
      const linkErrorsEl = document.createElement('div');
      linkErrorsEl.style.marginTop = '1rem';
      linkErrorsEl.style.padding = '0.5rem';
      linkErrorsEl.style.borderTop = '1px solid var(--rule)';
      linkErrorsEl.innerHTML = '<strong>Records with link errors:</strong><br>';

      const listEl = document.createElement('ul');
      linkErrors.forEach(symbol => {
        const itemEl = document.createElement('li');
        itemEl.textContent = symbol;
        listEl.appendChild(itemEl);
      });
      linkErrorsEl.appendChild(listEl);
      checksPanelEl.appendChild(linkErrorsEl);
    }

    document.getElementById('checks-count').textContent = checks.length;
  }

  function renderTable(searchKeyword) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    const searchTerms = searchKeyword.toLowerCase().split(/\s+/);
    const matchingRecords = filteredRecords.filter(record => {
      if (!searchKeyword) return true;
      const text = record.text.toLowerCase();
      const symbol = record.symbol.toLowerCase();
      return searchTerms.every(term => text.includes(term) || symbol.includes(term));
    });

    const captionEl = document.getElementById('table-caption');
    captionEl.textContent = `Showing ${matchingRecords.length.toLocaleString()} of ${filteredRecords.length.toLocaleString()} records`;

    // Sort by date
    const sortOrder = document.getElementById('sort-date').getAttribute('data-order') || 'desc';
    const sortedRecords = [...matchingRecords].sort((a, b) => {
      if (sortOrder === 'desc') {
        return b.date.localeCompare(a.date) || a.body.localeCompare(b.body) || compareParagraphs(a.text, b.text);
      } else {
        return a.date.localeCompare(b.date) || a.body.localeCompare(b.body) || compareParagraphs(a.text, b.text);
      }
    });

    // Show first 50
    const visibleRecords = sortedRecords.slice(0, 50);
    const loadMoreEl = document.getElementById('load-more');
    loadMoreEl.hidden = sortedRecords.length <= 50;

    visibleRecords.forEach(record => {
      const tr = document.createElement('tr');
      tr.setAttribute('tabindex', '0');
      tr.setAttribute('role', 'button');
      tr.setAttribute('aria-expanded', 'false');

      const date = new Date(record.date);
      const dateStr = date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

      const paragraphNumber = extractParagraphNumber(record.text) || '—';
      const firstLine = record.text.length > 120 ?
        record.text.slice(0, 120).replace(/\s+\S*$/, '') + '…' :
        record.text;

      // Highlight search terms
      let firstLineHighlighted = firstLine;
      if (searchKeyword) {
        searchTerms.forEach(term => {
          if (term) {
            const regex = new RegExp(escapeRegExp(term), 'gi');
            firstLineHighlighted = firstLineHighlighted.replace(regex, match => `<mark>${match}</mark>`);
          }
        });
      }

      // Extract states (UPR only)
      let stateCell = '—';
      if (record.mechanism === 'Universal Periodic Review') {
        const states = extractStates(record.text);
        stateCell = states.length ? states.join(', ') : 'State not found';
      }

      tr.innerHTML = `
        <td>${dateStr}</td>
        <td>${record.body}</td>
        <td><a href="${record.doc_url}" target="_blank">${record.symbol}</a></td>
        <td>${paragraphNumber}</td>
        <td>${firstLineHighlighted}</td>
        <td>${stateCell}</td>
      `;

      tr.addEventListener('click', () => toggleRowExpansion(tr, record));
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          toggleRowExpansion(tr, record);
        }
      });

      tbody.appendChild(tr);

      // Detail row
      const detailTr = document.createElement('tr');
      detailTr.className = 'detail';
      detailTr.hidden = true;

      const paragraphNumberLarge = extractParagraphNumber(record.text) || '(no paragraph number)';
      const citation = `${record.symbol}, para. ${paragraphNumberLarge}`;

      const themes = record.themes && record.themes.length ?
        record.themes.map(theme => `<span class="detail-label">${theme}</span>`).join('') :
        '<span class="detail-label">(no themes)</span>';
      const sdgs = record.sdgs && record.sdgs.length ?
        record.sdgs.map(sdg => `<span class="detail-label">SDG ${sdg}: ${sdgNames[sdg] || 'Unknown'}</span>`).join('') :
        '<span class="detail-label">(no SDGs)</span>';
      const targets = record.sdg_targets && record.sdg_targets.length ?
        record.sdg_targets.map(target => `<span class="detail-label">${target}</span>`).join('') :
        '<span class="detail-label">(no targets)</span>';
      const affected = record.affected_persons && record.affected_persons.length ?
        record.affected_persons.map(person => `<span class="detail-label">${person}</span>`).join('') :
        '<span class="detail-label">(no affected persons)</span>';
      const section = record.section ?
        `<span class="detail-label">${record.section}</span>` :
        '';

      detailTr.innerHTML = `
        <td colspan="6">
          <div class="detail-paragraph">${paragraphNumberLarge}</div>
          <div class="detail-text">${escapeHtml(record.text)}</div>
          <div class="detail-labels">
            ${themes}
            ${sdgs}
            ${targets}
            ${affected}
            ${section}
          </div>
          <div class="detail-actions">
            <button class="copy-citation" data-citation="${escapeHtml(citation)}">Copy citation${paragraphNumberLarge === '(no paragraph number)' ? ' (no paragraph number in this extract)' : ''}</button>
            <button class="open-document">Open the UN document</button>
            <span class="copied" hidden>Copied!</span>
          </div>
        </td>
      `;

      tbody.appendChild(detailTr);

      // Copy citation
      detailTr.querySelector('.copy-citation').addEventListener('click', (e) => {
        const button = e.target;
        const citation = button.getAttribute('data-citation');
        navigator.clipboard.writeText(citation).then(() => {
          const copiedEl = button.nextElementSibling.nextElementSibling;
          copiedEl.hidden = false;
          setTimeout(() => {
            copiedEl.hidden = true;
          }, 2000);
        });
      });

      // Open document
      detailTr.querySelector('.open-document').addEventListener('click', () => {
        window.open(record.doc_url, '_blank');
      });
    });
  }

  function toggleRowExpansion(tr, record) {
    const isExpanded = tr.getAttribute('aria-expanded') === 'true';
    tr.setAttribute('aria-expanded', !isExpanded);

    const detailTr = tr.nextElementSibling;
    detailTr.hidden = isExpanded;
  }

  function extractParagraphNumber(text) {
    const match = text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
    return match ? match[1] : null;
  }

  function extractStates(text) {
    // Match the trailing run of parenthesised groups
    const match = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
    if (!match) return [];

    const groups = match[1].match(/\((?:[^()]|\([^()]*\))*\)/g);
    if (!groups) return [];

    return groups.map(group => {
      // Remove outer parentheses and trim
      let state = group.slice(1, -1).trim();
      // Accept only if no comma and at most 60 characters
      if (state.includes(',') || state.length > 60) {
        return null;
      }
      return state;
    }).filter(state => state !== null);
  }

  function compareParagraphs(textA, textB) {
    const numA = extractParagraphNumber(textA);
    const numB = extractParagraphNumber(textB);

    if (numA === null && numB === null) return 0;
    if (numA === null) return 1;
    if (numB === null) return -1;

    // Split into parts (e.g., "144.43" -> [144, 43])
    const partsA = numA.split('.').map(Number);
    const partsB = numB.split('.').map(Number);

    for (let i = 0; i < Math.max(partsA.length, partsB.length); i++) {
      const partA = partsA[i] || 0;
      const partB = partsB[i] || 0;
      if (partA !== partB) {
        return partA - partB;
      }
    }
    return 0;
  }

  function downloadCSV() {
    const headers = [
      'Date', 'Body', 'Symbol', 'Paragraph', 'First line', 'Recommending State',
      'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Text'
    ];
    const rows = filteredRecords.map(record => {
      const date = new Date(record.date).toISOString().split('T')[0];
      const paragraph = extractParagraphNumber(record.text) || '';
      const firstLine = record.text.length > 120 ?
        record.text.slice(0, 120).replace(/\s+\S*$/, '') + '…' :
        record.text;
      const state = record.mechanism === 'Universal Periodic Review' ?
        extractStates(record.text).join(', ') :
        '';
      const themes = record.themes ? record.themes.join(' | ') : '';
      const sdgs = record.sdgs ? record.sdgs.map(s => `SDG ${s}: ${sdgNames[s] || 'Unknown'}`).join(' | ') : '';
      const targets = record.sdg_targets ? record.sdg_targets.join(' | ') : '';
      const affected = record.affected_persons ? record.affected_persons.join(' | ') : '';
      const section = record.section || '';

      return [
        `"${date}"`,
        `"${record.body}"`,
        `"${record.symbol}"`,
        `"${paragraph}"`,
        `"${firstLine.replace(/"/g, '""')}"`,
        `"${state}"`,
        `"${themes}"`,
        `"${sdgs}"`,
        `"${targets}"`,
        `"${affected}"`,
        `"${section}"`,
        `"${record.text.replace(/"/g, '""')}"`
      ].join(',');
    });

    const csv = [
      '# UN human rights recommendations and observations: Kenya',
      `# Source: ${source}`,
      `# Built: ${built}`,
      `# Filters: ${JSON.stringify(filters)}`,
      `# Records: ${filteredRecords.length}`,
      headers.join(','),
      ...rows
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `uhri-kenya-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  function copySummary() {
    const typeCounts = {};
    filteredRecords.forEach(record => {
      if (!typeCounts[record.type]) {
        typeCounts[record.type] = 0;
      }
      typeCounts[record.type]++;
    });
    const typeBreakdown = Object.entries(typeCounts)
      .sort((a, b) => b[1] - a[1])
      .map(([type, count]) => `${type.toLowerCase()} ${count}`)
      .join(', ');

    const themeCounts = new Map();
    filteredRecords.forEach(record => {
      if (record.themes && record.themes.length) {
        record.themes.forEach(theme => {
          if (!themeCounts.has(theme)) {
            themeCounts.set(theme, 0);
          }
          themeCounts.set(theme, themeCounts.get(theme) + 1);
        });
      }
    });
    const topThemes = Array.from(themeCounts.entries())
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10)
      .map(([theme, count]) => `${theme} (${count})`)
      .join(', ');

    const summary = `UN human rights recommendations and observations: Kenya
${filteredRecords.length.toLocaleString()} records (${typeBreakdown}), ${new Set(filteredRecords.map(r => r.symbol)).size} documents, ${Math.min(...filteredRecords.map(r => r.year))}–${Math.max(...filteredRecords.map(r => r.year))}
Top themes: ${topThemes}
Source: ${source} (${built})`;

    navigator.clipboard.writeText(summary).then(() => {
      const button = document.getElementById('copy-summary');
      const originalText = button.textContent;
      button.textContent = 'Copied!';
      setTimeout(() => {
        button.textContent = originalText;
      }, 2000);
    });
  }

  function switchTab(tab) {
    document.querySelectorAll('[role="tabpanel"]').forEach(panel => {
      panel.hidden = true;
    });
    document.getElementById(`panel-${tab}`).hidden = false;

    document.querySelectorAll('[role="tab"]').forEach(tabEl => {
      tabEl.setAttribute('aria-selected', 'false');
    });
    document.getElementById(`tab-${tab}`).setAttribute('aria-selected', 'true');

    // Adjust rail visibility
    const rail = document.getElementById('rail');
    if (tab === '03') {
      rail.style.display = 'none';
      document.querySelector('main').style.maxWidth = '100%';
    } else {
      rail.style.display = 'block';
      document.querySelector('main').style.maxWidth = 'calc(100vw - 220px)';
    }
  }

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function escapeHtml(unsafe) {
    return unsafe
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  init();
});
</script>
</body>
</html>
```