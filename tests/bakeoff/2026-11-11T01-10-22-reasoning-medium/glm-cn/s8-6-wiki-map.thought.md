A new tab MAP, mostly additive — but it requires edits to tabs (add tab button, panel, add to tabs array), and a new section. I'll provide edits. Layout: deterministic — e.g., circular layout grouped by type, or degree-based radial. Simplest deterministic: group nodes by type in concentric rings or columns; place by sorted order on a circle. I'll do: nodes sorted by in-degree descending, placed on a circle in one ring ordered by type groups. Deterministic, fine.

Edits needed:
1. Add tab button after tab-record in tabs div.
2. Add panel section after panel-record.
3. Update tabs JS selector — `document.querySelectorAll('.tab')` still works since it selects all.
4. Add MAP rendering code.
5. Update selectTab keyboard — works generically.

Also "Open this page" button on click, highlight neighbours. SVG ~900x700 viewBox.

Placement: order pages by type groups (source, concept, entity, question), then by title, then place on a circle per group at different radii. Or a single circle ordered by type then title — fine and deterministic. Size by in-degree (linked-from count).

Implement in a script block appended before the closing IIFE? My script is one IIFE ending with the RECORD tab. I'll add MAP code after RECORD section inside the IIFE via edit at the end: search for the closing `})();\n})();` and insert MAP code.

Careful with edges count: links where target exists, exclude self-links; count distinct? Just count each link once. Duplicates possible—count edges as unique pairs.

Hover tooltip: use a foreign title in SVG group — use a <title> element or an HTML div positioned. Simpler: an SVG text panel fixed at top-right showing info, or a div tooltip following mouse. I'll use a div tooltip.

Click: highlight neighbours, show an info box with "Open this page" button (an HTML overlay below/above map, fixed area). Simplest: a side panel (HTML) next to SVG showing selected node info with open button.

Let me write edits.

Edit 1: tab button.
Edit 2: panel section.
Edit 3: MAP code inserted before final `})();`.

Code sketch:

```js
/* ---------- TAB 04 : MAP ---------- */
(function(){
  const TYPE_COLORS={source:'#5a7d6c',concept:'#9b2335',entity:'#8a6d3b',question:'#3b5a8a'};
  const W_=W;
  const nodes=pages.map(p=>{
    const linksOut=(p.frontmatter.links||[]).filter(l=>l!==p.slug&&bySlug.has(l));
    return {slug:p.slug,title:p.title||p.slug,type:p.type,out:linksOut};
  });
  const inCount=new Map(nodes.map(n=>[n.slug,0]));
  nodes.forEach(n=>n.out.forEach(l=>inCount.set(l,(inCount.get(l)||0)+1)));
  const edges=[];
  const seen=new Set();
  nodes.forEach(n=>n.out.forEach(l=>{const k=[n.slug,l].sort().join('|'); if(!seen.has(k)){seen.add(k);edges.push([n.slug,l]);}}));
  // deterministic layout: group by type, sort by title, place on one circle
  const order=nodes.slice().sort((a,b)=> a.type===b.type ? a.title.localeCompare(b.title) : TYPES.indexOf(a.type)-TYPES.indexOf(b.type));
  const R=280, CX=450, CY=330;
  const pos=new Map();
  order.forEach((n,i)=>{const a=(i/order.length)*2*Math.PI - Math.PI/2;
    pos.set(n.slug,{x:CX+R*Math.cos(a),y:CY+R*Math.sin(a)});});
  ...
```

TYPES variable exists in the Pages section scope (declared with `let TYPES=['source','concept','entity','question'];` inside IIFE) — yes accessible. bySlug accessible. showPage accessible.

Render SVG with lines then circles+labels. Node radius 8+3*inDegree capped. Labels: small text under node, maybe only on hover/selection to avoid clutter; show all titles small (40 nodes is a lot). Show title text at 9px, truncated. Hover shows full title in tooltip.

Highlight: clicking sets class dim on others; info panel shows title, in/out counts, "Open this page" button (calls showPage(slug) and selectTab(0)).

