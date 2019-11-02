import markovify

def answer(text_model = None, question = ""):
    try:
        return sentence(text_model, question.split()[-1][:-1])
    except:
        return sentence(text_model, "")

def sentence(text_model = None, subject = ""):
    for i in range(50):

        if subject!="":
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
        if(c<4 and len(txt)>40):
            return txt.strip('.')
            break;

def getmodel(channel = "general"):
    chain_data = "general_1year"
    if channel == "salt":
        chain_data = "salt_all"
    if channel == "lobbies":
        chain_data = "lobbies_all"
    if channel == "nsfw":
        chain_data = "nsfw_all"
    
    with open(chain_data+".json") as f:
        text_model = markovify.Text.from_json(f.read());
        
    return text_model
