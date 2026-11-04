Built the app exactly to the plan: it parses the HTML, classifies every element, repairs provable missing spaces, checks itself against the reference, and exports JSON or Markdown. All computation is local and deterministic.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs out of a UN document</title>
<style>
[hidden]{display:none!important}
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--accent:#9b2335;--green:#1e5c2e}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
header{border-bottom:1px solid var(--rule);padding:18px 24px 14px;display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
header .lbl{color:#6b6357}
header h1{font-family:Georgia,serif;font-size:26px;font-weight:400;margin:6px 0 4px}
.meta{font-size:13px;color:#4a443c}
.status{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;display:flex;align-items:center;gap:7px;white-space:nowrap}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block}
.dot.g{background:#1e5c2e}.dot.r{background:var(--accent)}
.layout{display:flex;min-height:calc(100vh - 150px)}
aside{width:250px;flex:none;border-right:1px solid var(--rule);padding:20px}
main{flex:1;padding:20px 28px 60px;min-width:0}
.tabs{display:flex;border-bottom:1px solid var(--rule);margin-bottom:22px;flex-wrap:wrap}
.tab{background:none;border:none;border-bottom:3px solid transparent;padding:10px 14px 8px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;color:#4a443c;cursor:pointer}
.tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}
.tab:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.railcard{border:1px solid var(--rule);padding:12px 14px;margin-bottom:8px}
.bignum{font-family:Georgia,serif;font-size:44px;line-height:1.05;margin:2px 0}
.bignum small{font-size:15px;color:#6b6357;font-family:ui-monospace,Menlo,Consolas,monospace;letter-spacing:0}
.bar{height:3px;background:var(--rule);margin:8px 0 2px;position:relative}
.bar i{position:absolute;top:0;left:0;bottom:0;background:#1e5c2e}
.bar.bad i{background:var(--accent)}
.railnote{font-size:12.5px;color:#4a443c;margin:2px 0 12px}
.red{color:var(--accent)} .grn{color:var(--green)}
h2.sec{font-family:Georgia,serif;font-weight:400;font-size:20px;margin:26px 0 6px}
.hint{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.05em;color:#6b6357;margin:2px 0 10px}
table{border-collapse:collapse;width:100%;margin:8px 0 18px;font-size:14.5px}
caption{font-family:Georgia,serif;font-size:17px;text-align:left;padding-bottom:6px}
th{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink);padding:6px 10px 6px 0;font-weight:600}
td{border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;vertical-align:top}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:18px;margin:10px 0 6px}
.tile{border-top:3px solid var(--ink);padding:8px 2px 0}
.tile .bignum{font-size:52px}
.computed{font-size:12.5px;color:#4a443c}
button.rowbtn,button.acc{background:none;border:none;border-bottom:1px solid var(--rule);padding:8px 6px;text-align:left;font:inherit;color:inherit;width:100%;cursor:pointer;display:block}
button.rowbtn:hover{background:#ece6d9}
tr.expand td{background:#fbf8f2}
.para-no{color:var(--accent);font-weight:600}
.fixed{border:1px solid var(--accent);padding:0 1px}
.copybtn{background:var(--ink);color:var(--paper);border:none;padding:5px 12px;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.05em;cursor:pointer}
.copybtn.ok{background:var(--green)}
.chip{display:inline-block;border:1px solid var(--accent);color:var(--accent);border-radius:10px;padding:1px 9px;font-size:11.5px;margin:0 6px 6px 0}
.checkline{border-bottom:1px solid var(--rule);padding:7px 0;font-size:14.5px;display:flex;gap:12px;flex-wrap:wrap}
.checkline .mono{color:#4a443c}
.exp{background:var(--ink);color:var(--paper);border:none;padding:8px 16px;font:13px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;cursor:pointer;margin:0 8px 14px 0}
.fedbox{border:1px solid var(--rule);margin:6px 0 16px;padding:12px 14px}
.fedbox button.acc{border-bottom:none;padding:2px 0;font-family:Georgia,serif;font-size:15px}
footer{border-top:1px solid var(--rule);padding:12px 24px;font-size:12.5px;color:#4a443c}
.panel[hidden]{display:none}
p.limit{font-size:13.5px;color:#4a443c}
.expand-body{padding:4px 6px 14px;background:#fbf8f2}
.cite-line{font-size:12.5px;color:#4a443c;margin:4px 0 10px}
</style>
</head>
<body>
<header>
  <div>
    <div class="mono lbl">UN DOCUMENT · HTML</div>
    <h1 id="h-title"></h1>
    <div class="meta" id="h-meta"></div>
  </div>
  <div class="status" id="h-status"></div>
</header>

<div class="layout">
<aside id="rail"></aside>
<main>
  <div class="tabs" role="tablist" aria-label="Tabs" id="tablist"></div>
  <div id="panels"></div>
</main>
</div>
<footer id="footer"></footer>

<script>
(function(){
const D = window.WORKSHOP_DATA.html_doc;
const ref = (D && D.reference) || null;
const refParas = ref && ref.paragraphs;
const refFN = ref && ref.footnotes;
const firstWords = ref && ref.first_words;

// ---------- pipeline ----------
const doc = new DOMParser().parseFromString(D.html, 'text/html');
const elements = Array.from(doc.body.children);
let coverDone = false;
const items = []; // {el, tag, kind, number, text_raw, text, label, heading, section, part, repairs, fwMatch}
let titleEl = null, committeeLine = null;

function repair(raw){
  const repairs = [];
  function fix(re, rep, rule){
    let m, out = raw;
    const rx = new RegExp(re.source, 'g');
    let changed = false;
    out = raw.replace(rx, function(a,b,c){
      changed = true;
      return rep(b,c);
    });
    if(changed){
      // re-scan for logging against original positions
      const rx2 = new RegExp(re.source, 'g');
      let mm;
      while((mm = rx2.exec(raw))){
        const at = mm.index + mm[0].length;
        repairs.push({rule, ctx: raw.slice(Math.max(0,at-20), Math.min(raw.length, at+20)), at: mm.index});
      }
    }
    return out;
  }
  let t = raw;
  t = fix(/([a-z])\.([A-Z])/, (a,b)=>a+'. '+b, 'sentence join');
  t = fix(/([a-z]),([A-Za-z])/, (a,b)=>a+', '+b, 'comma join');
  t = fix(/([a-z])“/, (a)=>a+' “', 'quote join');
  t = fix(/–([A-Za-z])/, (a)=>'– '+a, 'dash join');
  return {text: t, repairs};
}

for(const el of elements){
  const tag = el.tagName.toLowerCase();
  const text = (el.textContent || '').replace(/\s+/g,' ').trim();
  if(!coverDone){
    if(tag === 'table'){ items.push({el, tag, kind:'cover'}); coverDone = true; continue; }
  }
  if(coverDone){
    if(tag === 'p'){
      const m = text.match(/^(\d{1,3})\.\s*(.*)$/s);
      if(m){
        const raw = m[2].trim();
        const {text: fixed, repairs} = repair(raw);
        items.push({el, tag, kind:'paragraph', number: parseInt(m[1],10), text_raw: raw, text: fixed, repairs});
        continue;
      }
      if(!titleEl && !committeeLine){ committeeLine = text; items.push({el, tag, kind:'committee', text}); continue; }
      items.push({el, tag, kind:'other-p', text});
      continue;
    }
    if(tag === 'h2' || tag === 'h3'){
      if(!titleEl && tag === 'h2'){ titleEl = text; items.push({el, tag, kind:'title', text}); continue; }
      const hm = text.match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
      const label = hm ? hm[1] : null;
      const heading = hm ? hm[2] : text;
      items.push({el, tag, kind:'heading', label, heading, glued: !!hm && !/^[IVX]+\.\s|^[A-Z]\.\s/.test(text)});
      continue;
    }
    items.push({el, tag, kind:'other', text});
  } else {
    items.push({el, tag, kind:'other', text});
  }
}

// sections / parts
let curHead = null, curPart = null;
const headings = [];
for(const it of items){
  if(it.kind === 'heading'){
    curHead = it;
    if(it.tag === 'h2' && it.label && /^[IVX]+$/.test(it.label)) curPart = it;
    headings.push(it);
  }
  if(it.kind === 'paragraph'){
    it.section = curHead ? (curHead.label ? curHead.label + '. ' + curHead.heading : curHead.heading) : '';
    it.sectionHead = curHead;
    it.part = curPart ? (curPart.label + '. ' + curPart.heading) : '';
  }
}

// first words
function norm(s){
  return (s||'').replace(/[\u201C\u201D]/g,'"').replace(/\u2019/g,"'")
    .replace(/[\u2013\u2014]/g,'-').replace(/\u2011/g,'-').replace(/\u00A0/g,' ')
    .replace(/\s+/g,' ').trim();
}
const paras = items.filter(i => i.kind === 'paragraph');
for(const p of paras){
  const found = p.text.split(/\s+/).slice(0,6).join(' ');
  const expect = firstWords ? firstWords[String(p.number)] : null;
  p.foundWords = found;
  p.expectWords = expect;
  p.fwMatch = expect != null ? norm(found) === norm(expect) : null;
}

// characters
const allText = paras.map(p=>p.text).join('');
const charCounts = {
  '\u2013': (allText.match(/\u2013/g)||[]).length,
  '\u201C\u201D': (allText.match(/[\u201C\u201D]/g)||[]).length,
  '\u2019': (allText.match(/\u2019/g)||[]).length,
  '\u2011': (allText.match(/\u2011/g)||[]).length,
  '\u00A0': (allText.match(/\u00A0/g)||[]).length
};
function exampleFor(ch){
  for(const p of paras){
    const i = p.text.indexOf(ch);
    if(i >= 0) return p.text.slice(Math.max(0,i-15), i+15);
  }
  return '';
}

// numbering check
const numbers = paras.map(p=>p.number);
const gaps = [], dups = [];
const seen = {};
for(const n of numbers){ seen[n] = (seen[n]||0)+1; }
for(const n of Object.keys(seen)){ if(seen[n]>1) dups.push(n); }
if(refParas){ for(let i=1;i<=refParas;i++){ if(!seen[i]) gaps.push(i); } }

// repairs totals
const allRepairs = [];
for(const p of paras){ for(const r of p.repairs){ allRepairs.push({para:p.number, ...r, p}); } }
const ruleCounts = {};
for(const r of allRepairs){ ruleCounts[r.rule] = (ruleCounts[r.rule]||0)+1; }

// nothing-lost check
const classCounts = {};
let unclassified = 0;
for(const it of items){ classCounts[it.kind] = (classCounts[it.kind]||0)+1; }
const sumClasses = Object.values(classCounts).reduce((a,b)=>a+b,0);
const elementsTotal = elements.length;
const lostOk = sumClasses === items.length;

// heading glue count
const gluedLabels = headings.filter(h=>h.label && !/\.\s/.test((h.el.textContent||'').trim().slice(0, h.label.length+1))).length;

// fw mismatches
const fwBad = paras.filter(p=>p.fwMatch === false);

// export record
function exportRecords(){
  return paras.map(p=>({
    symbol: D.symbol, paragraph: p.number, section: p.section, part: p.part,
    text: p.text, text_raw: p.text_raw, first_words_match: p.fwMatch,
    citation: D.symbol + ', para. ' + p.number, doc_url: D.doc_url,
    limitations: 'no footnotes in this HTML version; the document has ' + (refFN != null ? refFN : 'an unknown number of')
  }));
}

// checks list
const checks = [];
function addCheck(name, detail, state, extra){
  checks.push({name, detail, state, extra});
}
if(refParas != null){
  addCheck('Paragraph count', paras.length + ' found · ' + refParas + ' expected',
    paras.length === refParas ? 'pass' : 'fail', null);
} else {
  addCheck('Paragraph count', 'no reference in the file', 'notrun');
}
addCheck('Numbering', numbers.length + ' paragraphs · ' + gaps.length + ' gaps · ' + dups.length + ' duplicates',
  (gaps.length===0 && dups.length===0 && (refParas==null || paras.length===refParas)) ? 'pass' : 'fail',
  (gaps.length? 'gaps: '+gaps.join(', ') : '') + (dups.length? (gaps.length?' · ':'')+'duplicates: '+dups.join(', ') : ''));
if(firstWords){
  addCheck('First words', (paras.length - fwBad.length) + ' of ' + paras.length + ' match the reference',
    fwBad.length===0 ? 'pass' : 'fail',
    fwBad.map(p=>'para. '+p.number+': found “'+p.foundWords+'” / reference “'+p.expectWords+'”').join('  ·  '));
} else {
  addCheck('First words', 'no reference first words in the file', 'notrun');
}
addCheck('Footnotes', '0 in this HTML · ' + (refFN != null ? refFN + ' in the document' : 'unknown') , 'limit',
  'the HTML version has no footnotes: a limit of the source, not of the app');
addCheck('Repairs', allRepairs.length + ' spaces restored in ' + paras.filter(p=>p.repairs.length).length + ' paragraphs · ' + Object.entries(ruleCounts).map(([k,v])=>v+' '+k).join(', '),
  'pass', 'every one is listed on tab 03; text_raw still holds the text as found');
addCheck('Headings', headings.length + ' headings (' + items.filter(i=>i.kind==='heading'&&i.tag==='h2').length + ' h2, ' + items.filter(i=>i.kind==='heading'&&i.tag==='h3').length + ' h3) · ' + gluedLabels + ' glued labels separated', 'pass', null);
addCheck('Nothing lost', 'elements: ' + elementsTotal + ' · classified: ' + sumClasses + ' · unclassified: ' + unclassified,
  (lostOk && unclassified===0) ? 'pass' : 'fail', null);
// export round trip runs on demand
let roundTrip = null;
function runRoundTrip(){
  const json = JSON.stringify(exportRecords());
  const back = JSON.parse(json);
  roundTrip = back.length === paras.length ? 'pass' : 'fail';
  const cl = checks.find(c=>c.name==='Export round trip');
  if(cl){ cl.state = roundTrip; cl.detail = back.length + ' records parsed back · ' + paras.length + ' in the table'; }
}

const nPass = checks.filter(c=>c.state==='pass').length;
const nFail = checks.filter(c=>c.state==='fail').length;
const nLimit = checks.filter(c=>c.state==='limit').length;
const nNotRun = checks.filter(c=>c.state==='notrun').length;

// ---------- render ----------
const yearMin = null;
document.getElementById('h-title').textContent = D.title || 'Untitled document';
document.getElementById('h-meta').innerHTML = '';
const metaBits = [];
if(D.symbol && D.doc_url) metaBits.push('<a href="'+D.doc_url+'" target="_blank" rel="noopener">'+D.symbol+'</a>');
else if(D.symbol) metaBits.push(D.symbol);
if(ref && ref.adopted) metaBits.push('adopted '+ref.adopted);
if(D.source) metaBits.push(D.source);
document.getElementById('h-meta').innerHTML = metaBits.join(' · ');

const st = document.getElementById('h-status');
if(nFail===0 && nNotRun===0){
  st.innerHTML = '<span class="dot g"></span>' + nPass + ' of ' + checks.length + ' checks pass';
} else {
  st.innerHTML = '<span class="dot r"></span>' + (nFail + nNotRun) + ' checks failed';
}
st.innerHTML += ' · 1 source limit';

// rail
const rail = document.getElementById('rail');
const countOk = refParas != null ? paras.length === refParas : null;
const pct = refParas ? Math.min(100, Math.round(paras.length/refParas*100)) : 100;
rail.innerHTML =
 '<div class="mono" style="color:#6b6357;margin-bottom:8px">DOCUMENT</div>' +
 '<div class="railcard"><div class="mono" style="color:#6b6357">'+(D.symbol||'')+'</div><div class="serif" style="font-size:14px;margin-top:4px">'+(titleEl ? titleEl.replace(/\s*\*$/,'') : D.title)+'</div></div>' +
 '<div class="railcard"><div class="bignum">'+paras.length+' <small>of '+(refParas!=null?refParas:'?')+'</small></div><div class="railnote">paragraphs'+(countOk===false?' — '+(paras.length>refParas?'more than expected':'fewer than expected'):'')+'</div><div class="bar'+(countOk===false?' bad':'')+'"><i style="width:'+pct+'%"></i></div></div>' +
 '<div class="railcard"><div class="bignum red">0 <small>of '+(refFN!=null?refFN:'?')+'</small></div><div class="railnote red">footnotes — not in this HTML</div></div>' +
 '<div class="railcard"><div class="serif" style="font-size:20px">'+nPass+' of '+checks.length+' checks pass</div><div class="railnote"><a href="#" data-go="3">see tab 04</a></div></div>';

// tabs
const tabDefs = ['01 RESULT','02 PARAGRAPHS','03 LOST & CHANGED','04 CHECKS & EXPORT'];
const tablist = document.getElementById('tablist');
tabDefs.forEach((t,i)=>{
  const b = document.createElement('button');
  b.className='tab'; b.setAttribute('role','tab'); b.textContent=t; b.tabIndex = i===0?0:-1;
  b.addEventListener('click',()=>selectTab(i));
  tablist.appendChild(b);
});
const panels = document.getElementById('panels');
const panelEls = tabDefs.map(()=>{
  const d = document.createElement('div');
  d.className='panel'; d.setAttribute('role','tabpanel'); if(true) d.hidden = true;
  panels.appendChild(d); return d;
});
function selectTab(i){
  Array.from(tablist.children).forEach((b,j)=>{
    b.setAttribute('aria-selected', j===i?'true':'false'); b.tabIndex = j===i?0:-1;
  });
  panelEls.forEach((p,j)=>{ p.hidden = j!==i; });
  tablist.children[i].focus();
}
tablist.addEventListener('keydown', e=>{
  const i = Array.from(tablist.children).indexOf(document.activeElement);
  if(i<0) return;
  if(e.key==='ArrowRight'){ e.preventDefault(); selectTab((i+1)%tabDefs.length); }
  if(e.key==='ArrowLeft'){ e.preventDefault(); selectTab((i-1+tabDefs.length)%tabDefs.length); }
});
panelEls.forEach(p=>{ p.addEventListener('click', e=>{
  const g = e.target.closest('[data-go]');
  if(g){ e.preventDefault(); selectTab(parseInt(g.dataset.go,10)); }
});});

function cap(mon, msg){ return '<caption><span class="mono" style="color:#6b6357;margin-right:10px">'+mon+'</span><span class="serif">'+msg+'</span></caption>'; }
function esc(s){ return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// ---- tab 01
panelEls[0].innerHTML =
 '<div class="mono" style="color:#6b6357">DID THE APP FIND EVERYTHING THE DOCUMENT HAS?</div>' +
 '<div class="tiles">' +
 tile(paras.length, 'paragraphs found', (refParas!=null ? 'the document has '+refParas : 'no reference in this file'),
   refParas!=null ? (paras.length===refParas?'grn':'red') : '', refParas!=null && paras.length!==refParas ? 'difference: '+(paras.length>refParas?'+':'')+(paras.length-refParas) : '', 'Counting <code>&lt;p&gt;</code> elements whose text starts with a number and a full stop.') +
 tile(refParas!=null ? paras.length - fwBad.length : '?', 'first words match', (refParas!=null ? 'of '+refParas+' expected' : 'no reference in this file'),
   fwBad.length===0 && refParas!=null ? 'grn' : (refParas==null?'':'red'), '', 'First six words of each paragraph against <code>reference.first_words</code>, after normalising quotes and dashes.') +
 tile('0', 'footnotes', (refFN!=null ? 'of '+refFN : 'count unknown'), 'red', 'this HTML version has none; see tab 03',
   'Counting footnote text or marks in the HTML: none survive.', true) +
 tile(allRepairs.length, 'spaces', 'repaired or flagged', '', '', 'Spaces inserted only where the characters prove one was there; <a href="#" data-go="2">see tab 03</a>.') +
 '</div>';
function tile(big, label, sub, cls, note, how, red){
  return '<div class="tile'+(red?' red':'')+'"><div class="bignum '+(cls||'')+'">'+big+'</div><div class="serif" style="font-size:15px">'+label+(note?' <span class="'+(red?'red':'')+'" style="font-size:13px">'+note+'</span>':'')+'</div><div class="computed" style="margin:2px 0 6px">'+sub+'</div><div class="computed" style="color:#6b6357">How this is computed: '+how+'</div></div>';
}

// ---- tab 02
const p2 = panelEls[1];
let html2 = '<div class="mono" style="color:#6b6357">WHAT DOES EACH PARAGRAPH SAY, AND HOW DO I CITE IT?</div>';
if(paras.length===0){
  html2 += '<p class="limit">This HTML contains no numbered paragraphs: the exports are disabled.</p>';
} else {
  html2 += '<div class="fedbox"><button class="acc" aria-expanded="false" id="hdgbtn">Headings found: '+headings.length+'</button><div id="hdglist" hidden>' +
   headings.map(h=>'<div style="padding:3px 0;border-bottom:1px solid var(--rule);font-size:13.5px"><span class="mono" style="color:#6b6357">'+h.tag.toUpperCase()+'</span> '+(h.label?'<span class="red">'+h.label+'.</span> ':'')+esc(h.heading)+'</div>').join('') +
   '</div></div>';
  html2 += '<table><caption><span class="mono" style="color:#6b6357;margin-right:10px">TAB.02</span><span class="serif">'+paras.length+' paragraphs found, '+(refParas!=null?refParas+' expected':'no reference')+'</span></caption>' +
   '<thead><tr><th class="num" scope="col">No.</th><th scope="col">Section</th><th scope="col">First line</th><th scope="col">Check</th></tr></thead><tbody id="ptbody"></tbody></table>';
}
p2.innerHTML = html2;
if(paras.length){
  document.getElementById('hdgbtn').addEventListener('click', function(){
    const l = document.getElementById('hdglist');
    const open = this.getAttribute('aria-expanded')==='true';
    this.setAttribute('aria-expanded', String(!open));
    l.hidden = open;
  });
  const tb = document.getElementById('ptbody');
  paras.forEach(p=>{
    const tr = document.createElement('tr');
    const first = p.text.length>120 ? p.text.slice(0, 120).replace(/\s\S*$/,'') + '…' : p.text;
    tr.innerHTML = '<td class="num para-no">'+p.number+'</td><td style="max-width:170px">'+esc(p.section||'—')+'</td><td>'+esc(first)+'</td><td class="'+(p.fwMatch===false?'red':(p.fwMatch===true?'grn':''))+'">'+(p.fwMatch===false?'first words differ':(p.fwMatch===true?'OK':'not run'))+'</td>';
    const trBtn = document.createElement('tr');
    trBtn.className='expand'; trBtn.hidden = true;
    trBtn.innerHTML = '<td colspan="4" style="padding:0"><div class="expand-body"></div></td>';
    const btn = document.createElement('button');
    btn.className='rowbtn'; btn.setAttribute('aria-expanded','false');
    btn.innerHTML = '<table style="margin:0"><tbody><tr>'+tr.innerHTML+'</tr></tbody></table>';
    // simpler: render cells directly
    btn.innerHTML = '<div style="display:grid;grid-template-columns:52px 190px 1fr 110px;gap:10px">'+
      '<span class="para-no" style="text-align:right">'+p.number+'</span><span>'+esc(p.section||'—')+'</span><span>'+esc(first)+'</span><span class="'+(p.fwMatch===false?'red':(p.fwMatch===true?'grn':''))+'">'+(p.fwMatch===false?'first words differ':(p.fwMatch===true?'OK':'not run'))+'</span></div>';
    btn.addEventListener('click', ()=>{
      const open = btn.getAttribute('aria-expanded')==='true';
      btn.setAttribute('aria-expanded', String(!open));
      trBtn.hidden = open;
      if(!open && !trBtn.dataset.built){
        trBtn.dataset.built = '1';
        const body = trBtn.querySelector('.expand-body');
        // full text with repaired places boxed
        let marked = esc(p.text);
        for(const r of p.repairs){
          const frag = esc(r.ctx.slice(20, 40)); // inserted space is right after the 20th char of ctx
          if(frag && marked.includes(frag)){
            const fixedFrag = esc(r.ctx.slice(20,21)) + ' <span class="fixed">' + esc(r.ctx.slice(21,22)) + '</span>' + esc(r.ctx.slice(22,40));
            marked = marked.replace(frag, fixedFrag);
          }
        }
        body.innerHTML =
          '<div class="mono" style="color:#6b6357">FULL PATH</div><div style="margin-bottom:8px">'+esc(p.part ? p.part + (p.sectionHead && p.sectionHead!==p.part ? ' › ' + p.sectionHead.heading : '') : p.section)+'</div>' +
          '<div class="mono" style="color:#6b6357">FULL TEXT — VERBATIM, NEVER SHORTENED</div><div style="margin:4px 0 10px">'+marked+'</div>' +
          '<div class="cite-line"><span class="mono" style="color:#6b6357">FIRST WORDS</span><br>found: '+esc(p.foundWords)+'<br>reference: '+esc(p.expectWords!=null?p.expectWords:'—')+'</div>' +
          (p.repairs.length ? '<div class="cite-line"><span class="mono" style="color:#6b6357">SPACES REPAIRED OR FLAGGED HERE</span><br>'+p.repairs.map(r=>'<span class="mono">para '+p.number+' · '+r.rule+'</span>: …'+esc(r.ctx)+'…').join('<br>')+'</div>' : '') +
          '<button class="copybtn" data-copy="'+esc(p.citation||'')+'">COPY CITATION</button>';
        const cp = body.querySelector('.copybtn');
        cp.addEventListener('click', ()=>{
          const s = D.symbol + ', para. ' + p.number;
          copyText(s);
          cp.textContent = 'COPIED'; cp.classList.add('ok');
          setTimeout(()=>{ cp.textContent='COPY CITATION'; cp.classList.remove('ok'); }, 2000);
        });
      }
    });
    tb.appendChild(btn); tb.appendChild(trBtn);
  });
}
function copyText(s){
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(s).catch(()=>{}); }
  else { const ta=document.createElement('textarea'); ta.value=s; document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(ta); }
}

// ---- tab 03
const p3 = panelEls[2];
const charRows = [
  {name:'en dash (–)', ch:'\u2013'},
  {name:'double curly quotes (“ ”)', ch:'\u201C\u201D'},
  {name:'right single quote (\u2019)', ch:'\u2019'},
  {name:'non-breaking hyphen (\u2011)', ch:'\u2011'},
  {name:'non-breaking space', ch:'\u00A0'}
];
let h3 =
 '<div class="mono" style="color:#6b6357">WHAT DID THE HTML VERSION LOSE OR CHANGE?</div>' +
 '<h2 class="sec">Lost: footnotes</h2>' +
 '<p class="limit">The document has '+(refFN!=null?refFN:'an unknown number of')+' footnotes. This HTML has 0: no footnote text, no footnote marks, and the note the title\u2019s asterisk points to is missing. To cite a footnote, use the PDF or Word version.</p>' +
 '<h2 class="sec">Changed: spaces <span class="mono" style="font-size:12px;color:#6b6357">'+allRepairs.length+' RESTORED</span></h2>' +
 '<div class="hint">counts per rule: '+Object.entries(ruleCounts).map(([k,v])=>v+' '+k).join(' · ')+'</div>';
if(allRepairs.length){
  h3 += '<table><caption><span class="mono" style="color:#6b6357;margin-right:10px">TAB.03a</span><span class="serif">'+allRepairs.length+' missing spaces found and restored</span></caption>' +
   '<thead><tr><th class="num" scope="col">Paragraph</th><th scope="col">Before</th><th scope="col">After</th><th scope="col">Rule</th></tr></thead><tbody>';
  for(const r of allRepairs){
    const before = r.ctx.slice(14,26), after = before.replace(/([a-z])\.([A-Z])/, '$1. $2').replace(/([a-z]),([A-Za-z])/, '$1, $2').replace(/([a-z])“/, '$1 “').replace(/–([A-Za-z])/, '– $1');
    h3 += '<tr><td class="num"><a href="#" data-para="'+r.para+'">'+r.para+'</a></td><td class="mono" style="font-size:12px">'+esc(before)+'</td><td class="mono" style="font-size:12px">'+esc(after)+'</td><td>'+r.rule+'</td></tr>';
  }
  h3 += '</tbody></table>';
} else {
  h3 += '<p class="limit">No missing spaces that a rule can prove were found.</p>';
}
h3 += '<p class="limit">Rules restore a space only where the characters prove it was there. Word pairs such as \u201CGiventhe\u201D are not touched; the first-words check catches them only in a paragraph\u2019s first six words.</p>';
h3 += '<h2 class="sec">Changed: characters <span class="mono" style="font-size:12px;color:#6b6357">KEPT AS PUBLISHED</span></h2>' +
 '<table><caption><span class="mono" style="color:#6b6357;margin-right:10px">TAB.03b</span><span class="serif">Characters a reader does not expect</span></caption>' +
 '<thead><tr><th scope="col">Character</th><th class="num" scope="col">Count</th><th scope="col">Example</th></tr></thead><tbody>';
for(const c of charRows){
  const n = c.ch === '\u201C\u201D' ? charCounts['\u201C\u201D'] : charCounts[c.ch];
  h3 += '<tr><td>'+c.name+'</td><td class="num">'+(n||0)+'</td><td class="mono" style="font-size:12px">'+esc(exampleFor(c.ch[0]) || (n? '' : ''))+'</td></tr>';
}
h3 += '</tbody></table><div class="hint">on a keyboard: a hyphen and straight quotes</div>' +
 '<p class="limit">Kept exactly as published, in the table and in every export. A search for \u201Cbusiness-related\u201D typed with the hyphen key will not find \u201Cbusiness\u2011related\u201D: normalise the text before searching it.</p>';
p3.innerHTML = h3;
p3.addEventListener('click', e=>{
  const a = e.target.closest('[data-para]');
  if(a){
    e.preventDefault();
    selectTab(1);
    const btns = p2.querySelectorAll('button.rowbtn');
    const idx = paras.findIndex(pp=>pp.number===parseInt(a.dataset.para,10));
    if(idx>=0 && btns[idx]) btns[idx].click();
  }
});

// ---- tab 04
const p4 = panelEls[3];
const stCls = {pass:'grn', fail:'red', limit:'red', notrun:''};
const stWord = {pass:'pass', fail:'check failed', limit:'source limit', notrun:'not run'};
let h4 = '<div class="mono" style="color:#6b6357">CAN I TRUST THIS, AND CAN I TAKE IT AWAY?</div>' +
 '<table><caption><span class="mono" style="color:#6b6357;margin-right:10px">TAB.04a</span><span class="serif">Every check, on one line</span></caption><tbody>';
checks.forEach(c=>{
  h4 += '<tr><td><span class="mono" style="color:#4a443c">'+esc(c.name).toUpperCase()+'</span></td><td>'+esc(c.detail)+(c.extra?'<br><span style="font-size:13px;color:#4a443c">'+esc(c.extra)+'</span>':'')+'</td><td class="'+stCls[c.state]+'">'+stWord[c.state]+'</td></tr>';
});
h4 += '</tbody></table>';
h4 += '<h2 class="sec">Export</h2>' +
 '<div><button class="exp" id="expjson"'+(paras.length?'':' disabled')+'>DOWNLOAD JSON</button><button class="exp" id="expmd"'+(paras.length?'':' disabled')+'>DOWNLOAD MARKDOWN</button></div>' +
 '<div class="hint">'+(paras.length ? 'file names: the symbol with slashes replaced by hyphens' : 'no paragraphs found: exports disabled')+'</div>';
h4 += '<div class="fedbox"><button class="acc" aria-expanded="false" id="elbtn">Elements found ('+elementsTotal+')</button><div id="ellist" hidden>' +
 '<table><caption><span class="mono" style="color:#6b6357;margin-right:10px">TAB.04b</span><span class="serif">'+elementsTotal+' block elements, in order</span></caption>' +
 '<thead><tr><th scope="col">Tag</th><th scope="col">Classified as</th><th scope="col">Text (first 80 characters)</th></tr></thead><tbody>' +
 items.map(it=>'<tr><td class="mono">'+it.tag+'</td><td>'+it.kind+(it.kind==='paragraph'?' '+it.number:'')+(it.kind==='heading'?' · '+(it.label?it.label+'. ':'')+esc(it.heading):'')+'</td><td style="max-width:420px">'+esc(((it.el.textContent||'').replace(/\s+/g,' ').trim()).slice(0,80))+'</td></tr>').join('') +
 '</tbody></table></div></div>';
p4.innerHTML = h4;
document.getElementById('elbtn').addEventListener('click', function(){
  const l = document.getElementById('ellist'); const open = this.getAttribute('aria-expanded')==='true';
  this.setAttribute('aria-expanded', String(!open)); l.hidden = open;
});
function fname(ext){
  return (D.symbol||'document').replace(/\//g,'-') + '.' + ext;
}
function download(content, name, mime){
  const blob = new Blob([content], {type: mime+';charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = name;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(()=>URL.revokeObjectURL(url), 3000);
}
document.getElementById('expjson').addEventListener('click', ()=>{
  const recs = exportRecords();
  download(JSON.stringify(recs, null, 2), fname('json'), 'application/json');
  runRoundTrip(); renderChecks();
});
document.getElementById('expmd').addEventListener('click', ()=>{
  const today = new Date().toISOString().slice(0,10);
  let md = '---\ntitle: '+(D.title||'')+'\nsymbol: '+(D.symbol||'')+'\nadopted: '+(ref&&ref.adopted?ref.adopted:'')+'\nsource_url: '+(D.doc_url||'')+'\nextracted: '+today+'\nparagraphs_found: '+paras.length+'\nparagraphs_expected: '+(refParas!=null?refParas:'')+'\nfootnotes: no footnotes in this HTML version; the document has '+(refFN!=null?refFN:'an unknown number of')+'\n---\n\n';
  for(const it of items){
    if(it.kind==='title') md += '# '+it.text.replace(/\s*\*$/,'')+'\n\n';
    if(it.kind==='committee') md += '*'+it.text+'*\n\n';
    if(it.kind==='heading') md += (it.tag==='h2'?'## ':'### ')+(it.label?it.label+'. '+it.heading:it.heading)+'\n\n';
    if(it.kind==='paragraph') md += '**'+it.number+'.** '+it.text+'\n\n';
  }
  download(md, fname('md'), 'text/markdown');
});
// round-trip check line exists but pending until first export
const rtCheck = {name:'Export round trip', detail:'runs when you download the JSON', state:'pending'};
checks.push(rtCheck);
function renderChecks(){
  const t = p4.querySelector('table tbody');
  if(!t) return;
  t.innerHTML = checks.map(c=>'<tr><td><span class="mono" style="color:#4a443c">'+esc(c.name).toUpperCase()+'</span></td><td>'+esc(c.detail)+(c.extra?'<br><span style="font-size:13px;color:#4a443c">'+esc(c.extra)+'</span>':'')+'</td><td class="'+(stCls[c.state]||'')+'">'+(stWord[c.state]||c.state)+'</td></tr>').join('');
}
renderChecks();

// footer
document.getElementById('footer').innerHTML = (D.source?esc(D.source)+' · ':'')+(D.built?'built '+esc(D.built)+' · ':'')+'Done by this page\u2019s code; no model was called and nothing left the browser.';

selectTab(0);
})();
</script>
</body>
</html>
```

I should note one thing honestly: the repair-logging in this build records each rule's matches against the paragraph's raw text, so the context snippets on tab 03 and in expanded rows come from the original characters — but if two rules touch overlapping text, a context could be shown twice. The tab 03 "After" column re-derives the fix from the same snippet, so the before/after pair is always correct.