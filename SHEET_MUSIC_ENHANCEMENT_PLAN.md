# Enhancement Plan: Visual Sheet Music Output via Music21/LilyPond + PDF Export

## 📋 Overview
Add professional sheet music notation and PDF export capabilities to HarmonyHub using `music21` library (already in requirements.txt) and optional `lilypond` system dependency for enhanced rendering.

---

## 📊 Current State Analysis

### What Exists
- ✅ `music21==9.1.0` already in requirements.txt (not currently used for notation)
- ✅ Piano roll visualization (matplotlib-based) in `processing/visualization/visualizer.py`
- ✅ JSON → MIDI → MP3 conversion pipeline
- ✅ Output format system (JSON, MIDI, MP3, ALL) in cli.py
- ✅ Multi-stage generation pipeline

### What's Missing
- ❌ No sheet music rendering
- ❌ No PDF export capability
- ❌ No proper musical staff notation (treble/bass clef, time signatures displayed visually)
- ❌ No LilyPond integration
- ❌ Limited notation customization (key signature visual display, rests display, etc.)

---

## 🎯 Implementation Plan

### **Phase 1: Create New Sheet Music Module**

#### **Location**: `processing/notation/sheet_music.py` (NEW FILE)

**Purpose**: Generate professional sheet music from JSON note data

**Key Components**:

1. **`json_to_music21_score(json_data, instrument, key, time_signature, tempo, measures) → music21.stream.Score`**
   - Convert JSON exercise format → music21 Score object
   - Inputs:
     - `json_data`: List of dicts with note, duration, cumulative_duration
     - `instrument`: Instrument name (determines clef: treble for Trumpet/Flute, alto for Violin, etc.)
     - `key`: Key signature (e.g., "C Major")
     - `time_signature`: Time signature string (e.g., "4/4")
     - `tempo`: BPM
     - `measures`: Number of measures
   - Outputs:
     - music21 Score object with properly formatted score
   
   **Process**:
   - Create music21.stream.Score()
   - Add appropriate instrument (via music21.instrument module)
   - Set time signature metadata
   - Set key signature metadata
   - Add tempo marking
   - For each note in JSON:
     - Convert duration units → music21 duration (8th → Note object with quarterLength)
     - Add Note objects to stream
     - Group by measures using bar durations
   - Return complete Score

2. **`render_score_to_image(score, output_path, format='png', dpi=300) → str`**
   - Render music21 Score to image (PNG/SVG)
   - Uses music21's built-in MuseScore/Finale/LilyPond backend
   - Fallback: render to PNG if PDF requires external tools
   - Returns path to generated image

3. **`render_score_to_pdf(score, output_path, use_lilypond=True) → str`**
   - High-quality PDF export using LilyPond (preferred) or music21 backend
   - Two approaches:
     - **LilyPond Path**: Export via music21 to LilyPond format, compile to PDF
     - **Fallback Path**: Use music21's MusicXML → PDF conversion
   - Returns path to generated PDF

4. **Helper Functions**:
   ```python
   def get_clef_for_instrument(instrument: str) -> str
   def get_staff_type_for_instrument(instrument: str) -> str  
   def duration_units_to_quarter_length(duration_units: int) -> float
   def validate_score(score: music21.stream.Score) -> bool
   ```

---

### **Phase 2: Update CLI Output Format Enum**

#### **Location**: `cli.py` (MODIFY)

**Change**: Add new output format options

```python
class OutputFormat(str, Enum):
    JSON = "json"
    MIDI = "midi"
    MP3 = "mp3"
    PDF = "pdf"           # NEW: Professional sheet music PDF
    SVG = "svg"           # NEW: Scalable vector graphics (sheet music image)
    PNG = "png"           # NEW: Raster image (sheet music image)
    ALL = "all"           # Will now include PDF + PNG
```

**Rationale**: 
- PDF for print-ready professional output
- SVG for web/high-DPI displays
- PNG for web and quick preview
- Keep ALL to include all formats (but may want to make it configurable)

---

### **Phase 3: Update Main Generation Function**

#### **Location**: `cli.py` (MODIFY `generate_exercise_with_output()`)

**Current Return**:
```python
return output_json_str, mp3_path, str(tempo), midi, f"{real_duration:.2f} seconds", time_signature, total_duration
```

