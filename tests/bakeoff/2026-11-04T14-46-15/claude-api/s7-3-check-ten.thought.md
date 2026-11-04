The user wants changes to the app's random sample check, specifically letting them correct the theme labels. I need to return the complete file again, so I'll plan the design carefully but keep it compact.

I'm weighing how the user marks a label as wrong or arguable before removing it or adding another, with a default mark of "wrong" and the correction editor shown inside each open card under the existing verdict buttons.

I'm settling the correction feature: a switch between the UN's labels and labels with my corrections, with a line showing how many labels I've changed while keeping the UN's own labels visible. The mode will default to using my corrections, and every count, chart and filter will work from the effective theme list.

I'm working out how a reviewer marks a theme label as wrong or arguable before removing it or adding another, and I'm keeping the themes as the only labels that change, since SDGs and affected persons aren't part of this check. I also want a "corrected by you" tag on each record, with the UN's label struck through beside my version, and the counts and charts working from the corrected list.

I'm deciding how the corrected tags should look on each record: a tag reading "corrected by you" appears in the table row and in the detail view. In the detail view's Themes line, labels I've removed show struck through, and labels I've added show in a distinct dashed style, with the UN's own labels kept visible beside them.

I'm making the labels fully correctable now: the effective theme list gets recomputed from the UN's labels minus my removals plus my additions, so filters, counts and charts all follow it. The UN's original labels stay available for comparison, and a "corrected by you" tag plus strikethrough display keeps each change visible.

I'm checking how the sample and filters behave once corrections change the theme list. The theme filter will read the corrected labels, so a record can drop out of the filtered set while staying in the sample by its IDs, and the stale-sample note only compares the filter state, so it won't trigger from a correction alone.

Next I'm drafting the card's edit controls, starting with a "UN themes" line where each UN label gets its own remove button.

I'm settling how each record's correction gets stored: a removed list, an added list, and a mark, with "wrong" as the default. The add control will offer every theme label in the data, and picking one that the record already dropped simply restores it.

I'm settling how the correction data gets stored: each record keeps its removed labels, its added labels, and a mark that defaults to "wrong," with the mark held alongside the lists so it's saved even before any label changes. Only records with actual removals or additions will count toward the totals and the export.

I'm weighing where the undo controls should live, since each record already has per-label undo and a "clear this record" action, and the header is crowded with the view switch. I'll put the bulk actions (undo everything, download and load the correction file) on the Method & export tab so the Check tab stays uncluttered.

I'm weighing a single toggle for the UN-versus-corrected view, since putting every control in the header would crowd out the other tabs, and I'm keeping the corrections list and bulk actions on the Method & export tab.

I'm moving the corrections panel to tab 04 inside a collapsed details section, so the Check tab doesn't get any more crowded. The view switch becomes a single toggle, and the panel holds the list of corrected records with the download and load buttons.

I'm settling the export side now: corrections will be listed under a collapsed details section on tab 04, with the download and load buttons there, and I'll add a short hint in the sample section pointing to it.

I'm settling how corrections get matched when they're loaded back: by record ID when the file has one, falling back to symbol and paragraph. Since paragraph numbers aren't unique, I'll add an ID column and, for ambiguous matches, compare the UN labels before skipping and reporting the record.

I'm settling the CSV format now: the columns are symbol, paragraph, the UN labels, my labels, my mark, and a record id at the end so reloading matches exactly.

I'm deciding how to read the CSV back in: a small parser that handles quoted cells and line breaks, skips the comment lines at the top, and recognises the header row by its first cell being "symbol".

Writing the CSV parser and the comment handling now, stripping quotes and newlines from the comment lines so the parser doesn't break on them.

I'm settling on a plain page-only approach for the corrections, since storage outside the sandbox isn't reliable, so the CSV download is what keeps them. A short line under the header will tell the user the corrections are only held on this page and that they need to download them to keep them.

