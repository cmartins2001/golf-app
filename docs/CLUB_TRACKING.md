# Club Tracking Guide

## Overview

Since Uneekor VIEW software doesn't track which club was used in a driving range session, this dashboard provides a flexible club metadata system. You can assign clubs to sessions either when adding new data or retroactively for existing sessions.

## Why Track Clubs?

**Club-specific analysis enables:**
- Compare 7 iron performance across multiple sessions
- Track driver consistency separately from irons
- Identify which clubs need more practice
- Set club-specific improvement goals
- Build a complete bag profile over time

## Quick Start

### Method 1: Add Session with Club (Recommended)

```bash
python add_session.py ~/Downloads/my_range_session.csv
```

You'll be prompted interactively:
```
📋 Available clubs:
   1. Driver
   2. 3 Wood
   ...
  14. 7 Iron
  ...

Select club:
  • Enter number (1-16)
  • Enter club name directly
  • Press Enter to skip (can add later)

Club: 14

📝 Session notes (optional, press Enter to skip): Working on tempo
```

### Method 2: Add Session Non-Interactively

```bash
python add_session.py ~/Downloads/session.csv \
  --date 2025-01-20 \
  --club "7 Iron" \
  --notes "Windy conditions"
```

### Method 3: Assign Club to Existing Session

```bash
# List sessions to find IDs
python manage_clubs.py list-sessions

# Assign club
python manage_clubs.py assign session_2025_01_20 "Driver"

# With notes
python manage_clubs.py assign session_2025_01_20 "Driver" -n "Testing new driver"
```

## Club Management Commands

### List Sessions and Clubs

```bash
python manage_clubs.py list-sessions
```

Output:
```
📅 Sessions:

✅ Sessions with clubs assigned:
  2025-01-13 - 7 Iron          - session_2025_01_13 - "First session"
  2025-01-20 - Driver          - session_2025_01_20

⚠️  Sessions missing club assignment:
  2025-01-27 - session_2025_01_27

💡 Assign clubs with: python manage_clubs.py assign <session_id> <club>
```

### View Available Clubs

```bash
python manage_clubs.py list-clubs
```

Output:
```
📋 Available Clubs:

Standard Clubs:
  • Driver       - wood    - ~250 yards
  • 3 Wood       - wood    - ~230 yards
  • 7 Iron       - iron    - ~155 yards
  • PW           - wedge   - ~125 yards
  ...

Total: 16 clubs
```

### View Performance by Club

```bash
python manage_clubs.py stats
```

Output:
```
📊 Club Performance Comparison:

Club            Carry    Std     Offline  Quality  Sessions   Shots
---------------------------------------------------------------------------------
Driver          245.2y   12.3y   18.5y    72%      5          85
7 Iron          152.8y   8.2y    12.1y    81%      8          142
PW              121.3y   6.5y    9.8y     85%      3          52
```

This shows aggregated performance for each club across all sessions.

### Remove Club Assignment

```bash
python manage_clubs.py remove session_2025_01_20
```

## Using Club Filter in Dashboard

Once clubs are assigned, the dashboard provides powerful filtering:

### 1. Club Dropdown Filter

At the top of the dashboard, select a club from the dropdown:
- **"All Clubs"** - Show all sessions combined
- **"7 Iron"** - Show only 7 iron sessions
- **"Driver"** - Show only driver sessions

All charts and metrics update automatically based on selection.

### 2. Club Comparison Table

Scroll to the "Club Comparison" section to see a table comparing all your clubs:
- Median carry distance
- Distance consistency (std dev)
- Directional control
- Strike quality rate
- Number of sessions
- Total shots

This helps identify:
- Which clubs are most consistent
- Which clubs need work
- Typical distances for each club
- Practice gaps in your bag

## Advanced Usage

### Add Custom Club

If you have a non-standard club (e.g., custom hybrid, adjustable driver setting):

```bash
python manage_clubs.py add-club
```

Interactive prompts:
```
➕ Add Custom Club

Club name (e.g., '4 Hybrid'): 4 Hybrid Strong Loft

Club type:
  1. Wood
  2. Hybrid
  3. Iron
  4. Wedge
Select (1-4): 2

Typical carry distance (yards): 185

Optimal launch angle range:
  Minimum (degrees): 13
  Maximum (degrees): 17

Optimal spin range:
  Minimum (RPM): 4000
  Maximum (RPM): 5000
```

Your custom club is now available in all menus and will be used for optimal launch window calculations specific to that club.

### Bulk Session Management

For retroactively adding clubs to many sessions:

```bash
# Create a simple bash script
for session in session_2025_01_*; do
  python manage_clubs.py assign ${session%.csv} "7 Iron"
done
```

### Export Club Metadata

Club assignments are stored in `data/club_metadata.json`:

