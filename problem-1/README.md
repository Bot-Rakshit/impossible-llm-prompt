# Problem 1 — Cribbage Hand Scorer

Implement a cribbage hand scoring calculator.

## What Is Included

- `PROMPT.md`: the task prompt you give to an LLM.
- `test.py`: the validation suite (30+ tests, 70+ assertions).

## Usage

1. Give `PROMPT.md` to an LLM.
2. Save its generated implementation as `solution.py` in this directory.
3. Run `python3 -m unittest -v test.py` from this directory.

## Why This Is Hard

- Five interacting scoring categories that must all be correct.
- Fifteens require enumerating all 2^5 - 1 subsets and checking sums.
- Run detection must handle duplicate ranks correctly (multiply, don't double-count).
- Double-double runs, triple runs, and runs with gaps are common failure points.
- Crib vs non-crib flush rules differ subtly.
