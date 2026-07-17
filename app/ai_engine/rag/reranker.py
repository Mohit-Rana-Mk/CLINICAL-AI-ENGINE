import logging
from typing import List

from app.ai_engine.rag.schemas import SearchResult

logger = logging.getLogger(__name__)


class Reranker:
    """
    Production Clinical Evidence Reranker.

    Responsibilities
    ----------------
    - Remove duplicate evidence
    - Rank by semantic similarity
    - Keep highest-quality documents
    - Prepare context for downstream reasoning

    Future Upgrades
    ---------------
    - BAAI BGE Reranker
    - Cohere Rerank
    - Cross Encoder
    - LLM-based reranking
    """

    def rerank(
        self,
        results: List[SearchResult],
        query: str | None = None,
        top_k: int = 5,
    ) -> List[SearchResult]:

        logger.info("Reranking retrieved clinical evidence")

        if not results:
            logger.info("No documents available for reranking")
            return []

        unique_documents = {}
        ranked_results: List[SearchResult] = []

        # Keep highest-scoring duplicate
        for result in results:

            title = result.document.title.strip().lower()

            existing = unique_documents.get(title)

            if (
                existing is None
                or result.similarity_score > existing.similarity_score
            ):
                unique_documents[title] = result

        ranked_results = sorted(
            unique_documents.values(),
            key=lambda item: item.similarity_score,
            reverse=True,
        )

        ranked_results = ranked_results[:top_k]

        logger.info(
            "Reranking completed (%d documents)",
            len(ranked_results),
        )

        return ranked_results