Build the app per the plan. Two tabs, left rail, header, footer, checks, exports. Keep under ~1500 lines. Write carefully.

Key pieces:
- Parse HTML, walk body.querySelectorAll('table, p, h2, h3'), classify.
- Repairs with logging.
- First words check with normalization.
- Exports JSON/Markdown via Blob.
- Tabs with arrow keys, role=tablist.
- Expanded rows.
- Check panel.

Let me write it.