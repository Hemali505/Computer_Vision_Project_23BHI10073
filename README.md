# Computer_Vision_Project_23BHI10073

# README.md
# Industrial Defect Inspector

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-brightgreen)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

An advanced computer vision system for automated industrial defect detection using machine learning and image processing techniques.

## 🏭 Features

### 🔍 Defect Detection
- **Edge-based Detection**: Canny, Laplacian of Gaussian for crack detection
- **Texture Analysis**: Haralick features, LBP for surface defects
- **Color Analysis**: Discoloration and stain detection
- **Multi-algorithm Approach**: Combined analysis for accurate results

### 📊 Classification & Reporting
- **Defect Severity Classification**: GOOD, MINOR, MAJOR, CRITICAL
- **Real-time Processing**: Instant defect analysis
- **Comprehensive Reports**: Daily, weekly, and trend analysis
- **Data Export**: CSV reports with detailed metrics

### 🚨 Alert System
- **Critical Defect Alerts**: Immediate notifications for major issues
- **Email Notifications**: Automated alert system
- **Dashboard Monitoring**: Real-time defect tracking
- **Historical Analysis**: Trend monitoring and pattern detection

### 💻 User Interface
- **Web-based Dashboard**: Accessible from any device
- **Live Camera Support**: Real-time product inspection
- **Image Upload**: Batch processing capability
- **Mobile Responsive**: Works on all screen sizes

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Webcam (for live inspection)
- 4GB RAM minimum (8GB recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/industrial-defect-inspector.git
cd industrial-defect-inspector

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate


industrial-defect-inspector/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── config.py                      # Configuration settings
├── README.md                      # Project documentation
├── statement.md                   # Problem statement & scope
│
├── src/                           # Source code directory
│   ├── image_acquisition.py       # Image capture module
│   ├── preprocessing.py           # Image preprocessing
│   ├── edge_detection.py          # Edge-based defect detection
│   ├── texture_analysis.py        # Texture defect analysis
│   ├── color_analysis.py          # Color-based defect detection
│   ├── defect_classifier.py       # Defect classification
│   ├── report_generator.py        # Report generation
│   ├── alert_system.py            # Alert notifications
│   └── utils/                     # Utility functions
│       ├── image_utils.py
│       ├── validation.py
│       └── constants.py
│
├── models/                        # Trained models
│   ├── kmeans_model.pkl
│   ├── svm_classifier.pkl
│   └── feature_scaler.pkl
│
├── static/                        # Static files
│   ├── css/style.css
│   ├── js/main.js
│   ├── js/inspection.js
│   └── js/reports.js
│
├── templates/                     # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── inspection.html
│   ├── reports.html
│   └── alerts.html
│
├── database/                      # Database files
│   ├── defects.db
│   └── schema.sql
│
├── tests/                         # Test cases
│   ├── test_edge_detection.py
│   ├── test_texture_analysis.py
│   ├── test_classification.py
│   └── test_integration.py
│
└── scripts/                       # Utility scripts
    ├── setup_database.py
    ├── train_model.py
    └── backup_data.py





class Config:
    # Image processing
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600
    
    # Defect thresholds
    MINOR_DEFECT_THRESHOLD = 0.3
    MAJOR_DEFECT_THRESHOLD = 0.6
    CRITICAL_DEFECT_THRESHOLD = 0.8
    
    # Alert settings
    ALERT_EMAIL = 'quality@company.com'
    ALERT_THRESHOLD = 0.7

🔧 API Endpoints

GET / - Main dashboard
GET/POST /inspect - Product inspection
GET /reports - Defect reports
GET /alerts - Critical defect alerts
GET /export/csv - Export data to CSV



🔒 Security Features

Secure image processing pipeline
Input validation and sanitization
Database encryption
Secure file upload handling
XSS protection


# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app


🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

Fork the repository
Create feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open Pull Request






# statement.md
# Industrial Defect Inspector - Problem Statement & Scope

## 🎯 Problem Statement

Manual visual inspection in manufacturing industries is plagued by inefficiency, subjectivity, and human error. Current quality control processes face significant challenges:

### Current Challenges:
1. **Human Fatigue**: Inspectors suffer from visual fatigue, leading to decreased accuracy over time
2. **Subjectivity**: Different inspectors may have varying standards and interpretations
3. **Inconsistency**: Inspection quality fluctuates based on time of day, workload, and individual expertise
4. **Speed Limitations**: Manual inspection cannot keep pace with high-speed production lines
5. **Documentation Issues**: Poor record-keeping and difficulty in tracking defect patterns
6. **Training Costs**: Significant time and resources required to train skilled inspectors
7. **Scalability Problems**: Difficult to maintain consistent quality across multiple production lines

### Impact on Business:
- **Product Quality**: Inconsistent inspection leads to defective products reaching customers
- **Cost Overruns**: Rework, returns, and warranty claims increase operational costs
- **Reputation Damage**: Quality issues harm brand reputation and customer trust
- **Compliance Risks**: Failure to meet industry quality standards and regulations
- **Competitive Disadvantage**: Inability to compete on quality and reliability

## 🚀 Project Scope

### Primary Objectives:
1. **Automate Defect Detection**: Replace manual inspection with computer vision algorithms
2. **Ensure Consistency**: Provide uniform inspection standards across all products
3. **Increase Efficiency**: Process products faster than human capabilities
4. **Provide Analytics**: Generate comprehensive reports and trend analysis
5. **Enable Real-time Monitoring**: Instant detection and alerting for critical defects

### Target Industries:
- **Automotive**: Parts inspection, surface quality control
- **Electronics**: PCB inspection, component placement
- **Textiles**: Fabric defect detection, pattern consistency
- **Metalworking**: Surface cracks, corrosion detection
- **Plastics**: Injection molding defects, surface imperfections
- **Packaging**: Print quality, structural integrity

### System Capabilities:

#### Core Features:
- **Multi-modal Detection**: Combine edge, texture, and color analysis
- **Real-time
