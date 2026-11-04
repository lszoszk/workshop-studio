/* Workshop Studio: a chat that writes single-file apps over UN human rights data.

   What runs where (the point of the workshop, so it is also the shape of the code):
   - The model only ever receives the participant's words, the studio's instructions,
     a description of the data and a few sample records (see site/data/system_prompt.md),
     plus the reference-shelf excerpts that match a message (shelfSearch).
   - The full datasets never leave the browser: they are put into the preview next to
     the app's code (buildDoc), and the app computes everything from them.
   - The only way out of a preview is studio.ask() (site/runtime.js), which comes back
     here and is logged in the Trace drawer like every other request.
   API contract with the servers: docs/api-contract.md. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const fmt = (n) => (n == null ? '–' : Number(n).toLocaleString('en-US'));
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const words = (s) => ((s || '').match(/\S+/g) || []).length;
  const wordsOf = (tokens) => Math.round((tokens || 0) * 0.75);   // a token is about three quarters of an English word
  const UUID = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/g;
  const { datasetsUsed } = window.PreviewDoc;

  const params = new URLSearchParams(location.search);
  const hash = new URLSearchParams(location.hash.slice(1));

  const S = {
    config: null, index: null, prompts: [], schema: '', samples: null, sysmd: '', chart: '', runtime: '',
    route: null, routesDown: new Set(),
    seatCode: null, seat: null, key: hash.get('k') || null,
    country: null, countryFile: null, countryCount: 0,
    model: null, session: 'S7', ready: false,
    versions: [], current: null, freshNext: false, pendingPromptId: null, pendingText: '',
    talk: [],            // answers in words (no app): kept in the conversation, never a version
    draft: new Set(),    // files dragged into the message being written
    trace: [], linkOn: true, layersOn: false,
    busy: false, ctrl: null, dataText: {}, dataParsed: {},
    planMode: true,      // the four workshop apps plan first (the pill above the message box)
    planning: null,      // the plan being made or waiting to be built
    packs: {},           // planning packages by request id; null where there is none
  };
  const FIX = 'The app shows this error:';

  /* ---------- loading ---------- */

  async function getText(url) {
    const r = await fetch(url, { cache: 'no-cache' });
    if (!r.ok) throw new Error(`${url}: ${r.status}`);
    return r.text();
  }
  const getJSON = async (url) => JSON.parse(await getText(url));

  // a phone (the badge's QR code) gets a page that sends the link on to a laptop
  function handoff() {
    const code = (hash.get('s') || '').toUpperCase();
    const link = location.origin + location.pathname + (code ? '#s=' + code : '');
    document.body.classList.add('handoff-mode');
    $('handoff').hidden = false;
    $('handoffCode').textContent = code || 'on your badge';
    $('handoffUrl').textContent = (location.host + location.pathname).replace(/\/$/, '');
    $('handoffMail').href = 'mailto:?subject=' + encodeURIComponent('Garage Research') + '&body=' + encodeURIComponent(link);
    $('handoffCopy').onclick = async () => {
      try { await navigator.clipboard.writeText(link); $('handoffCopy').textContent = 'Copied'; } catch (e) { $('handoffCopy').textContent = link; }
    };
  }

  async function boot() {
    if (matchMedia('(max-width: 760px)').matches) return handoff();
    if (params.get('wall') === '1') document.body.classList.add('wall');
    const [config, index, prompts, schema, samples, sysmd, chart, runtime] = await Promise.all([
      getJSON('config.json'), getJSON('data/index.json'), getJSON('data/prompts.json'),
      getText('data/schema.md'), getJSON('data/samples.json'), getText('data/system_prompt.md'),
      getText('vendor/chart.umd.min.js'), getText('runtime.js'),
    ]);
    Object.assign(S, { config, index, prompts: prompts.prompts, schema, samples, sysmd, chart, runtime });
    $('event').textContent = config.event;
    $('brand').title = config.event;
    const stage = (params.get('stage') || '').toUpperCase().replace(/^S?/, 'S');
    S.session = ['S7', 'S8'].includes(stage) ? stage : (localGet('ws:session') || 'S7');
    renderSession();

    const code = (hash.get('s') || localGet('ws:seat') || '').toUpperCase();
    S.seatCode = code || null;
    if (S.seatCode) localSet('ws:seat', S.seatCode);
    if (hash.has('s') || hash.has('k')) history.replaceState(null, '', location.pathname + location.search);

    S.model = localGet('ws:model') || config.default_model;
    renderModelMenu();

    setRoute(await pickRoute());
    if (S.route.type === 'server') await ensureSeat();
    // a country the participant picked wins over the seat's, which wins over the default
    renderCountryMenu();
    setCountry(params.get('country') || localGet('ws:country') || (S.seat && S.seat.country) || config.default_country);

    restore();
    S.ready = true;
    $('sendBtn').disabled = false;
    renderFooter();
    renderAll();
    Tour.startOnce();   // the first visit in this browser
    if (!S.versions.length && !S.talk.length) {
      note(`Hello! Ask me anything, or pick a suggestion below. To build an app, first drag a file from <b>Your files</b> into the chat: ` +
        `your country is <b>${esc(S.country)}</b>, with ${fmt(S.countryCount)} UN recommendations and observations.`);
    }
  }

  /* ---------- routes ---------- */

  async function healthy(r) {
    const c = new AbortController();
    const t = setTimeout(() => c.abort(), 3000);
    try {
      const res = await fetch(r.base + '/health', { signal: c.signal });
      if (!res.ok) return false;
      const j = await res.json();
      return j.ok !== false && j.accepting !== false;
    } catch (e) {
      return false;
    } finally {
      clearTimeout(t);
    }
  }

  async function pickRoute() {
    // rehearsal on a laptop: ?api=http://127.0.0.1:8011/studio-api, honoured only on a local page for a local server
    const local = (h) => h === 'localhost' || h === '127.0.0.1';
    const api = params.get('api');
    if (api && !S.routesDown.has('local') && local(location.hostname)) {
      let url = null;
      try { url = new URL(api); } catch (e) { /* ignored below */ }
      const r = url && local(url.hostname) && { id: 'local', type: 'server', label: 'Local test server', base: api.replace(/\/$/, '') };
      if (r && (await healthy(r))) return r;
    }
    const forced = params.get('via');
    for (const r of S.config.routes) {
      if (S.routesDown.has(r.id) || (forced && r.id !== forced)) continue;
      if (r.type === 'server' && (await healthy(r))) return r;
      if (r.type === 'direct' && S.key) return r;
      if (r.type === 'replay') return r;
    }
    return S.config.routes.find((r) => r.type === 'replay');
  }

  function setRoute(r, why) {
    S.route = r;
    const b = $('routeBadge');
    b.textContent = r.type === 'replay' ? 'Recorded answers' : 'Live model';
    b.className = 'route ' + (r.type === 'replay' ? 'warn' : 'ok');
    b.title = r.label + (why ? '. ' + why : '');
    renderTools();
    if (why) note(esc(why));
  }

  async function ensureSeat() {
    for (;;) {
      let err = '';
      if (S.seatCode) {
        try {
          const res = await fetch(S.route.base + '/seat/' + encodeURIComponent(S.seatCode));
          if (res.ok) {
            S.seat = await res.json();
            setBudget(S.seat.budget_left);
            return;
          }
          err = 'That code was not recognised. Check your badge.';
        } catch (e) {
          err = 'The studio could not reach its server to check the code. Check the Wi‑Fi, then press Start again.';
        }
      }
      const answer = await askSeat(err);
      if (answer === null) {
        setRoute(S.config.routes.find((r) => r.type === 'replay'), 'No seat code: the studio replays recorded answers instead of calling a model.');
        return;
      }
      S.seatCode = answer;
      localSet('ws:seat', answer);
    }
  }

  function askSeat(err) {
    return new Promise((resolve) => {
      const d = $('seatDialog');
      $('seatErr').hidden = !err;
      $('seatErr').textContent = err;
      $('seatInput').value = '';
      d.onclose = () => resolve(d.returnValue === 'ok' && $('seatInput').value.trim() ? $('seatInput').value.trim().toUpperCase() : null);
      d.showModal();
    });
  }

  function setBudget(left) {
    if (left == null) return;
    const b = $('budget');
    b.hidden = false;
    b.textContent = `$${Number(left).toFixed(2)} left`;
    b.title = 'What this seat can still spend on requests to a model';
  }

  function setCountry(name) {
    const all = S.index.countries;
    const c = all.find((x) => x.name === name) || all.find((x) => x.name === S.config.default_country) || all[0];
    S.country = c.name;
    S.countryFile = c.file;
    S.countryCount = c.count;
    $('countrySelect').value = c.name;
    $('countryCount').textContent = `${fmt(c.count)} records`;
  }

  // every country in the index, by UN regional group
  function renderCountryMenu() {
    const groups = {};
    S.index.countries.forEach((c) => { (groups[c.region || 'Other'] = groups[c.region || 'Other'] || []).push(c); });
    $('countrySelect').innerHTML = Object.keys(groups).sort().map((g) => `<optgroup label="${esc(g)}">` +
      groups[g].map((c) => `<option value="${esc(c.name)}">${esc(c.name)}</option>`).join('') + '</optgroup>').join('');
  }

  // the same app on another country's records: nothing goes to a model, the code just runs again
  async function changeCountry(name) {
    if (S.busy) { $('countrySelect').value = S.country; return; }
    setCountry(name);
    localSet('ws:country', S.country);
    const p = S.prompts.find((q) => q.id === S.pendingPromptId);
    if (p && $('input').value.trim() === S.pendingText.trim()) useSuggestion(p, S.freshNext);   // its text names the country
    if (S.planning && !$('planView').hidden) showPlan(S.planning);
    renderSuggest();
    renderShelf();
    const v = currentVersion();
    if (!v) return;
    await showVersion(v);
    note(`Your app now runs on the ${fmt(S.countryCount)} records addressed to <b>${esc(S.country)}</b>: the same code, different data. Nothing was sent to a model.`);
  }

  /* ---------- talking to a model ---------- */

  function buildSystem() {
    const sp = S.sysmd.split('\n---\n')[1].trim();
    return [sp, S.schema.trim(),
      '## Sample records per dataset: five of the recommendations, a few of the others (the real data is much larger)\n\n```json\n' + JSON.stringify(S.samples, null, 1) + '\n```'].join('\n\n');
  }

  async function chat(o) {
    for (;;) {
      const r = S.route;
      try {
        if (r.type === 'server') return await serverChat(r, o);
        if (r.type === 'direct') return await directChat(o);
        return await replayChat(o);
      } catch (e) {
        if (e.name === 'AbortError' || !e.failover || e.started) throw e;
        S.routesDown.add(r.id);
        const next = await pickRoute();
        if (!next || next.id === r.id) throw e;
        setRoute(next, `${r.label} did not answer (${e.message}). Switched to: ${next.label}.`);
      }
    }
  }

  async function serverChat(r, o) {
    let res;
    try {
      res = await fetch(r.base + '/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seat: S.seatCode, model: o.model, purpose: o.purpose, messages: o.messages }),
        signal: o.signal,
      });
    } catch (e) {
      if (e.name === 'AbortError') throw e;
      throw Object.assign(new Error('no connection'), { failover: true });
    }
    if (!res.ok) {
      let j = {};
      try { j = await res.json(); } catch (e) { /* not JSON */ }
      throw Object.assign(new Error(j.error || `server error ${res.status}`), { status: res.status, failover: res.status >= 500 && res.status !== 503 });
    }
    return readSSE(res, o, (ev, j) => (ev === 'usage' ? { usage: j } : ev === 'error' ? { error: j.error || 'The model stopped' } : { delta: j.delta, reasoning: j.reasoning }));
  }

  async function directChat(o) {
    const m = S.config.models[o.model];
    const sys = o.purpose === 'build' ? buildSystem() : S.config.direct_system[o.purpose];
    const t0 = performance.now();
    let res;
    try {
      res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: { Authorization: 'Bearer ' + S.key, 'Content-Type': 'application/json', 'X-Title': 'Garage Research' },
        body: JSON.stringify({
          model: m.openrouter,
          messages: (sys ? [{ role: 'system', content: sys }] : []).concat(o.messages),
          stream: true,
          temperature: { build: 0.3, inapp: 0.2, question: 0.8 }[o.purpose],
          max_tokens: { build: 64000, inapp: 8000, question: 4000 }[o.purpose],
          provider: { only: [m.provider], allow_fallbacks: false, zdr: true },
          usage: { include: true },
          ...(m.reasoning && o.purpose === 'build' ? { reasoning: { effort: m.reasoning } } : {}),
          ...(m.reasoning && o.purpose === 'question' ? { reasoning: { effort: 'low' } } : {}),   // a quick question: think briefly
        }),
        signal: o.signal,
      });
    } catch (e) {
      if (e.name === 'AbortError') throw e;
      throw Object.assign(new Error('OpenRouter did not answer'), { failover: true });
    }
    if (!res.ok) {
      let j = {};
      try { j = await res.json(); } catch (e) { /* not JSON */ }
      throw Object.assign(new Error((j.error && j.error.message) || `OpenRouter error ${res.status}`), { failover: res.status >= 500 });
    }
    const out = await readSSE(res, o, (ev, j) => {
      if (j.error) return { error: j.error.message || 'The model stopped' };
      const d = j.choices && j.choices[0] && j.choices[0].delta;
      return { delta: d && d.content, reasoning: d && d.reasoning, usage: j.usage || null };
    });
    const u = out.usage || {};
    out.usage = { model: o.model, model_label: m.label, host: m.host, zdr: true, prompt_tokens: u.prompt_tokens, completion_tokens: u.completion_tokens, cost: u.cost, seconds: (performance.now() - t0) / 1000 };
    return out;
  }

  async function readSSE(res, o, map) {
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = '', text = '', thought = '', usage = null, started = false;
    try {
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        let i;
        while ((i = buf.indexOf('\n\n')) >= 0) {
          const raw = buf.slice(0, i);
          buf = buf.slice(i + 2);
          let ev = 'message', data = '';
          raw.split('\n').forEach((line) => {
            if (line.startsWith('event:')) ev = line.slice(6).trim();
            else if (line.startsWith('data:')) data += line.slice(5).trim();
          });
          if (!data || data === '[DONE]') continue;
          let j;
          try { j = JSON.parse(data); } catch (e) { continue; }
          const m = map(ev, j);
          if (m.error) throw Object.assign(new Error(m.error), { started, failover: !started });
          if (m.usage) usage = m.usage;
          if (m.reasoning) {
            started = true;  // the model is answering: too late to fail over without losing it
            thought += m.reasoning;
            if (o.onThought) o.onThought(thought);
          }
          if (m.delta) {
            started = true;
            text += m.delta;
            if (o.onDelta) o.onDelta(text);
          }
        }
      }
    } catch (e) {
      if (e.name === 'AbortError') throw e;
      if (e.failover === undefined) Object.assign(e, { started, failover: !started, message: started ? 'the connection dropped mid-answer' : e.message });
      throw e;
    }
    return { text, thought, usage: usage || {} };
  }

  async function replayChat(o) {
    if (o.purpose !== 'build') {
      throw Object.assign(new Error('No model is connected (recorded mode), so this needs a live model.'), { failover: false });
    }
    const id = o.promptId || nextPromptId();
    // recorded for Kenya; the apps read the country from the data, the words around them do not
    const local = (s) => (S.country === 'Kenya' ? s : s.replace(/Kenya/g, S.country));
    // the workshop apps are recorded from the current plans; the extras only in the fallback recording
    let rec = S.config.replay, text;
    try {
      text = local(await getText(rec.dir + id + '.md'));
    } catch (e) {
      rec = rec.fallback;
      text = rec && local(await getText(rec.dir + id + '.md').catch(() => ''));
      if (!text) throw Object.assign(new Error('Recorded mode can only play back the workshop requests. Pick one of the suggestions.'), { failover: false });
    }
    const thought = local(await getText(rec.dir + id + '.thought.md').catch(() => ''));
    const t0 = performance.now();
    // the recorded thinking first, sped up to at most about ten seconds, then the answer
    const step = Math.max(220, Math.ceil(thought.length / 250));
    for (let i = 0; i < thought.length; i += step) {
      if (o.signal && o.signal.aborted) throw new DOMException('stopped', 'AbortError');
      await new Promise((r) => setTimeout(r, 40));
      if (o.onThought) o.onThought(thought.slice(0, i + step));
    }
    for (let i = 0; i < text.length; i += 220) {
      if (o.signal && o.signal.aborted) throw new DOMException('stopped', 'AbortError');
      await new Promise((r) => setTimeout(r, 40));
      o.onDelta(text.slice(0, i + 220));
    }
    const m = S.config.models[rec.model];
    return { text, usage: { model: rec.model, model_label: m.label + ' (recorded)', host: m.host, zdr: true, recorded: true, cost: 0, seconds: (performance.now() - t0) / 1000 } };
  }

  function nextPromptId() {
    const used = new Set(chainOf(currentVersion()).map((v) => v.promptId));
    const ds = currentVersion() ? datasetsUsed(currentVersion().html) : ['uhri'];   // the wiki app also reads the library
    const p = S.prompts.find((q) => ds.includes(q.dataset) && !used.has(q.id) && (!q.builds_on || used.has(q.builds_on)));
    return p ? p.id : null;
  }

  /* ---------- building ---------- */

  function extractHtml(text, partial) {
    const i = text.indexOf('```html');
    if (i >= 0) {
      const rest = text.slice(i + 7).replace(/^\s*\n/, '');
      // the closing fence follows </html>: the app's own code may contain ``` (e.g. stripping fences from a model's answer)
      const close = /<\/html>\s*```/i.exec(rest);
      if (close) return rest.slice(0, close.index + 7).trim();
      if (partial) return rest;
      const j = rest.indexOf('```');
      return j >= 0 ? rest.slice(0, j).trim() : '';
    }
    const m = text.match(/<!doctype html[\s\S]*<\/html>/i);
    if (m) return m[0];
    const k = partial ? text.search(/<!doctype html/i) : -1;  // unfenced reply still streaming
    return k >= 0 ? text.slice(k) : '';
  }

  function summaryOf(text) {
    const fence = /<\/html>\s*```/i.test(text) ? /```html[\s\S]*?<\/html>\s*```/i : /```html[\s\S]*?(```|$)/;
    const s = text.replace(fence, '').replace(/<!doctype html[\s\S]*?(<\/html>|$)/i, '').trim();
    return s.length > 700 ? s.slice(0, 700) + '…' : s;
  }

  const currentVersion = () => (S.current ? S.versions[S.current - 1] : null);

  function chainOf(v) {
    const out = [];
    for (let x = v; x; x = x.parent ? S.versions[x.parent - 1] : null) out.unshift(x);
    return out;
  }

  // the conversation the model sees: answers in words and apps, in order; old apps by their summary only
  function buildMessages(parent, content) {
    const chain = chainOf(parent);
    const msgs = [];
    const talk = (after) => S.talk.filter((t) => t.after === after).slice(-6).forEach((t) => {
      msgs.push({ role: 'user', content: t.sent || t.user });
      msgs.push({ role: 'assistant', content: t.reply });
    });
    talk(null);
    chain.forEach((v, i) => {
      msgs.push({ role: 'user', content: v.sent || v.user });
      msgs.push({ role: 'assistant', content: i === chain.length - 1 ? v.reply : v.summary + '\n\n[The code of this earlier version is omitted; the latest version follows.]' });
      talk(v.n);
    });
    msgs.push({ role: 'user', content });
    return msgs;
  }

  /* ---------- files: dragged from the shelf into the chat ---------- */

  const fileMeta = (key) => S.config.files.find((f) => f.key === key);
  const fileLabel = (key) => fileMeta(key).label.replace(/\{country\}/g, S.country);
  // what the model gets for a file: its name and where the app finds it, never its contents
  const attachLine = (key) => `(Attached: ${fileLabel(key)} → WORKSHOP_DATA.${key}` +
    (fileMeta(key).also || []).map((k) => `, with WORKSHOP_DATA.${k}`).join('') + ')';
  const attachedBefore = () => new Set([...S.versions, ...S.talk, ...(S.planning ? [S.planning] : [])].flatMap((t) => t.files || []));

  function addFile(key) {
    S.draft.add(key);
    renderAttach();
    renderNeeds();
    renderShelfState();
    $('input').focus();
  }

  function chipHtml(key, removable) {
    const f = fileMeta(key);
    return `<span class="filechip"><i class="ficon ${f.kind}">${f.kind.toUpperCase()}</i><span>${esc(fileLabel(key))}</span>` +
      (removable ? `<button type="button" data-key="${key}" aria-label="Remove ${esc(fileLabel(key))}">×</button>` : '') + '</span>';
  }

  function renderAttach() {
    const box = $('attach');
    box.hidden = !S.draft.size;
    box.innerHTML = [...S.draft].map((k) => chipHtml(k, true)).join('');
    box.querySelectorAll('button').forEach((b) => { b.onclick = () => { S.draft.delete(b.dataset.key); renderAttach(); renderNeeds(); renderShelfState(); }; });
  }

  // a workshop request names the file it needs; until that file is in the chat, the box says so
  function renderNeeds() {
    const p = S.prompts.find((q) => q.id === S.pendingPromptId);
    // a file that comes with the needed one (the library with the wiki) stands for it: swap it in
    const part = p && p.dataset && !S.draft.has(p.dataset) && [...S.draft].find((k) => (fileMeta(p.dataset).also || []).includes(k));
    if (part) {
      S.draft.delete(part);
      S.draft.add(p.dataset);
      renderAttach();
      note(`This request needs <b>${esc(fileLabel(p.dataset))}</b>, which brings <b>${esc(fileLabel(part))}</b> with it, so the studio attached that instead.`);
    }
    const have = new Set([...attachedBefore(), ...S.draft]);
    const missing = p && p.dataset && !have.has(p.dataset) ? p.dataset : null;
    $('needs').hidden = !missing;
    if (missing) $('needs').innerHTML = `This request needs the file <b>${esc(fileLabel(missing))}</b>. Drag it here from <b>Your files</b>.`;
    renderShelfState(missing);
  }

  // every message goes through here, so a request is never lost or silently changed;
  // `plan` is set when the message is a plan on its way to being built
  function submitBuild(text, plan) {
    if (!S.ready || S.busy || !text.trim()) return;
    if (!S.linkOn) {
      note('The model link is cut, so the model cannot answer. Open <b>Look inside</b> and restore the link.');
      return;
    }
    if (!plan && S.planning && S.planning.changing) return revisePlan(S.planning, text);
    const p = S.prompts.find((q) => q.id === S.pendingPromptId);
    if (p && p.dataset && !new Set([...attachedBefore(), ...S.draft]).has(p.dataset)) {
      note(`This request needs the file <b>${esc(fileLabel(p.dataset))}</b>. Drag it from <b>Your files</b> into the chat, then send.`);
      showFiles(p.dataset);
      return;
    }
    if (!plan && plannable(p) && S.planMode) {
      if (text.trim() !== S.pendingText.trim()) {
        note('Plan mode replays a planning session prepared for this request as it is written. Undo your change, or turn <b>Plan mode</b> off to send your own words to the model.');
        return;
      }
      startPlanning(p, text, takeDraft());
      return true;
    }
    if (S.route.type === 'replay' && (!p || text.trim() !== S.pendingText.trim())) {
      note('Without a seat code the studio plays back recorded answers, so it can only answer the workshop requests as they are written. ' +
        'Pick a suggestion, or ask a facilitator for a seat code to chat freely.');
      return;
    }
    if (plan) {
      const files = [...new Set([...plan.files, ...S.draft])];
      S.draft.clear();
      renderAttach();
      if ($('input').value === CHANGE) { $('input').value = ''; fitInput(); }
      build(text, files);
      return true;
    }
    build(text, takeDraft());
    return true;
  }

  // the files and words in the box go into a message: the box is emptied
  function takeDraft() {
    const files = [...S.draft];
    S.draft.clear();
    $('input').value = '';
    fitInput();
    renderAttach();
    $('needs').hidden = true;
    return files;
  }

  function friendly(e) {
    const m = e.message || '';
    if (e.name === 'AbortError') return 'Stopped. Your message is back in the box.';
    if (e.status === 429 && /budget|spending/i.test(m)) return `${m}. Ask a facilitator for a top-up; your apps stay here.`;
    if (e.status === 429) return 'Too many messages from this seat in a short time. Wait a minute, then send again.';
    if (e.status === 403) return 'This seat code is not active. Ask a facilitator.';
    if (/too long/i.test(m)) return 'This conversation has become too long for the model. Start a new app with a clearer request.';
    if (e.status === 503) return (m || 'The model service is busy') + '. Your message is back in the box.';
    return `The model could not finish (${m}). Your message is back in the box: send it again.`;
  }

  async function build(userText, files = []) {
    if (S.busy || !userText.trim()) return;
    const parent = S.freshNext ? null : currentVersion();
    const promptId = S.pendingPromptId;
    const plan = S.planning && S.planning.building ? S.planning : null;
    S.freshNext = false;
    S.pendingPromptId = null;
    setBusy(true);
    $('planView').hidden = true;
    await shelfLoad();
    const hits = shelfSearch(userText);
    const asTyped = userText + files.map((k) => '\n\n' + attachLine(k)).join('');
    const sent = asTyped + shelfBlock(hits);
    const messages = buildMessages(parent, sent);
    const giveBack = () => {  // after a failure the message and its files go back in the box
      if (plan) { plan.building = false; showPlan(plan); return; }   // a plan stays on the stage, ready to build again
      const fresh = !parent && S.versions.length > 0;
      openComposer(userText);
      Object.assign(S, { pendingPromptId: promptId, pendingText: promptId ? userText : '', freshNext: fresh });
      files.forEach((k) => S.draft.add(k));
      renderAttach();
      renderContinuing();
    };
    setView('app');
    addUser(userText, files);
    const view = addAssistantLive();
    if (hits.length) view.step(shelfStep(hits));
    const t0 = performance.now();
    let lastSkeleton = 0, sketched = false;
    S.ctrl = new AbortController();
    try {
      const { text, usage } = await chat({
        purpose: 'build', model: S.model, messages, promptId, signal: S.ctrl.signal,
        onThought: (all) => view.think(all),
        onDelta: (all) => {
          view.update(all);
          const now = performance.now();
          if (now - lastSkeleton > 1200) {
            lastSkeleton = now;
            const part = extractHtml(all, true);
            if (part.length > 300) { Preview.show(PreviewDoc.skeleton(part)); sketched = true; }
          }
        },
      });
      const html = extractHtml(text);
      if (usage.model_label) view.who(usage.model_label);
      const seconds = usage.seconds || (performance.now() - t0) / 1000;
      addTrace({ purpose: 'build', usage, messages, userText: asTyped, parent, files, shelf: hits });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      const base = { user: userText, sent, files, model: usage.model || S.model, label: usage.model_label || S.config.models[S.model].label,
        seconds, cost: usage.cost, recorded: !!usage.recorded, promptId, created: Date.now(), ...view.thinking(),
        ...(hits.length ? { shelf: hits.map((h) => h.page.id) } : {}) };
      if (!html) {
        if (!text.trim()) {
          view.fail('', 'The model sent back nothing. Your message is back in the box: send it again.');
          giveBack();
          return;
        }
        // a workshop app that came back as one sentence: the model stopped before the code (Mistral, now and then)
        if (promptId && text.trim().length < 600) {
          view.fail('', 'The model stopped before writing the code; it happens now and then. Your request is back in the box: send it again.');
          giveBack();
          return;
        }
        // an answer in words: part of the conversation, not a new version of the app
        const t = Object.assign(base, { reply: text.trim(), after: S.current });
        S.talk.push(t);
        view.answer(t);
        save();
        if (plan) plan.building = false;
        if (sketched && S.current) await showVersion(currentVersion());   // a half-written app gives way to the real one
        return;
      }
      const v = Object.assign(base, {
        n: S.versions.length + 1, parent: parent ? parent.n : null, reply: text,
        summary: summaryOf(text), html, fix: userText.startsWith(FIX),
      });
      S.versions.push(v);
      S.current = v.n;
      if (plan) retirePlanning(`Built as v${v.n}.`);
      view.done(v);
      const p = S.prompts.find((q) => q.id === promptId);
      if (p && p.lesson) view.lesson(p.lesson);
      save();
      renderVersions();
      await showVersion(v);
    } catch (e) {
      view.fail('', friendly(e));
      giveBack();
    } finally {
      setBusy(false);
    }
  }

  function setBusy(on) {
    S.busy = on;
    $('sendBtn').disabled = on;
    $('stopBtn').hidden = !on;
    $('building').hidden = !on;
    $('empty').hidden = on || S.versions.length > 0;   // the shelf, until there is an app
    renderSuggest();   // nothing to choose while the model works
    renderTools();
  }

  /* ---------- preview ---------- */

  function fileFor(k) {
    return k === 'uhri' ? S.countryFile : S.index.datasets[k].file;
  }

  async function dataText(k) {
    const f = fileFor(k);
    if (!S.dataText[f]) S.dataText[f] = PreviewDoc.escapeScript(await getText('data/' + f));
    return S.dataText[f];
  }

  async function dataParsed(k) {
    const f = fileFor(k);
    if (!S.dataParsed[f]) S.dataParsed[f] = JSON.parse(await getText('data/' + f));
    return S.dataParsed[f];
  }

  const fullDoc = (v) => PreviewDoc.build(v.html, { chart: S.chart, runtime: S.runtime, dataText, files: chainOf(v).flatMap((x) => x.files || []) });

  const Preview = {
    frames: [],
    front: 0,
    init() {
      for (let i = 0; i < 2; i++) {
        const f = document.createElement('iframe');
        f.setAttribute('sandbox', 'allow-scripts allow-downloads allow-modals allow-popups allow-popups-to-escape-sandbox');
        f.setAttribute('allow', 'clipboard-write');
        f.title = 'Your app';
        f.className = 'back';
        $('viewport').prepend(f);
        this.frames.push(f);
      }
    },
    show(doc) {
      return new Promise((resolve) => {
        const back = this.frames[1 - this.front];
        back.onload = () => {
          // a skeleton set just before this doc fires its own load first; the second load must not swap again
          if (this.frames[this.front] === back) return resolve();
          back.classList.remove('back');
          this.frames[this.front].classList.add('back');
          this.front = 1 - this.front;
          resolve();
        };
        back.srcdoc = PreviewDoc.forFrame(doc);
      });
    },
    win() { return this.frames[this.front].contentWindow; },
  };

  async function showVersion(v) {
    tabs.forEach((w) => (w.closed ? tabs.delete(w) : sendToTab(w)));   // an open tab follows the version on stage
    $('empty').hidden = true;
    $('appError').hidden = true;
    renderContinuing();
    if (viewing === 'code') renderCode();
    await Preview.show(await fullDoc(v));
  }

  /* ---------- messages from the preview ---------- */

  // app tabs opened with "New tab": the same sandboxed app, whose model requests still come through here
  const tabs = new Set();
  window.addEventListener('message', (e) => {
    const m = e.data || {};
    if (typeof m.type !== 'string' || !m.type.startsWith('studio:')) return;
    if (m.type === 'studio:ready' && Run3.waiting && e.source === Run3.frame.contentWindow) return Run3.got({ fp: m.fingerprint, shown: m.shown || { picks: [] } });
    const fromTab = tabs.has(e.source);
    if (fromTab && m.type === 'studio:tab-ready') return sendToTab(e.source);
    if (e.source !== Preview.win() && !fromTab) return;
    if (m.type === 'studio:ask') handleAsk(e.source, m);
    else if (fromTab) return;   // a tab shows its own errors and PDFs
    else if (m.type === 'studio:open-source') openSource(m.symbol, m.page, m.quote);
    else if (m.type === 'studio:error') showAppError(m);
    else if (m.type === 'studio:ready' && S.layersOn) sendLayers();
  });

  function openTab() {
    const w = window.open('app.html', '_blank');   // not noopener: the tab talks back to the studio
    if (w) tabs.add(w);
  }

  async function sendToTab(w) {
    const v = currentVersion();
    if (!v || w.closed) return;
    w.postMessage({ type: 'studio:app-doc', doc: PreviewDoc.forFrame(await fullDoc(v)), title: `v${v.n} · ${titleOf(v.html)}` }, '*');
  }

  // the PDF of a document at a page, in the drawer; files/ holds them under their id ("/" becomes "_")
  const pdfOf = (id) => 'files/' + String(id).replace(/\//g, '_') + '.pdf';
  async function openSource(id, page, quote) {
    page = Math.max(1, Number(page) || 1);
    const file = pdfOf(id);
    const lib = await dataParsed('library').catch(() => null);
    const doc = lib && lib.records.find((d) => d.id === id || d.symbol === id);
    const printed = doc && (doc.passages.find((x) => x.page === page) || {}).page_label;
    openDrawer(doc ? `${doc.short_title}, ${printed && printed !== String(page) ? `p. ${printed} (PDF page ${page})` : `page ${page}`}` : `${id}, page ${page}`);
    $('drawer').classList.add('wide');
    const where = doc ? `<a href="${esc(doc.url)}" target="_blank" rel="noopener">${doc.symbol ? 'UN page' : 'Where it was published'}</a>`
      : `<a href="https://docs.un.org/en/${esc(id)}" target="_blank" rel="noopener">UN page</a>`;
    const head = `<p class="src-head">${doc ? esc(doc.kind) + ' · ' + esc(doc.author) + ', ' + doc.year : 'The document as published'}. ` +
      `<a href="${file}#page=${page}" target="_blank" rel="noopener">Open in a new tab</a> · ${where}</p>`;
    await PdfView.open($('drawerBody'), file, page, quote, head, '');
  }

  let asking = 0;
  async function handleAsk(win, m) {
    const reply = (x) => win.postMessage(Object.assign({ type: 'studio:answer', id: m.id }, x), '*');
    if (!S.linkOn) return reply({ error: 'The studio has cut the link to the model. The rest of your app keeps working; only this AI step needs a model.' });
    while (asking >= 2) await new Promise((r) => setTimeout(r, 150));
    asking++;
    const content = m.prompt + (m.json ? '\n\nReply with JSON only.' : '');
    try {
      const { text, usage } = await chat({ purpose: 'inapp', model: S.model, messages: [{ role: 'user', content }] });
      addTrace({ purpose: 'inapp', usage, messages: [{ role: 'user', content }], userText: content });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      reply({ text });
    } catch (e) {
      reply({ error: e.message });
    } finally {
      asking--;
    }
  }

  function showAppError(m) {
    const box = $('appError');
    const chain = chainOf(currentVersion());
    let fixes = 0;
    for (let i = chain.length - 1; i >= 0 && chain[i].fix; i--) fixes++;
    const detail = `<details><summary>Technical detail</summary>${esc(m.message)}${m.line ? ' (line ' + m.line + ')' : ''}</details>`;
    box.hidden = false;
    if (fixes >= 2) {
      // after two fixes that did not hold, a clearer fresh start usually beats a third patch
      box.innerHTML = `<span>This app still breaks after two fixes. A fresh start with a clearer request usually works better.</span>${detail}<button type="button">Start again</button>`;
      box.querySelector('button').onclick = () => {
        box.hidden = true;
        const first = chain.find((v) => !v.fix) || chain[0];
        S.freshNext = true;
        openComposer(first.user);
        S.pendingPromptId = first.promptId;
        S.pendingText = first.user;
        renderContinuing();
        note('The first request for this app is back in the box. Add what went wrong last time (which part broke), then press <b>Build</b>.');
      };
      return;
    }
    box.innerHTML = `<span>Something in the app broke.</span>${detail}<button type="button">Ask the model to fix it</button>`;
    box.querySelector('button').onclick = () => {
      box.hidden = true;
      openComposer(`${FIX} "${m.message}"${m.line ? ' at line ' + m.line : ''}. Please fix it and keep everything else the same.`);
    };
  }

  /* ---------- Layers, Run x3, Ask x3, model link ---------- */

  function sendLayers() {
    const v = currentVersion();
    if (!v) return;
    Preview.win().postMessage({ type: 'studio:layers', on: S.layersOn, source: S.layersOn ? v.html : '' }, '*');
  }

  function toggleLayers() {
    S.layersOn = !S.layersOn;
    $('layersBtn').setAttribute('aria-pressed', S.layersOn);
    closeMenu();
    $('legend').hidden = !S.layersOn;
    sendLayers();
  }

  const Run3 = {
    frame: null, waiting: null,
    got(fp) { const w = this.waiting; this.waiting = null; w(fp); },
    async once(doc) {
      if (!this.frame) {
        this.frame = document.createElement('iframe');
        this.frame.setAttribute('sandbox', 'allow-scripts');
        Object.assign(this.frame.style, { position: 'fixed', left: '-12000px', top: '0', width: '1280px', height: '900px', border: '0' });
        document.body.appendChild(this.frame);
      }
      const fp = new Promise((resolve) => {
        this.waiting = resolve;
        setTimeout(() => { if (this.waiting === resolve) { this.waiting = null; resolve({ fp: 'no answer', shown: { picks: [] } }); } }, 15000);
      });
      this.frame.srcdoc = PreviewDoc.forFrame(doc);
      return fp;
    },
  };

  async function run3() {
    const v = currentVersion();
    if (!v) return;
    openDrawer('Same data, same answer?');
    const body = $('drawerBody');
    body.innerHTML = '<p>The studio opened your app three times from scratch, on the same data, and read what it shows each time. Here are its first numbers, side by side.</p><div id="runTable"><p class="faint">Running…</p></div><div id="runVerdict"></div>';
    const doc = await fullDoc(v);
    const runs = [];
    for (let i = 0; i < 3; i++) runs.push(await Run3.once(doc));
    const ok = runs[0].fp !== 'no answer';
    const same = ok && runs.every((r) => r.fp === runs[0].fp);
    const rows = runs[0].shown.picks.map((t, k) => {
      const cells = runs.map((r) => r.shown.picks[k] || '–');
      const agree = cells.every((c) => c === cells[0]);
      return `<tr${agree ? '' : ' class="differs"'}>${cells.map((c) => `<td>${esc(c)}</td>`).join('')}<td class="mark">${agree ? '✓' : '≠'}</td></tr>`;
    }).join('');
    const sh = runs[0].shown;
    $('runTable').innerHTML = rows ? `<table class="runs3"><thead><tr><th>Run 1</th><th>Run 2</th><th>Run 3</th><th></th></tr></thead><tbody>${rows}</tbody></table>` +
      `<p>${same ? 'Not only these: all' : 'All'} ${fmt(sh.numbers)} numbers on the screen${sh.charts ? ` and the values behind ${sh.charts} chart${sh.charts === 1 ? '' : 's'}` : ''} ${same ? 'are identical in all three runs.' : 'were compared, and something differs.'}</p>`
      : '<p>The app shows no numbers on its first screen; everything it shows was compared instead.</p>';
    $('runVerdict').innerHTML = (same
      ? '<div class="verdict same"><b>The same answer, three times.</b> The model wrote this code once and takes no part when it runs: the code counts and draws from the data in the same way every time. Run it a hundred times and you get the same numbers, which is what makes them checkable. Compare <b>Ask the model directly</b>: the same question three times, and the answers vary.</div>'
      : ok ? '<div class="verdict diff"><b>Not the same every time.</b> Something in the app changes from run to run, usually on purpose (a random sample, the current time). Ask the model which part it is: code can use chance on purpose, but it should say so.</div>'
        : '<div class="verdict diff"><b>The app did not finish starting.</b> Try again, or ask the model to fix the app.</div>') +
      `<details class="faint small"><summary>For the technically minded</summary>A checksum of everything on the screen, per run: ${runs.map((r) => esc(r.fp)).join(' · ')}.</details>`;
  }

  async function truth(kind) {
    if (kind === 'uhri_count') {
      const d = await dataParsed('uhri');
      const upr = d.records.filter((r) => r.mechanism === 'Universal Periodic Review').length;
      return `${fmt(d.count)} records in total, of which ${fmt(upr)} come from the Universal Periodic Review (UHRI snapshot of ${d.built}).`;
    }
    if (kind === 'gc36_count') {   // a document the models think they know: on 4 Nov GLM said 79, 70, 79 and Mistral 70, 74, 70
      const d = await dataParsed('gc');
      const n = d.records.filter((r) => r.symbol === 'CCPR/C/GC/36').length;
      return `${fmt(n)} numbered paragraphs in CCPR/C/GC/36, counted in the UN Human Rights Database (${d.built}).`;
    }
    if (kind === 'gc_climate') {
      const d = await dataParsed('gc');
      const n = d.records.filter((r) => /climate/i.test(r.text)).length;
      return `${fmt(n)} of ${fmt(d.count)} paragraphs contain "climate" (UN Human Rights Database, ${d.built}).`;
    }
    if (kind === 'gc_paragraph') {
      const d = await dataParsed('gc');
      const t = S.config.trap;
      const doc = d.records.filter((r) => r.symbol === t.symbol);
      const hit = doc.find((r) => String(r.paragraph) === String(t.paragraph));
      return hit ? `${t.symbol}, para. ${t.paragraph}: “${hit.text}”`
        : `There is no paragraph ${t.paragraph}: ${t.symbol} has ${fmt(doc.length)} numbered paragraphs (UN Human Rights Database, ${d.built}). The script looked it up; it cannot make one up.`;
    }
    if (kind === 'pdf_count') {
      const r = (await dataParsed('pdf_text')).reference;
      return `${fmt(r.paragraphs)} numbered paragraphs and ${fmt(r.footnotes)} footnotes, adopted ${r.adopted} (UN Human Rights Database, checked against the document).`;
    }
    const d = await dataParsed('hrc');
    const n = d.records.filter((r) => r.kind === 'resolution').length;
    return `${fmt(n)} resolutions adopted by recorded vote since 2021, plus ${fmt(d.count - n)} recorded votes on amendments (OHCHR voting records, ${d.built}).`;
  }

  let askRun = 0;
  async function ask3(kind) {
    const run = ++askRun;
    const v = currentVersion();
    const ds = (v && datasetsUsed(v.html)[0]) || 'uhri';
    const trap = kind === 'trap';
    const q = trap ? S.config.trap : S.config.questions[ds];
    const question = q.ask.replace('{country}', S.country);
    const model = S.config.models[S.model];
    openDrawer('Ask the model directly, three times');
    const body = $('drawerBody');
    body.innerHTML = `<div class="seg" role="tablist" aria-label="Question">
        <button type="button" role="tab" data-kind="count" aria-selected="${!trap}">A number</button>
        <button type="button" role="tab" data-kind="trap" aria-selected="${trap}">A quotation</button></div>
      <p>The same question goes to ${esc(model.label)} three times, <b>without any data</b>: the model answers from what it absorbed in training.</p>
      <p class="question">“${esc(question)}”</p>
      <div class="answers">${[1, 2, 3].map((i) => `<div class="answer" id="ans${i}"><div class="who">Answer ${i}</div><span>…</span></div>`).join('')}</div>
      <div class="truth"><div class="who">Computed by a script from the data in this browser</div><span id="truth">…</span></div>
      <p id="askNote"></p>`;
    body.querySelectorAll('.seg button').forEach((b) => { b.onclick = () => { if (b.dataset.kind !== kind) ask3(b.dataset.kind); }; });
    truth(q.truth).then((t) => { if (run === askRun) $('truth').textContent = t; });
    if (!S.linkOn) { $('askNote').textContent = 'The model link is cut, so only the script can answer.'; return; }
    let ok = 0;
    await Promise.all([1, 2, 3].map(async (i) => {
      const span = $('ans' + i).querySelector('span');
      const messages = [{ role: 'user', content: question }];
      try {
        const { text, usage } = await chat({ purpose: 'question', model: S.model, messages, onDelta: (all) => { span.textContent = all; } });
        span.textContent = text;
        addTrace({ purpose: 'question', usage, messages, userText: question });
        ok++;
      } catch (e) {
        span.textContent = friendly(e);
      }
    }));
    if (run !== askRun || !ok) return;   // another question was picked meanwhile
    $('askNote').innerHTML = trap ? esc(q.note)
      : ok >= 2 ? 'Several answers, often several different numbers, all sounding sure. The script gives one answer, and you can check how it got it. <b>Use the model to write the code; let the code answer.</b>' : '';
  }

  function toggleLink() {
    S.linkOn = !S.linkOn;
    $('linkBtn').setAttribute('aria-pressed', S.linkOn);
    $('linkBtn').querySelector('b').textContent = S.linkOn ? 'Cut the model link' : 'Restore the model link';
    $('offlineBanner').hidden = S.linkOn;
    closeMenu();
    renderTools();
  }

  /* ---------- trace: what left this laptop ---------- */

  function addTrace({ purpose, usage, messages, userText, parent, files = [], shelf = [], plan = null }) {
    const sys = purpose === 'build' ? buildSystem() : (S.config.direct_system[purpose] || '');
    const ids = (userText.match(UUID) || []).length;
    const sent = [], kept = [];
    if (purpose === 'build') {
      sent.push(`Your message (${fmt(userText.length)} characters)`);
      if (plan) sent.push(`The plan you asked to change (v${plan.version}, about ${fmt(words(planText(plan.plan)))} words)`);
      if (shelf.length) sent.push(`${shelf.length === 1 ? 'An excerpt' : fmt(shelf.length) + ' excerpts'} from the workshop reference shelf, found by a search on your message: ${shelf.map((h) => h.page.title).join('; ')}`);
      if (files.length) sent.push(`The name of each file you added (${files.map(fileLabel).join('; ')}): not its contents`);
      sent.push(`The studio's instructions, a description of the data and a few sample records per dataset (about ${fmt(words(sys))} words, added ${S.route.type === 'server' ? 'by the server' : 'by the studio'})`);
      if (parent) sent.push(`The code of your current app (v${parent.n}, ${fmt(parent.html.split('\n').length)} lines) and a short summary of earlier steps`);
      kept.push(`All ${fmt(S.countryCount)} records addressed to ${S.country}, the General Comments, the Council votes and the PDFs: they stay in this browser, where your app reads them.`);
    } else if (purpose === 'inapp') {
      sent.push(`A request written by your app (${fmt(userText.length)} characters)${ids ? `, containing ${fmt(ids)} records` : ''}`);
      kept.push(ids ? `The other ${fmt(Math.max(0, S.countryCount - ids))} records stay in this browser.` : 'Everything not in the request stays in this browser.');
    } else {
      sent.push(`Your question (${fmt(userText.length)} characters), and nothing else`);
      kept.push('No data at all: the model answers from what it learned in training.');
    }
    S.trace.push({
      at: new Date(), purpose, sent, kept, records: ids,
      model: usage.model_label || (S.config.models[usage.model || S.model] || {}).label,
      host: usage.host, zdr: usage.zdr !== false, recorded: !!usage.recorded,
      tin: usage.prompt_tokens, tout: usage.completion_tokens, cost: usage.cost, seconds: usage.seconds,
      request: (sys ? `[system, ${S.route.type === 'server' ? 'added by the server' : 'added by the studio'}]\n${sys}\n\n` : '') +
        messages.map((m) => `[${m.role}]\n${m.content}`).join('\n\n'),
    });
    $('traceCount').textContent = S.trace.length;
    save();
    if (!$('drawer').hidden && $('drawerTitle').textContent === TRACE_TITLE) renderTrace();
  }

  const TRACE_TITLE = 'What left this laptop';
  const PURPOSE = { build: 'Your message', inapp: 'Your app asked a model', question: 'Question asked directly' };

  function renderTrace() {
    const T = S.trace;
    const sentWords = T.reduce((a, t) => a + wordsOf(t.tin), 0);
    const cost = T.reduce((a, t) => a + (t.cost || 0), 0);
    const recs = T.reduce((a, t) => a + t.records, 0);
    $('drawerBody').innerHTML = `
      <div class="tot">
        <div><b>${fmt(T.length)}</b><small>requests to a model</small></div>
        <div><b>≈ ${fmt(sentWords)}</b><small>words sent · $${cost.toFixed(3)}</small></div>
        <div><b>${fmt(recs)}</b><small>full records sent (only by your app's AI steps)</small></div>
        <div class="kept"><b>${fmt(S.countryCount)}</b><small>records kept in this browser</small></div>
      </div>
      ${T.length ? '' : '<p>Nothing has left this laptop yet.</p>'}
      ${T.slice().reverse().map((t) => `
        <div class="req">
          <h4>${PURPOSE[t.purpose]}<span>${t.at.toLocaleTimeString('en-GB')}</span></h4>
          <div class="meta">To <b>${esc(t.model || '')}</b>${t.host ? ' on ' + esc(t.host) : ''}${t.zdr ? ' <span class="zdr">zero data retention</span>' : ''}${t.recorded ? ' · recorded answer, nothing was sent' : ''}
            · ≈ ${fmt(wordsOf(t.tin))} words in, ${fmt(wordsOf(t.tout))} out${t.cost != null ? ' · $' + Number(t.cost).toFixed(4) : ''}${t.seconds ? ' · ' + t.seconds.toFixed(1) + ' s' : ''}</div>
          <div class="lab">${t.recorded ? 'Would be sent to a live model' : 'Sent'}</div><ul class="out">${t.sent.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
          <div class="lab">Not sent</div><ul class="kept">${t.kept.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>
          ${t.request ? `<details><summary>Show exactly what was sent</summary><pre>${esc(t.request)}</pre></details>` : ''}
        </div>`).join('')}`;
  }

  /* ---------- drawer ---------- */

  function openDrawer(title) {
    closeMenu();
    $('drawer').classList.remove('wide');
    $('drawerTitle').textContent = title;
    $('drawer').hidden = false;
  }

  /* ---------- the Look inside menu ---------- */

  function closeMenu() {
    $('lookPanel').hidden = true;
    $('lookBtn').setAttribute('aria-expanded', 'false');
  }

  function toggleMenu() {
    const open = $('lookPanel').hidden;
    $('lookPanel').hidden = !open;
    $('lookBtn').setAttribute('aria-expanded', String(open));
  }

  /* ---------- download and wall ---------- */

  function titleOf(html) {
    const m = html.match(/<title>([^<]*)<\/title>/i);
    return (m ? m[1] : 'workshop-app').trim();
  }

  async function download() {
    const v = currentVersion();
    if (!v) return;
    const blob = new Blob([await fullDoc(v)], { type: 'text/html' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${titleOf(v.html).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50) || 'app'}-v${v.n}.html`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    note(`Saved <b>${esc(a.download)}</b>. It holds the app and the data it needs, so it opens with a double-click, even offline. AI buttons inside it only work in the studio.`);
  }

  async function sendToWall() {
    const v = currentVersion();
    if (!v || S.route.type !== 'server') return;
    try {
      const res = await fetch(S.route.base + '/gallery', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seat: S.seatCode, title: titleOf(v.html), model: v.model, prompt_id: v.promptId, html: v.html,
          country: S.country, files: [...new Set(chainOf(v).flatMap((x) => x.files || []))] }),
      });
      const j = await res.json().catch(() => ({}));
      note(res.ok ? 'Sent to the wall.' : esc(j.error || 'The wall did not accept it.'));
    } catch (e) {
      note('The wall is not reachable right now.');
    }
  }

  /* ---------- chat column ---------- */

  function addUser(text, files = []) {
    const d = document.createElement('div');
    d.className = 'msg user';
    if (files.length) d.innerHTML = `<div class="files">${files.map((k) => chipHtml(k)).join('')}</div>`;
    d.append(document.createTextNode(text));
    $('log').append(d);
    // a long request shows its first lines; a click shows all of it
    if (text.length > 280 || text.split('\n').length > 6) {
      d.classList.add('clamped');
      d.title = 'Show the whole request';
      d.onclick = () => { d.classList.toggle('clamped'); d.title = d.classList.contains('clamped') ? 'Show the whole request' : ''; };
    }
    scrollLog();
  }

  function note(html) {
    const d = document.createElement('div');
    d.className = 'msg note';
    d.innerHTML = html;
    $('log').append(d);
    scrollLog();
  }

  function scrollLog() { $('log').scrollTop = $('log').scrollHeight; }

  function addAssistantLive() {
    const d = document.createElement('div');
    d.className = 'msg assistant';
    d.innerHTML = '<div class="who">' + esc(S.config.models[S.model].label) + '</div>' +
      '<details class="thought" hidden open><summary>Thinking</summary><div class="tt"></div></details>' +
      '<div class="summary"></div><div class="code"><div class="bar"><span class="stat">Waiting for the model…</span></div><pre></pre></div>';
    $('log').append(d);
    scrollLog();
    const sum = d.querySelector('.summary'), pre = d.querySelector('pre'), stat = d.querySelector('.stat');
    const th = d.querySelector('.thought'), tt = th.querySelector('.tt'), thLabel = th.querySelector('summary');
    const t0 = performance.now();
    let raf = 0, last = '', thought = '', thoughtEnd = null, folded = false;
    const secs = () => (performance.now() - t0) / 1000;
    const paint = () => {
      raf = 0;
      if (thought) {
        th.hidden = false;
        tt.textContent = thought.length > 1500 ? '…' + thought.slice(-1500) : thought;
        tt.scrollTop = tt.scrollHeight;
      }
      const code = extractHtml(last, true);
      const lines = code ? code.split('\n') : [];
      if (last && thought && !folded) { folded = true; th.open = false; thLabel.textContent = `Thought for ${thoughtEnd.toFixed(0)} s`; }
      sum.textContent = lines.length ? summaryOf(last) : last;   // an answer in words streams in full
      pre.textContent = lines.slice(-60).join('\n');
      pre.scrollTop = pre.scrollHeight;
      stat.textContent = lines.length ? `Writing code · ${fmt(lines.length)} lines · ${secs().toFixed(0)} s`
        : last ? `Answering · ${secs().toFixed(0)} s`
          : thought ? `Thinking · ${secs().toFixed(0)} s` : `Waiting for the model · ${secs().toFixed(0)} s`;
      if (thought && thoughtEnd === null) thLabel.textContent = `Thinking · ${secs().toFixed(0)} s`;
      // the stage shows the thinking, then the code as it is written, and fades to the sketch of the app
      // once the page body has begun (models write the styles first, and a sketch of those is blank)
      const thinking = !!thought && thoughtEnd === null;
      const body = code.search(/<body[\s>]/i);
      const writing = !thinking && lines.length > 0 && (body < 0 || code.length - body < 600);
      $('viewport').classList.toggle('thinking', thinking || writing);
      $('mind').classList.toggle('code', writing);
      $('mindWhere').textContent = where;
      if (thinking) {
        $('mindTitle').textContent = label + ' is thinking';
        $('mindText').textContent = thought.length > 2500 ? '…' + thought.slice(-2500) : thought;
        $('mindTime').textContent = `${secs().toFixed(0)} s`;
        $('mindNote').textContent = "The model's working notes, shown as it writes them. Ask again and they will be different. Your app is built from the code it writes next.";
      } else if (writing) {
        $('mindTitle').textContent = label + ' is writing the code';
        $('mindText').textContent = lines.slice(-40).join('\n');
        $('mindTime').textContent = `${fmt(lines.length)} lines · ${secs().toFixed(0)} s`;
        $('mindNote').textContent = 'The code runs in your browser, on the full dataset. The model wrote it from a description of the data and a few sample records.';
      }
      $('buildingText').textContent = stat.textContent;
      scrollLog();
    };
    const label = S.config.models[S.model].label;
    const where = whereOf(S.model);
    const schedule = () => { if (!raf) raf = requestAnimationFrame(paint); };
    const tick = setInterval(schedule, 1000);  // the clock keeps moving while nothing streams
    const stop = () => { clearInterval(tick); if (raf) cancelAnimationFrame(raf); $('viewport').classList.remove('thinking'); };
    return {
      step(el) { d.querySelector('.who').after(el); scrollLog(); },   // e.g. the reference shelf searched before the model answers
      who(label) { d.querySelector('.who').textContent = label; },   // a recorded answer names the model that recorded it
      think(all) { thought = all; schedule(); },
      // the answer's first words end the thinking: noted here, because a background tab may not redraw
      update(all) { if (thoughtEnd === null) thoughtEnd = secs(); last = all; schedule(); },
      // kept with the version, so the thinking is still there after a reload
      thinking() { return thought ? { thoughtTail: thought.slice(-2000), thoughtSecs: thoughtEnd } : {}; },
      done(v) {
        stop();
        if (thought) { th.hidden = false; th.open = false; thLabel.textContent = thoughtEnd != null ? `Thought for ${thoughtEnd.toFixed(0)} s` : 'Thought'; }
        sum.textContent = v.summary;
        renderCodeCard(d.querySelector('.code'), v);
        scrollLog();
      },
      fail(summary, err) {
        stop();
        sum.textContent = summary;
        d.querySelector('.code').remove();
        const e = document.createElement('div');
        e.className = 'msg err';
        e.textContent = err;
        d.append(e);
      },
      // an answer in words: rendered as text, no code card
      answer(t) {
        stop();
        if (thought) { th.hidden = false; th.open = false; thLabel.textContent = thoughtEnd != null ? `Thought for ${thoughtEnd.toFixed(0)} s` : 'Thought'; }
        sum.className = 'summary answer-md';
        sum.innerHTML = md(t.reply);
        d.querySelector('.code').remove();
        scrollLog();
      },
      lesson(text) { d.append(lessonEl(text)); },
    };
  }

  // enough Markdown for a chat answer or a plan: paragraphs, lists, headings, bold, italics, code,
  // fenced code and simple tables. A list item may run over several lines, and models often put a
  // blank line between items: consecutive items stay one list, numbered as written.
  function md(text) {
    const inline = (s) => esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<i>$2</i>');
    const out = [];
    let list = null;   // {tag, items: [html]}
    const close = () => { if (list) { out.push(`<${list.tag}${list.start > 1 ? ` start="${list.start}"` : ''}>${list.items.map((i) => `<li>${i}</li>`).join('')}</${list.tag}>`); list = null; } };
    const cells = (l) => l.trim().replace(/^\||\|$/g, '').split('|').map((c) => inline(c.trim()));
    // fenced code may hold blank lines, so it is cut out first (still open while a reply streams);
    // a heading is a block of its own, so a list may follow it on the next line
    text.trim().split(/```[^\n]*\n([\s\S]*?)(?:\n```[^\n]*|$)/).forEach((part, k) => {
      if (k % 2) { close(); out.push(`<pre class="md-code"><code>${esc(part)}</code></pre>`); return; }
      part.replace(/^(#{1,6}\s.*)$/gm, '\n$1\n').trim().split(/\n{2,}/).forEach((block) => mdBlock(block));
    });
    close();
    return out.join('');

    function mdBlock(block) {
      if (!block.trim()) return;
      const lines = block.split('\n');
      if (lines.length > 1 && lines.every((l) => /^\s*\|/.test(l)) && /^\s*\|?\s*:?-{3,}/.test(lines[1])) {
        close();
        out.push(`<div class="md-table"><table><thead><tr>${cells(lines[0]).map((c) => `<th>${c}</th>`).join('')}</tr></thead>` +
          `<tbody>${lines.slice(2).map((l) => `<tr>${cells(l).map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`);
        return;
      }
      const ul = /^\s*[-*•]\s+/, ol = /^\s*(\d+)[.)]\s+/;
      const kind = ul.test(lines[0]) ? 'ul' : ol.test(lines[0]) ? 'ol' : null;
      if (kind) {
        if (!list || list.tag !== kind) { close(); list = { tag: kind, items: [], start: kind === 'ol' ? Number(lines[0].match(ol)[1]) : 1 }; }
        lines.forEach((l) => {
          if ((kind === 'ul' ? ul : ol).test(l)) list.items.push(inline(l.replace(kind === 'ul' ? ul : ol, '')));
          else list.items[list.items.length - 1] += '<br>' + inline(l.trim());   // the item goes on
        });
        return;
      }
      close();
      const h = lines[0].match(/^(#{1,6})\s+(.*)$/);
      if (h) out.push(`<h4${h[1].length > 2 ? ' class="sub"' : ''}>${inline(h[2])}</h4>`);
      else out.push(`<p>${lines.map(inline).join('<br>')}</p>`);
    }
  }

  // the lesson's first sentence carries the point; the rest explains it
  function lessonEl(text) {
    const l = document.createElement('div');
    l.className = 'lesson';
    const i = text.indexOf('. ');
    const head = i > 0 ? text.slice(0, i + 1) : text;
    l.innerHTML = `<span class="lbl">Why this matters</span><b>${esc(head)}</b>${i > 0 ? ' ' + esc(text.slice(i + 2)) : ''}`;
    return l;
  }

  function whereOf(id) {
    const m = S.config.models[id];
    return `made in ${m.origin} · runs on ${m.host}, in ${m.host_region}`;
  }

  function renderCodeCard(box, v) {
    const lines = v.html.split('\n').length;
    box.className = 'code collapsed';
    box.innerHTML = `<div class="bar"><span>v${v.n} · ${fmt(lines)} lines · ${v.seconds ? v.seconds.toFixed(0) + ' s' : ''}${v.cost != null ? ' · $' + Number(v.cost).toFixed(3) : ''} · ${esc(v.label)}</span><button type="button">Show code</button></div><pre></pre>`;
    const pre = box.querySelector('pre');
    box.querySelector('button').onclick = (e) => {
      const open = box.classList.toggle('collapsed');
      if (!pre.textContent) pre.textContent = v.html;
      e.target.textContent = open ? 'Show code' : 'Hide code';
    };
  }

  // the conversation, apps and answers in words, in the order they happened
  function renderLog() {
    $('log').innerHTML = '';
    const items = S.versions.map((v) => ({ at: v.created, v })).concat(S.talk.map((t) => ({ at: t.created, t })));
    items.sort((x, y) => x.at - y.at).forEach(({ v, t }) => {
      const turn = v || t;
      addUser(turn.user, turn.files || []);
      const d = document.createElement('div');
      d.className = 'msg assistant';
      d.innerHTML = `<div class="who">${esc(turn.label)}</div>` +
        (turn.thoughtTail ? `<details class="thought"><summary>${turn.thoughtSecs != null ? `Thought for ${turn.thoughtSecs.toFixed(0)} s` : 'Thought'}</summary><div class="tt"></div></details>` : '') +
        '<div class="summary"></div>' + (v ? '<div class="code"></div>' : '');
      if (turn.thoughtTail) d.querySelector('.tt').textContent = '…' + turn.thoughtTail;
      if (turn.shelf) d.querySelector('.who').after(shelfStep(turn.shelf.map((id) => ({ page: { id } }))));
      if (v) {
        d.querySelector('.summary').textContent = v.summary;
        renderCodeCard(d.querySelector('.code'), v);
        const p = S.prompts.find((q) => q.id === v.promptId);
        if (p && p.lesson) d.append(lessonEl(p.lesson));
      } else {
        d.querySelector('.summary').className = 'summary answer-md';
        d.querySelector('.summary').innerHTML = md(t.reply);
      }
      $('log').append(d);
    });
  }

  const promptText = (p) => p.prompt.replace(/\{country\}/g, S.country);

  // a suggestion fills the message box, as in any chatbot: read it, change it if you like, send it.
  // The four workshop apps fill it with a short problem, in plan mode.
  function useSuggestion(p, fresh) {
    if (plannable(p)) return openPlanning(p, fresh);
    openComposer(promptText(p));
    Object.assign(S, { pendingPromptId: p.id, pendingText: promptText(p), freshNext: !!fresh });
    renderNeeds();
    renderSuggest();
    renderContinuing();
  }

  /* ---------- plan mode: a recorded planning session, then a live plan and build ---------- */

  // The planner's session for each workshop app was recorded beforehand (site/data/planning/<id>.json,
  // tools/planning/FORMAT.md). Its log streams like thinking, its looks at the data are recomputed from
  // the participant's own file, its questions come as cards, and the plan composed from the answers
  // goes on the stage. What follows is live: changes to the plan, and the build.
  const PLAN_HEAD = 'Build this app. Follow the plan below; where it says nothing, keep it simple.';
  const CHANGE = 'Change the plan: ';
  const PACE = Math.max(0.2, Number(params.get('planpace')) || 80);   // seconds the notes take (120 felt slow, 3.11); ?planpace=20 for a rehearsal
  const plannable = (p) => !!(p && p.planning && S.packs[p.id] !== null);
  const defaultOf = (q) => Math.max(0, q.options.findIndex((o) => o.default));
  const plain = (s) => s.replace(/\*\*|`/g, '').replace(/^#{1,6}\s*/gm, '');
  const ICON = {
    look: '<svg viewBox="0 0 16 16"><rect x="2" y="3" width="12" height="10" rx="1.5"/><path d="M2 7h12M6 7v6"/></svg>',
    search: '<svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.25"/><path d="m10.2 10.2 3.3 3.3"/></svg>',
    read: '<svg viewBox="0 0 16 16"><path d="M4 2h5l3 3v9H4z"/><path d="M9 2v3h3M6 9h4M6 11.5h4"/></svg>',
  };
  let shownPlan = null;   // the planning whose plan is on the stage (for its facilitator's brief)

  // a wait that Stop can cut short
  function wait(ms, signal) {
    return new Promise((resolve, reject) => {
      const stop = () => { clearTimeout(t); reject(new DOMException('stopped', 'AbortError')); };
      const t = setTimeout(() => { signal.removeEventListener('abort', stop); resolve(); }, ms);
      if (signal.aborted) stop(); else signal.addEventListener('abort', stop, { once: true });
    });
  }

  function loadPack(p) {
    if (S.packs[p.id] === undefined) {
      S.packs[p.id] = getJSON('data/' + p.planning).catch((e) => {
        S.packs[p.id] = null;   // no package: the request goes as written, without plan mode
        throw e;
      });
    }
    return S.packs[p.id];
  }

  async function openPlanning(p, fresh) {
    let pack;
    try {
      pack = await loadPack(p);
    } catch (e) {
      console.warn(`No planning session for ${p.id} (${e.message}); the request goes as written.`);
      return useSuggestion(p, fresh);
    }
    S.planMode = true;
    const text = planText(pack.problem);
    openComposer(text);
    Object.assign(S, { pendingPromptId: p.id, pendingText: text, freshNext: !!fresh });
    renderNeeds();
    renderSuggest();
    renderContinuing();
  }

  function renderPlanMode() {
    const p = S.prompts.find((q) => q.id === S.pendingPromptId);
    $('planModeBtn').hidden = !plannable(p) || S.busy;
    $('planModeBtn').setAttribute('aria-pressed', String(S.planMode));
  }

  // the plan from the chosen answers; tools/planning.py compose() writes the same text for the bake-off
  function composePlan(pack, answers) {
    const fill = {};
    pack.questions.forEach((q) => {
      const o = q.options[answers[q.id] != null ? answers[q.id] : defaultOf(q)];
      o.fragments.forEach((f) => (fill[f.section] = fill[f.section] || []).push(f.text.trim()));
    });
    return pack.plan_base.replace(/\{\{([\w.-]+)\}\}/g, (m, id) => (fill[id] || []).join('\n\n'));
  }
  // what the participant reads and the model receives: their country in place, no runs of empty lines
  const planText = (s) => s.replace(/\{country\}/g, S.country).replace(/\n{3,}/g, '\n\n').trim();

  // a "Looked at the data" step marked live is recomputed from the participant's own file
  async function lookFacts(key) {
    const f = { country: S.country };
    if (key !== 'uhri') return f;
    const d = await dataParsed('uhri');
    const years = d.records.map((r) => r.year).filter(Boolean);
    const by = (m) => fmt(d.records.filter((r) => r.mechanism === m).length);
    return Object.assign(f, {
      count: fmt(d.records.length),
      years: years.length ? `${Math.min(...years)}–${Math.max(...years)}` : 'no years',
      mechanisms: `${by('Universal Periodic Review')} from the Universal Periodic Review, ${by('Treaty bodies')} from treaty bodies, ${by('Special Procedures')} from special procedures`,
    });
  }

  // a tool step, as chatbots show them: what was looked at, searched or read
  function stepEl(s, facts = {}) {
    const fill = (t) => String(t || '').replace(/\{(country|count|years)\}/g, (m, k) => (facts[k] != null ? facts[k] : m));
    let detail = fill(s.detail);
    if (s.live === 'uhri_overview' && facts.mechanisms) detail = [detail, facts.mechanisms].filter(Boolean).join(': ');
    const row = document.createElement('div');
    row.className = 'step';
    row.innerHTML = `<span class="step-ico" aria-hidden="true">${ICON[s.kind] || ICON.look}</span><div class="step-main">` +
      `<span class="step-label">${esc(fill(s.label))}</span>${detail ? `<span class="step-detail">${esc(detail)}</span>` : ''}<span class="step-pages"></span></div>`;
    row.plainText = '→ ' + fill(s.label) + (detail ? ': ' + detail : '');
    // the shelf pages it found or read open in the drawer
    const pages = s.pages || (s.results || []).map((id) => ({ id })).concat(s.shelf_id ? [{ id: s.shelf_id, open: true }] : []);
    if (pages.length) {
      shelfLoad().then(() => {
        const box = row.querySelector('.step-pages');
        pages.forEach((pg) => {
          const page = Shelf.pages.find((x) => x.id === pg.id);
          if (!page) return;
          const b = document.createElement('button');
          b.type = 'button';
          b.className = 'linkish';
          b.textContent = pg.open ? 'Open the offline copy' : page.title;
          b.onclick = () => openShelfPage(page.id, pg.excerpt);
          box.append(b);
        });
      });
    }
    return row;
  }

  // the stage shows the thinking large, as it does before a build
  function mindShow(title, where, text, time, noteText) {
    $('viewport').classList.add('thinking');
    $('mind').classList.remove('code');
    $('mindTitle').textContent = title;
    $('mindWhere').textContent = where;
    $('mindText').textContent = text.length > 2500 ? '…' + text.slice(-2500) : text;
    $('mindTime').textContent = time;
    $('mindNote').textContent = noteText;
  }
  const mindHide = () => $('viewport').classList.remove('thinking');

  // an assistant message for plan mode: thinking in parts, steps between them, a status line, an answer
  function planMsg(who, sim) {
    const d = document.createElement('div');
    d.className = 'msg assistant plan-msg';
    d.innerHTML = `<div class="who">${esc(who)}</div>${sim || ''}<div class="flow"></div><div class="status" hidden></div><div class="summary answer-md"></div>`;
    $('log').append(d);
    scrollLog();
    const flow = d.querySelector('.flow'), st = d.querySelector('.status'), body = d.querySelector('.summary');
    return {
      el: d,
      // the recorded planner's log, or a live model's thinking
      segment(log) {
        const th = document.createElement('details');
        th.className = 'thought';
        th.open = true;
        th.innerHTML = `<summary>${log ? "Planner's log" : 'Thinking'}</summary><div class="tt md"></div>`;
        flow.append(th);
        const tt = th.querySelector('.tt'), lab = th.querySelector('summary'), t0 = performance.now();
        const secs = () => Math.max(1, Math.round((performance.now() - t0) / 1000));
        return {
          set(text) { tt.innerHTML = md(text); tt.scrollTop = tt.scrollHeight; lab.textContent = `${log ? "Planner's log" : 'Thinking'} · ${secs()} s`; scrollLog(); },
          close() { if (th.open) { th.open = false; lab.textContent = log ? "Planner's log" : `Thought for ${secs()} s`; } },
        };
      },
      step(el) { flow.append(el); scrollLog(); },
      status(t) { st.hidden = !t; st.textContent = t; scrollLog(); },
      body(html) { body.innerHTML = html; scrollLog(); },
      fail(err) {
        const e = document.createElement('div');
        e.className = 'msg err';
        e.textContent = err;
        d.append(e);
        scrollLog();
      },
    };
  }

  // Send in plan mode: the recorded session plays, then the plan waits on the stage for Build
  async function startPlanning(p, text, files) {
    const pack = await loadPack(p);
    retirePlanning('Replaced by a new plan.');
    const pl = S.planning = { p, pack, files, fresh: S.freshNext, answers: {}, version: 1, plan: '', history: [], cards: [] };
    Object.assign(S, { pendingPromptId: null, pendingText: '', freshNext: false });
    setBusy(true);
    $('building').hidden = true;
    setView('app');
    addUser(text, files);
    S.ctrl = new AbortController();
    const signal = S.ctrl.signal;
    const when = new Date((pack.recorded || '2026-11-01') + 'T12:00:00').toLocaleDateString('en-GB', { month: 'short', year: 'numeric' });
    const who = pack.planner || 'Claude Fable 5.1';
    const m = planMsg(`${who} · Plan mode`,
      `<p class="sim"><b>Simulation:</b> this plan was written beforehand by ${esc(who)} (${esc(when)}); your answers choose between versions it prepared. Changes you ask for next are made live by your model.</p>` +
      (pack.mock ? `<p class="sim mock">${esc(pack.mock)}</p>` : ''));
    const t0 = performance.now();
    const clock = () => { const s = Math.round((performance.now() - t0) / 1000); return s < 60 ? `${s} s` : `${Math.floor(s / 60)} min ${s % 60} s`; };
    const where = `recorded ${when}, replayed faster than it was written`;
    const noteText = "The planner's log: what it did and why, written for you while this plan was made. The numbers in \"Looked at the data\" are counted now, from your file.";
    let stage = '';
    try {
      const facts = await lookFacts(p.dataset);
      // the notes in parts, cut where a step happened; each step "runs" a moment
      const notes = pack.notes;
      const steps = (pack.steps || []).slice().sort((a, b) => a.at - b.at);
      const perTick = Math.max(1, Math.round(notes.length / (PACE * 20)));   // a tick is 50 ms
      let from = 0;
      for (let i = 0; i <= steps.length; i++) {
        const to = i < steps.length ? Math.min(steps[i].at, notes.length) : notes.length;
        const part = planText(notes.slice(from, to));
        from = to;
        if (part) {
          const seg = m.segment(true);
          for (let n = 0; n < part.length;) {
            await wait(50, signal);
            n = Math.min(part.length, n + perTick);
            seg.set(part.slice(0, n));
            mindShow(`${who} is planning`, where, plain(stage + part.slice(0, n)), clock(), noteText);
          }
          seg.close();
          stage += part + '\n\n';
        }
        if (i < steps.length) {
          const row = stepEl(steps[i], facts);
          row.classList.add('running');
          m.step(row);
          mindShow(`${who} is planning`, where, plain(stage) + row.plainText, clock(), noteText);
          await wait(PACE * 10, signal);
          row.classList.remove('running');
          stage += row.plainText + '\n\n';
        }
      }
      // the questions, one at a time; each answer is the participant's message
      const qs = pack.questions;
      m.body(md(`${qs.length === 1 ? 'One question' : 'A few questions'} before I write the plan.`));
      mindShow(`${who} has ${qs.length} question${qs.length === 1 ? '' : 's'} for you`, where, plain(stage), clock(), 'Answer them in the chat on the left, one at a time.');
      for (let i = 0; i < qs.length; i++) {
        await wait(PACE * 3, signal);
        pl.answers[qs[i].id] = await askCard(qs[i], i, qs.length, signal);
        addUser(qs[i].options[pl.answers[qs[i].id]].label);
      }
      // the plan streams onto the stage, like a document in any chatbot
      mindHide();
      const w = planMsg(`${who} · Plan mode`);
      pl.plan = composePlan(pack, pl.answers);
      const full = planText(pl.plan);
      const ticks = Math.max(1, Math.round(PACE * 1000 / 8 / 50));
      showPlan(pl, { version: 1, plan: '' });
      for (let n = 0; n < full.length;) {
        await wait(50, signal);
        n = Math.min(full.length, n + Math.ceil(full.length / ticks));
        $('planDoc').innerHTML = md(full.slice(0, n));
        $('planView').querySelector('.plan-scroll').scrollTop = 1e6;
        w.status(`Writing the plan · ${fmt(words(full.slice(0, n)))} words`);
      }
      w.status('');
      offerPlan(pl, w, who);
      showPlan(pl);
      w.body(md('The plan is on the right, written from your answers. Read it, then build from it or ask for a change.'));
    } catch (e) {
      mindHide();
      $('planView').hidden = true;
      if (S.planning === pl) S.planning = null;
      m.fail(e.name === 'AbortError' ? 'Stopped. Your message is back in the box.' : `The plan could not be shown (${e.message}). Your message is back in the box.`);
      openComposer(text);
      Object.assign(S, { pendingPromptId: p.id, pendingText: text, freshNext: pl.fresh });
      files.forEach((k) => S.draft.add(k));
      renderAttach();
      renderContinuing();
    } finally {
      setBusy(false);
      scrollLog();
    }
  }

  // a question as a card, as chatbots ask them: a few fixed answers, the recommended one marked
  function askCard(q, i, n, signal) {
    return new Promise((resolve, reject) => {
      const c = document.createElement('div');
      c.className = 'msg ask';
      c.innerHTML = `<div class="ask-head"><span class="ask-chip">${esc(q.header)}</span><span class="ask-n">Question ${i + 1} of ${n}</span></div>` +
        `<p class="ask-q">${esc(planText(q.question))}</p><div class="ask-opts" role="group" aria-label="${esc(planText(q.question))}">` +
        q.options.map((o, k) => `<button type="button" class="ask-opt" data-k="${k}"><span class="ask-k">${k + 1}</span><span class="ask-body">` +
          `<b>${esc(o.label)}</b>${o.default ? '<span class="rec">Recommended</span>' : ''}<small>${esc(planText(o.description || ''))}</small></span></button>`).join('') +
        '</div>' + (S.route.type === 'replay' ? '<p class="ask-note">Recorded mode builds only the recommended answers; the others show you their plan.</p>' : '');
      $('log').append(c);
      scrollLog();
      c.querySelector('.ask-opt').focus({ preventScroll: true });
      const stop = () => { c.remove(); reject(new DOMException('stopped', 'AbortError')); };
      signal.addEventListener('abort', stop, { once: true });
      c.querySelectorAll('.ask-opt').forEach((b) => {
        b.onclick = () => {
          signal.removeEventListener('abort', stop);
          c.classList.add('answered');
          c.querySelectorAll('.ask-opts, .ask-note').forEach((x) => x.remove());
          resolve(Number(b.dataset.k));
        };
      });
    });
  }

  // the plan on the stage: a document to read, not a form
  function showPlan(pl, h = pl.history[pl.history.length - 1]) {
    shownPlan = pl;
    const latest = h === pl.history[pl.history.length - 1];
    $('planTitle').textContent = pl.pack.title || pl.p.title;
    $('planKicker').textContent = (h.version === 1 ? `Plan · written beforehand by ${pl.pack.planner || 'Claude Fable 5.1'}, with your answers` : `Plan v${h.version} · changed live by ${h.by}`) +
      (latest ? '' : ' · an earlier version');
    $('planBrief').hidden = !pl.pack.facilitator_brief;
    $('planDoc').innerHTML = md(planText(h.plan));
    $('planView').hidden = false;
    $('planView').querySelector('.plan-scroll').scrollTop = 0;
  }

  function showBrief(pl) {
    openDrawer("Facilitator's brief");
    $('drawerBody').innerHTML = '<p>Your request was a sentence or two. Before the workshop, the facilitator also gave the planner this brief, and it shaped the plan. ' +
      'So the planner had your words, this brief, your data and the reference shelf: nothing else.</p>' +
      `<div class="brief answer-md">${md(pl.pack.facilitator_brief)}</div>`;
  }

  // under a finished plan: the plan as a card that opens on the stage, then Build or Change
  function offerPlan(pl, m, by) {
    const h = { version: pl.version, plan: pl.plan, by };
    pl.history.push(h);
    pl.cards.forEach((c) => c.retire(`Replaced by plan v${h.version}.`));
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'plan-card';
    card.innerHTML = `<span class="plan-card-ico" aria-hidden="true">${ICON.read}</span><span><b>${esc(pl.pack.title || pl.p.title)}</b>` +
      `<small>Plan${h.version > 1 ? ' v' + h.version : ''} · ${fmt(words(planText(h.plan)))} words · opens on the right</small></span>`;
    card.onclick = () => showPlan(pl, h);
    const box = document.createElement('div');
    box.className = 'approve';
    box.innerHTML = '<p>Build the app from this plan?</p><div class="row"><button type="button" class="primary">Build from this plan</button>' +
      '<button type="button" class="ghost">Change something</button></div>';
    const [yes, change] = box.querySelectorAll('button');
    yes.onclick = () => buildFromPlan(pl);
    change.onclick = () => changePlan(pl);
    m.el.append(card, box);
    pl.cards.push({ retire(why) { yes.disabled = change.disabled = true; box.querySelector('p').textContent = why; } });
    scrollLog();
  }

  function retirePlanning(why) {
    if (!S.planning) return;
    S.planning.cards.forEach((c) => c.retire(why));
    S.planning = null;
    $('planView').hidden = true;
  }

  function buildFromPlan(pl) {
    if (S.planning !== pl || S.busy) return;
    const h = pl.history[pl.history.length - 1];
    if (S.route.type === 'replay' && (h.version > 1 || pl.pack.questions.some((q) => pl.answers[q.id] !== defaultOf(q)))) {
      note('Recorded mode can build only the plan with the recommended answers: that is the plan the recorded app was built from. ' +
        'Your plan stays on the right to read. To build it, ask a facilitator for a seat code, or start this app again and keep the recommended answers.');
      return;
    }
    pl.changing = false;
    const text = PLAN_HEAD + '\n\n' + planText(h.plan);
    Object.assign(S, { pendingPromptId: pl.p.id, pendingText: text, freshNext: pl.fresh });
    pl.building = true;
    if (!submitBuild(text, pl)) pl.building = false;
  }

  function changePlan(pl) {
    if (S.planning !== pl || S.busy) return;
    if (S.route.type === 'replay') {
      note('Changes to a plan are made live by your model, and in recorded mode no model is connected. Build the plan as it is, or ask a facilitator for a seat code.');
      return;
    }
    pl.changing = true;
    openComposer(CHANGE);
    $('input').setSelectionRange(CHANGE.length, CHANGE.length);
  }

  // a model's plan, without what it may have written around it
  function planOf(reply) {
    const t = reply.replace(/^\s*```(?:markdown|md)?[ \t]*\n/i, '').replace(/\n```\s*$/, '');
    const i = t.search(/^#{1,4}\s/m);
    return i >= 0 ? t.slice(i).trim() : '';
  }

  // Change something: the participant's model rewrites the plan, live, and plan v2 goes on the stage
  async function revisePlan(pl, text) {
    pl.changing = false;
    $('input').value = '';
    fitInput();
    const h = pl.history[pl.history.length - 1];
    const label = S.config.models[S.model].label;
    setBusy(true);
    $('building').hidden = true;
    addUser(text);
    await shelfLoad();
    const hits = shelfSearch(text);
    const content = `Here is the plan for an app I am about to build (version ${h.version}):\n\n${planText(h.plan)}\n\n${text}\n\n` +
      'Reply with the whole revised plan in Markdown, with the same headings, and nothing else: no code, no comment before or after it.' + shelfBlock(hits);
    const messages = [{ role: 'user', content }];
    const m = planMsg(label);
    if (hits.length) m.step(shelfStep(hits));
    const t0 = performance.now();
    const secs = () => `${Math.round((performance.now() - t0) / 1000)} s`;
    let seg = null, painted = 0;
    S.ctrl = new AbortController();
    try {
      const { text: reply, usage } = await chat({
        purpose: 'build', model: S.model, messages, signal: S.ctrl.signal,
        onThought: (all) => {
          seg = seg || m.segment();
          seg.set(all);
          mindShow(`${label} is thinking`, whereOf(S.model), all, secs(), "The model's working notes, shown as it writes them.");
        },
        onDelta: (all) => {
          if (seg) seg.close();
          mindHide();
          const plan = planOf(all);
          m.status(`Rewriting the plan · ${fmt(words(plan))} words · ${secs()}`);
          if (!plan || performance.now() - painted < 150) return;
          painted = performance.now();
          if (shownPlan !== pl || $('planView').hidden) showPlan(pl);
          $('planKicker').textContent = `Plan v${h.version + 1} · being changed live by ${label}`;
          $('planDoc').innerHTML = md(plan);
        },
      });
      addTrace({ purpose: 'build', usage, messages, userText: text, shelf: hits, plan: h });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      if (seg) seg.close();
      m.status('');
      const plan = planOf(reply);
      if (!plan) {   // an answer without a plan: the plan, and its Build button above, stay as they were
        m.body(md((reply.trim() || 'The model sent back nothing.') + '\n\n*The plan is unchanged.*'));
        showPlan(pl, h);
        return;
      }
      pl.version = h.version + 1;
      pl.plan = plan;
      m.body(md(`Plan v${pl.version} is on the right, with your change.`));
      offerPlan(pl, m, label);
      showPlan(pl);
    } catch (e) {
      if (seg) seg.close();
      m.status('');
      m.fail(friendly(e));
      pl.changing = true;
      openComposer(text);
      showPlan(pl, h);
    } finally {
      mindHide();
      setBusy(false);
    }
  }

  /* ---------- the reference shelf: offline copies of good-practice pages, searched on each message ---------- */

  // BM25 over passages of about 150 words, scored as tools/shelf.py scores them
  const STOP = new Set(('a an and are as at be by for from has have in is it its of on or that the this to was were will with ' +
    'you your can should not but if into than then there these they their which when what how').split(' '));
  const K1 = 1.2, B = 0.75;
  const shelfTokens = (s) => (s.toLowerCase().match(/[a-z0-9]+/g) || []).filter((t) => !STOP.has(t) && t.length > 1);
  const Shelf = { ready: null, pages: [], docs: [], df: new Map(), avg: 1 };

  function passagesOf(text, size = 150) {
    const out = [];
    let cur = [], n = 0;
    text.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean).forEach((p) => {
      cur.push(p);
      n += p.split(/\s+/).length;
      if (n >= size) { out.push(cur.join('\n\n')); cur = []; n = 0; }
    });
    if (cur.length) out.push(cur.join('\n\n'));
    return out;
  }

  function shelfLoad() {
    if (!Shelf.ready) {
      Shelf.ready = getJSON('data/shelf.json').then((j) => {
        Shelf.pages = j.records || [];
        Shelf.pages.forEach((page) => passagesOf(page.text || '').forEach((text) => {
          const tf = new Map();
          shelfTokens(text + ' ' + page.title).forEach((w) => tf.set(w, (tf.get(w) || 0) + 1));
          Shelf.docs.push({ page, text, tf, len: [...tf.values()].reduce((a, b) => a + b, 0) });
        }));
        Shelf.docs.forEach((d) => d.tf.forEach((c, w) => Shelf.df.set(w, (Shelf.df.get(w) || 0) + 1)));
        Shelf.avg = Shelf.docs.reduce((a, d) => a + d.len, 0) / Math.max(1, Shelf.docs.length);
      }).catch(() => { /* no shelf: messages go without excerpts */ });
    }
    return Shelf.ready;
  }

  // the best passage of up to three pages. A passage counts when it shares at least two different
  // words with the message and scores at least what one word found in a single passage would:
  // one common word in both is not a reason to send it to the model.
  function shelfSearch(query) {
    const n = Shelf.docs.length;
    const q = shelfTokens(query);
    if (!n || !q.length) return [];
    const idf = (w) => Math.log(1 + (n - Shelf.df.get(w) + 0.5) / (Shelf.df.get(w) + 0.5));
    const floor = Math.log(1 + (n - 0.5) / 1.5);
    const hits = Shelf.docs.map((d) => {
      let s = 0;
      const shared = new Set();
      q.forEach((w) => {
        const c = d.tf.get(w);
        if (!c) return;
        shared.add(w);
        s += idf(w) * c * (K1 + 1) / (c + K1 * (1 - B + B * d.len / Shelf.avg));
      });
      return { d, s, shared: shared.size };
    }).filter((h) => h.shared >= 2 && h.s >= floor).sort((a, b) => b.s - a.s);
    const out = [];
    hits.forEach((h) => {
      if (out.length < 3 && !out.some((o) => o.page.id === h.d.page.id)) out.push({ page: h.d.page, text: h.d.text });
    });
    return out;
  }

  // what is added to the message, so the model can use it (and the trace shows it went out)
  function shelfBlock(hits) {
    if (!hits.length) return '';
    const kind = (p) => ({ summary: 'a summary written for the workshop', code: 'code' }[p.kind] || 'an excerpt');
    return '\n\nReference shelf excerpts (offline copies)\n' +
      'Found by a keyword search of the workshop reference shelf on this message. Use what helps; if the app uses a page\'s code or wording, credit it in the app.\n\n' +
      hits.map((h, i) => `[${i + 1}] ${h.page.title}. ${h.page.publisher}; ${kind(h.page)}; ${h.page.licence}; retrieved ${h.page.retrieved}. ${h.page.url}\n\n${h.text}`).join('\n\n');
  }

  const shelfStep = (hits) => stepEl({
    kind: 'search', label: `Searched the reference shelf · ${hits.length} page${hits.length === 1 ? '' : 's'}`,
    pages: hits.map((h) => ({ id: h.page.id, excerpt: h.text })),
  });

  async function openShelfPage(id, excerpt) {
    await shelfLoad();
    const pg = Shelf.pages.find((x) => x.id === id);
    openDrawer(pg ? pg.title : 'Reference shelf');
    if (!pg) { $('drawerBody').innerHTML = '<p>This page is not on the reference shelf.</p>'; return; }
    const kind = { summary: 'A summary written for the workshop', code: 'Code' }[pg.kind] || 'An excerpt';
    const orig = /^https?:\/\//.test(pg.url) ? ` · <a href="${esc(pg.url)}" target="_blank" rel="noopener">The original</a>` : '';
    $('drawerBody').innerHTML = `<p class="src-head">${kind}, from ${esc(pg.publisher)} · ${esc(pg.licence)}${orig}<br>` +
      `Workshop reference shelf: an offline copy, retrieved ${esc(pg.retrieved || '')}, not the live web.</p>` +
      (excerpt ? `<div class="sent-excerpt"><div class="lab">Sent to the model with your message</div><div class="answer-md">${md(excerpt)}</div></div>` : '') +
      `<div class="answer-md shelf-text">${md(pg.text)}</div>`;
  }

  function openComposer(text) {
    S.pendingPromptId = null;
    S.pendingText = '';
    if (text != null) $('input').value = text;
    renderSuggest();
    fitInput();
    $('input').focus();
  }

  // the box grows with what is in it, so a long request can be read before it is sent
  function fitInput() {
    const t = $('input');
    t.style.height = 'auto';
    t.style.height = Math.min(t.scrollHeight + 2, window.innerHeight * 0.4) + 'px';
  }

  function renderSuggest() {
    const box = $('suggest');
    box.innerHTML = '';
    renderPlanMode();
    if (!S.ready || S.busy) return;
    const v = currentVersion();
    const used = new Set(chainOf(v).map((x) => x.promptId));
    const built = new Set(S.versions.map((x) => x.promptId));
    const live = S.route && S.route.type !== 'replay';
    const mine = (p) => p.session === S.session && p.id !== S.pendingPromptId && !(S.planning && S.planning.p.id === p.id);
    // Hick's law: a few suggestions at a time, never the whole list
    // a next step continues this app; it may bring a file of its own (a second document to add)
    const next = v ? S.prompts.filter((p) => mine(p) && p.builds_on && p.builds_on !== 'any' && !used.has(p.id) && used.has(p.builds_on)).slice(0, 2) : [];
    if (v && live) next.push(...S.prompts.filter((p) => p.builds_on === 'any' && p.id !== S.pendingPromptId));   // "Suggest improvements"
    // Hick's law: Session 8 keeps its three apps in view (PDF, Verbatim finder, wiki); Session 7 has one
    const starters = S.prompts.filter((p) => mine(p) && !p.builds_on && !built.has(p.id)).slice(0, !v || S.session === 'S8' ? 3 : 1);
    const group = (label, list, fresh) => {
      if (!list.length) return;
      const l = document.createElement('div');
      l.className = 'lbl';
      l.textContent = label;
      box.append(l);
      list.forEach((p) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.innerHTML = `<b>${esc(p.title)}</b><span>${esc(p.blurb || '')}</span>`;
        b.title = (p.blurb ? p.blurb + '\n\n' : '') + (plannable(p) ? 'Plan mode: the model looks at your data and asks you a few questions before it builds.' : promptText(p));
        if (fresh) b.classList.add('new');
        b.onclick = () => useSuggestion(p, fresh);
        box.append(b);
      });
    };
    box.classList.toggle('compact', !!v || !!S.planning);   // a plan waiting to be built keeps the room
    group('Next step', next, false);
    group(v ? 'Or start a new app' : 'Try one of these', starters, !!v);
  }

  function renderContinuing() {
    const el = $('continuing');
    const v = currentVersion();
    if (S.freshNext && v) { el.hidden = false; el.textContent = 'Starts a new app. Your versions stay in the list above the preview.'; return; }
    if (v && v.n !== S.versions.length) { el.hidden = false; el.textContent = `Your next message continues from v${v.n}.`; return; }
    el.hidden = true;
  }

  // what a participant can see grows with what they have done (Hick's law)
  function renderTools() {
    const has = S.versions.length > 0;
    const s8 = S.session === 'S8';
    $('toolbar').hidden = !has;
    $('ask3Btn').hidden = !s8 || !S.route || S.route.type === 'replay';
    $('linkBtn').hidden = !s8 && S.linkOn;
    $('wallBtn').hidden = !(S.route && S.route.type === 'server');
    $('linkOffPill').hidden = S.linkOn;
    $('traceCount').hidden = !S.trace.length;
    ['downloadBtn', 'wallBtn', 'lookBtn'].forEach((id) => { $(id).disabled = !has; });
  }

  function renderSession() {
    document.querySelectorAll('#sessionSwitch button').forEach((b) => b.setAttribute('aria-selected', b.dataset.session === S.session));
  }

  function setSession(s) {
    if (s === S.session || S.busy) return;
    S.session = s;
    localSet('ws:session', s);
    renderSession();
    renderTools();
    renderSuggest();
    if (!S.versions.length) return;
    note(s === 'S8'
      ? '<b>Session 8.</b> New suggestions below. <b>Look inside</b> now also lets you ask the model directly and cut the model link.'
      : '<b>Session 7.</b> The suggestions below are from the first session.');
  }

  function renderVersions() {
    const box = $('versions');
    box.innerHTML = '';
    S.versions.forEach((v) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', v.n === S.current);
      b.textContent = 'v' + v.n;
      b.title = v.user.slice(0, 140);
      b.onclick = async () => {
        S.current = v.n;
        S.freshNext = false;
        renderVersions();
        renderSuggest();
        await showVersion(v);
        save();
      };
      box.append(b);
    });
    box.scrollLeft = box.scrollWidth;
    renderTools();
  }

  function renderModelMenu() {
    const sel = $('modelSelect');
    sel.innerHTML = S.config.model_groups.map((g) =>
      `<optgroup label="${esc(g.label)}">${g.ids.map((id) => `<option value="${id}">${esc(S.config.models[id].label)}</option>`).join('')}</optgroup>`).join('');
    sel.value = S.model;
    renderBadge();
  }

  function renderBadge() {
    const m = S.config.models[S.model];
    $('modelBadge').innerHTML = `Made in <b>${esc(m.origin)}</b> · runs in <b>${esc(m.host_region)}</b>`;
    $('modelBadge').title = `${m.label} by ${m.maker}, made in ${m.origin}. Runs on ${m.host}: ${m.host_note}. ` +
      `Zero data retention: the host may not keep what is sent. Price: ${m.price}.`;
    $('modelSelect').title = $('modelBadge').title;
  }

  function renderAll() {
    renderVersions();
    renderLog();
    renderShelf();
    renderSuggest();
    renderContinuing();
    $('traceCount').textContent = S.trace.length;
    renderTools();
    const v = currentVersion();
    if (v) showVersion(v);
  }

  /* ---------- the file shelf ---------- */

  function fileMetaLine(key) {
    const d = S.index.datasets[key];
    if (key === 'library') return `${fmt(d.count)} PDFs · passage by passage, with pages`;
    if (key === 'wiki') return `${fmt(d.count)} pages · every quotation verified`;
    if (key === 'uhri') return `${fmt(S.countryCount)} records · opens in Excel`;
    if (key === 'gc') return `${fmt(d.count)} paragraphs · opens in Excel`;
    if (key === 'hrc') return `${fmt(d.count)} recorded votes · opens in Excel`;
    return `${fmt(d.count)} pages · opens in your browser`;
  }

  // the shelf lives on the empty stage before the first app, and in the Your files drawer after it
  function renderShelf(box = $('shelf')) {
    box.innerHTML = S.config.files.map((f) => `
      <div class="fcard" draggable="true" data-key="${f.key}">
        <div class="fcard-top"><i class="ficon ${f.kind}">${f.kind.toUpperCase()}</i><h3>${esc(fileLabel(f.key))}</h3></div>
        <p>${esc(f.blurb.replace(/\{country\}/g, S.country))}</p>
        <div class="meta">${esc(fileMetaLine(f.key))}</div>
        ${f.from ? `<p class="from">Also published as data: ${f.from.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`).join(' · ')}</p>` : ''}
        <div class="row"><button type="button" class="ghost" data-act="open">Open</button><button type="button" class="ghost" data-act="add">Add to chat</button></div>
      </div>`).join('');
    box.querySelectorAll('.fcard').forEach((c) => {
      const key = c.dataset.key;
      c.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/x-studio-file', key);
        e.dataTransfer.setData('text/plain', fileLabel(key));
        e.dataTransfer.effectAllowed = 'copy';
      });
      c.querySelector('[data-act=open]').onclick = () => openFile(key);
      c.querySelector('[data-act=add]').onclick = () => addFile(key);
    });
    renderShelfState();
  }

  // which files are already in the chat, and which one the current request still needs
  function renderShelfState(needed) {
    const have = new Set([...attachedBefore(), ...S.draft]);
    document.querySelectorAll('.fcard').forEach((c) => {
      c.classList.toggle('used', have.has(c.dataset.key));
      c.classList.toggle('needed', c.dataset.key === needed);
    });
  }

  function showFiles(needed) {
    if (S.versions.length) {
      openDrawer('Your files');
      $('drawerBody').innerHTML = '<p>Open a file to see what is inside, or drag it into the chat on the left.</p><div class="shelf" id="drawerShelf"></div>' +
        '<p class="shelf-note">A file in the chat gives your app the whole file, here in your browser. The model reads only a short description of it and a few sample rows.</p>';
      renderShelf($('drawerShelf'));
    }
    renderShelfState(needed);
  }

  async function openFile(key) {
    const f = fileMeta(key);
    if (f.kind === 'pdf') { window.open(f.pdf, '_blank', 'noopener'); return; }
    if (f.kind === 'wiki') {
      const w = await dataParsed(key);
      openDrawer(fileLabel(key));
      $('drawerBody').innerHTML = `<p>The wiki's catalog, as its index page keeps it. Drag the wiki into the chat to build a workspace on it.</p>` +
        `<div class="answer-md">${md(w.index.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (m, s, t) => '**' + (t || s) + '**'))}</div>`;
      return;
    }
    if (f.kind === 'lib') {
      const lib = await dataParsed(key);
      openDrawer(fileLabel(key));
      $('drawerBody').innerHTML = `<p>${lib.records.length} documents of ${new Set(lib.records.map((d) => d.kind)).size} kinds, each as it was published. Open one, or drag the library into the chat to build on all of them.</p>` +
        lib.records.map((d) => `<div class="tool-card"><h4>${esc(d.short_title)}</h4><p>${esc(d.kind)} · ${esc(d.author)} · ${d.year} · ${fmt(d.passages.length)} passages, ${d.pages} pages</p>` +
          `<div class="row"><button type="button" class="ghost" data-sym="${esc(d.id)}">Open the PDF</button></div></div>`).join('');
      $('drawerBody').querySelectorAll('[data-sym]').forEach((b) => { b.onclick = () => openSource(b.dataset.sym, 1); });
      return;
    }
    const d = await dataParsed(key);
    const blob = new Blob(['﻿' + csvOf(key, d)], { type: 'text/csv;charset=utf-8' });   // the mark tells Excel it is UTF-8
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (key === 'uhri' ? 'un-recommendations-' + S.country : fileLabel(key)).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '.csv';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  // one row per record; lists joined with "; ", and each State's vote spelt out
  function csvOf(key, d) {
    const cell = (v) => {
      const s = v == null ? '' : Array.isArray(v) ? v.join('; ') : String(v);
      return /[",\r\n;]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    };
    let cols = Object.keys(d.records[0]);
    let row = (r) => cols.map((c) => r[c]);
    if (key === 'hrc') {
      const word = { Y: 'yes', N: 'no', A: 'abstained' };
      cols = cols.filter((c) => c !== 'votes').concat('votes');
      row = (r) => cols.map((c) => (c === 'votes' ? Object.entries(r.votes || {}).map(([k, v]) => `${d.countries[k] || k}: ${word[v] || v}`) : r[c]));
    }
    return [cols.map(cell).join(','), ...d.records.map((r) => row(r).map(cell).join(','))].join('\r\n');
  }

  /* ---------- the app, or the code behind it ---------- */

  let viewing = 'app';
  function setView(v) {
    viewing = v;
    $('viewApp').setAttribute('aria-selected', v === 'app');
    $('viewCode').setAttribute('aria-selected', v === 'code');
    $('codeView').hidden = v !== 'code';
    if (v === 'code') renderCode();
  }

  function renderCode() {
    const v = currentVersion();
    const src = v ? v.html : '';
    $('codeText').innerHTML = `<span class="gutter">${src.split('\n').map((_, i) => i + 1).join('\n')}</span><code>${highlight(src)}</code>`;
  }

  // a light colouring of HTML, CSS and JavaScript: comments, strings, tags, attributes, keywords, numbers
  function highlight(src) {
    const re = /(<!--[\s\S]*?-->|\/\*[\s\S]*?\*\/|(?<![:"'\w])\/\/[^\n]*)|("(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|`(?:\\.|[^`\\])*`)|(<\/?[a-zA-Z][\w-]*|\/?>)|(\b[a-zA-Z-]+(?==))|\b(const|let|var|function|return|if|else|for|while|of|in|new|async|await|true|false|null|undefined|class|try|catch|throw|switch|case|break|continue|typeof)\b|(\b\d+(?:\.\d+)?\b)/g;
    let out = '', last = 0, m;
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index));
      const cls = m[1] ? 'com' : m[2] ? 'str' : m[3] ? 'tag' : m[4] ? 'attr' : m[5] ? 'kw' : 'num';
      out += `<span class="tk-${cls}">${esc(m[0])}</span>`;
      last = re.lastIndex;
    }
    return out + esc(src.slice(last));
  }

  /* ---------- who made this, and where to take it ---------- */

  const link = (url, text, title) => `<a href="${url}" target="_blank" rel="noopener"${title ? ` title="${esc(title)}"` : ''}>${text}</a>`;

  function renderFooter() {
    const a = S.config.author;
    $('footWho').innerHTML = `Made by ${link(a.url, `<b>${esc(a.name)}</b>`)}, ${link(a.place_url, esc(a.place))}`;
    $('footLinks').innerHTML = 'Open tools: ' + a.tools.map((t) => link(t.url, esc(t.name), t.blurb)).join(' · ') + `<span class="tb"> · ${link(a.github, 'GitHub')}</span>`;
    renderTheme();
  }

  function takeFurther() {
    const a = S.config.author;
    openDrawer('Take it further');
    $('drawerBody').innerHTML = `
      <p>${esc(a.line)} These open tools were built the way you built your app today: a model writes the code, the code does the counting, and a person checks it.</p>
      ${a.tools.map((t) => `<div class="tool-card"><h4><a href="${t.url}" target="_blank" rel="noopener">${esc(t.name)}</a></h4>
        <p>${esc(t.blurb)}${t.with ? ` With ${esc(t.with)}.` : ''}</p>
        <div class="row"><a href="${t.url}" target="_blank" rel="noopener">Open the tool</a> · <a href="${t.repo}" target="_blank" rel="noopener">Source code</a></div></div>`).join('')}
      <h4>Take the method home</h4>
      <p>Point an AI coding assistant (Claude Code, Codex, Antigravity, Cursor) at one of these public repositories. Ask for a review first, then make one change at a time and check it.</p>
      <label>Repository <select id="tfRepo">${a.tools.map((t) => `<option value="${t.repo}">${esc(t.name)}</option>`).join('')}</select></label>
      <div class="prompt-box"><textarea id="tfPrompt" readonly></textarea></div>
      <div class="row"><button type="button" class="primary" id="tfCopy">Copy the prompt</button></div>
      <p class="caution">These assistants send the files they read to the company that runs the model. That is fine for public code like this; never point them at confidential documents.</p>
      <p>${esc(a.name)} · ${link(a.url, 'website')} · ${link(a.orcid, 'ORCID')} · ${link(a.github, 'GitHub')}</p>`;
    const fill = () => {
      $('tfPrompt').value = `You are reviewing an open-source research tool for human rights work: ${$('tfRepo').value}

1. Clone the repository. Read the README, then the code.
2. Explain in five sentences what the tool does and how its numbers are computed.
3. List ten concrete improvements, numbered, in four groups: correctness of the numbers, clarity of how they are computed, accessibility, documentation. For each: what to change, in which file, and why it matters to a human rights researcher.
4. Do not change any code yet. I will pick one improvement at a time; make only that change, show me the diff, and tell me how to check it.`;
    };
    fill();
    $('tfRepo').onchange = fill;
    $('tfCopy').onclick = async () => {
      try { await navigator.clipboard.writeText($('tfPrompt').value); $('tfCopy').textContent = 'Copied'; } catch (e) { $('tfPrompt').select(); }
    };
  }

  const darkNow = () => document.documentElement.dataset.theme === 'dark' ||
    (!document.documentElement.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);

  function renderTheme() {
    $('themeBtn').textContent = darkNow() ? 'Light mode' : 'Dark mode';
    $('themeBtn').setAttribute('aria-pressed', String(darkNow()));
  }

  function toggleTheme() {
    const t = darkNow() ? 'light' : 'dark';
    document.documentElement.dataset.theme = t;
    localSet('ws:theme', t);
    renderTheme();
  }

  /* ---------- the divider between the conversation and the app ---------- */

  // each participant sets their own split; it is kept in this browser
  const CHAT_MIN = 280;
  const chatMax = () => Math.round(window.innerWidth * 0.65);
  function setChatWidth(px, keep) {
    const work = document.querySelector('.work');
    if (px == null) { work.style.removeProperty('--chat-w'); if (keep) localSet('ws:chatw', ''); return; }
    const w = Math.max(CHAT_MIN, Math.min(chatMax(), Math.round(px)));
    work.style.setProperty('--chat-w', w + 'px');
    $('splitter').setAttribute('aria-valuenow', String(w));
    if (keep) localSet('ws:chatw', String(w));
  }

  function wireSplitter() {
    const sp = $('splitter');
    const saved = Number(localGet('ws:chatw'));
    if (saved) setChatWidth(saved, false);
    sp.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      sp.setPointerCapture(e.pointerId);
      document.body.classList.add('resizing');
      const left = document.querySelector('.work').getBoundingClientRect().left;
      const move = (ev) => setChatWidth(ev.clientX - left, false);
      const up = (ev) => {
        sp.releasePointerCapture(ev.pointerId);
        sp.removeEventListener('pointermove', move);
        sp.removeEventListener('pointerup', up);
        document.body.classList.remove('resizing');
        setChatWidth(document.querySelector('.chat').getBoundingClientRect().width, true);
        fitInput();
      };
      sp.addEventListener('pointermove', move);
      sp.addEventListener('pointerup', up);
    });
    sp.addEventListener('dblclick', () => { setChatWidth(null, true); fitInput(); });
    window.addEventListener('resize', () => { const w = Number(localGet('ws:chatw')); if (w) setChatWidth(w, false); });
    sp.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      setChatWidth(document.querySelector('.chat').getBoundingClientRect().width + (e.key === 'ArrowRight' ? 24 : -24), true);
    });
  }

  /* ---------- persistence (per seat and country; survives a reload) ---------- */

  function localGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function localSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  const storeKey = () => `ws:work:${S.seatCode || 'guest'}`;   // one workspace per seat; the country is a separate choice

  function save() {
    // the full text sent with each request is not kept: it would fill the browser's storage
    const trace = S.trace.map((t) => Object.assign({}, t, { request: '', at: t.at.toISOString() }));
    localSet(storeKey(), JSON.stringify({ versions: S.versions, current: S.current, talk: S.talk, trace }));
  }

  function restore() {
    try {
      const d = JSON.parse(localGet(storeKey()) || 'null');
      if (d && Array.isArray(d.versions)) { S.versions = d.versions; S.current = d.current; }
      if (d && Array.isArray(d.talk)) S.talk = d.talk;
      if (d && Array.isArray(d.trace)) S.trace = d.trace.map((t) => Object.assign(t, { at: new Date(t.at) }));
    } catch (e) { /* start clean */ }
  }

  /* ---------- wiring ---------- */

  Preview.init();
  wireSplitter();
  $('planClose').onclick = () => { $('planView').hidden = true; };
  $('planBrief').onclick = () => shownPlan && showBrief(shownPlan);
  $('planModeBtn').onclick = () => { S.planMode = !S.planMode; renderPlanMode(); $('input').focus(); };
  $('composer').addEventListener('submit', (e) => { e.preventDefault(); submitBuild($('input').value); });
  // Enter sends, as in any chatbot; Shift+Enter starts a new line
  $('input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); submitBuild($('input').value); }
  });
  $('input').addEventListener('input', () => {
    fitInput();
    if (!$('input').value.trim()) { S.pendingPromptId = null; S.pendingText = ''; S.freshNext = false; renderContinuing(); renderNeeds(); renderSuggest(); }
  });
  // a file from the shelf, dropped anywhere on the chat column
  const chatCol = document.querySelector('.chat');
  const isFile = (e) => [...(e.dataTransfer && e.dataTransfer.types || [])].includes('text/x-studio-file');
  chatCol.addEventListener('dragover', (e) => { if (isFile(e)) { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; chatCol.classList.add('dragging'); } });
  chatCol.addEventListener('dragleave', (e) => { if (!chatCol.contains(e.relatedTarget)) chatCol.classList.remove('dragging'); });
  chatCol.addEventListener('drop', (e) => {
    chatCol.classList.remove('dragging');
    if (!isFile(e)) return;
    e.preventDefault();   // not as text into the box
    addFile(e.dataTransfer.getData('text/x-studio-file'));
  });
  document.addEventListener('dragend', () => chatCol.classList.remove('dragging'));
  // before the first app the shelf is on the stage already: point at it
  $('addFileBtn').onclick = () => {
    if (S.versions.length) return showFiles();
    document.querySelectorAll('#shelf .fcard').forEach((c) => { c.classList.remove('needed'); void c.offsetWidth; c.classList.add('needed'); });
    setTimeout(() => renderNeeds(), 2200);
  };
  $('filesBtn').onclick = () => showFiles();
  $('tabBtn').onclick = openTab;
  $('viewApp').onclick = () => setView('app');
  $('viewCode').onclick = () => setView('code');
  $('takeHomeBtn').onclick = takeFurther;
  $('tourBtn').onclick = () => Tour.start();
  $('themeBtn').onclick = toggleTheme;
  $('stopBtn').onclick = () => S.ctrl && S.ctrl.abort();
  $('countrySelect').onchange = (e) => changeCountry(e.target.value);
  $('modelSelect').onchange = (e) => {
    S.model = e.target.value;
    localSet('ws:model', S.model);
    renderBadge();
    if (S.versions.length) note(`Your next build goes to <b>${esc(S.config.models[S.model].label)}</b> (${esc(whereOf(S.model))}). Earlier versions keep the model that made them.`);
  };
  document.querySelectorAll('#sessionSwitch button').forEach((b) => { b.onclick = () => setSession(b.dataset.session); });
  $('lookBtn').onclick = (e) => { e.stopPropagation(); toggleMenu(); };
  document.addEventListener('click', (e) => { if (!e.target.closest('.menu')) closeMenu(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeMenu(); $('drawer').hidden = true; } });
  $('layersBtn').onclick = toggleLayers;
  $('run3Btn').onclick = run3;
  $('ask3Btn').onclick = () => ask3('count');
  $('linkBtn').onclick = toggleLink;
  $('traceBtn').onclick = () => { openDrawer(TRACE_TITLE); renderTrace(); };
  $('downloadBtn').onclick = download;
  $('wallBtn').onclick = sendToWall;
  $('drawerClose').onclick = () => { $('drawer').hidden = true; };

  boot().catch((e) => {
    note('The studio could not start: ' + esc(e.message) + '. Reload the page; if it persists, tell a facilitator.');
  });
})();
