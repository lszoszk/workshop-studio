```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder: the rights of the child</title>
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#eef0f2;color:#1d2227;font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:20px 18px 48px}
.label{font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:#4a5560}
h1{font-size:30px;line-height:1.2;margin:6px 0 4px;font-weight:700}
.source{margin:0 0 16px;color:#3d4650}
.intro{margin:0 0 16px;max-width:70ch}
.intro p{margin:0 0 6px}
.intro ol{margin:0;padding-left:22px}
.search{background:#fff;border-radius:10px;padding:14px 16px;border:1px solid #d3d8dd}
.search label{display:block;margin-bottom:6px}
.search input{width:100%;font:inherit;font-size:18px;padding:10px 12px;border:1px solid #9aa4ad;border-radius:8px;background:#fff;color:#1d2227}
.hint{margin:6px 0 0}
.examples{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
button,a.sym{font:inherit}
.ex,.btn{font-size:15px;border:1px solid #8e99a3;background:#fff;color:#1d2227;border-radius:8px;padding:6px 12px;cursor:pointer}
.ex:hover,.btn:hover{background:#e6eaee}
.btn.primary{background:#2f4f6b;color:#fff;border-color:#2f4f6b}
.btn.primary:hover{background:#264059}
:focus-visible{outline:3px solid #1f5fae;outline-offset:2px}
.status{display:flex;flex-wrap:wrap;gap:6px 24px;align-items:baseline;margin:16px 0 8px}
.big{font-size:44px;line-height:1;font-weight:700}
.status .searched{font-size:15px}
.how{margin:0 0 12px}
.card{background:#fff;border-radius:10px;border:1px solid #dde1e5;border-left:8px solid var(--edge,#7f8a99);padding:12px 16px;margin:0 0 12px}
.card .head{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline}
.card .cmte{font-weight:700;font-size:15px}
.card .title{font-weight:600;font-size:16px}
.card .ref{margin:2px 0 8px;font-size:16px}
a.sym{color:#1b4f8f;font-weight:600}
.card .txt{margin:0 0 10px;white-space:pre-wrap}
mark{background:#ffe27a;color:#1d2227;padding:0 1px;border-radius:2px}
.shared{font-size:12px;color:#5a4a1a;background:#f6edcf;border-radius:4px;padding:1px 6px}
.btns{display:flex;flex-wrap:wrap;gap:8px}
.empty{background:#fff;border-radius:10px;padding:16px;border:1px dashed #9aa4ad}
.more{margin:4px 0 16px}
h2{font-size:20px;margin:28px 0 6px}
.draftbar{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.draftitem{background:#fff;border-radius:10px;border:1px solid #dde1e5;padding:10px 14px;margin:0 0 8px}
.draftitem blockquote{margin:0 0 4px;white-space:pre-wrap}
.draftitem .cit{font-weight:600}
.cannot{background:#fff;border-radius:10px;padding:8px 18px 12px;border:1px solid #d3d8dd}
.cannot li{margin:4px 0}
.toast{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);background:#1d2227;color:#fff;padding:8px 16px;border-radius:8px;font-size:15px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="label">WORKSHOP_DATA.gc &middot; general comments, paragraph by paragraph</div>
    <h1>Verbatim finder: the rights of the child</h1>
    <p class="source" id="source"></p>
    <div class="intro">
      <p>This search covers all the General Comments of every committee in the file, not only those on children. Three steps:</p>
      <ol>
        <li>Type a phrase.</li>
        <li>Compare the highlighted paragraph with the original.</li>
        <li>Copy the citation.</li>
      </ol>
    </div>
  </header>

  <main>
    <section class="search" aria-label="Search">
      <label for="q" class="label">Search phrase</label>
      <input id="q" type="search" autocomplete="off" placeholder="e.g. &quot;best interests&quot;">
      <p class="label hint">every word must appear &middot; "quotes" = words together, in that order &middot; child finds children</p>
      <div class="examples">
        <span class="label">Try</span>
        <button class="ex" type="button" data-q="&quot;best interests&quot;">"best interests"</button>
        <button class="ex" type="button" data-q="&quot;evolving capacities&quot;">"evolving capacities"</button>
        <button class="ex" type="button" data-q="child participation">child participation</button>
      </div>
    </section>

    <section aria-label="Results">
      <div class="status">
        <div><span class="big" id="count">0</span> <span id="countLabel">matching paragraphs</span></div>
        <div class="searched" id="searched"></div>
      </div>
      <p class="label how" id="how">How this is computed: each paragraph is tested in the browser against every word you typed; nothing is sent anywhere.</p>
      <div id="results" aria-live="polite"></div>
      <div class="more" id="moreBox" hidden><button class="btn" id="more" type="button">Show 50 more</button></div>
    </section>

    <section aria-label="Draft">
      <h2>Draft list <span class="label" id="draftCount"></span></h2>
      <div class="draftbar">
        <button class="btn primary" id="copyAll" type="button">Copy all</button>
        <button class="btn" id="download" type="button">Download</button>
        <button class="btn" id="clearDraft" type="button">Clear draft</button>
      </div>
      <div id="draft"></div>
    </section>

    <section aria-label="Limits">
      <h2>What this tool cannot do</h2>
      <ul class="cannot">
        <li>It does not summarise, paraphrase or find synonyms: only the words you typed. "Child" finds "children"; it does not find "minor".</li>
        <li>It searches only the attached General Comments: no concluding observations, no case law, no other sources.</li>
        <li>English only, no translation.</li>
        <li>Text is shown as stored in the file, curly apostrophes and footnote marks such as [[fn:12]] included. It does not check the file against the current UN version: click the symbol and compare.</li>
        <li>One symbol is not always one document: a symbol shared by several documents gets its short title added to the citation, and a joint General Comment carries two symbols in one field, copied as stored.</li>
      </ul>
    </section>
  </main>
</div>
<div class="toast" id="toast" role="status" hidden></div>

<script>
(function(){
  var PAGE = 50;
  var PALETTE = ['#6b8fa8','#a8786b','#7a9a6b','#9a7fa8','#b59a5a','#5f9a96','#a86b82','#7f8a99','#8f7a5f','#6b7fa8','#a89a6b','#7a6b8f'];
  var D = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.gc) || null;
  var records = (D && Array.isArray(D.records)) ? D.records : [];
  var $ = function(id){ return document.getElementById(id); };

  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function fmt(n){ return Number(n).toLocaleString('en'); }

  // committee colours: one per committee, in order of first appearance
  var colour = {}, order = [];
  // titles per symbol, to know when one symbol holds several documents
  var titlesBySymbol = {};
  var minY = null, maxY = null;
  records.forEach(function(r){
    var c = r.committee || '?';
    if (!(c in colour)){ colour[c] = PALETTE[order.length % PALETTE.length]; order.push(c); }
    var s = r.symbol || '';
    var t = r.short_title || r.title || '';
    (titlesBySymbol[s] = titlesBySymbol[s] || {})[t] = true;
    if (typeof r.year === 'number'){ if (minY === null || r.year < minY) minY = r.year; if (maxY === null || r.year > maxY) maxY = r.year; }
  });
  function sharedSymbol(r){ return Object.keys(titlesBySymbol[r.symbol || ''] || {}).length > 1; }

  var years = (minY !== null) ? (minY + '–' + maxY) : 'years not stated';
  $('source').textContent = (D && D.source ? D.source : 'Source not stated in the file') + ' · n = ' + fmt(records.length) + ' paragraphs · ' + years + ' · ' + order.length + ' committees';
  $('searched').textContent = fmt(records.length) + ' paragraphs searched';

  // ---- query parsing and matching
  function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function termRegex(term){
    var p = escRe(term.trim()).replace(/['’‘ʼ`]/g, "['’‘ʼ`]").replace(/\s+/g, '\\s+');
    return new RegExp('(?<![\\p{L}\\p{N}])' + p, 'iu');
  }
  function parse(q){
    var terms = [], re = /"([^"]*)"|(\S+)/g, m;
    while ((m = re.exec(q))){
      var t = (m[1] !== undefined ? m[1] : m[2].replace(/"/g, '')).trim();
      if (t) terms.push(t);
    }
    return terms;
  }

  var matches = [], shown = 0, lastTerms = [], hlRe = null;
  var draft = [];

  function citation(r){
    var c = (r.symbol || 'symbol not stated') + ', para. ' + (r.paragraph == null ? '?' : r.paragraph);
    if (sharedSymbol(r) && (r.short_title || r.title)) c += ' (' + (r.short_title || r.title) + ')';
    return c;
  }

  function highlight(text){
    if (!hlRe) return esc(text);
    var out = '', last = 0, m;
    hlRe.lastIndex = 0;
    while ((m = hlRe.exec(text))){
      if (m[0] === '') { hlRe.lastIndex++; continue; }
      out += esc(text.slice(last, m.index)) + '<mark>' + esc(m[0]) + '</mark>';
      last = m.index + m[0].length;
    }
    return out + esc(text.slice(last));
  }

  function cardHtml(r, i){
    var edge = colour[r.committee || '?'];
    var sym = r.symbol || 'symbol not stated';
    var link = r.doc_url ? '<a class="sym" target="_blank" rel="noopener" href="' + esc(r.doc_url) + '">' + esc(sym) + '</a>' : '<span class="sym">' + esc(sym) + '</span>';
    return '<article class="card" style="--edge:' + edge + '">' +
      '<div class="head"><span class="cmte">' + esc(r.committee || '') + '</span><span class="title">' + esc(r.short_title || r.title || '') + '</span>' +
      (sharedSymbol(r) ? '<span class="shared">symbol shared by several titles</span>' : '') + '</div>' +
      '<p class="ref">' + link + ', para. ' + esc(r.paragraph == null ? '?' : r.paragraph) + (r.year ? ' <span class="label">' + esc(r.year) + '</span>' : '') + '</p>' +
      '<p class="txt">' + highlight(r.text == null ? '' : r.text) + '</p>' +
      '<div class="btns"><button class="btn" type="button" data-act="copy" data-i="' + i + '">Copy citation</button>' +
      '<button class="btn" type="button" data-act="add" data-i="' + i + '">Add to draft</button></div></article>';
  }

  function render(append){
    var box = $('results');
    var q = $('q').value.trim();
    if (!append){
      box.innerHTML = '';
      shown = 0;
    }
    if (!records.length){
      box.innerHTML = '<div class="empty">The General Comments file is not attached to this app, so there is nothing to search. Attach it in the studio and reload.</div>';
      $('moreBox').hidden = true; $('count').textContent = '0'; return;
    }
    if (!q){
      $('count').textContent = '0';
      $('countLabel').textContent = 'matching paragraphs';
      box.innerHTML = '<div class="empty">Type a phrase above, or use one of the three examples. Every paragraph that contains your words will be listed here, in the file’s order, word for word.</div>';
      $('moreBox').hidden = true; return;
    }
    $('count').textContent = fmt(matches.length);
    $('countLabel').textContent = matches.length === 1 ? 'matching paragraph' : 'matching paragraphs';
    if (!matches.length){
      box.innerHTML = '<div class="empty">0 paragraphs contain ' + esc(lastTerms.map(function(t){ return '“' + t + '”'; }).join(' + ')) + ' among the ' + fmt(records.length) + ' searched. Only your exact words are matched (no synonyms).</div>';
      $('moreBox').hidden = true; return;
    }
    var end = Math.min(matches.length, shown + PAGE), html = '';
    for (var i = shown; i < end; i++) html += cardHtml(matches[i], i);
    box.insertAdjacentHTML('beforeend', html);
    shown = end;
    var left = matches.length - shown;
    $('moreBox').hidden = left <= 0;
    if (left > 0) $('more').textContent = 'Show ' + Math.min(PAGE, left) + ' more (' + fmt(left) + ' not yet shown)';
  }

  function search(){
    var q = $('q').value;
    var terms = parse(q);
    lastTerms = terms;
    if (!terms.length){ matches = []; hlRe = null; render(false); return; }
    var res = terms.map(termRegex);
    var sorted = terms.slice().sort(function(a, b){ return b.length - a.length; });
    hlRe = new RegExp(sorted.map(function(t){ return termRegex(t).source; }).join('|'), 'giu');
    matches = records.filter(function(r){
      var tx = r.text == null ? '' : String(r.text);
      for (var k = 0; k < res.length; k++) if (!res[k].test(tx)) return false;
      return true;
    });
    $('how').textContent = 'How this is computed: a paragraph is listed when it contains ' + (terms.length > 1 ? 'all of ' : '') + terms.map(function(t){ return '“' + t + '”'; }).join(', ') + ' (case and apostrophe shape ignored, word starts match). Words matched: ' + terms.join(', ') + '.';
    render(false);
  }

  // ---- clipboard, toast
  var toastTimer = null;
  function toast(msg){
    var t = $('toast'); t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function(){ t.hidden = true; }, 2200);
  }
  function copy(text, msg){
    function fallback(){
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      toast(ok ? msg : 'Could not copy: select the text and copy it by hand');
    }
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(text).then(function(){ toast(msg); }, fallback);
    } else fallback();
  }

  // ---- draft
  function draftText(){
    return draft.map(function(r){ return '“' + r.text + '”\n' + citation(r); }).join('\n\n');
  }
  function renderDraft(){
    $('draftCount').textContent = draft.length + (draft.length === 1 ? ' paragraph' : ' paragraphs');
    var box = $('draft');
    if (!draft.length){
      box.innerHTML = '<div class="empty">Empty. Use “Add to draft” on a result to collect paragraphs with their citations here.</div>';
      return;
    }
    box.innerHTML = draft.map(function(r, i){
      return '<div class="draftitem"><blockquote>“' + esc(r.text) + '”</blockquote><div class="cit">' + esc(citation(r)) +
        '</div><div class="btns" style="margin-top:6px"><button class="btn" type="button" data-act="remove" data-i="' + i + '">Remove</button></div></div>';
    }).join('');
  }

  // ---- events
  var timer = null;
  $('q').addEventListener('input', function(){ clearTimeout(timer); timer = setTimeout(search, 150); });
  document.querySelectorAll('.ex').forEach(function(b){
    b.addEventListener('click', function(){ $('q').value = b.getAttribute('data-q'); search(); });
  });
  $('more').addEventListener('click', function(){ render(true); });
  $('results').addEventListener('click', function(e){
    var b = e.target.closest('button[data-act]'); if (!b) return;
    var r = matches[+b.getAttribute('data-i')]; if (!r) return;
    if (b.getAttribute('data-act') === 'copy') copy(citation(r), 'Citation copied: ' + citation(r));
    else {
      if (draft.indexOf(r) === -1){ draft.push(r); renderDraft(); toast('Added to draft'); }
      else toast('Already in the draft');
    }
  });
  $('draft').addEventListener('click', function(e){
    var b = e.target.closest('button[data-act="remove"]'); if (!b) return;
    draft.splice(+b.getAttribute('data-i'), 1); renderDraft();
  });
  $('copyAll').addEventListener('click', function(){
    if (!draft.length){ toast('The draft is empty'); return; }
    copy(draftText(), 'Draft copied (' + draft.length + ')');
  });
  $('clearDraft').addEventListener('click', function(){ draft = []; renderDraft(); });
  $('download').addEventListener('click', function(){
    if (!draft.length){ toast('The draft is empty'); return; }
    var blob = new Blob([draftText() + '\n'], {type: 'text/plain;charset=utf-8'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'draft-quotations.txt';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
  });

  render(false);
  renderDraft();
})();
</script>
</body>
</html>
```
