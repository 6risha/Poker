import tkinter as tk
from frames import *


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Texas Holdem')
        self.geometry('1000x600')

        self.icon = tk.PhotoImage(file='images/icon.png')
        self.iconphoto(False, self.icon)

        self.bg_color = 'gray18'
        self.fg_color = 'white'
        self.accent_color = 'red'

        self.start_frame = StartFrame(self)
        self.start_frame.pack(fill=tk.BOTH, expand=True)

        self.settings_frame = SettingsFrame(self)
        self.game_frame = GameFrame(self)
        self.tutorials_frame = TutorialsFrame(self)
        self.analysis_frame = AnalysisFrame(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
