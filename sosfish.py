DEBUG = False

import re
import os
import datetime
import json
import random
import urbandictionary
import math
import asyncio
from sosfish_status import Status
import sosfish_buffs
import sosfish_constants
import sosfish_market
import sosfish_clues
from sosfish_constants import badge_scores
from sosfish_constants import badge_names 
from sosfish_constants import herbs
from sosfish_constants import spices
from sosfish_constants import dir_path
from sosfish_constants import loadList
from sosfish_constants import PokemonURL
from sosfish_constants import badge_text
from sosfish_constants import pokemon
from sosfish_constants import matchScore

from sosfish_board import CheckLeaderBoard

if DEBUG == False:
	import sosmarkov


def helpString(name):

	if data[name]["currentlocation"] == "":
		data[name]["currentlocation"] = name

	move_help = "\n		`!fish at [location]` The location can be the ID of another user\n		`!fish at [location] with/using [bait]`"
	campfire_help ="\n		`!fish campfire` To lay a campfire (requires a log)"
	campfire_light_help ="\n		`!fish light campfire` To light a campfire at your location"
	campfire_cook_help ="\n		`!fish cook [ingredient]` To add something to the stew (requires a lit campfire at your location)"
	companion_help ="\n		`!fish companion [name]` To make a creature your companion"

	if "bike" not in data[name]["flags"]:
		move_help = ""
	if "log" not in data[name]["flags"]:
		campfire_help = ""
	if "flintsteel" not in data[name]["flags"]:
		campfire_light_help = ""
	if data[data[name]["currentlocation"]]["campfire"]["alight"] == "N":
		campfire_cook_help = ""
	if len(data[name]["companions"])<=1:
		companion_help = ""


	return f"""Fishing commands:
        `!fish` to get started fishing
        `!fish status` to see your inventory
        `!sharebait` to share your starter bait with anyone at your location
        `!fish with/using [bait]` You need to have the bait in your baitbox{move_help}{campfire_help}{campfire_light_help}{campfire_cook_help}{companion_help}
        """

def loadData(file):
	try:
		with open(f"{dir_path}/{file}.json", "r") as file:
			try:
				return json.load(file)
			except json.decoder.JSONDecodeError:
				return {}
	except:
		return {}

def saveData(file, data):
	with open(f"{dir_path}/{file}.json", "w") as file:
		json.dump(data ,file)

def saveUserData(name, data):
	with open(f"{dir_path}/fishingdata/users/{name}.json", "w") as file:
		json.dump(data[name] ,file)

def loadUserData():
	dat = {}
	dir = f"{dir_path}/fishingdata/users/"
	for filename in os.listdir(dir):
   		with open(os.path.join(dir, filename), 'r') as f:
   			name = filename[:-5]
   			dat[name] = loadData(f"fishingdata/users/{name}")
	return dat

def numberFromString(string, range):
	number=0
	for char in string:
		number += ord(char)
	return (number % range)

def randomUser():
	usr = random.choice(list(data.keys()))

	for i in range(100):
		if data[usr]['currentlocation']=="":
			usr = random.choice(list(data.keys()))
		else:
			break
	return usr

def randomItem(name, location):
	i = random.randrange(0,7+1)

	equiptext = "\n(you can equip this item with !fish equip)"

	if i<=1:
		visit = random.choice(premadelocations)
		#print(f"randomly selected {visit}")
		retry = 0
		while f"Visited {visit}" in data[name]["flags"].keys() and retry < 50:
			retry += 1
			visit = random.choice(premadelocations)
			#print(f"randomly selected {visit}")

		if "Mead and Madness" in visit and "Dwarven Hold" not in location:
			return f"a flyer, but the water has damaged it to the point where you can't read what the runes say any more"
		if "Cafe" in visit and "leslie" not in location.lower() and "saiyuri" not in location.lower():
			return f"a flyer, but the water has damaged it to the point where all you can see is a smudged kawaii picture"
		if f"Visited {visit}" in data[name]["flags"]:
			return f"a flyer for '{visit}'"

		return f"a flyer for '{visit}', maybe you should visit sometime"

	if i<=2:
		word = randomUser()
		data[name]["last_item"] = f"{word}'s wellington boot"
		return f"{word}'s wellington boot!{equiptext}"
	if i<=3:
		word = urbandictionary.random()[0].word
		data[name]["last_item"] = f"a keyring with a tag that says '{word}' in worn letters"
		return f"a keyring with a tag that says '{word}' in worn letters!{equiptext}"
	if i<=4:
		randpoke = random.choice(sosfish_constants.pokemon['ALL'])
		randmat = random.choice(["plastic","metal","cloth","wooden"])
		data[name]["last_item"] = f"a keyring with a little {randmat} {randpoke}"
		return f"a keyring with a little {randmat} {randpoke}!{equiptext}"
	if i<=5:
		word = urbandictionary.random()[0].word
		data[name]["last_item"] = f"a hat with '{word}' emblazoned across the front"
		return f"a hat with '{word}' emblazoned across the front!{equiptext}"
	if i<=6:
		return f"a bottle containing a message that reads '{sosmarkov.sentence(sosmarkov.models['general'])} '"
	if i<=7:
		word = randomUser()
		word2 = randomUser()
		randpoke = random.choice(sosfish_constants.pokemon['ALL'])

		if random.randrange(0,100)>50:
			word2 = f"a {randpoke}"

		return f"a lewd drawing of {word2} signed by {word}"

