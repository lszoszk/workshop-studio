I added a "Data checks" line under the "Paragraphs searched" count. It counts, from the loaded records, paragraphs with empty text, with no doc_url, with a duplicated id (every record that shares its id with another) and with a [[fn:N]] mark, and shows each number even when it is 0.

```edit
<<<<<<< SEARCH
    <div class="stat"><span class="mono muted">Paragraphs searched</span><span class="num" id="nsearched">0</span></div>
  </div>
=======
    <div class="stat"><span class="mono muted">Paragraphs searched</span><span class="num" id="nsearched">0</span>
      <span class="mono muted" id="checks" style="display:block;margin-top:6px;text-transform:none"></span></div>
  </div>
>>>>>>> REPLACE
<<<<<<< SEARCH
  $('source').textContent = (DATA.source ? DATA.source + ' · ' : '') + 'n = ' + fmt(recs.length) + ' paragraphs · ' + committees.size + ' committees · ' + yr;
  $('nsearched').textContent = fmt(recs.length);
=======
  $('source').textContent = (DATA.source ? DATA.source + ' · ' : '') + 'n = ' + fmt(recs.length) + ' paragraphs · ' + committees.size + ' committees · ' + yr;
  $('nsearched').textContent = fmt(recs.length);

  var idCount = new Map(), cEmpty = 0, cNoUrl = 0, cDup = 0, cFn = 0;
  recs.forEach(function(r){ idCount.set(r.id, (idCount.get(r.id) || 0) + 1); });
  recs.forEach(function(r){
    var tx = String(r.text || '');
    if(!tx.trim()) cEmpty++;
    if(!r.doc_url) cNoUrl++;
    if(idCount.get(r.id) > 1) cDup++;
    if(/\[\[fn:\d+\]\]/.test(tx)) cFn++;
  });
  $('checks').textContent = 'Data checks: empty text ' + fmt(cEmpty) + ' · no doc_url ' + fmt(cNoUrl) + ' · duplicated id ' + fmt(cDup) + ' · with [[fn:N]] mark ' + fmt(cFn);
>>>>>>> REPLACE
```
