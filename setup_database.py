# scripts/setup_database.py
#!/usr/bin/env python3

import sqlite3
import os
from config import Config

def setup_database():
    """Initialize the database with required tables"""
    print("Setting up Industrial Defect Inspector database...")
    
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('database/schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Execute schema creation
    cursor.executescript(schema_sql)
    
    # Insert some sample data for testing
    cursor.execute('''
        INSERT OR IGNORE INTO products (product_id, product_type, specification)
        VALUES 
        ('PROD001', 'Metal Plate', 'Steel plate 10mm thickness'),
        ('PROD002', 'Plastic Component', 'Injection molded ABS'),
        ('PROD003', 'Ceramic Tile', 'Glazed ceramic 30x30cm')
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database setup completed successfully!")
    print(f"Database location: {Config.DATABASE_PATH}")

if __name__ == '__main__':
    setup_database()