def randomCafeExp(name, location):
	i = random.randrange(0,3+1)
	i = 2
	equiptext = "\n(you can equip this item with !fish equip)"

	if i<=1:
		data[name]["last_item"] = f"a t-shirt with a kawaii cat on the front"
		return f"At the counter there are t-shirts with a kawaii cat on the front for sale {equiptext}"
	if i<=2:
		advice_location = random.choice(list(data.keys()))
		while "Mead and Madness" in advice_location or "Cat Cafe" in advice_location:
			advice_location = random.choice(list(data.keys()))
		
		fid = random.randrange(4)
		
		amendProfile(advice_location)

		advice_fish = data[advice_location]["fish"][str(fid)]["name"]
		advice_time = data[advice_location]["fish"][str(fid)]["TOD"]

		if advice_location not in premadelocations:
			advice_location = f"{advice_location}'s"

		if int(advice_time)>12:
			advice_time = f"{(int(advice_time)-12)}pm"
		else:
			advice_time = f"{advice_time}am"
		
		return f"You stop for a chat and a coffee with a grizzled old fisherman, who tells you that the best place to catch {advice_fish} is at {advice_location} at around {advice_time}"

	return "You can't see anyone with a spare seat, maybe keep looking!"

def matchFish(tomatch, index):
	array = fish
	tomatchlower = tomatch.lower()
	highestScore=0
	highest = ""
	count=0
	for i in array:
		if ((count%5)==index):
			
			l = re.findall(f"[{tomatchlower}]", i)
			l2 = re.findall("["+tomatchlower[1]+"]", i)
			#print(f"matched {tomatch[0]} {len(l)} {len(l2)} from {i} ")
			score = len(l)*10+len(l2)
			if score>=highestScore:
				highestScore = score
				highest = i
		count+=1
	return highest

def matchFromArray(tomatch, array):
	tomatchlower = re.sub(r'\W+', '', tomatch.lower())
	highestScore=0
	for i in array:
		l = re.findall(f"[{tomatchlower}]", i)
		l2 = re.findall("["+tomatchlower[1]+"]", i)
		#print(f"matched {tomatch[0]} {len(l)} {len(l2)} from {i} ")
		score = len(l)*10+len(l2)
		if score>=highestScore:
			highestScore = score
			highest = i
	return highest



def describeTime(hour):
	if hour<sosfish_constants.SUNRISE_START or hour>sosfish_constants.SUNSET_END:
		return "As the moon reflects off the dark water "
	if hour<sosfish_constants.SUNRISE_END:
		return "As the sun rises on the horizon "
	if hour>sosfish_constants.SUNSET_START:
		return "As the sun sets over the water "
	return "It is a lovely day when "

def describeRarity(index):

	if index==2:
		return " [uncommon]"
	if index==3:
		return " [rare]"
	if index==4:
		return " [legendary]"
	return ""

def describeEffectiveness(percentage):
	if percentage<25:
		return "pretty bad"
	if percentage>75:
		return "really good"

def updatePremadeLocations():
	loaded_locations = []
	lines = loadList("premadelocations", True)
	i=0
	while i<len(lines)-2:
		if "---" in lines[i]:
			i+=1
			name = lines[i]
			loaded_locations.append(name)
			buildProfile(name)
			i+=1
			flags = lines[i]
			data[name]["requires"] = flags.split(' ')
			i+=1
			data[name]["description"] = lines[i]
			i+=1
			if "---" in lines[i] or lines[i]=="" or i>=len(lines)-2:
				continue
			data[name]["fish"] = {}
			for f in range(5):
				data[name]["fish"][str(f)] = {}
				data[name]["fish"][str(f)]["name"] = lines[i]
				data[name]["fish"][str(f)]["TOD"] = numberFromString(data[name]["fish"][str(f)]["name"],24)
				data[name]["fish"][str(f)]["rarity"] = describeRarity(f)
				i+=1
		else:
			i+=1

	return loaded_locations


