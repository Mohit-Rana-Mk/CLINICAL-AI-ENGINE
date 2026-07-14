from app.ai_engine.rag.embedding_engine import EmbeddingEngine

engine = EmbeddingEngine()

vector = engine.embed_text(
    "Patient has chest pain and breathing difficulty."
)

print("Embedding Dimension:", engine.get_dimension())
print("Vector Length:", len(vector))
print("First 10 Values:", vector[:10])