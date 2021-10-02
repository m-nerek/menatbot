import json
import os
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))



data = {}

TEST = False

INITIAL_CHECK = True

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


def QuitLog(guild):
	global INITIAL_CHECK
	serverName = str(guild.id)

	if serverName not in data:
		data[serverName] = {}
		data[serverName]["USERS"] = {}
		data[serverName]["LOG"] = []

	if len(guild.members) != len(data[serverName]["USERS"]) or INITIAL_CHECK:

		INITIAL_CHECK = False
		print(f"checking for member changes")
		#find missing users
		for x in data[serverName]["USERS"].keys():
			
			if not [y for y in guild.members if x == str(y.mention)]:
				# add quit to the log
				print(f"player {data[serverName]['USERS'][x]} quit")
				entry = {}
				time = datetime.datetime.now()
				entry["time"] = f"{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}"
				entry["id"] = x
				entry["name"] = data[serverName]["USERS"][x]
				entry["type"] = "QUIT"
				data[serverName]["LOG"].append(entry)

		#find new users
		for x in guild.members:
			if str(x.mention) not in data[serverName]["USERS"].keys():
				#add join to the log
				print(f"player {x.name} joined")
				entry = {}
				time = datetime.datetime.now()
				entry["time"] = f"{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}"
				entry["id"] = str(x.mention)
				entry["name"] = x.name
				entry["type"] = "JOIN"
				data[serverName]["LOG"].append(entry)


		data[serverName]["USERS"] = {}
		for x in guild.members:
			data[serverName]["USERS"][str(x.mention)] = x.name;

		saveData("quitlog", data)


def RecentActivity(guild, parameters):
	print("--- activity check ---")
	QuitLog(guild)
	serverName = str(guild.id)

	for s in data.keys():
		if s in parameters:
			serverName = s

	time = datetime.datetime.now()
	ts = f"{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}"

	output_text = (f"current server time: {ParseTimeString(ts)}\n")

	for x in data[serverName]["LOG"][-10:]:
		output_text += ParseTimeString(x["time"])+" "+x["name"]+" "+x["type"]+"\n"

	return output_text

class Guild:
	def __init__(self):
		self.id = ""
		self.members = []
	pass

class Member:
	def __init__(self, name, mention):
		self.name = name
		self.mention = mention
	pass



def ParseTimeString(time):
	t = time.split("-")
	if(len(t)>3):
		return f"{t[2]}/{t[1]}/{t[0]} {t[3]}:{int(t[4]):02d}"
	else:
		return ""

data = loadData("quitlog")

if TEST:

	guild1 = Guild()
	guild1.id = "728683307881070643"
	guild1.members.append(Member("test1", "1234"))
	guild1.members.append(Member("test2", "12345"))
	guild1.members.append(Member("test3", "123456"))

	print(RecentActivity(guild1, ""))

	print(RecentActivity(guild1, ""))


	guild2 = Guild()
	guild2.id = "728683307881070643"
	guild2.members.append(Member("test4", "12349"))
	guild2.members.append(Member("test2", "12345"))
	guild2.members.append(Member("test3", "123456"))
	guild2.members.append(Member("test5", "123497857"))

	print(RecentActivity(guild2, ""))



	