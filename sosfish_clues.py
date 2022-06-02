import random
import datetime
import math
import sosfish_constants
import sosfish_buffs

def likely():
	return random.randrange(0,100)>10

def unlikely():
	return random.randrange(0,100)>95

def companionAdvice(data, name):
	location = data[name]["currentlocation"]
	companion = data[name]["currentcompanion"]

	if companion == "":
		return ""

	# ===unused types===
    #"Normal","Electric","Ice","Poison","Ground",,
    #,"Bug","Rock","Ghost","Dark","Steel"]

	output = ""

	if unlikely() or (likely() and (companion in sosfish_constants.pokemon["PSYCHIC"] or companion in sosfish_constants.pokemon["FAIRY"])):
		output += f"\n{simping(data, name)}"

	if unlikely() or (likely() and (companion in sosfish_constants.pokemon["DRAGON"] or companion in sosfish_constants.pokemon["FLYING"])):
		output += f"\n{locationRareTimeAdvice(data, name)}"

	if unlikely() or (likely() and (companion in sosfish_constants.pokemon["WATER"] or companion in sosfish_constants.pokemon["GRASS"])):
		output += f"\n{locationBaitAdvice(data, name)}"

	if unlikely() or (likely() and (companion in sosfish_constants.pokemon["FIRE"] or companion in sosfish_constants.pokemon["FIGHTING"])):
		output += f"\n{cookingAdvice(data, name)}"


	return output

def simping(data, name):
	companion = data[name]["currentcompanion"]

	if random.randrange(0,100)>30:
		return ""

	if random.randrange(0,100)>90:
		return f"{companion} is very impressed with your fishing prowess"

	if random.randrange(0,100)>90:
		return f"{companion} enjoys your company"

	if len(data[name]["equipped"])>0:
		return f"{companion} admires {random.choice(list(data[name]['equipped'].keys()))}"

	return f"{companion} admires the scenery"

def locationRareTimeAdvice(data, name):
	location = data[name]["currentlocation"]
	companion = data[name]["currentcompanion"]
	current_time = datetime.datetime.now()

	diff1 = ((25 + int(data[location]['fish']['3']['TOD']) - current_time.hour)%24)-1
	diff2 = ((25 + int(data[location]['fish']['4']['TOD']) - current_time.hour)%24)-1

	delta = min( diff1, diff2  )

	time_advice = ""
	if delta<2:
		time_advice =  "right now!"
	elif delta<5:
		time_advice =  "in a few hours"
	else:
		time_advice = "some other time"

	return f"{companion} thinks you should fish here {time_advice}"

def locationBaitAdvice(data, name):
	location = data[name]["currentlocation"]
	companion = data[name]["currentcompanion"]
	current_time = datetime.datetime.now()

	closest_dist = 99
	closest_id = "0"

	for f in data[location]["fish"]:
		hoursfromoptimal = abs(datetime.datetime.now().hour-int(data[location]['fish'][f]['TOD']))

		if hoursfromoptimal>12:
			hoursfromoptimal = abs(24-hoursfromoptimal)

		if hoursfromoptimal<closest_dist:
			closest_dist = hoursfromoptimal
			closest_id = f

	fish_name = data[location]['fish'][closest_id]['name']

	best_bait_score = 0
	best_bait_name = ""
	for b in data[name]["baitbox"]:
		bait_name = data[name]['baitbox'][b]
		baitscore = min(3, sosfish_constants.matchScore(fish_name, bait_name, 3)) / 3

		if baitscore>best_bait_score:
			best_bait_score = baitscore
			best_bait_name = bait_name

	if best_bait_score>0.5:
		return f"{companion} thinks the fish would probably enjoy {best_bait_name}"
	else:
		return f"{companion} thinks you should find some more things fish like to eat"

def cookingAdvice(data, name):
	location = data[name]["currentlocation"]
	companion = data[name]["currentcompanion"]

	if "campfire" not in data[location]:
		return  f"{companion} looks around hopefully for any food"

	if data[location]["campfire"]["fuel"] == "N":
		return f"{companion} looks around hopefully for any food"

	if data[location]["campfire"]["alight"] == "N":
		return f"{companion} looks at the campfire expectantly"

	if len(data[location]["campfire"]["ingredients"])>20 or len(data[location]["campfire"]["ingredients"])<1:
		return f"{companion} dozes off nearby"

	last_ingredient =data[location]["campfire"]["ingredients"][list(data[location]["campfire"]["ingredients"].keys())[-1]]

	score = sosfish_buffs.calculateStew(location, data)

	for f in data[name]["catchlog"]:
		f = f.split("[")[0].lower().strip()
		if sosfish_buffs.calcIngredientCompatibility(last_ingredient, f, score)>0:
			return f"{companion} thinks you should add some {f} to the stew"

	for h in sosfish_buffs.herbs:
		if h in data[name]["flags"]:
			if sosfish_buffs.calcIngredientCompatibility(last_ingredient, h, score)>0:
				return f"{companion} thinks you should add some {h} to the stew"
		
	for s in sosfish_buffs.spices:
		if s in data[name]["flags"]:
			if sosfish_buffs.calcIngredientCompatibility(last_ingredient, s, score)>0:
				return f"{companion} thinks you should add some {s} to the stew"
	
	for b in data[name]["baitbox"]:
		if sosfish_buffs.calcIngredientCompatibility(last_ingredient, b, score)>0:
			return f"{companion} thinks you should add some {b} to the stew"
		
	return f"{companion} dozes off nearby"