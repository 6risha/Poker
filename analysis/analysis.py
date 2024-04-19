import matplotlib.pyplot as plt
import pandas as pd
from frames import SettingsFrame


class Analise:

    def __init__(self, df, df2):
        super().__init__()
        self.df = pd.read_csv(df, delimiter='\t')
        self.df2 = pd.read_csv(df2, delimiter='\t', skiprows=[0, 1])
        self.df3 = pd.read_csv(df2, delimiter='\t', nrows=2)
        self.start_chips = 10000
        self.player_list = []
        self.color_list = ['red', 'blue', 'green', 'yellow', 'black', 'white']

    def count_hands(self):
        count = 0
        for index, row in self.df.iterrows():
            if row['Hand#'] > count:
                count = (row['Hand#'])
        return count

    def count_hands2(self):
        count = 0
        for index, row in self.df2.iterrows():
            if row['Hand#'] > count:
                count = (row['Hand#'])
        return count

    def player_data(self, player):
        lst = []
        for i in range(len(self.df)):
            if self.df.iloc[i, 1] == player:
                lst.append([self.df.iloc[i, 0], self.df.iloc[i, 2]])
        return lst

    def player_data_2(self, player):
        lst = []
        for index, row in self.df2.iterrows():
            for j in range(len(self.df2.columns)):
                hand = [self.df2.iloc[index, 0], self.df2.iloc[index, j]]
                if (hand not in lst) and (player == self.df2.columns[j]):
                    lst.append(hand)
        return lst

    def players_list(self):
        for index, row in self.df.iterrows():
            if row['Player'] not in self.player_list:
                self.player_list.append(row['Player'])
        return self.player_list

    def player_list2(self):
        lst = []
        for i in range(1, len(self.df3.columns)):
            if self.df3.iloc[1, i] not in self.player_list:
                lst.append([self.df3.iloc[0, i], self.df3.iloc[1, i]])
        return lst

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
        for k in range(len(players)):
            data = self.player_data(players[k])
            for j in range(len(data)):
                if k == 0:
                    y1.append(data[j][1])
                elif k == 1:
                    y2.append(data[j][1])
                elif k == 2:
                    y3.append(data[j][1])
                elif k == 3:
                    y4.append(data[j][1])
                elif k == 4:
                    y5.append(data[j][1])
                elif k == 5:
                    y6.append(data[j][1])
        if len(y2) == len(x):
            plt.plot(x, y2, label=players[1][0])
        if len(y3) == len(x):
            plt.plot(x, y3, label=players[2][0])
        if len(y4) == len(x):
            plt.plot(x, y4, label=players[3][0])
        if len(y5) == len(x):
            plt.plot(x, y5, label=players[4][0])
        if len(y6) == len(x):
            plt.plot(x, y6, label=players[5][0])
        plt.show()

    def plot_multiple2(self):
        x = [0]
        y1 = [self.start_chips]
        y2 = [self.start_chips]
        y3 = [self.start_chips]
        y4 = [self.start_chips]
        y5 = [self.start_chips]
        y6 = [self.start_chips]
        players = self.player_list2()
        hands = self.count_hands2()
        for i in range(hands):
            x.append(i+1)
        for k in range(len(players)):
            data = self.player_data_2(players[k][1])
            for j in range(len(data)):
                if k == 0:
                    y1.append(data[j][1])
                elif k == 1:
                    y2.append(data[j][1])
                elif k == 2:
                    y3.append(data[j][1])
                elif k == 3:
                    y4.append(data[j][1])
                elif k == 4:
                    y5.append(data[j][1])
                elif k == 5:
                    y6.append(data[j][1])
        plt.plot(x, y1, label=players[0][0])
        if len(y2) == len(x):
            plt.plot(x, y2, label=players[1][0])
        if len(y3) == len(x):
            plt.plot(x, y3, label=players[2][0])
        if len(y4) == len(x):
            plt.plot(x, y4, label=players[3][0])
        if len(y5) == len(x):
            plt.plot(x, y5, label=players[4][0])
        if len(y6) == len(x):
            plt.plot(x, y6, label=players[5][0])
        plt.title(f'Chip count for all players')
        plt.xlabel('Hand')
        plt.ylabel('Chip count')
        plt.legend()
        plt.show()


class StoreData:

    def __init__(self, chip_start):
        super().__init__()
        self.chip_start = chip_start
        self.data = [['ChipStart', 'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6'],
                     [],
                     ['Hand#', 'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6']]
        self.data2 = {'ChipStart': [self.chip_start, {'Hand#': []}],
                      'Player1': ['', {'Player1': []}],
                      'Player2': ['', {'Player2': []}],
                      'Player3': ['', {'Player3': []}],
                      'Player4': ['', {'Player4': []}],
                      'Player5': ['', {'Player5': []}],
                      'Player6': ['', {'Player6': []}]}
        print(self.data)
        print(self.data2)
        self.df = pd.DataFrame()
        self.final = {}

    def get_header_data(self):
        pass

    def get_hand_data(self):
        pass

    def final_df(self):
        for k, v in self.data2.items():
            lst = []
            self.final[k] = [v[0]]



    def write_to_file(self):
        self.df = pd.DataFrame(self.data)
        self.df.to_csv('history/test_write.txt', index=False, sep='\t', index_label=False)
        self.df2.to_csv('history/test_write2.txt', index=False, sep='\t', index_label=False)
        pass


game = StoreData(10000)
StoreData.final_df(game)