"""
Club Assignment Interface - Dashboard Component
Interactive UI for assigning clubs to sessions
"""

import marimo as mo
import polars as pl
from typing import Dict, List, Optional


def create_club_assignment_interface(
    club_manager,
    all_session_ids: List[str],
    session_summaries: pl.DataFrame
) -> mo.Html:
    """
    Create an interactive interface for assigning clubs to sessions
    
    Args:
        club_manager: ClubManager instance
        all_session_ids: List of all available session IDs
        session_summaries: DataFrame with session metrics for suggestions
        
    Returns:
        Marimo HTML component with assignment interface
    """
    
    # Get unassigned sessions
    assignments = club_manager.metadata['sessions']
    unassigned = [sid for sid in all_session_ids if sid not in assignments]
    
    # Build session info with club assignments
    session_info = []
    for session_id in sorted(all_session_ids, reverse=True):
        # Get session stats for club suggestion
        session_data = session_summaries.filter(
            pl.col('session_id') == session_id
        )
        
        club = club_manager.get_session_club(session_id)
        notes = club_manager.get_session_notes(session_id) or ""
        
        # Suggest club based on median carry if unassigned
        suggestion = ""
        if not club and len(session_data) > 0:
            median_carry = session_data.select('median_carry').item()
            if median_carry:
                # Find closest club by typical carry
                closest_club = None
                min_diff = float('inf')
                for club_name, specs in club_manager.STANDARD_CLUBS.items():
                    diff = abs(specs['typical_carry'] - median_carry)
                    if diff < min_diff:
                        min_diff = diff
                        closest_club = club_name
                suggestion = f" (Suggested: {closest_club} based on {median_carry:.0f}yd carry)"
        
        # Format date nicely
        date_str = session_id.replace('session_', '').replace('_', '-')
        
        session_info.append({
            'session_id': session_id,
            'date': date_str,
            'club': club or "Unassigned",
            'notes': notes,
            'suggestion': suggestion,
            'has_club': club is not None
        })
    
    # Create status summary
    total = len(all_session_ids)
    assigned = len([s for s in session_info if s['has_club']])
    
    # Build HTML table
    html_parts = [
        f"""
        <div style="margin: 20px 0;">
            <h3>📋 Club Assignment Manager</h3>
            <p style="color: #666;">
                Status: <strong>{assigned}/{total} sessions assigned</strong>
            </p>
        </div>
        """
    ]
    
    if unassigned:
        html_parts.append(
            f"""
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 10px 0;">
                <strong>⚠️ {len(unassigned)} session(s) need club assignment</strong>
            </div>
            """
        )
    
    # Create table
    html_parts.append("""
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background: #2E7D32; color: white;">
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Date</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Session ID</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Club</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Notes</th>
                </tr>
            </thead>
            <tbody>
    """)
    
    for info in session_info:
        bg_color = "#f8f9fa" if info['has_club'] else "#fff3cd"
        club_display = info['club'] if info['has_club'] else f"<em>{info['club']}{info['suggestion']}</em>"
        
        html_parts.append(f"""
            <tr style="background: {bg_color};">
                <td style="padding: 10px; border: 1px solid #ddd;">{info['date']}</td>
                <td style="padding: 10px; border: 1px solid #ddd; font-family: monospace; font-size: 0.9em;">{info['session_id']}</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>{club_display}</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd; font-size: 0.9em;">{info['notes']}</td>
            </tr>
        """)
    
    html_parts.append("""
            </tbody>
        </table>
    """)
    
    # Add instructions
    html_parts.append("""
        <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 4px;">
            <h4 style="margin-top: 0;">🔧 How to Assign Clubs</h4>
            <p><strong>Option 1: Use the helper script (recommended)</strong></p>
            <pre style="background: #263238; color: #aed581; padding: 10px; border-radius: 4px; overflow-x: auto;">python assign_club.py</pre>
            <p>This interactive script will guide you through assigning clubs to all unassigned sessions.</p>
            
            <p><strong>Option 2: Manual editing</strong></p>
            <p>Edit <code>data/club_metadata.json</code> directly:</p>
            <pre style="background: #263238; color: #aed581; padding: 10px; border-radius: 4px; overflow-x: auto;">{
  "sessions": {
    "session_2025_01_20": "7 Iron",
    "session_2025_01_27": "Driver"
  },
  "notes": {
    "session_2025_01_20": "Working on consistency"
  }
}</pre>
            
            <p><strong>Available Clubs:</strong></p>
            <p style="font-size: 0.9em; color: #555;">
                Driver, 3 Wood, 5 Wood, 3 Hybrid, 4 Hybrid, 3 Iron, 4 Iron, 5 Iron, 
                6 Iron, 7 Iron, 8 Iron, 9 Iron, PW, GW, SW, LW
            </p>
            
            <p style="margin-top: 15px; font-style: italic; color: #666;">
                After assigning clubs, restart the dashboard to see club-specific analysis.
            </p>
        </div>
    """)
    
    return mo.Html("".join(html_parts))


def create_club_selector_dropdown(club_manager) -> mo.ui.dropdown:
    """Create a dropdown for selecting clubs"""
    clubs = club_manager.get_club_list()
    return mo.ui.dropdown(
        options=["All Clubs"] + clubs,
        value="All Clubs",
        label="Filter by club:"
    )
