I'm reworking the existing app so the user can correct a label flagged as wrong or arguable in the random-sample check on tab 03. I'll keep UN labels and never overwrite them silently, and I'm laying out the requirements before I write the full file.

I'm settling the CSV details: the requested columns are symbol, paragraph, UN labels, my labels and my mark, and since symbol plus paragraph isn't always unique, I'm adding a record id column too. On load I'll match by id first, then by a unique symbol and paragraph pair, and show a report of anything that doesn't match. I'm also starting to sketch the state for the corrections.

I'm weighing how to store the corrections: keeping the removed and added labels relative to the UN's set, or just the final set of my labels plus the verdict. A correction counts as a record where my labels differ from the UN's, and I'm still deciding whether the count should be per record or per individual label change.

I'm now deciding how a verdict should persist: rather than resetting per sample, I'm considering keeping one global mark per record so the CSV can restore it, and the sample tally would count those marks.

I'm checking how the verdict marks should persist, since the CSV's "my mark" column seems to belong with the corrections. The verdicts that call for a correction are "Doesn't fit" and "Unsure", and I'm working out whether a mark without any label change should be exported too.

I'm deciding whether the CSV should also carry records that only have a verdict and no label change, since the "my mark" column only makes sense if a mark can exist on its own. I'm weighing whether to export records with a "no" or "un" mark even when the labels are untouched, so the verdict survives a reload.

I'm deciding to keep records that have a label change or any verdict in the CSV, since marks alone are worth restoring, and I'll state that rule on screen. For undo, I'm planning a per-record button that clears that record's corrections, plus a way to revert individual labels.

I'm going to lay out a "Your corrections" panel on tab 03, below the sample, with an Undo on each entry and an Undo all option, since the Check tab already has a lot of buttons. The header switch, CSV download and load are the other new controls I'm adding.

I'm settling where the list of corrections should live: a collapsed "Your corrections" section on tab 03 below the sample, with a toggle to show the per-record Undo list, a CSV download, a CSV load, and Undo all. I'm weighing whether to mention the same controls on tab 04, since that's where exports usually sit.

I'm settling on a single header switch with two states, UN labels and with my corrections, rather than adding two more buttons to an already busy rail. The corrections management stays on tab 03, and I'm weighing whether the list belongs there too, since it's about trust.

I'm settling the header switch as a single toggle between "UN labels" and "with my corrections", so there's one click target rather than two buttons. I'll default it to "with my corrections", and when a correction is made I'm leaning toward switching to that mode automatically, since a correction that doesn't show up anywhere would be confusing, even though that flip could also surprise the user.

I'm deciding the header switch will track the effective labels, so the rest of the app reads from one place. I'll keep the UN's original themes untouched and store my version separately, then have the filters, chart, table and checks all pull from whichever set is active.

I'm working out how the corrections should flow into the summary, the sample cards and the detail rows, and whether the "Not labelled" check should count from the effective labels or from the UN's original file.

I'm settling the add-label control: a select listing every UN theme label in the data, minus the ones already on the record, with an Add button next to it. Since the list is limited to existing labels, a select is simpler than a free-text field, though with around 90 entries it may need to be long.

I'm adding a check that the UN's labels stay untouched by comparing them against a snapshot taken at load, and a check that every correction uses a label that exists in the file.

I'm working out the data model for the corrections: one map keeps any labels I've set that differ from the UN's, and a separate map keeps each record's verdict, so the UN's own themes are never touched.

Next I'm defining the helpers for the corrections: each record's UN themes stay as they are, and the effective themes come from my version only when the mode is on and that record has one. A diff helper will list what I removed and added against the UN set, and setting a record's labels will clear the entry when it matches the UN exactly. I'll tally the corrected labels from those diffs, and the remove and add actions will each build on the current set.

