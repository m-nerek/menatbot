import random;
import urbandictionary;

preamble = ["Looking into my crystal ball I can see"]
secondpreamble = ["I can also see"]

events = ["that you will meet a", "that you will have a", "that you will fall in love with a", "you with many", "you with lots of", "you will be a", "you will be happy with a", "you will be successful at work because of your", "you making love with a", "you married to a"]
descriptors = ["girthy", "beautiful", "lovely", "majestic", "warrior", "loving", "thicc", "elegant", "manly", "buff", "voluptuous", "mighty", "saucy"]
objects = ["woman", "house", "dong", "wallet", "car", "wife", "husband", "husbando", "femboy", "bank balance", "clothing", "waifu", "mansion", "robot", "vtuber", "body pillow"]
subobjects = ["with big tits", "made of gold", "that insipires you to accomplish your goals", "that hugs you when you feel sad", "that buys you kinder eggs"]

def numberFromString(string, range):
	number=0
	for char in string:
		number += ord(char)

	print(f"number total {number} remainder from {range} = {(number%range)}")
	return (number % range)

def Future(user):

	random.seed(numberFromString(user, 32000));
	output = f"{user}... {random.choice(preamble)}"
	for a in range(2+random.randrange(2)):

		if a>0:
			output = f"{output} {random.choice(secondpreamble)}"
		
		if random.randrange(2)==0:
			output = f"{output} {random.choice(events)} {random.choice(descriptors)} {random.choice(objects)} {random.choice(subobjects)}."
		else:
			output = f"{output} {random.choice(events)} {random.choice(descriptors)} {random.choice(objects)}."
			
	return output

#print(Future("technicalty"))
