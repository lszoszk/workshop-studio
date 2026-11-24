I added a short plain-words intro under the title. It says the search covers every General Comment of every committee in the file, not only those on children, and lists the three steps.

```edit
<<<<<<< SEARCH
.src{margin:0 0 4px;color:var(--soft);font-size:14px}
a{color:var(--ink)}
=======
.src{margin:0 0 4px;color:var(--soft);font-size:14px}
.intro{margin:14px 0 0;max-width:72ch;font-size:16px}
.intro p{margin:0 0 6px}
.intro ol{margin:0;padding-left:22px}
.intro li{margin:2px 0}
a{color:var(--ink)}
>>>>>>> REPLACE
<<<<<<< SEARCH
  <p class="src" id="src"></p>
</header>
=======
  <p class="src" id="src"></p>
  <div class="intro">
    <p>This search covers all the General Comments of every committee in the file, not only those on children. Three steps:</p>
    <ol>
      <li>Type a phrase, or put it in quotation marks.</li>
      <li>Compare the highlighted paragraph with the original: click its symbol.</li>
      <li>Copy the citation.</li>
    </ol>
  </div>
</header>
>>>>>>> REPLACE
```
