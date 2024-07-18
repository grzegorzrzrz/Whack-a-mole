import cv2
import numpy as np
import pyautogui
import mss
import keyboard

template_paths = [
    "match_1.png",
    "match_2.png",
    "match_3.png"
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

threshold = 0.6

def perform_template_matching(sct):

    input_img = np.array(sct.grab(monitor))

    results = []

    for template_img in templates:
        result = cv2.matchTemplate(input_img, template_img, cv2.TM_CCOEFF_NORMED)
        results.append(result)

    matches = []

    for result, (w, h) in zip(results, template_dimensions):
        yloc, xloc = np.where(result >= threshold)
        for (x, y) in zip(xloc, yloc):
            matches.append([x, y, w, h])

    matches, weights = cv2.groupRectangles(matches, groupThreshold=1, eps=0.2)

    for (x, y, w, h) in matches:
        center_x = x + monitor['left'] + int(w / 2)
        center_y = y + monitor['top'] + int(h / 2)

        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()

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
