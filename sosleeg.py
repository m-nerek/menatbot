import random
import urbandictionary

roles = ["Top", "Jungle", "Mid", "Bot", "Support"]
champs = ["Old Morde", "Alkali", "Yasuo", "Teemo", "Vayne", "Shaco", "Tryndamere", "Riven", "Katarina"]
ranks = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "Challenger"]
teams = ["GG", "CLG", "LCS", "EG", "IMT", "LCS", "TL", "DIG", "LCS", "TSM", "FNC", "MSF", "LEC", "S04", "VIT", "LEC", "RGE", "XL", "LEC", "AST", "SK", "LEC", "G2", "MAD", "LEC", "KT", "NS", "LCK", "T1", "HLE", "LCK"]
report = ["Spam", "Toxic behaviour", "Hacking", "Inting", "Racism", "Language"]

def numberFromString(string, range):
	number=0
	for char in string:
		number += ord(char)
	return (number % range)


def number():
	
	n = random.randint(1,10)

	while random.randint(1,4)>1:
		if n<100000:
			n=n*10
			n+= random.randint(1,10)
	return n

def leetUser(name):
	text = [f"XxX_{name}_XxX", f"{name}_Pu$sYsLaY3R", f"{name}_69", f"{name}_420",f"{name}_TeH_G0D"]

	return random.choice(text)

def describeAccount(accountName, smurf = False):
	if smurf:
		output = f"---{leetUser(accountName)}---\n"
		output+= f"Rank: {ranks[0]}\n"
	else:
		output = f"---{random.choice(teams)} {accountName}---\n"
		output+= f"Rank: {random.choice(ranks)}\n"

	
	output+= f"Champion: {random.choice(champs)}\n"
	output+= f"Role: {random.choice(roles)}\n"
	numgames = number()
	numquits = random.randint(0, numgames)

	output+= f"Games played: {numgames}\n"
	if smurf:
		output+= f"Wins: {min(numgames-numquits, max(0,numgames-number()))}\n"
	else:
		output+= f"Wins: {min(numgames-numquits, number())}\n"

	r = random.randint(1,6)
	while r<len(report):
		output += f"Reported {number()} times for {report[r]}\n"
		r+=random.randint(1,6)

	output+=f"{numquits} rage quits detected\n"

	return output


def Leeg(user):

	random.seed(numberFromString(user, 32000));

	output = describeAccount(user)
	output += f"Money spent on skins: €{number()}\n"
	

	if random.randint(1,4)>1:
		output += "\n"
		definitions = urbandictionary.random()
		output += f"\nALTERNATE ACCOUNT DETECTED FOR {user.upper()}:\n"
		output += describeAccount(definitions[0].word, True)

	return output
