Here's the research wiki: a sidebar of the eight concepts with live passage counts plus an "Add a concept" box, and a main page per concept with the kind-of-document table, passages grouped by document (each citation opens the PDF at its page via `studio.openSource`), related concepts, and an AI summary button that sends at most 12 passages.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neurotechnology &amp; justice — research wiki</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #f4f6f9; color: #17202a;
  }
  header { background: #fff; border-bottom: 1px solid #dde3ea; padding: 20px 28px; }
  header h1 { margin: 0 0 6px; font-size: 24px; color: #1f6fb2; }
  .desc { margin: 0; color: #4a5568; max-width: 75em; }
  .layout { display: flex; gap: 24px; align-items: flex-start; padding: 24px 28px; max-width: 1240px; }
  aside { flex: 0 0 260px; width: 260px; background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 16px; position: sticky; top: 16px; }
  aside h2 { margin: 0 0 10px; font-size: 14px; text-transform: uppercase; letter-spacing: .06em; color: #4a5568; }
  #conceptList { list-style: none; margin: 0 0 16px; padding: 0; }
  .concept { display: flex; justify-content: space-between; align-items: center; gap: 8px; width: 100%; padding: 7px 10px; border: 0; border-radius: 6px; background: transparent; color: #17202a; cursor: pointer; text-align: left; font: inherit; }
  .concept:hover { background: #eaf2fa; }
  .concept.active { background: #1f6fb2; color: #fff; }
  .ccount { background: #e3ecf5; color: #17202a; border-radius: 999px; padding: 1px 9px; font-size: 13px; white-space: nowrap; }
  .concept.active .ccount { background: rgba(255,255,255,.28); color: #fff; }
  .side-note { font-size: 13px; color: #5a6b7d; margin: 10px 0 0; }
  #addForm label { display: block; font-size: 14px; font-weight: 600; margin-bottom: 6px; }
  #addInput { width: 100%; padding: 8px 10px; border: 1px solid #c3cedb; border-radius: 6px; font: inherit; }
  #addInput:focus { outline: 2px solid #1f6fb2; outline-offset: 1px; }
  main { flex: 1; min-width: 0; }
  .pagetitle { margin: 0 0 4px; font-size: 24px; }
  .terms { margin: 0 0 10px; color: #4a5568; }
  .panel { background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 18px 22px; margin: 0 0 20px; }
  .paneltitle { margin: 0 0 12px; font-size: 19px; color: #1f6fb2; }
  .note { font-size: 13.5px; color: #4a5568; background: #eef4fa; border-left: 3px solid #1f6fb2; padding: 8px 12px; border-radius: 0 6px 6px 0; margin: 12px 0 0; }
  table { border-collapse: collapse; width: 100%; }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid #e4e9f0; }
  th { color: #4a5568; font-weight: 600; }
  th.num, td.num { text-align: right; }
  tr.total td { font-weight: 700; border-top: 2px solid #1f6fb2; border-bottom: 0; }
  .docgroup { border: 1px solid #dde3ea; border-radius: 8px; margin: 0 0 14px; overflow: hidden; }
  .dochead { background: #eef4fa; padding: 10px 16px; display: flex; flex-wrap: wrap; gap: 4px 14px; align-items: baseline; }
  .dochead .t { font-weight: 700; }
  .dochead .k, .dochead .y { color: #4a5568; font-size: 14px; }
  .dochead a.sym { color: #1f6fb2; font-weight: 600; text-decoration: none; }
  .dochead a.sym:hover { text-decoration: underline; }
  .dochead .sym { font-weight: 600; }
  .passage { padding: 12px 16px; border-top: 1px solid #e4e9f0; }
  .pmeta { display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: baseline; margin-bottom: 2px; }
  a.cite { color: #1f6fb2; font-weight: 600; text-decoration: none; }
  a.cite:hover { text-decoration: underline; }
  .sec { font-size: 13.5px; color: #5a6b7d; font-style: italic; }
  .ptext { margin: 4px 0 6px; white-space: pre-wrap; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden; }
  .ptext.open { display: block; -webkit-line-clamp: unset; }
  .foldbtn { background: none; border: 1px solid #1f6fb2; color: #1f6fb2; border-radius: 6px; padding: 3px 10px; font-size: 13px; cursor: pointer; }
  .foldbtn:hover { background: #eaf2fa; }
  .rellinks a { display: inline-block; margin: 0 8px 8px 0; padding: 5px 12px; background: #eef4fa; border-radius: 999px; color: #1f6fb2; text-decoration: none; }
  .rellinks a:hover { background: #dce9f6; }
  .btn { background: #1f6fb2; color: #fff; border: 0; border-radius: 6px; padding: 9px 16px; font: inherit; font-size: 15px; cursor: pointer; }
  .btn:hover { background: #185a94; }
  .btn:disabled { opacity: .55; cursor: default; }
  .status { color: #4a5568; font-size: 14px; margin: 10px 0 0; }
  .sumout { margin-top: 12px; }
  .ailabel { font-weight: 700; color: #1f6fb2; font-size: 14px; margin: 0 0 8px; }
  .aibox { border: 1px solid #1f6fb2; background: #f7fbff; border-radius: 8px; padding: 12px 16px; }
  .aibox p { margin: 0 0 8px; }
  .aibox p:last-child { margin-bottom: 0; }
  .empty { background: #fff; border: 1px solid #dde3ea; border-radius: 8px; padding: 18px 22px; color: #4a5568; }
  @media (max-width: 880px) {
    .layout { flex-direction: column; }
    aside { position: static; width: 100%; flex: none; }
  }
</style>
</head>
<body>
<header>
  <h1>Neurotechnology and the administration of justice — research wiki</h1>
  <p class="desc" id="desc"></p>
</header>
<div class="layout">
  <aside>
    <h2>Concepts</h2>
    <ul id="conceptList"></ul>
    <form id="addForm">
      <label for="addInput">Add a concept</label>
      <input id="addInput" type="text" placeholder="type a term, press Enter" autocomplete="off">
    </form>
    <p class="side-note">Counts: passages whose full text contains the concept's term(s), ignoring case and line breaks. Added concepts last only until reload.</p>
  </aside>
  <main id="main"></main>
</div>

<script>
(function () {
  "use strict";

  var LIB = (window.WORKSHOP_DATA && window.WORKSHOP_DATA.library) ? window.WORKSHOP_DATA.library : { records: [] };
  var docs = LIB.records || [];

  var BASE = [
    { name: "Mental privacy",     terms: ["mental privacy"] },
    { name: "Freedom of thought", terms: ["freedom of thought"] },
    { name: "Self-incrimination", terms: ["self-incrimination"] },
    { name: "Lie detection",      terms: ["lie detection", "deception detection", "brain fingerprinting"] },
    { name: "Consent",            terms: ["consent"] },
    { name: "Neural data",        terms: ["neural data"] },
    { name: "Data solidarity",    terms: ["data solidarity"] },
    { name: "Proportionality",    terms: ["proportionality"] }
  ];
  var concepts = BASE.map(function (c) { return { name: c.name, terms: c.terms.slice() }; });
  var current = concepts[0].name;
  var drafting = false;

  /* ---------- helpers ---------- */

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined && text !== null) e.textContent = String(text);
    return e;
  }
  function norm(s) { return (s || "").toLowerCase().replace(/\s+/g, " ").trim(); }
  function matches(text, terms) {
    var t = norm(text);
    for (var i = 0; i < terms.length; i++) if (t.indexOf(norm(terms[i])) !== -1) return true;
    return false;
  }
  function passagesFor(concept) {
    var out = [];
    docs.forEach(function (d) {
      (d.passages || []).forEach(function (p) {
        if (matches(p.text, concept.terms)) out.push({ doc: d, p: p });
      });
    });
    return out;
  }
  function surname(n) { var parts = (n || "").trim().split(/\s+/); return parts[parts.length - 1] || n; }
  function citeAuthor(doc) {
    if (doc.kind === "Journal article") {
      var names = (doc.author || "").split(/\s+and\s+|,|;/)
        .map(function (s) { return s.trim(); })
        .filter(function (s) { return s && !/^(et al\.?|others?)$/i.test(s); });
      if (names.length >= 3) return surname(names[0]) + " et al.";
      if (names.length === 2) return surname(names[0]) + " & " + surname(names[1]);
      if (names.length === 1) return surname(names[0]);
    }
    return doc.author || "";
  }
  function citation(doc, p) {
    if (p.paragraph !== null && p.paragraph !== undefined && p.paragraph !== "" && doc.symbol) {
      return doc.symbol + ", para. " + p.paragraph;
    }
    return citeAuthor(doc) + " " + (doc.year || "") + ", p. " + (p.page_label || p.page);
  }
  function plural(n, word) { return n + " " + word + (n === 1 ? "" : "s"); }

  /* ---------- sidebar ---------- */

  function renderSidebar() {
    var ul = document.getElementById("conceptList");
    ul.innerHTML = "";
    concepts.forEach(function (c) {
      var li = document.createElement("li");
      var b = el("button", "concept" + (c.name === current ? " active" : ""));
      b.appendChild(el("span", "cname", c.name));
      b.appendChild(el("span", "ccount", String(passagesFor(c).length)));
      b.addEventListener("click", function () { select(c.name); });
      li.appendChild(b);
      ul.appendChild(li);
    });
  }

  function select(name) {
    current = name;
    try { history.replaceState(null, "", "#" + encodeURIComponent(name)); } catch (e) {}
    renderSidebar();
    renderMain();
  }

  /* ---------- main page ---------- */

  function renderMain() {
    var concept = concepts.filter(function (c) { return c.name === current; })[0] || concepts[0];
    current = concept.name;
    var main = document.getElementById("main");
    main.innerHTML = "";
    var items = passagesFor(concept);

    main.appendChild(el("h2", "pagetitle", concept.name));
    main.appendChild(el("p", "terms",
      "Found by the terms: " + concept.terms.map(function (t) { return "\u201C" + t + "\u201D"; }).join(", ")));
    var docsHit = {};
    items.forEach(function (it) { docsHit[it.doc.id] = true; });
    var nDocs = Object.keys(docsHit).length;
    main.appendChild(el("p", "note",
      "How this is computed: a passage is listed when its full text contains one of the terms above, ignoring case and line breaks (substring match, so \u201Cconsent\u201D also finds \u201Cconsented\u201D). n = " +
      plural(items.length, "passage") + " in " + plural(nDocs, "document") + "."));

    if (!items.length) {
      main.appendChild(el("p", "empty", "No passage uses this term."));
      return;
    }

    /* table: passages by kind of document */
    var panel = el("section", "panel");
    panel.appendChild(el("h3", "paneltitle", "Passages by kind of document"));
    var kindCount = {};
    items.forEach(function (it) { var k = it.doc.kind || "Other"; kindCount[k] = (kindCount[k] || 0) + 1; });
    var rows = Object.keys(kindCount).map(function (k) { return [k, kindCount[k]]; })
      .sort(function (a, b) { return b[1] - a[1] || a[0].localeCompare(b[0]); });
    var table = el("table");
    var thead = el("thead"); var htr = el("tr");
    htr.appendChild(el("th", null, "Kind of document")); htr.appendChild(el("th", "num", "Passages"));
    thead.appendChild(htr); table.appendChild(thead);
    var tbody = el("tbody");
    rows.forEach(function (r) {
      var tr = el("tr");
      tr.appendChild(el("td", null, r[0]));
      tr.appendChild(el("td", "num", String(r[1])));
      tbody.appendChild(tr);
    });
    var ttr = el("tr", "total");
    ttr.appendChild(el("td", null, "Total"));
    ttr.appendChild(el("td", "num", String(items.length)));
    tbody.appendChild(ttr); table.appendChild(tbody);
    panel.appendChild(table);
    panel.appendChild(el("p", "note", "Each passage is counted once, under the kind of its document. Rows are the kinds that have at least one passage for this concept."));
    main.appendChild(panel);

    /* passages grouped by document, in library order */
    var gwrap = el("section", "panel");
    gwrap.appendChild(el("h3", "paneltitle", "Passages, grouped by document"));
    docs.forEach(function (d) {
      var ps = (d.passages || []).filter(function (p) { return matches(p.text, concept.terms); });
      if (!ps.length) return;
      var g = el("div", "docgroup");
      var head = el("div", "dochead");
      head.appendChild(el("span", "t", d.short_title || d.title || d.id));
      head.appendChild(el("span", "k", d.kind || ""));
      head.appendChild(el("span", "y", String(d.year || "")));
      if (d.symbol) {
        var a = el("a", "sym", d.symbol);
        a.href = d.url || "#"; a.target = "_blank"; a.rel = "noopener";
        head.appendChild(a);
      } else {
        head.appendChild(el("span", "sym", d.author || ""));
      }
      head.appendChild(el("span", "k", plural(ps.length, "passage")));
      g.appendChild(head);
      ps.forEach(function (p) {
        var row = el("div", "passage");
        var meta = el("div", "pmeta");
        var cite = el("a", "cite", citation(d, p));
        cite.href = "#";
        cite.title = "Open the PDF at the page where this paragraph starts";
        cite.addEventListener("click", function (ev) {
          ev.preventDefault();
          if (typeof studio !== "undefined" && studio.openSource) {
            try { studio.openSource(d.id, p.page); } catch (e) {}
          }
        });
        meta.appendChild(cite);
        if (p.section) meta.appendChild(el("span", "sec", p.section));
        row.appendChild(meta);
        var t = el("p", "ptext", p.text);
        row.appendChild(t);
        var b = el("button", "foldbtn", "Show full text");
        b.addEventListener("click", function () {
          var open = t.classList.toggle("open");
          b.textContent = open ? "Fold" : "Show full text";
        });
        row.appendChild(b);
        g.appendChild(row);
      });
      gwrap.appendChild(g);
    });
    main.appendChild(gwrap);

    /* related concepts */
    var rel = el("section", "panel");
    rel.appendChild(el("h3", "paneltitle", "Related concepts"));
    var relWrap = el("div", "rellinks");
    var any = false;
    concepts.forEach(function (c) {
      if (c.name === concept.name) return;
      var n = items.filter(function (it) { return matches(it.p.text, c.terms); }).length;
      if (n > 0) {
        any = true;
        var a = el("a", null, c.name + " (" + n + ")");
        a.href = "#" + encodeURIComponent(c.name);
        a.addEventListener("click", function (ev) { ev.preventDefault(); select(c.name); });
        relWrap.appendChild(a);
      }
    });
    if (!any) relWrap.appendChild(el("span", null, "No other concept appears in these passages."));
    rel.appendChild(relWrap);
    rel.appendChild(el("p", "note", "A concept is related when at least one of the passages above also contains its term(s)."));
    main.appendChild(rel);

    /* draft a summary */
    var sum = el("section", "panel");
    sum.appendChild(el("h3", "paneltitle", "Draft a summary"));
    var btn = el("button", "btn", "Draft a summary");
    var status = el("p", "status", "");
    var out = el("div", "sumout");
    btn.addEventListener("click", function () { onDraft(btn, status, out, concept, items); });
    sum.appendChild(btn);
    sum.appendChild(status);
    sum.appendChild(out);
    sum.appendChild(el("p", "note",
      "At most the first 12 passages on this page are sent, with their citations, to a language model; the model may only use what it is sent. Nothing is sent when the page loads."));
    main.appendChild(sum);
  }

  /* ---------- AI summary ---------- */

  function onDraft(btn, status, out, concept, items) {
    if (drafting) return;
    var n = Math.min(12, items.length);
    var sent = items.slice(0, n);
    status.textContent = "Sending " + plural(n, "passage") + " to the model \u2014 they leave the browser\u2026";
    btn.disabled = true; drafting = true;
    var lines = sent.map(function (it, i) {
      return (i + 1) + ". " + citation(it.doc, it.p) + "\n" + it.p.text;
    }).join("\n\n");
    var prompt = [
      "You are assisting human rights professionals (diplomats, NGO, NHRI and UN staff).",
      "Below are " + n + " verbatim passages from documents about neurotechnology and the administration of justice, each with its citation.",
      "",
      "Task: write exactly three sentences that summarise what these passages say about \u201C" + concept.name + "\u201D.",
      "Each sentence must end with the citation of the passage it rests on, in parentheses. Use only the passages below; do not invent anything.",
      "",
      "Passages:",
      lines
    ].join("\n");
    function done() { btn.disabled = false; drafting = false; }
    if (typeof studio === "undefined" || !studio.ask) {
      status.textContent = "The model is not available in this session.";
      done(); return;
    }
    studio.ask(prompt).then(function (ans) {
      status.textContent = "";
      out.innerHTML = "";
      out.appendChild(el("p", "ailabel",
        "Written by AI. " + plural(n, "passage") + " were sent to the model and left the browser."));
      var box = el("div", "aibox");
      box.setAttribute("data-source", "ai");
      String(ans || "").split(/\n+/).map(function (s) { return s.trim(); })
        .filter(Boolean).forEach(function (s) { box.appendChild(el("p", null, s)); });
      out.appendChild(box);
      done();
    }).catch(function (err) {
      status.textContent = "The model could not be reached: " + ((err && err.message) || err);
      done();
    });
  }

  /* ---------- add a concept ---------- */

  document.getElementById("addForm").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var inp = document.getElementById("addInput");
    var term = inp.value.trim();
    if (!term) return;
    var exists = concepts.filter(function (c) { return c.name.toLowerCase() === term.toLowerCase(); })[0];
    if (exists) select(exists.name);
    else { concepts.push({ name: term, terms: [term] }); select(term); }
    inp.value = "";
  });

  /* ---------- init ---------- */

  var totalP = docs.reduce(function (s, d) { return s + (d.passages || []).length; }, 0);
  var years = docs.map(function (d) { return d.year; }).filter(function (y) { return y !== null && y !== undefined; });
  var yr = years.length ? Math.min.apply(null, years) + "\u2013" + Math.max.apply(null, years) : "";
  document.getElementById("desc").textContent =
    (LIB.title || "Research library") + (LIB.source ? " \u2014 " + LIB.source : "") + ". " +
    docs.length + " documents, " + totalP + " passages" + (yr ? ", " + yr : "") + ".";

  var hash = "";
  try { hash = decodeURIComponent((location.hash || "").replace(/^#/, "")); } catch (e) {}
  if (hash && concepts.some(function (c) { return c.name === hash; })) current = hash;

  renderSidebar();
  renderMain();
})();
</script>
</body>
</html>
```