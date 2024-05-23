import matplotlib.pyplot as plt
import pandas as pd


class Analise:
    def __init__(self, df2):
        '''
        :param df2: File in string format to be used for analysis
        '''
        super().__init__()
        self.name = df2
        self.plot_name = ''
        self.df = pd.read_csv(df2, delimiter='\t')
        self.df2 = pd.read_csv(df2, delimiter='\t', skiprows=[0, 1])
        self.df3 = pd.read_csv(df2, delimiter='\t', nrows=2)
        self.start_chips = 10000
        self.player_list = []
        self.color_list = ['red', 'blue', 'green', 'yellow', 'black', 'white']

    def count_hands2(self):
        '''
        :return: Number of hands in the dataframe in as an integer
        '''
        count = 0
        for index, row in self.df2.iterrows():
            if row['Hand#'] > count:
                count = (row['Hand#'])
        return count

    def player_data_2(self, player):
        '''
        :param player: Name of player
        :return: List with the chip-count of a given player, hand by hand, from the dataframe
        '''
        lst = []
        for index, row in self.df2.iterrows():
            for j in range(len(self.df2.columns)):
                hand = [self.df2.iloc[index, 0], self.df2.iloc[index, j]]
                if (hand not in lst) and (player == self.df2.columns[j]):
                    lst.append(hand)
        return lst

    def player_list2(self):
        '''
        :return: List of all player in the dataframe
        '''
        lst = []
        for i in range(1, len(self.df3.columns)):
            if self.df3.iloc[1, i] not in self.player_list:
                lst.append([self.df3.iloc[0, i], self.df3.iloc[1, i]])
        return lst

    def plot_multiple2(self):
        '''
        :return: Returns the name of the plot created from the dataframe, after saving it as a png file
        '''
        plt.clf()
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
        self.plot_name = self.name.replace('txt', 'png')
        plt.savefig(self.plot_name, dpi= 1000)
        print(f'Graph of {self.plot_name} done')
        return self.plot_name


class StoreData:

    def __init__(self, chip_start):
        super().__init__()
        self.chip_start = chip_start
        self.player1 = ''
        self.player2 = ''
        self.player3 = ''
        self.player4 = ''
        self.player5 = ''
        self.player6 = ''
        self.data = {'ChipStart': [self.chip_start, 'Hand#'],
                     'Player1': ['', 'Player1'],
                     'Player2': ['', 'Player2'],
                     'Player3': ['', 'Player3'],
                     'Player4': ['', 'Player4'],
                     'Player5': ['', 'Player5'],
                     'Player6': ['', 'Player6']}
        print(self.data)
        self.df = pd.DataFrame()

    def get_header_data(self):
        '''
        :return: Gets data from the game to make the header of the dataframe
        '''

        pass

    def get_hand_data(self):
        '''
        :return: Gets data from the game to make the hand by hand section of the dataframe
        '''
        for k, v in self.data.items():
            if k == 'ChipStart':
                v.append(f'{len(v) - 1}')
            if self.data[k][0] == '':
                v.append('0')
        print(self.data)
        pass

    def write_to_file(self):
        '''
        :return: Writes data to a txt file and saves it to the history directory
        '''
        print(self.data['ChipStart'][0])
        self.df = pd.DataFrame(self.data)
        self.df.to_csv('history/test_write3.txt', index=False, sep='\t')

