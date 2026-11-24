"Copy all" and "Download" now write each paragraph in quotation marks with its citation in brackets after it. Footnote marks such as [[fn:12]] are left out of the copied text, and a final line says that they were omitted.

```edit
<<<<<<< SEARCH
function draftText(){return draft.map(function(i){return recs[i].text+'\n— '+cite(recs[i]);}).join('\n\n');}
function renderDraft(){
=======
function draftText(){
  var body=draft.map(function(i){
    var t=String(recs[i].text==null?'':recs[i].text).replace(/\[\[fn:[^\]]*\]\]/g,'');
    return '“'+t+'” ['+cite(recs[i])+']';
  }).join('\n\n');
  return body+'\n\nFootnote marks were omitted.';
}
function renderDraft(){
>>>>>>> REPLACE
```
