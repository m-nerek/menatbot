import os
import random

dir_path = os.path.dirname(os.path.realpath(__file__))
def loadList(file, keepcaps = False):
	f = open(f"{dir_path}/{file}.txt", "r")

	if keepcaps==True:
		data = [line.strip() for line in f]
	else:
		data = [line.strip().lower() for line in f]

	f.close()
	return data 

chars = loadList("sfvchars", True)



def CharSelect(user, message):

	
	name = message[message.index("random select")+14:]
	if(len(name)<2):
		name = user


	character = random.choice(chars)

	adjectives = ["boring", "exciting", "disgusting", "ridiculous", "cheap", "broken", "lame", "tedious", "filthy"]

	adjective = random.choice(adjectives)

	responses = []
	responses.append(f"{name} looks like a filthy {character} main to me")
	responses.append(f"{name} probably robs people with {character}")
	
	responses.append(f"{name} would play a {adjective} character like {character}")
	responses.append(f"{name} would play a {adjective} character like {character} for sure")
	responses.append(f"{name} would play a {adjective} character like {character}")
	responses.append(f"{name} would play a {adjective} character like {character} for certain")
	responses.append(f"{name} would play a {adjective} character like {character} definitely")
	

	return random.choice(responses)



#print(CharSelect("tech", "@menato random select tony"))