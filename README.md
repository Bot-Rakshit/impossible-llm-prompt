# Impossible LLM Prompt

A collection of benchmark prompts + test harnesses for evaluating LLMs on coding tasks
with verifiable test cases.

## Problems

| # | Challenge | Tests | Difficulty |
|---|-----------|-------|------------|
| 1 | [Chess Tactical Motif Recognizer](problem-1/) | 80+ assertions | Hard — chess domain reasoning |
| 2 | [Glicko-2 Rating Calculator](problem-2/) | 54+ assertions | Hard — numerical precision |

## How It Works

Each `problem-N/` folder contains:

- `PROMPT.md` — give this to an LLM.
- `test.py` — the validation suite.

The flow:

1. Give `PROMPT.md` to an LLM.
2. Save its output as `solution.py` in the same folder.
3. Run `python3 -m unittest -v test.py` from that folder.
