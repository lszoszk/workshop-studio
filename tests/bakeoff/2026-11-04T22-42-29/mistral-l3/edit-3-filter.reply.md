I'll add a filter for the document type (the `type` field) to the "Mechanism, body, type" section in the left rail. This will let users filter by "Recommendations", "Concerns/Observations", or "Other".

```edit
<<<<<<< SEARCH
        <div class="checkbox-group" style="margin-top: 1rem;">
          <div class="checkbox-item">
            <input type="radio" id="type-all" name="type" value="all" checked>
            <label for="type-all">All types (<span id="type-all-count"></span>)</label>
          </div>
          <!-- Filled by script -->
        </div>
=======
        <div class="checkbox-group" style="margin-top: 1rem;">
          <div style="font-family: var(--mono); font-size: 0.8rem; letter-spacing: 0.05em; color: #666; margin-bottom: 0.3rem;">TYPE</div>
          <div class="checkbox-item">
            <input type="radio" id="type-all" name="type" value="all" checked>
            <label for="type-all">All types (<span id="type-all-count"></span>)</label>
          </div>
          <!-- Filled by script -->
        </div>
>>>>>>> REPLACE
```

The type filter is already implemented in the code (it's filled by the script in the `init()` function), so I only need to add a heading to make it clearer in the UI. The existing code already handles the type filtering logic.