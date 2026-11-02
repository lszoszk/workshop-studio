The dashboard displays all UN human‑rights recommendations and observations addressed to Kenya, lets you filter them, and visualises the most frequent themes.  

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
</style>
</head>
<body>
<div class="container">
  <h1>UN Human Rights Recommendations & Observations – Kenya</h1>
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

<script>
(() => {
  const data = window.WORKSHOP_DATA.uhri.records || [];
  const mechanisms = [...new Set(data.map(r=>r.mechanism).filter(Boolean))];
  const sdgs = [...new Set(data.flatMap(r=>r.sdgs).filter(Boolean))].sort((a,b)=>a-b);
  const years = data.map(r=>r.year).filter(Boolean);
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);

  // Populate filters
  const mechDiv = document.getElementById('mechanism-filters');
  mechanisms.forEach(m=>{
    const label = document.createElement('label');
    const cb = document.createElement('input');
    cb.type='checkbox';cb.value=m;cb.checked=true;
    label.appendChild(cb);label.appendChild(document.createTextNode(' '+m));
    mechDiv.appendChild(label);
  });

  const sdgSelect = document.getElementById('sdg-filter');
  sdgs.forEach(s=>{
    const opt=document.createElement('option');
    opt.value=s;opt.textContent=`SDG ${s}`;
    sdgSelect.appendChild(opt);
  });

  // Set year inputs default
  document.getElementById('year-min').value=minYear;
  document.getElementById('year-max').value=maxYear;

  // Stats
  const recCountSpan=document.getElementById('record-count');
  const yearRangeSpan=document.getElementById('year-range');
  recCountSpan.textContent=`Total records: ${data.length}`;
  yearRangeSpan.textContent=`Years: ${minYear}–${maxYear}`;

  // Chart
  const ctx=document.getElementById('theme-chart').getContext('2d');
  let chart=null;
  function renderChart(themes) {
    const labels=themes.map(t=>t.name);
    const counts=themes.map(t=>t.count);
    if(chart) chart.destroy();
    chart=new Chart(ctx,{type:'bar',data:{labels, datasets:[{label:'Theme frequency',data:counts,borderColor:'#1f6fb2',backgroundColor:'#1f6fb2',borderWidth:1}]},
      options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
  }

  // Table
  const tbody=document.querySelector('#records-table tbody');
  const noRecords=document.getElementById('no-records');

  function firstLine(text){
    if(!text) return '';
    const line=text.split('\n')[0];
    return line.length>100?line.slice(0,97)+'…':line;
  }

  function updateView(){
    const selectedMechs = [...mechDiv.querySelectorAll('input:checked')].map(cb=>cb.value);
    const yearMin=parseInt(document.getElementById('year-min').value)||minYear;
    const yearMax=parseInt(document.getElementById('year-max').value)||maxYear;
    const sdgVal=document.getElementById('sdg-filter').value;
    const keyword=document.getElementById('keyword-filter').value.trim().toLowerCase();

    const filtered=data.filter(r=>{
      if(!selectedMechs.includes(r.mechanism)) return false;
      if(r.year<yearMin||r.year>yearMax) return false;
      if(sdgVal && !r.sdgs.includes(parseInt(sdgVal))) return false;
      if(keyword && !r.text.toLowerCase().includes(keyword)) return false;
      return true;
    });

    // Update chart
    const themeCounts={};
    filtered.forEach(r=>{
      (r.themes||[]).forEach(t=>{
        themeCounts[t]= (themeCounts[t]||0)+1;
      });
    });
    const themeArray=Object.entries(themeCounts).map(([name,count])=>({name,count}));
    themeArray.sort((a,b)=>b.count-a.count);
    renderChart(themeArray.slice(0,10));

    // Update table
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

  document.getElementById('apply-filters').addEventListener('click',updateView);

  // Initial render
  updateView();
})();
</script>
</body>
</html>
```