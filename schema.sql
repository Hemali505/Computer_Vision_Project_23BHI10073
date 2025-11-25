# database/schema.sql
-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE NOT NULL,
    product_type TEXT,
    specification TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Defects table
CREATE TABLE IF NOT EXISTS defects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT,
    defect_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edge_density REAL,
    texture_features TEXT,
    image_path TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- System logs table
CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    log_level TEXT,
    module TEXT,
    message TEXT
);

-- Quality reports table
CREATE TABLE IF NOT EXISTS quality_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATE NOT NULL,
    total_inspected INTEGER,
    defects_found INTEGER,
    defect_rate REAL,
    major_defects INTEGER,
    critical_defects INTEGER
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_defects_timestamp ON defects(timestamp);
CREATE INDEX IF NOT EXISTS idx_defects_type ON defects(defect_type);
CREATE INDEX IF NOT EXISTS idx_defects_product ON defects(product_id);
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON system_logs(timestamp);