# Problem 2 — CIEDE2000 Color Difference

Implement the CIEDE2000 perceptual color difference formula for CIELAB colors.

## What Is Included

- `PROMPT.md`: the task prompt you give to an LLM.
- `test.py`: the validation suite (12 tests, 34 reference pairs + property tests, ±0.0001 tolerance).

## Usage

1. Give `PROMPT.md` to an LLM.
2. Save its generated implementation as `solution.py` in this directory.
3. Run `python3 -m unittest -v test.py` from this directory.

## Why This Is Hard

- 22+ intermediate variables with intricate interdependencies.
- Hue angle edge cases when chroma is zero or near zero.
- Mean hue calculation across the 0°/360° boundary.
- Rotation term coupling chroma and hue contributions.
- Tests use published reference data with 4-decimal-place precision.
