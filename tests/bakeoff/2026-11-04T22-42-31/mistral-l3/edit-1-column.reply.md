Here’s the edit: I added a Year column after Date, and made it sortable by clicking its header. The column shows the `year` field, and the sort toggles between ascending and descending.

```edit
<<<<<<< SEARCH
      <tr>
        <th scope="col">Date</th>
        <th scope="col">Body</th>
        <th scope="col">Symbol</th>
        <th scope="col">Para.</th>
        <th scope="col">First line</th>
        <th scope="col">Recommending State</th>
      </tr>
=======
      <tr>
        <th scope="col">Date</th>
        <th scope="col">Year</th>
        <th scope="col">Body</th>
        <th scope="col">Symbol</th>
        <th scope="col">Para.</th>
        <th scope="col">First line</th>
        <th scope="col">Recommending State</th>
      </tr>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    tr.innerHTML = `
      <td>${date}</td>
      <td>${record.body}</td>
      <td><a href="${record.doc_url}" target="_blank">${record.symbol}</a></td>
      <td>${para || '—'}</td>
      <td>${firstLineHtml}</td>
      <td>${states}</td>
    `;
=======
    tr.innerHTML = `
      <td>${date}</td>
      <td>${record.year}</td>
      <td>${record.body}</td>
      <td><a href="${record.doc_url}" target="_blank">${record.symbol}</a></td>
      <td>${para || '—'}</td>
      <td>${firstLineHtml}</td>
      <td>${states}</td>
    `;
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
// Table sort
document.querySelector('#records-table th:nth-child(1)').addEventListener('click', () => {
  const th = document.querySelector('#records-table th:nth-child(1)');
  const isAsc = th.getAttribute('aria-sort') === 'ascending';
  th.setAttribute('aria-sort', isAsc ? 'descending' : 'ascending');
  filteredRecords.sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return isAsc ? dateA - dateB : dateB - dateA;
  });
  currentPage = 0;
  renderTable();
});
=======
// Table sort
document.querySelector('#records-table th:nth-child(1)').addEventListener('click', () => {
  const th = document.querySelector('#records-table th:nth-child(1)');
  const isAsc = th.getAttribute('aria-sort') === 'ascending';
  th.setAttribute('aria-sort', isAsc ? 'descending' : 'ascending');
  document.querySelector('#records-table th:nth-child(2)').setAttribute('aria-sort', 'none');
  filteredRecords.sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return isAsc ? dateA - dateB : dateB - dateA;
  });
  currentPage = 0;
  renderTable();
});

document.querySelector('#records-table th:nth-child(2)').addEventListener('click', () => {
  const th = document.querySelector('#records-table th:nth-child(2)');
  const isAsc = th.getAttribute('aria-sort') === 'ascending';
  th.setAttribute('aria-sort', isAsc ? 'descending' : 'ascending');
  document.querySelector('#records-table th:nth-child(1)').setAttribute('aria-sort', 'none');
  filteredRecords.sort((a, b) => {
    return isAsc ? a.year - b.year : b.year - a.year;
  });
  currentPage = 0;
  renderTable();
});
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
document.querySelector('#records-table th:nth-child(1)').addEventListener('click', () => {
=======
document.querySelector('#records-table th:nth-child(1)').addEventListener('click', function() {
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
document.querySelector('#records-table th:nth-child(2)').addEventListener('click', () => {
=======
document.querySelector('#records-table th:nth-child(2)').addEventListener('click', function() {
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
document.querySelector('#records-table th:nth-child(1)').addEventListener('click', function() {
  const th = document.querySelector('#records-table th:nth-child(1)');
  const isAsc = th.getAttribute('aria-sort') === 'ascending';
  th.setAttribute('aria-sort', isAsc ? 'descending' : 'ascending');
  document.querySelector('#records-table th:nth-child(2)').setAttribute('aria-sort', 'none');
  filteredRecords.sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return isAsc ? dateA - dateB : dateB - dateA;
  });
  currentPage = 0;
  renderTable();
});

document.querySelector('#records-table th:nth-child(2)').addEventListener('click', function() {
  const th = document.querySelector('#records-table th:nth-child(2)');
  const isAsc = th.getAttribute('aria-sort') === 'ascending';
  th.setAttribute('aria-sort', isAsc ? 'descending' : 'ascending');
  document.querySelector('#records-table th:nth-child(1)').setAttribute('aria-sort', 'none');
  filteredRecords.sort((a, b) => {
    return isAsc ? a.year - b.year : b.year - a.year;
  });
  currentPage = 0;
  renderTable();
});
=======
function setSort(columnIndex, compareFn) {
  const th = document.querySelector(`#records-table th:nth-child(${columnIndex})`);
  const isAsc = th.getAttribute('aria-sort') === 'ascending';
  document.querySelectorAll('#records-table th[aria-sort]').forEach(th => {
    th.setAttribute('aria-sort', 'none');
  });
  th.setAttribute('aria-sort', isAsc ? 'descending' : 'ascending');
  filteredRecords.sort(compareFn(isAsc));
  currentPage = 0;
  renderTable();
}

document.querySelector('#records-table th:nth-child(1)').addEventListener('click', function() {
  setSort(1, (isAsc) => (a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return isAsc ? dateA - dateB : dateB - dateA;
  });
});

document.querySelector('#records-table th:nth-child(2)').addEventListener('click', function() {
  setSort(2, (isAsc) => (a, b) => isAsc ? a.year - b.year : b.year - a.year);
});
>>>>>>> REPLACE
```