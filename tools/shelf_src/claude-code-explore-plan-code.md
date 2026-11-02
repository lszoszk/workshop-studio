---
id: claude-code-explore-plan-code
title: "Anthropic: Claude Code workflows, explore first, plan before editing, then code (summary)"
publisher: "Anthropic"
url: https://code.claude.com/docs/en/common-workflows
licence: summary
licence_url: https://code.claude.com/docs/en/legal-and-compliance
retrieved: 2026-11-02
kind: summary
topics: [ai-assistants, claude-code, planning, plan-mode, workflow, clarifying-questions]
---
> Summary of "Common workflows", Anthropic Claude Code documentation, https://code.claude.com/docs/en/common-workflows , with details of plan mode from the "Permission modes" page, https://code.claude.com/docs/en/permission-modes , and of clarifying questions from the best-practices page summarised elsewhere on this shelf. Read 2026-11-02; the documentation changes often.
> The documentation pages carry the notice "© Anthropic PBC. All rights reserved" (https://code.claude.com/docs/en/legal-and-compliance), so this page is an original summary with no copied passages.

## Summary written for the workshop

The documentation does not use a slogan for it, but its recipes line up as three phases: look around, agree a plan, then make changes. Clarifying questions are part of the first two.

## Phase 1: explore

- **Orient on a new project.** The recipe starts with broad questions and narrows down. First ask for an overview of the whole codebase, then for the main architecture patterns, the key data models, how a specific concern such as authentication is handled, the coding conventions and a glossary of project terms.
- **Find the relevant code.** Ask which files handle a feature, how those files work together, and ask for the path of one operation from the user interface to the database. The tips: be specific about what you are looking for, and use the project's own domain vocabulary.
- **Keep the main conversation clean.** Reading a large codebase fills the working context with file contents. The page suggests delegating the investigation to a subagent that reads in its own context and sends back only a summary of its findings.
- **Do not describe what it can read.** The best-practices page adds that the assistant reads the repository itself, so prompts should add what it cannot see (decisions, constraints, preferences).

## Phase 2: plan, and ask questions

- **Plan mode.** In plan mode the assistant researches and proposes changes but makes no edits to your source files until you approve its plan. Enter it by pressing Shift+Tab, by prefixing a prompt with the plan command, or by starting the program with the plan permission mode. The status bar shows that plan mode is on.
- **Approving.** When the plan is ready you can approve it and let edits proceed (with more or less automatic acceptance of edits, depending on the mode you pick) or say no and keep planning with your comments. You can open the proposed plan in your text editor and change it before it continues. A project can make plan mode its default.
- **When the goal is unclear, have it ask you.** The best-practices page recommends asking the assistant to interview you until it can write the specification, for example into a file such as SPEC.md. The assistant then puts multiple-choice questions about the open decisions. After that, start a fresh session to build from the written specification.
- **When the bug is unclear, give it the facts.** In the bug-fixing recipe you share the error, ask for several possible fixes, then ask it to apply the one you choose. The tips are to give the command that reproduces the problem, the steps, and whether the error is intermittent or constant.

## Phase 3: code and check

- Apply the chosen change in small steps and run the tests or other check after each step. The best-practices page stresses that the assistant needs something that returns pass or fail, and that you should ask to see the evidence.
- For work that must be reviewed before anything is written to disk, stay in plan mode until the plan is accepted.

## Notes for the workshop

- A reliable sequence for a small app: (1) ask the assistant to explore the existing files or sample data and report back; (2) ask it to propose a plan and list the questions it needs answered; (3) answer, correct the plan, then (4) let it build, with a check you can run.
- The same sequence works with other assistants even where there is no formal plan mode: write "do not change any files yet" in the first prompts and request a plan before the build.
