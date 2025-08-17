import os
import json
from flask import Blueprint, render_template, request, jsonify, send_file, current_app, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app.utils import allowed_file, validate_file_type, generate_unique_filename, cleanup_old_files, format_file_size, sanitize_text
from app.ocr_processor import OCRProcessor
import tempfile
import io

# Create blueprint
main = Blueprint('main', __name__)

# Initialize OCR processor
ocr_processor = OCRProcessor()

@main.route('/')
def index():
    """Main page with upload form."""
    cleanup_old_files()  # Clean up old files on each request
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and OCR processing."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Supported formats: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}'
            }), 400
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(file_path)
        
        # Validate file type using magic numbers
        if not validate_file_type(file_path):
            os.remove(file_path)  # Clean up invalid file
            return jsonify({
                'success': False,
                'error': 'Invalid file type detected'
            }), 400
        
        # Get file size for logging
        file_size = os.path.getsize(file_path)
        current_app.logger.info(f"Processing file: {filename} ({format_file_size(file_size)})")
        
        # Get language parameter (default to English)
        language = request.form.get('language', 'eng')
        
        # Process file with OCR
        result = ocr_processor.process_file(file_path, language)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except Exception as e:
            current_app.logger.warning(f"Failed to clean up file {filename}: {str(e)}")
        
        # Return result
        if result['success']:
            return jsonify({
                'success': True,
                'text': sanitize_text(result['text']),
                'filename': file.filename
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        current_app.logger.error(f"Upload processing error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred during processing'
        }), 500

@main.route('/download_text', methods=['POST'])
def download_text():
    """Download extracted text as a .txt file."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        filename = data.get('filename', 'extracted_text.txt')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text to download'
            }), 400
        
        # Create a text file in memory
        text_io = io.StringIO(text)
        text_bytes = io.BytesIO(text_io.getvalue().encode('utf-8'))
        
        # Generate download filename
        base_name = os.path.splitext(filename)[0] if filename else 'extracted_text'
        download_filename = f"{base_name}_extracted.txt"
        
        return send_file(
            text_bytes,
            as_attachment=True,
            download_name=download_filename,
            mimetype='text/plain'
        )
        
    except Exception as e:
        current_app.logger.error(f"Download error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate download'
        }), 500

@main.route('/languages')
def get_languages():
    """Get available OCR languages."""
    try:
        languages = ocr_processor.get_available_languages()
        return jsonify({
            'success': True,
            'languages': languages
        })
    except Exception as e:
        current_app.logger.error(f"Language retrieval error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve available languages'
        }), 500

@main.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'OCR Web Application'
    })

# Error handlers
@main.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    return jsonify({
        'success': False,
        'error': f'File too large. Maximum size allowed: {format_file_size(max_size)}'
    }), 413

@main.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    current_app.logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error occurred'
    }), 500
