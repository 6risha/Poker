from cards import *


def create_hand(cards: list[str]):
    res = []
    for card in cards:
        suit = ['♣', '♦', '♥', '♠'].index(card[-1])
        # All the symbols except the last one
        rank_str = card[:-1]
        if rank_str == '10':
            rank = 10
        else:
            rank = int(rank_str) if rank_str.isdigit() else {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank_str]
        res.append(Card(rank=rank, suit=suit))
    return sorted(res, key=lambda x: x.rank)


game = Game()

# print(':::: Test 1: Hand Evaluation')
# hand1 = create_hand(['8♣', 'A♦', 'A♥', '3♣', '5♦', '4♠', 'K♥'])
# print(game.evaluate_hand(hand1))  # Correct: (2, 14), a pair of aces
# print()
#
# print(':::: Test 2: Usual Combination Comparison')
# game.community_cards = create_hand(['10♠', '10♥', '4♠', '9♠', '5♦'])
# game.user.hole_cards = create_hand(['4♦', '2♠'])  # 2 pairs
# game.bot.hole_cards = create_hand(['5♠', '8♠'])  # flush
# game.divide_pot()  # Correct: Grisha (bot) wins the pot, because flush > 2 pairs
# print()
#
# print(':::: Test 3: Equal Combinations, High Card')
# game.community_cards = create_hand(['9♣', 'Q♣', '10♣', 'A♦', '4♥'])
# game.user.hole_cards = create_hand(['8♣', '5♦'])  # High card
# game.bot.hole_cards = create_hand(['8♣', '2♦'])  # High card
# game.divide_pot()  # Correct: Thomas (user) wins the pot, because 5 > 2
# print()
#
# print(':::: Test 4: Equal Combinations, Pair')
# game.community_cards = create_hand(['10♠', '2♥', '4♥', '9♠', '5♦'])
# game.user.hole_cards = create_hand(['J♦', '2♠'])  # pair
# game.bot.hole_cards = create_hand(['5♠', '8♠'])  # pair
# game.divide_pot()  # Correct: Thomas (user) wins the pot, because 5 > 2
# print()
#
# print(':::: Test 5: Equal Combinations, Two Pairs')
# game.community_cards = create_hand(['K♥', '2♥', '2♠', '9♠', '5♦'])
# game.user.hole_cards = create_hand(['K♦', '3♠'])  # 2 pairs
# game.bot.hole_cards = create_hand(['5♠', '8♠'])  # 2 pairs
# game.divide_pot()  # Correct: Thomas (user) wins the pot, because K > 5
# print()

print(':::: Test 5: Equal Combinations, Three Pairs')
# TODO: wrong result here
game.community_cards = create_hand(['2♥', 'K♥', '4♠', 'K♠', '5♦'])
game.user.hole_cards = create_hand(['2♦', '5♠'])
game.bot.hole_cards = create_hand(['4♠', '5♥'])
game.divide_pot()
print()


