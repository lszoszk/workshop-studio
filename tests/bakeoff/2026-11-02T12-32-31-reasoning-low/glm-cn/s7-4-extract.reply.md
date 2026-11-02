Here is the paragraph-checking app for E/C.12/GC/27: it splits the raw PDF text into numbered paragraphs, compares each opening with the answer key, flags where the converter damaged the text, and lets you download the result as CSV.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraph checker — E/C.12/GC/27</title>
<style>
  :root { --accent:#1f6fb2; --bg:#f7f9fb; --ink:#222; --line:#dde4ea; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; background:var(--bg); color:var(--ink); font-size:16px; line-height:1.5; }
  .wrap { max-width:1080px; margin:0 auto; padding:24px 20px 60px; }
  h1 { font-size:1.5rem; margin:0 0 4px; }
  h1 a, .meta a { color:var(--accent); text-decoration:none; }
  h1 a:hover, .meta a:hover { text-decoration:underline; }
  .meta { color:#556; margin-bottom:20px; }
  .note { font-size:.85rem; color:#667; margin:6px 0 0; }
  .counters { display:flex; gap:16px; flex-wrap:wrap; margin:18px 0 6px; }
  .counter { background:#fff; border:1px solid var(--line); border-radius:8px; padding:12px 18px; min-width:190px; }
  .counter .val { font-size:1.6rem; font-weight:600; }
  .counter .lbl { font-size:.85rem; color:#556; }
  .counter .val.bad { color:#b23c1f; }
  .toolbar { display:flex; align-items:center; gap:18px; flex-wrap:wrap; margin:20px 0 10px; }
  .toolbar label { display:flex; align-items:center; gap:6px; cursor:pointer; }
  button.primary { background:var(--accent); color:#fff; border:none; border-radius:6px; padding:9px 16px; font-size:1rem; cursor:pointer; }
  button.primary:hover { filter:brightness(1.1); }
  table { width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); font-size:.95rem; }
  th, td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { background:#eef3f7; font-size:.85rem; text-transform:uppercase; letter-spacing:.03em; color:#445; }
  tr.para { cursor:pointer; }
  tr.para:hover { background:#f2f7fb; }
  tr.diff td { background:#fdf3f0; }
  td.num { font-weight:600; white-space:nowrap; }
  td.pg { white-space:nowrap; color:#556; }
  td.sym { white-space:nowrap; }
  td.sym a { color:var(--accent); text-decoration:none; }
  td.sym a:hover { text-decoration:underline; }
  .mark { font-size:.78rem; font-weight:600; padding:1px 7px; border-radius:10px; }
  .mark.diff { background:#fbe3dc; color:#a03417; }
  .mark.noref { background:#e8e8e8; color:#666; }
  .mark.ok { color:#2c7a3d; }
  tr.detail td { background:#fbfcfd; }
  .detail-box { display:flex; gap:24px; flex-wrap:wrap; }
  .detail-box .full { flex:2 1 420px; white-space:pre-wrap; font-size:.88rem; background:#fff; border:1px solid var(--line); border-radius:6px; padding:12px; max-height:340px; overflow:auto; }
  .detail-box .ref { flex:1 1 260px; font-size:.88rem; }
  .detail-box .ref .lbl { font-weight:600; margin-bottom:4px; }
  details { margin-top:22px; }
  summary { cursor:pointer; font-weight:600; color:var(--accent); }
  .removed { background:#fff; border:1px solid var(--line); border-radius:6px; padding:10px 14px; margin-top:10px; max-height:320px; overflow:auto; font-size:.85rem; }
  .removed div { padding:2px 0; border-bottom:1px dashed #eee; }
  .removed .why { color:#889; font-style:italic; margin-left:8px; }
</style>
</head>
<body>
<div class="wrap">
  <h1 id="doc-title"></h1>
  <div class="meta" id="doc-meta"></div>
  <div class="counters" id="counters"></div>
  <p class="note">Found by the code from the page text; reference figures come from the file.</p>
  <div class="toolbar">
    <button class="primary" id="csv-btn">Download CSV</button>
    <label><input type="checkbox" id="diff-first"> Show differences first</label>
  </div>
  <table id="table">
    <thead><tr>
      <th>Para.</th><th>Page</th><th>First line</th><th>Document</th><th>Opening vs reference</th>
    </tr></thead>
    <tbody id="tbody"></tbody>
  </table>
  <p class="note">Click a row to see the full paragraph exactly as extracted, with the reference opening words beside it.</p>
  <details>
    <summary id="removed-summary">Lines removed as headers, footers and footnotes</summary>
    <div class="removed" id="removed-list"></div>
    <p class="note">Nothing else was discarded: every other line from the PDF text is kept inside the paragraph it belongs to.</p>
  </details>
</div>

<script>
(function () {
  const d = window.WORKSHOP_DATA.pdf_text;
  const symbol = d.symbol || "";
  const docUrl = d.doc_url || "";
  const pages = (d.records || []).slice().sort((a, b) => (a.page || 0) - (b.page || 0));
  const ref = d.reference || {};
  const refWords = ref.first_words || {};
  const refParas = ref.paragraphs;
  const refNotes = ref.footnotes;

  // ---------- header text ----------
  document.getElementById("doc-title").innerHTML =
    (docUrl ? `<a href="${docUrl}" target="_blank">${symbol}</a>` : symbol) +
    " — paragraph checker";
  document.getElementById("doc-meta").innerHTML =
    `${d.title || "Document"}, raw PDF text, ${pages.length} page${pages.length === 1 ? "" : "s"}, source: ${d.source || "not stated"}.`;

  // ---------- helpers ----------
  const words = s => (s || "").toString()
    .replace(/[“”"'’()\[\].,;:!?—–…]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase()
    .split(" ")
    .filter(Boolean);
  const firstSix = s => words(s).slice(0, 6);
  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // ---------- splitting ----------
  const removed = [];        // {page, text, reason}
  const paragraphs = [];     // {number, page, text}
  const isPageNum = l => /^\d{1,4}$/.test(l);
  const isSymbol  = l => l === symbol;
  const isGE      = l => /^GE\.\s*\d/.test(l);
  const startRe   = /^(\d{1,3})\.\s+/;

  let expected = 1;
  let cur = null;

  pages.forEach(pageRec => {
    const lines = (pageRec.text || "").split(/\r?\n/);
    const page = pageRec.page;
    // footnote candidate: small number at start, near the foot of the page
    const footZone = Math.max(0, lines.length - 8);
    lines.forEach((rawLine, i) => {
      const line = rawLine.trim();
      if (line === "") return;
      if (isPageNum(line)) { removed.push({page, text: line, reason: "page number"}); return; }
      if (isSymbol(line))  { removed.push({page, text: line, reason: "document symbol (header/footer)"}); return; }
      if (isGE(line))      { removed.push({page, text: line, reason: "distribution code"}); return; }

      const m = line.match(startRe);
      if (m && parseInt(m[1], 10) === expected) {
        // start of the next expected numbered paragraph
        if (cur) paragraphs.push(cur);
        cur = { number: expected, page, text: line };
        expected++;
        return;
      }

      // footnote heuristic: line begins with a small number + space or "N/"
      // (not "N. " which would be a paragraph number), in the foot of the page
      const fn = line.match(/^(\d{1,2})(\/|\s)\S/);
      if (fn && i >= footZone && parseInt(fn[1], 10) < expected) {
        removed.push({page, text: line, reason: "footnote (counted, not shown in paragraphs)"});
        return;
      }

      // otherwise: continuation of the current paragraph (or preamble text before para 1)
      if (cur) {
        cur.text += "\n" + line;
      } else {
        removed.push({page, text: line, reason: "front-matter before paragraph 1"});
      }
    });
  });
  if (cur) paragraphs.push(cur);

  // ---------- comparison with the reference ----------
  paragraphs.forEach(p => {
    const bodyText = p.text.replace(startRe, "");
    p.firstLine = p.text.replace(/\s+/g, " ").trim().slice(0, 90);
    p.foundWords = firstSix(bodyText);
    const refEntry = refWords[String(p.number)];
    if (refEntry === undefined) {
      p.status = "noref";
      p.refWords = null;
    } else {
      p.refWords = refEntry;
      p.status = firstSix(refEntry).join(" ") === p.foundWords.join(" ") ? "ok" : "diff";
    }
  });

  const nFound = paragraphs.length;
  const nDiff = paragraphs.filter(p => p.status === "diff").length;
  const noteLines = removed.filter(r => r.reason.indexOf("footnote") === 0);

  // ---------- counters ----------
  const counter = (val, lbl, bad) =>
    `<div class="counter"><div class="val${bad ? " bad" : ""}">${val}</div><div class="lbl">${lbl}</div></div>`;
  document.getElementById("counters").innerHTML =
    counter(nFound + " of " + (refParas !== undefined ? refParas : "?"), "numbered paragraphs found / in reference", refParas !== undefined && nFound !== refParas) +
    counter(noteLines.length + " of " + (refNotes !== undefined ? refNotes : "?"), "footnote lines removed / footnotes in reference") +
    counter(nDiff, "paragraphs whose opening words differ from the reference", nDiff > 0);

  // ---------- table ----------
  const tbody = document.getElementById("tbody");
  let openRow = null;

  function rowHtml(p) {
    let mark;
    if (p.status === "diff") mark = `<span class="mark diff">Differs</span>`;
    else if (p.status === "noref") mark = `<span class="mark noref">no reference</span>`;
    else mark = `<span class="mark ok">matches</span>`;
    return `<tr class="para ${p.status === "diff" ? "diff" : ""}" data-num="${p.number}">
      <td class="num">${p.number}</td>
      <td class="pg">p. ${p.page}</td>
      <td>${esc(p.firstLine)}${p.firstLine.length >= 90 ? "…" : ""}</td>
      <td class="sym">${docUrl ? `<a href="${docUrl}" target="_blank">${esc(symbol)}</a>` : esc(symbol)}</td>
      <td>${mark}</td>
    </tr>`;
  }

  function detailHtml(p) {
    const refBlock = p.refWords === null
      ? "<div class='lbl'>Reference opening words</div><div>No entry for this paragraph in the reference, so no comparison was made.</div>"
      : `<div class='lbl'>Reference opening words (paragraph ${p.number})</div><div>&ldquo;${esc(p.refWords)}&rdquo;</div>`;
    return `<tr class="detail"><td colspan="5">
      <div class="detail-box">
        <div class="full">${esc(p.text)}</div>
        <div class="ref">${refBlock}
          <p class="note">Shown exactly as extracted from the PDF text — nothing was edited. Opening words compared word by word, ignoring case, punctuation and extra spaces.</p>
        </div>
      </div>
    </td></tr>`;
  }

  function render() {
    const diffFirst = document.getElementById("diff-first").checked;
    let list = paragraphs.slice();
    if (diffFirst) list.sort((a, b) => (a.status === "diff" ? 0 : 1) - (b.status === "diff" ? 0 : 1) || a.number - b.number);
    tbody.innerHTML = list.map(rowHtml).join("");
    openRow = null;
    Array.from(tbody.querySelectorAll("tr.para")).forEach(tr => {
      tr.addEventListener("click", () => {
        if (openRow) openRow.nextSibling.remove();
        if (openRow === tr) { openRow = null; return; }
        const p = paragraphs.find(x => x.number === parseInt(tr.dataset.num, 10));
        tr.insertAdjacentHTML("afterend", detailHtml(p));
        openRow = tr;
      });
    });
  }
  document.getElementById("diff-first").addEventListener("change", render);
  render();

  // ---------- removed lines ----------
  document.getElementById("removed-summary").textContent =
    `Lines removed as headers, footers and footnotes (${removed.length} lines)`;
  document.getElementById("removed-list").innerHTML = removed.length
    ? removed.map(r => `<div>p. ${r.page}: ${esc(r.text)}<span class="why">— ${r.reason}</span></div>`).join("")
    : "<div>Nothing was removed.</div>";

  // ---------- CSV ----------
  document.getElementById("csv-btn").addEventListener("click", () => {
    const q = v => '"' + String(v === undefined || v === null ? "" : v).replace(/"/g, '""') + '"';
    const rows = [["paragraph", "page", "matches_reference", "full_text"].join(",")];
    paragraphs.forEach(p => {
      rows.push([
        q(p.number),
        q(p.page),
        q(p.status === "diff" ? "differs" : p.status === "noref" ? "no reference" : "matches"),
        q(p.text)
      ].join(","));
    });
    const blob = new Blob(["\uFEFF" + rows.join("\r\n")], {type: "text/csv;charset=utf-8"});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = (symbol || "document").replace(/[/\\]/g, "-") + "-paragraphs.csv";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(a.href);
  });
})();
</script>
</body>
</html>
```

Note two honest caveats shown on screen: the footnote count comes from a heuristic (small numbers at the foot of each page), so it may not exactly equal the reference figure; and paragraphs the converter mangled are flagged with "Differs" or "no reference" but never repaired.