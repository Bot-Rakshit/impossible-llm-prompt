import importlib
import unittest


def _load_impl():
    try:
        mod = importlib.import_module("solution")
        return mod.Note, mod.Interval, mod.Scale
    except ModuleNotFoundError as exc:
        if exc.name != "solution":
            raise
        raise ImportError(
            "No implementation found. Provide `solution.py` "
            "with Note, Interval, and Scale classes."
        ) from exc


Note, Interval, Scale = _load_impl()


class TestNote(unittest.TestCase):
    """Tests for the Note class."""

    def test_parse_basic(self):
        self.assertEqual(str(Note("A4")), "A")
        self.assertEqual(str(Note("Ab6")), "Ab")
        self.assertEqual(str(Note("Dbb")), "Dbb")

    def test_parse_triple_sharp(self):
        self.assertEqual(str(Note("G###0")), "G###")

    def test_parse_invalid(self):
        self.assertRaises(Exception, Note, "A99")
        self.assertRaises(Exception, Note, "Ab#")
        self.assertRaises(Exception, Note, "E####")

    def test_default_octave(self):
        """Omitting octave defaults to 4."""
        self.assertEqual(Note("C").scientific_notation(), "C4")
        self.assertEqual(Note("F#").scientific_notation(), "F#4")

    def test_scientific_notation(self):
        self.assertEqual(Note("C#4").scientific_notation(), "C#4")
        self.assertEqual(Note("Bb3").scientific_notation(), "Bb3")

    def test_midi(self):
        self.assertEqual(Note("C4").midi, 60)
        self.assertEqual(Note("D5").midi, 74)
        self.assertEqual(Note("A4").midi, 69)
        self.assertEqual(Note("B3").midi, 59)
        self.assertEqual(Note("C#4").midi, 61)

    def test_midi_enharmonic(self):
        """Enharmonic notes have the same MIDI number."""
        self.assertEqual(Note("C#4").midi, Note("Db4").midi)
        self.assertEqual(Note("E4").midi, Note("Fb4").midi)
        self.assertEqual(Note("B#3").midi, Note("C4").midi)

    def test_frequency(self):
        self.assertAlmostEqual(Note("A4").frequency(), 440.0, places=1)
        self.assertAlmostEqual(Note("A5").frequency(), 880.0, places=1)
        self.assertAlmostEqual(Note("C5").frequency(), 523.3, places=1)

    def test_equality_by_spelling(self):
        """Equality is based on spelling, not pitch."""
        self.assertEqual(Note("C#4"), Note("C#4"))
        self.assertNotEqual(Note("C#4"), Note("Db4"))
        self.assertNotEqual(Note("C4"), Note("C5"))

    def test_to_octave(self):
        self.assertEqual(Note("C#2").to_octave(5), Note("C#5"))
        self.assertEqual(Note("B#6").to_octave(3), Note("B#3"))
        self.assertEqual(Note("Ebb5").to_octave(1), Note("Ebb1"))


