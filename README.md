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


industrial-defect-inspector/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── config.py                      # Configuration settings
├── README.md                      # Project documentation
├── src/                           # Source code directory
│   ├── image_acquisition.py       # Image capture module
│   ├── preprocessing.py           # Image preprocessing
│   ├── edge_detection.py          # Edge-based defect detection
│   ├── texture_analysis.py        # Texture defect analysis
│   ├── color_analysis.py          # Color-based defect detection
│   ├── defect_classifier.py       # Defect classification
│   ├── report_generator.py        # Report generation
│   └── alert_system.py            # Alert notifications
├── static/                        # Static files (CSS, JS)
├── templates/                     # HTML templates
├── models/                        # Trained models
└── tests/                         # Test cases

🚀 Usage

Start the application: Run python app.py
Access the dashboard: Open http://localhost:5000 in your browser
Upload images or use live camera for inspection
View results and generate reports




## Key changes made:

1. **Removed duplicate content** that was repeated
2. **Fixed formatting** - proper markdown structure
3. **Removed incomplete lines** (like "Real-time" at the end of statement.md content)
4. **Organized sections** logically
5. **Added missing installation steps**
6. **Cleaned up project structure** to be more readable
7. **Separated content** - kept README.md as documentation and statement.md as problem statement

## To fix your file validation error:

1. **Save this as `README.md`** (not `.py` or any other extension)
2. **Ensure the file starts with proper markdown** (not code)
3. **Remove any Python code** from the README file
4. **Keep statement.md separate** for the problem statement content

This should resolve the file type validation error you were experiencing.
