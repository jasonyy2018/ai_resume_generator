import os
import json

config_file = 'config.json'

def load_config():
    if not os.path.exists(config_file):
        return None
    with open(config_file, 'r') as file:
        return json.load(file)

def save_config(config):
    with open(config_file, 'w') as file:
        json.dump(config, file)

config = load_config()