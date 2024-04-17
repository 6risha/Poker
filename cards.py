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
                        if self.bidding():
                            print(":::: Showdown:")
                            self.divide_pot()
                        else:
                            self.post_fold_pot_division()
                    else:
                        self.post_fold_pot_division()
                else:
                    self.post_fold_pot_division()
            else:
                self.post_fold_pot_division()

            self.swap_positions()
            self.clear()
            i += 1

    def clear(self):
        self.community_cards = []
        self.cards_for_current_hand = random.sample(self.deck, 9)

        self.user.bet = 0
        self.user.hole_cards = []

        self.bot.bet = 0
        self.bot.hole_cards = []

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
                    return True
                elif act == 'fold':
                    print(f'{player.name} has folded')
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
                print(f'{player.name} has folded')
                return False

            elif act == 'check':
                if player.bet != opponent.bet:
                    raise ValueError('Invalid action')
                else:
                    if asked >= 2:
                        return True

            elif act == 'call':
                if player.bet < opponent.bet:
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
                elif bet == player.chips and opponent.bet - player.bet < bet:
                    # All in case, bet can be less than minimum bet
                    player.make_bet(bet)
                else:
                    raise ValueError('Invalid action')

            else:
                raise ValueError('Invalid action')

            # Ask next
            i = not i
            player = self.players[i]
            opponent = self.players[not i]

    def divide_pot(self):
        user_hand = self.evaluate_hand(self.user.hole_cards + self.community_cards)
        combinations = {1: 'high card', 2: 'pair', 3: 'two pairs', 4: 'three of a kind', 5: 'straignt', 6: 'flush',
                        7: 'full house', 8: 'four of a kind', 9: 'straight flush', 10: 'royal flush'}
        print(f'{self.user.name} has {combinations[user_hand]}')
        bot_hand = self.evaluate_hand(self.bot.hole_cards + self.community_cards)
        print(f'{self.bot.name} has {combinations[bot_hand]}')

        if user_hand > bot_hand:
            self.user.chips += self.pot
            print(f"{self.user.name} wins the pot!")
        elif bot_hand > user_hand:
            self.bot.chips += self.pot
            print(f"{self.bot.name} wins the pot!")
        else:
            # TODO: дописать деление банка для равных рук начиная со слабых
            self.user.chips += self.pot // 2
            self.bot.chips += self.pot // 2
            print("It's a draw! Pot is split evenly between players.")

        self.pot = 0

    def post_fold_pot_division(self):
        print('There was a fold!')
        # TODO: дописать выигрыш пота одному игроку


    def evaluate_hand(self, cards):
        sorted_cards = sorted(cards, key=lambda card: card.rank, reverse=True)

        if self.is_royal_flush(sorted_cards):
            return 10
        elif self.is_straight_flush(sorted_cards):
            return 9
        elif self.is_four_of_a_kind(sorted_cards):
            return 8
        elif self.is_full_house(sorted_cards):
            return 7
        elif self.is_flush(sorted_cards):
            return 6
        elif self.is_straight(sorted_cards):
            return 5
        elif self.is_three_of_a_kind(sorted_cards):
            return 4
        elif self.is_two_pair(sorted_cards):
            return 3
        elif self.is_one_pair(sorted_cards):
            return 2
        else:
            return 1

    def is_royal_flush(self, cards):
        if self.is_straight_flush(cards[:5]):
            if cards[0].rank == 14:
                return True
        return False

    def is_straight_flush(self, cards):
        # The 'wheel' case: 5432A
        cards2 = cards.copy()
        if cards2[0].rank == 14:
            cards2.append(cards2[0])
            cards2[-1].rank = 1

        count = 1
        max_count = 1
        for i in range(0, len(cards2)-1):
            if cards2[i].rank - cards2[i + 1].rank == -1 and cards2[i].suit == cards2[i + 1].suit:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 1
        return max_count >= 5

    def is_four_of_a_kind(self, cards):
        for i in range(len(cards) - 3):
            if cards[i].rank == cards[i + 1].rank == cards[i + 2].rank == cards[i + 3].rank:
                return True
        return False

    def is_full_house(self, cards):
        counts = {}
        for card in cards:
            rank = card.rank
            if rank in counts:
                counts[rank] += 1
            else:
                counts[rank] = 1

        has_three_of_a_kind = False
        has_pair = False

        for count in counts.values():
            if count == 3:
                has_three_of_a_kind = True
            elif count == 2:
                has_pair = True

        return has_three_of_a_kind and has_pair

    def is_flush(self, cards):
        counts = {suit: 0 for suit in range(4)}
        for card in cards:
            counts[card.suit] += 1
        return max(counts.values()) >= 5

    def is_straight(self, cards):
        # The 'wheel' case: 5432A
        cards2 = cards.copy()
        if cards2[0].rank == 14:
            cards2.append(cards2[0])
            cards2[-1].rank = 1

        count = 1
        max_count = 1
        for i in range(0, len(cards2) - 1):
            if cards2[i].rank - cards2[i + 1].rank == -1:
                count += 1
                max_count = max(max_count, count)
            else:
                count = 1
        return max_count >= 5

    def is_three_of_a_kind(self, cards):
        for i in range(len(cards) - 2):
            if cards[i].rank == cards[i + 1].rank == cards[i + 2].rank:
                return True
        return False

    def is_two_pair(self, cards):
        pairs = 0
        for i in range(len(cards) - 1):
            if cards[i].rank == cards[i + 1].rank:
                pairs += 1
        return pairs == 2

    def is_one_pair(self, cards):
        for i in range(len(cards) - 1):
            if cards[i].rank == cards[i + 1].rank:
                return True
        return False


if __name__ == '__main__':
    game = Game()
    game.play()
