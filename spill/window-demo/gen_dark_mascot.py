#!/usr/bin/env python3
"""Dark variant of the Peka P-mascot for light backgrounds.

Same geometry as peka-logo/mascot.py::mascot_p, but rendered as a
transparent RGBA image: the P itself is dark (#111), eye + smile are
transparent holes, so it sits cleanly on the cream SPILL slides.
"""
from PIL import Image, ImageDraw

S = 1080
DARK = (17, 17, 17, 255)

mask = Image.new("L", (S, S), 0)
d = ImageDraw.Draw(mask)
# antenna
d.rounded_rectangle([507, 232, 523, 332], radius=8, fill=255)
d.ellipse([487, 177, 543, 233], fill=255)
# stem (body)
d.rounded_rectangle([450, 330, 580, 822], radius=65, fill=255)
# bowl
d.arc([600 - 140, 455 - 140, 600 + 140, 455 + 140], start=-90, end=90, fill=255, width=100)
# cut out eye + smile
d.ellipse([465, 400, 555, 490], fill=0)
d.arc([470, 515, 550, 595], start=25, end=155, fill=0, width=18)

out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
out.paste(Image.new("RGBA", (S, S), DARK), mask=mask)
out.save("mascot-p-dark.png")
print("saved mascot-p-dark.png", out.size)
