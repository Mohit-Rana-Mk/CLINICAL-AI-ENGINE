from pathlib import Path

from pydantic import BaseModel


class OCRResult(BaseModel):
    status: str
    document_type: str
    extracted_text: str


class OCRRouter:

    def detect_document(
        self,
        file_name: str,
    ) -> str:

        name = Path(file_name).stem.lower()

        if "prescription" in name:
            return "prescription"

        if "lab" in name:
            return "lab_report"

        if "discharge" in name:
            return "discharge_summary"

        if "certificate" in name:
            return "medical_certificate"

        return "unknown"

    def process(
        self,
        file_name: str,
    ) -> OCRResult:

        return OCRResult(
            status="success",
            document_type=self.detect_document(file_name),
            extracted_text="",
        )