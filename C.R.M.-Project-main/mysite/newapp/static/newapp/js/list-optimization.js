/**
 * List Page Optimization - Client-side filtering, sorting, and pagination
 * Reduces API calls for list operations
 */

class ListOptimizer {
    constructor() {
        this.cache = new Map();
        this.currentPage = 1;
        this.pageSize = 20;
        this.filters = {};
        this.sortField = null;
        this.sortDirection = 'asc';
        this.searchTerm = '';
        this.debounceTimer = null;
    }

    // Initialize list optimization
    init() {
        this.setupSearch();
        this.setupFilters();
        this.setupSorting();
        this.setupPagination();
        this.setupBulkActions();
        this.loadInitialData();
    }

    // Load initial data with caching
    async loadInitialData() {
        const cacheKey = this.getListCacheKey();
        
        try {
            let data = window.crmUtils.cache.get(cacheKey);
            
            if (!data) {
                data = await this.fetchListData();
                window.crmUtils.cache.set(cacheKey, data);
            }
            
            this.renderList(data);
            this.updatePagination(data.total_count);
        } catch (error) {
            console.error('Failed to load list data:', error);
            window.crmUtils.showMessage('Failed to load data', 'error');
        }
    }

    // Get list cache key
    getListCacheKey() {
        const params = new URLSearchParams(window.location.search);
        return `list_${window.location.pathname}_${params.toString()}`;
    }

