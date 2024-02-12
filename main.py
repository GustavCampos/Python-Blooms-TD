import configparser
import os
from packages.game_instances.game import Game

CONFIG_PATH = os.path.join(os.getcwd(), 'config.ini')

if not os.path.isfile(CONFIG_PATH):
    generated_config = configparser.ConfigParser()
    
    generated_config.add_section('DISPLAY')
    generated_config.set('DISPLAY', 'MAX_FPS', '60')
    generated_config.set('DISPLAY', 'VSYNC_OPTION', '0')
    generated_config.set('DISPLAY', 'SCREEN_WIDTH', '800')
    generated_config.set('DISPLAY', 'SCREEN_HEIGHT', '600')

    with open('config.ini', 'w') as file:
        generated_config.write(file)
        file.close()

if __name__ == "__main__":  
    CONFIG_OPT = configparser.ConfigParser()
    CONFIG_OPT.read(CONFIG_PATH)
      
    Game(CONFIG_OPT).run()