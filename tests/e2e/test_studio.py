"""End-to-end test of the studio in recorded mode (no model, no server, no cost).

    python3 -m pytest tests/e2e -q

Serves site/ on a free port, drives headless Chrome through a participant's path:
build the first request from its card (in plan mode: the recorded planning session, its
questions, the plan on the stage, Build), Run x3, Trace, saving the app and opening
it offline from disk, a reload; then what a
participant is shown at each step (Hick's law), recorded mode refusing free requests,
the phone hand-off page and the absence of technical jargon. A fake server stands in
for a live model to test what recorded mode cannot: switching country, asking the
model directly (with the paragraph that does not exist), changing a plan, and the
reference shelf's excerpts going out with a message.

?planpace=1 plays a planning session's notes in one second instead of 80 seconds.
"""
import functools
import http.server
import importlib.util
import json
import re
import urllib.request
import threading
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parents[2] / "site"
TOOLS = SITE.parent / "tools"
SHELF_MOCK = Path(__file__).with_name("shelf_mock.json")   # three pages, served as data/shelf.json where a test needs the shelf
JARGON = re.compile(r"\b(tokens?|fingerprint|hash|regular expression|regex|JSON|HTML|SSE|API|iframe|sandbox)\b", re.I)


@pytest.fixture(scope="module")
def base_url():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    class Server(http.server.ThreadingHTTPServer):
        request_queue_size = 64   # the default backlog of 5 resets Chrome's parallel loads at boot

    handler = functools.partial(Quiet, directory=str(SITE))
    with Server(("127.0.0.1", 0), handler) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        yield f"http://127.0.0.1:{srv.server_address[1]}/"
        srv.shutdown()


APP = ("Here is the app.\n```html\n<!doctype html><html><head><title>Count</title></head><body>"
       "<h1 id=c></h1><a id=jump href=\"#below\">jump</a><div id=below style=\"margin-top:1500px\">below</div>"
       "<script>const u = WORKSHOP_DATA.uhri; document.getElementById('c').textContent = u.country + ' ' + u.count;"
       "</script></body></html>\n```")
# edit mode: a change that fits the app above, one that does not, and the whole file the studio then asks for
EDIT_FITS = ("Now it says how many in words.\n```edit\n<<<<<<< SEARCH\nu.country + ' ' + u.count;\n=======\n"
             "u.country + ': ' + u.count + ' records';\n>>>>>>> REPLACE\n```")
EDIT_MISSES = ("Added a footer.\n```edit\n<<<<<<< SEARCH\n<p>a line that is not in the app</p>\n=======\n"
               "<p>a line that is not in the app</p><footer>Source: UHRI</footer>\n>>>>>>> REPLACE\n```")
APP_FOOTER = APP.replace("</body>", "<footer>Source: UHRI</footer></body>")
# automatic repair: an app that fails as it opens, and the one-line edit that repairs it
APP_BROKEN = APP.replace("<script>const u", "<script>undefinedHelper();\nconst u")
EDIT_REPAIR = ("Removed the call to a function that does not exist.\n```edit\n<<<<<<< SEARCH\nundefinedHelper();\n=======\n"
               "\n>>>>>>> REPLACE\n```")
# an app on the participant's own file (own-files.js)
APP_OWN = ("Here is your table.\n```html\n<!doctype html><html><head><title>Mine</title></head><body><h1 id=c></h1>"
           "<script>const d = WORKSHOP_DATA.own_1; document.getElementById('c').textContent = d.count + ' rows, first: ' + d.records[0].Name;"
           "</script></body></html>\n```")
# a checker built as a form: one that stops the submission itself, one that does not (the frame's policy stops it)
APP_FORM = ("Here is the checker.\n```html\n<!doctype html><html><head><title>Form</title></head><body>"
            "<form id=f><textarea>x</textarea><button id=go>Check</button></form><p id=out>none</p>"
            "<form id=g><button id=go2>Check again</button></form><p id=out2>none</p>"
            "<script>document.getElementById('f').addEventListener('submit', (e) => { e.preventDefault(); document.getElementById('out').textContent = 'checked'; });"
            "document.getElementById('g').addEventListener('submit', () => { document.getElementById('out2').textContent = 'ran'; });"
            "</script></body></html>\n```")
PLAN_V2 = ("Here is the revised plan.\n\n```markdown\n## Context\nThe same dashboard, revised.\n\n"
           "## The app, screen by screen\n1. A line chart of the records per year.\n2. The table of records.\n```")


FEEDBACK = []   # what the fake server received from the Feedback form
EVENTS = []     # the activity records it received (POST /events)


@pytest.fixture(scope="module")
def fake_api():
    """A stand-in for the studio server (docs/api-contract.md): one seat, canned answers, a wall."""
    calls, wall = [], []

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def head(self, status, ctype):
            self.send_response(status)
            self.send_header("Access-Control-Allow-Origin", self.headers.get("Origin") or "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Content-Type", ctype)
            self.end_headers()

        def do_OPTIONS(self):
            self.head(204, "text/plain")

        def do_GET(self):
            if self.path.endswith("/health"):
                body = {"ok": True, "accepting": True}
            elif self.path.endswith("/seat/TEST22"):
                body = {"seat": "TEST22", "country": "Colombia", "budget_total": 8, "budget_left": 7.5, "disabled": False}
            elif self.path.endswith("/gallery"):
                body = [{k: v for k, v in w.items() if k != "html"} for w in reversed(wall)]
            elif "/gallery/" in self.path:
                page = next((w["html"] for w in wall if self.path.endswith("/" + w["id"])), None)
                if page is None:
                    return self.head(404, "text/html")
                self.head(200, "text/html")
                return self.wfile.write(page.encode())
            else:
                return self.head(404, "application/json")
            self.head(200, "application/json")
            self.wfile.write(json.dumps(body).encode())

        def do_POST(self):
            req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.path.endswith("/gallery"):
                gid = f"1200{len(wall):02d}-{len(wall):08x}"
                wall.append({"id": gid, "seat": req.get("seat"), "country": req.get("country") or "Colombia", "title": req.get("title"),
                             "model": req.get("model"), "prompt_id": req.get("prompt_id"), "files": req.get("files") or [],
                             "created": "2026-12-04T10:4%d:00" % len(wall), "html": req["html"]})
                self.head(200, "application/json")
                return self.wfile.write(json.dumps({"ok": True, "id": gid}).encode())
            if self.path.endswith("/events"):
                EVENTS.append(req)
                self.head(200, "application/json")
                return self.wfile.write(json.dumps({"ok": True}).encode())
            if self.path.endswith("/feedback"):
                FEEDBACK.append(req)
                self.head(200, "application/json")
                return self.wfile.write(json.dumps({"ok": True, "id": "f1"}).encode())
            calls.append(req)
            last = req["messages"][-1]["content"]
            self.head(200, "text/event-stream")
            events = []
            if req["purpose"] == "build" and "how are you" in last.lower():
                events.append({"delta": "I'm well, thank you! Ask me anything, or drag a file into the chat to build an app."})
            elif req["purpose"] == "build" and "how should a bar chart" in last.lower():
                events.append({"delta": "Sort the bars, label them directly and start the axis at zero."})
            elif req["purpose"] == "build" and "a counter that breaks" in last.lower():
                events.append({"delta": APP_BROKEN})
            elif req["purpose"] == "build" and "The app shows this error" in last and "undefinedHelper" in last:
                events.append({"delta": EDIT_REPAIR})
            elif req["purpose"] == "build" and "say how many in words" in last.lower():
                events.append({"delta": EDIT_FITS})
            elif req["purpose"] == "build" and "add a footer" in last.lower():
                events.append({"delta": EDIT_MISSES})
            elif req["purpose"] == "build" and "did not match the current code" in last:
                events.append({"delta": APP_FOOTER})
            elif req["purpose"] == "build" and "Reply with the whole revised plan" in last:
                events.append({"reasoning": "They want a line per year; add it to the screens."})
                events.append({"delta": PLAN_V2})
            elif req["purpose"] == "build" and "a query that breaks" in last.lower():
                events.append({"delta": "I will count them.\n```query\nreturn WORKSHOP_DATA.uhri.records.map((r) => r.nothere.length);\n```"})
            elif req["purpose"] == "build" and "a checker with a form" in last.lower():
                events.append({"delta": APP_FORM})
            elif req["purpose"] == "build" and "WORKSHOP_DATA.own_1" in last:
                events.append({"delta": APP_OWN})
            elif req["purpose"] == "build":
                events.append({"reasoning": "Plan: read the country and the count from the data."})
                events.append({"delta": APP})
            elif "paragraph 97" in last:
                events.append({"delta": "Paragraph 97 calls on States Parties to integrate environmental impact assessments."})
            else:
                events.append({"delta": "About 2,000, most of them from the Universal Periodic Review."})
            for e in events:
                self.wfile.write(f"data: {json.dumps(e)}\n\n".encode())
            usage = {"model": req["model"], "model_label": "Mistral Large 3", "host": "Mistral", "zdr": True,
                     "prompt_tokens": 100, "completion_tokens": 50, "cost": 0.001, "seconds": 0.2, "budget_left": 7.4}
            self.wfile.write(f"event: usage\ndata: {json.dumps(usage)}\n\nevent: done\ndata: {{}}\n\n".encode())

    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), H) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        yield f"http://127.0.0.1:{srv.server_address[1]}/studio-api", calls
        srv.shutdown()


@pytest.fixture(scope="module")
def pw():
    with sync_playwright() as p:   # one per module: a second one cannot start while the first runs
        yield p


@pytest.fixture(scope="module")
def browser(pw):
    try:
        b = pw.chromium.launch()
    except Exception:
        b = pw.chromium.launch(channel="chrome")
    yield b
    b.close()


def started(page):
    page.wait_for_function("() => document.getElementById('countryCount').textContent !== '—' && document.querySelectorAll('#suggest button').length > 0", timeout=20000)


def built(page, n):
    page.wait_for_function(f"() => document.querySelectorAll('#versions [data-v]').length === {n} && document.getElementById('building').hidden", timeout=90000)


