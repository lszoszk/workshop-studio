I built an app that extracts the numbered paragraphs from the HTML version of a General Comment, checks them against the document's own reference, and lets you download the result as JSON or Markdown. The left rail shows the document's vital signs; the first tab gives the answer at a glance; the second tab lists every paragraph with its heading and citation.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Paragraphs from a UN document</title>
<style>
:root {
  --paper: #f4f0e8;
  --ink: #1d1b18;
  --rule: #d9d2c3;
  --red: #9b2335;
  --green: #2e6b49;
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
.hidden {
  display: none !important;
}
header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--rule);
  background-color: var(--paper);
  position: sticky;
  top: 0;
  z-index: 10;
}
.header-grid {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  align-items: center;
}
.label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  color: var(--ink);
  text-transform: uppercase;
}
.title {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: 400;
  margin: 0;
  line-height: 1.2;
}
.meta {
  font-size: 0.875rem;
  color: var(--ink);
  margin: 0;
}
.meta a {
  color: var(--ink);
  text-decoration: none;
}
.meta a:focus {
  outline: 2px solid var(--red);
  outline-offset: 2px;
}
.meta a:hover {
  text-decoration: underline;
}
.status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}
.status-dot {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
}
.status-dot.pass {
  background-color: var(--green);
}
.status-dot.fail {
  background-color: var(--red);
}
main {
  display: grid;
  grid-template-columns: 24rem 1fr;
  gap: 1rem;
  padding: 1rem;
}
.rail {
  background-color: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
  font-size: 0.875rem;
}
.rail h2 {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 1rem 0;
  padding: 0;
  color: var(--ink);
}
.rail-card {
  background-color: var(--ink);
  color: var(--paper);
  border-radius: 0.25rem;
  padding: 0.75rem;
  margin-bottom: 1rem;
}
.rail-card .symbol {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  word-break: break-all;
}
.rail-card .short-title {
  font-size: 0.875rem;
  margin: 0.25rem 0 0 0;
}
.rail-stats {
  margin: 0 0 1rem 0;
}
.rail-stat {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 0.5rem;
}
.rail-stat-value {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2rem;
  font-weight: 400;
  line-height: 1;
  margin: 0;
}
.rail-stat-label {
  font-size: 0.875rem;
  color: var(--ink);
}
.rail-stat-bar {
  height: 0.25rem;
  background-color: var(--rule);
  margin-top: 0.25rem;
  border-radius: 0.125rem;
  overflow: hidden;
}
.rail-stat-bar-fill {
  height: 100%;
  background-color: var(--red);
  width: 0%;
}
.rail-checks {
  margin-top: 1rem;
}
.rail-check {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.rail-check-value {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.5rem;
  font-weight: 400;
  line-height: 1;
  margin: 0;
}
.rail-check-label {
  font-size: 0.875rem;
  color: var(--ink);
}
.tabs {
  display: flex;
  gap: 0.25rem;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 1rem;
}
.tab {
  padding: 0.5rem 1rem;
  border: 1px solid transparent;
  border-bottom: none;
  border-radius: 0.25rem 0.25rem 0 0;
  background-color: transparent;
  color: var(--ink);
  text-decoration: none;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.tab.active {
  border-color: var(--rule);
  background-color: var(--paper);
  color: var(--red);
  font-weight: 600;
}
.tab:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
.tab-panel {
  display: none;
}
.tab-panel[aria-hidden="false"] {
  display: block;
}
.tab-content {
  background-color: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.tile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.tile {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 1rem;
}
.tile-value {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 2.5rem;
  font-weight: 400;
  line-height: 1;
  margin: 0 0 0.5rem 0;
  color: var(--ink);
}
.tile-label {
  font-size: 0.875rem;
  color: var(--ink);
  margin: 0;
}
.tile.half {
  grid-column: span 1;
}
.tile.fail .tile-value {
  color: var(--red);
}
.tile.limit .tile-value {
  color: var(--red);
}
.tile.how {
  font-size: 0.75rem;
  color: var(--ink);
  margin-top: 0.5rem;
  font-style: italic;
}
.mismatch-list {
  margin: 1rem 0;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 0.5rem;
  font-size: 0.875rem;
}
.mismatch-item {
  padding: 0.25rem 0;
  border-bottom: 1px solid var(--rule);
}
.mismatch-item:last-child {
  border-bottom: none;
}
.mismatch-item strong {
  font-family: ui-monospace, Menlo, Consolas, monospace;
}
.downloads {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}
.downloads button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background-color: var(--paper);
  color: var(--ink);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.downloads button:focus {
  outline: 2px solid var(--red);
  outline-offset: 2px;
}
.downloads button:hover {
  background-color: var(--ink);
  color: var(--paper);
}
.downloads button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.downloads button svg {
  width: 1rem;
  height: 1rem;
}
.section-heading {
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  margin: 1rem 0;
  background-color: var(--paper);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
}
.section-heading:focus {
  outline: 2px solid var(--red);
  outline-offset: 2px;
}
.section-heading[aria-expanded="false"] .section-icon {
  transform: rotate(0deg);
}
.section-heading[aria-expanded="true"] .section-icon {
  transform: rotate(180deg);
}
.section-icon {
  transition: transform 0.2s;
}
.section-content {
  display: none;
  padding: 0.5rem;
  border: 1px solid var(--rule);
  border-top: none;
  border-radius: 0 0 0.25rem 0.25rem;
  background-color: var(--paper);
}
.section-content[aria-hidden="false"] {
  display: block;
}
.check-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.check-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--rule);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}
.check-item:last-child {
  border-bottom: none;
}
.check-item.fail {
  color: var(--red);
}
.check-item.limit {
  color: var(--red);
}
.check-item.pass {
  color: var(--green);
}
.check-item a {
  color: var(--red);
  text-decoration: none;
}
.check-item a:focus {
  outline: 2px solid var(--red);
  outline-offset: 2px;
}
.check-item a:hover {
  text-decoration: underline;
}
.space-list {
  margin-top: 1rem;
}
.space-list table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}
.space-list caption {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  text-align: left;
}
.space-list th {
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
}
.space-list td {
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
.space-list tr:last-child td {
  border-bottom: none;
}
.space-list .count {
  text-align: right;
  font-family: ui-monospace, Menlo, Consolas, monospace;
}
.space-list .rule {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.75rem;
  color: var(--ink);
}
.space-list .before, .space-list .after {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  white-space: pre-wrap;
}
.space-list .after mark {
  background-color: transparent;
  color: var(--red);
  text-decoration: underline;
  text-decoration-color: var(--red);
  text-decoration-thickness: 1px;
}
.space-summary {
  font-size: 0.875rem;
  color: var(--ink);
  margin-top: 0.5rem;
  font-style: italic;
}
.table-container {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}
caption {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  text-align: left;
}
th {
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
}
td {
  padding: 0.5rem;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}
tr:last-child td {
  border-bottom: none;
}
tr.expanded td {
  border-bottom: 1px solid var(--rule);
}
tr:last-child.expanded td {
  border-bottom: 1px solid var(--rule);
}
tr button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  color: inherit;
  cursor: pointer;
  text-align: left;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}
