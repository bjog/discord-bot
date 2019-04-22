import json
# Handles banking functionality for Discord Bot.
class Bank:
	accounts = {}
	admins = []
	currencyName = ""
	name = ""

	def __init__(self, accounts, admins, currencyName, bankName):
		self.accounts = accounts
		self.admins = admins
		self.currencyName = currencyName
		self.name = bankName

	#TODO: Cleaner JSON serialisation implementation
	def to_dict(self):
		bankDict = {}
		bankDict["accounts"] = self.accounts
		bankDict["admins"] = self.admins
		bankDict["currencyName"] = self.currencyName
		bankDict["name"] = self.name

		return bankDict

def init_bank_data():
	f = open("etc/bank.json","r")
	bankDict = json.load(f)
	f.close()
	
	accounts = {}
	for k,v in bankDict["accounts"].items():
		accounts[int(k)] = v

	return Bank(accounts, bankDict["admins"], bankDict["currencyName"], bankDict["name"])


def save_bank_data():
	f = open("etc/bank.json","w")
	json.dump(bank.to_dict(),f)
	f.close()

async def view_balance(message):
	#!bank balance
	customer = message.author

	if(customer.id not in bank.accounts):
		await message.channel.send("Account error: You do not have an account with {0}.".format(bank.name))
		return

	funds = bank.accounts[customer.id]
	await message.channel.send("{0}, you have {1} {2} in your account.".format(customer.mention, funds, bank.currencyName ))

async def create_account(message):
	#!bank create <USER>

	if(len(message.mentions) != 1):
		await message.channel.send("Formatting error: `!bank create <USER>`")
		return

	customer = message.mentions[0]

	if(customer.id in bank.accounts):
		await message.channel.send("Error: Account already exists.")
		return

	await message.channel.send("Thank you for joining " + bank.name + ", " + customer.mention + ". You have been awarded 100.00 " + bank.currencyName + ".")

	bank.accounts[customer.id] = 100.00
	save_bank_data()

async def send_money(message):
	#!bank send <USER> <AMOUNT>
	sender = message.author

	if(len(message.mentions) != 1):
		await message.channel.send("Formatting error: `!bank send <USER> <AMOUNT>`")
		return

	receiver = message.mentions[0]

	#TODO: Rounding error fix, potential negative number issue
	amount = float(message.content.split()[3]) 

	if(sender.id not in bank.accounts):
		await message.channel.send("Sender has no account with " + bank.name + ".")
		return

	if(receiver.id not in bank.accounts):
		await message.channel.send("Receiver has no account with " + bank.name + ".")
		return

	if(bank.accounts[sender.id] < amount):
		await message.channel.send("Sender has insufficient funds.")
		return

	senderFunds = bank.accounts[sender.id]
	bank.accounts[sender.id] = senderFunds - amount

	receiverFunds = bank.accounts[receiver.id]
	bank.accounts[receiver.id] = receiverFunds + amount

	await message.channel.send("{0} sent {1} {2} to {3}.".format(sender.mention, amount, bank.currencyName, receiver.mention))
	save_bank_data()

def dump_bank_data():
	print(bank.accounts)
	print(bank.admins)
	print(bank.currencyName)

async def handle_bank_command(message):
	if(message.content.startswith("!bank dump")):
		dump_bank_data()
	if(message.content.startswith("!bank send")):
		await send_money(message)
	if(message.content.startswith("!bank create")):
		await create_account(message)
	if(message.content.startswith("!bank balance")):
		await view_balance(message)

bank = init_bank_data()