class TestInterval(unittest.TestCase):
    """Tests for the Interval class."""

    def test_parse_basic(self):
        self.assertEqual(Interval("d5").semitones, 6)
        self.assertEqual(Interval("P8").semitones, 12)
        self.assertEqual(Interval("A8").semitones, 13)
        self.assertEqual(Interval("P1").semitones, 0)
        self.assertEqual(Interval("m2").semitones, 1)
        self.assertEqual(Interval("M3").semitones, 4)

    def test_parse_invalid(self):
        """P3 is invalid (3 is not a perfect interval)."""
        self.assertRaises(Exception, Interval, "P3")

    def test_compound(self):
        self.assertTrue(Interval("M9").is_compound())
        self.assertFalse(Interval("P8").is_compound())
        self.assertEqual(Interval("M9").semitones, 14)
        self.assertEqual(Interval("m10").semitones, 15)
        self.assertEqual(Interval("P15").semitones, 24)

    def test_complement_complete(self):
        """Every simple interval and its complement."""
        pairs = [
            ("P1", "P8"), ("A1", "d8"),
            ("d2", "A7"), ("m2", "M7"), ("M2", "m7"), ("A2", "d7"),
            ("d3", "A6"), ("m3", "M6"), ("M3", "m6"), ("A3", "d6"),
            ("d4", "A5"), ("P4", "P5"), ("A4", "d5"),
            ("d5", "A4"), ("P5", "P4"), ("A5", "d4"),
            ("d6", "A3"), ("m6", "M3"), ("M6", "m3"), ("A6", "d3"),
            ("d7", "A2"), ("m7", "M2"), ("M7", "m2"), ("A7", "d2"),
            ("d8", "A1"), ("P8", "P1"), ("A8", "d1"),
        ]
        for i_str, c_str in pairs:
            i = Interval(i_str)
            c = Interval(c_str)
            self.assertEqual(
                str(i.complement()), str(c),
                msg=f"complement of {i_str} should be {c_str}"
            )

    def test_complement_roundtrip(self):
        """For every note and interval, note + i + complement(i) = note one octave up."""
        simple_intervals = [
            "P1", "m2", "M2", "m3", "M3", "P4", "A4",
            "d5", "P5", "m6", "M6", "m7", "M7", "P8",
        ]
        for note_str in ("C4", "D4", "F#4", "Bb3"):
            n = Note(note_str)
            for i_str in simple_intervals:
                i = Interval(i_str)
                result = n + i + i.complement()
                expected_oct = n.to_octave(n.octave + 1)
                self.assertEqual(
                    result, expected_oct,
                    msg=f"{note_str} + {i_str} + comp = {result.scientific_notation()}, "
                        f"expected {expected_oct.scientific_notation()}"
                )

    def test_complement_compound_raises(self):
        self.assertRaises(ValueError, Interval("M9").complement)
        self.assertRaises(ValueError, Interval("M10").complement)

    def test_split(self):
        self.assertEqual(
            [str(i) for i in Interval("M9").split()], ["P8", "M2"]
        )
        self.assertEqual(
            [str(i) for i in Interval("m17").split()], ["P8", "P8", "m3"]
        )
        self.assertEqual(
            [str(i) for i in Interval("P29").split()], ["P8", "P8", "P8", "P8"]
        )

    def test_str(self):
        self.assertEqual(str(Interval("P5")), "P5")
        self.assertEqual(str(Interval("m3")), "m3")
        self.assertEqual(str(Interval("M10")), "M10")


class TestTranspose(unittest.TestCase):
    """Tests for Note + Interval (transpose up)."""

    def test_basic_transpositions(self):
        cases = [
            ("A4", "d5", "Eb5"),
            ("A4", "P1", "A4"),
            ("G##4", "m3", "B#4"),
            ("F3", "P5", "C4"),
            ("B#4", "d2", "C5"),
        ]
        for note_str, interval_str, expected_str in cases:
            result = Note(note_str) + Interval(interval_str)
            self.assertEqual(
                result.scientific_notation(), expected_str,
                msg=f"{note_str} + {interval_str} = {result.scientific_notation()}, "
                    f"expected {expected_str}"
            )

    def test_diminished_unison(self):
        """Diminished unison lowers the note by one accidental."""
        self.assertEqual(
            (Note("C4") + Interval("d1")).scientific_notation(), "Cb4"
        )
        self.assertEqual(
            (Note("B4") + Interval("d1")).scientific_notation(), "Bb4"
        )
        self.assertEqual(
            (Note("C#4") + Interval("d1")).scientific_notation(), "C4"
        )

    def test_compound_intervals(self):
        cases = [
            ("C4", "M10", "E5"),
            ("Cb4", "A10", "E5"),
            ("Cb4", "m10", "Ebb5"),
            ("B3", "m10", "D5"),
            ("B3", "M17", "D#6"),
        ]
        for note_str, interval_str, expected_str in cases:
            result = Note(note_str) + Interval(interval_str)
            self.assertEqual(
                result.scientific_notation(), expected_str,
                msg=f"{note_str} + {interval_str} = {result.scientific_notation()}, "
                    f"expected {expected_str}"
            )

    def test_transpose_type_error(self):
        self.assertRaises(TypeError, lambda: Note("C4") + "P5")
        self.assertRaises(TypeError, lambda: Note("C4") + 5)


