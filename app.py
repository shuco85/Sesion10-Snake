import tkinter as tk
from snake_canvas import Snake

root = tk.Tk()
root.title('Snake')
root.resizable(False, False)

board = Snake(root)
board.pack()


root.mainloop()
