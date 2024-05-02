# Counterfactual Regret Minimization, with usage of regret matching

import numpy as np
from random import shuffle
# to display progress bar
from tqdm import tqdm
# to run computationally intensive tasks in parallel
import joblib

# Kuhn poker definitions
PASS, BET = 0, 1
NUM_ACTIONS = 2
TreeMap = {}


class Node:
    def __init__(self):
        self.infoSet = ''
        self.regretSum = np.zeros(NUM_ACTIONS)
        self.strategy = np.zeros(NUM_ACTIONS)
        self.strategySum = np.zeros(NUM_ACTIONS)

    def getStrategy(self, realizationWeight):
        # Get current information set mixed strategy through regret-matching
        self.strategy = np.maximum(0, self.regretSum)
        normalizingSum = np.sum(self.strategy)

        if normalizingSum > 0:
            self.strategy /= normalizingSum
        else:
            self.strategy = np.ones_like(self.strategy) / NUM_ACTIONS

        self.strategySum += realizationWeight * self.strategy

        return self.strategy

    def getAverageStrategy(self):
        normalizingSum = np.sum(self.strategySum)
        avgStrategy = np.zeros(NUM_ACTIONS)

        if normalizingSum > 0:
            avgStrategy = self.strategySum / normalizingSum
        else:
            avgStrategy = np.ones_like(self.strategySum) / NUM_ACTIONS

        return avgStrategy

    def display(self):
        average_strategy = np.around(self.getAverageStrategy(), 4)
        print(f"{self.infoSet.ljust(3)} -> {average_strategy}")


# p0, p1 reach probabilities
def cfr(cards, history, p0, p1):
    player = len(history) % 2
    opponent = 1 - player

    # Return payoff for terminal states
    if len(history) > 1:
        isPlayersCardHigher = (cards[player] > cards[opponent])

        # Terminal pass
        if history[-1] == 'p':
            if history == 'pp':
                return 1 if isPlayersCardHigher else -1
            else:
                if history == 'bp':
                    return 1
                # TODO: понять почему все-таки тут 1 возвращается
                elif history == 'pbp':
                    return 1

        # Double bet
        elif history[-2:] == 'bb':
            return 2 if isPlayersCardHigher else -2

    # Get information set node or create it
    infoSet = str(cards[player]) + history
    if infoSet not in TreeMap:
        node = Node()
        node.infoSet = infoSet
        TreeMap[infoSet] = node
    else:
        node = TreeMap[infoSet]

    # For each action, recursively call cfr with additional history and probability
    strategy = node.getStrategy(p0 if player == 0 else p1)
    util = np.zeros(NUM_ACTIONS)
    nodeUtil = 0

    for a in range(NUM_ACTIONS):
        nextHistory = history + ("p" if a == 0 else "b")
        if player == 0:
            util[a] = - cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = - cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    # For each action, compute and accumulate counterfactual regret
    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        node.regretSum[a] += (p1 if player == 0 else p0) * regret

    return nodeUtil


def train(iterations):
    cards = [1, 2, 3]
    util = 0
    for i in tqdm(range(iterations), desc="Training Loop"):
        shuffle(cards)
        util += cfr(cards, "", 1, 1)
        if i and (i % 100_000 == 0):
            print(" Average game value: ", util / (i+1))
    print("Training complete.")


if __name__ == "__main__":
    train_from_scratch = False
    if train_from_scratch:
        train(1_000_000)
        joblib.dump(TreeMap, "KuhnTreeMap.joblib")
    else:
        TreeMap = joblib.load("KuhnTreeMap.joblib")

    print("Total Number of Infosets:", len(TreeMap))
    for infoSet in TreeMap:
        TreeMap[infoSet].display()