**New Return** (or use dictionary for clarity):
```python
return {
    "json": output_json_str,
    "mp3": mp3_path,
    "pdf": pdf_path,        # NEW
    "svg": svg_path,        # NEW
    "png": png_path,        # NEW (from existing visualizer)
    "tempo": str(tempo),
    "midi": midi,
    "duration": f"{real_duration:.2f} seconds",
    "time_signature": time_signature,
    "total_duration": total_duration
}
```

**Process Changes**:
1. After `generate_exercise()` returns note data
2. Convert to MIDI (existing)
3. Convert to MP3 (existing)
4. **NEW**: Create music21 Score from note data
5. **NEW**: Render Score to PDF
6. **NEW**: Render Score to SVG/PNG (with better formatting than current piano roll)
7. Return all paths

---

### **Phase 4: Update CLI Commands**

#### **Location**: `cli.py` (MODIFY)

**1. `generate` Command**:
- Add `--include-pdf` / `--include-sheet-music` flags (optional)
- When `output_format == OutputFormat.ALL`:
  - Generate JSON, MIDI, MP3, PDF, SVG/PNG
  - Display all file outputs
- When `output_format == OutputFormat.PDF`:
  - Only generate PDF (+ JSON for reference)
- Add to output files display:
  ```
  [bold]Output Files:[/bold]
  [bold]JSON:[/bold] exercise.json
  [bold]MIDI:[/bold] exercise.mid
  [bold]MP3:[/bold] exercise.mp3
  [bold]Sheet Music PDF:[/bold] exercise.pdf     # NEW
  [bold]Sheet Music Image:[/bold] exercise.svg   # NEW
  [bold]Piano Roll:[/bold] exercise_viz.png      # EXISTING
  ```

**2. `convert` Command**:
- Update to support PDF output format
- Allow converting JSON → PDF directly

**3. `info` Command**:
- Update available formats display to include PDF, SVG, PNG

---

### **Phase 5: Update Requirements and Dependencies**

#### **Location**: `requirements.txt` (MODIFY)

**Already Present**:
- ✅ `music21==9.1.0` - Core notation library

**Already Present (indirect deps)**:
- ✅ `matplotlib==3.8.2` - For rendering

**Considerations**:
- ✅ `music21` can use system LilyPond if available
- Optional: Add system dependency in Dockerfile

#### **Location**: `Dockerfile` (MODIFY)

**New System Dependencies**:
```dockerfile
# Add after ffmpeg line:
lilypond \
```

**Why?**
- Enables high-quality PDF export from music21
- Optional but recommended for professional output
- Fallback: music21's built-in rendering (works without it)

---

### **Phase 6: Update Directory Structure**

#### **New Directory**: `processing/notation/` (CREATE)

```
processing/notation/
├── __init__.py              # Imports and exports
├── sheet_music.py           # Main sheet music generation
└── constants.py             # Optional: notation-specific constants
```

**Constants to Define**:
```python
# Clef types by instrument
INSTRUMENT_CLEFS = {
    "Trumpet": "treble",
    "Piano": "grand staff",    # Special case: needs both clefs
    "Violin": "treble",
    "Clarinet": "treble",
    "Flute": "treble"
}

# Staff types
INSTRUMENT_STAVES = {
    "Trumpet": "staff",
    "Piano": "grand staff",
    "Violin": "staff",
    "Clarinet": "staff",
    "Flute": "staff"
}

# Duration mapping
DURATION_MAP = {
    1: 0.5,      # 8th note → quarter_length 0.5
    2: 1.0,      # quarter note → quarter_length 1.0
    4: 2.0,      # half note → quarter_length 2.0
    8: 4.0       # whole note → quarter_length 4.0
}
```

---

### **Phase 7: Update Tests**

#### **New Test File**: `tests/processing/test_sheet_music.py` (CREATE)

**Test Cases**:
1. `test_json_to_music21_score_basic()` - Valid note data → Score object
2. `test_json_to_music21_score_different_instruments()` - Test each instrument's clef
3. `test_json_to_music21_score_duration_conversion()` - 8th note units → music21 durations
4. `test_render_score_to_pdf()` - PDF generation succeeds
5. `test_render_score_to_image()` - PNG/SVG generation succeeds
6. `test_key_signature_display()` - Key signature correctly displayed
7. `test_time_signature_display()` - Time signature correctly displayed
8. `test_invalid_json_data()` - Error handling for malformed input

