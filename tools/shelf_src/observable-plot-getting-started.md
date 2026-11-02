---
id: observable-plot-getting-started
title: "Observable Plot: Getting started (vanilla HTML via CDN, npm)"
publisher: "Observable, Inc. (Observable Plot contributors)"
url: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/docs/getting-started.md
licence: ISC
licence_url: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/LICENSE
retrieved: 2026-11-02
kind: excerpt
repo: observablehq/plot
path: docs/getting-started.md
commit: 535723d5e433727720d9b673c31622821bb03210
topics: [dataviz, observable-plot, javascript, cdn]
---
> Excerpt from `docs/getting-started.md` in https://github.com/observablehq/plot at commit 535723d5e433727720d9b673c31622821bb03210. Copyright 2020-2025 Observable, Inc. Released under the ISC licence (notice at the end of this page). Retrieved 2026-11-02.
> Trimmed; "[…]" marks cuts.
> Documentation-site markup is dropped (code-group tab labels are shown as captions); code samples are unchanged.

Observable Plot supports a variety of environments.

[…]

## Plot in vanilla HTML

In vanilla HTML, you can load Plot from a CDN such as jsDelivr or you can download it locally. We recommend using the CDN-hosted ES module bundle as it automatically loads Plot’s dependency on [D3](https://d3js.org). But for those who need it, we also provide a UMD bundle that exports the `Plot` global when loaded as a plain script.

ESM + CDN:

```html
<!DOCTYPE html>
<div id="myplot"></div>
<script type="module">

import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

const plot = Plot.rectY({length: 10000}, Plot.binX({y: "count"}, {x: Math.random})).plot();
const div = document.querySelector("#myplot");
div.append(plot);

</script>
```

UMD + CDN:

```html
<!DOCTYPE html>
<div id="myplot"></div>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6"></script>
<script type="module">

const plot = Plot.rectY({length: 10000}, Plot.binX({y: "count"}, {x: Math.random})).plot();
const div = document.querySelector("#myplot");
div.append(plot);

</script>
```

UMD + local:

```html
<!DOCTYPE html>
<div id="myplot"></div>
<script src="d3.js"></script>
<script src="plot.js"></script>
<script type="module">

const plot = Plot.rectY({length: 10000}, Plot.binX({y: "count"}, {x: Math.random})).plot();
const div = document.querySelector("#myplot");
div.append(plot);

</script>
```

Plot returns a detached DOM element — either an [SVG](https://developer.mozilla.org/en-US/docs/Web/SVG) or [HTML figure](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/figure) element. In vanilla web development, this means you need to insert the generated plot into the page to see it. Typically this is done by selecting a DOM element (such as a DIV with a unique identifier, like `myplot` above), and then calling [*element*.append](https://developer.mozilla.org/en-US/docs/Web/API/Element/append).

[…]

## Installing from npm

If you’re developing a web application using Node, you can install Plot via pnpm, npm, yarn, or your preferred package manager.

pnpm:

```bash
pnpm add @observablehq/plot
```

npm:

```bash
npm install @observablehq/plot
```

yarn:

```bash
yarn add @observablehq/plot
```

You can then load Plot into your app as:

```js
import * as Plot from "@observablehq/plot";
```

You can instead import specific symbols if you prefer:

```js
import {barY, groupX} from "@observablehq/plot";
```

---

## Licence notice (ISC)

Copyright 2020-2025 Observable, Inc.

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
