import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        # 0 - clubs (♣), 1 - diamonds (♦), 2 - hearts (♥), 3 - spades (♠)
        self.suit = suit
        self.front_face = f'images/cards/{self.rank}_of_{["clubs", "diamonds", "hearts", "spades"][self.suit]}.png'
        self.back_face = f'images/cards/red_back'

    def __str__(self):
        return f'{self.rank}{["♣", "♦", "♥", "♠"][self.suit]}'


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


class Hand:
    # This class is implemented for possible use for game of more than 2 players
    def __init__(self, players: list):
        # Players
        self.players = players
        self.hand_players = players.copy()

        self.dealer_position = 0
        self.big_blind_position = (self.dealer_position + 1) % len(self.hand_players)
        self.small_blind_position = (self.dealer_position + 2) % len(self.hand_players)

        # Cards
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.hole_cards = {}

        # Bets
        self.small_blind = 250
        self.big_blind = 500
        self.increasing_blinds = False

        self.bets = {player: 0 for player in self.hand_players}
        self.pot = 0

    def play(self):
        self.deal_hole_cards()
        # Preflop
        self.bidding(preflop=True)
        if len(self.hand_players) > 1:
            # Flop
            self.deal_community_cards(3)
            self.bidding()
            if len(self.hand_players) > 1:
                # Turn
                self.deal_community_cards(1)
                self.bidding()
                if len(self.hand_players) > 1:
                    # River
                    self.deal_community_cards(1)
                    self.bidding()

        self.divide_pot()
        self.shift_dealer()
        self.hand_players = self.players.copy()

        # The function will be in the while loop until there is one player with all the chips
        # TODO: change return for a proper one
        return None

    def shift_dealer(self):
        self.dealer_position += 1
        self.dealer_position %= len(self.hand_players)

    def deal_hole_cards(self):
        # Imitation of real poker, each player is dealt one card at a time
        for _ in range(2):
            for i in range(len(self.players)):
                player_index = (self.dealer_position + i) % len(self.players)
                player = self.players[player_index]
                card = self.deck.pop()

                if player not in self.hole_cards:
                    self.hole_cards[player] = []
                self.hole_cards[player].append(card)

                player.hole_cards.append(card)

    def deal_community_cards(self, num):
        for _ in range(num):
            self.community_cards.append(self.deck.pop())

    def equal_bets(self):
        res = True
        bet = self.bets[self.hand_players[0]]
        for player in self.hand_players:
            if bet != self.bets[player]:
                res = False
        return res

    def bidding(self, preflop=False):
        # The bidding process continues until:
        # the bets are equal and
        # all the players are asked about their actions and
        # the amount of players in the hand is more than 1
        asked = []
        if preflop:
            self.hand_players[self.small_blind_position].bet(self.small_blind)
            self.hand_players[self.big_blind_position].bet(self.big_blind)
            i = self.big_blind_position + 1
        else:
            i = self.dealer_position + 1
            while i in range(len(self.players)) and self.players[i] not in self.hand_players:
                i += 1

        while len(self.hand_players) > 1 and not self.equal_bets() and not set(asked) == set(self.hand_players):
            act = self.hand_players[i].ask_action()
            asked.append(self.hand_players[i])

            while True:
                if act[0] == 'fold':
                    # just out of the game and pass to the next player
                    # index does not change (except the border case), next player will be automatically at this place
                    self.hand_players.pop(i)
                    i = i % len(self.hand_players)
                    break

                elif act[0] == 'check':
                    # player passes to the next player if he already has the highest bet
                    if self.bets[self.hand_players[i]] == max:
                        i = (i + 1) % len(self.hand_players)
                        break
                    else:
                        print('Impossible action!')
                        act = self.hand_players[i].ask_action()

                elif act[0] == 'call':
                    # TODO
                    # player equates his to bet to the highest one
                    # Current bet
                    current_bet = 0
                    # Maximum bet
                    max_bet = 0
                    # Equate
                    if self.hand_players[i].chips_amount - (max_bet - current_bet) > 0:
                        pass
                        i = (i + 1) % len(self.hand_players)

                elif act[0] == 'raise':
                    # TODO
                    if act[1] == self.hand_players[i].chips_amount:
                        # All-in case
                        pass
                    elif act[1] < self.hand_players[i].chips_amount:
                        # Usual raise
                        pass
                    else:
                        print('Impossible action!')
                        act = self.hand_players[i].ask_action()

    def divide_pot(self):
        # Consider equal combinations
        pass


class Player:
    def __init__(self):
        self.name = 'John'
        self.chips_amount = 0
        self.hole_cards = []

    @staticmethod
    def ask_action(choice):
        res = choice.get()
        return res

    def bet(self, amount):
        # Consider the all-in bets in the game (not to forget about all-in at blinds)
        pass


class Bot(Player):
    def __init__(self):
        super().__init__()
        self.name = random.choice(['John', 'Bob'])


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    print(deck)

    player1 = Player()
    player2 = Player()
    player3 = Player()
    players = [player1, player2, player3]

    game = Hand(players)
    game.deal_hole_cards()
    print(game.hole_cards)
