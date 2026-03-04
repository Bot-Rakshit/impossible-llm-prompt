# Impossible LLM Prompt

A collection of benchmark prompts + test harnesses for evaluating LLMs on coding tasks
with verifiable test cases.

## Problems

| # | Challenge | Tests | Difficulty |
|---|-----------|-------|------------|
| 1 | [Cribbage Hand Scorer](problem-1/) | 37 tests, 70+ assertions | Hard — combinatorial scoring + run detection |
| 2 | [CIEDE2000 Color Difference](problem-2/) | 12 tests, 34 reference pairs | Hard — numerical precision + edge cases |
| 3 | [Music Note & Interval Arithmetic](problem-3/) | 43 tests, 80+ assertions | Hard — enharmonic spelling + domain rules |

## How It Works

Each `problem-N/` folder contains:

- `PROMPT.md` — give this to an LLM.
- `test.py` — the validation suite.

The flow:

1. Give `PROMPT.md` to an LLM.
2. Save its output as `solution.py` in the same folder.
3. Run `python3 -m unittest -v test.py` from that folder.

## Reference Solutions

Reference solutions are available on the `solution` branch.
