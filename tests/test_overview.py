"""site/data/gc-overview.json (tools/overview.py) must say what site/data/gc.json says: the studio's Data step shows it."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import overview  # noqa: E402


def test_the_overview_matches_the_file():
    full = json.loads((ROOT / "site/data/gc.json").read_text(encoding="utf-8"))["records"]
    ov = json.loads((ROOT / "site/data/gc-overview.json").read_text(encoding="utf-8"))
    assert {k: v for k, v in ov.items() if k != "file"} == overview.overview(full), "run python3 tools/overview.py"
    assert ov["count"] == 7304 and ov["records"] == full[:3]
