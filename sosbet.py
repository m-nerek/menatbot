# hello there!
import json
import os
import urbandictionary
import sosmarkov
import re
import string

dir_path = os.path.dirname(os.path.realpath(__file__))

STARTING_FUNDS = 5
MINIMUM_FUNDS = 1
CURRENCY = "$"

help_string = f"""Betting commands:
        `!bet [amount] on [thing]` create a new bet
        `!bet [amount] on [ID]` place {CURRENCY} on an existing bet
        `!bet [amount] against [ID]` place {CURRENCY} against an existing bet
        `!bets` to see all your currently active bets
        `!lock [ID]` once an event starts you can lock a bet to prevent further modification (if you are participating)
        `!unlock [ID]` you can also unlock if participating
        `!concede [ID]` lost a bet? This is how you give the winners their {CURRENCY}
        
        `!pay [userID] [amount]` give someone your hard earned {CURRENCY}
        `!balance [userID]` check how much {CURRENCY} someone has
        """



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
	for y in range(10):
		#words = urbandictionary.random()
		words = sosmarkov.sentence(sosmarkov.models['general']).split(" ")
		for x in range(len(words)):
			#key = re.sub('[\W_]', '', words[x].word)
			key = re.sub('[\W_]', '', words[x])
			if isValidKey(key.lower(),dict):
				return key.lower()
	return False



def sign(number):
	if number>0:
		return 1
	if number<0:
		return -1
	return 0
#bets[key]['description']
def findKey(search_key, dict):
	keys = [string for string in dict.keys() if search_key.lower() in string.lower()]
	descs = [string for string in dict.keys() if search_key.lower() == dict[string]['description'].lower()]
	if any(keys):
		return keys[0]
	if any(descs):
		return descs[0]
	else:
		return False

def isValidKey(string, dict):
	if len(string)<3 or len(string)>10:
		return False
	if findKey(string, dict):
		return False
	return True

def hasMoney(user, amount):
	if not user in money:
		money[user] = STARTING_FUNDS

	if money[user] == 1 and int(amount)== 1:
		return True

	return money[user]-1>=int(amount)

def subtractMoney(user, amount):
	if not user in money:
		money[user] = STARTING_FUNDS
	money[user] = max(MINIMUM_FUNDS, int(money[user]) - abs(int(amount)))

def addMoney(user, amount):
	money[user] = int(money[user]) + abs(int(amount))

def processBet(user, amount, description):
	
	if len(description)<2:
		return "which bet did you mean?"

	key = findKey(description, bets)
	if key:

		if 'lock' in bets[key] and bets[key]['lock']==True:
			return f"Bet [{key}] is locked. No further betting can take place on it."

		#is user already betting
		for x in range(len(bets[key].keys())):
			if str(x) in bets[key].keys() and user in bets[key][str(x)]["user"]:

				if sign(bets[key][str(x)]['amount']) != sign(amount):
					return f"you cannot bet against yourself"

				
				bets[key][str(x)]['amount'] += int(amount)
				
				subtractMoney(user, amount)

				return f"adding {CURRENCY}{abs(int(amount))} to existing bet [{key}], new total {CURRENCY}{abs(bets[key][str(x)]['amount'])}"
			elif str(x) not in bets[key].keys():

				bets[key][str(x)] = {"user":user, "amount":amount}
				
				subtractMoney(user, amount)

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
		subtractMoney(user, amount)

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
					addMoney(bet_user, refund)
					output+=f" {bet_user} was refunded {CURRENCY}{refund} from a bet of {CURRENCY}{amount_bet}."
				else:
					amount_bet = abs(int(bets[key][str(x)]['amount']))
					bet_user = bets[key][str(x)]['user']
					payoff = min(amount_bet, total_pot)
					total_pot -= payoff
					addMoney(bet_user, payoff + amount_bet)
					output+=f" {bet_user} was paid {CURRENCY}{payoff+amount_bet} from a bet of {CURRENCY}{amount_bet}."

		del bets[key]
		
		return output

	else:
		return "I cannot find that bet."


