import json
import os


class Config:
    def __init__(self, config_file=None):
        self._load_params(config_file)

    def _load_params(self, config_file):
        if config_file is None:
            config_file = self._default_file_path()

        self._map_json(self._load_json(config_file))

    def _map_json(self, data):
        self.genome_params = data["genome"]
        self.stagnation_params = data["stagnation"]
        self.reproduction_params = data["reproduction"]

    @staticmethod
    def _load_json(file_path):
        with open(file_path) as json_file:
            return json.load(json_file)

    @staticmethod
    def _default_file_path():
        curr_dir = os.path.dirname(__file__)
        return os.path.join(curr_dir, "config\default_file.json")
