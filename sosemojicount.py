import re
import os
import json
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
log_counter = 0
last_user = ""
last_user_emote_count = 0

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

def findCleanEmojis(string):
	emojis = re.findall( r"<a?:[^:\s]*(?:::[^:\s]*)*:[0-9]+>", string)
	for e in range(len(emojis)):
		emojis[e] = emojis[e][emojis[e].find(':')+1:emojis[e].rfind(':')]
	return emojis

def getMonth():
	return datetime.datetime.now().month

def logEmoji(string, guild, user):
	global last_user
	global last_user_emote_count
	global log_counter


	guild = str(guild)
	month = str(getMonth())

	if guild not in emojiCounts:
		emojiCounts[guild] = {}

	if month not in emojiCounts[guild]:
		emojiCounts[guild][month] = {}

	emojis = findCleanEmojis(string)
	made_changes = False
	
	
	if len(emojis)<1:
		return

	#print (f"{user} adding {len(emojis)} emojis  previous user: {last_user} at {last_user_emote_count} emojis, save counter {log_counter}")

	if str(user) not in last_user:
		last_user_emote_count = 0
		last_user = str(user)

	if last_user_emote_count>=3:
		return

	emojis = emojis[:(3-last_user_emote_count)]

	log_counter+=1
	for e in emojis:
		if e not in emojiCounts[guild][month]:
			emojiCounts[guild][month][e] = 0
		emojiCounts[guild][month][e] += 1

		if "turkic" not in e:
			last_user_emote_count+=1
		made_changes = True
		#print(f"logged {len(emojis)} emojis")
		
	if made_changes and log_counter>20:
		saveData("emojicounts", emojiCounts)
		log_counter=0
		#print("saved emojis")


def listEmoji(guild, parameters):


	output = ""

	if str(guild) not in emojiCounts:
		emojiCounts[str(guild)] = {}

	month = str(getMonth())
	list_month = month

	parameters = parameters.lower()

	if "12" in parameters or "dec" in parameters:
		list_month = 12
	elif "11" in parameters or "nov" in parameters:
		list_month = 11
	elif "10" in parameters or "oct" in parameters:
		list_month = 10
	elif "9" in parameters or "sep" in parameters:
		list_month = 9
	elif "8" in parameters or "aug" in parameters:
		list_month = 8
	elif "7" in parameters or "jul" in parameters:
		list_month = 7
	elif "6" in parameters or "jun" in parameters:
		list_month = 6
	elif "5" in parameters or "may" in parameters:
		list_month = 5
	elif "4" in parameters or "apr" in parameters:
		list_month = 4
	elif "3" in parameters or "mar" in parameters:
		list_month = 3
	elif "2" in parameters or "feb" in parameters:
		list_month = 2
	elif "1" in parameters or "jan" in parameters:
		list_month = 1

	list_month = str(list_month)

	if month not in emojiCounts[str(guild)]:
		emojiCounts[str(guild)][month] = {}

	if list_month not in emojiCounts[str(guild)]:
		return "No data for that month!"

	guild_emoji_names = {}
	if guild is not None:
		guild_emoji_names = [x.name for x in guild.emojis]

		for e in guild_emoji_names:
			if e not in emojiCounts[str(guild)][list_month]:
				emojiCounts[str(guild)][list_month][e] = 0

	bottom_count = 0
	for e in emojiCounts[str(guild)][list_month]:
		if emojiCounts[str(guild)][list_month][e] == 0:
			bottom_count+=1

	if bottom_count<10:
		bottom_count = 10

	top = sorted(emojiCounts[str(guild)][list_month].items(), key=lambda x: x[1], reverse=True)[:5]
	bottom = sorted(emojiCounts[str(guild)][list_month].items(), key=lambda x: x[1])[:bottom_count]
	
	output+= "Top Emojis:\n"
	for e in top:
		output += f" - {e[0]} ({e[1]})"

	output+= "Bottom Emojis:\n"
	for e in bottom:
		output += f" - {e[0]} ({e[1]})"


	return output

emojiCounts = loadData("emojicounts")


#log_counter = 20
#logEmoji(" <a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783>", None, "Tech")


#print(listEmoji(None))

#print(getMonth())