# Changelog

## Version 2.0.0 - Club Management Update (2025-02-16)

### 🎉 Major Features

#### Club-Specific Tracking
- **NEW**: Assign clubs to individual sessions for targeted analysis
- **NEW**: Filter all dashboard metrics by specific club
- **NEW**: Compare performance across your entire bag
- **NEW**: Track improvement for individual clubs over time

#### Interactive Assignment Tools
- **NEW**: `assign_club.py` - Interactive tool for assigning clubs to existing sessions
  - Distance-based suggestions (e.g., 155 yards → suggests 7 Iron)
  - Batch processing for multiple sessions
  - Progress tracking and validation
  - Optional notes per session

- **ENHANCED**: `add_session.py` - Now supports club assignment during upload
  - Interactive prompts for club and notes
  - Command-line flags: `--club`, `--notes`
  - Non-interactive mode for automation
  - Validates club names against standard list

#### Dashboard Enhancements
- **NEW**: Club assignment management UI (collapsible accordion)
  - Shows all sessions with their assigned clubs
  - Highlights unassigned sessions
  - Displays distance-based suggestions
  - Provides assignment instructions
  
- **NEW**: Club filtering dropdown
  - Filter all metrics by specific club
  - "All Clubs" view for overall performance
  - Dynamically populated from your data
  
- **NEW**: Club comparison visualization
  - Side-by-side distance comparison
  - Consistency metrics by club
  - Session volume per club
  - Automatic gap analysis

#### Data Management
- **NEW**: `ClubManager` class for persistent club metadata
  - JSON-based storage (`data/club_metadata.json`)
  - Session-to-club mapping
  - Optional notes per session
  - Support for custom clubs
  
- **NEW**: `club_interface.py` - Reusable UI components
  - Assignment table generator
  - Club selector dropdown
  - Status summaries

### 📚 Documentation

#### New Guides
- **`CLUB_MANAGEMENT.md`** (2,800 words) - Comprehensive guide to club features
  - Quick start examples
  - Workflow tutorials
  - Best practices
  - Troubleshooting
  
- **`CLUB_FEATURE_SUMMARY.md`** - Executive summary of new features
  - Technical implementation details
  - Migration guide
  - Usage examples

#### Updated Documentation
- **`README.md`** - Updated with club tracking quick start
- **`QUICKSTART.md`** - Added club assignment examples
- **`PROJECT_OVERVIEW.md`** - Updated feature list

### 🔧 Technical Changes

#### Core Updates
- **`utils/data_processor.py`**:
  - Added club column to all DataFrames
  - Club-aware filtering in `get_session_summary()`
  - New methods: `get_all_clubs()`, `get_club_comparison()`, `get_sessions_without_clubs()`
  - Integrated ClubManager for automatic metadata loading
  
- **`utils/visualizations.py`**:
  - New chart: `plot_club_comparison()` with distance and consistency subplots
  - All existing charts now work with club-filtered data
  
- **`dashboard.py`**:
  - Added club assignment accordion section
  - Added club filter dropdown
  - Added club comparison chart section
  - Warning display for unassigned sessions

#### New Utilities
- **`utils/club_manager.py`** (177 lines):
  - Persistent JSON storage
  - 16 standard clubs with typical characteristics
  - Distance-based club suggestion algorithm
  - CRUD operations for session-club mappings
  - Custom club support
  
- **`utils/club_interface.py`** (100+ lines):
  - HTML table generator for assignment status
  - Marimo UI components
  - Suggestion display logic

- **`assign_club.py`** (200+ lines):
  - Full interactive CLI for club assignment
  - Distance-based suggestions
  - Batch processing workflow
  - Progress tracking
  - Graceful error handling

### 📊 Standard Clubs Included

Woods: Driver, 3 Wood, 5 Wood  
Hybrids: 3 Hybrid, 4 Hybrid  
Irons: 3-9 Iron  
Wedges: PW, GW, SW, LW

Each club has:
- Typical carry distance (for suggestions)
- Optimal launch angle range
- Optimal spin rate range
- Club type classification

### 🎯 Use Cases Enabled

1. **Single-club improvement tracking**
   - Filter dashboard to one club
   - See consistency trends over weeks/months
   - Set club-specific goals
   
2. **Full bag assessment**
   - Hit each club once
   - View comparison chart
   - Identify gaps or overlaps
   
3. **Club selection validation**
   - Check if you're hitting clubs the expected distance
   - Validate gapping across irons
   - Identify clubs that need attention

4. **Practice planning**
   - See which club has worst consistency
   - Track sessions per club
   - Balance practice across bag

### 🔄 Migration Path

For existing users with sessions already uploaded:

1. Run `python assign_club.py`
2. Tool will show each session with distance-based suggestions
3. Confirm, override, or skip each session
4. Restart dashboard to see club-specific analysis

### ⚙️ Backwards Compatibility

- ✅ All existing features work without club assignments
- ✅ Dashboard displays warnings for unassigned sessions (non-blocking)
- ✅ Can mix assigned and unassigned sessions
- ✅ Club metadata is optional - no breaking changes

### 🐛 Bug Fixes

- Fixed issue where summary calculations didn't account for club context
- Improved error handling for missing metadata files
- Better validation of CSV file formats

### 📦 Dependencies

No new dependencies! Still just:
- marimo >= 0.10.0
- polars >= 0.20.0
- plotly >= 5.18.0

### 💡 Example Workflows

**Workflow 1: Add new session with club**
```bash
python add_session.py today.csv --club "Driver" --notes "Tempo work"
```

**Workflow 2: Assign clubs to 10 old sessions**
```bash
python assign_club.py
# Follow interactive prompts with smart suggestions
```

**Workflow 3: Filter dashboard to see just 7-iron data**
1. Open dashboard
2. Select "7 Iron" from dropdown
3. All charts update to show only 7-iron sessions

**Workflow 4: Compare performance across all clubs**
1. Assign clubs to multiple sessions
2. View "Club Performance Comparison" chart
3. Identify strengths and weaknesses

### 🔮 Future Enhancements

Potential next features:
- Multi-club sessions (split single session by club)
- Custom club definitions (e.g., "4-iron stinger")
- Optimal club recommendations based on conditions
- Equipment change tracking
- Tour average comparisons by club

---

## Version 1.0.0 - Initial Release (2025-02-15)

### Features
- Multi-session data loading and processing
- Interactive goal setting with sliders
- Performance overview with summary tables
- Consistency metrics dashboard
- Trend analysis with rolling averages
- Shot dispersion visualization
- Quality score calculation
- Polars-based data pipeline
- Marimo reactive notebook interface
- Plotly interactive visualizations

### Documentation
- Comprehensive README
- Quick start guide
- Architecture documentation
- Project overview

### Utilities
- `add_session.py` for importing new sessions
- `data_processor.py` for data pipeline
- `visualizations.py` for charts
