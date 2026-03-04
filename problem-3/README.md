# Problem 3 — Music Note and Interval Arithmetic

Implement a music theory library handling notes, intervals, and scales.

## What Is Included

- `PROMPT.md`: the task prompt you give to an LLM.
- `test.py`: the validation suite (30+ tests, 80+ assertions).

## Usage

1. Give `PROMPT.md` to an LLM.
2. Save its generated implementation as `solution.py` in this directory.
3. Run `python3 -m unittest -v test.py` from this directory.

## Why This Is Hard

- Enharmonic spelling must be preserved (C + m3 = Eb, not D#).
- Octave boundaries at B/C require careful handling.
- Diminished unison (d1) and augmented octave (A8) are edge cases.
- Compound interval splitting and sequential application is error-prone.
- Double/triple accidentals interact with interval arithmetic.
- The complement roundtrip property tests every simple interval × multiple root notes.
