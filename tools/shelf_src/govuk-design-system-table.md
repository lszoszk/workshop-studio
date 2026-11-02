---
id: govuk-design-system-table
title: "GOV.UK Design System: Table component (captions, headers, numbers, large tables)"
publisher: "GOV.UK Design System (Government Digital Service)"
url: https://design-system.service.gov.uk/components/table/
licence: OGL-3.0
licence_url: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
retrieved: 2026-11-02
kind: excerpt
topics: [tables, accessibility, html, design-system, numbers]
---
> Excerpt from "Table", GOV.UK Design System (Government Digital Service), https://design-system.service.gov.uk/components/table/. Crown copyright. Retrieved 2026-11-02.
> Contains public sector information licensed under the Open Government Licence v3.0.
> Trimmed; "[…]" marks cuts. Not an official version.
> The HTML example is Design System code, released separately under the MIT licence (notice at the end of this page). The Nunjucks macro variants and live-example links of the original are omitted.

Use the table component to make information easier to compare and scan for users.

[…]

```
<table class="govuk-table">
  <caption class="govuk-table__caption govuk-table__caption--m">Dates and amounts</caption>
  <thead class="govuk-table__head">
    <tr class="govuk-table__row">
      <th scope="col" class="govuk-table__header">Date</th>
      <th scope="col" class="govuk-table__header">Amount</th>
    </tr>
  </thead>
  <tbody class="govuk-table__body">
    <tr class="govuk-table__row">
      <th scope="row" class="govuk-table__header">First 6 weeks</th>
      <td class="govuk-table__cell">£109.80 per week</td>
    </tr>
    <tr class="govuk-table__row">
      <th scope="row" class="govuk-table__header">Next 33 weeks</th>
      <td class="govuk-table__cell">£109.80 per week</td>
    </tr>
    <tr class="govuk-table__row">
      <th scope="row" class="govuk-table__header">Total estimated pay</th>
      <td class="govuk-table__cell">£4,282.20</td>
    </tr>
  </tbody>
</table>
```

[…]

## When to use this component

Use the table component to let users compare information in rows and columns.

## When not to use this component

Never use the table component to layout content on a page. Instead, use the grid system.

## How it works

### Table captions

Use the `<caption>` element to describe a table in the same way you would use a heading. A caption helps users find, navigate and understand tables.

There are other styling options for table captions. You can use `govuk-table__caption--s`, `govuk-table__caption--m`, `govuk-table__caption--l` and `govuk-table__caption--xl` classes to make them larger or smaller from the default.

[…]

### Table headers

Use table headers to tell users what the rows and columns represent. Use the `scope` attribute to help users of assistive technology distinguish between row and column headers.

[…]

## Numbers in a table

When comparing columns of numbers, align the numbers to the right in table cells.

[…]

## Tables with a lot of data

If possible, you should aim to have less data in your tables. If you have a lot of data, try to organise it into multiple tables or multiple pages.

If you cannot split your data, you can use the CSS class `govuk-table--small-text-until-tablet`. This class reduces the size of the text on small screens so large amounts of data has more empty space around it. This makes it easier to visually differentiate between each piece of data when read on small screens.

The CSS class `govuk-table--small-text-until-tablet` is only available in version 5.2 of GOV.UK Frontend and later.

---

## Licence notice for the code example (MIT)

MIT License

Copyright (c) 2017 Crown Copyright (Government Digital Service)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
