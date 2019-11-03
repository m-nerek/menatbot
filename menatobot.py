import discord
import os
import random
import sosmarkov
import json
dir_path = os.path.dirname(os.path.realpath(__file__))
# todo set up logging

# Obtaining the discord key from the deployment machine
client_token = os.environ['MENAT_TOKEN']


class Menato(discord.Client):
    def __init__(self):
        super(Menato,self).__init__()
        with open(f'{dir_path}/responses.json', "r") as f:
            self.responses = json.load(f)

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
            if "!frames" in message.content:
                responses = self.frames(message)
            elif "menat op" in message.content:
                responses = ["can you not"]
            elif "crystal ball" in message.content or "!cb" in message.content:
                responses= self.responses['crystal ball']
            elif "?" in message.content:
                responses = [sosmarkov.answer(str(message.channel),message.content)]
            else:
                responses = self.responses['idle']
            to_send = random.choice(responses)
            to_send = self.prep(to_send)
            await message.channel.send(to_send)

    def prep(self, to_send):
        """
        Hook function for later, will translate :emoji: as we type it in the bot to the appropriate <emoji:1231...>
        code compatible with discord, need to sit down and get all the messages out first
        """
        return to_send

    def frames(self, message):
        """
        Hook for creating a function that will return frame data on the desired move, completely gonna steal this from
        Yarshabot, for now it just returns a short meme
        """
        response = "can't be bothered to check, look it up yourself on FAT"
        return [response]

if __name__ =="__main__":
    menat = Menato()
    menat.run(client_token)
