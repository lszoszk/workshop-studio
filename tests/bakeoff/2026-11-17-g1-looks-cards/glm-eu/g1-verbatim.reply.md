I built the verbatim finder exactly to the plan: one screen, phrase search with quoted phrases, results as index cards with a coloured edge per committee, copy-ready citations, a draft list with copy-all and download, the paragraphs-searched count always visible, and an on-screen list of what it cannot do.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verbatim finder — General Comments on the rights of persons with disabilities</title>
<style>
  :root{
    --bg:#eef0f2; --card:#ffffff; --ink:#1d1b18; --rule:#d4d7db;
    --accent:#9b2335; --muted:#5c5f63;
  }
  *{box-sizing:border-box}
  [hidden]{display:none!important}
  body{margin:0;background:var(--bg);color:var(--ink);
       font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
       font-size:16px;line-height:1.55}
  .mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11.5px;
        letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
  header{padding:20px 24px 14px;border-bottom:1px solid var(--rule);background:var(--card)}
  header h1{font-size:22px;margin:6px 0 4px;font-weight:700}
  header .src{font-size:13px;color:var(--muted)}
  main{max-width:960px;margin:0 auto;padding:20px 24px 60px}
  .searchbar{display:flex;gap:10px;align-items:center;margin:14px 0 6px}
  #q{flex:1;font-size:17px;padding:11px 14px;border:1px solid var(--rule);
     border-radius:8px;background:var(--card);color:var(--ink)}
  #q:focus{outline:2px solid var(--accent);outline-offset:1px}
  button{cursor:pointer;font-family:inherit}
  .go{background:var(--accent);color:#fff;border:none;border-radius:8px;
      padding:11px 20px;font-size:16px;font-weight:600}
  .examples{margin:8px 0 4px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
  .ex{background:var(--card);border:1px solid var(--rule);border-radius:16px;
      padding:4px 12px;font-size:13px;color:var(--ink)}
  .ex:hover{border-color:var(--accent)}
  .hint{font-size:13px;color:var(--muted);margin:6px 0 18px}
  .countline{display:flex;justify-content:space-between;align-items:baseline;
             margin:0 0 14px;gap:10px;flex-wrap:wrap}
  .bignum{font-size:40px;font-weight:700;line-height:1}
  .bignum small{font-size:15px;font-weight:400;color:var(--muted)}
  mark{background:#f7e3a1;padding:0 1px;border-radius:2px}
  .card{background:var(--card);border-radius:10px;padding:14px 18px 14px 16px;
        margin:0 0 14px;border-left:6px solid #999;box-shadow:0 1px 2px rgba(0,0,0,.05)}
  .card .meta{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline;margin-bottom:6px}
  .card .meta .com{font-weight:700;font-size:14px}
  .card .meta a{color:var(--accent);text-decoration:none;font-size:14px}
  .card .meta a:hover{text-decoration:underline}
  .card .meta .para{font-size:14px;color:var(--muted)}
  .card .title{font-size:13.5px;color:var(--muted);margin:0 0 8px}
  .card .text{font-size:15.5px;white-space:pre-wrap}
  .card .acts{margin-top:10px;display:flex;gap:8px}
  .btn{background:var(--card);border:1px solid var(--rule);border-radius:6px;
       padding:5px 12px;font-size:13.5px}
  .btn:hover{border-color:var(--accent)}
  .btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
  .nomatch{background:var(--card);border-radius:10px;padding:18px;margin-bottom:14px}
  .draft{background:var(--card);border-radius:10px;padding:16px 18px;margin-top:26px}
  .draft h2{font-size:17px;margin:0 0 4px}
  .draft .ditem{border-top:1px solid var(--rule);padding:10px 0}
  .draft .ditem:first-of-type{border-top:none}
  .draft .dtext{font-size:14.5px;margin:4px 0 0}
  .limits{background:var(--card);border-radius:10px;padding:16px 18px;margin-top:26px}
  .limits h2{font-size:17px;margin:0 0 6px}
  .limits ul{margin:6px 0 0;padding-left:20px;font-size:14.5px;color:var(--muted)}
  .toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);
         background:var(--ink);color:#fff;border-radius:6px;padding:8px 16px;
         font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none}
  .toast.show{opacity:1}
  a:focus,button:focus{outline:2px solid var(--accent);outline-offset:1px}
</style>
</head>
<body>
<header>
  <div class="mono">General Comments, paragraph by paragraph</div>
  <h1>Verbatim finder — the rights of persons with disabilities</h1>
  <div class="src" id="srcline"></div>
</header>
<main>
  <form id="form" class="searchbar" role="search">
    <input id="q" type="search" placeholder='Type words, or "a phrase in quotes"' aria-label="Search paragraphs">
    <button class="go" type="submit">Search</button>
  </form>
  <div class="examples">
    <span class="mono">try</span>
    <button class="ex" type="button">"persons with disabilities"</button>
    <button class="ex" type="button">"reasonable accommodation"</button>
    <button class="ex" type="button">inclusion disability education</button>
  </div>
  <p class="hint">Every word must appear in the paragraph, in any order; words in quotation marks must appear together, word for word. Case and apostrophe shape (’ or ') are ignored; <span class="mono">child</span> finds <span class="mono">children</span>. Literal matches only — no synonyms.</p>

  <div class="countline">
    <div class="bignum"><span id="nmatch">0</span> <small>matching paragraphs</small></div>
    <div class="mono" id="nsearched"></div>
  </div>

  <div id="results" aria-live="polite"></div>

  <section class="draft" id="draftsec" hidden>
    <h2>Your draft</h2>
    <p class="mono" id="draftcount"></p>
    <div id="draftlist"></div>
    <div class="acts" style="margin-top:12px">
      <button class="btn" id="copyall" type="button">Copy all</button>
      <button class="btn" id="download" type="button">Download</button>
      <button class="btn" id="cleardraft" type="button">Clear</button>
    </div>
  </section>

  <section class="limits">
    <h2>What this tool cannot do</h2>
    <ul>
      <li>No summaries, paraphrase or synonyms: it finds only the words you type.</li>
      <li>No other sources: General Comments only — no concluding observations, no case law.</li>
      <li>No translation: English only.</li>
      <li>Paragraphs are shown exactly as stored, including footnote marks like [[fn:12]].</li>
    </ul>
  </section>
</main>
<div class="toast" id="toast"></div>

<script>
(function(){
  var GC = window.WORKSHOP_DATA.gc;
  var records = GC.records || [];

  // header source line: n and years, computed from the data
  (function(){
    var years = records.map(function(r){return r.year;})
      .filter(function(y){return typeof y === "number";});
    var lo = years.length ? Math.min.apply(null, years) : "—";
    var hi = years.length ? Math.max.apply(null, years) : "—";
    document.getElementById("srcline").textContent =
      (GC.source ? GC.source + " · " : "") + records.length.toLocaleString() +
      " paragraphs · " + lo + "–" + hi;
  })();

  document.getElementById("nsearched").textContent =
    records.length.toLocaleString() + " paragraphs searched";

  // symbols that hold several titles: citation adds the short title
  var titlesBySymbol = {};
  records.forEach(function(r){
    if(!titlesBySymbol[r.symbol]) titlesBySymbol[r.symbol] = {};
    titlesBySymbol[r.symbol][r.short_title || r.title || ""] = true;
  });
  function multiTitle(symbol){
    return Object.keys(titlesBySymbol[symbol] || {}).length > 1;
  }

  // committee colours (muted)
  var PALETTE = ["#7a68a3","#3f7cac","#c2724b","#5a8a4a","#a3526b",
                 "#8a7a3a","#4a7a8a","#9b2335","#6b6b6b","#2f6b5a"];
  var comColor = {}, pi = 0;
  records.forEach(function(r){
    if(!comColor[r.committee]) comColor[r.committee] = PALETTE[pi++ % PALETTE.length];
  });

  // ---- matching ----
  function norm(s){
    return (s || "").replace(/\u2019/g, "'").replace(/\u2018/g, "'")
                    .replace(/[\u201c\u201d]/g, '"').toLowerCase();
  }
  function esc(s){return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");}
  function wordRe(w){
    // word must start a word in the text: child finds children
    return new RegExp("(?<![\\p{L}\\p{N}])" + esc(w), "u");
  }
  function parseQuery(q){
    var phrases = [], words = [], re = /"([^"]+)"/g, m, rest = q;
    while((m = re.exec(q)) !== null){
      var p = m[1].trim();
      if(p) phrases.push(norm(p));
      rest = rest.replace(m[0], " ");
    }
    rest.split(/[^\p{L}\p{N}'-]+/u).forEach(function(w){
      w = w.replace(/^[-']+|[-']+$/g, "");
      if(w) words.push(norm(w));
    });
    return {phrases:phrases, words:words};
  }
  function matches(text, pq){
    var t = norm(text);
    for(var i=0;i<pq.phrases.length;i++)
      if(t.indexOf(pq.phrases[i]) === -1) return false;
    for(var j=0;j<pq.words.length;j++)
      if(!wordRe(pq.words[j]).test(t)) return false;
    return true;
  }
  function highlight(text, pq){
    var patterns = [];
    pq.phrases.forEach(function(p){patterns.push(esc(p));});
    pq.words.forEach(function(w){patterns.push("(?<![\\p{L}\\p{N}])" + esc(w) + "[\\p{L}\\p{N}']*");});
    if(!patterns.length) return null;
    var re = new RegExp("(" + patterns.join("|") + ")", "giu");
    var out = "", last = 0, m;
    while((m = re.exec(text)) !== null){
      out += text.slice(last, m.index) + "<mark>" + m[0] + "</mark>";
      last = m.index + m[0].length;
      if(m[0].length === 0) re.lastIndex++;
    }
    out += text.slice(last);
    return out;
  }

  // ---- citation ----
  function citation(r){
    var c = r.symbol + ", para. " + r.paragraph;
    if(multiTitle(r.symbol)) c += " (" + (r.short_title || r.title) + ")";
    return c;
  }

  // ---- clipboard ----
  function toast(msg){
    var t = document.getElementById("toast");
    t.textContent = msg; t.classList.add("show");
    setTimeout(function(){t.classList.remove("show");}, 1600);
  }
  function copyText(txt, msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(function(){toast(msg);},
        function(){fallbackCopy(txt, msg);});
    } else fallbackCopy(txt, msg);
  }
  function fallbackCopy(txt, msg){
    var ta = document.createElement("textarea");
    ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try{document.execCommand("copy"); toast(msg);}
    catch(e){toast("Copy failed — select the text manually.");}
    document.body.removeChild(ta);
  }

  // ---- draft ----
  var draft = [];
  function renderDraft(){
    var sec = document.getElementById("draftsec");
    sec.hidden = draft.length === 0;
    document.getElementById("draftcount").textContent =
      draft.length + " paragraph" + (draft.length === 1 ? "" : "s") + " in your draft";
    var list = document.getElementById("draftlist");
    list.innerHTML = "";
    draft.forEach(function(r){
      var d = document.createElement("div");
      d.className = "ditem";
      d.innerHTML = "<div><strong>" + r.committee + "</strong> · <a href='" +
        r.doc_url + "' target='_blank' rel='noopener'>" + r.symbol + "</a>, para. " +
        r.paragraph + " <button class='btn' style='margin-left:8px' type='button'>Remove</button></div>" +
        "<p class='dtext'></p>";
      d.querySelector("p").textContent = r.text;
      d.querySelector("button").addEventListener("click", function(){
        draft = draft.filter(function(x){return x !== r;});
        renderDraft();
      });
      list.appendChild(d);
    });
  }
  function draftText(){
    return draft.map(function(r){
      return citation(r) + "\n\n" + r.text;
    }).join("\n\n---\n\n");
  }
  document.getElementById("copyall").addEventListener("click", function(){
    copyText(draftText(), "Draft copied (" + draft.length + " paragraphs)");
  });
  document.getElementById("download").addEventListener("click", function(){
    var blob = new Blob([draftText()], {type:"text/plain;charset=utf-8"});
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "verbatim-draft.txt";
    document.body.appendChild(a); a.click();
    setTimeout(function(){URL.revokeObjectURL(a.href); a.remove();}, 500);
  });
  document.getElementById("cleardraft").addEventListener("click", function(){
    draft = []; renderDraft();
  });

  // ---- search & render ----
  var lastPq = null;
  function run(q){
    var pq = parseQuery(q);
    lastPq = pq;
    var hits = [];
    if(pq.phrases.length || pq.words.length){
      for(var i=0;i<records.length;i++){
        if(matches(records[i].text, pq)) hits.push(records[i]);
      }
    }
    document.getElementById("nmatch").textContent = hits.length.toLocaleString();
    var res = document.getElementById("results");
    res.innerHTML = "";
    if(!pq.phrases.length && !pq.words.length){
      var p = document.createElement("p");
      p.className = "hint";
      p.textContent = "Type a word or a quoted phrase to search " +
        records.length.toLocaleString() + " paragraphs.";
      res.appendChild(p);
      return;
    }
    if(!hits.length){
      var nm = document.createElement("div");
      nm.className = "nomatch";
      nm.innerHTML = "<strong>No match.</strong> 0 of " +
        records.length.toLocaleString() +
        " paragraphs contain every word you typed. Try fewer words, or check the spelling.";
      res.appendChild(nm);
      return;
    }
    hits.forEach(function(r){
      var card = document.createElement("article");
      card.className = "card";
      card.style.borderLeftColor = comColor[r.committee] || "#999";
      var cite = citation(r);
      card.innerHTML =
        "<div class='meta'>" +
          "<span class='com'>" + r.committee + "</span>" +
          "<a href='" + r.doc_url + "' target='_blank' rel='noopener'>" + r.symbol + "</a>" +
          "<span class='para'>para. " + r.paragraph + "</span>" +
        "</div>" +
        "<p class='title'>" + (r.short_title || r.title || "") + "</p>" +
        "<p class='text'></p>" +
        "<div class='acts'>" +
          "<button class='btn primary' data-act='cite' type='button'>Copy citation</button>" +
          "<button class='btn' data-act='add' type='button'>Add to draft</button>" +
        "</div>";
      var textEl = card.querySelector(".text");
      var hl = highlight(r.text, pq);
      if(hl !== null) textEl.innerHTML = hl; else textEl.textContent = r.text;
      card.querySelector("[data-act='cite']").addEventListener("click", function(){
        copyText(cite, "Copied: " + cite);
      });
      card.querySelector("[data-act='add']").addEventListener("click", function(){
        if(draft.indexOf(r) === -1) draft.push(r);
        renderDraft();
        toast("Added to draft (" + draft.length + ")");
      });
      res.appendChild(card);
    });
  }

  document.getElementById("form").addEventListener("submit", function(e){
    e.preventDefault();
    run(document.getElementById("q").value.trim());
  });
  Array.prototype.forEach.call(document.querySelectorAll(".ex"), function(b){
    b.addEventListener("click", function(){
      document.getElementById("q").value = b.textContent;
      run(b.textContent);
    });
  });

  renderDraft();
})();
</script>
</body>
</html>
```