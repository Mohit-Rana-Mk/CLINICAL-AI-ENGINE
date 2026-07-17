from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, Field


class VoiceMetadata(BaseModel):
    filename: str
    extension: str
    language: str = "unknown"
    duration: float = 0.0
    confidence: float = 0.0


class VoiceResult(BaseModel):
    status: str
    text: str
    language: str
    confidence: float
    duration: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VoiceRouter:
    """
    Production-ready Voice Router.

    Future:
        Whisper
        Faster-Whisper
        Gemini
        Deepgram

    Only transcribe() will change.
    """

    SUPPORTED_FORMATS = {
        ".wav",
        ".mp3",
        ".m4a",
        ".aac",
        ".ogg",
        ".flac",
    }

    def validate_audio(self, file_name: str) -> None:
        extension = Path(file_name).suffix.lower()

        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported audio format: {extension}"
            )

    def extract_metadata(
        self,
        file_name: str,
    ) -> VoiceMetadata:

        extension = Path(file_name).suffix.lower()

        return VoiceMetadata(
            filename=file_name,
            extension=extension,
        )

    def transcribe(
        self,
        file_path: str,
    ) -> tuple[str, float, str]:
        """
        Placeholder.

        Replace later with:
        - Whisper
        - Faster Whisper
        - OpenAI
        - Gemini
        """

        return (
            "",
            0.0,
            "unknown",
        )

    def process(
    self,
    file_path: str,
    ) -> VoiceResult:

        self.validate_audio(file_path)

        metadata = self.extract_metadata(file_path)

        text, confidence, language = self.transcribe(file_path)

        metadata.language = language
        metadata.confidence = confidence

        return VoiceResult(
        status="success",
        text=text,
        language=language,
        confidence=confidence,
        duration=metadata.duration,
        metadata={
            **metadata.model_dump(),
            "router": "voice_router",
        },
    )