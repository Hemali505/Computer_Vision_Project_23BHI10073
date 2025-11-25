# src/report_generator.py
import csv
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from src.database_handler import DatabaseHandler

class ReportGenerator:
    def __init__(self):
        self.db_handler = DatabaseHandler()
    
    def generate_daily_report(self, date=None):
        """Generate daily defect report"""
        if date is None:
            date = datetime.now().date()
        
        defects = self.db_handler.get_defects_by_date(date)
        
        report_data = {
            'date': date.strftime('%Y-%m-%d'),
            'total_inspections': len(defects),
            'defects_found': len([d for d in defects if d[3] != 'GOOD']),
            'defect_rate': 0,
            'defect_breakdown': {
                'GOOD': 0,
                'MINOR': 0,
                'MAJOR': 0,
                'CRITICAL': 0
            },
            'defects': defects
        }
        
        # Calculate defect breakdown
        for defect in defects:
            defect_type = defect[3]
            report_data['defect_breakdown'][defect_type] += 1
        
        # Calculate defect rate
        if report_data['total_inspections'] > 0:
            report_data['defect_rate'] = report_data['defects_found'] / report_data['total_inspections']
        
        return report_data
    
    def generate_trend_report(self, days=7):
        """Generate trend report for specified number of days"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        trend_data = []
        current_date = start_date
        
        while current_date <= end_date:
            daily_report = self.generate_daily_report(current_date)
            trend_data.append(daily_report)
            current_date += timedelta(days=1)
        
        return trend_data
    
    def export_to_csv(self, report_data, filename=None):
        """Export report data to CSV"""
        if filename is None:
            filename = f"defect_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Date', 'Product ID', 'Defect Type', 'Confidence', 'Timestamp'])
            
            # Write data
            for defect in report_data['defects']:
                writer.writerow(defect)
        
        return filename
    
    def create_defect_chart(self, report_data, save_path=None):
        """Create visualization chart for defects"""
        if save_path is None:
            save_path = f"defect_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        defect_types = list(report_data['defect_breakdown'].keys())
        defect_counts = list(report_data['defect_breakdown'].values())
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(defect_types, defect_counts, color=['green', 'yellow', 'orange', 'red'])
        
        # Add value labels on bars
        for bar, count in zip(bars, defect_counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')
        
        plt.title(f'Defect Distribution - {report_data["date"]}')
        plt.xlabel('Defect Type')
        plt.ylabel('Number of Defects')
        plt.grid(axis='y', alpha=0.3)
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def generate_comprehensive_report(self, days=1):
        """Generate comprehensive report with multiple sections"""
        if days == 1:
            report_data = self.generate_daily_report()
        else:
            report_data = self.generate_trend_report(days)
        
        # Generate chart
        chart_path = self.create_defect_chart(
            report_data if days == 1 else report_data[-1]
        )
        
        comprehensive_report = {
            'summary': {
                'report_period': days,
                'total_defects': sum(item['defects_found'] for item in 
                                   (report_data if days > 1 else [report_data])),
                'average_defect_rate': np.mean([item['defect_rate'] for item in 
                                              (report_data if days > 1 else [report_data])])
            },
            'detailed_data': report_data,
            'chart_path': chart_path,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return comprehensive_report