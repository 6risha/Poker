# The training is done for the preflop stage only
# The training is done for the bot being small blind

from cards import *

import numpy as np
from random import shuffle
from tqdm import tqdm
import joblib

# Poker definitions
# The bot is trained as if its opponent is user
game = Game()
global player
players = [game.bot, game.user]

FOLD = ('fold', 0, 'p')
CHECK = ('check', 0, 'p')
CALL = ('call', 0, 'c')  # 0 is changed in the game to the right bet
RAISE_1BB = ('raise', max(game.bot.bet, game.user.bet) + game.big_blind, 'b')
RAISE_2BB = ('raise', max(game.bot.bet, game.user.bet) + game.big_blind * 2, 'b')
RAISE_4BB = ('raise', max(game.bot.bet, game.user.bet) + game.big_blind * 4, 'b')
ALL_IN = ('raise', game.user.chips if player == game.user else game.bot.chips, 'b')

ACTIONS = [FOLD, CHECK, CALL, RAISE_1BB, RAISE_2BB, RAISE_4BB, ALL_IN]
NUM_ACTIONS = 7

# Initialize TreeMap
TreeMap = {}


class Node:
    # TODO
    def __init__(self):
        self.infoSet = ''
        self.regretSum = np.zeros(NUM_ACTIONS)
        self.strategy = np.zeros(NUM_ACTIONS)
        self.strategySum = np.zeros(NUM_ACTIONS)

    def getStrategy(self, realizationWeight):
        pass

    def getAverageStrategy(self):
        pass

    def display(self):
        pass


def cfr(cards, history, p0, p1):
    # TODO
    player = players[len(history) % 2]
    opponent = players[1 - player]

    # Determine whether the node is terminal
    if len(history) > 1:
        # TODO: determine winners
        if history[-2:] == 'bp':  # raise (all-in), fold
            pass
        elif history[-2:] == 'cp':  # call, check
            pass
        elif history[-2:] == 'bc':  # raise (all-in), call
            pass
        elif history[-2:] == 'bb' and opponent.chips == 0:  # raise, all-in
            pass
    elif len(history) == 1:
        if history[0] == 'p':  # fold
            pass

    infoSet = ''.join(str(card) for card in player.hole_cards + history)
    if infoSet not in TreeMap:
        node = Node()
        node.infoSet = infoSet
        TreeMap[infoSet] = node
    else:
        node = TreeMap[infoSet]

    strategy = node.getStrategy(p0 if player == players[0] else p1)
    util = np.zeros(NUM_ACTIONS)
    nodeUtil = 0

    for act in ACTIONS:
        if act[0] == 'fold':
            pass
        elif act[0] == 'check':
            pass
        elif act[0] == 'call':
            pass
        elif act[0] == 'raise':
            pass


# Train the model
def train(iterations):
    util = 0
    for i in tqdm(range(iterations), desc="Training Loop"):
        cards = random.sample(game.deck, 4)
        util += cfr(cards, '', 1, 1)
        if i and (i % 100_000 == 0):
            print(" Average game value: ", util / (i + 1))
    print("Training complete.")


if __name__ == "__main__":
    train_from_scratch = False
    if train_from_scratch:
        train(1_000_000)
        joblib.dump(TreeMap, "HUNL-TreeMap.joblib")
    else:
        TreeMap = joblib.load("HUNL-TreeMap.joblib")

    print("Total Number of Infosets:", len(TreeMap))
    for infoSet in TreeMap:
        TreeMap[infoSet].display()
