import json
from pathlib import Path

from app.ai_engine.rag.schemas import MedicalDocument


class MedicalDocumentLoader:
    """
    Loads medical knowledge documents from JSON.
    """

    def __init__(self):

        self.base_path = (
            Path(__file__)
            .resolve()
            .parents[3]
            / "knowledge_base"
        )

    def load_documents(
        self,
        filename: str = "medical_documents.json",
    ) -> list[MedicalDocument]:

        file_path = self.base_path / filename

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            raw_documents = json.load(file)

        return [
            MedicalDocument(**document)
            for document in raw_documents
        ]