import random
import json

with open('spacefacts.json') as f:
	data = json.load(f)

def SpaceFact():
	return random.choice(data)


#print(SpaceFact())