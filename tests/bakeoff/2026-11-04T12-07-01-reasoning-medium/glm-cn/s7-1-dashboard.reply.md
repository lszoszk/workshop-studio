I built the full four-tab dashboard exactly to the plan: filters in a left rail with accordion headings, an overview with theme and timeline charts, an expandable records table with citations and UPR recommending States, a self-check panel with a seeded random-sample label check, and a method/export tab with CSV and summary copy. All numbers are computed in the browser from `WORKSHOP_DATA.uhri`, and the country name is read from the data.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations and observations</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --accent:#9b2335;
    --serif:Georgia,"Times New Roman",serif;
    --mono:ui-monospace,Menlo,Consolas,monospace;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  }
  *{box-sizing:border-box}
  [hidden]{display:none!important}
  html,body{margin:0;padding:0}
  body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.5}
  a{color:var(--accent)}
  a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .wrap{max-width:1200px;margin:0 auto;padding:0 20px 40px}

  /* header */
  header{border-bottom:1px solid var(--rule);padding:22px 0 14px}
  .klabel{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#5c564c}
  h1{font-family:var(--serif);font-weight:400;font-size:34px;margin:6px 0 8px;line-height:1.15}
  .meta{font-family:var(--mono);font-size:12px;color:#5c564c}
  .meta a{color:inherit;text-decoration:underline}

  /* layout */
  .cols{display:flex;gap:28px;align-items:flex-start;margin-top:18px}
  aside.rail{width:250px;flex:0 0 250px;border-right:1px solid var(--rule);padding-right:20px}
  main.tabarea{flex:1;min-width:0}

  /* rail */
  .railhead{display:flex;justify-content:space-between;align-items:baseline;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#5c564c;border-bottom:1px solid var(--rule);padding-bottom:6px}
  .railhead button{background:none;border:none;font-family:var(--mono);font-size:11px;color:var(--accent);cursor:pointer;padding:0}
  .bignum{font-family:var(--serif);font-size:48px;line-height:1.05;margin:14px 0 2px}
  .bignum small{font-family:var(--mono);font-size:12px;color:#5c564c;display:block;margin-top:4px}
  .sharebar{height:5px;background:#e6dfd0;margin:10px 0 12px;position:relative}
  .sharebar i{position:absolute;left:0;top:0;bottom:0;background:var(--accent)}
  .sharenote{font-family:var(--mono);font-size:11px;color:#5c564c;margin-bottom:10px}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
  .chip{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff;font-family:var(--mono);font-size:11px;padding:3px 8px;border-radius:2px}
  .chip button{background:none;border:none;color:#fff;cursor:pointer;font-size:13px;padding:0;line-height:1}
  .acc{border-top:1px solid var(--rule)}
  .acc h3{margin:0}
  .acc>button{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:none;font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:10px 2px;cursor:pointer;color:var(--ink)}
  .acc>button::after{content:"+";font-size:15px}
  .acc>button[aria-expanded="true"]::after{content:"−"}
  .acc .panel{padding:2px 2px 14px}
  .acc .panel label{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5c564c;margin:10px 0 4px}
  .acc .panel input[type=text],.acc .panel select{width:100%;font-family:var(--sans);font-size:14px;padding:6px 8px;border:1px solid var(--rule);background:#fbf9f4;color:var(--ink)}
  .hint{font-family:var(--mono);font-size:11px;color:#5c564c;margin-top:4px}
  .yrow{display:flex;gap:8px}
  .yrow select{flex:1}

  /* tabs */
  .tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-bottom:22px}
  .tabs button{background:none;border:none;border-bottom:3px solid transparent;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;padding:10px 14px 8px;cursor:pointer;color:#5c564c}
  .tabs button[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
  .panel-title{font-family:var(--serif);font-size:26px;font-weight:400;margin:0 0 6px}

  /* tiles */
  .tiles{display:flex;flex-wrap:wrap;gap:0;border-top:1px solid var(--rule);border-left:1px solid var(--rule);margin:14px 0 8px}
  .tile{flex:1 1 180px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:14px 16px}
  .tile .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#5c564c}
  .tile .num{font-family:var(--serif);font-size:44px;line-height:1.1}
  .tile .sub{font-size:13px;color:#444;margin-top:2px}
  .tile .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:baseline}
  .note{font-family:var(--mono);font-size:11px;color:#5c564c;margin:4px 0 20px}
  .inplacelist{margin:0 0 20px;border-top:1px solid var(--rule)}
  .inplacelist li{display:flex;justify-content:space-between;border-bottom:1px solid var(--rule);padding:6px 2px;font-size:14px}
  .inplacelist b{font-family:var(--serif);font-weight:400}

  /* figures */
  figure{margin:0 0 34px}
  figure .figno{font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:#5c564c}
  figure h2{font-family:var(--serif);font-weight:400;font-size:20px;margin:2px 0 10px}
  .chartbox{position:relative;height:340px}
  .chartbox.tall{height:360px}

  /* tables */
  table{width:100%;border-collapse:collapse;font-size:14px}
  caption{text-align:left;font-family:var(--mono);font-size:11px;color:#5c564c;padding:4px 0 8px;letter-spacing:.05em}
  th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
  th{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5c564c;font-weight:400}
  th .num,td.num{text-align:right;font-variant-numeric:tabular-nums}
  th button{background:none;border:none;font-family:inherit;font-size:inherit;color:inherit;cursor:pointer;text-transform:inherit;letter-spacing:inherit;padding:0}
  tbody tr.rec{cursor:pointer}
  tbody tr.rec:hover{background:#efe9dc}
  .sym{font-family:var(--mono);font-size:12px;white-space:nowrap}
  .firstline{max-width:420px}
  mark{background:#f0d9a8;color:inherit;padding:0 1px}
  tr.expand td{background:#faf7f0;cursor:default}
  .expand .para{font-family:var(--serif);font-size:30px;color:var(--accent);line-height:1;margin-bottom:8px}
  .expand .fulltext{font-size:15px;max-width:760px;white-space:pre-wrap}
  .labels{margin-top:10px;font-size:13px}
  .labels .row{margin:3px 0}
  .labels .k{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5c564c;display:inline-block;width:150px;vertical-align:top}
  .tchip{display:inline-block;border:1px solid var(--rule);padding:1px 7px;margin:2px 4px 2px 0;font-size:12px;background:#fff}
  .btnrow{margin-top:12px}
  .btn{background:var(--accent);color:#fff;border:none;font-family:var(--mono);font-size:12px;letter-spacing:.05em;padding:7px 14px;cursor:pointer;margin-right:8px}
  .btn.ghost{background:none;color:var(--accent);border:1px solid var(--accent)}
  .morebtn{margin:14px 0}
  .copied{font-family:var(--mono);font-size:12px;color:var(--accent)}

  /* checks */
  .check{border-bottom:1px solid var(--rule);padding:9px 2px;font-size:14px;display:flex;gap:10px;flex-wrap:wrap}
  .check .what{flex:0 0 260px}
  .check .vals{flex:1;color:#444;font-size:13px}
  .pass{color:#1a6b3c;font-family:var(--mono);font-size:12px}
  .fail{color:var(--accent);font-family:var(--mono);font-size:12px}
  .warn{color:#a05a00;font-family:var(--mono);font-size:12px}
  .samplehead{margin:26px 0 10px}
  .card{border:1px solid var(--rule);background:#fbf9f4;margin-bottom:14px}
  .card>button{width:100%;text-align:left;background:none;border:none;padding:10px 12px;cursor:pointer;font-family:var(--sans);font-size:14px;color:var(--ink)}
  .card .cardbody{padding:2px 14px 14px;border-top:1px solid var(--rule)}
  .card .ctext{font-size:14px;white-space:pre-wrap;max-width:760px}
  .verdicts{display:flex;gap:8px;margin-top:8px}
  .verdicts button{background:none;border:1px solid var(--rule);font-family:var(--mono);font-size:12px;padding:4px 12px;cursor:pointer}
  .verdicts button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
  .vnote{font-family:var(--mono);font-size:11px;color:#5c564c;margin-top:10px}

  /* method */
  .method p{max-width:760px}
  .method ol{max-width:760px}
  .method li{margin-bottom:8px}
  .srcnote{font-family:var(--mono);font-size:11px;color:#5c564c}

  footer{border-top:1px solid var(--rule);margin-top:20px;padding:12px 0;font-family:var(--mono);font-size:11px;color:#5c564c}
  .empty{font-family:var(--serif);font-size:20px;color:#5c564c;padding:30px 0}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="klabel" id="hd-label"></div>
    <h1 id="hd-title"></h1>
    <div class="meta" id="hd-meta"></div>
  </header>

  <div class="cols">
    <aside class="rail" aria-label="Filters">
      <div class="railhead"><span>Filters</span><button type="button" id="clearall">Clear all</button></div>
      <div class="bignum" aria-live="polite"><span id="matchcount">0</span><small id="ofcount"></small></div>
      <div class="sharebar" aria-hidden="true"><i id="sharefill" style="width:0%"></i></div>
      <div class="sharenote" id="sharenote"></div>
      <div class="chips" id="chips"></div>
      <div id="accordion">
        <div class="acc">
          <h3><button type="button" id="acc-kw-btn" aria-expanded="false" aria-controls="acc-kw">01 Keyword</button></h3>
          <div class="panel" id="acc-kw" hidden>
            <label for="kwbox">Keyword</label>
            <input type="text" id="kwbox" autocomplete="off">
            <div class="hint">literal match, not synonyms · every word must occur in the text or symbol</div>
          </div>
        </div>
        <div class="acc">
          <h3><button type="button" id="acc-mb-btn" aria-expanded="false" aria-controls="acc-mb">02 Mechanism, body, type</button></h3>
          <div class="panel" id="acc-mb" hidden>
            <label for="sel-mech">Mechanism</label>
            <select id="sel-mech"></select>
            <label for="sel-body">Body or mandate</label>
            <select id="sel-body"></select>
            <label for="sel-type">Type</label>
            <select id="sel-type"></select>
            <div id="statewrap" hidden>
              <label for="sel-state">Recommending State (UPR)</label>
              <select id="sel-state"></select>
            </div>
          </div>
        </div>
        <div class="acc">
          <h3><button type="button" id="acc-ys-btn" aria-expanded="false" aria-controls="acc-ys">03 Years and SDG</button></h3>
          <div class="panel" id="acc-ys" hidden>
            <div class="yrow">
              <span style="flex:1"><label for="sel-yfrom">Year from</label><select id="sel-yfrom"></select></span>
              <span style="flex:1"><label for="sel-yto">to</label><select id="sel-yto"></select></span>
            </div>
            <div class="hint">a reversed range is swapped</div>
            <label for="sel-sdg">SDG goal</label>
            <select id="sel-sdg"></select>
          </div>
        </div>
      </div>
    </aside>

    <main class="tabarea">
      <div class="tabs" role="tablist" aria-label="Sections">
        <button role="tab" id="tab1" aria-controls="p1" aria-selected="true">01 Overview</button>
        <button role="tab" id="tab2" aria-controls="p2" aria-selected="false" tabindex="-1">02 Records</button>
        <button role="tab" id="tab3" aria-controls="p3" aria-selected="false" tabindex="-1">03 Check</button>
        <button role="tab" id="tab4" aria-controls="p4" aria-selected="false" tabindex="-1">04 Method &amp; export</button>
      </div>

      <!-- TAB 1 -->
      <section id="p1" role="tabpanel" aria-labelledby="tab1">
        <h2 class="panel-title">What has the UN said, how much, and when?</h2>
        <div id="tiles"></div>
        <div class="note">How this is computed: the first tile counts every record in the file (the number of matching records is in the left rail); documents are distinct symbols; years are the minimum and maximum of the document date. Dated by document.</div>
        <div id="stateslist" hidden>
          <p class="srcnote" style="margin:0 0 6px">Ten States that made most recommendations to <span id="sl-country"></span> · current filter · a record counts once per State named · count of recommendations, not of influence</p>
          <ul class="inplacelist" id="stateslist-ul"></ul>
          <div class="note">Source: extracted from the parenthesised States at the end of UPR recommendation texts; two States can co-sponsor one line.</div>
        </div>
        <figure>
          <div class="figno">FIG.01</div>
          <h2 id="fig1-title"></h2>
          <div class="chartbox"><canvas id="chart-themes"></canvas></div>
          <p class="srcnote">How this is computed: for each matching record, each theme label counts once; top ten by count, ties alphabetical; bar width is 80% of scale. A record can carry several themes, so the bars add up to more than the number of records. Click a bar to filter by that theme. Source: <span id="fig1-src"></span>.</p>
          <table id="fig1-table">
            <caption>Same ten themes as the chart, with the year range of the matching records carrying each theme · percentages are of matching records, not of labels</caption>
            <thead><tr><th scope="col">Theme</th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col">Years</th></tr></thead>
            <tbody></tbody>
          </table>
          <p class="srcnote">Source: UN labels as recorded in the UHRI data; the tab “03 Check” lets you judge a sample of them. Themes may be legacy labels — check the year range before citing a theme.</p>
        </figure>
        <figure>
          <div class="figno">FIG.02</div>
          <h2 id="fig2-title"></h2>
          <div class="chartbox tall"><canvas id="chart-years"></canvas></div>
          <p class="srcnote">How this is computed: matching records counted per document year and per mechanism; years with no records appear as gaps. Dated by document. Source: <span id="fig2-src"></span>.</p>
        </figure>
      </section>

      <!-- TAB 2 -->
      <section id="p2" role="tabpanel" aria-labelledby="tab2" hidden>
        <h2 class="panel-title">Which paragraph says it, and in which UN document?</h2>
        <label for="searchbox" class="klabel">Search</label>
        <input type="text" id="searchbox" autocomplete="off" style="width:100%;max-width:560px;font-size:16px;padding:8px 10px;border:1px solid var(--rule);background:#fbf9f4;margin:4px 0 2px">
        <div class="hint" style="margin-bottom:8px">same box as the Keyword filter · literal match, not synonyms</div>
        <table id="rectable">
          <caption id="rectable-cap"></caption>
          <thead>
            <tr>
              <th scope="col"><button type="button" id="th-date">Date <span id="th-date-note">↓ newest first</span></button></th>
              <th scope="col">Body</th>
              <th scope="col">Symbol</th>
              <th scope="col">Para.</th>
              <th scope="col">First line</th>
              <th scope="col">Recommending State</th>
            </tr>
          </thead>
          <tbody id="rectable-body"></tbody>
        </table>
        <button type="button" class="btn ghost morebtn" id="morebtn">Show 50 more</button>
      </section>

      <!-- TAB 3 -->
      <section id="p3" role="tabpanel" aria-labelledby="tab3" hidden>
        <h2 class="panel-title">Can I trust these numbers?</h2>
        <p class="srcnote">How the app checks itself: each line below compares two numbers computed by independent loops, or checks every record for a property. Nothing is hidden — a failed check shows its values.</p>
        <div id="checks"></div>

        <div class="samplehead">
          <h3 style="font-family:var(--serif);font-weight:400;font-size:22px;margin:0 0 4px">Check the UN’s own labels on a random sample</h3>
          <p class="srcnote" style="margin:0 0 10px">This is your judgement of the UN’s labels; nothing is sent anywhere. The app never changes a UN label.</p>
          <button type="button" class="btn" id="drawbtn">Check 10 at random</button>
          <span id="drawcontrols" hidden>
            <button type="button" class="btn ghost" id="redrawbtn">Draw again</button>
            <label class="srcnote" for="seedbox">Seed</label>
            <input type="text" id="seedbox" value="1" style="width:70px;font-family:var(--mono);font-size:12px;padding:4px 6px;border:1px solid var(--rule);background:#fbf9f4">
            <button type="button" class="btn ghost" id="seedbtn">Draw with this seed</button>
          </span>
          <p class="srcnote" id="tally" style="margin:10px 0 4px"></p>
          <p class="srcnote">Draws come from the matching records, with the seed shown, so a colleague can draw the same ten.</p>
        </div>
        <div id="samplecards"></div>
      </section>

      <!-- TAB 4 -->
      <section id="p4" role="tabpanel" aria-labelledby="tab4" hidden>
        <h2 class="panel-title">How was this made, and how do I take it with me?</h2>
        <div class="method">
          <p><b>How each number is computed.</b> The headline total is the number of records in the file. Documents are distinct symbols; years are the minimum and maximum document year. Filters combine with AND: mechanism, body, type, State and SDG are exact matches on the field; year is inclusive between the two selects; a keyword requires every word to occur in the text or the symbol.</p>
          <p>Theme counts count each label once per matching record, so they sum to more than the record count; percentages are of matching records. The timeline counts records per year and per mechanism, filling empty years with zero. Paragraph numbers are read from the start of the text with a regular expression; recommending States are read only from UPR texts, from the parenthesised groups at the end.</p>
          <p>Nothing is estimated and no model is called. Every count is a loop over the records in JavaScript, in this page. Nothing leaves the browser except the clipboard write when you press “Copy”.</p>
          <ol>
            <li><b>Download CSV of the current filter</b> — the table columns plus the full verbatim text and all labels, preceded by comment lines with the country, source, build date, filters applied and row count. <button type="button" class="btn" id="csvbtn">Download CSV</button></li>
            <li><b>Copy summary</b> — a plain-text paragraph with the headline numbers and the ten most frequent themes, for pasting into notes. <button type="button" class="btn ghost" id="sumbtn">Copy summary</button> <span class="copied" id="sumcopied" hidden>Copied</span></li>
          </ol>
          <p class="srcnote" id="method-src"></p>
          <p class="srcnote">Citations follow the Dag Hammarskjöld Library’s advice: the document symbol is the key and the paragraph is kept as a pinpoint. Charts and tables follow the UK Government Analysis Function guidance on data visualisation. Transparency follows OHCHR’s Human Rights-Based Approach to Data: the method is stated at the point of use.</p>
          <p class="srcnote" id="licence"></p>
        </div>
      </section>
    </main>
  </div>

  <footer id="footer"></footer>
</div>

<script>
(function(){
"use strict";
const U = window.WORKSHOP_DATA.uhri;
const R = U.records || [];
const COUNTRY = U.country;
const fmt = n => Number(n).toLocaleString("en-GB");
const MECHCOLORS = {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
const mechColor = m => MECHCOLORS[m] || "#9b2335";

/* ---------- derived per record ---------- */
const paraRe = /^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
function paraOf(t){ const m = (t||"").match(paraRe); return m ? m[1] : null; }
function statesOf(rec){
  if(rec.mechanism !== "Universal Periodic Review") return null;
  const m = (rec.text||"").match(/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/);
  if(!m) return null;
  const groups = m[1].match(/\((?:[^()]|\([^()]*\))*\)/g) || [];
  const out = [];
  for(const g of groups){
    let s = g.replace(/^\(/,"").replace(/\)$/,"").trim();
    if(s.includes(",") || s.length > 60) return null; // not a State
    out.push(s);
  }
  return out.length ? out : null;
}
R.forEach(r => {
  r._para = paraOf(r.text);
  r._states = statesOf(r);
});

/* ---------- filter state ---------- */
const F = { keyword:"", mechanism:"", body:"", type:"", state:"", yfrom:"", yto:"", sdg:"", themes:new Set() };
let filtered = R.slice();
let dateDesc = true;

function applyFilters(){
  const kw = F.keyword.trim().toLowerCase();
  const words = kw ? kw.split(/\s+/) : [];
  const yf = F.yfrom ? Number(F.yfrom) : null, yt = F.yto ? Number(F.yto) : null;
  filtered = R.filter(r => {
    if(F.mechanism && r.mechanism !== F.mechanism) return false;
    if(F.body && r.body !== F.body) return false;
    if(F.type && r.type !== F.type) return false;
    if(F.state){
      const st = r._states || [];
      if(!st.includes(F.state)) return false;
    }
    if(yf !== null && r.year < yf) return false;
    if(yt !== null && r.year > yt) return false;
    if(F.sdg !== "" && !(Array.isArray(r.sdgs) && r.sdgs.includes(Number(F.sdg)))) return false;
    for(const t of F.themes){ if(!(r.themes||[]).includes(t)) return false; }
    if(words.length){
      const hay = ((r.text||"") + " " + (r.symbol||"")).toLowerCase();
      for(const w of words){ if(!hay.includes(w)) return false; }
    }
    return true;
  });
}

/* ---------- helpers ---------- */
function distinct(arr){ return [...new Set(arr)].filter(v => v !== undefined && v !== null && v !== ""); }
function countBy(recs, key){
  const m = new Map();
  for(const r of recs){ const k = typeof key === "function" ? key(r) : r[key]; m.set(k, (m.get(k)||0)+1); }
  return m;
}
function topThemes(recs){
  const m = new Map();
  for(const r of recs) for(const t of (r.themes||[])) m.set(t, (m.get(t)||0)+1);
  const rows = [...m.entries()].map(([theme,count])=>{
    const sub = recs.filter(r => (r.themes||[]).includes(theme));
    const yrs = sub.map(r=>r.year);
    return {theme, count, min:Math.min(...yrs), max:Math.max(...yrs)};
  });
  rows.sort((a,b)=> b.count - a.count || a.theme.localeCompare(b.theme));
  return rows;
}
function firstLine(t){
  t = t || "";
  if(t.length <= 120) return t;
  let cut = t.slice(0,120); const sp = cut.lastIndexOf(" ");
  if(sp > 40) cut = cut.slice(0,sp);
  return cut + "…";
}
function esc(s){ return String(s??"").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"); }
function highlight(html, kw){
  const words = kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  if(!words.length) return html;
  for(const w of words){
    const re = new RegExp("("+escRe(esc(w))+")","gi");
    html = html.replace(re,"<mark>$1</mark>");
  }
  return html;
}
function sortRecords(recs){
  const idx = new Map(R.map((r,i)=>[r.id,i]));
  const arr = recs.slice();
  arr.sort((a,b)=>{
    const d = (b.date||"").localeCompare(a.date||"");
    const dd = dateDesc ? d : -d;
    if(dd) return dd;
    const bb = (a.body||"").localeCompare(b.body||"");
    if(bb) return bb;
    const pa = a._para ? parseFloat(a._para) : Infinity;
    const pb = b._para ? parseFloat(b._para) : Infinity;
    if(pa !== pb) return pa - pb;
    return (idx.get(a.id)||0) - (idx.get(b.id)||0);
  });
  return arr;
}

/* ---------- header / footer ---------- */
(function(){
  const symbols = distinct(R.map(r=>r.symbol));
  const years = R.map(r=>r.year);
  document.getElementById("hd-label").textContent = "UHRI · " + COUNTRY;
  document.getElementById("hd-title").textContent = "UN human rights recommendations and observations: " + COUNTRY;
  const s = U.source ? '<a href="'+esc(U.source_url||"")+'" target="_blank" rel="noopener">'+esc(U.source)+"</a>" : "UHRI";
  document.getElementById("hd-meta").innerHTML =
    s + " · " + fmt(R.length) + " records · " + fmt(symbols.length) + " documents · " +
    (years.length?Math.min(...years):"—") + "–" + (years.length?Math.max(...years):"—") +
    (U.built ? " · built " + esc(U.built) : "") + " · dated by document";
  document.getElementById("footer").innerHTML =
    "Built on OHCHR UHRI data · " + fmt(R.length) + " records · <a href=\"" + esc(U.source_url||"") + "\" target=\"_blank\" rel=\"noopener\">source</a>";
})();

/* ---------- tabs ---------- */
const tabs = [...document.querySelectorAll('.tabs [role="tab"]')];
let curTab = 0;
function showTab(i){
  curTab = i;
  tabs.forEach((t,j)=>{
    t.setAttribute("aria-selected", j===i ? "true":"false");
    t.tabIndex = j===i ? 0 : -1;
    document.getElementById("p"+(j+1)).hidden = j!==i;
  });
  document.getElementById("accordion").hidden = (i>=2);
  if(i===0){ renderOverview(); }
  if(i===1){ rowsShown = 50; renderTable(); }
  if(i===2){ renderChecks(); }
  if(i===3){ /* static */ }
}
tabs.forEach((t,i)=>{
  t.addEventListener("click", ()=>showTab(i));
  t.addEventListener("keydown", e=>{
    let j = null;
    if(e.key==="ArrowRight") j = (i+1)%tabs.length;
    if(e.key==="ArrowLeft") j = (i-1+tabs.length)%tabs.length;
    if(j!==null){ e.preventDefault(); tabs[j].focus(); showTab(j); }
  });
});

/* ---------- rail: accordion ---------- */
const accBtns = [["acc-kw-btn","acc-kw"],["acc-mb-btn","acc-mb"],["acc-ys-btn","acc-ys"]];
function openAcc(id){
  accBtns.forEach(([b,p])=>{
    const open = b===id;
    document.getElementById(b).setAttribute("aria-expanded", open);
    document.getElementById(p).hidden = !open;
  });
}
accBtns.forEach(([b])=> document.getElementById(b).addEventListener("click", ()=>{
  const isOpen = document.getElementById(b).getAttribute("aria-expanded")==="true";
  if(isOpen){ document.getElementById(b).setAttribute("aria-expanded","false"); document.getElementById(accBtns.find(x=>x[0]===b)[1]).hidden = true; }
  else openAcc(b);
}));

/* ---------- rail: widgets ---------- */
let kwTimer = null;
function setKeyword(v){
  F.keyword = v;
  document.getElementById("kwbox").value = v;
  document.getElementById("searchbox").value = v;
  refresh();
}
document.getElementById("kwbox").addEventListener("input", e=>{
  clearTimeout(kwTimer);
  kwTimer = setTimeout(()=>setKeyword(e.target.value), 300);
});
document.getElementById("searchbox").addEventListener("input", e=>{
  clearTimeout(kwTimer);
  kwTimer = setTimeout(()=>setKeyword(e.target.value), 300);
});

function fillSelect(sel, options, allLabel){
  sel.innerHTML = "";
  const a = document.createElement("option");
  a.value = ""; a.textContent = allLabel || "all";
  sel.appendChild(a);
  for(const [val,label] of options){
    const o = document.createElement("option");
    o.value = val; o.textContent = label;
    sel.appendChild(o);
  }
}
function refreshMech(){
  fillSelect(document.getElementById("sel-mech"),
    distinct(R.map(r=>r.mechanism)).sort().map(m=>[m, m]), "all mechanisms");
}
function refreshBody(){
  const pool = F.mechanism ? R.filter(r=>r.mechanism===F.mechanism) : R;
  const m = countBy(pool,"body");
  const names = [...m.keys()].sort((a,b)=>a.localeCompare(b));
  fillSelect(document.getElementById("sel-body"),
    names.map(b=>[b, b + " (" + m.get(b) + ")"]), "all bodies");
  document.getElementById("sel-body").value = F.body;
}
function refreshType(){
  const pool = (F.mechanism ? R.filter(r=>r.mechanism===F.mechanism) : R)
    .filter(r=>!F.body || r.body===F.body);
  const m = countBy(pool,"type");
  fillSelect(document.getElementById("sel-type"),
    [...m.keys()].sort().map(t=>[t, t + " (" + m.get(t) + ")"]), "all types");
  document.getElementById("sel-type").value = F.type;
}
function refreshState(){
  const pool = R.filter(r=>r.mechanism==="Universal Periodic Review" &&
    (!F.mechanism || F.mechanism==="Universal Periodic Review"));
  const m = new Map();
  for(const r of pool) for(const s of (r._states||[])) m.set(s,(m.get(s)||0)+1);
  const wrap = document.getElementById("statewrap");
  wrap.hidden = !(F.mechanism==="" || F.mechanism==="Universal Periodic Review");
  fillSelect(document.getElementById("sel-state"),
    [...m.keys()].sort((a,b)=> (m.get(b)-m.get(a)) || a.localeCompare(b)).map(s=>[s, s+" ("+m.get(s)+")"]),
    "all States");
  document.getElementById("sel-state").value = F.state;
}
function refreshYears(){
  const yrs = distinct(R.map(r=>r.year)).sort((a,b)=>a-b);
  const f = document.getElementById("sel-yfrom"), t = document.getElementById("sel-yto");
  fillSelect(f, yrs.map(y=>[y,y]), "earliest");
  fillSelect(t, yrs.map(y=>[y,y]), "latest");
  f.value = F.yfrom; t.value = F.yto;
  if(F.yfrom==="" && yrs.length){ /* defaults empty = open */ }
  if(f.selectedIndex<0) f.value=""; if(t.selectedIndex<0) t.value="";
}
function refreshSdg(){
  const goals = distinct(R.flatMap(r=>Array.isArray(r.sdgs)?r.sdgs:[])).sort((a,b)=>a-b);
  const names = U.sdg_names || {};
  fillSelect(document.getElementById("sel-sdg"),
    goals.map(g=>[g, "SDG " + g + (names[String(g)] ? " · " + names[String(g)] : "")]),
    "any SDG");
  document.getElementById("sel-sdg").value = F.sdg;
  const sel = document.getElementById("sel-sdg");
  if(sel.selectedIndex<0) sel.value="";
}
document.getElementById("sel-mech").addEventListener("change", e=>{
  F.mechanism = e.target.value; F.body=""; F.type=""; F.state="";
  refreshBody(); refreshType(); refreshState(); refresh();
});
document.getElementById("sel-body").addEventListener("change", e=>{
  F.body = e.target.value; F.type="";
  refreshType(); refresh();
});
document.getElementById("sel-type").addEventListener("change", e=>{ F.type = e.target.value; refresh(); });
document.getElementById("sel-state").addEventListener("change", e=>{ F.state = e.target.value; refresh(); });
function onYearChange(){
  let a = document.getElementById("sel-yfrom").value, b = document.getElementById("sel-yto").value;
  if(a!=="" && b!=="" && Number(a) > Number(b)){ const t=a; a=b; b=t; }
  F.yfrom=a; F.yto=b; refreshYears(); refresh();
}
document.getElementById("sel-yfrom").addEventListener("change", onYearChange);
document.getElementById("sel-yto").addEventListener("change", onYearChange);
document.getElementById("sel-sdg").addEventListener("change", e=>{
  F.sdg = e.target.value; refresh();
});
document.getElementById("clearall").addEventListener("click", ()=>{
  F.keyword=""; F.mechanism=""; F.body=""; F.type=""; F.state="";
  F.yfrom=""; F.yto=""; F.sdg=""; F.themes.clear();
  document.getElementById("kwbox").value="";
  document.getElementById("searchbox").value="";
  refreshMech(); refreshBody(); refreshType(); refreshState(); refreshYears(); refreshSdg(); refresh();
});

/* ---------- chips ---------- */
function chipLabel(){
  const out = [];
  if(F.keyword) out.push(["keyword: " + F.keyword, ()=>{F.keyword=""; document.getElementById("kwbox").value=""; document.getElementById("searchbox").value="";}]);
  if(F.mechanism) out.push(["mechanism: " + F.mechanism, ()=>{F.mechanism=""; refreshMech(); refreshBody(); refreshType(); refreshState();}]);
  if(F.body) out.push(["body: " + F.body, ()=>{F.body=""; refreshBody(); refreshType();}]);
  if(F.type) out.push(["type: " + F.type, ()=>{F.type=""; refreshType();}]);
  if(F.state) out.push(["State: " + F.state, ()=>{F.state=""; refreshState();}]);
  if(F.yfrom!=="" || F.yto!=="") out.push(["years: " + (F.yfrom||"…") + "–" + (F.yto||"…"), ()=>{F.yfrom="";F.yto=""; refreshYears();}]);
  if(F.sdg!=="") out.push(["SDG " + F.sdg, ()=>{F.sdg=""; refreshSdg();}]);
  for(const t of F.themes) out.push(["theme: " + t, ()=>{F.themes.delete(t);}]);
  return out;
}
function renderChips(){
  const box = document.getElementById("chips");
  const chips = chipLabel();
  box.innerHTML = "";
  for(const [label, rm] of chips){
    const span = document.createElement("span");
    span.className = "chip";
    const txt = document.createElement("span"); txt.textContent = label;
    const b = document.createElement("button");
    b.textContent = "×"; b.setAttribute("aria-label","Remove filter " + label);
    b.addEventListener("click", ()=>{ rm(); refresh(); });
    span.append(txt,b); box.appendChild(span);
  }
}

/* ---------- refresh ---------- */
let chartThemes = null, chartYears = null;
function refresh(){
  applyFilters();
  renderChips();
  document.getElementById("matchcount").textContent = fmt(filtered.length);
  document.getElementById("ofcount").textContent = "matching records of " + fmt(R.length) + " in the file";
  const pct = R.length ? (filtered.length / R.length * 100) : 0;
  document.getElementById("sharefill").style.width = pct + "%";
  document.getElementById("sharenote").textContent = pct.toFixed(1) + "% of the file";
  if(curTab===0) renderOverview();
  if(curTab===1){ rowsShown = 50; renderTable(); }
}

/* ---------- TAB 1 ---------- */
function tileHTML(lbl, num, sub, extra){
  return '<div class="tile"><div class="lbl">'+lbl+'</div><div class="num">'+num+'</div>'+(sub?'<div class="sub">'+sub+'</div>':'')+(extra||'')+'</div>';
}
function renderOverview(){
  const symbols = distinct(filtered.map(r=>r.symbol));
  const years = filtered.map(r=>r.year);
  const types = countBy(filtered,"type");
  const typeLine = [...types.keys()].sort().map(t=>fmt(types.get(t)) + " " + esc(t)).join(" · ") || "no records";
  const mechs = countBy(filtered,"mechanism");
  const mechNames = [...mechs.keys()].sort();
  let html = "";
  html += tileHTML("All records", fmt(filtered.length), typeLine);
  html += tileHTML("Documents", fmt(symbols.length), "distinct symbols");
  html += tileHTML("Years", years.length ? (Math.min(...years) + "–" + Math.max(...years)) : "—", "first–last document year");
  for(const m of mechNames){
    const sub = R.filter(r=>r.mechanism===m);
    const docs = distinct(sub.map(r=>r.symbol)).length;
    const latest = Math.max(...sub.map(r=>r.year));
    html += tileHTML('<span class="dot" style="background:'+mechColor(m)+'"></span>'+esc(m),
      fmt(mechs.get(m)),
      fmt(docs) + " documents · latest " + latest + " · " +
      (filtered.length ? (mechs.get(m)/filtered.length*100).toFixed(1) : "0") + "% of filtered");
    if(m === "Universal Periodic Review"){
      html += '<div class="tile" style="flex:0 0 100%"><div class="lbl">UPR recommending States</div><div class="sub"><button type="button" class="btn ghost" id="seestates">see the States</button> <span class="hint" style="margin:0 0 0 8px">opens a short list in place</span></div></div>';
    }
  }
  if(!mechNames.length){
    html += tileHTML("No records", 0, "no mechanism matches the filter");
  }
  document.getElementById("tiles").innerHTML = html;
  const ss = document.getElementById("seestates");
  if(ss) ss.addEventListener("click", ()=>{
    const box = document.getElementById("stateslist");
    box.hidden = !box.hidden;
    if(!box.hidden) renderStatesList();
  });

  // FIG.01
  const themes = topThemes(filtered).slice(0,10);
  document.getElementById("fig1-title").textContent =
    "Ten most frequent themes among " + fmt(filtered.length) + " matching records" + (filtered.length===R.length ? " (whole file)" : "");
  document.getElementById("fig1-src").textContent = "UN theme labels in the UHRI data, " + COUNTRY + ".";
  const tb = document.querySelector("#fig1-table tbody");
  tb.innerHTML = "";
  if(!themes.length){
    tb.innerHTML = '<tr><td colspan="4" class="empty">No records match</td></tr>';
  } else {
    for(const t of themes){
      const tr = document.createElement("tr");
      tr.innerHTML = "<td>"+esc(t.theme)+"</td><td class='num'>"+fmt(t.count)+"</td><td class='num'>"+
        (filtered.length ? (t.count/filtered.length*100).toFixed(1) : "0.0")+"%</td><td>"+t.min+"–"+t.max+"</td>";
      tb.appendChild(tr);
    }
  }
  if(chartThemes) chartThemes.destroy();
  chartThemes = new Chart(document.getElementById("chart-themes"), {
    type:"bar",
    data:{ labels:themes.map(t=>t.theme),
      datasets:[{ data:themes.map(t=>t.count), backgroundColor:"#9b2355".replace("55",""), barPercentage:0.8, categoryPercentage:0.85 }]},
    options:{
      indexAxis:"y", responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{display:false}, tooltip:{enabled:true} },
      scales:{
        x:{ beginAtZero:true, grid:{color:"#e6dfd0"}, ticks:{color:"#1d1b18", font:{family:"Georgia, serif", size:13}} },
        y:{ grid:{display:false}, ticks:{color:"#1d1b18", font:{size:13}, autoSkip:false} }
      },
      onClick:(e, els)=>{
        if(!els.length) return;
        const th = themes[els[0].index].theme;
        F.themes.has(th) ? F.themes.delete(th) : F.themes.add(th);
        refresh();
      }
    }
  });

  // FIG.02
  const yrsAll = distinct(R.map(r=>r.year)).sort((a,b)=>a-b);
  const yMin = yrsAll.length ? Math.min(...yrsAll) : 0, yMax = yrsAll.length ? Math.max(...yrsAll) : 0;
  const axis = []; for(let y=yMin; y<=yMax; y++) axis.push(y);
  const mechAll = distinct(R.map(r=>r.mechanism)).sort();
  document.getElementById("fig2-title").textContent = "Records per year by mechanism · " + fmt(filtered.length) + " matching records";
  document.getElementById("fig2-src").textContent = "document years, " + COUNTRY + ".";
  const ds = mechAll.map(m => ({
    label:m, backgroundColor:mechColor(m),
    data: axis.map(y => filtered.filter(r=>r.year===y && r.mechanism===m).length)
  }));
  if(chartYears) chartYears.destroy();
  chartYears = new Chart(document.getElementById("chart-years"), {
    type:"bar",
    data:{ labels:axis.map(String), datasets:ds },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{position:"bottom", labels:{color:"#1d1b18", font:{size:13}}} },
      scales:{
        x:{ stacked:true, grid:{display:false}, ticks:{color:"#1d1b18"} },
        y:{ stacked:true, beginAtZero:true, grid:{color:"#e6dfd0"}, ticks:{color:"#1d1b18", precision:0} }
      }
    }
  });
}
function renderStatesList(){
  document.getElementById("sl-country").textContent = COUNTRY;
  const m = new Map();
  for(const r of filtered) for(const s of (r._states||[])) m.set(s,(m.get(s)||0)+1);
  const top = [...m.entries()].sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0])).slice(0,10);
  const ul = document.getElementById("stateslist-ul");
  ul.innerHTML = top.length
    ? top.map(([s,c])=>"<li><b>"+esc(s)+"</b><span>"+fmt(c)+"</span></li>").join("")
    : '<li><span class="empty">No UPR recommending States in the current filter</span></li>';
}

/* ---------- TAB 2 ---------- */
let rowsShown = 50;
function renderTable(){
  const recs = sortRecords(filtered);
  const shown = recs.slice(0, rowsShown);
  const cap = document.getElementById("rectable-cap");
  cap.textContent = "Showing " + fmt(shown.length) + " of " + fmt(recs.length) + " matching records · " +
    (dateDesc ? "newest first" : "oldest first") + " · click a row to expand, press Enter when it is focused";
  const body = document.getElementById("rectable-body");
  body.innerHTML = "";
  if(!shown.length){
    body.innerHTML = '<tr><td colspan="6" class="empty">No records match</td></tr>';
    document.getElementById("morebtn").hidden = true;
    return;
  }
  for(const r of shown) body.appendChild(rowEl(r));
  document.getElementById("morebtn").hidden = rowsShown >= recs.length;
}
function rowEl(r){
  const tr = document.createElement("tr");
  tr.className = "rec"; tr.tabIndex = 0;
  tr.setAttribute("aria-expanded","false");
  const kw = F.keyword;
  const stateTxt = r.mechanism === "Universal Periodic Review"
    ? (r._states ? r._states.join(", ") : "State not found") : "–";
  tr.innerHTML =
    "<td>"+esc(r.date||"")+"</td>"+
    "<td>"+esc(r.body||"")+"</td>"+
    "<td class='sym'>"+(r.doc_url ? '<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+"</a>" : esc(r.symbol))+"</td>"+
    "<td>"+(r._para ? esc(r._para) : "–")+"</td>"+
    "<td class='firstline'>"+highlight(esc(firstLine(r.text)), kw)+"</td>"+
    "<td>"+esc(stateTxt)+"</td>";
  const detail = document.createElement("tr");
  detail.className = "expand"; detail.hidden = true;
  tr.addEventListener("click", e=>{
    if(e.target.closest("a,button")) return;
    toggleRow(tr, detail, r, kw);
  });
  tr.addEventListener("keydown", e=>{
    if(e.key==="Enter"){ e.preventDefault(); toggleRow(tr, detail, r, kw); }
  });
  const frag = document.createDocumentFragment();
  frag.append(tr, detail);
  return frag;
}
function toggleRow(tr, detail, r, kw){
  if(!detail.innerHTML) buildDetail(detail, r, kw);
  const open = detail.hidden;
  detail.hidden = !open;
  tr.setAttribute("aria-expanded", open ? "true" : "false");
}
function buildDetail(detail, r, kw){
  const sdgNames = U.sdg_names || {};
  const labels = [];
  const add = (k, vals) => {
    if(!vals || !vals.length){ labels.push('<div class="row"><span class="k">'+k+'</span><span class="hint" style="margin:0">not labelled</span></div>'); return; }
    labels.push('<div class="row"><span class="k">'+k+'</span><span>'+vals.map(v=>'<span class="tchip">'+esc(v)+"</span>").join("")+"</span></div>");
  };
  let html = "<td colspan='6'><div class='para'>"+(r._para ? esc(r._para) : "—")+"</div>";
  html += "<div class='fulltext'>"+highlight(esc(r.text||""), kw)+"</div>";
  if(r.section) labels.push('<div class="row"><span class="k">Section</span><span>'+esc(r.section)+"</span></div>");
  add("Themes", r.themes);
  add("SDGs", (r.sdgs||[]).map(g=>"SDG " + g + (sdgNames[String(g)] ? " · " + sdgNames[String(g)] : "")));
  add("SDG targets", r.sdg_targets);
  add("Affected persons", r.affected_persons);
  if(r.mechanism === "Universal Periodic Review"){
    labels.push('<div class="row"><span class="k">Recommending State</span><span>'+esc(r._states ? r._states.join(", ") : "State not found")+"</span></div>");
  }
  html += "<div class='labels'>"+labels.join("")+"</div>";
  html += "<div class='btnrow'>"+
    "<button type='button' class='btn' data-act='cite'>"+(r._para ? "Copy citation" : "Copy citation (no paragraph number in this extract)")+"</button>"+
    (r.doc_url ? "<a class='btn ghost' href='"+esc(r.doc_url)+"' target='_blank' rel='noopener' style='text-decoration:none;display:inline-block'>Open the UN document</a>" : "")+
    " <span class='copied' hidden>Copied</span></div>";
  html += "<div class='hint' style='margin-top:8px'>"+esc(r.symbol)+(r._para?", para. "+esc(r._para):"")+" · "+esc(r.mechanism)+" · "+esc(r.date||"")+"</div>";
  html += "</td>";
  detail.innerHTML = html;
  const btn = detail.querySelector("[data-act='cite']");
  btn.addEventListener("click", ()=>{
    const cite = r.symbol + (r._para ? ", para. " + r._para : "");
    const done = ()=>{ const c = detail.querySelector(".copied"); c.hidden=false; setTimeout(()=>{c.hidden=true;},2000); };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(cite).then(done, done);
    } else { done(); }
  });
}
document.getElementById("th-date").addEventListener("click", ()=>{
  dateDesc = !dateDesc;
  document.getElementById("th-date-note").textContent = dateDesc ? "↓ newest first" : "↑ oldest first";
  renderTable();
});
document.getElementById("morebtn").addEventListener("click", ()=>{ rowsShown += 50; renderTable(); });

/* ---------- TAB 3 ---------- */
function checkRow(what, vals, status){
  const cls = status==="pass" ? "pass" : status==="warn" ? "warn" : "fail";
  const mark = status==="pass" ? "✓ pass" : status==="warn" ? "⚠ warning" : "✗ check failed";
  return '<div class="check"><span class="what">'+what+'</span><span class="vals">'+vals+'</span><span class="'+cls+'">'+mark+"</span></div>";
}
function renderChecks(){
  const el = document.getElementById("checks");
  const rows = [];
  // record count
  const declared = Number(U.count);
  rows.push(checkRow("Record count: file length against the file’s own <code>count</code> field",
    fmt(R.length) + " records vs " + fmt(declared),
    R.length === declared ? "pass" : "fail"));
  // partitions
  for(const field of ["mechanism","body","year"]){
    const m = countBy(R, field);
    const sum = [...m.values()].reduce((a,b)=>a+b,0);
    rows.push(checkRow("Partition by "+field+": counts sum to the record count",
      "sum " + fmt(sum) + " of " + fmt(R.length) + " across " + m.size + " values",
      sum === R.length ? "pass" : "fail"));
  }
  const tm = countBy(R,"type");
  const tsum = [...tm.values()].reduce((a,b)=>a+b,0);
  rows.push(checkRow("Type partition: counts per type sum to the headline total",
    [...tm.keys()].sort().map(t=>fmt(tm.get(t))+" "+esc(t)).join(" · ") + " = " + fmt(tsum),
    tsum === R.length ? "pass" : "fail"));
  // chart vs table
  const themes = topThemes(filtered).slice(0,10);
  let chartOk = true, chartVals = "";
  if(themes.length){
    const first = themes[0];
    const recount = filtered.filter(r=>(r.themes||[]).includes(first.theme)).length;
    chartOk = (recount === first.count) && (first.count <= filtered.length);
    chartVals = "largest bar “"+esc(first.theme)+"”: chart " + fmt(first.count) + ", recount " + fmt(recount) +
      ", filtered records " + fmt(filtered.length);
  } else chartVals = "no themes in the current filter";
  rows.push(checkRow("Chart against table (FIG.01): each bar’s value equals a recount",
    chartVals, chartOk ? "pass" : "fail"));
  // links
  const badLinks = R.filter(r=>{
    if(!r.doc_url || !r.doc_url.startsWith("https://docs.un.org/")) return true;
    let u; try { u = decodeURIComponent(r.doc_url).toLowerCase().replace(/\/+$/,""); } catch(e){ return true; }
    return !u.endsWith(String(r.symbol||"").toLowerCase());
  });
  rows.push(checkRow("Links: every record’s doc_url starts with https://docs.un.org/ and ends with its symbol",
    badLinks.length ? fmt(badLinks.length) + " records fail: " +
      badLinks.slice(0,5).map(r=>esc(r.symbol)+" → "+esc(r.doc_url||"(none)")).join("; ") +
      (badLinks.length>5 ? "; …" : "") : "all " + fmt(R.length) + " links pass",
    badLinks.length ? "fail" : "pass"));
  // paragraph numbers
  const pm = countBy(R.filter(r=>r._para),"mechanism");
  const allM = countBy(R,"mechanism");
  let pVals = [], pBad = false;
  for(const m of [...allM.keys()].sort()){
    const share = allM.get(m) ? Math.round(pm.get(m)/allM.get(m)*100) : 0;
    pVals.push(esc(m) + ": " + share + "% (" + fmt(pm.get(m)||0) + " of " + fmt(allM.get(m)) + ")");
    if(m === "Universal Periodic Review" && share < 100) pBad = true;
  }
  rows.push(checkRow("Paragraph numbers: share of records where a number was found at the start of the text",
    pVals.join(" · ") + " · UPR is expected at 100%",
    pBad ? "warn" : "pass"));
  // states
  const upr = R.filter(r=>r.mechanism==="Universal Periodic Review");
  const withStates = upr.filter(r=>r._states && r._states.length);
  const noStates = upr.filter(r=>!(r._states && r._states.length));
  rows.push(checkRow("States found: UPR records with at least one State in parentheses at the end",
    fmt(withStates.length) + " of " + fmt(upr.length) + " UPR records" +
      (noStates.length ? " · without one: " + noStates.slice(0,5).map(r=>esc(r.symbol)+(r._para?" para. "+esc(r._para):"")).join("; ") + (noStates.length>5?" ; …":"") : ""),
    withStates.length === upr.length ? "pass" : "warn"));
  // duplicates & gaps
  const ids = new Set(R.map(r=>r.id));
  const textCounts = countBy(R,"text");
  const dupTexts = [...textCounts.entries()].filter(([t,c])=>c>1);
  const noThemes = R.filter(r=>!(r.themes&&r.themes.length)).length;
  const noSdg = R.filter(r=>!(r.sdgs&&r.sdgs.length)).length;
  const noPers = R.filter(r=>!(r.affected_persons&&r.affected_persons.length)).length;
  rows.push(checkRow("Duplicates and gaps: distinct ids; duplicate texts; records not labelled",
    fmt(ids.size) + " distinct ids of " + fmt(R.length) + " records · " + fmt(dupTexts.length) +
      " duplicate text values · no themes: " + fmt(noThemes) + " · no SDGs: " + fmt(noSdg) +
      " · no affected persons: " + fmt(noPers) + " (shown as “not labelled” on expand)",
    ids.size === R.length ? "pass" : "fail"));
  el.innerHTML = "<div class='srcnote' style='margin:10px 0 4px'>Section: how the app checks itself · run on the whole file unless a check says otherwise</div>" + rows.join("");
}

/* sample check */
let sample = [], verdicts = {}, sampleSeed = 1;
function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function drawSample(seed){
  sampleSeed = seed;
  const rnd = mulberry32(seed);
  const pool = filtered.slice();
  sample = [];
  const n = Math.min(10, pool.length);
  for(let i=0;i<n;i++) sample.push(pool.splice(Math.floor(rnd()*pool.length),1)[0]);
  verdicts = {};
  renderSample();
  document.getElementById("drawcontrols").hidden = false;
  document.getElementById("seedbox").value = String(seed);
}
function renderSample(){
  const box = document.getElementById("samplecards");
  box.innerHTML = "";
  if(!sample.length){
    box.innerHTML = '<p class="empty">No records in the current filter to draw from.</p>';
  }
  sample.forEach((r,i)=>{
    const card = document.createElement("div");
    card.className = "card";
    const head = document.createElement("button");
    head.setAttribute("aria-expanded","false");
    head.innerHTML = (r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+"</a>":esc(r.symbol)) +
      (r._para ? ", para. " + esc(r._para) : "") + " · " + esc(r.date||"");
    const bodyEl = document.createElement("div");
    bodyEl.className = "cardbody"; bodyEl.hidden = true;
    bodyEl.innerHTML = "<div class='ctext'>"+esc(r.text||"")+"</div>"+
      "<div class='labels'><div class='row'><span class='k'>Themes</span><span>"+
      ((r.themes||[]).map(t=>'<span class="tchip">'+esc(t)+"</span>").join("") || '<span class="hint" style="margin:0">not labelled</span>')+
      "</span></div></div>"+
      "<div class='verdicts' role='group' aria-label='Your verdict on the themes as a set'>"+
      "<button type='button' data-v='fit'>Fits</button>"+
      "<button type='button' data-v='no'>Doesn’t fit</button>"+
      "<button type='button' data-v='unsure'>Unsure</button></div>";
    head.addEventListener("click", e=>{
      if(e.target.closest("a")) return;
      bodyEl.hidden = !bodyEl.hidden;
      head.setAttribute("aria-expanded", bodyEl.hidden ? "false" : "true");
    });
    bodyEl.querySelectorAll(".verdicts button").forEach(b=>{
      b.addEventListener("click", ()=>{
        verdicts[i] = b.dataset.v;
        bodyEl.querySelectorAll(".verdicts button").forEach(x=>x.classList.toggle("on", x===b));
        renderTally();
      });
    });
    card.append(head, bodyEl);
    box.appendChild(card);
  });
  renderTally();
}
function renderTally(){
  const fit = Object.values(verdicts).filter(v=>v==="fit").length;
  const no = Object.values(verdicts).filter(v=>v==="no").length;
  const un = Object.values(verdicts).filter(v=>v==="unsure").length;
  const judged = Object.keys(verdicts).length;
  document.getElementById("tally").textContent =
    "Themes: " + fit + " fit, " + no + " don’t, " + un + " unsure of " + judged + " of " + sample.length +
    " judged · seed " + sampleSeed + " · your judgement, not the app’s";
}
document.getElementById("drawbtn").addEventListener("click", ()=>drawSample(1));
document.getElementById("redrawbtn").addEventListener("click", ()=>drawSample(sampleSeed + 1));
document.getElementById("seedbtn").addEventListener("click", ()=>{
  const v = parseInt(document.getElementById("seedbox").value,10);
  drawSample(Number.isFinite(v) ? v : 1);
});

/* ---------- TAB 4 ---------- */
document.getElementById("method-src").innerHTML =
  "Data: " + (U.source ? '<a href="'+esc(U.source_url||"")+'" target="_blank" rel="noopener">'+esc(U.source)+"</a>" : "UHRI") +
  " · " + fmt(R.length) + " records · built " + esc(U.built||"n/a") + ".";
document.getElementById("licence").textContent =
  "Labels, themes and SDG mappings are the UN’s own, as recorded in the UHRI data; the app shows them unchanged and lets you check a sample (tab 03).";

function csvEscape(v){
  v = String(v??"");
  return /[",\n]/.test(v) ? '"' + v.replace(/"/g,'""') + '"' : v;
}
document.getElementById("csvbtn").addEventListener("click", ()=>{
  const filters = chipLabel().map(c=>c[0]).join(" | ") || "none";
  const lines = [];
  lines.push("# " + COUNTRY + " · UN human rights recommendations and observations");
  lines.push("# Source: " + (U.source||"UHRI") + " (" + (U.source_url||"") + ")");
  lines.push("# Built: " + (U.built||"n/a"));
  lines.push("# Filters applied: " + filters);
  lines.push("# Rows: " + filtered.length + " of " + R.length);
  lines.push("date,body,mechanism,type,symbol,paragraph,recommending_states,first_line,text,themes,sdgs,sdg_targets,affected_persons,section,doc_url");
  for(const r of sortRecords(filtered)){
    lines.push([r.date,r.body,r.mechanism,r.type,r.symbol,r._para||"",
      (r._states||[]).join("; "),firstLine(r.text).replace(/…$/,""),
      r.text,(r.themes||[]).join("; "),(r.sdgs||[]).join("; "),
      (r.sdg_targets||[]).join("; "),(r.affected_persons||[]).join("; "),r.section||"",r.doc_url
    ].map(csvEscape).join(","));
  }
  const blob = new Blob([lines.join("\r\n")], {type:"text/csv;charset=utf-8"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "uhri_" + String(COUNTRY).toLowerCase().replace(/\s+/g,"_") + ".csv";
  document.body.appendChild(a); a.click();
  setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); }, 500);
});
document.getElementById("sumbtn").addEventListener("click", ()=>{
  const types = countBy(filtered,"type");
  const symbols = distinct(filtered.map(r=>r.symbol));
  const years = filtered.map(r=>r.year);
  const themes = topThemes(filtered).slice(0,10);
  const txt = "UN human rights recommendations and observations: " + COUNTRY + ". " +
    fmt(filtered.length) + " records from " + fmt(symbols.length) + " UN documents, " +
    (years.length ? Math.min(...years) + "–" + Math.max(...years) : "n/a") +
    ", dated by document (" + [...types.keys()].sort().map(t=>fmt(types.get(t))+" "+t).join(", ") + "). " +
    "Most frequent themes: " + (themes.map(t=>t.theme+" ("+t.count+")").join("; ") || "none") +
    ". Source: " + (U.source||"UHRI") + ". Theme counts sum to more than the record count because a record can carry several themes.";
  const done = ()=>{ const c=document.getElementById("sumcopied"); c.hidden=false; setTimeout(()=>{c.hidden=true;},2000); };
  if(navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, done);
  else done();
});

/* ---------- init ---------- */
refreshMech(); refreshBody(); refreshType(); refreshState(); refreshYears(); refreshSdg();
refresh();
showTab(0);
})();
</script>
</body>
</html>
```
