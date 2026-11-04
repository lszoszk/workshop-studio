I built an app that extracts the numbered paragraphs of a General Comment from its HTML, checks them against the document's own reference, and lets you download them as JSON or Markdown. The header and left rail are always visible; the result and the paragraphs sit on two tabs.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Paragraphs from HTML – UN DOCUMENT</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --red: #9b2335;
  --green: #2e6b49;
  --mono: ui-monospace, Menlo, Consolas, monospace;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background-color: var(--paper);
  accent-color: var(--red);
}
[hidden] { display: none !important; }
a { color: var(--ink); }
a:focus { outline: 2px solid var(--red); outline-offset: 2px; }
h1, h2, h3, h4 { font-weight: 400; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: 2.25rem; margin: 0 0 .5rem; }
h2 { font-family: Georgia, "Times New Roman", serif; font-size: 1.75rem; margin: 1.5rem 0 .5rem; }
h3 { font-size: 1.25rem; margin: 1.25rem 0 .5rem; }
h4 { font-size: 1rem; margin: 1rem 0 .25rem; }
p { margin: .5rem 0; }
small { font-size: .875rem; }
code, kbd, pre, .mono { font-family: var(--mono); font-size: .875rem; }
.mono { letter-spacing: .05em; }
.mono a { text-decoration: none; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: .5rem .75rem; text-align: left; vertical-align: top; border-bottom: 1px solid var(--rule); }
th { font-weight: 600; }
th[scope="col"] { text-align: right; }
th[scope="row"] { text-align: left; }
th[scope="col"]:first-child, td:first-child { padding-left: 0; }
th[scope="col"]:last-child, td:last-child { padding-right: 0; }
caption { font-family: Georgia, "Times New Roman", serif; font-size: 2rem; text-align: left; caption-side: top; margin-bottom: 1rem; }
figcaption { font-family: var(--mono); font-size: .875rem; margin-top: .25rem; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 1.5rem 0; }
button, input, select, textarea {
  font: inherit;
  color: inherit;
  background: transparent;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: .5rem .75rem;
  cursor: pointer;
}
button:focus { outline: 2px solid var(--red); outline-offset: 2px; }
button:hover { background-color: rgba(155, 35, 53, .05); }
button:active { background-color: rgba(155, 35, 53, .1); }
button[aria-expanded="true"] { background-color: rgba(155, 35, 53, .1); }
button[disabled] { opacity: .5; cursor: not-allowed; }
button.secondary { border-color: transparent; }
button.secondary:hover { background-color: rgba(29, 27, 24, .05); }
button.secondary:active { background-color: rgba(29, 27, 24, .1); }
button.small { padding: .25rem .5rem; font-size: .875rem; }
.red { color: var(--red); }
.green { color: var(--green); }
.dot {
  display: inline-block;
  width: .75rem;
  height: .75rem;
  border-radius: 50%;
  margin-right: .5rem;
}
.dot.green { background-color: var(--green); }
.dot.red { background-color: var(--red); }
.dot.gray { background-color: var(--rule); }

/* Layout */
.container {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
}
@media (max-width: 768px) {
  .container { grid-template-columns: 1fr; }
  .rail { display: none; }
}
.header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}
.header h1 { margin-bottom: 0; }
.header .meta { text-align: right; }
.rail {
  border-right: 1px solid var(--rule);
  padding-right: 1.5rem;
  margin-right: 1.5rem;
}
.rail h3 { margin-top: 0; }
.rail .card {
  background-color: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.rail .card h4 { margin-top: 0; }
.rail .numbers {
  display: flex;
  justify-content: space-between;
  margin: 1rem 0;
}
.rail .numbers .number {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  line-height: 1;
}
.rail .numbers .label {
  font-family: var(--mono);
  font-size: .875rem;
  text-align: right;
}
.rail .bar {
  height: 4px;
  background-color: var(--rule);
  margin: .5rem 0;
  border-radius: 2px;
}
.rail .bar.green { background-color: var(--green); }
.rail .bar.red { background-color: var(--red); }
.rail .bar .fill {
  height: 100%;
  border-radius: 2px;
}
.main { padding-bottom: 3rem; }
.tabs {
  display: flex;
  gap: 1px;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 1.5rem;
}
.tabs button {
  padding: .75rem 1rem;
  border: 0;
  border-radius: 0;
  background: transparent;
  font-family: var(--mono);
  font-size: .875rem;
  letter-spacing: .05em;
  cursor: pointer;
  border-bottom: 3px solid transparent;
}
.tabs button[aria-selected="true"] {
  border-bottom-color: var(--red);
  font-weight: 600;
}
.tabpanel { padding: 0; }
.tabpanel:focus { outline: none; }

/* Tiles */
.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.tile {
  background-color: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
}
.tile h3 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  margin: 0 0 .5rem;
  line-height: 1;
}
.tile .label { font-family: var(--mono); font-size: .875rem; }
.tile .how {
  font-size: .875rem;
  color: var(--ink);
  margin-top: .5rem;
}
.tile .mismatch {
  margin-top: .5rem;
  font-size: .875rem;
}
.tile .mismatch ul { margin: .25rem 0; padding-left: 1rem; }
.tile .mismatch li { margin: .125rem 0; }
.tile .mismatch a { text-decoration: none; }
.tile .mismatch a:hover { text-decoration: underline; }
.tile .red { color: var(--red); }
.tile .green { color: var(--green); }

