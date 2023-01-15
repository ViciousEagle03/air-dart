from tkinter import *
import time
import os
import cv2
import mediapipe as mp
# import tkinter import filedialog
import random
from cvzone.HandTrackingModule import HandDetector as htm

from tkinter import ttk
import pyttsx3
import cvzone
from PIL import ImageTk
from PIL import Image
import cv2
import numpy as np
from hdpitkinter import *
import maingame_mechanics_func as ic




def instruc():
    bgimg4 = np.array(Image.open(r"INSTRUC 6.png"))
    bgimg4= cv2.resize(bgimg4, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    bgimg4 = ImageTk.PhotoImage(Image.fromarray(bgimg4))
    img_label = Label(root, image=bgimg4)
    img_label.place(x=0, y=0, relheight=1, relwidth=1)

    bgimg2 = np.array(Image.open(r"PLAY13.png"))
    bgimg2 = cv2.resize(bgimg2, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    bgimg2 = ImageTk.PhotoImage(Image.fromarray(bgimg2))
    button = Button(root, image= bgimg2, command= ic.main_game , relief="flat", bg="white")
    button.place(x=970, y=570)
    root.mainloop()
'''
def mainloop():
    my_program = filedialog.askopenfilename()
    #my_label.config(text=my_program)
    os.system('"%s "' & my_program)

'''

sf2=1
root = Tk()
root.title("Air Dart")
root.geometry("1280x720")
bgimg = np.array(Image.open(r"desk7.png"))
bgimg = cv2.resize(bgimg, None, fx=sf2, fy=sf2, interpolation=cv2.INTER_AREA)
bgimg = ImageTk.PhotoImage(Image.fromarray(bgimg))
img_label = Label(root, image=bgimg)
img_label.place(x=0, y=0, relheight=1, relwidth=1)

#photo1 = PhotoImage(file="darticon.png")
#root.iconphoto(False, photo1)

# import image for package styling

bgimg2 = np.array(Image.open(r"begin14.png"))
bgimg2 = cv2.resize(bgimg2, None, fx=1, fy =1, interpolation=cv2.INTER_AREA)
bgimg2 = ImageTk.PhotoImage(Image.fromarray(bgimg2))

bgimg3 = np.array(Image.open(r"exit11.png"))
bgimg3 = cv2.resize(bgimg3, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
bgimg3 = ImageTk.PhotoImage(Image.fromarray(bgimg3))

button1 = Button(root, image=bgimg2, command=instruc, relief="flat", )
button1.place(x=912, y=476)
button2 = Button(root, image=bgimg3, command=root.quit, relief="flat", )
button2.place(x=912, y=590)
root.mainloop()

#######################


##############




root.mainloop()



