import tkinter as tk
import tkinter.ttk as ttk

class TextWin(ttk.Frame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.frame = self
        self.text = tk.Text(self, **kwargs)
        #self.xscrollbar = tk.Scrollbar(self, command=self.text.xview, orient=tk.HORIZONTAL)
        self.yscrollbar = tk.Scrollbar(self, command=self.text.yview, orient=tk.VERTICAL, bg="red")
        #self.text.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)
        self.text.configure(yscrollcommand=self.yscrollbar.set)
        #self.xscrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.yscrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)