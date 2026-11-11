I'll build the Verbatim finder as one HTML page: a Boolean search over the General Comment paragraphs, a citation and quotation builder, a draft collector, and a self-check tab.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verbatim finder: General Comments and General Recommendations</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--green:#2d6a3e;--amber:#8a5300;--grey:#5f5a50}
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
.kicker{font:11px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--grey)}
.hint{font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;color:var(--grey);margin:6px 0}
.grey{color:var(--grey);font-size:14px}
.mast{max-width:1280px;margin:0 auto;padding:22px 28px 0}
h1{font:600 28px/1.2 Georgia,"Times New Roman",serif;margin:.2em 0 .3em}
.line{margin:0 0 12px;font-size:15px}
.status{margin-left:14px;white-space:nowrap}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}
.dot.ok{background:var(--green)}.dot.bad{background:var(--red)}
.layout{display:grid;grid-template-columns:300px 1fr;gap:28px;max-width:1280px;margin:0 auto;padding:18px 28px}
.layout.norail{grid-template-columns:1fr}
aside{border-right:1px solid var(--rule);padding-right:20px;min-width:0}
main{min-width:0}
.railhead{display:flex;justify-content:space-between;align-items:center}
.big{font:500 48px/1.05 Georgia,"Times New Roman",serif;margin-top:8px}
.bigsub{font-size:14px;color:var(--grey);margin-bottom:12px}
button{font:inherit;color:var(--ink);background:none;border:1px solid var(--rule);padding:5px 10px;cursor:pointer;border-radius:0}
button:hover{border-color:var(--ink)}
button.primary{border-color:var(--red);color:var(--red)}
button.link{border:0;padding:0;color:var(--red);text-decoration:underline;font-size:inherit}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
input[type=search],input[type=number],select,textarea{font:inherit;color:var(--ink);background:#fffdf8;border:1px solid #b9b0a0;padding:6px 8px;border-radius:0;max-width:100%}
input[type=number]{width:96px}
.srow{display:flex;gap:6px;margin-bottom:4px}
.srow input{flex:1;min-width:0}
form#qform{position:relative}
#examples{border:1px solid var(--rule);background:#fbf9f4;padding:10px 12px;margin:6px 0}
.syn{margin:4px 0 10px;padding-left:18px;font-size:14px}
.exlist{list-style:none;padding:0;margin:4px 0}
.exlist li{margin:4px 0}
.exlist button{font:14px ui-monospace,Menlo,Consolas,monospace;text-align:left;width:100%}
.echo{font-size:15px;margin:10px 0 4px}
.fail{color:var(--red)}.pass{color:var(--green)}.note{color:var(--amber)}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.chip{font:12px ui-monospace,Menlo,Consolas,monospace;border-color:var(--red);color:var(--red);padding:2px 8px}
.fh{font:inherit;margin:16px 0 6px}
.fh button{width:100%;text-align:left;font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;border:0;border-top:1px solid var(--rule);padding:10px 0}
.fh button[aria-expanded=true]{color:var(--red)}
#fpanel{padding:4px 0 8px}
.cfs{border:0;padding:0;margin:0 0 10px}
.crow{display:flex;gap:6px;align-items:center;font-size:14px;padding:2px 0}
.cnt{font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--grey);margin-left:auto}
.yrs{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:8px 0}
.docl{display:block;font-size:14px}
.docl select{width:100%;margin-top:4px}
.tabs{display:flex;gap:2px;border-bottom:1px solid var(--rule);flex-wrap:wrap}
.tabs button{border:0;border-bottom:3px solid transparent;font:11px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;padding:10px 12px}
.tabs button[aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
.msg{font:13px ui-monospace,Menlo,Consolas,monospace;color:var(--green);min-height:1.4em;word-break:break-word}
#fallback textarea{width:100%;height:90px;font-size:14px}
.fig{font:500 22px Georgia,"Times New Roman",serif;margin:18px 0 2px}
.cwrap{position:relative;margin:8px 0 14px}
.answer{font:500 26px Georgia,"Times New Roman",serif;margin:14px 0 4px}
table{border-collapse:collapse;width:100%;margin:10px 0}
caption{text-align:left;font:11px ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.08em;color:var(--grey);padding-bottom:4px}
th,td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;font-size:15px}
th{font-weight:600}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.how{font-size:13px;color:var(--grey);border-top:1px solid var(--rule);padding-top:8px}
.sumline{font-size:17px;margin:10px 0 2px}
.sortrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:8px 0}
.row{border-top:1px solid var(--rule);padding:14px 0}
.row h3{font:600 18px/1.3 Georgia,"Times New Roman",serif;margin:6px 0}
.row h3 button{border:0;padding:0;text-align:left;font:inherit;color:var(--ink)}
.row h3 button[aria-expanded=true]{color:var(--red)}
.meta{font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--grey);margin:0}
.badge{font:11px ui-monospace,Menlo,Consolas,monospace;border:1px solid var(--ink);padding:0 4px;margin-right:4px;color:var(--ink)}
.pin{color:var(--red);font-weight:600}
.ptxt{white-space:pre-wrap;margin:8px 0;font-size:16px;line-height:1.55}
mark{background:#fff1a8;color:var(--ink);font-weight:700;padding:0 1px}
.notes{font-size:13px;color:var(--amber);margin:4px 0}
.notes div::before{content:"\25B2  ";}
.actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:10px 0}
.ctxbox{border-left:2px solid var(--rule);padding-left:10px;margin:6px 0}
.cite{font:14px ui-monospace,Menlo,Consolas,monospace}
.qt{margin:6px 0;padding-left:12px;border-left:3px solid var(--red);font-size:16px}
.sec{font:500 20px Georgia,"Times New Roman",serif;margin:22px 0 6px}
.chk{margin:6px 0;font-size:15px}
.method p,.method li{font-size:15px}
footer.foot{max-width:1280px;margin:0 auto;padding:14px 28px 26px;border-top:1px solid var(--rule);font:11px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--grey)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media (max-width:820px){.layout{grid-template-columns:1fr}aside{border:0;padding:0}}
</style>
</head>
<body>
<header class="mast">
  <div class="kicker">UN TREATY BODIES · GENERAL COMMENTS</div>
  <h1>Verbatim finder: General Comments and General Recommendations</h1>
  <p class="line"><span id="hline"></span><span class="status"><span class="dot" id="hdot"></span><span id="hdotTxt"></span></span></p>
