import tkinter as tk


class StartFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 25, 'bold')

        self.img = tk.PhotoImage(file='images/joker-hat.png')
        self.img = self.img.subsample(2)

        self.label_1 = tk.Label(self, image=self.img, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_1.pack(side=tk.TOP)

        self.label_2 = tk.Label(self, text='Start', font=self.big_font, bg=self.window.bg_color,
                                fg=self.window.fg_color)
        self.label_2.pack(side=tk.TOP)
        self.label_2.bind('<Enter>', lambda event, lbl=self.label_2: self.on_enter(lbl, event))
        self.label_2.bind('<Leave>', lambda event, lbl=self.label_2: self.on_leave(lbl, event))
        self.label_2.bind('<Button-1>', lambda event: self.start_game(event))

        self.label_3 = tk.Label(self, text='Settings', font=self.small_font, bg=self.window.bg_color,
                                fg=self.window.fg_color)
        self.label_3.pack(side=tk.BOTTOM, pady=(0, 50))
        self.label_3.bind('<Enter>', lambda event, lbl=self.label_3: self.on_enter(lbl, event))
        self.label_3.bind('<Leave>', lambda event, lbl=self.label_3: self.on_leave(lbl, event))
        self.label_3.bind('<Button-1>', lambda event: self.open_settings(event))

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def start_game(self, event):
        self.pack_forget()
        self.window.game_frame.pack()

    def open_settings(self, event):
        self.pack_forget()
        self.window.settings.pack(fill=tk.BOTH, expand=True)


class SettingsFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 25, 'bold')

        # Set blinds sizes
        self.blind_size = tk.DoubleVar()
        self.min_blind_size = 250
        self.max_blind_size = 1000
        self.scale1 = tk.Scale(self, orient='horizontal', from_=self.min_blind_size, to=self.max_blind_size,
                               tickinterval=250, length=400, label='Small blind size', variable=self.blind_size,
                               resolution=250, font=self.small_font)
        self.scale1.pack(pady=30, padx=10)

        # Set starting chips amount
        self.starting_chips = tk.DoubleVar()
        self.min_chips = 5000
        self.max_chips = 15000
        self.scale2 = tk.Scale(self, orient='horizontal', from_=self.min_chips, to=self.max_chips + 2000,
                               tickinterval=5000, length=400, label='Starting chips', variable=self.starting_chips,
                               resolution=5000, font=self.small_font)
        self.scale2.pack(pady=30, padx=10)

        # Blind increase
        self.blind_increase_speed = tk.IntVar()
        self.blind_increase_speed.set(0)
        self.scale3 = tk.Scale(self, orient='horizontal', from_=0, to=1, length=250, label='Blind increase',
                               variable=self.blind_increase_speed, tickinterval=1, font=self.small_font)
        self.scale3.pack(pady=30, padx=10)


class GameFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
