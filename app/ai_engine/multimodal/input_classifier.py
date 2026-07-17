"""
Production Input Classifier

This module automatically detects the incoming input type
(Text, Voice, Image, OCR Document, Mixed).

The classifier is intentionally lightweight and independent
from downstream AI models so it can be reused across APIs,
background workers and batch jobs.
"""

from __future__ import annotations

import mimetypes
from enum import Enum
from pathlib import Path
from typing import Optional


class InputType(str, Enum):
    """
    Supported multimodal input types.
    """

    TEXT = "text"
    VOICE = "voice"
    IMAGE = "image"
    OCR_DOCUMENT = "ocr_document"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class InputClassifier:
    """
    Automatically classifies incoming user input.

    Examples
    --------

    classifier = InputClassifier()

    classifier.classify(
        text="I have chest pain"
    )

    -> InputType.TEXT


    classifier.classify(
        file_name="voice.mp3"
    )

    -> InputType.VOICE


    classifier.classify(
        file_name="report.pdf"
    )

    -> InputType.OCR_DOCUMENT
    """

    VOICE_EXTENSIONS = {
        ".wav",
        ".mp3",
        ".m4a",
        ".aac",
        ".ogg",
        ".flac",
    }

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
        ".tif",
        ".tiff",
    }

    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
    }

    def classify(
        self,
        *,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> InputType:
        """
        Detect the incoming input type.

        Priority

        Mixed
            Text + File

        Text
            Plain user message

        Voice
            Audio formats

        Image
            Medical images

        OCR Document
            PDF / DOC / DOCX

        Unknown
            Unsupported input
        """

        has_text = bool(text and text.strip())
        has_file = bool(file_name)

        if has_text and has_file:
            return InputType.MIXED

        if has_text:
            return InputType.TEXT

        if not has_file:
            return InputType.UNKNOWN

        extension = Path(file_name).suffix.lower()

        if self._is_voice(extension, mime_type):
            return InputType.VOICE

        if self._is_image(extension, mime_type):
            return InputType.IMAGE

        if self._is_document(extension, mime_type):
            return InputType.OCR_DOCUMENT

        return InputType.UNKNOWN

    def _is_voice(
        self,
        extension: str,
        mime_type: Optional[str],
    ) -> bool:
        """
        Detect audio input.
        """

        if extension in self.VOICE_EXTENSIONS:
            return True

        if mime_type:
            return mime_type.startswith("audio/")

        return False

    def _is_image(
        self,
        extension: str,
        mime_type: Optional[str],
    ) -> bool:
        """
        Detect image input.
        """

        if extension in self.IMAGE_EXTENSIONS:
            return True

        if mime_type:
            return mime_type.startswith("image/")

        return False

    def _is_document(
        self,
        extension: str,
        mime_type: Optional[str],
    ) -> bool:
        """
        Detect OCR-compatible documents.
        """

        if extension in self.DOCUMENT_EXTENSIONS:
            return True

        if mime_type:
            return (
                mime_type
                in {
                    "application/pdf",
                    "application/msword",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                }
            )

        return False

    @staticmethod
    def guess_mime_type(
        file_name: str,
    ) -> Optional[str]:
        """
        Guess MIME type using the filename.

        Useful when clients do not provide
        Content-Type.
        """

        mime_type, _ = mimetypes.guess_type(file_name)
        return mime_type