"""
This class contains all the information to resume and play a game from, this handles all the moves, rolls etc, and saves
the game state as we go.

"""
from menato_cyoa.dice import d6
import random

NAMES = "Aatrox,Ahri,Akali,Alistar,Amumu,Anivia,Annie,Aphelios,Ashe,Aurelion Sol,Azir,Bard,Blitzcrank,Brand,Braum,Caitlyn,Camille,Cassiopeia,Cho'Gath,Corki,Darius,Diana,Dr. Mundo,Draven,Ekko,Elise,Evelynn,Ezreal,Fiddlesticks,Fiora,Fizz,Galio,Gangplank,Garen,Gnar,Gragas,Graves,Hecarim,Heimerdinger,Illaoi,Irelia,Ivern,Janna,Jarvan IV,Jax,Jayce,Jhin,Jinx,Kai'Sa,Kalista,Karma,Karthus,Kassadin,Katarina,Kayle,Kayn,Kennen,Kha'Zix,Kindred,Kled,Kog'Maw,LeBlanc,Lee Sin,Leona,Lissandra,Lucian,Lulu,Lux,Malphite,Malzahar,Maokai,Master Yi,Miss Fortune,Mordekaiser,Morgana,Nami,Nasus,Nautilus,Neeko,Nidalee,Nocturne,Nunu and Willump,Olaf,Orianna,Ornn,Pantheon,Poppy,Pyke,Qiyana,Quinn,Rakan,Rammus,Rek'Sai,Renekton,Rengar,Riven,Rumble,Ryze,Sejuani,Senna,Sett,Shaco,Shen,Shyvana,Singed,Sion,Sivir,Skarner,Sona,Soraka,Swain,Sylas,Syndra,Tahm Kench,Taliyah,Talon,Taric,Teemo,Thresh,Tristana,Trundle,Tryndamere,Twisted Fate,Twitch,Udyr,Urgot,Varus,Vayne,Veigar,Vel'Koz,Vi,Viktor,Vladimir,Volibear,Warwick,Wukong,Xayah,Xerath,Xin Zhao,Yasuo,Yorick,Yuumi,Zac,Zed,Ziggs,Zilean,Zoe,Zyra,Lillia,Yone,Seraphine,Samira"
NAMES = NAMES.split(",")

class Character:
    def __init__(self):
        self.owner = ""

        # fluff
        self.name = ""

        # initial stats
        self.initial_luck = 0
        self.initial_stamina = 0
        self.initial_skill = 0

        # core stats
        self.luck = 0
        self.stamina = 0
        self.skill = 0

        # consumables
        self.rations = 0
        self.inventory = {}
        self.gold = 0

        # memory
        self.location = 0

        # history
        self.enemies = {}


    def roll_stats(self):
        """
        Rolling the intial value for stats
        :return:
        """
        sk1 = d6()
        st1 = d6()
        st2 = d6()
        l1 = d6()
        self.initial_luck = l1+6
        self.initial_stamina = st1+st2+12
        self.initial_skill = sk1+6
        self.skill = self.initial_skill
        self.luck = self.initial_luck
        self.stamina = self.initial_stamina
        self.name = random.choice(NAMES)
        response = f"And lo, a new adventurer approaches the mountain, {self.name}\n" \
            f"You rolled the following stats:\n" \
            f"LUCK: {self.initial_luck} (d6+6 | {l1}+6)\n" \
            f"SKILL: {self.initial_skill} (d6+6 |{sk1}+6)\n" \
            f"STAMINA: {self.initial_stamina} (2d6+12 | {st1}+{st2}+12)\n" \
            f"\n" \
            f"You can change your name by doing !rpg rename [name]"
        return response

    def print_status(self):
        """
        Return a string that contains all the information for a player in human-readable format.
        :return:
        """
        response = f"{self.name}\nLUCK:{self.luck}/{self.initial_luck}\nSKILL:{self.skill}/{self.initial_skill}\nSTAMINA:{self.stamina}/{self.initial_stamina}"
        equipment = f"You have the following equipment equipped:"
        itmes = ""
        gold = f"You have {self.gold} gold coins left"
        rations = f"You have {self.rations} rations left"
