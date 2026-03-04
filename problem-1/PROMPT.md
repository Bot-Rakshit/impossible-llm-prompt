Build a cribbage hand scoring calculator that passes all tests in `test.py`.

## Task

- Implement a `score_hand` function in a single `solution.py` file.
- Given a 4-card hand and a starter (cut) card, compute the score breakdown
  across all five scoring categories.

## Function Signature

```python
def score_hand(hand, starter, is_crib=False):
    """
    Score a cribbage hand.

    Args:
        hand: list of 4 card strings
        starter: single card string
        is_crib: bool, if True use crib flush rules (default False)

    Returns:
        dict with keys:
            "fifteens": int (points from combinations summing to 15)
            "pairs": int (points from matching ranks)
            "runs": int (points from consecutive rank sequences)
            "flush": int (points from matching suits)
            "nobs": int (points from Jack of starter's suit)
            "total": int (sum of all above)
    """
```

## Card Format

Each card is a 2-character string: `<rank><suit>`.

- **Ranks**: `A` (Ace), `2`–`9`, `T` (10), `J` (Jack), `Q` (Queen), `K` (King)
- **Suits**: `H` (Hearts), `D` (Diamonds), `C` (Clubs), `S` (Spades)

Examples: `"5H"` (5 of Hearts), `"TC"` (10 of Clubs), `"JD"` (Jack of Diamonds)

## Scoring Rules

All five cards (4 hand + 1 starter) are used for scoring fifteens, pairs, and runs.
Flush and nobs have special rules as noted below.

### 1. Fifteens (2 points each)

Every distinct subset of the 5 cards whose **values** sum to exactly 15 scores
2 points. Card values for this purpose:

| Rank  | Value |
|-------|-------|
| A     | 1     |
| 2–9   | Face value |
| T,J,Q,K | 10  |

All subset sizes (2, 3, 4, or 5 cards) are checked.

### 2. Pairs (2 points each)

Every distinct pair of cards with the **same rank** scores 2 points.
- One pair = 2 points
- Three of a kind = 3 pairs = 6 points
- Four of a kind = 6 pairs = 12 points

### 3. Runs (1 point per card per run)

A run is a sequence of 3 or more cards with **consecutive ranks**. Only the longest
maximal consecutive sequence counts — shorter sub-sequences within a longer run do
not score separately.

The rank order for runs is: A(1), 2, 3, 4, 5, 6, 7, 8, 9, T(10), J(11), Q(12),
K(13). Ace is always low. There is no wrapping (Q-K-A is not a run).

**Duplicate cards multiply runs:**
- If a run of length L contains ranks where some appear multiple times, the
  number of distinct runs equals L × product(frequency of each rank in the run).
- Example: ranks [3, 3, 4, 5] → run 3-4-5 (length 3), rank 3 appears 2×,
  so 2 distinct runs of 3 = 6 points.
- Example: ranks [3, 3, 4, 4, 5] → run 3-4-5 (length 3), ranks 3 and 4 each
  appear 2×, so 2 × 2 = 4 distinct runs of 3 = 12 points.

### 4. Flush

- If all **4 hand cards** share the same suit: 4 points.
- If the starter also matches: 5 points instead.
- If `is_crib=True`: flush only counts if all 5 cards (hand + starter) share the
  same suit (5 points). A 4-card flush does not count in the crib.

### 5. Nobs (1 point)

If the hand contains a **Jack of the same suit as the starter card**: 1 point.

## Technical Constraints

- Language: Python 3.
- Only standard library imports (`itertools`, etc.) — no external packages.
- Deterministic behavior only.
- Do not hardcode expected test values.
- Do not modify `test.py`.

## Acceptance

Running `python3 -m unittest -v test.py` must pass.
