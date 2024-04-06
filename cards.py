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
        self.num_players = len(self.hand_players)

        self.dealer_position = 0
        self.big_blind_position = (self.dealer_position + 1) % self.num_players
        self.small_blind_position = (self.dealer_position + 2) % self.num_players

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
        self.bidding()
        if self.num_players > 1:
            # Flop
            self.deal_community_cards(3)
            self.bidding()
            if self.num_players > 1:
                # Turn
                self.deal_community_cards(1)
                self.bidding()
                if self.num_players > 1:
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
        self.dealer_position %= self.num_players

    def deal_hole_cards(self):
        # Imitation of real poker, each player is dealt one card at a time
        for _ in range(2):
            for i in range(self.num_players):
                player_index = (self.dealer_position + i) % self.num_players
                player = self.hand_players[player_index]
                card = self.deck.pop()

                if player not in self.hole_cards:
                    self.hole_cards[player] = []
                self.hole_cards[player].append(card)

                player.hole_cards.append(card)

    def deal_community_cards(self, num):
        for _ in range(num):
            self.community_cards.append(self.deck.pop())

    def equal_bets(self):
        pass

    def bidding(self):
        # The bidding process continues until the bets are equal
        while not self.equal_bets():
            pass

    def divide_pot(self):
        pass


class Player:
    def __init__(self):
        self.name = 'John'
        self.chip_amount = 0
        self.hole_cards = []

    def fold(self):
        pass

    def call(self):
        pass

    def check(self):
        pass

    def raise_bet(self):
        pass

    @staticmethod
    def ask_action(choice):
        res = choice.get()
        return res

    def bet(self, amount):
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
