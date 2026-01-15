"""
Golf Performance Dashboard
Interactive marimo notebook for tracking launch monitor data over time
"""

import marimo

__generated_with = "0.19.2"
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

        # Initialize visualizer with goals
        viz = GolfVisualizer(goals=goals)

        mo.md(f"✅ **Loaded {summary.height} sessions** | Latest: `{latest_session}`")

    except FileNotFoundError as e:
        mo.md(f"⚠️ **Error:** {e}")
        mo.md("Place your session CSV files in the `data/` directory with format: `session_YYYY_MM_DD.csv`")
        raise
    return latest_session, processor, summary, viz


@app.cell
def _(summary):
    """Display data preview"""
    summary.head()
    return


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
def _(summary):
    summary
    return


@app.cell
def _(latest_session, pl, summary, viz):
    """Summary Comparison Table"""
    current_stats = summary.filter(summary['session_id'] == latest_session)

    # Calculate historical average (excluding current)
    historical_stats = (
        summary
        .filter(summary['session_id'] != latest_session)
        # .select([
        #     summary
        #     .select(pl.selectors.by_dtype(pl.Float64)).mean(),
        # ])
        .select(pl.selectors.by_dtype(pl.Float64)).mean()
    )

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
def _(latest_session, summary, viz):
    """Consistency Dashboard - Small Multiples"""
    consistency_fig = viz.plot_consistency_dashboard(summary, latest_session)
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
def _(processor, viz):
    """Distance Consistency Trend"""
    carry_trend = processor.calculate_trend('carry_std', window=3)

    carry_trend_fig = viz.plot_metric_trend(
        carry_trend,
        metric='carry_std',
        metric_label='Distance Std Dev (yards)',
        lower_is_better=True
    )
    carry_trend_fig
    return


@app.cell
def _(processor, viz):
    """Quality Score Trend"""
    quality_trend = processor.calculate_trend('quality_score', window=3)

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
def _(latest_session, processor, session_toggle, viz):
    """Shot Scatter Plot"""
    shots = processor.get_shot_distribution()

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
    """Data Management Section"""
    mo.md(
        """
        ---
        ## 💾 Data Management

        ### Adding New Sessions

        1. Export your range session from Refine software as CSV
        2. Rename file to format: `session_YYYY_MM_DD.csv` (e.g., `session_2025_01_20.csv`)
        3. Place file in the `data/` directory
        4. Restart this notebook to load the new session

        ### Current Data Directory

        ```
        golf_dashboard/
        ├── data/
        │   ├── session_2025_01_13.csv
        │   ├── session_2025_01_20.csv  ← Add new files here
        │   └── ...
        ├── utils/
        └── dashboard.py (this file)
        ```

        ### Troubleshooting

        - **Missing metrics?** Ensure your CSV has the standard Refine column headers
        - **Processing errors?** Check that files follow the naming convention
        - **Want to exclude a session?** Move the file out of the `data/` directory
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
