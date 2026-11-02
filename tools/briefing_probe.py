"""Test a built briefing-check app (s8-4) on a briefing with five planted errors and print its verdicts.

    python3 tools/briefing_probe.py tests/bakeoff/<run>/<model>/s8-4-briefing-check.html …

Planted: 50th session (51st), 20 against (19), 6 abstentions (7), India abstained (voted against),
and a mandate claim the voting data cannot check. Everything else in the text is right.
"""
import json, sys
sys.path.insert(0, "tools")
from bakeoff import inject, init_script, DATA
from playwright.sync_api import sync_playwright

BRIEF = ("Resolution A/HRC/RES/51/27 on the situation of human rights in Ethiopia was adopted by the Human Rights Council "
         "on 7 October 2022, at its 50th session, by a recorded vote of 21 in favour, 20 against and 6 abstentions. "
         "The text was presented by the European Union. The United States, Germany and Finland voted in favour; "
         "China, Pakistan and Eritrea voted against. India abstained, as did Indonesia. "
         "The resolution extended the mandate of the International Commission of Human Rights Experts on Ethiopia for one year.")
index = json.loads((DATA / "index.json").read_text())
init = init_script({"uhri": "uhri_kenya.json", **{k: v["file"] for k, v in index["datasets"].items()}})
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome")
    for path in sys.argv[1:]:
        p = b.new_page(viewport={"width": 1440, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.set_content(inject(open(path).read(), init), wait_until="load"); p.wait_for_timeout(800)
        p.locator("textarea").first.fill(BRIEF)
        p.locator("button", has_text="Check").first.click(); p.wait_for_timeout(1000)
        rows = p.evaluate("() => [...document.querySelectorAll('tbody tr')].map(r => [...r.cells].map(c => c.innerText.replace(/\\s+/g, ' ').trim()))")
        print("\n==", path.split("/")[-3], path.split("/")[-2], "rows:", len(rows), "errors:", errs[:1])
        for r in rows: print("  ", " | ".join(x[:70] for x in r))
        p.screenshot(path=path.replace(".html", ".probe.png"), full_page=True)
    b.close()
