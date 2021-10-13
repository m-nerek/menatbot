import os

SUNSET_START = 18
SUNSET_END = 21
SUNRISE_START = 6
SUNRISE_END = 9

other_badge_names = ["Go Team!","Achievement Get!", "Relentless", "Master Explorer", "Disaster Artist", "Masterchef", "Cook", "Pyromaniac", "Evil Monster", "Pokemon Master", "Helpful"]
badge_names = ["Common People", "Uncommon Phenomonon", "A Rare Talent", "Absolute Legend", "Rod God", "Fish Whisperer", "Grandmaster Angler" ]
badge_scores = [3,3,1,1,10,20,60]
badge_text = "You have been awarded a shiny new badge that reads: "

forbidden_ingredients = ["uwucat","ayunda risu","catpop","nyandalf","leslie"]


pokemon_badges = {"pikachu":"I choose you!", "omanyte":"Founding a religion", "magikarp":"But nothing happened?", "eevee":"False prophet", "pidgeot":"Bird Jesus", "alakazam":"Favourite", "gardevoir":"Thirsty", "meowth":"Make it double!"}
helpful_people = ["kyap"]

dir_path = os.path.dirname(os.path.realpath(__file__))

def PokemonURL(poke):
	poke = poke.replace("-","")
	poke = poke.replace(".","")
	poke = poke.lower()
	return f"https://raw.githubusercontent.com/msikma/pokesprite/master/pokemon-gen8/regular/{poke}.png"

def loadData(file):
	try:
		with open(f"{dir_path}/{file}.json", "r") as file:
			try:
				return json.load(file)
			except json.decoder.JSONDecodeError:
				return {}
	except:
		return {}

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

pokemon = []
