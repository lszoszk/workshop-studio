I'll add a filter for document type (the `type` field) to the left rail, under the existing "Mechanism, body, type" section. Here's the edit:

```edit
<<<<<<< SEARCH
        <div class="filter-label">Type</div>
        <div class="filter-radio-group" id="type-radio"></div>

        <div id="state-filter-container" hidden>
=======
        <div class="filter-label">Type</div>
        <div class="filter-radio-group" id="type-radio"></div>

        <div class="filter-label">Document type</div>
        <div class="filter-radio-group" id="doc-type-radio"></div>

        <div id="state-filter-container" hidden>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      const typeRadio = document.getElementById('type-radio');
      const stateFilterContainer = document.getElementById('state-filter-container');
      const stateSelect = document.getElementById('state-select');
=======
      const typeRadio = document.getElementById('type-radio');
      const docTypeRadio = document.getElementById('doc-type-radio');
      const stateFilterContainer = document.getElementById('state-filter-container');
      const stateSelect = document.getElementById('state-select');
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Type
      const types = ['', ...new Set(records.map(r => r.type))];
      types.forEach(t => {
        const radio = document.createElement('label');
        radio.className = 'filter-radio';
        radio.innerHTML = `
          <input type="radio" name="type" value="${t}" ${t === '' ? 'checked' : ''}>
          <span>${t || 'All types'}</span>
        `;
        typeRadio.appendChild(radio);
      });
=======
      // Type (recommendation, concern, etc.)
      const types = ['', ...new Set(records.map(r => r.type))];
      types.forEach(t => {
        const radio = document.createElement('label');
        radio.className = 'filter-radio';
        radio.innerHTML = `
          <input type="radio" name="type" value="${t}" ${t === '' ? 'checked' : ''}>
          <span>${t || 'All types'}</span>
        `;
        typeRadio.appendChild(radio);
      });

      // Document type (concluding observations, UPR recommendations, etc.)
      const docTypes = ['', ...new Set(records.map(r => {
        if (r.mechanism === 'Universal Periodic Review') return 'UPR recommendations';
        if (r.mechanism === 'Treaty bodies' && r.type === 'Recommendations') return 'Concluding observations';
        if (r.mechanism === 'Treaty bodies' && r.type === 'Concerns/Observations') return 'Concluding observations';
        if (r.mechanism === 'Special Procedures') return 'Special Procedures reports';
        return r.type;
      }))].filter((v, i, self) => self.indexOf(v) === i);

      docTypes.forEach(dt => {
        const radio = document.createElement('label');
        radio.className = 'filter-radio';
        radio.innerHTML = `
          <input type="radio" name="doc-type" value="${dt}" ${dt === '' ? 'checked' : ''}>
          <span>${dt || 'All document types'}</span>
        `;
        docTypeRadio.appendChild(radio);
      });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      document.querySelectorAll('input[name="type"]').forEach(radio => {
        radio.addEventListener('change', () => {
          activeFilters.type = radio.value;
          updateFilters();
        });
      });
=======
      document.querySelectorAll('input[name="type"]').forEach(radio => {
        radio.addEventListener('change', () => {
          activeFilters.type = radio.value;
          updateFilters();
        });
      });

      document.querySelectorAll('input[name="doc-type"]').forEach(radio => {
        radio.addEventListener('change', () => {
          activeFilters.docType = radio.value;
          updateFilters();
        });
      });
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Type
      if (activeFilters.type && record.type !== activeFilters.type) return false;
=======
      // Type
      if (activeFilters.type && record.type !== activeFilters.type) return false;

      // Document type
      if (activeFilters.docType) {
        if (activeFilters.docType === 'UPR recommendations' && record.mechanism !== 'Universal Periodic Review') return false;
        if (activeFilters.docType === 'Concluding observations' && !(record.mechanism === 'Treaty bodies' && (record.type === 'Recommendations' || record.type === 'Concerns/Observations'))) return false;
        if (activeFilters.docType === 'Special Procedures reports' && record.mechanism !== 'Special Procedures') return false;
      }
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      if (activeFilters.type) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Type: ${activeFilters.type}
          <button class="filter-chip-remove" aria-label="Remove type filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          document.querySelector('input[name="type"][value=""]').checked = true;
          delete activeFilters.type;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
=======
      if (activeFilters.type) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Type: ${activeFilters.type}
          <button class="filter-chip-remove" aria-label="Remove type filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          document.querySelector('input[name="type"][value=""]').checked = true;
          delete activeFilters.type;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }

      if (activeFilters.docType) {
        const chip = document.createElement('div');
        chip.className = 'filter-chip';
        chip.innerHTML = `
          Document type: ${activeFilters.docType}
          <button class="filter-chip-remove" aria-label="Remove document type filter">×</button>
        `;
        chip.querySelector('.filter-chip-remove').addEventListener('click', () => {
          document.querySelector('input[name="doc-type"][value=""]').checked = true;
          delete activeFilters.docType;
          updateFilters();
        });
        filterChips.appendChild(chip);
      }
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      delete activeFilters.type;
=======
      delete activeFilters.type;
      delete activeFilters.docType;
>>>>>>> REPLACE
```