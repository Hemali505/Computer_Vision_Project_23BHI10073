// static/js/inspection.js
// Inspection page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const inspectionForm = document.getElementById('inspectionForm');
    const productImage = document.getElementById('productImage');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const analysisDetails = document.getElementById('analysisDetails');
    const startCamera = document.getElementById('startCamera');
    const captureFrame = document.getElementById('captureFrame');
    const cameraFeed = document.getElementById('cameraFeed');
    const captureCanvas = document.getElementById('captureCanvas');
    
    let stream = null;

    // File upload inspection
    inspectionForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!productImage.files.length) {
            showNotification('Please select an image file', 'warning');
            return;
        }

        await analyzeImage(productImage.files[0]);
    });

    // Camera functionality
    startCamera.addEventListener('click', async function() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                } 
            });
            cameraFeed.srcObject = stream;
            captureFrame.disabled = false;
            startCamera.disabled = true;
            showNotification('Camera started successfully', 'success');
        } catch (err) {
            console.error('Error accessing camera:', err);
            showNotification('Error accessing camera: ' + err.message, 'danger');
        }
    });

    captureFrame.addEventListener('click', function() {
        if (!stream) {
            showNotification('Please start camera first', 'warning');
            return;
        }

        const context = captureCanvas.getContext('2d');
        captureCanvas.width = cameraFeed.videoWidth;
        captureCanvas.height = cameraFeed.videoHeight;
        context.drawImage(cameraFeed, 0, 0);

        captureCanvas.toBlob(async function(blob) {
            await analyzeImage(blob);
        }, 'image/jpeg', 0.8);
    });

    async function analyzeImage(imageFile) {
        const originalText = analyzeBtn.innerHTML;
        analyzeBtn.innerHTML = '<span class="loading"></span> Analyzing...';
        analyzeBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('image', imageFile);
            
            if (document.getElementById('productId').value) {
                formData.append('product_id', document.getElementById('productId').value);
            }

            const response = await fetch('/inspect', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const results = await response.json();
            displayResults(results);

        } catch (error) {
            console.error('Error analyzing image:', error);
            showNotification('Error analyzing image: ' + error.message, 'danger');
        } finally {
            analyzeBtn.innerHTML = originalText;
            analyzeBtn.disabled = false;
        }
    }

    function displayResults(results) {
        const defectClass = `defect-${results.defect_type.toLowerCase()}`;
        const confidencePercent = (results.confidence * 100).toFixed(1);
        
        let alertClass = 'alert-success';
        if (results.defect_type === 'MINOR') alertClass = 'alert-warning';
        if (results.defect_type === 'MAJOR') alertClass = 'alert-warning';
        if (results.defect_type === 'CRITICAL') alertClass = 'alert-danger';

        resultsContainer.innerHTML = `
            <div class="alert ${alertClass} ${defectClass}">
                <h4 class="alert-heading">
                    ${getDefectIcon(results.defect_type)} 
                    ${results.defect_type} Defect
                </h4>
                <p class="mb-0">
                    <strong>Confidence:</strong> ${confidencePercent}%<br>
                    <strong>Edge Density:</strong> ${(results.edge_density * 100).toFixed(2)}%<br>
                    <strong>Texture Analysis:</strong> ${results.texture_analysis}
                </p>
            </div>
        `;

        // Display detailed analysis
        analysisDetails.innerHTML = `
            <h6>Detailed Analysis:</h6>
            <ul class="list-unstyled">
                <li><strong>Edge Density:</strong> ${results.edge_density.toFixed(4)}</li>
                <li><strong>Texture Features:</strong></li>
                <ul>
                    ${results.texture_features ? results.texture_features.map((feature, index) => 
                        `<li>Feature ${index + 1}: ${feature.toFixed(4)}</li>`
                    ).join('') : '<li>No texture features available</li>'}
                </ul>
            </ul>
        `;

        // Show appropriate message based on defect type
        let actionMessage = '';
        switch(results.defect_type) {
            case 'GOOD':
                actionMessage = '✅ Product meets quality standards. No action required.';
                break;
            case 'MINOR':
                actionMessage = '⚠️ Minor defects detected. Review recommended.';
                break;
            case 'MAJOR':
                actionMessage = '🚨 Major defects detected. Immediate review required.';
                break;
            case 'CRITICAL':
                actionMessage = '🚨 CRITICAL defects detected! Remove from production line immediately!';
                break;
        }

        if (actionMessage) {
            resultsContainer.innerHTML += `<div class="alert alert-info mt-3">${actionMessage}</div>`;
        }

        showNotification('Analysis completed successfully', 'success');
    }

    function getDefectIcon(defectType) {
        const icons = {
            'GOOD': '✅',
            'MINOR': '⚠️',
            'MAJOR': '🚨',
            'CRITICAL': '🚨'
        };
        return icons[defectType] || '❓';
    }

    // Clean up camera stream when leaving page
    window.addEventListener('beforeunload', function() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });
});