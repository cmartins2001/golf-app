#!/usr/bin/env python3
"""
Helper script to add new golf sessions to the dashboard
Usage: python add_session.py <path_to_csv> [--date YYYY-MM-DD] [--club CLUB_NAME] [--notes "notes"]
"""

import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.club_manager import ClubManager


def add_session(
    source_file: str, 
    date: str = None,
    club: str = None,
    notes: str = None,
    interactive: bool = True
) -> None:
    """
    Add a new session CSV to the data directory with proper naming and club assignment
    
    Args:
        source_file: Path to the exported CSV from Refine
        date: Optional date string (YYYY-MM-DD). Uses today if not provided.
        club: Optional club name to assign
        notes: Optional session notes
        interactive: If True, prompt for missing information
    """
    source = Path(source_file)
    
    if not source.exists():
        print(f"❌ Error: File not found: {source}")
        return
    
    if not source.suffix == '.csv':
        print(f"❌ Error: File must be a CSV: {source}")
        return
    
    # Parse or use today's date
    if date:
        try:
            session_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(f"❌ Error: Date must be in format YYYY-MM-DD, got: {date}")
            return
    else:
        if interactive:
            date_input = input(f"Enter session date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_input:
                try:
                    session_date = datetime.strptime(date_input, "%Y-%m-%d")
                except ValueError:
                    print(f"❌ Error: Invalid date format: {date_input}")
                    return
            else:
                session_date = datetime.now()
        else:
            session_date = datetime.now()
    
    # Create destination path
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    date_str = session_date.strftime("%Y_%m_%d")
    session_id = f"session_{date_str}"
    dest = data_dir / f"{session_id}.csv"
    
    # Check if already exists
    if dest.exists():
        response = input(f"⚠️  Session already exists for {date_str}. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return
    
    # Copy file
    try:
        shutil.copy2(source, dest)
        print(f"✅ Session file added successfully!")
        print(f"   Source: {source}")
        print(f"   Destination: {dest}")
        print(f"   Date: {session_date.strftime('%B %d, %Y')}")
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return
    
    # Handle club assignment
    club_manager = ClubManager()
    
    if not club and interactive:
        print(f"\n🏌️  Club Assignment")
        print(f"Available clubs: {', '.join(club_manager.get_club_list()[:8])}...")
        club = input("Enter club name (or press Enter to skip): ").strip()
    
    if club:
        # Validate club
        if club not in club_manager.get_club_list():
            print(f"⚠️  Warning: Unknown club '{club}'")
            if interactive:
                use_anyway = input("Use anyway? (y/N): ")
                if use_anyway.lower() != 'y':
                    club = None
        
        if club:
            # Get notes if not provided
            if not notes and interactive:
                notes = input("Add notes (optional, press Enter to skip): ").strip()
            
            # Save club assignment
            club_manager.set_session_club(session_id, club, notes or "")
            print(f"   ✅ Club assigned: {club}")
            if notes:
                print(f"   📝 Notes: {notes}")
    
    print(f"\n💡 Restart the dashboard to load this session:")
    print(f"   marimo edit dashboard.py")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new golf session to the dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python add_session.py ~/Downloads/refine_export.csv
  
  # With date and club
  python add_session.py ~/Downloads/refine_export.csv --date 2025-01-20 --club "7 Iron"
  
  # With notes
  python add_session.py range_data.csv -d 2025-01-15 -c Driver -n "Working on tempo"
  
  # Non-interactive
  python add_session.py data.csv --date 2025-01-20 --club PW --no-interactive
        """
    )
    
    parser.add_argument(
        'source',
        help='Path to the CSV file exported from Refine software'
    )
    
    parser.add_argument(
        '-d', '--date',
        help='Session date (YYYY-MM-DD). Uses today if not provided.',
        default=None
    )
    
    parser.add_argument(
        '-c', '--club',
        help='Club used in this session (e.g., "7 Iron", "Driver")',
        default=None
    )
    
    parser.add_argument(
        '-n', '--notes',
        help='Optional notes about the session',
        default=None
    )
    
    parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Disable interactive prompts'
    )
    
    args = parser.parse_args()
    add_session(
        args.source, 
        args.date, 
        args.club, 
        args.notes,
        interactive=not args.no_interactive
    )


if __name__ == "__main__":
    main()
