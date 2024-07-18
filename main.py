import cv2
import numpy as np
import pyautogui
import mss
import keyboard

template_paths = [
    "match_1.png",
    "match_2.png",
    "match_3.png",
    "match_4.png"
]
monitor = {"top": 323, "left": 267, "width": 1327, "height": 598}

templates = []
template_dimensions = []
for path in template_paths:
    template_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if template_img is not None:
        templates.append(template_img)
        h, w = template_img.shape[:2]
        template_dimensions.append((w, h))

threshold = 0.5

def perform_template_matching(sct):
    input_img = np.array(sct.grab(monitor))

    for i, (template_img, (w, h)) in enumerate(zip(templates, template_dimensions)):
        result = cv2.matchTemplate(input_img, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(max_val)
        if max_val > threshold:
            x, y = max_loc
            center_x = monitor['left'] + x + int(w / 2)
            center_y = monitor['top'] + y + int(h / 2)
            pyautogui.moveTo(center_x, center_y)
            if i == 0:
                pyautogui.doubleClick()
            else:
                pyautogui.click()
            break

def main():
    print("Press 'e' to start")
    keyboard.wait('e')
    print("Press 'q' to quit.")

    sct = mss.mss()
    while True:
        perform_template_matching(sct)
        if keyboard.is_pressed('q'):
            break

if __name__ == '__main__':
    main()