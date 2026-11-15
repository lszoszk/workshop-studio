"""The scorer's checks for the two prototype tasks (tools/bakeoff.py: row_facts_*, diff_*), on small pages written
by hand: a check must pass the right page and fail the wrong one."""
import asyncio
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("bakeoff", ROOT / "tools" / "bakeoff.py")
bakeoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bakeoff)

FACTS = {"rows": ["CCPR/C/GC/32", "CEDAW/C/GC/35"],
         "facts": [{"row": "CCPR/C/GC/32", "has": ["23 August 2007|2007-08-23"]},
                   {"row": "CEDAW/C/GC/35", "has": ["26 July 2017|2017-07-26", "recommendation"]}]}
TABLE = """<!doctype html><html><head></head><body><table><tbody>
<tr><td>CCPR/C/GC/32</td><td>{d1}</td><td>General comment</td></tr>
<tr><td>CEDAW/C/GC/35</td><td>{d2}</td><td>General {t2}</td></tr></tbody></table></body></html>"""
DIFF = """<!doctype html><html><head></head><body><div role="tablist"><button role="tab">1951</button><button role="tab">1952</button></div>
<p>No restrictions <del>shall</del> <ins>may</ins> be placed … necessary <ins>in a democratic society</ins> <del>to ensure</del>
<ins>in the interests of</ins> national security {extra}</p></body></html>"""


def score(page, checks):
    async def go():
        from playwright.async_api import async_playwright
        async with async_playwright() as pw:
            browser = await bakeoff.launch(pw)
            res, _, _ = await bakeoff.score(browser, page, checks, "", Path("/dev/null"))
            await browser.close()
            return res
    return asyncio.run(go())


@pytest.mark.parametrize("d1,d2,t2,want", [("23 August 2007", "2017-07-26", "recommendation", True),
                                           ("23 August 2007", "26 July 2017", "comment", False),     # the wrong type
                                           ("12 September 2011", "26 July 2017", "recommendation", False)])
def test_row_facts_read_one_row_at_a_time(d1, d2, t2, want):
    assert score(TABLE.format(d1=d1, d2=d2, t2=t2), {"row_facts_x": FACTS})["row_facts_x"] is want


def test_row_facts_do_not_count_a_box_that_holds_every_row():
    # every fact is on the page, but no single row holds its own: the dates are swapped
    page = TABLE.format(d1="26 July 2017", d2="23 August 2007 recommendation", t2="recommendation")
    assert score(page, {"row_facts_x": FACTS})["row_facts_x"] is False


def test_diff_marks_what_was_added_and_removed_and_not_the_ocr_noise():
    checks = {"diff_added": ["democratic society", "in the interests of"], "diff_removed": ["to ensure"], "diff_not": ["restric"]}
    good = score(DIFF.format(extra=""), checks)
    assert good == {"diff_added": True, "diff_removed": True, "diff_not": True}
    noisy = score(DIFF.format(extra="<del>restric- tions</del> <ins>restrictions</ins>"), checks)
    assert noisy["diff_not"] is False and noisy["diff_added"] is True
