#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from mfrc522 import SimpleMFRC522
import time

serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

# UID → Name mapping
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

def display_message(line1, line2=""):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), line1, fill=255)
    draw.text((0, 20), line2, fill=255)
    oled.display(image)

display_message("Ready to Scan")

reader = SimpleMFRC522()
print("Waiting for RFID card...")

signed_in = []  

while True:
    try:
        uid, text = reader.read()
        print(f"Card detected: {uid}")

        name = UID.get(uid, "Unknown")

        if name not in signed_in:
            signed_in.append(name)

        if len(signed_in) == 1:
            display_message("Signed In:", signed_in[0])
        else:
            last_two = signed_in[-2:]
            line1 = "Signed In:"
            line2 = ", ".join(last_two)
            display_message(line1, line2)

        time.sleep(2)

        display_message("Ready to Scan")

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
