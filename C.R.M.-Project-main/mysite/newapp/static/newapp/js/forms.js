/**
 * Form Optimization - Client-side validation, calculations, and caching
 * Reduces API calls for form operations and improves responsiveness
 */

class FormOptimizer {
    constructor() {
        this.cache = new Map();
        this.debounceTimers = {};
        this.validators = {};
    }

    // Initialize form optimization
    init() {
        this.setupItemAutocomplete();
        this.setupProspectAutocomplete();
        this.setupRealTimeCalculations();
        this.setupFormValidation();
        this.setupAutoSave();
    }

    // Setup item autocomplete with caching
    setupItemAutocomplete() {
        const itemInputs = document.querySelectorAll('input[name*="item_code"]');
        
        itemInputs.forEach(input => {
            window.crmUtils.setupAutocomplete(
                input,
                '/api/search-items/',
                2,
                300
            );

            // Auto-fill item details on selection/change
            input.addEventListener('change', (e) => {
                this.handleItemCodeChange(e.target);
            });
        });
    }

    // Handle item code change with cached lookup
    async handleItemCodeChange(input) {
        const itemCode = input.value.trim();
        if (!itemCode) return;

        const cacheKey = `item:${itemCode}`;
        const row = input.closest('tr') || input.closest('.form-row');

        try {
            // Try cache first
            let itemData = window.crmUtils.cache.get(cacheKey);
            
            if (!itemData) {
                // Fetch from API with cache
                itemData = await window.crmUtils.cachedFetch(
                    `/api/get-item/?item_code=${encodeURIComponent(itemCode)}`,
                    cacheKey
                );
            }

            if (itemData && itemData.success) {
                this.populateItemFields(row, itemData.item);
                this.recalculateRowTotal(row);
                this.recalculateGrandTotal();
            }
        } catch (error) {
            console.log('Item lookup failed:', error.message);
        }
    }

    // Populate item fields from cached data
    populateItemFields(row, item) {
        const fields = {
            description: row.querySelector('[name*="-description"]'),
            uom: row.querySelector('[name*="-uom"]'),
            unitPrice: row.querySelector('[name*="-unit_price"]'),
            taxPercentage: row.querySelector('[name*="-tax_percentage"]')
        };

        if (fields.description && !fields.description.value) {
            fields.description.value = item.description || '';
        }
        if (fields.uom && !fields.uom.value) {
            fields.uom.value = item.unit_of_measurement || '';
        }
        if (fields.unitPrice && !fields.unitPrice.value) {
            fields.unitPrice.value = item.standard_price || 0;
        }
        if (fields.taxPercentage && !fields.taxPercentage.value) {
            fields.taxPercentage.value = item.default_tax_percentage || 0;
        }

        // Highlight the row
        row.style.backgroundColor = '#e8f5e9';
        setTimeout(() => {
            row.style.backgroundColor = '';
        }, 2000);
    }

    // Setup prospect autocomplete
    setupProspectAutocomplete() {
        const prospectInputs = document.querySelectorAll('input[name*="prospect"], input[name*="customer"]');
        
        prospectInputs.forEach(input => {
            window.crmUtils.setupAutocomplete(
                input,
                '/api/search-prospects/',
                2,
                300
            );

            input.addEventListener('change', (e) => {
                this.handleProspectChange(e.target);
            });
        });
    }

    // Handle prospect change
    async handleProspectChange(input) {
        const prospectName = input.value.trim();
        if (!prospectName) return;

        const cacheKey = `prospect:${prospectName}`;
        const form = input.closest('form');

        try {
            let prospectData = window.crmUtils.cache.get(cacheKey);
            
            if (!prospectData) {
                prospectData = await window.crmUtils.cachedFetch(
                    `/api/get-prospect/?name=${encodeURIComponent(prospectName)}`,
                    cacheKey
                );
            }

            if (prospectData && prospectData.success) {
                this.populateProspectFields(form, prospectData.prospect);
            }
        } catch (error) {
            console.log('Prospect lookup failed:', error.message);
        }
    }

    // Populate prospect fields
    populateProspectFields(form, prospect) {
        const fields = {
            contactPerson: form.querySelector('[name*="contact_person"]'),
            contactEmail: form.querySelector('[name*="contact_email"]'),
            contactPhone: form.querySelector('[name*="contact_phone"]'),
            billingAddress: form.querySelector('[name*="billing_address"]')
        };

        if (fields.contactPerson && !fields.contactPerson.value) {
            fields.contactPerson.value = prospect.contact_person || '';
        }
        if (fields.contactEmail && !fields.contactEmail.value) {
            fields.contactEmail.value = prospect.email || '';
        }
        if (fields.contactPhone && !fields.contactPhone.value) {
            fields.contactPhone.value = prospect.phone || '';
        }
        if (fields.billingAddress && !fields.billingAddress.value) {
            fields.billingAddress.value = prospect.address || '';
        }
    }

