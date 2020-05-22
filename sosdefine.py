#pip install urbandictionary

import urbandictionary

#rand = ud.random()

#for a in rand:
#	print(a.definition)

def ireplace(old, new, text):
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(new) 
    return text

def respond(message):
	searchTerm = str(message.content).lower().split("define",1)[1].strip()

	definitions = urbandictionary.define(searchTerm)

	if len(definitions)<1:
		definitions = urbandictionary.random()

	output = definitions[0].definition.replace("[","").replace("]","")

	output = ireplace(definitions[0].word, searchTerm, output )

	return (output[:998] + '..') if len(output) > 1000 else output


