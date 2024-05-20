import numpy as np
import itertools
import joblib
from tqdm import tqdm
from cards import *

# Poker definitions
game = Game()
global player
global opponent
players = [game.bot, game.user]

FOLD = ('fold', 0, 'p')
CHECK = ('check', 0, 'p')
CALL = ('call', abs(game.bot.bet - game.user.bet), 'c')
RAISE_1BB = ('raise', abs(game.bot.bet - game.user.bet) + game.big_blind, 'b')
RAISE_2BB = ('raise', abs(game.bot.bet - game.user.bet) + game.big_blind * 2, 'b')
RAISE_4BB = ('raise', abs(game.bot.bet - game.user.bet) + game.big_blind * 4, 'b')
ALL_IN = ('raise', game.user.chips if player == game.user else game.bot.chips, 'b')

ACTIONS = [FOLD, CHECK, CALL, RAISE_1BB, RAISE_2BB, RAISE_4BB, ALL_IN]
NUM_ACTIONS = 7

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


def cfr(community_cards, hole_cards, history, p0, p1):
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

    player_hand = []

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


def train_preflop(iterations):
    util = 0
    for i in tqdm(range(iterations), desc="Training Loop"):
        cards = random.sample(game.deck, 4)
        util += cfr(cards, '', 1, 1)
        if i and (i % 100_000 == 0):
            print(" Average game value: ", util / (i + 1))
    print("Training complete.")


def train(iterations, num_cards=3):
    utils = []
    community_combinations = list(itertools.combinations(game.deck, num_cards))
    for community_cards in tqdm(community_combinations, desc="Community Cards Combinations"):
        util = 0
        selected_set = set(community_cards)
        remaining_cards = [card for card in game.deck if card not in selected_set]
        for _ in tqdm(range(iterations), desc="Training Loop", leave=False):
            hole_cards = random.sample(remaining_cards, 4)
            util += cfr(community_cards, hole_cards, '', 1, 1)
        utils.append(util)
    avg_util = np.mean(utils)
    print(f"Average Utility: {avg_util}")


if __name__ == "__main__":
    train_from_scratch = False
    if train_from_scratch:
        train_preflop(1_000_000)
        train(1200, 3)
        train(800, 4)
        train(400, 5)
        joblib.dump(TreeMap, "HUNL-TreeMap.joblib")
    else:
        TreeMap = joblib.load("HUNL-TreeMap.joblib")

    print("Total Number of Infosets:", len(TreeMap))
    for infoSet in TreeMap:
        TreeMap[infoSet].display()
