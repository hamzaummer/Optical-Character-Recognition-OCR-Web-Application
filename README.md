# OCR Web Application

A modern, comprehensive web application for Optical Character Recognition (OCR) using Tesseract OCR. Upload images or PDF files and extract text with high accuracy using an elegant, dark theme interface.

**Author**: M Hamza Ummer
<br>
**Version**: 1.0.0
<br>
**License**: MIT

## ✨ Features

### 🎨 **Enhanced User Interface**
- **Linear-Inspired Design**: Modern dark theme with professional aesthetics
- **Enhanced File Upload**: Drag-and-drop interface with visual feedback
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Real-time Feedback**: Live progress indicators and status updates

### 🔍 **Advanced OCR Capabilities**
- **Multi-format Support**: JPEG, PNG, and PDF files
- **High Accuracy**: Powered by Tesseract OCR engine v5.5.0
- **PDF Processing**: Full PDF OCR with Poppler integration
- **Multi-language Support**: Extract text in 100+ languages
- **Batch Processing**: Handle multiple pages in PDF documents

### 🛡️ **Security & Performance**
- **Secure Processing**: Files automatically deleted after processing
- **File Validation**: Magic number validation and size limits
- **Error Handling**: Comprehensive error management
- **Performance Optimized**: Concurrent request handling

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Tesseract OCR v5.0+** installed:
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **CentOS/RHEL**: `sudo yum install tesseract`

3. **Poppler** (for PDF processing):
   - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)
   - **macOS**: `brew install poppler`
   - **Ubuntu/Debian**: `sudo apt-get install poppler-utils`

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ocr-web-app
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Tesseract path** (if needed):
   ```bash
   # Windows example
   set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   
   # macOS/Linux (usually auto-detected)
   export TESSERACT_CMD=/usr/local/bin/tesseract
   ```

5. **Run the application**:
   ```bash
   python run.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## Configuration

### Environment Variables

- `FLASK_CONFIG`: Set to `development`, `production`, or `testing`
- `SECRET_KEY`: Set a secure secret key for production
- `TESSERACT_CMD`: Path to Tesseract executable (if not in PATH)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 5000)
- `FLASK_DEBUG`: Enable debug mode (default: True)

### Application Settings

Edit `config.py` to customize:

- `MAX_CONTENT_LENGTH`: Maximum file size (default: 10MB)
- `ALLOWED_EXTENSIONS`: Supported file types
- `OCR_LANGUAGES`: Available OCR languages
- `FILE_RETENTION_HOURS`: Auto-delete uploaded files after X hours
- `OCR_TIMEOUT`: OCR processing timeout in seconds

## Usage

1. **Upload File**: Select or drag-and-drop an image or PDF file
2. **Choose Language**: Select the primary language of the text
3. **Extract Text**: Click "Extract Text" to process the file
4. **View Results**: Extracted text appears in the results area
5. **Export Text**: Copy to clipboard or download as .txt file

### Supported File Types

- **Images**: JPEG, PNG (up to 10MB)
- **Documents**: PDF (up to 10MB, first 10 pages)

### Supported Languages

- English (default)
- Spanish, French, German, Italian
- Portuguese, Russian
- Chinese (Simplified), Japanese, Korean
- Arabic

*Note: Additional languages require corresponding Tesseract language packs*

## API Endpoints

### POST /upload
Upload and process a file for OCR.

**Request**: Multipart form data
- `file`: Image or PDF file
- `language`: OCR language code (optional, default: 'eng')

**Response**: JSON
```json
{
  "success": true,
  "text": "Extracted text content",
  "filename": "original_filename.jpg"
}
```

### POST /download_text
Download extracted text as a .txt file.

**Request**: JSON
```json
{
  "text": "Text to download",
  "filename": "original_filename.jpg"
}
```

**Response**: Text file download

### GET /languages
Get available OCR languages.

**Response**: JSON
```json
{
  "success": true,
  "languages": ["eng", "spa", "fra", ...]
}
```

### GET /health
Health check endpoint.

**Response**: JSON
```json
{
  "status": "healthy",
  "service": "OCR Web Application"
}
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Deployment

### Development
```bash
python run.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Docker Deployment
```bash
# Build image
docker build -t ocr-web-app .

# Run container
docker run -p 5000:5000 ocr-web-app
```

## Troubleshooting

### Common Issues

1. **Tesseract not found**:
   - Ensure Tesseract is installed and in PATH
   - Set `TESSERACT_CMD` environment variable

2. **PDF processing fails**:
   - Install Poppler utilities
   - Check PDF file is not corrupted

3. **Poor OCR accuracy**:
   - Ensure image has good contrast and resolution
   - Try different OCR language settings
   - Use images with at least 300 DPI

4. **File upload fails**:
   - Check file size (max 10MB)
   - Verify file format is supported
   - Ensure sufficient disk space

### Logs

Application logs are stored in:
- Development: Console output
- Production: `logs/ocr_app.log`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**M Hamza Ummer**
- GitHub: [@hamzaummer](https://github.com/hamzaummer)
- Email: [mohammedhamza7428@gmail.com](mailto:mohammedhamza7428@gmail.com)

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Poppler](https://poppler.freedesktop.org/) - PDF processing utilities

## ⭐ Support

If you find this project helpful, please consider giving it a star on GitHub!

---

**Built with ❤️ by M Hamza Ummer**
