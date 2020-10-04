#!/usr/bin/python3

import sys
sys.path.append("../../lib/")

import screen as Screen
import ui as Ui
import cv2
import numpy as np
import math
import time

char_template = cv2.imread("./character.png")
viz = None

w = Screen.find_pico8()
Ui.set_window(w)

if not w:
    print("Couldn't find pico-8. Is it open?")
    exit(-1)

while True:
    frame_start = time.time()
    Ui.press_key("Left")
    time.sleep(1/30 - (time.time() - frame_start))
    
    frame_start = time.time()
    Ui.release_key("Left")
    time.sleep(1/30 - (time.time() - frame_start))
