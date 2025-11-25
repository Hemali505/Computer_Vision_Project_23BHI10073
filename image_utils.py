# src/utils/image_utils.py
import cv2
import numpy as np

def resize_image(image, width=None, height=None):
    """Resize image while maintaining aspect ratio"""
    if width is None and height is None:
        return image
    
    h, w = image.shape[:2]
    
    if width is None:
        # Calculate width based on height
        ratio = height / float(h)
        width = int(w * ratio)
    elif height is None:
        # Calculate height based on width
        ratio = width / float(w)
        height = int(h * ratio)
    
    return cv2.resize(image, (width, height))

def rotate_image(image, angle):
    """Rotate image by specified angle"""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h))
    
    return rotated

def adjust_brightness_contrast(image, brightness=0, contrast=0):
    """Adjust image brightness and contrast"""
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        
        image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        
        image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)
    
    return image

def create_image_montage(images, grid_shape=None):
    """Create montage of multiple images"""
    if grid_shape is None:
        grid_shape = (len(images), 1) if len(images) > 0 else (1, 1)
    
    rows, cols = grid_shape
    montage_images = []
    
    for i in range(rows):
        row_images = []
        for j in range(cols):
            idx = i * cols + j
            if idx < len(images):
                row_images.append(images[idx])
            else:
                # Add blank image
                blank = np.zeros_like(images[0]) if images else np.zeros((100, 100, 3), dtype=np.uint8)
                row_images.append(blank)
        
        # Concatenate row
        montage_row = np.concatenate(row_images, axis=1)
        montage_images.append(montage_row)
    
    # Concatenate all rows
    if montage_images:
        return np.concatenate(montage_images, axis=0)
    else:
        return np.zeros((100, 100, 3), dtype=np.uint8)