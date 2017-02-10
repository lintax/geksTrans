import json


def load_config():
    with open('config.json') as data_file:
        return json.load(data_file)
