import importlib
import math
import unittest


def _load_impl():
    try:
        mod = importlib.import_module("solution")
        return mod.ciede2000
    except ModuleNotFoundError as exc:
        if exc.name != "solution":
            raise
        raise ImportError(
            "No implementation found. Provide `solution.py` "
            "with a `ciede2000` function."
        ) from exc


ciede2000 = _load_impl()


# Sharma, Wu, Dalal (2005) — 34 reference color pairs
# Each tuple: (L*1, a*1, b*1, L*2, a*2, b*2, expected_dE00)
SHARMA_DATA = [
    (50.0000,   2.6772, -79.7751, 50.0000,   0.0000, -82.7485,  2.0425),
    (50.0000,   3.1571, -77.2803, 50.0000,   0.0000, -82.7485,  2.8615),
    (50.0000,   2.8361, -74.0200, 50.0000,   0.0000, -82.7485,  3.4412),
    (50.0000,  -1.3802, -84.2814, 50.0000,   0.0000, -82.7485,  1.0000),
    (50.0000,  -1.1848, -84.8006, 50.0000,   0.0000, -82.7485,  1.0000),
    (50.0000,  -0.9009, -85.5211, 50.0000,   0.0000, -82.7485,  1.0000),
    (50.0000,   0.0000,   0.0000, 50.0000,  -1.0000,   2.0000,  2.3669),
    (50.0000,  -1.0000,   2.0000, 50.0000,   0.0000,   0.0000,  2.3669),
    (50.0000,   2.4900,  -0.0010, 50.0000,  -2.4900,   0.0009,  7.1792),
    (50.0000,   2.4900,  -0.0010, 50.0000,  -2.4900,   0.0010,  7.1792),
    (50.0000,   2.4900,  -0.0010, 50.0000,  -2.4900,   0.0011,  7.2195),
    (50.0000,   2.4900,  -0.0010, 50.0000,  -2.4900,   0.0012,  7.2195),
    (50.0000,  -0.0010,   2.4900, 50.0000,   0.0009,  -2.4900,  4.8045),
    (50.0000,  -0.0010,   2.4900, 50.0000,   0.0010,  -2.4900,  4.8045),
    (50.0000,  -0.0010,   2.4900, 50.0000,   0.0011,  -2.4900,  4.7461),
    (50.0000,   2.5000,   0.0000, 50.0000,   0.0000,  -2.5000,  4.3065),
    (50.0000,   2.5000,   0.0000, 73.0000,  25.0000, -18.0000, 27.1492),
    (50.0000,   2.5000,   0.0000, 61.0000,  -5.0000,  29.0000, 22.8977),
    (50.0000,   2.5000,   0.0000, 56.0000, -27.0000,  -3.0000, 31.9030),
    (50.0000,   2.5000,   0.0000, 58.0000,  24.0000,  15.0000, 19.4535),
    (50.0000,   2.5000,   0.0000, 50.0000,   3.1736,   0.5854,  1.0000),
    (50.0000,   2.5000,   0.0000, 50.0000,   3.2972,   0.0000,  1.0000),
    (50.0000,   2.5000,   0.0000, 50.0000,   1.8634,   0.5757,  1.0000),
    (50.0000,   2.5000,   0.0000, 50.0000,   3.2592,   0.3350,  1.0000),
    (60.2574, -34.0099,  36.2677, 60.4626, -34.1751,  39.4387,  1.2644),
    (63.0109, -31.0961,  -5.8663, 62.8187, -29.7946,  -4.0864,  1.2630),
    (61.2901,   3.7196,  -5.3901, 61.4292,   2.2480,  -4.9620,  1.8731),
    (35.0831, -44.1164,   3.7933, 35.0232, -40.0716,   1.5901,  1.8645),
    (22.7233,  20.0904, -46.6940, 23.0331,  14.9730, -42.5619,  2.0373),
    (36.4612,  47.8580,  18.3852, 36.2715,  50.5065,  21.2231,  1.4146),
    (90.8027,  -2.0831,   1.4410, 91.1528,  -1.6435,   0.0447,  1.4441),
    (90.9257,  -0.5406,  -0.9208, 88.6381,  -0.8985,  -0.7239,  1.5381),
    ( 6.7747,  -0.2908,  -2.4247,  5.8714,  -0.0985,  -2.2286,  0.6377),
    ( 2.0776,   0.0795,  -1.1350,  0.9033,  -0.0636,  -0.5514,  0.9082),
]


