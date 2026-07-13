import os
import pymupdf4llm
import docx

def load_document(file_path: str) -> str:
    """
    Takes a file path, detects the format, and extracts the text.
    Supports: .txt, .md, .pdf, .docx
    Returns the extracted text as a string (Markdown formatting if PDF).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the file: {file_path}")
    if not os.path.isfile(file_path):
         raise IsADirectoryError(f"Expected a file path but got a directory: {file_path}")

    # Get the file extension and convert to lowercase
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Route to the appropriate extractor based on extension
    if file_extension in ['.txt', '.md']:
        return _extract_from_text(file_path)
    elif file_extension == '.pdf':
        return _extract_from_pdf(file_path)
    elif file_extension == '.docx':
        return _extract_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Only .txt, .md, .pdf, and .docx are supported.")


def _extract_from_text(file_path: str) -> str:
    """Extracts text from raw text or markdown files."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def _extract_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDF4LLM.
    Returns highly structured Markdown, preserving tables and headers.
    """
    md_text = pymupdf4llm.to_markdown(file_path)
    return md_text


def _extract_from_docx(file_path: str) -> str:
    """Extracts text paragraphs from a Word (.docx) document."""
    doc = docx.Document(file_path)
    full_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            full_text.append(paragraph.text)
    
    return "\n".join(full_text)