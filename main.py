# main.py
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cah import CardsAgainstHumanity
from user import CAH_User
from json_data import cards, settings
from deck import Deck
from player import Player
import typing


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

MAIN_CHANNEL = settings["main_channel"]
MIN_PLAYERS = settings["min_players"]

_allowed_decks = cards.keys()
for not_deck in settings["not_decks"]:
	_allowed_decks.remove(not_decks)
allowed_decks = []
if settings["deck_restriction_mode"] == "whitelist":
	for _allowed_deck in _allowed_decks:
		if _allowed_deck in settings["whitelisted_decks"]:
			allowed_decks.append(_allowed_deck)

elif settings["deck_restriction_mode"] == "blacklist":
	for _allowed_deck in _allowed_decks:
		if _allowed_deck not in settings["blacklisted_decks"]:
			allowed_decks.append(_allowed_deck)
else:
	pass

print(allowed_decks,type(allowed_decks),[(deck,type(deck)) for deck in allowed_decks])
bot = commands.Bot(command_prefix='!')
games = {}

async def is_game_owner(ctx):
	if games[ctx.author.id].game == None:
		await ctx.send("You have not started a game yet. \\\\/('-')\\\\/ lul idk")
		return False
	return True
async def is_in_unstarted_game(ctx):
	game = games[ctx.author.id].game
	if game.in_session:
		await ctx.send("but itz already staaaaarted.")
		return False
	return True
async def is_in_started_game(ctx):
	player = games[ctx.author.id].playing_as
	if not player.parent_game.in_session:
		await ctx.send("OMG it hasn't even staaaaarted yet, I mean itz only been like 2 minz jeeeez!")
		return False
	return True
async def is_in_system(ctx):
	if ctx.author.id not in games.keys():
		games[ctx.author.id] = CAH_User(ctx.author, bot)
	return True
async def is_in_game(ctx):
	if games[ctx.author.id].playing_as == None:
		await ctx.send("but yaint in a game tho?")
		return False
	return True
async def is_not_in_game(ctx):
	if games[ctx.author.id].playing_as != None:	
		await ctx.send("but ur already in a game with {}!".format(", ".join([player.cah_user.discord_user.name for player in games[ctx.author.id].playing_as.parent_game.players])))
		return False
	return True
async def is_not_judge(ctx):
	if games[ctx.author.id].playing_as.parent_game.judge == games[ctx.author.id].playing_as:
		await ctx.send("Haha! No... u cant do that ur da judge!")
		return False
	return True
async def is_judge(ctx):
	if games[ctx.author.id].playing_as.parent_game.judge != games[ctx.author.id].playing_as:
		await ctx.send("Excuse me but ya cant do dat! yaint da judge!")
		return False
	return True
async def judge_has_drawn(ctx):
	if games[ctx.author.id].playing_as.parent_game.prompting_blackcard != None:
		await ctx.send("judge hain't drawn yet!")
		return False
	return True
async def judge_has_not_drawn(ctx):
	if games[ctx.author.id].playing_as.parent_game.prompting_blackcard == None:
		await ctx.send("y'already did that!")
		return False
	return True
async def player_count_gtet_MIN_PLAYERS(ctx):
	players = games[ctx.author.id].playing_as.parent_game.players
	if len(players) >= MIN_PLAYERS:
		return True
	ctx.send("Yaint got enough people sowwy :( lul jk dont care")
	return False
@bot.command(name='newgame', help='starts a new game')
@commands.checks(
	is_in_system,
	is_not_in_game
)
async def _newgame(ctx, *decks):
	for deck in decks:
		if deck not in allowed_decks:
			return
	Decks = []
	for deck in decks:
		Decks.append(Deck(deck))
	f_contents = games[ctx.author.id]
	f_contents.game = CardsAgainstHumanity(f_contents, Decks, bot)
	player = Player(f_contents, f_contents.game)
	f_contents.game.players.append(player)
	await ctx.send("You have started a new game of Cards Against Humanity!")

	
@bot.command(name="playcards")
@commands.checks(
	is_in_system,
	is_in_game,
	is_in_started_game,
	is_not_judge,
	judge_has_drawn
)
async def _playcards(ctx, whitecards_ids:commands.Greedy[int]):
	f_contents = games[ctx.author.id]
	player = f_contents.playing_as
	player.playcards(whitecards_ids)

@bot.command(name="accept")
@commands.checks(
	is_in_system,
	is_not_in_game
)
async def _accept(ctx, user:discord.Member):

	if user.id not in games.keys():
		await ctx.send("{} has not made a game yet. \\\\/('-')\\\\/ lul idk".format(user.name))
		return
	if games[user.id].game == None:
		await ctx.send("{} has not made a game yet. \\\\/('-')\\\\/ lul idk".format(user.name))
		return
	game = games[user.id].game
	if ctx.author.id not in game.invited:
		await ctx.send("{} has made a game but yaint invited. lul get rekt.".format(user.name))
		return
	game.invited.remove(ctx.author.id)
	if ctx.author.id not in games.keys():
		games[ctx.author.id] = CAH_User(ctx.author, bot)
	player = Player(games[ctx.author.id], game)
	game.players.append(player)





bot.command(name='invite', help='invites people to your newest game')
@commands.check(
	is_in_system,
	is_in_game,
	is_in_unstarted_game,
	is_game_owner
)
async def _invite(ctx, invited_users:commands.Greedy[discord.Member]):

	game = games[ctx.author.id].game
	invited_already = []
	too_be_invited = []
	for user in invited_users:
		if user.id in game.invited:
			invited_already.append(user)
		elif user.id in [player.cah_user.discord_id for player in game.players]:
			invited_already.append(user)
		else:
			too_be_invited.append(user)
	game.invited += [user.id for user in too_be_invited]
	if len(too_be_invited) > 0:
		print(type(bot.get_channel(MAIN_CHANNEL)))
		await bot.get_channel(MAIN_CHANNEL).send("Hey {0}! {1} has invited you to play cards Cards Against Humanity! type: \"!accept {2}\" to a thier invitation!".format(", ".join([user.mention for user in too_be_invited]),ctx.author.name,ctx.author.mention))
	if len(invited_already) > 0:
		await bot.get_channel(MAIN_CHANNEL).send("btw you already invited {0}.".format(", ".join([user.name for user in invited_users])))






@bot.command(name="startgame")
@commands.checks(
	is_in_system,
	is_in_game,
	is_in_unstarted_game,
	is_game_owner
)
async def _startgame(ctx,args:commands.Greedy[str]):

	game = games[ctx.author.id].game
	await game.start("random_order" in args,"auto_read" in args)




@bot.command(name="draw")
@commands.checks(
	is_in_system,
	is_in_game,
	is_in_started_game,
	is_judge
)
async def _draw(ctx):

	game = games[ctx.author.id].playing_as.parent_game
	print("hi")
	await game.draw_blackcard()






@bot.command(name="collect")
@commands.checks(
	is_in_system,
	is_in_game,
	is_in_started_game,
	is_judge
)
async def _collect(ctx, no_play_ignore:bool):

	pass






bot.run(TOKEN)