def app_frame(page):
    """The visible preview iframe (the studio double-buffers two)."""
    page.wait_for_selector(".viewport > iframe:not(.back)", state="attached")
    return page.frame_locator(".viewport > iframe:not(.back)")


def look(page, item):
    """Open the Look inside menu and pick an item."""
    page.click("#lookBtn")
    page.click(f"#{item}")


def add_file(page, key):
    """Put a file from the shelf into the chat: from the stage before the first app, or from the
    drawer after it."""
    if page.is_visible(f"#shelf .fcard[data-key={key}]"):
        page.click(f"#shelf .fcard[data-key={key}] [data-act=add]")
    else:
        page.click("#filesBtn")
        page.click(f"#drawerShelf .fcard[data-key={key}] [data-act=add]")
        page.click("#drawerClose")


def pick(page, title):
    """Pick a suggestion; it fills the message box (a workshop app's once its planning session has loaded)."""
    page.locator("#suggest button", has_text=title).click()
    page.wait_for_function("() => document.getElementById('input').value.trim().length > 0")


def plan_through(page, choose=()):
    """Answer each question card (option `choose[i]`, 0-based, or the recommended one) until the
    plan is offered for building."""
    i = 0
    while True:
        page.wait_for_selector(".msg.ask:not(.answered), .approve button.primary:not([disabled])", timeout=60000)
        card = page.locator(".msg.ask:not(.answered)")
        if not card.count():
            return
        k = choose[i] if i < len(choose) and choose[i] is not None else None
        (card.locator(".ask-opt").nth(k) if k is not None else card.locator(".ask-opt:has(.rec)")).click()
        i += 1


def build_plan(page):
    page.locator(".approve button.primary:not([disabled])").last.click()


def send(page, title, key=None, n=None):
    """Pick a suggestion, add the file it needs and send it. A workshop app in plan mode plays its
    planning session: the recommended answers, then Build from this plan."""
    pick(page, title)
    if key:
        add_file(page, key)
    # in Basic the Plan mode switch is not shown, but planning is on for a workshop app all the same
    planning = page.get_attribute("#planModeBtn", "hidden") is None and page.get_attribute("#planModeBtn", "aria-pressed") == "true"
    page.click("#sendBtn")
    if planning:
        plan_through(page)
        build_plan(page)
    if n:
        built(page, n)


def serve_shelf(page):
    page.route("**/data/shelf.json", lambda r: r.fulfill(status=200, content_type="application/json", body=SHELF_MOCK.read_text()))


def tool(name):
    """A module from tools/ (planning.py, shelf.py), loaded as the bake-off and the planner load it."""
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DASHBOARD = "Your country's recommendations dashboard"
WIKI = "A research wiki on neurotechnology and justice"
PACK = json.loads((SITE / "data/planning/s7-1-dashboard.json").read_text())


def test_participant_path(base_url, browser, tmp_path):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    assert page.input_value("#countrySelect") == "Kenya"
    # plan mode: the short problem in the box, the planning session, the plan, then the build
    pick(page, DASHBOARD)
    assert page.input_value("#input") == PACK["problem"].replace("{country}", "Kenya")
    assert page.get_attribute("#planModeBtn", "hidden") is None and page.get_attribute("#planModeBtn", "aria-pressed") == "true"   # on; its switch is in Advanced
    add_file(page, "uhri")
    page.click("#sendBtn")
    page.wait_for_selector(".msg.ask:not(.answered)", timeout=30000)
    assert "Simulation: this plan was written beforehand by" in page.inner_text(".plan-msg .sim")
    assert "Looked at the data: Kenya, 2,264 records" in page.locator(".plan-msg .step-label").first.inner_text()   # counted from this file
    plan_through(page)
    assert "Kenya" in page.inner_text("#planDoc")
    build_plan(page)
    built(page, 1)
    assert "Build this app. Follow the plan below" in page.locator(".msg.user").last.inner_text()
    assert page.locator(".msg.user").last.locator(".filechip").count() == 1
    assert "Built as v1" in page.locator(".approve").last.inner_text()
    frame = app_frame(page)
    frame.locator("body").get_by_text("Kenya").first.wait_for(timeout=20000)
    assert "2264" in frame.locator("body").inner_text().replace(",", "")
    assert page.locator(".lesson").count() == 1

    # Run x3: three identical checksums
    look(page, "run3Btn")
    page.wait_for_selector(".verdict", timeout=60000)
    rows = page.locator(".runs3 tbody tr")
    assert rows.count() >= 3 and page.locator(".runs3 tr.differs").count() == 0   # the app's numbers, in words
    assert "2,264" in page.inner_text(".runs3") and not re.search(r"\b0\d [A-Z]", page.inner_text(".runs3"))   # no "01 OVERVIEW" labels
    assert "The same answer, three times" in page.inner_text(".verdict")
    page.click("#drawerClose")

    # Trace: one recorded build, nothing sent, data kept
    look(page, "traceBtn")
    body = page.inner_text("#drawerBody")
    assert "would be sent to a live model" in body.lower() and "2,264" in body
    page.click("#drawerClose")

    # Save as file: one file that runs offline from disk
    with page.expect_download() as dl:
        page.click("#keepBtn")
        page.click("#downloadBtn")
    path = tmp_path / dl.value.suggested_filename
    dl.value.save_as(path)
    html = path.read_text()
    assert "WORKSHOP_DATA" in html and "Content-Security-Policy" in html
    off = ctx.new_page()
    requests = []
    off.route("**/*", lambda r: (requests.append(r.request.url) if not r.request.url.startswith("file:") else None) or (r.continue_() if r.request.url.startswith("file:") else r.abort()))
    off.goto(path.as_uri())
    off.wait_for_timeout(1500)
    assert "Kenya" in off.inner_text("body")
    assert not requests, requests
    off.close()

    # a reload keeps the version, its thinking, its lesson and the trace
    page.reload()
    page.wait_for_function("() => document.querySelectorAll('#versions [data-v]').length === 1")
    if (SITE / "replay/claude/s7-1-dashboard.thought.md").exists():   # builds made in Claude Code have no recorded thinking
        assert page.locator(".thought summary").first.inner_text().startswith("Thought")
    assert page.locator(".lesson").count() == 1
    assert page.inner_text("#traceCount") == "1"

    assert not errors, errors
    ctx.close()


def test_what_is_shown_grows_with_progress(base_url, browser):
    """Hick's law: one card and no tools before the first app; tools after it."""
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    assert not page.is_visible("#toolbar")
    assert page.is_visible("#composer") and page.locator("#shelf .fcard[data-key]").count() == len([f for f in json.loads((SITE / "config.json").read_text())["files"] if "venice" not in f])
    assert page.locator("#suggest button").count() <= 3
    send(page, DASHBOARD, "uhri", 1)
    assert page.is_visible("#toolbar") and not page.is_visible("#shelf")
    assert page.locator("#suggest button").count() <= 3
    page.click("#lookBtn")
    assert page.is_visible("#run3Btn") and page.is_visible("#traceBtn") and not page.is_visible("#ask3Btn")   # Ask directly: Session 2
    assert page.locator("#layersBtn, #linkBtn").count() == 0 and page.locator("#lookBtn .count").count() == 0
    page.keyboard.press("Escape")
    # the toolbar fits on one row at 1280 px
    assert page.evaluate("() => document.getElementById('toolbar').getBoundingClientRect().height") < 60
    ctx.close()


TOP_OVERLAPS = """() => {
  const b = document.getElementById('budget'); b.hidden = false; b.textContent = '$7.50 left';
  const r = ['.brand', '.session', '#countryChip', '.model-pick', '#modelBadge', '.top-link', '#routeBadge', '#budget']
    .map((s) => document.querySelector(s)).filter((e) => getComputedStyle(e).display !== 'none')
    .map((e) => [e.className || e.id, e.getBoundingClientRect()]).filter((x) => x[1].width > 0);
  const bad = [];
  for (let i = 0; i < r.length - 1; i++) if (r[i][1].right > r[i + 1][1].left + 0.5) bad.push(r[i][0] + ' > ' + r[i + 1][0]);
  if (r[r.length - 1][1].right > innerWidth) bad.push('off screen');
  return bad;
}"""

SQUEEZED = "() => [...document.querySelectorAll('#log > *')].filter((e) => e.getBoundingClientRect().height < Math.min(e.scrollHeight, 120) - 2).map((e) => e.className)"


@pytest.mark.parametrize("engine", ["chromium", "webkit"])
def test_layout_holds_on_a_small_laptop(base_url, pw, browser, engine):
    """At 1000 and 1280 px, in Chrome and Safari's engine: nothing in the top bar overlaps, and a
    full chat log scrolls instead of squeezing a message to a sliver."""
    if engine == "webkit":
        try:
            b = pw.webkit.launch()
        except Exception as e:
            pytest.skip(f"WebKit not installed: {e}")
    else:
        b = browser
    for w, h in ((1000, 560), (1280, 720)):
        page = b.new_page(viewport={"width": w, "height": h})
        page.goto(base_url + "?via=replay&planpace=1&country=United%20Kingdom%20of%20Great%20Britain%20and%20Northern%20Ireland")
        started(page)
        assert page.evaluate(TOP_OVERLAPS) == [], (engine, w)
        send(page, DASHBOARD, "uhri", 1)
        assert page.evaluate(SQUEEZED) == [], (engine, w)
        # the conversation, not the chips and the box, gets most of the column
        share = page.evaluate("() => document.getElementById('log').clientHeight / document.querySelector('.chat').clientHeight")
        assert share >= 0.45, (engine, w, round(share, 2))
        page.close()
    if engine == "webkit":
        b.close()


