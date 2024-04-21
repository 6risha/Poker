# Regret matching algorithm for rock paper scissors

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice


class Trainer:
    def __init__(self):

        self.num_actions = 3

        # 0 - rock, 1 - paper, 3 - scissors
        self.actions = np.arange(self.num_actions)

        # player - vertical, opponent - horizontal
        self.actions_utility = np.array([[0, -1, 1],
                                         [1, 0, -1],
                                         [-1, 1, 0]])

        self.pl_regret_sum = np.zeros(self.num_actions)
        self.pl_strategy_sum = np.zeros(self.num_actions)

        self.opp_regret_sum = np.zeros(self.num_actions)
        self.opp_strategy_sum = np.zeros(self.num_actions)

    def get_action(self, strategy):
        # With this function it is possible to get action of player or opponent
        # Strategy - list of probabilities for choice of an action
        return choice(self.actions, p=strategy)

    def get_reward(self, player_action, opponent_action):
        return self.actions_utility[player_action, opponent_action]

    def get_strategy(self, regret_sum):
        # (regret sum)/(norm sum) = strategy

        # Set negative sums to 0
        new_sum = np.clip(regret_sum, 0, None)
        normalizing_sum = np.sum(new_sum)

        if normalizing_sum > 0:
            new_sum /= normalizing_sum
        else:
            # If norm. sum is nil it means that all the actions we distributed evenly
            new_sum = np.repeat(1 / self.num_actions, self.num_actions)

        return new_sum

    def get_average_strategy(self, strategy_sum):
        avg_strategy = np.zeros(self.num_actions)
        normalizing_sum = np.sum(strategy_sum)
        if normalizing_sum > 0:
            avg_strategy = strategy_sum / normalizing_sum
        else:
            avg_strategy = np.repeat(1 / self.num_actions, self.num_actions)
        return avg_strategy

    def train(self, num_iterations):
        for _ in range(num_iterations):

            pl_strategy = self.get_strategy(self.pl_regret_sum)
            opp_strategy = self.get_strategy(self.opp_regret_sum)

            self.pl_strategy_sum += pl_strategy
            self.opp_strategy_sum += opp_strategy

            pl_action = self.get_action(pl_strategy)
            opp_action = self.get_action(opp_strategy)

            pl_reward = self.get_reward(pl_action, opp_action)
            opp_reward = self.get_reward(pl_action, opp_action)

            for act in range(self.num_actions):
                # pl_regret = max(0, self.get_reward(player_action=act, opponent_action=opp_action) - pl_reward)
                # opp_regret = max(0, self.get_reward(player_action=act, opponent_action=pl_action) - opp_reward)

                pl_regret = self.get_reward(player_action=act, opponent_action=opp_action) - pl_reward
                opp_regret = self.get_reward(player_action=act, opponent_action=pl_action) - opp_reward

                self.pl_regret_sum[act] += pl_regret
                self.opp_regret_sum[act] += opp_regret

                # print(pl_regret, opp_regret)


def plot_evolution(strategy, title, iterations):
    plt.figure(figsize=(8, 6))
    num_iterations = len(strategy)
    x_values = np.arange(1, num_iterations + 1)
    plt.plot(x_values, strategy)
    plt.title(title)
    plt.xlabel('Iterations')
    plt.ylabel('Probability')
    plt.legend(['Rock', 'Paper', 'Scissors'])
    plt.grid(True)
    plt.xticks(ticks=x_values, labels=[str(num) for num in iterations])
    plt.show()


def main():
    pl_strategy_evolution = []
    opp_strategy_evolution = []
    iterations = [10, 100, 1000, 10000]
    for num in iterations:
        trainer = Trainer()
        trainer.train(num)
        pl_strategy_evolution.append(trainer.get_average_strategy(trainer.pl_strategy_sum))
        opp_strategy_evolution.append(trainer.get_average_strategy(trainer.opp_strategy_sum))

    plot_evolution(pl_strategy_evolution, 'Player Strategy Evolution', iterations)
    plot_evolution(opp_strategy_evolution, 'Opponent Strategy Evolution', iterations)

    print(f'Player Strategy Evolution: {pl_strategy_evolution}')
    print(f'Opponent Strategy Evolution: {opp_strategy_evolution}')


if __name__ == '__main__':
    main()
