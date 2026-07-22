def chunk_text(text: str, chunk_size: int = 300, overlap_size: int = 50) -> list[str]:
    """
    Splits a long string of text into smaller chunks of words with overlapping boundaries.
    
    Args:
        text (str): The cleaned text to be chunked.
        chunk_size (int): The maximum number of words per chunk.
        overlap_size (int): The number of words to overlap between consecutive chunks.
        
    Returns:
        list[str]: A list of chunked text strings.
    """
    if not text or not text.strip():
        return []

    if chunk_size <= overlap_size:
        raise ValueError("chunk_size must be greater than overlap_size")

    words = text.split()
    
    if not words:
        return []

    chunks = []
    stride = chunk_size - overlap_size

    for i in range(0, len(words), stride):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        
        # If we have reached the end of the text, break to avoid redundant overlapping chunks at the end
        if i + chunk_size >= len(words):
            break

    return chunks
