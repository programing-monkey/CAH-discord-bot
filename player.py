import typing
from user import CAH_User
from safe_dm import dm
class Player(object):
	"""docstring for Player"""
	def __init__(self, cah_user:CAH_User, parent_game):
		super(Player, self).__init__()
		self.parent_game = parent_game
		self.cah_user = cah_user
		self.cah_user.playing_as = self
		self.hand = []
		self.blackcards = []
		self.played_cards = []
		self.winnings = []
	@property
	def played_cards_as_text(self):
		return "\n".join(["\n"+card.text.replace("\n","\n> ") for card in played_cards])

	def playcards(self, card_ids:typing.List[int]):
		cards = []
		for card_id in card_ids:
			cards.append(self.hand[card_id-1])
		for card in cards:
			self.hand.remove(card)
		self.played_cards = cards
		
	def has_played(self):
		return len(self.played_cards) != 0

	def refill_hand(self):
		if len(self.hand) < 10:
			for _ in range(10 - len(self.hand)):
				self.hand.append(self.parent_game.draw_whitecard())

	async def show_hand(self):
		user = self.cah_user.discord_user
		await dm(user,"\n".join(["card #{card_id}:\n> {card}".format(card=self.hand[card_id].text.replace("\n","\n> "),card_id=card_id+1) for card_id in range(len(self.hand))]))