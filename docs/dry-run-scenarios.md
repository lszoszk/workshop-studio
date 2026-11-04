# Dry run on paper: five participants through Sessions 7 and 8

Written on 4 November 2026, before the rehearsal of about 20 November. Nothing here was run with a model: the five participants are invented, and their builds are the gallery's builds of 4 November (Claude Sonnet 5.5, Mistral Large 3, GLM-5.3 at medium reasoning), with the times measured in the bake-off that day. The aim is to see where the morning breaks before a room of 30 finds out.

## What the measurements say before anyone sits down

| Step | Time it takes now | Source |
|---|---|---|
| Logging in (link, password, seat code, country) | 2–4 min per person; 8–10 min for a room if done in the session | session plan |
| Planning (recorded log, 4–5 question cards) | 2.5–3 min, of which 80 s is the log | `PACE` in `studio.js` |
| First build, Mistral Large 3 | 2.4–4.8 min; dashboard, six builds: 2 with no error, 1 with a small one, 3 broken; Verbatim finder: the search does not work | bake-off, 4.11 |
| First build, GLM-5.3 (medium) | 3.4–8.7 min; dashboard, six builds: 5 with no error, 1 cut off mid-code; one PDF attempt in two stopped before the code; the wiki had a syntax error | bake-off, 4.11 |
| First build, Claude Sonnet 5.5 | not measured through the studio (built in Claude Code); earlier, shorter plans took 1–2 min | session plan |
| Any change ("add a column") | as long as a first build: the model rewrites the whole app, 500 to 2,000 lines | how the studio works |
| *Fix this error* | the same again, and it may break again | |
| *Improve it in the studio* (a gallery app as v1) | under a minute; the gallery shows each model's best of six dashboards | since 4.11 |

Two consequences follow. First, the default model (Mistral) gives a broken first dashboard about half the time, and the dashboard is the first thing all 30 people build: if half the room keeps the default, seven or eight people start with a broken app. Second, the 15-minute slot "Modify, in their own words" holds at most two changes per person, and only if nothing breaks.

## Third pass, 4 November, late afternoon

Run again after Session 8 moved from the PDF to the HTML of GC 27, in two tabs. Times and results are the bake-off's, with the studio's settings.

**Session 7 has not changed, and its first minutes are still the riskiest of the morning.** The default model, Mistral Large 3, gave 2 dashboards with no error in 6; GLM-5.3 gave 5 in 6. Amara (default) has a one-in-two chance of an empty dashboard at 09:47; the gallery's *Improve it in the studio* brings her back for the video at 09:45–09:48 if a co-facilitator is at her side. Claude through the studio is still unmeasured.

**Session 8 is now shorter and calmer.** Opening the HTML, planning (2.5 minutes) and building (1.6–3.4 minutes) fit the 13 minutes from 11:23. Every Mistral build shows what the lesson needs on its first tab: 90 of 90 paragraphs, footnotes 0 of 141, the five paragraphs whose first words differ, and the JSON and Markdown downloads. Two of its three builds leave the paragraph table on tab 02 empty, and all three log a JavaScript error, so Amara sees the lesson but not the table; the gallery's app gives her the table. Mr Chen on GLM may get "the model stopped before writing the code" (one build in three) and sends again, which still lands before the slide at 11:36. Leila on Claude gets the recorded quality (7 of 7) and spends the time comparing a paragraph with the PDF. Fatou, in recorded mode, gets Sonnet's build at once. Tomás, with a seat code, has five suggested improvements in seconds at 11:42 and builds one in about two minutes. The slide on three formats then explains what everyone has just seen, so the story of the UN Human Rights Database lands on a question the room already has: how can anyone cite a General Comment without its footnotes?

**What the third pass changes in the risks.** The extraction is no longer a risk to the timeline; the S7 dashboard and the logins are. Two things are open and need money first: the OpenRouter balance was $1.22 at 14:10 (the session plan asks for at least $300 on the day), and Claude and GLM run in the EU have not been measured through the studio, so the S7 default model is still to be decided.

## Second pass, 4 November afternoon

The morning was run again on paper after three changes: six dashboards per model were measured; the studio now supplies Chart.js when a model also loads it from the internet (Mistral Large 3 did in every build, which only gave a blocked request and an error in the console); and the gallery shows each model's best of six dashboards, with the count. What this changes:

