import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Poker")
        
        self.label = tk.Label(self, text='Bonjour !')
        self.label.pack()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
