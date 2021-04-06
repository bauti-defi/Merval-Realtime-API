import json


class AppSettings():

    def __init__(self):
        with open('config.json') as jsonFile:
            self.config = json.load(jsonFile)
