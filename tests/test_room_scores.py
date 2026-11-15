"""tools/room_scores.py: which request a wall app came from, how a build counts, and the room's new builds from the log;
and that a room's file holds no app code, titles or seat codes (the repository is public)."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("room_scores", ROOT / "tools" / "room_scores.py")
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)
PROMPTS = {"s8-1-verbatim": {"checks": {"no_console_errors": True}}, "s8-3-voting": {"checks": {"chart": True}}}


def test_a_wall_app_is_matched_to_its_request():
    assert rs.request_of({"prompt_id": "s8-1-verbatim", "files": []}, PROMPTS) == "s8-1-verbatim"
    assert rs.request_of({"title": "VoteGram · Votes au Conseil", "files": ["hrc"]}, PROMPTS) == "s8-3-voting"
    assert rs.request_of({"title": "Verbatim finder", "files": ["gc"]}, PROMPTS) == "s8-1-verbatim"
    assert rs.request_of({"title": "Ten PDFs into a wiki", "files": ["pdfs", "uhri"]}, PROMPTS) == "v3-wiki-pdfs"
    assert rs.request_of({"title": "Macro Master", "files": ["own_1"]}, PROMPTS) is None


def test_outcome_counts_as_the_slide_does():
    assert rs.outcome({"a": True, "no_console_errors": True}) == "works"
    assert rs.outcome({"a": False, "no_console_errors": True}) == "partly"
    assert rs.outcome({"a": True, "no_console_errors": False}) == "broke"
    assert rs.outcome({}) == "broke"


def test_new_builds_and_errors_as_they_opened_come_from_the_log():
    ev = [
        {"sid": "a", "ms": 1, "t": "build", "kind": "app", "prompt": "s8-1-verbatim", "model": "glm-eu", "parent": None},
        {"sid": "a", "ms": 2, "t": "app_error", "first": True},
        {"sid": "a", "ms": 3, "t": "build", "kind": "app", "prompt": None, "model": "glm-eu", "parent": 1},   # a change: not counted
        {"sid": "a", "ms": 4, "t": "app_error", "first": True},                                                  # after the change
        {"sid": "b", "ms": 1, "t": "build", "kind": "app", "prompt": "s8-1-verbatim", "model": "claude", "parent": None},
        {"sid": "b", "ms": 2, "t": "app_error", "first": False},                                                 # later, not on opening
        {"sid": "c", "ms": 1, "t": "build", "kind": "talk", "prompt": "s8-1-verbatim", "model": "claude"},
    ]
    got = {(b["model"], b["request"]): (b["new"], b["error_on_open"]) for b in rs.builds_from_events(ev, {"s8-1-verbatim"})}
    assert got == {("glm", "s8-1-verbatim"): (1, 1), ("claude", "s8-1-verbatim"): (1, 0)}


def test_a_room_file_holds_only_counts():
    for f in (ROOT / "tests" / "room").glob("*.json"):
        text = f.read_text()
        assert "<html" not in text.lower() and '"title"' not in text and '"seat"' not in text and '"sid"' not in text, f
        room = json.loads(text)
        assert set(room) == {"label", "days", "wall", "builds"}
        assert all(set(w) == {"model", "request", "outcome", "failed"} for w in room["wall"])
