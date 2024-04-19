from cards import *


def create_hand(cards: list[str]) -> list[Card]:
    res = []
    for card in cards:
        suit = ['♣', '♦', '♥', '♠'].index(card[-1])
        rank_str = card[:-1]
        rank = int(rank_str) if rank_str.isdigit() else {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank_str]
        res.append(Card(rank=rank, suit=suit))
    return sorted(res, key=lambda x: x.rank)


if __name__ == '__main__':
    game = Game()

    # Test Different Combinations: High Card vs One Pair
    game.community_cards = create_hand(['3♠', '7♦', '9♠', '10♣', 'Q♠'])
    game.user.hole_cards = create_hand(['K♦', '5♣'])  # high card
    game.bot.hole_cards = create_hand(['5♠', '5♥'])  # one pair
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot with one pair
    assert game.winner == game.bot

    # Test Different Combinations: Two Pairs vs Three of a Kind
    game.community_cards = create_hand(['2♠', '7♦', '2♦', '10♣', 'Q♠'])
    game.user.hole_cards = create_hand(['K♦', 'K♠'])  # two pairs
    game.bot.hole_cards = create_hand(['5♠', '5♥'])  # three of a kind
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot with two pairs
    assert game.winner == game.user

    # Test Different Combinations: Straight vs Flush
    game.community_cards = create_hand(['9♠', '10♠', 'J♠', 'Q♠', 'K♠'])
    game.user.hole_cards = create_hand(['8♣', '7♦'])  # straight
    game.bot.hole_cards = create_hand(['A♠', '5♠'])  # flush
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot with flush
    assert game.winner == game.bot

    # Test Different Combinations: Full House vs Four of a Kind
    game.community_cards = create_hand(['2♠', '2♦', '2♣', 'Q♠', 'Q♦'])
    game.user.hole_cards = create_hand(['Q♣', 'Q♥'])  # four of kind
    game.bot.hole_cards = create_hand(['A♠', 'A♥'])  # full House
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot with four of a kind
    assert game.winner == game.user

    # Test Different Combinations: Straight Flush vs Royal Flush
    game.community_cards = create_hand(['9♠', '10♠', 'J♠', 'Q♠', 'K♠'])
    game.user.hole_cards = create_hand(['8♠', '7♠'])  # Straight flush
    game.bot.hole_cards = create_hand(['A♠', '10♠'])  # Royal flush
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot with royal flush
    assert game.winner == game.bot

    # Test Different Combinations: High Card vs Royal Flush
    game.community_cards = create_hand(['3♠', '7♦', '9♠', '10♣', 'Q♠'])
    game.user.hole_cards = create_hand(['K♦', '5♣'])  # High card
    game.bot.hole_cards = create_hand(['10♠', 'J♠'])  # Royal flush
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot with royal flush
    assert game.winner == game.bot

    # Test Different Combinations: Flush vs Straight
    game.community_cards = create_hand(['2♠', '2♦', '2♣', 'Q♠', 'Q♦'])
    game.user.hole_cards = create_hand(['Q♣', 'Q♥'])  # Full house
    game.bot.hole_cards = create_hand(['8♣', '7♦'])  # Straight
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot with full house
    assert game.winner == game.user

    # Test Usual Combination Comparison
    game.community_cards = create_hand(['10♠', '10♥', '4♠', '9♠', '5♦'])
    game.user.hole_cards = create_hand(['4♦', '2♠'])  # 2 pairs
    game.bot.hole_cards = create_hand(['5♠', '8♠'])  # flush
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot, because flush > 2 pairs
    assert game.winner == game.bot

    # Test Equal Combinations, High Card
    game.community_cards = create_hand(['9♣', 'Q♣', '10♣', 'A♦', '4♥'])
    game.user.hole_cards = create_hand(['8♣', '2♦'])  # High card
    game.bot.hole_cards = create_hand(['8♣', '5♦'])  # High card
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot, because 5 > 2
    assert game.winner == game.bot

    # Test Equal Combinations, Pair
    game.community_cards = create_hand(['10♠', '2♥', '4♥', '9♠', '5♦'])
    game.user.hole_cards = create_hand(['J♦', '2♠'])  # pair
    game.bot.hole_cards = create_hand(['5♠', '8♠'])  # pair
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot, because 5 > 2
    assert game.winner == game.bot

    # Test Equal Combinations, Three of Kind
    game.community_cards = create_hand(['J♠', 'J♥', '4♥', '9♠', '5♦'])
    game.user.hole_cards = create_hand(['J♦', '7♠'])  # pair
    game.bot.hole_cards = create_hand(['J♣', '8♠'])  # pair
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot, because 8 > 7
    assert game.winner == game.bot

    # Test Equal Combinations, Four of Kind
    game.community_cards = create_hand(['Q♣', 'A♥', 'Q♥', 'Q♠', 'A♣'])
    game.user.hole_cards = create_hand(['Q♦', '2♠'])  # four of kind
    game.bot.hole_cards = create_hand(['A♠', 'A♦'])  # four of kind
    game.winner = game.determine_winner()  # Correct: Grisha (bot) wins the pot, because A > Q
    assert game.winner == game.bot

    # Test Equal Combinations, Two Pairs
    game.community_cards = create_hand(['K♥', '2♥', '2♠', '9♠', '5♦'])
    game.user.hole_cards = create_hand(['K♦', '8♠'])  # 2 pairs
    game.bot.hole_cards = create_hand(['5♠', '3♠'])  # 2 pairs
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot, because K > 5
    assert game.winner == game.user

    # Test Equal Combinations, Three Pairs
    game.community_cards = create_hand(['2♥', 'K♥', '4♥', 'K♠', '5♦'])
    game.user.hole_cards = create_hand(['4♦', '5♠'])
    game.bot.hole_cards = create_hand(['2♠', '5♥'])
    game.winner = game.determine_winner()
    assert game.winner == game.user  # Correct: Thomas (user) wins the pot, because 4 > 2

    # Test Equal Combinations, Full House
    game.community_cards = create_hand(['2♥', 'K♥', '4♥', '5♦', '5♦'])
    game.user.hole_cards = create_hand(['4♠', '5♥'])  # full house
    game.bot.hole_cards = create_hand(['2♦', '5♠'])  # full house
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot, because 4 > 2
    assert game.winner == game.user

    # Test Equal Combinations, Flush
    game.community_cards = create_hand(['10♠', '4♠', '8♠', '2♠', '6♠'])
    game.user.hole_cards = create_hand(['K♠', 'Q♠'])  # flush
    game.bot.hole_cards = create_hand(['A♣', '5♦'])  # flush
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot, because K > 10
    assert game.winner == game.user

    # Test Equal Combinations, Straight
    game.community_cards = create_hand(['9♠', '10♣', 'J♦', 'Q♠', 'K♥'])
    game.user.hole_cards = create_hand(['8♣', '7♦'])  # straight
    game.bot.hole_cards = create_hand(['7♠', '6♠'])  # straight
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot, because 8 > 7
    assert game.winner == game.user

    # Test Equal Combinations, Straight Flush
    game.community_cards = create_hand(['9♠', '10♠', 'J♠', 'Q♠', 'K♠'])
    game.user.hole_cards = create_hand(['8♠', '7♠'])  # straight flush
    game.bot.hole_cards = create_hand(['7♠', '6♠'])  # straight flush
    game.winner = game.determine_winner()  # Correct: Thomas (user) wins the pot, because 8 > 7
    assert game.winner == game.user

    # Test Equal Combinations, Royal Flush
    game.community_cards = create_hand(['10♠', 'Q♠', 'K♠', 'A♠', 'J♠'])
    game.user.hole_cards = create_hand(['9♦', '8♠'])  # royal flush
    game.bot.hole_cards = create_hand(['9♠', '8♦'])  # royal flush
    game.winner = game.determine_winner()  # No winner, both have royal flush
    assert game.winner is None
