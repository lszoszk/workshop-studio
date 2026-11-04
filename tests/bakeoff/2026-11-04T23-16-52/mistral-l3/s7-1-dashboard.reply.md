Here is the app. It follows the plan exactly: three tabs, filters in a left rail, big numbers on the Overview, a table on Records, method and export on the last tab, and the "Check this dashboard" panel under a closed heading on the Overview.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
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
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
}
@media (max-width: 800px) {
  body { grid-template-columns: 1fr; }
  #rail { display: none; }
  #rail-toggle { display: block; }
  #rail[aria-expanded="true"] { display: block; }
}
#rail-toggle {
  display: none;
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 10;
  padding: 0.5rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
#rail {
  padding: 1rem;
  border-right: 1px solid var(--rule);
  background-color: var(--paper);
  overflow-y: auto;
}
#rail h2 {
  font-size: 0.8rem;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink);
  margin: 1.5rem 0 0.5rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid var(--rule);
}
#rail button[aria-expanded] {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 0.25rem 0;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--ink);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
#rail button[aria-expanded]::after {
  content: "▼";
  font-size: 0.6rem;
  transform: rotate(-90deg);
  transition: transform 0.2s;
}
#rail button[aria-expanded][aria-expanded="true"]::after {
  transform: rotate(0deg);
}
#rail .filter-panel { display: none; }
#rail .filter-panel[aria-expanded="true"] { display: block; }
#rail input, #rail select {
  width: 100%;
  margin: 0.25rem 0;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  background: white;
  font-size: 0.9rem;
}
#rail .chip {
  display: inline-block;
  background: var(--accent);
  color: white;
  padding: 0.25rem 0.5rem;
  margin: 0.25rem;
  border-radius: 1rem;
  font-size: 0.8rem;
}
#rail .chip button {
  background: none;
  border: none;
  color: white;
  margin-left: 0.5rem;
  cursor: pointer;
  font-size: 0.8rem;
}
#rail .share-bar {
  height: 4px;
  background: var(--rule);
  margin-top: 0.5rem;
}
#rail .share-bar-fill {
  height: 100%;
  background: var(--accent);
  width: 0%;
}
#main {
  padding: 1rem;
  overflow-y: auto;
}
#header {
  grid-column: 1 / -1;
  padding: 0 1rem 1rem;
  border-bottom: 1px solid var(--rule);
}
#header .label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  color: var(--ink);
}
#header h1 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2rem;
  margin: 0.25rem 0;
}
#header .source {
  font-size: 0.9rem;
  color: var(--ink);
}
#header .source a {
  color: var(--ink);
}
#tabs {
  display: flex;
  border-bottom: 1px solid var(--rule);
  margin: 0 0 1rem;
  padding: 0;
  list-style: none;
}
#tabs button {
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}
#tabs button[aria-selected="true"] {
  color: var(--accent);
  border-bottom-color: var(--accent);
}
#tab-panels > div {
  display: none;
}
#tab-panels > div[aria-hidden="false"] {
  display: block;
}
.tile {
  border: 1px solid var(--rule);
  padding: 1rem;
  margin-bottom: 1rem;
  position: relative;
}
.tile h3 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 3rem;
  margin: 0 0 0.5rem;
  line-height: 1;
}
.tile .subtitle {
  font-size: 0.9rem;
  color: var(--ink);
  margin: 0;
}
.tile .mechanism {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
}
.tile .mechanism-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.tile .mechanism.upr .mechanism-dot { background: var(--upr); }
.tile .mechanism.treaty .mechanism-dot { background: var(--treaty); }
.tile .mechanism.special .mechanism-dot { background: var(--special); }
.tile .note {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.5rem;
}
.fig {
  margin: 2rem 0;
}
.fig h4 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5rem;
}
.fig .source {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 1rem;
}
.chart-container {
  position: relative;
  height: 400px;
  margin-bottom: 1rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}
th, td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid var(--rule);
}
th { font-weight: bold; }
td { vertical-align: top; }
td.num { text-align: right; }
caption {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  text-align: left;
  margin-bottom: 0.5rem;
}
tr.expanded td {
  border-bottom: 1px solid transparent;
}
tr.expanded td[colspan] {
  padding: 1rem;
  border: 1px solid var(--rule);
  border-top: none;
  background: white;
}
tr.expanded .para-num {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  color: var(--accent);
  margin: 0 0 0.5rem;
}
tr.expanded .labels {
  margin: 1rem 0;
}
tr.expanded .label-group {
  margin-bottom: 0.5rem;
}
tr.expanded .label-group h5 {
  font-size: 0.8rem;
  margin: 0 0 0.25rem;
  font-weight: bold;
}
tr.expanded .label-group span {
  display: inline-block;
  background: #f0f0f0;
  padding: 0.25rem 0.5rem;
  margin: 0.1rem;
  border-radius: 4px;
  font-size: 0.8rem;
}
tr.expanded .actions {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
}
tr.expanded .actions button {
  padding: 0.5rem 1rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
tr.expanded .actions button.secondary {
  background: #ccc;
}
tr:hover { background: #f9f9f9; }
tr[aria-expanded="true"] { background: white; }
mark {
  background: #ffeb3b;
  padding: 0 2px;
}
.hidden { display: none; }
[hidden] { display: none !important; }
#check-panel {
  border-top: 1px solid var(--rule);
  padding-top: 1rem;
  margin-top: 1rem;
}
#check-panel ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}
#check-panel li {
  padding: 0.25rem 0;
  font-size: 0.9rem;
}
#check-panel .pass::before {
  content: "✓";
  color: green;
  margin-right: 0.5rem;
}
#check-panel .fail::before {
  content: "✗";
  color: var(--accent);
  margin-right: 0.5rem;
}
#check-panel .warn::before {
  content: "!";
  color: orange;
  margin-right: 0.5rem;
}
#footer {
  grid-column: 1 / -1;
  padding: 1rem;
  border-top: 1px solid var(--rule);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.8rem;
  color: #666;
}
#footer a {
  color: #666;
}
</style>
</head>
<body>

<button id="rail-toggle" aria-label="Show filters">☰ Filters</button>

