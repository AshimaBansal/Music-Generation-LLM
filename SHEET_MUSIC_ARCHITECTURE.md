# Visual Architecture Diagram for Sheet Music Enhancement

## Current vs. Enhanced Architecture

### CURRENT ARCHITECTURE (Before Enhancement)
```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLI Interface (cli.py)                       │
│                                                                       │
│  Commands: generate | metronome | convert | info                     │
│  Formats: JSON, MIDI, MP3, ALL                                       │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
        ┌─────────────┴──────────────────────┐
        │                                    │
        ▼                                    ▼
┌──────────────────┐              ┌──────────────────────┐
│    Generator     │              │  Processing Modules  │
│  (generator.py)  │              │                      │
│                  │              │  1. MIDI Converter   │
│ • LLM Query      │              │     (JSON → MIDI)    │
│ • Fallbacks      │              │                      │
│ • Validation     │              │  2. Audio Converter  │
│ • Duration       │              │     (MIDI → MP3)     │
│   Scaling        │              │                      │
└────────┬─────────┘              │  3. Visualization    │
         │                        │     (Piano Roll PNG) │
         │                        │                      │
         └────────┬───────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
  JSON Output           File Storage
  (Note Data)           (./output/)
                        • .json
                        • .mid
                        • .mp3
                        • .png
```

---

### ENHANCED ARCHITECTURE (After Enhancement)
```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Enhanced CLI Interface (cli.py)                    │
│                                                                            │
│  Commands: generate | metronome | convert | info                          │
│  Formats: JSON, MIDI, MP3, PDF, SVG, PNG, ALL                            │
│           ✅ NEW: PDF, SVG formats                                        │
└──────────────────────┬──────────────────────────────────────────────────┘
                       │
       ┌───────────────┴──────────────────────┐
       │                                      │
       ▼                                      ▼
┌──────────────────┐              ┌──────────────────────────────────┐
│    Generator     │              │    Processing Pipeline           │
│  (generator.py)  │              │                                  │
│                  │              │  1. MIDI Converter               │
│ • LLM Query      │              │     (JSON → MIDI)                │
│ • Fallbacks      │              │                                  │
│ • Validation     │              │  2. Audio Converter              │
│ • Duration       │              │     (MIDI → MP3)                 │
│   Scaling        │              │                                  │
└────────┬─────────┘              │  3. Visualization (Piano Roll)   │
         │                        │     (JSON → PNG)                 │
         │                        │                                  │
         │                        │  4. NOTATION [NEW MODULE]        │
         │                        │     📁 processing/notation/      │
         │                        │     ├─ sheet_music.py           │
         │                        │     └─ constants.py             │
         │                        │                                  │
         │                        │     Functions:                   │
         │                        │     • json_to_music21_score()   │
         │                        │     • render_score_to_pdf()    │
         │                        │     • render_score_to_image()  │
         │                        │                                  │
         └────────┬───────────────┘
                  │
      ┌───────────┴────────────────────────────┐
      │                                        │
      ▼                                        ▼
  JSON Output                          File Storage (./output/)
  (Note Data)                          
                                       OLD OUTPUTS:
                                       ✅ exercise.json
                                       ✅ exercise.mid
                                       ✅ exercise.mp3
                                       ✅ exercise_viz.png
                                       
                                       NEW OUTPUTS:
                                       ✨ exercise.pdf
                                       ✨ exercise.svg
```

---

## Module Structure Comparison

### BEFORE (Existing)
```
lib/
  music_generation/
    ├── generator.py (398 lines)
    ├── theory.py
    └── constants.py

processing/
  ├── midi/
  │   └── converter.py
  ├── audio/
  │   └── converter.py
  └── visualization/
      └── visualizer.py
```

### AFTER (Enhanced)
```
lib/
  music_generation/
    ├── generator.py (398 lines) - NO CHANGE
    ├── theory.py - NO CHANGE
    └── constants.py - NO CHANGE

processing/
  ├── midi/
  │   └── converter.py - NO CHANGE
  ├── audio/
  │   └── converter.py - NO CHANGE
  ├── visualization/
  │   └── visualizer.py - NO CHANGE
  └── notation/  ✨ NEW DIRECTORY
      ├── __init__.py
      ├── sheet_music.py ✨ NEW (300-400 lines expected)
      └── constants.py ✨ NEW (50-100 lines expected)
```

---

## Data Transformation Pipeline (Detailed)

