I'm working out a per-year chart of records for the overview, since FIG.02 already breaks records down by mechanism. I'm leaning toward a new figure of recommendations and observations per year, either a single total or stacked by type.

Next I'm stacking the new chart by type, using red for recommendations, dark grey for concerns and observations, and light grey for everything else. I'll add the figure after the FIG.02 block in the HTML and declare a ch3 variable in the JS, so render1 can destroy and recreate it.

I'm making sure the new chart gets destroyed and rebuilt in render1, and that its empty-state element is shown when there's no data and the chart box is hidden. I also need to guard the year list in case it comes back null when there are no records.

