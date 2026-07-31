#!/usr/bin/env python3
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

# Initialize I2C OLED
serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

def display_message(line1, line2=""):
    with canvas(oled) as draw:
        draw.text((0, 0), line1, fill=255)
        draw.text((0, 20), line2, fill=255)

# Test message
display_message("OLED Test", "Hello Elizabeth!")
print("Displayed test message on OLED.")
