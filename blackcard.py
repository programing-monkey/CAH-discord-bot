from json_data import cards
class BlackCard(object):
	"""docstring for BlackCard"""
	def __init__(self, black_card_id:int, parent_deck = None):
		super(BlackCard, self).__init__()

		# corresponds to its position in the list of black cards located in the cards.json from lines 2 to 10851
		self.black_card_id = black_card_id

		# dict of {"text": some funny question with blanks in ____ places , "pick": number of blanks}
		self.json = cards["blackCards"][black_card_id]

		# adding the dict key/value pairs to the BlackCard object
		self.text = self.json["text"]
		self.pick = self.json["pick"]

		# adding a link to the parent deck used to initialize it
		self.parent_deck = parent_deck


		