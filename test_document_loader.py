from app.ai_engine.rag.document_loader import MedicalDocumentLoader

loader = MedicalDocumentLoader()

documents = loader.load_documents()

print(f"Loaded {len(documents)} documents.\n")

for document in documents:
    print(document.title)