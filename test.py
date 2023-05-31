import configparser
import os
from packages.game_instances.game import Game

CONFIG_OPT = configparser.ConfigParser()
CONFIG_OPT.read(os.path.join(os.getcwd(), 'config.ini'))

Game(CONFIG_OPT).run()

