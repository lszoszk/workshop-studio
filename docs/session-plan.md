# Session plan: Sessions 7 and 8, 4 December 2026

*AI for Human Rights Professionals*, Geneva Human Rights Hub, ITU Geneva, Day 3. Up to 30 participants: diplomats, and staff of NGOs, national human rights institutions and the UN. Each has a badge with a QR code and a seat code; the studio runs on their own laptop.

- **S7, 09:30–11:00**: Working with Human Rights Documents and Data – NLP and AI in Practice
- **S8, 11:15–12:45**: Using Generative AI with UN Human Rights Sources

The rhythm is the same in both: **use** a ready request, **modify** it, **create** something of your own (Use–Modify–Create). The studio shows little at first and more as people progress, so the facilitator's job is to say what to click next, not to explain the whole screen.

**Time.** Each session is planned for 75 minutes, with the last 15 kept free. A room of 30 loses that much to logins, stragglers and the moves between tasks, and one build takes a participant 5–7 minutes from choosing the request to understanding the result.

**Four apps, each different.** Two per session, each on other data and doing a different job: S7 the **dashboard** (a country's recommendations: count and explore) and **paragraphs out of a PDF** (a document into structure); S8 the **Verbatim finder** (General Comments: retrieve exact text) and **a research wiki on neurotechnology in the administration of justice** (nine documents of six kinds: organise what an institution knows). The other requests stay in the studio as extras.

**Plan first, then build.** Each of the four apps opens as a plan on the stage, drafted beforehand with Claude Fable 5.1 (`tools/draft_plans.py`, drafts in `tools/out/plans/`): Goal, The data, What the app shows, Rules for the code, How we will know it works, Your decisions, Not in this version. Participants put the file in the chat, read the plan, edit any sentence, set three or four decisions (the yellow words: things a human rights professional decides better than a model), add what is missing, and press **Build from this plan**. The point to make the first time: "this is how you work with an agent: a plan you have read and changed, then execution." In recorded mode only the unchanged plan builds.

## Before the room fills (09:00)

- **From 09:15 the link and a large QR code are on the screen**, with one line: "Open this on your laptop and enter the seat code from your badge." Participants log in over coffee; each co-facilitator takes a row and helps. Logging in during the session would cost 8–10 minutes, the largest single risk of the morning.
- Studio open on the projector at `https://lszoszk.github.io/workshop-studio/?wall=1` in a second window (the app alone, for showing a participant's work), and the normal studio in the first.
- `/health` of the VM answers (RUNBOOK); OpenRouter balance at least $300; the key's own limit raised or removed.
- Slides at hand: Budapest slide 4 with its video (`~/Desktop/AI/HURIDOCS/AI presentation/ECCHRD_Budapest_2026/`, `assets/film_coding.mp4`; slide 22 if the video fails), slide 21, and the WSIS "Execute / Decide / Deliver" slide (`~/Desktop/talks/wsis2026/index.html`).
- The eight cards for "What may leave the room" (S8), printed or on one slide.

## How long the model takes

Visible thinking starts within 1–6 seconds; a whole app takes:

| Request | Mistral (high) | Claude (high) | GLM (low) |
|---|---|---|---|
| Dashboard, next steps | 60–175 s | 55–130 s | 35–50 s |
| Paragraphs out of a PDF | about 3 min | about 3 min | about 1 min |
| A research wiki (old library, to re-run) | about 80 s | about 85 s | about 35 s |
| Check an AI briefing (extra) | 4–5 min | about 4 min | about 1 min |

Use the waiting time: the stage shows the model's thinking, then its code. That is the moment to say what is happening. The PDF request is the slow one in this plan: say beforehand that GLM or Claude are faster. The reasoning setting does not speed Mistral up: low and high take about as long.

---

## Session 7 (09:30–11:00)

| Time | Min | What happens | In the studio | Material |
|---|---|---|---|---|
| 09:30 | 3 | Welcome. Anyone not logged in yet does it now, with a co-facilitator. | Seat code, country, Session 7 | |
| 09:33 | 5 | **Four objections**: quality, hallucinations, confidentiality, security. "Each of them gets an answer on your screen today." | | 1 |
| 09:38 | 2 | Your files, **on the projector**: you open the country file in Excel. This is the data, one UN paragraph per row. | *Your files* → **Open** | |
| 09:40 | 5 | Everyone picks **Your country's recommendations dashboard**: a plan opens. Drag the country file in, read the plan for a minute, set the four decisions, **Build from this plan**. While the model thinks: "you planned; now it plans the code in words, then writes it." | Plan → *Build from this plan* | |
| 09:45 | 5 | First apps on screen. **A probabilistic model builds deterministic tools.** Play the video (82 s). | | 2 |
| 09:50 | 6 | **Run it three times**: three identical checksums; the model was involved once, when it wrote the code. Then **Layers**: what the model wrote (amber) and what the code computes (green). | *Look inside* | |
| 09:56 | 3 | **Deterministic is not the same as correct**: the HRC Voting audit. | | 3 |
| 09:59 | 15 | Modify, in their own words: a change to the dashboard (another chart, a filter, a column). Show **App / Code**: "AI writes in these languages; your browser turns them into what you see." **New tab** opens the app full screen. | Message box; *App / Code*; *New tab* | |
| 10:14 | 4 | **The second app: a document, not a table.** Open the PDF of CESCR General comment No. 27 from *Your files*: this is what the UN publishes. Everyone writes down how many of its 141 footnotes they expect a script to find. | *Your files* → PDF | |
| 10:18 | 16 | Drag the PDF into the chat, send **Paragraphs out of a PDF** (about 3 min with Mistral: say that GLM or Claude are faster). The app checks itself against the 90 paragraphs and 141 footnotes. Compare with the guesses, and with the gallery: three models found all 90 paragraphs, and 13, 129 and 0 footnotes. A converter damages text in four ways (order, breakage, loss, noise); a script repairs only what you tell it about. | *Your files*, Send; Gallery | |
| 10:34 | 6 | **Red-team your own tool**: three questions it should answer wrongly. Try them. | | 4 |
| 10:40 | 5 | Close: **Execute shrinks, Decide grows, Deliver is the point.** HRC Voting: one evening, then more than 50 fixes over ten weeks. Save the app. | **Save as file** | 5 |
| 10:45 | 15 | **Kept free.** Whatever ran over; then questions. Extras for the fast: *Who recommends what*, *Check ten at random*. | | |

**1. Four objections.** Source: `~/Desktop/inne/thread_ai_hr_workflows.md`. The lines to keep: "scripts are deterministic. You can run one a thousand times and get the same result each time"; where the material is not public, "the assistant writes the script from a synthetic document with the same format and structure"; and "you can run it on your own laptop with wi-fi turned off, so the documents themselves never reach the AI model". In the studio each objection has its answer: *Run it three times* (hallucination, quality), *What left this laptop* (confidentiality), *Save as file* plus the cut model link (security).

**2. Budapest, slide 4.** "A probabilistic model builds deterministic tools — then the tool, not the model, gives the answer." Three beats from the speaker notes: probabilistic is not a product; its real strength is writing code; the tool is deterministic. Video `film_coding.mp4`; if it does not play, slide 22.

**3. HRC Voting audit, finding A1** (`~/Desktop/HURIDOCS/OHCHR_voting/notes/AUDIT-2026-07.md`). "Most often outvoted" was computed from the most frequent vote, not the winning side: in 53 resolutions the text was carried and every State that voted yes, the winning side, was scored as outvoted. The audit's own summary: four measures "are documented as one thing" and implemented as another. One slide: same code, same wrong answer, every time.

**4. Red-teaming.** From the IHRL course plan, session 8 "Kuźnia" (`~/Desktop/UAM/Zajęcia 26-27/IHRL/mapa-ai-i-prawo/kurs/plan_zajec.md`). Examples to seed it: a mandate that did not exist in a given year; a keyword with two spellings; a State that changed its name; a filter that leaves nothing.

**5. WSIS 2026 slide** (`~/Desktop/talks/wsis2026/index.html`): "EXECUTE shrinks / DECIDE grows / DELIVER is the point". The honest version, from the UMCS panel notes: the first working HRC Voting was built in one evening (7 July 2026, Geneva), then more than 50 fixes over ten weeks; the evening was enough because the domain knowledge was already there.

---

## Session 8 (11:15–12:45)

| Time | Min | What happens | In the studio | Material |
|---|---|---|---|---|
| 11:15 | 5 | Back from the break. Switch to **Session 8** (top bar): two new tools under *Look inside*. | Session 8 | |
| 11:20 | 5 | **Ask the model directly: a quotation.** "Quote paragraph 97 of General comment No. 27." The document has 90 paragraphs. Read the three answers aloud before revealing the box. | *Look inside* → *Ask the model directly* → *A quotation* | |
| 11:25 | 10 | **Verbatim finder for General Comments** (drag the General Comments file in). Search for something from their own work. | New app | |
| 11:35 | 6 | **Generation for navigation; retrieval for substance.** The machine finds; the lawyer decides. Then the ✓ / ≈ / ✗ numbers. | | 6, 7 |
| 11:41 | 5 | **From one search to what an institution knows.** Open the library on *Your files*: nine documents on neurotechnology in the administration of justice, of six kinds: the Secretary-General's report A/81/351 (27 August 2026), the UNODC–INTERPOL background paper, the Futures Lab submission to that report, the Australian Human Rights Commission's *Peace of Mind*, two journal articles and three CCPR General Comments. Their weight differs; the wiki shows which is which. | *Your files* → Library | 10 |
| 11:46 | 18 | **A research wiki on neurotechnology and justice** (plan, drag the library in, build). Open *mental privacy*, click a citation ("A/81/351, para. 24" or "Szoszkiewicz & Yuste 2025, p. 3471"): the PDF opens next to the app at that page. Footnote 7 of the Secretary-General's report cites the EMBO article: two kinds of source on one page. Then **Draft a summary**: three sentences, each ending with a citation; check one by clicking it. | Plan; PDF drawer | 10 |
| 12:04 | 7 | **What may leave the room**: eight cards, three piles. The summary just sent up to 12 public paragraphs; what else may go? | | 8 |
| 12:11 | 5 | **What left this laptop**: only the paragraphs behind the summary left. Then **cut the model link**: the wiki still works, the summary button does not. | *Look inside* | |
| 12:16 | 6 | Close: **Suggest improvements** (the model lists five changes to their app in a few seconds; building them is for later), and **Take it further** in the footer: the open tools, a prompt to review code at home, and its warning that such assistants send what they read to the company that runs the model. Save the app. | Next step; footer | |
| 12:22 | 8 | Questions; what to try next week. | | |
| 12:30 | 15 | **Kept free**, for whatever ran over. If time is left: **check the checker** from the gallery. | Gallery | 9 |

Extras for those who finish early: **Check an AI briefing**, **A model inside the tool** (on their S7 dashboard), **How two States vote at the Human Rights Council**.

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

**10. The research wiki.** The method of the book's knowledge base (`~/Desktop/The Book/00_PROJECT/wiki/WIKI.md`): the author chooses the sources, agents write and file the pages, and every factual claim carries "an inline link straight to its source", a PDF opened at its page. The workshop app does the same on a small scale: code files each paragraph under its concepts, the model only drafts a summary, and each paragraph is one click from its page. The workshop library (2 November 2026) is profiled on neurotechnology in the administration of justice: 9 documents, 945 passages, each with the PDF page it starts on (to open) and the page printed there (to cite). Passages come from the PDFs (PyMuPDF; footnotes, running heads and pull quotes dropped), General Comment paragraphs from the UN Human Rights Database. The UNODC–INTERPOL *assessment draft* is confidential and is not used; the public background paper is.

A finding to use (from the earlier General Comments library, 1 November 2026): the exact word *proportionality* occurred in 8 paragraphs, every form of the word in 12, because CRPD General Comment No. 6 speaks of a *disproportionate* burden, a different test. The rule the code applies decides what the concept is. To redo on the new library after the bake-off; in it, "deception detection" without "lie detection" occurs in A/81/351 paras 20 and 53, which a wiki that searches one term misses.

**9. Check the checker** (optional, in the free time). In the gallery, *Check an AI briefing*: three apps, three models. On the projector, paste this briefing into each (it has five planted errors: 50th session, 20 against, 6 abstentions, India "abstained", and a mandate claim the voting data cannot check):

> Resolution A/HRC/RES/51/27 on the situation of human rights in Ethiopia was adopted by the Human Rights Council on 7 October 2022, at its 50th session, by a recorded vote of 21 in favour, 20 against and 6 abstentions. The text was presented by the European Union. The United States, Germany and Finland voted in favour; China, Pakistan and Eritrea voted against. India abstained, as did Indonesia. The resolution extended the mandate of the International Commission of Human Rights Experts on Ethiopia for one year.

What the apps did (1 November 2026, `tools/briefing_probe.py`): Claude's found all four checkable errors and confirmed the rest; Mistral's caught two, missed the abstentions and called two correct claims wrong; GLM's, which passed all eight automatic checks, misread the sentences and called eight claims wrong, including one that is not in the text. The lesson card: test a checker on errors you planted yourself before you trust it.

---

## When something fails

| Problem | What the room sees | What to do |
|---|---|---|
| The VM does not answer | A note in the chat: switched to the backup server (the badge still says "Live model") | Nothing: the studio has switched |
| A model's host fails | The answer comes from another model: Mistral falls back to GLM run in the EU, Claude to Mistral | Nothing to fix. The app card and *What left this laptop* name the model that answered: worth pointing out if someone chose a model for its origin |
| No model at all | "Recorded answers" | The workshop requests still work as recordings (with the model's thinking); free chat does not. Use the gallery. |
| One seat out of budget | A message naming the budget | Top up the seat on the admin page |
| A build takes too long | The thinking or code keeps streaming | Stop, switch to GLM, send again |
| An app breaks | "Something in the app broke" | *Ask the model to fix it*; after two failed fixes the studio offers a fresh start |
| Wi‑Fi down | Nothing loads | The saved files (*Save as file*) open offline; continue from the gallery on the facilitator's laptop |
