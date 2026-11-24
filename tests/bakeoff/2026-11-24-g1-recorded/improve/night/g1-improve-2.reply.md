I added a "Data checks" line below the "paragraphs searched" count. It counts, from the loaded records, paragraphs with empty text, with no document link, with a duplicated id and with a footnote mark, and it shows every number even when it is 0.

```edit
<<<<<<< SEARCH
    <p class="mono searched" id="searched"></p>
    <p class="hint" id="how"></p>
=======
    <p class="mono searched" id="searched"></p>
    <p class="hint" id="checks"></p>
    <p class="hint" id="how"></p>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
$('searched').textContent=fmt(N)+' paragraphs searched';
var byC={};recs.forEach(function(r){var c=r.committee||'?';byC[c]=(byC[c]||0)+1;});
=======
$('searched').textContent=fmt(N)+' paragraphs searched';
var idc={};recs.forEach(function(r){if(r.id!=null)idc[r.id]=(idc[r.id]||0)+1;});
var cEmpty=0,cNoUrl=0,cDup=0,cFn=0;
recs.forEach(function(r){
  var t=String(r.text==null?'':r.text);
  if(!t.trim())cEmpty++;
  if(!r.doc_url)cNoUrl++;
  if(r.id!=null&&idc[r.id]>1)cDup++;
  if(/\[\[fn:[^\]]*\]\]/.test(t))cFn++;
});
$('checks').textContent='DATA CHECKS: empty text '+fmt(cEmpty)+' · no doc_url '+fmt(cNoUrl)+' · duplicated id '+fmt(cDup)+' · with a [[fn:N]] footnote mark '+fmt(cFn)+'. Counted from the loaded records.';
var byC={};recs.forEach(function(r){var c=r.committee||'?';byC[c]=(byC[c]||0)+1;});
>>>>>>> REPLACE
```
