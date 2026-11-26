#!/usr/bin/env python3
"""Render a compact editorial briefing as a 1080x1350 PNG."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG = "#101822"
PANEL = "#17232e"
INK = "#f3f6f8"
MUTED = "#a8b7c4"
TEAL = "#4fd1c5"

STORIES = [
    ("US ARMY DETONATES IOWA STOCKPILE", "The Army called the detonation of a lead azide stockpile in Iowa a success after initial fears of a toxic plume drifting toward nearby communities."),
    ("HUANG-LINKED FIRMS PLEDGED $301M", "Reuters-reviewed records show firms linked to Alice Huang raised financing against AI servers and equipment worth $301 million in China as US authorities probe suspected chip diversion."),
    ("PLANE CRASH OFF MISSISSIPPI KILLS 6", "A small plane crashed off the Gulf coast during a family fishing trip, killing six members of an extended family in a single blow."),
    ("NORTH KOREA ORDERS DIPLOMAT OUT", "Pyongyang demanded the closure of Switzerland's new diplomatic office and ordered one diplomat to leave, deepening a rare dispute with a neutral broker."),
    ("COGNIZANT EYES S&P CAPITAL IQ OPS", "Cognizant is in talks to take over data and operations staff from S&P Global's India GCC, with around 1,500 employees potentially moving to its payroll."),
]


def font(size, bold=False):
    regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    strong = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    mac_regular = "/Library/Fonts/Arial.ttf"
    mac_bold = "/Library/Fonts/Arial Bold.ttf"
    for path in (strong if bold else regular, mac_bold if bold else mac_regular):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, face, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_story(draw, index, story, top, title_face, body_face):
    headline, summary = story
    bottom = top + 174
    draw.rounded_rectangle((64, top, 1016, bottom), radius=14, fill=PANEL)
    draw.rounded_rectangle((64, top, 71, bottom), radius=3, fill=TEAL)
    draw.text((94, top + 22), f"{index:02d}", font=font(19, True), fill=TEAL)

    text_x = 148
    headline_lines = wrap(draw, headline, title_face, 820)
    for row, line in enumerate(headline_lines):
        draw.text((text_x, top + 17 + row * 34), line, font=title_face, fill=INK)

    summary_top = top + 17 + max(1, len(headline_lines)) * 34 + 6
    for row, line in enumerate(wrap(draw, summary, body_face, 820)[:2]):
        draw.text((text_x, summary_top + row * 28), line, font=body_face, fill=MUTED)


def main():
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle((64, 66, 76, 292), radius=6, fill=TEAL)
    draw.text((105, 73), "WORLD / BRIEFING", font=font(22, True), fill=TEAL)
    draw.text((105, 119), "FIVE STORIES", font=font(66, True), fill=INK)
    draw.text((105, 193), "MOVING THE WORLD TODAY", font=font(47, True), fill=INK)
    draw.line((105, 254, 232, 254), fill="#d8b46a", width=2)
    draw.text((107, 267), "November 26, 2026", font=font(22, True), fill=MUTED)
    draw.line((64, 326, 1016, 326), fill="#344552", width=2)

    title_face, body_face = font(27, True), font(20)
    top = 354
    for index, story in enumerate(STORIES, 1):
        draw_story(draw, index, story, top, title_face, body_face)
        top += 190

    draw.text((64, 1320), "WORLD DESK  •  Reported 26 November 2026", font=font(16, True), fill="#708391")
    output = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(output, exist_ok=True)
    image.save(os.path.join(output, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
