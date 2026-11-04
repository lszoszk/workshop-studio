I need to make a substantial change to the app and return the full file. The main requirement is that in the random-sample check cards on the Check tab, when someone marks a label "Doesn't fit" or "Unsure," they can correct it by removing a theme or adding one from the themes already in the data. UN labels should stay as they are, and nothing should be overwritten without it being visible. Every count, chart, and filter has to update to reflect those corrections.

The plan now covers how corrections show up in the table, the expanded details, and the sample cards, plus a header line counting label changes and a UN/corrected switch.

I'm weighing where the correction controls should live, since a manager for corrections would be used rarely and shouldn't crowd the Check tab. I'm considering a separate Corrections tab over the Method & export tab, because the list of undo buttons plus the download and load controls would push that tab past a comfortable number of clicks.

I'm now weighing a separate Corrections tab, placed before Method & export, so the undo list and the download and load controls don't crowd that tab.

I'm settling the tab layout now: Corrections goes at 04 and Method & export moves to 05, which keeps the number of tabs at five. For the header, I'm treating the UN/corrected switch as a single toggle control, so it counts as one clickable item instead of two.

I'm weighing five tabs against cramming corrections into the Check or Method tabs, and five stays within the limit. The next question is how the switch works: it'll be either "UN labels" or "with my corrections", so counts and filters follow whichever is selected.

I'm settling on keeping corrections in their own record per label, with the verdict stored alongside them, and the sample won't be reset every time a filter changes.

I'm settling the correction model now: each label change is stored against its record by id, and the verdict marks persist per record rather than resetting on every filter change. Since corrections can move a record out of the current filter, I'll keep the drawn sample intact until the user redraws or changes a filter themselves. The tally will then count only the records in the current sample.

I'm settling how the correction editor gets enabled: only cards marked "Doesn't fit" or "Unsure" will open the label-editing controls, so the verdict itself decides when a correction is possible.

I'm now settling the rule for when the correction editor appears: it stays open whenever a card is marked "Doesn't fit" or "Unsure," and also on any record that already has corrections, so they can still be undone even if the mark is later changed to "Fits."

I'm settling on a CSV that records each corrected paragraph with its original and corrected labels, and I'm weighing whether to add an id column so a reloaded file matches the right record, since symbol and paragraph alone may not be unique.

I'm settling how restoration matches a reloaded row: by record id first, then by symbol and paragraph if that pair is unique. For the labels, I'll work out the removed and added themes from the UN labels versus the saved ones, then apply them against the current record's themes. If the UN labels in the file don't match the current data, I'll still apply the change but report how many rows differ.

I'm settling how corrections get exported and restored: the CSV carries the UN's labels, my labels, and my mark per record, and I'm adding a record id so a reloaded file matches the right row even when symbol and paragraph repeat. Loading will go through a plain file input and a quote-aware parser that skips comment lines and detects the header.

I'm weighing whether to merge loaded rows into the existing corrections or replace them outright. Replacing would silently drop any corrections not in the file, so I'm leaning toward merging, where loaded rows overwrite only the records they name and everything else stays.

I'm laying out how the correction editor will look on each card: a select of the themes not yet on the record, with an Add button. Each UN theme gets a × to remove it, and a removed one stays visible struck through with its own undo. Themes I add will carry their own style and an × to take them back.

I'm working out how the corrected records get shown: a small "corrected by you" tag on the table row, and the themes on each card drawn as the UN's label struck through beside my replacement, each with its own styling and a hidden text note for screen readers.

I'm settling how the correction view behaves in the two modes: under "UN labels" the cards show the UN's themes as they are, with a quiet mono hint that this record has corrections and the switch will show them. Under "with my corrections" I'll show the tags and the strike-throughs instead, and the corrected-by-you tag only appears there.

I'm now checking the sample cards, the Corrections tab list, and whether the theme counts and "Years" figures use the effective labels, with the chart title noting "(with your corrections)" when that mode is on. I'm also planning the CSV export to carry the current themes, the original UN themes, and a corrected flag, plus a comment line naming the active label mode, and a summary that states the mode and how many corrections exist.

I'm now planning a consistency check for the corrections: each record keeps its original UN themes in a separate frozen copy, while the effective themes are computed from those plus the corrections. The check will confirm that every removed label was on the UN list, every added label is in the data but not in the UN's, and the stored originals still match the file. The tally and chart will then count the effective themes.

Now I'm working out how the effective themes get recomputed: each record keeps its original UN list, and a refresh step rebuilds the shown themes from the corrections only where they exist, leaving everything else on the UN labels.

