I added a “Suggest SDGs with AI” button that sends the first 50 records of the current filter to a language model in two batches of 25, parses the returned JSON, and displays a side‑by‑side comparison of the UN’s SDGs, the AI’s SDGs, and whether they agree. The page also shows the agreement rate, a notice about the external model, and a “Run again” button that keeps the previous run next to the new one.  

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Human Rights Recommendations Dashboard</title>
<style>
  body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;margin:0;padding:1rem;background:#f9f9f9;color:#333}
  h1{font-size:1.75rem;margin-bottom:.5rem}
  h2{font-size:1.5rem;margin-top:1.5rem;margin-bottom:.5rem}
  p{margin:.5rem 0}
  .accent{color:#1f6fb2}
  .filter{margin:1rem 0}
  .filter input{padding:.5rem;font-size:1rem;width:100%;max-width:400px}
  table{border-collapse:collapse;width:100%;margin-bottom:1rem}
  th,td{border:1px solid #ddd;padding:.5rem;text-align:left}
  th{background:#e0e0e0}
  a{color:#1f6fb2;text-decoration:none}
  a:hover{text-decoration:underline}
  .btn{padding:.5rem 1rem;background:#1f6fb2;color:#fff;border:none;border-radius:4px;font-size:1rem;cursor:pointer}
  .btn:hover{background:#155b8c}
  .status{margin:1rem 0;font-style:italic}
  .results{display:flex;gap:1rem;flex-wrap:wrap}
  .result{flex:1 1 45%;background:#fff;border:1px solid #ddd;border-radius:4px;padding:.5rem}
  .result h3{margin-top:0;font-size:1.2rem}
  .agreement{font-weight:bold}
  .notice{background:#fff8e1;border:1px solid #ffe082;padding:.5rem;margin:1rem 0;border-radius:4px}
  .expand{cursor:pointer;color:#1f6fb2}
  .fulltext{display:none;margin-top:.5rem;background:#f0f0f0;padding:.5rem;border-radius:4px}
  @media(max-width:600px){.results{flex-direction:column}.result{flex:1 1 100%}}
</style>
</head>
<body>
<h1>Human Rights Recommendations Dashboard</h1>
<p id="dataset-info"></p>
<p class="accent">How this is computed: counts are based on the raw data loaded in <code>window.WORKSHOP_DATA</code> before the page loads.</p>

<div class="filter">
  <label for="filter-input">Filter records (any field): </label>
  <input id="filter-input" type="text" placeholder="Type to filter...">
</div>

<h2>Recommendations</h2>
<p id="record-count"></p>
<table id="records-table">
  <thead>
    <tr>
      <th>Symbol</th>
      <th>Year</th>
      <th>Body</th>
      <th>Mechanism</th>
      <th>Type</th>
      <th>Text</th>
    </tr>
  </thead>
  <tbody></tbody>
</table>

<button id="ai-btn" class="btn">Suggest SDGs with AI</button>
<div id="status" class="status"></div>

<div id="results-container" class="results"></div>

<script>
(() => {
  const uhriData = window.WORKSHOP_DATA.uhri;
  const records = Array.isArray(uhriData) ? uhriData : uhriData.records || [];
  const sdgNames = uhriData.sdg_names || {};

  // UI elements
  const datasetInfo = document.getElementById('dataset-info');
  const recordCount = document.getElementById('record-count');
  const filterInput = document.getElementById('filter-input');
  const recordsTableBody = document.querySelector('#records-table tbody');
  const aiBtn = document.getElementById('ai-btn');
  const statusDiv = document.getElementById('status');
  const resultsContainer = document.getElementById('results-container');

  let filtered = records.slice();
  let previousRun = null;
  let currentRun = null;

  // Initialize dataset info
  const years = records.map(r=>r.year).filter(y=>y).sort((a,b)=>a-b);
  const minYear = years[0]||'N/A', maxYear = years[years.length-1]||'N/A';
  datasetInfo.textContent = `Source: UN Human Rights Instruments, ${records.length} records, Years ${minYear}–${maxYear}`;

  // Render records table
  function renderTable() {
    recordsTableBody.innerHTML = '';
    recordCount.textContent = `Showing ${filtered.length} of ${records.length} records`;
    filtered.forEach(rec=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a href="${rec.doc_url}" target="_blank">${rec.symbol}</a></td>
        <td>${rec.year||'—'}</td>
        <td>${rec.body||'—'}</td>
        <td>${rec.mechanism||'—'}</td>
        <td>${rec.type||'—'}</td>
        <td class="expand">Show text</td>
      `;
      const fullDiv = document.createElement('div');
      fullDiv.className = 'fulltext';
      fullDiv.textContent = rec.text || '';
      tr.appendChild(fullDiv);
      tr.querySelector('.expand').addEventListener('click', ()=> {
        fullDiv.style.display = fullDiv.style.display==='none'?'block':'none';
      });
      recordsTableBody.appendChild(tr);
    });
  }

  // Filter logic
  filterInput.addEventListener('input', ()=>{
    const val = filterInput.value.trim().toLowerCase();
    filtered = records.filter(r=>{
      return Object.values(r).some(v=>{
        if (!v) return false;
        if (Array.isArray(v)) return v.some(e=>String(e).toLowerCase().includes(val));
        return String(v).toLowerCase().includes(val);
      });
    });
    renderTable();
  });

  // AI suggestion logic
  async function runAI() {
    const toSuggest = filtered.slice(0,50);
    if (toSuggest.length===0) {
      statusDiv.textContent = 'No records to suggest.';
      return;
    }
    statusDiv.textContent = `Preparing to send ${toSuggest.length} records to AI...`;
    const batches = [];
    for (let i=0;i<toSuggest.length;i+=25) batches.push(toSuggest.slice(i,i+25));

    const aiResults = {};
    for (let i=0;i<batches.length;i++) {
      const batch = batches[i];
      statusDiv.textContent = `Sending batch ${i+1} of ${batches.length} to AI...`;
      const prompt = `Please assign SDG numbers (1-17) to the following records based on their content. Return a JSON object mapping record IDs to an array of SDG numbers. Do not include any other text. Records:\n\n` +
        batch.map(r=>`ID: ${r.id}\nText: ${r.text}`).join('\n\n');
      let response;
      try {
        response = await studio.ask(prompt, {json:true});
      } catch (e) {
        statusDiv.textContent = `Error contacting AI: ${e}`;
        return;
      }
      let parsed;
      try {
        parsed = JSON.parse(response);
      } catch (e) {
        statusDiv.textContent = `AI returned invalid JSON.`;
        return;
      }
      Object.assign(aiResults, parsed);
    }
    statusDiv.textContent = 'AI suggestions completed.';
    // Build run data
    const runData = toSuggest.map(r=>{
      const unSDGs = r.sdgs || [];
      const aiSDGs = aiResults[r.id] || [];
      const agree = arraysEqual(unSDGs.sort(), aiSDGs.sort());
      return {id:r.id, symbol:r.symbol, doc_url:r.doc_url, unSDGs, aiSDGs, agree};
    });
    // Update runs
    previousRun = currentRun;
    currentRun = runData;
    displayResults();
  }

  function arraysEqual(a,b){
    if (a.length!==b.length) return false;
    for (let i=0;i<a.length;i++) if (a[i]!==b[i]) return false;
    return true;
  }

  function displayResults() {
    resultsContainer.innerHTML = '';
    if (!currentRun) return;
    const left = document.createElement('div');
    left.className='result';
    if (previousRun) {
      left.innerHTML = `<h3>Previous Run</h3>`;
      left.appendChild(buildTable(previousRun));
    } else {
      left.innerHTML = `<h3>No previous run</h3>`;
    }
    const right = document.createElement('div');
    right.className='result';
    right.innerHTML = `<h3>Current Run</h3>`;
    right.appendChild(buildTable(currentRun));
    resultsContainer.appendChild(left);
    resultsContainer.appendChild(right);
    // Agreement rate
    const agreeCount = currentRun.filter(r=>r.agree).length;
    const rate = ((agreeCount/currentRun.length)*100).toFixed(1);
    const notice = document.createElement('div');
    notice.className='notice';
    notice.innerHTML = `<p class="agreement">Agreement rate: ${rate}% (${agreeCount}/${currentRun.length})</p>
      <p>These 50 texts were sent to OpenAI GPT‑4. Running again may give different answers.</p>`;
    resultsContainer.appendChild(notice);
  }

  function buildTable(data){
    const table = document.createElement('table');
    table.innerHTML = `<thead><tr><th>Record</th><th>UN SDGs</th><th>AI SDGs</th><th>Agree?</th></tr></thead><tbody></tbody>`;
    const tbody = table.querySelector('tbody');
    data.forEach(r=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><a href="${r.doc_url}" target="_blank">${r.symbol}</a></td>
        <td>${r.unSDGs.length?r.unSDGs.join(', '):'None'}</td>
        <td>${r.aiSDGs.length?r.aiSDGs.join(', '):'None'}</td>
        <td>${r.agree?'Yes':'No'}</td>
      `;
      tbody.appendChild(tr);
    });
    return table;
  }

  aiBtn.addEventListener('click', runAI);

  // Initial render
  renderTable();
})();
</script>
</body>
</html>
```