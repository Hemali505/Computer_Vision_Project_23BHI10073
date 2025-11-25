# src/color_analysis.py
import cv2
import numpy as np

class ColorAnalyzer:
    def __init__(self):
        self.defect_color_ranges = {
            'rust': ([0, 50, 50], [20, 255, 255]),  # HSV range for rust
            'discoloration': ([0, 0, 0], [180, 50, 150]),  # Dark discoloration
            'stain': ([0, 0, 100], [180, 50, 200])  # Light stains
        }
    
    def detect_color_defects(self, image):
        """Detect defects based on color anomalies"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        defect_masks = {}
        total_defect_pixels = 0
        
        for defect_type, (lower, upper) in self.defect_color_ranges.items():
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            
            # Create mask for defect color
            mask = cv2.inRange(hsv, lower, upper)
            defect_pixels = np.count_nonzero(mask)
            
            defect_masks[defect_type] = {
                'mask': mask,
                'pixel_count': defect_pixels,
                'percentage': defect_pixels / (image.shape[0] * image.shape[1])
            }
            
            total_defect_pixels += defect_pixels
        
        total_percentage = total_defect_pixels / (image.shape[0] * image.shape[1])
        
        return defect_masks, total_percentage
    
    def analyze_color_consistency(self, image):
        """Analyze color consistency across the image"""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Calculate color standard deviations
        l_std = np.std(l)
        a_std = np.std(a)
        b_std = np.std(b)
        
        # High standard deviation indicates color inconsistency (potential defect)
        color_variation = (l_std + a_std + b_std) / 3
        
        return color_variation, (l_std, a_std, b_std)
    
    def detect_discoloration(self, image, reference_color=None):
        """Detect discoloration compared to reference color"""
        if reference_color is None:
            # Use average color as reference
            reference_color = np.mean(image, axis=(0, 1))
        
        # Calculate color difference for each pixel
        color_diff = np.sqrt(np.sum((image - reference_color) ** 2, axis=2))
        
        # Normalize and threshold
        max_diff = np.max(color_diff)
        if max_diff > 0:
            color_diff_normalized = color_diff / max_diff
        else:
            color_diff_normalized = color_diff
        
        # Create discoloration mask
        discoloration_mask = (color_diff_normalized > 0.3).astype(np.uint8) * 255
        
        discoloration_percentage = np.count_nonzero(discoloration_mask) / discoloration_mask.size
        
        return discoloration_mask, discoloration_percentage