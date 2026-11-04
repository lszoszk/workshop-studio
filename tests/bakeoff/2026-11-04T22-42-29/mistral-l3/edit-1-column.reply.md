Here is the edit: I added a Year column after Date, made it sortable, and updated the table header and the row rendering.

```edit
<<<<<<< SEARCH
            <th scope="col" class="sortable" id="sort-date">Date</th>
            <th scope="col">Body</th>
            <th scope="col">Symbol</th>
            <th scope="col">Para.</th>
            <th scope="col">Recommending State</th>
            <th scope="col">First line</th>
=======
            <th scope="col" class="sortable" id="sort-date">Date</th>
            <th scope="col" class="sortable" id="sort-year">Year</th>
            <th scope="col">Body</th>
            <th scope="col">Symbol</th>
            <th scope="col">Para.</th>
            <th scope="col">Recommending State</th>
            <th scope="col">First line</th>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Sort
      tableRecords.sort((a, b) => {
        if (currentSort.column === 'date') {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return currentSort.direction === 'asc' ? dateA - dateB : dateB - dateA;
        }
        return 0;
      });
=======
      // Sort
      tableRecords.sort((a, b) => {
        if (currentSort.column === 'date') {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return currentSort.direction === 'asc' ? dateA - dateB : dateB - dateA;
        } else if (currentSort.column === 'year') {
          return currentSort.direction === 'asc' ? a.year - b.year : b.year - a.year;
        }
        return 0;
      });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
        const date = new Date(r.date).toLocaleDateString('en-CA');
        const symbol = `<a href="${r.doc_url}" target="_blank">${r.symbol}</a>`;
        const para = r.paragraphNumber || '–';
        const state = r.recommendingState?.length ? r.recommendingState.join(', ') : '–';
=======
        const date = new Date(r.date).toLocaleDateString('en-CA');
        const year = r.year;
        const symbol = `<a href="${r.doc_url}" target="_blank">${r.symbol}</a>`;
        const para = r.paragraphNumber || '–';
        const state = r.recommendingState?.length ? r.recommendingState.join(', ') : '–';
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
            <td>${date}</td>
            <td>${r.body}</td>
            <td>${symbol}</td>
            <td>${para}</td>
            <td>${state}</td>
            <td>${firstLine}</td>
=======
            <td>${date}</td>
            <td>${year}</td>
            <td>${r.body}</td>
            <td>${symbol}</td>
            <td>${para}</td>
            <td>${state}</td>
            <td>${firstLine}</td>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Sort
      document.getElementById('sort-date').addEventListener('click', () => {
        currentSort = {
          column: 'date',
          direction: currentSort.direction === 'asc' ? 'desc' : 'asc'
        };
        document.querySelectorAll('.sortable').forEach(th => {
          th.classList.remove('sorted-asc', 'sorted-desc');
        });
        document.getElementById('sort-date').classList.add(`sorted-${currentSort.direction}`);
        updateRecordsTable();
      });
=======
      // Sort
      document.getElementById('sort-date').addEventListener('click', () => {
        currentSort = {
          column: 'date',
          direction: currentSort.direction === 'asc' ? 'desc' : 'asc'
        };
        document.querySelectorAll('.sortable').forEach(th => {
          th.classList.remove('sorted-asc', 'sorted-desc');
        });
        document.getElementById('sort-date').classList.add(`sorted-${currentSort.direction}`);
        updateRecordsTable();
      });

      document.getElementById('sort-year').addEventListener('click', () => {
        currentSort = {
          column: 'year',
          direction: currentSort.direction === 'asc' ? 'desc' : 'asc'
        };
        document.querySelectorAll('.sortable').forEach(th => {
          th.classList.remove('sorted-asc', 'sorted-desc');
        });
        document.getElementById('sort-year').classList.add(`sorted-${currentSort.direction}`);
        updateRecordsTable();
      });
>>>>>>> REPLACE
```