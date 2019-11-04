import markovify


def answer(text_model = None, question = "", subjectAtEnd=True):
    try:
        if subjectAtEnd == True:
            return sentence(text_model, question.split()[-1][:-1])
        else:
            return sentence(text_model, random.choice(question.split()))
    except:
        return sentence(text_model, "")


def sentence(text_model = None, subject = ""):

    if subject == "me": subject = "you"
    elif subject == "you": subject = "I"
    elif subject == "I": subject = "you"
    try:
        text_model = models[text_model]
    except KeyError:
        text_model = models['general']
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
    "lobbies": getmodel("lobbies"),
    "salt": getmodel("salt"),
    "nsfw": getmodel("nsfw")
}
