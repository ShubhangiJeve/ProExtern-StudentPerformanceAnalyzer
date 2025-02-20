# ProExtern-StudentPerformanceAnalyzer

This repository contains the complete implementation of the **Student Performance Analyzer & Career Recommendation System**. The system is designed to process various document formats (PDF, DOCX, images), extract text using advanced OCR techniques, and analyze the content to generate personalized career recommendations based on student performance.

## 🚀 Features & Functionalities

- **📁 Multi-Format File Upload**  
  - Supports JPEG, PNG, PDF, and DOCX file formats.  
  - Validates file type and size before processing.

- **🔍 Advanced Text Extraction & OCR**  
  - Utilizes Tesseract OCR for image and scanned document processing.  
  - Extracts text from digital PDFs using PyPDF2.

- **🧹 Preprocessing & Data Cleaning**  
  - Converts images to grayscale.  
  - Future enhancements include noise reduction and thresholding for improved OCR accuracy.

## 🛠️ Setup & Installation

### 1. Clone the Repository

Open your terminal and run:
```bash
git clone https://github.com/yourusername/StudentPerformanceAnalyzer.git
cd StudentPerformanceAnalyzer
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment for dependency management.

```bash
python -m venv venv
```

#### Windows:
```bash
venv\Scripts\activate
```

#### macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required libraries using:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Tesseract OCR Setup

Tesseract OCR is essential for extracting text from images and scanned documents.

### Download Tesseract

- **Windows:**  
  Download the installer from the [UB Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) page.

- **macOS:**  
  Install via Homebrew:
  ```bash
  brew install tesseract
  ```

- **Linux:**  
  Install via your package manager:
  ```bash
  sudo apt-get install tesseract-ocr
  ```

### Install Tesseract on Windows

- Run the downloaded installer and follow the prompts.
- The **default installation path** on Windows is typically:
  ```
  C:\Program Files\Tesseract-OCR\tesseract.exe
  ```

### Configure Tesseract in Your Project

In your Python code (e.g., in `src/config.py`), set the Tesseract command path as follows:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### 🔄 Note:
If Tesseract is installed elsewhere, or you're on macOS/Linux, adjust the path accordingly or ensure that **Tesseract is added to your system's PATH**.

---

## 📦 Dependencies

- **Python 3.8+**
- **FastAPI**: For building the RESTful API.
- **Uvicorn**: ASGI server for FastAPI.
- **pytesseract**: Python wrapper for Tesseract OCR.
- **Pillow (PIL)**: For image processing.
- **PyPDF2** & **PyMuPDF**: For handling PDF documents.
- **python-docx**: For processing DOCX files.
- **Tailwind CSS**: Used in the frontend for styling.

For a complete list of dependencies, please refer to the [requirements.txt](requirements.txt) file.

