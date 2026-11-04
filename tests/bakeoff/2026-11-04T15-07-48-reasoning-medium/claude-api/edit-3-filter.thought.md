I'm looking for a way to filter by document type, but the data has no explicit field for that. The closest options are `mechanism`, `type` (Recommendations or Concerns), and `body`. I'm considering deriving it from the symbol instead, since treaty body concluding observations carry a "/CO/" segment in their symbols, and UPR reports follow a different pattern.

I'm deriving document type from the mechanism and the symbol: UPR reports, treaty-body concluding observations (symbols containing "/CO/"), other treaty-body documents, and Special Procedures reports. I need to be clear with the user that this is a rule I'm applying, not an official UN label. I'll add the select beside the existing type filter, leaving the heading count unchanged, and wire it through the state, chips, sync, change handler, and clear logic. The new field gets defined in the preprocessing loop, placed after the `r._fl=firstLine(t);` line, which appears only once.

Next I'm defining a `docType` helper and registering it in the record loop, so each row gets a derived document type. I'll also list those types as a filter option, then hook up the dropdown's setup, state, and reset logic.

I'm defining a document-type filter and wiring it through the state, chips, and sync logic. Next I'm adding a `dt` field to the filter state and inserting the matching line into the filter and chip code.

I'm adding a document-type select to the filters and wiring it through state, chips, sync, the change handler, and clear, with the CSV export getting the new column too.

I'm going to add 'document_type' to the CSV header row, and add the derived value to each exported row. For the labels, UPR records will be called "UPR recommendations", treaty-body documents will be split by whether the symbol contains "/CO/", and Special Procedures will get their own label, with anything else falling back to "Other".

Adding a small hint element to the filter rail to explain the derived document type.

