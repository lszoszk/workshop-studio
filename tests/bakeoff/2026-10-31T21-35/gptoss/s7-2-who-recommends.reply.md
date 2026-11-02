The page now has two tabs: the original dashboard and a “Who recommends what” view that shows the most active recommending states, their SDG focus, and a list of their UPR recommendations.  

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UN Human Rights Recommendations – Kenya</title>
<style>
  body{font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;margin:0;padding:0;background:#f9f9f9;color:#333;font-size:16px;}
  .container{max-width:1200px;margin:auto;padding:1rem;}
  h1{margin-top:0;color:#1f6fb2;}
  .tabs{display:flex;border-bottom:2px solid #ddd;margin-bottom:1rem;}
  .tab{padding:.5rem 1rem;cursor:pointer;border:1px solid #ddd;border-bottom:none;background:#fff;border-top-left-radius:4px;border-top-right-radius:4px;margin-right:.5rem;}
  .tab.active{background:#fff;color:#1f6fb2;font-weight:600;}
  .tab-content{display:none;}
  .tab-content.active{display:block;}
  .stats{margin-bottom:1rem;}
  .filters{display:flex;flex-wrap:wrap;gap:1rem;margin-bottom:1rem;background:#fff;padding:1rem;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,.1);}
  .filter-group{display:flex;flex-direction:column;}
  .filter-group label{font-weight:600;margin-bottom:.5rem;}
  .filter-group input[type="number"]{width:80px;}
  .filter-group select{width:200px;}
  .filter-group .checkboxes{display:flex;flex-wrap:wrap;gap:.5rem;}
  .filter-group .checkboxes label{font-weight:normal;}
  button{background:#1f6fb2;color:#fff;border:none;padding:.5rem 1rem;border-radius:4px;cursor:pointer;}
  button:hover{background:#155a8e;}
  canvas{max-width:100%;height:auto;}
  table{width:100%;border-collapse:collapse;background:#fff;margin-top:1rem;}
  th,td{padding:.75rem;border:1px solid #ddd;text-align:left;}
  th{background:#f0f0f0;}
  tr.expandable{cursor:pointer;}
  tr.expandable:hover{background:#f5f5f5;}
  tr.fulltext{background:#fafafa;}
  tr.fulltext td{font-size:.9rem;color:#555;}
  .note{font-size:.9rem;color:#666;margin-top:.5rem;}
  .no-records{font-style:italic;color:#666;margin-top:1rem;}
  .state-table{margin-top:1rem;}
  .state-table th{background:#e0e0e0;}
</style>
</head>
<body>
<div class="container">
  <h1>UN Human Rights Recommendations – Kenya</h1>

  <div class="tabs">
    <div class="tab active" data-target="dashboard-section">Dashboard</div>
    <div class="tab" data-target="who-recommends-section">Who recommends what</div>
  </div>

  <div id="dashboard-section" class="tab-content active">
    <div class="stats">
      <span id="record-count"></span> |
      <span id="year-range"></span>
      <div class="note">Data source: <a href="https://docs.un.org/en/" target="_blank">UN Documents</a> (WORKSHOP_DATA.uhri)</div>
    </div>

    <div class="filters">
      <div class="filter-group">
        <label>Mechanism</label>
        <div class="checkboxes" id="mechanism-filters"></div>
      </div>
      <div class="filter-group">
        <label>Year range</label>
        <input type="number" id="year-min" placeholder="From" min="1900" max="2100">
        <input type="number" id="year-max" placeholder="To" min="1900" max="2100">
      </div>
      <div class="filter-group">
        <label>SDG</label>
        <select id="sdg-filter">
          <option value="">All SDGs</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Keyword</label>
        <input type="text" id="keyword-filter" placeholder="Search text">
      </div>
      <div class="filter-group" style="align-self:flex-end;">
        <button id="apply-filters">Apply Filters</button>
      </div>
    </div>

    <div class="chart-section">
      <canvas id="theme-chart"></canvas>
      <div class="note">Bar chart shows the 10 most frequent themes among the filtered records.</div>
    </div>

    <div class="table-section">
      <table id="records-table">
        <thead>
          <tr><th>Date</th><th>Body</th><th>Symbol</th><th>First line</th></tr>
        </thead>
        <tbody></tbody>
      </table>
      <div class="no-records" id="no-records" style="display:none;">No records match the current filter.</div>
    </div>
  </div>

  <div id="who-recommends-section" class="tab-content">
    <div class="stats">
      <span id="upr-count"></span> UPR recommendations found. <span id="missing-state-count"></span> had no recommending state in parentheses.
    </div>
    <div class="chart-section">
      <canvas id="state-chart"></canvas>
      <div class="note">Top 15 states that made the most UPR recommendations to Kenya.</div>
    </div>
    <div class="table-section">
      <table id="state-sdg-table">
        <thead>
          <tr><th>State</th><th>Most frequent SDG</th></tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
    <div class="state-table" id="state-recs-table" style="display:none;">
      <h3>Recommendations by <span id="state-name"></span></h3>
      <table>
        <thead><tr><th>Date</th><th>Body</th><th>Symbol</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
</div>

<script>
(() => {
  const uhri = window.WORKSHOP_DATA.uhri.records || [];
  const sdgNames = window.WORKSHOP_DATA.uhri.sdg_names || {};

  /* ---------- Tab handling ---------- */
  document.querySelectorAll('.tab').forEach(btn=>{
    btn.addEventListener('click',()=>{
      document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
      document.getElementById(btn.dataset.target).classList.add('active');
    });
  });

  /* ---------- Dashboard ---------- */
  const mechanisms = [...new Set(uhri.map(r=>r.mechanism).filter(Boolean))];
  const sdgs = [...new Set(uhri.flatMap(r=>r.sdgs).filter(Boolean))].sort((a,b)=>a-b);
  const years = uhri.map(r=>r.year).filter(Boolean);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);

  const mechDiv=document.getElementById('mechanism-filters');
  mechanisms.forEach(m=>{
    const label=document.createElement('label');
    const cb=document.createElement('input');
    cb.type='checkbox';cb.value=m;cb.checked=true;
    label.appendChild(cb);label.appendChild(document.createTextNode(' '+m));
    mechDiv.appendChild(label);
  });

  const sdgSelect=document.getElementById('sdg-filter');
  sdgs.forEach(s=>{
    const opt=document.createElement('option');
    opt.value=s;opt.textContent=`SDG ${s}`;
    sdgSelect.appendChild(opt);
  });

  document.getElementById('year-min').value=minYear;
  document.getElementById('year-max').value=maxYear;

  document.getElementById('record-count').textContent=`Total records: ${uhri.length}`;
  document.getElementById('year-range').textContent=`Years: ${minYear}–${maxYear}`;

  const ctx=document.getElementById('theme-chart').getContext('2d');
  let themeChart=null;
  function renderThemeChart(themes){
    const labels=themes.map(t=>t.name);
    const counts=themes.map(t=>t.count);
    if(themeChart) themeChart.destroy();
    themeChart=new Chart(ctx,{type:'bar',data:{labels,datasets:[{label:'Theme frequency',data:counts,borderColor:'#1f6fb2',backgroundColor:'#1f6fb2',borderWidth:1}]},
      options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
  }

  const tbody=document.querySelector('#records-table tbody');
  const noRecords=document.getElementById('no-records');
  function firstLine(text){
    if(!text) return '';
    const line=text.split('\n')[0];
    return line.length>100?line.slice(0,97)+'…':line;
  }

  function updateDashboard(){
    const selectedMechs=[...mechDiv.querySelectorAll('input:checked')].map(cb=>cb.value);
    const yearMin=parseInt(document.getElementById('year-min').value)||minYear;
    const yearMax=parseInt(document.getElementById('year-max').value)||maxYear;
    const sdgVal=document.getElementById('sdg-filter').value;
    const keyword=document.getElementById('keyword-filter').value.trim().toLowerCase();

    const filtered=uhri.filter(r=>{
      if(!selectedMechs.includes(r.mechanism)) return false;
      if(r.year<yearMin||r.year>yearMax) return false;
      if(sdgVal && !r.sdgs.includes(parseInt(sdgVal))) return false;
      if(keyword && !r.text.toLowerCase().includes(keyword)) return false;
      return true;
    });

    const themeCounts={};
    filtered.forEach(r=>{
      (r.themes||[]).forEach(t=>{themeCounts[t]=(themeCounts[t]||0)+1;});
    });
    const themeArray=Object.entries(themeCounts).map(([name,count])=>({name,count}));
    themeArray.sort((a,b)=>b.count-a.count);
    renderThemeChart(themeArray.slice(0,10));

    tbody.innerHTML='';
    if(filtered.length===0){
      noRecords.style.display='block';
    }else{
      noRecords.style.display='none';
      filtered.forEach(r=>{
        const tr=document.createElement('tr');
        tr.className='expandable';
        tr.innerHTML=`<td>${r.date||''}</td>
                      <td>${r.body||''}</td>
                      <td>${r.doc_url?`<a href="${r.doc_url}" target="_blank">${r.symbol}</a>`:r.symbol}</td>
                      <td>${firstLine(r.text)}</td>`;
        tbody.appendChild(tr);
        const fullTr=document.createElement('tr');
        fullTr.className='fulltext';
        fullTr.style.display='none';
        fullTr.innerHTML=`<td colspan="4">${r.text||''}</td>`;
        tbody.appendChild(fullTr);
        tr.addEventListener('click',()=>{
          fullTr.style.display=fullTr.style.display==='none'?'table-row':'none';
        });
      });
    }
  }
  document.getElementById('apply-filters').addEventListener('click',updateDashboard);
  updateDashboard();

  /* ---------- Who recommends what ---------- */
  const uprRecords=uhri.filter(r=>r.type==='Recommendations' && r.mechanism==='Universal Periodic Review');
  document.getElementById('upr-count').textContent=`${uprRecords.length}`;
  let missingStateCount=0;
  const stateCounts={};
  const stateSDGs={};

  uprRecords.forEach(r=>{
    const match=r.text.match(/\(([^)]+)\)\s*$/);
    const state=match?match[1].trim():null;
    if(!state){missingStateCount++; return;}
    stateCounts[state]=(stateCounts[state]||0)+1;
    (r.sdgs||[]).forEach(s=>{
      stateSDGs[state]=stateSDGs[state]||{};
      stateSDGs[state][s]=(stateSDGs[state][s]||0)+1;
    });
  });
  document.getElementById('missing-state-count').textContent=`${missingStateCount} had no recommending state in parentheses.`;

  const topStates=Object.entries(stateCounts).sort((a,b)=>b[1]-a[1]).slice(0,15).map(([s,c])=>({state:s,count:c}));
  const stateCtx=document.getElementById('state-chart').getContext('2d');
  let stateChart=null;
  function renderStateChart(){
    const labels=topStates.map(t=>t.state);
    const counts=topStates.map(t=>t.count);
    if(stateChart) stateChart.destroy();
    stateChart=new Chart(stateCtx,{type:'bar',data:{labels,datasets:[{label:'Recommendations',data:counts,borderColor:'#1f6fb2',backgroundColor:'#1f6fb2',borderWidth:1}]},
      options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
    stateChart.canvas.onclick=function(evt){
      const points=stateChart.getElementsAtEventForMode(evt,'nearest',{intersect:true},true);
      if(points.length){
        const idx=points[0].index;
        const state=topStates[idx].state;
        showStateRecs(state);
      }
    };
  }
  renderStateChart();

  const sdgTableBody=document.querySelector('#state-sdg-table tbody');
  topStates.forEach(t=>{
    const sdgsForState=stateSDGs[t.state]||{};
    const sortedSDGs=Object.entries(sdgsForState).sort((a,b)=>b[1]-a[1]);
    const mostSDG=sortedSDGs[0] ? sortedSDGs[0][0] : '';
    const row=document.createElement('tr');
    row.innerHTML=`<td>${t.state}</td><td>${mostSDG?`SDG ${mostSDG} – ${sdgNames[mostSDG]||''}`:''}</td>`;
    sdgTableBody.appendChild(row);
  });

  const stateRecsDiv=document.getElementById('state-recs-table');
  const stateNameSpan=document.getElementById('state-name');
  const stateRecsBody=document.querySelector('#state-recs-table tbody');
  function showStateRecs(state){
    stateNameSpan.textContent=state;
    stateRecsBody.innerHTML='';
    const recs=uprRecords.filter(r=>{
      const match=r.text.match(/\(([^)]+)\)\s*$/);
      return match && match[1].trim()===state;
    });
    recs.forEach(r=>{
      const tr=document.createElement('tr');
      tr.innerHTML=`<td>${r.date||''}</td><td>${r.body||''}</td><td>${r.doc_url?`<a href="${r.doc_url}" target="_blank">${r.symbol}</a>`:r.symbol}</td>`;
      stateRecsBody.appendChild(tr);
    });
    stateRecsDiv.style.display='block';
  }
})();
</script>
</body>
</html>
```