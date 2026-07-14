from abc import ABC, abstractmethod
from typing import List

import numpy as np

from app.ai_engine.rag.embedding_engine import EmbeddingEngine
from app.ai_engine.rag.schemas import (
    MedicalDocument,
    SearchResult,
)


class BaseVectorStore(ABC):
    """
    Abstract interface for every vector database.
    """

    @abstractmethod
    def add_document(self, document: MedicalDocument):
        pass

    @abstractmethod
    def add_documents(self, documents: List[MedicalDocument]):
        pass

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[SearchResult]:
        pass


class InMemoryVectorStore(BaseVectorStore):
    """
    In-memory vector store.

    Used during development.
    Can later be replaced with Qdrant, Pinecone,
    ChromaDB, Weaviate, etc. without changing the pipeline.
    """

    def __init__(self):

        self.embedding_engine = EmbeddingEngine()

        self.documents: List[MedicalDocument] = []

        self.embeddings: List[np.ndarray] = []

    def add_document(
        self,
        document: MedicalDocument,
    ):

        embedding = self.embedding_engine.embed(
            document.content
        )

        embedding = np.array(embedding)

        self.documents.append(document)

        self.embeddings.append(embedding)

    def add_documents(
        self,
        documents: List[MedicalDocument],
    ):

        for document in documents:
            self.add_document(document)

    def cosine_similarity(
        self,
        vector1: np.ndarray,
        vector2: np.ndarray,
    ) -> float:
        """
        Compute cosine similarity between two embedding vectors.
        """

        denominator = (
            np.linalg.norm(vector1)
            * np.linalg.norm(vector2)
        )

        if denominator == 0:
            return 0.0

        similarity = np.dot(vector1, vector2) / denominator

        return float(similarity)

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[SearchResult]:
        """
        Perform semantic similarity search.
        """

        query_embedding = np.array(
            self.embedding_engine.embed(query)
        )

        scores: List[SearchResult] = []

        for document, embedding in zip(
            self.documents,
            self.embeddings,
        ):

            similarity = self.cosine_similarity(
                query_embedding,
                embedding,
            )

            scores.append(
                SearchResult(
                    document=document,
                    similarity_score=similarity,
                )
            )

        scores.sort(
            key=lambda result: result.similarity_score,
            reverse=True,
        )

        return scores[:top_k]

    @property
    def total_documents(self) -> int:

        return len(self.documents)