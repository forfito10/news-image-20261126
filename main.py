from pathlib import Path
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
out = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "out"))
out.mkdir(parents=True, exist_ok=True)
im = Image.new("RGB", (W, H), "#101923")
d = ImageDraw.Draw(im)

def font(size, bold=False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size)

d.rectangle((0, 0, W, 14), fill="#efaa58")
d.text((72, 66), "WORLD / BRIEFING", font=font(20, True), fill="#efaa58")
d.text((72, 108), "THE DAY IN FIVE STORIES", font=font(54, True), fill="#f5f2e9")
d.text((75, 184), "Five stories moving the world today", font=font(26), fill="#b4c0c9")
d.line((72, 244, 1008, 244), fill="#344454", width=2)

stories = [
    ("US ARMY DETONATES IOWA STOCKPILE", "Officials called the lead azide blast a success.", "That eased fears of a toxic plume reaching nearby areas."),
    ("FIRMS TIED TO HUANG PLEDGED $301M", "The money backed AI server ventures in China.", "Those ties now sit within a chip diversion probe."),
    ("PLANE CRASH OFF MISSISSIPPI KILLS 6", "Six relatives died while on a family fishing outing.", "All were members of one extended family."),
    ("NORTH KOREA ORDERS DIPLOMAT OUT", "Pyongyang told Switzerland to shut a new office.", "The demand strains ties with a rare neutral broker."),
    ("COGNIZANT EYES S&P CAPITAL IQ OPS", "Talks cover data and operations staff based in India.", "About 1,500 workers could shift to Cognizant."),
]
top, card_h, gap = 276, 174, 16
for i, (title, line1, line2) in enumerate(stories, 1):
    y = top + (i - 1) * (card_h + gap)
    d.rounded_rectangle((72, y, 1008, y + card_h), radius=16, fill="#192633", outline="#2b3c4b", width=2)
    d.rounded_rectangle((72, y, 80, y + card_h), radius=4, fill="#efaa58")
    d.text((103, y + 24), f"0{i}", font=font(18, True), fill="#efaa58")
    d.text((151, y + 20), title, font=font(26, True), fill="#f5f2e9")
    d.text((151, y + 76), line1, font=font(22), fill="#c4ced5")
    d.text((151, y + 111), line2, font=font(22), fill="#c4ced5")

d.line((72, 1228, 1008, 1228), fill="#344454", width=2)
d.text((72, 1250), "WORLD DESK  •  Reported 26 November 2026", font=font(20, True), fill="#efaa58")
im.save(out / "entry.png")
