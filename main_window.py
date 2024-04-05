import tkinter as tk
from frames import *


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Texas Holdem")
        self.geometry('1000x600')

        #self.icon = tk.PhotoImage(file='images/icon.png')
        #self.iconphoto(False, self.icon)

        self.bg_color = 'gray18'
        self.fg_color = 'white'
        self.accent_color = 'red'

        self.main_menu = StartFrame(self)
        self.main_menu.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
