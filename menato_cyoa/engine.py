from menato_cyoa import character
from menato_cyoa.dice import d6
import json
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class Engine:
    """
    The engine class will manage the passing of engine, will store all instances of the character classes, and pass
    instructions around from the correct user to their character.
    """
    def __init__(self):
        self.characters = {}
        # todo load from disk
        self.book = {}
        self.special_rooms = []
        with open(f"{dir_path}/book.json", "r") as f:
            self.book = json.load(f)


    def read_instruction(self, message, player):
        # core loop, reads the message and parses out instructions, most instructions should be 1,2,3,4,5, or auxillary commands
        if message == "new_game":
            self.start(player) # todo
        elif message == "equipment":
            print("Show the player's equipment") # todo
        elif message == "fight":
            print("fight") # todo
        elif message == "escape":
            print("escape") # todo
        elif message == "stats":
            print("stats") # todo
        elif message == "inventory":
            print("inventory") # todo
        elif message == "test_luck":
            print("test luck") # todo
        elif message.startswith == "rename":
            print("rename") # todo
        pass

    def read(self, player):
        pass

    def start(self, player):
        new_character = character.Character()
        new_character.owner = player
        response = new_character.roll_stats()

        pass

    def surrender(self, player):
        # remove the player's progress, start fresh.
        pass

    def get_character(self, player):
        for character in self.characters:
            if character['player'] == player:
                return character['character']

    def save_character(self, player, to_save):
        for character in self.characters:
            if character['player'] == player:
                character['character'] = to_save
        # todo save on disk

    def check_room(self, player):
        """
        Core function, has all the logic to resolve all the possible encounters in a room:
        :param player:
        :return:
        """
        # get the character
        character = self.get_character(player)
        # get the room
        room = self.book[character.location]
        # check if special room
        if character.location in self.special_rooms:
            print("Do special room stuff here")

        # check if in combat
        for foe in room['foes']:
            if foe['id'] in character.enemies.keys():
                # We've fought this guy before
                current_foe = character.enemies[foe['id']]
                if current_foe['stamina'] > 0:
                    # We're fighting this guy right now.
                    print("a")
                else:
                    # He's defeated, next
                    continue
            # We've not fought this guy before, add him to seen guys, and do the first turn of combat.
            character.enemies[foe['id']] = foe
        # not in combat, check for challenges



