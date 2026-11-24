"Copy all" and "Download" now write each paragraph in quotation marks with its citation in brackets after it. The [[fn:N]] footnote marks are left out of the copied text, and the last line says that footnote marks were omitted.

```edit
<<<<<<< SEARCH
function draftText(){
  var n = 0, parts = [];
  draft.forEach(function(d){ n++; parts.push('[' + n + '] ' + d.cit + '\n' + d.text); });
  return parts.join('\n\n') + (parts.length ? '\n' : '');
}
=======
function draftText(){
  var parts = [];
  draft.forEach(function(d){
    var clean = d.text.replace(/\s*\[\[fn:[^\]]*\]\]/g, '');
    parts.push('“' + clean + '” [' + d.cit + ']');
  });
  if(!parts.length) return '';
  return parts.join('\n\n') + '\n\nFootnote marks ([[fn:N]]) were omitted from the quoted text.\n';
}
>>>>>>> REPLACE
```
