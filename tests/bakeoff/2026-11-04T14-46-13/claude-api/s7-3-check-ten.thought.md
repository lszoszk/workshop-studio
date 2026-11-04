I'm planning a change to the app: correcting the theme labels in the random-sample check, and I'll need to return the complete file. I'm also checking the Check tab against the limit of roughly seven clickable things, since it already has four tabs plus several buttons and may already be over.

I'm working out how to store the corrections: keyed by record id, each holding removed and added themes plus a "wrong" or "arguable" mark. I'll keep the view uncluttered by putting the correction controls inside the open card, with the UN-versus-corrected switch staying visible under the title as a single toggle button.

I'm weighing how to lay out the correction editor: a "Correct labels…" button inside the open card would keep it one click deeper, and I'm considering whether the wrong-or-arguable mark should default to one choice or be picked explicitly.

I'm settling the data shape for corrections: each one keyed by record id, holding the themes to remove, the themes to add, and a wrong-or-arguable mark. Toggling a removed label back or deleting an added one undoes it, and an empty correction gets dropped. I also want a list of all corrections, including ones from earlier draws or a loaded CSV, so each can be undone from one place.

I'm still deciding where the corrections list and CSV load/download should live, since tab 03 already has four tabs plus several buttons and I want to stay near the seven-clickables limit. I'm leaning toward putting the corrections download and load in the corrections panel on tab 03, with the rail reduced to just the number on those tabs.

I'm settling where the corrections live: a closed "Your corrections" panel on tab 03 that holds the undo list, download, and load, so none of it is in view until opened. The Check tab's clickables stay within reach that way, though the cards already count toward the limit.

I'm defaulting the switch to "with my corrections" once any exist, so every count, chart and the CSV reflects the labels I've fixed. The corrections download and load stay inside the closed panel on tab 03, and the CSV gets an extra column for the original labels plus a flag for records I've changed.

I'm defining how the UN-versus-corrected switch works: it's a single toggle under the title that shows the count of labels I've changed, and the count reflects every label removed or added. I'm also deciding that the first correction should switch the view to the corrected labels, so the effect is visible straight away.

I'm settling the switch: a two-button segmented control under the title, "UN labels" and "With my corrections," with the count line beside it. If I end up with no corrections, both options just show the same labels, so I'll leave it enabled and not force a view.

I'm working out how to apply the view across the app: each record gets its effective themes, built from the original labels minus any I removed plus any I added, and everything downstream (top themes, filters, the record table, checks, the sample, the summary and the CSV) reads from that. Because the record-count checks are cached, I'll need to clear that cache whenever a correction changes so the figures stay current.

I'm adding a corrections check to the checks list: how many labels and records the user has changed, which view is active, and any rows from a loaded CSV that didn't match a record. I'm also verifying that the original labels still match the raw data, and I'll reset the cached record-count checks whenever a correction changes so they stay current.

I'm working out how to key the corrections by each record's id, and I'm checking the CSV columns so the export stays consistent with the view.

I'm weighing whether to add an `id` column to the CSV, since matching rows back by symbol and paragraph alone breaks down when paragraph numbers are missing or repeat. I'm inclined to include the id as an extra column so corrections restore reliably, even though the requested columns were symbol, paragraph, the UN's labels, my labels and my mark.

I'm settling the CSV format: the header will be symbol, paragraph, UN labels, my labels, my mark, and a record id as the last column. On load I'll match rows by id first, and fall back to symbol plus paragraph only when that pair is unique, using the UN labels to break ties. Anything I can't match will go into a load report on screen, with the counts of restored and unmatched rows.

Now I'm settling the CSV details: the file will carry a record id as an extra last column, and labels will be joined with " | " and quoted properly, since some label names contain commas. On load I'll skip any leading comment lines and the BOM, then match rows by id, falling back to symbol plus paragraph only when that pair is unique.

I'm making the corrections store a map keyed by record id, with each entry listing the labels to remove and the labels to add, plus the wrong-or-arguable mark. When a CSV is loaded, I'm working out the removed and added labels by comparing the file's label list against the record's original UN labels, and skipping any added label that isn't in the dataset.