I'm switching the plan to store corrections as two lists per record: labels removed from the UN's set and labels added to it. The effective labels are then the UN's labels minus the removals plus the additions, so undoing a single change just takes it out of its list. For loading a CSV, I'll derive those two lists by comparing the saved labels against the UN's set, and reject any label that doesn't exist in the data.

I'm deciding that a correction made on a record will also flip the header switch to "with my corrections", so the change shows up immediately. The sample is currently drawn from the filtered set, and I'm checking whether a correction that changes which records match a theme filter should reset the sample or keep it.

I'm noting that a correction should re-render the view without clearing the sample, so the ten drawn records stay put, and I'm checking that render only redraws the charts when the overview tab is active.

I'm now working out how the corrections show on record detail: kept UN labels stay normal, removed ones get a struck-through style, and labels I've added get a distinct red-bordered tag, and I'm weighing how the "corrected" note should sit alongside them.

I'm putting the corrections in the record detail and the table rows as well: kept UN labels stay normal, removed ones are struck through, added ones get a red-bordered tag, and a small "corrected by you" marker shows on rows in the "with my corrections" mode.

I'm now deciding how the corrections show on the other places where a record appears: the table rows get a small "corrected by you" marker in the mine mode, and the sample cards keep the full editor. The theme tables on tab 01 only count records, so they stay as they are.

I'm wiring the figure captions to show whether the labels are the UN's own or carry my n corrections on m records, and I'll add that line to the source text under all three figures. The sample cards will reuse the same theme rendering with editing enabled, so each card keeps the UN label visible alongside my changes.

I'm deciding that in "UN labels" mode the cards, the record detail and the table rows will show only the UN's own labels, with a one-line mono note explaining that my corrections are hidden. In "with my corrections" mode they show the struck-through and added tags. The card editor will follow the same switch, so what I see always matches the mode I'm in.

I'm deciding that in the card editor, each UN label gets a remove control, and a removed one shows struck-through with a restore control, while the editor always shows the diff so I can undo anything I've changed.

I'm making the card editor show only when a verdict is "no" or "un" or the record already has a correction, so "Fits" cards stay uncluttered. Each button and select will carry an accessible label, and the label names will go through the escaping helper before they reach the markup.

I'm deciding that the card's focus should go back to its open button after a label is removed or restored, so the keyboard position isn't lost, though I'm still weighing whether to focus the add select instead.

I'm making the verdict live in one global map keyed by record index, and I'm about to count the corrections across the sample so the header line and captions stay in step with it.

I'm deciding that the corrections list panel is collapsible, with a count and an expand button that sets aria-expanded. Each row will show the symbol, paragraph, UN labels, my labels in diff style, my mark, and an undo control. I'm still weighing whether undo should clear both the label changes and the mark together, or whether undoing only the labels should keep the mark.

I'm settling the corrections panel: a collapsible list with each record's symbol, paragraph, UN labels, my labels, mark and an undo control, plus buttons to download or load the CSV, undo everything and show the list, which keeps it out of the way until it's needed.

Next I'm sketching the CSV load path: a hidden file input behind a visible button, reading the file locally, then a small parser that handles quoted fields, embedded newlines and CRLF, and drops any leading comment lines before parsing.

I'm settling the CSV export format: a comment line naming the file, then a header with symbol, paragraph, UN labels, my labels, my mark and record id, with multiple labels joined by a pipe separator. The mark will be written as "Fits", "Doesn't fit", "Unsure" or left blank, and on load I'll split on that same separator and check each label against the data.

I'm settling the CSV load so that a file's entries replace the corrections on the same records while the rest are kept, and I'll report how many matched, were not found, or had labels missing from the data.

I'm matching each CSV row back to a record, first by its id, then by symbol and paragraph, and falling back to the UN labels if that is still ambiguous. Anything that can't be matched cleanly gets reported rather than applied. I also want to flag rows whose UN labels no longer agree with this file, since that would mean the export was made from a different build.

I'm settling how the CSV download and the load report work: the download writes only a header if there are corrections, and the load result goes into a persistent status region, since it needs to stay readable.