- **The first dashboard is still the riskiest moment, but it now has a fast way out.** About half of Mistral's first dashboards break. Pressing *Fix this error* costs another three minutes and may break again; *Improve it in the studio* from the gallery gives a working dashboard of the same model in under a minute. The facilitator's instruction at 09:47 should be that one: "If your dashboard is empty, open the gallery and press *Improve it in the studio* under the model you chose."
- **GLM is now the most reliable of the measured models but has the longest tail** (up to 8.7 minutes), so the video belongs at 09:45, while builds run, not after them.
- **Nothing from Chart.js reaches *What left this laptop* any more**, so the confidentiality thread is not muddied by a request the participant never asked for.
- **Still unmeasured, and needing a top-up first:** Claude through the studio, and GLM run in the EU. Until they are measured, the default model for S7 stays an open decision.

## The five participants

**Amara, diplomat at a Permanent Mission (an African State).** Twelve years in the foreign service, uses Word, Outlook and a chatbot on her phone, has never seen code. Attended a UN briefing on generative AI last year. Her country's recommendations are a political matter for her: she reads the dashboard as the record of her State.

**Tomás, advocacy officer at an international NGO (Latin America desk).** Uses ChatGPT every day, fast, impatient, curious. Will type his own requests from the first minute and ask for things the studio does not do (internet access, his own PDFs).

**Dr Leila, legal adviser at a national human rights institution.** A careful lawyer who cites paragraph by paragraph. Sceptical of AI because she has caught invented citations before. She will check every number and say when a count is off by one.

**Mr Chen, human rights officer at OHCHR.** Knows the Universal Human Rights Index from the inside, including how its labels are assigned. Data-literate (Excel, some SQL). Bound by UN rules on which AI tools staff may use, and alert to where data goes.

**Fatou, programme officer at a regional organisation.** French is her working language and English her third. Arrives with a locked-down corporate laptop (Windows, Edge or Firefox, no admin rights), five minutes late.

## Session 7, minute by minute

