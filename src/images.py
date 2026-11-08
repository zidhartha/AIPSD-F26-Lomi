"""Downscale a phone photo before it is sent to a model."""
from __future__ import annotations

import io

from PIL import Image


def downscale(image_bytes: bytes, max_side: int = 1024, quality: int = 85) -> bytes:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    scale = max_side / max(width, height)
    if scale < 1:
        image = image.resize((max(1, round(width * scale)), max(1, round(height * scale))), Image.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="JPEG", quality=quality, optimize=True)
    return output.getvalue()
