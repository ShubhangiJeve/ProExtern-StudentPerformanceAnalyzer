import io
import os
import re
import shutil
import subprocess
import time
import json
from datetime import datetime
from typing import Dict, List
import pytesseract
from docx import Document
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import PyPDF2
import fitz  # PyMuPDF

app = FastAPI(title="Smart Document Processor")

# Configure paths
pytesseract.pytesseract.tesseract_cmd = "" # Add Your Path 
# POPPLER_PATH = r"C:\poppler\bin"  "" # Add Your Path If required 

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="templates", html=True), name="static")

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = re.sub(r'[^\w\s.,!?\-():&\'"/#*|]', '', text)
    return text.strip()

def structure_to_json(text: str) -> Dict:
    """Convert processed text to structured JSON"""
    structured_data = {
        "metadata": {
            "processed_at": datetime.now().isoformat(),
            "version": "1.0"
        },
        "content": [],
        "raw_text": text
    }

    current_section = None
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect sections
        section_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if section_match:
            if current_section:
                structured_data["content"].append(current_section)
            current_section = {
                "section_id": int(section_match.group(1)),
                "title": section_match.group(2),
                "subsections": []
            }
            continue

        # Detect subsections
        subsection_match = re.match(r'^([A-Z][a-z]+:)\s*(.+)$', line)
        if subsection_match and current_section:
            current_section["subsections"].append({
                "type": "subsection",
                "label": subsection_match.group(1),
                "content": subsection_match.group(2)
            })
            continue

        # Detect lists
        list_match = re.match(r'^[\*\-•]\s+(.+)$', line)
        if list_match and current_section:
            if not current_section["subsections"] or current_section["subsections"][-1]["type"] != "list":
                current_section["subsections"].append({
                    "type": "list",
                    "items": []
                })
            current_section["subsections"][-1]["items"].append(list_match.group(1))
            continue

        # Regular paragraphs
        if current_section:
            current_section["subsections"].append({
                "type": "paragraph",
                "content": line
            })

    if current_section:
        structured_data["content"].append(current_section)

    return structured_data

# File processors
def process_image(file_path: str) -> Dict:
    try:
        with Image.open(file_path) as img:
            img = img.convert('L')
            text = pytesseract.image_to_string(img)
            return structure_to_json(clean_text(text))
    except Exception as e:
        raise HTTPException(500, f"Image processing failed: {str(e)}")

def process_digital_pdf(file_path: str) -> Dict:
    try:
        text = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(clean_text(page_text))
        return structure_to_json('\n\n'.join(text))
    except Exception as e:
        raise HTTPException(500, f"Digital PDF processing failed: {str(e)}")

def process_handwritten_pdf(file_path: str) -> Dict:
    try:
        text = []
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap()
            img_data = pix.tobytes()
            with Image.open(io.BytesIO(img_data)) as img:
                img = img.convert('L')
                page_text = pytesseract.image_to_string(img)
                text.append(clean_text(page_text))
        return structure_to_json('\n\n'.join(text))
    except Exception as e:
        raise HTTPException(500, f"Handwritten PDF processing failed: {str(e)}")

def process_doc(file_path: str) -> Dict:
    try:
        text = ""
        if file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            text = '\n'.join(p.text for p in doc.paragraphs)
        elif file_path.lower().endswith('.doc'):
            result = subprocess.run(
                ['antiword', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            text = result.stdout
        else:
            raise HTTPException(400, "Unsupported Word format")
        return structure_to_json(clean_text(text))
    except subprocess.CalledProcessError:
        raise HTTPException(500, "DOC processing requires antiword")
    except Exception as e:
        raise HTTPException(500, f"DOC processing failed: {str(e)}")

PROCESSORS = {
    'image': process_image,
    'digital_pdf': process_digital_pdf,
    'handwritten_pdf': process_handwritten_pdf,
    'doc': process_doc,
}

@app.get("/", response_class=FileResponse)
async def get_index():
    return FileResponse("templates/index.html")

@app.get("/result.html", response_class=FileResponse)
async def get_result():
    return FileResponse("templates/result.html")

@app.post('/api/process')
async def process_document(
    file: UploadFile = File(...),
    file_type: str = Form(...)
):
    try:
        if not file.filename:
            raise HTTPException(400, "Filename required")
            
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        timestamp = str(int(time.time()))
        file_path = os.path.join(temp_dir, f"{timestamp}_{file.filename}")
        
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        if os.path.getsize(file_path) == 0:
            raise HTTPException(400, "Empty file")

        processor = PROCESSORS.get(file_type)
        if not processor:
            raise HTTPException(400, "Invalid file type")

        processed_data = processor(file_path)
        os.remove(file_path)

        return JSONResponse(content=processed_data)

    except HTTPException as he:
        return JSONResponse(status_code=he.status_code, content={'detail': he.detail})
    finally:
        await file.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)