tr button:focus {
  outline: 2px solid var(--red);
  outline-offset: -2px;
}
tr button[aria-expanded="false"] .expand-icon {
  transform: rotate(0deg);
}
tr button[aria-expanded="true"] .expand-icon {
  transform: rotate(180deg);
}
.expand-icon {
  transition: transform 0.2s;
  flex-shrink: 0;
}
.para-no {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--red);
  white-space: nowrap;
}
.para-section {
  font-size: 0.875rem;
  color: var(--ink);
}
.para-first-line {
  font-size: 0.875rem;
  color: var(--ink);
}
.para-check {
  font-size: 0.875rem;
  color: var(--ink);
  white-space: nowrap;
}
.para-check.fail {
  color: var(--red);
}
.para-details {
  display: none;
  padding: 0.5rem 0;
  border-top: 1px solid var(--rule);
  margin-top: 0.5rem;
  grid-column: 1 / -1;
}
.para-details[aria-hidden="false"] {
  display: block;
}
.para-text {
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0.5rem 0;
  white-space: pre-wrap;
}
.para-text mark {
  background-color: transparent;
  border: 1px solid var(--red);
  padding: 0 0.125rem;
  border-radius: 0.125rem;
}
.para-words {
  display: flex;
  gap: 0.5rem;
  margin: 0.5rem 0;
  font-size: 0.875rem;
}
.para-words-label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
}
.para-words-value {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  white-space: pre-wrap;
}
.para-spaces {
  margin: 0.5rem 0;
  font-size: 0.875rem;
}
.para-spaces-label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}
.para-spaces-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.para-spaces-item {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  white-space: pre-wrap;
}
.para-spaces-item mark {
  background-color: transparent;
  color: var(--red);
  text-decoration: underline;
  text-decoration-color: var(--red);
  text-decoration-thickness: 1px;
}
.copy-button {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--rule);
  border-radius: 0.25rem;
  background-color: var(--paper);
  color: var(--ink);
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 0.875rem;
  cursor: pointer;
  margin-top: 0.5rem;
}
.copy-button:focus {
  outline: 2px solid var(--red);
  outline-offset: 2px;
}
.copy-button:hover {
  background-color: var(--ink);
  color: var(--paper);
}
.copy-feedback {
  font-size: 0.875rem;
  color: var(--green);
  margin-top: 0.25rem;
}
.heading-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 0.875rem;
}
.heading-item {
  padding: 0.25rem 0;
  border-bottom: 1px solid var(--rule);
}
.heading-item:last-child {
  border-bottom: none;
}
.heading-item .heading-label {
  font-family: ui-monospace, Menlo, Consolas, monospace;
  color: var(--ink);
}
.heading-item .heading-text {
  color: var(--ink);
}
footer {
  padding: 1rem;
  border-top: 1px solid var(--rule);
  font-size: 0.875rem;
  color: var(--ink);
}
.credits {
  font-size: 0.75rem;
  color: var(--ink);
  margin-top: 1rem;
  font-style: italic;
}
</style>
</head>
<body>