**09:15–09:30, logging in over coffee.** Amara and Leila log in with a co-facilitator; the tour starts and Amara reads it to the end. Tomás skips the tour and starts typing. Mr Chen asks before logging in what the seat code is linked to and whether his name is stored (answer: the code is linked to a country and a budget, not to a person; requests go through the studio's server with zero data retention). Fatou is not there.

**09:30–09:43, welcome, four objections, the ladder.** Fatou arrives at 09:35. Edge works; Firefox has never been tested and her laptop defaults to it. A co-facilitator sits with her for six minutes. Tomás has already built something in free chat. Amara asks, during the objections, whether "her country's data" leaves the room (it is public UN data; the question is good and belongs to S8's cards: note it on the board).

**09:43–09:53, the first dashboard.** Everyone sends the dashboard in plan mode. The planning log plays for 80 s; the cards take another minute. Then the build:

- Amara keeps the default, Mistral Large 3. Three minutes later her dashboard shows a header and an empty chart area (in the bake-off, three of six dashboards broke like this, on a missing element or a variable declared twice). She does not know whether she did something wrong. A co-facilitator does not press *Fix this error* (another three minutes, and it may break again): she opens the gallery, takes Mistral's working dashboard with *Improve it in the studio*, and Amara has it as her v1 within a minute, in time for the video.
- Leila chose Claude, because she "trusts the American one more for English". Her build arrives and works.
- Mr Chen chose GLM from its developer's service, to see a Chinese model and where the badge says his request goes. It works (five of six GLM dashboards did), but GLM took anywhere from 3.4 to 8.7 minutes, so his may still be building at 09:48.
- Tomás is on his second free-chat app and has missed the plan mode.
- Fatou is still answering the planning cards.

At 09:48 the video should play. In this room two of five are not ready: Mr Chen's GLM build is still running, and Fatou's has just started. Playing the video at 09:45, while they wait, would catch everyone; at 09:48 the room splits between the screen and their laptops.

**09:53–10:02, Run it three times, Layers, the audit.** Works well for Leila and Mr Chen. Amara's fixed dashboard arrives at 09:55, during *Run it three times*. Mr Chen asks the first hard question: "*Layers* says this number is computed, but the UN labels it counts were assigned by people at OHCHR, sometimes inconsistently. The code is deterministic; the input is not." It is the right point, and *Check ten at random* answers it, 15 minutes later. Say so.

**10:02–10:17, modify in your own words.** The plan says 15 minutes. With each change taking 3–6 minutes and *Send to wall* in the same slot:

- Leila asks for "the number of recommendations per treaty body by year, as a table". Five minutes later it works; she checks two numbers against the Excel file and finds one off by one (the year filter includes a boundary year). This is the best moment of the morning, and only she has it.
- Amara asks for "a chart comparing my country to its neighbours". The data has one country. The model builds a chart with invented neighbour values, or says it cannot; either way she needs the facilitator to explain why.
- Tomás asks for a map, which needs a map library from the internet, which the sandbox blocks. The app shows a blank square.
- Mr Chen does not modify; he asks whether he may *Send to wall* a dashboard of a State that is not his. Amara overhears and asks that her country's dashboard not be shown on the projector.
- The wall shows three dashboards, one of them broken.

**10:17–10:32, Check ten at random.** Another full build (3–6 minutes). Mr Chen corrects two labels and is the only one who knows the right answer; Leila corrects one and asks how she would know whether a label is "wrong" or "arguable". The facilitator's answer matters more than the feature: the point is that clean data still carries someone's judgement.

**10:32–10:45, red team and close.** Red-teaming is where Tomás finally slows down: a keyword with two spellings ("Roma" / "Romani") gives two different counts. Amara saves her app. Fatou's dashboard works; she has not modified it.

**10:45–11:00, the free time.** It is all used: two late builds, Amara's question about the wall, and Tomás asking whether he can use the studio with his NGO's confidential witness statements (the answer is in S8; ask him to hold it).

## Session 8, minute by minute

**11:15–11:23, the quotation.** "Quote paragraph 97 of General comment No. 27" (it has 90). What the three models answer has not been measured with the current settings: do it at the rehearsal. If one of them quotes a paragraph that does not exist, the room remembers it; if all three decline, the lesson changes to "the models have learned to refuse this, but not the number question at 12:09", which the bake-off did measure.

**11:23–11:36, the document on the web.** Since the afternoon of 4 November the exercise uses the HTML that OHCHR publishes for GC 27. Guesses on paper. Builds are twice as fast as the PDF ones were: GLM 1.7–2.4 minutes, Mistral Large 3 1.8–2.0 (three builds each). But Mistral broke two of three, and GLM one of three; those who are hit take the gallery's working app with *Improve it in the studio*. Leila finds the tile "footnotes: 0 of 141" before anyone points at it, and asks how anyone can cite a General Comment without its footnotes. That is the question the slide answers. Mr Chen opens the closed list of restored spaces under the tiles and notices the glued words no rule repaired ("Giventhe") and asks whether the UN's own HTML is that careless; it is a conversion of the Word file, and conversions damage text.

**11:36–11:42, one document, three formats.** The slide, then the story of the UN Human Rights Database. This lands with Leila and Mr Chen, who have both copied paragraphs by hand; Tomás asks which format to use for his NGO's own reports (Word, if they have it). Amara asks nothing, but writes down that the PDF is the citable version.

**11:42–11:57, Suggest improvements, then one built.** The list of five takes seconds with a seat code; building one takes 2–3 minutes with the shorter plan. Tomás asks for a search box and gets it; Amara, in recorded mode, cannot ask for suggestions and continues from the gallery instead. Fatou exports the JSON and opens it, which shows her what "a dataset" means better than any slide.

**11:57–12:13, the data already exists; the Verbatim finder.** The reveal works on everyone, especially on Leila, who did not know the General Comments are available paragraph by paragraph. The Verbatim finder build: Mistral's bake-off build had an error that stops the search (one build only; worth measuring like the dashboard); GLM's misses one button; Claude's works. Those whose search does not work take one from the gallery. Leila searches "proportionality" and asks why the count differs from "proportional": on the earlier library the exact word was in 8 paragraphs and every form in 12, and the session plan's note on this fits here.

**12:13–12:28, the cards, the wiki demo, the close.** The eight cards work as a discussion; Mr Chen and Tomás disagree on whether a draft concluding observation may go to a model with zero data retention. The wiki demo works if the facilitator has a seat code and has rehearsed it.

**12:30–12:45, the free time.** Used for the builds that broke, and for Fatou, who has a working PDF app and asks for a copy of the session plan in French.

## What works

- **The arc.** Dashboard, then PDF, then published data, then the Verbatim finder: each step answers the question the previous one raised, and the method ladder gives the facilitator one sentence per step.
- **The quotation of paragraph 97** and **the reveal that the data already exists**: short, concrete, and they change how lawyers see the tool.
- **Run it three times, Layers, Check ten at random, the comparison table**: they turn "trust" into something to look at. This matters, because research on automation bias finds that teaching people about AI's limits does not by itself reduce over-reliance, while checks built into the workflow do (see Sources).
- **The confidentiality thread** (*What left this laptop*, the model badge, the model step's "n pages will leave the browser", the eight cards). For diplomats and UN staff it is the real question of the morning, and the studio answers it on screen.
- **Recorded mode and *Improve it in the studio***: anyone whose build breaks can continue from a working app in under a minute.
- **The HTML exercise** (since 4 November): a shorter plan, builds of about two minutes, and a loss (0 of 141 footnotes) that participants find themselves, which leads straight into the slide on formats.

## What does not work, and how to fix it

1. **The default model breaks the first build.** Measured on 4 November, six dashboards each: Mistral Large 3, the default, gave 2 with no error, 1 with a small one and 3 broken; GLM-5.3 at medium gave 5 with no error. (Mistral also loaded Chart.js from the internet every time; the studio now replaces that line with its own copy.) *Fix:* after a top-up, measure Claude and GLM run in the EU the same way and choose the S7 default on that; until then, the facilitator's first instruction after the build is "if your dashboard is empty, press *Fix this error* now, before the video".
2. **Every change costs a full build.** "Modify, in their own words" (15 min) fits one change, at most two. *Fix:* say so in the room ("each change takes 3–5 minutes; choose one well"), seed three good one-line changes on a slide, and cut *Send to wall* from this slot or move it to the end of *Check ten at random*.
3. **The video at 09:48 comes too early.** In this simulation three of five are still waiting. *Fix:* play it while they wait (09:45), not after.
4. **Requests the data cannot answer.** A comparison with neighbouring States, a map, the internet. The studio's instructions already tell the model to build the closest useful thing and say on screen what is missing, and never to invent records. *Fix:* one line on the first slide of "Modify": "your file has one country, no maps, no internet"; at the rehearsal, send the neighbours request to each model and see whether it says so.
5. **Political sensitivity of the wall.** A diplomat may not want her State's dashboard on the projector. *Fix:* the wall is opt-in already (*Send to wall*); say so aloud, and show your own example country first.
6. **Firefox and locked-down laptops.** Never tested. *Fix:* test Firefox before the rehearsal; ask GHRH to tell participants to bring a laptop with Chrome, Edge or Safari; keep two spare laptops logged in.
7. **GLM sometimes writes no code.** One PDF attempt in two. *Fix:* the studio already says "send it again"; in the room, suggest GLM run in the EU only for those who want to see it, and Mistral or Claude for the main builds.
8. **The fast and the slow.** Tomás finishes everything and goes off-script; Fatou is a build behind all morning. *Fix:* give the fast an explicit extra (*Who recommends what*, the gallery's *check the checker*, red-teaming another participant's app); give the slow the permission to use recorded mode or *Improve it in the studio* without feeling behind.
9. **Questions that belong to Sessions 9 and 10** (harms, agents, institutional policy on AI). *Fix:* a "parking lot" on the board, read at 12:30.
10. **Claude's time through the studio is unknown.** *Fix:* measure it at the rehearsal with a seat code (one build per app, about $1).

## Side discussions to prepare an answer for

- "Can I use this with confidential documents?" Not in this studio; at home, with a model run locally or under an agreement your institution approves; the script-first method keeps the documents themselves away from the model.
- "Which AI may UN staff use?" Their own institution's rules apply; the studio only shows where each request goes.
- "Why a Chinese model?" To compare where requests go and how the same plan fares; GLM is open weights, and the EU-hosted entry keeps requests in the EU.
- "Is the UN's labelling reliable?" *Check ten at random* exists to look at that, not to answer it.
- "Who pays, and what does it cost?" In the bake-off a build cost 4 to 31 cents with Mistral Large 3 and GLM (Claude costs more and was not measured through the studio); the seat budgets are set by the organisers.
- "Will this replace legal researchers?" The HRC Voting story: one evening of building, then more than 50 fixes over ten weeks; the knowledge of the domain did the work.

## Sources

- Dell'Acqua et al., 'Navigating the Jagged Technological Frontier', *Organization Science* (2026), https://doi.org/10.1287/orsc.2025.21838
- Automation bias despite AI-literacy training (physicians, randomized trial, 2025), summarised at https://ctisus.com/learning/journalclub/349524 ; review of 35 studies (*AI & Society*), summarised at https://www.longtermwiki.com/resources/a96cbf6f98644f2f ; a reading intervention that did not reduce over-reliance and increased rejection of correct answers, https://arxiv.org/abs/2503.10556 (to be checked against the full papers before quoting)
- Diplomats' training on generative AI: UNITAR's briefing for Geneva-based Permanent Missions, https://event.unitar.org/product/11704 ; Kenya's training of 280 diplomats, https://itweb.africa/article/kenya-equips-diplomats-for-genai/o1Jr5MxP4p6MKdWL ; data protection, verification and human responsibility at a UN-Habitat workshop, https://kuwaittimes.com/article/45521/kuwait/other-news/un-habitat-turkey-embassy-hold-ai-for-diplomacy-workshop/ ; "shadow AI" in diplomacy, https://dig.watch/?p=236273
- A participant's account of losing confidence while watching an AI build at length, https://diginomica.com/welcome-app-roulette-heres-what-happened-when-i-tried-vibe-coding
