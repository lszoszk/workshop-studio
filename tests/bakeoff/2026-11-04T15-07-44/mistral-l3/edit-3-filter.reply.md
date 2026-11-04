I'll add a "Document type" filter under the "02 Mechanism, body, type" heading. It will list the distinct values of the `type` field with their counts, and it will update when the mechanism changes.

```edit
<<<<<<< SEARCH
        <div id="type-filter-group">
          <label for="type-select">Type</label>
          <select id="type-select">
            <option value="all">All types</option>
          </select>
        </div>
        <div id="state-filter-group" hidden>
          <label for="state-select">Recommending State</label>
          <select id="state-select">
            <option value="all">All States</option>
          </select>
        </div>
=======
        <div id="type-filter-group">
          <label for="type-select">Type</label>
          <select id="type-select">
            <option value="all">All types</option>
          </select>
        </div>
        <div id="doc-type-filter-group">
          <label for="doc-type-select">Document type</label>
          <select id="doc-type-select">
            <option value="all">All document types</option>
          </select>
        </div>
        <div id="state-filter-group" hidden>
          <label for="state-select">Recommending State</label>
          <select id="state-select">
            <option value="all">All States</option>
          </select>
        </div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    document.getElementById('type-select').addEventListener('change', (e) => {
      filters.type = e.target.value;
      updateFilters();
    });
=======
    document.getElementById('type-select').addEventListener('change', (e) => {
      filters.type = e.target.value;
      updateFilters();
    });

    document.getElementById('doc-type-select').addEventListener('change', (e) => {
      filters.docType = e.target.value;
      updateFilters();
    });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  // Filters
  const filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    yearFrom: firstYear,
    yearTo: lastYear,
    sdg: 'all',
    state: 'all'
  };
=======
  // Filters
  const filters = {
    keyword: '',
    mechanism: 'all',
    body: 'all',
    type: 'all',
    docType: 'all',
    yearFrom: firstYear,
    yearTo: lastYear,
    sdg: 'all',
    state: 'all'
  };
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Type
      if (filters.type !== 'all' && record.type !== filters.type) {
        return false;
      }
=======
      // Type
      if (filters.type !== 'all' && record.type !== filters.type) {
        return false;
      }

      // Document type
      if (filters.docType !== 'all' && record.type !== filters.docType) {
        return false;
      }
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    if (filters.type !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Type: ${filters.type}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.type = 'all';
        document.getElementById('type-select').value = 'all';
        updateFilters();
      });
      chip.appendChild(button);
      activeFilters.appendChild(chip);
    }
=======
    if (filters.type !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Type: ${filters.type}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.type = 'all';
        document.getElementById('type-select').value = 'all';
        updateFilters();
      });
      chip.appendChild(button);
      activeFilters.appendChild(chip);
    }
    if (filters.docType !== 'all') {
      const chip = document.createElement('div');
      chip.className = 'chip';
      chip.textContent = `Document type: ${filters.docType}`;
      const button = document.createElement('button');
      button.textContent = '×';
      button.addEventListener('click', () => {
        filters.docType = 'all';
        document.getElementById('doc-type-select').value = 'all';
        updateFilters();
      });
      chip.appendChild(button);
      activeFilters.appendChild(chip);
    }
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
function populateFilters() {
    // Mechanism, body, type
    const mechanisms = [...new Set(records.map(r => r.mechanism))];
    const bodies = {};
    records.forEach(r => {
      if (!bodies[r.mechanism]) bodies[r.mechanism] = new Set();
      bodies[r.mechanism].add(r.body);
    });
    const types = [...new Set(records.map(r => r.type))];

    // Body select
    const bodySelect = document.getElementById('body-select');
    bodySelect.innerHTML = '<option value="all">All bodies</option>';
    Array.from(bodies['Universal Periodic Review'] || []).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.mechanism === 'Universal Periodic Review' && r.body === body).length})`;
      bodySelect.appendChild(option);
    });
    Array.from(bodies['Treaty bodies'] || []).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.mechanism === 'Treaty bodies' && r.body === body).length})`;
      bodySelect.appendChild(option);
    });
    Array.from(bodies['Special Procedures'] || []).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.mechanism === 'Special Procedures' && r.body === body).length})`;
      bodySelect.appendChild(option);
    });

    // Type select
    const typeSelect = document.getElementById('type-select');
    typeSelect.innerHTML = '<option value="all">All types</option>';
    types.forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = `${type} (${records.filter(r => r.type === type).length})`;
      typeSelect.appendChild(option);
    });