I'm settling the view switch as two buttons, "UN labels" and "With my corrections", with the active one marked as pressed, since that reads more clearly than a single toggle. That puts the tab 03 controls at about nine items, which is acceptable as long as the corrections panel stays collapsed on tab 04.

I'm settling the switch as a single button with both labels visible, so the active state is clear without needing two separate controls. I'll add a count of corrected labels to the line above it, with singular and plural forms handled, and note when the view is set to UN labels while corrections still exist.

I'm working out the header details: a short line that counts the labels corrected by the user, plus a small hint next to the switch saying whether the counts, charts and filters show the UN's labels or include the corrections. I'm also planning the CSV export so the themes column reflects the labels currently shown, with extra columns for the original UN themes and a flag marking corrected records, and a comment line noting which label set is in use.

I'm adding a check that the UN labels stay unchanged by snapshotting each record's original themes on load and comparing against it. I'll also add an info line showing the effective label totals, and a check that each corrected record's labels equal its UN labels minus the removed ones plus the added ones.

I'm now working out how the theme display changes between the two label views: in the UN view every label shows as plain, while with my corrections the removed UN labels get struck through and my added labels get marked, with a "corrected by you" tag on records that have changes.

I'm sketching the sample card's label editor now: each UN theme gets a remove control, removed ones show struck through with an undo option, and added labels appear as marked tags.

I'm settling the sample cards on the corrected view: each UN label gets a remove control and removed ones show struck through with an undo, while added labels appear as marked tags. Any edit from a card will switch the view to "with my corrections" first, so the change is visible straight away.

I'm setting the label-selection behaviour for each open card: an add dropdown lists the labels in the file that aren't already applied to that record, and a button adds the picked one.

Now I'm writing the helper functions for the corrections state, keyed by each record's index, with a small structure holding removed labels, added labels, and a mark.

Now I'm writing the helper functions that track corrections per record: a removed-labels list, an added-labels list, and a mark, all keyed by the record's index. The effective labels are the UN labels minus the removed ones plus the added ones, but only in the "with my corrections" view, and the record's themes get recomputed from that.

Now I'm writing the edit handler for the corrections: a remove action records a UN label as removed, undo takes it back out of the removed list, and undoing an added label drops it from the added list.

I'm now checking how the add and remove actions interact: adding a label that was removed just cancels the removal, and adding a label that is new to the record goes into the added list, as long as it isn't already there.

I'm wiring up the edit handler so that a removal, undo, or add updates the corrections state and then refreshes the view. After an edit, focus moves to the matching control, so the user's place in the card is kept.

Next I'm wiring the sample cards to the same theme renderer, so they show the corrected view with remove and undo controls, and a "corrected" tag appears in the card header when something has changed. The card's verdict buttons stay as they are.

Next I'm adding the corrections panel on tab 04 as a collapsible section with its own container, so re-rendering the method page won't close it when the user clicks undo.

I'm adding a collapsible corrections panel on tab 04 that keeps its open state across re-renders, and laying out its table with the UN labels removed and my added labels shown separately.

Writing the CSV export function now...

Still writing the CSV export parser...

Still writing the CSV parser...

Next I'm writing the CSV loader: parsing the file, checking that it has the symbol and my_labels columns, and matching each row back to a record by id or by symbol and paragraph.

Now I'm checking each row's record: first by record id, and if that fails, by symbol and paragraph, with the UN label list breaking any tie. Then I'm reading the user's labels from the cell, dropping any that aren't known, and working out which UN labels were removed and which new ones were added. Last, I'm starting to read the mark column.

Now I'm handling the status message after loading: it reports how many corrections were applied, how many rows couldn't be matched to a record, how many had a label not in the data, and how many had UN labels that differ from the current file.

Now I'm wiring the status message to a persistent element outside the corrections box, so it stays visible even when that box re-renders or closes.

I'm laying out the corrections header: a line under the title with a switch between the UN labels view and the view with my corrections, placed above the source line and kept on one row.

Still writing the switch and status styling for the corrections header...

