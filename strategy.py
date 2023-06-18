def match_suit(cards, lead_suit):
	legal_plays = []
	legal_play_ids = []
	for i, card in enumerate(cards):
		if card[-1] == lead_suit:
			legal_plays.append(card)
			legal_play_ids.append(i)

	if len(legal_plays) > 0:
		return legal_plays, legal_play_ids
	else:
		return cards, range(len(cards))

def list_followed_suit(cards, lead_id):
	lead_card = cards[lead_id]
	if lead_card == '':
		return [False] * len(cards) 
	return [ card[-1] == lead_card[-1] for card in cards ]