    // Setup real-time calculations
    setupRealTimeCalculations() {
        // Quantity, price, discount, tax changes
        const calculationFields = document.querySelectorAll(
            'input[name*="quantity"], input[name*="unit_price"], ' +
            'input[name*="discount"], input[name*="tax"]'
        );

        calculationFields.forEach(field => {
            field.addEventListener('input', window.crmUtils.debounce(() => {
                const row = field.closest('tr') || field.closest('.form-row');
                this.recalculateRowTotal(row);
                this.recalculateGrandTotal();
            }, 300));
        });

        // Exchange rate changes
        const exchangeRateInputs = document.querySelectorAll('input[name*="exchange_rate"]');
        exchangeRateInputs.forEach(input => {
            input.addEventListener('input', window.crmUtils.debounce(() => {
                this.recalculateGrandTotal();
            }, 300));
        });
    }

    // Recalculate row total
    recalculateRowTotal(row) {
        const quantity = parseFloat(row.querySelector('[name*="quantity"]')?.value) || 0;
        const unitPrice = parseFloat(row.querySelector('[name*="unit_price"]')?.value) || 0;
        const discountPercentage = parseFloat(row.querySelector('[name*="discount"]')?.value) || 0;
        const taxPercentage = parseFloat(row.querySelector('[name*="tax"]')?.value) || 0;

        const total = window.crmUtils.calculateLineTotal(
            quantity, unitPrice, discountPercentage, taxPercentage
        );

        const totalCell = row.querySelector('.calculated-total, .line-total');
        if (totalCell) {
            totalCell.textContent = window.crmUtils.formatNumber(total);
        }

        return total;
    }

    // Recalculate grand total
    recalculateGrandTotal() {
        const rows = document.querySelectorAll('.item-row, .form-row');
        let grandTotal = 0;

        rows.forEach(row => {
            const rowTotal = this.recalculateRowTotal(row);
            grandTotal += rowTotal;
        });

        // Update grand total displays
        const grandTotalElements = document.querySelectorAll('.grand-total, .total-amount');
        grandTotalElements.forEach(element => {
            element.textContent = window.crmUtils.formatCurrency(grandTotal);
        });

        // Update hidden fields
        const hiddenTotal = document.querySelector('input[name="total_amount"]');
        if (hiddenTotal) {
            hiddenTotal.value = grandTotal.toFixed(2);
        }
    }

    // Setup form validation
    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            window.crmUtils.initFormValidation(form);

