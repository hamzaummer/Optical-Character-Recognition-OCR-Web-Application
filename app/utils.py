import os
import magic
import hashlib
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def validate_file_type(file_path):
    """Validate file type using magic numbers (MIME type detection)."""
    try:
        mime = magic.Magic(mime=True)
        file_mime = mime.from_file(file_path)
        
        allowed_mimes = {
            'image/jpeg': ['jpg', 'jpeg'],
            'image/png': ['png'],
            'application/pdf': ['pdf']
        }
        
        return file_mime in allowed_mimes
    except Exception as e:
        current_app.logger.error(f"File type validation error: {str(e)}")
        return False

def generate_unique_filename(filename):
    """Generate a unique filename to prevent conflicts."""
    # Get file extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    # Create hash based on filename and timestamp
    timestamp = datetime.now().isoformat()
    hash_input = f"{filename}{timestamp}".encode('utf-8')
    file_hash = hashlib.md5(hash_input).hexdigest()[:8]
    
    # Secure the original filename
    base_name = secure_filename(filename.rsplit('.', 1)[0] if '.' in filename else filename)
    
    return f"{base_name}_{file_hash}.{ext}" if ext else f"{base_name}_{file_hash}"

def cleanup_old_files():
    """Remove old uploaded files based on retention policy."""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        retention_hours = current_app.config['FILE_RETENTION_HOURS']
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)
        
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_time < cutoff_time:
                    os.remove(file_path)
                    current_app.logger.info(f"Cleaned up old file: {filename}")
                    
    except Exception as e:
        current_app.logger.error(f"File cleanup error: {str(e)}")

def format_file_size(size_bytes):
    """Convert bytes to human readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def sanitize_text(text):
    """Basic text sanitization for display."""
    if not text:
        return ""
    
    # Remove null bytes and other problematic characters
    text = text.replace('\x00', '')
    
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    return text.strip()
