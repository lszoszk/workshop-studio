---
id: claude-code-best-practices
title: "Anthropic: Best practices for Claude Code (summary)"
publisher: "Anthropic"
url: https://code.claude.com/docs/en/best-practices
licence: summary
licence_url: https://code.claude.com/docs/en/legal-and-compliance
retrieved: 2026-11-02
kind: summary
topics: [ai-assistants, claude-code, prompting, specification, verification, planning]
---
> Summary of "Best practices for Claude Code", Anthropic Claude Code documentation, https://code.claude.com/docs/en/best-practices , as read on 2026-11-02. The documentation changes often; check the live page.
> The documentation pages carry the notice "© Anthropic PBC. All rights reserved" (https://code.claude.com/docs/en/legal-and-compliance), so this page is an original summary with no copied passages.

## Summary written for the workshop

**Starting point.** The page says Claude Code is set up so that a plain first prompt in a fresh session usually works without configuration. It is about what to do when the defaults are not enough, which tends to happen when a project has knowledge, rules or constraints that cannot be seen from the code. It sorts typical disappointments into four causes: the assistant lacked information it could not read from the repository; it declared the work finished without any way to check it; a rule that must never be broken (or a step that must always happen) was left to a prompt; or the result was right but cost more time, tokens or permission prompts than it was worth.

**1. Tell the assistant what it cannot see.** Write down only what the assistant cannot find by reading the project, or what it would waste time rediscovering each session. A two-question test: could it find this by reading the code, and would it actually go and look? If both answers are yes, leave it out. Typical items that do belong: a decision made in a meeting, a deployment procedure that lives in one person's head, an environment variable the tests need.

**2. Write specific prompts.** Name the file, describe the symptom and say what "fixed" looks like. If you prefer one of two reasonable approaches, say which, because the assistant cannot infer a preference. Hand over what you have (a file, a screenshot, command output) instead of describing it. Phrases that urge deeper thought are ordinary text; how much the model reasons is controlled by a separate effort setting. One phrase the page still endorses is asking the assistant to be ambitious when you want the fuller version of a feature, because it otherwise tends to build the smallest thing that satisfies the request. The page's examples contrast "fix the login bug" with a prompt that names the symptom, the folder to look in, the test to write first and then the fix.

**3. Ask it to interview you when you do not know what you want yet.** The page recommends asking the assistant to interview you until it could write a specification, and to save that specification in a file. It then asks multiple-choice questions about the unsettled parts, such as limits per user versus per key, what happens to requests over the limit, and what is out of scope. Once the specification exists, start a fresh session to build from it, so the work begins with clean context and a written definition of done.

**4. Keep the project instruction file short.** The instruction file (CLAUDE.md) is loaded into every session, so each line costs attention on every task. Keep to what cannot be derived from the code: commands, conventions, gotchas. Do not describe the architecture or file layout, which the assistant reads for itself. Rules that apply to one part of the codebase, team procedures and tool connections have their own mechanisms.

**5. Give it a check that returns pass or fail.** Without one, the assistant has only its own impression that the work is complete, and you become the test suite. The check can be a test file, a build exit code, a linter, a script that compares output with a fixture, or a browser screenshot next to a mockup. It can be requested in the prompt, set as a goal the assistant must meet, enforced by a hook that stops it from finishing until the check passes, or carried out by a separate reviewer that did not write the code. Ask for evidence (the command and its output), not just a statement that all is well. When asking for a review against a specification, tell the reviewer to skip style, otherwise it will always find something and you may end up with needless abstractions.

**6. Enforce rules that cannot have exceptions with the tool, not the prompt.** Hooks, permission rules and a sandbox can guarantee what a sentence in a prompt cannot, for example forbidding access to a file or requiring a step before committing.

**7. Change defaults deliberately.** The page covers permission modes, model and effort choices, the cost of delegating to subagents, and ways to keep cost and context down.

**8. Steer and automate.** It describes steering a running session, running the assistant from scripts or on a schedule, and running sessions in parallel, with five questions to answer before leaving a task unattended.

**9. Habits you can drop.** The page lists advice it considers outdated: shouting in capital letters for important instructions, describing the whole architecture in the instruction file, using subagents mainly to save context, and telling the assistant to keep going. A rule that truly cannot bend should become a hook or a deny rule.

## Notes for the workshop

- Before building an app with an assistant, write a half-page specification (audience, data, outputs, what is out of scope) and keep it in a file. If you cannot, ask the assistant to interview you.
- Define one check for every app: a test, a sample PDF whose expected extraction you know, or a list of known citations the finder must resolve.
- Ask the assistant to show the evidence, then look at it yourself.
