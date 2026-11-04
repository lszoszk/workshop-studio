On any Check card you mark Doesn't fit or Unsure, you can now remove a label or add one from the file; the UN's label stays beside yours, struck through. Your corrections change every count, chart, filter and export, and the switch under the title compares the UN's labels with yours. You can undo each one, download them as CSV and load that CSV again.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations dashboard</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--mute:#5b564c;--serif:Georgia,"Times New Roman",serif;--mono:ui-monospace,Menlo,Consolas,monospace;--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 var(--sans)}
a{color:var(--ink);text-decoration-color:var(--red);text-underline-offset:2px}
a:hover{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
[hidden]{display:none!important}
.wrap{max-width:1320px;margin:0 auto;padding:22px 28px 14px}
.lab{font:600 11.5px/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:0}
.mute{color:var(--mute)}
header h1{font:400 clamp(26px,3.6vw,42px)/1.12 var(--serif);margin:6px 0 8px;max-width:980px}
.meta{margin:0;color:var(--mute);font-size:15px}
.tabs{display:flex;flex-wrap:wrap;gap:2px;margin-top:18px;border-bottom:1px solid var(--rule)}
.tabs button{font:600 12px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;background:none;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:13px 16px;color:var(--mute);cursor:pointer}
.tabs button b{font-weight:700}
.tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.tabs button:hover{color:var(--ink)}
.layout{display:grid;grid-template-columns:268px minmax(0,1fr);gap:30px;margin-top:22px;align-items:start}
.rail{border-right:1px solid var(--rule);padding-right:22px}
.railhead{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}
.linkbtn{background:none;border:0;padding:0;font:600 11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--red);text-decoration:underline;text-underline-offset:3px;cursor:pointer;text-align:left}
.big{font:400 56px/1 var(--serif);font-variant-numeric:tabular-nums}
.matchlab{font-size:15px;margin-top:4px}
.sharebar{height:4px;background:var(--rule);margin:10px 0 12px}
.sharebar i{display:block;height:100%;background:var(--red);width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.chip{font:12px/1.3 var(--mono);color:var(--red);background:none;border:1px solid var(--red);border-radius:999px;padding:3px 10px;cursor:pointer;text-align:left}
.chip:hover{background:var(--red);color:var(--paper)}
.acch{margin:0;border-top:1px solid var(--rule)}
.acch button{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:0;padding:12px 0;font:600 12px/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink);cursor:pointer;text-align:left}
.acch b{color:var(--red);margin-right:6px}
.acch .cnt{color:var(--red);margin-left:6px}
.accp{padding:0 0 14px}
.accp .lab{display:block;margin:10px 0 4px}
input,select{font:16px/1.3 var(--sans);width:100%;padding:8px 9px;border:1px solid #8c8577;background:#fffdf8;color:var(--ink);border-radius:2px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hint{font:12px/1.4 var(--mono);color:var(--mute);margin:6px 0 0}
.panel{min-width:0}
.panel>.lab{margin-bottom:2px}
h2{font:400 clamp(22px,2.4vw,30px)/1.2 var(--serif);margin:0 0 18px}
h3{font:400 22px/1.25 var(--serif);margin:0 0 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:22px 30px;margin-bottom:26px}
.tile{border-top:1px solid var(--ink);padding-top:8px;min-width:0}
.tile .n{font:400 48px/1.05 var(--serif);margin:4px 0 2px;font-variant-numeric:tabular-nums}
.tile .sub{margin:0;font-size:15px}
.how{font:12px/1.5 var(--mono);color:var(--mute);margin:6px 0 0;max-width:80ch}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:7px;vertical-align:-1px}
.statesbox{margin-top:10px;border-top:1px solid var(--rule);padding-top:8px}
.statesbox h4{font:400 17px/1.3 var(--serif);margin:0 0 6px}
.statesbox ol{margin:0 0 6px;padding-left:24px;font-size:15px}
figure.fig{margin:34px 0 0;border-top:1px solid var(--ink);padding-top:10px}
.chartbox{position:relative;margin:10px 0 8px}
.empty{margin:0;padding:24px 0;color:var(--mute)}
.scroll{overflow-x:auto}
table.data{border-collapse:collapse;width:100%;margin-top:10px}
table.data caption{caption-side:top;text-align:left;font:600 11.5px/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);padding-bottom:6px}
table.data th{font:600 11.5px/1.3 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mute);text-align:left;padding:8px 10px;border-bottom:1px solid var(--ink);vertical-align:bottom}
table.data td{padding:9px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
table.data .num,table.data th.num{text-align:right;font-variant-numeric:tabular-nums}
.nw{white-space:nowrap}
.sorter{background:none;border:0;padding:0;font:inherit;letter-spacing:inherit;text-transform:inherit;color:var(--ink);cursor:pointer;text-decoration:underline;text-decoration-color:var(--red);text-underline-offset:3px}
.rowx{cursor:pointer}
.rowx:hover td{background:rgba(29,27,24,.04)}
.rowbtn{background:none;border:0;padding:0;font:inherit;color:inherit;text-align:left;cursor:pointer;width:100%}
.rowbtn::before{content:"+";color:var(--red);font-family:var(--mono);margin-right:8px}
.rowbtn[aria-expanded="true"]::before{content:"\2013"}
mark{background:rgba(155,35,53,.16);color:inherit;padding:0 1px}
.det td{background:#faf7f0}
.detail{display:grid;grid-template-columns:minmax(70px,130px) 1fr;gap:18px;padding:10px 4px}
.pn{font:400 52px/1 var(--serif);color:var(--red)}
.full{margin:0 0 12px;white-space:pre-wrap;max-width:78ch}
.dl{display:grid;grid-template-columns:150px 1fr;gap:6px;margin:6px 0}
.dl dt{padding-top:4px}
.dl dd{margin:0}
.tag{display:inline-block;border:1px solid var(--rule);padding:1px 8px;margin:0 6px 6px 0;font-size:14px;background:var(--paper)}
.btn{font:600 12px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:10px 14px;border:1px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer;text-decoration:none;display:inline-block}
.btn:hover{border-color:var(--red);color:var(--red)}
.btn[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.btn.primary{background:var(--ink);color:var(--paper)}
.btn.primary:hover{background:var(--red);border-color:var(--red);color:var(--paper)}
.ok{font:12px var(--mono);color:var(--red);margin:0 10px 0 8px}
.actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:14px 0 6px}
.more{margin:14px 0 4px}
.searchrow{max-width:640px;margin-bottom:6px}
.searchrow .lab{display:block;margin-bottom:4px}
ol.checks{list-style:none;margin:10px 0 30px;padding:0;border-top:1px solid var(--ink)}
.chk{display:grid;grid-template-columns:118px 1fr;gap:12px;padding:11px 0;border-bottom:1px solid var(--rule)}
.chk .mark{font:600 12px/1.5 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.chk.fail{border-left:3px solid var(--red);padding-left:9px}
.chk.fail .mark{color:var(--red)}
.chk.warn .mark{font-style:italic}
.vals{color:var(--ink)}
details{margin-top:6px;font-size:15px}
summary{cursor:pointer;font:600 12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--red)}
ul.lst{margin:6px 0 0;padding-left:20px;max-height:260px;overflow:auto;font-size:14px}
ol.cards{list-style:none;margin:10px 0 0;padding:0;border-top:1px solid var(--ink)}
.card{border-bottom:1px solid var(--rule)}
.cardline{display:flex;gap:12px;align-items:baseline;padding:9px 0;flex-wrap:wrap}
.cn{font:600 12px var(--mono);color:var(--red);min-width:22px}
.cardbtn{flex:1 1 260px;background:none;border:0;padding:0;font:inherit;color:inherit;text-align:left;cursor:pointer}
.cardbtn::before{content:"+";color:var(--red);font-family:var(--mono);margin-right:8px}
.cardbtn[aria-expanded="true"]::before{content:"\2013"}
.vd{font:12px var(--mono);color:var(--mute)}
.carddet{padding:4px 0 16px 34px}
.sample-ctl{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;margin:12px 0 8px}
.sample-ctl .seed{width:110px}
.tally{font:600 13px/1.5 var(--mono);margin:8px 0 0}
.method li{margin-bottom:8px;max-width:80ch}
dl.src{display:grid;grid-template-columns:150px 1fr;gap:6px 14px;margin:8px 0 0}
dl.src dt{padding-top:3px}
dl.src dd{margin:0}
footer{margin-top:40px;border-top:1px solid var(--rule);padding:12px 0 6px;font:12px/1.5 var(--mono);color:var(--mute)}
.corrbar{display:flex;flex-wrap:wrap;align-items:center;gap:4px 26px;margin-top:14px;padding-top:10px;border-top:1px solid var(--rule)}
.corrline{margin:0;font:13px/1.5 var(--mono)}
.corrbar .hint{margin:0}
.sw{display:inline-flex;align-items:center;gap:10px;background:none;border:0;padding:4px 2px;cursor:pointer;font:600 12px/1.3 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--ink)}
.sw .sl{color:var(--mute);padding-bottom:2px;border-bottom:2px solid transparent}
.sw .sl.on{color:var(--ink);border-bottom-color:var(--red)}
.sw .track{position:relative;width:44px;height:22px;border:1px solid var(--ink);border-radius:999px;background:var(--paper)}
.sw .track i{position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:var(--ink)}
.sw[aria-checked="true"] .track{background:var(--red);border-color:var(--red)}
.sw[aria-checked="true"] .track i{left:24px;background:var(--paper)}
.tag.mine{border-color:var(--red);color:var(--red);font-style:italic;background:rgba(155,35,53,.07)}
.tag.gone{border-style:dashed;color:var(--mute);background:transparent}
.tag s{text-decoration-color:var(--red);text-decoration-thickness:2px}
.tagx{background:none;border:0;margin:0;padding:0 2px 0 8px;min-height:24px;font:600 14px/1 var(--mono);color:var(--red);cursor:pointer}
.tagx:hover{text-decoration:underline}
.corr{display:inline-block;font:600 11px/1.2 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--red);border:1px solid var(--red);border-radius:999px;padding:2px 8px;margin-left:8px;white-space:nowrap}
.corr.hid{color:var(--mute);border-color:var(--mute)}
.rowx .corr{display:block;width:max-content;margin:4px 0 0 22px}
.mineword{color:var(--red);font-style:italic}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.editor{margin-top:12px;padding-top:10px;border-top:1px solid var(--rule)}
.editor .lab{margin-bottom:4px}
.addrow{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:flex-end;margin-top:8px}
.addrow label{flex-basis:100%;display:block}
.addrow select{flex:1 1 280px;width:auto;min-width:0}
@media(max-width:860px){.layout{grid-template-columns:1fr}.rail{border-right:0;padding-right:0;border-bottom:1px solid var(--rule);padding-bottom:12px}.wrap{padding:16px}.chk{grid-template-columns:1fr}.dl,dl.src{grid-template-columns:1fr}.detail{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="lab" id="hLab">UHRI</div>
  <h1 id="hTitle">UN human rights recommendations and observations</h1>
  <p class="meta" id="hMeta"></p>
  <div class="corrbar" id="corrBar">
    <p class="corrline" id="corrLine" aria-live="polite"></p>
    <button type="button" class="sw" id="modeSw" role="switch" aria-checked="false" data-act="mode" aria-label="Use my corrections in every count, chart and filter"><span class="sl on" id="swUn">UN labels</span><span class="track" aria-hidden="true"><i></i></span><span class="sl" id="swMe">with my corrections</span></button>
    <span class="hint" id="corrSub"></span>
  </div>
</header>
<div class="tabs" role="tablist" aria-label="Dashboard sections" id="tabs"></div>

<div class="layout">
<aside class="rail" aria-label="Filters">
  <div class="railhead"><span class="lab">Filters</span><button type="button" class="linkbtn" data-act="clear">Clear all</button></div>
  <div id="matchLive" aria-live="polite" aria-atomic="true">
    <div class="big" id="matchN">0</div>
    <div class="matchlab">matching records <span class="mute" id="matchOf"></span></div>
  </div>
  <div class="sharebar" aria-hidden="true"><i id="shareFill"></i></div>
  <div class="chips" id="chips"></div>
  <div id="accs">
    <h3 class="acch"><button type="button" id="ah-kw" aria-expanded="false" aria-controls="ac-kw" data-act="acc" data-k="kw"><span><b>01</b>Keyword<span class="cnt" id="an-kw"></span></span><span aria-hidden="true">+</span></button></h3>
    <div class="accp" id="ac-kw" role="region" aria-labelledby="ah-kw" hidden>
      <label class="lab" for="kwRail">Words (all must match)</label>
      <input id="kwRail" type="search" autocomplete="off" placeholder="e.g. torture">
      <p class="hint">literal match, not synonyms</p>
    </div>
    <h3 class="acch"><button type="button" id="ah-mbt" aria-expanded="false" aria-controls="ac-mbt" data-act="acc" data-k="mbt"><span><b>02</b>Mechanism, body, type<span class="cnt" id="an-mbt"></span></span><span aria-hidden="true">+</span></button></h3>
    <div class="accp" id="ac-mbt" role="region" aria-labelledby="ah-mbt" hidden>
      <label class="lab" for="mechSel">Mechanism</label><select id="mechSel"></select>
      <label class="lab" for="bodySel">Body or mandate</label><select id="bodySel"></select>
      <label class="lab" for="typeSel">Type</label><select id="typeSel"></select>
      <div id="stateWrap"><label class="lab" for="stateSel">Recommending State (UPR only)</label><select id="stateSel"></select></div>
    </div>
    <h3 class="acch"><button type="button" id="ah-ys" aria-expanded="false" aria-controls="ac-ys" data-act="acc" data-k="ys"><span><b>03</b>Years and SDG<span class="cnt" id="an-ys"></span></span><span aria-hidden="true">+</span></button></h3>
    <div class="accp" id="ac-ys" role="region" aria-labelledby="ah-ys" hidden>
      <div class="two">
        <div><label class="lab" for="fromSel">Year from</label><select id="fromSel"></select></div>
        <div><label class="lab" for="toSel">Year to</label><select id="toSel"></select></div>
      </div>
      <label class="lab" for="sdgSel">SDG</label><select id="sdgSel"></select>
    </div>
  </div>
</aside>

<main>
<section class="panel" id="p-ov" role="tabpanel" aria-labelledby="t-ov">
  <p class="lab">01 · Overview</p>
  <h2>What has the UN said, how much, and when?</h2>
  <div class="tiles" id="tiles1"></div>
  <div class="tiles" id="tiles2"></div>
  <figure class="fig">
    <p class="lab">FIG.01</p>
    <h3 id="fig1t"></h3>
    <div class="chartbox" id="box1"><canvas id="c1" role="img" aria-label="Ranked horizontal bars of the ten most frequent themes"></canvas><p class="empty" id="c1e" hidden></p></div>
    <div class="scroll">
    <table class="data" id="themeTable">
      <caption>The same ten themes as a table</caption>
      <thead><tr><th scope="col">Theme <span style="text-transform:none;letter-spacing:0">(click = filter)</span></th><th scope="col" class="num">Records</th><th scope="col" class="num">% of filtered</th><th scope="col" class="num">Years (first–last)</th></tr></thead>
      <tbody id="themeRows"></tbody>
    </table>
    </div>
    <p class="how" id="fig1n"></p>
    <p class="how" id="fig1l"></p>
    <p class="how">A theme confined to early years may be a legacy label that no longer describes its text. <button type="button" class="linkbtn" data-act="goto" data-t="chk">Judge a sample of the labels on 03 Check</button></p>
    <p class="how" id="fig1s"></p>
  </figure>
  <figure class="fig">
    <p class="lab">FIG.02</p>
    <h3 id="fig2t"></h3>
    <div class="chartbox" style="height:310px"><canvas id="c2" role="img" aria-label="Stacked bars of records per year by mechanism"></canvas><p class="empty" id="c2e" hidden></p></div>
    <p class="how" id="fig2n"></p>
    <p class="how" id="fig2s"></p>
  </figure>
</section>

<section class="panel" id="p-rec" role="tabpanel" aria-labelledby="t-rec" hidden>
  <p class="lab">02 · Records</p>
  <h2>Which paragraph says it, and in which UN document?</h2>
  <div class="searchrow"><label class="lab" for="kwMain">Search</label><input id="kwMain" type="search" autocomplete="off" placeholder="Search records, e.g. torture"><p class="hint">literal match, not synonyms · same box as 01 Keyword</p></div>
  <div class="scroll">
  <table class="data" id="recTable">
    <caption id="recCap"></caption>
    <thead><tr>
      <th scope="col"><button type="button" class="sorter" data-act="sortdate" id="dateSort" aria-label="Date: click to reverse the order">Date ▼</button></th>
      <th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line <span style="text-transform:none;letter-spacing:0">(click a row to open it)</span></th><th scope="col">Recommending State</th>
    </tr></thead>
    <tbody id="recBody"></tbody>
  </table>
  </div>
  <div class="more"><button type="button" class="btn" id="moreBtn" data-act="more">Show 50 more</button></div>
  <p class="how" id="recSrc"></p>
</section>

<section class="panel" id="p-chk" role="tabpanel" aria-labelledby="t-chk" hidden>
  <p class="lab">03 · Check</p>
  <h2>Can I trust these numbers?</h2>
  <p class="lab">How the app checks itself</p>
  <h3>Check this dashboard</h3>
  <p class="how" id="checkSum"></p>
  <ol class="checks" id="checks"></ol>
  <p class="lab">Random-sample label check</p>
  <h3>Do the UN's theme labels fit the paragraphs?</h3>
  <p>This is your judgement of the UN's labels; nothing is sent anywhere. Mark a set Doesn't fit or Unsure to correct its labels.</p>
  <div class="sample-ctl">
    <div class="seed"><label class="lab" for="seed">Seed</label><input id="seed" type="number" min="0" step="1" value="1"></div>
    <button type="button" class="btn primary" id="drawBtn" data-act="draw">Check 10 at random</button>
    <button type="button" class="btn" data-act="seeddraw">Draw with this seed</button>
  </div>
  <p class="hint" id="sampleHint"></p>
  <p class="tally" id="tally" aria-live="polite"></p>
  <ol class="cards" id="cards"></ol>
  <p class="lab" style="margin-top:34px">Your corrections</p>
  <h3>Keep them, undo them, take them with you</h3>
  <p class="how">Corrections live only in this page: download them before you close it. The CSV holds symbol, paragraph, the UN's labels, your labels and your mark, plus the record id so that loading it finds the same record again. The file is read in your browser; nothing is sent anywhere.</p>
  <div class="actions">
    <button type="button" class="btn primary" data-act="corrdl">Download my corrections (CSV)</button>
    <button type="button" class="btn" data-act="corrload">Load corrections (CSV)</button>
    <input type="file" id="corrFile" accept=".csv,text/csv,text/plain" hidden aria-label="Choose a corrections CSV file">
  </div>
  <p class="how" id="corrStatus" role="status"></p>
  <div id="corrMiss"></div>
  <details><summary id="corrSum">List and undo my corrections (0)</summary><ul class="lst" id="corrList"></ul></details>
</section>

<section class="panel" id="p-met" role="tabpanel" aria-labelledby="t-met" hidden>
  <p class="lab">04 · Method &amp; export</p>
  <h2>How was this made, and how do I take it with me?</h2>
  <h3>How each number is computed</h3>
  <ol class="method">
    <li>Every number is a loop over the records of the file you attached; nothing is estimated, no model is called, and nothing leaves the page except the text you choose to copy.</li>
    <li>A record is one paragraph of a UN document. Documents are counted as distinct symbols, and years come from the date of the document, not from the moment a recommendation was made.</li>
    <li>Filters combine with AND. Mechanism, body and type match exactly, the year range is inclusive, an SDG matches when the goal is among the record's SDGs, and a keyword matches when every word occurs in the text or the symbol (literal, not synonyms).</li>
    <li>Themes, SDGs and affected persons are the UN's own labels. A record can carry several themes, so theme counts add up to more than the number of records; the app never removes or renames a UN label.</li>
    <li>On 03 Check you can remove a theme label from a paragraph or add one that occurs in the file. The UN's label stays, struck through, beside yours; the switch under the title decides whether every count, chart, filter and export uses the UN's labels or yours, and the CSV on 03 Check saves your corrections so you can load them again.</li>
    <li>The paragraph number is the number at the start of the text. The recommending State is read only from UPR records, from the parentheses that end the text; where nothing fits, the row says State not found.</li>
    <li>A citation is the symbol plus ", para." and the number; where no number was found it is the symbol alone.</li>
  </ol>
  <h3 style="margin-top:26px">Take it with you</h3>
  <p class="hint" id="expInfo"></p>
  <div class="actions">
    <button type="button" class="btn primary" data-act="csv">Download CSV of the current filter</button>
    <button type="button" class="btn" data-act="copysum">Copy summary</button><span class="ok" id="expStatus" role="status"></span>
  </div>
  <h3 style="margin-top:26px">The data</h3>
  <dl class="src" id="srcList"></dl>
</section>
</main>
</div>

<footer id="foot"></footer>
</div>

<script>
(function(){
'use strict';
var D=(window.WORKSHOP_DATA&&window.WORKSHOP_DATA.uhri)||{};
var RAW=Array.isArray(D.records)?D.records:[];
var COUNTRY=D.country?String(D.country):'this country';
var SDG_NAMES=D.sdg_names||{};
var UPR='Universal Periodic Review';
var COLORS={};COLORS[UPR]='#c2410c';COLORS['Treaty bodies']='#0f766e';COLORS['Special Procedures']='#7c3aed';
var OTHERC='#6b6558';
var PAGE=50;
var PARA_RE=/^(\d{1,3}(?:\.\d{1,3})?)\.?\s/;
var TAIL_RE=/((?:\s*\((?:[^()]|\([^()]*\))*\))+)\s*[;.]?\s*$/;
var GROUP_RE=/\((?:[^()]|\([^()]*\))*\)/g;

function $(id){return document.getElementById(id);}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function fmt(n){return Number(n).toLocaleString('en-US');}
function pct(a,b){return (b?100*a/b:0).toFixed(1)+'%';}
function arr(v){return Array.isArray(v)?v:[];}
function str(v){return v==null?'':String(v);}
function cnt(){return Object.create(null);}
function uniq(a){return a.filter(function(x,i){return a.indexOf(x)===i;});}
function safeUrl(u){return /^https?:\/\//i.test(u)?u:'';}
function colorOf(m){return COLORS[m]||OTHERC;}
function mlabel(m){return m||'(mechanism not stated)';}
function rx(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function ci(a,b){a=a.toLowerCase();b=b.toLowerCase();return a<b?-1:a>b?1:0;}
function short(s,n){return s.length>n?s.slice(0,n-1)+'…':s;}
function yr(a,b){return a===null?'–':(a===b?String(a):a+'–'+b);}

function extractStates(text){
  var m=TAIL_RE.exec(text);
  if(!m)return [];
  var groups=m[1].match(GROUP_RE)||[];
  var out=[];
  groups.forEach(function(g){
    var s=g.slice(1,-1).trim();
    if(s&&s.indexOf(',')<0&&s.length<=60&&out.indexOf(s)<0)out.push(s);
  });
  return out;
}

/* ---------- prepare records ---------- */
var recs=RAW.map(function(r,i){
  r=r||{};
  var text=str(r.text),m=PARA_RE.exec(text),para=m?m[1]:'';
  var y=(r.year===null||r.year===undefined||r.year==='')?NaN:Number(r.year);
  var mech=str(r.mechanism),parts=para?para.split('.').map(Number):[];
  return {i:i,id:str(r.id),symbol:str(r.symbol),url:str(r.doc_url),date:str(r.date),year:isFinite(y)?y:null,
    body:str(r.body),mech:mech,type:str(r.type),section:str(r.section),text:text,
    un:uniq(arr(r.themes).map(str).filter(Boolean)),themes:[],
    sdgs:uniq(arr(r.sdgs).map(Number).filter(function(x){return isFinite(x);})),
    targets:arr(r.sdg_targets).map(str),persons:arr(r.affected_persons).map(str),
    para:para,p1:parts.length?parts[0]:Infinity,p2:parts.length>1?parts[1]:-1,
    states:mech===UPR?extractStates(text):[],
    lc:(text+' '+str(r.symbol)).toLowerCase()};
});
recs.forEach(function(o){o.themes=o.un.slice();});
var N=recs.length;

var mc=cnt();recs.forEach(function(o){mc[o.mech]=(mc[o.mech]||0)+1;});
var KNOWN=[UPR,'Treaty bodies','Special Procedures'];
var MECHS=KNOWN.filter(function(k){return k in mc;}).concat(Object.keys(mc).filter(function(k){return KNOWN.indexOf(k)<0;}).sort());
var ym=cnt();recs.forEach(function(o){if(o.year!==null)ym[o.year]=1;});
var YEARS=Object.keys(ym).map(Number).sort(function(a,b){return a-b;});
var tcAll=cnt();recs.forEach(function(o){if(o.type)tcAll[o.type]=(tcAll[o.type]||0)+1;});
var TYPES=Object.keys(tcAll).sort(function(a,b){return tcAll[b]-tcAll[a]||ci(a,b);});
var stAll=cnt();recs.forEach(function(o){o.states.forEach(function(s){stAll[s]=(stAll[s]||0)+1;});});
var STATE_LIST=Object.keys(stAll).sort(ci);
var sdAll=cnt();recs.forEach(function(o){o.sdgs.forEach(function(g){sdAll[g]=1;});});
var SDG_LIST=Object.keys(sdAll).map(Number).sort(function(a,b){return a-b;});
var DOCS=new Set(recs.map(function(o){return o.symbol;})).size;
var thAll=cnt();recs.forEach(function(o){o.un.forEach(function(t){thAll[t]=(thAll[t]||0)+1;});});
var ALL_THEMES=Object.keys(thAll).sort(ci);

function minmax(L){
  var a=null,b=null;
  for(var k=0;k<L.length;k++){var y=L[k].year;if(y===null)continue;if(a===null||y<a)a=y;if(b===null||y>b)b=y;}
  return {a:a,b:b};
}
var FILEYEARS=minmax(recs);

/* ---------- state ---------- */
var S={kw:'',mech:'',body:'',type:'',state:'',from:'',to:'',sdg:'',themes:[]};
var WORDS=[],HLRE=null,FILTERED=[],SORTED=[],dateAsc=false,shown=PAGE,OPEN={},THEME_TOP=[],LAST_BARS=[],CHIPFN=[];
var active='ov',openAcc='',statesOpen=false,charts={t:null,m:null},FILECHK=null;
var SAMPLE=[],MARK={},CORR={},MODE='un',SEED=1,kwT=null;
var MARKS={fit:'fits',no:"doesn't fit",unsure:'unsure'};
var TABS=[
  {id:'ov',num:'01',name:'Overview'},
  {id:'rec',num:'02',name:'Records'},
  {id:'chk',num:'03',name:'Check'},
  {id:'met',num:'04',name:'Method &amp; export'}
];

function setWords(){
  WORDS=S.kw.trim().toLowerCase().split(/\s+/).filter(Boolean);
  HLRE=WORDS.length?new RegExp('('+WORDS.map(rx).join('|')+')','gi'):null;
}
function hl(s){
  s=str(s);
  if(!HLRE)return esc(s);
  return s.split(HLRE).map(function(p,i){return i%2?'<mark>'+esc(p)+'</mark>':esc(p);}).join('');
}
function matches(o,skip){
  var k;
  if(skip!=='kw'){for(k=0;k<WORDS.length;k++){if(o.lc.indexOf(WORDS[k])<0)return false;}}
  if(skip!=='mech'&&S.mech&&o.mech!==S.mech)return false;
  if(skip!=='body'&&S.body&&o.body!==S.body)return false;
  if(skip!=='type'&&S.type&&o.type!==S.type)return false;
  if(skip!=='state'&&S.state&&o.states.indexOf(S.state)<0)return false;
  if(skip!=='years'){
    if(S.from!==''&&(o.year===null||o.year<Number(S.from)))return false;
    if(S.to!==''&&(o.year===null||o.year>Number(S.to)))return false;
  }
  if(skip!=='sdg'&&S.sdg!==''&&o.sdgs.indexOf(Number(S.sdg))<0)return false;
  if(skip!=='themes'){for(k=0;k<S.themes.length;k++){if(o.themes.indexOf(S.themes[k])<0)return false;}}
  return true;
}
function facet(getter,skip){
  var m=cnt();
  recs.forEach(function(o){
    if(!matches(o,skip))return;
    var v=getter(o);
    (Array.isArray(v)?v:[v]).forEach(function(x){if(x===''||x===null||x===undefined)return;m[x]=(m[x]||0)+1;});
  });
  return m;
}
function sortRecs(list){
  return list.slice().sort(function(a,b){
    if(a.date!==b.date){var s=a.date<b.date?-1:1;return dateAsc?s:-s;}
    if(a.body!==b.body)return a.body<b.body?-1:1;
    if(a.p1!==b.p1)return a.p1<b.p1?-1:1;
    if(a.p2!==b.p2)return a.p2<b.p2?-1:1;
    return a.i-b.i;
  });
}
function citation(o){return o.symbol+(o.para?', para. '+o.para:'');}
function firstLine(t){
  t=t.replace(/\s+/g,' ').trim();
  if(t.length<=120)return t;
  var cut=t.slice(0,120),sp=cut.lastIndexOf(' ');
  if(sp>0)cut=cut.slice(0,sp);
  return cut+'…';
}
function filterText(){
  var p=[];
  if(WORDS.length)p.push('keyword "'+S.kw.trim()+'"');
  if(S.mech)p.push('mechanism = '+S.mech);
  if(S.body)p.push('body = '+S.body);
  if(S.type)p.push('type = '+S.type);
  if(S.state)p.push('recommending State = '+S.state);
  if(S.from!==''||S.to!=='')p.push('years '+(S.from!==''?S.from:'first')+' to '+(S.to!==''?S.to:'last'));
  if(S.sdg!=='')p.push('SDG '+S.sdg);
  S.themes.forEach(function(t){p.push('theme = '+t);});
  return p.length?p.join('; '):'none';
}

/* ---------- header, footer, static fills ---------- */
function initStatic(){
  var src=D.source?(safeUrl(str(D.source_url))?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">'+esc(D.source)+'</a>':esc(D.source)):'source not stated';
  document.title='UN human rights recommendations: '+COUNTRY;
  $('hLab').textContent='UHRI · '+COUNTRY;
  $('hTitle').textContent='UN human rights recommendations and observations: '+COUNTRY;
  $('hMeta').innerHTML=src+' · '+fmt(N)+' records · '+fmt(DOCS)+' documents · '+yr(FILEYEARS.a,FILEYEARS.b)+' · built '+esc(D.built||'date not stated')+' · dated by document';
  $('foot').innerHTML='Built on OHCHR UHRI data · '+fmt(N)+' records · '+(safeUrl(str(D.source_url))?'<a href="'+esc(D.source_url)+'" target="_blank" rel="noopener">source</a>':'source link not given');
  $('srcList').innerHTML='<dt class="lab">Source</dt><dd>'+src+'</dd><dt class="lab">Records</dt><dd>'+fmt(N)+' records, '+fmt(DOCS)+' documents</dd><dt class="lab">Built</dt><dd>'+esc(D.built||'date not stated')+'</dd><dt class="lab">Licence</dt><dd>Not stated in the file you attached; check the OHCHR terms of use before republishing text. Every row links to the UN document it comes from.</dd>';
  $('fromSel').innerHTML=$('toSel').innerHTML='';
  var yo=YEARS.map(function(y){return '<option value="'+y+'">'+y+'</option>';}).join('');
  $('fromSel').innerHTML='<option value="">First</option>'+yo;
  $('toSel').innerHTML='<option value="">Last</option>'+yo;
  $('kwMain').placeholder='Search '+fmt(N)+' records, e.g. torture';
  $('stateWrap').hidden=!STATE_LIST.length;
}

/* ---------- tabs ---------- */
function buildTabs(){
  $('tabs').innerHTML=TABS.map(function(t,i){
    return '<button type="button" role="tab" id="t-'+t.id+'" aria-selected="'+(i===0)+'" aria-controls="p-'+t.id+'" tabindex="'+(i===0?0:-1)+'" data-tab="'+t.id+'"><b>'+t.num+'</b> '+t.name+'</button>';
  }).join('');
}
function selectTab(id,focus){
  active=id;
  TABS.forEach(function(t){
    var on=t.id===id,b=$('t-'+t.id);
    b.setAttribute('aria-selected',on?'true':'false');
    b.tabIndex=on?0:-1;
    $('p-'+t.id).hidden=!on;
  });
  $('accs').hidden=!(id==='ov'||id==='rec');
  if(focus)$('t-'+id).focus();
  if(id==='ov')drawCharts();
}
$('tabs').addEventListener('click',function(e){
  var b=e.target.closest('[data-tab]');
  if(b)selectTab(b.getAttribute('data-tab'),false);
});
$('tabs').addEventListener('keydown',function(e){
  var keys=['ArrowRight','ArrowLeft','Home','End'];
  if(keys.indexOf(e.key)<0)return;
  var ids=TABS.map(function(t){return t.id;}),i=ids.indexOf(active);
  if(e.key==='ArrowRight')i=(i+1)%ids.length;
  else if(e.key==='ArrowLeft')i=(i-1+ids.length)%ids.length;
  else if(e.key==='Home')i=0;
  else i=ids.length-1;
  e.preventDefault();
  selectTab(ids[i],true);
});

/* ---------- accordion ---------- */
function syncAcc(){
  ['kw','mbt','ys'].forEach(function(k){
    var open=openAcc===k,b=$('ah-'+k);
    b.setAttribute('aria-expanded',open?'true':'false');
    b.lastElementChild.textContent=open?'–':'+';
    $('ac-'+k).hidden=!open;
  });
}

/* ---------- rail ---------- */
function chipList(){
  var c=[];
  if(WORDS.length)c.push({l:'Keyword: '+S.kw.trim(),f:function(){S.kw='';syncKw();}});
  if(S.mech)c.push({l:'Mechanism: '+S.mech,f:function(){S.mech='';}});
  if(S.body)c.push({l:'Body: '+S.body,f:function(){S.body='';}});
  if(S.type)c.push({l:'Type: '+S.type,f:function(){S.type='';}});
  if(S.state)c.push({l:'State: '+S.state,f:function(){S.state='';}});
  if(S.from!==''||S.to!=='')c.push({l:'Years: '+(S.from!==''?S.from:'first')+'–'+(S.to!==''?S.to:'last'),f:function(){S.from='';S.to='';}});
  if(S.sdg!=='')c.push({l:'SDG '+S.sdg,f:function(){S.sdg='';}});
  S.themes.forEach(function(t){c.push({l:'Theme: '+t,f:function(){S.themes=S.themes.filter(function(x){return x!==t;});}});});
  return c;
}
function fillSelect(sel,allLabel,items,cur){
  sel.innerHTML='<option value="">'+esc(allLabel)+'</option>'+items.map(function(i){return '<option value="'+esc(i.v)+'">'+esc(i.l)+'</option>';}).join('');
  sel.value=cur;
}
function renderRail(){
  var n=FILTERED.length;
  $('matchN').textContent=fmt(n);
  $('matchOf').textContent='of '+fmt(N)+' in the file';
  $('shareFill').style.width=(N?100*n/N:0)+'%';
  CHIPFN=chipList();
  $('chips').innerHTML=CHIPFN.map(function(c,k){
    return '<button type="button" class="chip" data-act="chip" data-k="'+k+'" title="'+esc(c.l)+'" aria-label="Remove filter: '+esc(c.l)+'">'+esc(short(c.l,46))+' <span aria-hidden="true">×</span></button>';
  }).join('');
  var fm=facet(function(o){return o.mech;},'mech');
  fillSelect($('mechSel'),'All mechanisms',MECHS.filter(Boolean).map(function(m){return {v:m,l:m+' ('+fmt(fm[m]||0)+')'};}),S.mech);
  var fb=facet(function(o){return o.body;},'body'),bl=cnt();
  recs.forEach(function(o){if(o.body&&(!S.mech||o.mech===S.mech))bl[o.body]=1;});
  fillSelect($('bodySel'),'All bodies and mandates',Object.keys(bl).sort(ci).map(function(b){return {v:b,l:b+' ('+fmt(fb[b]||0)+')'};}),S.body);
  var ft=facet(function(o){return o.type;},'type');
  fillSelect($('typeSel'),'All types',TYPES.map(function(t){return {v:t,l:t+' ('+fmt(ft[t]||0)+')'};}),S.type);
  var fs=facet(function(o){return o.states;},'state');
  fillSelect($('stateSel'),'All States',STATE_LIST.map(function(s){return {v:s,l:s+' ('+fmt(fs[s]||0)+')'};}),S.state);
  var fg=facet(function(o){return o.sdgs;},'sdg');
  fillSelect($('sdgSel'),'All SDGs',SDG_LIST.map(function(g){return {v:String(g),l:'SDG '+g+(SDG_NAMES[String(g)]?' · '+SDG_NAMES[String(g)]:'')+' ('+fmt(fg[g]||0)+')'};}),S.sdg);
  $('fromSel').value=S.from;$('toSel').value=S.to;
  var a1=WORDS.length?1:0,a2=(S.mech?1:0)+(S.body?1:0)+(S.type?1:0)+(S.state?1:0),a3=((S.from!==''||S.to!=='')?1:0)+(S.sdg!==''?1:0);
  $('an-kw').textContent=a1?'· '+a1:'';$('an-mbt').textContent=a2?'· '+a2:'';$('an-ys').textContent=a3?'· '+a3:'';
}
function syncKw(){$('kwRail').value=S.kw;$('kwMain').value=S.kw;}
function onKw(e){
  var v=e.target.value,other=e.target===$('kwRail')?$('kwMain'):$('kwRail');
  other.value=v;
  clearTimeout(kwT);
  kwT=setTimeout(function(){S.kw=v;update();},300);
}
$('kwRail').addEventListener('input',onKw);
$('kwMain').addEventListener('input',onKw);
$('accs').addEventListener('change',function(e){
  var id=e.target.id,v=e.target.value;
  if(id==='mechSel'){
    S.mech=v;
    if(S.mech&&S.body&&!recs.some(function(o){return o.mech===S.mech&&o.body===S.body;}))S.body='';
  }
  else if(id==='bodySel')S.body=v;
  else if(id==='typeSel')S.type=v;
  else if(id==='stateSel')S.state=v;
  else if(id==='fromSel')S.from=v;
  else if(id==='toSel')S.to=v;
  else if(id==='sdgSel')S.sdg=v;
  else return;
  if(S.from!==''&&S.to!==''&&Number(S.from)>Number(S.to)){var t=S.from;S.from=S.to;S.to=t;}
  update();
});

/* ---------- overview ---------- */
function themeStats(list){
  var m=cnt();
  list.forEach(function(o){
    o.themes.forEach(function(t){
      var e=m[t]||(m[t]={name:t,count:0,y0:null,y1:null});
      e.count++;
      if(o.year!==null){if(e.y0===null||o.year<e.y0)e.y0=o.year;if(e.y1===null||o.year>e.y1)e.y1=o.year;}
    });
  });
  return Object.keys(m).map(function(k){return m[k];}).sort(function(a,b){return b.count-a.count||ci(a.name,b.name);});
}
function stateTop(L){
  var m=cnt(),upr=0,found=0;
  L.forEach(function(o){
    if(o.mech!==UPR)return;
    upr++;if(o.states.length)found++;
    o.states.forEach(function(s){m[s]=(m[s]||0)+1;});
  });
  var a=Object.keys(m).map(function(k){return {name:k,count:m[k]};}).sort(function(x,y){return y.count-x.count||ci(x.name,y.name);});
  return {top:a.slice(0,10),upr:upr,found:found};
}
function tile(label,big,sub,how,extra,color){
  return '<div class="tile"><p class="lab">'+(color?'<span class="dot" style="background:'+color+'"></span>':'')+label+'</p><p class="n">'+big+'</p><p class="sub">'+sub+'</p><p class="how">How this is computed: '+how+'</p>'+(extra||'')+'</div>';
}
function renderOverview(){
  var L=FILTERED,n=L.length,mm=minmax(L);
  var docs=new Set(L.map(function(o){return o.symbol;})).size;
  var tc=cnt();
  L.forEach(function(o){var k=o.type||'(type not stated)';tc[k]=(tc[k]||0)+1;});
  var tl=Object.keys(tc).sort(function(a,b){return tc[b]-tc[a]||ci(a,b);}).map(function(k){return fmt(tc[k])+' '+esc(k);}).join(' · ');
  $('tiles1').innerHTML=
    tile('Records',fmt(n),(n!==N?'of '+fmt(N)+' in the file<br>':'')+(tl||'No records match'),'every record in the filtered set; types are counted as spelled in the data.')+
    tile('Documents',fmt(docs),'distinct UN symbols','distinct symbol values in the filtered set.')+
    tile('Years',mm.a===null?'–':yr(mm.a,mm.b),'first–last year, dated by document','smallest and largest year in the filtered set.');
  $('tiles2').innerHTML=MECHS.map(function(m){
    var Lm=L.filter(function(o){return o.mech===m;}),mx=minmax(Lm);
    var d=new Set(Lm.map(function(o){return o.symbol;})).size;
    var extra='';
    if(m===UPR){
      extra='<p class="how"><button type="button" class="linkbtn" data-act="states" aria-expanded="'+statesOpen+'">see the States</button></p>';
      if(statesOpen){
        var st=stateTop(L);
        extra+='<div class="statesbox"><h4>Ten States that made most recommendations to '+esc(COUNTRY)+'</h4>'+
          (st.top.length?'<ol>'+st.top.map(function(s){return '<li>'+esc(s.name)+' · '+fmt(s.count)+'</li>';}).join('')+'</ol>':'<p>No State found in the current selection.</p>')+
          '<p class="how">How this is computed: States named in the parentheses that end each UPR text; a line made by several States counts once for each. '+fmt(st.found)+' of '+fmt(st.upr)+' UPR records name a State.</p></div>';
      }
    }
    return tile(esc(mlabel(m)),fmt(Lm.length),fmt(d)+' documents · latest '+(mx.b===null?'–':mx.b)+' · '+pct(Lm.length,n)+' of filtered','records with this mechanism in the filtered set; share = records / filtered records.',extra,colorOf(m));
  }).join('');

  var TS=themeStats(L);
  THEME_TOP=TS.slice(0,10);
  LAST_BARS=THEME_TOP.map(function(t){return t.count;});
  $('fig1t').textContent=(TS.length<10?'Most frequent themes (only '+TS.length+' present)':'Ten most frequent themes')+' among '+fmt(n)+' filtered records';
  $('themeRows').innerHTML=THEME_TOP.length?THEME_TOP.map(function(t,k){
    return '<tr data-count="'+t.count+'" data-name="'+esc(t.name)+'"><td><button type="button" class="sorter" data-act="theme" data-k="'+k+'">'+esc(t.name)+'</button></td><td class="num">'+fmt(t.count)+'</td><td class="num">'+pct(t.count,n)+'</td><td class="num">'+yr(t.y0,t.y1)+'</td></tr>';
  }).join(''):'<tr><td colspan="4">'+(n?'No themes are labelled in this selection.':'No records match the current filters.')+'</td></tr>';
  $('fig1n').textContent='How this is computed: each record counts once for every theme it carries, so bars add up to more than the '+fmt(n)+' records; percentages are of records, not of labels. Click a bar = add the theme as a filter.';
  var srcTxt='Source: '+(D.source||'UHRI file')+(D.built?', built '+D.built:'')+'; '+fmt(n)+' of '+fmt(N)+' records.';
  $('fig1s').textContent=srcTxt;
  $('fig1l').textContent='Labels in this figure: '+labelsText()+'. The switch under the title compares them.';
  $('fig2s').textContent=srcTxt;
  var undated=L.filter(function(o){return o.year===null;}).length;
  $('fig2t').textContent='Records per year by mechanism, '+fmt(n)+' filtered records';
  $('fig2n').textContent='How this is computed: records per year and mechanism in the filtered set, zero for missing combinations; empty years show as gaps.'+(undated?' '+fmt(undated)+' records without a year are not drawn.':'');
}

var endLabels={id:'endLabels',afterDatasetsDraw:function(chart){
  var ctx=chart.ctx,meta=chart.getDatasetMeta(0),data=chart.data.datasets[0].data;
  ctx.save();ctx.font='600 13px ui-monospace, Menlo, Consolas, monospace';ctx.fillStyle='#1d1b18';ctx.textBaseline='middle';
  meta.data.forEach(function(bar,i){ctx.fillText(fmt(data[i]),bar.x+6,bar.y);});
  ctx.restore();
}};
function wrap(s,w,maxLines){
  var words=s.split(' '),lines=[],cur='';
  words.forEach(function(x){
    if(cur&&(cur+' '+x).length>w){lines.push(cur);cur=x;}else cur=cur?cur+' '+x:x;
  });
  if(cur)lines.push(cur);
  if(lines.length>maxLines){lines=lines.slice(0,maxLines);lines[maxLines-1]+='…';}
  return lines;
}
function addTheme(name){
  if(S.themes.indexOf(name)<0)S.themes.push(name);
  update();
}
function drawCharts(){
  ['t','m'].forEach(function(k){if(charts[k]){charts[k].destroy();charts[k]=null;}});
  var n=FILTERED.length,hasChart=!!window.Chart;
  var msg=!hasChart?'Chart.js did not load; the table has the same numbers.':'No records match the current filters.';
  var show1=hasChart&&THEME_TOP.length>0;
  $('c1').hidden=!show1;$('c1e').hidden=show1;
  $('c1e').textContent=hasChart&&n?'No themes are labelled in this selection.':msg;
  var mm=minmax(FILTERED),show2=hasChart&&mm.a!==null;
  $('c2').hidden=!show2;$('c2e').hidden=show2;
  $('c2e').textContent=hasChart&&n?'No record in this selection has a year.':msg;
  if(!hasChart)return;
  try{
    Chart.defaults.font.family='system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
    Chart.defaults.color='#1d1b18';
    if(show1){
      var top=THEME_TOP;
      $('box1').style.height=Math.max(160,top.length*46+20)+'px';
      charts.t=new Chart($('c1'),{type:'bar',
        data:{labels:top.map(function(t){return wrap(t.name,34,3);}),datasets:[{data:LAST_BARS,backgroundColor:'rgba(155,35,53,0.8)',hoverBackgroundColor:'#9b2335',barPercentage:0.75,categoryPercentage:0.9}]},
        options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,animation:false,layout:{padding:{right:64}},
          interaction:{mode:'nearest',axis:'y',intersect:false},
          plugins:{legend:{display:false},tooltip:{callbacks:{
            title:function(items){return top[items[0].dataIndex].name;},
            label:function(c){return fmt(c.parsed.x)+' records ('+pct(c.parsed.x,n)+' of filtered)';}}}},
          scales:{x:{display:false,beginAtZero:true},y:{grid:{display:false},border:{display:false},ticks:{autoSkip:false,font:{size:13}}}},
          onClick:function(evt,els){if(els&&els.length)addTheme(top[els[0].index].name);},
          onHover:function(evt,els){if(evt.native&&evt.native.target)evt.native.target.style.cursor=els&&els.length?'pointer':'default';}},
        plugins:[endLabels]});
      $('c1').setAttribute('aria-label','Ranked horizontal bars. Largest: '+top[0].name+', '+fmt(top[0].count)+' records. The table below lists all ten.');
    }
    if(show2){
      var years=[];for(var y=mm.a;y<=mm.b;y++)years.push(y);
      var per={};MECHS.forEach(function(m){per[m]=years.map(function(){return 0;});});
      var tot=years.map(function(){return 0;});
      FILTERED.forEach(function(o){if(o.year===null)return;var k=o.year-mm.a;per[o.mech][k]++;tot[k]++;});
      var peak=0;tot.forEach(function(v,k){if(v>tot[peak])peak=k;});
      charts.m=new Chart($('c2'),{type:'bar',
        data:{labels:years,datasets:MECHS.map(function(m){return {label:mlabel(m),data:per[m],backgroundColor:colorOf(m),stack:'s'};})},
        options:{responsive:true,maintainAspectRatio:false,animation:false,
          plugins:{legend:{position:'top',labels:{boxWidth:12,font:{size:13}}},tooltip:{mode:'index',intersect:false}},
          scales:{x:{stacked:true,grid:{display:false},ticks:{autoSkip:true,maxRotation:0}},y:{stacked:true,beginAtZero:true,ticks:{precision:0},grid:{color:'#e7e1d3'}}}}});
      $('c2').setAttribute('aria-label','Stacked bars of records per year by mechanism, '+mm.a+' to '+mm.b+'. Busiest year: '+years[peak]+' with '+fmt(tot[peak])+' records.');
    }
  }catch(err){
    $('c1e').hidden=false;$('c1e').textContent='The charts could not be drawn ('+err.message+'); the table has the same numbers.';
  }
}

/* ---------- records ---------- */
function detailHtml(o){
  function tags(items,f){return items.length?items.map(function(x){return '<span class="tag">'+esc(f?f(x):x)+'</span>';}).join(''):'<span class="mute">not labelled</span>';}
  var cite=!o.para;
  return '<tr class="det"><td colspan="6"><div class="detail"><div class="pn" aria-label="Paragraph number">'+esc(o.para||'–')+'</div><div>'+
    '<p class="full">'+hl(o.text)+'</p>'+
    '<dl style="margin:0"><div class="dl"><dt class="lab">Themes</dt><dd>'+(MODE==='mine'&&CORR[o.i]?labelsHtml(o,false):tags(o.themes))+corrTag(o)+'</dd></div>'+
    '<div class="dl"><dt class="lab">SDGs</dt><dd>'+tags(o.sdgs,function(g){return 'SDG '+g+(SDG_NAMES[String(g)]?' · '+SDG_NAMES[String(g)]:'');})+'</dd></div>'+
    (o.targets.length?'<div class="dl"><dt class="lab">SDG targets</dt><dd>'+tags(o.targets)+'</dd></div>':'')+
    '<div class="dl"><dt class="lab">Affected persons</dt><dd>'+tags(o.persons)+'</dd></div>'+
    (o.section?'<div class="dl"><dt class="lab">Section</dt><dd>'+esc(o.section)+'</dd></div>':'')+'</dl>'+
    '<div class="actions"><button type="button" class="btn" data-act="copycite" data-i="'+o.i+'">Copy citation'+(cite?' (no paragraph number in this extract)':'')+'</button><span class="ok" role="status"></span>'+
    (safeUrl(o.url)?'<a class="btn" href="'+esc(o.url)+'" target="_blank" rel="noopener">Open the UN document</a>':'<span class="mute">no link in the file</span>')+'</div>'+
    '</div></div></td></tr>';
}
function rowHtml(o){
  var open=!!OPEN[o.i];
  var st=o.mech===UPR?(o.states.length?o.states.map(esc).join('; '):'<span class="mute">State not found</span>'):'<span class="mute">–</span>';
  var h='<tr class="rowx" data-i="'+o.i+'"><td class="nw">'+esc(o.date)+'</td><td>'+hl(o.body)+'</td><td>'+
    (safeUrl(o.url)?'<a href="'+esc(o.url)+'" target="_blank" rel="noopener">'+hl(o.symbol)+'</a>':hl(o.symbol))+'</td><td class="num">'+esc(o.para||'–')+
    '</td><td><button type="button" class="rowbtn" aria-expanded="'+open+'">'+hl(firstLine(o.text))+'</button>'+corrTag(o)+'</td><td>'+st+'</td></tr>';
  return open?h+detailHtml(o):h;
}
function renderRecords(){
  var total=SORTED.length;
  $('recCap').textContent=total?'Showing '+fmt(Math.min(shown,total))+' of '+fmt(total)+' matching records, '+(dateAsc?'oldest':'newest')+' first':'No records match the current filters';
  $('recBody').innerHTML=total?SORTED.slice(0,shown).map(rowHtml).join(''):'<tr><td colspan="6">No records match the current filters. Remove a chip or use Clear all.</td></tr>';
  $('moreBtn').hidden=shown>=total;
  $('dateSort').textContent='Date '+(dateAsc?'▲':'▼');
  $('recSrc').textContent='Source: '+(D.source||'UHRI file')+(D.built?', built '+D.built:'')+'. Dates are the date of the document. Para. is the number at the start of the text; Special Procedures items without one show a dash.';
}
function toggleRow(tr){
  var i=Number(tr.getAttribute('data-i')),open=!OPEN[i];
  OPEN[i]=open;
  tr.querySelector('.rowbtn').setAttribute('aria-expanded',open?'true':'false');
  var nx=tr.nextElementSibling;
  if(open){tr.insertAdjacentHTML('afterend',detailHtml(recs[i]));}
  else if(nx&&nx.classList.contains('det')){nx.remove();}
}

/* ---------- checks ---------- */
function listBox(label,items){
  if(!items.length)return '';
  var cap=300;
  return '<details><summary>'+esc(label)+' ('+fmt(items.length)+')</summary><ul class="lst">'+items.slice(0,cap).map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>'+(items.length>cap?'<p class="hint">'+fmt(items.length-cap)+' more are not listed here.</p>':'')+'</details>';
}
function sumPresent(getter){
  var m=cnt(),s=0,g=0;
  recs.forEach(function(o){var v=getter(o);if(v!==''&&v!==null)m[v]=(m[v]||0)+1;});
  for(var k in m){s+=m[k];g++;}
  return {sum:s,groups:g};
}
function snippet(o,tail){var t=o.text.replace(/\s+/g,' ');return esc(tail?'…'+t.slice(-90):t.slice(0,90)+(t.length>90?'…':''));}
function recLink(o){return (safeUrl(o.url)?'<a href="'+esc(o.url)+'" target="_blank" rel="noopener">'+esc(o.symbol||'(no symbol)')+'</a>':esc(o.symbol||'(no symbol)'))+(o.para?', para. '+esc(o.para):'');}
function buildFileChecks(){
  var f={},declared=Number(D.count);
  f.count={s:isFinite(declared)&&declared===N?'pass':'fail',name:'Record count',d:'records.length = '+fmt(N)+' · Number(count) = '+(D.count!==undefined&&isFinite(declared)?fmt(declared):'missing')};
  var pm=sumPresent(function(o){return o.mech;}),pb=sumPresent(function(o){return o.body;}),py=sumPresent(function(o){return o.year;});
  f.parts={s:(pm.sum===N&&pb.sum===N&&py.sum===N)?'pass':'fail',name:'Partitions',d:'mechanism: '+pm.groups+' groups sum to '+fmt(pm.sum)+' · body: '+pb.groups+' groups sum to '+fmt(pb.sum)+' · year: '+py.groups+' groups sum to '+fmt(py.sum)+' · each should equal '+fmt(N)};
  var pt=sumPresent(function(o){return o.type;});
  f.types={s:pt.sum===N?'pass':'fail',name:'Type partition',d:'counts per type ('+pt.groups+' values) sum to '+fmt(pt.sum)+' · headline total '+fmt(N)};
  var badLinks=recs.filter(function(o){
    var u=o.url;try{u=decodeURIComponent(u);}catch(e){}
    u=u.toLowerCase();var s=o.symbol.toLowerCase();
    return !(s&&u.indexOf('https://docs.un.org/')===0&&u.length>=s.length&&u.lastIndexOf(s)===u.length-s.length);
  });
  f.links={s:badLinks.length?'fail':'pass',name:'Links',d:fmt(N-badLinks.length)+' of '+fmt(N)+' doc_url values start with https://docs.un.org/ and end with their symbol · '+fmt(badLinks.length)+' fail',
    x:listBox('Records whose link fails',badLinks.map(function(o){return esc(o.symbol||'(no symbol)')+' → '+esc(o.url||'(no doc_url)');}))};
  var pp=MECHS.map(function(m){
    var Lm=recs.filter(function(o){return o.mech===m;}),k=Lm.filter(function(o){return o.para;}).length;
    return {m:m,k:k,n:Lm.length};
  });
  var uprRow=pp.filter(function(p){return p.m===UPR;})[0];
  var uprMiss=recs.filter(function(o){return o.mech===UPR&&!o.para;});
  f.para={s:uprMiss.length?'warn':'pass',name:'Paragraph numbers',d:pp.map(function(p){return esc(mlabel(p.m))+': '+pct(p.k,p.n)+' ('+fmt(p.k)+' of '+fmt(p.n)+')';}).join(' · ')+(uprRow?' · UPR is expected at 100%'+(uprMiss.length?', so this is a warning, not an error':''):''),
    x:listBox('UPR records without a number',uprMiss.map(function(o){return recLink(o)+' · '+snippet(o,false);}))};
  var upr=recs.filter(function(o){return o.mech===UPR;}),noState=upr.filter(function(o){return !o.states.length;});
  var odd=STATE_LIST.filter(function(s){return /\d/.test(s);});
  f.states={s:noState.length?'warn':'pass',name:'States found',d:fmt(upr.length-noState.length)+' of '+fmt(upr.length)+' UPR records have at least one State found'+(odd.length?' · '+odd.length+' extracted names contain a digit and may not be States':''),
    x:listBox('UPR records without a State (the end of the text shows what the parentheses held)',noState.map(function(o){return recLink(o)+' · '+snippet(o,true);}))+listBox('Extracted names containing a digit',odd.map(esc))};
  var ids=new Set(recs.map(function(o){return o.id;})).size,tm=cnt(),dg=0,dx=0;
  recs.forEach(function(o){tm[o.text]=(tm[o.text]||0)+1;});
  for(var k in tm){if(tm[k]>1){dg++;dx+=tm[k]-1;}}
  var nt=recs.filter(function(o){return !o.themes.length;}).length,ns=recs.filter(function(o){return !o.sdgs.length;}).length,np=recs.filter(function(o){return !o.persons.length;}).length;
  f.dups={s:ids!==N?'fail':(dg?'warn':'pass'),name:'Duplicates and gaps',d:'distinct id = '+fmt(ids)+' of '+fmt(N)+' · '+fmt(dg)+' texts occur more than once ('+fmt(dx)+' extra records) · not labelled ('+(MODE==='mine'?'with your corrections':'UN labels')+'): '+fmt(nt)+' without themes, '+fmt(ns)+' without SDGs, '+fmt(np)+' without affected persons',
    x:listBox('Records whose text occurs more than once',recs.filter(function(o){return tm[o.text]>1;}).map(function(o){return recLink(o)+' · '+snippet(o,false);}))};
  return f;
}
function chartCheck(){
  var n=FILTERED.length,bad=[],rows=document.querySelectorAll('#themeRows tr[data-count]');
  THEME_TOP.forEach(function(t,k){
    var c=0;
    for(var j=0;j<FILTERED.length;j++){if(FILTERED[j].themes.indexOf(t.name)>=0)c++;}
    var cell=rows[k]?Number(rows[k].getAttribute('data-count')):NaN;
    if(c!==LAST_BARS[k]||c!==cell)bad.push(t.name+': bar '+LAST_BARS[k]+', table '+cell+', recount '+c);
  });
  if(rows.length!==THEME_TOP.length)bad.push('table has '+rows.length+' rows, chart has '+THEME_TOP.length+' bars');
  var mx=THEME_TOP.length?THEME_TOP[0].count:0,okMax=mx<=n;
  return {s:bad.length||!okMax?'fail':'pass',name:'Chart against table',
    d:fmt(THEME_TOP.length)+' bars recounted by a second loop over '+fmt(n)+' filtered records · '+(bad.length?'disagreements below':'bars, table rows and recount agree')+' · largest bar '+fmt(mx)+(okMax?' ≤ ':' > ')+fmt(n)+' filtered records',
    x:bad.length?listBox('Disagreements',bad.map(esc)):''};
}
function corrCheck(){
  var s=corrStats(),bad=0,tu=0,tn=0;
  recs.forEach(function(o){
    var r=uniq(arr(RAW[o.i]&&RAW[o.i].themes).map(str).filter(Boolean));
    if(r.length!==o.un.length||r.some(function(t,x){return t!==o.un[x];}))bad++;
    tu+=o.un.length;tn+=o.themes.length;
  });
  var exp=tu+(MODE==='mine'?s.add-s.rem:0);
  return {s:(bad||tn!==exp)?'fail':'pass',name:'Your corrections',
    d:fmt(N-bad)+' of '+fmt(N)+' records still hold exactly the UN\'s labels from the file · labels counted in the app now: '+fmt(tn)+' = '+fmt(tu)+' UN labels'+(MODE==='mine'?' + '+fmt(s.add)+' added − '+fmt(s.rem)+' removed':' (your corrections are not applied)')+' = '+fmt(exp)};
}
function renderChecks(){
  if(!FILECHK)FILECHK=buildFileChecks();
  var f=FILECHK,list=[f.count,f.parts,f.types,chartCheck(),corrCheck(),f.links,f.para,f.states,f.dups];
  var p=list.filter(function(c){return c.s==='pass';}).length,w=list.filter(function(c){return c.s==='warn';}).length,x=list.filter(function(c){return c.s==='fail';}).length;
  $('checkSum').textContent=p+' of '+list.length+' checks pass'+(w?' · '+w+' warning'+(w>1?'s':''):'')+(x?' · '+x+' failed':'')+'. File checks cover all '+fmt(N)+' records; the chart check follows the current filter.';
  $('checks').innerHTML=list.map(function(c){
    var mark=c.s==='pass'?'✓ pass':c.s==='warn'?'warning':'check failed';
    return '<li class="chk '+c.s+'"><span class="mark">'+mark+'</span><div><strong>'+esc(c.name)+'</strong> · <span class="vals">'+c.d+'</span>'+(c.x||'')+'</div></li>';
  }).join('');
}

/* ---------- random sample ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return ((t^t>>>14)>>>0)/4294967296;};}
function pruneMarks(){Object.keys(MARK).forEach(function(i){if(!CORR[i])delete MARK[i];});}
function resetSample(){
  SAMPLE=[];pruneMarks();
  $('cards').innerHTML='';$('tally').textContent='';
  $('drawBtn').textContent='Check 10 at random';
  $('sampleHint').textContent='Ten paragraphs are drawn from the '+fmt(FILTERED.length)+' records matching the current filter, with a seeded generator (mulberry32): the same seed and filter give the same ten.';
}
function syncVerdict(k){
  var o=SAMPLE[k];if(!o)return;
  var m=MARK[o.i];
  Array.prototype.forEach.call(document.querySelectorAll('#cards [data-act="verdict"][data-k="'+k+'"]'),function(b){
    b.setAttribute('aria-pressed',b.getAttribute('data-v')===m?'true':'false');
  });
  $('vd'+k).textContent=m?{fit:'themes fit',no:'themes don\'t fit',unsure:'unsure'}[m]:'not judged';
}
function fillAdd(k){
  var o=SAMPLE[k],sel=$('add'+k);
  if(!o||!sel)return;
  var c=CORR[o.i]||{add:[]};
  sel.innerHTML='<option value="">Choose a label that occurs in the file…</option>'+ALL_THEMES.filter(function(t){return o.un.indexOf(t)<0&&c.add.indexOf(t)<0;}).map(function(t){return '<option value="'+esc(t)+'">'+esc(t)+' ('+fmt(thAll[t])+')</option>';}).join('');
}
function refreshCard(k){
  var o=SAMPLE[k];
  if(!o||!$('cl'+k))return;
  $('cl'+k).innerHTML=labelsHtml(o,true,k);
  $('ct'+k).innerHTML=CORR[o.i]?'<span class="corr">corrected by you</span>':'';
  var m=MARK[o.i];
  $('ed'+k).hidden=!(m==='no'||m==='unsure'||CORR[o.i]);
  fillAdd(k);
}
function refreshCards(){SAMPLE.forEach(function(o,k){refreshCard(k);});}
function draw(seed){
  var pool=FILTERED.slice(),rnd=mulberry32(seed>>>0),k=Math.min(10,pool.length);
  for(var i=0;i<k;i++){var j=i+Math.floor(rnd()*(pool.length-i)),t=pool[i];pool[i]=pool[j];pool[j]=t;}
  SAMPLE=pool.slice(0,k);pruneMarks();SEED=seed;
  $('seed').value=seed;
  $('drawBtn').textContent='Draw again';
  $('sampleHint').textContent='Drawn from the '+fmt(FILTERED.length)+' records matching the filter now (labels: '+(MODE==='mine'?'with your corrections':'UN labels')+'); the same seed and filter give the same ten.';
  $('cards').innerHTML=SAMPLE.map(function(o,c){
    return '<li class="card"><div class="cardline"><span class="cn">'+(c<9?'0':'')+(c+1)+'</span><span>'+recLink(o)+'</span><span id="ct'+c+'"></span>'+
      '<button type="button" class="cardbtn" data-act="card" data-k="'+c+'" aria-expanded="false">'+esc(short(firstLine(o.text),90))+'</button><span class="vd" id="vd'+c+'">not judged</span></div>'+
      '<div class="carddet" hidden><p class="full">'+esc(o.text)+'</p><p class="lab" style="margin-bottom:4px">Themes: the UN\'s own, and yours if you changed any</p><div id="cl'+c+'"></div>'+
      '<div class="actions" role="group" aria-label="Do the themes fit as a set?">'+
      '<button type="button" class="btn" aria-pressed="false" data-act="verdict" data-k="'+c+'" data-v="fit">Fits</button>'+
      '<button type="button" class="btn" aria-pressed="false" data-act="verdict" data-k="'+c+'" data-v="no">Doesn\'t fit</button>'+
      '<button type="button" class="btn" aria-pressed="false" data-act="verdict" data-k="'+c+'" data-v="unsure">Unsure</button></div>'+
      '<div class="editor" id="ed'+c+'" hidden><p class="lab">Correct the labels</p><p class="hint">× removes a label; the UN\'s own stays beside it, struck through. You can add only labels that occur in the file (in brackets: how many records the UN gave it to).</p>'+
      '<div class="addrow"><label class="lab" for="add'+c+'">Add a label</label><select id="add'+c+'"></select><button type="button" class="btn" data-act="addlab" data-k="'+c+'">Add</button></div></div></div></li>';
  }).join('');
  if(!SAMPLE.length)$('cards').innerHTML='<li class="card"><p class="empty">No records match the current filters, so nothing can be drawn.</p></li>';
  SAMPLE.forEach(function(o,c){refreshCard(c);syncVerdict(c);});
  tally();
}
function tally(){
  var f=0,d=0,u=0;
  SAMPLE.forEach(function(o){var m=MARK[o.i];if(m==='fit')f++;else if(m==='no')d++;else if(m==='unsure')u++;});
  $('tally').textContent=SAMPLE.length?'Themes: '+f+' fit, '+d+' don\'t, '+u+' unsure · '+(f+d+u)+' of '+SAMPLE.length+' judged · seed '+SEED+'. This is your judgement; the UN labels are never changed.':'';
}
function openCard(k){
  var btns=document.querySelectorAll('#cards .cardbtn');
  Array.prototype.forEach.call(btns,function(b,i){
    var on=i===k&&b.getAttribute('aria-expanded')!=='true';
    b.setAttribute('aria-expanded',on?'true':'false');
    b.parentNode.nextElementSibling.hidden=!on;
  });
}
function setVerdict(k,v){
  var o=SAMPLE[k];
  if(!o)return;
  MARK[o.i]=v;
  syncVerdict(k);refreshCard(k);tally();
}
/* ---------- method & export ---------- */
function typeCounts(L){
  var tc=cnt();
  L.forEach(function(o){var k=o.type||'(type not stated)';tc[k]=(tc[k]||0)+1;});
  return Object.keys(tc).sort(function(a,b){return tc[b]-tc[a]||ci(a,b);}).map(function(k){return fmt(tc[k])+' '+k;});
}
function summaryText(){
  var L=FILTERED,n=L.length,mm=minmax(L),docs=new Set(L.map(function(o){return o.symbol;})).size;
  var mech=MECHS.map(function(m){return mlabel(m)+' '+fmt(L.filter(function(o){return o.mech===m;}).length);}).join(', ');
  var themes=THEME_TOP.map(function(t,k){return (k+1)+'. '+t.name+' ('+fmt(t.count)+(t.y0!==null?', '+yr(t.y0,t.y1):'')+')';}).join('; ');
  return ['UN human rights recommendations and observations: '+COUNTRY+'.',
    'Source: '+(D.source||'UHRI file')+(D.built?', built '+D.built:'')+'; dates are the date of the document.',
    'Filters: '+filterText()+'.',
    'Labels: '+labelsText()+'.',
    fmt(n)+' of '+fmt(N)+' records from '+fmt(docs)+' documents, years '+yr(mm.a,mm.b)+' ('+typeCounts(L).join(', ')+').',
    'By mechanism: '+(mech||'none')+'.',
    'Ten most frequent themes among these records (a record can carry several): '+(themes||'none')+'.',
    'Counted in the browser from the file; the UN labels are used as given.'].join(' ');
}
function csvCell(v){return '"'+String(v==null?'':v).replace(/"/g,'""')+'"';}
function downloadCsv(){
  var head=['date','body','mechanism','type','symbol','paragraph','recommending_states','doc_url','text','themes','themes_un','corrected_by_you','sdgs','sdg_targets','affected_persons','section'];
  var lines=['# Country: '+COUNTRY,'# Source: '+(D.source||'')+(D.source_url?' '+D.source_url:''),'# Built: '+(D.built||''),'# Filters: '+filterText(),'# Labels: '+labelsText(),'# Rows: '+SORTED.length,head.join(',')];
  SORTED.forEach(function(o){
    lines.push([o.date,o.body,o.mech,o.type,o.symbol,o.para,o.states.join(' | '),o.url,o.text,o.themes.join(' | '),o.un.join(' | '),(CORR[o.i]?(MODE==='mine'?'yes':'yes (not applied)'):'no'),o.sdgs.join(' | '),o.targets.join(' | '),o.persons.join(' | '),o.section].map(csvCell).join(','));
  });
  var blob=new Blob(['﻿'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});
  var url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download='uhri-'+COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-filtered.csv';
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);},4000);
  $('expStatus').textContent='CSV created: '+fmt(SORTED.length)+' rows.';
}
function copyText(text,statusEl){
  function done(ok){
    statusEl.textContent=ok?'Copied':'Copy failed: select the text by hand';
    setTimeout(function(){statusEl.textContent='';},2000);
  }
  function fallback(){
    var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';
    document.body.appendChild(ta);ta.select();
    var ok=false;try{ok=document.execCommand('copy');}catch(e){}
    ta.remove();done(ok);
  }
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(function(){done(true);},fallback);}
  else fallback();
}
function renderMethod(){
  $('expInfo').textContent='The export holds '+fmt(FILTERED.length)+' rows. Filters applied: '+filterText()+'. Labels: '+labelsText()+'.';
}

/* ---------- corrections: the UN's labels are kept, yours sit beside them ---------- */
function viewThemes(o){
  var c=CORR[o.i];
  if(!c)return o.un.slice();
  var out=o.un.filter(function(t){return c.rem.indexOf(t)<0;});
  c.add.forEach(function(t){if(out.indexOf(t)<0)out.push(t);});
  return out;
}
function applyLabels(){
  recs.forEach(function(o){o.themes=MODE==='mine'?viewThemes(o):o.un.slice();});
}
function corrStats(){
  var s={add:0,rem:0,recs:0,labels:0};
  Object.keys(CORR).forEach(function(k){s.recs++;s.add+=CORR[k].add.length;s.rem+=CORR[k].rem.length;});
  s.labels=s.add+s.rem;
  return s;
}
function plural(n,one,many){return fmt(n)+' '+(n===1?one:many);}
function labelsText(){
  var s=corrStats();
  if(MODE==='mine')return 'with your corrections ('+plural(s.labels,'label','labels')+' corrected on '+plural(s.recs,'record','records')+'; the UN\'s own labels are kept)';
  return 'the UN\'s own'+(s.recs?' ('+plural(s.labels,'correction','corrections')+' by you exist but are not applied)':'');
}
function corrOp(o,op,l){
  var c=CORR[o.i]||(CORR[o.i]={rem:[],add:[]});
  if(op==='rem'){if(o.un.indexOf(l)>=0&&c.rem.indexOf(l)<0)c.rem.push(l);}
  else if(op==='restore'){c.rem=c.rem.filter(function(x){return x!==l;});}
  else if(op==='add'){if(o.un.indexOf(l)<0&&(l in thAll)&&c.add.indexOf(l)<0)c.add.push(l);}
  else if(op==='drop'){c.add=c.add.filter(function(x){return x!==l;});}
  if(!c.rem.length&&!c.add.length)delete CORR[o.i];
}
function say(m){$('corrStatus').textContent=m;}
function labelsHtml(o,edit,k){
  var c=CORR[o.i]||{rem:[],add:[]},out=[];
  function btn(op,l,txt,lab){
    return edit?'<button type="button" class="tagx" data-act="corr" data-op="'+op+'" data-i="'+o.i+'" data-k="'+k+'" data-l="'+esc(l)+'" aria-label="'+esc(lab+': '+l)+'">'+txt+'</button>':'';
  }
  o.un.forEach(function(t){
    if(c.rem.indexOf(t)<0)out.push('<span class="tag">'+esc(t)+btn('rem',t,'×','Remove the label')+'</span>');
  });
  o.un.forEach(function(t){
    if(c.rem.indexOf(t)>=0)out.push('<span class="tag gone"><s>'+esc(t)+'</s><span class="sr"> (UN label, removed by you)</span>'+btn('restore',t,'undo','Put back the UN label')+'</span>');
  });
  c.add.forEach(function(t){
    out.push('<span class="tag mine"><span aria-hidden="true">+ </span>'+esc(t)+'<span class="sr"> (added by you)</span>'+btn('drop',t,'undo','Undo adding the label')+'</span>');
  });
  return out.length?out.join(''):'<span class="mute">not labelled</span>';
}
function corrTag(o){
  if(!CORR[o.i])return '';
  return MODE==='mine'?'<span class="corr">corrected by you</span>':'<span class="corr hid" title="Switch to “with my corrections” to see it">corrected by you · hidden</span>';
}
function renderCorrBar(){
  var s=corrStats(),on=MODE==='mine';
  $('corrLine').textContent=plural(s.labels,'label','labels')+' corrected by you; the UN\'s own labels are kept';
  $('corrSub').textContent=s.recs?'on '+plural(s.recs,'record','records')+' · '+fmt(s.add)+' added, '+fmt(s.rem)+' removed · '+(on?'every count, chart and filter uses your labels':'hidden: every count uses the UN labels'):'mark a set Doesn\'t fit or Unsure on 03 Check to correct its labels';
  $('modeSw').setAttribute('aria-checked',on?'true':'false');
  $('swUn').className='sl'+(on?'':' on');
  $('swMe').className='sl'+(on?' on':'');
}
function undoBtn(op,o,t,what){
  return '<button type="button" class="linkbtn" data-act="corr" data-op="'+op+'" data-i="'+o.i+'" data-l="'+esc(t)+'" aria-label="'+esc('Undo '+what+' “'+t+'” ('+citation(o)+')')+'">Undo</button>';
}
function renderCorrList(){
  var s=corrStats(),items=[];
  recs.forEach(function(o){
    var c=CORR[o.i];
    if(!c)return;
    var who=recLink(o);
    c.rem.forEach(function(t){items.push('<li>'+who+' · removed <s>'+esc(t)+'</s> '+undoBtn('restore',o,t,'removing')+'</li>');});
    c.add.forEach(function(t){items.push('<li>'+who+' · added <span class="mineword">'+esc(t)+'</span> '+undoBtn('drop',o,t,'adding')+'</li>');});
  });
  $('corrSum').textContent='List and undo my corrections ('+fmt(s.labels)+')';
  $('corrList').innerHTML=items.length?items.join(''):'<li class="mute">No corrections yet.</li>';
}
function downloadCorr(){
  var L=recs.filter(function(o){return CORR[o.i];});
  if(!L.length){say('Nothing to download yet: you have not corrected any label.');return;}
  var head=['symbol','paragraph','un_labels','my_labels','my_mark','record_id'];
  var lines=['# Label corrections by you: '+COUNTRY,'# Source: '+(D.source||'')+(D.source_url?' '+D.source_url:''),'# Built: '+(D.built||''),'# Rows: '+L.length+' records, '+plural(corrStats().labels,'label','labels')+' corrected; un_labels are the UN\'s own and are kept','# Load this file again with Load corrections (CSV) on 03 Check',head.join(',')];
  L.forEach(function(o){
    lines.push([o.symbol,o.para,o.un.join(' | '),viewThemes(o).join(' | '),MARKS[MARK[o.i]]||'',o.id].map(csvCell).join(','));
  });
  var blob=new Blob(['﻿'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});
  var url=URL.createObjectURL(blob),a=document.createElement('a');
  a.href=url;a.download='uhri-'+COUNTRY.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-my-label-corrections.csv';
  document.body.appendChild(a);a.click();a.remove();
  setTimeout(function(){URL.revokeObjectURL(url);},4000);
  say('CSV created: '+plural(L.length,'record','records')+' with corrections.');
}
function parseCsv(t){
  t=t.replace(/^﻿/,'');
  var rows=[],row=[],cell='',q=false,start=true,k,ch;
  for(k=0;k<t.length;k++){
    ch=t.charAt(k);
    if(q){
      if(ch==='"'){if(t.charAt(k+1)==='"'){cell+='"';k++;}else q=false;}
      else cell+=ch;
    }else{
      if(start&&ch==='#'){while(k<t.length&&t.charAt(k)!=='\n')k++;continue;}
      start=false;
      if(ch==='"')q=true;
      else if(ch===','){row.push(cell);cell='';}
      else if(ch==='\n'||ch==='\r'){
        if(ch==='\r'&&t.charAt(k+1)==='\n')k++;
        row.push(cell);cell='';
        if(row.length>1||row[0]!=='')rows.push(row);
        row=[];start=true;
      }else cell+=ch;
    }
  }
  if(cell!==''||row.length){row.push(cell);rows.push(row);}
  return rows;
}
function parseMark(s){
  s=String(s||'').trim().toLowerCase().replace(/’/g,"'");
  if(s==='fits'||s==='fit')return 'fit';
  if(s==="doesn't fit"||s==='no')return 'no';
  if(s==='unsure')return 'unsure';
  return '';
}
function loadCorr(text,fname){
  var rows=parseCsv(text),miss=[];
  $('corrMiss').innerHTML='';
  if(rows.length<2){say('Nothing to load: '+fname+' has no data rows.');return;}
  var h=rows[0].map(function(x){return x.trim().toLowerCase();});
  var iS=h.indexOf('symbol'),iP=h.indexOf('paragraph'),iU=h.indexOf('un_labels'),iM=h.indexOf('my_labels'),iK=h.indexOf('my_mark'),iD=h.indexOf('record_id');
  if(iS<0||iU<0||iM<0){say('This does not look like a corrections file from this app: it needs the columns symbol, paragraph, un_labels, my_labels and my_mark.');return;}
  var byId=cnt(),bySP=cnt(),claimed={},ok=0,replaced=0,total=rows.length-1;
  recs.forEach(function(o){
    if(o.id)byId[o.id]=o;
    var key=o.symbol.trim()+'\u0001'+o.para;
    (bySP[key]||(bySP[key]=[])).push(o);
  });
  function cell(r,i){return i>=0&&i<r.length?r[i]:'';}
  function labs(x){return x.split('|').map(function(y){return y.trim();}).filter(Boolean);}
  function same(a,b){a=a.slice().sort();b=b.slice().sort();return a.length===b.length&&a.every(function(x,k){return x===b[k];});}
  rows.slice(1).forEach(function(r){
    var sym=cell(r,iS).trim(),para=cell(r,iP).trim(),id=cell(r,iD).trim(),un=labs(cell(r,iU)),mine=labs(cell(r,iM)),mark=parseMark(cell(r,iK));
    var what=esc(sym||'(no symbol)')+(para?', para. '+esc(para):'');
    var o=null,cand=bySP[sym+'\u0001'+para]||[];
    if(id&&byId[id]&&byId[id].symbol.trim()===sym&&!claimed[byId[id].i])o=byId[id];
    else o=cand.filter(function(x){return !claimed[x.i]&&same(x.un,un);})[0]||null;
    if(!o){miss.push(what+' · '+(cand.length||(id&&byId[id])?'the UN labels in this file differ from the CSV, or this record is already restored':'no such record in this file'));return;}
    if(!same(o.un,un)){miss.push(what+' · the UN labels in this file differ from the CSV');return;}
    var unknown=mine.filter(function(t){return o.un.indexOf(t)<0&&!(t in thAll);});
    if(unknown.length){miss.push(what+' · label not found in the file: '+esc(unknown.join(', ')));return;}
    claimed[o.i]=1;
    var rem=o.un.filter(function(t){return mine.indexOf(t)<0;}),add=uniq(mine.filter(function(t){return o.un.indexOf(t)<0;}));
    if(CORR[o.i])replaced++;
    if(rem.length||add.length)CORR[o.i]={rem:rem,add:add};else delete CORR[o.i];
    if(mark)MARK[o.i]=mark;
    ok++;
  });
  $('corrMiss').innerHTML=listBox('Rows not restored',miss);
  if(ok){MODE='mine';}
  say((ok?'Restored '+ok+' of '+total+' rows from '+fname+(replaced?' ('+replaced+' replaced a correction you had made here)':'')+(miss.length?'; '+miss.length+' could not be matched, listed below':'')+'. Counts, charts and filters now use your labels.':'Nothing restored: none of the '+total+' rows matched a record in this file (listed below).'));
  update(true);
}

/* ---------- update everything ---------- */
function update(keep){
  setWords();applyLabels();
  if(keep)FILECHK=null;
  FILTERED=recs.filter(function(o){return matches(o);});
  SORTED=sortRecs(FILTERED);
  if(!keep)shown=PAGE;
  renderRail();renderOverview();renderRecords();renderChecks();renderMethod();renderCorrBar();renderCorrList();
  if(keep)refreshCards();else resetSample();
  if(active==='ov')drawCharts();
}

/* ---------- clicks ---------- */
document.addEventListener('click',function(e){
  var t=e.target;
  var tr=t.closest('tr.rowx');
  if(tr&&!t.closest('a')){toggleRow(tr);return;}
  var a=t.closest('[data-act]');
  if(!a)return;
  var act=a.getAttribute('data-act'),k=Number(a.getAttribute('data-k'));
  if(act==='acc'){openAcc=openAcc===a.getAttribute('data-k')?'':a.getAttribute('data-k');syncAcc();}
  else if(act==='clear'){S={kw:'',mech:'',body:'',type:'',state:'',from:'',to:'',sdg:'',themes:[]};syncKw();update();}
  else if(act==='chip'){if(CHIPFN[k]){CHIPFN[k].f();update();}}
  else if(act==='states'){statesOpen=!statesOpen;renderOverview();}
  else if(act==='theme'){if(THEME_TOP[k])addTheme(THEME_TOP[k].name);}
  else if(act==='goto'){selectTab(a.getAttribute('data-t'),true);}
  else if(act==='sortdate'){dateAsc=!dateAsc;SORTED=sortRecs(FILTERED);renderRecords();}
  else if(act==='more'){shown+=PAGE;renderRecords();}
  else if(act==='copycite'){var o=recs[Number(a.getAttribute('data-i'))];copyText(citation(o),a.nextElementSibling);}
  else if(act==='copysum'){copyText(summaryText(),$('expStatus'));}
  else if(act==='csv'){downloadCsv();}
  else if(act==='draw'){draw(Math.floor(Math.random()*999999)+1);}
  else if(act==='seeddraw'){var s=parseInt($('seed').value,10);draw(isFinite(s)&&s>=0?s:1);}
  else if(act==='card'){openCard(k);}
  else if(act==='verdict'){setVerdict(k,a.getAttribute('data-v'));}
  else if(act==='mode'){MODE=MODE==='mine'?'un':'mine';update(true);}
  else if(act==='addlab'){
    var oa=SAMPLE[k],sel=$('add'+k);
    if(!oa||!sel)return;
    if(!sel.value){say('Choose a label from the list first.');sel.focus();return;}
    var lbl=sel.value;
    corrOp(oa,'add',lbl);MODE='mine';
    say('Added “'+lbl+'” to '+citation(oa)+', marked as yours. Counts, charts and filters now use your labels.');
    update(true);
    if($('add'+k))$('add'+k).focus();
  }
  else if(act==='corr'){
    var oc=recs[Number(a.getAttribute('data-i'))],op=a.getAttribute('data-op'),lb=a.getAttribute('data-l'),inCard=a.hasAttribute('data-k'),pos=-1;
    if(!oc)return;
    if(!inCard)pos=Array.prototype.indexOf.call(document.querySelectorAll('#corrList [data-act="corr"]'),a);
    corrOp(oc,op,lb);
    if(inCard)MODE='mine';
    say({rem:'Removed “'+lb+'” from ',restore:'Put back the UN label “'+lb+'” on ',add:'Added “'+lb+'” to ',drop:'Undid adding “'+lb+'” to '}[op]+citation(oc)+(op==='rem'?': the UN label is kept, struck through.':'.')+(inCard?' Counts, charts and filters now use your labels.':''));
    update(true);
    if(inCard){if($('add'+k))$('add'+k).focus();}
    else{var bs=document.querySelectorAll('#corrList [data-act="corr"]');(bs[Math.min(pos,bs.length-1)]||$('corrSum')).focus();}
  }
  else if(act==='corrdl'){downloadCorr();}
  else if(act==='corrload'){$('corrFile').click();}
});

$('corrFile').addEventListener('change',function(e){
  var f=e.target.files&&e.target.files[0];
  if(!f)return;
  var rd=new FileReader();
  rd.onload=function(){loadCorr(String(rd.result||''),f.name);};
  rd.onerror=function(){say('The file could not be read.');};
  rd.readAsText(f);
  e.target.value='';
});

/* ---------- start ---------- */
initStatic();
buildTabs();
syncAcc();
if(window.Chart){try{Chart.defaults.animation=false;}catch(e){}}
update();
})();
</script>
</body>
</html>
```