def buildProfile(name):
	#print("building profile")
	if name not in data:
		data[name] = {}

	data[name]["description"] = f"Behind {name}'s {matchFromArray(name, houses)} is a {matchFromArray(name, descriptors)} {matchFromArray(name, waterbodies)}."
	
	data[name]["baitbox"] = {}
	data[name]["baitbox"][str(0)] = matchFromArray(name, bait)

	data[name]["currentlocation"] = ""
	data[name]["currentbait"] = data[name]["baitbox"][str(0)]
	data[name]["catchtime"] = 0
	data[name]["catchlog"] = {}
	data[name]["flags"] = {}
	data[name]["requires"] = ["bike"]
	data[name]["fish"] = {}
	for i in range(5):
		data[name]["fish"][str(i)] = {}
		data[name]["fish"][str(i)]["name"] = matchFish(name, i)
		data[name]["fish"][str(i)]["TOD"] = numberFromString(data[name]["fish"][str(i)]["name"],24)
		data[name]["fish"][str(i)]["rarity"] = describeRarity(i)
	amendProfile(name)
	return ""

def amendProfile(name):
	if name == "":
		return
	if "campfire" not in data[name]:
		sosfish_buffs.resetCampfire(name, data)
	if "buffs" not in data[name]:
		data[name]["buffs"] = {}
	if "equipped" not in data[name]:
		data[name]["equipped"] = {}

	if "currentcompanion" not in data[name]:
		data[name]["currentcompanion"] = ""
	if "nearbycompanion" not in data[name]:
		data[name]["nearbycompanion"] = ""
	if "companions" not in data[name]:
		data[name]["companions"] = []

	sosfish_market.amendProfile(data, name)


async def BiteMessageCallback(mention_author, channel, time, text):
	try:
		await asyncio.sleep(time)
		await channel.send(f"{mention_author} {text}")
	except:
		return

def ArrivalText(location):
	if "bike" in data[location]["requires"]:
		return "arrives on a bicycle, "
	elif "surfboard" in data[location]["requires"]:
		return "paddles across the water and rides the surf in, "
	elif "platinumkey" in data[location]["requires"]:
		return "unlocks the door and enters, "
	elif "crampons" in data[location]["requires"]:
		return "scales the sheer cliffs and hikes to the water, "
	elif "catears" in data[location]["requires"]:
		return "dons their cat ears, "
	return ""

