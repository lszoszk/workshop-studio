#!/usr/bin/env bash
# Install the Workshop Studio nginx block (location /studio-api/ → studio-api on 127.0.0.1:8011).
# Run once on the VM, as root:
#
#   ssh -t amuvmuser@150.254.115.204 'sudo bash /home/amuvmuser/workshop-studio/server/install-nginx.sh'
#     (-t allocates a terminal so sudo can prompt for the password)
#
#   …install-nginx.sh --dry-run   show what would change, change nothing (no root needed; on a machine
#                                 without nginx it prints the block and the upstream it would install)
#   …install-nginx.sh --remove    undo
#
# Same mechanics as the aiact installer: our block sits between markers inside the 443 server block,
# the upstream goes to its own conf.d file, backups are kept OUTSIDE sites-enabled/ (nginx includes
# that directory by glob), `nginx -t` runs before and after, and a failed test restores the backup
# without reloading. Idempotent: a re-run with the same block changes nothing.
#
# What the block does and does not do:
#   - proxy_buffering off + 300 s read timeout: the model's answer streams as SSE for up to minutes.
#   - NO per-IP limit_req / limit_conn: the whole workshop room reaches us from one NAT address.
#     The app limits each seat instead (60 requests / 5 minutes).
#   - CORS (https://lszoszk.github.io only) is answered by the app itself, so nginx adds no CORS
#     headers: two layers would send the header twice and browsers reject that.
#   - No X-Real-IP / X-Forwarded-For and access_log off: the studio never needs, and never keeps, a
#     participant's address (and the admin key in ?key= stays out of the access log).
set -euo pipefail
SITE="${SITE:-/etc/nginx/sites-enabled/default}"
UPSTREAM="${UPSTREAM:-/etc/nginx/conf.d/studio-upstream.conf}"
BACKUP_DIR="${BACKUP_DIR:-/etc/nginx/studio-backups}"
MARK_A="# >>> studio-api (Workshop Studio) >>>"
MARK_B="# <<< studio-api <<<"
MODE="${1:-}"

BLOCK=$(cat <<'NGINX'
  # >>> studio-api (Workshop Studio) >>>
  # GHRH "AI for Human Rights Professionals", ITU Geneva, 4.12.2026. Remove after the workshop:
  # sudo bash /home/amuvmuser/workshop-studio/server/install-nginx.sh --remove
  location /studio-api/ {
    proxy_pass http://studio_app;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto https;
    proxy_buffering off;                 # SSE: every chunk goes out as it arrives
    proxy_cache off;
    proxy_connect_timeout 3s;            # a dead container fails fast, so the front fails over fast
    proxy_read_timeout 300s;             # a long answer streams for minutes
    proxy_send_timeout 300s;
    client_max_body_size 8m;             # conversation with earlier page versions and up to three screenshots; gallery pages ≤ 300 kB
    gzip off;
    access_log off;
    add_header X-Robots-Tag "noindex, nofollow" always;
  }
  # <<< studio-api <<<
NGINX
)
NEW_UPSTREAM=$(cat <<'NGINX'
# Workshop Studio (studio-api container). max_fails: a stopped container answers 502 at once and the
# studio front switches to the Cloudflare Worker.
upstream studio_app { server 127.0.0.1:8011 max_fails=3 fail_timeout=10s; keepalive 16; }
NGINX
)

strip_block() {   # $1 = file to edit in place
  python3 - "$1" "$MARK_A" "$MARK_B" <<'PY'
import sys, re
path, a, b = sys.argv[1:4]
t = open(path).read()
t = re.sub(r"[ \t]*" + re.escape(a) + r".*?" + re.escape(b) + r"[ \t]*\n?", "", t, flags=re.S)
open(path, "w").write(t)
PY
}

insert_block() {  # $1 = source, $2 = destination: the block goes before the 443 server block's closing brace
  python3 - "$1" "$2" <<PY
import re, sys
src, dst = sys.argv[1], sys.argv[2]
block = """$BLOCK"""
lines = open(src).read().splitlines(keepends=True)
code = lambda l: l.split('#', 1)[0]          # brace counting must ignore comments

def closing(start):
    depth = 0
    for i in range(start, len(lines)):
        c = code(lines[i])
        depth += c.count('{') - c.count('}')
        if depth == 0 and i > start:
            return i
    sys.exit("a server block is not closed")

# the first server block whose OWN lines say 'listen 443' (not one that merely precedes it)
start = end = None
for i, l in enumerate(lines):
    if re.match(r'\s*server\s*\{', code(l)):
        j = closing(i)
        if re.search(r'listen\s+443', "".join(code(x) for x in lines[i:j])):
            start, end = i, j
            break
if start is None:
    sys.exit("could not find the 443 server block")
lines.insert(end, block.rstrip("\n") + "\n")
open(dst, "w").write("".join(lines))
print(f"  inserting before line {end + 1} (closing brace of the server block that starts at line {start + 1})")
PY
}