            // Custom validation for specific forms
            if (form.id === 'quotation-form' || form.id === 'salesorder-form') {
                this.setupLineItemValidation(form);
            }
        });
    }

    // Setup line item validation
    setupLineItemValidation(form) {
        form.addEventListener('submit', (e) => {
            const rows = form.querySelectorAll('.item-row');
            let hasValidItems = false;

            rows.forEach(row => {
                const itemCode = row.querySelector('[name*="item_code"]')?.value;
                const quantity = row.querySelector('[name*="quantity"]')?.value;
                const unitPrice = row.querySelector('[name*="unit_price"]')?.value;

                if (itemCode && quantity && unitPrice) {
                    hasValidItems = true;
                }
            });

            if (!hasValidItems) {
                e.preventDefault();
                window.crmUtils.showMessage('Please add at least one valid item', 'error');
                return false;
            }
        });
    }

    // Setup auto-save functionality
    setupAutoSave() {
        const forms = document.querySelectorAll('form[data-auto-save]');
        
        forms.forEach(form => {
            let saveTimeout;
            
            const autoSave = window.crmUtils.debounce(() => {
                this.saveFormData(form);
            }, 2000);

            form.addEventListener('input', autoSave);
            form.addEventListener('change', autoSave);
        });
    }

    // Save form data to localStorage
    saveFormData(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }

        const formKey = `form_${form.id}_${window.location.pathname}`;
        localStorage.setItem(formKey, JSON.stringify({
            data: data,
            timestamp: Date.now()
        }));

        // Show subtle save indicator
        this.showSaveIndicator('saved');
    }

    // Load saved form data
    loadFormData(form) {
        const formKey = `form_${form.id}_${window.location.pathname}`;
        const saved = localStorage.getItem(formKey);
        
        if (!saved) return;

        try {
            const parsed = JSON.parse(saved);
            
            // Only load if saved within last hour
            if (Date.now() - parsed.timestamp < 60 * 60 * 1000) {
                this.populateForm(form, parsed.data);
                this.showSaveIndicator('restored');
            }
        } catch (error) {
            console.error('Failed to load saved form data:', error);
        }
    }

    // Populate form with saved data
    populateForm(form, data) {
        Object.entries(data).forEach(([key, value]) => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = value;
                field.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    }

    // Show save indicator
    showSaveIndicator(status) {
        const indicator = document.getElementById('save-indicator') || this.createSaveIndicator();
        
        const messages = {
            saved: 'Draft saved',
            restoring: 'Restoring draft...',
            restored: 'Draft restored'
        };

        indicator.textContent = messages[status] || '';
        indicator.style.display = 'block';

        if (status === 'saved') {
            setTimeout(() => {
                indicator.style.display = 'none';
            }, 2000);
        }
    }

    // Create save indicator
    createSaveIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'save-indicator';
        indicator.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 0.875em;
            z-index: 9999;
            display: none;
        `;
        document.body.appendChild(indicator);
        return indicator;
    }

    // Setup quotation lookup optimization
    setupQuotationLookup() {
        const lookupBtn = document.getElementById('quotation-lookup-btn');
        const quoteInput = document.getElementById('quote_number');

        if (lookupBtn && quoteInput) {
            lookupBtn.addEventListener('click', () => {
                this.lookupQuotation(quoteInput.value);
            });

            quoteInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.lookupQuotation(quoteInput.value);
                }
            });
        }
    }

    // Optimized quotation lookup with caching
    async lookupQuotation(quoteNumber) {
        if (!quoteNumber) return;

        const cacheKey = `quotation:${quoteNumber}`;
        const btn = document.getElementById('quotation-lookup-btn');

        try {
            btn.disabled = true;
            btn.innerHTML = '⏳ Loading...';

            let quotationData = window.crmUtils.cache.get(cacheKey);
            
            if (!quotationData) {
                quotationData = await window.crmUtils.cachedFetch(
                    `/api/get-quotation/?quote_number=${encodeURIComponent(quoteNumber)}`,
                    cacheKey
                );
            }

            if (quotationData && quotationData.success) {
                this.populateQuotationForm(quotationData);
                window.crmUtils.showMessage(`✅ Loaded quotation ${quoteNumber}!`, 'success');
            } else {
                window.crmUtils.showMessage('Quotation not found', 'error');
            }
        } catch (error) {
            window.crmUtils.showMessage('Failed to load quotation', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🔍 Load';
        }
    }

    // Populate form with quotation data
    populateQuotationForm(data) {
        const form = document.getElementById('quotation-form') || document.getElementById('salesorder-form');
        if (!form) return;

        // Populate header fields
        this.populateQuotationHeader(form, data.quotation);
        
        // Populate line items
        this.populateQuotationItems(data.items);
        
        // Recalculate totals
        this.recalculateGrandTotal();
    }

    // Populate quotation header
    populateQuotationHeader(form, quotation) {
        const fields = {
            prospect: form.querySelector('[name*="prospect"]'),
            contactPerson: form.querySelector('[name*="contact_person"]'),
            contactEmail: form.querySelector('[name*="contact_email"]'),
            contactPhone: form.querySelector('[name*="contact_phone"]')
        };

        Object.entries(fields).forEach(([key, field]) => {
            if (field && quotation[key]) {
                field.value = quotation[key];
            }
        });
    }

    // Populate quotation items
    populateQuotationItems(items) {
        const tbody = document.getElementById('items-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';
        
        items.forEach((item, index) => {
            const row = this.createItemRow(item, index);
            tbody.appendChild(row);
        });

        // Update form management
        const totalForms = document.querySelector('#id_items-TOTAL_FORMS');
        if (totalForms) {
            totalForms.value = items.length;
        }
    }

    // Create item row for quotation
    createItemRow(item, index) {
        const row = document.createElement('tr');
        row.className = 'item-row';
        row.innerHTML = `
            <td class="line-number">${item.line_number || index + 1}</td>
            <td>
                <input type="hidden" name="items-${index}-id" value="${item.id || ''}">
                <input type="text" name="items-${index}-item_code" class="form-input" 
                       value="${item.item_code}" readonly>
            </td>
            <td>
                <textarea name="items-${index}-description" class="form-input" rows="2" readonly>${item.description}</textarea>
            </td>
            <td>
                <input type="number" name="items-${index}-quantity" class="form-input" 
                       value="${item.quantity}" step="0.01" required>
            </td>
            <td>
                <input type="text" name="items-${index}-uom" class="form-input" 
                       value="${item.uom}" readonly>
            </td>
            <td>
                <input type="number" name="items-${index}-unit_price" class="form-input" 
                       value="${item.unit_price}" step="0.01" required>
            </td>
            <td>
                <input type="number" name="items-${index}-discount_percentage" class="form-input" 
                       value="${item.discount_percentage}" step="0.01">
            </td>
            <td>
                <input type="number" name="items-${index}-tax_percentage" class="form-input" 
                       value="${item.tax_percentage}" step="0.01">
            </td>
            <td class="calculated-total">${window.crmUtils.formatNumber(item.line_total)}</td>
            <td>
                <input type="checkbox" name="items-${index}-DELETE">
            </td>
        `;
        return row;
    }
}

// Initialize form optimizer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Wait for crmUtils to be available
    if (typeof window.crmUtils === 'undefined') {
        console.error('CRM Utils not loaded. Forms optimization disabled.');
        return;
    }
    
    window.formOptimizer = new FormOptimizer();
    window.formOptimizer.init();
});
