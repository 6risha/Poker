import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Poker")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
