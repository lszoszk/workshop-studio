Here’s the edit: I added a "Year" column after "Date" in the records table, and made it sortable like the others.

```edit
<<<<<<< SEARCH
          <thead>
            <tr>
              <th id="sort-date">Date</th>
              <th>Body</th>
              <th>Symbol</th>
              <th>Para.</th>
              <th>First line</th>
              <th id="state-column">Recommending State</th>
              <th></th>
            </tr>
          </thead>
=======
          <thead>
            <tr>
              <th id="sort-date">Date</th>
              <th id="sort-year">Year</th>
              <th>Body</th>
              <th>Symbol</th>
              <th>Para.</th>
              <th>First line</th>
              <th id="state-column">Recommending State</th>
              <th></th>
            </tr>
          </thead>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      const tr = document.createElement('tr');
      tr.tabIndex = 0;
      tr.innerHTML = `
        <td>${r.date}</td>
        <td>${r.body}</td>
        <td><a href="${r.doc_url}" target="_blank">${r.symbol}</a></td>
        <td>${r.paraNumber || '–'}</td>
        <td class="first-line">${highlightKeywords(r.firstLine)}</td>
        <td class="state">${r.state === '–' ? '<span class="state-dash">–</span>' : r.state}</td>
        <td class="expand-row"><button>+</button></td>
      `;
=======
      const tr = document.createElement('tr');
      tr.tabIndex = 0;
      tr.innerHTML = `
        <td>${r.date}</td>
        <td>${r.year}</td>
        <td>${r.body}</td>
        <td><a href="${r.doc_url}" target="_blank">${r.symbol}</a></td>
        <td>${r.paraNumber || '–'}</td>
        <td class="first-line">${highlightKeywords(r.firstLine)}</td>
        <td class="state">${r.state === '–' ? '<span class="state-dash">–</span>' : r.state}</td>
        <td class="expand-row"><button>+</button></td>
      `;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      if (recordsSort.column === 'date') {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return recordsSort.direction === 'asc' ? dateA - dateB : dateB - dateA;
      }
      if (recordsSort.column === 'body') {
        return recordsSort.direction === 'asc' ? a.body.localeCompare(b.body) : b.body.localeCompare(a.body);
      }
      if (recordsSort.column === 'symbol') {
        return recordsSort.direction === 'asc' ? a.symbol.localeCompare(b.symbol) : b.symbol.localeCompare(a.symbol);
      }
      if (recordsSort.column === 'para') {
        const aPara = a.paraNumber || '';
        const bPara = b.paraNumber || '';
        return recordsSort.direction === 'asc' ? aPara.localeCompare(bPara) : bPara.localeCompare(aPara);
      }
      if (recordsSort.column === 'state') {
        return recordsSort.direction === 'asc' ? a.state.localeCompare(b.state) : b.state.localeCompare(a.state);
      }
=======
      if (recordsSort.column === 'date') {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return recordsSort.direction === 'asc' ? dateA - dateB : dateB - dateA;
      }
      if (recordsSort.column === 'year') {
        return recordsSort.direction === 'asc' ? a.year - b.year : b.year - a.year;
      }
      if (recordsSort.column === 'body') {
        return recordsSort.direction === 'asc' ? a.body.localeCompare(b.body) : b.body.localeCompare(a.body);
      }
      if (recordsSort.column === 'symbol') {
        return recordsSort.direction === 'asc' ? a.symbol.localeCompare(b.symbol) : b.symbol.localeCompare(a.symbol);
      }
      if (recordsSort.column === 'para') {
        const aPara = a.paraNumber || '';
        const bPara = b.paraNumber || '';
        return recordsSort.direction === 'asc' ? aPara.localeCompare(bPara) : bPara.localeCompare(aPara);
      }
      if (recordsSort.column === 'state') {
        return recordsSort.direction === 'asc' ? a.state.localeCompare(b.state) : b.state.localeCompare(a.state);
      }
>>>>>>> REPLACE
```