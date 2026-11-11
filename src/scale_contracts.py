"""The tool contract for scale_notice. Both doors read this file.

  * src/tools.py registers ScaleNotice in TOOLS (the function-calling door)
  * src/mcp_scale.py builds the MCP tool from the same Pixel and PhotoLabel types

Rules:
  * extra="forbid": an argument we did not ask for is an error
  * width and height are the measured photo size, each from 1 to 4096
  * the label is one short line: a pattern and at most 80 characters,
    so a newline cannot carry instructions in with the measurements
  * the longest side stays 1024 inside the tool. The model cannot choose it
  * nothing here names who is calling
"""
from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Pixel = Annotated[
    int,
    Field(ge=1, le=4096, description="One side of the photo in pixels, from 1 to 4096"),
]
PhotoLabel = Annotated[
    str,
    Field(
        min_length=1,
        max_length=80,
        description="One short line naming what the photo shows, at most 80 characters. No line breaks.",
    ),
]


class ScaleNotice(BaseModel):
    """Give the size a notice photo will have after it is downscaled to 1024 pixels on the longest side. Reads only. It never sends the photo or stores it."""

    model_config = ConfigDict(extra="forbid")

    width: Pixel
    height: Pixel
    label: PhotoLabel
