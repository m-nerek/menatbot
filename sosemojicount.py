import re
import os
import json
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
log_counter = 0

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

def logEmoji(string, guild):
	guild = str(guild)
	month = str(getMonth())

	if guild not in emojiCounts:
		emojiCounts[guild] = {}

	if month not in emojiCounts[guild]:
		emojiCounts[guild][month] = {}

	emojis = findCleanEmojis(string)
	made_changes = False
	global log_counter
	log_counter+=1
	for e in emojis:
		if e not in emojiCounts[guild][month]:
			emojiCounts[guild][month][e] = 0
		emojiCounts[guild][month][e] += 1
		made_changes = True
		
	if made_changes and log_counter>20:
		saveData("emojicounts", emojiCounts)
		log_counter=0


def listEmoji(guild):

	output = ""

	if str(guild) not in emojiCounts:
		emojiCounts[str(guild)] = {}

	month = str(getMonth())
	if month not in emojiCounts[str(guild)]:
		emojiCounts[str(guild)][month] = {}

	guild_emoji_names = {}
	if guild is not None:
		guild_emoji_names = [x.name for x in guild.emojis]

		for e in guild_emoji_names:
			if e not in emojiCounts[str(guild)][month]:
				emojiCounts[str(guild)][month][e] = 0

	top = sorted(emojiCounts[str(guild)][month].items(), key=lambda x: x[1], reverse=True)[:5]
	bottom = sorted(emojiCounts[str(guild)][month].items(), key=lambda x: x[1])[:10]
	
	output+= "Top Emojis:\n"
	for e in top:
		output += f" - {e[0]} ({e[1]})\n"

	output+= "Bottom Emojis:\n"
	for e in bottom:
		output += f" - {e[0]} ({e[1]})\n"


	return output

emojiCounts = loadData("emojicounts")


#log_counter = 20
#logEmoji(" <a:turkic:1783>", None)
#print(listEmoji(None))

#print(getMonth())