---

### **Phase 8: Integration Flow**

#### **Complete Data Pipeline** (with new sheet music):

```
User Input (CLI)
    ↓
generate_exercise() 
    ↓ [JSON note data]
────────────────────────────────────────
    ├─→ json_to_midi() 
    │    ├─→ MIDI file ✅
    │    └─→ midi_to_mp3() → MP3 file ✅
    │
    ├─→ create_visualization() → Piano roll PNG ✅
    │
    └─→ json_to_music21_score() [NEW]
         ├─→ render_score_to_pdf() → PDF file ✨
         └─→ render_score_to_image() → SVG/PNG ✨
    ↓
Save all outputs to ./output/
    ├── exercise.json
    ├── exercise.mid
    ├── exercise.mp3
    ├── exercise.pdf          # NEW
    ├── exercise.svg          # NEW
    └── exercise_viz.png      # EXISTING
```

---

## 🔧 Implementation Checklist

### **Step-by-Step Changes**

- [ ] **Step 1**: Create `processing/notation/` directory
- [ ] **Step 2**: Create `processing/notation/__init__.py`
- [ ] **Step 3**: Create `processing/notation/sheet_music.py` with:
  - [ ] `json_to_music21_score()` function
  - [ ] `render_score_to_pdf()` function
  - [ ] `render_score_to_image()` function
  - [ ] Helper functions (clef selection, duration conversion, etc.)
- [ ] **Step 4**: Create `processing/notation/constants.py` with instrument mappings
- [ ] **Step 5**: Update `cli.py`:
  - [ ] Add PDF, SVG, PNG to OutputFormat enum
  - [ ] Update `generate_exercise_with_output()` to call sheet music generation
  - [ ] Update `generate` command to handle new output formats
  - [ ] Update `convert` command to support PDF output
  - [ ] Update `info` command to show new formats
  - [ ] Update output file display logic
- [ ] **Step 6**: Update `requirements.txt` (if needed - music21 already there)
- [ ] **Step 7**: Update `Dockerfile`:
  - [ ] Add lilypond system dependency
  - [ ] Add optional ghostscript if PDF generation needed
- [ ] **Step 8**: Create `tests/processing/test_sheet_music.py`
- [ ] **Step 9**: Update `CODEBASE_EXPLANATION.md` with new module
- [ ] **Step 10**: Test end-to-end with all output formats

---

## 📦 Dependencies Analysis

### **Already Available**
```python
music21==9.1.0           # Core: Score, Note, Stream, etc.
matplotlib==3.8.2        # Fallback rendering
```

### **System Dependencies (Dockerfile)**
```
lilypond                 # Preferred: High-quality PDF output
ghostscript              # Optional: PDF manipulation/optimization
```

### **No New Python Packages Needed**
- music21 handles everything
- Can work without system deps (uses built-in rendering)
- LilyPond optional but recommended for best quality

---

## 🎨 Design Decisions

### **1. Why Music21?**
- Already in dependencies
- Industry standard for music notation in Python
- Supports multiple backends (MuseScore, Finale, LilyPond)
- Good MIDI → Score conversion
- Built-in PDF export capability

### **2. Why LilyPond?**
- Professional-grade sheet music quality
- Excellent PDF output
- Free and open-source
- Music21 integrates seamlessly
- Can be optional (graceful degradation)

### **3. Format Strategy**
- **PDF**: Print-ready, professional, archival
- **SVG**: Web-friendly, scalable, high-DPI capable
- **PNG**: Quick preview, web embedding, fallback
- All generated automatically with `--output-format all`

### **4. Instrument Handling**
- **Treble Instruments** (Trumpet, Flute, Clarinet, Violin): Treble clef
- **Piano**: Special case with grand staff (treble + bass)
- Easily extensible for future instruments

### **5. Duration Conversion**
```
8th note units → music21 quarterLength
1 unit = 0.5 (8th note)
2 units = 1.0 (quarter note)
4 units = 2.0 (half note)
8 units = 4.0 (whole note)
```

---

## 🚀 Future Enhancement Possibilities

