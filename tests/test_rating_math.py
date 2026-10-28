"""Tests for chess rating math."""

import unittest

from chess_rating_tracker.rating_math import (
    DEFAULT_K_FACTOR,
    DEFAULT_STARTING_RATING,
    expected_score,
    new_rating,
    update_game,
)


class TestExpectedScore(unittest.TestCase):
    def test_equal_ratings(self):
        self.assertAlmostEqual(expected_score(1500, 1500), 0.5)

    def test_higher_rated_favored(self):
        self.assertGreater(expected_score(1600, 1400), 0.5)
        self.assertLess(expected_score(1400, 1600), 0.5)

    def test_bounds(self):
        self.assertGreaterEqual(expected_score(3000, 1000), 0.0)
        self.assertLessEqual(expected_score(3000, 1000), 1.0)
        self.assertGreaterEqual(expected_score(1000, 3000), 0.0)
        self.assertLessEqual(expected_score(1000, 3000), 1.0)

    def test_400_point_difference(self):
        # ~10x odds ratio => ~0.909 expected score
        self.assertAlmostEqual(expected_score(1500, 1100), 0.909090909, places=6)


class TestNewRating(unittest.TestCase):
    def test_win_against_equal_gains_points(self):
        new = new_rating(1500, 1500, 1.0)
        self.assertEqual(new, 1500 + int(round(DEFAULT_K_FACTOR * 0.5)))

    def test_loss_against_equal_loses_points(self):
        new = new_rating(1500, 1500, 0.0)
        self.assertEqual(new, 1500 - int(round(DEFAULT_K_FACTOR * 0.5)))

    def test_draw_no_change_against_equal(self):
        self.assertEqual(new_rating(1500, 1500, 0.5), 1500)

    def test_beating_stronger_opponent_gains_more(self):
        gain_weak = new_rating(1000, 2000, 1.0) - 1000
        gain_strong = new_rating(2000, 1000, 1.0) - 2000
        self.assertGreater(gain_weak, gain_strong)

    def test_k_factor_scales_change(self):
        normal = new_rating(1500, 1500, 1.0, k_factor=32)
        custom = new_rating(1500, 1500, 1.0, k_factor=16)
        self.assertEqual(custom - 1500, (normal - 1500) / 2)


class TestUpdateGame(unittest.TestCase):
    def test_white_win(self):
        white, black = update_game(1500, 1500, "1-0")
        self.assertEqual(white, 1516)
        self.assertEqual(black, 1484)

    def test_black_win(self):
        white, black = update_game(1500, 1500, "0-1")
        self.assertEqual(white, 1484)
        self.assertEqual(black, 1516)

    def test_draw(self):
        white, black = update_game(1500, 1500, "1/2-1/2")
        self.assertEqual(white, 1500)
        self.assertEqual(black, 1500)

    def test_invalid_result(self):
        with self.assertRaises(ValueError):
            update_game(1500, 1500, "1-1")


class TestDefaults(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(DEFAULT_STARTING_RATING, 1500)
        self.assertEqual(DEFAULT_K_FACTOR, 32)


if __name__ == "__main__":
    unittest.main()
