---
id: chartjs-accessibility
title: "Chart.js: Accessibility of canvas charts"
publisher: "Chart.js contributors"
url: https://github.com/chartjs/Chart.js/blob/71d44219e79e3ac41e6f9dc907022eebf574868d/docs/general/accessibility.md
licence: MIT
licence_url: https://github.com/chartjs/Chart.js/blob/71d44219e79e3ac41e6f9dc907022eebf574868d/LICENSE.md
retrieved: 2026-11-02
kind: excerpt
repo: chartjs/Chart.js
path: docs/general/accessibility.md
commit: 71d44219e79e3ac41e6f9dc907022eebf574868d
topics: [dataviz, chartjs, accessibility, aria, canvas]
---
> Excerpt from `docs/general/accessibility.md` in https://github.com/chartjs/Chart.js at commit 71d44219e79e3ac41e6f9dc907022eebf574868d. Copyright (c) 2014-2024 Chart.js Contributors. Released under the MIT licence (notice at the end of this page). Retrieved 2026-11-02.
> Trimmed; "[…]" marks cuts.

# Accessibility

Chart.js charts are rendered on user provided `canvas` elements. Thus, it is up to the user to create the `canvas` element in a way that is accessible. The `canvas` element has support in all browsers and will render on screen but the `canvas` content will not be accessible to screen readers.

With `canvas`, the accessibility has to be added with ARIA attributes on the `canvas` element or added using internal fallback content placed within the opening and closing canvas tags.

This [website](http://pauljadam.com/demos/canvas.html) has a more detailed explanation of `canvas` accessibility as well as in depth examples.

## Examples

These are some examples of **accessible** `canvas` elements.

By setting the `role` and `aria-label`, this `canvas` now has an accessible name.

```html
<canvas id="goodCanvas1" width="400" height="100" aria-label="Hello ARIA World" role="img"></canvas>
```

This `canvas` element has a text alternative via fallback content.

```html
<canvas id="okCanvas2" width="400" height="100">
    <p>Hello Fallback World</p>
</canvas>
```

These are some bad examples of **inaccessible** `canvas` elements.

This `canvas` element does not have an accessible name or role.

```html
<canvas id="badCanvas1" width="400" height="100"></canvas>
```

This `canvas` element has inaccessible fallback content.

```html
<canvas id="badCanvas2" width="400" height="100">Your browser does not support the canvas element.</canvas>
```

---

## Licence notice (MIT)

The MIT License (MIT)

Copyright (c) 2014-2024 Chart.js Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
