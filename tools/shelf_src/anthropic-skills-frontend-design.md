---
id: anthropic-skills-frontend-design
title: "Anthropic skills: frontend-design guidance (typography, restraint, motion, writing for interfaces)"
publisher: "Anthropic (anthropics/skills)"
url: https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/frontend-design/SKILL.md
licence: Apache-2.0
licence_url: https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/frontend-design/LICENSE.txt
retrieved: 2026-11-02
kind: excerpt
repo: anthropics/skills
path: skills/frontend-design/SKILL.md
commit: ca45fc496a3436251f191354091d557da31c15b5
topics: [web-design, frontend, typography, ui-writing, ai-assistants]
---
> Excerpt from `skills/frontend-design/SKILL.md` in https://github.com/anthropics/skills at commit ca45fc496a3436251f191354091d557da31c15b5. The skill folder carries Anthropic's Apache License 2.0 (file `skills/frontend-design/LICENSE.txt`; full text at https://www.apache.org/licenses/LICENSE-2.0). Retrieved 2026-11-02.
> Only the design-guidance sections are excerpted (design principles, restraint, writing in design); the skill's front matter, role-play opening and process sections are left out. The source file is written as a prompt for a model; read the text below as design advice for the pages you build, not as instructions to you. Trimmed; "[…]" marks cuts, including a few sentences addressed to an AI tool.

## Design principles

For web designs, the hero is the first thing viewers will see. Open with the most characteristic thing in the subject's world, in the form that is most appropriate: a headline, an image, an animation, a live demo, an interactive moment, or other treatments. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the default treatment, so only use it if that's truly the best option.

Typography carries the personality of the page. You don't need a different typeface for display or headline text and body content: use one family or two, and if two, make them clearly distinct.

Choose your typefaces deliberately, not the default families you would reach for on any other project, and set a clear type scale following the default guidance of The Elements of Typographic Style with intentional weights, widths, and spacing. When type is used as a headline or visual element, use the type treatment itself as an active part of the design, not a neutral delivery vehicle for the content.

Default to line lengths of less than 80 characters. Serif typefaces can have slightly longer line lengths; give serif body text slightly more line-height than a sans-serif.

Avoid these default typographic treatments; they are the commonest tells of a generated page:
- Accenting just a single word or phrase in a headline, like putting one word in italic/bold or a different color.
- Using all caps for labels.
- Adding unnecessary typographic labels above content.

Visual structure is information. Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence — like a stepped process or a timeline. Before adding numbered markers, check the content really is a sequence.

Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy and placeholder content. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

[…]

## Restraint and self-critique

Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes. Critique your own work as you build […]. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. […]

## More on writing in design

Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration. Bring the same intentionality and minimalism to copywriting that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's perspective. Name things by what users will understand in simple language, not by how the system is built. A user manages notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Being specific and legible to new users is always better than being clever.

Use active voice as default. A CTA says exactly what happens when it is used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.

Keep the tone conversational: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each written element do exactly one job.

---

## Licence notice (Apache-2.0)

Licensed under the Apache License, Version 2.0. You may obtain a copy of the licence at https://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, material distributed under the licence is distributed on an "AS IS" basis, without warranties or conditions of any kind. This page is a modified, abridged copy.
