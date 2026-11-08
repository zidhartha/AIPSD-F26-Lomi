"""scale_notice: the Lab 3 photo downscale as a tool, behind src/scale_contracts.py.

It runs images.downscale() on a photo of the measured size. It does not read a file,
call a model, store the photo, or send it. The longest side stays 1024 and the JPEG
quality stays 85. It takes no caller.
"""
from __future__ import annotations

import io

from PIL import Image
from pydantic import BaseModel

from . import images
from .scale_contracts import ScaleNotice

LONGEST = 1024
SCALED = "Resize the photo so the longest side is 1024 pixels before you send it. Do not send the original."
READY = "The photo is already within 1024 pixels on the longest side. You may send it."


class ScaleResult(BaseModel):
    scaled: bool
    width: int
    height: int
    next_step: str


def scale_notice(args: ScaleNotice) -> ScaleResult:
    blank = Image.new("RGB", (args.width, args.height), (255, 255, 255))
    raw = io.BytesIO()
    blank.save(raw, format="JPEG")
    out = Image.open(io.BytesIO(images.downscale(raw.getvalue())))
    width, height = out.size
    scaled = max(args.width, args.height) > LONGEST
    return ScaleResult(scaled=scaled, width=width, height=height, next_step=SCALED if scaled else READY)
