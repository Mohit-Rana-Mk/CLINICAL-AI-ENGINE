import logging
from typing import List

from app.ai_engine.rag.rag_pipeline import RAGPipeline
from app.ai_engine.rag.schemas import SearchResult

logger = logging.getLogger(__name__)


class Retriever:
    """
    Production Clinical Retriever.

    Responsibilities
    ----------------
    - Semantic retrieval
    - Similarity filtering
    - Optional category filtering
    - Return highest quality evidence
    """

    DEFAULT_TOP_K = 5
    DEFAULT_THRESHOLD = 0.55

    _pipeline = None

    def __init__(self):

        if Retriever._pipeline is None:
            Retriever._pipeline = RAGPipeline()

        self.rag_pipeline = Retriever._pipeline

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        category: str | None = None,
    ) -> List[SearchResult]:

        logger.info("Retrieving clinical evidence")

        if not query.strip():
            logger.warning("Empty retrieval query received")
            return []

        results = self.rag_pipeline.retrieve(
            query=query,
            top_k=top_k,
        )

        filtered_results: List[SearchResult] = []

        for result in results:

            if result.similarity_score < self.DEFAULT_THRESHOLD:
                continue

            if (
                category
                and result.document.category != category
            ):
                continue

            filtered_results.append(result)

        filtered_results.sort(
            key=lambda item: item.similarity_score,
            reverse=True,
        )

        logger.info(
            "Retrieved %d high-quality clinical documents",
            len(filtered_results),
        )

        return filtered_results