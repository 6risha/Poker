import unittest
from cards import *


def create_hand(cards: list[str]) -> list[Card]:
    res = []
    for card in cards:
        suit = ['♣', '♦', '♥', '♠'].index(card[-1])
        rank_str = card[:-1]
        rank = int(rank_str) if rank_str.isdigit() else {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank_str]
        res.append(Card(rank=rank, suit=suit))
    return sorted(res, key=lambda x: x.rank)


class TestPokerGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_high_card_vs_one_pair(self):
        self.game.community_cards = create_hand(['3♠', '7♦', '9♠', '10♣', 'Q♠'])
        self.game.user.hole_cards = create_hand(['K♦', '5♣'])  # high card
        self.game.bot.hole_cards = create_hand(['5♠', '5♥'])  # one pair
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_two_pairs_vs_three_of_a_kind(self):
        self.game.community_cards = create_hand(['2♠', '7♦', '2♦', '10♣', 'Q♠'])
        self.game.user.hole_cards = create_hand(['K♦', 'K♠'])  # two pairs
        self.game.bot.hole_cards = create_hand(['5♠', '5♥'])  # three of a kind
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_straight_vs_flush(self):
        self.game.community_cards = create_hand(['9♠', '10♠', 'J♠', 'Q♠', 'K♠'])
        self.game.user.hole_cards = create_hand(['8♣', '7♦'])  # straight
        self.game.bot.hole_cards = create_hand(['A♠', '5♠'])  # flush
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_full_house_vs_four_of_a_kind(self):
        self.game.community_cards = create_hand(['2♠', '2♦', '2♣', 'Q♠', 'Q♦'])
        self.game.user.hole_cards = create_hand(['Q♣', 'Q♥'])  # four of kind
        self.game.bot.hole_cards = create_hand(['A♠', 'A♥'])  # full House
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_straight_flush_vs_royal_flush(self):
        self.game.community_cards = create_hand(['9♠', '10♠', 'J♠', 'Q♠', 'K♠'])
        self.game.user.hole_cards = create_hand(['8♠', '7♠'])  # Straight flush
        self.game.bot.hole_cards = create_hand(['A♠', '10♠'])  # Royal flush
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_high_card_vs_royal_flush(self):
        self.game.community_cards = create_hand(['3♠', '7♦', '9♠', '10♣', 'Q♠'])
        self.game.user.hole_cards = create_hand(['K♦', '5♣'])  # High card
        self.game.bot.hole_cards = create_hand(['10♠', 'J♠'])  # Royal flush
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_flush_vs_straight(self):
        self.game.community_cards = create_hand(['2♠', '2♦', '2♣', 'Q♠', 'Q♦'])
        self.game.user.hole_cards = create_hand(['Q♣', 'Q♥'])  # Full house
        self.game.bot.hole_cards = create_hand(['8♣', '7♦'])  # Straight
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_usual_combination_comparison(self):
        self.game.community_cards = create_hand(['10♠', '10♥', '4♠', '9♠', '5♦'])
        self.game.user.hole_cards = create_hand(['4♦', '2♠'])  # 2 pairs
        self.game.bot.hole_cards = create_hand(['5♠', '8♠'])  # flush
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_equal_combinations_high_card(self):
        self.game.community_cards = create_hand(['9♣', 'Q♣', '10♣', 'A♦', '4♥'])
        self.game.user.hole_cards = create_hand(['8♣', '2♦'])  # High card
        self.game.bot.hole_cards = create_hand(['8♣', '5♦'])  # High card
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_equal_combinations_pair(self):
        self.game.community_cards = create_hand(['10♠', '2♥', '4♥', '9♠', '5♦'])
        self.game.user.hole_cards = create_hand(['J♦', '2♠'])  # pair
        self.game.bot.hole_cards = create_hand(['5♠', '8♠'])  # pair
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_equal_combinations_three_of_kind(self):
        self.game.community_cards = create_hand(['J♠', 'J♥', '4♥', '9♠', '5♦'])
        self.game.user.hole_cards = create_hand(['J♦', '7♠'])  # pair
        self.game.bot.hole_cards = create_hand(['J♣', '8♠'])  # pair
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_equal_combinations_four_of_kind(self):
        self.game.community_cards = create_hand(['Q♣', 'A♥', 'Q♥', 'Q♠', 'A♣'])
        self.game.user.hole_cards = create_hand(['Q♦', '2♠'])  # four of kind
        self.game.bot.hole_cards = create_hand(['A♠', 'A♦'])  # four of kind
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.bot)

    def test_equal_combinations_two_pairs(self):
        self.game.community_cards = create_hand(['K♥', '2♥', '2♠', '9♠', '5♦'])
        self.game.user.hole_cards = create_hand(['K♦', '8♠'])  # 2 pairs
        self.game.bot.hole_cards = create_hand(['5♠', '3♠'])  # 2 pairs
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_equal_combinations_three_pairs(self):
        self.game.community_cards = create_hand(['2♥', 'K♥', '4♥', 'K♠', '5♦'])
        self.game.user.hole_cards = create_hand(['4♦', '5♠'])
        self.game.bot.hole_cards = create_hand(['2♠', '5♥'])
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_equal_combinations_full_house(self):
        self.game.community_cards = create_hand(['2♥', 'K♥', '4♥', '5♦', '5♦'])
        self.game.user.hole_cards = create_hand(['4♠', '5♥'])  # full house
        self.game.bot.hole_cards = create_hand(['2♦', '5♠'])  # full house
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_equal_combinations_flush(self):
        self.game.community_cards = create_hand(['10♠', '4♠', '8♠', '2♠', '6♠'])
        self.game.user.hole_cards = create_hand(['K♠', 'Q♠'])  # flush
        self.game.bot.hole_cards = create_hand(['A♣', '5♦'])  # flush
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_equal_combinations_straight(self):
        self.game.community_cards = create_hand(['9♠', '10♣', 'J♦', 'Q♠', 'K♥'])
        self.game.user.hole_cards = create_hand(['8♣', '7♦'])  # straight
        self.game.bot.hole_cards = create_hand(['7♠', '6♠'])  # straight
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_equal_combinations_straight_flush(self):
        self.game.community_cards = create_hand(['9♠', '10♠', 'J♠', 'Q♠', 'K♠'])
        self.game.user.hole_cards = create_hand(['8♠', '7♠'])  # straight flush
        self.game.bot.hole_cards = create_hand(['7♠', '6♠'])  # straight flush
        self.game.winner = self.game.determine_winner()
        self.assertEqual(self.game.winner, self.game.user)

    def test_equal_combinations_royal_flush(self):
        self.game.community_cards = create_hand(['10♠', 'Q♠', 'K♠', 'A♠', 'J♠'])
        self.game.user.hole_cards = create_hand(['9♦', '8♠'])  # royal flush
        self.game.bot.hole_cards = create_hand(['9♠', '8♦'])  # royal flush
        self.game.winner = self.game.determine_winner()
        self.assertIsNone(self.game.winner)  # No winner, both have royal flush


if __name__ == '__main__':
    unittest.main()
