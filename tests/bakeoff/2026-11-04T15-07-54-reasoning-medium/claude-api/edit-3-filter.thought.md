I'm noting that the data has no explicit document-type field, so I'd have to infer it from the mechanism and the symbol format instead. Deriving it that way from symbols like CEDAW/C/.../CO/ seems fragile, so I'll keep the answer simple and honest.

I'm settling on a rule-based "document type" label, derived from the mechanism and the symbol pattern rather than any UN label, and I'll say so on screen. It goes in the existing filter heading 02 as a new select, so the heading count stays at three. The edits are a select in the HTML plus a doctype field threaded through the record, filters, controls and chips in the JS.

I'm working through the edit plan: a new `dtype` field gets added to each record through a `docType` helper, defined before the records are mapped, and the filter state, applied filters, chips and controls get the matching additions.

I'm listing the remaining edit points: the Type select's HTML, the onchange handler, the sync to controls, and the chip and init code.