def test_extraction_from_pdf(base_url, browser):
    """The recorded 'Paragraphs out of a PDF' app runs on the converter's page text, checks itself against
    the reference shipped with it and flags the paragraphs where footnote text may sit; picking it switches
    the studio to the model it runs on best."""
    if not (SITE / "replay/claude/s7-4-extract.md").exists():
        pytest.skip("no recording for s7-4-extract yet")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")   # the extraction is in Session 8
    started(page)
    page.select_option("#modelSelect", "mistral")                       # someone who picked another model
    send(page, "Paragraphs out of a PDF", "pdf_text", 1)
    assert page.locator("#modelSelect").input_value() == "claude"
    assert "This exercise runs on Claude Sonnet 5.5" in page.inner_text("#log")
    body = app_frame(page).locator("body")
    body.get_by_text("E/C.12/GC/27").first.wait_for(timeout=20000)
    text = body.inner_text()
    assert re.search(r"90\s*(paragraphs\s*)?(/|of)\s*90", text, re.I), text[:400]
    assert "141" in text, text[:400]                                     # the footnotes, not separated
    assert re.search(r"paragraphs? flagged|flagged paragraphs?", text, re.I), text[:400]
    assert page.locator(".lesson").inner_text().count("format decides") == 1
    # the PDF's next steps are hidden: the extraction ends here, with Suggest improvements when live
    nexts = page.locator("#suggest button b").all_inner_texts()
    assert "Add a second document" not in nexts and "A model for the pages that fail" not in nexts, nexts
    assert not errors, errors
    ctx.close()


def test_live_country_switch_and_asking_directly(base_url, browser, fake_api):
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?advanced=1&api={api}&planpace=1#s=TEST22")
    started(page)
    assert page.input_value("#countrySelect") == "Colombia"   # the seat's country
    assert "Live" in page.inner_text("#routeBadge") and "7.50" in page.inner_text("#budget")
    assert page.locator("#countrySelect option").count() > 150
    send(page, DASHBOARD, "uhri", 1)
    frame = app_frame(page)
    frame.get_by_text("Colombia 2150").wait_for(timeout=10000)
    frame.locator("#jump").click()   # an in-page link must stay in the app, not load the studio inside it
    page.wait_for_timeout(500)
    assert app_frame(page).locator("#c").inner_text() == "Colombia 2150"
    assert calls[-1]["purpose"] == "build" and all(m["role"] != "system" for m in calls[-1]["messages"])
    assert page.locator(".msg.assistant:not(.plan-msg) .thought summary").first.inner_text().startswith("Thought")   # the build's thinking

    # another country: the same code runs on other records, and no model is asked
    n = len(calls)
    page.select_option("#countrySelect", "Kenya")
    app_frame(page).get_by_text("Kenya 2264").wait_for(timeout=10000)
    assert "same code, different data" in page.locator(".msg.note").last.inner_text()
    assert len(calls) == n and page.locator("#versions [data-v]").count() == 1

    # a chatbot: small talk gets an answer in words, and no new version
    page.fill("#input", "How are you?")
    page.keyboard.press("Enter")
    page.wait_for_function("() => [...document.querySelectorAll('.msg.assistant .answer-md')].some((e) => e.textContent.includes('well, thank you'))", timeout=15000)
    assert page.locator("#versions [data-v]").count() == 1
    assert "(Attached:" in calls[-1]["messages"][0]["content"]   # the file named earlier is still in the conversation

    # Session 8: a new conversation (the country file goes in again); asking the model directly, a number, then a
    # paragraph that does not exist
    page.get_by_role("tab", name="Session 2").click()
    assert page.locator("#versions [data-v]").count() == 0 and page.locator(".msg.assistant").count() == 0
    add_file(page, "uhri")
    page.fill("#input", "Build a counter")
    page.click("#sendBtn")
    built(page, 1)
    look(page, "ask3Btn")
    page.wait_for_function("() => document.getElementById('truth').textContent.includes('records in total')")
    page.get_by_role("tab", name="A quotation").click()
    page.wait_for_function("() => document.getElementById('askNote').textContent.includes('no paragraph 97')", timeout=15000)
    assert "There is no paragraph 97: E/C.12/GC/27 has 90 numbered paragraphs" in page.inner_text("#truth")
    assert sum(1 for c in calls if c["purpose"] == "question" and "paragraph 97" in c["messages"][-1]["content"]) == 3
    assert page.inner_text("#traceCount") == "7"   # this session's: one build, three counts, three quotations
    page.click("#drawerClose")

    # the app in a tab of its own: still sandboxed, and its model requests still go through the studio
    with ctx.expect_page() as tab_info:
        page.click("#tabBtn")
    tab = tab_info.value
    tab.wait_for_function("() => document.getElementById('title').textContent.startsWith('v1')", timeout=15000)
    assert tab.get_attribute("#frame", "sandbox").startswith("allow-scripts") and "allow-same-origin" not in tab.get_attribute("#frame", "sandbox")
    tab.frame_locator("#frame").get_by_text("Kenya 2264").wait_for(timeout=10000)
    answer = tab.frames[1].evaluate("() => studio.ask('Say hello')")
    assert "2,000" in answer
    assert page.inner_text("#traceCount") == "8"
    assert not errors, errors
    ctx.close()


def test_session8_offers_its_apps_first(base_url, browser):
    """Session 8 starts with the PDF extraction, the Verbatim finder and the research wiki; the
    briefing check is an extra that appears once they are built (Hick's law: the plan's apps first)."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?advanced=1&via=replay&planpace=1&stage=s8&country=Kenya")
    started(page)
    titles = page.locator("#suggest button b").all_inner_texts()
    assert titles[:3] == ["Paragraphs out of a PDF", "Verbatim finder for General Comments", "A research wiki on neurotechnology and justice"], titles
    assert "Check an AI briefing" not in titles
    send(page, "Paragraphs out of a PDF", "pdf_text", 1)
    send(page, "Verbatim finder", "gc", 2)
    send(page, "A research wiki", "wiki", 3)
    send(page, "Check an AI briefing", "hrc", 4)
    body = app_frame(page).locator("body")
    body.locator("select, h1").first.wait_for(timeout=20000)
    assert "51/27" in body.inner_text() + " ".join(body.locator("option:checked").all_inner_texts())
    assert not errors, errors
    ctx.close()


def test_a_request_needs_its_file_and_a_drag_gives_it(base_url, browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    pick(page, DASHBOARD)
    problem = page.input_value("#input")
    assert page.is_visible("#needs") and "Kenya" in page.inner_text("#needs")
    page.click("#sendBtn")
    assert page.locator(".plan-msg").count() == 0 and "needs the file" in page.locator(".msg.note").last.inner_text()
    assert "needed" in page.get_attribute("#shelf .fcard[data-key=uhri]", "class")
    # a real drag from the shelf into the chat
    page.drag_and_drop("#shelf .fcard[data-key=uhri]", "#input")
    assert page.locator("#attach .filechip").count() == 1 and not page.is_visible("#needs")
    assert page.input_value("#input") == problem   # dropped as a file, not as text
    page.click("#sendBtn")
    plan_through(page)
    build_plan(page)
    built(page, 1)
    ctx.close()


def test_open_a_file_code_view_and_dark_mode(base_url, browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    # a country file opens as a spreadsheet: one header row and one row per record
    with page.expect_download() as dl:
        page.click("#shelf .fcard[data-key=uhri] [data-act=open]")
    csv = Path(dl.value.path()).read_text(encoding="utf-8-sig")
    assert csv.startswith("id,symbol,doc_url") and csv.count("\r\nfa") + 1 > 0
    assert dl.value.suggested_filename == "un-recommendations-kenya.csv"
    # the UN document is the PDF; it opens in the browser
    assert page.locator("#shelf .fcard[data-key=pdf_text] .ficon").inner_text() == "PDF"
    send(page, DASHBOARD, "uhri", 1)
    page.click("#viewCode")
    assert page.is_visible("#codeView") and "<!doctype html>" in page.inner_text("#codeText").lower()
    assert page.locator("#codeText .tk-tag").count() > 20
    page.click("#viewApp")
    assert not page.is_visible("#codeView")
    page.click("#themeBtn")
    assert page.evaluate("() => document.documentElement.dataset.theme") == "dark"
    assert page.evaluate("() => getComputedStyle(document.body).backgroundColor") != "rgb(242, 244, 247)"
    assert "Szoszkiewicz" in page.inner_text("#foot")
    page.click("#takeHomeBtn")
    assert "github.com/lszoszk" in page.input_value("#tfPrompt")
    ctx.close()


def test_the_divider_is_dragged_kept_and_reset(base_url, browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    width = lambda: page.evaluate("() => document.querySelector('.chat').getBoundingClientRect().width")
    w0 = width()
    box = page.locator("#splitter").bounding_box()
    x, y = box["x"] + box["width"] / 2, box["y"] + 200
    page.mouse.move(x, y)
    page.mouse.down()
    page.mouse.move(x + 180, y, steps=6)
    page.mouse.up()
    assert abs(width() - (w0 + 180)) < 6
    page.reload()
    started(page)
    assert abs(width() - (w0 + 180)) < 6   # kept in this browser
    page.dblclick("#splitter")
    assert abs(width() - w0) < 2
    page.mouse.move(x, y)                  # never narrower than the minimum, never wider than 65 %
    page.mouse.down()
    page.mouse.move(5, y, steps=4)
    page.mouse.up()
    assert 279 <= width() <= 281
    ctx.close()


def test_a_pdf_opens_next_to_the_app(base_url, browser):
    """studio.openSource from inside an app opens the PDF at its page in the studio's drawer, with
    the printed page where it differs and the quoted passage marked; the library card lists every PDF
    in the library."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    page.click("#shelf .fcard[data-key=library] [data-act=open]")
    page.wait_for_selector("#drawerBody .tool-card")
    assert page.locator("#drawerBody .tool-card").count() == len(json.loads((SITE / "data/library.json").read_text())["records"])
    page.click("#drawerClose")
    send(page, DASHBOARD, "uhri", 1)
    app_frame(page).locator("body").wait_for()
    frame = page.locator(".viewport > iframe:not(.back)").element_handle().content_frame()   # the app on stage
    frame.evaluate("() => studio.openSource('CCPR/C/GC/32', 5)")
    page.wait_for_selector("#drawer.wide .pdfpage canvas")   # drawn by PDF.js
    assert page.locator(".src-head a").first.get_attribute("href") == "files/CCPR_C_GC_32.pdf#page=5"
    assert "PDF page 5 of" in page.inner_text("#pdfNote") and page.locator("#drawer .pdfmark").count() == 0
    assert page.request.get(base_url + "files/CCPR_C_GC_32.pdf").status == 200
    frame.evaluate("() => studio.openSource('Szoszkiewicz-Yuste-2025', 3)")
    page.wait_for_function("() => document.getElementById('drawerTitle').textContent.includes('p. 3471')")
    page.wait_for_selector("#drawer.wide .pdfpage canvas")
    assert page.locator(".src-head a").first.get_attribute("href") == "files/Szoszkiewicz-Yuste-2025.pdf#page=3"
    assert page.request.get(base_url + "files/Szoszkiewicz-Yuste-2025.pdf").status == 200
    # with a quote: the passage is marked, across a line break and curly quotes
    frame.evaluate("() => studio.openSource('A/81/351', 3, 'defined as \u201cqualitative and quantitative data about the structure, activity and function of the nervous system')")
    page.wait_for_function("() => /is marked/.test(document.getElementById('pdfNote').textContent)")
    assert page.locator("#drawer .pdfmark").count() >= 2
    page.click("#pdfNote button[data-to='4']")
    page.wait_for_function("() => /PDF page 4 of/.test(document.getElementById('pdfNote').textContent)")
    ctx.close()


