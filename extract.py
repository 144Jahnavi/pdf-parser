import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re

# Set Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

HEALTH_METRICS = {
    "Hemoglobin": (12, 16, "g/dL"), "WBC": (4000, 11000, "cells/uL"),
    "RBC": (4.7, 6.1, "million/uL"), "Platelet": (150000, 450000, "cells/uL"),
    "Glucose": (70, 140, "mg/dL"), "Cholesterol": (125, 200, "mg/dL"),
    "Triglycerides": (0, 150, "mg/dL"), "Blood Pressure": (90, 120, "mmHg"),
    "Heart Rate": (60, 100, "bpm"), "BMI": (18.5, 24.9, ""),
    "Creatinine": (0.6, 1.2, "mg/dL"), "Urea": (7, 20, "mg/dL"),
    "ALT": (0, 40, "U/L"), "AST": (0, 40, "U/L"), "Bilirubin": (0.1, 1.2, "mg/dL")
}

def extract_health_data(text):
    abnormal_data = []
    normal_data = []
    normal = True

    for metric, (low, high, unit) in HEALTH_METRICS.items():
        pattern = rf"{metric}.*?(\d+\.?\d*)"
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            value = float(match.group(1))
            if value < low:
                abnormal_data.append(f"{metric}: {value} {unit} (Low)")
                normal = False
            elif value > high:
                abnormal_data.append(f"{metric}: {value} {unit} (High)")
                normal = False
            else:
                normal_data.append(f"{metric}: {value} {unit} (Normal)")

    summary_text = "Report Status: Normal" if normal else "Report Status: Abnormal"
    return '\n'.join(abnormal_data + normal_data) + "\n\n" + summary_text

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text("text")

    if not text.strip():
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(img)

    return extract_health_data(text)

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return extract_health_data(text)
