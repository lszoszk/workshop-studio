Here's the Verbatim finder. It searches the General Comments paragraph by paragraph with Boolean operators, exact phrases and wildcards; shows every matching paragraph exactly as stored, with self-checks, copyable citations in UN short form, and a draft collector that keeps quotations in the browser.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>Verbatim finder — General Comments and General Recommendations</title>
<style>
[hidden]{display:none!important}
*{box-sizing:border-box}
body{margin:0;background:#f4f0e8;color:#1d1b18;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#9b2335}
a:focus,button:focus,input:focus,select:focus,textarea:focus{outline:2px solid #9b2335;outline-offset:2px}
.mono{font-family:ui-monospace,Menlo,Consolas,"Courier New",monospace;font-size:12px;letter-spacing:.04em}
.lab{font-family:ui-monospace,Menlo,Consolas,"Courier New",monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.serif{font-family:Georgia,"Times New Roman",serif}
button{color:#1d1b18}
.linkish{background:none;border:none;padding:0;color:#5d5648;text-decoration:underline;cursor:pointer;font:inherit}
/* header */
.site-head{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;padding:18px 28px 14px;border-bottom:1px solid #d9d2c3;flex-wrap:wrap}
.site-head h1{font-family:Georgia,"Times New Roman",serif;font-size:26px;line-height:1.2;margin:6px 0 4px;font-weight:700}
#head-line{margin:0;color:#5d5648}
.head-checks{white-space:nowrap}
.head-checks.ok{color:#1e6b34}
.head-checks.fail{color:#9b2335}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:baseline}
.dot.green{background:#1e6b34}
.dot.red{background:#9b2335}
/* layout */
.layout{display:flex;align-items:stretch;min-height:60vh}
.rail{width:302px;flex:0 0 302px;border-right:1px solid #d9d2c3;padding:16px 20px 34px}
.main{flex:1;min-width:0;padding:16px 28px 44px}
@media (max-width:900px){.layout{flex-direction:column}.rail{width:auto;flex:none;border-right:none;border-bottom:1px solid #d9d2c3}}
/* tabs */
.tabs{display:flex;border-bottom:1px solid #d9d2c3;margin-bottom:16px;flex-wrap:wrap}
.tab{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;background:none;border:none;border-bottom:2px solid transparent;padding:10px 14px 8px;cursor:pointer}
.tab[aria-selected="true"]{color:#9b2335;border-bottom-color:#9b2335}
/* rail */
.rail-head{display:flex;justify-content:space-between;align-items:baseline;color:#5d5648}
#clear-all{font-size:11px}
.bignum{font-family:Georgia,"Times New Roman",serif;font-size:46px;line-height:1;margin:14px 0 0}
.bigsub{margin:2px 0 0;color:#5d5648;font-size:13px}
.ofsub{color:#5d5648;margin:2px 0 0;font-size:11.5px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip{border:1px solid #9b2335;color:#9b2335;background:#fdf9f2;padding:2px 8px;border-radius:10px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;text-align:left;max-width:100%}
.search{margin-top:16px;border-top:1px solid #d9d2c3;padding-top:12px}
.search-row{display:flex;gap:6px;margin-top:4px}
#q{flex:1;min-width:0;padding:7px 8px;border:1px solid #b7ac97;background:#fffdf8;font:14px ui-monospace,Menlo,Consolas,monospace}
.btn{border:1px solid #8b8271;background:#fffdf8;padding:5px 10px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.syntax{border:1px solid #d9d2c3;background:#fbf8f1;padding:10px 12px;margin-top:6px}
.syntax ul{margin:6px 0;padding-left:18px;font-size:13px;line-height:1.5}
.syntax .ex{display:block;width:100%;text-align:left;margin:4px 0;padding:4px 8px;border:1px solid #d9d2c3;background:#fffdf8;cursor:pointer;font:12px ui-monospace,Menlo,Consolas,monospace}
.normline{font-size:11px;color:#5d5648;line-height:1.5;margin:8px 0 0}
.echo{font-size:13px;margin:10px 0 0;border-left:2px solid #9b2335;padding-left:8px}
.echo.err{color:#9b2335;font-weight:600}
.acc{margin-top:18px;border-top:1px solid #d9d2c3}
.acc-btn{width:100%;text-align:left;background:none;border:none;padding:12px 0 10px;cursor:pointer;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;display:flex;gap:8px}
.acc-btn .num{color:#9b2335}
.fgroup{margin:0 0 16px}
.cb{display:block;margin:3px 0;font-size:13px;line-height:1.4}
.cb .code{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:700;font-size:12px}
.cb .cnt{color:#5d5648;font-size:11px}
.yr{width:78px;padding:4px 6px;border:1px solid #b7ac97;background:#fffdf8;font:inherit}
#docsel{width:100%;padding:5px 4px;border:1px solid #b7ac97;background:#fffdf8;font:inherit}
.small{font-size:11px;color:#5d5648}
/* copy status */
.copystatus{min-height:18px;font-size:11.5px;color:#1d1b18;margin:0 0 10px;white-space:pre-wrap;max-height:6em;overflow:auto}
.fallback{border:1px solid #9b2335;padding:10px;margin-bottom:14px}
.fallback textarea{width:100%;height:120px;font:12px ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;background:#fffdf8;border:1px solid #b7ac97;color:#1d1b18}
/* overview / fig */
.figno{color:#9b2335;margin:0 0 2px}
.figtitle{font-family:Georgia,"Times New Roman",serif;font-size:22px;margin:0 0 14px;font-weight:700}
.fig-flex{display:flex;gap:30px;align-items:flex-start;flex-wrap:wrap}
.chart-wrap{position:relative;flex:1 1 430px;min-width:320px}
.figtable{border-collapse:collapse;flex:0 0 auto;min-width:230px}
.figtable caption{text-align:left;color:#5d5648;padding-bottom:6px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.figtable th,.figtable td{border-top:1px solid #d9d2c3;padding:4px 10px;text-align:left;font-size:13px}
.figtable td.num,.figtable th.num{text-align:right}
.hint{color:#5d5648;font-size:11.5px;line-height:1.5}
.compute{color:#5d5648;font-size:11.5px;max-width:72ch;line-height:1.5}
/* records */
.rec-summary{font-family:Georgia,"Times New Roman",serif;font-size:21px;margin:0 0 4px;font-weight:700}
.orderline{margin:2px 0 6px;color:#5d5648}
.orderline select{margin-left:8px;padding:3px 4px;border:1px solid #b7ac97;background:#fffdf8;font:inherit;font-size:12px}
.row{border-top:1px solid #d9d2c3;padding:12px 0 14px;cursor:pointer;max-width:82ch}
.row:first-child{border-top:none}
.row.open{border-left:2px solid #9b2335;padding-left:12px}
.row-h{margin:0 0 6px;font-size:15px;font-weight:600;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
.row-toggle{background:none;border:none;padding:0;cursor:pointer;text-align:left;font:inherit;font-weight:inherit}
.badge{display:inline-block;border:1px solid #a2977e;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10px;letter-spacing:.06em;padding:0 5px;margin-right:4px;border-radius:2px;vertical-align:1px}
.row-h .doc{font-style:italic}
.meta{font-size:11px;color:#5d5648;letter-spacing:.02em}
.pin{color:#9b2335;font-weight:700}
.row-text{white-space:pre-wrap;margin:6px 0 4px;font-size:15.5px;line-height:1.6}
mark{background:#f3e6ad;color:#1d1b18;font-weight:700;padding:0 1px}
.row-sub{font-size:11px;color:#5d5648;margin:2px 0}
.row-sub .linkish{font-size:11px}
.ambernote{color:#7a4d00;font-size:13px;margin:6px 0 0}
.row-actions{margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.stylenote{color:#5d5648;margin-left:auto}
.ctx{color:#5d5648}
.ctxblock{margin:10px 0 0;border-left:2px solid #b7ac97;padding:2px 0 2px 12px;color:#5d5648;white-space:pre-wrap;font-size:14px}
.ctxblock .pin{display:block;margin-bottom:2px}
.dim{color:#867c68}
.more{display:block;margin:16px auto;padding:8px 18px}
.empty{color:#5d5648;font-style:italic}
/* checks */
.checks{list-style:none;padding:0;margin:0}
.checks li{border-top:1px solid #d9d2c3;padding:8px 0;font-size:14px;line-height:1.5}
.checks li:first-child{border-top:none}
.checks .res{font-weight:700}
.checks li.pass .res{color:#1e6b34}
.checks li.fail .res{color:#9b2335}
.quirks{padding-left:20px;font-size:14px;line-height:1.6;max-width:78ch}
h2.serif{font-size:22px;margin:22px 0 8px}
h3.serif{font-size:17px;margin:22px 0 6px}
/* draft */
.ditem{border-top:1px solid #d9d2c3;padding:10px 0;max-width:82ch}
.ditem:first-child{border-top:none}
.ditem blockquote{margin:0 0 4px;white-space:pre-wrap;font-size:15px;line-height:1.6}
.note-red{color:#9b2335;font-size:12.5px}
#draft-buttons{margin:10px 0 16px;display:flex;gap:10px;flex-wrap:wrap}
/* footer */
.site-foot{border-top:1px solid #d9d2c3;padding:12px 28px;color:#5d5648;font-size:11px;line-height:1.6}
</style>
</head>
<body>

<header class="site-head">
  <div>
    <p class="lab" style="margin:0;color:#5d5648">UN TREATY BODIES · GENERAL COMMENTS</p>
    <h1>Verbatim finder: General Comments and General Recommendations</h1>
    <p id="head-line" class="mono"></p>
  </div>
  <p id="head-checks" class="mono head-checks ok" aria-live="polite"></p>
</header>

<div class="layout">
  <aside class="rail" id="rail" aria-label="Filters">
    <div class="rail-head">
      <span class="lab">FILTERS</span>
      <button id="clear-all" class="linkish">Clear all</button>
    </div>
    <p class="bignum" id="big-num" aria-live="polite">0</p>
    <p class="bigsub">matching paragraphs</p>
    <p class="mono ofsub" id="of">of 0</p>
    <div class="chips" id="chips"></div>

    <div class="search">
      <label class="lab" for="q">SEARCH</label>
      <div class="search-row">
        <input id="q" type="text" autocomplete="off" spellcheck="false" placeholder='e.g. "best interests" AND child*'>
        <button id="q-go" class="btn" type="button">Search</button>
      </div>
      <div id="syntax" class="syntax" hidden>
        <p class="lab" style="margin:0;color:#5d5648">HOW TO SEARCH</p>
        <ul>
          <li>a space or AND joins words</li>
          <li>OR offers a choice</li>
          <li>NOT, or a leading -, excludes</li>
          <li>&ldquo;an exact phrase&rdquo; in double quotes</li>
          <li>parentheses group</li>
          <li>a star at the end of a word finds any ending (child* finds children)</li>
          <li>operators in capitals; lower-case &ldquo;or&rdquo; is a word</li>
        </ul>
        <p class="lab" style="margin:8px 0 0;color:#5d5648">TRY</p>
        <button class="ex" type="button