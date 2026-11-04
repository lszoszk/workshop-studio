#!/usr/bin/env bash
# Ship the Workshop Studio API to the VM and (re)start the container studio-api on 127.0.0.1:8011.
# Nothing here needs root. The nginx location is installed once, by hand: see install-nginx.sh.
#
#   bash server/deploy.sh             # tests, sync code + prompt files, rebuild, restart, wait for health
#   bash server/deploy.sh --dry-run   # print every step, touch nothing (no ssh at all)
#   The seat list tools/out/seats.csv (tools/make_seats.py; git-ignored) is shipped when it exists, or
#   SEATS_CSV=path. After the restart it is imported: new seats are added, known seats get the CSV's
#   country/label/budget, and spending is kept.
#
# The OpenRouter key comes from ~/.env on this laptop and is written once to server/.env on the VM
# (mode 600), together with a freshly generated STUDIO_ADMIN_KEY. It never goes into git or the image.
set -euo pipefail
VM_HOST="${VM_HOST:-amuvmuser@150.254.115.204}"
VM_DIR="${VM_DIR:-/home/amuvmuser/workshop-studio}"
PORT=8011
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
cd "$(dirname "$0")/.."
STAMP="$(date +%Y%m%d-%H%M)"

run() {            # run a local command, or show it
  if [ "$DRY" = 1 ]; then printf '  would run: %s\n' "$*"; else "$@"; fi
}
remote() {         # run a command on the VM, or show it
  if [ "$DRY" = 1 ]; then printf '  would run on %s: %s\n' "$VM_HOST" "$1"; else ssh "$VM_HOST" "$1"; fi
}

[ "$DRY" = 1 ] && echo "DRY RUN: nothing is sent, built or restarted."

echo "▸ unit tests"
run python3 -m pytest tests/test_server.py -q -p no:cacheprovider

echo "▸ syncing → $VM_HOST:$VM_DIR"
remote "mkdir -p $VM_DIR/server/state $VM_DIR/site/data"
run rsync -az --delete --exclude=state/ --exclude=.env --exclude=__pycache__ --exclude='*.pyc' \
    server/ "$VM_HOST:$VM_DIR/server/"
# the build system message is assembled from these three at start-up (server/app.py build_system_prompt)
PROMPT_FILES=(site/data/system_prompt.md site/data/schema.md site/data/samples.json)
for f in "${PROMPT_FILES[@]}"; do
  [ -f "$f" ] || { echo "✗ $f missing: build the data pack first (tools/build_data.py)"; exit 1; }
done
run rsync -az "${PROMPT_FILES[@]}" "$VM_HOST:$VM_DIR/site/data/"
SEATS_CSV="${SEATS_CSV:-}"
[ -z "$SEATS_CSV" ] && [ -f tools/out/seats.csv ] && SEATS_CSV=tools/out/seats.csv
if [ -n "$SEATS_CSV" ]; then
  [ -f "$SEATS_CSV" ] || { echo "✗ SEATS_CSV=$SEATS_CSV does not exist"; exit 1; }
  # over ssh with umask 077 (mode 600): the rsync on macOS has no --chmod
  if [ "$DRY" = 1 ]; then echo "  would copy $SEATS_CSV to $VM_DIR/server/state/seats.csv (mode 600)"
  else ssh "$VM_HOST" "umask 077; cat > $VM_DIR/server/state/seats.csv" < "$SEATS_CSV"; fi
fi

echo "▸ secrets (server/.env on the VM, created once)"
if [ "$DRY" = 1 ]; then
  echo "  would check $VM_DIR/server/.env; if missing, write OPENROUTER_API_KEY from ~/.env and a new"
  echo "  STUDIO_ADMIN_KEY (openssl rand) with umask 077. No key is printed."
  grep -q '^OPENROUTER_API_KEY=' ~/.env 2>/dev/null && echo "  ~/.env has OPENROUTER_API_KEY: yes" \
                                                   || echo "  ~/.env has OPENROUTER_API_KEY: NO — the real run would stop here"
elif ! ssh "$VM_HOST" "test -f $VM_DIR/server/.env"; then
  grep -q '^OPENROUTER_API_KEY=' ~/.env || { echo "✗ no OPENROUTER_API_KEY in ~/.env"; exit 1; }
  { grep '^OPENROUTER_API_KEY=' ~/.env; echo "STUDIO_ADMIN_KEY=$(openssl rand -hex 16)"; } \
    | ssh "$VM_HOST" "umask 077; cat > $VM_DIR/server/.env"
  echo "  ✓ written. Read the admin key with: ssh $VM_HOST 'grep ADMIN $VM_DIR/server/.env'"
else
  echo "  present, left as it is"
fi
# Claude goes straight to Anthropic (server/models.py): its key joins the VM's .env once, the same way
if [ "$DRY" = 1 ]; then
  echo "  would add ANTHROPIC_API_KEY from ~/.env to $VM_DIR/server/.env if it is not there yet"
elif grep -q '^ANTHROPIC_API_KEY=' ~/.env 2>/dev/null && ! ssh "$VM_HOST" "grep -q '^ANTHROPIC_API_KEY=' $VM_DIR/server/.env"; then
  grep '^ANTHROPIC_API_KEY=' ~/.env | ssh "$VM_HOST" "umask 077; cat >> $VM_DIR/server/.env"
  echo "  ✓ ANTHROPIC_API_KEY added (not printed)"
fi

# Same guard as aiact: the box runs production services on a disk near 90% full.
echo "▸ checking disk headroom"
remote 'free=$(df -BM --output=avail / | tail -1 | tr -dc 0-9); echo "  ${free}M free"; [ "$free" -ge 2048 ] || { echo "  ✗ under 2 GB free — not building. Try: docker image prune -f"; exit 1; }'

echo "▸ building and starting studio-api"
remote "cd $VM_DIR && STUDIO_BUILD=$STAMP docker compose -f server/docker-compose.yml up -d --build"
echo "▸ clearing our superseded images"
remote 'docker image prune -f --filter "label=app=studio-api" | tail -1'
echo "▸ waiting for health"
remote "for i in \$(seq 1 30); do curl -fsS http://127.0.0.1:$PORT/studio-api/health >/dev/null && { echo '  healthy'; exit 0; }; sleep 2; done; echo '  ✗ not healthy after 60 s — docker logs studio-api'; exit 1"
if [ -n "$SEATS_CSV" ]; then
  echo "▸ importing seats ($SEATS_CSV)"
  remote "docker exec studio-api python seats.py import /state/seats.csv"
fi
echo
if [ "$DRY" = 1 ]; then echo "✓ dry run finished"; exit 0; fi
echo "✓ studio-api up on 127.0.0.1:$PORT (build $STAMP)"
echo "  after a change to system_prompt.md, schema.md or samples.json: run this again (read at start-up)"
echo "  public, once install-nginx.sh has run:"
echo "    https://150.254.115.204/studio-api/health"
echo "    https://150.254.115.204/studio-api/admin?key=…"
