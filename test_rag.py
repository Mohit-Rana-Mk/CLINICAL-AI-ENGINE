from app.ai_engine.rag.rag_pipeline import RAGPipeline

rag = RAGPipeline()

query = "I have chest pain and difficulty breathing."

results = rag.retrieve(query)

print("\nRetrieved Documents\n")

for index, result in enumerate(results, start=1):

    print("-" * 60)

    print(f"Rank : {index}")

    print(f"Score : {result.similarity_score:.3f}")

    print(f"Title : {result.document.title}")

    print(f"Category : {result.document.category}")

    print(f"Source : {result.document.source}")

    print(f"Content : {result.document.content}")