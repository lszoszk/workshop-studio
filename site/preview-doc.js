/* Builds the document a generated app runs in: the app's own HTML with, in front of its
   scripts, a Content-Security-Policy that forbids any network access, Chart.js, the
   datasets the app uses (window.WORKSHOP_DATA) and the studio runtime (studio.ask etc.).
   Shared by the studio (studio.js) and the gallery viewer (gallery/view.html). */
window.PreviewDoc = (function () {
  'use strict';
  const DATASETS = ['uhri', 'gc', 'hrc', 'pdf_text', 'library'];
  const CSP = "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data: blob:; connect-src 'none'; form-action 'none'\">";

  function inject(html, head) {
    const m = html.match(/<head[^>]*>/i) || html.match(/<html[^>]*>/i);
    return m ? html.slice(0, m.index + m[0].length) + head + html.slice(m.index + m[0].length) : head + html;
  }

  function datasetsUsed(html) {
    if (!/WORKSHOP_DATA/.test(html)) return [];
    const found = DATASETS.filter((k) => new RegExp('\\b' + k + '\\b').test(html));
    return found.length ? found : ['uhri'];
  }

  // `dataText(k)` resolves to the JSON text of dataset k, already escaped with escapeScript()
  async function build(html, { chart, runtime, dataText }) {
    const used = datasetsUsed(html);
    const parts = await Promise.all(used.map(async (k) => JSON.stringify(k) + ':' + (await dataText(k))));
    return inject(html, CSP +
      '<script>' + escapeScript(chart) + '</script>' +
      '<script>window.WORKSHOP_DATA={' + parts.join(',') + '};</script>' +
      '<script>' + runtime + '</script>');
  }

  // the half-written page without any script, so the layout grows as the code streams in
  function skeleton(html) {
    return inject(html.replace(/<script[\s\S]*?(<\/script>|$)/gi, ''), CSP);
  }

  const escapeScript = (s) => s.replace(/<\//g, '<\\/');

  // For a frame filled from a string (srcdoc): a link to "#section" would otherwise resolve against
  // the studio's own address and load the studio inside the frame. Not for a saved file.
  const forFrame = (doc) => inject(doc, '<base href="about:srcdoc">');

  return { CSP, inject, datasetsUsed, build, skeleton, escapeScript, forFrame };
})();
