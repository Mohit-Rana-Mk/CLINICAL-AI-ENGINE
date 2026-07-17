from app.ai_engine.multimodal.image_router import ImageRouter
from app.ai_engine.multimodal.input_classifier import (
    InputClassifier,
    InputType,
)
from app.ai_engine.multimodal.ocr_router import OCRRouter
from app.ai_engine.multimodal.voice_router import VoiceRouter


class MultimodalPipeline:

    def __init__(self):

        self.classifier = InputClassifier()

        self.voice = VoiceRouter()

        self.image = ImageRouter()

        self.ocr = OCRRouter()

    def process(
        self,
        *,
        text=None,
        file_name=None,
        mime_type=None,
    ):

        input_type = self.classifier.classify(
            text=text,
            file_name=file_name,
            mime_type=mime_type,
        )

        if input_type == InputType.TEXT:
            return {
                "type": "text",
                "content": text,
            }

        if input_type == InputType.VOICE:
            return self.voice.process(file_name)

        if input_type == InputType.IMAGE:
            return self.image.process(file_name)

        if input_type == InputType.OCR_DOCUMENT:
            return self.ocr.process(file_name)

        return {
            "type": "unknown",
        }