import json
import toml
import yaml


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Conf(object):
    @staticmethod
    def parse(data):
        if type(data) is dict:
            return Conf.parse_dict(data)
        else:
            return data

    @staticmethod
    def parse_dict(data: dict) -> DotDict:
        config = DotDict()

        for key, value in data.items():
            config[key] = Conf.parse(value)

        return config

    @staticmethod
    def load_json(path: str) -> DotDict:
        with open(path, "r") as f:
            conf = Conf.parse(json.loads(f.read()))

        return conf

    @staticmethod
    def load_yaml(path: str) -> DotDict:
        with open(path, "r") as f:
            conf = Conf.parse(yaml.load(f.read(), Loader=yaml.CLoader))

        return conf

    @staticmethod
    def load_toml(path: str):
        with open(path, "r") as f:
            conf = Conf.parse(toml.load(f))

        return conf
