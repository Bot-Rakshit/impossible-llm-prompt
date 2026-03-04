import importlib
import unittest


def _load_impl():
    try:
        mod = importlib.import_module("solution")
        return mod.score_hand
    except ModuleNotFoundError as exc:
        if exc.name != "solution":
            raise
        raise ImportError(
            "No implementation found. Provide `solution.py` "
            "with a `score_hand` function."
        ) from exc


score_hand = _load_impl()


class TestCribbageScoring(unittest.TestCase):
    """
    Tests for a cribbage hand scoring calculator.

    score_hand(hand, starter, is_crib=False) -> dict

    Parameters:
        hand: list of 4 card strings (e.g., ["5H", "5D", "5S", "JC"])
        starter: single card string (e.g., "5C")
        is_crib: bool (default False)

    Returns:
        dict with keys "fifteens", "pairs", "runs", "flush", "nobs", "total"
    """

    # ── Maximum and minimum hands ────────────────────────────────────────

    def test_perfect_29(self):
        """The maximum possible cribbage hand: 5-5-5-J + 5 starter."""
        r = score_hand(["5H", "5D", "5S", "JC"], "5C")
        self.assertEqual(r["fifteens"], 16)
        self.assertEqual(r["pairs"], 12)
        self.assertEqual(r["runs"], 0)
        self.assertEqual(r["flush"], 0)
        self.assertEqual(r["nobs"], 1)
        self.assertEqual(r["total"], 29)

    def test_zero_hand(self):
        """A hand worth zero points."""
        r = score_hand(["2H", "4D", "6S", "8C"], "TH")
        self.assertEqual(r["fifteens"], 0)
        self.assertEqual(r["pairs"], 0)
        self.assertEqual(r["runs"], 0)
        self.assertEqual(r["flush"], 0)
        self.assertEqual(r["nobs"], 0)
        self.assertEqual(r["total"], 0)

    def test_24_hand(self):
        """A 24-point hand: double-double run of 4 with many fifteens."""
        r = score_hand(["7H", "7D", "8S", "8C"], "9H")
        self.assertEqual(r["fifteens"], 8)
        self.assertEqual(r["pairs"], 4)
        self.assertEqual(r["runs"], 12)
        self.assertEqual(r["total"], 24)

    # ── Fifteens ─────────────────────────────────────────────────────────

    def test_fifteens_single(self):
        """One fifteen: 5 + face card."""
        r = score_hand(["5H", "KD", "2S", "4C"], "9D")
        # 5+K=15, 2+4+9=15, 5+4+? No: 5+2+4+? = 11+9=20
        # Actually: 5+K=15(1), 2+4+9=15(1), 5+4+? None. Total: 2 fifteens = 4
        self.assertEqual(r["fifteens"], 4)

    def test_fifteens_three_fives_and_face(self):
        """Three 5s and a face card — many fifteen combos."""
        r = score_hand(["5H", "5D", "5S", "KH"], "2C")
        # 5+K=15 (×3), 5+5+5=15 (×1), 5+5+5+? nope
        # Wait: also need to check 5+5+2=12, K+2=12, K+5=15(×3)
        # K+5H=15, K+5D=15, K+5S=15 → 3 fifteens
        # 5H+5D+5S=15 → 1 fifteen
        # Any others? 5+5+2=12, K+2=12, 5+2=7, 5+5=10
        # 5H+5D+2=12, 5+K+2=17, 5+5+K=20, 5+5+5+2=17, 5+5+5+K=25, 5+5+K+2=22
        # All 5: 5+5+5+K+2=27
        # Total: 4 fifteens = 8
        self.assertEqual(r["fifteens"], 8)

    def test_fifteens_multiple_face_cards(self):
        """K-Q-T-5-5: each face card pairs with each 5."""
        r = score_hand(["KH", "QD", "TS", "5C"], "5H")
        # K+5C=15, K+5H=15, Q+5C=15, Q+5H=15, T+5C=15, T+5H=15 → 6 fifteens
        self.assertEqual(r["fifteens"], 12)
        self.assertEqual(r["pairs"], 2)  # pair of 5s
        self.assertEqual(r["total"], 14)

    def test_fifteens_five_card_subset(self):
        """A fifteen formed by all 5 cards."""
        r = score_hand(["AH", "2D", "3S", "4C"], "5H")
        # A+2+3+4+5=15 → 1 fifteen = 2 pts
        self.assertEqual(r["fifteens"], 2)
        self.assertEqual(r["runs"], 5)  # A-2-3-4-5

    # ── Pairs ────────────────────────────────────────────────────────────

    def test_one_pair(self):
        r = score_hand(["5H", "5D", "2S", "8C"], "KH")
        self.assertEqual(r["pairs"], 2)

    def test_two_pairs(self):
        r = score_hand(["3H", "3D", "9S", "9C"], "KH")
        self.assertEqual(r["pairs"], 4)

    def test_three_of_a_kind(self):
        """Three of a kind = pair royal = 3 pairs = 6 points."""
        r = score_hand(["AH", "AD", "AC", "2S"], "8H")
        self.assertEqual(r["pairs"], 6)

    def test_four_of_a_kind(self):
        """Four of a kind = double pair royal = 6 pairs = 12 points."""
        r = score_hand(["5H", "5D", "5S", "5C"], "KH")
        self.assertEqual(r["pairs"], 12)
        # Also: each 5+K=15 (×4), 5+5+5=15 (×4 choose 3 = 4) → 8 fifteens = 16
        self.assertEqual(r["fifteens"], 16)
        self.assertEqual(r["total"], 28)

    # ── Runs ─────────────────────────────────────────────────────────────

    def test_run_of_three(self):
        r = score_hand(["JH", "QD", "KS", "AC"], "2H")
        # J-Q-K = run of 3
        self.assertEqual(r["runs"], 3)

    def test_run_of_four(self):
        r = score_hand(["3H", "4D", "5S", "6C"], "TH")
        # 3-4-5-6 = run of 4
        self.assertEqual(r["runs"], 4)

    def test_run_of_five(self):
        r = score_hand(["6H", "7D", "8S", "9C"], "TH")
        self.assertEqual(r["runs"], 5)
        self.assertEqual(r["fifteens"], 4)  # 6+9=15, 7+8=15

    def test_double_run_of_three(self):
        """Duplicate rank in a 3-card run → 2 runs of 3."""
        r = score_hand(["3H", "3D", "4S", "5C"], "8H")
        self.assertEqual(r["runs"], 6)
        self.assertEqual(r["pairs"], 2)

    def test_double_run_of_four(self):
        """Duplicate rank in a 4-card run → 2 runs of 4."""
        r = score_hand(["3H", "3D", "4S", "5C"], "6H")
        self.assertEqual(r["runs"], 8)
        self.assertEqual(r["pairs"], 2)

    def test_triple_run(self):
        """Three of a kind in a 3-card run → 3 runs of 3."""
        r = score_hand(["AH", "AD", "AC", "2S"], "3H")
        self.assertEqual(r["runs"], 9)
        self.assertEqual(r["pairs"], 6)

    def test_double_double_run(self):
        """Two pairs in a 3-card run → 4 runs of 3."""
        r = score_hand(["3H", "3D", "4S", "4C"], "5H")
        self.assertEqual(r["runs"], 12)
        self.assertEqual(r["pairs"], 4)

    def test_no_run_two_consecutive(self):
        """Only two consecutive ranks — not enough for a run."""
        r = score_hand(["2H", "3D", "7S", "9C"], "KH")
        self.assertEqual(r["runs"], 0)

    def test_run_with_gap(self):
        """Non-adjacent sequences: only the long one scores."""
        r = score_hand(["2H", "3D", "5S", "6C"], "7H")
        # 2-3 (len 2, no score), 5-6-7 (len 3, scores)
        self.assertEqual(r["runs"], 3)

    def test_run_with_duplicate_at_end(self):
        """Duplicate at the end of a run: 3-4-5-5 → 2 runs of 3."""
        r = score_hand(["3H", "4D", "5S", "5C"], "8H")
        self.assertEqual(r["runs"], 6)
        self.assertEqual(r["pairs"], 2)

    # ── Flush ────────────────────────────────────────────────────────────

    def test_flush_four(self):
        """4-card flush (hand only, starter different suit)."""
        r = score_hand(["4H", "7H", "TH", "QH"], "2D")
        self.assertEqual(r["flush"], 4)

    def test_flush_five(self):
        """5-card flush (hand + starter same suit)."""
        r = score_hand(["4H", "7H", "TH", "QH"], "2H")
        self.assertEqual(r["flush"], 5)

    def test_no_flush(self):
        """Mixed suits — no flush."""
        r = score_hand(["4H", "7D", "TS", "QC"], "2H")
        self.assertEqual(r["flush"], 0)

    def test_three_same_suit_no_flush(self):
        """Only 3 of 4 hand cards same suit — no flush."""
        r = score_hand(["4H", "7H", "TH", "QD"], "2H")
        self.assertEqual(r["flush"], 0)

    def test_crib_flush_requires_all_five(self):
        """In crib, 4-card flush doesn't count."""
        r = score_hand(["4H", "7H", "TH", "QH"], "2D", is_crib=True)
        self.assertEqual(r["flush"], 0)

    def test_crib_flush_all_five(self):
        """In crib, all 5 same suit → 5 points."""
        r = score_hand(["4H", "7H", "TH", "QH"], "2H", is_crib=True)
        self.assertEqual(r["flush"], 5)

    # ── Nobs ─────────────────────────────────────────────────────────────

    def test_nobs(self):
        """Jack in hand matching starter's suit."""
        r = score_hand(["JH", "2D", "3S", "4C"], "5H")
        self.assertEqual(r["nobs"], 1)

    def test_no_nobs_wrong_suit(self):
        """Jack in hand but different suit from starter."""
        r = score_hand(["JH", "2D", "3S", "4C"], "5D")
        self.assertEqual(r["nobs"], 0)

    def test_no_nobs_no_jack(self):
        """No Jack in hand at all."""
        r = score_hand(["AH", "2D", "3S", "4C"], "5H")
        self.assertEqual(r["nobs"], 0)

    def test_nobs_starter_jack_doesnt_count(self):
        """The starter being a Jack does not give nobs (nobs is only for hand Jacks)."""
        r = score_hand(["AH", "2D", "3S", "4C"], "JH")
        self.assertEqual(r["nobs"], 0)

    # ── Combined scoring ─────────────────────────────────────────────────

    def test_combined_run_flush_nobs_fifteens(self):
        """A hand with multiple scoring types."""
        r = score_hand(["JH", "QH", "KH", "AH"], "TH")
        # Run: T-J-Q-K (4) — but A is rank 1, not adjacent to T(10)
        # Wait: A(1), T(10), J(11), Q(12), K(13) → T-J-Q-K is run of 4
        self.assertEqual(r["runs"], 4)
        self.assertEqual(r["flush"], 5)  # All hearts
        self.assertEqual(r["nobs"], 1)   # JH is Jack of Hearts, starter TH is Hearts
        self.assertEqual(r["fifteens"], 0)
        self.assertEqual(r["total"], 10)  # 4 + 5 + 1

    def test_combined_pair_and_fifteen(self):
        """Pair of 5s with face cards."""
        r = score_hand(["5H", "5D", "TH", "2C"], "3S")
        # Fifteens: 5H+TH=15, 5D+TH=15, TH+2C+3S=15, 5H+5D+2C+3S=15 → 4×2 = 8
        self.assertEqual(r["fifteens"], 8)
        self.assertEqual(r["pairs"], 2)
        self.assertEqual(r["runs"], 0)  # 2,3 only 2 consecutive
        self.assertEqual(r["total"], 10)

    def test_all_same_value(self):
        """Four Kings + a 5: lots of fifteens."""
        r = score_hand(["KH", "KD", "KS", "KC"], "5H")
        # Fifteens: K+5=15 (×4) → 8 pts
        self.assertEqual(r["fifteens"], 8)
        # Pairs: C(4,2)=6 pairs → 12 pts
        self.assertEqual(r["pairs"], 12)
        self.assertEqual(r["total"], 20)

    def test_eight_point_hand(self):
        """4-5-6 run with pair of 6s and a fifteen."""
        r = score_hand(["4H", "5D", "6S", "6C"], "KH")
        # Runs: 4-5-6 (len 3), 6 appears 2× → 2 × 3 = 6
        self.assertEqual(r["runs"], 6)
        # Pairs: 6-6 = 2
        self.assertEqual(r["pairs"], 2)
        # Fifteens: 5+K=15 (1), 4+5+6=15 (×2 for each 6) = 2
        # Total fifteens: 3 × 2 = 6
        self.assertEqual(r["fifteens"], 6)
        self.assertEqual(r["total"], 14)

    def test_ace_low_only(self):
        """Ace is always low — Q-K-A is NOT a run."""
        r = score_hand(["QH", "KD", "AS", "7C"], "2H")
        self.assertEqual(r["runs"], 0)

    def test_all_aces(self):
        """Four aces + a card."""
        r = score_hand(["AH", "AD", "AS", "AC"], "KH")
        # Pairs: C(4,2)=6 → 12
        self.assertEqual(r["pairs"], 12)
        # Fifteens: A+A+A+A+K = 4+10 = 14. None sum to 15.
        # A+K=11, A+A+K=12, A+A+A+K=13, A+A+A+A+K=14
        self.assertEqual(r["fifteens"], 0)
        self.assertEqual(r["total"], 12)


if __name__ == "__main__":
    unittest.main()
