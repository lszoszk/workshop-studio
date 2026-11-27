#!/usr/bin/env python3
"""Seat codes for the workshop, and a print sheet of badge cards with QR codes.

Each participant gets a 6-character code. The QR opens the studio with the code in the
URL fragment (#s=CODE), which never reaches any server log; the studio then asks the
server for the seat's country and budget.

    python3 tools/make_seats.py --participants seats_in.csv     # name,country per line
    python3 tools/make_seats.py --n 30 --countries Kenya,Tunisia,Colombia

Writes to tools/out/ (git-ignored: the codes are access keys):
    seats.csv          code,country,label,budget  -> import on the server
    seats_print.html   badge cards, open in a browser and print (A4, 8 per page)

Geneva (4 December 2026): seats "Geneva 01" to "Geneva 30" and "Geneva facilitator 1" to "4", cards with the studio's
two addresses and the password of the gate (read from a git-ignored file and checked against site/gate.js, so a typo
is not printed 34 times). It never overwrites a seat file it wrote before (--force does):

    python3 tools/make_seats.py --course geneva --n 30 --facilitators 4 --password-file tools/out/gate-password.txt
        seats-geneva.csv           -> import on the server (server/deploy.sh imports only seats.csv: see the run sheet)
        geneva-seat-cards.html     the cards (A4, 8 per page); geneva-seat-cards.pdf as well when Playwright is installed
"""
import argparse
import csv
import hashlib
import html
import io
import re
import secrets
from itertools import cycle
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "out"
ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I/L
BASE_URL = "https://lszoszk.github.io/workshop-studio/"
GENEVA_URL = BASE_URL + "?course=geneva"
GENEVA_BACKUP = "https://150.254.115.204/studio-api/site/?course=geneva"


def code():
    return "".join(secrets.choice(ALPHABET) for _ in range(6))


