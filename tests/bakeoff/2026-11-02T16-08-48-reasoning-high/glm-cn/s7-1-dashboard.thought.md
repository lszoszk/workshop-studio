Let me build the dashboard per the plan. Single HTML file, Chart.js available. Follow all rules carefully.

Key details:
- Title with country from WORKSHOP_DATA.uhri.country.
- Filter bar: mechanism dropdown, body dropdown, year from/to, SDG dropdown, keyword, Reset.
- "Showing X of Y records" + plain filter description.
- Horizontal bar chart top 10 themes, count labels.
- Table newest first, date, body, symbol linked, first line of text. Expandable rows. 100 at a time, "Show more".
- Only type "Recommendations" or "Concerns/Observations" counted anywhere — filter dataset first.

Chart horizontal bars: longest on top → in Chart.js with indexAxis: 'y', reverse order or sort so the largest is at top. If I put data ascending, first item appears at bottom by default; so sort descending and use reverse: true? Simpler: sort ascending and Chart draws first at bottom... Actually in Chart.js horizontal bar, the first data point is at the bottom of y-axis by default (category axis goes bottom-to-top). So to have longest on top, either sort ascending (smallest first at bottom, largest at top) or set reverse. I'll sort ascending and it'll put longest on top... wait: first category at bottom, last at top. If sorted ascending, last is largest → top. Yes. Or set `reverse: true` with descending. I'll sort descending and set y reverse: true. Either works.

Count labels: use a datalabels plugin? Not available (no external plugins). I can draw custom labels with a simple plugin inline — Chart.js allows custom plugin in config. Write a small inline plugin that draws value at end of each bar.

Ties broken alphabetically: sort by count desc, then theme asc.

Year range inputs: number inputs. If both empty, no filter. Parse ints.

SDG dropdown: unique sdgs across (filtered-type) records, sorted numerically, label "16 – Peace, justice and strong institutions" using sdg_names. Option for "All SDGs".

Body dropdown: unique bodies sorted alphabetically.

Keyword: case-insensitive substring on text.

Filter description string: build parts: mechanism, body, year range, SDG, keyword. E.g. "Treaty bodies · 2015–2020 · keyword: torture". If no filters: "all records" or "no filters applied".

Table: newest first by date. Missing date sorts last, shows "date unknown". Sort by date descending; records without date at end (sort among themselves maybe by id, keep stable).

First line: text up to first line break or 160 chars + "…". Careful: "up to its first line break or 160 characters plus '…'". So take substring before first \n; if length > 160 truncate to 160 and add "…". If truncated at line break... The spec: "the first line is `text` up to its first line break or 160 characters plus '…'". I'll do: firstLine = text.split('\n')[0]; if (firstLine.length > 160) firstLine = firstLine.slice(0,160) + '…'. Hmm, does the "…" get added when truncated at 160 only, or also at line break? Test 5 says full paragraph appears word for word. The "…" seems for the 160-char truncation. But if text is cut at line break and more text follows, arguably "…" too. The plan says "up to its first line break or 160 characters plus '…'" — ambiguous. I'll add "…" whenever the shown first line is shorter than the full text (either line break or char cut). That's reasonable and safe. Actually let me re-read: "the first line is `text` up to its first line break or 160 characters plus '…'". I'll interpret: cut at first line break, or if no line break within 160, cut at 160; append "…" if anything was cut. Hmm, but if the text is exactly one line and under 160, no "…". Good.

Expandable rows: click row toggles a details row with full text, themes, SDGs (with names?), affected persons maybe. Plan says "full paragraph with its themes and SDGs". Include affected_persons too? Fields used include affected_persons. Expanded view: "full paragraph with its themes and SDGs". I'll also show affected persons since it's listed in fields used — fine to include, harmless. Keep simple: Themes: ...; SDGs: ...; Affected persons: ... Empty themes/sdgs → "none recorded".

Charts: no matches → show "No records match these filters" instead of empty chart. Hide canvas, show message.

"How this is computed" note near chart.

Also top: source, count, years. Source: WORKSHOP_DATA.uhri.source and source_url? The file has `source`, `source_url`, `built`. Show source linked maybe. Keep: "Source: {source} · {count} records · {minYear}–{maxYear}".

Base type filter: "Only recommendations and concerns/observations are counted anywhere." So filter records where type is one of those two. But what if other types exist? Apply as base filter. Y = base count (all records after type filter). Actually "total number of records" — should be count after the type filter? The rules say only those two types are counted anywhere. So Y = number of records of those types. I'll compute base = records.filter(type in [Recommendations, Concerns/Observations]).

Chart theming: accent #1f6fb2.

Show more: render 100 rows, button loads next 100.

Reset button: clears all filters, re-renders.

Implementation structure: plain JS, no framework. Keep under ~700 lines.

Let me write the code.

Chart custom plugin for labels:

```js
const valueLabelPlugin = {
  id: 'valueLabels',
  afterDatasetsDraw(chart) {
    const {ctx} = chart;
    const meta = chart.getDatasetMeta(0);
    meta.data.forEach((bar, i) => {
      const v = chart.data.datasets[0].data[i];
      ctx.save();
      ctx.fillStyle = '#333';
      ctx.font = '13px sans-serif';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(v, bar.x + 6, bar.y);
      ctx.restore();
    });
  }
};
```

Need chart area to allow room for labels — set x max slightly above? Chart.js auto-scales to data max; labels at bar.x+6 might overflow right edge. I can set suggestedMax = max*1.1 or layout padding right. I'll add layout padding right: 40.

Row expansion: build table with tbody rows; each record gets a main <tr> plus a hidden <tr class="detail">. Toggle display on click.

Date formatting: show as-is (YYYY-MM-DD) or nicer? Keep ISO or format "10 Jul 2025". I'll format as e.g. "10 Jul 2025" — readable. Or keep simple: date as given. Plan says "date". I'll display formatted but simple; actually keep the raw date to avoid ambiguity — "2025-07-10" is fine and precise. Hmm, for diplomats maybe nicer format. I'll format to "10 Jul 2025". Fine.

Sorting with missing dates: date missing → sort last. Within, sort by date string descending.

Filters description: e.g. parts joined with " · ". Mechanism name, body name, year range "2015–2020", "SDG 16: Peace…", "keyword: torture". If none: "no filters — showing all records".

Keyword matching: case-insensitive on `text` only.

Note near chart: "How this is computed: each matching record contributes one count per theme it lists; a record with several themes is counted once for each. Only the 10 most frequent themes are shown; records with no recorded theme do not appear."

Let me also handle mechanism/body dropdown values from data.

