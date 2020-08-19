import os
import time
import json
import keyboard
import mouse
import pyautogui
import websocket
import subprocess
import requests
import _thread as thread
import os
from io import BytesIO

# NOTE: shift + number keys work, shift + letter doesn't
# it acted this way with 2 different libraries, so it's probably FTL
keys = {
    # engineering
    "enup": "s", "endn": "8",
    "shup": "a", "shdn": "`",
    "oxup": "f", "oxdn": "9",
    "mdup": "d", "mddn": "0",
    "arup": "y", "ardn": "\\",
    "clup": "h", "cldn": "=",
    "mcup": "k", "mcdn": "[",
    "hkup": "l", "hkdn": "]",
    "tpup": "g", "tpdn": "-",
    # tactical
    "dr1up": "5", "dr1dn": "shift+5",
    "dr2up": "6", "dr2dn": "shift+6",
    "dr3up": "7", "dr3dn": "shift+7",
    "hack": "n",
    "cloak": "c",
    "mindcontrol": "m",
    # weapons3
    "wep1up" : "1", "wep1dn": "shift+1",
    "wep2up" : "2", "wep2dn": "shift+2",
    "wep3up" : "3", "wep3dn": "shift+3",
    "wep4up" : "4", "wep4dn": "shift+4",
    # personnel
    "rtstat" : "enter", "ss": ".",
    "c1": "f1", "c2": "f2", "c3": "f3", "c4": "f4",
    "c5": "f5", "c6": "f6", "c7": "f7", "c8": "f8",
    "tpsend": "t", "tprt": "r", "claldr": "x",
}

wepOffset = (0, 0)
clickDelay = 0.1 # seconds between move mouse and click events
imgDelay = 1.6 # seconds to delay between sending images

url = "157.245.13.249"

def clickWith(posX, posY, key, right=False):
    # keyboard.send('esc')
    keyboard.send(key)
    time.sleep(clickDelay)
    mouse.move(posX, posY)
    time.sleep(clickDelay)
    if right:
        mouse.right_click()
    else:
        mouse.click()

def decodeAction(jsobj):
    for cmd in jsobj:
        # filter out bad packets
        if not ("type" in cmd):
            print("Got bad command: " + cmd)
            continue

        if cmd["type"] == "engineering":
            print("Got engineering packet: " + str(cmd))
            cmd_code = cmd["command"]
            keyboard.send(keys[cmd_code])
        elif cmd["type"] == "weapons":
            print("Got weapons packet: " + str(cmd))
            if cmd["command"] == "fire":
                cmd_code = cmd["active"]
                clickWith(float(cmd["posX"]), float(cmd["posY"]), keys[cmd_code])
            elif cmd["command"] == "beamfire":
                cmd_code = cmd["active"]
                clickWith(float(cmd["posX"]), float(cmd["posY"]), keys[cmd_code])
                time.sleep(clickDelay)
                mouse.move(float(cmd["posX1"]), float(cmd["posY1"]))
                time.sleep(clickDelay)
                mouse.click()
            else:
                cmd_code = cmd["command"]
                keyboard.send(keys[cmd_code])
        elif cmd["type"] == "tactical":
            print("Got tactical packet: " + str(cmd))
            cmd_code = cmd["command"]
            if cmd_code == "click":
                clickWith(float(cmd["posX"]), float(cmd["posY"]), keys[cmd["active"]])
            else:
                keyboard.send(keys[cmd_code])
        elif cmd["type"] == "personnel":
            print("Got personnel packet: " + str(cmd))
            cmd_code = cmd["command"]
            if cmd_code == "click":
                clickWith(float(cmd["posX"]), float(cmd["posY"]), keys[cmd["active"]], right=("c" in cmd["active"]))
            elif cmd_code in ["rtstat", "ss", "claldr"]:
                keyboard.send(keys[cmd_code])
        else:
            print("Got unknown packet type: " + cmd["type"])

    # clean up current selected action
    mouse.right_click()
    mouse.click()
        
def on_message(conn, msg):
    obj = json.loads(msg)
    decodeAction(obj)

def sendImg(img_obj):
    img_url = 'http://' + url + ':2999/image'
    path_img = "screenshot_full.png"

    bio = BytesIO()
    img_obj.save(bio, 'png')
    bio.seek(0)

    # with open(path_img, 'rb') as img:
    name_img = os.path.basename(path_img)
    files = {'image': (name_img, bio, 'multipart/form-data', {'Expires': '0'}) }
    try:
        r = requests.post(img_url, files=files, timeout=2)
        if r.status_code != 200:
            print("Screenshot upload status: " + str(r.status_code))
    except Exception as e:
        print("Upload failed completely: " + str(e))

def on_startup(ws):
    print("Starting Up")
    def img_loop(*args):
        while True:
            img = pyautogui.screenshot("screenshot_full.png")
            time.sleep(imgDelay / 2)
            sendImg(img)
            time.sleep(imgDelay / 2)
    thread.start_new_thread(img_loop, ())

    # poke server
    ws.send("CMD_REQUEST")

def on_close(ws):
    print("Websocket dead")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://" + url + ":8080", on_message=on_message, on_close=on_close)
    ws.on_open = on_startup
    while(True):
        print("waiting for socket to open")
        ws.run_forever()
        time.sleep(5)