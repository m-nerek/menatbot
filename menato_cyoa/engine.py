from menato_cyoa import character

class Engine:
    def __init__(self):
        self.player = ""


    def read_instruction(self, message, player):
        # core loop, reads the message and parses out instructions, most instructions should be 1,2,3,4,5, or auxillary commands
        if message == "start":
            self.start(player)
        pass

    def read(self, player):
        pass

    def start(self, player):
        # check if player already exists, if not ask them if they want to overwrite their current game.

    def surrender(self, player):
        # remove the player's progress, start fresh.