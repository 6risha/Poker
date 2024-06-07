import os
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
from cards import *
from analysis.analysis import *


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

        self.label_2 = tk.Label(self, text='Start', font=self.big_font, bg=self.window.bg_color,
                                fg=self.window.fg_color)
        self.label_2.pack(side=tk.TOP)
        self.label_2.bind('<Enter>', lambda event, lbl=self.label_2: self.on_enter(lbl, event))
        self.label_2.bind('<Leave>', lambda event, lbl=self.label_2: self.on_leave(lbl, event))
        self.label_2.bind('<Button-1>', lambda event: self.open_next('Game', event))

        self.label_3 = tk.Label(self, text='Tutorials', font=self.small_font, bg=self.window.bg_color,
                                fg=self.window.fg_color)
        self.label_3.pack(side=tk.TOP, pady=(100, 0))
        self.label_3.bind('<Enter>', lambda event, lbl=self.label_3: self.on_enter(lbl, event))
        self.label_3.bind('<Leave>', lambda event, lbl=self.label_3: self.on_leave(lbl, event))
        self.label_3.bind('<Button-1>', lambda event: self.open_next('Tutorials', event))

        self.label_4 = tk.Label(self, text='Analysis', font=self.small_font, bg=self.window.bg_color,
                                fg=self.window.fg_color)
        self.label_4.pack(side=tk.TOP)
        self.label_4.bind('<Enter>', lambda event, lbl=self.label_4: self.on_enter(lbl, event))
        self.label_4.bind('<Leave>', lambda event, lbl=self.label_4: self.on_leave(lbl, event))
        self.label_4.bind('<Button-1>', lambda event: self.open_next('Analysis', event))

        self.label_5 = tk.Label(self, text='Settings', font=self.small_font, bg=self.window.bg_color,
                                fg=self.window.fg_color)
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
            self.window.game_frame = GameFrame(self.window)
            self.window.game_frame.pack(fill=tk.BOTH, expand=True)
            self.window.game_frame.game.play()
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

        self.settings = {
            'blind_size': 250,
            'starting_chips': 5000,
            'blind_increase': 0,
            'selected_style': 'Optimal'
        }

        # Set blinds sizes
        self.blind_size = tk.IntVar()
        self.min_blind_size = 250
        self.max_blind_size = 1000
        # self.blind_size.set(345)
        self.scale1 = tk.Scale(self, orient='horizontal', from_=self.min_blind_size, to=self.max_blind_size,
                               tickinterval=250, length=400, label='Small blind size', variable=self.blind_size,
                               resolution=250, font=self.small_font)
        self.scale1.pack(pady=30, padx=10)

        # Set starting chips amount
        self.starting_chips = tk.IntVar()
        self.min_chips = 5000
        self.max_chips = 15000
        # self.starting_chips.set(6000)
        self.scale2 = tk.Scale(self, orient='horizontal', from_=self.min_chips, to=self.max_chips + 2000,
                               tickinterval=5000, length=400, label='Starting chips', variable=self.starting_chips,
                               resolution=5000, font=self.small_font)
        self.scale2.pack(pady=30, padx=10)

        # Blind increase
        self.blind_increase = tk.IntVar()
        # self.blind_increase.set(0)
        self.scale3 = tk.Scale(self, orient='horizontal', from_=0, to=1, length=300, label='Blind increase',
                               variable=self.blind_increase, tickinterval=1, font=self.small_font)
        self.scale3.pack(pady=30, padx=10)

        # Bot playing style
        self.styles = ["Optimal", "LAG", "TAG", "TP", "LP"]
        self.selected_style = tk.StringVar()
        # self.selected_style.set(self.styles[0])
        self.scale4 = tk.Scale(self, from_=0, to=len(self.styles) - 1, length=300, label="Bot style",
                               orient=tk.HORIZONTAL, command=self.update_label, showvalue=False, font=self.small_font)
        self.scale4.pack(pady=(30, 10), padx=10)
        self.label1 = tk.Label(self, text=self.styles[0], font=self.small_font)
        self.label1.pack(pady=(0, 30))

        # Save button
        self.button1 = tk.Button(self, text="Save", font=self.big_font)
        self.button1.bind("<Button-1>", self.update_settings)
        self.button1.pack()

        # Exit button
        self.label2 = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label2.pack()
        self.label2.bind('<Enter>', lambda event, lbl=self.label2: self.on_enter(lbl, event))
        self.label2.bind('<Leave>', lambda event, lbl=self.label2: self.on_leave(lbl, event))
        self.label2.bind('<Button-1>', lambda event: self.exit(event))

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def update_label(self, value):
        chosen_style = self.styles[int(value)]
        self.label1.config(text=chosen_style)
        self.selected_style.set(chosen_style)

    def exit(self, event):
        self.pack_forget()
        self.window.start_frame.pack(fill=tk.BOTH, expand=True)

    def update_settings(self, event):
        self.settings = {
            'blind_size': self.blind_size.get(),
            'starting_chips': self.starting_chips.get(),
            'blind_increase': self.blind_increase.get(),
            'selected_style': self.selected_style.get()
        }
        # print(self.settings)


class GameFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.game_params = self.window.settings_frame.settings
        # print(f'game parameters : {self.game_params}')
        self.game = Game(frame=self)

        # self.game.community_cards = create_hand(['3♠', '7♦', '9♠', '10♣', 'Q♠'])
        # self.game.user.hole_cards = create_hand(['9♦', '8♠'])

        self.table_color = 'forestgreen'
        self.red_card_color = 'firebrick2'
        self.black_card_color = 'gray8'
        self.bg_card_color = 'gray99'

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 24, 'bold')

        # Bot Frame
        self.bot_frame = tk.Frame(self)
        self.bot_frame.configure(bg=self.window.bg_color)
        self.bot_bet_label = tk.Label(self.bot_frame, text=self.game.bot.bet, font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.bot_style_label = tk.Label(self.bot_frame, text=self.game.bot.style, font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.bot_chips_label = tk.Label(self.bot_frame, text=self.game.bot.chips, font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.bot_role_label = tk.Label(self.bot_frame, text='SB' if self.game.players[self.game.sb_pos] == self.game.bot else 'BB', font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)

        self.bot_style_label.pack()
        self.bot_role_label.pack()
        self.bot_chips_label.pack()
        self.bot_bet_label.pack()
        self.bot_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 50))

        # Community Cards Frame
        self.community_cards_frame = tk.Frame(self, bg=self.table_color)
        self.pot_label = tk.Label(self.community_cards_frame, text=self.game.pot, font=self.big_font,
                                  bg=self.table_color, fg=self.window.fg_color)
        self.pot_label.pack()

        self.community_cards_labels = []
        for card in self.game.community_cards:
            if card.suit == 1 or card.suit == 2:
                label = tk.Label(self.community_cards_frame, text=str(card), font=self.big_font,
                                 foreground=self.red_card_color, background=self.bg_card_color)
            else:
                label = tk.Label(self.community_cards_frame, text=str(card), font=self.big_font,
                                 foreground=self.black_card_color, background=self.bg_card_color)
            self.community_cards_labels.append(label)
            label.pack(side=tk.LEFT, padx=10, pady=(10, 30))
        self.community_cards_frame.pack(side=tk.TOP, pady=(0, 50), padx=50)

        # User Frame
        self.user_frame = tk.Frame(self)
        self.user_frame.configure(bg=self.window.bg_color)
        self.user_bet_label = tk.Label(self.user_frame, text=self.game.user.bet, font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.user_chips_label = tk.Label(self.user_frame, text=self.game.user.chips, font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.user_role_label = tk.Label(self.user_frame,
                                        text='SB' if self.game.players[self.game.sb_pos] == self.game.user else 'BB',
                                        font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.user_hole_cards_frame = tk.Frame(self.user_frame)
        self.user_hole_cards_frame.configure(bg=self.window.bg_color)
        self.user_cards_labels = []
        for card in self.game.user.hole_cards:
            if card.suit == 1 or card.suit == 2:
                label = tk.Label(self.user_hole_cards_frame, text=str(card), font=self.big_font,
                                 foreground=self.red_card_color, background=self.bg_card_color)
            else:
                label = tk.Label(self.user_hole_cards_frame, text=str(card), font=self.big_font,
                                 foreground=self.black_card_color, background=self.bg_card_color)
            self.user_cards_labels.append(label)
            label.pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.user_frame)
        self.button_frame.configure(bg=self.window.bg_color)
        self.fold_button = tk.Button(self.button_frame, text="Fold", font=self.small_font)
        self.fold_button.bind("<Button-1>", self.fold)
        self.check_button = tk.Button(self.button_frame, text="Check", font=self.small_font)
        self.check_button.bind("<Button-1>", self.check)
        self.call_button = tk.Button(self.button_frame, text="Call", font=self.small_font)
        self.call_button.bind("<Button-1>", self.call)
        self.raise_button = tk.Button(self.button_frame, text="Raise", font=self.small_font)
        self.raise_button.bind("<Button-1>", self.do_raise)

        self.fold_button.pack(side=tk.LEFT, padx=10)
        self.check_button.pack(side=tk.LEFT, padx=10)
        self.call_button.pack(side=tk.LEFT, padx=10)
        self.raise_button.pack(side=tk.LEFT, padx=10)

        self.raise_slider = tk.Scale(self.user_frame, from_=0, to=self.game.user.chips, orient=tk.HORIZONTAL,
                                     font=self.small_font, length=500, tickinterval=1000, resolution=50, showvalue=True)

        self.user_bet_label.pack(side=tk.TOP)
        self.user_hole_cards_frame.pack(side=tk.TOP)
        self.user_chips_label.pack(side=tk.TOP)
        self.user_role_label.pack(side=tk.TOP)
        self.button_frame.pack(side=tk.TOP)
        self.raise_slider.pack(side=tk.TOP, pady=(10, 0))

        self.user_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 50))

        # Exit button
        self.label2 = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.label2.pack()
        self.label2.bind('<Enter>', lambda event, lbl=self.label2: self.on_enter(lbl, event))
        self.label2.bind('<Leave>', lambda event, lbl=self.label2: self.on_leave(lbl, event))
        self.label2.bind('<Button-1>', lambda event: self.exit(event))

    def fold(self, event):
        self.game.user.action = 'fold'
        self.game.user.action_bet = 0
        self.update_after_user_action()

    def check(self, event):
        self.game.user.action = 'check'
        self.game.user.action_bet = 0
        self.update_after_user_action()

    def call(self, event):
        self.game.user.action = 'check'
        self.game.user.action_bet = 0
        self.update_after_user_action()

    def do_raise(self, event):
        self.game.user.action = 'check'
        self.game.user.action_bet = self.raise_slider.get()
        self.update_after_user_action()

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        self.pack_forget()
        self.window.start_frame.pack(fill=tk.BOTH, expand=True)

    def update_after_user_action(self):
        self.pot_label.config(text=self.game.pot)
        self.user_bet_label.config(text=self.game.user.bet)
        self.user_chips_label.config(text=self.game.user.chips)

    def update_after_bot_action(self):
        self.pot_label.config(text=self.game.pot)
        self.bot_bet_label.config(text=self.game.bot.bet)
        self.bot_chips_label.config(text=self.game.bot.chips)

    def update_game_state(self):
        # print('i was here')

        self.pot_label.config(text=self.game.pot)
        self.user_bet_label.config(text=self.game.user.bet)
        self.user_chips_label.config(text=self.game.user.chips)
        self.bot_bet_label.config(text=self.game.bot.bet)
        self.bot_chips_label.config(text=self.game.bot.chips)

        # Update community cards
        for label in self.community_cards_labels:
            label.destroy()
            self.community_cards_labels.remove(label)

        for card in self.game.community_cards:
            if card.suit == 1 or card.suit == 2:
                label = tk.Label(self.community_cards_frame, text=str(card), font=self.big_font,
                                 foreground=self.red_card_color, background=self.bg_card_color)
            else:
                label = tk.Label(self.community_cards_frame, text=str(card), font=self.big_font,
                                 foreground=self.black_card_color, background=self.bg_card_color)
            self.community_cards_labels.append(label)
            label.pack(side=tk.LEFT, padx=10, pady=20)

        # Update positions
        self.bot_role_label.config(text='SB' if self.game.players[self.game.sb_pos] == self.game.bot else 'BB')
        self.user_role_label.config(text='SB' if self.game.players[self.game.sb_pos] == self.game.user else 'BB')


class TutorialsFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 24, 'bold')

        self.main_label = tk.Label(self, text="Tutorials", bg='gray18', fg='white', font=self.big_font)
        self.main_label.pack(pady=20)

        self.button_frame = tk.Frame(self.window, bg='gray18')
        self.button_frame.pack()

        self.tutorial_labels = ["1: Introduction to poker basics", "2: Understanding Strategy and Probability",
            "3: Advanced Concepts and Techniques", "4: Practice and Improvement"]

        for text in self.tutorial_labels:
            self.label_tuto = tk.Label(self, text=text, font=self.small_font, bg=self.window.bg_color,
                                       fg=self.window.fg_color)
            self.label_tuto.pack(side=tk.TOP, pady=(100, 0))
            self.label_tuto.bind('<Enter>', lambda event, lbl=self.label_tuto: self.on_enter(lbl, event))
            self.label_tuto.bind('<Leave>', lambda event, lbl=self.label_tuto: self.on_leave(lbl, event))
            self.label_tuto.bind('<Button-1>', lambda event, text=text: self.open_next(text, event))

        # Exit buttons
        self.leave_tuto = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color,
                                   fg=self.window.fg_color)
        self.leave_tuto.pack()
        self.leave_tuto.bind('<Enter>', lambda event, lbl=self.leave_tuto: self.on_enter(lbl, event))
        self.leave_tuto.bind('<Leave>', lambda event, lbl=self.leave_tuto: self.on_leave(lbl, event))
        self.leave_tuto.bind('<Button-1>', lambda event: self.exit(event))

    def open_next(self, menu, event):
        """
        :param menu:
        :param event:
        Opens the menu the user left clicks on
        """
        self.pack_forget()
        tutorial_windows = {
            "1: Introduction to poker basics": self.window.tutorials1,
            "2: Understanding Strategy and Probability": self.window.tutorials2,
            "3: Advanced Concepts and Techniques": self.window.tutorials3,
            "4: Practice and Improvement": self.window.tutorials4
        }

        for text, window in tutorial_windows.items():
            if menu == text:
                window.pack(fill=tk.BOTH, expand=True)

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        self.pack_forget()
        self.window.start_frame.pack(fill=tk.BOTH, expand=True)


