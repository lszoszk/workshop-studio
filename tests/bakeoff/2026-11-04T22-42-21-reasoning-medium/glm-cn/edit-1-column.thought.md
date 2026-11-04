Add a Year column after Date, sortable via clicking header. Update sortSet to support sort key. Keep date header toggle too. Simplest: add a "Year" header button toggling sort by year, and Date keeps its toggle. Implement sortKey = "date" | "year".

Edits:
1. Table header: add Year th.
2. sortSet: use sortKey.
3. Add yearSort button listener and state.
4. renderTable rows: add year cell, colspan for detail rows is 7 already? Detail row colspan=6 must become 7. Also empty-row colspan 6→7.
5. Caption mention.