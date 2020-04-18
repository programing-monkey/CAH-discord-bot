from json_data import cards
class WhiteCard(object):
	"""docstring for WhiteCard"""
	def __init__(self, white_card_id:int, parent_deck = None):
		super(WhiteCard, self).__init__()

		# corresponds to its position in the list of black cards located in the cards.json from lines 2 to 10851
		self.white_card_id = white_card_id


		# adding the dict key/value pair to the WhiteCard object
		self.text = cards["whiteCards"][white_card_id]

		# adding a link to the parent deck used to initialize it
		self.parent_deck = parent_deck
