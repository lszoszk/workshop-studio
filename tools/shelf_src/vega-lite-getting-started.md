---
id: vega-lite-getting-started
title: "Vega-Lite: Introduction tutorial (marks, encoding, aggregation, embed in a web page)"
publisher: "University of Washington Interactive Data Lab (Vega-Lite contributors)"
url: https://github.com/vega/vega-lite/blob/4a29260c30c2a7352ec681ecca65c0c2ad960dfc/site/tutorials/getting_started.md
licence: BSD-3-Clause
licence_url: https://github.com/vega/vega-lite/blob/4a29260c30c2a7352ec681ecca65c0c2ad960dfc/LICENSE
retrieved: 2026-11-02
kind: excerpt
repo: vega/vega-lite
path: site/tutorials/getting_started.md
commit: 4a29260c30c2a7352ec681ecca65c0c2ad960dfc
topics: [dataviz, vega-lite, javascript, declarative]
---
> Excerpt from `site/tutorials/getting_started.md` in https://github.com/vega/vega-lite at commit 4a29260c30c2a7352ec681ecca65c0c2ad960dfc. Copyright (c) 2015, University of Washington Interactive Data Lab. Released under the BSD 3-Clause licence (notice at the end of this page). Retrieved 2026-11-02.
> Trimmed; "[…]" marks cuts.
> Site-template items are dropped (embedded live demos, table-of-contents tags); relative links to other Vega-Lite pages are reduced to their text. The three CDN script URLs below contain version placeholders in the original source (Jekyll template variables): when you write the page, put explicit pinned version numbers there.

This tutorial will guide through the process of writing a visualization specification in Vega-Lite. We will walk you through all main components of Vega-Lite by adding each of them to an example specification one-by-one. After creating the example visualization, we will also guide you how to embed the final visualization on a web page.

[…]

## The Data

Let's say you have a tabular data set with a categorical variable in the first column `a` and a numerical variable in the second column `b`.

[…]

## Encoding Data with Marks

Now we have a data source but we haven't defined yet how the data should be visualized.

Basic graphical elements in Vega-Lite are _marks_. Marks provide basic shapes whose properties (such as position, size, and color) can be used to visually encode data, either from a data field (or a variable), or a constant value.

To show the data as a point, we can set the `mark` property to `point`.

Now, it looks like we get a point. In fact, Vega-Lite renders one point for each object in the array, but they are all overlapping since we have not specified each point's position.

To visually separate the points, data variables can be mapped to visual properties of a mark. For example, we can _encode_ the variable `a` of the data with `x` channel, which represents the x-position of the points. We can do that by adding an `encoding` object with its key `x` mapped to a channel definition that describes variable `a`.

```js
...
"encoding": {
  "x": {"field": "a", "type": "nominal"}
}
...
```

The `encoding` object is a key-value mapping between encoding channels (such as `x`, `y`) and definitions of the mapped data fields. The channel definition describes the field's name (`field`) and its data type (`type`). In this example, we map the values for field `a` to the _encoding channel_ `x` (the x-location of the points) and set `a`'s data type to `nominal`, since it represents categories. (See the documentation for more information about data types.)

In the visualization above, Vega-Lite automatically adds an axis with labels for the different categories as well as an axis title. However, 3 points in each category are still overlapping. So far, we have only defined a visual encoding for the field `a`. We can also map the field `b` to the `y` channel.

```js
...
"y": {"field": "b", "type": "quantitative"}
...
```

This time we set the field type to be `quantitative` because the values in field `b` are numeric.

Now we can see the raw data points. Note that Vega-Lite automatically adds grid lines to the y-axis to facilitate comparison of the `b` values.

## Data Transformation: Aggregation

Vega-Lite also supports data transformation such as aggregation. By adding `"aggregate": "average"` to the definition of the `y` channel, we can see the average value of `a` in each category. For example, the average value of category `D` is `(1 + 2 + 6)/3 = 9/3 = 3`.

Great! You computed the aggregate values for each category and visualized the resulting value as a point. Typically aggregated values for categories are visualized using bar charts. To create a bar chart, we have to change the mark type from `point` to `bar`.

```diff
- "mark": "point"
+ "mark": "bar"
```

Since the quantitative value is on `y`, you automatically get a vertical bar chart. If we swap the `x` and `y` channel, we get a horizontal bar chart instead.

[…]

## Publish your Visualization Online

You have learned about basic components of a Vega-Lite specification. Now, let's see how to publish your visualization.

You can use [Vega-Embed](https://github.com/vega/vega-embed) to embed your Vega-Lite visualization in a webpage. For example, you can create a web page with the following content:

```html
<!doctype html>
<html>
  <head>
    <title>Vega-Lite Bar Chart</title>
    <meta charset="utf-8" />

    <script src="https://cdn.jsdelivr.net/npm/vega@{{ site.data.versions.vega }}"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@{{ site.data.versions.vega-lite }}"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@{{ site.data.versions.vega-embed }}"></script>

    <style media="screen">
      /* Add space between Vega-Embed links  */
      .vega-actions a {
        margin-right: 5px;
      }
    </style>
  </head>
  <body>
    <h1>Template for Embedding Vega-Lite Visualization</h1>
    <!-- Container for the visualization -->
    <div id="vis"></div>

    <script>
      // Assign the specification to a local variable vlSpec.
      var vlSpec = {
        $schema: 'https://vega.github.io/schema/vega-lite/v6.json',
        data: {
          values: [
            {a: 'C', b: 2},
            {a: 'C', b: 7},
            {a: 'C', b: 4},
            {a: 'D', b: 1},
            {a: 'D', b: 2},
            {a: 'D', b: 6},
            {a: 'E', b: 8},
            {a: 'E', b: 4},
            {a: 'E', b: 7},
          ],
        },
        mark: 'bar',
        encoding: {
          y: {field: 'a', type: 'nominal'},
          x: {
            aggregate: 'average',
            field: 'b',
            type: 'quantitative',
            axis: {
              title: 'Average of b',
            },
          },
        },
      };

      // Embed the visualization in the container with id `vis`
      vegaEmbed('#vis', vlSpec);
    </script>
  </body>
</html>
```

In this webpage, we first load the dependencies for Vega-Lite (Vega-Embed, Vega, and Vega-Lite) in the `<head/>` tag of the document. We also create an HTML `<div/>` element with id `vis` to serve as a container for the visualization.

In the JavaScript code, we create a variable `vlSpec` that holds the Vega-Lite specification in JSON format. The `vegaEmbed` method translates a Vega-Lite specification into a Vega specification and then calls the [Vega Runtime](https://vega.github.io/vega/usage/) to display visualization in the container `<div/>` element.

If viewed in a browser, this page displays our bar chart like on our demo page. You can also fork our [Vega-Lite Block example](https://bl.ocks.org/domoritz/455e1c7872c4b38a58b90df0c3d7b1b9).

---

## Licence notice (BSD 3-Clause)

Copyright (c) 2015, University of Washington Interactive Data Lab.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
  may be used to endorse or promote products derived from this software
  without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
