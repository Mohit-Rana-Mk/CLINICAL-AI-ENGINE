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
    - Vector Database
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
        """

        if not text.strip():
            raise ValueError("Input text cannot be empty.")

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed(self, text: str) -> List[float]:
        """
        Alias for embed_text().

        Keeps compatibility with other modules that
        call embedding_engine.embed(...).
        """
        return self.embed_text(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
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
        Returns the currently loaded model.
        """

        return self.model_name