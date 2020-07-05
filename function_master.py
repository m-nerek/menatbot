import discord

class MenatCommand:
    def __init__(self):
        """
        Help text must explain what the command do in as few words as possible. Each help is concatenated by menat and
        newline delimited before being posted as an answer to the `help` command.
        The main bot loop will look for the first criteria to fulfill, and send the command your way.
        It's your job to then figure out which of the commands you called for.

        Write up any new menat skills as objects of *this* class, and add the filename to index.py
        (path relative to index.py)
        See: example_command.py to see how to do this.
        """
        self.help_text = ""
        self.commands_start = []
        self.commands_end = []

    def run(self):
        """
        Run must return the message menat is to send. Any random selection of messages must happen at this point.
        :return:
        message: str
        """
        return "This function hasn't been coded up yet :c"

