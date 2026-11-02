"""Use a built wiki app (s8-5) the way a participant would, and print what happened.

    python3 tools/wiki_probe.py tests/bakeoff/<run>/<model>/s8-5-wiki.html …

Opens the concept "mental privacy", counts the citations shown, clicks the first one (it must call
studio.openSource with a real document id and the PDF page of a passage cited that way), then
"Draft a summary" (it must call studio.ask with at most 12 passages). Checks against the library.
"""
import json, re, sys
sys.path.insert(0, "tools")
from bakeoff import inject, init_script, DATA
from playwright.sync_api import sync_playwright

CITE = re.compile(r"para\.\s*(\d+(?:\s*\([a-z]\))?)|p\.\s*(e?\d+)")
index = json.loads((DATA / "index.json").read_text())
lib = {d["id"]: d for d in json.loads((DATA / "library.json").read_text())["records"]}
truth = sum(1 for d in lib.values() for p in d["passages"] if "mental privacy" in p["text"].lower())
init = init_script({"uhri": "uhri_kenya.json", **{k: v["file"] for k, v in index["datasets"].items()}})


def right_page(opened, label):
    """The page opened is where a passage of that document starts, cited by the link's paragraph or printed page."""
    d = lib.get(opened[0])
    m = CITE.search(label or "")
    if not d or not m:
        return False
    para, printed = m.group(1), m.group(2)
    return any(p["page"] == opened[1] and (p["paragraph"] == para if para else p["page_label"] == printed) for p in d["passages"])


with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome")
    for path in sys.argv[1:]:
        p = b.new_page(viewport={"width": 1440, "height": 900})
        errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
        p.set_content(inject(open(path).read(), init), wait_until="load"); p.wait_for_timeout(800)
        p.get_by_text(re.compile(r"^\s*mental privacy", re.I)).first.click(); p.wait_for_timeout(600)
        shown = p.evaluate(r"() => (document.body.innerText.match(/para\.\s*\d+|\bp\.\s*e?\d+/g) || []).length")
        link = p.get_by_text(CITE).first
        label = link.inner_text() if link.count() else ""
        if link.count(): link.click(); p.wait_for_timeout(300)
        opened = p.evaluate("() => window.__opened || []")
        ok_page = bool(opened) and right_page(opened[0], label)
        btn = p.locator("button", has_text=re.compile("draft|summar", re.I)).first
        if btn.count(): btn.click(); p.wait_for_timeout(1500)
        asks = p.evaluate("() => window.__asks")
        print(f"{path.split('/')[-2]:8} citations shown {shown:3} (passages with 'mental privacy' in the library: {truth}) | link {label!r} -> {opened[:1]} right page: {ok_page} | "
              f"summary asks: {len(asks)}, chars {[a['chars'] for a in asks]} | errors {errs[:1]}")
        p.screenshot(path=path.replace(".html", ".probe.png"))
    b.close()
