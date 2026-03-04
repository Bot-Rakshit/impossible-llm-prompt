"""
Music theory library: Note, Interval, and Scale.
Reference implementation adapted from musthe by Gonzalo Ciruelos.
"""

import re
import math
from functools import reduce


LETTERS = 'CDEFGAB'
LETTERS_IDX = {x: i for i, x in enumerate(LETTERS)}
LETTER_SEMITONES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

# Interval definitions: quality+number -> semitones
INTERVAL_SEMITONES = {
    'd1': -1, 'P1': 0,  'A1': 1,
    'd2': 0,  'm2': 1,  'M2': 2,  'A2': 3,
    'd3': 2,  'm3': 3,  'M3': 4,  'A3': 5,
    'd4': 4,  'P4': 5,  'A4': 6,
    'd5': 6,  'P5': 7,  'A5': 8,
    'd6': 7,  'm6': 8,  'M6': 9,  'A6': 10,
    'd7': 9,  'm7': 10, 'M7': 11, 'A7': 12,
    'd8': 11, 'P8': 12, 'A8': 13,
}

QUALITY_INVERSE = {'P': 'P', 'd': 'A', 'A': 'd', 'm': 'M', 'M': 'm'}

SCALE_RECIPES = {
    'major':            ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7'],
    'natural_minor':    ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'm7'],
    'harmonic_minor':   ['P1', 'M2', 'm3', 'P4', 'P5', 'm6', 'M7'],
    'melodic_minor':    ['P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'M7'],
    'major_pentatonic': ['P1', 'M2', 'M3', 'P5', 'M6'],
    'minor_pentatonic': ['P1', 'm3', 'P4', 'P5', 'm7'],
}


def _accidental_value(acc):
    return sum(1 if c == '#' else -1 for c in acc)


def _accidental_str(val):
    if val < 0:
        return 'b' * (-val)
    return '#' * val


def _letter_add(letter, interval_number):
    if interval_number == 0:
        raise ValueError('Invalid interval number: 0')
    idx = LETTERS_IDX[letter]
    if interval_number > 0:
        new_idx = (idx + interval_number - 1) % 7
    else:
        new_idx = (idx + interval_number + 1) % 7
    return LETTERS[new_idx]


def _letter_sub(letter1, letter2):
    d = LETTERS_IDX[letter1] - LETTERS_IDX[letter2]
    if d >= 0:
        return d + 1
    return d - 1


class Note:
    _pattern = re.compile(r'^([A-G])(b{0,3}|#{0,3})(\d?)$')

    def __init__(self, note_str):
        m = self._pattern.match(note_str)
        if m is None:
            raise ValueError(f'Could not parse note: {note_str!r}')
        self.letter = m.group(1)
        self.accidental = m.group(2)
        self.octave = int(m.group(3)) if m.group(3) else 4
        self._number = LETTER_SEMITONES[self.letter] + self.octave * 12 + _accidental_value(self.accidental)

    @property
    def midi(self):
        return self._number + 12

    def frequency(self):
        a4_number = LETTER_SEMITONES['A'] + 4 * 12
        return 440.0 * math.pow(2, (self._number - a4_number) / 12.0)

    def to_octave(self, octave):
        return Note(self.letter + self.accidental + str(octave))

    def scientific_notation(self):
        return self.letter + self.accidental + str(self.octave)

    def __add__(self, other):
        if not isinstance(other, Interval):
            raise TypeError(f'Cannot add {type(other).__name__} to Note')

        if other.is_compound():
            return reduce(lambda n, i: n + i, other.split(), self)

        new_letter = _letter_add(self.letter, other.number)
        new_number = self._number + other.semitones
        new_octave = self.octave + int(
            self.letter in LETTERS[8 - other.number:]
        )
        difference = new_number % 12 - LETTER_SEMITONES[new_letter]
        if difference < -3:
            difference += 12
        if difference > 3:
            difference -= 12
        return Note(new_letter + _accidental_str(difference) + str(new_octave))

    def __sub__(self, other):
        if isinstance(other, Interval):
            if other.is_compound():
                return reduce(lambda n, i: n - i, other.split(), self)
            return self.to_octave(self.octave - 1) + other.complement()
        elif isinstance(other, Note):
            semitones = self.midi - other.midi
            if semitones < -1:
                raise ArithmeticError('Interval too small (descending)')
            number = _letter_sub(self.letter, other.letter)
            octaves = 0
            while semitones >= 12:
                semitones -= 12
                octaves += 1
            number = (number + (1 if number < 0 else -1)) % 7 + 1
            for name, st in INTERVAL_SEMITONES.items():
                q = name[0]
                n = int(name[1:])
                if n == number and st == semitones:
                    return Interval(q + str(octaves * 7 + number))
            raise ValueError(
                f'No standard interval for number={number}, semitones={semitones}'
            )
        raise TypeError(f'Cannot subtract {type(other).__name__} from Note')

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.scientific_notation() == other.scientific_notation()

    def __repr__(self):
        return f'Note({self.scientific_notation()!r})'

    def __str__(self):
        return self.letter + self.accidental


class Interval:
    def __init__(self, interval_str):
        self.quality = interval_str[0]
        self.number = int(interval_str[1:])
        self.semitones = 0

        number = self.number
        while number > 8:
            number -= 7
            self.semitones += 12
        simple_key = self.quality + str(number)
        if simple_key not in INTERVAL_SEMITONES:
            raise ValueError(f'Invalid interval: {interval_str!r}')
        self.semitones += INTERVAL_SEMITONES[simple_key]

    def is_compound(self):
        return self.number > 8

    def split(self):
        parts = []
        i_num = self.number
        i_semi = self.semitones
        while i_num > 8:
            i_num -= 7
            i_semi -= 12
            parts.append(Interval('P8'))
        parts.append(Interval(self.quality + str(i_num)))
        return parts

    def complement(self):
        if self.is_compound():
            raise ValueError('Cannot invert a compound interval')
        n = 9 - self.number
        q = QUALITY_INVERSE[self.quality]
        return Interval(q + str(n))

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        return str(self) == str(other)

    def __repr__(self):
        return f'Interval({str(self)!r})'

    def __str__(self):
        return self.quality + str(self.number)


class Scale:
    def __init__(self, root, name):
        if isinstance(root, str):
            root = Note(root)
        if not isinstance(root, Note):
            raise TypeError(f'Invalid root note type: {type(root).__name__}')
        if name not in SCALE_RECIPES:
            raise ValueError(f'Unknown scale type: {name!r}')
        self.root = root
        self.name = name
        self.notes = [(root + Interval(i)).to_octave(0) for i in SCALE_RECIPES[name]]

    def __getitem__(self, k):
        intervals = [Interval(i) for i in SCALE_RECIPES[self.name]]
        if isinstance(k, int):
            octaves = k // len(intervals)
            offset = k - octaves * len(intervals)
            return self.root.to_octave(self.root.octave + octaves) + intervals[offset]
        elif isinstance(k, slice):
            start = k.start or 0
            stop = k.stop or 0
            step = k.step or 1
            return [self[i] for i in range(start, stop, step)]
        raise TypeError(f'Invalid index type: {type(k).__name__}')

    def __len__(self):
        return len(self.notes)

    def __contains__(self, item):
        if isinstance(item, Note):
            return item.to_octave(0) in self.notes
        return False

    def __str__(self):
        return f'{self.root} {self.name}'

    def __repr__(self):
        return f'Scale({self.root!r}, {self.name!r})'
