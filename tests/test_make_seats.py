"""tools/make_seats.py --course geneva: the cards carry the gate's password only when it opens the gate, and the seat
file is never written over by accident (its codes may be printed or on the server already)."""
import csv
import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("make_seats", ROOT / "tools" / "make_seats.py")
make_seats = importlib.util.module_from_spec(spec)
spec.loader.exec_module(make_seats)


@pytest.fixture
def geneva(tmp_path, monkeypatch):
    (tmp_path / "site").mkdir()
    (tmp_path / "site" / "gate.js").write_text(f"var HASH = '{hashlib.sha256(b'open sesame').hexdigest()}';")
    monkeypatch.setattr(make_seats, "ROOT", tmp_path)
    monkeypatch.setattr(make_seats, "OUT", tmp_path / "out")
    monkeypatch.setitem(sys.modules, "playwright.sync_api", None)   # no PDF in the test: the HTML is what is checked

    def run(password="open sesame", *extra):
        (tmp_path / "pw.txt").write_text(password + "\n")
        monkeypatch.setattr(sys, "argv", ["make_seats.py", "--course", "geneva", "--n", "3", "--facilitators", "1",
                                          "--password-file", str(tmp_path / "pw.txt"), *extra])
        make_seats.main()
        return tmp_path / "out"
    return run


def test_geneva_cards_name_both_addresses_and_open_with_the_code(geneva):
    out = geneva()
    seats = list(csv.DictReader((out / "seats-geneva.csv").open()))
    assert [s["label"] for s in seats] == ["Geneva 01", "Geneva 02", "Geneva 03", "Geneva facilitator 1"]
    assert {s["budget"] for s in seats} == {"8.0"} and len({s["code"] for s in seats}) == 4
    page = (out / "geneva-seat-cards.html").read_text()
    assert page.count('class="card"') == 4 and all(s["code"] in page for s in seats)
    assert "150.254.115.204/studio-api/site/?course=geneva" in page and "open sesame" in page and "Kenya" not in page


def test_a_wrong_password_writes_nothing_and_a_second_run_keeps_the_codes(geneva):
    with pytest.raises(SystemExit, match="does not open the gate"):
        geneva("open sesam")
    out = geneva()
    first = (out / "seats-geneva.csv").read_text()
    with pytest.raises(SystemExit, match="already there"):
        geneva()
    assert (out / "seats-geneva.csv").read_text() == first
    geneva("open sesame", "--force")
    assert (out / "seats-geneva.csv").read_text() != first
