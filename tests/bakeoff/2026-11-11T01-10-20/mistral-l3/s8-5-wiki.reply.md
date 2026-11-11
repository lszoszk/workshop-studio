Here is the workspace for reading and checking the research wiki. It has three tabs: Pages (the wiki's pages with filters and rendered bodies), Check (the app's own checks on the wiki), and Record (the log, tensions, and a download).

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Wiki workspace: neurotechnology and justice</title>
  <style>
    :root {
      --paper: #f4f0e8;
      --ink: #1d1b18;
      --rule: #d9d2c3;
      --accent: #9b2335;
    }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      font-size: 16px;
      line-height: 1.5;
      color: var(--ink);
      background-color: var(--paper);
      padding: 1rem;
    }
    header {
      border-bottom: 1px solid var(--rule);
      padding-bottom: 1rem;
      margin-bottom: 1rem;
    }
    .data-label {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      color: #666;
      margin-right: 1rem;
    }
    h1 {
      font-family: Georgia, "Times New Roman", serif;
      font-size: 1.8rem;
      margin: 0;
      font-weight: normal;
    }
    .source-line {
      font-size: 0.8rem;
      color: #666;
      margin-top: 0.2rem;
    }
    .tabs {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }
    .tab {
      padding: 0.5rem 1rem;
      border: 1px solid var(--rule);
      background: var(--paper);
      cursor: pointer;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-radius: 4px 4px 0 0;
    }
    .tab[aria-selected="true"] {
      background: var(--accent);
      color: white;
      border-bottom-color: var(--accent);
    }
    .tab:focus {
      outline: 2px solid var(--accent);
      outline-offset: -2px;
    }
    .tab-panel {
      border: 1px solid var(--rule);
      border-radius: 0 0 4px 4px;
      padding: 1rem;
      display: none;
    }
    .tab-panel[aria-hidden="false"] {
      display: block;
    }
    .filter-rail {
      width: 240px;
      float: left;
      margin-right: 2rem;
      font-size: 0.9rem;
    }
    .filter-section {
      border-bottom: 1px solid var(--rule);
      padding-bottom: 1rem;
      margin-bottom: 1rem;
    }
    .filter-section h3 {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin: 0 0 0.5rem 0;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .filter-section h3::before {
      content: "▶";
      font-size: 0.7rem;
      margin-right: 0.5rem;
    }
    .filter-section[aria-expanded="true"] h3::before {
      content: "▼";
    }
    .filter-body {
      display: none;
    }
    .filter-section[aria-expanded="true"] .filter-body {
      display: block;
    }
    .filter-count {
      font-size: 2.5rem;
      font-family: Georgia, "Times New Roman", serif;
      margin: 0 0 0.5rem 0;
      line-height: 1;
    }
    .filter-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.3rem;
      margin-bottom: 0.5rem;
    }
    .filter-chip {
      background: var(--accent);
      color: white;
      padding: 0.2rem 0.5rem;
      border-radius: 1rem;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
    }
    .filter-chip-close {
      margin-left: 0.3rem;
      cursor: pointer;
      font-weight: bold;
    }
    input[type="search"] {
      width: 100%;
      padding: 0.3rem;
      border: 1px solid var(--rule);
      background: white;
      font-size: 0.9rem;
    }
    .page-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .page-list li {
      padding: 0.3rem 0;
      border-bottom: 1px solid var(--rule);
    }
    .page-list a {
      color: var(--ink);
      text-decoration: none;
    }
    .page-list a:hover {
      text-decoration: underline;
    }
    .page-meta {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      color: #666;
      margin-top: 0.2rem;
    }
    .page-body {
      margin-top: 1rem;
      clear: both;
    }
    .page-body h2, .page-body h3 {
      font-family: Georgia, "Times New Roman", serif;
      margin-top: 1.5rem;
    }
    .page-body h2 {
      font-size: 1.3rem;
    }
    .page-body h3 {
      font-size: 1.1rem;
    }
    .page-body p {
      margin: 0.5rem 0;
    }
    .page-body ul, .page-body ol {
      margin: 0.5rem 0;
      padding-left: 2rem;
    }
    .page-body li {
      margin: 0.3rem 0;
    }
    .wiki-link {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      background: #f0e8e0;
      padding: 0 0.2rem;
      border-radius: 2px;
      text-decoration: none;
      color: var(--accent);
    }
    .wiki-link:hover {
      text-decoration: underline;
    }
    .pin {
      display: inline;
      position: relative;
    }
    .pin-quote {
      font-style: italic;
    }
    .pin-chip {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.7rem;
      background: var(--accent);
      color: white;
      padding: 0.1rem 0.3rem;
      border-radius: 1rem;
      margin-left: 0.3rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
    }
    .pin-chip:hover {
      background: #7a1a2a;
    }
    .pin-chip::after {
      content: attr(data-mark);
      margin-left: 0.3rem;
      font-size: 0.6rem;
    }
    .contested-card {
      border: 1px solid var(--rule);
      border-radius: 4px;
      padding: 1rem;
      margin: 1rem 0;
      background: white;
    }
    .contested-card h4 {
      margin: 0 0 0.5rem 0;
      font-family: Georgia, "Times New Roman", serif;
    }
    .contested-verdict {
      font-weight: bold;
      margin-bottom: 0.5rem;
    }
    .contested-note {
      font-style: italic;
      color: #666;
      margin-bottom: 1rem;
    }
    .contested-entry {
      margin-bottom: 0.5rem;
      padding-left: 1rem;
      border-left: 2px solid var(--rule);
    }
    .contested-entry::before {
      content: attr(data-mark);
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      margin-left: -1.3rem;
      margin-right: 0.3rem;
    }
    .contested-entry[data-mark="+"]::before {
      color: green;
    }
    .contested-entry[data-mark="-"]::before {
      color: var(--accent);
    }
    .contested-entry[data-mark="~"]::before {
      color: #666;
    }
    .contested-gloss {
      font-style: italic;
    }
    .related-section {
      margin-top: 2rem;
      border-top: 1px solid var(--rule);
      padding-top: 1rem;
    }
    .related-section h4 {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin: 0 0 0.5rem 0;
    }
    .related-list {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .related-item {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      background: #f0e8e0;
      padding: 0.2rem 0.4rem;
      border-radius: 2px;
    }
    .lint-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
    }
    .lint-table th, .lint-table td {
      border: 1px solid var(--rule);
      padding: 0.5rem;
      text-align: left;
    }
    .lint-table th {
      background: #f0e8e0;
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .lint-table tr:nth-child(even) {
      background: #f9f7f4;
    }
    .big-number {
      font-size: 3rem;
      font-family: Georgia, "Times New Roman", serif;
      margin: 0 0 0.5rem 0;
      line-height: 1;
    }
    .log-entry {
      border-bottom: 1px solid var(--rule);
      padding-bottom: 1rem;
      margin-bottom: 1rem;
    }
    .log-date {
      font-family: ui-monospace, Menlo, Consolas, monospace;
      font-size: 0.8rem;
      color: #666;
      margin-bottom: 0.3rem;
    }
    .tension-entry {
      border-bottom: 1px solid var(--rule);
      padding-bottom: 1rem;
      margin-bottom: 1rem;
    }
    .tension-title {
      font-weight: bold;
      margin-bottom: 0.3rem;
    }
    .download-button {
      background: var(--accent);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.9rem;
    }
    [hidden] { display: none !important; }
  </style>
</head>
<body>

  <header>
    <span class="data-label">WORKSHOP_DATA.wiki</span>
    <h1>Wiki workspace: neurotechnology and justice</h1>
    <div class="source-line">40 pages, 707 pins, built 2026-11-02</div>
  </header>

  <div class="tabs" role="tablist" aria-label="Wiki workspace tabs">
    <button id="tab-01" class="tab" role="tab" aria-selected="true" aria-controls="panel-01">01 PAGES</button>
    <button id="tab-02" class="tab" role="tab" aria-selected="false" aria-controls="panel-02">02 CHECK</button>
    <button id="tab-03" class="tab" role="tab" aria-selected="false" aria-controls="panel-03">03 RECORD</button>
  </div>

  <main>
    <div id="panel-01" class="tab-panel" role="tabpanel" aria-labelledby="tab-01" aria-hidden="false">
      <div class="filter-rail">
        <div class="filter-count" id="filter-count">40</div>
        <div class="filter-chips" id="filter-chips"></div>

        <div class="filter-section" aria-expanded="true">
          <h3 id="filter-type-heading">01 TYPE</h3>
          <div class="filter-body">
            <input type="search" id="filter-type-search" placeholder="Search types…">
            <div id="filter-type-list"></div>
          </div>
        </div>

        <div class="filter-section" aria-expanded="false">
          <h3 id="filter-register-heading">02 REGISTER</h3>
          <div class="filter-body">
            <div id="filter-register-list"></div>
          </div>
        </div>

        <div class="filter-section" aria-expanded="false">
          <h3 id="filter-status-heading">03 STATUS</h3>
          <div class="filter-body">
            <div id="filter-status-list"></div>
          </div>
        </div>

        <div class="filter-section" aria-expanded="false">
          <h3 id="filter-tag-heading">04 TAG</h3>
          <div class="filter-body">
            <input type="search" id="filter-tag-search" placeholder="Search tags…">
            <div id="filter-tag-list"></div>
          </div>
        </div>
      </div>

      <div id="page-index">
        <ul class="page-list" id="page-list"></ul>
      </div>

      <div id="page-view" hidden>
        <div class="page-meta" id="page-meta"></div>
        <div class="page-body" id="page-body"></div>
        <div class="related-section">
          <h4>LINKS OUT</h4>
          <ul class="related-list" id="links-out"></ul>
        </div>
        <div class="related-section">
          <h4>LINKED FROM</h4>
          <ul class="related-list" id="linked-from"></ul>
        </div>
        <div class="related-section">
          <h4>SOURCES</h4>
          <ul class="related-list" id="sources"></ul>
        </div>
      </div>
    </div>

    <div id="panel-02" class="tab-panel" role="tabpanel" aria-labelledby="tab-02" aria-hidden="true">
      <div class="big-number" id="verified-pins">0</div>
      <p>pins verified by the code (a quote with "…" is several fragments, each found in order)</p>

      <h3>Lint table</h3>
      <table class="lint-table">
        <thead>
          <tr>
            <th>Issue</th>
            <th>Pages</th>
            <th>Count</th>
          </tr>
        </thead>
        <tbody id="lint-rows">
          <!-- Filled by JS -->
        </tbody>
      </table>
    </div>

    <div id="panel-03" class="tab-panel" role="tabpanel" aria-labelledby="tab-03" aria-hidden="true">
      <h3>Log (newest first)</h3>
      <div id="log-entries"></div>

      <h3>Tensions register</h3>
      <div id="tension-entries"></div>

      <h3>Download</h3>
      <button class="download-button" id="download-wiki">Download wiki as JSON</button>
    </div>
  </main>

  <script>
    // Data
    const wiki = window.WORKSHOP_DATA.wiki;
    const library = window.WORKSHOP_DATA.library.records.reduce((acc, doc) => {
      acc[doc.id] = doc;
      return acc;
    }, {});

    // State
    let activeFilters = {
      type: new Set(),
      register: new Set(),
      status: new Set(),
      tag: new Set(),
      search: ''
    };
    let currentPage = null;

    // DOM
    const tabButtons = document.querySelectorAll('.tab');
    const tabPanels = document.querySelectorAll('.tab-panel');
    const filterCount = document.getElementById('filter-count');
    const filterChips = document.getElementById('filter-chips');
    const filterSections = document.querySelectorAll('.filter-section');
    const pageList = document.getElementById('page-list');
    const pageIndex = document.getElementById('page-index');
    const pageView = document.getElementById('page-view');
    const pageMeta = document.getElementById('page-meta');
    const pageBody = document.getElementById('page-body');
    const linksOut = document.getElementById('links-out');
    const linkedFrom = document.getElementById('linked-from');
    const sourcesList = document.getElementById('sources');
    const verifiedPinsCount = document.getElementById('verified-pins');
    const lintRows = document.getElementById('lint-rows');
    const logEntries = document.getElementById('log-entries');
    const tensionEntries = document.getElementById('tension-entries');
    const downloadWiki = document.getElementById('download-wiki');

    // Tabs
    tabButtons.forEach(button => {
      button.addEventListener('click', () => {
        const panelId = button.getAttribute('aria-controls');
        tabButtons.forEach(b => {
          b.setAttribute('aria-selected', b === button);
        });
        tabPanels.forEach(p => {
          p.setAttribute('aria-hidden', p.id !== panelId);
        });
        if (panelId === 'panel-02') updateCheckTab();
        if (panelId === 'panel-03') updateRecordTab();
      });
    });

    // Filter sections
    filterSections.forEach(section => {
      const heading = section.querySelector('h3');
      heading.addEventListener('click', () => {
        const isExpanded = section.getAttribute('aria-expanded') === 'true';
        section.setAttribute('aria-expanded', !isExpanded);
      });
    });

    // Filter UI
    function updateFilterUI() {
      // Chips
      filterChips.innerHTML = '';
      const allFilters = [
        ...Array.from(activeFilters.type).map(t => ({type: 'type', value: t})),
        ...Array.from(activeFilters.register).map(r => ({type: 'register', value: r})),
        ...Array.from(activeFilters.status).map(s => ({type: 'status', value: s})),
        ...Array.from(activeFilters.tag).map(t => ({type: 'tag', value: t}))
      ];
      if (activeFilters.search) {
        allFilters.push({type: 'search', value: activeFilters.search});
      }
      allFilters.forEach(filter => {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.textContent = `${filter.type}: ${filter.value}`;
        const close = document.createElement('span');
        close.className = 'filter-chip-close';
        close.textContent = '×';
        close.addEventListener('click', e => {
          e.stopPropagation();
          if (filter.type === 'type') activeFilters.type.delete(filter.value);
          if (filter.type === 'register') activeFilters.register.delete(filter.value);
          if (filter.type === 'status') activeFilters.status.delete(filter.value);
          if (filter.type === 'tag') activeFilters.tag.delete(filter.value);
          if (filter.type === 'search') activeFilters.search = '';
          updateFilterUI();
          updatePageList();
        });
        chip.appendChild(close);
        filterChips.appendChild(chip);
      });

      // Count
      const filteredPages = wiki.pages.filter(page => matchesFilters(page));
      filterCount.textContent = filteredPages.length;

      // Type filter
      const typeList = document.getElementById('filter-type-list');
      typeList.innerHTML = '';
      const types = [...new Set(wiki.pages.map(p => p.type))].sort();
      types.forEach(type => {
        const div = document.createElement('div');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = `type-${type}`;
        input.checked = activeFilters.type.has(type);
        input.addEventListener('change', () => {
          if (input.checked) activeFilters.type.add(type);
          else activeFilters.type.delete(type);
          updateFilterUI();
          updatePageList();
        });
        const label = document.createElement('label');
        label.htmlFor = input.id;
        label.textContent = `${type} (${wiki.pages.filter(p => p.type === type).length})`;
        div.appendChild(input);
        div.appendChild(label);
        typeList.appendChild(div);
      });

      // Register filter
      const registerList = document.getElementById('filter-register-list');
      registerList.innerHTML = '';
      const registers = ['a', 'b', 'c', 'd', 'e', 'f'];
      registers.forEach(reg => {
        const div = document.createElement('div');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = `register-${reg}`;
        input.checked = activeFilters.register.has(reg);
        input.addEventListener('change', () => {
          if (input.checked) activeFilters.register.add(reg);
          else activeFilters.register.delete(reg);
          updateFilterUI();
          updatePageList();
        });
        const label = document.createElement('label');
        label.htmlFor = input.id;
        label.textContent = `${reg} (${wiki.pages.filter(p => p.frontmatter.register.includes(reg)).length})`;
        div.appendChild(input);
        div.appendChild(label);
        registerList.appendChild(div);
      });

      // Status filter
      const statusList = document.getElementById('filter-status-list');
      statusList.innerHTML = '';
      const statuses = [...new Set(wiki.pages.map(p => p.frontmatter.status))].sort();
      statuses.forEach(status => {
        const div = document.createElement('div');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = `status-${status}`;
        input.checked = activeFilters.status.has(status);
        input.addEventListener('change', () => {
          if (input.checked) activeFilters.status.add(status);
          else activeFilters.status.delete(status);
          updateFilterUI();
          updatePageList();
        });
        const label = document.createElement('label');
        label.htmlFor = input.id;
        label.textContent = `${status} (${wiki.pages.filter(p => p.frontmatter.status === status).length})`;
        div.appendChild(input);
        div.appendChild(label);
        statusList.appendChild(div);
      });

      // Tag filter
      const tagList = document.getElementById('filter-tag-list');
      tagList.innerHTML = '';
      const allTags = [...new Set(wiki.pages.flatMap(p => p.frontmatter.tags))].sort();
      const tagSearch = document.getElementById('filter-tag-search').value.toLowerCase();
      const filteredTags = allTags.filter(tag => tag.toLowerCase().includes(tagSearch));
      filteredTags.forEach(tag => {
        const div = document.createElement('div');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = `tag-${tag}`;
        input.checked = activeFilters.tag.has(tag);
        input.addEventListener('change', () => {
          if (input.checked) activeFilters.tag.add(tag);
          else activeFilters.tag.delete(tag);
          updateFilterUI();
          updatePageList();
        });
        const label = document.createElement('label');
        label.htmlFor = input.id;
        label.textContent = `${tag} (${wiki.pages.filter(p => p.frontmatter.tags.includes(tag)).length})`;
        div.appendChild(input);
        div.appendChild(label);
        tagList.appendChild(div);
      });
      document.getElementById('filter-tag-search').addEventListener('input', updateFilterUI);

      // Search
      document.getElementById('filter-type-search').addEventListener('input', e => {
        activeFilters.search = e.target.value.toLowerCase();
        updateFilterUI();
        updatePageList();
      });
    }

    function matchesFilters(page) {
      if (activeFilters.type.size > 0 && !activeFilters.type.has(page.type)) return false;
      if (activeFilters.register.size > 0 && !page.frontmatter.register.some(r => activeFilters.register.has(r))) return false;
      if (activeFilters.status.size > 0 && !activeFilters.status.has(page.frontmatter.status)) return false;
      if (activeFilters.tag.size > 0 && !page.frontmatter.tags.some(t => activeFilters.tag.has(t))) return false;
      if (activeFilters.search && !page.title.toLowerCase().includes(activeFilters.search)) return false;
      return true;
    }

    function updatePageList() {
      pageList.innerHTML = '';
      const filteredPages = wiki.pages.filter(page => matchesFilters(page)).sort((a, b) => a.title.localeCompare(b.title));
      filteredPages.forEach(page => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#';
        a.textContent = page.title;
        a.addEventListener('click', e => {
          e.preventDefault();
          showPage(page);
        });
        li.appendChild(a);
        const meta = document.createElement('div');
        meta.className = 'page-meta';
        meta.textContent = `${page.type} · ${page.frontmatter.register.join('')} · ${page.frontmatter.status}`;
        li.appendChild(meta);
        pageList.appendChild(li);
      });
    }

    function showPage(page) {
      currentPage = page;
      pageIndex.hidden = true;
      pageView.hidden = false;

      // Meta
      pageMeta.textContent = `${page.type} · ${page.frontmatter.register.join('')} · ${page.frontmatter.status} · updated ${page.frontmatter.updated}`;

      // Body
      pageBody.innerHTML = renderMarkdown(page.body);

      // Links out
      linksOut.innerHTML = '';
      const linksOutList = page.frontmatter.links || [];
      linksOutList.forEach(slug => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#';
        a.className = 'wiki-link';
        a.textContent = slug;
        a.addEventListener('click', e => {
          e.preventDefault();
          const linkedPage = wiki.pages.find(p => p.slug === slug);
          if (linkedPage) showPage(linkedPage);
        });
        li.appendChild(a);
        linksOut.appendChild(li);
      });

      // Linked from
      linkedFrom.innerHTML = '';
      const linkedFromList = wiki.pages.filter(p => p.frontmatter.links && p.frontmatter.links.includes(page.slug));
      linkedFromList.forEach(p => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = '#';
        a.className = 'wiki-link';
        a.textContent = p.slug;
        a.addEventListener('click', e => {
          e.preventDefault();
          showPage(p);
        });
        li.appendChild(a);
        linkedFrom.appendChild(li);
      });

      // Sources
      sourcesList.innerHTML = '';
      const sources = page.frontmatter.sources || [];
      sources.forEach(id => {
        const li = document.createElement('li');
        const doc = library[id];
        if (doc) {
          const a = document.createElement('a');
          a.href = doc.url || '#';
          a.className = 'wiki-link';
          a.textContent = doc.symbol || `${doc.author} ${doc.year}`;
          a.target = '_blank';
          li.appendChild(a);
        } else {
          const span = document.createElement('span');
          span.className = 'wiki-link';
          span.textContent = id;
          li.appendChild(span);
        }
        sourcesList.appendChild(li);
      });
    }

    function renderMarkdown(markdown) {
      // Headers
      markdown = markdown.replace(/^# (.*$)/gm, '<h2>$1</h2>');
      markdown = markdown.replace(/^## (.*$)/gm, '<h3>$1</h3>');
      markdown = markdown.replace(/^### (.*$)/gm, '<h4>$1</h4>');

      // Lists
      markdown = markdown.replace(/^\* (.*$)/gm, '<ul><li>$1</li></ul>');
      markdown = markdown.replace(/^\d+\. (.*$)/gm, '<ol><li>$1</li></ol>');
      markdown = markdown.replace(/<\/ul>\s*<ul>/g, '');
      markdown = markdown.replace(/<\/ol>\s*<ol>/g, '');

      // Links
      markdown = markdown.replace(/\[\[([^\]]+)\]\]/g, (match, slug) => {
        const page = wiki.pages.find(p => p.slug === slug);
        if (page) {
          return `<a href="#" class="wiki-link">${slug}</a>`;
        } else {
          return `<span class="wiki-link" style="color: var(--accent); text-decoration: line-through;">${slug}</span>`;
        }
      });

      // Pins
      const pinRegex = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
      markdown = markdown.replace(pinRegex, (match, label, id, page, quote, mark) => {
        const doc = library[id];
        if (!doc) return `<span class="pin"><span class="pin-quote">"${quote || ''}"</span> <span class="pin-chip" data-mark="${mark}" style="background: #666;">${label} (missing doc)</span></span>`;

        const passage = doc.passages.find(p => p.page == page);
        let isVerified = false;
        if (passage) {
          const passageText = normalizeText(passage.text);
          const quoteText = normalizeText(quote);
          if (quoteText.includes('…')) {
            // Split on "…" and check each fragment in order
            const fragments = quoteText.split('…').map(f => f.trim()).filter(f => f);
            let lastIndex = 0;
            isVerified = fragments.every(fragment => {
              const index = passageText.indexOf(normalizeText(fragment), lastIndex);
              if (index === -1) return false;
              lastIndex = index + fragment.length;
              return true;
            });
          } else {
            isVerified = passageText.includes(quoteText);
          }
        }

        const chip = document.createElement('span');
        chip.className = 'pin-chip';
        chip.textContent = label;
        chip.setAttribute('data-mark', mark);
        chip.addEventListener('click', () => {
          if (doc && passage) {
            studio.openSource(id, parseInt(page), quote || passage.text);
          }
        });

        return `<span class="pin"><span class="pin-quote">"${quote || ''}"</span> ${chip.outerHTML}</span>`;
      });

      // Contested blocks
      const contestedRegex = /```contested\n([\s\S]+?)```/g;
      markdown = markdown.replace(contestedRegex, (match, block) => {
        const lines = block.split('\n').filter(line => line.trim());
        let claim = '', verdict = '', note = '';
        const entries = [];
        lines.forEach(line => {
          if (line.startsWith('claim:')) claim = line.substring(6).trim();
          else if (line.startsWith('verdict:')) verdict = line.substring(8).trim();
          else if (line.startsWith('note:')) note = line.substring(5).trim();
          else if (line.match(/^[+~-] [a-f] \|/)) entries.push(line);
        });

        const card = document.createElement('div');
        card.className = 'contested-card';
        card.innerHTML = `
          <h4>${claim}</h4>
          <div class="contested-verdict">${verdict}</div>
          <div class="contested-note">${note}</div>
        `;

        entries.forEach(entry => {
          const parts = entry.split(' | ');
          const mark = parts[0][0];
          const reg = parts[0][2];
          const pin = parts[1];
          const gloss = parts[2];
          const link = parts[3];

          const div = document.createElement('div');
          div.className = 'contested-entry';
          div.setAttribute('data-mark', mark);
          div.innerHTML = `
            <span class="contested-gloss">${gloss}</span>
            <span class="wiki-link">${link}</span>
          `;
          card.appendChild(div);
        });

        return card.outerHTML;
      });

      return markdown;
    }

    function normalizeText(text) {
      if (!text) return '';
      return text
        .replace(/[\u2018\u2019]/g, "'")
        .replace(/[\u201C\u201D]/g, '"')
        .replace(/[\u2013\u2014]/g, '-')
        .replace(/\s+/g, ' ')
        .trim();
    }

    // Check tab
    function updateCheckTab() {
      // Count verified pins
      let verifiedCount = 0;
      const pinRegex = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
      wiki.pages.forEach(page => {
        let match;
        while ((match = pinRegex.exec(page.body)) !== null) {
          const [_, label, id, pageNum, quote, mark] = match;
          const doc = library[id];
          if (doc) {
            const passage = doc.passages.find(p => p.page == pageNum);
            if (passage) {
              const passageText = normalizeText(passage.text);
              const quoteText = normalizeText(quote);
              if (quoteText.includes('…')) {
                const fragments = quoteText.split('…').map(f => f.trim()).filter(f => f);
                let lastIndex = 0;
                const isVerified = fragments.every(fragment => {
                  const index = passageText.indexOf(normalizeText(fragment), lastIndex);
                  if (index === -1) return false;
                  lastIndex = index + fragment.length;
                  return true;
                });
                if (isVerified) verifiedCount++;
              } else {
                if (passageText.includes(quoteText)) verifiedCount++;
              }
            }
          }
        }
      });
      verifiedPinsCount.textContent = verifiedCount;

      // Lint table
      lintRows.innerHTML = '';

      // Dangling links
      const allSlugs = new Set(wiki.pages.map(p => p.slug));
      const danglingLinks = [];
      wiki.pages.forEach(page => {
        const links = (page.frontmatter.links || []).filter(slug => !allSlugs.has(slug));
        if (links.length > 0) {
          danglingLinks.push({page: page.slug, links});
        }
      });
      if (danglingLinks.length > 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>Dangling links (link to a page that does not exist)</td>
          <td>${danglingLinks.map(d => `${d.page}: ${d.links.join(', ')}`).join('<br>')}</td>
          <td>${danglingLinks.length}</td>
        `;
        lintRows.appendChild(row);
      }

      // Orphan pages
      const linkedFromMap = {};
      wiki.pages.forEach(page => {
        (page.frontmatter.links || []).forEach(slug => {
          if (!linkedFromMap[slug]) linkedFromMap[slug] = [];
          linkedFromMap[slug].push(page.slug);
        });
      });
      const orphanPages = wiki.pages.filter(page => !linkedFromMap[page.slug] && page.frontmatter.links && page.frontmatter.links.length > 0);
      if (orphanPages.length > 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>Orphan pages (linked from nowhere, but link out)</td>
          <td>${orphanPages.map(p => p.slug).join(', ')}</td>
          <td>${orphanPages.length}</td>
        `;
        lintRows.appendChild(row);
      }

      // Failed pins
      const failedPins = [];
      wiki.pages.forEach(page => {
        const pinRegex = /\[([^\]]+)\]\(pin:([^#\s)]+)#p(\d+)(?: "([^"]*)")?\) ?(✓|⚠)/g;
        let match;
        while ((match = pinRegex.exec(page.body)) !== null) {
          const [_, label, id, pageNum, quote, mark] = match;
          const doc = library[id];
          if (!doc) {
            failedPins.push({page: page.slug, label, id, reason: 'document not in library'});
            continue;
          }
          const passage = doc.passages.find(p => p.page == pageNum);
          if (!passage) {
            failedPins.push({page: page.slug, label, id, reason: 'page not in document'});
            continue;
          }
          const passageText = normalizeText(passage.text);
          const quoteText = normalizeText(quote);
          if (quoteText.includes('…')) {
            const fragments = quoteText.split('…').map(f => f.trim()).filter(f => f);
            let lastIndex = 0;
            const isVerified = fragments.every(fragment => {
              const index = passageText.indexOf(normalizeText(fragment), lastIndex);
              if (index === -1) return false;
              lastIndex = index + fragment.length;
              return true;
            });
            if (!isVerified) {
              failedPins.push({page: page.slug, label, id, reason: 'quote fragments not found in order'});
            }
          } else {
            if (!passageText.includes(quoteText)) {
              failedPins.push({page: page.slug, label, id, reason: 'quote not found'});
            }
          }
        }
      });
      if (failedPins.length > 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>Failed pins (quote not found in the passage)</td>
          <td>${failedPins.map(f => `${f.page}: ${f.label} (${f.reason})`).join('<br>')}</td>
          <td>${failedPins.length}</td>
        `;
        lintRows.appendChild(row);
      }

      // Source mismatch
      const sourceMismatches = [];
      wiki.pages.forEach(page => {
        (page.frontmatter.sources || []).forEach(id => {
          if (!library[id]) {
            sourceMismatches.push({page: page.slug, id, reason: 'source not in library'});
          }
        });
      });
      if (sourceMismatches.length > 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>Source mismatch (source in frontmatter but not in library)</td>
          <td>${sourceMismatches.map(s => `${s.page}: ${s.id}`).join('<br>')}</td>
          <td>${sourceMismatches.length}</td>
        `;
        lintRows.appendChild(row);
      }

      // Contested not in tensions
      const tensions = wiki.tensions.split('###').slice(1).map(t => t.trim().split('\n')[0].trim());
      const contestedNotInTensions = [];
      wiki.pages.forEach(page => {
        if (page.body.includes('```contested')) {
          const title = page.title;
          if (!tensions.includes(title)) {
            contestedNotInTensions.push(page.slug);
          }
        }
      });
      if (contestedNotInTensions.length > 0) {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>Contested cards not in tensions register</td>
          <td>${contestedNotInTensions.join(', ')}</td>
          <td>${contestedNotInTensions.length}</td>
        `;
        lintRows.appendChild(row);
      }
    }

    // Record tab
    function updateRecordTab() {
      // Log
      logEntries.innerHTML = '';
      const logLines = wiki.log.split('\n').filter(line => line.trim());
      const logEntriesList = [];
      let currentEntry = null;
      logLines.forEach(line => {
        if (line.startsWith('## ')) {
          if (currentEntry) logEntriesList.push(currentEntry);
          currentEntry = {date: line.substring(3, 13), title: line.substring(14), body: []};
        } else if (currentEntry) {
          currentEntry.body.push(line);
        }
      });
      if (currentEntry) logEntriesList.push(currentEntry);
      logEntriesList.reverse().forEach(entry => {
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.innerHTML = `
          <div class="log-date">${entry.date}</div>
          <div>${entry.title}</div>
          <div>${entry.body.join('<br>')}</div>
        `;
        logEntries.appendChild(div);
      });

      // Tensions
      tensionEntries.innerHTML = '';
      const tensionBlocks = wiki.tensions.split('###').slice(1);
      tensionBlocks.forEach(block => {
        const lines = block.trim().split('\n');
        const title = lines[0].trim();
        const body = lines.slice(1).join('\n').trim();
        const div = document.createElement('div');
        div.className = 'tension-entry';
        div.innerHTML = `
          <div class="tension-title">${title}</div>
          <div>${body.replace(/\n/g, '<br>')}</div>
        `;
        tensionEntries.appendChild(div);
      });
    }

    // Download
    downloadWiki.addEventListener('click', () => {
      const data = JSON.stringify(wiki, null, 2);
      const blob = new Blob([data], {type: 'application/json'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'wiki-neurotechnology-justice.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });

    // Init
    updateFilterUI();
    updatePageList();
  </script>
</body>
</html>
```