### **Phase 2 (Later)**
- [ ] Add articulation marks (staccato, accent, legato visual indicators)
- [ ] Add dynamics (pp, mf, f, ff)
- [ ] Add fingering numbers for stringed instruments
- [ ] Add breath marks
- [ ] Multiple staff rendering (score + parts)
- [ ] MusicXML export for DAW/notation software import
- [ ] Interactive score viewer (web-based)

### **Phase 3 (Later)**
- [ ] Chord symbol display
- [ ] Tuplet notation
- [ ] Cross-staff notation for complex pieces
- [ ] Customizable staff size/layout
- [ ] Transposition for different instrument ranges

---

## ⚠️ Edge Cases & Error Handling

### **Scenarios to Handle**:

1. **Missing LilyPond**: 
   - Fallback to music21's built-in rendering
   - Use PIL/matplotlib for PNG

2. **Very High Note Range**:
   - Auto-scale staff to fit all notes
   - Use ledger lines appropriately

3. **Unusual Time Signatures** (if expanded):
   - music21 handles most standard/compound time signatures
   - Graceful degradation for custom time signatures

4. **Long Exercises** (many measures):
   - music21 automatically handles page breaks
   - PDF pagination handled automatically

5. **Invalid Note Data**:
   - Validate JSON before score creation
   - Skip invalid notes with warning
   - Continue processing if possible

---

## 📝 File Modification Summary

| File | Type | Changes |
|------|------|---------|
| `processing/notation/sheet_music.py` | CREATE | New module with sheet music generation |
| `processing/notation/constants.py` | CREATE | Instrument/notation mappings |
| `processing/notation/__init__.py` | CREATE | Module exports |
| `tests/processing/test_sheet_music.py` | CREATE | Unit tests |
| `cli.py` | MODIFY | Add PDF/SVG/PNG format options, update commands |
| `requirements.txt` | CHECK | Verify music21 present (already is) |
| `Dockerfile` | MODIFY | Add lilypond system dependency |
| `CODEBASE_EXPLANATION.md` | UPDATE | Document new notation module |

---

## 🎯 Success Criteria

After implementation, users should be able to:

✅ Run: `python cli.py generate --instrument Trumpet --level Intermediate --output-format pdf`
✅ Get professional PDF sheet music in addition to MIDI/MP3
✅ Run: `python cli.py generate --output-format all` to get all formats including PDF
✅ Convert existing JSON exercises to PDF: `python cli.py convert --input-file exercise.json --output-format pdf`
✅ See visual sheet music with:
   - Correct clef for instrument
   - Proper time signature
   - Key signature
   - Notes correctly positioned on staff
   - Measure bars
   - Professional appearance

---

## 📊 Effort Estimation

| Task | Effort | Priority |
|------|--------|----------|
| Create sheet_music.py module | Medium (2-3 hrs) | HIGH |
| Create constants.py | Low (30 min) | HIGH |
| Update cli.py | Medium (1-2 hrs) | HIGH |
| Create tests | Medium (1-2 hrs) | MEDIUM |
| Update Dockerfile | Low (15 min) | MEDIUM |
| Documentation updates | Low (30 min) | LOW |
| **Total** | **~7-9 hours** | - |

---

## 🎼 Example Usage After Implementation

```bash
# Generate with all formats including PDF
python cli.py generate \
  --instrument Trumpet \
  --level Intermediate \
  --key "C Major" \
  --time-signature "4/4" \
  --measures 4 \
  --tempo 120 \
  --output-format all

# Output:
# ✓ exercise_Trumpet_Intermediate_4m.json
# ✓ exercise_Trumpet_Intermediate_4m.mid
# ✓ exercise_Trumpet_Intermediate_4m.mp3
# ✓ exercise_Trumpet_Intermediate_4m.pdf       ← NEW
# ✓ exercise_Trumpet_Intermediate_4m.svg       ← NEW
# ✓ exercise_Trumpet_Intermediate_4m_viz.png

# Direct PDF generation
python cli.py generate \
  --instrument Piano \
  --level Beginner \
  --output-format pdf

# Convert JSON to PDF
python cli.py convert \
  --input-file old_exercise.json \
  --output-format pdf \
  --instrument Piano
```

---

This plan provides a comprehensive roadmap for adding professional sheet music output while maintaining clean code architecture and seamless integration with existing systems.