I'm styling the corrections badges and the switch's on and off states, and I'm adding a note under the chart so it's clear whether counts include the user's corrections.

Next I'm adding a `labelNote()` helper that describes which label set the counts use, and I'm putting that note in the source line for FIG.01 and in the theme table caption. The year range will also count records that picked up an added theme. Then I'm adding checks for untouched UN labels and for corrections being applied, including a summary of how many labels were corrected on how many records.

Next I'm adding the summary line for the labels in use and making the records table's first cell carry the "corrected by you" tag whenever a record has been changed.

Now I'm writing the function that builds the theme tags for each record, showing UN labels that were removed with a dashed style and the user's added labels in red.

Now I'm writing the theme tag builder: each UN label that was removed shows up dashed and struck through with an undo control, and the labels the user added appear in red.

Now I'm wiring up the theme tag builder for each record, so removed UN labels show dashed and struck through with an undo control, and the user's added labels appear in red with their own remove control.

Now I'm adding the card's editor section: a dropdown of labels from the data that aren't already in effect for the record, and an Add button to apply the chosen one.

Still writing the card's editor and mark controls...

Next I'm setting up the head line for the corrections, so the count of corrected labels shows up on its own line, and I'm making the update step rerun the correction pass first, then the header, with the sample cards and the switch staying as they are.

I'm adding a switch and a corrections count to the header, so the user can see how many labels they've changed and flip between the UN's labels and their own view. The switch's hint text changes depending on whether corrections exist and which mode is active, and the handler will flip the mode and refresh the page.

I'm adding a collapsible corrections panel on tab 04 with the explanation sentence and the list of records the user has changed, and it's rebuilt on each render.

I'm adding an undo-all control to the corrections panel that needs two clicks before it clears anything, since there's no confirm dialog to fall back on, and the buttons will be handled through delegation on the box so they keep working after re-renders.

Now I'm wiring the corrections box's click handling through delegation, so the undo, download, load and undo-all buttons keep working after re-renders. The undo-all control will need a second click before it clears anything, and after each change I'll just run the normal update and let the method section redraw the box, then move focus to its summary.

Now I'm setting up the download and load paths for the corrections: the download gets a named CSV file and reports its status in the corrections panel, and loading builds the list of available labels from the data. I'm also taking a snapshot of the record themes at load time so I can check later that they were never changed.

I'm adding the CSV export changes: the filtered export gets a UN-labels column next to the shown themes, and a corrected-by-you flag that only reads yes when corrections are active and the user is in their own view.

Still writing the card's click handling for the expand and mark buttons...

Still writing the focus handling after each card action, so keyboard users land on the control that makes sense next.

Now I'm working out how the switch and corrections box handle their state, including the hint text and the two-click undo-all control.

Now I'm adding the header switch: a button that toggles between the UN's labels and my corrections, sitting on the same line as the source note.

Still writing the code, and I'm adding the final checks for the corrections and export.

I'm writing the label note helper, which picks a line describing whether the counts use the UN's labels alone or include the user's corrections, with the number corrected.

Now I'm writing the snapshot check, comparing the record themes against the copy taken at load to confirm they were never changed.

Now I'm checking that the UN's labels stayed untouched, comparing each record's theme labels against the copy taken when the page loaded, and then tallying how many active corrections reproduce the expected label sets.

Now I'm checking the snapshot and the corrections, confirming the theme labels still match the copy taken on load and that the shown labels agree with a fresh recomputation for every active record.

Now I'm writing the card's editor: a dropdown of labels not yet in effect for the record, plus an Add button to apply the chosen one.

Still writing the editor's label controls: a select of data labels not yet in effect, an Add button, and the mark buttons with an undo for the record.

Now I'm building the label editor and the verdict buttons for each card, and the add dropdown will be filled from the labels the data doesn't already have on that record.

Now I'm writing the CSV export: the parse key combines the symbol and paragraph, and the paragraph column will hold a string value, which might get mangled in Excel but is acceptable.

