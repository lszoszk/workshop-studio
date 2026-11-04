I added FIG.03 on the Overview, a single-colour bar chart of all records per year for the current filter, placed under FIG.02. Years with no records show as empty gaps, and the count sits at the top of each bar.

```edit
<<<<<<< SEARCH
  <div class="note">How this is computed: records per <i>year</i> and <i>mechanism</i> in the filtered set; years without records stay as gaps, years are the document's year.</div>
  <div class="note figsrc"></div>
=======
  <div class="note">How this is computed: records per <i>year</i> and <i>mechanism</i> in the filtered set; years without records stay as gaps, years are the document's year.</div>
  <div class="note figsrc"></div>
  <h3 class="fig"><span class="mono figlab">FIG.03</span> <span id="fig3T"></span></h3>
  <div class="chartbox short"><canvas id="c3" aria-label="Bar chart of recommendations and observations per year"></canvas></div>
  <div class="note" id="c3empty" hidden>No records match.</div>
  <div class="note">How this is computed: every record in the filtered set counts once in the <i>year</i> of its document, whatever its type; the bars add up to the filtered count.</div>
  <div class="note figsrc"></div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
let F=[],lastTop=[],c1=null,c2=null;
=======
let F=[],lastTop=[],c1=null,c2=null,c3=null;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  /* FIG.02 */
=======
  /* FIG.03 */
  const yr3=rngYears(F);
  $('fig3T').textContent='Recommendations and observations per year, '+fmt(F.length)+' filtered records';
  $('c3empty').hidden=!!yr3;$('c3').parentNode.hidden=!yr3;
  if(c3){c3.destroy();c3=null}
  if(yr3&&window.Chart){
    const ys3=[];for(let y=yr3[0];y<=yr3[1];y++)ys3.push(y);
    const vs3=ys3.map(y=>F.filter(r=>r.year===y).length);
    c3=new Chart($('c3'),{type:'bar',
      data:{labels:ys3,datasets:[{data:vs3,backgroundColor:'rgba(155,35,53,0.8)'}]},
      options:{animation:false,responsive:true,maintainAspectRatio:false,layout:{padding:{top:18}},plugins:{legend:{display:false}},
        scales:{x:{grid:{display:false},ticks:{autoSkip:false,maxRotation:0,font:{size:10}}},y:{display:false,beginAtZero:true,grid:{display:false}}}},
      plugins:[{id:'vl3',afterDatasetsDraw(ch){const c=ch.ctx;c.save();c.fillStyle='#1d1b18';c.font='11px system-ui,sans-serif';c.textAlign='center';c.textBaseline='bottom';ch.getDatasetMeta(0).data.forEach((b,i)=>{const v=ch.data.datasets[0].data[i];if(v>0)c.fillText(fmt(v),b.x,b.y-3)});c.restore()}}]});
  }
  /* FIG.02 */
>>>>>>> REPLACE
```