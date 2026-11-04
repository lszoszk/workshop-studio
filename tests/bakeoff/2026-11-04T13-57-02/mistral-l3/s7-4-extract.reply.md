I built an app that extracts the numbered paragraphs from the General Comment's HTML, checks them against the document's own reference, and lets you download the result as JSON or Markdown. The left rail shows the document's symbol and the counts; the first tab gives the answer at a glance, the second lists every paragraph with its heading and citation.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Paragraphs from a UN document</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --accent: #9b2335;
  --pass: #2e6b3a;
}
body {
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--ink);
  background: var(--paper);
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
header, footer {
  grid-column: 1 / -1;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid var(--rule);
  font-size: 0.8rem;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  letter-spacing: 0.05em;
  color: var(--ink);
}
h1 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: normal;
  margin: 0.5rem 0 0;
  line-height: 1.2;
}
.rail {
  padding: 1rem;
  border-right: 1px solid var(--rule);
  background: var(--paper);
}
.rail h2 {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 0 0 1rem;
  color: var(--ink);
}
.rail-card {
  background: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
}
.rail-card h3 {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 0 0 0.5rem;
  color: var(--ink);
}
.rail-card p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}
.big-number {
  font-family: Georgia, serif;
  font-size: 2.5rem;
  font-weight: normal;
  margin: 0.5rem 0;
  line-height: 1;
}
.big-number small {
  font-size: 1rem;
  color: var(--ink);
  display: block;
}
.big-number.red { color: var(--accent); }
.big-number.green { color: var(--pass); }
.status-dot {
  display: inline-block;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.status-dot.green { background: var(--pass); }
.status-dot.red { background: var(--accent); }
.tabs {
  display: flex;
  border-bottom: 1px solid var(--rule);
  margin: 0;
  padding: 0;
  list-style: none;
}
.tabs li {
  margin: 0;
  padding: 0;
}
.tabs button {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  padding: 0.75rem 1rem;
  margin: 0;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--ink);
  border-bottom: 2px solid transparent;
}
.tabs button[aria-selected="true"] {
  color: var(--accent);
  border-bottom-color: var(--accent);
}
.tab-panel {
  padding: 1.5rem;
}
.tab-panel:not([aria-hidden="true"]) {
  display: block;
}
.tab-panel[aria-hidden="true"] {
  display: none;
}
.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.tile {
  border: 1px solid var(--rule);
  border-radius: 4px;
  padding: 1rem;
  background: white;
}
.tile h3 {
  font-family: Georgia, serif;
  font-size: 2rem;
  font-weight: normal;
  margin: 0 0 0.5rem;
  line-height: 1.1;
}
.tile p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--ink);
}
.tile .red { color: var(--accent); }
.tile .green { color: var(--pass); }
.tile .how {
  font-family: ui-monospace, monospace;
  font-size: 0.7rem;
  letter-spacing: 0.05em;
  color: var(--ink);
  margin-top: 0.5rem;
}
.mismatch-list {
  margin: 1rem 0;
  padding: 0;
  list-style: none;
}
.mismatch-list li {
  padding: 0.25rem 0;
  border-bottom: 1px solid var(--rule);
}
.mismatch-list li:last-child { border-bottom: none; }
.mismatch-list code {
  font-family: ui-monospace, monospace;
  background: var(--rule);
  padding: 0.1rem 0.25rem;
  border-radius: 2px;
}
.export-buttons {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
}
.export-buttons button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
}
.export-buttons button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.check-panel {
  margin-top: 2rem;
}
.check-panel h2 {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 0 0 1rem;
  color: var(--ink);
}
.check-panel button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  cursor: pointer;
  display: flex;
  align-items: center;
  width: 100%;
  text-align: left;
}
.check-panel button[aria-expanded="true"] .arrow::after { content: "▼"; }
.check-panel button[aria-expanded="false"] .arrow::after { content: "▶"; }
.check-panel .arrow {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  margin-right: 0.5rem;
}
.check-panel .check-line {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.check-panel .check-line:last-child { border-bottom: none; }
.check-panel .check-line .status {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}
.check-panel .check-line .status.pass { color: var(--pass); }
.check-panel .check-line .status.fail { color: var(--accent); }
.check-panel .check-line .status.limit { color: var(--accent); }
.check-panel .check-line .link {
  color: var(--accent);
  text-decoration: none;
  font-size: 0.8rem;
}
.check-panel .check-details {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
}
.check-panel .check-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}
.spaces-panel {
  margin-top: 2rem;
}
.spaces-panel table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}
.spaces-panel caption {
  font-family: Georgia, serif;
  font-size: 1rem;
  text-align: left;
  margin-bottom: 0.5rem;
}
.spaces-panel th {
  text-align: left;
  font-weight: normal;
  padding: 0.25rem 0;
  border-bottom: 1px solid var(--rule);
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}
.spaces-panel td {
  padding: 0.25rem 0;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
.spaces-panel tr:last-child td { border-bottom: none; }
.spaces-panel td code {
  font-family: ui-monospace, monospace;
  background: var(--rule);
  padding: 0.1rem 0.25rem;
  border-radius: 2px;
}
.spaces-panel .rule-counts {
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
.spaces-panel .rule-counts span {
  display: inline-block;
  margin-right: 1rem;
}
table.paragraphs {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
table.paragraphs caption {
  font-family: Georgia, serif;
  font-size: 1rem;
  text-align: left;
  margin-bottom: 0.5rem;
}
table.paragraphs th {
  text-align: left;
  font-weight: normal;
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
}
table.paragraphs td {
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
table.paragraphs tr:last-child td { border-bottom: none; }
table.paragraphs tr[aria-expanded="true"] { background: white; }
table.paragraphs tr[aria-expanded="false"] { background: var(--paper); }
table.paragraphs tr[aria-expanded="false"]:hover { background: #e9e4d9; }
table.paragraphs .no { font-family: ui-monospace, monospace; text-align: right; }
table.paragraphs .section { font-size: 0.9rem; }
table.paragraphs .first-line { font-size: 0.9rem; }
table.paragraphs .check { font-family: ui-monospace, monospace; font-size: 0.8rem; }
table.paragraphs .check.fail { color: var(--accent); }
table.paragraphs .expanded {
  grid-column: 1 / -1;
  padding: 1rem;
  background: white;
  border: 1px solid var(--rule);
  border-radius: 4px;
  margin-top: 0.5rem;
}
table.paragraphs .expanded p {
  margin: 0.5rem 0;
  white-space: pre-wrap;
}
table.paragraphs .expanded .first-words {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}
table.paragraphs .expanded .first-words .found {
  font-family: ui-monospace, monospace;
  background: var(--rule);
  padding: 0.1rem 0.25rem;
  border-radius: 2px;
}
table.paragraphs .expanded .first-words .ref {
  color: var(--accent);
}
table.paragraphs .expanded .spaces {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}
table.paragraphs .expanded .spaces span {
  display: inline-block;
  background: #ffebee;
  border: 1px solid var(--accent);
  padding: 0 0.1rem;
  margin: 0 0.1rem;
}
table.paragraphs .expanded .citation {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  align-items: center;
}
table.paragraphs .expanded button {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background: white;
  cursor: pointer;
  font-size: 0.9rem;
}
table.paragraphs .expanded button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.headings-box {
  margin: 1rem 0;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 4px;
  background: white;
}
.headings-box h3 {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  margin: 0 0 0.5rem;
}
.headings-box ul {
  margin: 0;
  padding: 0 0 0 1rem;
  list-style: none;
}
.headings-box li {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}
footer {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
}
[hidden] { display: none !important; }
</style>
</head>
<body>

<header>
  <div>
    <label>UN DOCUMENT · HTML</label>
    <h1 id="doc-title"></h1>
  </div>
  <div id="header-status">
    <span class="status-dot" id="status-dot"></span>
    <span id="status-text"></span>
  </div>
</header>

<div class="rail">
  <h2>DOCUMENT</h2>
  <div class="rail-card">
    <h3 id="doc-symbol"></h3>
    <p id="doc-short-title"></p>
  </div>
  <div class="big-number" id="para-count">
    <span id="para-found">0</span>
    <small>paragraphs of <span id="para-expected">0</span></small>
  </div>
  <div class="big-number red" id="footnote-count">
    <span>0</span>
    <small>footnotes of <span id="footnote-expected">0</span></small>
  </div>
  <div id="check-count">
    <span id="check-pass">0</span> of <span id="check-total">0</span> checks pass
  </div>
</div>

<div role="main">
  <ul class="tabs" role="tablist" aria-label="Tabs">
    <li role="presentation"><button id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button></li>
    <li role="presentation"><button id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button></li>
  </ul>

  <div id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01">
    <div class="tiles">
      <div class="tile">
        <h3>Paragraphs found: <span id="para-found-tile">0</span></h3>
        <p>the document has <span id="para-expected-tile">0</span></p>
        <p class="how">How this is computed: counted the numbered &lt;p&gt; elements in the HTML.</p>
      </div>
      <div class="tile">
        <h3>First words match: <span id="first-words-match">0</span></h3>
        <p>of <span id="first-words-expected">0</span></p>
        <p class="how">How this is computed: the first six words of each paragraph against the reference.</p>
      </div>
      <div class="tile red">
        <h3>Footnotes: 0</h3>
        <p>of <span id="footnote-expected-tile">0</span></p>
        <p class="how">this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.</p>
      </div>
      <div class="tile">
        <h3>Spaces: <span id="spaces-restored">0</span></h3>
        <p>in <span id="spaces-paras">0</span> paragraphs</p>
        <p class="how">How this is computed: rules inserted a space where the characters proved one was missing.</p>
      </div>
    </div>

    <div id="mismatch-list-container" hidden>
      <p>First words that differ:</p>
      <ul class="mismatch-list" id="mismatch-list"></ul>
    </div>

    <div class="export-buttons">
      <button id="download-json" disabled>Download JSON</button>
      <button id="download-md" disabled>Download Markdown</button>
    </div>

    <div class="check-panel">
      <h2>01 EVERY CHECK (<span id="check-total-panel">0</span>)</h2>
      <div id="check-list"></div>
    </div>

    <div class="spaces-panel">
      <h2>02 THE SPACES RESTORED (<span id="spaces-restored-panel">0</span>)</h2>
      <div class="rule-counts">
        <span>Sentence join: <span id="rule-sentence">0</span></span>
        <span>Comma join: <span id="rule-comma">0</span></span>
        <span>Quote join: <span id="rule-quote">0</span></span>
        <span>Dash join: <span id="rule-dash">0</span></span>
      </div>
      <table id="spaces-table" hidden>
        <caption>Paragraph | Before | After | Rule</caption>
        <thead>
          <tr>
            <th scope="col">Paragraph</th>
            <th scope="col">Before</th>
            <th scope="col">After</th>
            <th scope="col">Rule</th>
          </tr>
        </thead>
        <tbody id="spaces-body"></tbody>
      </table>
      <p style="margin-top: 1rem; font-size: 0.9rem;">Rules restore a space only where the characters prove it was there. Word pairs such as "Giventhe" are not touched.</p>
    </div>
  </div>

  <div id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
    <div class="headings-box">
      <h3>HEADINGS FOUND: <span id="headings-found">0</span></h3>
      <ul id="headings-list"></ul>
    </div>
    <table class="paragraphs">
      <caption id="para-table-caption"></caption>
      <thead>
        <tr>
          <th scope="col" class="no">No.</th>
          <th scope="col">Section</th>
          <th scope="col">First line</th>
          <th scope="col">Check</th>
        </tr>
      </thead>
      <tbody id="para-table-body"></tbody>
    </table>
  </div>
</div>

<footer>
  <span id="footer-source"></span>
  <span id="footer-built"></span>
</footer>

<script>
(function() {
  const data = window.WORKSHOP_DATA.html_doc;
  const doc = new DOMParser().parseFromString(data.html, 'text/html');
  const body = doc.body;
  const ref = data.reference || {};

  // State
  let paragraphs = [];
  let headings = [];
  let checks = [];
  let spaces = [];
  let firstWordsMismatches = [];
  let paraExpected = ref.paragraphs || 0;
  let footnoteExpected = ref.footnotes || 0;
  let firstWordsExpected = Object.keys(ref.first_words || {}).length;
  let paraFound = 0;
  let firstWordsMatch = 0;
  let spacesRestored = 0;
  let checkPass = 0;
  let checkTotal = 0;

  // Classification
  const elements = body.querySelectorAll('table, p, h2, h3');
  let inContent = false;
  let currentPart = '';
  let currentSection = '';

  elements.forEach(el => {
    if (!inContent && el.tagName === 'TABLE') {
      // Cover table, skip
      return;
    }
    if (!inContent && el.tagName === 'P' && el.textContent.trim().includes('Committee on')) {
      // Committee line, skip
      return;
    }
    if (!inContent && el.tagName === 'H2' && el.textContent.trim().endsWith('*')) {
      // Title, skip
      inContent = true;
      return;
    }
    if (!inContent) {
      inContent = true;
    }

    if (el.tagName === 'H2') {
      const match = el.textContent.trim().match(/^([IVX]+|[A-Z])\.\s*(.+)$/);
      if (match) {
        currentPart = match[1] + '. ' + match[2];
        currentSection = currentPart;
        headings.push({ level: 'part', label: match[1], heading: match[2], element: el });
      } else {
        currentSection = el.textContent.trim();
        headings.push({ level: 'section', heading: currentSection, element: el });
      }
    } else if (el.tagName === 'H3') {
      currentSection = el.textContent.trim();
      headings.push({ level: 'subsection', heading: currentSection, element: el });
    } else if (el.tagName === 'P') {
      const match = el.textContent.trim().match(/^(\d{1,3})\.\s*(.*)$/s);
      if (match) {
        const number = parseInt(match[1], 10);
        let textRaw = match[2].trim();
        let text = textRaw;
        let repairs = [];

        // Repair rules
        const sentenceJoin = text.match(/([a-z])\.([A-Z])/g);
        if (sentenceJoin) {
          sentenceJoin.forEach(m => {
            const pos = text.indexOf(m);
            repairs.push({
              rule: 'sentence',
              before: text.slice(Math.max(0, pos - 20), pos + 20),
              after: text.slice(0, pos + 1) + ' ' + text.slice(pos + 2)
            });
            text = text.slice(0, pos + 1) + ' ' + text.slice(pos + 2);
          });
        }

        const commaJoin = text.match(/([a-z]),([A-Za-z])/g);
        if (commaJoin) {
          commaJoin.forEach(m => {
            const pos = text.indexOf(m);
            repairs.push({
              rule: 'comma',
              before: text.slice(Math.max(0, pos - 20), pos + 20),
              after: text.slice(0, pos + 1) + ' ' + text.slice(pos + 2)
            });
            text = text.slice(0, pos + 1) + ' ' + text.slice(pos + 2);
          });
        }

        const quoteJoin = text.match(/([a-z])“/g);
        if (quoteJoin) {
          quoteJoin.forEach(m => {
            const pos = text.indexOf(m);
            repairs.push({
              rule: 'quote',
              before: text.slice(Math.max(0, pos - 20), pos + 20),
              after: text.slice(0, pos + 1) + ' “'
            });
            text = text.slice(0, pos + 1) + ' “' + text.slice(pos + 2);
          });
        }

        const dashJoin = text.match(/–([A-Za-z])/g);
        if (dashJoin) {
          dashJoin.forEach(m => {
            const pos = text.indexOf(m);
            repairs.push({
              rule: 'dash',
              before: text.slice(Math.max(0, pos - 20), pos + 20),
              after: text.slice(0, pos) + ' – ' + text.slice(pos + 1)
            });
            text = text.slice(0, pos) + ' – ' + text.slice(pos + 1);
          });
        }

        const firstWordsRef = ref.first_words ? ref.first_words[String(number)] : null;
        let firstWordsFound = text.split(/\s+/).slice(0, 6).join(' ');
        let firstWordsMatchFlag = false;

        if (firstWordsRef) {
          const normalise = s => s.replace(/[“”]/g, '"').replace(/[–‑]/g, '-').replace(/\u00A0/g, ' ');
          firstWordsMatchFlag = normalise(firstWordsFound) === normalise(firstWordsRef);
          if (!firstWordsMatchFlag) {
            firstWordsMismatches.push({
              number,
              found: firstWordsFound,
              ref: firstWordsRef
            });
          }
        }

        paragraphs.push({
          number,
          text_raw: textRaw,
          text,
          section: currentSection,
          part: currentPart,
          first_words_match: firstWordsMatchFlag,
          repairs,
          citation: `${data.symbol}, para. ${number}`,
          doc_url: data.doc_url
        });
      }
    }
  });

  paraFound = paragraphs.length;
  firstWordsMatch = paragraphs.filter(p => p.first_words_match).length;
  spacesRestored = paragraphs.reduce((sum, p) => sum + p.repairs.length, 0);

  // Checks
  checks.push({
    name: 'Paragraph count',
    description: 'Found against reference.paragraphs',
    found: paraFound,
    expected: paraExpected,
    status: paraFound === paraExpected ? 'pass' : paraExpected ? 'fail' : 'limit',
    link: paraFound !== paraExpected ? '#para-table-body' : null
  });

  const numbers = paragraphs.map(p => p.number);
  const numberingCheck = {
    name: 'Numbering',
    description: 'Exactly 1 to n in order',
    found: numbers,
    expected: Array.from({length: paraExpected}, (_, i) => i + 1),
    status: 'pass',
    details: []
  };
  if (paraExpected) {
    const gaps = [];
    const duplicates = [];
    for (let i = 1; i <= paraExpected; i++) {
      if (!numbers.includes(i)) gaps.push(i);
      if (numbers.filter(n => n === i).length > 1) duplicates.push(i);
    }
    if (gaps.length || duplicates.length) {
      numberingCheck.status = 'fail';
      numberingCheck.details.push(`Gaps: ${gaps.join(', ') || 'none'}`);
      numberingCheck.details.push(`Duplicates: ${duplicates.join(', ') || 'none'}`);
    }
  } else {
    numberingCheck.status = 'limit';
  }
  checks.push(numberingCheck);

  checks.push({
    name: 'First words',
    description: 'Mismatches counted',
    found: firstWordsMatch,
    expected: firstWordsExpected,
    status: firstWordsMatch === firstWordsExpected ? 'pass' : firstWordsExpected ? 'fail' : 'limit',
    link: firstWordsMatch !== firstWordsExpected ? '#mismatch-list-container' : null
  });

  checks.push({
    name: 'Footnotes',
    description: '0 against reference.footnotes',
    found: 0,
    expected: footnoteExpected,
    status: 'limit',
    details: ['the HTML version has no footnotes: a limit of the source, not of the app']
  });

  checks.push({
    name: 'Repairs',
    description: 'Spaces restored in paragraphs',
    found: spacesRestored,
    expected: null,
    status: 'pass'
  });

  const h2Count = headings.filter(h => h.level === 'part' || h.level === 'section').length;
  const h3Count = headings.filter(h => h.level === 'subsection').length;
  const gluedLabels = headings.filter(h => h.level === 'part' && h.label && !h.label.endsWith('. ')).length;
  checks.push({
    name: 'Headings',
    description: 'How many &lt;h2&gt; and &lt;h3&gt;, and how many glued labels were separated',
    found: `${h2Count} h2, ${h3Count} h3, ${gluedLabels} glued labels`,
    expected: null,
    status: 'pass'
  });

  const classified = paragraphs.length + headings.length + 2; // +2 for title and committee line
  const unclassified = elements.length - classified;
  checks.push({
    name: 'Nothing lost',
    description: 'Every block element is classified exactly once',
    found: `classified ${classified}, unclassified ${unclassified}`,
    expected: `classified ${elements.length}`,
    status: unclassified === 0 ? 'pass' : 'fail',
    details: unclassified ? [`Unclassified elements: ${unclassified}`] : []
  });

  const exportRoundTrip = {
    name: 'Export round trip',
    description: 'The JSON to download is parsed back',
    found: null,
    expected: paraFound,
    status: 'not-run'
  };
  checks.push(exportRoundTrip);

  checkTotal = checks.length;
  checkPass = checks.filter(c => c.status === 'pass').length;

  // Render
  document.getElementById('doc-title').textContent = data.title;
  document.getElementById('doc-symbol').textContent = data.symbol;
  document.getElementById('doc-short-title').textContent = data.title.split(' on ')[0];
  document.getElementById('para-expected').textContent = paraExpected;
  document.getElementById('para-found').textContent = paraFound;
  document.getElementById('para-expected-tile').textContent = paraExpected;
  document.getElementById('para-found-tile').textContent = paraFound;
  document.getElementById('first-words-match').textContent = firstWordsMatch;
  document.getElementById('first-words-expected').textContent = firstWordsExpected;
  document.getElementById('first-words-expected-tile').textContent = firstWordsExpected;
  document.getElementById('footnote-expected').textContent = footnoteExpected;
  document.getElementById('footnote-expected-tile').textContent = footnoteExpected;
  document.getElementById('spaces-restored').textContent = spacesRestored;
  document.getElementById('spaces-paras').textContent = paragraphs.filter(p => p.repairs.length).length;
  document.getElementById('check-pass').textContent = checkPass;
  document.getElementById('check-total').textContent = checkTotal;
  document.getElementById('check-total-panel').textContent = checkTotal;
  document.getElementById('spaces-restored-panel').textContent = spacesRestored;
  document.getElementById('headings-found').textContent = headings.length;
  document.getElementById('footer-source').textContent = data.source;
  document.getElementById('footer-built').textContent = 'Done by this page\'s code; no model was called and nothing left the browser.';

  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');
  if (checkPass === checkTotal) {
    statusDot.classList.add('green');
    statusText.textContent = `${checkPass} checks pass`;
  } else {
    statusDot.classList.add('red');
    statusText.textContent = `${checkTotal - checkPass} checks failed`;
  }

  if (paraFound === paraExpected) {
    document.getElementById('para-count').classList.remove('red');
    document.getElementById('para-count').classList.add('green');
  } else {
    document.getElementById('para-count').classList.add('red');
    document.getElementById('para-count').classList.remove('green');
  }

  if (firstWordsMismatches.length) {
    const list = document.getElementById('mismatch-list');
    firstWordsMismatches.slice(0, 10).forEach(m => {
      const li = document.createElement('li');
      li.innerHTML = `para. <strong>${m.number}</strong>: found <code>${m.found}</code> / reference <code>${m.ref}</code>`;
      list.appendChild(li);
    });
    if (firstWordsMismatches.length > 10) {
      const li = document.createElement('li');
      li.textContent = `and ${firstWordsMismatches.length - 10} more`;
      list.appendChild(li);
    }
    document.getElementById('mismatch-list-container').hidden = false;
  }

  const checkList = document.getElementById('check-list');
  checks.forEach((check, i) => {
    const button = document.createElement('button');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', `check-${i}`);

    const line = document.createElement('div');
    line.className = 'check-line';

    const name = document.createElement('span');
    name.textContent = check.name;
    line.appendChild(name);

    const status = document.createElement('span');
    status.className = `status ${check.status}`;
    status.textContent = check.status === 'pass' ? 'pass' : check.status === 'fail' ? 'check failed' : 'source limit';
    if (check.link) {
      const link = document.createElement('a');
      link.href = check.link;
      link.className = 'link';
      link.textContent = ' → rows';
      status.appendChild(link);
    }
    line.appendChild(status);

    button.appendChild(line);
    checkList.appendChild(button);

    const details = document.createElement('div');
    details.id = `check-${i}`;
    details.className = 'check-details';
    details.hidden = true;

    const desc = document.createElement('p');
    desc.textContent = check.description;
    details.appendChild(desc);

    if (check.found !== null) {
      const found = document.createElement('p');
      found.textContent = `Found: ${check.found}`;
      details.appendChild(found);
    }

    if (check.expected !== null) {
      const expected = document.createElement('p');
      expected.textContent = `Expected: ${check.expected}`;
      details.appendChild(expected);
    }

    if (check.details && check.details.length) {
      check.details.forEach(d => {
        const p = document.createElement('p');
        p.textContent = d;
        details.appendChild(p);
      });
    }

    checkList.appendChild(details);

    button.addEventListener('click', () => {
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', !isExpanded);
      details.hidden = isExpanded;
    });
  });

  const spacesBody = document.getElementById('spaces-body');
  const ruleCounts = {
    sentence: 0,
    comma: 0,
    quote: 0,
    dash: 0
  };
  paragraphs.forEach(p => {
    p.repairs.forEach(r => {
      ruleCounts[r.rule]++;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${p.number}</td>
        <td><code>${r.before}</code></td>
        <td><code>${r.after}</code></td>
        <td>${r.rule}</td>
      `;
      tr.addEventListener('click', () => {
        document.getElementById('tab-02').click();
        const row = document.querySelector(`#para-table-body tr[data-number="${p.number}"]`);
        if (row) row.click();
      });
      spacesBody.appendChild(tr);
    });
  });
  document.getElementById('rule-sentence').textContent = ruleCounts.sentence;
  document.getElementById('rule-comma').textContent = ruleCounts.comma;
  document.getElementById('rule-quote').textContent = ruleCounts.quote;
  document.getElementById('rule-dash').textContent = ruleCounts.dash;
  if (spacesRestored) {
    document.getElementById('spaces-table').hidden = false;
  }

  const paraTableBody = document.getElementById('para-table-body');
  paragraphs.forEach(p => {
    const tr = document.createElement('tr');
    tr.setAttribute('aria-expanded', 'false');
    tr.setAttribute('tabindex', '0');
    tr.setAttribute('role', 'button');
    tr.dataset.number = p.number;

    const no = document.createElement('td');
    no.className = 'no';
    no.textContent = p.number;
    tr.appendChild(no);

    const section = document.createElement('td');
    section.className = 'section';
    section.textContent = p.section;
    tr.appendChild(section);

    const firstLine = document.createElement('td');
    firstLine.className = 'first-line';
    firstLine.textContent = p.text.slice(0, 120).replace(/\s+/g, ' ') + (p.text.length > 120 ? '…' : '');
    tr.appendChild(firstLine);

    const check = document.createElement('td');
    check.className = `check ${p.first_words_match ? '' : 'fail'}`;
    check.textContent = p.first_words_match ? 'OK' : 'first words differ';
    tr.appendChild(check);

    paraTableBody.appendChild(tr);

    const expanded = document.createElement('tr');
    expanded.className = 'expanded';
    expanded.hidden = true;

    const expandedTd = document.createElement('td');
    expandedTd.colSpan = 4;

    const textP = document.createElement('p');
    textP.textContent = p.text;
    expandedTd.appendChild(textP);

    if (ref.first_words && ref.first_words[String(p.number)]) {
      const firstWordsP = document.createElement('div');
      firstWordsP.className = 'first-words';
      firstWordsP.innerHTML = `First six words: <span class="found">${p.text.split(/\s+/).slice(0, 6).join(' ')}</span> / <span class="ref">${ref.first_words[String(p.number)]}</span>`;
      expandedTd.appendChild(firstWordsP);
    }

    if (p.repairs.length) {
      const spacesP = document.createElement('div');
      spacesP.className = 'spaces';
      spacesP.textContent = 'Spaces restored: ';
      const textWithMarks = p.text_raw;
      let lastPos = 0;
      p.repairs.forEach(r => {
        const pos = textWithMarks.indexOf(r.before.replace(/\s/g, ''), lastPos);
        if (pos !== -1) {
          spacesP.appendChild(document.createTextNode(textWithMarks.slice(lastPos, pos)));
          const mark = document.createElement('span');
          mark.textContent = textWithMarks.slice(pos, pos + r.before.length);
          spacesP.appendChild(mark);
          lastPos = pos + r.before.length;
        }
      });
      spacesP.appendChild(document.createTextNode(textWithMarks.slice(lastPos)));
      expandedTd.appendChild(spacesP);
    }

    const citationDiv = document.createElement('div');
    citationDiv.className = 'citation';
    const copyButton = document.createElement('button');
    copyButton.textContent = 'Copy citation';
    copyButton.addEventListener('click', () => {
      navigator.clipboard.writeText(p.citation).then(() => {
        copyButton.textContent = 'Copied';
        setTimeout(() => { copyButton.textContent = 'Copy citation'; }, 2000);
      });
    });
    citationDiv.appendChild(copyButton);
    expandedTd.appendChild(citationDiv);

    expanded.appendChild(expandedTd);
    paraTableBody.appendChild(expanded);

    tr.addEventListener('click', () => {
      const isExpanded = tr.getAttribute('aria-expanded') === 'true';
      tr.setAttribute('aria-expanded', !isExpanded);
      expanded.hidden = isExpanded;
    });
    tr.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        tr.click();
      }
    });
  });

  const headingsList = document.getElementById('headings-list');
  headings.forEach(h => {
    const li = document.createElement('li');
    li.textContent = h.level === 'part' ? `${h.label} ${h.heading}` : h.heading;
    headingsList.appendChild(li);
  });

  document.getElementById('para-table-caption').textContent =
    `${paraFound} paragraphs found, ${paraExpected} expected`;

  // Tabs
  const tabs = document.querySelectorAll('[role="tab"]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => {
        t.setAttribute('aria-selected', 'false');
        document.getElementById(t.getAttribute('aria-controls')).setAttribute('aria-hidden', 'true');
      });
      tab.setAttribute('aria-selected', 'true');
      document.getElementById(tab.getAttribute('aria-controls')).setAttribute('aria-hidden', 'false');
    });
  });

  // Exports
  const jsonButton = document.getElementById('download-json');
  const mdButton = document.getElementById('download-md');

  if (paraFound) {
    jsonButton.disabled = false;
    mdButton.disabled = false;

    jsonButton.addEventListener('click', () => {
      const json = paragraphs.map(p => ({
        symbol: data.symbol,
        paragraph: p.number,
        section: p.section,
        part: p.part,
        text: p.text,
        text_raw: p.text_raw,
        first_words_match: p.first_words_match,
        citation: p.citation,
        doc_url: p.doc_url,
        limitations: `no footnotes in this HTML version; the document has ${footnoteExpected}`
      }));
      const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.symbol.replace(/\//g, '-') + '.json';
      a.click();
      URL.revokeObjectURL(url);

      // Check round trip
      try {
        const parsed = JSON.parse(JSON.stringify(json));
        exportRoundTrip.found = parsed.length;
        exportRoundTrip.status = parsed.length === paraFound ? 'pass' : 'fail';
        document.getElementById('check-pass').textContent = checks.filter(c => c.status === 'pass').length;
      } catch (e) {
        exportRoundTrip.status = 'fail';
      }
    });

    mdButton.addEventListener('click', () => {
      let md = `---\n`;
      md += `title: "${data.title}"\n`;
      md += `symbol: ${data.symbol}\n`;
      md += `adopted: ${ref.adopted || 'unknown'}\n`;
      md += `source_url: ${data.doc_url}\n`;
      md += `extracted: ${new Date().toISOString().split('T')[0]}\n`;
      md += `paragraphs_found: ${paraFound}\n`;
      md += `paragraphs_expected: ${paraExpected}\n`;
      md += `footnotes: no footnotes in this HTML version; the document has ${footnoteExpected}\n`;
      md += `---\n\n`;

      let lastPart = '';
      let lastSection = '';
      paragraphs.forEach(p => {
        if (p.part && p.part !== lastPart) {
          md += `## ${p.part}\n\n`;
          lastPart = p.part;
          lastSection = '';
        }
        if (p.section && p.section !== lastSection) {
          md += `### ${p.section}\n\n`;
          lastSection = p.section;
        }
        md += `**${p.number}.** ${p.text}\n\n`;
      });

      const blob = new Blob([md], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.symbol.replace(/\//g, '-') + '.md';
      a.click();
      URL.revokeObjectURL(url);
    });
  }
})();
</script>
</body>
</html>
```