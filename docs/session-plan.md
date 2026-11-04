# Session plan: Sessions 7 and 8, 4 December 2026

*AI for Human Rights Professionals*, Geneva Human Rights Hub, ITU Geneva, Day 3. Up to 30 participants: diplomats, and staff of NGOs, national human rights institutions and the UN. Each has a badge with a QR code and a seat code; the studio runs on their own laptop.

- **S7, 09:30–11:00**: Working with Human Rights Documents and Data – NLP and AI in Practice. *What clean data lets you do.*
- **S8, 11:15–12:45**: Using Generative AI with UN Human Rights Sources. *Where clean data comes from, and generation as the last resort.*

The rhythm is the same in both: **use** a ready request, **modify** it, **create** something of your own (Use–Modify–Create). The studio shows little at first and more as people progress, so the facilitator's job is to say what to click next, not to explain the whole screen.

**Time.** Each session is planned for 75 minutes, with the last 15 kept free. A room of 30 loses that much to logins, stragglers and the moves between tasks, and one build takes a participant 5–7 minutes from choosing the request to understanding the result.

**The arc: three apps and a demo.** S7 is what clean data lets you do: the **dashboard** for the participant's own country (the UN's recommendations, UHRI data; it is not the HRC Voting tool), with the next step *Check ten at random* (validate the UN's labels) and, as an extra, *Who recommends what*. S8 is where clean data comes from, and generation as the last resort: **paragraphs out of a PDF** (CESCR General comment No. 27) with two next steps, *Add a second document* (CCPR General comment No. 32) and *A model for the pages that fail*; then the reveal that the data already exists as published data; then the **Verbatim finder** on that data. The **research wiki** on neurotechnology in the administration of justice is a 5-minute facilitator demo at the end; participants who finish early may build it themselves, with its next step *A map of the wiki*. The other requests stay in the studio as extras.

**One frame for both: the method ladder** (material 11, below). The least intrusive means first, as in the proportionality test the room knows.

**Plan first, then build.** A workshop request sent in plan mode replays a planning session recorded with Claude Fable 5.1: the planner's log, its looks at the data and its searches of the reference shelf, then 4–5 question cards with fixed answers. The plan assembled from the answers opens on the stage, and the model the participant chose builds it live (recorded mode builds only the recommended answers). This is a simulation, and the studio says so; say it too. The point to make the first time: "this is how you work with an agent: a plan you have read and decided on, then execution."

## Before the room fills (09:00)

- **From 09:15 the link and a large QR code are on the screen**, with one line: "Open this on your laptop and enter the seat code from your badge." Participants log in over coffee; each co-facilitator takes a row and helps. Logging in during the session would cost 8–10 minutes, the largest single risk of the morning.
- The studio opens with a short **tour** (eight steps, once per browser; *Tour* in the footer starts it again). Let participants click through it while they log in.
- Studio open on the projector at `https://lszoszk.github.io/workshop-studio/?wall=1` in a second window (the app alone, for showing a participant's work), and the normal studio in the first.
- `/health` of the VM answers (RUNBOOK); OpenRouter balance at least $300; the key's own limit raised or removed.
- Slides at hand: Budapest slide 4 with its video (`~/Desktop/AI/HURIDOCS/AI presentation/ECCHRD_Budapest_2026/`, `assets/film_coding.mp4`; slide 22 if the video fails), slide 21, and the WSIS "Execute / Decide / Deliver" slide (`~/Desktop/talks/wsis2026/index.html`).
- **Two browser tabs ready for the S8 reveal**: the API JSON (`https://lszoszk.github.io/generalcomments/corpus.json`) and the Hugging Face page (`https://huggingface.co/datasets/lszoszk/treaty-bodies-general-comments`).
- **The wall** open in a third tab: `https://lszoszk.github.io/workshop-studio/wall.html`. Every app a participant sends with *Send to wall* (it needs a seat code) appears there as a live thumbnail on that participant's country and files, within ten seconds; a click opens it full screen. A page can be taken down on the admin page.
- A seat code, or your own laptop, for the model step in S8: recorded mode cannot run it.
- The eight cards for "What may leave the room" (S8), printed or on one slide.

## How long the model takes

Visible thinking starts within 1–6 seconds; a whole app takes:

| Request | Mistral (high) | Claude (high) | GLM (low) |
|---|---|---|---|
| Dashboard, next steps | 60–175 s | 55–130 s | 35–50 s |
| Paragraphs out of a PDF | about 3 min | about 3 min | about 1 min |
| A research wiki (old library, to re-run) | about 80 s | about 85 s | about 35 s |
| Check an AI briefing (extra) | 4–5 min | about 4 min | about 1 min |

These timings are from the earlier plans. They must be measured again at the dry run (around 20 November) with the new plans; the new next steps (*Check ten at random*, *Add a second document*, *A model for the pages that fail*) have no timing yet.

Use the waiting time: the stage shows the model's thinking, then its code. That is the moment to say what is happening. The PDF request is the slow one in this plan: say beforehand that GLM or Claude are faster. The reasoning setting does not speed Mistral up: low and high take about as long.

---

## The frame for both sessions: the method ladder

**11. The method ladder.** Use the least intrusive means that does the job, as in the proportionality test the room knows: legitimate aim, suitability, necessity, proportionality in the strict sense. Five rungs, from the bottom:

1. **Published data** (an API, a dataset on Hugging Face): nothing to extract.
2. **Deterministic code** (rules, regular expressions): the same result every time, readable, auditable.
3. **Measured machine learning** (OCR, classifiers): probabilistic, with known error rates.
4. **A model inside the tool** for narrow, checkable decisions (labels, line numbers), checked by code.
5. **Free text generation**: the measure of last resort; every claim pinned to its source and verified.

Across all rungs, generative AI is the toolmaker, not the oracle: it writes the code of rungs 2–4, code a person can read, run three times and audit. That is the real democratisation: a human rights expert builds in an hour a pipeline that once needed a programmer.

How to use it. In S7 (09:38) three sentences, no more: the least intrusive means first, as in the test you know; five rungs, from published data to free text; AI as the toolmaker, not the oracle. In S8 name the rung at every step, and recap the five rungs at the close. Say "generation is a choice of method". Harms are Session 9's topic (Tech Harms Check) and agents Session 10's: do not go there. In the studio, *Look inside* → *Layers*, *Run it three times*, *Cut the model link* and *What left this laptop* are the tools for each step of the test.

---

## Session 7 (09:30–11:00): what clean data lets you do

| Time | Min | What happens | In the studio | Material |
|---|---|---|---|---|
| 09:30 | 3 | Welcome. Anyone not logged in yet does it now, with a co-facilitator. | Seat code, country, Session 7 | |
| 09:33 | 5 | **Four objections**: quality, hallucinations, confidentiality, security. "Each of them gets an answer on your screen today." | | 1 |
| 09:38 | 3 | **The method ladder**, in three sentences: the least intrusive means first; five rungs, from published data to free text generation; AI as the toolmaker, not the oracle. Session 7 stays at the bottom: what clean data lets you do. | | 11 |
| 09:41 | 2 | Your files, **on the projector**: you open the country file in Excel. This is the data, one UN paragraph per row: the UN's recommendations to your country. | *Your files* → **Open** | |
| 09:43 | 5 | Everyone picks **Your country's recommendations dashboard**, drags the country file in and sends it in plan mode: the recorded planning session plays (the planner's log, its looks at the data, 4–5 question cards). Answer the cards; the plan opens on the stage; the model you chose builds it. Say that this is a simulation. While the model thinks: "you planned; now it plans the code in words, then writes it." | Plan mode; question cards | |
| 09:48 | 5 | First apps on screen. **A probabilistic model builds deterministic tools.** Play the video (82 s). | | 2 |
| 09:53 | 6 | **Run it three times**: three identical checksums; the model was involved once, when it wrote the code. Then **Layers**: what the model wrote (amber) and what the code computes (green). The counting is rung 2 of the ladder. | *Look inside* | |
| 09:59 | 3 | **Deterministic is not the same as correct**: the HRC Voting audit. Say that it is from another of your tools. | | 3 |
| 10:02 | 15 | Modify, in their own words: a change to the dashboard (another chart, a filter, a column). Show **App / Code**: "AI writes in these languages; your browser turns them into what you see." **New tab** opens the app full screen. Then **Send to wall**: on the projector, three dashboards from three countries side by side. | Message box; *App / Code*; *New tab*; *Send to wall*; the wall | |
| 10:17 | 15 | **Next step: Check ten at random.** Validate the UN's labels on ten recommendations picked at random: clean data is not the same as correct labels. | *Next step* → *Check ten at random* | |
| 10:32 | 7 | **Red-team your own tool**: three questions it should answer wrongly. Try them. | | 4 |
| 10:39 | 6 | Close: **what clean data lets you do.** The dashboard works because every row is one clean UN paragraph. Where does clean data come from? That is Session 8. Save the app. | **Save as file** | |
| 10:45 | 15 | **Kept free.** Whatever ran over; then questions. Extra for the fast: *Who recommends what*. | | |

**1. Four objections.** Source: `~/Desktop/inne/thread_ai_hr_workflows.md`. The lines to keep: "scripts are deterministic. You can run one a thousand times and get the same result each time"; where the material is not public, "the assistant writes the script from a synthetic document with the same format and structure"; and "you can run it on your own laptop with wi-fi turned off, so the documents themselves never reach the AI model". In the studio each objection has its answer: *Run it three times* (hallucination, quality), *What left this laptop* (confidentiality), *Save as file* plus the cut model link (security).

**2. Budapest, slide 4.** "A probabilistic model builds deterministic tools — then the tool, not the model, gives the answer." Three beats from the speaker notes: probabilistic is not a product; its real strength is writing code; the tool is deterministic. Video `film_coding.mp4`; if it does not play, slide 22.

**3. HRC Voting audit, finding A1** (`~/Desktop/HURIDOCS/OHCHR_voting/notes/AUDIT-2026-07.md`). Say that it comes from another of your tools, not from the dashboard, and that it shows deterministic is not the same as correct. "Most often outvoted" was computed from the most frequent vote, not the winning side: in 53 resolutions the text was carried and every State that voted yes, the winning side, was scored as outvoted. The audit's own summary: four measures "are documented as one thing" and implemented as another. One slide: same code, same wrong answer, every time.

**4. Red-teaming.** From the IHRL course plan, session 8 "Kuźnia" (`~/Desktop/UAM/Zajęcia 26-27/IHRL/mapa-ai-i-prawo/kurs/plan_zajec.md`). Examples to seed it, which suit the dashboard: a mandate that did not exist in a given year; a keyword with two spellings; a State that changed its name; a filter that leaves nothing.

---

## Session 8 (11:15–12:45): where clean data comes from, and generation as the last resort

| Time | Min | What happens | In the studio | Material |
|---|---|---|---|---|
| 11:15 | 3 | Back from the break. Switch to **Session 8** (top bar): two new tools under *Look inside*. Recall the ladder in one sentence. | Session 8 | 11 |
| 11:18 | 5 | **Ask the model directly: a quotation.** "Quote paragraph 97 of General comment No. 27." The document has 90 paragraphs. Read the three answers aloud before revealing the box. This is generation as an oracle, rung 5 done wrong, before the ladder is climbed from the bottom. | *Look inside* → *Ask the model directly* → *A quotation* | 11 |
| 11:23 | 3 | **A document, not a table.** Open the PDF of CESCR General comment No. 27 from *Your files*: this is what the UN publishes. Everyone writes down how many of its 141 footnotes they expect a script to find. | *Your files* → PDF | |
| 11:26 | 12 | Drag the PDF into the chat, send **Paragraphs out of a PDF** in plan mode (about 3 min with Mistral: say that GLM or Claude are faster). Rung 2: the model writes the script, the script does the work. The recorded build found 90 of 90 paragraphs and 141 of 141 footnotes, and passed 9 of 9 of the app's own checks. Compare with the guesses, and with the gallery: the earlier builds, made from a shorter plan without the footnote rules, found all 90 paragraphs but 13, 129 and 0 footnotes. The plan made the difference. A converter damages text in four ways (order, breakage, loss, noise); a script repairs only what you tell it about. | *Your files*, Send; Gallery | |
| 11:38 | 7 | **Add a second document**: drag *CCPR General comment No. 32 (PDF)* into the chat. The same pipeline, unchanged, on an older layout (2007): 65 of 65 paragraphs, but 109 of 128 footnotes, and 4 of its 9 checks fail. "A pipeline that works on one document is a hypothesis about the next." This is where rung 2 stops. | *Your files* → CCPR GC 32; *Next step* → *Add a second document* | |
| 11:45 | 12 | **A model for the pages that fail.** Script first; only the pages whose checks fail go to the model, one page per call; the model labels lines and never retypes text; the code cuts the text and runs the checks again (details below). Rung 4. On pages 2–4 of GC 32, Claude Sonnet marked all 22 footnotes right. Say the limits: it costs, it varies between runs, errors the checks do not see stay. Recorded mode cannot run this step: show it with a seat code, or as a facilitator demo. Then **What left this laptop**: the pages that were sent, the failing ones and the control. Then **Cut the model link**: script first, so the first pass never needed it. | *Next step* → *A model for the pages that fail*; *Look inside* → *What left this laptop*, *Cut the model link* | 11 |
| 11:57 | 4 | **The data already exists.** Switch to the two browser tabs on the projector: the API JSON and the Hugging Face dataset. The extraction app checked itself against this data all along. Rung 1: nothing to extract. Nobody downloads in the app (it has no internet access, by design): the *General Comments, paragraph by paragraph* file is that data. | Two browser tabs; *Your files* → *General Comments, paragraph by paragraph* | 12 |
| 12:01 | 8 | **Verbatim finder for General Comments**, built on that data (drag the *General Comments, paragraph by paragraph* file in). Search for something from their own work. | New app | |
| 12:09 | 4 | **Generation for navigation; retrieval for substance.** The machine finds; the lawyer decides. Then the ✓ / ≈ / ✗ numbers. If there is time, on the Verbatim finder: *Look inside → Ask the model directly → A number* asks how many numbered paragraphs General Comment No. 36 has (70 in the data). On 4 November GLM answered 79, 70, 79, Mistral 70, 74, 70, Claude 70 three times with "as far as I recall": the typical error is ≈, sure of itself. | *Look inside* → *Ask the model directly* → *A number* | 6, 7 |
| 12:13 | 6 | **What may leave the room**: eight cards, three piles. The model step sent pages of a public UN text; what else may go? | | 8 |
| 12:19 | 5 | **The research wiki: a facilitator demo.** On the projector, from the library on *Your files*: open *mental privacy*, click a pin: the quotation stands in the sentence, its citation beside it ("A/81/351, para. 24" or "Szoszkiewicz & Yuste 2025, p. 3471"). The PDF opens next to the app, at its page, with the quoted passage marked. Then **02 Ask** a question (this needs a seat code) and check one pin of the answer by clicking it. Generation with every quotation checked: rung 5 done right. | *Your files* → Library; PDF drawer | 10 |
| 12:24 | 4 | Close: **the method ladder.** Recap the five rungs from the bottom and put the morning on them: published data (the reveal), the script (rung 2), the model for the failing pages (rung 4), the quotation (rung 5 done wrong), the wiki (rung 5 done right). "Generation is a choice of method." Then **Execute shrinks, Decide grows, Deliver is the point.** HRC Voting: one evening, then more than 50 fixes over ten weeks. | | 11, 5 |
| 12:28 | 2 | **Suggest improvements** (the model lists five changes to their app in a few seconds; building them is for later), and **Take it further** in the footer: the open tools, a prompt to review code at home, and its warning that such assistants send what they read to the company that runs the model. Save the app. | Next step; footer | |
| 12:30 | 15 | **Kept free**, for whatever ran over; then questions and what to try next week. If time is left: **check the checker** from the gallery. | Gallery | 9 |

**The extraction app, in numbers.** *CESCR General comment No. 27*, recorded build: 90 of 90 paragraphs, 141 of 141 footnotes, 9 of 9 of the app's own checks. *CCPR General comment No. 32* (2007), the same pipeline unchanged: the layout is older (a two-line header, "CCPR/C/GC/32 / Page n"; footnote numbers on their own line above the text; the numbers of a page's first footnotes moved to the end of the page), and the result is 65 of 65 paragraphs, 109 of 128 footnotes, and 4 of the 9 checks failing. *The model step*: the script runs first; only the pages whose checks fail go to the model, one page per call. The model says which lines are paragraph text, footnotes (with their numbers) or headers and footers, and never retypes text. The code cuts the text from the line numbers and runs the same checks again. It accepts a page only if every line is used exactly once, the footnote numbers continue from the page before, and every footnote mark has its footnote. One page that passed goes along as a control. On GC 32 every page fails at least one check (the older layout breaks each of them), so all 18 pages go to the model and none is left to serve as a control: the app says so, and says before it sends that 18 pages will leave the browser. In a test on pages 2–4 of GC 32 (4 November 2026), Claude Sonnet marked all 22 footnotes right, including the three whose numbers the converter had moved. The honest limits: it costs, it varies between runs, and errors the checks do not see stay. Recorded mode cannot run this step, because it calls a model: show it with a seat code, or as a facilitator demo.

