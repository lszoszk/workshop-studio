/* Workshop Studio runtime. Runs inside every preview before the app's own scripts.
   The preview is a sandboxed page with no network and no access to the studio;
   this file is its only line out: studio.ask(), error reports, the fingerprint
   for "Run x3" and the colouring for "Layers". In a downloaded copy it is inert. */
(function () {
  var inStudio = window.parent !== window;
  var pending = {}, seq = 0;

  function post(msg) { if (inStudio) window.parent.postMessage(msg, '*'); }

  window.studio = {
    ask: function (prompt, opts) {
      if (!inStudio) {
        return Promise.reject(new Error('AI steps only work inside Garage Research. This saved copy runs without a model.'));
      }
      return new Promise(function (resolve, reject) {
        var id = ++seq;
        pending[id] = { resolve: resolve, reject: reject };
        post({ type: 'studio:ask', id: id, prompt: String(prompt), json: !!(opts && opts.json) });
      });
    },
    // the PDF of a document in the library, at a page, next to the app, the quoted passage marked (a saved copy opens where it was published)
    openSource: function (id, page, quote) {
      if (inStudio) return post({ type: 'studio:open-source', symbol: String(id), page: Number(page) || 1, quote: quote ? String(quote) : '' });
      var lib = (window.WORKSHOP_DATA && WORKSHOP_DATA.library && WORKSHOP_DATA.library.records) || [];
      var doc = lib.filter(function (d) { return d.id === id || d.symbol === id; })[0];
      window.open(doc ? doc.url : 'https://docs.un.org/en/' + id, '_blank', 'noopener');
    }
  };

  // FNV-1a over the visible text and the numbers behind every chart
  function fingerprint() {
    var s = document.body ? document.body.innerText : '';
    try {
      if (window.Chart && Chart.instances) {
        Object.keys(Chart.instances).forEach(function (k) {
          var c = Chart.instances[k];
          s += JSON.stringify(c.data.labels) + JSON.stringify(c.data.datasets.map(function (d) { return d.data; }));
        });
      }
    } catch (e) { /* a chart without data still fingerprints by its text */ }
    var h = 0x811c9dc5;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = (h * 0x01000193) >>> 0; }
    return ('0000000' + h.toString(16)).slice(-8);
  }

  // what a run shows, in words a reader can compare: the first short lines with a number in them (the
  // innermost element that holds the whole line), and how many numbers and charts the screen has
  function shown() {
    var picks = [], els = [], all = document.body ? document.body.querySelectorAll('*') : [];
    for (var i = 0; i < all.length && picks.length < 6; i++) {
      var el = all[i];
      if (/^(SCRIPT|STYLE|OPTION|TEXTAREA|SELECT|BUTTON)$/.test(el.tagName) || !el.offsetParent) continue;
      if (els.some(function (p) { return p.contains(el); }) || el.closest('[role=tablist], nav')) continue;
      if (el.querySelector('button, input, select, [role=tab]')) continue;   // a control bar, not a result
      var t = (el.innerText || '').replace(/\s+/g, ' ').trim();
      // a result: a number that is not a numbered label ("01 Keyword")
      if (!t || t.length > 70 || !/(^|[^\d])[1-9]/.test(t) || picks.indexOf(t) >= 0) continue;
      picks.push(t); els.push(el);
    }
    var text = document.body ? document.body.innerText : '';
    var charts = window.Chart && Chart.instances ? Object.keys(Chart.instances).length : 0;
    return { picks: picks, numbers: (text.match(/\d[\d,.]*/g) || []).length, charts: charts };
  }

  // Layers: which words on screen the model wrote into its code (amber), which the code computed from
  // the data (green), which a model produced while the app ran (purple). A text that is a value of the
  // data is computed; otherwise a run of words is "written" when it stands in the model's source, and a
  // number only when the source holds it as a piece of text of its own ('01', >01<), not as 31px or a
  // calculation. Drawn as an overlay above the app, so the app's own page is never changed, and redrawn
  // when it scrolls or changes.
  var LAYER_CSS =
    '#studio-layers{position:fixed;inset:0;pointer-events:none;z-index:2147483647}' +
    '#studio-layers div{position:fixed;box-sizing:border-box}' +
    '#studio-layers .model{background:rgba(245,166,35,.30);outline:1px dashed #c47f00}' +
    '#studio-layers .script{background:rgba(46,160,67,.24);outline:1px solid #2ea043}' +
    '#studio-layers .ai{outline:2px solid #8957e5;background:rgba(137,87,229,.12)}' +
    '#studio-layers .chart{outline:3px solid #2ea043}';
  var layers = null;   // {source, data, box, style, observer, frame}

  function dataValues() {   // every text value in WORKSHOP_DATA, spaces collapsed
    var out = new Set(), stack = [window.WORKSHOP_DATA], n = 0;
    while (stack.length && n < 400000) {
      var v = stack.pop(); n++;
      if (typeof v === 'string') { var t = v.replace(/\s+/g, ' ').trim(); if (t.length > 1) out.add(t); }
      else if (v && typeof v === 'object') for (var k in v) stack.push(v[k]);
    }
    return out;
  }

  function numberInSource(num, source) {
    var e = num.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return new RegExp('[\'"`>]\\s?' + e + '\\s?[\'"`<]').test(source);
  }

  function decodeSource(html) {   // the source as text: entities and string escapes undone, spaces collapsed
    return html.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'")
      .replace(/\\u([0-9a-fA-F]{4})/g, function (m, h) { return String.fromCharCode(parseInt(h, 16)); })
      .replace(/\\(['"`])/g, '$1').replace(/\s+/g, ' ');
  }

  // the words of one text node, grouped into runs that the source holds (model) or does not (script)
  function segments(text, source) {
    var toks = [], re = /\S+/g, m;
    while ((m = re.exec(text))) toks.push({ s: m.index, e: m.index + m[0].length, t: m[0] });
    var out = [], i = 0;
    while (i < toks.length) {
      var best = -1;
      for (var j = i; j < toks.length; j++) {
        var run = text.slice(toks[i].s, toks[j].e).replace(/\s+/g, ' ');
        if (source.indexOf(run) < 0) break;
        var words = /[^\d\s.,:;%()\-–+/·]/.test(run);
        if (words ? (run.length >= 3 || j > i) : numberInSource(run, source)) best = j;
      }
      var layer = best >= 0 ? 'model' : 'script', end = best >= 0 ? best : i;
      var last = out[out.length - 1];
      if (last && last.layer === layer) last.e = toks[end].e; else out.push({ layer: layer, s: toks[i].s, e: toks[end].e });
      i = end + 1;
    }
    return out;
  }

  function box(cls, r, title) {
    var d = document.createElement('div');
    d.className = cls;
    d.style.left = r.left + 'px'; d.style.top = r.top + 'px'; d.style.width = r.width + 'px'; d.style.height = r.height + 'px';
    if (title) d.setAttribute('data-t', title);
    layers.box.appendChild(d);
  }

  function drawLayers() {
    layers.frame = 0;
    var counts = { model: 0, script: 0, ai: 0 }, H = window.innerHeight, W = window.innerWidth;
    layers.box.textContent = '';
    var seen = function (r) { return r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < H && r.right > 0 && r.left < W; };
    document.querySelectorAll('[data-source=ai]').forEach(function (el) {
      if (el.parentElement && el.parentElement.closest('[data-source=ai]')) return;
      var r = el.getBoundingClientRect(); if (seen(r)) { box('ai', r); counts.ai++; }
    });
    document.querySelectorAll('canvas, svg').forEach(function (el) {
      if (el.closest('[data-source=ai]') || (el.parentElement && el.parentElement.closest('svg'))) return;
      var r = el.getBoundingClientRect(); if (seen(r)) { box('chart', r); counts.script++; }
    });
    var walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentElement;
        if (!p || !n.nodeValue.trim() || p.closest('script, style, option, textarea, svg, [data-source=ai], #studio-layers')) return NodeFilter.FILTER_REJECT;
        var r = p.getBoundingClientRect();
        return seen(r) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      } });
    var range = document.createRange();
    for (var n = walk.nextNode(); n; n = walk.nextNode()) {
      var whole = n.nodeValue.replace(/\s+/g, ' ').trim();
      var parts = layers.data.has(whole) ? [{ layer: 'script', s: 0, e: n.nodeValue.length }] : segments(n.nodeValue, layers.source);
      parts.forEach(function (sg) {
        range.setStart(n, sg.s); range.setEnd(n, sg.e);
        var rects = range.getClientRects(), t = n.nodeValue.slice(sg.s, sg.e);
        for (var k = 0; k < rects.length; k++) if (seen(rects[k])) box(sg.layer, rects[k], t);
        counts[sg.layer]++;
      });
    }
    return counts;
  }

  function redraw() { if (layers && !layers.frame) layers.frame = requestAnimationFrame(drawLayers); }

  function applyLayers(on, source) {
    if (layers) {
      layers.observer.disconnect();
      document.removeEventListener('scroll', redraw, true);
      window.removeEventListener('resize', redraw);
      layers.box.remove(); layers.style.remove();
      layers = null;
    }
    if (!on) return {};
    layers = { source: decodeSource(String(source || '')), data: dataValues(), box: document.createElement('div'), style: document.createElement('style'), frame: 0 };
    layers.style.textContent = LAYER_CSS;
    layers.box.id = 'studio-layers';
    document.head.appendChild(layers.style);
    document.body.appendChild(layers.box);
    layers.observer = new MutationObserver(function (list) {
      if (list.some(function (m) { return !layers.box.contains(m.target) && m.target !== layers.box; })) redraw();
    });
    layers.observer.observe(document.body, { subtree: true, childList: true, characterData: true, attributes: true });
    document.addEventListener('scroll', redraw, true);
    window.addEventListener('resize', redraw);
    return drawLayers();
  }

  window.addEventListener('message', function (e) {
    if (e.source !== window.parent) return;
    var m = e.data || {};
    if (m.type === 'studio:answer' && pending[m.id]) {
      var p = pending[m.id];
      delete pending[m.id];
      if (m.error) p.reject(new Error(m.error)); else p.resolve(m.text);
    } else if (m.type === 'studio:layers') {
      post({ type: 'studio:layers-done', counts: applyLayers(m.on, m.source) });
    } else if (m.type === 'studio:fingerprint') {
      post({ type: 'studio:fingerprint', token: m.token, fingerprint: fingerprint() });
    }
  });

  window.addEventListener('error', function (e) {
    post({ type: 'studio:error', message: String(e.message || e), line: e.lineno || null });
  });
  window.addEventListener('unhandledrejection', function (e) {
    var r = e.reason;
    post({ type: 'studio:error', message: 'Unhandled: ' + (r && r.message ? r.message : String(r)), line: null });
  });
  window.addEventListener('load', function () {
    setTimeout(function () {
      post({ type: 'studio:ready', fingerprint: fingerprint(), shown: shown(), chars: document.body ? document.body.innerText.length : 0 });
    }, 700);
  });
})();
