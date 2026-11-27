#!/usr/bin/env python3
"""Everything about one workshop day in one folder, for the closing film's numbers and for debugging the studio later.

    python3 tools/day_bundle.py --day 2026-12-04 --course geneva

Writes tools/out/days/<day>-<course>/ (tools/out is git-ignored):
  events.jsonl      the activity events of the day (GET /studio-api/admin/events), the course's visits
  wall.json         the wall's apps of the course made that day (GET /studio-api/gallery?course=)
  admin.json        seats, wall, feedback (with its texts), mode, balance (GET /studio-api/admin?format=json)
  usage.csv         the server's per-request usage table for the day (sqlite, read inside the docker container)
  server-log.jsonl  the server's own JSON log lines of the day (docker logs; no message text, no IP addresses)
  report.txt        tools/events_report.py on events.jsonl, then a summary of usage, log, wall and feedback
  stats.json        the numbers for the closing film (null where unknown)

Read-only. The admin key comes from STUDIO_ADMIN_KEY, or else from the VM's server/.env over ssh; it is never
printed or written. Seat codes are replaced by S01, S02, … (by each seat's first event) in every file; the mapping is
never written. A step that fails (ssh refused, endpoint missing) is a warning, and the bundle is written with the rest.

Which events belong to the course: only `progress` and `progress_skip` events carry a course. A seat is a course seat
if one of its events says the course, or it sent a wall app of the course that day (the admin wall holds the seat);
a visit (sid) is a course visit if one of its events says the course or its seat is a course seat. Visits that say
another course are dropped; visits with no evidence either way are kept in events.jsonl (counted in report.txt) but
left out of the numbers. If nothing at all says the course (Venice has no progress events, and its wall may carry no
course), everything of the day is kept and counted, and report.txt says so.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
HOST = "amuvmuser@150.254.115.204"
BASE = "https://150.254.115.204/studio-api"
SSH = ["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes", HOST]
SEAT = re.compile(r"[A-Z0-9]{6}")
WARNINGS: list[str] = []


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print("WARNING:", msg, file=sys.stderr)


def ssh(cmd: str, timeout: int = 120) -> str | None:
    try:
        r = subprocess.run(SSH + [cmd], capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError) as e:
        warn(f"ssh failed ({type(e).__name__})")
        return None
    if r.returncode:
        warn(f"ssh command failed (exit {r.returncode}): {r.stderr.strip().splitlines()[-1][:120] if r.stderr.strip() else ''}")
        return None
    return r.stdout


def admin_key() -> str | None:
    key = os.environ.get("STUDIO_ADMIN_KEY", "").strip()
    if key:
        return key
    out = ssh("grep '^STUDIO_ADMIN_KEY=' /home/amuvmuser/workshop-studio/server/.env | cut -d= -f2-")
    return out.strip().strip("\"'") if out and out.strip() else None


def get(client: httpx.Client, path: str, **params) -> str | None:
    """The text of a GET, or None with a warning that names the path and the status, never the URL (it holds the key)."""
    try:
        r = client.get(BASE + path, params=params)
    except httpx.HTTPError as e:
        warn(f"GET {path}: {type(e).__name__}")
        return None
    if r.status_code != 200:
        warn(f"GET {path}: HTTP {r.status_code}")
        return None
    return r.text


def get_json(client, path, **params):
    text = get(client, path, **params)
    try:
        return json.loads(text) if text is not None else None
    except ValueError:
        warn(f"GET {path}: not JSON")
        return None


def jsonl(text: str | None) -> list[dict]:
    out = []
    for line in (text or "").splitlines():
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if isinstance(o, dict):
            out.append(o)
    return out


def usage_rows(day: str) -> list[dict] | None:
    """The usage table of the day, read through the running container (its sqlite file is the only copy)."""
    code = ("import sqlite3,json;c=sqlite3.connect(\"file:/state/studio.sqlite3?mode=ro\",uri=True);c.row_factory=sqlite3.Row;"
            f"print(json.dumps([dict(r) for r in c.execute(\"SELECT * FROM usage WHERE day=? ORDER BY id\",(\"{day}\",))]))")
    out = ssh(f"docker exec studio-api python -c '{code}'")
    try:
        return json.loads(out) if out else None
    except ValueError:
        warn("usage table: unreadable answer")
        return None


def server_log(day: str) -> list[dict] | None:
    nxt = (dt.date.fromisoformat(day) + dt.timedelta(days=1)).isoformat()
    out = ssh(f"docker logs studio-api --since {day}T00:00:00 --until {nxt}T00:00:00 2>&1", timeout=180)
    if out is None:
        return None
    return [o for o in (_obj(l) for l in out.splitlines()) if o is not None]


def _obj(line: str):
    line = line.strip()
    if not line.startswith("{"):
        return None   # uvicorn's own lines
    try:
        o = json.loads(line)
    except ValueError:
        return None
    return o if isinstance(o, dict) and "event" in o else None


def med(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(statistics.median(xs), 2) if xs else None


def seat_order(events, usage, log_lines, admin) -> dict[str, str]:
    """S01, S02, … by each seat's first event; seats seen only elsewhere follow, in the order they are met."""
    seen: dict[str, None] = {}

    def see(code):
        if isinstance(code, str) and SEAT.fullmatch(code.upper()):
            seen.setdefault(code.upper())
    for e in sorted(events, key=lambda e: e.get("at") or ""):
        see(e.get("seat"))
    for u in usage:
        see(u.get("seat"))
    for l in log_lines:
        see(l.get("seat"))
    if admin:
        for g in admin.get("gallery", []):
            see(g.get("seat"))
        for f in admin.get("feedback", []):
            see(f.get("seat"))
        for s in sorted(admin.get("seats", []), key=lambda s: s.get("code") or ""):
            see(s.get("code"))
    return {c: f"S{i:02d}" for i, c in enumerate(seen, 1)}