def qr_svg(data):
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode()
    return svg[svg.index("<svg"):]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--participants", type=Path, help="CSV with name,country (header optional)")
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--countries", default="Kenya,Tunisia,Colombia,Philippines,Georgia,Switzerland")
    ap.add_argument("--facilitators", type=int, default=6)
    ap.add_argument("--budget", type=float, default=8.0)
    ap.add_argument("--base-url", default=BASE_URL)
    ap.add_argument("--backup-url", help="the studio's second home, printed under the link (e.g. https://150.254.115.204/studio-api/site/?course=geneva)")
    ap.add_argument("--course", choices=["geneva"], help="the cards of one course (see above)")
    ap.add_argument("--password-file", type=Path, help="--course geneva: a file with the password of the gate, printed on the cards")
    ap.add_argument("--force", action="store_true", help="--course geneva: write new codes over an earlier seats-geneva.csv")
    a = ap.parse_args()
    if a.course == "geneva":
        return geneva(a)

    import json
    known = {c["name"] for c in json.loads((ROOT / "site/data/index.json").read_text())["countries"]}
    rows = []
    if a.participants:
        for r in csv.reader(a.participants.open(encoding="utf-8")):
            if not r or r[0].strip().lower() == "name":
                continue
            name, country = r[0].strip(), r[1].strip()
            if country not in known:
                raise SystemExit(f"{name}: no data pack for {country!r}. Add it with tools/build_data.py --countries first.")
            rows.append((country, name))
    else:
        countries = [c.strip() for c in a.countries.split(",")]
        rows = [(c, f"Participant {i + 1}") for i, c in zip(range(a.n), cycle(countries))]
    rows += [(sorted(known)[0] if "Kenya" not in known else "Kenya", f"Facilitator {i + 1}") for i in range(a.facilitators)]

    used, seats = set(), []
    for country, label in rows:
        c = code()
        while c in used:
            c = code()
        used.add(c)
        seats.append({"code": c, "country": country, "label": label, "budget": a.budget})

    OUT.mkdir(exist_ok=True)
    with (OUT / "seats.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["code", "country", "label", "budget"])
        w.writeheader()
        w.writerows(seats)

    cards = "".join(f"""
<div class="card">
  <div class="qr">{qr_svg(a.base_url + '#s=' + s['code'])}</div>
  <div class="txt">
    <div class="t">Workshop Studio</div>
    <div class="who">{html.escape(s['label'])}</div>
    <div class="c">{s['code']}</div>
    <div class="k">Your data: UN recommendations to <b>{html.escape(s['country'])}</b></div>
    <div class="u">Scan, or open {html.escape(a.base_url.replace('https://', ''))} and type the code.</div>{f'<div class="u">If that page does not open: {html.escape(a.backup_url.replace("https://", ""))}, and the same code.</div>' if a.backup_url else ''}
  </div>
</div>""" for s in seats)
    (OUT / "seats_print.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Seat cards</title>
<style>
@page {{ size: A4; margin: 10mm; }}
body {{ font: 12px system-ui, sans-serif; margin: 0; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }}
.card {{ border: 1px dashed #999; border-radius: 4mm; padding: 5mm; display: flex; gap: 5mm; height: 62mm; break-inside: avoid; }}
.qr svg {{ width: 42mm; height: 42mm; }}
.t {{ font-weight: 700; color: #1f6fb2; }}
.who {{ color: #555; margin: 1mm 0 3mm; }}
.c {{ font: 700 26px ui-monospace, Menlo, monospace; letter-spacing: .15em; }}
.k {{ margin-top: 3mm; }}
.u {{ margin-top: 3mm; color: #555; font-size: 10px; }}
</style>
<div class="grid">{cards}</div>""", encoding="utf-8")
    print(f"{len(seats)} seats -> {OUT / 'seats.csv'}, {OUT / 'seats_print.html'}")


def gate_password(path: Path | None) -> str:
    """The password of site/gate.js, from a file that stays out of the repository; refused unless it opens the gate."""
    if not path:
        raise SystemExit("--password-file is needed: the cards carry the password of the gate")
    pw = path.read_text(encoding="utf-8").strip()
    want = re.search(r"var HASH = '([0-9a-f]{64})'", (ROOT / "site/gate.js").read_text()).group(1)
    if hashlib.sha256(pw.encode()).hexdigest() != want:
        raise SystemExit(f"The password in {path} does not open the gate (site/gate.js): nothing written")
    return pw


def geneva_card(s: dict, password: str) -> str:
    short = lambda u: html.escape(u.replace("https://", "")).replace("/?", "/<wbr>?", 1)
    return f"""<div class="card">
  <div class="top"><span class="logo">GR <b>&gt;_</b></span><span class="what">Garage Research · Geneva, 4.12.2026</span><span class="lab">{html.escape(s["label"])}</span></div>
  <div class="mid">
    <div class="txt">
      <div class="k">Your seat code</div><div class="code">{html.escape(s["code"])}</div>
      <div class="k">Studio</div><div class="v">{short(GENEVA_URL)}</div>
      <div class="k">Password</div><div class="v">{html.escape(password)}</div>
    </div>
    <div class="qr">{qr_svg(GENEVA_URL + "#s=" + s["code"])}<div class="n">scan to open</div></div>
  </div>
  <div class="alt"><div class="k">Does not open? The same password and code at</div><span class="u">{html.escape(GENEVA_BACKUP.replace("https://", ""))}</span></div>
  <div class="foot">A live model with a small budget: if it runs out, tell the facilitator. No personal or confidential data.</div>
</div>"""


GENEVA_STYLE = """@page { size: A4; margin: 10mm; }
* { box-sizing: border-box; }
body { margin: 0; font: 10.5pt/1.35 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1d1b18; }
.grid { display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 68mm; }
.card { border: 1px dashed #999; padding: 4mm 5mm; overflow: hidden; display: flex; flex-direction: column; break-inside: avoid; }
.top { display: flex; align-items: center; gap: 3mm; font-size: 7.5pt; color: #5b564c; white-space: nowrap; }
.logo { background: #141414; color: #fff; font: 700 9pt ui-monospace, Menlo, monospace; padding: 1mm 2mm; border-radius: 1.5mm; }
.logo b { color: #5bd45b; }
.what { overflow: hidden; text-overflow: ellipsis; }
.lab { margin-left: auto; font-family: ui-monospace, Menlo, monospace; }
.mid { display: flex; gap: 4mm; margin-top: 1.5mm; }
.txt { flex: 1; min-width: 0; }
.k { font: 7.5pt ui-monospace, Menlo, monospace; letter-spacing: .08em; text-transform: uppercase; color: #1f5f9e; margin-top: 1.1mm; }
.code { font: 700 20pt/1.05 ui-monospace, Menlo, monospace; letter-spacing: .12em; }
.v { font-size: 9pt; overflow-wrap: anywhere; }
.n { font-size: 7.5pt; color: #5b564c; }
.qr { width: 27mm; flex: none; text-align: center; }
.qr svg { width: 27mm; height: 27mm; display: block; }
.alt { font-size: 9pt; margin: auto 0 1.5mm; }
.alt .u { white-space: nowrap; }
.foot { font-size: 7.5pt; color: #5b564c; border-top: 1px solid #d9d2c3; padding-top: 1.5mm; }"""


def geneva(a) -> None:
    out_csv, out_html = OUT / "seats-geneva.csv", OUT / "geneva-seat-cards.html"
    if out_csv.exists() and not a.force:
        raise SystemExit(f"{out_csv} is already there (its codes may be printed or on the server). --force writes new ones.")
    password = gate_password(a.password_file)
    labels = [f"Geneva {i + 1:02d}" for i in range(a.n)] + [f"Geneva facilitator {i + 1}" for i in range(a.facilitators)]
    used, seats = set(), []
    for label in labels:
        c = code()
        while c in used:
            c = code()
        used.add(c)
        seats.append({"code": c, "country": "Switzerland", "label": label, "budget": a.budget})
    OUT.mkdir(exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["code", "country", "label", "budget"])
        w.writeheader()
        w.writerows(seats)
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Geneva seat cards</title><style>{GENEVA_STYLE}</style>'
            f'</head><body><div class="grid">{"".join(geneva_card(s, password) for s in seats)}</div></body></html>')
    out_html.write_text(page, encoding="utf-8")
    done = [out_csv.name, out_html.name]
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            pg = b.new_page()
            pg.set_content(page)
            pg.pdf(path=str(OUT / "geneva-seat-cards.pdf"), format="A4", print_background=True,
                   margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"})
            b.close()
        done.append("geneva-seat-cards.pdf")
    except Exception as e:   # noqa: BLE001 — the HTML prints from any browser
        print(f"no PDF ({type(e).__name__}): print {out_html.name} from a browser")
    print(f"{len(seats)} seats (${a.budget:g} each) -> tools/out/: " + ", ".join(done))


if __name__ == "__main__":
    main()
