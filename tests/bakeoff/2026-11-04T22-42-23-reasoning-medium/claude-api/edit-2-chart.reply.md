I've added FIG.03, a bar chart of records per year, stacked by type so recommendations and concerns/observations show separately. It follows the same filters as the rest of the page, and years with no records stay as visible gaps.

```edit
<<<<<<< SEARCH
      <div class="src" id="f2src"></div>
=======
      <div class="src" id="f2src"></div>
      <div class="fig">FIG.03</div>
      <h3 id="f3t"></h3>
      <div id="f3empty" class="empty" hidden>No records match.</div>
      <div class="chartbox t" id="f3box"><canvas id="c3" role="img" aria-label="Stacked bar chart of records per year by type"></canvas></div>
      <div class="how">How this is computed: records per year of the document date, split by the type value as spelled in the data; every year from the first to the last is shown, empty years as gaps.</div>
      <div class="src" id="f3src"></div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
let filtered=[],cur=1,shown=50,dirDesc=true,expanded=new Set(),ch1=null,ch2=null,lastTop=[];
=======
let filtered=[],cur=1,shown=50,dirDesc=true,expanded=new Set(),ch1=null,ch2=null,ch3=null,lastTop=[];
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  if(ch1){ch1.destroy();ch1=null}if(ch2){ch2.destroy();ch2=null}
=======
  if(ch1){ch1.destroy();ch1=null}if(ch2){ch2.destroy();ch2=null}if(ch3){ch3.destroy();ch3=null}
  $('f3t').textContent='Recommendations and observations per year, '+fmt(n)+' filtered records';
  $('f3src').innerHTML=srcl;
  $('f3empty').hidden=!!n;$('f3box').hidden=!n;
  if(n&&yr&&window.Chart){
    const ys3=[];for(let y=yr[0];y<=yr[1];y++)ys3.push(y);
    const tcol=t=>t==='Recommendations'?'#9b2335':t==='Concerns/Observations'?'#4a463e':'#a39d8e';
    const ts3=uniq(f.map(r=>r.type));
    ch3=new Chart($('c3'),{type:'bar',data:{labels:ys3.map(String),datasets:ts3.map(t=>({label:t||'(no type)',backgroundColor:tcol(t),data:ys3.map(y=>f.filter(r=>r.type===t&&r.year===y).length)}))},
      options:{animation:false,maintainAspectRatio:false,plugins:{legend:{position:'top'}},scales:{x:{stacked:true,grid:{display:false},ticks:{maxRotation:0,autoSkip:true}},y:{stacked:true,beginAtZero:true,grid:{color:'#e6e0d2'}}}}});
  }
>>>>>>> REPLACE
```