from typing import Any, Dict, List, Optional

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

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class SearchResult(BaseModel):
    """
    Result returned from semantic retrieval.
    """

    document: MedicalDocument

    similarity_score: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Cosine similarity score.",
    )

    rerank_score: Optional[float] = None


class Citation(BaseModel):

    id: int

    title: str

    category: str

    source: str

    similarity_score: float


class RAGMetadata(BaseModel):

    query: str

    documents_retrieved: int

    top_k: int

    execution_time_seconds: float


class RAGResponse(BaseModel):

    status: str

    documents: List[SearchResult] = Field(
        default_factory=list
    )

    citations: List[Citation] = Field(
        default_factory=list
    )

    prompt: str = ""

    metadata: Optional[RAGMetadata] = None