class Tutorial1(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Lato', 40, 'bold')
        self.text_font = ('Lato', 12, 'bold')

        # Exit buttons
        self.leave_tuto = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color,
                                   fg=self.window.fg_color)
        self.leave_tuto.pack()
        self.leave_tuto.bind('<Enter>', lambda event, lbl=self.leave_tuto: self.on_enter(lbl, event))
        self.leave_tuto.bind('<Leave>', lambda event, lbl=self.leave_tuto: self.on_leave(lbl, event))
        self.leave_tuto.bind('<Button-1>', lambda event: self.exit(event))

        self.main_label = tk.Label(self, text="1: Introduction to poker basics", bg='gray18', fg='white',
                                   font=self.big_font)
        self.main_label.pack(pady=20)

        self.button_frame = tk.Frame(self.window, bg='gray18')
        self.button_frame.pack()

        #########################################

        self.text_1 = tk.Text(self, wrap=tk.WORD, bg='gray18', fg='white',
                              font=self.text_font)
        self.text_1.pack(expand=True, fill='both', padx=20, pady=20)
        #self.text_1.config(state=tk.DISABLED)

        self.text_1.tag_configure("big", font=("Lato", 20))
        self.text_1.tag_configure("small", font=("Lato", 10))
        self.text_1.tag_configure("bold", font=("Lato", 13, "bold"))
        self.text_1.tag_configure("italic", font=("Lato", 13, "italic"))

        self.subtitle1 = "Rules and objectives\n\n"
        self.text_1.insert(tk.END, self.subtitle1, "big")

        # Insert some initial text without explicit newlines
        self.long_text_1 = (
            "The game of poker is played in multiple different versions. This game, and thus this tutorial will focus on Texas Hold’em poker. It is played with a standard 52-card deck. The goal of the game is to multiply one’s money, represented on the table by chips. "
            "The game is over when only one player has chips at the table. A player is eliminated when they have no chips left. \n\n"
            "In Texas Hold’em, the game is played hand by hand. Each player will be dealt 2 cards, and, by the end of the hand there will be 5 cards present on the table. The player who can make the strongest 5-card combination out of the 2 in their hand and the 5 on the table wins the totality of the bets on the table, called the pot. \n\n"
            "To determine which player has the strongest combination, the rankings are as follows, from weakest to strongest : high card, one pair, two pairs, 3 of a kind, straight, flush, full house, 4 of a kind, straight-flush, royal flush.\n\n"
            "A high card means that out of the most favourable 5 card combination for each player, no player has any notable hand. In this case the player with the highest card wins. If players have the same high card, they split the pot between them. \n\n"
            "A pair means that a player has 2 cards of a kind, for example 2 queens. If multiple players have pairs, the highest pair wins. For the same pairs, the highest remaining card determines the winner. \n\n"
            "3 of a kind works like pairs, but intuitively with 3 cards of a kind, for example 3 queens. No 2 players can have the same strength as 3 of a kind, as there are no 4 cards of one kind in the deck.\n\n"
            "A straight means that a player can make a combination of 5 cards that follow each other, creating a straight. One example is 7, 8, 9, 10, J. In the case where multiple players have a straight, the higher straight takes the pot. \n\n"
            "If they have an identical straight, as no cards of the 5 remain without being taken into account, they split the pot. In the case of straights, the ace can be considered as the highest card in the deck, coming after the king, as the lowest preceding the deuce. In any other application the ace is considered the highest card of a colour, coming after the king. \n\n"
            "A flush is when a player makes a 5 card combination which have all the same colour. To split two players having flushes, the highest card of each flush is to be taken into account. In the case where these are identical, they split the pot. \n\n"
            "4 of a kind works like 3 of a kind. It is also sometimes called a set. A straight-flush is self explanatory, it is a straight from the same colour. Here also, if 2 players have this combination the higher straight wins. \n\n"
            "The royal flush is the best combination in poker, it is unbeatable. It is a straight-flush, at the very top of the deck, so 10, J, Q, K, A of the same colour. No 2 players can have a royal flush in the same hand. \n\n"
        )
        self.text_1.insert(tk.END, self.long_text_1)

        self.subtitle1 = "Gameplay and betting structure\n\n"
        self.text_1.insert(tk.END, self.subtitle1, "big")

        self.long_text_1_1 = (
            "..."
        )
        self.text_1.insert(tk.END, self.long_text_1_1)

    def on_enter(self, label, event):
        """

        :param label:
        :param event:
        Changes the color of the text the user's cursor is on to red
        """
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        """

        :param label:
        :param event:
        Changes the color of the text back to white when cursor is not on the text
        """
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        """
        :param event:
        Closes the tutorial1 window and goes back to main tutorial window
        """
        self.pack_forget()
        self.window.tutorials_frame.pack(fill=tk.BOTH, expand=True)


