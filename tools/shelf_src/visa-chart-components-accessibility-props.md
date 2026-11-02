---
id: visa-chart-components-accessibility-props
title: "Visa Chart Components: accessibility props of the bar chart (descriptions, summary, keyboard, data table)"
publisher: "Visa, Inc. (Visa Chart Components)"
url: https://github.com/visa/visa-chart-components/blob/8b657d1ccc3f0799eccdba31c5f669e402d4133c/packages/bar-chart/README.md
licence: MIT
licence_url: https://github.com/visa/visa-chart-components/blob/8b657d1ccc3f0799eccdba31c5f669e402d4133c/LICENSE
retrieved: 2026-11-02
kind: excerpt
repo: visa/visa-chart-components
path: packages/bar-chart/README.md
commit: 8b657d1ccc3f0799eccdba31c5f669e402d4133c
topics: [dataviz, accessibility, visa-chart-components, screen-reader, alt-text]
---
> Excerpt from `packages/bar-chart/README.md` in https://github.com/visa/visa-chart-components at commit 8b657d1ccc3f0799eccdba31c5f669e402d4133c. Copyright (c) Visa, Inc. Released under the MIT licence (notice at the end of this page). Retrieved 2026-11-02.
> Trimmed; "[…]" marks cuts.
> Only the "Accessibility Props" section of the bar-chart README is excerpted; table padding is collapsed and the heading anchor markup is removed.

## Accessibility Props

| Name | Type | Default Value(s) | Description |
| --- | --- | --- | --- |
| `accessibility` | object (custom type) | [IAccessibilityType](../types/src/prop-types.ts) | Manages messages and settings for chart accessibility, _see object definition below_. |

### IAccessibilityType Definition

| Name (accessibility.) | Type | Default Value(s) | Description |
| --- | --- | --- | --- |
| `longDescription` | string | '' | Use this to add a helpful description of the chart. |
| `executiveSummary` | string | '' | Use this to describe the biggest takeaway of the chart. |
| `purpose` | string | '' | Use this to describe the purpose of this particular chart. |
| `contextExplanation` | string | '' | Use this to explain any controls or content on your page that affect or are affected by this chart. |
| `title` | string | '' | Gives the chart an alternate title to be used by screen readers. |
| `elementDescriptionAccessor` | string | '' | Optional key used to add an additional description to any element, from your data. |
| `statisticalNotes` | string | '' | Use this to provide any statistical explanations, such as trends, clusters, patterns, or outliers. |
| `structureNotes` | string | '' | Use this to describe special visual features of the chart, such as sorting, color grouping, etc. |
| `includeDataKeyNames` | boolean | false | If true, includes data key names in voice over description of each element. EG "Year over year growth: 5.6%" instead of just "5.6%" |
| `hideDataTableButton` | boolean | false | If true, hides the data table button (but it is still available to screen reader users). |
| `disableValidation` | boolean | false | If true, disables validations of accessibility props for this chart. Validation is intended to be used during development; upon completion, validation should be disabled. |
| `elementsAreInterface` | any/boolean | null | Defaults to null. Set to true if interacting with the elements in this chart affects your application. Otherwise, must be set to false. |
| `onChangeFunc` | function | `undefined` | Custom event listener (changeFunc) that enables dev to control accessibility page experience when chart data updates. |
| `showSmallLabels` | boolean | false | Defaults to false. Set to true if you would like to display labels on small elements that are likely to overlap. Note, this could impact accessibility of your graphic. |
| `hideStrokes` | boolean | false | Defaults to false. Set to true if you would like to remove automated stroke outlines from the chart, note, this could impact accessibility of your graphic. |
| `hideTextures` | boolean | false | Defaults to false. Set to true if you would like to remove textures from the chart, note, this could impact accessibility of your graphic. |
| `keyboardNavConfig` | [IKeyConfig](../types/src/prop-types.ts) | `{ disabled: false }` | Defaults disabled to false. May be set to true if `accessibility.elementsAreInterface = false` and `suppressEvents = true`. This will disable keyboard navigation and simplify chart instructions for screen reader users. |
| `showExperimentalTextures` | boolean | false | Defaults to false. Set to true if you would like leverage our textures which are still undergoing research and development. |

```js
// accessibility = { ...accessibility, onChangeFunc: d => changeHandler(d)}
// example of setting updates on page based on changeFunc custom events
const changeHandler = d => {
  if (d.updated && (d.removed || d.added)) {
    let updates = 'The bar chart has ';
    if (d.removed) {
      updates += 'removed ' + d.removed + ' bar' + (d.removed > 1 ? 's ' : ' ');
    }
    if (d.added) {
      updates += (d.removed ? 'and ' : '') + 'added ' + d.added + (d.removed ? '' : d.added > 1 ? ' bars' : ' bar');
    }
    setChartUpdates(updates);
  } else if (d.updated) {
    const newUpdate = "The chart's data has changed, but no bars were removed or added.";
    setChartUpdates(
      newUpdate !== chartUpdates ? newUpdate : "The chart's data has changed again, but no bars were removed or added."
    );
  }
};
```

---

## Licence notice (MIT)

Copyright (c) Visa, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
