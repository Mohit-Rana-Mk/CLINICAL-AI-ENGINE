from app.ai_engine.rag.prompt_builder import PromptBuilder
from app.ai_engine.rag.retriever import Retriever

retriever = Retriever()

builder = PromptBuilder()

results = retriever.retrieve(
    "Chest pain with breathing difficulty"
)

prompt = builder.build(
    patient_message="Chest pain with breathing difficulty",
    documents=results,
)

print(prompt)