Extras for those who finish early: build the **research wiki** from the demo (with its next step *A map of the wiki*), **Check an AI briefing**, **A model inside the tool** (on their S7 dashboard), **How two States vote at the Human Rights Council**.

**12. The data already exists.** The reference the extraction app checked itself against all along is published data: the UN Human Rights Database API; `https://lszoszk.github.io/generalcomments/corpus.json` (every paragraph, with footnotes); and the Hugging Face dataset `https://huggingface.co/datasets/lszoszk/treaty-bodies-general-comments`. Open both in browser tabs on the projector. The apps in the studio have no internet access by design (part of the confidentiality answer), so participants do not download in the app: the *General Comments, paragraph by paragraph* file on *Your files* is that data, and its card now links the API and Hugging Face. The Verbatim finder is then built on it. This is rung 1: where the ladder starts.

**6. Budapest, slides 19 and 21.** "Generation for navigation; retrieval for substance." "The machine finds. The lawyer decides." The verbatim finder is that principle: it can only return paragraphs that exist, with their symbol and number.

**7. ✓ / ≈ / ✗.** From the IHRL class of 23 October 2026 (`kurs/demo/tablica/dane.json`): questions on ECtHR case law (Glukhin, S. and Marper, Bărbulescu), answers checked one by one. Without retrieval: 31 right, 7 nearly right, 1 invented. With retrieval: 36, 1 and 0. Say that it was a class exercise on the Strasbourg Court, not on UN sources. The point: in 2026 the typical error is ≈, a real case with a wrong detail, which is harder to catch than an invented one.

