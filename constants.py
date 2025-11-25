# src/utils/constants.py
# Application constants

# Defect types
DEFECT_TYPES = {
    'GOOD': 'No defects detected',
    'MINOR': 'Minor defects - acceptable',
    'MAJOR': 'Major defects - requires attention', 
    'CRITICAL': 'Critical defects - immediate action required',
    'UNKNOWN': 'Unable to determine defect status'
}

# Color codes for defect types
DEFECT_COLORS = {
    'GOOD': '#28a745',      # Green
    'MINOR': '#ffc107',     # Yellow
    'MAJOR': '#fd7e14',     # Orange
    'CRITICAL': '#dc3545',  # Red
    'UNKNOWN': '#6c757d'    # Gray
}

# Image processing parameters
IMAGE_SETTINGS = {
    'DEFAULT_WIDTH': 800,
    'DEFAULT_HEIGHT': 600,
    'MAX_FILE_SIZE': 16 * 1024 * 1024,  # 16MB
    'SUPPORTED_FORMATS': ['.jpg', '.jpeg', '.png', '.bmp']
}

# Alert thresholds
ALERT_THRESHOLDS = {
    'MINOR': 0.3,
    'MAJOR': 0.6,
    'CRITICAL': 0.8,
    'ALERT_EMAIL': 0.7
}

# Database settings
DB_SETTINGS = {
    'MAX_RECORDS': 10000,
    'BACKUP_INTERVAL': 24,  # hours
    'CLEANUP_DAYS': 30      # days
}