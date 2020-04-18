import random
from json_data import cards
from user import CAH_User
import typing
from deck import Deck
import sys
from safe_dm import dm
from discord.ext import commands
class CardsAgainstHumanity(object):
	"""docstring for CardsAgainstHumanity"""
	def __init__(self, owner:CAH_User, decks:typing.List[Deck], bot:commands.Bot):
		super(CardsAgainstHumanity, self).__init__()
		self.owner = owner
		self.decks = decks
		self.bot = bot
		self.unexpended_whitecards = []
		self.unexpended_blackcards = []
		self.players_static = []
		self.players = []
		self.invited = []
		self.judge = None
		self.prompting_blackcard = None
		self.in_session = False
		self.auto_read = None
		self.cardset_player_key = []

	async def start(self, random_order:bool=False, auto_read:bool=False):
		self.in_session = True
		self.auto_read = auto_read
		self.players = self.players_static.copy()
		if random_order:
			random.shuffle(self.players)
		for deck in self.decks:
			self.unexpended_whitecards += deck.whitecards
			self.unexpended_blackcards += deck.blackcards
		random.shuffle(self.unexpended_whitecards)
		random.shuffle(self.unexpended_blackcards)
		for player in self.players_static:
			player.refill_hand()
		await self.start_round()
	async def start_round(self):
		assert (self.prompting_blackcard == None),"something's wrong!"
		self.judge = self.players.pop(0)
		judge_user = self.judge.cah_user.discord_user

		for player in self.players_static:
			await player.show_hand()
		if self.auto_read:
			await dm(judge_user, "You are the judge!")
		else:
			await dm(judge_user, "You are the judge! type: \"!draw\" to draw a blackcard!")
		for player in self.players:
			user = player.cah_user.discord_user
			if self.auto_read:
				await dm(user, "{judge.name} is the judge.", judge=judge_user)
			else:
				await dm(user, "{judge.name} is the judge. Please wait for them to draw a blackcard!",judge=judge_user)
		if self.auto_read:
			self.draw_blackcard()
	async def collect(self):
		r = random.random()
		def ran():
			return r
		judge_user = self.judge.cah_user.discord_user
		list_sets_of_cards = []
		for player_id in range(len(self.players)):
			list_of_cards_as_text = []
			for card in self.players[player_id].played_cards:
				card_as_text = card.text.replace("\n","\n> ")
				list_of_cards_as_text.append(card_as_text)
			s = "set of cards #{brackets}:\n> {cards}".format(
				brackets = "{}",
				cards = "\n".join(list_of_cards_as_text)
			)
			list_sets_of_cards.append(s)
		self.cardset_player_key = self.players_static
		random.shuffle(self.cardset_player_key,ran)
		random.shuffle(list_sets_of_cards,ran)
		finished_string = "\n".join([list_sets_of_cards[i].format(i+1) for i in range(len(list_sets_of_cards))])
		await dm(judge_user,finished_string)
		
		if self.auto_read:
			for player in self.players_static:
				await dm(player.cah_user.discord_user,finished_string)
	async def pick(self,winner_id:int):
		game = games[ctx.author.id].playing_as.parent_game
		winner = game.cardset_player_key[winner_id-1]
		winner.winnings.append({"blackcard":self.prompting_blackcard,"response_cards":winner.played_cards})
		if self.auto_read:
			for player in players:
				if player == winner:
					dm(player.cah_user.discord_user,"You have won the round with:\n{winner.played_cards_as_text}",winner=winner)
				else:
					dm(player.cah_user.discord_user,"{winner.cah_user.discord_user.name} has won the round with {winner.played_cards_as_text}",winner=winner)

		self.players.append(self.judge)
	def draw_whitecard(self):
		if not len(self.unexpended_whitecards) > 0:
			return
		return self.unexpended_whitecards.pop()
	async def draw_blackcard(self):
		if not len(self.unexpended_blackcards) > 0:
			return

		drawn_blackcard = self.unexpended_blackcards.pop()
		self.prompting_blackcard = drawn_blackcard

		judge_user = self.judge.cah_user.discord_user
		await dm(judge_user,"The blackcard you have drawn is:\n>>> {card.text}".format(card=self.prompting_blackcard))

		if self.auto_read:
			for player in self.players_static:
				user = player.cah_user.discord_user
				
				if user != self.judge:
					if drawn_blackcard.pick != 1:
						await dm(user, "The blackcard is:\n>>> {card.text}".format(card=self.prompting_blackcard))
					else:
						await dm(user, "The blackcard is:\n>>> {card.text}".format(card=self.prompting_blackcard))


		
