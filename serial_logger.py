#!/usr/bin/env python
# Log data from serial port

# Author: Diego Herranz

import argparse
import serial
import datetime
import time
import os

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--device",  help="device to read from",  default="/dev/ttyUSB0")
parser.add_argument("-s", "--speed",   help="speed in bps",         default=9600, type=int)
parser.add_argument("-c", "--console", help="show only on console", action="store_true", dest="c")

args = parser.parse_args()

if (not args.c):
    outputFilePath = os.path.join(os.path.dirname(__file__),
                 datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S") + ".bin")
    outputFile = open(outputFilePath, mode='wb')
    print("will log to " + outputFilePath)
else:
    print("will log only to console")

try:
    ser = serial.Serial(args.device, args.speed)
except:
    print("Could not open serial line")
    exit()

print("Logging started. Ctrl-C to stop.") 
try:
    while True:
        if (args.c):
            character = str(ser.read(1), encoding='utf-8')
            print(character, end="", flush=True)
        else:
            time.sleep(1)
            outputFile.write((ser.read(ser.inWaiting())))
            outputFile.flush()

except KeyboardInterrupt:
    print("Logging stopped")
    if (not args.c):
        outputFile.close()
