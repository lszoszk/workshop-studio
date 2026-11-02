I added the "Suggest SDGs with AI" card below the records table. It sends the first 50 records of the current filter in two batches of 25, and "Run again" keeps every run side by side on the same 50 records. The page cannot see which model sits behind `studio.ask`, so the notice says so instead of naming one.

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
.pager,.btns{display:flex;gap:12px;align-items:center;margin-top:12px;flex-wrap:wrap}
.chartbox{position:relative;height:380px}
.warn{background:#fff6e0;border:1px solid #e8c766;border-radius:6px;padding:10px 14px;font-size:15px}
.aiwrap{overflow-x:auto}
.aiwrap table{table-layout:auto;min-width:700px}
.ok{color:#1b7a3a;font-weight:600}.part{color:#a66a00;font-weight:600}.no{color:#b3261e;font-weight:600}
.pill{display:inline-block;background:#eaf2fa;border-radius:10px;padding:0 8px;margin:1px 2px 1px 0;font-size:14px}
.pill.ai{background:#fdeede}
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

<div class="card" id="aiCard">
<h2 style="margin-top:0">Compare the UN's SDG tags with an AI's suggestions</h2>
<div class="warn" id="aiWarn"><b>Notice:</b> pressing the button sends the texts of the <b>first 50 records of the current filter</b> (in 2 batches of 25; each text cut to 1,500 characters) from your browser to an <b>external language model</b>. <span id="modelName"></span> Running it again can give <b>different answers</b>; AI suggestions are not official UN tags.</div>
<div class="btns">
<button id="aiGo">Suggest SDGs with AI</button>
<button id="aiAgain" class="sec" disabled>Run again</button>
<button id="aiStop" class="sec" disabled>Stop</button>
<span id="aiProg" aria-live="polite"></span>
</div>
<div id="aiOut"></div>
</div>
</main>
<script>
(function(){
var D=(window.WORKSHOP_DATA||{}).uhri||{};
var recs=Array.isArray(D.records)?D.records:[];
var sdgNames=D.sdg_names||{};
var PAGE=25,page=0,chart=null,open={};
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

/* ---------- AI SDG comparison ---------- */
var aiSet=[],runs=[],running=false,stopFlag=false,aiFilterText="";
var st=window.studio||{};
var mdl=st.model||st.modelName||(st.info&&st.info.model)||"";
$("modelName").textContent=mdl?"The model is: "+mdl+".":"The name of the model is not exposed to this page; it is the language model connected to this workshop environment. Ask the facilitator which one it is.";
if(typeof st.ask!=="function"){$("aiGo").disabled=true;$("aiProg").textContent="AI is not available in this environment."}

function cleanSdgs(a){
  if(!Array.isArray(a))a=(a==null?[]:[a]);
  return uniq(a.map(function(x){return parseInt(x,10)}).filter(function(n){return n>=1&&n<=17})).sort(function(a,b){return a-b});
}
function parseAnswer(s){
  var o=s;
  if(typeof s==="string"){
    var t=s.replace(/^\s*```(?:json)?/i,"").replace(/```\s*$/,"").trim();
    try{o=JSON.parse(t)}catch(e){
      var m=t.match(/[\[{][\s\S]*[\]}]/);
      try{o=m?JSON.parse(m[0]):null}catch(e2){o=null}
    }
  }
  var out={};
  if(!o)return out;
  var list=Array.isArray(o)?o:(Array.isArray(o.results)?o.results:null);
  if(list){list.forEach(function(x){if(x&&x.id!=null)out[String(x.id)]=cleanSdgs(x.sdgs!=null?x.sdgs:x.sdg)})}
  else if(typeof o==="object"){Object.keys(o).forEach(function(k){if(Array.isArray(o[k]))out[k]=cleanSdgs(o[k])})}
  return out;
}
function buildPrompt(batch){
  var goals=Object.keys(sdgNames).sort(function(a,b){return a-b}).map(function(k){return k+" = "+sdgNames[k]}).join("; ");
  var items=batch.map(function(r){return{id:r.id,text:(r.text||"").slice(0,1500)}});
  return "You are helping a human rights researcher. For each UN paragraph below, list the numbers (1-17) of the Sustainable Development Goals that the paragraph clearly relates to. Use an empty list if none clearly applies."+
   (goals?" Goals: "+goals+".":"")+
   ' Answer with JSON only, in this exact shape: {"results":[{"id":"<record id>","sdgs":[16,5]}]}. Include every id exactly once.\n\nRecords:\n'+JSON.stringify(items);
}
async function doRun(set){
  running=true;stopFlag=false;
  var run={n:runs.length+1,res:{},failed:0,stopped:false};
  runs.push(run);setBtns();
  var nb=Math.ceil(set.length/25);
  for(var b=0;b<nb;b++){
    if(stopFlag){run.stopped=true;break}
    $("aiProg").textContent="Run "+run.n+": sending batch "+(b+1)+" of "+nb+" ("+Math.min(25,set.length-b*25)+" records) to the external model… waiting for the answer.";
    var batch=set.slice(b*25,b*25+25);
    try{
      var ans=await st.ask(buildPrompt(batch),{json:true});
      var parsed=parseAnswer(ans),got=0;
      batch.forEach(function(r){if(parsed[String(r.id)]){run.res[r.id]=parsed[String(r.id)];got++}});
      if(got<batch.length)run.failed+=batch.length-got;
    }catch(e){run.failed+=batch.length}
    renderAI();
  }
  running=false;
  $("aiProg").textContent="Run "+run.n+(run.stopped?" stopped.":" finished.")+(run.failed?" "+run.failed+" record(s) got no usable answer.":"");
  setBtns();renderAI();
}
function setBtns(){
  var ok=typeof st.ask==="function";
  $("aiGo").disabled=running||!ok;
  $("aiAgain").disabled=running||!ok||!runs.length;
  $("aiStop").disabled=!running;
}
function same(a,b){return a.length===b.length&&a.every(function(x,i){return x===b[i]})}
function verdict(un,ai){
  if(!ai)return"none";
  if(same(un,ai))return"agree";
  return un.some(function(x){return ai.indexOf(x)>=0})?"part":"differ";
}
function pills(a,ai){
  if(!a||!a.length)return'<span class="note">none</span>';
  return a.map(function(g){return'<span class="pill'+(ai?" ai":"")+'" title="'+esc(sdgNames[g]||"")+'">'+g+'</span>'}).join("");
}
function renderAI(){
  if(!runs.length){$("aiOut").innerHTML="";return}
  var h='<p class="note">Records analysed: the '+aiSet.length+' first records of the filter that was active when you pressed "Suggest SDGs with AI" ('+esc(aiFilterText)+'). "Run again" uses these same records.</p><div class="stats" style="margin:8px 0">';
  runs.forEach(function(run){
    var n=0,ex=0,pt=0;
    aiSet.forEach(function(r){var a=run.res[r.id];if(!a)return;n++;var v=verdict(cleanSdgs(r.sdgs),a);if(v==="agree")ex++;else if(v==="part")pt++});
    h+='<div class="stat" data-source="ai"><b>'+(n?Math.round(100*ex/n)+"%":"n/a")+'</b>Run '+run.n+': exact agreement ('+ex+' of '+n+' answered); '+(n?Math.round(100*(ex+pt)/n):0)+'% share at least one SDG</div>';
  });
  if(runs.length>1){
    var a=runs[runs.length-2],b=runs[runs.length-1],c=0,t=0;
    aiSet.forEach(function(r){if(a.res[r.id]&&b.res[r.id]){t++;if(same(a.res[r.id],b.res[r.id]))c++}});
    h+='<div class="stat" data-source="ai"><b>'+(t?Math.round(100*c/t)+"%":"n/a")+'</b>Run '+a.n+' vs run '+b.n+': identical answers ('+c+' of '+t+')</div>';
  }
  h+='</div><div class="aiwrap"><table><thead><tr><th>Record</th><th>UN\'s SDGs</th>';
  runs.forEach(function(run){h+='<th>AI\'s SDGs (run '+run.n+')</th><th>Agree? (run '+run.n+')</th>'});
  h+='</tr></thead><tbody>';
  var lab={agree:['ok','Yes, identical'],part:['part','Partly (overlap)'],differ:['no','No'],none:['','no answer']};
  aiSet.forEach(function(r){
    var un=cleanSdgs(r.sdgs);
    h+='<tr><td>'+(r.doc_url?'<a href="'+esc(r.doc_url)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol||""))+'<div class="note" style="margin:0">'+esc(firstLine(r.text).slice(0,90))+'</div></td><td>'+pills(un,false)+'</td>';
    runs.forEach(function(run){
      var a=run.res[r.id],v=verdict(un,a);
      h+='<td data-source="ai">'+(a?pills(a,true):'<span class="note">–</span>')+'</td><td data-source="ai"><span class="'+lab[v][0]+'">'+lab[v][1]+'</span></td>';
    });
    h+='</tr>';
  });
  h+='</tbody></table></div><p class="note"><b>How this is computed:</b> "UN\'s SDGs" are the tags already in the data. "AI\'s SDGs" are what the model answered, limited to goals 1–17. <i>Identical</i> means exactly the same set of goals; <i>Partly</i> means at least one goal in common; the exact agreement rate counts identical sets among records the model answered (two empty lists count as identical). Agreement does not show who is right: the UN tags themselves are automatic classifications of the paragraph.</p>';
  $("aiOut").innerHTML=h;
}
$("aiGo").onclick=function(){
  var set=filtered().slice(0,50);
  if(!set.length){$("aiProg").textContent="No records match the current filter.";return}
  aiSet=set;runs=[];aiFilterText=$("filterNote").textContent.replace(/^Filters applied: /,"").replace(/\. n = .*$/,"");
  doRun(set);
};
$("aiAgain").onclick=function(){if(aiSet.length)doRun(aiSet)};
$("aiStop").onclick=function(){stopFlag=true;$("aiProg").textContent="Stopping after the current batch…"};
setBtns();
})();
</script>
</body>
</html>
```