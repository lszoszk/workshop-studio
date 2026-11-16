#!/usr/bin/env python3
"""Watch the wall during a class and keep tools/teaser/out/latest.mp4 fresh.

    python3 tools/teaser/teaser_watch.py --course geneva --day 2026-12-04 --label "Geneva" --date-text "4 December 2026" --voice scratch
    python3 tools/teaser/teaser_watch.py ... --final --voice eleven --upload     # the last run: real voice, then copy to the server

Polls every 60 s. Makes the first teaser when the first app appears, then again after every 3 new apps.
`--final` makes one teaser now and exits. `--upload` copies out/latest.mp4 to the studio server after each run (scp, ssh key needed).
"""
import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import make_teaser as mt   # same folder

REMOTE = "amuvmuser@150.254.115.204"
REMOTE_DIR = "/home/amuvmuser/workshop-studio/server/state/teaser"


def stamp():
    return datetime.now().strftime("%H:%M:%S")


def count(a):
    try:
        return len([i for i in mt.filter_wall(mt.fetch_wall(), a.day, a.course)
                    if not any(str(k).startswith("own_") for k in i.get("files") or [])])
    except Exception as e:   # the network may blink in a classroom; try again next minute
        print(f"[{stamp()}] wall not reachable ({type(e).__name__}); will retry", flush=True)
        return None


def upload(latest: Path):
    subprocess.run(["ssh", REMOTE, f"mkdir -p {REMOTE_DIR}"], check=True)
    subprocess.run(["scp", str(latest), f"{REMOTE}:{REMOTE_DIR}/latest.mp4"], check=True)
    print(f"[{stamp()}] uploaded to {REMOTE}:{REMOTE_DIR}/latest.mp4", flush=True)


def build(a, n):
    print(f"[{stamp()}] making a teaser from {n} app(s)", flush=True)
    try:
        mp4 = mt.make(a)
        print(f"[{stamp()}] done: {mp4.name}", flush=True)
        if a.upload:
            upload(Path(a.out).resolve() / "latest.mp4")
        return True
    except SystemExit as e:
        print(f"[{stamp()}] run failed: {e}", flush=True)
    except Exception as e:
        print(f"[{stamp()}] run failed: {type(e).__name__}: {e}", flush=True)
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--final", action="store_true", help="make one teaser now and exit")
    ap.add_argument("--upload", action="store_true", help="scp latest.mp4 to the studio server after each run")
    ap.add_argument("--every", type=int, default=3, help="make a new one after this many new apps")
    ap.add_argument("--poll", type=int, default=60, help="seconds between looks at the wall")
    # the rest is make_teaser's own options
    a, rest = ap.parse_known_args()
    sys.argv = [sys.argv[0]] + rest
    ma = mt.parse_args()
    ma.final, ma.upload, ma.every, ma.poll = a.final, a.upload, a.every, a.poll
    if a.final:
        sys.exit(0 if build(ma, count(ma) or "?") else 1)
    last = 0
    while True:
        n = count(ma)
        if n is not None:
            print(f"[{stamp()}] {n} app(s) on the wall", flush=True)
            if n >= 1 and (last == 0 or n >= last + a.every):
                if build(ma, n):
                    last = n
        time.sleep(a.poll)


if __name__ == "__main__":
    main()
