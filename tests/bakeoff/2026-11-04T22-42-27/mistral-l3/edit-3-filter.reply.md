I'll add a "Document type" filter under the "02 Mechanism, body, type" heading. This will let users filter by the specific type of document (e.g., "Concluding observations", "UPR recommendations") that appears in the `type` field.

```edit
<<<<<<< SEARCH
      <div class="filter-group">
        <fieldset>
          <legend>Type</legend>
          <label><input type="radio" name="type" value="all" checked/> All</label>
          <!-- Filled by script -->
        </fieldset>
      </div>
=======
      <div class="filter-group">
        <fieldset>
          <legend>Document type</legend>
          <label><input type="radio" name="type" value="all" checked/> All</label>
          <!-- Filled by script -->
        </fieldset>
      </div>
>>>>>>> REPLACE
```

Now I'll update the hint text in the method section to reflect this change:

```edit
<<<<<<< SEARCH
        <p>Filters: Mechanism, body and type match the field exactly. Year is inclusive between the two selects. SDG checks if the record's SDG list includes the goal number. Keyword matches every word as a substring of the text or symbol (case-insensitive). The filtered set feeds the tiles, charts, table and export.</p>
=======
        <p>Filters: Mechanism, body and document type match the field exactly. Year is inclusive between the two selects. SDG checks if the record's SDG list includes the goal number. Keyword matches every word as a substring of the text or symbol (case-insensitive). The filtered set feeds the tiles, charts, table and export.</p>
>>>>>>> REPLACE
```

The filter was already working correctly (the radio buttons for `type` were already being populated), I just changed the legend to be more descriptive as "Document type" instead of "Type". The functionality remains the same but the label is now clearer.