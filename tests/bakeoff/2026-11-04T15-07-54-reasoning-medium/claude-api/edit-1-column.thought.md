I'm adding a sortable Year column, which means introducing a sort key in state so the table can sort by either date or year. Year sorting will fall back to date, body, and paragraph, and clicking the Year header will toggle the direction. The changes touch the renderer, the sort function, the state initialization, and the detail row's colspan.

Still wiring up the sort logic and header...

I'm drafting the caption change next, so the caption can show which key the table is sorted by, not just the direction.

Next I'm adding a Year column to the row template after Date, and I'm updating the detail row's colspan to match the extra column.

Next I'm making the header click handler toggle the sort direction when Year is already active, and otherwise switch to the year key, and I'm also excluding the Year button from the row-click handler so it doesn't open a record.

