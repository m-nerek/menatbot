import json
import os
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))

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


data = loadData("quitlog")


def QuitLog(guild):

	serverName = str(guild.id)

	if serverName not in data:
		data[serverName] = {}
		data[serverName]["USERS"] = {}
		data[serverName]["LOG"] = []

	if len(guild.members) != len(data[serverName]["USERS"]):

		if len(guild.members)<len(data[serverName]["USERS"]):
			#find missing user
			for x in data[serverName]["USERS"].keys():
				found = False
				for y in guild.members:
					if x in str(y.mention):
						found = True
						break

				if not found:
					# add quit to the log
					entry = {}
					time = datetime.datetime.now()
					entry["time"] = f"{time.year}-{time.month}-{time.day}-{time.hour}-{time.minute}"
					entry["id"] = x
					entry["name"] = data[serverName]["USERS"][x]
					entry["type"] = "QUIT"
					data[serverName]["LOG"].append(entry)

		if len(guild.members)>len(data[serverName]["USERS"]):
			#find new user
			for x in guild.members:
				if str(x.mention) not in data[serverName]["USERS"].keys():
					#add join to the log
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