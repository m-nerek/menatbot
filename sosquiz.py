import urbandictionary
import sosdefine
import json
import datetime
import asyncio
import re
import sosmarkov
import sosbet
import random

with open('girl_boy_names_2005.json') as f:
	data = json.load(f)

data["girls"] = [x.lower() for x in data["girls"]]
data["boys"] = [x.lower() for x in data["boys"]]

people_words = ["friend", "person", "beautiful", "handsome", "girl", "boy", "she", "guy", "caring", "dude", "sex", "gorgeous"]
nonpeople_words = ["college", "university", "school", "town", "city"]


def UDquestion():
	definitions = urbandictionary.random()
	
	for attempts in range(10):

		for index in range(len(definitions)):
			valid = True

			words = definitions[index].word.lower().split()
			descriptionwords = definitions[index].definition.lower().split()

			if(len(words)>3):
				valid = False
				#print(f"rejected (too long) {definitions[index].word}")
				continue

			elif(len(words)>=len(descriptionwords)):
				valid = False
				#print(f"rejected (too short desc) {definitions[index].word}")
				continue

			elif(len(words)<2):
				for word in words:

					if word.lower() in data["girls"]:
						#print(f"rejected (girl) {definitions[index].word}")
						valid = False
						continue
					if word.lower() in data["boys"]:
						#print(f"rejected (boy) {definitions[index].word}")
						valid = False
						continue

				for personword in people_words:
					if personword in definitions[index].definition:
						#print(f"rejected person ({personword}) {definitions[index].word}")
						valid = False
						continue


			for nonpersonword in nonpeople_words:
				if nonpersonword in definitions[index].definition:
					#print(f"rejected nonperson ({nonpersonword}) {definitions[index].word}")
					valid = False
					continue
			if valid:
				break
		if valid:
			break

	if valid == False:
		return

	definitions[index].definition = definitions[index].definition.replace("[","").replace("]","")

	censoredoutput = sosdefine.ireplace(definitions[index].word, "[X]", definitions[index].definition )

	for word in definitions[index].word.split():
		if len(word)>2:
			censoredoutput = sosdefine.ireplace(word, "[X]", censoredoutput )

	definitions[index].censoreddef = censoredoutput
	definitions[index].questionpreamble = "--- URBAN JEOPARDY ROUND ---\n--- What is the word/phrase described by this definition? ---"
	definitions[index].questiontype = "UD"
	definitions[index].rules = ""
	definitions[index].maxguesses = 9999;
	return definitions[index]


class Object(object):
	pass

def MarkovQuestion():
	user =  random.choice(sosmarkov.usermodelsizes[:35] )[1]

	phrase = sosmarkov.answer(sosmarkov.models["nsfw"], f"quote {user}","").split('-')[0]
	phrase += "\n\n"+sosmarkov.answer(sosmarkov.models["nsfw"], f"quote {user}","").split('-')[0]
	phrase += "\n\n"+sosmarkov.answer(sosmarkov.models["nsfw"], f"quote {user}","").split('-')[0]

	question = Object()
	question.word = user
	question.censoreddef = f"{phrase}"
	question.questionpreamble = "--- WHO DAT?!? ROUND ---\n--- Who would say things like this? ---"
	question.questiontype = "MARKOV"
	question.definition = f"{phrase}"
	question.rules = "\n\nOnly 3 guesses per player allowed!"
	question.maxguesses = 3

	return question


def matchAnswer(question, attempt):

	matches = 0

	if len(attempt.split())>10:
		return 0

	for word in re.split('[^a-zA-Z]', attempt.replace("'","")):
		for word2 in re.split('[^a-zA-Z]', question.word.replace("'","")):
			if word.lower() == word2.lower():
				matches+=1

			elif question.questiontype == "MARKOV":
				if len(word)>2 and word.lower() in word2.lower():
					return 1



	if matches >= len(question.word.split()):
		return 2
	if matches >= len(question.word.split())/2:
		return 1
	return 0

