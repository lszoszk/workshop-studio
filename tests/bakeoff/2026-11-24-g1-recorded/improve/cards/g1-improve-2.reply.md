I added a "Data checks" line right under the count of paragraphs searched. It counts, over all loaded records, empty texts, missing doc_url, paragraphs whose id appears more than once, and paragraphs with a [[fn:N]] mark, and shows every number even when it is 0.

```edit
<<<<<<< SEARCH
      </div>
      <p class="label how" id="how">How this is computed: each paragraph is tested in the browser against every word you typed; nothing is sent anywhere.</p>
=======
      </div>
      <p class="label checks" id="checks"></p>
      <p class="label how" id="how">How this is computed: each paragraph is tested in the browser against every word you typed; nothing is sent anywhere.</p>
>>>>>>> REPLACE
<<<<<<< SEARCH
  $('searched').textContent = fmt(records.length) + ' paragraphs searched';

  // ---- query parsing and matching
=======
  $('searched').textContent = fmt(records.length) + ' paragraphs searched';

  // ---- data checks, counted over all loaded records
  (function(){
    var idCount = {}, empty = 0, noUrl = 0, dup = 0, fn = 0, fnRe = /\[\[fn:\d+\]\]/;
    records.forEach(function(r){
      if (r.id != null && r.id !== '') idCount[r.id] = (idCount[r.id] || 0) + 1;
    });
    records.forEach(function(r){
      if (r.text == null || String(r.text).trim() === '') empty++;
      if (!r.doc_url) noUrl++;
      if (r.id != null && r.id !== '' && idCount[r.id] > 1) dup++;
      if (r.text != null && fnRe.test(String(r.text))) fn++;
    });
    $('checks').textContent = 'Data checks (all ' + fmt(records.length) + ' paragraphs loaded): ' +
      fmt(empty) + ' with empty text · ' + fmt(noUrl) + ' with no doc_url · ' +
      fmt(dup) + ' with a duplicated id (shared with another paragraph) · ' +
      fmt(fn) + ' with a [[fn:N]] footnote mark';
  })();

  // ---- query parsing and matching
>>>>>>> REPLACE
```
