import configparser
from local_types import Vector2

config = configparser.ConfigParser()
config.read('config.ini')

def get_window_coords() -> Vector2:
    return Vector2(float(config['WINDOW']['x']), float(config['WINDOW']['y']))

def get_game_coords() -> Vector2:
    return Vector2(float(config['GAME']['x']), float(config['GAME']['y']))

def get_field_size() -> Vector2:
    return Vector2(int(config['FIELD']['width']), int(config['FIELD']['height']))
