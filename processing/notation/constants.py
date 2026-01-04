#!/usr/bin/env python

"""
Notation Constants
================
Configuration and constants for sheet music generation.
"""

from typing import Dict

# Clef types by instrument
INSTRUMENT_CLEFS: Dict[str, str] = {
    "Trumpet": "treble",
    "Piano": "grand staff",      # Special case: needs both treble and bass
    "Violin": "treble",
    "Clarinet": "treble",
    "Flute": "treble"
}

# Staff types for each instrument
INSTRUMENT_STAVES: Dict[str, str] = {
    "Trumpet": "staff",
    "Piano": "grand staff",      # Grand staff for piano
    "Violin": "staff",
    "Clarinet": "staff",
    "Flute": "staff"
}

# Duration mapping: 8th note units → music21 quarterLength
# Duration in JSON is in 8th note units where:
# 1 = 8th note, 2 = quarter note, 4 = half note, 8 = whole note
DURATION_MAP: Dict[int, float] = {
    1: 0.5,      # 8th note → quarter_length 0.5
    2: 1.0,      # quarter note → quarter_length 1.0
    4: 2.0,      # half note → quarter_length 2.0
    8: 4.0       # whole note → quarter_length 4.0
}

# PDF rendering settings
PDF_DPI = 300
PDF_PAGE_SIZE = "A4"
PDF_MARGIN = 0.5  # inches

# SVG rendering settings
SVG_WIDTH = 1000
SVG_HEIGHT = 600
SVG_DPI = 300

# PNG rendering settings
PNG_DPI = 300
PNG_WIDTH = 1000
PNG_HEIGHT = 600

# LilyPond settings
LILYPOND_PAPER_SIZE = "a4"
LILYPOND_MARGIN = 0.5
LILYPOND_FONT_SIZE = 14

# Color scheme for staff notation
STAFF_COLOR = "black"
NOTE_COLOR = "black"
LEDGER_LINE_COLOR = "black"
MEASURE_LINE_COLOR = "black"

# Key signature display settings
KEY_DISPLAY_SIZE = 12
KEY_OFFSET_X = 30
KEY_OFFSET_Y = 0

# Time signature display settings
TIME_DISPLAY_SIZE = 16
TIME_OFFSET_X = 70
TIME_OFFSET_Y = 0
