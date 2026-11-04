"""Seats, budgets and usage for Workshop Studio (sqlite, one file in the state directory).

A seat is a 6-character code printed as a QR code on a participant's badge (tools/make_seats.py writes
tools/out/seats.csv: code,country,label,budget). It carries a country (a name from site/data/index.json,
e.g. Kenya: the data the studio opens with), a label (who holds it: shown on the admin page only, never
logged, never in a public endpoint, never sent to Cloudflare), a budget in USD (default 8) and a disabled flag.
The usage table holds one row per model call: seat, model, host, tokens, cost, latency, status.
It never holds message content and never an IP address.

Rate limiting is per seat (20 requests / 5 minutes by default), never per IP: the whole room sits
behind one NAT address. It lives in memory, which is fine for one uvicorn worker.

CLI (from the repo root as `python3 -m server.seats …`; in the container `docker exec studio-api python seats.py …`):
    python3 -m server.seats import tools/out/seats.csv   # code,country,label,budget; re-import updates
                                                         # country/label/budget and keeps spending
    python3 -m server.seats create 5 --country Kenya     # spare seats, prints the codes
    python3 -m server.seats list
    python3 -m server.seats export-kv tools/out/seats.csv > seats-kv.json
                                                         # Worker KV (wrangler kv bulk put); no labels,
                                                         # no spending, so a re-seed keeps the Worker's spending
"""
import collections
import csv
import datetime as dt
import json
import os
import secrets
import sqlite3
import sys
import threading
import time
from pathlib import Path

ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"   # no 0/O, 1/I/L: codes are typed off badges too
CODE_LEN = 6

SCHEMA = """
CREATE TABLE IF NOT EXISTS seats (
  code TEXT PRIMARY KEY, country TEXT NOT NULL DEFAULT '', label TEXT NOT NULL DEFAULT '', budget REAL NOT NULL,
  spent REAL NOT NULL DEFAULT 0, disabled INTEGER NOT NULL DEFAULT 0,
  requests INTEGER NOT NULL DEFAULT 0, errors INTEGER NOT NULL DEFAULT 0,
  last_request TEXT, last_error TEXT);
CREATE TABLE IF NOT EXISTS usage (
  id INTEGER PRIMARY KEY, ts TEXT NOT NULL, day TEXT NOT NULL, seat TEXT NOT NULL,
  model TEXT, host TEXT, purpose TEXT, prompt_tokens INTEGER, completion_tokens INTEGER,
  cost REAL NOT NULL DEFAULT 0, estimated INTEGER NOT NULL DEFAULT 0,
  latency_ms INTEGER, status TEXT, error TEXT);
CREATE INDEX IF NOT EXISTS usage_day ON usage(day);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
"""


def new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))


def normalise(code: str) -> str:
    return "".join(str(code or "").split()).upper()


