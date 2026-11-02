Here's the research wiki: a sidebar of eight concept pages (plus ones you add), a passages-by-kind table, passages grouped by document with citations that open the PDF at the right page, related concepts, and an on-demand AI summary. Matching is case-insensitive and ignores line breaks, and passage text is always shown verbatim.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Neurotechnology &amp; Justice — Concept Wiki</title>
<style>
  :root { --accent: #1f6fb2; }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    font-size: 16px; line-height: 1.5; background: #f7f9fb; color: #1c2733;
  }
  header.app {
    background: #fff; border-bottom: 1px solid #dfe6ee; padding: 20px 28px;
  }
  header.app h1 { margin: 0 0 4px; font-size: 22px; color: var(--accent); }
  header.app p { margin: 0; color: #4a5a6a; font-size: 14px; }
  .layout { display: flex; min-height: calc(100vh - 90px); }
  nav.sidebar {
    width: 250px; flex-shrink: 0; background: #fff; border-right: 1px solid #dfe6ee;
    padding: 16px; }
  nav.sidebar h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .05em;
    color: #6b7b8c; margin: 0 0 8px; }
  nav.sidebar ul { list-style: none; margin: 0 0 20px; padding: 0; }
  nav.sidebar li { margin: 2px 0; }
  nav.sidebar a.concept {
    display: flex; justify-content: space-between; text-decoration: none; color: #1c2733;
    padding: 5px 8px; border-radius: 4px; font-size: 15px;
  }
  nav.sidebar a.concept:hover { background: #eef4fa; }
  nav.sidebar a.concept.active { background: var(--accent); color: #fff; }
  nav.sidebar a.concept .count { color: #6b7b8c; font-size: 13px; }
  nav.sidebar a.concept.active .count { color: #d5e6f5; }
  .add-concept { display: flex; gap: 6px; }
  .add-concept input {
    flex: 1; font-size: 15px; padding: 6px 8px; border: 1px solid #c6d2de;
    border-radius: 4px; }
  .add-concept button {
    font-size: 14px; padding: 6px 10px; border: none; border-radius: 4px;
    background: var(--accent); color: #fff; cursor: pointer;
  }
  main { flex: 1; padding: 24px 32px; max-width: 900px; }
  h2.page-title { margin: 0 0 4px; font-size: 24px; color: #14202c; }
  p.terms { margin: 0 0 20px; color: #4a5a6a; font-size: 14px; }
  p.terms code { background: #eef2f6; padding: 1px 6px; border-radius: 3px; font-size: 13px; }
  table.kinds { border-collapse: collapse; background: #fff; margin: 0 0 8px;
    border: 1px solid #dfe6ee; border-radius: 6px; overflow: hidden; width: 100%; }
  table.kinds th, table.kinds td { text-align: left; padding: 7px 14px;
    border-bottom: 1px solid #e6edf3; font-size: 15px; }
  table.kinds th { background: #eef4fa; color: #33506b; font-weight: 600; }
  table.kinds tr.total td { font-weight: 600; background: #f4f8fc; }
  .how { font-size: 13px; color: #6b7b8c; margin: 0 0 28px; }
  section.doc { background: #fff; border: 1px solid #dfe6ee; border-radius: 6px;
    margin-bottom: 20px; overflow: hidden; }
  .doc-head { padding: 12px 18px; background: #f4f8fc; border-bottom: 1px solid #e6edf3;
    font-size: 15px; }
  .doc-head a { color: var(--accent); text-decoration: none; font-weight: 600; }
  .doc-head .meta { color: #4a5a6a; font-weight: 400; margin-left: 8px; font-size: 14px; }
  .passage { padding: 12px 18px; border-bottom: 1px solid #eef2f6; }
  .passage:last-child { border-bottom: none; }
  .passage .cite-row { display: flex; justify-content: space-between; align-items: baseline;
    gap: 12px; flex-wrap: wrap; }
  .passage cite {
    font-style: normal; font-weight: 600; color: var(--accent); cursor: pointer;
    font-size: 15px; text-decoration: underline; text-decoration-color: #b9d2e8; }
  .passage cite:hover { text-decoration-color: var(--accent); }
  .passage .section-name { font-size: 13px; color: #6b7b8c; }
  .passage p { margin: 6px 0 0; font-size: 15px; color: #26313d; }
  .passage p.folded {
    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
    overflow: hidden; }
  .passage .more {
    display: inline-block; margin-top: 4px; font-size: 13px; color: var(--accent);
    background: none; border: none; cursor: pointer; padding: 0; text-decoration: underline;
    text-decoration-color: #b9d2e8; }
  .related { margin: 26px 0; }
  .related h3 { font-size: 16px; margin: 0 0 8px; }
  .related a {
    display: inline-block; margin: 0 10px 8px 0; padding: 4px 12px; border-radius: 14px;
    background: #eef4fa; color: var(--accent); text-decoration: none; font-size: 14px;
  }
  .related a:hover { background: #dcebfa; }
  .ai-box { margin: 26px 0; }
  .ai-box h3 { font-size: 16px; margin: 0 0 8px; }
  .ai-label { font-size: 13px; color: #8a5a00; background: #fdf3e0; padding: 4px 10px;
    border-radius: 4px; display: inline-block; margin-bottom: 8px; }
  .ai-output { background: #fff; border: 1px solid #e0c88a; border-radius: 6px;
    padding: 14px 18px; font-size: 15px; }
  button.draft {
    font-size: 15px; padding: 9px 18px; border: none; border-radius: 5px;
    background: var(--accent); color: #fff; cursor: pointer; margin: 26px 0 0;
  }
  button.draft:disabled { background: #9bb4c9; cursor: wait; }
  .empty { background: #fff; border: 1px dashed #c6d2de; border-radius: 6px;
    padding: 22px 26px; color: #4a5a6a; }
</style>
</head>
<body>
<header class="app">
  <h1>Neurotechnology &amp; the Administration of Justice — Concept Wiki</h1>
  <p id="src-line"></p>
</header>
<div class="layout">
  <nav class="sidebar">
    <h2>Concepts</h2>
    <ul id="concept-list"></ul>
    <h2>Add a concept</h2>
    <div class="add-concept">
      <input id="new-concept" type="text" placeholder="Type a term, press Enter" aria-label="New concept">
      <button id="add-btn" type="button">Add</button>
    </div>
  </nav>
  <main id="main"></main>
</div>

<script>
(function () {
  var lib = WORKSHOP_DATA.library;
  var docs = lib.records || [];

  var BASE_CONCEPTS = [
    { name: "Mental privacy", terms: ["mental privacy"] },
    { name: "Freedom of thought", terms: ["freedom of thought"] },
    { name: "Self-incrimination", terms: ["self-incrimination"] },
    { name: "Lie detection", terms: ["lie detection", "deception detection", "brain fingerprinting"] },
    { name: "Consent", terms: ["consent"] },
    { name: "Neural data", terms: ["neural data"] },
    { name: "Data solidarity", terms: ["data solidarity"] },
    { name: "Proportionality", terms: ["proportionality"] }
  ];
  var concepts = BASE_CONCEPTS.slice();

  var state = { current: "Mental privacy" };

  // ---- helpers ----------------------------------------------------------

  function norm(s) { return (s || "").replace(/\s+/g, " "); }

  function passageMatches(passage, terms) {
    var t = norm(passage.text).toLowerCase();
    for (var i = 0; i < terms.length; i++) {
      if (t.indexOf(terms[i].toLowerCase()) !== -1) return true;
    }
    return false;
  }

  function findPassages(concept) {
    var out = [];
    docs.forEach(function (doc) {
      (doc.passages || []).forEach(function (pass) {
        if (passageMatches(pass, concept.terms)) out.push({ doc: doc, pass: pass });
      });
    });
    return out;
  }

  function conceptCount(concept) { return findPassages(concept).length; }

  // Citation label for a document (used when passage has no paragraph).
  function authorCitation(doc) {
    if (doc.kind !== "Journal article" || !doc.author) return doc.author + " " + doc.year;
    var names = doc.author.split(/\s+(?:and|&)\s+/i).filter(Boolean);
    var surnames = names.map(function (n) {
      var parts = n.trim().split(/\s+/);
      return parts[parts.length - 1].replace(/,.*/, "");
    });
    if (surnames.length >= 3) return surnames[0] + " et al. " + doc.year;
    if (surnames.length === 2) return surnames[0] + " & " + surnames[1] + " " + doc.year;
    return surnames[0] + " " + doc.year;
  }

  function passageCitation(doc, pass) {
    if (doc.symbol && pass.paragraph) return doc.symbol + ", para. " + pass.paragraph;
    if (doc.symbol) return doc.symbol;
    return authorCitation(doc) + ", p. " + pass.page_label;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function getConcept(name) {
    for (var i = 0; i < concepts.length; i++) {
      if (concepts[i].name.toLowerCase() === name.toLowerCase()) return concepts[i];
    }
    return null;
  }

  // ---- rendering --------------------------------------------------------

  function renderSidebar() {
    var ul = document.getElementById("concept-list");
    ul.innerHTML = "";
    concepts.forEach(function (c) {
      var n = conceptCount(c);
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.className = "concept" + (c.name === state.current ? " active" : "");
      a.href = "#";
      a.innerHTML = "<span>" + esc(c.name) + "</span><span class='count'>" + n + "</span>";
      a.onclick = function (e) { e.preventDefault(); state.current = c.name; render(); };
      li.appendChild(a);
      ul.appendChild(li);
    });
  }

  function renderKindTable(matched) {
    var kinds = [];
    var byKind = {};
    docs.forEach(function (d) {
      if (byKind[d.kind] === undefined) { byKind[d.kind] = 0; kinds.push(d.kind); }
    });
    matched.forEach(function (m) { byKind[m.doc.kind]++; });
    var total = matched.length;
    var html = "<table class='kinds'><thead><tr><th>Kind of document</th><th>Passages</th></tr></thead><tbody>";
    kinds.forEach(function (k) {
      html += "<tr><td>" + esc(k) + "</td><td>" + byKind[k] + "</td></tr>";
    });
    html += "<tr class='total'><td>Total</td><td>" + total + "</td></tr>";
    html += "</tbody></table>";
    html += "<p class='how'>How this is computed: each row counts passages whose text contains one of the concept's terms " +
            "(case-insensitive, line breaks ignored), grouped by document kind. Documents with no matching passages still appear with a count of zero.</p>";
    return html;
  }

  function renderPassages(matched) {
    var html = "";
    var groups = [];
    var byDoc = {};
    matched.forEach(function (m) {
      if (byDoc[m.doc.id] === undefined) { byDoc[m.doc.id] = []; groups.push(m.doc); }
      byDoc[m.doc.id].push(m.pass);
    });
    groups.forEach(function (doc) {
      var symLink = doc.symbol
        ? "<a href='" + esc(doc.url) + "' target='_blank' rel='noopener'>" + esc(doc.symbol) + "</a>"
        : (doc.url ? "<a href='" + esc(doc.url) + "' target='_blank' rel='noopener'>" + esc(doc.author) + "</a>" : esc(doc.author));
      html += "<section class='doc'><div class='doc-head'>" + symLink +
              "<span class='meta'>" + esc(doc.kind) + ", " + esc(doc.year) + " &middot; " +
              byDoc[doc.id].length + " passage" + (byDoc[doc.id].length > 1 ? "s" : "") + "</span></div>";
      byDoc[doc.id].forEach(function (pass) {
        var cite = passageCitation(doc, pass);
        html += "<div class='passage' data-doc='" + esc(doc.id) + "' data-page='" + pass.page + "'>";
        html += "<div class='cite-row'><cite title='Open the PDF at this page'>" + esc(cite) + "</cite>";
        if (pass.section) html += "<span class='section-name'>" + esc(pass.section) + "</span>";
        html += "</div>";
        html += "<p class='text folded'>" + esc(pass.text) + "</p>";
        html += "<button class='more' type='button'>Show full text</button>";
        html += "</div>";
      });
      html += "</section>";
    });
    return html;
  }

  function renderRelated(currentConcept, matched) {
    var others = [];
    concepts.forEach(function (c) {
      if (c === currentConcept) return;
      var n = 0;
      matched.forEach(function (m) { if (passageMatches(m.pass, c.terms)) n++; });
      if (n > 0) others.push({ c: c, n: n });
    });
    if (!others.length) return "";
    var html = "<div class='related'><h3>Related concepts</h3><p class='how'>Other concepts whose terms appear in the same passages as \"" +
      esc(currentConcept.terms[0]) + "\". The number is how many of this page's passages they share.</p>";
    others.forEach(function (o) {
      html += "<a href='#' data-concept='" + esc(o.c.name) + "'>" + esc(o.c.name) + " (" + o.n + ")</a>";
    });
    return html + "</div>";
  }

  var aiState = { busy: false, output: null, sentCount: 0 };

  function render() {
    renderSidebar();
    var main = document.getElementById("main");
    var concept = getConcept(state.current);
    if (!concept) { main.innerHTML = "<p class='empty'>Concept not found.</p>"; return; }
    var matched = findPassages(concept);

    var html = "<h2 class='page-title'>" + esc(concept.name) + "</h2>";
    html += "<p class='terms'>Found by searching for: " +
      concept.terms.map(function (t) { return "<code>" + esc(t) + "</code>"; }).join(", ") + "</p>";

    if (!matched.length) {
      html += "<p class='empty'>No passage uses this term.</p>";
      main.innerHTML = html;
      return;
    }

    html += renderKindTable(matched);
    html += renderPassages(matched);
    html += renderRelated(concept, matched);

    html += "<button class='draft' id='draft-btn' type='button'>Draft a summary</button>";
    html += "<div class='ai-box' id='ai-box'></div>";

    main.innerHTML = html;
    wirePassages(main);
    wireDraft(main, concept, matched);
  }

  function wirePassages(root) {
    root.querySelectorAll(".passage").forEach(function (el) {
      var docId = el.getAttribute("data-doc");
      var page = parseInt(el.getAttribute("data-page"), 10);
      var cite = el.querySelector("cite");
      cite.addEventListener("click", function () {
        studio.openSource(docId, page);
      });
      var p = el.querySelector("p.text");
      var btn = el.querySelector(".more");
      btn.addEventListener("click", function () {
        var folded = p.classList.toggle("folded");
        btn.textContent = folded ? "Show full text" : "Hide full text";
      });
    });
    root.querySelectorAll(".related a").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        state.current = a.getAttribute("data-concept");
        render();
      });
    });
  }

  function wireDraft(root, concept, matched) {
    var btn = root.querySelector("#draft-btn");
    var box = root.querySelector("#ai-box");
    btn.addEventListener("click", async function () {
      var sent = matched.slice(0, 12);
      var listing = sent.map(function (m) {
        return passageCitation(m.doc, m.pass) + ": " + norm(m.pass.text);
      }).join("\n\n");
      var prompt =
        "You are helping diplomats and human rights staff research neurotechnology and the administration of justice.\n" +
        "Below are " + sent.length + " passages from UN and academic documents on the concept \"" + concept.name + "\" " +
        "(found by searching for: " + concept.terms.join("; ") + ").\n" +
        "Write exactly three sentences summarising what these passages say about this concept. " +
        "Each sentence must end with the citation of the passage it rests on, in brackets. " +
        "Rest only on the passages below; do not use outside knowledge.\n\n" +
        "PASSAGES:\n" + listing;
      aiState.busy = true;
      renderAiBox(box, sent.length);
      btn.disabled = true;
      btn.textContent = "Asking the model…";
      try {
        var answer = await studio.ask(prompt);
        aiState.output = answer;
      } catch (err) {
        aiState.output = "The model could not be reached: " + (err && err.message ? err.message : err);
      }
      aiState.busy = false;
      renderAiBox(box, sent.length);
      btn.disabled = false;
      btn.textContent = "Draft a summary";
    });
  }

  function renderAiBox(box, n) {
    if (aiState.busy) {
      box.innerHTML = "<h3>AI summary</h3><p class='ai-label'>Sending " + n + " passages to the model — they leave the browser. Waiting for the answer…</p>";
      return;
    }
    if (!aiState.output) { box.innerHTML = ""; return; }
    box.innerHTML = "<h3>AI summary</h3>" +
      "<p class='ai-label'>Written by AI. " + n + " passages were sent to the model and left the browser.</p>" +
      "<div class='ai-output' data-source='ai'></div>";
    box.querySelector(".ai-output").textContent = aiState.output;
  }

  // ---- add concept ------------------------------------------------------

  function addConcept(name) {
    var t = name.trim();
    if (!t) return;
    if (getConcept(t)) { state.current = getConcept(t).name; render(); return; }
    concepts.push({ name: t, terms: [t] });
    state.current = t;
    render();
  }
  document.getElementById("add-btn").addEventListener("click", function () {
    var input = document.getElementById("new-concept");
    addConcept(input.value);
    input.value = "";
  });
  document.getElementById("new-concept").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      addConcept(e.target.value);
      e.target.value = "";
    }
  });

  // ---- init -------------------------------------------------------------

  document.getElementById("src-line").textContent =
    lib.title + " — " + (lib.count || docs.length) + " documents on neurotechnology in the administration of justice. " +
    "Every passage can be opened at its original page in the PDF.";

  render();
})();
</script>
</body>
</html>
```

**How we will know it works**: click "Mental privacy" — the table rows sum to the total and the Journal article row is non-zero; clicking a citation such as "A/81/351, para. 2" calls `studio.openSource` with the PDF page; "Lie detection" also finds passages with "deception detection" or "brain fingerprinting" that never say "lie detection"; and "Draft a summary" sends at most 12 passages, saying so on screen, with the answer inside a `data-source="ai"` box.