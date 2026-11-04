Here is the edit: I added a Year column after Date, made it sortable, and kept the existing sort on Date descending as the default.

```edit
<<<<<<< SEARCH
      <thead>
        <tr>
          <th scope="col" id="col-date" aria-sort="descending">Date</th>
          <th scope="col">Body</th>
          <th scope="col">Symbol</th>
          <th scope="col">Para.</th>
          <th scope="col">First line</th>
          <th scope="col" id="col-state">Recommending State</th>
        </tr>
      </thead>
=======
      <thead>
        <tr>
          <th scope="col" id="col-date" aria-sort="descending">Date</th>
          <th scope="col" id="col-year">Year</th>
          <th scope="col">Body</th>
          <th scope="col">Symbol</th>
          <th scope="col">Para.</th>
          <th scope="col">First line</th>
          <th scope="col" id="col-state">Recommending State</th>
        </tr>
      </thead>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      const date = new Date(record.date);
      const dateStr = date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

      let firstLineHtml = firstLine;
      if (searchTerm) {
        const keywords = searchTerm.split(/\s+/);
        keywords.forEach(kw => {
          if (kw) {
            firstLineHtml = firstLineHtml.replace(new RegExp(kw, 'gi'), match => `<mark>${match}</mark>`);
          }
        });
      }

      tr.innerHTML = `
        <td>${dateStr}</td>
        <td>${record.body}</td>
        <td><a href="${record.doc_url}" target="_blank">${record.symbol}</a></td>
        <td>${paraNum || '–'}</td>
        <td class="highlight">${firstLineHtml}</td>
        <td class="state">${state}</td>
      `;
=======
      const date = new Date(record.date);
      const dateStr = date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
      const yearStr = record.year;

      let firstLineHtml = firstLine;
      if (searchTerm) {
        const keywords = searchTerm.split(/\s+/);
        keywords.forEach(kw => {
          if (kw) {
            firstLineHtml = firstLineHtml.replace(new RegExp(kw, 'gi'), match => `<mark>${match}</mark>`);
          }
        });
      }

      tr.innerHTML = `
        <td>${dateStr}</td>
        <td>${yearStr}</td>
        <td>${record.body}</td>
        <td><a href="${record.doc_url}" target="_blank">${record.symbol}</a></td>
        <td>${paraNum || '–'}</td>
        <td class="highlight">${firstLineHtml}</td>
        <td class="state">${state}</td>
      `;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    // Sort
    const sortDirection = colDate.getAttribute('aria-sort');
    visibleRecords.sort((a, b) => {
      if (sortDirection === 'descending') {
        if (a.date > b.date) return -1;
        if (a.date < b.date) return 1;
      } else {
        if (a.date < b.date) return -1;
        if (a.date > b.date) return 1;
      }
      if (a.body < b.body) return -1;
      if (a.body > b.body) return 1;
      const aPara = extractParagraphNumber(a.text);
      const bPara = extractParagraphNumber(b.text);
      if (aPara && bPara) {
        return aPara.localeCompare(bPara, undefined, { numeric: true });
      }
      if (aPara) return -1;
      if (bPara) return 1;
      return 0;
    });
=======
    // Sort
    const dateSort = colDate.getAttribute('aria-sort');
    const yearSort = colYear.getAttribute('aria-sort');
    visibleRecords.sort((a, b) => {
      // Year sort takes precedence
      if (yearSort !== 'none') {
        if (yearSort === 'descending') {
          if (a.year > b.year) return -1;
          if (a.year < b.year) return 1;
        } else {
          if (a.year < b.year) return -1;
          if (a.year > b.year) return 1;
        }
      }
      // Then date sort
      if (dateSort === 'descending') {
        if (a.date > b.date) return -1;
        if (a.date < b.date) return 1;
      } else if (dateSort === 'ascending') {
        if (a.date < b.date) return -1;
        if (a.date > b.date) return 1;
      }
      // Then body, paragraph
      if (a.body < b.body) return -1;
      if (a.body > b.body) return 1;
      const aPara = extractParagraphNumber(a.text);
      const bPara = extractParagraphNumber(b.text);
      if (aPara && bPara) {
        return aPara.localeCompare(bPara, undefined, { numeric: true });
      }
      if (aPara) return -1;
      if (bPara) return 1;
      return 0;
    });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    colDate.addEventListener('click', () => {
      const current = colDate.getAttribute('aria-sort');
      const newSort = current === 'ascending' ? 'descending' : 'ascending';
      colDate.setAttribute('aria-sort', newSort);
      updateRecords();
    });
=======
    const colYear = document.getElementById('col-year');
    colDate.addEventListener('click', () => {
      const current = colDate.getAttribute('aria-sort');
      const newSort = current === 'ascending' ? 'descending' : 'ascending';
      colDate.setAttribute('aria-sort', newSort);
      colYear.setAttribute('aria-sort', 'none');
      updateRecords();
    });

    colYear.addEventListener('click', () => {
      const current = colYear.getAttribute('aria-sort');
      const newSort = current === 'ascending' ? 'descending' : 'ascending';
      colYear.setAttribute('aria-sort', newSort);
      colDate.setAttribute('aria-sort', 'none');
      updateRecords();
    });
>>>>>>> REPLACE
```