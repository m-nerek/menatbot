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

def getYear():
	return datetime.datetime.now().year

def logEmoji(string, guild, user):
	global last_user
	global last_user_emote_count
	global log_counter


	guildstr = str(guild.id)
	month = str(getMonth())
	year = str(getYear())

	if guildstr not in emojiCounts:
		emojiCounts[guildstr] = {}

	if month not in emojiCounts[guildstr]:
		emojiCounts[guildstr][month] = {}

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
		if e not in emojiCounts[guildstr][month]:
			emojiCounts[guildstr][month][e] = 0
		emojiCounts[guildstr][month][e] += 1

		if "turkic" not in e:
			last_user_emote_count+=1
		made_changes = True
	
	#print(f"logged {len(emojis)} emojis (count {log_counter})")
		
	if made_changes and log_counter>20:

		guild_emoji_names = [x.name for x in guild.emojis]
		for e in guild_emoji_names:
			if e not in emojiCounts[guildstr][month]:
				emojiCounts[guildstr][month][e] = 0
				print(f"adding emoji to db {e}")

		saveData(f"emojidata/emojicounts_{year}_{month}_{guildstr}",emojiCounts[guildstr][month])
		log_counter=0

def serverEmoji(guild, parameters):
	guild_emojis = [x.name for x in guild.emojis]
	output = ""
	for e in guild_emojis:
		output+=f" {e} :"

	output+=f"\n {len(guild_emojis)} total"
	return output


def listEmoji(guild, parameters):

	output = ""

	if str(guild.id) not in emojiCounts:
		emojiCounts[str(guild.id)] = {}
	if str(getMonth()) not in emojiCounts[str(guild.id)]:
		emojicounts[str(guild.id)][str(getMonth())] = {}
	month = str(getMonth())

	list_month = month
	list_year = str(getYear())
	parameters = parameters.lower()

	for y in range(2020,2100):
		if str(y) in parameters:
			list_year = str(y)

	if "dec" in parameters:
		list_month = 12
	elif "nov" in parameters:
		list_month = 11
	elif "oct" in parameters:
		list_month = 10
	elif "sep" in parameters:
		list_month = 9
	elif "aug" in parameters:
		list_month = 8
	elif "jul" in parameters:
		list_month = 7
	elif "jun" in parameters:
		list_month = 6
	elif "may" in parameters:
		list_month = 5
	elif "apr" in parameters:
		list_month = 4
	elif "mar" in parameters:
		list_month = 3
	elif "feb" in parameters:
		list_month = 2
	elif "jan" in parameters:
		list_month = 1

	list_month = str(list_month)

	if "recent" in parameters:
		output+=f"Emoji counts for the last 3 months\n"

		list_month=int(list_month)-3
		if list_month<1:
			list_month+=12
			list_year=str(int(list_year)-1)

		list_month = str(list_month)
		for i in range(1,3):

			
			filename = f"{dir_path}/emojidata/emojicounts_{list_year}_{list_month}_{str(guild.id)}.json"
			try:
				with open(filename, 'r') as f:
					data = json.load(f)
					if i==1:
						list_data = data
					else:
						for d in data.keys():
							if d in list_data.keys():
								list_data[d] = int(list_data[d])+int(data[d])
						
			except:
				return f"I can't find any data for {list_month}/{list_year} server {str(guild.id)}!"

			list_month=int(list_month)+1
			if(int(list_month)>12):
				list_month = 1
				list_year = str(int(list_year)+1)
			list_month = str(list_month)


	else:
		output+=f"Emoji counts for {month}/{year}\n"
		list_data = emojiCounts[str(guild.id)][month]

		if list_month != month and list_year != getYear():
			filename = f"{dir_path}/emojidata/emojicounts_{list_year}_{list_month}_{str(guild.id)}.json"
			try:
				with open(filename, 'r') as f:
					list_data = json.load(f)
			except:
				return f"I can't find any data for {list_month}/{list_year} server {str(guild.id)}!"
	

	bottom_value = 0
	bottom_count = 0

	while bottom_count<20:
		for e in list_data:
			if list_data[e] == bottom_value:
				bottom_count+=1
		bottom_value += 1

	if bottom_count>40:
		bottom_count = 40


	top = sorted(list_data.items(), key=lambda x: x[1], reverse=True)[:5]
	bottom = sorted(list_data.items(), key=lambda x: x[1])[:bottom_count]
	guild_emojis = [x.name for x in guild.emojis]

	#print(f"---{len(guild_emojis)} emojis compared")


	output+= "Top Emojis:\n"
	for e in top:
		if e[0] in guild_emojis:
			output += f" - **{e[0]}** ({e[1]})"
		else:
			output += f" - *{e[0]}* ({e[1]})"

	output+= "\n\nBottom Emojis:\n"
	for e in bottom:
		if e[0] in guild_emojis:
			output += f" - **{e[0]}** ({e[1]})"
		else:
			output += f" - *{e[0]}* ({e[1]})"


	return output

emojiCounts = {}

dir = f"{dir_path}/emojidata/"
for filename in os.listdir(dir):
	with open(os.path.join(dir, filename), 'r') as f:
		name = filename[:-5]

		parts = name.split("_")
		year = parts[1]
		month = parts[2]
		guild = "".join(parts[3:])

		if year == str(getYear()) and month == str(getMonth()):
			emojiCounts[str(guild)] = {}
			emojiCounts[str(guild)][month] = {}
			emojiCounts[str(guild)][month] = json.load(f)

		

		#dat[name] = loadData(f"emojidata/{name}")

#log_counter = 20
#logEmoji(" <a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783><a:turkic:1783>", None, "Tech")


#print(listEmoji("People Of Salt", "jan 2020"))

#print(getMonth())