    // Fetch list data from API
    async fetchListData() {
        const params = new URLSearchParams({
            page: this.currentPage,
            page_size: this.pageSize,
            search: this.searchTerm,
            sort_field: this.sortField,
            sort_direction: this.sortDirection,
            ...this.filters
        });

        const response = await fetch(`${window.location.pathname}?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        return await response.json();
    }

    // Setup search functionality
    setupSearch() {
        const searchInput = document.getElementById('search-input');
        const searchBtn = document.getElementById('search-btn');

        if (searchInput) {
            // Debounced search
            searchInput.addEventListener('input', (e) => {
                clearTimeout(this.debounceTimer);
                this.debounceTimer = setTimeout(() => {
                    this.handleSearch(e.target.value);
                }, 300);
            });

            // Enter key search
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.handleSearch(e.target.value);
                }
            });
        }

        if (searchBtn) {
            searchBtn.addEventListener('click', () => {
                this.handleSearch(searchInput?.value || '');
            });
        }
    }

    // Handle search
    async handleSearch(term) {
        this.searchTerm = term;
        this.currentPage = 1;
        await this.loadInitialData();
        this.updateURL();
    }

    // Setup filters
    setupFilters() {
        const filterForm = document.getElementById('filter-form');
        const filterSelects = document.querySelectorAll('.filter-select');

        if (filterForm) {
            filterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.applyFilters();
            });
        }

        filterSelects.forEach(select => {
            select.addEventListener('change', () => {
                this.applyFilters();
            });
        });
    }

    // Apply filters
    async applyFilters() {
        const filterForm = document.getElementById('filter-form');
        if (!filterForm) return;

        const formData = new FormData(filterForm);
        this.filters = {};
        
        for (let [key, value] of formData.entries()) {
            if (value) {
                this.filters[key] = value;
            }
        }

        this.currentPage = 1;
        await this.loadInitialData();
        this.updateURL();
    }

    // Setup sorting
    setupSorting() {
        const sortableHeaders = document.querySelectorAll('.sortable');
        
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const field = header.dataset.field;
                this.handleSort(field);
            });
        });
    }

    // Handle sorting
    async handleSort(field) {
        if (this.sortField === field) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortField = field;
            this.sortDirection = 'asc';
        }

        this.updateSortIndicators();
        await this.loadInitialData();
        this.updateURL();
    }

    // Update sort indicators
    updateSortIndicators() {
        document.querySelectorAll('.sortable').forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
            const icon = header.querySelector('.sort-icon');
            if (icon) icon.textContent = '';
        });

        const currentHeader = document.querySelector(`[data-field="${this.sortField}"]`);
        if (currentHeader) {
            currentHeader.classList.add(`sort-${this.sortDirection}`);
            const icon = currentHeader.querySelector('.sort-icon');
            if (icon) {
                icon.textContent = this.sortDirection === 'asc' ? '↑' : '↓';
            }
        }
    }

    // Setup pagination
    setupPagination() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.pagination-btn')) {
                e.preventDefault();
                const page = parseInt(e.target.dataset.page);
                this.handlePageChange(page);
            }
        });
    }

    // Handle page change
    async handlePageChange(page) {
        this.currentPage = page;
        await this.loadInitialData();
        this.updateURL();
        this.scrollToTop();
    }

    // Setup bulk actions
    setupBulkActions() {
        const selectAllCheckbox = document.getElementById('select-all');
        const itemCheckboxes = document.querySelectorAll('.item-checkbox');
        const bulkActions = document.getElementById('bulk-actions');

        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => {
                itemCheckboxes.forEach(checkbox => {
                    checkbox.checked = e.target.checked;
                });
                this.updateBulkActionsVisibility();
            });
        }

        itemCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateBulkActionsVisibility();
                this.updateSelectAllCheckbox();
            });
        });

        // Bulk action buttons
        const bulkButtons = document.querySelectorAll('.bulk-action-btn');
        bulkButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = btn.dataset.action;
                this.handleBulkAction(action);
            });
        });
    }

    // Update bulk actions visibility
    updateBulkActionsVisibility() {
        const selectedCount = document.querySelectorAll('.item-checkbox:checked').length;
        const bulkActions = document.getElementById('bulk-actions');
        
        if (bulkActions) {
            bulkActions.style.display = selectedCount > 0 ? 'block' : 'none';
            
            const countSpan = bulkActions.querySelector('.selected-count');
            if (countSpan) {
                countSpan.textContent = selectedCount;
            }
        }
    }

    // Update select all checkbox
    updateSelectAllCheckbox() {
        const selectAllCheckbox = document.getElementById('select-all');
        const itemCheckboxes = document.querySelectorAll('.item-checkbox');
        const checkedCount = document.querySelectorAll('.item-checkbox:checked').length;
        
        if (selectAllCheckbox) {
            selectAllCheckbox.checked = checkedCount === itemCheckboxes.length;
            selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < itemCheckboxes.length;
        }
    }

    // Handle bulk action
    async handleBulkAction(action) {
        const selectedIds = Array.from(document.querySelectorAll('.item-checkbox:checked'))
            .map(checkbox => checkbox.value);

        if (selectedIds.length === 0) {
            window.crmUtils.showMessage('Please select items', 'error');
            return;
        }

        if (!confirm(`Are you sure you want to ${action} ${selectedIds.length} items?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/bulk-${action}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ ids: selectedIds })
            });

            if (response.ok) {
                window.crmUtils.showMessage(`${action} completed successfully`, 'success');
                await this.loadInitialData();
            } else {
                throw new Error('Action failed');
            }
        } catch (error) {
            window.crmUtils.showMessage(`Failed to ${action}`, 'error');
        }
    }

    // Get CSRF token
    getCSRFToken() {
        const cookie = document.cookie.match(/csrftoken=([^;]+)/);
        return cookie ? cookie[1] : '';
    }

    // Render list data
    renderList(data) {
        const tbody = document.querySelector('.list-table tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (data.items.length === 0) {
            this.renderEmptyState(tbody);
            return;
        }

        data.items.forEach(item => {
            const row = this.createRow(item);
            tbody.appendChild(row);
        });

        this.attachRowListeners();
    }

    // Render empty state
    renderEmptyState(container) {
        container.innerHTML = `
            <tr>
                <td colspan="100%" class="text-center py-8">
                    <div class="empty-state">
                        <div class="empty-icon">📭</div>
                        <h3>No items found</h3>
                        <p>Try adjusting your search or filters</p>
                        <button class="btn btn-primary" onclick="window.listOptimizer.clearFilters()">
                            Clear Filters
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }

    // Create table row
    createRow(item) {
        const row = document.createElement('tr');
        row.className = 'list-row';
        row.dataset.id = item.id;

        // Add checkbox column if bulk actions are enabled
        if (document.getElementById('bulk-actions')) {
            const checkboxCell = document.createElement('td');
            checkboxCell.innerHTML = `
                <input type="checkbox" class="item-checkbox" value="${item.id}">
            `;
            row.appendChild(checkboxCell);
        }

        // Add item-specific columns based on the current page
        this.populateRowColumns(row, item);

        // Add actions column
        const actionsCell = document.createElement('td');
        actionsCell.className = 'actions-cell';
        actionsCell.innerHTML = this.createActionButtons(item);
        row.appendChild(actionsCell);

        return row;
    }

    // Populate row columns (to be overridden by specific list types)
    populateRowColumns(row, item) {
        // Default implementation - should be overridden
        Object.entries(item).forEach(([key, value]) => {
            if (key !== 'id' && typeof value !== 'object') {
                const cell = document.createElement('td');
                cell.textContent = value;
                row.appendChild(cell);
            }
        });
    }

    // Create action buttons
    createActionButtons(item) {
        const baseUrl = window.location.pathname.replace('/list', '');
        return `
            <div class="action-buttons">
                <a href="${baseUrl}/${item.id}/" class="btn btn-sm btn-outline-primary" title="View">
                    👁️
                </a>
                <a href="${baseUrl}/${item.id}/edit/" class="btn btn-sm btn-outline-secondary" title="Edit">
                    ✏️
                </a>
                <button class="btn btn-sm btn-outline-danger" onclick="window.listOptimizer.deleteItem(${item.id})" title="Delete">
                    🗑️
                </button>
            </div>
        `;
    }

    // Delete item
    async deleteItem(id) {
        if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }

        try {
            const response = await fetch(`${window.location.pathname}${id}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                window.crmUtils.showMessage('Item deleted successfully', 'success');
                await this.loadInitialData();
            } else {
                throw new Error('Delete failed');
            }
        } catch (error) {
            window.crmUtils.showMessage('Failed to delete item', 'error');
        }
    }

    // Update pagination
    updatePagination(totalCount) {
        const pagination = document.querySelector('.pagination');
        if (!pagination) return;

        const totalPages = Math.ceil(totalCount / this.pageSize);
        let html = '';

        // Previous button
        html += `
            <button class="pagination-btn" data-page="${Math.max(1, this.currentPage - 1)}" 
                    ${this.currentPage === 1 ? 'disabled' : ''}>
                Previous
            </button>
        `;

        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);

        if (startPage > 1) {
            html += `<button class="pagination-btn" data-page="1">1</button>`;
            if (startPage > 2) {
                html += `<span class="pagination-ellipsis">...</span>`;
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            html += `
                <button class="pagination-btn ${i === this.currentPage ? 'active' : ''}" 
                        data-page="${i}">
                    ${i}
                </button>
            `;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                html += `<span class="pagination-ellipsis">...</span>`;
            }
            html += `<button class="pagination-btn" data-page="${totalPages}">${totalPages}</button>`;
        }

        // Next button
        html += `
            <button class="pagination-btn" data-page="${Math.min(totalPages, this.currentPage + 1)}"
                    ${this.currentPage === totalPages ? 'disabled' : ''}>
                Next
            </button>
        `;

        pagination.innerHTML = html;

        // Update info text
        const info = document.querySelector('.pagination-info');
        if (info) {
            const start = (this.currentPage - 1) * this.pageSize + 1;
            const end = Math.min(this.currentPage * this.pageSize, totalCount);
            info.textContent = `Showing ${start}-${end} of ${totalCount} items`;
        }
    }

    // Update URL without page reload
    updateURL() {
        const params = new URLSearchParams({
            page: this.currentPage > 1 ? this.currentPage : '',
            search: this.searchTerm,
            sort_field: this.sortField,
            sort_direction: this.sortDirection,
            ...this.filters
        });

        // Remove empty parameters
        for (let [key, value] of params.entries()) {
            if (!value) {
                params.delete(key);
            }
        }

        const newURL = `${window.location.pathname}${params.toString() ? '?' + params.toString() : ''}`;
        window.history.replaceState({}, '', newURL);
    }

    // Clear filters
    clearFilters() {
        this.filters = {};
        this.searchTerm = '';
        this.sortField = null;
        this.sortDirection = 'asc';
        this.currentPage = 1;

        // Reset form elements
        const filterForm = document.getElementById('filter-form');
        if (filterForm) {
            filterForm.reset();
        }

        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = '';
        }

        this.loadInitialData();
        this.updateURL();
    }

    // Scroll to top
    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Attach row listeners
    attachRowListeners() {
        // Row hover effects
        const rows = document.querySelectorAll('.list-row');
        rows.forEach(row => {
            row.addEventListener('mouseenter', () => {
                row.classList.add('row-hover');
            });
            
            row.addEventListener('mouseleave', () => {
                row.classList.remove('row-hover');
            });

            // Row click for navigation (if not clicking on buttons)
            row.addEventListener('click', (e) => {
                if (!e.target.matches('button, a, input')) {
                    const id = row.dataset.id;
                    const baseUrl = window.location.pathname.replace('/list', '');
                    window.location.href = `${baseUrl}/${id}/`;
                }
            });
        });
    }

    // Export data
    async exportData(format = 'csv') {
        try {
            const params = new URLSearchParams({
                export: format,
                ...this.filters,
                search: this.searchTerm
            });

            const response = await fetch(`${window.location.pathname}?${params.toString()}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `export_${new Date().toISOString().split('T')[0]}.${format}`;
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                throw new Error('Export failed');
            }
        } catch (error) {
            window.crmUtils.showMessage('Failed to export data', 'error');
        }
    }
}

// Initialize list optimizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for crmUtils to be available
    if (typeof window.crmUtils === 'undefined') {
        console.error('CRM Utils not loaded. List optimization disabled.');
        return;
    }
    
    if (document.querySelector('.list-table')) {
        window.listOptimizer = new ListOptimizer();
        window.listOptimizer.init();
    }
});
