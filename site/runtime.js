/* Workshop Studio runtime. Runs inside every preview before the app's own scripts.
   The preview is a sandboxed page with no network and no access to the studio;
   this file is its only line out: studio.ask(), error reports and the fingerprint
   for "Run x3". In a downloaded copy it is inert. */
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

  window.addEventListener('message', function (e) {
    if (e.source !== window.parent) return;
    var m = e.data || {};
    if (m.type === 'studio:answer' && pending[m.id]) {
      var p = pending[m.id];
      delete pending[m.id];
      if (m.error) p.reject(new Error(m.error)); else p.resolve(m.text);
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