I'm deciding how corrections show in the records table: a small "corrected by you" tag on the first line, my added labels in their own style, and the removed UN labels struck through next to them. I'm still weighing whether that tag should also appear in the UN labels view, since that view only shows the original labels.

I'm laying out how each corrected record shows its labels: in the "with my corrections" view, the UN labels stay plain except removed ones, which get struck through, and my added labels appear in their own style, with a "corrected by you" tag beside them. In the UN labels view, the record shows only the original labels, with a note that the corrections aren't applied there.

I'm settling how corrected labels look in the records table and the expanded rows: my added labels get their own red-bordered style with a "+" prefix, the removed UN labels show struck through with a hidden note for screen readers, and a small "corrected by you" tag goes on the first line and the sample card.

I'm working out the corrections display in the sample card: the theme chips become interactive, so in editing mode each UN label can be toggled to removed, and I'm planning how that fits with the header switch and the records table.

I'm laying out the sample card: the verdict buttons and a "Correct these labels" toggle come first, and the editor opens to let me strike UN labels, remove my additions, add labels from the data, pick a mark, and undo.

I'm settling how a corrected record's labels appear: in the "with my corrections" view, removed UN labels get struck through and my additions get their own style, with a "corrected by you" tag. In the UN view, the record only shows the original labels, with a note that the corrections aren't applied there. I'm also planning the sample card's editor, with label toggles, an add control, a mark choice, and undo, and I'll keep the open state per card so it resets when the card changes.

Now I'm checking the sample card's edit flow: the card's remaining state carries over after a correction, so I'll call renderSample directly when a correction changes, and filter chip removals leave the cards as they are.

I'm defining the correction store as a map keyed by each record's key, and a helper that returns a record's effective themes: its original UN labels minus any removed ones, plus my added labels, but only in the "with my corrections" view. Then a refresh function will recompute every record's themes from that.

I'm settling the correction rules: removed UN labels must come from the record's own labels, and I'll only offer added labels that the record doesn't already carry. Each change goes through one helper that saves the correction, drops it if it ends up empty, and clears the cached file checks.

I'm making the view switch to "with my corrections" whenever a correction is added, so the change is visible, and I'll leave the view alone on undo. After each change I'll refresh the effective themes, re-render the view and the sample, and I'm weighing whether to redraw the sample card on every render so the editor state stays consistent.

I'm writing a helper that wraps the sample re-render and restores focus afterward, keyed by a data attribute, so keyboard users don't lose their place after a correction. I still need to tag each card's buttons with that focus key.

I'm wiring up the card's focus keys and adding an undo option to expanded records, then exposing the corrections list in a details panel on tab 03.

Writing the Undo and Download controls, plus the CSV load path using a hidden file input.

Next I'm adding a paste-the-CSV fallback in case the file chooser is blocked in the sandbox, though I'm weighing whether that clutters the panel too much.

Next I'm writing the CSV export for corrections, one row per record, and I'll keep the file in a format the load step can read back.

Now I'm writing the CSV parser, which strips the leading comment lines and reads the rest of the file row by row.

Still writing the CSV parser: it skips the leading comment lines, then reads the remaining rows cell by cell, handling quoted fields and both line-ending styles.

Now I'm writing the header mapping, which finds the columns for the symbol, paragraph, UN labels, my labels, mark and optional record ID, and reports a missing-column message if the file doesn't look like a corrections export.

Next I'm reading the CSV rows and matching each one to a record, first by its record ID when present and otherwise by symbol and paragraph. I'm splitting the UN and added label cells into lists so I can check them against the record's labels.

I'm checking the record matching: if the ID turns up a record but its symbol differs, I'll drop the ID match and fall back to symbol and paragraph, and if several records share that pair, I'll narrow them down by their UN labels. Once a record is matched, I'll split out which UN labels were removed and which of my labels are new.

I'm writing the import step: it parses the uploaded file, matches each row to a record by its ID or by symbol and paragraph, and checks the labels against the record's own. I'll apply the changes, switch to the "with my corrections" view, and report what was restored, replaced, or skipped.

I'm adding a small CSV-paste fallback in the corrections panel, since the file chooser might be blocked in the sandbox, and I'm weighing whether it clutters things too much. I'll keep it, since the cost is modest and it's inside a closed details element.

