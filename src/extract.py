"""Read a photographed company notice into value, evidence, and confidence.

The model does not decide the route. checks.decide() does that, with no model call.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field as PField

from .images import downscale
from .llm import complete_json

PROMPT = (
    "Read this company notice. For every field return value, evidence "
    "(the exact text you read) and confidence. If you cannot read a field, "
    "set value and evidence to null. Never guess."
)


class Field(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str | None
    evidence: str | None
    confidence: float = PField(ge=0.0, le=1.0)


class Extraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Field
    action: Field
    timing: Field
    contact: Field


FIELDS = ("title", "action", "timing", "contact")


def extract(image_bytes: bytes) -> Extraction:
    raw = complete_json(PROMPT, image=downscale(image_bytes), schema=Extraction.model_json_schema())
    return Extraction.model_validate(raw)


if __name__ == "__main__":
    print(json.dumps(extract(Path(sys.argv[1]).read_bytes()).model_dump(), indent=2))