def CastRod(name, new_location, new_bait, mention_author=None, channel=None):
	global timer_tasks
	current_time = datetime.datetime.now()

	if data[name]["currentlocation"] == "":
		data[name]["currentlocation"] = name

	location = data[name]["currentlocation"]

	if new_bait!="":
		data[name]['currentbait'] = new_bait

	arrival_text=""

	if new_location!="" and new_location!=location:
		data[name]["currentlocation"] = new_location
		location = new_location
		arrival_text = ArrivalText(location)
		
	additional_description = ""

	if data[location]["campfire"]["fuel"] == "Y":
		additional_description = sosfish_buffs.describeCampfire(location, data, current_time.hour)

	timedescription = describeTime(current_time.hour)
	if "underground" in data[location]["requires"]:
		timedescription = ""

	base_description = f"{data[location]['description']}{additional_description} {timedescription}{name} {arrival_text}"

	if "surf shack" in location.lower() and "surfboard" not in data[name]["flags"]:
		output = f"{base_description}browses a bit and after some deliberation buys a { random.choice(descriptors) } second hand surfboard in the sale"
		data[name]["flags"]["surfboard"] = True
		return output

	if "epic baits" in location.lower():
		weekbaitindex = (math.floor((current_time.day-7)/7+current_time.month*4) % len(baitoftheweek))
		bait_of_the_week = baitoftheweek[ weekbaitindex ]
		hasBait = False
		for i in range(len(data[name]["baitbox"])):
			if bait_of_the_week in data[name]["baitbox"][str(i)]:
				hasBait = True
		if not hasBait:
			output = f"{base_description}stops for a chat and buys the bait of the week '{bait_of_the_week}'"
			data[name]["baitbox"][str(len(data[name]["baitbox"]))] = bait_of_the_week
			return output

	if "gardevoir" in location.lower():
		weekherbindex = (math.floor((current_time.day-7)/7+current_time.month*4) % len(herbs))
		herb_of_the_week = herbs[ weekherbindex ]
		
		if herb_of_the_week not in data[name]["flags"]:
			output = f"{base_description}notices that the '{herb_of_the_week}' has grown a lot this week, and picks some"
			data[name]["flags"][herb_of_the_week] = True
			return output

	if "spicy sailboat" in location.lower():
		weekspiceindex = (math.floor((current_time.day-7)/7+current_time.month*4) % len(spices))
		spice_of_the_week = spices[ weekspiceindex ]
		
		if spice_of_the_week not in data[name]["flags"]:
			output = f"{base_description}stops for a chat and buys the spice of the week '{spice_of_the_week}'"
			data[name]["flags"][spice_of_the_week] = True
			return output

	if "pub" in data[location]["requires"]:
		output = f"{base_description}heads over to the raucous packed bar, and orders a drink from the grumpy old dwarven barkeep"
	elif "cafe" in data[location]["requires"]:
		output = f"{base_description}decides to explore and find someone to sit and have coffee with"
	else:
		output = f"{base_description}settles down to fish and casts a rod baited with {data[name]['currentbait']} into the water"

	if "market" in location.lower():
		output += "\n\n"+sosfish_market.SellerText(data, name)


	secs = 60*5 + (100-max(FishingOdds(name))) * 3

	if DEBUG==True:
		secs = 0

	#print(f"seconds: {secs}")
	catchtime = datetime.datetime.now() + datetime.timedelta(seconds = secs)
	check_text = "your line twitches"

	if "cat cafe" in location.lower():
		check_text = "you finish checking around"


	if channel != None:
		if name in timer_tasks:
			timer_tasks[name].cancel()
			del timer_tasks[name]

		timer_tasks[name] = asyncio.get_event_loop().create_task(BiteMessageCallback(mention_author, channel, secs, check_text))

	data[name]["catchtime"] = f"{catchtime.year}-{catchtime.month}-{catchtime.day}-{catchtime.hour}-{catchtime.minute}"
	return output

base_catch_chance = [70,70,30,20, 10]
time_of_day_falloff = [14,14,12,10,6]

def FishingOdds(name):

	odds = [0,0,0,0,0]

	location = data[name]["currentlocation"]
	currentbait = data[name]["currentbait"]

	stewscore = sosfish_buffs.calculateStew(location, data)

	sosfish_buffs.checkAlcoholExpiry(name, data)

	alcoholscore = sosfish_buffs.alcoholBuff(name, data)


	for f in data[location]["fish"]:
		fishname = data[location]['fish'][f]['name']
		
		baitscore = min(3, matchScore(fishname, currentbait, 3)) / 3
		if "pub" in data[location]["requires"]:
			baitscore = 1
		if "cafe" in data[location]["requires"]:
			baitscore = 1

		hoursfromoptimal = abs(datetime.datetime.now().hour-int(data[location]['fish'][f]['TOD']))

		if hoursfromoptimal>12:
			hoursfromoptimal = abs(24-hoursfromoptimal)

		timescore = max(0,time_of_day_falloff[int(f)]-hoursfromoptimal) / time_of_day_falloff[int(f)]

		chance =  max(0, 100 + stewscore * 5 + alcoholscore * 10)
		chance *= baitscore
		chance *= timescore
	
		#print(f"\n{fishname} chance {chance}: baitscore {baitscore} : timescore {timescore} =  {time_of_day_falloff[int(f)]} - {hoursfromoptimal} / TOD")
		odds[int(f)] = chance

	return odds

