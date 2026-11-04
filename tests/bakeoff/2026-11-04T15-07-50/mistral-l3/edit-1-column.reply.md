Here’s the edit: I added a **Year** column after Date, and made it sortable (numeric, newest first). The sort icon now toggles between the two columns.

```edit
<<<<<<< SEARCH
          <tr>
            <th id="sort-date">Date <span id="sort-icon">↓</span></th>
            <th>Body</th>
            <th>Symbol</th>
            <th>Para.</th>
            <th>First line</th>
            <th>Recommending State</th>
          </tr>
=======
          <tr>
            <th id="sort-date">Date <span id="sort-icon">↓</span></th>
            <th id="sort-year">Year</th>
            <th>Body</th>
            <th>Symbol</th>
            <th>Para.</th>
            <th>First line</th>
            <th>Recommending State</th>
          </tr>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
        tr.innerHTML = `
          <td>${date}</td>
          <td>${body}</td>
          <td><a href="${docUrl}" target="_blank">${symbol}</a></td>
          <td>${para}</td>
          <td>${highlightedFirstLine}</td>
          <td>${state}</td>
        `;
=======
        tr.innerHTML = `
          <td>${date}</td>
          <td>${record.year}</td>
          <td>${body}</td>
          <td><a href="${docUrl}" target="_blank">${symbol}</a></td>
          <td>${para}</td>
          <td>${highlightedFirstLine}</td>
          <td>${state}</td>
        `;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Sort
      const sortedRecords = [...filteredRecords].sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        if (dateA > dateB) return sortDirection === 'desc' ? -1 : 1;
        if (dateA < dateB) return sortDirection === 'desc' ? 1 : -1;
        if (a.body < b.body) return -1;
        if (a.body > b.body) return 1;
        const paraA = a.paragraphNumber || '';
        const paraB = b.paragraphNumber || '';
        return paraA.localeCompare(paraB, undefined, { numeric: true });
      });
=======
      // Sort
      let sortedRecords;
      if (sortColumn === 'date') {
        sortedRecords = [...filteredRecords].sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          if (dateA > dateB) return sortDirection === 'desc' ? -1 : 1;
          if (dateA < dateB) return sortDirection === 'desc' ? 1 : -1;
          if (a.body < b.body) return -1;
          if (a.body > b.body) return 1;
          const paraA = a.paragraphNumber || '';
          const paraB = b.paragraphNumber || '';
          return paraA.localeCompare(paraB, undefined, { numeric: true });
        });
      } else { // year
        sortedRecords = [...filteredRecords].sort((a, b) => {
          if (a.year > b.year) return sortDirection === 'desc' ? -1 : 1;
          if (a.year < b.year) return sortDirection === 'desc' ? 1 : -1;
          if (a.body < b.body) return -1;
          if (a.body > b.body) return 1;
          const paraA = a.paragraphNumber || '';
          const paraB = b.paragraphNumber || '';
          return paraA.localeCompare(paraB, undefined, { numeric: true });
        });
      }
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    let sortDirection = 'desc';
=======
    let sortDirection = 'desc';
    let sortColumn = 'date';
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Sort
      sortDate.addEventListener('click', () => {
        sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
        sortIcon.textContent = sortDirection === 'desc' ? '↓' : '↑';
        updateTable();
      });
=======
      // Sort
      sortDate.addEventListener('click', () => {
        if (sortColumn === 'date') {
          sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
        } else {
          sortColumn = 'date';
          sortDirection = 'desc';
        }
        sortIcon.textContent = sortDirection === 'desc' ? '↓' : '↑';
        yearSortIcon.textContent = '';
        updateTable();
      });

      sortYear.addEventListener('click', () => {
        if (sortColumn === 'year') {
          sortDirection = sortDirection === 'desc' ? 'asc' : 'desc';
        } else {
          sortColumn = 'year';
          sortDirection = 'desc';
        }
        yearSortIcon.textContent = sortDirection === 'desc' ? '↓' : '↑';
        sortIcon.textContent = '';
        updateTable();
      });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    const sortDate = document.getElementById('sort-date');
    const sortIcon = document.getElementById('sort-icon');
=======
    const sortDate = document.getElementById('sort-date');
    const sortIcon = document.getElementById('sort-icon');
    const sortYear = document.getElementById('sort-year');
    const yearSortIcon = document.createElement('span');
    sortYear.appendChild(yearSortIcon);
>>>>>>> REPLACE
```