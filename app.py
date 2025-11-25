# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import cv2
import numpy as np
from src.image_acquisition import ImageCapture
from src.preprocessing import ImagePreprocessor
from src.edge_detection import EdgeDefectDetector
from src.texture_analysis import TextureAnalyzer
from src.defect_classifier import DefectClassifier
from src.database_handler import DatabaseHandler

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize components
db_handler = DatabaseHandler()
image_preprocessor = ImagePreprocessor()
edge_detector = EdgeDefectDetector()
texture_analyzer = TextureAnalyzer()
defect_classifier = DefectClassifier()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/inspect', methods=['GET', 'POST'])
def inspect():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image uploaded", 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return "No selected file", 400
        
        if image_file:
            # Save uploaded image
            filename = f"inspect_{np.random.randint(1000, 9999)}.jpg"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            
            # Process image for defects
            image = cv2.imread(image_path)
            results = process_image_for_defects(image)
            
            return jsonify(results)
    
    return render_template('inspection.html')

@app.route('/dashboard')
def dashboard():
    stats = db_handler.get_defect_statistics()
    return render_template('dashboard.html', stats=stats)

@app.route('/reports')
def reports():
    defects = db_handler.get_recent_defects()
    return render_template('reports.html', defects=defects)

@app.route('/alerts')
def alerts():
    critical_defects = db_handler.get_critical_defects()
    return render_template('alerts.html', defects=critical_defects)

def process_image_for_defects(image):
    """Main defect detection pipeline"""
    results = {}
    
    # Preprocess image
    processed_image = image_preprocessor.preprocess(image)
    
    # Edge-based defect detection
    edge_defects = edge_detector.detect_cracks_canny(processed_image)
    edge_density = np.sum(edge_defects) / (255 * edge_defects.size)
    results['edge_density'] = edge_density
    
    # Texture analysis
    texture_result, texture_features = texture_analyzer.analyze_texture_defects(processed_image)
    results['texture_analysis'] = texture_result
    results['texture_features'] = texture_features.tolist()
    
    # Combine features for classification
    combined_features = np.concatenate([
        [edge_density],
        texture_features
    ])
    
    # Classify defect
    defect_type, confidence = defect_classifier.classify_defect_severity(combined_features)
    results['defect_type'] = defect_type
    results['confidence'] = confidence
    
    # Save to database
    db_handler.record_defect(defect_type, confidence, results)
    
    return results

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)