I'm also settling how loading works: it merges into the current corrections rather than replacing them, so a row overwrites only the correction for its own record, and the on-screen report says how many were restored, how many replaced an existing correction, and how many didn't match.

Still writing the CSV export function, which builds comment lines and a header, then one row per correction in record order.

Now I'm adding the Undo-all control with a two-step confirm, since `window.confirm` may not work in the sandbox.

I'm adding the view toggle to the corrections line: two buttons, "UN labels" and "With my corrections", with the pressed state showing which one is active. The count text will say how many labels were corrected, singular for one, and switching the view will update the display.

I'm adding a view suffix to the chart title and source notes so it's clear whether the UN labels or my corrections are in use, and I'll include the same note in the summary and CSV comments.

Next I'm wiring the corrections count and the UN/with-corrections switch into the line above the chart, with a small hint when corrections exist but aren't applied in the UN view. The chart title and source notes will also name which label set is in use, and I'll make sure the cached checks get cleared whenever the view or the corrections change.

I'm restructuring the corrections check in the renderer, so it gets appended after the existing seven checks rather than cached. It should confirm the UN labels are unchanged from the source data and that the label totals match the active view.

Writing the corrections check now: it compares each record's UN labels against the original themes to confirm they're untouched, then totals the label counts for the active view.

Continuing the corrections check, I'm writing the label-total comparison: the UN label count plus any labels added by the user, minus those removed, and I'll show the expected figure alongside the one actually displayed.

I'm settling the Records-tab layout next, planning to add a small corrections badge beside each row's first line so it's clear which records have been changed.

I'm adding a corrections tag to each record's first line, and in the expanded row I'm building a themes display that shows which UN labels were removed and which ones I've added.

Now I'm working out the theme display for each record: struck-through UN labels in the corrections view, my added labels marked as mine, and a note when the corrections aren't applied in the UN view.

Still writing the CSS, adding the styles for the struck-through UN labels, my added labels, and the corrections badge.

I'm building the editor markup for each record, with a hint explaining that clicking a UN label removes it and clicking again restores it, and I'm filtering the available labels to exclude the ones already present.

I'm writing the editor markup for each record: the UN labels appear as clickable buttons, and a click toggles whether one is removed, with the removed ones struck through and marked as restorable.

I'm building the remove and restore buttons for each UN label, with struck-through text and a small "restore" action when a label is removed. Each of my added labels gets a "drop" button, and there's a select menu of the remaining available labels with a button to add one.

I'm laying out the editor for each record: UN labels as clickable buttons that toggle removal, a list of my added labels with a drop action, a select menu with an add button for the remaining labels, and a mark toggle between "Wrong" and "Arguable" that's stored as pending until a correction exists.

Still wiring up the card's event handlers: toggling the card open, the verdict and mark buttons, label removal and restore, adding and dropping labels, and undo. Each handler will look up the record by its index, and I'll reset the edit state when a different card is opened.

Still writing the corrections list render: it counts the corrected labels and records, then builds a list of the corrected records with the buttons for the body.

I'm putting the static controls in a separate details block that stays out of the dynamic list: a summary line, the undo-all, download and load buttons, and a paste box with its own status message. It will sit as a third panel on tab 03, after the sample.

I'm placing the corrections summary and its list above the cards, right below the tally, so they're visible without scrolling past an open card. Each list row will show the record reference, the mark, which UN labels were removed (struck through) and which I added, plus an undo control.

Now I'm wiring up undo: a document-level click handler will catch any undo button, whether it sits in a card, the corrections list, or the records tab. The undo-all control will need an arming timer so one click doesn't wipe everything. The records tab row handler will return early on undo clicks so they don't also toggle the row open.

Now I'm wiring up the document-level undo handler so it works from the cards, the corrections list and the records tab, and having the records tab click handler step aside for undo clicks.

Still wiring the re-render path: the corrections change will refresh the themes and view, then re-render the checks, sample and corrections list together, all wrapped so focus survives.

I'm wiring up the view switch so it clears the cached checks, refreshes the themes, and updates the header, then re-renders while keeping focus on the segment button. I'll set the initial theme list to the UN view and build each record's theme list with a key, plus a sorted list of every UN label with its record count for the select menu.