def Catch(name):

	current_time = datetime.datetime.now()
	location = data[name]["currentlocation"]
	#print(currentbait)

	highest_common_percentage=0
	highest_noncommon_percentage=0
	caught_fish = None

	fishing_odds = FishingOdds(name)

	for f in data[location]["fish"]:
		
		chance = fishing_odds[int(f)]
		
		if int(f)<3 and chance>highest_common_percentage:
			highest_common_percentage = chance
		elif int(f)>=3 and chance>highest_noncommon_percentage:
			highest_noncommon_percentage = chance

		#print(f"prebase[{chance}]")
		chance *= base_catch_chance[int(f)]/100
		#print(f"[{chance}]")
		if random.randrange(0,100)<chance:
			caught_fish = data[location]["fish"][f]

	if "gardevoir" in location.lower() and random.randrange(0,1000)<10:
		caught_fish = { "name":"Gardevoir", "rarity":" [Unexpected]", "TOD":"0" }

	output = ""

	if caught_fish != None:
		caught_fish_name = f"{caught_fish['name']}{caught_fish['rarity']}"
		
		if caught_fish_name in data[name]["catchlog"].keys():
			data[name]["catchlog"][caught_fish_name]+=1
			output = f"A bite! {name} has caught another {caught_fish_name}!"
			if "pub" in data[location]["requires"]:
				output = f"The barman returns and hands {name} another glass of {caught_fish_name}"
				if random.randrange(0,100)<60:
					sosfish_buffs.progressAlcohol(name, data)
			if "catears" in data[location]["requires"]:
				output = f"{caught_fish_name} happily waves {name} to come sit next to them and they have a lovely chat"
		else:
			data[name]["catchlog"][caught_fish_name]=1
			output = f"A bite! {name} has caught a {caught_fish_name}, congratulations on catching one!"
			if "pub" in data[location]["requires"]:
				output = f"The barman returns and hands {name} a glass of {caught_fish_name}, time to drink!"
			if "catears" in data[location]["requires"]:
				output = f"A spare seat! {name} has met {caught_fish_name} and they are very friendly!"

	elif "pub" in data[location]["requires"]:
		output = "It seems like the barman has forgotten about you, better order again!"
	elif "cafe" in data[location]["requires"]:
		output = randomCafeExp(name, location)
	elif "bike" not in data[name]["flags"]:
		data[name]["flags"]["bike"] = True
		output = f"A bite! {name} reels in the catch, only to discover an old bicycle! A bit of oil gets it working again, and you can now '!fish at [location]'. Try visiting other angler's locations and sharing your bait with them using '!sharebait'"
	elif "crampons" not in data[name]["flags"] and random.randrange(0,100)<10:
		data[name]["flags"]["crampons"] = True
		output = f"A bite! {name} reels in the catch, only to discover a pair of rusty climbing crampons! After cleaning them up you think they would come in handy if you ever had to climb something!"
	elif "platinumkey" not in data[name]["flags"] and "dwarven" in location.lower() and random.randrange(0,100)<10:
		data[name]["flags"]["platinumkey"] = True
		output = f"A bite! {name} reels in the catch, only to discover a beautifully smithed platinum key with 'Im Narvi hain echant' engraved upon it"
	elif "log" not in data[name]["flags"] and random.randrange(0,100)<20:
		data[name]["flags"]["log"] = True
		output = f"A bite! {name} reels in the catch, only to discover a log bleached by the sun and waves. Why not build a campfire somewhere with '!fish campfire'"
	elif "flintsteel" not in data[name]["flags"] and random.randrange(0,100)<10:
		data[name]["flags"]["flintsteel"] = True
		output = f"A bite! {name} reels in the catch, only to discover a flint and steel. You can now light a campfire with '!fish light campfire'"
	elif "catears" not in data[name]["flags"] and random.randrange(0,100)<10:
		data[name]["flags"]["catears"] = True
		output = f"A bite! {name} reels in the catch, only to discover a headband with a pair of adorable cat ears, most peculiar!"
	else:
		output = f"A bite! {name} reels in the catch, only to discover {randomItem(name, location)}"

	if "pub" not in data[location]["requires"] and "cafe" not in data[location]["requires"]:
		if (highest_common_percentage<25 and highest_noncommon_percentage<25) or (highest_common_percentage>75 and highest_noncommon_percentage>75):
			output +=f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_common_percentage)} for catching any fish"
		elif (highest_common_percentage<25 or highest_common_percentage>75) and (highest_noncommon_percentage<25 or highest_noncommon_percentage>75):
			output += f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_common_percentage)} for catching common fish, and {describeEffectiveness(highest_noncommon_percentage)} for catching uncommon fish"
		elif (highest_common_percentage<25 or highest_common_percentage>75):
			output +=f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_common_percentage)} for catching common fish"
		elif (highest_noncommon_percentage<25 or highest_noncommon_percentage>75):
			output +=f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_noncommon_percentage)} for catching uncommon fish"

	if len(data[location]["campfire"]["ingredients"])>0:
		output += f"\n{sosfish_buffs.describeStew(location, data)}"

	if "alcohol" in data[name]["buffs"]:
		output += f"\nYou are {sosfish_buffs.describeDrunkenness(name, data)}"

	output+=CheckBadgeQualification(name)

	if random.randrange(0,100)<15:
		for p in data[location]["requires"]:
			if "P_" in p:
				for poketype in sosfish_constants.pokemon:
					if poketype in p:
						poke = random.choice( sosfish_constants.pokemon[poketype] )
						timeout = 0
						while poke in data[name]["companions"] and timeout<100:
							poke = random.choice( sosfish_constants.pokemon[poketype] )
							timeout += 1

						data[name]["nearbycompanion"] = poke
						output += f"\nA {poke} peeks out at you from its hiding place! Make friends with '!fish companion {poke}'\n{PokemonURL(poke)}"

	monsterTime = numberFromString(location, 23)
	hour = current_time.hour

	if int(monsterTime) == int(hour):
		output+="\nA vast shadow slowly drifts beneath the water..."

	output += sosfish_clues.companionAdvice(data, name)

	#output+="\n\n"
	#output += f"\ncommon effectiveness: {highest_common_percentage}  noncommon effectiveness: {highest_noncommon_percentage}\n\n"

	return output



