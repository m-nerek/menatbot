DEBUG = True

import re
import os
import datetime
import json
import random
import urbandictionary
import math
import asyncio
from fishstatus import Status

if DEBUG == False:
	import sosmarkov

dir_path = os.path.dirname(os.path.realpath(__file__))

help_string = f"""Fishing commands:
        `!fish` to get started fishing
        `!fish status` to see your inventory
        `!sharebait` to share your starter bait with anyone at your location
        You will eventually unlock the ability to:
        `!fish at [location]` The location can be the ID of another user
        `!fish with/using [bait]` You need to have the bait in your baitbox
        `!fish at [location] with/using [bait]`
        """

def loadList(file, keepcaps = False):
	f = open(f"{dir_path}/fishingdata/{file}.txt", "r")

	if keepcaps==True:
		data = [line.strip() for line in f]
	else:
		data = [line.strip().lower() for line in f]

	f.close()
	return data 

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

def randomItem():
	i = random.randrange(0,5+1)

	if i<=1:
		return f"a flyer for '{ random.choice(premadelocations) }', maybe you should visit sometime"
	if i<=2:
		return f"{randomUser()}'s wellington boot"
	if i<=3:
		return f"a keyring with a tag that says '{urbandictionary.random()[0].word}' in worn letters"
	if i<=4:
		return f"a hat with '{urbandictionary.random()[0].word}' emblazoned across the front"
	if i<=5:
		return f"a bottle containing a message that reads '{sosmarkov.sentence(sosmarkov.models['general'])}'"



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

def matchScore(tomatch, string, maxlen):
	tomatchlower = re.sub(r'\W+', '', tomatch.lower())[:maxlen]
	stringlower = string.lower()
	return len(re.findall(f"[{tomatchlower}]", stringlower))

def describeTime(hour):
	if hour<6 or hour>21:
		return "As the moon reflects off the dark water"
	if hour<9:
		return "As the sun rises on the horizon"
	if hour>18:
		return "As the sun sets over the water"
	return "It is a lovely day when"

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
				data[name]["fish"][f] = {}
				data[name]["fish"][f]["name"] = lines[i]
				data[name]["fish"][f]["TOD"] = numberFromString(data[name]["fish"][f]["name"],24)
				data[name]["fish"][f]["rarity"] = describeRarity(f)
				i+=1
		else:
			i+=1

	return loaded_locations


def buildProfile(name):
	#print("building profile")
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
		data[name]["fish"][i] = {}
		data[name]["fish"][i]["name"] = matchFish(name, i)
		data[name]["fish"][i]["TOD"] = numberFromString(data[name]["fish"][i]["name"],24)
		data[name]["fish"][i]["rarity"] = describeRarity(i)

	return ""


