import discord
import os
import random
import sosmarkov

# todo set up logging

# Obtaining the discord key from the deployment machine
client_token = os.environ['MENAT_TOKEN']

text_model_general = sosmarkov.getmodel("general")
text_model_lobbies = sosmarkov.getmodel("lobbies")
text_model_salt = sosmarkov.getmodel("salt")
text_model_nsfw = sosmarkov.getmodel("nsfw")


class Menato(discord.Client):

    async def on_ready(self):
        """
        Ensure we can connect succesfuly, print which servers we're connected to
        """
        print(f'{self.user} has connected to discord')
        for guild in self.guilds:
            print(f'menat is connected to {guild}')


    async def on_message(self, message):
        """
        Function that runs every time a new message is sent, basically the heart of the bot
        :param message: The message object, see https://discordpy.readthedocs.io/en/latest/api.html#message
        """
        print(f'{message.guild}|{message.channel}|{message.author}: {message.content}')
        if message.mentions:
            pass
        if self.user in message.mentions:
            if "frames" in message.content:
                funny_responses = [
                    "Too bloody fast",
                    "that shit is -ob",
                    "I don't know, who labs that?",
                    "It beats my AA anyway who cares",
                    "Too fast",
                    "-3 OB +2 OH",
                    "not punishable",
                    "not reactable",
                    "play a top tier, like akumer",
                    "play a bottom tier instead, like me  <:uwu:601060544241336350>",
                    "just react bro lol",
                    "Message me later when aster bothers to add the frama data functionality"
                ]
            elif "menat op" in message.content:
                funny_responses = [
                    "can you not"
                ]
            elif "crystal ball" in message.content or "!cb" in message.content:
                funny_responses=[
                    "yes",
                    "no",
                    "It is certain",
                    "Certainly not",
                    "Maybe",
                    "Maybe not",
                    "When pigs fly",
                    "Hmm, sorry to say, it looks bad.",
                    "Yes, but you already know that",
                    "No, but you already know that",
                    "As I see it, yes",
                    "Most likely",
                    "Outlook good",
                    "ok boomer",
                    "Reply hazy, try again",
                    "Ask again later",
                    "Better not tell you now",
                    "Cannot predict now",
                    "Concentrate harder, and ask AGAIN",
                    "Don't count on it",
                    "nope",
                    "nada",
                    "nu-uh",
                    "Very doubtful",
                    "yup",
                    "Obviously, are you daft?",
                    "maybe, maybe not",
                    "only if you sacrifice your first born child",
                    "Only if you win your next ranked game",
                    "never in a thousand years",
                    "Post in nsfw, and it shall be true",
                    "Stay away from nsfw for a week, and it shall be true",
                    "hmm... I'm looking, and I'm struggling to see what the crystal ball is trying to show me about "
                    "your question... what is that blurry image... hmmm, is that...? OH GOD ITS POWAH BAWM, RUN"
                ]
            elif "?" == message.content[:-1]:
                if str(message.channel)=="lobbies":
                    funny_responses = [sosmarkov.answer(text_model_lobbies, message.content)]
                elif str(message.channel)=="salt":
                    funny_responses = [sosmarkov.answer(text_model_salt, message.content)]
                elif str(message.channel)=="nsfw":
                    funny_responses = [sosmarkov.answer(text_model_nsfw, message.content)]
                else:
                    funny_responses = [sosmarkov.answer(text_model_general, message.content)]
            else:
                funny_responses = [
                    "menat is bottom 5",
                    "Tell Tony to not be a wuss",
                    "I can't read yet, I'm just spouting crap when tagged",
                    "Guess which channel this markov chain comes from: ||Tony will never reach plat in League||",
                    "Guess which channel this markov chain comes from: ||Dom has brain damage||",
                    "Guess which channel this markov chain comes from: ||Italian food >>>>>>>>> other food||",
                    "Ok, Boomer.",
                    "I can't be bothered to listen to this",
                    "Message me later when Aster bothers to code up the bot",
                    "I'm bottom 5",
                    "I'm bottom 4",
                ]
            to_send = random.choice(funny_responses)

            await message.channel.send(to_send)

if __name__ =="__main__":
    menat = Menato()
    menat.run(client_token)
