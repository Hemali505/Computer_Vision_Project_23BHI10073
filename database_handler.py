# src/database_handler.py
import sqlite3
import os
from datetime import datetime
from config import Config

class DatabaseHandler:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        os.makedirs('database', exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create defects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS defects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                defect_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                edge_density REAL,
                texture_features TEXT,
                image_path TEXT
            )
        ''')
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE NOT NULL,
                product_type TEXT,
                specification TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create system_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_level TEXT,
                module TEXT,
                message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_defect(self, defect_type, confidence, additional_data=None):
        """Record a new defect in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        product_id = additional_data.get('product_id', 'UNKNOWN') if additional_data else 'UNKNOWN'
        edge_density = additional_data.get('edge_density', 0) if additional_data else 0
        texture_features = str(additional_data.get('texture_features', [])) if additional_data else '[]'
        image_path = additional_data.get('image_path', '') if additional_data else ''
        
        cursor.execute('''
            INSERT INTO defects (product_id, defect_type, confidence, edge_density, texture_features, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, defect_type, confidence, edge_density, texture_features, image_path))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def get_recent_defects(self, limit=50):
        """Get recent defect records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, defect_type, confidence, timestamp, edge_density
            FROM defects 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        defects = cursor.fetchall()
        conn.close()
        
        return defects
    
    def get_defects_by_date(self, date):
        """Get defects for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, defect_type, confidence, timestamp, edge_density
            FROM defects 
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp DESC
        ''', (date.strftime('%Y-%m-%d'),))
        
        defects = cursor.fetchall()
        conn.close()
        
        return defects
    
    def get_defect_statistics(self, days=7):
        """Get defect statistics for dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total defects today
        cursor.execute('''
            SELECT COUNT(*) FROM defects 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        today_defects = cursor.fetchone()[0]
        
        # Defect breakdown
        cursor.execute('''
            SELECT defect_type, COUNT(*) 
            FROM defects 
            WHERE DATE(timestamp) = DATE('now')
            GROUP BY defect_type
        ''')
        defect_breakdown = dict(cursor.fetchall())
        
        # Weekly trend
        cursor.execute('''
            SELECT DATE(timestamp), COUNT(*) 
            FROM defects 
            WHERE timestamp >= DATE('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY DATE(timestamp)
        ''')
        weekly_trend = cursor.fetchall()
        
        conn.close()
        
        return {
            'today_defects': today_defects,
            'defect_breakdown': defect_breakdown,
            'weekly_trend': weekly_trend
        }
    
    def get_critical_defects(self, hours=24):
        """Get critical defects from last specified hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, defect_type, confidence, timestamp
            FROM defects 
            WHERE defect_type IN ('MAJOR', 'CRITICAL')
            AND timestamp >= DATETIME('now', ?)
            ORDER BY timestamp DESC
        ''', (f'-{hours} hours',))
        
        critical_defects = cursor.fetchall()
        conn.close()
        
        return critical_defects
    
    def log_system_event(self, log_level, module, message):
        """Log system event to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        