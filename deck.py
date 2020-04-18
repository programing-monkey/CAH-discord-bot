from json_data import cards
from blackcard import BlackCard
from whitecard import WhiteCard
class Deck(object):
	"""docstring for Deck"""
	def __init__(self, deck_id:str="Base"):
		super(Deck, self).__init__()

		# corresponds to the "key" used for identification in the list of decks located in the cards.json from lines 18081 to 28971
		self.deck_id = deck_id

		# dict of   {"name": the name of the deck, "black": [1, 2, 3, ...], "white": [1, 2, 3, ...]} and sometimes an additional key/value pair of {"icon": name of icon}
		self.json = cards[self.deck_id]
		self.name = self.json["name"]

		# generating a list of every relevent BlackCard object (BlackCard object located in blackcard.py)
		self.blackcards = []
		for black_card_id in self.json["black"]:
			self.blackcards.append(BlackCard(black_card_id, self))

		# generating a list of every relevent WhiteCard object (WhiteCard object located in whitecard.py)
		self.whitecards = []
		for white_card_id in self.json["white"]:
			self.whitecards.append(WhiteCard(white_card_id, self))

if __name__ == "__main__":
	my_deck = Deck("misprint")
	print(my_deck.deck_id,my_deck.json,my_deck.name)
	for card in my_deck.blackcards[0:10]:
		print(card.text,"takes",card.pick,"card(s)")
	for card in my_deck.whitecards[0:10]:
		print(card.text)
	#print(my_deck.blackcards)
