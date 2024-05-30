import main
import frames
import random
import numpy as np
import copy
from analysis.analysis import *
import datetime


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
        self.fold = False

    def __str__(self):
        hole_cards_str = ', '.join(str(card) for card in self.hole_cards)
        return f'{self.name} | chips: {self.chips} | {hole_cards_str} | '

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

        # Possible styles:
        # LP - loose passive (plays every hand, calls every bet)
        # TP - tight passive (plays only strongest hands, calls every bet)
        # LAG - loose aggressive (plays every hand, raises actively)
        # TAG - tight aggressive (plays only strongest hands, raises actively)
        self.style = "LAG"

        self.history = ''
        self.info_set = ''
        self.tree_map = self.load_strategies()

    def load_strategies(self):
        return {}

    def update_info_set(self):
        sorted_cards = sorted(self.hole_cards + self.game.community_cards, key=lambda card: (card.rank, card.suit))
        self.info_set = ''.join(str(card) for card in sorted_cards)

    def ask_action(self):
        # print(self.info_set)

        fold = ('fold', 0, 'p')
        check = ('check', 0, 'p')
        call = ('call', self.game.user.bet - self.bet, 'c')
        raise_1bb = ('raise', (self.game.user.bet - self.bet) + self.game.big_blind, 'b')
        raise_2bb = ('raise', (self.game.user.bet - self.bet) + self.game.big_blind * 2, 'b')
        raise_4bb = ('raise', (self.game.user.bet - self.bet) + self.game.big_blind * 4, 'b')
        all_in = ('raise', self.chips, 'b')

        actions = [fold, check, call, raise_1bb, raise_2bb, raise_4bb, all_in]

        base_strategies = {
            'Optimal': [0.2, 0.3, 0.2, 0.14, 0.1, 0.05, 0.01],
            'LAG': [0.2, 0.2, 0.2, 0.15, 0.1, 0.1, 0.05],
            'TAG': [0.05, 0.2, 0.1, 0.25, 0.2, 0.15, 0.05],
            'TP': [0.1, 0.25, 0.4, 0.1, 0.05, 0.05, 0.05],
            'LP': [0.1, 0.3, 0.4, 0.1, 0.05, 0.03, 0.02]
        }

        if self.info_set in self.tree_map:
            strategy = self.tree_map[self.info_set]
        else:
            strategy = base_strategies[self.style]

        while True:
            # Returns a list of 1 element, so we need an index at the end
            action = random.choices(actions, weights=strategy)[0]
            # print(action)
            try:
                # Remove unnecessary folds first
                if action[0] == 'fold' and self.bet == self.game.user.bet:
                    action = check
                self.validate_action(action)
                print(f'{self}: {action}')
                self.info_set += action[2]
                return action[0], action[1]
            except ValueError:
                continue

    def validate_action(self, action):
        act, bet = action[0], action[1]
        opponent = self.game.user

        if act == 'fold':
            return

        if act == 'check':
            if self.bet != opponent.bet:
                raise ValueError('Invalid action')
            return

        if act == 'call':
            if self.bet >= opponent.bet:
                raise ValueError('Invalid action')
            return

        if act == 'raise':
            if opponent.chips == 0:
                raise ValueError('Invalid action')
            if not ((self.game.min_bet <= bet < self.chips and opponent.bet - self.bet < bet) or
                    (bet == self.chips and opponent.bet - self.bet < bet)):
                raise ValueError('Invalid action')
            return

        raise ValueError('Invalid action')


