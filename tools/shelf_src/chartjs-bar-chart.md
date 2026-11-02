---
id: chartjs-bar-chart
title: "Chart.js: Bar chart (dataset options, bar width, stacked and horizontal bars)"
publisher: "Chart.js contributors"
url: https://github.com/chartjs/Chart.js/blob/71d44219e79e3ac41e6f9dc907022eebf574868d/docs/charts/bar.md
licence: MIT
licence_url: https://github.com/chartjs/Chart.js/blob/71d44219e79e3ac41e6f9dc907022eebf574868d/LICENSE.md
retrieved: 2026-11-02
kind: excerpt
repo: chartjs/Chart.js
path: docs/charts/bar.md
commit: 71d44219e79e3ac41e6f9dc907022eebf574868d
topics: [dataviz, chartjs, bar-chart, javascript]
---
> Excerpt from `docs/charts/bar.md` in https://github.com/chartjs/Chart.js at commit 71d44219e79e3ac41e6f9dc907022eebf574868d. Copyright (c) 2014-2024 Chart.js Contributors. Released under the MIT licence (notice at the end of this page). Retrieved 2026-11-02.
> Trimmed; "[…]" marks cuts.

# Bar Chart

A bar chart provides a way of showing data values represented as vertical bars. It is sometimes used to show trend data, and the comparison of multiple data sets side by side.

```js
// <block:config:0>
const config = {
  type: 'bar',
  data: data,
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  },
};
// </block:config>
```

[…]

### Example dataset configuration

```javascript
data: {
    datasets: [{
        barPercentage: 0.5,
        barThickness: 6,
        maxBarThickness: 8,
        minBarLength: 2,
        data: [10, 20, 30, 40, 50, 60, 70]
    }]
};
```

[…]

### barPercentage

Percent (0-1) of the available width each bar should be within the category width. 1.0 will take the whole category width and put the bars right next to each other. [more...](#barpercentage-vs-categorypercentage)

### categoryPercentage

Percent (0-1) of the available width each category should be within the sample width. [more...](#barpercentage-vs-categorypercentage)

### barThickness

If this value is a number, it is applied to the width of each bar, in pixels. When this is enforced, `barPercentage` and `categoryPercentage` are ignored.

If set to `'flex'`, the base sample widths are calculated automatically based on the previous and following samples so that they take the full available widths without overlap. Then, bars are sized using `barPercentage` and `categoryPercentage`. There is no gap when the percentage options are 1. This mode generates bars with different widths when data are not evenly spaced.

If not set (default), the base sample widths are calculated using the smallest interval that prevents bar overlapping, and bars are sized using `barPercentage` and `categoryPercentage`. This mode always generates bars equally sized.

### maxBarThickness

Set this to ensure that bars are not sized thicker than this.

## Scale Configuration

The bar chart sets unique default values for the following configuration from the associated `scale` options:

| Name | Type | Default | Description
| ---- | ---- | ------- | -----------
| `offset` | `boolean` | `true` | If true, extra space is added to both edges and the axis is scaled to fit into the chart area.
| `grid.offset` | `boolean` | `true` | If true, the bars for a particular data point fall between the grid lines. The grid line will move to the left by one half of the tick interval. If false, the grid line will go right down the middle of the bars. [more...](#offsetgridlines)

[…]

### Offset Grid Lines

If true, the bars for a particular data point fall between the grid lines. The grid line will move to the left by one half of the tick interval, which is the space between the grid lines. If false, the grid line will go right down the middle of the bars. This is set to true for a category scale in a bar chart while false for other scales or chart types by default.

[…]

## barPercentage vs categoryPercentage

The following shows the relationship between the bar percentage option and the category percentage option.

```
// categoryPercentage: 1.0
// barPercentage: 1.0
Bar:        | 1.0 | 1.0 |
Category:   |    1.0    |
Sample:     |===========|

// categoryPercentage: 1.0
// barPercentage: 0.5
Bar:          |.5|  |.5|
Category:  |      1.0     |
Sample:    |==============|

// categoryPercentage: 0.5
// barPercentage: 1.0
Bar:             |1.0||1.0|
Category:        |   .5   |
Sample:     |==================|
```

[…]

## Stacked Bar Chart

Bar charts can be configured into stacked bar charts by changing the settings on the X and Y axes to enable stacking. Stacked bar charts can be used to show how one data series is made up of a number of smaller pieces.

```javascript
const stackedBar = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        scales: {
            x: {
                stacked: true
            },
            y: {
                stacked: true
            }
        }
    }
});
```

## Horizontal Bar Chart

A horizontal bar chart is a variation on a vertical bar chart. It is sometimes used to show trend data, and the comparison of multiple data sets side by side.
To achieve this, you will have to set the `indexAxis` property in the options object to `'y'`.
The default for this property is `'x'` and thus will show vertical bars.

[…]

### Horizontal Bar Chart config Options

The configuration options for the horizontal bar chart are the same as for the [bar chart](#scale-configuration). However, any options specified on the x-axis in a bar chart, are applied to the y-axis in a horizontal bar chart.

---

## Licence notice (MIT)

The MIT License (MIT)

Copyright (c) 2014-2024 Chart.js Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
