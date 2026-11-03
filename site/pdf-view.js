/* A library PDF at a page, the quoted passage marked: for the studio's drawer, the app in a tab of its
   own and the gallery. The browser's own PDF viewer can open a page but not mark a passage, so PDF.js
   (vendor/pdfjs, Apache 2.0) draws the page and the quotation is found in its text; if PDF.js fails,
   the browser's viewer opens the page. */
(function () {
  let pdfjs = null;
  const loadPdfjs = (base) => pdfjs || (pdfjs = new Promise((ok, fail) => {
    const s = document.createElement('script');
    s.src = base + 'vendor/pdfjs/pdf.min.js';
    s.onload = () => { window.pdfjsLib.GlobalWorkerOptions.workerSrc = base + 'vendor/pdfjs/pdf.worker.min.js'; ok(window.pdfjsLib); };
    s.onerror = () => { pdfjs = null; fail(new Error('PDF.js did not load')); };
    document.head.append(s);
  }));
  const pdfDocs = {};

  // the same text, whatever the PDF did to it: case, curly quotes, dashes, spaces, a word hyphenated at a line end
  const normChar = (c) => /[‘’‚′`]/.test(c) ? "'" : /[“”„″]/.test(c) ? '"' : /[‐-―−]/.test(c) ? '-' : /\s/.test(c) ? ' ' : c.toLowerCase();
  const normQuote = (q) => [...q].map(normChar).join('').replace(/\s+/g, ' ').trim();

  // the text items that hold each fragment of the quotation (a quotation may join fragments with "…")
  function findQuote(items, quote) {
    const text = [], owner = [];
    items.forEach((it, i) => {
      for (const c of it.str) {
        const n = normChar(c);
        if (n === ' ' && (!text.length || text[text.length - 1] === ' ')) continue;
        text.push(n); owner.push(i);
      }
      if (!it.hasEOL) return;   // PDF.js may cut a word into two items; spaces come as items of their own
      const last = text[text.length - 1];
      if (last === '-' && /[a-z]/.test(text[text.length - 2] || '')) { text.pop(); owner.pop(); }   // environ- / ment
      else if (last !== ' ') { text.push(' '); owner.push(-1); }
    });
    const hay = text.join(''), hit = new Set();
    String(quote || '').split(/…|\.\.\./).map(normQuote).filter((f) => f.length >= 8).forEach((f) => {
      let at = hay.indexOf(f), len = f.length;
      for (const cut of [60, 40, 25]) {   // a quotation that runs on to the next page: its beginning is on this one
        if (at >= 0 || f.length <= cut) continue;
        len = cut;
        at = hay.indexOf(f.slice(0, cut));
      }
      if (at < 0) return;
      for (let k = at; k < at + len; k++) if (owner[k] >= 0) hit.add(owner[k]);
    });
    return [...hit].sort((a, b) => a - b);
  }

  async function drawPage(pdf, n, quote, view, note) {
    const pg = await pdf.getPage(n);
    const width = view.clientWidth - 2 || 760;
    const vp = pg.getViewport({ scale: width / pg.getViewport({ scale: 1 }).width });
    const dpr = window.devicePixelRatio || 1;
    const sheet = document.createElement('div');
    sheet.className = 'pdfpage';
    sheet.style.width = vp.width + 'px';
    sheet.style.height = vp.height + 'px';
    const canvas = document.createElement('canvas');
    canvas.width = Math.floor(vp.width * dpr);
    canvas.height = Math.floor(vp.height * dpr);
    sheet.append(canvas);
    await pg.render({ canvasContext: canvas.getContext('2d'), viewport: vp, transform: dpr !== 1 ? [dpr, 0, 0, dpr, 0, 0] : null }).promise;
    const items = (await pg.getTextContent()).items;
    const hits = quote ? findQuote(items, quote) : [];
    hits.forEach((i) => {
      const it = items[i], t = it.transform, h = it.height || Math.hypot(t[2], t[3]);
      const [x1, y1, x2, y2] = vp.convertToViewportRectangle([t[4], t[5] - h * 0.25, t[4] + it.width, t[5] + h]);
      const mark = document.createElement('div');
      mark.className = 'pdfmark';
      Object.assign(mark.style, { left: Math.min(x1, x2) + 'px', top: Math.min(y1, y2) + 'px', width: Math.abs(x2 - x1) + 'px', height: Math.abs(y2 - y1) + 'px' });
      sheet.append(mark);
    });
    const nav = (k) => `<button type="button" class="ghost small" data-to="${n + k}"${n + k < 1 || n + k > pdf.numPages ? ' disabled' : ''}>${k < 0 ? '← Previous page' : 'Next page →'}</button>`;
    note.innerHTML = `${nav(-1)} <span>PDF page ${n} of ${pdf.numPages}</span> ${nav(1)} <span class="pdf-found">` +
      (!quote ? '' : hits.length ? 'The quoted passage is marked.' : 'The quotation was not found on this page; the page is shown as it is.') + '</span>';
    note.querySelectorAll('button[data-to]').forEach((b) => { b.onclick = () => { view.innerHTML = ''; drawPage(pdf, Number(b.dataset.to), quote, view, note); }; });
    view.innerHTML = '';
    view.append(sheet);
    const first = sheet.querySelector('.pdfmark');
    view.scrollTop = first ? Math.max(0, first.offsetTop - 80) : 0;
  }

  // fill `box` (a drawer's body) with `head` and the page; `base` leads from the page to the site's root
  async function open(box, file, page, quote, head, base) {
    box.innerHTML = (head || '') + '<p class="pdf-note" id="pdfNote">Opening the PDF…</p><div class="pdfview" id="pdfView"></div>';
    try {
      const lib = await loadPdfjs(base || '');
      const pdf = await (pdfDocs[file] = pdfDocs[file] || lib.getDocument(file).promise);
      await drawPage(pdf, Math.min(page, pdf.numPages), quote, box.querySelector('.pdfview'), box.querySelector('.pdf-note'));
    } catch (e) {
      box.innerHTML = (head || '') + `<iframe class="pdf" src="${file}#page=${page}" title="The document"></iframe>`;
    }
  }

  window.PdfView = { open, findQuote };
})();
