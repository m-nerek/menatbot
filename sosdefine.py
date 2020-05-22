#pip install urbandictionary

import urbandictionary

#rand = ud.random()

#for a in rand:
#	print(a.definition)

def respond(message):
	searchTerm = str(message.content).lower().split("define",1)[1].strip()

	definitions = urbandictionary.define(searchTerm)

	if len(definitions)<1:
		definitions = urbandictionary.random()

	output = definitions[0].definition.replace("[","").replace("]","")

	output = output.replace(definitions[0].word, searchTerm )

	return (output[:998] + '..') if len(output) > 1000 else output
	
