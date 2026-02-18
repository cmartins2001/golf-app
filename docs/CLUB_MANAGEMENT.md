# Club Management Guide

The golf dashboard now supports tracking which club was used in each session, enabling powerful club-specific analysis and comparisons.

## Why Club Tracking Matters

Since Uneekor Refine software doesn't automatically track club selection, we've built a flexible system that lets you:

1. **Assign clubs** to sessions after upload
2. **Filter analysis** by specific clubs
3. **Compare performance** across your entire bag
4. **Track improvement** for individual clubs over time

## Quick Start

### Adding a New Session with Club

**Easiest Method** (Interactive):
```bash
python add_session.py ~/Downloads/my_range_session.csv
```

The script will prompt you for:
- Session date (or use today)
- Club used (with suggestions)
- Optional notes

**Command Line Method**:
```bash
python add_session.py ~/Downloads/session.csv \
    --date 2025-01-20 \
    --club "7 Iron" \
    --notes "Working on consistency"
```

### Assigning Clubs to Existing Sessions

If you already have sessions uploaded without clubs:

```bash
python assign_club.py
```

This interactive tool will:
1. Show all unassigned sessions
2. Suggest clubs based on carry distance
3. Guide you through assignment
4. Save metadata automatically

## Usage Examples

### Example 1: Weekly Practice Session
```bash
# Monday - Driver work
python add_session.py mon_driver.csv --club Driver --notes "Tempo focus"

# Wednesday - Iron practice
python add_session.py wed_irons.csv --club "7 Iron"

# Friday - Short game
python add_session.py fri_wedges.csv --club "SW" --notes "60-yard distances"
```

### Example 2: Bulk Assignment
```bash
# Launch interactive assignment tool
python assign_club.py

# Follow prompts:
# Session: 2025-01-13 (session_2025_01_13)
#   Average carry: 105.2 yards
#   💡 Suggested club: PW
# Enter club name: PW
# Add notes: Baseline session
# ✅ Assigned: PW
```

### Example 3: Review Assignments
Open the dashboard and expand the "🏌️ Manage Club Assignments" section to see:
- All sessions with their clubs
- Unassigned sessions (highlighted)
- Suggestions based on distance
- Quick assignment instructions

## Club-Specific Analysis

Once clubs are assigned, the dashboard enables:

### 1. Club Filtering
Use the dropdown to view metrics for a single club:
- **All Clubs** - See everything (default)
- **Driver** - Just your driver sessions
- **7 Iron** - Track iron consistency
- etc.

### 2. Club Comparison Chart
Automatically compares:
- **Distance**: Median carry for each club
- **Consistency**: Standard deviation by club
- **Volume**: Number of sessions per club

### 3. Club-Specific Trends
When filtered to one club:
- Distance consistency over time
- Quality score progression
- Strike quality improvement

## Available Clubs

The system includes 16 standard clubs:

**Woods**: Driver, 3 Wood, 5 Wood

**Hybrids**: 3 Hybrid, 4 Hybrid

**Irons**: 3 Iron, 4 Iron, 5 Iron, 6 Iron, 7 Iron, 8 Iron, 9 Iron

**Wedges**: PW, GW, SW, LW

## Data Storage

Club assignments are stored in `data/club_metadata.json`:

```json
{
  "sessions": {
    "session_2025_01_13": "7 Iron",
    "session_2025_01_20": "Driver"
  },
  "notes": {
    "session_2025_01_13": "Working on consistency"
  },
  "custom_clubs": {}
}
```

**Safe to edit manually** if needed, but tools are recommended.

## Workflows

### Workflow 1: Single-Club Focus
```bash
# Track driver over 4 weeks
python add_session.py week1.csv -c Driver
python add_session.py week2.csv -c Driver
python add_session.py week3.csv -c Driver
python add_session.py week4.csv -c Driver

# In dashboard: Filter to "Driver" → See progression
```

### Workflow 2: Full Bag Assessment
```bash
# One session per club type
python add_session.py driver.csv -c Driver
python add_session.py iron7.csv -c "7 Iron"
python add_session.py wedge.csv -c SW

# In dashboard: View "Club Comparison" chart
```

