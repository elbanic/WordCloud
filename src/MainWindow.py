import tkinter as tk
import tkinter.ttk as ttk

from src import NLP, TextWin, PicWin


class Window(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=5)
        self.createVar()
        self.createUI()
        self.createLayout()
        self.pack()
        #self.create_variables()
        #self.create_images()

    def createVar(self):
        self.nlp = NLP.NLP()
        self.textWin = TextWin.TextWin(self, width=60, height=20)
        self.picWin = PicWin.PicWin(self)
        self.makeWCloudButton = ttk.Button(self, text="Get Word Cloud", command=self.getTextData)
        self.saveImageButton = ttk.Button(self, text="Save Image")
        self.helpButton = ttk.Button(self, text="Help")
        self.closeButton = ttk.Button(self, text="close", command=self.master.destroy)
        self.clearBtn = ttk.Button(self, text="Clear", command=self.clearData)

    def createUI(self):
        self.create_textWin()
        self.create_picWin()
        self.master.resizable(False, False)
        #self.master.minsize(650, 320)
        #self.master.maxsize(650, 320)

    def create_textWin(self):
        strData = """A tag cloud (word cloud, or weighted list in visual design) is a visual representation of text data, typically used to depict keyword metadata (tags) on websites, or to visualize free form text. Tags are usually single words, and the importance of each tag is shown with font size or color.[2] This format is useful for quickly perceiving the most prominent terms and for locating a term alphabetically to determine its relative prominence. When used as website navigation aids, the terms are hyperlinked to items associated with the tag."""
        self.textWin.text.insert(tk.END, strData)
        self.textWin.focus_set()

    def create_picWin(self):
        return

    def createLayout(self):
        self.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.picWin.grid(row =0, column =1, columnspan=2)
        self.textWin.grid(row =1, column =1, rowspan=12)
        self.makeWCloudButton.grid(row =1, column =2, sticky=tk.N+ tk.S+ tk.E+ tk.W)
        self.saveImageButton.grid(row =3, column =2, sticky=tk.N+ tk.S+ tk.E+ tk.W)
        self.helpButton.grid(row =9, column =2, sticky=tk.N+ tk.S+ tk.E+ tk.W)
        self.closeButton.grid(row =11, column =2, sticky=tk.N+ tk.S+ tk.E+ tk.W)
        self.clearBtn.grid(row=5, column=2, sticky=tk.N+ tk.S+ tk.E+ tk.W)

    def getTextData(self):
        data = self.nlp.generateWCData(self.textWin.text.get("1.0", tk.END))
        #self.picWin.drawWordCloud(data)
        #self.textWin.text.delete("0.0", tk.END)
        #self.textWin.text.insert(tk.END, data.items())
        self.picWin.drawWordCloud(data)

    def clearData(self):
        self.textWin.text.delete("0.0", tk.END)
        self.picWin.delete("all")

    def close(self, event=None):
        self.quit()
