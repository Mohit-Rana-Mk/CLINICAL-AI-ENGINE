import logging
from typing import List

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingEngine:
    """
    Embedding Engine

    Responsible for converting medical text into dense vector embeddings
    for semantic search and Retrieval-Augmented Generation (RAG).

    This module is intentionally independent of:
    - FastAPI
    - Clinical Pipeline
    - Qdrant
    - LLMs

    Responsibility:
        Text -> Embedding Vector
    """

    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or self.DEFAULT_MODEL

        logger.info(f"Loading embedding model: {self.model_name}")

        self.model = SentenceTransformer(self.model_name)

        logger.info("Embedding model loaded successfully.")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            List[float]
        """

        if not text.strip():
            raise ValueError("Input text cannot be empty.")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of text strings

        Returns:
            List[List[float]]
        """

        if not texts:
            raise ValueError("Text list cannot be empty.")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def get_dimension(self) -> int:
        """
        Returns embedding dimension.
        """

        return self.model.get_embedding_dimension()

    def get_model_name(self) -> str:
        """
        Returns currently loaded model.
        """

        return self.model_name