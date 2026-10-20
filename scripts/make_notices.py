"""Render the four synthetic notice photos used as Lab 3 fixtures."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "tests" / "images"
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 42)
TITLE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 56)


def card(name, heading, lines, cover=None, banner="COMPANY NOTICE"):
    image = Image.new("RGB", (1600, 2000), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((40, 40, 1560, 1960), outline="black", width=6)
    draw.text((90, 90), banner, font=TITLE, fill="black")
    draw.text((90, 200), heading, font=TITLE, fill="black")
    y = 340
    for line in lines:
        draw.text((90, y), line, font=FONT, fill="black")
        y += 78
    if cover:
        draw.rectangle(cover, fill=(190, 190, 190))
    image.save(OUT / name, format="JPEG", quality=85, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    card(
        "clean.jpg",
        "Time off",
        [
            "Title: Time off",
            "Action: File a request in the HR form",
            "Timing: at least 5 working days ahead",
            "Contact: your manager",
        ],
    )
    card(
        "degraded.jpg",
        "Time off",
        [
            "Title: Time off",
            "Action: File a request in the HR form",
            "Timing: at least 5 working days ahead",
            "Contact: your manager",
        ],
        cover=(80, 400, 1500, 490),
    )
    card(
        "ambiguous.jpg",
        "Time off",
        [
            "Title: Time off",
            "Action: File a request in the HR form",
            "Timing: sometime next week??",
            "Contact: your manager",
        ],
    )
    card(
        "not-applicable.jpg",
        "Friday lunch",
        [
            "Soup and bread",
            "Salad",
            "Tea",
        ],
        banner="FRIDAY LUNCH MENU",
    )


if __name__ == "__main__":
    main()
