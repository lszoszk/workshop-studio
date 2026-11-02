---
id: a11y-project-checklist
title: "The A11Y Project checklist (content, keyboard, images, tables, colour contrast, forms)"
publisher: "The A11Y Project"
url: https://github.com/a11yproject/a11yproject.com/blob/090a026713ea81676a03e9b0381a10850d7c955f/src/_data/checklists.json
licence: Apache-2.0
licence_url: https://www.a11yproject.com/checklist/
retrieved: 2026-11-02
kind: excerpt
repo: a11yproject/a11yproject.com
path: src/_data/checklists.json
commit: 090a026713ea81676a03e9b0381a10850d7c955f
topics: [accessibility, checklist, wcag, html, forms]
---
> Excerpt from the checklist data file `src/_data/checklists.json` in https://github.com/a11yproject/a11yproject.com at commit 090a026713ea81676a03e9b0381a10850d7c955f, which renders the checklist at https://www.a11yproject.com/checklist/. © 2013-2024 The Accessibility Project, released under the Apache License 2.0 (https://www.apache.org/licenses/LICENSE-2.0; repository file LICENSE-APLv2). Retrieved 2026-11-02.
> Converted from JSON to Markdown: HTML tags removed (code spans kept as backticks), links kept as Markdown links. Only the sections content, keyboard, images, tables, color contrast and forms are included; wording is otherwise unchanged.

## Content

Content is the most important part of your site.