I'm settling how corrections are keyed: each record gets a stable key from its id, falling back to its position when there's no id. Persistence is the open question, since sandboxed storage may not be available. I'll skip localStorage and rely on the CSV the user asked for, and tell them on the corrections tab that corrections only live on this page until downloaded. Corrections will be stored per record as lists of removed and added themes, and removing a UN theme will record it in the removed list.

Now I'm working out how the corrections get stored and undone: removing a theme records it as removed (or cancels an earlier addition), adding one records it as added (or cancels an earlier removal), and an empty entry gets deleted. Each record can be undone on its own, and I'm weighing a two-step "Undo all" button since a plain confirm dialog may be blocked here. I'm also counting the total corrected labels as the sum of removed and added entries across all records.

I'm laying out the header so a single line under the title shows how many labels the user has corrected, with a switch on the same row to flip between the UN labels and the user's corrections. I'm still settling whether the two modes should be a toggle button or a two-segment control, leaning toward the latter so each side is clearly labeled.

I'm settling on a single switch button for the two label modes, with "UN labels" and "with my corrections" both shown and the active side highlighted in red and bold. It toggles on click and reports its state through aria-checked, and I'm leaving it enabled even when no corrections exist yet.

I'm now deciding how the correction editor behaves in the UN-labels mode: the chips stay plain there, and a hint says to switch to "with my corrections" before editing, so the two modes don't get mixed up.

I'm settling on the editor behavior: the card's correction editor will always show the full corrected view with the UN labels struck and my replacements beside them, since that's where edits happen, while the switch still controls the rest of the page like counts, charts, filters, and the table.

I'm settling the editor behavior now: the card's correction editor always shows the corrections view as a workspace, with a hint that edits appear everywhere once the switch is on "with my corrections", and any edit there flips the switch over automatically. The sample stays fixed when corrections change, and the tally counts only the sample's records.

I'm handling the focus after a correction: the card re-renders and loses focus, so I'll move it back to the add control in that card's editor, and the header count and rail numbers will refresh with the rest of the page.

Now I'm moving on to the Corrections tab: a short intro saying corrections only live on this page until downloaded, then a table of records with their UN labels struck through, my labels beside them, and a per-record undo. The header count and switch stay where they are, and the download and load buttons come next.

I'm laying out the Corrections tab: a short note that corrections only live on this page until downloaded, a table of records showing UN labels with removed ones struck through beside my labels, and per-label undo controls. Download, load, and "Undo all" buttons go alongside, with an empty-state hint when there are no corrections yet.

I'm sketching the label editor as one shared function: each theme shows as a chip, struck through if the user removed it, and clicking a struck chip restores it, clicking an added chip undoes it, and clicking a plain chip removes it.

Now I'm writing the card's label editor: UN labels show as chips that can be removed, removed ones appear struck through and can be restored, and added labels appear as my own chips that can be undone. The detail rows and the corrections table will show the same chips without buttons.

I'm working out how the add control in each card will look: a select listing only the UN labels that aren't already on the record or added by the user, with a label, and an "Add label" button beside it.

I'm setting the add control in each card: a labeled select listing only the UN labels not already on the record or added by the user, plus an "Add label" button. The Fits, Doesn't fit, and Unsure marks decide whether the editor appears, and a hint tells the user to mark a record as Doesn't fit or Unsure when it isn't marked that way yet. The tally line will read "Themes: x fit, y don't, z unsure of 10 judged".

Now I'm settling the CSV handling: marks get written as "Fits", "Doesn't fit", or "Unsure", and on load I'll read those back and set them on the matching records, with the status line reporting how many were applied.

I'm working through the CSV import now: reading the header columns by name, matching each row to a record by its ID or else by symbol and paragraph, and splitting the label list apart to check each label against the known themes.

I'm writing the CSV import: a parser that skips comment lines and handles quoted fields, matching each row to a record by ID or by symbol and paragraph, then checking its labels against the known themes. I'm also reporting how many rows were restored, how many weren't found, and any labels that don't exist in the data.

I'm finishing the CSV export: a header with the country, source, build date, and a note that the UN's own labels are kept, then one row per record that has corrections, in record order. The download button stays disabled until there is something to save. I also need to check that filters and the summary count from the effective labels, and that "not labelled" counts records with no current themes.

I'm checking the corrections against the UN labels: first a line for how many labels were removed and added and in which mode, then one confirming the UN labels still match the file, and finally a check that every removed label was actually one of the record's UN labels.

I'm checking the corrections against the UN labels: a count of the sum over records for the current mode, compared with the total of the effective label lists, which should match. I'm also flagging the FIG.01 title to note that corrections are included when that mode is on.

