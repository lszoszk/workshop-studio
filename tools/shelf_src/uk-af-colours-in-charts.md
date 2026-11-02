---
id: uk-af-colours-in-charts
title: "Data visualisation: colours in charts (palette, contrast, bar charts)"
publisher: "UK Government Analysis Function"
url: https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours-in-charts/
licence: OGL-3.0
licence_url: https://analysisfunction.civilservice.gov.uk/terms-of-use/
retrieved: 2026-11-02
kind: excerpt
topics: [dataviz, colour, accessibility, contrast, palette]
---
> Excerpt from "Data visualisation: colours in charts", Government Analysis Function, Crown copyright, https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-colours-in-charts/. Retrieved 2026-11-02.
> Contains public sector information licensed under the Open Government Licence v3.0. Text only; images on the source site are not covered by the licence.
> Trimmed; "[…]" marks cuts. Original headings kept. Not an official version.

### Limit the number of colours you use

Limiting the number of colours you use in a chart makes them stand out. This is useful because colour helps the brain quickly identify differences. Using lots of colours makes this harder.

Think carefully before you introduce additional colours into a graph. Ask yourself:

- Do you really need the colours?
- Do they make your message clearer?

You should only use different colours when they show helpful differences in the data. When people look at a chart with lots of colours, they try to work out what those different colours mean. If your colours suggest meanings that are not there the user will waste time and effort trying to understand them.

When you have categorical data that cannot be grouped, use a single colour. The user is much more likely to compare the bars when they look alike than when they look different. See the first example in the Office for National Statistics’ (ONS) guidance on using colour in bar charts.

### Use colour consistently

If you have a series of charts, assign the same colour to the same variable in each chart.

If you change the way you use colours in a series of graphs it becomes harder for users to follow the story. It can also cause them to mistake one data series for another, especially if a user is skim reading. See guidance from ONS on using colour to connect information.

[…]

### Use a plain background

Never use an image as a background. This can make charts difficult to see. Charts that use an image as a background are also likely to fail the accessibility legislation.

We recommend using white as a background colour. All our suggested colour palettes are based on this.

There are some accessibility issues with using white as a background colour. Some users may find a white background difficult to look at because of glare or the high contrast of colours against it. On the other hand, other users prefer a white background because they need the high level of contrast it provides.

A perfect solution would be to have data visualisations that can be fully customised to meet specific user needs. As this is not possible at the moment we recommend a white background because it provides a helpful ‘anchor’ in general.

### Consider colour contrast ratios

Colour contrast ratios are a measure of difference in brightness between two colours. Colour contrast ratios range between 1 to 1 (white on white) and 21 to 1 (black on white).

More information on how to calculate colour contrast ratios from the Accessibility Developer Guide.

The Web Content Accessibility Guidelines (WCAG) which the UK accessibility legislation aligns to, require a 3 to 1 ratio for graphical elements and 4.5 to 1 ratio for text.

[…]

### Consider low vision and colour blindness

#### Low vision

When we talk about the accessibility of colours in data visualisations we tend to concentrate on colour blindness.

But we should also consider people with low vision. This can be caused by conditions like glaucoma and cataracts.

You can find out more about the difference between low vision and colour blindness in this article on visual disabilities.

Keeping a 3 to 1 contrast ratio between adjacent colours (as set out in success criterion 1.4.11) is important for people with low vision.

#### Colour blindness

Colour blindness affects around 8% of men and 0.5% women. It can come in many different forms. You can find more information about types of colour blindness in ONS guidance on using colours.

The section on ‘Using other colour palettes’ gives details of some useful tools for checking palettes for colour blindness issues.

We have checked our suggested colour palettes for different types of colour blindness. Guidance related to this is available in each section.

### Consider your colours in greyscale

It is a good idea to check your charts can be understood in greyscale.

This is because:

- it is a good way to check if your chart relies on colour to be understood
- there is still a need for some users to print in black and white
- seeing in greyscale is a specific type of colour blindness

Check how your charts look by using print preview and selecting ‘greyscale’ or ‘black and white’.

We have checked our suggested colour palettes to see how they look in greyscale. Guidance related to this is available in each section.

### Do not rely on colour alone

Colour should not be used as the only way to communicate information. This is stated in accessibility success criterion 1.4.1.

See the section on accessibility legislation for more information.

[…]

### Palette table

| Colour | Hex code | RGB code | CYMK code | Example of colour |
|---|---|---|---|---|
| Dark blue | #12436D | (18, 67, 109) | (83, 39, 0, 57) |  |
| Turquoise | #28A197 | (40, 161, 151) | (75, 0, 6, 37) |  |
| Dark pink | #801650 | (128, 22, 80) | (0, 83, 38, 50) |  |
| Orange | #F46A25 | (244, 106, 37) | (0, 57, 85, 4) |  |
| Dark grey | #3D3D3D | (61, 61, 61) | (0, 0, 0, 76) |  |
| Light purple | #A285D1 | (162, 133, 209) | (22, 36, 0, 18) |  |

[…]

### Information about these colours

- All colours have a contrast ratio of at least 3 to 1 against white.
- When used in the order presented in the list, all adjacent colours have a contrast ratio of at least 3 to 1.
- All colours have passed our checks for colour blindness – see the section on ‘Using other colour palettes’ for more information.
- When used in the order presented in the list, all adjacent colours appear distinct in greyscale.

### Ideally, use just the first four

We recommend a limit of four categories as best practice for basic data visualisations. More than four series can make a chart too cluttered. This is why all our examples of using the categorical colour palette only use four series.

The dark grey and light purple have been added to this palette due to demand for extra colours. But these should only be used when essential.

[…]

#### Simple bar charts

Use a single colour for all bars in vertical column charts and horizontal bar charts where there are no groups to highlight. We recommend using the first colour in the palette. We call this colour ‘dark blue’. We recommend dark blue because it:

- has the highest contrast ratio with a white background out of the first four main colours in the palette
- works for different types of colour blindness
- works in greyscale

The gap between the bars should be slightly narrower than the width of a single bar. Unless you are presenting a histogram. Histograms should have no gaps between bars.

Remember: all charts should have a plain text alternative. This can be a text description or a table of data, ideally in the body text of a page.
