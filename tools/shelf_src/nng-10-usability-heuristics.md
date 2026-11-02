---
id: nng-10-usability-heuristics
title: "Nielsen Norman Group: 10 usability heuristics for interface design (summary)"
publisher: "Nielsen Norman Group (Jakob Nielsen)"
url: https://www.nngroup.com/articles/ten-usability-heuristics/
licence: summary
licence_url: https://www.nngroup.com/copyright-and-reprint-info/
retrieved: 2026-11-02
kind: summary
topics: [ux, usability, heuristics, interface-design, evaluation]
---
> Summary of "10 Usability Heuristics for User Interface Design" by Jakob Nielsen, Nielsen Norman Group (first published 24 April 1994, page last reviewed 30 January 2024). Original: https://www.nngroup.com/articles/ten-usability-heuristics/ . Retrieved 2026-11-02.
> The article is copyrighted and NN/g does not permit copying its articles (see https://www.nngroup.com/copyright-and-reprint-info/). Everything below is an original summary in the workshop's own words; the examples for data apps are the workshop's, not NN/g's.

## Summary written for the workshop

The article presents ten broad rules of thumb for judging an interface. NN/g calls them heuristics because they are general principles that experienced evaluators apply by judgement, not detailed rules that can be ticked off one by one. A common way to use them is a quick expert review of a screen or flow: walk through it once per heuristic and note where it fails. The ten, with a plain-language reading and an example for a small data app, are below.

1. **Visibility of system status.** Tell people what the system is doing, and do it quickly. If something has consequences or takes time, the user should see that it started, how far it has got and what the outcome was. In a data app: show progress while a PDF is being parsed or a model call is running, and show when the data was last updated.
2. **Match between the system and the real world.** Use the words, concepts and ordering that your users already know, not internal jargon. Do not assume that your own vocabulary is theirs; user research reveals the real terms and mental models. In a data app: label a filter "Treaty body" or "Country", not the name of the column in your spreadsheet.
3. **User control and freedom.** People make wrong moves and need a clearly marked way out: undo and redo, cancel, back. In a data app: let users reset all filters in one click and cancel a long extraction.
4. **Consistency and standards.** Keep things consistent inside the product (the same word and the same icon for the same action) and consistent with conventions people know from elsewhere. Both kinds of consistency make an interface easier to learn.
5. **Error prevention.** Design so that mistakes are less likely. Deal with the costly errors first and the small annoyances later. Helpful constraints, sensible defaults, warnings and undo reduce slips (careless actions) and mistakes (wrong intentions). In a data app: validate a date range before running a query, and ask for confirmation before deleting a saved view.
6. **Recognition rather than recall.** Let people see and pick options instead of remembering them. Keep needed information visible or one step away, and offer help in context rather than a long tutorial to memorise. In a data app: provide a drop-down of known committees instead of asking users to type codes.
7. **Flexibility and efficiency of use.** Offer accelerators such as keyboard shortcuts or gestures for frequent users, and let people personalise content or settings, without making the basic path harder for newcomers.
8. **Aesthetic and minimalist design.** Keep content and visuals focused on what matters for the main goals. Each extra element competes with the information users need. In a data app: one clear message per chart, and no decoration that carries no data.
9. **Help users recognize, diagnose and recover from errors.** Write error messages in plain language, make them visibly look like errors, say what went wrong and offer a way to fix it, ideally a one-step fix. Avoid technical codes as the only explanation.
10. **Help and documentation.** The best interface needs little explanation, but if help is provided it should be easy to search, available at the moment of need, focused on the user's task and made of concrete steps.

## How the workshop can use this

- Treat the list as a review checklist for any prototype: ask the chatbot to review a planned screen against each heuristic and to point at the exact element that fails.
- Heuristics 2, 6 and 9 are mostly about wording. They pair well with the plain-English pages on this shelf (GOV.UK writing for user interfaces and clear language).
- Heuristics 1, 3 and 5 matter most for apps that call a language model or parse documents, because those steps are slow, can fail, and can produce wrong results that users must be able to notice and undo.
- An expert review with heuristics finds likely problems; it does not replace watching two or three real colleagues use the app.
