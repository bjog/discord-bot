#!/usr/bin/env python3
import discord

client = discord.Client()

@client.event
async def on_message(message):
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

TOKEN = load_token()
client.run(TOKEN)

