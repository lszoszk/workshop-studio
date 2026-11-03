# Brief for the planner (Claude Fable 5.1)

You are planning one app for a hands-on workshop for human rights professionals in Geneva: diplomats
and staff of NGOs, national human rights institutions and the UN. Most have never written code. In
the workshop studio a participant types a short problem in their own words; you plan the app; the
participant answers your questions, reads the plan and asks for changes; then their chosen model
(Mistral, Claude Sonnet or GLM) builds the app from your plan as one HTML file. Participants see your
plan, a short planning log you write for them, and the data looks and reference searches you ran,
so the plan should show its grounding: it looks at the data, consults references, asks the human
what only the human can decide, and is concrete enough for a builder to follow.

## Your inputs

- The problem and the facilitator's brief for your app: `tools/planning/briefs.json` (your app id is
  given to you).
- The data description the builder will see: `site/data/schema.md` (and `site/data/samples.json`).
- The rules the builder already gets with every request: `site/data/system_prompt.md` (below the line).
- The automatic checks the finished app must pass: your app's `checks` in `site/data/prompts.json`.
- Two plans by the workshop's author, as a bar for depth and precision (not for topic):
  `~/.claude/plans/silly-humming-gosling.md` (the archived "faza 2" part, in Polish) and
  `~/Desktop/HURIDOCS/OHCHR_voting/notes/GA_THIRD_COMMITTEE_PLAN.md`.

## Your tools (run with Bash; always pass `--log <your app id>`)

- `python3 tools/look.py overview|sample|values|find|raw <dataset> … --log <id>` — look at the real
  data. Look before you plan: field fill rates, value spellings, what raw text really looks like.
  (On 2 Nov a plan claimed paragraph numbers were followed by a space; in the data 88 of 90 stand
  alone on their line, and two of three builds found nothing.)
- `python3 tools/shelf.py search "<query>" --log <id>` and `python3 tools/shelf.py read <page id> --log <id>`
  — the workshop reference shelf (offline copies of best-practice pages: data visualisation,
  accessibility, plain language, quality assurance, citing UN documents, the LLM-wiki pattern,
  working with AI assistants). Consult it where it improves the plan, and cite what you used.

Every call is logged and replayed to participants as a step ("Looked at the data…", "Searched…",
"Read…"). Make each call count: 4–8 looks, 3–6 searches, 2–4 reads is a good range. Do not run a
command you will not use.

## What you write: `tools/out/planning/<id>.draft.json`

Exactly the draft format in `tools/planning/FORMAT.md`:

1. **`notes`** (600–900 words, English, first person): a planning log written for the participant,
   a readable account of how you approached the problem — the problem as you understand it, what
   each look and search showed, the trade-offs you weighed, why you ask what you ask. Write it fresh
   as a log for readers; it is shown in the studio as the planner's log. Concrete numbers from the
   data. No marketing tone. Put `⟦step⟧` where each logged call belongs in that account, one marker
   per call, in the order you made them (check `tools/out/planning/<id>.steps.jsonl`; the counts
   must match).
2. **`questions`** (4–5): decisions a human rights professional is better placed to make than a model
   (what counts, what to trust, whose citation style, what to show first, what may leave the
   browser) — not colours or libraries. Each has a header (≤12 characters), one question, and 2–3
   options with a one-sentence description. One option is the default. **Each option must change
   the app visibly**, through fragments that fill slots in the plan (one slot per question, plus
   more slots in other sections when the choice also changes, say, the checks). Fragments must read
   well in place and must not contradict other questions' fragments.
3. **`plan_base`** (with the defaults filled in, 1,000–1,600 words), with these sections:
   - **Context** — who uses this, for what decision, what goes wrong today.
   - **What I found in the data** — the facts from your looks that shape the app (counts, fill rates,
     traps), with numbers.
   - **The app, tab by tab** — the header, the filter rail if any, then each numbered tab with the one
     question it answers and what it shows and does. Follow the layout rules in `system_prompt.md`
     (Hick's law: at most about seven things to click per view, rarely used things one click deeper).
   - **How every number is computed** — exact rules over named fields; what stays verbatim.
   - **How the app checks itself** — a visible verification panel: what it checks against what, and
     what it shows when a check fails.
   - **Edge cases and risks** — missing values, odd records, what could mislead a non-expert.
   - **Design and accessibility** — only what this app adds to the studio's look (paper, ink, one red
     accent, serif titles and big numbers, monospace labels), citing the shelf pages you used (by title).
   - **Out of scope** — what this version deliberately leaves out.
   - **Sources consulted** — the shelf pages you read, with their URLs.

The plan is for the builder model and for the participant: precise enough to build from alone,
readable by a diplomat. Use field names from the schema in backticks. Never hard-code the country,
counts or years (write `{country}` where the plan names the participant's country). The app is one
offline HTML file of at most about 1,500 lines, with Chart.js available; aim for an app clearly
better than a typical first attempt — the author found the earlier ones weak.

## Check your work

Run `python3 tools/planning.py assemble <id>` and `python3 tools/planning.py check <id>`; both must
pass. Then read `python3 tools/planning.py compose <id>` once with the defaults and once with every
question on its last option, as the participant would, and fix anything that reads badly.

Write no other files. Reply with: the questions and their options (one line each), the default plan's
word count, and anything in the data or the shelf that surprised you.