class Tutorial2(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.text_font = ('Courier New', 12, 'bold')

        # Exit button
        self.leave_tuto = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color,
                                   fg=self.window.fg_color)
        self.leave_tuto.pack()
        self.leave_tuto.bind('<Enter>', lambda event, lbl=self.leave_tuto: self.on_enter(lbl, event))
        self.leave_tuto.bind('<Leave>', lambda event, lbl=self.leave_tuto: self.on_leave(lbl, event))
        self.leave_tuto.bind('<Button-1>', lambda event: self.exit(event))

        self.main_label = tk.Label(self, text="2: Understanding Strategy and Probability", bg='gray18', fg='white',
                                   font=self.big_font)
        self.main_label.pack(pady=20)

        self.button_frame = tk.Frame(self.window, bg='gray18')
        self.button_frame.pack()

        #########################################

        self.text_2 = tk.Text(self, wrap=tk.WORD, bg='gray18', fg='white',
                              font=self.text_font)
        self.text_2.pack(expand=True, fill='both', padx=20, pady=20)
        #self.text_2.config(state=tk.DISABLED)

        self.text_2.tag_configure("big", font=("Lato", 20))
        self.text_2.tag_configure("small", font=("Lato", 10))
        self.text_2.tag_configure("bold", font=("Lato", 13, "bold"))
        self.text_2.tag_configure("italic", font=("Lato", 13, "italic"))

        self.subtitle1 = "Basic strategy\n\n"
        self.text_2.insert(tk.END, self.subtitle1, "big")

        # Insert some initial text without explicit newlines
        self.text_2_1 = (
            "A player needs to develop a sense for the power of the hand they are dealt. This will enable them to male the good decisions, know when to fold, when to bet, and when to limp.\n\n"
            "Limping is when a player tries to go the furthest in a hand without wagering a lot of chips, as they are unsure of their hand. This also means they will know what sized raises they should call with their hands, and where the limit is, in terms of chips, between calling and folding.\n\n"
            "Pocket pairs, meaning being dreamt pairs are considered as strong, as whatever the flop, turn and river may be, they already have a pair at worst. This can also easily lead to 3 of a kind or even a set.\n\n"
            "Apart from that, suited hands, meaning both cards are of the same colour, are appreciated, as this opens up the possibility of a flush.\n\n"
        )
        self.text_2.insert(tk.END, self.text_2_1)

        # Load the image using PhotoImage
        self.image1 = tk.PhotoImage(file="images/poker_cards.png")
        self.resized_image1 = self.image1.subsample(2, 2)
        # Insert the image into the Text widget at the beginning of the second line
        self.text_2.image_create(tk.END, image=self.resized_image1)

        self.text_2_2 = (
        "\nMoreover, hands with a difference higher than 4 are to be avoided for high raises and calls, as they are disadvantageous to make a straight with.\n"
        "Of course, a straight can still be had, but only with one card as the two are too far apart to be on the same straight, meaning that 4 cards are dealt on the table in a straight configuration, making it easy for other players to also have a straight.\n\n"
        "Between all these cases there are a lot of other ordinary hands, but in general, the higher the values of the cards the better. \n\n")
        self.text_2.insert(tk.END, self.text_2_2)

        self.subtitle1 = "Probability and odds\n"
        self.text_2.insert(tk.END, self.subtitle1, "big")

        # Load the image using PhotoImage
        self.image2 = tk.PhotoImage(file="images/poker_odds.png")
        self.resized_image2 = self.image2.subsample(2, 2)
        # Insert the image into the Text widget at the beginning of the second line.
        self.text_2.image_create(tk.END, image=self.resized_image2)

        self.long_text_2_1 = (
            "\nIn pre-flo, each hand has a certain probability of winning, classified in the poker hand power chart. In this chart, all the possible hands are represented.\n\n"
            "The “o” means off-suit, “s” means suited, meaning that they are the same colour or oppositely two different colours.\n"
            "The number associated to the hand is the percentage of hands that are stronger.\n"
            "So, for a pair of aces, this number is 0, as 0% of hands are stronger.\n\n"
        )
        self.text_2.insert(tk.END, self.long_text_2_1)

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        """
        :param event:
        Closes the tutorial2 window and goes back to main tutorial window
        """
        self.pack_forget()
        self.window.tutorials_frame.pack(fill=tk.BOTH, expand=True)


