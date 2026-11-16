"use strict";
// Reads window.TEASER (data.js, written by make_teaser.py): label, dateText, n, duration, lines[{text,start,end}], apps[{img1,img2,title,model,name}]
const D = window.TEASER, DUR = D.duration, apps = D.apps;
const T_TITLE = 4.0, T_END = 4.0;
const film = document.getElementById("film");
const per = apps.length ? (DUR - T_TITLE - T_END) / apps.length : 0;
const titleEnd = apps.length ? T_TITLE : DUR / 2, endStart = apps.length ? DUR - T_END : DUR / 2;
const pad2 = n => String(n).padStart(2, "0");

// ── title card ──
const sTitle = el("div", "scene", film);
const kicker = D.label ? `Garage Research · ${esc(D.label)}` : "Garage Research";
el("div", "label abs", sTitle, kicker).style.cssText = "left:120px;top:130px";
const big = el("div", "abs serif", sTitle, `${D.n} ${D.n === 1 ? "tool" : "tools"} built<br>in this room`);
big.style.cssText = "left:120px;top:200px;font-size:132px;line-height:1.05;font-weight:500";
if (D.dateText) el("div", "abs mono", sTitle, esc(D.dateText)).style.cssText = "left:124px;top:520px;font-size:32px;color:var(--quiet);letter-spacing:.04em";
const thumbs = apps.slice(0, 6).map((a, i) => {
  const th = el("div", "thumb", sTitle, `<img src="${a.img1}">`);
  th._i = i; return th;
});

// ── app shots ──
const shots = apps.map((a, i) => {
  const s = el("div", "scene", film);
  const screen = el("div", "screen", s);
  const inner = el("div", "inner", screen);
  const im1 = el("img", "", inner); im1.src = a.img1;
  let im2 = null;
  if (a.img2) { im2 = el("img", "", inner); im2.src = a.img2; }
  const side = el("div", "side", s);
  const lab = el("div", "label", side, `Tool ${pad2(i + 1)} / ${pad2(apps.length)}`);
  const rule = el("div", "rule", side);
  const t = el("div", "t", side, esc(a.title));
  const parts = [`built with<b>${esc(a.model)}</b>`];
  if (a.name) parts.push(`<span style="display:block;margin-top:18px">by<b>${esc(a.name)}</b></span>`);
  const m = el("div", "m", side, parts.join(""));
  // each shot pushes in toward a different part of the screen (the top-left holds the search box in most apps)
  const focus = [[20, 14], [34, 22], [25, 36], [38, 16], [30, 12], [22, 30]][i % 6];
  return { s, inner, im2, lab, rule, t, m, screen, focus };
});

// ── end card ──
const sEnd = el("div", "scene", film);
el("div", "label abs", sEnd, kicker).style.cssText = "left:120px;top:200px";
const endBig = el("div", "abs serif", sEnd, "Retrieve,<br>don’t generate.");
endBig.style.cssText = "left:120px;top:270px;font-size:150px;line-height:1.04;font-weight:500";
const endRule = el("div", "abs", sEnd); endRule.style.cssText = "left:124px;top:630px;width:560px;height:4px;background:var(--accent);transform-origin:0 50%";
const endSmall = el("div", "abs mono", sEnd, "Narration voiced with AI (ElevenLabs) · film made with AI assistance (Claude)");
endSmall.style.cssText = "left:124px;top:690px;font-size:26px;color:var(--quiet);letter-spacing:.02em";

const subs = document.getElementById("subs"), cap = subs.querySelector(".cap");

function seek(t) {
  t = clamp(t, 0, DUR);
  sTitle.style.display = t < titleEnd ? "block" : "none";
  sEnd.style.display = t >= endStart ? "block" : "none";
  // title: thumbnails drift left slowly; the text is already on screen at frame 0 (thumbnail frame)
  const drift = t * 38;
  thumbs.forEach((th, i) => { th.style.left = (120 + i * 470 - drift) + "px"; th.style.top = (590 + (i % 2) * 26) + "px"; th.style.opacity = 0.95; });
  if (t < titleEnd) {
    const p = E.outCubic(seg(t, 0, 0.8));
    big.style.transform = `translateY(${(1 - p) * 14}px)`;
  }
  shots.forEach((sh, i) => {
    const a = titleEnd + i * per, b = a + per;
    const on = apps.length && t >= a && t < b;
    sh.s.style.display = on ? "block" : "none";
    if (!on) return;
    const u = t - a, p = u / per;
    const enter = E.outQuint(seg(u, 0, 0.45));
    sh.screen.style.transform = `translateX(${(1 - enter) * 90}px)`;
    sh.screen.style.opacity = clamp(u / 0.2);
    const sc = lerp(1.0, 1.07, E.inOutSine(p));
    sh.inner.style.transformOrigin = `${sh.focus[0]}% ${sh.focus[1]}%`;
    sh.inner.style.transform = `scale(${sc})`;
    if (sh.im2) sh.im2.style.opacity = seg(p, 0.5, 0.5 + 0.22 / per);   // the cross-cut to the shot after the search
    const rv = (x0) => E.outCubic(seg(u, x0, x0 + 0.5));
    sh.lab.style.opacity = rv(0.1); sh.lab.style.transform = `translateY(${(1 - rv(0.1)) * 16}px)`;
    sh.rule.style.transform = `scaleX(${rv(0.2)})`;
    sh.t.style.opacity = rv(0.3); sh.t.style.transform = `translateY(${(1 - rv(0.3)) * 18}px)`;
    sh.m.style.opacity = rv(0.6); sh.m.style.transform = `translateY(${(1 - rv(0.6)) * 18}px)`;
  });
  if (t >= endStart) {
    const u = t - endStart;
    endBig.style.opacity = E.outCubic(seg(u, 0, 0.5));
    endBig.style.transform = `translateY(${(1 - E.outCubic(seg(u, 0, 0.7))) * 24}px)`;
    endRule.style.transform = `scaleX(${E.outCubic(seg(u, 0.4, 1.0))})`;
    endSmall.style.opacity = E.outCubic(seg(u, 0.9, 1.5));
  }
  // burned-in captions of the narration
  const L = D.lines.find(l => t >= l.start && t < l.end);
  if (L) { cap.textContent = L.text; subs.style.display = "block"; subs.style.opacity = Math.min(seg(t, L.start, L.start + 0.12), 1 - seg(t, L.end - 0.1, L.end)); }
  else subs.style.display = "none";
}
window.seek = seek;
window.READY = (async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  const q = new URLSearchParams(location.search);
  seek(q.has("t") ? parseFloat(q.get("t")) : 0);
  return true;
})();
