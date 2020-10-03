from Xlib.display import Display
import Xlib
from Xlib import X
import Xlib.XK

import time

display = None
root = None
window = None

def set_window(win):
    global window
    window = win

def ensure_ready():
    global display
    global root
    if not display:
        display = Display()
    if not root:
        root = display.screen().root
    if not window:
        print("error in UI! no window!")

def press_key(key):
    ensure_ready()

    shift_mask = 0 # or Xlib.X.ShiftMask
    keysym = Xlib.XK.string_to_keysym(key)
    keycode = display.keysym_to_keycode(keysym)

    event = Xlib.protocol.event.KeyPress(
        time = 0,
        root = root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        detail = keycode
        )
    window.send_event(event, propagate = True)

    event = Xlib.protocol.event.KeyRelease(
        time = 0,
        root = root,
        window = window,
        same_screen = 0, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        detail = keycode
        )
    window.send_event(event, propagate = True)
