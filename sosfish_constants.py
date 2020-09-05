import os

SUNSET_START = 18
SUNSET_END = 21
SUNRISE_START = 6
SUNRISE_END = 9

badge_names = ["Common People", "Uncommon Phenomonon", "A Rare Talent", "Absolute Legend", "Rod God", "Fish Whisperer", "Grandmaster Angler" ]
badge_scores = [3,3,1,1,10,20,60]

dir_path = os.path.dirname(os.path.realpath(__file__))


def loadList(file, keepcaps = False):
	f = open(f"{dir_path}/fishingdata/{file}.txt", "r")

	if keepcaps==True:
		data = [line.strip() for line in f]
	else:
		data = [line.strip().lower() for line in f]

	f.close()
	return data 

herbs = loadList("herbs")
spices = loadList("spices")