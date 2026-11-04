I'll add a third figure on the Overview tab: records per year, split by type, alongside the existing mechanism chart.

```edit
<<<<<<< SEARCH
    <figcaption>Source: same UHRI extract. Counted from the <code>year</code> field, dated by document. Years with no records appear as gaps.</figcaption>
  </figure>
</section>
=======
    <figcaption>Source: same UHRI extract. Counted from the <code>year</code> field, dated by document. Years with no records appear as gaps.</figcaption>
  </figure>
  <figure>
    <div class="mono">FIG.03</div>
    <h2>Recommendations and observations per year</h2>
    <figcaption id="fig3Cap"></figcaption>
    <div class="legend" id="fig3Legend"></div>
    <div class="chartbox"><canvas id="fig3" height="0"></canvas></div>
    <figcaption>Source: same UHRI extract. Counted from the <code>year</code> and <code>type</code> fields, dated by document. Every type present in the filtered set gets a stack, including a small “Other” group when the data has one; years with no records appear as gaps.</figcaption>
  </figure>
</section>
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
let fig1Chart=null,fig2Chart=null;
=======
let fig1Chart=null,fig2Chart=null,fig3Chart=null;
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  fig2Chart=new Chart($("fig2"),{type:"bar",data:{labels:allY.map(String),datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.dataset.label}: ${fmt(c.parsed.y)}`}}},
      scales:{x:{stacked:true,title:{display:true,text:"Year (dated by document)"}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
  $("fig2").style.height="260px";$("fig2").parentElement.style.height="260px";
}
=======
  fig2Chart=new Chart($("fig2"),{type:"bar",data:{labels:allY.map(String),datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.dataset.label}: ${fmt(c.parsed.y)}`}}},
      scales:{x:{stacked:true,title:{display:true,text:"Year (dated by document)"}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
  $("fig2").style.height="260px";$("fig2").parentElement.style.height="260px";
}
function renderFig3(set){
  if(!set.length){if(fig3Chart){fig3Chart.destroy();fig3Chart=null;}$("fig3Cap").textContent="No records match.";return;}
  const y1=Math.min(...set.map(r=>r.year)),y2=Math.max(...set.map(r=>r.year));
  const allY=[];for(let y=y1;y<=y2;y++)allY.push(y);
  const types=[...new Set(set.map(r=>r.type))].sort();
  const ds=types.map(t=>({label:t,backgroundColor:t==="Recommendations"?"#9b2335":"#7a6f5f",
    data:allY.map(y=>set.filter(r=>r.year===y&&r.type===t).length)}));
  $("fig3Legend").innerHTML=types.map(t=>`<span><span class="dot" style="background:${t==="Recommendations"?"#9b2335":"#7a6f5f"}"></span>${esc(t)}</span>`).join("");
  $("fig3Cap").textContent=`Filtered set of ${fmt(set.length)} records, ${y1}–${y2}, counted per type as spelled in the data.`;
  if(fig3Chart)fig3Chart.destroy();
  fig3Chart=new Chart($("fig3"),{type:"bar",data:{labels:allY.map(String),datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.dataset.label}: ${fmt(c.parsed.y)}`}}},
      scales:{x:{stacked:true,title:{display:true,text:"Year (dated by document)"}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
  $("fig3").style.height="260px";$("fig3").parentElement.style.height="260px";
}
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  if(curTab===1){renderTiles(set);renderFig1(set);renderFig2(set);}
=======
  if(curTab===1){renderTiles(set);renderFig1(set);renderFig2(set);renderFig3(set);}
>>>>>>> REPLACE
```
```