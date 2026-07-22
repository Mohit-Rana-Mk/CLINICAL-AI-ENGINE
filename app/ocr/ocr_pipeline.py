import os
import fitz  # PyMuPDF
from paddleocr import PaddleOCR
from loguru import logger
import cv2
import numpy as np

# Initialize PaddleOCR with lightweight models
# Use English language models by default. can be extended.
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

def convert_pdf_to_images(pdf_path: str):
    """
    Converts a PDF file to a list of OpenCV images using PyMuPDF.
    """
    images = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300) # High DPI for better OCR
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            
            # Convert RGB (PyMuPDF default) to BGR (OpenCV default) if it's 3 channels
            if pix.n == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
            images.append(img)
        doc.close()
    except Exception as e:
        logger.error(f"Error converting PDF {pdf_path} to images: {e}")
    return images

def process_document(file_path: str):
    """
    Main entry point for OCR.
    Handles both PDFs and standard image formats.
    Returns the combined PaddleOCR result (text and bounding boxes).
    """
    logger.info(f"Processing document for OCR: {file_path}")
    
    # Check if the file is a PDF
    if file_path.lower().endswith('.pdf'):
        images = convert_pdf_to_images(file_path)
    else:
        # Load single image
        img = cv2.imread(file_path)
        if img is None:
            logger.error(f"Failed to load image: {file_path}")
            return []
        images = [img]

    all_results = []
    
    # Process each image/page
    for page_idx, img in enumerate(images):
        logger.debug(f"Running OCR on page {page_idx + 1}")
        # PaddleOCR expects a path, ndarray, or bytes. We can pass the ndarray directly.
        result = ocr.ocr(img, cls=True)
        if result and result[0]:
            all_results.extend(result[0])
            
    return all_results

def get_text_from_ocr_result(ocr_result):
    """
    Extracts purely text from the PaddleOCR result.
    """
    text_lines = []
    for line in ocr_result:
        # line is [ [[box coords]], (text, confidence) ]
        if len(line) == 2 and isinstance(line[1], tuple):
            text_lines.append(line[1][0])
    return "\n".join(text_lines)
