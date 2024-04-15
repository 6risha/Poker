import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        # 0 - clubs (♣), 1 - diamonds (♦), 2 - hearts (♥), 3 - spades (♠)
        self.suit = suit
        self.front_face = f'images/cards/{self.rank}_of_{["clubs", "diamonds", "hearts", "spades"][self.suit]}.png'
        self.back_face = f'images/cards/red_back'

    def __str__(self):
        if self.rank > 10:
            return {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}[self.rank] + ['♣', '♦', '♥', '♠'][self.suit]
        return str(self.rank) + ['♣', '♦', '♥', '♠'][self.suit]


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


class Game:
    # This class is implemented for possible use for game of more than 2 players
    def __init__(self, players: list['Player']):
        # Link players to the game
        for player in players:
            player.game = self

        # Players
        self.players = players
        self.hand_players = players.copy()

        self.dealer_pos = 0
        if len(self.players) > 2:
            # General case
            self.sb_pos = (self.dealer_pos + 1) % len(self.hand_players)
            self.bb_pos = (self.dealer_pos + 2) % len(self.hand_players)
        elif len(self.players) == 2:
            # Case of heads-up poker
            self.sb_pos = self.dealer_pos
            self.bb_pos = (self.dealer_pos + 1) % len(self.hand_players)

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
        while True:
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

            self.hand_players = []
            for player in self.players:
                if player.chips > 0:
                    self.hand_players.append(player)

            if len(self.hand_players) == 1:
                return f'winner: {self.hand_players[0]}'

            self.shift_dealer_and_blinds()

    def shift_dealer_and_blinds(self):
        if len(self.hand_players) == 2:
            # Heads up case
            pass
        else:
            # General case
            pass

    def deal_hole_cards(self):
        # Imitation of real poker, each player is dealt one card at a time
        for _ in range(2):
            for i in range(len(self.players)):
                player_index = (self.dealer_pos + i) % len(self.players)
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
        max_bet = max(self.bets.values())
        for player in self.hand_players:
            if self.bets[player] < max_bet and player.chips > 0:
                return False
        return True

    def everyone_is_asked(self, asked):
        for player in self.hand_players:
            if player not in asked:
                return False
        return True

    def bidding(self, preflop=False):
        # The bidding process continues until:
        # the bets are equal and
        # all the players are asked about their actions and
        # the amount of players in the hand is more than 1
        asked = set()
        if preflop:
            # 2 players clockwise from dealer bet SB and BB, next player after BB starts
            self.hand_players[self.sb_pos].bet(self.small_blind)
            self.hand_players[self.bb_pos].bet(self.big_blind)
            i = (self.bb_pos + 1) % len(self.hand_players)
        else:
            # Closest player clockwise to the dealer starts
            i = (self.dealer_pos + 1) % len(self.hand_players)

        while not ((self.equal_bets() and self.everyone_is_asked(asked)) or (len(self.hand_players) <= 1)):
            print([(player.name, game.bets[player]) for player in self.hand_players])
            # Player who is all in does nat make any actions more, but he still plays this hand
            if self.hand_players[i].chips == 0:
                # TODO: rewrite this
                # we need to check as well whether next players have 0 chips left
                i = (i + 1) % len(self.hand_players)

            act = self.hand_players[i].ask_action()
            asked.add(self.hand_players[i])

            while True:
                if act[0] == 'fold':
                    # the player is out of the game and pass to the next player
                    # index does not change (except the border case), next player will be automatically at this place
                    self.hand_players.pop(i)
                    # VERY IMPORTANT SHIFT
                    if i == self.dealer_pos:
                        self.dealer_pos = -1
                    i = i % len(self.hand_players)
                    break

                elif act[0] == 'check':
                    # player passes to the next player if he already has the highest bet
                    max_bet = max(self.bets.values())
                    if self.bets[self.hand_players[i]] == max_bet:
                        i = (i + 1) % len(self.hand_players)
                        break
                    else:
                        print('Impossible action!')
                        act = self.hand_players[i].ask_action()

                elif act[0] == 'call':
                    # player equates his to bet to the highest one
                    current_bet = self.bets[self.hand_players[i]]
                    max_bet = max(self.bets.values())
                    bet = max_bet - current_bet

                    if self.hand_players[i].chips - bet >= 0:
                        self.hand_players[i].bet(bet)
                        i = (i + 1) % len(self.hand_players)
                        break
                    else:
                        print('Impossible action!')
                        act = self.hand_players[i].ask_action()

                elif act[0] == 'raise':
                    if act[1] <= self.hand_players[i].chips:
                        self.hand_players[i].bet(act[1])
                        i = (i + 1) % len(self.hand_players)
                        break
                    else:
                        print('Impossible action!')
                        act = self.hand_players[i].ask_action()

        print('The bids are made the bidding is over.')

    def divide_pot(self):
        winners = self.determine_winners()

        if len(winners) == 1:
            winning_amount = self.pot
        else:
            winning_amount = self.pot // len(winners)

        for winner in winners:
            winner.chips += winning_amount

        self.pot = 0

    def determine_winners(self):
        return []


class Player:
    def __init__(self):
        self.name = 'John'
        self.game = None
        self.chips = 0
        # We need to provide every player to see its own hole cards
        # So we create a duplicate in this class
        self.hole_cards = []

    def __str__(self):
        hole_cards_str = ', '.join(str(card) for card in self.hole_cards)
        return f'{self.name} | {self.chips} | {hole_cards_str} | '

    def ask_action(self):
        # Returns a tuple (action, bet)
        action = input(f'{self} action: ')
        bet = 0
        if action == 'raise':
            bet = int(input(f'{self} bet: '))
        elif action == 'call':
            if self.game is not None:
                bet = max(game.bets.values())

        res = (action, bet)
        # res = choice.get()
        return res

    def bet(self, amount):
        if amount >= self.chips:
            # All in case
            # Amount of asked bet can be greater than the amount of chips on blinds, but player shouldn't be all in yet
            if self.chips > 0:
                self.game.bets[self] += self.chips
                self.game.pot += self.chips
                self.chips = 0
        else:
            # Usual case
            self.chips -= amount
            self.game.bets[self] += amount
            self.game.pot += amount


class Bot(Player):
    def __init__(self):
        super().__init__()
        self.name = random.choice(['John', 'Bob'])


if __name__ == '__main__':
    player1 = Player()
    player1.chips = 10000
    player2 = Player()
    player2.chips = 10000
    player2.name = 'Bob'
    player3 = Player()
    player3.chips = 10000
    player3.name = 'Stefan'
    players = [player1, player2, player3]

    game = Game(players)
    game.play()
