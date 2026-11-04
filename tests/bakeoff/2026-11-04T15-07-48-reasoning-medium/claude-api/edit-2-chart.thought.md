I'm weighing where a new per-year total chart should go, either after FIG.02 or in front of it. The plan had said nothing else on this tab, but the user is asking for it, so I'm considering whether to keep it as a single total or split it by type.

I'm settling on stacking the new chart by type, since the "recommendations and observations" label points that way, with red for recommendations and greys for the rest. Then I'll wire up the HTML after FIG.02, a shared chart variable, and a destroy-then-recreate step in the overview render.

Still wiring the new chart's code into the existing chart script. It needs to be created after the second chart and torn down alongside it, with its title and visibility handled in the same places.

Next I'm adding the new chart's visibility toggle, so its card hides when there's no data, the same way the other two do. I'm also picking the colour for each type: red for recommendations, and greys for the other categories.

