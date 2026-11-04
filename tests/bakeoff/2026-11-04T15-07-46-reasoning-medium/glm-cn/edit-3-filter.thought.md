Add "Document kind" filter based on... The data has `type` (Recommendations/Concerns/Observations/Other) but user asks "type of document (concluding observations, UPR recommendations)". Distinct documents — derive doc kind from symbol/first record of each symbol? Simplest: derive a document type label per symbol from the records' `mechanism`+`type`. Actually "concluding observations" vs "UPR recommendations" — could derive from symbol: contains "/CO/" → Concluding observations; "A/HRC/" UPR working group → UPR recommendations. Better to derive per-document from the records' type/mechanism: group by symbol, classify.

Simplest robust: new filter heading? No, add to heading 02 "Mechanism, body, type" a "Document type" select listing derived kinds: "Concluding observations (treaty body)", "UPR recommendations", "Special Procedures report", etc. Derive per symbol:
- mechanism Treaty bodies & type Concerns/Observations or symbol contains /CO/ → "Concluding observations"
- mechanism UPR → "UPR recommendations"
- mechanism Special Procedures → "Special Procedures report"
But per-record mechanism differs per record only by symbol? Records of one symbol share mechanism. So classify record by its symbol via a map built from first record of each symbol.

Rules:
- mech UPR → "UPR recommendations (A/HRC/…)"
- mech Treaty bodies → symbol includes '/CO/' ? "Concluding observations" : "Treaty-body report" — hmm treaty bodies could also be LOI etc. Just: "Treaty body concluding observations" if /CO/ in symbol else "Treaty body document".
- Special Procedures → "Special Procedures report".

Filter applies to records whose symbol's class matches. Add select in fbody of heading 02, F.dockind. Add chip. Update clearall, syncInputs (fillMech builds it), CSV filters line, method text mention? Method tab built once — add one sentence? It's fine to add briefly; but method text already written via renderMethod with dataset.done — update the filters paragraph. Easier: just add a clause. I'll edit the filters sentence.

Edits:
1. F state: add dockind:''.
2. In filtered(): add dockind check.
3. Build docKind map after stateCounts.
4. fillMech: add select after ftype.
5. Add HTML label+select in rail.
6. onchange handler.
7. chips: add dockind.
8. clearall: reset.
9. CSV filters line.
10. Method filters paragraph.