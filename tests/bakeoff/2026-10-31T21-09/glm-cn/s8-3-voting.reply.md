I built a two-State voting comparison for the Council roll calls: pick any two States that appear in at least one roll call, switch between resolutions / amendments / both, and see how many votes they shared, how often they agreed, a per-year timeline chart, and a clickable list of the votes where they differed. Rows where the official yes/no/abstain totals don't match the roll call (counted by the page) carry a ⚠ flag with both sets of numbers.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Comparing how two States vote at the Human Rights Council</title>
<style>
  :root{--accent:#1f6fb2;--accent-dark:#175a91;--ink:#1d2a38;--muted:#5c6b7a;--line:#dde5ee;--bg:#f4f7fa;--card:#fff}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
  .wrap{max-width:1100px;margin:0 auto;padding:28px 22px 64px}
  h1{font-size:26px;line-height:1.25;margin:0 0 6px}
  h2{font-size:18px;margin:0}
  .desc{color:var(--muted);font-size:15px;margin:0}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-top:18px}
  .note{font-size:13.5px;color:var(--muted);margin:12px 0 0;border-top:1px dashed var(--line);padding-top:10px;line-height:1.55}
  .controls{display:flex;flex-wrap:wrap;gap:16px 22px;align-items:flex-end}
  .field{display:flex;flex-direction:column;gap:4px}
  .field label,.flab{font-size:13px;font-weight:600;color:var(--muted)}
  select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;min-width:250px;max-width:100%}
  .helper{font-size:12.5px;color:var(--muted)}
  .btn{font:inherit;font-size:14px;padding:9px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer}
  .btn:hover{background:var(--accent-dark)}
  .seg{display:inline-flex;border:1px solid var(--accent);border-radius:8px;overflow:hidden;flex-wrap:wrap}
  .segbtn{position:relative;display:inline-flex}
  .segbtn input{position:absolute;opacity:0;pointer-events:none}
  .segbtn span{display:block;padding:7px 13px;font-size:13.5px;color:var(--accent);background:#fff;cursor:pointer;user-select:none;white-space:nowrap}
  .segbtn input:checked+span{background:var(--accent);color:#fff}
  .segbtn input:focus-visible+span{outline:2px solid var(--accent-dark);outline-offset:-3px}
  .notice{margin-top:18px;background:#fdf6e3;border:1px solid #e8d49a;border-radius:10px;padding:14px 16px;font-size:15px}
  .lede{margin:20px 0 0;font-size:17px;line-height:1.5}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:14px}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
  .stat .num{font-size:30px;font-weight:700;color:var(--accent);line-height:1.15}
  .stat .lab{font-size:14px;margin-top:4px;font-weight:600}
  .stat .sub{font-size:12.5px;color:var(--muted);margin-top:2px;line-height:1.45}
  .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
  .chip{font-size:13px;background:#e8f0f8;color:var(--accent-dark);border-radius:999px;padding:3px 12px}
  .smallnote{font-size:13.5px;color:var(--muted);margin:10px 2px 0;line-height:1.55}
  .chartbox{position:relative;height:340px;margin-top:10px}
  .emptymsg{color:var(--muted);font-size:15px;margin:10px 2px}
  .listhead{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;justify-content:space-between}
  .countline{font-size:13.5px;color:var(--muted);margin:8px 0 4px}
  .vrow{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-top:10px;background:#fff;cursor:pointer}
  .vrow:hover{border-color:var(--accent)}
  .vrow.open{border-color:var(--accent);background:#fafcff}
  .vrow .meta{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;font-size:14px}
  .date{color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
  .sym{font-size:14px;font-weight:600}
  .sym a,.details a{color:var(--accent);font-weight:600;text-decoration:none;border-bottom:1px solid #bcd3e7}
  .sym a:hover,.details a:hover{border-bottom-color:var(--accent)}
  .kindbadge{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);border:1px solid var(--line);border-radius:5px;padding:1px 7px}
  .warn{font-size:12px;color:#7a5200;background:#fdf3d7;border:1px solid #e8d49a;border-radius:6px;padding:2px 8px;cursor:help;white-space:nowrap}
  .chev{margin-left:auto;font-size:12.5px;color:var(--muted);white-space:nowrap}
  .vtitle{font-size:15.5px;font-weight:600;margin:7px 0 0;line-height:1.45}
  .votewrap{display:flex;flex-wrap:wrap;gap:8px;margin-top:9px}
  .vpill{display:inline-flex;align-items:baseline;gap:6px;border-radius:999px;padding:3px 12px;font-size:13.5px;font-weight:600;border:1px solid transparent}
  .vpill .who{font-weight:400;opacity:.8}
  .vpill.Y{background:#e4f2e8;color:#17603a;border-color:#bfe0cb}
  .vpill.N{background:#fce9e6;color:#99291c;border-color:#f2cdc7}
  .vpill.A,.vpill.X{background:#edf1f5;color:#48586a;border-color:#d7dfe8}
  .details{display:none;margin-top:11px;border-top:1px dashed var(--line);padding-top:10px;font-size:14px;color:#3d4c5c;line-height:1.7}
  .vrow.open .details{display:block}
  #moreBtn{margin-top:12px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Comparing how two States vote at the Human Rights Council</h1>
    <p class="desc" id="dataDesc"></p>
  </header>

  <section class="card" id="controls">
    <div class="controls">
      <div class="field">
        <label for="selA">First State</label>
        <select id="selA"></select>
        <span class="helper" id="helpA"></span>
      </div>
      <div class="field" style="justify-content:flex-end">
        <button class="btn" id="swapBtn" type="button" title="Swap the two States">⇄ Swap</button>
      </div>
      <div class="field">
        <label for="selB">Second State