def read_csv(path: Path) -> list[dict]:
    """tools/out/seats.csv (code,country,label,budget); label and budget may be missing or empty."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row.get("code") or "").strip():
                b = (row.get("budget") or "").strip()
                rows.append({"code": normalise(row["code"]), "country": (row.get("country") or "").strip(),
                             "label": (row.get("label") or "").strip(), "budget": float(b) if b else None})
    return rows


def kv_entries(seats: list[dict], default_budget: float) -> list[dict]:
    """wrangler kv bulk put format. Spending lives under spent:<CODE> in the Worker, so this never resets it."""
    return [{"key": f"seat:{s['code']}", "value": json.dumps(
        {"country": s["country"], "budget": default_budget if s.get("budget") is None else s["budget"],
         "disabled": bool(s.get("disabled"))})} for s in seats]


class Seats:
    def __init__(self, path: Path, default_budget: float = 8.0, daily_budget: float = 200.0,
                 rate_limit: int = 60, rate_window: int = 300):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.default_budget = default_budget
        self.daily_budget = daily_budget
        self.rate_limit, self.rate_window = rate_limit, rate_window
        self.lock = threading.Lock()
        self.db = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        if "label" not in {r["name"] for r in self.db.execute("PRAGMA table_info(seats)")}:   # databases from before labels
            self.db.execute("ALTER TABLE seats ADD COLUMN label TEXT NOT NULL DEFAULT ''")
        self.hits: dict[str, collections.deque] = collections.defaultdict(collections.deque)

    # ── seats ──
    def get(self, code: str) -> dict | None:
        r = self.db.execute("SELECT * FROM seats WHERE code=?", (normalise(code),)).fetchone()
        return dict(r) if r else None

    def all(self) -> list[dict]:
        return [dict(r) for r in self.db.execute("SELECT * FROM seats ORDER BY code")]

    def add(self, code: str, country: str = "", budget: float | None = None, keep_existing: bool = False,
            label: str = "") -> str:
        """Insert or update a seat; spending is never touched. keep_existing=True leaves a known seat
        (and its top-ups) alone: that is the start-up import, so a restart cannot undo a top-up."""
        code = normalise(code)
        if len(code) != CODE_LEN or any(c not in ALPHABET for c in code):
            raise ValueError(f"seat code must be {CODE_LEN} characters from {ALPHABET}: {code!r}")
        on_conflict = ("DO NOTHING" if keep_existing else
                       "DO UPDATE SET country=excluded.country, label=excluded.label, budget=excluded.budget")
        with self.lock:
            self.db.execute(f"INSERT INTO seats(code, country, label, budget) VALUES(?,?,?,?) ON CONFLICT(code) {on_conflict}",
                            (code, country.strip(), label.strip(), self.default_budget if budget is None else float(budget)))
        return code

    def create(self, n: int, country: str = "") -> list[str]:
        made = []
        while len(made) < n:
            c = new_code()
            if not self.get(c):
                made.append(self.add(c, country))
        return made

    def import_csv(self, path: Path, keep_existing: bool = False) -> int:
        rows = read_csv(path)
        for r in rows:
            self.add(r["code"], r["country"], r["budget"], keep_existing, r["label"])
        return len(rows)

    def set_disabled(self, code: str, disabled: bool) -> bool:
        with self.lock:
            return self.db.execute("UPDATE seats SET disabled=? WHERE code=?",
                                   (int(disabled), normalise(code))).rowcount == 1

    def set_budget(self, code: str, budget: float) -> bool:
        with self.lock:
            return self.db.execute("UPDATE seats SET budget=? WHERE code=?",
                                   (float(budget), normalise(code))).rowcount == 1

    # ── settings (kill switch, default model) ──
    def setting(self, key: str, default: str | None = None) -> str | None:
        r = self.db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return r["value"] if r else default

    def set_setting(self, key: str, value: str) -> None:
        with self.lock:
            self.db.execute("INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                            (key, value))

    # ── limits ──
    def spent_today(self) -> float:
        r = self.db.execute("SELECT COALESCE(SUM(cost),0) s FROM usage WHERE day=?", (dt.date.today().isoformat(),))
        return float(r.fetchone()["s"])

    def spent_on(self, model: str, host: str) -> float:
        """All that one route has cost, every day: the Anthropic cap is a total, not a daily limit."""
        r = self.db.execute("SELECT COALESCE(SUM(cost),0) s FROM usage WHERE model=? AND host=?", (model, host))
        return float(r.fetchone()["s"])

    def hit(self, code: str, now: float | None = None) -> int:
        """Count a request against the seat's window. Returns 0 if allowed, else seconds to wait."""
        now = time.monotonic() if now is None else now
        with self.lock:
            h = self.hits[normalise(code)]
            while h and now - h[0] >= self.rate_window:
                h.popleft()
            if len(h) >= self.rate_limit:
                return max(1, int(self.rate_window - (now - h[0])) + 1)
            h.append(now)
            return 0

    def active_count(self, minutes: int = 10) -> int:
        since = (dt.datetime.now() - dt.timedelta(minutes=minutes)).isoformat(timespec="seconds")
        r = self.db.execute("SELECT COUNT(*) n FROM seats WHERE last_request >= ?", (since,))
        return int(r.fetchone()["n"])

    # ── accounting ──
    def record(self, seat: str, *, model: str, host: str, purpose: str, prompt_tokens: int = 0,
               completion_tokens: int = 0, cost: float = 0.0, estimated: bool = False,
               latency_ms: int = 0, status: str = "ok", error: str | None = None) -> None:
        now = dt.datetime.now()
        seat = normalise(seat)
        with self.lock:
            self.db.execute(
                "INSERT INTO usage(ts, day, seat, model, host, purpose, prompt_tokens, completion_tokens, cost,"
                " estimated, latency_ms, status, error) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (now.isoformat(timespec="seconds"), now.date().isoformat(), seat, model, host, purpose,
                 prompt_tokens, completion_tokens, cost, int(estimated), latency_ms, status, error))
            self.db.execute(
                "UPDATE seats SET spent=spent+?, requests=requests+1, errors=errors+?, last_request=?,"
                " last_error=COALESCE(?, last_error) WHERE code=?",
                (cost, int(status != "ok"), now.isoformat(timespec="seconds"), error, seat))


def _cli(argv: list[str]) -> None:
    budget = float(os.environ.get("STUDIO_SEAT_BUDGET", "8"))
    cmd = argv[0] if argv else "list"
    if cmd == "export-kv" and len(argv) > 1:          # straight from the CSV: no database needed
        print(json.dumps(kv_entries(read_csv(Path(argv[1])), budget), indent=1))
        return
    state = Path(os.environ.get("STUDIO_STATE_DIR", Path(__file__).resolve().parent / "state"))
    s = Seats(state / "studio.sqlite3", default_budget=budget)
    if cmd == "create":
        country = argv[argv.index("--country") + 1] if "--country" in argv else ""
        print("\n".join(s.create(int(argv[1]), country)))
    elif cmd == "import":
        print(f"{s.import_csv(Path(argv[1]))} seats imported into {s.path}")
    elif cmd == "list":
        for r in s.all():
            print(f"{r['code']}  {r['country'] or '---':12}  {r['label'][:24]:24}  ${r['spent']:.2f} / ${r['budget']:.2f}"
                  f"  {r['requests']:4} req  {'DISABLED' if r['disabled'] else ''}")
    elif cmd == "export-kv":
        print(json.dumps(kv_entries(s.all(), budget), indent=1))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    _cli(sys.argv[1:])