Next I'm checking where the theme lists get read: the top-themes summary, the filter, and the CSV export, which should now write both the shown labels and the UN originals plus a column marking records the reader corrected.

Next I'm adding a sentence on corrections to the methods text, saying they last only while the page is open, the UN's own labels are never changed, and downloading the CSV is the way to keep them. I'll also tighten the methods paragraph so it still fits its original length.

Now I'm adding the corrections summary and list above the cards, and wiring the undo controls so they work from the cards, the list and the records tab.

Now I'm setting up the records' data: each record gets a key, and I'm keeping a copy of the original UN labels next to the ones shown, plus a count of how many records carry each UN label for the select menu. I'm also adding a view state that starts on the UN labels.

Still building the correction state: a map keyed by record, a count of every edited label, and a helper that re-derives each record's shown themes.

I'm wiring the mark toggle and the label remove, add, and drop actions so each one updates the stored correction for that record.

Now I'm setting up the view toggle: the corrections count line in the header, with the active view button marked as pressed.

I'm adding the corrections line to the header and the mark text on each card, so the reader can see which records they've changed.

Still building the editor markup: the card body will show the theme tags, the verdict buttons, and a "Correct these labels" toggle that opens the editor for that record.

Now I'm writing the corrections list: it picks out the records that have an edit, shows a count of the labels changed and the records they sit in, and builds a row for each with the record reference and its changes.

Still building the corrections list: each row shows the record reference, its mark, the struck-through UN labels and the added ones, plus an undo control. The summary counts those edits and the records they sit in, and the undo-all button only appears when there is something to undo.

Still writing the corrections list, which will show a short count line, one row per corrected record with its mark and any struck or added labels, and an undo control per row.

Now I'm writing the corrections CSV: it takes the records with an edit and writes one row for each, with the UN's own labels beside the labels the reader wants shown.

I'm also computing each record's chosen labels from its correction, whatever view is on screen, and pulling the shared theme-applying logic into one helper so it's reused.

Next I'm setting up the lookup maps: one keyed by each record's key, and one grouping records by symbol and paragraph so corrections can be matched back to them. I'll split the label strings on the pipe separator, though labels that contain a pipe would break that.

Now I'm writing the loader for a saved corrections file: it parses the rows, checks that the required columns are there, and stops with a message if any are missing.

I'm finishing the load routine: after the loop it will switch to the "mine" view when anything was restored, refresh the corrections list, and then show the result message, so the list rendering doesn't overwrite it.

Next I'm adding the file input handler, which reads the chosen CSV and passes it to the loader before clearing the input so the same file can be picked again. I'll also write the third tab's markup with its details section, update the explanation on the check tab to say corrections stay in the page until downloaded, and make sure the sample panel shows a placeholder when there's nothing to display.

Now I'm wiring focus retention: a helper remembers which control had focus, re-renders, then puts focus back on the matching element by its key. Verdict buttons and card toggles will use that, and the add select and add button get their own keys so focus returns to them after adding a label.

Next I'm wiring the add-label select and button so the chosen label is read when Add is clicked, and I'm adding CSS for the segmented view control, the correction tags, the editor, and the corrections list.

Now I'm writing the rest of the page's markup and CSS, covering the view toggle, the corrections list, and the editor styles. I'll build the record details so each theme shows as a tag, with an undo control next to it when it has been changed.

Still writing the mark handler: when a card's verdict changes and a correction already exists, it updates that record's stored mark and re-renders the corrections.

Now I'm finishing the mark handling: a click on a card's mark updates the stored mark for that record if a correction exists, and re-renders the corrections list. I'm also laying out the header with the corrections count and the view toggle.

Now I'm writing the editor markup for each record: the UN's labels stay as they are, and the reader's changes sit beside them as a mark and a set of added and removed labels.

Still writing the editor markup, which lists the record's UN labels with a click-to-remove control on each and any labels the reader has added, plus a dropdown of the other labels in the data to add.

Still writing the editor markup: each record's UN labels are listed with a click-to-remove control, followed by any labels the reader has added and a dropdown of other labels in the data to choose from.

Next I'm wiring up undo-all: the first click arms it and changes the label to ask for a second click, which clears every correction, and if no second click comes within four seconds it quietly disarms.

I'm adding a `record_id` column to the output so each row can be traced back to its source record.

