# HarmonyHub Codebase Explanation

## Overview

HarmonyHub is an AI-driven adaptive music education platform that uses the Mistral LLM API to generate personalized music exercises. The codebase is organized into modular components for music generation, processing, and visualization.

---

## Project Architecture

### Core Modules

#### `lib/music_generation/`
- **generator.py**: Orchestrates LLM-based exercise generation
- **theory.py**: Music theory utilities (note conversion, validation)
- **constants.py**: Musical constants and configurations

#### `processing/`
Handles conversion and rendering of generated music:
- **midi/converter.py**: JSON → MIDI conversion
- **audio/converter.py**: MIDI → MP3 audio conversion  
- **visualization/visualizer.py**: Piano roll visualization
- **notation/sheet_music.py**: JSON → Music21 → PDF/SVG/PNG (NEW)

#### `cli.py`
Command-line interface using Typer with Rich formatting for output

---

## Sheet Music Module (NEW)

### Purpose
The notation module (`processing/notation/`) provides professional sheet music generation from JSON exercise data. It converts music data to multiple visual formats suitable for printing, screen display, and digital distribution.

### Key Components

#### `constants.py`
Configuration mappings for:
- **Instrument clefs** (treble for wind/strings, grand staff for piano)
- **Duration conversion** (8th note units → music21 quarterLength)
- **Rendering settings** (DPI, page size, margins for PDF/SVG/PNG)

#### `sheet_music.py`
Core functions:

1. **json_to_music21_score()**
   - Converts JSON exercise data to music21 Score object
   - Handles: instruments, key signatures, time signatures, tempos
   - Parses both JSON strings and Python lists
   - Returns music21.stream.Score or None

2. **render_score_to_pdf()**
   - Primary: Uses LilyPond backend for professional quality
   - Fallback: music21's MusicXML → PDF rendering
   - Creates temporary file if no output path provided
   - Returns path to generated PDF or None

3. **render_score_to_image()**
   - Supports PNG and SVG formats
   - SVG via MusicXML intermediate format
   - PNG via matplotlib backend
   - Returns path to generated image or None

4. **Helper Functions**
   - `get_clef_for_instrument()`: Maps instrument → correct clef
   - `duration_units_to_quarter_length()`: Converts 8th note units to music21 format
   - `validate_score()`: Checks Score object integrity
   - `parse_key_signature()`: Converts string to music21 Key
   - `parse_time_signature()`: Converts string to music21 TimeSignature

### Data Flow

```
JSON Exercise Data (from generator.py)
         ↓
json_to_music21_score() [converts to music21 Score]
         ↓
    ┌────┴────┬────────┐
    ↓         ↓        ↓
render_to  render_to  render_to
  PDF       SVG       PNG
    ↓         ↓        ↓
Output files (saved to /output directory)
```

### Duration System

The JSON format uses **8th note units** where:
- 1 = 8th note (♪)
- 2 = quarter note (♩)
- 4 = half note (𝅗𝅥)
- 8 = whole note (𝅗𝅥·)

music21 uses **quarterLength** where 1.0 = quarter note, so conversion multiplies by 0.5.

### Instrument Support

✓ Trumpet (treble clef)
✓ Violin (treble clef)
✓ Flute (treble clef)
✓ Clarinet (treble clef)
✓ Piano (grand staff: treble + bass)

### Error Handling

All functions handle errors gracefully:
- Invalid notes: Skipped with warning, processing continues
- Missing LilyPond: Falls back to music21 rendering
- Invalid JSON: Returns None
- Missing output directory: Created automatically

---

## Integration with CLI

### Updated Commands

**generate** command now supports:
- `--output-format json|midi|mp3|pdf|svg|png|all`
- Generates sheet music alongside audio/MIDI

**convert** command now supports:
- PDF conversion from JSON files
- Sheet music generation from existing exercises

**info** command displays:
- All 6 output format options
- Descriptions of each format

### Usage Examples

```bash
# Generate with all formats
python cli.py generate --instrument Trumpet --level Intermediate --output-format all

# Generate PDF only
python cli.py generate --instrument Piano --output-format pdf

# Convert JSON to PDF
python cli.py convert --input-file exercise.json --output-format pdf

# View available options
python cli.py info
```

---

## Testing

### Unit Tests (`tests/processing/test_sheet_music.py`)

Test coverage includes:
- **Score Creation**: All 5 instruments, various keys, time signatures
- **Duration Conversion**: Correct quarterLength calculation
- **Helper Functions**: Clef selection, key/time signature parsing
- **PDF Rendering**: With/without LilyPond, fallback mechanisms
- **Image Rendering**: PNG and SVG generation
- **Error Handling**: Invalid notes, empty JSON, graceful degradation
- **Integration**: Full workflow from JSON → PDF/SVG

### Running Tests

```bash
# All sheet music tests
python -m pytest tests/processing/test_sheet_music.py -v

# With coverage
python -m pytest tests/processing/test_sheet_music.py --cov=processing.notation

# Specific test class
python -m pytest tests/processing/test_sheet_music.py::TestJsonToMusic21Score -v
```

---

## Dependencies

### Required
- **music21** (9.1.0): Core music notation library

### Optional (for best PDF quality)
- **lilypond**: Professional music notation engraver
- **ghostscript**: PDF optimization
- **matplotlib**: PNG rendering backend

### Development
- **pytest**: Test framework
- **typer**: CLI framework
- **rich**: Console formatting

---

## Quality Assurance

✅ **Backward Compatibility**: Existing `--output-format json|midi|mp3` unchanged
✅ **Error Handling**: Graceful degradation throughout
✅ **Type Hints**: Full type annotations on all functions
✅ **Docstrings**: Comprehensive documentation
✅ **Test Coverage**: 22 unit tests covering all major scenarios
✅ **Performance**: Optimized for 4-16 measure exercises (~5-20s generation time)

---

## Future Enhancements

- [ ] Chord symbol notation
- [ ] Dynamics and articulation marks
- [ ] MIDI velocity-based dynamics
- [ ] Export to MuseScore/Finale formats
- [ ] Interactive web viewer for SVG
- [ ] Batch PDF generation
- [ ] Custom page layouts and formatting
