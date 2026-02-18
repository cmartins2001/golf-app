"""
Club Metadata Management
Handles mapping sessions to clubs and managing club configuration
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ClubManager:
    """Manage club metadata for golf sessions"""
    
    # Standard club list with typical characteristics
    STANDARD_CLUBS = {
        'Driver': {'type': 'wood', 'typical_carry': 250, 'optimal_launch': (12, 16), 'optimal_spin': (2200, 2800)},
        '3 Wood': {'type': 'wood', 'typical_carry': 230, 'optimal_launch': (11, 15), 'optimal_spin': (2500, 3500)},
        '5 Wood': {'type': 'wood', 'typical_carry': 215, 'optimal_launch': (12, 16), 'optimal_spin': (3000, 4000)},
        '3 Hybrid': {'type': 'hybrid', 'typical_carry': 200, 'optimal_launch': (13, 17), 'optimal_spin': (3500, 4500)},
        '4 Hybrid': {'type': 'hybrid', 'typical_carry': 190, 'optimal_launch': (14, 18), 'optimal_spin': (4000, 5000)},
        '3 Iron': {'type': 'iron', 'typical_carry': 195, 'optimal_launch': (12, 16), 'optimal_spin': (4000, 5000)},
        '4 Iron': {'type': 'iron', 'typical_carry': 185, 'optimal_launch': (13, 17), 'optimal_spin': (4500, 5500)},
        '5 Iron': {'type': 'iron', 'typical_carry': 175, 'optimal_launch': (14, 18), 'optimal_spin': (5000, 6000)},
        '6 Iron': {'type': 'iron', 'typical_carry': 165, 'optimal_launch': (15, 19), 'optimal_spin': (5500, 6500)},
        '7 Iron': {'type': 'iron', 'typical_carry': 155, 'optimal_launch': (16, 20), 'optimal_spin': (6000, 7000)},
        '8 Iron': {'type': 'iron', 'typical_carry': 145, 'optimal_launch': (17, 21), 'optimal_spin': (6500, 7500)},
        '9 Iron': {'type': 'iron', 'typical_carry': 135, 'optimal_launch': (18, 22), 'optimal_spin': (7000, 8000)},
        'PW': {'type': 'wedge', 'typical_carry': 125, 'optimal_launch': (20, 24), 'optimal_spin': (7500, 9000)},
        'GW': {'type': 'wedge', 'typical_carry': 110, 'optimal_launch': (22, 26), 'optimal_spin': (8000, 10000)},
        'SW': {'type': 'wedge', 'typical_carry': 95, 'optimal_launch': (24, 28), 'optimal_spin': (8500, 11000)},
        'LW': {'type': 'wedge', 'typical_carry': 80, 'optimal_launch': (26, 30), 'optimal_spin': (9000, 12000)},
    }
    
    def __init__(self, metadata_file: str = "data/club_metadata.json"):
        self.metadata_file = Path(metadata_file)
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load club metadata from JSON file"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        else:
            # Initialize with empty structure
            return {
                'sessions': {},  # session_id -> club mapping
                'custom_clubs': {},  # user-defined clubs
                'notes': {}  # session_id -> notes
            }
    
    def _save_metadata(self):
        """Save metadata to JSON file"""
        self.metadata_file.parent.mkdir(exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def set_session_club(self, session_id: str, club: str, notes: str = "") -> None:
        """
        Associate a club with a session
        
        Args:
            session_id: Session identifier (e.g., 'session_2025_01_20')
            club: Club name (e.g., '7 Iron', 'Driver')
            notes: Optional notes about the session
        """
        self.metadata['sessions'][session_id] = club
        if notes:
            self.metadata['notes'][session_id] = notes
        self._save_metadata()
    
    def get_session_club(self, session_id: str) -> Optional[str]:
        """Get the club used in a session"""
        return self.metadata['sessions'].get(session_id)
    
    def get_session_notes(self, session_id: str) -> Optional[str]:
        """Get notes for a session"""
        return self.metadata['notes'].get(session_id)
    
    def get_sessions_by_club(self, club: str) -> List[str]:
        """Get all session IDs that used a specific club"""
        return [
            session_id for session_id, session_club in self.metadata['sessions'].items()
            if session_club == club
        ]
    
    def get_all_clubs_used(self) -> List[str]:
        """Get list of all clubs that have been used in sessions"""
        return sorted(list(set(self.metadata['sessions'].values())))
    
    def add_custom_club(
        self, 
        name: str, 
        club_type: str,
        typical_carry: int,
        optimal_launch: tuple,
        optimal_spin: tuple
    ) -> None:
        """
        Add a custom club configuration
        
        Args:
            name: Club name
            club_type: One of 'wood', 'hybrid', 'iron', 'wedge'
            typical_carry: Expected carry distance in yards
            optimal_launch: Tuple of (min, max) launch angle in degrees
            optimal_spin: Tuple of (min, max) spin in RPM
        """
        self.metadata['custom_clubs'][name] = {
            'type': club_type,
            'typical_carry': typical_carry,
            'optimal_launch': optimal_launch,
            'optimal_spin': optimal_spin
        }
        self._save_metadata()
    
    def get_club_specs(self, club: str) -> Optional[Dict]:
        """
        Get specifications for a club (standard or custom)
        
        Returns club specs or None if not found
        """
        # Check custom clubs first
        if club in self.metadata['custom_clubs']:
            return self.metadata['custom_clubs'][club]
        # Then check standard clubs
        elif club in self.STANDARD_CLUBS:
            return self.STANDARD_CLUBS[club]
        else:
            return None
    
    def remove_session_club(self, session_id: str) -> None:
        """Remove club association from a session"""
        if session_id in self.metadata['sessions']:
            del self.metadata['sessions'][session_id]
        if session_id in self.metadata['notes']:
            del self.metadata['notes'][session_id]
        self._save_metadata()
    
    def get_club_list(self) -> List[str]:
        """Get complete list of available clubs (standard + custom)"""
        standard = list(self.STANDARD_CLUBS.keys())
        custom = list(self.metadata['custom_clubs'].keys())
        return sorted(standard + custom)
    
    def export_summary(self) -> Dict:
        """Export summary of all session-club mappings"""
        summary = {
            'total_sessions': len(self.metadata['sessions']),
            'clubs_used': {},
            'sessions_without_club': []
        }
        
        # Count sessions per club
        for club in self.get_all_clubs_used():
            sessions = self.get_sessions_by_club(club)
            summary['clubs_used'][club] = len(sessions)
        
        return summary
    
    def validate_session(self, session_id: str) -> Dict[str, any]:
        """
        Check if a session has club metadata and return status
        
        Returns:
            Dictionary with 'has_club', 'club', 'has_notes', 'notes'
        """
        club = self.get_session_club(session_id)
        notes = self.get_session_notes(session_id)
        
        return {
            'has_club': club is not None,
            'club': club,
            'has_notes': notes is not None and notes != '',
            'notes': notes or ''
        }
