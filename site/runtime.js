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
        return Promise.reject(new Error('AI steps only work inside the Workshop Studio. This saved copy runs without a model.'));
      }
      return new Promise(function (resolve, reject) {
        var id = ++seq;
        pending[id] = { resolve: resolve, reject: reject };
        post({ type: 'studio:ask', id: id, prompt: String(prompt), json: !!(opts && opts.json) });
      });
    },
    // the PDF of a document in the library, at a page, next to the app (a saved copy opens where it was published)
    openSource: function (id, page) {
      if (inStudio) return post({ type: 'studio:open-source', symbol: String(id), page: Number(page) || 1 });
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

  var LAYER_CSS =
    '[data-studio-layer=model]{background:rgba(245,166,35,.28)!important;outline:1px dashed #c47f00!important}' +
    '[data-studio-layer=script]{background:rgba(46,160,67,.22)!important;outline:1px solid #2ea043!important}' +
    '[data-studio-layer=ai]{background:rgba(137,87,229,.28)!important;outline:2px solid #8957e5!important}' +
    'canvas[data-studio-layer],svg[data-studio-layer]{outline-width:3px!important;outline-offset:2px}';

  function ownText(el) {
    var t = '';
    for (var n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3) t += n.nodeValue;
    return t.replace(/\s+/g, ' ').trim();
  }

  function applyLayers(on, staticTexts) {
    var style = document.getElementById('studio-layer-css');
    document.querySelectorAll('[data-studio-layer]').forEach(function (el) { el.removeAttribute('data-studio-layer'); });
    if (!on) { if (style) style.remove(); return {}; }
    if (!style) {
      style = document.createElement('style');
      style.id = 'studio-layer-css';
      style.textContent = LAYER_CSS;
      document.head.appendChild(style);
    }
    var known = {};
    (staticTexts || []).forEach(function (t) { known[t] = 1; });
    var counts = { model: 0, script: 0, ai: 0 };
    document.body.querySelectorAll('*').forEach(function (el) {
      var tag = el.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'OPTION') return;
      var layer = null;
      if (el.closest('[data-source=ai]')) {
        if (el.matches('[data-source=ai]')) layer = 'ai';
      } else if (tag === 'CANVAS' || tag === 'svg' || tag === 'SVG') {
        layer = 'script';
      } else if (tag === 'SELECT') {
        var opts = [].slice.call(el.options).map(function (o) { return o.text.replace(/\s+/g, ' ').trim(); });
        layer = opts.some(function (t) { return t && !known[t]; }) ? 'script' : 'model';
      } else if (!el.closest('svg')) {
        var t = ownText(el);
        if (t) layer = known[t] ? 'model' : 'script';
      }
      if (layer) { el.setAttribute('data-studio-layer', layer); counts[layer]++; }
    });
    return counts;
  }

  window.addEventListener('message', function (e) {
    if (e.source !== window.parent) return;
    var m = e.data || {};
    if (m.type === 'studio:answer' && pending[m.id]) {
      var p = pending[m.id];
      delete pending[m.id];
      if (m.error) p.reject(new Error(m.error)); else p.resolve(m.text);
    } else if (m.type === 'studio:layers') {
      post({ type: 'studio:layers-done', counts: applyLayers(m.on, m.staticTexts) });
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
      post({ type: 'studio:ready', fingerprint: fingerprint(), chars: document.body ? document.body.innerText.length : 0 });
    }, 700);
  });
})();