I'm settling how the sample behaves when a filter changes: the apply step will keep the current sample and page only when the switch is flipped, and otherwise reset both and close any open card. Marks will survive these refreshes since they're now keyed by record rather than index.

I'm updating the method text so the labels paragraph also explains that corrections sit on top of the UN labels when the switch is on, while the UN's own labels stay in the file and the CSV columns.

I'm settling the details of the Corrections tab's CSV: each row can flag "corrected by you," and in the mine mode the table's first cell gets a small tag beside its button. I'm also keeping the detail view's themes as plain chips, with that same tag appended after them.

I'm writing the chip helper for the corrections view, with one branch for the UN labels, one for the user's labels, and an edit mode that adds the buttons.

I'm working on the corrections logic now: a removal or addition helper that looks up the record by its key and creates a corrections entry for it if one doesn't exist yet.

I'm adding the helpers that remove or add a label: a removal of a UN label gets recorded unless it was already added by the user, which undoes the addition instead. Adding a label works the same way in reverse, and a helper clears out a record's corrections entry once it's empty.

I'm writing the function that renders the sample cards, with the sample reset on the fly.

I'm rendering the sample cards now, showing a corrected-by-you tag on any record I've changed. When a card is open, its themes appear as a diff view with the UN's labels kept and my edits marked.

I'm wiring up the add control in each card: a labeled select of UN labels not already on the record or added by the user, plus an "Add label" button. The verdict buttons come first so the flow is judge, then correct, and the editor hides again once a record is marked Fits without any corrections.

I'm working out how the corrections helpers will handle the sample cards: each card's editor will open when a record is marked Doesn't fit or Unsure, and the focus will move to the label select after a change, or to the card toggle if the editor disappears.

I'm sorting out the Corrections tab's render: it will list the records that have corrections in record order, and I'm wrapping up the focus handling so that after an undo the heading takes focus, since losing focus to the page body would be poor for keyboard users.

I'm working on the Corrections tab's HTML: a panel with a heading, an intro line, and a table body that gets filled in dynamically. I'm also adding a hidden file input for loading a corrections CSV, which a visible button will trigger, and I'm checking whether that click will be allowed in the sandboxed frame.

I'm settling how the file input gets triggered: a visible label styled as a button will open the hidden file input, which I'm keeping out of the layout rather than removing it entirely, so the click still works in the sandboxed frame.

Next I'm switching the Load corrections control to a styled label that wraps a visually hidden file input, so clicking the label opens the file dialog natively without any extra JavaScript. I'll also restyle the button selectors from `button.btn` to a general `.btn` class so the label matches, and add a focus ring that shows when the hidden input has keyboard focus.

Next I'm styling the switch: a bordered track with a sliding knob, set in small uppercase monospace text.

Still writing the switch styles: a bordered track with a sliding knob, with the red state for the on position and the labels highlighting accordingly.

Next I'm settling the tab layout: five tabs, with a new Corrections panel and a Method & export panel, and the arrow-key navigation will follow the tab count instead of a fixed number.

I'm working out how the record key helper maps each record to a stable identifier, and how the theme lists are recomputed from the user's corrections whenever the mode switches.

I'm checking the summary line so it says which labels are being shown, and the CSV export so it gets the two new columns, one for the UN labels and one flagging corrected records. The theme column will reflect whichever mode is active.

Checking whether the rendered check text is already HTML-escaped, since theme names containing "&" would otherwise be misread as markup.

I'm checking the correction validation next: each saved correction should point to a real record, and any removed label should actually be one of that record's UN labels, while any added label must be a known theme not already on the record.

I'm checking that the saved corrections point to real records and valid labels, then verifying that the UN labels stayed intact.
I'll also make sure the counts match the active mode, with the expected total computed from each record's UN labels plus or minus its corrections.

I'm checking the sample section's wording and layout: the intro stays as it is, with a second line explaining that marking a card as Doesn't fit or Unsure lets the reader remove or add labels, while the UN's original label stays visible struck through. I'm also keeping the number of interactive controls on that tab in mind, and I'm making the draw use the current mode with the open card reset, while marks persist across redraws. Finally I'm reading the seed input and the sample seed value.

I'm finishing the event handling for the Corrections workflow: removing or adding a label switches the view to the reader's corrected labels, while undoing an edit leaves the current mode as it is.

I'm updating the Corrections-related toggle and status text so the header reflects the current label mode, and I'm checking which labels are shown in each record's cell as the view changes.

