from pydantic import BaseModel, Field


class MedicalDocument(BaseModel):
    """
    Represents one medical knowledge document.
    """

    id: str
    title: str
    content: str
    source: str
    category: str


class SearchResult(BaseModel):
    """
    Represents one retrieved document.
    """

    document: MedicalDocument
    similarity_score: float = Field(..., ge=0.0, le=1.0)