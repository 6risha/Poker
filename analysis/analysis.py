import matplotlib.pyplot as plt
import pandas as pd


class Analise:
    def __init__(self, df2):
        """
        :param df2: File in string format to be used for analysis
        """
        super().__init__()
        self.name = df2
        self.plot_name = ''
        self.df = pd.read_csv(df2, delimiter='\t')
        self.df2 = pd.read_csv(df2, delimiter='\t', skiprows=[0, 1])
        self.df3 = pd.read_csv(df2, delimiter='\t', nrows=2)
        self.player_list = []

    def count_hands2(self):
        """
        :return: Number of hands in the dataframe in as an integer
        """
        count = 0
        for index, row in self.df2.iterrows():
            if row['Hand#'] > count:
                count = (row['Hand#'])
        return count

    def player_data_2(self, player):
        """
        :param player: Name of player
        :return: List with the chip-count of a given player, hand by hand, from the dataframe
        """
        lst = []
        for index, row in self.df2.iterrows():
            for j in range(len(self.df2.columns)):
                hand = [self.df2.iloc[index, 0], self.df2.iloc[index, j]]
                if (hand not in lst) and (player == self.df2.columns[j]):
                    lst.append(hand)
        return lst

    def player_list2(self):
        """
        :return: List of all player in the dataframe
        """
        lst = []
        for i in range(1, len(self.df3.columns)):
            if self.df3.iloc[1, i] not in self.player_list:
                lst.append([self.df3.iloc[0, i], self.df3.iloc[1, i]])
        return lst

    def plot_multiple2(self):
        """
        :return: Returns the name of the plot created from the dataframe, after saving it as a png file
        """
        plt.clf()
        x = [0]
        y1 = []
        y2 = []
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
        plt.plot(x, y1, label=players[0][0])
        if len(y2) == len(x):
            plt.plot(x, y2, label=players[1][0])
        plt.title(f'Chip count for all players')
        plt.xlabel('Hand')
        plt.ylabel('Chip count')
        plt.legend()
        self.plot_name = self.name.replace('txt', 'png')
        plt.savefig(self.plot_name, dpi=1000)
        print(f'Graph of {self.plot_name} done')
        return self.plot_name


class StoreData:

    def __init__(self, dico, p1, p2, file_name):
        super().__init__()
        self.dico = dico
        self.file_name = file_name
        self.chip_start = self.dico['chip_start']
        self.p1 = p1
        self.p2 = p2
        self.data = {'ChipStart': [self.chip_start, 'Hand#'],
                     'Player1': ['', 'Player1'],
                     'Player2': ['', 'Player2']}
        # print(self.data)
        self.df = pd.DataFrame()

    def get_header_data(self):
        """
        :return: Gets data from the game to make the header of the dataframe
        """
        self.data['ChipStart'][0] = self.chip_start
        self.data['Player1'][0] = self.p1
        self.data['Player2'][0] = self.p2
        pass

    def get_hand_data(self):
        """
        :return: Gets data from the game to make the hand by hand section of the dataframe
        """
        for i in range(len(self.dico['Player1'])):
            self.data['Player1'].append(self.dico['Player1'][i])
            self.data['Player2'].append(self.dico['Player2'][i])
            self.data['ChipStart'].append(i)
    def write_to_file(self):
        """
        :return: Writes data to a txt file and saves it to the history directory
        """
        self.get_header_data()
        self.get_hand_data()
        self.df = pd.DataFrame(self.data)
        print(self.df)
        self.df.to_csv(f'analysis/history/{self.file_name}', index=False, sep='\t')
