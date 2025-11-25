# scripts/backup_data.py
#!/usr/bin/env python3

import shutil
import os
from datetime import datetime
from config import Config

def backup_database():
    """Create a backup of the database"""
    print("Creating database backup...")
    
    if not os.path.exists(Config.DATABASE_PATH):
        print("Database file not found. No backup created.")
        return
    
    # Create backup directory if it doesn't exist
    backup_dir = 'database/backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"defects_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Copy database file
    shutil.copy2(Config.DATABASE_PATH, backup_path)
    
    # Clean up old backups (keep only last 10)
    backup_files = sorted([f for f in os.listdir(backup_dir) if f.startswith('defects_backup_')])
    if len(backup_files) > 10:
        for old_backup in backup_files[:-10]:
            os.remove(os.path.join(backup_dir, old_backup))
    
    print(f"Backup created: {backup_path}")
    print(f"Total backups: {len(backup_files)}")

if __name__ == '__main__':
    backup_database()