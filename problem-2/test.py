import importlib
import math
import unittest


def _load_impl():
    try:
        mod = importlib.import_module("solution")
        return mod.compute_game
    except ModuleNotFoundError as exc:
        if exc.name != "solution":
            raise
        raise ImportError(
            "No implementation found. Provide `solution.py` "
            "with a `compute_game` function."
        ) from exc


compute_game = _load_impl()


class TestGlickoCalculator(unittest.TestCase):
    """
    Tests for a Glicko-2 rating calculator for two-player games.

    Validated against the Lichess scalachess implementation:
    https://github.com/lichess-org/scalachess

    compute_game(white, black, outcome, tau=0.75, skip_deviation_increase=False)

    Parameters:
        white: dict  {"rating": float, "deviation": float, "volatility": float}
        black: dict  {"rating": float, "deviation": float, "volatility": float}
        outcome: str  "white" | "black" | "draw"
        tau: float  system constant (default 0.75)
        skip_deviation_increase: bool  (default False)

    Returns:
        (white_result, black_result)  — same dict shape as inputs
    """

    def assertCloseTo(self, actual, expected, tolerance, msg=None):
        diff = abs(actual - expected)
        if msg is None:
            msg = (
                f"Expected {expected} ± {tolerance}, "
                f"got {actual} (diff={diff:.10f})"
            )
        self.assertLessEqual(diff, tolerance, msg)

    # ── Group 1: Equal players  (1500 / 350 / 0.06) ─────────────────────

    def test_equal_players_white_wins(self):
        p = {"rating": 1500.0, "deviation": 350.0, "volatility": 0.06}
        w, b = compute_game(
            p.copy(), p.copy(), "white", tau=0.75, skip_deviation_increase=True
        )
        self.assertCloseTo(w["rating"], 1662.21, 0.005)
        self.assertCloseTo(b["rating"], 1337.79, 0.005)
        # outcome equally probable → symmetric deviations
        self.assertAlmostEqual(w["deviation"], b["deviation"], places=10)
        self.assertCloseTo(w["deviation"], 290.2305, 0.00005)
        # outcome equally probable → symmetric volatilities
        self.assertAlmostEqual(w["volatility"], b["volatility"], places=10)
        self.assertCloseTo(w["volatility"], 0.0599993, 0.0000001)

    def test_equal_players_black_wins(self):
        p = {"rating": 1500.0, "deviation": 350.0, "volatility": 0.06}
        w, b = compute_game(
            p.copy(), p.copy(), "black", tau=0.75, skip_deviation_increase=True
        )
        self.assertCloseTo(w["rating"], 1337.79, 0.005)
        self.assertCloseTo(b["rating"], 1662.21, 0.005)
        self.assertAlmostEqual(w["deviation"], b["deviation"], places=10)
        self.assertCloseTo(w["deviation"], 290.2305, 0.00005)
        self.assertAlmostEqual(w["volatility"], b["volatility"], places=10)
        self.assertCloseTo(w["volatility"], 0.0599993, 0.0000001)

    def test_equal_players_draw(self):
        p = {"rating": 1500.0, "deviation": 350.0, "volatility": 0.06}
        w, b = compute_game(
            p.copy(), p.copy(), "draw", tau=0.75, skip_deviation_increase=True
        )
        self.assertCloseTo(w["rating"], 1500.0, 0.005)
        self.assertCloseTo(b["rating"], 1500.0, 0.005)
        self.assertAlmostEqual(w["deviation"], b["deviation"], places=10)
        self.assertCloseTo(w["deviation"], 290.2305, 0.00005)
        self.assertAlmostEqual(w["volatility"], b["volatility"], places=10)
        # draw is the most expected outcome → different volatility shift
        self.assertCloseTo(w["volatility"], 0.0599977, 0.0000001)

    # ── Group 2: Mixed ratings  (1400/79/0.06 vs 1550/110/0.065) ────────

    def test_mixed_ratings_white_wins(self):
        white = {"rating": 1400.0, "deviation": 79.0, "volatility": 0.06}
        black = {"rating": 1550.0, "deviation": 110.0, "volatility": 0.065}
        w, b = compute_game(white, black, "white", tau=0.75, skip_deviation_increase=True)
        self.assertCloseTo(w["rating"], 1422.63, 0.005)
        self.assertCloseTo(b["rating"], 1506.32, 0.005)
        self.assertCloseTo(w["deviation"], 77.4956, 0.00005)
        self.assertCloseTo(b["deviation"], 105.8706, 0.00005)
        self.assertCloseTo(w["volatility"], 0.06, 0.00001)
        self.assertCloseTo(b["volatility"], 0.065, 0.00001)

    def test_mixed_ratings_black_wins(self):
        white = {"rating": 1400.0, "deviation": 79.0, "volatility": 0.06}
        black = {"rating": 1550.0, "deviation": 110.0, "volatility": 0.065}
        w, b = compute_game(white, black, "black", tau=0.75, skip_deviation_increase=True)
        self.assertCloseTo(w["rating"], 1389.99, 0.005)
        self.assertCloseTo(b["rating"], 1568.90, 0.005)
        self.assertCloseTo(w["deviation"], 77.4956, 0.00005)
        self.assertCloseTo(b["deviation"], 105.8706, 0.00005)
        self.assertCloseTo(w["volatility"], 0.06, 0.00001)
        self.assertCloseTo(b["volatility"], 0.065, 0.00001)

    def test_mixed_ratings_draw(self):
        white = {"rating": 1400.0, "deviation": 79.0, "volatility": 0.06}
        black = {"rating": 1550.0, "deviation": 110.0, "volatility": 0.065}
        w, b = compute_game(white, black, "draw", tau=0.75, skip_deviation_increase=True)
        self.assertCloseTo(w["rating"], 1406.31, 0.005)
        self.assertCloseTo(b["rating"], 1537.61, 0.005)
        self.assertCloseTo(w["deviation"], 77.4956, 0.00005)
        self.assertCloseTo(b["deviation"], 105.8706, 0.00005)
        self.assertCloseTo(w["volatility"], 0.06, 0.00001)
        self.assertCloseTo(b["volatility"], 0.065, 0.00001)

    # ── Group 3: Large rating gap  (1200/60/0.053 vs 1850/200/0.062) ────

    def test_large_gap_white_wins(self):
        white = {"rating": 1200.0, "deviation": 60.0, "volatility": 0.053}
        black = {"rating": 1850.0, "deviation": 200.0, "volatility": 0.062}
        w, b = compute_game(white, black, "white", tau=0.75, skip_deviation_increase=True)
        self.assertCloseTo(w["rating"], 1216.73, 0.005)
        self.assertCloseTo(b["rating"], 1635.99, 0.005)
        self.assertCloseTo(w["deviation"], 59.9006, 0.00005)
        self.assertCloseTo(b["deviation"], 196.9873, 0.00005)
        self.assertCloseTo(w["volatility"], 0.053013, 0.000001)
        self.assertCloseTo(b["volatility"], 0.062028, 0.000001)

    def test_large_gap_black_wins(self):
        white = {"rating": 1200.0, "deviation": 60.0, "volatility": 0.053}
        black = {"rating": 1850.0, "deviation": 200.0, "volatility": 0.062}
        w, b = compute_game(white, black, "black", tau=0.75, skip_deviation_increase=True)
        self.assertCloseTo(w["rating"], 1199.29, 0.005)
        self.assertCloseTo(b["rating"], 1855.42, 0.005)
        self.assertCloseTo(w["deviation"], 59.9006, 0.00005)
        self.assertCloseTo(b["deviation"], 196.9873, 0.00005)
        self.assertCloseTo(w["volatility"], 0.052999, 0.000001)
        self.assertCloseTo(b["volatility"], 0.061999, 0.000001)

    def test_large_gap_draw(self):
        white = {"rating": 1200.0, "deviation": 60.0, "volatility": 0.053}
        black = {"rating": 1850.0, "deviation": 200.0, "volatility": 0.062}
        w, b = compute_game(white, black, "draw", tau=0.75, skip_deviation_increase=True)
        self.assertCloseTo(w["rating"], 1208.01, 0.005)
        self.assertCloseTo(b["rating"], 1745.71, 0.005)
        self.assertCloseTo(w["deviation"], 59.9006, 0.00005)
        self.assertCloseTo(b["deviation"], 196.9873, 0.00005)
        self.assertCloseTo(w["volatility"], 0.053002, 0.000001)
        self.assertCloseTo(b["volatility"], 0.062006, 0.000001)


if __name__ == "__main__":
    unittest.main()
