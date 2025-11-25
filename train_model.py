# scripts/train_model.py
#!/usr/bin/env python3

import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import os
from config import Config

def train_sample_model():
    """Train a sample defect classification model with synthetic data"""
    print("Training defect classification model...")
    
    # Create sample training data (in real scenario, this would come from labeled defects)
    np.random.seed(42)
    
    # Generate synthetic features for different defect types
    n_samples = 1000
    
    # GOOD products: low edge density, low texture variation
    good_features = np.column_stack([
        np.random.uniform(0.0, 0.2, n_samples//4),  # edge_density
        np.random.uniform(0.0, 0.3, n_samples//4),  # texture_contrast
        np.random.uniform(0.7, 1.0, n_samples//4),  # texture_correlation
        np.random.uniform(0.8, 1.0, n_samples//4),  # texture_energy
        np.random.uniform(0.8, 1.0, n_samples//4),  # texture_homogeneity
        np.random.uniform(0.0, 0.3, n_samples//4)   # defect_probability
    ])
    
    # MINOR defects: medium edge density, some texture issues
    minor_features = np.column_stack([
        np.random.uniform(0.2, 0.4, n_samples//4),
        np.random.uniform(0.3, 0.6, n_samples//4),
        np.random.uniform(0.4, 0.7, n_samples//4),
        np.random.uniform(0.6, 0.8, n_samples//4),
        np.random.uniform(0.6, 0.8, n_samples//4),
        np.random.uniform(0.3, 0.6, n_samples//4)
    ])
    
    # MAJOR defects: high edge density, significant texture issues
    major_features = np.column_stack([
        np.random.uniform(0.4, 0.7, n_samples//4),
        np.random.uniform(0.6, 0.9, n_samples//4),
        np.random.uniform(0.2, 0.5, n_samples//4),
        np.random.uniform(0.3, 0.6, n_samples//4),
        np.random.uniform(0.3, 0.6, n_samples//4),
        np.random.uniform(0.6, 0.8, n_samples//4)
    ])
    
    # CRITICAL defects: very high edge density, severe texture issues
    critical_features = np.column_stack([
        np.random.uniform(0.7, 1.0, n_samples//4),
        np.random.uniform(0.8, 1.0, n_samples//4),
        np.random.uniform(0.0, 0.3, n_samples//4),
        np.random.uniform(0.0, 0.3, n_samples//4),
        np.random.uniform(0.0, 0.3, n_samples//4),
        np.random.uniform(0.8, 1.0, n_samples//4)
    ])
    
    # Combine all features and labels
    X = np.vstack([good_features, minor_features, major_features, critical_features])
    y = ['GOOD'] * len(good_features) + ['MINOR'] * len(minor_features) + \
        ['MAJOR'] * len(major_features) + ['CRITICAL'] * len(critical_features)
    
    # Train SVM classifier
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    svm_classifier = SVC(probability=True, random_state=42)
    svm_classifier.fit(X_scaled, y)
    
    # Create models directory if it doesn't exist
    os.makedirs(Config.MODEL_PATH, exist_ok=True)
    
    # Save the trained model and scaler
    model_data = {
        'svm_classifier': svm_classifier,
        'scaler': scaler,
        'feature_names': ['edge_density', 'contrast', 'correlation', 'energy', 'homogeneity', 'defect_probability']
    }
    
    with open(os.path.join(Config.MODEL_PATH, 'svm_classifier.pkl'), 'wb') as f:
        pickle.dump(model_data, f)
    
    print("Model training completed!")
    print(f"Model saved to: {os.path.join(Config.MODEL_PATH, 'svm_classifier.pkl')}")
    print(f"Training samples: {len(X)}")
    print(f"Classes: {set(y)}")

if __name__ == '__main__':
    train_sample_model()