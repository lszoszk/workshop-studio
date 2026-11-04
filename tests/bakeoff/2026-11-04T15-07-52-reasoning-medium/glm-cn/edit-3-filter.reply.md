I'll add a fourth filter heading, "Document kind", derived from each record's symbol and mechanism (e.g. `/CO/` symbols are concluding observations, UPR records are UPR recommendations, Special Procedures records are mandate reports). It combines with the other filters by AND, shows as a removable chip, and feeds every tab and the export.

```edit
<<<<<<< SEARCH
const S = {kw:"", mech:"all", body:"all", type:"all", st:"all", yFrom:YEARS[0], yTo:YEARS[YEARS.length-1], sdg:"all", themes:[], sortDesc:true, page:1, tab:0, seed:1, sample:null, tally:null};
=======
const S = {kw:"", mech:"all", body:"all", type:"all", st:"all", doc:"all", yFrom:YEARS[0], yTo:YEARS[YEARS.length-1], sdg:"all", themes:[], sortDesc:true, page:1, tab:0, seed:1, sample:null, tally:null};
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
const mechColor = m => MECHCOLOR[m] || "#555";
=======
const mechColor = m => MECHCOLOR[m] || "#555";
function docKind(r){
  const s=r.symbol||"";
  if(s.includes("/CO/")) return "Concluding observations";
  if(r.mechanism==="Universal Periodic Review") return "UPR recommendations";
  if(r.mechanism==="Special Procedures") return "Special Procedures report";
  if(r.mechanism==="Treaty bodies") return "Other treaty-body document";
  return "Other";
}
const DOCKINDS = [...new Set(RECS.map(docKind))].sort();
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
    if(S.st!=="all" && !(STATES[i]||[]).includes(S.st)) return false;
=======
    if(S.st!=="all" && !(STATES[i]||[]).includes(S.st)) return false;
    if(S.doc!=="all" && docKind(r)!==S.doc) return false;
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  S.kw="";S.mech="all";S.body="all";S.type="all";S.st="all";S.sdg="all";S.themes=[];
=======
  S.kw="";S.mech="all";S.body="all";S.type="all";S.st="all";S.doc="all";S.sdg="all";S.themes=[];
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
      <label for="sdgsel">SDG goal (only those present)</label><select id="sdgsel"></select>
     </div></div>`;
=======
      <label for="sdgsel">SDG goal (only those present)</label><select id="sdgsel"></select>
     </div></div>
  <div class="acc"><button aria-expanded="false" data-acc="3">04 Document kind <span aria-hidden="true"></span></button>
    <div id="acc3body" hidden>
      <label for="docksel">Kind of document</label><select id="docksel"></select>
      <div class="hint">derived from the symbol and mechanism: “/CO/” symbols are concluding observations</div>
    </div></div>`;
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
  if(S.st!=="all")add(`State: ${S.st}`,()=>S.st="all");
=======
  if(S.st!=="all")add(`State: ${S.st}`,()=>S.st="all");
  if(S.doc!=="all")add(`document kind: ${S.doc}`,()=>S.doc="all");
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
      `# Filters: keyword="${S.kw.trim()}"; mechanism=${S.mech}; body=${S.body}; type=${S.type}; State=${S.st}; years=${S.yFrom}-${S.yTo}; SDG=${S.sdg}; themes=${S.themes.join(" | ")||"(none)"}`,
=======
      `# Filters: keyword="${S.kw.trim()}"; mechanism=${S.mech}; body=${S.body}; type=${S.type}; State=${S.st}; document kind=${S.doc}; years=${S.yFrom}-${S.yTo}; SDG=${S.sdg}; themes=${S.themes.join(" | ")||"(none)"}`,
>>>>>>> REPLACE
```


```edit
<<<<<<< SEARCH
function refresh(){
  buildAcc1();
  drawMatch();
=======
function buildAcc3(){
  const sel=document.getElementById("docksel");
  const kc=new Map(); RECS.forEach(r=>kc.set(docKind(r),(kc.get(docKind(r))||0)+1));
  sel.innerHTML=`<option value="all">all kinds (${fmt(RECS.length)})</option>`+
    DOCKINDS.map(k=>`<option value="${esc(k)}"${S.doc===k?" selected":""}>${esc(k)} (${fmt(kc.get(k)||0)})</option>`).join("");
  sel.addEventListener("change",e=>{S.doc=e.target.value;S.page=1;refresh();});
}
function refresh(){
  buildAcc1();
  buildAcc3();
  drawMatch();
>>>>>>> REPLACE
```