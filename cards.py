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
    # This class is written for possible use for game of more than 2 players
    def __init__(self, players: list):
        # Players
        self.players = players
        self.num_players = len(self.players)

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

    def deal_hole_cards(self):
        # Imitation of real poker, each player is dealt one card at a time
        for _ in range(2):
            for i in range(self.num_players):
                player_index = (self.dealer_position + i) % self.num_players
                player = self.players[player_index]
                card = self.deck.pop()

                if player not in self.hole_cards:
                    self.hole_cards[player] = []
                self.hole_cards[player].append(card)

                # player.hole_cards.append(card)

    def deal_community_cards(self, num):
        for _ in range(num):
            self.community_cards.append(self.deck.pop())

    def bidding(self, current_player_index=0):
        if current_player_index == self.dealer_position:
            return

        current_player = self.players[current_player_index]
        action = current_player.ask_action()

        if action == 'raise':
            pass
        elif action == 'fold':
            pass
        elif action == 'call':
            pass
        elif action == 'check':
            pass

        next_player_index = (current_player_index + 1) % self.num_players
        self.bidding(next_player_index)

    def pre_flop(self):
        pass

    def flop(self):
        pass

    def turn(self):
        pass

    def river(self):
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

    def ask_action(self, choice):
        res = choice.get()
        if res == 'fold':
            self.fold()
        elif res == 'call':
            self.call()
        elif res == 'check':
            self.check()
        elif res == 'raise_bet':
            self.raise_bet()
        return res

    def bet(self, amount):
        pass


class Bot(Player):
    pass


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    print(deck)

    game = Hand(['Player1', 'Player2', 'Player3', 'Player4'])
    game.deal_hole_cards()
    print(game.hole_cards)