Bottom line: pages count, links count, orphans clickable — reuse linkedFrom? Orphan logic already in lint; recompute: nodes with out 0 and in 0.

Tooltip: HTML div absolutely positioned in a relative container; mousemove updates.

Edge count display: edges.length (unique pairs).

Write the SVG string, then attach listeners via querySelectorAll.

Let me write final edits compactly. Keep code reasonably short.

Node labels: draw text for each node, rotate? Just place title below node with text-anchor middle, font 9px mono, truncated to 18 chars. 40 labels on a circle — acceptable.

Interactions:
- mouseenter node → tooltip div shows title, in N / out M; update on hover.
- click → selected; dim non-neighbours; info panel visible with title, counts, open button.

CSS additions needed: .mapwrap{position:relative}, .map-tip, .dim{opacity:.15}, .node circle cursor pointer. Add CSS via edit in style block.

Edits:
1. CSS: after `.ok-note` rule add map styles.
2. Tab button.
3. Panel section.
4. JS before final close.

For the tab numbering: "01 PAGES · 02 CHECK · 03 RECORD · 04 MAP" — insert MAP tab after 03. selectTab indices auto.

Write JS:

```js
/* ---------- TAB 04 : MAP ---------- */
(function(){
  const COLORS={source:'#5a7d6c',concept:'#9b2335',entity:'#8a6d3b',question:'#3b5a8a'};
  const nodes=pages.map(p=>{
    const out=(p.frontmatter.links||[]).filter(l=>l!==p.slug&&bySlug.has(l));
    return {slug:p.slug,title:p.title||p.slug,type:COLORS[p.type]?p.type:'other',out};
  });
  const bySlugMap=new Map(nodes.map(n=>[n.slug,n]));
  const inC=new Map(nodes.map(n=>[n.slug,0]));
  nodes.forEach(n=>n.out.forEach(l=>inC.set(l,inC.get(l)+1)));
  const seen=new Set(),edges=[];
  nodes.forEach(n=>n.out.forEach(l=>{const k=[n.slug,l].sort().join('\u0001');
    if(!seen.has(k)){seen.add(k);edges.push([n.slug,l]);}}));
  const order=nodes.slice().sort((a,b)=>a.type===b.type
      ?a.title.localeCompare(b.title)
      :TYPES.indexOf(a.type)-TYPES.indexOf(b.type));
  const R=300,CX=460,CY=340,pos=new Map();
  order.forEach((n,i)=>{const a=2*Math.PI*i/order.length-Math.PI/2;
    pos.set(n.slug,{x:CX+R*Math.cos(a),y:CY+R*Math.sin(a)});});
  let svg='<svg viewBox="0 0 920 700" role="img" aria-label="Wiki map" style="width:100%;max-width:920px;display:block">';
  edges.forEach(([a,b])=>{const p=pos.get(a),q=pos.get(b);
    svg+='<line class="edge" data-a="'+esc(a)+'" data-b="'+esc(b)+'" x1="'+p.x.toFixed(1)+'" y1="'+p.y.toFixed(1)+'" x2="'+q.x.toFixed(1)+'" y2="'+q.y.toFixed(1)+'" stroke="#d9d2c3" stroke-width="1"/>';});
  order.forEach(n=>{const p=pos.get(n.slug),r=7+3*(inC.get(n.slug)||0);
    const t=n.title.length>22?n.title.slice(0,21)+'…':n.title;
    svg+='<g class="node" data-slug="'+esc(n.slug)+'" tabindex="0" role="button">'
      +'<circle cx="'+p.x.toFixed(1)+'" cy="'+p.y.toFixed(1)+'" r="'+r+'" fill="'+COLORS[n.type]+'">'
      +'<title>'+esc(n.title)+'</title></circle>'
      +'<text x="'+p.x.toFixed(1)+'" y="'+(p.y+r+13).toFixed(1)+'" text-anchor="middle" font-size="9.5" font-family="ui-monospace,Menlo,Consolas,monospace" fill="#57524a">'+esc(t)+'</text></g>';});
  svg+='</svg>';
  const orphans=nodes.filter(n=>!n.out.length&&!(inC.get(n.slug)||0));
  let h='<p class="fig">FIG.02 · MAP</p>'
    +'<p class="how">one circle per page, coloured by type · radius grows with the number of pages linking in · fixed layout computed by this code (type groups, then alphabetical), so the map is identical every time</p>'
    +'<div class="mapwrap">'+svg+'<div id="maptip" class="map-tip" hidden></div></div>'
    +'<div id="mapinfo" hidden></div>'
    +'<p class="how">'+nodes.length+' pages · '+edges.length+' links (unique pairs; dangling links are not drawn)</p>'
    +(orphans.length?'<p class="how">No other page links to: '+orphans.map(o=>pageBtn(o.slug,o.title)).join(' · ')+'</p>':'<p class="ok-note">\u2713 every page is linked to</p>');
  const panel=document.getElementById('panel-map');
  panel.innerHTML=h;
  const tip=panel.querySelector('#maptip');
  panel.querySelectorAll('.node').forEach(g=>{
    const slug=g.dataset.slug,n=bySlugMap.get(slug);
    const show=()=>{tip.hidden=false;
      tip.innerHTML='<strong>'+esc(n.title)+'</strong><br>'+esc(n.type)+' · '+
        (inC.get(slug)||0)+' in · '+n.out.length+' out';};
    g.addEventListener('mouseenter',e=>{show();move(e);});
    g.addEventListener('mousemove',move);
    g.addEventListener('mouseleave',()=>{tip.hidden=true;});
    g.addEventListener('focus',show);
    g.addEventListener('blur',()=>{tip.hidden=true;});
    function move(e){const r=panel.querySelector('.mapwrap').getBoundingClientRect();
      tip.style.left=Math.min(e.clientX-r.left+14,r.width-220)+'px';
      tip.style.top=(e.clientY-r.top+14)+'px';}
    g.addEventListener('click',()=>selectMap(slug));
    g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectMap(slug);}});
  });
  function selectMap(slug){
    const n=bySlugMap.get(slug);
    const neigh=new Set([slug,...n.out]);
    nodes.forEach(m=>{if(neigh.has(m.slug))neigh.add(...m.out.filter(x=>x===slug));});
    const keep=new Set([slug,...n.out,...nodes.filter(m=>m.out.includes(slug)).map(m=>m.slug)]);
    panel.querySelectorAll('.edge').forEach(el=>{
      el.style.opacity=(keep.has(el.dataset.a)&&keep.has(el.dataset.b))?1:0.12;});
    panel.querySelectorAll('.node').forEach(el=>{
      el.classList.toggle('dim',!keep.has(el.dataset.slug));});
    const info=panel.querySelector('#mapinfo');
    info.hidden=false;
    info.innerHTML='<div class="card"><span class="verdict">'+esc(n.type)+'</span><strong>'+esc(n.title)+'</strong>'
      +'<p class="how">'+(inC.get(slug)||0)+' pages link in · links out to '+n.out.length+' pages</p>'
      +'<button class="pinchip" id="mapopen" style="font-size:12px;padding:5px 12px">OPEN THIS PAGE</button></div>';
    info.querySelector('#mapopen').addEventListener('click',()=>{selectTab(0);showPage(slug);});
  }
})();
```

Remove stray line `nodes.forEach(m=>{...})` (dead). Keep clean. Also hovering again with selected works fine.

CSS:
```
.mapwrap{position:relative;max-width:920px}
.map-tip{position:absolute;background:#fffdf7;border:1px solid var(--rule);padding:6px 10px;font-size:13px;pointer-events:none;max-width:220px;box-shadow:none}
.node{cursor:pointer}
.node.dim{opacity:.15}
.node:focus-visible circle{outline:none;stroke:#9b2335;stroke-width:3}
```
stroke on circle works via focus ring on circle child? :focus-visible on g... use `.node:focus circle{stroke:#1d1b18;stroke-width:2}`. Simpler: `.node:focus circle{stroke:#1d1b18;stroke-width:2}`. But focus ring visibility requirement — acceptable.

Now edits.