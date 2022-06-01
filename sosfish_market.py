import random
import sosbet
import datetime
import math
import sosfish_constants

def SellerText(data, user):

	fish = FishOfTheDay(data)

	output = f"You hear a local merchant offering to buy three {fish} for a {sosbet.CURRENCY}."

	if fish in data[user]["catchlog"].keys():

		if fish not in data[user]["sell_log"].keys():
			data[user]["sell_log"][fish] = 0

		count = data[user]["catchlog"][fish] - data[user]["sell_log"][fish]

		output += f" You have {count} {fish}"

		if count>=3:
			output += ", sell three of them with \"!fish sell\"."
		else:
			output += "."

	else:
		output += "\nUnfortunately you do not have any."

	return output

def Sell(data, user):
	fish = FishOfTheDay(data)

	if fish in data[user]["catchlog"].keys():

		if fish not in data[user]["sell_log"].keys():
			data[user]["sell_log"][fish] = 0
		count = data[user]["catchlog"][fish] - data[user]["sell_log"][fish]
		if count>=3:
			data[user]["sell_log"][fish] += 3
			sosbet.addMoney(user, 1)
			sosbet.saveMoney()
			return f"You sell three {fish} for {sosbet.CURRENCY}.\nYour new balance: {sosbet.balance(user, user)}"
		else:
			return f"You do not have enough {fish}."
	return f"You do not have any {fish}"


def FishOfTheDay(data):
	current_time = datetime.datetime.now()

	index = current_time.day + current_time.month * 31

	#index = random.randrange(1000)

	location_id =  int( math.floor(index/4) % len(data.keys()) )
	location_fish_id = (index%4)
	location = list(data.keys())[location_id]
	
	while "Mead and Madness" in location or "Cat Cafe" in location:
		index+=10
		location_id =  int( math.floor(index/4) % len(data.keys()) )
		location_fish_id = (index%4)
		location = list(data.keys())[location_id]

	location_fish = data[location]["fish"][str(location_fish_id)]["name"]

	while location_fish in sosfish_constants.pokemon["ALL"]:
		index+=10
		location_id =  int( math.floor(index/4) % len(data.keys()) )
		location_fish_id = (index%4)
		location = list(data.keys())[location_id]
		location_fish = data[location]["fish"][str(location_fish_id)]["name"]

	return location_fish

def amendProfile(data, name):
	if "sell_log" not in data[name]:
		data[name]["sell_log"] = {}