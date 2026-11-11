I will count the records whose text contains "torture" or "ill-treatment" (case-insensitive, also "ill treatment", "illtreatment" and "ill-treated"), and show how many fall under each mechanism in each year, restricted to records of type "Recommendations".

```query
const d = WORKSHOP_DATA.uhri;
const recs = (d && d.records) || [];
const re = /torture|ill[\s\-]?treat/i;
const hit = recs.filter(r => r.type === "Recommendations" && re.test(r.text || ""));
const mechs = Array.from(new Set(hit.map(r => r.mechanism || "(none)"))).sort();
const years = Array.from(new Set(hit.map(r => r.year))).sort((a, b) => a - b);
const rows = years.map(y => {
  const counts = mechs.map(m => hit.filter(r => r.year === y && (r.mechanism || "(none)") === m).length);
  return [y, ...counts, counts.reduce((a, b) => a + b, 0)];
});
const totals = mechs.map(m => hit.filter(r => (r.mechanism || "(none)") === m).length);
rows.push(["Total", ...totals, hit.length]);
return {
  title: "Recommendations mentioning torture or ill-treatment, by mechanism and year (" + (d ? d.country : "") + ")",
  columns: ["Year", ...mechs, "All mechanisms"],
  rows: rows.slice(0, 200),
  note: "Counted records with type exactly \"Recommendations\" whose text matches (case-insensitive) \"torture\" or \"ill-treat…\" / \"ill treat…\" / \"illtreat…\"; synonyms such as \"cruel, inhuman or degrading\" are not matched, and Concerns/Observations are left out. Years are the document's year."
};
```