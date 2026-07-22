import logging
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """
    Handles image preprocessing before AI inference.
    """

    SUPPORTED_FORMATS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
        ".tif",
        ".tiff",
    }

    IMAGE_SIZE = (224, 224)

    def validate_image(self, image_path: str) -> bool:
        path = Path(image_path)

        if not path.exists():
            logger.error("Image not found: %s", image_path)
            return False

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            logger.error(
                "Unsupported image format: %s",
                path.suffix
            )
            return False

        return True

    def load_image(
        self,
        image_path: str,
    ) -> Image.Image:

        try:
            return Image.open(image_path).convert("RGB")

        except Exception as exc:
            logger.exception(
                "Failed to load image: %s",
                image_path,
            )
            raise ValueError(
                f"Unable to load image: {image_path}"
            ) from exc

    def resize_image(
        self,
        image: Image.Image
    ) -> Image.Image:
        return image.resize(self.IMAGE_SIZE)

    def normalize_image(
        self,
        image: Image.Image
    ) -> np.ndarray:
        array = np.asarray(
            image,
            dtype=np.float32
        )

        return array / 255.0

    def preprocess(
    self,
    image_path: str,
    ) -> dict[str, Any]:

        if not self.validate_image(image_path):
            return {
            "status": "failed",
            "image": None,
            "error": "Invalid image.",
        }

        try:
            image = self.load_image(image_path)
            image = self.resize_image(image)
            image = self.normalize_image(image)

            return {
                "status": "success",
                "image": image,
                "shape": image.shape,
            }

        except Exception as exc:
            logger.exception(
                "Image preprocessing failed."
            )

            return {
            "status": "failed",
            "image": None,
            "error": str(exc),
            }