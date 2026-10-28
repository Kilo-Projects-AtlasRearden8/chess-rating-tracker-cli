"""Command-line interface for the chess rating tracker."""

import argparse
import sys

from .rating_math import DEFAULT_STARTING_RATING
from .storage import Storage


def build_parser():
    parser = argparse.ArgumentParser(
        prog="chess-rating-tracker",
        description="Log chess ratings over time from manual entry (local JSON storage, CSV export).",
    )
    parser.add_argument(
        "--data", default="ratings.json",
        help="Path to the JSON data file (default: ratings.json)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add-player", help="Add or update a player")
    p_add.add_argument("name")
    p_add.add_argument("--rating", type=int, default=DEFAULT_STARTING_RATING)

    p_game = sub.add_parser("record-game", help="Record a game and update ratings")
    p_game.add_argument("white")
    p_game.add_argument("black")
    p_game.add_argument("result", choices=["1-0", "0-1", "1/2-1/2"])
    p_game.add_argument("--k-factor", type=int, default=32)

    p_list = sub.add_parser("list-players", help="List players and ratings")
    p_list.add_argument("--sort", choices=["name", "rating"], default="rating")

    p_hist = sub.add_parser("history", help="Show a player's rating history")
    p_hist.add_argument("name")

    p_export = sub.add_parser("export", help="Export all games to CSV")
    p_export.add_argument("csv_file")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.data)
    storage.load()

    if args.command == "add-player":
        rating = storage.ensure_player(args.name, args.rating)
        print(f"{args.name}: {rating}")
        storage.save()
        return 0

    if args.command == "record-game":
        try:
            record = storage.record_game(
                args.white, args.black, args.result,
                k_factor=args.k_factor,
            )
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(
            f"{record['white']} {record['white_before']} -> {record['white_after']}  |  "
            f"{record['black']} {record['black_before']} -> {record['black_after']}  "
            f"({record['result']})"
        )
        return 0

    if args.command == "list-players":
        items = sorted(
            storage.players.items(),
            key=lambda item: (item[1], item[0]) if args.sort == "rating" else item[0],
            reverse=(args.sort == "rating"),
        )
        if not items:
            print("No players yet.")
            return 0
        width = max(len(name) for name, _ in items)
        for name, rating in items:
            print(f"{name:<{width}}  {rating}")
        return 0

    if args.command == "history":
        hist = storage.history(args.name)
        if not hist:
            print(f"No games recorded for {args.name}.")
            return 0
        print(f"{args.name} rating history:")
        for played_at, rating in hist:
            print(f"  {played_at}  {rating}")
        return 0

    if args.command == "export":
        storage.export_csv(args.csv_file)
        print(f"Exported {len(storage.games)} games to {args.csv_file}")
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