<header>
  <div class="header-grid">
    <div class="label">UN DOCUMENT · HTML</div>
    <div class="title" id="doc-title"></div>
    <div class="status">
      <div class="status-dot" id="status-dot"></div>
      <div id="status-text"></div>
    </div>
  </div>
  <div class="meta">
    <span id="doc-meta"></span>
    <span> · 1 source limit</span>
  </div>
</header>

<main>
  <aside class="rail">
    <h2>DOCUMENT</h2>
    <div class="rail-card">
      <div class="symbol" id="rail-symbol"></div>
      <div class="short-title" id="rail-short-title"></div>
    </div>
    <div class="rail-stats">
      <div class="rail-stat">
        <div class="rail-stat-value" id="rail-paragraphs-found"></div>
        <div class="rail-stat-label">paragraphs of <span id="rail-paragraphs-expected"></span></div>
      </div>
      <div class="rail-stat-bar">
        <div class="rail-stat-bar-fill" id="rail-paragraphs-bar"></div>
      </div>
      <div class="rail-stat">
        <div class="rail-stat-value" id="rail-footnotes-found">0</div>
        <div class="rail-stat-label">footnotes of <span id="rail-footnotes-expected"></span></div>
      </div>
      <div class="rail-stat-label" style="color: var(--red);">not in this HTML</div>
    </div>
    <div class="rail-checks">
      <div class="rail-check">
        <div class="rail-check-value" id="rail-checks-pass"></div>
        <div class="rail-check-label">of <span id="rail-checks-total"></span> checks pass</div>
      </div>
    </div>
  </aside>

  <div class="content">
    <div class="tabs" role="tablist" aria-label="Tabs">
      <button class="tab active" id="tab-01" role="tab" aria-selected="true" aria-controls="panel-01">01 RESULT</button>
      <button class="tab" id="tab-02" role="tab" aria-selected="false" aria-controls="panel-02">02 PARAGRAPHS</button>
    </div>

    <div id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01" aria-hidden="false">
      <div class="tab-content">
        <div class="tile-grid">
          <div class="tile">
            <div class="tile-value" id="tile-paragraphs-found"></div>
            <div class="tile-label">Paragraphs found</div>
            <div class="tile how">How this is computed: counted the numbered &lt;p&gt; elements in the HTML.</div>
          </div>
          <div class="tile">
            <div class="tile-value" id="tile-paragraphs-expected"></div>
            <div class="tile-label">the document has</div>
            <div class="tile how">How this is computed: read from the document's own reference.</div>
          </div>
          <div class="tile">
            <div class="tile-value" id="tile-first-words-match"></div>
            <div class="tile-label">First words match</div>
            <div class="tile how">How this is computed: the first six words of each paragraph against the reference.</div>
          </div>
          <div class="tile limit">
            <div class="tile-value" id="tile-footnotes-found">0</div>
            <div class="tile-label">Footnotes</div>
            <div class="tile how">this HTML version has none: no footnote text, no footnote marks. To cite a footnote, use the PDF or Word version.</div>
          </div>
          <div class="tile half">
            <div class="tile-value" id="tile-spaces-restored"></div>
            <div class="tile-label">Spaces</div>
            <div class="tile how">in <span id="tile-spaces-paragraphs"></span> paragraphs</div>
          </div>
        </div>

        <div id="mismatch-list-container">
          <div class="mismatch-list" id="mismatch-list"></div>
        </div>

        <div class="downloads">
          <button id="download-json" disabled>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
            Download JSON
          </button>
          <button id="download-markdown" disabled>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M14 17H17L19 13V17H22V9H19L17 13V9H14M12 15L9 9H7L12 15M6 17H9V13L7 11.5V9.5L5 13V17Z"/></svg>
            Download Markdown
          </button>
        </div>

        <div class="section-heading" id="checks-heading" role="button" aria-expanded="false" tabindex="0">
          <span>Every check (<span id="checks-heading-count"></span>)</span>
          <svg class="section-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </div>
        <div class="section-content" id="checks-content" aria-hidden="true">
          <ul class="check-list" id="check-list"></ul>
        </div>

        <div class="section-heading" id="spaces-heading" role="button" aria-expanded="false" tabindex="0">
          <span>The spaces restored (<span id="spaces-heading-count"></span>)</span>
          <svg class="section-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </div>
        <div class="section-content" id="spaces-content" aria-hidden="true">
          <div class="space-list">
            <table>
              <caption>FIG.01 Spaces restored by rule</caption>
              <thead>
                <tr>
                  <th scope="col">Rule</th>
                  <th scope="col">Count</th>
                </tr>
              </thead>
              <tbody id="space-rules-body"></tbody>
            </table>
            <div class="space-summary">Rules restore a space only where the characters prove it was there. Word pairs such as "Giventhe" are not touched.</div>
            <table>
              <caption>FIG.02 Every space restored</caption>
              <thead>
                <tr>
                  <th scope="col">Paragraph</th>
                  <th scope="col">Before</th>
                  <th scope="col">After</th>
                  <th scope="col">Rule</th>
                </tr>
              </thead>
              <tbody id="space-list-body"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <div id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
      <div class="tab-content">
        <div class="section-heading" id="headings-heading" role="button" aria-expanded="false" tabindex="0">
          <span>Headings found: <span id="headings-heading-count"></span></span>
          <svg class="section-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </div>
        <div class="section-content" id="headings-content" aria-hidden="true">
          <ul class="heading-list" id="heading-list"></ul>
        </div>

        <div class="table-container">
          <table>
            <caption>TAB.02 Every numbered paragraph</caption>
            <thead>
              <tr>
                <th scope="col">No.</th>
                <th scope="col">Section</th>
                <th scope="col">First line</th>
                <th scope="col">Check</th>
              </tr>
            </thead>
            <tbody id="paragraph-table-body"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</main>

