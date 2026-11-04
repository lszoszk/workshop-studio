"""End-to-end test of the studio in recorded mode (no model, no server, no cost).

    python3 -m pytest tests/e2e -q

Serves site/ on a free port, drives headless Chrome through a participant's path:
build the first request from its card (in plan mode: the recorded planning session, its
questions, the plan on the stage, Build), Layers, Run x3, Trace, saving the app and opening
it offline from disk, a reload; then Session 8 with the model link cut; then what a
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
PLAN_V2 = ("Here is the revised plan.\n\n```markdown\n## Context\nThe same dashboard, revised.\n\n"
           "## The app, screen by screen\n1. A line chart of the records per year.\n2. The table of records.\n```")


FEEDBACK = []   # what the fake server received from the Feedback form


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
            elif req["purpose"] == "build" and "Reply with the whole revised plan" in last:
                events.append({"reasoning": "They want a line per year; add it to the screens."})
                events.append({"delta": PLAN_V2})
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
    page.wait_for_function(f"() => document.querySelectorAll('#versions button').length === {n} && document.getElementById('building').hidden", timeout=90000)


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
    planning = page.is_visible("#planModeBtn") and page.get_attribute("#planModeBtn", "aria-pressed") == "true"
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
    assert page.is_visible("#planModeBtn") and page.get_attribute("#planModeBtn", "aria-pressed") == "true"
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

    # Layers: an overlay marks what the model wrote and what the code computed, the legend shows;
    # the country and the record count come from the data, the tab names from the model's code
    look(page, "layersBtn")
    page.wait_for_timeout(800)
    assert page.is_visible("#legend")
    marks = lambda cls: [t for t in frame.locator(f"#studio-layers .{cls}").evaluate_all("(b) => b.map((d) => d.dataset.t || '')") if t]
    computed, written = marks("script"), marks("model")
    assert "Kenya" in computed and any("2,264" in t for t in computed), computed[:20]
    assert any(re.search(r"overview", t, re.I) for t in written), written[:20]
    assert not any("Kenya" in t or "2,264" in t for t in written), written[:20]
    look(page, "layersBtn")
    assert frame.locator("#studio-layers").count() == 0

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
    page.wait_for_function("() => document.querySelectorAll('#versions button').length === 1")
    if (SITE / "replay/claude/s7-1-dashboard.thought.md").exists():   # builds made in Claude Code have no recorded thinking
        assert page.locator(".thought summary").first.inner_text().startswith("Thought")
    assert page.locator(".lesson").count() == 1
    assert page.inner_text("#traceCount") == "1"

    assert not errors, errors
    ctx.close()


def test_session8_model_link_off_blocks_inapp_ai(base_url, browser):
    """Session 8 adds the model link; with it cut, studio.ask fails inside the recorded
    'A model inside the tool' app while the rest keeps working, and nothing can be built."""
    if not (SITE / "replay/mistral/s8-2-ai-inside.md").exists():
        pytest.skip("no recording for s8-2-ai-inside yet (run tools/bakeoff.py and copy to site/replay)")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
    assert page.locator("#suggest button", has_text="A model inside the tool").count() == 0   # a Session 8 step
    page.get_by_role("tab", name="Session 8").click()
    send(page, "A model inside the tool", None, 2)   # the country file is already in the chat
    look(page, "linkBtn")
    assert page.is_visible("#offlineBanner") and page.is_visible("#linkOffPill")
    frame = app_frame(page)
    frame.get_by_role("button", name=re.compile("suggest", re.I)).first.click()
    page.wait_for_timeout(2500)
    assert re.search(r"cut the link|model", frame.locator("body").inner_text(), re.I)
    assert page.inner_text("#traceCount") == "2"  # the two builds; the AI call never left
    # a build with the link cut is refused, and the request is not lost
    page.fill("#input", "Make the chart blue.")
    page.click("#sendBtn")
    assert "link is cut" in page.locator(".msg.note").last.inner_text()
    assert page.input_value("#input") == "Make the chart blue."
    ctx.close()


def test_what_is_shown_grows_with_progress(base_url, browser):
    """Hick's law: one card and no tools before the first app; tools after it."""
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    page = ctx.new_page()
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
    started(page)
    assert not page.is_visible("#toolbar")
    assert page.is_visible("#composer") and page.locator("#shelf .fcard").count() == len(json.loads((SITE / "config.json").read_text())["files"])
    assert page.locator("#suggest button").count() <= 3
    send(page, DASHBOARD, "uhri", 1)
    assert page.is_visible("#toolbar") and not page.is_visible("#shelf")
    assert page.locator("#suggest button").count() <= 3
    page.click("#lookBtn")
    assert page.is_visible("#layersBtn") and page.is_visible("#run3Btn") and page.is_visible("#traceBtn")
    assert not page.is_visible("#ask3Btn") and not page.is_visible("#linkBtn")   # Session 8 tools
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


