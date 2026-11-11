/* A participant's own files: a spreadsheet (CSV, Excel), a data file (JSON) or a Word document, read here in
   the browser and kept in it (IndexedDB), never uploaded. The app gets the whole file as WORKSHOP_DATA.own_<n>;
   the model gets the line describe() writes: the fields and their types, and sample records only when the
   participant ticks the box. Excel and Word files are zip archives of XML: unzipped with the browser's own
   DecompressionStream, so nothing is loaded from the internet. */
window.OwnFiles = (function () {
  'use strict';
  const MAX_BYTES = 10 * 1024 * 1024;
  const SAMPLES = 3;
  const KINDS = { csv: 'csv', tsv: 'csv', txt: 'csv', json: 'json', xlsx: 'xlsx', docx: 'docx' };
  const NOUN = { csv: 'spreadsheet', xlsx: 'Excel workbook', json: 'data file', docx: 'Word document' };

  /* ---------- reading ---------- */

  async function read(file, key) {
    const ext = (file.name.split('.').pop() || '').toLowerCase();
    const kind = KINDS[ext];
    if (ext === 'xls' || ext === 'doc') throw new Error(`"${file.name}" is in the old ${ext === 'xls' ? 'Excel' : 'Word'} format. Open it and save it as .${ext}x, then add it again.`);
    if (!kind) throw new Error(`"${file.name}" is not a file the studio can read: use a spreadsheet (.csv, .xlsx), a data file (.json) or a Word document (.docx).`);
    if (file.size > MAX_BYTES) throw new Error(`"${file.name}" is ${(file.size / 1048576).toFixed(1)} MB; the studio takes files up to 10 MB.`);
    const buf = await file.arrayBuffer();
    const base = { dataset: key, title: file.name, source: 'Added by the participant from their own computer; kept in this browser' };
    let data, note = '';
    if (kind === 'csv') {
      const { text, encoding } = decode(buf);
      if (encoding !== 'utf-8') note = 'Read as Western European text (the file is not in UTF-8).';
      data = table(base, parseCSV(text));
    } else if (kind === 'json') {
      let parsed;
      try { parsed = JSON.parse(decode(buf).text); } catch (e) { throw new Error(`"${file.name}" is not valid JSON: ${e.message}`); }
      data = Array.isArray(parsed) ? Object.assign({}, base, { count: parsed.length, records: parsed }) : parsed;
    } else if (kind === 'xlsx') {
      const sheets = await readXlsx(buf);
      const first = sheets.find((s) => s.rows.length) || sheets[0];
      if (!first) throw new Error(`"${file.name}" has no sheets.`);
      data = table(base, first.rows);
      data.sheet = first.name;
      if (sheets.length > 1) {
        data.sheets = {};
        sheets.forEach((s) => { data.sheets[s.name] = table({}, s.rows).records; });
        note = `${sheets.length} sheets; \`records\` is "${first.name}", every sheet is in \`sheets\`.`;
      }
    } else {
      data = Object.assign(base, await readDocx(buf));
    }
    const text = JSON.stringify(data);
    return { key, name: file.name, kind, size: file.size, added: new Date().toISOString(), samples: false, note, text, shape: shape(data) };
  }

  function decode(buf) {
    try { return { text: new TextDecoder('utf-8', { fatal: true }).decode(buf).replace(/^﻿/, ''), encoding: 'utf-8' }; } catch (e) {
      return { text: new TextDecoder('windows-1252').decode(buf), encoding: 'windows-1252' };
    }
  }

  // rows (arrays) -> records under a header row: empty names become column_<n>, repeated ones get _2, _3
  function table(base, rows) {
    rows = rows.filter((r) => r.some((c) => c !== null && c !== ''));
    const head = (rows.shift() || []).map((h, i) => String(h == null ? '' : h).trim() || `column_${i + 1}`);
    const width = Math.max(head.length, ...rows.map((r) => r.length));
    for (let i = head.length; i < width; i++) head.push(`column_${i + 1}`);
    const seen = {};
    const fields = head.map((h) => { seen[h] = (seen[h] || 0) + 1; return seen[h] > 1 ? `${h}_${seen[h]}` : h; });
    const records = rows.map((r) => Object.fromEntries(fields.map((f, i) => [f, r[i] === undefined || r[i] === '' ? null : r[i]])));
    return Object.assign({}, base, { count: records.length, fields, records });
  }

  function parseCSV(text) {
    const line = text.slice(0, (text.indexOf('\n') + 1 || text.length + 1) - 1);
    const outside = line.replace(/"[^"]*"/g, '');
    const delim = [',', ';', '\t'].map((d) => [d, outside.split(d).length]).sort((a, b) => b[1] - a[1])[0][0];
    const rows = [];
    let row = [], cell = '', q = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) {
        if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c;
      } else if (c === '"' && cell === '') q = true;
      else if (c === delim) { row.push(cell); cell = ''; }
      else if (c === '\n' || c === '\r') {
        if (c === '\r' && text[i + 1] === '\n') i++;
        row.push(cell); rows.push(row); row = []; cell = '';
      } else cell += c;
    }
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    // a plain number becomes a number; "007" and "1,5" stay text
    return rows.map((r) => r.map((s) => (/^-?(0|[1-9]\d*)(\.\d+)?$/.test(s.trim()) ? Number(s.trim()) : s)));
  }

  /* ---------- zip archives (Excel, Word) ---------- */

  async function unzip(buf) {
    const v = new DataView(buf), u8 = new Uint8Array(buf);
    let e = buf.byteLength - 22;
    while (e >= 0 && v.getUint32(e, true) !== 0x06054b50) e--;
    if (e < 0) throw new Error('The file is damaged or not an Office file.');
    const entries = {};
    let p = v.getUint32(e + 16, true);
    for (let i = 0, n = v.getUint16(e + 10, true); i < n; i++) {
      const nlen = v.getUint16(p + 28, true);
      entries[new TextDecoder().decode(u8.subarray(p + 46, p + 46 + nlen))] =
        { method: v.getUint16(p + 10, true), size: v.getUint32(p + 20, true), off: v.getUint32(p + 42, true) };
      p += 46 + nlen + v.getUint16(p + 30, true) + v.getUint16(p + 32, true);
    }
    return {
      has: (name) => name in entries,
      async xml(name) {
        const f = entries[name];
        if (!f) return null;
        const start = f.off + 30 + v.getUint16(f.off + 26, true) + v.getUint16(f.off + 28, true);
        let bytes = u8.subarray(start, start + f.size);
        if (f.method === 8) bytes = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).arrayBuffer());
        else if (f.method !== 0) throw new Error('The file uses a compression the studio cannot read.');
        return new DOMParser().parseFromString(new TextDecoder().decode(bytes), 'application/xml');
      },
    };
  }

  const tags = (node, name) => [...node.getElementsByTagName(name)];
  const attr = (el, name) => (el ? el.getAttribute(name) : null);

  async function readXlsx(buf) {
    const z = await unzip(buf);
    const book = await z.xml('xl/workbook.xml');
    if (!book) throw new Error('The file is not an Excel workbook.');
    const rels = await z.xml('xl/_rels/workbook.xml.rels');
    const target = {};
    if (rels) tags(rels, 'Relationship').forEach((r) => { target[attr(r, 'Id')] = attr(r, 'Target').replace(/^\/?(xl\/)?/, 'xl/'); });
    const sst = await z.xml('xl/sharedStrings.xml');
    // the text of a shared string, without its phonetic guide (rPh)
    const strings = sst ? tags(sst, 'si').map((si) => tags(si, 't').filter((t) => t.parentNode.nodeName !== 'rPh').map((t) => t.textContent).join('')) : [];
    const dates = await dateStyles(z);
    const sheets = [];
    for (const s of tags(book, 'sheet')) {
      const doc = await z.xml(target[attr(s, 'r:id')] || `xl/worksheets/sheet${sheets.length + 1}.xml`);
      if (!doc) continue;
      const rows = [];
      tags(doc, 'row').forEach((r) => {
        const out = [];
        tags(r, 'c').forEach((c, j) => {
          const ref = attr(c, 'r');
          const col = ref ? colIndex(ref) : j;
          const t = attr(c, 't'), vEl = c.getElementsByTagName('v')[0], raw = vEl ? vEl.textContent : null;
          let val = null;
          if (t === 's') val = raw == null ? null : strings[Number(raw)];
          else if (t === 'inlineStr') val = tags(c, 't').map((x) => x.textContent).join('');
          else if (t === 'b') val = raw === '1';
          else if (t === 'str' || t === 'e') val = raw;
          else if (raw != null && raw !== '') {
            val = Number(raw);
            if (dates.has(Number(attr(c, 's') || 0))) val = excelDate(val);
          }
          out[col] = val;
        });
        rows[Number(attr(r, 'r') || rows.length + 1) - 1] = Array.from(out, (x) => (x === undefined ? null : x));
      });
      sheets.push({ name: attr(s, 'name'), rows: Array.from(rows, (r) => r || []) });
    }
    return sheets;
  }

  const colIndex = (ref) => [...ref.replace(/\d+$/, '')].reduce((n, ch) => n * 26 + ch.charCodeAt(0) - 64, 0) - 1;

  // the cell styles whose number format is a date: built-in formats 14-22 and 45-47, and custom ones with d, m or y
  async function dateStyles(z) {
    const st = await z.xml('xl/styles.xml');
    const out = new Set();
    if (!st) return out;
    const custom = {};
    tags(st, 'numFmt').forEach((f) => {
      const code = (attr(f, 'formatCode') || '').replace(/"[^"]*"|\[[^\]]*\]|\\./g, '');
      custom[attr(f, 'numFmtId')] = /[dmy]/i.test(code);
    });
    const xfs = st.getElementsByTagName('cellXfs')[0];
    if (xfs) tags(xfs, 'xf').forEach((xf, i) => {
      const id = Number(attr(xf, 'numFmtId') || 0);
      if ((id >= 14 && id <= 22) || (id >= 45 && id <= 47) || custom[id]) out.add(i);
    });
    return out;
  }

  function excelDate(serial) {
    const d = new Date(Date.UTC(1899, 11, 30) + Math.round(serial * 86400000));
    const iso = d.toISOString();
    return serial % 1 ? iso.slice(0, 16).replace('T', ' ') : iso.slice(0, 10);
  }

  async function readDocx(buf) {
    const z = await unzip(buf);
    const doc = await z.xml('word/document.xml');
    if (!doc) throw new Error('The file is not a Word document.');
    const body = doc.getElementsByTagName('w:body')[0];
    const records = [];
    // paragraphs in document order, also those inside tables and content controls
    const visit = (node, inTable) => {
      for (const el of node.children) {
        if (el.nodeName === 'w:p') para(el, inTable);
        else if (el.nodeName === 'w:tbl') visit(el, true);
        else if (['w:tr', 'w:tc', 'w:sdt', 'w:sdtContent', 'w:customXml', 'w:ins'].includes(el.nodeName)) visit(el, inTable);
      }
    };
    const para = (p, inTable) => {
      let text = '';
      const notes = [];
      const walk = (n) => {
        for (const el of n.children) {
          const name = el.nodeName;
          if (name === 'w:pPr' || name === 'w:del' || name === 'w:rPr') continue;
          if (name === 'w:t') text += el.textContent;
          else if (name === 'w:tab') text += '\t';
          else if (name === 'w:br' || name === 'w:cr') text += '\n';
          else if (name === 'w:noBreakHyphen') text += '‑';
          else if (name === 'w:footnoteReference') notes.push(Number(attr(el, 'w:id')));
          else walk(el);
        }
      };
      walk(p);
      if (!text.trim()) return;
      const style = attr(p.getElementsByTagName('w:pStyle')[0], 'w:val') || 'Normal';
      const outline = p.getElementsByTagName('w:outlineLvl').length > 0;
      records.push({ n: records.length + 1, style, heading: outline || /^(heading|title|subtitle|berschrift|titre|t[ií]tulo|nag)/i.test(style),
        text: text.trim(), in_table: inTable, footnotes: notes });
    };
    if (body) visit(body, false);
    const notes = async (file, tag) => {
      const x = await z.xml(file);
      if (!x) return [];
      return tags(x, tag).filter((f) => !attr(f, 'w:type') || attr(f, 'w:type') === 'normal')
        .map((f) => ({ id: Number(attr(f, 'w:id')), text: tags(f, 'w:t').map((t) => t.textContent).join('').trim() }));
    };
    const footnotes = await notes('word/footnotes.xml', 'w:footnote');
    const endnotes = await notes('word/endnotes.xml', 'w:endnote');
    return Object.assign({ count: records.length, records, footnotes }, endnotes.length ? { endnotes } : {});
  }

  /* ---------- what the model is told ---------- */

  const typeOf = (v) => (v === null || v === undefined ? null : Array.isArray(v) ? 'list' : typeof v === 'object' ? 'object' :
    typeof v === 'string' && /^\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?$/.test(v) ? 'date' : typeof v === 'number' ? 'number' : typeof v === 'boolean' ? 'yes/no' : 'text');

  // where the records are (the top level, or the largest list of objects in it), and each field's types
  function shape(data) {
    let path = null, list = Array.isArray(data) ? data : null;
    if (data && Array.isArray(data.records)) { path = 'records'; list = data.records; }   // the studio's own shape
    if (!list && data && typeof data === 'object') {
      for (const [k, v] of Object.entries(data)) {
        if (Array.isArray(v) && v.length && typeof v[0] === 'object' && (!list || v.length > list.length)) { path = k; list = v; }
      }
    }
    const fields = {};
    (list || []).forEach((r) => {
      if (!r || typeof r !== 'object' || Array.isArray(r)) return;
      Object.entries(r).forEach(([k, v]) => {
        const f = fields[k] || (fields[k] = { name: k, types: new Set(), empty: 0 });
        const t = typeOf(v);
        if (t) f.types.add(t); else f.empty++;
      });
    });
    const top = data && typeof data === 'object' && !Array.isArray(data) ?
      Object.entries(data).filter(([k]) => k !== path).map(([k, v]) => ({ name: k, type: typeOf(v) || 'empty', length: Array.isArray(v) ? v.length : null })) : [];
    return { path, count: list ? list.length : 0, top,
      fields: Object.values(fields).map((f) => ({ name: f.name, types: [...f.types], empty: f.empty })) };
  }

  function describe(entry, label) {
    const s = entry.shape;
    const where = s.path ? `\`WORKSHOP_DATA.${entry.key}.${s.path}\`` : `\`WORKSHOP_DATA.${entry.key}\` itself`;
    const fields = s.fields.map((f) => `\`${f.name}\` (${f.types.join(' or ') || 'always empty'}${f.empty && f.types.length ? `, ${f.empty} empty` : ''})`).join(', ');
    const top = s.top.map((t) => `\`${t.name}\` (${t.type}${t.length != null ? `, ${t.length} items` : ''})`).join(', ');
    const lines = [
      `(Attached: ${label} → WORKSHOP_DATA.${entry.key}. The participant added this ${NOUN[entry.kind]} from their own computer; the system prompt does not describe it, this note does.`,
      s.count ? `The records are ${where}: ${s.count} of them, with the fields ${fields}.` : 'It holds no list of records.',
    ];
    if (top) lines.push(`Also at its top level: ${top}.`);
    if (entry.kind === 'docx') lines.push('Each record is one paragraph of the document in order (`style` is the Word style, `heading` marks titles and headings, `footnotes` the ids of the footnotes it cites); `footnotes` and `endnotes` at the top level are `{id, text}`.');
    if (entry.note) lines.push(entry.note);
    const list = s.path ? JSON.parse(entry.text)[s.path] : JSON.parse(entry.text);
    if (entry.samples && Array.isArray(list) && list.length) {
      lines.push(`The first ${Math.min(SAMPLES, list.length)} records, which the participant chose to send:\n\`\`\`json\n${JSON.stringify(list.slice(0, SAMPLES), null, 1)}\n\`\`\``);
    } else {
      lines.push('No values were sent: the participant chose to send only the field names and their types. Read every value from the data, and handle text of any length and empty fields.');
    }
    return lines.join(' ') + ')';
  }

  /* ---------- kept in this browser ---------- */

  let dbp = null;
  function db() {
    if (!dbp) dbp = new Promise((res, rej) => {
      const r = indexedDB.open('ws-own-files', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('files', { keyPath: 'key' });
      r.onsuccess = () => res(r.result);
      r.onerror = () => rej(r.error);
    });
    return dbp;
  }
  const tx = async (mode, fn) => {
    const d = await db();
    return new Promise((res, rej) => {
      const t = d.transaction('files', mode);
      const out = fn(t.objectStore('files'));
      t.oncomplete = () => res(out && out.result);
      t.onerror = () => rej(t.error);
    });
  };
  const load = () => tx('readonly', (s) => s.getAll()).catch(() => []);
  const put = (entry) => tx('readwrite', (s) => s.put(entry)).catch(() => null);
  const remove = (key) => tx('readwrite', (s) => s.delete(key)).catch(() => null);

  return { read, describe, shape, load, put, remove, NOUN, SAMPLES };
})();
