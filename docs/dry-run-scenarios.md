# Dry run on paper: five participants through Sessions 7 and 8

Written on 4 November 2026, before the rehearsal of about 20 November. Nothing here was run with a model: the five participants are invented, and their builds are the gallery's builds of 4 November (Claude Sonnet 5.5, Mistral Large 3, GLM-5.3 at medium reasoning), with the times measured in the bake-off that day. The aim is to see where the morning breaks before a room of 30 finds out.

## What the measurements say before anyone sits down

| Step | Time it takes now | Source |
|---|---|---|
| Logging in (link, password, seat code, country) | 2–4 min per person; 8–10 min for a room if done in the session | session plan |
| Planning (recorded log, 4–5 question cards) | 2.5–3 min, of which 80 s is the log | `PACE` in `studio.js` |
| First build, Mistral Large 3 | 2.4–4.8 min; the dashboard and the Verbatim finder each had an error that stops the app | bake-off, 4.11 |
| First build, GLM-5.3 (medium) | 3.6–8.2 min; one PDF attempt in two stopped before the code, the wiki had a syntax error | bake-off, 4.11 |
| First build, Claude Sonnet 5.5 | not measured through the studio (built in Claude Code); earlier, shorter plans took 1–2 min | session plan |
| Any change ("add a column") | as long as a first build: the model rewrites the whole app, 500 to 2,000 lines | how the studio works |
| *Fix this error* | the same again | |

Two consequences follow. First, the default model (Mistral) gives a broken first dashboard in the bake-off, and the dashboard is the first thing all 30 people build. Second, the 15-minute slot "Modify, in their own words" holds at most two changes per person, and only if nothing breaks.

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

- Amara keeps the default, Mistral Large 3. Three minutes later her dashboard shows a header and an empty chart area: the bake-off build had an error ("Cannot access 'themeChart' before initialization") and an attempt to load something from the internet. She does not know whether she did something wrong.
- Leila chose Claude, because she "trusts the American one more for English". Her build arrives and works.
- Mr Chen chose GLM from its developer's service, to see a Chinese model and where the badge says his request goes. It works, in under four minutes (the bake-off's 8 of 8).
- Tomás is on his second free-chat app and has missed the plan mode.
- Fatou is still answering the planning cards.

At 09:48 the video should play. In this room, three of five are not ready: Amara needs *Fix this error* (three more minutes), Fatou's build has just started. The facilitator plays the video anyway and the room splits between the screen and their laptops.

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

**11:23–11:38, the PDF.** Guesses on paper. Builds: Mistral Large 3 in 2.5 minutes with 7 of 7 checks; GLM in about 8, and in one attempt of two it wrote a description and no code (the studio says "send it again", which costs another 8 minutes). Leila notices that 20 of 20 pages are flagged and asks whether a flag on every page means anything. A good question: here it means "every page has footnotes"; on the second document the flags differ, and that is where the flag starts to inform.

**11:38–11:45, the second document.** A next step of 3–8 minutes; the comparison table (66 paragraphs against 65, 4 of 6 checks failing) is the lesson. Mr Chen asks which paragraph is the extra one: the table on tab 02 shows it, if he can find it in the time.

**11:45–11:57, the model step.** Only the facilitator runs it (recorded mode cannot). Before it sends, the app says how many pages will leave the browser: 38 for both documents. This is where Tomás's question from S7 comes back: "So for my witness statements the pages would go to Mistral?" Yes; and that is why S8's cards exist. Mr Chen asks whether GLM's route sends them to China (glm-cn: yes, to Z.AI; glm-eu: no, Mistral in the EU). The model-step limits ("it costs, it varies, errors the checks do not see stay") land well with Leila.

**11:57–12:13, the data already exists; the Verbatim finder.** The reveal works on everyone, especially on Leila, who did not know the General Comments are available paragraph by paragraph. The Verbatim finder build: Mistral's bake-off build had an error that stops the search; GLM's misses one button; Claude's works. Leila searches "proportionality" and asks why the count differs from "proportional": on the earlier library the exact word was in 8 paragraphs and every form in 12, and the session plan's note on this fits here.

**12:13–12:28, the cards, the wiki demo, the close.** The eight cards work as a discussion; Mr Chen and Tomás disagree on whether a draft concluding observation may go to a model with zero data retention. The wiki demo works if the facilitator has a seat code and has rehearsed it.

**12:30–12:45, the free time.** Used for the builds that broke, and for Fatou, who has a working PDF app and asks for a copy of the session plan in French.

## What works

- **The arc.** Dashboard, then PDF, then published data, then the Verbatim finder: each step answers the question the previous one raised, and the method ladder gives the facilitator one sentence per step.
- **The quotation of paragraph 97** and **the reveal that the data already exists**: short, concrete, and they change how lawyers see the tool.
- **Run it three times, Layers, Check ten at random, the comparison table**: they turn "trust" into something to look at. This matters, because research on automation bias finds that teaching people about AI's limits does not by itself reduce over-reliance, while checks built into the workflow do (see Sources).
- **The confidentiality thread** (*What left this laptop*, the model badge, the model step's "n pages will leave the browser", the eight cards). For diplomats and UN staff it is the real question of the morning, and the studio answers it on screen.
- **Recorded mode and *Improve it in the studio***: anyone whose build breaks can continue from a working app in under a minute.

## What does not work, and how to fix it

1. **The default model breaks the first build.** Mistral Large 3, the default, had an error in its first dashboard and first Verbatim finder in the bake-off. *Fix:* before the rehearsal, build the dashboard five times with Mistral Large 3 and GLM (about $0.50) to measure the rate rather than rely on one build; if it holds, make the facilitator's first instruction "if your dashboard is empty, press *Fix this error* now, before the video", or make Claude the default for S7 only.
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