def test_the_wiki_links_every_paragraph_to_its_pdf_page(base_url, browser):
    if not (SITE / "replay/claude/s8-5-wiki.md").exists():
        pytest.skip("no recording for s8-5-wiki yet")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?advanced=1&via=replay&planpace=1&stage=s8&country=Kenya")
    started(page)
    send(page, "A research wiki", "wiki", 1)
    frame = app_frame(page)
    frame.get_by_text(re.compile(r"^\s*mental privacy", re.I)).first.click()
    frame.get_by_text(re.compile(r"(para\.\s*\d+|p\.\s*\d{4})")).first.click()
    opener = frame.get_by_role("button", name=re.compile(r"open the pdf", re.I))   # a pin may open a card first
    if opener.count():
        opener.first.click()
    page.wait_for_selector("#drawer.wide .pdfpage canvas")   # PDF.js draws the page; the pin's quote is marked on it
    assert re.fullmatch(r"files/[\w.\-]+\.pdf#page=\d+", page.locator(".src-head a").first.get_attribute("href"))
    page.wait_for_function("() => /marked|not found/.test(document.getElementById('pdfNote').textContent)")
    assert "is marked" in page.inner_text("#pdfNote") and page.locator("#drawer .pdfmark").count() > 0
    if (SITE / "replay/claude/s8-6-wiki-map.md").exists():   # the follow-up: a map of the pages' links
        page.click("#drawerClose")
        send(page, "A map of the wiki")
        built(page, 2)
        app_frame(page).get_by_role("tab", name=re.compile("map", re.I)).click()
        assert app_frame(page).locator("svg circle, svg rect, svg polygon, svg path").count() >= 40   # 40 pages, any shape
    ctx.close()


def test_the_wall_shows_what_participants_sent(base_url, browser, fake_api):
    """Send to wall puts an app on the facilitator's wall with the country and files it ran on; the wall
    draws each as a live thumbnail, and a click opens it full screen on the same data."""
    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?advanced=1&api={api}&planpace=1#s=TEST22")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    page.click("#keepBtn")
    page.click("#wallBtn")
    page.wait_for_function("() => /Sent to the wall/.test(document.getElementById('log').innerText)")
    # a second participant's app, given two files in the chat
    app = re.search(r"```html\s*(.*?</html>)", (SITE / "replay/claude/s7-5-second-document.md").read_text(), re.S).group(1)
    req = urllib.request.Request(api + "/gallery", method="POST", headers={"Content-Type": "application/json"},
                                 data=json.dumps({"seat": "TEST22", "title": "Two General Comments", "model": "claude", "country": "Kenya",
                                                  "files": ["pdf_text", "pdf_text_2"], "html": app}).encode())
    urllib.request.urlopen(req).read()
    page.goto(base_url + f"wall.html?api={api}")
    page.wait_for_function("() => document.querySelectorAll('.tile').length === 2")
    caps = page.locator(".tile .cap").all_inner_texts()
    assert "COLOMBIA" in caps[1].upper() and "KENYA" in caps[0].upper(), caps   # newest first; the studio sent the seat's country
    page.wait_for_function("() => document.querySelectorAll('.thumb iframe').length === 2", timeout=30000)
    page.locator(".tile").first.click()
    page.wait_for_url("**/gallery/view.html?wall=*")
    body = page.frame_locator("#frame").locator("body")
    body.get_by_text("CCPR/C/GC/32").first.wait_for(timeout=20000)   # the second file reached the app
    assert "Two General Comments" in page.inner_text(".bar")
    assert not errors, errors
    ctx.close()


def test_a_tester_sends_feedback_with_its_context(base_url, browser, fake_api):
    """Feedback in the footer: the tester's words go to the server with the page's context (version,
    model, the app on stage), shown before sending; never data or an app's code."""
    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    page.click("#feedbackBtn")
    page.locator("#feedbackDialog summary").click()
    shown = page.inner_text("#feedbackCtx")
    assert "model" in shown and "app" in shown and "v1" in shown
    page.fill("#feedbackText", "The chart labels overlap on a small screen")
    page.click("#feedbackSend")
    page.wait_for_function("() => /Thank you/.test(document.getElementById('log').innerText)")
    sent = FEEDBACK[-1]
    assert sent["seat"] == "TEST22" and sent["text"] == "The chart labels overlap on a small screen"
    payload = json.dumps(sent)
    assert sent["context"]["version"] and "v1" in sent["context"]["app"]
    assert "<!doctype" not in payload.lower() and "WORKSHOP_DATA" not in payload   # no app code, no data
    ctx.close()


def test_the_tour_from_the_footer(base_url, browser):
    """The tour lights one part of the studio at a time; Tour in the footer starts it again. It does not
    start by itself in an automated browser, so it never stands in the way of the other tests."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    assert page.locator(".tour").count() == 0
    page.click("#tourBtn")
    titles = []
    for _ in range(8):
        titles.append(page.locator(".tour-card h3").inner_text())
        page.locator(".tour-card [data-t=next]").click()
    assert titles[0] == "Welcome to Garage Research" and len(set(titles)) == 8
    assert page.locator(".tour").count() == 0 and page.evaluate("localStorage.getItem('ws:toured')") == "1"
    page.click("#tourBtn")
    page.keyboard.press("Escape")
    assert page.locator(".tour").count() == 0
    ctx.close()


def test_the_library_stands_for_the_wiki(base_url, browser):
    """The wiki request needs the wiki, which brings the library with it: a participant who drags the
    library gets the wiki attached instead, with a note, and can send."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")
    started(page)
    pick(page, "A research wiki")
    add_file(page, "library")
    assert [c.get_attribute("data-key") for c in page.locator("#attach .filechip button").all()] == ["wiki"]
    assert page.is_hidden("#needs")
    assert "brings" in page.locator(".msg").last.inner_text()
    ctx.close()


def plain_md(s):
    """A Markdown fragment as the plan on the stage shows it: no list marks, bold or code marks."""
    return re.sub(r"^\s*([-*]|\d+\.)\s+", "", re.sub(r"[*`_]", "", s)).strip()


def test_plan_mode_in_recorded_mode(base_url, browser):
    """The planning session plays without a model: Stop gives the request back; a question is a card
    with fixed answers; each answer is the participant's message; the plan is a document on the stage
    with the facilitator's brief beside it; recorded mode builds only the recommended answers and
    cannot change a plan."""
    ctx = browser.new_context(viewport={"width": 1366, "height": 800})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?advanced=1&via=replay&planpace=6&country=Kenya")
    started(page)
    pick(page, DASHBOARD)
    page.click("#planModeBtn")
    assert page.get_attribute("#planModeBtn", "aria-pressed") == "false"
    page.click("#planModeBtn")
    assert page.get_attribute("#planModeBtn", "aria-pressed") == "true"
    add_file(page, "uhri")
    page.click("#sendBtn")
    page.wait_for_selector(".plan-msg .step")
    assert page.is_visible("#mind") and "is planning" in page.inner_text("#mindTitle")
    page.click("#stopBtn")
    page.wait_for_function("() => document.querySelector('.plan-msg .msg.err')")
    assert "back in the box" in page.inner_text(".plan-msg .msg.err")
    assert page.input_value("#input") == PACK["problem"] and page.locator("#attach .filechip").count() == 1
    ctx.close()

    ctx = browser.new_context(viewport={"width": 1366, "height": 800})
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?advanced=1&via=replay&planpace=1&country=Kenya")
    started(page)
    pick(page, DASHBOARD)
    add_file(page, "uhri")
    page.click("#sendBtn")
    card = page.locator(".msg.ask:not(.answered)")
    card.wait_for(timeout=30000)
    q = PACK["questions"][0]
    assert card.locator(".ask-chip").inner_text() == q["header"] and q["question"] in card.inner_text()
    assert f"Question 1 of {len(PACK['questions'])}" in card.inner_text()
    assert card.locator(".ask-opt").count() == len(q["options"]) and card.locator(".ask-opt .rec").count() == 1
    assert card.locator(".ask-opt small").all_inner_texts() == [o["description"] for o in q["options"]]
    assert card.locator("input, textarea").count() == 0   # fixed answers, no free text
    assert "Recorded mode builds only the recommended answers" in card.inner_text()
    other = next(k for k, o in enumerate(q["options"]) if not o.get("default"))
    plan_through(page, [other])
    assert page.locator(".msg.user").nth(1).inner_text() == q["options"][other]["label"]   # the answer, as the participant's message
    assert page.locator(".msg.ask.answered").count() == len(PACK["questions"]) and page.locator(".msg.ask .ask-opt").count() == 0
    # the plan on the stage: the version that answer chose, to read, not a form
    doc = page.inner_text("#planDoc")
    assert plain_md(q["options"][other]["fragments"][0]["text"])[:40] in doc
    assert page.locator("#planDoc input, #planDoc select, #planDoc textarea, #planDoc [contenteditable]").count() == 0
    assert "written beforehand" in page.text_content("#planKicker")
    page.click("#planBrief")
    assert page.inner_text("#drawerTitle") == "Facilitator's brief" and PACK["facilitator_brief"][:60] in page.inner_text("#drawerBody")
    page.click("#drawerClose")
    # Build: recorded mode has only the app built from the recommended answers
    build_plan(page)
    assert "only the plan with the recommended answers" in page.locator(".msg.note").last.inner_text()
    page.locator(".approve button.ghost").last.click()   # Change something
    assert "no model is connected" in page.locator(".msg.note").last.inner_text()
    page.wait_for_timeout(300)
    assert page.locator("#versions [data-v]").count() == 0 and page.is_visible("#planView")
    # closed, the plan opens again from its card in the chat
    page.click("#planClose")
    page.locator(".plan-card").last.click()
    assert page.is_visible("#planView")
    assert not errors, errors
    ctx.close()


