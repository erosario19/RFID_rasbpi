#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
import time

serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

draw.text((0, 0), "OLED Test", fill=255)
draw.text((0, 20), "Hello Elizabeth!", fill=255)

oled.display(image)

print("Message displayed.")

# Keep program running
while True:
    time.sleep(1)
