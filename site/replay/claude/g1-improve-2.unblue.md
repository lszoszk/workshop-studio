I added a "Data checks" line under the paragraph count. It counts, from the loaded records, paragraphs with empty text, with no doc_url, with an id that occurs more than once, and with a [[fn:N]] footnote mark, and shows every number even when it is 0.

```edit
<<<<<<< SEARCH
    <span class="searched" id="searched"></span>
  </div>
=======
    <span class="searched" id="searched"></span>
  </div>
  <p class="how" id="checks"></p>
>>>>>>> REPLACE
<<<<<<< SEARCH
  $('searched').textContent=nf(recs.length)+' paragraphs searched';
})();

/* citations */
=======
  $('searched').textContent=nf(recs.length)+' paragraphs searched';
  var idCount={};
  recs.forEach(function(r){idCount[r.id]=(idCount[r.id]||0)+1;});
  var cEmpty=0,cNoUrl=0,cDup=0,cFn=0,fnRe=/\[\[fn:\d+\]\]/;
  recs.forEach(function(r){
    if(!String(r.text==null?'':r.text).trim())cEmpty++;
    if(!r.doc_url)cNoUrl++;
    if(idCount[r.id]>1)cDup++;
    if(fnRe.test(String(r.text==null?'':r.text)))cFn++;
  });
  $('checks').textContent='Data checks (counted over all '+nf(recs.length)+' loaded paragraphs): empty text '+nf(cEmpty)+' · no doc_url '+nf(cNoUrl)+' · duplicated id '+nf(cDup)+' · with a [[fn:N]] footnote mark '+nf(cFn);
})();

/* citations */
>>>>>>> REPLACE
```
