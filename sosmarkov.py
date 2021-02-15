import markovify
import random
import os
from os import listdir
import re
import datetime


def respond(message):
	try:

		if "catpop" in str(message.channel).lower():
			text_model = models["nsfw"]
		else:
			text_model = models[str(message.channel)]
	except KeyError:
		text_model = models['general']

	return answer(text_model,message.content, str(message.channel))


def answer(text_model = None, question = "", channel = ""):

	question = question.rstrip()
	subject = ""
	
	if question.rstrip().endswith("?"):
		question = question[:-1]
		subject = question.split()[-1]
	elif question.rstrip().endswith("!"):
		question = question[:-1]
		subject=random.choice(question.split())
	
	if re.search("((?i)what would .*)|((?i)how would .*)", question) or "QUOTE" in question.upper():
		for word in question.split(" "):
			for key in usermodels:
				if len(word)>2 and word.upper() in key.upper():

					if usermodels[key] == "":
						#print(f"loading model {key}")
						usermodels[key] = getmodel(f"userdata/{key}.json")

					return "\""+sentence(usermodels[key], "", channel, False)+"\" - "+word   
					
	try:
		return sentence(text_model, subject, channel, "nsfw" in channel or "memes" in channel or "catpop" in channel)
	except:
		return sentence(text_model, "", channel, "nsfw" in channel or "memes" in channel or "catpop" in channel)



def sentence(text_model = None, subject = "", channel = "", moar_images=False):

	if subject == "me": subject = "you"
	elif subject == "you": subject = "I"
	elif subject == "I": subject = "you"
	
	for i in range(50):

		if subject!="" and i<40:
			try:
				txt = text_model.make_sentence_with_start(beginning=subject, strict=False)
			except:
				txt = text_model.make_sentence()
		else:
			txt = text_model.make_sentence()
		txt = txt.replace(":.",":")
		txt = txt.replace("?.",".")
		txt = txt.replace("@","")
		c = txt.count('.')
		#print("test point 0")
		if moar_images:
			c = 0
			#print("test point 1")
			if "http" not in txt:
				for j in range(10):
					#print("test point 2")
					txt2 = text_model.make_sentence()
					if "http" in txt2:
						#print("test point 3")
						txt += ". "+txt2
						break
		
		if c<4 and len(txt)>40:
			return txt.strip('.')
	return "I Failed to generate a markov chain :c"

def getmodel(channel = "general"):
	with open(f"{channel}") as f:
		text_model = markovify.Text.from_json(f.read())
	return text_model

models = dict()
for file in listdir("channeldata"):
	if ".json" in file:
		print("LOADING: "+file)
		models[file.split('.')[0]] = getmodel("channeldata/"+file)    

usermodels = dict()
usermodelsizes = []
for file in listdir("userdata"):
	if ".json" in file:
		size = os.path.getsize("userdata/"+file)
		#print("LOADING: "+file+" "+str())
		usermodels[file.split('.')[0]] = "" # getmodel("userdata/"+file)
		usermodelsizes.append( [size, file.split('.')[0]] )

def getKey(item):
	return item[0]

usermodelsizes = sorted(usermodelsizes, key=getKey, reverse=True)
#print(usermodelsizes)


#print(answer("","quote tech", ""))