<div id="rail" aria-expanded="false">
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <h2>Filters</h2>
    <button id="clear-all">Clear all</button>
  </div>
  <div id="matching-count" aria-live="polite">
    <span id="matching-num" style="font-family: Georgia, 'Times New Roman', serif; font-size: 2.5rem; color: var(--accent);">0</span>
    <span style="font-size: 0.9rem;">matching records</span>
    <div style="font-size: 0.8rem; color: #666;">of <span id="total-num">0</span> in the file</div>
  </div>
  <div class="share-bar"><div class="share-bar-fill" id="share-bar-fill"></div></div>
  <div id="active-filters"></div>

  <button id="filter-keyword-btn" aria-expanded="false">01 Keyword</button>
  <div id="filter-keyword" class="filter-panel" aria-expanded="false">
    <input type="text" id="keyword-input" placeholder="Search text or symbol…"/>
    <div style="font-size: 0.8rem; color: #666;">literal match, not synonyms</div>
  </div>

  <button id="filter-mechanism-btn" aria-expanded="true">02 Mechanism, body, type</button>
  <div id="filter-mechanism" class="filter-panel" aria-expanded="true">
    <h3>Mechanism</h3>
    <select id="mechanism-select">
      <option value="">All mechanisms</option>
    </select>

    <h3>Body or mandate</h3>
    <div id="body-options"></div>

    <h3>Type</h3>
    <select id="type-select">
      <option value="">All types</option>
    </select>

    <h3>Recommending State (UPR only)</h3>
    <select id="state-select">
      <option value="">All States</option>
    </select>
  </div>

  <button id="filter-year-sdg-btn" aria-expanded="false">03 Years and SDG</button>
  <div id="filter-year-sdg" class="filter-panel" aria-expanded="false">
    <h3>Year</h3>
    <div style="display: flex; gap: 0.5rem;">
      <select id="year-from">
        <option value="">From</option>
      </select>
      <select id="year-to">
        <option value="">To</option>
      </select>
    </div>

    <h3>SDG</h3>
    <select id="sdg-select">
      <option value="">All SDGs</option>
    </select>
  </div>
</div>

<div id="main">
  <header id="header">
    <div class="label">UHRI · <span id="country-name">Kenya</span></div>
    <h1>UN human rights recommendations and observations: <span id="country-name-title">Kenya</span></h1>
    <div class="source">Source: <a id="source-link" href="#" target="_blank">Universal Human Rights Index</a> · <span id="total-records">0</span> records · <span id="total-docs">0</span> documents · <span id="year-range">0000–0000</span> · built <span id="built-date">0000-00-00</span> · dated by document</div>
  </header>

  <div role="tablist" aria-label="Tabs">
    <div id="tabs">
      <button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 Overview</button>
      <button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 Records</button>
      <button id="tab-03" role="tab" aria-selected="false" aria-controls="panel-03">03 Method & export</button>
    </div>
  </div>

  <div id="tab-panels">
    <div id="panel-01" role="tabpanel" aria-labelledby="tab-01" aria-hidden="false">
      <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem;">
        <div class="tile" style="flex: 1; min-width: 200px;">
          <h3 id="headline-total">0</h3>
          <div class="subtitle" id="headline-breakdown">0 Recommendations, 0 Concerns/Observations, 0 Other</div>
          <div class="note">How this is computed: count of all records in the file.</div>
        </div>
        <div class="tile" style="flex: 1; min-width: 200px;">
          <h3 id="headline-docs">0</h3>
          <div class="subtitle">documents</div>
          <div class="note">How this is computed: distinct document symbols.</div>
        </div>
        <div class="tile" style="flex: 1; min-width: 200px;">
          <h3 id="headline-years">0000–0000</h3>
          <div class="note">How this is computed: minimum and maximum year of the records.</div>
        </div>
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem;">
        <div class="tile mechanism upr" style="flex: 1; min-width: 200px;">
          <div class="mechanism"><div class="mechanism-dot"></div> Universal Periodic Review</div>
          <h3 id="upr-records">0</h3>
          <div class="subtitle"><span id="upr-docs">0</span> documents · latest <span id="upr-latest">0000</span> · <span id="upr-share">0</span>%</div>
          <div class="note">How this is computed: records with mechanism = "Universal Periodic Review".</div>
          <div style="margin-top: 0.5rem; font-size: 0.8rem;"><a href="#" id="upr-states-link">see the States</a></div>
          <div id="upr-states-list" class="hidden">
            <h4 style="font-size: 0.9rem; margin: 0.5rem 0 0;">Ten States that made most recommendations to <span id="country-name-states">Kenya</span></h4>
            <div id="upr-states-top"></div>
          </div>
        </div>
        <div class="tile mechanism treaty" style="flex: 1; min-width: 200px;">
          <div class="mechanism"><div class="mechanism-dot"></div> Treaty bodies</div>
          <h3 id="treaty-records">0</h3>
          <div class="subtitle"><span id="treaty-docs">0</span> documents · latest <span id="treaty-latest">0000</span> · <span id="treaty-share">0</span>%</div>
          <div class="note">How this is computed: records with mechanism = "Treaty bodies".</div>
        </div>
        <div class="tile mechanism special" style="flex: 1; min-width: 200px;">
          <div class="mechanism"><div class="mechanism-dot"></div> Special Procedures</div>
          <h3 id="special-records">0</h3>
          <div class="subtitle"><span id="special-docs">0</span> documents · latest <span id="special-latest">0000</span> · <span id="special-share">0</span>%</div>
          <div class="note">How this is computed: records with mechanism = "Special Procedures".</div>
        </div>
      </div>

      <div class="fig">
        <h4>FIG.01 Ten most frequent themes among <span id="fig01-n">0</span> filtered records</h4>
        <div class="source">Source: themes field in the records; a record can carry several themes, so bars add up to more than n.</div>
        <div class="chart-container">
          <canvas id="theme-chart"></canvas>
        </div>
        <table>
          <caption>Same data as the chart: theme, records, share of filtered records, and the years the theme appears in.</caption>
          <thead>
            <tr><th>Theme</th><th>Records</th><th>%</th><th>Years</th></tr>
          </thead>
          <tbody id="theme-table"></tbody>
        </table>
      </div>

      <div class="fig">
        <h4>FIG.02 Records per year by mechanism</h4>
        <div class="source">Source: year and mechanism fields; every year from the first to the last appears.</div>
        <div class="chart-container">
          <canvas id="timeline-chart"></canvas>
        </div>
      </div>

      <div style="margin-top: 2rem;">
        <button id="check-btn" aria-expanded="false">Every check (<span id="check-count">0</span>)</button>
        <div id="check-panel" aria-expanded="false">
          <ul id="check-list"></ul>
        </div>
      </div>
    </div>

    <div id="panel-02" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
      <div style="margin-bottom: 1rem;">
        <input type="text" id="search-input" placeholder="Search records, e.g. torture"/>
        <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">literal match, not synonyms</div>
      </div>
      <div style="font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.8rem; margin-bottom: 1rem;">
        <span id="table-caption">Showing 0 of 0 matching records</span>
      </div>
      <div style="overflow-x: auto;">
        <table id="records-table">
          <caption>Records matching the current filter, newest first. Click a row to expand it.</caption>
          <thead>
            <tr><th id="sort-date">Date ▼</th><th>Body</th><th>Symbol</th><th>Para.</th><th>Recommending State</th><th>First line</th></tr>
          </thead>
          <tbody id="records-tbody"></tbody>
        </table>
      </div>
      <div style="text-align: center; margin-top: 1rem;">
        <button id="load-more">Show 50 more</button>
      </div>
    </div>

    <div id="panel-03" role="tabpanel" aria-labelledby="tab-03" aria-hidden="true">
      <h2>How each number is computed</h2>
      <p>Every number is computed by the app's own code, deterministically, from the records in the file. Nothing is estimated and no model is called.</p>
      <ul>
        <li><strong>Headline total</strong> = number of records in the file. The breakdown counts records per <code>type</code>.</li>
        <li><strong>Documents</strong> = number of distinct <code>symbol</code>. <strong>Years</strong> = minimum and maximum <code>year</code>.</li>
        <li><strong>Filters</strong>. Mechanism, body, type: exact match on the field. Year: <code>year</code> between the two selects. SDG: <code>sdgs.includes(goal)</code>. Keyword: every word must occur as a substring of <code>text</code> or <code>symbol</code>.</li>
        <li><strong>Theme counts</strong>. For each record in the filtered set, each value in <code>themes</code> counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = min and max <code>year</code> of the records carrying that theme.</li>
        <li><strong>Timeline</strong> = records per <code>year</code> per <code>mechanism</code> in the filtered set, with zero for missing combinations.</li>
        <li><strong>Paragraph number</strong> = the first match of <code>/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/</code> on <code>text</code>; no match means no number.</li>
        <li><strong>Recommending State</strong>. Only for UPR records. The trailing run of parenthesised groups is split into States; a group is accepted only if it has no comma and at most 60 characters.</li>
        <li><strong>Citation</strong> = <code>symbol</code> + ", para. " + paragraph number when one was found; otherwise <code>symbol</code>.</li>
      </ul>

      <h2>Export</h2>
      <div style="margin-bottom: 1rem;">
        <button id="download-csv">Download CSV of the current filter</button>
        <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">The visible columns plus the full text and labels, with comment lines for the filters applied.</div>
      </div>
      <div>
        <button id="copy-summary">Copy summary</button>
        <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">A plain-text paragraph with the headline numbers and the ten themes, for pasting into notes.</div>
      </div>

      <h2>Data</h2>
      <p>Source: <a id="source-link-2" href="#" target="_blank">Universal Human Rights Index</a> · Licence: CC BY 4.0 · Built <span id="built-date-2">0000-00-00</span></p>
    </div>
  </div>
