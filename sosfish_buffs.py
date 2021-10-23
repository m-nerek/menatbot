import re
import datetime
import sosfish_constants
from sosfish_constants import herbs
from sosfish_constants import spices
from sosfish_constants import badge_text
from sosfish_constants import forbidden_ingredients
from sosfish_constants import pokemon

def checkAlcoholExpiry(name, data):
	if "alcohol" in data[name]["buffs"]:
		expiry_time = datetime.datetime.strptime( data[name]["buffs"]["alcohol"]["timer"] ,"%Y-%m-%d-%H-%M")
		if expiry_time < datetime.datetime.now():
			del data[name]["buffs"]["alcohol"]

def progressAlcohol(name, data):
	if "alcohol" not in data[name]["buffs"]:
		data[name]["buffs"]["alcohol"] = {}
		data[name]["buffs"]["alcohol"]["level"] = "1"
	else:
		level = int(data[name]["buffs"]["alcohol"]["level"])
		if level == 2:
			level = -1
		elif level>=0:
			level += 1
		elif level<0:
			level -= 1
		data[name]["buffs"]["alcohol"]["level"] = str(level)

	timer = datetime.datetime.now() + datetime.timedelta(hours = 2)
	data[name]["buffs"]["alcohol"]["timer"] = f"{timer.year}-{timer.month}-{timer.day}-{timer.hour}-{timer.minute}"


def describeDrunkenness(name, data):
	if data[name]["buffs"]["alcohol"]["level"] == "1":
		return "energised, providing a small boost to concentration"
	if data[name]["buffs"]["alcohol"]["level"] == "2":
		return "buzzing, providing a significant boost to concentration"
	if data[name]["buffs"]["alcohol"]["level"] == "-1":
		return "tipsy, which is affecting your concentration a little"
	if data[name]["buffs"]["alcohol"]["level"] == "-2":
		return "drunk, which is affecting your concentration quite a bit"
	if data[name]["buffs"]["alcohol"]["level"] == "-3":
		return "hammered, which is affecting your concentration a lot"
	if int(data[name]["buffs"]["alcohol"]["level"]) <= -4:
		return "barely coherent, which is making it hard to do anything not involving the floor"
	return "sober"

def alcoholBuff(name, data):
	if "alcohol" not in data[name]["buffs"]:
		return 0
	return int(data[name]["buffs"]["alcohol"]["level"])

def resetCampfire(name, data):
	#print(f"amend data {name}")
	data[name]["campfire"] = {}
	data[name]["campfire"]["fuel"] = "N"
	data[name]["campfire"]["alight"] = "N"
	data[name]["campfire"]["timer"] = "0"
	data[name]["campfire"]["ingredients"] = {}
	data[name]["campfire"]["stewscore"] = "0"

def describeCampfire(name, data, hour):

	if len(data[name]["campfire"]["ingredients"])>0:
		if hour<sosfish_constants.SUNRISE_START or hour>sosfish_constants.SUNSET_START:
			return " The flickering flames of a campfire cast a glow on the surroundings, and the silhouette of a stew pot hangs above it. "
		return " A campfire casts a trail of smoke into the sky, and above it a pot of stew bubbles away. "
	if data[name]["campfire"]["alight"] == "Y":
		if hour<sosfish_constants.SUNRISE_START or hour>sosfish_constants.SUNSET_START:
			return " The flickering flames of a campfire cast a glow on the surroundings. "
		return " A campfire casts a trail of smoke into the sky. "
	else:
		return " A campfire is ready to be lit. "

def calculateStew(location, data):

	score = 0

	prev_ingredients = []
	prev_ingredient = ""
	for i in data[location]["campfire"]["ingredients"]:
		ingredient = data[location]["campfire"]["ingredients"][i]

		#print(f"comparing {ingredient} to {prev_ingredient}")
		if ingredient in prev_ingredient:
			score += 0
		elif prev_ingredient == "":
			score += 1;
			prev_ingredient = ingredient
			prev_ingredients.append(ingredient)
		else:
			matches = len(re.findall(f"[{prev_ingredient}]", ingredient))
			#print(f"matches: {matches} len: {len(ingredient)}")
			if matches>=len(ingredient)/2 + score:
				score+=1;
			elif matches<len(ingredient)/2-1 + score:
				score-=1;
			prev_ingredient = ingredient
			prev_ingredients.append(ingredient)
		

	return score

def describeStew_(score):
	score = int(score)
	bad_stew = ["looks a bit gray and watery","smells a little weird","has turned an unpleasant green colour","smells revolting","has turned black and is making your eyes water"]
	good_stew = ["smells appetizing","looks succulent","smells delicious","looks rich and tasty","smells irresistably divine"]
	ok_stew = "looks ok"

	if score == 0:
		return ok_stew
	if score > 0:
		index = min(score-1, len(good_stew)-1)
		return good_stew[index]
	if score < 0:
		index = min(-score-1, len(bad_stew)-1)
		return bad_stew[index]

def describeBuff(score):
	score = int(score)
	amounts = ["small", "moderate", "significant", "large", "huge"]
	if score == 0:
		return ""
	if score > 0:
		index = min(score-1, len(amounts)-1)
		return f" and improves the spirits of anyone nearby a {amounts[index]} amount."
	if score < 0:
		index = min(-score-1, len(amounts)-1)
		return f" and interferes with the concentration of anyone nearby a {amounts[index]} amount."

