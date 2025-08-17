// OCR Web Application JavaScript

class OCRApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadLanguages();
    }

    initializeElements() {
        // Form elements
        this.uploadForm = document.getElementById('uploadForm');
        this.fileInput = document.getElementById('fileInput');
        this.languageSelect = document.getElementById('languageSelect');
        this.uploadBtn = document.getElementById('uploadBtn');

        // UI elements
        this.progressContainer = document.getElementById('progressContainer');
        this.resultsContainer = document.getElementById('resultsContainer');
        this.errorAlert = document.getElementById('errorAlert');
        this.errorMessage = document.getElementById('errorMessage');

        // Results elements
        this.extractedText = document.getElementById('extractedText');
        this.fileName = document.getElementById('fileName');
        this.copyBtn = document.getElementById('copyBtn');
        this.downloadBtn = document.getElementById('downloadBtn');

        // State
        this.currentFileName = '';
        this.currentText = '';
    }

    bindEvents() {
        // Form submission
        this.uploadForm.addEventListener('submit', (e) => this.handleUpload(e));

        // File input change
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Action buttons
        this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        this.downloadBtn.addEventListener('click', () => this.downloadText());

        // Drag and drop
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        const dropZone = document.getElementById('fileUploadZone');
        if (!dropZone) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => this.handleDrop(e), false);

        // Also handle click on the drop zone
        dropZone.addEventListener('click', (e) => {
            if (e.target === dropZone || e.target.closest('.file-upload-content')) {
                this.fileInput.click();
            }
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.fileInput.files = files;
            this.handleFileSelect({ target: { files: files } });
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            // Validate file size
            const maxSize = 10 * 1024 * 1024; // 10MB
            if (file.size > maxSize) {
                this.showError('File size exceeds 10MB limit');
                this.fileInput.value = '';
                this.updateUploadZoneText();
                return;
            }

            // Validate file type
            const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
            if (!allowedTypes.includes(file.type)) {
                this.showError('Invalid file type. Please select JPEG, PNG, or PDF files only.');
                this.fileInput.value = '';
                this.updateUploadZoneText();
                return;
            }

            this.hideError();
            this.updateUploadZoneText(file);
        }
    }

    updateUploadZoneText(file = null) {
        const uploadZone = document.getElementById('fileUploadZone');
        const titleElement = uploadZone.querySelector('.file-upload-title');
        const subtitleElement = uploadZone.querySelector('.file-upload-subtitle');
        const iconElement = uploadZone.querySelector('.file-upload-icon i');

        if (file) {
            titleElement.textContent = file.name;
            subtitleElement.textContent = `${this.formatFileSize(file.size)} • Ready to process`;
            iconElement.className = 'fas fa-file-check';
            uploadZone.style.borderColor = 'var(--success-500)';
        } else {
            titleElement.textContent = 'Drop your file here or click to browse';
            subtitleElement.textContent = 'Upload images or PDF files to extract text';
            iconElement.className = 'fas fa-cloud-upload-alt';
            uploadZone.style.borderColor = '';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async loadLanguages() {
        try {
            const response = await fetch('/languages');
            const data = await response.json();
            
            if (data.success && data.languages) {
                this.populateLanguageSelect(data.languages);
            }
        } catch (error) {
            console.warn('Failed to load languages:', error);
            // Keep default English option
        }
    }

    populateLanguageSelect(languages) {
        // Clear existing options except English
        this.languageSelect.innerHTML = '<option value="eng" selected>English</option>';

        // Add other languages
        const languageNames = {
            'spa': 'Spanish',
            'fra': 'French',
            'deu': 'German',
            'ita': 'Italian',
            'por': 'Portuguese',
            'rus': 'Russian',
            'chi_sim': 'Chinese (Simplified)',
            'jpn': 'Japanese',
            'kor': 'Korean',
            'ara': 'Arabic'
        };

        languages.forEach(lang => {
            if (lang !== 'eng' && languageNames[lang]) {
                const option = document.createElement('option');
                option.value = lang;
                option.textContent = languageNames[lang];
                this.languageSelect.appendChild(option);
            }
        });
    }

    async handleUpload(e) {
        e.preventDefault();

        const file = this.fileInput.files[0];
        if (!file) {
            this.showError('Please select a file');
            return;
        }

        this.showProgress();
        this.hideError();
        this.hideResults();

        const formData = new FormData();
        formData.append('file', file);
        formData.append('language', this.languageSelect.value);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.showResults(data.text, data.filename);
            } else {
                this.showError(data.error || 'OCR processing failed');
            }
        } catch (error) {
            this.showError('Network error occurred. Please try again.');
            console.error('Upload error:', error);
        } finally {
            this.hideProgress();
        }
    }

    showProgress() {
        this.progressContainer.style.display = 'block';
        this.uploadBtn.disabled = true;
        this.uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    }

    hideProgress() {
        this.progressContainer.style.display = 'none';
        this.uploadBtn.disabled = false;
        this.uploadBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Extract Text';
    }

    showResults(text, filename) {
        this.currentText = text;
        this.currentFileName = filename;
        
        this.extractedText.value = text;
        this.fileName.textContent = filename;
        this.resultsContainer.style.display = 'block';

        // Scroll to results
        this.resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    hideResults() {
        this.resultsContainer.style.display = 'none';
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorAlert.style.display = 'block';
        this.errorAlert.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => this.hideError(), 5000);
    }

    hideError() {
        this.errorAlert.style.display = 'none';
        this.errorAlert.classList.remove('show');
    }

    async copyToClipboard() {
        try {
            await navigator.clipboard.writeText(this.currentText);
            
            // Visual feedback
            const originalHTML = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            this.copyBtn.classList.add('btn-copy-success');
            
            setTimeout(() => {
                this.copyBtn.innerHTML = originalHTML;
                this.copyBtn.classList.remove('btn-copy-success');
            }, 2000);
            
        } catch (error) {
            this.showError('Failed to copy text to clipboard');
        }
    }

    async downloadText() {
        try {
            const response = await fetch('/download_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: this.currentText,
                    filename: this.currentFileName
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${this.currentFileName.split('.')[0]}_extracted.txt`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                this.showError('Failed to download text file');
            }
        } catch (error) {
            this.showError('Download failed');
            console.error('Download error:', error);
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new OCRApp();
});
