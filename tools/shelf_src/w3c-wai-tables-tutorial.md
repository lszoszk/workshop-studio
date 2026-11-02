---
id: w3c-wai-tables-tutorial
title: "W3C WAI tutorial: Tables (header cells, scope, headers and id, captions)"
publisher: "W3C Web Accessibility Initiative (WAI)"
url: https://www.w3.org/WAI/tutorials/tables/
licence: W3C-Document
licence_url: https://www.w3.org/WAI/about/using-wai-material/
retrieved: 2026-11-02
kind: excerpt
topics: [accessibility, tables, html, screen-reader, wcag]
---
> Complete main text of "Tables Concepts", Web Accessibility Tutorials, W3C Web Accessibility Initiative (WAI). Original: https://www.w3.org/WAI/tutorials/tables/
> Copyright © 2026 World Wide Web Consortium. W3C® liability, trademark and document use rules apply (W3C Document License, https://www.w3.org/copyright/document-license-2023/; see https://www.w3.org/WAI/about/using-wai-material/). Retrieved 2026-11-02.
> Verbatim; navigation and feedback links removed; list markup normalised.

Data tables are used to organize data with a logical relationship in grids. Accessible tables need HTML markup that indicates header cells and data cells and defines their relationship. Assistive technologies use this information to provide context to users.

Header cells must be marked up with `<th>`, and data cells with `<td>` to make tables accessible. For more complex tables, explicit associations may be needed using `scope`, `id`, and `headers` attributes.

This tutorial shows you how to apply appropriate structural markup to tables. It includes the following pages:

- **Tables with one header** for rows or columns: For tables with content that is easy to distinguish, mark up header cells with `<th>` and data cells with `<td>` elements.

- **Tables with two headers** have a simple row header and a simple column header: For tables with unclear header directions, define the direction of each header by setting the `scope` attribute to `col` or `row`.

- **Tables with irregular headers** have header cells that span multiple columns and/or rows: For these tables, define column and row groups and set the range of the header cells using the `colgroup` and `rowgroup` values of the scope attribute.

- **Tables with multi-level headers** have multiple header cells associated per data cell: For tables that are so complex that header cells can’t be associated in a strictly horizontal or vertical way, use `id` and `headers` attributes to associate header and data cells explicitly.

- **Caption & Summary:** A caption identifies the overall topic of a table and is useful in most situations. A summary provides orientation or navigation hints in complex tables.

Some document formats other than HTML, such as PDF, provide similar mechanisms to markup table structures. Word processing applications may also provide mechanisms to markup tables. Tables markup is often lost when converting from one format to another, though some programs may provide functionality to assist converting table markup.

Many web authoring tools and content management systems (CMS) provide functions to define header cells during table creation without having to edit the code manually.

This tutorial provides guidance for creating tables used to display data in a grid. This tutorial does not apply to tables used for layout. As a general rule, tables aren’t meant to be used for layout purposes. Instead, a best practice is to use Cascading Style Sheets (CSS) for visual presentation.

## Why is this important?

Tables without structural markup to differentiate and properly link between header and data cells, create accessibility barriers. Relying on visual cues alone is not sufficient to create an accessible table. With structural markup, headers and data cells can be programmatically determined by software, which means that:

- **People using screen readers** can have the row and column headers read aloud as they navigate through the table. Screen readers speak one cell at a time and reference the associated header cells, so the reader doesn’t lose context.

- **Some people use alternative ways to render the data**, for example by using custom stylesheets to display header cells more prominently. Techniques like this enable them to change text size and colors and display the information as lists rather than grids. The table code needs to be properly structured to allow alternative renderings.

These tutorials provide best-practice guidance on implementing accessibility in different situations. This page combined the following WCAG success criteria and techniques from different conformance levels:

**Success Criteria:**

- **1.3.1** Info and Relationships (Level A)