class TestSubtractNotes(unittest.TestCase):
    """Tests for Note - Note (find interval)."""

    def test_basic_intervals(self):
        self.assertEqual(str(Note("E4") - Note("C4")), "M3")
        self.assertEqual(str(Note("G4") - Note("C4")), "P5")
        self.assertEqual(str(Note("C#4") - Note("C4")), "A1")
        self.assertEqual(str(Note("Cb4") - Note("C4")), "d1")

    def test_descending_raises(self):
        """Subtracting a higher note raises ArithmeticError."""
        self.assertRaises(ArithmeticError, lambda: Note("C4") - Note("C5"))

    def test_unsupported_interval_raises(self):
        """Intervals outside the supported quality range raise ValueError."""
        self.assertRaises(ValueError, lambda: Note("A#4") - Note("Gb4"))

    def test_roundtrip_add_sub(self):
        """(note + interval) - interval = note, (note + interval) - note = interval."""
        cases = [
            ("A4", "d5", "Eb5"),
            ("A4", "P1", "A4"),
            ("G##4", "m3", "B#4"),
            ("F3", "P5", "C4"),
        ]
        for note_str, interval_str, result_str in cases:
            n = Note(note_str)
            i = Interval(interval_str)
            r = Note(result_str)
            self.assertEqual(r - i, n)
            self.assertEqual(r - n, i)


class TestSubtractInterval(unittest.TestCase):
    """Tests for Note - Interval (transpose down)."""

    def test_basic_subtraction(self):
        """Transposing down should be the inverse of transposing up."""
        self.assertEqual(
            (Note("G4") - Interval("P5")).scientific_notation(), "C4"
        )
        self.assertEqual(
            (Note("E5") - Interval("M10")).scientific_notation(), "C4"
        )

    def test_compound_subtraction(self):
        self.assertEqual(
            (Note("D#6") - Interval("M17")).scientific_notation(), "B3"
        )


class TestScale(unittest.TestCase):
    """Tests for the Scale class."""

    def test_major_scale(self):
        self.assertEqual(
            list(map(str, Scale("C4", "major").notes)),
            ["C", "D", "E", "F", "G", "A", "B"],
        )

    def test_natural_minor(self):
        self.assertEqual(
            list(map(str, Scale("C4", "natural_minor").notes)),
            ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
        )

    def test_harmonic_minor(self):
        self.assertEqual(
            list(map(str, Scale("C4", "harmonic_minor").notes)),
            ["C", "D", "Eb", "F", "G", "Ab", "B"],
        )

    def test_melodic_minor(self):
        self.assertEqual(
            list(map(str, Scale("C4", "melodic_minor").notes)),
            ["C", "D", "Eb", "F", "G", "A", "B"],
        )

    def test_major_pentatonic(self):
        self.assertEqual(
            list(map(str, Scale("C4", "major_pentatonic").notes)),
            ["C", "D", "E", "G", "A"],
        )

    def test_minor_pentatonic(self):
        self.assertEqual(
            list(map(str, Scale("C4", "minor_pentatonic").notes)),
            ["C", "Eb", "F", "G", "Bb"],
        )

    def test_sharp_root_scale(self):
        """Scale from a sharp root note."""
        s = Scale("F#4", "major")
        self.assertEqual(
            list(map(str, s.notes)),
            ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
        )

    def test_flat_root_scale(self):
        """Scale from a flat root note."""
        s = Scale("Bb4", "major")
        self.assertEqual(
            list(map(str, s.notes)),
            ["Bb", "C", "D", "Eb", "F", "G", "A"],
        )

    def test_scale_indexing(self):
        """Indexing wraps around with octaves."""
        s = Scale("C4", "major")
        self.assertEqual(s[0].scientific_notation(), "C4")
        self.assertEqual(s[7].scientific_notation(), "C5")
        self.assertEqual(s[14].scientific_notation(), "C6")

    def test_scale_slice(self):
        s = Scale("C4", "harmonic_minor")
        result = [n.scientific_notation() for n in s[7:12]]
        self.assertEqual(result, ["C5", "D5", "Eb5", "F5", "G5"])

    def test_scale_length(self):
        self.assertEqual(len(Scale("C4", "major")), 7)
        self.assertEqual(len(Scale("C4", "major_pentatonic")), 5)

    def test_scale_contains(self):
        s = Scale("C4", "major")
        self.assertTrue(Note("E4") in s)
        self.assertFalse(Note("Eb4") in s)
        self.assertTrue(Note("F7") in s)  # Octave doesn't matter

    def test_invalid_scale(self):
        self.assertRaises(Exception, Scale, "C4", "non_existent")

    def test_scale_from_string(self):
        """Scale root can be a string instead of a Note."""
        s = Scale("D4", "natural_minor")
        self.assertEqual(
            list(map(str, s.notes)),
            ["D", "E", "F", "G", "A", "Bb", "C"],
        )

    def test_scale_str(self):
        self.assertEqual(str(Scale("C4", "major")), "C major")


if __name__ == "__main__":
    unittest.main()
