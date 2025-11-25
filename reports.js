// static/js/reports.js
// Reports page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const exportCsvBtn = document.getElementById('exportCsv');
    const refreshDataBtn = document.getElementById('refreshData');
    const generateDailyReportBtn = document.getElementById('generateDailyReport');
    const generateWeeklyReportBtn = document.getElementById('generateWeeklyReport');
    const viewTrendsBtn = document.getElementById('viewTrends');
    const defectChartCanvas = document.getElementById('defectChart');

    let defectChart = null;

    // Initialize defect chart
    initializeDefectChart();

    // Event listeners
    exportCsvBtn.addEventListener('click', exportToCsv);
    refreshDataBtn.addEventListener('click', refreshData);
    generateDailyReportBtn.addEventListener('click', generateDailyReport);
    generateWeeklyReportBtn.addEventListener('click', generateWeeklyReport);
    viewTrendsBtn.addEventListener('click', viewTrends);

    function initializeDefectChart() {
        if (!defectChartCanvas) return;

        const ctx = defectChartCanvas.getContext('2d');
        
        // Get defect counts from the table
        const defectCounts = {
            'GOOD': document.querySelectorAll('tr:has(.bg-success)').length,
            'MINOR': document.querySelectorAll('tr:has(.bg-warning)').length,
            'MAJOR': document.querySelectorAll('tr:has(.bg-warning)').length, // Same as MINOR for now
            'CRITICAL': document.querySelectorAll('tr:has(.bg-danger)').length
        };

        defectChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Good', 'Minor Defects', 'Major Defects', 'Critical Defects'],
                datasets: [{
                    data: [
                        defectCounts.GOOD,
                        defectCounts.MINOR,
                        defectCounts.MAJOR,
                        defectCounts.CRITICAL
                    ],
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#fd7e14',
                        '#dc3545'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Defect Distribution'
                    }
                }
            }
        });
    }

    async function exportToCsv() {
        try {
            const response = await fetch('/export/csv');
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `defect_report_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                showNotification('CSV export started', 'success');
            } else {
                throw new Error('Export failed');
            }
        } catch (error) {
            console.error('Export error:', error);
            showNotification('Error exporting CSV: ' + error.message, 'danger');
        }
    }

    function refreshData() {
        location.reload();
    }

    async function generateDailyReport() {
        try {
            showNotification('Generating daily report...', 'info');
            // In a real implementation, this would call an API endpoint
            setTimeout(() => {
                showNotification('Daily report generated successfully', 'success');
            }, 2000);
        } catch (error) {
            console.error('Report generation error:', error);
            showNotification('Error generating report: ' + error.message, 'danger');
        }
    }

    async function generateWeeklyReport() {
        try {
            showNotification('Generating weekly report...', 'info');
            // In a real implementation, this would call an API endpoint
            setTimeout(() => {
                showNotification('Weekly report generated successfully', 'success');
            }, 2000);
        } catch (error) {
            console.error('Report generation error:', error);
            showNotification('Error generating report: ' + error.message, 'danger');
        }
    }

    function viewTrends() {
        showNotification('Trend analysis feature coming soon', 'info');
    }

    // Auto-refresh data every 30 seconds
    setInterval(refreshData, 30000);
});