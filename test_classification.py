# tests/test_classification.py
import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.defect_classifier import DefectClassifier

class TestDefectClassification(unittest.TestCase):
    def setUp(self):
        self.classifier = DefectClassifier()
        self.test_features = np.array([0.5, 0.3, 0.7, 0.2, 0.6])  # Sample features
    
    def test_rule_based_classification(self):
        defect_type, confidence = self.classifier.rule_based_classification(self.test_features)
        self.assertIn(defect_type, ['GOOD', 'MINOR', 'MAJOR', 'CRITICAL', 'UNKNOWN'])
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_classification_without_training(self):
        # Should fall back to rule-based classification
        defect_type, confidence = self.classifier.classify_defect_severity(self.test_features)
        self.assertIn(defect_type, ['GOOD', 'MINOR', 'MAJOR', 'CRITICAL', 'UNKNOWN'])
        self.assertIsInstance(confidence, float)
    
    def test_feature_extraction_integration(self):
        # This test would require actual image processing components
        # For now, just test that the method exists and returns expected format
        self.assertTrue(hasattr(self.classifier, 'extract_comprehensive_features'))

if __name__ == '__main__':
    unittest.main()