#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import time

# --- OLED SETUP ---
serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

# --- UID → NAME MAPPING ---
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

# --- SHORT NAME RULES ---
def short_name(full):
    if full == "Tyrone Thames":
        return "Tyrone T"
    if full == "Tyrone Morales":
        return "Tyrone M"
    return full.split()[0]

# --- RELIABLE RFID READ (THIS FIXES YOUR FREEZE) ---
def read_uid_only(reader):
    try:
        uid, _ = reader.read()   # FULL READ — WORKS EVERY TIME
        return uid
    except:
        return None

# --- SIGNED-IN SCREEN ---
def display_signed_in(names):
    image = Image.new("1", (oled.width, oled.height))  # FULL CLEAR
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

# --- SCAN SCREEN ---
def display_scan(uid, full_name):
    ts = time.strftime("%H:%M:%S")

    image = Image.new("1", (oled.width, oled.height))  # FULL CLEAR
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), str(uid), fill=255)
    draw.text((0, 20), ts, fill=255)
    draw.text((0, 40), full_name, fill=255)

    oled.display(image)

# --- MAIN LOOP ---
reader = SimpleMFRC522()
signed_in = []
startup_time = time.time()

last_uid = None
last_time = 0
debounce_delay = 0.8

display_signed_in(signed_in)

while True:
    try:
        uid = read_uid_only(reader)

        if uid is None:
            continue

        # Prevent double-scan
        if uid == last_uid and time.time() - last_time < debounce_delay:
            continue

        last_uid = uid
        last_time = time.time()

        if uid not in UID:
            continue

        full = UID[uid]
        short = short_name(full)

        # Toggle logic
        if short in signed_in:
            signed_in.remove(short)
        else:
            signed_in.append(short)

        # Show scan screen
        display_scan(uid, full)
        time.sleep(2)

        # Return to signed-in list
        display_signed_in(signed_in)
        time.sleep(0.5)

    except KeyboardInterrupt:
        break

    except Exception as e:
        print("Error:", e)
        continue
