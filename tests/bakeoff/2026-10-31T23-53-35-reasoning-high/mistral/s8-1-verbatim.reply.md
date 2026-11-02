I built a self-contained search tool over `WORKSHOP_DATA.gc` with a small boolean query language (uppercase AND/OR/NOT, `-term`, and `"exact phrases"`), committee and year dropdowns, live highlighting of matches in the untouched paragraph text, per-row "Copy citation" buttons, and a Chart.js bar chart of hits per committee. Everything is computed locally from the loaded records, and each result links its symbol to `doc_url` in a new tab.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>General Comments search · workshop data</title>
<style>
:root{--accent:#1f6fb2;--accent-dark:#185a92;--ink:#1d2733;--muted:#5c6b7a;--bg:#f4f6f9;--card:#fff;--line:#dce3ec}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px}
header.top{background:var(--card);border-bottom:1px solid var(--line);padding:26px 0 20px}
.kicker{font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 6px}
h1{font-size:1.55rem;line-height:1.25;margin:0 0 8px}
.lede{margin:0 0 6px}
.note{font-size:.86rem;color:var(--muted);margin:8px 0 0}
main.wrap{padding-bottom:70px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:18px 0}
.search-row{display:flex;gap:10px;flex-wrap:wrap}
#q{flex:1 1 320px;font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink)}
#q:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.btn-primary{font:inherit;font-weight:600;background:var(--accent);color:#fff;border:0;border-radius:8px;padding:10px 18px;cursor:pointer}
.btn-primary:hover{background:var(--accent-dark)}
.btn-secondary{font:inherit;background:#fff;border:1px solid var(--accent);color:var(--accent);border-radius:8px;padding:8px 14px;cursor:pointer;margin-top:8px}
.btn-secondary:hover{background:#eaf2fa}
.warn{display:none;margin:10px 0 0;font-size:.88rem;color:#7a5200;background:#fff6df;border:1px solid #ecd9a0;border-radius:8px;padding:8px 12px}
.howto{margin-top:12px;font-size:.9rem;color:var(--muted)}
.howto summary{cursor:pointer;color:var(--accent);font-weight:600}
.howto ul{margin:8px 0 0;padding-left:20px}
.howto li{margin:3px 0}
code{background:#eef2f7;border-radius:4px;padding:1px 5px;font-size:.88em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.chips{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:12px}
.chips-label{font-size:.86rem;color:var(--muted)}
.chip{font:inherit;font-size:.86rem;border:1px solid var(--line);background:#eef4fa;color:var(--accent-dark);border-radius:999px;padding:4px 12px;cursor:pointer}
.chip:hover{background:#dfeafa}
.filters{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
.filters label{display:flex;flex-direction:column;gap:4px;font-size:.86rem;color:var(--muted)}
.filters select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink);max-width:340px}
.stats{font-size:1.02rem;margin:20px 2px 2px}
h2{font-size:1.12rem;margin:0 0 10px}
.chartwrap{position:relative;width:100%;min-height:60px}
.result{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:12px 0}
.rhead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.symbol{font-weight:700;color:var(--accent);text-decoration:none}
.symbol:hover{text-decoration:underline}
.symbol.plain{color:var(--ink)}
.pill{font-size:.78rem;background:#eef2f7;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--muted);white-space:nowrap}
.pill.comm{background:#e8f1fa;border-color:#cfe2f2;color:var(--accent-dark);font-weight:600}
.copy-btn{margin-left:auto;font:inherit;font-size:.86rem;border:1px solid var(--accent);color:var(--accent);background:#fff;border-radius:8px;padding:5px 12px;cursor:pointer}
.copy-btn:hover{background:#eaf2fa}
.copy-btn.done{background:var(--accent);color:#fff}
.gc{margin:9px 0 2px;font-weight:600}
.fulltitle{font-weight:400;color:var(--muted);font-size:.88rem}
.citeline{font-size:.85rem;color:var(--muted);margin:2px 0 6px}
.ptext{margin:6px 0 0;white-space:pre-wrap;word-break:break-word}
.ptext.clamped{max-height:8.6em;overflow:hidden}
.linkbtn{background:none;border:0;color:var(--accent);font:inherit;font-size:.88rem;cursor:pointer;padding:4px 0 0;text-decoration:underline}
.cited{margin-top:8px;font-size:.82rem;color:var(--muted)}
mark{background:#ffe08a;color:inherit;border-radius:2px;padding:0 1px}
.fbar{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:.9rem}
.flabel{width:90px;flex:none;text-align:right;color:var(--muted)}
.ftrack{flex:1;background:#eef2f7;border-radius:4px;height:18px;overflow:hidden}
.ffill{display:block;height:100%;background:var(--accent)}
.fnum{width:44px;flex:none}
footer.note{margin-top:26px;border-top:1px solid var(--line);padding-top:12px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
@media (max-width:640px){.copy-btn{margin-left:0}}
</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <p class="kicker">Workshop tool · offline</p>
    <h1>Search the treaty bodies’ General Comments</h1>
    <p class="lede" id="lede"></p>
    <p class="note">Every result links to the UN document (<code>doc_url</code>, opens in a new tab) and shows the paragraph <strong>exactly as published</strong> — nothing is summarised. Matching words are highlighted.</p>
  </div>
</header>

<main class="wrap">
  <section class="card">
    <form id="searchForm">
      <div class="search-row">
        <label class="sr" for="q">Search the paragraph text</label>
        <input id="q" type="search" autocomplete="off" placeholder='e.g. "substantial grounds" OR torture NOT reservations'>
        <button class="btn-primary" type="submit">Search</button>
      </div>
    </form>
    <p id="warn" class="warn"></p>
    <details class="howto">
      <summary>How the search works (AND / OR / NOT / "phrases")</summary>
      <ul>
        <li>A word matches <strong>whole words</strong> in the paragraph text, ignoring case: <code>torture</code> matches “torture”, not “tortured”.</li>
        <li><code>"…"</code> = exact phrase, e.g. <code>"substantial grounds"</code>.</li>
        <li>Terms separated by spaces are combined with AND. Use uppercase <code>AND</code>, <code>OR</code>, <code>NOT</code> — or a leading <code>-</code> for NOT — e.g. <code>children OR adolescents</code>, <code>discrimination AND women NOT reservations</code>.</li>
        <li>Only the paragraph text is searched, not the titles. An empty box shows every paragraph (subject to the filters).</li>
      </ul>
    </details>
    <div class="chips">
      <span class="chips-label">Try:</span>
      <button type="button" class="chip" data-q='"substantial grounds"'>“substantial grounds”</button>
      <button type="button" class="chip" data-q="discrimination AND women">discrimination AND women</button>
      <button type="button" class="chip" data-q="children OR adolescents">children OR adolescents</button>
      <button type="button" class="chip" data-q="torture NOT reservations">torture NOT reservations</button>
    </div>
    <div class="filters">
      <label>Committee
        <select id="committee"></select>
      </label>
      <label>Year
        <select id="year"></select>
      </label>
      <label>Sort results
        <select id="sort">
          <option value="newest">Newest first</option>
          <option value="oldest">Oldest first</option>
          <option value="relevance">Most matched search terms</option>
        </select>
      </label>
    </div>
  </section>

  <p id="stats" class="stats" aria-live="polite"></p>
  <p id="statsNote" class="note"></p>

  <section class="card">
    <h2>Hits per committee</h2>
    <div id="chartWrap" class="chartwrap"></div>
    <p class="note">How this is computed: for each committee, the number of paragraphs in <code>WORKSHOP_DATA.gc</code> whose text matches the current query and the committee/year filters above — counted by this page from the loaded records, not estimated. Only committees with at least one hit are drawn.</p>
  </section>

  <section>
    <h2>Results</h2>
    <p class="note">How this is computed: the paragraphs of <code>WORKSHOP_DATA.gc</code> that pass the query and the filters, sorted as chosen above. Each row shows the symbol (link to the UN document, new tab), paragraph number, committee, year, the General Comment’s short title, the ready-to-use citation, and the full paragraph text exactly as in the data, with matches highlighted.</p>
    <div id="results"></div>
    <button id="more" class="btn-secondary" type="button" style="display:none"></button>
  </section>

  <footer class="note">Data: <code>window.WORKSHOP_DATA.gc</code>, already loaded in this page — no network requests are made. Counting, filtering, sorting, highlighting and the chart are all computed locally in your browser.</footer>
</main>

<script>
(function(){
'use strict';
var DATA = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc) || {};
var recs = Array.isArray(DATA.records) ? DATA.records : [];
function $(s){ return document.querySelector(s); }
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }

var qInput=$('#q'), committeeSel=$('#committee'), yearSel=$('#year'), sortSel=$('#sort');
var statsEl=$('#stats'), listEl=$('#results'), moreBtn=$('#more'), warnEl=$('#warn'), chartWrap=$('#chartWrap');

/* ---------- header: source, n, years (all read from the data) ---------- */
(function(){
  var years=recs.map(function(r){return Number(r.year);}).filter(function(y){return !isNaN(y);});
  var min=years.length?Math.min.apply(null,years):null, max=years.length?Math.max.apply(null,years):null;
  var docs=new Set(recs.map(function(r){return r.symbol;}).filter(Boolean)).size;
  $('#lede').textContent=(DATA.title?DATA.title+' — ':'')+
    'source: '+(DATA.source||'WORKSHOP_DATA.gc')+
    ' · '+recs.length+' paragraphs from '+docs+' documents'+
    (min!==null?' · years '+min+'–'+max:'');
  $('#statsNote').textContent='Counted locally in this page from the '+recs.length+' loaded paragraphs, after applying the query and the committee/year filters — not estimated.';
})();

/* ---------- filters ---------- */
function fillFilters(){
  var cc={}, yc={};
  recs.forEach(function(r){
    if(r.committee) cc[r.committee]=(cc[r.committee]||0)+1;
    var y=Number(r.year); if(!isNaN(y)) yc[y]=(yc[y]||0)+1;
  });
  var comms=Object.keys(cc).sort(function(a,b){ return cc[b]-cc[a] || a.localeCompare(b); });
  committeeSel.innerHTML='<option value="">All committees ('+recs.length+')</option>'+
    comms.map(function(c){ return '<option value="'+esc(c)+'">'+esc(c)+' ('+cc[c]+')</option>'; }).join('');
  var ys=Object.keys(yc).map(Number).sort(function(a,b){ return b-a; });
  yearSel.innerHTML='<option value="">All years</option>'+
    ys.map(function(y){ return '<option value="'+y+'">'+y+' ('+yc[y]+')</option>'; }).join('');
}

/* ---------- query language: AND / OR / NOT / "phrases" / -term ---------- */
function tokenize(q){
  var tokens=[], i=0, n=q.length, pendingNot=false, unbal=false;
  while(i<n){
    var c=q[i];
    if(/\s/.test(c)){ i++; continue; }
    if(c==='"' || c==='\u201C'){
      var close=(c==='"')?'"':'\u201D';
      var j=q.indexOf(close, i+1);
      if(j===-1){ j=n; unbal=true; }
      var val=q.slice(i+1,j);
      if(val.trim()===''){ i=j+1; continue; }
      tokens.push(pendingNot?{type:'not',value:val,phrase:true}:{type:'phrase',value:val});
      pendingNot=false; i=j+1; continue;
    }
    var k=i;
    while(k<n && !/\s/.test(q[k]) && q[k]!=='"' && q[k]!=='\u201C') k++;
    var raw=q.slice(i,k); i=k;
    if(raw==='-'){ pendingNot=true; continue; }
    var neg=pendingNot; pendingNot=false;
    if(raw.charAt(0)==='-' && raw.length>1){ neg=true; raw=raw.slice(1); }
    if(!raw) continue;
    if(!neg && (raw==='AND'||raw==='OR'||raw==='NOT')){ tokens.push({type:'op',value:raw}); continue; }
    tokens.push(neg?{type:'not',value:raw}:{type:'term',value:raw});
  }
  return {tokens:tokens, unbal:unbal};
}
function parse(tokens){
  var pos=0, warnings=[];
  function peek(){ return tokens[pos]; }
  function isTerm(t){ return t && (t.type==='term'||t.type==='phrase'||t.type==='not'); }
  function parseNot(){
    var t=peek(); if(!t) return null;
    if(t.type==='op' && t.value==='NOT'){ pos++; var c=parseNot(); return c?{kind:'not',child:c}:null; }
    if(t.type==='not'){ pos++; var c2=parseNot(); return c2?{kind:'not',child:{kind:'term',value:t.value,phrase:!!t.phrase}}:null; }
    if(t.type==='term'||t.type==='phrase'){ pos++; return {kind:'term',value:t.value,phrase:(t.type==='phrase')}; }
    return null;
  }
  function parseAnd(){
    var left=parseNot();
    while(true){
      var t=peek(); if(!t) break;
      if(t.type==='op' && t.value==='OR') break;
      if(t.type==='op' && t.value==='AND'){ pos++; var r=parseNot(); if(!r){ warnings.push('a trailing AND was ignored'); break; } left={kind:'and',children:[left,r]}; continue; }
      if(isTerm(t)){ var r2=parseNot(); if(!r2) break; left={kind:'and',children:[left,r2]}; continue; }
      break;
    }
    return left;
  }
  function parseOr(){
    var left=parseAnd();
    while(peek() && peek().type==='op' && peek().value==='OR'){
      pos++;
      var r=parseAnd();
      if(!r){ warnings.push('a trailing OR was ignored'); break; }
      left = left ? {kind:'or',children:[left,r]} : r;
    }
    return left;
  }
  var ast=parseOr();
  if(tokens.length && !ast) warnings.push('no search terms found in the query');
  return {ast:ast, warnings:warnings};
}
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
function termPattern(t){
  var e=escRe(String(t.value).trim()); if(!e) return null;
  if(t.phrase){ var parts=e.split(/\s+/).filter(Boolean); return parts.length?parts.join('\\s+'):null; }
  return '(?<![\\p{L}\\p{N}_])'+e+'(?![\\p{L}\\p{N}_])';
}
function compile(node){
  if(!node) return;
  if(node.kind==='term'){
    var p=termPattern(node);
    if(p){ node.pattern=p; node.reTest=new RegExp(p,'iu'); }
    else node.pattern=null;
  } else if(node.kind==='not'){ compile(node.child); }
  else { node.children.forEach(compile); }
}
function evalAst(node,text){
  if(!node) return true;
  if(node.kind==='term') return node.reTest ? node.reTest.test(text) : false;
  if(node.kind==='not') return !evalAst(node.child,text);
  if(node.kind==='and') return node.children.every(function(c){ return evalAst(c,text); });
  if(node.kind==='or') return node.children.some(function(c){ return evalAst(c,text); });
  return false;
}
function collectPositive(node,out,neg){
  if(!node) return;
  if(node.kind==='not'){ collectPositive(node.child,out,true); return; }
  if(node.kind==='term'){ if(!neg && node.pattern) out.push(node); return; }
  node.children.forEach(function(c){ collectPositive(c,out,neg); });
}

/* ---------- highlighting ---------- */
function highlight(text,pats){
  var sorted=pats.slice().sort(function(a,b){ return b.length-a.length; });
  var re=new RegExp('(?:'+sorted.join(')|(?:')+')','giu');
  var out='', last=0, m; re.lastIndex=0;
  while((m=re.exec(text))!==null){
    if(m[0]===''){ re.lastIndex++; continue; }
    out+=esc(text.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';
    last=m.index+m[0].length;
  }
  return out+esc(text.slice(last));
}

/* ---------- search ---------- */
var current=[];
function ynum(r){ var y=Number(r.year); return isNaN(y)?null:y; }
function run(){
  var q=qInput.value.trim(), ast=null, warnings=[];
  if(q){
    var tk=tokenize(q), p=parse(tk.tokens);
    ast=p.ast; warnings=p.warnings;
    if(tk.unbal) warnings.push('unbalanced quote — the text after the last opening quote was treated as a phrase');
    compile(ast);
  }
  var comm=committeeSel.value, yr=yearSel.value;
  var positives=[]; collectPositive(ast,positives,false);
  var out=[];
  recs.forEach(function(r){
    if(comm && r.committee!==comm) return;
    if(yr && String(r.year)!==yr) return;
    var text=(r.text==null)?'':String(r.text);
    if(ast && !evalAst(ast,text)) return;
    var pats=[], rel=0;
    positives.forEach(function(t){ if(t.reTest.test(text)){ pats.push(t.pattern); rel++; } });
    out.push({r:r, pats:pats, rel:rel});
  });
  var s=sortSel.value;
  out.sort(function(a,b){
    if(s==='relevance' && b.rel!==a.rel) return b.rel-a.rel;
    var ya=ynum(a.r), yb=ynum(b.r);
    var da=(ya===null)?(s==='oldest'?Infinity:-Infinity):ya;
    var db=(yb===null)?(s==='oldest'?Infinity:-Infinity):yb;
    if(da!==db) return (s==='oldest')? da-db : db-da;
    var ca=String(a.r.committee||''), cb=String(b.r.committee||'');
    if(ca!==cb) return ca.localeCompare(cb);
    return (Number(a.r.paragraph)||0)-(Number(b.r.paragraph)||0);
  });
  current=out;
  warnEl.textContent=warnings.join(' · ');
  warnEl.style.display=warnings.length?'block':'none';
  var bits=[current.length+' of '+recs.length+' paragraphs match',
    'query: '+(q?'\u201C'+q+'\u201D':'(empty — showing all)'),
    'committee: '+(comm||'all'), 'year: '+(yr||'all')];
  statsEl.innerHTML='<strong>'+esc(bits[0])+'</strong> · '+bits.slice(1).map(esc).join(' · ');
  renderChart();
  renderList(true);
}

/* ---------- chart: hits per committee ---------- */
var chart=null;
function renderChart(){
  var counts={};
  current.forEach(function(it){ var c=it.r.committee||'(no committee)'; counts[c]=(counts[c]||0)+1; });
  var labels=Object.keys(counts).sort(function(a,b){ return counts[b]-counts[a] || a.localeCompare(b); });
  var data=labels.map(function(l){ return counts[l]; });
  if(!labels.length){
    if(chart){ chart.destroy(); chart=null; }
    chartWrap.style.height='auto';
    chartWrap.innerHTML='<p class="note">No hits — the chart is empty because no paragraph matches the current query and filters.</p>';
    return;
  }
  if(window.Chart){
    chartWrap.innerHTML='<canvas id="chartCanvas"></canvas>';
    chartWrap.style.height=Math.max(140, labels.length*30+56)+'px';
    if(chart) chart.destroy();
    chart=new Chart($('#chartCanvas').getContext('2d'),{
      type:'bar',
      data:{labels:labels, datasets:[{label:'matching paragraphs', data:data, backgroundColor:'#1f6fb2', borderRadius:4}]},
      options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false}, tooltip:{callbacks:{label:function(c){ return ' '+c.parsed.x+' matching paragraph'+(c.parsed.x===1?'':'s'); }}}},
        scales:{x:{beginAtZero:true, ticks:{precision:0}, title:{display:true, text:'matching paragraphs'}}, y:{ticks:{autoSkip:false}}}}
    });
  } else {
    var max=Math.max.apply(null,data);
    chartWrap.style.height='auto';
    chartWrap.innerHTML=labels.map(function(l,i){
      return '<div class="fbar"><span class="flabel">'+esc(l)+'</span><span class="ftrack"><span class="ffill" style="width:'+Math.round(data[i]/max*100)+'%"></span></span><span class="fnum">'+data[i]+'</span></div>';
    }).join('');
  }
}

/* ---------- results ---------- */
var PAGE=100, shown=0;
function renderList(reset){
  if(reset){ listEl.innerHTML=''; shown=0; }
  if(!current.length){
    listEl.innerHTML='<p class="note">No paragraphs match. Try removing a filter or simplifying the query (for example, drop a NOT term).</p>';
    moreBtn.style.display='none'; return;
  }
  var frag=document.createDocumentFragment();
  current.slice(shown, shown+PAGE).forEach(function(it){ frag.appendChild(resultEl(it)); });
  listEl.appendChild(frag);
  shown+=Math.min(PAGE, current.length-shown);
  if(shown<current.length){
    moreBtn.style.display='inline-block';
    moreBtn.textContent='Show more ('+(current.length-shown)+' remaining)';
  } else moreBtn.style.display='none';
}
function resultEl(item){
  var r=item.r;
  var cite=String(r.symbol||'(no symbol)')+(r.paragraph!=null? ', para. '+r.paragraph : '');
  var art=document.createElement('article'); art.className='result';
  var head=document.createElement('div'); head.className='rhead';
  if(r.doc_url){
    var a=document.createElement('a'); a.className='symbol'; a.href=r.doc_url; a.target='_blank'; a.rel='noopener noreferrer';
    a.textContent=r.symbol||r.doc_url; head.appendChild(a);
  } else {
    var sp=document.createElement('span'); sp.className='symbol plain'; sp.textContent=r.symbol||'(no symbol)'; head.appendChild(sp);
  }
  if(r.paragraph!=null){ var p=document.createElement('span'); p.className='pill'; p.textContent='para. '+r.paragraph; head.appendChild(p); }
  if(r.committee){ var b=document.createElement('span'); b.className='pill comm'; b.textContent=r.committee; head.appendChild(b); }
  var y=Number(r.year); if(!isNaN(y)){ var yl=document.createElement('span'); yl.className='pill'; yl.textContent=y; head.appendChild(yl); }
  var btn=document.createElement('button'); btn.type='button'; btn.className='copy-btn'; btn.dataset.cite=cite; btn.textContent='Copy citation';
  head.appendChild(btn);
  art.appendChild(head);

  var gc=document.createElement('div'); gc.className='gc';
  gc.innerHTML=esc(r.short_title||r.title||'(untitled)')+(r.title&&r.short_title?' <span class="fulltitle">— '+esc(r.title)+'</span>':'');
  art.appendChild(gc);

  var cl=document.createElement('div'); cl.className='citeline';
  cl.innerHTML='Citation: <code>'+esc(cite)+'</code>';
  art.appendChild(cl);

  var text=(r.text==null)?'':String(r.text);
  var pt=document.createElement('p'); pt.className='ptext';
  pt.innerHTML=item.pats.length?highlight(text,item.pats):esc(text);
  art.appendChild(pt);
  if(text.length>900){
    pt.classList.add('clamped');
    var t=document.createElement('button'); t.type='button'; t.className='linkbtn';
    t.textContent='Show full paragraph ('+text.length+' chars)';
    t.addEventListener('click',function(){
      pt.classList.toggle('clamped');
      t.textContent=pt.classList.contains('clamped')?('Show full paragraph ('+text.length+' chars)'):'Show less';
    });
    art.appendChild(t);
  }
  if(Array.isArray(r.cited_articles)&&r.cited_articles.length){
    var ca=document.createElement('div'); ca.className='cited';
    ca.textContent='Cited articles: '+r.cited_articles.join(', ');
    art.appendChild(ca);
  }
  return art;
}

/* ---------- copy citation ---------- */
listEl.addEventListener('click', function(ev){
  var btn=ev.target.closest('.copy-btn'); if(!btn) return;
  var cite=btn.dataset.cite, done=function(ok){
    var old='Copy citation';
    btn.textContent=ok?'Copied \u2713':'Copy failed — citation shown above';
    btn.classList.add('done');
    setTimeout(function(){ btn.textContent=old; btn.classList.remove('done'); },1800);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(cite).then(function(){ done(true); }, function(){ fallback(); });
  } else fallback();
  function fallback(){
    var ok=false;
    try{
      var ta=document.createElement('textarea'); ta.value=cite;
      ta.style.cssText='position:fixed;opacity:0'; document.body.appendChild(ta);
      ta.select(); ok=document.execCommand('copy'); ta.remove();
    }catch(e){ ok=false; }
    done(ok);
  }
});

/* ---------- events ---------- */
var deb=null;
qInput.addEventListener('input',function(){ clearTimeout(deb); deb=setTimeout(run,180); });
$('#searchForm').addEventListener('submit',function(e){ e.preventDefault(); clearTimeout(deb); run(); });
committeeSel.addEventListener('change',run);
yearSel.addEventListener('change',run);
sortSel.addEventListener('change',run);
moreBtn.addEventListener('click',function(){ renderList(false); });
Array.prototype.forEach.call(document.querySelectorAll('.chip'),function(ch){
  ch.addEventListener('click',function(){ qInput.value=ch.dataset.q; run(); qInput.focus(); });
});

fillFilters();
run();
})();
</script>
</body>
</html>
```