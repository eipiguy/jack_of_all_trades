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

	def deal( self, num_players = DEFAULT_PLAYERS, num_cards = TOTAL_CARDS ):
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
	def __init__( self, deck, num_players, lead = 0, trump = '' ):
		self.game_deck = deck
		self.cards = [''] * num_players
		self.lead = lead
		self.cur_player_id = lead
		self.trump = trump

	def determine_trump(self):
		num_players = len(self.cards)
		for i in range(num_players):
			check_player = ( self.lead + i ) % num_players
			if self.cards[check_player] == '':
				return ''
			elif self.cards[check_player][0] == 'J':
				return self.cards[check_player][-1]
		return ''

	def list_played_trump(self):
		if self.trump == '':
			self.trump = self.determine_trump()
		return [ card[-1] == self.trump for card in self.cards ]

	def match_suit(self):
		lead_suit = '' if self.cards[self.lead] == '' else self.cards[self.lead][-1]
		return match_suit(self.cards, lead_suit)

	def list_followed_suit(self):
		return list_followed_suit(self.cards, self.lead)

	def check_highest( self, valid_list ):
		highest_rank = 0
		highest_rank_id = 0
		for i, card in enumerate(self.cards):
			if valid_list[i]:
				rank = Deck.CHARS_TO_RANKS[card[0]]
				if rank > highest_rank:
					highest_rank = rank
					highest_rank_id = i
		return highest_rank_id, highest_rank

	def id_winning(self):
		played_trump = self.list_played_trump()
		followed_suit = self.list_followed_suit()

		highest_rank_id = 0
		if any(played_trump):
			# if anyone played trump, highest trump wins
			highest_rank_id, _ = self.check_highest(played_trump)
		elif any(followed_suit):
			# if no one played trump, highest led suit wins
			highest_rank_id, _ = self.check_highest(followed_suit)
		return highest_rank_id

	def play(self, card):
		self.cards[self.cur_player_id] = card
		print(f"Player ID {self.cur_player_id} played a {card}!\n")
		self.cur_player_id = (self.cur_player_id + 1) % len(self.cards)

	def print(self):
		win_id = self.id_winning()
		print(f"Current Trick: {self.cards}, Lead: {self.lead}, Trump: {self.trump}")
		print(f"Played Trump: {[ 'Y' if trump else 'N' for trump in self.list_played_trump() ]}")
		print(f"Followed Suit: {[ 'Y' if followed else 'N' for followed in self.list_followed_suit() ]}")
		print(f"Player ID {win_id} won the trick with a {self.cards[win_id]}\n")
