import logging
from typing import List

from app.ai_engine.rag.schemas import SearchResult

logger = logging.getLogger(__name__)


class CitationEngine:
    """
    Production Citation Engine.

    Responsibilities
    ----------------
    - Convert retrieved documents into API citations
    - Remove duplicate citations
    - Preserve ranking order
    """

    def generate(
        self,
        documents: List[SearchResult],
    ) -> List[dict]:

        logger.info("Generating RAG citations")

        citations: List[dict] = []
        seen_titles: set[str] = set()

        for index, result in enumerate(documents, start=1):

            title = (result.document.title or "").strip()

            if not title:
                continue

            if title.lower() in seen_titles:
                continue

            seen_titles.add(title.lower())

            citations.append(
                {
                    "id": len(citations) + 1,
                    "title": title,
                    "category": result.document.category,
                    "source": result.document.source,
                    "similarity_score": round(
                        result.similarity_score,
                        3,
                    ),
                    "rank": index,
                }
            )

        logger.info(
            "Generated %d citations",
            len(citations),
        )

        return citations