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
    draftImages: [],     // screenshots pasted or dropped into it: [{media_type, data, url, w, h, kb}]
    trace: [],
    busy: false, ctrl: null, dataText: {}, dataParsed: {},
    planMode: true,      // the four workshop apps plan first (the pill above the message box)
    freeBrief: {},       // request id -> true where its planning pack takes any brief the participant writes (set when the pack loads)
    planning: null,      // the plan being made or waiting to be built
    packs: {},           // planning packages by request id; null where there is none
    own: {},             // the participant's own files (own-files.js), by key: kept in this browser
    advanced: false,     // Basic shows one path through the exercises; Advanced (footer) shows the rest
    course: 'full',      // 'geneva' (?course=geneva, one session), 'venice' (?course=venice) or 'full': see COURSE
    progress: { done: Array(7).fill(false), skipped: Array(7).fill(false) },   // the seven steps of the one-session course
    test: { shown: false, checks: [false, false, false], note: '' },   // the "Test your app" card (step 6); kept with the work
    wallAsked: false,    // "Show it to the room?" was opened once, at 100%; kept with the work, never asked twice
    lastLenses: [],      // the three perspectives of the previous "Suggest three improvements"
  };
  // Everything that differs between the courses lives here, so no other code asks which course it is.
  //   full:   the two-session Geneva path of before (S7, S8), the whole shelf, Advanced
  //   venice: the Global Campus, three sessions (V1-V3), the course picks the requests
  //   geneva: the one-session workshop of 4 December 2026 (G1)
  // sessions: its session ids, shown as 1, 2, 3.  promptKey: the field of prompts.json that gives a request its session.
  // storeId: the course part of the key a participant's work is kept under (the two-session path keeps 'geneva', the id
  // it had before there were three courses, so earlier work still loads).  roomId: the room chat's course.
  // models: the menu, in order (null: every model).  country: whether there is a country picker.  advanced: whether the
  // Advanced switch exists.  wallWithoutAdvanced / ignoreLevel: the course, not Advanced, picks the requests.
  // ownSession: the one session where one's own files are allowed without Advanced.  askDirect: "Ask the model directly"
  // in the later sessions.  tour: starts by itself on a first visit.  pace: seconds the recorded planning takes.
  // files: null (the shelf without the Venice-only files), 'session' (what the open session's requests read) or a list.
  // kit: the take-home kit's requests and data.  planBrief: the facilitator's brief button.  event: the key in config.json.
  // feedbackHint, improveSwap, courseLink, look, progress: the feedback box's hint, one way to improve, the course-page
  // link, the Look inside menu and the seven-step bar.  briefCard: the participant writes a brief from labelled paragraphs
  // (a pack with free_brief) instead of picking a suggestion.  insideFile: "Open" on the General Comments shelf card shows
  // "What is in the file" instead of downloading it.
  // keepModel: a model that is busy or fails is never swapped for another behind the participant's back: the studio says so
  // and offers Try again or the other model (the server is asked with fallback:false).  ideas: "Suggest three improvements"
  // (three cards, one request) instead of the five review lenses.  signWall: a name may sign what goes on the wall, which is
  // asked once at 100%.  dataFirst: the chat opens on a card about the data ("Look inside the file"); the brief card
  // comes under it, and the bar starts with Data.  backup: when the model or the server fails, the participant or the facilitator
  // switches to recorded answers (the badge, the error boxes, the admin page's "Recorded answers for everyone"), and recorded mode
  // plays the whole session: the app recorded beforehand for the plan's look, three recorded ideas, a recorded improvement.
  const COURSE = {
    full: {
      sessions: ['S7', 'S8'], promptKey: 'session', storeId: 'geneva', roomId: 'full', models: null, country: true,
      advanced: true, wallWithoutAdvanced: false, ignoreLevel: false, ownSession: null, askDirect: true, tour: true, pace: 80,
      files: null, planBrief: true, event: 'event', feedbackHint: null, improveSwap: false, courseLink: false, look: true, progress: false, briefCard: false, insideFile: false,
      kit: {
        steps: [['Session 1', 's7-1-dashboard', true], ['Session 1', 's7-3-quote-check', false], ['Session 1', 's7-1b-ask-data', false],
          ['Session 2', 's7-4-extract', true], ['Session 2', 's7-4b-run-ten', false], ['Session 2', 's7-4c-show-broken', false],
          ['Session 2', 's8-1-verbatim', true], ['Session 2', 's8-5-wiki', true]],
        data: ['uhri', 'gc', 'pdf_text', 'pdf_ten', 'wiki', 'library'],
      },
    },
    venice: {
      sessions: ['V1', 'V2', 'V3'], promptKey: 'venice', storeId: 'venice', roomId: 'venice', models: ['glm-eu', 'claude'], country: true,
      advanced: false, wallWithoutAdvanced: true, ignoreLevel: true, ownSession: 'V3', askDirect: true, tour: true, pace: 20,
      files: 'session', planBrief: false, event: 'event_venice', feedbackHint: 'e.g. I pasted a quotation into Check and nothing happened',
      improveSwap: true, courseLink: true, look: true, progress: false, briefCard: false, insideFile: false,
      kit: {
        steps: [['Session 1', 's8-1-verbatim', true], ['Session 1', 's8-1b-gc-quote-check', false],
          ['Session 2', 's8-3-voting', true], ['Session 2', 's8-3c-alignment', false],
          ['Session 3', 's7-1-dashboard', true], ['Session 3', 's7-1b-ask-data', false]],
        data: ['uhri', 'gc', 'hrc'],
      },
    },
    geneva: {
      sessions: ['G1'], promptKey: 'geneva', storeId: 'g1', roomId: 'geneva', models: ['claude', 'glm-eu'], country: false,
      advanced: false, wallWithoutAdvanced: true, ignoreLevel: true, ownSession: null, askDirect: false, tour: true, pace: 25,
      files: ['gc'], planBrief: false, event: 'event_geneva', feedbackHint: null, improveSwap: false, courseLink: false, look: false, progress: true, briefCard: true, insideFile: true,
      keepModel: true, ideas: true, signWall: true, dataFirst: true, highlights: true, cheatsheet: true,
      backup: true,   // the backup plan: recorded mode covers the whole session (see 'Recorded mode in Geneva')
      defaultModel: 'claude',   // Venice: no error in Claude's 136 builds, GLM's in about one of three; GLM stays a click away
      kit: { steps: [['Session 1', 'g1-verbatim', true], ['At home', 'g-home-hrc', true]], data: ['gc', 'hrc_all'] },
    },
    // Forum Podatkowe UAM, Poznań, 19 November 2026 (?course=poznan): one live build on the GAAR Council's resolutions, in
    // Polish, on Claude. The two data files go onto the shelf by themselves and are attached, the request waits in the chat
    // box for the room's wish, and the seat is the event's own (no code to type; the server switches it off at 11:35).
    poznan: {
      sessions: ['P1'], promptKey: 'poznan', storeId: 'poznan', roomId: 'poznan', models: ['claude'], country: false,
      advanced: false, wallWithoutAdvanced: true, ignoreLevel: true, ownSession: 'P1', askDirect: false, tour: false, pace: 20,
      files: [], planBrief: false, event: 'event_poznan', feedbackHint: null, improveSwap: false, courseLink: false, look: false, progress: false, briefCard: false, insideFile: false,
      keepModel: true, defaultModel: 'claude', seat: 'KM7KD4', phones: true,
      preload: [['data/poznan/uchwaly.json', 'uchwaly.json'], ['data/poznan/punkty.json', 'punkty.json']],
      request: 'Zbuduj aplikację „Opinie Rady PUO”: przegląd i wyszukiwarkę uchwał Rady do Spraw Przeciwdziałania Unikaniu Opodatkowania (2019–2026). Cały interfejs po polsku.\n\nDane: dwa dołączone pliki. uchwaly.json to 74 uchwały (id, nr, date, outcome, scheme_type_name, tax, taxpayer_type, pdf_url…), punkty.json to 5613 fragmentów ich tekstu (doc_id wskazuje uchwałę; text, page).\n\nCo ma umieć:\n- domyślnie wyszukiwarka pokazuje punkty (fragmenty z punkty.json), nie uchwały: każdy wynik to jeden punkt z podświetlonym trafieniem, stroną i numerem uchwały, z której pochodzi; nad listą liczba trafień;\n- filtry: rok, rozstrzygnięcie (outcome), podatek; filtrują punkty według ich uchwały;\n- kliknięcie punktu otwiera kartę jego uchwały: numer, data, rozstrzygnięcie, schemat, link do PDF na gov.pl.\n\nZasady: pokazuj tylko to, co jest w danych; niczego nie oceniaj i nie streszczaj.\n\nŻyczenie z sali: ',
      kit: { steps: [], data: [] },
    },
  };
  let CFG = COURSE.full;   // set again at boot, once the course is known
  // a request's session in this course (the course's field of prompts.json)
  const sessionOf = (p) => p[CFG.promptKey];
  // the participant's own files: Advanced, or the one session built on one's own idea
  const ownAllowed = () => S.advanced || (!!CFG.ownSession && S.session === CFG.ownSession);
  const modelAllowed = (id) => !CFG.models || CFG.models.includes(id);
  // the files a session works on, as a Set, or null for the course's usual shelf
  const sessionFiles = () => !CFG.files ? null : Array.isArray(CFG.files) ? new Set(CFG.files)
    : new Set([...S.prompts.filter((p) => sessionOf(p) === S.session && p.dataset).flatMap((p) => [p.dataset, ...(fileMeta(p.dataset).also || [])]),
      ...S.config.files.filter((f) => (f.venice || []).includes(S.session)).map((f) => f.key)]);
  // the country picker: in a session whose requests read the recommendations, or for an app on the stage that reads them
  const countryUsed = () => CFG.country && (S.prompts.some((p) => sessionOf(p) === S.session && p.dataset === 'uhri' &&
      (S.advanced || p.level !== 'advanced' || CFG.ignoreLevel)) ||
    (!!currentVersion() && chainOf(currentVersion()).some((x) => (x.files || []).includes('uhri'))));

  // Activity, to calibrate the studio before the workshop (server/app.py, POST /studio-api/events): what was done,
  // how long it took and what failed, as ids and codes; never a message, a file, an app or a value from the data.
  // Sent to the studio's server every 20 s and when the page is hidden; not from a test page (?via=, localhost
  // without ?api=), and never with ?notrack=1, which is remembered.
  const Track = {
    q: [], t0: performance.now(),
    sid: (() => { try { return crypto.getRandomValues(new Uint32Array(2)).reduce((s, n) => s + n.toString(16).padStart(8, '0'), ''); } catch (e) { return 'ffffffff'; } })(),
    off: params.has('notrack') || localGet('ws:notrack') === '1' || params.has('via') ||
      (/^(localhost|127\.0\.0\.1)$/.test(location.hostname) && !params.has('api')),
    base() {
      const vm = S.config && S.config.routes.find((r) => r.id === 'vm');
      return params.get('api') || (vm && vm.base);
    },
    add(t, f = {}) {
      if (this.off) return;
      this.q.push(Object.assign({ t, ms: Math.round(performance.now() - this.t0) }, f));
      if (this.q.length >= 50) this.flush();
    },
    flush(leaving) {
      const base = this.base();
      if (this.off || !this.q.length || !base) return;
      const body = JSON.stringify({ seat: S.seatCode, sid: this.sid, v: (document.querySelector('script[src^="studio.js"]') || { src: '' }).src.split('v=')[1] || '', events: this.q.splice(0, 100) });
      if (leaving && navigator.sendBeacon) navigator.sendBeacon(base + '/events', new Blob([body], { type: 'text/plain' }));
      else fetch(base + '/events', { method: 'POST', body, keepalive: true, headers: { 'Content-Type': 'text/plain' } }).catch(() => {});
    },
  };
  const track = (t, f) => Track.add(t, f);
  if (params.has('notrack')) localSet('ws:notrack', '1');
  setInterval(() => Track.flush(), 20000);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') Track.flush(true); });
  const FIX = 'The app shows this error:';

  /* ---------- loading ---------- */

  // Geneva's recordings and planning pack, kept in memory after boot (preloadRecorded): an open tab that loses the network still plays them
  const PRELOADED = new Map();
  async function getText(url) {
    if (PRELOADED.has(url)) return PRELOADED.get(url);
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
    // the course (?course=, remembered): venice, geneva (one session) or full (two sessions; also ?course=geneva-full).
    // ws:course2 is a new key on purpose: the old ws:course held 'geneva' for the two-session path, which now means G1.
    const asked = params.get('course');
    S.course = asked ? ({ venice: 'venice', geneva: 'geneva', full: 'full', 'geneva-full': 'full', poznan: 'poznan' }[asked] || 'full')
      : (COURSE[localGet('ws:course2')] ? localGet('ws:course2') : 'full');
    localSet('ws:course2', S.course);
    CFG = COURSE[S.course];
    document.body.dataset.course = S.course;
    document.body.classList.toggle('venice', CFG === COURSE.venice);   // the stylesheet's hook
    $('courseLink').hidden = !CFG.courseLink;
    const event = config[CFG.event] || config.event;
    $('event').textContent = event;
    $('brand').title = event;
    if (CFG.feedbackHint) $('feedbackText').placeholder = CFG.feedbackHint;
    $('lookBtn').closest('.menu').hidden = !CFG.look;
    $('progress').hidden = !CFG.progress;
    document.body.classList.toggle('with-progress', CFG.progress);
    const list = CFG.sessions;
    $('sessionSwitch').hidden = list.length < 2;
    $('sessionSwitch').innerHTML = list.map((s, i) => `<button type="button" role="tab" data-session="${s}" aria-label="Session ${i + 1}">` +
      `<span class="sl">Session </span><span class="ss">S</span>${i + 1}</button>`).join('');
    const stage = (params.get('stage') || '').toUpperCase();
    const wanted = list.find((s) => s === stage || s === 'S' + stage.replace(/^S/, '') || s === 'V' + stage.replace(/^V/, '') || s === 'G' + stage.replace(/^G/, ''));
    S.session = wanted || (list.includes(localGet('ws:session')) ? localGet('ws:session') : list[0]);
    renderSession();

    const code = (hash.get('s') || CFG.seat || localGet('ws:seat') || '').toUpperCase();
    S.seatCode = code || null;
    if (hash.has('s') || hash.has('k')) history.replaceState(null, '', location.pathname + location.search);

    const savedModel = localGet('ws:model');
    const courseDefault = CFG.defaultModel || config.default_model;
    S.model = savedModel && modelAllowed(savedModel) ? savedModel : modelAllowed(courseDefault) ? courseDefault : CFG.models[0];
    renderModelMenu();
    // where the course picks the requests there is no Advanced
    setAdvanced(CFG.advanced && (params.get('advanced') === '1' || (params.get('advanced') !== '0' && localGet('ws:advanced') === '1')));

    setRoute(await pickRoute());
    if (S.route.type === 'server') await ensureSeat();
    // a country the participant picked wins over the seat's, which wins over the default
    renderCountryMenu();
    setCountry(CFG.country ? params.get('country') || localGet('ws:country') || (S.seat && S.seat.country) || config.default_country : config.default_country);

    (await OwnFiles.load()).forEach((e) => { S.own[e.key] = e; });   // before restore(): an app may read one
    const fresh = params.has('reset');
    if (fresh) {   // ?reset=1: a clean start in this browser, for a facilitator's laptop or a second run
      clearWork();
      history.replaceState(null, '', location.pathname + location.search.replace(/[?&]reset(=[^&]*)?/, '').replace(/^&/, '?') + location.hash);
    }
    restore();
    S.ready = true;
    $('sendBtn').disabled = false;
    renderFooter();
    renderAll();
    if (S.savedPlan) resumePlan(S.savedPlan);
    if (CFG.preload) await preloadCourseFiles();
    if (CFG.phones) phonesButtons();
    track('open', { route: S.route.type, session: S.session, model: S.model, has_seat: !!S.seatCode, apps: S.versions.length,
      w: innerWidth, ua: /Firefox/.test(navigator.userAgent) ? 'firefox' : /Edg\//.test(navigator.userAgent) ? 'edge' : /Chrome/.test(navigator.userAgent) ? 'chrome' : /Safari/.test(navigator.userAgent) ? 'safari' : 'other' });
    Room.start();
    if (CFG.backup) {
      if (S.route.type === 'replay' && !params.get('via') && S.recBy == null) { S.recBy = 'auto'; S.watchBase = S.watchBase || Track.base(); }   // no server answered at boot: told when one does
      badgeButton(); Watch.start(); preloadRecorded();
    }
    if (params.get('from')) await fromGallery(params.get('from'));
    else if (CFG.tour) Tour.startOnce();   // the first visit in this browser
    if (!S.versions.length && !S.talk.length) {
      if (CFG.briefCard && CFG.dataFirst) {
        if (!S.savedPlan) note('Hello! Start with the data: look inside the file below. Then write your prompt and send it. The planner looks at the data too and writes a plan; you read it, change it if you like, and build from it.');
        if (DataCard.el && DataCard.el.isConnected) $('log').append(DataCard.el);   // the card under the greeting
      } else if (CFG.briefCard) { if (!S.savedPlan) note('Hello! Write your prompt in the card below, then send it. The planner will look at your data and write a plan; you read it, change it if you like, and build from it.'); }
      else note(`Hello! Ask me anything, or pick a suggestion below. To build an app, first drag a file from <b>Your files</b> into the chat` +
        (countryUsed() ? `: your country is <b>${esc(S.country)}</b>, with ${fmt(S.countryCount)} UN recommendations and observations.` : '.'));
    }
  }

  // A back-up for when a plan or a build fails: a gallery app comes in as a version of its own, with the plan
  // it was built from as the request, so the next message asks the model to change it. ?from=<model>/<prompt id>
  async function fromGallery(id) {
    history.replaceState(null, '', location.pathname + location.search.replace(/[?&]from=[^&]*/, '').replace(/^&/, '?'));
    const [model, promptId] = id.split('/');
    track('gallery_in', { model, prompt: promptId });
    try {
      if (!/^[\w-]+\/[\w-]+$/.test(id)) throw new Error('not a gallery app');
      const g = await getJSON('gallery/gallery.json');
      const r = g.results.find((x) => x.model === model && x.prompt === promptId && x.app);
      const p = S.prompts.find((q) => q.id === promptId);
      if (!r || !p) throw new Error('not in the gallery');
      const html = await getText(`gallery/apps/${model}/${promptId}.html`);
      const name = (g.models[model] || {}).name || model;
      const to = sessionOf(p) || S.session;   // a request this course does not have stays where the participant is
      if (to !== S.session) loadSession(to);
      const v = {
        n: S.versions.length + 1, parent: null, user: `From the gallery: ${p.title}`, files: p.dataset ? [p.dataset] : [],
        sent: g.prompts.find((x) => x.id === promptId).prompt, model, label: `${name} · from the gallery`, seconds: null, cost: null,
        recorded: true, promptId, created: Date.now(), html, reply: '```html\n' + html + '\n```', fix: false,
        summary: `${p.title}, built by ${name} from the plan above. It was loaded from the gallery: ask for a change in your own words, or pick a next step below.`,
      };
      S.versions.push(v);
      S.current = v.n;
      save();
      renderAll();
      await showVersion(v);
    } catch (e) {
      note('That app could not be loaded from the gallery. Open the gallery and try again.');
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
    if (S.route && S.route.id !== r.id) track('route', { from: S.route.id, to: r.id });
    S.route = r;
    if (r.type === 'server') S.watchBase = r.base;   // where the facilitator's switch is watched, also while the route is the recordings
    if (r.type !== 'replay') S.recBy = null;
    const b = $('routeBadge');
    b.textContent = r.type === 'replay' ? 'Recorded answers' : 'Live model';
    b.className = 'route ' + (r.type === 'replay' ? 'warn' : 'ok') + (CFG.backup ? ' pick' : '');
    b.title = r.label + (why ? '. ' + why : '') + (CFG.backup ? ' (click to change)' : '');
    renderTools();
    if (CFG.backup && S.ready) { renderSuggest(); renderPlanTools(); }
    if (why) note(esc(why));
  }

  /* ---------- Recorded mode in Geneva: the backup plan ---------- */

  // When the model or the server fails, a participant (the badge, an error box) or the facilitator (the admin page) switches to the
  // answers recorded beforehand with Claude Sonnet 5.5: the first app for each look, three ideas, and an improvement for each.
  // The work so far stays; setRoute is all that changes. S.recBy says who switched: 'you', 'facilitator' or 'paused'.
  const replayRoute = () => S.config.routes.find((r) => r.type === 'replay');
  const recordedNow = () => !!CFG.backup && !!S.route && S.route.type === 'replay';
  const RECORDED_NOTE = 'Recorded mode builds the app recorded beforehand from the recommended answers, on the topic the rights of the child. Changes to the plan need a live model.';
  const NEEDS_LIVE = 'This needs a live model, and in recorded mode no model is connected. Use the badge at the top (Back to the live model) when it is back.';

  function useRecorded(why, by = 'you') {
    S.recBy = by;
    S.backNoted = false;
    setRoute(replayRoute(), why);
  }

  async function backToLive() {
    if (!CFG.backup || S.route.type !== 'replay') return false;
    if (S.busy) { note('Wait until the studio has finished, then press <b>Back to the live model</b> again.'); return false; }
    S.routesDown.clear();
    const r = await pickRoute();
    if (r.type === 'replay') {
      note(S.recBy === 'facilitator' ? 'The facilitator still has recorded answers on for everyone, so the live model is not available yet. You are on recorded answers; your work stays.'
        : S.recBy === 'paused' ? 'The studio is still paused by the facilitator. You are on recorded answers; your work stays.'
          : 'The live model cannot be reached right now. You are on recorded answers; try again in a minute. Your work stays.');
      return false;
    }
    setRoute(r);
    if (r.type === 'server') await ensureSeat();   // the live model needs the seat code
    if (S.route.type === 'replay') return false;   // no code typed: the dialog's "Continue without a model" put the recordings back
    track('backup', { to: 'live' });
    note('Back on the live model. Your work stays.');
    return true;
  }

  // the badge's popover
  const RoutePop = {
    el: null,
    close() { if (this.el) { this.el.remove(); this.el = null; $('routeBadge').setAttribute('aria-expanded', 'false'); } },
    toggle() {
      if (this.el) return this.close();
      const recorded = S.route.type === 'replay', d = this.el = document.createElement('div');
      d.id = 'routePop';
      d.className = 'route-pop';
      d.setAttribute('role', 'dialog');
      d.setAttribute('aria-label', 'Recorded answers');
      d.innerHTML = recorded
        ? '<b>Recorded answers</b><p>The apps, ideas and improvements were recorded beforehand with Claude Sonnet 5.5. Nothing is sent to a model. Your work so far stays.</p>' +
          '<button type="button" class="primary" data-a="live">Back to the live model</button>'
        : '<b>Live model</b><p>The apps, ideas and improvements were recorded beforehand with Claude Sonnet 5.5. Nothing is sent to a model. Your work so far stays.</p>' +
          '<button type="button" class="primary" data-a="rec">Switch to recorded answers</button>';
      d.onclick = async (e) => {
        const b = e.target.closest('button');
        if (!b) return;
        this.close();
        if (b.dataset.a === 'rec') {
          track('backup', { to: 'recorded', by: 'badge' });
          useRecorded('Switched to recorded answers. Your work stays; what you do now plays what was recorded beforehand.');
        } else await backToLive();
      };
      const badge = $('routeBadge');
      badge.setAttribute('aria-expanded', 'true');
      document.body.append(d);
      const r = badge.getBoundingClientRect();
      d.style.top = Math.round(r.bottom + 8) + 'px';
      d.style.right = Math.max(8, Math.round(innerWidth - r.right)) + 'px';
      d.querySelector('button').focus();
    },
  };

  // the badge becomes a button: a click opens the popover; a click elsewhere or Escape closes it
  function badgeButton() {
    const b = $('routeBadge');
    b.setAttribute('role', 'button');
    b.setAttribute('tabindex', '0');
    b.setAttribute('aria-haspopup', 'dialog');
    b.setAttribute('aria-expanded', 'false');
    b.onclick = () => RoutePop.toggle();
    b.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); RoutePop.toggle(); } };
    document.addEventListener('click', (e) => { if (RoutePop.el && !RoutePop.el.contains(e.target) && !b.contains(e.target)) RoutePop.close(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && RoutePop.el) { RoutePop.close(); b.focus(); } });
  }

  // an error box about the model or the server gets "Continue with recorded answers": it switches the route, takes the failed turn
  // away (`gone`) and plays the same step again from the recordings (`resend`). `row` is the box's button row when it has one.
  function backupButton(box, gone, resend, row) {
    if (!row) {
      row = document.createElement('div');
      row.className = 'choice';
      box.append(row);
    }
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'ghost';
    b.dataset.c = 'recorded';
    b.textContent = 'Continue with recorded answers';
    b.onclick = () => {
      if (S.busy) return;
      track('backup', { to: 'recorded', by: 'error' });
      useRecorded('The model did not answer, so the studio switched to recorded answers. Your work stays.');
      gone.forEach((el) => el.remove());
      resend();
    };
    row.append(b);
    scrollLog();
  }
  // which errors get it: the model busy or failed, no connection, any 503 (paused, recorded_mode)
  const backupFor = (e) => !!CFG.backup && e.name !== 'AbortError' && (TROUBLE.has(e.code) || e.failover === true || e.status === 503);

  // the facilitator's switch and the server's health, every 20 s while there is a server to ask (?healthpoll=<seconds> in a test)
  const Watch = {
    fails: 0, offered: false, timer: 0,
    start() {
      if (!CFG.backup || this.timer) return;
      const every = Math.max(0.2, Number(params.get('healthpoll')) || 20) * 1000;
      this.timer = setInterval(() => { if (!document.hidden) this.poll(); }, every);
      document.addEventListener('visibilitychange', () => { if (!document.hidden) this.poll(); });
    },
    async poll() {
      // while on a server route; and on the recordings the facilitator or a pause put there: that server tells when to go back
      const watching = S.route && (S.route.type === 'server' || (S.route.type === 'replay' && (S.recBy === 'facilitator' || S.recBy === 'paused' || S.recBy === 'auto')));
      if (!watching || !S.watchBase || this.busy) return;
      this.busy = true;
      let j = null;
      const c = new AbortController(), t = setTimeout(() => c.abort(), 3000);
      try {
        const res = await fetch(S.watchBase + '/health', { signal: c.signal, cache: 'no-store' });
        if (res.ok) j = await res.json();
      } catch (e) { /* counted below */ } finally { clearTimeout(t); this.busy = false; }
      if (!j) return this.failed();
      this.fails = 0;
      this.offered = false;
      const recorded = j.mode === 'recorded', paused = !recorded && j.accepting === false;
      if ((recorded || paused) && S.route.type === 'server') {
        track('backup', { to: 'recorded', by: recorded ? 'facilitator' : 'paused' });
        useRecorded(recorded ? 'The facilitator has switched the studio to recorded answers. Your work stays; what you do now plays what was recorded beforehand.'
          : 'The studio is paused by the facilitator, so it switched to recorded answers. Your work stays; what you do now plays what was recorded beforehand.', recorded ? 'facilitator' : 'paused');
      } else if (!recorded && !paused && S.route.type === 'replay' && !S.backNoted) {
        S.backNoted = true;
        const n = note('The live model is back. You are still on recorded answers; switch when it suits you. Your work stays. ');
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'ghost';
        b.textContent = 'Back to the live model';
        b.onclick = async () => { if (await backToLive()) n.remove(); };
        n.append(b);
        scrollLog();
      scrollLog();
      }
    },
    failed() {
      this.fails++;
      if (this.fails < 2 || this.offered || S.route.type !== 'server') return;
      this.offered = true;   // once per outage; a Wi-Fi glitch must not switch anything by itself
      const n = note('The studio cannot reach its server. If it stays like this, you can carry on with recorded answers. Your work stays. ');
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'ghost';
      b.textContent = 'Continue with recorded answers';
      b.onclick = () => { if (S.route.type !== 'server') return; track('backup', { to: 'recorded', by: 'poll' }); useRecorded('Switched to recorded answers. Your work stays.', 'you'); n.remove(); };
      n.append(b);
      scrollLog();
    },
  };

  // after boot, every recording and the planning pack go into memory: a tab that loses the network still plays them
  async function preloadRecorded() {
    const dir = S.config.replay.dir, plan = 'data/planning/g1-verbatim.json';
    const grab = async (url) => { try { const r = await fetch(url, { cache: 'no-cache' }); if (r.ok) PRELOADED.set(url, await r.text()); } catch (e) { /* played from the network if it is still there */ } };
    await grab(plan);
    let looks = [];
    try { looks = JSON.parse(PRELOADED.get(plan) || '{}').looks || []; } catch (e) { /* no looks, no preload of them */ }
    const names = ['g1-verbatim.md', 'g1-improve.md', ...looks.map((l) => `g1-verbatim.${l.id}.md`),
      ...[1, 2, 3].flatMap((n) => looks.map((l) => `g1-improve-${n}.${l.id}.md`))];
    // the shelf the build looks at, and the data the app runs on (the data card has the parsed copy already)
    await Promise.all([...names.map((n) => grab(dir + n)), grab('data/shelf.json'), ...CFG.files.map((k) => dataText(k).catch(() => {})), ...CFG.files.map((k) => dataParsed(k).catch(() => {}))]);
    document.body.dataset.recorded = 'ready';
  }

  async function ensureSeat() {
    let typed = false;   // the code came from the dialog, not from the link or from an earlier visit
    for (;;) {
      let err = '';
      if (S.seatCode) {
        try {
          const res = await fetch(S.route.base + '/seat/' + encodeURIComponent(S.seatCode));
          if (res.ok) {
            S.seat = await res.json();
            setBudget(S.seat.budget_left);
            localSet('ws:seat', S.seatCode);
            track('seat_ok', { typed });
            return;
          }
          err = 'That code was not recognised. Check your card: six letters and digits, no O, I, L, 0 or 1.';
          track('seat_wrong', { typed, status: res.status, len: S.seatCode.length });
          S.seatCode = null;   // a wrong code is not kept for the next visit
          try { localStorage.removeItem('ws:seat'); } catch (e) { /* private mode */ }
        } catch (e) {
          err = 'The studio could not reach its server to check the code. Check the Wi‑Fi, then press Start again.';
        }
      }
      const answer = await askSeat(err);
      typed = true;
      if (answer === null) {
        S.seatCode = null;
        track('seat_skip', {});
        setRoute(S.config.routes.find((r) => r.type === 'replay'), 'No seat code: the studio replays recorded answers instead of calling a model.');
        return;
      }
      S.seatCode = answer;
    }
  }

  function askSeat(err) {
    return new Promise((resolve) => {
      const d = $('seatDialog');
      $('seatErr').hidden = !err;
      $('seatErr').textContent = err;
      $('seatInput').value = '';
      // only the "Continue without a model" button leads to recorded answers: Escape keeps the dialog, and so does
      // Start (or Enter) on an empty field
      d.oncancel = (e) => e.preventDefault();
      $('seatForm').onsubmit = (e) => {
        if (e.submitter !== $('seatSkip') && !$('seatInput').value.trim()) { e.preventDefault(); $('seatInput').focus(); }
      };
      d.onclose = () => {
        const typed = $('seatInput').value.trim().toUpperCase();
        if (d.returnValue === 'skip') return resolve(null);
        if (d.returnValue === 'ok' && typed) return resolve(typed);
        d.returnValue = '';
        d.showModal();   // closed some other way (a second Escape in Chrome): ask again
        $('seatInput').focus();
      };
      d.returnValue = '';
      d.showModal();
      $('seatInput').focus();
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
        if (CFG.backup && next.type === 'replay') throw e;   // Geneva: the recordings are the participant's choice (the error box offers them), not a silent switch
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
        body: JSON.stringify({ seat: S.seatCode, model: o.model, purpose: o.purpose, messages: o.messages, ...(CFG.keepModel ? { fallback: false } : {}) }),
        signal: o.signal,
      });
    } catch (e) {
      if (e.name === 'AbortError') throw e;
      throw Object.assign(new Error('no connection'), { failover: true });
    }
    if (!res.ok) {
      let j = {};
      try { j = await res.json(); } catch (e) { /* not JSON */ }
      throw Object.assign(new Error(j.error || `server error ${res.status}`), { status: res.status, code: j.code,
        failover: res.status >= 500 && res.status !== 503 && j.code !== 'model_failed' });   // model_failed: the participant chooses, not a silent switch of route
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
          messages: (sys ? [{ role: 'system', content: sys }] : []).concat(o.messages.map((x) => (x.images ? { role: x.role, content: [{ type: 'text', text: x.content },
            ...x.images.map((i) => ({ type: 'image_url', image_url: { url: `data:${i.media_type};base64,${i.data}` } }))] } : x))),
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

  // o.replay: the recording to play by its file name (Geneva: the app for a look, the ideas, an improvement), or a list of names of
  // which the first that exists is played; without it the recording is the request's own, by o.promptId
  async function replayChat(o) {
    if (o.purpose !== 'build') {
      throw Object.assign(new Error('No model is connected (recorded mode), so this needs a live model.'), { failover: false });
    }
    const id = o.promptId || (o.replay ? '' : nextPromptId());
    // recorded for Kenya; the apps read the country from the data, the words around them do not
    const local = (s) => (S.country === 'Kenya' ? s : s.replace(/Kenya/g, S.country));
    // the workshop apps are recorded from the current plans; the extras only in the fallback recording
    let rec = S.config.replay, text = '';
    if (o.replay) {
      for (const name of [].concat(o.replay)) {
        text = await getText(rec.dir + name).catch(() => '');
        if (text) break;
      }
      if (!text) throw Object.assign(new Error('That recording is not available. It needs a live model.'), { failover: false });
    } else try {
      text = local(await getText(rec.dir + id + '.md'));
    } catch (e) {
      rec = rec.fallback;
      text = rec && local(await getText(rec.dir + id + '.md').catch(() => ''));
      if (!text) throw Object.assign(new Error('Recorded mode can only play back the workshop requests. Pick one of the suggestions.'), { failover: false });
    }
    const thought = o.replay ? '' : local(await getText(rec.dir + id + '.thought.md').catch(() => ''));
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
      if (o.onDelta) o.onDelta(text.slice(0, i + 220));
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

  // Edit mode: a change to an existing app comes back as SEARCH/REPLACE pairs (site/data/system_prompt.md).
  // The same rules as tools/edits.py, which the bake-off uses.
  const EDIT = /<<<<<<< SEARCH\n([\s\S]*?)\n?=======\n([\s\S]*?)\n?>>>>>>> REPLACE/g;
  const WHOLE_FILE = 'Your edits did not match the current code exactly. Reply with the complete updated HTML document in one ```html block instead.';
  function parseEdits(text) {
    return [...text.matchAll(EDIT)].map((m) => ({ search: m[1], replace: m[2] })).filter((e) => e.search.trim());
  }

  // Apply every edit or none: an exact match first, then one that ignores indentation and trailing spaces;
  // a SEARCH that occurs twice is as useless as one that occurs nowhere
  function applyEdits(code, edits) {
    let out = code, lines = 0;
    for (const e of edits) {
      const at = out.indexOf(e.search);
      if (at >= 0 && out.indexOf(e.search, at + 1) < 0) {
        out = out.slice(0, at) + e.replace + out.slice(at + e.search.length);
      } else {
        const L = out.split('\n'), want = e.search.split('\n').map((s) => s.trim());
        const hits = [];
        for (let i = 0; i + want.length <= L.length; i++) {
          if (want.every((w, j) => L[i + j].trim() === w)) hits.push(i);
        }
        if (hits.length !== 1) return { ok: false, failed: e.search.split('\n')[0].trim().slice(0, 80) };
        L.splice(hits[0], want.length, ...e.replace.split('\n'));
        out = L.join('\n');
      }
      lines += e.replace.split('\n').length;
    }
    return { ok: true, html: out, lines };
  }

  function summaryOf(text) {
    const fence = /<\/html>\s*```/i.test(text) ? /```html[\s\S]*?<\/html>\s*```/i : /```html[\s\S]*?(```|$)/;
    const s = text.replace(fence, '').replace(/```edit[\s\S]*?(```\s*$|$)/, '').replace(EDIT, '').replace(/<!doctype html[\s\S]*?(<\/html>|$)/i, '').trim();
    return s.length > 700 ? s.slice(0, 700) + '…' : s;
  }

  const currentVersion = () => (S.current ? S.versions[S.current - 1] : null);

  function chainOf(v, versions = S.versions) {
    const out = [];
    for (let x = v; x; x = x.parent ? versions[x.parent - 1] : null) out.unshift(x);
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

  const fileMeta = (key) => S.config.files.find((f) => f.key === key) || ownMeta(key);
  const fileLabel = (key) => fileMeta(key).label.replace(/\{country\}/g, S.country);
  // what the model gets for a file: its name and where the app finds it, never its contents; for the
  // participant's own file also its fields, and its first records only if they ticked the box
  const attachLine = (key) => S.own[key] ? OwnFiles.describe(S.own[key], fileLabel(key)) :
    `(Attached: ${fileLabel(key)} → WORKSHOP_DATA.${key}` + (fileMeta(key).also || []).map((k) => `, with WORKSHOP_DATA.${k}`).join('') + ')';
  // a file removed from the shelf still has a name in the conversations that used it
  const ownMeta = (key) => {
    const e = S.own[key];
    return { key, kind: e ? e.kind : 'csv', own: true, label: e ? e.name : 'a file you removed', blurb: '' };
  };
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
    box.hidden = !S.draft.size && !S.draftImages.length;
    box.innerHTML = [...S.draft].map((k) => chipHtml(k, true)).join('') + S.draftImages.map((im, i) =>
      `<span class="filechip pic"><img src="${im.url}" alt=""><span>Picture ${im.w}×${im.h}</span>` +
      `<button type="button" data-img="${i}" aria-label="Remove the picture">×</button></span>`).join('');
    box.querySelectorAll('button[data-key]').forEach((b) => { b.onclick = () => { S.draft.delete(b.dataset.key); renderAttach(); renderNeeds(); renderShelfState(); }; });
    box.querySelectorAll('button[data-img]').forEach((b) => { b.onclick = () => { S.draftImages.splice(Number(b.dataset.img), 1); renderAttach(); }; });
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
    if (!S.ready || S.busy || !text.trim() || text.trim() === CHANGE_APP.trim()) return;   // the prefix of "My own idea", with nothing after it
    if (!plan && S.planning && S.planning.changing) {
      if (!commitEdit(S.planning)) return;   // a plan being edited by hand is saved first, so the change starts from it
      return revisePlan(S.planning, text);
    }
    const p = S.prompts.find((q) => q.id === S.pendingPromptId);
    if (p && p.dataset && !new Set([...attachedBefore(), ...S.draft]).has(p.dataset)) {
      note(`This request needs the file <b>${esc(fileLabel(p.dataset))}</b>. Drag it from <b>Your files</b> into the chat, then send.`);
      showFiles(p.dataset);
      return;
    }
    if (!plan && plannable(p) && S.planMode) {
      if (freeBrief(p)) {   // the participant's own brief: any text of some length starts the recorded planning
        const t = text.trim();
        if (t.length < BRIEF_MIN) { note(`A prompt needs a few more words: at least ${BRIEF_MIN} characters, so the planner has something to work from.`); return; }
        if (t.length > BRIEF_MAX) { note(`That prompt is too long: up to ${fmt(BRIEF_MAX)} characters, and it is ${fmt(t.length)}. Shorten it, then send.`); return; }
        startPlanning(p, t, takeDraft());
        return true;
      }
      if (text.trim() !== S.pendingText.trim()) {
        note('Plan mode replays a planning session prepared for this request as it is written. Undo your change, or turn <b>Plan mode</b> off to send your own words to the model.');
        return;
      }
      startPlanning(p, text, takeDraft());
      return true;
    }
    // Geneva's recorded mode: a recorded idea's request plays the improvement recorded for it (g1-improve-<n>.<look>.md); a plan plays the app of its look
    const idea = recordedNow() && !plan && S.ideaOf && S.ideaOf.get(text.trim());
    const look = plan && plan.look ? plan.look : (currentVersion() && currentVersion().look) || '';
    const recOpts = !recordedNow() ? {}
      : plan ? { replay: plan.look ? [`g1-verbatim.${plan.look}.md`, 'g1-verbatim.md'] : undefined }
        : idea ? { replay: `g1-improve-${idea}.${look || 'paper'}.md` } : {};
    if (recordedNow() && !plan && !idea && (!p || text.trim() !== S.pendingText.trim())) {
      note('In recorded mode the studio can only play what was recorded beforehand: the first app, the three ideas and the improvement for each. Anything else needs a live model: use the badge at the top (Back to the live model) when it is back.');
      return;
    }
    if (!CFG.backup && S.route.type === 'replay' && (!p || text.trim() !== S.pendingText.trim())) {
      note('Without a seat code the studio plays back recorded answers, so it can only answer the workshop requests as they are written. ' +
        'Pick a suggestion, or ask a facilitator for a seat code to chat freely.');
      return;
    }
    // a model that cannot read pictures (GLM) hands this one message to one that can, Claude first
    const reader = S.draftImages.length && !S.config.models[S.model].vision ? (S.config.models.claude && S.config.models.claude.vision ? 'claude'
      : Object.keys(S.config.models).find((k) => S.config.models[k].vision)) : null;
    if (reader) note(`This message goes to <b>${esc(S.config.models[reader].label)}</b> (${esc(whereOf(reader))}): <b>${esc(S.config.models[S.model].label)}</b> cannot read pictures. Your next message goes back to ${esc(S.config.models[S.model].label)}.`);
    if (plan) {
      const files = [...new Set([...plan.files, ...S.draft])];
      S.draft.clear();
      if ($('input').value === CHANGE) { $('input').value = ''; fitInput(); }
      build(text, files, { images: takeImages(), model: reader || undefined, ...recOpts, ...(CFG.backup && plan.look ? { look: plan.look } : {}) });
      return true;
    }
    const images = takeImages();
    build(text, takeDraft(), { images, model: reader || undefined, ...recOpts });
    return true;
  }

  function takeImages() {
    const images = S.draftImages;
    S.draftImages = [];
    renderAttach();
    return images;
  }

  // a screenshot, scaled to at most 1568 pixels on its long side (what the models read in full), as PNG, or as
  // JPEG when the PNG would be over 1.2 MB; it goes to the model whole, so the trace says so
  async function imagePart(blob) {
    const bmp = await createImageBitmap(blob);
    const k = Math.min(1, 1568 / Math.max(bmp.width, bmp.height));
    const c = document.createElement('canvas');
    c.width = Math.round(bmp.width * k);
    c.height = Math.round(bmp.height * k);
    c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height);
    let out = await new Promise((r) => c.toBlob(r, 'image/png'));
    if (out.size > 1200000) out = await new Promise((r) => c.toBlob(r, 'image/jpeg', 0.85));
    const url = await new Promise((r) => { const f = new FileReader(); f.onload = () => r(f.result); f.readAsDataURL(out); });
    return { media_type: out.type, data: url.split(',')[1], url, w: c.width, h: c.height, kb: Math.round(out.size / 1024) };
  }

  async function addImages(list) {
    for (const f of [...list]) {
      if (S.draftImages.length >= 3) { note('Up to three pictures can go with one message.'); break; }
      try { S.draftImages.push(await imagePart(f)); track('picture', { kb: S.draftImages[S.draftImages.length - 1].kb }); } catch (e) { note(`The studio could not read the picture "${esc(f.name || 'pasted')}".`); }
    }
    renderAttach();
    if (S.route.type === 'replay') note('Pictures go to a live model, so they need a seat code. Recorded answers cannot see them.');
    else if (S.draftImages.length && !S.config.models[S.model].vision) note(`<b>${esc(S.config.models[S.model].label)}</b> cannot read pictures, so the message with it will go to <b>${esc((S.config.models.claude || {}).label || 'a model that can')}</b>.`);
    $('input').focus();
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
    if (e.code === 'model_busy' || e.code === 'model_failed') return m;   // the choice (Try again, the other model) sits under it
    if (e.status === 503) return (m || 'The model service is busy') + '. Your message is back in the box.';
    return `The model could not finish (${m}). Your message is back in the box: send it again.`;
  }

  async function build(userText, files = [], opts = {}) {
    if (S.busy || !userText.trim()) return;
    const model = opts.model || S.model;   // a message with a picture may go to another model than the menu's
    const parent = S.freshNext ? null : currentVersion();
    const promptId = S.pendingPromptId;
    const plan = S.planning && S.planning.building ? S.planning : null;
    const planned = plan && freeBrief(plan.p) ? plan.history[plan.history.length - 1] : null;   // the version a free brief is built from
    S.freshNext = false;
    S.pendingPromptId = null;
    setBusy(true);
    $('planView').hidden = true;
    await shelfLoad();
    const hits = shelfSearch(userText);
    const asTyped = userText + files.map((k) => '\n\n' + attachLine(k)).join('');
    const sent = asTyped + shelfBlock(hits);
    const messages = buildMessages(parent, sent);
    const images = opts.images || [];   // only this message carries them; later requests send the words alone
    if (images.length) messages[messages.length - 1].images = images.map(({ media_type, data }) => ({ media_type, data }));
    const giveBack = () => {  // after a failure the message and its files go back in the box
      S.draftImages = images;
      if (plan) { plan.building = false; showPlan(plan); return; }   // a plan stays on the stage, ready to build again
      const fresh = !parent && S.versions.length > 0;
      openComposer(userText);
      Object.assign(S, { pendingPromptId: promptId, pendingText: promptId ? userText : '', freshNext: fresh });
      files.forEach((k) => S.draft.add(k));
      renderAttach();
      renderContinuing();
    };
    setView('app');
    addUser(userText, files, images);
    const userEl = $('log').lastElementChild;
    const view = addAssistantLive();
    if (hits.length) view.step(shelfStep(hits));
    const t0 = performance.now();
    let lastSkeleton = 0, sketched = false;
    S.ctrl = new AbortController();
    try {
      let { text, usage } = await chat({
        purpose: 'build', model, messages, promptId, signal: S.ctrl.signal, replay: opts.replay,
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
      let html = extractHtml(text), edit = null, asked = messages;
      // edit mode: a change came back as edits to the app on the stage; if one does not fit, ask once for the whole file
      const edits = !html && parent ? parseEdits(text) : [];
      if (edits.length) {
        const r = applyEdits(parent.html, edits);
        if (r.ok) {
          html = r.html;
          edit = { edits: edits.length, lines: r.lines };
        } else if (usage.recorded) {   // a recorded change was written for the recorded app, not for this one
          view.fail('', 'This recorded change was written for the recorded app, and your app is different, so it does not fit. It needs a live model: use the badge at the top (Back to the live model) when it is back.');
          giveBack();
          return;
        } else {
          addTrace({ purpose: 'build', usage, messages, userText: asTyped, parent, files, shelf: hits, images, planned });
          view.retry(`The changes did not fit your app's code (at "${r.failed}"). Asking the model for the whole app instead; this takes longer.`);
          asked = [...messages.map(({ images: _, ...m }) => m), { role: 'assistant', content: text }, { role: 'user', content: WHOLE_FILE }];
          const again = await chat({ purpose: 'build', model, messages: asked, promptId, signal: S.ctrl.signal,
            onThought: (all) => view.think(all), onDelta: (all) => view.update(all) });
          usage = { ...again.usage, cost: (usage.cost || 0) + (again.usage.cost || 0), seconds: (usage.seconds || 0) + (again.usage.seconds || 0) };
          text = again.text;
          html = extractHtml(text);
        }
      }
      if (usage.model_label) view.who(usage.model_label);
      const seconds = usage.seconds || (performance.now() - t0) / 1000;
      addTrace({ purpose: 'build', usage, messages: asked, userText: asTyped, parent, files, shelf: hits, images: asked === messages ? images : [], planned });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      // what the activity record keeps of a build: never its words or code
      const buildFacts = (kind) => ({ kind, prompt: promptId, model: usage.model || model, asked: model, fell: usage.fallback_from || null,
        s: Math.round(seconds), cost: usage.cost != null ? Number(usage.cost) : null, rec: !!usage.recorded, plan: !!plan,
        files: files.length, own: files.filter((k) => S.own[k]).length, images: images.length, parent: parent ? parent.n : null });
      const base = { user: userText, sent, files, model: usage.model || model, label: usage.model_label || S.config.models[model].label,
        seconds, cost: usage.cost, recorded: !!usage.recorded, promptId, created: Date.now(), ...view.thinking(),
        ...(CFG.backup && (opts.look || (parent && parent.look)) ? { look: opts.look || parent.look } : {}),   // which look's recorded app an improvement is played for
        ...(hits.length ? { shelf: hits.map((h) => h.page.id) } : {}) };
      if (!html) {
        if (!text.trim()) {
          track('build_fail', { prompt: promptId, model: base.model, code: 'empty' });
          view.fail('', 'The model sent back nothing. Your message is back in the box: send it again.');
          giveBack();
          return;
        }
        // a question about the data came back as a query: the browser runs it on all the data, the model never sees the result
        if (extractQuery(text)) {
          track('build', buildFacts('query'));
          const t = Object.assign(base, { reply: text.trim(), after: S.current, query: true });
          S.talk.push(t);
          if (S.trace.length) S.trace[S.trace.length - 1].kept.unshift('The result of the query: your browser computed it on all the data; the model wrote the code and never saw the numbers.');
          view.answer(t);
          const p = S.prompts.find((q) => q.id === promptId);
          if (p && p.lesson) view.lesson(p.lesson);
          save();
          if (plan) plan.building = false;
          if (sketched && S.current) await showVersion(currentVersion());
          return;
        }
        // a workshop app that came back as one sentence: the model stopped before the code (Mistral, now and then)
        if (promptId && text.trim().length < 600) {
          track('build_fail', { prompt: promptId, model: base.model, code: 'no_code' });
          view.fail('', 'The model stopped before writing the code; it happens now and then. Your request is back in the box: send it again.');
          giveBack();
          return;
        }
        // an answer in words: part of the conversation, not a new version of the app
        track('build', buildFacts('talk'));
        const t = Object.assign(base, { reply: text.trim(), after: S.current });
        S.talk.push(t);
        view.answer(t);
        save();
        if (plan) plan.building = false;
        if (sketched && S.current) await showVersion(currentVersion());   // a half-written app gives way to the real one
        return;
      }
      // an edited version keeps its whole code in the reply: the next request shows the model the app as it is now
      const v = Object.assign(base, {
        n: S.versions.length + 1, parent: parent ? parent.n : null,
        reply: edit ? summaryOf(text) + '\n\n```html\n' + html + '\n```' : text,
        summary: summaryOf(text), html, fix: userText.startsWith(FIX), ...(edit ? { edit } : {}), ...(opts.auto ? { auto: true } : {}),
      });
      S.versions.push(v);
      S.current = v.n;
      // steps 5 and 7, once its preview is up; first: the first Verbatim finder, which brings the test card
      S.watch = { n: v.n, err: false, improves: !!parent && !v.fix && !opts.auto, first: promptId === 'g1-verbatim' && !S.versions.slice(0, -1).some((x) => x.promptId === 'g1-verbatim') };
      track('build', Object.assign(buildFacts('app'), { ver: v.n, lines: html.split('\n').length, edit: !!edit, whole: asked !== messages, auto: !!opts.auto }));
      if (plan) retirePlanning(`Built as v${v.n}.`);
      view.done(v);
      const p = S.prompts.find((q) => q.id === promptId);
      if (p && p.lesson) view.lesson(p.lesson);
      save();
      renderVersions();
      // automatic repair: an error in the first seconds of a new live version is sent back to the model once, as an
      // edit (a few seconds); a version that is itself a repair, or a recorded answer, is never repaired again
      S.autoFix = S.route.type !== 'replay' && !opts.auto ? { n: v.n, t: performance.now() } : null;
      await showVersion(v);
    } catch (e) {
      track('build_fail', { prompt: promptId, model, code: e.name === 'AbortError' ? 'stopped' : String(e.code || e.status || (e.failover ? 'no_route' : 'error')) });
      const box = view.fail('', friendly(e));
      giveBack();
      const again = () => (plan ? buildFromPlan(plan) : submitBuild(userText));
      if (CFG.keepModel && TROUBLE.has(e.code)) modelChoice(box, [userEl, box.parentElement], again);
      else if (backupFor(e)) backupButton(box, [userEl, box.parentElement], again);
    } finally {
      setBusy(false);
      if (S.pendingRepair) { const m = S.pendingRepair; S.pendingRepair = null; autoRepair(m); }
    }
  }

  const REPAIR_WINDOW_MS = 8000;   // an app that fails on load fails in the first seconds; later errors come from a click
  function autoRepair(m) {
    track('repair', { ver: S.current });
    note(`The app showed an error as it opened (<i>${esc(String(m.message || '').slice(0, 120))}</i>). The studio sends it back to the model to fix, once; the fix usually takes a few seconds.`);
    build(`${FIX} "${m.message}"${m.line ? ' at line ' + m.line : ''}. Please fix it and keep everything else the same.`, [], { auto: true });
  }

  function setBusy(on) {
    S.busy = on;
    $('sendBtn').disabled = on;
    $('stopBtn').hidden = !on;
    $('building').hidden = !on;
    $('empty').hidden = on || S.versions.length > 0;   // the shelf, until there is an app
    renderSuggest();   // nothing to choose while the model works
    renderTools();
    renderPlanTools();   // nor a plan to change
  }

  /* ---------- questions about the data: a query the browser runs ---------- */

  // the model answers a question about the data with the body of a function (system_prompt.md, "Questions about
  // the data"); it runs here, on all the data, in a frame with no network, like an app, and only the table is shown
  const QUERY = /```query[ \t]*\n([\s\S]*?)```/;
  const extractQuery = (text) => { const m = QUERY.exec(text || ''); return m ? m[1].trim() : ''; };
  const withoutQuery = (text) => text.replace(QUERY, '').trim();
  const QUERY_TIMEOUT_MS = 15000;

  async function runQuery(code, files) {
    const id = 'q' + Math.random().toString(36).slice(2);
    const known = (k) => k === 'uhri' || (S.index.datasets[k]) || k.startsWith('own_');
    const parts = await Promise.all(files.filter(known).map(async (k) => JSON.stringify(k) + ':' + (await dataText(k))));
    const post = `parent.postMessage({ type: 'studio:query', id: ${JSON.stringify(id)}, out: out }, '*')`;
    // A body that does not parse (a typo, or `await` in a plain function) never runs, so nothing would come back
    // and the card waited for the timeout: 29 of 30 queries on 13.11.2026. window.onerror reports the SyntaxError,
    // and the body runs inside an async function, so `await` is allowed.
    const doc = PreviewDoc.inject('<!doctype html><html><head></head><body></body></html>', PreviewDoc.CSP +
      `<script>window.onerror = function (m) { var out = { ok: false, error: String(m).replace(/^Uncaught /, '') }; ${post}; };</script>` +
      '<script>window.WORKSHOP_DATA={' + parts.join(',') + '};</script>' +
      '<script>(async function () { let out; try { const r = await (async function () {\n' + PreviewDoc.escapeScript(code) + '\n})();' +
      ' out = { ok: true, r: JSON.parse(JSON.stringify(r === undefined ? null : r)) }; } catch (e) { out = { ok: false, error: String((e && e.message) || e) }; }' +
      ` ${post}; })();</script>`);
    const f = document.createElement('iframe');
    f.setAttribute('sandbox', 'allow-scripts');
    f.hidden = true;
    f.title = 'A query on your data';
    return new Promise((resolve) => {
      const done = (out) => { clearTimeout(timer); window.removeEventListener('message', on); f.remove(); resolve(out); };
      const on = (e) => { if (e.source === f.contentWindow && e.data && e.data.type === 'studio:query' && e.data.id === id) done(e.data.out); };
      const timer = setTimeout(() => done({ ok: false, error: `it ran for more than ${QUERY_TIMEOUT_MS / 1000} seconds` }), QUERY_TIMEOUT_MS);
      window.addEventListener('message', on);
      f.srcdoc = doc;
      document.body.append(f);
    });
  }

  function queryCard(t) {
    const code = extractQuery(t.reply);
    const card = document.createElement('div');
    card.className = 'qcard';
    card.innerHTML = '<div class="qhead">Computed in your browser, on all the data</div><div class="qbody">Running the query…</div>' +
      '<details><summary>The code the model wrote</summary><pre></pre></details>' +
      '<div class="row"><button type="button" class="ghost" data-act="again">Run again</button><button type="button" class="ghost" data-act="csv" hidden>Copy as CSV</button></div>';
    card.querySelector('pre').textContent = code;
    const files = [...new Set([...S.versions, ...S.talk].filter((x) => x.created <= t.created).flatMap((x) => x.files || []))];
    const body = card.querySelector('.qbody'), csv = card.querySelector('[data-act=csv]');
    const run = async () => {
      body.textContent = 'Running the query…';
      const t0 = performance.now();
      const out = await runQuery(code, files);
      const secs = ((performance.now() - t0) / 1000).toFixed(1);
      track('query', { ok: !!out.ok, rows: out.ok && out.r && Array.isArray(out.r.rows) ? out.r.rows.length : null, s: Number(secs),
        kind: out.ok ? null : (/^\w*Error\b/.exec(out.error || '') || ['other'])[0], prompt: t.promptId || null });
      if (!out.ok) {
        body.innerHTML = `<p class="qerr">The query failed: ${esc(out.error)}. Tell the model what went wrong, or ask again in other words.</p>`;
        csv.hidden = true;
        return;
      }
      const r = out.r || {};
      if (!Array.isArray(r.rows) || !Array.isArray(r.columns)) {
        body.innerHTML = `<p>${esc(typeof r === 'object' ? JSON.stringify(r) : String(r))}</p><p class="qnote">${secs} s</p>`;
        csv.hidden = true;
        return;
      }
      const cell = (v) => esc(v == null ? '' : typeof v === 'number' ? fmt(v) : String(v));
      body.innerHTML = `<table><caption>${esc(r.title || 'Result')}</caption><thead><tr>${r.columns.map((c) => `<th scope="col">${esc(c)}</th>`).join('')}</tr></thead>` +
        `<tbody>${r.rows.slice(0, 200).map((row) => `<tr>${(Array.isArray(row) ? row : [row]).map((v) => `<td${typeof v === 'number' ? ' class="num"' : ''}>${cell(v)}</td>`).join('')}</tr>`).join('')}</tbody></table>` +
        `<p class="qnote">${esc(r.note || '')}${r.note ? ' · ' : ''}${fmt(r.rows.length)} rows · ${secs} s · nothing was sent to a model</p>`;
      csv.hidden = false;
      csv.onclick = async () => {
        const q = (v) => { const s = v == null ? '' : String(v); return /[",\r\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
        const text = [r.columns, ...r.rows].map((row) => (Array.isArray(row) ? row : [row]).map(q).join(',')).join('\r\n');
        try { await navigator.clipboard.writeText(text); csv.textContent = 'Copied'; } catch (e) { csv.textContent = 'Could not copy'; }
        setTimeout(() => { csv.textContent = 'Copy as CSV'; }, 2000);
      };
    };
    card.querySelector('[data-act=again]').onclick = run;
    run();
    return card;
  }

  /* ---------- preview ---------- */

  function fileFor(k) {
    return k === 'uhri' ? S.countryFile : S.index.datasets[k].file;
  }

  // the participant's own file is already in this browser; one that was removed gives an app no records
  const ownText = (k) => (S.own[k] ? S.own[k].text : JSON.stringify({ dataset: k, removed: true, count: 0, records: [] }));

  async function dataText(k) {
    if (k.startsWith('own_')) return PreviewDoc.escapeScript(ownText(k));
    const f = fileFor(k);
    if (!S.dataText[f]) S.dataText[f] = PreviewDoc.escapeScript(await getText('data/' + f));
    return S.dataText[f];
  }

  async function dataParsed(k) {
    if (k.startsWith('own_')) return JSON.parse(ownText(k));
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
        f.setAttribute('sandbox', 'allow-scripts allow-forms allow-downloads allow-modals allow-popups allow-popups-to-escape-sandbox');
        f.setAttribute('allow', 'clipboard-write');
        f.title = 'Your app';
        f.className = 'back';
        $('viewport').prepend(f);
        this.frames.push(f);
      }
    },
    // one load at a time: a sketch set while the code streams and the finished app set right after it (an answer
    // that arrives in one piece) would otherwise race for the same frame, and the sketch, with no scripts, could win
    show(doc) {
      const run = () => this.load(doc);
      this.queue = (this.queue || Promise.resolve()).then(run, run);
      return this.queue;
    },
    load(doc) {
      return new Promise((resolve) => {
        const back = this.frames[1 - this.front];
        this.loading = back;   // its scripts run before it comes to the front: their errors belong to the app being shown
        back.onload = () => {
          this.loading = null;
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
    // a session without an app yet: no frame on the stage
    clear() {
      const run = () => this.frames.forEach((f) => { f.classList.add('back'); f.removeAttribute('srcdoc'); });
      this.queue = (this.queue || Promise.resolve()).then(run, run);
    },
    win() { return this.frames[this.front].contentWindow; },
    // the frame on the stage, or the one loading to take its place (an app that fails as it opens fails there)
    owns(w) { return w === this.win() || (this.loading && w === this.loading.contentWindow); },
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
    if (m.type === 'studio:ready' && S.watch && S.watch.n === S.current && Preview.owns(e.source)) {   // the new version's scripts ran: any error came first
      const w = S.watch;
      S.watch = null;
      if (!w.err) { const had5 = S.progress.done[4]; Progress.mark(5); if (w.improves && had5) Progress.mark(7); if (w.first) TestCard.open(); }
    }
    if (m.type === 'studio:ready' && Run3.waiting && e.source === Run3.frame.contentWindow) return Run3.got({ fp: m.fingerprint, shown: m.shown || { picks: [] } });
    const fromTab = tabs.has(e.source);
    if (fromTab && m.type === 'studio:tab-ready') return sendToTab(e.source);
    if (!Preview.owns(e.source) && !fromTab) return;
    if (m.type === 'studio:ask') handleAsk(e.source, m);
    else if (fromTab) return;   // a tab shows its own errors and PDFs
    else if (m.type === 'studio:open-source') openSource(m.symbol, m.page, m.quote);
    else if (m.type === 'studio:error') showAppError(m);
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
    const libs = await Promise.all(['library', 'pdfs'].map((k) => dataParsed(k).catch(() => null)));
    const doc = libs.flatMap((l) => (l ? l.records : [])).find((d) => d.id === id || d.symbol === id);
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
  const askCache = new Map();   // model + request -> answer, until the page is reloaded
  async function handleAsk(win, m) {
    const reply = (x) => win.postMessage(Object.assign({ type: 'studio:answer', id: m.id }, x), '*');
    const content = m.prompt + (m.json ? '\n\nReply with JSON only.' : '');
    const key = S.model + '\n' + content;
    if (askCache.has(key)) { track('ask_cached'); return reply({ text: askCache.get(key) }); }
    while (asking >= 2) await new Promise((r) => setTimeout(r, 150));
    asking++;
    try {
      const { text, usage } = await chat({ purpose: 'inapp', model: S.model, messages: [{ role: 'user', content }] });
      addTrace({ purpose: 'inapp', usage, messages: [{ role: 'user', content }], userText: content });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      askCache.set(key, text);
      reply({ text });
    } catch (e) {
      reply({ error: e.message });
    } finally {
      asking--;
    }
  }

  /* ---------- feedback: the tester's words and the page's own context, never data or an app's code ---------- */

  function feedbackContext() {
    const v = currentVersion();
    const m = S.config.models[S.model] || {};
    return {
      version: (document.querySelector('script[src^="studio.js"]') || {}).src?.split('v=')[1] || '',
      session: S.session, route: S.route ? S.route.id : '', model: m.label || S.model || '', country: S.country || '',
      app: v ? `v${v.n} · ${titleOf(v.html)}${v.promptId ? ' · ' + v.promptId : ''} · ${v.label || ''}` : 'no app yet',
      error: S.lastAppError || '', browser: navigator.userAgent.replace(/^Mozilla\/5\.0 /, ''), screen: `${innerWidth}×${innerHeight}`,
    };
  }

  function openFeedback() {
    const d = $('feedbackDialog'), ctx = feedbackContext();
    $('feedbackErr').hidden = true;
    $('feedbackCtx').innerHTML = Object.entries(ctx).filter(([, x]) => x).map(([k, x]) => `<li><b>${esc(k)}</b> ${esc(x)}</li>`).join('');
    d.onclose = async () => {
      const text = $('feedbackText').value.trim();
      if (d.returnValue !== 'send' || !text) return;
      const base = S.route && S.route.type === 'server' ? S.route.base : (S.config.routes.find((r) => r.type === 'server') || {}).base;
      try {
        const res = await fetch(base + '/feedback', { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ seat: S.seatCode || null, text, context: ctx }) });
        if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || 'not sent');
        $('feedbackText').value = '';
        note('<b>Thank you.</b> Your message went to the facilitator.');
      } catch (e) {
        note('Your message could not be sent (' + esc(e.message) + '). It is still in the Feedback box; try again, or tell the facilitator.');
      }
    };
    d.showModal();
    $('feedbackText').focus();
  }

  /* ---------- the room chat: the facilitator's messages to everyone in the course, and a participant's message back ---------- */

  // GET /room every 15 s while the page is visible, in recorded mode too; a local page talks only to a local test
  // server (?api=). The newest unread message stays in a strip until it is closed; Messages opens them all, with a
  // box to write to the facilitator, who answers the whole room. What a participant wrote reaches only the
  // facilitator's room page (server/room_page.html) and this browser.
  const Room = {
    items: [], title: 'Messages',
    key: (k) => `ws:room:${CFG.roomId}:${k}`,
    base() {
      if (S.route && S.route.type === 'server') return S.route.base;
      if (/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) return null;
      return (S.config.routes.find((r) => r.type === 'server') || {}).base || null;
    },
    seen() { return Number(localGet(this.key('seen'))) || 0; },
    top() { return this.items.length ? this.items[this.items.length - 1].id : 0; },
    mine() { try { return JSON.parse(localGet(this.key('mine')) || '[]'); } catch (e) { return []; } },
    drawerOpen() { return !$('drawer').hidden && $('drawerTitle').textContent === this.title; },
    start() {
      if (!this.base()) return;
      $('roomBtn').hidden = false;
      this.poll();
      setInterval(() => { if (!document.hidden) this.poll(); }, 15000);
      document.addEventListener('visibilitychange', () => { if (!document.hidden) this.poll(); });
    },
    async poll() {
      const base = this.base();
      if (!base) return;
      try {
        const res = await fetch(`${base}/room?course=${encodeURIComponent(CFG.roomId)}`, { cache: 'no-store' });
        if (!res.ok) return;
        const items = (await res.json()).items || [];
        const changed = items.map((i) => i.id).join() !== this.items.map((i) => i.id).join();
        this.items = items;
        if (changed) this.render();
      } catch (e) { /* the next poll */ }
    },
    render() {
      if (this.drawerOpen()) { this.renderList(); if (this.top() > this.seen()) localSet(this.key('seen'), String(this.top())); }
      const unread = this.items.filter((i) => i.id > this.seen()), last = unread[unread.length - 1];
      $('roomDot').hidden = !unread.length;
      if (last) {
        if ($('roomStrip').hidden) track('room_msg', { n: unread.length });
        $('roomText').innerHTML = linkify(last.text);
        $('roomWhen').textContent = '· ' + hhmm(last.at) + (unread.length > 1 ? ` · ${unread.length} new` : '');
      }
      $('roomStrip').hidden = !last;
    },
    read() {
      if (this.top() > this.seen()) localSet(this.key('seen'), String(this.top()));
      this.render();
    },
    open() {
      openDrawer(this.title);
      $('drawerBody').innerHTML = `<div class="room-list" id="roomList"></div>
        <form class="room-form" id="roomForm">
          <label for="roomInput"><b>Write to the facilitator</b></label>
          <textarea id="roomInput" maxlength="1000" placeholder="A question, a problem, a link that does not work…"></textarea>
          <div class="row"><small>Only the facilitator sees what you write; answers come here, to the whole room.</small>
            <button type="submit" class="primary">Send</button></div>
          <p class="room-err" id="roomErr" hidden></p>
        </form>`;
      $('roomForm').onsubmit = (e) => { e.preventDefault(); this.send(); };
      $('roomInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); this.send(); }
      });
      this.renderList();
      this.read();
      track('room_open', { n: this.items.length });
      $('roomInput').focus();
    },
    renderList() {
      if (!$('roomList')) return;
      const all = [...this.items.map((i) => ({ ...i, me: false })), ...this.mine().map((i) => ({ ...i, me: true }))]
        .sort((a, b) => new Date(a.at) - new Date(b.at));
      $('roomList').innerHTML = all.length ? all.map((i) => `<div class="room-msg${i.me ? ' mine' : ''}"><span class="who">${i.me ? 'You, to the facilitator' : 'Facilitator, to the room'} · ${hhmm(i.at)}</span>${linkify(i.text)}</div>`).join('')
        : '<p class="room-empty">No messages yet. The facilitator\'s messages to the room appear here and at the top of the studio.</p>';
    },
    async send() {
      const text = $('roomInput').value.trim();
      if (!text) return;
      $('roomErr').hidden = true;
      try {
        const res = await fetch(`${this.base()}/room`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ course: CFG.roomId, text, seat: S.seatCode || null, sid: Track.sid }) });
        if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || 'not sent');
        localSet(this.key('mine'), JSON.stringify([...this.mine(), { at: new Date().toISOString(), text }].slice(-30)));
        $('roomInput').value = '';
        track('room_sent', { chars: text.length });
        this.renderList();
      } catch (e) {
        $('roomErr').textContent = 'Your message could not be sent (' + e.message + '). Try again, or raise your hand.';
        $('roomErr').hidden = false;
      }
    },
  };
  const hhmm = (iso) => new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  // plain text with its web addresses as links, which open in a new tab
  const linkify = (s) => esc(s).replace(/https?:\/\/(?:(?!&#39;|&quot;|&gt;)[^\s<])+/g, (u) => {
    const tail = (/[.,;:!?)\]]+$/.exec(u) || [''])[0], url = u.slice(0, u.length - tail.length);   // "see https://x.org." ends before the dot
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>${tail}`;
  });

  function showAppError(m) {
    S.lastAppError = String(m.message || '').slice(0, 200);
    if (S.watch && S.watch.n === S.current) S.watch.err = true;
    const a = S.autoFix;
    // the kind of error only (TypeError, SyntaxError…): its message may quote the data
    track('app_error', { prompt: (currentVersion() || {}).promptId || null, kind: (/^\w*Error\b/.exec(String(m.message || '').replace(/^Uncaught\s+/, '')) || ['other'])[0], ver: S.current,
      first: !!(a && a.n === S.current && performance.now() - a.t < REPAIR_WINDOW_MS) });
    if (a && a.n === S.current && performance.now() - a.t < REPAIR_WINDOW_MS) {
      S.autoFix = null;
      if (S.busy) S.pendingRepair = m;   // the build that showed the app has not finished yet
      else autoRepair(m);
      return;
    }
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
    offerRecorded(box, chain);
  }

  // a second button where a working build of the same exercise was recorded beforehand: it comes in as a new
  // version, so the session goes on (the broken one stays in the version menu)
  async function offerRecorded(box, chain) {
    const ids = [...new Set([chain[chain.length - 1].promptId, (chain.find((v) => !v.fix) || chain[0]).promptId].filter(Boolean))];
    for (const id of ids) {
      let html = '', by = '';
      for (const rec of [S.config.replay, S.config.replay.fallback]) {
        if (!rec || html) continue;
        html = extractHtml(await getText(rec.dir + id + '.md').catch(() => '')) || '';
        by = (S.config.models[rec.model] || {}).label || rec.model;
      }
      if (!html || box.hidden) continue;
      const p = S.prompts.find((q) => q.id === id);
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'recorded';
      b.textContent = 'Load a working version';
      b.onclick = async () => {
        box.hidden = true;
        track('rescue', { prompt: id });
        const local = S.country === 'Kenya' ? html : html.replace(/Kenya/g, S.country);
        const v = { n: S.versions.length + 1, parent: null, user: `A working version: ${p.title}`, files: p.dataset ? [p.dataset] : [], sent: promptText(p),
          model: S.model, label: `${by} · recorded beforehand`, seconds: null, cost: null, recorded: true, promptId: id, created: Date.now(),
          html: local, reply: '```html\n' + local + '\n```', fix: false,
          summary: `${p.title}, as ${by} built it before the class. Your broken version stays in the version menu. Go on from here: ask for a change, or pick a next step below.` };
        S.versions.push(v);
        S.current = v.n;
        save();
        renderAll();
        await showVersion(v);
      };
      box.append(b);
      return;
    }
  }

  /* ---------- Run x3, Ask x3 ---------- */

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

  /* ---------- trace: what left this laptop ---------- */

  function addTrace({ purpose, usage, messages, userText, parent, files = [], shelf = [], plan = null, images = [], planned = null }) {
    const sys = purpose === 'build' ? buildSystem() : (S.config.direct_system[purpose] || '');
    const ids = (userText.match(UUID) || []).length;
    const sent = [], kept = [];
    if (purpose === 'build') {
      sent.push(`Your message (${fmt(userText.length)} characters)`);
      if (planned) sent.push(`Your prompt and the plan you approved (v${planned.version}, ${whoOf(planned)}, about ${fmt(words(planText(planned.plan)))} words), both inside your message`);
      if (plan) sent.push(`The plan you asked to change (v${plan.version}, about ${fmt(words(planText(plan.plan)))} words)`);
      if (shelf.length) sent.push(`${shelf.length === 1 ? 'An excerpt' : fmt(shelf.length) + ' excerpts'} from the workshop reference shelf, found by a search on your message: ${shelf.map((h) => h.page.title).join('; ')}`);
      if (images.length) sent.push(`Your ${images.length === 1 ? 'picture' : images.length + ' pictures'} (${images.map((im) => `${im.w}×${im.h}`).join(', ')}): ` +
        'the whole image, with everything on it');
      const shelfFiles = files.filter((k) => !S.own[k]);
      if (shelfFiles.length) sent.push(`The name of each file you added (${shelfFiles.map(fileLabel).join('; ')}): not its contents`);
      files.filter((k) => S.own[k]).forEach((k) => {
        const e = S.own[k];
        sent.push(`Your ${OwnFiles.NOUN[e.kind]} "${e.name}": its name, its field names and their types` +
          (e.samples ? `, and its first ${Math.min(OwnFiles.SAMPLES, e.shape.count)} records, as you chose` : ', no values'));
        kept.push(`All ${fmt(e.shape.count)} records of "${e.name}" stay in this browser, where your app reads them.`);
      });
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
        messages.map((m) => `[${m.role}]\n${m.content}` + (m.images ? `\n[${m.images.length} picture(s) attached, sent whole]` : '')).join('\n\n'),
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
    $('drawer').classList.remove('wide', 'inside');
    $('drawerTitle').textContent = title;
    $('drawer').hidden = false;
  }

  /* ---------- the Look inside menu ---------- */

  // the toolbar's two menus (Look inside, Save & share): one open at a time
  function closeMenu() {
    document.querySelectorAll('.menu-panel').forEach((p) => { p.hidden = true; });
    document.querySelectorAll('.menu > button[aria-haspopup]').forEach((b) => b.setAttribute('aria-expanded', 'false'));
  }

  function toggleMenu(btn = $('lookBtn'), panel = $('lookPanel')) {
    const open = panel.hidden;
    closeMenu();
    panel.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
  }

  /* ---------- download and wall ---------- */

  function titleOf(html) {
    const m = html.match(/<title>([^<]*)<\/title>/i);
    return (m ? m[1] : 'workshop-app').trim();
  }

  async function download() {
    const v = currentVersion();
    if (!v) return;
    track('save', { prompt: v.promptId || null, ver: v.n });
    const blob = new Blob([await fullDoc(v)], { type: 'text/html' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${titleOf(v.html).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50) || 'app'}-v${v.n}.html`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    note(`Saved <b>${esc(a.download)}</b>. It holds the app and the data it needs, so it opens with a double-click, even offline. AI buttons inside it only work in the studio.`);
  }

  // the take-home kit (site/kit.js, site/kit/kit.html): one file with the workshop requests for any chatbot, a place to
  // run the app a chatbot writes, the data, and the participant's apps
  // by course: the requests of its sessions, and the files they read
  const slugOf = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 50) || 'app';

  async function downloadKit(btn) {
    const label = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Building the kit…';
    try {
      const built = new Date().toISOString().slice(0, 10), sys = Kit.system(S.sysmd), steps = [];
      let had = [];
      for (const [session, id, first] of CFG.kit.steps) {
        const p = S.prompts.find((q) => q.id === id);
        if (!p) continue;
        const keys = p.dataset ? [p.dataset, ...(fileMeta(p.dataset).also || [])] : [];
        const pack = p.planning ? await getJSON('data/' + p.planning) : null;
        const plan = pack ? planText(composePlan(pack, {})) : '';
        // a free-brief pack: the participant's own brief and plan, as their latest build of it sent them (without any
        // shelf excerpts); before a build, the brief with the topic's default and the plan
        const mine = pack && pack.free_brief && [...S.versions].reverse().find((v) => v.promptId === id && (v.sent || '').startsWith(BRIEF_HEAD));
        const req = !pack ? promptText(p) : mine ? mine.sent.split('\n\nReference shelf excerpts (offline copies)\n')[0]
          : pack.free_brief ? `${BRIEF_HEAD}\n\nMy prompt:\n${pack.problem.replace(/\[my topic\]/g, () => topicDefault(pack))}\n\nThe plan:\n${plan}` : PLAN_HEAD + '\n\n' + plan;
        const fresh = first ? keys : keys.filter((k) => !had.includes(k));   // a follow-up describes only data the conversation lacks
        const text = [first ? sys : '', fresh.length ? Kit.data(S.schema, S.samples, fresh) : '',
          '# The request\n\n' + req + (p.dataset ? '\n\n' + attachLine(p.dataset) : '')].filter(Boolean).join('\n\n---\n\n');
        had = first ? keys : [...new Set([...had, ...keys])];
        steps.push({ session, first, title: p.title, blurb: p.blurb, text });
      }
      // the participant's apps: the latest version of each (no other version builds on it), the newest six; their code
      // here, their data the kit's (with any of the participant's own files they read)
      // (every session's: the current one here, the others from this browser's storage)
      const work = CFG.sessions.map((s, i) => {
        let vs = S.versions;
        if (s !== S.session) try { vs = (JSON.parse(localGet(storeKey(s)) || 'null') || {}).versions || []; } catch (e) { vs = []; }
        return vs.filter((v) => !vs.some((w) => w.parent === v.n)).map((v) => ({ v, vs, n: i + 1 }));
      });
      const leaves = work.flat().sort((a, b) => (a.v.created || 0) - (b.v.created || 0)).slice(-6);
      const apps = leaves.map(({ v, n }) => ({ title: titleOf(v.html), note: `Session ${n}, version ${v.n}, by ${v.label}`, html: v.html }));
      if (CFG.backup) {   // Geneva: the five recorded apps after the participant's own, so the kit shows working apps with no model and no internet
        const pack = await getJSON('data/planning/g1-verbatim.json');
        for (const l of pack.looks) {
          const html = extractHtml(await getText(`${S.config.replay.dir}g1-verbatim.${l.id}.md`).catch(() => ''));
          if (html) apps.push({ title: `Recorded app: ${l.label}`, note: 'recorded beforehand with Claude Sonnet 5.5', html });
        }
      }
      // every file those apps read, the workshop's (hrc_all dragged into a Venice app) and the participant's own
      const used = [...new Set(leaves.flatMap(({ v, vs }) => chainOf(v, vs).flatMap((x) => x.files || [])).filter((k) => S.own[k] || S.index.datasets[k]))];
      const datasets = {};
      for (const k of new Set([...CFG.kit.data, ...used])) datasets[k] = await dataParsed(k);
      const html = Kit.page(await getText('kit/kit.html'), { chart: S.chart, runtime: S.runtime, datasets, meta: { country: CFG.country ? S.country : '', built }, steps, apps });
      const blob = new Blob([html], { type: 'text/html' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `garage-research-kit-${CFG.country ? slugOf(S.country) : S.course}.html`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 4000);
      track('kit', { mb: Math.round(blob.size / 1e5) / 10, apps: apps.length });
      note(`Saved <b>${esc(a.download)}</b> (${(blob.size / 1e6).toFixed(0)} MB). Open it with a double-click: the workshop requests to paste into your own chatbot or LM Arena, a place to paste its answer and run the app on the data, offline, and your apps from today.`);
    } catch (e) {
      note(`The kit could not be built (${esc(e.message || String(e))}).`);
    } finally {
      btn.disabled = false;
      btn.textContent = label;
    }
  }

  // The wall takes the app on the stage, with the country and the files it ran on; in Geneva also a name to sign it with and
  // the course, so the room's wall shows this course and each person's newest app. The seat code is for that grouping only
  // and is never shown.
  async function postWall(v, name) {
    track('wall', { prompt: v.promptId || null });
    try {
      const res = await fetch(S.route.base + '/gallery', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seat: S.seatCode, title: titleOf(v.html), model: v.model, prompt_id: v.promptId, html: v.html,
          country: S.country, files: [...new Set(chainOf(v).flatMap((x) => x.files || []))],
          ...(CFG.signWall ? { course: CFG.roomId, ...(name ? { name } : {}) } : {}) }),
      });
      const j = await res.json().catch(() => ({}));
      return res.ok ? { ok: true } : { ok: false, code: j.code, error: j.error || 'The wall did not accept it.' };
    } catch (e) {
      return { ok: false, error: 'The wall is not reachable right now.' };
    }
  }

  async function sendToWall() {
    const v = currentVersion();
    if (!v || S.route.type !== 'server') return;
    let err = '';
    for (;;) {
      const name = CFG.signWall ? await askName(err) : '';
      if (name === null) return;   // Cancel
      const r = await postWall(v, name);
      if (r.code === 'bad_name') { err = r.error; continue; }   // the same question again, with the server's words
      if (r.ok && name) localSet('ws:wallname', name);
      note(r.ok ? 'Sent to the wall.' : esc(r.error));
      return;
    }
  }

  // "Sign it": a small card in the chat; a name is optional, Enter sends, Escape or Cancel does not
  function askName(err) {
    return new Promise((resolve) => {
      const d = document.createElement('form');
      d.className = 'msg note signcard';
      d.innerHTML = '<b>Sign it?</b> <span>Your name, or a name for your app. Leave it empty to send it unsigned.</span>' +
        '<input type="text" maxlength="40" autocomplete="off" aria-label="Sign it (optional)" placeholder="Your name, or a name for your app">' +
        `<p class="err" ${err ? '' : 'hidden'}></p><div class="row"><button type="submit" class="primary">Send to wall</button><button type="button" class="ghost">Cancel</button></div>`;
      d.querySelector('.err').textContent = err || '';
      const input = d.querySelector('input');
      input.value = localGet('ws:wallname') || '';
      const done = (v) => { d.remove(); resolve(v); };
      d.onsubmit = (e) => { e.preventDefault(); done(input.value.trim()); };
      d.querySelector('.ghost').onclick = () => done(null);
      d.onkeydown = (e) => { if (e.key === 'Escape') done(null); };
      $('log').append(d);
      scrollLog();
      input.focus();
    });
  }

  // At 100%: "Show it to the room?" (once; Send to wall in Save & share stays)
  function wallDialog() {
    const d = $('wallDialog');
    $('wallName').value = localGet('ws:wallname') || '';
    $('wallErr').hidden = true;
    d.returnValue = '';
    d.showModal();
    $('wallName').focus();
  }
  $('wallForm').onsubmit = async (e) => {
    if (e.submitter !== $('wallSend')) return;   // Not now closes the dialog as it is
    e.preventDefault();
    const v = currentVersion(), name = $('wallName').value.trim();
    if (!v) return $('wallDialog').close('no');
    $('wallSend').disabled = true;
    const r = await postWall(v, name);
    $('wallSend').disabled = false;
    if (!r.ok) { $('wallErr').textContent = r.error; $('wallErr').hidden = false; return; }   // bad_name too: it stays open, with the server's words
    track('wall_dlg', { named: name ? 1 : 0 });
    if (name) localSet('ws:wallname', name);
    $('wallDialog').close('sent');
    note('Sent to the wall. Look at the projector.');
  };

  // A model that is busy or that fails is never swapped for another without saying so: the server's own words, then
  // Try again or the other model (the menu changes with it). The failed turn gives way to the new one.
  const TROUBLE = new Set(['model_busy', 'model_failed']);
  function modelChoice(box, gone, resend) {
    const other = CFG.models.find((m) => m !== S.model);
    const row = document.createElement('div');
    row.className = 'choice';
    row.innerHTML = '<button type="button" class="primary" data-c="again">Try again</button>' +
      (other ? `<button type="button" class="ghost" data-c="other">Use ${esc(S.config.models[other].label)}</button>` : '');
    box.append(row);
    if (CFG.backup) backupButton(box, gone, resend, row);   // the third button: the recordings
    scrollLog();
    row.onclick = (e) => {
      const b = e.target.closest('button');
      if (!b || S.busy || b.dataset.c === 'recorded') return;
      track('model_retry', { choice: b.dataset.c });
      if (b.dataset.c === 'other') {
        track('model', { from: S.model, to: other, by: 'busy' });
        S.model = other;
        localSet('ws:model', S.model);
        $('modelSelect').value = S.model;
        renderBadge();
      }
      gone.forEach((el) => el.remove());
      resend();
    };
  }

  /* ---------- Geneva: the test card (step 6) and three improvement ideas (step 7) ---------- */

  const CHANGE_APP = 'Change the app: ';
  const TESTS = ['I searched a phrase I know and it appears word for word',
    'I opened the source of one result and the paragraph is the same',
    'I pasted a copied citation and it has the symbol and the paragraph number'];

  // The card sits under the first Verbatim finder, once it has opened without an error; what is ticked is kept with the work.
  const TestCard = {
    el: null,
    open() {
      if (!CFG.progress || S.test.shown) return;
      S.test.shown = true;
      save();
      this.add();
    },
    // (re)made from the saved state, after the given message or at the end of the chat
    add(after) {
      if (!CFG.progress || !S.test.shown) return;
      if (this.el) this.el.remove();
      const el = this.el = document.createElement('div');
      el.className = 'msg test-card';
      el.innerHTML = '<b>Test your app</b><span class="tsum">Try it on something you know. Tick a line when it is true.</span>' +
        TESTS.map((t, i) => `<label class="tline"><input type="checkbox" data-i="${i}"${S.test.checks[i] ? ' checked' : ''}><span>${esc(t)}</span></label>`).join('') +
        '<label class="tnote"><span>One thing I would change (optional)</span><input type="text" maxlength="200" autocomplete="off" placeholder="e.g. show the year next to each result"></label>' +
        '<p class="tdone" hidden>All three are true. Next: ask for one improvement.</p>';
      el.querySelector('.tnote input').value = S.test.note;
      const sync = () => { el.querySelector('.tdone').hidden = !S.test.checks.every(Boolean); };
      el.addEventListener('change', (e) => {
        const i = e.target.dataset.i;
        if (i == null) return;
        S.test.checks[Number(i)] = e.target.checked;
        if (S.test.checks.every(Boolean) && !S.progress.done[5]) { track('test_done', { n: 3 }); Progress.mark(6); }   // the note's words never leave the browser
        save();
        sync();
      });
      el.querySelector('.tnote input').addEventListener('input', (e) => { S.test.note = e.target.value; save(); });
      sync();
      if (after) after.after(el); else { $('log').append(el); scrollLog(); }
    },
  };

  // eight perspectives; each time three of them are drawn, never the three just shown
  const LENSES = [
    { id: 'first_user', label: 'A first-time user', ask: "a first-time user, judged by Nielsen's usability heuristics: is it clear what the app does, what is happening and what to do next" },
    { id: 'trust', label: 'Can I trust the results?', ask: 'can I trust the results: data quality, meaning accuracy, completeness, consistency, and whether the app says what it leaves out' },
    { id: 'premortem', label: 'A pre-mortem', ask: 'a pre-mortem (Gary Klein): imagine the app failed badly in front of a room, say what went wrong, and propose what would have prevented it' },
    { id: 'access', label: 'Accessibility', ask: 'accessibility, judged by WCAG 2.2: keyboard use, contrast, text size, labels and focus' },
    { id: 'hurry', label: 'A colleague in a hurry', ask: 'a colleague in a hurry: speed, and the fewest clicks from opening the app to a usable answer' },
    { id: 'citation', label: 'A careful drafter', ask: 'a careful drafter: citation precision, the symbol and the paragraph number exactly right and easy to copy' },
    { id: 'language', label: 'Another language', ask: 'someone working in another language: a French or Spanish speaker reading English results, and what helps them find and check a passage' },
    { id: 'judge', label: 'A sceptical judge', ask: 'a sceptical judge: could a quotation, shown without its context, mislead a reader' },
  ];
  function pickLenses() {
    let pool = LENSES.filter((l) => !S.lastLenses.includes(l.id));
    if (pool.length < 3) pool = LENSES.slice();
    for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
    S.lastLenses = pool.slice(0, 3).map((l) => l.id);
    return S.lastLenses.slice();
  }

  // the model's JSON block, or bare JSON; null when there is none to read
  function parseIdeas(text, ids) {
    const found = [];
    const fence = /```(?:json)?[ \t]*\n?([\s\S]*?)```/gi;
    let m;
    while ((m = fence.exec(text))) found.push(m[1]);
    const a = text.indexOf('{'), b = text.lastIndexOf('}');
    if (a >= 0 && b > a) found.push(text.slice(a, b + 1));
    const cut = (x, n) => String(x || '').trim().slice(0, n);
    for (const raw of found) {
      try {
        const j = JSON.parse(raw.trim());
        const list = (Array.isArray(j) ? j : (j && j.ideas) || []).filter((x) => x && typeof x.title === 'string' && typeof x.request === 'string' && x.title.trim() && x.request.trim());
        if (list.length) return list.slice(0, 3).map((x, i) => ({ title: cut(x.title, 90), what: cut(x.what, 420), why: cut(x.why, 320), request: cut(x.request, 700),
          perspective: ids.includes(x.perspective) ? x.perspective : ids[i] || ids[0] }));
      } catch (e) { /* the next candidate */ }
    }
    return null;
  }

  const REC_PERSPECTIVES = ['first_user', 'trust', 'citation'];   // the order the recorded ideas (g1-improve.md) were made in
  async function suggestIdeas(ids) {
    const v = currentVersion(), p = S.prompts.find((q) => q.id === 'g1-improve');
    if (!v || !p || S.busy || !S.ready) return;
    const rec = recordedNow();
    ids = rec ? REC_PERSPECTIVES : ids || pickLenses();   // recorded: the three perspectives the recording was made for
    const content = p.prompt.replace('{perspectives}', ids.map((id) => { const l = LENSES.find((x) => x.id === id); return `- ${l.id}: ${l.ask}`; }).join('\n'));
    const model = S.model;
    setBusy(true);
    addUser('Suggest three improvements');
    const userEl = $('log').lastElementChild;
    const d = document.createElement('div');
    d.className = 'msg assistant';
    d.innerHTML = `<div class="who">${esc(S.config.models[model].label)}</div><div class="summary">Looking at your app from three points of view…</div>`;
    $('log').append(d);
    scrollLog();
    const t0 = performance.now();
    const say = () => { $('buildingText').textContent = `Looking at your app · ${Math.round((performance.now() - t0) / 1000)} s`; };
    say();
    const tick = setInterval(say, 1000);
    S.ctrl = new AbortController();
    try {
      const { text, usage } = await chat({ purpose: 'build', model, messages: buildMessages(v, content), promptId: p.id, signal: S.ctrl.signal,
        replay: rec ? 'g1-improve.md' : undefined });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      d.remove();
      const ideas = parseIdeas(text, ids);
      track('ideas_shown', { n: ideas ? ideas.length : 0, rec: !!usage.recorded });
      if (ideas) showIdeas(ideas, !!usage.recorded);
      else {
        const t = document.createElement('div');
        t.className = 'msg assistant';
        t.innerHTML = `<div class="who">${esc(usage.model_label || S.config.models[model].label)}</div><div class="summary answer-md">${md(text.trim() || 'The model sent back nothing.')}</div>`;
        $('log').append(t);
        note('The ideas did not come back as three cards, so they are shown as the model wrote them. Read them, then write your own change in the box, or ask again.');
        openComposer(CHANGE_APP);
      }
    } catch (e) {
      d.querySelector('.summary').remove();
      const box = document.createElement('div');
      box.className = 'msg err';
      box.textContent = e.name === 'AbortError' ? 'Stopped.' : TROUBLE.has(e.code) ? e.message : `The model could not finish (${e.message}). Try again.`;
      d.append(box);
      if (CFG.keepModel && TROUBLE.has(e.code)) modelChoice(box, [userEl, d], () => suggestIdeas(ids));
      else if (backupFor(e)) backupButton(box, [userEl, d], () => suggestIdeas(ids));
    } finally {
      clearInterval(tick);
      setBusy(false);
    }
  }

  // recorded: these ideas come from the recording, and "Build this" plays the improvement recorded for each
  function showIdeas(ideas, recorded) {
    if (recorded) { S.ideaOf = new Map(ideas.map((x, i) => [x.request.trim(), i + 1])); }
    const label = (id) => (LENSES.find((l) => l.id === id) || { label: id }).label;
    $('log').querySelectorAll('.ideas:not(.old)').forEach((g) => { g.classList.add('old'); g.querySelector('.ihead').textContent = 'Earlier ideas, set aside.'; });
    const g = document.createElement('div');
    g.className = 'msg ideas';
    g.innerHTML = '<p class="ihead"><b>Three ideas.</b> Each looks at your app from a different point of view. Build one, change it first, or skip it.</p>' +
      ideas.map((x, i) => `<div class="idea" data-i="${i}"><span class="ipersp">${esc(label(x.perspective))}</span><b class="ititle">${esc(x.title)}</b>` +
        `<p class="iwhat">${esc(x.what)}</p><p class="iwhy"><i>Why it matters:</i> ${esc(x.why)}</p><p class="ireq"><span>Request</span>${esc(x.request)}</p>` +
        '<div class="irow"><button type="button" class="primary" data-a="build">Build this</button><button type="button" class="ghost" data-a="edit">Edit first</button>' +
        '<button type="button" class="linkish" data-a="no">Not this</button></div></div>').join('') +
      '<div class="imore"><button type="button" class="ghost" data-a="own">My own idea</button><button type="button" class="ghost" data-a="more">Three other ideas</button></div>';
    g.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-a]');
      if (!b || b.closest('.old')) return;
      const card = b.closest('.idea'), x = card && ideas[Number(card.dataset.i)];
      if (recordedNow() && b.dataset.a !== 'no' && (b.dataset.a !== 'build' || !recorded)) {   // only the recorded ideas can be built, as they are
        return note(b.dataset.a === 'build' ? 'These ideas came from a live model, and in recorded mode no model is connected. Ask for three improvements again in recorded mode, or go back to the live model with the badge at the top.'
          : 'Changing an idea, asking for other ideas or writing your own needs a live model, and in recorded mode no model is connected. Build one of the three recorded ideas, or use the badge at the top (Back to the live model) when it is back.');
      }
      if (b.dataset.a === 'build') {
        if (S.busy) return note('Wait until the model has finished, then press <b>Build this</b> again.');
        const keep = $('input').value;   // what was being written stays
        track('idea_built', { perspective: x.perspective });
        card.classList.add('built');
        b.textContent = 'Sent';
        b.disabled = true;
        if (submitBuild(x.request) && keep.trim() && keep !== CHANGE_APP) { $('input').value = keep; fitInput(); }
      } else if (b.dataset.a === 'edit') {
        openComposer(x.request);
        $('input').setSelectionRange(x.request.length, x.request.length);
      } else if (b.dataset.a === 'no') {
        card.classList.toggle('folded');
        b.textContent = card.classList.contains('folded') ? 'Show it again' : 'Not this';
      } else if (b.dataset.a === 'own') {
        openComposer(CHANGE_APP + S.test.note.trim());
        $('input').setSelectionRange($('input').value.length, $('input').value.length);
      } else if (b.dataset.a === 'more') {
        suggestIdeas();
      }
    });
    $('log').append(g);
    g.scrollIntoView({ block: 'start' });
  }

  /* ---------- chat column ---------- */

  function addUser(text, files = [], images = []) {
    const d = document.createElement('div');
    d.className = 'msg user';
    if (files.length || images.length) d.innerHTML = `<div class="files">${files.map((k) => chipHtml(k)).join('')}` +
      `${images.map((im) => `<img class="pic" src="${im.url}" alt="Your picture, ${im.w}×${im.h}">`).join('')}</div>`;
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
    return d;
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
      const editing = !lines.length && last.includes('<<<<<<< SEARCH');
      const changes = editing ? last.slice(last.indexOf('<<<<<<< SEARCH')).split('\n') : [];
      if (last && thought && !folded) { folded = true; th.open = false; thLabel.textContent = `Thought for ${thoughtEnd.toFixed(0)} s`; }
      sum.textContent = lines.length || editing ? summaryOf(last) : last;   // an answer in words streams in full
      pre.textContent = (editing ? changes : lines).slice(-60).join('\n');
      pre.scrollTop = pre.scrollHeight;
      stat.textContent = editing ? `Writing changes · ${(last.match(/<<<<<<< SEARCH/g) || []).length} so far · ${secs().toFixed(0)} s`
        : lines.length ? `Writing code · ${fmt(lines.length)} lines · ${secs().toFixed(0)} s`
        : last ? `Answering · ${secs().toFixed(0)} s`
          : thought ? `Thinking · ${secs().toFixed(0)} s` : `Waiting for the model · ${secs().toFixed(0)} s`;
      if (thought && thoughtEnd === null) thLabel.textContent = `Thinking · ${secs().toFixed(0)} s`;
      // the stage shows the thinking, then the code as it is written, and fades to the sketch of the app
      // once the page body has begun (models write the styles first, and a sketch of those is blank)
      const thinking = !!thought && thoughtEnd === null;
      const body = code.search(/<body[\s>]/i);
      const writing = !thinking && (editing || (lines.length > 0 && (body < 0 || code.length - body < 600)));
      $('viewport').classList.toggle('thinking', thinking || writing);
      $('mind').classList.toggle('code', writing);
      $('mindWhere').textContent = where;
      if (thinking) {
        $('mindTitle').textContent = label + ' is thinking';
        $('mindText').textContent = thought.length > 2500 ? '…' + thought.slice(-2500) : thought;
        $('mindTime').textContent = `${secs().toFixed(0)} s`;
        $('mindNote').textContent = "The model's working notes, shown as it writes them. Ask again and they will be different. Your app is built from the code it writes next.";
      } else if (writing && editing) {
        $('mindTitle').textContent = label + ' is writing the changes';
        $('mindText').textContent = changes.slice(-40).join('\n');
        $('mindTime').textContent = `${secs().toFixed(0)} s`;
        $('mindNote').textContent = 'Only the lines that change are written: SEARCH is what is in your app now, REPLACE what takes its place. The studio puts them into your app.';
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
      // the edits did not fit: say so in the bubble, and stream the whole file that follows
      retry(msg) { const n = document.createElement('p'); n.className = 'retry-note'; n.textContent = msg; sum.before(n); last = ''; schedule(); },
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
        return e;
      },
      // an answer in words: rendered as text, no code card
      answer(t) {
        stop();
        if (thought) { th.hidden = false; th.open = false; thLabel.textContent = thoughtEnd != null ? `Thought for ${thoughtEnd.toFixed(0)} s` : 'Thought'; }
        sum.className = 'summary answer-md';
        sum.innerHTML = md(t.query ? withoutQuery(t.reply) : t.reply);
        d.querySelector('.code').remove();
        if (t.query) sum.after(queryCard(t));
        scrollLog();
      },
      lesson(text) { d.append(lessonEl(text)); },
    };
  }

  // enough Markdown for a chat answer or a plan: paragraphs, lists, headings, bold, italics, code,
  // fenced code and simple tables. A list item may run over several lines, and models often put a
  // blank line between items: consecutive items stay one list, numbered as written.
  function md(text, links) {   // links: [text](https://…) become links (the cheatsheet); a model's reply never gets them
    const inline = (s) => esc(s).replace(links ? /\[([^\]]+)\]\((https:\/\/[^)\s]+)\)/g : /$^/, '<a href="$2" target="_blank" rel="noopener">$1</a>').replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<i>$2</i>');
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
    const changed = v.edit ? ` · changed ${fmt(v.edit.lines)} of ${fmt(lines)} lines in ${v.edit.edits} ${v.edit.edits === 1 ? 'place' : 'places'}` : '';
    box.innerHTML = `<div class="bar"><span>v${v.n} · ${fmt(lines)} lines${changed} · ${v.seconds ? v.seconds.toFixed(0) + ' s' : ''}${v.cost != null ? ' · $' + Number(v.cost).toFixed(3) : ''} · ${esc(v.label)}</span><button type="button">Show code</button></div><pre></pre>`;
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
    let carded = false;   // the test card goes under the first Verbatim finder
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
        d.querySelector('.summary').innerHTML = md(t.query ? withoutQuery(t.reply) : t.reply);
        if (t.query) d.querySelector('.summary').after(queryCard(t));
      }
      $('log').append(d);
      if (v && !carded && v.promptId === 'g1-verbatim') { carded = true; TestCard.add(d); }
    });
    if (!carded) TestCard.add();   // a step skipped without such an app: at the end
  }

  const promptText = (p) => p.prompt.replace(/\{country\}/g, S.country);

  // a suggestion fills the message box, as in any chatbot: read it, change it if you like, send it.
  // The four workshop apps fill it with a short problem, in plan mode.
  function useSuggestion(p, fresh) {
    track('pick', { prompt: p.id, plan: plannable(p) && S.planMode });
    if (p.id === 'any-improve' && CFG.improveSwap) p = S.prompts.find((q) => q.id === 'improve-trust') || p;   // one way, not five
    if (p.id === 'any-improve') return showLenses();
    if (p.id === 'g1-improve') return suggestIdeas();
    preferModel(p);
    if (plannable(p)) return openPlanning(p, fresh);
    openComposer(promptText(p));
    Object.assign(S, { pendingPromptId: p.id, pendingText: promptText(p), freshNext: !!fresh });
    renderNeeds();
    renderSuggest();
    renderContinuing();
  }

  // "Suggest improvements": five ways to review an app (prompts.json, "lens"), each a method with a name, so that
  // participants meet more than one way of asking for a review; a pick fills the box, as any suggestion does
  function showLenses() {
    const d = document.createElement('div');
    d.className = 'msg note lenses';
    d.innerHTML = '<b>Pick a way to review your app.</b> Each asks the model for five improvements in its own way; you choose one to build.' +
      S.prompts.filter((p) => p.lens).map((p) => `<button type="button" data-lens="${p.id}"><b>${esc(p.title)}</b><span>${esc(p.blurb)}</span></button>`).join('');
    d.querySelectorAll('[data-lens]').forEach((b) => { b.onclick = () => useSuggestion(S.prompts.find((p) => p.id === b.dataset.lens)); });
    $('log').append(d);
    scrollLog();
  }

  // an exercise may name the model it runs on best (prompts.json "model", "model_note"); the participant can switch back
  function preferModel(p) {
    const m = p.model && S.config.models[p.model];
    if (!m || S.model === p.model) return;
    track('model', { from: S.model, to: p.model, by: 'exercise' });
    S.model = p.model;
    localSet('ws:model', S.model);
    $('modelSelect').value = S.model;
    renderBadge();
    note(`This exercise runs on <b>${esc(m.label)}</b> (${esc(whereOf(S.model))})${p.model_note ? ': ' + esc(p.model_note) : ''}. You can switch back in the model menu.`);
  }

  /* ---------- plan mode: a recorded planning session, then a live plan and build ---------- */

  // The planner's session for each workshop app was recorded beforehand (site/data/planning/<id>.json,
  // tools/planning/FORMAT.md). Its log streams like thinking, its looks at the data are recomputed from
  // the participant's own file, its questions come as cards, and the plan composed from the answers
  // goes on the stage. What follows is live: changes to the plan, and the build.
  const PLAN_HEAD = 'Build this app. Follow the plan below; where it says nothing, keep it simple.';
  // a free brief: the participant's own words come first, and the plan wins where the two differ
  const BRIEF_HEAD = 'Build this app. Follow my prompt and the plan; where they differ, the plan wins; where both are silent, keep it simple.';
  const BRIEF_MIN = 40, BRIEF_MAX = 4000;   // characters
  const CHANGE = 'Change the plan: ';
  const NO_MODEL = 'Changes to a plan are made live by your model, and in recorded mode no model is connected. Build the plan as it is, or ask a facilitator for a seat code.';
  const freeBrief = (p) => !!(p && S.freeBrief[p.id]);
  // what Build sends: for a free brief the brief and the plan, for the other requests the plan alone
  const buildMessage = (pl, h) => freeBrief(pl.p) ? `${BRIEF_HEAD}\n\nMy prompt:\n${pl.brief}\n\nThe plan:\n${planText(h.plan)}` : PLAN_HEAD + '\n\n' + planText(h.plan);
  // who made a plan version, in words
  const whoOf = (h) => h.by === 'you' ? 'edited by you' : h.by === 'model' ? `changed by ${h.label}` : 'the planner';
  const planPace = () => Math.max(0.2, Number(params.get('planpace')) || CFG.pace);   // seconds the notes take (120 felt slow, 3.11); ?planpace=20 for a rehearsal
  const plannable = (p) => !!(p && p.planning && S.packs[p.id] !== null);
  const defaultOf = (q) => Math.max(0, q.options.findIndex((o) => o.default));
  const plain = (s) => s.replace(/\*\*|`/g, '').replace(/^#{1,6}\s*/gm, '');
  const ICON = {
    look: '<svg viewBox="0 0 16 16"><rect x="2" y="3" width="12" height="10" rx="1.5"/><path d="M2 7h12M6 7v6"/></svg>',
    search: '<svg viewBox="0 0 16 16"><circle cx="7" cy="7" r="4.25"/><path d="m10.2 10.2 3.3 3.3"/></svg>',
    read: '<svg viewBox="0 0 16 16"><path d="M4 2h5l3 3v9H4z"/><path d="M9 2v3h3M6 9h4M6 11.5h4"/></svg>',
  };
  let shownPlan = null;   // the planning whose plan is on the stage (for its facilitator's brief)
  let shownH = null;      // the version of it that is shown

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
      S.packs[p.id] = getJSON('data/' + p.planning).then((pack) => {
        S.freeBrief[p.id] = !!pack.free_brief;
        return pack;
      }, (e) => {
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

  // the plan from the chosen answers; tools/planning.py compose() writes the same text for the bake-off.
  // opts.topic and opts.look (a look's id) fill {topic} and {look} in a free-brief pack: the topic's default and the first look without them
  function composePlan(pack, answers, opts = {}) {
    const fill = {};
    pack.questions.forEach((q) => {
      const o = q.options[answers[q.id] != null ? answers[q.id] : defaultOf(q)];
      o.fragments.forEach((f) => (fill[f.section] = fill[f.section] || []).push(f.text.trim()));
    });
    const looks = pack.looks || [], chosen = looks.find((x) => x.id === opts.look) || looks[0];
    const topic = opts.topic || pack.topic_default || 'my topic';
    // function replacements: a topic with "$&" in it stays as typed
    return pack.plan_base.replace(/\{\{([\w.-]+)\}\}/g, (m, id) => (fill[id] || []).join('\n\n'))
      .replace(/\{topic\}/g, () => topic).replace(/\{look\}/g, () => (chosen ? `${chosen.label}: ${chosen.text}` : ''));
  }
  // the look a seat starts with: a stable hash of its code (or, without a seat, of the page's session id), so the room gets a mix
  function defaultLook(pack, key = S.seatCode || Track.sid) {
    let h = 2166136261;
    for (const c of String(key)) h = Math.imul(h ^ c.charCodeAt(0), 16777619) >>> 0;
    return pack.looks[h % pack.looks.length].id;
  }
  const lookText = (pack, id) => { const l = pack.looks.find((x) => x.id === id) || pack.looks[0]; return `${l.label}: ${l.text}`; };
  window.__studioTest = { composePlan: (pack, answers, opts) => PLAN_HEAD + '\n\n' + planText(composePlan(pack, answers, opts)), defaultLook };   // for tests/e2e
  // what the participant reads and the model receives: their country in place, no runs of empty lines
  const planText = (s) => s.replace(/\{country\}/g, S.country).replace(/\n{3,}/g, '\n\n').trim();

  // a "Looked at the data" step marked live is recomputed from the participant's own file
  async function lookFacts(key) {
    const f = { country: S.country };
    if (key === 'gc') {   // paragraphs, documents (a symbol can hold several), committees and years of the loaded file
      const r = (await dataParsed('gc')).records, years = r.map((x) => x.year).filter(Boolean);
      return Object.assign(f, {
        count: fmt(r.length), documents: fmt(new Set(r.map((x) => x.symbol + '\n' + x.title)).size), committees: fmt(new Set(r.map((x) => x.committee)).size),
        years: years.length ? `${Math.min(...years)}–${Math.max(...years)}` : 'no years',
      });
    }
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
    const fill = (t) => String(t || '').replace(/\{(country|count|documents|committees|years)\}/g, (m, k) => (facts[k] != null ? facts[k] : m));
    let detail = fill(s.detail);
    if (s.live === 'uhri_overview' && facts.mechanisms) detail = [detail, facts.mechanisms].filter(Boolean).join(': ');
    const row = document.createElement('div');
    row.className = 'step';
    row.innerHTML = `<span class="step-ico" aria-hidden="true">${ICON[s.kind] || ICON.look}</span><div class="step-main">` +
      `<span class="step-label">${esc(fill(s.label))}</span>${detail ? `<span class="step-detail">${esc(detail)}</span>` : ''}<span class="step-pages"></span></div>`;
    row.plainText = '→ ' + fill(s.label) + (detail ? ': ' + detail : '');
    if (s.live === 'gc_overview') {   // the counts are the participant's own: the button shows the file they come from
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'linkish';
      b.textContent = 'Look inside the file';
      b.onclick = () => openInside('gc');
      row.querySelector('.step-pages').append(b);
    }
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
    Progress.mark(2);
    const PACE = planPace();
    const pack = await loadPack(p);
    const free = freeBrief(p);
    const field = Brief.el && Brief.el.isConnected ? Brief.topic.trim() : '';
    const pl0 = free ? { brief: text, topic: field || topicFrom(pack, text) || topicDefault(pack), look: defaultLook(pack) } : {};
    track('plan_open', free ? { prompt: p.id, brief_w: words(text), topic_w: words(pl0.topic), blocks: Brief.el && Brief.el.isConnected ? briefIncluded() : pack.brief.length } : { prompt: p.id });
    retirePlanning('Replaced by a new plan.');
    const pl = S.planning = Object.assign({ p, pack, files, fresh: S.freshNext, answers: {}, history: [], cards: [] }, pl0);
    if (free) Brief.sent(true);
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
    let stage = '', skipping = false;
    // a recorded log can be cut short: the log and its steps finish at once, the questions are still the participant's
    const nap = (ms) => skipping ? Promise.resolve() : wait(ms, signal);
    let skip = null;
    if (free) {
      skip = document.createElement('button');
      skip.type = 'button';
      skip.className = 'linkish skip-plan';
      skip.textContent = 'Skip to the plan';
      skip.onclick = () => { skipping = true; skip.remove(); };
      m.el.querySelector('.who').after(skip);
    }
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
            await nap(50);
            n = skipping ? part.length : Math.min(part.length, n + perTick);
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
          if (steps[i].live === 'gc_overview') Progress.mark(1);   // "Data": the counts of their own file are on screen
          mindShow(`${who} is planning`, where, plain(stage) + row.plainText, clock(), noteText);
          await nap(PACE * 10);
          row.classList.remove('running');
          stage += row.plainText + '\n\n';
        }
      }
      // the questions, one at a time; each answer is the participant's message
      const qs = pack.questions;
      if (skip) skip.remove();
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
      const first = composePlan(pack, pl.answers, { topic: pl.topic, look: pl.look });
      const full = planText(first);
      const ticks = Math.max(1, Math.round(PACE * 1000 / 8 / 50));
      showPlan(pl, { version: 1, by: 'planner', plan: '' });
      for (let n = 0; n < full.length;) {
        await wait(50, signal);
        n = Math.min(full.length, n + Math.ceil(full.length / ticks));
        $('planDoc').innerHTML = md(full.slice(0, n));
        $('planView').querySelector('.plan-scroll').scrollTop = 1e6;
        w.status(`Writing the plan · ${fmt(words(full.slice(0, n)))} words`);
      }
      w.status('');
      offerPlan(pl, w, pushVersion(pl, first, 'planner'));
      showPlan(pl);
      Progress.mark(3);
      w.body(md('The plan is on the right, written from your answers. Read it, then build from it or ask for a change.'));
    } catch (e) {
      mindHide();
      $('planView').hidden = true;
      if (S.planning === pl) S.planning = null;
      m.fail(e.name === 'AbortError' ? 'Stopped. Your message is back in the box.' : `The plan could not be shown (${e.message}). Your message is back in the box.`);
      if (skip) skip.remove();
      if (free) Brief.sent(false);
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
        '</div>' + (S.route.type === 'replay' ? `<p class="ask-note">${CFG.backup ? 'Recorded mode builds the app recorded beforehand from the recommended answers; the others show you their plan.' : 'Recorded mode builds only the recommended answers; the others show you their plan.'}</p>` : '');
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

  // one version of a plan, by the planner, by the participant (a direct edit or a new look) or by their model; the latest
  // is what Build sends and what a change by chat starts from
  function pushVersion(pl, plan, by, label) {
    const h = { version: pl.history.length + 1, plan, by };
    if (label) h.label = label;
    pl.history.push(h);
    save();
    return h;
  }

  // what the kicker above the plan says: who made the version shown
  function kickerOf(pl, h, latest) {
    const t = freeBrief(pl.p) ? `v${h.version} · ${whoOf(h)}`
      : h.version === 1 ? `Plan · written beforehand by ${pl.pack.planner || 'Claude Fable 5.1'}, with your answers` : `Plan v${h.version} · changed live by ${h.label || h.by}`;
    return t + (latest ? '' : ' · an earlier version');
  }

  // the plan on the stage: a document to read; its edit box (planEdit) is a separate element
  function showPlan(pl, h = pl.history[pl.history.length - 1]) {
    const latest = !pl.history.length || h === pl.history[pl.history.length - 1];
    if (pl.editing && !latest && !commitEdit(pl)) return;   // opening an older version saves an edit in progress first
    shownPlan = pl;
    shownH = h;
    $('planTitle').textContent = pl.pack.title || pl.p.title;
    $('planBrief').hidden = !pl.pack.facilitator_brief || !CFG.planBrief;   // written for Geneva's facilitators
    $('planView').hidden = false;
    renderPlanTools();
    if (pl.editing) return;   // the box stays as it was
    $('planKicker').textContent = kickerOf(pl, h, latest);
    $('planDoc').innerHTML = md(planText(h.plan));
    $('planView').querySelector('.plan-scroll').scrollTop = 0;
  }

  // the look and edit controls under the plan's title: only for a free brief, and only on the latest version, with a live model
  function renderPlanTools() {
    const pl = shownPlan, free = !!pl && freeBrief(pl.p), live = !!S.route && S.route.type !== 'replay';
    $('planTools').hidden = !free;
    if (!free) return;
    const latest = !pl.history.length || shownH === pl.history[pl.history.length - 1];
    const ready = live && !S.busy && latest && pl.history.length > 0;
    const lookReady = (live || CFG.backup) && !S.busy && latest && pl.history.length > 0;   // another look needs no model, and picks the recorded app in Geneva
    const sel = $('planLook');
    if (sel.dataset.pack !== pl.p.id) {
      sel.innerHTML = pl.pack.looks.map((l) => `<option value="${esc(l.id)}">${esc(l.label)}</option>`).join('');
      sel.dataset.pack = pl.p.id;
    }
    sel.value = pl.look;
    sel.disabled = !lookReady || !!pl.editing;
    $('planEditBtn').hidden = !!pl.editing;
    $('planEditBtn').disabled = !ready;
    $('planDone').hidden = $('planCancel').hidden = !pl.editing;
    $('planDone').disabled = $('planCancel').disabled = S.busy;
    $('planNote').hidden = live;
    $('planNote').textContent = live ? '' : CFG.backup ? NO_MODEL + ' ' + RECORDED_NOTE : NO_MODEL;
    const hl = $('planHl');
    hl.hidden = !CFG.highlights;
    if (CFG.highlights) {
      hl.replaceChildren(...highlightRow(pl, false).childNodes);
      hl.querySelectorAll('button').forEach((b) => { b.disabled = !ready || !!pl.editing; });
    }
  }

  // Edit the plan: the rendered plan gives way to its Markdown in a box, for the participant's own words
  function beginEdit(pl) {
    if (S.planning !== pl || S.busy || pl.editing || S.route.type === 'replay') return;
    const h = pl.history[pl.history.length - 1];
    pl.editing = true;
    showPlan(pl, h);
    $('planEdit').value = planText(h.plan);
    $('planEditMsg').hidden = true;
    $('planDoc').hidden = true;
    $('planEdit').hidden = false;
    $('planScroll').classList.add('editing');
    $('planKicker').textContent = `v${h.version} · editing`;
    renderPlanTools();
    $('planEdit').focus();
    $('planEdit').setSelectionRange(0, 0);   // from the top: some browsers put the cursor, and the view, at the end
    $('planEdit').scrollTop = 0;
  }

  function endEdit(pl) {
    pl.editing = false;
    $('planEdit').hidden = true;
    $('planEditMsg').hidden = true;
    $('planDoc').hidden = false;
    $('planScroll').classList.remove('editing');
  }

  function cancelEdit(pl) {
    if (!pl.editing) return;
    endEdit(pl);
    showPlan(pl);
  }

  // Done, or anything that goes on from the plan (Build, a change by chat, an older version): true when the edit is saved or there was none.
  // A changed text becomes a new version by "you"; it must still start with a heading, or the box stays open.
  function commitEdit(pl) {
    if (!pl.editing) return true;
    const text = $('planEdit').value.trim(), h = pl.history[pl.history.length - 1];
    if (text === planText(h.plan)) { cancelEdit(pl); return true; }
    if (!text.startsWith('#')) {
      $('planEditMsg').hidden = false;
      $('planEditMsg').textContent = 'A plan starts with a # heading line. Put one back at the top, or choose Cancel to keep the plan as it was.';
      shownPlan = pl;
      $('planView').hidden = false;
      $('planEdit').focus();
      return false;
    }
    endEdit(pl);
    const next = pushVersion(pl, text, 'you');
    track('plan_edit', { prompt: pl.p.id, plan_v: next.version, words: words(text) });
    const m = planMsg('Your edit');
    m.body(md(`Plan v${next.version} is on the right, with your edits.`));
    offerPlan(pl, m, next);
    showPlan(pl);
    return true;
  }

  // another look: the plan's Look line changes and the rest stays as it is, whoever wrote it; a new version by "you"
  function changeLook(pl, id) {
    if (S.planning !== pl || S.busy || id === pl.look || pl.editing) { renderPlanTools(); return; }
    const h = pl.history[pl.history.length - 1], was = lookText(pl.pack, pl.look), now = lookText(pl.pack, id);
    let plan = h.plan;
    if (plan.includes(was)) plan = plan.replace(was, () => now);
    else if (/^## Look\b/m.test(plan)) plan = plan.replace(/(^## Look\b[^\n]*\n+)[\s\S]*?(?=\n## |$(?![\s\S]))/m, (m, head) => head + now + '\n');   // the line was edited: its section is replaced
    else plan = plan.trimEnd() + `\n\n## Look\n\n${now}\n`;
    pl.look = id;
    track('plan_look', { look: id });
    const next = pushVersion(pl, plan, 'you');
    const m = planMsg('Your edit');
    m.body(md(`Plan v${next.version} is on the right, with the look changed to **${pl.pack.looks.find((l) => l.id === id).label}**.`));
    offerPlan(pl, m, next);
    showPlan(pl);
  }

  function showBrief(pl) {
    openDrawer("Facilitator's brief");
    $('drawerBody').innerHTML = '<p>Your request was a sentence or two. Before the workshop, the facilitator also gave the planner this brief, and it shaped the plan. ' +
      'So the planner had your words, this brief, your data and the reference shelf: nothing else.</p>' +
      `<div class="brief answer-md">${md(pl.pack.facilitator_brief)}</div>`;
  }

  // under a finished plan: the plan as a card that opens on the stage, then Build or Change
  function offerPlan(pl, m, h) {
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
    S.savedPlan = null;
    if (!S.planning) return;
    S.planning.cards.forEach((c) => c.retire(why));
    if (S.planning.editing) endEdit(S.planning);
    S.planning = null;
    $('planView').hidden = true;
    save();   // a plan that was built or replaced is not kept
  }

  function buildFromPlan(pl) {
    if (S.planning !== pl || S.busy) return;
    if (!commitEdit(pl)) return;   // an edit in progress is saved first, and is what gets built
    const h = pl.history[pl.history.length - 1];
    track('plan_build', { prompt: pl.p.id, changed: pl.pack.questions.filter((q) => pl.answers[q.id] !== defaultOf(q)).length, plan_v: h.version, by: h.by, look: pl.look || null });
    if (!CFG.backup && S.route.type === 'replay' && (h.version > 1 || pl.pack.questions.some((q) => pl.answers[q.id] !== defaultOf(q)))) {
      note('Recorded mode can build only the plan with the recommended answers: that is the plan the recorded app was built from. ' +
        'Your plan stays on the right to read. To build it, ask a facilitator for a seat code, or start this app again and keep the recommended answers.');
      return;
    }
    if (recordedNow()) note(RECORDED_NOTE);   // Geneva: it never refuses; the recorded app of the plan's look is played
    Progress.mark(4);
    pl.changing = false;
    const text = buildMessage(pl, h);
    Object.assign(S, { pendingPromptId: pl.p.id, pendingText: text, freshNext: pl.fresh });
    pl.building = true;
    if (!submitBuild(text, pl)) pl.building = false;
  }

  function changePlan(pl) {
    if (S.planning !== pl || S.busy) return;
    if (S.route.type === 'replay') {
      note(NO_MODEL);
      if (CFG.highlights) { highlightRow(pl, true); scrollLog(); }   // the examples, switched off
      return;
    }
    if (!commitEdit(pl)) return;
    pl.changing = true;
    openComposer(CHANGE);
    $('input').setSelectionRange(CHANGE.length, CHANGE.length);
    if (CFG.highlights) { highlightRow(pl, true); scrollLog(); }
  }

  // "What would you like to highlight?": three examples that put a change into the box, to be edited before it is sent
  const HIGHLIGHTS = [
    ['Languages', 'add a short note in French and Spanish explaining how to search, for colleagues who work in those languages (the paragraphs stay in English).'],
    ['Accessibility (WCAG 2.2)', 'make the app fully usable with a keyboard, with strong contrast and larger text.'],
    ['Something else', ''],
  ];
  // the row: a card in the chat (after Change something), or the line in the plan's tools (inline)
  function highlightRow(pl, card) {
    const live = !!S.route && S.route.type !== 'replay';
    const row = document.createElement('div');
    row.className = card ? 'msg hl-card' : 'plan-hl';
    row.innerHTML = '<span class="hl-q">What would you like to highlight? For example:</span><span class="hl-btns">' +
      HIGHLIGHTS.map(([l]) => `<button type="button" class="ghost hl-btn">${esc(l)}</button>`).join('') + '</span>';
    row.querySelectorAll('button').forEach((b, i) => {
      b.disabled = !live;
      b.onclick = () => {
        if (S.planning !== pl || S.busy || !commitEdit(pl)) return;
        pl.changing = true;
        const t = CHANGE + HIGHLIGHTS[i][1];
        openComposer(t);
        $('input').setSelectionRange(t.length, t.length);
      };
    });
    if (card) { document.querySelectorAll('#log .hl-card').forEach((e) => e.remove()); $('log').append(row); }
    return row;
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
    const mine = freeBrief(pl.p) ? `My prompt:\n${pl.brief}\n\n` + (h.by === 'you' ? 'I edited this plan myself; keep my edits and change only what I ask.\n\n' : '') : '';
    const content = `Here is the plan for an app I am about to build (version ${h.version}):\n\n${planText(h.plan)}\n\n${mine}${text}\n\n` +
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
          $('planKicker').textContent = freeBrief(pl.p) ? `v${h.version + 1} · being changed by ${label}` : `Plan v${h.version + 1} · being changed live by ${label}`;
          $('planDoc').innerHTML = md(plan);
        },
      });
      addTrace({ purpose: 'build', usage, messages, userText: text, shelf: hits, plan: h });
      if (usage.budget_left != null) setBudget(usage.budget_left);
      if (seg) seg.close();
      m.status('');
      const plan = planOf(reply);
      if (!plan) {   // an answer without a plan: the plan, and its Build button above, stay as they were
        track('plan_revise', { prompt: pl.p.id, plan_v: h.version, ok: false });
        m.body(md((reply.trim() || 'The model sent back nothing.') + '\n\n*The plan is unchanged.*'));
        showPlan(pl, h);
        return;
      }
      const next = pushVersion(pl, plan, 'model', label);
      track('plan_revise', { prompt: pl.p.id, plan_v: next.version, ok: true });
      m.body(md(`Plan v${next.version} is on the right, with your change.`));
      offerPlan(pl, m, next);
      showPlan(pl);
    } catch (e) {
      if (seg) seg.close();
      m.status('');
      track('plan_revise', { prompt: pl.p.id, plan_v: h.version, ok: false });
      m.fail(friendly(e));
      pl.changing = true;
      openComposer(text);
      showPlan(pl, h);
    } finally {
      mindHide();
      setBusy(false);
    }
  }


  /* ---------- the brief card: the participant writes a brief from labelled paragraphs (a pack with free_brief) ---------- */

  // The card is a helper for the message box, not a lock: whatever is changed on it is copied into the box as the brief,
  // and the box can still be edited by hand. Sending the box starts the recorded planning, whatever it says.
  const Brief = {
    el: null, pack: null, p: null, loading: false, failed: false, attached: false,
    topic: '', on: {}, text: {},
  };
  const briefIncluded = () => Brief.pack.brief.filter((b) => Brief.on[b.id]).length;
  // "[my topic]" is the participant's topic, or stays as it is while the topic is empty
  const briefText = () => Brief.pack.brief.filter((b) => Brief.on[b.id]).map((b) => `${b.label}\n${Brief.text[b.id].trim()}`).join('\n\n')
    .replace(/\[my topic\]/g, () => Brief.topic.trim() || '[my topic]');
  const growBox = (t) => { t.style.height = 'auto'; t.style.height = t.scrollHeight + 2 + 'px'; };
  // the pack names a default topic, or the plan says "my topic"
  const topicDefault = (pack) => pack.topic_default || 'my topic';
  const escRe = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

  // the topic the participant wrote in place of "[my topic]", read back from the brief when its field is empty
  function topicFrom(pack, text) {
    for (const b of pack.brief) {
      const [a, c] = b.text.split('[my topic]');
      if (c === undefined) continue;
      const m = new RegExp(escRe(a.slice(-24)) + '([^\\n]{2,120}?)' + escRe(c.slice(0, 24))).exec(text);
      if (m && m[1].trim() && m[1].trim() !== '[my topic]') return m[1].trim();
    }
    return '';
  }

  // a course that looks at the data first: a card on the request's file, before the brief. "Look inside the file" opens
  // the records; it, "Write your brief" or the Data step done or skipped brings the brief card under it.
  const DataCard = { el: null, next: null };
  function offerData(p) {
    if (DataCard.el && DataCard.el.isConnected) return;
    const el = DataCard.el = document.createElement('div');
    el.className = 'msg data-card';
    el.innerHTML = '<b>First, your data</b>' + `<span class="bsum">${esc(fileLabel(p.dataset))}</span>` +
      '<p class="dc-facts">Counting the file…</p>' +
      '<p>One record per paragraph: the document symbol, the paragraph number, the committee, the year and the text, word for word. ' +
      'Look at a few records before you say what to build from them.</p>' +
      '<div class="row"><button type="button" class="primary" id="dataLook">Look inside the file</button>' +
      '<button type="button" class="ghost" id="dataNext">Write your prompt</button></div>';
    $('log').append(el);
    lookFacts(p.dataset).then((f) => {
      if (f.count) el.querySelector('.dc-facts').innerHTML = `<b>${esc(f.count)} paragraphs</b> from ${esc(f.documents)} documents of ${esc(f.committees)} committees, ${esc(f.years)}.`;
    }, () => { el.querySelector('.dc-facts').textContent = ''; });
    DataCard.next = () => {
      if (!el.isConnected) return;
      el.querySelector('#dataNext').hidden = true;
      offerBrief(p);
    };
    el.querySelector('#dataLook').onclick = () => { openInside(p.dataset); DataCard.next(); };
    el.querySelector('#dataNext').onclick = () => DataCard.next();
    if (S.progress.done[0]) DataCard.next();   // back after a reload, with the data already looked at
  }

  // the card in the chat; created once, where a suggestion would have offered the request
  function offerBrief(p) {
    if (Brief.loading || (Brief.el && Brief.el.isConnected)) return;
    Brief.loading = true;
    loadPack(p).then((pack) => {
      Brief.loading = false;
      if (!pack.free_brief || (Brief.el && Brief.el.isConnected) || S.planning || S.versions.length) { Brief.failed = !pack.free_brief; return; }
      Object.assign(Brief, { pack, p, topic: '', attached: false, on: {}, text: {} });
      pack.brief.forEach((b) => { Brief.on[b.id] = true; Brief.text[b.id] = b.text; });
      const el = Brief.el = document.createElement('details');
      el.className = 'msg brief-card';
      el.open = true;
      el.innerHTML = '<summary><b>Write your prompt</b><span class="bsum">1. Name your topic. 2. Read the five paragraphs; change or switch off any. 3. Press Send.</span></summary>' +
        '<div class="brief-body"><label class="brief-topic"><span>My topic</span>' +
        `<input type="text" id="briefTopic" maxlength="120" autocomplete="off" placeholder="${esc(pack.topic_default || 'e.g. freedom of expression online')}"></label>` +
        pack.brief.map((b) => `<div class="brief-block" data-id="${esc(b.id)}"><label class="brief-lab"><input type="checkbox" checked><span>${esc(b.label)}</span></label>` +
          `<textarea rows="2" aria-label="${esc(b.label)}"></textarea><small class="brief-asks">${esc(b.asks || '')}</small></div>`).join('') +
        '<p class="brief-hint">What you write here appears in the message box below. Send it when it says what you want.</p></div>';
      el.querySelectorAll('textarea').forEach((t, i) => { t.value = Brief.text[pack.brief[i].id]; });
      $('log').append(el);
      el.querySelectorAll('textarea').forEach(growBox);
      el.addEventListener('input', (e) => {
        const blk = e.target.closest('.brief-block');
        if (e.target.id === 'briefTopic') Brief.topic = e.target.value;
        else if (blk && e.target.tagName === 'TEXTAREA') { Brief.text[blk.dataset.id] = e.target.value; growBox(e.target); }
        else return;
        briefFill();
      });
      el.addEventListener('change', (e) => {
        const blk = e.target.closest('.brief-block');
        if (!blk || e.target.type !== 'checkbox') return;
        Brief.on[blk.dataset.id] = e.target.checked;
        blk.classList.toggle('off', !e.target.checked);
        briefFill();
      });
      briefFill();
      el.scrollIntoView({ block: 'start' });   // from its first line, not its last
    }, () => { Brief.loading = false; Brief.failed = true; renderSuggest(); });   // no pack: the suggestion is offered as before
  }

  // the brief goes into the message box, and the box is the request that sending will plan; the file it names comes along once
  function briefFill() {
    const text = briefText();
    S.planMode = true;
    $('input').value = text;
    fitInput(112);   // the card is where it is read; the box shows the first lines of what will be sent
    Object.assign(S, { pendingPromptId: Brief.p.id, pendingText: text, freshNext: false });
    if (!Brief.attached) {
      Brief.attached = true;
      if (Brief.p.dataset) S.draft.add(Brief.p.dataset);
      renderAttach();
      renderShelfState();
    }
    renderNeeds();
    renderPlanMode();
    renderContinuing();
  }

  // once sent, the card folds up and stops taking changes (it scrolls away with the chat); if the plan fails, it opens again
  Brief.sent = (on) => {
    if (!Brief.el) return;
    Brief.el.classList.toggle('sent', on);
    Brief.el.querySelector('.brief-body').inert = on;
    Brief.el.querySelector('.bsum').textContent = on ? 'Sent. Open it to read it again.' : '1. Name your topic. 2. Read the five paragraphs; change or switch off any. 3. Press Send.';
    Brief.el.querySelector('summary b').textContent = on ? 'Your prompt' : 'Write your prompt';
    Brief.el.open = !on;
  };

  // picking up a plan after a reload: its latest version goes back on the stage with Build and Edit (no replay)
  async function resumePlan(d) {
    const p = S.prompts.find((q) => q.id === d.promptId);
    let pack;
    try { pack = p && await loadPack(p); } catch (e) { pack = null; }
    if (!pack || !pack.free_brief || S.planning) { S.savedPlan = null; renderSuggest(); return; }   // nothing to put back: the card is offered
    const pl = S.planning = { p, pack, files: d.files, fresh: false, answers: d.answers, history: d.history, cards: [], brief: d.brief, topic: d.topic, look: d.look };
    S.savedPlan = null;
    const m = planMsg(`${pack.planner || 'Claude Fable 5.1'} · Plan mode`);
    m.body(md('Your plan is back on the right, as you left it. Read it, then build from it, edit it or ask for a change.'));
    offerPlan(pl, m, d.history[d.history.length - 1]);
    showPlan(pl);
    renderSuggest();
  }

  // a saved plan, checked: a free brief with its versions
  function planFrom(d) {
    const ok = d && typeof d.promptId === 'string' && typeof d.brief === 'string' && typeof d.topic === 'string' && typeof d.look === 'string' &&
      Array.isArray(d.files) && d.files.every((k) => typeof k === 'string') && d.answers && typeof d.answers === 'object' &&
      Array.isArray(d.history) && d.history.length > 0 && d.history.every((h, i) => h && h.version === i + 1 && typeof h.plan === 'string' && ['planner', 'you', 'model'].includes(h.by));
    return ok ? d : null;
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
  function fitInput(max = window.innerHeight * 0.4) {
    const t = $('input');
    t.style.height = 'auto';
    t.style.height = Math.min(t.scrollHeight + 2, max) + 'px';
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
    const mine = (p) => sessionOf(p) === S.session && !p.hidden && p.id !== S.pendingPromptId && !(S.planning && S.planning.p.id === p.id) && (S.advanced || p.level !== 'advanced' || CFG.ignoreLevel);   // where the course picks the requests, Advanced does not
    // Hick's law: a few suggestions at a time, never the whole list
    // a next step continues this app; it may bring a file of its own (a second document to add)
    // a step with no recorded answer (prompts.json "live_only") is offered only when a model is on the line
    const next = v ? S.prompts.filter((p) => mine(p) && p.builds_on && p.builds_on !== 'any' && !used.has(p.id) && used.has(p.builds_on) && (live || !p.live_only)).slice(0, 2) : [];
    // "Suggest improvements" (or, where the course has them, "Suggest three improvements": its request is Geneva's)
    if (v && (live || CFG.backup)) next.push(...S.prompts.filter((p) => p.builds_on === 'any' && !p.lens && !p.geneva === !CFG.ideas && p.id !== S.pendingPromptId && (S.advanced || p.level !== 'advanced')));
    // Hick's law: Session 8 keeps its three apps in view (PDF, Verbatim finder, wiki); Session 7 has one
    let starters = S.prompts.filter((p) => mine(p) && !p.builds_on && !built.has(p.id) && (live || !p.live_only)).slice(0, !v || S.session !== 'S7' ? 3 : 1);
    // a course that has the participant write a brief shows its card in the chat, not the suggestion, before the first app
    if (CFG.briefCard && !v && !S.versions.length && !S.planning && !S.savedPlan && !Brief.failed) {
      const b = starters.find((p) => p.planning);
      if (b) { starters = starters.filter((p) => p !== b); if (CFG.dataFirst) offerData(b); else offerBrief(b); }
    }
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
    if (S.freshNext && v) { el.hidden = false; el.textContent = 'Starts a new app. Your versions stay in the version menu above the preview.'; return; }
    if (v && v.n !== S.versions.length) { el.hidden = false; el.textContent = `Your next message continues from v${v.n}.`; return; }
    el.hidden = true;
  }

  // what a participant can see grows with what they have done (Hick's law)
  function renderTools() {
    const has = S.versions.length > 0;
    const s8 = CFG.askDirect && S.session !== 'S7';   // the later sessions of the two courses that have them: Ask directly
    $('toolbar').hidden = !has;
    $('ask3Btn').hidden = !s8 || !S.route || S.route.type === 'replay';
    $('countryChip').hidden = !countryUsed();
    const noWall = recordedNow();   // Geneva, recorded: the wall is the server's; the button stays, switched off, with the reason
    $('wallBtn').hidden = !(S.route && S.route.type === 'server') && !noWall;
    $('traceSoFar').hidden = !S.trace.length;   // the count sits on the item it counts, not on the menu (it read as a to-do)
    ['downloadBtn', 'wallBtn', 'lookBtn'].forEach((id) => { $(id).disabled = !has; });
    if (CFG.backup) {
      const sub = $('wallBtn').querySelector('span');
      if (!S.wallHint) S.wallHint = sub.textContent;
      $('wallBtn').disabled = !has || noWall;
      sub.textContent = noWall ? "The wall needs the studio's server; in recorded mode your app stays here." : S.wallHint;
    }
  }

  function renderSession() {
    document.querySelectorAll('#sessionSwitch button').forEach((b) => b.setAttribute('aria-selected', b.dataset.session === S.session));
    document.body.classList.toggle('own-ok', ownAllowed());
  }

  function setSession(s) {
    if (s === S.session || S.busy) return;
    track('session', { to: s });
    loadSession(s);
    const n = CFG.sessions.indexOf(s) + 1;
    note(`<b>Session ${n}.</b> ` + (S.versions.length || S.talk.length ? 'Your conversation in this session, as you left it.'
      : 'A new conversation, with its own suggestions below. What you built in another session stays there.') +
      (s === 'S8' ? ' <b>Look inside</b> now also lets you ask the model directly.' : ''));
  }

  // each session is a conversation of its own: its chat, its apps and its record of what left this laptop; the
  // others wait in this browser under their own keys
  function loadSession(s) {
    save();
    S.session = s;
    localSet('ws:session', s);
    Object.assign(S, { versions: [], current: null, talk: [], trace: [], planning: null, pendingPromptId: null, pendingText: '', freshNext: false, draftImages: [] });
    S.draft.clear();
    restore();   // also brings back this session's progress
    $('input').value = '';
    fitInput();
    $('planView').hidden = true;
    $('appError').hidden = true;
    $('drawer').hidden = true;
    setView('app');
    if (!S.versions.length) { Preview.clear(); $('empty').hidden = false; }
    renderSession();
    renderAttach();
    renderNeeds();
    renderAll();
  }

  // Hick's law for versions: one button names the app and the version on the stage, arrows step to the next or the
  // one before; the full list, grouped by app with one line on each version, is one click away
  const rootOf = (v) => { let r = v; while (r && r.parent) r = S.versions.find((x) => x.n === r.parent) || null; return r || v; };
  const versionLine = (v) => {
    const s = (v.summary || v.user || '').replace(/\s+/g, ' ').trim();
    return (s.length > 80 ? s.slice(0, 78).replace(/\s+\S*$/, '') + '…' : s) || 'no description';
  };
  const appName = (v) => {
    const p = S.prompts.find((q) => q.id === rootOf(v).promptId);
    return p ? p.title : titleOf(v.html);
  };

  async function goToVersion(n) {
    const v = S.versions.find((x) => x.n === n);
    if (!v || S.busy) return;
    S.current = v.n;
    S.freshNext = false;
    renderVersions();
    renderSuggest();
    await showVersion(v);
    save();
  }

  function renderVersions() {
    const box = $('versions');
    box.innerHTML = '';
    if (!S.versions.length) { renderTools(); return; }
    const cur = currentVersion() || S.versions[S.versions.length - 1];
    const i = S.versions.indexOf(cur);
    const groups = [];
    S.versions.forEach((v) => {
      const r = rootOf(v).n;
      let g = groups.find((x) => x.root === r);
      if (!g) groups.push(g = { root: r, name: appName(v), items: [] });
      g.items.push(v);
    });
    box.innerHTML =
      `<button type="button" class="vnav" data-dir="-1" aria-label="The version before"${i <= 0 ? ' disabled' : ''}>‹</button>` +
      `<button type="button" class="vcur" aria-haspopup="menu" aria-expanded="false" title="All versions">` +
      `<span class="vapp">${esc(appName(cur))}</span> <b>v${cur.n}</b><span class="vof"> of ${S.versions.length}</span> ▾</button>` +
      `<button type="button" class="vnav" data-dir="1" aria-label="The next version"${i >= S.versions.length - 1 ? ' disabled' : ''}>›</button>` +
      `<div class="vmenu" role="menu" hidden>${groups.map((g) => `<div class="vgroup"><div class="vglab">${esc(g.name)}</div>` +
        g.items.map((v) => `<button type="button" role="menuitemradio" data-v="${v.n}" aria-checked="${v.n === cur.n}">` +
          `<b>v${v.n}</b><span>${esc(versionLine(v))}</span><i>${esc(v.label || '')}${v.edit ? ' · a change' : ''}</i></button>`).join('') + '</div>').join('')}</div>`;
    const menu = box.querySelector('.vmenu'), btn = box.querySelector('.vcur');
    const close = () => { menu.hidden = true; btn.setAttribute('aria-expanded', 'false'); };
    btn.onclick = (e) => {
      e.stopPropagation();
      menu.hidden = !menu.hidden;
      btn.setAttribute('aria-expanded', String(!menu.hidden));
      if (!menu.hidden) { const on = menu.querySelector('[aria-checked=true]'); if (on) on.focus(); }
    };
    box.querySelectorAll('.vnav').forEach((b) => { b.onclick = () => goToVersion(S.versions[i + Number(b.dataset.dir)].n); });
    menu.querySelectorAll('[data-v]').forEach((b) => { b.onclick = () => { close(); goToVersion(Number(b.dataset.v)); }; });
    menu.addEventListener('keydown', (e) => {
      const items = [...menu.querySelectorAll('[data-v]')], k = items.indexOf(document.activeElement);
      if (e.key === 'Escape') { close(); btn.focus(); }
      else if (e.key === 'ArrowDown') { e.preventDefault(); items[Math.min(items.length - 1, k + 1)].focus(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); items[Math.max(0, k - 1)].focus(); }
    });
    document.addEventListener('click', (e) => { if (!box.contains(e.target)) close(); }, { once: true });
    renderTools();
  }

  function setAdvanced(on, said) {
    S.advanced = on;
    localSet('ws:advanced', on ? '1' : '0');
    document.body.classList.toggle('basic', !on);
    document.body.classList.toggle('own-ok', ownAllowed());
    $('advBtn').textContent = on ? 'Advanced: on' : 'Advanced: off';
    $('advBtn').setAttribute('aria-pressed', String(on));
    if (S.ready) { renderSuggest(); renderShelf(); renderTools(); }
    if (said) {
      track('advanced', { on });
      note(on ? '<b>Advanced</b> is on: more requests in the suggestions, your own files on the shelf, Plan mode on or off, <b>New tab</b> and <b>Send to wall</b>.'
        : '<b>Advanced</b> is off: one path through the exercises.');
    }
  }

  function renderModelMenu() {
    const sel = $('modelSelect');
    sel.innerHTML = S.config.model_groups.map((g) => ({ label: g.label, ids: g.ids.filter(modelAllowed) })).filter((g) => g.ids.length).map((g) =>
      `<optgroup label="${esc(g.label)}">${g.ids.map((id) => `<option value="${id}">${esc(S.config.models[id].label)}</option>`).join('')}</optgroup>`).join('');
    sel.value = S.model;
    renderBadge();
  }

  function renderBadge() {
    const m = S.config.models[S.model];
    $('modelBadge').innerHTML = `Made in <b>${esc(m.origin)}</b> · runs in <b>${esc(m.host_region)}</b>`;
    $('modelBadge').title = `${m.label} by ${m.maker}, made in ${m.origin}. Runs on ${m.host}: ${m.host_note}. ` +
      (m.zdr === false ? 'No zero data retention: the host keeps requests for a limited time. ' : 'Zero data retention: the host may not keep what is sent. ') + `Price: ${m.price}.`;
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
    Progress.render();
    const v = currentVersion();
    if (v) showVersion(v);
  }

  /* ---------- the file shelf ---------- */

  function fileMetaLine(key) {
    const d = S.index.datasets[key];
    if (key === 'library' || key === 'pdfs') return `${fmt(d.count)} PDFs · passage by passage, with pages`;
    if (key === 'hrc_all' || key === 'un_hr_all') return `${fmt(d.count)} texts · opens in Excel`;
    if (key === 'wiki') return `${fmt(d.count)} pages · every quotation verified`;
    if (key === 'uhri') return `${fmt(S.countryCount)} records · opens in Excel`;
    if (key === 'gc') return `${fmt(d.count)} paragraphs · opens in Excel`;
    if (key === 'hrc') return `${fmt(d.count)} recorded votes · opens in Excel`;
    if (key === 'pdf_ten') return `${fmt(d.count)} documents · their PDFs open on the UN's site`;
    if (S.own[key]) {
      const s = S.own[key].shape;
      const kb = S.own[key].size / 1024;
      return `${fmt(s.count)} ${S.own[key].kind === 'docx' ? 'paragraphs' : 'records'} · ${fmt(s.fields.length)} fields · ${kb < 1 ? 'under 1' : fmt(Math.round(kb))} KB`;
    }
    return `${fmt(d.count)} pages · opens in your browser`;
  }

  // the shelf lives on the empty stage before the first app, and in the Your files drawer after it;
  // the participant's own files follow the workshop's, then the card that adds one
  function renderShelf(box = $('shelf')) {
    const own = Object.values(S.own).sort((a, b) => a.key.localeCompare(b.key, 'en', { numeric: true }));
    const keep = sessionFiles();   // Venice: only the files of this session's requests
    box.innerHTML = S.config.files.filter((f) => (keep ? keep.has(f.key) : !f.venice)).map((f) => `
      <div class="fcard" draggable="true" data-key="${f.key}">
        <div class="fcard-top"><i class="ficon ${f.kind}">${f.kind.toUpperCase()}</i><h3>${esc(fileLabel(f.key))}</h3></div>
        <p>${esc(f.blurb.replace(/\{country\}/g, S.country))}</p>
        <div class="meta">${esc(fileMetaLine(f.key))}</div>
        ${f.from ? `<p class="from">Also published as data: ${f.from.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener"${/\.json$/.test(l.url) ? ` data-json="${esc(l.url)}"` : ''}>${l.icon ? `<span class="from-icon" aria-hidden="true">${esc(l.icon)}</span>` : ''}${esc(l.label)}</a>`).join(' · ')}</p>` : ''}
        <div class="row"><button type="button" class="ghost" data-act="open">Open</button><button type="button" class="ghost" data-act="add">Add to chat</button></div>
      </div>`).join('') + own.map((e) => `
      <div class="fcard own adv" draggable="true" data-key="${e.key}">
        <div class="fcard-top"><i class="ficon ${e.kind}">${e.kind.toUpperCase()}</i><h3>${esc(e.name)}</h3></div>
        <p>Your own file, kept in this browser. Your app gets all of it; the model gets its field names and their types.</p>
        <div class="meta">${esc(fileMetaLine(e.key))}</div>
        <label class="own-samples"><input type="checkbox" data-act="samples"${e.samples ? ' checked' : ''}> Also send its first ${OwnFiles.SAMPLES} records to the model</label>
        <div class="row"><button type="button" class="ghost" data-act="open">Open</button><button type="button" class="ghost" data-act="add">Add to chat</button><button type="button" class="ghost" data-act="remove">Remove</button></div>
      </div>`).join('') + `
      <div class="fcard add-own adv">
        <div class="fcard-top"><i class="ficon own">+</i><h3>Your own file</h3></div>
        <p>A spreadsheet, an Excel workbook, a data file or a Word document from your computer. It stays in this browser: the model sees only its field names, unless you choose to send a few records.</p>
        <div class="meta">.csv · .xlsx · .json · .docx · up to 10 MB · or drop it here</div>
        <div class="row"><button type="button" class="ghost" data-act="pick">Choose a file</button></div>
      </div>`;
    box.querySelector('.add-own [data-act=pick]').onclick = pickOwnFile;
    box.querySelectorAll('a[data-json]').forEach((a) => { a.onclick = (e) => { e.preventDefault(); showJson(a.dataset.json, a.textContent); }; });
    box.querySelectorAll('.fcard[data-key]').forEach((c) => {
      const key = c.dataset.key;
      c.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/x-studio-file', key);
        e.dataTransfer.setData('text/plain', fileLabel(key));
        e.dataTransfer.effectAllowed = 'copy';
      });
      c.querySelector('[data-act=open]').onclick = () => openFile(key);
      c.querySelector('[data-act=add]').onclick = () => addFile(key);
      if (!S.own[key]) return;
      c.querySelector('[data-act=samples]').onchange = (e) => { S.own[key].samples = e.target.checked; OwnFiles.put(S.own[key]); track('own_samples', { on: e.target.checked }); };
      c.querySelector('[data-act=remove]').onclick = () => removeOwn(key);
    });
    renderShelfState();
  }

  /* ---------- the participant's own files (own-files.js) ---------- */

  function pickOwnFile() {
    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    input.accept = '.csv,.tsv,.txt,.json,.xlsx,.docx';
    input.id = 'ownFileInput';
    input.hidden = true;
    input.onchange = () => { addOwnFiles(input.files, false); input.remove(); };
    document.body.append(input);
    input.click();
  }

  // a key is never used twice, even after its file was removed: older apps keep pointing at the file they read
  function nextOwnKey() {
    const used = [...Object.keys(S.own), ...S.versions.flatMap((v) => v.files || []), ...S.talk.flatMap((x) => x.files || [])];
    return 'own_' + (Math.max(0, ...used.map((k) => (/^own_(\d+)$/.exec(k) || [0, 0])[1]).map(Number)) + 1);
  }

  async function addOwnFiles(list, attach) {
    const added = [];
    for (const file of [...list]) {
      try {
        const e = await OwnFiles.read(file, nextOwnKey());
        S.own[e.key] = e;
        await OwnFiles.put(e);
        added.push(e);
        track('own_file', { kind: e.kind, kb: Math.round(e.size / 1024), records: e.shape.count });
        if (attach) addFile(e.key);
      } catch (err) {
        note(esc(err.message || String(err)));
      }
    }
    if (added.length) {
      note(added.map((e) => `<b>${esc(e.name)}</b> (${esc(fileMetaLine(e.key))})`).join(', ') + ` ${added.length > 1 ? 'are' : 'is'} on your shelf, ` +
        `kept in this browser. In the chat, the model gets the field names and their types, not the values; tick the box on a file's card to send its first ${OwnFiles.SAMPLES} records too.`);
    }
    renderShelf();
    if ($('drawerShelf')) renderShelf($('drawerShelf'));
  }

  // a course with its own data (Poznań): the files go onto the shelf by themselves, once per browser, with their first records
  // sent to the model; before the first app they are attached and the course's request waits in the chat box
  async function preloadCourseFiles() {
    for (const [url, name] of CFG.preload) {
      let e = Object.values(S.own).find((x) => x.name === name);
      if (!e) {
        try {
          const blob = await (await fetch(url, { cache: 'no-store' })).blob();
          e = await OwnFiles.read(new File([blob], name, { type: 'application/json' }), nextOwnKey());
          e.samples = true;
          S.own[e.key] = e;
          await OwnFiles.put(e);
        } catch (err) { note(esc(name + ': ' + (err.message || err))); continue; }
      }
      if (!S.versions.length) S.draft.add(e.key);
    }
    renderAttach(); renderNeeds(); renderShelf(); renderShelfState();
    if (!S.versions.length && !$('input').value && CFG.request) {   // the cursor waits after "Życzenie z sali:"
      const t = $('input'); t.value = CFG.request; fitInput(); t.focus(); t.setSelectionRange(t.value.length, t.value.length); t.scrollTop = t.scrollHeight; }
  }

  // Poznań: "Nowa rozmowa" (an empty chat and an empty stage; the data and the request come back by themselves) and
  // "Na telefony (QR)": the app on the stage goes to the server's wall, and poznan.html shows the newest one on phones,
  // behind one fixed QR code (data/poznan/qr.svg), with the same data files from data/poznan/
  function phonesButtons() {
    const at = document.querySelector('a.top-link[href="gallery/"]');
    const mk = (label, title, fn) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'top-link'; b.textContent = label; b.title = title; b.onclick = fn;
      at.before(b);
    };
    mk('Nowa rozmowa', 'Pusty czat i pusty podgląd; dane i polecenie wracają same', () => {
      if (!confirm('Zacząć nową rozmowę? Obecny czat i aplikacja znikną z tej przeglądarki.')) return;
      clearWork();
      location.reload();
    });
    mk('Na telefony (QR)', 'Wyślij aplikację z podglądu na telefony i pokaż kod QR', sendToPhones);
  }

  async function sendToPhones() {
    const v = currentVersion();
    if (!v) { note('Najpierw zbuduj aplikację: wtedy trafi na telefony.'); return; }
    const files = [...new Set(chainOf(v).flatMap((x) => x.files || []))];
    const names = Object.fromEntries(files.filter((k) => S.own[k]).map((k) => [k, S.own[k].name]));
    try {
      const res = await fetch(S.route.base + '/gallery', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seat: S.seatCode, title: titleOf(v.html), model: v.model, prompt_id: v.promptId || null,
          html: '<!-- poznan-files: ' + JSON.stringify(names) + ' -->\n' + v.html, files, course: 'poznan' }),
      });
      const j = await res.json().catch(() => ({}));
      if (!res.ok) { note(esc(j.error || 'Serwer nie przyjął aplikacji.')); return; }
    } catch (e) { note('Serwer jest teraz nieosiągalny.'); return; }
    track('phones', {});
    const d = document.createElement('div');
    d.style.cssText = 'position:fixed;inset:0;z-index:1000;background:rgba(10,14,24,.94);display:flex;flex-direction:column;align-items:center;' +
      'justify-content:center;gap:16px;color:#fff;font:600 24px/1.3 system-ui,sans-serif;text-align:center;padding:20px;cursor:pointer';
    d.innerHTML = '<img src="data/poznan/qr.svg" alt="Kod QR do aplikacji na telefon" style="width:min(62vh,80vw);height:min(62vh,80vw);background:#fff;padding:14px;border-radius:14px">' +
      '<div>Aplikacja jest w Państwa telefonach</div>' +
      '<div style="font:500 18px ui-monospace,Menlo,monospace;color:#ffd166">lszoszk.github.io/workshop-studio/poznan.html</div>' +
      '<small style="font-weight:400;font-size:15px;color:#aab">Kliknij albo Esc, aby zamknąć</small>';
    const onKey = (e) => { if (e.key === 'Escape') close(); };
    const close = () => { d.remove(); removeEventListener('keydown', onKey, true); };
    d.onclick = close;
    addEventListener('keydown', onKey, true);
    document.body.append(d);
  }

  function removeOwn(key) {
    const e = S.own[key];
    if (!e || !confirm(`Remove "${e.name}" from this browser? An app built on it will show no records.`)) return;
    delete S.own[key];
    OwnFiles.remove(key);
    S.draft.delete(key);
    renderAttach();
    renderShelf();
    if ($('drawerShelf')) renderShelf($('drawerShelf'));
  }

  // what is inside, and exactly what the model would get
  function openOwn(key) {
    const e = S.own[key], d = JSON.parse(e.text), s = e.shape;
    const list = (s.path ? d[s.path] : d) || [];
    const cols = s.fields.slice(0, 8).map((f) => f.name);
    const cell = (v) => esc(v == null ? '' : (typeof v === 'object' ? JSON.stringify(v) : String(v)).slice(0, 90));
    openDrawer(e.name);
    $('drawerBody').innerHTML = `<p>Your ${esc(OwnFiles.NOUN[e.kind])}, read here in your browser: ${esc(fileMetaLine(key))}.${e.note ? ' ' + esc(e.note) : ''}</p>` +
      (cols.length ? `<table class="own-preview"><caption>The first ${Math.min(10, list.length)} records${s.fields.length > 8 ? `, the first 8 of ${s.fields.length} fields` : ''}</caption>` +
        `<thead><tr>${cols.map((c) => `<th scope="col">${esc(c)}</th>`).join('')}</tr></thead>` +
        `<tbody>${list.slice(0, 10).map((r) => `<tr>${cols.map((c) => `<td>${cell(r && r[c])}</td>`).join('')}</tr>`).join('')}</tbody></table>` : '') +
      `<details><summary>What the model gets when you add it to the chat</summary><pre class="own-sent">${esc(OwnFiles.describe(e, e.name))}</pre></details>`;
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

  // a JSON file as a code editor shows it: indented and coloured, its first records only (the public file is
  // megabytes on one line); a range request fetches only the start of it
  async function showJson(url, label) {
    openDrawer(label);
    $('drawer').classList.add('wide');
    $('drawerBody').innerHTML = '<p>Loading the first records…</p>';
    try {
      const r = await fetch(url, { headers: { Range: 'bytes=0-60000' } });
      const text = await r.text();
      const total = Number((r.headers.get('content-range') || '').split('/')[1]) || text.length;
      const recs = firstRecords(text, 10);
      if (!recs.length) throw new Error('no records');
      track('json_view', { file: url.split('/').pop() });
      $('drawerBody').innerHTML = `<p>The first ${recs.length} records of ${total > text.length ? `a ${(total / 1e6).toFixed(1)} MB file` : 'the file'}, ` +
        `laid out the way a code editor shows them: one record per paragraph, one field per line. In the file itself all of it stands on one line.</p>` +
        `<pre class="json-view">${jsonHtml(recs)}</pre>` +
        `<p><a href="${esc(url)}" target="_blank" rel="noopener">Open the whole file as it is</a></p>`;
    } catch (e) {
      $('drawerBody').innerHTML = `<p>The file could not be shown here. <a href="${esc(url)}" target="_blank" rel="noopener">Open it in a new tab</a>.</p>`;
    }
  }

  // the complete records at the start of a JSON array, from a text that may stop in the middle of one
  function firstRecords(text, n) {
    const out = [];
    let depth = 0, start = -1, inStr = false, escaped = false;
    for (let i = 0; i < text.length && out.length < n; i++) {
      const c = text[i];
      if (inStr) {
        if (escaped) escaped = false; else if (c === '\\') escaped = true; else if (c === '"') inStr = false;
      } else if (c === '"') inStr = true;
      else if (c === '[' || c === '{') { if (c === '{' && depth === 1) start = i; depth++; }
      else if (c === ']' || c === '}') {
        depth--;
        if (c === '}' && depth === 1 && start >= 0) { out.push(JSON.parse(text.slice(start, i + 1))); start = -1; }
      }
    }
    return out;
  }

  function jsonHtml(v) {
    const src = JSON.stringify(v, null, 2), re = /("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)/g;
    let out = '', last = 0, m;
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index));
      out += m[1] ? `<span class="tk-${m[2] ? 'attr' : 'str'}">${esc(m[1])}</span>${m[2] || ''}` : `<span class="tk-${m[3] ? 'kw' : 'num'}">${esc(m[0])}</span>`;
      last = re.lastIndex;
    }
    return out + esc(src.slice(last));
  }

  async function openFile(key) {
    if (S.own[key]) return openOwn(key);
    if (CFG.insideFile && key === 'gc') return openInside(key);
    const f = fileMeta(key);
    if (f.kind === 'pdf') { window.open(f.pdf, '_blank', 'noopener'); return; }
    if (f.kind === 'html') { window.open(f.page, '_blank', 'noopener'); return; }
    if (f.kind === 'pdfs') {
      const ten = await dataParsed(key);
      openDrawer(fileLabel(key));
      $('drawerBody').innerHTML = `<p>${ten.records.length} documents, each as the converter extracted it from its PDF. Drag the file into the chat to run your app on all of them.</p>` +
        ten.records.map((d) => `<div class="tool-card"><h4>${esc(d.symbol)}</h4><p>${esc(d.title)} · ${esc(d.committee)} · ${esc(d.year)} · ${fmt(d.count)} pages, ` +
          `${fmt(d.reference.paragraphs)} paragraphs</p><div class="row"><a class="ghost" href="${esc(d.doc_url)}" target="_blank" rel="noopener">Open the PDF</a></div></div>`).join('');
      return;
    }
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
    return downloadCsv(key);
  }

  // the whole file as a spreadsheet
  async function downloadCsv(key) {
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
    if (key === 'hrc' || key === 'hrc_all' || key === 'un_hr_all') {
      const word = { Y: 'yes', N: 'no', A: 'abstained' };
      cols = cols.filter((c) => c !== 'votes').concat('votes');
      row = (r) => cols.map((c) => (c === 'votes' ? Object.entries(r.votes || {}).map(([k, v]) => `${d.countries[k] || k}: ${word[v] || v}`) : r[c]));
    }
    return [cols.map(cell).join(','), ...d.records.map((r) => row(r).map(cell).join(','))].join('\r\n');
  }


  // "What is in the file": the first records as they are stored, what each field means, where else the data is published,
  // and the spreadsheet. All from the file already in this browser: no request goes out.
  const FIELDS = {
    gc: [['id', 'a code for the paragraph, unique in the file'], ['symbol', 'the UN document symbol, as stored; a few hold two documents'],
      ['paragraph', 'the paragraph number inside that document'], ['committee', 'the treaty body that adopted it'], ['year', 'the year it was adopted'],
      ['title', 'the full title of the General Comment'], ['short_title', 'a shorter title, to tell documents apart'], ['doc_url', 'the document at the United Nations'],
      ['text', 'the paragraph, word for word'], ['cited_articles', 'the treaty articles it cites (often empty)']],
  };

  // "The same record, two ways": the first record as a spreadsheet row and as JSON, and the whole file's size in each,
  // counted here from the file in this browser (the CSV is the one "Download as CSV" gives)
  function twoWays(key, d) {
    const r = d.records, rec = r[0], cols = ['symbol', 'paragraph', 'committee', 'year', 'text'];
    const cut = (t) => { t = String(t == null ? '' : t); return t.length > 90 ? t.slice(0, 90).trimEnd() + '…' : t; };
    const bytes = (t) => new Blob([t]).size, mb = (n) => (n / 1e6).toFixed(1) + ' MB';
    const csv = bytes(csvOf(key, d)), json = bytes(JSON.stringify(d));
    return '<h4>The same record, two ways</h4>' +
      '<p>As a spreadsheet, the first record is one row under column headings:</p>' +
      `<div class="sheet-wrap"><table class="sheet"><thead><tr><th></th>${cols.map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead>` +
      `<tbody><tr><th>1</th>${cols.map((c) => `<td>${esc(cut(rec[c]))}</td>`).join('')}</tr></tbody></table></div>` +
      '<p>As JSON, the same record carries the name of every field:</p>' +
      `<pre class="json-view">${jsonHtml(rec)}</pre>` +
      `<table class="compare"><thead><tr><th></th><th>Spreadsheet (CSV)</th><th>JSON</th></tr></thead><tbody>` +
      `<tr><th>Whole file</th><td>${mb(csv)}</td><td>${mb(json)}</td></tr>` +
      `<tr><th>Holds</th><td>${fmt(r.length)} rows</td><td>${fmt(r.length)} records</td></tr></tbody></table>` +
      '<p>The same content. A spreadsheet is for people: sort, filter, read. JSON is for programs: every value carries its field name, which is why the file is larger.</p>';
  }

  async function openInside(key) {
    Progress.mark(1);
    const d = await dataParsed(key), r = d.records, f = fileMeta(key), facts = await lookFacts(key);
    openDrawer('What is in the file');
    $('drawer').classList.add('inside');
    $('drawerBody').innerHTML =
      `<p><b>${esc(facts.count)} paragraphs</b> from ${esc(facts.documents)} documents of ${esc(facts.committees)} committees, ${esc(facts.years)}.</p>` +
      `<p>The first three, as they are stored: one record per paragraph, one field per line. This is the whole file; your app reads all of it here in your browser.</p>` +
      `<pre class="json-view">${jsonHtml(r.slice(0, 3))}</pre>` +
      twoWays(key, d) +
      `<h4>The fields</h4><dl class="fields">${FIELDS[key].map(([n, t]) => `<dt>${esc(n)}</dt><dd>${esc(t)}</dd>`).join('')}</dl>` +
      (f.from ? `<p class="from">Also published as data: ${f.from.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${l.icon ? `<span class="from-icon" aria-hidden="true">${esc(l.icon)}</span>` : ''}${esc(l.label)}</a>`).join(' · ')}</p>` : '') +
      `<div class="row"><button type="button" class="ghost" id="insideCsv">Download as CSV</button></div>`;
    $('insideCsv').onclick = () => downloadCsv(key);
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
    $('advBtn').hidden = !CFG.advanced;
    $('cheatBtn').hidden = !CFG.cheatsheet;
    $('wallBtn').classList.toggle('adv', !CFG.wallWithoutAdvanced);   // with no Advanced the wall is for everyone
    renderTheme();
  }

  // Geneva's cheatsheet: Markdown in its own file, so the text can be replaced without touching the code
  async function openCheatsheet() {
    openDrawer('Prompting: best practices');
    $('drawerBody').innerHTML = '<p>Loading…</p>';
    try {
      $('drawerBody').innerHTML = `<div class="cheatsheet answer-md">${md(await getText('data/cheatsheet.md'), true)}</div>`;
    } catch (e) {
      $('drawerBody').innerHTML = '<p>The cheatsheet could not be loaded. Try again in a moment.</p>';
    }
  }

  function takeFurther() {
    const a = S.config.author;
    openDrawer('About');
    $('drawerBody').innerHTML = `
      <p>${esc(a.line)} These open tools were built the way you built your app today: a model writes the code, the code does the counting, and a person checks it.</p>
      ${a.tools.map((t) => `<div class="tool-card"><h4><a href="${t.url}" target="_blank" rel="noopener">${esc(t.name)}</a></h4>
        <p>${esc(t.blurb)}${t.with ? ` With ${esc(t.with)}.` : ''}</p>
        <div class="row"><a href="${t.url}" target="_blank" rel="noopener">Open the tool</a> · <a href="${t.repo}" target="_blank" rel="noopener">Source code</a></div></div>`).join('')}
      <h4>The take-home kit</h4>
      <p>One file for when the studio is not the place to work: every workshop request, ready to paste into your own chatbot (Claude, ChatGPT, Gemini, Copilot) or LM Arena; a place to paste its answer and run the app on the workshop data for ${esc(S.country)}, with no internet; and your own apps from today.</p>
      <div class="row"><button type="button" class="primary" id="kitBtn">Download the take-home kit</button></div>
      <h4>Take the method home</h4>
      <p>Point an AI coding assistant (Claude Code, Codex, Antigravity, Cursor) at one of these public repositories. Ask for a review first, then make one change at a time and check it.</p>
      <label>Repository <select id="tfRepo">${a.tools.map((t) => `<option value="${t.repo}">${esc(t.name)}</option>`).join('')}</select></label>
      <div class="prompt-box"><textarea id="tfPrompt" readonly></textarea></div>
      <div class="row"><button type="button" class="primary" id="tfCopy">Copy the prompt</button></div>
      <p class="caution">These assistants send the files they read to the company that runs the model. That is fine for public code like this; never point them at confidential documents.</p>
      <h4>Start over</h4>
      <p>Clear your apps and your conversation in this browser, to begin again from the first request. Your seat code, your settings and your own files stay. Save an app as a file first if you want to keep it.</p>
      <div class="row"><button type="button" class="ghost" id="startOverBtn">Start over</button></div>
      <h4>What this studio records</h4>
      <p class="caution">To improve the workshop, the studio records what you do: which steps you pick, which model answers, how long it takes and what fails. It never records your messages, your files, your apps or anything from the data. Add <code>?notrack=1</code> to the address to switch it off in this browser.</p>
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
    $('kitBtn').onclick = (e) => downloadKit(e.currentTarget);
    $('startOverBtn').onclick = () => {
      if (!confirm('Clear your apps and your conversation in this browser? This cannot be undone.')) return;
      track('reset', {});
      Track.flush(true);
      clearWork();
      location.reload();
    };
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

  /* ---------- the seven steps of the one-session course (the bar under the header) ---------- */

  // Steps are done in any order and never undone; each is marked by something the participant did, or skipped.
  // 1 Data: "What is in the file" is opened, or the planner's look at the file is on screen.  2 Brief: a planning session starts.
  // 3 Plan read: the plan is on the stage.  4 Plan approved: Build from this plan.
  // 5 App built: a build's preview opened without an app error.  7 Improved: such a build on top of an earlier app.
  // 6 Tested has no hook of its own yet: until the studio reports it, the step's Skip link is the way on.
  const Progress = {
    LABELS: ['Data', 'Prompt', 'Plan read', 'Plan approved', 'App built', 'Tested', 'Improved'],
    HINTS: ['look inside the file', 'write your prompt and send it', 'read the plan on the right', 'approve the plan to build it',
      'let the model build the app', 'try the app and test what it says', 'ask for one improvement'],
    fresh: () => ({ done: Array(7).fill(false), skipped: Array(7).fill(false) }),
    // a saved value, checked: seven booleans each
    from(d) {
      const ok = (a) => Array.isArray(a) && a.length === 7 && a.every((x) => typeof x === 'boolean');
      return d && ok(d.done) && ok(d.skipped) ? { done: d.done, skipped: d.skipped } : this.fresh();
    },
    mark(n) {
      if (!CFG.progress || S.progress.done[n - 1]) return;
      S.progress.done[n - 1] = true;
      track('progress', { step: n, secs: Math.round((performance.now() - Track.t0) / 1000), course: S.course });
      save();
      this.render();
      this.allDone();
    },
    skip(n) {
      if (!CFG.progress || S.progress.done[n - 1]) return;
      S.progress.done[n - 1] = S.progress.skipped[n - 1] = true;
      track('progress_skip', { step: n, course: S.course });
      save();
      this.render();
      this.allDone();
    },
    // all seven, the first time: "Show it to the room?" (only where there is a wall to send to)
    allDone() {
      if (!CFG.signWall || S.wallAsked || !S.progress.done.every(Boolean) || !S.route || S.route.type !== 'server' || !currentVersion()) return;
      S.wallAsked = true;
      save();
      setTimeout(wallDialog, 500);   // the finished app is on the stage first
    },
    render() {
      if (!CFG.progress) return;
      const { done, skipped } = S.progress, count = done.filter(Boolean).length, cur = done.indexOf(false);
      $('progressSteps').innerHTML = this.LABELS.map((l, i) => `<li class="${done[i] ? 'done' : ''}${skipped[i] ? ' skipped' : ''}${i === cur ? ' current' : ''}"` +
        `${i === cur ? ' aria-current="step"' : ''}><span class="pn" aria-hidden="true">${done[i] ? (skipped[i] ? '–' : '✓') : i + 1}</span><span class="pl">${esc(l)}</span>` +
        `${i === cur ? `<button type="button" class="linkish pskip" data-skip="${i + 1}" title="Mark this step as done without doing it">Skip</button>` : ''}</li>`).join('');
      $('progressNext').textContent = cur < 0 ? 'All seven steps are done' : `Next: ${this.HINTS[cur]}`;
      const bar = $('progress');
      bar.setAttribute('aria-valuenow', String(count));
      bar.setAttribute('aria-valuetext', `${count} of 7 steps done`);
    },
  };

  /* ---------- persistence (per seat and country; survives a reload) ---------- */

  function localGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function localSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  // one conversation per seat and session (each session starts a clean chat); the country is a separate choice
  const storeKey = (session = S.session) => `ws:work:${S.seatCode || 'guest'}:${CFG.storeId}:${session}`;

  function save() {
    // the full text sent with each request is not kept: it would fill the browser's storage
    const trace = S.trace.map((t) => Object.assign({}, t, { request: '', at: t.at.toISOString() }));
    localSet(storeKey(), JSON.stringify({ versions: S.versions, current: S.current, talk: S.talk, trace, progress: S.progress, test: S.test, wallAsked: S.wallAsked, planning: planSaved() }));
  }

  // the plan of a free brief waits in the browser until it is built or replaced: brief, topic, look, answers and every version.
  // (After a reload it is put back before anything saves: until then the saved one is kept as it was.)
  function planSaved() {
    const pl = S.planning;
    if (pl && freeBrief(pl.p)) {
      return pl.history.length ? { promptId: pl.p.id, brief: pl.brief, topic: pl.topic, look: pl.look, answers: pl.answers, files: pl.files, history: pl.history } : S.savedPlan || null;
    }
    return S.savedPlan || null;
  }

  // the apps, the conversation and the trace in this browser, for every seat; the seat code, the settings and the
  // participant's own files stay
  function clearWork() {
    try {
      Object.keys(localStorage).filter((k) => k.startsWith('ws:work:')).forEach((k) => localStorage.removeItem(k));
    } catch (e) { /* private mode */ }
    Object.assign(S, { versions: [], current: null, talk: [], trace: [], progress: Progress.fresh(), test: { shown: false, checks: [false, false, false], note: '' }, wallAsked: false });
  }

  function restore() {
    S.progress = Progress.fresh();
    S.test = { shown: false, checks: [false, false, false], note: '' };
    S.wallAsked = false;
    S.savedPlan = null;
    try {
      // the one conversation of the studio before 11.11.2026 goes to the session opened first
      const legacy = `ws:work:${S.seatCode || 'guest'}`;
      if (!localGet(storeKey()) && localGet(legacy)) { localSet(storeKey(), localGet(legacy)); localStorage.removeItem(legacy); }
      const d = JSON.parse(localGet(storeKey()) || 'null');
      S.progress = Progress.from(d && d.progress);
      const t = d && d.test;
      if (t && t.shown === true && Array.isArray(t.checks) && t.checks.length === 3 && t.checks.every((x) => typeof x === 'boolean')) S.test = { shown: true, checks: t.checks, note: String(t.note || '').slice(0, 200) };
      S.wallAsked = !!(d && d.wallAsked);
      if (d && Array.isArray(d.versions)) { S.versions = d.versions; S.current = d.current; }
      if (d && Array.isArray(d.talk)) S.talk = d.talk;
      S.savedPlan = planFrom(d && d.planning);
      if (d && Array.isArray(d.trace)) S.trace = d.trace.map((t) => Object.assign(t, { at: new Date(t.at) }));
    } catch (e) { /* start clean */ }
  }

  /* ---------- wiring ---------- */

  Preview.init();
  wireSplitter();
  $('progressSteps').addEventListener('click', (e) => {
    const b = e.target.closest('[data-skip]');
    if (!b) return;
    Progress.skip(Number(b.dataset.skip));
    if (b.dataset.skip === '1' && DataCard.next) DataCard.next();   // Data skipped: on to the brief
  });
  $('planClose').onclick = () => { $('planView').hidden = true; };
  $('planEditBtn').onclick = () => shownPlan && beginEdit(shownPlan);
  $('planDone').onclick = () => shownPlan && commitEdit(shownPlan);
  $('planCancel').onclick = () => shownPlan && cancelEdit(shownPlan);
  $('planLook').onchange = (e) => shownPlan && changeLook(shownPlan, e.target.value);
  $('planBrief').onclick = () => shownPlan && showBrief(shownPlan);
  $('planModeBtn').onclick = () => { S.planMode = !S.planMode; renderPlanMode(); $('input').focus(); };
  $('composer').addEventListener('submit', (e) => { e.preventDefault(); submitBuild($('input').value); });
  // Enter sends, as in any chatbot; Shift+Enter starts a new line
  $('input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); submitBuild($('input').value); }
  });
  // a screenshot pasted into the box goes with the message
  $('input').addEventListener('paste', (e) => {
    const pics = [...((e.clipboardData && e.clipboardData.items) || [])].filter((i) => i.kind === 'file' && i.type.startsWith('image/')).map((i) => i.getAsFile());
    if (pics.length) { e.preventDefault(); addImages(pics); }
  });
  $('input').addEventListener('input', () => {
    fitInput();
    if (!$('input').value.trim()) { S.pendingPromptId = null; S.pendingText = ''; S.freshNext = false; renderContinuing(); renderNeeds(); renderSuggest(); }
  });
  $('lookPanel').addEventListener('click', (e) => { const b = e.target.closest('button[id]'); if (b) track('look', { item: b.id }); });
  // a file from the shelf, dropped anywhere on the chat column
  const chatCol = document.querySelector('.chat');
  const isFile = (e) => [...(e.dataTransfer && e.dataTransfer.types || [])].includes('text/x-studio-file');
  const isOwn = (e) => [...(e.dataTransfer && e.dataTransfer.types || [])].includes('Files');   // from the computer
  chatCol.addEventListener('dragover', (e) => { if (isFile(e) || isOwn(e)) { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; chatCol.classList.add('dragging'); } });
  chatCol.addEventListener('dragleave', (e) => { if (!chatCol.contains(e.relatedTarget)) chatCol.classList.remove('dragging'); });
  chatCol.addEventListener('drop', (e) => {
    chatCol.classList.remove('dragging');
    if (isOwn(e)) { e.preventDefault(); e.stopPropagation(); return dropped(e.dataTransfer.files, true); }
    if (!isFile(e)) return;
    e.preventDefault();   // not as text into the box
    addFile(e.dataTransfer.getData('text/x-studio-file'));
  });
  // a file from the computer dropped anywhere else goes onto the shelf, and the browser does not open it instead
  document.addEventListener('dragover', (e) => { if (isOwn(e)) e.preventDefault(); });
  document.addEventListener('drop', (e) => { if (isOwn(e)) { e.preventDefault(); dropped(e.dataTransfer.files, false); } });
  // pictures go with the message being written; other files onto the shelf
  function dropped(list, attach) {
    const all = [...list], pics = all.filter((f) => f.type.startsWith('image/'));
    if (pics.length) addImages(pics);
    if (pics.length < all.length && !ownAllowed()) note('Your own files are part of <b>Advanced</b> (in the footer). Turn it on, then add the file again.');
    else if (pics.length < all.length) addOwnFiles(all.filter((f) => !f.type.startsWith('image/')), attach);
  }
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
  $('cheatBtn').onclick = openCheatsheet;
  $('feedbackBtn').onclick = openFeedback;
  $('themeBtn').onclick = toggleTheme;
  $('advBtn').onclick = () => setAdvanced(!S.advanced, true);
  $('stopBtn').onclick = () => S.ctrl && S.ctrl.abort();
  $('countrySelect').onchange = (e) => changeCountry(e.target.value);
  $('modelSelect').onchange = (e) => {
    track('model', { from: S.model, to: e.target.value, by: 'user' });
    S.model = e.target.value;
    localSet('ws:model', S.model);
    renderBadge();
    if (S.versions.length) note(`Your next build goes to <b>${esc(S.config.models[S.model].label)}</b> (${esc(whereOf(S.model))}). Earlier versions keep the model that made them.`);
  };
  $('sessionSwitch').onclick = (e) => { const b = e.target.closest('[data-session]'); if (b) setSession(b.dataset.session); };
  $('lookBtn').onclick = (e) => { e.stopPropagation(); toggleMenu(); };
  $('keepBtn').onclick = (e) => { e.stopPropagation(); toggleMenu($('keepBtn'), $('keepPanel')); };
  document.addEventListener('click', (e) => { if (!e.target.closest('.menu')) closeMenu(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeMenu(); $('drawer').hidden = true; } });
  $('run3Btn').onclick = run3;
  $('ask3Btn').onclick = () => ask3('count');
  $('traceBtn').onclick = () => { openDrawer(TRACE_TITLE); renderTrace(); };
  $('downloadBtn').onclick = () => { closeMenu(); download(); };
  $('wallBtn').onclick = () => { closeMenu(); sendToWall(); };
  $('kitMenuBtn').onclick = (e) => { downloadKit(e.currentTarget.querySelector('b')).then(closeMenu); };
  $('drawerClose').onclick = () => { $('drawer').hidden = true; };
  $('roomBtn').onclick = () => Room.open();
  $('roomOpen').onclick = () => Room.open();
  $('roomClose').onclick = () => Room.read();

  boot().catch((e) => {
    note('The studio could not start: ' + esc(e.message) + '. Reload the page; if it persists, tell a facilitator.');
  });
})();
