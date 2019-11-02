import discord
import os
import random
import sosmarkov

# todo set up logging

# Obtaining the discord key from the deployment machine
client_token = os.environ['MENAT_TOKEN']

text_model = sosmarkov.getmodel("general")

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
            if "?" in message.content:
                
                to_send = sosmarkov.answer(text_model, message.content)
                
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
                to_send = random.choice(funny_responses)
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
