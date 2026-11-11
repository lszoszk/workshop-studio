I rebuilt the app with two tabs, **01 COMPARE** (your earlier tool) and **02 WHO VOTES WITH**, in the paper-and-ink style with a red accent. "Who votes with" uses State A as the first State, and the resolutions/amendments/both switch is shared by both tabs. Because it adds tabs and a new layout, this is the whole file.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Human Rights Council votes: comparing States</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--muted:#5a554c}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.mono{font:11.5px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
header{padding:20px 0 12px;border-bottom:1px solid var(--rule)}
h1{font:400 30px/1.2 Georgia,"Times New Roman",serif;margin:6px 0}
header p{margin:0;color:var(--muted);font-size:14px}
[role=tablist]{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-top:6px}
[role=tab]{background:none;border:0;border-bottom:3px solid transparent;padding:12px 18px 10px;cursor:pointer;font:12px ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
[role=tab][aria-selected=true]{color:var(--red);border-bottom-color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.controls{display:flex;flex-wrap:wrap;gap:14px 26px;padding:16px 0;border-bottom:1px solid var(--rule);align-items:flex-end}
.field{display:flex;flex-direction:column;gap:4px}
select{font:inherit;padding:7px 9px;border:1px solid var(--rule);background:#fffdf8;color:var(--ink);max-width:290px}
h2{font:400 22px Georgia,serif;margin:28px 0 4px}
.big{font:400 52px/1.1 Georgia,serif;color:var(--ink)}
.stats{display:flex;flex-wrap:wrap;gap:10px 48px;margin-top:20px}
.how{font-size:13.5px;color:var(--muted);margin:6px 0;max-width:90ch}
.hint{font:11px ui-monospace,Menlo,monospace;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:15px;margin-top:8px}
caption{text-align:left;font:11.5px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:6px 0}
th{text-align:left;font:11px ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border-bottom:2px solid var(--rule);padding:8px 8px 6px}
td{border-bottom:1px solid var(--rule);padding:8px;vertical-align:top}
a{color:var(--red)}
.v{font:12px ui-monospace,Menlo,monospace;white-space:nowrap}
.warn{display:block;color:#8a5a00;font-size:12.5px;margin-top:3px}
.chartbox{position:relative;margin-top:8px}
.msg{padding:14px 0;color:var(--muted)}
[hidden]{display:none!important}
footer{padding:26px 0;color:var(--muted);font-size:13px}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="mono">Human Rights Council · recorded votes</div>
  <h1>How States vote at the Human Rights Council</h1>
  <p id="sourceLine"></p>
</header>
<div role="tablist" aria-label="Views">
  <button role="tab" id="tab1" aria-selected="true" aria-controls="p1" tabindex="0">01 Compare two States</button>
  <button role="tab" id="tab2" aria-selected="false" aria-controls="p2" tabindex="-1">02 Who votes with</button>
</div>
<div class="controls">
  <div class="field"><span class="mono"><label for="selA" id="lblA">State A</label></span><select id="selA"></select></div>
  <div class="field" id="fieldB"><span class="mono"><label for="selB">State B</label></span><select id="selB"></select></div>
  <div class="field"><span class="mono"><label for="selKind">Votes included</label></span>
    <select id="selKind"><option value="all">Resolutions and amendments</option><option value="resolution">Resolutions only</option><option value="amendment">Amendments only</option></select></div>
  <div class="field" id="fieldList"><span class="mono"><label for="selList">List below</label></span>
    <select id="selList"><option value="diff">Differing votes only</option><option value="all">All joint votes</option></select></div>
</div>
<p class="msg" id="fatal" hidden></p>

<section id="p1" role="tabpanel" aria-labelledby="tab1">
  <p class="msg" id="sameMsg" hidden></p>
  <div id="res1">
    <div class="stats">
      <div><div class="big" id="sJoint">0</div><div class="mono">votes both took part in</div></div>
      <div><div class="big" id="sSame">0</div><div class="mono">voted the same way</div></div>
      <div><div class="big" id="sDiff">0</div><div class="mono">votes where they differed</div></div>
    </div>
    <p class="how" id="howStats"></p>
    <h2>Timeline by year</h2>
    <span class="mono">FIG.01 · joint votes and agreement per year</span>
    <div class="chartbox" style="height:340px"><canvas id="cTime" aria-label="Timeline by year"></canvas></div>
    <p class="msg" id="timeEmpty" hidden>No joint votes in this filter, so there is no timeline.</p>
    <p class="how" id="howTime"></p>
    <h2 id="listTitle"></h2>
    <p class="how" id="howList"></p>
    <table>
      <caption id="cap1">Votes in the current filter</caption>
      <thead><tr><th scope="col">Date</th><th scope="col">Vote</th><th scope="col" id="thA"></th><th scope="col" id="thB"></th></tr></thead>
      <tbody id="tbody"></tbody>
    </table>
    <p class="msg" id="emptyList" hidden></p>
  </div>
</section>

<section id="p2" role="tabpanel" aria-labelledby="tab2" hidden>
  <h2 id="rTitle"></h2>
  <p class="hint">State A is the first State you picked · change it in the bar above · minimum 10 shared votes</p>
  <p class="msg" id="rEmpty" hidden></p>
  <div id="rWrap">
    <h2 style="font-size:18px">Closest</h2>
    <span class="mono">FIG.02 · share of shared votes cast the same way</span>
    <div class="chartbox" id="boxClose"><canvas id="cClose" aria-label="Closest States"></canvas></div>
    <h2 style="font-size:18px">Furthest</h2>
    <span class="mono">FIG.03 · share of shared votes cast the same way</span>
    <div class="chartbox" id="boxFar"><canvas id="cFar" aria-label="Furthest States"></canvas></div>
    <p class="how" id="rCut"></p>
    <p class="how" id="rHow"></p>
    <p class="how" id="rLeaves"></p>
  </div>
</section>
<footer>All figures are counted in your browser from the loaded Council votes. Nothing is estimated.</footer>
</div>

<script>
(function(){
"use strict";
var D=window.WORKSHOP_DATA||{}, H=D.hrc||{}, recs=Array.isArray(H.records)?H.records:[], names=H.countries||{};
var MIN=10, TOP=20;
function $(i){return document.getElementById(i);}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function yr(r){if(typeof r.year==='number')return r.year;var m=/^(\d{4})/.exec(r.date||'');return m?+m[1]:null;}
var VL={Y:'Yes',N:'No',A:'Abstain'};
function nm(iso){return names[iso]||iso;}
function kindText(k){return k==='all'?'resolutions and amendments':k==='resolution'?'resolutions only':'amendments only';}
function filt(){var k=$('selKind').value;return recs.filter(function(r){return k==='all'||r.kind===k;});}
function roll(r){var c={Y:0,N:0,A:0},v=r.votes||{};for(var i in v)if(c[v[i]]!==undefined)c[v[i]]++;return c;}
function mism(r){if(typeof r.yes!=='number'||typeof r.no!=='number'||typeof r.abstain!=='number')return null;var c=roll(r);return(c.Y===r.yes&&c.N===r.no&&c.A===r.abstain)?null:c;}

var isos={};
recs.forEach(function(r){for(var i in (r.votes||{}))isos[i]=1;});
var members=Object.keys(isos).map(function(i){return{iso:i,name:nm(i)};}).sort(function(a,b){return a.name.localeCompare(b.name);});

function fill(sel,v){sel.innerHTML='';members.forEach(function(m){var o=document.createElement('option');o.value=m.iso;o.textContent=m.name+' ('+m.iso+')';sel.appendChild(o);});sel.value=v;}

var charts={};
function kill(k){if(charts[k]){charts[k].destroy();charts[k]=null;}}

/* ---------- tab 1 ---------- */
function renderCompare(){
  var a=$('selA').value,b=$('selB').value,na=nm(a),nb=nm(b);
  if(a===b){$('res1').hidden=true;$('sameMsg').hidden=false;$('sameMsg').textContent='State A and State B are the same ('+na+'). Pick two different States.';return;}
  $('sameMsg').hidden=true;$('res1').hidden=false;
  var rows=[];
  filt().forEach(function(r){var v=r.votes||{};if(v[a]&&v[b])rows.push({r:r,va:v[a],vb:v[b],same:v[a]===v[b]});});
  var j=rows.length,s=rows.filter(function(x){return x.same;}).length;
  $('sJoint').textContent=j;
  $('sSame').textContent=j?s+' ('+Math.round(100*s/j)+'%)':'0';
  $('sDiff').textContent=j-s;
  $('howStats').textContent='How this is computed: for each recorded vote ('+kindText($('selKind').value)+') where both States appear in the roll call, their codes Y/N/A are compared; an abstention counts as a choice of its own. Exact counts, not estimates.';
  // timeline
  var by={};rows.forEach(function(x){var y=yr(x.r);if(y==null)return;by[y]=by[y]||{j:0,s:0};by[y].j++;if(x.same)by[y].s++;});
  var ys=Object.keys(by).map(Number).sort(function(p,q){return p-q;});
  kill('time');
  $('timeEmpty').hidden=ys.length>0;$('cTime').parentNode.style.display=ys.length?'':'none';
  if(ys.length&&window.Chart){
    charts.time=new Chart($('cTime').getContext('2d'),{type:'bar',data:{labels:ys.map(String),datasets:[
      {label:'Joint votes',data:ys.map(function(y){return by[y].j;}),backgroundColor:'#9b2335'},
      {label:'Voted the same',data:ys.map(function(y){return by[y].s;}),backgroundColor:'#d9a9b0'}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom'},tooltip:{callbacks:{afterBody:function(c){var e=by[ys[c[0].dataIndex]];return Math.round(100*e.s/e.j)+'% the same';}}}},
        scales:{y:{beginAtZero:true,ticks:{precision:0},grid:{display:false}},x:{grid:{display:false}}}}});
  }
  $('howTime').textContent='How this is computed: joint votes grouped by the year of each vote; the lighter bar is how many of them were cast the same way. Hover for the percentage.';
  // list
  var all=$('selList').value==='all';
  var list=all?rows.slice():rows.filter(function(x){return !x.same;});
  list.sort(function(p,q){var x=p.r.date||'',y=q.r.date||'';return x===y?0:(x<y?1:-1);});
  $('listTitle').textContent=all?'All joint votes ('+list.length+')':'Votes where '+na+' and '+nb+' differed ('+list.length+')';
  $('howList').textContent='Most recent first. Symbols link to the UN document in a new tab. A warning marks records where the official totals differ from the roll call; both are shown.';
  $('thA').textContent=na;$('thB').textContent=nb;
  var tb=$('tbody');tb.innerHTML='';
  list.forEach(function(x){
    var r=x.r,link=r.doc_url||r.record_url||'',m=mism(r);
    var sym=r.symbol?(link?'<a href="'+esc(link)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol)):'—';
    var tr=document.createElement('tr');
    tr.innerHTML='<td class="v">'+esc(r.date||'—')+'</td><td>'+esc(r.title||'(untitled)')+'<br><span class="hint">'+sym+' · '+esc(r.kind||'')+'</span>'+
      (m?'<span class="warn">⚠ official totals '+r.yes+'/'+r.no+'/'+r.abstain+' (yes/no/abstain) ≠ roll call '+m.Y+'/'+m.N+'/'+m.A+'</span>':'')+'</td>'+
      '<td class="v">'+esc(VL[x.va]||x.va)+'</td><td class="v">'+esc(VL[x.vb]||x.vb)+'</td>';
    tb.appendChild(tr);
  });
  $('emptyList').hidden=list.length>0;$('emptyList').textContent='No votes to show for this choice.';
}

/* ---------- tab 2 ---------- */
var valueLabels={id:'valueLabels',afterDatasetsDraw:function(ch){
  var ex=ch.config.options.extra||[],meta=ch.getDatasetMeta(0),c=ch.ctx;
  c.save();c.fillStyle='#1d1b18';c.font='12px ui-monospace,Menlo,Consolas,monospace';c.textBaseline='middle';
  meta.data.forEach(function(bar,i){if(ex[i])c.fillText(ex[i],bar.x+6,bar.y);});c.restore();}};
function bars(key,boxId,canvasId,list){
  kill(key);var box=$(boxId);box.style.height=Math.max(60,list.length*28+30)+'px';
  if(!window.Chart||!list.length)return;
  charts[key]=new Chart($(canvasId).getContext('2d'),{type:'bar',plugins:[valueLabels],
    data:{labels:list.map(function(x){return x.name;}),datasets:[{data:list.map(function(x){return Math.round(1000*x.share)/10;}),backgroundColor:'#9b2335',barThickness:16}]},
    options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,layout:{padding:{right:130}},
      extra:list.map(function(x){return(Math.round(1000*x.share)/10)+'% · '+x.joint+' votes';}),
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){var x=list[c.dataIndex];return x.same+' of '+x.joint+' shared votes the same';}}}},
      scales:{x:{min:0,max:100,display:false},y:{grid:{display:false},ticks:{font:{size:13}}}}}});
}
function renderRank(){
  var a=$('selA').value,na=nm(a),acc={};
  var f=filt();
  f.forEach(function(r){var v=r.votes||{},va=v[a];if(!va)return;
    for(var i in v){if(i===a)continue;var e=acc[i]||(acc[i]={joint:0,same:0});e.joint++;if(v[i]===va)e.same++;}});
  var all=Object.keys(acc).map(function(i){var e=acc[i];return{iso:i,name:nm(i),joint:e.joint,same:e.same,share:e.joint?e.same/e.joint:0};});
  var ok=all.filter(function(x){return x.joint>=MIN;});
  var cut=all.length-ok.length;
  $('rTitle').textContent='Who votes with '+na+'?';
  $('rEmpty').hidden=ok.length>0;$('rWrap').hidden=ok.length===0;
  if(!ok.length){kill('close');kill('far');$('rEmpty').textContent='No other State shared at least '+MIN+' votes with '+na+' in this filter ('+kindText($('selKind').value)+').';return;}
  function cmpHi(p,q){return q.share-p.share||q.joint-p.joint||p.name.localeCompare(q.name);}
  var hi=ok.slice().sort(cmpHi).slice(0,TOP);
  var used={};hi.forEach(function(x){used[x.iso]=1;});
  var lo=ok.slice().sort(function(p,q){return p.share-q.share||q.joint-p.joint||p.name.localeCompare(q.name);}).filter(function(x){return !used[x.iso];}).slice(0,TOP);
  bars('close','boxClose','cClose',hi);bars('far','boxFar','cFar',lo);
  $('rCut').textContent='Left out: '+cut+' State'+(cut===1?'':'s')+' with fewer than '+MIN+' shared votes with '+na+'. '+ok.length+' State'+(ok.length===1?' is':'s are')+' ranked'+(ok.length<2*TOP?'; with fewer than '+(2*TOP)+' ranked, a State appears only in the closest chart if it would qualify for both.':'.');
  $('rHow').textContent='How this is computed: for every recorded vote ('+kindText($('selKind').value)+') in which '+na+' and another State both appear in the roll call, agreement is 1 if both cast the same code (Yes, No or Abstain) and 0 otherwise; share = agreements ÷ shared votes. Ties are ordered by more shared votes, then by name.';
  $('rLeaves').textContent='What it leaves out: texts adopted without a vote, which are not in this data. Abstention is treated as a choice of its own, so two abstentions count as agreement although they may hide different reasons, and Yes against Abstain counts as disagreement although the two States are not opposed. States are compared only on votes from the years both were members.';
}

/* ---------- shell ---------- */
function render(){
  var t2=$('tab2').getAttribute('aria-selected')==='true';
  $('p1').hidden=t2;$('p2').hidden=!t2;
  $('fieldB').hidden=t2;$('fieldList').hidden=t2;
  $('lblA').textContent=t2?'State A (first State)':'State A';
  if(t2)renderRank();else renderCompare();
}
function selectTab(n){
  [$('tab1'),$('tab2')].forEach(function(t,i){var on=i===n;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;});
  render();[$('tab1'),$('tab2')][n].focus();
}
$('tab1').onclick=function(){selectTab(0);};
$('tab2').onclick=function(){selectTab(1);};
document.querySelector('[role=tablist]').addEventListener('keydown',function(e){
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'||e.key==='Home'||e.key==='End'){
    e.preventDefault();var cur=$('tab2').getAttribute('aria-selected')==='true'?1:0;
    selectTab(e.key==='Home'?0:e.key==='End'?1:(cur+1)%2);}
});
['selA','selB','selKind','selList'].forEach(function(i){$(i).addEventListener('change',render);});

function main(){
  var ys=recs.map(yr).filter(function(y){return y!=null;});
  $('sourceLine').textContent=(H.title||'Human Rights Council recorded votes')+' · n = '+recs.length+' recorded votes · '+(ys.length?Math.min.apply(null,ys)+'–'+Math.max.apply(null,ys):'years n/a')+' · only States that appear in at least one roll call can be picked';
  if(recs.length===0||members.length<2){
    document.querySelector('.controls').hidden=true;$('p1').hidden=true;
    $('fatal').hidden=false;$('fatal').textContent='The loaded data has too few recorded votes or States to compare.';return;
  }
  var uc=D.uhri&&D.uhri.country,m=members.filter(function(x){return x.name===uc;})[0];
  var a=(m||members[0]).iso;
  var b=members.filter(function(x){return x.iso!==a;})[0].iso;
  fill($('selA'),a);fill($('selB'),b);
  render();
}
main();
})();
</script>
</body>
</html>
```