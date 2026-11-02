---
id: chartability-workbook
title: "Chartability: accessibility heuristics for data visualisations (workbook, critical tests)"
publisher: "Frank Elavsky / Chartability community"
url: https://chartability.github.io/POUR-CAF/
licence: CC-BY-SA-3.0
licence_url: https://chartability.fizz.studio/
retrieved: 2026-11-02
kind: excerpt
repo: Chartability/POUR-CAF
path: workbook.md
commit: 1eec6bbf21b1df6b118f7c9ff6ef25bfbf85c9dd
topics: [dataviz, accessibility, chartability, audit, heuristics]
---
> Excerpt from "The Chartability Workbook", Frank Elavsky and the Chartability community, https://chartability.github.io/POUR-CAF/ (source file `workbook.md` in https://github.com/Chartability/POUR-CAF at commit 1eec6bbf21b1df6b118f7c9ff6ef25bfbf85c9dd). Retrieved 2026-11-02.
> Chartability was created by Frank Elavsky and is licensed under CC BY-SA 3.0 Unported (https://creativecommons.org/licenses/by-sa/3.0/), as stated on https://chartability.fizz.studio/ and on the workbook page. This excerpt is a derivative: it is trimmed, and for the tests it keeps only the headings and the description lines of the tests marked critical. Any reuse must keep this credit and the CC BY-SA 3.0 licence (share-alike).
> The repository has no licence file of its own; the licence statement was confirmed on the two web pages named above.

# The Chartability Workbook

This workbook is intended to serve as a lightweight, high-level audit for catching data experience* design failures related to accessibility. For more on Chartability, see our home page: [https://chartability.fizz.studio/](https://chartability.fizz.studio/)

*A data experience (DX) could refer to a data visualization such as a chart, graph, or plot, a “bespoke” (highly customized) graphic based on data, a model, or an algorithm, or a data driven interface or system. If a human has an experience with data using any of their senses, then it counts as a data experience. We intentionally use an inclusive term.

## Method


This workbook organizes tests into seven categories, four of which are based on broad accessibility principles: Perceivable, Operable, Understandable, and Robust (POUR). The last three extend Robust: Compromising, Assistive, and Flexible (CAF).

An auditor should proceed through each test and determine whether the content fails or succeeds using techniques provided or their own methodology. The auditor should assume failure when tests are inconclusive and (if early in the design process) a proven pass to a future consideration has not yet been demonstrated.

## Failures


Unlike a compliance audit (which determines adherence to regulatory guidelines), Chartability is meant to identify design failures. Generally, Chartability approaches accessibility as a scale rather than a state: how accessible a DX is is determined by how few failures it contains. It should be assumed that even the absolute best DX may contain several failures, even after remediation. Note that Chartability should never be used in place of a compliance audit but always in tandem with it.

Chartability’s insistence on a scale (instead of a state) of accessibility requires that designers and creators consider their choices carefully: they must be willing to argue that lack of scope, time, or research or perhaps a unique consideration led to a given failure. No failure should be left unconsidered.

An important note about language: Chartability's tests are framed in negative language, like "Target pointer interaction size is too small." This is intentional. Chartability is not meant to be used to "pass" accessibility requirements. You cannot "pass" Chartability 100%. Rather, Chartability is simply framed as a tool that helps people catch known barriers, or "failures." It is possible to have 0 failures in Chartability but still have accessibility issues. This is because the work of accessibility never ends!

## What are "Critical" heuristics?


Some tests are considered _critical_ by members of the community because they are prohibitively expensive to fix, common, produces signficant barriers, and/or affect many aspects of a data experience design or development.

While all tests in Chartability are important, it is worth noting that Chartability's community has contributed to emphasizing the tests marked critical. All data experiences should strive to have 0 critical failures as a minimum while working toward 0 failures overall.

## The critical tests (headings and descriptions only)

## Perceivable

### Low contrast (critical)

__Description__: Geometries and large text must have >3:1 contrast against background, Regular text must have >4.5:1.

### Content is only visual (critical)

__Description__: Information in the chart must be available without visuals (no screen reader/braille support). At a minimum test using JAWS + Chrome, NVDA + Firefox (on Windows), VoiceOver + Safari (on Mac), and VoiceOver + Safari (on iOS). These devices must be able to access all chart information. All annotations, “visually apparent” trends or features, and all major narrative elements must be exposed to screen readers. Videos, presentations, and animations must include synchronized audio descriptions.

### Small text size (critical)

__Description__: Text (any) must not be smaller than 9pt/12px in size. Ideally only minor text is rendered at 9pt (Eg. axis labels) while all other text is larger.

### Visual presents seizure risk (critical)

__Description__: Chart must not pose a seizure risk when static or active. Chart must avoid red flashes and should avoid animating with red or have a significant portion of the display area use the color red. Tools like PEAT may be used to assess risk.

## Operable

### Interaction modality only has one input type (critical)

__Description__: If chart is interactive with a mouse (or another input device) it must also be made interactive for use with a keyboard. Test navigating to chart with keyboard, using tab and arrow keys. Focusing should mirror hovering, selecting (enter or spacebar) should mirror clicks. The chart must also be tested with a touch device and screen reader, as these devices may have different experiences than a keyboard.

### No interaction cues or instructions (critical)

__Description__: If chart has any interactive capabilities at all, it must be explained somewhere for users to understand. All keyboard controls must also be explained as well.

### Controls override AT controls (critical)

__Description__: Custom keyboard and touch controls must not override screen reader settings. Any custom key controls must only apply when the chart or elements have focus (no page or app overrides).

## Understandable

### No explanation for purpose or for how to read (critical)

__Description__: Chart should explain its purpose and how to read, use, and interpret it.

### No title, summary, or caption (critical)

__Description__: A title, summary, context, or caption must be provided.

### Reading level inappropriate (critical)

__Description__: All text (and alternative text) provided must target a reading grade level of 9 or lower. Tools may be used to automate reading level estimation.

## Compromising

### No table (critical)

__Description__: A table must be provided that contains a human-readable version of the data the chart is based on. This may be excluded if the chart title, summary, context, or annotations are sufficient at conveying all relevant information contained in the chart.

## Assistive

### Data density is inappropriate (critical)

__Description__: Data must be presented at an appropriate density. If too many elements are competing for the same space (approximate limit is based on cognitive load): clustering or patterns (or lack of) must be explained, chart must be aggregated to a higher level with less elements, or chart must be divided into smaller charts with less data. Visual density should serve a purpose, such as retaining the data's signal (when appropriate).

### Navigation and interaction is tedious (critical)

__Description__: Large blocks of repeated content must be skippable and interactions where the user is required to perform significant labor must not be considered essential (in content or function). The number of interactions or time required to perform a single task should be measured and compared across modalities (mouse pointer versus sequential keyboard versus search versus voice, etc).

## Flexible

### User style change not respected (critical)

__Description__: Styling changed by the user must be respected. Chart must not interfere with or override styling changes made by the user (such as importing a custom style sheet for use in an HTML application or web site).
