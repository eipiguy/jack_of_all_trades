import random
from strategy import *

class Deck:

	DEFAULT_PLAYERS = 4
	
	ID_TO_CARDINALS = { 0:'E', 1:'S', 2:'W', 3:'N' }
	CHARS_TO_RANKS = { 'A':14, 'K':13, 'Q':12, 'J':11, 'T':10, '9':9 }
	RANKS_TO_CHARS = { 14: 'A', 13:'K', 12:'Q', 11:'J', 10:'T', 9:'9' }
	SUITS = { 'H', 'S', 'D', 'C'}
	TOTAL_CARDS = len(SUITS) * len(CHARS_TO_RANKS)

	def __init__(self):
		self.cards = []
		for suit in self.SUITS:
			for value in self.CHARS_TO_RANKS:
				self.cards.append(f"{value}{suit}")

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self, num_players=DEFAULT_PLAYERS, num_cards=TOTAL_CARDS):
		hands = [ [] for _ in range(num_players) ]
		for card_num in range(num_cards):
			hands[ card_num % num_players ].append(self.cards.pop(-1))
		return hands

	def sort_cards(self, cards):
		by_suit = {}
		for suit in self.SUITS:
			by_suit[suit] = []

		for card in cards:
			by_suit[card[-1]].append(self.CHARS_TO_RANKS[card[0]])

		sorted = []
		for sorted_suit in by_suit:
			by_suit[sorted_suit].sort(reverse=True)
			sorted.extend([
				self.RANKS_TO_CHARS[value] + sorted_suit
				for value in by_suit[sorted_suit] ])
		return sorted

	def print(self):
		print(f"Values: {self.CHARS_TO_RANKS}")
		print(f"Values: {self.SUITS}")
		print(f"Remaining cards: {self.cards}")


class Trick:
	def __init__(self, deck, num_players, lead=0):
		self.game_deck = deck
		self.cards = [''] * num_players
		self.lead = lead
		self.cur_play = lead

	def determine_trump(self):
		num_players = len(self.cards)
		for i in range(num_players):
			cur_player = ( self.lead + i ) % num_players
			if self.cards[cur_player] == '':
				return ''
			elif self.cards[cur_player][0] == 'J':
				return self.cards[cur_player][-1]

	def list_played_trump(self):
		trump = self.determine_trump()
		return [ card[-1] == trump for card in self.cards ]

	def match_suit(self):
		lead_suit = '' if self.cards[self.lead] == '' else self.cards[self.lead][-1]
		return match_suit(self.cards, lead_suit)

	def list_followed_suit(self):
		return list_followed_suit(self.cards, self.lead)

	def id_winning(self):
		played_trump = self.list_played_trump()
		followed_suit = self.list_followed_suit()

		highest_rank = 0
		highest_rank_id = 0
		if any(played_trump):
			for i, card in enumerate(self.cards):
				if played_trump[i]:
					rank = Deck.CHARS_TO_RANKS[card[0]]
					if rank > highest_rank:
						highest_rank = rank
						highest_rank_id = i
		elif any(followed_suit):
			for i, card in enumerate(self.cards):
				if followed_suit[i]:
					rank = Deck.CHARS_TO_RANKS[card[0]]
					if rank > highest_rank:
						highest_rank = rank
						highest_rank_id = i
		return highest_rank_id

	def play(self, card):
		self.cards[self.cur_play] = card
		print(f"Player {self.cur_play} played a {card}!")
		self.cur_play = (self.cur_play + 1) % len(self.cards)

	def print(self):
		win_id = self.id_winning()
		print(f"Current trick: {self.cards}, Lead: {self.lead}, Trump: {self.determine_trump()}")
		print(f"Trump suit: {[ 'T' if trump else 'F' for trump in self.list_played_trump() ]}")
		print(f"Followed suit: {[ 'T' if followed else 'F' for followed in self.list_followed_suit() ]}")
		print(f"Player {win_id} won the trick with a {self.cards[win_id]}\n")
