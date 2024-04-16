import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        # 0 - clubs (♣), 1 - diamonds (♦), 2 - hearts (♥), 3 - spades (♠)
        self.suit = suit
        self.front_face = f'images/cards/{self.rank}_of_{["clubs", "diamonds", "hearts", "spades"][self.suit]}.png'
        self.back_face = f'images/cards/red_back'

    def __str__(self):
        suits_symbols = ['♣', '♦', '♥', '♠']
        ranks_symbols = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

        rank_str = ranks_symbols.get(self.rank, str(self.rank))
        suit_str = suits_symbols[self.suit]

        return f"{rank_str}{suit_str}"


class Deck(list):
    def __init__(self):
        super().__init__()
        for suit in range(4):
            for rank in range(2, 15):
                self.append(Card(rank, suit))

    def __str__(self):
        return '[' + ', '.join(str(card) for card in self) + ']'


class Player:
    def __init__(self):
        self.name = 'No name'
        self.game = None
        self.chips = 0
        self.bet = 0
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
                bet = max(self.game.user.bet, self.game.bot.bet)

        return action, bet

    def make_bet(self, amount):
        if amount >= self.chips:
            # All in case
            if self.chips > 0:
                self.bet += self.chips
                self.game.pot += self.chips
                self.chips = 0
            else:
                raise ValueError('No chips left to do the bet')
        else:
            # Usual case
            self.chips -= amount
            self.bet += amount
            self.game.pot += amount


class Bot(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Grisha'
        self.style = None


class User(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Thomas'


class Game:
    # This class is implemented only for heads-up poker
    def __init__(self):
        # Parameters of the game
        self.starting_chips = 10000
        self.small_blind = 250
        self.increasing_blinds = False
        self.playing_style = None

        # Bot
        self.bot = Bot()
        self.bot.game = self
        self.bot.chips = self.starting_chips
        self.bot.style = self.playing_style

        # User
        self.user = User()
        self.user.game = self
        self.user.chips = self.starting_chips

        # positions distribution
        self.players = [self.bot, self.user]
        random.shuffle(self.players)
        self.sb_pos = 0
        self.bb_pos = 1

        # Cards
        self.deck = Deck()
        random.shuffle(self.deck)

        self.cards_for_current_hand = random.sample(self.deck, 8)
        self.community_cards = []

        # Bets
        self.big_blind = 2 * self.small_blind
        self.min_bet = self.big_blind
        self.user.bet = 0
        self.bot.bet = 0
        self.pot = 0

    def play(self):
        i = 1
        while self.user.chips > 0 and self.bot.chips > 0:
            print(f':::: Hand #{i}')
            print()
            # Preflop
            self.players[self.sb_pos].make_bet(self.small_blind)
            print(f':::: SB: {self.players[self.sb_pos].name}')

            self.players[self.bb_pos].make_bet(self.big_blind)
            print(f':::: BB: {self.players[self.bb_pos].name}')

            self.deal_hole_cards()
            print(f':::: Dealing hole cards: {self.bot.name} - {[str(card) for card in self.bot.hole_cards]}, {self.user.name} - {[str(card) for card in self.user.hole_cards]}')
            print()
            print(f':::: Preflop')

            if self.bidding(preflop=True):
                self.deal_community_cards(3)
                print()
                print(f':::: Flop: {[str(card) for card in self.community_cards]}')
                if self.bidding():
                    self.deal_community_cards(1)
                    print()
                    print(f':::: Turn: {[str(card) for card in self.community_cards]}')
                    if self.bidding():
                        self.deal_community_cards(1)
                        print()
                        print(f':::: River: {[str(card) for card in self.community_cards]}')
                        self.bidding()

            print("THE HAND IS AT FINAL STAGE")
            self.divide_pot()
            self.swap_positions()
            i += 1

    def deal_hole_cards(self):
        for i in range(2):
            self.players[i].hole_cards = self.cards_for_current_hand[0:2]
            del self.cards_for_current_hand[:2]

    def deal_community_cards(self, num):
        self.community_cards.extend(self.cards_for_current_hand[:num])
        del self.cards_for_current_hand[:num]

    def swap_positions(self):
        self.sb_pos, self.bb_pos = self.bb_pos, self.sb_pos

    def divide_pot(self):
        pass

    def bidding(self, preflop=False):
        current_player_index = self.sb_pos if preflop else self.bb_pos

        asked = 0
        round_completed = False

        while not round_completed:
            print(f'{[(player.name, player.bet) for player in self.players]}')
            player = self.players[current_player_index]
            opponent = self.players[not current_player_index]
            action, bet = player.ask_action()
            asked += 1
            # print(asked)

            if action == 'fold':
                round_completed = True
                print(f'{player.name} has folded')
                return False

            elif action == 'check':
                if player.bet != opponent.bet:
                    print('Impossible action. Try again.')
                    asked -= 1
                    continue
                else:
                    if asked >= 2:
                        round_completed = True

            elif action == 'call':
                if player.bet < opponent.bet:
                    player.make_bet(opponent.bet - player.bet)
                else:
                    print('Impossible action. Try again.')
                    asked -= 1
                    continue

                if asked >= 2:
                    round_completed = True

            elif action == 'raise':
                if self.min_bet <= bet <= player.chips and opponent.bet - player.bet < bet:
                    player.make_bet(bet)
                else:
                    print('Impossible action. Try again.')
                    asked -= 1
                    continue

            else:
                print('Impossible action. Try again.')
                asked -= 1
                continue

            current_player_index = not current_player_index

        print('The bids are made and the bidding is over.')
        return True if self.user.chips and self.bot.chips else False


if __name__ == '__main__':
    game = Game()
    game.play()
