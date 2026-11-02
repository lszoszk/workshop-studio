I built a comparison tool for two Council States, with a resolution/amendment/both switch, a yearly agreement timeline, and a list of the votes where they differed. Rows where the official totals differ from the roll call carry a warning. Both States must have a recorded vote on the same item to count as "took part together"; abstentions count as a vote cast.

```html
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Compare two States at the Human Rights Council</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;font-size:16px;background:#f6f8fa;color:#1c2630;margin:0}
main{max-width:1050px;margin:0 auto;padding:24px 20px 60px}
h1{margin:0 0 6px;font-size:1.7rem}h2{margin-top:32px;font-size:1.25rem}
.desc{color:#4a5a68;margin-bottom:20px}
.card{background:#fff;border:1px solid #dde3e9;border-radius:8px;padding:16px 18px;margin-top:14px}
.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:end}
label{display:flex;flex-direction:column;font-weight:600;font-size:.9rem;gap:4px}
select{font-size:1rem;padding:6px 8px;min-width:230px}
.seg button{font-size:1rem;padding:7px 14px;border:1px solid #1f6fb2;background:#fff;color:#1f6fb2;cursor:pointer}
.seg button.on{background:#1f6fb2;color:#fff}
.seg{display:flex}
.stats{display:flex;gap:16px;flex-wrap:wrap}
.stat{flex:1;min-width:180px}.stat b{display:block;font-size:2rem;color:#1f6fb2}
.note{font-size:.88rem;color:#566573;margin-top:10px;background:#eef3f8;padding:8px 10px;border-radius:5px}
table{border-collapse:collapse;width:100%}
th,td{text-align:left;padding:8px 6px;border-bottom:1px solid #e5e9ed;vertical-align:top;font-size:.93rem}
th{font-size:.82rem;text-transform:uppercase;color:#566573}
.warn{display:inline-block;background:#fff3cd;color:#7a5b00;border:1px solid #e8cf7a;border-radius:4px;font-size:.78rem;padding:1px 6px;margin-top:4px}
.v{font-weight:700}
.tt{cursor:pointer;color:#1f6fb2;font-size:.85rem;background:none;border:0;padding:0}
.full{font-size:.85rem;color:#4a5a68;margin-top:4px}
canvas{max-height:320px}
</style></head><body><main>
<h1>Compare two States at the Human Rights Council</h1>
<div class="desc" id="desc"></div>
<div class="card"><div class="controls">
<label>State A<select id="a"></select></label>
<label>State B<select id="b"></select></label>
<div><div style="font-weight:600;font-size:.9rem;margin-bottom:4px">Show</div><div class="seg" id="seg"></div></div>
</div>
<div class="note">Only States that appear in at least one roll call (recorded vote) are listed.</div></div>
<div id="out"></div>
<script>
const H=(window.WORKSHOP_DATA||{}).hrc||{};
const recs=H.records||[],names=H.countries||{};
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const years=recs.map(r=>r.year).filter(Boolean);
document.getElementById("desc").textContent=`Source: ${H.title||"Human Rights Council recorded votes"}. ${recs.length} recorded votes`+(years.length?`, ${Math.min(...years)}–${Math.max(...years)}.`:".");
const present=new Set();recs.forEach(r=>Object.keys(r.votes||{}).forEach(k=>present.add(k)));
const list=[...present].sort((x,y)=>(names[x]||x).localeCompare(names[y]||y));
const A=document.getElementById("a"),B=document.getElementById("b");
list.forEach(c=>{for(const s of[A,B]){const o=document.createElement("option");o.value=c;o.textContent=names[c]||c;s.appendChild(o)}});
if(list.length>1)B.selectedIndex=1;
let kind="both",chart=null;
const seg=document.getElementById("seg");
[["both","Both"],["resolution","Resolutions"],["amendment","Amendments"]].forEach(([k,l])=>{const b=document.createElement("button");b.textContent=l;b.onclick=()=>{kind=k;render()};b.dataset.k=k;seg.appendChild(b)});
const VN={Y:"Yes",N:"No",A:"Abstain"};
function rollMismatch(r){let y=0,n=0,a=0;Object.values(r.votes||{}).forEach(v=>{if(v==="Y")y++;else if(v==="N")n++;else if(v==="A")a++});
 if(y!==r.yes||n!==r.no||a!==r.abstain)return `Official totals Y${r.yes}/N${r.no}/A${r.abstain}; roll call Y${y}/N${n}/A${a}`;return ""}
function render(){
 [...seg.children].forEach(b=>b.classList.toggle("on",b.dataset.k===kind));
 const out=document.getElementById("out");
 if(!list.length){out.innerHTML='<div class="card">No roll-call data available.</div>';return}
 const a=A.value,b=B.value,na=names[a]||a,nb=names[b]||b;
 if(a===b){out.innerHTML='<div class="card">Please pick two different States.</div>';return}
 const sel=recs.filter(r=>kind==="both"||r.kind===kind);
 const both=sel.filter(r=>r.votes&&r.votes[a]&&r.votes[b]);
 const same=both.filter(r=>r.votes[a]===r.votes[b]);
 const diff=both.filter(r=>r.votes[a]!==r.votes[b]).sort((x,y)=>(y.date||"").localeCompare(x.date||""));
 const pct=both.length?(100*same.length/both.length).toFixed(1)+"%":"n/a";
 const by={};both.forEach(r=>{const y=r.year;(by[y]=by[y]||{n:0,s:0});by[y].n++;if(r.votes[a]===r.votes[b])by[y].s++});
 const ys=Object.keys(by).sort();
 out.innerHTML=`<h2>${esc(na)} and ${esc(nb)}</h2>
 <div class="card"><div class="stats">
 <div class="stat"><b>${both.length}</b>recorded votes where both took part (of ${sel.length} in this selection)</div>
 <div class="stat"><b>${same.length}</b>voted the same way</div>
 <div class="stat"><b>${pct}</b>agreement rate</div>
 <div class="stat"><b>${diff.length}</b>voted differently</div></div>
 <div class="note">How this is computed: for each recorded vote in the selected type where both States appear in the roll call, we compare their codes (Yes / No / Abstain). Same code = agreement; an abstention against a yes or no counts as a difference. Votes where either State was not a member are left out.</div></div>
 <h2>Agreement by year</h2><div class="card"><canvas id="ch"></canvas>
 <div class="note">Bars show the % of jointly recorded votes in each year with identical votes; the number of votes per year is in the tooltip. Years with few votes can swing widely.</div></div>
 <h2>Votes where they differed (${diff.length})</h2><div class="card">
 ${diff.length?`<table><thead><tr><th>Date</th><th>Title</th><th>${esc(na)}</th><th>${esc(nb)}</th><th>Document</th></tr></thead><tbody>${diff.map((r,i)=>{const w=rollMismatch(r);const u=r.doc_url||r.record_url;
 return `<tr><td>${esc(r.date)}</td><td>${esc(r.title)}<br><span style="color:#566573;font-size:.82rem">${esc(r.kind)}${r.session?" · "+esc(r.session):""}</span>${w?`<br><span class="warn" title="${esc(w)}">⚠ Totals differ from roll call</span><div class="full">${esc(w)}</div>`:""}</td><td class="v">${VN[r.votes[a]]||esc(r.votes[a])}</td><td class="v">${VN[r.votes[b]]||esc(r.votes[b])}</td><td>${u?`<a href="${esc(u)}" target="_blank" rel="noopener">${esc(r.symbol)}</a>`:esc(r.symbol)}</td></tr>`}).join("")}</tbody></table>`:"<p>No differing votes in this selection.</p>"}
 <div class="note">Filter applied: ${kind==="both"?"resolutions and amendments":kind+"s"}. Sorted newest first. Symbols link to the document (or the library record if no document link exists). The warning appears when the official yes/no/abstain totals differ from the count of the roll call.</div></div>`;
 if(chart)chart.destroy();
 chart=new Chart(document.getElementById("ch"),{type:"bar",data:{labels:ys,datasets:[{label:"% same vote",data:ys.map(y=>+(100*by[y].s/by[y].n).toFixed(1)),backgroundColor:"#1f6fb2"}]},
 options:{animation:false,scales:{y:{min:0,max:100,title:{display:true,text:"% same vote"}}},plugins:{tooltip:{callbacks:{afterLabel:c=>`${by[ys[c.dataIndex]].s} of ${by[ys[c.dataIndex]].n} votes`}}}}});
}
A.onchange=B.onchange=render;render();
</script></main></body></html>
```