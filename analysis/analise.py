import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np


class Analise:

    def __init__(self, df):
        super().__init__()
        self.df = pd.read_csv(df, delimiter='\t')
        self.start_chips = 10000
        self.player_list = []
        self.color_list = ['red', 'blue', 'green', 'yellow', 'black', 'white']

    def count_hands(self):
        count = 0
        for index, row in self.df.iterrows():
            if row['Hand#'] > count:
                count = (row['Hand#'])
        return count

    def player_data(self, player):
        lst = []
        for i in range(len(self.df)):
            if self.df.iloc[i, 1] == player:
                lst.append([self.df.iloc[i, 0], self.df.iloc[i, 2]])
        return lst

    def players_list(self):
        for index, row in self.df.iterrows():
            if row['Player'] not in self.player_list:
                self.player_list.append(row['Player'])
        return self.player_list

    def plot_graph(self, player):
        x = []
        y = []
        lst = self.player_data(player)
        for i in range(len(lst)):
            x.append(lst[i][0])
            y.append(lst[i][1])
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel='Hand#', ylabel='Chip count', title=f'Chip count for {player}')
        ax.grid()
        plt.show()

    def plot_multiple(self):
        x = [0]
        y1 = [self.start_chips]
        y2 = [self.start_chips]
        y3 = [self.start_chips]
        y4 = [self.start_chips]
        y5 = [self.start_chips]
        y6 = [self.start_chips]
        players = self.players_list()
        hands = self.count_hands()
        for i in range(hands):
            x.append(i+1)
        for player in players:
            data = self.player_data(player)
            i = players.index(player)
            if i == 1:
                for j in range(len(data)):
                    y1.append(data[j][1])
            if i == 2:
                for j in range(len(data)):
                    y2.append(data[j][1])
            if i == 3:
                for j in range(len(data)):
                    y3.append(data[j][1])
            if i == 4:
                for j in range(len(data)):
                    y4.append(data[j][1])
            if i == 5:
                for j in range(len(data)):
                    y5.append(data[j][1])
            if i == 6:
                for j in range(len(data)):
                    y6.append(data[j][1])
        plt.plot(x, y1)
        plt.show()
        print(y1)
        print(y2)


game = Analise('history/poker_analisis_test.txt')
Analise.plot_multiple(game)
