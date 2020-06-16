# hello there!
import json
import os
import urbandictionary
import re
import string

dir_path = os.path.dirname(os.path.realpath(__file__))

STARTING_FUNDS = 5
MINIMUM_FUNDS = 1
CURRENCY = "$"

def load(file):
	try:
		with open(f"{dir_path}/{file}.json", "r") as file:
			try:
				return json.load(file)
			except json.decoder.JSONDecodeError:
				return {}
	except:
		return {}

def save(file, data):
	with open(f"{dir_path}/{file}.json", "w") as file:
		json.dump(data ,file)

def getKey(dict):

	words = urbandictionary.random()

	for x in range(len(words)):
		key = re.sub('[\W_]', '', words[x].word)
		if isValidKey(key.lower(),dict):
			return key.lower()
	return False


def sign(number):
	if number>0:
		return 1
	if number<0:
		return -1
	return 0

def findKey(search_key, dict):
	keys = [string for string in dict.keys() if search_key.lower() in string.lower()]
	if any(keys):
		return keys[0]
	else:
		return False

def isValidKey(string, dict):
	if len(string)<2 or len(string)>10:
		return False
	if findKey(string, dict):
		return False
	return True

def hasMoney(user, amount):
	if not user in money:
		money[user] = STARTING_FUNDS
	return money[user]>=int(amount)


def processBet(user, amount, description):
	
	if len(description)<2:
		return "which bet did you mean?"

	key = findKey(description, bets)
	if key:
		#is user already betting
		for x in range(len(bets[key].keys())):
			if str(x) in bets[key].keys() and user in bets[key][str(x)]["user"]:

				if sign(bets[key][str(x)]['amount']) != sign(amount):
					return f"you cannot bet against yourself"

				bets[key][str(x)]['amount'] += amount
				money[user] -= abs(amount)
				money[user] = min(MINIMUM_FUNDS, money[user])

				return f"adding {CURRENCY}{abs(amount)} to existing bet [{key}], new total {CURRENCY}{abs(bets[key][str(x)]['amount'])}"
			elif str(x) not in bets[key].keys():
				bets[key][str(x)] = {"user":user, "amount":amount}
				output = f"[{key}]. Will \"{bets[key]['description']}\" happen?  {user} is betting {CURRENCY}{abs(amount)}"
				if amount>0:
					output+=" it will!"
				else:
					output+=" it won't!"
				return output
		return "something went wrong o_o"
	else:
		
		key = description.lower()
		if not isValidKey(key, bets):
			key = getKey(bets)
		if not isValidKey(key, bets):
			return "something went wrong UwU"

		bets[key] = {"description": description, str(0):{"user":user, "amount":amount } }
		output = f"A new bet ID [{key}] has been created. Will \"{description}\" happen? {user} is betting {CURRENCY}{abs(amount)}"
		if amount>0:
			output+=" it will!"
		else:
			output+=" it won't!"

		return output

def concedeBet(user, description):

	key = findKey(description, bets)
	if key:

		total_pot=0
		total_to_pay=0
		conceding_sign=0
		output = ""

		for x in range(len(bets[key].keys())):
			if str(x) in bets[key].keys() and user in bets[key][str(x)]["user"]:
				conceding_sign = sign(bets[key][str(x)]['amount'])

		if conceding_sign==0:
			return "well this is unexpected o_o"

		for x in range(len(bets[key].keys())):
			if str(x) in bets[key].keys():
				if conceding_sign == sign(bets[key][str(x)]['amount']):
					total_pot += abs(int(bets[key][str(x)]['amount']))
				else:
					total_to_pay += abs(int(bets[key][str(x)]['amount']))

		output+=f"Total pot {total_pot+total_to_pay} was bet."

		for x in range(len(bets[key].keys())):
			
			if str(x) in bets[key].keys():
				if conceding_sign == sign(bets[key][str(x)]['amount']):
					amount_bet = abs(int(bets[key][str(x)]['amount']))
					bet_user = bets[key][str(x)]['user']
					refund = max(0, amount_bet - total_to_pay)

					total_to_pay-=min(amount_bet, total_to_pay)
					money[bet_user] += refund
					output+=f" {bet_user} was refunded {CURRENCY}{refund} from a bet of {CURRENCY}{amount_bet}."
				else:
					amount_bet = abs(int(bets[key][str(x)]['amount']))
					bet_user = bets[key][str(x)]['user']
					payoff = min(amount_bet, total_pot)
					total_pot -= payoff
					money[bet_user] += payoff + amount_bet
					output+=f" {bet_user} was paid {CURRENCY}{payoff+amount_bet} from a bet of {CURRENCY}{amount_bet}."

		del bets[key]
		
		return output

	else:
		return "I cannot find that bet."


def showBet(key):
	output = f"[{key}] \"{bets[key]['description']}\" \n"
	for x in range(len(bets[key].keys())):
			if str(x) in bets[key].keys():
				amount = bets[key][str(x)]['amount']
				user = bets[key][str(x)]['user']
				output+=f"{user} has bet {CURRENCY}{abs(amount)} "
				if amount<0:
					output+="against"
				output+="\n"
	return output


def showBets(user, user_to_find):
	output = ""
	if user_to_find == "me" or user_to_find == "":
		user_to_find=user

	for bet in bets.keys():
		for x in range(len(bets[bet].keys())):
			if str(x) in bets[bet].keys():
				if (user_to_find == bets[bet][str(x)]['user']):
					amount = bets[bet][str(x)]['amount']
					output+=f"{showBet(bet)}"
	return output

def balance(user, user_to_find):
	output = ""
	if user_to_find == "me" or user_to_find == "":
		user_to_find=user

	key = findKey(user_to_find, money)

	if key:
		return f"{user_to_find} has {CURRENCY}{money[key]}"
	else:
		return "I'm not sure whose balance to show"

def pay(user, user_to_find, amount):
	amount = abs(int(amount))
	key = findKey(user_to_find, money)

	if amount<=0:
		return "how much?"
	if key==False:
		return "who?"

	if money[user]<amount-MINIMUM_FUNDS:
		return "you do not have the funds to pay"

	money[user] -= amount;
	money[key] += amount;

	return f"{user} paid {key} {CURRENCY}{amount}"



def respond(user, string):
	
	output = "I don't understand the instruction o_o"
	s = string.lower().split(" ")
	if s[0] == "!bet":
		if s[2] == "against":
			if hasMoney(user,abs(int(s[1]))):
				output = processBet(user, -int(s[1]), " ".join(s[3:]))
			else:
				output = "you do not have the funds"
		elif s[2] == "on" or s[2] == "for":
			if hasMoney(user,abs(int(s[1]))):
				output = processBet(user, int(s[1]), " ".join(s[3:]))
			else:
				output = "you do not have the funds"
		else:
			if hasMoney(user,abs(int(s[1]))):
				output = processBet(user, int(s[1]), " ".join(s[2:]))
			else:
				output = "you do not have the funds"
	elif s[0] == "!concede":
		output = concedeBet(user, " ".join(s[1:]))
	elif s[0] == "!bets":
		output = showBets(user," ".join(s[1:]))
	elif s[0] == "!balance":
		output = balance(user," ".join(s[1:]))
	elif s[0] == "!pay":
		output = pay(user,s[1],s[2])


	save("bets",bets)
	save("money", money)
	return output



bets = load("bets")
money = load("money")

#print(respond("dude", "!bet 2 on asdl 1"))
#print(respond("dude", "!bet 2 on asdl"))

#print(respond("dude2", "!bet 5 against asdl"))

#print(command("dude2", "!concede 12345"))
#print(respond("dude2", "!bets dude"))