class Tutorial3(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.text_font = ('Courier New', 12, 'bold')

        # Exit button
        self.leave_tuto = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color,
                                   fg=self.window.fg_color)
        self.leave_tuto.pack()
        self.leave_tuto.bind('<Enter>', lambda event, lbl=self.leave_tuto: self.on_enter(lbl, event))
        self.leave_tuto.bind('<Leave>', lambda event, lbl=self.leave_tuto: self.on_leave(lbl, event))
        self.leave_tuto.bind('<Button-1>', lambda event: self.exit(event))

        self.main_label = tk.Label(self, text="3: Advanced Concepts and Techniques", bg='gray18', fg='white',
                                   font=self.big_font)
        self.main_label.pack(pady=20)

        self.button_frame = tk.Frame(self.window, bg='gray18')
        self.button_frame.pack()

        #########################################

        self.text_3 = tk.Text(self, wrap=tk.WORD, bg='gray18', fg='white',
                              font=self.text_font)
        self.text_3.pack(expand=True, fill='both', padx=20, pady=20)
        #self.text_3.config(state=tk.DISABLED)

        self.text_3.tag_configure("big", font=("Lato", 20))
        self.text_3.tag_configure("small", font=("Lato", 10))
        self.text_3.tag_configure("bold", font=("Lato", 13, "bold"))
        self.text_3.tag_configure("italic", font=("Lato", 13, "italic"))

        self.subtitle1 = "Bluffing & deception\n\n"
        self.text_3.insert(tk.END, self.subtitle1, "big")

        # Insert some initial text without explicit newlines
        self.long_text_3 = (
            "Bluffing is the action of raising by a big amount of chips, without having a strong hand. Its purpose is to deceive another player, making them think that one has a very strong, almost unbeatable hand, and thus making them fold and winning the hand.\n\n"
            "To male this technique more advanced, one should look at the cards on the table. If the table makes a lot of powerful combinations possible, often called a wet board, then bluffing will be easier. This is because other players can see that there is also a non-negligible chance of one having a strong hand, thus not daring to challenge the bluff.\n\n"
            "On the other hand, if to have a string combination one has to have a very specific hand, bluffing is harder, as other players will be more inclined to challenge the fact that in fact, one has that specific hand, calling and hoping to win a big amount of chips coming from the bluff.\n\n"
            "Of course, if one has said specific hand, they can either lay low, bet small and grow the pot trying to keep the players in the hand without folding, or bet big, hoping that at least one player will think it is a bluff and call that big raise.\n\n"
            "From there comes an infinite circle, and the only advice that should be taken is that strategy should be adapted to the behaviour and habits of other players around the table. The chip count of players might also affect their capability and inclination to bluff. It should also be carefully adapted to the table.\n\n"
        )
        self.text_3.insert(tk.END, self.long_text_3)

        # Load the image using PhotoImage
        self.image3 = tk.PhotoImage(file="images/poker_serious_guy.png")
        self.resized_image3 = self.image3.subsample(2, 2)
        self.text_3.image_create(tk.END, image=self.resized_image3)

        self.subtitle1 = "\nOpponents and table dynamics\n\n"
        self.text_3.insert(tk.END, self.subtitle1, "big")

        self.long_text_3_1 = (
            "One should keep track for the entirety of the game of the behaviours, patterns and habits of all the other players. Patterns are created and prepared strategies that players use, in which, for all situations betting amounts, acceptable call amounts and fold conditions are determined.\n\n"
            "These of course all need the judgement of the player to be perfect, to know which situation they are in. These are dangerous, as if one’s pattern becomes known to another player, by repeating betting amounts and strategies.\n\n"
            "This can be exploited.\n\n"
            "If a player plays without patterns, they are still going to have a general behaviour, depending on their style and personality. This is much less systematic and depends on way more parameters, so these are harder to exploit. On the other hand, they sometimes lead to errors that wouldn’t have happened with a pattern. \n\n"
            "Each player will also have tells, in body language or even in body function. When one discovers their cards, they will feel pleased or displeased, and noone can totally hide their emotions.\n\n"
            "These are what we call tells, which can range from eye movement, breath depth and rhythm to swallowing reflexes. Again, these can be exploited.\n\n"
        )
        self.text_3.insert(tk.END, self.long_text_3_1)

        self.subtitle1 = "Bet sizing\n\n"
        self.text_3.insert(tk.END, self.subtitle1, "big")

        self.long_text_3_2 = (
            "Bets should be sized according to the type of play we would like to obtain. For example, a bluff will be an unusually large bet compared to the pot and the table. Value bets, when one is nearly sure of winning the hand, is a relatively small bet, small enough to be realistically called by another player. For this one should not appear too confident in their previous plays.\n\n"
            "Continuation betting resembles value betting. It differs in the fact that one is not sure of winning the hand. The board and hand looks promising, but nothing promising came out yet.\n"
            "So, the player feels like their hand has the most chance of winning, thus they slowly grow the pot hoping that their winning card will be turned over. Of course, when there is an infinitesimal chance of winning a hand, one should not continuation bet.\n\n"
        )
        self.text_3.insert(tk.END, self.long_text_3_2)

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        """
        :param event:
        Closes the tutorial3 window and goes back to main tutorial window
        """
        self.pack_forget()
        self.window.tutorials_frame.pack(fill=tk.BOTH, expand=True)

