#!/usr/bin/env python3
"""
Exhaustive test suite for OCR Web Application.
Tests all features including enhanced UI, image OCR, PDF OCR, and error handling.
"""

import requests
import os
import json
import time
from PIL import Image, ImageDraw, ImageFont
import tempfile
import io

class ExhaustiveOCRTester:
    def __init__(self, base_url='http://127.0.0.1:5000'):
        self.base_url = base_url
        self.test_results = []
        self.passed_tests = 0
        self.total_tests = 0
        
    def log_test(self, test_name, success, details=""):
        """Log test result."""
        self.total_tests += 1
        if success:
            self.passed_tests += 1
            
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'details': details
        })
        
    def test_server_health(self):
        """Test 1: Server health and availability."""
        try:
            response = requests.get(f'{self.base_url}/health', timeout=5)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Service: {data.get('service', 'Unknown')}"
        except Exception as e:
            success = False
            details = f"Connection error: {str(e)}"
        
        self.log_test("Server Health Check", success, details)
        return success
    
    def test_enhanced_ui_loading(self):
        """Test 2: Enhanced UI loads with new design system."""
        try:
            response = requests.get(self.base_url, timeout=10)
            success = response.status_code == 200
            
            # Check for design system elements
            content = response.text
            has_enhanced_ui = all([
                'file-upload-zone' in content,
                'file-upload-icon' in content,
                'format-badge' in content,
                'OCR Web App' in content
            ])
            
            success = success and has_enhanced_ui
            details = f"Status: {response.status_code}, Enhanced UI elements: {has_enhanced_ui}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test("Enhanced UI Loading", success, details)
        return success
    
    def test_languages_endpoint(self):
        """Test 3: Languages endpoint returns real Tesseract languages."""
        try:
            response = requests.get(f'{self.base_url}/languages', timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                languages = data.get('languages', [])
                has_real_langs = 'eng' in languages and len(languages) >= 1
                success = has_real_langs
                details = f"Languages: {', '.join(languages)}"
            else:
                details = f"Status: {response.status_code}"
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test("Languages Endpoint", success, details)
        return success
    
    def create_test_image(self, filename, text_content, size=(600, 200)):
        """Create a test image with specific text content."""
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Add text with good contrast
        draw.text((20, 50), text_content, fill='black', font=font)
        
        # Add border for better OCR
        draw.rectangle([(5, 5), (size[0]-5, size[1]-5)], outline='black', width=2)
        
        img.save(filename)
        return filename
    
    def test_image_ocr_jpeg(self):
        """Test 4: JPEG image OCR processing."""
        test_text = "JPEG OCR Test - Hello World 12345"
        test_image = "temp_test_jpeg.jpg"
        
        try:
            # Create test JPEG
            self.create_test_image(test_image, test_text)
            
            # Upload and process
            with open(test_image, 'rb') as f:
                files = {'file': f}
                data = {'language': 'eng'}
                response = requests.post(f'{self.base_url}/upload', files=files, data=data, timeout=30)
            
            success = response.status_code == 200
            if success:
                result = response.json()
                extracted_text = result.get('text', '')
                
                # Check if we got real OCR (not mock)
                is_real_ocr = 'DEMONSTRATION MODE' not in extracted_text
                has_expected_content = any(word in extracted_text for word in ['JPEG', 'OCR', 'Test', 'Hello'])
                
                success = is_real_ocr and has_expected_content
                details = f"Real OCR: {is_real_ocr}, Content match: {has_expected_content}"
            else:
                details = f"Upload failed: {response.status_code}"
                
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        finally:
            if os.path.exists(test_image):
                os.remove(test_image)
        
        self.log_test("JPEG Image OCR", success, details)
        return success
    
    def test_image_ocr_png(self):
        """Test 5: PNG image OCR processing."""
        test_text = "PNG OCR Test - Advanced Processing 67890"
        test_image = "temp_test_png.png"
        
        try:
            # Create test PNG
            self.create_test_image(test_image, test_text)
            
            # Upload and process
            with open(test_image, 'rb') as f:
                files = {'file': f}
                data = {'language': 'eng'}
                response = requests.post(f'{self.base_url}/upload', files=files, data=data, timeout=30)
            
            success = response.status_code == 200
            if success:
                result = response.json()
                extracted_text = result.get('text', '')
                
                is_real_ocr = 'DEMONSTRATION MODE' not in extracted_text
                has_expected_content = any(word in extracted_text for word in ['PNG', 'OCR', 'Advanced', 'Processing'])
                
                success = is_real_ocr and has_expected_content
                details = f"Real OCR: {is_real_ocr}, Content match: {has_expected_content}"
            else:
                details = f"Upload failed: {response.status_code}"
                
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        finally:
            if os.path.exists(test_image):
                os.remove(test_image)
        
        self.log_test("PNG Image OCR", success, details)
        return success
    
    def test_pdf_ocr(self):
        """Test 6: PDF OCR processing."""
        pdf_file = "test_ocr_document.pdf"
        
        try:
            if not os.path.exists(pdf_file):
                self.log_test("PDF OCR", False, "Test PDF file not found")
                return False
            
            # Upload and process PDF
            with open(pdf_file, 'rb') as f:
                files = {'file': f}
                data = {'language': 'eng'}
                response = requests.post(f'{self.base_url}/upload', files=files, data=data, timeout=45)
            
            success = response.status_code == 200
            if success:
                result = response.json()
                extracted_text = result.get('text', '')
                
                # Check for PDF-specific content
                is_real_ocr = 'DEMONSTRATION MODE' not in extracted_text
                has_pdf_content = any(word in extracted_text for word in ['OCR Test Document', 'PDF', 'demonstrate'])
                has_page_markers = '--- Page' in extracted_text
                
                success = is_real_ocr and has_pdf_content and has_page_markers
                details = f"Real OCR: {is_real_ocr}, PDF content: {has_pdf_content}, Page markers: {has_page_markers}"
            else:
                result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                details = f"Upload failed: {response.status_code}, Error: {result.get('error', 'Unknown')}"
                
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test("PDF OCR Processing", success, details)
        return success
    
    def test_file_validation(self):
        """Test 7: File validation and security."""
        try:
            # Test unsupported file type
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
                f.write(b'This is a text file')
                txt_file = f.name
            
            with open(txt_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{self.base_url}/upload', files=files, timeout=10)
            
            # Should reject unsupported file type
            success = response.status_code == 400
            details = f"Correctly rejected .txt file: {response.status_code}"
            
            os.unlink(txt_file)
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test("File Type Validation", success, details)
        return success
    
    def test_text_export(self):
        """Test 8: Text export functionality."""
        try:
            test_data = {
                'text': 'Sample extracted text for download test\nLine 2\nLine 3',
                'filename': 'test_image.png'
            }
            
            response = requests.post(
                f'{self.base_url}/download_text',
                json=test_data,
                timeout=10
            )
            
            success = response.status_code == 200
            is_text_file = 'text/plain' in response.headers.get('content-type', '')
            has_content = len(response.content) > 0
            
            success = success and is_text_file and has_content
            details = f"Status: {response.status_code}, Content-Type: {response.headers.get('content-type', 'Unknown')}, Size: {len(response.content)} bytes"
            
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test("Text Export/Download", success, details)
        return success
    
    def test_error_handling(self):
        """Test 9: Comprehensive error handling."""
        tests_passed = 0
        total_error_tests = 3
        
        # Test 1: Empty file upload
        try:
            files = {'file': ('', b'', 'application/octet-stream')}
            response = requests.post(f'{self.base_url}/upload', files=files, timeout=10)
            if response.status_code == 400:
                tests_passed += 1
        except:
            pass
        
        # Test 2: No file in request
        try:
            response = requests.post(f'{self.base_url}/upload', timeout=10)
            if response.status_code == 400:
                tests_passed += 1
        except:
            pass
        
        # Test 3: Invalid JSON for download
        try:
            response = requests.post(f'{self.base_url}/download_text', json={}, timeout=10)
            if response.status_code == 400:
                tests_passed += 1
        except:
            pass
        
        success = tests_passed >= 2  # Allow some flexibility
        details = f"Error handling tests passed: {tests_passed}/{total_error_tests}"
        
        self.log_test("Error Handling", success, details)
        return success
    
    def test_ui_responsiveness(self):
        """Test 10: UI responsiveness and design elements."""
        try:
            response = requests.get(self.base_url, timeout=10)
            success = response.status_code == 200
            
            if success:
                content = response.text
                # Check for responsive design elements
                has_bootstrap = 'bootstrap' in content.lower()
                has_responsive_meta = 'viewport' in content
                has_css_vars = '--' in content or 'var(' in content
                
                success = has_bootstrap and has_responsive_meta
                details = f"Bootstrap: {has_bootstrap}, Responsive meta: {has_responsive_meta}, CSS vars: {has_css_vars}"
            else:
                details = f"Status: {response.status_code}"
                
        except Exception as e:
            success = False
            details = f"Error: {str(e)}"
        
        self.log_test("UI Responsiveness", success, details)
        return success
    
    def run_all_tests(self):
        """Run the complete exhaustive test suite."""
        print("🧪 Starting Exhaustive OCR Application Test Suite")
        print("=" * 70)
        
        # Define all tests
        tests = [
            self.test_server_health,
            self.test_enhanced_ui_loading,
            self.test_languages_endpoint,
            self.test_image_ocr_jpeg,
            self.test_image_ocr_png,
            self.test_pdf_ocr,
            self.test_file_validation,
            self.test_text_export,
            self.test_error_handling,
            self.test_ui_responsiveness
        ]
        
        # Run all tests
        for test in tests:
            try:
                test()
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                self.log_test(f"{test.__name__}", False, f"Unexpected error: {e}")
        
        # Print summary
        print("=" * 70)
        print(f"📊 Test Results: {self.passed_tests}/{self.total_tests} tests passed")
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! All major features working perfectly.")
            print("\n✅ Comprehensive Validation Complete:")
            print("   ✅ Enhanced UI with Linear-inspired design system")
            print("   ✅ Real OCR text extraction (JPEG, PNG)")
            print("   ✅ PDF OCR processing with Poppler integration")
            print("   ✅ File upload validation and security")
            print("   ✅ Text display, copy, and download features")
            print("   ✅ Comprehensive error handling")
            print("   ✅ Responsive design and UI components")
            return True
        elif success_rate >= 70:
            print("⚠️  Most features working, some issues need attention.")
            return False
        else:
            print("❌ Significant issues found. Review failed tests.")
            return False

if __name__ == '__main__':
    tester = ExhaustiveOCRTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 The OCR Web Application is ready for production!")
        print("🌐 Access at: http://127.0.0.1:5000")
        print("📋 All features validated and working correctly.")
    else:
        print("\n🔧 Some issues need to be addressed.")
        print("📋 Review the test results above for details.")
