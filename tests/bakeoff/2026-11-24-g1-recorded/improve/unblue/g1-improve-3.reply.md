"Copy all" and "Download" now write each paragraph in quotation marks with its citation in brackets after it. [[fn:N]] footnote marks are left out of the copied and downloaded text, and the last line says so. The list on screen still shows the stored text.

```edit
<<<<<<< SEARCH
function draftText(){
  var parts=[];
  inDraft.forEach(function(v){parts.push(v.cite+'\n“'+v.text+'”');});
  return parts.join('\n\n')+'\n';
}
=======
function draftText(){
  var parts=[];
  inDraft.forEach(function(v){
    var clean=v.text.replace(/\s*\[\[fn:\d+\]\]/g,'');
    parts.push('“'+clean+'” ['+v.cite+']');
  });
  return parts.join('\n\n')+'\n\nFootnote marks such as [[fn:N]] were omitted from the quoted text.\n';
}
>>>>>>> REPLACE
```
