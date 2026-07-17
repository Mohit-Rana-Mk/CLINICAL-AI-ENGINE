from app.ai_engine.rag.retriever import Retriever
from app.ai_engine.rag.reranker import Reranker

retriever = Retriever()

reranker = Reranker()

results = retriever.retrieve(
    "Chest pain with breathing difficulty"
)

results = reranker.rerank(results)

for index, result in enumerate(results, start=1):

    print(f"{index}. {result.document.title}")

    print(result.similarity_score)

    print()