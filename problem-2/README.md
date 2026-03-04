# Problem 2 — Glicko-2 Rating Calculator

Implement the Glicko-2 rating system for two-player games.

## What Is Included

- `PROMPT.md`: the task prompt you give to an LLM.
- `test.py`: the validation suite (9 tests, 54+ numerical assertions with tight tolerances).

## Usage

1. Give `PROMPT.md` to an LLM.
2. Save its generated implementation as `solution.py` in this directory.
3. Run `python3 -m unittest -v test.py` from this directory.

## Why This Is Hard

- Multi-step iterative algorithm with convergence requirements.
- Tests verify ratings to ±0.005, deviations to ±0.00005, volatility to ±0.0000001.
- Floating-point errors compound across steps.
- Scale conversions between display and internal representations.

## Origin / Attribution

Test cases derived from [lichess-org/scalachess](https://github.com/lichess-org/scalachess)
(`test-kit/src/test/scala/rating/glicko/GlickoCalculatorTest.scala`).
