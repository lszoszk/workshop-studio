The dataset doesn't have a clean document-type field, so the closest options are mechanism, body, and type. Deriving the kind from the symbol is possible, since treaty body symbols carry "/CO/" for concluding observations and UPR symbols follow an "A/HRC" pattern, but that's heuristic. The more honest route is to compute a "Document kind" field in code, mapping treaty bodies to concluding observations.

Now I'm mapping out a derived "Document kind" field: treaty-body concluding observations keyed off "/CO/" in the symbol, UPR reports, and Special Procedures reports. I'll place it in the second filter heading so the filters stay at three, then plan the edits across the HTML, the record parser, the state object, the matcher, the filter descriptions, the static fill, the controls sync, the change handler, and clearAll.

I'm going through the remaining edit points: the select addition after the type field, the parser line that picks up the derived kind, the new state key, the matcher and chip cleanup, and the static fill. The rest is syncing the controls, the change handler, and clearAll.

Still wiring the derived kind through the remaining spots: syncing the controls, the change handler, and clearing it in clearAll.

