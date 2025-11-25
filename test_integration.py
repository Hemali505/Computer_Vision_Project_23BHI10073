# tests/test_integration.py
import unittest
import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import ImagePreprocessor
from src.edge_detection import EdgeDefectDetector
from src.texture_analysis import TextureAnalyzer
from src.defect_classifier import DefectClassifier

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.preprocessor = ImagePreprocessor()
        self.edge_detector = EdgeDefectDetector()
        self.texture_analyzer = TextureAnalyzer()
        self.classifier = DefectClassifier()
        
        # Create a more realistic test image with various features
        self.test_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        # Add some structure to the image
        self.test_image[50:70, 50:150] = 0  # Dark rectangle
        self.test_image[100:102, :] = 255   # White line
    
    def test_full_processing_pipeline(self):
        # Test the complete processing pipeline
        processed_image = self.preprocessor.preprocess(self.test_image)
        self.assertIsNotNone(processed_image)
        
        edges = self.edge_detector.detect_cracks_canny(processed_image)
        self.assertIsNotNone(edges)
        
        texture_result, texture_features = self.texture_analyzer.analyze_texture_defects(processed_image)
        self.assertIsNotNone(texture_result)
        self.assertIsNotNone(texture_features)
        
        # Test classification with combined features
        edge_density = self.edge_detector.calculate_edge_density(edges)
        combined_features = np.concatenate([[edge_density], texture_features])
        
        defect_type, confidence = self.classifier.classify_defect_severity(combined_features)
        self.assertIn(defect_type, ['GOOD', 'MINOR', 'MAJOR', 'CRITICAL', 'UNKNOWN'])
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_image_quality_after_processing(self):
        processed_image = self.preprocessor.preprocess(self.test_image)
        
        # Check that processed image has valid properties
        self.assertIsInstance(processed_image, np.ndarray)
        self.assertEqual(len(processed_image.shape), 3)  # Should be 3-channel
        self.assertEqual(processed_image.shape[2], 3)    # RGB channels
        
        # Check image data type
        self.assertEqual(processed_image.dtype, np.uint8)
        
        # Check that image is not empty
        self.assertGreater(np.mean(processed_image), 0)

if __name__ == '__main__':
    unittest.main()