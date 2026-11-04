I'm adding a sortable Year column, so I'm planning a new sort state keyed by date or year, with year sorting falling back to date, then body, paragraph, and order. The edits are to the sorting function, the header row, the row cells, and the colspan change, plus wiring up the click handler.

I'm wrapping up the caption, so with year sorting it should read "by year, newest first." Clicking the date header will set the sort key back to date and toggle direction, or default to descending. Next I'm rewriting the sort function, adding a sort key variable ahead of it, since the function's own search lines have to match the existing code exactly.

Still writing the header and row edits...

I'm now setting the caption to reflect the year sort, and the date header's click handler is being updated to reset the sort key and toggle direction.

