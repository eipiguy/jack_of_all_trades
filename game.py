from cards import *

class Player:
	def __init__(self, name, position, starting_hand):
		self.name = name
		self.position = position
		self.hand = starting_hand
		self.tricks = []
		self.memory = [[]]

	def new_game(self, starting_hand):
		self.hand = starting_hand
		self.tricks = []
		self.memory.append([])

	def play(self, cur_trick):
		self.print
		legal_plays = self.hand
		legal_play_ids = range(len(legal_plays))
		lead_card = cur_trick.cards[cur_trick.lead]
		if lead_card != '':
			legal_plays, legal_play_ids = match_suit(lead_card, self.hand)
			if len(legal_plays) == 1:
				return self.hand.pop(legal_play_ids[0])
		
		# TODO: Make a choice
		choice_id = legal_play_ids[0]
		return self.hand.pop(choice_id)

	def memorize_trick(self, position, cards, lead):
		self.memory[-1].append([position, cards, lead])

	def print(self):
		print(f"Player name: {self.name}, cards remaining = {len(self.hand)}")
		print(f"Current hand: {self.hand}\n")


class Game:
	def __init__(self, num_players=4):
		self.deck = Deck()
		self.game_number = 0
		self.trick_number = 0
		self.lead_player = 0
		starting_hands = self.deck.deal(num_players, len(self.deck.cards))
		self.players = [ Player(f"Player_{i}", i, hand) for i, hand in enumerate(starting_hands) ]
		self.num_starting_cards = len(starting_hands[0])

	def play_trick(self):
		num_players = len(self.players)
		self.cur_trick = Trick(self.deck, num_players, self.lead_player)

		for i in range(num_players):
			self.cur_trick.play(self.players[self.cur_trick.cur_play].play(self.cur_trick))

		self.cur_trick.print()
		for i, player in enumerate(self.players):
			player.memorize_trick(i, self.cur_trick.cards, self.lead_player)
		self.lead_player = self.cur_trick.id_winning()
		self.trick_number += 1