async def BiteMessageCallback(mention_author, channel, time):
	try:
		await asyncio.sleep(time)
		await channel.send(f"{mention_author} your line twitches")
	except:
		return

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
		if "bike" in data[location]["requires"]:
			arrival_text="arrives on a bicycle, "
		elif "surfboard" in data[location]["requires"]:
			arrival_text="paddles across the water and rides the surf in, "
		elif "crampons" in data[location]["requires"]:
			arrival_text="scales the sheer cliffs and hikes to the water, "
		
	if "surf shack" in location.lower() and "surfboard" not in data[name]["flags"]:
		output = data[location]["description"]
		output += f" {describeTime(current_time.hour)} {name} {arrival_text}browses a bit and after some deliberation buys a { random.choice(descriptors) } second hand surfboard in the sale"
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
			output = data[location]["description"]
			output += f" {describeTime(current_time.hour)} {name} {arrival_text}stops for a chat and buys the bait of the week '{bait_of_the_week}'"
			data[name]["baitbox"][str(len(data[name]["baitbox"]))] = bait_of_the_week
			return output

	if "gardevoir" in location.lower():
		weekherbindex = (math.floor((current_time.day-7)/7+current_time.month*4) % len(herbs))
		herb_of_the_week = herbs[ weekherbindex ]
		
		if herb_of_the_week not in data[name]["flags"]:
			output = data[location]["description"]
			output += f" {describeTime(current_time.hour)} {name} {arrival_text}notices that the '{herb_of_the_week}' has grown a lot this week, and picks some"
			data[name]["flags"][herb_of_the_week] = True
			return output

	if "spicy sailboat" in location.lower():
		weekspiceindex = (math.floor((current_time.day-7)/7+current_time.month*4) % len(spices))
		spice_of_the_week = spices[ weekspiceindex ]
		
		if spice_of_the_week not in data[name]["flags"]:
			output = data[location]["description"]
			output += f" {describeTime(current_time.hour)} {name} {arrival_text}stops for a chat and buys the spice of the week '{spice_of_the_week}'"
			data[name]["flags"][spice_of_the_week] = True
			return output


	output = data[location]["description"]
	output += f" {describeTime(current_time.hour)} {name} {arrival_text}settles down to fish and casts a rod baited with {data[name]['currentbait']} into the water"

	secs = 60*5 + (100-max(FishingOdds(name))) * 3

	if DEBUG==True:
		secs = 0

	#print(f"seconds: {secs}")
	catchtime = datetime.datetime.now() + datetime.timedelta(seconds = secs)

	if channel != None:
		if name in timer_tasks:
			timer_tasks[name].cancel()
			del timer_tasks[name]

		timer_tasks[name] = asyncio.get_event_loop().create_task(BiteMessageCallback(mention_author, channel, secs))

	data[name]["catchtime"] = f"{catchtime.year}-{catchtime.month}-{catchtime.day}-{catchtime.hour}-{catchtime.minute}"
	return output

base_catch_chance = [70,70,30,20, 10]
time_of_day_falloff = [14,14,12,10,6]

def FishingOdds(name):

	odds = [0,0,0,0,0]

	location = data[name]["currentlocation"]
	currentbait = data[name]["currentbait"]

	for f in data[location]["fish"]:
		fishname = data[location]['fish'][f]['name']
		
		baitscore = min(3, matchScore(fishname, currentbait, 3)) / 3
		
		hoursfromoptimal = abs(datetime.datetime.now().hour-int(data[location]['fish'][f]['TOD']))

		if hoursfromoptimal>12:
			hoursfromoptimal = abs(24-hoursfromoptimal)

		timescore = max(0,time_of_day_falloff[int(f)]-hoursfromoptimal) / time_of_day_falloff[int(f)]

		chance = 100
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
			caught_fish = f

	if "gardevoir" in location.lower() and random.randrange(0,1000)<10:
		caught_fish = { "name":"Gardevoir", "rarity":" [Unexpected]", "TOD":"0" }

	output = ""

	if caught_fish != None:
		caught_fish_name = f"{data[location]['fish'][caught_fish]['name']}{data[location]['fish'][caught_fish]['rarity']}"
		

		if caught_fish_name in data[name]["catchlog"].keys():
			data[name]["catchlog"][caught_fish_name]+=1
			output = f"A bite! {name} has caught another {caught_fish_name}!"
		else:
			data[name]["catchlog"][caught_fish_name]=1
			output = f"A bite! {name} has caught a {caught_fish_name}, congratulations on catching one!"

	elif "bike" not in data[name]["flags"]:
		data[name]["flags"]["bike"] = True
		output = f"A bite! {name} reels in the catch, only to discover an old bicycle! A bit of oil gets it working again, and you can now '!fish at [location]'. Try visiting other angler's locations and sharing your bait with them using '!sharebait'"
	elif "crampons" not in data[name]["flags"] and random.randrange(0,100)<10:
		data[name]["flags"]["crampons"] = True
		output = f"A bite! {name} reels in the catch, only to discover a pair of rusty climbing crampons! After cleaning them up you think they would come in handy if you ever had to climb something!"
	elif "platinumkey" not in data[name]["flags"] and "dwarven" in location.lower() and random.randrange(0,100)<10:
		data[name]["flags"]["platinumkey"] = True
		output = f"A bite! {name} reels in the catch, only to discover a beautifully smithed platinum key with 'Im Narvi hain echant' engraved upon it"
	else:
		output = f"A bite! {name} reels in the catch, only to discover {randomItem()}!"

	
	if (highest_common_percentage<25 and highest_noncommon_percentage<25) or (highest_common_percentage>75 and highest_noncommon_percentage>75):
		output +=f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_common_percentage)} for catching any fish"
	elif (highest_common_percentage<25 or highest_common_percentage>75) and (highest_noncommon_percentage<25 or highest_noncommon_percentage>75):
		output += f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_common_percentage)} for catching common fish, and {describeEffectiveness(highest_noncommon_percentage)} for catching uncommon fish"
	elif (highest_common_percentage<25 or highest_common_percentage>75):
		output +=f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_common_percentage)} for catching common fish"
	elif (highest_noncommon_percentage<25 or highest_noncommon_percentage>75):
		output +=f"\nUsing this bait at this time of day seems to be {describeEffectiveness(highest_noncommon_percentage)} for catching uncommon fish"

	output+=CheckBadgeQualification(name)
	output+="\n\n"
	#output += f"\ncommon effectiveness: {highest_common_percentage}  noncommon effectiveness: {highest_noncommon_percentage}\n\n"

	return output