**8. What may leave the room.** From AI4HR, "Hall of mirrors" (`~/Desktop/inne/AI4HR/modules/02-hall-of-mirrors/card.md`). Three piles: *paste into a hosted model*, *never*, *depends*. "Push for the condition, not the verdict." Cards for this room:

1. A published UPR report
2. A draft resolution under negotiation
3. Instructions from your capital
4. An NHRI complaint file with the complainant's name
5. A witness statement naming a person and a village
6. An anonymised interview transcript
7. Your own draft speech
8. A colleague's unpublished analysis

Vote by show of hands, card by card; spend the time on the "depends" pile.

**10. The research wiki.** The method of the book's knowledge base (`~/Desktop/The Book/00_PROJECT/wiki/WIKI.md`): the author chooses the sources, agents write and file the pages, and every factual claim carries "an inline link straight to its source", a PDF opened at its page. The workshop app does the same on a small scale: the pages were written by agents beforehand; in the app the code checks every quotation against its passage, the model answers questions and drafts the changes a new source brings (*Ingest*), a person approves each change, and every quotation is one click from its page. The workshop library (2 November 2026) is profiled on neurotechnology in the administration of justice: 9 documents, 945 passages, each with the PDF page it starts on (to open) and the page printed there (to cite). Passages come from the PDFs (PyMuPDF; footnotes, running heads and pull quotes dropped), General Comment paragraphs from the UN Human Rights Database. The UNODC–INTERPOL *assessment draft* is confidential and is not used; the public background paper is.

