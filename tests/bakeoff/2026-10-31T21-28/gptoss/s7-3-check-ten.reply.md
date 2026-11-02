Added a random SDG check feature with marking and CSV export.  

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>UN Recommendations – Random SDG Check</title>
<style>
  body{font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;font-size:16px;background:#f9f9f9;margin:0;padding:0;}
  .header{background:#1f6fb2;color:#fff;padding:12px;}
  .header h1{margin:0;font-size:1.5rem;}
  .container{max-width:800px;margin:auto;padding:12px;}
  .search{margin-bottom:12px;}
  .search input{padding:6px;width:200px;}
  .search button{padding:6px 12px;background:#1f6fb2;color:#fff;border:none;border-radius:4px;cursor:pointer;}
  .search button:hover{background:#155a8e;}
  .btn{padding:6px 12px;background:#1f6fb2;color:#fff;border:none;border-radius:4px;cursor:pointer;}
  .btn:hover{background:#155a8e;}
  .record{background:#fff;border:1px solid #ddd;border-radius:4px;padding:12px;margin-bottom:12px;}
  .record h3{margin:0 0 4px;}
  .record p{margin:4px 0;}
  .sdg{display:flex;align-items:center;margin-bottom:4px;}
  .sdg span{flex:1;}
  .sdg select{margin-left:8px;}
  .info{margin-bottom:12px;}
  .note{font-size:.9rem;color:#555;}
  .results{margin-top:12px;background:#fff;border:1px solid #ddd;border-radius:4px;padding:12px;}
  .agreement{font-weight:bold;}
  .examples{margin-top:8px;}
  .examples ul{margin:4px 0 0 20px;}
  .download{margin-top:12px;}
  .hidden{display:none;}
  a{color:#1f6fb2;text-decoration:none;}
  a:hover{text-decoration:underline;}
</style>
</head>
<body>
<div class="header"><h1>UN Recommendations – Random SDG Check</h1></div>
<div class="container">
  <div class="info">
    <p id="filterInfo" class="note"></p>
    <p id="selectionInfo" class="note"></p>
  </div>
  <div class="search">
    <input type="text" id="searchInput" placeholder="Search text…">
    <button id="applyFilterBtn" class="btn">Apply Filter</button>
  </div>
  <button id="checkBtn" class="btn">Check 10 at random</button>
  <div id="recordsContainer"></div>
  <div id="resultsContainer" class="results hidden">
    <p class="agreement" id="agreementRate"></p>
    <div class="examples" id="wrongExamples"></div>
    <div class="examples" id="argExamples"></div>
    <div class="download">
      <a id="downloadLink" href="#" download="sdg_marks.csv" class="btn hidden">Download CSV</a>
      <button id="drawAgainBtn" class="btn">Draw again</button>
    </div>
  </div>
</div>
<script>
(() => {
  const data = window.WORKSHOP_DATA.uhri.records || [];
  const sdgNames = window.WORKSHOP_DATA.uhri.sdg_names || {};
  const searchInput = document.getElementById('searchInput');
  const applyFilterBtn = document.getElementById('applyFilterBtn');
  const checkBtn = document.getElementById('checkBtn');
  const recordsContainer = document.getElementById('recordsContainer');
  const resultsContainer = document.getElementById('resultsContainer');
  const agreementRateEl = document.getElementById('agreementRate');
  const wrongExamplesEl = document.getElementById('wrongExamples');
  const argExamplesEl = document.getElementById('argExamples');
  const downloadLink = document.getElementById('downloadLink');
  const drawAgainBtn = document.getElementById('drawAgainBtn');
  const filterInfoEl = document.getElementById('filterInfo');
  const selectionInfoEl = document.getElementById('selectionInfo');

  let filteredRecords = [];
  let selectedRecords = [];
  let marks = {}; // {recordId: [mark, mark, ...]}

  function updateFilterInfo() {
    filterInfoEl.textContent = `Filtered ${filteredRecords.length} record${filteredRecords.length===1?'':'s'}.`;
  }

  function applyFilter() {
    const term = searchInput.value.trim().toLowerCase();
    filteredRecords = data.filter(rec => !term || (rec.text && rec.text.toLowerCase().includes(term)));
    updateFilterInfo();
  }

  function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  function pickRandom10() {
    const arr = shuffle([...filteredRecords]);
    selectedRecords = arr.slice(0, 10);
    selectionInfoEl.textContent = `Showing ${selectedRecords.length} of ${filteredRecords.length} record${selectedRecords.length===1?'':'s'} (random selection).`;
  }

  function renderRecords() {
    recordsContainer.innerHTML = '';
    marks = {};
    selectedRecords.forEach(rec => {
      const div = document.createElement('div');
      div.className = 'record';
      const symbolLink = rec.doc_url ? `<a href="${rec.doc_url}" target="_blank" rel="noopener noreferrer">${rec.symbol}</a>` : rec.symbol;
      div.innerHTML = `
        <h3>${symbolLink} (${rec.year})</h3>
        <p><strong>Body:</strong> ${rec.body || '—'}</p>
        <p>${rec.text || '—'}</p>
        <div class="sdg-list"></div>
      `;
      const sdgList = div.querySelector('.sdg-list');
      if (rec.sdgs && rec.sdgs.length) {
        rec.sdgs.forEach((sdg, idx) => {
          const name = sdgNames[sdg] || `SDG ${sdg}`;
          const select = document.createElement('select');
          select.dataset.recordId = rec.id;
          select.dataset.sdgIndex = idx;
          select.innerHTML = `<option value="">Mark</option><option value="Right">Right</option><option value="Wrong">Wrong</option><option value="Arguable">Arguable</option>`;
          select.addEventListener('change', onMarkChange);
          const sdgDiv = document.createElement('div');
          sdgDiv.className = 'sdg';
          sdgDiv.innerHTML = `<span>${name}</span>`;
          sdgDiv.appendChild(select);
          sdgList.appendChild(sdgDiv);
        });
        marks[rec.id] = Array(rec.sdgs.length).fill('');
      } else {
        sdgList.innerHTML = '<p>No SDGs assigned.</p>';
      }
      recordsContainer.appendChild(div);
    });
    downloadLink.classList.add('hidden');
    resultsContainer.classList.add('hidden');
  }

  function onMarkChange(e) {
    const recId = e.target.dataset.recordId;
    const idx = parseInt(e.target.dataset.sdgIndex, 10);
    marks[recId][idx] = e.target.value;
    if (allMarked()) {
      computeResults();
      downloadLink.classList.remove('hidden');
    } else {
      downloadLink.classList.add('hidden');
    }
  }

  function allMarked() {
    return selectedRecords.every(rec => {
      if (!rec.sdgs || !rec.sdgs.length) return true;
      return marks[rec.id].every(m => m);
    });
  }

  function computeResults() {
    let totalMarks = 0;
    let rightMarks = 0;
    const wrongList = [];
    const argList = [];
    selectedRecords.forEach(rec => {
      if (!rec.sdgs || !rec.sdgs.length) return;
      rec.sdgs.forEach((sdg, idx) => {
        const mark = marks[rec.id][idx];
        totalMarks++;
        if (mark === 'Right') rightMarks++;
        if (mark === 'Wrong') wrongList.push({rec, sdg});
        if (mark === 'Arguable') argList.push({rec, sdg});
      });
    });
    const rate = totalMarks ? ((rightMarks / totalMarks) * 100).toFixed(1) : 0;
    agreementRateEl.textContent = `Agreement rate: ${rate}% (${rightMarks}/${totalMarks} right marks)`;
    wrongExamplesEl.innerHTML = '<strong>Wrong examples:</strong>' + (wrongList.length ? '<ul>' + wrongList.map(w => `<li>${w.rec.symbol} – SDG ${w.sdg}</li>`).join('') + '</ul>' : ' None');
    argExamplesEl.innerHTML = '<strong>Arguable examples:</strong>' + (argList.length ? '<ul>' + argList.map(a => `<li>${a.rec.symbol} – SDG ${a.sdg}</li>`).join('') + '</ul>' : ' None');
    resultsContainer.classList.remove('hidden');
  }

  function generateCSV() {
    let csv = 'Record ID,Symbol,SDG,Mark\n';
    selectedRecords.forEach(rec => {
      if (!rec.sdgs || !rec.sdgs.length) return;
      rec.sdgs.forEach((sdg, idx) => {
        const mark = marks[rec.id][idx];
        csv += `"${rec.id}","${rec.symbol}","${sdg}","${mark}"\n`;
      });
    });
    const blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
    const url = URL.createObjectURL(blob);
    downloadLink.href = url;
  }

  applyFilterBtn.addEventListener('click', () => {
    applyFilter();
    checkBtn.disabled = !filteredRecords.length;
  });

  checkBtn.addEventListener('click', () => {
    if (!filteredRecords.length) return;
    pickRandom10();
    renderRecords();
  });

  drawAgainBtn.addEventListener('click', () => {
    renderRecords();
    downloadLink.classList.add('hidden');
    resultsContainer.classList.add('hidden');
  });

  downloadLink.addEventListener('click', generateCSV);

  // Initial setup
  applyFilter();
  checkBtn.disabled = !filteredRecords.length;
})();
</script>
</body>
</html>
```