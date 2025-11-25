# tests/test_edge_detection.py
import unittest
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.edge_detection import EdgeDefectDetector

class TestEdgeDetection(unittest.TestCase):
    def setUp(self):
        self.detector = EdgeDefectDetector()
        # Create test image with simulated crack
        self.test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        # Add a vertical line as simulated crack
        self.test_image[:, 50:52] = 0
    
    def test_canny_edge_detection(self):
        edges = self.detector.detect_cracks_canny(self.test_image)
        self.assertIsInstance(edges, np.ndarray)
        self.assertEqual(edges.shape[:2], self.test_image.shape[:2])
    
    def test_edge_density_calculation(self):
        edges = self.detector.detect_cracks_canny(self.test_image)
        density = self.detector.calculate_edge_density(edges)
        self.assertIsInstance(density, float)
        self.assertGreaterEqual(density, 0.0)
        self.assertLessEqual(density, 1.0)
    
    def test_log_edge_detection(self):
        edges = self.detector.detect_cracks_log(self.test_image)
        self.assertIsInstance(edges, np.ndarray)
    
    def test_line_defect_detection(self):
        line_image = self.detector.detect_line_defects(self.test_image)
        self.assertIsInstance(line_image, np.ndarray)

if __name__ == '__main__':
    unittest.main()