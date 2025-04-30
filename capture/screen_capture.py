
import mss

def capture_screen(save_path):
    with mss.mss() as sct:
        sct.shot(output=save_path)