def describeStew(location, data):
	stewscore = data[location]["campfire"]["stewscore"]
	return f"The stew cooking on the campfire at this location {describeStew_(stewscore)}{describeBuff(stewscore)}"		

def addToStew(ingredient, name, location, data):

	if len(data[location]["campfire"]["ingredients"])>20:
		return "The pot is too full to add anything else"

	alreadyIn=False
	for i in data[location]["campfire"]["ingredients"]:
		if data[location]["campfire"]["ingredients"][i] == ingredient:
			alreadyIn = True

	if not alreadyIn:
		index = str(len(data[location]["campfire"]["ingredients"]))
		data[location]["campfire"]["ingredients"][index] = ingredient
	stewscore = calculateStew(location, data)
	data[location]["campfire"]["stewscore"] = str(stewscore)

	output = f"{name} adds {ingredient} to the pot. The stew {describeStew_(stewscore)}{describeBuff(stewscore)}"

	if "Cook" not in data[name]["flags"]:
		data[name]["flags"]["Cook"] = True
		output += f"\n{badge_text}[Cook]"

	if "Masterchef" not in data[name]["flags"] and int(stewscore)>=5:
		data[name]["flags"]["Masterchef"] = True
		output += f"\n{badge_text}[Masterchef]"

	if "Disaster Artist" not in data[name]["flags"] and int(stewscore)<=-5:
		data[name]["flags"]["Disaster Artist"] = True
		output += f"\n{badge_text}[Disaster Artist]"

	forbidden = False

	if ingredient in forbidden_ingredients:
		forbidden = True

	if ingredient.lower() in (name.lower() for name in sosfish_constants.pokemon["ALL"]):
		forbidden = True

	if "Evil Monster" not in data[name]["flags"] and forbidden == True:
		data[name]["flags"]["Evil Monster"] = True
		output += f"\n{badge_text}[Evil Monster]"
	elif forbidden == True:
		output += f"\nYour [Evil Monster] badge glows a sinister red"

	return output


def campfire_main_loop(name, location, parameters, data):

	if data[name]["currentlocation"] == "":
		data[name]["currentlocation"] = name

	#if location!="" and data[name]["currentlocation"]!=location:
	#	data[name]["currentlocation"] = location

	if location == "":
		location = data[name]["currentlocation"]

	if data[location]["campfire"]["timer"] == 0:
		data[location]["campfire"]["timer"] = "0"


	if "stewscore" not in data[location]["campfire"]:
		data[location]["campfire"]["stewscore"] = "0"

	if data[location]["campfire"]["stewscore"] == 0:
		data[location]["campfire"]["stewscore"] = "0"

	if data[location]["campfire"]["timer"] != "0":
		campfire_expiry_time = datetime.datetime.strptime( data[location]["campfire"]["timer"] ,"%Y-%m-%d-%H-%M")
		if campfire_expiry_time < datetime.datetime.now():
			resetCampfire(location, data)

	if " cook " in parameters:

		if data[location]["campfire"]["fuel"] == "N":
			return "A campfire has not been made at this location"

		if data[location]["campfire"]["alight"] == "N":
			return "The campfire at this location has not been lit"

		for h in herbs:
			if h in parameters:
				if h in data[name]["flags"]:
					return addToStew(h, name, location, data)
				else:
					return f"Ingredient not recognized, or not in {name}'s inventory"

		for s in spices:
			if s in parameters:
				if s in data[name]["flags"]:
					return addToStew(s, name, location, data)
				else:
					return f"Ingredient not recognized, or not in {name}'s inventory"

		for b in data[name]["baitbox"]:
			if data[name]["baitbox"][b] in parameters:
				return addToStew(data[name]["baitbox"][b], name, location, data)

		for f in data[name]["catchlog"]:
			f = f.split("[")[0].lower().strip()
			if f in parameters:
				return addToStew(f, name, location, data)

		return f"Ingredient not recognized, or not in {name}'s inventory"

	if " campfire" in parameters:
		if " light" in parameters:
			if "flintsteel" not in data[name]["flags"]:
				return "You do not have anything with which to light a fire"

			if data[location]["campfire"]["fuel"] == "N":
				return "A campfire has not been laid at this location"

			if data[location]["campfire"]["alight"] == "Y":
				return "There is an already lit campfire at this location"

			data[location]["campfire"]["alight"] = "Y"
			camptimer = datetime.datetime.now() + datetime.timedelta(hours = 4)
			data[location]["campfire"]["timer"] = f"{camptimer.year}-{camptimer.month}-{camptimer.day}-{camptimer.hour}-{camptimer.minute}"
			output = "You light the campfire and the flames crackle merrily. You can now make stew with the '!fish cook [ingredient]' command"
			if "Pyromaniac" not in data[name]["flags"]:
				data[name]["flags"]["Pyromaniac"] = True
				output += f"\n{badge_text}[Pyromaniac]"
			return output

		else:
			if "nofire" in data[location]["requires"]:
				return "A campfire cannot be made at this location"

			if data[location]["campfire"]["fuel"] == "Y":
				return "A campfire has already been laid at this location"
			if "log" not in data[name]["flags"]:
				return "You don't have anything you can make a fire with"

			data[location]["campfire"]["fuel"] = "Y"
			del data[name]["flags"]["log"]

			return f"{data[location]['description']} {name} gathers stones for a firepit and sets down a log. Now the fire just needs lighting with '!fish light campfire'"

	return None