Now I'm writing the CSV parser and the load path for the corrections file.

I'm working out the theme counts over all records, using a map to tally each theme once per record, and then sorting the theme names alphabetically.

I'm setting up the state for the corrections: a flag for whether to show my corrections, a map of per-record label changes, and a map of marks. Then I'm defining helpers that return a record's UN labels, its effective labels with my changes applied, and a count of total changes.

I'm working out how the card editor will handle the corrections in memory: each record gets a small pair of lists for removed and added labels, and I'm checking that a label already in the UN set is restored rather than added twice.

Writing the edit helper for removing and restoring labels...

I'm writing the label-editing helper so that removing a UN label records it as removed and restoring it clears that removal, with the count of corrected labels updating in the header line.

I'm working out how the label helper treats the switch and the counts, starting with the theme filter, which should now read the effective labels rather than the raw UN ones.

I'm writing the label helper so that a UN label I remove is recorded as removed, and adding it back clears that removal, with the header count updating as I go.

I'm turning to the corrections panel's markup now, so that a label I've struck from a record shows as a struck-through tag beside the UN's own, with a screen-reader note saying it was removed.

I'm working out how the mine-mode details will show each record: the struck-through UN labels beside my added ones, with a note that the correction is hidden when UN labels are on. The row's first line will also get a small "corrected by you" tag wherever I've changed that record.

I'm updating the chart recount to use the effective labels, and adding checks that the UN's own labels stay unchanged from a snapshot, that every label used exists in the data, and that the counts follow the switch.

I'm checking the label totals now: the file's labels before my corrections, minus what I've removed, plus what I've added, should match what the view shows.

I'm wiring the sample cards up to the same correction editor, so a card shows a "corrected by you" tag when its record has changes and the editor opens with the UN labels and my edits side by side.

Next I'm building the corrections editor for each card: the UN labels show as chips, with removed ones struck through and a restore control, and my added labels get their own style and a remove control.

I'm wiring the card editor to the shared correction helpers, so the paragraph's labels show as chips that can be removed, restored or added to.

I'm wiring the verdict buttons so that clicking one sets or clears that record's mark, then re-rendering the cards and the corrections panel, since marks feed the CSV and the list even though they don't change the counts.

I'm putting together the verdict and the sample tally, keeping the count of judged themes against the sample size. Draws reset the sample and remove the verdict. After a correction, I'm marking my changes as active and re-rendering the view.

I'm laying out the corrections panel beneath the sample cards, and I'm making sure the renderers all run from one render pass so the seed input and the cards stay in step.

Writing the corrections panel markup: an intro note, buttons to show the list, download the CSV, load a CSV, and undo everything, plus a hidden file input and status regions.

I'm deciding that "Undo all" will clear only the label changes and leave my verdicts alone, using a two-step confirmation instead of a browser dialog.

I'm settling the corrections list: each row gets one "Undo" that clears both the label changes and the mark for that record, and "Undo all" will clear the label changes and the marks together, guarded by a two-step confirmation.

I'm writing the corrections list, with a helper that gathers every record that has a label change or a mark, sorted by paragraph number.

I'm writing the CSV export and the loader for the corrections file, starting with the header and a parser that handles quoted fields.

Still writing the CSV parser, handling quoted fields and line endings, and filtering out blank rows.

I'm stripping the leading comment lines off the CSV first, using a regex that handles both line-ending styles, and then I'll look for the header row and match the column names to find the indices I need.

I'm working out the CSV loader now: stripping the leading comment lines, finding the header row, and matching the columns by name before applying each row's label changes and marks.

I'm working out the CSV loader's record matching: each row first looks for its record ID, and if that fails, falls back to matching on symbol and paragraph number, narrowing by the UN labels when several records share them.

I'm working out how each record's label changes get saved: the UN labels that aren't in my list count as removed, my labels not already in the UN set count as added, and the record is only kept in the corrections map if either set is non-empty.