# ── dry run: no root, nothing written outside mktemp ──
if [ "$MODE" = "--dry-run" ]; then
  echo "DRY RUN: nothing is written, nginx is not tested or reloaded."
  echo "── $UPSTREAM would contain ──"; echo "$NEW_UPSTREAM"
  if [ -r "$SITE" ]; then
    CUR=$(mktemp); TMP=$(mktemp); cp "$SITE" "$CUR"
    grep -q "$MARK_A" "$CUR" && strip_block "$CUR"
    insert_block "$CUR" "$TMP"
    echo "── diff for $SITE ──"; diff -u "$SITE" "$TMP" || true
    rm -f "$CUR" "$TMP"
  else
    echo "── $SITE is not readable here; this block would go inside its 443 server block ──"
    echo "$BLOCK"
  fi
  echo "── then: back up to $BACKUP_DIR, nginx -t, systemctl reload nginx (restore + no reload if the test fails)"
  exit 0
fi

[ "$(id -u)" = "0" ] || { echo "run me with sudo (or use --dry-run)"; exit 1; }
mkdir -p "$BACKUP_DIR"
STAMP=$(date +%Y%m%d-%H%M%S)

if [ "$MODE" = "--remove" ]; then
  B="$BACKUP_DIR/default.$STAMP.bak"
  cp -a "$SITE" "$B"
  UB=""; [ -f "$UPSTREAM" ] && { UB="$BACKUP_DIR/studio-upstream.$STAMP.bak"; cp -a "$UPSTREAM" "$UB"; }
  strip_block "$SITE"
  rm -f "$UPSTREAM"
  if nginx -t; then
    systemctl reload nginx
    echo "✓ removed (backup: $B)"
  else
    echo "✗ nginx -t failed — restoring $B"
    cp -a "$B" "$SITE"; [ -n "$UB" ] && cp -a "$UB" "$UPSTREAM"
    exit 1
  fi
  exit 0
fi

nginx -t 2>/dev/null || { echo '✗ the nginx config is already invalid — fix that first, nothing changed:'; nginx -t || true; exit 1; }

CUR=$(mktemp); TMP=$(mktemp)        # outside /etc/nginx, so neither is ever parsed
cp -a "$SITE" "$CUR"
grep -q "$MARK_A" "$CUR" && strip_block "$CUR"
insert_block "$CUR" "$TMP"

if diff -q "$SITE" "$TMP" >/dev/null && [ -f "$UPSTREAM" ] && diff -q <(echo "$NEW_UPSTREAM") "$UPSTREAM" >/dev/null; then
  echo "✓ already up to date — nothing to change"
  rm -f "$CUR" "$TMP"; exit 0
fi

BACKUP="$BACKUP_DIR/default.$STAMP.bak"
cp -a "$SITE" "$BACKUP"
UPSTREAM_BACKUP=""
if [ -f "$UPSTREAM" ]; then UPSTREAM_BACKUP="$BACKUP_DIR/studio-upstream.$STAMP.bak"; cp -a "$UPSTREAM" "$UPSTREAM_BACKUP"; fi
echo "$NEW_UPSTREAM" > "$UPSTREAM"
cat "$TMP" > "$SITE"
rm -f "$CUR" "$TMP"

if nginx -t; then
  systemctl reload nginx
  echo "✓ installed (backup: $BACKUP)"
  echo "  check: curl -s https://150.254.115.204/studio-api/health"
else
  echo "✗ nginx -t failed — restoring, nginx NOT reloaded"
  cp -a "$BACKUP" "$SITE"
  if [ -n "$UPSTREAM_BACKUP" ]; then cp -a "$UPSTREAM_BACKUP" "$UPSTREAM"; else rm -f "$UPSTREAM"; fi
  if nginx -t 2>/dev/null; then
    echo "  ✓ config is back to its previous, valid state (backup: $BACKUP)"
  else
    echo "  ✗✗ THE CONFIG IS STILL INVALID. Restore by hand and do not reload until it passes:"
    echo "       sudo cp -a $BACKUP $SITE && sudo nginx -t"
  fi
  exit 1
fi
