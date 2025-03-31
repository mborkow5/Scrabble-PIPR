import json
import os


class WordsFileNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def overwrite_save(data):
    with open("config/save.json", "w") as handle:
        json.dump(data, handle, indent=4)


def load_saved_game():
    with open("config/save.json", "r") as handle:
        data = json.load(handle)
    return data
