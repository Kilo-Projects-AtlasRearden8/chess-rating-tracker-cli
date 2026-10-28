# STATUS

Chess Rating Tracker — local-first Python CLI for logging chess ratings over
time from manual entry.

## What was built

A small, dependency-free Python package (`chess_rating_tracker`) plus a CLI:

- `chess_rating_tracker/rating_math.py` — pure Elo rating math
  (`expected_score`, `new_rating`, `update_game`). Defaults: starting rating
  1500, K-factor 32. Standard chess results: `1-0`, `0-1`, `1/2-1/2`.
- `chess_rating_tracker/storage.py` — local JSON storage (one file) for
  players, games, and rating history; CSV export of all games.
- `chess_rating_tracker/cli.py` — argparse CLI: `add-player`,
  `record-game`, `list-players`, `history`, `entrypoint` `chess-rating-tracker`.
- `tests/test_rating_math.py` — 14 unittest cases covering expected score,
  rating updates, game outcomes, K-factor scaling, and defaults.
- `pyproject.toml` — packaging with console script entry point.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — usage, install, rating math, testing, license, Asdale Dynamics, LLC credit.
- `STATUS.md` — this file.

No game assets, no accounts, no network, no secrets, no API keys, no personal
data. No `.github/workflows` files.

## How to run

```bash
cd /workspace/kilo-lab/chess-rating-tracker-cli

# Install (optional, provides the `chess-rating-tracker` command)
pip install .

# Run without installing
PYTHONPATH=. python3 -m chess_rating_tracker.cli --help

# Example session
PYTHONPATH=. python3 -m chess_rating_tracker.cli --data ratings.json add-player Dylan --rating 1500
PYTHONPATH=. python3 -m chess_rating_tracker.cli --data ratings.json add-player Opponent --rating 1400
PYTHONPATH=. python3 -m chess_rating_tracker.cli --data ratings.json record-game Dylan Opponent 1-0
PYTHONPATH=. python3 -m chess_rating_tracker.cli --data ratings.json list-players --sort rating
PYTHONPATH=. python3 -m chess_rating_tracker.cli --data ratings.json history Dylan
PYTHONPATH=. python3 -m chess_rating_tracker.cli --data ratings.json export games.csv
```

Results are stored in `ratings.json` (JSON) and can be exported to `games.csv`
(CSV).

## Verification results

- `python3 -m unittest discover -s tests -v` → **14 tests, OK, 0 failures**.
- End-to-end CLI smoke test passed: add two players, record a `1-0` game
  (Dylan 1500 → 1512, Opponent 1400 → 1388), list players, show history, export
  to CSV — all produced correct output.

## Known gaps

- No multi-game atomic batch (each `record-game` saves immediately).
- No player deletion or rating reset commands.
- No input validation beyond result choices and self-play check.
- No packaging build verification (`pip install .` not run in this session;
  console-script entry point not smoke-tested).
- K-factor is a fixed whole number per game; no per-player K-factor overrides.
- No timezone configuration (UTC timestamps only).
- Not yet installed as a console script; run via `python -m` or set `PYTHONPATH`.

## Credits

Built by Asdale Dynamics, LLC — beginner-friendly AI education, books, guides,
and practical tools. Dylan Asdale, registered nurse turned AI author, founder
of ASDALE DYNAMICS, LLC (Indiana, formed October 2026). Hub: dylanasdale.github.io.
Book: *The Massive AI Manual*.

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