</header>

<div class="layout" id="layout">
<aside id="rail">
  <div class="railhead"><span class="kicker">Filters</span><button type="button" id="clearAll">Clear all</button></div>
  <div class="big"><span id="bigN">0</span></div>
  <div class="bigsub">matching paragraphs · <span id="ofN"></span></div>
  <form id="qform" role="search">
    <label for="q" class="kicker">Search the text</label>
    <div class="srow"><input id="q" type="search" autocomplete="off" spellcheck="false"><button class="primary" type="submit">Search</button></div>
    <div id="examples" hidden>
      <p class="kicker">Syntax</p>
      <ul class="syn">
        <li>a space or AND joins words</li>
        <li>OR finds either word</li>
        <li>NOT or a leading minus leaves a word out</li>
        <li>"an exact phrase" in double quotes</li>
        <li>parentheses group terms</li>
        <li>a star at the end of a word matches any ending: child* finds children</li>
        <li>operators in capitals; lower-case "or" is a word</li>
      </ul>
      <p class="kicker">Examples (choose one to run it)</p>
      <ul class="exlist" id="exlist"></ul>
    </div>
  </form>
  <p class="hint" id="qhelp">Whole words, any case. Curly and straight quotes, apostrophes, dashes and hyphens count as the same, and footnote marks are skipped, so State's finds State’s and a phrase can cross a footnote.</p>
  <p class="echo" id="echo" aria-live="polite"></p>
  <p class="fail" id="qerr" aria-live="polite"></p>
  <div class="chips" id="chips"></div>
  <h2 class="fh"><button type="button" id="fbtn" aria-expanded="false" aria-controls="fpanel">01 Committee, years, document</button></h2>
  <div id="fpanel" hidden>
    <fieldset class="cfs">
      <legend class="kicker">Committee</legend>
      <p><button type="button" id="allC">all</button> <button type="button" id="noneC">none</button></p>
      <div id="cbox"></div>
    </fieldset>
    <div class="yrs"><label>From <input id="yFrom" type="number"></label><label>to <input id="yTo" type="number"></label></div>
    <label class="docl">Document <select id="doc"></select></label>
  </div>
</aside>

