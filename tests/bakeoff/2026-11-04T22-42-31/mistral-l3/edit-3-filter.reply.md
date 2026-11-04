I'll add a "Type" filter to the "02 MECHANISM, BODY, TYPE" section in the left rail. Here's the edit:

```edit
<<<<<<< SEARCH
      <div>
        <div style="font-size: 0.9rem; margin-bottom: 0.4rem;">Type</div>
        <div class="radio-group" id="type-radio-group">
          <label><input type="radio" name="type" value="all" checked/> All</label>
        </div>
      </div>
=======
      <div>
        <div style="font-size: 0.9rem; margin-bottom: 0.4rem;">Type</div>
        <div class="radio-group" id="type-radio-group">
          <label><input type="radio" name="type" value="all" checked/> All</label>
        </div>
      </div>
      <div id="document-type-filter-container" style="margin-top: 1rem;">
        <div style="font-size: 0.9rem; margin-bottom: 0.4rem;">Document type</div>
        <select id="document-type-select">
          <option value="all">All</option>
        </select>
      </div>
>>>>>>> REPLACE
```

Now I'll add the JavaScript to populate and handle this new filter:

```edit
<<<<<<< SEARCH
  <div id="state-filter-container" style="margin-top: 1rem;">
    <div style="font-size: 0.9rem; margin-bottom: 0.4rem;">Recommending State (UPR only)</div>
    <select id="state-select">
      <option value="all">All</option>
    </select>
  </div>
=======
  <div id="document-type-filter-container" style="margin-top: 1rem;">
    <div style="font-size: 0.9rem; margin-bottom: 0.4rem;">Document type</div>
    <select id="document-type-select">
      <option value="all">All</option>
    </select>
  </div>
  <div id="state-filter-container" style="margin-top: 1rem;">
    <div style="font-size: 0.9rem; margin-bottom: 0.4rem;">Recommending State (UPR only)</div>
    <select id="state-select">
      <option value="all">All</option>
    </select>
  </div>
>>>>>>> REPLACE
```

Now I'll update the filters object and add the logic to populate and handle the document type filter:

```edit
<<<<<<< SEARCH
let filters = {
  keyword: '',
  mechanism: 'all',
  body: 'all',
  type: 'all',
  state: 'all',
  yearFrom: '',
  yearTo: '',
  sdg: 'all'
};
=======
let filters = {
  keyword: '',
  mechanism: 'all',
  body: 'all',
  type: 'all',
  documentType: 'all',
  state: 'all',
  yearFrom: '',
  yearTo: '',
  sdg: 'all'
};
>>>>>>> REPLACE
```

Now I'll add the function to update the document type filter and call it in the initialization:

