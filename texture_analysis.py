# src/texture_analysis.py
import cv2
import numpy as np
import mahotas as mt
from sklearn.cluster import KMeans

class TextureAnalyzer:
    def __init__(self):
        self.kmeans = KMeans(n_clusters=3, random_state=42)
    
    def extract_haralick_features(self, image):
        """Extract Haralick texture features"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate Haralick features
        features = mt.features.haralick(gray)
        return features.mean(axis=0)  # Return mean of all directions
    
    def analyze_texture_defects(self, image):
        """Analyze texture for defects using GLCM and clustering"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate GLCM and Haralick features
        glcm = mt.features.haralick(gray)
        
        # Extract important texture features
        contrast = glcm[:, 0].mean()
        correlation = glcm[:, 1].mean()
        energy = glcm[:, 2].mean()
        homogeneity = glcm[:, 3].mean()
        
        # Classify based on texture features
        defect_probability = self.calculate_defect_probability(
            contrast, correlation, energy, homogeneity
        )
        
        if defect_probability > 0.5:
            return "DEFECT", np.array([contrast, correlation, energy, homogeneity, defect_probability])
        else:
            return "GOOD", np.array([contrast, correlation, energy, homogeneity, defect_probability])
    
    def calculate_defect_probability(self, contrast, correlation, energy, homogeneity):
        """Calculate probability of defect based on texture features"""
        # Higher contrast often indicates defects
        contrast_score = min(contrast / 1000, 1.0)
        
        # Lower energy often indicates defects
        energy_score = 1.0 - min(energy * 100, 1.0)
        
        # Lower homogeneity often indicates defects
        homogeneity_score = 1.0 - min(homogeneity * 2, 1.0)
        
        # Weighted combination
        defect_prob = (0.5 * contrast_score + 0.3 * energy_score + 0.2 * homogeneity_score)
        return defect_prob
    
    def compute_lbp_features(self, image, radius=3, points=24):
        """Compute Local Binary Pattern features"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Compute LBP image
        lbp = mt.features.lbp(gray, radius, points)
        
        # Compute LBP histogram
        hist, _ = np.histogram(lbp, bins=points+2, range=(0, points+2))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-7)  # Normalize
        
        return hist
    
    def detect_texture_anomalies(self, image):
        """Detect texture anomalies using multiple methods"""
        haralick_features = self.extract_haralick_features(image)
        lbp_features = self.compute_lbp_features(image)
        
        # Combine features
        combined_features = np.concatenate([haralick_features, lbp_features])
        
        # Simple anomaly detection (can be replaced with ML model)
        anomaly_score = np.std(combined_features) / np.mean(combined_features)
        
        return anomaly_score, combined_features