#!/usr/bin/python3

import sys
sys.path.append("../../lib/")

import screen as Screen
import ui as Ui
import cv2
import numpy as np
import math

char_template = cv2.imread("./character.png")

def find_char(scr):
    match = cv2.matchTemplate(scr, char_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

    return math.floor(max_loc[0]*5/128) # quick and dirty...

w = Screen.find_pico8()
Ui.set_window(w)

if not w:
    print("Couldn't find pico-8. Is it open?")
    exit(-1)

while True:
    screen = Screen.filter(Screen.get_screen(w))

    current_slot = find_char(screen)
    cv2.circle(screen, (math.floor(current_slot*128/5 + 12), 90), 4, (255, 0, 255), 2)

    # cv2.imshow("screen", screen)
    cv2.imshow("viz", cv2.resize(screen, (512, 512), None, 0, 0, cv2.INTER_NEAREST))

    # 30 fps
    if cv2.waitKey(1000//30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
