from game import *

new_game = Game()
last_lead = 0
lead_player = 0
for i in range(new_game.num_starting_cards):
	new_game.play_trick()