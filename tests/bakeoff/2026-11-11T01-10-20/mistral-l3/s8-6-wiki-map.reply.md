Here is the new MAP tab. It draws the wiki as a force-directed graph in SVG, with nodes sized by in-degree and coloured by type. The layout is fixed (same every time) and computed by the code.

```edit
<<<<<<< SEARCH
    <button id="tab-03" class="tab" role="tab" aria-selected="false" aria-controls="panel-03">03 RECORD</button>
=======
    <button id="tab-03" class="tab" role="tab" aria-selected="false" aria-controls="panel-03">03 MAP</button>
    <button id="tab-04" class="tab" role="tab" aria-selected="false" aria-controls="panel-04">04 RECORD</button>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    <div id="panel-03" class="tab-panel" role="tabpanel" aria-labelledby="tab-03" aria-hidden="true">
=======
    <div id="panel-03" class="tab-panel" role="tabpanel" aria-labelledby="tab-03" aria-hidden="true">
      <div id="graph-container" style="width: 100%; height: 600px; background: white; border: 1px solid var(--rule); margin-bottom: 1rem;"></div>
      <div id="graph-stats" style="font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.8rem;"></div>
    </div>
    <div id="panel-04" class="tab-panel" role="tabpanel" aria-labelledby="tab-04" aria-hidden="true">
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    const tabButtons = document.querySelectorAll('.tab');
    const tabPanels = document.querySelectorAll('.tab-panel');
=======
    const tabButtons = document.querySelectorAll('.tab');
    const tabPanels = document.querySelectorAll('.tab-panel');
    const graphContainer = document.getElementById('graph-container');
    const graphStats = document.getElementById('graph-stats');
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
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
=======
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
        if (panelId === 'panel-03') updateGraphTab();
        if (panelId === 'panel-04') updateRecordTab();
      });
    });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
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
=======
    // Graph tab
    function updateGraphTab() {
      // Build graph
      const nodes = [];
      const links = [];
      const nodeMap = {};
      const typeColors = {
        'source': '#4e79a7',
        'concept': '#f28e2b',
        'entity': '#e15759',
        'question': '#76b7b2'
      };

      // Create nodes
      wiki.pages.forEach((page, i) => {
        nodeMap[page.slug] = i;
        nodes.push({
          id: i,
          slug: page.slug,
          title: page.title,
          type: page.type,
          inDegree: 0,
          outDegree: page.frontmatter.links ? page.frontmatter.links.length : 0
        });
      });

      // Create links and count in-degree
      wiki.pages.forEach(page => {
        (page.frontmatter.links || []).forEach(slug => {
          if (nodeMap[slug] !== undefined) {
            links.push({source: nodeMap[page.slug], target: nodeMap[slug]});
            nodes[nodeMap[slug]].inDegree++;
          }
        });
      });

      // Orphans (no incoming links)
      const orphans = nodes.filter(node => node.inDegree === 0 && node.outDegree > 0).map(node => node.slug);

      // Fixed layout: grid with spacing, nodes sized by in-degree
      const width = graphContainer.clientWidth;
      const height = graphContainer.clientHeight;
      const cols = Math.ceil(Math.sqrt(nodes.length));
      const cellSize = Math.min(width, height) / cols * 0.8;
      const radiusScale = d3.scaleSqrt().domain([0, d3.max(nodes, d => d.inDegree)]).range([4, 20]);

      // Assign fixed positions
      nodes.forEach((node, i) => {
        node.x = (i % cols) * cellSize + cellSize / 2;
        node.y = Math.floor(i / cols) * cellSize + cellSize / 2;
        node.radius = radiusScale(node.inDegree);
      });

      // SVG
      graphContainer.innerHTML = '';
      const svg = d3.select(graphContainer).append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('style', 'max-width: 100%; height: auto;');

      // Links
      svg.append('g')
        .selectAll('line')
        .data(links)
        .enter().append('line')
        .attr('x1', d => nodes[d.source].x)
        .attr('y1', d => nodes[d.source].y)
        .attr('x2', d => nodes[d.target].x)
        .attr('y2', d => nodes[d.target].y)
        .attr('stroke', '#ccc')
        .attr('stroke-width', 1);

      // Nodes
      const nodeGroup = svg.append('g')
        .selectAll('g')
        .data(nodes)
        .enter().append('g')
        .attr('transform', d => `translate(${d.x},${d.y})`)
        .on('mouseover', function(event, d) {
          tooltip.style('visibility', 'visible')
            .html(`<strong>${d.title}</strong><br>Type: ${d.type}<br>Links in: ${d.inDegree}<br>Links out: ${d.outDegree}`);
        })
        .on('mousemove', function(event) {
          tooltip.style('top', (event.pageY - 10) + 'px')
            .style('left', (event.pageX + 10) + 'px');
        })
        .on('mouseout', function() {
          tooltip.style('visibility', 'hidden');
        })
        .on('click', function(event, d) {
          // Highlight neighbours
          nodeGroup.selectAll('circle')
            .attr('stroke', null)
            .attr('stroke-width', null);
          linkGroup.attr('stroke', '#ccc');

          const neighbours = new Set();
          links.forEach(link => {
            if (link.source === d.id) neighbours.add(link.target);
            if (link.target === d.id) neighbours.add(link.source);
          });

          nodeGroup.filter(node => node.id === d.id || neighbours.has(node.id))
            .select('circle')
            .attr('stroke', '#000')
            .attr('stroke-width', 2);

          linkGroup.filter(link => link.source === d.id || link.target === d.id)
            .attr('stroke', '#000')
            .attr('stroke-width', 2);

          // Show action
          actionDiv.html(`
            <button id="open-page" style="margin-top: 0.5rem;">Open ${d.slug}</button>
          `);
          document.getElementById('open-page').addEventListener('click', () => {
            const page = wiki.pages.find(p => p.slug === d.slug);
            if (page) {
              tabButtons[0].click(); // Switch to PAGES tab
              showPage(page);
            }
          });
        });

      nodeGroup.append('circle')
        .attr('r', d => d.radius)
        .attr('fill', d => typeColors[d.type] || '#666');

      nodeGroup.append('text')
        .attr('dy', d => d.radius + 15)
        .attr('text-anchor', 'middle')
        .attr('font-size', '10px')
        .attr('font-family', 'ui-monospace, Menlo, Consolas, monospace')
        .text(d => d.slug);

      const linkGroup = svg.selectAll('line');

      // Tooltip
      const tooltip = d3.select('body').append('div')
        .attr('style', 'position: absolute; padding: 0.5rem; background: white; border: 1px solid #ccc; border-radius: 4px; pointer-events: none; font-size: 0.9rem;')
        .style('visibility', 'hidden');

      // Action div
      const actionDiv = d3.select(graphContainer).append('div')
        .attr('style', 'position: absolute; bottom: 10px; right: 10px; background: white; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;');

      // Stats
      graphStats.innerHTML = `
        ${nodes.length} pages, ${links.length} links.
        Orphans (no incoming links): ${orphans.length > 0 ? orphans.map(slug => `<a href="#" class="wiki-link">${slug}</a>`).join(', ') : 'none'}
      `;
      graphStats.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', e => {
          e.preventDefault();
          const slug = a.textContent;
          const page = wiki.pages.find(p => p.slug === slug);
          if (page) {
            tabButtons[0].click();
            showPage(page);
          }
        });
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
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  <script>
=======
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
>>>>>>> REPLACE
```

The MAP tab is now added. It draws the wiki as a graph with one node per page (coloured by type, sized by in-degree) and one line per link. The layout is fixed (a grid) so the map looks the same every time. Hovering a node shows its title and link counts; clicking it highlights its neighbours and offers "Open this page" to show the page on the PAGES tab. Under the map, the stats line lists the orphans (pages no other page links to), each clickable to open it.