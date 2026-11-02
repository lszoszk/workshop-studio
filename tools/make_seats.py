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
"""
import argparse
import csv
import html
import io
import secrets
from itertools import cycle
from pathlib import Path

import qrcode
import qrcode.image.svg

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "out"
ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I/L
BASE_URL = "https://lszoszk.github.io/workshop-studio/"


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
    a = ap.parse_args()

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
    <div class="u">Scan, or open {html.escape(a.base_url.replace('https://', ''))} and type the code.</div>
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


if __name__ == "__main__":
    main()