```
USER INPUT (CLI)
│
├─ instrument: Trumpet
├─ level: Intermediate
├─ key: C Major
├─ time_signature: 4/4
├─ measures: 4
├─ tempo: 120
└─ output_format: all

     │
     ▼

┌─────────────────────────────────────────┐
│   EXERCISE GENERATION                   │
│   (lib/music_generation/generator.py)   │
└─────────────────┬───────────────────────┘
                  │
         Output: JSON note data
         [{note: "C4", duration: 2, ...},
          {note: "E4", duration: 2, ...},
          ...]
                  │
    ┌─────────────┼─────────────┬─────────────┬────────────┐
    │             │             │             │            │
    ▼             ▼             ▼             ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│ MIDI   │  │ AUDIO  │  │  PIANO   │  │ NOTATION │  │ NOTATION     │
│Convert │  │Convert │  │ ROLL VIZ │  │ (PDF)    │  │ (SVG/PNG)    │
└───┬────┘  └───┬────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘
    │           │            │             │               │
    ▼           ▼            ▼             ▼               ▼
 .midi        .mp3        .png(viz)  .pdf(sheet)      .svg/.png(sheet)
    │           │            │             │               │
    └─────────────┼────────────┴─────────────┴───────────────┘
                  │
                  ▼
         ┌─────────────────────────────┐
         │  FILE OUTPUT (./output/)    │
         │                             │
         │  Generated files:           │
         │  ✅ exercise.json           │
         │  ✅ exercise.mid            │
         │  ✅ exercise.mp3            │
         │  ✅ exercise_viz.png        │
         │  ✨ exercise.pdf (NEW)      │
         │  ✨ exercise.svg (NEW)      │
         └─────────────────────────────┘
```

---

## CLI Command Changes

### BEFORE
```bash
python cli.py generate \
  --instrument Trumpet \
  --level Intermediate \
  --output-format all
```

**Output formats**: JSON, MIDI, MP3, PNG (piano roll)

---

### AFTER
```bash
python cli.py generate \
  --instrument Trumpet \
  --level Intermediate \
  --output-format all
```

**Output formats**: JSON, MIDI, MP3, PNG (piano roll), **PDF (NEW)**, **SVG (NEW)**

---

## Code Changes Map

### **File Modifications Summary**

```
┌─────────────────────────────────────────────────────────────────┐
│                        cli.py (MODIFY)                           │
│                                                                  │
│  CHANGES:                                                        │
│  1. OutputFormat Enum (line 70):                                │
│     ADD: PDF = "pdf"                                            │
│     ADD: SVG = "svg"                                            │
│     ADD: PNG = "png"                                            │
│                                                                  │
│  2. generate_exercise_with_output() function (line ~95):        │
│     ADD: Call to notation.sheet_music.json_to_music21_score()  │
│     ADD: Call to notation.sheet_music.render_score_to_pdf()    │
│     ADD: Call to notation.sheet_music.render_score_to_image()  │
│                                                                  │
│  3. generate command (~line 150):                               │
│     ADD: PDF/SVG format handling in output section              │
│                                                                  │
│  4. convert command (~line 260):                                │
│     ADD: PDF output format support                              │
│                                                                  │
│  5. info command (~line 360):                                   │
│     ADD: Display PDF, SVG, PNG in available formats             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│           processing/notation/sheet_music.py (CREATE)            │
│                                                                   │
│  NEW MODULE with functions:                                      │
│                                                                   │
│  json_to_music21_score()                                         │
│    Input: json_data, instrument, key, time_sig, tempo, measures │
│    Output: music21.stream.Score object                          │
│    ~120 lines                                                    │
│                                                                   │
│  render_score_to_pdf()                                           │
│    Input: Score, output_path, use_lilypond=True                │
│    Output: Path to PDF file                                     │
│    ~80 lines                                                     │
│                                                                   │
│  render_score_to_image()                                         │
│    Input: Score, output_path, format='png', dpi=300             │
│    Output: Path to image file                                   │
│    ~60 lines                                                     │
│                                                                   │
│  Helper functions:                                               │
│    - get_clef_for_instrument()                                   │
│    - duration_units_to_quarter_length()                          │
│    - validate_score()                                            │
│    ~70 lines                                                     │
│                                                                   │
│  TOTAL: ~330 lines                                               │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│          processing/notation/constants.py (CREATE)               │
│                                                                   │
│  NEW CONSTANTS:                                                  │
│                                                                   │
│  INSTRUMENT_CLEFS = {...}                                       │
│  DURATION_MAP = {...}                                           │
│  LILYPOND_PATHS = {...}                                         │
│  PDF_SETTINGS = {...}                                           │
│                                                                   │
│  TOTAL: ~80 lines                                                │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    Dockerfile (MODIFY)                            │
│                                                                   │
│  ADD system dependency:                                          │
│  lilypond \                                                      │
│  ghostscript \  (optional, for PDF optimization)                │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│           tests/processing/test_sheet_music.py (CREATE)          │
│                                                                   │
│  Unit tests for:                                                 │
│  - json_to_music21_score()                                      │
│  - render_score_to_pdf()                                        │
│  - render_score_to_image()                                      │
│  - Instrument clef selection                                     │
│  - Duration conversion                                           │
│  - Error handling                                                │
│                                                                   │
│  TOTAL: ~150-200 lines                                           │
└──────────────────────────────────────────────────────────────────┘

MINIMAL CHANGES:
┌──────────────────────────────────────────────────────────────────┐
│  requirements.txt (CHECK ONLY)                                   │
│    - music21==9.1.0 already present ✅                          │
│    - No new Python packages needed                               │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  CODEBASE_EXPLANATION.md (UPDATE)                               │
│    - Add section about notation module                           │
│    - Update data flow diagrams                                   │
│    - Document sheet music generation                             │
└──────────────────────────────────────────────────────────────────┘
```