```edit
<<<<<<< SEARCH
function updateStateFilter() {
  const stateSelect = document.getElementById('state-select');
  stateSelect.innerHTML = '<option value="all">All</option>';
  const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
  const stateCounts = {};
  uprRecords.forEach(record => {
    const states = extractStates(record.text);
    states.forEach(state => {
      stateCounts[state] = (stateCounts[state] || 0) + 1;
    });
  });
  const states = Object.keys(stateCounts).sort();
  states.forEach(state => {
    const option = document.createElement('option');
    option.value = state;
    option.textContent = `${state} (${stateCounts[state]})`;
    stateSelect.appendChild(option);
  });
  stateSelect.addEventListener('change', (e) => {
    filters.state = e.target.value;
    updateFilters();
  });
}
=======
function updateDocumentTypeFilter() {
  const documentTypeSelect = document.getElementById('document-type-select');
  documentTypeSelect.innerHTML = '<option value="all">All</option>';

  // Extract document types from symbols
  const documentTypes = {};
  records.forEach(record => {
    // Common patterns for document types
    let docType = 'Other';
    const symbol = record.symbol;

    if (symbol.includes('/CO/')) docType = 'Concluding observations';
    else if (symbol.includes('/GC/')) docType = 'General Comment';
    else if (symbol.includes('/REC/')) docType = 'Recommendations';
    else if (symbol.includes('/SP/')) docType = 'Special Procedures report';
    else if (record.mechanism === 'Universal Periodic Review') docType = 'UPR recommendations';
    else if (record.type === 'Recommendations') docType = 'Recommendations';
    else if (record.type === 'Concerns/Observations') docType = 'Concerns/Observations';

    documentTypes[docType] = (documentTypes[docType] || 0) + 1;
  });

  const types = Object.keys(documentTypes).sort();
  types.forEach(type => {
    const option = document.createElement('option');
    option.value = type;
    option.textContent = `${type} (${documentTypes[type]})`;
    documentTypeSelect.appendChild(option);
  });

  documentTypeSelect.addEventListener('change', (e) => {
    filters.documentType = e.target.value;
    updateFilters();
  });
}

function updateStateFilter() {
  const stateSelect = document.getElementById('state-select');
  stateSelect.innerHTML = '<option value="all">All</option>';
  const uprRecords = records.filter(r => r.mechanism === 'Universal Periodic Review');
  const stateCounts = {};
  uprRecords.forEach(record => {
    const states = extractStates(record.text);
    states.forEach(state => {
      stateCounts[state] = (stateCounts[state] || 0) + 1;
    });
  });
  const states = Object.keys(stateCounts).sort();
  states.forEach(state => {
    const option = document.createElement('option');
    option.value = state;
    option.textContent = `${state} (${stateCounts[state]})`;
    stateSelect.appendChild(option);
  });
  stateSelect.addEventListener('change', (e) => {
    filters.state = e.target.value;
    updateFilters();
  });
}
>>>>>>> REPLACE
```

Now I need to update the filter logic to include the document type filter:

```edit
<<<<<<< SEARCH
  filteredRecords = records.filter(record => {
    if (filters.keyword) {
      const words = filters.keyword.toLowerCase().split(/\s+/).filter(w => w);
      if (!words.every(w => record.text.toLowerCase().includes(w) || record.symbol.toLowerCase().includes(w))) {
        return false;
      }
    }
    if (filters.mechanism !== 'all' && record.mechanism !== filters.mechanism) return false;
    if (filters.body !== 'all' && record.body !== filters.body) return false;
    if (filters.type !== 'all' && record.type !== filters.type) return false;
    if (filters.state !== 'all' && record.mechanism === 'Universal Periodic Review') {
      const states = extractStates(record.text);
      if (!states.includes(filters.state)) return false;
    }
    if (filters.yearFrom && record.year < parseInt(filters.yearFrom)) return false;
    if (filters.yearTo && record.year > parseInt(filters.yearTo)) return false;
    if (filters.sdg !== 'all') {
      const goal = parseInt(filters.sdg);
      if (!record.sdgs || !record.sdgs.includes(goal)) return false;
    }
    return true;
  });
=======
  filteredRecords = records.filter(record => {
    if (filters.keyword) {
      const words = filters.keyword.toLowerCase().split(/\s+/).filter(w => w);
      if (!words.every(w => record.text.toLowerCase().includes(w) || record.symbol.toLowerCase().includes(w))) {
        return false;
      }
    }
    if (filters.mechanism !== 'all' && record.mechanism !== filters.mechanism) return false;
    if (filters.body !== 'all' && record.body !== filters.body) return false;
    if (filters.type !== 'all' && record.type !== filters.type) return false;
    if (filters.documentType !== 'all') {
      let docType = 'Other';
      const symbol = record.symbol;

      if (symbol.includes('/CO/')) docType = 'Concluding observations';
      else if (symbol.includes('/GC/')) docType = 'General Comment';
      else if (symbol.includes('/REC/')) docType = 'Recommendations';
      else if (symbol.includes('/SP/')) docType = 'Special Procedures report';
      else if (record.mechanism === 'Universal Periodic Review') docType = 'UPR recommendations';
      else if (record.type === 'Recommendations') docType = 'Recommendations';
      else if (record.type === 'Concerns/Observations') docType = 'Concerns/Observations';

      if (docType !== filters.documentType) return false;
    }
    if (filters.state !== 'all' && record.mechanism === 'Universal Periodic Review') {
      const states = extractStates(record.text);
      if (!states.includes(filters.state)) return false;
    }
    if (filters.yearFrom && record.year < parseInt(filters.yearFrom)) return false;
    if (filters.yearTo && record.year > parseInt(filters.yearTo)) return false;
    if (filters.sdg !== 'all') {
      const goal = parseInt(filters.sdg);
      if (!record.sdgs || !record.sdgs.includes(goal)) return false;
    }
    return true;
  });
>>>>>>> REPLACE
```

