# src/edge_detection.py
import cv2
import numpy as np
from scipy import ndimage

class EdgeDefectDetector:
    def __init__(self):
        self.canny_threshold1 = 50
        self.canny_threshold2 = 150
    
    def detect_cracks_canny(self, image):
        """Detect cracks and edges using Canny edge detection"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, self.canny_threshold1, self.canny_threshold2)
        
        # Morphological operations to enhance crack detection
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        return edges
    
    def detect_cracks_log(self, image):
        """Detect cracks using Laplacian of Gaussian"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply Laplacian
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
        
        # Zero-crossing detection for LOG
        log_edges = np.zeros_like(laplacian)
        log_edges[laplacian > 0.1] = 255
        
        return log_edges.astype(np.uint8)
    
    def detect_line_defects(self, image):
        """Detect line-shaped defects using Hough Transform"""
        edges = self.detect_cracks_canny(image)
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                               minLineLength=50, maxLineGap=10)
        
        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        return line_image
    
    def calculate_edge_density(self, edges):
        """Calculate edge density as defect indicator"""
        total_pixels = edges.shape[0] * edges.shape[1]
        edge_pixels = np.count_nonzero(edges)
        return edge_pixels / total_pixels
    
    def highlight_defect_regions(self, image, edges):
        """Highlight defect regions on original image"""
        # Find contours in edge image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on original image
        result = image.copy()
        cv2.drawContours(result, contours, -1, (0, 0, 255), 2)
        
        return result