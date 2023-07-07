import unittest
from cards import *

class TestDeck(unittest.TestCase):
	def setUp(self):
		self.test_deck = Deck()
		self.starting_cards = self.test_deck.cards[:]

	def cards_match_start(self):
		return [ 1 if self.starting_cards[i] == card else 0 for i, card in enumerate(self.test_deck.cards) ]

	def test_shuffle_changes_most_positions(self):
		MAX_MATCH_PERCENT = 0.1
		NUM_TRIES = 3
		
		# shuffle the cards and test how many are in the same position as where they started.
		# not quite random, but this is the "something is better than nothing" answer
		for i in range(NUM_TRIES):
			self.test_deck.shuffle()
			cards_match = [ 1 if self.starting_cards[i] == card else 0 for i,card in enumerate(self.test_deck.cards) ]
			match_percent = sum(cards_match) / len(self.starting_cards)
			if match_percent <= MAX_MATCH_PERCENT:
				break
		self.assertLessEqual(match_percent, MAX_MATCH_PERCENT)

	def test_sort_cards_by_suit_then_value(self):
		sorted_cards = self.test_deck.sort_cards(self.test_deck.cards)
		cards_match = [self.starting_cards[i] == card for i, card in enumerate(sorted_cards)]
		self.assertTrue( all(cards_match) )


class TestDeckDeal(unittest.TestCase):
	def setUp(self):
		self.test_deck = Deck()
		self.test_hands = self.test_deck.deal()

	def test_deal_correct_num_cards(self):
		num_starting_cards = Deck.TOTAL_CARDS // Deck.DEFAULT_PLAYERS
		correct_num_cards = [ len(hand) == num_starting_cards for hand in self.test_hands ]
		self.assertTrue( all(correct_num_cards) )

	def test_none_remaining(self):
		self.assertEqual( len(self.test_deck.cards), 0 )

if __name__ == '__main__':
	unittest.main()