### Workflow 3: Fixing Missing Data
```bash
# You uploaded 10 sessions without clubs
python assign_club.py

# Follow interactive prompts for each
# Suggestions based on your actual carry distances
```

## Smart Features

### Distance-Based Suggestions
The system suggests clubs based on median carry:
- 250 yards → Driver
- 155 yards → 7 Iron
- 95 yards → SW

These are typical amateur distances. The system adapts to YOUR actual distances.

### Notes and Context
Add session notes to remember:
- Practice focus ("tempo work")
- Conditions ("windy day")
- Equipment changes ("new grips")
- Feel ("felt rushed")

### Validation
Both tools validate club names against the standard list, preventing typos.

## Advanced Usage

### Manual JSON Editing
If you need to bulk-update:

```bash
# Edit data/club_metadata.json directly
{
  "sessions": {
    "session_2025_01_13": "PW",
    "session_2025_01_14": "PW",
    "session_2025_01_15": "9 Iron",
    "session_2025_01_16": "8 Iron"
  }
}
```

Then restart dashboard.

### Custom Clubs
To add non-standard clubs (e.g., "4 Iron Stinger"):

Edit `club_metadata.json`:
```json
{
  "custom_clubs": {
    "4 Iron Stinger": {
      "type": "iron",
      "typical_carry": 175,
      "optimal_launch": [10, 14],
      "optimal_spin": [4000, 5000]
    }
  }
}
```

### Removing Assignments
```python
# In Python/marimo
from utils.club_manager import ClubManager
cm = ClubManager()
cm.remove_session_club("session_2025_01_20")
```

Or edit JSON and delete the entry.

## Best Practices

### 1. Assign Immediately
```bash
# Right after session
python add_session.py today.csv --club "Driver"
# You won't forget which club you used!
```

### 2. Use Consistent Names
- ✅ "7 Iron" (matches standard)
- ❌ "7-iron" (won't match filters)
- ❌ "Seven Iron" (not in list)

### 3. Batch Similar Sessions
```bash
# If you did 3 driver sessions this week
python add_session.py mon.csv -c Driver -n "Day 1"
python add_session.py wed.csv -c Driver -n "Day 2"  
python add_session.py fri.csv -c Driver -n "Day 3"

# Filter to Driver → See week's progression
```

### 4. Add Meaningful Notes
Good notes:
- "New swing thought: lead with hips"
- "Windy, 15mph crosswind"
- "After lesson - focusing on tempo"

Not useful:
- "Practice"
- "Range session"

## Troubleshooting

**Q: Can I change a club assignment?**

A: Yes! Either:
1. Run `python assign_club.py` (skip to session, reassign)
2. Edit `data/club_metadata.json` manually
3. Use the dashboard's accordion to see what's assigned

**Q: What if I used multiple clubs in one session?**

A: Currently, one club per session. Options:
1. Split the CSV into separate files (manual)
2. Assign to the "primary" club you focused on
3. Add note: "Also hit driver and 9-iron"

**Q: Do I have to assign clubs?**

A: No! The dashboard works fine without clubs. But:
- You'll miss club-specific analysis
- Comparison charts won't populate
- Can't filter by club

**Q: I have 50 old sessions. Do I need to assign all?**

A: No. Start with recent sessions. The interactive tool makes it quick:
- Shows suggestions based on distance
- Press Enter to skip unimportant ones
- Assign only what matters to you

**Q: Can I track the same club across years?**

A: Yes! Filter to "Driver" and you'll see all driver sessions regardless of date. Great for long-term tracking.

## Summary

Club tracking is **optional but powerful**. It takes ~10 seconds per session to assign:

```bash
python add_session.py today.csv --club "7 Iron"
```

In return, you get:
- ✅ Club-specific performance trends
- ✅ Compare across your bag  
- ✅ Identify which clubs need work
- ✅ Track improvement per club

Start simple: assign clubs going forward. Backfill old data when you have time.

---

**Next Steps:**
1. Try `python assign_club.py` to assign existing sessions
2. Use `python add_session.py` with `--club` for new sessions
3. Open dashboard and filter by club
4. View the club comparison chart
5. Track improvement in your weakest club!
