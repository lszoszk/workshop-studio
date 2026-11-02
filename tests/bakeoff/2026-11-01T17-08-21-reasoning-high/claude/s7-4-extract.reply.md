I built a tool that splits the document into numbered paragraphs, removes repeated headers and footers, and keeps footnotes out of the text. It compares the count and the first six words of each paragraph with the reference, and clicking a row shows the full paragraph. I only saw the first page as a sample, so check the "What was removed" section on screen to confirm the cleaning matches the real pages.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraph splitter</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#f6f8fa;color:#1d2b36}
main{max-width:1100px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:28px;margin:0 0 4px}
h2{font-size:19px;margin:28px 0 8px}
.sub{color:#51606d;margin:0 0 18px}
a{color:#1f6fb2}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:18px 0}
.card{background:#fff;border:1px solid #d9e0e6;border-radius:8px;padding:14px 16px;border-top:4px solid #1f6fb2}
.card.warn{border-top-color:#c77700}
.card.ok{border-top-color:#2e8540}
.card .big{font-size:30px;font-weight:700;line-height:1.1}
.card .lbl{color:#51606d;font-size:14px}
.note{background:#eaf3fb;border-left:4px solid #1f6fb2;padding:10px 14px;border-radius:4px;font-size:15px;margin:12px 0}
.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:14px 0}
.controls input[type=text],.controls select{font:inherit;padding:6px 10px;border:1px solid #b9c4cd;border-radius:6px;background:#fff}
button{font:inherit;background:#1f6fb2;color:#fff;border:0;border-radius:6px;padding:8px 16px;cursor:pointer}
button:hover{background:#185a93}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #d9e0e6}
th,td{padding:8px 10px;text-align:left;vertical-align:top;border-bottom:1px solid #e5eaee}
th{background:#eef2f5;font-size:14px;position:sticky;top:0}
tr.row{cursor:pointer}
tr.row:hover{background:#f1f7fc}
tr.row.open{background:#e3eff9}
td.num{width:60px;font-weight:700}
td.pg{width:60px;color:#51606d}
td.st{width:150px;white-space:nowrap}
.badge{display:inline-block;padding:1px 9px;border-radius:12px;font-size:13px;font-weight:600}
.b-match{background:#e2f3e6;color:#1f6a30}
.b-differs,.b-missing,.b-extra{background:#fdeacc;color:#8a4b00}
.b-noref{background:#e8ecef;color:#51606d}
tr.diff td.num{color:#a35a00}
tr.detail td{background:#fbfcfd;padding:14px 18px}
.full{white-space:pre-wrap;background:#fff;border:1px solid #d9e0e6;border-radius:6px;padding:12px 14px;margin:8px 0}
.cmp{font-size:14px;color:#33434f}
.cmp code{background:#eef2f5;padding:1px 5px;border-radius:3px}
details{background:#fff;border:1px solid #d9e0e6;border-radius:6px;padding:8px 14px;margin:10px 0}
summary{cursor:pointer;font-weight:600}
details ul{margin:8px 0;padding-left:20px;font-size:14px}
.muted{color:#51606d;font-size:14px}
</style>
</head>
<body>
<main>
  <h1>Numbered paragraphs from a UN document</h1>
  <p class="sub" id="desc"></p>
  <div id="app"></div>
</main>
<script>
(function(){
const D = window.WORKSHOP_DATA || {};
const P = D.pdf_text || {};
const pages = (Array.isArray(P.records) ? P.records : []).slice().sort((a,b)=>(a.page||0)-(b.page||0));
const ref = P.reference || {};
const refWords = ref.first_words || {};
const esc = s => String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const app = document.getElementById('app');

document.getElementById('desc').innerHTML =
  esc(P.title||'Document') + ' — ' + (P.doc_url ? '<a href="'+esc(P.doc_url)+'" target="_blank" rel="noopener">'+esc(P.symbol||'document')+'</a>' : esc(P.symbol||''))
  + ' · source: ' + esc(P.source||'PDF text') + ' · ' + pages.length + ' pages of raw PDF text'
  + (ref.adopted ? ' · adopted: ' + esc(ref.adopted) : '');

if(!pages.length){ app.innerHTML = '<div class="note">No PDF text is available in the data, so there is nothing to split.</div>'; return; }

/* ---------- helpers ---------- */
const norm = l => l.trim().toLowerCase().replace(/\d+/g,'#').replace(/\s+/g,' ');
const pageLines = p => String(p.text||'').replace(/\r/g,'').split('\n').map(s=>s.replace(/\u00ad/g,'').replace(/\s+/g,' ').trim());
const symCompact = String(P.symbol||'').replace(/\s+/g,'');

function words6(t){
  return String(t||'').split(/\s+/).map(w=>w.toLowerCase().replace(/[^\p{L}\p{N}]+/gu,'')).filter(Boolean).slice(0,6).join(' ');
}

/* repeated lines near the top/bottom of many pages = running headers/footers */
const edgeCounts = {};
pages.forEach(p=>{
  const ls = pageLines(p).filter(Boolean);
  const set = new Set();
  ls.slice(0,4).concat(ls.slice(-4)).forEach(l=>{
    if(l.length<100 && /[a-z]{2,}/i.test(l) && !/^\d{1,3}\.(\s|$)/.test(l)) set.add(norm(l));
  });
  set.forEach(k=>{ edgeCounts[k]=(edgeCounts[k]||0)+1; });
});
const minPages = Math.max(3, Math.ceil(pages.length*0.3));
const repeated = new Set(Object.keys(edgeCounts).filter(k=>edgeCounts[k]>=minPages));

function cleanPage(p,res){
  const ls = pageLines(p).filter(Boolean), n = ls.length, out = [];
  ls.forEach((l,i)=>{
    const edge = i<4 || i>=n-4;
    let why = null;
    if(edge){
      if(symCompact && l.replace(/\s+/g,'')===symCompact) why='document symbol in header/footer';
      else if(/^GE\.\d{2}-\d{3,6}/.test(l)) why='UN print code (GE.xx-xxxxx)';
      else if(/^(page\s*)?\d+\s*(\/|of)\s*\d+$/i.test(l)) why='page number';
      else if(/^\d{1,3}$/.test(l) && (i===0||i===n-1) && Math.abs(+l-(p.page||0))<=3) why='page number';
      else if(repeated.has(norm(l))) why='line repeated at the edge of many pages';
    }
    if(why){
      const k = why+'|'+norm(l);
      if(!res.removed[k]) res.removed[k]={why:why,example:l,pages:[]};
      res.removed[k].pages.push(p.page);
    } else out.push(l);
  });
  return out;
}

const PARA = /^(\d{1,3})\.(?!\d)\s*(.*)$/;
const FN = /^(\d{1,3})(?![\d.])\s*(.*)$/;
const isFnStart = (l,n,loose) => {
  const m = FN.exec(l); if(!m) return null;
  const k = +m[1], rest = m[2];
  const okNum = loose ? (k>=n && k<=n+3) : k===n;
  if(okNum && (rest==='' || /^[A-Z“"‘'(\[]/.test(rest))) return {n:k,rest:rest};
  return null;
};

const sentEnd = s => /[.!?”"’]$/.test(s);
const isMarker = s => /^([IVX]{1,5}|[A-Z])\.$/.test(s) || (/^([IVX]{1,5}|[A-Z])\.\s+\S.{0,90}$/.test(s) && !/[.;,:]$/.test(s));
const headLike = s => s.length<=100 && /^[A-Z]/.test(s) && !/[.;,:]$/.test(s);
function trimHeadings(ls){
  ls = ls.slice();
  let changed = true;
  while(ls.length>1 && changed){
    changed = false;
    const last = ls[ls.length-1], prev = ls[ls.length-2];
    if(isMarker(last) || (headLike(last) && (sentEnd(prev) || isMarker(prev)))){ ls.pop(); changed=true; }
  }
  return ls;
}
function joinLines(ls){
  let t = '';
  ls.forEach(l=>{
    if(!t) t = l;
    else if(/-$/.test(t) && /^[a-z]/.test(l)) t += l;
    else t += ' ' + l;
  });
  return t.replace(/\s+/g,' ').trim();
}

/* ---------- main parse ---------- */
function parse(stripCalls){
  const res = {paras:[], footnotes:[], removed:{}, gaps:[], calls:0};
  let cur = null, last = 0, nextFn = 1;

  const finish = () => {
    if(!cur) return;
    let t = joinLines(trimHeadings(cur.lines));
    if(stripCalls){
      t = t.replace(/([A-Za-z\u00c0-\u024f)”’"][.,;:])(\d{1,3})(?=\s|$)/g,(m,a)=>{ res.calls++; return a; });
    }
    res.paras.push({num:cur.num, page:cur.page, text:t});
    cur = null;
  };

  pages.forEach(p=>{
    const ls = cleanPage(p,res);
    /* where does the footnote block of this page start? */
    let sep=-1, cand=-1, star=-1;
    ls.forEach((l,i)=>{
      if(/^[_\-–—=]{5,}$/.test(l)) sep=i;
      if(isFnStart(l,nextFn,false)) cand=i;
      if(star<0 && /^\*\s*\S/.test(l)) star=i;
    });
    let zone = (sep>=0 && (cand<0 || sep<=cand)) ? sep : cand;
    if(zone<0) zone = star;
    let inZone = false;

    ls.forEach((l,i)=>{
      if(i===zone) inZone = true;
      const m = PARA.exec(l);
      if(m){
        const n = +m[1], rest = m[2];
        let ok = false, gap = false;
        if(n===last+1) ok = true;
        else if(last>0 && n>last+1 && n<=last+5 && rest==='' && !inZone){ ok = true; gap = true; }
        if(ok){
          if(gap) for(let g=last+1; g<n; g++) res.gaps.push(g);
          finish();
          cur = {num:n, page:p.page, lines: rest ? [rest] : []};
          last = n; inZone = false;
          return;
        }
      }
      if(!cur && last===0 && !inZone) return;           /* front matter before paragraph 1 */
      if(inZone){
        if(/^[_\-–—=]{5,}$/.test(l)) return;
        const f = isFnStart(l,nextFn,true);
        if(f){ res.footnotes.push({n:f.n,text:f.rest,page:p.page}); nextFn = f.n+1; }
        else if(/^\*\s*\S/.test(l)) res.footnotes.push({n:null,text:l,page:p.page});
        else if(res.footnotes.length) res.footnotes[res.footnotes.length-1].text += ' ' + l;
        return;
      }
      if(cur) cur.lines.push(l);
    });
  });
  finish();
  return res;
}

/* ---------- compare with the reference ---------- */
function buildRows(res){
  const hasRef = Object.keys(refWords).length>0;
  const rows = [], seen = new Set();
  res.paras.forEach(pa=>{
    seen.add(pa.num);
    const found = words6(pa.text), exp = refWords[pa.num];
    let st;
    if(!hasRef) st='noref';
    else if(exp==null) st='extra';
    else st = (words6(exp)===found) ? 'match' : 'differs';
    rows.push({num:pa.num,page:pa.page,text:pa.text,status:st,found:found,expected:exp==null?'':exp});
  });
  Object.keys(refWords).forEach(k=>{
    const n = +k;
    if(!seen.has(n)) rows.push({num:n,page:'',text:'',status:'missing',found:'',expected:refWords[k]});
  });
  rows.sort((a,b)=>a.num-b.num);
  return rows;
}
const LABEL = {match:'matches reference',differs:'first words differ',missing:'not found',extra:'not in reference',noref:'no reference'};

/* ---------- render ---------- */
let state = {strip:true, filter:'all', q:'', res:null, rows:[]};

function render(){
  const res = state.res = parse(state.strip);
  const rows = state.rows = buildRows(res);
  const found = res.paras.length;
  const refN = ref.paragraphs;
  const diff = rows.filter(r=>r.status==='differs').length;
  const missing = rows.filter(r=>r.status==='missing').length;
  const extra = rows.filter(r=>r.status==='extra').length;
  const compared = rows.filter(r=>r.status==='match'||r.status==='differs').length;
  const fnNumbered = res.footnotes.filter(f=>f.n!=null).length;
  const sameCount = refN!=null && found===refN;
  const sameFn = ref.footnotes!=null && fnNumbered===ref.footnotes;

  app.innerHTML =
  '<div class="cards">'
  + '<div class="card '+(sameCount?'ok':'warn')+'"><div class="big">'+found+' <span class="muted">/ '+(refN!=null?refN:'?')+'</span></div><div class="lbl">paragraphs found / paragraphs the document really has</div></div>'
  + '<div class="card '+(diff||missing||extra?'warn':'ok')+'"><div class="big">'+diff+'</div><div class="lbl">paragraphs whose first words differ from the reference (of '+compared+' compared); '+missing+' not found, '+extra+' not in reference</div></div>'
  + '<div class="card '+(sameFn?'ok':'warn')+'"><div class="big">'+fnNumbered+' <span class="muted">/ '+(ref.footnotes!=null?ref.footnotes:'?')+'</span></div><div class="lbl">footnotes set aside / footnotes the document has</div></div>'
  + '</div>'
  + '<div class="note"><b>How this is computed.</b> The code reads the '+pages.length+' pages in order. It deletes lines that repeat at the top or bottom of many pages (running headers, print codes, page numbers). A line like “12.” starts paragraph 12 only if 11 came just before. Section headings (I., A., short titles) are cut off the end of the paragraph before them. On each page, everything from the footnote separator or from the first numbered footnote to the bottom of the page goes into the footnote list, not into the paragraph text. Text before paragraph 1 (cover, title) is ignored. “First words differ” means the first six words, ignoring capitals and punctuation, are not the same as <code>reference.first_words</code>. Everything here is counted by code, nothing is estimated.</div>'
  + '<div class="controls">'
  + '<label>Show <select id="flt"><option value="all">all paragraphs</option><option value="diff">only differences / problems</option></select></label>'
  + '<input type="text" id="q" placeholder="Search number or text…" size="26">'
  + '<label><input type="checkbox" id="strip"> remove footnote call numbers glued to punctuation (e.g. “rights.12”)</label>'
  + '<button id="csv">Download CSV</button>'
  + '</div>'
  + '<p class="muted" id="count"></p>'
  + '<table><thead><tr><th>No.</th><th>Page</th><th>Check</th><th>First line of the paragraph (click a row for the full text)</th></tr></thead><tbody id="tb"></tbody></table>'
  + diagnostics(res,rows);

  document.getElementById('flt').value = state.filter;
  document.getElementById('q').value = state.q;
  document.getElementById('strip').checked = state.strip;
  document.getElementById('flt').onchange = e=>{state.filter=e.target.value; fill();};
  document.getElementById('q').oninput = e=>{state.q=e.target.value; fill();};
  document.getElementById('strip').onchange = e=>{state.strip=e.target.checked; render();};
  document.getElementById('csv').onclick = downloadCsv;
  document.getElementById('tb').onclick = toggle;
  fill();
}

function fill(){
  const q = state.q.trim().toLowerCase();
  const list = state.rows.filter(r=>{
    if(state.filter==='diff' && (r.status==='match'||r.status==='noref')) return false;
    if(q && !(String(r.num)===q || r.text.toLowerCase().includes(q) || r.expected.toLowerCase().includes(q))) return false;
    return true;
  });
  document.getElementById('count').textContent = 'Showing '+list.length+' of '+state.rows.length+' rows.';
  document.getElementById('tb').innerHTML = list.map(r=>{
    const first = r.text ? (r.text.length>110 ? r.text.slice(0,110).replace(/\s+\S*$/,'')+' …' : r.text) : '(paragraph not found in the text; the reference starts: “'+r.expected+'”)';
    return '<tr class="row'+(r.status==='match'||r.status==='noref'?'':' diff')+'" data-n="'+r.num+'"><td class="num">'+r.num+'</td><td class="pg">'+esc(r.page)+'</td><td class="st"><span class="badge b-'+r.status+'">'+LABEL[r.status]+'</span></td><td>'+esc(first)+'</td></tr>';
  }).join('') || '<tr><td colspan="4" class="muted">No rows match this filter.</td></tr>';
}

function toggle(e){
  const tr = e.target.closest('tr.row'); if(!tr) return;
  const nxt = tr.nextElementSibling;
  if(nxt && nxt.classList.contains('detail')){ nxt.remove(); tr.classList.remove('open'); return; }
  const r = state.rows.find(x=>x.num===+tr.dataset.n); if(!r) return;
  const d = document.createElement('tr'); d.className='detail';
  const link = P.doc_url ? '<a href="'+esc(P.doc_url)+'" target="_blank" rel="noopener">'+esc(P.symbol||'document')+'</a>' : esc(P.symbol||'');
  d.innerHTML = '<td colspan="4"><b>'+link+', para. '+r.num+'</b>'+(r.page!==''?' · starts on PDF page '+esc(r.page)+' · '+r.text.length+' characters':'')
    + (r.text ? '<div class="full">'+esc(r.text)+'</div>' : '<div class="full">This paragraph number was not found in the extracted text.</div>')
    + '<div class="cmp">First six words found: <code>'+esc(r.found||'—')+'</code><br>First six words in the reference: <code>'+esc(r.expected||'—')+'</code></div></td>';
  tr.after(d); tr.classList.add('open');
}

function diagnostics(res,rows){
  const rem = Object.values(res.removed);
  const remHtml = rem.length ? rem.map(x=>'<li><code>'+esc(x.example)+'</code> — '+esc(x.why)+', removed on '+x.pages.length+' page(s)</li>').join('') : '<li>Nothing was removed.</li>';
  const fnHtml = res.footnotes.slice(0,12).map(f=>'<li>'+(f.n!=null?f.n:'*')+' (page '+esc(f.page)+'): '+esc(f.text.length>140?f.text.slice(0,140)+' …':f.text)+'</li>').join('');
  return '<h2>What was removed</h2>'
   + '<details><summary>Headers, footers and page numbers removed ('+rem.length+' kinds)</summary><ul>'+remHtml+'</ul></details>'
   + '<details><summary>Footnotes kept out of the paragraphs ('+res.footnotes.length+')</summary><ul>'+(fnHtml||'<li>No footnotes detected.</li>')+'</ul>'+(res.footnotes.length>12?'<p class="muted">First 12 shown.</p>':'')+'</details>'
   + '<details><summary>Other notes</summary><ul>'
   + '<li>Footnote call numbers removed from the text: '+res.calls+(state.strip?'':' (option switched off)')+'.</li>'
   + '<li>Paragraph numbers skipped while reading (gaps in the sequence): '+(res.gaps.length?res.gaps.join(', '):'none')+'.</li>'
   + '</ul></details>';
}

function downloadCsv(){
  const q = s => '"'+String(s==null?'':s).replace(/"/g,'""')+'"';
  const head = ['symbol','paragraph','pdf_page','check','first_six_words_found','first_six_words_reference','characters','text'];
  const lines = [head.join(',')];
  state.rows.forEach(r=>{
    lines.push([q(P.symbol||''),r.num,q(r.page),q(LABEL[r.status]),q(r.found),q(r.expected),r.text.length,q(r.text)].join(','));
  });
  const blob = new Blob(['\ufeff'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = String(P.symbol||'document').replace(/[^\w.-]+/g,'_')+'_paragraphs.csv';
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),2000);
}

render();
})();
</script>
</body>
</html>
```