import copy
import json
import pathlib

import customtkinter as tk
    
class Settings:
    def __init__(self, file_path: str):
        self.path = pathlib.Path(file_path)
        self.logging_window = None

        with open(self.path) as f:
            self.data = json.load(f)

        self.reset()

    def __getitem__(self, name):
        return self.data[name]
    
    def get_user(self, setting):
        return self.updated_settings["user"][setting]
    
    def get_app(self, setting):
        return self.updated_settings["app"][setting]

    def set_app(self, setting, value):
        self.updated_settings["app"][setting] = value

    def set_user(self, setting, value):
        self.updated_settings["user"][setting] = value

    def reset(self):
        self.updated_settings = copy.deepcopy(self.data)

    def save(self):
        self.data = copy.deepcopy(self.updated_settings)
        with open(self.path, "w") as f:
            json.dump(self.data, f)