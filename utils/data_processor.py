"""
Golf Launch Monitor Data Processing Utilities
Handles data loading, cleaning, and metric calculation for Uneekor Refine sessions
"""

import polars as pl
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from .club_manager import ClubManager


class GolfDataProcessor:
    """Process and aggregate golf launch monitor data across sessions"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.df: Optional[pl.DataFrame] = None
        self.club_manager = ClubManager()
        
    def load_sessions(self, pattern: str = "session_*.csv") -> pl.DataFrame:
        """
        Load and concatenate all session CSV files with club metadata
        
        Args:
            pattern: Glob pattern for session files (default: session_*.csv)
            
        Returns:
            Combined DataFrame with all sessions including club information
        """
        csv_files = list(self.data_dir.glob(pattern))
        
        if not csv_files:
            raise FileNotFoundError(f"No files matching '{pattern}' in {self.data_dir}")
        
        # Load and concatenate with session metadata
        dfs = []
        for file_path in sorted(csv_files):
            df = pl.read_csv(file_path)
            # Extract date from filename (format: session_YYYY_MM_DD.csv)
            date_str = file_path.stem.replace("session_", "")
            session_date = datetime.strptime(date_str, "%Y_%m_%d")
            session_id = file_path.stem
            
            # Get club metadata
            club = self.club_manager.get_session_club(session_id)
            notes = self.club_manager.get_session_notes(session_id) or ""
            
            df = df.with_columns([
                pl.lit(session_date).alias("session_date"),
                pl.lit(session_id).alias("session_id"),
                pl.lit(club).alias("club"),
                pl.lit(notes).alias("session_notes")
            ])
            dfs.append(df)
        
        self.df = pl.concat(dfs)
        return self._clean_and_enrich()
    
    def _clean_and_enrich(self) -> pl.DataFrame:
        """Clean data and add derived metrics"""
        
        df = self.df.with_columns([
            # Parse numeric fields (handle '--' as null)
            pl.col("Smash Factor").str.replace("--", "").cast(pl.Float64, strict=False),
            pl.col("Club Speed").str.replace("--", "").cast(pl.Float64, strict=False),
            
            # Parse angles (remove degree symbols)
            pl.col("Launch Angle").str.replace("°", "").cast(pl.Float64, strict=False),
            pl.col("Side Angle").str.replace("°", "").cast(pl.Float64, strict=False),
            
            # Parse side distance with direction
            pl.when(pl.col("Side Dist").str.contains("R"))
              .then(pl.col("Side Dist").str.extract(r"(\d+\.?\d*)", 1).cast(pl.Float64))
              .when(pl.col("Side Dist").str.contains("L"))
              .then(-pl.col("Side Dist").str.extract(r"(\d+\.?\d*)", 1).cast(pl.Float64))
              .otherwise(0.0)
              .alias("side_dist_signed"),
            
            # Flight time to seconds
            pl.col("Flight Time").str.replace(" s", "").cast(pl.Float64, strict=False).alias("flight_time_sec"),
        ])
        
        # Add shot quality flags
        df = df.with_columns([
            # Valid shot: >50 yards carry, reasonable ball speed
            ((pl.col("Carry") > 50) & (pl.col("Ball Speed") > 60)).alias("valid_shot"),
            
            # Quality strike: good smash factor
            (pl.col("Smash Factor") > 1.25).alias("quality_strike"),
            
            # Mishit: very short distance
            (pl.col("Carry") < 30).alias("mishit"),
            
            # Optimal launch window (adjust these based on your clubs)
            (
                pl.col("Launch Angle").is_between(12, 18) & 
                pl.col("Back Spin").is_between(2000, 4000)
            ).alias("optimal_launch"),
        ])
        
        self.df = df
        return df
    
    def get_session_summary(self, session_id: Optional[str] = None, club: Optional[str] = None) -> pl.DataFrame:
        """
        Calculate summary statistics for a session or all sessions
        
        Args:
            session_id: Specific session to analyze (None = all sessions)
            club: Filter to specific club (None = all clubs)
            
        Returns:
            DataFrame with aggregated metrics
        """
        df = self.df
        if session_id:
            df = df.filter(pl.col("session_id") == session_id)
        if club:
            df = df.filter(pl.col("club") == club)
        
        # Filter to valid shots for statistics
        valid_df = df.filter(pl.col("valid_shot"))
        
        summary = valid_df.group_by("session_id", "session_date", "club").agg([
            # Distance metrics
            pl.col("Carry").median().alias("median_carry"),
            pl.col("Carry").std().alias("carry_std"),
            pl.col("Total").median().alias("median_total"),
            
            # Directional metrics
            pl.col("side_dist_signed").abs().mean().alias("avg_offline"),
            pl.col("side_dist_signed").std().alias("directional_std"),
            
            # Strike quality
            (pl.col("quality_strike").sum() / pl.len()).alias("strike_quality_rate"),
            pl.col("Smash Factor").mean().alias("avg_smash"),
            
            # Launch metrics
            pl.col("Ball Speed").mean().alias("avg_ball_speed"),
            pl.col("Launch Angle").mean().alias("avg_launch_angle"),
            pl.col("Back Spin").mean().alias("avg_backspin"),
            
            # Shot shape distribution
            (pl.col("Type").str.contains("Slice").sum() / pl.len()).alias("slice_rate"),
            (pl.col("Type").str.contains("Hook").sum() / pl.len()).alias("hook_rate"),
            (pl.col("Type").str.contains("Straight").sum() / pl.len()).alias("straight_rate"),
            
            # Quality metrics
            (pl.col("optimal_launch").sum() / pl.len()).alias("optimal_launch_rate"),
            pl.len().alias("valid_shots"),
        ])
        
        # Add composite quality score
        summary = summary.with_columns([
            (
                (1 - pl.col("carry_std") / 100) * 0.3 +  # Distance consistency
                (1 - pl.col("directional_std") / 100) * 0.3 +  # Direction consistency  
                pl.col("strike_quality_rate") * 0.2 +  # Strike quality
                (1 - (pl.col("slice_rate") + pl.col("hook_rate"))) * 0.2  # Shot shape
            ).clip(0, 1).alias("quality_score")
        ])
        
        return summary.sort("session_date")
    
    def get_latest_session_id(self) -> str:
        """Get the most recent session ID"""
        return self.df.select(pl.col("session_id")).unique().sort().tail(1).item()
    
    def get_shot_distribution(self, session_id: Optional[str] = None, club: Optional[str] = None) -> pl.DataFrame:
        """Get shot pattern distribution for scatter plots"""
        df = self.df.filter(pl.col("valid_shot"))
        if session_id:
            df = df.filter(pl.col("session_id") == session_id)
        if club:
            df = df.filter(pl.col("club") == club)
        
        return df.select([
            "Carry",
            "side_dist_signed",
            "Type",
            "Ball Speed",
            "Launch Angle",
            "session_id",
            "session_date",
            "club"
        ])
    
    def calculate_trend(self, metric: str, window: int = 3, club: Optional[str] = None) -> pl.DataFrame:
        """
        Calculate rolling average trend for a metric
        
        Args:
            metric: Column name to trend
            window: Number of sessions for rolling average
            club: Filter to specific club (None = all clubs)
            
        Returns:
            DataFrame with trend data
        """
        summary = self.get_session_summary(club=club)
        
        trend = summary.select([
            "session_date",
            "session_id",
            "club",
            pl.col(metric),
            pl.col(metric).rolling_mean(window_size=window).alias(f"{metric}_trend")
        ])
        
        return trend
    
    def get_all_clubs(self) -> List[str]:
        """Get list of all clubs used in loaded sessions"""
        return sorted([c for c in self.df.select(pl.col("club")).unique().to_series().to_list() if c is not None])
    
    def get_club_comparison(self) -> pl.DataFrame:
        """
        Generate comparison statistics across all clubs
        
        Returns:
            DataFrame with key metrics aggregated by club
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_sessions() first.")
        
        valid_df = self.df.filter(pl.col("valid_shot") & pl.col("club").is_not_null())
        
        comparison = valid_df.group_by("club").agg([
            pl.col("Carry").median().alias("median_carry"),
            pl.col("Carry").std().alias("carry_std"),
            pl.col("side_dist_signed").abs().mean().alias("avg_offline"),
            pl.col("side_dist_signed").std().alias("directional_std"),
            (pl.col("quality_strike").sum() / pl.len()).alias("strike_quality_rate"),
            pl.col("Ball Speed").mean().alias("avg_ball_speed"),
            pl.len().alias("total_shots"),
            pl.col("session_id").n_unique().alias("num_sessions")
        ])
        
        return comparison.sort("median_carry", descending=True)
    
    def get_sessions_without_clubs(self) -> List[str]:
        """Get list of session IDs that don't have club metadata"""
        sessions = self.df.select(["session_id", "club"]).unique()
        missing = sessions.filter(pl.col("club").is_null())
        return missing.select(pl.col("session_id")).to_series().to_list()
