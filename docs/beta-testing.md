# Garage Research: a guide for beta testers

Thank you for testing Garage Research. It is the workshop studio for Sessions 7 and 8 of *AI for Human Rights Professionals* (Geneva, 4 December 2026), in which participants build small tools on UN human rights data by asking a language model and then check every number these tools show. The test takes about 30 minutes, and what you report will be fixed before the workshop.

## What we do and why

Many of us (lawyers, diplomats, staff of NGOs and national human rights institutions) lose a lot of time on searching: going through UN documents, looking for the paragraph in which a body dealt with a given issue, or checking whether a recommendation was really addressed to a given state. The workshop shows that generative AI does not have to write texts that shape human judgement, as it may be used to shorten the way to the sources a person should take into account. Thus, the model writes the tool, while the tool itself works on the data in the participant's browser, so its results can be counted, repeated and checked. Each tool should therefore speed up the search, make it easy to confirm a finding in the source (each result links to the document and paragraph it comes from) and leave the assessment to the person using it. The only texts written by a model (the wiki in Session 8) are the last step of the workshop, and each quote in them is checked against its source.

Moreover, building such tools is a way of developing individual capacity. A participant who builds a tool and checks it learns where the models help and where they fail on tasks from their own work, and Dell'Acqua et al. call the boundary between the two the 'jagged technological frontier' ([*Organization Science*, 2026](https://doi.org/10.1287/orsc.2025.21838)). For this reason, the exercises go from published data and code that can be checked, through a model inside an app whose answers are checked by code, to text written by a model, which is the measure of last resort.

Nothing here is final. The exercises, their order and their wording can still be adjusted after the beta tests, and each app can be adjusted by the person using it: it is enough to ask for a change in your own words.

## How to open it

- Open https://lszoszk.github.io/workshop-studio/ on a laptop (Chrome or Safari; a phone gets a page that sends you to a laptop). The password is in the invitation email.
- If you received a seat code, enter it: the studio then calls real models (Mistral, Claude or GLM), and each seat has its own small budget. Without a code, the studio plays recorded answers, which is enough for most of the steps below.
- A short tour starts on the first visit. *Tour* in the footer starts it again.

## What to try

Session 7 (pick *Session 7* at the top):

1. Choose your country, pick *Your country's recommendations dashboard* and drag the country file from *Your files* into the chat. Answer the planning questions and build the app from the plan.
2. Open *Look inside* and try *Layers*, *Run it three times* and *What left this laptop*. Each of them should be understandable without the facilitator.
3. Try the next step *Check a quotation*: paste a passage that quotes UN recommendations to your country (or use the sample the app offers) and see whether the verdicts are right.
4. Ask for a change in your own words (another chart, a filter, a column), then *Save as file* and open the saved file with Wi-Fi turned off.

Session 8 (pick *Session 8*):

5. *Paragraphs out of a UN document*: drag *CESCR General comment No. 27 (HTML)* into the chat and build it. The web version of the document gives the paragraphs almost for free, but its footnotes are missing: check whether the app says so, and try the JSON and Markdown downloads. Then *Suggest improvements* (it needs a seat code).
6. *Verbatim finder for General Comments*: search for something from your own work and copy a citation.
7. *A research wiki on neurotechnology and justice*: open a page and click a citation. The PDF should open next to the app, at the right page, with the quoted passage marked.

## What to report

Use *Feedback* in the footer. Please write what you tried, what you expected and what you saw. The page adds technical details to your message (the version, the browser, the app and model you were using), which you can check before sending; it does not send your data or the app's code. Things that are confusing count as much as things that break, and so does any wording that would not work for a diplomat or a colleague from a national human rights institution.

## Known limitations

- The steps that call a model (*Suggest improvements*, and *Ask* and *Ingest* in the wiki) need a seat code; in recorded mode they say so.
- *Send to wall* needs a seat code as well.
- Firefox has not been tested yet.
- The data are snapshots (the UN Human Rights Index on 1 November 2026, the General Comments on 1 November 2026), so a figure may differ from today's UN websites.
