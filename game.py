from cards import *

class Player:
	def __init__(self, name, position, starting_hand):
		self.name = name
		self.position = position
		self.hand = starting_hand
		self.points = 0
		self.num_jacks = 0
		self.tricks = []
		self.memory = [[]]

	def new_game(self, starting_hand):
		self.hand = starting_hand
		self.tricks = []
		self.memory.append([])

	def bid(self):
		# TODO: Make a better bidding
		# strategy. For now always bids agressive
		return True

	def play(self, cur_trick):
		self.print()
		legal_plays = self.hand
		legal_play_ids = range( len(legal_plays) )
		lead_card = cur_trick.cards[ cur_trick.lead ]

		# if following,
		if lead_card != '':
			# filter the legal plays to match the lead suit
			# (this also handles the case when no cards match, returning the whole hand)
			legal_plays, legal_play_ids = match_suit(self.hand, lead_card[-1])

			# if only one legal play, then play it
			if len(legal_plays) == 1:
				return self.hand.pop( legal_play_ids[0] )

		# TODO: Make a choice strategy for picking the "best" plays
		# for now, this just picks the first card in the hand that's legal
		choice_id = legal_play_ids[0]
		return self.hand.pop( choice_id )

	def memorize_trick(self, position, cards, lead, trump):
		self.memory[-1].append([position, cards, lead, trump])

	def print(self):
		print(f"Player name: {self.name}, cards remaining = {len(self.hand)}")
		print(f"Current hand: {self.hand}")
		print(f"Jacks Won: {self.num_jacks}\n")


class Game:
	def __init__(self, num_players = 2, cards_per_player = 5):
		self.deck = Deck()
		self.game_number = 0
		self.bids = []
		self.trick_number = 0
		self.lead_player_id = 0
		self.trump = ''
		starting_hands = self.deck.deal(num_players, cards_per_player)
		self.players = [ Player(f"Player_{i}", i, hand) for i, hand in enumerate(starting_hands) ]
		self.num_starting_cards = len(starting_hands[0])

	# bid whether the player believes they will take the most jacks
	def bid( self ):
		self.bids = []
		for player in self.players:
			self.bids.append( player.bid() )

	# Request or play one card for each player,
	# managing trump and adding results to the appropriate variables.
	def play_trick(self):
		num_players = len(self.players)
		self.cur_trick = Trick( self.deck, num_players, self.lead_player_id, self.trump )
		self.trump = self.cur_trick.trump # once trump is set, it gets saved for future tricks

		# request a card from each player in turn
		for i in range(num_players):
			current_player_id = self.cur_trick.cur_player_id
			current_player = self.players[ current_player_id ]
			
			# given the current play information,
			# get the card the current player wishes to play
			card_choice = current_player.play( self.cur_trick )

			# append the resulting choice to the end of the trick
			self.cur_trick.play( card_choice )

		# once everyone has played a card,
		# record the resulting hand, and add it to each player's memory
		self.cur_trick.print()
		self.trump = self.cur_trick.trump
		for i, player in enumerate(self.players):
			player.memorize_trick(i, self.cur_trick.cards, self.lead_player_id, self.trump)

		# then determine the winner for the purposes of starting the next trick
		self.lead_player_id = self.cur_trick.id_winning()

		# assign them points equal to the number of jacks won in the trick
		self.players[ self.lead_player_id ].num_jacks += self.cur_trick.count_jacks()
		self.trick_number += 1

	def play_round( self ):
		# Bid, starting with lead
		# "Will you take the most jacks?"
		self.bid()

		for i in range( self.num_starting_cards ):
			self.play_trick()

		# What is the most jacks won amongst the players?
		most_jacks = 0
		for player in self.players:
			if player.num_jacks > most_jacks:
				most_jacks = player.num_jacks
		
		# give a point to the players with the most jacks and reset the jack count
		round_winners = []
		for i, player in enumerate( self.players ):
			if player.num_jacks == most_jacks:
				player.points += 1
				round_winners.append(i)
			player.num_jacks = 0

		# assign points for correct bids
		for i, player in enumerate( self.players ):
			# bid and made it
			if i in round_winners and player.bid:
				player.points += 1
			# bid nil and lost (as desired)
			if i not in round_winners and not player.bid:
				player.points += 1
