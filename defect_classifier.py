# src/defect_classifier.py
import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

class DefectClassifier:
    def __init__(self):
        self.kmeans = None
        self.svm_classifier = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train_kmeans(self, features, n_clusters=3):
        """Train K-Means clustering for defect categorization"""
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        scaled_features = self.scaler.fit_transform(features)
        self.kmeans.fit(scaled_features)
        return self.kmeans.labels_
    
    def train_svm_classifier(self, features, labels):
        """Train SVM classifier for defect severity"""
        scaled_features = self.scaler.fit_transform(features)
        self.svm_classifier = SVC(probability=True, random_state=42)
        self.svm_classifier.fit(scaled_features, labels)
        self.is_trained = True
    
    def classify_defect_severity(self, features):
        """Classify defect severity"""
        if not self.is_trained or self.svm_classifier is None:
            # Fallback to rule-based classification
            return self.rule_based_classification(features)
        
        try:
            scaled_features = self.scaler.transform([features])
            prediction = self.svm_classifier.predict(scaled_features)
            confidence = np.max(self.svm_classifier.predict_proba(scaled_features))
            return prediction[0], confidence
        except Exception as e:
            print(f"Classification error: {e}")
            return self.rule_based_classification(features)
    
    def rule_based_classification(self, features):
        """Rule-based defect classification as fallback"""
        if len(features) >= 5:
            edge_density = features[0]
            texture_probability = features[4] if len(features) > 4 else 0
            
            # Combine scores
            combined_score = (edge_density + texture_probability) / 2
            
            if combined_score < 0.3:
                return "GOOD", 1.0 - combined_score
            elif combined_score < 0.6:
                return "MINOR", combined_score
            elif combined_score < 0.8:
                return "MAJOR", combined_score
            else:
                return "CRITICAL", combined_score
        else:
            return "UNKNOWN", 0.5
    
    def extract_comprehensive_features(self, image, edge_detector, texture_analyzer, color_analyzer):
        """Extract comprehensive features for classification"""
        # Edge features
        edges = edge_detector.detect_cracks_canny(image)
        edge_density = np.sum(edges) / (255 * edges.size)
        
        # Texture features
        texture_result, texture_features = texture_analyzer.analyze_texture_defects(image)
        
        # Color features
        color_variation, color_stds = color_analyzer.analyze_color_consistency(image)
        
        # Combine all features
        combined_features = np.concatenate([
            [edge_density],
            texture_features,
            [color_variation],
            color_stds
        ])
        
        return combined_features
    
    def save_model(self, model_path):
        """Save trained model to file"""
        if self.svm_classifier is not None:
            with open(model_path, 'wb') as f:
                pickle.dump({
                    'svm_classifier': self.svm_classifier,
                    'scaler': self.scaler,
                    'is_trained': self.is_trained
                }, f)
    
    def load_model(self, model_path):
        """Load trained model from file"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.svm_classifier = model_data['svm_classifier']
                self.scaler = model_data['scaler']
                self.is_trained = model_data['is_trained']
        except Exception as e:
            print(f"Error loading model: {e}")