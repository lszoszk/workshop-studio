I added a "Suggest SDGs with AI" card that sends the first 50 records of the current filter to the model in batches of 25, with a progress line and a Stop button. "Run again" re-sends the same 50 records and adds a column, so runs sit side by side. The app is not told the model's name, so the notice says so rather than guessing.

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
button:disabled{background:#9db4c8;cursor:not-allowed}
button.sec{background:#fff;color:#1f6fb2;border:1px solid #1f6fb2}
table{width:100%;border-collapse:collapse;table-layout:fixed}
th{text-align:left;font-size:14px;color:#33475b;border-bottom:2px solid #dde4ec;padding:8px}
td{padding:8px;border-bottom:1px solid #eef1f5;vertical-align:top;overflow-wrap:anywhere}
tr.row{cursor:pointer}
tr.row:hover{background:#f0f6fc}
tr.full td{background:#f8fafc;white-space:pre-wrap}
a{color:#1f6fb2}
.chartbox{position:relative;height:380px}
.pager{display:flex;gap:10px;align-items:center;margin-top:12px}
.warn{background:#fff6e0;border:1px solid #e8c766;border-radius:6px;padding:12px 14px;margin:0 0 14px;font-size:15px}
.ok{color:#1b7a3d;font-weight:600}.mid{color:#9a6a00;font-weight:600}.bad{color:#b3261e;font-weight:600}
.chip{display:inline-block;background:#e8f1f9;border-radius:10px;padding:0 8px;margin:1px 2px 1px 0;font-size:14px}
.btns{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
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
<h2>AI check of the UN's SDG tags</h2>
<div class="warn" id="aiNotice"></div>
<div class="btns">
<button id="aiGo">Suggest SDGs with AI</button>
<button id="aiAgain" class="sec" disabled>Run again</button>
<button id="aiStop" class="sec" style="display:none">Stop</button>
<span id="aiProg"></span>
</div>
<div id="aiRates"></div>
<div id="aiOut"></div>
<p class="note">How this is computed: the AI is asked which SDG numbers (1–17) each paragraph would get. Our code then compares them with the SDGs tagged in the UN data. <b>Agree</b> = exactly the same set of numbers (two empty sets also count as agreeing). <b>Partly</b> = at least one number in common but not identical. <b>Differ</b> = no number in common. Records the model did not answer are left out of the rate. Everything in blue-bordered "AI" cells comes from the model, not from the UN; it is a suggestion, not a classification.</p>
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
 drawChart();drawTable();noticeIdle();
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
function expander(tbody,getRec,cols){
 tbody.addEventListener("click",function(e){
  if(e.target.tagName==="A")return;
  var tr=e.target.closest("tr.row");if(!tr)return;
  var nx=tr.nextElementSibling;
  if(nx&&nx.classList.contains("full")){nx.remove();return}
  var r=getRec(+tr.dataset.i);if(!r)return;
  var x=document.createElement("tr");x.className="full";
  var meta=[r.mechanism,r.type,r.section].filter(Boolean).join(" · ");
  x.innerHTML='<td colspan="'+cols()+'"><small>'+esc(meta)+'</small><br>'+esc(r.text)+
   ((r.themes||[]).length?'<br><small>Themes: '+esc(r.themes.join("; "))+'</small>':'')+'</td>';
  tr.after(x);
 });
}
expander($("tb"),function(i){return cur[i]},function(){return 4});
$("more").onclick=function(){limit+=50;drawTable()};
["fMech","fBody","fSdg","fFrom","fTo"].forEach(function(id){$(id).addEventListener("change",update)});
$("fKw").addEventListener("input",update);
$("reset").onclick=function(){["fMech","fBody","fSdg","fFrom","fTo","fKw"].forEach(function(id){$(id).value=""});update()};

/* ---------- AI SDG suggestions ---------- */
var runs=[],aiRecs=[],busy=false,stopFlag=false;
function modelName(){
 var s=window.studio||{};
 return s.model||s.modelName||null;
}
function noticeText(n){
 var m=modelName();
 return '<b>Before you run this:</b> the text of '+n+' paragraph'+(n===1?'':'s')+' (the first 50 of the current filter at most) will be <b>sent outside your browser to an external language model</b>, in batches of 25. '+
  'Model: '+(m?esc(m):'the workshop\'s language model, reached through <code>studio.ask</code>; this page is not told its name or version')+'. '+
  '<b>Running it again can give different answers</b>, so treat results as suggestions and compare runs.';
}
function noticeIdle(){
 if(busy||runs.length)return;
 $("aiNotice").innerHTML=noticeText(Math.min(50,cur.length));
 $("aiGo").disabled=!cur.length;
}
function sdgSet(a){return Array.from(new Set((a||[]).map(Number).filter(function(n){return n>=1&&n<=17}))).sort(function(a,b){return a-b})}
function relation(un,ai){
 if(ai==null)return null;
 var a=sdgSet(un),b=ai;
 if(a.length===b.length&&a.every(function(v,i){return v===b[i]}))return "agree";
 return a.some(function(v){return b.indexOf(v)>=0})?"partly":"differ";
}
function parseAnswer(s){
 var out={};
 if(typeof s!=="string")return out;
 var t=s.replace(/```json|```/g,"").trim(),j=null;
 try{j=JSON.parse(t)}catch(e){
  var a=t.indexOf("{"),b=t.lastIndexOf("}");
  if(a>=0&&b>a){try{j=JSON.parse(t.slice(a,b+1))}catch(e2){}}
  if(j==null){a=t.indexOf("[");b=t.lastIndexOf("]");if(a>=0&&b>a){try{j=JSON.parse(t.slice(a,b+1))}catch(e3){}}}
 }
 if(j==null)return out;
 if(Array.isArray(j)){
  j.forEach(function(o){if(o&&o.id!=null){var v=o.sdgs||o.sdg||o.SDGs||[];out[o.id]=sdgSet([].concat(v))}});
 }else if(typeof j==="object"){
  var src=j.results&&typeof j.results==="object"?j.results:j;
  if(Array.isArray(src)){return parseAnswer(JSON.stringify(src))}
  Object.keys(src).forEach(function(k){var v=src[k];if(v&&!Array.isArray(v)&&typeof v==="object")v=v.sdgs||v.sdg||[];out[k]=sdgSet([].concat(v==null?[]:v))});
 }
 return out;
}
async function runAI(recs){
 busy=true;stopFlag=false;
 $("aiGo").disabled=true;$("aiAgain").disabled=true;$("aiStop").style.display="";
 var run={answers:{},errors:0,stopped:false,at:new Date()};
 var goals=Object.keys(sdgNames).length?Object.keys(sdgNames).sort(function(a,b){return a-b}).map(function(k){return k+" = "+sdgNames[k]}).join("; "):"the 17 UN Sustainable Development Goals";
 var batches=Math.ceil(recs.length/25);
 for(var b=0;b<batches;b++){
  if(stopFlag){run.stopped=true;break}
  $("aiProg").textContent="Run "+(runs.length+1)+": batch "+(b+1)+" of "+batches+" … ("+Object.keys(run.answers).length+" of "+recs.length+" records answered)";
  var chunk=recs.slice(b*25,b*25+25);
  var payload=chunk.map(function(r){return {id:r.id,text:(r.text||"").slice(0,1200)}});
  var prompt='You are helping a human rights analyst. For each UN paragraph below, decide which Sustainable Development Goals (numbers 1 to 17) it relates to. Goals: '+goals+'. '+
   'Assign only goals clearly relevant to the paragraph; use an empty list if none. Return ONLY a JSON object mapping each record id to an array of goal numbers, for example {"id-1":[16,5],"id-2":[]}. Records: '+JSON.stringify(payload);
  try{
   var ans=await studio.ask(prompt,{json:true});
   var p=parseAnswer(ans);
   chunk.forEach(function(r){if(Object.prototype.hasOwnProperty.call(p,r.id))run.answers[r.id]=p[r.id]});
   if(!Object.keys(p).length)run.errors++;
  }catch(e){run.errors++}
 }
 runs.push(run);
 busy=false;$("aiStop").style.display="none";$("aiGo").disabled=false;$("aiAgain").disabled=false;
 $("aiProg").textContent=run.stopped?"Stopped. Partial results shown.":(run.errors?"Done, but "+run.errors+" batch(es) failed or could not be read.":"Done.");
 renderAI();
}
function chips(a){return a.length?a.map(function(n){return '<span class="chip" title="'+esc(sdgNames[n]||"")+'">'+n+'</span>'}).join(""):'<span style="color:#7a8896">none</span>'}
function renderAI(){
 var n=aiRecs.length;
 $("aiNotice").innerHTML=noticeText(n)+' <br>Sent so far: <b>'+n+'</b> texts per run, <b>'+runs.length+'</b> run'+(runs.length===1?'':'s')+'.';
 var rh="";
 runs.forEach(function(run,k){
  var c={agree:0,partly:0,differ:0,none:0};
  aiRecs.forEach(function(r){var rel=relation(r.sdgs,run.answers[r.id]);c[rel||"none"]++});
  var done=c.agree+c.partly+c.differ;
  rh+='<p style="margin:4px 0"><span class="big" style="font-size:28px">'+(done?Math.round(100*c.agree/done)+'%':'n/a')+'</span> '+
   '<b>Run '+(k+1)+'</b>: exact agreement with the UN tags in '+c.agree+' of '+done+' answered records ('+c.partly+' partly, '+c.differ+' differ'+(c.none?'; '+c.none+' not answered':'')+').</p>';
 });
 if(runs.length>1){
  var same=0,both=0;
  aiRecs.forEach(function(r){var a=runs[0].answers[r.id],b=runs[runs.length-1].answers[r.id];
   if(a&&b){both++;if(a.length===b.length&&a.every(function(v,i){return v===b[i]}))same++}});
  rh+='<p style="margin:4px 0">Run 1 and run '+runs.length+' gave identical suggestions for '+same+' of '+both+' records answered in both.</p>';
 }
 $("aiRates").innerHTML=rh;
 var th='<th style="width:30%">Record</th><th style="width:110px">UN SDGs</th>';
 runs.forEach(function(_,k){th+='<th>AI run '+(k+1)+' SDGs</th><th style="width:80px">Run '+(k+1)+'</th>'});
 var h='<table><thead><tr>'+th+'</tr></thead><tbody id="aiTb">';
 aiRecs.forEach(function(r,i){
  h+='<tr class="row" data-i="'+i+'"><td>'+(r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol))+
   '<br><small>'+esc(r.body||"")+' · '+esc(r.date||"")+'</small><br><small>'+esc(first(r.text).slice(0,90))+'</small></td><td>'+chips(sdgSet(r.sdgs))+'</td>';
  runs.forEach(function(run){
   var a=run.answers[r.id],rel=relation(r.sdgs,a);
   h+='<td data-source="ai" style="border-left:3px solid #1f6fb2">'+(a==null?'<span style="color:#7a8896">no answer</span>':chips(a))+'</td><td>'+
    (rel==="agree"?'<span class="ok">Agree</span>':rel==="partly"?'<span class="mid">Partly</span>':rel==="differ"?'<span class="bad">Differ</span>':'–')+'</td>';
  });
  h+='</tr>';
 });
 h+='</tbody></table>';
 $("aiOut").innerHTML=h;
 expander($("aiTb"),function(i){return aiRecs[i]},function(){return 2+2*runs.length});
}
$("aiGo").onclick=function(){
 if(busy||!cur.length)return;
 aiRecs=cur.slice(0,50);runs=[];
 $("aiRates").innerHTML="";$("aiOut").innerHTML="";
 $("aiNotice").innerHTML=noticeText(aiRecs.length);
 runAI(aiRecs);
};
$("aiAgain").onclick=function(){if(busy||!aiRecs.length)return;runAI(aiRecs)};
$("aiStop").onclick=function(){stopFlag=true;$("aiProg").textContent="Stopping after the current batch …"};
update();
})();
</script>
</body>
</html>
```