import os
import logging
from PIL import Image
from flask import current_app
import tempfile

# Try to import OCR dependencies, fall back to mock if not available
try:
    import pytesseract
    import pdf2image
    TESSERACT_AVAILABLE = True
    print("OCR dependencies imported successfully.")
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Warning: PyTesseract not available. Using mock OCR for demonstration.")

class OCRProcessor:
    """Handles OCR processing for various file types."""
    
    def __init__(self):
        """Initialize OCR processor with configuration."""
        self.logger = logging.getLogger(__name__)
        self.tesseract_available = None  # Will be determined on first use

    def _ensure_tesseract_configured(self):
        """Ensure Tesseract is configured and test availability."""
        if self.tesseract_available is not None:
            return self.tesseract_available

        # Configure Tesseract path
        try:
            if hasattr(current_app, 'config') and current_app.config.get('TESSERACT_CMD'):
                pytesseract.pytesseract.tesseract_cmd = current_app.config['TESSERACT_CMD']
                self.logger.info(f"Tesseract path configured: {current_app.config['TESSERACT_CMD']}")
        except Exception as e:
            self.logger.warning(f"Failed to configure Tesseract path: {e}")

        # Test Tesseract availability
        if not TESSERACT_AVAILABLE:
            self.tesseract_available = False
            return False

        try:
            version = pytesseract.get_tesseract_version()
            self.logger.info(f"Tesseract OCR available: {version}")
            self.tesseract_available = True
            return True
        except Exception as e:
            self.logger.warning(f"Tesseract not available: {e}")
            self.tesseract_available = False
            return False
        
    def process_file(self, file_path, language='eng'):
        """
        Process a file and extract text using OCR.
        
        Args:
            file_path (str): Path to the file to process
            language (str): Tesseract language code (default: 'eng')
            
        Returns:
            dict: Result containing success status, text, and any errors
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': 'File not found',
                    'text': ''
                }
            
            # Get file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Process based on file type
            if file_ext == '.pdf':
                return self._process_pdf(file_path, language)
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                return self._process_image(file_path, language)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {file_ext}',
                    'text': ''
                }
                
        except Exception as e:
            self.logger.error(f"OCR processing error: {str(e)}")
            return {
                'success': False,
                'error': f'OCR processing failed: {str(e)}',
                'text': ''
            }
    
    def _process_image(self, image_path, language):
        """Process a single image file."""
        try:
            # Open and validate image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                if self._ensure_tesseract_configured():
                    # Configure Tesseract
                    config = self._get_tesseract_config()

                    # Extract text
                    text = pytesseract.image_to_string(
                        img,
                        lang=language,
                        config=config
                    )
                else:
                    # Mock OCR for demonstration
                    text = self._mock_ocr_text(image_path)

                # Clean and validate text
                text = self._clean_text(text)

                return {
                    'success': True,
                    'text': text,
                    'error': None
                }

        except Exception as e:
            self.logger.error(f"Image processing error: {str(e)}")
            return {
                'success': False,
                'error': f'Image processing failed: {str(e)}',
                'text': ''
            }
    
    def _process_pdf(self, pdf_path, language):
        """Process a PDF file by converting to images first."""
        try:
            if self._ensure_tesseract_configured():
                # Check if Poppler is available
                try:
                    # Test Poppler availability
                    import pdf2image
                    # Get Poppler path from config
                    poppler_path = None
                    if hasattr(current_app, 'config') and current_app.config.get('POPPLER_PATH'):
                        poppler_path = current_app.config['POPPLER_PATH']
                    # Try to get PDF info to test Poppler
                    pdf2image.pdfinfo_from_path(pdf_path, poppler_path=poppler_path)

                    # Get Poppler path from config
                    poppler_path = None
                    if hasattr(current_app, 'config') and current_app.config.get('POPPLER_PATH'):
                        poppler_path = current_app.config['POPPLER_PATH']

                    # Convert PDF to images
                    images = pdf2image.convert_from_path(
                        pdf_path,
                        dpi=300,  # High DPI for better OCR accuracy
                        first_page=1,
                        last_page=10,  # Limit to first 10 pages for performance
                        poppler_path=poppler_path
                    )

                    all_text = []

                    # Process each page
                    for i, image in enumerate(images):
                        try:
                            # Configure Tesseract
                            config = self._get_tesseract_config()

                            # Extract text from page
                            page_text = pytesseract.image_to_string(
                                image,
                                lang=language,
                                config=config
                            )

                            if page_text.strip():
                                all_text.append(f"--- Page {i+1} ---\n{page_text}")

                        except Exception as e:
                            self.logger.warning(f"Error processing PDF page {i+1}: {str(e)}")
                            continue

                    # Combine all text
                    combined_text = '\n\n'.join(all_text)

                except pdf2image.exceptions.PDFInfoNotInstalledError:
                    self.logger.error("Poppler not installed - cannot process PDF")
                    return {
                        'success': False,
                        'error': 'PDF processing requires Poppler utilities to be installed. Please install Poppler and restart the application.',
                        'text': ''
                    }
                except pdf2image.exceptions.PDFPageCountError:
                    self.logger.error("Invalid PDF file")
                    return {
                        'success': False,
                        'error': 'Invalid or corrupted PDF file. Please try with a different PDF.',
                        'text': ''
                    }
                except Exception as pdf_error:
                    self.logger.error(f"PDF conversion error: {str(pdf_error)}")
                    # Check if it's a Poppler-related error
                    if 'poppler' in str(pdf_error).lower() or 'pdfinfo' in str(pdf_error).lower():
                        return {
                            'success': False,
                            'error': 'PDF processing requires Poppler utilities. Please install Poppler and restart the application.',
                            'text': ''
                        }
                    else:
                        return {
                            'success': False,
                            'error': f'PDF processing failed: {str(pdf_error)}',
                            'text': ''
                        }
            else:
                # Mock OCR for PDF when Tesseract is not available
                combined_text = self._mock_ocr_text(pdf_path, is_pdf=True)

            combined_text = self._clean_text(combined_text)

            return {
                'success': True,
                'text': combined_text,
                'error': None
            }

        except Exception as e:
            self.logger.error(f"PDF processing error: {str(e)}")
            # Provide specific error messages for common issues
            error_message = str(e)
            if 'poppler' in error_message.lower() or 'pdfinfo' in error_message.lower():
                error_message = 'PDF processing requires Poppler utilities to be installed. Please install Poppler and restart the application.'
            elif 'tesseract' in error_message.lower():
                error_message = 'OCR processing requires Tesseract to be installed and configured properly.'
            else:
                error_message = f'PDF processing failed: {error_message}'

            return {
                'success': False,
                'error': error_message,
                'text': ''
            }
    
    def _get_tesseract_config(self):
        """Get Tesseract configuration string."""
        # Basic configuration for better accuracy
        config = '--oem 3 --psm 6'  # OCR Engine Mode 3, Page Segmentation Mode 6
        
        # Add timeout if configured
        if hasattr(current_app.config, 'OCR_TIMEOUT'):
            timeout = current_app.config['OCR_TIMEOUT']
            config += f' -c tessedit_do_invert=0 -c timeout={timeout}'
        
        return config
    
    def _clean_text(self, text):
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        # Join with single newlines
        cleaned_text = '\n'.join(lines)
        
        # Remove null bytes and other problematic characters
        cleaned_text = cleaned_text.replace('\x00', '')
        
        return cleaned_text.strip()
    
    def get_available_languages(self):
        """Get list of available Tesseract languages."""
        try:
            if self._ensure_tesseract_configured():
                languages = pytesseract.get_languages()
                return languages
            else:
                # Return mock languages for demonstration
                return ['eng', 'spa', 'fra', 'deu']
        except Exception as e:
            self.logger.error(f"Error getting available languages: {str(e)}")
            return ['eng']  # Default fallback

    def _mock_ocr_text(self, file_path, is_pdf=False):
        """Generate mock OCR text for demonstration when Tesseract is not available."""
        filename = os.path.basename(file_path)

        if is_pdf:
            return f"""--- Page 1 ---
DEMONSTRATION MODE - TESSERACT NOT INSTALLED

This is a mock OCR result for the PDF file: {filename}

In a real deployment with Tesseract OCR installed, this would contain
the actual text extracted from your PDF document.

To enable real OCR functionality:
1. Install Tesseract OCR on your system
2. Restart the application

--- Page 2 ---
Additional pages would appear here with their extracted text content.

The OCR Web Application supports:
- Multiple image formats (JPEG, PNG)
- PDF documents (up to 10 pages)
- Multi-language text recognition
- High accuracy text extraction"""
        else:
            return f"""DEMONSTRATION MODE - TESSERACT NOT INSTALLED

This is a mock OCR result for the image file: {filename}

In a real deployment with Tesseract OCR installed, this would contain
the actual text extracted from your image.

To enable real OCR functionality:
1. Install Tesseract OCR on your system
2. Restart the application

The OCR Web Application supports:
- High-quality text extraction
- Multiple languages
- Image preprocessing for better accuracy
- Secure file handling"""