I'm finishing the CSV loader's apply step: each record's file labels are compared against its UN labels, and the mark is set or cleared to match the file, with a status message reporting how many rows were restored, skipped, or had unknown labels.

I'm adding the export's extra columns for the labels as shown, the UN's own labels, and whether each row was corrected by hand, and I'm updating the CSV comment line to say which labels it carries. Next, the summary gets a line that states which labelling mode is active, using the effective labels from the theme stats, and the method text gets a paragraph on corrections. Finally I'm checking that render() calls the rail, overview, records and cards renderers in that order.

I'm putting the correction line between the heading and the meta line, and styling it with a small mono font and a bordered toggle button.

Still writing the toggle's styles, with the active state in red and the switch track drawn with a pseudo-element.

I'm adding the mine-tag and struck-label styles, plus the small tag for corrected records and the remove button next to each chip.

I'm finishing the corrections styles: the editor block gets a top border and spacing, and its select is sized to fit. I'm also wiring the theme tags so that, in the diff view, a corrected record's Themes entry gets a small marker.

I'm working out how the corrections export and the sample cards fit together, and the CSV loader's details come first.

I'm building the sample cards now, and each one shows a correction tag when that record has label changes, along with its verdict and the UN labels beside it.

I'm wiring up the sample card's editor so that the chips and the controls for adding or undoing a label appear when a verdict is "Doesn't fit" or "Unsure", and otherwise a hint tells the user to pick one of those verdicts first.

I'm wiring the sample click handler so the draw, seed, open, verdict and label actions each route to their own branch, with focus put back on the control that was used.

I'm wiring the list-remove and restore handlers, and I'm making the add action read the selected label first and report an error when none is picked.

I'm wiring the list-remove and restore handlers next, and the add action reads the selected label first, reporting an error if none is picked.

I'm now writing the corrections panel's render function, which sets the intro text, enables or disables the export and undo-all buttons based on whether there are any corrections, and then fills in the list.

I'm adding the undo-all confirmation reset to the render, plus the per-row undo that clears both the label changes and the mark. The list's undo will skip the forced labelling-mode switch, since it isn't needed there.

Next I'm finishing the undo-all and undo handlers, and the list's undo will set the labelling mode as-is rather than forcing it. I'm also wiring the load and switch buttons, plus a short label for the chosen mode in the description.

Still writing the summary code, checking the unlabelled counts against the UN data and the total label counts.

I'm tallying the correction counts so the expected label total can be checked against the summed UN and view counts. Then I'm checking that every added label is a known theme absent from the UN set and every removed label is one the UN set really has.

Now I'm wiring the theme tags so that a corrected record's chips show which labels were added or removed.

Still writing the theme tags, with the struck UN labels and the added ones shown in their own styles.

Now I'm writing the corrections panel's Undo-all and per-row undo handlers, and the list's undo keeps the labelling mode as it is instead of forcing it.

I'm laying out the header markup next: a label line, the title, a correction line with the UN-labels/my-corrections switch beside it, and the meta line below.

I'm writing the header markup now, with the label line, title, correction line and switch, and the meta line below.

I'm writing the corrections list renderer next, which builds one row per corrected record with its UN labels and the user's chosen labels.

I'm building the corrections table now, with one row per corrected record that shows its UN labels, my labels, the verdict, and an undo button.

I'm setting the corrections list to show a row per corrected record, with its UN labels, my labels, the verdict and an undo button, and I'm giving the toggle button its expanded state.

I'm writing the corrections export next, starting with the list of corrected records and how each one's labels are compared against the UN set.

I'm building the corrections CSV now, starting with a header block that names the source, the build date, and how many records were corrected or marked.

I'm writing the corrections CSV now, starting with a header block that names the source, the build date, and how many records were corrected or marked. The next part of the export will be the column header and the data rows.

I'm writing out the final code now, with a brief lead-in of at most three short sentences before it and nothing after.

