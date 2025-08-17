#!/usr/bin/env python3
"""
OCR Web Application
Main entry point for the Flask application.

Author: M Hamza Ummer
Version: 2.0.0
License: MIT
"""

import os
from app import create_app

# Create Flask application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # Development server settings
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting OCR Web Application on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True  # Enable threading for concurrent requests
    )
