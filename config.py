# config.py
import os

class Config:
    SECRET_KEY = 'industrial-defect-secret-key-2024'
    DATABASE_PATH = 'database/defects.db'
    UPLOAD_FOLDER = 'static/uploads'
    MODEL_PATH = 'models'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
    
    # Image processing settings
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600
    CANNY_THRESHOLD1 = 50
    CANNY_THRESHOLD2 = 150
    
    # Defect classification thresholds
    MINOR_DEFECT_THRESHOLD = 0.3
    MAJOR_DEFECT_THRESHOLD = 0.6
    CRITICAL_DEFECT_THRESHOLD = 0.8
    
    # Alert settings
    ALERT_EMAIL = 'admin@company.com'
    ALERT_THRESHOLD = 0.7