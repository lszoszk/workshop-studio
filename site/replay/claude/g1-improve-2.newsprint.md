I added a "Data checks" line under the "paragraphs searched" count. It counts, from the loaded records, the paragraphs with empty text, with no doc_url, with a duplicated id and with a [[fn:N]] footnote mark, and shows each number even when it is 0.

```edit
<<<<<<< SEARCH
    </div>
    <p class="how" id="how">How this is computed: your code compares every paragraph in the file with what you typed. Nothing is estimated.</p>
=======
    </div>
    <p class="how" id="checks"></p>
    <p class="how" id="how">How this is computed: your code compares every paragraph in the file with what you typed. Nothing is estimated.</p>
>>>>>>> REPLACE
<<<<<<< SEARCH
  $('src').textContent = parts.join(' · ');
  $('searched').textContent = fmt(recs.length);
=======
  $('src').textContent = parts.join(' · ');
  $('searched').textContent = fmt(recs.length);
  var seen = new Map();
  recs.forEach(function(r){ seen.set(r.id, (seen.get(r.id) || 0) + 1); });
  var txt = function(r){ return String(r.text == null ? '' : r.text); };
  var chk = {
    empty: recs.filter(function(r){ return !txt(r).trim(); }).length,
    nourl: recs.filter(function(r){ return !r.doc_url; }).length,
    dup: recs.filter(function(r){ return r.id != null && seen.get(r.id) > 1; }).length,
    fn: recs.filter(function(r){ return /\[\[fn:[^\]]*\]\]/.test(txt(r)); }).length
  };
  $('checks').textContent = 'Data checks (paragraphs counted from the loaded records): empty text ' + fmt(chk.empty) +
    ' · no doc_url ' + fmt(chk.nourl) + ' · duplicated id ' + fmt(chk.dup) + ' · with a [[fn:N]] footnote mark ' + fmt(chk.fn);
>>>>>>> REPLACE
```
