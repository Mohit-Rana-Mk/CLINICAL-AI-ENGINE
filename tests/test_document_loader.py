import os
import pytest
from unittest.mock import patch, MagicMock

from app.rag.document_loader import load_document

def test_load_document_not_found():
    with pytest.raises(FileNotFoundError, match="Could not find the file"):
        load_document("nonexistent_file.txt")

def test_load_document_is_directory(tmp_path):
    dir_path = tmp_path / "somedir.txt"
    dir_path.mkdir()
    with pytest.raises(IsADirectoryError, match="Expected a file path but got a directory"):
        load_document(str(dir_path))

def test_load_document_unsupported_extension(tmp_path):
    file_path = tmp_path / "image.jpg"
    file_path.write_text("fake image data")
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_document(str(file_path))

def test_load_document_txt(tmp_path):
    file_path = tmp_path / "test.txt"
    expected_text = "This is a text file.\nWith multiple lines."
    file_path.write_text(expected_text, encoding="utf-8")
    
    result = load_document(str(file_path))
    assert result == expected_text

def test_load_document_md(tmp_path):
    file_path = tmp_path / "test.md"
    expected_text = "# Markdown\n\nSome text."
    file_path.write_text(expected_text, encoding="utf-8")
    
    result = load_document(str(file_path))
    assert result == expected_text

@patch("app.rag.document_loader.pymupdf4llm.to_markdown")
def test_load_document_pdf(mock_to_markdown, tmp_path):
    file_path = tmp_path / "test.pdf"
    file_path.write_text("fake pdf content")
    expected_text = "# PDF Content\n\nMocked."
    mock_to_markdown.return_value = expected_text
    
    result = load_document(str(file_path))
    
    mock_to_markdown.assert_called_once_with(str(file_path))
    assert result == expected_text

@patch("app.rag.document_loader.docx.Document")
def test_load_document_docx(mock_document, tmp_path):
    file_path = tmp_path / "test.docx"
    file_path.write_text("fake docx content")
    
    mock_doc_instance = MagicMock()
    
    # Create mock paragraphs
    mock_para1 = MagicMock()
    mock_para1.text = "Paragraph 1"
    
    mock_para2 = MagicMock()
    mock_para2.text = "   " # Empty/whitespace paragraph, should be ignored
    
    mock_para3 = MagicMock()
    mock_para3.text = "Paragraph 3"
    
    mock_doc_instance.paragraphs = [mock_para1, mock_para2, mock_para3]
    mock_document.return_value = mock_doc_instance
    
    result = load_document(str(file_path))
    
    mock_document.assert_called_once_with(str(file_path))
    assert result == "Paragraph 1\nParagraph 3"
