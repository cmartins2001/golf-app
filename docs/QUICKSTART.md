# Quick Start Guide

## Installation (5 minutes)

```bash
# 1. Navigate to the dashboard directory
cd golf_dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python -c "import polars, plotly, marimo; print('✓ All dependencies installed')"
```

## Your First Session (10 minutes)

### Step 1: Prepare Your Data

Your CSV files from Refine should look like this:
```
No,Carry,Total,Side Dist,Smash Factor,Club Speed,Ball Speed,...
20,96.7,104,R 26.7,--,--,86.7,...
19,74.4,81.8,R 19.6,1.05,81.3,85.3,...
```

**Rename** your file to: `session_2025_01_20.csv` (use actual date)

**Move** it to: `golf_dashboard/data/`

### Step 2: Launch Dashboard

```bash
marimo edit dashboard.py
```

Your browser will open automatically at `http://localhost:2718`

### Step 3: Set Your Goals

Use the sliders at the top:
- **Distance Consistency**: Start with 15 yards (tighten as you improve)
- **Directional Consistency**: Start with 20 yards  
- **Quality Score**: Start with 0.70
- **Strike Quality Rate**: Start with 0.60

### Step 4: Explore Your Data

The dashboard has 4 main sections:

1. **Performance Overview** (top)
   - Summary table comparing current vs historical
   - Radar chart showing strengths/weaknesses

2. **Consistency Metrics** (middle)
   - 4 charts tracking key indicators
   - Orange bar = current session
   - Blue bars = historical sessions

3. **Trends Over Time** (middle-bottom)
   - Line charts with 3-session rolling averages
   - Dashed purple line = your goals

4. **Shot Dispersion** (bottom)
   - Scatter plot of where balls landed
   - Toggle between current and all sessions

## Adding Your Second Session

1. Export new session from Refine → CSV
2. Rename to `session_2025_01_27.csv` (new date)
3. Move to `data/` directory
4. Restart marimo (Ctrl+C in terminal, then `marimo edit dashboard.py` again)

The dashboard automatically:
- Loads all sessions
- Recalculates trends
- Updates historical averages
- Shows improvement (or areas to work on!)

## Example Workflow

**Session 1 (Baseline)**
- Upload data
- Set conservative goals
- Identify 2-3 focus areas

**Sessions 2-4 (Practice)**
- Track consistency metrics
- Watch for trends in charts
- Adjust practice based on data

**Session 5+ (Review)**
- Check if meeting goals
- Tighten goal targets
- Celebrate improvements! 🎉

## Pro Tips

### Get Better Data
- Hit at least 15-20 valid shots per session
- Mix clubs to see differences
- Note any equipment changes in filename

### Interpret Metrics
- **Distance std dev < 10 yards** = Tour-level consistency
- **Directional std dev < 15 yards** = Excellent control  
- **Strike quality > 80%** = Finding the sweet spot
- **Quality score > 0.85** = Well-rounded performance

### Common Patterns
- **High slice rate**: Check club path and face angle
- **Inconsistent distance**: Focus on strike location
- **Good quality but offline**: May need alignment work

### Adjust for Your Game
- Playing wedges? Lower distance expectations
- Using driver? Higher variance is normal
- Different clubs? Track separately (requires code modification)

## Troubleshooting

**"No files matching pattern"**
```bash
# Check files are in right place
ls data/
# Should show: session_2025_01_13.csv, etc.

# Check naming format
mv my_session.csv data/session_2025_01_20.csv
```

**Metrics look wrong**
- Ensure CSV has all standard Refine columns
- Check for units (yards not meters, mph not kmh)
- Filter thresholds may need adjustment for your swing

**Dashboard is slow**
- Polars should be fast, but if you have 50+ sessions:
  - Consider archiving old data
  - Use `pl.scan_csv()` lazy evaluation (already implemented)

**Want to modify metrics?**
- See "Customization" section in README.md
- Core logic in `utils/data_processor.py`
- Visualization styling in `utils/visualizations.py`

## What to Track

**First month**: Distance consistency
- Focus on one metric
- Build baseline data
- Set achievable goals

**After 10 sessions**: Add directional work
- Two-pronged improvement
- Balance distance + accuracy
- Track shot shape trends

**Long term**: Full quality score
- Holistic approach
- Compare against past self
- Identify seasonal patterns

## Example Analysis

After 5 sessions, you might see:
- Distance std dev: 18 → 14 yards ✓ (trending toward 12 goal)
- Directional std dev: 25 → 22 yards → (slow progress)
- Strike quality: 55% → 68% ✓ (beating 65% goal)
- Quality score: 0.68 → 0.74 ✓ (approaching 0.80 goal)

**Takeaway**: Solid improvement in striking and distance. Next focus = directional control.

---

Need help? Check the full README.md or customize the code!
