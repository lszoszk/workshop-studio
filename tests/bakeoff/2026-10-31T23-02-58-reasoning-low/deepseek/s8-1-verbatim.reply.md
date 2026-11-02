I built a search tool for treaty body General Comments with boolean operators, phrase search, committee/year filters, highlighted matches, per-committee hit chart, and copy-citation buttons. The paragraph text is shown exactly as in the data.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments Search</title>
<style>
  :root {
    --accent: #1f6fb2;
    --accent-light: #e8f0f8;
    --border: #d0d7de;
    --text: #1f2328;
    --muted: #57606a;
    --bg: #f6f8fa;
    --card-bg: #ffffff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    font-size: 16px;
    padding: 0 1rem 2rem;
  }
  .container {
    max-width: 1100px;
    margin: 0 auto;
  }
  header {
    padding: 2rem 0 1rem;
    border-bottom: 2px solid var(--accent);
    margin-bottom: 1.5rem;
  }
  h1 {
    font-size: 2rem;
    margin: 0 0 0.25rem;
    color: #0b2e4f;
  }
  .subtitle {
    color: var(--muted);
    margin: 0;
    font-size: 1rem;
  }
  .search-panel {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .search-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: flex-end;
  }
  .search-input-group {
    flex: 2 1 300px;
  }
  .filter-group {
    flex: 1 1 150px;
  }
  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.25rem;
    font-size: 0.9rem;
    color: var(--muted);
  }
  input[type="text"], select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 1rem;
    background: #fff;
    color: var(--text);
  }
  input[type="text"]:focus, select:focus {
    outline: 2px solid var(--accent);
    outline-offset: 1px;
  }
  .search-note {
    margin-top: 0.75rem;
    font-size: 0.85rem;
    color: var(--muted);
  }
  .chart-section {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }
  .chart-container {
    position: relative;
    height: 220px;
    width: 100%;
  }
  .results-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    margin-bottom: 0.75rem;
  }
  .results-count {
    font-weight: 600;
    color: var(--muted);
  }
  .result-item {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  }
  .result-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }
  .committee-badge {
    background: var(--accent-light);
    color: var(--accent);
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.8rem;
    white-space: nowrap;
  }
  .short-title {
    font-weight: 600;
    color: #0b2e4f;
  }
  .symbol-link {
    color: var(--accent);
    text-decoration: none;
    font-size: 0.9rem;
  }
  .symbol-link:hover {
    text-decoration: underline;
  }
  .copy-btn {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    cursor: pointer;
    color: var(--text);
    transition: background 0.1s;
  }
  .copy-btn:hover {
    background: var(--accent-light);
    border-color: var(--accent);
  }
  .copy-btn.copied {
    background: #d4edda;
    border-color: #28a745;
    color: #155724;
  }
  .paragraph-text {
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 0;
    font-size: 0.95rem;
  }
  mark {
    background: #fff3b0;
    padding: 0 0.1em;
    border-radius: 2px;
  }
  .no-results {
    text-align: center;
    padding: 2rem;
    color: var(--muted);
    background: var(--card-bg);
    border: 1px dashed var(--border);
    border-radius: 8px;
  }
  .how-computed {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.5rem;
  }
  @media (max-width: 700px) {
    .search-row { flex-direction: column; }
    .filter-group { width: 100%; }
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>General Comments Search</h1>
    <p class="subtitle" id="data-description"></p>
  </header>

  <div class="search-panel">
    <div class="search-row">
      <div class="search-input-group">
        <label for="search-input">Search paragraphs</label>
        <input type="text" id="search-input" placeholder='e.g. "access to justice" AND children NOT detention' autocomplete="off">
      </div>
      <div class="filter-group">
        <label for="committee-filter">Committee</label>
        <select id="committee-filter"><option value="">All committees</option></select>
      </div>
      <div class="filter-group">
        <label for="year-filter">Year</label>
        <select id="year-filter"><option value="">All years</option></select>
      </div>
    </div>
    <div class="search-note">
      Supports <strong>AND</strong>, <strong>OR</strong>, <strong>NOT</strong>, and <strong>"exact phrases"</strong>. Terms are case-insensitive; single words match whole words. Filters apply before search.
    </div>
  </div>

  <div class="chart-section">
    <h2 style="margin-top:0; font-size:1.2rem;">Hits per committee</h2>
    <div class="chart-container">
      <canvas id="committee-chart"></canvas>
    </div>
    <div class="how-computed">Number of matching paragraphs per committee, after applying the current search and filters.</div>
  </div>

  <div class="results-header">
    <span class="results-count" id="results-count"></span>
  </div>
  <div id="results-container"></div>
</div>

<script>
(function() {
  const data = window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc;
  if (!data || !data.records || data.records.length === 0) {
    document.getElementById('data-description').textContent = 'No General Comments data available.';
    document.getElementById('results-container').innerHTML = '<div class="no-results">No data to display.</div>';
    return;
  }

  const records = data.records;
  const committees = [...new Set(records.map(r => r.committee).filter(Boolean))].sort();
  const years = [...new Set(records.map(r => r.year).filter(Number.isInteger))].sort((a,b) => a-b);
  const minYear = years.length ? years[0] : '?';
  const maxYear = years.length ? years[years.length-1] : '?';
  const description = `Search across ${records.length} paragraphs from ${data.source || 'UN treaty bodies'} (${minYear}–${maxYear}).`;
  document.getElementById('data-description').textContent = description;

  // Populate filters
  const committeeSelect = document.getElementById('committee-filter');
  committees.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    committeeSelect.appendChild(opt);
  });
  const yearSelect = document.getElementById('year-filter');
  years.forEach(y => {
    const opt = document.createElement('option');
    opt.value = y;
    opt.textContent = y;
    yearSelect.appendChild(opt);
  });

  // Search parser
  function tokenize(query) {
    const tokens = [];
    const regex = /"([^"]+)"|(\S+)/g;
    let m;
    while ((m = regex.exec(query)) !== null) {
      if (m[1] !== undefined) {
        tokens.push({ type: 'phrase', value: m[1] });
      } else {
        tokens.push({ type: 'word', value: m[2] });
      }
    }
    return tokens;
  }

  function parseQuery(query) {
    if (!query.trim()) return { groups: [[]] }; // empty query matches all
    const tokens = tokenize(query);
    const groups = [];
    let currentGroup = [];
    let pendingNot = false;
    for (let i = 0; i < tokens.length; i++) {
      const tok = tokens[i];
      const upper = tok.value.toUpperCase();
      if (tok.type === 'word' && upper === 'OR') {
        if (currentGroup.length > 0) {
          groups.push(currentGroup);
          currentGroup = [];
        }
        pendingNot = false;
        continue;
      }
      if (tok.type === 'word' && upper === 'AND') {
        // AND is default, ignore
        pendingNot = false;
        continue;
      }
      if (tok.type === 'word' && upper === 'NOT') {
        pendingNot = true;
        continue;
      }
      // It's a term (word or phrase)
      const term = {
        value: tok.value,
        isPhrase: tok.type === 'phrase',
        negated: pendingNot
      };
      currentGroup.push(term);
      pendingNot = false;
    }
    if (currentGroup.length > 0) groups.push(currentGroup);
    if (groups.length === 0) groups.push([]); // e.g. query was only operators
    return { groups };
  }

  function termMatches(textLower, term) {
    if (term.isPhrase) {
      return textLower.includes(term.value.toLowerCase());
    } else {
      const escaped = term.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`\\b${escaped}\\b`, 'i');
      return regex.test(textLower);
    }
  }

  function recordMatches(record, parsed) {
    const textLower = (record.text || '').toLowerCase();
    // OR across groups, AND within group
    return parsed.groups.some(group => {
      if (group.length === 0) return true; // empty group matches all (shouldn't happen)
      return group.every(term => {
        const found = termMatches(textLower, term);
        return term.negated ? !found : found;
      });
    });
  }

  // Highlighting: collect positive term matches
  function getHighlightRanges(text, parsed) {
    const positiveTerms = [];
    parsed.groups.forEach(group => {
      group.forEach(term => {
        if (!term.negated) positiveTerms.push(term);
      });
    });
    if (positiveTerms.length === 0) return [];

    const ranges = [];
    const lowerText = text.toLowerCase();
    positiveTerms.forEach(term => {
      if (term.isPhrase) {
        const phraseLower = term.value.toLowerCase();
        let idx = lowerText.indexOf(phraseLower);
        while (idx !== -1) {
          ranges.push({ start: idx, end: idx + phraseLower.length });
          idx = lowerText.indexOf(phraseLower, idx + 1);
        }
      } else {
        const escaped = term.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`\\b${escaped}\\b`, 'gi');
        let m;
        while ((m = regex.exec(text)) !== null) {
          ranges.push({ start: m.index, end: m.index + m[0].length });
        }
      }
    });

    // Merge overlapping ranges
    if (ranges.length === 0) return [];
    ranges.sort((a,b) => a.start - b.start || a.end - b.end);
    const merged = [ranges[0]];
    for (let i = 1; i < ranges.length; i++) {
      const last = merged[merged.length-1];
      if (ranges[i].start <= last.end) {
        last.end = Math.max(last.end, ranges[i].end);
      } else {
        merged.push(ranges[i]);
      }
    }
    return merged;
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function highlightText(text, ranges) {
    if (!ranges || ranges.length === 0) return escapeHtml(text);
    let html = '';
    let lastIndex = 0;
    ranges.forEach(range => {
      html += escapeHtml(text.slice(lastIndex, range.start));
      html += '<mark>' + escapeHtml(text.slice(range.start, range.end)) + '</mark>';
      lastIndex = range.end;
    });
    html += escapeHtml(text.slice(lastIndex));
    return html;
  }

  // Copy citation
  function copyCitation(symbol, paragraph) {
    const citation = `${symbol}, para. ${paragraph}`;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(citation).then(() => {
        // visual feedback handled by button
      }).catch(() => fallbackCopy(citation));
    } else {
      fallbackCopy(citation);
    }
  }
  function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
    } catch (e) {}
    document.body.removeChild(textarea);
  }

  // Chart
  let chartInstance = null;
  function updateChart(counts) {
    const canvas = document.getElementById('committee-chart');
    const ctx = canvas.getContext('2d');
    if (chartInstance) {
      chartInstance.destroy();
    }
    const labels = Object.keys(counts).filter(c => counts[c] > 0);
    const values = labels.map(c => counts[c]);
    if (labels.length === 0) {
      // Show empty state
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: { labels: ['No matches'], datasets: [{ data: [0], backgroundColor: '#ccc' }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
      });
      return;
    }
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Matching paragraphs',
          data: values,
          backgroundColor: '#1f6fb2',
          borderColor: '#1a5c94',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (ctx) => `${ctx.parsed.y} paragraph(s)` } }
        },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } }
        }
      }
    });
  }

  // Main render
  function render() {
    const query = document.getElementById('search-input').value;
    const committeeFilter = committeeSelect.value;
    const yearFilter = yearSelect.value;

    // Apply filters first
    let filtered = records.filter(r => {
      if (committeeFilter && r.committee !== committeeFilter) return false;
      if (yearFilter && String(r.year) !== yearFilter) return false;
      return true;
    });

    const parsed = parseQuery(query);
    const matched = filtered.filter(r => recordMatches(r, parsed));

    // Count per committee among matched
    const counts = {};
    matched.forEach(r => {
      const c = r.committee || 'Unknown';
      counts[c] = (counts[c] || 0) + 1;
    });
    updateChart(counts);

    // Results count
    const resultsCount = document.getElementById('results-count');
    resultsCount.textContent = `Showing ${matched.length} of ${filtered.length} paragraphs (after filters)`;

    // Render results
    const container = document.getElementById('results-container');
    if (matched.length === 0) {
      container.innerHTML = '<div class="no-results">No paragraphs match your search and filters.</div>';
      return;
    }

    let html = '';
    matched.forEach(r => {
      const ranges = getHighlightRanges(r.text || '', parsed);
      const highlighted = highlightText(r.text || '', ranges);
      const symbol = r.symbol || '';
      const docUrl = r.doc_url || '';
      const paragraph = r.paragraph;
      const committee = r.committee || 'Unknown';
      const shortTitle = r.short_title || r.title || '';
      const symbolDisplay = symbol ? (docUrl ? `<a class="symbol-link" href="${escapeHtml(docUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(symbol)}</a>` : escapeHtml(symbol)) : '';
      const citation = symbol ? `${symbol}, para. ${paragraph}` : `para. ${paragraph}`;
      html += `
        <div class="result-item">
          <div class="result-meta">
            <span class="committee-badge">${escapeHtml(committee)}</span>
            <span class="short-title">${escapeHtml(shortTitle)}</span>
            ${symbolDisplay ? `<span>${symbolDisplay}</span>` : ''}
            <button class="copy-btn" data-citation="${escapeHtml(citation)}">Copy citation</button>
          </div>
          <p class="paragraph-text">${highlighted}</p>
        </div>
      `;
    });
    container.innerHTML = html;

    // Attach copy handlers
    container.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const citation = this.getAttribute('data-citation');
        copyCitation(citation.split(', para. ')[0], parseInt(citation.split(', para. ')[1], 10));
        this.textContent = 'Copied!';
        this.classList.add('copied');
        setTimeout(() => {
          this.textContent = 'Copy citation';
          this.classList.remove('copied');
        }, 1500);
      });
    });
  }

  // Event listeners
  document.getElementById('search-input').addEventListener('input', render);
  committeeSelect.addEventListener('change', render);
  yearSelect.addEventListener('change', render);

  // Initial render
  render();
})();
</script>
</body>
</html>
```