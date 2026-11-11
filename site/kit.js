/* The take-home kit: one HTML file the studio builds in the browser with one click (About → Download the take-home
   kit), for when the studio is not the place to work: a participant's own chatbot (Claude, ChatGPT, Gemini, Copilot)
   or LM Arena. It holds every workshop request ready to copy, a place to paste a chatbot's answer and run the app on
   the workshop data (inside the file, offline), and the participant's own apps. */
window.Kit = (function () {
  'use strict';
  /* ---------- the requests, for a chatbot that is not the studio ---------- */

  // the studio's instructions, adapted: no edits (a chatbot answer is pasted whole), no model inside the app
  function system(sysmd) {
    let s = sysmd.split('\n---\n')[1].trim();
    s = s.replace(/\n## Asking a model from inside the app[\s\S]*?(?=\n## )/, '\n');
    s = s.replace(/\n## Files\n[\s\S]*?(?=\n## )/, '\n## Files\n\nThe data is already in `window.WORKSHOP_DATA` when your script runs: the kit page, where the participant pastes your answer, puts it there. Build on the data the request names.\n');
    s = s.replace(/\n- A change to the app you already wrote[\s\S]*?(?=\n- A change to most of the app)/, '\n- A change to an app you already wrote: the complete updated document in one ```html block; the kit page cannot apply edits.');
    return 'You are helping a participant of a workshop outside its studio, in an ordinary chatbot. They paste your answer into the kit page, which shows the app on the data; it has no model inside it, so the app must not call `studio.ask`.\n\n' + s;
  }

  // the parts of schema.md and samples.json for the datasets one request needs
  function data(schema, samples, keys) {
    const parts = schema.split(/\n(?=## )/);
    const keep = parts.filter((p) => keys.some((k) => p.startsWith('## `WORKSHOP_DATA.' + k + '`')) || p.startsWith('## Rules for every app'));
    const sample = {};
    keys.forEach((k) => { if (samples[k]) sample[k] = samples[k]; });
    return keep.join('\n') + '\n\n## Sample records (the real data is much larger)\n\n```json\n' + JSON.stringify(sample, null, 1) + '\n```';
  }

  // the kit page (site/kit/kit.html) with everything inside: Chart.js, the apps' runtime, the data, the requests, the apps
  function page(template, { chart, runtime, datasets, meta, steps, apps }) {
    const js = (o) => JSON.stringify(o).replace(/<\//g, '<\\/');
    return template
      .replace('/*@CHART@*/', () => chart.replace(/<\//g, '<\\/'))
      .replace('/*@RUNTIME@*/', () => runtime.replace(/<\//g, '<\\/'))
      .replace('/*@DATA@*/', () => 'window.KIT_DATA=' + js(datasets) + ';window.KIT_META=' + js(meta) + ';window.KIT_STEPS=' + js(steps) +
        ';window.KIT_APPS=' + js(apps) + ';');
  }

  return { system, data, page };
})();
