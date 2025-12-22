/**
 * Dashboard Optimization - Client-side data processing and caching
 * Preserves original visual layout while adding performance enhancements
 */

class DashboardOptimizer {
    constructor() {
        this.cache = new Map();
        this.refreshInterval = 5 * 60 * 1000; // 5 minutes
        this.lastUpdate = null;
    }

    // Initialize dashboard with minimal impact on layout
    async init() {
        // Only set up background data refresh, no visual changes
        this.setupBackgroundRefresh();
        console.log('Dashboard optimization initialized - preserving original layout');
    }

    // Setup background data refresh without visual changes
    setupBackgroundRefresh() {
        // Refresh data in background every 5 minutes
        setInterval(() => {
            this.refreshDataSilently();
        }, this.refreshInterval);
    }

    // Refresh data silently without updating UI
    async refreshDataSilently() {
        try {
            const response = await fetch('/api/dashboard-data/');
            const data = await response.json();
            
            // Cache data for potential use, but don't update UI
            this.cache.set('dashboard_data', {
                data: data,
                timestamp: Date.now()
            });
            
            console.log('Dashboard data refreshed in background');
        } catch (error) {
            console.log('Background data refresh failed:', error);
        }
    }

    // Export data functionality (available but not visible)
    exportData(format = 'csv') {
        const data = window.dashboardData;
        if (!data) {
            console.log('No dashboard data available for export');
            return;
        }

        if (format === 'csv') {
            this.exportToCSV(data);
        } else if (format === 'json') {
            this.exportToJSON(data);
        }
    }

    // Export to CSV
    exportToCSV(data) {
        let csv = 'Metric,Value\n';
        
        csv += `Visits Today,${data.visits_today || 0}\n`;
        csv += `Visits This Month,${data.visits_month || 0}\n`;
        csv += `Total Leads,${data.total_leads || 0}\n`;
        csv += `Conversion Rate,${data.conversion_rate || 0}%\n`;
        csv += `Converted Count,${data.converted_count || 0}\n`;
        
        if (data.leads_by_stage) {
            csv += '\nLeads by Stage\n';
            csv += 'Stage,Count\n';
            data.leads_by_stage.forEach(stage => {
                csv += `${stage.status},${stage.count}\n`;
            });
        }

        this.downloadFile(csv, 'dashboard_data.csv', 'text/csv');
    }

    // Export to JSON
    exportToJSON(data) {
        const json = JSON.stringify(data, null, 2);
        this.downloadFile(json, 'dashboard_data.json', 'application/json');
    }

    // Download file utility
    downloadFile(content, filename, contentType) {
        const blob = new Blob([content], { type: contentType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }
}

// Initialize dashboard optimizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for crmUtils to be available
    if (typeof window.crmUtils === 'undefined') {
        console.error('CRM Utils not loaded. Dashboard optimization disabled.');
        return;
    }
    
    window.dashboardOptimizer = new DashboardOptimizer();
    
    // Check if we're on the dashboard page
    if (document.querySelector('.dashboard') || document.getElementById('dashboard-content') || window.dashboardData) {
        window.dashboardOptimizer.init();
    }
});