<main>
  <div class="tabs" role="tablist" aria-label="Sections">
    <button role="tab" id="t0" aria-controls="p0" aria-selected="true" tabindex="0">01 Overview</button>
    <button role="tab" id="t1" aria-controls="p1" aria-selected="false" tabindex="-1">02 Paragraphs</button>
    <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">03 Draft</button>
    <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">04 Check &amp; method</button>
  </div>
  <p class="msg" id="msg" aria-live="polite"></p>
  <div id="fallback" hidden><p class="hint">The browser refused the copy. Select and copy:</p><textarea readonly id="fbx"></textarea></div>

  <section role="tabpanel" id="p0" aria-labelledby="t0">
    <p class="answer" id="answer"></p>
    <h2 class="fig">FIG.01 Paragraphs per committee</h2>
    <p class="hint">click a bar = tick that committee alone</p>
    <div class="cwrap" id="cwrap"><canvas id="chart" role="img" aria-label="Paragraphs per committee"></canvas></div>
    <table>
      <caption>Paragraphs per committee</caption>
      <thead><tr><th scope="col">Committee</th><th scope="col">Name</th><th scope="col" class="n">Paragraphs</th></tr></thead>
      <tbody id="ctbody"></tbody>
    </table>
    <p class="how">How this is computed: one count per committee over the paragraphs that match the query and filters. Joint General Comments count under both committees, so the bars can add up to more than the hits.</p>
  </section>

  <section role="tabpanel" id="p1" aria-labelledby="t1" hidden>
    <p class="sumline" id="sum" aria-live="polite"></p>
    <div class="sortrow">
      <label>Order <select id="sort">
        <option value="year">document order, newest first</option>
        <option value="matches">most matches first</option>
      </select></label>
      <span class="hint" id="sortnote"></span>
    </div>
    <p class="hint">This page retrieves; it never writes. Every paragraph shown is a record of the file, as stored.</p>
    <div id="list"></div>
    <p><button type="button" id="more">Show 25 more</button></p>
  </section>

  <section role="tabpanel" id="p2" aria-labelledby="t2" hidden>
    <h2 class="sec">Your draft (<span id="dn">0</span> quotations)</h2>
    <p class="hint" id="dwhere"></p>
    <p><button type="button" id="copyAll">Copy all</button> <button type="button" id="dtxt">Download .txt</button> <button type="button" id="dcsv">Download .csv</button></p>
    <div id="dlist"></div>
  </section>

  <section role="tabpanel" id="p3" aria-labelledby="t3" hidden>
    <h2 class="sec">How the app checks itself</h2>
    <div id="checks"></div>
    <h2 class="sec">Known quirks of this file</h2>
    <div id="quirks"></div>
    <h2 class="sec">How this is computed</h2>
    <div class="method">
      <p>The query is read as typed. Curly quotes, straight quotes and dashes are made one form, and the text is compared the same way, so a phrase pasted from Word still matches.</p>
      <p>A word matches whole words only, in any case; child* also matches children. A phrase must appear with its words in order. NOT removes paragraphs; a query that only excludes words matches every paragraph that lacks them.</p>
      <p>Each paragraph is shown as stored, minus its footnote marks (the marks are counted and can be shown back). Copies are built only from the file's fields: the symbol, the paragraph number, the committee and the document's own title. No symbol or number is invented; a leading number that differs from the record's paragraph is never corrected.</p>
      <p>Citation: symbol and pinpoint (para. N, preamble, or subpara. (b)). Where one symbol covers several General Comments, the committee and the document's number come first, for example CERD, General Recommendation No. 29 (A/57/18), para. 3. The style is UN short form.</p>
      <p>Counting, matching and sorting are done by this page's code; no model is called and nothing leaves the browser.</p>
    </div>
  </section>
</main>
</div>
<footer class="foot" id="foot"></footer>

<script>
'use strict';
const GC = window.WORKSHOP_DATA.gc;
const R = GC.records;
const COMMITTEES = {
  CAT:'Committee against Torture', 'CAT-OP':'Subcommittee on Prevention of Torture',
  CCPR:'Human Rights Committee', CED:'Committee on Enforced Disappearances',
  CEDAW:'Committee on the Elimination of Discrimination against Women',
  CERD:'Committee on the Elimination of Racial Discrimination',
  CESCR:'Committee on Economic, Social and Cultural Rights', CMW:'Committee on Migrant Workers',
  CRC:'Committee on the Rights of the Child', CRPD:'Committee on the Rights of Persons with Disabilities'
};
const CODES = Object.keys(COMMITTEES);
const FNRE = /\[\[fn:\d+\]\]/g;
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
const fmt = n => Number(n).toLocaleString('en-GB');
const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const shownOf = t => t.replace(FNRE, '');
function normalise(s){
  return s.replace(/[\u201C\u201D\u201E]/g,'"').replace(/[\u2018\u2019\u201A]/g,"'")
          .replace(/[\u2013\u2014\u00AD]/g,'-').replace(/\s+/g,' ').toLowerCase();
}
function codesOf(sym, committee){
  const out = new Set();
  const s = sym.replace(/CAT\/OP/g, () => { out.add('CAT-OP'); return ''; });
  const re = /\b(CAT|CCPR|CED|CEDAW|CERD|CESCR|CMW|CRC|CRPD)\b/g; let m;
  while ((m = re.exec(s))) out.add(m[1]);
  if (committee) out.add(committee);
  return [...out].filter(c => COMMITTEES[c]);
}

