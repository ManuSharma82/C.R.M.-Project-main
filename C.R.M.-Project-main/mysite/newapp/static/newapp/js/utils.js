/**
 * CRM JavaScript Utilities
 * Client-side caching, validation, and data processing utilities
 */

class CRMCache {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    set(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }

    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        if (Date.now() - item.timestamp > this.cacheTimeout) {
            this.cache.delete(key);
            return null;
        }
        
        return item.data;
    }

    clear() {
        this.cache.clear();
    }
}

class CRMUtils {
    constructor() {
        this.cache = new CRMCache();
        this.debounceTimers = {};
    }

    // Debounce function to reduce API calls
    debounce(func, delay = 300) {
        return (...args) => {
            clearTimeout(this.debounceTimers[func]);
            this.debounceTimers[func] = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Format currency
    formatCurrency(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    // Format number with decimal places
    formatNumber(number, decimals = 2) {
        return parseFloat(number).toFixed(decimals);
    }

    // Calculate line total
    calculateLineTotal(quantity, unitPrice, discountPercentage = 0, taxPercentage = 0) {
        const subtotal = quantity * unitPrice;
        const discountAmount = subtotal * (discountPercentage / 100);
        const afterDiscount = subtotal - discountAmount;
        const taxAmount = afterDiscount * (taxPercentage / 100);
        return afterDiscount + taxAmount;
    }

    // Calculate grand total with multiple items
    calculateGrandTotal(items) {
        return items.reduce((total, item) => {
            return total + this.calculateLineTotal(
                item.quantity || 0,
                item.unitPrice || 0,
                item.discountPercentage || 0,
                item.taxPercentage || 0
            );
        }, 0);
    }

    // Validate email format
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Validate phone number (basic validation)
    validatePhone(phone) {
        const re = /^[\d\s\-\+\(\)]+$/;
        return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
    }

    // Validate required fields
    validateRequired(form) {
        const errors = [];
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                errors.push(`${field.name || field.id} is required`);
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });
        
        return errors;
    }

    // Show message with auto-dismiss
    showMessage(message, type = 'info', duration = 5000) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type}`;
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            padding: 12px 20px;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideIn 0.3s ease-out;
        `;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => messageDiv.remove(), 300);
        }, duration);
    }

    // Cached API call with error handling
    async cachedFetch(url, cacheKey = null, options = {}) {
        if (cacheKey) {
            const cached = this.cache.get(cacheKey);
            if (cached) {
                return cached;
            }
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            if (cacheKey) {
                this.cache.set(cacheKey, data);
            }
            
            return data;
        } catch (error) {
            this.showMessage(`Network error: ${error.message}`, 'error');
            throw error;
        }
    }

    // Autocomplete with caching
    async setupAutocomplete(input, apiUrl, minChars = 2, delay = 300) {
        let currentRequest = null;
        
        const debouncedSearch = this.debounce(async (query) => {
            if (query.length < minChars) {
                this.hideAutocomplete(input);
                return;
            }

            // Cancel previous request
            if (currentRequest) {
                currentRequest.abort();
            }

            const cacheKey = `${apiUrl}:${query}`;
            
            try {
                currentRequest = new AbortController();
                const data = await this.cachedFetch(
                    `${apiUrl}?q=${encodeURIComponent(query)}`,
                    cacheKey,
                    { signal: currentRequest.signal }
                );
                
                this.showAutocomplete(input, data.items || data);
            } catch (error) {
                if (error.name !== 'AbortError') {
                    console.error('Autocomplete error:', error);
                }
            }
        }, delay);

        input.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });

        input.addEventListener('blur', () => {
            setTimeout(() => this.hideAutocomplete(input), 200);
        });
    }

    // Show autocomplete dropdown
    showAutocomplete(input, items) {
        this.hideAutocomplete(input);
        
        if (!items || items.length === 0) return;

        const dropdown = document.createElement('div');
        dropdown.className = 'autocomplete-dropdown';
        dropdown.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #ddd;
            border-top: none;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        `;

        items.forEach(item => {
            const option = document.createElement('div');
            option.className = 'autocomplete-option';
            option.style.cssText = `
                padding: 8px 12px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
            `;
            
            const displayText = item.name || item.description || item.item_code || JSON.stringify(item);
            option.textContent = displayText;
            
            option.addEventListener('click', () => {
                input.value = item.item_code || item.code || displayText;
                input.dispatchEvent(new Event('change', { bubbles: true }));
                this.hideAutocomplete(input);
            });
            
            option.addEventListener('mouseenter', () => {
                option.style.backgroundColor = '#f5f5f5';
            });
            
            option.addEventListener('mouseleave', () => {
                option.style.backgroundColor = '';
            });
            
            dropdown.appendChild(option);
        });

        // Position dropdown
        const rect = input.getBoundingClientRect();
        dropdown.style.position = 'fixed';
        dropdown.style.top = `${rect.bottom}px`;
        dropdown.style.left = `${rect.left}px`;
        dropdown.style.width = `${rect.width}px`;

        document.body.appendChild(dropdown);
        input._autocompleteDropdown = dropdown;
    }

    // Hide autocomplete dropdown
    hideAutocomplete(input) {
        if (input._autocompleteDropdown) {
            input._autocompleteDropdown.remove();
            input._autocompleteDropdown = null;
        }
    }

    // Export data to CSV
    exportToCSV(data, filename) {
        const headers = Object.keys(data[0] || {});
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    // Initialize form with real-time validation
    initFormValidation(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', () => {
                this.validateField(input);
            });

            // Clear error on input
            input.addEventListener('input', () => {
                input.classList.remove('error');
                const errorMsg = input.parentNode.querySelector('.error-message');
                if (errorMsg) errorMsg.remove();
            });
        });

        // Form submission validation
        form.addEventListener('submit', (e) => {
            const errors = this.validateRequired(form);
            if (errors.length > 0) {
                e.preventDefault();
                this.showMessage('Please correct the errors in the form', 'error');
            }
        });
    }

    // Validate individual field
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Remove existing error message
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) existingError.remove();

        // Email validation
        if (field.type === 'email' && value) {
            if (!this.validateEmail(value)) {
                isValid = false;
                message = 'Please enter a valid email address';
            }
        }

        // Phone validation
        if (field.name && field.name.toLowerCase().includes('phone') && value) {
            if (!this.validatePhone(value)) {
                isValid = false;
                message = 'Please enter a valid phone number';
            }
        }

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        }

        // Show error or clear
        if (!isValid) {
            field.classList.add('error');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            errorDiv.style.cssText = `
                color: #dc3545;
                font-size: 0.875em;
                margin-top: 4px;
            `;
            field.parentNode.appendChild(errorDiv);
        } else {
            field.classList.remove('error');
        }

        return isValid;
    }
}

// Global instance
try {
    window.crmUtils = new CRMUtils();
    console.log('CRM Utils loaded successfully:', window.crmUtils);
} catch (error) {
    console.error('Failed to initialize CRM Utils:', error);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .form-input.error {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 2px rgba(220, 53, 69, 0.2) !important;
    }
    
    .autocomplete-option:hover {
        background-color: #f5f5f5 !important;
    }
`;
document.head.appendChild(style);
