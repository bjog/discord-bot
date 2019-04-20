import discord
import asyncio
import json
import string
import bank

client = discord.Client()

enableCharLimit = True
charLimit = 140

enableWordBan = True
bannedWordList = []

dadMode = True

def remove_non_alpha_chars(s):
	for x in string.digits.join(string.punctuation):
		s = s.replace(x,"")
	return s

@client.event
async def on_message(message):
	global enableCharLimit
	global enableWordBan

	if message.author == client.user:
		return

	if(message.content.startswith("!bank")):
		await bank.handle_bank_command(message)
	
	if(dadMode):
		dadPrefix = "Hi "
		dadSuffix = ", I'm Dad!"
		dadJokeFound = False
		dadJokeString = " "

		msg = message.content.casefold().split()

		for word in msg:
			if(dadJokeFound):
				dadJokeString = dadJokeString + " " + word
			if(word in ["i'm","im"]):
				dadJokeFound = True
				
		if(dadJokeFound):
			reply = dadPrefix + dadJokeString.strip() + dadSuffix
			dadJokeFound = False
			await message.channel.send(reply)

	if message.content.startswith('!hello'):
		reply = "Hello there!"
		await message.channel.send(reply)

	if message.content.startswith('!whoami'):
		reply = "You are " + message.author.name
		await message.channel.send(reply)

	if message.content.startswith("!siege"):
		reply = "**LAUNCH R6:SIEGE ->** steam://run/359550"
		await message.channel.send(reply)

	if message.content.startswith("!stellaris"):
		reply = "**LAUNCH Stellaris ->** steam://run/281990"
		await message.channel.send(reply)

	if message.content.startswith("!stardew"):
		reply = "**LAUNCH Stardew Valley ->** steam://run/413150"
		await message.channel.send(reply)


	if message.content.startswith("!arma3"):
		reply = "**LAUNCH ARMA 3 ->** steam://run/107410"
		await message.channel.send(reply)

	if message.content.startswith("!getinfo"):
		print(message.channel.id)
		print(message.channel.name)
		print(message.channel.server.name)
		print(message.channel.position)
	
	if message.content.startswith("!toggle limit"):
		enableCharLimit = not enableCharLimit
		reply = "Character limit enabled: " + str(enableCharLimit)
		await message.channel.send(reply)

	if message.content.startswith("!toggle wordban"):
		enableWordBan = not enableWordBan
		reply = "Word ban enabled: " + str(enableWordBan)
		await message.channel.send(reply)
	
	if (len(message.content) > charLimit) and (enableCharLimit):
		reply = "Message exceeds character limit."
		await message.channel.send(reply)
		await message.delete()

	#Check message for banned words		
	if(enableWordBan):
		msg =remove_non_alpha_chars(message.content.casefold()).split()
		for word in bannedWordList:
			if word in msg:
				reply = "Message contained banned word: " + word[0] + ("\*"*(len(word)-2)) + word[-1] + "."
				await message.delete()
				await message.channel.send(reply)
				break
				
@client.event
async def on_message_edit(before,after):
	global enableCharLimit
	global enableWordBan

	if (len(after.content) > charLimit) and (enableCharLimit):
		reply = "Edited message exceeds character limit."
		await after.delete()
		await after.channel.send(reply)

	#Check message for banned words		
	if(enableWordBan):
		msg =remove_non_alpha_chars(after.content.casefold()).split()
		for word in bannedWordList:
			if word in msg:
				reply = "Edited message contained banned word: " + word[0] + ("\*"*(len(word)-2)) + word[-1] + "."
				await after.delete()
				await after.channel.send(reply)
				break
				

@client.event
async def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)

def load_token():
	f = open("etc/token.secret","r")
	token = f.readline()
	f.close()
	return token.strip('\n')

def load_banned_words():
	f = open("etc/banned_words.json","r")
	bannedWords = json.load(f)
	return bannedWords

bannedWordList = load_banned_words()
TOKEN = load_token()

client.run(TOKEN)


