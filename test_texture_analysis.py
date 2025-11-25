# tests/test_texture_analysis.py
import unittest
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.texture_analysis import TextureAnalyzer

class TestTextureAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextureAnalyzer()
        # Create test texture image
        self.test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    def test_haralick_features(self):
        features = self.analyzer.extract_haralick_features(self.test_image)
        self.assertIsInstance(features, np.ndarray)
        self.assertEqual(len(features), 13)  # Haralick features count
    
    def test_texture_defect_analysis(self):
        result, features = self.analyzer.analyze_texture_defects(self.test_image)
        self.assertIn(result, ['GOOD', 'DEFECT'])
        self.assertIsInstance(features, np.ndarray)
    
    def test_lbp_features(self):
        features = self.analyzer.compute_lbp_features(self.test_image)
        self.assertIsInstance(features, np.ndarray)
    
    def test_texture_anomaly_detection(self):
        anomaly_score, features = self.analyzer.detect_texture_anomalies(self.test_image)
        self.assertIsInstance(anomaly_score, float)
        self.assertIsInstance(features, np.ndarray)

if __name__ == '__main__':
    unittest.main()