Now I need to update the active filters display to show the document type filter:

```edit
<<<<<<< SEARCH
  if (filters.type !== 'all') {
    const chip = document.createElement('div');
    chip.className = 'filter-chip';
    chip.innerHTML = `Type: ${filters.type} <button aria-label="Remove type filter">&times;</button>`;
    chip.querySelector('button').addEventListener('click', () => {
      filters.type = 'all';
      document.querySelector('input[name="type"][value="all"]').checked = true;
      updateFilters();
      renderTab();
    });
    activeFiltersEl.appendChild(chip);
  }
=======
  if (filters.type !== 'all') {
    const chip = document.createElement('div');
    chip.className = 'filter-chip';
    chip.innerHTML = `Type: ${filters.type} <button aria-label="Remove type filter">&times;</button>`;
    chip.querySelector('button').addEventListener('click', () => {
      filters.type = 'all';
      document.querySelector('input[name="type"][value="all"]').checked = true;
      updateFilters();
      renderTab();
    });
    activeFiltersEl.appendChild(chip);
  }
  if (filters.documentType !== 'all') {
    const chip = document.createElement('div');
    chip.className = 'filter-chip';
    chip.innerHTML = `Document type: ${filters.documentType} <button aria-label="Remove document type filter">&times;</button>`;
    chip.querySelector('button').addEventListener('click', () => {
      filters.documentType = 'all';
      document.getElementById('document-type-select').value = 'all';
      updateFilters();
      renderTab();
    });
    activeFiltersEl.appendChild(chip);
  }
>>>>>>> REPLACE
```

Finally, I need to call the update function in the initialization:

```edit
<<<<<<< SEARCH
updateBodyFilter();
updateTypeFilter();
updateStateFilter();
updateYearSdgFilters();
updateFilters();
switchTab('01');
=======
updateBodyFilter();
updateTypeFilter();
updateDocumentTypeFilter();
updateStateFilter();
updateYearSdgFilters();
updateFilters();
switchTab('01');
>>>>>>> REPLACE
```

And I need to update the clear filters function:

```edit
<<<<<<< SEARCH
document.getElementById('clear-filters').addEventListener('click', () => {
  filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    state: 'all',
    yearFrom: '',
    yearTo: '',
    sdg: 'all'
  };
=======
document.getElementById('clear-filters').addEventListener('click', () => {
  filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    documentType: 'all',
    state: 'all',
    yearFrom: '',
    yearTo: '',
    sdg: 'all'
  };
>>>>>>> REPLACE
```

Now let's test the complete implementation by updating the initialization section:

```edit
<<<<<<< SEARCH
  document.querySelector('input[name="type"][value="all"]').checked = true;
  document.getElementById('state-select').value = 'all';
  document.getElementById('year-from-select').value = '';
  document.getElementById('year-to-select').value = '';
  document.getElementById('sdg-select').value = 'all';
=======
  document.querySelector('input[name="type"][value="all"]').checked = true;
  document.getElementById('document-type-select').value = 'all';
  document.getElementById('state-select').value = 'all';
  document.getElementById('year-from-select').value = '';
  document.getElementById('year-to-select').value = '';
  document.getElementById('sdg-select').value = 'all';
>>>>>>> REPLACE
```