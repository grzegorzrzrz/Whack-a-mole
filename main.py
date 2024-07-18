import cv2
import numpy as np
import pyautogui
import mss
import keyboard
import threading
import time

template_paths = [
    "match_1.png",
    "match_2.png",
    "match_3.png",
    "match_4.png"
]
monitor = {"top": 240, "left": 410, "width": 1140, "height": 580}

templates = []
template_dimensions = []
for path in template_paths:
    template_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if template_img is not None:
        templates.append(template_img)
        h, w = template_img.shape[:2]
        template_dimensions.append((w, h))

threshold = 0.6

lock = threading.Lock()

def perform_template_matching(sct):
    input_img = np.array(sct.grab(monitor))

    threads = []
    for template_img, (w, h) in zip(templates, template_dimensions):
        thread = threading.Thread(target=match_and_click, args=(input_img, template_img, w, h))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def match_and_click(input_img, template_img, w, h):
    result = cv2.matchTemplate(input_img, template_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > threshold:
        x, y = max_loc
        center_x = monitor['left'] + x + int(w / 2)
        center_y = monitor['top'] + y + int(h / 2)
        pyautogui.click(center_x, center_y)
        pyautogui.click(center_x, center_y)

def main():
    print("Press 'e' to start")
    keyboard.wait('e')
    print("Press 'q' to quit.")

    sct = mss.mss()

    while True:
        start_time = time.time()
        perform_template_matching(sct)

        if keyboard.is_pressed('q'):
            break

        elapsed_time = time.time() - start_time
        if elapsed_time < 0.2:
            time.sleep(0.2 - elapsed_time)

if __name__ == '__main__':
    main()
