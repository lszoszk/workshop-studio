"""Every activity event the front sends must be one the server keeps: clean_event drops any name that is not in
EVENT_NAMES, silently, so a new track('…') in site/*.js without its name there is lost in the next session.

    python3 -m pytest tests/test_event_names.py -q
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

import app as studio  # noqa: E402


def test_every_tracked_name_is_kept_by_the_server():
    sent = {}
    for p in sorted((ROOT / "site").glob("*.js")):
        for name in re.findall(r"\btrack\(\s*'([a-z_]+)'", p.read_text(encoding="utf-8")):
            sent.setdefault(name, p.name)
    assert sent, "no track('…') call found: the pattern or the folder is wrong"
    lost = {n: f for n, f in sent.items() if n not in studio.EVENT_NAMES}
    assert not lost, f"sent by the studio but dropped by the server (add to EVENT_NAMES): {lost}"
