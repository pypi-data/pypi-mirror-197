with open("test.py", "r+") as file:
    data = [line.replace("\n", "") for line in file]

with open("test.py", "w+") as file:
    for each in data:
        if each not in ["import PIL.Image", "from pynput import keyboard", "from pynput.mouse import Listener", "import tkinter as tk", "import pyautogui as pg"]:
            file.write(f"{each}\n")


