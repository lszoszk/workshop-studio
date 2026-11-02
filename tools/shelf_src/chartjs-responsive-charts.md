---
id: chartjs-responsive-charts
title: "Chart.js: Responsive charts (container sizing, aspect ratio, printing)"
publisher: "Chart.js contributors"
url: https://github.com/chartjs/Chart.js/blob/71d44219e79e3ac41e6f9dc907022eebf574868d/docs/configuration/responsive.md
licence: MIT
licence_url: https://github.com/chartjs/Chart.js/blob/71d44219e79e3ac41e6f9dc907022eebf574868d/LICENSE.md
retrieved: 2026-11-02
kind: excerpt
repo: chartjs/Chart.js
path: docs/configuration/responsive.md
commit: 71d44219e79e3ac41e6f9dc907022eebf574868d
topics: [dataviz, chartjs, responsive, layout, css]
---
> Excerpt from `docs/configuration/responsive.md` in https://github.com/chartjs/Chart.js at commit 71d44219e79e3ac41e6f9dc907022eebf574868d. Copyright (c) 2014-2024 Chart.js Contributors. Released under the MIT licence (notice at the end of this page). Retrieved 2026-11-02.
> Trimmed; "[…]" marks cuts.

# Responsive Charts

When it comes to changing the chart size based on the window size, a major limitation is that the canvas *render* size (`canvas.width` and `.height`) can **not** be expressed with relative values, contrary to the *display* size (`canvas.style.width` and `.height`). Furthermore, these sizes are independent of each other and thus the canvas *render* size does not adjust automatically based on the *display* size, making the rendering inaccurate.

The following examples **do not work**:

- `<canvas height="40vh" width="80vw">`: **invalid** values, the canvas doesn't resize ([example](https://codepen.io/chartjs/pen/oWLZaR))
- `<canvas style="height:40vh; width:80vw">`: **invalid** behavior, the canvas is resized but becomes blurry ([example](https://codepen.io/chartjs/pen/WjxpmO))
- `<canvas style="margin: 0 auto;">`: **invalid** behavior, the canvas continually shrinks. Chart.js needs a dedicated container for each canvas and this styling should be applied there.

Chart.js provides a [few options](#configuration-options) to enable responsiveness and control the resize behavior of charts by detecting when the canvas *display* size changes and update the *render* size accordingly.

## Configuration Options

Namespace: `options`

| Name | Type | Default | Description
| ---- | ---- | ------- | -----------
| `responsive` | `boolean` | `true` | Resizes the chart canvas when its container does ([important note...](#important-note)).
| `maintainAspectRatio` | `boolean` | `true` | Maintain the original canvas aspect ratio `(width / height)` when resizing.
| `aspectRatio` | `number` | `1`\|`2` | Canvas aspect ratio (i.e. `width / height`, a value of 1 representing a square canvas). Note that this option is ignored if the height is explicitly defined either as attribute or via the style. The default value varies by chart type; Radial charts (doughnut, pie, polarArea, radar) default to `1` and others default to `2`.
| `onResize` | `function` | `null` | Called when a resize occurs. Gets passed two arguments: the chart instance and the new size.
| `resizeDelay` | `number` | `0` | Delay the resize update by the given amount of milliseconds. This can ease the resize process by debouncing the update of the elements.

## Important Note

Detecting when the canvas size changes can not be done directly from the `canvas` element. Chart.js uses its parent container to update the canvas *render* and *display* sizes. However, this method requires the container to be **relatively positioned** and **dedicated to the chart canvas only**. Responsiveness can then be achieved by setting relative values for the container size ([example](https://codepen.io/chartjs/pen/YVWZbz)):

```html
<div class="chart-container" style="position: relative; height:40vh; width:80vw">
    <canvas id="chart"></canvas>
</div>
```

The chart can also be programmatically resized by modifying the container size:

```javascript
chart.canvas.parentNode.style.height = '128px';
chart.canvas.parentNode.style.width = '128px';
```

Note that in order for the above code to correctly resize the chart height, the [`maintainAspectRatio`](#configuration-options) option must also be set to `false`.

## Flexbox / Grid Layout

To prevent overflow issues when using flexbox / grid layout, you must set the flex / grid child element to have a `min-width` of `0`.
See [issue 4156](https://github.com/chartjs/Chart.js/issues/4156#issuecomment-295180128) for more details.

```html
<div class="grid-container" style="display: grid">
  <div class="chart-container" style="min-width: 0">
    <canvas id="chart"></canvas>
  </div>
</div>
```

## Printing Resizable Charts

CSS media queries allow changing styles when printing a page. The CSS applied from these media queries may cause charts to need to resize. However, the resize won't happen automatically. To support resizing charts when printing, you need to hook the [onbeforeprint](https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onbeforeprint) event and manually trigger resizing of each chart.

```javascript
function beforePrintHandler () {
    for (let id in Chart.instances) {
        Chart.instances[id].resize();
    }
}
```

You may also find that, due to complexities in when the browser lays out the document for printing and when resize events are fired, Chart.js is unable to properly resize for the print layout. To work around this, you can pass an explicit size to `.resize()` then use an [onafterprint](https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onafterprint) event to restore the automatic size when done.

```javascript
window.addEventListener('beforeprint', () => {
  myChart.resize(600, 600);
});
window.addEventListener('afterprint', () => {
  myChart.resize();
});
```

---

## Licence notice (MIT)

The MIT License (MIT)

Copyright (c) 2014-2024 Chart.js Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
