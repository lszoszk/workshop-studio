The page provides a searchable interface for the General Comments dataset, with filtering by committee and year, highlighting of matched terms, and a bar chart of hits per committee.  

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>General Comments Search</title>
<style>
  body{font-family:system-ui,sans-serif;margin:0;padding:1rem;background:#f9f9f9;color:#333}
  h1{font-size:1.8rem;margin-bottom:.5rem}
  .desc{font-size:1rem;margin-bottom:1rem}
  .search-box{margin-bottom:1rem}
  .search-box input{width:100%;padding:.5rem;font-size:1rem}
  .filters{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:1rem}
  .filters label{display:flex;align-items:center;gap:.3rem}
  .results{margin-top:1rem}
  .result{border-bottom:1px solid #ddd;padding:1rem 0}
  .result h3{margin:0 0 .5rem 0;font-size:1.1rem}
  .citation{margin-top:.5rem}
  .citation button{background:#1f6fb2;color:white;border:none;padding:.3rem .6rem;border-radius:4px;cursor:pointer}
  .citation button:hover{background:#155a8c}
  .chart-container{width:100%;max-width:400px;margin-top:1rem}
  .chart-container canvas{width:100%;height:200px}
  mark{background:#fffa87}
</style>
</head>
<body>
<h1>General Comments Search</h1>
<p class="desc" id="desc"></p>

<div class="search-box">
  <input type="text" id="query" placeholder='Search (use AND, OR, NOT, "exact phrases")'>
</div>

<div class="filters">
  <div id="committee-filters"></div>
  <div id="year-filter"></div>
</div>

<button id="search-btn">Search</button>

<div class="chart-container">
  <canvas id="chart"></canvas>
</div>

<div class="results" id="results"></div>

<script>
(() => {
  const data = window.WORKSHOP_DATA.gc || [];
  const desc = document.getElementById('desc');
  const queryInput = document.getElementById('query');
  const committeeFilters = document.getElementById('committee-filters');
  const yearFilter = document.getElementById('year-filter');
  const resultsDiv = document.getElementById('results');
  const searchBtn = document.getElementById('search-btn');
  const chartCtx = document.getElementById('chart').getContext('2d');
  let chart;

  // Utility
  const escapeRegex = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // Build UI
  const committees = [...new Set(data.map(r=>r.committee))].sort();
  const years = [...new Set(data.map(r=>r.year))].sort((a,b)=>a-b);

  committees.forEach(c=>{
    const id = 'chk_'+c.replace(/\s+/g,'_');
    const label = document.createElement('label');
    label.innerHTML = `<input type="checkbox" id="${id}" value="${c}"> ${c}`;
    committeeFilters.appendChild(label);
  });

  const yearSelect = document.createElement('select');
  const allOption = document.createElement('option');
  allOption.value = '';
  allOption.textContent = 'All years';
  yearSelect.appendChild(allOption);
  years.forEach(y=>{
    const opt = document.createElement('option');
    opt.value = y;
    opt.textContent = y;
    yearSelect.appendChild(opt);
  });
  yearFilter.appendChild(yearSelect);

  // Description
  const minYear = Math.min(...years);
  const maxYear = Math.max(...years);
  desc.textContent = `General Comments dataset: ${data.length} records, years ${minYear}-${maxYear}. Search uses AND, OR, NOT, "exact phrases".`;

  // Tokenizer
  function tokenize(str) {
    const tokens = [];
    const regex = /"([^"]+)"|(\bAND\b|\bOR\b|\bNOT\b)|(\S+)/gi;
    let m;
    while ((m = regex.exec(str)) !== null) {
      if (m[1]) tokens.push({type:'PHRASE', value:m[1]});
      else if (m[2]) tokens.push({type:m[2], value:m[2]});
      else if (m[3]) tokens.push({type:'WORD', value:m[3]});
    }
    return tokens;
  }

  // Shunting-yard to postfix
  function toPostfix(tokens) {
    const output = [];
    const stack = [];
    const prec = {NOT:3, AND:2, OR:1};
    tokens.forEach(tok=>{
      if (tok.type==='WORD' || tok.type==='PHRASE') {
        output.push(tok);
      } else if (tok.type==='NOT' || tok.type==='AND' || tok.type==='OR') {
        while (stack.length && prec[stack[stack.length-1].type] >= prec[tok.type]) {
          output.push(stack.pop());
        }
        stack.push(tok);
      }
    });
    while (stack.length) output.push(stack.pop());
    return output;
  }

  // Evaluate postfix against text
  function evaluate(postfix, text) {
    const stack = [];
    const lower = text.toLowerCase();
    postfix.forEach(tok=>{
      if (tok.type==='WORD') {
        const re = new RegExp(`\\b${escapeRegex(tok.value)}\\b`, 'i');
        stack.push(re.test(text));
      } else if (tok.type==='PHRASE') {
        const re = new RegExp(escapeRegex(tok.value), 'i');
        stack.push(re.test(text));
      } else if (tok.type==='NOT') {
        const a = stack.pop();
        stack.push(!a);
      } else if (tok.type==='AND') {
        const b = stack.pop();
        const a = stack.pop();
        stack.push(a && b);
      } else if (tok.type==='OR') {
        const b = stack.pop();
        const a = stack.pop();
        stack.push(a || b);
      }
    });
    return stack.pop() || false;
  }

  // Highlight matches
  function highlight(text, terms) {
    if (!terms.length) return text;
    const pattern = terms.map(t=>escapeRegex(t)).join('|');
    const re = new RegExp(pattern, 'gi');
    return text.replace(re, m=>`<mark>${m}</mark>`);
  }

  // Copy to clipboard
  function copyCitation(symbol, para) {
    const txt = `${symbol}, para. ${para}`;
    navigator.clipboard.writeText(txt).then(()=>alert('Citation copied: '+txt));
  }

  // Search handler
  function performSearch() {
    const query = queryInput.value.trim();
    const selectedComms = Array.from(committeeFilters.querySelectorAll('input:checked')).map(cb=>cb.value);
    const selectedYear = yearFilter.value ? parseInt(yearFilter.value,10) : null;

    const tokens = tokenize(query);
    const postfix = tokens.length ? toPostfix(tokens) : [];
    const terms = tokens.filter(t=>t.type==='WORD' || t.type==='PHRASE').map(t=>t.value);

    const filtered = data.filter(rec=>{
      if (selectedComms.length && !selectedComms.includes(rec.committee)) return false;
      if (selectedYear && rec.year!==selectedYear) return false;
      if (!postfix.length) return true;
      return evaluate(postfix, rec.text);
    });

    // Update chart
    const counts = {};
    committees.forEach(c=>counts[c]=0);
    filtered.forEach(r=>counts[r.committee]++);
    const chartData = {
      labels: committees,
      datasets:[{
        label:'Hits',
        data: committees.map(c=>counts[c]),
        backgroundColor:'#1f6fb2',
        borderColor:'#155a8c',
        borderWidth:1
      }]
    };
    if (chart) chart.destroy();
    chart = new Chart(chartCtx, {
      type:'bar',
      data:chartData,
      options:{
        responsive:true,
        maintainAspectRatio:false,
        plugins:{legend:{display:false}},
        scales:{x:{display:true},y:{display:true, beginAtZero:true, ticks:{stepSize:1}}}
      }
    });

    // Render results
    resultsDiv.innerHTML='';
    if (!filtered.length) {
      resultsDiv.textContent='No matches found.';
      return;
    }
    filtered.forEach(r=>{
      const div = document.createElement('div');
      div.className='result';
      const h3 = document.createElement('h3');
      h3.textContent = `${r.short_title} (${r.committee})`;
      const para = document.createElement('p');
      para.innerHTML = highlight(r.text, terms);
      const cit = document.createElement('div');
      cit.className='citation';
      const btn = document.createElement('button');
      btn.textContent='Copy citation';
      btn.onclick=()=>copyCitation(r.symbol, r.paragraph);
      cit.appendChild(btn);
      div.appendChild(h3);
      div.appendChild(para);
      div.appendChild(cit);
      resultsDiv.appendChild(div);
    });
  }

  searchBtn.addEventListener('click', performSearch);
  queryInput.addEventListener('keypress', e=>{
    if (e.key==='Enter') performSearch();
  });
})();
</script>
</body>
</html>
```