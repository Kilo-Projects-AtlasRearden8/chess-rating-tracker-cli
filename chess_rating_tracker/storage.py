"""Local JSON storage for players, games, and rating history."""

import csv
import json
import os
from datetime import datetime, timezone

from .rating_math import DEFAULT_STARTING_RATING, update_game


class Storage:
    def __init__(self, path):
        self.path = path
        self.players = {}      # name -> rating
        self.games = []        # list of game records
        self._loaded = False

    def load(self):
        if not os.path.exists(self.path):
            self.players = {}
            self.games = []
            self._loaded = True
            return
        with open(self.path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.players = {str(k): int(v) for k, v in data.get("players", {}).items()}
        self.games = data.get("games", [])
        self._loaded = True

    def save(self):
        data = {
            "players": self.players,
            "games": self.games,
        }
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)

    def player_rating(self, name):
        return self.players.get(name, DEFAULT_STARTING_RATING)

    def ensure_player(self, name, rating=None):
        if name not in self.players:
            self.players[name] = rating if rating is not None else DEFAULT_STARTING_RATING
        return self.players[name]

    def record_game(self, white, black, result, k_factor=None, played_at=None):
        if white == black:
            raise ValueError("a player cannot play against themselves")
        k_factor = k_factor if k_factor is not None else 32
        white_before = self.player_rating(white)
        black_before = self.player_rating(black)
        white_after, black_after = update_game(
            white_before, black_before, result, k_factor=k_factor
        )
        self.players[white] = white_after
        self.players[black] = black_after
        record = {
            "played_at": played_at or datetime.now(timezone.utc).isoformat(),
            "white": white,
            "black": black,
            "result": result,
            "white_before": white_before,
            "black_before": black_before,
            "white_after": white_after,
            "black_after": black_after,
            "k_factor": k_factor,
        }
        self.games.append(record)
        self.save()
        return record

    def history(self, name):
        """Rating history for a player: list of (played_at, rating_after)."""
        out = []
        for game in self.games:
            if game["white"] == name:
                out.append((game["played_at"], game["white_after"]))
            elif game["black"] == name:
                out.append((game["played_at"], game["black_after"]))
        return out

    def export_csv(self, path):
        """Export all games to a CSV file."""
        fields = [
            "played_at", "white", "black", "result",
            "white_before", "black_before",
            "white_after", "black_after", "k_factor",
        ]
        with open(path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            for game in self.games:
                writer.writerow({field: game.get(field, "") for field in fields})
