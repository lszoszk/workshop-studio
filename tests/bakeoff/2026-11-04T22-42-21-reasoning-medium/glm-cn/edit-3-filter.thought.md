The user asks to filter by "type of document (for example concluding observations, UPR recommendations)". The data has no document-type field; the closest is the existing "Type" (Recommendations/Concerns) and mechanism. But we can derive document type from the symbol: e.g., /CO/ = concluding observations, UPR docs A/HRC/... Add a derived "document type" filter computed from symbol patterns. Explain briefly.

This is an edit to my app. I need SEARCH/REPLACE pairs matching my latest file exactly.

Derive document type per record once:
- symbol contains "/CO/" → "Concluding observations"
- mechanism UPR → "UPR recommendations" (symbols like A/HRC/... or the docs) — actually UPR recs come from A/HRC/... reports of the working group. Use mechanism === "Universal Periodic Review" → "UPR recommendations".
- Special Procedures → "Special Procedures report".
- else "Other".

Add filter heading 03 (renumber years/SDG to 04? Headings are numbered 01 Keyword, 02 Mechanism..., 03 Years and SDG). Add as a fourth heading "04 Document type". Fine.

Edits:
1. Derive _doctype in the recs.forEach.
2. Add F.doctype.
3. Add select in fp2 or a new heading. Put it inside heading 02? Heading 02 is "Mechanism, body, type" — adding document type there keeps at 3 headings. But labels: "Type" (record type) vs "Document type" may confuse. Plan says at most ~7 clickable things; adding a 4th heading is fine. I'll add heading 04 "Document type".

Edits list:

A) derived field:
SEARCH:
recs.forEach((r,i)=>{r._i=i;r._para=paraNum(r.text);
  r._states=r.mechanism==="Universal Periodic Review"?extractStates(r.text):null;});
REPLACE: add _doctype derivation function before and set in forEach.

B) F object: add doctype:"".

C) HTML: add fh4/fp4 heading + select after fp3 block.

D) filter logic: add condition.

E) buildSelects: fill selDoc.

F) change listener: add selDoc mapping.

G) clearAll: reset doctype.

H) chips: add chip.

I) filterDesc in export: add.

J) tab03 checks mention per body etc — fine.

Doctype function:
function docType(r){
 if(r.mechanism==="Universal Periodic Review")return"UPR recommendations";
 if(/\/CO\//.test(r.symbol))return"Concluding observations";
 if(r.mechanism==="Special Procedures")return"Special Procedures report";
 return"Other document";
}

Now write the edit block carefully, matching exact lines from my file.

Filter condition insert in filtered(): add after body check:
    if(F.doctype&&r._doctype!==F.doctype)return false;

buildSelects add:
  const dts={};recs.forEach(r=>dts[r._doctype]=(dts[r._doctype]||0)+1);
  fillSel($("selDoc"),[{v:"",l:"all"}].concat(Object.keys(dts).sort().map(...)),F.doctype);

Listeners array: add "selDoc" to the map.

Chips: if(F.doctype)h+=chip(F.doctype,"doctype");

clearAll: F={...,doctype:"",...} — Object.assign line.

filterDesc: if(F.doctype)p.push(...).

HTML heading: after fp3 close div, before </div> of filterHeadings:
    <button class="fhead" id="fh4" aria-expanded="false" aria-controls="fp4"><span>04 Document type</span><span aria-hidden="true">+</span></button>
    <div class="fpanel" id="fp4" hidden>
      <label for="selDoc">Document type</label><select id="selDoc"></select>
      <div class="hint">Derived from the symbol and the mechanism: “/CO/” in the symbol = concluding observations; UPR mechanism = UPR recommendations.</div>
    </div>

onePanel uses array of three; need to include fh4/fp4. Edit onePanel array.

Also intro sentence: explain derived field since data lacks it.