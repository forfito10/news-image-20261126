#!/usr/bin/env python3
"""Render a compact editorial briefing as a 1080x1350 PNG."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG = "#0f1720"
PANEL = "#17232e"
INK = "#f3f6f8"
MUTED = "#a8b7c4"
TEAL = "#42d6c5"

STORIES = [
    ("HUANG RETURNS AS NVIDIA CEO", "Jensen Huang has returned to the chief executive role as Nvidia reshapes its leadership around the next phase of the AI boom."),
    ("CROWDSTRIKE AND ZSCALER: $43.9B", "A proposed $43.9 billion combination would unite two major cybersecurity firms and redraw the contest for cloud security."),
    ("700,000 RUSSIAN SOLDIERS KILLED", "A new estimate puts Russian military deaths at roughly 700,000 since the invasion of Ukraine, underscoring the war's staggering toll."),
    ("RSF ADVANCES IN KHARTOUM", "Sudan's Rapid Support Forces have pushed farther into Khartoum as fighting intensifies and civilians face worsening danger."),
    ("ICJ HEARS MYANMAR GENOCIDE CASE", "The International Court of Justice has opened hearings on allegations that Myanmar committed genocide against the Rohingya."),
]


def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, face, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=face) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def main():
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((64, 66, 76, 292), radius=6, fill=TEAL)
    draw.text((105, 73), "WORLD / BRIEFING", font=font(22, True), fill=TEAL)
    draw.text((105, 119), "FIVE STORIES", font=font(66, True), fill=INK)
    draw.text((105, 193), "MOVING THE WORLD TODAY", font=font(47, True), fill=INK)
    draw.text((107, 267), "NOVEMBER 25 2026", font=font(22, True), fill=MUTED)
    draw.line((64, 326, 1016, 326), fill="#344552", width=2)
    head, body = font(27, True), font(20)
    y = 354
    for index, (headline, summary) in enumerate(STORIES, 1):
        box = (64, y, 1016, y + 174)
        draw.rounded_rectangle(box, radius=14, fill=PANEL)
        draw.rounded_rectangle((64, y, 71, y + 174), radius=3, fill=TEAL)
        draw.text((94, y + 22), f"{index:02d}", font=font(19, True), fill=TEAL)
        x = 148
        for n, line in enumerate(wrap(draw, headline, head, 820)):
            draw.text((x, y + 17 + n * 34), line, font=head, fill=INK)
        summary_y = y + 17 + max(1, len(wrap(draw, headline, head, 820))) * 34 + 6
        for n, line in enumerate(wrap(draw, summary, body, 820)[:2]):
            draw.text((x, summary_y + n * 28), line, font=body, fill=MUTED)
        y += 190
    draw.text((64, 1320), "compiled from global reporting - make.fun daily brief", font=font(16, True), fill="#708391")
    output = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(output, exist_ok=True)
    image.save(os.path.join(output, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
