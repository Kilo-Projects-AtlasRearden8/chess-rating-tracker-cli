# Chess Rating Tracker

A small, local-first Python CLI for logging chess ratings over time from
manual entry. Ratings are stored in a local JSON file and can be exported
to CSV. No accounts, no game assets, no network calls. A fan project by
and for chess enthusiasts, published by Asdale Dynamics, LLC.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of
ASDALE DYNAMICS, LLC (Indiana, formed October 2026). His book *The
Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a
friend would": plain English, step by step, never condescending.

This tool fits the LLC's "fun extras" line: accessible, beginner-friendly
software for everyday hobbies and life admin — chess in this case. It is
local-first, tested, and contains no secrets, API keys, or personal data.

## Features

- Manual entry of chess games with Elo-style rating updates
- Local JSON storage (one file, easy to back up or move)
- CSV export of all recorded games
- Per-player rating history
- Pure-Python rating math with no dependencies
- Tested rating math (unittest)

## Install

```bash
git clone <this-repo>
cd chess-rating-tracker-cli
pip install .
```

Or run without installing:

```bash
python -m chess_rating_tracker.cli --help
```

## Usage

```bash
# Add players
chess-rating-tracker add-player "Dylan" --rating 1500
chess-rating-tracker add-player "Opponent" --rating 1400

# Record a game (result: 1-0 white win, 0-1 black win, 1/2-1/2 draw)
chess-rating-tracker record-game "Dylan" "Opponent" 1-0

# List players and ratings
chess-rating-tracker list-players

# Rating history for a player
chess-rating-tracker history "Dylan"

# Export all games to CSV
chess-rating-tracker export games.csv

# Use a different data file
chess-rating-tracker --data my_ratings.json list-players
```

## Rating math

Standard Elo: expected score `1 / (1 + 10^((opponent - rating) / 400))`,
update `rating + K * (score - expected)` with default K = 32 and a
starting rating of 1500.

## Testing

```bash
python -m unittest discover -s tests -v
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

Credit: built by Asdale Dynamics, LLC — beginner-friendly AI education,
books, guides, and practical tools. dylanasdale.github.io
