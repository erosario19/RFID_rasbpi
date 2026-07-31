#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

# Initialize I2C OLED
serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

def display_message_forever(line1, line2=""):
    # Create a persistent image buffer
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Draw text onto the image
    draw.text((0, 0), line1, fill=255)
    draw.text((0, 20), line2, fill=255)

    # Display the image and KEEP it there forever
    oled.display(image)

# Show message permanently
display_message_forever("OLED Test", "Hello Elizabeth!")
print("Displayed permanent message on OLED.")
