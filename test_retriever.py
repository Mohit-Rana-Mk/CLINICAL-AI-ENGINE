from app.ai_engine.rag.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve(
    "I have severe chest pain and breathing difficulty."
)

print()

for result in results:

    print(result.document.title)

    print(round(result.similarity_score, 3))

    print()