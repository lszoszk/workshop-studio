Built as planned: one screen, verbatim search over every paragraph in the file, ready-to-copy citations, and a draft list you can copy or download. Nothing leaves the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: the rights of the child</title>
<style>
  :root{
    --paper:#f4f0e8; --ink:#1d1b18; --rule:#d9d2c3; --accent:#9b2335;
  }
  *{box-sizing:border-box}
  [hidden]{display:none!important}
  body{margin:0;background:var(--paper);color:var(--ink);
       font:16px/1.55 -apple-system,"Segoe UI",system-ui,sans-serif;padding:0 24px 60px}
  .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;
        letter-spacing:.08em;text-transform:uppercase;color:#6b6355}
  header{border-bottom:1px solid var(--rule);padding:22px 0 14px}
  header h1{font-family:Georgia,"Times New Roman",serif;font-size:30px;margin:6px 0 4px;font-weight:normal}
  .srcline{font-size:13px;color:#6b6355}
  .searchbar{display:flex;gap:10px;align-items:center;margin:22px 0 6px;flex-wrap:wrap}
  #q{flex:1;min-width:260px;font:18px Georgia,serif;padding:10px 12px;border:1px solid var(--rule);
     background:#fff;color:var(--ink)}
  #q:focus{outline:2px solid var(--accent);outline-offset:1px}
  button{font:13px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.05em;
         background:none;border:1px solid var(--rule);color:var(--ink);
         padding:8px 12px;cursor:pointer}
  button:hover{border-color:var(--ink)}
  button:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
  button.accent{border-color:var(--accent);color:var(--accent)}
  .examples{margin:8px 0 0;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
  .bignum{font-family:Georgia,serif;font-size:46px;margin:18px 0 0;line-height:1}
  .bignum small{font-size:16px;font-family:inherit;color:#6b6355}
  .hint{font-size:13px;color:#6b6355;margin:4px 0 0}
  mark{background:#f3ddab;padding:0 1px}
  .result{border-top:1px solid var(--rule);padding:16px 0}
  .rhead{display:flex;gap:14px;flex-wrap:wrap;align-items:baseline;margin-bottom:6px}
  .rhead .committee{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;
        letter-spacing:.08em;color:var(--accent)}
  .rhead a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--rule)}
  .rhead a:hover{border-color:var(--accent)}
  .rtitle{font-family:Georgia,serif;font-size:15px;font-style:italic;color:#4a443a}
  .rtext{margin:8px 0 10px;max-width:70ch;white-space:pre-wrap}
  .racts{display:flex;gap:8px}
  #draft{margin-top:40px;border-top:2px solid var(--ink);padding-top:14px}
  #draftList .result{border-top:1px solid var(--rule)}
  .note{border-top:1px solid var(--rule);margin-top:44px;padding-top:14px;
        font-size:14px;color:#4a443a;max-width:70ch}
  .note h2{font-family:Georgia,serif;font-size:18px;font-weight:normal;margin:0 0 6px;color:var(--ink)}
  .toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
         background:var(--ink);color:var(--paper);padding:8px 16px;font-size:13px;
         font-family:ui-monospace,Menlo,Consolas,monospace}
</style>
</head>
<body>
<header>
  <div class="mono" id="dataLabel"></div>
  <h1>Verbatim finder: the rights of the child</h1>
  <div class="srcline" id="srcLine"></div>
</header>

<div class="searchbar">
  <input id="q" type="search" placeholder='Type words, or "a phrase in quotation marks"' aria-label="Search paragraphs">
  <button id="go" class="accent">SEARCH</button>
</div>
<div class="examples">
  <span class="mono">Examples</span>
  <button class="ex" data-q="&quot;best interests of the child&quot;">"best interests of the child"</button>
  <button class="ex" data-q="child participation">child participation</button>
  <button class="ex" data-q="&quot;evolving capacities&quot;">"evolving capacities"</button>
</div>
<p class="hint">All words must appear in the paragraph, in any order; words in quotation marks must appear together, word for word. Case and apostrophe shape (’ or ') are ignored; a word also finds its longer forms (child finds children). Literal match, not synonyms.</p>

<div class="bignum" id="matchCount">0 <small>matching paragraphs</small></div>
<div class="mono" id="searched"></div>
<div id="results"></div>
<div id="nomatch" hidden>
  <p>No paragraph contains what you typed. The words must all appear, exactly as spelled (apart from case and apostrophes); there are no synonyms and no paraphrase.</p>
</div>

<section id="draft" hidden>
  <div class="mono">Draft list</div>
  <div style="display:flex;gap:8px;margin:8px 0 4px">
    <button id="copyAll">COPY ALL</button>
    <button id="download">DOWNLOAD .TXT</button>
    <button id="clearDraft">CLEAR</button>
  </div>
  <div id="draftList"></div>
</section>

<div class="note">
  <h2>How this is computed, and what it cannot do</h2>
  <p id="howComputed"></p>
  <p><strong>Cannot do:</strong> no summaries, paraphrase or synonyms — only the words you typed; no sources beyond this file (no concluding observations, no case law); English only, no translation. A symbol is not always one document: some symbols hold several General Comments, and joint General Comments carry two symbols in one field; the citation adds the short title when a symbol holds more than one. The text is shown exactly as stored, including footnote marks such as [[fn:12]].</p>
</div>

<script>
(function(){
  const data = WORKSHOP_DATA.gc;
  const records = data.records || [];

  document.getElementById('dataLabel').textContent = data.title || 'General Comments';
  document.getElementById('srcLine').textContent =
    (data.source ? data.source + ' · ' : '') + (data.count != null ? data.count : records.length) + ' paragraphs';

  // symbols that hold more than one title
  const titlesBySymbol = {};
  records.forEach(r=>{
    (titlesBySymbol[r.symbol] = titlesBySymbol[r.symbol] || new Set()).add(r.title);
  });

  const norm = s => (s||'')
    .replace(/[\u2018\u2019\u02BC']/g,"'")
    .replace(/[\u201C\u201D]/g,'"')
    .toLowerCase();

  // parse query into {phrases:[], words:[]}
  function parseQuery(q){
    const phrases=[], words=[];
    const re=/"([^"]+)"/g; let m, rest=q;
    while((m=re.exec(q))!==null){ phrases.push(m[1].trim()); }
    rest = q.replace(re,' ');
    rest.split(/\s+/).filter(Boolean).forEach(w=>words.push(w));
    return {phrases:phrases.filter(Boolean), words:words};
  }

  function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

  // highlight all matched words/phrases in text
  function highlight(text, parsed){
    let html = esc(text);
    const terms = [];
    parsed.phrases.forEach(p=>terms.push({re:new RegExp('('+p.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi'), phrase:true}));
    parsed.words.forEach(w=>{
      const n = norm(w).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
      terms.push({re:new RegExp('\\b('+n+'\\w*)\\b','gi'), phrase:false});
    });
    // apply sequentially on text nodes only: simpler — apply to whole string, avoiding nested marks is rare; do phrase first
    terms.sort((a,b)=>(b.phrase?1:0)-(a.phrase?1:0));
    terms.forEach(t=>{ html = html.replace(t.re,'<mark>$1</mark>'); });
    return html;
  }

  function matches(r, parsed){
    const t = norm(r.text);
    for(const p of parsed.phrases){
      if(t.indexOf(norm(p))===-1) return false;
    }
    for(const w of parsed.words){
      const n = norm(w);
      if(!new RegExp('\\b'+n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\w*\\b').test(t)) return false;
    }
    return true;
  }

  function citation(r){
    const multi = titlesBySymbol[r.symbol] && titlesBySymbol[r.symbol].size > 1;
    return multi ? r.symbol + ', para. ' + r.paragraph + ' (' + r.short_title + ')'
                 : r.symbol + ', para. ' + r.paragraph;
  }

  const draft = new Map(); // id -> record

  function resultHTML(r, parsed){
    const cit = citation(r);
    return '<article class="result" id="res-'+r.id+'">' +
      '<div class="rhead">' +
      '<span class="committee">'+esc(r.committee||'')+'</span>' +
      '<a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>' +
      '<span class="mono">para. '+r.paragraph+'</span>' +
      '<span class="rtitle">'+esc(r.short_title||r.title||'')+'</span>' +
      '</div>' +
      '<p class="rtext">'+highlight(r.text, parsed)+'</p>' +
      '<div class="racts">' +
      '<button data-copy="'+esc(cit)+'">COPY CITATION</button>' +
      '<button data-add="'+r.id+'">ADD TO DRAFT</button>' +
      '</div></article>';
  }

  const el = id=>document.getElementById(id);
  const resultsEl=el('results'), countEl=el('matchCount'), noEl=el('nomatch');
  let lastParsed=null;

  function runSearch(){
    const q = el('q').value.trim();
    lastParsed = parseQuery(q);
    const hasTerms = lastParsed.phrases.length || lastParsed.words.length;
    const hits = hasTerms ? records.filter(r=>matches(r,lastParsed)) : [];
    countEl.innerHTML = hits.length + ' <small>matching paragraphs</small>';
    el('searched').textContent = records.length + ' paragraphs searched';
    noEl.hidden = hits.length>0 || !hasTerms;
    resultsEl.innerHTML = hits.map(r=>resultHTML(r,lastParsed)).join('');
  }

  function toast(msg){
    const t=document.createElement('div');t.className='toast';t.textContent=msg;
    document.body.appendChild(t);setTimeout(()=>t.remove(),1600);
  }
  function copyText(txt,msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(()=>toast(msg),()=>fallbackCopy(txt,msg));
    } else fallbackCopy(txt,msg);
  }
  function fallbackCopy(txt,msg){
    const ta=document.createElement('textarea');ta.value=txt;
    document.body.appendChild(ta);ta.select();try{document.execCommand('copy');toast(msg);}catch(e){toast('Copy failed');}
    ta.remove();
  }

  el('go').addEventListener('click',runSearch);
  el('q').addEventListener('keydown',e=>{if(e.key==='Enter')runSearch();});
  document.querySelectorAll('.ex').forEach(b=>b.addEventListener('click',()=>{
    el('q').value=b.dataset.q; runSearch(); el('q').focus();
  }));

  resultsEl.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    if(b.dataset.copy) copyText(b.dataset.copy,'Citation copied');
    if(b.dataset.add){
      const r=records.find(x=>x.id===b.dataset.add);
      if(r && !draft.has(r.id)){ draft.set(r.id,r); renderDraft(); toast('Added to draft'); }
    }
  });

  function draftText(){
    return Array.from(draft.values()).map(r=>
      citation(r) + '\n\n' + r.text + '\n\n---\n\n'
    ).join('');
  }
  function renderDraft(){
    el('draft').hidden = draft.size===0;
    el('draftList').innerHTML = Array.from(draft.values()).map(r=>
      '<article class="result">' +
      '<div class="rhead"><span class="committee">'+esc(r.committee||'')+'</span>' +
      '<a href="'+esc(r.doc_url||'#')+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>' +
      '<span class="mono">para. '+r.paragraph+'</span>' +
      '<span class="rtitle">'+esc(r.short_title||r.title||'')+'</span></div>' +
      '<p class="rtext">'+esc(r.text)+'</p>' +
      '<div class="racts"><button data-copy="'+esc(citation(r))+'">COPY CITATION</button>' +
      '<button data-remove="'+r.id+'">REMOVE</button></div></article>'
    ).join('');
  }
  el('draftList').addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    if(b.dataset.copy) copyText(b.dataset.copy,'Citation copied');
    if(b.dataset.remove){ draft.delete(b.dataset.remove); renderDraft(); }
  });
  el('copyAll').addEventListener('click',()=>copyText(draftText(),'Draft copied'));
  el('download').addEventListener('click',()=>{
    const blob=new Blob([draftText()],{type:'text/plain'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);
    a.download='verbatim-draft.txt';a.click();URL.revokeObjectURL(a.href);
  });
  el('clearDraft').addEventListener('click',()=>{draft.clear();renderDraft();});

  el('howComputed').textContent =
    'Every one of the ' + records.length + ' paragraphs in the file is searched directly in your browser. ' +
    'Words match case-insensitively after apostrophe shapes are unified; a word also matches its longer forms (child finds children). ' +
    'Quoted phrases must appear as a contiguous string. Results keep the file\'s order and show the text exactly as stored.';

  el('searched').textContent = records.length + ' paragraphs searched';
})();
</script>
</body>
</html>
```