class Tutorial4(tk.Frame):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.text_font = ('Courier New', 12, 'bold')

        # Exit button
        self.leave_tuto = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color,
                                   fg=self.window.fg_color)
        self.leave_tuto.pack()
        self.leave_tuto.bind('<Enter>', lambda event, lbl=self.leave_tuto: self.on_enter(lbl, event))
        self.leave_tuto.bind('<Leave>', lambda event, lbl=self.leave_tuto: self.on_leave(lbl, event))
        self.leave_tuto.bind('<Button-1>', lambda event: self.exit(event))

        self.main_label = tk.Label(self, text="Additional resources", bg='gray18', fg='white',
                                   font=self.big_font)
        self.main_label.pack(pady=20)

        self.button_frame = tk.Frame(self.window, bg='gray18')
        self.button_frame.pack()

        #########################################
        self.link = tk.Label(self, text="Great playlist to learn from a poker expert", bg='white', fg="blue", font=self.text_font, cursor="hand2")
        self.link.pack(pady=20)
        self.link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.youtube.com/watch?v=iPByaVUKI90&list=PL3N4X2KgtefdYT6dGleeoN00XxBbhZZ0V"))

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def exit(self, event):
        """
        :param event:
        Closes the tutorial3 window and goes back to main tutorial window
        """
        self.pack_forget()
        self.window.tutorials_frame.pack(fill=tk.BOTH, expand=True)