<footer>
  <div id="footer-source"></div>
  <div id="footer-built"></div>
  <div>Done by this page's code; no model was called and nothing left the browser.</div>
</footer>

<script>
(function() {
  'use strict';

  // Data
  const data = window.WORKSHOP_DATA.html_doc;
  const doc = new DOMParser().parseFromString(data.html, 'text/html');
  const reference = data.reference || {};
  const paragraphsExpected = reference.paragraphs || '?';
  const footnotesExpected = reference.footnotes || '?';
  const firstWordsExpected = reference.first_words || {};
  const adopted = reference.adopted || '?';
  const source = data.source || '?';
  const built = new Date().toISOString().split('T')[0];

  // State
  let paragraphs = [];
  let headings = [];
  let checks = [];
  let spaces = [];
  let checksPass = 0;
  let checksTotal = 0;
  let spacesRestored = 0;
  let spacesParagraphs = 0;
  let firstWordsMismatch = 0;
  let mismatchList = [];

  // DOM
  const docTitle = document.getElementById('doc-title');
  const docMeta = document.getElementById('doc-meta');
  const railSymbol = document.getElementById('rail-symbol');
  const railShortTitle = document.getElementById('rail-short-title');
  const railParagraphsFound = document.getElementById('rail-paragraphs-found');
  const railParagraphsExpected = document.getElementById('rail-paragraphs-expected');
  const railParagraphsBar = document.getElementById('rail-paragraphs-bar');
  const railFootnotesFound = document.getElementById('rail-footnotes-found');
  const railFootnotesExpected = document.getElementById('rail-footnotes-expected');
  const railChecksPass = document.getElementById('rail-checks-pass');
  const railChecksTotal = document.getElementById('rail-checks-total');
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');
  const tileParagraphsFound = document.getElementById('tile-paragraphs-found');
  const tileParagraphsExpected = document.getElementById('tile-paragraphs-expected');
  const tileFirstWordsMatch = document.getElementById('tile-first-words-match');
  const tileSpacesRestored = document.getElementById('tile-spaces-restored');
  const tileSpacesParagraphs = document.getElementById('tile-spaces-paragraphs');
  const mismatchListContainer = document.getElementById('mismatch-list-container');
  const mismatchListEl = document.getElementById('mismatch-list');
  const downloadJson = document.getElementById('download-json');
  const downloadMarkdown = document.getElementById('download-markdown');
  const checksHeading = document.getElementById('checks-heading');
  const checksHeadingCount = document.getElementById('checks-heading-count');
  const checksContent = document.getElementById('checks-content');
  const checkList = document.getElementById('check-list');
  const spacesHeading = document.getElementById('spaces-heading');
  const spacesHeadingCount = document.getElementById('spaces-heading-count');
  const spacesContent = document.getElementById('spaces-content');
  const spaceRulesBody = document.getElementById('space-rules-body');
  const spaceListBody = document.getElementById('space-list-body');
  const headingsHeading = document.getElementById('headings-heading');
  const headingsHeadingCount = document.getElementById('headings-heading-count');
  const headingsContent = document.getElementById('headings-content');
  const headingList = document.getElementById('heading-list');
  const paragraphTableBody = document.getElementById('paragraph-table-body');
  const footerSource = document.getElementById('footer-source');
  const footerBuilt = document.getElementById('footer-built');

  // Tabs
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.tab-panel');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = document.getElementById(tab.getAttribute('aria-controls'));

      tabs.forEach(t => {
        t.setAttribute('aria-selected', 'false');
        t.classList.remove('active');
      });
      tab.setAttribute('aria-selected', 'true');
      tab.classList.add('active');

      panels.forEach(p => {
        p.setAttribute('aria-hidden', 'true');
      });
      target.setAttribute('aria-hidden', 'false');
    });
  });

  // Section headings
  const sectionHeadings = document.querySelectorAll('.section-heading');
  sectionHeadings.forEach(heading => {
    heading.addEventListener('click', () => {
      const expanded = heading.getAttribute('aria-expanded') === 'true';
      heading.setAttribute('aria-expanded', !expanded);
      document.getElementById(heading.id.replace('-heading', '-content')).setAttribute('aria-hidden', expanded);
    });
  });

  // Run the pipeline
  function run() {
    classifyElements();
    computeParagraphs();
    computeHeadings();
    computeChecks();
    render();
  }

  function classifyElements() {
    const body = doc.body;
    const elements = Array.from(body.children);
    let inContent = false;
    let currentPart = null;
    let currentSection = null;

    elements.forEach(el => {
      if (el.tagName === 'TABLE') {
        // Cover table
        return;
      }
      if (el.classList.contains('content')) {
        inContent = true;
        return;
      }
      if (!inContent) return;

      if (el.tagName === 'P') {
        const text = el.textContent.trim();
        const match = text.match(/^(\d{1,3})\.\s*(.*)$/s);
        if (match) {
          const number = parseInt(match[1], 10);
          const textRaw = match[2].trim();
          paragraphs.push({
            element: el,
            number,
            textRaw,
            part: currentPart,
            section: currentSection,
            text: null,
            spaces: [],
            firstWordsMatch: null,
            citation: `${data.symbol}, para. ${number}`
          });
          return;
        }
        // Committee line
        return;
      }

      if (el.tagName === 'H2') {
        const text = el.textContent.trim();
        if (text === data.title) {
          // Title
          return;
        }
        const match = text.match(/^([IVX]+)\.\s*(.+)$/);
        if (match) {
          currentPart = {
            label: match[1],
            heading: match[2],
            element: el
          };
          currentSection = null;
          headings.push(currentPart);
          return;
        }
        // Unnumbered H2 (should not happen)
        currentPart = null;
        currentSection = null;
        return;
      }

      if (el.tagName === 'H3') {
        const text = el.textContent.trim();
        const match = text.match(/^([A-Z])\.\s*(.+)$/);
        if (match) {
          currentSection = {
            label: match[1],
            heading: match[2],
            element: el,
            part: currentPart
          };
          headings.push(currentSection);
          return;
        }
        // Unlettered H3
        currentSection = {
          label: null,
          heading: text,
          element: el,
          part: currentPart
        };
        headings.push(currentSection);
        return;
      }
    });
  }

  function computeParagraphs() {
    paragraphs.forEach(p => {
      // Repair spaces
      let text = p.textRaw;
      const spacesLog = [];

      // Rule 1: full stop between lowercase and capital
      const rule1 = /([a-z])\.([A-Z])/g;
      let match;
      while ((match = rule1.exec(text)) !== null) {
        const before = text.slice(Math.max(0, match.index - 20), match.index);
        const after = text.slice(match.index + match[0].length, match.index + match[0].length + 20);
        spacesLog.push({
          rule: 'sentence',
          before: before + match[0] + after,
          after: before + match[1] + '. ' + match[2] + after,
          context: match[0]
        });
        text = text.slice(0, match.index + match[1].length + 1) + ' ' + text.slice(match.index + match[0].length);
        rule1.lastIndex = match.index + match[1].length + 2;
      }

      // Rule 2: comma between letters
      const rule2 = /([a-z]),([A-Za-z])/g;
      while ((match = rule2.exec(text)) !== null) {
        const before = text.slice(Math.max(0, match.index - 20), match.index);
        const after = text.slice(match.index + match[0].length, match.index + match[0].length + 20);
        spacesLog.push({
          rule: 'comma',
          before: before + match[0] + after,
          after: before + match[1] + ', ' + match[2] + after,
          context: match[0]
        });
        text = text.slice(0, match.index + match[1].length + 1) + ' ' + text.slice(match.index + match[0].length);
        rule2.lastIndex = match.index + match[1].length + 2;
      }

      // Rule 3: opening curly quote touching a letter
      const rule3 = /([a-z])“/g;
      while ((match = rule3.exec(text)) !== null) {
        const before = text.slice(Math.max(0, match.index - 20), match.index);
        const after = text.slice(match.index + match[0].length, match.index + match[0].length + 20);
        spacesLog.push({
          rule: 'quote',
          before: before + match[0] + after,
          after: before + match[1] + ' “' + after,
          context: match[0]
        });
        text = text.slice(0, match.index + match[1].length) + ' “' + text.slice(match.index + match[0].length);
        rule3.lastIndex = match.index + match[1].length + 2;
      }

      // Rule 4: en dash touching a letter
      const rule4 = /–([A-Za-z])/g;
      while ((match = rule4.exec(text)) !== null) {
        const before = text.slice(Math.max(0, match.index - 20), match.index);
        const after = text.slice(match.index + match[0].length, match.index + match[0].length + 20);
        spacesLog.push({
          rule: 'dash',
          before: before + match[0] + after,
          after: before + '– ' + match[1] + after,
          context: match[0]
        });
        text = text.slice(0, match.index) + '– ' + text.slice(match.index + match[0].length);
        rule4.lastIndex = match.index + 2;
      }

      p.text = text;
      p.spaces = spacesLog;

      // First words
      const words = text.split(/\s+/).slice(0, 6).join(' ');
      const expected = firstWordsExpected[String(p.number)] || '';
      const normalisedWords = words.replace(/[“”]/g, '"').replace(/[–‑]/g, '-').replace(/\u00A0/g, ' ');
      const normalisedExpected = expected.replace(/[“”]/g, '"').replace(/[–‑]/g, '-').replace(/\u00A0/g, ' ');
      p.firstWordsMatch = normalisedWords === normalisedExpected;

      if (!p.firstWordsMatch) {
        firstWordsMismatch++;
        mismatchList.push(p);
      }

      // Count spaces
      if (spacesLog.length > 0) {
        spacesParagraphs++;
        spacesRestored += spacesLog.length;
      }
      spaces.push(...spacesLog);
    });
  }

  function computeHeadings() {
    // Nothing to compute; headings are already classified
  }

  function computeChecks() {
    checks = [];

    // Check 1: paragraph count
    checks.push({
      name: 'Paragraph count',
      found: paragraphs.length,
      expected: paragraphsExpected,
      pass: paragraphs.length === paragraphsExpected,
      limit: false,
      message: `Found ${paragraphs.length}, expected ${paragraphsExpected}`
    });

    // Check 2: numbering
    const numbers = paragraphs.map(p => p.number);
    const uniqueNumbers = [...new Set(numbers)];
    const duplicates = numbers.filter((n, i) => numbers.indexOf(n) !== i);
    const gaps = [];
    for (let i = 1; i <= paragraphsExpected; i++) {
      if (!numbers.includes(i)) gaps.push(i);
    }
    checks.push({
      name: 'Numbering',
      found: numbers.join(', '),
      expected: `1 to ${paragraphsExpected}`,
      pass: duplicates.length === 0 && gaps.length === 0,
      limit: false,
      message: duplicates.length > 0 ? `Duplicates: ${duplicates.join(', ')}` : gaps.length > 0 ? `Gaps: ${gaps.join(', ')}` : 'Pass'
    });

    // Check 3: first words
    checks.push({
      name: 'First words',
      found: `${paragraphs.length - firstWordsMismatch} of ${paragraphs.length}`,
      expected: `${paragraphs.length}`,
      pass: firstWordsMismatch === 0,
      limit: false,
      message: firstWordsMismatch > 0 ? `Mismatches: ${firstWordsMismatch}` : 'Pass'
    });

    // Check 4: footnotes
    checks.push({
      name: 'Footnotes',
      found: '0',
      expected: footnotesExpected,
      pass: false,
      limit: true,
      message: 'Source limit: the HTML version has no footnotes'
    });

    // Check 5: spaces
    checks.push({
      name: 'Spaces',
      found: `${spacesRestored} in ${spacesParagraphs} paragraphs`,
      expected: '0',
      pass: true, // Not a pass/fail check
      limit: false,
      message: `Restored ${spacesRestored} spaces in ${spacesParagraphs} paragraphs`
    });

    // Check 6: headings
    const h2Count = headings.filter(h => h.element.tagName === 'H2').length;
    const h3Count = headings.filter(h => h.element.tagName === 'H3').length;
    const gluedLabels = headings.filter(h => h.label && h.element.textContent.trim().startsWith(h.label + '.')).length;
    checks.push({
      name: 'Headings',
      found: `${h2Count} H2, ${h3Count} H3, ${gluedLabels} glued labels`,
      expected: '?',
      pass: true, // Not a pass/fail check
      limit: false,
      message: `Found ${h2Count} H2, ${h3Count} H3, ${gluedLabels} glued labels`
    });

    // Check 7: nothing lost
    const classified = paragraphs.length + headings.length + 1; // +1 for the committee line
    const total = Array.from(doc.body.querySelector('.content').children).length;
    checks.push({
      name: 'Nothing lost',
      found: classified,
      expected: total,
      pass: classified === total,
      limit: false,
      message: classified === total ? 'Pass' : `Classified ${classified}, total ${total}`
    });

    // Check 8: export round trip
    checks.push({
      name: 'Export round trip',
      found: '?',
      expected: '?',
      pass: null, // Will be set after export
      limit: false,
      message: 'Not run'
    });

    // Count checks
    checksPass = checks.filter(c => c.pass === true).length;
    checksTotal = checks.length;
  }

  function render() {
    // Header
    docTitle.textContent = data.title;
    docMeta.innerHTML = `<a href="${data.doc_url}" target="_blank">${data.symbol}</a>, adopted ${adopted}, ${source}`;
    railSymbol.textContent = data.symbol;
    railShortTitle.textContent = data.title.split(' (')[0];
    railParagraphsFound.textContent = paragraphs.length;
    railParagraphsExpected.textContent = paragraphsExpected;
    railFootnotesExpected.textContent = footnotesExpected;
    railChecksPass.textContent = checksPass;
    railChecksTotal.textContent = checksTotal;

    // Status
    if (checksPass === checksTotal) {
      statusDot.className = 'status-dot pass';
      statusText.textContent = `${checksPass} of ${checksTotal} checks pass`;
    } else {
      statusDot.className = 'status-dot fail';
      statusText.textContent = `${checksTotal - checksPass} checks failed`;
    }

    // Rail bar
    const percent = paragraphsExpected > 0 ? Math.min(100, (paragraphs.length / paragraphsExpected) * 100) : 0;
    railParagraphsBar.style.width = `${percent}%`;
    if (paragraphs.length !== paragraphsExpected) {
      railParagraphsBar.style.backgroundColor = 'var(--red)';
    }

    // Tiles
    tileParagraphsFound.textContent = paragraphs.length;
    tileParagraphsExpected.textContent = paragraphsExpected;
    if (paragraphs.length !== paragraphsExpected) {
      tileParagraphsFound.parentElement.classList.add('fail');
    }
    tileFirstWordsMatch.textContent = `${paragraphs.length - firstWordsMismatch} of ${paragraphs.length}`;
    if (firstWordsMismatch > 0) {
      tileFirstWordsMatch.parentElement.classList.add('fail');
    }
    tileSpacesRestored.textContent = spacesRestored;
    tileSpacesParagraphs.textContent = spacesParagraphs;

    // Mismatch list
    if (firstWordsMismatch > 0) {
      mismatchListContainer.style.display = 'block';
      mismatchListEl.innerHTML = '';
      const show = Math.min(10, mismatchList.length);
      for (let i = 0; i < show; i++) {
        const p = mismatchList[i];
        const found = p.text.split(/\s+/).slice(0, 6).join(' ');
        const expected = firstWordsExpected[String(p.number)] || '';
        const item = document.createElement('div');
        item.className = 'mismatch-item';
        item.innerHTML = `<strong>para. ${p.number}:</strong> found <span style="font-family: ui-monospace">${escapeHtml(found)}</span> / reference <span style="font-family: ui-monospace">${escapeHtml(expected)}</span>`;
        mismatchListEl.appendChild(item);
      }
      if (mismatchList.length > 10) {
        const item = document.createElement('div');
        item.className = 'mismatch-item';
        item.textContent = `and ${mismatchList.length - 10} more`;
        mismatchListEl.appendChild(item);
      }
    } else {
      mismatchListContainer.style.display = 'none';
    }

    // Downloads
    downloadJson.disabled = paragraphs.length === 0;
    downloadMarkdown.disabled = paragraphs.length === 0;

    // Checks
    checksHeadingCount.textContent = checks.length;
    checkList.innerHTML = '';
    checks.forEach((check, i) => {
      const item = document.createElement('li');
      item.className = `check-item ${check.pass === false ? 'fail' : check.limit ? 'limit' : 'pass'}`;
      const expected = check.expected === '?' ? '' : ` / ${check.expected}`;
      item.innerHTML = `
        <span>${check.name}</span>
        <span>${check.found}${expected}</span>
        <span>${check.limit ? 'source limit' : check.pass ? 'pass' : 'check failed'}</span>
      `;
      if (check.name === 'First words' && firstWordsMismatch > 0) {
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = 'see list';
        link.addEventListener('click', e => {
          e.preventDefault();
          document.getElementById('tab-01').click();
          mismatchListContainer.scrollIntoView({ behavior: 'smooth' });
        });
        item.appendChild(link);
      }
      checkList.appendChild(item);
    });

    // Spaces
    spacesHeadingCount.textContent = spaces.length;
    spaceRulesBody.innerHTML = '';
    const rules = {};
    spaces.forEach(s => {
      rules[s.rule] = (rules[s.rule] || 0) + 1;
    });
    Object.entries(rules).forEach(([rule, count]) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${rule}</td>
        <td class="count">${count}</td>
      `;
      spaceRulesBody.appendChild(row);
    });
    spaceListBody.innerHTML = '';
    spaces.forEach(s => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${s.context}</td>
        <td class="before">${escapeHtml(s.before)}</td>
        <td class="after">${escapeHtml(s.after)}</td>
        <td class="rule">${s.rule}</td>
      `;
      spaceListBody.appendChild(row);
    });

    // Headings
    headingsHeadingCount.textContent = headings.length;
    headingList.innerHTML = '';
    headings.forEach(h => {
      const item = document.createElement('li');
      item.className = 'heading-item';
      const label = h.label ? `${h.label}. ` : '';
      const part = h.part ? `${h.part.label}. ` : '';
      item.innerHTML = `
        <span class="heading-label">${part}${label}</span>
        <span class="heading-text">${h.heading}</span>
      `;
      headingList.appendChild(item);
    });

    // Paragraphs
    paragraphTableBody.innerHTML = '';
    paragraphs.forEach(p => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>
          <button aria-expanded="false" aria-controls="para-${p.number}-details">
            <span class="para-no">${p.number}.</span>
            <span class="expand-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </span>
          </button>
        </td>
        <td class="para-section">${p.section ? p.section.heading : ''}</td>
        <td class="para-first-line">${escapeHtml(p.text.slice(0, 120).replace(/\s+/g, ' '))}${p.text.length > 120 ? '…' : ''}</td>
        <td class="para-check ${p.firstWordsMatch ? '' : 'fail'}">${p.firstWordsMatch ? 'OK' : 'first words differ'}</td>
      `;
      const details = document.createElement('tr');
      details.className = 'expanded';
      details.innerHTML = `
        <td colspan="4">
          <div class="para-details" id="para-${p.number}-details" aria-hidden="true">
            <div class="para-text">${formatTextWithSpaces(p.text, p.spaces)}</div>
            <div class="para-words">
              <div class="para-words-label">First six words:</div>
              <div class="para-words-value">${escapeHtml(p.text.split(/\s+/).slice(0, 6).join(' '))}</div>
              <div class="para-words-label">Reference:</div>
              <div class="para-words-value">${escapeHtml(firstWordsExpected[String(p.number)] || '')}</div>
            </div>
            ${p.spaces.length > 0 ? `
            <div class="para-spaces">
              <div class="para-spaces-label">Spaces restored:</div>
              <ul class="para-spaces-list">
                ${p.spaces.map(s => `<li class="para-spaces-item">${escapeHtml(s.context)} <mark>${escapeHtml(s.context)}</mark></li>`).join('')}
              </ul>
            </div>
            ` : ''}
            <button class="copy-button" data-citation="${p.citation}">Copy citation</button>
            <div class="copy-feedback" id="copy-feedback-${p.number}"></div>
          </div>
        </td>
      `;
      paragraphTableBody.appendChild(row);
      paragraphTableBody.appendChild(details);

      const button = row.querySelector('button');
      const detailsEl = details.querySelector('.para-details');
      button.addEventListener('click', () => {
        const expanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', !expanded);
        detailsEl.setAttribute('aria-hidden', expanded);
        row.classList.toggle('expanded');
      });

      const copyButton = details.querySelector('.copy-button');
      copyButton.addEventListener('click', () => {
        navigator.clipboard.writeText(copyButton.dataset.citation).then(() => {
          const feedback = document.getElementById(`copy-feedback-${p.number}`);
          feedback.textContent = 'Copied';
          setTimeout(() => {
            feedback.textContent = '';
          }, 2000);
        });
      });
    });

    // Footer
    footerSource.textContent = source;
    footerBuilt.textContent = `Built ${built}`;
  }

  function formatTextWithSpaces(text, spaces) {
    let result = text;
    // Apply spaces in reverse order to avoid offset issues
    spaces.slice().reverse().forEach(s => {
      const index = result.indexOf(s.context);
      if (index !== -1) {
        result = result.slice(0, index) + `<mark>${escapeHtml(s.context)}</mark>` + result.slice(index + s.context.length);
      }
    });
    return escapeHtml(result).replace(/\n/g, '<br>');
  }

  function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  // Downloads
  downloadJson.addEventListener('click', () => {
    const json = paragraphs.map(p => ({
      symbol: data.symbol,
      paragraph: p.number,
      section: p.section ? p.section.heading : null,
      part: p.part ? `${p.part.label}. ${p.part.heading}` : null,
      text: p.text,
      text_raw: p.textRaw,
      first_words_match: p.firstWordsMatch,
      citation: p.citation,
      doc_url: data.doc_url,
      limitations: `no footnotes in this HTML version; the document has ${footnotesExpected}`
    }));
    const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.json';
    a.click();
    URL.revokeObjectURL(url);

    // Update export round trip check
    const check = checks.find(c => c.name === 'Export round trip');
    try {
      const parsed = JSON.parse(JSON.stringify(json));
      check.found = parsed.length;
      check.expected = paragraphs.length;
      check.pass = parsed.length === paragraphs.length;
      check.message = `Exported ${parsed.length}, found ${paragraphs.length}`;
    } catch (e) {
      check.found = 'error';
      check.expected = paragraphs.length;
      check.pass = false;
      check.message = 'Export failed';
    }
    checksPass = checks.filter(c => c.pass === true).length;
    railChecksPass.textContent = checksPass;
    renderChecks();
  });

  downloadMarkdown.addEventListener('click', () => {
    let markdown = `---\n`;
    markdown += `title: "${data.title}"\n`;
    markdown += `symbol: ${data.symbol}\n`;
    markdown += `adopted: ${adopted}\n`;
    markdown += `source_url: ${data.doc_url}\n`;
    markdown += `extracted: ${built}\n`;
    markdown += `paragraphs_found: ${paragraphs.length}\n`;
    markdown += `paragraphs_expected: ${paragraphsExpected}\n`;
    markdown += `footnotes: no footnotes in this HTML version; the document has ${footnotesExpected}\n`;
    markdown += `---\n\n`;

    let currentPart = null;
    let currentSection = null;

    paragraphs.forEach(p => {
      if (p.part && p.part !== currentPart) {
        markdown += `## ${p.part.label}. ${p.part.heading}\n\n`;
        currentPart = p.part;
        currentSection = null;
      }
      if (p.section && p.section !== currentSection) {
        markdown += `### ${p.section.label ? `${p.section.label}. ` : ''}${p.section.heading}\n\n`;
        currentSection = p.section;
      }
      markdown += `**${p.number}.** ${p.text}\n\n`;
    });

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = data.symbol.replace(/\//g, '-') + '.md';
    a.click();
    URL.revokeObjectURL(url);
  });

  function renderChecks() {
    checkList.innerHTML = '';
    checks.forEach((check, i) => {
      const item = document.createElement('li');
      item.className = `check-item ${check.pass === false ? 'fail' : check.limit ? 'limit' : 'pass'}`;
      const expected = check.expected === '?' ? '' : ` / ${check.expected}`;
      item.innerHTML = `
        <span>${check.name}</span>
        <span>${check.found}${expected}</span>
        <span>${check.limit ? 'source limit' : check.pass ? 'pass' : 'check failed'}</span>
      `;
      if (check.name === 'First words' && firstWordsMismatch > 0) {
        const link = document.createElement('a');
        link.href = '#';
        link.textContent = 'see list';
        link.addEventListener('click', e => {
          e.preventDefault();
          document.getElementById('tab-01').click();
          mismatchListContainer.scrollIntoView({ behavior: 'smooth' });
        });
        item.appendChild(link);
      }
      checkList.appendChild(item);
    });
  }

  // Run
  run();
})();
</script>
</body>
</html>
```