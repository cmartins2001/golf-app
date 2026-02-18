# ⛳ Golf Performance Dashboard

A clean, interactive dashboard for tracking Uneekor launch monitor data over time. Built with Python, Polars, and marimo for fast data processing and beautiful visualizations.

## Features

- **📊 Multi-session tracking**: Automatically combines data from multiple range sessions
- **🏌️ Club tracking**: Assign clubs to sessions for club-specific analysis and comparison
- **🎯 Goal setting**: Set personal targets and track progress against them
- **📈 Trend analysis**: Rolling averages show improvement over time
- **🎪 Shot patterns**: Visualize dispersion and identify consistency issues
- **⚡ Fast processing**: Polars-based pipeline handles large datasets efficiently
- **🔍 Flexible filtering**: Filter all visualizations by club for targeted practice insights

## Quick Start

### 1. Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install marimo polars plotly
```

### 2. Add Your Data

Export your range session from Refine software and add it with club information:

**Easy method (with prompts):**
```bash
python add_session.py ~/Downloads/my_session.csv
# Follow prompts to select club and add notes
```

**Quick method (all at once):**
```bash
python add_session.py ~/Downloads/my_session.csv \
  --date 2025-01-20 \
  --club "7 Iron" \
  --notes "Working on consistency"
```

Files are automatically saved as:
```
golf_dashboard/
├── data/
│   ├── session_2025_01_13.csv
│   ├── session_2025_01_20.csv  ← Your new session
│   └── club_metadata.json       ← Club assignments (auto-created)
```

**File naming convention:** `session_YYYY_MM_DD.csv`

See [CLUB_TRACKING.md](CLUB_TRACKING.md) for complete club management guide.

### 3. Launch Dashboard

```bash
cd golf_dashboard
marimo edit dashboard.py
```

Your browser will open automatically with the interactive dashboard.

## Dashboard Sections

### 🏌️ Club Filter
Dropdown selector to filter all visualizations by specific club:
- View "All Clubs" for comprehensive analysis
- Select individual club (e.g., "7 Iron") for focused tracking
- All charts update automatically when filter changes

### 🎯 Goal Configuration
Set personal targets for:
- Distance consistency (std dev)
- Directional consistency (std dev)
- Overall quality score
- Strike quality rate

### 📊 Performance Overview
- **Summary table**: Current vs historical vs goals
- **Radar chart**: Multi-dimensional performance comparison

### 🎯 Consistency Metrics
Four key indicators tracked across sessions:
- Distance consistency
- Directional control
- Strike quality
- Shot shape quality

### 📉 Trend Analysis
- Distance consistency trend (3-session rolling average)
- Quality score trend (composite metric)
- Automatic goal comparison

### 🎪 Shot Dispersion
Interactive scatter plot showing:
- Landing positions (carry distance vs lateral)
- Current session highlighted
- Goal zones overlaid
- Shot type color coding

### 📊 Club Comparison
Performance table across all clubs:
- Median carry distance per club
- Consistency metrics by club
- Strike quality rates
- Total sessions and shots per club

## Key Metrics Explained

### Quality Score (Composite)
Weighted combination of four factors:
- **Distance consistency (30%)**: Lower std dev = better
- **Directional consistency (30%)**: Lower std dev = better
- **Strike quality (20%)**: % of shots with smash factor > 1.25
- **Shot shape (20%)**: % of non-slice/hook shots

### Valid Shots
Filters applied for statistics:
- Carry distance > 50 yards
- Ball speed > 60 mph
- Excludes obvious mishits

### Strike Quality
Percentage of shots with smash factor > 1.25, indicating center-face contact

### Optimal Launch
Percentage of shots in ideal launch window:
- Launch angle: 12-18°
- Backspin: 2000-4000 rpm
- *Note: Adjust these ranges in `data_processor.py` for your clubs*

## Customization

### Modify Goal Ranges
Edit slider parameters in `dashboard.py`:
```python
carry_std_goal = mo.ui.slider(
    start=5, stop=20, value=12,  # Change these
    step=0.5
)
```

### Change Optimal Launch Windows
Edit `_clean_and_enrich()` in `utils/data_processor.py`:
```python
(
    pl.col("Launch Angle").is_between(12, 18) &  # Adjust ranges
    pl.col("Back Spin").is_between(2000, 4000)
).alias("optimal_launch"),
```

### Add Custom Metrics
In `utils/data_processor.py`, extend `get_session_summary()`:
```python
summary = valid_df.group_by("session_id", "session_date").agg([
    # ... existing metrics ...
    pl.col("YourColumn").mean().alias("your_metric"),
])
```

Then create visualizations in `utils/visualizations.py`.

## Project Structure

```
golf_dashboard/
├── dashboard.py              # Main marimo dashboard
├── data/                     # Your CSV files go here
│   └── session_*.csv
├── utils/
│   ├── data_processor.py     # Polars data pipeline
│   └── visualizations.py     # Plotly chart functions
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Tips for Best Results

1. **Consistent naming**: Use `session_YYYY_MM_DD.csv` format
2. **Regular uploads**: Track weekly for meaningful trends
3. **Set realistic goals**: Start conservative, adjust as you improve
4. **Filter mishits**: Statistics automatically exclude obvious errors
5. **Version control**: Keep dashboard in git for easy updates

## Troubleshooting

**Error: "No files matching pattern"**
- Check that CSV files are in `data/` directory
- Verify filename format: `session_YYYY_MM_DD.csv`

**Missing columns in visualizations**
- Ensure your Refine export includes all standard columns
- Check column names match expected format (case-sensitive)

**Metrics seem incorrect**
- Verify "valid shot" filters in `data_processor.py`
- Adjust thresholds for your typical distances

**Dashboard won't load**
- Confirm marimo installation: `marimo --version`
- Check Python version: Requires 3.9+

## Future Enhancements

Ideas for extending the dashboard:
- [ ] Club-specific analysis (requires club data in CSV)
- [ ] Weather impact tracking (manual metadata)
- [ ] Session notes/annotations
- [ ] Export performance reports
- [ ] Mobile-friendly layouts
- [ ] Comparison with tour averages

## Dependencies

- **Python**: 3.9+
- **marimo**: Interactive notebook environment
- **polars**: Fast data processing
- **plotly**: Interactive visualizations

## License

MIT License - Feel free to modify and share!

---

**Built for golfers who love data** 📊⛳
