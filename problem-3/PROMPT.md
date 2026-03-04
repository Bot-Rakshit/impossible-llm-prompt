Build a music theory library for notes, intervals, and scales that passes all tests
in `test.py`.

## Task

- Implement `Note`, `Interval`, and `Scale` classes in a single `solution.py` file.
- Handle note parsing, interval arithmetic, and scale construction with correct
  enharmonic spelling.

## Classes

### Note

```python
class Note:
    """
    A musical note parsed from a string like "C4", "F#3", "Bb5", "C##4", "Dbb2".

    Format: <letter><accidentals><octave>
      - letter: one of C, D, E, F, G, A, B
      - accidentals: up to 3 sharps (#) or flats (b), or empty
      - octave: single digit 0-9 (default 4 if omitted)

    Properties / methods:
      .midi        -> int   (MIDI number; C4 = 60, A4 = 69)
      .frequency() -> float (Hz; A4 = 440 Hz, equal temperament)
      .to_octave(n) -> Note (same letter and accidentals, different octave)
      .scientific_notation() -> str  (letter + accidentals + octave, e.g. "C#4")

    str(note) returns letter + accidentals (no octave), e.g. str(Note("C#4")) == "C#"

    Equality is based on spelling: Note("C#4") != Note("Db4") even though they
    sound the same.
    """
```

### Interval

```python
class Interval:
    """
    A musical interval parsed from a string like "P5", "m3", "A4", "d7", "M10".

    Format: <quality><number>
      - quality: P (perfect), M (major), m (minor), A (augmented), d (diminished)
      - number: positive integer (1-8 for simple intervals, >8 for compound)

    Properties / methods:
      .semitones       -> int
      .number          -> int
      .quality         -> str (single character)
      .is_compound()   -> bool (True if number > 8)
      .split()         -> list of Intervals (decompose compound into octaves + remainder)
      .complement()    -> Interval (inversion; only for simple intervals)

    str(interval) returns quality + number, e.g. str(Interval("P5")) == "P5"
    """
```

### Scale

```python
class Scale:
    """
    A musical scale built from a root note and scale type.

    Constructor: Scale(root, name) where root is a Note or note string,
                 name is one of the supported scale types.

    Properties / methods:
      .notes -> list of Note (scale degrees, each with octave set to 0)
      .root  -> Note
      .name  -> str
      [k]    -> Note (k-th degree, 0-indexed, wraps with octaves)
      [start:stop:step] -> list of Note
      len(scale) -> int (number of degrees)
      note in scale -> bool (checks if a Note belongs to the scale, ignoring octave)

    str(scale) returns "root name", e.g. "C major"
    """
```

## Operations

- **`Note + Interval -> Note`**: Transpose up. The result's letter name is determined
  by the interval number (e.g., any kind of fifth from A always lands on E).
  Accidentals adjust to produce the correct number of semitones. Compound intervals
  (number > 8) are applied by splitting into octaves + simple interval.

- **`Note - Interval -> Note`**: Transpose down. Equivalent to dropping one octave
  and adding the interval's complement.

- **`Note - Note -> Interval`**: Compute the ascending interval from the lower note
  to the higher note. The letter distance determines the interval number; the
  semitone distance determines the quality. Raises `ArithmeticError` if the second
  note is higher (descending interval). Raises `ValueError` for intervals outside
  the supported quality range (e.g., doubly augmented).

## Musical Constants

The chromatic scale has 12 semitones per octave. The natural (unmodified) notes
map to these semitone offsets from C:

| C | D | E | F | G | A | B |
|---|---|---|---|---|---|---|
| 0 | 2 | 4 | 5 | 7 | 9 | 11|

Each `#` adds 1 semitone; each `b` subtracts 1.

MIDI numbering: `midi = (octave + 1) * 12 + semitone_offset + accidental_adjustment`

Frequency: `freq = 440 * 2^((midi - 69) / 12)`

## Interval Semitone Table

| Interval | Semitones | | Interval | Semitones |
|----------|-----------|---|----------|-----------|
| d1       | -1        | | d5       | 6         |
| P1       | 0         | | P5       | 7         |
| A1       | 1         | | A5       | 8         |
| d2       | 0         | | d6       | 7         |
| m2       | 1         | | m6       | 8         |
| M2       | 2         | | M6       | 9         |
| A2       | 3         | | A6       | 10        |
| d3       | 2         | | d7       | 9         |
| m3       | 3         | | m7       | 10        |
| M3       | 4         | | M7       | 11        |
| A3       | 5         | | A7       | 12        |
| d4       | 4         | | d8       | 11        |
| P4       | 5         | | P8       | 12        |
| A4       | 6         | | A8       | 13        |

Perfect intervals (P): 1, 4, 5, 8. Major/minor intervals (M/m): 2, 3, 6, 7.

## Interval Complement

The complement (inversion) of an interval within one octave:
- number becomes `9 - number`
- quality flips: P↔P, M↔m, A↔d

Example: complement of M3 is m6, complement of P4 is P5.

## Compound Intervals

Intervals with number > 8 are compound. A compound interval splits into one or
more perfect octaves (P8) plus a simple remainder.

Example: M9 = P8 + M2, m17 = P8 + P8 + m3.

Semitones for a compound interval: add 12 for each octave removed, then look up
the simple remainder.

## Supported Scale Types

| Name              | Intervals from root                          |
|-------------------|----------------------------------------------|
| major             | P1, M2, M3, P4, P5, M6, M7                  |
| natural_minor     | P1, M2, m3, P4, P5, m6, m7                  |
| harmonic_minor    | P1, M2, m3, P4, P5, m6, M7                  |
| melodic_minor     | P1, M2, m3, P4, P5, M6, M7                  |
| major_pentatonic  | P1, M2, M3, P5, M6                           |
| minor_pentatonic  | P1, m3, P4, P5, m7                            |

## Technical Constraints

- Language: Python 3.
- Only standard library imports (`math`, `re`, etc.) — no external packages.
- Deterministic behavior only.
- Do not hardcode expected test values.
- Do not modify `test.py`.

## Acceptance

Running `python3 -m unittest -v test.py` must pass.
