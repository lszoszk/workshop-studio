"Copy all" and "Download" now write each paragraph in quotation marks, followed by its citation in square brackets. The [[fn:N]] footnote marks are left out of that text, and one final line says so.

```edit
<<<<<<< SEARCH
  function draftText(){
    return draft.map(function(id){
      var r = byId.get(id);
      return r.text + '\n' + cite(r);
    }).join('\n\n');
  }
=======
  function draftText(){
    var body = draft.map(function(id){
      var r = byId.get(id);
      return '“' + String(r.text || '').replace(/\[\[fn:\d+\]\]/g, '') + '” [' + cite(r) + ']';
    }).join('\n\n');
    return body + '\n\nFootnote marks [[fn:N]] were omitted from the quoted text.';
  }
>>>>>>> REPLACE
```
