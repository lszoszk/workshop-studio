# Geneva, 4 December 2026: run sheet for the one-session studio

*AI for Human Rights Professionals*, Geneva Human Rights Hub, ITU, Day 3. One session of 90 minutes, up to 30 participants (diplomats, NGO, NHRI and UN staff), one app: the **Verbatim finder** for the treaty bodies' General Comments. The studio is `lszoszk.github.io/workshop-studio/?course=geneva`; the QR code on each seat card opens it with the seat code. The two-session path of November stays available as `?course=full` (tag `two-sessions-2026-11-15`; its session plan is in `docs/archive/`).

The arc in one line: **data → brief → plan → change the plan → build → test → improve → wall → teaser.** The progress bar under the studio's header follows the same seven steps, so the room can see where everyone is.

Draft status: the times below are planned, not yet measured; measure them at the dry run and replace them.

## Before the day

- [ ] **Keys and money** (see `server/RUNBOOK.md`): the OpenRouter key "zajecia" and the Anthropic key "garage-research" are enabled; the studio is resumed on the admin page; `STUDIO_ANTHROPIC_CAP` raised to about $150; the OpenRouter balance at least $100 and the key's own limit at least $150.
- [ ] **Default model** on the admin page: Claude Sonnet 5.5 (the course already starts on it; the admin setting covers requests that name no model).
- [ ] **Certificate**: `echo | openssl s_client -connect 150.254.115.204:443 2>/dev/null | openssl x509 -noout -enddate` shows a date after 4 December (certbot renews it twice a day; check anyway).
- [x] **Trial builds, Sonnet** (17.11, in Claude Code, no API): one app per look (paper, night, UN blue, newsprint, index cards), each 6/6 on the bake-off checks (`tests/bakeoff/2026-11-17-g1-looks-*`); the paper build is the recorded app behind **Load a working version**.
- [ ] **Trial builds, GLM**: the same five prompts through the API once the keys are on.
- [ ] **Load test**: 30 builds at once on Sonnet (about $10), then 5 on GLM; note the times here.
- [ ] **Seat cards** printed with the QR code to `?course=geneva` and the seat code; budget per seat $8.
- [ ] **Room chat**: the facilitator's page `…/studio-api/admin/room?key=…&course=geneva` open on your phone or laptop; test one message to the room.
- [ ] **Wall**: `lszoszk.github.io/workshop-studio/wall.html?course=geneva` in a second window.
- [ ] **Teaser**: `python3 tools/teaser/teaser_watch.py --course geneva --day 2026-12-04 --upload` running on your laptop from the start of the session; `site/teaser.html` open in a third window (full screen with F).
- [ ] **Organisers' consent** to show participants' chosen names on the wall and in the teaser (the name is optional; without one, the wall shows the app alone).

## The session (90 minutes)

