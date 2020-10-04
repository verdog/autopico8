from Xlib import XK, display, ext, X, protocol

import time

DISPLAY = None
ROOT = None
WINDOW = None

def set_window(win):
    global WINDOW
    WINDOW = win

def ensure_ready():
    global DISPLAY
    global ROOT
    if not DISPLAY:
        print("Setting UI DISPLAY...")
        DISPLAY = display.Display()
    if not ROOT:
        print("Setting UI ROOT...")
        ROOT = DISPLAY.screen().root
    if not WINDOW:
        print("error in UI! no window!")

def press_key(key):
    ensure_ready()

    keysym = XK.string_to_keysym(key)
    keycode = DISPLAY.keysym_to_keycode(keysym)
    
    # print("pressin", key, keysym, keycode)

    event = protocol.event.KeyPress(
        time = int(time.time()),
        root = ROOT,
        window = WINDOW,
        same_screen = 0, child = X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = 0,
        detail = keycode
        )
    DISPLAY.send_event(WINDOW, event, propagate = True)
    DISPLAY.sync()

    # release_key(key)

def release_key(key):
    ensure_ready()

    keysym = XK.string_to_keysym(key)
    keycode = DISPLAY.keysym_to_keycode(keysym)

    event = protocol.event.KeyRelease(
        time = int(time.time()),
        root = ROOT,
        window = WINDOW,
        same_screen = 0, child = X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = 0,
        detail = keycode
        )
    DISPLAY.send_event(WINDOW, event, propagate = True)
    DISPLAY.sync()

