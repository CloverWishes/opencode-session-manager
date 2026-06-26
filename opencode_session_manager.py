#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCode Session Manager
A tool to list and restore archived OpenCode chat sessions
"""

import sqlite3
import os
import sys
import argparse
from datetime import datetime
from typing import List, Tuple, Optional


class OpenCodeSessionManager:
    """Manager for OpenCode chat sessions"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the session manager
        
        Args:
            db_path: Path to the SQLite database. Defaults to ~/.local/share/opencode/opencode.db
        """
        if db_path is None:
            home = os.path.expanduser('~')
            db_path = os.path.join(home, '.local', 'share', 'opencode', 'opencode.db')
        
        self.db_path = db_path
        self._validate_db()
    
    def _validate_db(self):
        """Validate that the database file exists"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
    
    def _connect(self) -> sqlite3.Connection:
        """Establish database connection"""
        return sqlite3.connect(self.db_path)
    
    def list_sessions(self, show_all: bool = False) -> List[Tuple]:
        """
        List all sessions
        
        Args:
            show_all: Whether to show all sessions (including active ones)
            
        Returns:
            List of sessions with (id, title, created, updated, archived, status)
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        if show_all:
            cursor.execute('''
                SELECT id, title, time_created, time_updated, time_archived,
                       CASE 
                           WHEN time_archived IS NOT NULL THEN 'Archived'
                           ELSE 'Active'
                       END as status
                FROM session
                ORDER BY COALESCE(time_updated, time_created) DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, title, time_created, time_updated, time_archived,
                       'Archived' as status
                FROM session
                WHERE time_archived IS NOT NULL
                ORDER BY time_archived DESC
            ''')
        
        sessions = cursor.fetchall()
        conn.close()
        return sessions
    
    def restore_session(self, session_id: str) -> bool:
        """
        Restore a specific session
        
        Args:
            session_id: The session ID to restore
            
        Returns:
            True if successful, False otherwise
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        # Check if session exists and is archived
        cursor.execute(
            'SELECT title, time_archived FROM session WHERE id = ?',
            (session_id,)
        )
        result = cursor.fetchone()
        
        if not result:
            print(f"Error: Session '{session_id}' not found")
            conn.close()
            return False
        
        title, archived = result
        
        if archived is None:
            print(f"Session '{title}' is already active")
            conn.close()
            return True
        
        # Perform restore
        cursor.execute(
            'UPDATE session SET time_archived = NULL WHERE id = ?',
            (session_id,)
        )
        conn.commit()
        
        print(f"✓ Successfully restored session: {title}")
        conn.close()
        return True
    
    def restore_all_sessions(self) -> int:
        """
        Restore all archived sessions
        
        Returns:
            Number of sessions restored
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        # Get list of sessions to restore
        cursor.execute(
            'SELECT id, title FROM session WHERE time_archived IS NOT NULL'
        )
        to_restore = cursor.fetchall()
        
        if not to_restore:
            print("No archived sessions to restore")
            conn.close()
            return 0
        
        # Perform restore
        cursor.execute('UPDATE session SET time_archived = NULL WHERE time_archived IS NOT NULL')
        restored_count = cursor.rowcount
        conn.commit()
        
        print(f"✓ Successfully restored {restored_count} session(s):")
        for session_id, title in to_restore:
            print(f"  - {title}")
        
        conn.close()
        return restored_count
    
    def archive_session(self, session_id: str) -> bool:
        """
        Archive a specific session (optional feature)
        
        Args:
            session_id: The session ID to archive
            
        Returns:
            True if successful, False otherwise
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        # Check if session exists
        cursor.execute(
            'SELECT title, time_archived FROM session WHERE id = ?',
            (session_id,)
        )
        result = cursor.fetchone()
        
        if not result:
            print(f"Error: Session '{session_id}' not found")
            conn.close()
            return False
        
        title, archived = result
        
        if archived is not None:
            print(f"Session '{title}' is already archived")
            conn.close()
            return True
        
        # Perform archive
        current_time = int(datetime.now().timestamp() * 1000)
        cursor.execute(
            'UPDATE session SET time_archived = ? WHERE id = ?',
            (current_time, session_id)
        )
        conn.commit()
        
        print(f"✓ Successfully archived session: {title}")
        conn.close()
        return True


