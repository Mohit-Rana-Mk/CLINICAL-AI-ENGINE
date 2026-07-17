from app.ai_engine.rag.citation_engine import CitationEngine
from app.ai_engine.rag.retriever import Retriever

retriever = Retriever()

documents = retriever.retrieve(
    "chest pain with breathing difficulty"
)

engine = CitationEngine()

citations = engine.generate(documents)

print("\nGenerated Citations\n")

for citation in citations:
    print(citation)