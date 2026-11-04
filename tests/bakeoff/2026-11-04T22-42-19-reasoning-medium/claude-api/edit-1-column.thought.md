I'm adding a Year column that sorts the table by year, with the year sort falling back to date, then body and paragraph. That means a Year header button after Date, a year cell in each row, bumping the detail row's colspan from 6 to 7, and a new sortKey in the state to switch between date and year sorting.

Next I'm changing the sort so it can run by year as well as date, using a sortKey in the state. The header button and the click handlers need to switch between the two, and the sort comparator gets a year check ahead of the date comparison.

Now I'm finding the table row and the detail row so I can add the year cell and bump the colspan. The row markup has a date cell followed by a body cell, and the detail row's colspan is 6.

