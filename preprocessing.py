# src/preprocessing.py
import cv2
import numpy as np

class ImagePreprocessor:
    def __init__(self):
        self.target_width = 800
        self.target_height = 600
    
    def preprocess(self, image):
        """Main preprocessing pipeline"""
        if image is None:
            return None
        
        # Step 1: Resize image
        resized = self.resize_image(image)
        
        # Step 2: Convert to appropriate color space
        processed = self.convert_color_space(resized)
        
        # Step 3: Noise reduction
        denoised = self.remove_noise(processed)
        
        # Step 4: Contrast enhancement
        enhanced = self.enhance_contrast(denoised)
        
        return enhanced
    
    def resize_image(self, image):
        """Resize image to standard dimensions"""
        return cv2.resize(image, (self.target_width, self.target_height))
    
    def convert_color_space(self, image):
        """Convert to appropriate color space for analysis"""
        # For defect detection, we often use grayscale or LAB color space
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Convert back to 3-channel for consistency
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    def remove_noise(self, image):
        """Apply noise reduction filters"""
        # Gaussian blur for noise reduction
        return cv2.GaussianBlur(image, (5, 5), 0)
    
    def enhance_contrast(self, image):
        """Enhance image contrast using CLAHE"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        
        # Merge back and convert to BGR
        lab_enhanced = cv2.merge([l_enhanced, a, b])
        return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
    
    def normalize_illumination(self, image):
        """Normalize uneven illumination"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create illumination model using Gaussian blur
        illumination_model = cv2.GaussianBlur(gray, (101, 101), 0)
        
        # Normalize by illumination model
        normalized = gray.astype(np.float32) / illumination_model.astype(np.float32)
        normalized = np.uint8(255 * normalized / np.max(normalized))
        
        return cv2.cvtColor(normalized, cv2.COLOR_GRAY2BGR)