Expanded SDGs display: "SDG 16 – Peace, justice and strong institutions". Use sdg_names map; keys are strings of numbers.

Write full HTML now. Keep CSS clean, UN-portal style.

Header description: "Source: {source} (linked to source_url if present) · n records · earliest–latest". Also "built" maybe not needed.

Escape HTML in text when injecting. Write esc() helper.

Detail row content: full text in a <p>, then meta lists: Themes, SDGs, Affected persons.

Show more button below table; hide when all shown. Also show "Showing 100 of X records in the table" maybe — keep simple: "Show more (N more)".

Chart: destroy and recreate on each update, or update data. Recreate is simpler.

Empty chart case: replace canvas parent with message. I'll have a div #chartWrap containing canvas and a p #noChart hidden.

Test 1: "Showing X of Y" X==Y on load — yes since no filters.

Let me write it.

Also table columns: Date, Body, Symbol, Text preview. Body column shows body or "unknown". Symbol: linked if doc_url else unlinked; if no symbol "(no symbol)". Also maybe show type? Not required. Keep four columns.

Row click: clicking anywhere on the main row toggles; but clicking the symbol link shouldn't toggle — stop propagation on link click.

Now write:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UN human rights recommendations</title>
<style> ... </style>
</head>
<body>
<header>
  <h1 id="title"></h1>
  <p id="subtitle" class="subtitle"></p>
</header>
<section class="filters"> ... </section>
<p id="showing"></p>
<p id="filterDesc" class="muted"></p>
<section class="chart-block">
  <h2>Most frequent themes</h2>
  <div id="chartWrap"><canvas id="themeChart"></canvas></div>
  <p id="noChart" class="muted" hidden>No records match these filters</p>
  <p class="note">How this is computed: ...</p>
</section>
<section>
  <h2>Records</h2>
  <table>...</table>
  <button id="showMore">Show more</button>
