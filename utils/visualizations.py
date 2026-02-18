"""
Golf Dashboard Visualization Utilities
Beautiful, interactive Plotly charts for tracking golf performance
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import polars as pl
from typing import Optional, Dict, List


# Color palette - clean, professional golf theme
COLORS = {
    'primary': '#2E7D32',      # Golf green
    'secondary': '#1565C0',    # Sky blue
    'accent': '#F57C00',       # Orange (current session)
    'goal': '#7B1FA2',         # Purple (goals)
    'positive': '#388E3C',     # Success green
    'negative': '#D32F2F',     # Warning red
    'neutral': '#757575',      # Gray
    'background': '#FAFAFA',   # Light background
}

# Chart template
CHART_TEMPLATE = 'plotly_white'

# Common layout settings
BASE_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=60, b=60),
    hovermode='closest',
    height=400,
)


class GolfVisualizer:
    """Create interactive visualizations for golf performance tracking"""
    
    def __init__(self, goals: Optional[Dict[str, float]] = None):
        """
        Initialize visualizer with optional goal targets
        
        Args:
            goals: Dictionary of metric names to goal values
                   e.g., {'carry_std': 10, 'quality_score': 0.85}
        """
        self.goals = goals or {}
    
    def plot_shot_scatter(
        self, 
        shot_data: pl.DataFrame,
        current_session_id: Optional[str] = None,
        title: str = "Shot Dispersion Pattern"
    ) -> go.Figure:
        """
        Create scatter plot of shot landing positions
        
        Args:
            shot_data: DataFrame with Carry and side_dist_signed columns
            current_session_id: Highlight specific session
            title: Chart title
        """
        # Convert to pandas for Plotly Express
        df = shot_data.to_pandas()
        
        # Determine color coding
        if current_session_id:
            df['session_type'] = df['session_id'].apply(
                lambda x: 'Current' if x == current_session_id else 'Historical'
            )
            color_col = 'session_type'
            color_map = {'Current': COLORS['accent'], 'Historical': COLORS['neutral']}
        else:
            color_col = 'Type'
            color_map = None
        
        fig = px.scatter(
            df,
            x='side_dist_signed',
            y='Carry',
            color=color_col,
            color_discrete_map=color_map,
            hover_data=['Ball Speed', 'Launch Angle', 'session_id'],
            title=title,
            labels={
                'side_dist_signed': 'Lateral Distance (yards)',
                'Carry': 'Carry Distance (yards)'
            }
        )
        
        # Add target circle (e.g., ±20 yards offline, ±15 yards distance)
        if self.goals:
            offline_goal = self.goals.get('max_offline', 20)
            distance_goal = self.goals.get('carry_std', 15)
            
            # Add rectangle for "fairway"
            fig.add_shape(
                type="rect",
                x0=-offline_goal, x1=offline_goal,
                y0=df['Carry'].median() - distance_goal,
                y1=df['Carry'].median() + distance_goal,
                line=dict(color=COLORS['goal'], width=2, dash='dash'),
                fillcolor=COLORS['goal'],
                opacity=0.1,
                layer='below'
            )
        
        # Add centerline
        fig.add_hline(y=0, line_dash="dot", line_color=COLORS['neutral'], opacity=0.5)
        fig.add_vline(x=0, line_dash="dot", line_color=COLORS['neutral'], opacity=0.5)
        
        fig.update_layout(**BASE_LAYOUT, height=500)
        fig.update_xaxis(zeroline=True, zerolinewidth=1, zerolinecolor=COLORS['neutral'])
        fig.update_yaxis(zeroline=False)
        
        return fig
    
    def plot_metric_trend(
        self,
        trend_data: pl.DataFrame,
        metric: str,
        metric_label: str,
        lower_is_better: bool = False,
        goal_value: Optional[float] = None
    ) -> go.Figure:
        """
        Create time series trend chart with rolling average
        
        Args:
            trend_data: DataFrame with session_date and metric columns
            metric: Column name to plot
            metric_label: Display label for metric
            lower_is_better: Whether lower values are better
            goal_value: Target value to display as reference line
        """
        df = trend_data.to_pandas()
        
        fig = go.Figure()
        
        # Individual session values
        fig.add_trace(go.Scatter(
            x=df['session_date'],
            y=df[metric],
            mode='markers',
            name='Session',
            marker=dict(size=10, color=COLORS['secondary'], opacity=0.6),
            hovertemplate='<b>%{x|%b %d}</b><br>' + metric_label + ': %{y:.2f}<extra></extra>'
        ))
        
        # Trend line
        if f"{metric}_trend" in df.columns:
            fig.add_trace(go.Scatter(
                x=df['session_date'],
                y=df[f"{metric}_trend"],
                mode='lines',
                name='Trend (3-session avg)',
                line=dict(color=COLORS['primary'], width=3),
                hovertemplate='<b>%{x|%b %d}</b><br>Trend: %{y:.2f}<extra></extra>'
            ))
        
        # Goal line
        if goal_value is not None:
            fig.add_hline(
                y=goal_value,
                line_dash="dash",
                line_color=COLORS['goal'],
                annotation_text=f"Goal: {goal_value:.2f}",
                annotation_position="right"
            )
        elif metric in self.goals:
            goal_val = self.goals[metric]
            fig.add_hline(
                y=goal_val,
                line_dash="dash",
                line_color=COLORS['goal'],
                annotation_text=f"Goal: {goal_val:.2f}",
                annotation_position="right"
            )
        
        fig.update_layout(
            **BASE_LAYOUT,
            title=f"{metric_label} Over Time",
            xaxis_title="Session Date",
            yaxis_title=metric_label,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def plot_performance_radar(
        self,
        current_stats: pl.DataFrame,
        historical_avg: pl.DataFrame,
        metrics: List[str] = None
    ) -> go.Figure:
        """
        Create radar chart comparing current session to historical average
        
        Args:
            current_stats: Current session summary stats
            historical_avg: Average of all historical sessions
            metrics: List of metrics to include (uses defaults if None)
        """
        if metrics is None:
            metrics = [
                'strike_quality_rate',
                'optimal_launch_rate', 
                'quality_score',
                'straight_rate'
            ]
        
        labels = {
            'strike_quality_rate': 'Strike Quality',
            'optimal_launch_rate': 'Launch Window',
            'quality_score': 'Overall Quality',
            'straight_rate': 'Straight Shots'
        }
        
        current = current_stats.to_dicts()[0]
        historical = historical_avg.to_dicts()[0]
        
        fig = go.Figure()
        
        # Historical average
        fig.add_trace(go.Scatterpolar(
            r=[historical.get(m, 0) * 100 for m in metrics],
            theta=[labels.get(m, m) for m in metrics],
            fill='toself',
            name='Historical Avg',
            line_color=COLORS['neutral'],
            fillcolor=COLORS['neutral'],
            opacity=0.3
        ))
        
        # Current session
        fig.add_trace(go.Scatterpolar(
            r=[current.get(m, 0) * 100 for m in metrics],
            theta=[labels.get(m, m) for m in metrics],
            fill='toself',
            name='Current Session',
            line_color=COLORS['accent'],
            fillcolor=COLORS['accent'],
            opacity=0.5
        ))
        
        # Goals
        if any(m in self.goals for m in metrics):
            goal_values = [self.goals.get(m, historical.get(m, 0)) * 100 for m in metrics]
            fig.add_trace(go.Scatterpolar(
                r=goal_values,
                theta=[labels.get(m, m) for m in metrics],
                mode='lines',
                name='Goals',
                line=dict(color=COLORS['goal'], width=2, dash='dash')
            ))
        
        fig.update_layout(
            **BASE_LAYOUT,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=True),
                angularaxis=dict(direction="clockwise")
            ),
            showlegend=True,
            title="Performance Comparison",
            height=450
        )
        
        return fig
    
    def plot_consistency_dashboard(
        self,
        summary: pl.DataFrame,
        current_session_id: str
    ) -> go.Figure:
        """
        Create multi-metric consistency dashboard with small multiples
        
        Args:
            summary: Session summary DataFrame
            current_session_id: ID of current session to highlight
        """
        df = summary.to_pandas()
        current_idx = df[df['session_id'] == current_session_id].index[0] if current_session_id in df['session_id'].values else -1
        
        # Create 2x2 subplot grid
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Distance Consistency', 
                'Directional Control',
                'Strike Quality',
                'Shot Shape Quality'
            ),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Distance consistency (lower is better)
        fig.add_trace(
            go.Bar(
                x=df['session_date'],
                y=df['carry_std'],
                marker_color=[COLORS['accent'] if i == current_idx else COLORS['secondary'] for i in range(len(df))],
                showlegend=False,
                hovertemplate='%{x|%b %d}<br>Std Dev: %{y:.1f} yds<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Directional control (lower is better)
        fig.add_trace(
            go.Bar(
                x=df['session_date'],
                y=df['directional_std'],
                marker_color=[COLORS['accent'] if i == current_idx else COLORS['secondary'] for i in range(len(df))],
                showlegend=False,
                hovertemplate='%{x|%b %d}<br>Std Dev: %{y:.1f} yds<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Strike quality (higher is better)
        fig.add_trace(
            go.Bar(
                x=df['session_date'],
                y=df['strike_quality_rate'] * 100,
                marker_color=[COLORS['accent'] if i == current_idx else COLORS['positive'] for i in range(len(df))],
                showlegend=False,
                hovertemplate='%{x|%b %d}<br>Quality: %{y:.1f}%<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Shot shape (higher is better)
        fig.add_trace(
            go.Bar(
                x=df['session_date'],
                y=df['straight_rate'] * 100,
                marker_color=[COLORS['accent'] if i == current_idx else COLORS['positive'] for i in range(len(df))],
                showlegend=False,
                hovertemplate='%{x|%b %d}<br>Straight: %{y:.1f}%<extra></extra>'
            ),
            row=2, col=2
        )
        
        # Update axes
        fig.update_xaxes(title_text="Session Date", row=2, col=1)
        fig.update_xaxes(title_text="Session Date", row=2, col=2)
        fig.update_yaxes(title_text="Std Dev (yards)", row=1, col=1)
        fig.update_yaxes(title_text="Std Dev (yards)", row=1, col=2)
        fig.update_yaxes(title_text="Quality Rate (%)", row=2, col=1)
        fig.update_yaxes(title_text="Straight Rate (%)", row=2, col=2)
        
        fig.update_layout(
            height=600,
            title_text="Consistency Metrics Dashboard",
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=60, r=40, t=80, b=60),
        )
        
        return fig
    
    def create_summary_table(
        self,
        current: pl.DataFrame,
        historical: pl.DataFrame,
        goals: Optional[Dict[str, float]] = None
    ) -> go.Figure:
        """
        Create comparison table: Current vs Historical vs Goals
        
        Args:
            current: Current session stats
            historical: Historical average stats
            goals: Goal values for each metric
        """
        goals = goals or self.goals
        
        curr_dict = current.to_dicts()[0]
        hist_dict = historical.to_dicts()[0]
        
        metrics = [
            ('Median Carry', 'median_carry', 'yards', False),
            ('Distance Std Dev', 'carry_std', 'yards', True),
            ('Avg Offline', 'avg_offline', 'yards', True),
            ('Strike Quality', 'strike_quality_rate', '%', False),
            ('Optimal Launch', 'optimal_launch_rate', '%', False),
            ('Quality Score', 'quality_score', '', False),
        ]
        
        rows = []
        for label, key, unit, lower_better in metrics:
            curr_val = curr_dict.get(key, 0)
            hist_val = hist_dict.get(key, 0)
            goal_val = goals.get(key, None)
            
            # Format values
            if unit == '%':
                curr_str = f"{curr_val*100:.1f}%"
                hist_str = f"{hist_val*100:.1f}%"
                goal_str = f"{goal_val*100:.1f}%" if goal_val else "--"
            elif unit == '':
                curr_str = f"{curr_val:.3f}"
                hist_str = f"{hist_val:.3f}"
                goal_str = f"{goal_val:.3f}" if goal_val else "--"
            else:
                curr_str = f"{curr_val:.1f}"
                hist_str = f"{hist_val:.1f}"
                goal_str = f"{goal_val:.1f}" if goal_val else "--"
            
            # Determine if improving
            if lower_better:
                improving = curr_val < hist_val
            else:
                improving = curr_val > hist_val
            
            trend_emoji = "✓" if improving else "→"
            
            rows.append([label, curr_str, hist_str, goal_str, trend_emoji])
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Metric</b>', '<b>Current</b>', '<b>Historical Avg</b>', '<b>Goal</b>', '<b>Trend</b>'],
                fill_color=COLORS['primary'],
                font=dict(color='white', size=13),
                align='left',
                height=35
            ),
            cells=dict(
                values=list(zip(*rows)),
                fill_color=['white', COLORS['background'], 'white', COLORS['background'], 'white'],
                align='left',
                font=dict(size=12),
                height=30
            )
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            title="Performance Summary"
        )
        
        return fig
    
    def plot_club_comparison(self, club_comparison: pl.DataFrame) -> go.Figure:
        """
        Create comparison chart showing performance across different clubs
        
        Args:
            club_comparison: DataFrame with club-level aggregated metrics
            
        Returns:
            Plotly figure with club comparison
        """
        df = club_comparison.to_pandas()
        
        if len(df) == 0:
            # Return empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="No club data available. Assign clubs to sessions to see comparison.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color=COLORS['neutral'])
            )
            fig.update_layout(**BASE_LAYOUT, height=400)
            return fig
        
        # Create subplots: Distance and Consistency
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Distance by Club', 'Consistency by Club'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Distance chart
        fig.add_trace(
            go.Bar(
                x=df['club'],
                y=df['median_carry'],
                name='Median Carry',
                marker_color=COLORS['primary'],
                text=df['median_carry'].round(1),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Carry: %{y:.1f} yds<br>Sessions: %{customdata}<extra></extra>',
                customdata=df['num_sessions']
            ),
            row=1, col=1
        )
        
        # Consistency chart (lower is better, so invert for visual)
        fig.add_trace(
            go.Bar(
                x=df['club'],
                y=df['carry_std'],
                name='Distance Std Dev',
                marker_color=COLORS['secondary'],
                text=df['carry_std'].round(1),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Std Dev: %{y:.1f} yds<br>Total Shots: %{customdata}<extra></extra>',
                customdata=df['total_shots']
            ),
            row=1, col=2
        )
        
        # Update axes
        fig.update_xaxes(title_text="Club", row=1, col=1)
        fig.update_xaxes(title_text="Club", row=1, col=2)
        fig.update_yaxes(title_text="Carry Distance (yards)", row=1, col=1)
        fig.update_yaxes(title_text="Std Deviation (yards)", row=1, col=2)
        
        fig.update_layout(
            height=450,
            title_text="Club Performance Comparison",
            showlegend=False,
            font=dict(family="Inter, sans-serif"),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=60, r=40, t=80, b=60),
        )
        
        return fig

