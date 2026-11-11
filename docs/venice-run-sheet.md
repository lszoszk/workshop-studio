# Global Campus, Venice: run sheet for the studio parts

Four sessions of 90 minutes over two days. The slides are on `lszoszk.github.io/teaching-materials/global-campus`; the studio is `lszoszk.github.io/workshop-studio/?course=venice`. Times below are for the studio parts only, as measured live on 12 November 2026 with GLM-5.3 (EU).

## Before each day

- Server: `https://150.254.115.204/studio-api/health` shows `ok: true` and a balance well above the room's budget (15 seats × $6). Top up OpenRouter if not.
- Seat cards printed (`tools/out/venice-seat-cards.pdf`); a seat's budget can be raised on the admin page (Set budget).
- The wall on the projector in a second tab: `lszoszk.github.io/workshop-studio/wall.html`.

## Day 1, Session 2 · studio Session 1 (about 40 minutes of the 90)

| Min | What | Measured |
|---|---|---|
| 0–5 | Log in at the start of the session (seat code, Session 1, the tour), then lids closed | the step that costs the most time |
| +0 | Drag **General Comments** into the chat, pick **Verbatim finder**, answer the planning questions, Build | planning 20 s, build 2–3.5 min, $0.14 |
| while it builds | The two benchmark slides; students write down what a correct result should show | |
| +5 | Search "necessary in a democratic society": is GC 37, para. 40 there? Check one result on docs.un.org; Run it three times | |
| +15 | **Check a quotation**: the worksheet sentence, then a sentence from their own essay | build 2–2.5 min, $0.19 |
| last 5 | Feedback form; tonight's task (own idea in three sentences) | |

## Day 2, Session 3 · studio Session 2 (about 45 minutes)

| Min | What | Measured |
|---|---|---|
| +0 | Drag **Human Rights Council votes**, pick **How two States vote** | build about 1 min, $0.04–0.10; the first version broke once and the studio repaired it by itself |
| +8 | Compare two States; check one vote by hand in HRC Voting | |
| +15 | **Where every State stands** (the alignment map) | 25–40 s, $0.03 |
| +25 | Discussion: what do two dots close together mean; what is not on the map (texts adopted without a vote) | |
| +30 | **Suggest improvements** → build one change → **Send to wall** | a change takes 15–45 s, $0.03 |
| last 5 | The wall on the projector | |

## Day 2, Session 4 · studio Session 3 (about 55 minutes)

| Track | Steps | Measured |
|---|---|---|
| Your country | **Recommendations dashboard** (planning, build), then **Ask your data a question** | build 2–4 min, $0.10; GLM built it in 2 tries of 3 in our tests |
| From ten PDFs to a wiki | Build, tick documents, **Read with the model**, then **The wiki as a network** (runs on Claude) | build 40–50 s, $0.07; reading ten PDFs 35–45 s, $0.11 (four PDFs: about $0.04); network 20 s, $0.13 |
| Your own idea | Needs a seat code; the model asks three questions first | varies |

Last 15 minutes: Send to wall, two minutes per pair (what the app shows, what they checked by hand), Save as file, Take-home kit, feedback form.

## When an app does not build

1. An error as the app opens: the studio sends it back to the model once by itself. Wait.
2. Still an error in red: **Ask the model to fix it** (same conversation).
3. Still broken: **Load a working version** next to it brings in the build of the same exercise recorded before the class, as a new version; the student goes on with the next step from there.
4. A slow or failing model for the whole room: switch the model menu to Claude Sonnet 5.5 (about three times the price per build, nine builds in ten work).
5. No connection to the server at all: the studio falls back to recorded answers; every step except the wiki from PDFs and "Your own idea" still plays.

## Cost

A full path for one seat on GLM-5.3 is about $0.60–0.90; the room, $9–14. The Anthropic part (the wiki network, pictures, any switch to Claude) counts against `STUDIO_ANTHROPIC_CAP` on the server.