</section>
<script> ... </script>
</body>
</html>
```

JS:

```js
const U = window.WORKSHOP_DATA.uhri;
const ALL = U.records.filter(r => r.type === 'Recommendations' || r.type === 'Concerns/Observations');
```

Years: min/max of ALL by year (skip null years? if year missing, ignore in min/max). Use filtered finite years.

Subtitle: `Source: <a>U.source</a> · N records · A–B`. If min or max missing handle gracefully.

Filters state read from controls each change; single update() function.

Mechanism dropdown: '' = All mechanisms; unique sorted from ALL.
Body dropdown: same.
SDG: unique sdgs flattened, sorted numeric; label `${n} – ${sdg_names[n] || ''}`.

Year from/to: if from > to, treat as no matches? Just filter normally (from <= r.year <= to) — empty result naturally. Fine.

matches(r):
- mech === '' || r.mechanism === mech
- body likewise
- from: r.year >= from (if from set; if r.year missing, record fails when year filter active? Hmm. If year filter active and record has no year, exclude — reasonable.)
- keyword: r.text.toLowerCase().includes(kw)

Chart data: counts map over matching; sort by count desc then name asc; take top 10; for chart, reverse so longest on top (put largest last in array with default axis, or set reverse). I'll pass labels/data in ascending order... Let me just compute top10 sorted desc (best first), then for chart reverse arrays so array[0] = smallest → drawn at bottom; array last = largest at top. Wait default: first category at bottom? In Chart.js, category axis default: labels start at the bottom for y? Actually for a horizontal bar chart (indexAxis 'y'), the y-axis is a category axis; by default the first label appears at the top. Hmm. Let me recall: In Chart.js bar chart, default category axis order — the first data point is at the top? I believe in v3/v4, for vertical bars first is leftmost; for horizontal bars (indexAxis:'y'), the first is at the top... no wait.

Testing memory: Chart.js horizontal bar — data renders top to bottom, first item at top. Hmm, actually I recall that horizontal bar charts in Chart.js show the first label at the top by default... No — I remember people complaining that horizontal bars appear in reverse order (first item at bottom), and the fix is `reverse: true` on... Hmm. Let me think about the coordinate system: y=0 is at the bottom of the canvas. Category scale by default positions the first category at the smallest coordinate... The category scale's default is that labels go from bottom to top for y axes? For the y category axis in a horizontal bar chart, Chart.js docs: "the chart is rendered with the first bar at the top"? 

From experience: with indexAxis:'y' and data [a,b,c], 'a' appears at the top. Actually no — I've built horizontal bar charts and found that the first item appears at the bottom, requiring reverse. Hmm.

Let me reason from Chart.js source: CategoryScale computes pixel for value via getPixelForValue, index maps to position; for vertical axis, index 0 → lowest pixel? The scale's direction: charts draw y-axis from bottom (min) to top (max). CategoryScale extends Scale, and for index 0 the position... In CategoryScale, `getPixelForValue` uses `this.getPixelForDecimal((index + offset) / ...)`. Hmm hard to recall exactly.

I recall clearly: In Chart.js horizontal bar charts, data appears in reverse order relative to the array (first element at the bottom). Many StackOverflow questions "Chart.js horizontal bar chart order reversed" with answer "set reverse: true". Hmm, but also there are questions the other way.

Actually I'm fairly confident: with indexAxis: 'y', the first item in the data array is drawn at the TOP. Let me think of the default axis: for a horizontal bar, the category axis is y. Chart.js scale default `reverse: false` means values ascend along axis direction. For y-axis, ascending goes bottom→top, so index 0 at bottom. Hmm, but for category counts, "ascending" means first category at the start of the axis; y-axis start is bottom. So first category at bottom. 

Hmm wait — but for line charts, the x category axis first label is left. For horizontal bar, y category axis first label is... I believe bottom. But I genuinely recall seeing horizontal bar charts with first item on top...

Safest: sort data descending (largest first) and set y-axis `reverse: true` if needed... no, I can't be sure both ways. Alternative safest approach: use `reverse` and verify? Can't verify.

Let me settle with strong memory: Chart.js docs example "Horizontal Bar Chart" — the dataset ['January','February',...] with random values; in the rendered image, January appears at the top. Hmm, I picture the docs' horizontal bar image... I genuinely think in the docs image the first month is at the top.

Actually, decisive reasoning: CategoryScale in Chart.js v3+: it has `getPointPosition`... For the index axis, Chart.js internally draws items in order; for indexAxis 'y', the bar for dataset index i at category j is positioned at y = yScale.getPixelForValue(j). CategoryScale.getPixelForValue(value) → getPixelForDecimal((value - this._startPixel... ) hmm.

Alternative: I remember that in Chart.js 3+, for horizontal bar charts, "the first bar is displayed at the top" is FALSE and people use reverse:true to get that. E.g., SO question "Chart.js: Horizontal bar chart, ordering from top to bottom" — answer: set `scales: { y: { reverse: true } }` because by default first item is at the bottom. I'm fairly confident about this SO question existing. Yes — "How to order horizontal bar chart in Chart.js" — default renders bottom-to-top.

Hmm, conflicting memories. Let me think about a fresh Chart.js bar with indexAxis:'y': labels ['A','B','C']. The y-axis labels would be C at top? or A at top?

In Chart.js, the y-axis for a horizontal bar chart is a category scale. Category scale default: `reverse: false`. The scale's values increase from the axis minimum. For a y-axis, minimum is at the bottom. Category indices: A=0, B=1, C=2. So A at bottom, C at top. That's the mathematically consistent interpretation.

But wait — for a vertical bar chart, x category axis: A=0 at left (minimum). Consistent. So horizontal: A at bottom. But then people's intuition "first at top" leads to reverse:true. And I do recall that SO answer. OK here's another consideration: many tutorials on "sorting bar charts" with Chart.js sort data ascending for horizontal charts so the largest is on top. E.g., "sort your data before passing to get largest at top". Yes, I've seen that: "for horizontal bar charts, sort ascending so the biggest bar is at the top."

Hmm, but actually now I remember the opposite too: dataviz articles... 

I'll go with: default first item at bottom → to get largest on top, put largest LAST in the array (ascending order). If my memory is wrong, the chart would show largest at bottom — a visual imperfection but not a functional failure against tests. Hmm, but the plan explicitly says "longest bar on top". Let me be more certain.

Chart.js v4 source, CategoryScale: 

```js
getPixelForValue(value) {
  ...
  return this.getPixelForDecimal((index - offset) / this._valueRange?) 
```

Actually CategoryScale.getPixelForDecimal(decimal) returns `_reversePixels ? start - decimal... : start + decimal * (end-start)`? Hmm.

Scale base: getPixelForDecimal: `start + decimal * (end - start)` where for y scale, start = top? No... In Scale.configure, `this._startPixel` etc. Hmm. For a linear y-scale, pixel for min value is at the bottom (canvas y high). getPixelForDecimal(0) should give the pixel for the minimum. For a y-axis, minimum at bottom of canvas = larger canvas y coordinate. Chart.js handles axis direction internally ("left"/"bottom" position axes have different orientations).

Actually for scales positioned 'left', Chart.js's pixel for decimal 0 is the TOP of the chart area (since pixel coordinates increase downward and... no). Ugh.

Empirical memory attempt: I've definitely written `indexAxis: 'y'` charts where I passed labels in normal order and they appeared top-to-bottom matching array order. E.g., many dashboard tutorials: labels ['Red','Blue','Yellow'] appear with Red at top in horizontal bar. Hmm... I picture the Chart.js docs "Bar Chart" page horizontal example with months — and I believe January was at the top in that image.

Counter-memory: SO question with hundreds of upvotes: "Chart.js bar chart order is reversed" — no, that one is about stacking? 

OK here's a cleaner empirical anchor: Chart.js horizontal bar — there's a well-known behavior that to get the "first item at the top" you need to reverse the data OR set reverse:true, and the docs for the horizontal bar example don't do anything special... In the official docs example (chartjs.org docs, "Bar Chart" → Horizontal Bar Chart), the code just uses labels months and default config. The rendered image: I recall seeing January at top, December at bottom. I'll trust this: first item at top by default for indexAxis 'y'.

Hmm, wait. Why would that be? Because Chart.js category scale for the y-axis: category scale's `_startPixel`... For index axis, Chart.js draws ticks from the axis start; for 'left' axes, tick 0 is at the top (since canvas coordinates). Actually yes! Canvas y-coordinates increase downward, and scales positioned on the left compute pixel positions... for a linear y-scale, value min is at the bottom — but that's because linear scale maps min→chartArea.bottom. Category scale could map index 0 → chartArea.bottom too... but then ticks would go 0,1,2 from bottom to top, which would look "reversed" against typical reading.

I now recall definitively: there IS a known quirk. From Chart.js docs on category axis? No. From experience building charts: when I made a horizontal bar with data [10, 20, 30] and labels [A, B, C], the bar for A (10) was at the TOP. I'm going to commit to: first item at top.

Hmm, let me find one more anchor. The SO question "Chart.js — horizontal bar chart shows data in reverse order" — I'm now fairly sure this exists with the accepted answer "This is because the y-axis... use reverse: true" and it has many upvotes... but there's also "Chart.js horizontal bar chart: how to sort descending"...

The stakes: if wrong, the longest bar is at the bottom instead of top. Tests listed don't include "longest on top" as a check item, but the plan requires it. I want to get it right.

Let me actually reason through Chart.js v4 source more carefully from memory.

`class Scale extends Element` — `getPixelForDecimal(decimal)`: 
```js
getPixelForDecimal(decimal) {
  const me = this;
  if (me._reversePixels) {
    decimal = 1 - decimal;
  }
  return _int16Range(me._startPixel + decimal * me._length);
}
```
Hmm, something like that. And for scales, `_startPixel` is set in `configure()`: 
```js
configure() {
  ...
  const reverse = !this._reversePixels? ...
}
```
Actually in Scale.configure:
```js
const pixels = ...
if (this.options.position === 'left' || 'right') ...
```

Hmm, in `Chart` layout, for 'left' axis, `_startPixel` = chartArea.top and `_length` = chartArea.height? If getPixelForDecimal(0) = top for left axes, then value 0 (min) maps to top — but for a linear y-scale, the min is at the bottom! So there must be direction handling: for 'left'/'right' axes, the scale computes pixels in reverse (min at bottom). In Scale base class there's this in configure:

```js
// vertical scales: y increases from bottom to top? 
```

I recall in Scale:
```js
getPixelForDecimal(decimal) {
  if (this._reversePixels) decimal = 1 - decimal;
  return _int16Range(this._startPixel + decimal * this._length);
}
```
and in LinearScaleBase/LinearScale, getPixelForValue(value):
```js
const {top, bottom} = this... 
return this.getPixelForDecimal((value - this._startValue) / this._valueRange)
```
Hmm, but then min would be at top...

Wait — actually, I remember now! In Scale.configure:

```js
configure() {
    let me = this;
    let reversePixels = me.options.reverse;
    let startPixel, endPixel;
    if (me.isHorizontal()) {
      startPixel = me.left;
      endPixel = me.right;
    } else {
      startPixel = me.top;
      endPixel = me.bottom;
    }
    me._startPixel = startPixel;
    me._endPixel = endPixel;
    ...
    me._reversePixels = reversePixels? ... 
```

Hmm and then getPixelForValue for linear scale:
```js
getPixelForValue(value) {
    return value === null ? NaN : this.getPixelForDecimal((value - this._startValue) / this._valueRange);
}
```
and getPixelForDecimal:
```js
getPixelForDecimal(decimal) {
    const me = this;
    if (me._reversePixels) { decimal = 1 - decimal; }
    return _int16Range(me._startPixel + decimal * me._length);
}
```
For a left-positioned vertical scale, if _startPixel = top and decimal 0 (min value) → top... but we know linear y min is at bottom. So there must be something making _reversePixels true or swapping start/end for vertical scales. I believe in configure there's:

```js
} else {
  startPixel = me.top;
  endPixel = me.bottom;
}
me._startPixel = startPixel;
me._endPixel = endPixel;
me._pixelMargin...
me._length = endPixel - startPixel;  // negative for vertical? no, bottom > top so positive
```

Hmm, that gives min at top, which contradicts known behavior. Unless getPixelForDecimal for vertical uses `endPixel - decimal*length`. 

OK, honestly, I remember there IS asymmetry handled somewhere, since linear y-axes clearly put min at bottom. For CategoryScale on y: categories would then have index 0 at bottom (same direction as linear values). That supports "first item at bottom" for horizontal bars.

BUT — counterpoint that I keep coming back to: I have a vivid memory of horizontal bar charts in Chart.js showing first label at top without any reverse setting... That might be from other libraries (D3, matplotlib inverted axis, or Chart.js after sorting ascending, which is a common tutorial step).

Let me search memory for "indexAxis" introduction (v3): Migration guide? The v3 horizontal bar example in docs... 

Another anchor: Chart.js sample "bar-horizontal.html" in the chart.js GitHub repo:
```js
const labels = Utils.months({count: 7});
data: {
  labels: labels,
  datasets: [{
    label: 'My First Dataset',
    data: [65, 59, 80, 81, 56, 55, 40],
    ...
  }]
},
options: { indexAxis: 'y', }
```
The rendered image bar-horizontal.png in the repo... I genuinely can't picture it with certainty.

Practical resolution: Use `reverse` explicitly to force the order I want, chosen so it works under either default. That's impossible—reverse flips whichever default. 

Alternative: don't rely on memory — set the y-axis ticks `reverse: false` explicitly... that just asserts the default.

OK, decisive approach: In Chart.js, for horizontal bar charts, I'm going to go with the widely-reported fact that data is drawn with the FIRST element at the BOTTOM, and SO answers recommend either reversing the data array or `scales.y.reverse = true` to show first element at top. I'm now recalling the specific SO question: "Chart.js v2 horizontal bar chart tooltips order" ... and "Bar chart displayed in reverse order" — yes, there's a classic question about horizontal bars being "upside down" relative to expectation. Also, in Chart.js v2 days, `horizontalBar` type had this exact quirk and people always added `scales.yAxes:[{ticks:{reverse:true}}]`... wait no, in v2 horizontalBar, the category axis was `yAxes` and I remember NOT needing reverse; the bars appeared with first label at top...

Argh. Let me think about v2 'horizontalBar' concretely. I built these. labels: ['A','B'], first dataset [1,2]. Result: A at top? I recall building a "top 10" horizontal bar where I sorted descending and it looked right (biggest at top) WITHOUT reverse. Hmm, do I? Or did I sort ascending...

I also remember MDN or chartjs tutorial "make a horizontal bar chart where the largest is at the top: sort your data ascending". 

Time to just decide. Given the ambiguity, I'll implement it with y-axis `reverse: true` and data sorted DESCENDING (largest first). If the default is "first at bottom", reverse:true makes first at top → largest at top ✓. If the default is "first at top", reverse:true makes first at bottom → largest at bottom ✗.

Alternatively, no reverse, data sorted ASCENDING (largest last). If default "first at bottom": largest last → top ✓. If default "first at top": largest last → bottom ✗.

Both strategies are equivalent in risk. I need to pick the correct belief about the default.

Let me try once more with the source. I'll reconstruct Scale.configure from Chart.js v4 (I've read this code):

```js
configure() {
    let me = this;
    let reversePixels = me.options.reverse;
    let startPixel, endPixel;

    if (me.isHorizontal()) {
      startPixel = me.left;
      endPixel = me.right;
    } else {
      startPixel = me.top;
      endPixel = me.bottom;
    }
    me._startPixel = startPixel;
    me._endPixel = endPixel;
    me._pixelMargin...
    me._horizontal ? ... 
```

and:

```js
getPixelForDecimal(decimal) {
    const me = this;
    if (me._reversePixels) {
      decimal = 1 - decimal;
    }
    return _int16Range(me._startPixel + decimal * me._length);
}
```

Hmm wait, but then for a vertical linear scale, getPixelForValue(min) = _startPixel + 0 = me.top → min at top. That's WRONG for known behavior (min at bottom for y axes). So my reconstruction must be wrong. The correction: in configure:

```js
} else {
  startPixel = me.bottom;   // ← for vertical scales
  endPixel = me.top;
}
```
Hmm if startPixel = bottom and length = endPixel - startPixel = top - bottom = negative... then getPixelForDecimal(0) = bottom ✓ (min at bottom), and decimal 1 → bottom + (top-bottom) = top ✓. Yes! I think `_length` can be negative, and there's a comment about it. Actually I recall `_int16Range` and the code:

```js
me._length = endPixel - startPixel;
```

and for vertical: startPixel = me.top, endPixel = me.bottom, so length positive, but then getPixelForDecimal would need reversal... 

I actually now recall in Scale base:

```js
getPixelForDecimal(decimal) {
    const me = this;
    if (me._reversePixels) {
      decimal = 1 - decimal;
    }
    return _int16Range(me._startPixel + decimal * me._length);
}
```

and in configure, for the vertical case:
```js
} else {
    startPixel = me.top;
    endPixel = me.bottom;
}
...
me._reversePixels = ...
```
Hmm, where does `reversePixels` get set? There's:

```js
const reversePixels = me.options.reverse;
...
me._reversePixels = me.isHorizontal() ? ... 
```

No... I recall in `_configure` (renamed from configure in v4?):

```js
_configure() {
    const me = this;
    const reversePixels = me.options.reverse;
    let startPixel, endPixel;

    if (me.isHorizontal()) {
      startPixel = me.left;
      endPixel = me.right;
    } else {
      startPixel = me.top;
      endPixel = me.bottom;
    }
    me._startPixel = startPixel;
    me._endPixel = endPixel;
    me._pixelMargin = ...;
    me._horizontal = me.isHorizontal();
    me._length = endPixel - startPixel;  // hmm
    me._reversePixels = reversePixels;   
    ...
}
```

If that's it, then for a vertical scale, getPixelForDecimal(0) = top... contradiction with linear min-at-bottom. UNLESS LinearScaleBase overrides: getPixelForValue:

```js
getPixelForValue(value) {
    return value === null ? NaN : this.getPixelForDecimal((value - this._startValue) / this._valueRange);
}
```

Hmm, so min → decimal 0 → top. But empirically y-axes put min at bottom! So my reconstruction is definitely off somewhere. The actual v4 code for getPixelForDecimal... maybe:

```js
getPixelForDecimal(decimal) {
    const me = this;
    if (me._reversePixels) {
      decimal = 1 - decimal;
    }
    return _int16Range(me._startPixel + decimal * me._length);
}
```

and _configure:

```js
_configure() {
    ...
    if (me.isHorizontal()) {
      startPixel = me.left;
      endPixel = me.right;
    } else {
      startPixel = me.top;
      endPixel = me.bottom;
    }
    ...
    me._reversePixels = !me.isHorizontal() ? !reversePixels : reversePixels? 
```

Hmm, hmm. I genuinely recall something like:

```js
// vertical scales need their pixels reversed
me._reversePixels = me.isHorizontal() ? reversePixels : !reversePixels;
```

Hmm no wait — I actually recall from reading the source that horizontal and vertical differ: for horizontal scales, pixel 0 is left (matching min at left), and for vertical scales, the code sets start at bottom. Specifically I now remember this bit in `_configure`:

```js
} else {
  startPixel = me.top;
  endPixel = me.bottom;
}
```
combined with `getPixelForDecimal` using `me._startPixel + decimal * (me._endPixel - me._startPixel)`... same issue.

You know what, let me approach from CategoryScale.getPixelForValue, which I remember more specifically because of this exact question:

```js
getPixelForValue(value) {
    if (typeof value !== 'number') {
      value = this.parse(value);
    }
    return value === null ? NaN : this.getPixelForDecimal((value - this._startValue) / this._valueRange);
}
```

And CategoryScale also has `getPixelForTick(index)` → `this.getPixelForValue(this.getValueForPixel? ...` no:

```js
getPixelForTick(index) {
    const me = this;
    const ticks = me.ticks;
    if (index < 0 || index > ticks.length - 1) {
      return null;
    }
    return me.getPixelForValue(ticks[index].value);
}
```

Not decisive.

Empirical final answer attempt — I'm going to recall an actual project. In a previous Chart.js horizontal bar I wrote (with indexAxis 'y'), I passed countries sorted by value descending and the chart displayed... the largest at the TOP. And I did NOT set reverse. Hmm, but did I? I have written `reverse: true` in some projects...

Let me think about Chart.js docs' "Different Axes Types" or the horizontal example once more. chartjs.org/docs/latest/charts/bar.html — the horizontal bar chart example image: labels January..June? The image shows... bars with 'January' at top. I'm ~70% confident the docs image has the first month at the top, because I remember the picture being a normal-looking descending-list-like arrangement... no, the data is random so it wouldn't look sorted either way.

Alright — different strategy: make the order robust regardless of default. I can set the y-axis `afterFit`... no. I can just draw with the data in a specific order AND set `reverse` — under one default it's right, wrong under the other. Not robust.

Robust option: after creating the chart, I can't easily detect orientation.

Hmm, actually there IS a robust way: compute using the chart itself! After rendering, check the pixel position of the first bar: if meta.data[0].y > meta.data[last].y (canvas y grows downward), then first is at bottom → I need reverse. I could create the chart, measure, and set reverse accordingly, then update. That's hacky but deterministic. Actually simpler: create chart with reverse:false, measure pixel positions, and if data[0] is at the bottom while I want it at top... but I want largest at top; I sorted data descending, so largest is data[0]. If meta.data[0].y > meta.data[1].y (first bar lower on screen = closer to bottom), set options.scales.y.reverse = true and chart.update(). One-frame flicker maybe; "No animations that delay the result" — set animation: false, so no delay.

Hmm, that's clever but adds complexity. Is it worth it? Actually, let me just settle the fact. Let me carefully recall the Chart.js v4 source of Scale._configure — I've actually read this function:

```js
_configure() {
    const me = this;
    const reversePixels = me.options.reverse;
    let startPixel, endPixel;

    if (me.isHorizontal()) {
      startPixel = me.left;
      endPixel = me.right;
    } else {
      startPixel = me.top;
      endPixel = me.bottom;
    }
    me._startPixel = startPixel;
    me._endPixel = endPixel;
    me._pixelMargin = ... 
    me._axis = ... 
    me._length = endPixel - startPixel;   
    me._reversePixels = ... 
}
```

No... OK here it is, I remember now! The trick is in getPixelForDecimal's counterpart and in how `_startValue`/`_valueRange` are computed per orientation. For CategoryScale:

```js
handleTickRange() ...
```

No. CategoryScale:

```js
parse(raw, index) { ... return index; }
```

and 

```js
getLabelForValue(value) {...}
```

CategoryScale._configure? It has:

```js
configure() {
    super.configure();
    if (!this.isHorizontal()) {
      // reverse order for vertical
      this._reversePixels = !this._reversePixels;
    }
}
```

Hmm!! Is that real? Something tugs at me — "CategoryScale reverses pixels for vertical axes"... I believe there IS something like this! Let me think... In Chart.js source category.scale.js:

```js
export default class CategoryScale extends Scale {
  ...
  getPixelForValue(value) {
    ...
  }
```

Hmm, and in Scale.getPixelForDecimal... 

AH WAIT. I remember now, for real. In Scale:

```js
getPixelForDecimal(decimal) {
    const me = this;
    if (me._reversePixels) {
      decimal = 1 - decimal;
    }
    return _int16Range(me._startPixel + decimal * me._length);
}
```

and in Scale._configure:

```js
_configure() {
    const me = this;
    const reversePixels = me.options.reverse;
    let startPixel, endPixel;

    if (me.isHorizontal()) {
      startPixel = me.left;
      endPixel = me.right;
    } else {
      startPixel = me.top;
      endPixel = me.bottom;
    }
    me._startPixel = startPixel;
    me._endPixel = endPixel;
    ...
    me._length = endPixel - startPixel;
    me._reversePixels = reversePixels;
}
```

and LinearScaleBase.handleTickRangeOptions / LinearScale.getPixelForValue:

```js
getPixelForValue(value) {
    return value === null ? NaN : this.getPixelForDecimal((value - this._startValue) / this._valueRange);
}
```

With this, vertical linear scale: decimal 0 (min) → _startPixel = me.top → pixel at TOP. But y-axes put min at BOTTOM in reality!! Contradiction → therefore startPixel for vertical must be me.bottom:

```js
} else {
    startPixel = me.bottom;
    endPixel = me.top;
}
```

Hmm, but then _length = top - bottom < 0, and getPixelForDecimal(0) = bottom ✓, decimal 1 = bottom + (top - bottom) = top ✓. And _int16Range just clamps. So this works with negative length! And I think this IS the actual code — `_length` negative for vertical scales. Hmm, do I buy it? There's `me._length = endPixel - startPixel`... 

If that's true for ALL scales (including category), then CategoryScale on y: index 0 → decimal 0 → bottom → FIRST CATEGORY AT BOTTOM for horizontal bar charts. And with options.reverse... note `reversePixels = me.options.reverse` and `_reversePixels = reversePixels` — for a vertical scale, setting reverse:true would flip it so first at top.

Hmm wait, but that means for vertical LINE charts (category x, linear y) everything's normal, and for horizontal BARS (category y), first category at bottom. And SO: "why is my horizontal bar chart upside down" → answer: add `scales: {y: {reverse: true}}`. I DO strongly remember this SO answer. Multiple questions: "Chart.js horizontal bar chart displays data in reverse order". Yes. I'm now ~80% confident: default = first item at BOTTOM for indexAxis:'y'.

Hmm, but one more consideration: the docs example... if the default put first at bottom, the docs' horizontal example would show January at the bottom, and I feel like I'd have noticed... Whatever, 80% is decent, but let me look for the definitive memory: Chart.js GitHub issue "Horizontal bar chart order" ... 

Actually, here's a cleaner one: **the "indexAxis" docs**. When v3 introduced indexAxis, the migration docs said creating a horizontal bar chart is `indexAxis: 'y'`, equivalent to v2's `type: 'horizontalBar'`. In v2 horizontalBar — did first item show at top or bottom? I built v2 horizontalBars... I remember the y-axis labels reading top-to-bottom in array order... like a list. Hmm, in v2, for horizontalBar, the category axis was yAxes and I remember needing... 

STOP. Decision: I'll implement the robust auto-correct approach — it's only ~6 lines and guarantees correctness:

```js
chart.options.scales.y.reverse = ...based on measured pixels...
```

Actually even simpler and fully robust: build chart with data sorted descending (largest first in array). After `new Chart(...)`, check `const m = chart.getDatasetMeta(0).data; if (m.length>1 && m[0].y > m[m.length-1].y) { chart.options.scales.y.reverse = true; chart.update('none'); }`. Wait — if first item (largest) is at bottom (m[0].y > m[last].y in canvas coords, since canvas y increases downward, bottom = larger y), we want it at top → set reverse:true flips order so first item goes to top. If first already at top (m[0].y < m[last].y), leave it. 

Edge: with animation disabled, meta positions available immediately. Set `animation: false`. Also only when m.length >= 2; with 1 bar it doesn't matter.

Hmm, but wait: does `m[0]` correspond to data[0]? Yes, in order.

Is this over-engineering? Slightly, but it guarantees the stated requirement. Alternatively I can just sort ascending and also set reverse... no. I'll do the measure-and-flip. Actually, let me simplify: I'll sort data descending and always... no, measure-and-flip. Fine.

Hmm, actually there's an even simpler robust trick: put data in ascending order (largest LAST) and set `y.reverse: true`? No — still depends on default.

OK going with measure-and-flip, with a fallback: if meta data unavailable (chart hidden), skip.

Wait, actually if chart area is hidden (display:none), getDatasetMeta positions may be 0. I only render the chart when there are matches and canvas visible. Fine.

Also note: when no matches, "No records match these filters" shown instead of chart — I'll hide the canvas (display:none) and show the message. On next update with matches, show again and recreate chart (destroy old). Since I destroy/recreate each update, that's fine.

Now the rest of the app.

Line count: keep under 700. Should be fine ~450.

CSS: system font stack, #1f6fb2 accent, light bg (#f7f9fb), cards white with subtle border, base 16px.

Table styles: borders, hover, cursor pointer, expanded detail row with left accent border.

Let me write the JavaScript fully.

```js
(function(){
const U = window.WORKSHOP_DATA.uhri;
const TYPES = ['Recommendations', 'Concerns/Observations'];
const ALL = (U.records||[]).filter(r => TYPES.includes(r.type));

// header
const yearsAll = ALL.map(r=>r.year).filter(y=>typeof y==='number');
const minYear = yearsAll.length? Math.min(...yearsAll) : null;
const maxYear = yearsAll.length? Math.max(...yearsAll) : null;
document.getElementById('title').textContent = 'UN human rights recommendations to ' + (U.country||'your country');
// subtitle
const srcLink = U.source_url ? `<a href="${esc(U.source_url)}" target="_blank" rel="noopener">${esc(U.source||'Source')}</a>` : esc(U.source||'');
subtitle.innerHTML = `${srcLink} · ${ALL.length} records (recommendations and concerns/observations) · ${minYear}–${maxYear}`;
```

Wait: "total number of records" — U.count vs ALL.length? Rules: "Total and year range come from counting all records and taking the smallest and largest year." But also "Only recommendations and concerns/observations are counted anywhere." So total = ALL.length. If U.count differs, prefer ALL.length per rules. Fine.

Filter description example format: "Treaty bodies · 2015–2020 · keyword: torture".

Build description:
- mech: if set, add mechanism name.
- body: add body name.
- years: if from||to: `${from||minYear}–${to||maxYear}`... but better show exactly what's typed: if from and to: "from–to"; if only from: "from or later"; only to: "up to to". Keep simple: build "2015–2020", "since 2015", "up to 2020".
- sdg: `SDG ${n}` maybe with name.
- keyword: `keyword: “x”`.
Join with " · ", prefix "Filters: ". If empty: "No filters applied — showing all records."

Matches function:

```js
function currentMatches(){
  const mech = el.mechanism.value, body = el.body.value;
  const y1 = el.yFrom.value===''?null:parseInt(el.yFrom.value,10);
  const y2 = el.yTo.value===''?null:parseInt(el.yTo.value,10);
  const sdg = el.sdg.value===''?null:parseInt(el.sdg.value,10);
  const kw = el.keyword.value.trim().toLowerCase();
  return ALL.filter(r=>{
    if (mech && r.mechanism!==mech) return false;
    if (body && r.body!==body) return false;
    if (y1!==null || y2!==null){
      if (typeof r.year!=='number') return false;
      if (y1!==null && r.year<y1) return false;
      if (y2!==null && r.year>y2) return false;
    }
    if (sdg!==null && !(Array.isArray(r.sdgs)&&r.sdgs.includes(sdg))) return false;
    if (kw && !(typeof r.text==='string' && r.text.toLowerCase().includes(kw))) return false;
    return true;
  });
}
```

Note sdgs values are numbers per sample (e.g. [16,5]) — "e.g. 16, 5, 4, 10" — ints. But sample JSON shows "sdgs": [] and description says goal numbers. Could be strings in real data? Sample shows `"sdgs": []`. Description: "`sdgs` holds goal numbers (1–17)". I'll compare loosely: use String comparison: `r.sdgs.map(String).includes(String(sdg))`. Safer.

Sort matches for table: newest first; missing date last.

```js
function sortRows(list){
  return list.slice().sort((a,b)=>{
    const da=a.date, db=b.date;
    if(!da && !db) return 0;
    if(!da) return 1;
    if(!db) return -1;
    return db.localeCompare(da);
  });
}
```

First line:

```js
function firstLine(text){
  if(!text) return '';
  let s = String(text);
  const nl = s.indexOf('\n');
  let cut = nl>=0 ? s.slice(0,nl) : s;
  let truncated = nl>=0;
  if (cut.length>160){ cut = cut.slice(0,160); truncated = true; }
  // also if no newline and whole text <=160, nothing truncated
  return cut + (truncated ? '…' : '');
}
```

Hmm, if nl>=0 but remainder after newline is empty? Then "…" still added — minor. Fine. Actually if text = "abc\n", first line "abc…"? Slightly off but negligible. Could check s.length > cut.length. Let me do: truncated = cut.length < s.length after the 160 cut. So:

```js
let cut = nl>=0 ? s.slice(0, nl) : s;
if (cut.length > 160) cut = cut.slice(0,160);
return cut + (cut.length < s.length ? '…' : '');
```

That handles both.

Render table:

```js
const PAGE = 100;
let shown = 0;
function renderRows(list){
  shown = Math.min(PAGE, list.length);
  tbody.innerHTML='';
  for (i<shown) appendRow(list[i]);
  showMoreBtn visibility: shown < list.length;
  showMoreBtn.textContent = `Show more (${list.length - shown} remaining)`;
}
showMoreBtn.onclick = () => { add next 100 rows };
```

appendRow creates two <tr>: main and detail (hidden). Use event listener toggling.

Main row cells:
- date: r.date ? fmtDate(r.date) : 'date unknown'
- body: r.body || 'unknown'
- symbol: r.symbol ? (r.doc_url ? `<a href=... target=_blank rel=noopener>${esc(r.symbol)}</a>` : esc(r.symbol)) : '(no symbol)'
- preview: esc(firstLine(r.text))

Detail row: colspan 4, contains full text (esc, but preserve line breaks → use white-space: pre-wrap), then meta:
- Themes: r.themes?.length ? join ', ' : 'none recorded'
- SDGs: list of `16 – name` or 'none recorded'
- Affected persons: length ? join : maybe omit or 'none recorded'. Plan mentions empty themes/sdgs → "none recorded". For affected persons I'll show similarly.

fmtDate: parse ISO, output "10 Jul 2025"; fallback to raw string if unparseable.

```js
function fmtDate(d){
  const t = Date.parse(d);
  if(isNaN(t)) return d;
  const dt = new Date(t);
  const months=['Jan',...];
  return `${dt.getUTCDate()} ${months[dt.getUTCMonth()]} ${dt.getUTCFullYear()}`;
}
```

Chart:

```js
let chart=null;
function renderChart(list){
  const counts = {};
  list.forEach(r=>(r.themes||[]).forEach(t=>{counts[t]=(counts[t]||0)+1;}));
  let entries = Object.entries(counts)
    .sort((a,b)=> b[1]-a[1] || a[0].localeCompare(b[0]))
    .slice(0,10);
  // entries[0] = largest
  if(!entries.length){ show msg; hide canvas; if(chart){chart.destroy();chart=null;} return; }
  hide msg; show canvas;
  const labels = entries.map(e=>e[0]);
  const data = entries.map(e=>e[1]);
  if(chart) chart.destroy();
  chart = new Chart(ctx, {
    type:'bar',
    data:{labels, datasets:[{label:'Records', data, backgroundColor:'#1f6fb2'}]},
    options:{
      indexAxis:'y',
      animation:false,
      responsive:true,
      maintainAspectRatio:false,
      layout:{padding:{right:48}},
      scales:{
        x:{beginAtZero:true, ticks:{precision:0}, grid:{color:'#e6ecf2'}},
        y:{grid:{display:false}, ticks:{font:{size:13}}}
      },
      plugins:{legend:{display:false}, tooltip:{...}}
    },
    plugins:[valueLabels]
  });
  // ensure longest on top
  const m = chart.getDatasetMeta(0).data;
  if (m.length>1 && m[0].y > m[m.length-1].y){
    chart.options.scales.y.reverse = true;
    chart.update('none');
  }
}
```

Wait: labels might be long — set y ticks to show full theme names; container height fixed maybe 380px, and canvas width full. Long theme labels take horizontal space; fine.

Chart container: fixed height div (e.g., 360px, but with 10 bars min 300). Use style height: 340px.

valueLabels plugin draws counts next to bar ends.

Note text under chart: "How this is computed: each matching record contributes one count for each theme it lists, so a record with several themes is counted once for each. Only the 10 most frequent themes among the matching records are shown; records with no recorded theme do not appear in this chart."

Showing line: `Showing X of Y records` where Y = ALL.length.

Update function ties it all: matches = currentMatches(); renderChart; sortRows; renderRows; showing text; filter description.

Reset: set all controls to default then update.

Also chart title/heading: "Top 10 themes". 

Empty data edge: if ALL.length===0, subtitle shows 0 records etc., chart hidden, table shows "No records match these filters"? Better: if ALL empty show no-records message. Handle gracefully.

SDG dropdown populate from ALL: collect unique sdgs (String), sort numerically. Option value = the string. Label: `${n} – ${sdg_names[n]||''}`. sdg_names keys are strings like "16".

Mechanism dropdown from ALL unique sorted. Body dropdown unique sorted (filter non-empty).

Keyword box: input type search. All controls have labels.

Also "Any change updates everything below at once" — add 'input'/'change' listeners.

Accessibility labels via <label for>.

Now the "How this is computed" note near table too? Rule says near every chart or number. Add small note near showing line: "Counts are computed by filtering this file's records; nothing is estimated."

Now write the full HTML. Also table: newest first — the date column first. Column headers: Date, Body, Symbol, Text (first line). Style with proper widths.

Expanded row: full text verbatim with `white-space:pre-wrap`, plus themes/SDGs/affected persons as definition-ish lines, plus link again? Not needed.

Detail row structure:

```html
<tr class="detail" hidden><td colspan="4">
  <div class="detail-text">...</div>
  <dl>...</dl>
</td></tr>
```

Use divs.

Let me also handle: clicking row toggles aria-expanded maybe; keep simple with class 'open'.

Show more: maintain `matchedList` global and `shownCount`; on click append next 100.

One more requirement: "A line 'Showing X of Y records' plus a plain description of the active filters". Good.

Also test 2: choosing UPR shouldn't show treaty body rows — our filter handles.

Header area includes the file title? Use U.title in subtitle maybe. Subtitle: source, n, years. I'll include source name linked.

Write CSS:

```css
:root{--accent:#1f6fb2;}
*{box-sizing:border-box;}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:#f5f7fa;color:#1c2733;font-size:16px;line-height:1.5;}
.wrap{max-width:1100px;margin:0 auto;padding:24px 20px 60px;}
header{margin-bottom:20px;}
h1{font-size:26px;margin:0 0 6px;color:#123;}
.subtitle{margin:0;color:#4a5a6a;}
a{color:var(--accent);}
.card{background:#fff;border:1px solid #dfe6ee;border-radius:8px;padding:16px 20px;margin-bottom:20px;}
.filters{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end;}
.filters label{display:block;font-size:13px;color:#41566b;margin-bottom:4px;font-weight:600;}
.filters select,.filters input{font:inherit;padding:7px 8px;border:1px solid #c4cfd9;border-radius:5px;background:#fff;min-width:120px;}
.filters input[type=number]{width:100px;}
.filters input[type=search]{min-width:200px;flex:1;}
button{font:inherit;padding:8px 16px;border-radius:5px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer;}
button.secondary...
#showingLine{font-size:18px;font-weight:600;margin:...}
#filterDesc{color:#4a5a6a;margin-top:2px;}
.note{font-size:13px;color:#5a6a7a;margin-top:10px;}
.chart-box{height:360px;position:relative;}
table{width:100%;border-collapse:collapse;font-size:15px;}
th{ text-align:left; border-bottom:2px solid #d6dee7;padding:8px 10px;font-size:13px;text-transform:uppercase;letter-spacing:.03em;color:#41566b;}
td{border-bottom:1px solid #e6ecf2;padding:9px 10px;vertical-align:top;}
tr.rec{cursor:pointer;}
tr.rec:hover{background:#f0f6fb;}
tr.open{background:#eef5fb;}
tr.detail td{background:#f7fafd;border-left:4px solid var(--accent);}
.detail-text{white-space:pre-wrap;margin:0 0 10px;}
.meta{font-size:14px;color:#3c4c5c;}
.meta strong{...}
```

Table wrap with horizontal scroll if needed? "Works on a laptop screen without horizontal scrolling" — table max-width 1100 fine; text column flexible.

Now, one subtlety: the detail row `hidden` attribute vs class toggling. I'll toggle style.display.

Event: main tr click → toggle next sibling. Link click stopPropagation.

Also number inputs: `input type="number"` with min/max hints from data (placeholder min/max years).

Let me now also double check "Showing X of Y" X==Y on load — yes.

Note about only two types: mention in subtitle: "recommendations and concerns/observations only". Also if some records were excluded, could note "of N paragraphs in the file, M are recommendations or concerns/observations". Nice honesty touch: if U.records.length !== ALL.length, add note. I'll include: subtitle line plus small note "Only records of type “Recommendations” or “Concerns/Observations” are included (M of N in the file)."

Write final code. Estimate ~420 lines. Good.

valueLabels plugin:

```js
const valueLabels = {
  id:'valueLabels',
  afterDatasetsDraw(c){
    const ctx=c.ctx, meta=c.getDatasetMeta(0);
    ctx.save();
    ctx.font='13px sans-serif';
    ctx.fillStyle='#1c2733';
    ctx.textAlign='left';
    ctx.textBaseline='middle';
    meta.data.forEach((bar,i)=>{
      ctx.fillText(c.data.datasets[0].data[i], bar.x+6, bar.y);
    });
    ctx.restore();
  }
};
```

Longest-on-top check: after chart creation with animation:false, meta data positions should be computed. But if canvas hidden (display:none) at creation... I ensure canvas visible before creating. Also responsive resize might re-layout but order stays.

Edge: if only 1 theme, skip check.

One more: canvas parent height fixed → maintainAspectRatio false.

Table "Show more" button styled secondary. Also a line under table: "Showing first Z of X matching records" maybe. Add small note.

Let me now write everything out.

Also date column: also show year? date includes year. Fine.

Filter desc when only keyword: 'keyword: "torture"'. Use quotes. Example in plan: "Treaty bodies · 2015–2020 · keyword: torture". I'll match that style: no quotes, `keyword: torture`.

SDG desc: `SDG 16` or include name? "SDG 16: Peace, justice and strong institutions" is nice. Keep short: "SDG 16". I'll include name — helpful. Keep "SDG 16 – Peace, justice and strong institutions"? Just do `SDG 16`.

Body desc: body name.

Mechanism: mechanism name.

Years: if y1&&y2 `${y1}–${y2}`; y1 only: `${y1} onwards`; y2 only: `up to ${y2}`.

Now write it. Also ensure `esc()` used for all dynamic text.

For SDG display in expanded row: `16 – Peace, justice and strong institutions` using sdg_names. Sort numerically.

affected_persons: label "Affected persons". If empty → "none recorded"? Plan only specifies for themes/sdgs. I'll show 'none recorded' for consistency.

Full code:

I'll write the script as an IIFE. Elements referenced by id.

Also handle U.sdg_names possibly undefined.

Let me count lines mentally — fine.

Edge: `Math.min(...yearsAll)` with big arrays could blow stack? Spread with e.g. 50k args is risky. Use reduce. ALL could be tens of thousands of records. Use reduce for min/max. Also rendering 100 rows at a time is fine.

Sorting large array each update: fine.

Chart recreation each keystroke of keyword: fine with animation off.

Debounce keyword input? Not required; direct is fine.

Write final answer: 3 short sentences before code block, nothing after.

Double-check doc_url linking: `<a href="${escAttr(r.doc_url)}" target="_blank" rel="noopener">`. esc for attribute — use esc (handles quotes).

Now write.