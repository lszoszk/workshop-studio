/* A short tour of the studio: a dimmed screen with one element lit and a card beside it. It starts by
   itself the first time someone opens the studio (once per browser) and from "Tour" in the footer.
   An element that is not on screen yet (the toolbar before the first app) gets a card in the middle. */
window.Tour = (function () {
  'use strict';
  const STEPS = [
    { title: 'Welcome to Garage Research', wide: true,
      text: ['Many of us lose hours on searching UN documents: finding what a body said on an issue, or checking whether a recommendation was really addressed to a given state. Here you ask a model to build a small tool for such a task, on real UN human rights data.',
        'Generative AI does not have to write the text you rely on. Here it writes the tool, which shortens the way to the sources you should take into account: each finding links to the document and paragraph it comes from. Reading those sources and judging them stays with you.',
        'Building such tools is also a way to learn where the models help and where they fail (the so-called jagged frontier), and to keep that skill after the workshop.',
        'Every app can be adjusted: ask for a change in your own words. The tour takes one minute.'] },
    { at: '#sessionSwitch', title: 'Two sessions',
      text: 'Session 1 and Session 2 offer different apps. Your facilitator will say when to switch.' },
    { at: '#countryChip', title: 'Your country',
      text: 'Its UN recommendations and observations are your first file. Pick another country to run the same app on its records.' },
    { at: '.model-pick', title: 'Your model',
      text: 'Choose who builds your app. The line beside it says where the model was made and where it runs: that is where your request goes.' },
    { at: ['#shelf .fcard', '#filesBtn'], title: 'Your files',
      text: 'Open a file to see what is inside. To build on it, drag it into the chat, or press Add to chat. Your app gets the whole file, here in your browser; the model sees only a description and a few sample rows.' },
    { at: ['#suggest', '#composer'], together: true, title: 'Ask',
      text: 'Click a suggestion above the box, or describe a tool in your own words. In plan mode the model first looks at your data and asks you a few questions. Enter sends.' },
    { at: '#toolbar', title: 'Your app',
      text: 'When an app is on the stage: App and Code show what the model wrote, New tab opens it full screen, Save as file keeps a copy that works offline, and Look inside shows how it works and what left this laptop.' },
    { at: '.foot-end', title: 'The gallery, and this tour again',
      text: 'The Gallery at the top shows what different models built from the same plans. Tour, down here, starts this again.' },
  ];
  let i = 0, root = null, onKey = null;

  const visible = (el) => el && el.offsetParent !== null && el.getBoundingClientRect().width > 0;
  // the area to light: the first of the step's elements on screen, or all of them together
  function target(step) {
    const els = [].concat(step.at || []).map((sel) => document.querySelector(sel)).filter(visible);
    if (!els.length) return null;
    if (!step.together) return els[0].getBoundingClientRect();
    const rs = els.map((e) => e.getBoundingClientRect());
    const left = Math.min(...rs.map((r) => r.left)), top = Math.min(...rs.map((r) => r.top));
    const right = Math.max(...rs.map((r) => r.right)), bottom = Math.max(...rs.map((r) => r.bottom));
    return { left, top, right, bottom, width: right - left, height: bottom - top };
  }

  function draw() {
    const step = STEPS[i], r = target(step);
    const hole = root.querySelector('.tour-hole'), card = root.querySelector('.tour-card');
    card.querySelector('.tour-n').textContent = `${i + 1} of ${STEPS.length}`;
    card.querySelector('h3').textContent = step.title;
    card.querySelector('.tour-text').replaceChildren(...[].concat(step.text).map((t) => Object.assign(document.createElement('p'), { textContent: t })));
    card.classList.toggle('wide', !!step.wide);
    card.querySelector('[data-t=back]').hidden = i === 0;
    card.querySelector('[data-t=next]').textContent = i === STEPS.length - 1 ? 'Start' : i === 0 ? 'Show me around' : 'Next';
    if (!r) {   // nothing to point at: the card in the middle, the whole screen dimmed
      hole.style.cssText = 'left:50%;top:50%;width:0;height:0';
      card.style.cssText = 'left:50%;top:50%;transform:translate(-50%,-50%)';
    } else {
      const pad = 6;
      hole.style.cssText = `left:${r.left - pad}px;top:${r.top - pad}px;width:${r.width + 2 * pad}px;height:${r.height + 2 * pad}px`;
      const W = innerWidth, H = innerHeight, cw = Math.min(360, W - 32), ch = card.offsetHeight || 180;
      let top = r.bottom + 14 + ch < H ? r.bottom + 14 : r.top - 14 - ch;   // below, or above when there is no room
      if (top < 12) top = Math.min(H - ch - 12, Math.max(12, r.top));
      const left = Math.min(W - cw - 16, Math.max(16, r.left));
      card.style.cssText = `left:${left}px;top:${top}px;width:${cw}px`;
    }
    card.querySelector('[data-t=next]').focus();
  }

  function go(d) {
    if (i + d >= STEPS.length || i + d < 0) return stop();
    i += d;
    draw();
  }

  function stop() {
    if (!root) return;
    root.remove(); root = null;
    removeEventListener('keydown', onKey, true);
    removeEventListener('resize', draw);
    try { localStorage.setItem('ws:toured', '1'); } catch (e) { /* a private window: the tour may show again */ }
  }

  function start() {
    if (root) return;
    i = 0;
    root = document.createElement('div');
    root.className = 'tour';
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', 'A tour of the studio');
    root.innerHTML = '<div class="tour-hole"></div><div class="tour-card"><div class="tour-n"></div><h3></h3><div class="tour-text"></div>' +
      '<div class="tour-row"><button type="button" class="linkish" data-t="skip">Skip the tour</button>' +
      '<span><button type="button" class="ghost" data-t="back">Back</button> <button type="button" class="primary" data-t="next">Next</button></span></div></div>';
    document.body.appendChild(root);
    root.querySelector('[data-t=next]').onclick = () => go(1);
    root.querySelector('[data-t=back]').onclick = () => go(-1);
    root.querySelector('[data-t=skip]').onclick = stop;
    onKey = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); stop(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
    };
    addEventListener('keydown', onKey, true);
    addEventListener('resize', draw);
    draw();
  }

  // the first visit starts it by itself; an automated browser (the tests) does not get it unasked
  function startOnce() {
    let seen = null;
    try { seen = localStorage.getItem('ws:toured'); } catch (e) { /* treated as not seen */ }
    if (!seen && !navigator.webdriver) start();
  }

  return { start, startOnce, stop };
})();
