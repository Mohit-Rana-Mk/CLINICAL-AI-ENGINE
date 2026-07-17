import os
import logging
import pymupdf4llm
import docx

logger = logging.getLogger(__name__)

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


def load_document(file_path: str) -> dict:
    """
    Loads a document and returns a metadata dict with keys:
      - "text":   extracted text content
      - "source": original file path
      - "type":   file extension without dot (pdf, docx, txt, md)

    Supports: .txt, .md, .pdf, .docx
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the file: {file_path}")
    if not os.path.isfile(file_path):
        raise IsADirectoryError(f"Expected a file path but got a directory: {file_path}")

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File too large: {file_size / 1e6:.1f} MB. "
            f"Maximum allowed is {MAX_FILE_SIZE_BYTES / 1e6:.0f} MB."
        )

    _, file_extension = os.path.splitext(file_path)
    file_type = file_extension.lower().lstrip(".")

    if file_type in ["txt", "md"]:
        text = _extract_from_text(file_path)
    elif file_type == "pdf":
        text = _extract_from_pdf(file_path)
    elif file_type == "docx":
        text = _extract_from_docx(file_path)
    else:
        raise ValueError(
            f"Unsupported file format: .{file_type}. "
            f"Only .txt, .md, .pdf, and .docx are supported."
        )

    logger.info(
        f"Loaded .{file_type} document: {len(text)} chars "
        f"from '{os.path.basename(file_path)}'"
    )
    return {"text": text, "source": file_path, "type": file_type}


def _extract_from_text(file_path: str) -> str:
    """Extracts text from raw text or markdown files with encoding fallback."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        logger.warning(f"UTF-8 decoding failed for '{file_path}', retrying with latin-1.")
        with open(file_path, "r", encoding="latin-1") as f:
            return f.read()


def _extract_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF using PyMuPDF4LLM.
    Returns highly structured Markdown, preserving tables and headers.
    """
    try:
        return pymupdf4llm.to_markdown(file_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to extract text from PDF '{os.path.basename(file_path)}': {e}"
        ) from e


def _extract_from_docx(file_path: str) -> str:
    """Extracts text paragraphs from a Word (.docx) document."""
    doc = docx.Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)