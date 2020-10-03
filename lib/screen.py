import cv2
import numpy as np
from Xlib import display, X
from PIL import ImageGrab, Image

# these are in BGR format
COLOR_0 = (0, 0, 0)
COLOR_1 = (83, 43, 29)
COLOR_2 = (83, 37, 126)
COLOR_3 = (81, 135, 0)
COLOR_4 = (54, 82, 171)
COLOR_5 = (79, 87, 95)
COLOR_6 = (199, 195, 194)
COLOR_7 = (232, 241, 255)
COLOR_8 = (77, 0, 255)
COLOR_9 = (0, 163, 255)
COLOR_A = (39, 236, 255)
COLOR_B = (54, 228, 0)
COLOR_C = (255, 173, 41)
COLOR_D = (156, 118, 131)
COLOR_E = (168, 119, 255)
COLOR_F = (170, 204, 255)

# find the pico8 x window
def find_pico8():
    print("Trying to find pico8...")
    dsp = display.Display()
    q = []
    q.append(dsp.screen().root)

    while len(q) != 0:
        tree = q.pop(0)
        for node in tree.query_tree().children:
            name = node.get_wm_name()
            if name and "PICO-8" in name:
                print(f"Found it: {node.id}")
                return node
            q.append(node)
    
    print("Couldn't find it...")
    return None

# return a cv2 image of the screen of a given window
def get_screen(window):
    geo = window.get_geometry()
    w = geo.width
    h = geo.height
    raw = window.get_image(0, 0, w, h, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (w, h), raw.data, "raw", "BGRX")
    array = np.array(image)
    return cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

# reduce image to one more easily processable
def filter(image):
    w = image.shape[1]
    h = image.shape[0]

    smallest = min(w, h)
    scale = smallest//128

    sidesize = scale * 128

    x = (w - sidesize) // 2
    y = (h - sidesize) // 2

    cropped = image[y:y+sidesize, x:x+sidesize]
    return cv2.resize(cropped, (128, 128), None, 0, 0, cv2.INTER_NEAREST)
