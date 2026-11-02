I'll add an AI SDG suggestion feature with batching, progress tracking, stop capability, and side-by-side run comparison.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN Human Rights Recommendations — Kenya</title>
<style>
  :root {
    --accent: #1f6fb2;
    --accent-light: #e8f0f7;
    --bg: #f5f7fa;
    --card: #ffffff;
    --text: #1a1a2e;
    --muted: #5a6a7a;
    --border: #dde3ea;
    --radius: 10px;
    --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    font-size: 16px;
    line-height: 1.5;
    padding: 0 0 60px;
  }
  .container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }

  header {
    background: var(--card);
    border-bottom: 3px solid var(--accent);
    padding: 28px 0 20px;
    margin-bottom: 24px;
  }
  header h1 { font-size: 1.7rem; font-weight: 700; color: var(--text); letter-spacing: -0.01em; }
  header .subtitle { color: var(--muted); font-size: 0.95rem; margin-top: 6px; max-width: 800px; }

  .stats-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }
  .stat-card {
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 18px 22px;
    flex: 1 1 200px;
    min-width: 180px;
  }
  .stat-card .stat-value { font-size: 1.9rem; font-weight: 700; color: var(--accent); line-height: 1.2; }
  .stat-card .stat-label { font-size: 0.82rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }

  .card {
    background: var(--card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 22px 24px;
    margin-bottom: 24px;
  }
  .card h2 { font-size: 1.15rem; font-weight: 600; margin-bottom: 4px; }
  .card .note { font-size: 0.82rem; color: var(--muted); font-style: italic; margin-bottom: 14px; }

  .filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin-bottom: 12px;
  }
  .filter-grid label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }
  .filter-grid select, .filter-grid input[type="text"], .filter-grid input[type="number"] {
    padding: 8px 10px;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.95rem;
    font-family: inherit;
    background: #fff;
    color: var(--text);
    width: 100%;
  }
  .filter-grid select:focus, .filter-grid input:focus {
    outline: 2px solid var(--accent);
    outline-offset: 1px;
    border-color: var(--accent);
  }
  .year-range { display: flex; gap: 8px; align-items: center; }
  .year-range input { flex: 1; min-width: 0; }
  .year-range span { color: var(--muted); font-size: 0.9rem; }
  .reset-btn {
    background: var(--accent-light);
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s;
  }
  .reset-btn:hover { background: #d4e4f0; }

  .chart-container { position: relative; height: 400px; width: 100%; }
  .chart-empty {
    text-align: center;
    color: var(--muted);
    padding: 40px 0;
    font-style: italic;
  }

  .table-wrapper { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
  thead th {
    text-align: left;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--muted);
    border-bottom: 2px solid var(--border);
    padding: 10px 12px;
    white-space: nowrap;
  }
  tbody td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  .summary-row { cursor: pointer; transition: background 0.12s; }
  .summary-row:hover { background: #f0f5fa; }
  .summary-row.expanded { background: var(--accent-light); }
  .summary-row .chevron {
    display: inline-block;
    width: 18px;
    color: var(--accent);
    font-weight: 700;
    transition: transform 0.15s;
    user-select: none;
  }
  .summary-row.expanded .chevron { transform: rotate(90deg); }
  .summary-row a { color: var(--accent); text-decoration: none; font-weight: 600; }
  .summary-row a:hover { text-decoration: underline; }
  .summary-row .body-badge {
    display: inline-block;
    background: var(--accent-light);
    color: var(--accent);
    border-radius: 4px;
    padding: 1px 8px;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
  }
  .summary-row .text-preview { color: var(--text); }
  .detail-row td { background: #fafbfd; padding: 0; }
  .detail-content { padding: 16px 20px 18px; }
  .detail-content .full-text {
    font-size: 0.95rem;
    line-height: 1.65;
    color: var(--text);
    margin-bottom: 12px;
    white-space: pre-wrap;
  }
  .detail-meta { display: flex; flex-wrap: wrap; gap: 8px; }
  .detail-meta .meta-tag {
    background: #eef2f6;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.78rem;
    color: var(--muted);
  }
  .detail-meta .meta-tag strong { color: var(--text); font-weight: 600; }

  .pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 14px;
    gap: 12px;
    flex-wrap: wrap;
  }
  .pagination .page-info { font-size: 0.85rem; color: var(--muted); }
  .pagination .page-btns { display: flex; gap: 6px; }
  .pagination button {
    padding: 6px 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: #fff;
    cursor: pointer;
    font-size: 0.85rem;
    font-family: inherit;
    color: var(--text);
  }
  .pagination button:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
  .pagination button:disabled { opacity: 0.4; cursor: default; }

  .no-results {
    text-align: center;
    padding: 40px 20px;
    color: var(--muted);
    font-style: italic;
  }
  .footer-note {
    font-size: 0.78rem;
    color: var(--muted);
    text-align: center;
    margin-top: 8px;
  }

  /* AI section styles */
  .ai-controls { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 14px; }
  .ai-btn {
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: background 0.15s;
  }
  .ai-btn:hover:not(:disabled) { background: #185a8a; }
  .ai-btn:disabled { opacity: 0.5; cursor: default; }
  .ai-stop-btn {
    background: #c0392b;
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
  }
  .ai-stop-btn:hover { background: #a93226; }
  .ai-progress {
    font-size: 0.9rem;
    color: var(--muted);
    font-style: italic;
  }
  .ai-notice {
    background: #fff8e1;
    border: 1px solid #f5d76e;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 16px;
    font-size: 0.9rem;
    color: #6d5a00;
  }
  .ai-error {
    background: #fdecea;
    border: 1px solid #f5c6cb;
    border-radius: 6px;
    padding: 12px 16px;
    color: #721c24;
    font-size: 0.9rem;
  }
  .ai-agreement-rates { margin-bottom: 16px; }
  .ai-rate { margin-bottom: 4px; font-size: 0.95rem; }
  .ai-rate-label { font-weight: 600; color: var(--text); }
  .ai-rate-value { font-weight: 700; color: var(--accent); font-size: 1.1rem; }
  .ai-rate-detail { color: var(--muted); font-size: 0.85rem; }
  .ai-record-preview {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 2px;
    max-width: 300px;
  }
  .agree-yes { color: #1a7f37; font-weight: 700; font-size: 1.1rem; }
  .agree-partial { color: #b45309; font-weight: 700; font-size: 1.1rem; }
  .agree-no { color: #c0392b; font-weight: 700; font-size: 1.1rem; }
  .ai-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
  .ai-table th {
    text-align: left;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--muted);
    border-bottom: 2px solid var(--border);
    padding: 8px 10px;
    white-space: nowrap;
  }
  .ai-table td {
    padding: 8px 10px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  .ai-table a { color: var(--accent); text-decoration: none; font-weight: 600; }
  .ai-table a:hover { text-decoration: underline; }

  @media (max-width: 700px) {
    .stats-row { flex-direction: column; }
    .filter-grid { grid-template-columns: 1fr; }
    header h1 { font-size: 1.35rem; }
    .card { padding: 16px; }
  }
</style>
</head>
<body>

<header>
  <div class="container">
    <h1 id="pageTitle">UN Human Rights Recommendations</h1>
    <p class="subtitle" id="pageSubtitle"></p>
  </div>
</header>

<div class="container">

  <div class="stats-row" id="statsRow"></div>

  <section class="card" id="filtersCard">
    <h2>Filters</h2>
    <p class="note">Narrow the records by mechanism, body, year, SDG, or keyword. All filters combine.</p>
    <div class="filter-grid">
      <label>Mechanism
        <select id="filterMechanism"><option value="">All mechanisms</option></select>
      </label>
      <label>Treaty body / mandate
        <select id="filterBody"><option value="">All bodies</option></select>
      </label>
      <label>Year range
        <div class="year-range">
          <input type="number" id="filterYearFrom" min="0" max="2100" step="1">
          <span>–</span>
          <input type="number" id="filterYearTo" min="0" max="2100" step="1">
        </div>
      </label>
      <label>SDG
        <select id="filterSdg"><option value="">All SDGs</option></select>
      </label>
      <label>Keyword search
        <input type="text" id="filterKeyword" placeholder="Search in text and themes…">
      </label>
    </div>
    <button class="reset-btn" id="resetBtn">Reset all filters</button>
  </section>

  <section class="card" id="chartCard">
    <h2>Top 10 themes</h2>
    <p class="note">How this is computed: each record can carry multiple themes. The chart counts how many of the currently filtered records mention each theme, and shows the 10 most frequent.</p>
    <div class="chart-container">
      <canvas id="themeChart"></canvas>
      <div class="chart-empty" id="chartEmpty" style="display:none;">No themes found in the current selection.</div>
    </div>
  </section>

  <section class="card" id="tableCard">
    <h2>Matching records <span id="tableCount" style="font-weight:400;color:var(--muted);font-size:0.9rem;"></span></h2>
    <p class="note">Each row is one paragraph from a UN document. Click a row to read the full text. The symbol links to the official document.</p>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th style="width:30px;"></th>
            <th>Date</th>
            <th>Body</th>
            <th>Symbol</th>
            <th>Text</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
    <div class="no-results" id="noResults" style="display:none;">No records match the current filters.</div>
    <div class="pagination" id="pagination" style="display:none;">
      <span class="page-info" id="pageInfo"></span>
      <div class="page-btns">
        <button id="prevBtn" disabled>← Previous</button>
        <button id="nextBtn" disabled>Next →</button>
      </div>
    </div>
  </section>

  <section class="card" id="aiCard">
    <h2>AI SDG Suggestions</h2>
    <p class="note">How this works: the first 50 records of the current filter are sent to an external language model, which assigns SDG numbers to each record. The AI's assignments are compared with the UN's official SDG tags. Agreement rate = percentage of records where the AI's assignment exactly matches the UN's.</p>
    <div class="ai-controls">
      <button class="ai-btn" id="aiRunBtn">Suggest SDGs with AI</button>
      <button class="ai-stop-btn" id="aiStopBtn" style="display:none;">Stop</button>
      <span class="ai-progress" id="aiProgress" style="display:none;"></span>
    </div>
    <div class="ai-notice" id="aiNotice" style="display:none;"></div>
    <div id="aiResults" style="display:none;"></div>
  </section>

  <p class="footer-note" id="footerNote"></p>
</div>

<script>
(function() {
  const data = window.WORKSHOP_DATA && window.WORKSHOP_DATA.uhri;
  if (!data || !data.records || data.records.length === 0) {
    document.getElementById('pageTitle').textContent = 'No data available';
    document.getElementById('pageSubtitle').textContent = 'The UHRI dataset could not be loaded.';
    return;
  }

  const records = data.records;
  const country = data.country || 'this country';
  const sdgNames = data.sdg_names || {};
  const sourceLabel = data.source || 'Universal Human Rights Index (UHRI)';

  const years = records.map(r => r.year).filter(y => typeof y === 'number' && !isNaN(y));
  const minYear = years.length ? Math.min(...years) : null;
  const maxYear = years.length ? Math.max(...years) : null;

  const mechanisms = [...new Set(records.map(r => r.mechanism).filter(Boolean))].sort();
  const bodies = [...new Set(records.map(r => r.body).filter(Boolean))].sort();

  const state = {
    mechanism: '',
    body: '',
    yearFrom: minYear !== null ? minYear : 0,
    yearTo: maxYear !== null ? maxYear : 2100,
    sdg: '',
    keyword: '',
    page: 1
  };
  const PAGE_SIZE = 20;
  let chartInstance = null;

  const $ = id => document.getElementById(id);
  const elMechanism = $('filterMechanism');
  const elBody = $('filterBody');
  const elYearFrom = $('filterYearFrom');
  const elYearTo = $('filterYearTo');
  const elSdg = $('filterSdg');
  const elKeyword = $('filterKeyword');
  const elReset = $('resetBtn');
  const elTableBody = $('tableBody');
  const elNoResults = $('noResults');
  const elPagination = $('pagination');
  const elPageInfo = $('pageInfo');
  const elPrevBtn = $('prevBtn');
  const elNextBtn = $('nextBtn');
  const elTableCount = $('tableCount');
  const elChartEmpty = $('chartEmpty');
  const elThemeChart = $('themeChart');

  document.getElementById('pageTitle').textContent = 'UN Human Rights Recommendations — ' + country;
  const yearRangeStr = minYear !== null && maxYear !== null
    ? (minYear === maxYear ? String(minYear) : minYear + '–' + maxYear)
    : 'unknown years';
  document.getElementById('pageSubtitle').textContent =
    sourceLabel + ' · ' + records.length.toLocaleString() + ' records · ' + yearRangeStr +
    ' · Recommendations and observations from UN treaty bodies, the Universal Periodic Review, and Special Procedures.';
  document.getElementById('footerNote').textContent =
    'Source: ' + sourceLabel + '. Each record is one paragraph from an official UN document.';

  function renderStats() {
    const statsRow = $('statsRow');
    statsRow.innerHTML = '';
    const cards = [
      { value: records.length.toLocaleString(), label: 'Total records' },
      { value: yearRangeStr, label: 'Year range' },
      { value: String(mechanisms.length), label: 'Mechanisms' },
      { value: String(bodies.length), label: 'Bodies / mandates' }
    ];
    cards.forEach(c => {
      const div = document.createElement('div');
      div.className = 'stat-card';
      div.innerHTML = '<div class="stat-value">' + c.value + '</div><div class="stat-label">' + c.label + '</div>';
      statsRow.appendChild(div);
    });
  }

  mechanisms.forEach(m => {
    const opt = document.createElement('option');
    opt.value = m;
    opt.textContent = m;
    elMechanism.appendChild(opt);
  });
  bodies.forEach(b => {
    const opt = document.createElement('option');
    opt.value = b;
    opt.textContent = b;
    elBody.appendChild(opt);
  });
  for (let i = 1; i <= 17; i++) {
    const name = sdgNames[String(i)] || '';
    const opt = document.createElement('option');
    opt.value = String(i);
    opt.textContent = name ? 'SDG ' + i + ': ' + name : 'SDG ' + i;
    elSdg.appendChild(opt);
  }
  elYearFrom.min = minYear !== null ? minYear : 0;
  elYearFrom.max = maxYear !== null ? maxYear : 2100;
  elYearTo.min = minYear !== null ? minYear : 0;
  elYearTo.max = maxYear !== null ? maxYear : 2100;
  elYearFrom.value = state.yearFrom;
  elYearTo.value = state.yearTo;

  function formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    return d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear();
  }

  function firstLine(text) {
    if (!text) return '';
    const clean = String(text).trim();
    const match = clean.match(/^(.{0,200}?[.!?])(?:\s|$)/);
    if (match && match[1].length > 20) return match[1];
    return clean.slice(0, 200) + (clean.length > 200 ? '…' : '');
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function getFiltered() {
    const kw = state.keyword.trim().toLowerCase();
    return records.filter(r => {
      if (state.mechanism && r.mechanism !== state.mechanism) return false;
      if (state.body && r.body !== state.body) return false;
      if (typeof r.year === 'number' && (r.year < state.yearFrom || r.year > state.yearTo)) return false;
      if (state.sdg) {
        const sdgNum = parseInt(state.sdg, 10);
        if (!(r.sdgs || []).includes(sdgNum)) return false;
      }
      if (kw) {
        const haystack = ((r.text || '') + ' ' + (r.themes || []).join(' ') + ' ' + (r.body || '')).toLowerCase();
        if (!haystack.includes(kw)) return false;
      }
      return true;
    }).sort((a, b) => {
      const da = a.date || '';
      const db = b.date || '';
      if (da !== db) return db.localeCompare(da);
      return (b.year || 0) - (a.year || 0);
    });
  }

  function countThemes(filtered) {
    const counts = {};
    filtered.forEach(r => {
      (r.themes || []).forEach(t => {
        if (t) counts[t] = (counts[t] || 0) + 1;
      });
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  }

  function renderChart(filtered) {
    const themes = countThemes(filtered);
    if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
    if (themes.length === 0) {
      elChartEmpty.style.display = 'block';
      elThemeChart.style.display = 'none';
      return;
    }
    elChartEmpty.style.display = 'none';
    elThemeChart.style.display = 'block';
    const ctx = elThemeChart.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: themes.map(t => t[0]),
        datasets: [{
          label: 'Records',
          data: themes.map(t => t[1]),
          backgroundColor: '#1f6fb2',
          borderRadius: 4,
          barThickness: 22
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
              label: function(ctx) { return ctx.parsed.x + ' record' + (ctx.parsed.x !== 1 ? 's' : ''); }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            ticks: { precision: 0, font: { size: 13 } },
            grid: { color: '#eef2f6' }
          },
          y: {
            ticks: {
              font: { size: 12 },
              callback: function(value) {
                const label = this.getLabelForValue(value);
                return label.length > 45 ? label.slice(0, 42) + '…' : label;
              }
            },
            grid: { display: false }
          }
        }
      }
    });
  }

  function renderTable(filtered) {
    elTableBody.innerHTML = '';
    elTableCount.textContent = '(' + filtered.length.toLocaleString() + ' record' + (filtered.length !== 1 ? 's' : '') + ')';

    if (filtered.length === 0) {
      elNoResults.style.display = 'block';
      elPagination.style.display = 'none';
      return;
    }
    elNoResults.style.display = 'none';

    const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    if (state.page > totalPages) state.page = totalPages;
    if (state.page < 1) state.page = 1;
    const start = (state.page - 1) * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, filtered.length);
    const pageRecords = filtered.slice(start, end);

    pageRecords.forEach((r, idx) => {
      const rowId = 'row-' + start + '-' + idx;
      const detailId = 'detail-' + start + '-' + idx;

      const trSummary = document.createElement('tr');
      trSummary.className = 'summary-row';
      trSummary.setAttribute('data-detail-id', detailId);
      trSummary.setAttribute('aria-expanded', 'false');

      const tdChevron = document.createElement('td');
      tdChevron.innerHTML = '<span class="chevron">▶</span>';
      trSummary.appendChild(tdChevron);

      const tdDate = document.createElement('td');
      tdDate.textContent = formatDate(r.date);
      tdDate.style.whiteSpace = 'nowrap';
      trSummary.appendChild(tdDate);

      const tdBody = document.createElement('td');
      tdBody.innerHTML = '<span class="body-badge">' + (r.body || '—') + '</span>';
      trSummary.appendChild(tdBody);

      const tdSymbol = document.createElement('td');
      if (r.doc_url) {
        tdSymbol.innerHTML = '<a href="' + r.doc_url + '" target="_blank" rel="noopener noreferrer">' + (r.symbol || '—') + '</a>';
      } else {
        tdSymbol.textContent = r.symbol || '—';
      }
      tdSymbol.style.whiteSpace = 'nowrap';
      trSummary.appendChild(tdSymbol);

      const tdText = document.createElement('td');
      tdText.className = 'text-preview';
      tdText.textContent = firstLine(r.text);
      trSummary.appendChild(tdText);

      trSummary.addEventListener('click', function(e) {
        if (e.target.closest('a')) return;
        const detailRow = document.getElementById(detailId);
        if (!detailRow) return;
        const isHidden = detailRow.hidden;
        detailRow.hidden = !isHidden;
        trSummary.classList.toggle('expanded', !isHidden);
        trSummary.setAttribute('aria-expanded', String(!isHidden));
      });

      elTableBody.appendChild(trSummary);

      const trDetail = document.createElement('tr');
      trDetail.className = 'detail-row';
      trDetail.id = detailId;
      trDetail.hidden = true;

      const tdDetail = document.createElement('td');
      tdDetail.colSpan = 5;
      const detailDiv = document.createElement('div');
      detailDiv.className = 'detail-content';

      const fullText = document.createElement('p');
      fullText.className = 'full-text';
      fullText.textContent = r.text || '(no text)';
      detailDiv.appendChild(fullText);

      const metaDiv = document.createElement('div');
      metaDiv.className = 'detail-meta';
      const metaItems = [];
      if (r.mechanism) metaItems.push('<strong>Mechanism:</strong> ' + r.mechanism);
      if (r.type) metaItems.push('<strong>Type:</strong> ' + r.type);
      if (r.section) metaItems.push('<strong>Section:</strong> ' + r.section);
      if (r.themes && r.themes.length) metaItems.push('<strong>Themes:</strong> ' + r.themes.join('; '));
      if (r.sdgs && r.sdgs.length) {
        const sdgLabels = r.sdgs.map(s => {
          const name = sdgNames[String(s)] || '';
          return 'SDG ' + s + (name ? ' (' + name + ')' : '');
        });
        metaItems.push('<strong>SDGs:</strong> ' + sdgLabels.join('; '));
      }
      if (r.affected_persons && r.affected_persons.length) metaItems.push('<strong>Affected persons:</strong> ' + r.affected_persons.join('; '));
      metaItems.forEach(m => {
        const span = document.createElement('span');
        span.className = 'meta-tag';
        span.innerHTML = m;
        metaDiv.appendChild(span);
      });
      detailDiv.appendChild(metaDiv);

      tdDetail.appendChild(detailDiv);
      trDetail.appendChild(tdDetail);
      elTableBody.appendChild(trDetail);
    });

    elPagination.style.display = 'flex';
    elPageInfo.textContent = 'Showing ' + (start + 1) + '–' + end + ' of ' + filtered.length.toLocaleString();
    elPrevBtn.disabled = state.page <= 1;
    elNextBtn.disabled = state.page >= totalPages;
  }

  function update() {
    const filtered = getFiltered();
    renderChart(filtered);
    renderTable(filtered);
  }

  // ==================== AI SDG Suggestions ====================
  const AI_MAX_RECORDS = 50;
  const AI_BATCH_SIZE = 25;
  const MAX_AI_RUNS = 3;

  let aiGeneration = 0;
  const aiState = {
    running: false,
    stopRequested: false,
    recordIds: [],
    runs: []
  };

  const elAIRunBtn = $('aiRunBtn');
  const elAIStopBtn = $('aiStopBtn');
  const elAIProgress = $('aiProgress');
  const elAINotice = $('aiNotice');
  const elAIResults = $('aiResults');

  function clearAIState() {
    aiGeneration++;
    aiState.recordIds = [];
    aiState.runs = [];
    aiState.running = false;
    aiState.stopRequested = false;
    elAIRunBtn.textContent = 'Suggest SDGs with AI';
    elAIRunBtn.disabled = false;
    elAIStopBtn.style.display = 'none';
    elAIProgress.style.display = 'none';
    elAINotice.style.display = 'none';
    elAIResults.style.display = 'none';
    elAIResults.innerHTML = '';
  }

  function updateAIButtons() {
    if (aiState.running) {
      elAIRunBtn.disabled = true;
      elAIStopBtn.style.display = 'inline-block';
    } else {
      elAIRunBtn.disabled = aiState.runs.length >= MAX_AI_RUNS;
      elAIStopBtn.style.display = 'none';
      elAIRunBtn.textContent = aiState.runs.length > 0 ? 'Run again' : 'Suggest SDGs with AI';
    }
  }

  function updateAIProgress() {
    elAIProgress.style.display = 'inline';
    const batchSize = Math.min(AI_BATCH_SIZE, aiState.recordIds.length - (aiState.currentBatch - 1) * AI_BATCH_SIZE);
    elAIProgress.textContent = 'Sending batch ' + aiState.currentBatch + ' of ' + aiState.totalBatches +
      ' (' + batchSize + ' records) to the model...';
  }

  function buildAIPrompt(batch) {
    const sdgList = [];
    for (let i = 1; i <= 17; i++) {
      const name = sdgNames[String(i)] || '';
      sdgList.push(i + ': ' + name);
    }
    const recordsJson = batch.map(r => JSON.stringify({ id: r.id, text: r.text }));
    return 'You are analyzing UN human rights recommendations. For each record below, assign the Sustainable Development Goals (SDGs, numbered 1-17) that the recommendation most directly relates to. Return ONLY a JSON object mapping record IDs to arrays of SDG numbers. Example: {"abc123": [16, 5], "def456": []}. If no SDG clearly applies, use an empty array. Do not include any explanation or markdown formatting.\n\nSDG reference:\n' + sdgList.join('\n') + '\n\nRecords:\n' + recordsJson.join('\n');
  }

  function parseAIResponse(response) {
    if (typeof response !== 'string') {
      if (typeof response === 'object' && response !== null) return response;
      throw new Error('Unexpected response format from model.');
    }
    let text = response.trim();
    text = text.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
    const start = text.indexOf('{');
    const end = text.lastIndexOf('}');
    if (start === -1 || end === -1 || end <= start) {
      throw new Error('Could not find JSON in model response.');
    }
    try {
      const parsed = JSON.parse(text.slice(start, end + 1));
      if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
        throw new Error('Model returned unexpected JSON structure.');
      }
      return parsed;
    } catch (e) {
      if (e.message && e.message.includes('Model returned')) throw e;
      throw new Error('Model returned invalid JSON.');
    }
  }

  function normalizeSDGs(sdgs) {
    if (!Array.isArray(sdgs)) return [];
    return sdgs
      .map(s => typeof s === 'string' ? parseInt(s, 10) : s)
      .filter(s => Number.isInteger(s) && s >= 1 && s <= 17)
      .sort((a, b) => a - b);
  }

  function setsEqual(a, b) {
    if (a.length !== b.length) return false;
    const setA = new Set(a);
    const setB = new Set(b);
    if (setA.size !== setB.size) return false;
    for (const x of setA) {
      if (!setB.has(x)) return false;
    }
    return true;
  }

  function setsOverlap(a, b) {
    const setA = new Set(a);
    return b.some(x => setA.has(x));
  }

  function showAIError(msg) {
    elAIResults.style.display = 'block';
    elAIResults.innerHTML = '<div class="ai-error">⚠️ ' + escapeHtml(msg) + '</div>';
  }

  function renderAINotice() {
    elAINotice.style.display = 'block';
    elAINotice.innerHTML = '⚠️ <strong>' + aiState.recordIds.length + ' record texts</strong> were sent to an external language model for SDG classification. Running the analysis again can produce different results.';
  }

  function renderAIResults() {
    const runs = aiState.runs;
    if (runs.length === 0) return;

    const recordsById = {};
    records.forEach(r => { recordsById[r.id] = r; });
    const recordIds = aiState.recordIds;

    const rates = runs.map(run => {
      let exact = 0, partial = 0, none = 0;
      recordIds.forEach(id => {
        const unSdgs = (recordsById[id]?.sdgs || []).slice().sort((a, b) => a - b);
        const aiSdgs = (run.results.get(id) || []).slice().sort((a, b) => a - b);
        if (setsEqual(unSdgs, aiSdgs)) exact++;
        else if (setsOverlap(unSdgs, aiSdgs)) partial++;
        else none++;
      });
      return { exact, partial, none, total: recordIds.length, rate: recordIds.length ? (exact / recordIds.length * 100) : 0 };
    });

    let html = '';
    html += '<div class="ai-agreement-rates" data-source="ai">';
    runs.forEach((run, i) => {
      const r = rates[i];
      html += '<div class="ai-rate">';
      html += '<span class="ai-rate-label">Run ' + (i + 1) + ' agreement rate:</span> ';
      html += '<span class="ai-rate-value">' + r.rate.toFixed(0) + '%</span> ';
      html += '<span class="ai-rate-detail">(' + r.exact + ' exact, ' + r.partial + ' partial, ' + r.none + ' no overlap)</span>';
      html += '</div>';
    });
    html += '</div>';

    html += '<div class="table-wrapper"><table class="ai-table">';
    html += '<thead><tr><th>Record</th><th>UN SDGs</th>';
    runs.forEach((run, i) => {
      html += '<th>AI Run ' + (i + 1) + '</th><th>Agree</th>';
    });
    html += '</tr></thead><tbody>';

    recordIds.forEach(id => {
      const rec = recordsById[id];
      if (!rec) return;
      const unSdgs = (rec.sdgs || []).slice().sort((a, b) => a - b);

      html += '<tr>';
      html += '<td>';
      if (rec.doc_url) {
        html += '<a href="' + rec.doc_url + '" target="_blank" rel="noopener noreferrer">' + (rec.symbol || '—') + '</a>';
      } else {
        html += escapeHtml(rec.symbol || '—');
      }
      html += '<div class="ai-record-preview">' + escapeHtml(firstLine(rec.text)) + '</div>';
      html += '</td>';

      html += '<td>' + (unSdgs.length ? unSdgs.join(', ') : '—') + '</td>';

      runs.forEach((run, i) => {
        const aiSdgs = (run.results.get(id) || []).slice().sort((a, b) => a - b);
        html += '<td data-source="ai">' + (aiSdgs.length ? aiSdgs.join(', ') : '—') + '</td>';

        const isExact = setsEqual(unSdgs, aiSdgs);
        const isPartial = !isExact && setsOverlap(unSdgs, aiSdgs);
        const cls = isExact ? 'agree-yes' : (isPartial ? 'agree-partial' : 'agree-no');
        const sym = isExact ? '✓' : (isPartial ? '~' : '✗');
        const title = isExact ? 'Exact match' : (isPartial ? 'Partial overlap' : 'No overlap');
        html += '<td data-source="ai" class="' + cls + '" title="' + title + '">' + sym + '</td>';
      });

      html += '</tr>';
    });

    html += '</tbody></table></div>';
    elAIResults.innerHTML = html;
    elAIResults.style.display = 'block';
  }

  async function runAI() {
    if (aiState.running) return;
    if (aiState.runs.length >= MAX_AI_RUNS) return;
    if (typeof studio === 'undefined' || typeof studio.ask !== 'function') {
      showAIError('The AI model is not available in this environment.');
      return;
    }

    let targetRecords;
    if (aiState.recordIds.length > 0) {
      const recordsById = {};
      records.forEach(r => { recordsById[r.id] = r; });
      targetRecords = aiState.recordIds.map(id => recordsById[id]).filter(Boolean);
    } else {
      const filtered = getFiltered();
      targetRecords = filtered.slice(0, AI_MAX_RECORDS);
      aiState.recordIds = targetRecords.map(r => r.id);
    }

    if (targetRecords.length === 0) {
      showAIError('No records to analyze with the current filters.');
      return;
    }

    aiState.running = true;
    aiState.stopRequested = false;
    aiState.currentBatch = 0;
    aiState.totalBatches = Math.ceil(targetRecords.length / AI_BATCH_SIZE);

    const generation = aiGeneration;
    const results = new Map();

    updateAIButtons();

    try {
      for (let i = 0; i < targetRecords.length; i += AI_BATCH_SIZE) {
        if (aiState.stopRequested) break;
        if (generation !== aiGeneration) return;

        const batch = targetRecords.slice(i, i + AI_BATCH_SIZE);
        aiState.currentBatch++;
        updateAIProgress();

        const prompt = buildAIPrompt(batch);
        const response = await studio.ask(prompt, { json: true });
        const parsed = parseAIResponse(response);

        for (const [id, sdgs] of Object.entries(parsed)) {
          results.set(id, normalizeSDGs(sdgs));
        }
      }

      if (generation !== aiGeneration) return;

      if (!aiState.stopRequested) {
        aiState.runs.push({ results });
        renderAINotice();
        renderAIResults();
      } else if (results.size > 0) {
        aiState.runs.push({ results });
        renderAINotice();
        renderAIResults();
      }
    } catch (err) {
      if (generation === aiGeneration) {
        showAIError(err.message || 'An error occurred while contacting the model.');
      }
    } finally {
      if (generation === aiGeneration) {
        aiState.running = false;
        aiState.stopRequested = false;
        elAIProgress.style.display = 'none';
        updateAIButtons();
      }
    }
  }

  elAIRunBtn.addEventListener('click', runAI);
  elAIStopBtn.addEventListener('click', function() {
    aiState.stopRequested = true;
  });

  // ==================== Event listeners ====================
  elMechanism.addEventListener('change', function() {
    state.mechanism = this.value;
    state.page = 1;
    clearAIState();
    update();
  });
  elBody.addEventListener('change', function() {
    state.body = this.value;
    state.page = 1;
    clearAIState();
    update();
  });
  elYearFrom.addEventListener('change', function() {
    let v = parseInt(this.value, 10);
    if (isNaN(v)) v = minYear !== null ? minYear : 0;
    state.yearFrom = v;
    if (state.yearFrom > state.yearTo) state.yearTo = state.yearFrom;
    elYearTo.value = state.yearTo;
    state.page = 1;
    clearAIState();
    update();
  });
  elYearTo.addEventListener('change', function() {
    let v = parseInt(this.value, 10);
    if (isNaN(v)) v = maxYear !== null ? maxYear : 2100;
    state.yearTo = v;
    if (state.yearTo < state.yearFrom) state.yearFrom = state.yearTo;
    elYearFrom.value = state.yearFrom;
    state.page = 1;
    clearAIState();
    update();
  });
  elSdg.addEventListener('change', function() {
    state.sdg = this.value;
    state.page = 1;
    clearAIState();
    update();
  });
  let keywordTimer = null;
  elKeyword.addEventListener('input', function() {
    clearTimeout(keywordTimer);
    keywordTimer = setTimeout(function() {
      state.keyword = elKeyword.value;
      state.page = 1;
      clearAIState();
      update();
    }, 250);
  });
  elReset.addEventListener('click', function() {
    state.mechanism = '';
    state.body = '';
    state.yearFrom = minYear !== null ? minYear : 0;
    state.yearTo = maxYear !== null ? maxYear : 2100;
    state.sdg = '';
    state.keyword = '';
    state.page = 1;
    elMechanism.value = '';
    elBody.value = '';
    elYearFrom.value = state.yearFrom;
    elYearTo.value = state.yearTo;
    elSdg.value = '';
    elKeyword.value