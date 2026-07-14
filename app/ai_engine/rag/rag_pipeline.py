from app.ai_engine.rag.document_loader import MedicalDocumentLoader
from app.ai_engine.rag.vector_store import InMemoryVectorStore


class RAGPipeline:
    """
    End-to-end RAG pipeline.
    Loads medical documents, indexes them,
    and performs semantic retrieval.
    """

    def __init__(self):

        self.loader = MedicalDocumentLoader()

        self.vector_store = InMemoryVectorStore()

        self._build_index()

    def _build_index(self):

        documents = self.loader.load_documents()

        self.vector_store.add_documents(documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        return self.vector_store.similarity_search(
            query=query,
            top_k=top_k,
        )