def CheckBadgeQualification(name):
	output = ""

	fish_counts = [0,0,0,0,0]

	for a in data[name]["catchlog"].keys():
		fish_counts[4]+=1
		if "legendary" in a:
			fish_counts[3]+=1
		elif "rare" in a:
			fish_counts[2]+=1
		elif "uncommon" in a:
			fish_counts[1]+=1
		else:
			fish_counts[0]+=1
	

	for a in range(len(fish_counts)):

		count_id = a
		if a>4:
			count_id=4

		if fish_counts[count_id]>=badge_scores[a] and badge_names[a] not in data[name]["flags"]:
			output += f"\n{badge_text}[{badge_names[a]}]"
			data[name]["flags"][badge_names[a]] = True


	location = data[name]["currentlocation"]
	location_all_badge_name = f"I :heart: {location}"
	location_any_badge_name = f"Visited {location}"


	if location_all_badge_name not in data[name]["flags"] and HasCaughtAllFishAtCurrentLocation(name):
		data[name]["flags"][location_all_badge_name] = True
		if "pub" in data[location]["requires"]:
			output += f"\n{badge_text}[{location_all_badge_name}] Congratulations on sampling all the alcohol at this location!"
		if "cafe" in data[location]["requires"]:
			output += f"\n{badge_text}[{location_all_badge_name}] Congratulations on catching all the locals at this location!"
		else:
			output += f"\n{badge_text}[{location_all_badge_name}] Congratulations on catching all the fish at this location!"

	if location != name:
		if location_any_badge_name not in data[name]["flags"] and HasCaughtAnyFishAtCurrentLocation(name):
			data[name]["flags"][location_any_badge_name] = True
			output += f"\n{badge_text}[{location_any_badge_name}]"


	if data[name]["currentcompanion"].lower() in sosfish_constants.pokemon_badges.keys():
		pokebadge = sosfish_constants.pokemon_badges[ data[name]["currentcompanion"].lower() ]
		if pokebadge not in data[name]["flags"]:
			data[name]["flags"][pokebadge] = True
			output += f"\n{badge_text}[{pokebadge}]"

	if name.lower() in sosfish_constants.helpful_people and "Helpful" not in data[name]["flags"]:
		data[name]["flags"]["Helpful"] = True
		output += f"\n{badge_text}[Helpful]"

	saveUserData(name, data)
	return output
	
def HasCaughtAllFishAtCurrentLocation(name):
	location = data[name]["currentlocation"]

	for caught_fish in data[location]["fish"]:
		caught_fish_name = f"{data[location]['fish'][caught_fish]['name']}{data[location]['fish'][caught_fish]['rarity']}"
		if caught_fish_name not in data[name]["catchlog"].keys():
			return False

	return True

def HasCaughtAnyFishAtCurrentLocation(name):
	location = data[name]["currentlocation"]

	for caught_fish in data[location]["fish"]:
		caught_fish_name = f"{data[location]['fish'][caught_fish]['name']}{data[location]['fish'][caught_fish]['rarity']}"
		if caught_fish_name in data[name]["catchlog"].keys():
			return True

	return False


