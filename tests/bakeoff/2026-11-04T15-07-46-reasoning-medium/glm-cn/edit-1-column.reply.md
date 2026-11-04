I added a Year column between Date and Body, and made its header clickable to sort by year (ascending/descending), keeping date, body, paragraph and file order as tie-breakers. The expanded row now spans seven columns.

```edit
<<<<<<< SEARCH
      <thead><tr><th scope="col" id="thdate" style="cursor:pointer" title="Click to reverse order">Date ↑↓</th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead>
=======
      <thead><tr><th scope="col" id="thdate" style="cursor:pointer" title="Click to reverse order">Date ↑↓</th><th scope="col" id="thyear" style="cursor:pointer" title="Click to sort by year">Year ↑↓</th><th scope="col">Body</th><th scope="col">Symbol</th><th scope="col" class="num">Para.</th><th scope="col">First line</th><th scope="col">Recommending State</th></tr></thead>
>>>>>>> REPLACE
```