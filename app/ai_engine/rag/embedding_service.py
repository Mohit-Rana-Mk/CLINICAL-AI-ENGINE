import logging
from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Production Embedding Service.

    Responsibilities
    ----------------
    - Load embedding model only once
    - Generate embeddings
    - Normalize vectors
    - Cache query embeddings
    """

    MODEL_NAME = "BAAI/bge-base-en-v1.5"

    _model = None

    def __init__(self):

        if EmbeddingService._model is None:

            logger.info(
                "Loading embedding model: %s",
                self.MODEL_NAME,
            )

            EmbeddingService._model = SentenceTransformer(
                self.MODEL_NAME
            )

        self.model = EmbeddingService._model

    @lru_cache(maxsize=2048)
    def embed_query(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for user query.
        """

        return self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).tolist()

    def embed_document(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for a single document.
        """

        return self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).tolist()

    def embed_documents(
        self,
        documents: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        """

        if not documents:
            return []

        return self.model.encode(
            documents,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).tolist()

    @property
    def dimension(self) -> int:
        """
        Embedding dimension.
        """

        return self.model.get_sentence_embedding_dimension()