I built a paragraph splitter for the PDF text: it cleans repeated page headers/footers, separates footnote blocks (`3/ See …`) from the numbered body paragraphs, and lists each paragraph with its first line. It checks the first six words against the reference list, flags mismatches, lets you click a row to read the full text, and download everything as CSV.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph splitter — <span id="t-sym"></span></title>
<style>
  :root { --accent:#1f6fb2; --bg:#f6f8fa; --line:#d9dee3; --ink:#1c2733; --muted:#5a6b7b; --ok:#1d7a3e; --bad:#b23a2f; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  .wrap { max-width:1080px; margin:0 auto; padding:32px 28px 64px; }
  h1 { font-size:26px; margin:0 0 4px; color:#123; }
  .sub { color:var(--muted); margin:0 0 6px; }
  .sub a { color:var(--accent); }
  .note { background:#eef4f9; border-left:4px solid var(--accent); padding:10px 14px; font-size:14px; color:#2b3d4d; margin:14px 0 22px; }
  .cards { display:flex; flex-wrap:wrap; gap:14px; margin:18px 0 6px; }
  .card { background:#fff; border:1px solid var(--line); border-radius:8px; padding:14px 18px; min-width:170px; }
  .card .label { font-size:13px; color:var(--muted); }
  .card .big { font-size:30px; font-weight:700; }
  .ok { color:var(--ok); } .bad { color:var(--bad); }
  .chartbox { background:#fff; border:1px solid var(--line); border-radius:8px; padding:16px; margin:22px 0; }
  table { width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:8px; overflow:hidden; font-size:15px; }
  th, td { text-align:left; padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { background:#eef2f5; font-size:13px; text-transform:uppercase; letter-spacing:.03em; color:#334; }
  tr.para { cursor:pointer; }
  tr.para:hover { background:#f0f6fb; }
  td.num { font-weight:700; white-space:nowrap; color:var(--accent); width:64px; }
  .badge { display:inline-block; font-size:12px; padding:2px 8px; border-radius:10px; white-space:nowrap; }
  .badge.ok { background:#e2f2e7; color:var(--ok); }
  .badge.bad { background:#f9e6e3; color:var(--bad); }
  tr.full td { background:#fbfcfd; }
  .fulltext { white-space:pre-wrap; font-size:14.5px; max-height:420px; overflow:auto; padding:8px 4px; }
  .ref { color:var(--muted); font-size:13px; }
  button { background:var(--accent); color:#fff; border:none; border-radius:6px; padding:9px 18px; font-size:15px; cursor:pointer; }
  button:hover { background:#175a94; }
  .toolbar { margin:20px 0 12px; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
  .legend { font-size:14px; color:var(--muted); }
  .muted { color:var(--muted); }
</style>
</head>
<body>
<div class="wrap">
  <h1 id="h1">Paragraph splitter</h1>
  <p class="sub" id="sub"></p>
  <div class="note"><strong>How this is computed:</strong> the raw PDF text of each page is cleaned by dropping lines that repeat on half or more of the pages (running headers/footers, distribution lines, page numbers). Numbered body paragraphs are lines starting with <code>N.</code> followed by text; footnote lines start with <code>N/</code> and everything until the next numbered paragraph is kept out of the paragraph text. Each paragraph's first six words are compared with the reference list — counting, splitting and matching are done entirely in your browser, nothing is estimated.</div>
  <div class="cards" id="cards"></div>
  <div class="chartbox">
    <div class="label muted" style="font-size:13px;margin-bottom:8px;">Found vs. reference: number of numbered paragraphs and footnote markers detected by this tool, compared with the official counts.</div>
    <canvas id="chart" height="140"></canvas>
  </div>
  <div class="toolbar">
    <button id="csv">Download CSV</button>
    <span class="legend" id="legend"></span>
  </div>
  <table>
    <thead><tr><th>Para.</th><th>First line</th><th>Check</th></tr></thead>
    <tbody id="tbody"></tbody>
  </table>
</div>
<script>
(function () {
  const P = window.WORKSHOP_DATA.pdf_text || {};
  const pages = Array.isArray(P.records) ? P.records : [];
  const ref = P.reference || {};
  const refWords = ref.first_words || {};
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  document.getElementById('h1').textContent = 'Paragraph splitter — ' + (P.symbol || 'document');
  document.getElementById('sub').innerHTML = (P.title ? esc(P.title) + '. ' : '') +
    (P.symbol ? '<a href="' + esc(P.doc_url || '#') + '" target="_blank" rel="noopener">' + esc(P.symbol) + '</a>. ' : '') +
    (pages.length ? pages.length + ' pages of raw PDF text. ' : '');

  if (!pages.length) {
    document.getElementById('tbody').innerHTML = '<tr><td colspan="3" class="muted">No page text is available in this session, so there is nothing to split.</td></tr>';
    return;
  }

  // ---- 1. Split each page into lines ----
  const pageLines = pages.map(p => (p.text || '').split(/\r?\n/));

  // ---- 2. Detect repeated header/footer lines across pages ----
  const freq = {};
  pageLines.forEach(lines => {
    const seen = new Set();
    lines.forEach(l => { const t = l.trim(); if (t && !seen.has(t)) { seen.add(t); freq[t] = (freq[t] || 0) + 1; } });
  });
  const threshold = Math.max(2, Math.ceil(pages.length / 2));
  const isChrome = t => freq[t] >= threshold && t.length < 110; // repeated short line = header/footer
  const isNoise = t =>
    /^[A-Z]{1,4}\/[A-Z0-9./()-]+$/.test(t) ||     // symbols like E/C.12/GC/27
    /^\d{1,3}$/.test(t) ||                        // bare page numbers
    /^GE\.\d/.test(t) ||                          // job number
    /^[_*=—-]{4,}$/.test(t) ||                    // rules / footnote separators
    /^\*?\s*\*?\s*$/.test(t);
  const cleanPages = pageLines.map(lines =>
    lines.filter(l => { const t = l.trim(); return t && !isChrome(t) && !isNoise(t); })
  );

  // ---- 3. Walk lines, build paragraphs, skip footnotes ----
  const paraStart = t => /^(\d{1,3})\.\s+\S/.exec(t) || /^(\d{1,3})\.$/.exec(t);
  const fnStart   = t => /^(\d{1,3})\/\s+\S/.exec(t);
  const paras = [];        // {num, lines}
  const footnotes = [];    // {num, lines}
  let cur = null, curFn = null, inFn = false;

  cleanPages.forEach(lines => {
    lines.forEach(raw => {
      const t = raw.trim();
      const mP = paraStart(t);
      const mF = fnStart(t);
      if (mP) {
        // footnotes end when the numbered body resumes
        if (curFn) { footnotes.push(curFn); curFn = null; inFn = false; }
        if (cur) paras.push(cur);
        const body = t.replace(/^\d{1,3}\.\s*/, '');
        cur = { num: parseInt(mP[1], 10), lines: body ? [body] : [] };
      } else if (mF) {
        if (cur) { paras.push(cur); cur = null; }
        if (curFn) footnotes.push(curFn);
        curFn = { num: parseInt(mF[1], 10), lines: [t.replace(/^\d{1,3}\/\s*/, '')] };
        inFn = true;
      } else if (inFn) {
        curFn.lines.push(t);
      } else if (cur) {
        cur.lines.push(t);
      }
      // lines before paragraph 1 (title page, headings) are dropped
    });
    if (curFn) { footnotes.push(curFn); curFn = null; inFn = false; } // footnote block ends at page break
  });
  if (cur) paras.push(cur);
  if (curFn) footnotes.push(curFn);

  paras.forEach(p => p.text = p.lines.join('\n').replace(/\s*\n\s*/g, ' ').trim());
  footnotes.forEach(f => f.text = f.lines.join(' ').replace(/\s+/g, ' ').trim());

  // ---- 4. Compare first six words with the reference ----
  const words = s => String(s || '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim().split(/\s+/).filter(Boolean);
  paras.forEach(p => {
    const got = words(p.text).slice(0, 6).join(' ');
    const expected = words(refWords[String(p.num)]).slice(0, 6).join(' ');
    p.match = !!expected && got === expected;
    p.expected = refWords[String(p.num)] || '';
  });

  // ---- 5. Summary cards ----
  const refParaCount = ref.paragraphs != null ? ref.paragraphs : null;
  const refFnCount = ref.footnotes != null ? ref.footnotes : null;
  const mismatched = paras.filter(p => !p.match).length;
  const cls = (a, b) => (b == null || a === b) ? 'ok' : 'bad';
  const cards = [
    { label: 'Paragraphs found', big: paras.length, extra: refParaCount != null ? 'reference: ' + refParaCount : 'no reference count', cls: cls(paras.length, refParaCount) },
    { label: 'Footnote markers found', big: footnotes.length, extra: refFnCount != null ? 'reference: ' + refFnCount : 'no reference count', cls: cls(footnotes.length, refFnCount) },
    { label: 'First-words mismatches', big: mismatched, extra: paras.length + ' paragraphs checked', cls: mismatched === 0 ? 'ok' : 'bad' }
  ];
  if (ref.adopted) cards.push({ label: 'Adopted (reference)', big: '', extra: esc(String(ref.adopted)), cls: '' });
  document.getElementById('cards').innerHTML = cards.map(c =>
    '<div class="card"><div class="label">' + esc(c.label) + '</div>' +
    (c.big !== '' ? '<div class="big ' + c.cls + '">' + c.big + '</div>' : '<div class="big" style="font-size:16px;line-height:1.4">' + c.extra + '</div>') +
    (c.big !== '' ? '<div class="label">' + esc(c.extra) + '</div>' : '') + '</div>').join('');
  document.getElementById('legend').innerHTML =
    'Click any row to read the full paragraph. <span class="badge ok">✓ matches reference</span> <span class="badge bad">⚠ first words differ from reference</span>';

  // ---- 6. Chart: found vs reference ----
  const labels = ['Numbered paragraphs', 'Footnote markers'];
  const found = [paras.length, footnotes.length];
  const reference = [refParaCount, refFnCount];
  if (window.Chart) {
    new Chart(document.getElementById('chart'), {
      type: 'bar',
      data: { labels: labels, datasets: [
        { label: 'Found by this tool', data: found, backgroundColor: '#1f6fb2' },
        { label: 'Reference count', data: reference, backgroundColor: '#9db8cc' }
      ]},
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
    });
    document.getElementById('chart').style.height = '140px';
  }

  // ---- 7. Table ----
  const tbody = document.getElementById('tbody');
  const openSet = new Set();
  function render() {
    tbody.innerHTML = paras.map(p => {
      const first = (p.lines[0] || '').slice(0, 160);
      const badge = p.match
        ? '<span class="badge ok">✓ matches reference</span>'
        : '<span class="badge bad">⚠ differs</span>';
      const refNote = p.match ? '' :
        '<div class="ref">Reference first words: “' + esc(p.expected) + '”</div>';
      const row = '<tr class="para" data-id="' + p.num + '"><td class="num">' + p.num + '</td>' +
        '<td>' + esc(first) + (first.length < (p.lines[0] || '').length ? '…' : '') + '</td>' +
        '<td>' + badge + refNote + '</td></tr>';
      const full = openSet.has(p.num)
        ? '<tr class="full"><td></td><td colspan="2"><div class="fulltext">' + esc(p.text) + '</div></td></tr>'
        : '';
      return row + full;
    }).join('') || '<tr><td colspan="3" class="muted">No numbered paragraphs were found in the page text.</td></tr>';
    tbody.querySelectorAll('tr.para').forEach(tr => {
      tr.addEventListener('click', () => {
        const n = parseInt(tr.dataset.id, 10);
        openSet.has(n) ? openSet.delete(n) : openSet.add(n);
        render();
      });
    });
  }
  render();

  // ---- 8. CSV download ----
  document.getElementById('csv').addEventListener('click', () => {
    const q = s => '"' + String(s == null ? '' : s).replace(/"/g, '""').replace(/\r?\n/g, ' ') + '"';
    const rows = [['paragraph', 'first_six_words_found', 'first_words_reference', 'matches_reference', 'full_text']];
    paras.forEach(p => rows.push([p.num, words(p.text).slice(0, 6).join(' '), p.expected, p.match ? 'yes' : 'no', p.text]));
    const csv = '\ufeff' + rows.map(r => r.map(q).join(',')).join('\r\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = (P.symbol || 'paragraphs').replace(/[^\w.-]+/g, '_') + '_paragraphs.csv';
    a.click();
    URL.revokeObjectURL(a.href);
  });
})();
</script>
</body>
</html>
```