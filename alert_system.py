# src/alert_system.py
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import json
from datetime import datetime

class AlertSystem:
    def __init__(self, config):
        self.config = config
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_defect_alert(self, defect_data):
        """Send alert for critical defects"""
        if defect_data['defect_type'] in ['MAJOR', 'CRITICAL']:
            subject = f"🚨 DEFECT ALERT: {defect_data['defect_type']} Defect Detected"
            message = self.create_alert_message(defect_data)
            
            # Send email alert
            self.send_email_alert(subject, message)
            
            # Log alert
            self.log_alert(defect_data)
    
    def create_alert_message(self, defect_data):
        """Create alert message content"""
        message = f"""
        INDUSTRIAL DEFECT ALERT SYSTEM
        ==============================
        
        Critical Defect Detected!
        
        Details:
        - Defect Type: {defect_data['defect_type']}
        - Confidence: {defect_data['confidence']:.2%}
        - Timestamp: {defect_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
        - Edge Density: {defect_data.get('edge_density', 0):.4f}
        - Texture Analysis: {defect_data.get('texture_analysis', 'N/A')}
        
        Immediate Action Required!
        
        Please inspect the product and take necessary quality control measures.
        
        This is an automated alert from the Industrial Defect Inspection System.
        """
        return message
    
    def send_email_alert(self, subject, message):
        """Send email alert to configured recipients"""
        try:
            # Email configuration (should be in config in production)
            sender_email = "defect.alerts@company.com"
            receiver_email = self.config.ALERT_EMAIL
            password = "your-email-password"  # Use app-specific password
            
            # Create message
            msg = MimeMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            
            # Add message body
            msg.attach(MimeText(message, 'plain'))
            
            # Create server connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(sender_email, password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            print(f"Alert email sent to {receiver_email}")
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")
    
    def log_alert(self, defect_data):
        """Log alert to file or database"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'defect_type': defect_data['defect_type'],
            'confidence': defect_data['confidence'],
            'action': 'ALERT_SENT'
        }
        
        # Append to log file
        with open('alert_log.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def check_alert_conditions(self, defect_data):
        """Check if alert conditions are met"""
        if defect_data['defect_type'] == 'CRITICAL':
            return True
        elif (defect_data['defect_type'] == 'MAJOR' and 
              defect_data['confidence'] > self.config.ALERT_THRESHOLD):
            return True
        return False