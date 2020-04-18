import random
from json_data import cards
from user import CAH_User
import typing
from deck import Deck
import sys
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
		self.players = []
		self.invited = []
		self.judge = None
		self.prompting_blackcard = None
		self.in_session = False
		self.auto_read = None

	async def start(self, random_order:bool=False, auto_read:bool=False):
		self.in_session = True
		self.auto_read = auto_read
		if random_order:
			random.shuffle(self.players)
		for deck in self.decks:
			self.unexpended_whitecards += deck.whitecards
			self.unexpended_blackcards += deck.blackcards
		random.shuffle(self.unexpended_whitecards)
		random.shuffle(self.unexpended_blackcards)
		for player in self.players:
			player.refill_hand()
		await self.start_round()

	async def start_round(self):
		self.prompting_blackcard = None
		self.judge = self.players.pop(0)
		judge_user = self.judge.cah_user.discord_user
		if judge_user.dm_channel == None:
			await judge_user.create_dm()
		if self.auto_read:
			await judge_user.dm_channel.send("You are the judge!")
		else:
			await judge_user.dm_channel.send("You are the judge! type: \"!draw\" to draw a blackcard!")

		for player in self.players:
			await player.show_hand()
			user = player.cah_user.discord_user
			if user.dm_channel == None:
				await user.create_dm()
			if self.auto_read:
				await user.dm_channel.send("{judge.name} is the judge.".format(judge=judge_user))
			else:
				await user.dm_channel.send("{judge.name} is the judge. Please wait for them to draw a blackcard!".format(judge=judge_user))

		self.players.append(self.judge)
		if self.auto_read:
			self.draw_blackcard()




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

		await judge_user.dm_channel.send("The blackcard you have drawn is:\n>>> {card.text}".format(card=self.prompting_blackcard))


		if self.auto_read:
			for player in self.players:
				user = player.cah_user.discord_user
				if user.dm_channel == None:
					await player.create_dm()

				if user != self.judge:
					if drawn_blackcard.pick != 1:
						await user.dm_channel.send("The blackcard is:\n>>> {card.text}".format(card=self.prompting_blackcard))
					else:
						await user.dm_channel.send("The blackcard is:\n>>> {card.text}".format(card=self.prompting_blackcard))


		
