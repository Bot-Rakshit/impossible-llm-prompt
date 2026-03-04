Build a Glicko-2 rating calculator for two-player games that passes all tests in `test.py`.

## Task

- Implement a `compute_game` function in a single `solution.py` file.
- Given two players' current ratings, compute their updated ratings after a game.
- Each player has three properties: a rating (skill estimate), a rating deviation
  (uncertainty in the rating), and a volatility (expected fluctuation).
- After a game, both players are updated independently — each treats the other as
  their sole opponent.

## Function Signature

```python
def compute_game(white, black, outcome, tau=0.75, skip_deviation_increase=False):
    """
    Compute new Glicko-2 ratings for both players after a single game.

    Args:
        white: dict with keys "rating", "deviation", "volatility"
        black: dict with keys "rating", "deviation", "volatility"
        outcome: str, one of "white" (white wins), "black" (black wins), "draw"
        tau: float, system constant controlling volatility change (default 0.75)
        skip_deviation_increase: bool, if True treat elapsed rating periods as 0;
                                  otherwise elapsed rating periods = 1 (default False)

    Returns:
        tuple of (white_result, black_result), each a dict with keys
        "rating", "deviation", "volatility"
    """
```

## Key Details

- The algorithm operates on an internal scale. Convert between the display scale and
  the internal scale using these constants:
  - `MULTIPLIER = 173.7178`
  - `DEFAULT_RATING = 1500.0`
- The volatility update uses an iterative root-finding procedure. Use a convergence
  tolerance of `0.000001` and a maximum of `1000` iterations.
- Game scores: win = 1.0, loss = 0.0, draw = 0.5 (from each player's perspective).

## Technical Constraints

- Language: Python 3.
- Only standard library imports (`math`, etc.) — no external packages.
- Deterministic behavior only.
- Do not hardcode expected test values or specific player ratings.
- Do not modify `test.py`.

## Acceptance

Running `python3 -m unittest -v test.py` must pass.