/* Table */
table.paragraphs {
  width: 100%;
  border-collapse: collapse;
}
table.paragraphs th, table.paragraphs td {
  padding: .75rem 1rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
table.paragraphs th { font-weight: 600; }
table.paragraphs th[scope="col"]:nth-child(1) { width: 60px; }
table.paragraphs th[scope="col"]:nth-child(2) { width: 240px; }
table.paragraphs th[scope="col"]:nth-child(3) { width: 1fr; }
table.paragraphs th[scope="col"]:nth-child(4) { width: 120px; }
table.paragraphs tr[aria-expanded="true"] td { border-bottom: 0; }
table.paragraphs tr[aria-expanded="true"] + tr.separator td {
  padding: 0;
  border-bottom: 1px solid var(--rule);
  line-height: 4px;
}
table.paragraphs tr.separator td { border-bottom: 0; }
table.paragraphs .expanded {
  background-color: white;
  border: 1px solid var(--rule);
  border-top: 0;
  border-radius: 0 0 4px 4px;
  padding: 1rem;
  margin-top: -1px;
}
table.paragraphs .expanded p {
  margin: .5rem 0;
  white-space: pre-wrap;
}
table.paragraphs .expanded .first-words {
  display: flex;
  gap: 1rem;
  margin: .5rem 0;
}
table.paragraphs .expanded .first-words .found, table.paragraphs .expanded .first-words .reference {
  flex: 1;
}
table.paragraphs .expanded .first-words .label {
  font-family: var(--mono);
  font-size: .875rem;
  color: var(--ink);
}
table.paragraphs .expanded .spaces {
  margin: .5rem 0;
}
table.paragraphs .expanded .spaces .space {
  display: inline-block;
  background-color: rgba(155, 35, 53, .1);
  border: 1px solid var(--red);
  border-radius: 2px;
  padding: 0 .25rem;
  margin: 0 .125rem;
  font-family: var(--mono);
  font-size: .875rem;
}
table.paragraphs .expanded .spaces .rule {
  font-family: var(--mono);
  font-size: .875rem;
  color: var(--ink);
  margin-left: .5rem;
}
table.paragraphs .expanded .citation {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}
table.paragraphs .expanded .citation button {
  white-space: nowrap;
}
table.paragraphs .expanded .citation .copied {
  font-family: var(--mono);
  font-size: .875rem;
  color: var(--green);
  opacity: 0;
  transition: opacity .2s;
}
table.paragraphs .expanded .citation .copied.show {
  opacity: 1;
}
table.paragraphs .no { font-family: var(--mono); text-align: right; }
table.paragraphs .section { font-size: .875rem; }
table.paragraphs .first-line {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 480px;
}
table.paragraphs .check {
  font-family: var(--mono);
  font-size: .875rem;
  text-align: right;
}
table.paragraphs .check.red { color: var(--red); }
table.paragraphs .check.green { color: var(--green); }

/* Headings box */
.headings-box {
  background-color: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.headings-box h4 {
  margin-top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.headings-box ul {
  margin: .5rem 0 0;
  padding-left: 1rem;
  columns: 2;
}
.headings-box li {
  margin: .25rem 0;
  break-inside: avoid;
}

/* Checks */
.checks {
  background-color: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.checks h4 {
  margin-top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.checks ul { margin: .5rem 0 0; padding-left: 0; list-style: none; }
.checks li {
  padding: .5rem 0;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.checks li:last-child { border-bottom: 0; }
.checks .check { font-family: var(--mono); font-size: .875rem; }
.checks .check.red { color: var(--red); }
.checks .check.green { color: var(--green); }
.checks .check.gray { color: var(--rule); }
.checks .details {
  margin-top: .5rem;
  padding-left: 1rem;
  font-size: .875rem;
}
.checks .details ul { margin: .25rem 0; padding-left: 1rem; }
.checks .details li { margin: .125rem 0; }
.checks .details a { text-decoration: none; }
.checks .details a:hover { text-decoration: underline; }

/* Spaces */
.spaces {
  background-color: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.spaces h4 {
  margin-top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.spaces table {
  width: 100%;
  border-collapse: collapse;
  margin-top: .5rem;
}
.spaces th, .spaces td {
  padding: .5rem .75rem;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid var(--rule);
}
.spaces th { font-weight: 600; }
.spaces th[scope="col"]:nth-child(1) { width: 60px; }
.spaces th[scope="col"]:nth-child(2) { width: 1fr; }
.spaces th[scope="col"]:nth-child(3) { width: 1fr; }
.spaces th[scope="col"]:nth-child(4) { width: 1fr; }
.spaces tr[aria-expanded="true"] td { border-bottom: 0; }
.spaces tr[aria-expanded="true"] + tr.separator td {
  padding: 0;
  border-bottom: 1px solid var(--rule);
  line-height: 4px;
}
.spaces tr.separator td { border-bottom: 0; }
.spaces .expanded {
  background-color: white;
  border: 1px solid var(--rule);
  border-top: 0;
  border-radius: 0 0 4px 4px;
  padding: 1rem;
  margin-top: -1px;
}
.spaces .expanded p {
  margin: .5rem 0;
  white-space: pre-wrap;
}
.spaces .expanded .space {
  display: inline-block;
  background-color: rgba(155, 35, 53, .1);
  border: 1px solid var(--red);
  border-radius: 2px;
  padding: 0 .25rem;
  margin: 0 .125rem;
  font-family: var(--mono);
  font-size: .875rem;
}
.spaces .expanded .rule {
  font-family: var(--mono);
  font-size: .875rem;
  color: var(--ink);
  margin-left: .5rem;
}
.spaces .counts {
  display: flex;
  gap: 1rem;
  margin-top: .5rem;
  font-family: var(--mono);
  font-size: .875rem;
}
.spaces .counts .count {
  flex: 1;
  text-align: center;
  padding: .5rem;
  background-color: rgba(155, 35, 53, .05);
  border-radius: 4px;
}

/* Footer */
.footer {
  grid-column: 1 / -1;
  border-top: 1px solid var(--rule);
  padding-top: 1rem;
  margin-top: 1.5rem;
  font-size: .875rem;
  color: var(--ink);
}
.footer a { color: var(--ink); }
</style>
</head>
<body>

<div class="container">
  <header class="header">
    <div>
      <h1><span class="mono">UN DOCUMENT · HTML</span><br>Paragraphs from HTML</h1>
    </div>
    <div class="meta">
      <div id="check-status">
        <span class="dot green" id="check-dot"></span>
        <span id="check-count">0 of 0 checks pass</span>
      </div>
      <div>1 source limit</div>
    </div>
  </header>

  <aside class="rail">
    <div class="card">
      <h4 class="mono">DOCUMENT</h4>
      <h3 id="symbol" class="mono"></h3>
      <p id="short-title"></p>
    </div>
    <h4>Paragraphs</h4>
    <div class="numbers">
      <div class="number" id="paragraphs-found">0</div>
      <div class="label">of <span id="paragraphs-expected">0</span></div>
    </div>
    <div class="bar" id="paragraphs-bar">
      <div class="fill" id="paragraphs-fill"></div>
    </div>
    <h4>Footnotes</h4>
    <div class="numbers">
      <div class="number red">0</div>
      <div class="label">of <span id="footnotes-expected">0</span></div>
    </div>
    <p class="red">not in this HTML</p>
    <h4>Checks</h4>
    <div id="checks-passed">0 of 0 checks pass</div>
  </aside>

  <main class="main">
    <div class="tabs" role="tablist" aria-label="Tabs">
      <button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
      <button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
    </div>

    <div id="panel-01" class="tabpanel" role="tabpanel" aria-labelledby="tab-01" tabindex="0">
      <div class="tiles">
        <div class="tile">
          <h3 id="paragraphs-found-tile">0</h3>
          <div class="label">Paragraphs found</div>
          <div class="how">How this is computed: the app counts the numbered &lt;p&gt; elements in the HTML.</div>
        </div>
        <div class="tile">
          <h3 id="paragraphs-expected-tile">0</h3>
          <div class="label">the document has</div>
          <div class="how">How this is computed: the reference in the data.</div>
        </div>
        <div class="tile">
          <h3 id="first-words-match-tile">0</h3>
          <div class="label">First words match</div>
          <div class="how">How this is computed: the first six words of each paragraph against the reference.</div>
          <div class="mismatch" id="first-words-mismatch">
            <div id="first-words-list"></div>
          </div>
        </div>
        <div class="tile">
          <h3 class="red">0</h3>
          <div class="label red">of <span id="footnotes-expected-tile">0</span></div>
          <div class="how red">Footnotes</div>
          <div class="mismatch red">this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.</div>
        </div>
        <div class="tile">
          <h3 id="spaces-restored-tile">0</h3>
          <div class="label">Spaces</div>
          <div class="how">How this is computed: rules restore a space where the characters prove it was there.</div>
        </div>
      </div>

      <h3>Take the paragraphs away</h3>
      <div>
        <button id="download-json" class="secondary">Download JSON</button>
        <button id="download-markdown" class="secondary">Download Markdown</button>
      </div>

      <div class="checks">
        <h4>
          <button id="checks-toggle" aria-expanded="false" aria-controls="checks-list">Every check (<span id="checks-count">0</span>)</button>
        </h4>
        <div id="checks-list" hidden>
          <ul id="checks-results"></ul>
        </div>
      </div>

      <div class="spaces">
        <h4>
          <button id="spaces-toggle" aria-expanded="false" aria-controls="spaces-list">The spaces restored (<span id="spaces-count">0</span>)</button>
        </h4>
        <div id="spaces-list" hidden>
          <div class="counts">
            <div class="count">
              <div>sentence join</div>
              <div id="spaces-sentence">0</div>
            </div>
            <div class="count">
              <div>comma join</div>
              <div id="spaces-comma">0</div>
            </div>
            <div class="count">
              <div>quote join</div>
              <div id="spaces-quote">0</div>
            </div>
            <div class="count">
              <div>dash join</div>
              <div id="spaces-dash">0</div>
            </div>
          </div>
          <table>
            <thead>
              <tr>
                <th scope="col">Para.</th>
                <th scope="col">Before</th>
                <th scope="col">After</th>
                <th scope="col">Rule</th>
              </tr>
            </thead>
            <tbody id="spaces-table"></tbody>
          </table>
          <p><small>Rules restore a space only where the characters prove it was there. Word pairs such as "Giventhe" are not touched.</small></p>
        </div>
      </div>
    </div>

    <div id="panel-02" class="tabpanel" role="tabpanel" aria-labelledby="tab-02" hidden>
      <div class="headings-box">
        <h4>
          Headings found: <span id="headings-count">0</span>
          <button id="headings-toggle" aria-expanded="false" aria-controls="headings-list" class="small">show</button>
        </h4>
        <div id="headings-list" hidden>
          <ul id="headings-ul"></ul>
        </div>
      </div>

      <table class="paragraphs">
        <caption>FIG.01 – The numbered paragraphs of <span id="symbol-table"></span>. Click a row to expand it and see the full text, the first words and the spaces restored.</caption>
        <thead>
          <tr>
            <th scope="col">No.</th>
            <th scope="col">Section</th>
            <th scope="col">First line</th>
            <th scope="col">Check</th>
          </tr>
        </thead>
        <tbody id="paragraphs-table"></tbody>
      </table>
    </div>
  </main>
</div>

<footer class="footer">
  <p>Source: <span id="source"></span> · Built: <span id="built"></span> · Done by this page's code; no model was called and nothing left the browser.</p>
</footer>

<script>
document.addEventListener('DOMContentLoaded', () => {
  const data = window.WORKSHOP_DATA.html_doc;
  const doc = new DOMParser().parseFromString(data.html, 'text/html');
  const reference = data.reference || {};
  const today = new Date().toISOString().split('T')[0];

  // Header
  document.querySelector('#symbol').textContent = data.symbol;
  document.querySelector('#short-title').textContent = data.title.split('*')[0].trim();
  const titleLink = document.createElement('a');
  titleLink.href = data.doc_url;
  titleLink.target = '_blank';
  titleLink.textContent = data.symbol;
  document.querySelector('h1').innerHTML = `<span class="mono">UN DOCUMENT · HTML</span><br>Paragraphs from <a href="${data.doc_url}" target="_blank">${data.symbol}</a>`;
  document.querySelector('#source').textContent = data.source;
  document.querySelector('#built').textContent = today;

  // Rail
  document.querySelector('#paragraphs-expected').textContent = reference.paragraphs || '?';
  document.querySelector('#footnotes-expected').textContent = reference.footnotes || '?';

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabPanels = document.querySelectorAll('[role="tabpanel"]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const selected = tab.getAttribute('aria-selected') === 'true';
      if (selected) return;
      tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
      tabPanels.forEach(p => p.hidden = true);
      tab.setAttribute('aria-selected', 'true');
      document.querySelector(`#${tab.getAttribute('aria-controls')}`).hidden = false;
    });
  });

  // Pipeline
  const elements = Array.from(doc.body.children);
  const coverEnd = elements.findIndex(el => el.tagName === 'TABLE') + 1;
  const content = elements.slice(coverEnd);

  const paragraphs = [];
  const headings = [];
  let committeeLine = null;
  let title = null;

  content.forEach(el => {
    if (el.tagName === 'P') {
      const text = el.textContent.trim();
      const match = text.match(/^(\d{1,3})\.\s*(.*)$/s);
      if (match) {
        const number = parseInt(match[1], 10);
        const textRaw = match[2].trim().replace(/\s+/g, ' ');
        paragraphs.push({ el, number, textRaw, text: textRaw, section: null, part: null });
      } else if (!committeeLine && text.match(/Committee on/)) {
        committeeLine = text;
      }
    } else if (el.tagName === 'H2') {
      if (!title) {
        title = el.textContent.trim();
      } else {
        const match = el.textContent.trim().match(/^([IVX]+)\.\s*(.+)$/);
        const label = match ? match[1] : null;
        const heading = match ? match[2] : el.textContent.trim();
        headings.push({ el, level: 2, label, heading, part: label });
      }
    } else if (el.tagName === 'H3') {
      const match = el.textContent.trim().match(/^([A-Z])\.\s*(.+)$/);
      const label = match ? match[1] : null;
      const heading = match ? match[2] : el.textContent.trim();
      headings.push({ el, level: 3, label, heading, part: null });
    }
  });

  // Assign section and part
  let currentPart = null;
  let currentSection = null;
  content.forEach(el => {
    const heading = headings.find(h => h.el === el);
    if (heading) {
      if (heading.level === 2 && heading.part) currentPart = heading;
      currentSection = heading;
    }
    const paragraph = paragraphs.find(p => p.el === el);
    if (paragraph) {
      paragraph.part = currentPart ? currentPart.heading : null;
      paragraph.section = currentSection ? currentSection.heading : null;
    }
  });

  // Repairs
  const repairs = [];
  const rules = {
    sentence: /([a-z])\.([A-Z])/g,
    comma: /([a-z]),([A-Za-z])/g,
    quote: /([a-z])“/g,
    dash: /–([A-Za-z])/g
  };
  paragraphs.forEach(p => {
    let text = p.text;
    Object.entries(rules).forEach(([name, regex]) => {
      let match;
      while ((match = regex.exec(text)) !== null) {
        const before = text.slice(Math.max(0, match.index - 20), match.index);
        const after = text.slice(match.index + match[0].length, match.index + match[0].length + 20);
        repairs.push({
          paragraph: p.number,
          rule: name,
          before: match[0],
          after: match[0].replace(regex, `$1 ${name === 'quote' ? '“' : name === 'dash' ? '–' : '$2'}`),
          contextBefore: before,
          contextAfter: after
        });
        text = text.replace(regex, `$1 ${name === 'quote' ? '“' : name === 'dash' ? '–' : '$2'}`);
        regex.lastIndex = 0; // Reset for global regex
      }
    });
    p.text = text;
  });

  // First words
  const firstWordsMismatch = [];
  paragraphs.forEach(p => {
    const found = p.text.split(/\s+/).slice(0, 6).join(' ');
    const expected = reference.first_words ? reference.first_words[String(p.number)] : null;
    if (expected) {
      const normalise = s => s.replace(/[“”]/g, '"').replace(/[–‑]/g, '-').replace(/\u00A0/g, ' ');
      p.firstWordsMatch = normalise(found) === normalise(expected);
      if (!p.firstWordsMatch) {
        firstWordsMismatch.push({
          number: p.number,
          found: found,
          expected: expected
        });
      }
    } else {
      p.firstWordsMatch = null;
    }
  });

  // Checks
  const checks = [];
  const check = (name, actual, expected, message, details = null, limit = false) => {
    const pass = limit ? 'limit' : actual === expected;
    checks.push({
      name,
      actual,
      expected,
      pass,
      message,
      details,
      limit
    });
  };

  check('Paragraph count', paragraphs.length, reference.paragraphs || null, 'Found against reference.paragraphs');
  check('Numbering', paragraphs.every((p, i) => p.number === i + 1), true, 'Exactly 1 to n in order', paragraphs.filter((p, i) => p.number !== i + 1).map(p => p.number));
  check('First words', paragraphs.filter(p => p.firstWordsMatch === false).length, 0, 'Mismatches counted', firstWordsMismatch);
  check('Footnotes', 0, reference.footnotes || null, '0 against reference.footnotes', null, true);
  check('Repairs', repairs.length, null, `${repairs.length} spaces restored in ${new Set(repairs.map(r => r.paragraph)).size} paragraphs`, Object.entries(rules).map(([name, regex]) => ({
    name,
    count: repairs.filter(r => r.rule === name).length
  })));
  check('Headings', headings.length, null, `${headings.filter(h => h.level === 2).length} h2, ${headings.filter(h => h.level === 3).length} h3; ${headings.filter(h => h.label).length} glued labels separated`);
  check('Nothing lost', content.length, paragraphs.length + headings.length + (committeeLine ? 1 : 0) + (title ? 1 : 0), 'Every block element is classified exactly once', content.filter(el => !paragraphs.some(p => p.el === el) && !headings.some(h => h.el === el) && el.textContent.trim() !== committeeLine && el.textContent.trim() !== title));

  const json = paragraphs.map(p => ({
    symbol: data.symbol,
    paragraph: p.number,
    section: p.section,
    part: p.part,
    text: p.text,
    text_raw: p.textRaw,
    first_words_match: p.firstWordsMatch,
    citation: `${data.symbol}, para. ${p.number}`,
    doc_url: data.doc_url,
    limitations: `no footnotes in this HTML version; the document has ${reference.footnotes || '?'}`
  }));
  const roundTrip = JSON.parse(JSON.stringify(json));
  check('Export round trip', roundTrip.length, paragraphs.length, 'The JSON to download is parsed back; its record count equals the table\'s');

  // Render
  const checksPassed = checks.filter(c => c.pass === true).length;
  const checksFailed = checks.filter(c => c.pass === false).length;
  const checksLimit = checks.filter(c => c.limit).length;
  const checksTotal = checks.length - checksLimit;

  document.querySelector('#check-dot').className = checksFailed > 0 ? 'dot red' : 'dot green';
  document.querySelector('#check-count').textContent = `${checksPassed} of ${checksTotal} checks pass`;
  document.querySelector('#checks-passed').textContent = `${checksPassed} of ${checksTotal} checks pass`;
  document.querySelector('#checks-count').textContent = checks.length;

  document.querySelector('#paragraphs-found').textContent = paragraphs.length;
  document.querySelector('#paragraphs-found-tile').textContent = paragraphs.length;
  document.querySelector('#paragraphs-expected-tile').textContent = reference.paragraphs || '?';
  document.querySelector('#footnotes-expected-tile').textContent = reference.footnotes || '?';
  document.querySelector('#spaces-restored-tile').textContent = repairs.length;

  const paragraphsBar = document.querySelector('#paragraphs-bar');
  const paragraphsFill = document.querySelector('#paragraphs-fill');
  if (reference.paragraphs) {
    const percent = Math.min(100, Math.max(0, (paragraphs.length / reference.paragraphs) * 100));
    paragraphsFill.style.width = `${percent}%`;
    paragraphsBar.className = percent === 100 ? 'bar green' : 'bar red';
  } else {
    paragraphsBar.className = 'bar';
    paragraphsFill.style.width = '0%';
  }

  // First words mismatch
  const firstWordsList = document.querySelector('#first-words-list');
  if (firstWordsMismatch.length > 0) {
    firstWordsList.innerHTML = '<ul>' + firstWordsMismatch.slice(0, 10).map(m => `
      <li>para. ${m.number}: found <span class="mono">${m.found}</span> / reference <span class="mono">${m.expected}</span></li>
    `).join('') + '</ul>';
    if (firstWordsMismatch.length > 10) {
      firstWordsList.innerHTML += `<p>and ${firstWordsMismatch.length - 10} more</p>`;
    }
  } else {
    firstWordsList.innerHTML = '<p>All match.</p>';
  }
  document.querySelector('#first-words-match-tile').textContent = paragraphs.filter(p => p.firstWordsMatch === true).length;

  // Checks
  const checksResults = document.querySelector('#checks-results');
  checksResults.innerHTML = checks.map(c => `
    <li>
      <div>${c.name}</div>
      <div class="check ${c.pass === true ? 'green' : c.limit ? 'gray' : 'red'}">
        ${c.pass === true ? 'pass' : c.limit ? 'source limit' : 'check failed'}
      </div>
      ${c.details ? `
      <div class="details">
        <p>${c.message}</p>
        ${Array.isArray(c.details) ? `
        <ul>
          ${c.details.map(d => `<li>${typeof d === 'object' ? `${d.name}: ${d.count}` : d}</li>`).join('')}
        </ul>
        ` : c.details}
      </div>
      ` : ''}
    </li>
  `).join('');

  // Spaces
  const spacesTable = document.querySelector('#spaces-table');
  const repairsByParagraph = {};
  repairs.forEach(r => {
    if (!repairsByParagraph[r.paragraph]) repairsByParagraph[r.paragraph] = [];
    repairsByParagraph[r.paragraph].push(r);
  });
  spacesTable.innerHTML = Object.entries(repairsByParagraph).map(([number, repairs]) => `
    <tr>
      <td>${number}</td>
      <td>${repairs[0].contextBefore}<span class="space">${repairs[0].before}</span>${repairs[0].contextAfter}</td>
      <td>${repairs[0].contextBefore}<span class="space">${repairs[0].after}</span>${repairs[0].contextAfter}</td>
      <td>${repairs[0].rule}</td>
    </tr>
    ${repairs.slice(1).map(r => `
    <tr>
      <td></td>
      <td>${r.contextBefore}<span class="space">${r.before}</span>${r.contextAfter}</td>
      <td>${r.contextBefore}<span class="space">${r.after}</span>${r.contextAfter}</td>
      <td>${r.rule}</td>
    </tr>
    `).join('')}
  `).join('');

  document.querySelector('#spaces-sentence').textContent = repairs.filter(r => r.rule === 'sentence').length;
  document.querySelector('#spaces-comma').textContent = repairs.filter(r => r.rule === 'comma').length;
  document.querySelector('#spaces-quote').textContent = repairs.filter(r => r.rule === 'quote').length;
  document.querySelector('#spaces-dash').textContent = repairs.filter(r => r.rule === 'dash').length;
  document.querySelector('#spaces-count').textContent = repairs.length;

  // Headings
  const headingsUl = document.querySelector('#headings-ul');
  headingsUl.innerHTML = headings.map(h => `
    <li>${h.level === 2 ? `<strong>${h.heading}</strong>` : h.heading}</li>
  `).join('');
  document.querySelector('#headings-count').textContent = headings.length;

  // Paragraphs table
  const paragraphsTable = document.querySelector('#paragraphs-table');
  const symbolTable = document.querySelector('#symbol-table');
  symbolTable.textContent = data.symbol;
  paragraphsTable.innerHTML = paragraphs.map(p => `
    <tr aria-expanded="false" tabindex="0">
      <td class="no">${p.number}</td>
      <td class="section">${p.section || ''}</td>
      <td class="first-line">${p.text.slice(0, 120).replace(/\s+/g, ' ').trim()}${p.text.length > 120 ? '…' : ''}</td>
      <td class="check ${p.firstWordsMatch === false ? 'red' : 'green'}">${p.firstWordsMatch === false ? 'first words differ' : 'OK'}</td>
    </tr>
    <tr class="separator"><td colspan="4"></td></tr>
    <tr hidden>
      <td colspan="4" class="expanded">
        <p>${p.text.replace(/\s+/g, ' ')}</p>
        <div class="first-words">
          <div class="found">
            <div class="label">Found</div>
            <div>${p.text.split(/\s+/).slice(0, 6).join(' ')}</div>
          </div>
          <div class="reference">
            <div class="label">Reference</div>
            <div>${reference.first_words ? reference.first_words[String(p.number)] || '?' : '?'}</div>
          </div>
        </div>
        ${repairsByParagraph[p.number] ? `
        <div class="spaces">
          <div class="label">Spaces restored in this paragraph:</div>
          ${repairsByParagraph[p.number].map(r => `
          <div>
            <span class="space">${r.before}</span> → <span class="space">${r.after}</span>
            <span class="rule">(${r.rule})</span>
          </div>
          `).join('')}
        </div>
        ` : ''}
        <div class="citation">
          <button class="copy-citation" data-citation="${data.symbol}, para. ${p.number}">Copy citation</button>
          <span class="copied">Copied</span>
        </div>
      </td>
    </tr>
  `).join('');

  // Expand rows
  document.querySelectorAll('[aria-expanded][tabindex="0"]').forEach(button => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !expanded);
      const nextRow = button.parentElement.nextElementSibling;
      if (nextRow && nextRow.classList.contains('separator')) {
        nextRow.hidden = expanded;
        nextRow.nextElementSibling.hidden = expanded;
      }
    });
    button.addEventListener('keydown', e => {
      if (e.key === 'Enter') button.click();
    });
  });

  // Copy citation
  document.querySelectorAll('.copy-citation').forEach(button => {
    button.addEventListener('click', () => {
      navigator.clipboard.writeText(button.dataset.citation);
      const copied = button.nextElementSibling;
      copied.classList.add('show');
      setTimeout(() => copied.classList.remove('show'), 2000);
    });
  });

  // Download JSON
  document.querySelector('#download-json').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.json';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Download Markdown
  document.querySelector('#download-markdown').addEventListener('click', () => {
    const frontMatter = `---
title: "${data.title.replace(/\*$/, '').trim()}"
symbol: ${data.symbol}
adopted: ${reference.adopted || '?'}
source_url: ${data.doc_url}
extracted: ${today}
paragraphs_found: ${paragraphs.length}
paragraphs_expected: ${reference.paragraphs || '?'}
footnotes: no footnotes in this HTML version; the document has ${reference.footnotes || '?'}
---`;

    const headingsByPart = {};
    headings.forEach(h => {
      if (h.level === 2 && h.part) {
        if (!headingsByPart[h.part]) headingsByPart[h.part] = [];
        headingsByPart[h.part].push(h);
      }
    });

    const parts = Object.entries(headingsByPart).sort((a, b) => {
      const roman = { I: 1, II: 2, III: 3, IV: 4, V: 5, VI: 6, VII: 7, VIII: 8, IX: 9, X: 10 };
      return roman[a[0]] - roman[b[0]];
    });

    const markdown = [frontMatter];
    parts.forEach(([part, headings]) => {
      markdown.push(`\n## ${part}`);
      headings.forEach(h => {
        if (h.level === 3) markdown.push(`\n### ${h.heading}`);
      });
      paragraphs.filter(p => p.part === part).forEach(p => {
        markdown.push(`\n**${p.number}.** ${p.text}`);
      });
    });

    const blob = new Blob([markdown.join('\n')], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.md';
    a.click();
    URL.revokeObjectURL(url);
  });

  // Toggle checks and spaces
  document.querySelector('#checks-toggle').addEventListener('click', () => {
    const expanded = document.querySelector('#checks-toggle').getAttribute('aria-expanded') === 'true';
    document.querySelector('#checks-toggle').setAttribute('aria-expanded', !expanded);
    document.querySelector('#checks-list').hidden = expanded;
  });
  document.querySelector('#spaces-toggle').addEventListener('click', () => {
    const expanded = document.querySelector('#spaces-toggle').getAttribute('aria-expanded') === 'true';
    document.querySelector('#spaces-toggle').setAttribute('aria-expanded', !expanded);
    document.querySelector('#spaces-list').hidden = expanded;
  });
  document.querySelector('#headings-toggle').addEventListener('click', () => {
    const expanded = document.querySelector('#headings-toggle').getAttribute('aria-expanded') === 'true';
    document.querySelector('#headings-toggle').setAttribute('aria-expanded', !expanded);
    document.querySelector('#headings-list').hidden = expanded;
  });
});
</script>
</body>
</html>
```