def showBet(key):
	output = f"\"{bets[key]['description']}\" [{key}]\n"
	for x in range(len(bets[key].keys())):
			if str(x) in bets[key].keys():
				amount = bets[key][str(x)]['amount']
				user = bets[key][str(x)]['user']
				if amount<0:
					output+="-"
				else:
					output+="+"
				output+=f"{CURRENCY}{abs(amount)} {user}"
				
				output+="\n"
	return output


def showBets(user, user_to_find):
	output = "```diff"
	if user_to_find == "me" or user_to_find == "":
		user_to_find=user

	for bet in bets.keys():
		for x in range(len(bets[bet].keys())):
			if str(x) in bets[bet].keys():
				if (user_to_find == bets[bet][str(x)]['user']):
					amount = bets[bet][str(x)]['amount']
					output+=f"{showBet(bet)}"
	output+="```"
	return output

def lockBet(user, id):
	
	key = findKey(id, bets)

	if key == False:
		return "I don't recognise that bet ID"
	
	for x in range(len(bets[key].keys())):
		if str(x) in bets[key].keys():
			if (user == bets[key][str(x)]['user']):
				if 'lock' in bets[key] and bets[key]['lock']==True:
					return f"Bet [{key}] is already locked. No further betting can take place on it."

				bets[key]['lock'] = True
				return f"[{key}] is now locked. No further betting can take place on it."

	return "You can only lock a bet if you are participating"

def unlockBet(user, id):
	
	key = findKey(id, bets)

	if key == False:
		return "I don't recognise that bet ID"
	
	for x in range(len(bets[key].keys())):
		if str(x) in bets[key].keys():
			if (user == bets[key][str(x)]['user']):
				if 'lock' in bets[key] and bets[key]['lock']==True:
					bets[key]['lock'] = False
					return f"Bet [{key}] is unlocked."

				return f"[{key}] is already unlocked."

	return "You can only unlock a bet if you are participating"



def balance(user, user_to_find):
	output = ""
	if user_to_find == "me" or user_to_find == "":
		user_to_find=user

	key = findKey(user_to_find, money)

	if key:
		return f"{key} has {CURRENCY}{money[key]}"
	elif user_to_find==user:
		money[user] = STARTING_FUNDS
		return f"{user} has {CURRENCY}{money[user]}"
	else:
		return "I'm not sure whose balance to show"

def pay(user, user_to_find, amount):


	try:
		amount = abs(int(amount))
	except:
		return f"I need a whole number please, '{amount}' is too confusing!"

	key = findKey(user_to_find, money)

	if amount<=0:
		return "how much?"
	if key==False:
		return "who?"

	if money[user]<amount+MINIMUM_FUNDS:
		return "you do not have the funds to pay"

	money[user] -= amount;
	money[key] += amount;

	return f"{user} paid {key} {CURRENCY}{amount}"



def respond(user, string):
	
	output = "I don't understand the instruction o_o"
	s = string.lower().split(" ")
	if s[0] == "!bet":

		try:
			int(s[1])
		except:
			return f"I need a whole number please, '{s[1]}' is too confusing!"

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
		output = pay(user,s[1]," ".join(s[2:]))
	elif s[0] == "!lock":
		output = lockBet(user,s[1])
	elif s[0] == "!unlock":
		output = unlockBet(user,s[1])
	

	save("bets",bets)
	save("money", money)
	return output



bets = load("bets")
money = load("money")


#print(respond("dude", "!balance"))
#print(respond("dude2", "!balance"))

#print(respond("dude", "!bet custard on asdl"))
#print(respond("dude", "!lock asdl"))
#print(respond("dude", "!bet 1 on asdl"))
#print(respond("dude", "!unlock asdl"))
#print(respond("dude", "!bet 1 on asdl"))

#print(respond("dude", "!balance"))
#print(respond("dude2", "!balance"))

#print(respond("dude2", "!concede asdl"))

#print(respond("dude", "!balance"))
#print(respond("dude2", "!balance"))

