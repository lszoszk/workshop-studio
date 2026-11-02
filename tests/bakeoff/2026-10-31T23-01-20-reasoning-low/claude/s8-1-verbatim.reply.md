I built a search tool over the General Comments paragraphs with AND/OR/NOT and "exact phrase" support, committee and year filters, highlighted matches, a Copy citation button, and a bar chart of hits per committee. Paragraph text is shown exactly as in the data, and all matching is done by deterministic code.

```html
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>General Comments search</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#f6f8fa;color:#1d2733}
main{max-width:1000px;margin:0 auto;padding:24px 20px 60px}
h1{margin:0 0 4px;font-size:28px;color:#1f6fb2}
.desc{color:#4a5a6a;margin-bottom:18px}
.card{background:#fff;border:1px solid #dde4ea;border-radius:8px;padding:16px;margin-bottom:16px}
input[type=text]{width:100%;box-sizing:border-box;font-size:18px;padding:10px;border:1px solid #9fb2c3;border-radius:6px}
.row{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px;align-items:end}
label{font-size:14px;color:#4a5a6a;display:block}
select{font-size:16px;padding:7px;border:1px solid #9fb2c3;border-radius:6px;background:#fff}
button{font-size:15px;padding:7px 12px;border:1px solid #1f6fb2;background:#1f6fb2;color:#fff;border-radius:6px;cursor:pointer}
button.sec{background:#fff;color:#1f6fb2}
.note{font-size:14px;color:#566676;margin-top:10px}
.res{border-top:1px solid #e3e9ee;padding:14px 0}
.meta{font-size:14px;color:#566676}
.meta b{color:#1d2733}
.txt{margin:6px 0;white-space:pre-wrap}
.txt.clip{max-height:6.5em;overflow:hidden}
mark{background:#ffe58a;padding:0 1px}
a{color:#1f6fb2}
.tag{display:inline-block;background:#e6f0f8;color:#1f6fb2;border-radius:4px;padding:0 7px;font-size:13px;margin-right:6px}
.err{color:#b3261e}
.chartbox{height:260px}
</style></head><body><main>
<h1>General Comments search</h1>
<div class="desc" id="desc"></div>
<div class="card">
<input type="text" id="q" placeholder='e.g. torture AND "effective remedy" NOT children'>
<div class="row">
<div><label for="com">Committee</label><select id="com"></select></div>
<div><label for="y1">Year from</label><select id="y1"></select></div>
<div><label for="y2">Year to</label><select id="y2"></select></div>
<button id="clr" class="sec">Reset</button>
</div>
<div class="note"><b>How to search:</b> words next to each other mean AND. Use <code>OR</code> between alternatives, <code>NOT</code> (or a minus sign) to exclude a word, and quotation marks for an exact phrase. Capital letters do not matter in the words you search for. Example: <code>"effective remedy" AND (torture OR ill-treatment)</code> – brackets are supported.</div>
<div id="qerr" class="err"></div>
</div>
<div class="card"><h3 style="margin-top:0">Hits per committee</h3>
<div class="chartbox"><canvas id="ch"></canvas></div>
<div class="note"><b>How this is computed:</b> each paragraph that matches your search and the year filter is counted once under its committee. The committee filter is not applied to this chart so you can compare committees.</div></div>
<div class="card"><div id="sum"></div><div id="list"></div>
<div class="note"><b>How this is computed:</b> a paragraph is a hit when its text satisfies the search expression (plain substring match, ignoring upper/lower case). Results are sorted by year, then symbol, then paragraph number. Only the first 100 hits are shown at a time.</div></div>
</main>
<script>
const D=(window.WORKSHOP_DATA&&WORKSHOP_DATA.gc)||{records:[]};
const R=D.records||[];
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const years=R.map(r=>r.year).filter(y=>typeof y==="number");
const minY=years.length?Math.min(...years):0,maxY=years.length?Math.max(...years):0;
$("desc").textContent=`Source: ${D.source||D.title||"UN treaty body General Comments"} · ${R.length} paragraphs · ${years.length?minY+"–"+maxY:"years unknown"}`;
const coms=[...new Set(R.map(r=>r.committee).filter(Boolean))].sort();
$("com").innerHTML='<option value="">All committees</option>'+coms.map(c=>`<option>${esc(c)}</option>`).join("");
const ys=[...new Set(years)].sort((a,b)=>a-b);
$("y1").innerHTML=ys.map(y=>`<option>${y}</option>`).join("");
$("y2").innerHTML=ys.map(y=>`<option>${y}</option>`).join("");
function resetYears(){if(ys.length){$("y1").value=ys[0];$("y2").value=ys[ys.length-1]}}
resetYears();
// query parser
function tokenize(s){const t=[];const re=/"([^"]*)"|\(|\)|[^\s()"]+/g;let m;
while((m=re.exec(s))){if(m[1]!==undefined){if(m[1].trim())t.push({t:"term",v:m[1].toLowerCase()})}
else if(m[0]==="("||m[0]===")")t.push({t:m[0]});
else if(m[0]==="AND"||m[0]==="OR"||m[0]==="NOT")t.push({t:m[0]});
else if(m[0].length>1&&m[0][0]==="-")t.push({t:"NOT"}),t.push({t:"term",v:m[0].slice(1).toLowerCase()});
else t.push({t:"term",v:m[0].toLowerCase()})}
return t}
function parse(s){const tk=tokenize(s);let i=0;const terms=[];
function or(){let a=and();while(tk[i]&&tk[i].t==="OR"){i++;const b=and();a={o:"or",a,b}}return a}
function and(){let a=not();while(tk[i]&&tk[i].t!==")"&&tk[i].t!=="OR"){if(tk[i].t==="AND")i++;const b=not();a={o:"and",a,b}}return a}
function not(){if(tk[i]&&tk[i].t==="NOT"){i++;return {o:"not",a:not()}}return atom()}
function atom(){const k=tk[i];if(!k)throw new Error("The search ends unexpectedly.");
if(k.t==="("){i++;const e=or();if(!tk[i]||tk[i].t!==")")throw new Error("Missing closing bracket.");i++;return e}
if(k.t==="term"){i++;terms.push(k.v);return {o:"t",v:k.v}}
throw new Error("Unexpected "+k.t+" in the search.")}
if(!tk.length)return {ast:null,terms:[]};
const ast=or();if(i<tk.length)throw new Error("Unexpected bracket or operator.");
return {ast,terms:terms}}
function ev(n,txt){switch(n.o){case"t":return txt.includes(n.v);case"and":return ev(n.a,txt)&&ev(n.b,txt);case"or":return ev(n.a,txt)||ev(n.b,txt);case"not":return !ev(n.a,txt)}}
function positive(n,out,neg){if(!n)return;if(n.o==="t"){if(!neg)out.push(n.v)}else if(n.o==="not")positive(n.a,out,!neg);else{positive(n.a,out,neg);positive(n.b,out,neg)}}
function hl(text,terms){if(!terms.length)return esc(text);
const re=new RegExp(terms.map(t=>t.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).sort((a,b)=>b.length-a.length).join("|"),"gi");
let out="",last=0,m;while((m=re.exec(text))){if(!m[0].length){re.lastIndex++;continue}out+=esc(text.slice(last,m.index))+"<mark>"+esc(m[0])+"</mark>";last=m.index+m[0].length}
return out+esc(text.slice(last))}
let chart,shown=[];
function run(){
$("qerr").textContent="";let p={ast:null,terms:[]};
try{p=parse($("q").value)}catch(e){$("qerr").textContent="Cannot read the search: "+e.message}
let a=+$("y1").value,b=+$("y2").value;if(a>b)[a,b]=[b,a];
const inYear=R.filter(r=>typeof r.year!=="number"||(r.year>=a&&r.year<=b));
const hit=inYear.filter(r=>!p.ast||ev(p.ast,String(r.text||"").toLowerCase()));
const counts={};hit.forEach(r=>{const c=r.committee||"(unknown)";counts[c]=(counts[c]||0)+1});
const labs=Object.keys(counts).sort((x,y)=>counts[y]-counts[x]);
if(chart)chart.destroy();
chart=new Chart($("ch"),{type:"bar",data:{labels:labs,datasets:[{label:"Hits",data:labs.map(l=>counts[l]),backgroundColor:"#1f6fb2"}]},options:{maintainAspectRatio:false,animation:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{precision:0}}}}});
const c=$("com").value;
const res=hit.filter(r=>!c||r.committee===c).sort((x,y)=>(x.year||0)-(y.year||0)||String(x.symbol).localeCompare(String(y.symbol))||(x.paragraph||0)-(y.paragraph||0));
const pos=[];positive(p.ast,pos,false);
$("sum").innerHTML=`<b>${res.length}</b> of ${R.length} paragraphs match`+(res.length>100?" (showing the first 100)":"")+`. Filters: committee ${esc(c||"all")}, years ${a||"?"}–${b||"?"}, search ${esc($("q").value||"(none)")}.`;
shown=res.slice(0,100);
$("list").innerHTML=shown.length?shown.map((r,i)=>{const long=String(r.text||"").length>600;
return `<div class="res"><div class="meta"><span class="tag">${esc(r.committee)}</span><b>${esc(r.short_title||r.title)}</b> · ${r.year||""}<br>
<a href="${esc(r.doc_url)}" target="_blank" rel="noopener">${esc(r.symbol)}</a>, para. ${esc(r.paragraph)}</div>
<div class="txt${long?" clip":""}" id="t${i}">${hl(String(r.text||""),pos)}</div>
<button class="sec" data-c="${i}">Copy citation</button> ${long?`<button class="sec" data-e="${i}">Show full paragraph</button>`:""}</div>`}).join(""):'<p>No paragraphs match. Try fewer words, OR, or wider years.</p>'}
document.addEventListener("click",e=>{const t=e.target;
if(t.dataset.e!==undefined){const el=$("t"+t.dataset.e);el.classList.toggle("clip");t.textContent=el.classList.contains("clip")?"Show full paragraph":"Collapse"}
if(t.dataset.c!==undefined){const r=shown[+t.dataset.c];const s=`${r.symbol}, para. ${r.paragraph}`;
const done=()=>{t.textContent="Copied: "+s;setTimeout(()=>t.textContent="Copy citation",1800)};
const fb=()=>{const x=document.createElement("textarea");x.value=s;document.body.appendChild(x);x.select();try{document.execCommand("copy")}catch(_){}x.remove();done()};
if(navigator.clipboard)navigator.clipboard.writeText(s).then(done,fb);else fb()}});
let tm;$("q").addEventListener("input",()=>{clearTimeout(tm);tm=setTimeout(run,250)});
["com","y1","y2"].forEach(id=>$(id).addEventListener("change",run));
$("clr").onclick=()=>{$("q").value="";$("com").value="";resetYears();run()};
run();
</script></body></html>
```