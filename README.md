# RFID_rasbpi

## Electronics Used: 
$\bullet$ Raspberry Pi Zero 2W
$\bullet$ RFID RC522 Module 
$\bullet$ 0.96 Inch OLED I2C IIC module 

## Purpose: 
This code is used to connect the RC522 scanner and the OLED display so that whenever a card or keychain with a UID is tapped, it reads it and displays who is "signed in"

## Details: 
Tapping once is registered as signing in, and twice registers as signing out. When people scan, the date, time and their name will be displayed temporarily and then added to the signed in screen. When they sign out, their name will be removed. The details of the scan (UID, name, date, time, in/out, room number) are all written in a csv file named attendance_log.csv which is saved on the raspberry pi. 

## Accessing the raspberry pi: 
Plug into monitor, username: npmraspberry and password: pi \\
All information is stored in the environment called rfid-env and the folder RFID_rasbpi. The python script that is running is called id_logger. \\
The rasbpi is set to run this script infinitely and it automatically runs it in the case that it reboots. These commands can be accessed via command prompt **sudo nanmo /etc/systemd/system/rfid.service** \\ 