| Min | You | The room in the studio | Progress |
|---|---|---|---|
| 0–8 | **Why we do this.** Uploading a document to a chatbot gets you a paraphrase you cannot cite and cannot check; building a small tool on clean data gets you the exact words with their source, every time. Login over the first minutes (QR code on the card). | Log in; the studio opens on the brief. | – |
| 8–18 | **The data.** Structured data from Hugging Face (the UN Human Rights Database): why paragraphs with symbols and numbers beat PDFs; what is in the file and what is not. Look at it before you ask for anything. | The studio opens on **First, your data**: the counts of the file; **Look inside the file**: three records as JSON, the fields, the Hugging Face link. | 1 Data |
| 18–28 | **What a prompt is: a brief.** Ethan Mollick's delegation questions (slide, links below): what and why, the limits, what "done" looks like, what to check before finishing; and the rule of this session: **plan first** (more agency for you, a better result, no rabbit hole at the start). | **Write your brief**: fill in **My topic**, switch paragraphs off or rewrite them, Send. The planner looks at the file too (its counts are the participant's own). | 2 Brief |
| 28–43 | **The plan (a simulation).** The planning session was recorded with Claude Fable 5.1; the plan is short on purpose. Pairs: read it, argue about the three decisions (what counts as a match, how a citation reads, what a result shows first). | Answer the three cards; read the plan (about 380 words). | 3 Plan read |
| 43–50 | **Change the plan.** Two ways, both reach the build: ask in the chat ("Change the plan: …") or press **Edit the plan** and type. The look of the app (five looks, one per seat at random) can be changed too. | Edit, then **Build from this plan**. | 4 Plan approved |
| 50–58 | **While it builds:** the jagged-frontier slide (`/slides/jagged-frontier.html`): no model is best at everything; test a model on your own task. | Claude Sonnet (default) or GLM-5.3, their choice; say the difference honestly (Sonnet: no build error in Venice, no zero data retention; GLM: open weights in the EU, more errors). | 5 App built |
| 58–68 | **Does it work?** Three checks on the card **Test your app**: a phrase you know, word for word; one paragraph against its source; a pasted citation with symbol and paragraph. Brainstorm in pairs: one thing to change. | Tick the three checks; write "One thing I would change". | 6 Tested |
| 68–80 | **Improve it.** **Suggest three improvements** (three alternatives each time) or their own idea; pick, edit or reject; build one change. | Build one change (15–60 s). | 7 Improved |
| 80–85 | **The wall.** At 100% the studio asks whether to show the app to the room, with an optional name. Two or three apps on the projector: what they found, what they checked. | **Send to wall**. | 100% |
| 85–90 | **The teaser.** Full screen: 30 seconds made from the room's apps while they worked. Take-home kit (About → Take-home kit): their brief, plan and app, the data, and **At home**: a dashboard on Human Rights Council votes 2006–2026 to build with their own chatbot. Feedback form. | Download the kit. | – |

## Slide notes: sources to show (all checked 16.11.2026)

- Ethan Mollick, [Management as AI superpower](https://www.oneusefulthing.org/p/management-as-ai-superpower) (27 January 2026): delegation documentation answers what we are trying to accomplish and why, where the limits of the delegated authority are, what "done" looks like, what outputs and interim outputs are needed, and what to check before saying it is finished. The brief's five paragraphs map onto these questions (each block shows its question).
- Ethan Mollick, [Getting started with AI: Good enough prompting](https://www.oneusefulthing.org/p/getting-started-with-ai-good-enough) (24 November 2024): treat it like a new coworker; give context; ask it to ask you questions.
- Ethan Mollick, [Agency and Agents](https://www.oneusefulthing.org/p/agency-and-agents) (31 August 2026): agents should come back to people for approval, expertise, variance and the interesting decisions; otherwise "we will have automated the wrong half of the job". This is why the plan stops for your three decisions.
- The data: [treaty-bodies-general-comments on Hugging Face](https://huggingface.co/datasets/lszoszk/treaty-bodies-general-comments) and the [UN Human Rights Database](https://lszoszk.github.io/generalcomments/).
- The jagged frontier: Dell'Acqua et al., [Navigating the Jagged Technological Frontier](https://doi.org/10.1287/orsc.2025.21838), *Organization Science* (2026).

## When something goes wrong

1. **An error as the app opens:** the studio sends it back to the model once by itself. Wait.
2. **Still an error in red:** **Ask the model to fix it**; after two failed fixes, **Load a working version** (a Sonnet build of the default plan recorded before the day) and go on from there.
3. **Stuck on a step:** every step of the progress bar has **Skip**, so nobody misses the wall.
4. **The model is slow or failing for the whole room:** tell the room to switch the model menu (Sonnet ↔ GLM). The studio never switches a participant's model silently; it asks.
5. **No server at all:** the studio plays the recorded session and the recorded app; editing the plan and building changes need the live model.
6. **The teaser is not ready:** the last good version is always in `tools/teaser/out/latest.mp4` on your laptop; play it from there.

## After the session

- Pause the studio on the admin page and disable both keys (as after Venice).
- Clear the room chat for `geneva`.
- `python3 tools/events_report.py` on the day's log, and `tools/room_scores.py --label Geneva --day 2026-12-04` for the jagged-frontier slide.