The nine documents, of six kinds: the Secretary-General's report A/81/351 (27 August 2026), the UNODC–INTERPOL background paper, the Futures Lab submission to that report, the Australian Human Rights Commission's *Peace of Mind*, two journal articles and three CCPR General Comments. Their weight differs; the wiki shows which is which. For the demo: footnote 7 of the Secretary-General's report cites the EMBO article, so two kinds of source stand on one page. For those who build it themselves: send the request in plan mode with the *Research wiki* file dragged in (it brings the library with it), then the next step *A map of the wiki*.

A finding to use (from the earlier General Comments library, 1 November 2026): the exact word *proportionality* occurred in 8 paragraphs, every form of the word in 12, because CRPD General Comment No. 6 speaks of a *disproportionate* burden, a different test. The rule the code applies decides what the concept is. To redo on the new library after the bake-off; in it, "deception detection" without "lie detection" occurs in A/81/351 paras 20 and 53, which a wiki that searches one term misses.

**5. WSIS 2026 slide** (`~/Desktop/talks/wsis2026/index.html`): "EXECUTE shrinks / DECIDE grows / DELIVER is the point". The honest version, from the UMCS panel notes: the first working HRC Voting was built in one evening (7 July 2026, Geneva), then more than 50 fixes over ten weeks; the evening was enough because the domain knowledge was already there.