def format_timestamp(timestamp_ms: Optional[int]) -> str:
    """Format timestamp to readable string"""
    if timestamp_ms is None:
        return 'N/A'
    try:
        return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return 'Invalid'


def print_sessions(sessions: List[Tuple]):
    """Print session list"""
    if not sessions:
        print("No sessions found")
        return
    
    print(f"\n{'='*100}")
    print(f"Found {len(sessions)} session(s):")
    print(f"{'='*100}\n")
    
    for i, session in enumerate(sessions, 1):
        session_id, title, created, updated, archived, status = session
        
        print(f"[{i}] {status}")
        print(f"    ID:       {session_id}")
        print(f"    Title:    {title or '(No title)'}")
        print(f"    Created:  {format_timestamp(created)}")
        print(f"    Updated:  {format_timestamp(updated)}")
        if archived:
            print(f"    Archived: {format_timestamp(archived)}")
        print()


def interactive_mode(manager: OpenCodeSessionManager):
    """Interactive mode"""
    print("\n" + "="*60)
    print("OpenCode Session Manager - Interactive Mode")
    print("="*60)
    
    while True:
        print("\nSelect an option:")
        print("  1. List all sessions (active + archived)")
        print("  2. List archived sessions only")
        print("  3. Restore a specific session")
        print("  4. Restore all archived sessions")
        print("  5. Archive a specific session")
        print("  0. Exit")
        
        choice = input("\nEnter option (0-5): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        
        elif choice == '1':
            sessions = manager.list_sessions(show_all=True)
            print_sessions(sessions)
        
        elif choice == '2':
            sessions = manager.list_sessions(show_all=False)
            print_sessions(sessions)
        
        elif choice == '3':
            session_id = input("Enter session ID to restore: ").strip()
            if session_id:
                manager.restore_session(session_id)
            else:
                print("Error: Session ID cannot be empty")
        
        elif choice == '4':
            confirm = input("Restore all archived sessions? (y/N): ").strip().lower()
            if confirm == 'y':
                manager.restore_all_sessions()
            else:
                print("Cancelled")
        
        elif choice == '5':
            session_id = input("Enter session ID to archive: ").strip()
            if session_id:
                manager.archive_session(session_id)
            else:
                print("Error: Session ID cannot be empty")
        
        else:
            print("Invalid option, please try again")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='OpenCode Session Manager - List and restore chat sessions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Interactive mode
  python opencode_session_manager.py
  
  # List all sessions
  python opencode_session_manager.py --list-all
  
  # List archived sessions only
  python opencode_session_manager.py --list-archived
  
  # Restore specific session
  python opencode_session_manager.py --restore ses_xxx
  
  # Restore all archived sessions
  python opencode_session_manager.py --restore-all
  
  # Specify custom database path
  python opencode_session_manager.py --db /path/to/opencode.db --list-all
        '''
    )
    
    parser.add_argument(
        '--db', '-d',
        help='Database file path (default: ~/.local/share/opencode/opencode.db)'
    )
    
    parser.add_argument(
        '--list-all', '-a',
        action='store_true',
        help='List all sessions (active + archived)'
    )
    
    parser.add_argument(
        '--list-archived', '-l',
        action='store_true',
        help='List archived sessions only'
    )
    
    parser.add_argument(
        '--restore', '-r',
        metavar='SESSION_ID',
        help='Restore a specific session by ID'
    )
    
    parser.add_argument(
        '--restore-all', '-R',
        action='store_true',
        help='Restore all archived sessions'
    )
    
    parser.add_argument(
        '--archive',
        metavar='SESSION_ID',
        help='Archive a specific session by ID'
    )
    
    args = parser.parse_args()
    
    try:
        manager = OpenCodeSessionManager(args.db)
        
        if args.list_all:
            sessions = manager.list_sessions(show_all=True)
            print_sessions(sessions)
        
        elif args.list_archived:
            sessions = manager.list_sessions(show_all=False)
            print_sessions(sessions)
        
        elif args.restore:
            manager.restore_session(args.restore)
        
        elif args.restore_all:
            manager.restore_all_sessions()
        
        elif args.archive:
            manager.archive_session(args.archive)
        
        else:
            interactive_mode(manager)
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nTip: Use --db to specify a custom database path")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
