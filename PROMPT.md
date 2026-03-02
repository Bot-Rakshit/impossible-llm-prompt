Build a Python chess tactical puzzle motif recognizer that passes all tests in `test.py`.

Task:
- Implement code that satisfies the public interfaces and behavior expected by `test.py`.
- Preferred layout: a single `solution.py` file.
- Optional legacy layout: separate `cook.py` and `util.py` (and optionally `tagger.py`).
- Use rule-based tactical analysis over chess board states and move sequences.
- Parse puzzles from `{_id, fen, line|moves, cp}` documents.
- Expose a `read(doc)` function and a module-level `logger` if using `solution.py`.
- Provide motif detectors and utility logic for tactical patterns (forks, skewers, deflection, discovered attack, trapped pieces, pins, promotions, side attacks, etc.).
- Implement a top-level tag composer that combines motif detections into stable tag output.

Technical constraints:
- Language: Python 3.
- Library: `python-chess`.
- No network, no engines, no DB calls at runtime for tests.
- Deterministic behavior only.
- Do not hardcode puzzle IDs, FENs, or test case move strings.
- Do not modify `test.py`.

Acceptance:
- Running `python3 -m unittest -v test.py` must pass.