def ShareBait(name):

	output = ""

	location = data[name]["currentlocation"]

	changes = False

	sbait = data[name]["baitbox"][str(0)]
	output += f"\n{name} offers to share {sbait} with anyone nearby"

	for a in data.keys():
		if data[a]["currentlocation"] == location and a != name:
			
			hasBait = False
			for i in data[a]["baitbox"]:
				if sbait in data[a]["baitbox"][i]:
					hasBait = True

			if hasBait:
				output += f"\n{a} already has {sbait}"
			else:
				output += f"\n{a} now has {sbait} in their baitbox!"
				data[a]["baitbox"][str(len(data[a]["baitbox"]))] = sbait
				saveUserData(a, data)
				if "Go team!" not in data[name]["flags"]:
					output +=f"\n {badge_text}[Go team!]"
					data[name]["flags"]["Go team!"] = True
					saveUserData(name, data)

	if output == "":
		output = f"{name} wishes someone else was around they could share bait with"

	return output

def Fish(name, parameters, mention_author=None, channel=None):
	parameters = parameters.lower()
	if not name in data:
		buildProfile(name)
	amendProfile(name)
	amendProfile(data[name]["currentlocation"])

	if " companion " in parameters:

		chosenPoke = ""
		for poke in sosfish_constants.pokemon["ALL"]:
			if poke.lower() in parameters:
				chosenPoke = poke

		if chosenPoke=="":
			return f"I do not recognize that name"

		if chosenPoke in data[name]["companions"]:
			data[name]["currentcompanion"] = chosenPoke
			saveUserData(name, data)
			return f"{chosenPoke} is now the companion of {name}\n{PokemonURL(chosenPoke)}{CheckBadgeQualification(name)}"

		for catch in data[name]["catchlog"].keys():
			if chosenPoke.lower() in catch.lower():
				data[name]["currentcompanion"] = chosenPoke
				data[name]["companions"].append(chosenPoke)
				saveUserData(name, data)
				return f"{name} makes friends with a {chosenPoke} that was caught, it is now a companion\n{PokemonURL(chosenPoke)}{CheckBadgeQualification(name)}"

		if data[name]["nearbycompanion"] == chosenPoke:
			data[name]["currentcompanion"] = chosenPoke
			data[name]["companions"].append(chosenPoke)
			data[name]["nearbycompanion"] = ""
			saveUserData(name, data)
			return f"{name} makes friends with the {chosenPoke}, it is now a companion\n{PokemonURL(chosenPoke)}{CheckBadgeQualification(name)}"

		if chosenPoke!="":
			return f"{chosenPoke} does not appear to be anywhere near {name}"

		if data[name]["nearbycompanion"] == "":
			return "No companions nearby"

		return "I do not recognize that name"
	
	if " sell" in parameters:
		if "Market" not in data[name]["currentlocation"]:
			return "You must be at the market to sell!"

		output = sosfish_market.Sell(data, name)
		saveUserData(name, data)
		return output

	if " equip" in parameters:
		if "last_item" not in data[name]:
			return "No item to equip!"

		item = data[name]["last_item"]
		
		del data[name]["last_item"]

		data[name]["equipped"][item] = True

		saveUserData(name,data)
		return f"{name} equips {item}"

	if "status" in parameters:

		saveUserData(name, data)
		status_output = Status(name, data)

		if len(status_output.splitlines()) > 22 and DEBUG == False:
			status_output = Status(name, data, True)
			#commented out because server down
			if False and len(status_output.splitlines()) > 22:
				status_output = Status(name, data, True, False, True)
				if len(status_output.splitlines()) > 22:
					status_output = Status(name, data, True, True, True)
				status_output += f"http://mena.to/fishinfo/{name}".replace(" ", "%20")
			
		return status_output

	current_time = datetime.datetime.now()

	if data[name]["catchtime"]==0:
		catch_time = 0
	else:
		catch_time = datetime.datetime.strptime( data[name]["catchtime"] ,"%Y-%m-%d-%H-%M")
	
	
	location = ""
	usebait = ""

	if " at " in parameters:
		new_location = parameters[parameters.index(" at ")+4:]
		if "using" in new_location:
			new_location = new_location.split("using")[0].strip()
		if "with" in new_location:
			new_location = new_location.split("with")[0].strip()

		new_location = new_location.rstrip("'s")
		new_location = new_location.rstrip("s")
		#print(new_location)
		for loc in data.keys():
			if (len(new_location)>3 and new_location.lower() in loc.lower()) or new_location.lower()==loc.lower():
				#print(f"from location {new_location} matched {loc}\n")

				if location=="" or abs(len(new_location)-len(location))>abs(len(new_location)-len(loc)):
					location = loc
		if location == "":
			return "I don't recognize that location"

	if location != "":
		amendProfile(location)


	if (" using " in parameters) or (" with " in parameters):
		
		if (" using " in parameters):
			new_bait = parameters[parameters.index(" using ")+7:]
		elif (" with " in parameters):
			new_bait = parameters[parameters.index(" with ")+6:]

		if "at" in new_bait:
			new_bait = new_bait.split("at")[0].strip()
		if len(new_bait)>3:
			for bt in bait:
				if new_bait.lower() in bt.lower():
					print(f"from baits {new_bait} matched {bt}\n")
					usebait = bt
			for bt in baitoftheweek:
				if new_bait.lower() in bt.lower():
					print(f"from baits {new_bait} matched {bt}\n")
					usebait = bt

		if usebait == "":
			return "I don't recognize that bait"

	#print(f"location [{location}]")
	#print(f"bait [{bait}]")

	changed_location = location!="" and location != data[name]["currentlocation"]
	changed_bait = usebait!="" and usebait != data[name]["currentbait"]

	if changed_location:
		for req in data[location]["requires"]:
			if req == "bike" and "bike" not in data[name]["flags"]:
				return f"{name} doesn't have a mode of transport to use the command '!fish at' yet"
			if req == "surfboard" and "surfboard" not in data[name]["flags"]:
				return f"{name} needs a way to cross the water to reach this place"
			if req == "crampons" and "crampons" not in data[name]["flags"]:
				return f"There doesn't seem to be any way for {name} to climb up to this location"
			if req == "platinumkey" and "platinumkey" not in data[name]["flags"]:
				return f"{name} is not yet a friend of the dwarves, so cannot pass this way"
			if req == "catears" and "catears" not in data[name]["flags"]:
				return f"{name} spots a cute looking cafe and approaches, but is too embarassed to walk in without proper attire"

	

	if changed_bait:
		hasBait = False
		for b in data[name]["baitbox"].keys():
			if data[name]["baitbox"][b] == usebait:
		 		hasBait=True;

		if hasBait == False:
			return f"{name} you do not have that bait. Try asking someone to !sharebait when you are at the same location to get their starting bait"

	# --- campfire stuff ---
	if location != "":
		amendProfile(location)

	camp = sosfish_buffs.campfire_main_loop(name, location, parameters, data)
	
	if camp != None:


		if location == "":
			saveUserData(data[name]["currentlocation"], data)
		else:
			saveUserData(location, data)
		saveUserData(name, data)
		return camp
	
	if " leaderboards" in parameters:
		if ("Salt Mine" in location or "Salt Mine" in data[name]["currentlocation"]):
			output = CheckLeaderBoard(data, name)	
			saveUserData(name, data)
			return output
		else:
			return "You must visit the Salt Mine to check the leaderboards"

	output = ""
	if catch_time == 0 or changed_location or changed_bait:

		if changed_location:
			data[name]["nearbycompanion"] = ""

		output = CastRod(name, location, usebait, mention_author, channel)
		saveUserData(name, data)
	elif catch_time<current_time:
		output = Catch(name)
		data[name]["catchtime"] = 0
		saveUserData(name, data)
	else:
		if "pub" in data[data[name]["currentlocation"]]["requires"]:
			output = f"{name} waits for a drink.."
		elif "cafe" in data[data[name]["currentlocation"]]["requires"]:
			output = f"{name} looks around.."
		else:
			output = f"{name} waits for a fish.."
	return output

timer_tasks = {}

data = loadUserData();

houses = loadList("houses")
descriptors = loadList("descriptors")
waterbodies = loadList("waterbodies")
fish = loadList("fish")
bait = loadList("bait")
baitoftheweek = loadList("baitoftheweek")
premadelocations = updatePremadeLocations()
sosfish_constants.pokemon = loadData("/fishingdata/pokemon")


if DEBUG==True:
	print(Fish("technicalty", "!fish at kanna"))
	#print(Fish("technicalty", "!fish campfire"))
	#print(Fish("technicalty", "!fish light campfire"))
	#print(Fish("technicalty", "!fish cook oregano"))
	#print(helpString("technicalty"))
#print(Fish("dovah chief", "!fish"))
#print(Fish("dovah chief", "!fish at surf shack"))
#(Fish("dovah chief", "!fish at epic bait"))
#print(Fish("dovah chief", "!fish status"))
#print(ShareBait("dovah chief"))

#print(Fish("dovah chief", "!fish status"))
#print(Fish("aster", "!fish status"))

#print(Fish("aster iris", ""))
#print(Fish("nemphtis", ""))
#print(Fish("kyap", ""))
#print(Fish("doc no", ""))