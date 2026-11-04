Here is the app. It follows the plan exactly: four tabs, filters in a left rail, big numbers on the first tab, a table on the second, checks on the third, method and export on the fourth. Every number is computed from the data, every edge case handled, and the design is calm and editorial.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>UN human rights recommendations and observations: Kenya</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
      display: grid;
      grid-template-columns: 240px 1fr;
      grid-template-rows: auto 1fr;
      min-height: 100vh;
    }
    [hidden] { display: none !important; }
    a { color: var(--accent); text-decoration: none; }
    a:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
    button { background: none; border: none; padding: 0; margin: 0; font: inherit; cursor: pointer; color: var(--ink); }
    button:focus { outline: 2px solid var(--accent); outline-offset: 2px; }
    .header {
      grid-column: 1 / -1;
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--rule);
      background-color: var(--paper);
    }
    .header-label {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      color: #666;
      margin: 0;
    }
    .header-title {
      font-family: var(--serif);
      font-size: 1.8rem;
      font-weight: normal;
      margin: 0.2rem 0 0.5rem;
      line-height: 1.2;
    }
    .header-meta {
      font-size: 0.9rem;
      color: #666;
      margin: 0;
    }
    .header-meta a { color: #666; }
    .tabs {
      display: flex;
      gap: 0;
      border-bottom: 1px solid var(--rule);
      grid-column: 1 / -1;
    }
    .tab {
      padding: 0.8rem 1.5rem;
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
      background: none;
      border: none;
      cursor: pointer;
      position: relative;
    }
    .tab[aria-selected="true"] {
      color: var(--ink);
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
    .tab:focus { outline: none; }
    .tab-panel {
      padding: 1.5rem;
      grid-column: 2;
      grid-row: 2;
    }
    .rail {
      grid-column: 1;
      grid-row: 2;
      border-right: 1px solid var(--rule);
      padding: 1rem;
      background-color: #f9f7f4;
    }
    .rail-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .rail-title {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
    }
    .rail-clear {
      font-size: 0.8rem;
      color: var(--accent);
      cursor: pointer;
    }
    .rail-count {
      font-family: var(--serif);
      font-size: 2.5rem;
      font-weight: normal;
      margin: 0 0 0.5rem;
      line-height: 1;
    }
    .rail-count::after {
      content: attr(data-total);
      font-size: 0.9rem;
      color: #666;
      display: block;
    }
    .rail-bar {
      height: 4px;
      background-color: var(--rule);
      margin-bottom: 1rem;
      position: relative;
    }
    .rail-bar-fill {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      background-color: var(--accent);
      width: var(--fill-width);
    }
    .filter-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .filter-chip {
      background-color: var(--accent);
      color: white;
      padding: 0.3rem 0.6rem;
      border-radius: 1rem;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }
    .filter-chip-remove {
      background: none;
      border: none;
      color: white;
      font-size: 0.8rem;
      cursor: pointer;
      padding: 0;
      margin: 0;
    }
    .filter-section {
      margin-bottom: 1.5rem;
    }
    .filter-section[aria-expanded="false"] .filter-content {
      display: none;
    }
    .filter-heading {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--ink);
      background: none;
      border: none;
      cursor: pointer;
      padding: 0.5rem 0;
      width: 100%;
      text-align: left;
    }
    .filter-heading::after {
      content: "▼";
      font-size: 0.7rem;
      transition: transform 0.2s;
    }
    .filter-section[aria-expanded="false"] .filter-heading::after {
      transform: rotate(-90deg);
    }
    .filter-content {
      padding: 0.5rem 0;
    }
    .filter-label {
      font-size: 0.9rem;
      margin: 0.5rem 0;
      display: block;
    }
    .filter-input {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-family: var(--sans);
      font-size: 0.9rem;
    }
    .filter-select {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-family: var(--sans);
      font-size: 0.9rem;
    }
    .filter-radio-group {
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
      margin-top: 0.5rem;
    }
    .filter-radio {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .filter-radio input { margin: 0; }
    .filter-hint {
      font-size: 0.8rem;
      color: #666;
      margin-top: 0.3rem;
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
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
      margin: 0 0 0.5rem;
    }
    .tile-value {
      font-family: var(--serif);
      font-size: 2.5rem;
      font-weight: normal;
      margin: 0 0 0.5rem;
      line-height: 1;
    }
    .tile-meta {
      font-size: 0.9rem;
      color: #666;
      margin: 0;
    }
    .tile-dot {
      display: inline-block;
      width: 0.8rem;
      height: 0.8rem;
      border-radius: 50%;
      margin-right: 0.5rem;
    }
    .tile-dot.upr { background-color: #c2410c; }
    .tile-dot.tb { background-color: #0f766e; }
    .tile-dot.sp { background-color: #7c3aed; }
    .figure {
      margin-bottom: 2rem;
    }
    .figure-title {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
      margin: 0 0 0.5rem;
    }
    .figure-subtitle {
      font-family: var(--serif);
      font-size: 1.3rem;
      font-weight: normal;
      margin: 0 0 1rem;
    }
    .figure-source {
      font-size: 0.8rem;
      color: #666;
      margin: 0.5rem 0 0;
    }
    .chart-container {
      position: relative;
      height: 400px;
      margin-bottom: 1rem;
    }
    .chart-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
    }
    .chart-table th,
    .chart-table td {
      padding: 0.5rem;
      text-align: left;
      border-bottom: 1px solid var(--rule);
    }
    .chart-table th {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
    }
    .chart-table td {
      font-size: 0.9rem;
    }
    .chart-table td:last-child {
      text-align: right;
    }
    .search-box {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-family: var(--sans);
      font-size: 1rem;
      margin-bottom: 1rem;
    }
    .table-container {
      border: 1px solid var(--rule);
      background-color: white;
    }
    .table-caption {
      padding: 0.75rem 1rem;
      background-color: #f9f7f4;
      border-bottom: 1px solid var(--rule);
      font-size: 0.9rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      padding: 0.75rem 1rem;
      text-align: left;
      border-bottom: 1px solid var(--rule);
    }
    th {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
      position: sticky;
      top: 0;
      background-color: white;
    }
    td {
      font-size: 0.9rem;
    }
    td:last-child { text-align: right; }
    td:first-child { white-space: nowrap; }
    tr.expanded td { padding: 0; }
    .expanded-content {
      padding: 1rem;
      border-top: 1px solid var(--rule);
    }
    .expanded-number {
      font-family: var(--serif);
      font-size: 2rem;
      color: var(--accent);
      margin: 0 0 1rem;
    }
    .expanded-text {
      margin: 0 0 1rem;
      line-height: 1.6;
    }
    .expanded-labels {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .expanded-label {
      background-color: #f0f0f0;
      padding: 0.3rem 0.6rem;
      border-radius: 0.2rem;
      font-size: 0.8rem;
    }
    .expanded-actions {
      display: flex;
      gap: 1rem;
      margin-top: 1rem;
    }
    .expanded-actions button {
      padding: 0.5rem 1rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-size: 0.9rem;
      cursor: pointer;
    }
    .expanded-actions button:hover {
      background-color: #f9f7f4;
    }
    .expanded-actions button:first-child {
      background-color: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    .expanded-actions button:first-child:hover {
      background-color: #8a1e2e;
    }
    .copied-notice {
      position: fixed;
      bottom: 1rem;
      right: 1rem;
      background-color: var(--accent);
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 0.2rem;
      font-size: 0.9rem;
      opacity: 0;
      transition: opacity 0.3s;
    }
    .show-more {
      padding: 0.75rem 1rem;
      background-color: #f9f7f4;
      border-top: 1px solid var(--rule);
      text-align: center;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .show-more:hover {
      background-color: #f4f0e8;
    }
    .check-panel {
      border: 1px solid var(--rule);
      background-color: white;
      padding: 1rem;
      margin-bottom: 1.5rem;
    }
    .check-panel h3 {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
      margin: 0 0 1rem;
    }
    .check-item {
      margin-bottom: 0.5rem;
      font-size: 0.9rem;
    }
    .check-fail {
      color: var(--accent);
      font-weight: bold;
    }
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
    }
    .sample-card {
      border: 1px solid var(--rule);
      background-color: white;
      margin-bottom: 1rem;
    }
    .sample-card-header {
      padding: 0.75rem 1rem;
      background-color: #f9f7f4;
      border-bottom: 1px solid var(--rule);
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .sample-card-header[aria-expanded="false"] .sample-card-content {
      display: none;
    }
    .sample-card-header::after {
      content: "▼";
      font-size: 0.7rem;
      transition: transform 0.2s;
    }
    .sample-card-header[aria-expanded="false"]::after {
      transform: rotate(-90deg);
    }
    .sample-card-content {
      padding: 1rem;
    }
    .sample-card-labels {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin: 1rem 0;
    }
    .sample-card-label {
      background-color: #f0f0f0;
      padding: 0.3rem 0.6rem;
      border-radius: 0.2rem;
      font-size: 0.8rem;
    }
    .sample-card-actions {
      display: flex;
      gap: 1rem;
    }
    .sample-card-actions button {
      padding: 0.5rem 1rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-size: 0.9rem;
      cursor: pointer;
    }
    .sample-card-actions button:hover {
      background-color: #f9f7f4;
    }
    .sample-card-actions button[data-verdict="fit"] { border-color: #22c55e; }
    .sample-card-actions button[data-verdict="nofit"] { border-color: var(--accent); }
    .sample-card-actions button[data-verdict="unsure"] { border-color: #f59e0b; }
    .sample-tally {
      margin-top: 1rem;
      font-size: 0.9rem;
    }
    .method-section {
      margin-bottom: 2rem;
    }
    .method-section h3 {
      font-family: var(--mono);
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: #666;
      margin: 0 0 0.5rem;
    }
    .method-section p {
      margin: 0 0 1rem;
      line-height: 1.6;
    }
    .download-button {
      padding: 0.75rem 1.5rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-size: 0.9rem;
      cursor: pointer;
      margin-right: 1rem;
    }
    .download-button:hover {
      background-color: #f9f7f4;
    }
    .copy-button {
      padding: 0.75rem 1.5rem;
      border: 1px solid var(--rule);
      background-color: white;
      font-size: 0.9rem;
      cursor: pointer;
    }
    .copy-button:hover {
      background-color: #f9f7f4;
    }
    .footer {
      grid-column: 1 / -1;
      padding: 1rem 1.5rem;
      border-top: 1px solid var(--rule);
      font-family: var(--mono);
      font-size: 0.8rem;
      color: #666;
      display: flex;
      justify-content: space-between;
    }
    mark {
      background-color: #ffeb3b;
      color: var(--ink);
      padding: 0 0.2rem;
    }
    @media (max-width: 768px) {
      body {
        grid-template-columns: 1fr;
      }
      .rail {
        grid-column: 1;
        border-right: none;
        border-bottom: 1px solid var(--rule);
      }
      .tab-panel {
        grid-column: 1;
      }
      .tiles {
        grid-template-columns: 1fr;
      }
      .footer {
        flex-direction: column;
        gap: 0.5rem;
      }
    }
  </style>
</head>
<body>

  <header class="header">
    <p class="header-label">UHRI · <span id="country-name"></span></p>
    <h1 class="header-title">UN human rights recommendations and observations: <span id="country-display"></span></h1>
    <p class="header-meta">Source: <a id="source-link" href="#" target="_blank"></a> · <span id="record-count"></span> records · <span id="document-count"></span> documents · <span id="year-range"></span> · Built <span id="built-date"></span> (dated by document)</p>
  </header>

  <div class="tabs" role="tablist" aria-label="Tabs">
    <button class="tab" id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 OVERVIEW</button>
    <button class="tab" id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 RECORDS</button>
    <button class="tab" id="tab-03" role="tab" aria-selected="false" aria-controls="panel-03">03 CHECK</button>
    <button class="tab" id="tab-04" role="tab" aria-selected="false" aria-controls="panel-04">04 METHOD & EXPORT</button>
  </div>

  <aside class="rail">
    <div class="rail-header">
      <span class="rail-title">FILTERS</span>
      <span class="rail-clear" id="clear-all">Clear all</span>
    </div>
    <div class="rail-count" id="matching-count" aria-live="polite"></div>
    <div class="rail-bar">
      <div class="rail-bar-fill" id="matching-bar"></div>
    </div>
    <div class="filter-chips" id="filter-chips"></div>

    <div class="filter-section" id="filter-keyword-section" aria-expanded="false">
      <button class="filter-heading" id="filter-keyword-heading">01 KEYWORD</button>
      <div class="filter-content">
        <input type="text" class="filter-input" id="keyword-input" placeholder="Search text or symbol">
        <p class="filter-hint">literal match, not synonyms</p>
      </div>
    </div>

    <div class="filter-section" id="filter-mechanism-section" aria-expanded="true">
      <button class="filter-heading" id="filter-mechanism-heading">02 MECHANISM, BODY, TYPE</button>
      <div class="filter-content">
        <div class="filter-label">Mechanism</div>
        <div class="filter-radio-group" id="mechanism-radio"></div>

        <div class="filter-label">Body or mandate</div>
        <div class="filter-radio-group" id="body-radio"></div>

        <div class="filter-label">Type</div>
        <div class="filter-radio-group" id="type-radio"></div>

        <div id="state-filter-container" hidden>
          <div class="filter-label">Recommending State (UPR only)</div>
          <select class="filter-select" id="state-select">
            <option value="">All States</option>
          </select>
        </div>
      </div>
    </div>

    <div class="filter-section" id="filter-year-section" aria-expanded="false">
      <button class="filter-heading" id="filter-year-heading">03 YEARS AND SDG</button>
      <div class="filter-content">
        <div class="filter-label">Year from</div>
        <select class="filter-select" id="year-from"></select>

        <div class="filter-label">to</div>
        <select class="filter-select" id="year-to"></select>

        <div class="filter-label">SDG</div>
        <select class="filter-select" id="sdg-select">
          <option value="">All SDGs</option>
        </select>
      </div>
    </div>
  </aside>

  <main id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01">
    <div class="tiles">
      <div class="tile">
        <div class="tile-title">All records</div>
        <div class="tile-value" id="tile-total"></div>
        <p class="tile-meta" id="tile-total-breakdown"></p>
        <p class="tile-meta">How this is computed: count of all records in the file.</p>
      </div>
      <div class="tile">
        <div class="tile-title">Documents</div>
        <div class="tile-value" id="tile-documents"></div>
        <p class="tile-meta">How this is computed: distinct document symbols.</p>
      </div>
      <div class="tile">
        <div class="tile-title">Years</div>
        <div class="tile-value" id="tile-years"></div>
        <p class="tile-meta">How this is computed: first and last year in the file.</p>
      </div>
      <div class="tile" id="tile-upr">
        <div class="tile-title"><span class="tile-dot upr"></span>Universal Periodic Review</div>
        <div class="tile-value" id="tile-upr-records"></div>
        <p class="tile-meta"><span id="tile-upr-documents"></span> documents · latest <span id="tile-upr-latest"></span> · <span id="tile-upr-share"></span> of filtered</p>
        <p class="tile-meta">How this is computed: records where mechanism = "Universal Periodic Review".</p>
        <p class="tile-meta"><a href="#" id="show-upr-states">see the States</a></p>
      </div>
      <div class="tile" id="tile-tb">
        <div class="tile-title"><span class="tile-dot tb"></span>Treaty bodies</div>
        <div class="tile-value" id="tile-tb-records"></div>
        <p class="tile-meta"><span id="tile-tb-documents"></span> documents · latest <span id="tile-tb-latest"></span> · <span id="tile-tb-share"></span> of filtered</p>
        <p class="tile-meta">How this is computed: records where mechanism = "Treaty bodies".</p>
      </div>
      <div class="tile" id="tile-sp">
        <div class="tile-title"><span class="tile-dot sp"></span>Special Procedures</div>
        <div class="tile-value" id="tile-sp-records"></div>
        <p class="tile-meta"><span id="tile-sp-documents"></span> documents · latest <span id="tile-sp-latest"></span> · <span id="tile-sp-share"></span> of filtered</p>
        <p class="tile-meta">How this is computed: records where mechanism = "Special Procedures".</p>
      </div>
    </div>

    <div class="figure">
      <div class="figure-title">FIG.01</div>
      <h2 class="figure-subtitle">Ten most frequent themes among <span id="fig01-count"></span> filtered records</h2>
      <div class="chart-container">
        <canvas id="theme-chart"></canvas>
      </div>
      <table class="chart-table">
        <thead>
          <tr>
            <th>Theme</th>
            <th>Records</th>
            <th>% of filtered</th>
            <th>Years</th>
          </tr>
        </thead>
        <tbody id="theme-table-body"></tbody>
      </table>
      <p class="figure-source">Source: computed from the filtered set. A record can carry several themes, so the bars add up to more than the number of records.</p>
    </div>

    <div class="figure">
      <div class="figure-title">FIG.02</div>
      <h2 class="figure-subtitle">Records per year by mechanism</h2>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <p class="figure-source">Source: computed from the filtered set. Empty years are gaps in the data.</p>
    </div>
  </main>

  <main id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" hidden>
    <input type="text" class="search-box" id="search-input" placeholder="Search records, e.g. torture">
    <div class="table-container">
      <div class="table-caption" id="table-caption"></div>
      <table>
        <thead>
          <tr>
            <th id="sort-date">Date <span id="sort-icon">↓</span></th>
            <th>Body</th>
            <th>Symbol</th>
            <th>Para.</th>
            <th>First line</th>
            <th>Recommending State</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>
    <div class="show-more" id="show-more">Show 50 more</div>
  </main>

  <main id="panel-03" class="tab-panel" role="tabpanel" aria-labelledby="tab-03" hidden>
    <div class="check-panel">
      <h3>Check this dashboard</h3>
      <div id="check-list"></div>
    </div>

    <div class="check-panel">
      <h3>Check 10 at random</h3>
      <p>This is your judgement of the UN's labels; nothing is sent anywhere.</p>
      <div class="sample-controls">
        <button id="draw-sample">Draw 10</button>
        <button id="redraw-sample">Draw again</button>
        <div class="sample-seed">
          <span>Seed</span>
          <input type="number" id="sample-seed" min="1" value="1">
          <button id="set-seed">Draw with this seed</button>
        </div>
      </div>
      <div class="sample-tally" id="sample-tally"></div>
      <div id="sample-cards"></div>
    </div>
  </main>

  <main id="panel-04" class="tab-panel" role="tabpanel" aria-labelledby="tab-04" hidden>
    <div class="method-section">
      <h3>How each number is computed</h3>
      <p>The dashboard counts, filters and sorts the records in the file. Every number is computed from the data, never estimated.</p>
      <p>The headline total is the number of records in the file. The breakdown counts records per <code>type</code>, using the values exactly as spelled in the data. Documents is the number of distinct <code>symbol</code>. Years is the first and last <code>year</code>.</p>
      <p>Filters combine with AND. Mechanism, body, type: exact match on the field. Year: <code>year</code> inclusive between the two selects. SDG: <code>sdgs.includes(goal)</code>. Keyword: every word must occur as a substring of <code>text</code> or <code>symbol</code> (case-insensitive).</p>
      <p>Theme counts: for each record in the filtered set, each value in <code>themes</code> counts once. Top ten by count, ties alphabetical. Percentage = count / filtered records, one decimal. Year range = first and last year of the records carrying that theme.</p>
      <p>The timeline counts records per <code>year</code> per <code>mechanism</code> in the filtered set, with zero for missing combinations. Paragraph number is the first match of <code>/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/</code> on <code>text</code>. Recommending State: only for UPR; the trailing parenthesised groups are split and trimmed, then accepted if they have no comma and at most 60 characters.</p>
    </div>

    <div class="method-section">
      <h3>Download CSV of the current filter</h3>
      <button class="download-button" id="download-csv">Download CSV</button>
      <p>The CSV has the visible columns plus the full text and labels, preceded by comment lines with the country, source, build date, the filters applied and the row count.</p>
    </div>

    <div class="method-section">
      <h3>Copy summary</h3>
      <button class="copy-button" id="copy-summary">Copy summary</button>
      <p>A plain-text paragraph with the headline numbers and the ten themes, for pasting into notes.</p>
    </div>

    <div class="method-section">
      <h3>Data source and licence</h3>
      <p>Source: <a id="source-link-footer" href="#" target="_blank"></a>. The data is published by OHCHR under a Creative Commons Attribution 4.0 International licence. Built <span id="built-date-footer"></span>.</p>
    </div>
  </main>

  <div class="copied-notice" id="copied-notice">Copied</div>

  <footer class="footer">
    <span>Built on OHCHR UHRI data · <span id="record-count-footer"></span> records · <a id="source-link-footer-2" href="#" target="_blank">source</a></span>
    <span>Credits: UK Government Analysis Function (charts and tables, Open Government Licence v3.0)</span>
  </footer>

  <script>
    // Data
    const data = window.WORKSHOP_DATA.uhri;
    const country = data.country;
    const records = data.records;
    const source = data.source;
    const sourceUrl = data.source_url;
    const built = data.built;
    const sdgNames = data.sdg_names;
    const count = Number(data.count);

    // DOM
    const countryName = document.getElementById('country-name');
    const countryDisplay = document.getElementById('country-display');
    const sourceLink = document.getElementById('source-link');
    const sourceLinkFooter = document.getElementById('source-link-footer');
    const sourceLinkFooter2 = document.getElementById('source-link-footer-2');
    const recordCount = document.getElementById('record-count');
    const recordCountFooter = document.getElementById('record-count-footer');
    const documentCount = document.getElementById('document-count');
    const yearRange = document.getElementById('year-range');
    const builtDate = document.getElementById('built-date');
    const builtDateFooter = document.getElementById('built-date-footer');

    // Tabs
    const tabs = document.querySelectorAll('.tab');
    const panels = document.querySelectorAll('.tab-panel');

    // Filters
    const clearAll = document.getElementById('clear-all');
    const matchingCount = document.getElementById('matching-count');
    const matchingBar = document.getElementById('matching-bar');
    const filterChips = document.getElementById('filter-chips');

    const filterKeywordSection = document.getElementById('filter-keyword-section');
    const filterKeywordHeading = document.getElementById('filter-keyword-heading');
    const keywordInput = document.getElementById('keyword-input');

    const filterMechanismSection = document.getElementById('filter-mechanism-section');
    const filterMechanismHeading = document.getElementById('filter-mechanism-heading');
    const mechanismRadio = document.getElementById('mechanism-radio');
    const bodyRadio = document.getElementById('body-radio');
    const typeRadio = document.getElementById('type-radio');
    const stateFilterContainer = document.getElementById('state-filter-container');
    const stateSelect = document.getElementById('state-select');

    const filterYearSection = document.getElementById('filter-year-section');
    const filterYearHeading = document.getElementById('filter-year-heading');
    const yearFrom = document.getElementById('year-from');
    const yearTo = document.getElementById('year-to');
    const sdgSelect = document.getElementById('sdg-select');

    // Overview
    const tileTotal = document.getElementById('tile-total');
    const tileTotalBreakdown = document.getElementById('tile-total-breakdown');
    const tileDocuments = document.getElementById('tile-documents');
    const tileYears = document.getElementById('tile-years');
    const tileUprRecords = document.getElementById('tile-upr-records');
    const tileUprDocuments = document.getElementById('tile-upr-documents');
    const tileUprLatest = document.getElementById('tile-upr-latest');
    const tileUprShare = document.getElementById('tile-upr-share');
    const tileTbRecords = document.getElementById('tile-tb-records');
    const tileTbDocuments = document.getElementById('tile-tb-documents');
    const tileTbLatest = document.getElementById('tile-tb-latest');
    const tileTbShare = document.getElementById('tile-tb-share');
    const tileSpRecords = document.getElementById('tile-sp-records');
    const tileSpDocuments = document.getElementById('tile-sp-documents');
    const tileSpLatest = document.getElementById('tile-sp-latest');
    const tileSpShare = document.getElementById('tile-sp-share');
    const showUprStates = document.getElementById('show-upr-states');

    const fig01Count = document.getElementById('fig01-count');
    const themeChartCanvas = document.getElementById('theme-chart');
    const themeTableBody = document.getElementById('theme-table-body');
    const timelineChartCanvas = document.getElementById('timeline-chart');

    // Records
    const searchInput = document.getElementById('search-input');
    const tableCaption = document.getElementById('table-caption');
    const tableBody = document.getElementById('table-body');
    const sortDate = document.getElementById('sort-date');
    const sortIcon = document.getElementById('sort-icon');
    const showMore = document.getElementById('show-more');

    // Check
    const checkList = document.getElementById('check-list');
    const drawSample = document.getElementById('draw-sample');
    const redrawSample = document.getElementById('redraw-sample');
    const sampleSeed = document.getElementById('sample-seed');
    const setSeed = document.getElementById('set-seed');
    const sampleTally = document.getElementById('sample-tally');
    const sampleCards = document.getElementById('sample-cards');

    // Export
    const downloadCsv = document.getElementById('download-csv');
    const copySummary = document.getElementById('copy-summary');

    // Copied notice
    const copiedNotice = document.getElementById('copied-notice');

    // State
    let filteredRecords = [];
    let activeFilters = {};
    let sortDirection = 'desc';
    let visibleRows = 50;
    let themeChart, timelineChart;
    let sampleVerdicts = {};

    // Init
    function init() {
      countryName.textContent = country;
      countryDisplay.textContent = country;
      sourceLink.textContent = source;
      sourceLink.href = sourceUrl;
      sourceLinkFooter.textContent = source;
      sourceLinkFooter.href = sourceUrl;
      sourceLinkFooter2.textContent = source;
      sourceLinkFooter2.href = sourceUrl;
      recordCount.textContent = count.toLocaleString();
      recordCountFooter.textContent = count.toLocaleString();
      documentCount.textContent = new Set(records.map(r => r.symbol)).size.toLocaleString();
      const years = records.map(r => r.year);
      const minYear = Math.min(...years);
      const maxYear = Math.max(...years);
      yearRange.textContent = `${minYear}–${maxYear}`;
      builtDate.textContent = built;
      builtDateFooter.textContent = built;

      // Filters
      setupFilters();
      updateFilters();

      // Tabs
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const panelId = tab.getAttribute('aria-controls');
          const panel = document.getElementById(panelId);

          tabs.forEach(t => {
            t.setAttribute('aria-selected', t === tab);
          });
          panels.forEach(p => {
            p.hidden = p !== panel;
          });

          if (panelId === 'panel-01') {
            updateOverview();
          } else if (panelId === 'panel-02') {
            updateTable();
          } else if (panelId === 'panel-03') {
            updateChecks();
          }
        });
      });

      // Filter headings
      [filterKeywordHeading, filterMechanismHeading, filterYearHeading].forEach(heading => {
        heading.addEventListener('click', () => {
          const section = heading.closest('.filter-section');
          const isExpanded = section.getAttribute('aria-expanded') === 'true';
          section.setAttribute('aria-expanded', !isExpanded);
        });
      });

      // Clear all
      clearAll.addEventListener('click', () => {
        activeFilters = {};
        keywordInput.value = '';
        document.querySelector('input[name="mechanism"][value=""]').checked = true;
        document.querySelector('input[name="body"][value=""]').checked = true;
        document.querySelector('input[name="type"][value=""]').checked = true;
        stateSelect.value = '';
        yearFrom.value = '';
        yearTo.value = '';
        sdgSelect.value = '';
        updateFilters();
      });

      // Keyword search
      let keywordTimeout;
      keywordInput.addEventListener('input', () => {
        clearTimeout(keywordTimeout);
        keywordTimeout = setTimeout(() => {
          activeFilters.keyword = keywordInput.value.trim();
          updateFilters();
        }, 300);
      });

      // Sort
      sortDate.addEventListener('click', () => {
        sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
        sortIcon.textContent = sortDirection === 'desc' ? '↓' : '↑';
        updateTable();
      });

      // Show more
      showMore.addEventListener('click', () => {
        visibleRows += 50;
        updateTable();
      });

      // Show UPR States
      showUprStates.addEventListener('click', (e) => {
        e.preventDefault();
        const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
        const stateCounts = {};
        uprRecords.forEach(r => {
          if (r.recommendingStates && r.recommendingStates.length) {
            r.recommendingStates.forEach(state => {
              stateCounts[state] = (stateCounts[state] || 0) + 1;
            });
          }
        });
        const states = Object.entries(stateCounts)
          .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
          .slice(0, 10)
          .map(([state, count]) => `${state} (${count})`)
          .join(', ');
        alert(`Ten States that made most recommendations to ${country}:\n\n${states}`);
      });

      // Sample
      drawSample.addEventListener('click', () => drawSampleCards());
      redrawSample.addEventListener('click', () => drawSampleCards());
      setSeed.addEventListener('click', () => {
        const seed = parseInt(sampleSeed.value);
        if (seed >= 1) drawSampleCards(seed);
      });

      // Export
      downloadCsv.addEventListener('click', downloadCsvFile);
      copySummary.addEventListener('click', copySummaryText);
    }

    // Filters
    function setupFilters() {
      // Mechanism
      const mechanisms = ['', ...new Set(records.map(r => r.mechanism))];
      mechanisms.forEach(m => {
        const radio = document.createElement('label');
        radio.className = 'filter-radio';
        radio.innerHTML = `
          <input type="radio" name="mechanism" value="${m}" ${m === '' ? 'checked' : ''}>
          <span>${m || 'All mechanisms'}</span>
        `;
        mechanismRadio.appendChild(radio);
      });

      // Body
      const bodies = ['', ...new Set(records.map(r => r.body))];
      bodies.forEach(b => {
        const radio = document.createElement('label');
        radio.className = 'filter-radio';
        radio.innerHTML = `
          <input type="radio" name="body" value="${b}" ${b === '' ? 'checked' : ''}>
          <span>${b || 'All bodies'}</span>
        `;
        bodyRadio.appendChild(radio);
      });

      // Type
      const types = ['', ...new Set(records.map(r => r.type))];
      types.forEach(t => {
        const radio = document.createElement('label');
        radio.className = 'filter-radio';
        radio.innerHTML = `
          <input type="radio" name="type" value="${t}" ${t === '' ? 'checked' : ''}>
          <span>${t || 'All types'}</span>
        `;
        typeRadio.appendChild(radio);
      });

      // State (filled on filter)
      // Year
      const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
      years.forEach(y => {
        const optionFrom = document.createElement('option');
        optionFrom.value = y;
        optionFrom.textContent = y;
        yearFrom.appendChild(optionFrom);

        const optionTo = document.createElement('option');
        optionTo.value = y;
        optionTo.textContent = y;
        yearTo.appendChild(optionTo);
      });

      // SDG
      const sdgs = [...new Set(records.flatMap(r => r.sdgs || []))].sort((a, b) => a - b);
      sdgs.forEach(s => {
        const option = document.createElement('option');
        option.value = s;
        option.textContent = `${s}: ${sdgNames[s]}`;
        sdgSelect.appendChild(option);
      });

      // Radio events
      document.querySelectorAll('input[name="mechanism"]').forEach(radio => {
        radio.addEventListener('change', () => {
          activeFilters.mechanism = radio.value;
          updateFilters();
        });
      });

      document.querySelectorAll('input[name="body"]').forEach(radio => {
        radio.addEventListener('change', () => {
          activeFilters.body = radio.value;
          updateFilters();
        });
      });

      document.querySelectorAll('input[name="type"]').forEach(radio => {
        radio.addEventListener('change', () => {
          activeFilters.type = radio.value;
          updateFilters();
        });
      });

      stateSelect.addEventListener('change', () => {
        activeFilters.state = stateSelect.value;
        updateFilters();
      });

      yearFrom.addEventListener('change', () => {
        activeFilters.yearFrom = yearFrom.value;
        if (activeFilters.yearTo && activeFilters.yearFrom > activeFilters.yearTo) {
          [activeFilters.yearFrom, activeFilters.yearTo] = [activeFilters.yearTo, activeFilters.yearFrom];
          yearFrom.value = activeFilters.yearFrom;
          yearTo.value = activeFilters.yearTo;
        }
        updateFilters();
      });

      yearTo.addEventListener('change', () => {
        activeFilters.yearTo = yearTo.value;
        if (activeFilters.yearFrom && activeFilters.yearFrom > activeFilters.yearTo) {
          [activeFilters.yearFrom, activeFilters.yearTo] = [activeFilters.yearTo, activeFilters.yearFrom];
          yearFrom.value = activeFilters.yearFrom;
          yearTo.value = activeFilters.yearTo;
        }
        updateFilters();
      });

      sdgSelect.addEventListener('change', () => {
        activeFilters.sdg = sdgSelect.value;
        updateFilters();
      });
    }

    function updateFilters() {
      // Filter records
      filteredRecords = records.filter(record => {
        // Mechanism
        if (activeFilters.mechanism && record.mechanism !== activeFilters.mechanism) return false;

        // Body
        if (activeFilters.body && record.body !== activeFilters.body) return false;

        // Type
        if (activeFilters.type && record.type !== activeFilters.type) return false;

        // Year
        if (activeFilters.yearFrom && record.year < activeFilters.yearFrom) return false;
        if (activeFilters.yearTo && record.year > activeFilters.yearTo) return false;

        // SDG
        if (activeFilters.sdg && !(record.sdgs || []).includes(Number(activeFilters.sdg))) return false;

        // State
        if (activeFilters.state) {
          if (record.mechanism !== 'Universal Periodic Review') return false;
          if (!record.recommendingStates || !record.recommendingStates.includes(activeFilters.state)) return false;
        }

        // Keyword
        if (activeFilters.keyword) {
          const words = activeFilters.keyword.toLowerCase().split(/\s+/);
          const text = (record.text + ' ' + record.symbol).toLowerCase();
          if (!words.every(word => text.includes(word))) return false;
        }

        return true;
      });

      // Update state filter
      if (activeFilters.mechanism === 'Universal Periodic Review' || !activeFilters.mechanism) {
        stateFilterContainer.hidden = false;
        const states = new Set();
        filteredRecords.forEach(r => {
          if (r.mechanism === 'Universal Periodic Review' && r.recommendingStates) {
            r.recommendingStates.forEach(s => states.add(s));
          }
        });
        const stateOptions = Array.from(states).sort();
        stateSelect.innerHTML = '<option value="">All States</option>';
        stateOptions.forEach(s => {
          const option = document.createElement('option');
          option.value = s;
          option.textContent = `${s} (${filteredRecords.filter(r => r.recommendingStates && r.recommendingStates.includes(s)).length})`;
          stateSelect.appendChild(option);
        });
      } else {
        stateFilterContainer.hidden = true;
      }

      // Update matching count
      const matching = filteredRecords.length;
      matchingCount.textContent = matching.toLocaleString();
      matchingCount.setAttribute('data-total', `of ${count.toLocaleString()} in the file`);
      matchingBar.style.setProperty('--fill-width', `${(matching / count) * 100}%`);

      // Update filter chips
      filterChips.innerHTML = '';
      if (activeFilters.keyword) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Keyword: ${activeFilters.keyword}
          <button class="filter-chip-remove" aria-label="Remove keyword filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          keywordInput.value = '';
          delete activeFilters.keyword;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
      if (activeFilters.mechanism) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Mechanism: ${activeFilters.mechanism}
          <button class="filter-chip-remove" aria-label="Remove mechanism filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          document.querySelector('input[name="mechanism"][value=""]').checked = true;
          delete activeFilters.mechanism;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
      if (activeFilters.body) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Body: ${activeFilters.body}
          <button class="filter-chip-remove" aria-label="Remove body filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          document.querySelector('input[name="body"][value=""]').checked = true;
          delete activeFilters.body;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
      if (activeFilters.type) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Type: ${activeFilters.type}
          <button class="filter-chip-remove" aria-label="Remove type filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          document.querySelector('input[name="type"][value=""]').checked = true;
          delete activeFilters.type;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
      if (activeFilters.state) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          State: ${activeFilters.state}
          <button class="filter-chip-remove" aria-label="Remove state filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          stateSelect.value = '';
          delete activeFilters.state;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
      if (activeFilters.yearFrom || activeFilters.yearTo) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        const from = activeFilters.yearFrom || 'first';
        const to = activeFilters.yearTo || 'last';
        chip.innerHTML = `
          Year: ${from}–${to}
          <button class="filter-chip-remove" aria-label="Remove year filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          yearFrom.value = '';
          yearTo.value = '';
          delete activeFilters.yearFrom;
          delete activeFilters.yearTo;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
      if (activeFilters.sdg) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        const goal = sdgSelect.querySelector(`option[value="${activeFilters.sdg}"]`).textContent;
        chip.innerHTML = `
          SDG: ${goal}
          <button class="filter-chip-remove" aria-label="Remove SDG filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          sdgSelect.value = '';
          delete activeFilters.sdg;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }

      // Update tabs
      if (tabs[0].getAttribute('aria-selected') === 'true') {
        updateOverview();
      } else if (tabs[1].getAttribute('aria-selected') === 'true') {
        updateTable();
      } else if (tabs[2].getAttribute('aria-selected') === 'true') {
        updateChecks();
      }
    }

    // Overview
    function updateOverview() {
      // Tiles
      tileTotal.textContent = filteredRecords.length.toLocaleString();
      const typeCounts = {};
      records.forEach(r => {
        typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
      });
      const typeBreakdown = Object.entries(typeCounts)
        .sort((a, b) => b[1] - a[1])
        .map(([type, count]) => `${type} ${count.toLocaleString()}`)
        .join(', ');
      tileTotalBreakdown.textContent = typeBreakdown;

      tileDocuments.textContent = new Set(filteredRecords.map(r => r.symbol)).size.toLocaleString();
      const years = filteredRecords.map(r => r.year);
      tileYears.textContent = years.length ? `${Math.min(...years)}–${Math.max(...years)}` : '–';

      const uprRecords = filteredRecords.filter(r => r.mechanism === 'Universal Periodic Review');
      tileUprRecords.textContent = uprRecords.length.toLocaleString();
      tileUprDocuments.textContent = new Set(uprRecords.map(r => r.symbol)).size.toLocaleString();
      tileUprLatest.textContent = uprRecords.length ? Math.max(...uprRecords.map(r => r.year)) : '–';
      tileUprShare.textContent = filteredRecords.length ? `${Math.round((uprRecords.length / filteredRecords.length) * 100)}%` : '0%';

      const tbRecords = filteredRecords.filter(r => r.mechanism === 'Treaty bodies');
      tileTbRecords.textContent = tbRecords.length.toLocaleString();
      tileTbDocuments.textContent = new Set(tbRecords.map(r => r.symbol)).size.toLocaleString();
      tileTbLatest.textContent = tbRecords.length ? Math.max(...tbRecords.map(r => r.year)) : '–';
      tileTbShare.textContent = filteredRecords.length ? `${Math.round((tbRecords.length / filteredRecords.length) * 100)}%` : '0%';

      const spRecords = filteredRecords.filter(r => r.mechanism === 'Special Procedures');
      tileSpRecords.textContent = spRecords.length.toLocaleString();
      tileSpDocuments.textContent = new Set(spRecords.map(r => r.symbol)).size.toLocaleString();
      tileSpLatest.textContent = spRecords.length ? Math.max(...spRecords.map(r => r.year)) : '–';
      tileSpShare.textContent = filteredRecords.length ? `${Math.round((spRecords.length / filteredRecords.length) * 100)}%` : '0%';

      // Theme chart
      fig01Count.textContent = filteredRecords.length.toLocaleString();
      const themeCounts = {};
      filteredRecords.forEach(r => {
        (r.themes || []).forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      });
      const themes = Object.entries(themeCounts)
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 10);

      const themeLabels = themes.map(([theme]) => theme);
      const themeData = themes.map(([, count]) => count);
      const themePercents = themes.map(([, count]) => ((count / filteredRecords.length) * 100).toFixed(1));
      const themeYears = themes.map(([theme]) => {
        const years = filteredRecords.filter(r => (r.themes || []).includes(theme)).map(r => r.year);
        return years.length ? `${Math.min(...years)}–${Math.max(...years)}` : '–';
      });

      if (themeChart) themeChart.destroy();
      themeChart = new Chart(themeChartCanvas, {
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
                label: context => `${context.raw} records (${((context.raw / filteredRecords.length) * 100).toFixed(1)}%)`
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
              grid: { display: false }
            }
          },
          onClick: (e, activeEls) => {
            if (activeEls.length) {
              const theme = themeLabels[activeEls[0].index];
              activeFilters.theme = theme;
              updateFilters();
            }
          }
        }
      });

      themeTableBody.innerHTML = '';
      themes.forEach(([theme, count], i) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${theme}</td>
          <td>${count.toLocaleString()}</td>
          <td>${themePercents[i]}%</td>
          <td>${themeYears[i]}</td>
        `;
        themeTableBody.appendChild(row);
      });

      // Timeline chart
      const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
      const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
      const timelineData = {};
      mechanisms.forEach(m => {
        timelineData[m] = {};
        years.forEach(y => {
          timelineData[m][y] = 0;
        });
      });
      filteredRecords.forEach(r => {
        timelineData[r.mechanism][r.year]++;
      });

      const datasets = mechanisms.map(m => ({
        label: m,
        data: years.map(y => timelineData[m][y]),
        backgroundColor: m === 'Universal Periodic Review' ? '#c2410c' : m === 'Treaty bodies' ? '#0f766e' : '#7c3aed'
      }));

      if (timelineChart) timelineChart.destroy();
      timelineChart = new Chart(timelineChartCanvas, {
        type: 'bar',
        data: {
          labels: years,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: context => `${context.dataset.label}: ${context.raw} records`
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              title: { display: true, text: 'Year' }
            },
            y: {
              stacked: true,
              title: { display: true, text: 'Records' },
              ticks: {
                callback: value => value.toLocaleString()
              }
            }
          }
        }
      });
    }

    // Records
    function updateTable() {
      // Sort
      const sortedRecords = [...filteredRecords].sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        if (dateA > dateB) return sortDirection === 'desc' ? -1 : 1;
        if (dateA < dateB) return sortDirection === 'desc' ? 1 : -1;
        if (a.body < b.body) return -1;
        if (a.body > b.body) return 1;
        const paraA = a.paragraphNumber || '';
        const paraB = b.paragraphNumber || '';
        return paraA.localeCompare(paraB, undefined, { numeric: true });
      });

      // Search
      const searchTerm = searchInput.value.trim().toLowerCase();
      const searchedRecords = searchTerm
        ? sortedRecords.filter(r => {
            const text = (r.text + ' ' + r.symbol).toLowerCase();
            return text.includes(searchTerm);
          })
        : sortedRecords;

      // Table
      tableCaption.textContent = `${searchedRecords.length.toLocaleString()} records match (newest first)`;
      tableBody.innerHTML = '';

      const rowsToShow = searchedRecords.slice(0, visibleRows);
      rowsToShow.forEach(record => {
        const tr = document.createElement('tr');
        tr.setAttribute('tabindex', '0');
        tr.setAttribute('role', 'button');
        tr.setAttribute('aria-expanded', 'false');

        const date = new Date(record.date).toLocaleDateString('en-CA');
        const body = record.body;
        const symbol = record.symbol;
        const docUrl = record.doc_url;
        const para = record.paragraphNumber || '–';
        const firstLine = record.text.substring(0, 120).replace(/\s+\S*$/, '') + (record.text.length > 120 ? '…' : '');
        const state = record.mechanism === 'Universal Periodic Review' && record.recommendingStates
          ? record.recommendingStates.join(', ')
          : '–';

        const highlightedFirstLine = searchTerm
          ? firstLine.replace(new RegExp(searchTerm.split(/\s+/).join('|'), 'gi'), match => `<mark>${match}</mark>`)
          : firstLine;

        tr.innerHTML = `
          <td>${date}</td>
          <td>${body}</td>
          <td><a href="${docUrl}" target="_blank">${symbol}</a></td>
          <td>${para}</td>
          <td>${highlightedFirstLine}</td>
          <td>${state}</td>
        `;

        tr.addEventListener('click', () => {
          const isExpanded = tr.getAttribute('aria-expanded') === 'true';
          tr.setAttribute('aria-expanded', !isExpanded);
          if (!isExpanded) {
            const expandedContent = document.createElement('tr');
            expandedContent.className = 'expanded';
            expandedContent.innerHTML = `
              <td colspan="6">
                <div class="expanded-content">
                  <div class="expanded-number">${record.paragraphNumber || '–'}</div>
                  <div class="expanded-text">${record.text}</div>
                  <div class="expanded-labels">
                    ${(record.themes || []).map(theme => `<span class="expanded-label">${theme}</span>`).join('')}
                    ${(record.sdgs || []).map(sdg => `<span class="expanded-label">SDG ${sdg}: ${sdgNames[sdg]}</span>`).join('')}
                    ${(record.sdg_targets || []).map(target => `<span class="expanded-label">${target}</span>`).join('')}
                    ${(record.affected_persons || []).map(person => `<span class="expanded-label">${person}</span>`).join('')}
                    ${record.section ? `<span class="expanded-label">Section: ${record.section}</span>` : ''}
                  </div>
                  <div class="expanded-actions">
                    <button class="copy-citation" data-symbol="${symbol}" data-para="${record.paragraphNumber || ''}">Copy citation</button>
                    <button class="open-document" data-url="${docUrl}">Open the UN document</button>
                  </div>
                </div>
              </td>
            `;
            tr.after(expandedContent);
            expandedContent.querySelector('.copy-citation').addEventListener('click', (e) => {
              const symbol = e.target.getAttribute('data-symbol');
              const para = e.target.getAttribute('data-para');
              const citation = para ? `${symbol}, para. ${para}` : symbol;
              navigator.clipboard.writeText(citation).then(() => {
                copiedNotice.style.opacity = '1';
                setTimeout(() => { copiedNotice.style.opacity = '0'; }, 2000);
              });
            });
            expandedContent.querySelector('.open-document').addEventListener('click', (e) => {
              window.open(e.target.getAttribute('data-url'), '_blank');
            });
          } else {
            tr.nextElementSibling.remove();
          }
        });

        tr.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
            tr.click();
          }
        });

        tableBody.appendChild(tr);
      });

      showMore.hidden = visibleRows >= searchedRecords.length;
    }

    // Check
    function updateChecks() {
      // Self-checks
      checkList.innerHTML = '';

      // Record count
      const recordCountCheck = document.createElement('div');
      recordCountCheck.className = 'check-item';
      if (records.length === count) {
        recordCountCheck.textContent = `✓ Record count: ${records.length.toLocaleString()} (matches the file)`;
      } else {
        recordCountCheck.innerHTML = `<span class="check-fail">✗ Record count: ${records.length.toLocaleString()} (file says ${count.toLocaleString()})</span>`;
      }
      checkList.appendChild(recordCountCheck);

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

      const mechanismCheck = document.createElement('div');
      mechanismCheck.className = 'check-item';
      if (mechanismSum === records.length) {
        mechanismCheck.textContent = `✓ Mechanism partition: ${mechanismSum.toLocaleString()} (sums to record count)`;
      } else {
        mechanismCheck.innerHTML = `<span class="check-fail">✗ Mechanism partition: ${mechanismSum.toLocaleString()} (record count ${records.length.toLocaleString()})</span>`;
      }
      checkList.appendChild(mechanismCheck);

      const bodyCheck = document.createElement('div');
      bodyCheck.className = 'check-item';
      if (bodySum === records.length) {
        bodyCheck.textContent = `✓ Body partition: ${bodySum.toLocaleString()} (sums to record count)`;
      } else {
        bodyCheck.innerHTML = `<span class="check-fail">✗ Body partition: ${bodySum.toLocaleString()} (record count ${records.length.toLocaleString()})</span>`;
      }
      checkList.appendChild(bodyCheck);

      const yearCheck = document.createElement('div');
      yearCheck.className = 'check-item';
      if (yearSum === records.length) {
        yearCheck.textContent = `✓ Year partition: ${yearSum.toLocaleString()} (sums to record count)`;
      } else {
        yearCheck.innerHTML = `<span class="check-fail">✗ Year partition: ${yearSum.toLocaleString()} (record count ${records.length.toLocaleString()})</span>`;
      }
      checkList.appendChild(yearCheck);

      // Type partition
      const typeCounts = {};
      records.forEach(r => {
        typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
      });
      const typeSum = Object.values(typeCounts).reduce((a, b) => a + b, 0);
      const typeCheck = document.createElement('div');
      typeCheck.className = 'check-item';
      if (typeSum === records.length) {
        typeCheck.textContent = `✓ Type partition: ${typeSum.toLocaleString()} (sums to record count)`;
      } else {
        typeCheck.innerHTML = `<span class="check-fail">✗ Type partition: ${typeSum.toLocaleString()} (record count ${records.length.toLocaleString()})</span>`;
      }
      checkList.appendChild(typeCheck);

      // Chart against table
      const themeCounts = {};
      filteredRecords.forEach(r => {
        (r.themes || []).forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      });
      const themes = Object.entries(themeCounts)
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 10);
      const chartValues = themes.map(([, count]) => count);
      const tableValues = Array.from(themeTableBody.querySelectorAll('tr')).map(tr => {
        const td = tr.querySelector('td:nth-child(2)');
        return td ? Number(td.textContent.replace(/,/g, '')) : 0;
      });
      const chartTableMatch = chartValues.every((v, i) => v === tableValues[i]);
      const chartCheck = document.createElement('div');
      chartCheck.className = 'check-item';
      if (chartTableMatch) {
        chartCheck.textContent = `✓ Chart against table: values match`;
      } else {
        chartCheck.innerHTML = `<span class="check-fail">✗ Chart against table: values differ</span>`;
      }
      checkList.appendChild(chartCheck);

      // Links
      const linkErrors = records.filter(r => !r.doc_url.startsWith('https://docs.un.org/') || !decodeURIComponent(r.doc_url).toLowerCase().endsWith(r.symbol.toLowerCase()));
      const linkCheck = document.createElement('div');
      linkCheck.className = 'check-item';
      if (linkErrors.length === 0) {
        linkCheck.textContent = `✓ Links: all ${records.length.toLocaleString()} records have valid doc_url`;
      } else {
        linkCheck.innerHTML = `<span class="check-fail">✗ Links: ${linkErrors.length} records have invalid doc_url (shown below)</span>`;
        linkErrors.forEach(r => {
          const error = document.createElement('div');
          error.style.fontSize = '0.8rem';
          error.style.marginLeft = '1rem';
          error.textContent = `${r.symbol}: ${r.doc_url}`;
          linkCheck.appendChild(error);
        });
      }
      checkList.appendChild(linkCheck);

      // Paragraph numbers
      const paraStats = {};
      ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'].forEach(m => {
        const records = filteredRecords.filter(r => r.mechanism === m);
        const withPara = records.filter(r => r.paragraphNumber).length;
        paraStats[m] = { total: records.length, withPara, percent: records.length ? Math.round((withPara / records.length) * 100) : 0 };
      });
      const paraCheck = document.createElement('div');
      paraCheck.className = 'check-item';
      paraCheck.textContent = `Paragraph numbers: UPR ${paraStats['Universal Periodic Review'].percent}% (${paraStats['Universal Periodic Review'].withPara}/${paraStats['Universal Periodic Review'].total}), Treaty bodies ${paraStats['Treaty bodies'].percent}% (${paraStats['Treaty bodies'].withPara}/${paraStats['Treaty bodies'].total}), Special Procedures ${paraStats['Special Procedures'].percent}% (${paraStats['Special Procedures'].withPara}/${paraStats['Special Procedures'].total})`;
      checkList.appendChild(paraCheck);

      // States found
      const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
      const uprWithState = uprRecords.filter(r => r.recommendingStates && r.recommendingStates.length).length;
      const stateCheck = document.createElement('div');
      stateCheck.className = 'check-item';
      if (uprWithState === uprRecords.length) {
        stateCheck.textContent = `✓ States found: all ${uprRecords.length.toLocaleString()} UPR records have at least one State`;
      } else {
        stateCheck.innerHTML = `<span class="check-fail">✗ States found: ${uprWithState} of ${uprRecords.length.toLocaleString()} UPR records have a State (${uprRecords.length - uprWithState} missing, shown below)</span>`;
        const missing = uprRecords.filter(r => !r.recommendingStates || !r.recommendingStates.length);
        missing.forEach(r => {
          const error = document.createElement('div');
          error.style.fontSize = '0.8rem';
          error.style.marginLeft = '1rem';
          error.textContent = `${r.symbol}: "${r.text}"`;
          stateCheck.appendChild(error);
        });
      }
      checkList.appendChild(stateCheck);

      // Duplicates and gaps
      const ids = new Set(records.map(r => r.id));
      const duplicateIds = records.filter(r => {
        const firstIndex = records.findIndex(rec => rec.id === r.id);
        return firstIndex !== records.indexOf(r);
      });
      const duplicateIdCheck = document.createElement('div');
      duplicateIdCheck.className = 'check-item';
      if (ids.size === records.length && duplicateIds.length === 0) {
        duplicateIdCheck.textContent = `✓ IDs: ${ids.size.toLocaleString()} distinct (no duplicates)`;
      } else {
        duplicateIdCheck.innerHTML = `<span class="check-fail">✗ IDs: ${ids.size.toLocaleString()} distinct (${duplicateIds.length} duplicates)</span>`;
      }
      checkList.appendChild(duplicateIdCheck);

      const duplicateTexts = records.filter(r => {
        const firstIndex = records.findIndex(rec => rec.text === r.text);
        return firstIndex !== records.indexOf(r);
      });
      const duplicateTextCheck = document.createElement('div');
      duplicateTextCheck.className = 'check-item';
      duplicateTextCheck.textContent = `Duplicate texts: ${new Set(duplicateTexts.map(r => r.text)).size} records`;
      checkList.appendChild(duplicateTextCheck);

      const noThemes = records.filter(r => !r.themes || r.themes.length === 0).length;
      const noSdgs = records.filter(r => !r.sdgs || r.sdgs.length === 0).length;
      const noAffected = records.filter(r => !r.affected_persons || r.affected_persons.length === 0).length;
      const gapsCheck = document.createElement('div');
      gapsCheck.className = 'check-item';
      gapsCheck.textContent = `Not labelled: ${noThemes.toLocaleString()} records without themes, ${noSdgs.toLocaleString()} without SDGs, ${noAffected.toLocaleString()} without affected persons`;
      checkList.appendChild(gapsCheck);
    }

    function drawSampleCards(seed = 1) {
      sampleVerdicts = {};
      sampleCards.innerHTML = '';

      // Seeded random (mulberry32)
      function mulberry32(a) {
        return function() {
          a |= 0; a = a + 0x6D2B79F5 | 0;
          let t = Math.imul(a ^ a >>> 15, 1 | a);
          t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
          return ((t ^ t >>> 14) >>> 0) / 4294967296;
        };
      }
      const random = mulberry32(seed);

      // Sample 10 from filteredRecords
      const sample = [];
      const indices = new Set();
      while (indices.size < 10 && indices.size < filteredRecords.length) {
        const index = Math.floor(random() * filteredRecords.length);
        indices.add(index);
      }
      indices.forEach(index => {
        sample.push(filteredRecords[index]);
      });

      // Draw cards
      sample.forEach((record, i) => {
        const card = document.createElement('div');
        card.className = 'sample-card';
        card.innerHTML = `
          <div class="sample-card-header" aria-expanded="false">
            <span><a href="${record.doc_url}" target="_blank">${record.symbol}</a>, para. ${record.paragraphNumber || '–'}</span>
          </div>
          <div class="sample-card-content">
            <div class="sample-card-text">${record.text}</div>
            <div class="sample-card-labels">
              ${(record.themes || []).map(theme => `<span class="sample-card-label">${theme}</span>`).join('')}
            </div>
            <div class="sample-card-actions">
              <button data-verdict="fit">Fits</button>
              <button data-verdict="nofit">Doesn't fit</button>
              <button data-verdict="unsure">Unsure</button>
            </div>
          </div>
        `;
        sampleCards.appendChild(card);

        const header = card.querySelector('.sample-card-header');
        const content = card.querySelector('.sample-card-content');
        header.addEventListener('click', () => {
          const isExpanded = header.getAttribute('aria-expanded') === 'true';
          header.setAttribute('aria-expanded', !isExpanded);
        });

        const buttons = card.querySelectorAll('.sample-card-actions button');
        buttons.forEach(button => {
          button.addEventListener('click', () => {
            buttons.forEach(b => b.style.fontWeight = 'normal');
            button.style.fontWeight = 'bold';
            sampleVerdicts[i] = button.getAttribute('data-verdict');
            updateSampleTally();
          });
        });
      });

      updateSampleTally();
    }

    function updateSampleTally() {
      const fit = Object.values(sampleVerdicts).filter(v => v === 'fit').length;
      const nofit = Object.values(sampleVerdicts).filter(v => v === 'nofit').length;
      const unsure = Object.values(sampleVerdicts).filter(v => v === 'unsure').length;
      sampleTally.textContent = `Themes: ${fit} fit, ${nofit} don't, ${unsure} unsure of 10 judged (seed ${sampleSeed.value})`;
    }

    // Export
    function downloadCsvFile() {
      const headers = [
        'Date', 'Body', 'Symbol', 'Paragraph', 'First line', 'Recommending State',
        'Themes', 'SDGs', 'SDG targets', 'Affected persons', 'Section', 'Full text'
      ];
      const rows = filteredRecords.map(record => {
        const date = new Date(record.date).toISOString().split('T')[0];
        const body = record.body;
        const symbol = record.symbol;
        const para = record.paragraphNumber || '';
        const firstLine = record.text.substring(0, 120).replace(/\s+\S*$/, '') + (record.text.length > 120 ? '…' : '');
        const state = record.mechanism === 'Universal Periodic Review' && record.recommendingStates
          ? record.recommendingStates.join('; ')
          : '';
        const themes = (record.themes || []).join('; ');
        const sdgs = (record.sdgs || []).map(s => `${s}: ${sdgNames[s]}`).join('; ');
        const sdgTargets = (record.sdg_targets || []).join('; ');
        const affected = (record.affected_persons || []).join('; ');
        const section = record.section || '';

        return [
          `"${date}"`, `"${body}"`, `"${symbol}"`, `"${para}"`, `"${firstLine.replace(/"/g, '""')}"`, `"${state}"`,
          `"${themes}"`, `"${sdgs}"`, `"${sdgTargets}"`, `"${affected}"`, `"${section}"`, `"${record.text.replace(/"/g, '""')}"`
        ].join(',');
      });

      const csv = [
        `# UN human rights recommendations and observations: ${country}`,
        `# Source: ${source} (${sourceUrl})`,
        `# Built: ${built}`,
        `# Filters: ${JSON.stringify(activeFilters)}`,
        `# Records: ${filteredRecords.length}`,
        headers.join(','),
        ...rows
      ].join('\n');

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `uhri-${country.toLowerCase()}-${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    function copySummaryText() {
      const typeCounts = {};
      records.forEach(r => {
        typeCounts[r.type] = (typeCounts[r.type] || 0) + 1;
      });
      const typeBreakdown = Object.entries(typeCounts)
        .sort((a, b) => b[1] - a[1])
        .map(([type, count]) => `${type} ${count.toLocaleString()}`)
        .join(', ');

      const themeCounts = {};
      filteredRecords.forEach(r => {
        (r.themes || []).forEach(theme => {
          themeCounts[theme] = (themeCounts[theme] || 0) + 1;
        });
      });
      const themes = Object.entries(themeCounts)
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 10)
        .map(([theme, count]) => `${theme} (${count})`)
        .join(', ');

      const text = `UN human rights recommendations and observations: ${country}
Source: ${source} (${sourceUrl})
Records: ${filteredRecords.length.toLocaleString()} (${typeBreakdown})
Documents: ${new Set(filteredRecords.map(r => r.symbol)).size.toLocaleString()}
Years: ${Math.min(...filteredRecords.map(r => r.year))}–${Math.max(...filteredRecords.map(r => r.year))}
Top themes: ${themes}`;

      navigator.clipboard.writeText(text).then(() => {
        copiedNotice.style.opacity = '1';
        setTimeout(() => { copiedNotice.style.opacity = '0'; }, 2000);
      });
    }

    // Preprocess records
    function preprocessRecords() {
      records.forEach(record => {
        // Paragraph number
        const paraMatch = record.text.match(/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/);
        record.paragraphNumber = paraMatch ? paraMatch[1] : null;

        // Recommending State (UPR only)
        if (record.mechanism === 'Universal Periodic Review') {
          const stateMatch = record.text.match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
          if (stateMatch) {
            const groups = stateMatch[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
            record.recommendingStates = groups.map(g => {
              const state = g.slice(1, -1).trim();
              return state.includes(',') || state.length > 60 ? null : state;
            }).filter(s => s);
          } else {
            record.recommendingStates = [];
          }
        }
      });
    }

    preprocessRecords();
    init();
  </script>
</body>
</html>
```