- **Use plain language and avoid figures of speech, idioms, and complicated metaphors.** (WCAG 3.1.5 Reading Level)
  Write content at [an 8th grade reading level](https://datayze.com/readability-analyzer.php).
- **Make sure that `button`, `a`, and `label` element content is unique and descriptive.** (WCAG 1.3.1 Info and Relationships)
  Terms like “click here” and “read more” do not provide any context. Some people navigate using a list of all buttons or links on a page or view. When using this mode, the terms indicate what will happen if navigated to or activated.
- **Use left-aligned text for left-to-right (LTR) languages, and right-aligned text for right-to-left (RTL) languages.** (WCAG 1.4.8 Visual Presentation)
  Centered-aligned or justified text is difficult to read.

## Keyboard

It is important that your interface and content can be operated, and navigated by use of a keyboard. Some people cannot use a mouse, or may be using other assistive technologies that may not allow for hovering or precise clicking.

- **Make sure there is a visible focus style for interactive elements that are navigated to via keyboard input.** (WCAG 2.4.7 Focus Visible)
  Can a person navigating with a keyboard, [switch](https://axesslab.com/switches/), voice control, or screen reader see where they currently are on the page?
- **Check to see that keyboard focus order matches the visual layout.** (WCAG 1.3.2 Meaningful Sequence)
  Can a person navigating with a keyboard or screen reader move around the page in a predictable way?
- **Remove invisible focusable elements.** (WCAG 2.4.3 Focus Order)
  Remove the ability to focus on elements that are not presently meant to be discoverable. This includes things like inactive drop down menus, off screen navigations, or modals.

## Images

Images are a very common part of most websites. Help make sure they can be enjoyed by all.

- **Make sure that all `img` elements have an `alt` attribute.** (WCAG 1.1.1 Non-text Content)
  `alt` attributes (alt text) give a description of an image for people who may not be able to view them. When an `alt` attribute isn't present on an image, a screen reader may announce the image's file name and path instead. This fails to communicate the image’s content.
- **Make sure that decorative images use null `alt` (empty) attribute values.** (WCAG 1.1.1 Non-text Content)
  Null `alt` attributes are also sometimes known as empty `alt` attributes. They are made by including no information between the opening and closing quotes of an `alt` attribute. Decorative images do not communicate information that is required to understand the website's overall meaning. Historically they were used for flourishes and [spacer gif](https://en.wikipedia.org/wiki/Spacer_GIF) images, but tend to be less relevant for modern websites and web apps.
- **Provide a text alternative for complex images such as charts, graphs, and maps.** (WCAG 1.1.1 Non-text Content)
  Is there a plain text which lists points on the map or sections of a flowchart? Describe all visible information. This includes graph axes, data points and labels, and the overall point the graphic is communicating.
- **For images containing text, make sure the alt description includes the image's text.** (WCAG 1.1.1 Non-text Content)
  For example, the FedEx logo should have an alt value of “FedEx.”

## Tables

Tables are a structured set of data that help people understand the relationships between different types of information.

- **Use the `table` element to describe tabular data.** (WCAG 1.3.1 Info and Relationships)
  Do you need to display data in rows and columns? Use the `table` element.
- **Use the `th` element for table headers (with appropriate `scope` attributes).** (WCAG 4.1.1 Parsing)
  Depending on [how complex your table is](https://www.w3.org/WAI/tutorials/tables/), you may also consider using `scope="col"` for column headers, and `scope="row"` for row headers. Many different kinds of assistive technology still use the `scope` attribute to help them understand and describe the structure of a table.
- **Use the `caption` element to provide a title for the table.** (WCAG 2.4.6 Headings or Labels)
  The table's `caption` should describe what kind of information the table contains.

## Color contrast

Color contrast is how legible colors are when placed next to, and on top of each other.

- **Check the contrast for all normal-sized text.** (WCAG 1.4.3 Contrast)
  Level AA compliance requires a contrast ratio of 4.5:1.
- **Check the contrast for all large-sized text.** (WCAG 1.4.3 Contrast)
  Level AA compliance requires a contrast ratio of 3:1.
- **Check the contrast for all icons.** (WCAG 1.4.11 Non-text Contrast)
  Level AA compliance requires a contrast ratio of 3.0:1.
- **Check the contrast of borders for input elements (text input, radio buttons, checkboxes, etc.).** (WCAG 1.4.11 Non-text Contrast)
  Level AA compliance requires a contrast ratio of 3.0:1.
- **Check text that overlaps images or video.** (WCAG 1.4.3 Contrast)
  Is text still legible?
- **Check custom `::selection` colors.** (WCAG 1.4.3 Contrast)
  Is the color contrast you set in your [`::selection` CSS declaration](https://developer.mozilla.org/en-US/docs/Web/CSS/::selection) sufficient? Otherwise someone may not be able read it if they highlight it.

## Forms

Forms allow people to enter information into a site for processing and manipulation. This includes things like sending messages and placing orders.

- **All inputs in a form are associated with a corresponding `label` element.** (WCAG 3.2.2 On Input)
  Use a `for`/`id` pairing to guarantee the highest level of browser/assistive technology support.
- **Use `fieldset` and `legend` elements where appropriate.** (WCAG 1.3.1 Info and Relationships)
  Does your form contain multiple sections of related inputs? Use `fieldset` to group them, and `legend` to provide a label for what this section is for.
- **Inputs use `autocomplete` where appropriate.** (WCAG 1.3.5 Identify Input Purpose)
  [Providing a mechanism](https://www.w3.org/TR/html52/sec-forms.html#sec-autofill) to help people more quickly, easily, and accurately fill in form fields that ask for common information (for example, name, address, phone number).
- **Make sure that form input errors are displayed in list above the form after submission.** (WCAG 3.3.1 Error Identification)
  This provides a way for assistive technology users to quickly have a high-level understanding of what issues are present in the form. This is especially important for larger forms with many inputs. Make sure that each reported error also has a link to the corresponding field with invalid input.
- **Associate input error messaging with the input it corresponds to.** (WCAG 3.3.1 Error Identification)
  Techniques such as [using `aria-describedby`](https://developer.paciellogroup.com/blog/2018/09/describing-aria-describedby/) allow people who use assistive technology to more easily understand the difference between the input and the error message associated with it.
- **Make sure that error, warning, and success states are not visually communicated by just color.** (WCAG 1.4.1 Use of Color)
  People who are color blind, who have other low vision conditions, or different cultural understandings for color may not see the state change, or understand what kind of feedback the state represents if color is the only indicator.

---

## Licence notice (Apache-2.0)

Licensed under the Apache License, Version 2.0. You may obtain a copy of the licence at https://www.apache.org/licenses/LICENSE-2.0 (also in the repository file LICENSE-APLv2). Unless required by applicable law or agreed to in writing, material distributed under the licence is distributed on an "AS IS" basis, without warranties or conditions of any kind. This page is a modified, abridged copy.
