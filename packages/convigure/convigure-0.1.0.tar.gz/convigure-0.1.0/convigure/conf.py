import json
import toml


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Conf(object):
    @staticmethod
    def parse(data):
        if type(data) is dict:
            return Conf.parse_dict(data)
        elif type(data) is list:
            return Conf.parse_list(data)
        else:
            return data

    @staticmethod
    def parse_dict(data: dict) -> DotDict:
        config = DotDict()

        for key, value in data.items():
            config[key] = Conf.parse(value)

        return config

    @staticmethod
    def parse_list(data: list):
        return [Conf.parse(item) for item in data]

    @staticmethod
    def load_json(path: str) -> DotDict:
        with open(path, "r") as f:
            result = Conf.parse(json.loads(f.read()))

        return result

    @staticmethod
    def load_toml(path: str):
        with open(path, "r") as f:
            result = Conf.parse(toml.load(f))

        return result
