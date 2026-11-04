Build the full app per plan. Single HTML file, four tabs, left rail filters, charts, table, checks, export. Keep under ~1500 lines. Let me write carefully.

Key data: WORKSHOP_DATA.uhri. Compute everything.

Structure:
- header
- rail with filters (chips, three collapsible headings)
- tabs 01-04

Filters state: keyword, mechanism, body, type, state (UPR States), yearFrom, yearTo, sdg, themes (from chart click chips).

Tabs: only rail filters shown on tabs 1-2; on 3-4 rail shows number/bar/chips only.

Implement paragraph extraction, State extraction, checks, seeded sample.

Credits line: sources consulted include Analysis Function guidance — I used their chart/table conventions; add Credits line.

Let me write the code.