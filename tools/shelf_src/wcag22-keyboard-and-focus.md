---
id: wcag22-keyboard-and-focus
title: "WCAG 2.2: keyboard operation, focus and target size (2.1.1, 2.1.2, 2.1.4, 2.4.7, 2.4.11, 2.5.8)"
publisher: "W3C (World Wide Web Consortium), Accessibility Guidelines Working Group"
url: https://www.w3.org/TR/WCAG22/
licence: W3C-Document
licence_url: https://www.w3.org/copyright/document-license-2023/
retrieved: 2026-11-02
kind: excerpt
topics: [accessibility, wcag, keyboard, focus, interaction]
---
> Portions of "Web Content Accessibility Guidelines (WCAG) 2.2", W3C Recommendation, 12 December 2024. Original: https://www.w3.org/TR/WCAG22/
> Copyright © 2020-2024 World Wide Web Consortium. W3C® liability, trademark and document use rules apply (W3C Document License, https://www.w3.org/copyright/document-license-2023/). Status: W3C Recommendation. Retrieved 2026-11-02.
> Verbatim extracts of the normative success-criterion text and definitions, in the order shown; navigation links removed. Not the complete document.

#### Success Criterion 2.1.1 Keyboard

(Level A)

All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes, except where the underlying function requires input that depends on the path of the user's movement and not just the endpoints.

Note 1

This exception relates to the underlying function, not the input technique. For example, if using handwriting to enter text, the input technique (handwriting) requires path-dependent input but the underlying function (text input) does not.

Note 2

This does not forbid and should not discourage providing mouse input or other input methods in addition to keyboard operation.

#### Success Criterion 2.1.2 No Keyboard Trap

(Level A)

If keyboard focus can be moved to a component of the page using a keyboard interface, then focus can be moved away from that component using only a keyboard interface, and, if it requires more than unmodified arrow or tab keys or other standard exit methods, the user is advised of the method for moving focus away.

Note

Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference.

#### Success Criterion 2.1.4 Character Key Shortcuts

(Level A)

If a keyboard shortcut is implemented in content using only letter (including upper- and lower-case letters), punctuation, number, or symbol characters, then at least one of the following is true:

**Turn off**

A mechanism is available to turn the shortcut off;

**Remap**

A mechanism is available to remap the shortcut to include one or more non-printable keyboard keys (e.g., Ctrl, Alt);

**Active only on focus**

The keyboard shortcut for a user interface component is only active when that component has focus.

#### Success Criterion 2.4.7 Focus Visible

(Level AA)

Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible.

#### Success Criterion 2.4.11 Focus Not Obscured (Minimum)

(Level AA)

New

When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content.

Note 1

Where content in a configurable interface can be repositioned by the user, then only the initial positions of user-movable content are considered for testing and conformance of this success criterion.

Note 2

Content opened by the *user* may obscure the component receiving focus. If the user can reveal the focused component without advancing the keyboard focus, the component with focus is not considered visually hidden due to author-created content.

#### Success Criterion 2.5.8 Target Size (Minimum)

(Level AA)

New

The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:

**Spacing**

Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target;

**Equivalent**

The function can be achieved through a different control on the same page that meets this criterion;

**Inline**

The target is in a sentence or its size is otherwise constrained by the line-height of non-target text;

**User Agent Control**

The size of the target is determined by the user agent and is not modified by the author;

**Essential**

A particular presentation of the target is essential or is legally required for the information being conveyed.

Note 1

Targets that allow for values to be selected spatially based on position within the target are considered one target for the purpose of the success criterion. Examples include sliders, color pickers displaying a gradient of colors, or editable areas where you position the cursor.

Note 2

For inline targets the line-height should be interpreted as perpendicular to the flow of text. For example, in a language displayed vertically, the line-height would be horizontal.

## Definitions used by these criteria

**keyboard interface**

interface used by software to obtain keystroke input

Note 1

A keyboard interface allows users to provide keystroke input to programs even if the native technology does not contain a keyboard.

Example

A touchscreen PDA has a keyboard interface built into its operating system as well as a connector for external keyboards. Applications on the PDA can use the interface to obtain keyboard input either from an external keyboard or from other applications that provide simulated keyboard output, such as handwriting interpreters or speech-to-text applications with "keyboard emulation" functionality.

Note 2

Operation of the application (or parts of the application) through a keyboard-operated mouse emulator, such as MouseKeys, does not qualify as operation through a keyboard interface because operation of the program is through its pointing device interface, not through its keyboard interface.
