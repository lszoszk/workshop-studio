"Copy all" and "Download" now write each paragraph in quotation marks, with its citation in brackets after it. The [[fn:N]] footnote marks are left out of the copied text, and the last line says so. The draft list on screen is unchanged.

```edit
<<<<<<< SEARCH
  function draftText(){
    return draft.map(function(r){ return '“' + r.text + '”\n' + citation(r); }).join('\n\n');
  }
=======
  function draftText(){
    var body = draft.map(function(r){
      var t = String(r.text == null ? '' : r.text).replace(/\s*\[\[fn:\d+\]\]/g, '');
      return '“' + t + '” [' + citation(r) + ']';
    }).join('\n\n');
    return body + '\n\nFootnote marks ([[fn:N]]) were omitted from the quoted text.';
  }
>>>>>>> REPLACE
```
