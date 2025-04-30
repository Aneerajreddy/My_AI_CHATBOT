
import pyperclip

def get_clipboard_text():
    try:
        return pyperclip.paste()
    except:
        return ""
