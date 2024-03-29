import tkinter as tk
import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        # 0 - clubs (♣), 1 - diamonds (♦), 2 - hearts (♥), 3 - spades (♠)
        self.suit = suit
        self.image = f'cards/{self.rank}_of_{['clubs', 'diamonds', 'hearts', 'spades'][self.suit]}.png'

    def __str__(self):
        return f'{self.rank}{['♣', '♦', '♥', '♠'][self.suit]}'


class Deck(list):
    def __init__(self):
        super().__init__()
        # Jokers are added to the deck
        for suit in range(4):
            for rank in range(2, 15):
                self.append(Card(rank, suit))

    def __str__(self):
        return '[' + ', '.join(str(card) for card in self) + ']'

    def shuffle(self):
        random.shuffle(self)


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    print(deck)
