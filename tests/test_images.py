import io
from pathlib import Path

from PIL import Image

from src.extract import Extraction, Field, extract
from src.images import downscale

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "tests" / "images"
NAMES = ("clean.jpg", "degraded.jpg", "ambiguous.jpg", "not-applicable.jpg")


def test_four_notice_images_exist_and_are_small_enough():
    for name in NAMES:
        path = IMAGES / name
        assert path.is_file()
        assert path.stat().st_size < 2_000_000
        with Image.open(path) as image:
            assert image.format == "JPEG"


def test_downscale_limits_the_longest_side():
    huge = Image.new("RGB", (1800, 2400), "white")
    raw = io.BytesIO()
    huge.save(raw, format="JPEG")
    small = downscale(raw.getvalue())
    with Image.open(io.BytesIO(small)) as image:
        assert max(image.size) <= 1024
        assert max(image.size) > 100


def test_extract_sends_the_downscaled_image(monkeypatch):
    seen = {}

    def fake(prompt, image=None, schema=None):
        seen["image"] = image
        return Extraction(
            title=Field(value="Time off", evidence="Time off", confidence=0.9),
            action=Field(value="File a request in the HR form", evidence="File a request in the HR form", confidence=0.9),
            timing=Field(value="at least 5 working days ahead", evidence="at least 5 working days ahead", confidence=0.9),
            contact=Field(value="your manager", evidence="your manager", confidence=0.9),
        ).model_dump()

    monkeypatch.setattr("src.extract.complete_json", fake)
    huge = Image.new("RGB", (1800, 2400), "white")
    raw = io.BytesIO()
    huge.save(raw, format="JPEG")
    original = raw.getvalue()
    extract(original)
    assert len(seen["image"]) < len(original)
