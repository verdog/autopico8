#!/usr/bin/python3

import sys
sys.path.append("../../lib/")

import screen as Screen
import ui as Ui
import cv2
import numpy as np
import math

char_template = cv2.imread("./character.png")
viz = None

def find_char(scr):
    match = cv2.matchTemplate(scr, char_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

    return math.floor(max_loc[0]*5/128) # quick and dirty...

def find_walls(scr, color, width, height):
    global viz
    
    blurshape = (3, 9)
    mask = cv2.inRange(scr, color, color)
    mask = cv2.blur(mask, blurshape)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    results = [False, False, False, False, False]

    # scan line
    cv2.line(viz, (64 - width//2, height), (64 + width//2, height), (255, 0, 255), 1)
    
    cv2.imshow("mask", mask)

    x = 64 - width//2
    while x < 64 + width//2:
        if mask[height][x] == 255:
            idx = (x - (64 - width//2))/width*5
            results[math.floor(idx)] = True
        x += 1

    # results
    x = 0
    for r in results:
        if r:
            xx = math.floor(64-width//2 + x/5 * width) + 8
            cv2.line(viz, (xx, height-4), (xx, height+4), (255, 255, 0), 1)
        x += 1

    return results

def move(current_slot, walls):
    if walls[current_slot]:
        print("Danger!")
    else:
        # try to go to middle
        if current_slot < 2:
            Ui.press_key("Right")
        elif current_slot > 2:
            Ui.press_key("Left")

w = Screen.find_pico8()
Ui.set_window(w)

if not w:
    print("Couldn't find pico-8. Is it open?")
    exit(-1)

while True:
    screen = Screen.filter(Screen.get_screen(w))
    viz = screen.copy()

    current_slot = find_char(screen)

    # walls = find_walls(screen, Screen.COLOR_4, 72, 38)
    walls = find_walls(screen, Screen.COLOR_A, 100, 24)
    # walls = find_walls(screen, Screen.COLOR_F, 120, 20)

    cv2.circle(viz, (math.floor(current_slot*128/5 + 12), 90), 4, (255, 0, 255), 2)
    # cv2.imshow("screen", screen)
    cv2.imshow("viz", cv2.resize(viz, (512, 512), None, 0, 0, cv2.INTER_NEAREST))

    move(current_slot, walls)

    # 30 fps
    if cv2.waitKey(1000//30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
