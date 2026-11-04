I'm weighing whether the data has a document type field, which it doesn't directly. The closest fields are the mechanism and the type of recommendation or observation, and the mechanism filter already exists. I'm considering deriving the document type from the symbol pattern, since codes like the "/CO/" segment seem to mark concluding observations.

I'm settling on deriving the document type from mechanism and symbol: Treaty body symbols with "/CO/" count as concluding observations, other treaty body documents get their own label, UPR reports and Special Procedures reports are each separate. Since the app derives this itself rather than using UN's labeling, I'll say so explicitly. I'll put it into heading 02 as a select so it stays a one-click filter.

Still working through the search edits: the clear handler and the let initializer for the filter state are different strings, so I'll match on the "let " prefix to keep the search unique. Then I'll add the document-type check after the existing type filter, plus the description, chip, and select entries.

Still wiring the new document-type filter through the code: a dropdown in heading 02, a derived value per record, and matching in the filter, description, chips, clear handler, and rail sync. The next part is the event list, where the new select's element ID gets paired with its filter key.

