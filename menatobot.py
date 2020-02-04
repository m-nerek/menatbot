import discord
import os
import random
import sosmarkov
import json
import frames
dir_path = os.path.dirname(os.path.realpath(__file__))
# todo set up logging

# Obtaining the discord key from the deployment machine
client_token = os.environ['MENAT_TOKEN']


class Menato(discord.Client):
    def __init__(self):
        super(Menato,self).__init__()
        self.help_string = """Commands:
        `!frames` for SFV Frame data
        `!help` to show this again
        `@menato !cb` to use my crystal ball
        `@menato` and end with`?` or `!` to have a chat with me 
        `@menato` otherwise for a random shitpost
        `@menato quote "user"!` to get a random quote from any, past or present SoS member. 
        `@menato groups` to list all existing groups
        `@menato ping "group"` for me to ping all the members of a group, groups can only be single words, no spaces.
        `@menato add me to "group"` to be added to a group for pings
        `@menato remove me from "group"` to be removed from a group for pings
        NSFW channel only:
        ||`@menato post porn!` I'll try to post porn... you filthy degenerate.||
        """
        self.groups = {}
        self.tagged_string = f""
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
        self.tagged_string = f"{self.user.mention[:2]}!{self.user.mention[2:]}"
        print(f'{message.guild}|{message.channel}|{message.author}: {message.content}')
        responses = []
        markov = False
        if message.mentions:
            pass
        if self.user == message.author:
            return
        if message.content.startswith("!frames"):
            responses = self.frames(message)
        elif message.content.startswith("!help"):
            responses = [self.help_string]
        elif self.user in message.mentions:
            if "menat op" in message.content:
                responses = ["can you not"]
            elif "nemph stream link" in message.content:
                responses = ["here you go you lazy degen: http://twitch.tv/nemphtis"]
            elif message.content.strip(f"{self.tagged_string} ").startswith("ping"):
                responses = self.ping_function(message)
            elif "can i have the n word pass?" in message.content.lower():
                if message.author.mention in ["<@238240578180087808>","<@!238240578180087808>"]: # blackbeard userID
                    responses = ["You tell me, cowboy."]
                else:
                    responses = ["No", "no way", "nope", "nu-uh"]
            elif "groups" in message.content.lower():
                responses = self.all_groups()
            elif "!ban" in message.content:
                responses = [f"Banning {message.content.split()[2]} from sending any messages for 30 minutes."]
            elif message.content.strip(f"{self.tagged_string} ").startswith("add me to"):
                responses = self.add_to_group(message)
            elif message.content.strip(f"{self.tagged_string} ").startswith("remove me from"):
                responses = self.remove_from_group(message)
            elif "crystal ball" in message.content or "!cb" in message.content:
                responses = self.responses['crystal ball']
            elif message.content.endswith('!') or message.content.endswith('?'):
                pass
                responses = [sosmarkov.respond(message)]
                markov = True # shitty workaround, sue me
            else:
                responses = self.responses['idle']
        if responses:
            to_send = random.choice(responses)
            if markov:
                to_send = self.markov_emoji(to_send, message.guild)
            to_send = self.prep(to_send)
            if isinstance(to_send, list): # in case message is too long
                for part in to_send:
                    await message.channel.send(part) # todo I don't know if this will work :help: but that's how I think it would if it needs to
            else:
                await message.channel.send(to_send)

    def add_to_group(self, message):
        """
        Function to add a user to a ping group, ping groups are stored in a .json file next to the script root.
        :param message:
        :return:
        """
        group = message.content.split()[4]
        self.get_groups()
        if group not in self.groups.keys():
            self.groups[group] = [message.author.mention]
            response = f"Made a new tagging group for you; {group}, someone can now ping me for it to tag you."

        else:
            if message.author.mention in self.groups[group]:
                response = f"You're already in {group}, I will @ you when necessary."
            else:
                self.groups[group].append(message.author.mention)
                response = f"You're added to the group {group}, I will ping you if anyone asks me to."
        self.update_groups()
        return [response]

    def remove_from_group(self, message):
        """
        Removes a user from a group, from the json stored on the disk
        :param message:
        :return:
        """
        group = message.content.split()[4]
        self.get_groups()
        if group not in self.groups.keys():
            response = ":bap: You buffoon, that is not a group!"
        else:
            if message.author.mention not in self.groups[group]:
                response = ":bap: You buffoon, you absolute fool, you're not in that group!"
            else:
                self.groups[group].pop(self.groups[group].index(message.author.mention))
                response = f"You have been removed from {group} you will be no longer pinged for it."
        self.update_groups()
        return [response]

    def ping_function(self, message):
        """
        pings all the members of a given group
        :param message:
        :return:
        """
        group_to_ping = message.content.split()[2]
        self.get_groups()
        if group_to_ping not in self.groups.keys():
            response =  ":bap: That is not a group I can ping"
        else:
            members_to_ping = self.groups[group_to_ping]
            response = ""
            for member in members_to_ping:
                response = f"{response} {member}"
            response = f"{response} You're being pinged for {group_to_ping}"
        return [response]

    def all_groups(self):
        """
        Lists all existing groups
        :return:
        """
        self.get_groups()
        response = f"Groups: {', '.join(sorted(self.groups.keys()))}.".replace("<!@","<@");
        return [response]

    def get_groups(self):
        """
        wrapper to read the groups database
        :return:
        """
        try:
            with open(f"{dir_path}/groups.json", "r") as file:
                try:
                    groups = json.load(file)
                except json.decoder.JSONDecodeError:
                    groups = {}
            self.groups = groups
        except FileNotFoundError:
            self.update_groups()

    def update_groups(self):
        """
        handler for updating the groups ""database""
        :return:
        """
        with open(f"{dir_path}/groups.json", "w") as file:
            json.dump(self.groups,file)


    def markov_emoji(self, to_send, guild):
        """
        markov chain emoji prep funciton
        :param to_send:
        :param guild:
        :return:
        """
        emojis = []
        emoji_names = [x.name for x in guild.emojis]
        split_send = to_send.split(":")
        i = 0
        while i < len(split_send):
            if i % 2 == 1:
                emoji_name = split_send[i]
                if emoji_name in emoji_names:
                    emoji_to_add = {
                        "name": f":{emoji_name}:",
                        "value": str(guild.emojis[emoji_names.index(emoji_name)])
                    }
                    emojis.append(emoji_to_add)
            i += 1

        for emoji in emojis:
            to_send = to_send.replace(emoji["name"], emoji["value"])
        return to_send


    def prep(self, to_send):
        """
        Hook function for later, will translate :emoji: as we type it in the bot to the appropriate <emoji:1231...>
        code compatible with discord, need to sit down and get all the messages out first.
        Returns a list of messages to send if the message is too long, this will break emojis, I'll fix this if it becomes an actual issue

        """
        if len(to_send) > 1999:
            to_send = to_send.split()
            to_send = [to_send[i: i + 1900] for i in range(0,len(to_send), 1900)] # index notation code golf lmao
        return to_send

    def frames(self, message):
        """
        Hook for creating a function that will return frame data on the desired move, completely gonna steal this from
        Yarshabot, for now it just returns a short meme
        """

        text = message.content
        text = text.replace("<@606796019346309120>","") # just in case
        text = text.replace("!frames","")
        text = text.strip()
        response = framesy_boye.get_frames(text,message.author.name)
        return response

if __name__ =="__main__":
    menat = Menato()
    framesy_boye = frames.Frames()
    menat.run(client_token)