=======
function populateFilters() {
    // Mechanism, body, type, doc type
    const mechanisms = [...new Set(records.map(r => r.mechanism))];
    const bodies = {};
    records.forEach(r => {
      if (!bodies[r.mechanism]) bodies[r.mechanism] = new Set();
      bodies[r.mechanism].add(r.body);
    });
    const types = [...new Set(records.map(r => r.type))];

    // Body select
    const bodySelect = document.getElementById('body-select');
    bodySelect.innerHTML = '<option value="all">All bodies</option>';
    Array.from(bodies['Universal Periodic Review'] || []).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.mechanism === 'Universal Periodic Review' && r.body === body).length})`;
      bodySelect.appendChild(option);
    });
    Array.from(bodies['Treaty bodies'] || []).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.mechanism === 'Treaty bodies' && r.body === body).length})`;
      bodySelect.appendChild(option);
    });
    Array.from(bodies['Special Procedures'] || []).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.mechanism === 'Special Procedures' && r.body === body).length})`;
      bodySelect.appendChild(option);
    });

    // Type select
    const typeSelect = document.getElementById('type-select');
    typeSelect.innerHTML = '<option value="all">All types</option>';
    types.forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = `${type} (${records.filter(r => r.type === type).length})`;
      typeSelect.appendChild(option);
    });

    // Document type select
    const docTypeSelect = document.getElementById('doc-type-select');
    docTypeSelect.innerHTML = '<option value="all">All document types</option>';
    types.forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = `${type} (${records.filter(r => r.type === type).length})`;
      docTypeSelect.appendChild(option);
    });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
function updateBodyFilter() {
    const bodySelect = document.getElementById('body-select');
    bodySelect.innerHTML = '<option value="all">All bodies</option>';
    const mechanism = filters.mechanism === 'all' ? null : filters.mechanism;
    const bodies = new Set();
    records.forEach(r => {
      if (!mechanism || r.mechanism === mechanism) {
        bodies.add(r.body);
      }
    });
    Array.from(bodies).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.body === body && (!mechanism || r.mechanism === mechanism)).length})`;
      bodySelect.appendChild(option);
    });
    bodySelect.value = 'all';
    filters.body = 'all';
  }
=======
function updateBodyFilter() {
    const bodySelect = document.getElementById('body-select');
    bodySelect.innerHTML = '<option value="all">All bodies</option>';
    const mechanism = filters.mechanism === 'all' ? null : filters.mechanism;
    const bodies = new Set();
    records.forEach(r => {
      if (!mechanism || r.mechanism === mechanism) {
        bodies.add(r.body);
      }
    });
    Array.from(bodies).sort().forEach(body => {
      const option = document.createElement('option');
      option.value = body;
      option.textContent = `${body} (${records.filter(r => r.body === body && (!mechanism || r.mechanism === mechanism)).length})`;
      bodySelect.appendChild(option);
    });
    bodySelect.value = 'all';
    filters.body = 'all';

    // Update document type filter
    const docTypeSelect = document.getElementById('doc-type-select');
    docTypeSelect.innerHTML = '<option value="all">All document types</option>';
    const types = new Set();
    records.forEach(r => {
      if (!mechanism || r.mechanism === mechanism) {
        types.add(r.type);
      }
    });
    Array.from(types).sort().forEach(type => {
      const option = document.createElement('option');
      option.value = type;
      option.textContent = `${type} (${records.filter(r => r.type === type && (!mechanism || r.mechanism === mechanism)).length})`;
      docTypeSelect.appendChild(option);
    });
    docTypeSelect.value = 'all';
    filters.docType = 'all';
  }
>>>>>>> REPLACE
```

Now I'll clear the filter when the "Clear all" button is clicked:

```edit
<<<<<<< SEARCH
    clearFilters.addEventListener('click', () => {
      filters.keyword = '';
      filters.mechanism = 'all';
      filters.body = 'all';
      filters.type = 'all';
      filters.yearFrom = firstYear;
      filters.yearTo = lastYear;
      filters.sdg = 'all';
      filters.state = 'all';
      document.getElementById('keyword-input').value = '';
      document.querySelector('input[name="mechanism"][value="all"]').checked = true;
      document.getElementById('body-select').value = 'all';
      document.getElementById('type-select').value = 'all';
      document.getElementById('year-from').value = firstYear;
      document.getElementById('year-to').value = lastYear;
      document.getElementById('sdg-select').value = 'all';
      document.getElementById('state-select').value = 'all';
      updateFilters();
    });
=======
    clearFilters.addEventListener('click', () => {
      filters.keyword = '';
      filters.mechanism = 'all';
      filters.body = 'all';
      filters.type = 'all';
      filters.docType = 'all';
      filters.yearFrom = firstYear;
      filters.yearTo = lastYear;
      filters.sdg = 'all';
      filters.state = 'all';
      document.getElementById('keyword-input').value = '';
      document.querySelector('input[name="mechanism"][value="all"]').checked = true;
      document.getElementById('body-select').value = 'all';
      document.getElementById('type-select').value = 'all';
      document.getElementById('doc-type-select').value = 'all';
      document.getElementById('year-from').value = firstYear;
      document.getElementById('year-to').value = lastYear;
      document.getElementById('sdg-select').value = 'all';
      document.getElementById('state-select').value = 'all';
      updateFilters();
    });
>>>>>>> REPLACE
```