class TestCIEDE2000(unittest.TestCase):
    """
    Tests for CIEDE2000 color difference (ΔE00).

    Reference data from Sharma, Wu, Dalal (2005):
    "The CIEDE2000 Color-Difference Formula: Implementation Notes,
     Supplementary Test Data, and Mathematical Observations"

    ciede2000(L1, a1, b1, L2, a2, b2, kL=1.0, kC=1.0, kH=1.0) -> float
    """

    TOLERANCE = 0.0001

    # ── Sharma 2005 reference pairs ──────────────────────────────────────

    def test_sharma_pairs_1_to_6(self):
        """Near-blue hue region. Pairs 4-6 should give dE = 1.0 exactly."""
        for i in range(6):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )

    def test_sharma_pairs_7_8_symmetry(self):
        """Swapping color 1 and color 2 gives the same result."""
        for i in (6, 7):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )
        # explicit symmetry check
        d1 = SHARMA_DATA[6]
        d2 = SHARMA_DATA[7]
        r1 = ciede2000(d1[0], d1[1], d1[2], d1[3], d1[4], d1[5])
        r2 = ciede2000(d2[0], d2[1], d2[2], d2[3], d2[4], d2[5])
        self.assertAlmostEqual(r1, r2, places=10,
                               msg="Symmetry: swapping colors must give same ΔE")

    def test_sharma_pairs_9_to_12(self):
        """Near-axis hue edge cases with very small b* values."""
        for i in range(8, 12):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )

    def test_sharma_pairs_13_to_16(self):
        """Near-axis hue edge cases with very small a* values."""
        for i in range(12, 16):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )

    def test_sharma_pairs_17_to_20(self):
        """Large color differences spanning different regions."""
        for i in range(16, 20):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )

    def test_sharma_pairs_21_to_24(self):
        """Unit chroma/hue differences — all should give dE = 1.0."""
        for i in range(20, 24):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )

    def test_sharma_pairs_25_to_34(self):
        """Real-world color pairs from various regions of color space."""
        for i in range(24, 34):
            L1, a1, b1, L2, a2, b2, expected = SHARMA_DATA[i]
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertAlmostEqual(
                result, expected, delta=self.TOLERANCE,
                msg=f"Pair {i+1}: expected {expected}, got {result}"
            )

    # ── Identity and symmetry properties ─────────────────────────────────

    def test_identity(self):
        """A color compared with itself should give ΔE = 0."""
        test_colors = [
            (50.0, 0.0, 0.0),
            (50.0, 2.5, 0.0),
            (90.0, -2.0, 1.4),
            (0.0, 0.0, 0.0),
            (100.0, 0.0, 0.0),
        ]
        for L, a, b in test_colors:
            result = ciede2000(L, a, b, L, a, b)
            self.assertAlmostEqual(
                result, 0.0, places=10,
                msg=f"Identity failed for ({L}, {a}, {b}): got {result}"
            )

    def test_symmetry_property(self):
        """ΔE(a, b) must equal ΔE(b, a) for arbitrary color pairs."""
        pairs = [
            (50.0, 2.5, 0.0, 73.0, 25.0, -18.0),
            (60.2574, -34.0099, 36.2677, 60.4626, -34.1751, 39.4387),
            (22.7233, 20.0904, -46.6940, 23.0331, 14.9730, -42.5619),
            (2.0776, 0.0795, -1.1350, 0.9033, -0.0636, -0.5514),
        ]
        for L1, a1, b1, L2, a2, b2 in pairs:
            d_forward = ciede2000(L1, a1, b1, L2, a2, b2)
            d_reverse = ciede2000(L2, a2, b2, L1, a1, b1)
            self.assertAlmostEqual(
                d_forward, d_reverse, places=10,
                msg=f"Symmetry failed for ({L1},{a1},{b1}) <-> ({L2},{a2},{b2})"
            )

    def test_non_negative(self):
        """ΔE must always be non-negative."""
        for data in SHARMA_DATA:
            L1, a1, b1, L2, a2, b2, _ = data
            result = ciede2000(L1, a1, b1, L2, a2, b2)
            self.assertGreaterEqual(result, 0.0)

    # ── Zero chroma edge cases ───────────────────────────────────────────

    def test_both_achromatic(self):
        """Both colors on the L* axis (a*=0, b*=0) — pure lightness difference."""
        result = ciede2000(50.0, 0.0, 0.0, 60.0, 0.0, 0.0)
        self.assertGreater(result, 0.0)
        # Reverse should be the same
        result2 = ciede2000(60.0, 0.0, 0.0, 50.0, 0.0, 0.0)
        self.assertAlmostEqual(result, result2, places=10)

    def test_one_achromatic(self):
        """One color is achromatic — the pair 7 case from Sharma."""
        result = ciede2000(50.0, 0.0, 0.0, 50.0, -1.0, 2.0)
        self.assertAlmostEqual(result, 2.3669, delta=self.TOLERANCE)


if __name__ == "__main__":
    unittest.main()
