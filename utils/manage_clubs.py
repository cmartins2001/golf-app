#!/usr/bin/env python3
"""
Club Metadata Management Utility
Manage club assignments for golf sessions
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.club_manager import ClubManager
from utils.data_processor import GolfDataProcessor


def list_clubs(club_mgr: ClubManager):
    """List all available clubs"""
    print("\n📋 Available Clubs:\n")
    
    clubs = club_mgr.get_club_list()
    standard = [c for c in clubs if c in ClubManager.STANDARD_CLUBS]
    custom = [c for c in clubs if c not in ClubManager.STANDARD_CLUBS]
    
    if standard:
        print("Standard Clubs:")
        for club in standard:
            specs = club_mgr.get_club_specs(club)
            print(f"  • {club:12s} - {specs['type']:7s} - ~{specs['typical_carry']} yards")
    
    if custom:
        print("\nCustom Clubs:")
        for club in custom:
            specs = club_mgr.get_club_specs(club)
            print(f"  • {club:12s} - {specs['type']:7s} - ~{specs['typical_carry']} yards")
    
    print(f"\nTotal: {len(clubs)} clubs")


def list_sessions(club_mgr: ClubManager, show_all: bool = False):
    """List sessions and their club assignments"""
    try:
        processor = GolfDataProcessor()
        processor.load_sessions()
        
        sessions = processor.df.select(["session_id", "session_date", "club"]).unique().sort("session_date")
        sessions_df = sessions.to_pandas()
        
        print("\n📅 Sessions:\n")
        
        has_club = []
        missing_club = []
        
        for _, row in sessions_df.iterrows():
            session_id = row['session_id']
            date = row['session_date'].strftime('%Y-%m-%d')
            club = row['club']
            notes = club_mgr.get_session_notes(session_id)
            
            if club:
                has_club.append((date, session_id, club, notes))
            else:
                missing_club.append((date, session_id))
        
        # Show sessions with clubs
        if has_club:
            print("✅ Sessions with clubs assigned:")
            for date, session_id, club, notes in has_club:
                if notes:
                    print(f"  {date} - {club:15s} - {session_id:25s} - \"{notes}\"")
                else:
                    print(f"  {date} - {club:15s} - {session_id}")
        
        # Show sessions missing clubs
        if missing_club:
            print("\n⚠️  Sessions missing club assignment:")
            for date, session_id in missing_club:
                print(f"  {date} - {session_id}")
            print(f"\n💡 Assign clubs with: python manage_clubs.py assign <session_id> <club>")
        
        if show_all:
            print(f"\n📊 Summary:")
            summary = club_mgr.export_summary()
            print(f"  Total sessions: {summary['total_sessions']}")
            print(f"  Sessions with clubs: {len(has_club)}")
            print(f"  Sessions missing clubs: {len(missing_club)}")
            if summary['clubs_used']:
                print(f"\n  Usage by club:")
                for club, count in sorted(summary['clubs_used'].items(), key=lambda x: -x[1]):
                    print(f"    {club:15s}: {count} sessions")
        
    except FileNotFoundError:
        print("❌ No session data found. Add sessions first with: python add_session.py")


def assign_club(club_mgr: ClubManager, session_id: str, club: str, notes: Optional[str] = None):
    """Assign a club to a session"""
    # Validate club exists
    available_clubs = club_mgr.get_club_list()
    
    if club not in available_clubs:
        print(f"⚠️  Warning: '{club}' is not in the standard club list.")
        response = input(f"Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return
    
    # Assign club
    club_mgr.set_session_club(session_id, club, notes or "")
    print(f"✅ Assigned '{club}' to {session_id}")
    if notes:
        print(f"   Notes: {notes}")


def remove_club(club_mgr: ClubManager, session_id: str):
    """Remove club assignment from a session"""
    validation = club_mgr.validate_session(session_id)
    
    if not validation['has_club']:
        print(f"⚠️  Session {session_id} has no club assigned")
        return
    
    print(f"Removing club '{validation['club']}' from {session_id}")
    response = input("Continue? (y/N): ")
    
    if response.lower() == 'y':
        club_mgr.remove_session_club(session_id)
        print(f"✅ Removed club assignment from {session_id}")
    else:
        print("❌ Cancelled")


def add_custom_club(club_mgr: ClubManager, interactive: bool = True):
    """Add a custom club interactively"""
    if interactive:
        print("\n➕ Add Custom Club\n")
        
        name = input("Club name (e.g., '4 Hybrid'): ").strip()
        if not name:
            print("❌ Club name required")
            return
        
        print("\nClub type:")
        print("  1. Wood")
        print("  2. Hybrid")
        print("  3. Iron")
        print("  4. Wedge")
        
        club_type_map = {'1': 'wood', '2': 'hybrid', '3': 'iron', '4': 'wedge'}
        type_choice = input("Select (1-4): ").strip()
        club_type = club_type_map.get(type_choice)
        
        if not club_type:
            print("❌ Invalid club type")
            return
        
        try:
            typical_carry = int(input("Typical carry distance (yards): ").strip())
            
            print("\nOptimal launch angle range:")
            launch_min = float(input("  Minimum (degrees): ").strip())
            launch_max = float(input("  Maximum (degrees): ").strip())
            
            print("\nOptimal spin range:")
            spin_min = int(input("  Minimum (RPM): ").strip())
            spin_max = int(input("  Maximum (RPM): ").strip())
            
            # Add club
            club_mgr.add_custom_club(
                name=name,
                club_type=club_type,
                typical_carry=typical_carry,
                optimal_launch=(launch_min, launch_max),
                optimal_spin=(spin_min, spin_max)
            )
            
            print(f"\n✅ Added custom club: {name}")
            print(f"   Type: {club_type}")
            print(f"   Typical carry: {typical_carry} yards")
            print(f"   Launch: {launch_min}° - {launch_max}°")
            print(f"   Spin: {spin_min} - {spin_max} RPM")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")


def show_club_stats(club_mgr: ClubManager):
    """Show statistics for each club"""
    try:
        processor = GolfDataProcessor()
        processor.load_sessions()
        
        comparison = processor.get_club_comparison()
        
        if comparison.height == 0:
            print("⚠️  No clubs assigned to sessions yet")
            return
        
        print("\n📊 Club Performance Comparison:\n")
        print(f"{'Club':<15} {'Carry':<8} {'Std':<7} {'Offline':<8} {'Quality':<8} {'Sessions':<10} {'Shots'}")
        print("-" * 85)
        
        for row in comparison.iter_rows(named=True):
            club = row['club'] or 'Unknown'
            carry = f"{row['median_carry']:.1f}y"
            std = f"{row['carry_std']:.1f}y"
            offline = f"{row['avg_offline']:.1f}y"
            quality = f"{row['strike_quality_rate']*100:.0f}%"
            sessions = f"{row['num_sessions']}"
            shots = f"{row['total_shots']}"
            
            print(f"{club:<15} {carry:<8} {std:<7} {offline:<8} {quality:<8} {sessions:<10} {shots}")
        
        print(f"\n💡 This shows aggregated performance across all sessions for each club")
        
    except FileNotFoundError:
        print("❌ No session data found")


def main():
    parser = argparse.ArgumentParser(
        description="Manage club metadata for golf sessions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available clubs
  python manage_clubs.py list-clubs
  
  # List sessions and their club assignments
  python manage_clubs.py list-sessions
  
  # Assign a club to a session
  python manage_clubs.py assign session_2025_01_20 "7 Iron"
  
  # Assign with notes
  python manage_clubs.py assign session_2025_01_20 Driver -n "Trying new swing thought"
  
  # Remove club assignment
  python manage_clubs.py remove session_2025_01_20
  
  # Add custom club
  python manage_clubs.py add-club
  
  # Show performance stats by club
  python manage_clubs.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List clubs command
    subparsers.add_parser('list-clubs', help='List all available clubs')
    
    # List sessions command
    list_sessions_parser = subparsers.add_parser('list-sessions', help='List sessions and club assignments')
    list_sessions_parser.add_argument('--all', action='store_true', help='Show detailed summary')
    
    # Assign club command
    assign_parser = subparsers.add_parser('assign', help='Assign a club to a session')
    assign_parser.add_argument('session_id', help='Session ID (e.g., session_2025_01_20)')
    assign_parser.add_argument('club', help='Club name (e.g., "7 Iron", "Driver")')
    assign_parser.add_argument('-n', '--notes', help='Session notes', default=None)
    
    # Remove club command
    remove_parser = subparsers.add_parser('remove', help='Remove club assignment from session')
    remove_parser.add_argument('session_id', help='Session ID')
    
    # Add custom club command
    subparsers.add_parser('add-club', help='Add a custom club (interactive)')
    
    # Show stats command
    subparsers.add_parser('stats', help='Show performance statistics by club')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    club_mgr = ClubManager()
    
    if args.command == 'list-clubs':
        list_clubs(club_mgr)
    elif args.command == 'list-sessions':
        list_sessions(club_mgr, show_all=args.all)
    elif args.command == 'assign':
        assign_club(club_mgr, args.session_id, args.club, args.notes)
    elif args.command == 'remove':
        remove_club(club_mgr, args.session_id)
    elif args.command == 'add-club':
        add_custom_club(club_mgr)
    elif args.command == 'stats':
        show_club_stats(club_mgr)


if __name__ == "__main__":
    main()