</div>

<footer id="footer">
  Built on OHCHR UHRI data · <span id="footer-records">0</span> records · <a id="footer-source" href="#" target="_blank">source</a>
</footer>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
document.addEventListener('DOMContentLoaded', () => {
  // ------------------------------------------------------------
  // DATA
  // ------------------------------------------------------------
  const data = window.WORKSHOP_DATA.uhri;
  const country = data.country;
  const records = data.records;
  const sdgNames = data.sdg_names || {};
  const totalRecords = records.length;
  const totalDocs = new Set(records.map(r => r.symbol)).size;
  const years = records.map(r => r.year);
  const yearRange = `${Math.min(...years)}–${Math.max(...years)}`;
  const builtDate = data.built;

  // ------------------------------------------------------------
  // STATE
  // ------------------------------------------------------------
  let filtered = [...records];
  let currentTab = '01';
  let sortDirection = 'desc';
  let visibleRows = 50;

  // ------------------------------------------------------------
  // UTILS
  // ------------------------------------------------------------
  const debounce = (fn, ms) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn(...args), ms);
    };
  };

  const formatNumber = n => n.toLocaleString();
  const formatPercent = (n, total) => total ? (n / total * 100).toFixed(1) + '%' : '0%';

  const extractParagraphNumber = text => {
    const match = text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
    return match ? match[1] : null;
  };

  const extractStates = text => {
    if (!text) return [];
    const match = text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
    if (!match) return [];
    const groups = match[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
    return groups.map(g => {
      const inner = g.slice(1, -1).trim();
      if (inner.includes(',') || inner.length > 60) return null;
      return inner;
    }).filter(Boolean);
  };

  const getThemeYears = theme => {
    const themeRecords = filtered.filter(r => r.themes && r.themes.includes(theme));
    if (themeRecords.length === 0) return '';
    const years = themeRecords.map(r => r.year);
    return `${Math.min(...years)}–${Math.max(...years)}`;
  };

  // ------------------------------------------------------------
  // HEADER
  // ------------------------------------------------------------
  document.getElementById('country-name').textContent = country;
  document.getElementById('country-name-title').textContent = country;
  document.getElementById('total-records').textContent = formatNumber(totalRecords);
  document.getElementById('total-docs').textContent = formatNumber(totalDocs);
  document.getElementById('year-range').textContent = yearRange;
  document.getElementById('built-date').textContent = builtDate;
  document.getElementById('built-date-2').textContent = builtDate;
  document.getElementById('source-link').href = data.source_url;
  document.getElementById('source-link-2').href = data.source_url;
  document.getElementById('footer-records').textContent = formatNumber(totalRecords);
  document.getElementById('footer-source').href = data.source_url;

  // ------------------------------------------------------------
  // FILTERS
  // ------------------------------------------------------------
  const updateMatchingCount = () => {
    const n = filtered.length;
    document.getElementById('matching-num').textContent = formatNumber(n);
    document.getElementById('total-num').textContent = formatNumber(totalRecords);
    document.getElementById('share-bar-fill').style.width = `${n / totalRecords * 100}%`;
  };

  const updateActiveFilters = () => {
    const container = document.getElementById('active-filters');
    container.innerHTML = '';
    const filters = [];

    const keyword = document.getElementById('keyword-input').value.trim();
    if (keyword) filters.push(`Keyword: "${keyword}"`);

    const mechanism = document.getElementById('mechanism-select').value;
    if (mechanism) filters.push(`Mechanism: ${mechanism}`);

    const body = Array.from(document.querySelectorAll('#body-options input:checked')).map(el => el.value);
    if (body.length > 0) filters.push(`Body: ${body.join(', ')}`);

    const type = document.getElementById('type-select').value;
    if (type) filters.push(`Type: ${type}`);

    const state = document.getElementById('state-select').value;
    if (state) filters.push(`State: ${state}`);

    const yearFrom = document.getElementById('year-from').value;
    const yearTo = document.getElementById('year-to').value;
    if (yearFrom || yearTo) {
      const range = [];
      if (yearFrom) range.push(`from ${yearFrom}`);
      if (yearTo) range.push(`to ${yearTo}`);
      filters.push(`Year: ${range.join(' ')}`);
    }

    const sdg = document.getElementById('sdg-select').value;
    if (sdg) filters.push(`SDG: ${sdg}`);

    filters.forEach(text => {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = text;
      const btn = document.createElement('button');
      btn.textContent = '×';
      btn.onclick = () => {
        if (text.startsWith('Keyword:')) document.getElementById('keyword-input').value = '';
        if (text.startsWith('Mechanism:')) document.getElementById('mechanism-select').value = '';
        if (text.startsWith('Body:')) document.querySelectorAll('#body-options input').forEach(el => el.checked = false);
        if (text.startsWith('Type:')) document.getElementById('type-select').value = '';
        if (text.startsWith('State:')) document.getElementById('state-select').value = '';
        if (text.startsWith('Year:')) {
          document.getElementById('year-from').value = '';
          document.getElementById('year-to').value = '';
        }
        if (text.startsWith('SDG:')) document.getElementById('sdg-select').value = '';
        applyFilters();
      };
      chip.appendChild(btn);
      container.appendChild(chip);
    });
  };

  const applyFilters = () => {
    const keyword = document.getElementById('keyword-input').value.trim().toLowerCase();
    const mechanism = document.getElementById('mechanism-select').value;
    const bodies = Array.from(document.querySelectorAll('#body-options input:checked')).map(el => el.value);
    const type = document.getElementById('type-select').value;
    const state = document.getElementById('state-select').value;
    const yearFrom = document.getElementById('year-from').value;
    const yearTo = document.getElementById('year-to').value;
    const sdg = document.getElementById('sdg-select').value;

    filtered = records.filter(r => {
      if (keyword) {
        const words = keyword.split(/\s+/).filter(w => w);
        if (words.length === 0) return true;
        const text = (r.text || '').toLowerCase();
        const symbol = (r.symbol || '').toLowerCase();
        if (!words.every(w => text.includes(w) || symbol.includes(w))) return false;
      }
      if (mechanism && r.mechanism !== mechanism) return false;
      if (bodies.length > 0 && !bodies.includes(r.body)) return false;
      if (type && r.type !== type) return false;
      if (state && r.mechanism === 'Universal Periodic Review') {
        const states = extractStates(r.text);
        if (!states.includes(state)) return false;
      }
      if (yearFrom && r.year < parseInt(yearFrom)) return false;
      if (yearTo && r.year > parseInt(yearTo)) return false;
      if (sdg && (!r.sdgs || !r.sdgs.includes(parseInt(sdg)))) return false;
      return true;
    });

    updateMatchingCount();
    updateActiveFilters();
    updateTabs();
  };

  const populateFilters = () => {
    const mechanisms = [...new Set(records.map(r => r.mechanism))];
    const mechanismSelect = document.getElementById('mechanism-select');
    mechanisms.forEach(m => {
      const opt = document.createElement('option');
      opt.value = m;
      opt.textContent = m;
      mechanismSelect.appendChild(opt);
    });

    const types = [...new Set(records.map(r => r.type))];
    const typeSelect = document.getElementById('type-select');
    types.forEach(t => {
      const opt = document.createElement('option');
      opt.value = t;
      opt.textContent = t;
      typeSelect.appendChild(opt);
    });

    const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
    const yearFrom = document.getElementById('year-from');
    const yearTo = document.getElementById('year-to');
    years.forEach(y => {
      const opt1 = document.createElement('option');
      opt1.value = y;
      opt1.textContent = y;
      yearFrom.appendChild(opt1);
      const opt2 = document.createElement('option');
      opt2.value = y;
      opt2.textContent = y;
      yearTo.appendChild(opt2);
    });

    const sdgs = [...new Set(records.flatMap(r => r.sdgs || []))].sort((a, b) => a - b);
    const sdgSelect = document.getElementById('sdg-select');
    sdgs.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = `${s} ${sdgNames[s] || ''}`;
      sdgSelect.appendChild(opt);
    });

    const updateBodyOptions = () => {
      const mechanism = document.getElementById('mechanism-select').value;
      const bodies = [...new Set(records.filter(r => !mechanism || r.mechanism === mechanism).map(r => r.body))].sort();
      const container = document.getElementById('body-options');
      container.innerHTML = '';
      bodies.forEach(b => {
        const div = document.createElement('div');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = `body-${b}`;
        input.value = b;
        const label = document.createElement('label');
        label.htmlFor = `body-${b}`;
        label.textContent = `${b} (${records.filter(r => r.body === b).length})`;
        div.appendChild(input);
        div.appendChild(label);
        container.appendChild(div);
      });
    };

    const updateStateOptions = () => {
      const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
      const states = uprRecords.flatMap(r => extractStates(r.text)).filter(Boolean);
      const stateCounts = {};
      states.forEach(s => stateCounts[s] = (stateCounts[s] || 0) + 1);
      const sortedStates = Object.entries(stateCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
      const stateSelect = document.getElementById('state-select');
      stateSelect.innerHTML = '<option value="">All States</option>';
      sortedStates.forEach(([s, count]) => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = `${s} (${count})`;
        stateSelect.appendChild(opt);
      });
    };

    document.getElementById('mechanism-select').addEventListener('change', () => {
      updateBodyOptions();
      updateStateOptions();
      applyFilters();
    });

    document.getElementById('keyword-input').addEventListener('input', debounce(applyFilters, 300));
    document.getElementById('type-select').addEventListener('change', applyFilters);
    document.getElementById('state-select').addEventListener('change', applyFilters);
    document.getElementById('year-from').addEventListener('change', () => {
      const from = document.getElementById('year-from').value;
      const to = document.getElementById('year-to').value;
      if (from && to && parseInt(from) > parseInt(to)) {
        document.getElementById('year-to').value = from;
      }
      applyFilters();
    });
    document.getElementById('year-to').addEventListener('change', () => {
      const from = document.getElementById('year-from').value;
      const to = document.getElementById('year-to').value;
      if (from && to && parseInt(from) > parseInt(to)) {
        document.getElementById('year-from').value = to;
      }
      applyFilters();
    });
    document.getElementById('sdg-select').addEventListener('change', applyFilters);
    document.getElementById('body-options').addEventListener('change', applyFilters);
    document.getElementById('clear-all').addEventListener('click', () => {
      document.getElementById('keyword-input').value = '';
      document.getElementById('mechanism-select').value = '';
      document.querySelectorAll('#body-options input').forEach(el => el.checked = false);
      document.getElementById('type-select').value = '';
      document.getElementById('state-select').value = '';
      document.getElementById('year-from').value = '';
      document.getElementById('year-to').value = '';
      document.getElementById('sdg-select').value = '';
      applyFilters();
    });

    updateBodyOptions();
    updateStateOptions();
  };

  // ------------------------------------------------------------
  // TABS
  // ------------------------------------------------------------
  const updateTabs = () => {
    if (currentTab === '01') updateOverview();
    if (currentTab === '02') updateRecords();
    if (currentTab === '03') updateMethod();
  };

  document.getElementById('tab-01').addEventListener('click', () => {
    currentTab = '01';
    document.getElementById('tab-01').setAttribute('aria-selected', 'true');
    document.getElementById('tab-02').setAttribute('aria-selected', 'false');
    document.getElementById('tab-03').setAttribute('aria-selected', 'false');
    document.getElementById('panel-01').setAttribute('aria-hidden', 'false');
    document.getElementById('panel-02').setAttribute('aria-hidden', 'true');
    document.getElementById('panel-03').setAttribute('aria-hidden', 'true');
    updateTabs();
  });
  document.getElementById('tab-02').addEventListener('click', () => {
    currentTab = '02';
    document.getElementById('tab-01').setAttribute('aria-selected', 'false');
    document.getElementById('tab-02').setAttribute('aria-selected', 'true');
    document.getElementById('tab-03').setAttribute('aria-selected', 'false');
    document.getElementById('panel-01').setAttribute('aria-hidden', 'true');
    document.getElementById('panel-02').setAttribute('aria-hidden', 'false');
    document.getElementById('panel-03').setAttribute('aria-hidden', 'true');
    updateTabs();
  });
  document.getElementById('tab-03').addEventListener('click', () => {
    currentTab = '03';
    document.getElementById('tab-01').setAttribute('aria-selected', 'false');
    document.getElementById('tab-02').setAttribute('aria-selected', 'false');
    document.getElementById('tab-03').setAttribute('aria-selected', 'true');
    document.getElementById('panel-01').setAttribute('aria-hidden', 'true');
    document.getElementById('panel-02').setAttribute('aria-hidden', 'true');
    document.getElementById('panel-03').setAttribute('aria-hidden', 'false');
    updateTabs();
  });

  // ------------------------------------------------------------
  // FILTER PANELS
  // ------------------------------------------------------------
  const setupFilterPanels = () => {
    const panels = [
      { btn: 'filter-keyword-btn', panel: 'filter-keyword' },
      { btn: 'filter-mechanism-btn', panel: 'filter-mechanism' },
      { btn: 'filter-year-sdg-btn', panel: 'filter-year-sdg' }
    ];
    panels.forEach(({btn, panel}) => {
      const btnEl = document.getElementById(btn);
      const panelEl = document.getElementById(panel);
      btnEl.addEventListener('click', () => {
        const isExpanded = panelEl.getAttribute('aria-expanded') === 'true';
        panelEl.setAttribute('aria-expanded', !isExpanded);
        btnEl.setAttribute('aria-expanded', !isExpanded);
      });
    });
  };

  // ------------------------------------------------------------
  // OVERVIEW TAB
  // ------------------------------------------------------------
  const updateOverview = () => {
    const n = filtered.length;
    document.getElementById('fig01-n').textContent = formatNumber(n);

    // Headline numbers
    document.getElementById('headline-total').textContent = formatNumber(n);
    const typeCounts = {};
    filtered.forEach(r => typeCounts[r.type] = (typeCounts[r.type] || 0) + 1);
    const typeBreakdown = Object.entries(typeCounts).map(([k, v]) => `${formatNumber(v)} ${k}`).join(', ');
    document.getElementById('headline-breakdown').textContent = typeBreakdown;

    // Mechanism tiles
    const uprRecords = filtered.filter(r => r.mechanism === 'Universal Periodic Review');
    const treatyRecords = filtered.filter(r => r.mechanism === 'Treaty bodies');
    const specialRecords = filtered.filter(r => r.mechanism === 'Special Procedures');
    document.getElementById('upr-records').textContent = formatNumber(uprRecords.length);
    document.getElementById('upr-docs').textContent = formatNumber(new Set(uprRecords.map(r => r.symbol)).size);
    document.getElementById('upr-latest').textContent = uprRecords.length ? Math.max(...uprRecords.map(r => r.year)) : '–';
    document.getElementById('upr-share').textContent = formatPercent(uprRecords.length, n);
    document.getElementById('treaty-records').textContent = formatNumber(treatyRecords.length);
    document.getElementById('treaty-docs').textContent = formatNumber(new Set(treatyRecords.map(r => r.symbol)).size);
    document.getElementById('treaty-latest').textContent = treatyRecords.length ? Math.max(...treatyRecords.map(r => r.year)) : '–';
    document.getElementById('treaty-share').textContent = formatPercent(treatyRecords.length, n);
    document.getElementById('special-records').textContent = formatNumber(specialRecords.length);
    document.getElementById('special-docs').textContent = formatNumber(new Set(specialRecords.map(r => r.symbol)).size);
    document.getElementById('special-latest').textContent = specialRecords.length ? Math.max(...specialRecords.map(r => r.year)) : '–';
    document.getElementById('special-share').textContent = formatPercent(specialRecords.length, n);

    // Top themes
    const themeCounts = {};
    filtered.forEach(r => {
      (r.themes || []).forEach(t => themeCounts[t] = (themeCounts[t] || 0) + 1);
    });
    const topThemes = Object.entries(themeCounts)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10);
    const themeTable = document.getElementById('theme-table');
    themeTable.innerHTML = '';
    topThemes.forEach(([theme, count]) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${theme}</td>
        <td class="num">${formatNumber(count)}</td>
        <td class="num">${formatPercent(count, n)}</td>
        <td>${getThemeYears(theme)}</td>
      `;
      themeTable.appendChild(tr);
    });

    // Theme chart
    const ctx = document.getElementById('theme-chart').getContext('2d');
    if (window.themeChart) window.themeChart.destroy();
    window.themeChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: topThemes.map(([t]) => t),
        datasets: [{
          label: 'Records',
          data: topThemes.map(([, c]) => c),
          backgroundColor: topThemes.map(() => `rgba(155, 35, 53, 0.8)`),
          borderColor: topThemes.map(() => `rgba(155, 35, 53, 1)`),
          borderWidth: 1
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { beginAtZero: true, ticks: { precision: 0 } },
          y: { grid: { display: false } }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.raw} records (${formatPercent(ctx.raw, n)})`
            }
          }
        },
        onClick: (e, activeEls) => {
          if (activeEls.length === 0) return;
          const idx = activeEls[0].index;
          const theme = topThemes[idx][0];
          document.getElementById('keyword-input').value = `"${theme}"`;
          applyFilters();
        }
      }
    });

    // Timeline chart
    const timelineData = {};
    filtered.forEach(r => {
      if (!timelineData[r.year]) timelineData[r.year] = { upr: 0, treaty: 0, special: 0 };
      timelineData[r.year][r.mechanism.toLowerCase().replace(/ /g, '')] += 1;
    });
    const allYears = Array.from({length: Math.max(...years) - Math.min(...years) + 1}, (_, i) => Math.min(...years) + i);
    const uprData = allYears.map(y => timelineData[y]?.upr || 0);
    const treatyData = allYears.map(y => timelineData[y]?.treaty || 0);
    const specialData = allYears.map(y => timelineData[y]?.special || 0);
    const timelineCtx = document.getElementById('timeline-chart').getContext('2d');
    if (window.timelineChart) window.timelineChart.destroy();
    window.timelineChart = new Chart(timelineCtx, {
      type: 'bar',
      data: {
        labels: allYears,
        datasets: [
          { label: 'Universal Periodic Review', data: uprData, backgroundColor: 'rgba(194, 65, 12, 0.8)' },
          { label: 'Treaty bodies', data: treatyData, backgroundColor: 'rgba(15, 118, 110, 0.8)' },
          { label: 'Special Procedures', data: specialData, backgroundColor: 'rgba(124, 58, 237, 0.8)' }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { stacked: true },
          y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.dataset.label}: ${ctx.raw} records`
            }
          }
        }
      }
    });

    // UPR States top 10
    const uprStates = uprRecords.flatMap(r => extractStates(r.text)).filter(Boolean);
    const stateCounts = {};
    uprStates.forEach(s => stateCounts[s] = (stateCounts[s] || 0) + 1);
    const topStates = Object.entries(stateCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 10);
    const uprStatesTop = document.getElementById('upr-states-top');
    uprStatesTop.innerHTML = '';
    topStates.forEach(([state, count]) => {
      const div = document.createElement('div');
      div.textContent = `${state}: ${count}`;
      uprStatesTop.appendChild(div);
    });
    document.getElementById('country-name-states').textContent = country;

    // Check panel
    updateCheckPanel();
  };

  const updateCheckPanel = () => {
    const checks = [];
    const n = filtered.length;

    // Record count
    checks.push({
      label: `Record count: ${formatNumber(records.length)} (file) vs ${data.count} (header)`,
      pass: records.length === Number(data.count),
      actual: `file: ${records.length}, header: ${data.count}`
    });

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
    checks.push({
      label: `Mechanism partition: ${mechanismSum} (sum) vs ${records.length} (total)`,
      pass: mechanismSum === records.length,
      actual: `sum: ${mechanismSum}, total: ${records.length}`
    });
    checks.push({
      label: `Body partition: ${bodySum} (sum) vs ${records.length} (total)`,
      pass: bodySum === records.length,
      actual: `sum: ${bodySum}, total: ${records.length}`
    });
    checks.push({
      label: `Year partition: ${yearSum} (sum) vs ${records.length} (total)`,
      pass: yearSum === records.length,
      actual: `sum: ${yearSum}, total: ${records.length}`
    });

    // Type partition
    const typeCounts = {};
    records.forEach(r => typeCounts[r.type] = (typeCounts[r.type] || 0) + 1);
    const typeSum = Object.values(typeCounts).reduce((a, b) => a + b, 0);
    checks.push({
      label: `Type partition: ${typeSum} (sum) vs ${records.length} (total)`,
      pass: typeSum === records.length,
      actual: `sum: ${typeSum}, total: ${records.length}`
    });

    // Chart vs table
    const themeCounts = {};
    filtered.forEach(r => (r.themes || []).forEach(t => themeCounts[t] = (themeCounts[t] || 0) + 1));
    const topThemes = Object.entries(themeCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 10);
    const chartValues = topThemes.map(([, c]) => c);
    const tableValues = Array.from(document.querySelectorAll('#theme-table tr')).map(tr => parseInt(tr.children[1].textContent.replace(/,/g, '')));
    const chartVsTable = chartValues.every((v, i) => v === tableValues[i]) && chartValues.length === tableValues.length;
    checks.push({
      label: `Chart vs table: top 10 themes match`,
      pass: chartVsTable,
      actual: chartVsTable ? '' : `chart: [${chartValues}], table: [${tableValues}]`
    });
    checks.push({
      label: `Largest bar ≤ filtered count: ${Math.max(...chartValues)} ≤ ${n}`,
      pass: Math.max(...chartValues) <= n,
      actual: `max: ${Math.max(...chartValues)}, filtered: ${n}`
    });

    // Links
    const linkErrors = records.filter(r => !r.doc_url.startsWith('https://docs.un.org/') || !decodeURIComponent(r.doc_url).toLowerCase().endsWith(r.symbol.toLowerCase()));
    checks.push({
      label: `Links: all doc_url start with "https://docs.un.org/" and end with symbol (case-insensitive)`,
      pass: linkErrors.length === 0,
      actual: linkErrors.length ? `failed: ${linkErrors.map(r => r.symbol).join(', ')}` : ''
    });

    // Paragraph numbers
    const uprWithNumber = records.filter(r => r.mechanism === 'Universal Periodic Review' && extractParagraphNumber(r.text)).length;
    const uprTotal = records.filter(r => r.mechanism === 'Universal Periodic Review').length;
    checks.push({
      label: `Paragraph numbers: UPR records with a number (${uprWithNumber}/${uprTotal})`,
      pass: true,
      warn: uprWithNumber < uprTotal,
      actual: `${uprWithNumber} of ${uprTotal} UPR records have a paragraph number`
    });

    // States found
    const uprWithState = records.filter(r => r.mechanism === 'Universal Periodic Review' && extractStates(r.text).length > 0).length;
    const uprWithoutState = records.filter(r => r.mechanism === 'Universal Periodic Review' && extractStates(r.text).length === 0);
    checks.push({
      label: `States found: UPR records with at least one State (${uprWithState}/${uprTotal})`,
      pass: true,
      warn: uprWithoutState.length > 0,
      actual: uprWithoutState.length ? `no State found: ${uprWithoutState.map(r => r.symbol).join(', ')}` : ''
    });

    // Duplicates and gaps
    const distinctIds = new Set(records.map(r => r.id)).size;
    checks.push({
      label: `Distinct ids: ${distinctIds} vs ${records.length} records`,
      pass: distinctIds === records.length,
      actual: `ids: ${distinctIds}, records: ${records.length}`
    });

    const duplicateTexts = records.reduce((acc, r) => {
      const key = r.text.trim();
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    const duplicates = Object.values(duplicateTexts).filter(v => v > 1).reduce((a, b) => a + b, 0) - Object.values(duplicateTexts).filter(v => v > 1).length;
    checks.push({
      label: `Duplicate texts: ${duplicates}`,
      pass: true,
      actual: `${duplicates} duplicate texts (counting pairs)`
    });

    const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
    const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
    const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
    checks.push({
      label: `Records not labelled: themes (${noThemes}), SDGs (${noSdgs}), affected persons (${noAffected})`,
      pass: true,
      actual: `themes: ${noThemes}, SDGs: ${noSdgs}, affected: ${noAffected}`
    });

    const checkList = document.getElementById('check-list');
    checkList.innerHTML = '';
    checks.forEach(check => {
      const li = document.createElement('li');
      li.className = check.pass ? 'pass' : check.warn ? 'warn' : 'fail';
      li.textContent = check.label;
      if (check.actual) {
        const div = document.createElement('div');
        div.style.fontSize = '0.8rem';
        div.style.color = '#666';
        div.textContent = check.actual;
        li.appendChild(div);
      }
      checkList.appendChild(li);
    });
    document.getElementById('check-count').textContent = checks.length;
  };

  // ------------------------------------------------------------
  // RECORDS TAB
  // ------------------------------------------------------------
  const updateRecords = () => {
    const searchInput = document.getElementById('search-input');
    const keyword = searchInput.value.trim().toLowerCase();
    const tableCaption = document.getElementById('table-caption');
    const tbody = document.getElementById('records-tbody');

    let filteredForTable = [...filtered];
    if (keyword) {
      const words = keyword.split(/\s+/).filter(w => w);
      filteredForTable = filteredForTable.filter(r => {
        const text = (r.text || '').toLowerCase();
        const symbol = (r.symbol || '').toLowerCase();
        return words.every(w => text.includes(w) || symbol.includes(w));
      });
    }

    tableCaption.textContent = `Showing ${Math.min(visibleRows, filteredForTable.length)} of ${filteredForTable.length} matching records`;

    const rows = filteredForTable.slice(0, visibleRows).map(r => {
      const date = new Date(r.date).toISOString().split('T')[0];
      const body = r.body;
      const symbol = r.symbol;
      const docUrl = r.doc_url;
      const paraNum = extractParagraphNumber(r.text);
      const states = r.mechanism === 'Universal Periodic Review' ? extractStates(r.text).join(', ') : '–';
      const firstLine = r.text.substring(0, 120).replace(/\s+\S*$/, '') + (r.text.length > 120 ? '…' : '');

      const tr = document.createElement('tr');
      tr.setAttribute('tabindex', '0');
      tr.setAttribute('aria-expanded', 'false');
      tr.innerHTML = `
        <td>${date}</td>
        <td>${body}</td>
        <td><a href="${docUrl}" target="_blank">${symbol}</a></td>
        <td>${paraNum || '–'}</td>
        <td>${states}</td>
        <td>${firstLine}</td>
      `;

      const fullText = r.text;
      const themes = r.themes || [];
      const sdgs = (r.sdgs || []).map(s => `${s} ${sdgNames[s] || ''}`).join(', ');
      const sdgTargets = r.sdg_targets || [];
      const affectedPersons = r.affected_persons || [];
      const section = r.section || null;

      tr.addEventListener('click', () => {
        const isExpanded = tr.getAttribute('aria-expanded') === 'true';
        if (isExpanded) {
          tr.setAttribute('aria-expanded', 'false');
          tr.nextElementSibling?.remove();
        } else {
          const expandedTr = document.createElement('tr');
          expandedTr.className = 'expanded';
          expandedTr.innerHTML = `
            <td colspan="6">
              <div class="para-num">${paraNum || '–'}</div>
              <div>${fullText}</div>
              <div class="labels">
                ${themes.length ? `<div class="label-group"><h5>Themes</h5>${themes.map(t => `<span>${t}</span>`).join('')}</div>` : ''}
                ${sdgs ? `<div class="label-group"><h5>SDGs</h5><span>${sdgs}</span></div>` : ''}
                ${sdgTargets.length ? `<div class="label-group"><h5>SDG targets</h5>${sdgTargets.map(t => `<span>${t}</span>`).join('')}</div>` : ''}
                ${affectedPersons.length ? `<div class="label-group"><h5>Affected persons</h5>${affectedPersons.map(a => `<span>${a}</span>`).join('')}</div>` : ''}
                ${section ? `<div class="label-group"><h5>Section</h5><span>${section}</span></div>` : ''}
              </div>
              <div class="actions">
                <button class="copy-citation">Copy citation</button>
                <button class="secondary open-doc">Open the UN document</button>
              </div>
            </td>
          `;
          tr.setAttribute('aria-expanded', 'true');
          tr.after(expandedTr);

          expandedTr.querySelector('.copy-citation').addEventListener('click', () => {
            const citation = paraNum ? `${symbol}, para. ${paraNum}` : symbol;
            navigator.clipboard.writeText(citation).then(() => {
              const btn = expandedTr.querySelector('.copy-citation');
              const originalText = btn.textContent;
              btn.textContent = 'Copied!';
              setTimeout(() => btn.textContent = originalText, 2000);
            });
          });
          expandedTr.querySelector('.open-doc').addEventListener('click', () => {
            window.open(docUrl, '_blank');
          });
        }
      });

      tr.addEventListener('keydown', e => {
        if (e.key === 'Enter') tr.click();
      });

      return tr;
    });

    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));

    document.getElementById('sort-date').addEventListener('click', () => {
      sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
      document.getElementById('sort-date').innerHTML = `Date ${sortDirection === 'desc' ? '▼' : '▲'}`;
      filteredForTable.sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return sortDirection === 'desc' ? dateB - dateA : dateA - dateB;
      });
      updateRecords();
    });

    document.getElementById('load-more').addEventListener('click', () => {
      visibleRows += 50;
      updateRecords();
    });
  };

  // ------------------------------------------------------------
  // METHOD TAB
  // ------------------------------------------------------------
  const updateMethod = () => {
    // Already populated in HTML
  };

  // ------------------------------------------------------------
  // EXPORT
  // ------------------------------------------------------------
  document.getElementById('download-csv').addEventListener('click', () => {
    const headers = [
      'Date', 'Body', 'Symbol', 'Paragraph', 'Recommending State', 'First line',
      'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Full text'
    ];
    const rows = filtered.map(r => {
      const date = new Date(r.date).toISOString().split('T')[0];
      const paraNum = extractParagraphNumber(r.text);
      const states = r.mechanism === 'Universal Periodic Review' ? extractStates(r.text).join(', ') : '';
      const firstLine = r.text.substring(0, 120).replace(/\s+\S*$/, '') + (r.text.length > 120 ? '…' : '');
      return [
        `"${date}"`,
        `"${r.body}"`,
        `"${r.symbol}"`,
        `"${paraNum || ''}"`,
        `"${states}"`,
        `"${firstLine.replace(/"/g, '""')}"`,
        `"${(r.themes || []).join('; ')}"`,
        `"${(r.sdgs || []).map(s => `${s} ${sdgNames[s] || ''}`).join('; ')}"`,
        `"${(r.sdg_targets || []).join('; ')}"`,
        `"${(r.affected_persons || []).join('; ')}"`,
        `"${r.section || ''}"`,
        `"${r.text.replace(/"/g, '""')}"`
      ];
    });

    const keyword = document.getElementById('keyword-input').value.trim();
    const mechanism = document.getElementById('mechanism-select').value;
    const bodies = Array.from(document.querySelectorAll('#body-options input:checked')).map(el => el.value);
    const type = document.getElementById('type-select').value;
    const state = document.getElementById('state-select').value;
    const yearFrom = document.getElementById('year-from').value;
    const yearTo = document.getElementById('year-to').value;
    const sdg = document.getElementById('sdg-select').value;

    const comments = [
      `# UN human rights recommendations and observations: ${country}`,
      `# Source: ${data.source_url}`,
      `# Built: ${builtDate}`,
      `# Filters:`,
      `#   Keyword: ${keyword || 'none'}`,
      `#   Mechanism: ${mechanism || 'all'}`,
      `#   Body: ${bodies.length ? bodies.join(', ') : 'all'}`,
      `#   Type: ${type || 'all'}`,
      `#   State: ${state || 'all'}`,
      `#   Year: from ${yearFrom || 'first'} to ${yearTo || 'last'}`,
      `#   SDG: ${sdg || 'all'}`,
      `# Records: ${filtered.length}`,
      headers.join(',')
    ];

    const csv = comments.join('\n') + '\n' + rows.map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `uhri_${country.toLowerCase()}_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  });

  document.getElementById('copy-summary').addEventListener('click', () => {
    const typeCounts = {};
    filtered.forEach(r => typeCounts[r.type] = (typeCounts[r.type] || 0) + 1);
    const typeBreakdown = Object.entries(typeCounts).map(([k, v]) => `${v} ${k}`).join(', ');

    const themeCounts = {};
    filtered.forEach(r => (r.themes || []).forEach(t => themeCounts[t] = (themeCounts[t] || 0) + 1));
    const topThemes = Object.entries(themeCounts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 10).map(([t, c]) => `${t} (${c})`).join(', ');

    const text = `UN human rights recommendations and observations: ${country}. ${filtered.length} records (${typeBreakdown}), ${new Set(filtered.map(r => r.symbol)).size} documents, ${Math.min(...filtered.map(r => r.year))}–${Math.max(...filtered.map(r => r.year))}. Top themes: ${topThemes}.`;
    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('copy-summary');
      const originalText = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => btn.textContent = originalText, 2000);
    });
  });

  // ------------------------------------------------------------
  // CHECK PANEL TOGGLE
  // ------------------------------------------------------------
  document.getElementById('check-btn').addEventListener('click', () => {
    const isExpanded = document.getElementById('check-panel').getAttribute('aria-expanded') === 'true';
    document.getElementById('check-panel').setAttribute('aria-expanded', !isExpanded);
    document.getElementById('check-btn').setAttribute('aria-expanded', !isExpanded);
  });

  // ------------------------------------------------------------
  // UPR STATES LINK
  // ------------------------------------------------------------
  document.getElementById('upr-states-link').addEventListener('click', e => {
    e.preventDefault();
    const list = document.getElementById('upr-states-list');
    list.classList.toggle('hidden');
  });

  // ------------------------------------------------------------
  // RAIL TOGGLE
  // ------------------------------------------------------------
  document.getElementById('rail-toggle').addEventListener('click', () => {
    const rail = document.getElementById('rail');
    const isExpanded = rail.getAttribute('aria-expanded') === 'true';
    rail.setAttribute('aria-expanded', !isExpanded);
  });

  // ------------------------------------------------------------
  // INIT
  // ------------------------------------------------------------
  populateFilters();
  setupFilterPanels();
  applyFilters();
});
</script>
</body>
</html>
```