def test_a_plan_is_changed_live_and_built(base_url, browser, fake_api):
    """Build sends the composed plan, word for word what tools/planning.py composes; Change something
    goes live to the participant's model with the plan, and plan v2 goes on the stage and is built."""
    api, calls = fake_api
    compose = tool("planning").compose
    ctx = browser.new_context(viewport={"width": 1366, "height": 800})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    sent = calls[-1]["messages"][-1]["content"]
    assert sent.startswith(compose(PACK, {}, "Colombia") + "\n\n(Attached: Colombia: UN recommendations"), sent[:300]
    ctx.close()

    ctx = browser.new_context(viewport={"width": 1366, "height": 800})
    page = ctx.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    pick(page, DASHBOARD)
    add_file(page, "uhri")
    page.click("#sendBtn")
    plan_through(page)
    n = len(calls)
    page.locator(".approve button.ghost").last.click()   # Change something
    assert page.input_value("#input") == "Change the plan: "
    page.keyboard.type("add a line chart of the records per year.")
    page.keyboard.press("Enter")
    page.wait_for_function("() => document.getElementById('planKicker').textContent.startsWith('Plan v2 · changed')", timeout=15000)
    assert len(calls) == n + 1 and calls[-1]["purpose"] == "build" and len(calls[-1]["messages"]) == 1
    asked = calls[-1]["messages"][0]["content"]
    assert compose(PACK, {}, "Colombia").split("\n\n", 1)[1] in asked and "Change the plan: add a line chart" in asked
    assert "changed live by GLM-5.3 (run in the EU)" in page.text_content("#planKicker")
    assert "A line chart of the records per year." in page.inner_text("#planDoc") and "revised plan" not in page.inner_text("#planDoc")
    assert page.locator(".plan-msg .thought").last.inner_text().startswith("Thought")
    assert page.locator(".approve button.primary[disabled]").count() == 1   # v1's Build is retired
    build_plan(page)
    built(page, 1)
    assert calls[-1]["messages"][-1]["content"].startswith(
        "Build this app. Follow the plan below; where it says nothing, keep it simple.\n\n## Context\nThe same dashboard, revised.")
    look(page, "traceBtn")
    assert "The plan you asked to change (v1" in page.inner_text("#drawerBody")
    assert not errors, errors
    ctx.close()


def test_the_reference_shelf_goes_out_with_a_message(base_url, browser, fake_api):
    """A message that matches the shelf takes its best passages along, scored as tools/shelf.py
    scores them; the step opens each page in the drawer and the trace lists what went out. Small
    talk takes nothing."""
    api, calls = fake_api
    shelf = tool("shelf")
    records = json.loads(SHELF_MOCK.read_text())["records"]
    shelf.load = lambda: records
    ctx = browser.new_context(viewport={"width": 1366, "height": 800})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    serve_shelf(page)
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    page.fill("#input", "Build me a small app that counts my records.")   # an app first: the trace is under Look inside
    page.keyboard.press("Enter")
    built(page, 1)
    question = "How should a bar chart show its labels, and what contrast do the bars need?"
    page.fill("#input", question)
    page.keyboard.press("Enter")
    page.wait_for_function("() => [...document.querySelectorAll('.answer-md')].some((e) => e.textContent.includes('label them directly'))", timeout=15000)
    step = page.locator(".msg.assistant .step").last
    titles = step.locator(".step-pages button").all_inner_texts()
    ranked = [h["title"] for h in shelf.search(question)]
    assert len(titles) >= 2 and titles == ranked[:len(titles)], (titles, ranked)
    assert f"Searched the reference shelf · {len(titles)} pages" in step.inner_text()
    sent = calls[-1]["messages"][-1]["content"]
    assert sent.startswith(question + "\n\nReference shelf excerpts (offline copies)")
    assert all(f"] {t}." in sent for t in titles)
    step.locator(".step-pages button").first.click()
    assert page.inner_text("#drawerTitle") == titles[0]
    drawer = page.inner_text("#drawerBody").lower()
    assert "sent to the model with your message" in drawer and "offline copy" in drawer
    look(page, "traceBtn")
    assert "excerpts from the workshop reference shelf" in page.inner_text("#drawerBody")
    page.click("#drawerClose")
    # small talk takes nothing from the shelf
    steps = page.locator(".msg.assistant .step").count()
    page.fill("#input", "How are you?")
    page.keyboard.press("Enter")
    page.wait_for_function("() => [...document.querySelectorAll('.answer-md')].some((e) => e.textContent.includes('well, thank you'))", timeout=15000)
    assert page.locator(".msg.assistant .step").count() == steps and "Reference shelf" not in calls[-1]["messages"][-1]["content"]
    # the step is kept with the conversation
    page.reload()
    started(page)
    assert page.locator(".msg.assistant .step").count() == 1
    assert not errors, errors
    ctx.close()


def test_recorded_mode_refuses_free_requests(base_url, browser):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    page.fill("#input", "Make the chart red.")
    page.click("#sendBtn")
    assert "recorded answers" in page.locator(".msg.note").last.inner_text()
    assert page.input_value("#input") == "Make the chart red."
    page.wait_for_timeout(500)
    assert page.locator("#versions [data-v]").count() == 1
    ctx.close()


def test_phone_gets_the_handoff_page(base_url, browser):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    page.goto(base_url + "#s=K7Q2MA")
    page.wait_for_selector("#handoff:not([hidden])")
    assert page.inner_text("#handoffCode") == "K7Q2MA"
    assert "#s=K7Q2MA" in page.get_attribute("#handoffMail", "href").replace("%23", "#").replace("%3D", "=")
    assert not page.is_visible(".work")
    assert page.evaluate("() => localStorage.getItem('ws:seat')") is None
    ctx.close()


def test_no_jargon_in_the_studio_itself(base_url, browser):
    """The words a participant reads around their app (not the model's own summary or code)."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    texts = [page.inner_text(".top"), page.inner_text("#toolbar"), page.inner_text("#suggest"), page.inner_text(".lesson")]
    page.click("#lookBtn")
    texts.append(page.inner_text("#lookPanel"))
    page.click("#run3Btn")
    page.wait_for_selector(".verdict", timeout=60000)
    texts.append(page.inner_text("#drawerBody"))
    look(page, "traceBtn")
    texts.append(page.locator("#drawerBody").evaluate("b => { const c = b.cloneNode(true); c.querySelectorAll('details').forEach(d => d.remove()); return c.innerText; }"))
    hits = [m.group(0) for t in texts for m in JARGON.finditer(t)]
    assert not hits, hits
    ctx.close()


def test_a_gallery_app_comes_into_the_studio(base_url, browser):
    """The back-up when a plan or a build fails: Improve it in the studio brings a gallery app in as v1, in its
    session, with the plan it was built from as the request the model will see before the next change."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&country=Kenya&from=sonnet-tabs%2Fs7-4-extract")
    started(page)
    built(page, 1)
    assert "from=" not in page.url
    assert page.get_attribute("#sessionSwitch [data-session=S8]", "aria-selected") == "true"
    assert "From the gallery: Paragraphs out of a PDF" in page.inner_text("#log")
    app_frame(page).get_by_text(re.compile(r"paragraphs? flagged|flagged paragraphs?", re.I)).first.wait_for(timeout=20000)
    work = page.evaluate("JSON.parse(localStorage.getItem('ws:work:guest:geneva:S8'))")   # the conversation of its session
    assert work["versions"][0]["sent"].startswith("Build this app.") and "```html" in work["versions"][0]["reply"]
    page.goto(base_url + "?via=replay&country=Kenya&from=nobody%2Fnothing")
    started(page)
    assert "could not be loaded" in page.inner_text("#log")
    ctx.close()


def test_edit_mode_changes_only_what_was_asked(base_url, browser, fake_api):
    """A change comes back as edits: the studio applies them to the app on the stage, says how much changed, and
    sends the model the whole new code next time. Edits that do not fit make it ask once for the whole file."""
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    app_frame(page).get_by_text("Colombia 2150").wait_for(timeout=10000)
    page.fill("#input", "Say how many in words.")
    page.click("#sendBtn")
    built(page, 2)
    app_frame(page).get_by_text("Colombia: 2150 records").wait_for(timeout=10000)
    assert "changed 1 of" in page.locator(".msg.assistant .code .bar").last.inner_text()
    n = len(calls)
    page.fill("#input", "Add a footer.")
    page.click("#sendBtn")
    built(page, 3)
    assert len(calls) == n + 2                                         # the edits, then the whole file
    assert "did not match the current code" in calls[-1]["messages"][-1]["content"]
    assert "u.country + ': ' + u.count" in calls[-1]["messages"][-4]["content"]   # v2's whole code went with the request
    app_frame(page).get_by_text("Source: UHRI").wait_for(timeout=10000)
    assert "did not fit your app" in page.locator(".retry-note").last.inner_text()
    assert not errors, errors
    ctx.close()


