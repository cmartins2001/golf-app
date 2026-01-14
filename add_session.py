#!/usr/bin/env python3
"""
Helper script to add new golf sessions to the dashboard
Usage: python add_session.py <path_to_csv> [--date YYYY-MM-DD]
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime


def add_session(source_file: str, date: str = None) -> None:
    """
    Add a new session CSV to the data directory with proper naming
    
    Args:
        source_file: Path to the exported CSV from Refine
        date: Optional date string (YYYY-MM-DD). Uses today if not provided.
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
        session_date = datetime.now()
    
    # Create destination path
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    date_str = session_date.strftime("%Y_%m_%d")
    dest = data_dir / f"session_{date_str}.csv"
    
    # Check if already exists
    if dest.exists():
        response = input(f"⚠️  Session already exists for {date_str}. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled")
            return
    
    # Copy file
    try:
        shutil.copy2(source, dest)
        print(f"✅ Session added successfully!")
        print(f"   Source: {source}")
        print(f"   Destination: {dest}")
        print(f"   Date: {session_date.strftime('%B %d, %Y')}")
        print(f"\n💡 Restart the dashboard to load this session:")
        print(f"   marimo edit dashboard.py")
    except Exception as e:
        print(f"❌ Error copying file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new golf session to the dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add today's session
  python add_session.py ~/Downloads/refine_export.csv
  
  # Add session with specific date
  python add_session.py ~/Downloads/refine_export.csv --date 2025-01-20
  
  # Add session using explicit date
  python add_session.py range_data.csv -d 2025-01-15
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
    
    args = parser.parse_args()
    add_session(args.source, args.date)


if __name__ == "__main__":
    main()
