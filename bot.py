#!/usr/bin/env python3
import discord
import json
import re

client = discord.Client()

enableCharLimit = True
charLimit = 140

enableWordBan = True
bannedWordList = []

@client.event
async def on_message(message):
	global enableCharLimit

	if message.author == client.user:
		return
	
	if message.content.startswith('!hello'):
		reply = "Hello there!"
		await client.send_message(message.channel,reply)

	if message.content.startswith('!whoami'):
		reply = "You are " + message.author.name
		await client.send_message(message.channel, reply)

	if message.content.startswith("!siege"):
		reply = "@everyone **LAUNCH R6:SIEGE ->** steam://run/359550"
		await client.send_message(message.channel,reply)

	if message.content.startswith("!stellaris"):
		reply = "@everyone **LAUNCH Stellaris ->** steam://run/281990"
		await client.send_message(message.channel,reply)

	if message.content.startswith("!stardew"):
		reply = "@everyone **LAUNCH Stardew Valley ->** steam://run/413150"
		await client.send_message(message.channel,reply)


	if message.content.startswith("!arma3"):
		reply = "@everyone **LAUNCH ARMA 3 ->** steam://run/107410"
		await client.send_message(message.channel,reply)

	if message.content.startswith("!getinfo"):
		print(message.channel.id)
		print(message.channel.name)
		print(message.channel.server.name)
		print(message.channel.position)
	
	if message.content.startswith("!toggle limit"):
		enableCharLimit = not enableCharLimit
		reply = "Character limit enabled: " + str(enableCharLimit)
		await client.send_message(message.channel,reply)

	if message.content.startswith("!toggle wordban"):
		enableWordBan = not enableWordBan
		reply = "Word ban enabled: " + str(enableWordBan)
		await client.send_message(message.channel,reply)
	
	if (len(message.content) > charLimit) and (enableCharLimit):
		reply = "Message exceeds character limit."
		await client.send_message(message.channel,reply)
		await client.delete_message(message)

	#Check message for banned words		
	if(enableWordBan):
		msg = message.content.casefold().split()
		for word in bannedWordList:
			if word in msg:
				reply = "Message contained banned word: " + word[0] + ("\*"*(len(word)-2)) + word[-1] + "."
				await client.send_message(message.channel,reply)
				await client.delete_message(message)
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
	print(bannedWords)
	return bannedWords

bannedWordList = load_banned_words()
TOKEN = load_token()

client.run(TOKEN)