/* ---------- load: one record per paragraph ---------- */
const titlesBySym = new Map();
for (const r of R){
  if (!titlesBySym.has(r.symbol)) titlesBySym.set(r.symbol, new Set());
  titlesBySym.get(r.symbol).add(r.title);
}
const byTP = new Map();
const tpKey = (t, p) => t + '\u0001' + p;
const D = R.map((r, i) => {
  const shown = shownOf(r.text);
  const lead = shown.match(/^(\d{1,3})\.\s/);
  const letter = shown.match(/^\(([a-z]{1,4})\)/);
  const d = {
    i, id: r.id, r, title: r.title, symbol: r.symbol, committee: r.committee,
    paragraph: r.paragraph, year: r.year, short_title: r.short_title, doc_url: r.doc_url,
    shown, marks: (r.text.match(FNRE) || []).length, norm: normalise(shown),
    leading: lead ? parseInt(lead[1], 10) : null,
    letter: letter ? letter[1] : null,
    joint: /[\u2013,]/.test(r.symbol),
    shared: titlesBySym.get(r.symbol).size > 1,
    codes: codesOf(r.symbol, r.committee)
  };
  const cut = r.title.search(/:| on /);
  d.docName = cut > 0 ? r.title.slice(0, cut) : r.title;
  d.pin = r.paragraph === 0 ? 'preamble' : d.letter ? `subpara. (${d.letter})` : `para. ${r.paragraph}`;
  d.cite = d.shared ? `${r.committee}, ${d.docName} (${r.symbol}), ${d.pin}` : `${r.symbol}, ${d.pin}`;
  d.copied = (d.leading !== null && d.leading === r.paragraph) ? shown.replace(/^\d{1,3}\.\s+/, '') : shown;
  const k = tpKey(r.title, r.paragraph);
  if (!byTP.has(k)) byTP.set(k, []);
  byTP.get(k).push(d);
  return d;
});
const DBID = new Map(D.map(d => [d.id, d]));
const dupCount = d => byTP.get(tpKey(d.title, d.paragraph)).length;
const TITLES = new Set(R.map(r => r.title)).size;
const COMS = new Set(R.map(r => r.committee)).size;
const YMIN = Math.min(...R.map(r => r.year)), YMAX = Math.max(...R.map(r => r.year));
const SRC_URL = /^https?:/.test(GC.source || '') ? GC.source : (GC.source_url || '');

const QUIRKS = (() => {
  const q = [];
  const p0 = D.filter(d => d.paragraph === 0);
  if (p0.length) q.push({t:`${p0.length} records have paragraph 0: preambles of early General Recommendations, cited as "preamble".`, e:`e.g. ${p0[0].symbol}, ${p0[0].docName}`});
  const sh = [...titlesBySym.entries()].filter(([s, t]) => t.size > 1);
  if (sh.length) q.push({t:`${sh.length} symbols hold more than one General Comment; their citations carry the committee and the document's number.`, e:`e.g. ${sh[0][0]} holds ${sh[0][1].size}`});
  const jt = D.filter(d => d.joint);
  if (jt.length) q.push({t:`${jt.length} records are joint General Comments carrying two symbols in one field.`, e:`e.g. ${jt[0].symbol}`});
  const dupKeys = [...byTP.entries()].filter(([k, v]) => v.length > 1);
  if (dupKeys.length) q.push({t:`${dupKeys.length} pinpoints occur in more than one record of the same document.`, e:`e.g. ${dupKeys[0][1][0].symbol}, ${dupKeys[0][1][0].pin}`});
  const mm = D.filter(d => d.leading !== null && d.leading !== d.paragraph);
  if (mm.length) q.push({t:`${mm.length} texts begin with a number that differs from the record's paragraph; both numbers are shown, nothing is corrected.`, e:`e.g. text begins ${mm[0].leading}., record is para. ${mm[0].paragraph} (${mm[0].symbol})`});
  const lt = D.filter(d => d.letter);
  if (lt.length) q.push({t:`${lt.length} records are lettered sub-paragraphs, numbered by the file; verify them in the document.`, e:`e.g. ${lt[0].symbol}, ${lt[0].pin}`});
  const fnw = D.filter(d => /\p{L}\[\[fn:\d+\]\]\p{L}/u.test(d.r.text));
  if (fnw.length) q.push({t:`${fnw.length} records have a footnote mark between two letters of a word; the mark is removed and the word is joined.`, e:`e.g. ${fnw[0].symbol}`});
  return q;
})();

