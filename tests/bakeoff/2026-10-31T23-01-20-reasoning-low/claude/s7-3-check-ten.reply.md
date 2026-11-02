I added a "Check 10 at random" panel that draws up to 10 records from the current filter, shows each full text with its UN-assigned SDGs, and lets you mark every SDG right, wrong or arguable. When all are marked it shows the agreement rate, lists the wrong and arguable examples, and offers a CSV download. "Draw again" makes a new draw.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UN human rights recommendations dashboard</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#f5f8fb;color:#1c2733}
header,main{max-width:1200px;margin:0 auto;padding:0 20px}
header{padding-top:24px}
h1{margin:0 0 4px;font-size:28px;color:#1f6fb2}
.desc{color:#4a5a6a;margin:0 0 16px}
.card{background:#fff;border:1px solid #dce5ee;border-radius:8px;padding:16px 20px;margin-bottom:20px}
.stats{display:flex;gap:32px;flex-wrap:wrap}
.stat b{display:block;font-size:30px;color:#1f6fb2}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
label{font-size:14px;font-weight:600;display:block}
select,input{width:100%;font:inherit;padding:6px 8px;border:1px solid #b9c7d5;border-radius:4px;background:#fff}
.yr{display:flex;gap:6px}
.note{font-size:14px;color:#556677;margin-top:10px}
table{width:100%;border-collapse:collapse;table-layout:fixed}
th,td{text-align:left;padding:8px;border-bottom:1px solid #e4ebf2;vertical-align:top;overflow-wrap:anywhere}
th{font-size:14px;color:#334}
tr.row{cursor:pointer}
tr.row:hover{background:#eef5fb}
tr.full td{background:#f7fafd;white-space:pre-wrap}
a{color:#1f6fb2}
button{font:inherit;padding:6px 14px;border:1px solid #1f6fb2;background:#1f6fb2;color:#fff;border-radius:4px;cursor:pointer}
button.sec{background:#fff;color:#1f6fb2}
button:disabled{opacity:.4;cursor:default}
.pager{display:flex;gap:12px;align-items:center;margin-top:12px}
.chartbox{position:relative;height:380px}
.chk{border:1px solid #dce5ee;border-radius:6px;padding:12px 16px;margin:12px 0;background:#fbfdff}
.chk .txt{white-space:pre-wrap;background:#f3f7fb;padding:8px 10px;border-radius:4px;margin:8px 0}
.sdgrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:6px 0}
.sdgname{flex:1 1 280px;font-size:15px}
.mk button{background:#fff;color:#334;border-color:#b9c7d5;padding:4px 10px;margin-right:4px}
.mk button.on.right{background:#2e7d32;color:#fff;border-color:#2e7d32}
.mk button.on.wrong{background:#c62828;color:#fff;border-color:#c62828}
.mk button.on.arguable{background:#e08a00;color:#fff;border-color:#e08a00}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.result{border-left:4px solid #1f6fb2;padding:8px 14px;background:#eef5fb;margin-top:14px}
</style>
</head>
<body>
<header>
<h1 id="title">Recommendations</h1>
<p class="desc" id="desc"></p>
</header>
<main>
<div class="card"><div class="stats" id="stats"></div></div>

<div class="card">
<div class="filters">
<div><label for="fMech">Mechanism</label><select id="fMech"></select></div>
<div><label for="fBody">Treaty body or mandate</label><select id="fBody"></select></div>
<div><label>Year range</label><div class="yr"><select id="fFrom" aria-label="From year"></select><select id="fTo" aria-label="To year"></select></div></div>
<div><label for="fSdg">SDG</label><select id="fSdg"></select></div>
<div><label for="fQ">Keyword search</label><input id="fQ" type="search" placeholder="e.g. refugees"></div>
</div>
<p class="note" id="filterNote"></p>
</div>

<div class="card">
<h2 style="margin-top:0">Spot check: are the UN index's SDG tags right?</h2>
<div class="bar"><button id="draw">Check 10 at random</button><button id="again" class="sec" style="display:none">Draw again</button><span class="note" id="drawInfo" style="margin:0"></span></div>
<div id="checkArea"></div>
<p class="note"><b>How this is computed:</b> your code-drawn sample is a random selection (without replacement) of up to 10 records from the current filter. Each SDG tag shown is the one stored in the data (assigned by the UN index, not by this tool). The marks are yours. Agreement rate = SDG tags marked "right" ÷ all SDG tags marked, over the sample. "Arguable" counts as not agreeing. Records with no SDG tags are shown but need no marks and are not in the rate.</p>
</div>

<div class="card">
<h2 style="margin-top:0">10 most frequent themes (current filter)</h2>
<div class="chartbox"><canvas id="chart"></canvas></div>
<p class="note"><b>How this is computed:</b> each record can carry several themes; every theme is counted once per matching record. Records without themes are not counted in the chart. Only the 10 highest counts are shown.</p>
</div>

<div class="card">
<h2 style="margin-top:0">Matching records</h2>
<p class="note" id="tableNote" style="margin-top:0"></p>
<table>
<colgroup><col style="width:105px"><col style="width:130px"><col style="width:200px"><col></colgroup>
<thead><tr><th>Date</th><th>Body</th><th>Symbol (UN document)</th><th>First line of text (click row for full text)</th></tr></thead>
<tbody id="tbody"></tbody>
</table>
<div class="pager"><button id="prev">Previous</button><span id="pageInfo"></span><button id="next">Next</button></div>
<p class="note"><b>How this is computed:</b> records are filtered by all choices above together (a record must match every one), then sorted by date, newest first. Keyword search looks for the typed words anywhere in the full text (case-insensitive, all words must appear). The first line is the text up to the first sentence end, shortened to 200 characters.</p>
</div>
</main>
<script>
(function(){
var D=(window.WORKSHOP_DATA||{}).uhri||{};
var recs=Array.isArray(D.records)?D.records:[];
var sdgNames=D.sdg_names||{};
var PAGE=25,page=0,chart=null,open={};
var sample=[],marks={};
function $(i){return document.getElementById(i)}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function uniq(a){return Array.from(new Set(a)).filter(function(x){return x!==""&&x!=null})}

var country=D.country||"the selected country";
$("title").textContent="UN human rights recommendations and observations: "+country;
var years=recs.map(function(r){return r.year}).filter(function(y){return typeof y==="number"});
var minY=years.length?Math.min.apply(null,years):null,maxY=years.length?Math.max.apply(null,years):null;
$("desc").textContent="Source: "+(D.source||"UHRI")+" ("+(D.title||"")+"). "+recs.length+" paragraphs from UN documents, "+(minY!==null?minY+"–"+maxY:"years unknown")+"."+(D.built?" Data built "+D.built+".":"");

function fill(sel,opts,first){
  sel.innerHTML="";
  var o=document.createElement("option");o.value="";o.textContent=first;sel.appendChild(o);
  opts.forEach(function(x){var e=document.createElement("option");e.value=x[0];e.textContent=x[1];sel.appendChild(e)});
}
fill($("fMech"),uniq(recs.map(function(r){return r.mechanism})).sort().map(function(x){return[x,x]}),"All mechanisms");
var sdgs=uniq([].concat.apply([],recs.map(function(r){return r.sdgs||[]}))).sort(function(a,b){return a-b});
fill($("fSdg"),sdgs.map(function(g){return[String(g),"SDG "+g+(sdgNames[g]?": "+sdgNames[g]:"")]}),"All SDGs");
var yl=[];if(minY!==null)for(var y=minY;y<=maxY;y++)yl.push([String(y),String(y)]);
fill($("fFrom"),yl,"From");fill($("fTo"),yl,"To");

function refreshBodies(){
  var m=$("fMech").value,cur=$("fBody").value;
  var b=uniq(recs.filter(function(r){return !m||r.mechanism===m}).map(function(r){return r.body})).sort();
  fill($("fBody"),b.map(function(x){return[x,x]}),"All bodies / mandates");
  if(b.indexOf(cur)>=0)$("fBody").value=cur;
}
refreshBodies();

function filtered(){
  var m=$("fMech").value,b=$("fBody").value,s=$("fSdg").value;
  var f=$("fFrom").value?+$("fFrom").value:null,t=$("fTo").value?+$("fTo").value:null;
  var words=$("fQ").value.toLowerCase().split(/\s+/).filter(Boolean);
  return recs.filter(function(r){
    if(m&&r.mechanism!==m)return false;
    if(b&&r.body!==b)return false;
    if(s&&(r.sdgs||[]).map(String).indexOf(s)<0)return false;
    if(f!==null&&!(r.year>=f))return false;
    if(t!==null&&!(r.year<=t))return false;
    if(words.length){var tx=(r.text||"").toLowerCase();for(var i=0;i<words.length;i++)if(tx.indexOf(words[i])<0)return false}
    return true;
  }).sort(function(a,b){return (b.date||"").localeCompare(a.date||"")});
}
function firstLine(t){
  t=(t||"").replace(/\s+/g," ").trim();
  var m=t.match(/^.*?[.;:](\s|$)/);var s=m?m[0].trim():t;
  return s.length>200?s.slice(0,200)+"…":s;
}
function render(){
  var rows=filtered();
  var ys=rows.map(function(r){return r.year}).filter(function(y){return typeof y==="number"});
  $("stats").innerHTML=
   '<div class="stat"><b>'+recs.length+'</b>records in total</div>'+
   '<div class="stat"><b>'+(minY!==null?minY+"–"+maxY:"n/a")+'</b>years covered</div>'+
   '<div class="stat"><b>'+rows.length+'</b>match current filters'+(ys.length?' ('+Math.min.apply(null,ys)+'–'+Math.max.apply(null,ys)+')':'')+'</div>';
  var fl=[];
  if($("fMech").value)fl.push("mechanism = "+$("fMech").value);
  if($("fBody").value)fl.push("body = "+$("fBody").value);
  if($("fFrom").value||$("fTo").value)fl.push("years "+($("fFrom").value||"…")+"–"+($("fTo").value||"…"));
  if($("fSdg").value)fl.push("SDG "+$("fSdg").value);
  if($("fQ").value.trim())fl.push('keyword "'+$("fQ").value.trim()+'"');
  $("filterNote").textContent="Filters applied: "+(fl.length?fl.join("; "):"none")+". n = "+rows.length+" of "+recs.length+" records.";

  var cnt={};
  rows.forEach(function(r){(r.themes||[]).forEach(function(t){cnt[t]=(cnt[t]||0)+1})});
  var top=Object.keys(cnt).map(function(k){return[k,cnt[k]]}).sort(function(a,b){return b[1]-a[1]||a[0].localeCompare(b[0])}).slice(0,10);
  if(chart)chart.destroy();
  chart=new Chart($("chart"),{type:"bar",
   data:{labels:top.map(function(x){return x[0].length>45?x[0].slice(0,45)+"…":x[0]}),datasets:[{label:"Records",data:top.map(function(x){return x[1]}),backgroundColor:"#1f6fb2"}]},
   options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false},title:{display:!top.length,text:"No themes for the current filter"}},scales:{x:{beginAtZero:true,ticks:{precision:0},title:{display:true,text:"Number of matching records"}}}}});

  var pages=Math.max(1,Math.ceil(rows.length/PAGE));
  if(page>=pages)page=pages-1;
  var slice=rows.slice(page*PAGE,page*PAGE+PAGE);
  var h="";
  slice.forEach(function(r){
    h+='<tr class="row" data-id="'+esc(r.id)+'"><td>'+esc(r.date||r.year||"")+'</td><td>'+esc(r.body||"")+'</td><td>'+
      (r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol||""))+
      '</td><td>'+esc(firstLine(r.text))+'</td></tr>';
    if(open[r.id])h+='<tr class="full"><td colspan="4"><b>Full text</b> ('+esc(r.type||"")+(r.section?", "+esc(r.section):"")+')<br>'+esc(r.text)+'</td></tr>';
  });
  $("tbody").innerHTML=h||'<tr><td colspan="4">No records match these filters.</td></tr>';
  $("tableNote").textContent=rows.length?"Showing "+(page*PAGE+1)+"–"+(page*PAGE+slice.length)+" of "+rows.length+", newest first.":"";
  $("pageInfo").textContent="Page "+(page+1)+" of "+pages;
  $("prev").disabled=page===0;$("next").disabled=page>=pages-1;
}

/* ---- spot check ---- */
function sdgLabel(g){return "SDG "+g+(sdgNames[g]?": "+sdgNames[g]:"")}
function draw(){
  var rows=filtered().slice();
  for(var i=rows.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=rows[i];rows[i]=rows[j];rows[j]=t}
  sample=rows.slice(0,10);marks={};
  $("again").style.display="";
  $("drawInfo").textContent=sample.length?("Drew "+sample.length+" of "+rows.length+" records matching the current filter."):"";
  renderCheck();
}
function totals(){
  var tot=0,done=0,c={right:0,wrong:0,arguable:0};
  sample.forEach(function(r){(r.sdgs||[]).forEach(function(g){tot++;var m=marks[r.id+"|"+g];if(m){done++;c[m]++}})});
  return{tot:tot,done:done,c:c};
}
function renderCheck(){
  var A=$("checkArea");
  if(!sample.length){A.innerHTML='<p class="note">'+(arguments.length||$("drawInfo").textContent===""?"":"")+'No records match the current filter, so nothing can be drawn.</p>';return}
  var h="";
  sample.forEach(function(r,n){
    h+='<div class="chk"><b>'+(n+1)+'. </b>'+(r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol||""))+
      ' · '+esc(r.body||"")+' · '+esc(r.date||r.year||"")+'<div class="txt">'+esc(r.text)+'</div>';
    var g=r.sdgs||[];
    if(!g.length)h+='<div class="note">The UN index assigned no SDGs to this record. Nothing to mark.</div>';
    else{
      h+='<div><b>SDGs assigned by the UN index:</b></div>';
      g.forEach(function(x){
        var m=marks[r.id+"|"+x]||"";
        h+='<div class="sdgrow"><span class="sdgname">'+esc(sdgLabel(x))+'</span><span class="mk" data-k="'+esc(r.id+"|"+x)+'">'+
          ["right","wrong","arguable"].map(function(v){return '<button class="'+v+(m===v?' on':'')+'" data-v="'+v+'">'+v.charAt(0).toUpperCase()+v.slice(1)+'</button>'}).join("")+'</span></div>';
      });
    }
    h+='</div>';
  });
  var T=totals();
  if(T.tot===0)h+='<div class="result">None of the drawn records has SDG tags, so there is nothing to rate. Draw again.</div>';
  else if(T.done<T.tot)h+='<div class="note"><b>Progress:</b> '+T.done+' of '+T.tot+' SDG tags marked. The result appears when all are marked.</div>';
  else{
    var rate=Math.round(1000*T.c.right/T.tot)/10;
    h+='<div class="result"><b>Agreement rate: '+rate+'%</b> ('+T.c.right+' right, '+T.c.wrong+' wrong, '+T.c.arguable+' arguable, out of '+T.tot+' SDG tags in '+sample.length+' records).';
    h+='<p class="note">This is your judgement on a small random sample, not a measure for the whole dataset.</p>';
    var bad=[];
    sample.forEach(function(r){(r.sdgs||[]).forEach(function(x){var m=marks[r.id+"|"+x];if(m!=="right")bad.push([r,x,m])})});
    if(bad.length){
      h+='<b>Wrong and arguable examples</b><ul>';
      bad.forEach(function(b){h+='<li><b>'+esc(b[2])+'</b>: '+esc(sdgLabel(b[1]))+' on <a href="'+esc(b[0].doc_url||"#")+'" target="_blank" rel="noopener">'+esc(b[0].symbol)+'</a>: '+esc(firstLine(b[0].text))+'</li>'});
      h+='</ul>';
    }else h+='<p>No wrong or arguable tags in this sample.</p>';
    h+='<button id="csv">Download CSV of the '+sample.length+' records with my marks</button></div>';
  }
  A.innerHTML=h;
  var cb=$("csv");if(cb)cb.onclick=downloadCsv;
}
function q(v){return '"'+String(v==null?"":v).replace(/"/g,'""')+'"'}
function downloadCsv(){
  var lines=[["id","symbol","doc_url","date","body","text","sdg","sdg_name","my_mark"].map(q).join(",")];
  sample.forEach(function(r){
    var g=r.sdgs||[];
    if(!g.length)lines.push([r.id,r.symbol,r.doc_url,r.date,r.body,r.text,"","(no SDG assigned)",""].map(q).join(","));
    g.forEach(function(x){lines.push([r.id,r.symbol,r.doc_url,r.date,r.body,r.text,x,sdgNames[x]||"",marks[r.id+"|"+x]||""].map(q).join(","))});
  });
  var blob=new Blob(["\ufeff"+lines.join("\r\n")],{type:"text/csv;charset=utf-8"});
  var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="sdg_check_"+(D.country||"records")+".csv";
  document.body.appendChild(a);a.click();document.body.removeChild(a);
}
$("draw").onclick=draw;$("again").onclick=draw;
$("checkArea").addEventListener("click",function(e){
  var b=e.target.closest(".mk button");if(!b)return;
  var k=b.parentNode.getAttribute("data-k"),v=b.getAttribute("data-v");
  marks[k]=marks[k]===v?"":v;if(!marks[k])delete marks[k];
  var y=window.scrollY;renderCheck();window.scrollTo(0,y);
});

["fMech","fBody","fFrom","fTo","fSdg"].forEach(function(i){$(i).addEventListener("change",function(){if(i==="fMech")refreshBodies();page=0;render()})});
$("fQ").addEventListener("input",function(){page=0;render()});
$("prev").onclick=function(){page--;render()};
$("next").onclick=function(){page++;render()};
$("tbody").addEventListener("click",function(e){
  if(e.target.closest("a"))return;
  var tr=e.target.closest("tr.row");if(!tr)return;
  var id=tr.getAttribute("data-id");open[id]=!open[id];render();
});
render();
})();
</script>
</body>
</html>
```