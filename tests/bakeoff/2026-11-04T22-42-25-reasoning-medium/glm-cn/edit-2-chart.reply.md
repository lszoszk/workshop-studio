I'll add a third figure to the Overview tab: records per year, split by type, as a stacked bar chart with a legend, plus a "How this is computed" note. It reads the same filtered set as the other figures.

```edit
<<<<<<< SEARCH
  <div class="fig">
    <div class="figno">FIG.02</div>
    <h3 id="fig2Title"></h3>
    <div class="chartwrap small"><canvas id="fig2"></canvas></div>
    <p class="note">How this is computed: records per calendar year per mechanism in the current filter, from the file's first to its last year; empty years are shown as gaps. Source: OHCHR UHRI.</p>
  </div>
=======
  <div class="fig">
    <div class="figno">FIG.02</div>
    <h3 id="fig2Title"></h3>
    <div class="chartwrap small"><canvas id="fig2"></canvas></div>
    <p class="note">How this is computed: records per calendar year per mechanism in the current filter, from the file's first to its last year; empty years are shown as gaps. Source: OHCHR UHRI.</p>
  </div>
  <div class="fig">
    <div class="figno">FIG.03</div>
    <h3 id="fig3Title"></h3>
    <div class="chartwrap small"><canvas id="fig3"></canvas></div>
    <p class="note">How this is computed: records per calendar year per <span class="mono">type</span> value in the current filter (spelled as in the data), with zero for missing years; empty years are shown as gaps. Source: OHCHR UHRI.</p>
  </div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
let c1=null,c2=null;
=======
let c1=null,c2=null,c3=null;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(!filtered.length){
    document.getElementById('fig2').parentElement.insertAdjacentHTML('beforeend','<p class="muted" id="noRec2">No records match.</p>');
  }else{
    const n2=document.getElementById('noRec2'); if(n2)n2.remove();
    c2=new Chart(document.getElementById('fig2'),{type:'bar',
      data:{labels:years.map(String),datasets:mechanisms.map(m=>({label:m,data:byM[m],backgroundColor:MECH_COLORS[m]}))},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{boxWidth:10}},tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmt(c.raw)}}},
        scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{display:false},ticks:{precision:0}}}}});
  }
}
=======
  if(!filtered.length){
    document.getElementById('fig2').parentElement.insertAdjacentHTML('beforeend','<p class="muted" id="noRec2">No records match.</p>');
  }else{
    const n2=document.getElementById('noRec2'); if(n2)n2.remove();
    c2=new Chart(document.getElementById('fig2'),{type:'bar',
      data:{labels:years.map(String),datasets:mechanisms.map(m=>({label:m,data:byM[m],backgroundColor:MECH_COLORS[m]}))},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{boxWidth:10}},tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmt(c.raw)}}},
        scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{display:false},ticks:{precision:0}}}}});
  }

  /* FIG.03 */
  document.getElementById('fig3Title').textContent='Recommendations and observations per year, '+fmt(filtered.length)+' filtered records';
  if(c3)c3.destroy();
  const byT={}; types.forEach(t=>{byT[t]=years.map(()=>0);});
  filtered.forEach(r=>{const i=years.indexOf(r.year); if(i>=0)byT[r.type][i]++;});
  if(!filtered.length){
    document.getElementById('fig3').parentElement.insertAdjacentHTML('beforeend','<p class="muted" id="noRec3">No records match.</p>');
  }else{
    const n3=document.getElementById('noRec3'); if(n3)n3.remove();
    c3=new Chart(document.getElementById('fig3'),{type:'bar',
      data:{labels:years.map(String),datasets:types.map((t,i)=>({label:t,data:byT[t],backgroundColor:TYPE_COLORS[i%TYPE_COLORS.length]}))},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{boxWidth:10}},tooltip:{callbacks:{label:c=>c.dataset.label+': '+fmt(c.raw)}}},
        scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{display:false},ticks:{precision:0}}}}});
  }
}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
const MECH_COLORS = {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
=======
const MECH_COLORS = {"Universal Periodic Review":"#c2410c","Treaty bodies":"#0f766e","Special Procedures":"#7c3aed"};
const TYPE_COLORS = ["#9b2335","#0f766e","#7c3aed"];
>>>>>>> REPLACE
```