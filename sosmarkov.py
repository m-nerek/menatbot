import markovify
import random


def respond(message):
    try:
        text_model = models[str(message.channel)]
    except KeyError:
        text_model = models['general']

    if "turtle" in message.author.name:
        text_model = models['general_positive']
    
    return answer(text_model,message.content)


def answer(text_model = None, question = ""):

    question = question.rstrip()
    subject = ""
    
    if question.rstrip().endswith("?"):
        question = question[:-1]
        subject = question.split()[-1]
    elif question.rstrip().endswith("!"):
        question = question[:-1]
        subject=random.choice(question.split())

    if "porn" in question:
        subject=""
    
    try:
        return sentence(text_model, subject)
    except:
        return sentence(text_model, "")


def sentence(text_model = None, subject = ""):

    print("["+subject+"]")
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
        if c<4 and len(txt)>40:
            return txt.strip('.')
    return "I Failed to generate a markov chain :c";

def getmodel(channel = "general"):
    with open(f"{channel}_all.json") as f:
        text_model = markovify.Text.from_json(f.read())
    return text_model

models = {
    "general": getmodel("general"),
    "general_positive": getmodel("general_positive"),
    "lobbies": getmodel("lobbies"),
    "salt": getmodel("salt"),
    "nsfw": getmodel("nsfw")
}
