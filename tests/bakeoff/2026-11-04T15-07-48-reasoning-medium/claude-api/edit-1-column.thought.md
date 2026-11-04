I'm adding a sortable Year column next to Date, which means introducing a sort key state that switches between date and year. I'm also bumping the empty-row colspan from 6 to 7 and starting on the table header markup.

I'm working out the header edit now: the Year button goes right before the Body column header, placed after Date. Then I'll look at a year-based sort that uses the date comparison as a tie-break.

I'm now updating the sort logic so the year key orders by year first, with the existing date comparison as a tie-breaker. I'm also changing the caption text to reflect whether the table is sorting by year or by date.

Still working on the sort handlers: the Date and Year buttons need to switch the sort key and toggle direction. I'm also updating the row cell to add a Year cell next to the date.

I'm changing the colspan on the empty-row cell from 6 to 7 and adding a sort-key field to the state that defaults to date. I'm also reviewing how the Year column's header alignment should be set.