def pseudonymiser(mapping: dict[str, str]):
    if not mapping:
        return lambda s: s
    rx = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(map(re.escape, mapping)) + r")(?![A-Za-z0-9])", re.I)
    return lambda s: rx.sub(lambda m: mapping[m.group(1).upper()], s)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def lines_of(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Save a workshop day's logs and stats in one folder.")
    ap.add_argument("--day", required=True, help="YYYY-MM-DD")
    ap.add_argument("--course", required=True, help="the course id on the wall and in events: geneva, venice, …")
    a = ap.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", a.day) or not re.fullmatch(r"[a-z0-9-]{1,20}", a.course):
        sys.exit("--day must be YYYY-MM-DD and --course a short lower-case id")
    day, course = a.day, a.course
    out = ROOT / "tools" / "out" / "days" / f"{day}-{course}"
    out.mkdir(parents=True, exist_ok=True)
    labels = {k: m.get("label", k) for k, m in json.loads((ROOT / "site" / "config.json").read_text(encoding="utf-8"))["models"].items()}

    key = admin_key()
    if not key:
        warn("no admin key: events, admin state are skipped")
    # verify=False for this one host only: the studio server's certificate is a Let's Encrypt IP certificate that
    # Python's TLS store may reject (as in tools/teaser/make_teaser.py). Every request here is a read-only GET.
    with httpx.Client(timeout=60, verify=False) as client:
        events = jsonl(get(client, "/admin/events", key=key, day=day)) if key else []
        admin = get_json(client, "/admin", key=key, format="json") if key else None
        wall_all = get_json(client, "/gallery", course=course) or []
        wall_any = None   # fetched only when the course's wall is empty
        if not wall_all:
            wall_any = get_json(client, "/gallery") or []
    usage = usage_rows(day) or []
    log_lines = server_log(day) or []

    # ── the wall of the day ──
    on_day = lambda items: [i for i in items if str(i.get("created") or "").startswith(day)]   # noqa: E731
    wall, notes = on_day(wall_all), []
    if not wall and wall_any:
        wall = [i for i in on_day(wall_any) if i.get("course") in (None, course)]
        if wall:
            notes.append(f"No wall item of the day carries course '{course}': kept the {len(wall)} items of the day with no course field.")

    # ── which seats and visits are the course's ──
    ev_by_sid = defaultdict(list)
    for e in events:
        ev_by_sid[e.get("sid")].append(e)
    course_seats = {e["seat"] for e in events if e.get("course") == course and e.get("seat")}
    if admin:
        course_seats |= {g["seat"] for g in admin.get("gallery", []) if g.get("course") == course and str(g.get("created", "")).startswith(day) and g.get("seat")}
    says = {sid: {e["course"] for e in es if e.get("course")} for sid, es in ev_by_sid.items()}
    seat_of = {sid: next((e["seat"] for e in es if e.get("seat")), None) for sid, es in ev_by_sid.items()}
    course_sids = {sid for sid, c in says.items() if course in c} | {sid for sid, s in seat_of.items() if s in course_seats}
    other_sids = {sid for sid, c in says.items() if c and course not in c and sid not in course_sids}
    fallback = not course_sids and not course_seats
    if fallback:
        notes.append(f"Nothing in the day's events or wall says which visits belong to '{course}': all events and all usage of the day are kept and counted.")
        keep_sids = set(ev_by_sid)
        course_seats = {s for s in seat_of.values() if s} | {u["seat"] for u in usage}
        course_sids = set(ev_by_sid)
    else:
        keep_sids = set(ev_by_sid) - other_sids
        unknown = len(keep_sids - course_sids)
        notes.append(f"Visits of the course: {len(course_sids)}; visits of another course left out: {len(other_sids)}; "
                     f"visits with no course evidence kept in events.jsonl but not counted: {unknown}.")
    kept = [e for e in events if e.get("sid") in keep_sids]
    cev = [e for e in events if e.get("sid") in course_sids]
    cusage = [u for u in usage if u["seat"] in course_seats]

    # ── pseudonyms, then the files ──
    pseudo = pseudonymiser(seat_order(kept, usage, log_lines, admin))
    write(out / "events.jsonl", "".join(pseudo(json.dumps(e, ensure_ascii=False)) + "\n" for e in kept))
    write(out / "wall.json", pseudo(json.dumps(wall, ensure_ascii=False, indent=1)))
    if admin:
        admin = {k: v for k, v in admin.items() if k != "keys"}   # the last four characters of the API keys: not needed
        write(out / "admin.json", pseudo(json.dumps(admin, ensure_ascii=False, indent=1)))
    buf = io.StringIO()
    cols = ["id", "ts", "day", "seat", "model", "host", "purpose", "prompt_tokens", "completion_tokens", "cost", "estimated", "latency_ms", "status", "error"]
    w = csv.DictWriter(buf, cols, lineterminator="\n")
    w.writeheader()
    w.writerows({c: u.get(c) for c in cols} for u in usage)   # the whole day; the summary and the numbers use the course's seats
    write(out / "usage.csv", pseudo(buf.getvalue()))
    write(out / "server-log.jsonl", "".join(pseudo(json.dumps(l, ensure_ascii=False)) + "\n" for l in log_lines))

    # ── the numbers for the film ──
    builds = [e for e in cev if e["t"] == "build" and e.get("kind") == "app"]
    per_seat = Counter(e.get("seat") or e.get("sid") for e in builds)
    first_pick, first_ok = {}, {}
    for sid in course_sids:
        es = sorted(ev_by_sid[sid], key=lambda e: e.get("ms") or 0)
        pick = next((e for e in es if e["t"] == "pick" and isinstance(e.get("ms"), (int, float))), None)
        if not pick:
            continue
        for i, e in enumerate(es):
            if e["t"] == "build" and e.get("kind") == "app" and isinstance(e.get("ms"), (int, float)) and e["ms"] >= pick["ms"]:
                nxt = next((x["ms"] for x in es[i + 1:] if x["t"] == "build" and isinstance(x.get("ms"), (int, float))), float("inf"))
                broke = any(x["t"] == "app_error" and x.get("first") and e["ms"] <= (x.get("ms") or 0) < nxt for x in es)
                if not broke:
                    first_ok[sid] = (e["ms"] - pick["ms"]) / 60000
                    break
    by_model = {}
    for m in sorted({e.get("model") for e in builds if e.get("model")} | {i.get("model") for i in wall if i.get("model")}):
        mine = [e for e in builds if e.get("model") == m]
        new = [e for e in mine if not e.get("rec") and e.get("parent") is None and not e.get("edit") and not e.get("auto")]
        by_model[m] = {"label": labels.get(m, m), "wall": sum(1 for i in wall if i.get("model") == m), "builds": len(mine),
                       "median_s": med(e.get("s") for e in mine if not e.get("rec")),   # every live app answer, edits included
                       "new": len(new), "median_new_s": med(e.get("s") for e in new)}   # a new tool from a prompt (no parent version)
    stats = {"day": day, "course": course, "tools": len(wall), "named": sum(1 for i in wall if i.get("name")), "people": None,
             "requests": sum(1 for u in cusage if u.get("status") == "ok"), "apps_built": len(builds),
             "plans_changed": sum(1 for e in cev if e["t"] == "plan_build" and e.get("changed")) + sum(1 for e in cev if e["t"] == "plan_revise"),
             "versions_per_tool_median": med(per_seat.values()), "first_app_min_median": med(first_ok.values()),
             "app_errors": sum(1 for e in cev if e["t"] == "app_error"), "repairs": sum(1 for e in cev if e["t"] == "repair"),
             "cost_usd": round(sum(u.get("cost") or 0 for u in cusage), 4), "by_model": by_model}
    write(out / "stats.json", json.dumps(stats, ensure_ascii=False, indent=2) + "\n")

    # ── the report ──
    rep = subprocess.run([sys.executable, str(ROOT / "tools" / "events_report.py"), str(out / "events.jsonl")], capture_output=True, text=True)
    parts = [f"Day bundle: {day}, course {course}", *notes, *(f"Warning: {m}" for m in WARNINGS), "",
             "── events_report.py ──", rep.stdout if rep.returncode == 0 else f"(events_report failed: {rep.stderr.strip()[-200:]})", "── usage ──",
             f"{len(cusage)} requests of the course's seats ({len(usage)} on the day in all); cost ${sum(u.get('cost') or 0 for u in cusage):.4f}"]
    for name, rows in (("by model", Counter(u.get("model") for u in cusage)), ("by purpose", Counter(u.get("purpose") for u in cusage)),
                       ("by status", Counter(u.get("status") for u in cusage))):
        parts.append(f"  {name}: {dict(rows.most_common())}")
    refused = Counter((u.get("status"), u.get("error")) for u in cusage if u.get("status") != "ok")
    parts.append(f"  not answered, by status and error code: {dict(refused.most_common())}")
    parts += ["", "── server log ──", f"{len(log_lines)} lines; by event: {dict(Counter(l['event'] for l in log_lines).most_common())}"]
    chat = Counter((l.get("status"), l.get("error")) for l in log_lines if l["event"] == "chat")
    parts.append(f"  chat by status and error: {dict(chat.most_common())}")
    parts += ["", "── wall ──", f"{len(wall)} apps, {stats['named']} with a name; by model: {dict(Counter(i.get('model') for i in wall).most_common())}"]
    fb = [f for f in (admin or {}).get("feedback", []) if str(f.get("created", "")).startswith(day)]
    parts += ["", "── feedback ──", f"{len(fb)} on the day ({len((admin or {}).get('feedback', []))} in the admin list; texts are in admin.json)"]
    write(out / "report.txt", pseudo("\n".join(parts)) + "\n")

    print(f"\nWritten to {out}")
    for p in sorted(out.iterdir()):
        print(f"  {p.name:18} {lines_of(p):6} lines")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s), see above and report.txt")


if __name__ == "__main__":
    main()
