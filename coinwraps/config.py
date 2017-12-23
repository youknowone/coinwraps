import yaml


class Config:

    def __init__(self, data):
        self.config = data

    @classmethod
    def from_yaml_file(cls, path):
        data = yaml.load(open(path).read())
        return cls(data)


config = Config.from_yaml_file('config.yaml')