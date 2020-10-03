#!/usr/bin/python3

import screen as Screen
import cv2

w = Screen.find_pico8()

if not w:
    print("Couldn't find pico-8. Is it open?")
    exit(-1)

while True:
    screen = Screen.filter(Screen.get_screen(w))
    viz = screen.copy()

    cv2.imshow("screen", screen)
    cv2.imshow("viz", cv2.resize(viz, (512, 512), None, 0, 0, cv2.INTER_NEAREST))

    # 30 fps
    if cv2.waitKey(1000//30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
