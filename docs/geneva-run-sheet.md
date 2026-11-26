# Geneva, 4 December 2026: run sheet for the one-session studio

*AI for Human Rights Professionals*, Geneva Human Rights Hub, ITU, Day 3. One session of 90 minutes, up to 30 participants (diplomats, NGO, NHRI and UN staff), one app: the **Verbatim finder** for the treaty bodies' General Comments. The studio is `lszoszk.github.io/workshop-studio/?course=geneva`; the QR code on each seat card opens it with the seat code. The two-session path of November stays available as `?course=full` (tag `two-sessions-2026-11-15`; its session plan is in `docs/archive/`).

The arc in one line: **data → prompt → plan → change the plan → build → test → improve → wall → teaser.** The progress bar under the studio's header follows the same seven steps, so the room can see where everyone is.

Draft status: the times below are planned, not yet measured; measure them at the dry run and replace them.

## Before the day

- [ ] **Keys and money** (see `server/RUNBOOK.md`): the OpenRouter key "zajecia" and the Anthropic key "garage-research" are enabled; the studio is resumed on the admin page; `STUDIO_ANTHROPIC_CAP` raised to about $150; the OpenRouter balance at least $100 and the key's own limit at least $150.
- [ ] **Default model** on the admin page: Claude Sonnet 5.5 (the course already starts on it; the admin setting covers requests that name no model).
- [ ] **Certificate**: `echo | openssl s_client -connect 150.254.115.204:443 2>/dev/null | openssl x509 -noout -enddate` shows a date after 4 December (certbot renews it twice a day; check anyway).
- [x] **Trial builds, Sonnet** (17.11, in Claude Code, no API): one app per look (paper, night, UN blue, newsprint, index cards), each 6/6 on the bake-off checks (`tests/bakeoff/2026-11-17-g1-looks-*`); the paper build is the recorded app behind **Load a working version**.
- [x] **Trial builds, GLM** (17.11, through the live studio, one seat): 17–20 s and $0.02–0.06 each; four of five 6/6, the night look 4/6 (a script error as it opens: "Cannot set properties of null", the kind the studio sends back once by itself). Both models keep footnote marks such as `[[fn:42]]` in the text as stored, as the plan asks; worth a word in the room ("the marks are the file's, not an error").
- [ ] **Load test**: 30 builds at once on Sonnet (about $10), then 5 on GLM; note the times here.
- [ ] **Seat cards** printed with the QR code to `?course=geneva` and the seat code; budget per seat $8.
- [ ] **Room chat**: the facilitator's page `…/studio-api/admin/room?key=…&course=geneva` open on your phone or laptop; test one message to the room.
- [ ] **Wall**: `lszoszk.github.io/workshop-studio/wall.html?course=geneva` in a second window.
- [ ] **Teaser**: `python3 tools/teaser/teaser_watch.py --course geneva --day 2026-12-04 --upload` running on your laptop from the start of the session; `site/teaser.html` open in a third window (full screen with F).
- [ ] **Organisers' consent** to show participants' chosen names on the wall and in the teaser (the name is optional; without one, the wall shows the app alone).

## The session (90 minutes)

| Min | You | The room in the studio | Progress |
|---|---|---|---|
| 0–8 | **Why we do this.** Uploading a document to a chatbot gets you a paraphrase you cannot cite and cannot check; building a small tool on clean data gets you the exact words with their source, every time. Login over the first minutes (QR code on the card). | Log in; the studio opens on the data card (and, on a first visit, the tour). | – |
| 8–18 | **The data.** Structured data from Hugging Face (the UN Human Rights Database): why paragraphs with symbols and numbers beat PDFs; what is in the file and what is not. Look at it before you ask for anything. | The studio opens on **First, your data**: the counts of the file; **Look inside the file**: three records as JSON, the fields, the Hugging Face link. | 1 Data |
| 18–28 | **What a prompt is.** Ethan Mollick's delegation questions (slide, links below): what and why, the limits, what "done" looks like, what to check before finishing; and the rule of this session: **plan first** (more agency for you, a better result, no rabbit hole at the start). | **Write your prompt**: fill in **My topic**, switch paragraphs off or rewrite them, Send. The planner looks at the file too (its counts are the participant's own). | 2 Prompt |
| 28–43 | **The plan (a simulation).** The planning session was recorded with Claude Fable 5.1; the plan is short on purpose. Pairs: read it, argue about the three decisions (what counts as a match, how a citation reads, what a result shows first). | Answer the three cards; read the plan (about 380 words). | 3 Plan read |
| 43–50 | **Change the plan.** Two ways, both reach the build: ask in the chat ("Change the plan: …") or press **Edit the plan** and type. The look of the app (five looks, one per seat at random) can be changed too. | Edit, then **Build from this plan**. | 4 Plan approved |
| 50–58 | **While it builds:** the jagged-frontier slide (`/slides/jagged-frontier.html`): no model is best at everything; test a model on your own task. | Claude Sonnet (default) or GLM-5.3, their choice; say the difference honestly (Sonnet: no build error in Venice, no zero data retention; GLM: open weights in the EU, more errors). | 5 App built |
| 58–68 | **Does it work?** Three checks on the card **Test your app**: a phrase you know, word for word; one paragraph against its source; a pasted citation with symbol and paragraph. Brainstorm in pairs: one thing to change. | Tick the three checks; write "One thing I would change". | 6 Tested |
| 68–80 | **Improve it.** **Suggest three improvements** (three alternatives each time) or their own idea; pick, edit or reject; build one change. | Build one change (15–60 s). | 7 Improved |
| 80–85 | **The wall.** At 100% the studio asks whether to show the app to the room, with an optional name. Two or three apps on the projector: what they found, what they checked. | **Send to wall**. | 100% |
| 85–90 | **The teaser.** Full screen: 30 seconds made from the room's apps while they worked. Take-home kit (About → Take-home kit): their prompt, plan and app, the data, and **At home**: a dashboard on Human Rights Council votes 2006–2026 to build with their own chatbot. Feedback form. | Download the kit. | – |

