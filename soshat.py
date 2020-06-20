import re

house_names = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
house_regex = ["[gryfindor]","[slytherin]","[ravenclw]","[huflep]"]

def numberFromString(string, range):
	number=0
	for char in string:
		number += ord(char)

	print(f"number total {number} remainder from {range} = {(number%range)}")
	return (number % range)

def findHouse(name):

	# find the top house candidates
	totals = [0,0,0,0]

	for i in range(4):
		l = re.findall(house_regex[i], name)
		totals[i] = len(l)
	
	
	highest = max(totals[0],max(totals[1],max(totals[2],totals[3])))
	candidate_count = 0
	for i in range(4):
		if totals[i] == highest:
			candidate_count+=1

	# select house if there are multiple options
	house_id = 0
	if candidate_count>1:
		candidate_choice = numberFromString(name, candidate_count)
	else:
		candidate_choice = 0

	for i in range(4):
		if totals[i] == highest:
			if candidate_choice<=0:
				house_id = i
				break
			else:
				candidate_choice-=1

	#responds depending on the house or houses chosen

	if candidate_count>1:
		does_not_want_id = numberFromString(name+"1", candidate_count)
		if does_not_want_id == house_id:
			does_not_want_id+=1
			if does_not_want_id>3:
				does_not_want_id = 0

		return f"""The last thing {name} saw before the hat dropped over his eyes was the hall full of people craning to get a good look at him. Next second he was looking at the black inside of the hat. He waited. Hmm," said a small voice in his ear. "Difficult. Very difficult. Plenty of courage, I see. Not a bad mind either. There's talent, A my goodness, yes -- and a nice thirst to prove yourself, now that's interesting.... So where shall I put you?" {name} gripped the edges of the stool and thought, Not {house_names[does_not_want_id]}, not {house_names[does_not_want_id]}. "Not {house_names[does_not_want_id]}, eh?" said the small voice. "Are you sure? You could be great, you know, it's all here in your head, and {house_names[does_not_want_id]} will help you on the way to greatness, no doubt about that -- no? Well, if you're sure -- better be {house_names[house_id]}!"""
	

	if house_id==0:
		response_id = numberFromString(name,3)
		if response_id == 0:
			return f"""{name} almost ran to the stool and jammed the hat eagerly on her head. "GRYFFINDOR!" shouted the hat. Ron groaned."""
		elif response_id == 1:
			return f"""{name} stumbled forwards and put the Hat on his head; it was only prevented from falling right down to his shoulders by his very prominent ears. The Hat considered for a moment, then the rip near the brim opened again and shouted: 'Gryffindor!'"""
		else:
			return f"""When {name} was called, he fell over on his way to the stool. The hat took a long time to decide with {name}. When it finally shouted, "GRYFFINDOR," {name} ran off still wearing it, and had to jog back amid gales of laughter."""
	
	if house_id==1:
		return f"""{name} swaggered forward when his name was called and got his wish at once: the hat had barely touched his head when it screamed, "SLYTHERIN!". {name} went to join his friends, looking pleased with himself."""

	if house_id==2:
		return f"""{name} walked forward, visibly trembling from head to foot, picked up the Sorting Hat, put it on, and sat down on the stool. "RAVENCLAW!" shouted the hat."""

	if house_id==3:
		return f"""{name} stumbled out of line, put on the hat, which fell right down over his eyes, and sat down. A moments pause -- "HUFFLEPUFF!" shouted the hat. The table on the right cheered and clapped as {name} went to sit down at the Hufflepuff table."""



#print(findHouse("gswu"))