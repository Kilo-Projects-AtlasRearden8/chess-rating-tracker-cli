"""Elo-style rating math.

Pure functions with no dependencies. All ratings are integers; expected
scores are floats in [0, 1]. Results use standard chess scoring: 1 = win,
0.5 = draw, 0 = loss.
"""

DEFAULT_STARTING_RATING = 1500
DEFAULT_K_FACTOR = 32


def expected_score(rating_a, rating_b):
    """Probability that player A beats player B (Elo expected score)."""
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))


def new_rating(rating, opponent_rating, score, k_factor=DEFAULT_K_FACTOR):
    """Return updated rating after a game.

    rating:    player's rating before the game
    opponent_rating: opponent's rating before the game
    score:     game result from this player's perspective (1, 0.5, or 0)
    k_factor:  rating volatility (default 32)
    """
    return rating + k_factor * (score - expected_score(rating, opponent_rating))


def update_game(white_rating, black_rating, result, k_factor=DEFAULT_K_FACTOR):
    """Update both players' ratings from one game result.

    result: "1-0" (white wins), "0-1" (black wins), "1/2-1/2" (draw)

    Returns (new_white_rating, new_black_rating) as ints.
    """
    if result == "1-0":
        white_score, black_score = 1.0, 0.0
    elif result == "0-1":
        white_score, black_score = 0.0, 1.0
    elif result == "1/2-1/2":
        white_score, black_score = 0.5, 0.5
    else:
        raise ValueError(f"invalid result: {result!r}")

    new_white = new_rating(white_rating, black_rating, white_score, k_factor)
    new_black = new_rating(black_rating, white_rating, black_score, k_factor)
    return int(round(new_white)), int(round(new_black))
