#!/usr/bin/env python3
"""
Interactive Club Assignment Tool
Easily assign clubs to your golf sessions with guided prompts and smart suggestions
"""

import sys
from pathlib import Path
import polars as pl

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.club_manager import ClubManager
from utils.data_processor import GolfDataProcessor


def print_header():
    """Print a nice header"""
    print("\n" + "="*70)
    print("🏌️  GOLF CLUB ASSIGNMENT TOOL")
    print("="*70 + "\n")


def print_club_list(club_manager: ClubManager):
    """Display available clubs in a nice format"""
    clubs = club_manager.get_club_list()
    
    print("Available Clubs:")
    print("-" * 50)
    
    # Group by type
    woods = [c for c in clubs if 'Wood' in c or c == 'Driver']
    hybrids = [c for c in clubs if 'Hybrid' in c]
    irons = [c for c in clubs if 'Iron' in c]
    wedges = ['PW', 'GW', 'SW', 'LW']
    
    if woods:
        print(f"  Woods:   {', '.join(woods)}")
    if hybrids:
        print(f"  Hybrids: {', '.join(hybrids)}")
    if irons:
        print(f"  Irons:   {', '.join(irons)}")
    if wedges:
        print(f"  Wedges:  {', '.join(wedges)}")
    
    print("-" * 50)


def suggest_club(avg_carry: float, club_manager: ClubManager) -> str:
    """Suggest a club based on average carry distance"""
    best_match = None
    min_diff = float('inf')
    
    for club_name, specs in club_manager.STANDARD_CLUBS.items():
        diff = abs(specs['typical_carry'] - avg_carry)
        if diff < min_diff:
            min_diff = diff
            best_match = club_name
    
    return best_match


def assign_session(
    session_id: str,
    session_date: str,
    avg_carry: float,
    club_manager: ClubManager
) -> tuple:
    """
    Prompt user to assign a club to a session
    
    Returns:
        (club, notes) tuple
    """
    print(f"\n📅 Session: {session_date} ({session_id})")
    
    if avg_carry:
        suggestion = suggest_club(avg_carry, club_manager)
        print(f"   Average carry: {avg_carry:.1f} yards")
        print(f"   💡 Suggested club: {suggestion}")
    
    # Get club input
    while True:
        club_input = input("\nEnter club name (or 'skip' to skip, 'list' to see clubs, 'quit' to exit): ").strip()
        
        if club_input.lower() == 'quit':
            return None, None
        
        if club_input.lower() == 'skip':
            print("   ⏭️  Skipping this session")
            return "SKIP", None
        
        if club_input.lower() == 'list':
            print()
            print_club_list(club_manager)
            continue
        
        # Validate club
        if club_input in club_manager.get_club_list():
            break
        else:
            print(f"   ❌ Unknown club: '{club_input}'")
            print(f"   💡 Try: {', '.join(club_manager.get_club_list()[:5])}... (type 'list' for all)")
    
    # Get optional notes
    notes = input("Add notes (optional, press Enter to skip): ").strip()
    
    return club_input, notes if notes else None


def main():
    """Main interactive loop"""
    print_header()
    
    # Initialize managers
    try:
        club_manager = ClubManager()
        processor = GolfDataProcessor(data_dir="data")
        
        # Load sessions
        print("📂 Loading sessions from data/ directory...")
        df = processor.load_sessions()
        summary = processor.get_session_summary()
        
        print(f"✅ Found {summary.height} sessions\n")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have session CSV files in the data/ directory.")
        print("Format: session_YYYY_MM_DD.csv")
        return 1
    
    # Find unassigned sessions
    all_sessions = summary.select(['session_id', 'session_date', 'median_carry']).to_dicts()
    assigned_sessions = set(club_manager.metadata['sessions'].keys())
    
    unassigned = [s for s in all_sessions if s['session_id'] not in assigned_sessions]
    
    if not unassigned:
        print("🎉 All sessions have been assigned clubs!")
        print("\nCurrent assignments:")
        print("-" * 70)
        for session_id, club in sorted(club_manager.metadata['sessions'].items()):
            date = session_id.replace('session_', '').replace('_', '-')
            notes = club_manager.get_session_notes(session_id)
            notes_str = f" - {notes}" if notes else ""
            print(f"  {date}: {club}{notes_str}")
        print("-" * 70)
        return 0
    
    # Show status
    total = len(all_sessions)
    assigned_count = total - len(unassigned)
    
    print(f"Status: {assigned_count}/{total} sessions assigned")
    print(f"📋 {len(unassigned)} session(s) need assignment\n")
    
    # Show club list
    print_club_list(club_manager)
    
    # Process each unassigned session
    assigned_this_session = 0
    
    for session_data in sorted(unassigned, key=lambda x: x['session_date']):
        session_id = session_data['session_id']
        date_str = session_data['session_date'].strftime('%Y-%m-%d')
        avg_carry = session_data.get('median_carry')
        
        club, notes = assign_session(session_id, date_str, avg_carry, club_manager)
        
        if club is None:  # User wants to quit
            print(f"\n👋 Assigned {assigned_this_session} sessions this session. Exiting.")
            break
        
        if club == "SKIP":  # User wants to skip
            continue
        
        # Save assignment
        club_manager.set_session_club(session_id, club, notes or "")
        print(f"   ✅ Assigned: {club}")
        assigned_this_session += 1
    
    # Summary
    print("\n" + "="*70)
    print(f"✅ Successfully assigned {assigned_this_session} session(s)")
    print("="*70)
    
    if assigned_this_session > 0:
        print("\n💡 Restart the dashboard to see club-specific analysis:")
        print("   marimo edit dashboard.py")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
