I built the verbatim finder on the General Comments file: one screen, a search box, three example searches, and the count of paragraphs searched always in view. Each result shows the paragraph word for word, its symbol linked to the original, and buttons to copy a citation or add it to a draft list.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder for General Comments</title>
<style>
:root{--paper:#f4f0e8;--ink:#1d1b18;--rule:#d9d2c3;--red:#9b2335;--muted:#5c574e;--field:#fbf9f4}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:24px 20px 64px}
.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.muted{color:var(--muted)}
header{border-bottom:1px solid var(--rule);padding-bottom:16px}
h1{font:400 38px/1.15 Georgia,"Times New Roman",serif;margin:6px 0 8px}
header p{margin:0;color:var(--muted)}
a{color:var(--red)}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
button{font:inherit;cursor:pointer}
.btn{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase;background:transparent;color:var(--ink);border:1px solid var(--ink);padding:7px 11px;border-radius:0}
.btn:hover{background:var(--ink);color:var(--paper)}
.btn[disabled]{border-color:var(--rule);color:var(--muted);cursor:default;background:transparent}
.btn.red{border-color:var(--red);color:var(--red)}
.btn.red:hover{background:var(--red);color:var(--paper)}
.search{margin-top:22px}
.search label{display:block;margin-bottom:6px}
.search input{width:100%;font:20px/1.3 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--field);border:1px solid var(--ink);border-radius:0;padding:12px 14px}
.examples{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
.hint{margin:8px 0 0;color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:12px 48px;margin-top:26px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:14px 0}
.stat .num{font:400 48px/1.05 Georgia,"Times New Roman",serif;display:block}
.stat.match .num{color:var(--red)}
.how{margin:10px 0 0;color:var(--muted);font-size:14px}
#status{margin:18px 0 0;font-family:Georgia,"Times New Roman",serif;font-size:20px}
ol.results,ol.draft{list-style:none;margin:0;padding:0}
.res{border-top:1px solid var(--rule);padding:18px 0}
.res .meta{display:block;margin-bottom:4px;color:var(--muted)}
.res .cite{font-family:Georgia,"Times New Roman",serif;font-size:18px;margin:0 0 8px}
.res .cite a{font-weight:700}
.res .text{margin:0 0 12px;max-width:72ch;white-space:pre-wrap}
.res .actions{display:flex;flex-wrap:wrap;gap:8px}
mark{background:#ecd5cb;color:var(--ink);box-shadow:inset 0 -2px var(--red);padding:0 1px}
.fn{color:var(--muted);font-size:.85em}
.more{margin:18px 0 0}
section.draftbox{margin-top:40px;border-top:2px solid var(--ink);padding-top:14px}
section.draftbox h2{font:400 26px/1.2 Georgia,"Times New Roman",serif;margin:4px 0 10px}
.draft li{border-top:1px solid var(--rule);padding:12px 0}
.draft .cite{font-family:Georgia,"Times New Roman",serif;font-size:17px;font-weight:700;margin:0 0 4px}
.draft .text{margin:0 0 8px;max-width:72ch;white-space:pre-wrap}
.draftbar{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 6px}
footer{margin-top:44px;border-top:1px solid var(--rule);padding-top:14px}
footer ul{margin:8px 0 0;padding-left:20px;max-width:72ch}
footer li{margin:4px 0}
.draftlink{margin-left:auto;color:var(--red);text-decoration:underline}
@media (max-width:560px){h1{font-size:30px}.stat .num{font-size:40px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <span class="mono muted">WORKSHOP_DATA.gc · General Comments, paragraph by paragraph</span>
  <h1>Verbatim finder for General Comments</h1>
  <p id="source">Loading the file…</p>
</header>

<main>
  <div class="search">
    <label class="mono" for="q">01 · Type a phrase</label>
    <input id="q" type="search" autocomplete="off" spellcheck="false" placeholder="best interests, or &quot;right to be heard&quot;">
    <div class="examples">
      <span class="mono muted">Try</span>
      <button class="btn" type="button" data-q="&quot;best interests&quot;">"best interests"</button>
      <button class="btn" type="button" data-q="&quot;right to be heard&quot;">"right to be heard"</button>
      <button class="btn" type="button" data-q="child protection">child protection</button>
      <a class="mono draftlink" href="#draft" id="draftlink">Draft: 0 ↓</a>
    </div>
    <p class="hint mono">words: any order, word starts (child finds children) · "quotes": exact words together</p>
  </div>

  <div class="stats" role="group" aria-label="Counts">
    <div class="stat match"><span class="mono muted">Paragraphs that match</span><span class="num" id="nmatch">–</span></div>
    <div class="stat"><span class="mono muted">Paragraphs searched</span><span class="num" id="nsearched">0</span></div>
  </div>
  <p class="how" id="how">How this is computed: this page tests every paragraph for every word you type and every quoted phrase, ignoring capitals and apostrophe shape. It counts in your browser; nothing is sent anywhere.</p>

  <p id="status" aria-live="polite"></p>
  <ol class="results" id="results"></ol>
  <p class="more" id="more" hidden><button class="btn" type="button" id="moreBtn">Show more</button></p>

  <section class="draftbox" id="draft" aria-labelledby="drafth">
    <span class="mono muted">02 · Your draft list</span>
    <h2 id="drafth">Draft: <span id="ndraft">0</span> paragraphs</h2>
    <p class="hint" id="draftempty">Nothing yet. Use "Add to draft" on a result to collect paragraphs here.</p>
    <div class="draftbar" id="draftbar" hidden>
      <button class="btn red" type="button" id="copyAll">Copy all</button>
      <button class="btn" type="button" id="download">Download</button>
    </div>
    <ol class="draft" id="draftlist"></ol>
  </section>
</main>

<footer>
  <span class="mono muted">What this tool cannot do</span>
  <ul id="limits"></ul>
</footer>
</div>

<script>
(function(){
  var DATA = (window.WORKSHOP_DATA || {}).gc || {};
  var recs = Array.isArray(DATA.records) ? DATA.records : [];
  var CHUNK = 50;
  var byId = new Map();
  var titlesBySymbol = new Map();
  var years = [], committees = new Set();

  recs.forEach(function(r){
    byId.set(r.id, r);
    var t = r.short_title || r.title || '';
    if(!titlesBySymbol.has(r.symbol)) titlesBySymbol.set(r.symbol, new Set());
    titlesBySymbol.get(r.symbol).add(t);
    if(typeof r.year === 'number') years.push(r.year);
    if(r.committee) committees.add(r.committee);
  });

  function multi(r){
    var s = String(r.symbol || '');
    var set = titlesBySymbol.get(r.symbol);
    return /[–—]/.test(s) || (set && set.size > 1);
  }
  var nMulti = 0;
  titlesBySymbol.forEach(function(set, sym){ if(set.size > 1 || /[–—]/.test(String(sym))) nMulti++; });

  function cite(r){
    var c = r.symbol + ', para. ' + r.paragraph;
    if(multi(r) && r.short_title) c += ' (' + r.short_title + ')';
    return c;
  }

  var $ = function(id){ return document.getElementById(id); };
  var q = $('q'), results = $('results'), status = $('status');
  var nmatch = $('nmatch'), moreP = $('more'), moreBtn = $('moreBtn');

  function el(tag, cls, text){
    var e = document.createElement(tag);
    if(cls) e.className = cls;
    if(text != null) e.textContent = text;
    return e;
  }
  function fmt(n){ return Number(n).toLocaleString('en-GB'); }

  /* header and fixed facts */
  var yr = years.length ? Math.min.apply(null, years) + '–' + Math.max.apply(null, years) : 'years not given';
  $('source').textContent = (DATA.source ? DATA.source + ' · ' : '') + 'n = ' + fmt(recs.length) + ' paragraphs · ' + committees.size + ' committees · ' + yr;
  $('nsearched').textContent = fmt(recs.length);

  var limits = [
    'It does not summarise, paraphrase or find synonyms: only the words you typed (child finds children, not minors).',
    'It searches only General Comments in the attached file: no concluding observations, no case law.',
    'It is English only: no translation.',
    'Footnote marks such as [[fn:12]] stay in the text exactly as stored; this page does not show the footnotes themselves.',
    'It cannot confirm a citation against the original: click the symbol and compare the paragraph yourself.'
  ];
  if(nMulti) limits.push(fmt(nMulti) + ' symbols in the file hold more than one document or carry two symbols; their copied citation adds the short title.');
  if(!recs.length) limits.unshift('The file WORKSHOP_DATA.gc is empty or missing, so nothing can be searched.');
  limits.forEach(function(t){ $('limits').appendChild(el('li', null, t)); });

  /* query parsing */
  var APOS = "['’‘ʼ]";
  var SEP = '(?:\\s|\\[\\[fn:\\d+\\]\\])+';
  var START = '(?<![\\p{L}\\p{N}])';
  var END = '(?![\\p{L}\\p{N}])';

  function wordPattern(w){
    var out = '';
    for(var i = 0; i < w.length; i++){
      var ch = w[i];
      if(/['’‘ʼ]/.test(ch)) out += APOS;
      else out += ch.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&');
    }
    return out;
  }
  function hasContent(s){ return /[\p{L}\p{N}]/u.test(s); }

  function parse(str){
    var terms = [];
    var re = /["“”]([^"“”]*)["“”]?|[^\s"“”]+/g, m;
    while((m = re.exec(str))){
      if(m[1] !== undefined){
        var words = m[1].split(/\s+/).filter(hasContent);
        if(words.length) terms.push({src: START + words.map(wordPattern).join(SEP) + END, phrase: true});
      } else if(hasContent(m[0])){
        terms.push({src: START + wordPattern(m[0]), phrase: false});
      }
    }
    return terms;
  }

  /* rendering text with highlights */
  var FN = /(\[\[fn:\d+\]\])/;
  function plain(parent, s){
    s.split(FN).forEach(function(p){
      if(!p) return;
      if(FN.test(p)) parent.appendChild(el('span', 'fn', p));
      else parent.appendChild(document.createTextNode(p));
    });
  }
  function highlight(parent, text, re){
    if(!re){ plain(parent, text); return; }
    var last = 0, m;
    re.lastIndex = 0;
    while((m = re.exec(text))){
      if(m[0] === '') { re.lastIndex++; continue; }
      if(m.index > last) plain(parent, text.slice(last, m.index));
      parent.appendChild(el('mark', null, m[0]));
      last = m.index + m[0].length;
    }
    if(last < text.length) plain(parent, text.slice(last));
  }

  /* clipboard */
  function flash(btn, msg){
    var old = btn.dataset.label || btn.textContent;
    btn.dataset.label = old;
    btn.textContent = msg;
    clearTimeout(btn._t);
    btn._t = setTimeout(function(){ btn.textContent = old; }, 1400);
  }
  function copy(text, btn){
    function fallback(){
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch(e){}
      document.body.removeChild(ta);
      flash(btn, ok ? 'Copied' : 'Copy failed');
    }
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){ flash(btn, 'Copied'); }, fallback);
    } else fallback();
  }

  /* draft list */
  var draft = [];
  function draftText(){
    return draft.map(function(id){
      var r = byId.get(id);
      return r.text + '\n' + cite(r);
    }).join('\n\n');
  }
  function setAddBtn(btn, inDraft){
    btn.textContent = inDraft ? 'In draft ✓' : 'Add to draft';
    btn.disabled = inDraft;
  }
  function syncAddButtons(id){
    var list = results.querySelectorAll('[data-add="' + id + '"]');
    for(var i = 0; i < list.length; i++) setAddBtn(list[i], draft.indexOf(id) >= 0);
  }
  function renderDraft(){
    var list = $('draftlist');
    list.textContent = '';
    draft.forEach(function(id){
      var r = byId.get(id);
      var li = el('li');
      li.appendChild(el('p', 'cite', cite(r)));
      li.appendChild(el('p', 'text', r.text));
      var rm = el('button', 'btn', 'Remove');
      rm.type = 'button';
      rm.addEventListener('click', function(){
        draft = draft.filter(function(x){ return x !== id; });
        renderDraft();
        syncAddButtons(id);
      });
      li.appendChild(rm);
      list.appendChild(li);
    });
    $('ndraft').textContent = draft.length;
    $('draftlink').textContent = 'Draft: ' + draft.length + ' ↓';
    $('draftbar').hidden = !draft.length;
    $('draftempty').hidden = draft.length > 0;
  }
  $('copyAll').addEventListener('click', function(){ copy(draftText(), this); });
  $('download').addEventListener('click', function(){
    var blob = new Blob([draftText() + '\n'], {type: 'text/plain;charset=utf-8'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'draft-quotes.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
  });

  /* results */
  var matches = [], shown = 0, hlRe = null;

  function resultEl(r){
    var li = el('li', 'res');
    li.appendChild(el('span', 'mono meta', (r.committee || '') + (r.year ? ' · ' + r.year : '') + ' · ' + (r.short_title || r.title || '')));
    var c = el('p', 'cite');
    if(r.doc_url){
      var a = el('a', null, r.symbol);
      a.href = r.doc_url; a.target = '_blank'; a.rel = 'noopener';
      c.appendChild(a);
    } else c.appendChild(el('strong', null, r.symbol));
    c.appendChild(document.createTextNode(', para. ' + r.paragraph));
    li.appendChild(c);
    var t = el('p', 'text');
    highlight(t, String(r.text || ''), hlRe);
    li.appendChild(t);
    var act = el('div', 'actions');
    var cb = el('button', 'btn red', 'Copy citation');
    cb.type = 'button';
    cb.addEventListener('click', function(){ copy(cite(r), cb); });
    var ab = el('button', 'btn');
    ab.type = 'button';
    ab.dataset.add = r.id;
    setAddBtn(ab, draft.indexOf(r.id) >= 0);
    ab.addEventListener('click', function(){
      if(draft.indexOf(r.id) < 0){ draft.push(r.id); renderDraft(); syncAddButtons(r.id); }
    });
    act.appendChild(cb); act.appendChild(ab);
    li.appendChild(act);
    return li;
  }

  function showMore(){
    var end = Math.min(shown + CHUNK, matches.length);
    var frag = document.createDocumentFragment();
    for(var i = shown; i < end; i++) frag.appendChild(resultEl(matches[i]));
    results.appendChild(frag);
    shown = end;
    moreP.hidden = shown >= matches.length;
    if(!moreP.hidden) moreBtn.textContent = 'Show ' + Math.min(CHUNK, matches.length - shown) + ' more (' + fmt(matches.length - shown) + ' not yet shown)';
  }
  moreBtn.addEventListener('click', showMore);

  function run(){
    var raw = q.value.trim();
    results.textContent = '';
    moreP.hidden = true;
    matches = []; shown = 0; hlRe = null;
    var terms = parse(raw);
    if(!terms.length){
      nmatch.textContent = '–';
      status.textContent = raw ? 'Type at least one word or letter.' : 'Type a phrase, or pick one of the examples.';
      return;
    }
    var tests = terms.map(function(t){ return new RegExp(t.src, 'iu'); });
    var ordered = terms.slice().sort(function(a, b){ return (b.phrase - a.phrase) || (b.src.length - a.src.length); });
    hlRe = new RegExp(ordered.map(function(t){ return t.src; }).join('|'), 'giu');
    for(var i = 0; i < recs.length; i++){
      var tx = String(recs[i].text || ''), ok = true;
      for(var j = 0; j < tests.length; j++){ if(!tests[j].test(tx)){ ok = false; break; } }
      if(ok) matches.push(recs[i]);
    }
    nmatch.textContent = fmt(matches.length);
    if(!matches.length){
      status.textContent = '0 paragraphs of ' + fmt(recs.length) + ' contain this. Nothing is shown; try fewer words or remove the quotation marks.';
      return;
    }
    status.textContent = fmt(matches.length) + (matches.length === 1 ? ' paragraph contains' : ' paragraphs contain') + ' ' + raw + ', in the order of the file.';
    showMore();
  }

  var timer;
  q.addEventListener('input', function(){ clearTimeout(timer); timer = setTimeout(run, 150); });
  q.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ clearTimeout(timer); run(); } });
  Array.prototype.forEach.call(document.querySelectorAll('[data-q]'), function(b){
    b.addEventListener('click', function(){ q.value = b.getAttribute('data-q'); run(); q.focus(); });
  });

  renderDraft();
  run();
})();
</script>
</body>
</html>
```
