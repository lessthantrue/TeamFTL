import pyautogui 
import os
import sys
import time

while True:
    x = int(sys.stdin.readline())
    y = int(sys.stdin.readline())
    r = sys.stdin.readline()
    # pyautogui.doubleClick(x, y)
    pyautogui.moveTo(x, y)
    time.sleep(0.01)
    if 't' in r:
        pyautogui.mouseDown(x, y, button='right')
        pyautogui.mouseUp(x, y, button='right')
    else:
        pyautogui.mouseDown(x, y)
        pyautogui.mouseUp(x, y)
    print("Mouse to " + str(x) + ", " + str(y))