def respondToCorrectAnswer(q, score, user):
	if int(score)>=2:
		output = f"{user} was correct!\n\n"
	elif int(score)>=1:
		output = f"{user} was close enough!\n\n"
	


	output = f"{output}the answer was:[{q.word}]\n\n\n{q.definition}\n\n{Score(user)}"
	return output
	
questions = {}
questiontimers = {}

scoring = Object()
scoring.scores = {}
scoring.expires = ""
scoring.max = 3
guesses = {}

def Score(user):
	global scoring
	global questionnumber

	if scoring.expires == "" or  datetime.datetime.now() > scoring.expires:
		scoring.scores = {}
		scoring.scores[user] = 1
		scoring.expires = datetime.datetime.now() + datetime.timedelta(minutes = 15)
		return f"{user} wins a point! First person to three points wins {sosbet.CURRENCY}1!"

	if user in scoring.scores.keys():
		scoring.scores[user]+=1
		if scoring.scores[user]>=scoring.max:
			scoring.expires = ""
			questionnumber=0
			scoring.count=0
			sosbet.addMoney(user,1)
			return f"{user} gets to {scoring.scores[user]} points and wins {sosbet.CURRENCY}1\nScoring is now reset"
		else:
			scoring.expires = datetime.datetime.now() + datetime.timedelta(minutes = 15)
			return f"{user} wins a point, bringing their score to {scoring.scores[user]} points total"
	else:
		scoring.scores[user] = 1
		scoring.expires = datetime.datetime.now() + datetime.timedelta(minutes = 15)
		return f"{user} wins a point! First person to three points wins {sosbet.CURRENCY}1!"

debug = False

questionnumber = 0

def trimLength(to_send):
	if len(to_send) > 1999:
		return f"{to_send[i: i + 1900]}..."
	else:
		return to_send


async def quiz(user, server, channel, text):
	global questions
	global questiontimers
	global questionnumber
	global debug
	global guesses

	if server not in questions.keys():
		questions[server] = {}
		questiontimers[server] = {}

	if channel not in questions[server].keys():
		questions[server][channel] = ""

	combinedID = f"{server}{channel}{user}"

	if combinedID not in guesses:
		guesses[combinedID] = 0

	q = questions[server][channel] 

	if q == "" and "!quiz" in text.lower():

		if (questionnumber%3)==2:
			questions[server][channel] = MarkovQuestion()
		else:
			questions[server][channel] = UDquestion()
		
		guesses = {}

		questionnumber+=1
		q = questions[server][channel]
		questiontimers[server][channel] = datetime.datetime.now() + datetime.timedelta(seconds = 30)

		if q.questiontype == "MARKOV":
			questiontimers[server][channel] = datetime.datetime.now() + datetime.timedelta(seconds = 30)

		to_send = f"{q.questionpreamble}\n\n{q.censoreddef}{q.rules}\n\nType your answers below!"

		if debug:
			to_send+=f"[{q.word}]"

		to_send = trimLength(to_send)

		if debug:
			print(to_send)
		else:
			await channel.send(to_send)

	elif q != "" and len(text.split())<6:
		score = matchAnswer(q, text)
		if int(score)>0 and guesses[combinedID]<q.maxguesses:

			to_send = respondToCorrectAnswer(q, score, user)
			to_send = trimLength(to_send)

			if debug:
				print(to_send)
			else:
				await channel.send(to_send)
			questions[server][channel] = ""
			return
		guesses[combinedID] += 1

	for s in questions.keys():
		for c in questions[s].keys():

			if questions[s][c]!="" and datetime.datetime.now()>questiontimers[s][c]:
				to_send = f"Times up! the answer was: '{questions[s][c].word}'\n\n{questions[s][c].definition}"
				to_send = trimLength(to_send)

				if debug:
					print(to_send)
				else:
					await c.send(to_send)

				questions[s][c] = ""



if debug:
	for a in range(100):
		val = input("Enter your value: ")
		asyncio.run( quiz("tech","server", "chan", val))

