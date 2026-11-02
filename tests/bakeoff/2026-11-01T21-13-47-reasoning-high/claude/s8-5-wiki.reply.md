I built a concept wiki over the nine General Comments, with your seven starting concepts in the sidebar and a box to add your own. Matching is by wording (case-insensitive, with the variants shown on each page), not by meaning. The summary is sent to the model only when you click the button, and the page shows how many paragraphs were sent.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Concept wiki: nine General Comments</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *{box-sizing:border-box}
  body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:#f6f8fa;color:#1d2733}
  header{background:#fff;border-bottom:1px solid #d9e0e7;padding:18px 28px}
  h1{margin:0 0 4px;font-size:1.6rem}
  .sub{margin:0;color:#4a5a6a}
  .layout{display:grid;grid-template-columns:290px minmax(0,1fr);gap:24px;padding:24px 28px;max-width:1300px;margin:0 auto}
  @media(max-width:820px){.layout{grid-template-columns:1fr}}
  aside{background:#fff;border:1px solid #d9e0e7;border-radius:8px;padding:16px;align-self:start;position:sticky;top:12px}
  @media(max-width:820px){aside{position:static}}
  aside h2{font-size:1rem;margin:0 0 10px;text-transform:uppercase;letter-spacing:.04em;color:#4a5a6a}
  .clist{list-style:none;margin:0 0 14px;padding:0}
  .clist li{display:flex;gap:4px;margin-bottom:4px}
  .clist .c{flex:1;text-align:left;background:none;border:1px solid transparent;border-radius:6px;padding:7px 10px;font:inherit;cursor:pointer;color:#1f6fb2;display:flex;justify-content:space-between;gap:8px}
  .clist .c:hover{background:#eef5fb}
  .clist .c.on{background:#1f6fb2;color:#fff}
  .clist .n{opacity:.8;font-variant-numeric:tabular-nums}
  .clist .x{background:none;border:none;color:#7a8794;cursor:pointer;font-size:1.1rem;padding:0 6px}
  form{display:flex;gap:6px}
  input[type=text]{flex:1;min-width:0;font:inherit;padding:8px 10px;border:1px solid #b9c4cf;border-radius:6px}
  button.pri{font:inherit;background:#1f6fb2;color:#fff;border:none;border-radius:6px;padding:8px 14px;cursor:pointer}
  button.pri:disabled{background:#9db8cf;cursor:default}
  button.sec{font:inherit;background:#fff;color:#1f6fb2;border:1px solid #1f6fb2;border-radius:6px;padding:6px 12px;cursor:pointer}
  .hint{font-size:.88rem;color:#5b6b7b;margin:8px 0 0}
  main{min-width:0}
  .card{background:#fff;border:1px solid #d9e0e7;border-radius:8px;padding:18px 20px;margin-bottom:18px}
  h2.t{margin:0 0 6px;font-size:1.5rem;text-transform:capitalize}
  .note{font-size:.9rem;color:#4a5a6a;background:#f1f6fa;border-left:3px solid #1f6fb2;padding:8px 12px;margin:10px 0;border-radius:0 6px 6px 0}
  .doc{margin-bottom:22px}
  .doc h3{margin:0 0 8px;font-size:1.05rem;padding-bottom:6px;border-bottom:2px solid #1f6fb2}
  .doc h3 a{color:#1f6fb2;font-weight:700}
  .doc h3 span{font-weight:400;color:#4a5a6a}
  .para{border:1px solid #e3e9ee;border-radius:6px;padding:10px 12px;margin-bottom:10px;background:#fcfdfe}
  .meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:6px;font-size:.9rem}
  .pbtn{font:inherit;font-size:.9rem;background:#eef5fb;color:#1f6fb2;border:1px solid #b6d3ea;border-radius:5px;padding:2px 9px;cursor:pointer;font-weight:600}
  .pbtn:hover{background:#dcebf7}
  .chip{font-size:.78rem;background:#eef1f4;color:#4a5a6a;border-radius:10px;padding:1px 8px}
  .ptext{white-space:pre-wrap}
  .ptext.clamp{display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}
  mark{background:#ffe9a8;padding:0 1px;border-radius:2px}
  .more{background:none;border:none;color:#1f6fb2;cursor:pointer;font:inherit;font-size:.9rem;padding:4px 0 0}
  .rel{display:flex;flex-wrap:wrap;gap:8px}
  .rel button{font:inherit;background:#eef5fb;color:#1f6fb2;border:1px solid #b6d3ea;border-radius:16px;padding:4px 12px;cursor:pointer}
  .rel button small{color:#4a5a6a}
  .ai{border:1px dashed #1f6fb2;border-radius:6px;padding:12px 14px;background:#f7fbff;margin-top:10px}
  .badge{display:inline-block;background:#1f6fb2;color:#fff;font-size:.78rem;font-weight:700;border-radius:4px;padding:1px 8px;margin-right:6px;letter-spacing:.03em}
  .cite{font:inherit;background:none;border:none;color:#1f6fb2;text-decoration:underline;cursor:pointer;padding:0}
  .cite.bad{color:#b3261e}
  .err{color:#b3261e}
  .empty{color:#4a5a6a;font-style:italic}
  .bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
</style>
</head>
<body>
<header>
  <h1>Concept wiki: nine General Comments</h1>
  <p class="sub" id="desc"></p>
</header>
<div class="layout">
  <aside>
    <h2>Concept pages</h2>
    <ul class="clist" id="clist"></ul>
    <form id="addForm">
      <input type="text" id="term" placeholder="Add a concept…" aria-label="New concept term">
      <button class="pri" type="submit">Add</button>
    </form>
    <p class="hint">Type a word or phrase. Separate several wordings with commas, e.g. <i>torture, ill-treatment</i>. Counts are paragraphs that use the term.</p>
  </aside>
  <main id="main"></main>
</div>

<script>
(function(){
  const D = window.WORKSHOP_DATA || {};
  const LIB = D.un_library || {};
  const docs = Array.isArray(LIB.records) ? LIB.records : [];
  const MAXSEND = 12;

  // flat list of every paragraph with its document
  const flat = [];
  docs.forEach(d => (d.paragraphs || []).forEach(p => flat.push({d, p})));

  function h(tag, attrs, ...kids){
    const e = document.createElement(tag);
    if (attrs) for (const k in attrs){
      if (k === 'class') e.className = attrs[k];
      else if (k.startsWith('on')) e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    }
    kids.flat().forEach(c => { if (c == null || c === false) return; e.append(c.nodeType ? c : document.createTextNode(String(c))); });
    return e;
  }
  const SEP = '[\\s\\-\\u2010\\u2011\\u2013]+';
  function esc(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function variantPattern(v){
    return v.trim().split(/[\s\-\u2010\u2011\u2013]+/).filter(Boolean).map(esc).join(SEP);
  }
  function buildRegex(variants){
    const pats = variants.map(variantPattern).filter(Boolean).sort((a,b) => b.length - a.length);
    if (!pats.length) return null;
    return new RegExp('(?<![A-Za-z])(?:' + pats.join('|') + ')(?:s|es)?(?![A-Za-z])', 'gi');
  }

  const concepts = [];
  function addConcept(name, variants, builtin){
    const c = {id: 'c' + concepts.length + '_' + Date.now(), name, variants, builtin};
    c.re = buildRegex(variants);
    c.hits = [];
    flat.forEach((x, i) => {
      if (!c.re) return;
      c.re.lastIndex = 0;
      if (c.re.test(x.p.text || '')) c.hits.push(i);
    });
    c.set = new Set(c.hits);
    concepts.push(c);
    return c;
  }
  [
    ['proportionality', ['proportionality','proportionate','proportional']],
    ['legal capacity', ['legal capacity']],
    ['surveillance', ['surveillance']],
    ['non-State actors', ['non-State actor','non-State entities']],
    ['reasonable accommodation', ['reasonable accommodation']],
    ['access to information', ['access to information']],
    ['deprivation of liberty', ['deprivation of liberty','deprived of their liberty','deprived of liberty','deprived of his or her liberty']]
  ].forEach(([n, v]) => addConcept(n, v, true));

  let currentId = concepts[0] ? concepts[0].id : null;
  const summaries = {};   // concept id -> state
  const tokens = {};      // concept id -> running token
  const expanded = new Set();

  const cur = () => concepts.find(c => c.id === currentId);

  // ---------- header ----------
  function renderHeader(){
    const years = docs.map(d => d.year).filter(y => typeof y === 'number');
    const yr = years.length ? (Math.min(...years) === Math.max(...years) ? Math.min(...years) : Math.min(...years) + '–' + Math.max(...years)) : 'years not given';
    document.getElementById('desc').textContent =
      (LIB.source ? LIB.source + ' · ' : 'UN treaty-body General Comments · ') +
      docs.length + ' documents · ' + flat.length + ' numbered paragraphs · ' + yr;
  }

  // ---------- sidebar ----------
  function renderSidebar(){
    const ul = document.getElementById('clist');
    ul.innerHTML = '';
    concepts.forEach(c => {
      const li = h('li', null,
        h('button', {class: 'c' + (c.id === currentId ? ' on' : ''), onclick: () => select(c.id)},
          h('span', null, c.name), h('span', {class: 'n'}, c.hits.length)));
      if (!c.builtin){
        li.append(h('button', {class: 'x', title: 'Remove this concept', 'aria-label': 'Remove ' + c.name, onclick: () => removeConcept(c.id)}, '×'));
      }
      ul.append(li);
    });
  }
  function select(id){ currentId = id; renderSidebar(); renderMain(); window.scrollTo(0, 0); }
  function removeConcept(id){
    const i = concepts.findIndex(c => c.id === id);
    if (i < 0) return;
    concepts.splice(i, 1);
    delete summaries[id];
    if (currentId === id) currentId = concepts[0] ? concepts[0].id : null;
    renderSidebar(); renderMain();
  }
  document.getElementById('addForm').addEventListener('submit', ev => {
    ev.preventDefault();
    const inp = document.getElementById('term');
    const raw = inp.value.trim();
    if (!raw) return;
    const variants = raw.split(',').map(s => s.trim()).filter(Boolean);
    const name = variants[0];
    const existing = concepts.find(c => c.name.toLowerCase() === name.toLowerCase());
    inp.value = '';
    if (existing){ select(existing.id); return; }
    const c = addConcept(name, variants, false);
    select(c.id);
  });

  // ---------- helpers ----------
  function openPdf(symbol, page){
    if (window.studio && typeof studio.openSource === 'function') studio.openSource(symbol, page);
    else alert('The PDF viewer is not available in this preview.');
  }
  function highlighted(text, re){
    const span = h('div', {class: 'ptext'});
    if (!re){ span.textContent = text; return span; }
    let last = 0;
    for (const m of text.matchAll(new RegExp(re.source, 'gi'))){
      if (m.index > last) span.append(text.slice(last, m.index));
      span.append(h('mark', null, m[0]));
      last = m.index + m[0].length;
    }
    if (last < text.length) span.append(text.slice(last));
    return span;
  }
  function paraCard(x, c){
    const {d, p} = x;
    const key = d.symbol + '|' + p.id;
    const long = (p.text || '').length > 380;
    const txt = highlighted(p.text || '', c.re);
    if (long && !expanded.has(key)) txt.classList.add('clamp');
    const meta = h('div', {class: 'meta'},
      h('button', {class: 'pbtn', title: 'Open the PDF at page ' + p.page, onclick: () => openPdf(d.symbol, p.page)}, '¶ ' + p.paragraph + ' · p. ' + p.page),
      h('span', null, d.symbol + ', para. ' + p.paragraph),
      (p.cited_articles || []).map(a => h('span', {class: 'chip'}, a)));
    const card = h('div', {class: 'para'}, meta, txt);
    if (long){
      const b = h('button', {class: 'more'}, expanded.has(key) ? 'Show less' : 'Show full paragraph');
      b.addEventListener('click', () => {
        if (expanded.has(key)) expanded.delete(key); else expanded.add(key);
        const on = expanded.has(key);
        txt.classList.toggle('clamp', !on);
        b.textContent = on ? 'Show less' : 'Show full paragraph';
      });
      card.append(b);
    }
    return card;
  }

  // ---------- summary ----------
  function pickForModel(c){
    const groups = new Map();
    c.hits.forEach(i => {
      const s = flat[i].d.symbol;
      if (!groups.has(s)) groups.set(s, []);
      groups.get(s).push(i);
    });
    const lists = [...groups.values()];
    const chosen = [];
    let round = 0;
    while (chosen.length < MAXSEND){
      let added = false;
      for (const l of lists){
        if (round < l.length && chosen.length < MAXSEND){ chosen.push(l[round]); added = true; }
      }
      if (!added) break;
      round++;
    }
    return chosen.sort((a, b) => a - b);
  }
  function renderAiText(box, st){
    box.innerHTML = '';
    const text = st.text || '';
    const re = /\(([^()]*?),\s*para\.\s*(\d+)\)/g;
    let last = 0, ok = 0, total = 0, m;
    while ((m = re.exec(text)) !== null){
      if (m.index > last) box.append(text.slice(last, m.index));
      const sym = m[1].trim(), para = m[2];
      const key = sym + '|' + para;
      total++;
      const inSent = st.sentKeys.has(key);
      if (inSent) ok++;
      const doc = docs.find(d => d.symbol === sym);
      const pp = doc && (doc.paragraphs || []).find(q => String(q.paragraph) === para);
      const label = '(' + sym + ', para. ' + para + ')';
      if (pp){
        box.append(h('button', {class: 'cite' + (inSent ? '' : ' bad'),
          title: inSent ? 'Open the PDF at page ' + pp.page : 'This paragraph was NOT among those sent: check it',
          onclick: () => openPdf(sym, pp.page)}, label));
      } else {
        box.append(h('span', {class: 'cite bad', title: 'No such paragraph in the library'}, label));
      }
      last = m.index + m[0].length;
    }
    if (last < text.length) box.append(text.slice(last));
    st.check = total ? ('Citation check by code: ' + ok + ' of ' + total + ' citations point to paragraphs that were sent' + (ok < total ? ' (red ones need checking).' : '.')) : 'Citation check by code: no citation in the expected form “(SYMBOL, para. N)” was found.';
  }
  async function draft(c){
    const idx = pickForModel(c);
    if (!idx.length) return;
    const my = (tokens[c.id] = (tokens[c.id] || 0) + 1);
    const st = summaries[c.id] = {status: 'running', nsent: idx.length, total: c.hits.length, sentKeys: new Set(idx.map(i => flat[i].d.symbol + '|' + flat[i].p.paragraph))};
    if (currentId === c.id) renderMain();
    const body = idx.map(i => '[' + flat[i].d.symbol + ', para. ' + flat[i].p.paragraph + '] ' + flat[i].p.text).join('\n\n');
    const prompt =
      'You are assisting a human rights researcher. Below are ' + idx.length + ' numbered paragraphs from UN General Comments that use the concept "' + c.name + '".\n\n' +
      'Write a summary of exactly three sentences on how these paragraphs treat this concept. Rules:\n' +
      '- Use only what the paragraphs say; add no outside knowledge.\n' +
      '- Each sentence must end with the paragraph it rests on, written exactly like this: (CCPR/C/GC/37, para. 40), placed before the full stop.\n' +
      '- Cite one paragraph per sentence, using the symbol and number given in the square brackets.\n' +
      '- Return plain text only, no list, no heading.\n\nPARAGRAPHS:\n\n' + body;
    try {
      if (!(window.studio && typeof studio.ask === 'function')) throw new Error('The model is not available in this preview.');
      const out = await studio.ask(prompt);
      if (tokens[c.id] !== my) return; // cancelled
      st.text = typeof out === 'string' ? out.trim() : String(out == null ? '' : out);
      st.status = 'done';
    } catch (e){
      if (tokens[c.id] !== my) return;
      st.status = 'error'; st.error = (e && e.message) ? e.message : String(e);
    }
    if (currentId === c.id) renderMain();
  }
  function cancel(c){
    tokens[c.id] = (tokens[c.id] || 0) + 1;
    delete summaries[c.id];
    renderMain();
  }
  function summaryCard(c){
    const card = h('div', {class: 'card'}, h('h3', {style: 'margin:0 0 6px'}, 'Summary'));
    const st = summaries[c.id];
    const planned = pickForModel(c).length;
    if (!c.hits.length){
      card.append(h('p', {class: 'empty'}, 'No paragraphs to summarise.'));
      return card;
    }
    const bar = h('div', {class: 'bar'});
    const btn = h('button', {class: 'pri', onclick: () => draft(c)}, st && st.status === 'done' ? 'Draft again' : 'Draft a summary');
    if (st && st.status === 'running'){
      btn.disabled = true; btn.textContent = 'Waiting for the model…';
      bar.append(btn, h('button', {class: 'sec', onclick: () => cancel(c)}, 'Stop'));
    } else bar.append(btn);
    card.append(bar);
    card.append(h('p', {class: 'hint'},
      'Clicking sends the text of ' + planned + ' paragraph' + (planned === 1 ? '' : 's') + ' (of ' + c.hits.length + ' found) to a language model. The text leaves your browser.' +
      (c.hits.length > MAXSEND ? ' Only ' + MAXSEND + ' can be sent: they are taken in turn from each document, in paragraph order, so every document is represented.' : '')));
    if (st && st.status === 'error') card.append(h('p', {class: 'err'}, 'The model could not answer: ' + st.error));
    if (st && st.status === 'done'){
      const aiBox = h('div', {'data-source': 'ai'});
      renderAiText(aiBox, st);
      card.append(h('div', {class: 'ai'},
        h('div', null, h('span', {class: 'badge'}, 'WRITTEN BY AI'), 'Draft, not a verified text. ' + st.nsent + ' paragraph' + (st.nsent === 1 ? '' : 's') + ' sent' + (st.total > st.nsent ? ' (of ' + st.total + ' found)' : '') + '.'),
        h('p', {style: 'margin:10px 0'}, aiBox),
        h('div', {class: 'hint', style: 'margin:0'}, st.check + ' Click a citation to open the PDF.')));
    }
    return card;
  }

  // ---------- main ----------
  function renderMain(){
    const main = document.getElementById('main');
    main.innerHTML = '';
    const c = cur();
    if (!c){ main.append(h('div', {class: 'card empty'}, 'No concept selected. Add one in the sidebar.')); return; }
    if (!docs.length){ main.append(h('div', {class: 'card'}, 'The library of General Comments is empty: attach it from “Your files”.')); return; }

    const nDocs = new Set(c.hits.map(i => flat[i].d.symbol)).size;
    main.append(h('div', {class: 'card'},
      h('h2', {class: 't'}, c.name),
      h('div', null, c.hits.length + ' paragraph' + (c.hits.length === 1 ? '' : 's') + ' in ' + nDocs + ' of ' + docs.length + ' documents'),
      h('div', {class: 'note'}, 'How this is computed: code searches every numbered paragraph of the nine documents for these wordings, ignoring capitals, hyphens and a plural “s”: ',
        h('b', null, c.variants.join(' · ')), '. It finds words, not meaning: a paragraph that discusses the idea in other words is not listed. Matches are highlighted.')));

    main.append(summaryCard(c));

    const listCard = h('div', {class: 'card'}, h('h3', {style: 'margin:0 0 12px'}, 'Paragraphs that use the term, by document'));
    if (!c.hits.length){
      listCard.append(h('p', {class: 'empty'}, 'No paragraph in these nine documents uses this wording. Try another spelling or add variants separated by commas.'));
    } else {
      const groups = new Map();
      c.hits.forEach(i => {
        const s = flat[i].d.symbol;
        if (!groups.has(s)) groups.set(s, []);
        groups.get(s).push(i);
      });
      groups.forEach((list, sym) => {
        const d = flat[list[0]].d;
        const head = h('h3', null,
          d.doc_url ? h('a', {href: d.doc_url, target: '_blank', rel: 'noopener'}, sym) : sym,
          h('span', null, ' · ' + (d.short_title || d.title || '') + (d.year ? ' (' + d.year + ')' : '') + ' · ' + list.length + ' paragraph' + (list.length === 1 ? '' : 's')));
        const wrap = h('div', {class: 'doc'}, head);
        list.forEach(i => wrap.append(paraCard(flat[i], c)));
        listCard.append(wrap);
      });
    }
    main.append(listCard);

    // related concepts
    const rel = concepts.filter(o => o.id !== c.id).map(o => ({o, n: c.hits.filter(i => o.set.has(i)).length})).filter(r => r.n > 0).sort((a, b) => b.n - a.n);
    const relCard = h('div', {class: 'card'}, h('h3', {style: 'margin:0 0 6px'}, 'Related concepts'));
    relCard.append(h('div', {class: 'note'}, 'How this is computed: other concepts of this wiki whose wording also appears in the paragraphs above. The number is how many of those paragraphs they share. Add more concepts in the sidebar to widen the web.'));
    if (!rel.length) relCard.append(h('p', {class: 'empty'}, 'No other concept in the sidebar appears in the same paragraphs.'));
    else relCard.append(h('div', {class: 'rel'}, rel.map(r => h('button', {onclick: () => select(r.o.id)}, r.o.name + ' ', h('small', null, '(' + r.n + ' shared)')))));
    main.append(relCard);
  }

  renderHeader();
  renderSidebar();
  renderMain();
})();
</script>
</body>
</html>
```