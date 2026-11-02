# Planning packages

A planning package is a recorded planning session for one workshop app. The studio replays it as a
chat: the planner's log (a readable account written for participants) streams in the bubble, its tool steps appear between them, it asks
4–5 questions as cards, and the plan assembled from the participant's answers appears on the stage.
The participant's own model then builds from that plan, live.

The session is a **simulation**: the plan was written beforehand by Claude Fable 5.1, and the answers
choose between versions it prepared. The studio says so on the bubble.

## Files

| File | Written by | What |
|---|---|---|
| `tools/planning/briefs.json` | facilitator | per app: `problem` (what the participant types) and `facilitator_brief` (the steering) |
| `tools/out/planning/<id>.steps.jsonl` | `tools/look.py --log <id>`, `tools/shelf.py ... --log <id>` | every look at the data, search and read the planner really made |
| `tools/out/planning/<id>.draft.json` | the planner (Fable) | notes with step markers, questions, plan_base |
| `site/data/planning/<id>.json` | `python3 tools/planning.py assemble <id>` | the package the studio loads |

## The draft (`<id>.draft.json`)

```json
{
  "notes": "Markdown planning log for readers, 600–900 words. Put ⟦step⟧ where each logged step happened, in order: one marker per line of <id>.steps.jsonl.",
  "questions": [
    {"id": "q1", "header": "≤12 chars", "question": "One sentence ending with ?",
     "options": [
       {"label": "1–5 words", "description": "One sentence: what this choice changes in the app.", "default": true,
        "fragments": [{"section": "q1", "text": "Markdown that replaces {{q1}} in plan_base"},
                      {"section": "q1.checks", "text": "…replaces {{q1.checks}}"}]},
       {"label": "…", "description": "…", "fragments": [ … the same slots … ]}
     ]}
  ],
  "plan_base": "Markdown plan with slots {{q1}}, {{q1.checks}}, … in the sections they belong to."
}
```

- `section` names the slot the fragment fills: `{{q1}}` is filled by fragments with `"section": "q1"`,
  `{{q1.checks}}` by `"section": "q1.checks"`. Every option of a question fills the same slots.
- Exactly one option per question has `"default": true`; the defaults give the reference app.

## The package (`site/data/planning/<id>.json`)

```json
{"id", "title", "problem", "facilitator_brief", "planner": "Claude Fable 5.1", "recorded": "2026-11-02",
 "notes": "notes without markers",
 "steps": [{"at": 1234, "kind": "look|search|read", "label": "…", "detail": "…", "live": "uhri_overview"?}],
 "questions": [...as in the draft...],
 "plan_base": "..."}
```

`at` is the character offset in `notes` where the step appears. A step with `live` is recomputed by
the studio from the participant's own data; its `label` may hold `{country}`, `{count}`, `{years}`.

## Composing a plan

Replace every slot with the chosen options' fragments, put `{country}` in place, drop empty lines left
over, and prefix the build request: see `compose()` in `tools/planning.py` (the studio does the same).
