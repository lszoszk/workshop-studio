Here's the paragraph-checking tool. It splits the raw page text into numbered paragraphs with the rules you set out, checks each opening against the reference's first words, and keeps every removed line visible for review.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paragraph check</title>
<style>
  :root{
    --accent:#1f6fb2; --accent-dark:#175a91;
    --bg:#f4f6f8; --card:#ffffff; --line:#d9dfe5; --ink:#1c2733; --muted:#5a6672;
    --red:#b3261e; --red-bg:#fdecea; --green:#1e7a3c; --green-bg:#e9f6ee; --noref-bg:#eef1f4;
  }
  *{ box-sizing:border-box; }
  body{
    margin:0; background:var(--bg); color:var(--ink);
    font:16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  .wrap{ max-width:1120px; margin:0 auto; padding:30px 26px 70px; }
  a{ color:var(--accent); }
  h1{ font-size:26px; line-height:1.3; margin:6px 0 6px; }
  .kicker{ text-transform:uppercase; letter-spacing:.08em; font-size:13px; color:var(--accent); font-weight:600; margin:0; }
  .sub{ color:var(--muted); margin:0 0 4px; }
  .sym{ font-weight:600; }
  .card{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:18px 20px; margin:18px 0; }
  .how{ font-size:14px; color:var(--muted); margin:10px 0 0; }
  .stats{ display:flex; flex-wrap:wrap; gap:14px; margin:18px 0 0; }
  .stat{ flex:1 1 200px; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:16px 18px; }
  .stat .big{ font-size:34px; font-weight:700; color:var(--accent); line-height:1.1; }
  .stat .big .of{ font-size:17px; font-weight:600; color:var(--muted); margin-left:6px; }
  .stat .lab{ margin-top:6px; font-size:14px; color:var(--muted); }
  .toolbar{ display:flex; flex-wrap:wrap; align-items:center; gap:18px; margin:22px 0 10px; }
  .toolbar label{ display:flex; align-items:center; gap:8px; cursor:pointer; }
  button.primary{
    background:var(--accent); color:#fff; border:none; border-radius:6px;
    padding:9px 16px; font-size:15px; cursor:pointer;
  }
  button.primary:hover{ background:var(--accent-dark); }
  .legend{ font-size:14px; color:var(--muted); }
  .badge{ display:inline-block; padding:2px 9px; border-radius:10px; font-size:13px; font-weight:600; white-space:nowrap; }
  .b-differs{ background:var(--red-bg); color:var(--red); }
  .b-match{ background:var(--green-bg); color:var(--green); }
  .b-noref{ background:var(--noref-bg); color:var(--muted); }
  .b-notfound{ background:var(--red-bg); color:var(--red); }
  table{ width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--line); border-radius:8px; overflow:hidden; }
  th, td{ text-align:left; padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top; font-size:15px; }
  th{ background:#eef3f7; font-size:13px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
  tr.prow{ cursor:pointer; }
  tr.prow:hover{ background:#f2f7fb; }
  tr.prow:focus{ outline:2px solid var(--accent); outline-offset:-2px; }
  td.num{ font-weight:700; white-space:nowrap; }
  td.pg{ white-space:nowrap; color:var(--muted); }
  td.first{ max-width:420px; }
  td.symcell{ white-space:nowrap; font-size:14px; }
  tr.xrow > td{ background:#fbfcfd; border-bottom:1px solid var(--line); padding:16px 16px 18px; }
  .panel{ display:flex; flex-wrap:wrap; gap:26px; }
  .pcol{ flex:1 1 340px; min-width:280px; }
  .pcol h4{ margin:0 0 8px; font-size:14px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }
  .verbatim{
    white-space:pre-wrap; font:14px/1.6 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    background:#fff; border:1px solid var(--line); border-radius:6px; padding:12px 14px; max-height:420px; overflow:auto;
  }
  blockquote{ margin:8px 0; padding:8px 12px; border-left:3px solid var(--accent); background:#fff; border-radius:0 6px 6px 0; }
  .cite{ font-size:13px; color:var(--muted); margin:8px 0 0; }
  details.removed{ margin:26px 0 0; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px 20px; }
  details.removed summary{ cursor:pointer; font-weight:600; color:var(--accent); }
  details.removed h4{ margin:16px 0 6px; font-size:14px; color:var(--muted); }
  details.removed ul{ margin:0; padding-left:20px; }
  details.removed li{ font-size:14px; margin:2px 0; word-break:break-word; }
  details.removed li .pg{ color:var(--muted); }
  .empty{ padding:30px; background:var(--card); border:1px solid var(--line); border-radius:8px; }
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<script>
(function(){
  "use strict";

  const D = window.WORKSHOP_DATA && window.WORKSHOP_DATA.pdf_text;
  const app = document.getElementById("app");
  if (!D || !D.records || !D.records.length) {
    app.innerHTML = '<p class="empty">No PDF text was found in WORKSHOP_DATA.pdf_text, so there is nothing to check.</p>';
    return;
  }

  const symbol  = D.symbol || "";
  const docUrl  = D.doc_url || "";
  const source  = D.source || "not stated in the file";
  const ref     = D.reference || {};
  const refParas = (typeof ref.paragraphs === "number") ? ref.paragraphs : null;
  const refNotes = (typeof ref.footnotes  === "number") ? ref.footnotes  : null;
  const refWords = ref.first_words || {};
  const pages = D.records.slice().sort((a, b) => (a.page || 0) - (b.page || 0));
  const pageCount = (typeof D.count === "number") ? D.count : pages.length;

  const esc = s => String(s).replace(/[&<>"']/g, c =>
    ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
  const symbolCell = docUrl
    ? '<a href="' + esc(docUrl) + '" target="_blank" rel="noopener">' + esc(symbol) + "</a>"
    : esc(symbol);

  /* ---------- Split the raw page text ---------- */

  const MONTH = /^(january|february|march|april|may|june|july|august|september|october|november|december)\b/i;
  const stream  = [];   // surviving lines: {page, text}
  const removed = [];   // lines taken out:  {page, text, kind}
  let footnoteStarts = 0;

  pages.forEach(rec => {
    const lines   = String(rec.text == null ? "" : rec.text).split(/\r?\n/);
    const n       = lines.length;
    const trimmed = lines.map(l => l.trim());
    const keep    = new Array(n).fill(true);

    // Pass 1 — page furniture: bare page numbers, the document symbol, "GE." distribution codes.
    for (let i = 0; i < n; i++) {
      const t = trimmed[i];
      if (!t) continue;
      const furniture =
        (symbol && t === symbol) ||
        /^GE\.\s?\d/.test(t) ||
        (/^\d{1,3}$/.test(t) && (i < 4 || i >= n - 4));
      if (furniture) { keep[i] = false; removed.push({ page: rec.page, text: t, kind: "furniture" }); }
    }

    // Pass 2 — footnotes at the foot of the page, scanned bottom-up.
    let idx = n - 1;
    while (idx >= 0 && (!keep[idx] || trimmed[idx] === "")) idx--;
    let inZone = false, buffer = [], sinceFn = 0;
    const flush = () => {
      buffer.forEach(b => { keep[b] = false; removed.push({ page: rec.page, text: trimmed[b], kind: "fncont" }); });
      buffer = [];
    };
    while (idx >= 0) {
      const t = trimmed[idx];
      if (t === "" || /^_+$/.test(t) || /^[-\u2013\u2014=]{3,}$/.test(t)) {
        if (inZone && sinceFn < 40) { idx--; continue; }
        break;
      }
      const isFnStart =
        /^(\d{1,2}|\*)\s+\S/.test(t) &&
        !/^\d{1,3}\./.test(t) &&
        !MONTH.test(t.replace(/^(\d{1,2}|\*)\s+/, ""));
      if (isFnStart) {
        flush();
        keep[idx] = false;
        removed.push({ page: rec.page, text: t, kind: "footnote" });
        footnoteStarts++;
        inZone = true; sinceFn = 0; idx--; continue;
      }
      if (inZone && sinceFn < 40) {
        if (/^\d{1,3}\.(?:\s|$)/.test(t)) break;        // a numbered paragraph starts: body begins
        if (/^[IVXLCDM]+\.\s/.test(t)) break;           // a section heading: body begins
        buffer.push(idx); sinceFn++; idx--; continue;   // possible wrapped footnote text
      }
      break;
    }

    for (let i = 0; i < n; i++) if (keep[i]) stream.push({ page: rec.page, text: lines[i] });
  });

  /* ---------- Find the numbered paragraphs ---------- */

  // Does the trimmed line begin with "n." as a paragraph number?
  // Returns the first text line of the paragraph ("" when the number stands alone), or null.
  function startMatch(t, n) {
    const s = String(n);
    if (t === s + ".") return "";
    let m = t.match(new RegExp("^" + s + "\\.\\s+([A-Z\u201C\u2018(].*)$"));
    if (m) return m[1];
    m = t.match(new RegExp("^" + s + "\\.([A-Z\u201C\u2018(].*)$")); // number glued to text (damage)
    if (m) return m[1];
    return null;
  }

  let expected = 1, current = null;
  const paras = [], preLines = [];
  for (const L of stream) {
    const t = L.text.trim();
    if (t !== "") {
      let sn = null, rest = null, r = startMatch(t, expected);
      if (r !== null) { sn = expected; rest = r; }
      else {
        // Resync: if the next expected number was damaged, accept expected+1..+3 so the
        // rest of the document still splits; the missed number shows up as a gap.
        for (let k = 1; k <= 3 && sn === null; k++) {
          r = startMatch(t, expected + k);
          if (r !== null) { sn = expected + k; rest = r; }
        }
      }
      if (sn !== null) {
        current = { num: sn, page: L.page, lines: rest ? [rest] : [] };
        paras.push(current);
        expected = sn + 1;
        continue;
      }
    }
    if (current) current.lines.push(L.text);
    else preLines.push(L);
  }

  function paraText(lines) {
    const a = lines.slice();
    while (a.length && a[0].trim() === "") a.shift();
    while (a.length && a[a.length - 1].trim() === "") a.pop();
    return a.join("\n");
  }

  // Compare the first six words, ignoring case, punctuation and spacing.
  function words(s) {
    return String(s).toLowerCase()
      .replace(/[\u2019']/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim().split(/\s+/).filter(Boolean);
  }

  const rows = [];
  const maxNum = Math.max(paras.length ? paras[paras.length - 1].num : 0, refParas || 0);
  const byNum = new Map(paras.map(p => [p.num, p]));
  for (let n = 1; n <= maxNum; n++) {
    const p = byNum.get(n);
    if (!p) { rows.push({ num: n, found: false }); continue; }
    const text = paraText(p.lines);
    const rw = refWords[String(n)];
    let check;
    if (rw === undefined) check = "noreference";
    else {
      const w = words(text).slice(0, 6);
      const r = words(rw).slice(0, 6);
      check = (w.length === r.length && w.every((x, i) => x === r[i])) ? "match" : "differs";
    }
    rows.push({ num: n, found: true, page: p.page, text, check, rw });
  }

  const foundCount   = paras.length;
  const differsCount = rows.filter(r => r.found && r.check === "differs").length;
  const norefCount   = rows.filter(r => r.found && r.check === "noreference").length;
  const gapCount     = rows.filter(r => !r.found).length;

  /* ---------- Render ---------- */

  function firstLine(text) {
    const l = text.split("\n").find(x => x.trim() !== "");
    if (!l) return "";
    const s = l.trim();
    return s.length > 90 ? s.slice(0, 90) + "\u2026" : s;
  }
  const BADGE = {
    differs:    '<span class="badge b-differs">Differs</span>',
    match:      '<span class="badge b-match">matches</span>',
    noreference:'<span class="badge b-noref">no reference</span>',
    notfound:   '<span class="badge b-notfound">not found</span>'
  };

  let openRows = new Set();
  let diffFirst = false;

  function panelHTML(r) {
    if (!r.found) {
      const rw = refWords[String(r.num)];
      return '<td colspan="5"><div class="panel"><div class="pcol">' +
        "<p>No line beginning \u201C" + r.num + ".\u201D was found in the raw page text. The number may be " +
        "missing, merged into another line, or otherwise damaged by the PDF conversion.</p>" +
        (rw !== undefined
          ? '<p>The reference file expects this paragraph to begin:</p><blockquote>\u201C' + esc(rw) + "\u201D</blockquote>"
          : "") +
        "</div></div></td>";
    }
    let refBlock;
    if (r.rw === undefined) {
      refBlock = "<p>The reference file has no entry for paragraph " + r.num +
        ", so this row is marked <span class=\"badge b-noref\">no reference</span>, not \u201CDiffers\u201D.</p>";
    } else {
      refBlock = "<p>First six words in the reference:</p><blockquote>\u201C" + esc(r.rw) + "\u201D</blockquote>";
      if (r.check === "differs") {
        refBlock += "<p><strong>Word-by-word comparison</strong> (lower-case, punctuation ignored):</p>" +
          "<p>Extracted: " + esc(words(r.text).slice(0, 6).join(" \u00B7 ")) + "</p>" +
          "<p>Reference: " + esc(words(r.rw).slice(0, 6).join(" \u00B7 ")) + "</p>";
      }
    }
    return '<td colspan="5"><div class="panel">' +
      '<div class="pcol"><h4>Full paragraph \u2014 exactly as extracted, unedited</h4>' +
      '<div class="verbatim">' + esc(r.text) + "</div>" +
      '<p class="cite">Starts on page ' + r.page + " of the raw PDF text, at the line \u201C" + r.num +
      ".\u201D Lettered sub-paragraphs are part of this paragraph.</p></div>" +
      '<div class="pcol"><h4>Reference check</h4>' + refBlock + "</div>" +
      "</div></td>";
  }

  function renderTable() {
    const ordered = rows.slice().sort((a, b) => {
      if (diffFirst) {
        const ra = !a.found || a.check !== "match" ? 0 : 1;
        const rb = !b.found || b.check !== "match" ? 0 : 1;
        if (ra !== rb) return ra - rb;
      }
      return a.num - b.num;
    });
    const body = ordered.map(r => {
      const badge = r.found ? BADGE[r.check] : BADGE.notfound;
      const hidden = openRows.has(r.num) ? "" : " hidden";
      return '<tr class="prow" data-num="' + r.num + '" tabindex="0" aria-expanded="' + openRows.has(r.num) + '">' +
        '<td class="num">' + r.num + "</td>" +
        '<td class="pg">' + (r.found ? "p." + r.page : "\u2014") + "</td>" +
        '<td class="first">' + (r.found ? esc(firstLine(r.text)) : "<em>not found in the raw page text</em>") + "</td>" +
        "<td>" + badge + "</td>" +
        '<td class="symcell">' + symbolCell + "</td>" +
        "</tr>" +
        '<tr class="xrow" data-num="' + r.num + '"' + hidden + ">" + panelHTML(r) + "</tr>";
    }).join("");
    document.getElementById("tbody").innerHTML = body;
  }

  function renderRemoved() {
    const groups = [
      { kind: "furniture", h: "Page furniture \u2014 page numbers, the document symbol and \u201CGE.\u201D distribution codes" },
      { kind: "footnote",  h: "Footnote lines \u2014 a small number (or *) then text, at the foot of a page. Removed and counted." },
      { kind: "fncont",    h: "Wrapped continuation lines of those footnotes (removed with them)" }
    ];
    let html = "<p class=\"how\">Nothing was discarded silently: every line the code took out of the paragraph " +
      "text is listed below, with the page it came from, exactly as extracted.</p>";
    groups.forEach(g => {
      const items = removed.filter(x => x.kind === g.kind);
      html += "<h4>" + esc(g.h) + " \u2014 " + items.length + " line" + (items.length === 1 ? "" : "s") + "</h4>";
      html += items.length
        ? "<ul>" + items.map(x =>
            '<li><span class="pg">p.' + x.page + ":</span> \u201C" + esc(x.text) + "\u201D</li>").join("") + "</ul>"
        : "<ul><li>none</li></ul>";
    });
    const pre = preLines.filter(l => l.text.trim() !== "");
    html += "<h4>Lines before paragraph 1 (title page and headings \u2014 not part of any numbered paragraph, " +
      "listed here so you can check that nothing substantive was lost) \u2014 " + pre.length + " line" +
      (pre.length === 1 ? "" : "s") + "</h4>";
    html += pre.length
      ? "<ul>" + pre.map(l => '<li><span class="pg">p.' + l.page + ":</span> \u201C" + esc(l.text.trim()) + "\u201D</li>").join("") + "</ul>"
      : "<ul><li>none</li></ul>";
    document.getElementById("removedBody").innerHTML = html;
  }

  const ofRef = v => (v === null ? "of \u2014" : "of " + v);
  app.innerHTML =
    '<p class="kicker">Paragraph-level verification tool</p>' +
    "<h1>" + esc(D.title || "UN document") + "</h1>" +
    '<p class="sub">Raw PDF text, ' + pageCount + " page" + (pageCount === 1 ? "" : "s") +
    " \u00B7 source: " + esc(source) + " \u00B7 " + symbolCell + "</p>" +

    '<div class="stats">' +
      '<div class="stat"><div class="big">' + foundCount + '<span class="of">' + ofRef(refParas) + "</span></div>" +
      '<div class="lab">Paragraphs found' + (gapCount ? " (" + gapCount + " expected number" + (gapCount === 1 ? "" : "s") + " not found)" : "") + "</div></div>" +
      '<div class="stat"><div class="big">' + footnoteStarts + '<span class="of">' + ofRef(refNotes) + "</span></div>" +
      '<div class="lab">Footnote lines removed</div></div>' +
      '<div class="stat"><div class="big">' + differsCount + (norefCount ? '<span class="of">+ ' + norefCount + " no reference</span>" : "") + "</div>" +
      '<div class="lab">Paragraphs whose opening words differ' + (norefCount ? " (a further " + norefCount + " have no reference entry)" : "") + "</div></div>" +
    "</div>" +
    '<p class="how">Found by the code from the page text; reference figures come from the file. A paragraph starts at a ' +
      "line beginning with the next expected number and a full stop, and runs to the next start; lettered " +
      "sub-paragraphs stay inside their paragraph. \u201CDiffers\u201D compares the first six words with the reference, " +
      "ignoring case, punctuation and extra spaces. When a number in sequence is missing, the code resumes at the " +
      "next recognisable number and the missing paragraph is shown as \u201Cnot found\u201D.</p>" +

    '<div class="toolbar">' +
      '<label><input type="checkbox" id="diffFirst"> Show differences first</label>' +
      '<button class="primary" id="csvBtn">Download CSV</button>' +
      '<span class="legend">' + BADGE.differs + " " + BADGE.match + " " + BADGE.noref + " " + BADGE.notfound + "</span>" +
    "</div>" +
    "<table><thead><tr>" +
      "<th scope=\"col\">Para.</th><th scope=\"col\">Page</th><th scope=\"col\">First line</th>" +
      "<th scope=\"col\">Check</th><th scope=\"col\">Symbol</th>" +
    '</tr></thead><tbody id="tbody"></tbody></table>' +
    '<p class="how">How this is computed: click any row to see the full paragraph exactly as extracted, with the ' +
      "reference's first words beside it. Numbers in the table run 1, 2, 3 \u2026; rows marked \u201Cnot found\u201D are " +
      "numbers the code could not find in the page text.</p>" +
    '<details class="removed" id="removedBox"><summary>Lines removed as headers, footers and footnotes (' +
    removed.length + ')</summary><div id="removedBody"></div></details>';

  renderTable();
  renderRemoved();

  const tbody = document.getElementById("tbody");
  function toggle(tr) {
    const xr = tr.nextElementSibling;
    if (!xr || !xr.classList.contains("xrow")) return;
    const num = Number(tr.getAttribute("data-num"));
    const willOpen = xr.hasAttribute("hidden");
    if (willOpen) { xr.removeAttribute("hidden"); openRows.add(num); }
    else { xr.setAttribute("hidden", ""); openRows.delete(num); }
    tr.setAttribute("aria-expanded", willOpen ? "true" : "false");
  }
  tbody.addEventListener("click", e => {
    const tr = e.target.closest("tr.prow");
    if (tr) toggle(tr);
  });
  tbody.addEventListener("keydown", e => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const tr = e.target.closest("tr.prow");
    if (tr) { e.preventDefault(); toggle(tr); }
  });
  document.getElementById("diffFirst").addEventListener("change", e => {
    diffFirst = e.target.checked;
    renderTable();
  });

  /* ---------- CSV ---------- */

  document.getElementById("csvBtn").addEventListener("click", () => {
    const q = v => '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"';
    const CHECK = { match: "matches", differs: "differs", noreference: "no reference" };
    let csv = "\uFEFFparagraph,page,check,reference_first_words,text\n";
    rows.forEach(r => {
      csv += [
        r.num,
        r.found ? r.page : "",
        r.found ? CHECK[r.check] : "not found",
        r.found && r.rw !== undefined ? r.rw : "",
        r.found ? r.text : ""
      ].map(q).join(",") + "\n";
    });
    const name = (symbol || "document").replace(/[^\w.-]+/g, "_") + "-paragraph-check.csv";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  });
})();
</script>
</body>
</html>
```

The app joins the 20 pages in order, strips page furniture and footnotes (each removed line stays visible in the collapsible list), splits the text at each "N." in sequence, and checks every paragraph's first six words against the reference. Gaps where a number was never found appear as "not found" rows, and the CSV carries the full verbatim text of every row.