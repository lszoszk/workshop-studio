# Workshop Studio

A chat that writes single-file web apps over UN human rights data, built for the hands-on sessions of *AI for Human Rights Professionals* (Geneva Human Rights Hub, ITU, 4 December 2026, Sessions 7 and 8).

Participants describe a tool in plain language; a model writes the code; the code runs in their browser on the full dataset. The studio is built to make four things visible while they work, all under *Look inside*:

- **Where the model is and where the script is.** *Layers* colours what the model wrote once, what the code computes from the data every time, and what a model produced while the app ran. *Run it three times* shows that the app gives the same result three times; *Ask the model directly* (Session 8) shows that the model, asked the same question without the data, does not.
- **What leaves the laptop.** The model receives the participant's words, the studio's instructions, a description of the data and three sample records. The full datasets stay in the browser. *What left this laptop* lists every request, what was sent and what was not.
- **Who runs the model.** Participants choose a European, US or Chinese model, and see who made it and whose servers run it. Every request is pinned to one provider with zero data retention.
- **What still works offline.** *Cut the model link* (Session 8) cuts the model; the app keeps working. *Save as file* gives a single HTML file that opens with a double-click, without internet.

It works like a chatbot: participants can ask anything, and the model writes an app only when asked for one. Data comes from **Your files**, a shelf that fills the stage before the first app: a country's UN recommendations, the General Comments and the Council votes (each opens as a CSV in Excel), and the PDF of CESCR General comment No. 27. A file is dragged into the chat (or added with *Add to chat*); the model then gets one line naming it, and the app gets the whole file, in the browser. A workshop request does not go out without its file. *App / Code* switches between the app and what the model wrote; *New tab* opens the app in a tab of its own (`app.html`), still sandboxed, following the studio's current version, its model requests still going through the studio.

What a participant sees grows with what they have done (Hick's law): before the first app, three suggestions and the shelf; after it, two next steps, *Suggest improvements*, one new start and the *Look inside* menu; *Session 8* (the switch in the top bar, or `?stage=s8`) adds its requests and two more tools. On a phone the page only hands the seat code and link on to a laptop. The footer says who made the studio and links to the open tools it comes from; *Take it further* has a prompt for reviewing those repositories with an AI coding assistant. Dark mode follows the system, or the footer's switch.

## Layout

```
site/                  the studio (GitHub Pages): index.html, studio.js, runtime.js, config.json
site/data/             data pack, schema.md, samples.json, system_prompt.md, prompts.json
site/replay/           recorded answers for the no-model fallback
server/, worker/       the proxy to OpenRouter (VM) and its Cloudflare stand-in
docs/api-contract.md   the contract between the studio and both servers
docs/session-plan.md   Sessions 7 and 8 minute by minute: what to click, what to show, what to do when something fails
tools/build_data.py    rebuilds site/data from UHRI+, the UN Human Rights Database and HRC votes
tools/bakeoff.py       every model on every workshop prompt, scored in headless Chrome
tools/make_seats.py    seat codes and printable badge cards (tools/out/, git-ignored)
tools/wiki_probe.py    uses a built research wiki as a participant would: a concept, a PDF link, a summary
tools/briefing_probe.py  tests a built briefing checker on a briefing with planted errors
tools/draft_plans.py     drafts the plans for the four workshop apps (Fable 5.1), or writes their briefs
```

## Run locally

```bash
python3 -m http.server 8766 --bind 127.0.0.1 --directory site
```

Open `http://localhost:8766/?via=replay` for recorded answers. For live models, run the server locally (`server/RUNBOOK.md`) and open `http://127.0.0.1:8766/?api=http://127.0.0.1:8011/studio-api#s=CODE` (`?api=` is honoured only on a local page, for a local server). `?via=<route id>` forces a route; `#s=CODE` passes a seat code; `?stage=s8` opens Session 8; `?wall=1` shows the app alone, for the projector; `?planpace=20` plays a planning session's notes in 20 seconds instead of two minutes (rehearsals; the tests use 1).

After changing `studio.css`, `studio.js` or `preview-doc.js`, bump the `?v=` date on their links in `index.html` and `gallery/*.html`, so no browser keeps an old copy.

## Data

- UHRI+: the OHCHR Universal Human Rights Index, cleaned (one file per country).
- General Comments: the UN Human Rights Database, paragraph by paragraph.
- Human Rights Council recorded votes since 2021.
- Raw PDF text: CESCR General comment No. 27, 20 pages exactly as `pdftotext` gives them, with the reference (90 paragraphs, 141 footnotes) for the extraction exercise.
- Library: neurotechnology in the administration of justice, nine documents of six kinds (`tools/sources/` and the book wiki's UN PDFs, copied to `site/files/`), 945 passages, each with the PDF page it starts on and the page printed there. Apps open a PDF at its page with `studio.openSource(id, page)`, in a drawer next to the app. `python3 tools/build_data.py --pdf-only` rebuilds the PDF text and the library alone (needs PyMuPDF and Ghostscript).
- Plan mode: the four workshop apps replay a planning session recorded beforehand with Claude Fable 5.1 (`site/data/planning/<id>.json`, named by `planning` in `prompts.json`; format in `tools/planning/FORMAT.md`), and the chat says it is a simulation. The planner's log (an account written for participants) streams like thinking, with its steps between them (its looks at the data recomputed from the participant's own file); its questions come as cards with fixed answers; the plan composed from the answers goes on the stage, with the facilitator's brief beside it. *Build from this plan* sends the plan to the participant's model; *Change something* sends their change and the plan to it, live, and plan v2 replaces the first. Recorded mode builds only the recommended answers. Without a package, a request goes as written. `tools/bakeoff.py` builds from the plan with the recommended answers (`tools/planning.py compose`, which the studio matches).
- Reference shelf: `site/data/shelf.json` (`tools/shelf.py build`), offline copies of good-practice pages. The studio searches it on every message (BM25 over passages of about 150 words, as `tools/shelf.py` scores them); up to three passages that match well go with the message under "Reference shelf excerpts (offline copies)", the chat shows the search as a step whose pages open in the drawer, and *What left this laptop* lists them.

Rebuild with `python3 tools/build_data.py --countries "Kenya,Tunisia,…"` once the participants' countries are known.
