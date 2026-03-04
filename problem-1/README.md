# Impossible LLM Prompt

This repository is a benchmark prompt + test harness for evaluating new LLMs on both:

- coding ability (implementing a non-trivial Python codebase from requirements), and
- chess tactical reasoning (detecting puzzle motifs from positions and move lines).

## What Is Included

- `PROMPT.md`: the task prompt you can give to an LLM.
- `test.py`: the validation suite used to score whether the generated implementation works.

The intended flow is:

1. Give `PROMPT.md` to an LLM.
2. Save its generated implementation (for example as `solution.py`) in this repo.
3. Run `python3 -m unittest -v test.py`.

## Origin / Attribution

This benchmark is derived from the tactical tagging logic and tests from the Lichess puzzler project:

- Original repository: [ornicar/lichess-puzzler](https://github.com/ornicar/lichess-puzzler)

This repo repackages the idea as a standalone LLM evaluation setup.
