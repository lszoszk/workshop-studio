---
id: wcag22-non-text-content
title: "WCAG 2.2: non-text content, images of text, text alternatives (1.1.1, 1.4.5)"
publisher: "W3C (World Wide Web Consortium), Accessibility Guidelines Working Group"
url: https://www.w3.org/TR/WCAG22/
licence: W3C-Document
licence_url: https://www.w3.org/copyright/document-license-2023/
retrieved: 2026-11-02
kind: excerpt
topics: [accessibility, wcag, alt-text, images, charts]
---
> Portions of "Web Content Accessibility Guidelines (WCAG) 2.2", W3C Recommendation, 12 December 2024. Original: https://www.w3.org/TR/WCAG22/
> Copyright © 2020-2024 World Wide Web Consortium. W3C® liability, trademark and document use rules apply (W3C Document License, https://www.w3.org/copyright/document-license-2023/). Status: W3C Recommendation. Retrieved 2026-11-02.
> Verbatim extracts of the normative success-criterion text and definitions, in the order shown; navigation links removed. Not the complete document.

#### Success Criterion 1.1.1 Non-text Content

(Level A)

All non-text content that is presented to the user has a text alternative that serves the equivalent purpose, except for the situations listed below.

**Controls, Input**

If non-text content is a control or accepts user input, then it has a name that describes its purpose. (Refer to Success Criterion 4.1.2 for additional requirements for controls and content that accepts user input.)

**Time-Based Media**

If non-text content is time-based media, then text alternatives at least provide descriptive identification of the non-text content. (Refer to Guideline 1.2 for additional requirements for media.)

**Test**

If non-text content is a test or exercise that would be invalid if presented in text, then text alternatives at least provide descriptive identification of the non-text content.

**Sensory**

If non-text content is primarily intended to create a specific sensory experience, then text alternatives at least provide descriptive identification of the non-text content.

**CAPTCHA**

If the purpose of non-text content is to confirm that content is being accessed by a person rather than a computer, then text alternatives that identify and describe the purpose of the non-text content are provided, and alternative forms of CAPTCHA using output modes for different types of sensory perception are provided to accommodate different disabilities.

**Decoration, Formatting, Invisible**

If non-text content is pure decoration, is used only for visual formatting, or is not presented to users, then it is implemented in a way that it can be ignored by assistive technology.

#### Success Criterion 1.4.5 Images of Text

(Level AA)

If the technologies being used can achieve the visual presentation, text is used to convey information rather than images of text except for the following:

**Customizable**

The image of text can be visually customized to the user's requirements;

**Essential**

A particular presentation of text is essential to the information being conveyed.

Note

Logotypes (text that is part of a logo or brand name) are considered essential.

## Definitions used by these criteria

**text alternative**

Text that is programmatically associated with non-text content or referred to from text that is programmatically associated with non-text content. Programmatically associated text is text whose location can be programmatically determined from the non-text content.

Example

An image of a chart is described in text in the paragraph after the chart. The short text alternative for the chart indicates that a description follows.

Note

Refer to Understanding Text Alternatives for more information.

**pure decoration**

serving only an aesthetic purpose, providing no information, and having no functionality

Note

Text is only purely decorative if the words can be rearranged or substituted without changing their purpose.

Example

The cover page of a dictionary has random words in very light text in the background.
