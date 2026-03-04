"""
Golf Performance Dashboard
Interactive marimo notebook for tracking launch monitor data over time
"""

import marimo

__generated_with = "0.19.7"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from pathlib import Path
    import sys

    # Add utils to path
    sys.path.insert(0, str(Path.cwd()))

    from utils.data_processor import GolfDataProcessor
    from utils.visualizations import GolfVisualizer, COLORS
    from utils.club_manager import ClubManager

    return GolfDataProcessor, GolfVisualizer, mo, pl


@app.cell
def _(mo):
    """Dashboard Header and Configuration"""
    mo.md(
        """
        # ⛳ Golf Performance Dashboard

        Track your launch monitor data across sessions with beautiful visualizations.
        **Current focus:** Distance consistency, directional control, and strike quality.
        """
    )
    return


@app.cell
def _(mo):
    """Goal Configuration Interface"""
    mo.md("## 🎯 Set Your Goals")

    # Goal sliders for key metrics
    carry_std_goal = mo.ui.slider(
        start=5, stop=20, value=12, step=0.5,
        label="Distance Consistency Goal (std dev in yards):",
        show_value=True
    )

    directional_std_goal = mo.ui.slider(
        start=5, stop=30, value=15, step=1,
        label="Directional Consistency Goal (std dev in yards):",
        show_value=True
    )

    quality_score_goal = mo.ui.slider(
        start=0.5, stop=1.0, value=0.80, step=0.05,
        label="Quality Score Goal:",
        show_value=True
    )

    strike_quality_goal = mo.ui.slider(
        start=0.3, stop=1.0, value=0.70, step=0.05,
        label="Strike Quality Rate Goal:",
        show_value=True
    )

    mo.hstack([
        mo.vstack([carry_std_goal, directional_std_goal]),
        mo.vstack([quality_score_goal, strike_quality_goal])
    ])
    return (
        carry_std_goal,
        directional_std_goal,
        quality_score_goal,
        strike_quality_goal,
    )


@app.cell
def _(
    carry_std_goal,
    directional_std_goal,
    quality_score_goal,
    strike_quality_goal,
):
    """Compile goals dictionary"""
    goals = {
        'carry_std': carry_std_goal.value,
        'directional_std': directional_std_goal.value,
        'quality_score': quality_score_goal.value,
        'strike_quality_rate': strike_quality_goal.value,
        'max_offline': 20,  # Fixed for now
    }
    return (goals,)


@app.cell
def _(GolfDataProcessor, GolfVisualizer, goals, mo):
    """Load and Process Data"""
    mo.md("## 📊 Loading Session Data...")

    try:
        processor = GolfDataProcessor(data_dir="data")
        df = processor.load_sessions()

        # Get summaries
        summary = processor.get_session_summary()
        latest_session = processor.get_latest_session_id()

        # Get club information
        all_clubs = processor.get_all_clubs()
        missing_clubs = processor.get_sessions_without_clubs()

        # Initialize visualizer with goals
        viz = GolfVisualizer(goals=goals)

        status_msg = f"✅ **Loaded {summary.height} sessions** | Latest: `{latest_session}`"
        if missing_clubs:
            status_msg += f"\n\n⚠️ **{len(missing_clubs)} sessions missing club assignment** - Use `python manage_clubs.py assign <session_id> <club>` to add"

        mo.md(status_msg)

    except FileNotFoundError as e:
        mo.md(f"⚠️ **Error:** {e}")
        mo.md("Place your session CSV files in the `data/` directory with format: `session_YYYY_MM_DD.csv`")
        raise

    return all_clubs, latest_session, processor, summary, viz


@app.cell
def _(mo, processor, summary):
    """Club Assignment Interface"""
    from utils.club_interface import create_club_assignment_interface

    # Get all session IDs
    all_session_ids = summary.select('session_id').to_series().to_list()

    # Create assignment interface
    assignment_ui = create_club_assignment_interface(
        processor.club_manager,
        all_session_ids,
        summary
    )

    mo.accordion({
        "🏌️ Manage Club Assignments": assignment_ui
    })
    return


