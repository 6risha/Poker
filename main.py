import tkinter as tk
from frames import *


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Texas Holdem')
        self.geometry('1920x1080')

        self.icon = tk.PhotoImage(file='images/icon.png')
        self.iconphoto(False, self.icon)

        self.bg_color = 'gray18'
        self.fg_color = 'white'
        self.accent_color = 'red'

        self.start_frame = StartFrame(self)
        self.start_frame.pack(fill=tk.BOTH, expand=True)

        self.tutorials_frame = TutorialsFrame(self)
        self.settings_frame = SettingsFrame(self)
        self.game_frame = None
        self.analysis_frame = AnalysisFrame(self)
        self.tutorials1 = Tutorial1(self)
        self.tutorials2 = Tutorial2(self)
        self.tutorials3 = Tutorial3(self)
        self.tutorials4 = Tutorial4(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
