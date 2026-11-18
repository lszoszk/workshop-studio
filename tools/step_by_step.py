"""Screenshots of the Geneva session, step by step, for site/step-by-step/ (a page a co-trainer can copy them from).

Walks the studio as a participant: the data, the brief, the recorded planning session, the plan edited by hand, a live
build, the test card, three improvement ideas, one improvement built, the "Show it to the room?" dialog (answered "Not
now", so nothing goes on the wall), then the wall, a frame of the teaser and the take-home kit.

    python3 tools/step_by_step.py --seat CODE            # the studio served on localhost:8766, the live server running
    python3 tools/step_by_step.py --seat CODE --only 01,02

The steps with a model (build, ideas, improvement) spend the seat's budget: about $0.50 on Claude Sonnet. The seat code
is never written anywhere, and every screenshot is checked for it before it is saved.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site/step-by-step/img"
BASE = "http://localhost:8766/"
TEASER = ROOT / "tools/teaser/out/latest.mp4"
FOCUS = ".sbs-focus { outline: 4px solid #e07a1f !important; outline-offset: 3px !important; }"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--only", default="")
    ap.add_argument("--model", default="", help="a model id of the menu (claude, glm-eu); the course's default when empty")
    ap.add_argument("--free", action="store_true", help="stop before the first model call (steps 01 to 06)")
    a = ap.parse_args()
    only = set(filter(None, a.only.split(",")))
    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except Exception:   # bundled Chromium missing: the installed Chrome
            browser = pw.chromium.launch(channel="chrome")
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, accept_downloads=True)
        page = ctx.new_page()

        def shot(name, *focus, pg=None):
            pg = pg or page
            if only and name[:2] not in only:
                return
            body = pg.evaluate("() => document.body.innerText + [...document.querySelectorAll('input,textarea')].map(e => e.value).join(' ')")
            if a.seat in body or a.seat in pg.url.split("#")[0]:
                sys.exit(f"{name}: the seat code is on the page; not saved")
            pg.add_style_tag(content=FOCUS)
            for sel in focus:
                pg.locator(sel).first.evaluate("e => e.classList.add('sbs-focus')")
            pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / f"{name}.png"))
            for sel in focus:
                pg.locator(sel).first.evaluate("e => e.classList.remove('sbs-focus')")
            print("saved", name, flush=True)

        page.goto(a.base + f"?course=geneva&reset=1&planpace=8#s={a.seat}")
        page.wait_for_selector(".data-card")
        if a.model:
            page.select_option("#modelSelect", a.model)
        page.wait_for_function("() => /paragraphs/.test(document.querySelector('.data-card .dc-facts').textContent)")
        shot("01-data-card", ".data-card", "#progress")

        page.click("#dataLook")
        page.wait_for_selector("#drawer .json-view")
        shot("02-inside-the-file", "#drawer")
        page.click("#drawerClose")

        page.wait_for_selector(".brief-card")
        page.fill("#briefTopic", "the rights of the child")
        page.locator(".brief-card").scroll_into_view_if_needed()
        shot("03-brief", ".brief-card")

        page.click("#sendBtn")
        page.wait_for_selector(".msg.ask:not(.answered)", timeout=120000)
        page.locator(".msg.ask:not(.answered)").scroll_into_view_if_needed()
        shot("04-planner-and-decision", ".msg.ask:not(.answered)")
        while True:   # the recommended answer to each decision card
            page.wait_for_selector(".msg.ask:not(.answered), .approve button.primary:not([disabled])", timeout=120000)
            card = page.locator(".msg.ask:not(.answered)")
            if not card.count():
                break
            card.locator(".ask-opt:has(.rec)").click()
        page.wait_for_selector("#planView:not([hidden])")
        page.wait_for_timeout(800)
        shot("05-plan", "#planView", ".approve")

        page.click("#planEditBtn")
        text = page.input_value("#planEdit")
        line = "- Show the year next to each document symbol."
        at = text.find("\n## ", text.find("## What the tool will do") + 5)
        page.fill("#planEdit", text[:at] + "\n" + line + "\n" + text[at:] if at > 0 else text + "\n" + line)
        page.evaluate("(l) => { const t = document.getElementById('planEdit'); const i = t.value.indexOf(l); t.focus(); t.setSelectionRange(i, i + l.length); t.scrollTop = Math.max(0, t.scrollHeight * i / t.value.length - 200); }", line)
        shot("06-edit-the-plan", "#planEdit")
        page.click("#planDone")
        if a.free:
            browser.close()
            return

        page.locator(".approve button.primary:not([disabled])").last.click()
        page.wait_for_selector("#building:not([hidden])", timeout=60000)
        page.wait_for_timeout(15000)
        shot("07-building", "#modelSelect")
        for attempt in range(3):   # a model that answers in words instead of writing the app is asked once more
            page.wait_for_function("() => document.getElementById('building').hidden && !document.querySelector('#sendBtn[disabled]')", timeout=600000)
            page.wait_for_timeout(2000)
            if page.locator("#versions [data-v]").count():
                break
            page.fill("#input", "Please build the app now, from my brief and the plan: the whole app in one html code block.")
            page.click("#sendBtn")
            page.wait_for_selector("#building:not([hidden])", timeout=60000)
        page.wait_for_timeout(3000)
        app = page.frame_locator(".viewport > iframe:not(.back)")
        box = app.locator("input[type=search], input[type=text]").first
        box.fill('"best interests" child')
        box.press("Enter")
        page.wait_for_timeout(1500)
        shot("08-the-app", ".viewport")

        page.wait_for_selector(".test-card", timeout=60000)
        for i in range(3):
            page.locator(".test-card .tline input").nth(i).check()
        page.fill(".test-card .tnote input", "show the year of each result")
        page.locator(".test-card").scroll_into_view_if_needed()
        shot("09-test-your-app", ".test-card")

        page.locator("#suggest button", has_text="Suggest three improvements").click()
        page.wait_for_selector(".msg.ideas .idea", timeout=300000)
        page.wait_for_timeout(500)
        page.locator(".msg.ideas").scroll_into_view_if_needed()
        shot("10-three-ideas", ".msg.ideas")

        page.locator(".msg.ideas .idea").nth(0).locator("[data-a=build]").click()
        page.wait_for_selector("#wallDialog[open]", timeout=600000)
        page.fill("#wallName", "Demo")
        page.wait_for_timeout(1500)
        shot("11-show-it-to-the-room")
        page.click("#wallNo")   # nothing goes on the wall

        page.click("#takeHomeBtn")
        with page.expect_download(timeout=120000) as dl:
            page.click("#kitBtn")
        kit = OUT.parent / "_kit.html"
        dl.value.save_as(kit)

        wall = ctx.new_page()
        wall.goto(a.base + "wall.html")
        wall.wait_for_selector(".card, .cap", timeout=60000)
        wall.wait_for_timeout(4000)
        shot("12-the-wall", pg=wall)

        k = ctx.new_page()
        k.goto(kit.as_uri())
        k.wait_for_selector(".req")
        shot("14-take-home-kit", "#reqs", pg=k)
        kit.unlink()
        browser.close()

    if (not only or "13" in only) and TEASER.exists():   # a frame of the teaser, from the film itself
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "12", "-i", str(TEASER), "-frames:v", "1",
                        str(OUT / "13-teaser.png")], check=True)
        print("saved 13-teaser", flush=True)


if __name__ == "__main__":
    main()
