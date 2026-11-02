// A password gate for the preview on GitHub Pages: it keeps casual visitors out, nothing more.
// The site is static and its repository is public, so the data and PDFs stay reachable by URL.
// Remove this file (and its <script> tags) to open the site.
(function () {
  var HASH = 'd79e5dcbbfa52f79d701651a0cb3c0f8727ff1060f276af1cd604d49761b4641';
  var KEY = 'ws:gate';
  if (/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) return;   // local development and tests
  var ok = false;
  try { ok = localStorage.getItem(KEY) === HASH; } catch (e) { /* no storage: ask every time */ }
  if (ok) return;
  document.documentElement.style.visibility = 'hidden';
  async function sha(s) {
    var b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
    return Array.from(new Uint8Array(b)).map(function (x) { return x.toString(16).padStart(2, '0'); }).join('');
  }
  function show() {
    var f = document.createElement('form');
    f.setAttribute('style', 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;' +
      'background:#f2f4f7;font:16px system-ui,sans-serif;visibility:visible;color:#16202b');
    f.innerHTML = '<div style="background:#fff;padding:28px 32px;border-radius:12px;box-shadow:0 4px 16px rgba(16,30,54,.12);max-width:360px">' +
      '<h1 style="margin:0 0 6px;font-size:20px">Workshop Studio</h1>' +
      '<p style="margin:0 0 14px;color:#4a5664">A preview. Enter the password to continue.</p>' +
      '<input type="password" autocomplete="current-password" aria-label="Password" style="width:100%;font:inherit;padding:9px 10px;border:1px solid #c7ced6;border-radius:8px">' +
      '<p class="gate-err" style="color:#a3261b;margin:8px 0 0;min-height:1.2em"></p>' +
      '<button style="margin-top:8px;font:inherit;padding:8px 18px;border:0;border-radius:8px;background:#1f6fb2;color:#fff;cursor:pointer">Enter</button></div>';
    f.onsubmit = async function (e) {
      e.preventDefault();
      var h = await sha(f.querySelector('input').value);
      if (h === HASH) {
        try { localStorage.setItem(KEY, HASH); } catch (err) { /* this visit only */ }
        location.reload();
      } else {
        f.querySelector('.gate-err').textContent = 'That is not the password.';
      }
    };
    document.body.appendChild(f);
    f.querySelector('input').focus();
  }
  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