---

## Import Changes Needed

### In cli.py - Add at top:
```python
# NEW IMPORT
from processing.notation.sheet_music import (
    json_to_music21_score,
    render_score_to_pdf,
    render_score_to_image
)
```

### Create processing/notation/__init__.py with:
```python
from .sheet_music import (
    json_to_music21_score,
    render_score_to_pdf,
    render_score_to_image
)

__all__ = [
    'json_to_music21_score',
    'render_score_to_pdf',
    'render_score_to_image'
]
```

---

## Key Decision Points

### **1. PDF Generation Strategy**
- **Primary**: Use LilyPond backend via music21
- **Fallback**: Use music21's built-in MusicXML renderer
- **Reason**: LilyPond produces professional-grade output

### **2. SVG/PNG Generation Strategy**
- **Primary**: music21's built-in rendering with matplotlib
- **Fallback**: Use PIL image manipulation
- **Reason**: Better quality than piano roll, actual staff notation

### **3. Instrument Support**
- **All 5 existing instruments** automatically supported
- **Clef selection**: Treble for most, special handling for Piano
- **Extensibility**: Easy to add more instruments

### **4. Error Handling Approach**
```
Try LilyPond export
  ├─ Success → Return PDF path
  ├─ LilyPond not installed → Try music21 fallback
  └─ All fail → Log warning, skip PDF, continue
```

### **5. Performance Considerations**
- PDF generation slower than other formats (~1-2 seconds)
- Happens asynchronously during file save
- Doesn't block user if it fails (graceful degradation)

---

## Testing Strategy

### Unit Tests (test_sheet_music.py)
- Test each function in isolation
- Mock music21 for speed
- Test error conditions

### Integration Tests
- End-to-end: JSON → PDF
- Verify PDF file is valid
- Check file naming and placement

### Manual Tests
- Generate exercises with each instrument
- Open PDFs in multiple viewers (Adobe, browser, etc.)
- Check visual quality of sheet music
- Verify all output files created

---

## Rollout Plan

### Phase 1: Create New Module
- [ ] Create processing/notation directory
- [ ] Write sheet_music.py
- [ ] Write constants.py
- [ ] Write __init__.py

### Phase 2: Update CLI
- [ ] Add OutputFormat options
- [ ] Update generate command
- [ ] Update convert command
- [ ] Update info command

### Phase 3: Update Infrastructure
- [ ] Update Dockerfile
- [ ] Update requirements.txt (if needed)

### Phase 4: Testing
- [ ] Write unit tests
- [ ] Test end-to-end generation
- [ ] Test error cases
- [ ] Manual quality checks

### Phase 5: Documentation
- [ ] Update CODEBASE_EXPLANATION.md
- [ ] Update README.md with examples
- [ ] Document new CLI options

---

## Expected Output Example

After running:
```bash
python cli.py generate \
  --instrument Trumpet \
  --level Intermediate \
  --key "C Major" \
  --time-signature "4/4" \
  --measures 4 \
  --output-format all
```

Resulting files:
```
output/
├── exercise_Trumpet_Intermediate_4m.json
│   └── Contains: [{"note": "C4", "duration": 2, ...}, ...]
│
├── exercise_Trumpet_Intermediate_4m.mid
│   └── MIDI file with instrument, tempo, time signature
│
├── exercise_Trumpet_Intermediate_4m.mp3
│   └── Audio synthesis using soundfont
│
├── exercise_Trumpet_Intermediate_4m_viz.png
│   └── Piano roll visualization (existing)
│
├── exercise_Trumpet_Intermediate_4m.pdf ✨ NEW
│   └── Professional sheet music, ready to print
│       Shows: staff, clef, key signature, time signature,
│       notes on staff, measure lines, proper formatting
│
└── exercise_Trumpet_Intermediate_4m.svg ✨ NEW
    └── Scalable vector sheet music (for web)
        Same content as PDF but as SVG
```

---

## Summary Table

| Aspect | Before | After |
|--------|--------|-------|
| **Output Formats** | 4 (JSON, MIDI, MP3, PNG) | 6 (+ PDF, SVG) |
| **Modules** | 3 (midi, audio, visualization) | 4 (+ notation) |
| **Python Packages** | No change needed | No change (music21 exists) |
| **System Dependencies** | fluidsynth, ffmpeg | + lilypond (optional) |
| **File Size** | ~1000 lines | +~500 lines |
| **Test Coverage** | Existing tests | + Sheet music tests |
| **User Commands** | 4 formats | 6 formats |
| **PDF Quality** | N/A | Professional/Print-ready |

---

This plan provides a clear, structured approach to adding sheet music generation without disrupting existing functionality!
