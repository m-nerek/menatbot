from string import punctuation
import random

def numberFromString(string, range):
	number=0
	for char in string:
		number += ord(char)

	return (number % range)

def respond(message):
	searchTerm = str(message.content).lower().split("who",1)[1].strip(punctuation+" ")

	id = numberFromString(searchTerm, len(message.guild.members) )

	member = message.guild.members[id].name

	responses = [" for sure!", " definitely!", "!"]

	return f"{member} {searchTerm}{random.choice(responses)}"