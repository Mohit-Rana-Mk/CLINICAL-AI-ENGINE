from pathlib import Path

from pydantic import BaseModel


class ImageResult(BaseModel):
    status: str
    image_type: str
    route: str


class ImageRouter:

    IMAGE_TYPES = {
        "skin": "skin_model",
        "eye": "eye_model",
        "tongue": "tongue_model",
        "wound": "wound_model",
        "prescription": "ocr",
        "lab_report": "ocr",
    }

    def detect_type(
        self,
        file_name: str,
    ) -> str:

        name = Path(file_name).stem.lower()

        for key in self.IMAGE_TYPES:

            if key in name:
                return key

        return "general"

    def process(
        self,
        file_name: str,
    ) -> ImageResult:

        image_type = self.detect_type(file_name)

        return ImageResult(
            status="success",
            image_type=image_type,
            route=self.IMAGE_TYPES.get(
                image_type,
                "general_model",
            ),
        )