@app.cell
def _(all_clubs, mo):
    """Club Filter Selector"""
    mo.md("## 🏌️ Filter by Club")

    # Create dropdown for club selection
    club_options = ["All Clubs"] + all_clubs

    club_selector = mo.ui.dropdown(
        options=club_options,
        value="All Clubs",
        label="Select club to analyze:"
    )

    club_selector
    return (club_selector,)


@app.cell
def _(club_selector):
    """Get selected club (None if 'All Clubs')"""
    selected_club = None if club_selector.value == "All Clubs" else club_selector.value
    return (selected_club,)


@app.cell
def _(processor, selected_club):
    """Display data preview"""
    summary_filtered = processor.get_session_summary(club=selected_club)
    summary_filtered.head()
    return (summary_filtered,)


@app.cell
def _(mo):
    """Performance Overview Section"""
    mo.md(
        """
        ---
        ## 📈 Performance Overview

        Compare your current session against historical averages and goals.
        """
    )
    return


@app.cell
def _(latest_session, pl, summary_filtered, viz):
    """Summary Comparison Table"""
    current_stats = summary_filtered.filter(summary_filtered['session_id'] == latest_session)

    # Calculate historical average (excluding current)
    historical_stats = summary_filtered.filter(summary_filtered['session_id'] != latest_session).select([
        summary_filtered.select(pl.selectors.by_dtype(pl.Float64)).mean(),
    ])

    table_fig = viz.create_summary_table(current_stats, historical_stats)
    table_fig
    return current_stats, historical_stats


@app.cell
def _(current_stats, historical_stats, viz):
    """Performance Radar Chart"""
    radar_fig = viz.plot_performance_radar(
        current_stats, 
        historical_stats,
        metrics=['strike_quality_rate', 'optimal_launch_rate', 'quality_score', 'straight_rate']
    )
    radar_fig
    return


@app.cell
def _(mo):
    """Consistency Metrics Section"""
    mo.md(
        """
        ---
        ## 🎯 Consistency Metrics

        Track the key indicators of improving ball striking: distance control, directional control, and quality contact.
        """
    )
    return


@app.cell
def _(latest_session, summary_filtered, viz):
    """Consistency Dashboard - Small Multiples"""
    consistency_fig = viz.plot_consistency_dashboard(summary_filtered, latest_session)
    consistency_fig
    return


@app.cell
def _(mo):
    """Trend Analysis Section"""
    mo.md(
        """
        ---
        ## 📉 Trends Over Time

        Identify long-term patterns and improvement trajectories.
        """
    )
    return


@app.cell
def _(processor, selected_club, viz):
    """Distance Consistency Trend"""
    carry_trend = processor.calculate_trend('carry_std', window=3, club=selected_club)

    carry_trend_fig = viz.plot_metric_trend(
        carry_trend,
        metric='carry_std',
        metric_label='Distance Std Dev (yards)',
        lower_is_better=True
    )
    carry_trend_fig
    return


@app.cell
def _(processor, selected_club, viz):
    """Quality Score Trend"""
    quality_trend = processor.calculate_trend('quality_score', window=3, club=selected_club)

    quality_trend_fig = viz.plot_metric_trend(
        quality_trend,
        metric='quality_score',
        metric_label='Composite Quality Score',
        lower_is_better=False
    )
    quality_trend_fig
    return


@app.cell
def _(mo):
    """Shot Pattern Analysis Section"""
    mo.md(
        """
        ---
        ## 🎪 Shot Dispersion Pattern

        Visualize where your shots are landing relative to target.
        """
    )
    return


@app.cell
def _(mo):
    """Session selector for shot pattern"""
    session_toggle = mo.ui.radio(
        options=['current', 'all'],
        value='current',
        label="Show shots from:"
    )

    mo.hstack([
        mo.md("**Display:**"),
        session_toggle
    ])
    return (session_toggle,)


