"""
OCR Web Application Configuration
Author: M Hamza Ummer
Version: 2.0.0
License: MIT
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # OCR settings
    TESSERACT_CMD = os.environ.get('TESSERACT_CMD') or r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    POPPLER_PATH = os.environ.get('POPPLER_PATH') or r'C:\poppler\poppler-24.08.0\Library\bin'
    OCR_LANGUAGES = ['eng']  # Default language
    
    # Security settings
    UPLOAD_RATE_LIMIT = "10 per minute"  # Rate limiting for uploads
    
    # File retention settings
    FILE_RETENTION_HOURS = 1  # Auto-delete uploaded files after 1 hour
    
    # Performance settings
    MAX_CONCURRENT_UPLOADS = 5
    OCR_TIMEOUT = 30  # seconds
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
