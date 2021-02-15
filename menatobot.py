import discord
import os
import random
import sosmarkov
import sosplay
import sosdefine
import sosbet
import soshat
import sosemojicount
import sosfish
import soscharselect
import sosfuture
import sosquiz
import json
import frames
import minecraft_manage
import re
import asyncio
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
        `!bethelp` to show the betting commands
        `!fishhelp` to show the fishing commands
        `@menato !cb` to use my crystal ball
        `@menato` and end with`?` or `!` to have a chat with me 
        `@menato` otherwise for a random shitpost
        `@menato quote "user"!` to get a random quote from any, past or present SoS member. 
        `@menato groups` to list all existing groups
        `@menato popular groups` to list the groups with the most members
        `@menato ping "group"` for me to ping all the members of a group, groups can only be single words, no spaces.
        `@menato add me to "group"` to be added to a group for pings
        `@menato remove me from "group"` to be removed from a group for pings
        `@menato play "video"` to play a youtube video
        `@menato define "term"` to find out what something is
        `@menato !minecraft_info` to get the current minecraft IP address and server status
        `@menato !minecraft_start` to remotely start the server if it's not online
        `@menato list emoji rankings` to show the most/least popular emojis
        `@menato sorting hat` to be sorted into your harry potter house
        `@menato tell my fortune` to have your fortune told
        
        Feel free to ask me to reply `with context` 
        
        """
        self.mc_handler = minecraft_manage.MinecraftManager()
        self.groups = {}
        self.tagged_string = f""
        self.guild_id = ""
        with open(f'{dir_path}/responses.json', "r") as f:
            self.responses = json.load(f)
        with open(f'{dir_path}/nemph.txt', 'r') as f:
            self.nemphs = f.readlines()


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
        add_nemph = False
        self.tagged_string = f"{self.user.mention[:2]}!{self.user.mention[2:]}"
        self.guild_id = str(message.guild.id)
        print(f'{message.guild}|{message.channel}|{message.author}: {message.content}')
        responses = []
        markov = False
        if message.mentions:
            pass
        if self.user == message.author:
            return

        await sosquiz.quiz(message.author.name,message.server,message.channel, message.content)

        if message.content.startswith("!frames"):
            responses = self.frames(message)
        elif "eekum bokum" in message.content.lower():
            responses = ["eekum bokum"]
        elif message.content.startswith("!help"):
            responses = [self.help_string]
        elif message.content.startswith("!bethelp"):
            responses = [sosbet.help_string]
        elif message.content.startswith("!bet") or message.content.startswith("!concede"):
            responses = [sosbet.respond(str(message.author.name), str(message.content))]
        elif message.content.startswith("!balance") or message.content.startswith("!pay"):
            responses = [sosbet.respond(str(message.author.name), str(message.content))]
        elif message.content.startswith("!lock") or message.content.startswith("!unlock"):
            responses = [sosbet.respond(str(message.author.name), str(message.content))]
        elif message.content.startswith("!fishhelp"):
            responses = [sosfish.helpString(message.author.name)]
        elif message.content.lower().startswith("!fish"):
            #Fish(name, parameters, mention_author=None, channel=None)
            responses = [sosfish.Fish(message.author.name, message.content.lower(),message.author.mention, message.channel)]
        elif message.content.lower().startswith("!sharebait"):
            responses = [sosfish.ShareBait(message.author.name)]

        #elif message.channel.contains("nsfw") and message.contains("<@360897040986800130>"):
        #    responses = [""]
        
        elif self.user in message.mentions:
            if "menat op" in message.content:
                await message.channel.send("https://cdn.discordapp.com/attachments/750340925066051604/752632855665967204/favicon_crop1.png")
                await message.channel.send("Hmm what's this?")
                await message.channel.send("https://cdn.discordapp.com/attachments/750340925066051604/752632958153785394/unknown.png")
                await message.channel.send("What are you trying to say?")
                await message.channel.send("https://cdn.discordapp.com/attachments/750340925066051604/752633033164718100/unknown.png")
                await message.channel.send("You really out here starting shit?")
                return
            elif "nemph stream link" in message.content:
                responses = ["here you go you lazy degen: http://twitch.tv/nemphtis"]
            elif message.content.strip(f"{self.tagged_string} ").startswith("ping"):
                responses = self.ping_function(message)
            elif "can i have the n word pass?" in message.content.lower():
                if message.author.mention in ["<@238240578180087808>","<@!238240578180087808>"]: # blackbeard userID
                    responses = ["You tell me, cowboy."]
                else:
                    responses = ["No", "no way", "nope", "nu-uh"]
            elif "popular groups" in message.content.lower():
                responses = self.popular_groups()
            elif "groups" in message.content.lower():
                responses = self.all_groups()
            elif "!minecraft_info" in message.content:
                responses = self.mc_handler.server_status()
            elif "!minecraft_start" in message.content:
                responses = self.mc_handler.start_server()
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
            #elif "play" in message.content.lower():
            #    responses = [sosplay.respond(message)]
            elif "tell my fortune" in message.content.lower():
                responses = [sosfuture.Future(message.author.name)]
            elif "tell me my fortune" in message.content.lower():
                responses = [sosfuture.Future(message.author.name)]
            elif "sorting hat" in message.content.lower():
                responses = [soshat.findHouse(message.author.name)]
            elif "define" in message.content.lower():
                responses = [sosdefine.respond(message)]
            elif "list emoji rankings" in message.content.lower():
                responses = [sosemojicount.listEmoji(message.guild, message.content)]
            elif "list guild emojis" in message.content.lower():
                responses = [sosemojicount.serverEmoji(message.guild, message.content)]
            elif "test delayed response" in message.content.lower():
                asyncio.get_event_loop().create_task(self.delayed_message(message.channel, message.author, 30, self.test_response))
            elif "de kong me" in message.content.lower():
                responses = ["https://media.discordapp.net/attachments/728684452603232327/741708975539617902/kong_jr2.png"]
            elif "random select" in message.content.lower():
                responses = [soscharselect.CharSelect(message.author.name, message.content)]
            else:
                responses = self.responses['idle']

        sosemojicount.logEmoji(str(message.content), message.guild, message.author)

        if responses and "with context" in message.content.lower():
            add_nemph = True
        if responses:
            to_send = random.choice(responses)

            if markov:
                to_send = self.markov_emoji(to_send, message.guild)
            if add_nemph:
                nemph_quote = random.choice(self.nemphs)
                to_send = f"{to_send}\n{nemph_quote}"
            to_send = self.prep(to_send, message.guild)
            if isinstance(to_send, tuple) and isinstance(to_send[1], discord.embeds.Embed):
                # Hacky workaround for the output of the frames bot I poached
                await message.channel.send(embed=to_send[1])
            elif isinstance(to_send, list): # in case message is too long
                for part in to_send:
                    await message.channel.send(part) # todo I don't know if this will work :help: but that's how I think it would if it needs to
            else:
                await message.channel.send(to_send)

    async def on_reaction_add(self, reaction, user):
        #print(f"react {str(reaction)}")
        #if reaction.message not None:
        sosemojicount.logEmoji(str(reaction), reaction.message.guild, user)

    async def delayed_message(self, channel, user, delay, responseCallback):
        await asyncio.sleep(delay)
        await channel.send(responseCallback(user))

    def test_response(self, user):
        return f"{user.mention} this is {user.name}'s test delayed response"

    def add_to_group(self, message):
        """
        Function to add a user to a ping group, ping groups are stored in a .json file next to the script root.
        :param message:
        :return:
        """
        group = message.content.split()[4]
        self.get_groups()
        author = message.author.mention.replace("!", "")
        group_key = self.lowercase_group_keys.get(group.lower())

        if group_key not in self.groups.keys():
            self.groups[group] = [author]
            response = f"Made a new tagging group for you; {group}, someone can now ping me for it to tag you."
        else:
            if author in self.groups[group_key]:
                response = f"You're already in {group_key}, I will @ you when necessary."
            else:
                self.groups[group_key].append(author)
                response = f"You're added to the group {group_key} ({str(len(self.groups[group_key]))} members), I will ping you if anyone asks me to."
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
        author = message.author.mention.replace("!","")
        group_key = self.lowercase_group_keys.get(group.lower())

        if group_key not in self.groups.keys():
            response = ":bap: You buffoon, that is not a group!"
        else:
            if author not in self.groups[group_key]:
                response = ":bap: You buffoon, you absolute fool, you're not in that group!"
            else:
                self.groups[group_key].pop(self.groups[group_key].index(author))
                response = f"You have been removed from {group_key} you will be no longer pinged for it."
                if len(self.groups[group_key]) == 0:
                    self.groups.pop(group_key)
                    response = f"{response} I removed the group too now that it's empty."
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

        group_key = self.lowercase_group_keys.get(group_to_ping.lower())

        if group_key not in self.groups.keys():
            response =  ":bap: That is not a group I can ping"

            matching_keys = []
            words = group_to_ping.lower().split('_')

            if len(words)<6:
                for word in words:
                    for key in self.lowercase_group_keys:
                        for keyword in key.split('_'):
                            if len(word)>2 and len(keyword)>2:
                                if word in keyword or keyword in word:
                                    group_description = self.clean_groupname(self.lowercase_group_keys[key]) + " (" + str(len(self.groups[self.lowercase_group_keys[key]]))+")"

                                    if group_description not in matching_keys:
                                        matching_keys.append(group_description)

                if len(matching_keys)>0:
                    response = f":bap: That is not a group I can ping, did you mean any of these groups? {', '.join(sorted(matching_keys))}"

        else:
            members_to_ping = self.groups[group_key]
            response = ""
            for member in members_to_ping:
                response = f"{response} {member}"

            response = f"You're being pinged for {group_key}\n\n{response}"
        return [response]

    def clean_groupname(self, name):
        if name == "@everyone":
            name = "@ everyone"
        name = name.replace("@", "at") # fuck you you little shits
        name = name.replace("<","\<")
        return name

    def all_groups(self):
        """
        Lists all existing groups
        :return:
        """
        self.get_groups()
        clean_groups = []
        for group in self.groups.keys():
            clean_groups.append(self.clean_groupname(group))
        response = f"Groups: {', '.join(sorted(clean_groups))}."
        return [response]

    def popular_groups(self):
        """
        Lists biggest groups
        :return:
        """
        self.get_groups()
        topgroups = sorted(self.groups, key=lambda x: -len(self.groups[x]))[:25]
        clean_groups = []
        for group in topgroups:
            clean_groups.append("("+str(len(self.groups[group]))+") "+str(self.clean_groupname(group)))
        response = f"Groups: {', '.join(clean_groups)}."
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

            try:
                self.groups = groups[self.guild_id]
            except KeyError:
                self.groups = {}
            self.lowercase_group_keys = {k.lower():k for k,v in self.groups.items()}

        except FileNotFoundError:
            self.update_groups()

    def update_groups(self):
        """
        handler for updating the groups ""database""
        :return:
        """
        try:
            with open(f"{dir_path}/groups.json", "r") as file:
                try:
                    groups = json.load(file)
                except json.decoder.JSONDecodeError:
                    groups = {}
            groups[self.guild_id] = self.groups
            with open(f"{dir_path}/groups.json", "w") as file:
                json.dump(groups, file)

        except FileNotFoundError:
            with open(f"{dir_path}/groups.json", "w") as file:
                groups = {f"{self.guild_id}": self.groups}
                json.dump(groups,file)


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
                already_correct = split_send[i-1].endswith("<")

                if already_correct==False and emoji_name in emoji_names:
                    emoji_to_add = {
                        "name": f":{emoji_name}:",
                        "value": str(guild.emojis[emoji_names.index(emoji_name)])
                    }
                    emojis.append(emoji_to_add)
            i += 1

        for emoji in emojis:
            to_send = to_send.replace(emoji["name"], emoji["value"])
        return to_send
    def fix_emojis(self, to_send, guild):
        # updated regex version that hopefully fixes the issues
        emojis = []
        guild_emoji_names = [x.name for x in guild.emojis]
        # todo sorry tech, nothing personel, but the bot gotta keep on running
        #input_emojis = re.findall("(?<!<):[^:]+:", to_send)
        # The above line kept breaking for any !frames-v and when doing @menato groups
        input_emojis = []

        for emoji_name in input_emojis:
            name_without_colons = emoji_name.replace(":","")

            if name_without_colons in guild_emoji_names:
                emoji_to_add = {
                    "name": emoji_name,
                    "value": str(guild.emojis[guild_emoji_names.index(name_without_colons)])
                }
                emojis.append(emoji_to_add)

        for emoji in emojis:
            to_send = re.sub(f"(?<!<){emoji['name']}",emoji['value'], to_send)

        return to_send


    def prep(self, to_send, guild):
        """
        Hook function for later, will translate :emoji: as we type it in the bot to the appropriate <emoji:1231...>
        code compatible with discord, need to sit down and get all the messages out first.
        Returns a list of messages to send if the message is too long, this will break emojis, I'll fix this if it becomes an actual issue
        
        Tech was here, and flicked the switch to turn on the emojis :salute:
        """
        if len(to_send) > 1999:
            to_send = [to_send[i: i + 1900] for i in range(0,len(to_send), 1900)] # index notation code golf lmao

        to_send = self.fix_emojis(to_send, guild)

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