class User(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Thomas'
        self.action = None
        self.action_bet = None

    # def ask_action(self):
    #     while 1:
    #         if self.action is not None:
    #             break
    #
    #     # Returns a tuple (action, bet)
    #     if self.action == 'call':
    #         if self.game is not None:
    #             self.action_bet = max(self.game.user.bet, self.game.bot.bet)
    #
    #     act, bet = self.action, self.action_bet
    #     self.action, self.action_bet = None, None
    #
    #     return act, bet


class Game:
    # This class is implemented only for heads-up poker
    def __init__(self, frame=None, window=None):
        # Pointer to the frame
        self.frame = frame
        self.window = window

        # Parameters of the game
        if self.frame and self.window:
            self.starting_chips = self.window.settings_frame.starting_chips.get()
            self.small_blind = self.window.settings_frame.blind_size.get()
            self.increasing_blinds = self.window.settings_frame.blind_increase.get()
            self.playing_style = self.window.settings_frame.selected_style.get()
        else:
            self.starting_chips = 10000
            self.small_blind = 250
            self.increasing_blinds = 0
            self.playing_style = 'Optimal'

        # User
        self.user = User()
        self.user.game = self
        self.user.chips = self.starting_chips

        # Bot
        self.bot = Bot()
        self.bot.game = self
        self.bot.chips = self.starting_chips
        self.bot.style = self.playing_style

        # Data Writting
        self.player_chips = {'chip_start': self.starting_chips,
                             'Player1': [self.user.chips],
                             'Player2': [self.bot.chips]}
        self.date = datetime.datetime.today()
        self.file_name = f'Game_from_{self.date.strftime("%Y-%m-%d")}_at_{self.date.strftime("%H-%M")}.txt'
        self.data = StoreData(self.player_chips, self.user.name, self.bot.name, self.file_name)

        # Positions distribution
        self.players = [self.bot, self.user]
        random.shuffle(self.players)
        self.sb_pos = 0
        self.bb_pos = 1

        # Cards
        self.deck = Deck()
        random.shuffle(self.deck)

        self.cards_for_current_hand = random.sample(self.deck, 9)
        self.community_cards = []

        # Bets
        self.big_blind = 2 * self.small_blind
        self.min_bet = self.big_blind
        self.user.bet = 0
        self.bot.bet = 0
        self.pot = 0
        self.winner = None


    def play(self):
        # Messages about game initialization
        print(f':::: New Game: {self.date.strftime("%Y-%m-%d-%H-%M")}')
        print(f':::: Bot Playing Style: {self.bot.style}')

        i = 1
        StoreData.get_header_data(self.data)
        while self.user.chips > 0 and self.bot.chips > 0:
            print(f':::: Hand #{i}')
            print()
            if self.frame:
                self.frame.update()
            # Preflop
            self.players[self.sb_pos].make_bet(self.small_blind)
            print(f':::: SB: {self.players[self.sb_pos].name}')

            self.players[self.bb_pos].make_bet(self.big_blind)
            print(f':::: BB: {self.players[self.bb_pos].name}')
            if self.frame:
                self.frame.update()

            self.deal_hole_cards()
            self.bot.update_info_set()
            print(f':::: Dealing hole cards: {self.user.name} - {[str(card) for card in self.user.hole_cards]}, {self.bot.name} - {[str(card) for card in self.bot.hole_cards]}')
            print()
            print(f':::: Preflop')

            if self.bidding(preflop=True):
                self.deal_community_cards(3)
                self.bot.update_info_set()
                print()
                print(f':::: Flop: {[str(card) for card in self.community_cards]}')
                if self.frame:
                    self.frame.update()
                if self.bidding():
                    self.deal_community_cards(1)
                    self.bot.update_info_set()
                    print()
                    print(f':::: Turn: {[str(card) for card in self.community_cards]}')
                    if self.frame:
                        self.frame.update()
                    if self.bidding():
                        self.deal_community_cards(1)
                        self.bot.update_info_set()
                        print()
                        print(f':::: River: {[str(card) for card in self.community_cards]}')
                        if self.frame:
                            self.frame.update()
                        if self.bidding():
                            print()
                            print(":::: Showdown:")
                            self.winner = self.determine_winner()
                            if self.frame:
                                self.frame.update()
                        else:
                            self.winner = self.post_fold_determine_winner()
                            if self.frame:
                                self.frame.update()
                    else:
                        self.winner = self.post_fold_determine_winner()
                        if self.frame:
                            self.frame.update()
                else:
                    self.winner = self.post_fold_determine_winner()
                    if self.frame:
                        self.frame.update()
            else:
                self.winner = self.post_fold_determine_winner()
                if self.frame:
                    self.frame.update()

            if self.winner is not None:
                print(f':::: Winner: {self.winner.name}')
                self.winner.chips += self.pot
                if self.frame:
                    self.frame.update()
            else:
                print()
                print(f':::: It is a draw')
                self.user.chips += self.pot//2
                self.bot.chips += self.pot//2
                if self.frame:
                    self.frame.update()

            self.player_chips['Player1'].append(self.user.chips)
            self.player_chips['Player2'].append(self.bot.chips)

            print(f':::: End of the hand: {self.user.name} - {self.user.chips} chips | {self.bot.name} - {self.bot.chips} chips')
            print()
            self.swap_positions()
            self.clear()
            i += 1
            if self.frame:
                self.frame.update()
        print(self.player_chips)
        StoreData.write_to_file(self.data)

        if self.user.chips <= 0:
            print(":::: Game over! You ran out of chips.")
        else:
            print(":::: Congratulations! You defeated the bot.")

    def clear(self):
        self.community_cards = []
        self.cards_for_current_hand = random.sample(self.deck, 9)
        self.pot = 0

        self.user.bet = 0
        self.user.hole_cards = []
        self.user.fold = False

        self.bot.bet = 0
        self.bot.hole_cards = []
        self.bot.fold = False
        self.bot.info_set = ''

        self.winner = None

    def deal_hole_cards(self):
        for i in range(2):
            self.players[i].hole_cards = self.cards_for_current_hand[0:2]
            del self.cards_for_current_hand[:2]

    def deal_community_cards(self, num):
        self.community_cards.extend(self.cards_for_current_hand[:num])
        del self.cards_for_current_hand[:num]

    def swap_positions(self):
        self.sb_pos, self.bb_pos = self.bb_pos, self.sb_pos

    def bidding(self, preflop=False):
        """
        :param preflop: determines game stage
        :return: False if fold, True otherwise
        """
        if preflop:
            i = self.sb_pos
            player = self.players[i]  # SB at preflop
            opponent = self.players[not i]  # BB at preflop

            # Cases if a player is all-in because of blinds
            if player.chips == 0:
                print(f':::: {self.user.name} bet: {self.user.bet} | {self.bot.name} bet: {self.bot.bet} | total: {self.pot}')
                print(f'{player.name} is already all-in')
                return True

            elif opponent.chips == 0:
                print(f':::: {self.user.name} bet: {self.user.bet} | {self.bot.name} bet: {self.bot.bet} | total: {self.pot}')
                act, bet = player.ask_action()
                if act == 'call':
                    # Bet the full big blind
                    player.make_bet(self.big_blind - player.bet)
                    print(f'{opponent.name} is already all-in')
                    self.bot.info_set += 'c'
                    return True
                elif act == 'fold':
                    player.fold = True
                    print(f'{player.name} has folded')
                    self.bot.info_set += 'p'
                    return False
                else:
                    raise ValueError('Invalid action')
        else:
            i = self.bb_pos
            player = self.players[i]
            opponent = self.players[not i]

            # Case if a player is all-in from the previous bidding
            if player.chips == 0 or opponent.chips == 0:
                print('There is a player already all in')
                return True

        # Usual bidding
        asked = 0
        while True:
            print(f':::: {self.user.name} bet: {self.user.bet} | {self.bot.name} bet: {self.bot.bet} | total: {self.pot}')

            act, bet = player.ask_action()
            asked += 1

            if act == 'fold':
                player.fold = True
                print(f'{player.name} has folded')
                self.bot.info_set += 'p'
                return False

            elif act == 'check':
                if player.bet != opponent.bet:
                    raise ValueError('Invalid action')
                else:
                    self.bot.info_set += 'p'
                    if asked >= 2:
                        return True

            elif act == 'call':
                if player.bet < opponent.bet:
                    self.bot.info_set += 'c'
                    player.make_bet(opponent.bet - player.bet)
                else:
                    raise ValueError('Invalid action')
                if asked >= 2:
                    return True

            elif act == 'raise':
                if opponent.chips == 0:
                    raise ValueError('Invalid action')

                if self.min_bet <= bet < player.chips and opponent.bet - player.bet < bet:
                    # Usual case, bet is greater than minimum bet
                    player.make_bet(bet)
                    self.bot.info_set += 'b'
                elif bet == player.chips and opponent.bet - player.bet < bet:
                    # All in case, bet can be less than minimum bet
                    player.make_bet(bet)
                    self.bot.info_set += 'b'
                else:
                    raise ValueError('Invalid action')

            else:
                raise ValueError('Invalid action')

            # Ask next
            i = not i
            player = self.players[i]
            opponent = self.players[not i]

    def determine_winner(self):
        winner = None

        combinations = {1: 'high card', 2: 'pair', 3: 'two pairs', 4: 'three of a kind', 5: 'straight', 6: 'flush',
                        7: 'full house', 8: 'four of a kind', 9: 'straight flush', 10: 'royal flush'}

        user_hand = sorted(self.user.hole_cards + self.community_cards, key=lambda x: x.rank)
        user_combo = self.evaluate_hand(user_hand)
        print(f'{self.user.name} has {combinations[user_combo[0]]}')

        bot_hand = sorted(self.bot.hole_cards + self.community_cards, key=lambda x: x.rank)
        bot_combo = self.evaluate_hand(bot_hand)
        print(f'{self.bot.name} has {combinations[bot_combo[0]]}')

        if user_combo[0] > bot_combo[0]:
            winner = self.user
        elif bot_combo[0] > user_combo[0]:
            winner = self.bot
        else:
            # Equal combinations
            if user_combo[0] == 1:
                # High card
                winner = self.compare_kicker()

            elif user_combo[0] == 2 or user_combo[0] == 4 or user_combo[0] == 8:
                # Pair or three of kind or four of kind
                if user_combo[1] > bot_combo[1]:
                    winner = self.user
                elif user_combo[1] < bot_combo[1]:
                    winner = self.bot
                else:
                    winner = self.compare_kicker()

            elif user_combo[0] == 3 or user_combo[0] == 7:
                # Two pairs or full house
                if user_combo[1][0] > bot_combo[1][0]:
                    winner = self.user
                elif user_combo[1][0] < bot_combo[1][0]:
                    winner = self.bot
                else:
                    if user_combo[1][1] > bot_combo[1][1]:
                        winner = self.user
                    elif user_combo[1][1] < bot_combo[1][1]:
                        winner = self.bot
                    else:
                        winner = self.compare_kicker()

            elif user_combo[0] == 5 or user_combo[0] == 9:
                # Straight or straight flush
                if user_combo[1] > bot_combo[1]:
                    winner = self.user
                elif user_combo[1] < bot_combo[1]:
                    winner = self.bot
                else:
                    winner = self.compare_kicker()

            elif user_combo[0] == 6:
                # Flush
                for i in range(5):
                    if user_combo[1][i] > bot_combo[1][i]:
                        winner = self.user
                        break
                    if bot_combo[1][i] > user_combo[1][i]:
                        winner = self.bot
                        break

                if winner is None:
                    winner = self.compare_kicker()

            elif user_combo[0] == 10:
                # Royal flush
                winner = self.compare_kicker()

        return winner

    def post_fold_determine_winner(self):
        if self.user.fold:
            return self.bot
        else:
            return self.user

    def evaluate_hand(self, sorted_cards):
        # Cards are sorted by ascending rank
        combo = self.royal_flush(sorted_cards)
        if combo is None:
            combo = self.straight_flush(sorted_cards)
            if combo is None:
                combo = self.four_of_kind(sorted_cards)
                if combo is None:
                    combo = self.full_house(sorted_cards)
                    if combo is None:
                        combo = self.flush(sorted_cards)
                        if combo is None:
                            combo = self.straight(sorted_cards)
                            if combo is None:
                                combo = self.three_of_kind(sorted_cards)
                                if combo is None:
                                    combo = self.pair_or_two(sorted_cards)
                                    if combo is None:
                                        # High card
                                        combo = (1, 0)
        return combo

    def royal_flush(self, cards):
        # Cards are sorted by ascending rank
        if self.straight_flush(cards[2:]):
            if cards[-1].rank == 14:
                return 10, 0
        return None

    def straight_flush(self, cards):
        # Cards are sorted by ascending rank
        # The 'wheel' case: A2345
        cards2 = copy.deepcopy(cards)
        if cards2[-1].rank == 14:
            cards2.insert(0, Card(rank=1, suit=cards2[-1].suit))
            cards2[0].rank = 1

        count = 1
        max_count = 1
        max_card = None
        for i in range(0, len(cards2)-1):
            if cards2[i].rank - cards2[i + 1].rank == -1 and cards2[i].suit == cards2[i + 1].suit:
                count += 1
                max_count = max(max_count, count)
                max_card = cards2[i+1]
            else:
                count = 1
        if max_count >= 5:
            return 9, max_card.rank
        else:
            return None

    def four_of_kind(self, cards):
        # Cards are sorted by ascending rank
        for i in range(len(cards) - 3):
            if cards[i].rank == cards[i + 1].rank == cards[i + 2].rank == cards[i + 3].rank:
                return 8, cards[i].rank
        return None

    def full_house(self, cards):
        # Cards are sorted by ascending rank
        counts = {}
        for card in cards:
            rank = card.rank
            if rank in counts:
                counts[rank] += 1
            else:
                counts[rank] = 1

        counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

        if counts[0][1] >= 3 and counts[1][1] >= 2:
            return 7, [counts[0][0], counts[1][0]]

        return None

    def flush(self, cards):
        # Cards are sorted by ascending rank
        counts = {suit: [] for suit in range(4)}
        for card in cards:
            counts[card.suit].append(card.rank)

        max_count = max(len(suit_cards) for suit_cards in counts.values())
        if max_count >= 5:
            flush_suit = max(counts, key=lambda x: len(counts[x]))
            flush_ranks = sorted(counts[flush_suit], reverse=True)
            # Ranks are sorted by descending order
            return 6, flush_ranks, flush_suit
        else:
            return None

    def straight(self, cards):
        # Cards are sorted by ascending rank
        # The 'wheel' case: A2345
        cards2 = copy.deepcopy(cards)
        if cards2[-1].rank == 14:
            cards2.insert(0, Card(rank=1, suit=cards2[-1].suit))
            cards2[0].rank = 1

        count = 1
        max_count = 1
        max_card = None
        for i in range(0, len(cards2) - 1):
            if cards2[i].rank - cards2[i + 1].rank == -1:
                count += 1
                max_count = max(max_count, count)
                max_card = cards2[i + 1]
            else:
                count = 1
        if max_count >= 5:
            return 5, max_card.rank
        else:
            return None

    def three_of_kind(self, cards):
        # Cards are sorted by ascending rank
        for i in range(len(cards) - 2):
            if cards[i].rank == cards[i + 1].rank == cards[i + 2].rank:
                return 4, cards[i].rank
        return None

    def pair_or_two(self, cards):
        # Cards are sorted by ascending rank
        pairs = []
        for i in range(len(cards) - 1):
            if cards[i].rank == cards[i + 1].rank:
                # In the result pairs are sorted by descending rank
                pairs.insert(0, cards[i].rank)
        if len(pairs) >= 2:
            return 3, pairs
        elif len(pairs) == 1:
            return 2, pairs[0]
        else:
            return None

    def compare_kicker(self):
        # Cards are sorted by descending rank
        user_cards = sorted(self.user.hole_cards, key=lambda x: x.rank, reverse=True)
        bot_cards = sorted(self.bot.hole_cards, key=lambda x: x.rank, reverse=True)
        winner = None

        if user_cards and bot_cards:
            if user_cards[0].rank > bot_cards[0].rank:
                winner = self.user
            elif user_cards[0].rank < bot_cards[0].rank:
                winner = self.bot
            else:
                if len(user_cards) > 1 and len(bot_cards) > 1:
                    if user_cards[1].rank > bot_cards[1].rank:
                        winner = self.user
                    elif user_cards[1].rank < bot_cards[1].rank:
                        winner = self.bot

        return winner


if __name__ == '__main__':
    game = Game()
    game.play()
