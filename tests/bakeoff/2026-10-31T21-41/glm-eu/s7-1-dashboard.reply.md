I built a single-page dashboard that reads the country, record count and year span from `WORKSHOP_DATA.uhri`, with filters for mechanism, treaty body/mandate, year range, SDG and free-text keyword. It shows a top-10 theme bar chart (Chart.js) and a table of matching records — date, body, linked symbol, verbatim text preview — where clicking a row expands the full paragraph plus its themes, SDGs and affected persons. Every number carries a "how this is computed" note, and counts are computed in the browser, never estimated.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations</title>
<style>
  :root{
    --accent:#1f6fb2;
    --accent-soft:#e9f2f9;
    --ink:#1c2b39;
    --muted:#5b6b7a;
    --line:#dfe6ee;
    --bg:#f4f6f9;
    --card:#ffffff;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
  .wrap{max-width:1200px;margin:0 auto;padding:30px 26px 64px}
  .page-head{border-bottom:3px solid var(--accent);padding-bottom:16px;margin-bottom:22px}
  .page-head h1{margin:0 0 8px;font-size:27px;line-height:1.25;font-weight:700}
  .desc{margin:0;color:var(--muted);font-size:15px}
  .desc a{color:var(--accent)}
  .stats-row{display:flex;flex-wrap:wrap;gap:14px}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 22px;min-width:175px}
  .stat .num{font-size:27px;font-weight:700;color:var(--accent);line-height:1.2}
  .stat .lbl{font-size:13px;color:var(--muted);margin-top:2px}
  .stats-note{font-size:13.5px;color:var(--muted);margin:12px 2px 0}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:22px 24px;margin:18px 0}
  .card h2{margin:0 0 8px;font-size:19px;font-weight:600}
  .h2sub{font-size:14px;font-weight:400;color:var(--muted)}
  .note{font-size:13.5px;color:var(--muted);margin:6px 0 14px}
  .filters-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px 16px;align-items:end}
  .field label{display:block;font-size:12px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}
  .field .hint{font-weight:400;text-transform:none;letter-spacing:0}
  select,input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit;font-size:15px;color:var(--ink)}
  select:focus,input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  .years{display:flex;gap:8px;align-items:center}
  .dash{color:var(--muted)}
  button{font:inherit;font-size:15px;padding:8px 16px;border-radius:6px;border:1px solid var(--accent);background:var(--accent-soft);color:var(--accent);cursor:pointer}
  button:hover{background:var(--accent);color:#fff}
  .matchline{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:8px;padding:12px 18px;margin:18px 0;font-size:16px}
  .matchline b{color:var(--accent)}
  .chart-wrap{position:relative;height:460px;margin-top:4px}
  .empty{font-size:15px;color:var(--muted);background:var(--accent-soft);border:1px dashed var(--accent);border-radius:8px;padding:14px 16px}
  .fallback ol{margin:0;padding-left:22px;font-size:15px}
  .fallback li{margin:4px 0}
  .shownline{font-size:14px;color:var(--muted);margin:0 0 4px}
  .table-scroll{overflow-x:auto}
  table{width:100%;border-collapse:collapse;font-size:15px}
  thead th{text-align:left;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);border-bottom:2px solid var(--line);padding:9px 10px;white-space:nowrap}
  th.c-date{width:112px}
  th.c-body{width:95px}
  tbody td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}
  tr.rec{cursor:pointer}
  tr.rec:hover{background:var(--accent-soft)}
  tr.rec:focus{outline:2px solid var(--accent);outline-offset:-2px}
  td.c-date{white-space:nowrap;color:var(--muted)}
  td.c-body{white-space:nowrap;font-weight:600}
  td.c-sym{white-space:nowrap}
  td.c-sym a{color:var(--accent);font-weight:600;text-decoration:none}
  td.c-sym a:hover{text-decoration:underline}
  tr.detail td{background:#f6f9fc;border-bottom:1px solid var(--line);border-left:4px solid var(--accent);padding:16px 18px}
  .d-head{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:8px}
  .fulltext{white-space:pre-wrap;margin:0 0 12px;max-width:920px;font-size:15px}
  .meta{display:flex;flex-direction:column;gap:6px;margin-bottom:12px;font-size:13.5px}
  .meta .m b{color:var(--ink);font-weight:600;margin-right:4px}
  .chip{display:inline-block;background:var(--accent-soft);color:#17486e;border-radius:12px;padding:2px 10px;margin:2px 6px 2px 0;font-size:12.5px}
  .doclink{color:var(--accent);font-weight:600;text-decoration:none}
  .doclink:hover{text-decoration:underline}
  .more{margin-top:14px}
  .foot{font-size:13px;color:var(--muted);margin-top:26px;border-top:1px solid var(--line);padding-top:12px}
</style>
</head>
<body>
<div class="wrap">

  <header class="page-head">
    <h1 id="pageTitle">UN human rights recommendations</h1>
    <p class="desc" id="pageDesc"></p>
  </header>

  <section class="stats-row" id="stats" aria-label="Dataset overview"></section>
  <p class="stats-note">How this is computed: every figure on this page is counted directly in your browser from the loaded records — nothing is estimated. One record = one paragraph from a UN document (a recommendation or an observation).</p>

  <section class="card">
    <h2>Filters</h2>
    <div class="filters-grid">
      <div class="field">
        <label for="fMech">Mechanism</label>
        <select id="fMech"><option value="">All mechanisms</option></select>
      </div>
      <div class="field">
        <label for="fBody">Treaty body / mandate</label>
        <select id="fBody"><option value="">All bodies &amp; mandates</option></select>
      </div>
      <div class="field">
        <label for="fFrom">Year range <span class="hint" id="yearHint"></span></label>
        <div class="years">
          <input type="number" id="fFrom" inputmode="numeric" aria-label="From year">
          <span class="dash">–</span>
          <input type="number" id="fTo" inputmode="numeric" aria-label="To year">
        </div>
      </div>
      <div class="field">
        <label for="fSdg">SDG</label>
        <select id="fSdg"><option value="">All SDGs</option></select>
      </div>
      <div class="field">
        <label for="fKeyword">Keyword search</label>
        <input type="search" id="fKeyword" placeholder="Search text, symbol, themes…">
      </div>
      <div class="field">
        <button type="button" id="resetBtn">Reset filters</button>
      </div>
    </div>
    <p class="note">Keyword search is case-insensitive and matches the exact string anywhere in the paragraph text, the document symbol or the theme labels. Year range boundaries are inclusive.</p>
  </section>

  <p class="matchline" id="matchLine"></p>

  <section class="card">
    <h2>Most frequent themes <span class="h2sub">(top 10, current filters)</span></h2>
    <p class="note" id="chartNote"></p>
    <div class="chart-wrap" id="chartWrap"><canvas id="themeChart" role="img" aria-label="Bar chart of the most frequent themes"></canvas></div>
    <p class="empty" id="chartEmpty" hidden>No theme information is attached to the matching records, so there is nothing to chart.</p>
    <div class="fallback" id="chartFallback" hidden>
      <p class="note">The chart library is unavailable in this session, so the same counts are listed as text:</p>
      <ol id="chartFallbackList"></ol>
    </div>
  </section>

  <section class="card">
    <h2>Matching records</h2>
    <p class="shownline" id="shownLine"></p>
    <p class="note">How this is computed: the table lists the records matching the current filters, sorted by document date (newest first). The last column shows the verbatim beginning of the paragraph; click a row to read the full text. The symbol links to the UN document in a new tab.</p>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th class="c-date">Date</th>
            <th class="c-body">Body</th>
            <th class="c-sym">Symbol</th>
            <th>Text (click row for full paragraph)</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <p class="empty" id="tableEmpty" hidden></p>
    <button type="button" id="moreBtn" class="more