class AnalysisFrame(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.configure(bg=self.window.bg_color)

        self.big_font = ('Courier New', 40, 'bold')
        self.small_font = ('Courier New', 24, 'bold')

        self.img = tk.PhotoImage(file='images/analyste-daffaires.png')
        self.img = self.img.subsample(2)
        self.img_label = tk.Label(self, image=self.img, bg=self.window.bg_color)
        self.img_label.pack(side=tk.TOP)

        self.button = []
        for file in os.listdir('analysis/history'):
            if '.txt' in file:
                self.button.append([tk.Label(self, text=file, font=self.big_font, bg=self.window.bg_color,
                                             fg=self.window.fg_color), 'analysis/history/' + f'{file}'])
        for i in range(len(self.button)):
            self.button[i][0].pack(side=tk.TOP)
            self.button[i][0].bind('<Enter>', lambda event, lbl=self.button[i][0]: self.on_enter(lbl, event))
            self.button[i][0].bind('<Leave>', lambda event, lbl=self.button[i][0]: self.on_leave(lbl, event))
            self.assign_button(self.button[i][0], self.button[i][1])

        self.button2 = tk.Label(self, text='<<', font=self.big_font, bg=self.window.bg_color, fg=self.window.fg_color)
        self.button2.pack(side=tk.BOTTOM)
        self.button2.bind('<Enter>', lambda event, lbl=self.button2: self.on_enter(lbl, event))
        self.button2.bind('<Leave>', lambda event, lbl=self.button2: self.on_leave(lbl, event))
        self.button2.bind('<Button-1>', lambda event: self.back_to_menu(event))

    def on_enter(self, label, event):
        label.config(fg=self.window.accent_color)

    def on_leave(self, label, event):
        label.config(fg=self.window.fg_color)

    def back_to_menu(self, event):
        self.pack_forget()
        self.window.start_frame.pack(fill=tk.BOTH, expand=True)

    def assign_button(self, button, file):
        button.bind('<Button-1>', lambda event: self.open_graph(file, event))

    def open_graph(self, file, event):
        new_graph = Analise(file)
        name = new_graph.plot_multiple2()

        img = Image.open(name)
        img.show()
