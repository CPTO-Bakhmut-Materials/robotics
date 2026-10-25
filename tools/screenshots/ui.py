"""Drive the Webots window on Hyprland (hyprctl + ydotool) and capture it with grim.

Usage (from the repo root):
    python3 tools/screenshots/ui.py shot NAME          # capture Webots window -> raw/NAME.png
    python3 tools/screenshots/ui.py move X Y           # hover at window-relative X, Y
    python3 tools/screenshots/ui.py click X Y [right]  # click at window-relative X, Y
    python3 tools/screenshots/ui.py drag X1 Y1 X2 Y2   # drag with the left button (e.g. dock splitters)
    python3 tools/screenshots/ui.py key ctrl+shift+s   # press a key combination
    python3 tools/screenshots/ui.py pkey down right    # keys inside an open menu (no refocus)
    python3 tools/screenshots/ui.py type "text"        # type text
    python3 tools/screenshots/ui.py relayout           # fix a garbled Webots layout
    python3 tools/screenshots/ui.py back               # return to the previous workspace

Every command first switches to the workspace that holds Webots and focuses it.
Needs a running ydotoold (systemctl --user start ydotool).
"""
import json
import pathlib
import subprocess
import sys
import time

RAW = pathlib.Path(__file__).parent / "raw"

KEYS = {
    "ctrl": 29, "shift": 42, "alt": 56, "super": 125, "enter": 28, "esc": 1, "tab": 15,
    "backspace": 14, "delete": 111, "space": 57, "up": 103, "down": 108, "left": 105, "right": 106,
    "home": 102, "end": 107, "pageup": 104, "pagedown": 109,
    "f1": 59, "f2": 60, "f3": 61, "f4": 62, "f5": 63, "f6": 64, "f7": 65, "f8": 66, "f9": 67, "f10": 68,
    "0": 11, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10,
}
KEYS.update({c: code for c, code in zip("qwertyuiop", range(16, 26))})
KEYS.update({c: code for c, code in zip("asdfghjkl", range(30, 39))})
KEYS.update({c: code for c, code in zip("zxcvbnm", range(44, 51))})


def hypr(*args):
    return subprocess.run(["hyprctl", *args], check=True, capture_output=True, text=True).stdout


def webots():
    for c in json.loads(hypr("clients", "-j")):
        if c["class"] == "Webots" and " - Webots" in c["title"]:
            return c
    sys.exit("Webots window not found")


def focus():
    # Refocusing while a Qt popup menu is open makes Webots re-layout at the popup size
    # (XWayland), so only switch when Webots is not already the active window.
    w = webots()
    if json.loads(hypr("activewindow", "-j")).get("address") != w["address"]:
        hypr("dispatch", "workspace", str(w["workspace"]["id"]))
        hypr("dispatch", "focuswindow", "address:" + w["address"])
        time.sleep(0.4)
    return w


def ydo(*args):
    subprocess.run(["ydotool", *args], check=True, capture_output=True)


def pointer(x, y):
    # Real (absolute) pointer motion. Never use `hyprctl dispatch movecursor`: warping while
    # a Qt popup (menu, tooltip) is open makes Webots re-layout at the popup size on XWayland.
    ydo("mousemove", "--absolute", "-x", str(int(x)), "-y", str(int(y)))


def move(x, y):
    w = focus()
    pointer(w["at"][0] + int(x), w["at"][1] + int(y))
    time.sleep(0.4)


def click(x, y, button="left"):
    move(x, y)
    ydo("click", {"left": "0xC0", "right": "0xC1"}[button])
    time.sleep(0.4)


def drag(x1, y1, x2, y2):
    horizontal = abs(int(x2) - int(x1)) >= abs(int(y2) - int(y1))
    move(int(x1) - 3 * horizontal, int(y1) - 3 * (not horizontal))
    for _ in range(3):  # real motion onto the target so Qt picks up the hover (e.g. splitter cursor)
        ydo("mousemove", "-x", str(int(horizontal)), "-y", str(int(not horizontal)))
        time.sleep(0.05)
    time.sleep(0.2)
    ydo("click", "0x40")  # left button down
    time.sleep(0.2)
    # Qt only sees real pointer motion during a drag, so move relatively in small steps
    dx, dy = int(x2) - int(x1), int(y2) - int(y1)
    steps = 10
    for i in range(steps):
        ydo("mousemove", "-x", str(dx // steps), "-y", str(dy // steps))
        time.sleep(0.03)
    time.sleep(0.2)
    ydo("click", "0x80")  # left button up
    time.sleep(0.5)


def key(combo, refocus=True):
    if refocus:
        focus()
    codes = [KEYS[k] for k in combo.lower().split("+")]
    ydo("key", *[f"{c}:1" for c in codes], *[f"{c}:0" for c in reversed(codes)])
    time.sleep(0.4)


def type_text(text):
    focus()
    ydo("type", "--key-delay", "15", text)
    time.sleep(0.3)


def relayout():
    # Recover from a stale/garbled Webots layout: float, resize, re-tile
    focus()
    hypr("dispatch", "togglefloating")
    time.sleep(0.5)
    hypr("dispatch", "resizeactive", "exact", "1600", "900")
    time.sleep(1)
    hypr("dispatch", "togglefloating")
    time.sleep(1.5)


def shot(name, park=True):
    # park=False keeps the pointer where it is (e.g. hovering a menu item)
    w = webots() if not park else focus()
    if park:
        pointer(w["at"][0] + w["size"][0] - 5, w["at"][1] + w["size"][1] - 5)
        time.sleep(0.3)
    RAW.mkdir(exist_ok=True)
    out = RAW / f"{name}.png"
    geometry = f"{w['at'][0]},{w['at'][1]} {w['size'][0]}x{w['size'][1]}"
    subprocess.run(["grim", "-g", geometry, str(out)], check=True)
    print(out)


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    if cmd == "shot":
        shot(rest[0])
    elif cmd == "pshot":  # capture with a menu open: no refocus, cursor stays put
        shot(rest[0], park=False)
    elif cmd == "move":
        move(*rest)
    elif cmd == "click":
        click(*rest)
    elif cmd == "drag":
        drag(*rest)
    elif cmd == "key":
        key(rest[0])
    elif cmd == "pkey":  # inside an open popup menu: no refocus, no cursor moves
        for combo in rest:
            key(combo, refocus=False)
    elif cmd == "type":
        type_text(rest[0])
    elif cmd == "relayout":
        relayout()
    elif cmd == "back":
        hypr("dispatch", "workspace", "previous")
    else:
        sys.exit(__doc__)
