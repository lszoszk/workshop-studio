Write single HTML app. Keep under 700 lines. Implement query parser: tokens: quoted phrases, AND/OR/NOT uppercase keywords? Spec: words combined with AND unless you write OR; NOT excludes. Treat uppercase AND/OR/NOT as operators; example shows `"best interests" AND child`. I'll treat AND, OR, NOT (case-insensitive, standalone) as operators. Grammar: expression → OR of AND groups; each AND group items are terms or NOT term. Evaluate per record.

Highlighting: wrap matched words/phrases with <mark>. Build highlight regex from all positive terms (whole word, escaped), also highlight inside NOT terms? No—only matched words that caused inclusion, i.e., positive terms. Simpler: highlight positive terms.

Chart with Chart.js, bar chart per committee, update on search.

Sorting: newest year first; tie-breaker maybe by symbol/paragraph — keep stable, sort by year desc, then title.

Copy citation via navigator.clipboard with fallback (execCommand).

Write code.