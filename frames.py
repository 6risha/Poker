import tkinter as tk
from PIL import Image, ImageTk
from cards import *
from tests import create_hand


class StartFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 24, 'bold')

        self.img = tk.PhotoImage(file='images/joker-hat.png')
        self.img = self.img.subsample(2)

        self.label_1 = tk.Label(self, image=self.img, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_1.pack(side=tk.TOP)

        self.label_2 = tk.Label(self, text='Start', font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_2.pack(side=tk.TOP)
        self.label_2.bind('<Enter>', lambda event, lbl=self.label_2: self.on_enter(lbl, event))
        self.label_2.bind('<Leave>', lambda event, lbl=self.label_2: self.on_leave(lbl, event))
        self.label_2.bind('<Button-1>', lambda event: self.open_next('Game', event))

        self.label_3 = tk.Label(self, text='Tutorials', font=self.small_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_3.pack(side=tk.TOP, pady=(100, 0))
        self.label_3.bind('<Enter>', lambda event, lbl=self.label_3: self.on_enter(lbl, event))
        self.label_3.bind('<Leave>', lambda event, lbl=self.label_3: self.on_leave(lbl, event))
        self.label_3.bind('<Button-1>', lambda event: self.open_next('Tutorials', event))

        self.label_4 = tk.Label(self, text='Analysis', font=self.small_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_4.pack(side=tk.TOP)
        self.label_4.bind('<Enter>', lambda event, lbl=self.label_4: self.on_enter(lbl, event))
        self.label_4.bind('<Leave>', lambda event, lbl=self.label_4: self.on_leave(lbl, event))
        self.label_4.bind('<Button-1>', lambda event: self.open_next('Analysis', event))

        self.label_5 = tk.Label(self, text='Settings', font=self.small_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_5.pack(side=tk.TOP)
        self.label_5.bind('<Enter>', lambda event, lbl=self.label_5: self.on_enter(lbl, event))
        self.label_5.bind('<Leave>', lambda event, lbl=self.label_5: self.on_leave(lbl, event))
        self.label_5.bind('<Button-1>', lambda event: self.open_next('Settings', event))

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def open_next(self, menu, event):
        self.pack_forget()
        if menu == 'Game':
            self.window.game_frame.pack(fill=tk.BOTH, expand=True)
        elif menu == 'Tutorials':
            self.window.tutorials_frame.pack(fill=tk.BOTH, expand=True)
        elif menu == 'Analysis':
            self.window.analysis_frame.pack(fill=tk.BOTH, expand=True)
        elif menu == 'Settings':
            self.window.settings_frame.pack(fill=tk.BOTH, expand=True)


class SettingsFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 24, 'bold')

        # Set blinds sizes
        self.blind_size = tk.DoubleVar()
        self.min_blind_size = 250
        self.max_blind_size = 1000
        self.scale1 = tk.Scale(self, orient='horizontal', from_=self.min_blind_size, to=self.max_blind_size, tickinterval=250, length=400, label='Small blind size', variable=self.blind_size, resolution=250, font=self.small_font)
        self.scale1.pack(pady=30, padx=10)

        # Set starting chips amount
        self.starting_chips = tk.DoubleVar()
        self.min_chips = 5000
        self.max_chips = 15000
        self.scale2 = tk.Scale(self, orient='horizontal', from_=self.min_chips, to=self.max_chips + 2000, tickinterval=5000, length=400, label='Starting chips', variable=self.starting_chips, resolution=5000, font=self.small_font)
        self.scale2.pack(pady=30, padx=10)

        # Blind increase
        self.blind_increase = tk.IntVar()
        self.blind_increase.set(0)
        self.scale3 = tk.Scale(self, orient='horizontal', from_=0, to=1, length=300, label='Blind increase', variable=self.blind_increase, tickinterval=1, font=self.small_font)
        self.scale3.pack(pady=30, padx=10)

        # Exit button
        self.label_1 = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label_1.pack()
        self.label_1.bind('<Enter>', lambda event, lbl=self.label_1: self.on_enter(lbl, event))
        self.label_1.bind('<Leave>', lambda event, lbl=self.label_1: self.on_leave(lbl, event))
        self.label_1.bind('<Button-1>', lambda event: self.exit(event))

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        self.pack_forget()
        self.window.start_frame.pack(fill=tk.BOTH, expand=True)


class GameFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.game = Game()
        self.game.community_cards = create_hand(['3♠', '7♦', '9♠', '10♣', 'Q♠'])
        self.game.user.hole_cards = create_hand(['9♦', '8♠'])

        self.table_color = 'forestgreen'
        self.red_card_color = 'firebrick2'
        self.black_card_color = 'gray8'
        self.bg_card_color = 'gray99'

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 24, 'bold')

        # Bot Frame
        self.bot_frame = tk.Frame(self)
        self.bot_chips_label = tk.Label(self.bot_frame, text=self.game.bot.chips, font=self.big_font)
        self.bot_role_label = tk.Label(self.bot_frame, text='SB' if self.game.players[self.game.sb_pos] == self.game.bot else 'BB', font=self.big_font)
        self.bot_chips_label.pack()
        self.bot_role_label.pack()
        self.bot_frame.pack(side=tk.TOP, fill=tk.X)

        # Community Cards Frame
        self.community_cards_frame = tk.Frame(self, bg=self.table_color)
        self.pot_label = tk.Label(self.community_cards_frame, text=self.game.pot, font=self.big_font, background=self.table_color)
        self.pot_label.pack()
        for card in self.game.community_cards:
            if card.suit == 1 or card.suit == 2:
                label = tk.Label(self.community_cards_frame, text=str(card), font=self.big_font, foreground=self.red_card_color, background=self.bg_card_color)
            else:
                label = tk.Label(self.community_cards_frame, text=str(card), font=self.big_font, foreground=self.black_card_color, background=self.bg_card_color)
            label.pack(side=tk.LEFT, padx=10)
        self.community_cards_frame.pack(side=tk.TOP)

        # User Frame
        self.user_frame = tk.Frame(self)
        self.user_chips_label = tk.Label(self.user_frame, text=self.game.user.chips, font=self.big_font)
        self.user_role_label = tk.Label(self.user_frame, text='SB' if self.game.players[self.game.sb_pos] == self.game.user else 'BB', font=self.big_font)
        self.user_hole_cards_frame = tk.Frame(self.user_frame)

        for card in self.game.user.hole_cards:
            if card.suit == 1 or card.suit == 2:
                label = tk.Label(self.user_hole_cards_frame, text=str(card), font=self.big_font, foreground=self.red_card_color, background=self.bg_card_color)
            else:
                label = tk.Label(self.user_hole_cards_frame, text=str(card), font=self.big_font, foreground=self.black_card_color, background=self.bg_card_color)
            label.pack(side=tk.LEFT, padx=10)

        self.button_fame = tk.Frame(self.user_frame)
        self.fold_button = tk.Button(self.button_fame, text="Fold", font=self.small_font)
        self.check_button = tk.Button(self.button_fame, text="Check", font=self.small_font)
        self.call_button = tk.Button(self.button_fame, text="Call", font=self.small_font)
        self.raise_button = tk.Button(self.button_fame, text="Raise", font=self.small_font)

        self.fold_button.pack(side=tk.LEFT, padx=10)
        self.check_button.pack(side=tk.LEFT, padx=10)
        self.call_button.pack(side=tk.LEFT, padx=10)
        self.raise_button.pack(side=tk.LEFT, padx=10)

        self.raise_slider = tk.Scale(self.user_frame, from_=0, to=self.game.user.chips, orient=tk.HORIZONTAL, font=self.small_font)

        self.user_hole_cards_frame.pack(side=tk.TOP)
        self.user_chips_label.pack(side=tk.TOP)
        self.user_role_label.pack(side=tk.TOP)
        self.button_fame.pack(side=tk.TOP)
        self.raise_slider.pack(side=tk.TOP)

        self.user_frame.pack(side=tk.TOP, fill=tk.X)



class TutorialsFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

    
    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        self.pack_forget()
        self.window.start_frame.pack(fill=tk.BOTH, expand=True)

class AnalysisFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