**9. Check the checker** (optional, in the free time). In the gallery, *Check an AI briefing*: three apps, three models. On the projector, paste this briefing into each (it has five planted errors: 50th session, 20 against, 6 abstentions, India "abstained", and a mandate claim the voting data cannot check):

> Resolution A/HRC/RES/51/27 on the situation of human rights in Ethiopia was adopted by the Human Rights Council on 7 October 2022, at its 50th session, by a recorded vote of 21 in favour, 20 against and 6 abstentions. The text was presented by the European Union. The United States, Germany and Finland voted in favour; China, Pakistan and Eritrea voted against. India abstained, as did Indonesia. The resolution extended the mandate of the International Commission of Human Rights Experts on Ethiopia for one year.

What the apps did (1 November 2026, `tools/briefing_probe.py`): Claude's found all four checkable errors and confirmed the rest; Mistral's caught two, missed the abstentions and called two correct claims wrong; GLM's, which passed all eight automatic checks, misread the sentences and called eight claims wrong, including one that is not in the text. The lesson card: test a checker on errors you planted yourself before you trust it.

---

## When something fails

| Problem | What the room sees | What to do |
|---|---|---|
| The VM does not answer | A note in the chat: switched to the backup server (the badge still says "Live model") | Nothing: the studio has switched |
| A model's host fails | The answer comes from another model: Mistral falls back to GLM run in the EU, Claude to Mistral | Nothing to fix. The app card and *What left this laptop* name the model that answered: worth pointing out if someone chose a model for its origin |
| No model at all | "Recorded answers" | The workshop requests still work as recordings; free chat does not, nor do the steps that call a model from inside an app (*A model for the pages that fail*, the wiki's *Ask* and *Ingest*). Use the gallery. |
| One seat out of budget | A message naming the budget | Top up the seat on the admin page |
| The account is out of credit | "The studio's account with the model service has run out of credit" | Top up OpenRouter; the balance is on the admin page and in `/health`. Recorded answers and saved apps keep working |
| Someone reports a problem | They press *Feedback* in the footer | Read it on the admin page (Feedback), with the version, browser, app and model it came from |
| A build takes too long | The thinking or code keeps streaming | Stop, switch to GLM, send again |
| An app breaks | "Something in the app broke" | *Ask the model to fix it*; after two failed fixes the studio offers a fresh start |
| Wi‑Fi down | Nothing loads | The saved files (*Save as file*) open offline; continue from the gallery on the facilitator's laptop |
