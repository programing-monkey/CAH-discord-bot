import discord
async def dm(user:discord.User,message:str,*args,**kwargs):
	if user.dm_channel == None:
		await user.create_dm()
	message = message.format(*args,**kwargs)
	await user.dm_channel.send(message)
