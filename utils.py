import fitz  # PyMuPDF
from PIL import Image
import pytesseract

def is_pdf_scanned(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            if text.strip():
                return False
    return True

def extract_text_with_ocr(pdf_path):
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img).strip()

                # Output the cleaned text to a file
                with open("extracted_text.txt", "w") as text_file:
                    text_file.write(text)

                print(f"Extracted text from page {page_num + 1}:")
                print(text)

    except Exception as e:
        print(f"Error during OCR extraction: {e}")