@app.cell
def _(latest_session, processor, selected_club, session_toggle, viz):
    """Shot Scatter Plot"""
    shots = processor.get_shot_distribution(club=selected_club)

    if session_toggle.value == 'current':
        scatter_fig = viz.plot_shot_scatter(
            shots,
            current_session_id=latest_session,
            title="Shot Dispersion - Current vs Historical"
        )
    else:
        scatter_fig = viz.plot_shot_scatter(
            shots,
            title="Shot Dispersion - All Sessions"
        )

    scatter_fig
    return


@app.cell
def _(mo):
    """Club Comparison Section"""
    mo.md(
        """
        ---
        ## 📊 Club Comparison

        Compare performance across different clubs (only shows clubs with assigned sessions).
        """
    )
    return


@app.cell
def _(all_clubs, mo, processor):
    """Club Comparison Table"""
    if all_clubs:
        club_comparison = processor.get_club_comparison()
        club_comparison
    else:
        mo.md("⚠️ No clubs assigned yet. Use `python manage_clubs.py assign <session_id> <club>` to add club metadata.")
    return


@app.cell
def _(mo):
    """Club Comparison Section"""
    mo.md(
        """
        ---
        ## 🏌️ Club Performance Comparison

        Compare your performance across different clubs to identify strengths and opportunities.
        """
    )
    return


@app.cell
def _(mo, processor, viz):
    """Club Comparison Chart"""
    try:
        club_comp = processor.get_club_comparison()
        club_comp_fig = viz.plot_club_comparison(club_comp)
        club_comp_fig
    except Exception as e:
        mo.md(f"⚠️ Club comparison unavailable. Assign clubs to sessions to enable this feature.")
    return


@app.cell
def _(mo):
    """Data Management Section"""
    mo.md(
        """
        ---
        ## 💾 Data Management

        ### Adding New Sessions with Club Tracking

        **Easy Method (Recommended):**
        ```bash
        python add_session.py ~/Downloads/refine_export.csv
        # Follow prompts to select club and add notes
        ```

        **Manual Method:**
        1. Export your range session from Refine software as CSV
        2. Rename file to format: `session_YYYY_MM_DD.csv` (e.g., `session_2025_01_20.csv`)
        3. Place file in the `data/` directory
        4. Assign club: `python manage_clubs.py assign session_2025_01_20 "7 Iron"`
        5. Restart this notebook to load the new session

        ### Managing Club Metadata

        ```bash
        # List all sessions and their clubs
        python manage_clubs.py list-sessions

        # Assign club to existing session
        python manage_clubs.py assign session_2025_01_20 "Driver"

        # View performance stats by club
        python manage_clubs.py stats

        # List available clubs
        python manage_clubs.py list-clubs
        ```

        ### Current Data Directory

        ```
        golf_dashboard/
        ├── data/
        │   ├── session_2025_01_13.csv
        │   ├── session_2025_01_20.csv  ← Add new files here
        │   ├── club_metadata.json       ← Club assignments (auto-created)
        │   └── ...
        ├── utils/
        ├── dashboard.py (this file)
        ├── add_session.py (helper script)
        └── manage_clubs.py (club management)
        ```

        ### Troubleshooting

        - **Missing metrics?** Ensure your CSV has the standard Refine column headers
        - **Processing errors?** Check that files follow the naming convention
        - **Want to exclude a session?** Move the file out of the `data/` directory
        - **Missing club data?** Sessions without clubs show ⚠️ warning - use manage_clubs.py to assign
        """
    )
    return


@app.cell
def _(mo):
    """Footer"""
    mo.md(
        """
        ---

        <div style="text-align: center; color: #757575; font-size: 0.9em;">
        Built with <a href="https://marimo.io" target="_blank">marimo</a> 🌊 | 
        Data from Uneekor Launch Monitor
        </div>
        """
    )
    return


if __name__ == "__main__":
    app.run()
