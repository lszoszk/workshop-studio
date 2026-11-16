# Teaser: a 30-second film of what the room built

Reads the Workshop Studio wall, runs the newest apps (one per person) offline with their data, screenshots each as it opens and after one search, and makes a 30 s, 1920×1080 film: title card, the apps with a slow push-in and a caption (title, model, builder's name when the wall has one), end card ("Retrieve, don't generate."), burned-in captions, narration, a synthesized music bed ducked under the voice, about -14 LUFS. Apps built on a participant's own file (`own_*`) are skipped. Apps that throw on open are logged and skipped.

Needs only `python3` with `playwright`, `httpx`, `numpy`, plus `ffmpeg` (all present on this laptop). Chrome is used if Playwright's Chromium is missing. Nothing is read from outside the repo. Seat codes are used in memory to pick one app per person and are never printed or written.

## The day

```bash
cd workshop-studio
# during the class: remake the teaser as apps arrive (first app, then every 3 more); scratch voice
python3 tools/teaser/teaser_watch.py --course geneva --day 2026-12-04 --label "Geneva" --date-text "4 December 2026"

# at the end: one run with the real voice, then put it on the server
python3 tools/teaser/teaser_watch.py --final --voice eleven --upload \
    --course geneva --day 2026-12-04 --label "Geneva" --date-text "4 December 2026"

# or a single run by hand (no watching, no upload)
python3 tools/teaser/make_teaser.py --day 2026-12-04 --label "Geneva" --date-text "4 December 2026" --voice eleven
```

Result: `tools/teaser/out/teaser-<time>.mp4` and `tools/teaser/out/latest.mp4`. Options: `--max-apps 5`, `--course` (only used once the wall has a `course` field; until then it is ignored with a note), `--day` (repeatable), `--out`, `--keep` (keep screenshots and frames in `out/work-*`).

`--upload` runs `ssh amuvmuser@150.254.115.204 mkdir -p …/server/state/teaser` and `scp`s `latest.mp4` to `/home/amuvmuser/workshop-studio/server/state/teaser/latest.mp4`. It needs your ssh key; the studio endpoint `/studio-api/teaser` has to serve that file.

## The projector page

`site/teaser.html` plays the video full screen on a black page: click or `F` toggles full screen (first click also turns the sound on; the video starts muted because browsers require that), `R` restarts, space pauses. It loads `https://150.254.115.204/studio-api/teaser`, or `?src=<url>` (e.g. `?src=../tools/teaser/out/latest.mp4` from a local server started in the repo root). If the video is missing it shows "The teaser is not ready yet" and retries every 30 s. When the server's file changes (ETag / Last-Modified, a HEAD request every 30 s) it shows "New version: click to reload" and does not reload by itself.

## Cost (ElevenLabs)

Six lines, about 400 characters (a few hundred; the run prints the exact number). A cached line costs nothing: takes are stored in `tools/teaser/cache/`, named by a hash of voice, model and text, so rerunning with the same lines and `--voice eleven` sends 0 characters. Any change to a line (a new name, a new count) sends that line again. The `scratch` voice (macOS `say -v Daniel`) is free and is the default: use it for every test. Voice id `JBFqnCBsd6RMkjVDRZzb`, model `eleven_v4`, key `ELEVENLABS_API_KEY` from `~/.env`.

Timing: the voice is trimmed of silences and sped up to at most 1.15x to fit 30 s; if it still does not fit, a warning is printed.

## Test on the Venice apps (no network cost, scratch voice)

```bash
python3 tools/teaser/make_teaser.py --day 2026-11-13 --label "Venice" --date-text "13 November 2026" --voice scratch --keep
```

About two to three minutes. Frames to look at: `ffmpeg -i tools/teaser/out/latest.mp4 -vf fps=1/5 tools/teaser/out/check/f%02d.png`. Then `python3 -m http.server 8000` in the repo root and open `http://localhost:8000/site/teaser.html?src=../tools/teaser/out/latest.mp4`.

## Files

`make_teaser.py` (everything), `teaser_watch.py` (polling, `--final`, `--upload`), `film/` (HTML film: `index.html`, `engine.js`, `film.js`, fonts; `data.js` and `shots/` are generated per run), `out/` and `cache/` (generated, ignored by git). The film is a pure function of time (`window.seek(t)`), as in the garage film studio.
