import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
import tkinter as tk
from src import MainWindow


def main():
    application = tk.Tk()
    application.withdraw()
    application.title("Word Cloud v.1.0")
    application.option_add("*tearOff", False)
    window = MainWindow.Window(application)
    application.protocol("WM_DELETE_WINDOW", window.close)
    application.deiconify()
    application.mainloop()

main()