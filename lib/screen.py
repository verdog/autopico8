import cv2
import numpy as np
from Xlib import display, X
from PIL import ImageGrab, Image

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