I'm now writing the helper that turns a record's labels into chips, with the corrected view marked, since the detail row needs to show what the reader changed.

I'm writing the chip helper for the record view: plain tags for the UN view, and for the edit view each original label gets a struck-through state with its own remove control.

Still writing the chip helper: for the struck-through UN labels in the edit view, each becomes a button that restores the label when clicked, and the other labels get a remove control.

Still writing the chip helper: for the struck-through UN labels in the edit view, each becomes a button that restores the label when clicked, and the other labels get a remove control. Added labels get a pen-marked chip with a button to undo them.

Still writing the sidebar and tag styles: a dashed, muted border for the struck-through labels and a red-tinted, italic tag for the labels the reader added.

Still building the table helper: the UN labels column will show every original label, with the removed ones struck through, while the "My labels" column shows what remains plus anything I added.

I'm writing the table helper for the Corrections tab, where each row shows the UN's labels with removed ones struck through, next to the labels that remain plus any I added. The removed and added chips become buttons so they can be undone from there, and each row gets an undo-all control.

Still writing the CSV import: I'm splitting each line into fields and handling quoted values, then loading the corrections from the file's text.

Still writing the CSV import: I'm parsing the header row, looking up the columns for symbol, paragraph, labels and mark, and matching each row to a record by its ID, with a fallback on symbol and paragraph.

Still writing the CSV import: I'm matching each row to its record by ID, with a fallback on symbol and paragraph, and checking that the UN labels in the file agree with the record before saving the correction.

I'm wrapping up the header and tab keyboard handling: arrow keys cycle through the tabs, and End jumps to the last one. I'll also check the earlier state filter wiring, since it still attaches a listener even when there are no states to fill.

I'm now checking the event flow and small robustness issues: the document click handler ignores clicks in detail rows, and keyboard activation focuses the new control. I'm also confirming that the keyword filter trims its input before applying it, and that the draw step re-runs the filters.

I'm adding a labels note to the FIG.01 overview that says whether the view shows UN labels or the reader's corrected labels, with the count when corrections exist, and I'm keeping the tiles and how-computed text as they are.

Writing the JavaScript for the data setup and record mapping, with a unique key for each record.

Still writing the record keys and state: each record gets a unique key, with mode set to the user's corrected view and the corrections and marks kept in their own stores.

I'm defining a helper that computes each record's effective labels by removing the reader's removals and adding their additions, and I'm writing the mutation functions that update those corrections alongside the marking labels.

I'm checking how the sample card and its chips are built, with the editor showing when a card is marked Doesn't fit or Unsure or already has corrections.

I'm writing the sample card editor: it lists the labels the reader can remove and offers a dropdown of other labels from the data to add.

Still writing the sample card editor: each card gets a select of other labels from the data, a button to add the chosen one, and an undo-all control when the record already has corrections.

Still writing the sample card handlers: the verdict buttons will update the mark for each card and redraw just the sample, and the add-label button will read the chosen label from its dropdown.

Still writing the record helpers, I'm now looking at how the Corrections tab handles undoing labels: a removed or added label on a record can be undone straight from the chip, so the handler needs the record's key and index. I'll look up the record through its key and use that index to find the matching editor and card.

Now I'm writing the Corrections tab's render function: it pulls out the records that have corrections, sets the intro text from the label count, and fills the table along with the download and undo-all controls.

Still writing the Corrections table row: each row shows the record's symbol and paragraph, the UN labels, my labels, the mark, and an undo control.

I'm writing the download function for the corrections, which will export the labels so they can be reloaded later.

Writing the CSV export: I'm building the header comment lines with the country, the save date and the label count, then the column row for symbol, paragraph, UN labels, my labels, my mark and record ID.

Still writing the Corrections download and the file-loading wiring: after the CSV is exported and the change handler is attached, I'll look at the Method text and the summary line so they mention the corrected labels.

Still writing the Corrections-related rendering: I'm finishing the export controls and the table's undo buttons, and polishing the button and file-input styles so the hidden file picker still gets a visible focus outline.

Still writing the Corrections-related rendering: I'm wiring the header correction summary so it notes how many labels were corrected and whether they are currently hidden by the UN view.

Still writing the Corrections handlers: each undo or remove click finds its record through the key, and after a commit the focus goes back to the title or the matching sample card.

I'm making the sample-card signature change with a version counter, so the chart redraws whenever the labels are refreshed. Next I'll wire the keyword filter's timer.

Now I'm finishing the keyword filter and the page setup: on load it initialises the header, controls and labels, then applies the filters. The tab switch will call the render step, and the "Show 50 more" button will call the records render again.

