import tkinter as tk
from snake_canvas import Snake
import traceback
import os
import sys
from os import path

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
os.chdir(bundle_dir)
try:
    root = tk.Tk()
    root.title('Snake')
    root.resizable(False, False)

    board = Snake(root)
    board.pack()

    root.mainloop()
except:
    traceback.print_exc()
    input("Press Enter to end...")
