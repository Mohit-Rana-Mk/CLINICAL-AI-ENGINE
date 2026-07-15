import logging
import time

from app.ai_engine.rag.citation_engine import CitationEngine
from app.ai_engine.rag.prompt_builder import PromptBuilder
from app.ai_engine.rag.reranker import Reranker
from app.ai_engine.rag.retriever import Retriever

logger = logging.getLogger(__name__)


class RAGService:
    """
    Production RAG orchestration layer.

    User Query
        ↓
    Retriever
        ↓
    Reranker
        ↓
    Citation Engine
        ↓
    Prompt Builder
        ↓
    Final Prompt
    """

    def __init__(self):

        logger.info("Initializing RAG Service")

        self.retriever = Retriever()
        self.reranker = Reranker()
        self.citation_engine = CitationEngine()
        self.prompt_builder = PromptBuilder()

    def process(
        self,
        query: str,
        patient_context=None,
        emergency_status=None,
        risk_assessment=None,
        top_k: int = 5,
    ):

        start_time = time.time()

        try:

            logger.info("RAG pipeline started")

            if not query.strip():
                raise ValueError("Query cannot be empty")

            top_k = max(1, min(top_k, 20))

            # ---------------------------------
            # Retrieve
            # ---------------------------------

            documents = self.retriever.retrieve(
                query=query,
                top_k=top_k,
            )

            # ---------------------------------
            # Rerank
            # ---------------------------------

            documents = self.reranker.rerank(
                results=documents,
                query=query,
            )

            # ---------------------------------
            # Citations
            # ---------------------------------

            citations = self.citation_engine.generate(
                documents
            )

            # ---------------------------------
            # Convert Pydantic -> dict
            # ---------------------------------

            if hasattr(patient_context, "model_dump"):
                patient_context = patient_context.model_dump()

            if hasattr(emergency_status, "model_dump"):
                emergency_status = emergency_status.model_dump()

            if hasattr(risk_assessment, "model_dump"):
                risk_assessment = risk_assessment.model_dump()

            # ---------------------------------
            # Prompt
            # ---------------------------------

            prompt = self.prompt_builder.build(
                query=query,
                documents=documents,
                patient_context=patient_context,
                emergency_status=emergency_status,
                risk_assessment=risk_assessment,
            )

            execution_time = round(
                time.time() - start_time,
                4,
            )

            return {
                "status": "success",
                "documents": documents,
                "citations": citations,
                "prompt": prompt,
                "metadata": {
                    "query": query,
                    "documents_retrieved": len(documents),
                    "top_k": top_k,
                    "execution_time_seconds": execution_time,
                },
            }

        except Exception as error:

            logger.exception("RAG pipeline failed")

            return {
                "status": "error",
                "documents": [],
                "citations": [],
                "prompt": "",
                "metadata": {
                    "error": str(error),
                },
            }