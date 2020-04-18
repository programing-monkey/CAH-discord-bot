from discord.ext import commands
import discord
class CAH_User(object):
	"""docstring for CAH_User"""
	def __init__(self, discord_user:discord.User, bot:commands.Bot):
		super(CAH_User, self).__init__()
		self.discord_user = discord_user
		self.discord_id = discord_user.id
		self.bot = bot
		self.game = None
		self.playing_as = None
		