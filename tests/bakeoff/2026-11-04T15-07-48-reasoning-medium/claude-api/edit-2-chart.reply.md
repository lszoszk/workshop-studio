I added FIG.03 at the bottom of the overview: records per year, stacked by type (recommendations, concerns/observations, other). It reads the same filtered set as the other charts, and empty years show as gaps. I have not run it against your data.

```edit
<<<<<<< SEARCH
    <p class="how">How this is computed: records per year and mechanism in the filtered set; every year from first to last is shown, empty years are gaps. Years are the document's year.</p>
=======
    <p class="how">How this is computed: records per year and mechanism in the filtered set; every year from first to last is shown, empty years are gaps. Years are the document's year.</p>
    <h3 id="f3t"></h3>
    <div class="mono">FIG.03</div>
    <div class="chartbox s" id="cb3"><canvas id="c3" role="img" aria-label="Stacked bars of the number of recommendations and observations per year, by type"></canvas></div>
    <p class="how">How this is computed: records per year in the filtered set, split by the type value as spelled in the data; every year from first to last is shown, empty years are gaps. Years are the document's year.</p>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
let F=[],CH=[],c1=null,c2=null,statCache=null;
=======
let F=[],CH=[],c1=null,c2=null,c3=null,statCache=null;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  $('f2t').textContent='Records per year by mechanism, '+fmt(F.length)+' filtered records';
=======
  $('f2t').textContent='Records per year by mechanism, '+fmt(F.length)+' filtered records';
  $('f3t').textContent='Recommendations and observations per year, '+fmt(F.length)+' filtered records';
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  $('cb1').hidden=!F.length;$('cb2').hidden=!F.length;
=======
  $('cb1').hidden=!F.length;$('cb2').hidden=!F.length;$('cb3').hidden=!F.length;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(c2){c2.destroy();c2=null}
=======
  if(c2){c2.destroy();c2=null}
  if(c3){c3.destroy();c3=null}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      scales:{x:{stacked:true,grid:{display:false},ticks:{color:'#1d1b18',autoSkip:false,maxRotation:90,font:{size:11}}},y:{stacked:true,grid:{color:'#e6dfd0'},ticks:{color:'#1d1b18'},beginAtZero:true}}}});
=======
      scales:{x:{stacked:true,grid:{display:false},ticks:{color:'#1d1b18',autoSkip:false,maxRotation:90,font:{size:11}}},y:{stacked:true,grid:{color:'#e6dfd0'},ticks:{color:'#1d1b18'},beginAtZero:true}}}});
  const tcnt={};F.forEach(r=>{const k=typeOf(r)+'|'+r.year;tcnt[k]=(tcnt[k]||0)+1});
  const tcol=t=>t==='Recommendations'?'#9b2335':t==='Concerns/Observations'?'#5a554c':'#b9b19f';
  const tsl=types.filter(t=>F.some(r=>typeOf(r)===t));
  c3=new Chart($('c3'),{type:'bar',
    data:{labels:ys,datasets:tsl.map(t=>({label:t,data:ys.map(y=>tcnt[t+'|'+y]||0),backgroundColor:tcol(t)}))},
    options:{responsive:true,maintainAspectRatio:false,animation:false,
      plugins:{legend:{position:'top',labels:{color:'#1d1b18',boxWidth:12}}},
      scales:{x:{stacked:true,grid:{display:false},ticks:{color:'#1d1b18',autoSkip:false,maxRotation:90,font:{size:11}}},y:{stacked:true,grid:{color:'#e6dfd0'},ticks:{color:'#1d1b18'},beginAtZero:true}}}});
>>>>>>> REPLACE
```