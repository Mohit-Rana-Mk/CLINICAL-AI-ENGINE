from app.ai_engine.rag.rag_service import RAGService

rag = RAGService()

result = rag.process(
    "Chest pain with breathing difficulty"
)

print("\nRetrieved Documents:", len(result["documents"]))

print("\nCitations:")
for citation in result["citations"]:
    print(citation)

print("\nPrompt Preview:\n")
print(result["prompt"][:700])