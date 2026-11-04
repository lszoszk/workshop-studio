/* Builds the document a generated app runs in: the app's own HTML with, in front of its
   scripts, a Content-Security-Policy that forbids any network access, Chart.js, the
   datasets the app uses (window.WORKSHOP_DATA) and the studio runtime (studio.ask etc.).
   Shared by the studio (studio.js) and the gallery viewer (gallery/view.html). */
window.PreviewDoc = (function () {
  'use strict';
  const DATASETS = ['uhri', 'gc', 'hrc', 'pdf_text', 'pdf_text_2', 'library', 'wiki'];
  const CSP = "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data: blob:; connect-src 'none'; form-action 'none'\">";

  const CHART_CDN = /<script\b[^>]*\bsrc=["']https?:\/\/[^"']*\bchart(?:\.js|\.umd|\.min)[^"']*["'][^>]*>\s*<\/script>/gi;

  function inject(html, head) {
    const m = html.match(/<head[^>]*>/i) || html.match(/<html[^>]*>/i);
    return m ? html.slice(0, m.index + m[0].length) + head + html.slice(m.index + m[0].length) : head + html;
  }

  function datasetsUsed(html) {
    if (!/WORKSHOP_DATA/.test(html)) return [];
    const found = DATASETS.filter((k) => new RegExp('\\b' + k + '\\b').test(html));
    return found.length ? found : ['uhri'];
  }

  // `dataText(k)` resolves to the JSON text of dataset k, already escaped with escapeScript();
  // `files` are the keys attached in the app's conversation: a file in the chat gives the app the
  // whole file, also to an app that reads WORKSHOP_DATA in a loop and never names it
  async function build(html, { chart, runtime, dataText, files }) {
    // Chart.js comes with the studio; a model that also loads it from a CDN (Mistral Large 3 did in five
    // builds of five, 4.11.2026) would only get a blocked request and an error in the console
    html = html.replace(CHART_CDN, '<!-- Chart.js: the studio\'s own copy, not the internet -->');
    const attached = /WORKSHOP_DATA/.test(html) ? (files || []).filter((k) => DATASETS.includes(k)) : [];
    const named = DATASETS.filter((k) => new RegExp('\\b' + k + '\\b').test(html));
    const used = attached.length ? [...new Set([...named, ...attached])] : datasetsUsed(html);
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
