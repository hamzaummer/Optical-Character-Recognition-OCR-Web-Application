# Tesseract OCR Installation Guide

This guide provides detailed instructions for installing Tesseract OCR on different operating systems to enable full OCR functionality in the web application.

## Windows Installation

### Method 1: Using Pre-compiled Binaries (Recommended)

1. **Download Tesseract**:
   - Visit: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-v5.3.3.20231005.exe`)

2. **Install Tesseract**:
   - Run the installer as Administrator
   - Choose installation directory (default: `C:\Program Files\Tesseract-OCR`)
   - Make sure to select additional language packs if needed

3. **Add to PATH**:
   - Open System Properties → Advanced → Environment Variables
   - Add `C:\Program Files\Tesseract-OCR` to your PATH
   - Or set environment variable: `TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe`

4. **Install Poppler (for PDF support)**:
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract to a folder (e.g., `C:\poppler`)
   - Add `C:\poppler\Library\bin` to your PATH

### Method 2: Using Chocolatey

```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Tesseract
choco install tesseract

# Install Poppler
choco install poppler
```

## macOS Installation

### Method 1: Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tesseract
brew install tesseract

# Install additional languages (optional)
brew install tesseract-lang

# Install Poppler for PDF support
brew install poppler
```

### Method 2: Using MacPorts

```bash
# Install Tesseract
sudo port install tesseract

# Install Poppler
sudo port install poppler
```

## Linux Installation

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Tesseract
sudo apt install tesseract-ocr

# Install additional languages (optional)
sudo apt install tesseract-ocr-spa tesseract-ocr-fra tesseract-ocr-deu

# Install Poppler for PDF support
sudo apt install poppler-utils

# Install development headers (if needed)
sudo apt install libtesseract-dev
```

### CentOS/RHEL/Fedora

```bash
# For CentOS/RHEL (enable EPEL repository first)
sudo yum install epel-release
sudo yum install tesseract tesseract-langpack-spa tesseract-langpack-fra

# For Fedora
sudo dnf install tesseract tesseract-langpack-spa tesseract-langpack-fra

# Install Poppler
sudo yum install poppler-utils  # CentOS/RHEL
sudo dnf install poppler-utils  # Fedora
```

### Arch Linux

```bash
# Install Tesseract
sudo pacman -S tesseract tesseract-data-eng tesseract-data-spa

# Install Poppler
sudo pacman -S poppler
```

## Verification

After installation, verify that Tesseract is working:

```bash
# Check Tesseract version
tesseract --version

# List available languages
tesseract --list-langs

# Test OCR on an image (if you have one)
tesseract test_image.png output.txt
```

## Language Packs

### Available Languages

Common language codes:
- `eng` - English
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `chi_sim` - Chinese (Simplified)
- `chi_tra` - Chinese (Traditional)
- `jpn` - Japanese
- `kor` - Korean
- `ara` - Arabic

### Installing Additional Languages

**Windows**: Select during installation or download from the GitHub releases page

**macOS**: 
```bash
brew install tesseract-lang
```

**Ubuntu/Debian**:
```bash
sudo apt install tesseract-ocr-[lang_code]
# Example: sudo apt install tesseract-ocr-spa
```

## Configuration

### Environment Variables

Set these environment variables if Tesseract is not in your PATH:

**Windows**:
```cmd
set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**macOS/Linux**:
```bash
export TESSERACT_CMD=/usr/local/bin/tesseract
```

### Application Configuration

In the OCR web application, you can also set the Tesseract path in `config.py`:

```python
class Config:
    TESSERACT_CMD = '/path/to/tesseract'  # Set your path here
```

## Troubleshooting

### Common Issues

1. **"tesseract is not installed or it's not in your PATH"**
   - Ensure Tesseract is installed and added to PATH
   - Set the TESSERACT_CMD environment variable

2. **"No such file or directory: 'tesseract'"**
   - Tesseract executable not found
   - Check installation and PATH configuration

3. **PDF processing fails**
   - Install Poppler utilities
   - Ensure poppler is in PATH

4. **Poor OCR accuracy**
   - Use high-resolution images (300+ DPI)
   - Ensure good contrast and lighting
   - Try image preprocessing options

5. **Language not found**
   - Install the required language pack
   - Check available languages with `tesseract --list-langs`

### Testing Installation

Use the provided test image in the application:

1. Start the OCR web application
2. Upload the `test_ocr_image.png` file
3. Verify that text is extracted correctly

## Performance Tips

1. **Image Quality**: Use images with at least 300 DPI for best results
2. **Preprocessing**: The application includes automatic image preprocessing
3. **File Size**: Keep images under 10MB for optimal performance
4. **Language Selection**: Choose the correct language for better accuracy

## Support

If you encounter issues:

1. Check the application logs in `logs/ocr_app.log`
2. Verify Tesseract installation with `tesseract --version`
3. Test with the provided sample image
4. Check the GitHub issues page for common problems

For more information, visit:
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- PyTesseract: https://github.com/madmaze/pytesseract