badge_names = ["Common People", "Uncommon Phenomonon", "A Rare Talent", "Absolute Legend", "Rod God", "Fish Whisperer", "Grandmaster Angler" ]
badge_scores = [3,3,1,1,10,20,60]
badge_text = "You have been awarded a shiny new badge that reads: "

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
		output += f"\n{badge_text}[{location_all_badge_name}] Congratulations on catching all the fish at this location!"

	if location != name:
		if location_any_badge_name not in data[name]["flags"] and HasCaughtAnyFishAtCurrentLocation(name):
			data[name]["flags"][location_any_badge_name] = True
			output += f"\n{badge_text}[{location_any_badge_name}]"

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

	if "status" in parameters:
		status_output = Status(name, data, herbs, spices, badge_names)

		if len(status_output.splitlines()) > 22:
			status_output = Status(name, data, herbs, spices, badge_names, True)
			if len(status_output.splitlines()) > 22:
				status_output = Status(name, data, herbs, spices, badge_names, True, False, True)
				if len(status_output.splitlines()) > 22:
					status_output = Status(name, data, herbs, spices, badge_names, True, True, True)
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
		print(new_location)
		for loc in data.keys():
			if (len(new_location)>3 and new_location.lower() in loc.lower()) or new_location.lower()==loc.lower():
				#print(f"from location {new_location} matched {loc}\n")

				if location=="" or abs(len(new_location)-len(location))>abs(len(new_location)-len(loc)):
					location = loc
		if location == "":
			return "I don't recognize that location"

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


	if changed_bait:
		hasBait = False
		for b in data[name]["baitbox"].keys():
			if data[name]["baitbox"][b] == usebait:
		 		hasBait=True;

		if hasBait == False:
			return f"{name} you do not have that bait. Try asking someone to !sharebait when you are at the same location to get their starting bait"

	output = ""
	if catch_time == 0 or changed_location or changed_bait:
		output = CastRod(name, location, usebait, mention_author, channel)
		saveUserData(name, data)
	elif catch_time<current_time:
		output = Catch(name)
		data[name]["catchtime"] = 0
		saveUserData(name, data)
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
herbs = loadList("herbs")
spices = loadList("spices")
premadelocations = updatePremadeLocations()


if DEBUG==True:
	print(Fish("Kyap", "!fish status"))
	print(Fish("Kanna", "!fish status"))
	print(Fish("technicalty", "!fish status"))
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