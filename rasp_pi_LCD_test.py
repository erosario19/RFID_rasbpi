#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

# Initialize I2C OLED
serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

def display_message(line1, line2=""):
  
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), line1, fill=255)
    draw.text((0, 20), line2, fill=255)

    oled.display(image)

# Test message
display_message("OLED Test", "test!")
print("Displayed test message on OLED.")
