#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from mfrc522 import SimpleMFRC522
import time

# Initialize OLED
serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

def display_message(line1, line2=""):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), line1, fill=255)
    draw.text((0, 20), line2, fill=255)
    oled.display(image)

# Initial screen (stays forever)
display_message("Ready to Scan", "Present your card")

# Initialize RC522
reader = SimpleMFRC522()

print("Waiting for RFID card...")

while True:
    try:
        id, text = reader.read()
        print(f"Card detected: {id}")

        # Update OLED permanently
        display_message("Card Scanned!", f"ID: {id}")

        time.sleep(2)

        # Return to idle screen
        display_message("Ready to Scan", "Present your card")

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