```json
{
  "sessions": {
    "session_2025_01_13": "7 Iron",
    "session_2025_01_20": "Driver"
  },
  "custom_clubs": {
    "4 Hybrid Strong": {
      "type": "hybrid",
      "typical_carry": 185,
      "optimal_launch": [13, 17],
      "optimal_spin": [4000, 5000]
    }
  },
  "notes": {
    "session_2025_01_13": "First session - baseline"
  }
}
```

You can:
- Back up this file
- Edit manually (be careful with format)
- Share with others
- Version control it

## Workflow Examples

### Scenario 1: Single-Club Practice

You're working exclusively on your 7 iron for a month:

```bash
# Add each session
python add_session.py ~/Downloads/jan_15.csv -d 2025-01-15 -c "7 Iron"
python add_session.py ~/Downloads/jan_22.csv -d 2025-01-22 -c "7 Iron"
python add_session.py ~/Downloads/jan_29.csv -d 2025-01-29 -c "7 Iron"

# View progress
python manage_clubs.py stats

# In dashboard: Select "7 Iron" from dropdown to see trend
```

### Scenario 2: Full Bag Session

You hit multiple clubs in one range session - export separate CSVs:

```bash
# Export each club's shots as separate CSV from Refine
python add_session.py ~/Downloads/driver_jan_20.csv -d 2025-01-20 -c "Driver"
python add_session.py ~/Downloads/7iron_jan_20.csv -d 2025-01-20 -c "7 Iron"
python add_session.py ~/Downloads/wedges_jan_20.csv -d 2025-01-20 -c "PW"
```

Note: Session IDs will need unique dates. Consider using different times:
- `session_2025_01_20_am.csv` (requires code modification)
- Or just use sequential dates: 01-20, 01-21, 01-22

### Scenario 3: Equipment Testing

Comparing two drivers:

```bash
# Add custom clubs for each driver
python manage_clubs.py add-club
# Name: "Driver - Old"
# ...

python manage_clubs.py add-club
# Name: "Driver - New"
# ...

# Assign sessions
python manage_clubs.py assign session_2025_01_15 "Driver - Old"
python manage_clubs.py assign session_2025_01_20 "Driver - New"

# Compare in dashboard
```

## Best Practices

### 1. Consistent Naming
- Use standard club names when possible
- Stick to format: "7 Iron" not "7i" or "seven iron"
- Custom clubs: Be descriptive ("Driver 9° vs Driver 10.5°")

### 2. Regular Assignment
- Assign clubs immediately when adding sessions
- Don't let sessions pile up without clubs
- Use `list-sessions` to find unassigned sessions

### 3. Meaningful Notes
- Record practice focus: "Working on draw"
- Track conditions: "Windy, crosswind from right"
- Note equipment changes: "New shaft installed"

### 4. Club-Specific Goals
- Set different consistency targets per club
- Driver: May have higher variance (12-15 yard std dev)
- Short irons: Expect tighter dispersion (6-8 yard std dev)

### 5. Data Quality
- Only assign club if entire session was that club
- Mixed sessions: Better to split CSVs or skip club assignment
- Accuracy > completeness

## Troubleshooting

### Sessions Not Showing in Club Filter

Check assignment:
```bash
python manage_clubs.py list-sessions
```

If missing, assign:
```bash
python manage_clubs.py assign session_2025_01_20 "7 Iron"
```

Then restart dashboard.

### Club Comparison Table Empty

No clubs assigned yet. Assign at least one:
```bash
python manage_clubs.py assign session_2025_01_13 "7 Iron"
```

### Wrong Club Assigned

Remove and reassign:
```bash
python manage_clubs.py remove session_2025_01_20
python manage_clubs.py assign session_2025_01_20 "Driver"
```

### Lost Club Metadata

If `club_metadata.json` is deleted, you'll need to reassign clubs. Consider:
- Keep backups of club_metadata.json
- Version control it with git
- Document club assignments elsewhere

## Technical Details

### Where Data Lives

```
data/
├── session_2025_01_13.csv       # Shot data
├── session_2025_01_20.csv       # Shot data
└── club_metadata.json           # Club assignments (auto-created)
```

### How It Works

1. CSV files contain shot data but no club info
2. `club_metadata.json` maps session IDs → club names
3. Data processor merges club info when loading
4. Dashboard filters based on merged data

### Metadata Structure

```python
{
  "sessions": {
    "<session_id>": "<club_name>",
    ...
  },
  "custom_clubs": {
    "<club_name>": {
      "type": "<wood|hybrid|iron|wedge>",
      "typical_carry": <int>,
      "optimal_launch": [<min>, <max>],
      "optimal_spin": [<min>, <max>]
    },
    ...
  },
  "notes": {
    "<session_id>": "<notes_text>",
    ...
  }
}
```

## Future Enhancements

Potential features to add:
- Multi-club sessions (assign multiple clubs to one file)
- Club auto-detection based on distance patterns
- Import/export club profiles
- Share club standards across users
- Club recommendation based on performance

---

**Remember**: Club tracking is optional but powerful. Start simple with a single club, then expand as you see the value in club-specific analysis.
