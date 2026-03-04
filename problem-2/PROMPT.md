Build a CIEDE2000 color difference calculator that passes all tests in `test.py`.

## Task

- Implement a `ciede2000` function in a single `solution.py` file.
- Given two colors in the CIELAB color space, compute their perceptual color
  difference using the CIEDE2000 formula.
- Each color is specified by three coordinates: L* (lightness, 0–100),
  a* (green–red axis), and b* (blue–yellow axis).

## Function Signature

```python
def ciede2000(L1, a1, b1, L2, a2, b2, kL=1.0, kC=1.0, kH=1.0):
    """
    Compute the CIEDE2000 color difference between two CIELAB colors.

    Args:
        L1, a1, b1: CIELAB values for the first color
        L2, a2, b2: CIELAB values for the second color
        kL, kC, kH: parametric weighting factors (default 1.0)

    Returns:
        float: the CIEDE2000 color difference (ΔE00)
    """
```

## Key Details

- The formula uses `25**7 = 6103515625` as a reference constant for chroma
  calculations.
- `kL`, `kC`, `kH` are parametric weighting factors, typically all 1.0.
- The result must match published reference values to ±0.0001.
- The formula involves converting between Cartesian (a*, b*) and polar (chroma,
  hue angle) representations.
- Special care is needed when:
  - One or both chroma values are zero (hue angle is undefined).
  - Hue angles cross the 0°/360° boundary (mean hue and hue difference
    calculations).
- The formula includes a rotation term that couples the chroma and hue difference
  contributions.

## Technical Constraints

- Language: Python 3.
- Only standard library imports (`math`, etc.) — no external packages.
- Deterministic behavior only.
- Do not hardcode expected test values.
- Do not modify `test.py`.

## Acceptance

Running `python3 -m unittest -v test.py` must pass.
