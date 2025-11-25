# src/utils/validation.py
import re
import os

def validate_image_file(filename, allowed_extensions=None):
    """Validate image file name and extension"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp'}
    
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions

def validate_product_id(product_id):
    """Validate product ID format"""
    if not product_id or len(product_id) > 50:
        return False
    return re.match(r'^[A-Z0-9_-]+$', product_id) is not None

def validate_confidence_score(confidence):
    """Validate confidence score range"""
    return 0.0 <= confidence <= 1.0

def validate_defect_type(defect_type):
    """Validate defect type"""
    valid_types = ['GOOD', 'MINOR', 'MAJOR', 'CRITICAL', 'UNKNOWN']
    return defect_type in valid_types

def validate_file_path(file_path):
    """Validate file path exists and is accessible"""
    return os.path.exists(file_path) and os.path.isfile(file_path)

def validate_image_dimensions(image, min_width=100, min_height=100):
    """Validate image dimensions"""
    if image is None:
        return False
    
    height, width = image.shape[:2]
    return width >= min_width and height >= min_height