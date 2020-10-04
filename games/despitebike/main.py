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

def mid(a, b, c):
    return min(max(a,b),max(b,c),max(a,c))

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
    
    cv2.imshow("mask_" + str(color), mask)

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
    # find lane with longest forward path
    paths = [0, 0, 0, 0, 0]

    for i in range(5):
        count = 0
        layer = 0
        while layer < len(walls) and not walls[layer][i]:
            layer += 1
            count += 1
        paths[i] = count
    
    # block out lanes we can't get to
    # block out going right
    flag = False
    for i in range(current_slot, 5):
        if paths[i] == 0:
            flag = True
            # print("set flag right", i)
        if flag:
            paths[i] = 0
    
    flag = False
    for i in range(current_slot, -1, -1):
        if paths[i] == 0:
            flag = True
            # print("set flag left", i)
        if flag:
            paths[i] = 0

    # print(paths)

    # find desired lane
    longest = 0
    lane = 2
    for i in [2, 3, 4, 0, 1]:
        # ordering above to prefer middle
        if paths[i] > longest:
            lane = i
            longest = paths[i]
    
    # move
    if current_slot < lane:
        Ui.press_key("Right")
        Ui.release_key("Left")
    elif current_slot > lane:
        Ui.press_key("Left")
        Ui.release_key("Right")
    else:
        Ui.release_key("Left")
        Ui.release_key("Right")

    return lane

w = Screen.find_pico8()
Ui.set_window(w)

if not w:
    print("Couldn't find pico-8. Is it open?")
    exit(-1)

while True:
    framestart = time.time()

    screen = Screen.filter(Screen.get_screen(w))
    viz = screen.copy()

    current_slot = find_char(screen)

    # walls = find_walls(screen, Screen.COLOR_4, 72, 38)
    walls_0 = find_walls(screen, Screen.COLOR_F, 120, 20)
    walls_1 = find_walls(screen, Screen.COLOR_A, 100, 24)
    walls_2 = find_walls(screen, Screen.COLOR_9, 80, 30)
    walls_3 = find_walls(screen, Screen.COLOR_4, 76, 36)
    walls_4 = find_walls(screen, Screen.COLOR_5, 68, 40)
    # walls_5 = find_walls(screen, Screen.COLOR_1, 60, 46)

    lane = move(current_slot, [walls_0, walls_1, walls_2, walls_3, walls_4])

    # player
    cv2.circle(viz, (math.floor(current_slot*128/5 + 12), 90), 4, (255, 0, 255), 2)
    # lane
    cv2.circle(viz, (math.floor(lane*128/5 + 12), 110), 4, (0, 255, 255), 2)

    # cv2.imshow("screen", screen)
    cv2.imshow("viz", cv2.resize(viz, (512, 512), None, 0, 0, cv2.INTER_NEAREST))

    # 30 fps
    if cv2.waitKey(1000//120) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
