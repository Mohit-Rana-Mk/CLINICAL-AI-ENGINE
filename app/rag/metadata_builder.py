from datetime import datetime
from typing import Any, Dict, Optional

def build_metadata(
    chunk: str,
    disease: Optional[str] = None,
    speciality: Optional[str] = None,
    language: Optional[str] = None,
    source: Optional[str] = None,
    organization: Optional[str] = None,
    publication: Optional[str] = None,
    page: Optional[int] = None,
    version: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Builds a metadata dictionary for a given text chunk.

    Args:
        chunk (str): The text chunk.
        disease (str, optional): The disease context.
        speciality (str, optional): The medical speciality.
        language (str, optional): The language of the text.
        source (str, optional): The source document or system.
        organization (str, optional): The organization associated with the text.
        publication (str, optional): The publication name.
        page (int, optional): The page number.
        version (str, optional): The version of the document.
        **kwargs: Any additional custom metadata fields.

    Returns:
        Dict[str, Any]: A dictionary containing the chunk's metadata.
    """
    metadata: Dict[str, Any] = {
        "disease": disease,
        "speciality": speciality,
        "language": language,
        "source": source,
        "organization": organization,
        "publication": publication,
        "page": page,
        "version": version,
    }

    # Automatically extract some basic properties
    word_count = len(chunk.split()) if chunk else 0
    
    # Add automated properties
    metadata["word_count"] = word_count
    metadata["generated_at"] = datetime.utcnow().isoformat() + "Z"

    # Add any extra custom fields passed via kwargs
    metadata.update(kwargs)

    # Filter out None values to keep the metadata clean
    clean_metadata = {k: v for k, v in metadata.items() if v is not None}

    return clean_metadata
