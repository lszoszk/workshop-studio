---
id: uk-af-tables
title: "Data visualisation: tables (layout, headers, titles, HTML markup)"
publisher: "UK Government Analysis Function"
url: https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/
licence: OGL-3.0
licence_url: https://analysisfunction.civilservice.gov.uk/terms-of-use/
retrieved: 2026-11-02
kind: excerpt
topics: [dataviz, tables, accessibility, numbers]
---
> Excerpt from "Data visualisation: tables", Government Analysis Function, Crown copyright, https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/. Retrieved 2026-11-02.
> Contains public sector information licensed under the Open Government Licence v3.0. Text only; images on the source site are not covered by the licence.
> Trimmed; "[…]" marks cuts. Original headings kept. Not an official version.

## Using tables in publications

Demonstration tables are useful when:

- you want users to compare values
- you want to include values and measures such as percentages or indices
- you want to include summary statistics such as averages or totals
- you need to show values of very different sizes in the same display, for example values in the tens and values in the millions

Charts should be used when you want to show patterns, trends and relationships.

Reference tables should be used when you want to supply large amounts of data for further analysis.

[…]

### Comparing numbers

To help the reader make comparisons:

- present the numbers close together
- present the numbers in columns, not rows
- use the same level of precision within each column
- use commas to separate thousands
- right align the figures and the column headings
- start numbers of less than one with a zero, not a point

[…]

### Rounding

Presenting too much detail can make things harder for users. Rounding numbers makes them easier to read and remember.

For example, in Figure 1.1, headcount numbers are rounded to the nearest ten.

The extent of rounding will depend on the intended use. A journalist may be happy to report that the population of the UK is 66 million, or that the population has changed from 64.1 million to 66.4 million. An analyst performing further calculations will want to work with more precise figures.

Rounding does reduce precision. This usually means that the reported totals no longer equal the sum of the component parts.

Making a decision on rounding can be difficult when the values show a variety of units. Consider rounding to a fixed number of significant figures or effective digits.

[…]

### Ordering categories

Ordering the categories in a table can make it easier for users to see patterns and groups in the data.

For some categorical variables, like month of the year or age group, there is a natural order for presentation. Other variables may have harmonised ordering, such as regions of the UK.

Use natural or harmonised principles whenever possible. An appropriate order may also be obvious from knowledge of the subject matter. For example in Figure 1.1 in this guidance we order Civil Service grades by seniority, it would not make sense to order them alphabetically.

[…]

### Titles

All tables should have a title.

Ideally, they should have a headline title which states the message you’re trying to get across and a statistical subtitle stating what the data is and the geography and time period it relates to.

You do not have to have a headline title, but we recommend them as they help users see the messages in the data.

If you have a mix of charts and tables in your publication, it may be useful to use ‘Figure n’ in the titles instead of numbering tables and charts separately.

### Column headers, row labels and merged cells

Column headings and row labels are important parts of tables. Column headings should describe the data in each column. Units should also be described, unless all the data in the table has the same units. In this case information on units can be given in the table title.

It is also very important that tables published in HTML have properly ‘marked-up’ column headers and row labels. This mark-up allows screen reader software to understand the table layout.

This mark-up also allows HTML tables to have merged cells in the table layout.

But note: merged cells in tables published in spreadsheets and text documents are not accessible. This is because the document software does not yet have the more complex mark-up this type of layout needs. Also, be aware that some HTML table builder tools may not allow you to use merged cells.

The ‘Publication’ section of this guidance has more information on what table mark-up is and how to do it.

### Footnotes

Tables can have footnotes but they should be avoided whenever possible as jumping from one section of text to another can be confusing. It is better to put the information at the point of need.

If you do have to use footnotes, it is best practice to place them in the title, column headings or row labels. Avoid placing them in cells with data, this affects the alignment of the figures and can make the table more difficult to understand.

### Source

It is best practice to give the source of the data in the table and hyperlink to it. This information should go underneath the table.

Source information should be provided in the following format: [publication, survey or other source of data] from the [organisation].

For example: Source: Childcare and early years survey of parents from the Department for Education.

If the table uses more than one source you should list them all.

If all the tables and charts in your publication have the same source, you can state this somewhere else in the publication. You do not need to repeat the source information under every figure.

[…]

### Shading

Shading should be avoided in tables whenever possible.

If you need to use shading you must not use it as the only way to communicate a message. Using colour like this will fail accessibility success criterion 1.4.1 use of colour.

You must also ensure the colour contrast ratio between the shaded background and the font colour is 3 to 1 or higher. More information on the use of colour is in our colours guidance.

### Gridlines

Do not over use gridlines. They can help a user read data from a table, but if they are too dark or there are too many of them they can make a table hard to read.

If you publish in HTML you may not have much control over the gridlines shown on a table. If you publish your table in a text document you will.

Generally, it is a good idea to mark out the line under the header row and the lines above and below any summary statistics.

[…]

### Using HTML

We advise that all publications on public sector websites should be in HTML. Demonstration tables within these publications should be built into the HTML code of the webpage. Images of tables should never be used as they fail accessibility success criterion 1.4.5 images of text.

When tables are published in HTML they need to be ‘marked-up’. This means using HTML code that presents the data as a table. This code tells screen reader software there is a table, how many columns and rows it has, where the edge of the table is and how the row labels, column headers and data cells are laid out.

Improving your understanding of how screen readers deal with HTML tables and watching this video of a screen reader accessing a table may help you understand how tables are marked-up in HTML.
