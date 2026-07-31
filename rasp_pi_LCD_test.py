#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from mfrc522 import SimpleMFRC522
import time

serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

UID = {
    660952385193: "Stephen Kuebler",
    84873119234: "Nicholas Young",
    829966124588: "Kyle Langlois",
    698318784313: "Logan Smith",
    770927363601: "Tyrone Thames",
    213938826799: "Tyrone Morales",
    212213919448: "Alexander Cockerham",
    211993128642: "Chad Horton"
}

def display_signed_in(names):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), "Signed In:", fill=255)

    col1_x = 0
    col2_x = 70
    row_height = 12

    for i, name in enumerate(names):
        row = i % 4
        col = i // 4
        x = col1_x if col == 0 else col2_x
        y = 12 + row * row_height
        draw.text((x, y), name[:12], fill=255)

    oled.display(image)

reader = SimpleMFRC522()
signed_in = []

display_signed_in(signed_in)

while True:
    try:
        uid, text = reader.read()
        name = UID.get(uid, "Unknown")

        if name not in signed_in:
            signed_in.append(name)

        display_signed_in(signed_in)
        time.sleep(1)

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
