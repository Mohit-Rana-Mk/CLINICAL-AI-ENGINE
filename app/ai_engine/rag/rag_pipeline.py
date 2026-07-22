import logging
from threading import Lock

from app.ai_engine.rag.document_loader import MedicalDocumentLoader

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Production Clinical RAG Pipeline.

    Responsibilities
    ----------------
    - Load clinical knowledge
    - Build vector index once
    - Provide semantic retrieval
    - Reuse vector database across requests
    """

    _initialized = False
    _vector_store = None
    _lock = Lock()

    def __init__(self):

        self.loader = MedicalDocumentLoader()

        if not RAGPipeline._initialized:

            with RAGPipeline._lock:

                if not RAGPipeline._initialized:

                    logger.info(
                        "Building Clinical Knowledge Index..."
                    )

                    try:
                        # Qdrant and sentence-transformers are optional runtime
                        # enrichments.  Import them here so a missing ML package
                        # cannot prevent FastAPI from loading its core triage API.
                        from app.ai_engine.rag.vector_store import VectorStore

                        vector_store = VectorStore()
                        documents = self.loader.load_documents()

                        if documents:
                            logger.info(
                                "Indexing %d clinical documents",
                                len(documents),
                            )
                            vector_store.add_documents(documents)
                        else:
                            logger.warning("No clinical documents available.")

                        RAGPipeline._vector_store = vector_store
                    except Exception as error:
                        # Retrieval is enrichment, not a prerequisite for safe
                        # triage.  Keep the API available when Qdrant or the
                        # embedding model is temporarily unavailable.
                        logger.warning(
                            "RAG unavailable; continuing without retrieval: %s",
                            error,
                        )
                        RAGPipeline._vector_store = None
                    RAGPipeline._initialized = True

        self.vector_store = RAGPipeline._vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        if not query:

            return []

        query = query.strip()

        if not query:

            return []

        top_k = max(
            1,
            min(
                top_k,
                20,
            ),
        )

        logger.info(
            "Searching clinical evidence..."
        )

        if self.vector_store is None:
            return []

        return self.vector_store.similarity_search(
            query=query,
            top_k=top_k,
        )
