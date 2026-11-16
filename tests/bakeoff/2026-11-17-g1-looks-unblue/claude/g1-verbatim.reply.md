I built a one-screen verbatim finder: type words or put a phrase in quotation marks, and every matching General Comment paragraph appears word for word with its symbol, paragraph number and a "Copy citation" button. Paragraphs you add go to a draft list at the bottom, which you can copy or download.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: General Comments</title>
<style>
  :root{
    --ink:#1a2a3a; --panel:#eef4f8; --blue:#009edb; --blue-hover:#33b3e3;
    --rule:#c5d5e0; --muted:#3d5266; --bg:#ffffff;
  }
  *{box-sizing:border-box}
  [hidden]{display:none!important}
  html{background:var(--bg)}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  .wrap{max-width:920px;margin:0 auto;padding:24px 20px 64px}
  .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
  header{border-bottom:3px solid var(--blue);padding-bottom:14px;margin-bottom:20px}
  header .mono{color:var(--muted)}
  h1{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    font-size:30px;line-height:1.2;margin:6px 0 6px;font-weight:700}
  header p{margin:0;color:var(--muted)}
  :focus-visible{outline:3px solid var(--ink);outline-offset:2px}
  .panel{background:var(--panel);padding:18px 20px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
  .searchrow{display:flex;gap:10px;flex-wrap:wrap}
  .searchrow input{flex:1 1 320px;min-width:0;font:inherit;font-size:18px;padding:12px 14px;
    border:2px solid var(--ink);background:#fff;color:var(--ink);border-radius:2px}
  button,.btn{font:inherit;font-weight:600;cursor:pointer;border-radius:2px}
  .primary{background:var(--blue);color:var(--ink);border:2px solid var(--blue);padding:10px 18px}
  .primary:hover{background:var(--blue-hover);border-color:var(--blue-hover)}
  .ghost{background:#fff;color:var(--ink);border:2px solid var(--ink);padding:8px 14px}
  .ghost:hover{background:var(--panel)}
  .examples{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:12px}
  .examples .mono{color:var(--muted);margin-right:4px}
  .example{background:#fff;color:var(--ink);border:2px solid var(--blue);padding:6px 12px;font-weight:600}
  .example:hover{background:var(--blue-hover)}
  .hint{margin:12px 0 0;color:var(--muted);font-size:14px}
  .hint code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;background:#fff;padding:0 4px}
  .stat{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin:24px 0 4px}
  .stat .big{font-size:52px;line-height:1;font-weight:700}
  .stat .what{font-size:18px}
  .searched{color:var(--muted);margin:0}
  .how{margin:6px 0 18px;color:var(--muted);font-size:14px;border-bottom:1px solid var(--rule);padding-bottom:14px}
  .how .mono{color:var(--ink)}
  .empty{padding:18px 0;font-size:18px}
  article.hit{border-top:1px solid var(--rule);padding:16px 0}
  article.hit:last-child{border-bottom:1px solid var(--rule)}
  .meta{color:var(--muted)}
  .cite{font-size:18px;font-weight:700;margin:2px 0 8px}
  .cite a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--blue);text-decoration-thickness:3px;text-underline-offset:3px}
  .cite a:hover{background:var(--panel)}
  .text{margin:0 0 12px;white-space:pre-wrap;overflow-wrap:anywhere;max-width:72ch}
  mark{background:var(--blue);color:var(--ink);padding:0 1px;border-radius:2px}
  .acts{display:flex;gap:8px;flex-wrap:wrap}
  .more{margin:18px 0;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
  section.draft{margin-top:40px}
  h2{font-size:22px;margin:0 0 4px}
  .draftitem{border-top:1px solid var(--rule);padding:12px 0;display:flex;gap:12px;align-items:flex-start;justify-content:space-between}
  .draftitem .dtext{max-width:72ch;white-space:pre-wrap;overflow-wrap:anywhere}
  .draftitem .dcite{font-weight:700;display:block;margin-top:2px}
  .cannot{margin-top:40px;background:var(--panel);padding:16px 20px;border-top:1px solid var(--rule)}
  .cannot ul{margin:8px 0 0;padding-left:20px}
  .cannot li{margin:4px 0}
  .status{min-height:22px;color:var(--muted);font-size:14px;margin:6px 0}
  @media (max-width:560px){.stat .big{font-size:42px} h1{font-size:25px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="mono">WORKSHOP_DATA.gc &middot; General Comments, paragraph by paragraph</div>
    <h1>Verbatim finder: the right to water and sanitation</h1>
    <p id="source-line">Loading the file&hellip;</p>
  </header>

  <main>
    <form class="panel" id="search-form" role="search" autocomplete="off">
      <label class="mono" for="q">01 &middot; Your words or phrase</label>
      <div class="searchrow" style="margin-top:8px">
        <input id="q" type="search" placeholder='e.g. water sanitation   or   "right to water"' aria-describedby="hint">
        <button class="primary" type="submit">Search</button>
      </div>
      <div class="examples" id="examples">
        <span class="mono">Try</span>
      </div>
      <p class="hint" id="hint">
        <span class="mono">all words, any order</span> &nbsp;
        <span class="mono">&ldquo;quotes&rdquo; = words together</span> &nbsp;
        <span class="mono">ignores case and &rsquo; vs '</span> &nbsp;
        <span class="mono">child finds children</span>
      </p>
    </form>

    <div class="stat" aria-live="polite">
      <span class="big" id="hits-n">0</span>
      <span class="what" id="hits-what">matching paragraphs</span>
    </div>
    <p class="searched" id="searched"><strong id="searched-n">0</strong> paragraphs searched</p>
    <p class="how" id="how"><span class="mono">How this is computed</span> &nbsp;Nothing searched yet. Every paragraph in the file is checked by your browser; no word list, no synonyms.</p>

    <div id="results"></div>
    <div class="more" id="more" hidden>
      <button class="ghost" id="more-btn" type="button">Show more</button>
      <span class="meta" id="more-info"></span>
    </div>

    <section class="draft" aria-labelledby="draft-h">
      <div class="mono" style="color:var(--muted)">02 &middot; Your draft</div>
      <h2 id="draft-h">Draft list: <span id="draft-n">0</span> paragraphs</h2>
      <p class="hint" style="margin-top:2px">Each entry is the paragraph exactly as stored, in quotation marks, followed by its citation. Footnote marks such as [[fn:12]] stay in the stored text.</p>
      <div class="acts" style="margin:12px 0">
        <button class="ghost" id="copy-all" type="button">Copy all</button>
        <button class="ghost" id="download" type="button">Download</button>
      </div>
      <div class="status" id="status" role="status" aria-live="polite"></div>
      <div id="draft-list"></div>
    </section>

    <section class="cannot" aria-labelledby="cannot-h">
      <div class="mono" style="color:var(--muted)">03 &middot; What this tool cannot do</div>
      <h2 id="cannot-h" style="font-size:18px">Limits, so you do not over-trust it</h2>
      <ul>
        <li>It does not summarise, paraphrase or find synonyms: only the words you type. &ldquo;Drinking water&rdquo; will not find &ldquo;potable&rdquo;.</li>
        <li>It searches only the attached General Comments file: no concluding observations, no case law, no other sources. English only.</li>
        <li>A symbol is not always one document: one symbol can hold several General Recommendations, and a joint General Comment carries two symbols in one field. The citation then adds the short title; check the document at the link.</li>
        <li>A word also matches longer words that start with it (water finds watercourse). A quoted phrase must match whole words, in order.</li>
        <li>It does not check that the file is complete or that the text matches the original: click the symbol and compare. Footnote marks are ignored when searching but kept in the text shown.</li>
        <li>Nothing leaves your browser: no network, no AI model.</li>
      </ul>
    </section>
  </main>
</div>

<script>
(function(){
  var APOS = "’‘ʼ'`";
  var PAGE = 40;
  var gcData = (window.WORKSHOP_DATA || {}).gc;
  var recs = (gcData && Array.isArray(gcData.records)) ? gcData.records : [];

  var $ = function(id){ return document.getElementById(id); };
  var qEl = $('q'), resultsEl = $('results'), moreEl = $('more');
  var state = { hits: [], shown: 0, terms: [], query: '' };
  var draft = [];

  /* ---------- prepare ---------- */
  var FN = /\[\[fn:[^\]]*\]\]/g;
  var hay = recs.map(function(r){
    return String(r.text == null ? '' : r.text).replace(FN, function(m){ return new Array(m.length + 1).join(' '); });
  });
  var titlesBySymbol = {};
  recs.forEach(function(r){
    var s = String(r.symbol || '');
    (titlesBySymbol[s] = titlesBySymbol[s] || {})[r.short_title || r.title || ''] = 1;
  });
  function isMulti(r){
    var s = String(r.symbol || '');
    return Object.keys(titlesBySymbol[s] || {}).length > 1 || /[–—]/.test(s);
  }
  function citation(r){
    var c = r.symbol + ', para. ' + r.paragraph;
    if (isMulti(r) && (r.short_title || r.title)) c += ' (' + (r.short_title || r.title) + ')';
    return c;
  }

  /* header line */
  (function(){
    var years = recs.map(function(r){ return r.year; }).filter(function(y){ return typeof y === 'number'; });
    var cms = {}; recs.forEach(function(r){ if (r.committee) cms[r.committee] = 1; });
    var src = (gcData && gcData.source) ? gcData.source : 'attached file';
    var line = 'Source: ' + src + ' · n = ' + recs.length.toLocaleString('en') + ' paragraphs';
    if (years.length) line += ' · ' + Math.min.apply(null, years) + '–' + Math.max.apply(null, years);
    if (Object.keys(cms).length) line += ' · ' + Object.keys(cms).length + ' committees';
    $('source-line').textContent = recs.length ? line : 'No General Comments file is attached: drag it from "Your files" into the chat.';
    $('searched-n').textContent = recs.length.toLocaleString('en');
  })();

  /* ---------- query parsing ---------- */
  function escChar(ch){
    if (APOS.indexOf(ch) >= 0) return '[’‘ʼ\'`]';
    return ch.replace(/[.*+?^${}()|[\]\\\/-]/g, '\\$&');
  }
  function toPattern(words, isPhrase){
    var parts = words.map(function(w){ return Array.from(w).map(escChar).join(''); });
    var src = '(?<![\\p{L}\\p{N}])' + parts.join('\\s+');
    if (isPhrase) src += '(?![\\p{L}\\p{N}])';
    return src;
  }
  function parse(q){
    var terms = [], re = /["“”]([^"“”]*)["“”]|(\S+)/g, m;
    while ((m = re.exec(q))){
      if (m[1] !== undefined){
        var ws = m[1].trim().split(/\s+/).filter(Boolean);
        if (ws.length) terms.push({ src: toPattern(ws, true), label: ws.join(' ') });
      } else {
        var w = m[2].replace(/^["“”]+|["“”]+$/g, '');
        if (w) terms.push({ src: toPattern([w], false), label: w });
      }
    }
    return terms.map(function(t){
      return { label: t.label, test: new RegExp(t.src, 'iu'), find: new RegExp(t.src, 'giu') };
    });
  }

  /* ---------- search ---------- */
  function run(q){
    q = q.trim();
    state.query = q;
    state.terms = q ? parse(q) : [];
    state.hits = [];
    if (state.terms.length){
      for (var i = 0; i < recs.length; i++){
        var ok = true;
        for (var t = 0; t < state.terms.length; t++){
          if (!state.terms[t].test.test(hay[i])){ ok = false; break; }
        }
        if (ok) state.hits.push(i);
      }
    }
    state.shown = 0;
    resultsEl.textContent = '';
    renderMore();
    summary();
  }
  function summary(){
    var n = state.hits.length;
    $('hits-n').textContent = n.toLocaleString('en');
    $('hits-what').textContent = n === 1 ? 'matching paragraph' : 'matching paragraphs';
    var how = $('how');
    how.textContent = '';
    var lab = document.createElement('span'); lab.className = 'mono'; lab.textContent = 'How this is computed';
    how.appendChild(lab);
    var msg;
    if (!state.terms.length){
      msg = ' Nothing searched yet. Every paragraph in the file is checked by your browser; no word list, no synonyms.';
    } else {
      var parts = state.terms.map(function(t){ return '“' + t.label + '”'; }).join(' and ');
      msg = ' A paragraph counts only if it contains ' + parts + ' (case and apostrophe shape ignored; footnote marks ignored), checked in all ' + recs.length.toLocaleString('en') + ' paragraphs. Results keep the file’s order.';
    }
    how.appendChild(document.createTextNode(msg));
    if (state.terms.length && !n){
      resultsEl.textContent = '';
      var e = document.createElement('div'); e.className = 'empty';
      e.textContent = 'No paragraph in this file contains ' + state.terms.map(function(t){ return '“' + t.label + '”'; }).join(' and ') + '. Matches: 0 of ' + recs.length.toLocaleString('en') + '. Try fewer words, or drop the quotation marks.';
      resultsEl.appendChild(e);
    }
  }

  /* ---------- results ---------- */
  function ranges(i){
    var rs = [];
    state.terms.forEach(function(t){
      t.find.lastIndex = 0;
      var m;
      while ((m = t.find.exec(hay[i])) && m[0].length){ rs.push([m.index, m.index + m[0].length]); }
    });
    rs.sort(function(a, b){ return a[0] - b[0]; });
    var out = [];
    rs.forEach(function(r){
      var last = out[out.length - 1];
      if (last && r[0] <= last[1]) last[1] = Math.max(last[1], r[1]); else out.push([r[0], r[1]]);
    });
    return out;
  }
  function highlighted(text, rs){
    var frag = document.createDocumentFragment(), pos = 0;
    rs.forEach(function(r){
      if (r[0] > pos) frag.appendChild(document.createTextNode(text.slice(pos, r[0])));
      var mk = document.createElement('mark'); mk.textContent = text.slice(r[0], r[1]); frag.appendChild(mk);
      pos = r[1];
    });
    if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
    return frag;
  }
  function mkBtn(label, cls, fn){
    var b = document.createElement('button'); b.type = 'button'; b.className = cls; b.textContent = label;
    b.addEventListener('click', function(){ fn(b); }); return b;
  }
  function flash(btn, msg){
    var old = btn.dataset.label || btn.textContent; btn.dataset.label = old;
    btn.textContent = msg; clearTimeout(btn._t);
    btn._t = setTimeout(function(){ btn.textContent = old; }, 1600);
  }
  function card(i){
    var r = recs[i];
    var art = document.createElement('article'); art.className = 'hit';
    var meta = document.createElement('div'); meta.className = 'mono meta';
    meta.textContent = [r.committee, r.short_title || r.title].filter(Boolean).join(' · ');
    art.appendChild(meta);
    var cite = document.createElement('div'); cite.className = 'cite';
    if (r.doc_url){
      var a = document.createElement('a'); a.href = r.doc_url; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = r.symbol; a.title = 'Open the original document in a new tab'; cite.appendChild(a);
    } else { cite.appendChild(document.createTextNode(r.symbol)); }
    cite.appendChild(document.createTextNode(', para. ' + r.paragraph));
    art.appendChild(cite);
    var p = document.createElement('p'); p.className = 'text';
    var text = String(r.text == null ? '' : r.text);
    p.appendChild(highlighted(text, ranges(i)));
    art.appendChild(p);
    var acts = document.createElement('div'); acts.className = 'acts';
    acts.appendChild(mkBtn('Copy citation', 'primary', function(b){
      copy(citation(r), function(ok){ flash(b, ok ? 'Copied' : 'Copy failed'); });
    }));
    var inDraft = draft.indexOf(i) >= 0;
    acts.appendChild(mkBtn(inDraft ? 'In draft' : 'Add to draft', 'ghost', function(b){
      if (draft.indexOf(i) < 0){ draft.push(i); renderDraft(); }
      b.textContent = 'In draft';
    }));
    art.appendChild(acts);
    return art;
  }
  function renderMore(){
    var end = Math.min(state.shown + PAGE, state.hits.length);
    for (var k = state.shown; k < end; k++) resultsEl.appendChild(card(state.hits[k]));
    state.shown = end;
    var left = state.hits.length - state.shown;
    moreEl.hidden = left <= 0;
    $('more-btn').textContent = 'Show ' + Math.min(PAGE, left) + ' more';
    $('more-info').textContent = 'Showing ' + state.shown.toLocaleString('en') + ' of ' + state.hits.length.toLocaleString('en') + ' matching paragraphs';
  }
  $('more-btn').addEventListener('click', renderMore);

  /* ---------- clipboard, draft ---------- */
  function copy(text, done){
    function fallback(){
      var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta); done(ok);
    }
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){ done(true); }, fallback);
    } else fallback();
  }
  function draftText(){
    return draft.map(function(i){
      var r = recs[i];
      return '“' + String(r.text == null ? '' : r.text) + '” (' + citation(r) + ')';
    }).join('\n\n');
  }
  function renderDraft(){
    $('draft-n').textContent = draft.length;
    var box = $('draft-list'); box.textContent = '';
    if (!draft.length){
      var e = document.createElement('div'); e.className = 'meta'; e.textContent = 'Empty. Use “Add to draft” on a result.';
      box.appendChild(e);
    }
    draft.forEach(function(i, pos){
      var r = recs[i];
      var row = document.createElement('div'); row.className = 'draftitem';
      var d = document.createElement('div'); d.className = 'dtext';
      d.appendChild(document.createTextNode('“' + String(r.text == null ? '' : r.text) + '”'));
      var c = document.createElement('span'); c.className = 'dcite'; c.textContent = citation(r);
      d.appendChild(c);
      row.appendChild(d);
      row.appendChild(mkBtn('Remove', 'ghost', function(){
        draft.splice(pos, 1); renderDraft();
        Array.prototype.forEach.call(resultsEl.querySelectorAll('article.hit'), function(){});
      }));
      box.appendChild(row);
    });
  }
  function status(msg){ $('status').textContent = msg; clearTimeout(status._t); status._t = setTimeout(function(){ $('status').textContent = ''; }, 3000); }
  $('copy-all').addEventListener('click', function(){
    if (!draft.length){ status('The draft list is empty.'); return; }
    copy(draftText(), function(ok){ status(ok ? 'Copied ' + draft.length + ' paragraphs with citations.' : 'Copy failed: use Download instead.'); });
  });
  $('download').addEventListener('click', function(){
    if (!draft.length){ status('The draft list is empty.'); return; }
    try {
      var blob = new Blob([draftText() + '\n'], { type: 'text/plain;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a'); a.href = url; a.download = 'draft-quotations.txt';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
      status('Downloaded draft-quotations.txt');
    } catch (e) { status('Download is blocked here: use Copy all.'); }
  });

  /* ---------- wiring ---------- */
  var examples = ['"right to water"', 'water sanitation', '"safe drinking water"'];
  examples.forEach(function(ex){
    var b = document.createElement('button'); b.type = 'button'; b.className = 'example'; b.textContent = ex;
    b.addEventListener('click', function(){ qEl.value = ex; run(ex); });
    $('examples').appendChild(b);
  });
  $('search-form').addEventListener('submit', function(ev){ ev.preventDefault(); run(qEl.value); });
  var timer;
  qEl.addEventListener('input', function(){ clearTimeout(timer); timer = setTimeout(function(){ run(qEl.value); }, 250); });

  renderDraft();
  summary();
})();
</script>
</body>
</html>
```
