__author__ = 'ejjeong'

import os
import sys
imagePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk

class PicWin2(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="light grey", width=320, height=320)
        
    def __init__(self, master):
        super().__init__(master, bg="light grey", width=320, height=320) #bg="white"
        filename = os.path.join(imagePath, "wclogo2.gif")
        if os.path.exists(filename):
            file_out = self.resizeLogo(filename)
            self.logo = tk.PhotoImage(file= os.path.abspath(imagePath) + '/' + file_out)
            self.create_image(int(self.winfo_reqwidth()/2), int(self.winfo_reqheight()/2), anchor='center', image=self.logo)

    def resizeLogo(self, filename):
        sizeW = int(self.winfo_reqwidth() / 2)
        sizeH = int(self.winfo_reqheight() / 2)
        orglogo = Image.open(filename)
        resized = orglogo.resize((int(sizeW), int(sizeH)), Image.ANTIALIAS)
        transparency = resized.info['transparency']
        file_out = '_resized.gif'
        resized.save(os.path.abspath(imagePath) + '/' + file_out, "GIF", transparency=transparency)
        print ("File saved as %s" %file_out)
        return file_out

