I built a Kenya dashboard with the record count and year span at the top, filters for mechanism, body, year range, SDG and keyword, a top-10 themes chart, and a table where clicking a row shows the full text. The country name and all counts are read from the data, and every number updates with the filters.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UN human rights recommendations dashboard</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#f5f7fa;color:#1d2733}
main{max-width:1150px;margin:0 auto;padding:28px 20px 60px}
h1{margin:0 0 4px;font-size:28px}
h2{font-size:20px;margin:0 0 6px}
.desc{color:#4a5a6a;margin:0 0 20px}
.card{background:#fff;border:1px solid #dde4ec;border-radius:8px;padding:18px 20px;margin-bottom:20px}
.note{font-size:14px;color:#5b6b7b;margin:8px 0 0}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
label{display:block;font-size:14px;font-weight:600;color:#33475b}
select,input{width:100%;padding:8px;font-size:16px;border:1px solid #b9c5d1;border-radius:5px;background:#fff;margin-top:4px}
.yr{display:flex;gap:6px}
.big{font-size:34px;font-weight:700;color:#1f6fb2;line-height:1.1}
.stats{display:flex;gap:40px;flex-wrap:wrap}
.stats div span{display:block;font-size:14px;color:#5b6b7b}
button{background:#1f6fb2;color:#fff;border:0;border-radius:5px;padding:8px 14px;font-size:15px;cursor:pointer}
table{width:100%;border-collapse:collapse;table-layout:fixed}
th{text-align:left;font-size:14px;color:#33475b;border-bottom:2px solid #dde4ec;padding:8px}
td{padding:8px;border-bottom:1px solid #eef1f5;vertical-align:top;overflow-wrap:anywhere}
tr.row{cursor:pointer}
tr.row:hover{background:#f0f6fc}
tr.full td{background:#f8fafc;white-space:pre-wrap}
a{color:#1f6fb2}
.chartbox{position:relative;height:380px}
.pager{display:flex;gap:10px;align-items:center;margin-top:12px}
mark{background:#ffe9a8}
</style>
</head>
<body>
<main>
<h1 id="title"></h1>
<p class="desc" id="desc"></p>

<div class="card">
<div class="stats">
<div><div class="big" id="nAll"></div><span>records in total</span></div>
<div><div class="big" id="nMatch"></div><span>records match the current filters</span></div>
<div><div class="big" id="years"></div><span>years covered (all records)</span></div>
</div>
<p class="note">How this is computed: each record is one paragraph of a UN document. Totals are simple counts of the records loaded; "match" counts the records that pass every filter below.</p>
</div>

<div class="card">
<div class="filters">
<label>Mechanism<select id="fMech"></select></label>
<label>Treaty body or mandate<select id="fBody"></select></label>
<label>Year range
<div class="yr"><select id="fFrom"></select><select id="fTo"></select></div></label>
<label>SDG<select id="fSdg"></select></label>
<label>Keyword search<input id="fKw" type="search" placeholder="e.g. detention"></label>
</div>
<p class="note">Filters combine (all must match). The keyword search looks for the typed text anywhere in the paragraph, ignoring capitals. <button id="reset" style="margin-left:8px">Reset filters</button></p>
</div>

<div class="card">
<h2>10 most frequent themes</h2>
<div class="chartbox"><canvas id="chart"></canvas></div>
<p class="note" id="chartNote"></p>
</div>

<div class="card">
<h2>Matching records</h2>
<table>
<thead><tr><th style="width:105px">Date</th><th style="width:130px">Body</th><th style="width:200px">Symbol</th><th>First line of text</th></tr></thead>
<tbody id="tb"></tbody>
</table>
<div class="pager"><button id="more">Show more</button><span id="shown"></span></div>
<p class="note">How this is computed: records are sorted by date, newest first. The first line is the start of the paragraph (up to 160 characters). Click a row to show or hide the full, unaltered text. The symbol links to the UN document in a new tab.</p>
</div>
</main>

<script>
(function(){
var D=(window.WORKSHOP_DATA&&WORKSHOP_DATA.uhri)||{};
var all=(D.records||[]).slice().sort(function(a,b){return (b.date||"").localeCompare(a.date||"")});
var sdgNames=D.sdg_names||{};
var $=function(id){return document.getElementById(id)};
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
var country=D.country||"the selected country";
$("title").textContent="UN human rights recommendations and observations: "+country;
var ys=all.map(function(r){return r.year}).filter(function(y){return typeof y==="number"});
var minY=ys.length?Math.min.apply(null,ys):null,maxY=ys.length?Math.max.apply(null,ys):null;
$("desc").textContent=(D.title||"UN recommendations")+" — source: "+(D.source||"UHRI")+"; n = "+all.length+" paragraphs"+(minY!==null?", "+minY+"–"+maxY:"")+".";
$("nAll").textContent=all.length;
$("years").textContent=minY!==null?(minY===maxY?minY:minY+"–"+maxY):"n/a";

function uniq(a){return Array.from(new Set(a)).filter(Boolean).sort()}
function fill(sel,vals,first,labelFn){
 sel.innerHTML='<option value="">'+first+'</option>'+vals.map(function(v){return '<option value="'+esc(v)+'">'+esc(labelFn?labelFn(v):v)+'</option>'}).join("")}
fill($("fMech"),uniq(all.map(function(r){return r.mechanism})),"All mechanisms");
fill($("fBody"),uniq(all.map(function(r){return r.body})),"All bodies / mandates");
var sd=uniq([].concat.apply([],all.map(function(r){return (r.sdgs||[]).map(String)}))).sort(function(a,b){return a-b});
fill($("fSdg"),sd,"All SDGs",function(v){return "SDG "+v+(sdgNames[v]?": "+sdgNames[v]:"")});
var yl=[];if(minY!==null)for(var y=minY;y<=maxY;y++)yl.push(y);
fill($("fFrom"),yl,"From");fill($("fTo"),yl,"To");

var chart=null,cur=[],limit=50;
function filtered(){
 var m=$("fMech").value,b=$("fBody").value,s=$("fSdg").value,f=+$("fFrom").value||-Infinity,t=+$("fTo").value||Infinity,k=$("fKw").value.trim().toLowerCase();
 return all.filter(function(r){
  if(m&&r.mechanism!==m)return false;
  if(b&&r.body!==b)return false;
  if(s&&(r.sdgs||[]).map(String).indexOf(s)<0)return false;
  if(typeof r.year==="number"&&(r.year<f||r.year>t))return false;
  if(typeof r.year!=="number"&&(f>-Infinity||t<Infinity))return false;
  if(k&&(r.text||"").toLowerCase().indexOf(k)<0)return false;
  return true});
}
function update(){
 cur=filtered();limit=50;
 $("nMatch").textContent=cur.length;
 drawChart();drawTable();
}
function drawChart(){
 var c={};
 cur.forEach(function(r){(r.themes||[]).forEach(function(t){c[t]=(c[t]||0)+1})});
 var top=Object.keys(c).map(function(k){return [k,c[k]]}).sort(function(a,b){return b[1]-a[1]}).slice(0,10);
 $("chartNote").textContent="How this is computed: for the "+cur.length+" matching records, each theme tag is counted once per record (a record can have several themes, so bars add up to more than the record count). "+(top.length?"":"No themes to show for this filter.");
 if(chart)chart.destroy();
 chart=new Chart($("chart"),{type:"bar",
  data:{labels:top.map(function(x){return x[0]}),datasets:[{label:"Records",data:top.map(function(x){return x[1]}),backgroundColor:"#1f6fb2"}]},
  options:{indexAxis:"y",maintainAspectRatio:false,animation:false,plugins:{legend:{display:false}},scales:{x:{beginAtZero:true,ticks:{precision:0,font:{size:13}},title:{display:true,text:"Number of records"}},y:{ticks:{font:{size:13}}}}}});
}
function first(t){t=(t||"").replace(/\s+/g," ").trim();return t.length>160?t.slice(0,160)+"…":t}
function drawTable(){
 var rows=cur.slice(0,limit),h="";
 rows.forEach(function(r,i){
  h+='<tr class="row" data-i="'+i+'"><td>'+esc(r.date||r.year||"")+'</td><td>'+esc(r.body||"")+'</td><td>'+
   (r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol))+
   '</td><td>'+esc(first(r.text))+'</td></tr>';
 });
 if(!rows.length)h='<tr><td colspan="4">No records match these filters.</td></tr>';
 $("tb").innerHTML=h;
 $("shown").textContent="Showing "+rows.length+" of "+cur.length;
 $("more").style.display=cur.length>limit?"":"none";
}
$("tb").addEventListener("click",function(e){
 if(e.target.tagName==="A")return;
 var tr=e.target.closest("tr.row");if(!tr)return;
 var nx=tr.nextElementSibling;
 if(nx&&nx.classList.contains("full")){nx.remove();return}
 var r=cur[+tr.dataset.i];
 var x=document.createElement("tr");x.className="full";
 var meta=[r.mechanism,r.type,r.section].filter(Boolean).join(" · ");
 x.innerHTML='<td colspan="4"><small>'+esc(meta)+'</small><br>'+esc(r.text)+
  ((r.themes||[]).length?'<br><small>Themes: '+esc(r.themes.join("; "))+'</small>':'')+'</td>';
 tr.after(x);
});
$("more").onclick=function(){limit+=50;drawTable()};
["fMech","fBody","fSdg","fFrom","fTo"].forEach(function(id){$(id).addEventListener("change",update)});
$("fKw").addEventListener("input",update);
$("reset").onclick=function(){["fMech","fBody","fSdg","fFrom","fTo","fKw"].forEach(function(id){$(id).value=""});update()};
update();
})();
</script>
</body>
</html>
```