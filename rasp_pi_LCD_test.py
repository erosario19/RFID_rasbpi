#!/usr/bin/env python3
from PIL import Image, ImageDraw
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time
import csv
import os

GPIO.setwarnings(False)
serial = i2c(port=1, address=0x3C)
oled = sh1106(serial)

CSV_PATH = "/home/npmraspberry/RFID_rasbpi/attendance_log.csv"

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
    try:
        return reader.read_id_no_block()
    except Exception as e:
        print(f"Read error: {e}")
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
    date = time.strftime("%Y-%m-%d")
    ts = time.strftime("%H:%M:%S")
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), str(uid), fill=255)
    draw.text((0, 20), date, fill=255)
    draw.text((0, 40), ts, fill=255)
    draw.text((0, 55), full_name, fill=255)
    oled.display(image)

def log_csv(uid, full_name, status):
    date = time.strftime("%Y-%m-%d")
    ts = time.strftime("%H:%M:%S")
    exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["UID", "FullName", "Date", "Time", "Status"])
        writer.writerow([uid, full_name, date, ts, status])

signed_in = []
display_signed_in(signed_in)
reader = SimpleMFRC522()
last_uid = None
last_time = 0
debounce_delay = 0.8

while True:
    try:
        uid = read_uid_only(reader)
        if uid is None:
            continue
        if uid == last_uid and time.time() - last_time < debounce_delay:
            continue
        last_uid = uid
        last_time = time.time()

        if uid in UID:
            full = UID[uid]
            short = short_name(full)
        else:
            full = "Unknown"
            short = "Unknown"

        if short in signed_in:
            signed_in.remove(short)
            status = "OUT"
        else:
            signed_in.append(short)
            status = "IN"

        log_csv(uid, full, status)
        display_scan(uid, full)
        time.sleep(2)
        display_signed_in(signed_in)
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
        continue
