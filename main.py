import cv2
import numpy as np
import pyautogui
# from draw_in_air import draw_in_air
from HandTrackingModule import main
from AiVirtualMouseProject import AiVirtualMouseProject
from AI_VIRTUAL_PAINTER import AI_VIRTUAL_PAINTER
import tkinter as tk
from PIL import ImageTk, Image
import webbrowser

def callback(url):
    webbrowser.open_new(url)

def manual():
    AI_VIRTUAL_PAINTER()
    # control_mouse("manual")
    # control_mouse("AiVirtualMouseProject")

def automatic():
    main()

root = tk.Tk()

root.geometry("500x500")

image = ImageTk.PhotoImage(Image.open("tap.png"))
img_label = tk.Label(image=image)
img_label.grid(row=0, columnspan=2, pady=10)

label = tk.Label(root, text="Welcome to AI Virtual Paint", font='system 18 bold')
label.grid(row=1, columnspan=2, pady=5)

button = tk.Button(root, text="AIHTM ",fg="green", font='TkDefaultFont 12 bold', command=automatic, height="4")
button.grid(row=2, column=0, pady=20, padx=10)


button = tk.Button(root,text="AIVM",fg="green", font='TkDefaultFontTkDefaultFont 12 bold', command=manual, height="4")
button.grid(row=2, column=1, pady=20)

button = tk.Button(root,text="AIVMP",fg="green", font='TkDefaultFont 12 bold', command=AiVirtualMouseProject, height="4", width="16")
button.grid(row=3, column=0, pady=20)

button = tk.Button(root,text="Close",fg="red", font='TkDefaultFont 12 bold', command=root.quit, height="4", width="16")
button.grid(row=3, column=1, pady=20)

link1 = tk.Label(root, text="How to use?", fg="blue", cursor="hand2", font='TkDefaultFont 12 bold')
link1.grid(row=4, columnspan=2)
link1.bind("<Button-1>", lambda e: callback("about.html"))

root.mainloop()