/* ---------- query: lex, parse, compile ---------- */
function lex(src){
  const s = src.replace(/[\u201C\u201D\u201E]/g,'"').replace(/[\u2018\u2019\u201A]/g,"'").replace(/[\u2013\u2014\u00AD]/g,'-');
  const toks = []; let i = 0;
  while (i < s.length){
    const c = s[i];
    if (/\s/.test(c)) { i++; continue; }
    if (c === '(' || c === ')') { toks.push({t:c}); i++; continue; }
    if (c === '"'){
      const j = s.indexOf('"', i + 1);
      if (j < 0) throw new Error('A quotation mark is not closed.');
      const v = s.slice(i + 1, j).trim();
      if (!v) throw new Error('An empty phrase.');
      toks.push({t:'phrase', v}); i = j + 1; continue;
    }
    let j = i; while (j < s.length && !/[\s()"]/.test(s[j])) j++;
    let w = s.slice(i, j); i = j;
    if (w === 'AND' || w === 'OR' || w === 'NOT'){ toks.push({t:w}); continue; }
    if (w.length > 1 && w[0] === '-'){ toks.push({t:'NOT'}); w = w.slice(1); }
    else if (w === '-') throw new Error('A minus sign needs a word after it.');
    toks.push({t:'word', v:w});
  }
  return toks;
}
function wordSrc(w, mode){
  const star = w.endsWith('*');
  const base = (star ? w.slice(0, -1) : w).toLowerCase();
  if (!base) throw new Error('A star needs a word before it.');
  let s = '';
  if (mode === 'norm') s = escRe(base);
  else for (const ch of base){
    if (ch === "'") s += "['\u2019\u2018]";
    else if (ch === '"') s += '["\u201C\u201D]';
    else if (ch === '-') s += '[-\u2013\u2014\u00AD]';
    else s += escRe(ch);
  }
  return s + (star ? '[\\p{L}\\p{N}_]*' : '');
}
function makeTerm(tok){
  const words = tok.t === 'phrase' ? tok.v.split(/\s+/).filter(Boolean) : [tok.v];
  const bnd = core => `(?<![\\p{L}\\p{N}])${core}(?![\\p{L}\\p{N}])`;
  const normCore = words.map(w => wordSrc(w, 'norm')).join('\\s+');
  const hlCore = words.map(w => wordSrc(w, 'hl')).join('(?:\\s|\\[\\[fn:\\d+\\]\\])+');
  return { op:'term', phrase: tok.t === 'phrase', label: tok.v,
           norm: bnd(normCore), hl: bnd(hlCore), re: new RegExp(bnd(normCore), 'u') };
}
function parseQuery(src){
  const toks = lex(src);
  if (!toks.length) return null;
  let p = 0;
  const peek = () => toks[p];
  const fail = m => { throw new Error(m); };
  const startsTerm = t => t && ['word','phrase','(','NOT'].includes(t.t);
  function primary(){
    const t = peek();
    if (!t) fail('The search ends where a word was expected.');
    if (t.t === '('){
      p++;
      if (peek() && peek().t === ')') fail('Empty parentheses.');
      const e = orE();
      if (!peek() || peek().t !== ')') fail('A parenthesis is not closed.');
      p++; return e;
    }
    if (t.t === 'word' || t.t === 'phrase'){ p++; return makeTerm(t); }
    fail(`Unexpected ${t.t === ')' ? 'closing parenthesis' : t.t}.`);
  }
  function unary(){
    if (peek() && peek().t === 'NOT'){
      p++;
      if (!peek()) fail('NOT needs a word after it.');
      return { op:'not', k: unary() };
    }
    return primary();
  }
  function andE(){
    const ks = [unary()];
    for (;;){
      const t = peek();
      if (t && t.t === 'AND'){ p++; if (!peek()) fail('AND needs a word after it.'); ks.push(unary()); }
      else if (startsTerm(t)) ks.push(unary());
      else break;
    }
    return ks.length > 1 ? { op:'and', k: ks } : ks[0];
  }
  function orE(){
    const ks = [andE()];
    while (peek() && peek().t === 'OR'){ p++; if (!peek()) fail('OR needs a word after it.'); ks.push(andE()); }
    return ks.length > 1 ? { op:'or', k: ks } : ks[0];
  }
  const tree = orE();
  if (p < toks.length) fail(toks[p].t === ')' ? 'A parenthesis is not open.' : `Unexpected ${toks[p].t}.`);
  return tree;
}
function compile(src){
  try { return { tree: parseQuery(src), err: null }; }
  catch (e) { return { tree: null, err: e.message }; }
}
function evalNode(n, norm){
  switch (n.op){
    case 'term': return n.re.test(norm);
    case 'not': return !evalNode(n.k, norm);
    case 'and': return n.k.every(c => evalNode(c, norm));
    case 'or': return n.k.some(c => evalNode(c, norm));
  }
  return false;
}
function positives(n, out){
  if (n.op === 'term') out.push(n);
  else if (n.op !== 'not') n.k.forEach(c => positives(c, out));
  return out;
}
function describe(n, top){
  if (n.op === 'term') return n.phrase ? `the phrase “${n.label}”` : `the word ${n.label}`;
  if (n.op === 'not') return 'without ' + describe(n.k, false);
  const s = n.k.map(c => describe(c, false)).join(n.op === 'and' ? ' and ' : ' or ');
  return (n.op === 'or' && !top) ? `(${s})` : s;
}
function echoOf(tree){
  if (tree.op === 'not') return `Paragraphs ${describe(tree, true)}: every paragraph that lacks the word or phrase`;
  return `Paragraphs containing ${describe(tree, true)}`;
}
function highlight(text, srcs){
  if (!srcs.length) return esc(text);
  const re = new RegExp(srcs.map(s => `(?:${s})`).join('|'), 'giu');
  let out = '', last = 0, m;
  while ((m = re.exec(text))){
    if (m[0] === ''){ re.lastIndex++; continue; }
    out += esc(text.slice(last, m.index)) + '<mark>' + esc(m[0]) + '</mark>';
    last = m.index + m[0].length;
  }
  return out + esc(text.slice(last));
}

/* ---------- state ---------- */
const KEY = 'gc-verbatim-draft';
let STORE = true;
try { localStorage.setItem('t', '1'); localStorage.removeItem('t'); } catch (e) { STORE = false; }
let loaded = [];
if (STORE){ try { loaded = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { loaded = []; } }
const S = {
  q:'', tree:null, err:null, echo:'', pos:[], posG:[], hlSrcs:[],
  ticked: new Set(CODES), y0: YMIN, y1: YMAX, doc:'', sort:'year', limit:25,
  open:null, ctx:null, full:new Set(), stored:new Set(), rendered:0, order:[], draft: Array.isArray(loaded) ? loaded : []
};
let res = { base:[], hits:[] };
let chart = null, CHIPS = [];
const EX = ['"best interests" AND child', '(torture OR ill-treatment) NOT detention', '"reasonable accommodation"'];

function compute(){
  const yOK = d => d.year >= S.y0 && d.year <= S.y1;
  const dOK = d => !S.doc || d.title === S.doc;
  const base = S.err ? [] : D.filter(d => yOK(d) && dOK(d) && (!S.tree || evalNode(S.tree, d.norm)));
  const hits = base.filter(d => d.codes.some(c => S.ticked.has(c)));
  return { base, hits };
}
function yearCmp(x, y){
  return (y.year - x.year) || (x.title < y.title ? -1 : x.title > y.title ? 1 : 0) || (x.paragraph - y.paragraph);
}
function sortList(list){
  const a = list.slice();
  if (S.sort === 'matches' && S.tree){
    const m = new Map();
    a.forEach(d => m.set(d, S.posG.reduce((s, re) => s + ((d.norm.match(re) || []).length), 0)));
    a.sort((x, y) => (m.get(y) - m.get(x)) || yearCmp(x, y));
  } else a.sort(yearCmp);
  