def test_extraction_from_raw_pdf_text(base_url, browser):
    """The recorded 'Paragraphs out of a PDF' app runs on the raw page text and checks itself
    against the reference shipped with it."""
    if not (SITE / "replay/claude/s7-4-extract.md").exists():
        pytest.skip("no recording for s7-4-extract yet")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")   # the extraction is in Session 8
    started(page)
    send(page, "Paragraphs out of a PDF", "pdf_text", 1)
    body = app_frame(page).locator("body")
    body.get_by_text("E/C.12/GC/27").first.wait_for(timeout=20000)
    text = body.inner_text()
    assert re.search(r"90\s*(/|of)\s*90", text, re.I), text[:400]
    assert page.locator(".lesson").inner_text().count("four ways") == 1
    assert not errors, errors
    ctx.close()


def test_live_country_switch_and_asking_directly(base_url, browser, fake_api):
    api, calls = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
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
    assert len(calls) == n and page.locator("#versions button").count() == 1

    # a chatbot: small talk gets an answer in words, and no new version
    page.fill("#input", "How are you?")
    page.keyboard.press("Enter")
    page.wait_for_function("() => [...document.querySelectorAll('.msg.assistant .answer-md')].some((e) => e.textContent.includes('well, thank you'))", timeout=15000)
    assert page.locator("#versions button").count() == 1
    assert "(Attached:" in calls[-1]["messages"][0]["content"]   # the file named earlier is still in the conversation

    # Session 8: asking the model directly, a number, then a paragraph that does not exist
    page.get_by_role("tab", name="Session 8").click()
    look(page, "ask3Btn")
    page.wait_for_function("() => document.getElementById('truth').textContent.includes('records in total')")
    page.get_by_role("tab", name="A quotation").click()
    page.wait_for_function("() => document.getElementById('askNote').textContent.includes('no paragraph 97')", timeout=15000)
    assert "There is no paragraph 97: E/C.12/GC/27 has 90 numbered paragraphs" in page.inner_text("#truth")
    assert sum(1 for c in calls if c["purpose"] == "question" and "paragraph 97" in c["messages"][-1]["content"]) == 3
    assert page.inner_text("#traceCount") == "8"   # one build, one chat, three counts, three quotations
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
    assert page.inner_text("#traceCount") == "9"
    assert not errors, errors
    ctx.close()


def test_session8_offers_its_apps_first(base_url, browser):
    """Session 8 starts with the PDF extraction, the Verbatim finder and the research wiki; the
    briefing check is an extra that appears once they are built (Hick's law: the plan's apps first)."""
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")
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
    # the PDF opens in the browser
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
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")
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


def test_the_extraction_grows_to_a_second_document(base_url, browser):
    """Session 8: the extraction app, then "Add a second document" with CCPR GC 32 dragged in (the app
    gets both files, though its code never names the second), then the model step, which in recorded
    mode cannot call a model and says so."""
    if not (SITE / "replay/claude/s7-6-model-on-flagged-pages.md").exists():
        pytest.skip("no recording for the extraction's next steps")
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + "?via=replay&planpace=1&stage=s8&country=Kenya")
    started(page)
    send(page, "Paragraphs out of a PDF", "pdf_text", 1)
    pick(page, "Add a second document")
    assert "CCPR General comment No. 32" in page.inner_text("#needs")
    add_file(page, "pdf_text_2")
    page.click("#sendBtn")
    built(page, 2)
    body = app_frame(page).locator("body")
    body.get_by_text("CCPR/C/GC/32").first.wait_for(timeout=20000)
    assert re.search(r"17\s*of\s*18", body.inner_text()), body.inner_text()[:600]     # GC 32: pages flagged
    send(page, "A model for the pages that fail", None, 3)
    app_frame(page).get_by_text("CCPR/C/GC/32").first.click()
    app_frame(page).get_by_role("tab", name=re.compile("flagged", re.I)).click()   # the step sits with the flagged pages
    assert re.search(r"\d+ pages? will leave the browser", app_frame(page).locator("body").inner_text(), re.I)
    assert not errors, errors
    ctx.close()


def test_the_wall_shows_what_participants_sent(base_url, browser, fake_api):
    """Send to wall puts an app on the facilitator's wall with the country and files it ran on; the wall
    draws each as a live thumbnail, and a click opens it full screen on the same data."""
    api, _ = fake_api
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base_url + f"?api={api}&planpace=1#s=TEST22")
    started(page)
    send(page, DASHBOARD, "uhri", 1)
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
    page.goto(base_url + "?via=replay&planpace=6&country=Kenya")
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
    page.goto(base_url + "?via=replay&planpace=1&country=Kenya")
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
    assert page.locator("#versions button").count() == 0 and page.is_visible("#planView")
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
    assert "changed live by Mistral Large 3" in page.text_content("#planKicker")
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
    assert page.locator("#versions button").count() == 1
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
    app_frame(page).get_by_text(re.compile(r"pages? flagged", re.I)).first.wait_for(timeout=20000)
    work = page.evaluate("JSON.parse(localStorage.getItem('ws:work:guest'))")
    assert work["versions"][0]["sent"].startswith("Build this app.") and "```html" in work["versions"][0]["reply"]
    page.goto(base_url + "?via=replay&country=Kenya&from=nobody%2Fnothing")
    started(page)
    assert "could not be loaded" in page.inner_text("#log")
    ctx.close()
