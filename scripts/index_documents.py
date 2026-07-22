"""
Indexing Pipeline Support

Workflow:
Documents
    ↓
Clean
    ↓
Chunk
    ↓
Embedding
    ↓
Qdrant
"""

from pathlib import Path

KNOWLEDGE_BASE = Path("knowledge_base")


def get_documents():
    """Collect all PDF documents from the knowledge base."""
    return list(KNOWLEDGE_BASE.rglob("*.pdf"))


def clean_document(document_path):
    """
    Placeholder for document cleaning.
    Cleaning will be handled in the NLP pipeline.
    """
    return document_path


def chunk_document(document):
    """
    Placeholder for document chunking.
    Chunking will be performed before embedding generation.
    """
    return [document]


def main():
    documents = get_documents()

    print(f"Found {len(documents)} documents.")

    for doc in documents:
        cleaned = clean_document(doc)
        chunks = chunk_document(cleaned)

        print(f"{doc.name} -> {len(chunks)} chunk(s)")


if __name__ == "__main__":
    main()