def test_an_app_that_fails_as_it_opens_is_repaired_once(base_url, browser, fake_api):
    """A new live version that throws in its first seconds goes back to the model once, as an edit, with a note in
    the chat; the repaired version is never repaired automatically again."""
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?advanced=1&api={api}&planpace=1#s=TEST22")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    app_frame(page).get_by_text("Colombia 2150").wait_for(timeout=10000)
    page.fill("#input", "Make it a counter that breaks.")
    page.click("#sendBtn")
    built(page, 3)                                                     # the broken version, then its repair
    assert "The app shows this error" in calls[-1]["messages"][-1]["content"] and "undefinedHelper" in calls[-1]["messages"][-1]["content"]
    assert "sends it back to the model to fix, once" in page.locator(".msg.note").last.inner_text()
    app_frame(page).get_by_text("Colombia 2150").wait_for(timeout=10000)
    assert page.is_hidden("#appError")
    ctx.close()


# ---------- the participant's own files ----------

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def own_fixtures(tmp):
    """One small file of each kind the studio reads, written the way Excel and Word write them (zip of XML)."""
    import zipfile
    (tmp / "mine.csv").write_bytes('\ufeffName;Count;Code\n"Smith; J.";12;007\nŁódź;3;\n'.encode("utf-8"))
    (tmp / "mine.json").write_text('[{"a": 1, "b": "x"}, {"a": 2, "b": null}]')
    with zipfile.ZipFile(tmp / "mine.xlsx", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("xl/workbook.xml", '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
                   '<sheet name="Recs" sheetId="1" r:id="rId1"/><sheet name="Notes" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Target="/xl/worksheets/sheet2.xml"/></Relationships>')
        z.writestr("xl/sharedStrings.xml", '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                   '<si><t>Country</t></si><si><t>Date</t></si><si><t>Kenya</t></si><si><r><t>Ma</t></r><r><t>li</t></r></si></sst>')
        z.writestr("xl/styles.xml", '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                   '<cellXfs count="2"><xf numFmtId="0"/><xf numFmtId="14"/></cellXfs></styleSheet>')
        z.writestr("xl/worksheets/sheet1.xml", '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
                   '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c><c r="C1" t="inlineStr"><is><t>Votes</t></is></c></row>'
                   '<row r="2"><c r="A2" t="s"><v>2</v></c><c r="B2" s="1"><v>46000</v></c><c r="C2"><v>12</v></c></row>'
                   '<row r="4"><c r="A4" t="s"><v>3</v></c><c r="C4"><v>7.5</v></c></row></sheetData></worksheet>')
        z.writestr("xl/worksheets/sheet2.xml", '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
                   '<row r="1"><c r="A1" t="inlineStr"><is><t>Note</t></is></c></row>'
                   '<row r="2"><c r="A2" t="b"><v>1</v></c></row></sheetData></worksheet>')
    with zipfile.ZipFile(tmp / "mine.docx", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", f'<w:document {W}><w:body>'
                   '<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>I. Introduction</w:t></w:r></w:p>'
                   '<w:p><w:r><w:t xml:space="preserve">1. A clean environment</w:t></w:r><w:r><w:footnoteReference w:id="2"/></w:r>'
                   '<w:r><w:t xml:space="preserve"> matters.</w:t></w:r></w:p><w:p></w:p>'
                   '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Cell text</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
                   '<w:p><w:del><w:r><w:delText>gone </w:delText></w:r></w:del><w:r><w:t>2. Second</w:t></w:r></w:p></w:body></w:document>')
        z.writestr("word/footnotes.xml", f'<w:footnotes {W}><w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:t>---</w:t></w:r></w:p></w:footnote>'
                   '<w:footnote w:id="2"><w:p><w:r><w:t>See E/C.12/GC/27.</w:t></w:r></w:p></w:footnote></w:footnotes>')
    (tmp / "old.xls").write_bytes(b"\xd0\xcf\x11\xe0")
    return [tmp / n for n in ("mine.csv", "mine.json", "mine.xlsx", "mine.docx", "old.xls")]


def test_own_files_are_read_in_the_browser(base_url, browser, tmp_path):
    """CSV, JSON, Excel and Word files from the participant's computer land on the shelf, read in the browser
    and kept there; an old .xls is refused with what to do; the model's note has values only when asked."""
    import datetime
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?advanced=1&via=replay&country=Kenya")
    started(page)
    with page.expect_file_chooser() as fc:
        page.click("#shelf .add-own [data-act=pick]")
    fc.value.set_files([str(p) for p in own_fixtures(tmp_path)])
    page.wait_for_function("() => document.querySelectorAll('#shelf .fcard.own').length === 4", timeout=20000)
    assert "old Excel format" in page.inner_text("#log")
    files = {e["name"]: e for e in page.evaluate("OwnFiles.load()")}
    assert [files[n]["key"] for n in ("mine.csv", "mine.json", "mine.xlsx", "mine.docx")] == ["own_1", "own_2", "own_3", "own_4"]
    csv = json.loads(files["mine.csv"]["text"])
    assert csv["fields"] == ["Name", "Count", "Code"] and csv["records"] == [
        {"Name": "Smith; J.", "Count": 12, "Code": "007"}, {"Name": "Łódź", "Count": 3, "Code": None}]
    assert json.loads(files["mine.json"]["text"]) == {"dataset": "own_2", "title": "mine.json",
        "source": "Added by the participant from their own computer; kept in this browser", "count": 2, "records": [{"a": 1, "b": "x"}, {"a": 2, "b": None}]}
    xl = json.loads(files["mine.xlsx"]["text"])
    day = (datetime.date(1899, 12, 30) + datetime.timedelta(days=46000)).isoformat()
    assert xl["records"] == [{"Country": "Kenya", "Date": day, "Votes": 12}, {"Country": "Mali", "Date": None, "Votes": 7.5}], xl["records"]
    assert xl["sheet"] == "Recs" and xl["sheets"]["Notes"] == [{"Note": True}]
    doc = json.loads(files["mine.docx"]["text"])
    assert [(r["style"], r["heading"], r["text"], r["in_table"], r["footnotes"]) for r in doc["records"]] == [
        ("Heading1", True, "I. Introduction", False, []), ("Normal", False, "1. A clean environment matters.", False, [2]),
        ("Normal", False, "Cell text", True, []), ("Normal", False, "2. Second", False, [])]
    assert doc["footnotes"] == [{"id": 2, "text": "See E/C.12/GC/27."}]
    # what the model gets: the fields and types, values only when the box is ticked
    note = page.evaluate("(e) => OwnFiles.describe(e, e.name)", files["mine.csv"])
    assert "WORKSHOP_DATA.own_1" in note and "`Name` (text)" in note and "`Count` (number)" in note and "No values were sent" in note
    assert "Smith" not in note and "Łódź" not in note
    page.check("#shelf .fcard[data-key=own_1] [data-act=samples]")
    page.wait_for_function("async () => (await OwnFiles.load()).find((e) => e.key === 'own_1').samples")
    note = page.evaluate("async () => { const e = (await OwnFiles.load()).find((x) => x.key === 'own_1'); return OwnFiles.describe(e, e.name); }")
    assert "Smith; J." in note and "chose to send" in note
    # the drawer shows what is inside and exactly what would be sent
    page.click("#shelf .fcard[data-key=own_3] [data-act=open]")
    assert "Kenya" in page.inner_text("#drawerBody") and "2 sheets" in page.inner_text("#drawerBody")
    page.click("#drawerClose")
    # kept in this browser: still there after a reload
    page.reload()
    started(page)
    assert page.locator("#shelf .fcard.own").count() == 4
    page.once("dialog", lambda d: d.accept())
    page.click("#shelf .fcard[data-key=own_2] [data-act=remove]")
    page.wait_for_function("() => document.querySelectorAll('#shelf .fcard.own').length === 3")
    assert not errors, errors
    ctx.close()


def test_an_app_on_your_own_file(base_url, browser, fake_api, tmp_path):
    """Dropped into the chat, a file from the computer goes onto the shelf and into the message; the app reads
    all of it; the model got the field names, not the values; What left this laptop says so."""
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?advanced=1&api={api}&planpace=1#s=TEST22")
    started(page)
    path = own_fixtures(tmp_path)[0]
    # a drop from the computer onto the chat column, as the browser delivers it
    page.evaluate("""async ({ name, b64 }) => {
      const bytes = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
      const dt = new DataTransfer();
      dt.items.add(new File([bytes], name, { type: 'text/csv' }));
      document.querySelector('.chat').dispatchEvent(new DragEvent('drop', { dataTransfer: dt, bubbles: true, cancelable: true }));
    }""", {"name": path.name, "b64": __import__("base64").b64encode(path.read_bytes()).decode()})
    page.wait_for_selector("#attach .filechip", timeout=20000)
    assert "mine.csv" in page.inner_text("#attach")
    n = len(calls)
    page.fill("#input", "Build a table of my file")
    page.click("#sendBtn")
    built(page, 1)
    app_frame(page).get_by_text("2 rows, first: Smith; J.").wait_for(timeout=20000)
    sent = calls[n]["messages"][-1]["content"]
    assert "WORKSHOP_DATA.own_1" in sent and "`Name` (text)" in sent and "Smith" not in sent, sent
    look(page, "traceBtn")
    trace = page.inner_text("#drawerBody")
    assert 'Your spreadsheet "mine.csv": its name, its field names and their types, no values' in trace, trace
    assert 'All 2 records of "mine.csv" stay in this browser' in trace
    assert not errors, errors
    ctx.close()


def test_a_screenshot_goes_with_the_message(base_url, browser, fake_api):
    """A picture pasted into the box shows as a chip, goes to the model with the message (scaled, whole), and the
    trace says so; with a model that cannot read pictures (GLM), that one message goes to Claude."""
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    paste = """async () => {
      const c = document.createElement('canvas'); c.width = 2400; c.height = 1200;
      const g = c.getContext('2d'); g.fillStyle = '#9b2335'; g.fillRect(0, 0, 2400, 1200);
      const blob = await new Promise((r) => c.toBlob(r, 'image/png'));
      const dt = new DataTransfer(); dt.items.add(new File([blob], 'shot.png', { type: 'image/png' }));
      document.getElementById('input').dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
    }"""
    page.select_option("#modelSelect", "glm-cn")
    page.evaluate(paste)
    page.wait_for_selector("#attach .filechip.pic")
    assert "Picture 1568×784" in page.inner_text("#attach")          # scaled to 1568 on the long side
    assert "cannot read pictures" in page.inner_text("#log")
    n = len(calls)
    page.fill("#input", "What is wrong here?")
    page.click("#sendBtn")                                               # GLM cannot read it: this message goes to Claude
    page.wait_for_function(f"() => document.querySelectorAll('.msg.user img.pic').length === 1", timeout=20000)
    page.wait_for_function("() => document.getElementById('building').hidden", timeout=30000)
    last = calls[n]["messages"][-1]
    assert calls[n]["model"] == "claude" and page.input_value("#modelSelect") == "glm-cn"   # the menu stays as chosen
    assert last["content"].startswith("What is wrong here?") and last["images"][0]["media_type"] == "image/png"
    assert len(last["images"][0]["data"]) > 100
    look(page, "traceBtn")
    assert "Your picture (1568×784): the whole image, with everything on it" in page.inner_text("#drawerBody")
    assert not errors, errors
    ctx.close()


def test_the_extraction_runs_on_ten_documents(base_url, browser):
    """Recorded: the PDF app, then the same rules on ten General Comments (where they hold, where they break),
    then the panel with the lines that broke them and the Copy for the model button; Fix needs a live model."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")
    started(page)
    send(page, "Paragraphs out of a PDF", "pdf_text", 1)
    send(page, "Run it on ten General Comments", "pdf_ten", 2)
    frame = app_frame(page)
    frame.get_by_role("tab", name=re.compile("03", re.I)).click()
    body = frame.locator("body")
    body.get_by_text("CEDAW/C/GC/35").first.wait_for(timeout=20000)
    text = body.inner_text()
    assert all(s in text for s in ("E/C.12/GC/24", "CRC/C/GC/25", "CAT/C/GC/4")), text[:400]
    assert "hypothesis" in page.locator(".lesson").last.inner_text()       # each answer brings its own lesson
    send(page, "Show what broke the rules", None, 3)
    frame = app_frame(page)
    frame.get_by_role("tab", name=re.compile("03", re.I)).click()
    frame.get_by_role("button", name=re.compile("copy for the model", re.I)).wait_for(timeout=20000)
    assert "CCPR/C/GC/32" in frame.locator("body").inner_text()
    assert not errors, errors
    ctx.close()


def test_a_question_about_the_data_is_answered_by_a_query(base_url, browser, fake_api):
    """Recorded: after the dashboard, a question about the data comes back as a query; the browser runs it on all
    the records and shows the table and the code, and the trace says the numbers stayed here. Live: a query that
    fails says so, with no table."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    pick(page, "Ask your data a question")
    page.click("#sendBtn")
    page.wait_for_selector(".qcard table", timeout=30000)
    card = page.locator(".qcard").last
    assert "Total" in card.inner_text() and "nothing was sent to a model" in card.inner_text()
    assert "WORKSHOP_DATA.uhri" in card.locator("pre").text_content()   # closed until opened
    assert page.locator("#versions [data-v]").count() == 1                     # an answer, not a new version of the app
    look(page, "traceBtn")
    assert "never saw the numbers" in page.inner_text("#drawerBody")
    page.click("#drawerClose")
    page.reload()                                                            # the table is computed again after a reload
    started(page)
    page.wait_for_selector(".qcard table", timeout=30000)
    assert not errors, errors
    ctx.close()

    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    add_file(page, "uhri")
    page.fill("#input", "Count with a query that breaks")
    page.click("#sendBtn")
    page.wait_for_selector(".qcard .qerr", timeout=30000)
    assert "The query failed" in page.inner_text(".qcard")
    ctx.close()


def test_activity_is_recorded_without_content(base_url, browser, fake_api):
    """The page records what was done (a build, its model and seconds, a tool opened) for calibration, and sends it
    when the page is hidden; no message text, no code and no data go with it."""
    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    n = len(EVENTS)
    add_file(page, "uhri")
    page.fill("#input", "Build a counter of my secret words")
    page.click("#sendBtn")
    built(page, 1)
    look(page, "traceBtn")
    page.goto("about:blank")                                            # hidden: the queue goes out with sendBeacon
    page.wait_for_function("() => true")
    import time
    for _ in range(50):
        if len(EVENTS) > n:
            break
        time.sleep(0.1)
    evs = [e for batch in EVENTS[n:] for e in batch["events"]]
    names = [e["t"] for e in evs]
    assert "open" in names and "build" in names and "look" in names, names
    b = next(e for e in evs if e["t"] == "build")
    assert b["kind"] == "app" and b["files"] == 1 and isinstance(b["s"], int)
    assert "secret" not in json.dumps(EVENTS[n:])
    assert EVENTS[n]["seat"] == "TEST22" and re.fullmatch(r"[0-9a-f]{16}", EVENTS[n]["sid"])
    ctx.close()


def test_the_take_home_kit_works_offline(base_url, browser, tmp_path):
    """About → Download the take-home kit: one HTML file with every workshop request ready for any chatbot, the data
    and the participant's apps. Opened from disk, it runs an app of the participant's, an answer pasted from a
    chatbot and a query, with no network; the template on its own says where to get a kit."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    page.click("#takeHomeBtn")
    with page.expect_download(timeout=60000) as dl:
        page.click("#kitBtn")
    kit = tmp_path / dl.value.suggested_filename
    dl.value.save_as(kit)
    assert kit.name == "garage-research-kit-kenya.html"

    p = ctx.new_page()
    net = []
    p.on("request", lambda r: net.append(r.url) if r.url.startswith("http") else None)
    p.goto(kit.as_uri())
    assert p.locator(".req").count() == 8 and "KENYA" in p.inner_text("#kicker").upper()   # the label is in capitals
    first, follow = p.locator(".req textarea").nth(0).input_value(), p.locator(".req textarea").nth(4).input_value()
    assert "Build this app" in first and "WORKSHOP_DATA.uhri" in first and "studio.ask(" not in first and "```edit" not in first
    assert "WORKSHOP_DATA.pdf_ten" in follow and "You are helping a participant" not in follow   # same conversation, new data only
    p.click("[data-app='0']")                                             # the participant's own app, on the kit's data
    p.frame_locator(".stage iframe").locator("body").get_by_text(re.compile("Kenya")).first.wait_for(timeout=20000)
    p.fill("#answer", (SITE / "replay/claude/s7-1-dashboard.md").read_text())
    p.click("#run")
    p.frame_locator(".stage iframe").locator("body").get_by_text(re.compile("2,264")).first.wait_for(timeout=20000)
    assert p.is_enabled("#save")
    p.fill("#answer", (SITE / "replay/claude/s7-1b-ask-data.md").read_text())
    p.click("#run")
    p.wait_for_selector(".qbox table", timeout=20000)
    assert "Total" in p.inner_text(".qbox")
    assert not net, net                                                   # nothing went to the internet
    p.goto((SITE / "kit/kit.html").as_uri())                              # the template, opened by mistake
    assert p.is_visible("#template") and "Download the take-home kit" in p.inner_text("#template")
    ctx.close()


def test_basic_shows_one_path_and_advanced_the_rest(base_url, browser, fake_api):
    """Basic (the default): Session 1 offers the dashboard or the Council votes, Session 2 the PDF, the Verbatim
    finder and the wiki; no own files, no Plan mode switch. Advanced (footer) shows the rest, and is remembered.
    Suggest improvements offers five ways to review an app, each filling the box."""
    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    assert page.locator("#suggest button b").all_inner_texts()[:2] == [DASHBOARD, "How two States vote at the Human Rights Council"]
    assert not page.is_visible("#shelf .add-own") and page.inner_text("#advBtn") == "Advanced: off"
    page.get_by_role("tab", name="Session 2").click()
    assert page.locator("#suggest button b").all_inner_texts()[:3] == ["Paragraphs out of a PDF", "Verbatim finder for General Comments", "A research wiki on neurotechnology and justice"]
    page.click("#advBtn")
    assert page.is_visible("#shelf .add-own") and "Check an AI briefing" not in page.inner_text("#suggest")   # three at a time before an app
    page.reload()
    started(page)
    assert page.inner_text("#advBtn") == "Advanced: on"
    page.click("#advBtn")
    page.get_by_role("tab", name="Session 1").click()
    add_file(page, "uhri")
    page.fill("#input", "Build a counter")
    page.click("#sendBtn")
    built(page, 1)
    page.locator("#suggest button", has_text="Suggest improvements").click()
    page.wait_for_selector(".msg.lenses button")
    assert page.locator(".msg.lenses button").count() == 5
    page.locator(".msg.lenses button", has_text="Pre-mortem").click()
    assert "pre-mortem" in page.input_value("#input").lower()
    ctx.close()


def test_versions_sit_in_one_menu(base_url, browser, fake_api, tmp_path):
    """Hick's law for versions: one button names the app and the version on the stage, arrows step between versions,
    and the menu lists them grouped by app with one line on each."""
    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    add_file(page, "uhri")
    page.fill("#input", "Build a counter")
    page.click("#sendBtn")
    built(page, 1)
    page.fill("#input", "Now say how many in words")
    page.click("#sendBtn")
    built(page, 2)
    assert "v2" in page.inner_text("#versions .vcur") and "of 2" in page.inner_text("#versions .vcur")
    assert page.is_disabled("#versions .vnav[data-dir='1']")
    page.click("#versions .vnav[data-dir='-1']")
    page.wait_for_function("() => document.querySelector('#versions .vcur').textContent.includes('v1')")
    page.click("#versions .vcur")
    assert page.is_visible("#versions .vmenu") and page.locator("#versions .vmenu .vgroup").count() == 1
    assert page.locator("#versions .vmenu [data-v]").count() == 2
    page.screenshot(path=str(tmp_path / "menu.png"))
    page.locator("#versions .vmenu [data-v='2']").click()
    page.wait_for_function("() => document.querySelector('#versions .vcur').textContent.includes('v2')")
    assert not page.is_visible("#versions .vmenu")
    ctx.close()


def test_the_venice_course_has_three_sessions(base_url, browser):
    """?course=venice (the Global Campus): three sessions, one set of data each: the General Comments with the
    Verbatim finder and a quotation checker, the Council votes with the blocs, then the recommendations or one's
    own idea, with one's own files on the shelf without Advanced. ?course=geneva goes back to two sessions."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?course=venice&via=replay&planpace=1&country=Kenya")
    started(page)
    assert page.locator("#sessionSwitch button").count() == 3
    assert page.locator("#suggest button b").all_inner_texts() == ["Verbatim finder for General Comments"]
    page.get_by_role("tab", name="Session 2").click()
    assert page.locator("#suggest button b").all_inner_texts() == ["How two States vote at the Human Rights Council"]
    assert not page.is_visible("#shelf .add-own")
    page.get_by_role("tab", name="Session 3").click()
    assert page.locator("#suggest button b").all_inner_texts() == [DASHBOARD]   # the wiki and "Your own idea" need a live model
    assert page.is_visible("#shelf .add-own")                                    # own files without Advanced
    send(page, DASHBOARD, "uhri", 1)
    assert "Check a quotation" in page.inner_text("#suggest")
    page.goto(base_url + "?course=geneva&via=replay&planpace=1&country=Kenya")
    started(page)
    assert page.locator("#sessionSwitch button").count() == 2
    ctx.close()


def test_venice_shows_only_what_its_sessions_use(base_url, browser, tmp_path):
    """The Venice course without Geneva's leftovers: each session's shelf holds only its own file, the country picker
    shows only where the recommendations are used, two models, no Advanced, no Facilitator's brief, its own
    header line, and a take-home kit with the Venice requests."""
    ctx = browser.new_context(viewport={"width": 1600, "height": 900}, accept_downloads=True)
    page = ctx.new_page()
    page.goto(base_url + "?course=venice&via=replay&planpace=1&country=Kenya&reset=1")
    started(page)
    shelf = lambda: page.eval_on_selector_all("#shelf .fcard[data-key]", "cs => cs.filter(c => c.offsetParent).map(c => c.dataset.key)")
    assert "Venice" in page.inner_text("#event") and "Geneva" not in page.get_attribute("#brand", "title")
    assert sorted(page.eval_on_selector_all("#modelSelect option", "os => os.map(o => o.value)")) == ["claude", "glm-eu"]
    assert not page.is_visible("#advBtn")
    assert shelf() == ["gc"] and not page.is_visible("#countryChip")
    assert "your country is" not in page.inner_text("#log")
    # the General Comments as published in JSON: the first records, laid out as a code editor shows them
    corpus = '[' + ','.join(json.dumps({"id": f"p{i}", "n": i, "text": "A paragraph with \"quotes\".", "year": 2020}) for i in range(30)) + ']'
    page.route("**/generalcomments/corpus.json", lambda r: r.fulfill(status=206, body=corpus[:900], headers={"Content-Range": f"bytes 0-899/{len(corpus)}", "Access-Control-Allow-Origin": "*", "Access-Control-Expose-Headers": "Content-Range"}))
    page.click("#shelf .fcard[data-key=gc] a[data-json]")
    page.wait_for_selector("#drawerBody .json-view .tk-attr")
    assert "The first" in page.inner_text("#drawerBody") and page.locator("#drawerBody .json-view").inner_text().count('"id"') >= 5
    page.click("#drawerClose")
    page.get_by_role("tab", name="Session 2").click()
    assert shelf() == ["hrc", "hrc_all"] and not page.is_visible("#countryChip")
    assert "Hugging Face" in page.inner_text("#shelf .fcard[data-key=hrc_all]")
    page.get_by_role("tab", name="Session 3").click()
    assert shelf() == ["uhri", "pdfs"] and page.is_visible("#countryChip")
    send(page, DASHBOARD, "uhri", 1)
    assert page.get_attribute("#planBrief", "hidden") is not None
    page.click("#lookBtn")
    assert page.is_visible("#traceBtn")
    page.keyboard.press("Escape")
    page.click("#takeHomeBtn")
    with page.expect_download(timeout=60000) as dl:
        page.click("#kitBtn")
    kit = tmp_path / dl.value.suggested_filename
    dl.value.save_as(kit)
    k = ctx.new_page()
    k.goto(kit.as_uri())
    reqs = k.locator(".req").all_inner_texts()
    assert len(reqs) == 8 and any("Who votes with this State" in r for r in reqs) and any("Where every State stands" in r for r in reqs)
    assert not any("PDF" in r for r in reqs)
    data = k.text_content("#datalist")   # in a folded section
    assert "WORKSHOP_DATA.hrc" in data and "wiki" not in data and "pdf_t" not in data
    ctx.close()


def test_the_tour_and_the_country_picker_follow_the_course(base_url, browser):
    """Geneva keeps two sessions in the tour and the country picker in Session 1, without it in Session 2 (Basic);
    Venice's tour says three sessions and skips the country step where the picker is not shown."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?course=geneva&via=replay&planpace=1&country=Kenya&reset=1&advanced=0")
    started(page)
    assert page.is_visible("#countryChip")
    page.get_by_role("tab", name="Session 2").click()
    assert not page.is_visible("#countryChip")
    page.click("#tourBtn")
    page.click(".tour-card [data-t=next]")
    assert page.inner_text(".tour-card h3") == "Two sessions"
    page.click(".tour-card [data-t=next]")
    assert page.inner_text(".tour-card h3") == "Your model"          # the country step is skipped where it is hidden
    page.click(".tour-card [data-t=skip]")
    page.goto(base_url + "?course=venice&via=replay&planpace=1&country=Kenya")
    started(page)
    page.get_by_role("tab", name="Session 1").click()
    page.click("#tourBtn")
    page.click(".tour-card [data-t=next]")
    assert page.inner_text(".tour-card h3") == "Three sessions"
    ctx.close()


def test_start_over_clears_the_work_and_keeps_the_settings(base_url, browser):
    """About → Start over, and ?reset=1: the apps and the conversation in this browser go; the course, the
    settings and the seat stay."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?course=venice&via=replay&planpace=1&country=Kenya")
    started(page)
    page.get_by_role("tab", name="Session 3").click()
    send(page, DASHBOARD, "uhri", 1)
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya&reset=1")
    started(page)
    assert page.locator("#versions [data-v]").count() == 0 and "reset" not in page.url
    assert page.locator("#sessionSwitch button").count() == 3                 # still the Venice course
    send(page, DASHBOARD, "uhri", 1)
    page.click("#takeHomeBtn")
    page.once("dialog", lambda d: d.accept())
    page.click("#startOverBtn")
    page.wait_for_load_state()
    started(page)
    assert page.locator("#versions [data-v]").count() == 0
    ctx.close()


def test_a_button_in_a_form_works_in_the_app(base_url, browser, fake_api):
    """A model often builds a checker as a form. Without allow-forms Chrome never fires its submit event, so the
    button did nothing (11.11.2026). A form that does not stop its own submission reloads the app, as on any page;
    the frame's policy (form-action 'none') keeps a submission from reaching another address."""
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + f"?api={api}&planpace=1&reset=1#s=TEST22")
    started(page)
    page.fill("#input", "Build a checker with a form")
    page.click("#sendBtn")
    built(page, 1)
    app = app_frame(page)
    app.locator("#go").click()
    app.locator("#out", has_text="checked").wait_for(timeout=5000)
    app.locator("#go2").click()   # submits: the app may reload, too fast to read its line, but it stays on the stage
    page.wait_for_timeout(500)
    app.locator("#go").wait_for(timeout=5000)
    ctx.close()


def test_each_session_is_a_conversation_of_its_own(base_url, browser):
    """Switching sessions opens a clean chat and an empty stage; the other session's apps wait there and come
    back with it. Start over clears every session."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?course=venice&via=replay&planpace=1&country=Kenya&reset=1")
    started(page)
    page.get_by_role("tab", name="Session 3").click()
    send(page, DASHBOARD, "uhri", 1)
    page.get_by_role("tab", name="Session 1").click()
    assert page.locator("#versions [data-v]").count() == 0 and page.locator(".msg.assistant").count() == 0
    assert page.is_visible("#shelf") and not page.is_visible("#toolbar")
    assert "A new conversation" in page.locator(".msg.note").last.inner_text()
    page.get_by_role("tab", name="Session 3").click()
    assert page.locator("#versions [data-v]").count() == 1 and page.locator(".msg.assistant").count() >= 1
    app_frame(page).locator("body").get_by_text("Kenya").first.wait_for(timeout=20000)
    page.reload()
    started(page)
    assert page.locator("#versions [data-v]").count() == 1   # still there after a reload
    ctx.close()


def test_venice_session2_adds_the_alignment_map(base_url, browser):
    """Session 2 in recorded mode: the two-State comparison, then "Where every State stands" offered first, built on
    it as a map of every State by its agreement with the two (dots coloured by regional group)."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?course=venice&via=replay&planpace=1&country=Kenya&reset=1")
    started(page)
    page.get_by_role("tab", name="Session 2").click()
    send(page, "How two States vote at the Human Rights Council", "hrc", 1)
    assert page.locator("#suggest button b").all_inner_texts()[:2] == ["Where every State stands", "Who votes with this State"]
    send(page, "Where every State stands", None, 2)
    app = app_frame(page)
    app.get_by_role("tab", name=re.compile("map", re.I)).click()
    app.locator("svg circle").nth(40).wait_for(state="attached", timeout=10000)
    assert "African States" in app.locator("body").inner_text() and "adopted without a vote" in app.locator("body").inner_text()
    assert not errors, errors
    ctx.close()
