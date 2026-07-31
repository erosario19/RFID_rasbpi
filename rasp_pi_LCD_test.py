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

def short_name(full):
    if full == "Tyrone Thames":
        return "Tyrone T"
    if full == "Tyrone Morales":
        return "Tyrone M"
    return full.split()[0]

def read_uid_only(reader):
    reader.READER.init()
    (status, uid) = reader.READER.anticoll()
    if status == reader.READER.OK:
        return int("".join(str(x) for x in uid))
    return None

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

def display_scan(uid, full_name):
    ts = time.strftime("%H:%M:%S")
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), str(uid), fill=255)
    draw.text((0, 20), ts, fill=255)
    draw.text((0, 40), full_name, fill=255)
    oled.display(image)

reader = SimpleMFRC522()
signed_in = []
startup_time = time.time()

display_signed_in(signed_in)

while True:
    try:
        uid = read_uid_only(reader)
        if uid is None:
            continue

        if time.time() - startup_time < 1:
            signed_in = []
            display_signed_in(signed_in)
            continue

        if uid not in UID:
            continue

        full = UID[uid]
        short = short_name(full)

        if short in signed_in:
            signed_in.remove(short)
        else:
            signed_in.append(short)

        display_scan(uid, full)
        time.sleep(2)

        display_signed_in(signed_in)
        time.sleep(0.5)

    except KeyboardInterrupt:
        break

    except:
        continue
