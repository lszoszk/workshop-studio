Added FIG.03 on the Overview tab: a stacked bar chart counting records per year, split by `type` (Recommendations, Concerns/Observations, and any other type present), over the same years and filter as FIG.02.

```edit
<<<<<<< SEARCH
      <div class="note">How this is computed: records counted per year and per mechanism in the current filter; years with no records appear as gaps. Source: OHCHR UHRI, document dates ("dated by document").</div>
    </figure>
  </section>
=======
      <div class="note">How this is computed: records counted per year and per mechanism in the current filter; years with no records appear as gaps. Source: OHCHR UHRI, document dates ("dated by document").</div>
    </figure>
    <figure>
      <div class="figno">FIG.03</div>
      <figcaption id="fig3title"></figcaption>
      <div class="chartbox"><canvas id="fig3"></canvas></div>
      <div class="note">How this is computed: records counted per year and per <em>type</em> in the current filter, using the UN&rsquo;s own labels; years with no records appear as gaps. Source: OHCHR UHRI, document dates ("dated by document").</div>
    </figure>
  </section>
>>>>>>> REPLACE REPLACE
```


```edit
<<<<<<< SEARCH
      scales:{x:{stacked:true,title:{display:true,text:'Year (dated by document)'}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}
  });
}

/* ---------- records table ---------- */
=======
      scales:{x:{stacked:true,title:{display:true,text:'Year (dated by document)'}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}
  });

  document.getElementById('fig3title').textContent='Recommendations and observations per year ('+fmt(set.length)+' filtered records)';
  const types=[...new Set(recs.map(r=>r.type))];
  if(ch3)ch3.destroy();
  ch3=new Chart(document.getElementById('fig3'),{
    type:'bar',
    data:{labels:allY,datasets:types.map(t=>({label:t,data:allY.map(y=>set.filter(r=>r.year===y&&r.type===t).length),backgroundColor:typeColor[t]||'#888'}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'bottom',labels:{boxWidth:10}},tooltip:{}},
      scales:{x:{stacked:true,title:{display:true,text:'Year (dated by document)'}},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}
  });
}

/* ---------- records table ---------- */
>>>>>>> REPLACE REPLACE
```


```edit
<<<<<<< SEARCH
let ch1=null,ch2=null;
=======
let ch1=null,ch2=null,ch3=null;
const typeColor={'Recommendations':'#9b2335','Concerns/Observations':'#0f766e','Other':'#a16207'};
>>>>>>> REPLACE REPLACE
```
```