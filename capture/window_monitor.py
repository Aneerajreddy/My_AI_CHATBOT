
import pygetwindow as gw

def get_active_window_title():
    window = gw.getActiveWindow()
    if window:
        return window.title
    else:
        return "Unknown Window"
