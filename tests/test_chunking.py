import pytest
from app.rag.chunking import chunk_text

def test_empty_string():
    assert chunk_text("") == []
    assert chunk_text("   ") == []

def test_short_string():
    text = "This is a short text."
    chunks = chunk_text(text, chunk_size=10, overlap_size=2)
    assert chunks == ["This is a short text."]

def test_exact_chunk_size():
    text = "word1 word2 word3 word4 word5"
    chunks = chunk_text(text, chunk_size=5, overlap_size=2)
    assert chunks == ["word1 word2 word3 word4 word5"]

def test_chunking_with_overlap():
    text = "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10"
    # chunk_size 5, overlap 2, stride 3
    # chunk 1: w1 w2 w3 w4 w5
    # chunk 2: w4 w5 w6 w7 w8
    # chunk 3: w7 w8 w9 w10
    chunks = chunk_text(text, chunk_size=5, overlap_size=2)
    
    assert len(chunks) == 3
    assert chunks[0] == "w1 w2 w3 w4 w5"
    assert chunks[1] == "w4 w5 w6 w7 w8"
    assert chunks[2] == "w7 w8 w9 w10"

def test_invalid_chunk_overlap():
    with pytest.raises(ValueError, match="chunk_size must be greater than overlap_size"):
        chunk_text("test", chunk_size=5, overlap_size=5)

    with pytest.raises(ValueError, match="chunk_size must be greater than overlap_size"):
        chunk_text("test", chunk_size=2, overlap_size=5)