## Slide notes: sources to show (all checked 16.11.2026)

- Ethan Mollick, [Management as AI superpower](https://www.oneusefulthing.org/p/management-as-ai-superpower) (27 January 2026): delegation documentation answers what we are trying to accomplish and why, where the limits of the delegated authority are, what "done" looks like, what outputs and interim outputs are needed, and what to check before saying it is finished. The prompt's five paragraphs map onto these questions (each block shows its question).
- Ethan Mollick, [Getting started with AI: Good enough prompting](https://www.oneusefulthing.org/p/getting-started-with-ai-good-enough) (24 November 2024): treat it like a new coworker; give context; ask it to ask you questions.
- Ethan Mollick, [Agency and Agents](https://www.oneusefulthing.org/p/agency-and-agents) (31 August 2026): agents should come back to people for approval, expertise, variance and the interesting decisions; otherwise "we will have automated the wrong half of the job". This is why the plan stops for your three decisions.
- The data: [treaty-bodies-general-comments on Hugging Face](https://huggingface.co/datasets/lszoszk/treaty-bodies-general-comments) and the [UN Human Rights Database](https://lszoszk.github.io/generalcomments/).
- The jagged frontier: Dell'Acqua et al., [Navigating the Jagged Technological Frontier](https://doi.org/10.1287/orsc.2025.21838), *Organization Science* (2026).

## When something goes wrong

The backup plan is **recorded mode**. When the model API fails for any reason, a participant or you switch the studio to the answers recorded beforehand with Claude Sonnet 5.5. In Geneva recorded mode covers the whole session: all seven steps, everything except the wall. Nothing is sent to a model, and the participant's work (versions, plan, progress, test card) stays.

1. **An error as the app opens:** the studio sends it back to the model once by itself. Wait.
2. **Still an error in red:** **Ask the model to fix it**; after two failed fixes, **Load a working version** (a Sonnet build of the default plan recorded before the day) and go on from there.
3. **Stuck on a step:** every step of the progress bar has **Skip**, so nobody misses the wall.
   **Ahead of the room:** a step that is done (or skipped) on the bar is a button back to it; nothing done is lost, and every app stays in the versions. Say which step: **Data** opens the file; **Prompt** brings the prompt card back with what was sent (Send starts a new plan, Cancel folds it up); **Plan read** or **Plan approved** brings back the plan the app was built from, with **Change my answers** (the three questions again, the earlier answer marked; no model needed); building from it makes a new app beside the first. A skipped step clicked this way is no longer skipped.
4. **The model is slow or failing for one person:** the error box has three buttons: **Try again**, **Use the other model** and **Continue with recorded answers**. The studio never switches a participant's model silently; it asks.
5. **The model is failing for the whole room:** open the admin page and press **Recorded answers for everyone** (next to the kill switch). Within about 20 seconds every open page switches by itself and says why; the badge shows **Recorded answers**. When the model is back, press **Back to the live model**: nobody is switched back automatically, each page offers **Back to the live model** in a note and in the badge.
6. **A participant's own switch:** the route badge at the top ("Live model") is a button. It explains recorded answers and offers **Switch to recorded answers**; in recorded mode it offers **Back to the live model** (it needs the seat code).
7. **The server is gone (Wi-Fi, the university server):** after two failed health checks in a row the page offers **Continue with recorded answers** in a note; it never switches by itself, because a Wi-Fi glitch should not cost anybody the live model. The recordings are loaded into the page at the start, so an open tab keeps playing them with no network at all.
8. **What works in recorded mode:** the data card, the prompt and the plan, **Build from this plan** (it plays the app recorded beforehand from the recommended answers on the topic *the rights of the child*, in the plan's look), the test card, **Suggest three improvements** (three recorded ideas), **Build this** on any of them (the improvement recorded for that idea and look), the take-home kit. Not in recorded mode: changing the plan, editing an idea, three other ideas, your own idea (they need a live model; the studio says so), and the wall (**Send to wall** is off, "in recorded mode your app stays here").
9. **Two independent providers:** paste a Claude key on the admin page (Model keys) so that Claude goes straight to Anthropic and GLM goes through OpenRouter. If one provider fails, the other model is still live.
10. **The teaser is not ready:** the last good version is always in `tools/teaser/out/latest.mp4` on your laptop; play it from there.
11. **The last resort:** the take-home kit (**Save & share**, or About) is one file that holds the requests, the data and five recorded apps ("Recorded app: Paper and ink", and four more looks). It opens with a double-click and shows working apps with no model and no internet.

## After the session

- Pause the studio on the admin page and disable both keys (as after Venice). If you had switched to recorded answers for everyone, press **Back to live models** first, so the next course starts live.
- Clear the room chat for `geneva`.
- `python3 tools/events_report.py` on the day's log, and `tools/room_scores.py --label Geneva --day 2026-12-04` for the jagged-frontier slide.
