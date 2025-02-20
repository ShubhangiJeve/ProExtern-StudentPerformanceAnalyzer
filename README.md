# ProExtern-StudentPerformanceAnalyzer

This repository contains the complete implementation of the  Student Performance Analyzer &amp; Career Recommendation System. The system is designed to process various document formats (PDF, DOCX, images), extract text using advanced OCR techniques, and analyze the content to generate personalized career recommendations based on student performance.

## 🚀 Features & Functionalities

- **📁 Multi-Format File Upload**  
  - Supports JPEG, PNG, PDF, and DOCX file formats.  
  - Validates file type and size before processing.

- **🔍 Advanced Text Extraction & OCR**  
  - Utilizes Tesseract OCR for image and scanned document processing.  
  - Extracts text from digital PDFs using PyPDF2.

- **🧹 Preprocessing & Data Cleaning**  
  - Converts images to grayscale.  
  - Future enhancements include noise reduction and thresholding for improve

## 🛠️ Setup & Installation
- **1. Clone the Repository**
- Open your terminal and run:git clone https://github.com/yourusername/StudentPerformanceAnalyzer.git
cd StudentPerformanceAnalyzer

 - **2.Create a Virtual Environment**
 -It is recommended to use a virtual environment for dependency management.
python -m venv venv
-  Windows
venv\Scripts\activate
-  macOS/Linux
source venv/bin/activate

- **3. Install Dependencies**
Install the required libraries using:
pip install -r requirements.txt

__________________________________________________________________________________________________________________________________________________________________



