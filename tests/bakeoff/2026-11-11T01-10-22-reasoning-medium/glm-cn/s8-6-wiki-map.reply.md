Adding tab 04 MAP: a deterministic SVG graph (fixed layout: type groups, then alphabetical, on a circle), nodes sized by in-links and coloured by type, hover tooltips, click to highlight neighbours with an "Open this page" button, and an orphan line underneath.

```edit
<<<<<<< SEARCH
  .ok-note{font-family:var(--mono);font-size:11px;color:#2e6b3a;letter-spacing:.05em}
=======
  .ok-note{font-family:var(--mono);font-size:11px;color:#2e6b3a;letter-spacing:.05em}
  .mapwrap{position:relative;max-width:920px}
  .map-tip{position:absolute;background:#fffdf7;border:1px solid var(--rule);padding:6px 10px;font-size:13px;pointer-events:none;max-width:230px}
  .node{cursor:pointer}
  .node.dim{opacity:.15}
  .node:focus circle{stroke:#1d1b18;stroke-width:2}
  .node:focus{outline:none}
  .node:focus-visible circle{stroke:#9b2335;stroke-width:3}
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  <button class="tab" id="tab-record" role="tab" aria-selected="false" aria-controls="panel-record">03 RECORD</button>
</div>
=======
  <button class="tab" id="tab-record" role="tab" aria-selected="false" aria-controls="panel-record">03 RECORD</button>
  <button class="tab" id="tab-map" role="tab" aria-selected="false" aria-controls="panel-map">04 MAP</button>
</div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  <section id="panel-record" role="tabpanel" aria-labelledby="tab-record" hidden></section>
</main>
=======
  <section id="panel-record" role="tabpanel" aria-labelledby="tab-record" hidden></section>
  <section id="panel-map" role="tabpanel" aria-labelledby="tab-map" hidden></section>
</main>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
})();
})();
</script>
=======
})();

/* ---------- TAB 04 : MAP ---------- */
(function(){
  const COLORS={source:'#5a7d6c',concept:'#9b2335',entity:'#8a6d3b',question:'#3b5a8a'};
  const nodes=pages.map(p=>{
    const out=(p.frontmatter.links||[]).filter(l=>l!==p.slug&&bySlug.has(l));
    return {slug:p.slug,title:p.title||p.slug,type:p.type,out:out};
  });
  const nodeBy=new Map(nodes.map(n=>[n.slug,n]));
  const inC=new Map(nodes.map(n=>[n.slug,0]));
  nodes.forEach(n=>n.out.forEach(l=>inC.set(l,inC.get(l)+1)));
  const seen=new Set(),edges=[];
  nodes.forEach(n=>n.out.forEach(l=>{
    const k=[n.slug,l].sort().join('\u0001');
    if(!seen.has(k)){seen.add(k);edges.push([n.slug,l]);}
  }));
  /* fixed layout: grouped by type, alphabetical within group, on one circle */
  const order=nodes.slice().sort((a,b)=> a.type===b.type
    ? a.title.localeCompare(b.title)
    : TYPES.indexOf(a.type)-TYPES.indexOf(b.type));
  const R=300,CX=460,CY=340,pos=new Map();
  order.forEach((n,i)=>{const a=2*Math.PI*i/order.length-Math.PI/2;
    pos.set(n.slug,{x:CX+R*Math.cos(a),y:CY+R*Math.sin(a)});});
  let svg='<svg viewBox="0 0 920 700" role="img" aria-label="Map of wiki pages and their links" style="width:100%;max-width:920px;display:block">';
  edges.forEach(function(pair){const p=pos.get(pair[0]),q=pos.get(pair[1]);
    svg+='<line class="edge" data-a="'+esc(pair[0])+'" data-b="'+esc(pair[1])
      +'" x1="'+p.x.toFixed(1)+'" y1="'+p.y.toFixed(1)+'" x2="'+q.x.toFixed(1)+'" y2="'+q.y.toFixed(1)
      +'" stroke="#d9d2c3" stroke-width="1"/>';});
  order.forEach(function(n){
    const p=pos.get(n.slug),r=7+3*(inC.get(n.slug)||0);
    const t=n.title.length>22?n.title.slice(0,21)+'\u2026':n.title;
    svg+='<g class="node" data-slug="'+esc(n.slug)+'" tabindex="0" role="button" aria-label="'+esc(n.title)+'">'
      +'<circle cx="'+p.x.toFixed(1)+'" cy="'+p.y.toFixed(1)+'" r="'+r+'" fill="'+(COLORS[n.type]||'#8a8172')+'">'
      +'<title>'+esc(n.title)+'</title></circle>'
      +'<text x="'+p.x.toFixed(1)+'" y="'+(p.y+r+13).toFixed(1)+'" text-anchor="middle" font-size="9.5" '
      +'font-family="ui-monospace,Menlo,Consolas,monospace" fill="#57524a">'+esc(t)+'</text></g>';
  });
  svg+='</svg>';
  const orphans=nodes.filter(n=>!n.out.length&&!(inC.get(n.slug)||0));
  let h='<p class="fig">FIG.02 \u00b7 MAP</p>'
    +'<p class="how">one circle per page, coloured by type (green source \u00b7 red concept \u00b7 ochre entity \u00b7 blue question) \u00b7 radius grows with the number of pages linking in \u00b7 fixed layout computed by this code (type groups, alphabetical within each), so the map is identical every time \u00b7 hover = title and link counts, click = highlight neighbours</p>'
    +'<div class="mapwrap">'+svg+'<div id="maptip" class="map-tip" hidden></div></div>'
    +'<div id="mapinfo" hidden></div>'
    +'<p class="how">'+nodes.length+' pages \u00b7 '+edges.length+' links (unique pairs; dangling [[links]] are not drawn)</p>'
    +(orphans.length
      ?'<p class="how">No other page links to: '+orphans.map(function(o){return pageBtn(o.slug,o.title);}).join(' \u00b7 ')+'</p>'
      :'<p class="ok-note">\u2713 every page is linked to</p>');
  const panel=document.getElementById('panel-map');
  panel.innerHTML=h;
  const tip=panel.querySelector('#maptip'),wrap=panel.querySelector('.mapwrap');
  panel.querySelectorAll('.node').forEach(function(g){
    const slug=g.dataset.slug,n=nodeBy.get(slug);
    function show(){tip.hidden=false;
      tip.innerHTML='<strong>'+esc(n.title)+'</strong><br>'+esc(n.type)+' \u00b7 '
        +(inC.get(slug)||0)+' in \u00b7 '+n.out.length+' out';}
    function move(e){const r=wrap.getBoundingClientRect();
      tip.style.left=Math.min(e.clientX-r.left+14,Math.max(10,r.width-240))+'px';
      tip.style.top=(e.clientY-r.top+14)+'px';}
    g.addEventListener('mouseenter',function(e){show();move(e);});
    g.addEventListener('mousemove',move);
    g.addEventListener('mouseleave',function(){tip.hidden=true;});
    g.addEventListener('focus',show);
    g.addEventListener('blur',function(){tip.hidden=true;});
    g.addEventListener('click',function(){selectMap(slug);});
    g.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();selectMap(slug);}});
  });
  function selectMap(slug){
    const n=nodeBy.get(slug);
    const keep=new Set([slug].concat(n.out,
      nodes.filter(function(m){return m.out.includes(slug);}).map(function(m){return m.slug;})));
    panel.querySelectorAll('.edge').forEach(function(el){
      el.style.opacity=(keep.has(el.dataset.a)&&keep.has(el.dataset.b))?1:0.12;});
    panel.querySelectorAll('.node').forEach(function(el){
      el.classList.toggle('dim',!keep.has(el.dataset.slug));});
    const info=panel.querySelector('#mapinfo');
    info.hidden=false;
    info.innerHTML='<div class="card"><span class="verdict">'+esc(n.type)+'</span><strong>'+esc(n.title)+'</strong>'
      +'<p class="how">'+(inC.get(slug)||0)+' pages link in \u00b7 this page links out to '+n.out.length+' pages</p>'
      +'<button class="pinchip" id="mapopen" style="font-size:12px;padding:5px 12px">OPEN THIS PAGE</button></div>';
    info.querySelector('#mapopen').addEventListener('click',function(){
      selectTab(0);showPage(slug);});
  }
})();
})();
</script>
>>>>>>> REPLACE
```