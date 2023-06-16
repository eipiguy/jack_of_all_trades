import random

SUITS = {'H', 'S', 'D', 'C'}
VALUES = ['9', 'T', 'J', 'Q', 'K', 'A']


class Deck:
	def __init__(self, values=VALUES, suits=SUITS):
		self.values_to_rank = {'9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
		self.ranks_to_values = {9:'9', 10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
		self.suits = {'H', 'S', 'D', 'C'}
		print(f"Values: {self.values_to_rank}")
		print(f"Values: {self.suits}")

		self.cards = []
		for suit in self.suits:
			for value in self.values_to_rank:
				self.cards.append(f"{value}{suit}")
		print(f"Starting deck: {self.cards}")

		self.shuffle()
		print(f"Shuffled deck: {self.cards}")

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self, num_players, num_cards):
		hands = [ [] for _ in range(num_players) ]
		for card_num in range(num_cards):
			hands[ card_num % num_players ].append(self.cards.pop(-1))
		return hands

	def sort_cards(self, cards):
		by_suit = {}
		suits = set()
		for card in cards:
			suits.add(card[-1])
		for suit in suits:
			by_suit[suit] = []

		for card in cards:
			by_suit[card[-1]].append(self.values_to_rank[card[0]])

		#for cards_in_suit in by_suit:
			#cards_in_suit.sort_by_value()
		
		sorted = []
		for sorted_suit in by_suit:
			by_suit[sorted_suit].sort(reverse=True)
			sorted.extend([
				self.ranks_to_values[value] + sorted_suit 
				for value in by_suit[sorted_suit] ])
		return sorted

class Game:
	def __init__(self, num_players = 4):
		self.deck = Deck()
		self.num_players = num_players
		self.hands = [ [] for _ in range(num_players) ]
	def deal(self):
		new_hands = self.deck.deal(self.num_players, len(self.deck.cards))
		print(f"Starting hands:")
		for i, new_hand in enumerate(new_hands):
			new_hand = self.deck.sort_cards(new_hand)
			print(new_hand)
			self.hands[i].extend(new_hand)